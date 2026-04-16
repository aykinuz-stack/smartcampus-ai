"""Auth router — login, refresh, me."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..core.config import settings
from ..core.deps import get_current_user
from ..core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from ..schemas.auth import (
    CurrentUserResponse,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    TokenResponse,
)


# Mevcut Streamlit auth sistemini ic ceki
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


router = APIRouter(prefix="/auth", tags=["Auth"])


def _load_users_for_tenant(tenant_id: str) -> list[dict]:
    """Mevcut users.json'i oku (tenant-aware)."""
    candidates = [
        _PROJECT_ROOT / "data" / "tenants" / tenant_id / "users.json",
        _PROJECT_ROOT / "data" / "users.json",
    ]
    import json
    for p in candidates:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return []


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """Kullanici giris — JWT access+refresh uretir."""
    users = _load_users_for_tenant(req.tenant_id)
    user = next((u for u in users if u.get("username") == req.username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Kullanici bulunamadi")

    # Sifre dogrulama — mevcut sistem bcrypt hash tutuyor olabilir
    # Ilk surumde basit dogrulama: sifre_hash veya password_hash alanina bak
    stored = user.get("password_hash") or user.get("sifre_hash") or user.get("sifre", "")
    ok = False
    if stored.startswith("$2"):  # bcrypt hash
        ok = verify_password(req.password, stored)
    else:
        # Plain text (gelistirme)
        ok = stored == req.password

    if not ok:
        raise HTTPException(status_code=401, detail="Sifre hatali")

    # Token payload
    payload = {
        "sub": user.get("username"),
        "role": user.get("role", "Ogrenci").lower(),
        "tenant_id": req.tenant_id,
        "user_id": user.get("id", user.get("username")),
        "ad_soyad": user.get("ad_soyad", f"{user.get('ad','')} {user.get('soyad','')}").strip(),
        "student_id": user.get("student_id", ""),
        "children_ids": user.get("children_ids", []),
    }

    access = create_access_token(payload)
    refresh = create_refresh_token({"sub": payload["sub"], "tenant_id": req.tenant_id})

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "username": payload["sub"],
            "role": payload["role"],
            "ad_soyad": payload["ad_soyad"],
            "tenant_id": payload["tenant_id"],
            "student_id": payload["student_id"],
            "children_ids": payload["children_ids"],
        },
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: RefreshRequest):
    """Refresh token ile yeni access token uret."""
    payload = decode_token(req.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token gecersiz")

    username = payload["sub"]
    tenant_id = payload.get("tenant_id", "default")

    # Kullaniciyi yeniden yukle
    users = _load_users_for_tenant(tenant_id)
    user = next((u for u in users if u.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Kullanici artik yok")

    new_payload = {
        "sub": username,
        "role": user.get("role", "Ogrenci").lower(),
        "tenant_id": tenant_id,
        "user_id": user.get("id", username),
        "ad_soyad": user.get("ad_soyad", ""),
        "student_id": user.get("student_id", ""),
        "children_ids": user.get("children_ids", []),
    }
    access = create_access_token(new_payload)
    refresh_new = create_refresh_token({"sub": username, "tenant_id": tenant_id})

    return TokenResponse(
        access_token=access,
        refresh_token=refresh_new,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={"username": username, "role": new_payload["role"], "tenant_id": tenant_id,
              "ad_soyad": new_payload["ad_soyad"], "student_id": new_payload["student_id"],
              "children_ids": new_payload["children_ids"]},
    )


@router.post("/logout")
async def logout(req: LogoutRequest):
    """Client taraftan token'i silmesi yeterli — burda sadece 200."""
    # Production'da token blacklist sistemine ekleme yapilabilir
    return {"ok": True, "message": "Cikis yapildi"}


@router.get("/me", response_model=CurrentUserResponse)
async def get_me(user: Annotated[dict, Depends(get_current_user)]):
    """Kullanici token'in sahibi — kim giris yapmis?"""
    return CurrentUserResponse(
        username=user.get("sub"),
        role=user.get("role"),
        ad_soyad=user.get("ad_soyad"),
        tenant_id=user.get("tenant_id", "default"),
        student_id=user.get("student_id"),
        children_ids=user.get("children_ids", []),
    )
