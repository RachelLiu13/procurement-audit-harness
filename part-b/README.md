# Part B: independent agent harness

- **Website:** https://procurement-audit-harness.fly.dev
- **Completed end-to-end run, signed off:** https://procurement-audit-harness.fly.dev/?run=live
  (every agent's tool calls and messages, both auditor gates, the final pack, and the lead's reports
  before and after sign-off; the zip of all outputs downloads from that page)
- **Part A example run:** https://procurement-audit-harness.fly.dev/?run=example (Part A's signed-off outputs, read-only)

Part B turns Part A into an **independently deployed web application**.
A Python harness re-creates what Claude Code provided (the agent loop, the
tools, sub-agents, skills, agent memory and agent-team messaging) on the Claude
API, and a web front end gives the human auditor the two gates. Nothing runs
on anyone's local machine:

```
browser ──► Fly.io (server.py: FastAPI + harness, Docker)
                 ├─ /       the website (web/)
                 └─ /api/*  runs, gates, events, files
                                                          │
                                                          └──► Claude API (the agents)
```

One Fly.io app serves both the website and the agent API from the same Docker
image, so there is a single URL. The agents need a long-lived server: a run
lasts 30–60 minutes and waits on the auditor between stages, longer than
serverless functions allow. The machine never auto-stops, and runs are kept on
a Fly volume (`/data`), so a run waiting at a gate survives a restart. The image
also installs `pdftotext` (poppler) for the PDF quote checks.

## What runs, end to end

| Stage | Component (from Part A) | Output |
| --- | --- | --- |
| 1 | `extract-rules` skill, run in the main session | `rules.json`, quotes checked by `verify_quotes.py` |
| 2 | `spend-analyst` and `findings-analyst` sub-agents, in parallel | `analytics.json`, `history.json` |
| 3 | `risk-assessor` sub-agent + `risk-assessment` skill (`build_register.py`) | `risk-register.md`, `auditor-comments.md` |
| **Gate 1** | **The auditor approves, amends or rejects each risk in the web UI** | `auditor-comments.md` filled in |
| 4 | `risk-assessor` issues the revision; the harness runs `build_pack.py --gate` | register revision, gate open |
| 5 | Agent team: `planner` (+ `audit-program` skill), `challenger`, `qa-reviewer` | planning memo, risk-control matrix, audit program, samples, `challenges.md`, `review.md` |
| 6 | Lead report | summary for the auditor |
| **Gate 2** | **The auditor signs off (or returns) the pack in the web UI** | `review.md` signed |

Every file the agents read and write is the same as in Part A, so Part A's
Python builders and its four QA checks run as they are (apart from the
analysis changes listed below). The principles carry over: the
model reads and judges, Python computes every number; everything is traceable;
indicators, not accusations.

## Analysis changes after review

| Change | Where | Effect |
| --- | --- | --- |
| Sample count reported as rows *and* unique transactions | `part-a/.claude/skills/audit-program/build_pack.py` | The memo states both figures, because a transaction drawn by more than one test is counted once per test |
| Buyer name matched case-insensitively | `part-a/scripts/clean.py`, CLAUDE.md, spend-analyst | 141 council notices instead of 135 |
| Statutory thresholds supplied | `part-a/data/statutory-thresholds.json`, `part-a/scripts/apply_thresholds.py`, `part-a/scripts/analyse.py` | Goods and services £207,720 incl. VAT (£173,100 excl.), works/concessions £5,193,000, light touch £663,540, in force from 1 Jan 2026 (PPN 023; Threshold Amounts (Amendment) Regulations 2025). Adds a clustering tier below £173,100 (CPR-54), and statutory tiers in `high_value_suppliers` and `off_contract`. "The relevant Threshold" stays skipped with a stated reason: the spend data has no contract-type field to choose between the three figures |

The completed run in `saved-runs/` and `web/live-run/` (signed off 2026-10-16) was run with these changes, as a full pipeline run (Phase 1 not reused).

