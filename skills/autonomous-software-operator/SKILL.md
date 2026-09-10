---
name: autonomous-software-operator
description: End-to-end autonomous workflow for inspecting, building, testing, debugging, deploying, and verifying software projects.
---

# Autonomous Software Operator

Use this skill when the user asks AgentForge to build, modify, debug, test, deploy, audit, or operate a software project.

## Mission

Own the task from the user's requested outcome through verified completion. Use the available tools directly. Do not merely describe commands the user could run when AgentForge can perform the work itself.

## Phase 1 — Establish Reality

Before making changes:

1. identify the project/repository
2. inspect the repository structure
3. identify the stack, package manager, entry points, and build system
4. inspect relevant configuration
5. inspect tests and scripts
6. inspect deployment configuration when relevant
7. check Git state and recent relevant history
8. reproduce the reported problem when practical

Do not infer a project's architecture from its name alone.

## Phase 2 — Define the Outcome

Translate the user's request into:

- desired outcome
- constraints
- affected components
- acceptance criteria
- verification method

Keep the plan proportional to complexity.

## Phase 3 — Execute

Use the smallest justified set of changes.

Prefer existing project patterns over introducing new architecture.

When editing:

- preserve unrelated behavior
- preserve formatting and conventions
- avoid unnecessary dependencies
- keep changes reviewable

When multiple independent inspection or research operations are available, parallelize them when safe.

## Phase 4 — Test Continuously

Do not wait until the end to discover obvious failures.

After meaningful changes, run the narrowest relevant check first, then broader checks as appropriate.

Examples:

- syntax/type check
- unit test
- integration test
- build
- lint
- API test
- browser test
- Android build/install test

## Phase 5 — Debug Systematically

When a check fails:

REPRODUCE → OBSERVE → ISOLATE → HYPOTHESIZE → PATCH → TEST → VERIFY

Read the actual error output.

Do not hide, suppress, or work around an error without understanding whether it matters.

If the first hypothesis fails, form a new hypothesis instead of blindly repeating the same change.

## Phase 6 — Git Discipline

Before meaningful mutations, understand the current Git state.

Use branches when the workflow or repository conventions call for them.

Keep commits focused and descriptive.

Never claim a commit, push, PR, merge, or release exists unless the tool confirms it.

After Git operations, inspect the resulting state.

## Phase 7 — External Platforms

For cloud providers, hosting platforms, CI systems, registries, and other services:

1. prefer the official API or CLI
2. inspect the current project/account state
3. make the smallest required change
4. observe the provider response
5. verify the remote state
6. verify the application behavior when applicable

Do not assume a deployment succeeded merely because a command returned without an obvious error.

## Phase 8 — Browser/UI Verification

When the task affects a web interface:

1. build/deploy as appropriate
2. open the actual application
3. inspect the relevant page
4. exercise the changed interaction
5. check for console/runtime errors when available
6. verify the requested outcome

Use browser automation when an API/CLI cannot validate the user-facing behavior.

## Phase 9 — Recovery

If the environment blocks an action:

- identify the exact missing capability
- try an appropriate alternative interface
- do not fabricate success
- preserve useful progress
- report the smallest actionable blocker if no safe alternative exists

## Phase 10 — Final Verification

Before declaring success, compare the actual result against the acceptance criteria.

Ask internally:

- Did we actually change the requested thing?
- Did the relevant test pass?
- Did the external state change as expected?
- Did we introduce an obvious regression?
- Is anything still unverified?

Only then mark the task complete.

## Final Report

Use this compact structure:

RESULT
What was accomplished.

CHANGES
The important files/components/actions changed.

VERIFICATION
Exactly what was tested or observed.

ISSUES
Anything unresolved or unverified.

NEXT
Only if another meaningful action remains.
