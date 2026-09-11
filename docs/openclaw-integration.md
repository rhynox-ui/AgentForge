# OpenClaw integration

AgentForge uses OpenClaw as its preferred execution layer. OpenClaw provides the real-world tools and host runtime; AgentForge provides the engineering workflow, planning discipline, verification, and recovery rules.

## Native mode — recommended

The normal user experience is:

```text
User → OpenClaw → AgentForge skills → OpenClaw native tools → verification → result
```

Install/load the AgentForge skills once, then interact with OpenClaw normally. There is no need to start a separate AgentForge process for every task.

Configure OpenClaw to load the local AgentForge skills directory with `skills.load.extraDirs`:

```json5
{
  skills: {
    load: {
      extraDirs: ["/absolute/path/to/AgentForge/skills"],
      watch: true,
    },
  },
}
```

Recommended skills:

- `agentforge-core`
- `autonomous-software-operator`
- `agentforge-openclaw`

The `agentforge-openclaw` skill tells OpenClaw to use its native terminal, filesystem, browser, Git/GitHub, Android, build, deployment, and other enabled capabilities directly. AgentForge therefore does not need to duplicate host tooling.

## External runtime mode

When AgentForge is intentionally running as a separate Python process, configure:

```bash
export OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
export OPENCLAW_GATEWAY_TOKEN='your-local-gateway-token'
export OPENCLAW_SESSION_KEY=main
```

Do not commit the token.

Call the Gateway through the existing adapter:

```python
from core.openclaw import OpenClawClient

client = OpenClawClient.from_env()
result = client.invoke("sessions_list", {"limit": 5})
print(result)
```

The adapter uses OpenClaw's Gateway `/tools/invoke` boundary. OpenClaw remains responsible for tool policy, approvals, authentication, and host security controls.

## Operational contract

For software-engineering work, the integrated system follows:

```text
Understand
    ↓
Inspect real state
    ↓
Plan
    ↓
Decide + authorize
    ↓
Execute with OpenClaw
    ↓
Observe actual result
    ↓
Verify
    ↓
Recover safely or complete
```

Never declare success from an attempted action alone. Verify the actual files, command results, tests, UI state, deployment state, or other evidence relevant to the task.

## Security boundary

OpenClaw's tool policy and approval system is the final host-level security boundary. AgentForge must not bypass it.

Treat destructive shell commands, arbitrary credential handling, destructive Git operations, production changes, financial actions, and other irreversible operations as high-impact. Use the OpenClaw approval flow when required.

Never place `OPENCLAW_GATEWAY_TOKEN` or other credentials in source code, prompts, skill files, logs, or commits.

## Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      OpenClaw       │
                    │ host + tools + auth │
                    └──────────┬──────────┘
                               │ loads
                               ▼
                    ┌─────────────────────┐
                    │  AgentForge Skills  │
                    │ workflow + doctrine │
                    └──────────┬──────────┘
                               │ selects capability
                               ▼
                    ┌─────────────────────┐
                    │ OpenClaw native     │
                    │ tools / integrations│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Observe + Verify    │
                    └──────────┬──────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
                  Recover             Complete
```

The Python Gateway adapter remains available for external AgentForge processes and tests. Native OpenClaw mode is the preferred path for the everyday user experience because it avoids a second competing agent runtime and avoids unnecessary nested Gateway calls.
