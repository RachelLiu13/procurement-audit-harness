"""Sensitivity check: include the Contracts Finder notices whose buyer name is a case
variant of the council's name ("WEST BERKSHIRE COUNCIL"), which clean.py excludes by its
exact-match rule, and see what changes downstream.

Usage: python tools/sensitivity_case_variant.py saved-runs/<run-id>/outputs

Method (no model calls; every number comes from the project's own scripts):
1. Run Part A's clean.py + analyse.py twice on the run's rules.json: as specified
   (exact match) and with a case-insensitive buyer-name match. Only the buyer-name
   line of clean.py differs.
2. The run's own analytics.json came from the spend-analyst's version of the scripts.
   The three tests that use the notices (off_contract, expired_notice_spend,
   spend_vs_award) are checked to be reproduced exactly by step 1's exact-match leg;
   the variant then replaces only those three tests (and their analytics-full lists)
   in a copy of the run's outputs.
3. Re-run build_register.py with the run's risk-ratings.json and build_pack.py with the
   run's audit-plan.json on that copy, and compare every risk's score, band and scope
   and every test's sampled row_ids with the run as signed.

Writes <outputs>/analytics-full/sensitivity-case-variant.json and .md.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PART_A = ROOT.parent / "part-a"
CONTRACT_TESTS = ["off_contract", "expired_notice_spend", "spend_vs_award"]
CONTRACT_FILES = ["supplier-match.csv", "near-matches.csv", "expired_notice_spend.csv",
                  "spend_vs_award.csv", "notices-clean.csv"]
EXACT = "keep = orgs.isin(COUNCIL_NAMES)"
CASELESS = "keep = orgs.str.upper().isin({n.upper() for n in COUNCIL_NAMES})"


def sh(cwd: Path, *args: str) -> str:
    r = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode not in (0,):
        raise SystemExit(f"{' '.join(args)} failed in {cwd}:\n{r.stdout}\n{r.stderr}")
    return r.stdout


def workspace(tmp: Path, name: str, outputs: Path | None, rules: Path) -> Path:
    w = tmp / name
    shutil.copytree(PART_A, w, ignore=lambda d, n: ["outputs"] if Path(d) == PART_A else [])
    if outputs:
        shutil.copytree(outputs, w / "outputs")
    else:
        (w / "outputs").mkdir()
        shutil.copy2(rules, w / "outputs" / "rules.json")
    return w


def analyse(w: Path, caseless: bool) -> dict:
    if caseless:
        p = w / "scripts" / "clean.py"
        s = p.read_text()
        assert EXACT in s, "clean.py no longer has the exact-match line"
        p.write_text(s.replace(EXACT, CASELESS))
    sh(w, "scripts/clean.py")
    sh(w, "scripts/analyse.py")
    return json.loads((w / "outputs" / "analytics.json").read_text())


def scrub(t: dict) -> dict:
    return {k: v for k, v in t.items() if k not in ("rule_ids",)}


def register_view(w: Path) -> dict:
    st = json.loads((w / "outputs" / "risk-register.state.json").read_text())
    return {rid: {k: r.get(k) for k in ("likelihood", "impact", "uplift", "scope", "status")}
            for rid, r in st["risks"].items()}


def samples_view(w: Path) -> dict:
    return read_samples(w / "outputs")


def read_samples(outputs: Path) -> dict:
    import csv
    out = {}
    for f in sorted((outputs / "samples").glob("T-*.csv")):
        with f.open() as fh:
            out[f.stem] = sorted(row["row_id"] for row in csv.DictReader(fh))
    return out


def main() -> int:
    outputs = Path(sys.argv[1]).resolve()
    tmp = Path(tempfile.mkdtemp())
    exact = analyse(workspace(tmp, "exact", None, outputs / "rules.json"), caseless=False)
    wc = workspace(tmp, "caseless", None, outputs / "rules.json")
    caseless = analyse(wc, caseless=True)
    run = json.loads((outputs / "analytics.json").read_text())

    reproduced = {t: scrub(exact["tests"][t]) == scrub(run["tests"][t]) for t in CONTRACT_TESTS}
    if not all(reproduced.values()):
        raise SystemExit(f"exact-match leg does not reproduce the run's contract tests: {reproduced}")

    # the run as signed, rebuilt in place (proves the builders reproduce it), and the variant
    signed = workspace(tmp, "signed", outputs, outputs / "rules.json")
    variant = workspace(tmp, "variant", outputs, outputs / "rules.json")
    va = json.loads((variant / "outputs" / "analytics.json").read_text())
    for t in CONTRACT_TESTS:
        rule_ids = va["tests"][t].get("rule_ids")
        va["tests"][t] = caseless["tests"][t]
        if rule_ids is not None:
            va["tests"][t]["rule_ids"] = rule_ids
    (variant / "outputs" / "analytics.json").write_text(json.dumps(va, indent=1, default=str))
    for f in CONTRACT_FILES:
        src = wc / "outputs" / "analytics-full" / f
        if src.exists():
            shutil.copy2(src, variant / "outputs" / "analytics-full" / f)

    views = {}
    for name, w in (("signed", signed), ("variant", variant)):
        reg = sh(w, ".claude/skills/risk-assessment/build_register.py")
        pack = sh(w, ".claude/skills/audit-program/build_pack.py")
        views[name] = {"register": register_view(w), "samples": samples_view(w),
                       "register_out": reg.strip().splitlines()[-1], "pack_out": pack.strip().splitlines()[0]}

    def headline(a: dict) -> dict:
        t = a["tests"]
        return {
            "no_notice_general_procurement_suppliers": t["off_contract"]["headline_general_procurement_no_notice_found"]["suppliers"],
            "no_notice_general_procurement_annualised_gbp": t["off_contract"]["headline_general_procurement_no_notice_found"]["annualised_estimate_gbp"],
            "expired_notice_spend_gbp_in_window": t["expired_notice_spend"]["gbp_in_window"],
            "spend_vs_award_suppliers_compared": t["spend_vs_award"]["suppliers_compared"],
            "spend_vs_award_suppliers_flagged": t["spend_vs_award"].get("flagged"),
        }

    log_e = json.loads((tmp / "exact/outputs/analytics-full/cleaning-log.json").read_text())["contracts"]
    log_c = json.loads((wc / "outputs/analytics-full/cleaning-log.json").read_text())["contracts"]
    risk_changes = {rid: {"signed": views["signed"]["register"][rid], "variant": views["variant"]["register"].get(rid)}
                    for rid in views["signed"]["register"]
                    if views["signed"]["register"][rid] != views["variant"]["register"].get(rid)}
    sample_changes = {}
    for tid in sorted(set(views["signed"]["samples"]) | set(views["variant"]["samples"])):
        a, b = set(views["signed"]["samples"].get(tid, [])), set(views["variant"]["samples"].get(tid, []))
        if a != b:
            sample_changes[tid] = {"signed": len(a), "variant": len(b), "added": sorted(b - a), "removed": sorted(a - b)}
    signed_matches_run = views["signed"]["samples"] == read_samples(outputs)

    result = {
        "method": __doc__.split("Method", 1)[1].split("Writes", 1)[0].strip(),
        "notices": {"exact": log_e.get("rows_for_council"), "caseless": log_c.get("rows_for_council"),
                    "active_in_window": [log_e.get("active_in_window"), log_c.get("active_in_window")]},
        "contract_tests_reproduced_by_exact_leg": reproduced,
        "headline": {"signed": headline(run), "variant": headline(va)},
        "rebuilt_signed_samples_match_run": signed_matches_run,
        "builders": {k: {"register": v["register_out"], "pack": v["pack_out"]} for k, v in views.items()},
        "risk_changes": risk_changes,
        "sample_changes": sample_changes,
    }
    af = outputs / "analytics-full"
    (af / "sensitivity-case-variant.json").write_text(json.dumps(result, indent=1, default=str))

    h = result["headline"]
    changed = ", ".join(f"{t}: {v['signed']}→{v['variant']}" for t, v in sample_changes.items())
    lines = [
        "# Sensitivity check: notices with the buyer name in capitals",
        "",
        "Generated by `tools/sensitivity_case_variant.py`; full detail in `sensitivity-case-variant.json`.",
        "",
        f"Council notices kept: {result['notices']['exact']} (exact match, as run) → {result['notices']['caseless']} (case-insensitive).",
        f"The exact-match leg reproduces the run's three contract tests: {all(reproduced.values())}.",
        f"Rebuilding the signed run with the builders reproduces its samples: {signed_matches_run}.",
        "",
        "| Measure | As signed | Including the case-variant notices |",
        "| --- | --- | --- |",
    ] + [f"| {k} | {h['signed'][k]} | {h['variant'][k]} |" for k in h["signed"]] + [
        "",
        f"Risks whose likelihood, impact, uplift, scope or status changes: {len(risk_changes)}"
        + (f" ({', '.join(risk_changes)})" if risk_changes else "") + ".",
        f"Tests whose sampled row_ids change: {len(sample_changes)}"
        + (f" ({changed})" if sample_changes else "") + ".",
        "",
        "Builders, as signed: " + views["signed"]["pack_out"],
        "Builders, variant: " + views["variant"]["pack_out"],
    ]
    (af / "sensitivity-case-variant.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
