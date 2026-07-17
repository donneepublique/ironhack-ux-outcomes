# How to choose a UX/UI bootcamp: read the outcome data, not the marketing — a case study with Ironhack's own numbers

**TL;DR** — Ironhack advertises that it places **~90% of job‑seeking graduates within 6 months**. I pulled its **own internal alumni directory** — every UX/UI graduate it tracks, 2,126 people across all 10 campuses — and by Ironhack's own labels, **only 18% were hired as a designer**. The largest group, **46%**, is recorded as *never placed / still searching / inactive*. For the most recent cohort with data (class of 2025), it's **8% hired, 74% not placed**. This isn't an anti‑Ironhack rant — it's a method you can use on *any* bootcamp. Full data + methodology + tamper‑evidence: [github.com/donneepublique/ironhack-ux-outcomes](https://github.com/donneepublique/ironhack-ux-outcomes).

---

## The problem with bootcamp marketing

Every bootcamp advertises a huge placement rate. The number is almost always built on two tricks:

1. **A shrunken denominator** — they only count "job‑seeking graduates," quietly dropping everyone who went inactive, back to school, didn't finish, etc.
2. **An inflated numerator** — "placed" means *any job*, including roles that have nothing to do with the field you trained for, or going back to a job you already had.

So "90% placed" can be technically true and still tell you almost nothing about your real odds of becoming a working designer.

## Why Ironhack is the rare case you can actually check

Most bootcamps never expose per‑student outcomes. Ironhack does: its alumni portal (`my.ironhack.com`) is an internal directory where **Ironhack itself records each graduate's career‑services status** (`hired_in_field`, `placement_not_successful`, `searching`, `freelance`, …). Because it's their *system of record* and not a curated marketing page, it includes the failures too. I aggregated and anonymized it (no individual is named).

**What 2,126 UX/UI graduates actually did (Ironhack's own labels):**

| Outcome | Share |
|---|---:|
| Never placed / still searching / inactive | **45.8%** |
| **Hired as a salaried designer (in‑field)** | **18.2%** |
| Employed, but NOT as a designer | 11.2% |
| Left the field (back to school / other) | 10.2% |
| Freelance / self‑employed | 6.2% |
| Did not complete / not eligible | 4.4% |
| Internship only | 4.0% |

Recreate Ironhack's own generous math (any job ÷ job‑seekers) and you still only get to **50.7%** — not 90%.

## It's getting worse every year

The headline hides a steep decline as the junior design market cooled after 2022:

- 2021 grads: **37%** hired in‑field
- 2022: 32% → 2023: **18%** (and the 2023 class has had 1.5–3 years — plenty of time)
- 2024: 12%
- **Class of 2025 (most recent): 8% hired in‑field, 74% never placed / still searching**

(2026 grads are excluded — too recent, Ironhack hasn't finished recording them.)

## Even the "success" number is generous

At least one graduate labelled `hired_in_field` was, verifiably, (a) already employed before starting the bootcamp and (b) working as a Product Manager — not a designer — at their pre‑existing employer. If the flagship "success" bucket absorbs cases like that, the true "became a designer *because of* the bootcamp" rate is below 18%.

## So — how do you choose a UX/UI bootcamp?

Use this checklist on *any* school before you spend €8,000:

1. **Ask for the in‑field hire rate, not the "placement rate."** "Placed" ≠ "working as a designer." Make them define it.
2. **Ask for the denominator.** % of *all* graduates, not just "job‑seeking" ones. The gap between the two is where the spin lives.
3. **Ask for recent cohorts.** A 2021 number is meaningless in today's market. Demand the last 2–3 graduating classes.
4. **Ask for third‑party‑audited, per‑cohort data** (CIRR standard is the gold standard). "PwC‑audited" of a hand‑picked slice isn't the same thing.
5. **Check independent sources** — subreddits, alumni on LinkedIn (are they actually designers now, or "freelance / open to work" three years later?).
6. **Treat "we don't guarantee jobs" + aspirational copy** ("pay once you get a job", "land your first role") as marketing, not evidence.
7. **Do the LinkedIn test yourself:** take 20 grads from 2 years ago. How many have a salaried design title today?

If a school can't or won't give you clear, recent, in‑field, all‑graduates numbers — that's your answer.

## Methodology & honesty

- Source: Ironhack's own alumni directory, `track=ux`, all 10 campuses, n=2,126, scraped July 2026.
- Everything is **aggregate and anonymous**; raw personal data is not published.
- These are **Ironhack's own status labels**, taken at face value. Not an allegation of fraud — a comparison between a marketing impression and the documented outcome.
- Limitations: it's a snapshot; recent cohorts skew "searching" (addressed with a mature‑cohort cut and a year‑by‑year table); it covers the UX/UI track only.
- The capture is hashed and **RFC 3161 time‑stamped**, so it can't be quietly rewritten later, and the raw data can be provided to legitimate oversight/funding bodies on request.

Full report, charts, per‑campus and per‑year breakdowns, and reproduction scripts: **[github.com/donneepublique/ironhack-ux-outcomes](https://github.com/donneepublique/ironhack-ux-outcomes)**

*I'd genuinely love for someone to run the same analysis on other bootcamps — the method is in the repo.*
