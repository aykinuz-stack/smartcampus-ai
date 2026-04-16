"""Yonetici endpoint'leri — dashboard, erken uyari, onaylar."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..core.data_adapter import DataAdapter, DataPaths
from ..core.deps import get_current_user, get_data_adapter
from ..schemas.yonetici import (
    DashboardResponse,
    OnayAksiyonRequest,
    OnayIstegiItem,
    RiskOzetResponse,
)


router = APIRouter(prefix="/yonetici", tags=["Yonetici"])


def _require_yonetici(user: dict):
    role = user.get("role", "").lower()
    if role not in ("superadmin", "yonetici", "mudur", "mudur_yardimcisi"):
        raise HTTPException(403, "Sadece yonetici bu endpoint'i kullanabilir")


# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════

@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Yonetici ana sayfa metrikleri."""
    _require_yonetici(user)
    today = date.today().isoformat()

    students = adapter.load(DataPaths.STUDENTS) or []
    teachers = adapter.load(DataPaths.TEACHERS) or []
    att = adapter.load(DataPaths.ATTENDANCE) or []
    vakalar = adapter.load(DataPaths.VAKA) or []
    ihbarlar = adapter.load(DataPaths.IHBAR) or []
    risk_data = adapter.load(DataPaths.DVR_RISK) or []
    randevular = adapter.load("akademik/veli_randevular.json") or []
    belgeler = adapter.load("akademik/veli_belge_talepleri.json") or []

    aktif_ogr = sum(1 for s in students if s.get("durum", "aktif") == "aktif")
    aktif_ogt = sum(1 for t in teachers if t.get("durum", "aktif") == "aktif")

    # Bugun yoklama alinan sinif
    today_att = [a for a in att if a.get("tarih") == today]
    sinif_kombos = {(a.get("student_id", ""), a.get("ders", ""), a.get("ders_saati", ""))
                    for a in today_att}
    yoklama_alinan = len({(a.get("ders", ""), a.get("ders_saati", "")) for a in today_att})
    bugun_devamsiz = sum(1 for a in today_att
                        if a.get("turu", "").lower() in ("devamsiz", "ozursuz"))

    # Acik vaka
    acik_vaka = sum(1 for v in vakalar if v.get("durum") in ("acik", "devam"))

    # Bekleyen ihbar
    bekleyen_ihbar = sum(1 for i in ihbarlar if i.get("durum", "Yeni") == "Yeni")

    # Kritik risk
    kritik_risk = sum(1 for r in risk_data
                     if r.get("behavioral_risk_score", 0) >= 70)

    # Bekleyen onaylar (randevu + belge)
    bekleyen_onay = (
        sum(1 for r in randevular if r.get("durum") == "beklemede") +
        sum(1 for b in belgeler if b.get("durum") == "bekliyor")
    )

    return DashboardResponse(
        toplam_ogrenci=aktif_ogr,
        toplam_ogretmen=aktif_ogt,
        bugun_yoklama_alinan_sinif=yoklama_alinan,
        bugun_devamsiz=bugun_devamsiz,
        acik_vaka=acik_vaka,
        bekleyen_ihbar=bekleyen_ihbar,
        kritik_risk_ogrenci=kritik_risk,
        bekleyen_onay=bekleyen_onay,
    )


# ══════════════════════════════════════════════════════════════
# ERKEN UYARI OZETI
# ══════════════════════════════════════════════════════════════

