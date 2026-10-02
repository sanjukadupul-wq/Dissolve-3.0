# -*- coding: utf-8 -*-
"""
Supplementary figure: SA/V study using STRAIGHT-STRUT specimens (companion
to plot_sav_study.py's disc-based SA/V study -- same question, different
specimen geometry). Same house style (Times New Roman, dpi 300, PDF+PNG).

Three straight wires, same rounded-square cross-section shape as
Rounded_Wire_Study's G0_straight_wire_rounded, scaled SELF-SIMILARLY so SA/V
varies as ~1/STRUT with no shape confound: L_TARGET=10*STRUT and
FILLET_R/HALF ratio held fixed at G0's 0.60606 for every specimen (not a
fixed 0.05mm fillet). Strut thickness 0.5x/1.0x/1.5x of the already-run
0.165mm G0 baseline (mid_sav IS a fresh regeneration of G0's exact geometry,
not reused by reference). Same kinetics as Rounded_Wire_Study/G0
(k_orr=0.25, k_f=10, k_d=39.22, film_tortuosity=120), 672h, 4h cadence,
redistance every 24h -- only geometry/thickness varies, so this isolates
the same SA/V effect the disc study probes, on an unrelated specimen shape.

Mesh: DELIBERATELY COARSE (size_min=0.3*STRUT per specimen, ~3 elements
across the strut width -- a scoping/confirmatory run against the
already-known SA/V phenomenology, not a new precision production run).
UNLIKE plot_sav_study.py, there is no companion fine-mesh run for these
struts, so NO mesh-bias correction is applied here -- the raw coarse-mesh
mass-loss values are plotted as-is. This means the absolute mass-loss
numbers carry whatever coarse-mesh bias is intrinsic to this resolution
(see pod_surrogate_v3's own coarse/fine mesh-correction work for the
expected sign/magnitude of that bias on similar specimens); the SHAPE of
the trend and the relative ordering across the 3 thicknesses are the
quantities this scoping run is meant to check, not the absolute values.

Panel A display smoothing: same bin-average (8 bins across 0-672h) + PCHIP
pass as plot_sav_study.py's Panel A, to remove the coarse-mesh/coarse-dt
stair-step quantization visible in the raw 169-point series without
altering the underlying trend or the true endpoint (anchored to the exact
first/last raw points).

Data: sav_strut_study_timeseries.csv (Config, SAV_ratio, TimeHours,
MassLossPercent) and sav_strut_study_summary.csv (Config,
StrutThickness_mm, SAV_ratio, FinalMassLoss_pct) -- RAW simulation output,
unmodified, built by build_sav_strut_csvs.py from the M3 run's result.txt
files, kept for provenance.

Two panels:
  A. Mass loss (%) vs time, one curve per strut -- the actual simulated
     trajectory (no mesh-bias correction, but display-smoothed the same way
     as plot_sav_study.py's Panel A: bin-average + PCHIP).
  B. Final (672h) mass loss vs SA/V ratio, with a linear fit through the
     origin (physically sensible: no surface, no dissolution).
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

BASE = os.path.dirname(os.path.abspath(__file__))
ts = pd.read_csv(os.path.join(BASE, "sav_strut_study_timeseries.csv"))
summary = pd.read_csv(os.path.join(BASE, "sav_strut_study_summary.csv"))

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'font.size': 19,
    'axes.labelsize': 19,
    'axes.linewidth': 1.0,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'figure.dpi': 300,
    'savefig.dpi': 300,
})

COLORS = ["#4C72B0", "#8C6D31", "#C44E52"]
CONFIG_ORDER = ["thin_sav", "mid_sav", "thick_sav"]
LABELS = {
    "thin_sav":  "t = 0.0825 mm (0.5x)",
    "mid_sav":   "t = 0.165 mm (baseline)",
    "thick_sav": "t = 0.2475 mm (1.5x)",
}

fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

# --- Panel A: mass-loss trajectories, display-smoothed (no mesh correction) -
N_BINS = 8
ax = axes[0]
t_max_all = ts["TimeHours"].max()
for cfg, color in zip(CONFIG_ORDER, COLORS):
    d = ts[ts.Config == cfg].sort_values("TimeHours")
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
    sav = summary.loc[summary.Config == cfg, "SAV_ratio"].values[0]
    ax.plot(t_smooth, pchip(t_smooth), color=color, linewidth=2.0,
             label=f"{LABELS[cfg]}, SA/V={sav:.2f}")
ax.set_xlim(0, t_max_all)
ax.set_ylim(0, None)
ax.set_xlabel("Time (hours)")
ax.set_ylabel("Cumulative mass loss (%)")
ax.legend(loc="upper left", fontsize=11.5, frameon=True, ncol=1)

# --- Panel B: final mass loss vs SA/V ratio ---------------------------------
ax = axes[1]
savs = summary["SAV_ratio"].values
mls = summary["FinalMassLoss_pct"].values
slope = np.sum(savs * mls) / np.sum(savs ** 2)
sav_line = np.linspace(0, savs.max() * 1.15, 100)
ax.plot(sav_line, slope * sav_line, color="0.35", linestyle="--", linewidth=1.3, zorder=1,
         label=f"Linear fit through origin\n(ML = {slope:.4f} x SA/V)")
for cfg, color in zip(CONFIG_ORDER, COLORS):
    row = summary[summary.Config == cfg].iloc[0]
    ax.scatter([row.SAV_ratio], [row.FinalMassLoss_pct], s=110, color=color,
                edgecolor="black", linewidth=0.6, zorder=3)
ax.set_xlabel("SA/V ratio (mm$^{-1}$)")
ax.set_ylabel("Final (672 h) mass loss (%)")
ax.legend(loc="upper left", fontsize=13.5, frameon=True, ncol=1)
ax.set_xlim(0, savs.max() * 1.15)
ax.set_ylim(0, mls.max() * 1.15)

for ax in axes:
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)

plt.tight_layout()

out_base = os.path.join(BASE, "FigS_SAV_StrutStudy")
plt.savefig(out_base + ".pdf", format="pdf", bbox_inches="tight")
plt.savefig(out_base + ".png", format="png", bbox_inches="tight", dpi=300)
print(f"Saved {out_base}.pdf / .png")
for cfg in CONFIG_ORDER:
    print(f"  {cfg}: final ML = {summary.loc[summary.Config == cfg, 'FinalMassLoss_pct'].values[0]:.4f}%")
