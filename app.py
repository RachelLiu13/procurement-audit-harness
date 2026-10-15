"""Procurement Audit Planner: the Part A agents and skills as a deployed web harness."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from harness import config, gate
from harness.pipeline import STATUS_TEXT, Run

st.set_page_config(page_title="Procurement Audit Planner", page_icon="📋", layout="wide")

STAGES = [
    ("1", "Extract rules", "skill · extract-rules", "rules.json"),
    ("2", "Analyse spend & history", "sub-agents · spend-analyst ∥ findings-analyst", "analytics.json · history.json"),
    ("3", "Rate risks", "sub-agent · risk-assessor + risk-assessment skill", "risk-register.md"),
    ("G1", "Auditor decisions", "human gate", "auditor-comments.md"),
    ("4", "Revise register", "sub-agent · risk-assessor", "register revision"),
    ("5", "Plan, challenge, QA", "agent team · planner · challenger · qa-reviewer", "planning pack · review.md"),
    ("G2", "Auditor sign-off", "human gate", "review.md signed"),
]

KEY_FILES = ["planning-memo.md", "risk-control-matrix.md", "audit-program.md", "challenges.md", "review.md",
             "risk-register.md", "auditor-comments.md", "rules.json", "analytics.json", "history.json"]


# ------------------------------------------------------------------ access
def require_password() -> None:
    pw = config.app_password()
    if not pw or st.session_state.get("authed"):
        return
    st.title("Procurement Audit Planner")
    entered = st.text_input("Access password", type="password")
    if entered and entered == pw:
        st.session_state.authed = True
        st.rerun()
    elif entered:
        st.error("Wrong password.")
    st.stop()


# ------------------------------------------------------------------ helpers
def stage_index(state: dict) -> int:
    stage = state.get("stage", "")
    status = state.get("status")
    if status == "complete":
        return len(STAGES)
    if status == "awaiting_signoff":
        return 6
    if status == "awaiting_decisions":
        return 3
    for i, (code, *_rest) in enumerate(STAGES):
        if stage.startswith(code + " ") or stage.startswith(code + "–"):
            return i
    if stage.startswith("1–2"):
        return 2
    return 0


def render_file(path: Path, key: str) -> None:
    if not path.exists():
        st.info(f"`{path.name}` has not been produced yet.")
        return
    suffix = path.suffix.lower()
    if suffix == ".md":
        st.markdown(path.read_text(encoding="utf-8"))
    elif suffix == ".json":
        try:
            st.json(json.loads(path.read_text(encoding="utf-8")), expanded=1)
        except json.JSONDecodeError:
            st.code(path.read_text(encoding="utf-8")[:20000])
    elif suffix == ".csv":
        st.dataframe(pd.read_csv(path), use_container_width=True)
    else:
        st.code(path.read_text(encoding="utf-8", errors="replace")[:20000])
    st.download_button("Download", path.read_bytes(), file_name=path.name, key=f"dl-{key}")


def outputs_browser(outputs: Path, prefix: str) -> None:
    if not outputs.exists():
        st.info("No outputs yet.")
        return
    files = [p for p in sorted(outputs.rglob("*")) if p.is_file() and p.suffix in {".md", ".json", ".csv", ".txt"}]
    if not files:
        st.info("No outputs yet.")
        return
    rel = [str(p.relative_to(outputs)) for p in files]
    ordered = [f for f in KEY_FILES if f in rel] + [f for f in rel if f not in KEY_FILES]
    choice = st.selectbox("File", ordered, key=f"{prefix}-file")
    render_file(outputs / choice, f"{prefix}-{choice}")


ICON = {"text": "💬", "tool": "🔧", "result": "↳", "message": "✉️", "report": "📄", "stage": "▶️",
        "status": "ℹ️", "error": "⚠️", "script": "🐍", "decision": "🧑‍⚖️", "thinking": "💭"}


def activity(run: Run, key: str) -> None:
    events = run.events()
    agents = sorted({e["agent"] for e in events})
    c1, c2 = st.columns([2, 1])
    pick = c1.multiselect("Agents", agents, key=f"{key}-agents")
    detail = c2.toggle("Show tool results and thinking", key=f"{key}-detail")
    shown = [e for e in events if (not pick or e["agent"] in pick)
             and (detail or e["kind"] not in {"result", "thinking"})]
    for e in reversed(shown[-300:]):
        head = f"{ICON.get(e['kind'], '•')} **{e['agent']}** · {e['kind']} · {e['t'][11:]}"
        text = e["text"]
        if e["kind"] in {"report", "stage", "error", "decision", "message"} or len(text) < 300:
            st.markdown(head)
            if e["kind"] in {"tool", "result", "script"}:
                st.code(text[:4000])
            else:
                st.markdown(text)
        else:
            with st.expander(head + " · " + text[:80].replace("\n", " ")):
                st.code(text[:8000]) if e["kind"] in {"tool", "result", "script"} else st.markdown(text)


def cost_line(state: dict) -> str:
    u = state.get("usage") or {}
    if not u:
        return ""
    return (f"Tokens so far: {u.get('input_tokens', 0):,} input · {u.get('cache_read', 0):,} cache read · "
            f"{u.get('output_tokens', 0):,} output · model `{state.get('model')}`")


# ------------------------------------------------------------------ gates
def decisions_form(run: Run, state: dict) -> None:
    st.subheader("Gate 1 · Your decisions on the risk register")
    if state.get("gate_output") and "GATE CLOSED" in state["gate_output"]:
        st.error("The approval gate is still closed:")
        st.code(state["gate_output"])
    with st.expander("Risk register (outputs/risk-register.md)", expanded=False):
        render_file(run.outputs / "risk-register.md", "gate-register")
    if state.get("assessor_report"):
        with st.expander("risk-assessor's report"):
            st.markdown(state["assessor_report"])
    _, rows, other = gate.read_decisions(run.outputs)
    if not rows:
        st.warning("auditor-comments.md has no decision table.")
        return
    st.caption("Approve, Amend or Reject every risk. For Amend, say exactly what to change; give a reason "
               "for Reject. The risk-assessor then re-issues the register and the agent team starts.")
    with st.form("decisions"):
        decisions = {}
        for r in rows:
            rid = r["Risk ID"]
            c1, c2, c3 = st.columns([4, 1.7, 3])
            c1.markdown(f"**{rid}** · {r.get('Risk', '')}  \n"
                        f"L{r.get('L', '')} × I{r.get('I', '')} = {r.get('Score', '')} · {r.get('Band', '')} · "
                        f"proposed scope: *{r.get('Proposed scope', '')}*")
            cur = r.get("Decision") if r.get("Decision") in gate.DECISIONS else "Approve"
            d = c2.selectbox("Decision", gate.DECISIONS, index=gate.DECISIONS.index(cur), key=f"d-{rid}",
                             label_visibility="collapsed")
            c = c3.text_input("Comment", value=r.get("Comment", ""), key=f"c-{rid}",
                              label_visibility="collapsed", placeholder="Comment (required for Amend/Reject)")
            decisions[rid] = (d, c)
        other_in = st.text_area("Other instructions (optional, e.g. \"add a risk on …\")", value=other)
        ok = st.form_submit_button("Submit decisions and start the agent team", type="primary")
    if ok:
        missing = [k for k, (d, c) in decisions.items() if d != "Approve" and not c.strip()]
        if missing:
            st.error(f"Add a comment for: {', '.join(missing)}")
            return
        try:
            run.submit_decisions(decisions, other_in)
            st.rerun()
        except RuntimeError as e:
            st.error(str(e))


def signoff_form(run: Run, state: dict) -> None:
    st.subheader("Gate 2 · Sign off the audit planning pack")
    if state.get("lead_report"):
        st.markdown("**Lead's report**")
        st.markdown(state["lead_report"])
    st.caption("Read the planning memo, risk-control matrix, audit program, challenges and QA review in "
               "the Outputs tab before you sign.")
    with st.form("signoff"):
        decision = st.radio("Decision", ["Sign off", "Return to the team"], horizontal=True)
        name = st.text_input("Name")
        role = st.text_input("Role", value="Internal auditor")
        comments = st.text_area("Comments")
        ok = st.form_submit_button("Record decision in review.md", type="primary")
    if ok:
        if not name.strip():
            st.error("Enter your name.")
            return
        run.sign_off(decision, name.strip(), role.strip(), comments.strip())
        st.rerun()


# ------------------------------------------------------------------ pages
def workflow(run: Run) -> None:
    state = run.state()
    status = state.get("status", "created")
    idx = stage_index(state)
    cols = st.columns(len(STAGES))
    for i, (col, (code, title, who, out)) in enumerate(zip(cols, STAGES)):
        mark = "✅" if i < idx else ("⏳" if i == idx and status == "running" else
                                    ("👤" if i == idx and status.startswith("awaiting") else "○"))
        col.markdown(f"{mark} **{title}**  \n<small>{who}<br>→ {out}</small>", unsafe_allow_html=True)
    st.divider()
    msg = STATUS_TEXT.get(status, status)
    if status == "running":
        st.info(f"⏳ {msg}: **{state.get('stage', '')}**. You can close this page; the run continues. "
                f"Return with this link: `?run={run.id}`")
    elif status in {"failed", "cancelled", "blocked"}:
        st.error(f"{msg}. {state.get('error') or ''}")
    elif status == "complete":
        st.success("✅ The pack is signed off. Download it below or browse it in the Outputs tab.")
    st.caption(cost_line(state))

    if status == "created":
        if st.button("▶ Start the agents", type="primary"):
            try:
                run.start()
                st.rerun()
            except RuntimeError as e:
                st.error(str(e))
    elif status == "running":
        if st.button("Cancel run"):
            run.cancel.set()
    elif status == "awaiting_decisions":
        decisions_form(run, state)
    elif status == "awaiting_signoff":
        signoff_form(run, state)
    elif status in {"failed", "cancelled"}:
        st.caption("Start a new run from the sidebar to try again.")
    if status in {"complete", "awaiting_signoff", "blocked"}:
        if state.get("lead_report") and status != "awaiting_signoff":
            st.markdown("**Lead's report**")
            st.markdown(state["lead_report"])
        st.download_button("⬇ Download all outputs (.zip)", run.zip_outputs(), file_name=f"audit-pack-{run.id}.zip")


def run_page(run: Run) -> None:
    st.markdown(f"#### Run `{run.id}`")
    tab_flow, tab_log, tab_out = st.tabs(["Workflow", "Agent activity", "Outputs"])

    live = run.state().get("status") == "running"
    every = 4 if live else None

    @st.fragment(run_every=every)
    def live_flow():
        if live and run.state().get("status") != "running":
            st.rerun()  # the stage finished: redraw the whole page (gate forms, buttons)
        workflow(run)

    @st.fragment(run_every=every)
    def live_log():
        activity(run, "log")

    with tab_flow:
        live_flow()
    with tab_log:
        live_log()
    with tab_out:
        outputs_browser(run.outputs, f"run-{run.id}")


def home() -> None:
    st.title("📋 Procurement Audit Planner")
    st.markdown(
        "An agent harness that plans an internal audit of **West Berkshire Council's procurement** from its "
        "public data. It runs the skills and agents our team built in Claude Code (Part A) as an "
        "independent web application on the Claude API: the rulebook becomes testable rules, Python analyses "
        "every payment, past audits are folded in, risks are rated with citations, **you** approve the "
        "register, and an agent team writes and cross-checks the audit planning pack for your sign-off.")
    st.markdown(
        "- **The model reads and judges; Python computes every number.**\n"
        "- **Everything is traceable** to the source PDFs and data.\n"
        "- **Indicators, not accusations.**")
    st.markdown("**Workflow**")
    for code, title, who, out in STAGES:
        st.markdown(f"- `{code}` **{title}** — {who} → `{out}`")
    st.info("Start a new run from the sidebar. A full run takes roughly 30–60 minutes of agent time; "
            "reusing Part A's Phase 1 outputs starts at the risk-assessor and takes about half as long.")


def sidebar() -> Run | None:
    sb = st.sidebar
    sb.header("Runs")
    if not config.api_key():
        sb.error("ANTHROPIC_API_KEY is not set on the server, so agents cannot run. See DEPLOY.md.")
    reuse = sb.checkbox("Reuse Part A's Phase 1 outputs (start at the risk-assessor)", value=False,
                        help="Copies rules.json, analytics.json and history.json from the completed Part A run.")
    if sb.button("➕ New run", type="primary", disabled=not config.api_key()):
        run = Run.create(reuse_phase1=reuse)
        st.query_params["run"] = run.id
        st.rerun()
    runs = Run.list_runs()
    if runs:
        labels = {r["id"]: f"{r['id']} · {STATUS_TEXT.get(r.get('status'), r.get('status', ''))[:28]}" for r in runs}
        current = st.query_params.get("run")
        ids = list(labels)
        pick = sb.radio("Open a run", ids, format_func=labels.get,
                        index=ids.index(current) if current in ids else None)
        if pick and pick != current:
            st.query_params["run"] = pick
            st.rerun()
    sb.divider()
    if sb.button("Part A example run"):
        st.query_params["run"] = "example"
        st.rerun()
    if sb.button("About"):
        st.query_params.clear()
        st.rerun()
    sb.caption(f"Model: `{config.model()}` · effort `{config.effort()}`")
    rid = st.query_params.get("run")
    return Run.load(rid) if rid and rid != "example" else None


def example_page() -> None:
    st.markdown("#### Part A example run")
    st.caption("The complete outputs of the team's Claude Code run (Part A), signed off on 2026-10-14. "
               "Read-only; use it to compare with a live run.")
    outputs_browser(config.EXAMPLE_RUN, "example")


def main() -> None:
    require_password()
    run = sidebar()
    if st.query_params.get("run") == "example":
        example_page()
    elif run:
        run_page(run)
    else:
        if st.query_params.get("run"):
            st.warning("That run was not found (runs are cleared when the server restarts).")
        home()


main()
