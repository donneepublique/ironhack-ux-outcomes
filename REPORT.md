# Does an Ironhack UX/UI bootcamp make you a "high‑paid UX designer"? A look at Ironhack's own alumni data

**TL;DR** — Using the data Ironhack itself publishes about its alumni (2,126 UX/UI graduates across all 10 campuses), **only 18% are recorded as hired into a salaried design role.** The single largest group — **46%** — is labelled *placement not successful, still searching, or inactive.* Ironhack's headline "~90% placed" is not wrong so much as narrow: it counts only "job‑seeking" graduates and treats **any** job (including non‑design roles and returning to a former employer) as a "placement." Becoming a working designer is the exception here, not the rule.

> This is a data‑journalism exercise built entirely on Ironhack's **own** public numbers. It is aggregate and anonymous: no individual graduate is named. It does not allege fraud — it shows the distance between a marketing impression and the typical documented outcome.

---

## What Ironhack promises

Ironhack's marketing and its PwC‑audited outcomes reporting lead with placement:

- **"We placed 90% of job‑seeking graduates within 6 months"** (PwC‑audited outcomes report).
- **76% placed within 90 days** and **89% within 180 days** of graduating, across a reported cohort of 829 graduates (322 of them UX/UI).
- A **96% graduation rate**.
- Salary messaging pointing at UX/UI pay (Ironhack's own salary blog cites averages such as **€25–35k in Spain**, **€42k in Germany**; US outcomes materials have cited roughly **$65k** starting).

Two words do a lot of work in those claims: **"job‑seeking"** (the denominator) and **"placed"** (which is never defined as *in‑field*). The alumni directory lets us see what those words hide.

## Method

- **Source:** `my.ironhack.com/api/alumni` — the public alumni directory Ironhack uses as a marketing showcase. Each record carries Ironhack's own `career_services.status` label (e.g. `hired_in_field`, `placement_not_successful`, `searching`, `freelance`).
- **Scope:** every UX/UI graduate the directory exposes, across all 10 campuses — **n = 2,126**.
- **Ground truth:** we take Ironhack's own status labels at face value and group them into plain‑language buckets. We invent nothing.
- **Recency control:** graduates from the last 12 months are naturally still "searching," so we also report **mature cohorts** (graduated ≥ 12 months ago, n = 1,999) separately.
- **Privacy:** all outputs are counts. Names, photos, and LinkedIn URLs stayed on the analyst's machine and are excluded from this repository.

## What actually happened

Grouping Ironhack's own labels for all 2,126 UX/UI graduates:

| Outcome (Ironhack's own labels, grouped) | Count | Share |
|---|---:|---:|
| Never placed / still searching / inactive | 969 | **45.6%** |
| **Hired into a salaried design role (in‑field)** | **386** | **18.2%** |
| Employed, but **not** as a designer | 238 | 11.2% |
| Left the field (back to school / other) | 217 | 10.2% |
| Freelance / self‑employed | 131 | 6.2% |
| Did not complete / not eligible | 94 | 4.4% |
| Internship only | 86 | 4.0% |
| Other / unknown | 5 | 0.2% |

![What actually happened to 2,126 Ironhack UX/UI graduates: only 18.2% were hired as a designer in‑field, while 45.6% were never placed, still searching, or inactive.](assets/01_outcomes.png)

The most common single raw label is `placement_not_successful` — **584 people, more than a quarter of everyone.** More graduates went **back to a previous (non‑design) job** (138) or **back to university** (120) than the marketing would suggest.

## How the "~90% placed" headline is manufactured

We can reconstruct Ironhack's generous framing from the same data:

1. **Shrink the denominator.** Drop everyone not "job‑seeking" — inactive, back‑to‑school, didn't‑complete, personal development, withdrew. That removes ~470 people (2,126 → 1,660).
2. **Widen the numerator.** Count **any** employment as a "placement" — in‑field, out‑of‑field, freelance, entrepreneur, internship, or returning to a former employer.

Even doing **both**, the best we reach is:

| Metric | Result |
|---|---:|
| Ironhack‑style "placed" (any job ÷ job‑seekers), all cohorts | **50.7%** |
| Same, mature cohorts only | 53.7% |
| **Honest headline: hired as a designer ÷ all graduates** | **18.2%** |

![The "~90% placed" headline deconstructed: Ironhack's claim ~90%, a generous any-job-over-job-seekers redo of the same data 50.7%, and the honest hired-as-a-designer-over-all-graduates reading 18.2%.](assets/02_claim_vs_reality.png)

So even bending the definitions as far as they'll go, this population lands around **50%, not 90%.** The remaining gap is what "PwC‑audited" quietly absorbs: a specific, time‑boxed, self‑reported reporting cohort — not the full body of alumni Ironhack tracks and displays.

The crucial point for a prospective student: **"placement" ≠ "working as a designer."** Strip out the non‑design jobs and the "still looking," and fewer than **1 in 5** ended up where the brochure implies.

## Even the "success" bucket is inflated

The 18% "hired in‑field" figure is itself an *over*count. In at least one case the authors can personally verify, a graduate labelled `hired_in_field` was, in reality:

- **already employed before enrolling** — the role predates the bootcamp entirely, and
- **working as a Product Manager, not a designer**, at a **pre‑existing employer**.

Ironhack still books that person as a UX/UI "designer hired in field." If the flagship success label absorbs people who were already employed, in a different role, before they started, then the true "became a working designer *because of* Ironhack" rate sits **below** the 18% headline.

## Recency doesn't rescue it

Limiting to graduates who finished **≥ 12 months ago** (they've had a full year‑plus to land a role):

- Hired in‑field: **19.2%** (383 / 1,999)
- Never placed / searching / inactive: still ~45%

The picture barely moves. This isn't a "give them time" artefact.

## The "freelance" question

A common suspicion is that "freelance UX designer" is often a polite label for *couldn't find a salaried role.* In this data, freelance is a **small** group — **89 people, 4.2%** — so it is **not** the main story. But it is strikingly **long‑tenured**: the median freelancer graduated **40 months** ago, and **88 of 89** have been freelance for **24+ months.** That is consistent with (though not proof of) freelancing being a durable destination rather than a short bridge to employment.

## Not all campuses are equal

The in‑field hire rate varies sharply by campus — and the **remote** program, which is also the **largest** (886 graduates, 42% of the dataset), is the **worst**:

| Campus | n | Hired in‑field | Never placed / searching |
|---|---:|---:|---:|
| Remote (rmt) | 886 | **14.3%** | 59.1% |
| Berlin | 286 | 15.0% | 55.6% |
| Miami | 41 | 12.2% | 36.6% |
| Paris | 223 | 19.3% | 42.2% |
| Mexico City | 42 | 19.0% | 26.2% |
| Madrid | 299 | 23.1% | 20.1% |
| Lisbon | 104 | 24.0% | 22.1% |
| São Paulo | 43 | 25.6% | 34.9% |
| Barcelona | 194 | 27.8% | 35.1% |

![Hired-as-a-designer rate by campus: Barcelona highest at 27.8%, down to Miami at 12.2%; the Remote track (largest cohort, n=886) is among the worst at 14.3%.](assets/03_by_campus.png)

Even the **best** campus (Barcelona) tops out at ~28% hired in‑field. The heavily‑marketed remote option performs worst.

## Limitations (read these)

- **Ironhack's labels, not ours.** We trust `career_services.status`. We don't know Ironhack's exact internal definition of `placement_not_successful` or how aggressively `searching`/`inactive` are refreshed.
- **Snapshot in time** (scraped July 2026). Recent graduates skew "searching"; the mature‑cohort cut addresses this.
- **Directory ≠ census.** The directory may not contain 100% of graduates. Notably, it *does* include failures and drop‑outs, so it is not a cherry‑picked success reel — if anything it undercounts the worst outcomes (people who vanish entirely).
- **No salary data.** These records show employment *status*, not pay. We cannot verify "high‑paid." But if only ~18% are employed as designers at all, the "high‑paid designer" promise is moot for the other ~82%.
- **UX/UI track only.** Other tracks (web dev, data) are not covered here.

## Bottom line

Ironhack's UX/UI marketing invites you to picture yourself as a well‑paid working designer. Ironhack's **own** alumni data says that outcome — a salaried, in‑field design job — is what happened to **fewer than 1 in 5** graduates, while the plurality are recorded as never placed, still searching, or inactive. The "~90% placed" statistic is real only under a narrow definition of who counts and a broad definition of what "placed" means. Prospective students should read "placement rate" as "got *a* job (any job)," not "became a designer," and weight the ~18% in‑field figure accordingly.

## Sources

- Ironhack, *Student outcomes report (PwC‑audited)* — <https://www.ironhack.com/en/news/ironhack-student-outcomes-report-audited-by-pwc>
- "We placed 90% of job‑seeking graduates within 6 months" — <https://www.linkedin.com/pulse/we-placed-90-job-seeking-graduates-within-6-months-take-alvaro-rojas/>
- CareerKarma, *Ironhack career services & outcomes review* (76%/90d, 89%/180d, 829 grads, PwC audit) — <https://careerkarma.com/blog/ironhack-career-services-and-outcomes-review/>
- Ironhack, *Salary Talk: what are UX/UI designers earning?* — <https://www.ironhack.com/us/blog/salary-talk-what-are-ux-ui-designers-earning>
- Primary data: `my.ironhack.com/api/alumni` (public alumni directory), scraped July 2026. Reproduction scripts in this repository.
