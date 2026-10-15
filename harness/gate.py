"""The two human gates: auditor decisions on the register, and sign-off of the pack.

In Part A the auditor edited outputs/auditor-comments.md and the sign-off block
of outputs/review.md by hand. The web UI fills in the same files, in the same
format, so the builders and checks read them unchanged.
"""
from __future__ import annotations

import re
from pathlib import Path

DECISIONS = ["Approve", "Amend", "Reject"]


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_decisions(outputs: Path) -> tuple[list[str], list[dict], str]:
    """Return (header, rows, other_instructions) from auditor-comments.md."""
    text = (outputs / "auditor-comments.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    header: list[str] = []
    rows: list[dict] = []
    for i, line in enumerate(lines):
        if line.startswith("| Risk ID"):
            header = _cells(line)
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append(dict(zip(header, _cells(row))))
            break
    other = ""
    m = re.search(r"## Other instructions\n(.*)$", text, re.S)
    if m:
        other = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()
    return header, rows, other


def write_decisions(outputs: Path, decisions: dict[str, tuple[str, str]], other: str) -> None:
    """decisions: risk_id -> (decision, comment). Only the Decision and Comment cells change."""
    path = outputs / "auditor-comments.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    header: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("| Risk ID"):
            header = _cells(line)
            continue
        if header and line.startswith("|") and not line.startswith("|---"):
            cells = _cells(line)
            row = dict(zip(header, cells))
            rid = row.get("Risk ID")
            if rid in decisions:
                d, c = decisions[rid]
                row["Decision"] = d
                row["Comment"] = c.replace("|", "/").replace("\n", " ").strip()
                lines[i] = "| " + " | ".join(row.get(h, "") for h in header) + " |"
        elif header and not line.startswith("|"):
            header = []
    text = "\n".join(lines) + "\n"
    if other.strip():
        marker = "## Other instructions"
        head, _, tail = text.partition(marker)
        comment = re.search(r"<!--.*?-->", tail, re.S)
        text = head + marker + "\n\n" + (comment.group(0) + "\n" if comment else "") + other.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def sign_off(outputs: Path, decision: str, name: str, role: str, date: str, comments: str) -> None:
    path = outputs / "review.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("- [ ] I have read", "- [x] I have read").replace("- [ ] I accept", "- [x] I accept")
    for field, value in (("Decision", decision), ("Name", name), ("Role", role),
                         ("Date", date), ("Comments", comments)):
        text = re.sub(rf"^- {field}:.*$", f"- {field}: {value}".rstrip(), text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8")
