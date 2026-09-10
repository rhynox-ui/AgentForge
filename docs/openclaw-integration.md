# OpenClaw integration

AgentForge uses OpenClaw as its preferred execution layer. OpenClaw provides the tools; AgentForge provides orchestration, planning, verification, and recovery.

## Local setup

OpenClaw's Gateway is normally available on the local host. Configure AgentForge with environment variables:

```bash
export OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
export OPENCLAW_GATEWAY_TOKEN='your-local-gateway-token'
export OPENCLAW_SESSION_KEY=main
```

Do not commit the token.

## Calling a tool

```python
from core.openclaw import OpenClawClient

client = OpenClawClient.from_env()
result = client.invoke("sessions_list", {"limit": 5})
print(result)
```

The adapter sends the request to OpenClaw's Gateway `/tools/invoke` endpoint. OpenClaw still applies its configured tool policy, so AgentForge does not bypass the host runtime's capability controls.

## Skills

AgentForge's `skills/` directory follows the OpenClaw `SKILL.md` format. OpenClaw can load these skills from a workspace skills root. The recommended arrangement is to make the AgentForge skills available in the OpenClaw workspace rather than maintaining a second, divergent copy.

For a local checkout, configure OpenClaw's `skills.load.extraDirs` to include the AgentForge `skills/` directory, or copy/install the selected skills into the OpenClaw workspace. Workspace skills have higher precedence than lower-priority skill roots.

Recommended initial skill set:

- `agentforge-core`
- `autonomous-software-operator`
- `agentforge-openclaw`

Add specialized skills only when a task needs them.

## Architecture

```text
User request
    |
    v
AgentForge / LangGraph
    |  plan / decide / verify / recover
    v
OpenClaw adapter
    |
    v
OpenClaw Gateway
    |
    +--> terminal / files
    +--> browser / web
    +--> Git / GitHub
    +--> deployment / infrastructure
    +--> other enabled tools and skills
```

The adapter is intentionally small. If OpenClaw changes its transport later, the integration boundary can change without rewriting AgentForge's orchestration graph.
