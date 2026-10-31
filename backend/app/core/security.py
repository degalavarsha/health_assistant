"""Supabase JWT verification.

In production a valid Supabase access token is always required. In development
with no SUPABASE_JWT_SECRET configured, requests are allowed as a clearly
marked dev user so the API can be explored locally. That bypass is disabled
whenever APP_ENV is not "development".
"""
import logging
from dataclasses import dataclass

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings

log = logging.getLogger(__name__)
_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class CurrentUser:
    id: str
    email: str | None = None
    is_dev: bool = False


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    if not settings.supabase_jwt_secret:
        if settings.is_dev:
            log.warning("Auth bypass active: SUPABASE_JWT_SECRET is not set (dev only)")
            return CurrentUser(id="dev-user", is_dev=True)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Server auth is not configured")

    if creds is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    try:
        claims = jwt.decode(
            creds.credentials,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token") from None
    return CurrentUser(id=claims["sub"], email=claims.get("email"))
