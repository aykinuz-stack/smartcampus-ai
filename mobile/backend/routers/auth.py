"""Auth router — login, refresh, me."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

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

    # Sifre dogrulama — bcrypt + legacy sha256 + plain destekler
    stored = user.get("password_hash") or user.get("sifre_hash") or user.get("sifre", "")
    ok = False
    if stored.startswith("$2"):
        # bcrypt hash
        ok = verify_password(req.password, stored)
    elif len(stored) == 64 and all(c in "0123456789abcdef" for c in stored):
        # SHA-256 legacy hash (utils/auth.py ile ortak)
        import hashlib
        ok = hashlib.sha256(req.password.encode("utf-8")).hexdigest() == stored
    else:
        # Plain text (gelistirme)
        ok = stored == req.password

    if not ok:
        raise HTTPException(status_code=401, detail="Sifre hatali")

    # Token payload
    # ad_soyad: once ad_soyad, sonra name, sonra ad+soyad
    ad_soyad = (
        user.get("ad_soyad")
        or user.get("name")
        or f"{user.get('ad', '')} {user.get('soyad', '')}".strip()
        or user.get("username", "")
    )
    payload = {
        "sub": user.get("username"),
        "role": user.get("role", "Ogrenci").lower(),
        "tenant_id": req.tenant_id,
        "user_id": user.get("id", user.get("username")),
        "ad_soyad": ad_soyad,
        "student_id": user.get("student_id") or user.get("id", ""),
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


@router.post("/change-password")
async def change_password(
    req: Annotated[dict, Body()],
    user: Annotated[dict, Depends(get_current_user)],
):
    """Sifre degistir — eski sifre + yeni sifre."""
    import json
    from ..core.security import hash_password

    old_password = req.get("old_password", "")
    new_password = req.get("new_password", "")
    if not old_password or not new_password:
        raise HTTPException(status_code=400, detail="Eski ve yeni sifre gerekli")
    if len(new_password) < 4:
        raise HTTPException(status_code=400, detail="Yeni sifre en az 4 karakter olmali")

    username = user.get("sub", "")
    tenant_id = user.get("tenant_id", "default")

    # Kullanici dosyasini bul
    candidates = [
        _PROJECT_ROOT / "data" / "tenants" / tenant_id / "users.json",
        _PROJECT_ROOT / "data" / "users.json",
    ]
    users_path = None
    users = []
    for p in candidates:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    users = json.load(f)
                users_path = p
                break
            except Exception:
                pass

    if not users_path:
        raise HTTPException(status_code=500, detail="Kullanici dosyasi bulunamadi")

    target = next((u for u in users if u.get("username") == username), None)
    if not target:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi")

    # Eski sifre dogrulama
    stored = target.get("password_hash") or target.get("sifre_hash") or target.get("sifre", "")
    ok = False
    if stored.startswith("$2"):
        ok = verify_password(old_password, stored)
    elif len(stored) == 64 and all(c in "0123456789abcdef" for c in stored):
        import hashlib
        ok = hashlib.sha256(old_password.encode("utf-8")).hexdigest() == stored
    else:
        ok = stored == old_password
    if not ok:
        raise HTTPException(status_code=401, detail="Eski sifre hatali")

    # Yeni sifre hash'le ve kaydet
    target["password_hash"] = hash_password(new_password)
    # Eski alanlari temizle
    target.pop("sifre_hash", None)
    target.pop("sifre", None)

    with open(users_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    return {"ok": True, "message": "Sifre basariyla degistirildi"}


@router.post("/forgot-password")
async def forgot_password(req: Annotated[dict, Body()]):
    """Sifre sifirlama talebi — username ile gecici sifre uretir."""
    import json
    import secrets
    import logging
    from ..core.security import hash_password

    username = req.get("username", "").strip()
    tenant_id = req.get("tenant_id", "default")
    if not username:
        raise HTTPException(status_code=400, detail="Kullanici adi gerekli")

    candidates = [
        _PROJECT_ROOT / "data" / "tenants" / tenant_id / "users.json",
        _PROJECT_ROOT / "data" / "users.json",
    ]
    users_path = None
    users = []
    for p in candidates:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    users = json.load(f)
                users_path = p
                break
            except Exception:
                pass

    if not users_path:
        raise HTTPException(status_code=500, detail="Kullanici dosyasi bulunamadi")

    target = next((u for u in users if u.get("username") == username), None)
    if not target:
        # Guvenlik: kullanicinin var olup olmadigini belli etme
        return {"ok": True, "message": "Eger kullanici mevcutsa, gecici sifre olusturuldu. Yoneticiyle iletisime gecin."}

    # Gecici sifre uret
    temp_password = secrets.token_urlsafe(8)
    target["password_hash"] = hash_password(temp_password)
    target.pop("sifre_hash", None)
    target.pop("sifre", None)

    with open(users_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    # Log'a yaz (production'da e-posta/SMS gonderilir)
    logger = logging.getLogger("smartcampus.auth")
    logger.info(f"[FORGOT-PASSWORD] Kullanici: {username} | Gecici sifre: {temp_password}")

    return {"ok": True, "message": "Gecici sifre olusturuldu. Yoneticiyle iletisime gecin."}


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
