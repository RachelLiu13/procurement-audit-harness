"""The tools the agents use, re-implemented outside Claude Code.

Names and arguments follow Claude Code's built-in tools (Bash, Read, Write,
Edit, Glob, Grep, SendMessage), so the Part A agent files work unchanged.
Every path is resolved inside the run's workspace.
"""
from __future__ import annotations

import fnmatch
import os
import re
import subprocess
from pathlib import Path
from typing import Callable

from . import config


def _schema(props: dict, required: list[str]) -> dict:
    return {"type": "object", "properties": props, "required": required, "additionalProperties": False}


TOOL_SCHEMAS: dict[str, dict] = {
    "Bash": {
        "description": "Run a shell command (bash) in the project's root directory and return stdout+stderr. "
                       "Use for running the Python scripts and builders (.venv/bin/python ...), pdftotext, jq, ls.",
        "input_schema": _schema({
            "command": {"type": "string", "description": "The command to run."},
            "timeout": {"type": "integer", "description": "Seconds, max 600 (default 300)."},
        }, ["command"]),
    },
    "Read": {
        "description": "Read a text file. Returns lines numbered like `cat -n`. Use offset/limit for large files.",
        "input_schema": _schema({
            "file_path": {"type": "string", "description": "Path relative to the project root, or absolute inside it."},
            "offset": {"type": "integer", "description": "1-based line to start from."},
            "limit": {"type": "integer", "description": "Number of lines (default 2000)."},
        }, ["file_path"]),
    },
    "Write": {
        "description": "Create or overwrite a text file with the given content.",
        "input_schema": _schema({
            "file_path": {"type": "string"},
            "content": {"type": "string"},
        }, ["file_path", "content"]),
    },
    "Edit": {
        "description": "Replace an exact string in a file. old_string must be unique unless replace_all is true.",
        "input_schema": _schema({
            "file_path": {"type": "string"},
            "old_string": {"type": "string"},
            "new_string": {"type": "string"},
            "replace_all": {"type": "boolean"},
        }, ["file_path", "old_string", "new_string"]),
    },
    "Glob": {
        "description": "List files matching a glob pattern such as `outputs/**/*.json`.",
        "input_schema": _schema({
            "pattern": {"type": "string"},
            "path": {"type": "string", "description": "Directory to search from (default project root)."},
        }, ["pattern"]),
    },
    "Grep": {
        "description": "Search file contents with a regular expression. Returns file:line:text matches.",
        "input_schema": _schema({
            "pattern": {"type": "string"},
            "path": {"type": "string", "description": "File or directory (default project root)."},
            "glob": {"type": "string", "description": "Only search files whose name matches this glob, e.g. *.md"},
            "case_insensitive": {"type": "boolean"},
        }, ["pattern"]),
    },
    "SendMessage": {
        "description": "Send a message to a teammate (planner, challenger, qa-reviewer) or to the lead. "
                       "The first line carries the protocol keyword (e.g. PACK READY v1).",
        "input_schema": _schema({
            "to": {"type": "string", "enum": ["planner", "challenger", "qa-reviewer", "lead"]},
            "message": {"type": "string"},
        }, ["to", "message"]),
    },
}


class ToolError(Exception):
    pass


