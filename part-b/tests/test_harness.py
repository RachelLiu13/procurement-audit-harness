"""Offline tests: the agent loop, tools and team messaging with a scripted fake Claude client.

Run: python -m pytest tests/  (or python tests/test_harness.py)
"""
from __future__ import annotations

import os
import sys
import tempfile
import threading
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("RUNS_DIR", tempfile.mkdtemp())

from harness import gate  # noqa: E402
from harness.agent import Agent, Usage  # noqa: E402
from harness.pipeline import Run  # noqa: E402
from harness.team import Team  # noqa: E402


def text(t):
    return NS(type="text", text=t)


def tool(i, name, **inp):
    return NS(type="tool_use", id=i, name=name, input=inp)


def resp(*blocks, stop="end_turn"):
    return NS(content=list(blocks), stop_reason=stop,
              usage=NS(input_tokens=10, output_tokens=5, cache_read_input_tokens=0, cache_creation_input_tokens=0))


class FakeClient:
    """Answers each request by the agent named in its system prompt, from a script per agent."""

    def __init__(self, scripts: dict[str, list]):
        self.scripts = {k: list(v) for k, v in scripts.items()}
        self.requests: list[dict] = []
        self.beta = NS(messages=NS(stream=self._stream))

    def _stream(self, **kw):
        self.requests.append({**kw, "messages": list(kw["messages"])})  # snapshot: the agent mutates its list
        system = kw["system"][0]["text"]
        who = next(n for n in self.scripts if f"You are the {n}" in system or f"`/{n}`" in system)
        r = self.scripts[who].pop(0)

        class S:
            def __enter__(s):
                return s

            def __exit__(s, *a):
                return False

            def get_final_message(s):
                return r
        return S()


def new_run() -> Run:
    return Run.create(reuse_phase1=True)


def test_agent_loop_runs_tools_and_returns_report():
    run = new_run()
    client = FakeClient({"risk assessor": [
        resp(tool("t1", "Bash", command="ls outputs"), tool("t2", "Write", file_path="outputs/x.txt",
                                                            content="hi"), stop="tool_use"),
        resp(tool("t3", "Read", file_path="outputs/x.txt"), stop="tool_use"),
        resp(text("REPORT done")),
    ]})
    events = []
    a = Agent("risk-assessor", run.dir, client, lambda *e: events.append(e), Usage(), threading.Event())
    assert a.run("go") == "REPORT done"
    assert (run.outputs / "x.txt").read_text() == "hi"
    # all tool results of one turn go back in a single user message
    results = client.requests[1]["messages"][-1]["content"]
    assert [r["tool_use_id"] for r in results] == ["t1", "t2"]
    assert "rules.json" in results[0]["content"]
    assert "hi" in client.requests[2]["messages"][-1]["content"][0]["content"]
    # risk-assessor preloads its skill and memory; tools follow its frontmatter
    sys_text = client.requests[0]["system"][0]["text"]
    assert "Preloaded skill: risk-assessment" in sys_text and "agent memory" in sys_text
    assert {t["name"] for t in client.requests[0]["tools"]} == {"Bash", "Read", "Write", "Edit", "Glob", "Grep"}


def test_tool_errors_are_returned_not_raised():
    run = new_run()
    client = FakeClient({"risk assessor": [
        resp(tool("t1", "Read", file_path="../../etc/passwd"), tool("t2", "SendMessage", to="planner",
                                                                     message="x"), stop="tool_use"),
        resp(text("ok")),
    ]})
    a = Agent("risk-assessor", run.dir, client, lambda *e: None, Usage(), threading.Event())
    a.run("go")
    res = client.requests[1]["messages"][-1]["content"]
    assert all(r.get("is_error") for r in res)


def test_team_messages_flow_and_stop_when_all_done():
    run = new_run()
    client = FakeClient({
        "planner": [
            resp(tool("p1", "SendMessage", to="challenger", message="PACK READY v1"),
                 tool("p2", "SendMessage", to="qa-reviewer", message="PACK READY v1"), stop="tool_use"),
            resp(text("announced")),
            # woken by the challenge and the QA pass together
            resp(tool("p3", "SendMessage", to="lead", message="PLANNER DONE v1"), stop="tool_use"),
            resp(text("done")),
        ],
        # the planner announced before their first turn, so the kickoff carries PACK READY v1
        "challenger": [
            resp(tool("c1", "SendMessage", to="planner", message="CHALLENGE #1 [x] R-01"),
                 tool("c2", "SendMessage", to="lead", message="CHALLENGER DONE"), stop="tool_use"),
            resp(text("sent")),
        ],
        "QA reviewer": [
            resp(tool("q1", "SendMessage", to="planner", message="QA v1: PASS"),
                 tool("q2", "SendMessage", to="lead", message="QA DONE v1: READY FOR SIGN-OFF"), stop="tool_use"),
            resp(text("sent")),
        ],
    })
    team = Team(run.dir, client, run.log, Usage(), threading.Event())
    team.run("GATE OPEN")
    assert team.done == {"PLANNER DONE", "CHALLENGER DONE", "QA DONE"}
    assert all(not v for v in client.scripts.values())  # every scripted turn was used
    planner_wake = [r for r in client.requests if "You are the planner" in r["system"][0]["text"]][2]
    inbox = planner_wake["messages"][-1]["content"]
    assert "CHALLENGE #1" in inbox and "QA v1: PASS" in inbox


