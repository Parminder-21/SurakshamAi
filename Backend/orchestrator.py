"""
LangGraph StateGraph implementation for Suraksha Agent.
Implements the 'Shared Risk Registry' where URL Agent and Message Agent coordinate.
"""

from typing import Dict, List, Literal
import re

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

from guidance_agent import GuidanceAgent
from message_agent import MessageAgent
from privacy_scrubber import scrub_sensitive_data
from risk_engine import RiskEngine
from url_agent import URLAgent


class SurakshaState(TypedDict):
    """Shared typed state for the Suraksha analysis graph (The Shared Risk Registry)."""
    input_type: Literal["message", "url"]
    raw_text: str
    scrubbed_text: str
    detected_category: str
    risk_score: float
    reasons: List[str]
    suspicious_flags: List[str]
    advice: str
    severity: str


MESSAGE_AGENT = MessageAgent()
URL_AGENT = URLAgent()
GUIDANCE_AGENT = GuidanceAgent()
RISK_ENGINE = RiskEngine()


def scrub_input(state: SurakshaState) -> SurakshaState:
    """Node 1: Scrub sensitive data from raw input before analysis."""
    state["scrubbed_text"] = scrub_sensitive_data(state["raw_text"] or "")
    return state


def url_agent(state: SurakshaState) -> SurakshaState:
    """Node 2: Analyze URL. If input is a message, extract all links and analyze them."""
    if state["input_type"] == "url":
        analysis = URL_AGENT.analyze(state["scrubbed_text"])
        state["detected_category"] = analysis["category"]
        state["risk_score"] = float(analysis["risk_score"])
        state["reasons"] = [scrub_sensitive_data(r) for r in analysis.get("reasons", [])]
        state["suspicious_flags"] = analysis.get("flags", [])
    else:
        # It's a message. Extract URLs to build shared intelligence.
        urls = re.findall(r'(https?://\S+|www\.\S+|bit\.ly\S+|tinyurl\.com\S+)', state["scrubbed_text"], re.IGNORECASE)
        all_reasons = state.get("reasons", [])
        all_flags = state.get("suspicious_flags", [])
        
        highest_url_risk = 0.0
        for u in urls:
            ans = URL_AGENT.analyze(u)
            all_reasons.extend(ans.get("reasons", []))
            all_flags.extend(ans.get("flags", []))
            if ans["risk_score"] > highest_url_risk:
                highest_url_risk = ans["risk_score"]
                state["detected_category"] = ans["category"]
                
        state["suspicious_flags"] = list(set(all_flags))
        state["reasons"] = list(set([scrub_sensitive_data(r) for r in all_reasons]))
        state["risk_score"] = highest_url_risk # Baseline risk from URLs
        
    return state


def message_agent(state: SurakshaState) -> SurakshaState:
    """Node 3: Analyze text. Uses intelligence gathered by URL Agent."""
    analysis = MESSAGE_AGENT.analyze(state["scrubbed_text"])
    
    # If the message agent detects a scam category, it overrides the URL agent's category
    if analysis["category"] != "safe":
        state["detected_category"] = analysis["category"]
        
    # The message_agent calculates its own risk_score based on text.
    # We take the maximum risk between the text content and the embedded URLs.
    message_risk = float(analysis["risk_score"])
    if message_risk > state["risk_score"]:
        state["risk_score"] = message_risk
        
    reasons = state.get("reasons", [])
    reasons.extend([scrub_sensitive_data(r) for r in analysis.get("reasons", [])])
    state["reasons"] = list(set(reasons))
    
    return state


def risk_scoring(state: SurakshaState) -> SurakshaState:
    """Node 4: Normalize severity from the final risk score."""
    state["severity"] = RISK_ENGINE.calculate_severity(float(state["risk_score"]))
    return state


def guidance_agent(state: SurakshaState) -> SurakshaState:
    """Node 5: Generate prevention guidance."""
    state["advice"] = GUIDANCE_AGENT.get_detailed_guidance(
        category=state["detected_category"],
        risk_score=state["risk_score"],
        severity=state["severity"],
        reasons=state["reasons"],
    )
    return state


def route_after_url(state: SurakshaState) -> Literal["message_agent", "risk_scoring"]:
    """Conditional router: messages go to message_agent, URLs go straight to risk_scoring."""
    if state["input_type"] == "message":
        return "message_agent"
    return "risk_scoring"


def build_suraksha_graph() -> StateGraph:
    """Build and return the Coordinated Suraksha analysis StateGraph."""
    graph = StateGraph(SurakshaState)

    # Add nodes
    graph.add_node("scrub_input", scrub_input)
    graph.add_node("url_agent", url_agent)
    graph.add_node("message_agent", message_agent)
    graph.add_node("risk_scoring", risk_scoring)
    graph.add_node("guidance_agent", guidance_agent)

    # Edge logic
    graph.add_edge(START, "scrub_input")
    
    # After scrubbing, ALWAYS run the URL Agent first (to check links even in messages)
    graph.add_edge("scrub_input", "url_agent")
    
    # After URL Agent, route conditionally
    graph.add_conditional_edges("url_agent", route_after_url, {
        "message_agent": "message_agent",
        "risk_scoring": "risk_scoring",
    })

    # Message Agent goes to Risk Scoring
    graph.add_edge("message_agent", "risk_scoring")
    
    # Risk Scoring to Guidance
    graph.add_edge("risk_scoring", "guidance_agent")
    graph.add_edge("guidance_agent", END)

    return graph.compile()


SURAKSHA_APP = build_suraksha_graph()


def analyze_input(raw_text: str, input_type: Literal["message", "url"] = "message") -> Dict:
    """
    Analyze input text using the coordinated LangGraph orchestrator.
    """
    initial_state: SurakshaState = {
        "input_type": input_type,
        "raw_text": raw_text,
        "scrubbed_text": "",
        "detected_category": "safe",
        "risk_score": 0.0,
        "reasons": [],
        "suspicious_flags": [],
        "advice": "",
        "severity": "safe",
    }
    result = SURAKSHA_APP.invoke(initial_state)
    return result


if __name__ == "__main__":
    sample = analyze_input("Dear Customer, your electricity bill is unpaid. Pay via https://bit.ly/malicious-link immediately!", "message")
    import json
    print(json.dumps(sample, indent=2))