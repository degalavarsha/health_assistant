"""Guideline-based interpretation of labs and vitals.

These are deterministic rules, not ML: where a clinical definition exists we
apply it directly and cite it. Units are US conventional (mg/dL, g/dL, cm, kg).

NOTE: thresholds below were written from the published guidelines named in
each `source` string. Before any public release, re-verify each against the
official text (see reports/Free health AI datasets and APIs.md).
"""
from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    NORMAL = "normal"
    BORDERLINE = "borderline"
    ABNORMAL = "abnormal"
    URGENT = "urgent"


@dataclass(frozen=True)
class Finding:
    id: str
    label: str
    value: float | str | None
    unit: str | None
    category: str
    severity: Severity
    message: str
    source: str


@dataclass
class Profile:
    sex: str | None = None  # "male" | "female"
    age_years: float | None = None
    pregnant: bool | None = None
    weight_kg: float | None = None
    height_cm: float | None = None
    waist_cm: float | None = None
    sbp: float | None = None
    dbp: float | None = None
    glucose_mgdl: float | None = None
    glucose_fasting: bool = True
    hba1c_pct: float | None = None
    total_chol_mgdl: float | None = None
    hdl_mgdl: float | None = None
    triglycerides_mgdl: float | None = None
    hemoglobin_gdl: float | None = None
    extra: dict = field(default_factory=dict)


def bmi_value(p: Profile) -> float | None:
    if p.weight_kg and p.height_cm:
        return round(p.weight_kg / (p.height_cm / 100) ** 2, 1)
    return None


# ---------------------------------------------------------------- anemia
_WHO_ANEMIA = "WHO. Haemoglobin concentrations for the diagnosis of anaemia (2011)"


def evaluate_anemia(p: Profile) -> Finding | None:
    if p.hemoglobin_gdl is None or p.sex not in ("male", "female"):
        return None
    hb = p.hemoglobin_gdl
    if p.sex == "male":
        cutoff, mild_low = 13.0, 11.0
    elif p.pregnant:
        cutoff, mild_low = 11.0, 10.0
    else:
        cutoff, mild_low = 12.0, 11.0
    if hb >= cutoff:
        return Finding("anemia", "Hemoglobin", hb, "g/dL", "No anemia", Severity.NORMAL,
                       "Hemoglobin is at or above the WHO threshold for your group.", _WHO_ANEMIA)
    if hb >= mild_low:
        cat, sev = "Mild anemia", Severity.ABNORMAL
    elif hb >= (7.0 if p.sex == "female" and p.pregnant else 8.0):
        cat, sev = "Moderate anemia", Severity.ABNORMAL
    else:
        cat, sev = "Severe anemia", Severity.URGENT
    return Finding("anemia", "Hemoglobin", hb, "g/dL", cat, sev,
                   "Hemoglobin is below the WHO threshold. A clinician should find the cause.",
                   _WHO_ANEMIA)


# ------------------------------------------------------------------- BMI
_WHO_BMI = "WHO. Obesity: preventing and managing the global epidemic (2000)"


def evaluate_bmi(p: Profile) -> Finding | None:
    b = bmi_value(p)
    if b is None:
        return None
    if b < 18.5:
        cat, sev = "Underweight", Severity.BORDERLINE
    elif b < 25:
        cat, sev = "Healthy weight", Severity.NORMAL
    elif b < 30:
        cat, sev = "Overweight", Severity.BORDERLINE
    elif b < 35:
        cat, sev = "Obesity class 1", Severity.ABNORMAL
    elif b < 40:
        cat, sev = "Obesity class 2", Severity.ABNORMAL
    else:
        cat, sev = "Obesity class 3", Severity.ABNORMAL
    return Finding("bmi", "Body mass index", b, "kg/m2", cat, sev,
                   "BMI is a screening measure and does not account for muscle mass or "
                   "ethnicity-specific risk.", _WHO_BMI)


# --------------------------------------------------------- blood pressure
_ACC_BP = "2017 ACC/AHA Guideline for High Blood Pressure in Adults"


def evaluate_blood_pressure(p: Profile) -> Finding | None:
    if p.sbp is None or p.dbp is None:
        return None
    s, d = p.sbp, p.dbp
    value = f"{s:g}/{d:g}"
    if s > 180 or d > 120:
        return Finding("blood_pressure", "Blood pressure", value, "mmHg",
                       "Hypertensive crisis range", Severity.URGENT,
                       "This is very high. Recheck after resting; if confirmed, or if you have "
                       "chest pain, shortness of breath, weakness or vision changes, seek "
                       "emergency care.", _ACC_BP)
    if s >= 140 or d >= 90:
        cat, sev = "Stage 2 hypertension range", Severity.ABNORMAL
    elif s >= 130 or d >= 80:
        cat, sev = "Stage 1 hypertension range", Severity.ABNORMAL
    elif s >= 120:
        cat, sev = "Elevated", Severity.BORDERLINE
    else:
        cat, sev = "Normal", Severity.NORMAL
    return Finding("blood_pressure", "Blood pressure", value, "mmHg", cat, sev,
                   "A diagnosis needs readings on two or more occasions.", _ACC_BP)


# --------------------------------------------------------------- glycemia
_ADA = "ADA Standards of Care in Diabetes (Classification and Diagnosis)"


