# Development classifier and detection-threshold comparison

All 332 development subjects and the original split are from train.csv. All nine configurations use the same microbial taxa and metadata (age, BMI, sequencing depth, gender, cohort). A detection is a relative abundance strictly above the listed cutoff. Median imputation and standardization, mode imputation and one-hot encoding are fitted within each training fold. Unknown categories are ignored.

L2 logistic regression uses C=0.01 and liblinear. RBF SVM uses C=1 and gamma=scale. ExtraTrees uses 160 trees, sqrt feature subsampling, minimum leaf size 2 and seed 42. SVM is scored by decision value and the other models by case probability. LightGBM and CatBoost were unavailable.

Five shuffled five-fold splits stratify jointly by cohort and label (seeds 42, 17, 73, 101, 211). LOCO holds out each entire development cohort. Rank gives equal weight to the 25-fold mean and the five-cohort macro mean. SD is the sample SD across folds. W/T/L compares each fold with LR at cutoff zero. Repeated folds share subjects.

| Rank | Model | Cutoff | CV mean ± SD | LOCO mean ± SD | Worst cohort | Rank score | CV W/T/L | LOCO W/T/L |
|---:|---|---:|---:|---:|---|---:|---|---|
| 1 | ExtraTrees | 0 | 0.8909 ± 0.0411 | 0.8606 ± 0.0556 | FRA 0.7755 | 0.8757 | 10/0/15 | 3/0/2 |
| 1 | ExtraTrees | 1e-05 | 0.8909 ± 0.0411 | 0.8606 ± 0.0556 | FRA 0.7755 | 0.8757 | 10/0/15 | 3/0/2 |
| 3 | LR | 0 | 0.8919 ± 0.0336 | 0.8268 ± 0.0580 | FRA 0.7765 | 0.8594 | 0/25/0 | 0/5/0 |
| 3 | LR | 1e-05 | 0.8919 ± 0.0336 | 0.8268 ± 0.0580 | FRA 0.7765 | 0.8594 | 0/25/0 | 0/5/0 |
| 5 | RBF | 0 | 0.8723 ± 0.0340 | 0.8124 ± 0.0635 | FRA 0.7167 | 0.8424 | 3/0/22 | 2/0/3 |
| 5 | RBF | 1e-05 | 0.8723 ± 0.0340 | 0.8124 ± 0.0635 | FRA 0.7167 | 0.8424 | 3/0/22 | 2/0/3 |
| 7 | ExtraTrees | 0.0001 | 0.8440 ± 0.0397 | 0.8259 ± 0.0424 | AUS 0.7858 | 0.8350 | 3/0/22 | 3/0/2 |
| 8 | LR | 0.0001 | 0.8337 ± 0.0288 | 0.7855 ± 0.0260 | AUS 0.7558 | 0.8096 | 1/0/24 | 1/1/3 |
| 9 | RBF | 0.0001 | 0.8195 ± 0.0400 | 0.7616 ± 0.0654 | AUS 0.7000 | 0.7905 | 1/0/24 | 1/0/4 |

## Transfer AUC by held-out cohort

| Model | Cutoff | AUS | CHI | FRA | GER | USA |
|---|---:|---:|---:|---:|---:|---:|
| ExtraTrees | 0 | 0.8505 | 0.8949 | 0.7755 | 0.9227 | 0.8595 |
| ExtraTrees | 1e-05 | 0.8505 | 0.8949 | 0.7755 | 0.9227 | 0.8595 |
| LR | 0 | 0.8242 | 0.8040 | 0.7765 | 0.9261 | 0.8033 |
| LR | 1e-05 | 0.8242 | 0.8040 | 0.7765 | 0.9261 | 0.8033 |
| RBF | 0 | 0.8021 | 0.8337 | 0.7167 | 0.8924 | 0.8174 |
| RBF | 1e-05 | 0.8021 | 0.8337 | 0.7167 | 0.8924 | 0.8174 |
| ExtraTrees | 0.0001 | 0.7858 | 0.8930 | 0.8029 | 0.8076 | 0.8404 |
| LR | 0.0001 | 0.7558 | 0.8169 | 0.7765 | 0.8084 | 0.7701 |
| RBF | 0.0001 | 0.7000 | 0.8491 | 0.7157 | 0.8126 | 0.7305 |

Run `python model_comparison.py` in the baseline environment to emit the full paired fold table. Rankings use development data and carry model-selection uncertainty.


## Interpretation and recommendation

Advance ExtraTrees at cutoff zero for cross-cohort generalization. Keep logistic regression as the reference for samples from the same study populations. ExtraTrees gained 0.0338 macro LOCO AUC and lost 0.0010 mean repeated CV AUC. Its transfer gains were concentrated in CHI (+0.0909), USA (+0.0562) and AUS (+0.0263), with small losses in GER (−0.0034) and FRA (−0.0010). It won 10 of 25 repeated folds. The weakest cohort saw no improvement. The five held-out populations limit precision about future cohorts.

The minimum positive development abundance was 0.00002189. Cutoffs 0 and 0.00001 produced identical matrices and share ranks. A cutoff of 0.0001 removed 17,183 of 79,147 positive entries (21.7%) and reduced both mean AUCs within each classifier. RBF SVM trailed logistic regression on both means at cutoff zero. The 83 reserved subjects entered only the original partition reconstruction via ID, cohort and label. No holdout or competition-test scores were calculated.