## How the harness replaces Claude Code

| Claude Code (Part A) | This harness (`harness/`) |
| --- | --- |
| Agent file `.claude/agents/<name>.md` (frontmatter `tools`, `skills`) | `agent.py` parses the frontmatter. The system prompt is CLAUDE.md + the agent body + each preloaded `SKILL.md` + the agent's `MEMORY.md` |
| Built-in tools Bash, Read, Write, Edit, Glob, Grep | `tools.py` implements tools with the same names and arguments, confined to the run's workspace. Each agent gets only the tools its frontmatter lists |
| Sub-agent launched by the main session | `pipeline.py` runs each agent as its own Claude conversation (manual tool-use loop, streaming, adaptive thinking, prompt caching, refusal fallback) |
| `/extract-rules` typed by the human | Stage 1 runs the skill in a main-session agent |
| Experimental agent teams + `SendMessage` | `team.py`: one persistent conversation per teammate. `SendMessage` drops a message in the recipient's inbox, and a scheduler wakes whichever teammate has mail. The lead never relays; it collects `PLANNER DONE`, `CHALLENGER DONE`, `QA DONE` and stops the team |
| The auditor edits `auditor-comments.md` and `review.md` | `gate.py` writes the same cells from the web forms |
| Local `.venv` | Each run gets a fresh copy of `../part-a/` (without its outputs) in `RUNS_DIR/<id>`, with `.venv/bin/python` pointing at the server's Python. `pdftotext` and `jq` are installed by the `Dockerfile` |

Runs execute in a background thread on the server and record their state in
`run.json` and an event log in `events.jsonl`. The browser can close and come
back with `?run=<id>`, and the **Agent activity** tab shows every tool call,
message and report as it happens.

## Repository layout

```
web/                   the website: index.html, app.js, style.css (served by server.py)
server.py              FastAPI: the API over the harness (runs, gates, events, files, zip) and the website
harness/
  agent.py             agent assembly and the tool-use loop
  tools.py             Bash, Read, Write, Edit, Glob, Grep, SendMessage
  team.py              agent-team scheduler and message bus
  pipeline.py          stages, runs, state, gates
  gate.py              reads and writes auditor-comments.md and the review.md sign-off
  config.py            settings from environment variables
saved-runs/            completed Part B runs the server restores after every restart
web/live-run/          the same run as static files, for the read-only "Completed end-to-end run" page
                       (update both copies together with `python save_live_run.py <run-id>`)
tools/                 sensitivity_case_variant.py (sensitivity check of the six case-variant notices)
tests/test_harness.py  offline tests with a scripted fake Claude client
Dockerfile             the image (Python 3.12, poppler-utils, jq), built from the repository root
                       with ../fly.toml so it holds part-a/ as well (volume at /data)
```

## Running it

Locally, from `part-b/` (the server also serves `web/` at http://localhost:8000):

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # Python 3.10+
brew install poppler jq                                             # or apt install poppler-utils jq
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/uvicorn server:app --port 8000
```

Tests (no API key needed): `.venv/bin/python tests/test_harness.py`

To deploy, see [DEPLOY.md](DEPLOY.md) (run `fly` from the repository root). Settings (Fly.io secrets, or `[env]` in `fly.toml`):

| Name | Default | Meaning |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | required | Claude API key, server side only |
| `APP_PASSWORD` | none | If set, visitors must enter it |
| `CLAUDE_MODEL` | `claude-opus-5-5` | Model for every agent |
| `CLAUDE_EFFORT` | `medium` | `low` … `max` |
| `MAX_TURNS` / `MAX_TEAM_TURNS` | 60 / 30 | Safety caps per agent and per team |
| `MAX_ACTIVE_RUNS` | 1 | Concurrent runs per server |

The checkbox **Reuse Part A's Phase 1 outputs** starts a run at the
risk-assessor, using Part A's `rules.json`, `analytics.json` and `history.json`.
It is faster and cheaper for a demonstration. Leave it off for the full
pipeline.
