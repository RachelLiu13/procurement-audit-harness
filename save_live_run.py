"""Copy one finished run from the deployed server into web/live-run/, so the site keeps
showing it after the free Render instance restarts (which clears stored runs).

Usage: python save_live_run.py <run-id> [https://<site>.vercel.app]

Writes web/live-run/state.json, events.json, files.json and outputs/<text files>.
Only web/ changes, so pushing it does not redeploy the agent server.
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
              "verdict", "gate_output", "assessor_report", "lead_report", "status_text"]


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
    print(f"saved run {run_id} ({state.get('status')}): {len(files)} files to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
