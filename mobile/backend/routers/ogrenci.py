"""Ogrenci odakli endpoint'ler — notlar, devamsizlik, odev."""
from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.ogrenci import (
    AttendanceItem,
    AttendanceResponse,
    GradeItem,
    GradeSummary,
    GradesResponse,
    OdevItem,
    OdevListResponse,
    OdevTeslimRequest,
)


router = APIRouter(prefix="/ogrenci", tags=["Ogrenci"])


def _target_student_id(user: dict, query_sid: str | None = None) -> str:
    """Hangi ogrencinin verisi? Veli ise cocuk ID, ogrenci ise kendi ID."""
    role = user.get("role", "").lower()
    if role == "ogrenci":
        return user.get("student_id") or user.get("user_id")
    if role == "veli":
        children = user.get("children_ids", [])
        if query_sid and query_sid in children:
            return query_sid
        return children[0] if children else ""
    # Yetkili (rehber/mudur/ogretmen) her ogrenciye bakabilir
    if query_sid:
        return query_sid
    raise HTTPException(400, "student_id gerekli")


# ══════════════════════════════════════════════════════════════
# NOTLAR
# ══════════════════════════════════════════════════════════════

@router.get("/notlar", response_model=GradesResponse)
async def get_notlar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
    donem: str | None = None,   # "1. Donem" / "2. Donem" / None=hepsi
):
    """Ogrenci notlari — ders, donem, not turu bazli."""
    sid = _target_student_id(user, student_id)
    all_grades = adapter.load(DataPaths.GRADES) or []

    mine = [g for g in all_grades if g.get("student_id") == sid]
    if donem:
        mine = [g for g in mine if g.get("donem") == donem]

    # Tarih DESC siralama
    mine.sort(key=lambda g: g.get("tarih", ""), reverse=True)

    notlar = [
        GradeItem(
            id=g.get("id", ""),
            ders=g.get("ders", ""),
            donem=g.get("donem", ""),
            not_turu=g.get("not_turu", ""),
            not_sirasi=int(g.get("not_sirasi", 0) or 0),
            puan=float(g.get("puan", 0) or 0),
            tarih=g.get("tarih", ""),
            aciklama=g.get("aciklama", ""),
        )
        for g in mine
    ]

    # Ders bazli ortalama
    ders_puanlari: dict[str, list[float]] = defaultdict(list)
    for n in notlar:
        ders_puanlari[n.ders].append(n.puan)

    ders_ozetleri = [
        GradeSummary(
            ders=ders,
            ortalama=round(sum(p) / len(p), 1),
            not_sayisi=len(p),
            en_yuksek=max(p),
            en_dusuk=min(p),
        )
        for ders, p in sorted(ders_puanlari.items())
    ]

    # Genel ortalama
    tum_puanlar = [n.puan for n in notlar]
    genel = round(sum(tum_puanlar) / len(tum_puanlar), 1) if tum_puanlar else 0.0

    # Donem ortalaması (mevcut donem)
    if donem:
        donem_ort = genel
    else:
        now = datetime.now()
        curr_donem = "1. Donem" if now.month >= 9 or now.month <= 1 else "2. Donem"
        donem_puanlari = [n.puan for n in notlar if n.donem == curr_donem]
        donem_ort = round(sum(donem_puanlari) / len(donem_puanlari), 1) \
            if donem_puanlari else 0.0

    return GradesResponse(
        notlar=notlar,
        donem_ortalamasi=donem_ort,
        genel_ortalama=genel,
        ders_ozetleri=ders_ozetleri,
    )


# ══════════════════════════════════════════════════════════════
# DEVAMSIZLIK
# ══════════════════════════════════════════════════════════════

