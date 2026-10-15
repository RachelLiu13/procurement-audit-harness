"""The end-to-end workflow, with the two human gates between background stages.

    stage 1  /extract-rules skill            -> rules.json (+ verify_quotes.py)
    stage 2  spend-analyst ∥ findings-analyst -> analytics.json, history.json
    stage 3  risk-assessor                    -> risk-register.md, auditor-comments.md
    GATE 1   auditor decides each risk in the web UI
    stage 4  risk-assessor revision, then build_pack.py --gate
    stage 5  agent team: planner, challenger, qa-reviewer -> the planning pack, review.md
    stage 6  lead report
    GATE 2   auditor signs off review.md in the web UI

Each run lives in its own copy of the Part A project under RUNS_DIR/<id>, with
its state in run.json and a log in events.jsonl, so the browser can disconnect
and reconnect (?run=<id>) while the agents keep working.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
import sys
import threading
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

from . import config, gate
from .agent import Agent, Cancelled, Usage
from .team import Team

PHASE1_FILES = ["rules.json", "analytics.json", "history.json", "analytics-full", "committee-text"]

STATUS_TEXT = {
    "running": "Agents are working",
    "awaiting_decisions": "Waiting for the auditor's decisions on the risk register",
    "awaiting_signoff": "Waiting for the auditor's sign-off",
    "complete": "Signed off",
    "blocked": "QA verdict BLOCKED: the pack went back to the team",
    "failed": "Stopped with an error",
    "cancelled": "Cancelled",
}

LEAD_ROLE = """\
You are the lead (the main session) of the Phase 3 agent team. The team has
finished. Write the lead's report to the auditor exactly as CLAUDE.md
("How the lead runs the team", step 5) asks, in under 300 words: risks in
scope, the three documents and the sample count, the challenges marked *for
the auditor*, the QA verdict, and the request to complete the sign-off block
at the end of `outputs/review.md`. Read outputs/review.md,
outputs/challenges.md and the header of outputs/planning-memo.md to do so.
Copy figures from those files; compute nothing. If review.md is missing or
the verdict is BLOCKED, say the pack is not ready for sign-off and why.
"""

_active_lock = threading.Lock()
_active: dict[str, "Run"] = {}


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


class Run:
    def __init__(self, run_id: str):
        self.id = run_id
        self.dir = config.RUNS_DIR / run_id
        self.outputs = self.dir / "outputs"
        self.state_path = self.dir / "run.json"
        self.events_path = self.dir / "events.jsonl"
        self.cancel = threading.Event()
        self._log_lock = threading.Lock()
        self.usage = Usage()

    # ---------------------------------------------------------------- state
    @classmethod
    def create(cls, reuse_phase1: bool) -> "Run":
        run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]
        run = cls(run_id)
        shutil.copytree(config.PROJECT_TEMPLATE, run.dir)
        run.outputs.mkdir(exist_ok=True)
        # The agent files call `.venv/bin/python`; point it at this interpreter.
        venv_bin = run.dir / ".venv" / "bin"
        venv_bin.mkdir(parents=True, exist_ok=True)
        for name in ("python", "python3"):
            p = venv_bin / name
            p.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n')
            p.chmod(0o755)
        if reuse_phase1:
            for name in PHASE1_FILES:
                src = config.EXAMPLE_RUN / name
                if src.is_dir():
                    shutil.copytree(src, run.outputs / name)
                elif src.exists():
                    shutil.copy2(src, run.outputs / name)
        run.save(status="created", stage="", created=_now(), reuse_phase1=reuse_phase1,
                 model=config.model(), effort=config.effort())
        return run

    @classmethod
    def load(cls, run_id: str) -> "Run | None":
        if not run_id or "/" in run_id or ".." in run_id:
            return None
        with _active_lock:
            if run_id in _active:
                return _active[run_id]
        run = cls(run_id)
        if not run.state_path.exists():
            return None
        if run.state().get("status") == "running":
            # No live thread owns it: the server restarted mid-stage.
            run.save(status="failed", error="Interrupted: the server restarted while agents were working.")
        return run

    @staticmethod
    def active_count() -> int:
        with _active_lock:
            return len(_active)

    @staticmethod
    def list_runs() -> list[dict]:
        if not config.RUNS_DIR.exists():
            return []
        out = []
        for d in sorted(config.RUNS_DIR.iterdir(), reverse=True):
            p = d / "run.json"
            if p.exists():
                try:
                    out.append({"id": d.name, **json.loads(p.read_text())})
                except json.JSONDecodeError:
                    pass
        return out

    def state(self) -> dict:
        try:
            return json.loads(self.state_path.read_text())
        except (OSError, json.JSONDecodeError):
            return {}

    def save(self, **updates) -> None:
        s = self.state()
        s.update(updates)
        s["updated"] = _now()
        s["usage"] = self.usage.as_dict() if self.usage.input_tokens else s.get("usage", {})
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(s, indent=1))
        tmp.replace(self.state_path)

    def log(self, agent: str, kind: str, text: str) -> None:
        with self._log_lock:
            with self.events_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"t": _now(), "agent": agent, "kind": kind, "text": text},
                                   ensure_ascii=False) + "\n")

    def events(self, limit: int | None = None) -> list[dict]:
        if not self.events_path.exists():
            return []
        lines = self.events_path.read_text(encoding="utf-8").splitlines()
        if limit:
            lines = lines[-limit:]
        return [json.loads(x) for x in lines if x.strip()]

    def is_busy(self) -> bool:
        return self.state().get("status") == "running"

    # --------------------------------------------------------------- helpers
    def _client(self) -> anthropic.Anthropic:
        key = config.api_key()
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured on the server.")
        return anthropic.Anthropic(api_key=key, max_retries=5, timeout=900)

    def _agent(self, client, name: str, **kw) -> Agent:
        return Agent(name, self.dir, client, self.log, self.usage, self.cancel, **kw)

    def _script(self, label: str, *args: str) -> tuple[int, str]:
        r = subprocess.run([sys.executable, *args], cwd=self.dir, capture_output=True, text=True, timeout=900)
        out = (r.stdout + ("\n" + r.stderr if r.stderr else "")).strip()
        self.log("harness", "script", f"$ python {' '.join(args)}\n{out}\n[exit {r.returncode}]")
        return r.returncode, out

    def _stage(self, stage: str) -> None:
        self.log("harness", "stage", stage)
        self.save(stage=stage)

    def _background(self, fn) -> None:
        if self.is_busy():
            raise RuntimeError("This run is already working.")
        if Run.active_count() >= config.MAX_ACTIVE_RUNS:
            raise RuntimeError("Another run is already working on this server. Try again when it reaches a gate.")
        self.cancel.clear()
        self.save(status="running", error=None)
        with _active_lock:
            _active[self.id] = self

        def wrapper():
            try:
                fn(self._client())
            except Cancelled:
                self.log("harness", "error", "Cancelled by the user.")
                self.save(status="cancelled")
            except Exception as e:  # report every failure in the UI
                self.log("harness", "error", f"{type(e).__name__}: {e}\n{traceback.format_exc()[-2000:]}")
                self.save(status="failed", error=f"{type(e).__name__}: {e}")
            finally:
                self.save()
                with _active_lock:
                    _active.pop(self.id, None)

        threading.Thread(target=wrapper, name=f"run-{self.id}", daemon=True).start()

    # ---------------------------------------------------------------- stages
    def start(self) -> None:
        self._background(self._phase_1_to_3)

    def _phase_1_to_3(self, client) -> None:
        if not self.state().get("reuse_phase1"):
            self._stage("1 · extract-rules skill → rules.json")
            report = self._agent(client, "extract-rules", skill="extract-rules").run(
                "/extract-rules\n\nExtract the rules from data/contract-rules.pdf into outputs/rules.json, "
                "verify every quote, and report.")
            self.log("extract-rules", "report", report)
            if not (self.outputs / "rules.json").exists():
                raise RuntimeError("extract-rules did not write outputs/rules.json")
            self._script("verify quotes", ".claude/skills/extract-rules/verify_quotes.py",
                         "outputs/rules.json", "data/contract-rules.pdf")

            self._stage("2 · spend-analyst ∥ findings-analyst → analytics.json, history.json")
            prompts = {
                "spend-analyst": "Run your full analysis: clean the spend and contracts data, run every test "
                                 "parameterised from outputs/rules.json, write outputs/analytics.json and "
                                 "outputs/analytics-full/, run the self-check, and report.",
                "findings-analyst": "Record the audit history and the council's risk scoring method from "
                                    "data/committee/*.pdf into outputs/history.json, run "
                                    "scripts/verify_history.py until it passes, and report.",
            }
            with ThreadPoolExecutor(max_workers=2) as pool:
                futs = {n: pool.submit(self._agent(client, n).run, p) for n, p in prompts.items()}
                for n, f in futs.items():
                    self.log(n, "report", f.result())
            for name in ("analytics.json", "history.json"):
                if not (self.outputs / name).exists():
                    raise RuntimeError(f"Phase 2 did not produce outputs/{name}")
        else:
            self.log("harness", "stage", "1–2 · reusing Part A's rules.json, analytics.json and history.json")

        self._stage("3 · risk-assessor → risk-register.md")
        report = self._agent(client, "risk-assessor").run(
            "Build the procurement risk register (first build, no auditor decisions yet). Follow your "
            "process and report.")
        self.log("risk-assessor", "report", report)
        if not (self.outputs / "auditor-comments.md").exists():
            raise RuntimeError("risk-assessor did not produce outputs/auditor-comments.md")
        self.save(status="awaiting_decisions", stage="Gate 1 · auditor decisions", assessor_report=report)

    def submit_decisions(self, decisions: dict[str, tuple[str, str]], other: str) -> None:
        gate.write_decisions(self.outputs, decisions, other)
        self.log("auditor", "decision", "\n".join(f"{k}: {d}" + (f" — {c}" if c else "")
                                                  for k, (d, c) in decisions.items())
                 + (f"\nOther instructions: {other}" if other.strip() else ""))
        self._background(self._phase_4_to_6)

    def _phase_4_to_6(self, client) -> None:
        self._stage("4 · risk-assessor revision → register re-issued with the decisions")
        report = self._agent(client, "risk-assessor").run(
            "The auditor has recorded decisions in outputs/auditor-comments.md. Issue the next revision of "
            "the register, applying exactly those decisions, following the skill's Revisions section. Report.")
        self.log("risk-assessor", "report", report)

        code, out = self._script("gate", ".claude/skills/audit-program/build_pack.py", "--gate")
        if code != 0:
            self.save(status="awaiting_decisions", stage="Gate 1 · auditor decisions",
                      gate_output=out, assessor_report=report)
            self.log("lead", "status", "Gate closed: the auditor must complete or change the decisions.")
            return
        self.save(gate_output=out)

        self._stage("5 · agent team: planner, challenger, qa-reviewer")
        team = Team(self.dir, client, self.log, self.usage, self.cancel)
        team.run(out)

        self._stage("6 · lead report")
        lead = self._agent(client, "lead", role=LEAD_ROLE)
        report = lead.run("Write the lead's report to the auditor now.")
        self.log("lead", "report", report)
        self._script("final checks", "scripts/checks/run_checks.py")
        review = self.outputs / "review.md"
        verdict = ""
        if review.exists():
            text = review.read_text(encoding="utf-8")
            verdict = "READY FOR SIGN-OFF" if "Verdict: READY FOR SIGN-OFF" in text else (
                "BLOCKED" if "Verdict: BLOCKED" in text else "")
        status = "awaiting_signoff" if verdict == "READY FOR SIGN-OFF" else "blocked"
        self.save(status=status, stage="Gate 2 · auditor sign-off" if status == "awaiting_signoff"
                  else "Pack blocked", lead_report=report, verdict=verdict or "no review.md")

    def sign_off(self, decision: str, name: str, role: str, comments: str) -> None:
        gate.sign_off(self.outputs, decision, name, role, dt.date.today().isoformat(), comments)
        self.log("auditor", "decision", f"Sign-off: {decision} by {name}")
        self.save(status="complete" if decision == "Sign off" else "blocked",
                  stage="Signed off" if decision == "Sign off" else "Returned to the team")

    def zip_outputs(self) -> bytes:
        import io
        import zipfile
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for p in sorted(self.outputs.rglob("*")):
                if p.is_file():
                    z.write(p, p.relative_to(self.dir))
        return buf.getvalue()
