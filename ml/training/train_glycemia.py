"""Screening models for undiagnosed dysglycemia from non-glycemic inputs.

Population : adults 20+ with no prior diabetes diagnosis (DIQ010 != 1) and a measured HbA1c.
Targets    : diabetes_range   = HbA1c >= 6.5      (undiagnosed diabetes)
             prediabetes_plus = HbA1c >= 5.7      (prediabetes or worse)
Features   : age, sex, BMI, waist, systolic/diastolic BP, total cholesterol, HDL.
             NO glucose/HbA1c/diagnosis/ID columns (enforced by leakage.assert_no_leakage).
Validation : train on cycles F,G,H,I,P (2009-Mar 2020); test on L (2021-23), a later cycle.
Baselines  : age-only, and age+BMI+waist logistic regression (to show the model earns its keep).

Run:  venv/Scripts/python ml/training/train_glycemia.py
"""
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parent))
from leakage import assert_no_leakage, univariate_auc_scan  # noqa: E402
from nhanes_dataset import ROOT, build_dataset  # noqa: E402

FEATURES = ["age", "sex", "bmi", "waist_cm", "sbp", "dbp", "total_chol", "hdl"]
TARGETS = {"diabetes_range": 6.5, "prediabetes_plus": 5.7}
TRAIN_CYCLES, TEST_CYCLES = ["F", "G", "H", "I", "P"], ["L"]
SEED = 42


def prepare() -> pd.DataFrame:
    df = build_dataset()
    df = df[df["diabetes_dx"] != 1].dropna(subset=["hba1c"])  # exclude diagnosed diabetes
    for name, cut in TARGETS.items():
        df[name] = (df["hba1c"] >= cut).astype(int)
    return df.reset_index(drop=True)


def boot_ci(y, p, fn, n=300, seed=SEED):
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if len(set(y[i])) == 2:
            vals.append(fn(y[i], p[i]))
    return [round(float(np.percentile(vals, q)), 3) for q in (2.5, 97.5)]


def evaluate(y, p, w=None) -> dict:
    y = np.asarray(y)
    p = np.asarray(p)
    out = {
        "n": int(len(y)), "prevalence": round(float(y.mean()), 4),
        "auroc": round(float(roc_auc_score(y, p)), 3),
        "auroc_ci95": boot_ci(y, p, roc_auc_score),
        "auprc": round(float(average_precision_score(y, p)), 3),
        "brier": round(float(brier_score_loss(y, p)), 4),
        "mean_predicted": round(float(p.mean()), 4),
    }
    if w is not None:
        out["auroc_survey_weighted"] = round(float(roc_auc_score(y, p, sample_weight=w)), 3)
    return out


def sens_spec(y, p, thr):
    y = np.asarray(y)
    pred = np.asarray(p) >= thr
    return (round(float((pred & (y == 1)).sum() / (y == 1).sum()), 3),
            round(float((~pred & (y == 0)).sum() / (y == 0).sum()), 3))


def make_models():
    gbm = CalibratedClassifierCV(
        HistGradientBoostingClassifier(max_depth=4, learning_rate=0.06, max_iter=250,
                                       l2_regularization=1.0, random_state=SEED),
        method="isotonic", cv=5)
    return gbm


def baseline(cols):
    pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                         LogisticRegression(max_iter=1000))
    return pipe, cols


def main() -> int:
    df = prepare()
    assert_no_leakage(FEATURES)
    train = df[df["cycle"].isin(TRAIN_CYCLES)]
    test = df[df["cycle"].isin(TEST_CYCLES)]
    print(f"train n={len(train)} (cycles {TRAIN_CYCLES}), test n={len(test)} (cycles {TEST_CYCLES})")

    report: dict = {"features": FEATURES, "train_cycles": TRAIN_CYCLES, "test_cycles": TEST_CYCLES,
                    "population": "adults 20+, no prior diabetes diagnosis, HbA1c measured",
                    "targets": {k: f"HbA1c >= {v}" for k, v in TARGETS.items()}, "results": {}}
    (ROOT / "models").mkdir(exist_ok=True)

    for target in TARGETS:
        scan = univariate_auc_scan(train, FEATURES, target)  # raises on a leak
        gbm = make_models().fit(train[FEATURES], train[target])
        p = gbm.predict_proba(test[FEATURES])[:, 1]
        res = {"model": evaluate(test[target], p, test["mec_weight"]),
               "single_feature_auroc_train": scan}

        # operating point: threshold giving ~85% sensitivity on TRAIN (out-of-fold not needed: calibrated probs)
        ptr = gbm.predict_proba(train[FEATURES])[:, 1]
        thr = float(np.quantile(ptr[train[target] == 1], 0.15))
        res["operating_point"] = {"threshold": round(thr, 4),
                                  "test_sensitivity_specificity": sens_spec(test[target], p, thr)}

        for name, cols in {"age_only": ["age"], "age_bmi_waist_logreg": ["age", "bmi", "waist_cm"]}.items():
            pipe, c = baseline(cols)
            pipe.fit(train[c], train[target])
            res[f"baseline_{name}"] = evaluate(test[target], pipe.predict_proba(test[c])[:, 1])

        # leave-one-cycle-out stability over the training cycles
        loco = {}
        for held in TRAIN_CYCLES:
            tr, te = train[train["cycle"] != held], train[train["cycle"] == held]
            m = make_models().fit(tr[FEATURES], tr[target])
            loco[held] = round(float(roc_auc_score(te[target], m.predict_proba(te[FEATURES])[:, 1])), 3)
        res["leave_one_cycle_out_auroc"] = loco

        # subgroup performance on the test cycle
        sub = {}
        groups = {"sex": test["sex"].map({1: "male", 2: "female"}),
                  "age_band": pd.cut(test["age"], [19, 39, 59, 120], labels=["20-39", "40-59", "60+"]),
                  "race": test["race"].map({1: "Mexican American", 2: "Other Hispanic",
                                            3: "Non-Hispanic White", 4: "Non-Hispanic Black",
                                            5: "Other/multiracial"})}
        for gname, g in groups.items():
            for lvl in g.dropna().unique():
                m = (g == lvl).to_numpy()
                yy = test[target].to_numpy()[m]
                if len(yy) >= 100 and len(set(yy)) == 2:
                    sub[f"{gname}={lvl}"] = {"n": int(m.sum()), "events": int(yy.sum()),
                                             "auroc": round(float(roc_auc_score(yy, p[m])), 3)}
        res["subgroups_test"] = sub

        joblib.dump({"model": gbm, "features": FEATURES, "target": target,
                     "threshold": thr, "trained_cycles": TRAIN_CYCLES},
                    ROOT / "models" / f"glycemia_{target}.joblib")
        report["results"][target] = res
        m = res["model"]
        print(f"\n[{target}] test AUROC {m['auroc']} {m['auroc_ci95']}  AUPRC {m['auprc']}  "
              f"Brier {m['brier']}  prev {m['prevalence']}")
        print("  baselines AUROC: age-only", res["baseline_age_only"]["auroc"],
              "| age+BMI+waist", res["baseline_age_bmi_waist_logreg"]["auroc"])
        print("  sens/spec @ train 85%-sens threshold:", res["operating_point"]["test_sensitivity_specificity"])
        print("  leave-one-cycle-out:", loco)

    out = ROOT / "docs" / "model_cards"
    out.mkdir(parents=True, exist_ok=True)
    (out / "glycemia_metrics.json").write_text(json.dumps(report, indent=2))
    print("\nWrote", out / "glycemia_metrics.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
