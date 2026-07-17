# Ironhack UX/UI outcomes — a look at the numbers Ironhack itself publishes

Ironhack markets its UX/UI bootcamp with placement statistics ("~90% of job‑seeking
graduates placed within 6 months"). This repository checks that promise against
**Ironhack's own public alumni directory** — 2,126 UX/UI graduates across all 10
campuses — and finds that **only ~18% are recorded as hired into a salaried design
role**, while the largest single group (~46%) is labelled *placement not successful,
still searching, or inactive*.

**→ Read the full write‑up: [REPORT.md](REPORT.md)**

![Outcomes](assets/01_outcomes.png)

## What's in here

| File | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | The full analysis, charts, methodology, and limitations |
| `scrape.py` | Collects the public alumni directory into local JSONL + CSV |
| `analyze.py` | Single‑campus aggregate stats |
| `analyze_all.py` | Combined analysis across all campuses → `data/report_all.json` |
| `make_charts.py` | Renders the infographics in `assets/` |
| `data/report_all.json` | The aggregate, **anonymous** result set (counts only) |
| `assets/*.png` | The charts |

## Reproduce

```bash
# 1. Get a fresh x-csrf-token from the Network tab of the alumni page while logged in.
export IRONHACK_CSRF="<token>"

# 2. Scrape every campus (ux track).
for c in rmt par mad bcn ber mia lis ams sao mex; do
  python3 scrape.py --track ux --campus "$c"
done

# 3. Aggregate + chart.
python3 analyze_all.py
python3 make_charts.py
```

## Ethics & privacy

- The source is data Ironhack **publishes itself** as a marketing showcase.
- All published outputs are **aggregate and anonymous**. The raw per‑person data
  (names, LinkedIn URLs, photos) is git‑ignored and never leaves the analyst's machine.
- Status labels (`hired_in_field`, `placement_not_successful`, …) are **Ironhack's
  own**, taken at face value. This is not an allegation of fraud — it is a comparison
  between a marketing impression and the typical documented outcome. See the
  *Limitations* section of the report.

## License

Data is Ironhack's; analysis and code here are released under the MIT License.