def test_done_sent_only_to_planner_and_lead_still_reaches_qa():
    """The first live run stalled: the challenger sent CHALLENGER DONE to the planner and the lead
    only (as its protocol says), and the qa-reviewer waited for it forever."""
    run = new_run()
    client = FakeClient({
        "planner": [
            resp(tool("p1", "SendMessage", to="challenger", message="PACK READY v1"),
                 tool("p2", "SendMessage", to="qa-reviewer", message="PACK READY v1"), stop="tool_use"),
            resp(text("announced")),
            resp(tool("p3", "SendMessage", to="lead", message="PLANNER DONE v1"),
                 tool("p4", "SendMessage", to="qa-reviewer", message="PLANNER DONE v1"), stop="tool_use"),
            resp(text("done")),
        ],
        "challenger": [
            resp(tool("c1", "SendMessage", to="planner", message="CHALLENGER DONE\nno challenges"),
                 tool("c2", "SendMessage", to="lead", message="CHALLENGER DONE\nno challenges"), stop="tool_use"),
            resp(text("sent")),
            resp(text("noted PLANNER DONE")),  # woken by the broadcast of PLANNER DONE
        ],
        "QA reviewer": [
            resp(tool("q1", "SendMessage", to="planner", message="QA v1: PASS"), stop="tool_use"),
            resp(text("waiting for both done messages")),
            # must be woken with CHALLENGER DONE as well as PLANNER DONE
            resp(tool("q2", "SendMessage", to="lead", message="QA DONE v1: READY FOR SIGN-OFF"), stop="tool_use"),
            resp(text("review written")),
        ],
    })
    team = Team(run.dir, client, run.log, Usage(), threading.Event())
    team.run("GATE OPEN")
    assert team.done == {"PLANNER DONE", "CHALLENGER DONE", "QA DONE"}
    qa_inboxes = " ".join(m["content"] for r in client.requests if "You are the QA reviewer" in r["system"][0]["text"]
                          for m in r["messages"] if m["role"] == "user" and isinstance(m["content"], str))
    assert "CHALLENGER DONE" in qa_inboxes and "PLANNER DONE" in qa_inboxes


def test_quiet_team_gets_one_lead_nudge_then_stops():
    run = new_run()
    client = FakeClient({
        "planner": [resp(text("built, forgot to announce")), resp(text("still nothing"))],
        "challenger": [resp(text("waiting")), resp(text("waiting"))],
        "QA reviewer": [resp(text("waiting")), resp(text("waiting"))],
    })
    team = Team(run.dir, client, run.log, Usage(), threading.Event())
    team.run("GATE OPEN")  # must terminate: one nudge round, then stop
    assert all(not v for v in client.scripts.values())
    assert team.done == set()


def test_sign_off_writes_final_lead_report_and_keeps_the_first():
    import time
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-not-used")
    run = new_run()
    (run.outputs / "review.md").write_text(
        "# QA review\n\n## Verdict: READY FOR SIGN-OFF\n\n## Auditor sign-off\n\n"
        "- [ ] I have read planning-memo.md\n- [ ] I accept the challenges\n"
        "- Decision: Sign off / Return to the team\n- Name:\n- Role:\n- Date:\n- Comments:\n")
    run.save(status="awaiting_signoff", lead_report="Ready for your sign-off.")
    client = FakeClient({"lead (the main session)": [
        resp(tool("r1", "Read", file_path="outputs/review.md"), stop="tool_use"),
        resp(text("Signed off by Team 9 on 2026-10-15.")),
    ]})
    run._client = lambda: client
    run.sign_off("Sign off", "Team 9", "Internal auditor", "ok")
    for _ in range(100):
        if run.state().get("final_report_status") != "writing":
            break
        time.sleep(0.05)
    s = run.state()
    assert s["status"] == "complete" and s["final_report_status"] == "done"
    assert s["final_report"] == "Signed off by Team 9 on 2026-10-15."
    assert s["lead_report"] == "Ready for your sign-off."  # the first report stays as it was
    assert "Ready for your sign-off." in (run.outputs / "lead-report-before-sign-off.md").read_text()
    assert "Team 9" in (run.outputs / "lead-report-after-sign-off.md").read_text()


