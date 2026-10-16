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
[Procurement Audit Planner guide](https://procurement-audit-planner.vercel.app/).
The full specification is in [`part-a/CLAUDE.md`](part-a/CLAUDE.md), and
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
