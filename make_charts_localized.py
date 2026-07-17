#!/usr/bin/env python3
"""Localised copies of the scale chart + the 6 by-year track charts -> assets/<lang>/.
Reads data_all/. Run: python3 make_charts_localized.py"""
import glob
import json
import os
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyze_all import BUCKETS

HERE = os.path.dirname(__file__)
SURFACE, INK, INK2, MUTED, GRID, GREY = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, RED = "#2a78d6", "#d03b3b"
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.edgecolor": GRID, "xtick.color": MUTED, "ytick.color": INK})
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]
BYEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
TRACKS = ["wd", "ux", "da", "cy", "ai", "ml"]
MIN_N = 15

STR = {
 "fr": {
  "scale_t": "Ironhack a grossi ×10 — et l'insertion dans le domaine s'est effondrée",
  "scale_s": "Diplômés par an (6 formations), par résultat. Bleu = recruté dans le domaine ; le % est la part recrutée.",
  "scale_y": "Diplômés (6 formations)", "leg_in": "Recruté dans le domaine", "leg_other": "Autre issue",
  "leg_never": "Jamais placé / en recherche / inactif",
  "scale_f": "Les promotions 2024-2025 se remplissent encore (effectifs = planchers). Source : répertoire alumni interne d'Ironhack, agrégé & anonymisé.",
  "by_t": "{name} — résultats par année de diplôme (données propres d'Ironhack)",
  "by_s": "Recruté dans le domaine vs. jamais placé, par promotion. Les moyennes all-time masquent la chute récente.",
  "by_in": "Recruté comme {role} (dans le domaine)", "by_never": "Jamais placé / en recherche / inactif",
  "by_y": "% des diplômés de l'année",
  "by_f": "Source : répertoire alumni interne d'Ironhack, agrégé & anonymisé. github.com/donneepublique/ironhack-ux-outcomes",
  "name": {"wd": "Développement web", "ux": "UX/UI Design", "da": "Data Analytics", "cy": "Cybersécurité", "ai": "AI Engineering", "ml": "Data Science & ML"},
  "role": {"wd": "développeur", "ux": "designer", "da": "analyste de données", "cy": "poste en cybersécurité", "ai": "ingénieur IA", "ml": "data scientist"},
 },
 "de": {
  "scale_t": "Ironhack wuchs ~10× — und die Fachvermittlung brach ein",
  "scale_s": "Absolventen pro Jahr (6 Tracks), nach Ergebnis. Blau = im Fachgebiet; % ist der Fachanteil.",
  "scale_y": "Absolventen (6 Tracks)", "leg_in": "Im Fachgebiet eingestellt", "leg_other": "Anderes Ergebnis",
  "leg_never": "Nie vermittelt / auf Suche / inaktiv",
  "scale_f": "Kohorten 2024-2025 werden noch befüllt (Zahlen = Untergrenzen). Quelle: Ironhacks internes Alumni-Verzeichnis, aggregiert & anonymisiert.",
  "by_t": "{name} — Ergebnisse nach Abschlussjahr (Ironhacks eigene Daten)",
  "by_s": "Im Fachgebiet vs. nie vermittelt, je Kohorte. Gesamtdurchschnitte verbergen den jüngsten Einbruch.",
  "by_in": "Als {role} eingestellt (im Fachgebiet)", "by_never": "Nie vermittelt / auf Suche / inaktiv",
  "by_y": "% der Absolventen des Jahres",
  "by_f": "Quelle: Ironhacks internes Alumni-Verzeichnis, aggregiert & anonymisiert. github.com/donneepublique/ironhack-ux-outcomes",
  "name": {"wd": "Webentwicklung", "ux": "UX/UI Design", "da": "Data Analytics", "cy": "Cybersecurity", "ai": "AI Engineering", "ml": "Data Science & ML"},
  "role": {"wd": "Entwickler", "ux": "Designer", "da": "Datenanalyst", "cy": "Sicherheitsrolle", "ai": "KI-Ingenieur", "ml": "Data Scientist"},
 },
 "pt": {
  "scale_t": "A Ironhack cresceu ~10× — e a colocação na área entrou em colapso",
  "scale_s": "Diplomados por ano (6 formações), por resultado. Azul = contratado na área; a % é a fração na área.",
  "scale_y": "Diplomados (6 formações)", "leg_in": "Contratado na área", "leg_other": "Outro resultado",
  "leg_never": "Nunca colocado / à procura / inativo",
  "scale_f": "As coortes de 2024-2025 ainda estão a ser preenchidas (contagens = pisos). Fonte: diretório interno de alumni da Ironhack, agregado & anónimo.",
  "by_t": "{name} — resultados por ano de conclusão (dados da própria Ironhack)",
  "by_s": "Contratado na área vs. nunca colocado, por coorte. As médias globais escondem a queda recente.",
  "by_in": "Contratado como {role} (na área)", "by_never": "Nunca colocado / à procura / inativo",
  "by_y": "% dos diplomados do ano",
  "by_f": "Fonte: diretório interno de alumni da Ironhack, agregado & anónimo. github.com/donneepublique/ironhack-ux-outcomes",
  "name": {"wd": "Desenvolvimento web", "ux": "UX/UI Design", "da": "Data Analytics", "cy": "Cibersegurança", "ai": "AI Engineering", "ml": "Data Science & ML"},
  "role": {"wd": "developer", "ux": "designer", "da": "analista de dados", "cy": "função de cibersegurança", "ai": "engenheiro de IA", "ml": "cientista de dados"},
 },
}


