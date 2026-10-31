from typing import Literal

from pydantic import BaseModel, Field

DISCLAIMER = (
    "Educational information only, not a diagnosis or medical advice. "
    "Talk to a qualified clinician about your results."
)


class LabInput(BaseModel):
    sex: Literal["male", "female"] | None = None
    age_years: float | None = Field(None, ge=0, le=120)
    pregnant: bool | None = None
    weight_kg: float | None = Field(None, ge=20, le=400)
    height_cm: float | None = Field(None, ge=50, le=250)
    waist_cm: float | None = Field(None, ge=30, le=250)
    sbp: float | None = Field(None, ge=50, le=300, description="Systolic mmHg")
    dbp: float | None = Field(None, ge=30, le=200, description="Diastolic mmHg")
    glucose_mgdl: float | None = Field(None, ge=20, le=1000)
    glucose_fasting: bool = True
    hba1c_pct: float | None = Field(None, ge=3, le=20)
    total_chol_mgdl: float | None = Field(None, ge=50, le=600)
    hdl_mgdl: float | None = Field(None, ge=5, le=200)
    triglycerides_mgdl: float | None = Field(None, ge=10, le=5000)
    hemoglobin_gdl: float | None = Field(None, ge=3, le=25)


class FindingOut(BaseModel):
    id: str
    label: str
    value: float | str | None
    unit: str | None
    category: str
    severity: Literal["normal", "borderline", "abnormal", "urgent"]
    message: str
    source: str


class LabResult(BaseModel):
    findings: list[FindingOut]
    disclaimer: str = DISCLAIMER
