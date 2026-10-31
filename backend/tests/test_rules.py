import pytest

from app.services.rules import (
    Profile, Severity, evaluate_all, evaluate_anemia, evaluate_blood_pressure,
    evaluate_bmi, evaluate_glucose, evaluate_hba1c, evaluate_metabolic_syndrome,
    evaluate_triglycerides,
)


@pytest.mark.parametrize("sex,pregnant,hb,expected", [
    ("male", None, 13.0, "No anemia"),
    ("male", None, 12.0, "Mild anemia"),
    ("female", False, 12.0, "No anemia"),
    ("female", False, 11.5, "Mild anemia"),
    ("female", False, 9.0, "Moderate anemia"),
    ("female", False, 7.5, "Severe anemia"),
    ("female", True, 10.5, "Mild anemia"),
    ("female", True, 11.0, "No anemia"),
])
def test_anemia(sex, pregnant, hb, expected):
    f = evaluate_anemia(Profile(sex=sex, pregnant=pregnant, hemoglobin_gdl=hb))
    assert f.category == expected


def test_anemia_needs_sex():
    assert evaluate_anemia(Profile(hemoglobin_gdl=10)) is None


@pytest.mark.parametrize("w,h,expected", [
    (50, 180, "Underweight"), (70, 175, "Healthy weight"), (80, 175, "Overweight"),
    (95, 175, "Obesity class 1"), (115, 175, "Obesity class 2"), (140, 175, "Obesity class 3"),
])
def test_bmi(w, h, expected):
    assert evaluate_bmi(Profile(weight_kg=w, height_cm=h)).category == expected


@pytest.mark.parametrize("s,d,expected,sev", [
    (115, 75, "Normal", Severity.NORMAL),
    (125, 78, "Elevated", Severity.BORDERLINE),
    (132, 78, "Stage 1 hypertension range", Severity.ABNORMAL),
    (118, 85, "Stage 1 hypertension range", Severity.ABNORMAL),
    (145, 85, "Stage 2 hypertension range", Severity.ABNORMAL),
    (150, 95, "Stage 2 hypertension range", Severity.ABNORMAL),
    (190, 100, "Hypertensive crisis range", Severity.URGENT),
    (150, 125, "Hypertensive crisis range", Severity.URGENT),
])
def test_blood_pressure(s, d, expected, sev):
    f = evaluate_blood_pressure(Profile(sbp=s, dbp=d))
    assert (f.category, f.severity) == (expected, sev)


def test_glucose_ignored_when_not_fasting():
    assert evaluate_glucose(Profile(glucose_mgdl=150, glucose_fasting=False)) is None


@pytest.mark.parametrize("g,expected", [(90, "Normal"), (100, "Prediabetes range"),
                                        (125, "Prediabetes range"), (126, "Diabetes range")])
def test_fasting_glucose(g, expected):
    assert evaluate_glucose(Profile(glucose_mgdl=g)).category == expected


@pytest.mark.parametrize("a,expected", [(5.6, "Normal"), (5.7, "Prediabetes range"),
                                        (6.4, "Prediabetes range"), (6.5, "Diabetes range")])
def test_hba1c(a, expected):
    assert evaluate_hba1c(Profile(hba1c_pct=a)).category == expected


def test_very_high_triglycerides_is_urgent():
    assert evaluate_triglycerides(Profile(triglycerides_mgdl=550)).severity is Severity.URGENT


def test_metabolic_syndrome_met():
    p = Profile(sex="male", waist_cm=110, triglycerides_mgdl=180, hdl_mgdl=35,
                sbp=120, dbp=70, glucose_mgdl=90)
    assert evaluate_metabolic_syndrome(p).category == "Metabolic syndrome criteria met"


def test_metabolic_syndrome_not_met_when_enough_known_negatives():
    p = Profile(sex="female", waist_cm=80, triglycerides_mgdl=100, hdl_mgdl=60,
                sbp=110, dbp=70, glucose_mgdl=90)
    assert evaluate_metabolic_syndrome(p).category == "Criteria not met"


def test_metabolic_syndrome_indeterminate_when_inputs_missing():
    p = Profile(sex="male", waist_cm=110, triglycerides_mgdl=180, hdl_mgdl=60)
    assert evaluate_metabolic_syndrome(p).category.startswith("Indeterminate")


def test_metabolic_syndrome_silent_with_too_few_inputs():
    assert evaluate_metabolic_syndrome(Profile(sex="male", waist_cm=110, triglycerides_mgdl=180)) is None


def test_sex_specific_hdl_threshold_for_metabolic_syndrome():
    base = dict(waist_cm=110, triglycerides_mgdl=180, sbp=120, dbp=70, glucose_mgdl=90)
    assert evaluate_metabolic_syndrome(Profile(sex="female", hdl_mgdl=45, **base)).category \
        == "Metabolic syndrome criteria met"
    assert evaluate_metabolic_syndrome(Profile(sex="male", hdl_mgdl=45, **base)).category \
        == "Criteria not met"


def test_evaluate_all_skips_missing():
    assert evaluate_all(Profile()) == []
    assert len(evaluate_all(Profile(sex="male", hemoglobin_gdl=14, sbp=118, dbp=76))) == 2
