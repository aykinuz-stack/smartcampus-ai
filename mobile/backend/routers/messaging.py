"""Mesajlasma — ogretmen/veli/ogrenci arasi okul ici mesaj."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.messaging import MesajGonderRequest, MesajItem, MesajListResponse


router = APIRouter(prefix="/mesaj", tags=["Mesajlasma"])


@router.get("/liste", response_model=MesajListResponse)
async def get_mesajlar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
    limit: int = 50,
):
    """Kullaniciya iliskin mesajlar."""
    role = user.get("role", "").lower()
    user_id = user.get("user_id", "")
    own_student = user.get("student_id", "")

    all_msg = adapter.load(DataPaths.__dict__.get(
        "VELI_MESAJLAR", "akademik/veli_mesajlar.json"
    )) or []

    # Filtreleme
    mine = []
    for m in all_msg:
        if role == "ogrenci":
            # Kendi mesajlari (ogrenci konulu)
            if m.get("student_id") == own_student:
                mine.append(m)
        elif role == "veli":
            # Cocugunun mesajlari
            children = user.get("children_ids", [])
            if m.get("student_id") in children:
                mine.append(m)
        elif role == "ogretmen":
            # Kendine atif ogretmen mesajlari
            if m.get("ogretmen_id") == user_id:
                mine.append(m)
        else:
            # Admin vb — hepsini gorebilir (ogrenci filtreli)
            if student_id:
                if m.get("student_id") == student_id:
                    mine.append(m)
            else:
                mine.append(m)

    mine.sort(key=lambda m: m.get("tarih", ""), reverse=True)
    mine = mine[:limit]

    mesajlar = [
        MesajItem(
            id=m.get("id", ""),
            student_id=m.get("student_id", ""),
            veli_adi=m.get("veli_adi", ""),
            ogretmen_id=m.get("ogretmen_id", ""),
            ogretmen_adi=m.get("ogretmen_adi", ""),
            tarih=m.get("tarih", ""),
            mesaj=m.get("mesaj", ""),
            yon=m.get("yon", ""),
            okundu=bool(m.get("okundu", False)),
        )
        for m in mine
    ]

    okunmamis = sum(1 for m in mesajlar if not m.okundu)
    return MesajListResponse(mesajlar=mesajlar, toplam=len(mesajlar), okunmamis=okunmamis)


@router.post("/gonder", response_model=MesajItem, status_code=201)
async def gonder(
    req: MesajGonderRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yeni mesaj gonder."""
    role = user.get("role", "").lower()

    # Yon belirleme
    yon = f"{role}_to_{req.alici_rol}"

    student_id = req.student_id or user.get("student_id", "")
    if role == "veli":
        # Veli'nin cocuklarindan biri olmali
        children = user.get("children_ids", [])
        if student_id and student_id not in children:
            raise HTTPException(403, "Bu ogrenci sizin cocugunuz degil")
        if not student_id and children:
            student_id = children[0]

    yeni_mesaj = {
        "id": f"vm_{uuid.uuid4().hex[:8]}",
        "student_id": student_id,
        "veli_adi": user.get("ad_soyad", "") if role == "veli" else "",
        "ogretmen_id": req.alici_id if req.alici_rol == "ogretmen" else (
            user.get("user_id", "") if role == "ogretmen" else ""
        ),
        "ogretmen_adi": user.get("ad_soyad", "") if role == "ogretmen" else "",
        "tarih": datetime.now().isoformat(),
        "mesaj": req.mesaj,
        "yon": yon,
        "okundu": False,
    }
    path = DataPaths.__dict__.get("VELI_MESAJLAR", "akademik/veli_mesajlar.json")
    adapter.append(path, yeni_mesaj)

    return MesajItem(**{k: v for k, v in yeni_mesaj.items() if k in MesajItem.model_fields})


@router.post("/{mesaj_id}/okundu")
async def mark_read(
    mesaj_id: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Mesaji okundu olarak isaretle."""
    path = DataPaths.__dict__.get("VELI_MESAJLAR", "akademik/veli_mesajlar.json")
    ok = adapter.update_by_id(path, mesaj_id, {"okundu": True})
    if not ok:
        raise HTTPException(404, "Mesaj bulunamadi")
    return {"ok": True}
