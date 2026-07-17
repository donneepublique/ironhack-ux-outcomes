#!/usr/bin/env python3
"""Per-track, per-YEAR outcome charts (not all-time) -> assets/tracks/<track>_by_year.png.

Grouped bars: hired in-field vs never-placed, by graduation year. Reads data_all/.
Also prints the per-track-per-year table (for the Reddit comments).
"""
import glob
import json
import os
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyze_all import BUCKETS

HERE = os.path.dirname(__file__)
DATADIR = os.path.join(HERE, "data_all")
OUT = os.path.join(HERE, "assets", "tracks")
os.makedirs(OUT, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, RED = "#2a78d6", "#d03b3b"
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.edgecolor": GRID, "xtick.color": MUTED, "ytick.color": INK})

NAME = {"wd": "Web Development", "ux": "UX/UI Design", "da": "Data Analytics",
        "cy": "Cybersecurity", "ai": "AI Engineering", "ml": "Data Science & ML"}
ROLE = {"wd": "developer", "ux": "designer", "da": "data analyst",
        "cy": "security role", "ai": "AI engineer", "ml": "data scientist"}
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
MIN_N = 15  # skip year-cells too small to read


def load_years(track):
    by_year = defaultdict(list)
    for line in open(os.path.join(DATADIR, f"alumni_{track}.jsonl")):
        r = json.loads(line)
        y = ((r.get("cohort") or {}).get("end_date") or "")[:4]
        st = (r.get("career_services") or {}).get("status") or ""
        by_year[y].append(st)
    out = {}
    for y in YEARS:
        sts = by_year.get(y, [])
        if len(sts) < MIN_N:
            continue
        bc = Counter(BUCKETS.get(s, "?") for s in sts)
        n = len(sts)
        out[y] = {"n": n,
                  "in": round(100 * bc.get("Salaried designer job (in field)", 0) / n, 1),
                  "never": round(100 * bc.get("Never placed / searching / inactive", 0) / n, 1)}
    return out


def chart(track, per_year):
    yrs = list(per_year.keys())
    ns = [per_year[y]["n"] for y in yrs]
    infield = [per_year[y]["in"] for y in yrs]
    never = [per_year[y]["never"] for y in yrs]
    fig, ax = plt.subplots(figsize=(max(6.5, 1.15 * len(yrs) + 2.5), 5.2), dpi=200)
    x = range(len(yrs)); w = 0.4
    ax.bar([i - w / 2 for i in x], infield, w, color=BLUE, zorder=3, label=f"Hired as a {ROLE[track]} (in-field)")
    ax.bar([i + w / 2 for i in x], never, w, color=RED, zorder=3, label="Never placed / searching / inactive")
    ax.set_xticks(list(x)); ax.set_xticklabels([f"{y}\n(n={n})" for y, n in zip(yrs, ns)], fontsize=10)
    ax.set_ylim(0, max(infield + never + [1]) * 1.18)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0); ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
    ax.set_ylabel("% of that year's graduates", fontsize=9.5, color=INK2)
    for xi in x:
        for off, arr in [(-w / 2, infield), (w / 2, never)]:
            ax.text(xi + off, arr[xi] + max(infield + never + [1]) * 0.012, f"{arr[xi]:.0f}",
                    ha="center", va="bottom", fontsize=8.5, color=INK, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    fig.suptitle(f"{NAME[track]} — outcomes by graduation year (Ironhack's own data)",
                 x=0.012, y=0.99, ha="left", fontsize=14, fontweight="bold", color=INK)
    ax.set_title("Hired in-field vs. never placed, per cohort. All-time averages hide the recent decline.",
                 loc="left", fontsize=9.5, color=INK2, pad=10)
    fig.text(0.012, 0.005, "Source: Ironhack's own alumni directory, aggregated & anonymized. "
             "github.com/donneepublique/ironhack-ux-outcomes", ha="left", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(os.path.join(OUT, f"{track}_by_year.png"), bbox_inches="tight"); plt.close(fig)


def main():
    print(f"{'track':16s} " + " ".join(f"{y:>11s}" for y in YEARS))
    result = {}
    for t in ["wd", "ux", "da", "cy", "ai", "ml"]:
        py = load_years(t)
        result[t] = py
        cells = []
        for y in YEARS:
            cells.append(f"{py[y]['in']:.0f}/{py[y]['never']:.0f}%({py[y]['n']})" if y in py else "—")
        print(f"{NAME[t]:16s} " + " ".join(f"{c:>11s}" for c in cells))
        chart(t, py)
    json.dump(result, open(os.path.join(DATADIR, "report_tracks_by_year.json"), "w"), indent=2)
    print("\n(cells = in-field%/never-placed%(n))  charts -> assets/tracks/<track>_by_year.png")


if __name__ == "__main__":
    main()
