"""Veli endpoint'leri — cocuk ozet, kapsul, randevu, belge."""
from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.veli import (
    BELGE_TURLERI,
    BelgeTalebiItem,
    BelgeTalebiRequest,
    BelgeTalepListResponse,
    CocukOzetResponse,
    GeriBildirimRequest,
    GunlukKapsulItem,
    KapsulListResponse,
    RandevuAlRequest,
    RandevuItem,
    RandevuListResponse,
)


router = APIRouter(prefix="/veli", tags=["Veli"])


# Path kisayollari — DataPaths'te yok olanlari burada tanimla
class VeliPaths:
    KAPSULLER = "veli_gunluk_kapsul/kapsuller.json"
    RANDEVULAR = "akademik/veli_randevular.json"
    BELGE_TALEPLERI = "akademik/veli_belge_talepleri.json"
    GERI_BILDIRIM = "akademik/veli_geri_bildirim.json"


def _require_veli(user: dict) -> list[str]:
    """Veli rolu kontrolu + cocuklar listesi."""
    role = user.get("role", "").lower()
    if role not in ("veli", "superadmin", "yonetici", "mudur"):
        raise HTTPException(403, "Sadece veli bu endpoint'i kullanabilir")
    return user.get("children_ids", [])


def _validate_student_id(user: dict, student_id: str | None) -> str:
    """Veli sadece kendi cocuguna bakabilir."""
    children = _require_veli(user)
    if student_id and student_id in children:
        return student_id
    if children:
        return children[0]
    if user.get("role", "").lower() in ("superadmin", "yonetici", "mudur"):
        if not student_id:
            raise HTTPException(400, "student_id zorunlu")
        return student_id
    raise HTTPException(400, "Kayitli cocuk yok")


# ══════════════════════════════════════════════════════════════
# COCUKLARIM — Veli'nin cocuk listesi + ozet
# ══════════════════════════════════════════════════════════════

