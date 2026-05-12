"""
Recreate the two minimalist bar charts using the official NEU / AEP palette,
and label every bar with the proper percent price effect:

  Figure A — final-price effect · comparison across attributes
             (one color for positives, one for negatives).

  Figure B — import premium · by parent category
             (one color for positives, one for negatives).

Both figures use bar widths and labels measured in percent price effect
(exp(β) − 1) × 100, NOT raw log-points × 100. For example, β = 1.00 in
Fresh Produce becomes +173 %, not +100 %.

Sources:
  output/thesis_table_coefficient_comparison.csv  (β_final column)
  output/thesis_table_category_heterogeneity.csv  (is_import column)
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

HERE = Path(__file__).resolve().parent

# ---- official NEU / AEP palette ------------------------------------------
GOLD   = "#c8a02d"   # NEU/AEP gold
NEG    = "#0b2647"   # AEP deep navy        (negatives)
POS    = "#8d0f1f"   # NEU burgundy         (positives)
INK    = "#141414"   # near-black for body text
PANEL  = "#f7f3ec"   # warm parchment background
WHITE  = "#ffffff"
MUTED  = GOLD        # use gold for italic p-value tags

rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.edgecolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.labelcolor": INK,
    "axes.titlecolor": INK,
})


def colorfor(v: float) -> str:
    return POS if v >= 0 else NEG


def pct_effect(beta: float) -> float:
    """Convert a log-point coefficient to a proper percent price effect."""
    return float(np.exp(beta) - 1.0)


# =========================================================================
# Figure A — final-price effect · comparison across attributes
# =========================================================================
coef_df = pd.read_csv(HERE / "thesis_table_coefficient_comparison.csv",
                      index_col=0)

ATTR_KEEP = [
    ("Premium tier (+)",        "is_premium"),
    ("Pack size (log)",         "ln_pack_size"),
    ("High recognition (+)",    "is_high_recognition"),
    ("House brand (WinEco)",    "is_house_brand"),
    ("Imported",                "is_import"),
    ("Freshness claim",         "has_freshness_claim"),
    ("Branded (Local & Value)", "is_branded"),
]
keep_idx = [name for name, _ in ATTR_KEEP]
labels   = [code for _, code in ATTR_KEEP]
betas    = [coef_df.loc[name, "β_final"] for name in keep_idx]
pcts     = [pct_effect(b) for b in betas]

# Sort by |percent effect| descending
order = np.argsort([abs(p) for p in pcts])[::-1]
labels = [labels[i] for i in order]
pcts   = [pcts[i]   for i in order]

fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=PANEL)
ax.set_facecolor(PANEL)

y = np.arange(len(labels))[::-1]
abs_p   = [abs(p) for p in pcts]
colors  = [colorfor(p) for p in pcts]

ax.barh(y, abs_p, color=colors, height=0.55, edgecolor="none")

# Numeric labels (signed %) just to the right of each bar
xmax_a = max(abs_p) * 1.30
pad_a  = 0.012 * xmax_a
for yi, p in zip(y, pcts):
    ax.text(abs(p) + pad_a, yi, f"{p*100:+.1f}%",
            va="center", ha="left", fontsize=11, fontweight="bold",
            color=colorfor(p), family="DejaVu Sans Mono")

# Attribute labels left of each bar (monospace, like the original)
LEFT_GUTTER_A = -0.02
for yi, lbl in zip(y, labels):
    ax.text(LEFT_GUTTER_A, yi, lbl,
            va="center", ha="right", fontsize=11, color=INK,
            family="DejaVu Sans Mono")

# Headline — gold rule + INK title
HEADLINE_Y = len(labels) - 0.05
ax.plot([-0.6, xmax_a], [HEADLINE_Y + 0.55] * 2,
        color=GOLD, linewidth=1.8, zorder=2)
ax.text(-0.6, HEADLINE_Y + 0.18,
        "f i n a l - p r i c e   e f f e c t   ·   "
        "c o m p a r i s o n   a c r o s s   a t t r i b u t e s",
        ha="left", va="bottom",
        fontsize=12, fontweight="bold", color=INK,
        family="DejaVu Sans")

ax.set_xlim(0, xmax_a)
ax.set_ylim(-0.6, len(labels) + 0.4)
ax.set_xticks([])
ax.set_yticks([])
for side in ("left", "right", "top", "bottom"):
    ax.spines[side].set_visible(False)
fig.patch.set_facecolor(PANEL)

plt.tight_layout()
out_a = HERE / "thesis_fig_betas_comparison_simple.png"
plt.savefig(out_a, dpi=200, bbox_inches="tight", facecolor=PANEL)
plt.close(fig)
print(f"Saved -> {out_a}")


# =========================================================================
# Figure B — import premium · by parent category
# =========================================================================
hetero = pd.read_csv(HERE / "thesis_table_category_heterogeneity.csv",
                     index_col=0)

CAT_EN = {
    "Bánh Kẹo":               "Confectionery",
    "Chăm Sóc Bé":            "Baby Care",
    "Gia Vị":                 "Spices",
    "Mì - Thực Phẩm Ăn Liền": "Instant Food",
    "Rau - Củ - Trái Cây":    "Fresh Produce",
    "Sữa Tươi":               "Dairy",
    "Thực Phẩm Chế Biến":     "Processed Food",
    "Thực Phẩm Khô":          "Dry Food",
    "Thực Phẩm Đông Lạnh":    "Frozen",
}

imp_beta = hetero["is_import"].rename(index=CAT_EN)
DROP = {"Baby Care", "Confectionery"}            # drop near-zero / hidden rows
imp_beta = imp_beta[~imp_beta.index.isin(DROP)]
imp_beta = imp_beta.sort_values(ascending=False)

# Convert betas to proper percent price effect
imp_pct = imp_beta.apply(pct_effect)

# Significance annotations — only the two extremes were highlighted in the
# original figure (Fresh Produce p<0.001, Processed Food p=0.013).
SIG = {
    "Fresh Produce":  "p<0.001",
    "Processed Food": "p=0.013",
}

fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=PANEL)
ax.set_facecolor(PANEL)

y        = np.arange(len(imp_pct))[::-1]
vals     = imp_pct.values
labels_b = imp_pct.index.tolist()
colors_b = [colorfor(v) for v in vals]

ax.barh(y, vals, color=colors_b, height=0.55, edgecolor="none")

# Vertical zero line — gold
ax.axvline(0, color=GOLD, linewidth=1.8, alpha=0.95)

# Value labels just outside the bar
xmax_b = max(abs(vals)) * 1.05
pad_b  = 0.02 * xmax_b
for yi, v in zip(y, vals):
    if v >= 0:
        ax.text(v + pad_b, yi, f"{v*100:+.0f}%",
                va="center", ha="left",
                fontsize=12, fontweight="bold", color=POS)
    else:
        ax.text(v - pad_b, yi, f"{v*100:+.0f}%",
                va="center", ha="right",
                fontsize=12, fontweight="bold", color=NEG)

# Category labels — fixed gutter on the left
LEFT_GUTTER_B = -xmax_b - 0.55
for yi, lbl in zip(y, labels_b):
    ax.text(LEFT_GUTTER_B, yi, lbl,
            va="center", ha="left", fontsize=12, color=INK)

# Significance tags — italic gold, well past the value label so they never
# collide. Negatives place the tag on the positive side of zero.
SIG_OFFSET = 0.32 * xmax_b
for yi, lbl, v in zip(y, labels_b, vals):
    if lbl not in SIG:
        continue
    if v >= 0:
        ax.text(v + SIG_OFFSET, yi, SIG[lbl],
                va="center", ha="left",
                fontsize=10, fontstyle="italic", color=MUTED)
    else:
        ax.text(0.10 * xmax_b, yi, SIG[lbl],
                va="center", ha="left",
                fontsize=10, fontstyle="italic", color=MUTED)

# Headline — gold rule + INK title
HEADLINE_Y_B = len(imp_pct) + 0.05
ax.plot([LEFT_GUTTER_B, xmax_b + 0.55], [HEADLINE_Y_B + 0.55] * 2,
        color=GOLD, linewidth=1.8, zorder=2)
ax.text(LEFT_GUTTER_B, HEADLINE_Y_B + 0.18,
        "i m p o r t   p r e m i u m   ·   "
        "b y   p a r e n t   c a t e g o r y",
        ha="left", va="bottom",
        fontsize=12, fontweight="bold", color=INK)

ax.set_xlim(LEFT_GUTTER_B - 0.05, xmax_b + 0.65)
ax.set_ylim(-0.7, len(imp_pct) + 1.0)
ax.set_xticks([])
ax.set_yticks([])
for side in ("left", "right", "top", "bottom"):
    ax.spines[side].set_visible(False)
fig.patch.set_facecolor(PANEL)

plt.tight_layout()
out_b = HERE / "thesis_fig_import_premium_simple.png"
plt.savefig(out_b, dpi=200, bbox_inches="tight", facecolor=PANEL)
plt.close(fig)
print(f"Saved -> {out_b}")

# ---- recap to stdout for sanity check ------------------------------------
print("\nFigure B values (β -> proper % effect):")
for cat in imp_pct.index:
    print(f"  {cat:<16}  β = {imp_beta[cat]:+.4f}  ->  "
          f"{imp_pct[cat]*100:+.1f}%")
