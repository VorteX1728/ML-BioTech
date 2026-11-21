"""Nested decision-threshold study. From the repository run python threshold_study.py > folds.csv."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold, train_test_split
from threadpoolctl import threadpool_limits

from model_comparison import SEEDS, estimator

GRID = (35, 40, 45, 50, 55, 60, 65)


def development():
    path = Path(__file__).resolve().parent / "data/train.csv"
    keys = pd.read_csv(path, usecols=["sample_id", "cohort", "label"],
                       dtype={"sample_id": str}).sort_values("sample_id")
    members, _ = train_test_split(keys.index.to_numpy(), test_size=.2, random_state=42,
                                  stratify=keys.cohort + "/" + keys.label.astype(str))
    selected = set(members)
    frame = pd.read_csv(path, skiprows=lambda i: i > 0 and i - 1 not in selected,
                        dtype={"sample_id": str})
    dev = frame.set_index("sample_id").loc[keys.loc[members, "sample_id"]].reset_index()
    assert len(dev) == 332 and dev.sample_id.is_unique
    return dev


def choose(y, scores):
    positive = y == 1
    cases = positive.sum()
    controls = len(y) - cases

    def rank(cut):
        calls = scores >= cut / 100
        # Exact integer numerator of balanced accuracy; denominator constant for this fold.
        correct = (calls & positive).sum() * controls + (~calls & ~positive).sum() * cases
        return correct, -abs(cut - 50), -cut

    return max(GRID, key=rank) / 100


def splits(frame, method, seed, count):
    if method == "LOCO":
        return LeaveOneGroupOut().split(frame, groups=frame.cohort)
    strata = frame.cohort + "/" + frame.label.astype(str)
    return StratifiedKFold(count, shuffle=True, random_state=seed).split(frame, strata)


def run():
    dev = development()
    taxa = sorted(c for c in dev if "mOTU" in c)
    rows = []
    schemes = [("CV", seed) for seed in SEEDS] + [("LOCO", 0)]
    for method, seed in schemes:
        for fold, (fit, val) in enumerate(splits(dev, method, seed, 5), 1):
            train, valid = dev.iloc[fit], dev.iloc[val]
            inner = list(splits(train, method, 42, 3))
            for name in ("LR", "ExtraTrees"):
                def predict(training, evaluation):
                    clf = estimator(name, 0, taxa).fit(training, training.label)
                    return clf.predict_proba(evaluation)[:, 1]

                oof = np.full(len(train), np.nan)
                for a, b in inner:
                    oof[b] = predict(train.iloc[a], train.iloc[b])
                assert np.isfinite(oof).all()
                cut = choose(train.label.to_numpy(), oof)
                scores = predict(train, valid)
                cases = valid.label.to_numpy() == 1
                for rule, threshold in (("fixed", .5), ("inner", cut)):
                    calls = scores >= threshold
                    sensitivity = calls[cases].mean()
                    specificity = (~calls[~cases]).mean()
                    rows.append(dict(method=method, seed=seed, fold=valid.cohort.iloc[0]
                                     if method == "LOCO" else str(fold), classifier=name,
                                     rule=rule, threshold=threshold, cases=cases.sum(),
                                     controls=(~cases).sum(), auc=roc_auc_score(cases, scores),
                                     ba=(sensitivity + specificity)/2, sensitivity=sensitivity,
                                     specificity=specificity))
    pd.DataFrame(rows).to_csv(sys.stdout, index=False, float_format="%.12g")


if __name__ == "__main__":
    with threadpool_limits(limits=1):
        run()
