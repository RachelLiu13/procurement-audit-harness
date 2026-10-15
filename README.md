# Procurement Audit Planner: independent agent harness (Part B)

Part A built a procurement audit planner for West Berkshire Council as a
Claude Code project: 3 skills, 6 agents and an agent team
([Part A repository](https://github.com/crystaljingjiang/procurement-audit-planner)).
It only ran inside Claude Code on a team member's machine.

This repository turns it into an **independently deployed web application**.
A Python harness re-creates what Claude Code provided (the agent loop, the
tools, sub-agents, skills, agent memory and agent-team messaging) on the Claude
API, and a web front end gives the human auditor the two gates. Nothing runs
on anyone's local machine:

```
browser ──► Vercel (web/: static site)  ──/api/*──►  Render (server.py: FastAPI + harness, Docker)
                                                          │
                                                          └──► Claude API (the agents)
```

Vercel serves the site and forwards `/api/*` to the agent server. The agent
server runs on Render because a run lasts 30–60 minutes and waits on the
auditor between stages, which is longer than Vercel's serverless functions
allow. It also needs `pdftotext` (poppler) for the PDF quote checks.

## What runs, end to end

| Stage | Component (from Part A, unchanged) | Output |
| --- | --- | --- |
| 1 | `extract-rules` skill, run in the main session | `rules.json`, quotes checked by `verify_quotes.py` |
| 2 | `spend-analyst` and `findings-analyst` sub-agents, in parallel | `analytics.json`, `history.json` |
| 3 | `risk-assessor` sub-agent + `risk-assessment` skill (`build_register.py`) | `risk-register.md`, `auditor-comments.md` |
| **Gate 1** | **The auditor approves, amends or rejects each risk in the web UI** | `auditor-comments.md` filled in |
| 4 | `risk-assessor` issues the revision; the harness runs `build_pack.py --gate` | register revision, gate open |
| 5 | Agent team: `planner` (+ `audit-program` skill), `challenger`, `qa-reviewer` | planning memo, risk-control matrix, audit program, samples, `challenges.md`, `review.md` |
| 6 | Lead report | summary for the auditor |
| **Gate 2** | **The auditor signs off (or returns) the pack in the web UI** | `review.md` signed |

Every file the agents read and write is the same as in Part A, so the Python
builders and the four QA checks run unchanged. The principles carry over: the
model reads and judges, Python computes every number; everything is traceable;
indicators, not accusations.

## How the harness replaces Claude Code

| Claude Code (Part A) | This harness (`harness/`) |
| --- | --- |
| Agent file `.claude/agents/<name>.md` (frontmatter `tools`, `skills`) | `agent.py` parses the frontmatter. The system prompt is CLAUDE.md + the agent body + each preloaded `SKILL.md` + the agent's `MEMORY.md` |
| Built-in tools Bash, Read, Write, Edit, Glob, Grep | `tools.py` implements tools with the same names and arguments, confined to the run's workspace. Each agent gets only the tools its frontmatter lists |
| Sub-agent launched by the main session | `pipeline.py` runs each agent as its own Claude conversation (manual tool-use loop, streaming, adaptive thinking, prompt caching, refusal fallback) |
| `/extract-rules` typed by the human | Stage 1 runs the skill in a main-session agent |
| Experimental agent teams + `SendMessage` | `team.py`: one persistent conversation per teammate. `SendMessage` drops a message in the recipient's inbox, and a scheduler wakes whichever teammate has mail. The lead never relays; it collects `PLANNER DONE`, `CHALLENGER DONE`, `QA DONE` and stops the team |
| The auditor edits `auditor-comments.md` and `review.md` | `gate.py` writes the same cells from the web forms |
| Local `.venv` | Each run gets a copy of the project in `RUNS_DIR/<id>`, with `.venv/bin/python` pointing at the server's Python. `pdftotext` and `jq` come from `packages.txt` |

Runs execute in a background thread on the server and record their state in
`run.json` and an event log in `events.jsonl`. The browser can close and come
back with `?run=<id>`, and the **Agent activity** tab shows every tool call,
message and report as it happens.

## Repository layout

```
web/                   the Vercel site: index.html, app.js, style.css, vercel.json (/api rewrite)
server.py              FastAPI API over the harness (runs, gates, events, files, zip)
harness/
  agent.py             agent assembly and the tool-use loop
  tools.py             Bash, Read, Write, Edit, Glob, Grep, SendMessage
  team.py              agent-team scheduler and message bus
  pipeline.py          stages, runs, state, gates
  gate.py              reads and writes auditor-comments.md and the review.md sign-off
  config.py            settings from environment variables
project/               a full copy of Part A (its README, CLAUDE.md, .claude/ agents + skills,
                       scripts/, data/); copied into a fresh workspace for each run
example_run/outputs/   Part A's outputs/: the completed, signed-off run, viewable in the app
tests/test_harness.py  offline tests with a scripted fake Claude client
Dockerfile, render.yaml   the agent server on Render (Python 3.12, poppler-utils, jq)
```

## Running it

Locally (the server also serves `web/` at http://localhost:8000):

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # Python 3.10+
brew install poppler jq                                             # or apt install poppler-utils jq
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/uvicorn server:app --port 8000
```

Tests (no API key needed): `.venv/bin/python tests/test_harness.py`

To deploy, see [DEPLOY.md](DEPLOY.md). Settings (environment variables on the Render service):

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