def _clip(text: str) -> str:
    lim = config.TOOL_OUTPUT_LIMIT
    if len(text) <= lim:
        return text
    return text[: lim // 2] + f"\n\n... [{len(text) - lim} characters cut] ...\n\n" + text[-lim // 2:]


class Toolbox:
    """Executes tool calls for one agent inside one workspace."""

    def __init__(self, workspace: Path, allowed: list[str],
                 send_message: Callable[[str, str], str] | None = None):
        self.ws = workspace.resolve()
        self.allowed = [t for t in allowed if t in TOOL_SCHEMAS and (t != "SendMessage" or send_message)]
        self.send_message = send_message

    def definitions(self) -> list[dict]:
        return [{"name": n, **TOOL_SCHEMAS[n]} for n in self.allowed]

    # -- paths -----------------------------------------------------------
    def _path(self, p: str) -> Path:
        p = p.strip()
        path = Path(p) if os.path.isabs(p) else self.ws / p
        path = path.resolve()
        if not (path == self.ws or self.ws in path.parents or str(path).startswith("/tmp")):
            raise ToolError(f"{p} is outside the project directory {self.ws}")
        return path

    # -- dispatch --------------------------------------------------------
    def run(self, name: str, args: dict) -> str:
        if name not in self.allowed:
            raise ToolError(f"tool {name} is not available to this agent")
        return getattr(self, "_" + name.lower())(**args)

    def _bash(self, command: str, timeout: int | None = None) -> str:
        timeout = max(1, min(int(timeout or 300), config.BASH_TIMEOUT))
        env = dict(os.environ)
        env["PATH"] = f"{self.ws / '.venv' / 'bin'}:{env.get('PATH', '')}"
        env.pop("ANTHROPIC_API_KEY", None)  # scripts never need the key
        try:
            r = subprocess.run(["bash", "-c", command], cwd=self.ws, capture_output=True,
                               text=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout}s"
        out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
        return _clip(f"{out.strip()}\n[exit code {r.returncode}]")

    def _read(self, file_path: str, offset: int | None = None, limit: int | None = None) -> str:
        path = self._path(file_path)
        if not path.is_file():
            raise ToolError(f"{file_path} does not exist")
        if path.suffix.lower() in {".pdf", ".xlsx", ".xls", ".png", ".jpg"}:
            raise ToolError(f"{file_path} is binary; use Bash (pdftotext, python) to inspect it")
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        start = max(1, int(offset or 1))
        n = int(limit or 2000)
        chunk = lines[start - 1: start - 1 + n]
        body = "\n".join(f"{i:6d}\t{line[:2000]}" for i, line in enumerate(chunk, start))
        more = f"\n[{len(lines)} lines in total]" if start - 1 + n < len(lines) else ""
        return _clip(body + more) if body else "(empty file)"

    def _write(self, file_path: str, content: str) -> str:
        path = self._path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Wrote {path.relative_to(self.ws) if self.ws in path.parents else path} ({len(content)} chars)"

    def _edit(self, file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> str:
        path = self._path(file_path)
        if not path.is_file():
            raise ToolError(f"{file_path} does not exist")
        text = path.read_text(encoding="utf-8")
        count = text.count(old_string)
        if count == 0:
            raise ToolError("old_string not found in file")
        if count > 1 and not replace_all:
            raise ToolError(f"old_string occurs {count} times; make it unique or set replace_all")
        text = text.replace(old_string, new_string) if replace_all else text.replace(old_string, new_string, 1)
        path.write_text(text, encoding="utf-8")
        return f"Edited {file_path} ({count if replace_all else 1} replacement(s))"

    def _glob(self, pattern: str, path: str | None = None) -> str:
        base = self._path(path) if path else self.ws
        hits = sorted(p for p in base.glob(pattern) if ".venv" not in p.parts)
        rel = [str(p.relative_to(self.ws)) if self.ws in p.parents else str(p) for p in hits[:500]]
        return "\n".join(rel) or "No files found"

    def _grep(self, pattern: str, path: str | None = None, glob: str | None = None,
              case_insensitive: bool = False) -> str:
        rx = re.compile(pattern, re.IGNORECASE if case_insensitive else 0)
        base = self._path(path) if path else self.ws
        files = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        out: list[str] = []
        for f in sorted(files):
            if ".venv" in f.parts or ".git" in f.parts or f.suffix.lower() in {".pdf", ".xlsx", ".png"}:
                continue
            if glob and not fnmatch.fnmatch(f.name, glob):
                continue
            try:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if rx.search(line):
                        out.append(f"{f.relative_to(self.ws) if self.ws in f.parents else f}:{i}:{line[:400]}")
                        if len(out) >= 300:
                            return "\n".join(out) + "\n[stopped at 300 matches]"
            except OSError:
                continue
        return "\n".join(out) or "No matches"

    def _sendmessage(self, to: str, message: str) -> str:
        assert self.send_message
        return self.send_message(to, message)
