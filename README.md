# AgentForge

AgentForge is a model-agnostic autonomous software engineering runtime designed to operate through OpenClaw and other tool environments.

## Design

AgentForge separates four concerns:

- **Skills** — engineering workflows and operating doctrine.
- **Graph** — stateful orchestration and control flow.
- **Tools** — real-world capabilities supplied by the host runtime.
- **Memory** — durable state, project context, decisions, and execution history.

The target workflow is:

`Understand → Inspect → Plan → Decide → Execute → Observe → Verify → Recover/Complete`

## Current status

v0.1 contains a deterministic LangGraph foundation. It intentionally does not pretend to have external tool access yet. The next layers will connect model-backed planning, tool selection, OpenClaw adapters, persistent checkpoints, and verification/recovery loops.

## Development

Python 3.10+ is supported. Install the package and development dependencies, then run:

```bash
pip install -e '.[dev]'
pytest
python -m core "Build a software agent"
```

## Philosophy

AgentForge should be autonomous without being reckless: it should make ordinary engineering decisions itself, use the most direct available tool, verify actual results, recover from failures, and require appropriate authorization for irreversible high-impact actions.
