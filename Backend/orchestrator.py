"""
LangGraph StateGraph implementation for Suraksha Agent.
Minimal, typed, with conditional routing on input_type.
"""

from typing import Dict, List, Literal

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

from guidance_agent import GuidanceAgent
from message_agent import MessageAgent
from privacy_scrubber import scrub_sensitive_data
from risk_engine import RiskEngine
from url_agent import URLAgent


class SurakshaState(TypedDict):
    """Shared typed state for the Suraksha analysis graph."""

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
    """Node: Scrub sensitive data from raw input."""
    state["scrubbed_text"] = scrub_sensitive_data(state["raw_text"] or "")
    return state


def message_agent(state: SurakshaState) -> SurakshaState:
    """Node: Analyze scrubbed text as a message."""
    analysis = MESSAGE_AGENT.analyze(state["scrubbed_text"])
    state["detected_category"] = analysis["category"]
    state["risk_score"] = float(analysis["risk_score"])
    state["reasons"] = [scrub_sensitive_data(r) for r in analysis.get("reasons", [])]
    state["suspicious_flags"] = []
    return state


def url_agent(state: SurakshaState) -> SurakshaState:
    """Node: Analyze scrubbed text as a URL."""
    analysis = URL_AGENT.analyze(state["scrubbed_text"])
    state["detected_category"] = analysis["category"]
    state["risk_score"] = float(analysis["risk_score"])
    state["reasons"] = [scrub_sensitive_data(r) for r in analysis.get("reasons", [])]
    state["suspicious_flags"] = analysis.get("flags", [])
    return state


def risk_scoring(state: SurakshaState) -> SurakshaState:
    """Node: Normalize severity from risk score for consistent downstream behavior."""
    state["severity"] = RISK_ENGINE.calculate_severity(float(state["risk_score"]))
    return state


def guidance_agent(state: SurakshaState) -> SurakshaState:
    """Node: Generate guidance based on analysis."""
    state["advice"] = GUIDANCE_AGENT.get_detailed_guidance(
        category=state["detected_category"],
        risk_score=state["risk_score"],
        severity=state["severity"],
        reasons=state["reasons"],
    )
    return state


def route_on_input_type(state: SurakshaState) -> Literal["message_agent", "url_agent"]:
    """Conditional router: split on input_type."""
    if state["input_type"] == "url":
        return "url_agent"
    return "message_agent"


def build_suraksha_graph() -> StateGraph:
    """Build and return the Suraksha analysis StateGraph."""
    graph = StateGraph(SurakshaState)

    # Add nodes
    graph.add_node("scrub_input", scrub_input)
    graph.add_node("message_agent", message_agent)
    graph.add_node("url_agent", url_agent)
    graph.add_node("risk_scoring", risk_scoring)
    graph.add_node("guidance_agent", guidance_agent)

    # Add edges: START -> scrub -> conditional route
    graph.add_edge(START, "scrub_input")
    graph.add_conditional_edges("scrub_input", route_on_input_type, {
        "message_agent": "message_agent",
        "url_agent": "url_agent",
    })

    # Both analysis nodes lead to risk scoring, then guidance
    graph.add_edge("message_agent", "risk_scoring")
    graph.add_edge("url_agent", "risk_scoring")
    graph.add_edge("risk_scoring", "guidance_agent")

    # guidance leads to END
    graph.add_edge("guidance_agent", END)

    return graph.compile()


SURAKSHA_APP = build_suraksha_graph()


def analyze_input(raw_text: str, input_type: Literal["message", "url"] = "message") -> Dict:
    """
    Analyze input text using the Suraksha StateGraph.
    
    Args:
        raw_text: The text or URL to analyze.
        input_type: Either "message" or "url".
    
    Returns:
        Final state as a dictionary.
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
    sample = analyze_input("Click here to verify your account: https://example.com/login", "message")
    print(sample)