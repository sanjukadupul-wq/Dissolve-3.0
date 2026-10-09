"""Supplementary figure: normalized log10 trajectories of kf, kd, kORR over the 32 BO evaluations of the initial run
(12 global, 8 phase-2, 4 dip, 8 phase-3; best = iteration 22, RMSE 0.0424 %). Data: optimization_runs_v4.csv"""
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE, "optimization_runs_v4.csv")

runs, k1, k2, korr, rmse = [], [], [], [], []
with open(CSV_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        runs.append(int(row["Run"]))
        k1.append(float(row["k1_kf"]))
        k2.append(float(row["k2_kd"]))
        korr.append(float(row["k_ORR"]))
        rmse.append(float(row["RMSE"]))

runs = np.array(runs)
k1 = np.array(k1)
k2 = np.array(k2)
korr = np.array(korr)
rmse = np.array(rmse)

def normalize(x):
    x = np.log10(x)   # parameters span 1-2 decades: normalise log10 values
    return (x - x.min()) / (x.max() - x.min())

k1_n = normalize(k1)
k2_n = normalize(k2)
korr_n = normalize(korr)

best_i = int(np.argmin(rmse))
best_run = runs[best_i]
print(f"Global optimum: run {best_run}, RMSE={rmse[best_i]:.6f}")

EXPLOIT_START = 21  # local-refinement phase (iterations 21-28)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
    'font.size': 13,
    'axes.labelsize': 15,
    'axes.titlesize': 17,
    'figure.dpi': 300,
    'savefig.dpi': 300,
})

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.set_facecolor("#F2F3FB")

ax.axvspan(EXPLOIT_START, runs.max(), color="#F5DFA0", alpha=0.6, zorder=0, label="Local-refinement phase")
ax.axvline(best_run, color="black", linestyle="--", linewidth=1.3, zorder=1)

ax.plot(runs, k1_n, "-o", color="#1f6fd6", markeredgecolor="black", markeredgewidth=0.6,
        label=r"$k_f$ (film precipitation)", zorder=3)
ax.plot(runs, k2_n, "-s", color="#2ca02c", markeredgecolor="black", markeredgewidth=0.6,
        label=r"$k_d$ (Cl$^-$-driven dissolution)", zorder=3)
ax.plot(runs, korr_n, "-^", color="#ff7f0e", markeredgecolor="black", markeredgewidth=0.6,
        label=r"$k_{\mathrm{ORR}}$ (oxygen reduction)", zorder=3)

for series, color in [(k1_n, "#1f6fd6"), (k2_n, "#2ca02c"), (korr_n, "#ff7f0e")]:
    ax.scatter([best_run], [series[best_i]], marker="*", s=350, color="gold",
               edgecolor="black", linewidth=1.0, zorder=5)

ax.annotate(f"Global optimum\n(iter. {best_run})",
            xy=(best_run, 1.03), xytext=(best_run - 6, 1.10),
            fontsize=12, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.3))

ax.set_xlabel("Optimization iteration")
ax.set_ylabel("Normalized log$_{10}$ parameter value")
ax.set_title("Bayesian optimization parameter convergence", pad=45)
ax.set_xlim(runs.min(), runs.max())
ax.set_ylim(-0.08, 1.28)

handles, labels = ax.get_legend_handles_labels()
order = [1, 2, 3, 0]  # kf, kd, kORR, Exploitation phase -- 2x2 legend like the reference
ax.legend([handles[i] for i in order], [labels[i] for i in order],
          loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2,
          frameon=True, fontsize=12)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)

out_base = os.path.join(BASE, "FigS_BO_Parameter_Trajectories_v4")
plt.savefig(out_base + ".pdf", format="pdf", bbox_inches="tight")
plt.savefig(out_base + ".png", format="png", bbox_inches="tight", dpi=300)
print(f"Saved {out_base}.pdf / .png")
