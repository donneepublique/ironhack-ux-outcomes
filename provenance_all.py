#!/usr/bin/env python3
"""
Tamper-evidence manifest for the ALL-TRACKS capture (capture_all/ + data_all/).

Same construction as provenance.py, pointed at the all-tracks dirs, writing
provenance_all/manifest.json. Git-ignored for now; timestamp it with RFC 3161
the same way (see PROVENANCE.md) to freeze it in time.
"""
import glob
import hashlib
import json
import os

from provenance import sha256_file, tls_cert, HOST

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "provenance_all")


def rel(p):
    return os.path.relpath(p, HERE)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = []
    files += sorted(glob.glob(os.path.join(HERE, "capture_all", "**", "*.json"), recursive=True))
    files += sorted(glob.glob(os.path.join(HERE, "data_all", "*.jsonl")))
    files += sorted(glob.glob(os.path.join(HERE, "data_all", "*.csv")))
    rep = os.path.join(HERE, "data_all", "report_tracks.json")
    if os.path.isfile(rep):
        files.append(rep)

    entries = [{"path": rel(p), "sha256": sha256_file(p), "bytes": os.path.getsize(p)}
               for p in files if os.path.isfile(p)]
    lines = sorted(f"{e['sha256']}  {e['path']}" for e in entries)
    root = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()

    cf_rays, dates = [], []
    for e in entries:
        if e["path"].endswith(".headers.json"):
            with open(os.path.join(HERE, e["path"])) as f:
                m = json.load(f)
            if m.get("cf-ray"):
                cf_rays.append(m["cf-ray"])
            if m.get("date"):
                dates.append(m["date"])

    manifest = {
        "what_this_is": "Tamper-evidence manifest for the ALL-TRACKS Ironhack capture (private).",
        "endpoint": "POST https://my.ironhack.com/api/alumni",
        "tracks": ["ux", "wd", "da", "cy", "ai", "ml"],
        "host": HOST,
        "n_files": len(entries),
        "merkle_root_sha256": root,
        "cloudflare_witness": {
            "cf_ray_count": len(cf_rays), "cf_rays": cf_rays,
            "server_date_min": min(dates) if dates else None,
            "server_date_max": max(dates) if dates else None,
        },
        "tls_certificate": tls_cert(),
        "files": entries,
    }
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"files hashed : {len(entries)}")
    print(f"merkle root  : {root}")
    print(f"cf-rays      : {len(cf_rays)}")
    print(f"wrote        : provenance_all/manifest.json")


if __name__ == "__main__":
    main()
