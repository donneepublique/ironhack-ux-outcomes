#!/usr/bin/env python3
"""
Tamper-evident capture of ALL Ironhack tracks (not just ux).

The endpoint accepts an omitted campus filter, so each track is fetched in one
paginated pass covering every campus. Outputs go to SEPARATE dirs from the
published ux material (capture_all/ and data_all/), and are git-ignored for now.

    IRONHACK_CSRF="<token>" python3 capture_all.py

Then: provenance_all.py to hash+manifest, and timestamp it (RFC 3161).
"""
import csv
import json
import os
import sys
import time
import urllib.request

from scrape import API, flatten

HERE = os.path.dirname(__file__)
CAPDIR = os.path.join(HERE, "capture_all")
DATADIR = os.path.join(HERE, "data_all")
# discovered track codes (campus omitted -> all campuses):
TRACKS = ["ux", "wd", "da", "cy", "ai", "ml"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def fetch_raw(token, track, page, limit=100):
    body = json.dumps({"tracks": [track], "isSearching": False}).encode()
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
        headers = {k.lower(): v for k, v in resp.getheaders()}
        return raw, headers, resp.status, url, body


def main():
    token = os.environ.get("IRONHACK_CSRF")
    if not token:
        print("Set IRONHACK_CSRF.", file=sys.stderr)
        sys.exit(2)
    os.makedirs(CAPDIR, exist_ok=True)
    os.makedirs(DATADIR, exist_ok=True)

    grand = 0
    for track in TRACKS:
        tdir = os.path.join(CAPDIR, track)
        os.makedirs(tdir, exist_ok=True)
        records, page = [], 1
        while True:
            raw, headers, status, url, reqbody = fetch_raw(token, track, page)
            with open(os.path.join(tdir, f"p{page:02d}.body.json"), "wb") as f:
                f.write(raw)
            meta = {
                "request": {"method": "POST", "url": url, "body": reqbody.decode()},
                "status": status, "date": headers.get("date"),
                "cf-ray": headers.get("cf-ray"), "server": headers.get("server"),
                "etag": headers.get("etag"),
                "content-length": headers.get("content-length"),
                "content-type": headers.get("content-type"),
            }
            with open(os.path.join(tdir, f"p{page:02d}.headers.json"), "w") as f:
                json.dump(meta, f, indent=2)
            data = json.loads(raw)
            pag = data.get("meta", {}).get("pagination", {})
            records.extend(data.get("result", []))
            print(f"{track} p{page}/{pag.get('total_pages','?')} cf-ray={meta['cf-ray']} "
                  f"total={pag.get('total')}")
            if not pag.get("has_next"):
                break
            page = pag.get("next", page + 1)
            time.sleep(0.6)

        with open(os.path.join(DATADIR, f"alumni_{track}.jsonl"), "w") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        rows = [flatten(r) for r in records]
        if rows:
            with open(os.path.join(DATADIR, f"alumni_{track}.csv"), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
        grand += len(records)
        print(f"  {track}: {len(records)} records\n")

    print(f"TOTAL captured: {grand} alumni across {len(TRACKS)} tracks")
    print("Next: python3 provenance_all.py")


if __name__ == "__main__":
    main()
