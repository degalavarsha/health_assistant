import logging
import os
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.core.security import CurrentUser, get_current_user
from app.services import imaging

router = APIRouter(prefix="/imaging", tags=["imaging"])
log = logging.getLogger(__name__)

_ALLOWED = {"image/png": ".png", "image/jpeg": ".jpg"}
_DISCLAIMER = ("Research demo only. Not a medical device and not a diagnosis. "
               "Have images interpreted by a qualified radiologist.")


@router.post("/xray")
async def predict_xray(
    file: UploadFile = File(...),
    threshold: float = 0.4,
    _user: CurrentUser = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    if file.content_type not in _ALLOWED:
        raise HTTPException(415, "Only PNG or JPEG images are accepted")
    if not 0.0 < threshold < 1.0:
        raise HTTPException(422, "threshold must be between 0 and 1")

    limit = settings.max_upload_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, f"File larger than {settings.max_upload_mb} MB")

    # Server-chosen temp name: the client filename is never used in a path.
    fd, path = tempfile.mkstemp(suffix=_ALLOWED[file.content_type])
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        try:
            probs = imaging.predict(path)
        except imaging.ModelUnavailable:
            raise HTTPException(503, "X-ray model is not available") from None
        except Exception:
            log.exception("X-ray inference failed")
            raise HTTPException(422, "Could not process this image") from None
    finally:
        if os.path.exists(path):
            os.remove(path)

    flagged = sorted((k for k, v in probs.items() if v >= threshold), key=lambda k: -probs[k])
    return {"probabilities": probs, "flagged": flagged, "threshold": threshold,
            "disclaimer": _DISCLAIMER}
