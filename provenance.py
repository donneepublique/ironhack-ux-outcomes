#!/usr/bin/env python3
"""
Build a tamper-evidence manifest over the raw capture + analysis inputs.

Outputs provenance/manifest.json:
  - SHA-256 of every raw response body and header file in capture/
  - SHA-256 of the parsed analysis inputs (data/alumni_ux_*.jsonl, report_all.json)
  - a Merkle-style root over all of the above (sha256 of the sorted "hash  path" lines)
  - the Cloudflare witness fields (cf-ray, server Date) extracted from headers
  - the live TLS certificate fingerprint of my.ironhack.com

The manifest is then timestamped with a trusted RFC 3161 authority (see
PROVENANCE.md), which freezes it in time: after that, no later deletion or
edit by Ironhack can change what we can prove the endpoint returned.
"""
import glob
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "provenance")
HOST = "my.ironhack.com"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, HERE)


def tls_cert():
    try:
        p1 = subprocess.run(
            ["openssl", "s_client", "-connect", f"{HOST}:443", "-servername", HOST],
            input=b"", capture_output=True, timeout=20)
        p2 = subprocess.run(
            ["openssl", "x509", "-noout", "-fingerprint", "-sha256",
             "-issuer", "-subject", "-dates"],
            input=p1.stdout, capture_output=True, timeout=20)
        out = p2.stdout.decode(errors="replace")
        info = {"host": HOST}
        for line in out.splitlines():
            if "=" in line:
                k, _, v = line.partition("=")
                info[k.strip().lower().replace(" ", "_")] = v.strip()
        return info
    except Exception as e:  # noqa
        return {"host": HOST, "error": str(e)}


def main():
    os.makedirs(OUT, exist_ok=True)

    files = []
    files += sorted(glob.glob(os.path.join(HERE, "capture", "**", "*.json"), recursive=True))
    files += sorted(glob.glob(os.path.join(HERE, "data", "alumni_ux_*.jsonl")))
    files += sorted(glob.glob(os.path.join(HERE, "data", "alumni_ux_*.csv")))
    files.append(os.path.join(HERE, "data", "report_all.json"))

    entries = []
    for p in files:
        if os.path.isfile(p):
            entries.append({"path": rel(p), "sha256": sha256_file(p),
                            "bytes": os.path.getsize(p)})

    # Merkle-style root: sha256 over the sorted "hash  path" lines
    lines = sorted(f"{e['sha256']}  {e['path']}" for e in entries)
    root = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()

    # Cloudflare witness fields from the header files
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
        "what_this_is": (
            "Tamper-evidence manifest for the Ironhack alumni-portal capture. "
            "SHA-256 over every raw response and analysis input; Merkle root below. "
            "Timestamp this file with an RFC 3161 authority to freeze it in time."
        ),
        "endpoint": "POST https://my.ironhack.com/api/alumni",
        "host": HOST,
        "n_files": len(entries),
        "merkle_root_sha256": root,
        "cloudflare_witness": {
            "cf_ray_count": len(cf_rays),
            "cf_rays": cf_rays,
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
    print(f"cf-rays      : {len(cf_rays)}  ({manifest['cloudflare_witness']['server_date_min']} .. {manifest['cloudflare_witness']['server_date_max']})")
    print(f"tls sha256   : {manifest['tls_certificate'].get('sha256_fingerprint') or manifest['tls_certificate']}")
    print(f"wrote        : provenance/manifest.json")


if __name__ == "__main__":
    main()
