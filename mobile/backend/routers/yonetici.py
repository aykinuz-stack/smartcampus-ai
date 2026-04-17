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


# ══════════════════════════════════════════════════════════════
# BUGUN OKULDA NE VAR?
# ══════════════════════════════════════════════════════════════

_GUN_MAP = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe",
           4: "Cuma", 5: "Cumartesi", 6: "Pazar"}


@router.get("/bugun-okulda")
async def bugun_okulda(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Gun basi — bugun okulda ne oluyor akisi."""
    _require_yonetici(user)
    today = date.today()
    today_str = today.isoformat()
    gun_adi = _GUN_MAP[today.weekday()]

    # Ders programi (bugun olan dersler)
    schedule = adapter.load("akademik/schedule.json") or []
    bugun_dersler = [
        s for s in schedule
        if s.get("gun", "").lower() == gun_adi.lower()
    ]
    # Saate gore sirala
    bugun_dersler.sort(key=lambda s: int(s.get("saat", 0) or 0))
    # Unique sinif+saat
    ders_ozet = {}
    for s in bugun_dersler:
        saat = int(s.get("saat", 0) or 0)
        ders_ozet.setdefault(saat, [])
        ders_ozet[saat].append({
            "sinif": f"{s.get('sinif','')}/{s.get('sube','')}",
            "ders": s.get("ders", ""),
            "ogretmen": s.get("ogretmen_adi", ""),
        })

    # Bugunku etkinlik / duyurular
    etkinlikler = adapter.load("akademik/etkinlik_duyurular.json") or []
    bugun_etk = [
        e for e in etkinlikler
        if e.get("tarih", "").startswith(today_str)
        and e.get("durum", "aktif") == "aktif"
    ]

    # Bugunku randevular
    randevular = adapter.load("akademik/veli_randevular.json") or []
    bugun_randevular = [
        r for r in randevular
        if r.get("tarih", "") == today_str
        and r.get("durum", "") not in ("iptal",)
    ]
    bugun_randevular.sort(key=lambda r: r.get("saat", ""))

    # Yoklama alinan sinif sayisi
    att = adapter.load("akademik/attendance.json") or []
    today_att = [a for a in att if a.get("tarih") == today_str]
    yoklama_sinif_sayisi = len({(a.get("ders", ""), a.get("ders_saati", ""))
                                for a in today_att})

    # Bugunku devamsizlik
    ozursuz = sum(1 for a in today_att
                 if a.get("turu", "").lower() in ("devamsiz", "ozursuz"))

    return {
        "tarih": today_str,
        "gun": gun_adi,
        "ders_programi": [
            {"saat": saat, "dersler": d}
            for saat, d in sorted(ders_ozet.items())
        ],
        "etkinlikler": [
            {"baslik": e.get("baslik"), "konum": e.get("konum", ""),
             "tarih": e.get("tarih"), "tur": e.get("tur", "")}
            for e in bugun_etk
        ],
        "randevular": [
            {"saat": r.get("saat"), "veli": r.get("veli_adi"),
             "ogretmen": r.get("ogretmen_adi"), "konu": r.get("konu"),
             "durum": r.get("durum")}
            for r in bugun_randevular
        ],
        "istatistik": {
            "yoklama_alinan_sinif": yoklama_sinif_sayisi,
            "bugun_devamsiz": ozursuz,
            "toplam_ders_saati": len(bugun_dersler),
        },
    }


# ══════════════════════════════════════════════════════════════
# BUTCE — GUNLUK AKIS
# ══════════════════════════════════════════════════════════════

@router.get("/butce-gunluk")
async def butce_gunluk(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    days: int = 30,
):
    """Son N gun gelir/gider akisi."""
    _require_yonetici(user)
    cutoff = (date.today() - timedelta(days=days)).isoformat()

    # Gider kayitlari
    gider = adapter.load("butce/gider_kayitlari.json") or []
    gelir = adapter.load("butce/gelir_kayitlari.json") or []

    gider_son = [g for g in gider if g.get("tarih", "") >= cutoff]
    gelir_son = [g for g in gelir if g.get("tarih", "") >= cutoff]

    # Gun bazli agrege
    gun_agrege: dict[str, dict] = {}
    for g in gelir_son:
        t = g.get("tarih", "")[:10]
        gun_agrege.setdefault(t, {"gelir": 0, "gider": 0})
        gun_agrege[t]["gelir"] += float(g.get("tutar", 0) or 0)
    for g in gider_son:
        t = g.get("tarih", "")[:10]
        gun_agrege.setdefault(t, {"gelir": 0, "gider": 0})
        gun_agrege[t]["gider"] += float(g.get("tutar", 0) or 0)

    gunluk_akis = sorted(
        [{"tarih": t, **v, "net": v["gelir"] - v["gider"]}
         for t, v in gun_agrege.items()],
        key=lambda x: x["tarih"], reverse=True
    )

    toplam_gelir = sum(g["gelir"] for g in gun_agrege.values())
    toplam_gider = sum(g["gider"] for g in gun_agrege.values())

    # Son 10 islem (genel)
    son_islemler = []
    for g in (gelir_son[-10:])[::-1]:
        son_islemler.append({
            "tip": "gelir",
            "tarih": g.get("tarih", "")[:10],
            "kategori": g.get("kategori", ""),
            "aciklama": g.get("aciklama", ""),
            "tutar": float(g.get("tutar", 0) or 0),
        })
    for g in (gider_son[-10:])[::-1]:
        son_islemler.append({
            "tip": "gider",
            "tarih": g.get("tarih", "")[:10],
            "kategori": g.get("kategori", ""),
            "aciklama": g.get("aciklama", ""),
            "tutar": float(g.get("tutar", 0) or 0),
        })
    son_islemler.sort(key=lambda x: x["tarih"], reverse=True)

    return {
        "toplam_gelir": round(toplam_gelir, 2),
        "toplam_gider": round(toplam_gider, 2),
        "net": round(toplam_gelir - toplam_gider, 2),
        "gunluk_akis": gunluk_akis[:30],
        "son_islemler": son_islemler[:20],
        "gun_sayisi": len(gun_agrege),
    }


# ══════════════════════════════════════════════════════════════
# RANDEVU (yonetici icin tum randevular)
# ══════════════════════════════════════════════════════════════

@router.get("/randevular")
async def randevular(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Okuldaki tum randevular."""
    _require_yonetici(user)
    randevular = adapter.load("akademik/veli_randevular.json") or []
    today = date.today().isoformat()

    bugun = [r for r in randevular if r.get("tarih") == today]
    yaklasilan = [r for r in randevular
                 if r.get("tarih", "") > today
                 and r.get("durum", "") not in ("iptal", "tamamlandi")]
    bekleyen = [r for r in randevular if r.get("durum") == "beklemede"]

    bugun.sort(key=lambda r: r.get("saat", ""))
    yaklasilan.sort(key=lambda r: (r.get("tarih", ""), r.get("saat", "")))
    bekleyen.sort(key=lambda r: r.get("tarih", ""))

    def _item(r):
        return {
            "id": r.get("id"),
            "student_id": r.get("student_id"),
            "veli": r.get("veli_adi"),
            "ogretmen": r.get("ogretmen_adi"),
            "tarih": r.get("tarih"),
            "saat": r.get("saat"),
            "konu": r.get("konu"),
            "durum": r.get("durum"),
        }

    return {
        "bugun": [_item(r) for r in bugun],
        "yaklasilan": [_item(r) for r in yaklasilan[:20]],
        "bekleyen": [_item(r) for r in bekleyen[:20]],
        "toplam": len(randevular),
    }
