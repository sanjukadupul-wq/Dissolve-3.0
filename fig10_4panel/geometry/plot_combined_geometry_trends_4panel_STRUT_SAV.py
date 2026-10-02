# -*- coding: utf-8 -*-
"""
COPY of plot_combined_geometry_trends_4panel.py, made per explicit
instruction NOT to overlay the new strut-based SA/V data onto the original
disc-based Figure 10 (that script/figure is left completely untouched).
Panels (a)/(b) here use the STRUT-based SA/V study (straight rounded-square-
cross-section wires, self-similar 0.5x/1.0x/1.5x rescaling of
Rounded_Wire_Study's G0_straight_wire_rounded, STRUT=0.165mm baseline) in
place of the disc-based SA/V study -- a companion/robustness check on a
different specimen shape, same SA/V question. Panels (c)/(d) (curvature,
adjacent-strut spacing) are UNCHANGED from the original. Same Arial
house style/layout/panel-letter conventions as the original.

Unlike the disc-based panels, no mesh-bias correction is applied here --
there is no companion fine-mesh run for these struts (the mesh is
deliberately coarse, a scoping/confirmatory run against the already-known
SA/V phenomenology), so the raw coarse-mesh mass-loss values are the basis
for panel (a); they ARE display-smoothed the same way as the original's
disc panel (8-bin average + PCHIP) to remove coarse-mesh/coarse-dt
stair-step quantization in the raw 169-point series.

(a) Strut SA/V study: cumulative mass loss vs. time
(b) Strut SA/V ratio vs. final (672h) mass loss
(c) Wire curvature vs. final (672h) mass loss [unchanged]
(d) Adjacent-strut spacing vs. final (672h) mass loss [unchanged]

Data:
  sav_strut_study_summary.csv, sav_strut_study_timeseries.csv
  ("Supplementary figures" folder)
  Arc_MassLoss_TimeSeries.csv, Gap_MassLoss_TimeSeries.csv (this folder)
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

BASE = os.path.dirname(os.path.abspath(__file__))
SUPP = os.path.join(BASE, "..", "Supplementary figures")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 16,
    "axes.linewidth": 1.2,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
})


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.2)
    ax.spines["bottom"].set_linewidth(1.2)
    ax.tick_params(width=1.2, length=5)
    ax.set_facecolor("white")


def panel_letter(ax, text):
    ax.text(-0.16, 1.06, text, transform=ax.transAxes, fontsize=20,
             fontweight="bold", ha="left", va="bottom")


LABEL_FS = 18
LEGEND_FS = 13
MARKER_S = 110

fig, axes = plt.subplots(2, 2, figsize=(13.0, 10.4), facecolor="white")

# ===================================================================
# (b) Strut SA/V ratio vs. final mass loss
# ===================================================================
ax = axes[0, 1]
sav_summary = pd.read_csv(os.path.join(SUPP, "sav_strut_study_summary.csv"))

SAV_COLORS = ["#4C72B0", "#8C6D31", "#C44E52"]
SAV_ORDER = ["thin_sav", "mid_sav", "thick_sav"]
SAV_LABELS = {"thin_sav": "t=0.0825mm", "mid_sav": "t=0.165mm", "thick_sav": "t=0.2475mm"}
savs = sav_summary["SAV_ratio"].values
mls = sav_summary["FinalMassLoss_pct"].values
slope = np.sum(savs * mls) / np.sum(savs**2)
sav_line = np.linspace(0, savs.max() * 1.15, 100)
ax.plot(sav_line, slope * sav_line, color="0.35", linestyle="--", linewidth=1.4, zorder=1,
        label="Linear fit through origin")
for cfg, color in zip(SAV_ORDER, SAV_COLORS):
    row = sav_summary[sav_summary.Config == cfg].iloc[0]
    ax.scatter([row.SAV_ratio], [row.FinalMassLoss_pct], s=MARKER_S, color=color,
               edgecolor="black", linewidth=0.6, zorder=3,
               label=f"SA/V = {row.SAV_ratio:.2f} ({SAV_LABELS[cfg]})")
ax.set_xlabel("SA/V ratio (mm$^{-1}$)", fontsize=LABEL_FS)
ax.set_ylabel("Mass loss (%)", fontsize=LABEL_FS)
ax.set_xlim(0, savs.max() * 1.15)
ax.set_ylim(0, mls.max() * 1.15)
style_axes(ax)
ax.legend(loc="upper left", frameon=False, fontsize=LEGEND_FS, handlelength=2.0, labelspacing=0.5)
panel_letter(ax, "(b)")

# ===================================================================
# (a) Strut SA/V study: mass loss vs time
# ===================================================================
ax = axes[0, 0]
sav_ts = pd.read_csv(os.path.join(SUPP, "sav_strut_study_timeseries.csv"))

N_BINS = 8
t_max_all = sav_ts["TimeHours"].max()
for cfg, color in zip(SAV_ORDER, SAV_COLORS):
    d = sav_ts[sav_ts.Config == cfg].sort_values("TimeHours")
    t_raw = d["TimeHours"].values
    ml_raw = d["MassLossPercent"].values
    bin_edges = np.linspace(t_raw.min(), t_raw.max(), N_BINS + 1)
    bin_idx = np.clip(np.digitize(t_raw, bin_edges) - 1, 0, N_BINS - 1)
    t_bin = np.array([t_raw[bin_idx == k].mean() for k in range(N_BINS) if (bin_idx == k).any()])
    ml_bin = np.array([ml_raw[bin_idx == k].mean() for k in range(N_BINS) if (bin_idx == k).any()])
    t_bin = np.concatenate([[t_raw[0]], t_bin, [t_raw[-1]]])
    ml_bin = np.concatenate([[ml_raw[0]], ml_bin, [ml_raw[-1]]])
    t_bin, uniq_idx = np.unique(t_bin, return_index=True)
    ml_bin = ml_bin[uniq_idx]
    pchip = PchipInterpolator(t_bin, ml_bin)
    t_smooth = np.linspace(t_raw.min(), t_raw.max(), 400)
    sav = sav_summary.loc[sav_summary.Config == cfg, "SAV_ratio"].values[0]
    ax.plot(t_smooth, pchip(t_smooth), color=color, linewidth=2.3,
            zorder=3, label=f"SA/V = {sav:.2f}")
ax.set_xlabel("Time (h)", fontsize=LABEL_FS)
ax.set_ylabel("Mass loss (%)", fontsize=LABEL_FS)
ax.set_xlim(0, t_max_all)
ax.set_ylim(0, None)
style_axes(ax)
ax.legend(loc="upper left", frameon=False, fontsize=LEGEND_FS, handlelength=2.0, labelspacing=0.5)
panel_letter(ax, "(a)")

# ===================================================================
# (c) Curvature vs. final mass loss
# ===================================================================
ax = axes[1, 0]
arc = pd.read_csv(os.path.join(BASE, "Arc_MassLoss_TimeSeries.csv")).iloc[-1]
CURV_CONFIGS = ["StraightWire", "Arc30deg", "Arc90deg", "Arc150deg"]
RADIUS_MM = {"StraightWire": np.inf, "Arc30deg": 3.15, "Arc90deg": 1.05, "Arc150deg": 0.63}
CURV_COLORS = {"StraightWire": "#595959", "Arc30deg": "#2b6cb8", "Arc90deg": "#b32428", "Arc150deg": "#2ca02c"}
curvature = np.array([1.0 / RADIUS_MM[c] for c in CURV_CONFIGS])
final_ml_curv = np.array([arc[c] for c in CURV_CONFIGS])
slope_c, intercept_c = np.polyfit(curvature, final_ml_curv, 1)
x_line = np.linspace(0, curvature.max() * 1.15, 100)
ax.plot(x_line, slope_c * x_line + intercept_c, color="0.35", linestyle="--", linewidth=1.4, zorder=1,
        label="Linear fit")
for cfg in CURV_CONFIGS:
    ax.scatter([1.0 / RADIUS_MM[cfg]], [arc[cfg]], s=MARKER_S, color=CURV_COLORS[cfg],
               edgecolor="black", linewidth=0.6, zorder=3, label=f"$\\kappa$ = {1.0 / RADIUS_MM[cfg]:.2f}")
ax.set_xlabel("Curvature $\\kappa$ = 1/R (mm$^{-1}$)", fontsize=LABEL_FS)
ax.set_ylabel("Mass loss (%)", fontsize=LABEL_FS)
ax.set_xlim(0, curvature.max() * 1.15)
y_range = final_ml_curv.max() - final_ml_curv.min()
ax.set_ylim(final_ml_curv.min() - 0.15 * y_range, final_ml_curv.max() + 0.95 * y_range)
style_axes(ax)
ax.legend(loc="upper left", frameon=False, fontsize=LEGEND_FS, handlelength=2.0, labelspacing=0.5)
panel_letter(ax, "(c)")

# ===================================================================
# (d) Adjacent-strut spacing vs. final mass loss
# ===================================================================
ax = axes[1, 1]
gap = pd.read_csv(os.path.join(BASE, "Gap_MassLoss_TimeSeries.csv")).iloc[-1]
GAP_CONFIGS = ["CloseGap_CC0.30mm", "FarGap_CC1.60mm"]
SPACING_MM = {"CloseGap_CC0.30mm": 0.30, "FarGap_CC1.60mm": 1.60}
GAP_COLORS = {"CloseGap_CC0.30mm": "#2b6cb8", "FarGap_CC1.60mm": "#b32428"}
spacing = np.array([SPACING_MM[c] for c in GAP_CONFIGS])
final_ml_gap = np.array([gap[c] for c in GAP_CONFIGS])
slope_g, intercept_g = np.polyfit(spacing, final_ml_gap, 1)
x_line_g = np.linspace(0, spacing.max() * 1.3, 100)
ax.plot(x_line_g, slope_g * x_line_g + intercept_g, color="0.35", linestyle="--", linewidth=1.4, zorder=1,
        label="Linear fit")
for cfg in GAP_CONFIGS:
    ax.scatter([SPACING_MM[cfg]], [gap[cfg]], s=MARKER_S, color=GAP_COLORS[cfg],
               edgecolor="black", linewidth=0.6, zorder=3, label=f"Spacing = {SPACING_MM[cfg]:.2f} mm")
ax.set_xlabel("Center-to-center spacing (mm)", fontsize=LABEL_FS)
ax.set_ylabel("Mass loss (%)", fontsize=LABEL_FS)
ax.set_xlim(0, spacing.max() * 1.3)
y_range_g = final_ml_gap.max() - final_ml_gap.min()
ax.set_ylim(final_ml_gap.min() - 0.15 * y_range_g, final_ml_gap.max() + 0.75 * y_range_g)
style_axes(ax)
ax.legend(loc="upper left", frameon=False, fontsize=LEGEND_FS, handlelength=2.0, labelspacing=0.5)
panel_letter(ax, "(d)")

plt.tight_layout(w_pad=2.0, h_pad=1.4)
out_base = os.path.join(BASE, "Figure10_Combined_GeometryTrends_4Panel_STRUT_SAV")
plt.savefig(out_base + ".pdf", format="pdf", bbox_inches="tight", pad_inches=0.1)
plt.savefig(out_base + ".png", format="png", bbox_inches="tight", pad_inches=0.1, dpi=300)
print("Saved:", out_base + ".png / .pdf")
