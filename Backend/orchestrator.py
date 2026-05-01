"""
LangGraph StateGraph implementation for Suraksha Agent.
Minimal, typed, with conditional routing on input_type.
"""

from typing import Dict, Literal

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
    reasons: list
    advice: str
    severity: str


def scrub_input(state: SurakshaState) -> SurakshaState:
    """Node: Scrub sensitive data from raw input."""
    state["scrubbed_text"] = scrub_sensitive_data(state["raw_text"] or "")
    return state


def message_agent(state: SurakshaState) -> SurakshaState:
    """Node: Analyze scrubbed text as a message."""
    agent = MessageAgent()
    analysis = agent.analyze(state["scrubbed_text"])
    state["detected_category"] = analysis["category"]
    state["risk_score"] = float(analysis["risk_score"])
    state["reasons"] = [scrub_sensitive_data(r) for r in analysis.get("reasons", [])]
    engine = RiskEngine()
    state["severity"] = engine.calculate_severity(state["risk_score"])
    return state


def url_agent(state: SurakshaState) -> SurakshaState:
    """Node: Analyze scrubbed text as a URL."""
    agent = URLAgent()
    analysis = agent.analyze(state["scrubbed_text"])
    state["detected_category"] = analysis["category"]
    state["risk_score"] = float(analysis["risk_score"])
    state["reasons"] = [scrub_sensitive_data(r) for r in analysis.get("reasons", [])]
    state["severity"] = analysis.get("severity", "safe")
    return state


def guidance_agent(state: SurakshaState) -> SurakshaState:
    """Node: Generate guidance based on analysis."""
    agent = GuidanceAgent()
    state["advice"] = agent.get_detailed_guidance(
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
    graph.add_node("guidance_agent", guidance_agent)

    # Add edges: START -> scrub -> conditional route
    graph.add_edge(START, "scrub_input")
    graph.add_conditional_edges("scrub_input", route_on_input_type, {
        "message_agent": "message_agent",
        "url_agent": "url_agent",
    })

    # Both analysis nodes lead to guidance
    graph.add_edge("message_agent", "guidance_agent")
    graph.add_edge("url_agent", "guidance_agent")

    # guidance leads to END
    graph.add_edge("guidance_agent", END)

    return graph.compile()


def analyze_input(raw_text: str, input_type: Literal["message", "url"] = "message") -> Dict:
    """
    Analyze input text using the Suraksha StateGraph.
    
    Args:
        raw_text: The text or URL to analyze.
        input_type: Either "message" or "url".
    
    Returns:
        Final state as a dictionary.
    """
    app = build_suraksha_graph()
    initial_state: SurakshaState = {
        "input_type": input_type,
        "raw_text": raw_text,
        "scrubbed_text": "",
        "detected_category": "safe",
        "risk_score": 0.0,
        "reasons": [],
        "advice": "",
        "severity": "safe",
    }
    result = app.invoke(initial_state)
    return result


if __name__ == "__main__":
    sample = analyze_input("Click here to verify your account: https://example.com/login", "message")
    print(sample)