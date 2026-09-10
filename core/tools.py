"""Tool registry and safe built-in developer tools for AgentForge."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from langchain_core.tools import BaseTool, StructuredTool


def _read_file(path: str, max_chars: int = 20000) -> str:
    """Read a UTF-8 text file, bounded to avoid unbounded context growth."""
    target = Path(path).expanduser().resolve()
    if not target.is_file():
        raise FileNotFoundError(f"Not a file: {target}")
    return target.read_text(encoding="utf-8")[:max_chars]


def _list_directory(path: str = ".") -> str:
    """List one directory without recursively traversing it."""
    target = Path(path).expanduser().resolve()
    if not target.is_dir():
        raise NotADirectoryError(f"Not a directory: {target}")
    entries = sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    return "\n".join(f"{'[DIR] ' if p.is_dir() else '[FILE]'}{p.name}" for p in entries)


def _search_text(query: str, path: str = ".", max_results: int = 50) -> str:
    """Search UTF-8 text files below a directory, skipping common build metadata."""
    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    ignored = {".git", ".venv", "node_modules", "dist", "build", "__pycache__"}
    results: list[str] = []
    for file in root.rglob("*"):
        if len(results) >= max_results or not file.is_file() or any(part in ignored for part in file.parts):
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if query.lower() in line.lower():
                results.append(f"{file}:{number}: {line.strip()}")
                if len(results) >= max_results:
                    break
    return "\n".join(results) or "No matches found."


def build_builtin_tools() -> list[BaseTool]:
    """Return the initial read-only tool set.

    Mutating tools will be added behind an explicit capability/approval policy.
    """
    return [
        StructuredTool.from_function(
            func=_read_file,
            name="read_file",
            description="Read a UTF-8 text file. Use this to inspect source/configuration files.",
        ),
        StructuredTool.from_function(
            func=_list_directory,
            name="list_directory",
            description="List entries in a directory without recursive traversal.",
        ),
        StructuredTool.from_function(
            func=_search_text,
            name="search_text",
            description="Search UTF-8 text files under a directory for a case-insensitive string.",
        ),
    ]


class ToolRegistry:
    """Central registry used by the graph and future OpenClaw adapters."""

    def __init__(self, tools: list[BaseTool] | None = None) -> None:
        self._tools: dict[str, BaseTool] = {tool.name: tool for tool in (tools or build_builtin_tools())}

    def all(self) -> list[BaseTool]:
        return list(self._tools.values())

    def get(self, name: str) -> BaseTool:
        return self._tools[name]

    def add(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool
