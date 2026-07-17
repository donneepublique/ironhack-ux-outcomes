#!/usr/bin/env python3
"""
Analyze the scraped Ironhack alumni data.

Everything here is AGGREGATE and ANONYMOUS: we count statuses, never emit
names. Outputs a report-ready JSON (data/report.json) with counts only.
"""
import csv
import json
import os
from collections import Counter
from datetime import date

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "data")

# As-of date for cohort-maturity math (kept explicit; no Date.now equivalent).
AS_OF = date(2026, 7, 17)
MATURE_MONTHS = 12  # a fair "you've had a full year to land a job" cutoff


def months_since(end_date_str):
    if not end_date_str:
        return None
    y, m, d = int(end_date_str[:4]), int(end_date_str[5:7]), int(end_date_str[8:10])
    return (AS_OF.year - y) * 12 + (AS_OF.month - m)


# How each raw Ironhack status maps to a plain-language bucket.
BUCKETS = {
    "hired_in_field": "Salaried designer job (in field)",
    "freelance": "Freelance / self-employed",
    "entrepreneur": "Freelance / self-employed",
    "hired_out_of_field": "Job, but NOT as a designer",
    "back_to_job": "Job, but NOT as a designer",   # returned to prior (non-design) job
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


def load():
    rows = []
    with open(os.path.join(DATA, "alumni_ux_rmt.csv")) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def pct(n, d):
    return round(100 * n / d, 1) if d else 0.0


def main():
    rows = load()
    n = len(rows)

    status_counts = Counter(r["career_status"] or "(empty)" for r in rows)
    bucket_counts = Counter(
        BUCKETS.get(r["career_status"], "Other / unknown") for r in rows
    )

    # ---- headline rates (whole population) ----
    hired = status_counts.get("hired_in_field", 0)
    freelance = status_counts.get("freelance", 0)
    entre = status_counts.get("entrepreneur", 0)
    intern = status_counts.get("internship", 0) + status_counts.get("short_term", 0)

    # ---- mature cohorts only (>= MATURE_MONTHS since graduation) ----
    mature = [r for r in rows if (months_since(r["end_date"]) or 0) >= MATURE_MONTHS]
    nm = len(mature)
    mature_status = Counter(r["career_status"] or "(empty)" for r in mature)
    mature_bucket = Counter(
        BUCKETS.get(r["career_status"], "Other / unknown") for r in mature
    )
    mh = mature_status.get("hired_in_field", 0)

    # ---- freelance tenure: still freelance how long after graduating? ----
    freelancers = [r for r in rows if r["career_status"] == "freelance"]
    fl_tenure = sorted(m for r in freelancers if (m := months_since(r["end_date"])) is not None)
    fl_median = fl_tenure[len(fl_tenure) // 2] if fl_tenure else None
    fl_over_18m = sum(1 for m in fl_tenure if m >= 18)

    # ---- who are the "hired_in_field" working for / as? (aggregate) ----
    hired_rows = [r for r in rows if r["career_status"] == "hired_in_field"]
    hired_titles = Counter(r["outcome_job_title"] or "(unspecified)" for r in hired_rows)
    hired_companies = Counter(r["outcome_company"].strip() or "(unspecified)" for r in hired_rows)

    report = {
        "source": "my.ironhack.com/api/alumni (Ironhack alumni-portal directory, login-gated)",
        "track": "ux",
        "campus": "rmt (remote)",
        "as_of": AS_OF.isoformat(),
        "n_total": n,
        "headline": {
            "hired_in_field_n": hired,
            "hired_in_field_pct": pct(hired, n),
            "any_paid_design_outcome_n": hired + freelance + entre + intern,
            "any_paid_design_outcome_pct": pct(hired + freelance + entre + intern, n),
            "placement_not_successful_pct": pct(status_counts.get("placement_not_successful", 0), n),
        },
        "mature_cohorts": {
            "cutoff_months": MATURE_MONTHS,
            "n": nm,
            "hired_in_field_n": mh,
            "hired_in_field_pct": pct(mh, nm),
            "bucket_breakdown": dict(mature_bucket.most_common()),
        },
        "freelance_signal": {
            "n": freelance,
            "pct": pct(freelance, n),
            "median_months_since_grad": fl_median,
            "still_freelance_over_18m_n": fl_over_18m,
        },
        "status_breakdown": dict(status_counts.most_common()),
        "bucket_breakdown": dict(bucket_counts.most_common()),
        "hired_in_field_titles": dict(hired_titles.most_common(10)),
        "hired_in_field_companies_top": dict(hired_companies.most_common(15)),
    }

    with open(os.path.join(DATA, "report.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # ---- console summary ----
    print(f"n = {n} UX alumni (remote campus)\n")
    print("BUCKETS (whole population):")
    for b, c in bucket_counts.most_common():
        print(f"  {pct(c,n):5.1f}%  {c:4d}  {b}")
    print(f"\nHEADLINE: hired as a designer (in field) = {hired}/{n} = {pct(hired,n)}%")
    print(f"Any paid design outcome (hired+freelance+entrepreneur+intern) = {pct(hired+freelance+entre+intern,n)}%")
    print(f"\nMATURE cohorts (graduated >= {MATURE_MONTHS} mo ago), n={nm}:")
    print(f"  hired in field = {mh}/{nm} = {pct(mh,nm)}%")
    for b, c in mature_bucket.most_common():
        print(f"    {pct(c,nm):5.1f}%  {c:4d}  {b}")
    print(f"\nFreelance: {freelance} people, median {fl_median} months since grad, "
          f"{fl_over_18m} still freelance >=18mo out")
    print(f"\nTop 'hired_in_field' job titles: {dict(hired_titles.most_common(6))}")
    print(f"\nReport written to data/report.json")


if __name__ == "__main__":
    main()
