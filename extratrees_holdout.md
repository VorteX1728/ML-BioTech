# Frozen ExtraTrees submission

The model uses all 849 microbial features, age, BMI, sequencing depth, gender and cohort. The trees use 160 estimators, square-root feature sampling, minimum leaf size 2, seed 42 and one worker (scikit-learn 1.6.1). Microbial fractions are median-imputed, converted to presence at abundance > 0, and standardized. Numeric metadata are median-imputed and standardized. Categorical metadata use mode imputation and one-hot encoding with unknown categories ignored. A case probability ≥ 0.50 produces label 1.

## Final evaluation

After sorting sample IDs, the original seed-42 split stratified by cohort and label yields 332 development subjects (165 cases, 167 controls) and 83 holdout subjects (40 cases, 43 controls). One ExtraTrees pipeline was fitted exclusively on development data and scored once on holdout. The earlier logistic regression results are included as recorded. Threshold, features and model settings were frozen before evaluation.

| Model | Probability ROC AUC | Binary balanced accuracy | Sensitivity | Specificity | TN | FP | FN | TP | Predicted 0 / 1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ExtraTrees | 0.7494 | 0.6622 | 0.6500 | 0.6744 | 29 | 14 | 14 | 26 | 43 / 40 |
| Logistic regression | 0.7878 | 0.7355 | 0.7500 | 0.7209 | 31 | 12 | 10 | 30 | 41 / 42 |

### ExtraTrees by cohort

| Cohort | N | Cases / controls | ROC AUC | Binary BA | Sensitivity | Specificity | TN / FP / FN / TP |
|---|---:|---:|---:|---:|---:|---:|---:|
| AUS | 16 | 6 / 10 | 0.8167 | 0.6500 | 0.5000 | 0.8000 | 8 / 2 / 3 / 3 |
| CHI | 19 | 11 / 8 | 0.8295 | 0.7841 | 0.8182 | 0.7500 | 6 / 2 / 2 / 9 |
| FRA | 16 | 7 / 9 | 0.6508 | 0.5476 | 0.4286 | 0.6667 | 6 / 3 / 4 / 3 |
| GER | 18 | 9 / 9 | 0.8642 | 0.7222 | 0.6667 | 0.7778 | 7 / 2 / 3 / 6 |
| USA | 14 | 7 / 7 | 0.4490 | 0.5000 | 0.7143 | 0.2857 | 2 / 5 / 2 / 5 |

Each subgroup has only 6–11 subjects per class. For USA one subject changes sensitivity or specificity by 14.3 percentage points. Holdout results favored the logistic reference. The submitted candidate follows the prior development decision. Its leaderboard score is unknown.

## Production fit and verification

The standalone notebook fits a fresh pipeline on all 415 labeled rows. Only transformation and inference are applied to the 160 test rows. Two independent fresh-kernel runs in the baseline environment produced byte-identical CSV output. Each run verified all 160 original IDs, original order, unique IDs, zero missing values, exact columns and integer labels. The exported CSV also matched the saved notebook's final output after reopening it. The displayed HTML and plain-text representations matched the complete table. There are 89 zeros and 71 ones.

Use the supplied train.csv and test.csv together beside the notebook, under data/, or under CU_hackathon_participants/. The notebook reads only these two files and writes no intermediate files. No upload was performed.