def load_all_by_year():
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
    return agg


def load_track_years(track):
    by = defaultdict(list)
    for line in open(os.path.join(HERE, "data_all", f"alumni_{track}.jsonl")):
        r = json.loads(line)
        by[((r.get("cohort") or {}).get("end_date") or "")[:4]].append((r.get("career_services") or {}).get("status") or "")
    out = {}
    for y in BYEARS:
        sts = by.get(y, [])
        if len(sts) < MIN_N:
            continue
        bc = Counter(BUCKETS.get(s, "?") for s in sts); n = len(sts)
        out[y] = {"n": n, "in": round(100 * bc.get("Salaried designer job (in field)", 0) / n, 1),
                  "never": round(100 * bc.get("Never placed / searching / inactive", 0) / n, 1)}
    return out


def scale_chart(lang, t, agg):
    infield = [agg[y]["in"] for y in YEARS]
    never = [agg[y]["never"] for y in YEARS]
    other = [agg[y]["n"] - agg[y]["in"] - agg[y]["never"] for y in YEARS]
    ns = [agg[y]["n"] for y in YEARS]
    pin = [round(100 * agg[y]["in"] / agg[y]["n"]) for y in YEARS]
    fig, ax = plt.subplots(figsize=(9.5, 5.6), dpi=200)
    x = range(len(YEARS))
    ax.bar(x, infield, 0.62, color=BLUE, zorder=3, label=t["leg_in"])
    ax.bar(x, other, 0.62, bottom=infield, color=GREY, zorder=3, label=t["leg_other"])
    ax.bar(x, never, 0.62, bottom=[i + o for i, o in zip(infield, other)], color=RED, zorder=3, label=t["leg_never"])
    ax.set_xticks(list(x)); ax.set_xticklabels(YEARS, fontsize=11)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0); ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
    ax.set_ylabel(t["scale_y"], fontsize=10, color=INK2); ax.set_ylim(0, max(ns) * 1.15)
    for xi in x:
        ax.text(xi, ns[xi] + max(ns) * 0.015, f"{ns[xi]:,}".replace(",", " "), ha="center", va="bottom", fontsize=9.5, color=INK, fontweight="bold")
        ax.text(xi, infield[xi] / 2, f"{pin[xi]}%", ha="center", va="center", fontsize=9, color="#fff", fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    fig.suptitle(t["scale_t"], x=0.012, y=0.99, ha="left", fontsize=14.5, fontweight="bold", color=INK)
    ax.set_title(t["scale_s"], loc="left", fontsize=10, color=INK2, pad=10)
    fig.text(0.012, 0.005, t["scale_f"], ha="left", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    os.makedirs(os.path.join(HERE, "assets", lang), exist_ok=True)
    fig.savefig(os.path.join(HERE, "assets", lang, "scale_vs_placement.png"), bbox_inches="tight"); plt.close(fig)


def track_chart(lang, t, track, py):
    yrs = list(py.keys()); ns = [py[y]["n"] for y in yrs]
    infield = [py[y]["in"] for y in yrs]; never = [py[y]["never"] for y in yrs]
    fig, ax = plt.subplots(figsize=(max(6.5, 1.15 * len(yrs) + 2.5), 5.2), dpi=200)
    x = range(len(yrs)); w = 0.4
    ax.bar([i - w / 2 for i in x], infield, w, color=BLUE, zorder=3, label=t["by_in"].format(role=t["role"][track]))
    ax.bar([i + w / 2 for i in x], never, w, color=RED, zorder=3, label=t["by_never"])
    ax.set_xticks(list(x)); ax.set_xticklabels([f"{y}\n(n={n})" for y, n in zip(yrs, ns)], fontsize=10)
    mx = max(infield + never + [1])
    ax.set_ylim(0, mx * 1.18)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0); ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
    ax.set_ylabel(t["by_y"], fontsize=9.5, color=INK2)
    for xi in x:
        for off, arr in [(-w / 2, infield), (w / 2, never)]:
            ax.text(xi + off, arr[xi] + mx * 0.012, f"{arr[xi]:.0f}%", ha="center", va="bottom", fontsize=8.5, color=INK, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    fig.suptitle(t["by_t"].format(name=t["name"][track]), x=0.012, y=0.99, ha="left", fontsize=14, fontweight="bold", color=INK)
    ax.set_title(t["by_s"], loc="left", fontsize=9.5, color=INK2, pad=10)
    fig.text(0.012, 0.005, t["by_f"], ha="left", fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    d = os.path.join(HERE, "assets", lang, "tracks"); os.makedirs(d, exist_ok=True)
    fig.savefig(os.path.join(d, f"{track}_by_year.png"), bbox_inches="tight"); plt.close(fig)


def main():
    agg = load_all_by_year()
    tracks = {t: load_track_years(t) for t in TRACKS}
    for lang in ["fr", "de", "pt"]:
        t = STR[lang]
        scale_chart(lang, t, agg)
        for tr in TRACKS:
            track_chart(lang, t, tr, tracks[tr])
        print(f"{lang}: scale + 6 track charts -> assets/{lang}/")


if __name__ == "__main__":
    main()
