"""Settings for the harness, read from environment variables."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # part-b/
PROJECT_TEMPLATE = ROOT.parent / "part-a"     # the Part A project, beside part-b/: CLAUDE.md, .claude/, scripts/, data/
EXAMPLE_RUN = PROJECT_TEMPLATE / "outputs"     # Part A's completed, signed-off run, for browsing
SAVED_RUNS = ROOT / "saved-runs"               # Part B runs restored after a server restart
RUNS_DIR = Path(os.environ.get("RUNS_DIR", "/tmp/audit-planner-runs"))


def _secret(name: str, default: str | None = None) -> str | None:
    """Settings come from environment variables (on Fly.io: `fly secrets set` or [env] in fly.toml)."""
    return os.environ.get(name) or default


def api_key() -> str | None:
    return _secret("ANTHROPIC_API_KEY")


def model() -> str:
    return _secret("CLAUDE_MODEL", "claude-opus-5-5")


def effort() -> str:
    return _secret("CLAUDE_EFFORT", "medium")


def app_password() -> str | None:
    return _secret("APP_PASSWORD")


# Per-agent cap on model turns, so a stuck agent cannot loop (and spend) forever.
MAX_TURNS = int(_secret("MAX_TURNS", "60"))
# Cap on agent-team turns (one turn = one teammate handling its inbox).
MAX_TEAM_TURNS = int(_secret("MAX_TEAM_TURNS", "30"))
MAX_ACTIVE_RUNS = int(_secret("MAX_ACTIVE_RUNS", "1"))
BASH_TIMEOUT = 600
TOOL_OUTPUT_LIMIT = 30_000
