import json
from urllib.error import HTTPError

import pytest

from core.openclaw import OpenClawClient, OpenClawError


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def test_openclaw_client_invokes_gateway(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["headers"] = dict(request.headers)
        captured["body"] = json.loads(request.data.decode())
        captured["timeout"] = timeout
        return FakeResponse({"ok": True, "result": {"status": "ok"}})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    client = OpenClawClient(
        base_url="http://127.0.0.1:18789",
        token="test-token",
        session_key="agent:main:main",
    )
    result = client.invoke("sessions_list", {"limit": 1}, idempotency_key="abc")

    assert result == {"status": "ok"}
    assert captured["url"] == "http://127.0.0.1:18789/tools/invoke"
    assert captured["headers"]["Authorization"] == "Bearer test-token"
    assert captured["body"] == {
        "tool": "sessions_list",
        "args": {"limit": 1},
        "sessionKey": "agent:main:main",
        "idempotencyKey": "abc",
    }


def test_openclaw_client_surfaces_gateway_errors(monkeypatch):
    def fake_urlopen(request, timeout):
        raise HTTPError(
            request.full_url,
            403,
            "Forbidden",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    with pytest.raises(OpenClawError, match="OpenClaw HTTP 403"):
        OpenClawClient().invoke("browser", {})
