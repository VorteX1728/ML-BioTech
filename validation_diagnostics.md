# Logistic baseline diagnostics

Run `python validation_diagnostics.py` from the baseline environment to emit all fold metrics as CSV. Only data/train.csv is read. Fixed presence features, L2 C=0.01 and decision threshold 0.5. All learned transforms fit on each training split. Cohort and label jointly stratify the original 332/83 split and repeated development folds. Unknown categories are ignored.

## Development ROC AUC

Each row is one paired validation fold. LOCO holds out a whole cohort. Summary SD is the sample SD across folds; repeated folds share samples.

| Method | Seed | Fold | Metadata | Microbial | Combined | Without cohort |
|---|---:|---|---:|---:|---:|---:|
| repeated | 42 | 1 | 0.5998 | 0.9144 | 0.9171 | 0.9162 |
| repeated | 42 | 2 | 0.6907 | 0.9144 | 0.9153 | 0.9153 |
| repeated | 42 | 3 | 0.5138 | 0.8557 | 0.8548 | 0.8548 |
| repeated | 42 | 4 | 0.6244 | 0.8788 | 0.8806 | 0.8815 |
| repeated | 42 | 5 | 0.6094 | 0.8456 | 0.8474 | 0.8465 |
| repeated | 17 | 1 | 0.6337 | 0.9118 | 0.9091 | 0.9100 |
| repeated | 17 | 2 | 0.6301 | 0.8957 | 0.9002 | 0.9002 |
| repeated | 17 | 3 | 0.8162 | 0.8768 | 0.8768 | 0.8768 |
| repeated | 17 | 4 | 0.5895 | 0.9210 | 0.9229 | 0.9238 |
| repeated | 17 | 5 | 0.5165 | 0.8805 | 0.8768 | 0.8778 |
| repeated | 73 | 1 | 0.6881 | 0.8904 | 0.8913 | 0.8913 |
| repeated | 73 | 2 | 0.6783 | 0.9064 | 0.9091 | 0.9082 |
| repeated | 73 | 3 | 0.5423 | 0.9320 | 0.9320 | 0.9320 |
| repeated | 73 | 4 | 0.5207 | 0.8889 | 0.8861 | 0.8871 |
| repeated | 73 | 5 | 0.6921 | 0.8465 | 0.8511 | 0.8502 |
| repeated | 101 | 1 | 0.6105 | 0.8565 | 0.8574 | 0.8574 |
| repeated | 101 | 2 | 0.6809 | 0.8271 | 0.8333 | 0.8342 |
| repeated | 101 | 3 | 0.6241 | 0.9164 | 0.9228 | 0.9219 |
| repeated | 101 | 4 | 0.6731 | 0.9330 | 0.9330 | 0.9330 |
| repeated | 101 | 5 | 0.6066 | 0.9191 | 0.9182 | 0.9182 |
| repeated | 211 | 1 | 0.6132 | 0.9011 | 0.8975 | 0.8966 |
| repeated | 211 | 2 | 0.5722 | 0.8699 | 0.8690 | 0.8681 |
| repeated | 211 | 3 | 0.5974 | 0.9614 | 0.9614 | 0.9623 |
| repeated | 211 | 4 | 0.7172 | 0.8310 | 0.8320 | 0.8320 |
| repeated | 211 | 5 | 0.6553 | 0.9017 | 0.9026 | 0.9026 |
| LOCO | — | AUS | 0.6126 | 0.8232 | 0.8242 | 0.8232 |
| LOCO | — | CHI | 0.4165 | 0.8098 | 0.8040 | 0.8040 |
| LOCO | — | FRA | 0.5088 | 0.7696 | 0.7765 | 0.7765 |
| LOCO | — | GER | 0.5933 | 0.9294 | 0.9261 | 0.9261 |
| LOCO | — | USA | 0.5415 | 0.8020 | 0.8033 | 0.8020 |
| repeated |  | mean | 0.6278 | 0.8910 | 0.8919 | 0.8919 |
| repeated |  | SD | 0.0693 | 0.0340 | 0.0336 | 0.0337 |
| LOCO |  | mean | 0.5345 | 0.8268 | 0.8268 | 0.8263 |
| LOCO |  | SD | 0.0778 | 0.0607 | 0.0580 | 0.0582 |

## Selected model by cohort

Scores are case probabilities. FP and FN use the fixed threshold.

| Method | Cohort | N | Controls | Cases | AUC | P10 | Median | P90 | Control mean | Case mean | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LOCO | AUS | 63 | 38 | 25 | 0.8242 | 0.1126 | 0.3374 | 0.8703 | 0.2905 | 0.5972 | 6 | 12 |
| LOCO | CHI | 80 | 33 | 47 | 0.8040 | 0.2040 | 0.5074 | 0.9317 | 0.3819 | 0.6614 | 9 | 15 |
| LOCO | FRA | 64 | 34 | 30 | 0.7765 | 0.0951 | 0.5644 | 0.8915 | 0.3827 | 0.6618 | 14 | 7 |
| LOCO | GER | 69 | 35 | 34 | 0.9261 | 0.0922 | 0.3704 | 0.8494 | 0.2165 | 0.6306 | 2 | 12 |
| LOCO | USA | 56 | 27 | 29 | 0.8033 | 0.1776 | 0.5187 | 0.8800 | 0.3510 | 0.6296 | 7 | 7 |
| holdout | all | 83 | 43 | 40 | 0.7878 | 0.1080 | 0.5103 | 0.8908 | 0.3728 | 0.6391 | 12 | 10 |
| holdout | AUS | 16 | 10 | 6 | 0.8667 | 0.1113 | 0.4325 | 0.8055 | 0.3282 | 0.6869 | 3 | 1 |
| holdout | CHI | 19 | 8 | 11 | 0.7955 | 0.3023 | 0.5887 | 0.8851 | 0.4729 | 0.7165 | 3 | 0 |
| holdout | FRA | 16 | 9 | 7 | 0.7143 | 0.0586 | 0.4528 | 0.7672 | 0.3174 | 0.5624 | 3 | 3 |
| holdout | GER | 18 | 9 | 9 | 0.9136 | 0.0815 | 0.5248 | 0.9078 | 0.2634 | 0.6851 | 1 | 1 |
| holdout | USA | 14 | 7 | 7 | 0.4490 | 0.3944 | 0.4304 | 0.8604 | 0.5338 | 0.4940 | 2 | 5 |

Metadata improved 14/25 paired repeated folds and tied in four. Combined and microbial-only LOCO means agree to four decimals. Including cohort tied in 11 repeated folds, won seven and lost seven. USA had 5/7 missed cases on the holdout but AUC 0.8033 on 56 USA development samples in LOCO. The two estimates involve different subjects and training sets. Prior selection among 24 configurations and split variability can contribute to the gap; these data cannot identify a single cause.
