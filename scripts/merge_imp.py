#!/usr/bin/env python3
"""Merge IMP (Modern Physics Institute) roster into faculty.json.

Reads data/imp.json (raw IMP parse) and appends records to data/faculty.json,
skipping names already present in the Physics department list (e.g. 马余刚).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

PUFF = {
    "核物理": "粒子物理与原子核物理",
    "粒子物理": "粒子物理与原子核物理",
    "原子分子物理": "原子与分子物理",
    "核技术": "核技术及应用",
    "计算物理": "计算物理",
    "聚变科学与工程": "聚变科学与工程",
}


def slugify(name):
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def main():
    faculty = json.loads((DATA / "faculty.json").read_text(encoding="utf-8"))
    imp = json.loads((DATA / "imp.json").read_text(encoding="utf-8"))

    existing_names = {p["name"] for p in faculty["professors"]}
    seen_ids = {p["id"] for p in faculty["professors"]}

    added = 0
    skipped = 0
    idx = 0
    for rec in imp:
        name = rec["name"].strip()
        if name in existing_names:
            skipped += 1
            idx += 1
            continue
        pid = f"fudan-imp-{idx:03d}"
        while pid in seen_ids:
            idx += 1
            pid = f"fudan-imp-{idx:03d}"
        idx += 1
        seen_ids.add(pid)
        existing_names.add(name)

        sources = ["https://imp.fudan.edu.cn/49366/list.htm",
                   "https://imp.fudan.edu.cn/49367/list.htm",
                   "https://imp.fudan.edu.cn/49368/list.htm",
                   "https://imp.fudan.edu.cn/49369/list.htm",
                   "https://imp.fudan.edu.cn/49370/list.htm",
                   "https://imp.fudan.edu.cn/49371/list.htm"]
        entry = {
            "id": pid,
            "name": name,
            "school": "复旦大学",
            "department": "现代物理研究所（核科学与技术系）",
            "title": rec.get("title", ""),
            "subject": "物理学",
            "research_directions": [PUFF.get(rec.get("imp_section", ""), rec.get("imp_section", ""))],
            "focus_areas": [PUFF.get(rec.get("imp_section", ""), rec.get("imp_section", ""))],
            "email": rec.get("email", ""),
            "sources": sources,
            "confidence": "coarse",
            "verified": False,
        }
        if rec.get("profile_url"):
            entry["profile_url"] = rec["profile_url"]
        faculty["professors"].append(entry)
        added += 1

    faculty["generated_at"] = "2026-10-01T00:00:00Z"
    (DATA / "faculty.json").write_text(
        json.dumps(faculty, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"added {added}, skipped {skipped}, total {len(faculty['professors'])}")


if __name__ == "__main__":
    main()