@router.get("/devamsizlik", response_model=AttendanceResponse)
async def get_devamsizlik(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrenci devamsizlik kayitlari ve ozet."""
    sid = _target_student_id(user, student_id)
    all_att = adapter.load(DataPaths.ATTENDANCE) or []
    mine = [a for a in all_att if a.get("student_id") == sid]
    mine.sort(key=lambda a: a.get("tarih", ""), reverse=True)

    kayitlar = [
        AttendanceItem(
            id=a.get("id", ""),
            tarih=a.get("tarih", ""),
            ders=a.get("ders", ""),
            ders_saati=int(a.get("ders_saati", 0) or 0),
            turu=a.get("turu", ""),
            aciklama=a.get("aciklama", ""),
        )
        for a in mine
    ]

    ozursuz = sum(1 for k in kayitlar if k.turu.lower() in ("devamsiz", "ozursuz"))
    ozurlu = sum(1 for k in kayitlar if k.turu.lower() in ("izinli", "raporlu", "ozurlu"))
    gec = sum(1 for k in kayitlar if k.turu.lower() == "gec")

    # Son 30 gun
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    son_30 = sum(1 for k in kayitlar if k.tarih >= cutoff and k.turu.lower() in ("devamsiz", "ozursuz"))

    total = len(kayitlar)
    oran = round(ozursuz / max(total, 1) * 100, 1)

    return AttendanceResponse(
        kayitlar=kayitlar,
        toplam_ders_saati=ozursuz,
        ozursuz=ozursuz,
        ozurlu=ozurlu,
        gec=gec,
        oran=oran,
        son_30_gun=son_30,
    )


# ══════════════════════════════════════════════════════════════
# ODEVLER
# ══════════════════════════════════════════════════════════════

@router.get("/odevler", response_model=OdevListResponse)
async def get_odevler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
):
    """Ogrencinin odev listesi — bekleyen/geciken/teslim edilen."""
    sid = _target_student_id(user, student_id)

    # Ogrencinin sinif/sube bilgisi
    students = adapter.load(DataPaths.STUDENTS) or []
    student = next((s for s in students if s.get("id") == sid), None)
    sinif, sube = (student.get("sinif", ""), student.get("sube", "")) if student else ("", "")

    all_odev = adapter.load(DataPaths.HOMEWORK) or []
    # Ogrencinin sinif/subesi icin verilen odevler
    mine_odev = [
        o for o in all_odev
        if str(o.get("sinif", "")) == str(sinif) and o.get("sube", "") == sube
    ]

    # Teslim kayitlarinda bu ogrenciye ait olanlar
    all_teslim = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
    mine_teslim = {t.get("odev_id"): t for t in all_teslim
                  if t.get("student_id") == sid}

    today = date.today().isoformat()
    bekleyen, geciken, teslim_edilen = [], [], []

    for o in mine_odev:
        teslim = mine_teslim.get(o.get("id"))
        teslim_tarihi = o.get("teslim_tarihi", "")
        durum = o.get("durum", "")

        item = OdevItem(
            id=o.get("id", ""),
            baslik=o.get("baslik", ""),
            ders=o.get("ders", ""),
            ogretmen_adi=o.get("ogretmen_adi", ""),
            tur=o.get("tur", ""),
            aciklama=o.get("aciklama", ""),
            verilis_tarihi=o.get("verilis_tarihi", ""),
            teslim_tarihi=teslim_tarihi,
            durum=durum,
            teslim_edildi=teslim is not None,
            teslim_tarih=teslim.get("teslim_tarihi") if teslim else None,
            puan=teslim.get("puan") if teslim else None,
            gec_teslim=teslim.get("gec_teslim", False) if teslim else False,
        )

        if teslim:
            teslim_edilen.append(item)
        elif teslim_tarihi and teslim_tarihi < today:
            geciken.append(item)
        else:
            bekleyen.append(item)

    # Bekleyenler: en yakın teslim tarihi önce
    bekleyen.sort(key=lambda o: o.teslim_tarihi or "9999")
    geciken.sort(key=lambda o: o.teslim_tarihi or "9999", reverse=True)
    teslim_edilen.sort(key=lambda o: o.teslim_tarih or "", reverse=True)

    return OdevListResponse(
        bekleyen=bekleyen,
        geciken=geciken,
        teslim_edilen=teslim_edilen,
        toplam=len(mine_odev),
    )


@router.post("/odev/teslim")
async def teslim_et(
    req: OdevTeslimRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Odev teslim kaydi. Sadece ogrenci kendi odevini teslim edebilir."""
    role = user.get("role", "").lower()
    if role != "ogrenci":
        raise HTTPException(403, "Sadece ogrenci teslim edebilir")

    sid = user.get("student_id") or user.get("user_id")
    if not sid:
        raise HTTPException(400, "student_id yok")

    # Odev var mi
    odevler = adapter.load(DataPaths.HOMEWORK) or []
    odev = next((o for o in odevler if o.get("id") == req.odev_id), None)
    if not odev:
        raise HTTPException(404, "Odev bulunamadi")

    # Zaten teslim mi
    teslimler = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
    existing = next((t for t in teslimler
                    if t.get("odev_id") == req.odev_id and t.get("student_id") == sid),
                   None)

    today = date.today().isoformat()
    teslim_tarihi = odev.get("teslim_tarihi", "")
    gec = today > teslim_tarihi if teslim_tarihi else False

    if existing:
        # Guncelle
        existing["teslim_tarihi"] = today
        existing["durum"] = "teslim_edildi"
        existing["gec_teslim"] = gec
        if req.dosya_url:
            existing["dosya_url"] = req.dosya_url
        if req.not_:
            existing["not"] = req.not_
        adapter.save(DataPaths.HOMEWORK_SUBMISSIONS, teslimler)
        return {"id": existing["id"], "updated": True}

    # Yeni teslim
    yeni = {
        "id": f"ot_{uuid.uuid4().hex[:8]}",
        "odev_id": req.odev_id,
        "student_id": sid,
        "teslim_tarihi": today,
        "puan": None,
        "durum": "teslim_edildi",
        "gec_teslim": gec,
        "dosya_url": req.dosya_url or "",
        "not": req.not_,
    }
    adapter.append(DataPaths.HOMEWORK_SUBMISSIONS, yeni)
    return {"id": yeni["id"], "created": True}
