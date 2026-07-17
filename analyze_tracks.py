#!/usr/bin/env python3
"""
Per-track headline analysis over the all-tracks capture (data_all/).

Prints a comparison table and writes data_all/report_tracks.json (git-ignored).
Reuses the exact same status->bucket mapping as the published ux analysis.
"""
import glob
import json
import os
from collections import Counter

from analyze_all import BUCKETS, IN_FIELD, PLACED_BROAD, NOT_JOB_SEEKING, pct

HERE = os.path.dirname(__file__)
DATADIR = os.path.join(HERE, "data_all")
TRACK_NAME = {"ux": "UX/UI Design", "wd": "Web Development", "da": "Data Analytics",
              "cy": "Cybersecurity", "ai": "AI Engineering", "ml": "Data Science & ML"}


def load(track):
    rows = []
    p = os.path.join(DATADIR, f"alumni_{track}.jsonl")
    if not os.path.isfile(p):
        return rows
    with open(p) as f:
        for line in f:
            r = json.loads(line)
            cs = r.get("career_services") or {}
            rows.append(cs.get("status") or "")
    return rows


def analyze(statuses):
    n = len(statuses)
    sc = Counter(statuses)
    bc = Counter(BUCKETS.get(s, "Other/unknown") for s in statuses)
    in_field = sum(sc.get(s, 0) for s in IN_FIELD)
    placed = sum(sc.get(s, 0) for s in PLACED_BROAD)
    seekers = n - sum(sc.get(s, 0) for s in NOT_JOB_SEEKING)
    return {
        "n": n,
        "in_field_n": in_field,
        "in_field_pct": pct(in_field, n),
        "never_placed_pct": pct(bc.get("Never placed / searching / inactive", 0), n),
        "not_designer_or_field_pct": pct(bc.get("Job, but NOT as a designer", 0), n),
        "freelance_pct": pct(bc.get("Freelance / self-employed", 0), n),
        "ironhack_style_placed_pct": pct(placed, seekers),
        "buckets": dict(bc.most_common()),
        "status": dict(sc.most_common()),
    }


def main():
    report = {"note": "Per-track outcomes, Ironhack alumni-portal directory. Private/unpublished.",
              "tracks": {}}
    order = ["wd", "ux", "da", "cy", "ai", "ml"]
    print(f"{'track':22s} {'n':>5s} {'in-field':>9s} {'never-plc':>10s} {'not-in-field job':>17s} {'IH-style placed':>16s}")
    total = 0
    for t in order:
        st = load(t)
        if not st:
            continue
        a = analyze(st)
        report["tracks"][t] = a
        total += a["n"]
        print(f"{TRACK_NAME.get(t,t):22s} {a['n']:5d} {a['in_field_pct']:8.1f}% "
              f"{a['never_placed_pct']:9.1f}% {a['not_designer_or_field_pct']:16.1f}% "
              f"{a['ironhack_style_placed_pct']:15.1f}%")
    report["grand_total"] = total
    print(f"{'TOTAL':22s} {total:5d}")
    os.makedirs(DATADIR, exist_ok=True)
    with open(os.path.join(DATADIR, "report_tracks.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("\nWrote data_all/report_tracks.json (git-ignored)")


if __name__ == "__main__":
    main()
