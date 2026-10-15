"""Save one finished run from the deployed server into the repository, in both places
it is kept, so the two copies always match:

- web/live-run/  static files for the read-only "Part B live run" page on Vercel
                 (state.json, events.json, files.json, outputs/<text files>)
- saved-runs/<id>/  what the agent server restores after a restart
                 (run.json, events.jsonl, outputs/)

Usage: python save_live_run.py <run-id> [https://<site>.vercel.app]

Pushing saved-runs/ redeploys the agent server (which then restores this run), so push
when no other run is in progress.
"""
from __future__ import annotations

import io
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

TEXT = {".md", ".json", ".csv", ".txt"}
KEEP_STATE = ["id", "status", "stage", "created", "updated", "reuse_phase1", "model", "effort", "usage",
              "verdict", "gate_output", "assessor_report", "lead_report", "final_report", "final_report_status",
              "status_text"]


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def main() -> int:
    run_id = sys.argv[1]
    site = (sys.argv[2] if len(sys.argv) > 2 else "https://procurement-audit-harness-web.vercel.app").rstrip("/")
    api = f"{site}/api/runs/{run_id}"
    out = Path(__file__).parent / "web" / "live-run"
    if out.exists():
        shutil.rmtree(out)
    (out / "outputs").mkdir(parents=True)

    state = json.loads(fetch(api))
    (out / "state.json").write_text(json.dumps({k: state.get(k) for k in KEEP_STATE}, indent=1))
    (out / "events.json").write_bytes(fetch(api + "/events?after=0"))

    files = []
    with zipfile.ZipFile(io.BytesIO(fetch(api + "/zip"))) as z:
        for name in z.namelist():
            rel = name.removeprefix("outputs/")
            if Path(rel).suffix in TEXT and not name.endswith("/"):
                dest = out / "outputs" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(z.read(name))
                files.append(rel)
    (out / "files.json").write_text(json.dumps(sorted(files), indent=1))

    saved = Path(__file__).parent / "saved-runs" / run_id
    if saved.exists():
        shutil.rmtree(saved)
    (saved / "outputs").mkdir(parents=True)
    for rel in files:
        dest = saved / "outputs" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out / "outputs" / rel, dest)
    run_state = {k: state.get(k) for k in KEEP_STATE if k != "status_text"}
    (saved / "run.json").write_text(json.dumps(run_state, indent=1))
    events = json.loads((out / "events.json").read_text())["events"]
    (saved / "events.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in events))

    a = sorted(p.relative_to(out / "outputs") for p in (out / "outputs").rglob("*") if p.is_file())
    b = sorted(p.relative_to(saved / "outputs") for p in (saved / "outputs").rglob("*") if p.is_file())
    same = a == b and all((out / "outputs" / f).read_bytes() == (saved / "outputs" / f).read_bytes() for f in a)
    print(f"saved run {run_id} ({state.get('status')}): {len(files)} files to {out} and {saved}; "
          f"copies identical: {same}")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
