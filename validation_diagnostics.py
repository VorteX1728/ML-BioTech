"""Run paired baseline diagnostics using only the labeled competition data."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parent
GROUPS = ("metadata", "microbial", "combined", "without_cohort")
SEEDS = (42, 17, 73, 101, 211)


def presence(x):
    return (x > 0).astype(float)


def model(group, taxa):
    blocks = []
    if group != "metadata":
        blocks.append(("micro", make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True),
                       FunctionTransformer(presence), StandardScaler()), taxa))
    if group != "microbial":
        categories = ["gender"] if group == "without_cohort" else ["gender", "cohort"]
        blocks.append(("numeric", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
                       ["age", "bmi", "library_size"]))
        blocks.append(("category", make_pipeline(SimpleImputer(strategy="most_frequent"),
                       OneHotEncoder(handle_unknown="ignore")), categories))
    return make_pipeline(ColumnTransformer(blocks),
                         LogisticRegression(C=0.01, solver="liblinear", max_iter=2000, random_state=42))


def describe(y, scores):
    tn, fp, fn, tp = confusion_matrix(y, scores >= 0.5, labels=[0, 1]).ravel()
    return dict(n=len(y), controls=tn+fp, cases=tp+fn, auc=roc_auc_score(y, scores),
                mean=scores.mean(), sd=scores.std(ddof=1), q10=np.quantile(scores, .1),
                median=np.median(scores), q90=np.quantile(scores, .9),
                control_mean=scores[y == 0].mean(), case_mean=scores[y == 1].mean(),
                tn=tn, fp=fp, fn=fn, tp=tp)


def main():
    data = pd.read_csv(ROOT / "data/train.csv", dtype={"sample_id": str}).sort_values("sample_id")
    strata = data.cohort + "/" + data.label.astype(str)
    dev, hold = train_test_split(np.arange(len(data)), test_size=.2, stratify=strata, random_state=42)
    taxa = sorted(c for c in data if "mOTU" in c)
    assert len(dev) == 332 and len(hold) == 83 and data.sample_id.is_unique

    def predict(group, fit, val):
        estimator = model(group, taxa).fit(data.iloc[fit], data.label.iloc[fit])
        return estimator.predict_proba(data.iloc[val])[:, 1]

    def evaluate(method, seed, fold, fit, val):
        for group in GROUPS:
            yield dict(method=method, seed=seed, fold=fold, group=group,
                       **describe(data.label.iloc[val].to_numpy(), predict(group, fit, val)))

    rows = []
    for seed in SEEDS:
        splits = StratifiedKFold(5, shuffle=True, random_state=seed)
        for fold, (fit, val) in enumerate(splits.split(dev, strata.iloc[dev]), 1):
            rows.extend(evaluate("repeated", seed, str(fold), dev[fit], dev[val]))
    for cohort in sorted(data.cohort.iloc[dev].unique()):
        mask = data.cohort.iloc[dev].to_numpy() == cohort
        rows.extend(evaluate("LOCO", 0, cohort, dev[~mask], dev[mask]))
    scores = predict("combined", dev, hold)
    hold_data = data.iloc[hold].assign(score=scores)
    for name, frame in [("all", hold_data), *hold_data.groupby("cohort")]:
        rows.append(dict(method="holdout", seed=42, fold=name, group="combined",
                         **describe(frame.label.to_numpy(), frame.score.to_numpy())))
    results = pd.DataFrame(rows)
    original = results.query("method == 'repeated' and seed == 42 and group == 'combined'")
    assert round(original.auc.mean(), 4) == .8831
    assert round(roc_auc_score(hold_data.label, scores), 4) == .7878
    print(results.to_csv(index=False, float_format="%.10f"), end="")


if __name__ == "__main__":
    with threadpool_limits(limits=1):
        main()
