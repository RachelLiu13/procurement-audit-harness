"""Fill the statutory threshold parameters in outputs/rules.json from the auditor-supplied
data/statutory-thresholds.json.

The Contract Procedure Rules refer to the Procurement Legislation thresholds but do not
state them, so /extract-rules leaves those parameters null. The auditor supplies each
figure with its source; this script copies them in. The Act's figures include VAT, while
the rules and the spend data's Net amount exclude it, so `value` is the VAT-exclusive
equivalent (rounded to whole pounds) and `value_incl_vat` keeps the figure as published.

Usage: python scripts/apply_thresholds.py [outputs/rules.json] [data/statutory-thresholds.json]
Parameters with no supplied figure are left null with the auditor's reason in `note`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    rules_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "rules.json"
    src_path = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "statutory-thresholds.json"
    if not src_path.exists():
        print(f"no {src_path.name}: statutory parameters stay null")
        return 0
    rules = json.loads(rules_path.read_text())
    src = json.loads(src_path.read_text())
    vat = float(src["vat_rate_assumed"])
    params = rules.setdefault("parameters", {})
    filled = []
    for name, p in params.items():
        s = src.get("parameters", {}).get(name)
        if s:
            incl = int(s["value_incl_vat"])
            p["value"] = int(round(incl / (1 + vat)))
            p["value_incl_vat"] = incl
            p["vat_basis"] = (f"value = value_incl_vat / {1 + vat:g} (VAT-exclusive, to compare with the rules' "
                              "VAT-exclusive amounts and the spend data's Net amount)")
            p["source"] = s["source"]
            p["effective_from"] = src["effective_from"]
            p["supplied_by"] = "auditor: data/statutory-thresholds.json"
            filled.append(f"{name} = {p['value']} (incl. VAT {incl})")
        elif name in src.get("not_supplied", {}):
            p["note"] = src["not_supplied"][name]
    rules["parameters_sources"] = src.get("sources", [])
    rules_path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n")
    print("filled: " + ("; ".join(filled) if filled else "none"))
    left = [n for n, p in params.items() if p.get("value") is None]
    print("still null: " + (", ".join(left) if left else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
