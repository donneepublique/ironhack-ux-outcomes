#!/usr/bin/env python3
"""Render the report's infographics as PNGs (matplotlib), from aggregate counts."""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)

# --- validated palette (dataviz skill, light surface) ---
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BAR = "#c3c2b7"      # neutral bar
BLUE = "#2a78d6"     # the honest / key metric
RED = "#d03b3b"      # critical
AMBER = "#fab219"    # generous / caveat

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "text.color": INK,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK2,
    "xtick.color": MUTED,
    "ytick.color": INK,
})


def hbar(fname, title, subtitle, labels, values, colors, value_fmt, note=None):
    fig, ax = plt.subplots(figsize=(9.5, 0.62 * len(labels) + 1.9), dpi=200)
    y = range(len(labels))
    ax.barh(y, values, color=colors, height=0.66, zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values) * 1.16)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=9)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for yi, v in zip(y, values):
        ax.text(v + max(values) * 0.015, yi, value_fmt(v), va="center",
                ha="left", fontsize=10.5, color=INK, fontweight="bold")
    fig.suptitle(title, x=0.012, y=0.985, ha="left", fontsize=15.5,
                 fontweight="bold", color=INK)
    ax.set_title(subtitle, loc="left", fontsize=10.5, color=INK2, pad=12)
    if note:
        fig.text(0.012, 0.012, note, ha="left", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03 if note else 0, 1, 0.94))
    out = os.path.join(ASSETS, fname)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


def grouped_years(fname, title, subtitle, years, ns, s1, s2, s1label, s2label, note):
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
    x = range(len(years))
    w = 0.4
    b1 = ax.bar([i - w / 2 for i in x], s1, w, color=BLUE, zorder=3, label=s1label)
    b2 = ax.bar([i + w / 2 for i in x], s2, w, color=RED, zorder=3, label=s2label)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{y}\n(n={n})" for y, n in zip(years, ns)], fontsize=10)
    ax.set_ylim(0, max(s1 + s2) * 1.18)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("% of that year's graduates", fontsize=9.5, color=INK2)
    for bars in (b1, b2):
        for r in bars:
            h = r.get_height()
            ax.text(r.get_x() + r.get_width() / 2, h + max(s1 + s2) * 0.012,
                    f"{h:.0f}", ha="center", va="bottom", fontsize=8.5,
                    color=INK, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=10.5)
    fig.suptitle(title, x=0.012, y=0.99, ha="left", fontsize=15.5, fontweight="bold", color=INK)
    ax.set_title(subtitle, loc="left", fontsize=10.5, color=INK2, pad=10)
    fig.text(0.012, 0.005, note, ha="left", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    out = os.path.join(ASSETS, fname)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


rep = json.load(open(os.path.join(HERE, "data", "report_all.json")))
N = rep["overall"]["n"]

# ---- Chart 1: outcome distribution ----
buckets = rep["overall"]["buckets"]
order = [
    ("Never placed / still searching / inactive", RED),
    ("Hired as a designer (in-field)", BLUE),
    ("Employed, but NOT as a designer", BAR),
    ("Left the field (school / other)", BAR),
    ("Freelance / self-employed", BAR),
    ("Did not complete / not eligible", BAR),
    ("Internship only", BAR),
]
key = {
    "Never placed / still searching / inactive": "Never placed / searching / inactive",
    "Hired as a designer (in-field)": "Salaried designer job (in field)",
    "Employed, but NOT as a designer": "Job, but NOT as a designer",
    "Left the field (school / other)": "Left the field (school / other)",
    "Freelance / self-employed": "Freelance / self-employed",
    "Did not complete / not eligible": "Did not complete / not eligible",
    "Internship only": "Internship only",
}
labels = [l for l, _ in order]
counts = [buckets[key[l]] for l in labels]
pcts = [round(100 * c / N, 1) for c in counts]
hbar("01_outcomes.png",
     f"What actually happened to {N:,} Ironhack UX/UI graduates",
     "Ironhack's own alumni-directory labels, grouped. Only ~1 in 5 was hired as a designer.",
     labels, pcts, [c for _, c in order],
     lambda v: f"{v:.1f}%  ({counts[pcts.index(v)]:,})".replace(",", " "))

# ---- Chart 2: the 90% claim deconstructed ----
hbar("02_claim_vs_reality.png",
     "The “~90% placed” headline, deconstructed",
     "Same alumni data, three definitions. “Placement” is not “working as a designer.”",
     ["Ironhack's claim:\n“~90% of job-seekers placed”",
      "Generous re-do on the data:\nANY job ÷ job-seekers",
      "Honest reading:\nhired as a designer ÷ all grads"],
     [90.0, rep["overall"]["ironhack_style_placed_pct"], rep["overall"]["in_field_pct_of_all"]],
     [BAR, AMBER, BLUE],
     lambda v: f"{v:.1f}%",
     note="Ironhack figure: PwC-audited outcomes report (job-seeking grads, within 6 months).")

# ---- Chart 3: per-campus in-field rate ----
pc = rep["per_campus"]
name = {"rmt": "Remote", "mad": "Madrid", "ber": "Berlin", "par": "Paris",
        "bcn": "Barcelona", "lis": "Lisbon", "sao": "São Paulo",
        "mex": "Mexico City", "mia": "Miami", "ams": "Amsterdam"}
items = sorted(pc.items(), key=lambda kv: -kv[1]["in_field_pct"])
labels = [f"{name.get(c, c)}  (n={d['n']})" for c, d in items]
vals = [d["in_field_pct"] for c, d in items]
cols = [RED if c == "rmt" else BAR for c, d in items]
hbar("03_by_campus.png",
     "Hired as a designer, by campus",
     "Even the best campus tops out near 28%. The heavily-marketed Remote track (largest cohort) is worst.",
     labels, vals, cols, lambda v: f"{v:.1f}%",
     note="Amsterdam n=8 — too small to read into.")

# ---- Chart 4: outcomes by graduation year ----
py = rep["per_year"]
years = [y for y in ["2020", "2021", "2022", "2023", "2024", "2025", "2026"] if y in py]
ns = [py[y]["n"] for y in years]
infield = [py[y]["in_field_pct"] for y in years]
never = [py[y]["never_placed_pct"] for y in years]
grouped_years(
    "04_by_year.png",
    "Outcomes are getting worse, cohort by cohort",
    "Share hired as a designer vs. never placed / searching, by graduation year.",
    years, ns, infield, never,
    "Hired as a designer (in-field)", "Never placed / searching / inactive",
    "2025–2026 cohorts are recency-inflated (little time to land a role). "
    "Placeholder-dated (1987) and n<20 years excluded.")

print("done")
