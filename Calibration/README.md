# Calibration (Bayesian optimization) files

Scripts and target data for the joint (k_f, k_d, k_ORR) calibration on `disc_10x2_coarse_hmin0.5.mesh`
(simulation duration 336 h, matching the literature target).

| File | Role |
|---|---|
| `target_jmst2018.csv` | Literature mass-loss / corrosion-rate target (Liu et al., J. Mater. Sci. Technol. 2018, doi:10.1016/j.jmst.2018.05.005), 0-336 h |
| `generate_doe_global.py` | Phase 1: 12-point log10-uniform Latin hypercube over wide bounds (k_f 1-100, k_d 5-100, k_ORR 0.05-5), seed 7; writes `doe_design_global.csv` and a SLURM array script |
| `generate_verify_dip.py` | 4-point verification batch around the GP-predicted minimum (k_f~48.4, k_d~29.5, k_ORR~0.596) |
| `generate_doe_phase3_local.py` | Phase 3: 8-point local LHS (+/-2.5x) around the best point found (k_f 35.9058, k_d 27.1696, k_ORR 0.5075; RMSE 0.0424 %), seed 314 |
| `generate_doe.py` | Earlier local-bounds 8-point DoE around the original baseline (k_f 10, k_d 39.22, k_ORR 0.25), seed 42; superseded by the global-then-local plan |

The scripts require numpy and scipy (`scipy.stats.qmc`) and write their outputs next to the script.
