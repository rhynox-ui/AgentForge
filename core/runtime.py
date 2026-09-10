"""Public runtime entry point for AgentForge."""

from .graph import agent_graph


def run(request: str) -> dict:
    """Run the foundation graph for a user request."""
    if not request or not request.strip():
        raise ValueError("request must not be empty")

    return agent_graph.invoke(
        {
            "request": request.strip(),
            "attempts": 0,
        }
    )
