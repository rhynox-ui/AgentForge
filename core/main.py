"""CLI entry point for the AgentForge foundation runtime."""

import json
import sys

from .runtime import run


def main() -> int:
    request = " ".join(sys.argv[1:]).strip()
    if not request:
        print("Usage: python -m core <task>", file=sys.stderr)
        return 2

    result = run(request)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
