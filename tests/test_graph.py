from core.runtime import run


def test_foundation_graph_completes():
    result = run("Build a software agent")

    assert result["status"] == "success"
    assert result["phase"] == "complete"
    assert result["request"] == "Build a software agent"
    assert result["plan"]
    assert result["verification"]
