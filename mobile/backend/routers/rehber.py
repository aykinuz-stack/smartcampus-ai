"""Rehber endpoint'leri — vaka, gorusme, aile formu, mood paneli."""
from __future__ import annotations

import uuid
from collections import Counter
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.rehber import (
    AileFormCreateRequest,
    AileFormItem,
    GorusmeCreateRequest,
    GorusmeItem,
    VAKA_KONULARI,
    VakaCreateRequest,
    VakaItem,
)


router = APIRouter(prefix="/rehber", tags=["Rehber"])


def _require_rehber(user: dict):
    role = user.get("role", "").lower()
    if role not in ("rehber", "psikolog", "calisan",
                    "superadmin", "yonetici", "mudur", "mudur_yardimcisi"):
        raise HTTPException(403, "Sadece rehber/psikolog bu endpoint'i kullanabilir")


# ══════════════════════════════════════════════════════════════
# VAKA
# ══════════════════════════════════════════════════════════════

@router.get("/vakalar", response_model=list[VakaItem])
async def vakalar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    durum: str | None = None,
    konu: str | None = None,
    limit: int = 100,
):
    """Rehberin tum vakalari (filtre destekli)."""
    _require_rehber(user)
    all_v = adapter.load(DataPaths.VAKA) or []
    if durum:
        all_v = [v for v in all_v if v.get("durum") == durum]
    if konu:
        all_v = [v for v in all_v if v.get("konu") == konu]
    all_v.sort(key=lambda v: v.get("acilis_tarihi", ""), reverse=True)

    return [
        VakaItem(
            id=v.get("id", ""), student_id=v.get("student_id", ""),
            ogrenci_adi=v.get("ogrenci_adi", ""),
            sinif=v.get("sinif", ""), sube=v.get("sube", ""),
            konu=v.get("konu", ""), aciklama=v.get("aciklama", ""),
            oncelik=v.get("oncelik", "orta"), durum=v.get("durum", "acik"),
            acilis_tarihi=v.get("acilis_tarihi", ""),
            kapatis_tarihi=v.get("kapatis_tarihi"),
        )
        for v in all_v[:limit]
    ]


