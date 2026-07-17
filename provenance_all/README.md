# All-tracks capture — tamper-evidence proof (data withheld)

This folder is the **time-anchored proof** for a capture of **all six Ironhack
tracks** (UX/UI, Web Development, Data Analytics, Cybersecurity, AI Engineering,
Data Science & ML — 7,707 alumni), taken from `my.ironhack.com/api/alumni` on
2026-07-17.

The **raw data and per-track findings are intentionally withheld** for now
(`capture_all/` and `data_all/` are git-ignored). What is published here is only
the cryptographic proof:

- `manifest.json` — SHA-256 of every raw response + a Merkle root, plus the
  Cloudflare `cf-ray`/`Date` witness and the live TLS certificate fingerprint.
- `manifest.tsr` — an **RFC 3161 signed timestamp** (freetsa) over `manifest.json`.
- `freetsa_cacert.pem`, `freetsa_tsa.crt` — the authority's certs for offline verification.

Why publish the proof but not the data: this **freezes the all-tracks capture in
time** (so it is provably not fabricated after the fact, and survives any later
deletion by Ironhack) while the analysis itself is finalised. Verify with:

```bash
openssl ts -verify -data manifest.json -in manifest.tsr \
  -CAfile freetsa_cacert.pem -untrusted freetsa_tsa.crt
```

See the repository's `PROVENANCE.md` for the full threat model and honest limits.
The underlying raw data can be provided on request to legitimate funding or
oversight bodies for independent verification.
