# Provenance & tamper‑evidence

**Question this answers:** *how do we show we really fetched this from Ironhack, that the numbers weren't altered, and that our proof survives even if Ironhack later deletes or edits the directory?*

Short version: we **froze the data in time** at capture. Once the capture is hashed and the hash is signed by an independent timestamp authority, **nothing Ironhack does afterward — deleting records, editing statuses, taking the directory down — can change what we can prove the endpoint returned on the capture date.** Our proof does not depend on their servers staying up.

Be clear‑eyed about the limits, too: this gives strong **integrity** and **freshness** guarantees, and strong practical evidence of **origin**, but not a cryptographic *transferable* proof of origin. That last one needs TLSNotary‑style attestation (see below).

---

## What we captured

`capture.py` saves, for every page of every campus:

- **`*.body.json`** — the **verbatim** response bytes from `POST https://my.ironhack.com/api/alumni` (not re‑serialized; the exact bytes the server sent).
- **`*.headers.json`** — the response metadata: HTTP status, server `Date`, Cloudflare **`cf-ray`**, `etag`, `server`, and the exact request (URL + body).

`provenance.py` then builds **`provenance/manifest.json`**:

- **SHA‑256** of every raw body, every header file, and every analysis input (`data/alumni_ux_*.jsonl/.csv`, `data/report_all.json`);
- a **Merkle‑style root** = SHA‑256 over the sorted `hash  path` lines (one hash that commits to the whole set);
- the **Cloudflare witness** (all `cf-ray` IDs + the server `Date` range of the capture);
- the **live TLS certificate** fingerprint of `my.ironhack.com` at capture time.

Finally the manifest is **timestamped with an RFC 3161 authority** (freetsa.org): `manifest.tsq` (request) → `manifest.tsr` (the authority's signed token), verifiable offline against the authority's CA certs in `provenance/`.

## What each artifact proves — and against which attack

| Artifact | Defends against | Strength |
|---|---|---|
| SHA‑256 of raw bodies + Merkle root | *"you edited the data after downloading it"* | **Strong** — any 1‑byte change breaks the root |
| RFC 3161 signed timestamp over the manifest | *"you fabricated / back‑dated this after Ironhack changed things"* | **Strong** — a trusted authority signed "this exact manifest existed by `<date>`"; independent of Ironhack |
| Verbatim capture retained offline | *"Ironhack deleted it, so you can't show what it said"* | **Strong** — deletion on their side doesn't touch our timestamped copy |
| Cloudflare `cf-ray` + server `Date` + TLS cert | *"this didn't come from my.ironhack.com at all"* | **Corroborating** — consistent with a real Cloudflare‑fronted response, but client‑observed, so not by itself unforgeable |
| Reproducibility (any alumni re‑runs and gets 886 / 2 126 …) | *"your totals are wrong"* | **Medium** — strong while the endpoint is up; **evaporates if Ironhack deletes it**, which is exactly why we timestamp now |

## The "Ironhack deletes it after we publish" scenario

This is the main threat and the reason this package exists. The defense is **sequencing**:

1. **Capture + hash + timestamp happen before/at publication.** The RFC 3161 token binds our exact bytes to a date. That token stays valid forever and needs nothing from Ironhack.
2. **We keep the verbatim capture** (`capture/*.body.json`) archived offline (it holds personal data, so it is *not* published — see below). If ever challenged, those bytes can be disclosed to a journalist, auditor, or regulator and re‑hashed; they must match the timestamped manifest.
3. **The published, aggregate `report_all.json` is itself in the manifest** — so the exact numbers behind this report are frozen and cannot be quietly "corrected" later, by us or anyone.

So even if the directory goes dark the day after publication, the claim "on `<capture date>`, `my.ironhack.com/api/alumni` returned data showing 18% hired in‑field across 2,126 UX/UI alumni" remains provably unaltered.

## What this does NOT prove (honesty section)

- **Transferable proof of origin.** HTTPS authenticates the server *to us* but leaves no signature a third party can check later; in principle a determined actor could fabricate a body + plausible headers. The `cf-ray`/cert are corroboration, not cryptographic origin proof.
- **The fix, if you need it:** a **TLSNotary / zkTLS** attestation (e.g. TLSNotary, Reclaim, Opacity) has an independent notary co‑sign the TLS session, yielding a proof that *this response came from `my.ironhack.com`* — verifiable by anyone, forever, with no trust in us and no dependence on the endpoint. It is heavier to run (and the login‑gated endpoint adds friction), so it is offered as an upgrade rather than the default here.
- **Decentralized timestamp upzip:** RFC 3161 trusts one authority. For a censorship‑resistant anchor, also stamp the same Merkle root with **OpenTimestamps** (Bitcoin). One command (`ots stamp provenance/manifest.json`) if the `ots` client is installed.

## Privacy

The raw capture contains personal data (names, LinkedIn URLs, photos), so **`capture/*.body.json` is git‑ignored and never published** — only their **hashes** appear in the (public) manifest. The header files (`*.headers.json`) carry no personal data and are published as part of the witness.

## Verify it yourself

```bash
# 1. Recompute the Merkle root and compare to manifest.json:
python3 provenance.py
#    -> "merkle root : <hex>" must equal manifest.json .merkle_root_sha256

# 2. Verify the signed timestamp binds THIS manifest to a date, offline:
openssl ts -verify -data provenance/manifest.json \
  -in provenance/manifest.tsr \
  -CAfile provenance/freetsa_cacert.pem \
  -untrusted provenance/freetsa_tsa.crt
#    -> "Verification: OK"

# 3. Read the authority's timestamp:
openssl ts -reply -in provenance/manifest.tsr -text | grep -iA1 "Time stamp"
```
