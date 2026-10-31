"""Guards that stop a label's defining variables from leaking into features."""
import pandas as pd
from sklearn.metrics import roc_auc_score

# Anything that defines, or is a direct proxy of, a glycemia label, plus identifiers.
FORBIDDEN_FOR_GLYCEMIA = {
    "hba1c", "fasting_glucose", "diabetes_dx", "SEQN", "cycle", "cycle_year", "mec_weight",
}


class LeakageError(ValueError):
    pass


def assert_no_leakage(features: list[str], forbidden: set[str] = FORBIDDEN_FOR_GLYCEMIA) -> None:
    bad = sorted(set(features) & forbidden)
    if bad:
        raise LeakageError(f"Features contain label-defining or identifier columns: {bad}")


def univariate_auc_scan(df: pd.DataFrame, features: list[str], target: str,
                        warn_above: float = 0.85) -> dict[str, float]:
    """Single-feature AUROC. A very high value means the feature nearly *is* the label."""
    res = {}
    for f in features:
        sub = df[[f, target]].dropna()
        if sub[target].nunique() < 2:
            continue
        auc = roc_auc_score(sub[target], sub[f])
        res[f] = round(max(auc, 1 - auc), 3)
    suspicious = {k: v for k, v in res.items() if v >= warn_above}
    if suspicious:
        raise LeakageError(f"Suspiciously predictive single features (possible leak): {suspicious}")
    return res
