"""One agent = one Claude conversation with a system prompt built from the Part A files.

Claude Code assembled each agent from CLAUDE.md, the agent's file in
.claude/agents/, the skills named in its frontmatter and its MEMORY.md. This
module does the same and runs the tool-use loop against the Claude API.
"""
from __future__ import annotations

import json
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import anthropic

from . import config
from .tools import Toolbox, ToolError

Logger = Callable[[str, str, str], None]  # (agent, kind, text)


class Cancelled(Exception):
    pass


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cache_write: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add(self, u) -> None:
        with self.lock:
            self.input_tokens += getattr(u, "input_tokens", 0) or 0
            self.output_tokens += getattr(u, "output_tokens", 0) or 0
            self.cache_read += getattr(u, "cache_read_input_tokens", 0) or 0
            self.cache_write += getattr(u, "cache_creation_input_tokens", 0) or 0

    def as_dict(self) -> dict:
        return {"input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "cache_read": self.cache_read, "cache_write": self.cache_write}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta: dict = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def _split_list(v: str | None) -> list[str]:
    return [x.strip() for x in (v or "").split(",") if x.strip()]


HARNESS_PREAMBLE = """\
# Runtime

You are running inside the Procurement Audit Planner harness: a web application
that runs the same agents and skills the team built in Claude Code, but outside
Claude Code, against the Claude API. Differences that matter:

- Your working directory is the project root. Paths like `outputs/rules.json`
  are relative to it. `.venv/bin/python` is the project's Python (pandas,
  openpyxl, pypdf installed); `pdftotext` and `jq` are on PATH.
- Your tools: {tools}. They behave like Claude Code's tools of the same name.
- No human can answer you mid-run. Where your instructions say to ask the
  user or the lead, or to stop and report, end your turn with the report
  instead. The human auditor acts only at the gates the harness shows them.
- Agent memory files are read-only context here: the container is reset
  between deployments, so do not spend turns saving memory.
- Finish each turn with the report your instructions ask for; it is shown to
  the auditor.
"""


class Agent:
    def __init__(self, name: str, workspace: Path, client: anthropic.Anthropic, log: Logger,
                 usage: Usage, cancel: threading.Event,
                 send_message: Callable[[str, str], str] | None = None,
                 skill: str | None = None, role: str | None = None):
        """name: an agent file in .claude/agents/. skill: run a human-invoked skill in the
        main session instead (e.g. /extract-rules). role: main-session text (the lead)."""
        self.name = name
        self.ws = workspace
        self.client = client
        self.log = log
        self.usage = usage
        self.cancel = cancel
        self.messages: list[dict] = []
        claude_md = (workspace / "CLAUDE.md").read_text(encoding="utf-8")

        if skill or role:
            tools = ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
            memory = ""
            if skill:
                skill_text = (workspace / ".claude" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                _, body = parse_frontmatter(skill_text)
                role = (f"You are the main session. The auditor has invoked the `/{skill}` skill. "
                        f"Follow it exactly.\n\n# Skill: {skill}\n\n{body}")
            else:
                tools = ["Bash", "Read", "Glob", "Grep"]
        else:
            meta, body = parse_frontmatter(
                (workspace / ".claude" / "agents" / f"{name}.md").read_text(encoding="utf-8"))
            tools = _split_list(meta.get("tools")) or ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
            role = body
            for skill in _split_list(meta.get("skills")):
                sp = workspace / ".claude" / "skills" / skill / "SKILL.md"
                if sp.exists():
                    _, sbody = parse_frontmatter(sp.read_text(encoding="utf-8"))
                    role += f"\n\n# Preloaded skill: {skill} (`.claude/skills/{skill}/SKILL.md`)\n\n{sbody}"
            mp = workspace / ".claude" / "agent-memory" / name / "MEMORY.md"
            memory = (f"\n\n# Your agent memory (`.claude/agent-memory/{name}/MEMORY.md`)\n\n"
                      f"{mp.read_text(encoding='utf-8')}") if mp.exists() else ""

        self.toolbox = Toolbox(workspace, tools, send_message)
        self.system = [{
            "type": "text",
            "text": (HARNESS_PREAMBLE.format(tools=", ".join(self.toolbox.allowed))
                     + "\n\n# Project instructions (CLAUDE.md)\n\n" + claude_md
                     + "\n\n# Your role\n\n" + role + memory),
        }]

    # ------------------------------------------------------------------
    def _call(self):
        kwargs = dict(
            model=config.model(),
            max_tokens=64000,
            system=self.system,
            tools=self.toolbox.definitions(),
            messages=self.messages,
            thinking={"type": "adaptive", "display": "summarized"},
            output_config={"effort": config.effort()},
            cache_control={"type": "ephemeral"},
        )
        if config.model().startswith(("claude-opus-5", "claude-fable-5", "claude-sonnet-5-5")):
            # Retry on Anthropic's recommended model if a safety classifier declines a benign request.
            kwargs["betas"] = ["server-side-fallback-2026-07-01"]
            kwargs["fallbacks"] = "default"
        with self.client.beta.messages.stream(**kwargs) as stream:
            return stream.get_final_message()

    @staticmethod
    def _echo(content: list) -> list:
        """Content to send back next turn. After a mid-output fallback, drop the
        declined model's thinking/tool_use blocks that precede the last fallback block."""
        idx = max((i for i, b in enumerate(content) if b.type == "fallback"), default=-1)
        if idx < 0:
            return list(content)
        keep = [b for b in content[:idx] if b.type == "text"]
        return keep + list(content[idx + 1:])

    def run(self, prompt: str) -> str:
        """Send one user message and loop until the agent ends its turn. Returns its final text."""
        self.messages.append({"role": "user", "content": prompt})
        final_text = ""
        for _ in range(config.MAX_TURNS):
            if self.cancel.is_set():
                raise Cancelled()
            resp = self._call()
            self.usage.add(resp.usage)
            for b in resp.content:
                if b.type == "thinking" and getattr(b, "thinking", ""):
                    self.log(self.name, "thinking", b.thinking)
                elif b.type == "text" and b.text.strip():
                    self.log(self.name, "text", b.text)
                    final_text = b.text
            if resp.stop_reason == "refusal":
                self.log(self.name, "error", "The model declined this request (refusal).")
                self.messages.append({"role": "assistant", "content": self._echo(resp.content) or
                                      [{"type": "text", "text": "(declined)"}]})
                return final_text or "(the model declined)"
            if resp.stop_reason == "max_tokens":
                kept = [b for b in self._echo(resp.content) if b.type != "tool_use"]
                self.messages.append({"role": "assistant", "content": kept or [{"type": "text", "text": "…"}]})
                self.messages.append({"role": "user", "content": "Your last response was cut off at the "
                                      "output limit. Continue, in smaller steps."})
                continue
            self.messages.append({"role": "assistant", "content": self._echo(resp.content)})
            calls = [b for b in resp.content if b.type == "tool_use"]
            if resp.stop_reason != "tool_use" or not calls:
                return final_text
            results = []
            for c in calls:
                args = c.input if isinstance(c.input, dict) else json.loads(c.input or "{}")
                self.log(self.name, "tool", f"{c.name} {json.dumps(args, ensure_ascii=False)[:600]}")
                try:
                    out = self.toolbox.run(c.name, args)
                    results.append({"type": "tool_result", "tool_use_id": c.id, "content": out})
                    self.log(self.name, "result", out[:1500])
                except (ToolError, TypeError, OSError, ValueError) as e:
                    results.append({"type": "tool_result", "tool_use_id": c.id,
                                    "content": f"Error: {e}", "is_error": True})
                    self.log(self.name, "result", f"Error: {e}")
            self.messages.append({"role": "user", "content": results})
        self.log(self.name, "error", f"Stopped after {config.MAX_TURNS} model turns.")
        self.messages.append({"role": "user", "content": "Turn limit reached. Stop and give your report now, "
                              "with no more tool calls."})
        resp = self._call()
        self.usage.add(resp.usage)
        self.messages.append({"role": "assistant", "content": self._echo(resp.content)})
        return "\n".join(b.text for b in resp.content if b.type == "text") or final_text
