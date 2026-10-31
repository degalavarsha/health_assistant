from dataclasses import asdict

from fastapi import APIRouter, Depends

from app.core.security import CurrentUser, get_current_user
from app.schemas.labs import FindingOut, LabInput, LabResult
from app.services.rules import Profile, evaluate_all

router = APIRouter(prefix="/labs", tags=["labs"])


@router.post("/evaluate", response_model=LabResult)
def evaluate_labs(body: LabInput, _user: CurrentUser = Depends(get_current_user)) -> LabResult:
    """Interpret labs and vitals against published guideline thresholds."""
    findings = evaluate_all(Profile(**body.model_dump()))
    return LabResult(findings=[FindingOut(**{**asdict(f), "severity": f.severity.value})
                               for f in findings])
