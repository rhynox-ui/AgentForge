"""State carried through an AgentForge execution."""

from typing import Literal

from typing_extensions import TypedDict


Phase = Literal[
    "understand",
    "inspect",
    "plan",
    "decide",
    "execute",
    "observe",
    "verify",
    "recover",
    "complete",
]


class AgentState(TypedDict, total=False):
    """Minimal state contract for the first AgentForge graph."""

    request: str
    phase: Phase
    plan: list[str]
    decision: str
    observations: list[str]
    verification: list[str]
    attempts: int
    status: Literal["running", "success", "needs_recovery", "blocked"]
    result: str
    error: str
