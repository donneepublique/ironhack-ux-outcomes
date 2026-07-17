#!/usr/bin/env python3
"""
Combined analysis across ALL scraped Ironhack UX campuses.

Aggregate & anonymous only. Produces data/report_all.json for the writeup.
Also reconstructs Ironhack's own "% placed" headline to show how the
90%-style claim is manufactured (narrow denominator + broad numerator).
"""
import csv
import glob
import json
import os
from collections import Counter, defaultdict
from datetime import date

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "data")
AS_OF = date(2026, 7, 17)
MATURE_MONTHS = 12

# ---- status semantics ------------------------------------------------------
# A salaried, in-field design job — the thing the marketing implies you get.
IN_FIELD = {"hired_in_field"}
# Ironhack-style "placed": ANY employment outcome counts.
PLACED_BROAD = {
    "hired_in_field", "hired_out_of_field", "freelance", "entrepreneur",
    "internship", "short_term", "back_to_job", "ironhack_employee",
}
# People Ironhack's methodology drops from the "job-seeking" denominator.
NOT_JOB_SEEKING = {
    "back_to_university", "not_graduated_cs", "not_eligible",
    "personal_development", "withdrew", "inactive",
    "intervention_education", "intervention_education_not_success",
}

BUCKETS = {
    "hired_in_field": "Salaried designer job (in field)",
    "freelance": "Freelance / self-employed",
    "entrepreneur": "Freelance / self-employed",
    "hired_out_of_field": "Job, but NOT as a designer",
    "back_to_job": "Job, but NOT as a designer",
    "ironhack_employee": "Job, but NOT as a designer",
    "internship": "Internship only",
    "short_term": "Internship only",
    "placement_not_successful": "Never placed / searching / inactive",
    "searching": "Never placed / searching / inactive",
    "inactive": "Never placed / searching / inactive",
    "deferred_more_than_45d": "Never placed / searching / inactive",
    "deferred_less_than_45d": "Never placed / searching / inactive",
    "intervention_careers": "Never placed / searching / inactive",
    "intervention_careers_not_success": "Never placed / searching / inactive",
    "intervention_education": "Never placed / searching / inactive",
    "intervention_education_not_success": "Never placed / searching / inactive",
    "back_to_university": "Left the field (school / other)",
    "personal_development": "Left the field (school / other)",
    "withdrew": "Left the field (school / other)",
    "not_graduated_cs": "Did not complete / not eligible",
    "not_eligible": "Did not complete / not eligible",
}


def months_since(s):
    if not s:
        return None
    return (AS_OF.year - int(s[:4])) * 12 + (AS_OF.month - int(s[5:7]))


def pct(n, d):
    return round(100 * n / d, 1) if d else 0.0


def load_all():
    rows = []
    for path in sorted(glob.glob(os.path.join(DATA, "alumni_ux_*.csv"))):
        with open(path) as f:
            for r in csv.DictReader(f):
                rows.append(r)
    return rows


def analyze(rows):
    n = len(rows)
    status = Counter(r["career_status"] or "(empty)" for r in rows)
    buckets = Counter(BUCKETS.get(r["career_status"], "Other/unknown") for r in rows)
    in_field = sum(status.get(s, 0) for s in IN_FIELD)
    placed_broad = sum(status.get(s, 0) for s in PLACED_BROAD)
    job_seekers = n - sum(status.get(s, 0) for s in NOT_JOB_SEEKING)
    return {
        "n": n,
        "in_field_n": in_field,
        "in_field_pct_of_all": pct(in_field, n),
        # Ironhack-style headline: broad "placed" over the job-seeker denominator
        "job_seekers": job_seekers,
        "placed_broad_n": placed_broad,
        "ironhack_style_placed_pct": pct(placed_broad, job_seekers),
        "status": dict(status.most_common()),
        "buckets": dict(buckets.most_common()),
    }


def main():
    rows = load_all()
    overall = analyze(rows)

    mature = [r for r in rows if (months_since(r["end_date"]) or 0) >= MATURE_MONTHS]
    overall_mature = analyze(mature)

    # per-campus in-field rate (is "remote" an outlier?)
    by_campus = defaultdict(list)
    for r in rows:
        by_campus[r["campus"] or "?"].append(r)
    per_campus = {
        c: {"n": len(rs),
            "in_field_pct": pct(sum(1 for r in rs if r["career_status"] == "hired_in_field"), len(rs)),
            "never_placed_pct": pct(sum(1 for r in rs if BUCKETS.get(r["career_status"]) == "Never placed / searching / inactive"), len(rs))}
        for c, rs in sorted(by_campus.items(), key=lambda kv: -len(kv[1]))
    }

    # freelance tenure across all campuses
    fl = sorted(m for r in rows if r["career_status"] == "freelance" and (m := months_since(r["end_date"])) is not None)
    freelance = {
        "n": len(fl),
        "pct_of_all": pct(len(fl), len(rows)),
        "median_months_since_grad": fl[len(fl) // 2] if fl else None,
        "over_24m_n": sum(1 for m in fl if m >= 24),
    }

    report = {
        "source": "my.ironhack.com/api/alumni (public alumni directory), scraped 2026-07",
        "scope": "track=ux, all 10 campuses",
        "as_of": AS_OF.isoformat(),
        "ironhack_public_claims": {
            "placed_6mo_job_seeking": "90% of job-seeking grads placed within 6 months (PwC-audited)",
            "employed_180d_uxui": "83% of job-seeking UX/UI grads employed within 180 days",
            "avg_starting_salary_usd": 65000,
        },
        "overall": overall,
        "overall_mature_cohorts": {"cutoff_months": MATURE_MONTHS, **overall_mature},
        "per_campus": per_campus,
        "freelance_signal": freelance,
    }
    with open(os.path.join(DATA, "report_all.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # ---- console ----
    n = overall["n"]
    print(f"ALL CAMPUSES — n = {n} UX alumni\n")
    print("What actually happened (Ironhack's own labels, grouped):")
    for b, c in overall["buckets"].items():
        print(f"  {pct(c,n):5.1f}%  {c:5d}  {b}")
    print(f"\nHired as a designer (in field): {overall['in_field_n']}/{n} = {overall['in_field_pct_of_all']}%")
    print(f"Mature cohorts (>= {MATURE_MONTHS} mo): {overall_mature['in_field_n']}/{overall_mature['n']} = {overall_mature['in_field_pct_of_all']}%")
    print(f"\n--- Reconstructing Ironhack's headline ---")
    print(f"Job-seeker denominator (drop inactive/back-to-school/etc.): {overall['job_seekers']}")
    print(f"'Placed' = ANY job (incl. out-of-field/freelance/back-to-old-job): {overall['placed_broad_n']}")
    print(f"=> Ironhack-style 'placed' rate = {overall['ironhack_style_placed_pct']}%  (vs their claimed ~90%)")
    print(f"\nFreelance: n={freelance['n']} ({freelance['pct_of_all']}%), median {freelance['median_months_since_grad']} mo since grad, {freelance['over_24m_n']} still freelance >=24mo out")
    print(f"\nPer-campus in-field rate:")
    for c, d in per_campus.items():
        print(f"  {c:5s} n={d['n']:4d}  in_field={d['in_field_pct']:5.1f}%  never_placed={d['never_placed_pct']:5.1f}%")
    print(f"\nWrote data/report_all.json")


if __name__ == "__main__":
    main()
