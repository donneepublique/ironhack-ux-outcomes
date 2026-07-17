#!/usr/bin/env python3
"""One outcome-distribution chart per Ironhack track -> assets/tracks/<track>.png.

Reads data_all/report_tracks.json (aggregate counts only). In-field bucket is
labelled with each track's actual role (developer, analyst, ...), not "designer".
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "assets", "tracks")
os.makedirs(OUT, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, BAR = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, RED = "#2a78d6", "#d03b3b"
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.edgecolor": GRID, "xtick.color": MUTED, "ytick.color": INK})

NAME = {"wd": "Web Development", "ux": "UX/UI Design", "da": "Data Analytics",
        "cy": "Cybersecurity", "ai": "AI Engineering", "ml": "Data Science & ML"}
ROLE = {"wd": "developer", "ux": "designer", "da": "data analyst",
        "cy": "security role", "ai": "AI engineer", "ml": "data scientist"}
# raw bucket key -> (display label, color). {role} filled per track.
BK = [
    ("Never placed / searching / inactive", "Never placed / still searching / inactive", RED),
    ("Salaried designer job (in field)", "Hired as a {role} (in-field)", BLUE),
    ("Job, but NOT as a designer", "Employed, but NOT in-field", BAR),
    ("Left the field (school / other)", "Left the field (school / other)", BAR),
    ("Freelance / self-employed", "Freelance / self-employed", BAR),
    ("Did not complete / not eligible", "Did not complete / not eligible", BAR),
    ("Internship only", "Internship only", BAR),
]


def chart(track, v):
    n = v["n"]; b = v["buckets"]; role = ROLE[track]
    rows = [(lbl.format(role=role), round(100 * b.get(key, 0) / n, 1), col) for key, lbl, col in BK]
    rows.sort(key=lambda r: -r[1])
    labels = [r[0] for r in rows]; vals = [r[1] for r in rows]; cols = [r[2] for r in rows]
    fig, ax = plt.subplots(figsize=(9.6, 0.62 * len(labels) + 1.9), dpi=200)
    y = range(len(labels))
    ax.barh(y, vals, color=cols, height=0.66, zorder=3)
    ax.set_yticks(list(y)); ax.set_yticklabels(labels, fontsize=11); ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.16)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", labelsize=9)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
    for yi, val in zip(y, vals):
        ax.text(val + max(vals) * 0.015, yi, f"{val:.1f}%", va="center", ha="left",
                fontsize=10.5, color=INK, fontweight="bold")
    fig.suptitle(f"{NAME[track]} — Ironhack alumni outcomes (n={n:,})".replace(",", " "),
                 x=0.012, y=0.985, ha="left", fontsize=15, fontweight="bold", color=INK)
    ax.set_title(f"{v['in_field_pct']}% hired as a {role} (in-field). "
                 f"{v['never_placed_pct']}% never placed or still searching.",
                 loc="left", fontsize=10.5, color=INK2, pad=12)
    fig.text(0.012, 0.012, "Source: Ironhack's own alumni directory, aggregated & anonymized. "
             "github.com/donneepublique/ironhack-ux-outcomes", ha="left", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))
    out = os.path.join(OUT, f"{track}.png")
    fig.savefig(out, bbox_inches="tight"); plt.close(fig)
    print(f"{track}: {v['in_field_pct']}% in-field -> assets/tracks/{track}.png")


def main():
    d = json.load(open(os.path.join(HERE, "data_all", "report_tracks.json")))
    for t in ["wd", "ux", "da", "cy", "ai", "ml"]:
        if t in d["tracks"]:
            chart(t, d["tracks"][t])


if __name__ == "__main__":
    main()
