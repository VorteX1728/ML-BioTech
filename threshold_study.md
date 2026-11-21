# Decision thresholds for the microbiome baseline

**Submission recommendation.** Use the original ExtraTrees configuration with abundance > 0 and classify a sample as positive when the case probability is at least 0.50. Fixed ExtraTrees scored 0.8115 repeated-CV balanced accuracy and 0.7576 macro LOCO balanced accuracy. For binary outputs, balanced accuracy equals leaderboard ROC AUC whenever both classes are present.

**Measured trade-off.** ExtraTrees at 0.50 beat fixed logistic regression by 0.0362 across cohorts (four wins, one loss), but by only 0.0027 in repeated CV (11 wins, two ties, 12 losses). The cross-cohort gains were largest in AUS, GER and CHI; USA was nearly tied and FRA favored logistic regression. Inner cutoff selection reduced ExtraTrees balanced accuracy by 0.0131 in repeated CV and 0.0064 in LOCO. For logistic regression, the 0.0110 mean LOCO gain came from AUS alone. Across the other four cohorts two tied and two declined. Tuning logistic regression generally increased sensitivity at the expense of specificity.

The classifiers were shortlisted using earlier development results. Nested evaluation isolates threshold selection, while model choice still uses these development subjects. The overlapping folds and five transfer cohorts limit precision about hidden-test performance.

Both classifiers use the original combined preprocessing and microbial abundance > 0. For split reconstruction alone the loader reads sample ID, cohort and label from train.csv. Feature rows are loaded only for the original 332 development subjects. Neither competition-test data nor holdout predictions enter this study. The source models and their fitted preprocessing are rebuilt for each training partition.

Outer CV uses five jointly cohort/label-stratified folds for each seed (42, 17, 73, 101, 211). Inner CV uses three shuffled folds stratified the same way (seed 42). Outer LOCO evaluates each cohort once. Inner LOCO generates one out-of-fold score per training subject by leaving out each remaining cohort in turn. In both schemes the threshold maximizes pooled inner balanced accuracy over 0.35 through 0.65 in steps of 0.05. Exact ties favor proximity to 0.50, then the lower cutoff. Both rules use the same outer model scores and predict class 1 at or above the threshold.

## Aggregate performance

Unweighted means across outer folds. SD is the sample SD across folds; LOCO weights each cohort equally. Sensitivity and specificity are fold means. All outer probabilities match the prior experiment in ROC AUC to numerical precision.

| Outer scheme | Model | Rule | Probability AUC ± SD | Binary BA ± SD | Sensitivity | Specificity |
|---|---|---|---:|---:|---:|---:|
| CV | ExtraTrees | fixed | 0.8909 ± 0.0411 | 0.8115 ± 0.0429 | 0.7699 | 0.8531 |
| CV | ExtraTrees | inner | 0.8909 ± 0.0411 | 0.7984 ± 0.0457 | 0.7578 | 0.8391 |
| CV | LR | fixed | 0.8919 ± 0.0336 | 0.8088 ± 0.0432 | 0.7813 | 0.8363 |
| CV | LR | inner | 0.8919 ± 0.0336 | 0.8032 ± 0.0462 | 0.8186 | 0.7878 |
| LOCO | ExtraTrees | fixed | 0.8606 ± 0.0556 | 0.7576 ± 0.0786 | 0.6985 | 0.8168 |
| LOCO | ExtraTrees | inner | 0.8606 ± 0.0556 | 0.7512 ± 0.0923 | 0.7462 | 0.7562 |
| LOCO | LR | fixed | 0.8268 ± 0.0580 | 0.7214 ± 0.0502 | 0.6746 | 0.7682 |
| LOCO | LR | inner | 0.8268 ± 0.0580 | 0.7325 ± 0.0453 | 0.7455 | 0.7195 |

## Paired differences

Wins / ties / losses count positive / zero / negative differences in outer-fold binary BA. The 25 CV folds reuse the same subjects.

