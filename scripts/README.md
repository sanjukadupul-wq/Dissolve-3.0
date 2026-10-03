# Scripts

- `BO/` Bayesian-optimization calibration (DoE generation, scoring, SLURM jobs, target data)
- `GSA/` Morris global sensitivity analysis
- `Uncertainty/` post-hoc uncertainty of the calibrated parameters

## BO

Scripts and target data for the joint (k_f, k_d, k_ORR) calibration on `disc_10x2_coarse_hmin0.5.mesh`
(simulation duration 336 h, matching the literature target).

| File | Role |
|---|---|
| `target_jmst2018.csv` | Literature mass-loss / corrosion-rate target (Liu et al., J. Mater. Sci. Technol. 2018, doi:10.1016/j.jmst.2018.05.005), 0-336 h |
| `generate_doe_global.py` | Phase 1: 12-point log10-uniform Latin hypercube over wide bounds (k_f 1-100, k_d 5-100, k_ORR 0.05-5), seed 7; writes `doe_design_global.csv` and a SLURM array script |
| `generate_verify_dip.py` | 4-point verification batch around the GP-predicted minimum (k_f~48.4, k_d~29.5, k_ORR~0.596) |
| `generate_doe_phase3_local.py` | Phase 3: 8-point local LHS (+/-2.5x) around the best point found (k_f 35.9058, k_d 27.1696, k_ORR 0.5075; RMSE 0.0424 %), seed 314 |
| `generate_doe.py` | Earlier local-bounds 8-point DoE around the original baseline (k_f 10, k_d 39.22, k_ORR 0.25), seed 42; superseded by the global-then-local plan |
| `score_global.py` | Scores completed Phase 1 runs (coarse-to-fine correction, RMSE vs target at 7 time points), fits a Matern-5/2 + white-noise GP in normalized log10 space, and proposes the Phase 2 batch by expected improvement (k_d stratified) |
| `run_bo_disc_joint_doe_global.slurm` | SLURM array (12 tasks) for Phase 1 global DoE, 336 h |
| `run_bo_disc_joint_phase2.slurm` | SLURM array (8 tasks) for Phase 2 EI-guided batch, 336 h |
| `run_bo_disc_joint_phase3_local.slurm` | SLURM array (8 tasks) for Phase 3 local refinement, 336 h |
| `run_bo_disc_joint_doe.slurm` | SLURM array (8 tasks) for the superseded local DoE, 672 h |
| `run_bo_disc_verify_dip.slurm` | SLURM array (4 tasks) for the dip-verification batch, 336 h |
| `run_bo_disc_phase4_fine_verify.slurm` | Phase 4: single run of the final point (k_f 35.9058, k_d 27.1696, k_ORR 0.5075) on the fine mesh `disc_10x2_hmin0.25.mesh`, 336 h, no bias correction |

Workflow: global DoE (12) -> `score_global.py` -> Phase 2 EI batch (8) -> dip verification (4) -> Phase 3 local DoE (8) -> Phase 4 fine-mesh verification (1).
Coarse evaluations: 12 + 8 + 4 + 8 = 32.
The SLURM scripts expect `dissolve.edp` and the mesh in `/fs04/uj24/zinc_simulation` and the design CSVs in `bo_disc_coarse_joint/`.
Not included: `score_combined.py` (fits the GP on the combined dataset) and the Phase 3 scoring script.

## Uncertainty

| File | Role |
|---|---|
| `compute_95ci.py` | Post-hoc 95% intervals from `final_all_evaluations.txt` (32 BO trials; no new simulations): GP-predicted RMSE interval at the best point (mu +/- 1.96 sigma) and a bootstrap interval on k_f, k_d, k_ORR (400 resamples, GP refit, posterior minimum over 20,000 candidates); writes `bo_bootstrap_minima.csv` |

## GSA

`GSA/run_gsa_full_v2.slurm`: Morris GSA (180 runs = 20 trajectories x 8 parameters, 168 h, coarse cylinder mesh) with the corrected chloride molar-unit physics; design from `morris_full_design.csv` (seed 7).

## Requirements

The scripts require numpy, scipy (`scipy.stats.qmc`), pandas and scikit-learn and write their outputs next to the script.
