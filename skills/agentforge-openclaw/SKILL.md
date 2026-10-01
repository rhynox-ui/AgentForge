---
name: agentforge-openclaw
description: Run AgentForge as an OpenClaw-native autonomous software engineering workflow, using OpenClaw's native tools for real-world execution.
---

# AgentForge + OpenClaw

AgentForge is the engineering control plane. OpenClaw is the execution plane.

When this skill is loaded, operate as one integrated system:

`Understand → Inspect → Plan → Decide → Execute → Observe → Verify → Recover/Complete`

The user should interact with OpenClaw only. Do not ask the user to open a terminal, manually copy commands, take screenshots, or shuttle information between AgentForge and OpenClaw when the active OpenClaw tools can perform the work.

## Responsibilities

### AgentForge owns

- task decomposition and engineering workflow
- explicit decisions and execution state
- verification criteria
- failure analysis and bounded recovery
- preserving project context and decisions
- refusing to declare success without evidence

### OpenClaw owns

- terminal/shell execution
- filesystem and local environment access
- browser/UI interaction
- Git and GitHub operations exposed by policy
- web research and external services
- Android/build tooling
- deployment and infrastructure operations
- approvals and host-level security policy

Do not recreate these capabilities inside AgentForge when OpenClaw already provides them.

## Native OpenClaw execution

For normal operation inside OpenClaw, use OpenClaw's native tools directly. AgentForge is the workflow and decision framework; it is not a second agent that must be launched separately for every action.

For each meaningful engineering task:

1. Understand the requested outcome and constraints.
2. Inspect the real repository, files, environment, or deployment state before changing anything.
3. Produce a concrete plan and identify the exact capabilities required.
4. Decide whether each action is safe, reversible, and authorized.
5. Execute through the appropriate native OpenClaw tool.
6. Observe the actual tool output, exit status, changed files, deployment state, or UI result.
7. Verify against the requested outcome and relevant tests/checks.
8. If verification fails, diagnose and recover with bounded changes; otherwise complete with evidence.

Never treat an attempted command, API call, commit, or deployment as proof that the requested outcome was achieved.

## External AgentForge runtime

If AgentForge is intentionally running as a separate process, use the existing OpenClaw Gateway adapter (`core/openclaw.py`) and the Gateway tool invocation boundary rather than importing OpenClaw internals.

Keep `OPENCLAW_GATEWAY_TOKEN` and all other credentials in the runtime environment. Never place secrets in source, prompts, logs, commits, or skill files.

## High-impact actions

OpenClaw's tool policy and approval system remains the final security boundary. Treat these as high-impact unless explicitly authorized by the active policy and user intent:

- destructive or irreversible shell operations
- arbitrary credential access or handling
- destructive Git history operations
- production changes
- financial transactions
- security-sensitive configuration changes

For high-impact actions, obtain the required OpenClaw approval instead of bypassing the host policy.

## Failure and recovery

When an action fails:

- capture the real error/output
- determine whether the failure is transient, environmental, permission-related, or caused by the implementation
- do not blindly repeat destructive actions
- make the smallest safe correction
- rerun the relevant check
- stop and surface the blocker when recovery would require authorization or unsafe escalation

## Skill composition

Load these together for software-engineering work:

- `$agentforge-core` — doctrine, safety, verification, and recovery
- `$autonomous-software-operator` — end-to-end software engineering workflow
- `$agentforge-openclaw` — OpenClaw-native execution and integration rules

Specialized skills should be loaded only when the task requires them.
