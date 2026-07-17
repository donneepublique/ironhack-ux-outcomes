# Ironhack bootcamp outcomes: scaled up ~10×, placement collapsed — from their own data

🌍 **English** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md)

**What actually happens after an Ironhack bootcamp — across all 6 tracks, cohort by cohort — built from Ironhack's own internal alumni directory.**

> This is a data‑journalism exercise on Ironhack's **own system of record**: the alumni‑portal directory (`my.ironhack.com`) where Ironhack itself logs each graduate's career‑services outcome (accessed with an alumni login). Because it's the internal record and not a marketing page, it includes the failures too. Everything here is **aggregate and anonymous** — no individual is named, no raw personal data is republished. It's **not** an allegation of fraud. The story isn't one headline number; it's a **trend**: as Ironhack scaled to its largest cohorts ever and launched new premium tracks, the share of graduates actually hired *in‑field* collapsed.

## Contents

- [The big picture](#the-big-picture) — all 6 tracks, scaled up while placement fell
- **Per bootcamp:**
  - [Web Development](#web-development)
  - [UX/UI Design](#uxui-design)
  - [Data Analytics](#data-analytics)
  - [Cybersecurity](#cybersecurity)
  - [AI Engineering](#ai-engineering)
  - [Data Science & ML](#data-science--ml)
- [How the "~90% placed" claim fits in](#how-the-90-placed-claim-fits-in)
- [Method](#method) · [Limitations](#limitations) · [Provenance & tamper‑evidence](#provenance--tamper-evidence) · [Ethics & privacy](#ethics--privacy)

---

## The big picture

Ironhack grew from a few hundred graduates a year to **thousands** — and over the same period, the share actually hired *in‑field* fell from ~35% to ~11%.

![Graduates per year across all 6 Ironhack tracks, by outcome: the cohort grows ~10× from 235 (2020) to 2,552 (2023) while the hired-in-field share falls from 35% to 12% and the never-placed share balloons.](assets/scale_vs_placement.png)

| Graduation year | Graduates (all 6 tracks) | Hired in‑field | Never placed / searching |
|---|---:|---:|---:|
| 2020 | 235 | 17% | 14% |
| 2021 | 295 | **35%** | 19% |
| 2022 | 1,345 | 33% | 28% |
| 2023 | 2,552 | 21% | 41% |
| 2024 | 1,543 | 16% | 51% |
| 2025 | 859 | **11%** | 64% |

Two things happened at once, and together they're the story:

- **Scale.** Annual graduating cohorts grew **~10×** between 2020 and the 2022–2023 peak. These are the biggest classes in Ironhack's history.
- **Collapse.** In‑field placement fell every year after the 2021 boom — from 35% to ~11%.

So the largest cohorts Ironhack ever enrolled are also the ones with the worst outcomes. In absolute terms the **2023 cohort alone has 1,066 graduates recorded as never placed / still searching**, versus 35 in 2020. *(2024–2025 counts are floors — the directory is still being populated for recent years — which makes the falling placement %, not the headcount, the reliable signal.)*

Across **~7,700 graduates in all 6 tracks**, this pattern holds everywhere. Per track:

## Web Development

![Web Development outcomes by graduation year: hired-as-a-developer falls from 36% (2021) to 14% (2025) while never-placed rises to 57%.](assets/tracks/wd_by_year.png)

**2,832 grads.** Hired as a developer in‑field, by cohort: 2021 **36%** → 2022 32% → 2023 21% → 2024 15% → **2025 14%**, with **44–57%** of the last two cohorts never placed / still searching.

## UX/UI Design

![UX/UI outcomes by graduation year: hired-as-a-designer falls from 37% (2021) to 8% (2025) while never-placed rises to 74%.](assets/tracks/ux_by_year.png)

**2,126 grads.** Hired as a designer in‑field: 2021 **37%** → 2023 18% → 2024 12% → **2025 8%**, with **63–74%** of recent grads never placed. It's also the track with the deepest per‑campus and per‑year breakdown — the remote campus (largest cohort) is the weakest.

## Data Analytics

![Data Analytics outcomes by graduation year: hired-as-an-analyst falls from 40% (2022) to 13% (2025), never-placed rises to 65%.](assets/tracks/da_by_year.png)

**1,954 grads.** Ironhack's *strongest* track — and still collapsing: 2022 **40%** → 2023 28% → 2024 20% → **2025 13%** (65% never placed).

## Cybersecurity

![Cybersecurity outcomes by graduation year: hired-in-field falls from 35% (2022) to 10% (2025), never-placed 72%.](assets/tracks/cy_by_year.png)

**505 grads.** 2022 35% → 2023 16% → 2024 14% → **2025 10%** hired in‑field, with **57–72%** of recent grads never placed.

## AI Engineering

![AI Engineering outcomes by graduation year: 2025 cohort 14% hired in-field, 60% never placed.](assets/tracks/ai_by_year.png)

**139 grads** (newest, priciest track). **2025 cohort: 14% hired in‑field, 60% never placed** (n=76). Launched right as the market turned — and it shows.

## Data Science & ML

![Data Science & ML outcomes by graduation year: 2025 cohort 13% hired in-field, 52% never placed.](assets/tracks/ml_by_year.png)

**151 grads.** **2025 cohort: 13% hired in‑field, 52% never placed** (n=75) — the lowest in‑field rate of any track.

---

## How the "~90% placed" claim fits in

Around **2019**, Ironhack's *first* outcomes report (presented as PwC‑audited) advertised *"we placed 90% of job‑seeking graduates within 6 months"* (76% / 89% at 90 / 180 days). That number leaned on two moves: a **narrow denominator** (only "job‑seeking" grads) and a **broad numerator** ("placed" = *any* job, including out‑of‑field or returning to a former employer). Recreate it generously on the full data and you reach ~**51%**, not 90%; count only *hired as a designer ÷ all graduates* and it's **18%** (UX/UI, all‑time) — and, as shown above, far lower for recent cohorts. This ~6‑year‑old figure — pre‑dating the market downturn — is **no longer displayed** (the page redirects; archived 2022 on the [Wayback Machine](http://web.archive.org/web/20220126230803/https://www.ironhack.com/en/news/ironhack-student-outcomes-report-audited-by-pwc)); today's marketing is softer ("pay once you get a job", "land your first role"). It isn't the point of this report — the **trend and scale** are.

## Method

- **Source:** `POST my.ironhack.com/api/alumni` — Ironhack's internal alumni‑portal directory (accessed with an alumni login), its system of record for each graduate's `career_services.status`. Not a public marketing page, so it reports the real outcome spread, failures included.
- **Scope:** all 6 tracks (ux, wd, da, cy, ai, ml), every campus — **≈7,700 graduates**.
- **Ground truth:** Ironhack's own status labels, grouped into plain‑language buckets. "Hired in‑field" = `hired_in_field`; "never placed / searching" groups `placement_not_successful`, `searching`, `inactive`, `intervention_*`, `deferred_*`, `pending`. Full mapping below.
- **By year:** cohorts are split by graduation year so recent classes aren't hidden inside boom‑era averages.
- **Privacy:** published outputs are counts only.

<details><summary>Full status → bucket mapping</summary>

| Bucket | Raw `career_services.status` values |
|---|---|
| Hired in‑field | `hired_in_field` |
| Employed, not in‑field | `hired_out_of_field`, `back_to_job`, `ironhack_employee` |
| Freelance / self‑employed | `freelance`, `entrepreneur` |
| Internship only | `internship`, `short_term` |
| Never placed / searching / inactive | `placement_not_successful`, `searching`, `inactive`, `intervention_careers`, `intervention_careers_not_success`, `intervention_education`, `intervention_education_not_success`, `deferred_more_than_45d`, `deferred_more_than_45d_sc`, `deferred_less_than_45d`, `pending` |
| Left the field | `back_to_university`, `personal_development`, `withdrew` |
| Did not complete / not eligible | `not_graduated_cs`, `not_eligible` |

</details>

## Limitations

- **Ironhack's labels**, taken at face value; we don't know their exact internal definition of `placement_not_successful` or how often `searching`/`inactive` are refreshed.
- **Snapshot** (July 2026); recent cohorts (2024–2026) are still being populated, so their **headcounts are floors** — the reliable signal is the falling placement **%**, and the mature cohorts (2021–2023, 1.5–5 years out) already show the collapse.
- A handful of records carry a placeholder date (`1987`, Madrid) — excluded from the year charts, kept in totals.

## Provenance & tamper‑evidence

The capture is hashed into a Merkle root and **time‑stamped by an independent RFC 3161 authority**, so it can't be quietly rewritten and survives any later deletion by Ironhack. The raw data can be provided **on request to legitimate funding or oversight bodies** for verification. Threat model + verification steps: [PROVENANCE.md](PROVENANCE.md).

## Ethics & privacy

- Source is Ironhack's **internal alumni directory**, accessed with an alumni account — their system of record, not a public page.
- **Nothing identifying is republished** — aggregate, anonymous counts only. Raw per‑person data (names, LinkedIn, photos) is git‑ignored and never leaves the analyst's machine.
- Ironhack's **own labels**, taken at face value — a comparison between marketing and documented outcomes, not an allegation of fraud.

## License

Underlying data is Ironhack's; analysis, code and charts are released under the MIT License.
