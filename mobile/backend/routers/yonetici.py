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

# ══════════════════════════════════════════════════════════════
# GUN BASI + GUN SONU RAPORU
# ══════════════════════════════════════════════════════════════

@router.get("/gun-raporu")
async def gun_raporu(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Gun basi + gun sonu raporu — tek endpoint."""
    _require_yonetici(user)
    today = date.today().isoformat()
    gun_adi = _GUN_MAP[date.today().weekday()]

    # Ogrenci + ogretmen sayisi
    students = adapter.load("akademik/students.json") or []
    teachers = adapter.load("akademik/teachers.json") or []
    aktif_ogrenci = sum(1 for s in students if s.get("durum") == "aktif")
    aktif_ogretmen = len(teachers)

    # Yoklama
    att = adapter.load("akademik/attendance.json") or []
    bugun_att = [a for a in att if a.get("tarih") == today]
    devamsiz = sum(1 for a in bugun_att if a.get("turu", "").lower() in ("devamsiz", "ozursuz"))
    gec = sum(1 for a in bugun_att if a.get("turu", "").lower() == "gec")

    # Etkinlik
    etkinlikler = adapter.load("akademik/etkinlik_duyurular.json") or []
    bugun_etk = [e for e in etkinlikler if e.get("tarih", "").startswith(today)]

    # Randevu
    randevular = adapter.load("akademik/veli_randevular.json") or []
    bugun_randevu = [r for r in randevular if r.get("tarih") == today]

    # Mood
    mood = adapter.load("mood_checkin/checkins.json") or []
    bugun_mood = [m for m in mood if m.get("tarih") == today]
    mood_ort = round(sum(int(m.get("level", 3)) for m in bugun_mood) / max(len(bugun_mood), 1), 1) if bugun_mood else 0

    # Ihbar
    ihbar = adapter.load("ihbar_hatti/ihbarlar.json") or []
    yeni_ihbar = sum(1 for i in ihbar if i.get("durum") == "Yeni")

    # Risk
    risk = adapter.load("davranissal_risk/risk_records.json") or []
    kritik_risk = sum(1 for r in risk if r.get("behavioral_risk_score", 0) >= 70)

    # Odev
    odevler = adapter.load("akademik/odevler.json") or []
    bugun_odev = sum(1 for o in odevler if o.get("verilis_tarihi", "").startswith(today))

    return {
        "tarih": today,
        "gun": gun_adi,
        "gun_basi": {
            "aktif_ogrenci": aktif_ogrenci,
            "aktif_ogretmen": aktif_ogretmen,
            "bugun_etkinlik": len(bugun_etk),
            "bugun_randevu": len(bugun_randevu),
            "bekleyen_ihbar": yeni_ihbar,
            "kritik_risk": kritik_risk,
            "etkinlikler": [{"baslik": e.get("baslik"), "konum": e.get("konum")} for e in bugun_etk],
            "randevular": [{"saat": r.get("saat"), "veli": r.get("veli_adi"),
                           "ogretmen": r.get("ogretmen_adi"), "konu": r.get("konu")}
                          for r in bugun_randevu],
        },
        "gun_sonu": {
            "devamsiz": devamsiz,
            "gec": gec,
            "yoklama_alinan": len(set(a.get("student_id") for a in bugun_att)),
            "mood_ortalama": mood_ort,
            "mood_katilim": len(bugun_mood),
            "verilen_odev": bugun_odev,
        },
    }


# ══════════════════════════════════════════════════════════════
# KAYIT MODULU OZET
# ══════════════════════════════════════════════════════════════

@router.get("/kayit-ozet")
async def kayit_ozet(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Kayit modulu pipeline ozeti — bugun + toplam."""
    _require_yonetici(user)
    today = date.today().isoformat()

    adaylar = adapter.load("kayit_modulu/kayit_adaylar.json") or []

    # Asama dagilimi
    from collections import Counter
    asama_sayilari = Counter(a.get("asama", "?") for a in adaylar)

    # Bugun aranan
    bugun_aranan = 0
    bugun_gorusme = 0
    bugun_randevu = 0
    bugun_kayit = 0
    toplam_veli = len(set(f"{a.get('veli_adi','')} {a.get('veli_soyadi','')}" for a in adaylar))

    for a in adaylar:
        aramalar = a.get("aramalar") or []
        for ar in aramalar:
            if ar.get("tarih", "").startswith(today):
                bugun_aranan += 1
                break

        gorusmeler = a.get("gorusmeler") or []
        for g in gorusmeler:
            if g.get("tarih", "").startswith(today):
                bugun_gorusme += 1
                break

    # Bugun randevu (kayit amaçlı)
    randevular = adapter.load("akademik/veli_randevular.json") or []
    bugun_randevu = sum(1 for r in randevular if r.get("tarih") == today)

    # Bugun kayit olan (asama=kesin_kayit, son guncelleme bugün)
    bugun_kayit = sum(1 for a in adaylar
                     if a.get("asama") == "kesin_kayit"
                     and any(g.get("tarih", "").startswith(today)
                            for g in (a.get("gorusmeler") or [])))

    return {
        "pipeline": {
            "aday": asama_sayilari.get("aday", 0),
            "arandi": asama_sayilari.get("arandi", 0),
            "randevu": asama_sayilari.get("randevu", 0),
            "gorusme": asama_sayilari.get("gorusme", 0),
            "fiyat_verildi": asama_sayilari.get("fiyat_verildi", 0),
            "sozlesme": asama_sayilari.get("sozlesme", 0),
            "kesin_kayit": asama_sayilari.get("kesin_kayit", 0),
            "olumsuz": asama_sayilari.get("olumsuz", 0),
        },
        "bugun": {
            "aranan": bugun_aranan,
            "gorusme": bugun_gorusme,
            "randevu": bugun_randevu,
            "kayit": bugun_kayit,
        },
        "toplam": {
            "aday_sayisi": len(adaylar),
            "veli_sayisi": toplam_veli,
            "kesin_kayit": asama_sayilari.get("kesin_kayit", 0),
            "olumsuz": asama_sayilari.get("olumsuz", 0),
            "donusum_orani": round(
                asama_sayilari.get("kesin_kayit", 0) / max(len(adaylar), 1) * 100, 1
            ),
        },
        # Detay listeleri
        "aranacak_liste": [
            {"veli": f"{a.get('veli_adi','')} {a.get('veli_soyadi','')}".strip(),
             "ogrenci": a.get("ogrenci_adi", ""),
             "telefon": a.get("veli_telefon", ""),
             "asama": a.get("asama", ""),
             "son_arama": (a.get("aramalar") or [{}])[-1].get("tarih", "")[:10] if a.get("aramalar") else "-"}
            for a in adaylar
            if a.get("asama") in ("aday", "arandi")
            and a.get("asama") != "olumsuz"
        ][:20],
        "geciken_takip": [
            {"veli": f"{a.get('veli_adi','')} {a.get('veli_soyadi','')}".strip(),
             "ogrenci": a.get("ogrenci_adi", ""),
             "asama": a.get("asama", ""),
             "son_islem": (a.get("aramalar") or a.get("gorusmeler") or [{}])[-1].get("tarih", "")[:10]
                          if (a.get("aramalar") or a.get("gorusmeler")) else "-"}
            for a in adaylar
            if a.get("asama") in ("arandi", "randevu", "gorusme", "fiyat_verildi")
            and a.get("asama") != "olumsuz"
            and a.get("asama") != "kesin_kayit"
        ][:15],
        "bugun_randevu_liste": [
            {"saat": r.get("saat", ""),
             "veli": r.get("veli_adi", ""),
             "ogretmen": r.get("ogretmen_adi", ""),
             "konu": r.get("konu", ""),
             "durum": r.get("durum", "")}
            for r in randevular if r.get("tarih") == today
        ],
        "bugun_tamamlanan": [
            {"veli": f"{a.get('veli_adi','')} {a.get('veli_soyadi','')}".strip(),
             "ogrenci": a.get("ogrenci_adi", ""),
             "islem": "arama" if any(ar.get("tarih", "").startswith(today) for ar in (a.get("aramalar") or []))
                      else "gorusme" if any(g.get("tarih", "").startswith(today) for g in (a.get("gorusmeler") or []))
                      else "kayit"}
            for a in adaylar
            if any(ar.get("tarih", "").startswith(today) for ar in (a.get("aramalar") or []))
            or any(g.get("tarih", "").startswith(today) for g in (a.get("gorusmeler") or []))
        ][:20],
    }


# ══════════════════════════════════════════════════════════════
# DERS PROGRAMI
# ══════════════════════════════════════════════════════════════

@router.get("/ders-programi")
async def ders_programi(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    sinif: str | None = None,
    sube: str | None = None,
    gun: str | None = None,
):
    """Ders programi — sinif/gun filtreli."""
    _require_yonetici(user)
    schedule = adapter.load("akademik/schedule.json") or []

    if sinif:
        schedule = [s for s in schedule if str(s.get("sinif", "")) == sinif]
    if sube:
        schedule = [s for s in schedule if s.get("sube", "") == sube]
    if gun:
        schedule = [s for s in schedule if s.get("gun", "").lower() == gun.lower()]

    # Gune gore grupla
    from collections import defaultdict
    gun_gruplari: dict[str, list] = defaultdict(list)
    for s in schedule:
        gun_gruplari[s.get("gun", "?")].append(s)

    # Her gun icinde saate gore sirala
    gunler = []
    for g in ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]:
        dersler = gun_gruplari.get(g, [])
        dersler.sort(key=lambda x: int(x.get("saat", 0) or 0))
        if dersler:
            gunler.append({
                "gun": g,
                "ders_sayisi": len(dersler),
                "dersler": [
                    {"saat": s.get("saat"), "ders": s.get("ders"),
                     "ogretmen": s.get("ogretmen_adi"),
                     "sinif": f"{s.get('sinif','')}/{s.get('sube','')}"}
                    for s in dersler
                ],
            })

    # Mevcut siniflar (filtre)
    tum_siniflar = sorted(set(f"{s.get('sinif','')}/{s.get('sube','')}"
                             for s in adapter.load("akademik/schedule.json") or []))

    return {"gunler": gunler, "siniflar": tum_siniflar, "toplam": len(schedule)}


