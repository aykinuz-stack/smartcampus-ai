"""Mood Check-in router — ogrenci gunluk ruh hali."""
from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.mood import (
    MoodCheckinCreate,
    MoodCheckinResponse,
    MoodSummaryResponse,
)


router = APIRouter(prefix="/mood", tags=["Mood Check-in"])


@router.post("/checkin", response_model=MoodCheckinResponse, status_code=201)
async def create_checkin(
    req: MoodCheckinCreate,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yeni mood check-in olustur. Ayni gun varsa gunceller."""
    role = user.get("role", "").lower()
    if role not in ("ogrenci", "veli", "superadmin", "yonetici"):
        raise HTTPException(403, "Sadece ogrenci kendi check-in'ini yapabilir.")

    student_id = user.get("student_id") or user.get("user_id")
    if not student_id:
        raise HTTPException(400, "Ogrenci ID bulunamadi.")

    today = date.today().isoformat()
    now = datetime.now().isoformat()

    # Ayni gun var mi kontrol + guncelle
    checkins = adapter.load(DataPaths.MOOD_CHECKINS) or []
    existing_idx = next(
        (i for i, c in enumerate(checkins)
         if c.get("student_id") == student_id and c.get("tarih") == today),
        None
    )

    if existing_idx is not None:
        # Guncelle
        item = checkins[existing_idx]
        item["level"] = req.level
        item["tags"] = req.tags
        item["not"] = req.not_
        item["olusturma"] = now
        adapter.save(DataPaths.MOOD_CHECKINS, checkins)
    else:
        # Yeni ekle
        item = {
            "id": f"mood_{uuid.uuid4().hex[:8]}",
            "student_id": student_id,
            "student_name": user.get("ad_soyad", ""),
            "tarih": today,
            "level": req.level,
            "tags": req.tags,
            "not": req.not_,
            "olusturma": now,
        }
        adapter.append(DataPaths.MOOD_CHECKINS, item)

    return MoodCheckinResponse(
        id=item["id"],
        student_id=student_id,
        student_name=item["student_name"],
        tarih=today,
        level=req.level,
        tags=req.tags,
        not_=req.not_,
        olusturma=now,
    )


@router.get("/today")
async def get_today(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Ogrencinin bugunku check-in'i (yoksa None)."""
    student_id = user.get("student_id") or user.get("user_id")
    today = date.today().isoformat()
    checkins = adapter.load(DataPaths.MOOD_CHECKINS) or []
    mine = next((c for c in checkins
                 if c.get("student_id") == student_id and c.get("tarih") == today), None)
    return mine


@router.get("/history")
async def get_history(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    days: int = 30,
):
    """Son N gun check-in'ler."""
    student_id = user.get("student_id") or user.get("user_id")
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    checkins = adapter.load(DataPaths.MOOD_CHECKINS) or []
    mine = [c for c in checkins
            if c.get("student_id") == student_id and c.get("tarih", "") >= cutoff]
    mine.sort(key=lambda c: c.get("tarih", ""), reverse=True)
    return mine


@router.get("/summary", response_model=MoodSummaryResponse)
async def get_summary(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Son 30 gun ozet — ortalama, trend, negatif gun sayisi."""
    student_id = user.get("student_id") or user.get("user_id")
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    checkins = adapter.load(DataPaths.MOOD_CHECKINS) or []
    mine = [c for c in checkins
            if c.get("student_id") == student_id and c.get("tarih", "") >= cutoff]

    if not mine:
        return MoodSummaryResponse(
            ortalama_seviye=0.0, toplam_checkin=0,
            son_7_gun=[], negatif_gun_sayisi=0, trend="stabil",
        )

    ort = sum(c.get("level", 3) for c in mine) / len(mine)
    negatif = sum(1 for c in mine if c.get("level", 3) <= 2)

    # Son 7 gun
    son_7_cutoff = (date.today() - timedelta(days=7)).isoformat()
    son_7 = sorted(
        [{"tarih": c["tarih"], "level": c["level"], "tags": c.get("tags", [])}
         for c in mine if c.get("tarih", "") >= son_7_cutoff],
        key=lambda x: x["tarih"],
    )

    # Trend — son 7 vs onceki 7-14
    son_7_ort = sum(x["level"] for x in son_7) / max(len(son_7), 1)
    onceki_cutoff = (date.today() - timedelta(days=14)).isoformat()
    onceki_7 = [c for c in mine
                if onceki_cutoff <= c.get("tarih", "") < son_7_cutoff]
    onceki_7_ort = sum(c["level"] for c in onceki_7) / max(len(onceki_7), 1) \
        if onceki_7 else son_7_ort
    delta = son_7_ort - onceki_7_ort
    trend = "yukseliyor" if delta > 0.3 else ("dusuyor" if delta < -0.3 else "stabil")

    return MoodSummaryResponse(
        ortalama_seviye=round(ort, 2),
        toplam_checkin=len(mine),
        son_7_gun=son_7,
        negatif_gun_sayisi=negatif,
        trend=trend,
    )
