"""Compare fixed classifiers and microbial detection limits on the baseline development set.

From this directory run: python model_comparison.py > model_comparison.csv
Requires validation_diagnostics.py from the same branch and the baseline environment.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.svm import SVC
from threadpoolctl import threadpool_limits

from validation_diagnostics import SEEDS, model

CUTOFFS = (0.0, 1e-5, 1e-4)
CLASSIFIERS = ("LR", "RBF", "ExtraTrees")


def detected(values, cutoff):
    return (values > cutoff).astype(float)


def estimator(name, cutoff, taxa):
    pipeline = model("combined", taxa)
    preprocessing = pipeline.steps[0][1]
    # Use the original fold-fitted median imputer, scaler and metadata branches.
    microbial = next(block for key, block, columns in preprocessing.transformers if key == "micro")
    microbial.set_params(functiontransformer__func=detected,
                         functiontransformer__kw_args={"cutoff": cutoff})
    if name == "RBF":
        pipeline.steps[-1] = ("svm", SVC(C=1, kernel="rbf", gamma="scale"))
    elif name == "ExtraTrees":
        pipeline.steps[-1] = ("trees", ExtraTreesClassifier(
            n_estimators=160, max_features="sqrt", min_samples_leaf=2, n_jobs=1, random_state=42))
    return pipeline


def main():
    train_file = Path(__file__).resolve().parent / "data" / "train.csv"
    data = pd.read_csv(train_file, dtype={"sample_id": str}).sort_values("sample_id")
    indices, _ = train_test_split(np.arange(len(data)), test_size=0.2, random_state=42,
                                  stratify=data.cohort + "/" + data.label.astype(str))
    dev = data.iloc[indices].reset_index(drop=True)
    del data
    assert len(dev) == 332 and dev.sample_id.is_unique
    strata = dev.cohort + "/" + dev.label.astype(str)
    taxa = sorted(column for column in dev if "mOTU" in column)
    folds = []
    for seed in SEEDS:
        cv = StratifiedKFold(5, shuffle=True, random_state=seed)
        for fold, (fit, val) in enumerate(cv.split(dev, strata), 1):
            folds.append(("CV", seed, str(fold), fit, val))
    for cohort in sorted(dev.cohort.unique()):
        mask = dev.cohort.to_numpy() == cohort
        folds.append(("LOCO", 0, cohort, np.flatnonzero(~mask), np.flatnonzero(mask)))

    rows = []
    for method, seed, fold, fit, val in folds:
        for cutoff in CUTOFFS:
            for name in CLASSIFIERS:
                clf = estimator(name, cutoff, taxa).fit(dev.iloc[fit], dev.label.iloc[fit])
                if name == "RBF":
                    score = clf.decision_function(dev.iloc[val])
                else:
                    score = clf.predict_proba(dev.iloc[val])[:, 1]
                rows.append(dict(method=method, seed=seed, fold=fold, n=len(val),
                                 cases=int(dev.label.iloc[val].sum()), classifier=name,
                                 cutoff=cutoff, auc=roc_auc_score(dev.label.iloc[val], score)))
    results = pd.DataFrame(rows)
    baseline = results.query("classifier == 'LR' and cutoff == 0")
    assert round(baseline.query("method == 'CV'").auc.mean(), 4) == .8919
    assert round(baseline.query("method == 'LOCO'").auc.mean(), 4) == .8268
    results.to_csv(sys.stdout, index=False, float_format="%.12g")


if __name__ == "__main__":
    with threadpool_limits(limits=1):
        main()
