# Part B's changes to Part A files

`../../part-a/` is Part A exactly as the team completed it. The files here are
the Part A files that Part B amends after review, at the same paths. When the
harness builds a run's workspace it copies `part-a/` and then copies these files
over it (`harness/pipeline.py`, `Run._workspace`), so every run on the website
uses them. This README is not copied.

| Change | Files |
| --- | --- |
| Sample count reported as rows *and* unique transactions | `.claude/skills/audit-program/build_pack.py` |
| Buyer names in the Contracts Finder export matched case-insensitively | `scripts/clean.py`, `CLAUDE.md`, `.claude/agents/spend-analyst.md`, `.claude/agent-memory/spend-analyst/input-formats.md` |
| Procurement Act 2023 thresholds supplied with sources | `data/statutory-thresholds.json`, `scripts/apply_thresholds.py`, `scripts/analyse.py`, `.claude/skills/extract-rules/SKILL.md`, `CLAUDE.md` |

Part A had already recorded the buyer-name and threshold issues as open
questions for the auditor: the six case-variant notices in its cleaning log, and
the thresholds as `null` parameters with a note that the auditor supplies them. See `../README.md` → "Analysis changes
after review" for the effect of each change.
