from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional
import os
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

# Admin password (set via environment variable in production)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Simple in-memory token store (acceptable for dev; replace with DB or JWT in production)
_valid_tokens: set[str] = set()


@router.post("/login")
async def login(payload: dict):
    """Login with admin password. Returns a short-lived token for admin actions.

    Request body: { "password": "..." }
    Response: { "token": "..." }
    """
    password = payload.get("password")
    if not password or password != ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    token = secrets.token_urlsafe(32)
    _valid_tokens.add(token)
    return {"token": token}


def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """Dependency to verify Authorization header 'Bearer <token>' and return token string."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid authorization header")
    token = authorization.split(" ", 1)[1]
    if token not in _valid_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return token


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """Invalidate the provided token (logout)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid authorization header")
    token = authorization.split(" ", 1)[1]
    _valid_tokens.discard(token)
    return {"detail": "logged out"}
