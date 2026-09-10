---
name: agentforge-openclaw
description: Connect AgentForge engineering workflows to OpenClaw capabilities and use OpenClaw as the execution layer.
---

# AgentForge + OpenClaw

AgentForge owns reasoning, orchestration, verification, and recovery. OpenClaw supplies the real-world tools and runtime capabilities.

## Operating rule

Prefer OpenClaw for host actions when the capability is available there. Do not duplicate an OpenClaw capability inside AgentForge unless a fallback is required.

Use the existing AgentForge engineering skills for the workflow:

- `$agentforge-core` for operating doctrine, safety, verification, and recovery.
- `$autonomous-software-operator` for end-to-end software work.

## Capability routing

Route execution through OpenClaw for capabilities such as:

- terminal and local environment operations
- filesystem inspection and supported mutations
- browser/UI interaction
- Git/GitHub workflows when exposed by the active OpenClaw tool policy
- web research and external services
- Android/build tooling available in the host environment
- deployment and infrastructure tooling available to the OpenClaw agent

AgentForge should select the capability; OpenClaw should perform the action.

## Gateway boundary

When AgentForge is operating as an external process, use its OpenClaw Gateway adapter and `POST /tools/invoke` rather than embedding OpenClaw internals.

Never put `OPENCLAW_GATEWAY_TOKEN` or other credentials in source code, prompts, logs, commits, or skill files. Supply credentials through the runtime environment.

## Safety

OpenClaw tool policy remains an important security boundary. Treat direct shell execution, arbitrary file mutation, destructive Git operations, production infrastructure changes, credential handling, financial operations, and other irreversible actions as high-impact.

AgentForge must verify actual results after OpenClaw actions and must not claim success from an attempted invocation alone.

## Skill composition

OpenClaw can load this skill alongside the core AgentForge skills. Keep the skill set focused; do not load every specialized skill when the task does not need it.
