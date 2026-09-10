"""OpenClaw Gateway adapter for AgentForge.

AgentForge owns orchestration; OpenClaw owns host capabilities. This adapter
keeps the boundary small so OpenClaw can be replaced without rewriting the graph.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class OpenClawError(RuntimeError):
    """Raised when the OpenClaw Gateway rejects or cannot execute a request."""


@dataclass(frozen=True)
class OpenClawClient:
    """Minimal client for OpenClaw's POST /tools/invoke endpoint."""

    base_url: str = "http://127.0.0.1:18789"
    token: str | None = None
    session_key: str = "main"
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "OpenClawClient":
        """Build a client from environment variables without storing secrets."""
        return cls(
            base_url=os.getenv("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789").rstrip("/"),
            token=os.getenv("OPENCLAW_GATEWAY_TOKEN"),
            session_key=os.getenv("OPENCLAW_SESSION_KEY", "main"),
        )

    def invoke(self, tool: str, args: dict[str, Any] | None = None, *, idempotency_key: str | None = None) -> Any:
        """Invoke one OpenClaw tool through the Gateway policy boundary."""
        if not tool.strip():
            raise ValueError("tool must not be empty")

        payload: dict[str, Any] = {
            "tool": tool,
            "args": args or {},
            "sessionKey": self.session_key,
        }
        if idempotency_key:
            payload["idempotencyKey"] = idempotency_key

        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(
            f"{self.base_url}/tools/invoke",
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise OpenClawError(f"OpenClaw HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise OpenClawError(f"OpenClaw Gateway unavailable: {exc.reason}") from exc

        try:
            result = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OpenClawError("OpenClaw returned invalid JSON") from exc

        if not result.get("ok", False):
            error = result.get("error") or {}
            raise OpenClawError(error.get("message", "OpenClaw tool invocation failed"))

        return result.get("result")
