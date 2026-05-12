"""
Redo the per-category hedonic premiums heatmap with row/column ordering.

Produces two versions, both with English labels:
  1) Hierarchical-clustering ordering (similar patterns grouped together).
  2) "Diverging-diagonal" ordering (warm cells top-left, cool cells bottom-right).

Source: output/thesis_table_category_heterogeneity.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import pdist

# ----- paths -----
HERE = Path(__file__).resolve().parent
SRC = HERE / "thesis_table_category_heterogeneity.csv"

# ----- load data -----
df = pd.read_csv(SRC, index_col=0)

# ----- translations -----
CAT_EN = {
    "Bánh Kẹo":               "Confectionery",
    "Chăm Sóc Bé":            "Baby Care",
    "Gia Vị":                 "Spices",
    "Mì - Thực Phẩm Ăn Liền": "Instant Food",
    "Rau - Củ - Trái Cây":    "Vegetables & Fruit",
    "Sữa Tươi":               "Fresh Dairy",
    "Thực Phẩm Chế Biến":     "Processed Food",
    "Thực Phẩm Khô":          "Dry Food",
    "Thực Phẩm Đông Lạnh":    "Frozen Food",
}
COL_EN = {
    "is_branded":          "Brand\npremium",
    "is_import":           "Import\npremium",
    "ln_pack_size":        "Pack size\n(log)",
    "has_health_claim":    "Health\nclaim",
    "has_freshness_claim": "Freshness\nclaim",
}

df = df.rename(index=CAT_EN, columns=COL_EN)

# Force tiny floating dust around zero (e.g. 1e-15) to a clean zero so the
# colormap doesn't read meaningless noise as a tint.
DUST = 1e-6
M = df.where(df.abs() > DUST, 0.0).astype(float)

print("Data after relabel + dedust:")
print(M.round(2))


def render_heatmap(matrix: pd.DataFrame, title: str, out_path: Path) -> None:
    """Render a single annotated heatmap with the project's RdBu_r colour scale."""
    vmax = float(np.nanmax(np.abs(matrix.values)))
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    im = ax.imshow(matrix.values, cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                   aspect="auto")

    # Cell annotations (white text on dark cells, black on light)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            v = matrix.values[i, j]
            if np.isnan(v):
                continue
            colour = "white" if abs(v) > vmax * 0.55 else "black"
            ax.text(j, i, f"{v:+.2f}", ha="center", va="center",
                    fontsize=9, color=colour)

    # Axes & ticks
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_xticklabels(matrix.columns, fontsize=10)
    ax.set_yticks(range(matrix.shape[0]))
    ax.set_yticklabels(matrix.index, fontsize=10)
    ax.set_xlabel("")
    ax.set_ylabel("")

    # Light cell separators
    ax.set_xticks(np.arange(-0.5, matrix.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, matrix.shape[0], 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("Coefficient (log price)", fontsize=10)

    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {out_path}")


# -------------------------------------------------------------------------
# Version A: hierarchical clustering on both axes
# -------------------------------------------------------------------------
# Use correlation distance so categories with similar premium *patterns*
# (regardless of magnitude) cluster together.
row_link = linkage(pdist(M.values,        metric="correlation"), method="average")
col_link = linkage(pdist(M.values.T,      metric="correlation"), method="average")
row_order = leaves_list(row_link)
col_order = leaves_list(col_link)

M_clustered = M.iloc[row_order, :].iloc[:, col_order]

render_heatmap(
    M_clustered,
    title="Hedonic Premiums by Category — clustered\n"
          "(rows & columns reordered to group similar patterns)",
    out_path=HERE / "thesis_fig_category_heterogeneity_clustered.png",
)

# -------------------------------------------------------------------------
# Version B: diverging-diagonal ordering
# -------------------------------------------------------------------------
# Sort rows so the most "warm" (positive average) categories are at the top,
# and columns so the most "warm" attributes are on the left.
row_score = M.mean(axis=1).sort_values(ascending=False)
col_score = M.mean(axis=0).sort_values(ascending=False)

M_diag = M.loc[row_score.index, col_score.index]

render_heatmap(
    M_diag,
    title="Hedonic Premiums by Category — diverging diagonal\n"
          "(warm premiums concentrated top-left, cool effects bottom-right)",
    out_path=HERE / "thesis_fig_category_heterogeneity_diagonal.png",
)

print("\nRow order (clustered):", list(M_clustered.index))
print("Col order (clustered):", [c.replace('\n', ' ') for c in M_clustered.columns])
print("\nRow order (diagonal): ", list(M_diag.index))
print("Col order (diagonal): ", [c.replace('\n', ' ') for c in M_diag.columns])
