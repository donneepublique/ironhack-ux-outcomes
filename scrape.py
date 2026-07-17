#!/usr/bin/env python3
"""
Scrape Ironhack's public alumni directory (my.ironhack.com/api/alumni).

This is the same data Ironhack surfaces on its own alumni marketing pages.
We store it verbatim (JSONL, full fidelity) and a flattened CSV for analysis.

Usage:
    IRONHACK_CSRF="<token>" python3 scrape.py --track ux --campus rmt

The CSRF token is short-lived; grab a fresh one from the Network tab of the
alumni page if requests start returning 401/403.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error

API = "https://my.ironhack.com/api/alumni"
# The CSRF token is read from the IRONHACK_CSRF env var — never commit it.
# Grab a fresh one from the Network tab of the alumni page when it expires.


def fetch_page(token, track, campus, page, limit):
    body = json.dumps(
        {"tracks": [track], "campus": campus, "isSearching": False}
    ).encode()
    url = f"{API}?page={page}&limit={limit}"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-csrf-token", token)
    req.add_header("Accept", "application/json")
    # Cloudflare (error 1010) blocks the default Python-urllib UA; mimic a browser.
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    )
    req.add_header("Accept-Language", "en-US,en;q=0.9")
    req.add_header("Origin", "https://my.ironhack.com")
    req.add_header("Referer", "https://my.ironhack.com/")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def link(links, name):
    for l in links or []:
        if l.get("name") == name:
            return l.get("url", "")
    return ""


def fact(facts, name):
    for f in facts or []:
        if f.get("name") == name:
            return (f.get("content") or "").replace("\n", " ").strip()
    return ""


def flatten(rec):
    cohort = rec.get("cohort") or {}
    cs = rec.get("career_services") or {}
    outcome = cs.get("outcome") or {}
    links = rec.get("links") or []
    facts = rec.get("profile_facts") or []
    return {
        "id": rec.get("id", ""),
        "first_name": rec.get("first_name", ""),
        "last_name": rec.get("last_name", ""),
        "track": cohort.get("track", ""),
        "campus": cohort.get("campus", ""),
        "end_date": (cohort.get("end_date") or "")[:10],
        "career_status": cs.get("status", ""),
        "outcome_type": outcome.get("outcome_type", ""),
        "outcome_company": outcome.get("company", ""),
        "outcome_job_title": outcome.get("job_title", ""),
        "linkedin": link(links, "linkedin"),
        "portfolio": link(links, "portfolio"),
        "medium": link(links, "medium"),
        "cv": link(links, "cv"),
        "calendly": link(links, "calendly"),
        "n_links": len(links),
        "has_picture": bool(rec.get("picture")),
        "quote": fact(facts, "quote"),
        "why_ironhack": fact(facts, "why_ironhack"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", default="ux")
    ap.add_argument("--campus", default="rmt")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--sleep", type=float, default=1.0)
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(__file__), "data"))
    args = ap.parse_args()

    token = os.environ.get("IRONHACK_CSRF")
    if not token:
        print("Set IRONHACK_CSRF to a valid x-csrf-token (see Network tab).", file=sys.stderr)
        sys.exit(2)
    os.makedirs(args.outdir, exist_ok=True)
    tag = f"{args.track}_{args.campus}"
    jsonl_path = os.path.join(args.outdir, f"alumni_{tag}.jsonl")
    csv_path = os.path.join(args.outdir, f"alumni_{tag}.csv")

    records = []
    page = 1
    total = None
    while True:
        try:
            data = fetch_page(token, args.track, args.campus, page, args.limit)
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code} on page {page}: {e.read()[:200]!r}", file=sys.stderr)
            sys.exit(1)
        pag = data.get("meta", {}).get("pagination", {})
        total = pag.get("total", total)
        batch = data.get("result", [])
        records.extend(batch)
        print(f"page {page}/{pag.get('total_pages','?')}  +{len(batch)}  total so far {len(records)}/{total}")
        if not pag.get("has_next"):
            break
        page = pag.get("next", page + 1)
        time.sleep(args.sleep)

    # raw JSONL (full fidelity, keep PII locally for analysis)
    with open(jsonl_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # flattened CSV
    rows = [flatten(r) for r in records]
    if rows:
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    print(f"\nSaved {len(records)} records")
    print(f"  {jsonl_path}")
    print(f"  {csv_path}")
    if total and len(records) != total:
        print(f"WARNING: collected {len(records)} but API reported total {total}", file=sys.stderr)


if __name__ == "__main__":
    main()
