"""Odeme Takip endpoint'leri — taksit, odeme, borc durumu."""
from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter


router = APIRouter(prefix="/odeme", tags=["Odeme"])


@router.get("/ozet")
async def odeme_ozet(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Genel odeme ozeti — yonetici dashboard."""
    planlar = adapter.load(DataPaths.ODEME_PLANLAR) or []
    today = date.today().isoformat()

    toplam_borc = sum(p.get("net_tutar", 0) for p in planlar)
    toplam_odenen = 0
    geciken = 0

    for p in planlar:
        for t in p.get("taksitler", []):
            if t.get("durum") == "odendi":
                toplam_odenen += t.get("odeme_tutari", 0)
            elif t.get("vade_tarihi", "") < today and t.get("durum") == "bekliyor":
                geciken += t.get("tutar", 0)

    return {
        "toplam_ogrenci": len(planlar),
        "toplam_borc": round(toplam_borc, 2),
        "toplam_odenen": round(toplam_odenen, 2),
        "kalan_borc": round(toplam_borc - toplam_odenen, 2),
        "geciken_tutar": round(geciken, 2),
        "tahsilat_orani": round(toplam_odenen / max(toplam_borc, 1) * 100, 1),
    }


@router.get("/planlar")
async def odeme_planlar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Taksit planlari listesi."""
    planlar = adapter.load(DataPaths.ODEME_PLANLAR) or []
    if student_id:
        planlar = [p for p in planlar if p.get("student_id") == student_id]
    return {"planlar": planlar}


@router.get("/plan/{plan_id}")
async def odeme_plan_detay(
    plan_id: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Tek bir taksit plani detayi."""
    planlar = adapter.load(DataPaths.ODEME_PLANLAR) or []
    plan = next((p for p in planlar if p.get("id") == plan_id), None)
    if not plan:
        raise HTTPException(404, "Plan bulunamadi")
    return plan


@router.get("/veli-borc")
async def veli_borc_durumu(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Velinin cocuklarinin borc durumu."""
    children = user.get("children_ids", [])
    planlar = adapter.load(DataPaths.ODEME_PLANLAR) or []
    today = date.today().isoformat()

    sonuc = []
    for cid in children:
        child_plans = [p for p in planlar if p.get("student_id") == cid]
        for p in child_plans:
            odenen = sum(t.get("odeme_tutari", 0) for t in p.get("taksitler", []) if t.get("durum") == "odendi")
            bekleyen = [t for t in p.get("taksitler", []) if t.get("durum") in ("bekliyor", "gecikti")]
            geciken = [t for t in bekleyen if t.get("vade_tarihi", "") < today]
            sonuc.append({
                "student_id": cid,
                "student_adi": p.get("student_adi", ""),
                "plan_id": p.get("id"),
                "toplam": p.get("net_tutar", 0),
                "odenen": odenen,
                "kalan": round(p.get("net_tutar", 0) - odenen, 2),
                "sonraki_taksit": bekleyen[0] if bekleyen else None,
                "geciken_sayisi": len(geciken),
            })

    return {"borclar": sonuc}


@router.get("/geciken")
async def geciken_odemeler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Geciken odeme listesi — yonetici icin."""
    planlar = adapter.load(DataPaths.ODEME_PLANLAR) or []
    today = date.today().isoformat()

    geciken = []
    for p in planlar:
        for t in p.get("taksitler", []):
            if t.get("vade_tarihi", "") < today and t.get("durum") in ("bekliyor", "gecikti"):
                geciken.append({
                    "student_id": p.get("student_id"),
                    "student_adi": p.get("student_adi"),
                    "sinif": p.get("sinif"),
                    "taksit_sira": t.get("sira"),
                    "tutar": t.get("tutar"),
                    "vade_tarihi": t.get("vade_tarihi"),
                    "geciken_gun": (date.today() - date.fromisoformat(t["vade_tarihi"])).days,
                })

    geciken.sort(key=lambda x: x.get("geciken_gun", 0), reverse=True)
    return {"geciken": geciken, "toplam": len(geciken)}


@router.get("/ucretler")
async def ucret_kalemleri(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Ucret kalemleri listesi."""
    ucretler = adapter.load(DataPaths.ODEME_UCRETLER) or []
    return {"ucretler": ucretler}
