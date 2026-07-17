#!/usr/bin/env python3
"""
Tamper-evident capture of the Ironhack alumni-portal endpoint.

Unlike scrape.py (which keeps only parsed records), this saves each HTTP
response VERBATIM — raw body bytes + response headers (date, cf-ray, etag) —
into capture/, so a hash manifest can later attest exactly what the server
returned and when. It also refreshes the parsed JSONL/CSV so the analysis and
the attested bytes describe the same snapshot.

    IRONHACK_CSRF="<token>" python3 capture.py

Then run provenance.py to build the hash manifest, and timestamp it (RFC 3161).
"""
import csv
import json
import os
import sys
import time
import urllib.request

from scrape import API, flatten  # reuse the exact same parsing

HERE = os.path.dirname(__file__)
CAPDIR = os.path.join(HERE, "capture")
DATADIR = os.path.join(HERE, "data")
CAMPUSES = ["rmt", "par", "mad", "bcn", "ber", "mia", "lis", "ams", "sao", "mex"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def fetch_raw(token, track, campus, page, limit=100):
    body = json.dumps({"tracks": [track], "campus": campus, "isSearching": False}).encode()
    url = f"{API}?page={page}&limit={limit}"
    req = urllib.request.Request(url, data=body, method="POST")
    for k, v in {
        "Content-Type": "application/json", "x-csrf-token": token,
        "Accept": "application/json", "User-Agent": UA,
        "Origin": "https://my.ironhack.com", "Referer": "https://my.ironhack.com/",
    }.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
        # case-insensitive: Cloudflare sends header names lowercased over HTTP/2
        headers = {k.lower(): v for k, v in resp.getheaders()}
        status = resp.status
        return raw, headers, status, url, body


def main():
    token = os.environ.get("IRONHACK_CSRF")
    if not token:
        print("Set IRONHACK_CSRF.", file=sys.stderr)
        sys.exit(2)
    os.makedirs(CAPDIR, exist_ok=True)
    os.makedirs(DATADIR, exist_ok=True)

    for campus in CAMPUSES:
        cdir = os.path.join(CAPDIR, f"ux_{campus}")
        os.makedirs(cdir, exist_ok=True)
        records = []
        page = 1
        while True:
            raw, headers, status, url, reqbody = fetch_raw(token, "ux", campus, page)
            # verbatim body
            with open(os.path.join(cdir, f"p{page:02d}.body.json"), "wb") as f:
                f.write(raw)
            # response metadata (no PII) — the Cloudflare/server witness fields
            meta = {
                "request": {"method": "POST", "url": url,
                            "body": reqbody.decode()},
                "status": status,
                "date": headers.get("date"),
                "cf-ray": headers.get("cf-ray"),
                "server": headers.get("server"),
                "etag": headers.get("etag"),
                "content-length": headers.get("content-length"),
                "content-type": headers.get("content-type"),
            }
            with open(os.path.join(cdir, f"p{page:02d}.headers.json"), "w") as f:
                json.dump(meta, f, indent=2)
            data = json.loads(raw)
            pag = data.get("meta", {}).get("pagination", {})
            records.extend(data.get("result", []))
            print(f"{campus} p{page}/{pag.get('total_pages','?')} cf-ray={meta['cf-ray']} "
                  f"+{len(data.get('result', []))}")
            if not pag.get("has_next"):
                break
            page = pag.get("next", page + 1)
            time.sleep(0.6)

        # refresh parsed outputs so analysis == attested bytes
        with open(os.path.join(DATADIR, f"alumni_ux_{campus}.jsonl"), "w") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        rows = [flatten(r) for r in records]
        if rows:
            with open(os.path.join(DATADIR, f"alumni_ux_{campus}.csv"), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
        print(f"  {campus}: {len(records)} records")

    print("\nCapture complete -> capture/ . Next: python3 provenance.py")


if __name__ == "__main__":
    main()
