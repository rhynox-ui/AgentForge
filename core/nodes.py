"""First deterministic AgentForge graph nodes.

These nodes deliberately avoid an LLM dependency. The next layer will inject a
model-backed planner/decision engine while keeping the state machine stable.
"""

from .state import AgentState


def understand(state: AgentState) -> dict:
    request = state["request"].strip()
    return {
        "request": request,
        "phase": "inspect",
        "status": "running",
        "observations": [f"Received task: {request}"],
    }


def inspect(state: AgentState) -> dict:
    return {
        "phase": "plan",
        "observations": state.get("observations", [])
        + ["Initial inspection checkpoint reached."],
    }


def plan(state: AgentState) -> dict:
    return {
        "phase": "decide",
        "plan": [
            "Understand the requested outcome and constraints.",
            "Select the smallest set of tools needed to execute it.",
            "Execute the work and observe actual results.",
            "Verify the result against the acceptance criteria.",
        ],
    }


def decide(state: AgentState) -> dict:
    return {
        "phase": "execute",
        "decision": "Proceed with the planned workflow; tool-backed execution will be connected next.",
    }


def execute(state: AgentState) -> dict:
    return {
        "phase": "observe",
        "observations": state.get("observations", [])
        + ["Execution boundary reached; no external tool was invoked in v0.1."],
    }


def observe(state: AgentState) -> dict:
    return {
        "phase": "verify",
        "observations": state.get("observations", [])
        + ["Execution output was observed by the runtime."],
    }


def verify(state: AgentState) -> dict:
    """Route to completion for the deterministic foundation graph."""
    return {
        "phase": "complete",
        "status": "success",
        "verification": ["Graph reached the verification node successfully."],
        "result": "AgentForge execution graph completed its foundation workflow.",
    }