| Comparison | Scheme | Mean difference | Wins / ties / losses |
|---|---|---:|---:|
| LR inner vs fixed | CV | -0.0056 | 7 / 10 / 8 |
| ExtraTrees inner vs fixed | CV | -0.0131 | 2 / 14 / 9 |
| ExtraTrees vs LR, fixed | CV | +0.0027 | 11 / 2 / 12 |
| ExtraTrees vs LR, inner | CV | -0.0048 | 10 / 0 / 15 |
| LR inner vs fixed | LOCO | +0.0110 | 1 / 2 / 2 |
| ExtraTrees inner vs fixed | LOCO | -0.0064 | 1 / 2 / 2 |
| ExtraTrees vs LR, fixed | LOCO | +0.0362 | 4 / 0 / 1 |
| ExtraTrees vs LR, inner | LOCO | +0.0187 | 3 / 0 / 2 |

## Outer folds

Paired columns give fixed 0.50 / inner-selected results. Cases and controls are validation counts. AUC uses the shared continuous scores.

| Scheme | Seed | Fold | Model | Cases / controls | Inner cutoff | AUC | BA | Sensitivity | Specificity |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| CV | 17 | 1 | ExtraTrees | 33 / 34 | 0.50 | 0.8913 | 0.8053 / 0.8053 | 0.7576 / 0.7576 | 0.8529 / 0.8529 |
| CV | 17 | 1 | LR | 33 / 34 | 0.40 | 0.9091 | 0.8351 / 0.7919 | 0.7879 / 0.8485 | 0.8824 / 0.7353 |
| CV | 17 | 2 | ExtraTrees | 33 / 34 | 0.40 | 0.8770 | 0.8057 / 0.7335 | 0.7879 / 0.8788 | 0.8235 / 0.5882 |
| CV | 17 | 2 | LR | 33 / 34 | 0.50 | 0.9002 | 0.8057 / 0.8057 | 0.7879 / 0.7879 | 0.8235 / 0.8235 |
| CV | 17 | 3 | ExtraTrees | 32 / 34 | 0.50 | 0.8732 | 0.7730 / 0.7730 | 0.7812 / 0.7812 | 0.7647 / 0.7647 |
| CV | 17 | 3 | LR | 32 / 34 | 0.55 | 0.8768 | 0.8493 / 0.8180 | 0.8750 / 0.8125 | 0.8235 / 0.8235 |
| CV | 17 | 4 | ExtraTrees | 33 / 33 | 0.55 | 0.9284 | 0.8182 / 0.7879 | 0.7576 / 0.6667 | 0.8788 / 0.9091 |
| CV | 17 | 4 | LR | 33 / 33 | 0.40 | 0.9229 | 0.8636 / 0.8333 | 0.8788 / 0.9091 | 0.8485 / 0.7576 |
| CV | 17 | 5 | ExtraTrees | 34 / 32 | 0.50 | 0.9145 | 0.8814 / 0.8814 | 0.7941 / 0.7941 | 0.9688 / 0.9688 |
| CV | 17 | 5 | LR | 34 / 32 | 0.45 | 0.8768 | 0.7914 / 0.8033 | 0.6765 / 0.7941 | 0.9062 / 0.8125 |
| CV | 42 | 1 | ExtraTrees | 33 / 34 | 0.55 | 0.9376 | 0.8351 / 0.8191 | 0.7879 / 0.6970 | 0.8824 / 0.9412 |
| CV | 42 | 1 | LR | 33 / 34 | 0.40 | 0.9171 | 0.8053 / 0.8066 | 0.7576 / 0.8485 | 0.8529 / 0.7647 |
| CV | 42 | 2 | ExtraTrees | 33 / 34 | 0.50 | 0.9149 | 0.8351 / 0.8351 | 0.7879 / 0.7879 | 0.8824 / 0.8824 |
| CV | 42 | 2 | LR | 33 / 34 | 0.40 | 0.9153 | 0.8213 / 0.8516 | 0.8485 / 0.9091 | 0.7941 / 0.7941 |
| CV | 42 | 3 | ExtraTrees | 32 / 34 | 0.45 | 0.8392 | 0.7574 / 0.6847 | 0.7500 / 0.7812 | 0.7647 / 0.5882 |
| CV | 42 | 3 | LR | 32 / 34 | 0.45 | 0.8548 | 0.7574 / 0.7592 | 0.7500 / 0.8125 | 0.7647 / 0.7059 |
| CV | 42 | 4 | ExtraTrees | 33 / 33 | 0.50 | 0.8577 | 0.8485 / 0.8485 | 0.7879 / 0.7879 | 0.9091 / 0.9091 |
| CV | 42 | 4 | LR | 33 / 33 | 0.45 | 0.8806 | 0.8333 / 0.8030 | 0.7879 / 0.7879 | 0.8788 / 0.8182 |
| CV | 42 | 5 | ExtraTrees | 34 / 32 | 0.50 | 0.7960 | 0.7583 / 0.7583 | 0.7353 / 0.7353 | 0.7812 / 0.7812 |
| CV | 42 | 5 | LR | 34 / 32 | 0.50 | 0.8474 | 0.7601 / 0.7601 | 0.6765 / 0.6765 | 0.8438 / 0.8438 |
| CV | 73 | 1 | ExtraTrees | 33 / 34 | 0.50 | 0.8868 | 0.8351 / 0.8351 | 0.7879 / 0.7879 | 0.8824 / 0.8824 |
| CV | 73 | 1 | LR | 33 / 34 | 0.50 | 0.8913 | 0.8507 / 0.8507 | 0.8485 / 0.8485 | 0.8529 / 0.8529 |
| CV | 73 | 2 | ExtraTrees | 33 / 34 | 0.55 | 0.9109 | 0.7910 / 0.8200 | 0.7879 / 0.7576 | 0.7941 / 0.8824 |
| CV | 73 | 2 | LR | 33 / 34 | 0.50 | 0.9091 | 0.8204 / 0.8204 | 0.7879 / 0.7879 | 0.8529 / 0.8529 |
| CV | 73 | 3 | ExtraTrees | 32 / 34 | 0.50 | 0.9154 | 0.8033 / 0.8033 | 0.8125 / 0.8125 | 0.7941 / 0.7941 |
| CV | 73 | 3 | LR | 32 / 34 | 0.45 | 0.9320 | 0.8346 / 0.8355 | 0.8750 / 0.9062 | 0.7941 / 0.7647 |
| CV | 73 | 4 | ExtraTrees | 33 / 33 | 0.55 | 0.8893 | 0.8636 / 0.8333 | 0.7879 / 0.6970 | 0.9394 / 0.9697 |
| CV | 73 | 4 | LR | 33 / 33 | 0.45 | 0.8861 | 0.7727 / 0.8182 | 0.6667 / 0.7576 | 0.8788 / 0.8788 |
| CV | 73 | 5 | ExtraTrees | 34 / 32 | 0.50 | 0.8764 | 0.7904 / 0.7904 | 0.7059 / 0.7059 | 0.8750 / 0.8750 |
| CV | 73 | 5 | LR | 34 / 32 | 0.40 | 0.8511 | 0.7436 / 0.6921 | 0.7059 / 0.8529 | 0.7812 / 0.5312 |
| CV | 101 | 1 | ExtraTrees | 33 / 34 | 0.50 | 0.8565 | 0.7758 / 0.7758 | 0.7576 / 0.7576 | 0.7941 / 0.7941 |
| CV | 101 | 1 | LR | 33 / 34 | 0.50 | 0.8574 | 0.7910 / 0.7910 | 0.7879 / 0.7879 | 0.7941 / 0.7941 |
| CV | 101 | 2 | ExtraTrees | 33 / 34 | 0.50 | 0.8275 | 0.7001 / 0.7001 | 0.6061 / 0.6061 | 0.7941 / 0.7941 |
| CV | 101 | 2 | LR | 33 / 34 | 0.45 | 0.8333 | 0.7313 / 0.7313 | 0.7273 / 0.7273 | 0.7353 / 0.7353 |
| CV | 101 | 3 | ExtraTrees | 32 / 34 | 0.55 | 0.9403 | 0.8631 / 0.7996 | 0.8438 / 0.6875 | 0.8824 / 0.9118 |
| CV | 101 | 3 | LR | 32 / 34 | 0.40 | 0.9228 | 0.8327 / 0.8373 | 0.8125 / 0.9688 | 0.8529 / 0.7059 |
| CV | 101 | 4 | ExtraTrees | 33 / 33 | 0.50 | 0.9256 | 0.8333 / 0.8333 | 0.7576 / 0.7576 | 0.9091 / 0.9091 |
| CV | 101 | 4 | LR | 33 / 33 | 0.50 | 0.9330 | 0.8939 / 0.8939 | 0.8182 / 0.8182 | 0.9697 / 0.9697 |
| CV | 101 | 5 | ExtraTrees | 34 / 32 | 0.45 | 0.9108 | 0.8649 / 0.8327 | 0.8235 / 0.8529 | 0.9062 / 0.8125 |
| CV | 101 | 5 | LR | 34 / 32 | 0.40 | 0.9182 | 0.8336 / 0.8162 | 0.8235 / 0.8824 | 0.8438 / 0.7500 |
| CV | 211 | 1 | ExtraTrees | 33 / 34 | 0.50 | 0.9242 | 0.8360 / 0.8360 | 0.8485 / 0.8485 | 0.8235 / 0.8235 |
| CV | 211 | 1 | LR | 33 / 34 | 0.50 | 0.8975 | 0.7758 / 0.7758 | 0.7576 / 0.7576 | 0.7941 / 0.7941 |
| CV | 211 | 2 | ExtraTrees | 33 / 34 | 0.45 | 0.9242 | 0.8494 / 0.8204 | 0.7576 / 0.7879 | 0.9412 / 0.8529 |
| CV | 211 | 2 | LR | 33 / 34 | 0.55 | 0.8690 | 0.7750 / 0.7442 | 0.6970 / 0.6061 | 0.8529 / 0.8824 |
| CV | 211 | 3 | ExtraTrees | 32 / 34 | 0.45 | 0.9421 | 0.8189 / 0.8061 | 0.8438 / 0.9062 | 0.7941 / 0.7059 |
| CV | 211 | 3 | LR | 32 / 34 | 0.50 | 0.9614 | 0.8658 / 0.8658 | 0.9375 / 0.9375 | 0.7941 / 0.7941 |
| CV | 211 | 4 | ExtraTrees | 33 / 33 | 0.50 | 0.8072 | 0.7576 / 0.7576 | 0.6061 / 0.6061 | 0.9091 / 0.9091 |
| CV | 211 | 4 | LR | 33 / 33 | 0.35 | 0.8320 | 0.7424 / 0.7424 | 0.6364 / 0.7879 | 0.8485 / 0.6970 |
| CV | 211 | 5 | ExtraTrees | 34 / 32 | 0.55 | 0.9049 | 0.7877 / 0.7904 | 0.7941 / 0.7059 | 0.7812 / 0.8750 |
| CV | 211 | 5 | LR | 34 / 32 | 0.45 | 0.9026 | 0.8336 / 0.8327 | 0.8235 / 0.8529 | 0.8438 / 0.8125 |
| LOCO | — | AUS | ExtraTrees | 25 / 38 | 0.45 | 0.8505 | 0.7542 / 0.7221 | 0.6400 / 0.7600 | 0.8684 / 0.6842 |
| LOCO | — | AUS | LR | 25 / 38 | 0.40 | 0.8242 | 0.6811 / 0.7416 | 0.5200 / 0.7200 | 0.8421 / 0.7632 |
| LOCO | — | CHI | ExtraTrees | 47 / 33 | 0.45 | 0.8949 | 0.7692 / 0.7966 | 0.6596 / 0.7447 | 0.8788 / 0.8485 |
| LOCO | — | CHI | LR | 47 / 33 | 0.45 | 0.8040 | 0.7041 / 0.7012 | 0.6809 / 0.7660 | 0.7273 / 0.6364 |
| LOCO | — | FRA | ExtraTrees | 30 / 34 | 0.45 | 0.7755 | 0.6461 / 0.6186 | 0.7333 / 0.7667 | 0.5588 / 0.4706 |
| LOCO | — | FRA | LR | 30 / 34 | 0.50 | 0.7765 | 0.6775 / 0.6775 | 0.7667 / 0.7667 | 0.5882 / 0.5882 |
| LOCO | — | GER | ExtraTrees | 34 / 35 | 0.50 | 0.9227 | 0.8676 / 0.8676 | 0.7353 / 0.7353 | 1.0000 / 1.0000 |
| LOCO | — | GER | LR | 34 / 35 | 0.50 | 0.9261 | 0.7950 / 0.7950 | 0.6471 / 0.6471 | 0.9429 / 0.9429 |
| LOCO | — | USA | ExtraTrees | 29 / 27 | 0.50 | 0.8595 | 0.7510 / 0.7510 | 0.7241 / 0.7241 | 0.7778 / 0.7778 |
| LOCO | — | USA | LR | 29 / 27 | 0.40 | 0.8033 | 0.7497 / 0.7471 | 0.7586 / 0.8276 | 0.7407 / 0.6667 |
