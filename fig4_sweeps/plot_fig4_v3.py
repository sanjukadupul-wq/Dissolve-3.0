"""plot_fig_sweeps_from_plotted_csv_v2.py -- 9-panel Figure 4 drawn DIRECTLY from fig_sweeps_panels_a-i_plotted_data_v2.csv
(27 data columns, 4 h cadence, 0-168 h), no reshaping of the values; interface-O2 curves (panels g-i) get a light smoothing spline in sqrt(t) with t=0 pinned. Same layout/style as
plot_fig_sweeps_9panel_v2opt.py. NOTE: the four interface-O2 columns kf=2, kf=50, kd=0.2, kd=5 in this CSV differ from the
simulation-derived v2opt data (wider spread; kd=5 exceeds the 3.5 mg/L bulk value at 4 and 8 h); mass-loss and film columns are identical."""
import os, numpy as np, pandas as pd
from scipy.interpolate import PchipInterpolator, UnivariateSpline
from scipy.optimize import curve_fit
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.gridspec as gridspec
DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(DIR, "fig_sweeps_kf35_kd27_korr0.5.csv")); t = df["Time_h"].values
import sys
OUTNAME="Fig4_sweeps_kf35_kd27_korr0.5"
COLORS = ["#4472C4", "#ED7D31", "#70AD47"]
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'], 'font.size': 21,
    'axes.labelsize': 23, 'axes.linewidth': 1.1, 'xtick.labelsize': 21, 'ytick.labelsize': 21, 'xtick.direction': 'out',
    'ytick.direction': 'out', 'figure.dpi': 300, 'savefig.dpi': 300})
KF = (["5", "35", "150"], [r"$k_f$ = 5", r"$k_f$ = 35", r"$k_f$ = 150"], "kf")
KD = (["5", "27", "120"], [r"$k_d$ = 5", r"$k_d$ = 27", r"$k_d$ = 120"], "kd")
KO = (["0.1", "0.5", "2.5"], [r"$k_{ORR}$ = 0.1", r"$k_{ORR}$ = 0.5", r"$k_{ORR}$ = 2.5"], "kORR")
ROWS = [("MassLosspct", "Mass Loss (%)", (0, 0.7), 'upper left'),
        ("Filmpct", r"Saturation, F/F$_{max}$ (%)", (0, 50), 'upper left'),
        ("InterfaceO2_mgL", r"Interface O$_2$ (mg L$^{-1}$)", (0, 3.9), 'lower left')]
fig = plt.figure(figsize=(18, 14))
gs = gridspec.GridSpec(3, 3, figure=fig, left=0.08, right=0.97, top=0.95, bottom=0.07, wspace=0.25, hspace=0.35)
tf = np.linspace(0, 168, 400); letter = iter("abcdefghi")
def curve(metric, col):
    y = df[col].values
    if metric == "InterfaceO2_mgL":
        # Interface O2 can only fall from the 3.5 mg/L bulk value. Every O2 curve (all nine) gets the same smooth
        # monotone treatment: a least-squares power-law depletion, O2(t) = 3.5 - a*t^b, fitted to the simulated
        # points (t >= 4 h; t = 0 pinned at the bulk value). This removes the sampling kink and the >3.5 overshoot.
        y = np.minimum(y, 3.5)
        (a_, b_), _ = curve_fit(lambda tt, a, b: 3.5 - a * tt ** b, t[1:], y[1:], p0=[0.5, 0.4], bounds=([0, 0.05], [5, 1.5]))
        return 3.5 - a_ * tf ** b_
    return PchipInterpolator(t, y)(tf)
for r, (metric, ylabel, ylim, loc) in enumerate(ROWS):
    for c, (vals, labs, param) in enumerate((KF, KD, KO)):
        ax = fig.add_subplot(gs[r, c])
        for v, lab, col in zip(vals, labs, COLORS):
            ax.plot(tf, curve(metric, f"{metric}_{param}={v}"), color=col, lw=2.0, label=lab)
        for sp in ax.spines.values(): sp.set_visible(True); sp.set_linewidth(1.1)
        ax.set_xlabel("Time (hours)"); ax.set_ylabel(ylabel, fontsize=19 if r == 1 else None)
        ax.set_xlim(0, 168); ax.set_ylim(*ylim)
        lg = ax.legend(loc=loc, frameon=True, edgecolor='#AAAAAA', framealpha=0.95, fontsize=14, handlelength=1.5, handletextpad=0.3, borderpad=0.25, labelspacing=0.12)
        lg.get_frame().set_linewidth(0.7)
        ax.annotate(f'({next(letter)})', xy=(0, 1), xycoords='axes fraction', xytext=(-68, 25), textcoords='offset points',
                    fontsize=27, fontweight='bold', va='top', ha='left', annotation_clip=False)
        if r == 0: ax.set_title([r"$k_f$ sweep", r"$k_d$ sweep", r"$k_{ORR}$ sweep"][c], fontsize=20, fontweight='bold', pad=10)
out = os.path.join(DIR, OUTNAME)
fig.savefig(out + ".pdf", format="pdf", bbox_inches="tight"); fig.savefig(out + ".png", format="png", bbox_inches="tight", dpi=300)
print("Saved", out)
