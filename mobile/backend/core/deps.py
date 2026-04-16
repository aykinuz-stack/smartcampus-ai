"""FastAPI dependencies — yetki + veri adapter injection."""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Header, status

from .data_adapter import DataAdapter
from .security import decode_token


# ──────────────────────────────────────────────────────────────────────
# Auth Header'dan token al ve kullaniciyi dondur
# ──────────────────────────────────────────────────────────────────────

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> dict:
    """Authorization: Bearer <token> header'indan JWT'yi dogrula."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header eksik",
            headers={"WWW-Authenticate": "Bearer"},
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yanlis Authorization formati",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = parts[1]
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token gecersiz veya suresi doldu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  # {sub: username, role, tenant_id, ...}


# ──────────────────────────────────────────────────────────────────────
# Rol bazli erisim — decorator yerine dependency
# ──────────────────────────────────────────────────────────────────────

def require_roles(*roles: str):
    """Belirli rol listesinde olma zorunlulugu.

    Ornek: @router.get("/x", dependencies=[Depends(require_roles("rehber", "mudur"))])
    """
    async def checker(user: Annotated[dict, Depends(get_current_user)]) -> dict:
        user_role = (user.get("role") or "").lower()
        allowed = [r.lower() for r in roles]
        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Bu endpoint icin yetki yok. Gerekli rol: {roles}",
            )
        return user
    return checker


# ──────────────────────────────────────────────────────────────────────
# Veri adapter injection — tenant-aware
# ──────────────────────────────────────────────────────────────────────

async def get_data_adapter(
    user: Annotated[dict, Depends(get_current_user)],
) -> DataAdapter:
    """Kullanicinin tenant_id'sine uyumlu DataAdapter olustur."""
    tenant_id = user.get("tenant_id", "default")
    return DataAdapter(tenant_id=tenant_id)