@router.post("/vaka", response_model=VakaItem, status_code=201)
async def vaka_ac(
    req: VakaCreateRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yeni vaka ac."""
    _require_rehber(user)
    if req.konu not in VAKA_KONULARI:
        raise HTTPException(400, f"Gecersiz konu. Secenek: {VAKA_KONULARI}")

    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == req.student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci yok")

    yeni = {
        "id": f"vaka_{uuid.uuid4().hex[:8]}",
        "student_id": req.student_id,
        "ogrenci_adi": f"{s.get('ad','')} {s.get('soyad','')}".strip(),
        "sinif": s.get("sinif", ""), "sube": s.get("sube", ""),
        "konu": req.konu, "aciklama": req.aciklama,
        "oncelik": req.oncelik, "durum": "acik",
        "acilis_tarihi": datetime.now().isoformat(),
        "kapatis_tarihi": None,
    }
    adapter.append(DataPaths.VAKA, yeni)
    return VakaItem(**{k: v for k, v in yeni.items() if k in VakaItem.model_fields})


@router.post("/vaka/{vid}/kapat")
async def vaka_kapat(
    vid: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_rehber(user)
    ok = adapter.update_by_id(DataPaths.VAKA, vid, {
        "durum": "cozuldu",
        "kapatis_tarihi": datetime.now().isoformat(),
    })
    if not ok:
        raise HTTPException(404, "Vaka bulunamadi")
    return {"ok": True}


# ══════════════════════════════════════════════════════════════
# GORUSME
# ══════════════════════════════════════════════════════════════

@router.get("/gorusmeler", response_model=list[GorusmeItem])
async def gorusmeler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    student_id: str | None = None,
    vaka_id: str | None = None,
    limit: int = 100,
):
    _require_rehber(user)
    all_g = adapter.load(DataPaths.GORUSME) or []
    if student_id:
        all_g = [g for g in all_g if g.get("student_id") == student_id]
    if vaka_id:
        all_g = [g for g in all_g if g.get("vaka_id") == vaka_id]
    all_g.sort(key=lambda g: g.get("tarih", ""), reverse=True)

    return [
        GorusmeItem(
            id=g.get("id", ""), vaka_id=g.get("vaka_id"),
            student_id=g.get("student_id", ""), tarih=g.get("tarih", ""),
            sure_dakika=int(g.get("sure_dakika", 0) or 0),
            gorusen=g.get("gorusen", ""), notlar=g.get("notlar", ""),
            sonraki_adim=g.get("sonraki_adim", ""),
        )
        for g in all_g[:limit]
    ]


@router.post("/gorusme", response_model=GorusmeItem, status_code=201)
async def gorusme_ekle(
    req: GorusmeCreateRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_rehber(user)
    yeni = {
        "id": f"gor_{uuid.uuid4().hex[:8]}",
        "vaka_id": req.vaka_id,
        "student_id": req.student_id,
        "tarih": datetime.now().isoformat(),
        "sure_dakika": req.sure_dakika,
        "gorusen": user.get("ad_soyad", ""),
        "notlar": req.notlar,
        "sonraki_adim": req.sonraki_adim,
    }
    adapter.append(DataPaths.GORUSME, yeni)
    return GorusmeItem(**yeni)


# ══════════════════════════════════════════════════════════════
# AILE FORMU
# ══════════════════════════════════════════════════════════════

@router.get("/aile-form/{student_id}", response_model=AileFormItem | None)
async def aile_form_get(
    student_id: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_rehber(user)
    all_f = adapter.load(DataPaths.AILE_FORM) or []
    mine = [f for f in all_f if f.get("student_id") == student_id]
    if not mine:
        return None
    latest = max(mine, key=lambda f: f.get("tarih", ""))
    return AileFormItem(**{k: v for k, v in latest.items()
                          if k in AileFormItem.model_fields})


@router.post("/aile-form", response_model=AileFormItem, status_code=201)
async def aile_form_ekle(
    req: AileFormCreateRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_rehber(user)
    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == req.student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci yok")

    yeni = {
        "id": f"aile_{uuid.uuid4().hex[:8]}",
        "student_id": req.student_id,
        "ogrenci_adi": f"{s.get('ad','')} {s.get('soyad','')}".strip(),
        "anne_egitim": req.anne_egitim, "baba_egitim": req.baba_egitim,
        "anne_meslek": req.anne_meslek, "baba_meslek": req.baba_meslek,
        "kardes_sayisi": req.kardes_sayisi,
        "aile_durumu": req.aile_durumu, "ev_durumu": req.ev_durumu,
        "ozel_durum": req.ozel_durum,
        "tarih": datetime.now().isoformat(),
    }
    adapter.append(DataPaths.AILE_FORM, yeni)
    return AileFormItem(**{k: v for k, v in yeni.items()
                          if k in AileFormItem.model_fields})


# ══════════════════════════════════════════════════════════════
# MOOD PANELI — REHBER ICIN
# ══════════════════════════════════════════════════════════════

@router.get("/mood-panel")
async def mood_panel(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    days: int = 14,
):
    """Tum ogrencilerin son N gun mood ozeti — riskli olanlari isaretler."""
    _require_rehber(user)

    cutoff = (date.today() - timedelta(days=days)).isoformat()
    all_mood = adapter.load(DataPaths.MOOD_CHECKINS) or []
    recent = [m for m in all_mood if m.get("tarih", "") >= cutoff]

    # Ogrenci bazli grup
    by_student: dict[str, list] = {}
    for m in recent:
        sid = m.get("student_id", "")
        by_student.setdefault(sid, []).append(m)

    riskli = []
    for sid, kayitlar in by_student.items():
        negatif_gun = sum(1 for k in kayitlar if int(k.get("level", 3)) <= 2)
        if negatif_gun >= 3:
            ortalama = sum(int(k.get("level", 3)) for k in kayitlar) / len(kayitlar)
            riskli.append({
                "student_id": sid,
                "student_name": kayitlar[0].get("student_name", "?"),
                "negatif_gun": negatif_gun,
                "toplam_kayit": len(kayitlar),
                "ortalama": round(ortalama, 2),
                "son_check_in": max(k.get("tarih", "") for k in kayitlar),
            })

    riskli.sort(key=lambda r: r["negatif_gun"], reverse=True)

    # Genel istatistik
    all_levels = [int(m.get("level", 3)) for m in recent]
    gen_ort = round(sum(all_levels) / len(all_levels), 2) if all_levels else 0.0

    return {
        "genel_ortalama": gen_ort,
        "toplam_checkin": len(recent),
        "aktif_ogrenci_sayisi": len(by_student),
        "riskli_ogrenciler": riskli[:30],
    }


# ══════════════════════════════════════════════════════════════
# IHBAR INCELEME — REHBER/PSIKOLOG
# ══════════════════════════════════════════════════════════════

@router.get("/ihbar-liste")
async def ihbar_liste(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    durum: str | None = None,
    kategori: str | None = None,
):
    """Anonim ihbarlar (rehber incelemesi icin)."""
    _require_rehber(user)
    all_i = adapter.load(DataPaths.IHBAR) or []
    if durum:
        all_i = [i for i in all_i if i.get("durum") == durum]
    if kategori:
        all_i = [i for i in all_i if i.get("kategori") == kategori]
    all_i.sort(key=lambda i: i.get("olusturma_tarihi", ""), reverse=True)
    return all_i[:100]


@router.post("/ihbar/{anonim_id}/durum-guncelle")
async def ihbar_durum_guncelle(
    anonim_id: str,
    yeni_durum: str,
    not_metni: str = "",
    user: Annotated[dict, Depends(get_current_user)] = None,
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)] = None,
):
    _require_rehber(user)
    all_i = adapter.load(DataPaths.IHBAR) or []
    for idx, i in enumerate(all_i):
        if i.get("anonim_id") == anonim_id:
            all_i[idx]["durum"] = yeni_durum
            all_i[idx]["guncelleme_tarihi"] = datetime.now().isoformat()
            if not_metni:
                all_i[idx].setdefault("rehber_notlari", []).append({
                    "tarih": datetime.now().isoformat(),
                    "not": not_metni,
                    "rehber": user.get("ad_soyad", ""),
                })
            adapter.save(DataPaths.IHBAR, all_i)
            return {"ok": True}
    raise HTTPException(404, "Ihbar bulunamadi")


# ══════════════════════════════════════════════════════════════
# YÖNLENDİRME (SEVK)
# ══════════════════════════════════════════════════════════════

YONLENDIRME_TURLERI = [
    "RAM", "Hastane", "CIMER", "Sosyal Hizmet", "Polis/Jandarma",
    "Aile Danışmanlığı", "Psikiyatri", "Dil Terapisi", "Diğer",
]

@router.get("/yonlendirmeler")
async def yonlendirmeler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    durum: str | None = None,
):
    _require_rehber(user)
    items = adapter.load(DataPaths.YONLENDIRME) or []
    if durum:
        items = [i for i in items if i.get("durum") == durum]
    items.sort(key=lambda i: i.get("tarih", ""), reverse=True)
    return items[:100]


@router.post("/yonlendirme", status_code=201)
async def yonlendirme_ekle(
    student_id: str,
    tur: str,
    kurum: str = "",
    aciklama: str = "",
    user: Annotated[dict, Depends(get_current_user)] = None,
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)] = None,
):
    _require_rehber(user)
    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci yok")

    yeni = {
        "id": f"yon_{uuid.uuid4().hex[:8]}",
        "student_id": student_id,
        "ogrenci_adi": f"{s.get('ad', '')} {s.get('soyad', '')}".strip(),
        "sinif": str(s.get("sinif", "")),
        "sube": s.get("sube", ""),
        "tur": tur,
        "kurum": kurum,
        "aciklama": aciklama,
        "durum": "beklemede",
        "tarih": datetime.now().isoformat(),
        "rehber": user.get("ad_soyad", user.get("name", "")),
    }
    adapter.append(DataPaths.YONLENDIRME, yeni)
    return yeni


# ══════════════════════════════════════════════════════════════
# RİSK DEĞERLENDİRME
# ══════════════════════════════════════════════════════════════

@router.get("/risk-degerlendirme")
async def risk_degerlendirme_list(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_rehber(user)
    items = adapter.load(DataPaths.RISK_DEGER) or []
    items.sort(key=lambda i: i.get("tarih", ""), reverse=True)
    return items[:100]


@router.post("/risk-degerlendirme", status_code=201)
async def risk_degerlendirme_ekle(
    student_id: str,
    risk_alanlari: str = "",
    risk_seviyesi: str = "orta",
    aciklama: str = "",
    oneri: str = "",
    user: Annotated[dict, Depends(get_current_user)] = None,
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)] = None,
):
    _require_rehber(user)
    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci yok")

    yeni = {
        "id": f"risk_{uuid.uuid4().hex[:8]}",
        "student_id": student_id,
        "ogrenci_adi": f"{s.get('ad', '')} {s.get('soyad', '')}".strip(),
        "sinif": str(s.get("sinif", "")),
        "sube": s.get("sube", ""),
        "risk_alanlari": risk_alanlari,
        "risk_seviyesi": risk_seviyesi,
        "aciklama": aciklama,
        "oneri": oneri,
        "tarih": datetime.now().isoformat(),
        "rehber": user.get("ad_soyad", user.get("name", "")),
    }
    adapter.append(DataPaths.RISK_DEGER, yeni)
    return yeni


# ══════════════════════════════════════════════════════════════
# KRİZ MÜDAHALE
# ══════════════════════════════════════════════════════════════

KRIZ_TURLERI = [
    "İntihar Riski", "Öz Zarar", "Şiddet/Saldırganlık", "İstismar Şüphesi",
    "Madde Kullanımı", "Aile İçi Şiddet", "Kayıp/Yas", "Doğal Afet", "Diğer",
]

@router.get("/kriz-kayitlari")
async def kriz_list(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_rehber(user)
    items = adapter.load(DataPaths.KRIZ) or []
    items.sort(key=lambda i: i.get("tarih", ""), reverse=True)
    return items[:100]


@router.post("/kriz-kayit", status_code=201)
async def kriz_ekle(
    student_id: str,
    kriz_turu: str,
    acil_durum: str = "hayir",
    yapilan_mudahale: str = "",
    bilgilendirilen: str = "",
    user: Annotated[dict, Depends(get_current_user)] = None,
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)] = None,
):
    _require_rehber(user)
    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci yok")

    yeni = {
        "id": f"kriz_{uuid.uuid4().hex[:8]}",
        "student_id": student_id,
        "ogrenci_adi": f"{s.get('ad', '')} {s.get('soyad', '')}".strip(),
        "sinif": str(s.get("sinif", "")),
        "sube": s.get("sube", ""),
        "kriz_turu": kriz_turu,
        "acil_durum": acil_durum,
        "yapilan_mudahale": yapilan_mudahale,
        "bilgilendirilen": bilgilendirilen,
        "durum": "acik",
        "tarih": datetime.now().isoformat(),
        "rehber": user.get("ad_soyad", user.get("name", "")),
    }
    adapter.append(DataPaths.KRIZ, yeni)
    return yeni


# ══════════════════════════════════════════════════════════════
# GELİŞİM DOSYASI
# ══════════════════════════════════════════════════════════════

@router.get("/gelisim-dosyasi/{student_id}")
async def gelisim_dosyasi(
    student_id: str,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Öğrencinin tüm rehberlik geçmişini tek dosyada toplar."""
    _require_rehber(user)

    students = adapter.load(DataPaths.STUDENTS) or []
    s = next((x for x in students if x.get("id") == student_id), None)
    if not s:
        raise HTTPException(404, "Ogrenci yok")

    vakalar = [v for v in (adapter.load(DataPaths.VAKA) or []) if v.get("student_id") == student_id]
    gorusmeler = [g for g in (adapter.load(DataPaths.GORUSME) or []) if g.get("student_id") == student_id]
    aile = [f for f in (adapter.load(DataPaths.AILE_FORM) or []) if f.get("student_id") == student_id]
    yonlendirmeler = [y for y in (adapter.load(DataPaths.YONLENDIRME) or []) if y.get("student_id") == student_id]
    riskler = [r for r in (adapter.load(DataPaths.RISK_DEGER) or []) if r.get("student_id") == student_id]
    krizler = [k for k in (adapter.load(DataPaths.KRIZ) or []) if k.get("student_id") == student_id]

    # Mood
    moods = [m for m in (adapter.load(DataPaths.MOOD_CHECKINS) or []) if m.get("student_id") == student_id]
    mood_ort = round(sum(int(m.get("level", 3)) for m in moods) / len(moods), 2) if moods else 0

    return {
        "ogrenci": {
            "id": student_id,
            "ad_soyad": f"{s.get('ad', '')} {s.get('soyad', '')}".strip(),
            "sinif": str(s.get("sinif", "")),
            "sube": s.get("sube", ""),
        },
        "vaka_sayisi": len(vakalar),
        "gorusme_sayisi": len(gorusmeler),
        "yonlendirme_sayisi": len(yonlendirmeler),
        "risk_sayisi": len(riskler),
        "kriz_sayisi": len(krizler),
        "mood_ortalamasi": mood_ort,
        "vakalar": vakalar[-5:],
        "gorusmeler": gorusmeler[-5:],
        "aile_formu": aile[-1] if aile else None,
        "yonlendirmeler": yonlendirmeler[-5:],
        "riskler": riskler[-5:],
        "krizler": krizler[-3:],
    }
