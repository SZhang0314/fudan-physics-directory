#!/usr/bin/env python3
"""Merge enriched_N.json fragments into data/faculty.json.

For each record in an enriched fragment, find the matching faculty record by id
and merge in research_directions, focus_areas, summary, homepage, email,
publications, and title. Promote confidence to 'fine' when research_directions
and homepage (or publications) are present.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

MERGE_FIELDS = ["research_directions", "focus_areas", "summary",
                "homepage", "email", "title", "publications"]


def main():
    faculty = json.loads((DATA / "faculty.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in faculty["professors"]}

    total_merged = 0
    for frag in sorted(DATA.glob("enriched_*.json")):
        try:
            recs = json.loads(frag.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"skip {frag.name}: {e}")
            continue
        for rec in recs:
            p = by_id.get(rec.get("id"))
            if not p:
                print(f"  no match id={rec.get('id')} name={rec.get('name')}")
                continue
            for f in MERGE_FIELDS:
                v = rec.get(f)
                if v:
                    p[f] = v
            total_merged += 1

    # promote confidence
    fine = 0
    for p in faculty["professors"]:
        if p.get("research_directions") and (p.get("homepage") or p.get("publications")):
            p["confidence"] = "fine"
            p["verified"] = True
            fine += 1

    faculty["generated_at"] = "2026-10-01T00:00:00Z"
    (DATA / "faculty.json").write_text(
        json.dumps(faculty, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"merged {total_merged} enriched records, {fine} now 'fine', "
          f"total {len(faculty['professors'])}")


if __name__ == "__main__":
    main()
