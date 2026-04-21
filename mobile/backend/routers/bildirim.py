"""Bildirim endpoint'leri — tum roller icin ortak."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter


router = APIRouter(prefix="/bildirim", tags=["Bildirim"])


@router.get("/liste")
async def get_bildirimler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    limit: int = 50,
    sadece_okunmamis: bool = False,
):
    """Kullanicinin bildirimlerini getir."""
    uid = user.get("user_id", "")
    role = user.get("role", "").lower()

    all_bildirim = adapter.load(DataPaths.BILDIRIMLER) or []

    # Kullaniciya ait veya rolune ait bildirimleri filtrele
    mine = [
        b for b in all_bildirim
        if b.get("alici_id") == uid
        or b.get("alici_rol") == role
        or b.get("alici_rol") == "hepsi"
    ]

    if sadece_okunmamis:
        mine = [b for b in mine if not b.get("okundu", False)]

    mine.sort(key=lambda b: b.get("tarih", ""), reverse=True)

    return {
        "bildirimler": mine[:limit],
        "toplam": len(mine),
        "okunmamis": sum(1 for b in mine if not b.get("okundu", False)),
    }


@router.post("/{bildirim_id}/okundu")
async def mark_okundu(
    bildirim_id: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Bildirimi okundu olarak isaretle."""
    adapter.update_by_id(DataPaths.BILDIRIMLER, bildirim_id, {"okundu": True})
    return {"ok": True}


@router.post("/tumunu-oku")
async def mark_all_okundu(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Tum bildirimleri okundu yap."""
    uid = user.get("user_id", "")
    role = user.get("role", "").lower()
    all_bildirim = adapter.load(DataPaths.BILDIRIMLER) or []

    for b in all_bildirim:
        if (b.get("alici_id") == uid or b.get("alici_rol") == role
                or b.get("alici_rol") == "hepsi"):
            b["okundu"] = True

    adapter.save(DataPaths.BILDIRIMLER, all_bildirim)
    return {"ok": True}
