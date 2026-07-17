#!/usr/bin/env python3
"""'Scaled up, placement collapsed' — stacked absolute counts per year, all tracks.
-> assets/scale_vs_placement.png . Reads data_all/."""
import glob
import json
import os
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyze_all import BUCKETS

HERE = os.path.dirname(__file__)
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, RED, GREY = "#2a78d6", "#d03b3b", "#c3c2b7"
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.edgecolor": GRID, "xtick.color": MUTED, "ytick.color": INK})
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]

agg = defaultdict(lambda: {"n": 0, "in": 0, "never": 0})
for f in glob.glob(os.path.join(HERE, "data_all", "alumni_*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        y = ((r.get("cohort") or {}).get("end_date") or "")[:4]
        b = BUCKETS.get((r.get("career_services") or {}).get("status") or "", "?")
        if y in YEARS:
            agg[y]["n"] += 1
            if b == "Salaried designer job (in field)":
                agg[y]["in"] += 1
            elif b == "Never placed / searching / inactive":
                agg[y]["never"] += 1

infield = [agg[y]["in"] for y in YEARS]
never = [agg[y]["never"] for y in YEARS]
other = [agg[y]["n"] - agg[y]["in"] - agg[y]["never"] for y in YEARS]
ns = [agg[y]["n"] for y in YEARS]
pct_in = [round(100 * agg[y]["in"] / agg[y]["n"]) for y in YEARS]

fig, ax = plt.subplots(figsize=(9.5, 5.6), dpi=200)
x = range(len(YEARS))
ax.bar(x, infield, 0.62, color=BLUE, zorder=3, label="Hired in-field")
ax.bar(x, other, 0.62, bottom=infield, color=GREY, zorder=3, label="Other outcome")
ax.bar(x, never, 0.62, bottom=[i + o for i, o in zip(infield, other)], color=RED, zorder=3,
       label="Never placed / searching / inactive")
ax.set_xticks(list(x)); ax.set_xticklabels(YEARS, fontsize=11)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
ax.tick_params(length=0); ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
ax.set_ylabel("Graduates (all 6 tracks)", fontsize=10, color=INK2)
ax.set_ylim(0, max(ns) * 1.15)
for xi in x:
    ax.text(xi, ns[xi] + max(ns) * 0.015, f"{ns[xi]:,}".replace(",", " "), ha="center", va="bottom",
            fontsize=9.5, color=INK, fontweight="bold")
    ax.text(xi, infield[xi] / 2, f"{pct_in[xi]}%", ha="center", va="center", fontsize=9,
            color="#fff", fontweight="bold")
ax.legend(loc="upper left", frameon=False, fontsize=10)
fig.suptitle("Ironhack scaled up ~10× — and in-field placement collapsed", x=0.012, y=0.99,
             ha="left", fontsize=15, fontweight="bold", color=INK)
ax.set_title("Graduates per year (all 6 tracks), by outcome. Blue = hired in-field; % is the in-field share.",
             loc="left", fontsize=10, color=INK2, pad=10)
fig.text(0.012, 0.005, "2024–2025 cohorts are still being populated in the directory (counts are floors). "
         "Source: Ironhack's own alumni directory, aggregated & anonymized.", ha="left", fontsize=7.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
out = os.path.join(HERE, "assets", "scale_vs_placement.png")
fig.savefig(out, bbox_inches="tight"); plt.close(fig)
print("wrote", out)
for y in YEARS:
    print(y, agg[y]["n"], "grads,", agg[y]["in"], "in-field,", agg[y]["never"], "never-placed")