@router.get("/erken-uyari/ozet", response_model=list[RiskOzetResponse])
async def erken_uyari_ozet(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Kategori bazli risk ozeti (Butuncul Risk 20-Boyut)."""
    _require_yonetici(user)
    risk_data = adapter.load(DataPaths.DVR_RISK) or []

    # Unique — en son hesaplama
    latest = {}
    for r in risk_data:
        sid = r.get("student_id", "")
        if sid not in latest or r.get("calculated_at", "") > latest[sid].get("calculated_at", ""):
            latest[sid] = r
    records = list(latest.values())

    kategoriler_map = {
        "zorbalik_pattern": "Zorbalık",
        "kendine_zarar_intihar": "İntihar Riski",
        "madde_kullanim_supheli": "Madde Şüphesi",
        "duygusal_kizilbayrak": "Duygusal",
        "aile_risk": "Aile Riski",
        "kronik_devamsizlik": "Kronik Devamsızlık",
        "disiplin_sikligi": "Disiplin",
        "sosyal_izolasyon": "Sosyal İzolasyon",
        "sosyoekonomik_stres": "Sosyoekonomik",
    }

    out = []
    for key, label in kategoriler_map.items():
        izlenen = sum(1 for r in records if 25 <= r.get(key, 0) < 45)
        yuksek = sum(1 for r in records if 45 <= r.get(key, 0) < 70)
        kritik = sum(1 for r in records if r.get(key, 0) >= 70)
        out.append(RiskOzetResponse(
            kategori=label, izlenen=izlenen, yuksek=yuksek, kritik=kritik,
            toplam=izlenen + yuksek + kritik,
        ))

    return out


@router.get("/erken-uyari/riskli-ogrenciler")
async def riskli_ogrenciler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    min_skor: float = 45,
    limit: int = 30,
):
    _require_yonetici(user)
    risk_data = adapter.load(DataPaths.DVR_RISK) or []
    latest = {}
    for r in risk_data:
        sid = r.get("student_id", "")
        if sid not in latest or r.get("calculated_at", "") > latest[sid].get("calculated_at", ""):
            latest[sid] = r

    filtered = [r for r in latest.values()
               if r.get("behavioral_risk_score", 0) >= min_skor]
    filtered.sort(key=lambda r: r.get("behavioral_risk_score", 0), reverse=True)
    return filtered[:limit]


# ══════════════════════════════════════════════════════════════
# ONAYLAR — birlesik liste (randevu + belge)
# ══════════════════════════════════════════════════════════════

@router.get("/onaylar", response_model=list[OnayIstegiItem])
async def onaylar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_yonetici(user)
    out = []
    # Randevular
    for r in adapter.load("akademik/veli_randevular.json") or []:
        if r.get("durum") == "beklemede":
            out.append(OnayIstegiItem(
                id=r.get("id", ""),
                tur="randevu",
                baslik=f"Randevu: {r.get('konu', '')}",
                aciklama=f"{r.get('ogretmen_adi', '')} ile {r.get('tarih', '')} {r.get('saat', '')}",
                talep_eden=r.get("veli_adi", ""),
                tarih=r.get("tarih", ""),
                durum=r.get("durum", ""),
            ))
    # Belge talepleri
    for b in adapter.load("akademik/veli_belge_talepleri.json") or []:
        if b.get("durum") == "bekliyor":
            out.append(OnayIstegiItem(
                id=b.get("id", ""),
                tur="belge",
                baslik=f"Belge: {b.get('belge_turu', '')}",
                aciklama=b.get("aciklama", ""),
                talep_eden=b.get("veli_adi", ""),
                tarih=(b.get("talep_tarihi", "") or "")[:10],
                durum=b.get("durum", ""),
            ))

    out.sort(key=lambda o: o.tarih, reverse=True)
    return out


@router.post("/onay-aksiyon")
async def onay_aksiyon(
    req: OnayAksiyonRequest,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    _require_yonetici(user)
    # Hem randevu hem belge aramak
    paths = ["akademik/veli_randevular.json", "akademik/veli_belge_talepleri.json"]
    for path in paths:
        data = adapter.load(path) or []
        for idx, item in enumerate(data):
            if item.get("id") == req.onay_id:
                if req.aksiyon == "onayla":
                    data[idx]["durum"] = "onaylandi" if "randevu" in path else "hazirlaniyor"
                elif req.aksiyon == "reddet":
                    data[idx]["durum"] = "iptal" if "randevu" in path else "iptal"
                data[idx]["onay_notu"] = req.not_metni
                adapter.save(path, data)
                return {"ok": True}
    raise HTTPException(404, "Onay istegi bulunamadi")
