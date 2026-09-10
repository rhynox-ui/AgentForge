"""LangGraph execution graph for AgentForge v0.1."""

from langgraph.graph import END, START, StateGraph

from .nodes import decide, execute, inspect, observe, plan, understand, verify
from .state import AgentState


def build_graph():
    """Build and compile the deterministic foundation graph."""
    builder = StateGraph(AgentState)

    builder.add_node("understand", understand)
    builder.add_node("inspect", inspect)
    builder.add_node("plan", plan)
    builder.add_node("decide", decide)
    builder.add_node("execute", execute)
    builder.add_node("observe", observe)
    builder.add_node("verify", verify)

    builder.add_edge(START, "understand")
    builder.add_edge("understand", "inspect")
    builder.add_edge("inspect", "plan")
    builder.add_edge("plan", "decide")
    builder.add_edge("decide", "execute")
    builder.add_edge("execute", "observe")
    builder.add_edge("observe", "verify")
    builder.add_edge("verify", END)

    return builder.compile()


agent_graph = build_graph()
