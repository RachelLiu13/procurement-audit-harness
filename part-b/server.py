"""HTTP API for the harness, plus the website (web/) at /. Deployed on Fly.io.

Runs take tens of minutes and wait on the auditor between stages, so they live
here, on a long-running server, not in short serverless functions.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse, Response
from pydantic import BaseModel

from harness import config, gate
from harness.pipeline import STATUS_TEXT, Run

app = FastAPI(title="Procurement Audit Planner API")
Run.restore_saved()  # runs committed to saved-runs/ come back after every restart
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
                   allow_methods=["*"], allow_headers=["*"])

TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt"}


def check_password(x_app_password: str | None = Header(default=None)) -> None:
    pw = config.app_password()
    if pw and x_app_password != pw:
        raise HTTPException(401, "Wrong or missing access password.")


def get_run(run_id: str) -> Run:
    run = Run.load(run_id)
    if not run:
        raise HTTPException(404, "Run not found (runs are cleared when the server restarts).")
    return run


def outputs_dir(run_id: str) -> Path:
    return config.EXAMPLE_RUN if run_id == "example" else get_run(run_id).outputs


def public_state(run: Run) -> dict:
    s = run.state()
    return {"id": run.id, "status_text": STATUS_TEXT.get(s.get("status"), s.get("status")), **s}


# ------------------------------------------------------------------ info
@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "key_configured": bool(config.api_key()), "model": config.model(),
            "effort": config.effort(), "password_required": bool(config.app_password())}


@app.get("/api/auth", dependencies=[Depends(check_password)])
def auth() -> dict:
    return {"ok": True}


# ------------------------------------------------------------------ runs
class NewRun(BaseModel):
    reuse_phase1: bool = False


@app.get("/api/runs", dependencies=[Depends(check_password)])
def list_runs() -> list[dict]:
    return [{"id": r["id"], "status": r.get("status"), "stage": r.get("stage"),
             "status_text": STATUS_TEXT.get(r.get("status"), r.get("status")),
             "created": r.get("created"), "reuse_phase1": r.get("reuse_phase1")} for r in Run.list_runs()]


@app.post("/api/runs", dependencies=[Depends(check_password)])
def create_run(body: NewRun) -> dict:
    if not config.api_key():
        raise HTTPException(503, "ANTHROPIC_API_KEY is not configured on the server.")
    return public_state(Run.create(reuse_phase1=body.reuse_phase1))


@app.get("/api/runs/{run_id}", dependencies=[Depends(check_password)])
def run_state(run_id: str) -> dict:
    return public_state(get_run(run_id))


def _act(fn) -> dict:
    try:
        fn()
    except RuntimeError as e:
        raise HTTPException(409, str(e))
    return {"ok": True}


@app.post("/api/runs/{run_id}/start", dependencies=[Depends(check_password)])
def start(run_id: str) -> dict:
    run = get_run(run_id)
    if run.state().get("status") != "created":
        raise HTTPException(409, "This run has already started.")
    return _act(run.start)


@app.post("/api/runs/{run_id}/cancel", dependencies=[Depends(check_password)])
def cancel(run_id: str) -> dict:
    get_run(run_id).cancel.set()
    return {"ok": True}


@app.get("/api/runs/{run_id}/events", dependencies=[Depends(check_password)])
def events(run_id: str, after: int = 0) -> dict:
    ev = get_run(run_id).events()
    return {"total": len(ev), "events": ev[after:]}


# ------------------------------------------------------------------ gates
@app.get("/api/runs/{run_id}/decisions", dependencies=[Depends(check_password)])
def decisions(run_id: str) -> dict:
    run = get_run(run_id)
    if not (run.outputs / "auditor-comments.md").exists():
        raise HTTPException(404, "The register has not been built yet.")
    _, rows, other = gate.read_decisions(run.outputs)
    return {"rows": rows, "other": other, "choices": gate.DECISIONS}


class Decisions(BaseModel):
    decisions: dict[str, tuple[str, str]]
    other: str = ""


@app.post("/api/runs/{run_id}/decisions", dependencies=[Depends(check_password)])
def submit_decisions(run_id: str, body: Decisions) -> dict:
    run = get_run(run_id)
    if run.state().get("status") != "awaiting_decisions":
        raise HTTPException(409, "The run is not waiting for decisions.")
    bad = [k for k, (d, c) in body.decisions.items() if d not in gate.DECISIONS or (d != "Approve" and not c.strip())]
    if bad:
        raise HTTPException(422, f"Each Amend or Reject needs a comment: {', '.join(bad)}")
    return _act(lambda: run.submit_decisions(body.decisions, body.other))


class SignOff(BaseModel):
    decision: str
    name: str
    role: str = ""
    comments: str = ""


@app.post("/api/runs/{run_id}/signoff", dependencies=[Depends(check_password)])
def sign_off(run_id: str, body: SignOff) -> dict:
    run = get_run(run_id)
    if run.state().get("status") != "awaiting_signoff":
        raise HTTPException(409, "The pack is not waiting for sign-off.")
    if body.decision not in {"Sign off", "Return to the team"} or not body.name.strip():
        raise HTTPException(422, "Choose a decision and enter your name.")
    run.sign_off(body.decision, body.name.strip(), body.role.strip(), body.comments.strip())
    return {"ok": True}


@app.post("/api/runs/{run_id}/final-report", dependencies=[Depends(check_password)])
def final_report(run_id: str) -> dict:
    """The lead's report after the auditor's decision. Written automatically at sign-off;
    this starts it for a run signed before that existed. Once written, it is not redone."""
    run = get_run(run_id)
    if run.state().get("final_report_status") == "done":
        raise HTTPException(409, "The final report has already been written.")
    if not config.api_key():
        raise HTTPException(503, "ANTHROPIC_API_KEY is not configured on the server.")
    return _act(run.start_final_report)


# ------------------------------------------------------------------ files
@app.get("/api/runs/{run_id}/files", dependencies=[Depends(check_password)])
def files(run_id: str) -> list[str]:
    out = outputs_dir(run_id)
    if not out.exists():
        return []
    return [str(p.relative_to(out)) for p in sorted(out.rglob("*"))
            if p.is_file() and p.suffix in TEXT_SUFFIXES]


@app.get("/api/runs/{run_id}/file", dependencies=[Depends(check_password)])
def file(run_id: str, path: str) -> Response:
    out = outputs_dir(run_id).resolve()
    p = (out / path).resolve()
    if out not in p.parents or not p.is_file() or p.suffix not in TEXT_SUFFIXES:
        raise HTTPException(404, "File not found.")
    return PlainTextResponse(p.read_text(encoding="utf-8", errors="replace"))


@app.get("/api/runs/{run_id}/zip", dependencies=[Depends(check_password)])
def zip_outputs(run_id: str) -> Response:
    run = get_run(run_id)
    return Response(run.zip_outputs(), media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="audit-pack-{run.id}.zip"'})


# ------------------------------------------------------------------ website
WEB = (Path(__file__).parent / "web").resolve()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB / "index.html")


@app.get("/{path:path}")
def static(path: str) -> FileResponse:
    """Files under web/, including web/live-run/ for the read-only "Completed end-to-end run" page."""
    p = (WEB / path).resolve()
    if not p.is_relative_to(WEB) or not p.is_file():
        raise HTTPException(404)
    return FileResponse(p)