def test_failed_final_checks_block_sign_off_whatever_review_md_says():
    ready = "## Verdict: READY FOR SIGN-OFF\n"
    assert gate.pack_verdict(0, ready) == ("awaiting_signoff", "READY FOR SIGN-OFF")
    status, verdict = gate.pack_verdict(1, ready)  # the agent wrote READY, the checks failed
    assert status == "blocked" and "final QA checks failed" in verdict and "said READY" in verdict
    assert gate.pack_verdict(0, "## Verdict: BLOCKED\n")[0] == "blocked"
    assert gate.pack_verdict(0, "no verdict here")[0] == "blocked"
    assert gate.pack_verdict(0, None) == ("blocked", "BLOCKED: no review.md")


SIGN_OFF_REVIEW = ("# QA review\n\n## Verdict: READY FOR SIGN-OFF\n\n## Auditor sign-off\n\n"
                   "- [ ] I have read planning-memo.md\n- [ ] I accept the challenges\n"
                   "- Decision: Sign off / Return to the team\n- Name:\n- Role:\n- Date:\n- Comments:\n")


def test_return_without_comments_is_refused_and_records_nothing():
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-not-used")
    run = new_run()
    (run.outputs / "review.md").write_text(SIGN_OFF_REVIEW)
    run.save(status="awaiting_signoff")
    try:
        run.sign_off("Return to the team", "Team 9", "Internal auditor", "  ")
        raise AssertionError("a return with no comments must be refused")
    except RuntimeError:
        pass
    assert (run.outputs / "review.md").read_text() == SIGN_OFF_REVIEW
    assert run.state()["status"] == "awaiting_signoff"


def test_return_to_team_reworks_the_pack_and_comes_back_to_sign_off():
    import time
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-not-used")
    run = new_run()
    (run.outputs / "review.md").write_text(SIGN_OFF_REVIEW)
    run.save(status="awaiting_signoff", lead_report="Ready for your sign-off.")
    new_review = "# QA review\n\n## Verdict: READY FOR SIGN-OFF\n\nv2\n"
    client = FakeClient({
        "planner": [
            resp(tool("p1", "SendMessage", to="challenger", message="PACK READY v2"),
                 tool("p2", "SendMessage", to="qa-reviewer", message="PACK READY v2"), stop="tool_use"),
            resp(text("announced")),
            resp(tool("p3", "SendMessage", to="lead", message="PLANNER DONE v2"), stop="tool_use"),
            resp(text("done")),
        ],
        "challenger": [
            resp(tool("c1", "SendMessage", to="lead", message="CHALLENGER DONE"), stop="tool_use"),
            resp(text("sent")),
        ],
        "QA reviewer": [
            resp(tool("q1", "SendMessage", to="planner", message="QA v2: PASS"),
                 tool("q2", "Write", file_path="outputs/review.md", content=new_review),
                 tool("q3", "SendMessage", to="lead", message="QA DONE v2: READY FOR SIGN-OFF"), stop="tool_use"),
            resp(text("review written")),
        ],
        "lead (the main session)": [resp(text("Revised pack v2 is ready for your sign-off."))],
    })
    run._client = lambda: client
    scripts = []

    def fake_script(label, *args):
        scripts.append(label)
        return (0, "GATE OPEN: register revision 1") if "--gate" in args else (0, "VERDICT: READY FOR SIGN-OFF")
    run._script = fake_script

    run.sign_off("Return to the team", "Team 9", "Internal auditor", "Add a CPR-38 step to T-03-1.")
    for _ in range(200):
        if run.state().get("status") != "running":
            break
        time.sleep(0.05)
    s = run.state()
    assert s["status"] == "awaiting_signoff" and s["rework_round"] == 1, s
    assert s["lead_report"] == "Revised pack v2 is ready for your sign-off."
    assert scripts == ["gate", "final checks"]
    archived = (run.outputs / "review-returned-1.md").read_text()
    assert "- Decision: Return to the team" in archived and "Add a CPR-38 step" in archived
    assert (run.outputs / "review.md").read_text() == new_review
    planner_kickoff = next(r for r in client.requests if "You are the planner" in r["system"][0]["text"])
    assert "Add a CPR-38 step to T-03-1." in planner_kickoff["messages"][0]["content"]


def test_gate_files_round_trip():
    run = new_run()
    (run.outputs / "auditor-comments.md").write_text(
        "# Auditor decisions\n\n| Risk ID | Risk | L | I | Score | Band | Proposed scope | Decision | Comment |\n"
        "|---|---|---|---|---|---|---|---|---|\n| R-01 | A | 2 | 3 | 6 | Moderate | in |  |  |\n"
        "| R-02 | B | 3 | 5 | 15 | Red | in |  |  |\n\n## Other instructions\n\n<!-- hint -->\n")
    gate.write_decisions(run.outputs, {"R-01": ("Approve", ""), "R-02": ("Amend", "likelihood 2 | lower")},
                         "add a risk on agency staff")
    _, rows, other = gate.read_decisions(run.outputs)
    assert rows[0]["Decision"] == "Approve" and rows[1]["Comment"] == "likelihood 2 / lower"
    assert other == "add a risk on agency staff"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