@router.get("/cocuklarim", response_model=list[CocukOzetResponse])
async def cocuklarim(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Velinin cocuklari + her biri icin ozet."""
    children = _require_veli(user)
    if not children:
        return []

    students = adapter.load(DataPaths.STUDENTS) or []
    grades = adapter.load(DataPaths.GRADES) or []
    att = adapter.load(DataPaths.ATTENDANCE) or []
    odevler = adapter.load(DataPaths.HOMEWORK) or []
    teslimler = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
    kapsuller = adapter.load(VeliPaths.KAPSULLER) or []

    # Mood
    mood_data = adapter.load(DataPaths.MOOD_CHECKINS) or []

    # EU risk
    risk_data = adapter.load(DataPaths.DVR_RISK) or []
    risk_by_sid = {r.get("student_id"): r for r in risk_data}

    today = date.today().isoformat()
    month_ago = (date.today() - timedelta(days=30)).isoformat()

    out: list[CocukOzetResponse] = []
    for sid in children:
        s = next((x for x in students if x.get("id") == sid), None)
        if not s:
            continue

        # Not ortalamasi (bu donem)
        now = datetime.now()
        curr_donem = "1. Donem" if now.month >= 9 or now.month <= 1 else "2. Donem"
        donem_grades = [
            g for g in grades
            if g.get("student_id") == sid and g.get("donem") == curr_donem
        ]
        not_ort = (
            round(sum(float(g.get("puan", 0)) for g in donem_grades) / len(donem_grades), 1)
            if donem_grades else 0.0
        )

        # Devamsizlik (bu donem)
        devamsizlik = sum(
            1 for a in att
            if a.get("student_id") == sid
            and a.get("turu", "").lower() in ("devamsiz", "ozursuz")
        )

        # Odev
        student_sinif = str(s.get("sinif", ""))
        student_sube = s.get("sube", "")
        cocuk_odevler = [
            o for o in odevler
            if str(o.get("sinif", "")) == student_sinif
            and o.get("sube", "") == student_sube
        ]
        cocuk_teslimler = {t.get("odev_id") for t in teslimler
                          if t.get("student_id") == sid}
        bekleyen = 0
        geciken = 0
        for o in cocuk_odevler:
            if o.get("id") in cocuk_teslimler:
                continue
            teslim_tarihi = o.get("teslim_tarihi", "")
            if teslim_tarihi and teslim_tarihi < today:
                geciken += 1
            else:
                bekleyen += 1

        # Mood (son 30 gun ortalama)
        cocuk_mood = [
            m for m in mood_data
            if m.get("student_id") == sid and m.get("tarih", "") >= month_ago
        ]
        mood_ort = (
            round(sum(int(m.get("level", 3)) for m in cocuk_mood) / len(cocuk_mood), 2)
            if cocuk_mood else 0.0
        )

        # Son kapsul tarihi
        cocuk_kapsuller = [k for k in kapsuller if k.get("student_id") == sid]
        son_kapsul = max((k.get("tarih", "") for k in cocuk_kapsuller), default=None)

        # Risk
        risk = risk_by_sid.get(sid)
        risk_var = False
        risk_seviye = ""
        if risk:
            skor = risk.get("behavioral_risk_score", 0)
            risk_seviye = risk.get("behavioral_risk_level", "LOW")
            risk_var = skor >= 45

        out.append(CocukOzetResponse(
            student_id=sid,
            ad_soyad=f"{s.get('ad','')} {s.get('soyad','')}".strip(),
            sinif=str(s.get("sinif", "")),
            sube=s.get("sube", ""),
            numara=s.get("numara", ""),
            not_ortalamasi=not_ort,
            devamsizlik_sayisi=devamsizlik,
            bekleyen_odev=bekleyen,
            geciken_odev=geciken,
            bu_ay_mood_ortalamasi=mood_ort,
            son_kapsul_tarih=son_kapsul,
            risk_var=risk_var,
            risk_seviyesi=risk_seviye,
        ))

    return out


# ══════════════════════════════════════════════════════════════
# GUNLUK KAPSUL — AI uretimli ozet
# ══════════════════════════════════════════════════════════════

@router.get("/kapsul", response_model=KapsulListResponse)
async def get_kapsuller(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
    limit: int = 30,
):
    """Cocugun son N gunluk kapsul ozeti."""
    sid = _validate_student_id(user, student_id)
    kapsuller = adapter.load(VeliPaths.KAPSULLER) or []
    mine = [k for k in kapsuller if k.get("student_id") == sid]
    mine.sort(key=lambda k: k.get("tarih", ""), reverse=True)

    today = date.today().isoformat()
    bugunku = next((k for k in mine if k.get("tarih") == today), None)

    items = [
        GunlukKapsulItem(
            id=k.get("id", ""),
            tarih=k.get("tarih", ""),
            student_id=k.get("student_id", ""),
            student_name=k.get("student_name", ""),
            akademik=k.get("akademik", {}),
            sosyal_duygusal=k.get("sosyal_duygusal", {}),
            etkinlik=k.get("etkinlik", {}),
            yarin_hazirlik=k.get("yarin_hazirlik", {}),
            ozel_an=k.get("ozel_an", {}),
            mood=k.get("mood", {}),
            ai_ozet=k.get("ai_ozet", k.get("ozet", "")),
            olusturma=k.get("olusturma", ""),
        )
        for k in mine[:limit]
    ]

    bugunku_item = next((i for i in items if i.tarih == today), None)

    return KapsulListResponse(kapsuller=items, bugunku=bugunku_item)


# ══════════════════════════════════════════════════════════════
# RANDEVU — Ogretmenle randevu alma
# ══════════════════════════════════════════════════════════════

@router.get("/randevularim", response_model=RandevuListResponse)
async def randevularim(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Velinin tum randevulari."""
    children = _require_veli(user)
    all_r = adapter.load(VeliPaths.RANDEVULAR) or []
    mine = [r for r in all_r if r.get("student_id") in children]
    today = date.today().isoformat()

    aktif = sorted(
        [r for r in mine
         if r.get("tarih", "") >= today and r.get("durum", "") not in ("iptal", "tamamlandi")],
        key=lambda r: (r.get("tarih", ""), r.get("saat", "")),
    )
    gecmis = sorted(
        [r for r in mine
         if r.get("tarih", "") < today or r.get("durum", "") in ("iptal", "tamamlandi")],
        key=lambda r: r.get("tarih", ""),
        reverse=True,
    )

    def _to_item(r):
        return RandevuItem(
            id=r.get("id", ""),
            student_id=r.get("student_id", ""),
            veli_adi=r.get("veli_adi", ""),
            ogretmen_id=r.get("ogretmen_id", ""),
            ogretmen_adi=r.get("ogretmen_adi", ""),
            tarih=r.get("tarih", ""),
            saat=r.get("saat", ""),
            konu=r.get("konu", ""),
            durum=r.get("durum", ""),
            notlar=r.get("notlar", ""),
        )

    return RandevuListResponse(
        aktif=[_to_item(r) for r in aktif],
        gecmis=[_to_item(r) for r in gecmis[:20]],
    )


@router.post("/randevu/al", response_model=RandevuItem, status_code=201)
async def randevu_al(
    req: RandevuAlRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yeni randevu talebi olustur (durum=beklemede)."""
    sid = _validate_student_id(user, req.student_id)

    yeni = {
        "id": f"rnd_{uuid.uuid4().hex[:8]}",
        "student_id": sid,
        "veli_adi": user.get("ad_soyad", ""),
        "ogretmen_id": req.ogretmen_id,
        "ogretmen_adi": req.ogretmen_adi,
        "tarih": req.tarih,
        "saat": req.saat,
        "konu": req.konu,
        "durum": "beklemede",
        "notlar": "",
    }
    adapter.append(VeliPaths.RANDEVULAR, yeni)

    return RandevuItem(**{k: v for k, v in yeni.items() if k in RandevuItem.model_fields})


@router.post("/randevu/{rid}/iptal")
async def randevu_iptal(
    rid: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Randevu iptal."""
    children = _require_veli(user)
    ok = adapter.update_by_id(VeliPaths.RANDEVULAR, rid, {"durum": "iptal"})
    if not ok:
        raise HTTPException(404, "Randevu bulunamadi")
    return {"ok": True}


# ══════════════════════════════════════════════════════════════
# BELGE TALEBI
# ══════════════════════════════════════════════════════════════

@router.get("/belge/turler")
async def belge_turler(_: Annotated[dict, Depends(get_current_user)]):
    """Mevcut belge turleri."""
    return {"turler": BELGE_TURLERI}


@router.get("/belge/taleplerim", response_model=BelgeTalepListResponse)
async def belge_taleplerim(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Velinin belge talepleri."""
    children = _require_veli(user)
    all_t = adapter.load(VeliPaths.BELGE_TALEPLERI) or []
    mine = [t for t in all_t if t.get("student_id") in children]
    mine.sort(key=lambda t: t.get("talep_tarihi", ""), reverse=True)

    talepler = [
        BelgeTalebiItem(
            id=t.get("id", ""),
            student_id=t.get("student_id", ""),
            veli_adi=t.get("veli_adi", ""),
            belge_turu=t.get("belge_turu", ""),
            aciklama=t.get("aciklama", ""),
            durum=t.get("durum", "bekliyor"),
            talep_tarihi=t.get("talep_tarihi", ""),
            teslim_tarihi=t.get("teslim_tarihi"),
        )
        for t in mine
    ]
    return BelgeTalepListResponse(talepler=talepler)


@router.post("/belge/talep", response_model=BelgeTalebiItem, status_code=201)
async def belge_talep(
    req: BelgeTalebiRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yeni belge talebi."""
    sid = _validate_student_id(user, req.student_id)
    if req.belge_turu not in BELGE_TURLERI:
        raise HTTPException(400, f"Gecersiz belge turu. Secenek: {BELGE_TURLERI}")

    yeni = {
        "id": f"blg_{uuid.uuid4().hex[:8]}",
        "student_id": sid,
        "veli_adi": user.get("ad_soyad", ""),
        "belge_turu": req.belge_turu,
        "aciklama": req.aciklama,
        "durum": "bekliyor",
        "talep_tarihi": datetime.now().isoformat(),
        "teslim_tarihi": None,
    }
    adapter.append(VeliPaths.BELGE_TALEPLERI, yeni)

    return BelgeTalebiItem(
        id=yeni["id"], student_id=yeni["student_id"], veli_adi=yeni["veli_adi"],
        belge_turu=yeni["belge_turu"], aciklama=yeni["aciklama"],
        durum=yeni["durum"], talep_tarihi=yeni["talep_tarihi"],
    )


# ══════════════════════════════════════════════════════════════
# GERI BILDIRIM
# ══════════════════════════════════════════════════════════════

@router.post("/geri-bildirim", status_code=201)
async def geri_bildirim(
    req: GeriBildirimRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Veli memnuniyet / oneri / sikayet geri bildirimi."""
    _require_veli(user)
    yeni = {
        "id": f"gb_{uuid.uuid4().hex[:8]}",
        "veli_id": user.get("user_id", ""),
        "veli_adi": user.get("ad_soyad", ""),
        "student_id": req.student_id,
        "kategori": req.kategori,
        "puan": req.puan,
        "mesaj": req.mesaj,
        "tarih": datetime.now().isoformat(),
        "durum": "yeni",
    }
    adapter.append(VeliPaths.GERI_BILDIRIM, yeni)
    return {"ok": True, "id": yeni["id"]}