# ══════════════════════════════════════════════════════════════
# NOBET YONETIMI
# ══════════════════════════════════════════════════════════════

@router.get("/nobet")
async def nobet_yonetimi(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Nobet gorevleri + kayitlari."""
    _require_yonetici(user)
    gorevler = adapter.load("akademik/nobet_gorevler.json") or []
    kayitlar = adapter.load("akademik/nobet_kayitlar.json") or []
    today = date.today().isoformat()
    gun_adi = _GUN_MAP[date.today().weekday()]

    # Bugunku nobetciler
    bugun_nobetciler = [g for g in gorevler if g.get("gun", "").lower() == gun_adi.lower()]

    # Gun bazli grupla
    from collections import defaultdict
    gun_gruplari: dict[str, list] = defaultdict(list)
    for g in gorevler:
        gun_gruplari[g.get("gun", "?")].append(g)

    # Kayit durumu
    kayit_map = {k.get("gorev_id"): k for k in kayitlar}

    haftalik = []
    for gun in ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]:
        nobetciler = gun_gruplari.get(gun, [])
        haftalik.append({
            "gun": gun,
            "nobetciler": [
                {"ogretmen": n.get("ogretmen_adi"), "yer": n.get("yer"),
                 "saat": n.get("saat"),
                 "durum": kayit_map.get(n.get("id"), {}).get("durum", "bekliyor")}
                for n in nobetciler
            ],
        })

    return {
        "bugun": {
            "gun": gun_adi,
            "nobetciler": [
                {"ogretmen": n.get("ogretmen_adi"), "yer": n.get("yer"), "saat": n.get("saat")}
                for n in bugun_nobetciler
            ],
        },
        "haftalik": haftalik,
        "toplam_gorev": len(gorevler),
        "toplam_kayit": len(kayitlar),
    }


# ══════════════════════════════════════════════════════════════
# ZAMAN CIZELGESI
# ══════════════════════════════════════════════════════════════

@router.get("/zaman-cizelgesi")
async def zaman_cizelgesi(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Gunluk zaman cizelgesi — ders/teneffus/ogle arasi."""
    _require_yonetici(user)

    # Standart okul zaman cizelgesi
    cizelge = [
        {"saat": "08:30", "bitis": "09:10", "tur": "ders", "no": 1, "sure": 40},
        {"saat": "09:10", "bitis": "09:20", "tur": "teneffus", "no": 0, "sure": 10},
        {"saat": "09:20", "bitis": "10:00", "tur": "ders", "no": 2, "sure": 40},
        {"saat": "10:00", "bitis": "10:10", "tur": "teneffus", "no": 0, "sure": 10},
        {"saat": "10:10", "bitis": "10:50", "tur": "ders", "no": 3, "sure": 40},
        {"saat": "10:50", "bitis": "11:00", "tur": "teneffus", "no": 0, "sure": 10},
        {"saat": "11:00", "bitis": "11:40", "tur": "ders", "no": 4, "sure": 40},
        {"saat": "11:40", "bitis": "12:20", "tur": "ogle", "no": 0, "sure": 40},
        {"saat": "12:20", "bitis": "13:00", "tur": "ders", "no": 5, "sure": 40},
        {"saat": "13:00", "bitis": "13:10", "tur": "teneffus", "no": 0, "sure": 10},
        {"saat": "13:10", "bitis": "13:50", "tur": "ders", "no": 6, "sure": 40},
        {"saat": "13:50", "bitis": "14:00", "tur": "teneffus", "no": 0, "sure": 10},
        {"saat": "14:00", "bitis": "14:40", "tur": "ders", "no": 7, "sure": 40},
        {"saat": "14:40", "bitis": "14:50", "tur": "teneffus", "no": 0, "sure": 10},
        {"saat": "14:50", "bitis": "15:30", "tur": "ders", "no": 8, "sure": 40},
        {"saat": "15:30", "bitis": "16:00", "tur": "etut", "no": 0, "sure": 30},
    ]

    # Simdi hangi dilim aktif
    from datetime import datetime as dt
    now = dt.now().strftime("%H:%M")
    aktif_dilim = None
    for c in cizelge:
        if c["saat"] <= now < c["bitis"]:
            aktif_dilim = c
            break

    return {
        "cizelge": cizelge,
        "aktif_dilim": aktif_dilim,
        "simdi": now,
    }


# ══════════════════════════════════════════════════════════════
# AKTIF CALISAN LISTESI
# ══════════════════════════════════════════════════════════════

@router.get("/calisanlar")
async def calisanlar(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Aktif calisan (ogretmen) listesi."""
    _require_yonetici(user)
    teachers = adapter.load("akademik/teachers.json") or []

    from collections import Counter
    brans_dag = Counter(t.get("brans", "?") for t in teachers)

    return {
        "toplam": len(teachers),
        "aktif": sum(1 for t in teachers if t.get("durum") != "pasif"),
        "brans_dagilimi": dict(brans_dag.most_common()),
        "liste": [
            {"id": t.get("id"), "ad_soyad": f"{t.get('ad','')} {t.get('soyad','')}".strip(),
             "brans": t.get("brans", ""), "email": t.get("email", ""),
             "telefon": t.get("telefon", ""), "durum": t.get("durum", "aktif")}
            for t in sorted(teachers, key=lambda x: f"{x.get('ad','')} {x.get('soyad','')}")
        ],
    }


# ══════════════════════════════════════════════════════════════
# SINIF LISTELERI
# ══════════════════════════════════════════════════════════════

@router.get("/sinif-listeleri")
async def sinif_listeleri(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    sinif: str | None = None,
    sube: str | None = None,
):
    """Sinif bazli ogrenci listeleri."""
    _require_yonetici(user)
    students = adapter.load("akademik/students.json") or []
    aktif = [s for s in students if s.get("durum") == "aktif"]

    if sinif:
        aktif = [s for s in aktif if str(s.get("sinif", "")) == sinif]
    if sube:
        aktif = [s for s in aktif if s.get("sube", "") == sube]

    # Sinif bazli grupla
    from collections import defaultdict
    sinif_gruplari: dict[str, list] = defaultdict(list)
    for s in aktif:
        key = f"{s.get('sinif','')}/{s.get('sube','')}"
        sinif_gruplari[key].append(s)

    siniflar = []
    for key in sorted(sinif_gruplari.keys()):
        ogr = sinif_gruplari[key]
        ogr.sort(key=lambda x: int(x.get("numara", 0) or 0))
        siniflar.append({
            "sinif_sube": key,
            "ogrenci_sayisi": len(ogr),
            "kiz": sum(1 for o in ogr if o.get("cinsiyet", "").lower() in ("kiz", "k")),
            "erkek": sum(1 for o in ogr if o.get("cinsiyet", "").lower() in ("erkek", "e")),
            "ogrenciler": [
                {"id": o.get("id"), "numara": o.get("numara", ""),
                 "ad_soyad": f"{o.get('ad','')} {o.get('soyad','')}".strip(),
                 "cinsiyet": o.get("cinsiyet", ""), "veli": o.get("veli_adi", "")}
                for o in ogr
            ],
        })

    tum_siniflar = sorted(sinif_gruplari.keys())

    return {
        "toplam_ogrenci": len(aktif),
        "toplam_sinif": len(sinif_gruplari),
        "siniflar": siniflar,
        "sinif_listesi": tum_siniflar,
    }


# ══════════════════════════════════════════════════════════════
# TUKETIM & DEMIRBAS GUNLUK RAPOR
# ══════════════════════════════════════════════════════════════

@router.get("/tuketim-demirbas")
async def tuketim_demirbas_rapor(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Tuketim & demirbas gunluk rapor — stok, min stok uyari, hareketler."""
    _require_yonetici(user)
    today = date.today().isoformat()

    # Tuketim urunleri (tdm klasoru veya tuketim_demirbas)
    urunler = (adapter.load("tdm/tuketim_urunleri.json")
               or adapter.load("tuketim_demirbas/tuketim_urunleri.json") or [])
    kategoriler = (adapter.load("tdm/tuketim_kategorileri.json")
                   or adapter.load("tuketim_demirbas/tuketim_kategorileri.json") or [])
    demirbaslar = (adapter.load("tdm/demirbaslar.json")
                   or adapter.load("tuketim_demirbas/demirbaslar.json") or [])
    hareketler = (adapter.load("tdm/tuketim_hareketleri.json")
                  or adapter.load("tuketim_demirbas/tuketim_hareketleri.json") or [])
    zimmetler = (adapter.load("tdm/zimmet_kayitlari.json")
                 or adapter.load("tuketim_demirbas/zimmet_kayitlari.json") or [])

    # Min stok uyari
    min_stok_uyari = [
        {"urun": u.get("urun_adi"), "stok": u.get("stok", 0),
         "min_stok": u.get("min_stok", 0), "kategori": u.get("kategori", "")}
        for u in urunler
        if (u.get("stok", 0) or 0) <= (u.get("min_stok", 0) or 0)
        and u.get("aktif", True)
    ]

    # Bugun hareketler
    bugun_hareket = [h for h in hareketler if h.get("tarih", "").startswith(today)]

    # Toplam stok degeri
    toplam_deger = sum(
        (u.get("stok", 0) or 0) * (u.get("birim_fiyat", 0) or 0)
        for u in urunler if u.get("aktif", True)
    )

    # Kategori bazli urun sayisi
    from collections import Counter
    kat_sayilari = Counter(u.get("kategori", "?") for u in urunler if u.get("aktif", True))

    return {
        "ozet": {
            "toplam_urun": len([u for u in urunler if u.get("aktif", True)]),
            "toplam_demirbas": len(demirbaslar),
            "aktif_zimmet": len([z for z in zimmetler if z.get("durum", "") == "aktif"]),
            "min_stok_uyari": len(min_stok_uyari),
            "toplam_deger": round(toplam_deger, 2),
            "bugun_hareket": len(bugun_hareket),
        },
        "min_stok_uyari": min_stok_uyari[:15],
        "bugun_hareketler": [
            {"urun": h.get("urun_adi", h.get("urun_id", "")),
             "miktar": h.get("miktar"), "tur": h.get("tur", ""),
             "tarih": h.get("tarih", ""), "yapan": h.get("yapan_kisi", "")}
            for h in bugun_hareket[:20]
        ],
        "kategori_dagilimi": dict(kat_sayilari.most_common()),
        "urun_listesi": [
            {"urun": u.get("urun_adi"), "stok": u.get("stok", 0),
             "min_stok": u.get("min_stok", 0), "birim": u.get("birim", ""),
             "kategori": u.get("kategori", ""),
             "deger": round((u.get("stok", 0) or 0) * (u.get("birim_fiyat", 0) or 0), 2)}
            for u in sorted(urunler, key=lambda x: x.get("stok", 0) or 0)
            if u.get("aktif", True)
        ][:30],
    }


# ══════════════════════════════════════════════════════════════
# KISISEL DIL GELISIMI
# ══════════════════════════════════════════════════════════════

@router.get("/dil-gelisimi")
async def dil_gelisimi(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    dil: str = "ingilizce",
):
    """Kisisel dil gelisimi — ders listesi + kelimeler."""
    import json
    from pathlib import Path
    base = Path(adapter.base)

    dil_map = {
        "ingilizce": "fono/fono_lessons.json",
        "almanca": "fono_almanca_104/fono_almanca_104_lessons.json",
        "fransizca": "fono_fransizca/fono_fransizca_lessons.json",
        "italyanca": "fono_italyanca/fono_italyanca_lessons.json",
        "ispanyolca": "fono_ispanyolca/fono_ispanyolca_lessons.json",
    }

    # Dosyayi bul — birden fazla yol dene
    rel = dil_map.get(dil, dil_map["ingilizce"])
    data = None
    search_paths = [
        base / rel,
        Path(__file__).resolve().parent.parent.parent.parent / "data" / rel,
    ]
    for sp in search_paths:
        if sp.exists():
            try:
                with open(sp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data:
                    break
            except Exception:
                pass
    if not data:
        data = {}

    lessons = data.get("lessons", []) if isinstance(data, dict) else data if isinstance(data, list) else []

    # Ders ozet listesi
    ders_listesi = []
    for i, l in enumerate(lessons):
        voc = l.get("vocabulary", l.get("words", []))
        ders_listesi.append({
            "no": l.get("ders", i + 1),
            "title": l.get("title", f"Ders {i+1}"),
            "type": l.get("type_label", ""),
            "kelime_sayisi": len(voc),
            "gramer_sayisi": len(l.get("grammar_topics", [])),
            "alistirma_sayisi": len(l.get("exercises", [])),
        })

    # Mevcut diller — tum yollari tara
    diller = []
    for dk, dp in dil_map.items():
        for sp in [base / dp, Path(__file__).resolve().parent.parent.parent.parent / "data" / dp]:
            if sp.exists():
                diller.append(dk)
                break

    return {
        "dil": dil,
        "toplam_ders": len(lessons),
        "diller": diller,
        "dersler": ders_listesi,
    }


@router.get("/dil-gelisimi/ders/{ders_no}")
async def dil_ders_detay(
    ders_no: int,
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    dil: str = "ingilizce",
):
    """Tek ders detayi — kelimeler + gramer + alistirmalar."""
    import json
    from pathlib import Path

    dil_map = {
        "ingilizce": "fono/fono_lessons.json",
        "almanca": "fono_almanca_104/fono_almanca_104_lessons.json",
        "fransizca": "fono_fransizca/fono_fransizca_lessons.json",
        "italyanca": "fono_italyanca/fono_italyanca_lessons.json",
        "ispanyolca": "fono_ispanyolca/fono_ispanyolca_lessons.json",
    }

    rel = dil_map.get(dil, dil_map["ingilizce"])
    data = None
    base = Path(adapter.base)
    for sp in [base / rel, Path(__file__).resolve().parent.parent.parent.parent / "data" / rel]:
        if sp.exists():
            try:
                with open(sp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data: break
            except Exception: pass
    if not data: data = {}

    lessons = data.get("lessons", []) if isinstance(data, dict) else []

    # Ders bul (0-indexed veya ders numarasi)
    lesson = None
    for l in lessons:
        if l.get("ders") == ders_no or lessons.index(l) == ders_no - 1:
            lesson = l
            break

    if not lesson:
        raise HTTPException(404, f"Ders {ders_no} bulunamadi")

    return {
        "no": lesson.get("ders", ders_no),
        "title": lesson.get("title", ""),
        "type": lesson.get("type_label", ""),
        "vocabulary": lesson.get("vocabulary", lesson.get("words", [])),
        "grammar_topics": lesson.get("grammar_topics", []),
        "grammar_examples": lesson.get("grammar_examples", []),
        "reading": lesson.get("reading", ""),
        "exercises": lesson.get("exercises", []),
    }


# ══════════════════════════════════════════════════════════════
# DESTEK HIZMETLERI TAKIP
# ══════════════════════════════════════════════════════════════

@router.get("/destek-hizmetleri")
async def destek_hizmetleri(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
):
    """Destek hizmetleri — ticket ozet + bekleyen + SLA."""
    _require_yonetici(user)
    today = date.today().isoformat()

    tickets = (adapter.load("destek_hizmetleri/tickets.json")
               or adapter.load("tdm/tickets.json") or [])
    periyodik = (adapter.load("destek_hizmetleri/periyodik_gorevler.json") or [])
    bakimlar = (adapter.load("destek_hizmetleri/bakim_kayitlari.json") or [])

    from collections import Counter
    durum_dag = Counter(t.get("durum", "?") for t in tickets)
    oncelik_dag = Counter(t.get("oncelik", "?") for t in tickets)

    acik = [t for t in tickets if t.get("durum") not in ("Tamamlandi", "Kapandi", "Kontrol")]
    bugun_acilan = [t for t in tickets if t.get("olusturma_tarihi", "").startswith(today)]

    return {
        "ozet": {
            "toplam_ticket": len(tickets),
            "acik": len(acik),
            "bugun_acilan": len(bugun_acilan),
            "periyodik_gorev": len(periyodik),
            "bakim_kaydi": len(bakimlar),
        },
        "durum_dagilimi": dict(durum_dag.most_common()),
        "oncelik_dagilimi": dict(oncelik_dag.most_common()),
        "acik_ticketlar": [
            {"id": t.get("id"), "ticket_no": t.get("ticket_no", ""),
             "baslik": t.get("baslik", t.get("aciklama", "")[:50]),
             "kategori": t.get("hizmet_alani", t.get("kategori", "")),
             "oncelik": t.get("oncelik", "Normal"),
             "durum": t.get("durum", ""),
             "tarih": (t.get("olusturma_tarihi") or "")[:10],
             "talep_eden": t.get("talep_eden", "")}
            for t in sorted(acik, key=lambda x: {"Kritik": 0, "Yuksek": 1, "Normal": 2, "Dusuk": 3}.get(x.get("oncelik", "Normal"), 2))
        ][:20],
    }


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
