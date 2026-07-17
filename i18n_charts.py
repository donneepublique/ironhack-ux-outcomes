#!/usr/bin/env python3
"""
Generate LOCALISED copies of the five charts into assets/<lang>/ (fr, de, pt).

The English assets/*.png are left untouched (they are in the timestamped
provenance manifest). Run:  python3 i18n_charts.py
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(__file__)
rep = json.load(open(os.path.join(HERE, "data", "report_all.json")))
N = rep["overall"]["n"]

# palette (dataviz skill, light surface)
SURFACE, INK, INK2, MUTED, GRID, BAR = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, RED, AMBER = "#2a78d6", "#d03b3b", "#fab219"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95"]
LOWN_FILL, MIN_N = "#edeeea", 20
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": INK,
})

# bucket keys in report_all.json
BK = {
    "never": "Never placed / searching / inactive",
    "infield": "Salaried designer job (in field)",
    "notdes": "Job, but NOT as a designer",
    "left": "Left the field (school / other)",
    "free": "Freelance / self-employed",
    "incomplete": "Did not complete / not eligible",
    "intern": "Internship only",
}

STR = {
 "fr": {
  "b_never": "Jamais placé / en recherche / inactif", "b_infield": "Recruté comme designer (dans le domaine)",
  "b_notdes": "En emploi, mais PAS comme designer", "b_left": "A quitté le domaine (études / autre)",
  "b_free": "Freelance / à son compte", "b_incomplete": "Non diplômé / non éligible", "b_intern": "Stage uniquement",
  "c1_t": f"Ce qui est réellement arrivé aux {N:,} diplômés UX/UI d'Ironhack".replace(",", " "),
  "c1_s": "Statuts issus du répertoire alumni d'Ironhack, regroupés. Seulement ~1 sur 5 a été recruté comme designer.",
  "c2_t": "Le chiffre « ~90 % placés », décortiqué",
  "c2_s": "Mêmes données alumni, trois définitions. « Placé » n'est pas « travaille comme designer ».",
  "c2_b": ["Affirmation d'Ironhack :\n« ~90 % des chercheurs d'emploi placés »",
           "Recalcul généreux sur les données :\nN'IMPORTE quel emploi ÷ chercheurs d'emploi",
           "Lecture honnête :\nrecruté comme designer ÷ tous les diplômés"],
  "c2_n": "Chiffre Ironhack : rapport d'insertion audité par PwC (diplômés en recherche, sous 6 mois).",
  "c3_t": "Recrutés comme designer, par campus",
  "c3_s": "Même le meilleur campus plafonne vers 28 %. Le campus À distance (le plus gros effectif), très mis en avant, est le pire.",
  "c3_n": "Amsterdam n=8 — trop peu pour en tirer une conclusion.",
  "c4_t": "Les résultats se dégradent, promotion après promotion",
  "c4_s": "Part recrutée comme designer vs. jamais placée / en recherche, par année de diplôme.",
  "c4_l": ["Recruté comme designer (dans le domaine)", "Jamais placé / en recherche / inactif"],
  "c4_y": "% des diplômés de l'année",
  "c4_n": "Promotions 2025–2026 gonflées par la récence (peu de temps pour trouver). Années à date placeholder (1987) et n<20 exclues.",
  "c5_t": "Taux de recrutement comme designer, campus × année de diplôme",
  "c5_s": "Plus foncé = taux plus élevé. Cases grises : n<20 (trop peu). Vide = aucun diplômé.",
  "c5_n": "L'étiquette de ligne indique le n total du campus. Même les meilleures cases dépassent rarement 50 %, et s'érodent après 2022.",
  "c6_t": "La promotion 2025 — la cohorte UX/UI la plus récente d'Ironhack (n={n})",
  "c6_s": "{a} % recrutés comme designer. {b} % jamais placés ou encore en recherche. (2026 est trop récent pour être lu.)",
  "camp": {"rmt": "À distance", "mad": "Madrid", "ber": "Berlin", "par": "Paris", "bcn": "Barcelone",
           "lis": "Lisbonne", "sao": "São Paulo", "mex": "Mexico", "mia": "Miami", "ams": "Amsterdam"},
 },
 "de": {
  "b_never": "Nie vermittelt / auf Suche / inaktiv", "b_infield": "Als Designer angestellt (im Fachgebiet)",
  "b_notdes": "Beschäftigt, aber NICHT als Designer", "b_left": "Fachgebiet verlassen (Studium / Sonstiges)",
  "b_free": "Freiberuflich / selbstständig", "b_incomplete": "Nicht abgeschlossen / nicht berechtigt", "b_intern": "Nur Praktikum",
  "c1_t": f"Was mit den {N:,} UX/UI-Absolventen von Ironhack wirklich geschah".replace(",", "."),
  "c1_s": "Ironhacks eigene Alumni-Verzeichnis-Labels, gruppiert. Nur ~1 von 5 wurde als Designer eingestellt.",
  "c2_t": "Die Schlagzeile „~90 % vermittelt“, auseinandergenommen",
  "c2_s": "Dieselben Alumni-Daten, drei Definitionen. „Vermittelt“ heißt nicht „arbeitet als Designer“.",
  "c2_b": ["Ironhacks Behauptung:\n„~90 % der Suchenden vermittelt“",
           "Großzügige Neuberechnung:\nIRGENDEIN Job ÷ Suchende",
           "Ehrliche Lesart:\nals Designer eingestellt ÷ alle Absolventen"],
  "c2_n": "Ironhack-Zahl: von PwC geprüfter Outcomes-Bericht (suchende Absolventen, binnen 6 Monaten).",
  "c3_t": "Als Designer eingestellt, nach Standort",
  "c3_s": "Selbst der beste Standort erreicht kaum 28 %. Der stark beworbene Remote-Track (größte Kohorte) ist am schlechtesten.",
  "c3_n": "Amsterdam n=8 — zu klein für eine Aussage.",
  "c4_t": "Die Ergebnisse werden Kohorte für Kohorte schlechter",
  "c4_s": "Anteil als Designer eingestellt vs. nie vermittelt / auf Suche, nach Abschlussjahr.",
  "c4_l": ["Als Designer eingestellt (im Fachgebiet)", "Nie vermittelt / auf Suche / inaktiv"],
  "c4_y": "% der Absolventen des Jahres",
  "c4_n": "Kohorten 2025–2026 durch Aktualität verzerrt (wenig Zeit). Platzhalterdatierte (1987) und n<20-Jahre ausgeschlossen.",
  "c5_t": "Einstellungsquote als Designer, Standort × Abschlussjahr",
  "c5_s": "Dunkler = höhere Quote. Graue Zellen: n<20 (zu klein). Leer = keine Absolventen.",
  "c5_n": "Zeilenbeschriftung = Gesamt-n des Standorts. Selbst die stärksten Zellen überschreiten selten 50 % und erodieren nach 2022.",
  "c6_t": "Der Jahrgang 2025 — Ironhacks jüngste UX/UI-Kohorte (n={n})",
  "c6_s": "{a} % als Designer eingestellt. {b} % nie vermittelt oder noch auf Suche. (2026 ist zu aktuell.)",
  "camp": {"rmt": "Remote", "mad": "Madrid", "ber": "Berlin", "par": "Paris", "bcn": "Barcelona",
           "lis": "Lissabon", "sao": "São Paulo", "mex": "Mexiko-Stadt", "mia": "Miami", "ams": "Amsterdam"},
 },
 "pt": {
  "b_never": "Nunca colocado / à procura / inativo", "b_infield": "Contratado como designer (na área)",
  "b_notdes": "Empregado, mas NÃO como designer", "b_left": "Saiu da área (estudos / outro)",
  "b_free": "Freelancer / por conta própria", "b_incomplete": "Não concluiu / não elegível", "b_intern": "Apenas estágio",
  "c1_t": f"O que realmente aconteceu aos {N:,} diplomados de UX/UI da Ironhack".replace(",", " "),
  "c1_s": "Rótulos do próprio diretório de alumni da Ironhack, agrupados. Apenas ~1 em 5 foi contratado como designer.",
  "c2_t": "A manchete «~90% colocados», desmontada",
  "c2_s": "Os mesmos dados de alumni, três definições. «Colocado» não é «a trabalhar como designer».",
  "c2_b": ["Afirmação da Ironhack:\n«~90% dos candidatos colocados»",
           "Recálculo generoso sobre os dados:\nQUALQUER emprego ÷ candidatos",
           "Leitura honesta:\ncontratado como designer ÷ todos os diplomados"],
  "c2_n": "Número da Ironhack: relatório de resultados auditado pela PwC (diplomados à procura, em 6 meses).",
  "c3_t": "Contratados como designer, por campus",
  "c3_s": "Mesmo o melhor campus não passa dos ~28%. O campus Remoto (maior coorte), muito promovido, é o pior.",
  "c3_n": "Amesterdão n=8 — demasiado pequeno para conclusões.",
  "c4_t": "Os resultados pioram, coorte após coorte",
  "c4_s": "Percentagem contratada como designer vs. nunca colocada / à procura, por ano de conclusão.",
  "c4_l": ["Contratado como designer (na área)", "Nunca colocado / à procura / inativo"],
  "c4_y": "% dos diplomados do ano",
  "c4_n": "Coortes de 2025–2026 inflacionadas pela recência (pouco tempo). Anos com data placeholder (1987) e n<20 excluídos.",
  "c5_t": "Taxa de contratação como designer, campus × ano de conclusão",
  "c5_s": "Mais escuro = taxa mais alta. Células cinzentas: n<20 (demasiado pequeno). Vazio = sem diplomados.",
  "c5_n": "O rótulo da linha mostra o n total do campus. Mesmo as melhores células raramente passam de 50% e erodem após 2022.",
  "c6_t": "A turma de 2025 — a coorte de UX/UI mais recente da Ironhack (n={n})",
  "c6_s": "{a}% contratados como designer. {b}% nunca colocados ou à procura. (2026 é demasiado recente.)",
  "camp": {"rmt": "Remoto", "mad": "Madrid", "ber": "Berlim", "par": "Paris", "bcn": "Barcelona",
           "lis": "Lisboa", "sao": "São Paulo", "mex": "Cidade do México", "mia": "Miami", "ams": "Amesterdão"},
 },
}


def hbar(ax_out, title, subtitle, labels, values, colors, value_fmt, note):
    fig, ax = plt.subplots(figsize=(9.8, 0.62 * len(labels) + 1.9), dpi=200)
    y = range(len(labels))
    ax.barh(y, values, color=colors, height=0.66, zorder=3)
    ax.set_yticks(list(y)); ax.set_yticklabels(labels, fontsize=11); ax.invert_yaxis()
    ax.set_xlim(0, max(values) * 1.18)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", labelsize=9)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
    for yi, v in zip(y, values):
        ax.text(v + max(values) * 0.015, yi, value_fmt(yi, v), va="center", ha="left",
                fontsize=10.5, color=INK, fontweight="bold")
    fig.suptitle(title, x=0.012, y=0.985, ha="left", fontsize=15, fontweight="bold", color=INK)
    ax.set_title(subtitle, loc="left", fontsize=10, color=INK2, pad=12)
    if note:
        fig.text(0.012, 0.012, note, ha="left", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03 if note else 0, 1, 0.94))
    fig.savefig(ax_out, bbox_inches="tight"); plt.close(fig)


def grouped_years(out, title, subtitle, years, ns, s1, s2, l1, l2, ylab, note):
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
    x = range(len(years)); w = 0.4
    ax.bar([i - w / 2 for i in x], s1, w, color=BLUE, zorder=3, label=l1)
    ax.bar([i + w / 2 for i in x], s2, w, color=RED, zorder=3, label=l2)
    ax.set_xticks(list(x)); ax.set_xticklabels([f"{y}\n(n={n})" for y, n in zip(years, ns)], fontsize=10)
    ax.set_ylim(0, max(s1 + s2) * 1.18)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID); ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0); ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0); ax.set_axisbelow(True)
    ax.set_ylabel(ylab, fontsize=9.5, color=INK2)
    for xi in x:
        for off, arr in [(-w / 2, s1), (w / 2, s2)]:
            ax.text(xi + off, arr[xi] + max(s1 + s2) * 0.012, f"{arr[xi]:.0f}", ha="center",
                    va="bottom", fontsize=8.5, color=INK, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=10.5)
    fig.suptitle(title, x=0.012, y=0.99, ha="left", fontsize=15, fontweight="bold", color=INK)
    ax.set_title(subtitle, loc="left", fontsize=10, color=INK2, pad=10)
    fig.text(0.012, 0.005, note, ha="left", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(out, bbox_inches="tight"); plt.close(fig)


def heatmap(out, title, subtitle, rows_labels, cols, matrix, note):
    nr, nc = len(rows_labels), len(cols)
    fig, ax = plt.subplots(figsize=(1.15 * nc + 2.8, 0.62 * nr + 2.0), dpi=200)
    for i in range(nr):
        for j in range(nc):
            cell = matrix[i][j]; x, y = j, nr - 1 - i
            if cell is None:
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor=SURFACE, edgecolor="#fff", linewidth=2)); continue
            v, n = cell["in_field_pct"], cell["n"]
            if n < MIN_N:
                fc, tc = LOWN_FILL, MUTED
            else:
                idx = min(len(BLUE_RAMP) - 1, int(v // 8)); fc = BLUE_RAMP[idx]; tc = "#fff" if idx >= 3 else INK
            ax.add_patch(Rectangle((x, y), 1, 1, facecolor=fc, edgecolor="#fff", linewidth=2))
            ax.text(x + 0.5, y + 0.60, f"{v:.0f}%", ha="center", va="center", fontsize=11, fontweight="bold", color=tc)
            ax.text(x + 0.5, y + 0.28, f"n={n}", ha="center", va="center", fontsize=8, color=tc)
    ax.set_xlim(0, nc); ax.set_ylim(0, nr)
    ax.set_xticks([j + 0.5 for j in range(nc)]); ax.set_xticklabels(cols, fontsize=10)
    ax.set_yticks([nr - 1 - i + 0.5 for i in range(nr)]); ax.set_yticklabels(rows_labels, fontsize=10.5)
    ax.xaxis.tick_top()
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    fig.suptitle(title, x=0.012, y=0.995, ha="left", fontsize=14.5, fontweight="bold", color=INK)
    ax.set_title(subtitle, loc="left", fontsize=10, color=INK2, pad=22)
    fig.text(0.012, 0.008, note, ha="left", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(out, bbox_inches="tight"); plt.close(fig)


def gen(lang):
    t = STR[lang]
    outdir = os.path.join(HERE, "assets", lang)
    os.makedirs(outdir, exist_ok=True)
    b = rep["overall"]["buckets"]

    # chart 1
    order = [("b_never", BK["never"], RED), ("b_infield", BK["infield"], BLUE),
             ("b_notdes", BK["notdes"], BAR), ("b_left", BK["left"], BAR),
             ("b_free", BK["free"], BAR), ("b_incomplete", BK["incomplete"], BAR),
             ("b_intern", BK["intern"], BAR)]
    labels = [t[k] for k, _, _ in order]
    counts = [b[bk] for _, bk, _ in order]
    pcts = [round(100 * c / N, 1) for c in counts]
    cols = [c for _, _, c in order]
    hbar(os.path.join(outdir, "01_outcomes.png"), t["c1_t"], t["c1_s"], labels, pcts, cols,
         lambda yi, v: f"{v:.1f} %  ({counts[yi]:,})".replace(",", " "), None)

    # chart 2
    hbar(os.path.join(outdir, "02_claim_vs_reality.png"), t["c2_t"], t["c2_s"], t["c2_b"],
         [90.0, rep["overall"]["ironhack_style_placed_pct"], rep["overall"]["in_field_pct_of_all"]],
         [BAR, AMBER, BLUE], lambda yi, v: f"{v:.1f} %", t["c2_n"])

    # chart 3
    pc = rep["per_campus"]
    items = sorted(pc.items(), key=lambda kv: -kv[1]["in_field_pct"])
    l3 = [f"{t['camp'].get(c, c)}  (n={d['n']})" for c, d in items]
    v3 = [d["in_field_pct"] for c, d in items]
    c3 = [RED if c == "rmt" else BAR for c, d in items]
    hbar(os.path.join(outdir, "03_by_campus.png"), t["c3_t"], t["c3_s"], l3, v3, c3,
         lambda yi, v: f"{v:.1f} %", t["c3_n"])

    # chart 4
    py = rep["per_year"]
    years = [y for y in ["2020", "2021", "2022", "2023", "2024", "2025", "2026"] if y in py]
    grouped_years(os.path.join(outdir, "04_by_year.png"), t["c4_t"], t["c4_s"], years,
                  [py[y]["n"] for y in years], [py[y]["in_field_pct"] for y in years],
                  [py[y]["never_placed_pct"] for y in years], t["c4_l"][0], t["c4_l"][1], t["c4_y"], t["c4_n"])

    # chart 5
    cyr = rep["per_campus_year"]
    cy_years = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
    order5 = sorted(cyr, key=lambda c: -pc[c]["n"])
    rows_l = [f"{t['camp'].get(c, c)} ({pc[c]['n']})" for c in order5]
    mat = [[cyr[c].get(y) for y in cy_years] for c in order5]
    heatmap(os.path.join(outdir, "05_campus_year.png"), t["c5_t"], t["c5_s"], rows_l, cy_years, mat, t["c5_n"])

    # chart 6 — class of 2025
    py25 = rep["per_year"]["2025"]
    b25 = [(t["b_never"], py25["never_placed_pct"], RED), (t["b_infield"], py25["in_field_pct"], BLUE),
           (t["b_notdes"], py25["not_designer_pct"], BAR), (t["b_free"], py25["freelance_pct"], BAR),
           (t["b_left"], py25["left_field_pct"], BAR), (t["b_intern"], py25["internship_pct"], BAR),
           (t["b_incomplete"], py25["incomplete_pct"], BAR)]
    b25.sort(key=lambda x: -x[1])
    a = f"{py25['in_field_pct']}".replace(".", ",")
    bb = f"{py25['never_placed_pct']}".replace(".", ",")
    hbar(os.path.join(outdir, "06_class_2025.png"), t["c6_t"].format(n=py25["n"]),
         t["c6_s"].format(a=a, b=bb), [l for l, _, _ in b25], [v for _, v, _ in b25],
         [c for _, _, c in b25], lambda yi, v: f"{v:.1f} %", None)
    print(f"{lang}: 6 charts -> assets/{lang}/")


if __name__ == "__main__":
    for lg in ["fr", "de", "pt"]:
        gen(lg)
    print("done")
