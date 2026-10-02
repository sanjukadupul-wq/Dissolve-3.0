"""Figure 6: disc vs. stent predicted degradation (a: mass loss, b: corrosion rate).
Usage:  python plot_fig6.py            (reads fig6_disc_stent_data.csv next to this file)
Outputs: Fig6.png (400 dpi), Fig6.pdf (vector)
Requires: numpy, pandas, matplotlib
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).resolve().parent
df = pd.read_csv(HERE / "fig6_disc_stent_data.csv")

DISC_COLOR, STENT_COLOR = "#4C72B0", "#C44E52"
T_DISC, T_STENT = 40, 100            # onset of diffusion control (h)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 14, "axes.labelsize": 16, "xtick.labelsize": 14, "ytick.labelsize": 14,
    "legend.fontsize": 13, "axes.linewidth": 0.8,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 3.6))

# (a) cumulative mass loss
ax1.plot(df.time_h, df.disc_mass_loss_pct, color=DISC_COLOR, lw=2, label="Disc")
ax1.plot(df.time_h, df.stent_mass_loss_pct, color=STENT_COLOR, lw=2, label="Stent")
ax1.set_xlabel("Time (hours)"); ax1.set_ylabel("Mass loss (%)")
ax1.set_xlim(0, 700); ax1.set_ylim(0, None)
ax1.legend(frameon=False, loc="upper left")

# (b) corrosion rate with diffusion-control onset markers
ax2.plot(df.time_h, df.disc_corrosion_rate_mm_per_yr, color=DISC_COLOR, lw=2, label="Disc")
ax2.plot(df.time_h, df.stent_corrosion_rate_mm_per_yr, color=STENT_COLOR, lw=2, label="Stent")
ax2.axvline(T_DISC, color=DISC_COLOR, ls="--", lw=1.3, label="Disc transition to\ndiffusion (40 h)")
ax2.axvline(T_STENT, color=STENT_COLOR, ls="--", lw=1.3, label="Stent transition to\ndiffusion (100 h)")
ax2.set_xlabel("Time (hours)"); ax2.set_ylabel("Corrosion rate (mm/yr)")
ax2.set_xlim(0, 700); ax2.set_ylim(0, 0.22)   # headroom for the two-row legend
ax2.legend(frameon=False, loc="upper right", labelspacing=0.6)

for ax, lab in ((ax1, "(a)"), (ax2, "(b)")):
    ax.text(-0.17 if ax is ax1 else -0.21, 1.04, lab, transform=ax.transAxes, fontsize=18, fontweight="bold", va="bottom")
    ax.tick_params(direction="out")

fig.tight_layout()
fig.savefig(HERE / "Fig6.png", dpi=400, bbox_inches="tight")
fig.savefig(HERE / "Fig6.pdf", bbox_inches="tight")
print("saved Fig6.png / Fig6.pdf")