def evaluate_glucose(p: Profile) -> Finding | None:
    if p.glucose_mgdl is None or not p.glucose_fasting:
        return None
    g = p.glucose_mgdl
    if g >= 126:
        cat, sev = "Diabetes range", Severity.ABNORMAL
    elif g >= 100:
        cat, sev = "Prediabetes range", Severity.BORDERLINE
    else:
        cat, sev = "Normal", Severity.NORMAL
    return Finding("fasting_glucose", "Fasting glucose", g, "mg/dL", cat, sev,
                   "Diagnosis requires confirmation with repeat testing.", _ADA)


def evaluate_hba1c(p: Profile) -> Finding | None:
    if p.hba1c_pct is None:
        return None
    a = p.hba1c_pct
    if a >= 6.5:
        cat, sev = "Diabetes range", Severity.ABNORMAL
    elif a >= 5.7:
        cat, sev = "Prediabetes range", Severity.BORDERLINE
    else:
        cat, sev = "Normal", Severity.NORMAL
    return Finding("hba1c", "HbA1c", a, "%", cat, sev,
                   "Diagnosis requires confirmation with repeat testing.", _ADA)


# ----------------------------------------------------------------- lipids
_ATP3 = "NCEP ATP III lipid classification"


def evaluate_total_cholesterol(p: Profile) -> Finding | None:
    if p.total_chol_mgdl is None:
        return None
    c = p.total_chol_mgdl
    if c >= 240:
        cat, sev = "High", Severity.ABNORMAL
    elif c >= 200:
        cat, sev = "Borderline high", Severity.BORDERLINE
    else:
        cat, sev = "Desirable", Severity.NORMAL
    return Finding("total_cholesterol", "Total cholesterol", c, "mg/dL", cat, sev,
                   "Cardiovascular risk depends on the whole profile, not one number.", _ATP3)


def evaluate_hdl(p: Profile) -> Finding | None:
    if p.hdl_mgdl is None:
        return None
    h = p.hdl_mgdl
    if h < 40:
        cat, sev = "Low", Severity.ABNORMAL
    elif h >= 60:
        cat, sev = "High (protective)", Severity.NORMAL
    else:
        cat, sev = "Acceptable", Severity.NORMAL
    return Finding("hdl", "HDL cholesterol", h, "mg/dL", cat, sev,
                   "Higher HDL is generally better.", _ATP3)


def evaluate_triglycerides(p: Profile) -> Finding | None:
    if p.triglycerides_mgdl is None:
        return None
    t = p.triglycerides_mgdl
    if t >= 500:
        cat, sev = "Very high", Severity.URGENT
    elif t >= 200:
        cat, sev = "High", Severity.ABNORMAL
    elif t >= 150:
        cat, sev = "Borderline high", Severity.BORDERLINE
    else:
        cat, sev = "Normal", Severity.NORMAL
    msg = "Very high triglycerides can cause pancreatitis; see a clinician soon." if t >= 500 \
        else "Triglycerides are best measured after fasting."
    return Finding("triglycerides", "Triglycerides", t, "mg/dL", cat, sev, msg, _ATP3)


# ------------------------------------------------------ metabolic syndrome
_MS = "AHA/NHLBI 2005 metabolic syndrome criteria (US waist cutoffs)"


def evaluate_metabolic_syndrome(p: Profile) -> Finding | None:
    """>=3 of 5 criteria. Reports 'indeterminate' if missing inputs could change the result."""
    if p.sex not in ("male", "female"):
        return None
    male = p.sex == "male"
    checks: list[bool | None] = [
        None if p.waist_cm is None else p.waist_cm >= (102 if male else 88),
        None if p.triglycerides_mgdl is None else p.triglycerides_mgdl >= 150,
        None if p.hdl_mgdl is None else p.hdl_mgdl < (40 if male else 50),
        None if p.sbp is None or p.dbp is None else (p.sbp >= 130 or p.dbp >= 85),
        None if p.glucose_mgdl is None or not p.glucose_fasting else p.glucose_mgdl >= 100,
    ]
    met = sum(1 for c in checks if c is True)
    unknown = sum(1 for c in checks if c is None)
    if met < 3 and 5 - unknown < 3:
        return None  # fewer than 3 criteria known: nothing useful to report
    if met >= 3:
        cat, sev = "Metabolic syndrome criteria met", Severity.ABNORMAL
    elif met + unknown < 3:
        cat, sev = "Criteria not met", Severity.NORMAL
    else:
        cat, sev = "Indeterminate (more measurements needed)", Severity.BORDERLINE
    return Finding("metabolic_syndrome", "Metabolic syndrome", f"{met} of 5 criteria", None,
                   cat, sev,
                   f"{met} criteria met, {unknown} not provided. Ethnicity-specific waist "
                   "cutoffs may apply.", _MS)


_ALL = (
    evaluate_anemia, evaluate_bmi, evaluate_blood_pressure, evaluate_glucose,
    evaluate_hba1c, evaluate_total_cholesterol, evaluate_hdl,
    evaluate_triglycerides, evaluate_metabolic_syndrome,
)


def evaluate_all(p: Profile) -> list[Finding]:
    return [f for fn in _ALL if (f := fn(p)) is not None]
