# Procurement Audit Planner: Part A + Part B (Team 9)

An agent system that plans an internal audit of West Berkshire Council's
procurement from its public data: it reads the purchasing rulebook, analyses
every payment, folds in past audit history, produces a risk register for a human
auditor to approve, and turns the approved risks into a checked audit plan.

| | **Part A**: rebuild using Skills & Agents | **Part B**: independent harness |
| --- | --- | --- |
| Where in this repository | [`part-a/`](part-a/) (details in [`part-a/README.md`](part-a/README.md)) | [`part-b/`](part-b/) (details in [`part-b/README.md`](part-b/README.md)) |
| Runs on | Claude Code, on a team member's machine | Fly.io, in the browser: **https://procurement-audit-harness.fly.dev** |
| Signed-off result | [`part-a/outputs/`](part-a/outputs/) | **https://procurement-audit-harness.fly.dev/?run=live** |

Part B runs Part A's skills and agents unchanged in architecture: every run on
the website starts from a fresh copy of `part-a/`, with Part B's analysis
changes (`part-b/part-a-changes/`) copied over it.

---

## Part A: Skills and Agents

We completed all 27 steps of the
[Procurement Audit Planner guide](https://procurement-audit-planner.vercel.app/);
the [checklist below](#guide-steps-completed) maps each step to what it left
in the repository. The full specification is in [`part-a/CLAUDE.md`](part-a/CLAUDE.md), and
[`part-a/README.md`](part-a/README.md) documents each component in detail.

**Skills** (`part-a/.claude/skills/`)

| Skill | What it does |
| --- | --- |
| `extract-rules` | Turns the Contract Procedure Rules PDF into `rules.json`: every testable rule with clause, thresholds, approver and a verbatim quote that `verify_quotes.py` checks against the PDF |
| `risk-assessment` | The method for rating risks on the council's likelihood × impact scale. The agent writes cited judgments; `build_register.py` resolves every citation, computes scores and bands, and renders the risk register and the auditor's decision sheet |
| `audit-program` | Turns the approved risks into controls, test steps, samples and a PBC list; `build_pack.py` checks the approval gate, draws and verifies every sample, and renders the planning memo, risk-control matrix and audit program |

**Agents** (`part-a/.claude/agents/`)

| Agent | Type | What it does |
| --- | --- | --- |
| `spend-analyst` | sub-agent | Writes and runs Python that cleans the spend and Contracts Finder data and runs the risk tests → `analytics.json` |
| `findings-analyst` | sub-agent | Extracts past audits, opinions, actions and the council's risk-scoring method from committee papers → `history.json` |
| `risk-assessor` | sub-agent | Rates risks with citations using the `risk-assessment` skill → `risk-register.md`; re-issues it after the auditor's decisions |
| `planner` | agent team | Builds the planning pack with the `audit-program` skill |
| `challenger` | agent team | Challenges weak spots in the pack and messages the planner directly |
| `qa-reviewer` | agent team | Runs the four QA scripts (quotes, numbers, trace, samples) and writes `review.md` |

**How they work together**

```
contract-rules.pdf ─(1) extract-rules skill─▶ rules.json
        ├─(2a) spend-analyst ──────▶ analytics.json ─┐
        └─(2b) findings-analyst ───▶ history.json ───┤
                     (3) risk-assessor + risk-assessment skill ─▶ risk-register.md
                     (4) HUMAN GATE 1: auditor approves / amends / rejects each risk
                     (5) agent team: planner ⇄ challenger, planner ⇄ qa-reviewer
                         ─▶ planning memo, risk-control matrix, audit program, review.md
                     (6) HUMAN GATE 2: auditor signs off
```

Throughout, the model reads and judges while Python computes every number;
every quote, figure and rating is traceable to its source; and outputs describe
risk indicators to investigate, never wrongdoing.

### Guide steps completed

All 27 steps of the guide, in its own order and numbering. Paths are relative
to [`part-a/`](part-a/).

**Setup (7)**

| | Step | Evidence in the repository |
| --- | --- | --- |
| ✅ | Prerequisite: VS Code installed | Development environment (no file) |
| ✅ | Prerequisite: Claude Code installed and signed in | The whole project was built in Claude Code: `.claude/` |
| ✅ | 1.1 Make a folder, open it, and start Claude Code | The project folder, `part-a/` |
| ✅ | 1.2 Hand over the project brief | `CLAUDE.md` |
| ✅ | 1.3 Download the data folder | `data/contract-rules.pdf`, `data/contracts.csv`, `data/spend/` (3 workbooks), `data/committee/` (4 PDFs) |
| ✅ | 1.4 Set up Python and check the data | `requirements.txt` (pandas, openpyxl); `.venv/` is git-ignored |
| ✅ | 1.5 Create the project folders | `.claude/skills/`, `.claude/agents/`, `scripts/`, `outputs/` |

**Lesson 1: Skills (2)**

| | Step | Evidence in the repository |
| --- | --- | --- |
| ✅ | 2.1 Build the extract-rules skill | `.claude/skills/extract-rules/SKILL.md`, `verify_quotes.py` |
| ✅ | 2.2 Run the skill | `outputs/rules.json` (67 rules, 95 excluded); `verify_quotes.py`: ALL CHECKS PASSED |

**Lesson 2: Sub-agents (7)**

| | Step | Evidence in the repository |
| --- | --- | --- |
| ✅ | 3.1 Build the spend-analyst | `.claude/agents/spend-analyst.md`; the scripts it wrote: `scripts/clean.py`, `scripts/analyse.py`, `scripts/selfcheck.py` |
| ✅ | 3.2 Run the spend-analyst | `outputs/analytics.json`, `outputs/analytics-full/` |
| ✅ | 3.3 Build the findings-analyst | `.claude/agents/findings-analyst.md`, `scripts/verify_history.py` |
| ✅ | 3.4 Run the findings-analyst and check it | `outputs/history.json` (every item checked by `scripts/verify_history.py`), `outputs/committee-text/` |
| ✅ | 3.5 Build the risk-assessment skill | `.claude/skills/risk-assessment/SKILL.md`, `build_register.py`, `tests/` |
| ✅ | 3.6 Build the risk-assessor sub-agent | `.claude/agents/risk-assessor.md` |
| ✅ | 3.7 Run the risk-assessor and review the register | `outputs/risk-ratings.json`, `outputs/risk-register.md`, `outputs/auditor-comments.md` |

**Lesson 3: The human gate (3)**

| | Step | Evidence in the repository |
| --- | --- | --- |
| ✅ | 4.1 Open the decision template | `outputs/auditor-comments.md`, one Decision row per risk |
| ✅ | 4.2 Record your decisions | `outputs/auditor-comments.md`: a decision on all 7 risks (all Approve) |
| ✅ | 4.3 Revise the register | `outputs/risk-register.md` is Revision 1 and applies the decisions; `outputs/risk-register.state.json` |

**Lesson 4: Agent teams (8)**

| | Step | Evidence in the repository |
| --- | --- | --- |
| ✅ | 5.1 Close the gate | Every risk approved in revision 1, so no further revision was needed; `build_pack.py --gate` prints GATE OPEN |
| ✅ | 5.2 Enable agent teams | `.claude/settings.json`: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| ✅ | 5.3 Build the audit-program skill | `.claude/skills/audit-program/SKILL.md`, `build_pack.py`, `tests/` |
| ✅ | 5.4 Build the planner | `.claude/agents/planner.md` |
| ✅ | 5.5 Build the challenger | `.claude/agents/challenger.md` |
| ✅ | 5.6 Build the qa-reviewer and its checks | `.claude/agents/qa-reviewer.md`; `scripts/checks/` (`run_checks.py`, `check_quotes.py`, `check_numbers.py`, `check_trace.py`, `check_samples.py`) |
| ✅ | 5.7 Run the team | `outputs/planning-memo.md`, `risk-control-matrix.md`, `audit-program.md`, `samples/` (8 files), `challenges.md`, `review.md` (pack v4, READY FOR SIGN-OFF); team lessons in `.claude/agent-memory/` |
| ✅ | 5.8 Sign off | The completed sign-off block at the end of `outputs/review.md` |

`part-a/` is Part A exactly as completed, identical to the team's Part A
repository. The analysis improvements made later, for Part B, are kept apart in
[`part-b/part-a-changes/`](part-b/part-a-changes/); see
[Analysis changes after review](part-b/README.md#analysis-changes-after-review).

---

## Part B: Independent harness

Part B turns Part A into an **independently deployed web application**. A
Python harness re-creates what Claude Code provided (the agent loop, tools,
sub-agents, skills, agent memory and agent-team messaging) on the Claude API,
and a web front end gives the human auditor the two gates. Nothing runs on
anyone's local machine.

- **Website:** https://procurement-audit-harness.fly.dev
- **Completed end-to-end run, signed off:** https://procurement-audit-harness.fly.dev/?run=live
- **Details:** [`part-b/README.md`](part-b/README.md) (architecture, how the harness replaces
  Claude Code, analysis changes after review, running and deploying)

---

## Repository layout

```
README.md          this overview
part-a/            Part A: the Claude Code project
  README.md          skills, agents, how they work together
  CLAUDE.md          full specification
  .claude/           skills/, agents/, agent-memory/, settings.json
  scripts/           analysis scripts and the four QA checks
  data/              public inputs (rules PDF, spend, Contracts Finder, committee papers)
  outputs/           Part A's signed-off run
part-b/            Part B: the deployed harness
  README.md          architecture and how to run it
  server.py          FastAPI: the API and the website
  harness/           agent loop, tools, agent team, pipeline, gates
  part-a-changes/    Part B's analysis changes to Part A files, applied in each run
  web/               the website; web/live-run/ is the completed run, read-only
  saved-runs/        the completed run, restored by the server after a restart
  tests/, tools/     offline tests; a sensitivity check
  Dockerfile         the image (holds part-a/ and part-b/)
  DEPLOY.md          deployment guide
fly.toml           Fly.io app config (at the root because the image is built from here)
```
