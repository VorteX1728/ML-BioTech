# ML-BioTech

## Reproduce the frozen ExtraTrees submission

Use Python 3.13.5 and the package versions listed below. Place the organizer-provided `train.csv` and `test.csv` in `data/`. Run [extratrees_submission.ipynb](extratrees_submission.ipynb) from a fresh Python kernel. Its final cell displays the ordered submission table. The frozen model uses 160 ExtraTrees with seed 42, detection at abundance > 0 and a decision threshold of 0.50. The [holdout report](extratrees_holdout.md) records its final evaluation.

From the repository root, reproduce the aggregate validation tables with `python validation_diagnostics.py`, `python model_comparison.py` and `python threshold_study.py`. Each script reads the supplied training CSV and prints fold-level results. Compare the output with the corresponding Markdown report in this directory.

## Logistic regression reference

The CU / Genotek baseline predicts colorectal cancer case status from microbial relative abundances and clinical/study metadata. Open `baseline.ipynb` in a Python kernel and run all cells from the repository root. Place the competition CSVs at `data/train.csv` and `data/test.csv`, or set `CU_DATA_DIR` to their directory. Data and executed outputs are ignored by Git.

For a two-run reproducibility check and CSV export, run `python verify_baseline.py` from an environment with the Python 3 kernel available. The verifier runs the notebook twice, checks the reported scores, compares every prediction and checks IDs against the test file, then writes `artifacts/predictions.csv` and `artifacts/baseline.executed.ipynb`. The notebook itself only reads the provided CSVs. Tested with Python 3.13.5, scikit-learn 1.6.1, NumPy 2.1.3, SciPy 1.15.3, pandas 2.2.3, threadpoolctl 3.5.0, nbclient 0.10.2, nbformat 5.10.4 and ipykernel 6.29.5.

## Baseline results

Seed 42, stratified by cohort and label. The development partition had 332 samples (167 controls, 165 cases). The holdout had 83 (43 controls, 40 cases). The notebook compares 24 configurations on identical five-fold development splits. All fitted transformations are inside the pipeline. The table shows the best mean development ROC AUC per feature set across the three values of C.

| Representation | Microbial only | With metadata |
| --- | ---: | ---: |
| Raw | 0.7237 | 0.7269 |
| Log | 0.8753 | 0.8757 |
| CLR | 0.8771 | 0.8766 |
| Presence/absence | 0.8818 | 0.8831 |

The selected L2 logistic regression used presence/absence, age, BMI, sequencing depth, gender and cohort with C = 0.01. Mean CV AUC was 0.8831 (fold SD 0.0327). Holdout AUC was 0.7878. Within-cohort holdout AUCs were AUS 0.8667 (n=16), CHI 0.7955 (n=19), FRA 0.7143 (n=16), GER 0.9136 (n=18) and USA 0.4490 (n=14). The holdout contains only known cohorts. Small subgroup counts and a single split limit comparisons. The test labels are private.

Next experiments: use leave-one-cohort-out evaluation on development data to measure transfer, and compare metadata-only and cohort-omitted baselines on common folds to assess the small observed gain from metadata. Keep the reported holdout out of tuning.
