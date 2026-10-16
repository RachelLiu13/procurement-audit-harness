"""The Phase 3 agent team, without Claude Code's experimental agent teams.

Each teammate is a long-lived Agent conversation. SendMessage puts a message in
the recipient's inbox; the scheduler gives a turn to whichever teammate has
mail, delivering its whole inbox as one user message. The lead (this harness)
does not relay between teammates: it only collects the DONE / BLOCKED /
QUESTION messages addressed to it, as the team lead did in Part A.
"""
from __future__ import annotations

import threading
from collections import deque
from pathlib import Path

import anthropic

from . import config
from .agent import Agent, Logger, Usage

TEAM = ["planner", "challenger", "qa-reviewer"]
DONE_TAGS = ("PLANNER DONE", "CHALLENGER DONE", "QA DONE")

KICKOFF = {
    "planner": ("The lead has run the approval gate and it is open (output below). Your teammates are "
                "`challenger` and `qa-reviewer`. Start now: follow your instructions, build the pack, "
                "announce PACK READY v1 to both, then handle messages as they arrive.\n\nGate output:\n{gate}"),
    "challenger": ("The gate is open. Your teammates are `planner` and `qa-reviewer`. The planner is building "
                   "the pack. Read the register, ratings, decisions and inputs now, then end your turn; you "
                   "will be woken when PACK READY v1 arrives. Send nothing before it."),
    "qa-reviewer": ("The gate is open. Your teammates are `planner` and `challenger`. Do nothing until "
                    "PACK READY v1 arrives; end your turn now. You will be woken when it does."),
}

LEAD_REPLY = ("Lead: I have no information beyond the inputs, the register and auditor-comments.md. "
              "Decide within your instructions; where they do not allow it, record the point "
              "\"for the auditor\" and carry on.")


class Team:
    def __init__(self, workspace: Path, client: anthropic.Anthropic, log: Logger, usage: Usage,
                 cancel: threading.Event):
        self.log = log
        self.inbox: dict[str, list[str]] = {n: [] for n in TEAM}
        self.lead_mail: list[tuple[str, str]] = []
        self.done: set[str] = set()
        # Which teammates have seen each done announcement. In Claude Code's agent teams every member
        # sees when a teammate finishes; here a done message is copied to anyone it was not sent to,
        # so a teammate waiting on it (the qa-reviewer waits for both PLANNER and CHALLENGER DONE)
        # is never left waiting for a message that went only to the lead.
        self.seen_done: dict[str, set[str]] = {n: set() for n in TEAM}
        self.nudged = False
        self.agents = {
            n: Agent(n, workspace, client, log, usage, cancel, send_message=self._sender(n)) for n in TEAM
        }

    @staticmethod
    def _done_tag(message: str) -> str | None:
        first = message.strip().splitlines()[0] if message.strip() else ""
        return next((t for t in DONE_TAGS if first.startswith(t)), None)

    def _broadcast_done(self, frm: str, tag: str, message: str) -> None:
        for name in TEAM:
            if name != frm and tag not in self.seen_done[name]:
                self.seen_done[name].add(tag)
                self.inbox[name].append(f"Message from {frm} (team broadcast of a done announcement):\n{message}")

    def _sender(self, frm: str):
        def send(to: str, message: str) -> str:
            self.log(frm, "message", f"→ {to}: {message}")
            tag = self._done_tag(message)
            if to == "lead":
                self.lead_mail.append((frm, message))
                if tag:
                    self.done.add(tag)
                    self._broadcast_done(frm, tag, message)
                first = message.strip().splitlines()[0] if message.strip() else ""
                if "QUESTION" in first:
                    self.inbox[frm].append(LEAD_REPLY)
                return "Delivered to the lead."
            if to not in self.inbox:
                return f"No teammate called {to}."
            if to == frm:
                return "You cannot message yourself."
            if tag:
                self.seen_done[to].add(tag)
            self.inbox[to].append(f"Message from {frm}:\n{message}")
            return f"Delivered to {to}."
        return send

    def _nudge(self) -> bool:
        """The team went quiet before everyone reported done. Tell each unfinished teammate, once,
        which done messages the lead holds, so a missed announcement cannot stall the team."""
        if self.nudged:
            return False
        self.nudged = True
        held = [msg.strip().splitlines()[0] for _, msg in self.lead_mail if self._done_tag(msg)]
        owners = {"PLANNER DONE": "planner", "CHALLENGER DONE": "challenger", "QA DONE": "qa-reviewer"}
        waiting = [owners[t] for t in DONE_TAGS if t not in self.done]
        for name in waiting:
            self.inbox[name].append(
                "Lead status: the team has gone quiet. Done messages the lead has received: "
                + (", ".join(held) or "none") + ". You have not reported done yet. Finish your protocol now.")
        return bool(waiting)

    def blocked(self) -> str | None:
        for frm, msg in self.lead_mail:
            if "BLOCKED" in msg.splitlines()[0] and not msg.startswith("QA DONE"):
                return f"{frm}: {msg}"
        return None

    def run(self, gate_output: str) -> None:
        queue = deque(TEAM)
        first = {n: KICKOFF[n].format(gate=gate_output) for n in TEAM}
        turns = 0
        while turns < config.MAX_TEAM_TURNS:
            if {"PLANNER DONE", "CHALLENGER DONE", "QA DONE"} <= self.done:
                self.log("lead", "status", "All three teammates reported done. Shutting the team down.")
                return
            if self.blocked() and turns > 0 and not any(self.inbox.values()):
                return
            # next teammate with work to do
            for _ in range(len(queue)):
                name = queue[0]
                queue.rotate(-1)
                if name in first or self.inbox[name]:
                    break
            else:
                if self._nudge():
                    self.log("lead", "status", "The team went quiet before everyone reported done; "
                                               "the lead sent a status update to the unfinished teammates.")
                    continue
                self.log("lead", "status", "No teammate has pending messages; the team has stopped.")
                return
            if name in first:
                prompt = first.pop(name)
                if self.inbox[name]:
                    prompt += "\n\n" + "\n\n---\n\n".join(self.inbox[name])
            else:
                prompt = "\n\n---\n\n".join(self.inbox[name])
            self.inbox[name] = []
            self.log("lead", "status", f"Turn {turns + 1}: {name}")
            self.agents[name].run(prompt)
            turns += 1
        self.log("lead", "error", f"Team stopped after {config.MAX_TEAM_TURNS} turns.")
