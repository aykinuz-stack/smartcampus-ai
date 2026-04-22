"""Odeme Takip Modulu — Kolej ucret yonetimi.

Ogrenci bazli taksit plani, odeme kaydi, makbuz, borc takibi.
Veli portali + yonetici dashboard.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Optional


# ══════════════════════════════════════════════════════════════
# VERI MODELLERI
# ══════════════════════════════════════════════════════════════

@dataclass
class UcretKalemi:
    """Tek bir ucret kalemi (ogretim ucreti, yemek, servis, vb.)."""
    id: str = ""
    ad: str = ""                      # "Ogretim Ucreti", "Yemek", "Servis", "Kiyafet"
    kategori: str = ""                # ogretim, yemek, servis, kiyafet, etkinlik, diger
    tutar: float = 0.0
    donem: str = ""                   # "2025-2026"
    aciklama: str = ""
    zorunlu: bool = True

    def __post_init__(self):
        if not self.id:
            self.id = f"uk_{uuid.uuid4().hex[:8]}"


@dataclass
class TaksitPlani:
    """Ogrenci bazli taksit plani."""
    id: str = ""
    student_id: str = ""
    student_adi: str = ""
    sinif: str = ""
    sube: str = ""
    donem: str = ""                   # "2025-2026"
    toplam_tutar: float = 0.0
    indirim_orani: float = 0.0        # % olarak (kardes indirimi, basari bursu vb.)
    indirim_tutari: float = 0.0
    net_tutar: float = 0.0
    taksit_sayisi: int = 10
    taksitler: list = field(default_factory=list)  # Taksit listesi
    durum: str = "aktif"              # aktif, tamamlandi, iptal
    olusturma_tarihi: str = ""
    notlar: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"tp_{uuid.uuid4().hex[:8]}"
        if not self.olusturma_tarihi:
            self.olusturma_tarihi = datetime.now().isoformat()
        if self.indirim_orani > 0 and self.indirim_tutari == 0:
            self.indirim_tutari = self.toplam_tutar * self.indirim_orani / 100
        if self.net_tutar == 0:
            self.net_tutar = self.toplam_tutar - self.indirim_tutari


@dataclass
class Taksit:
    """Tek bir taksit."""
    id: str = ""
    plan_id: str = ""
    sira: int = 0                     # 1, 2, 3...
    tutar: float = 0.0
    vade_tarihi: str = ""             # "2025-09-15"
    odeme_tarihi: Optional[str] = None
    odeme_tutari: float = 0.0
    durum: str = "bekliyor"           # bekliyor, odendi, gecikti, iptal
    odeme_yontemi: str = ""           # nakit, havale, kredi_karti, eft
    makbuz_no: str = ""
    aciklama: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"tks_{uuid.uuid4().hex[:8]}"


@dataclass
class OdemeKaydi:
    """Yapilan bir odeme (tek sefer veya taksit odemesi)."""
    id: str = ""
    student_id: str = ""
    plan_id: str = ""
    taksit_id: str = ""
    tutar: float = 0.0
    odeme_tarihi: str = ""
    odeme_yontemi: str = ""           # nakit, havale, kredi_karti, eft, pos
    makbuz_no: str = ""
    islem_yapan: str = ""             # admin/muhasebe kullanici adi
    aciklama: str = ""
    iptal: bool = False

    def __post_init__(self):
        if not self.id:
            self.id = f"ok_{uuid.uuid4().hex[:8]}"
        if not self.odeme_tarihi:
            self.odeme_tarihi = datetime.now().isoformat()


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

class OdemeDataStore:
    """JSON tabanli odeme veri yonetimi."""

    def __init__(self, data_dir: str = "data/odeme"):
        self.base = Path(data_dir)
        self.base.mkdir(parents=True, exist_ok=True)
        self._paths = {
            "ucret_kalemleri": self.base / "ucret_kalemleri.json",
            "taksit_planlari": self.base / "taksit_planlari.json",
            "odeme_kayitlari": self.base / "odeme_kayitlari.json",
        }

    def _load(self, key: str) -> list:
        p = self._paths[key]
        if not p.exists():
            return []
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, key: str, data: list):
        p = self._paths[key]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # --- Ucret Kalemleri ---
    def get_ucret_kalemleri(self, donem: str = "") -> list[dict]:
        data = self._load("ucret_kalemleri")
        if donem:
            data = [d for d in data if d.get("donem") == donem]
        return data

    def save_ucret_kalemi(self, kalemi: UcretKalemi) -> str:
        data = self._load("ucret_kalemleri")
        existing = next((i for i, d in enumerate(data) if d.get("id") == kalemi.id), None)
        if existing is not None:
            data[existing] = asdict(kalemi)
        else:
            data.append(asdict(kalemi))
        self._save("ucret_kalemleri", data)
        return kalemi.id

    # --- Taksit Planlari ---
    def get_taksit_planlari(self, student_id: str = "", donem: str = "") -> list[dict]:
        data = self._load("taksit_planlari")
        if student_id:
            data = [d for d in data if d.get("student_id") == student_id]
        if donem:
            data = [d for d in data if d.get("donem") == donem]
        return data

    def save_taksit_plani(self, plan: TaksitPlani) -> str:
        data = self._load("taksit_planlari")
        existing = next((i for i, d in enumerate(data) if d.get("id") == plan.id), None)
        if existing is not None:
            data[existing] = asdict(plan)
        else:
            data.append(asdict(plan))
        self._save("taksit_planlari", data)
        return plan.id

    def taksit_plani_olustur(self, student_id: str, student_adi: str,
                              sinif: str, sube: str, donem: str,
                              toplam: float, taksit_sayisi: int = 10,
                              indirim_orani: float = 0.0,
                              baslangic_ay: int = 9) -> TaksitPlani:
        """Otomatik taksit plani + taksitler olustur."""
        plan = TaksitPlani(
            student_id=student_id,
            student_adi=student_adi,
            sinif=sinif, sube=sube,
            donem=donem,
            toplam_tutar=toplam,
            indirim_orani=indirim_orani,
            taksit_sayisi=taksit_sayisi,
        )
        # Taksitleri olustur
        aylık = round(plan.net_tutar / taksit_sayisi, 2)
        yil = int(donem.split("-")[0]) if "-" in donem else date.today().year
        taksitler = []
        for i in range(taksit_sayisi):
            ay = (baslangic_ay + i - 1) % 12 + 1
            t_yil = yil if ay >= baslangic_ay else yil + 1
            taksit = Taksit(
                plan_id=plan.id,
                sira=i + 1,
                tutar=aylık,
                vade_tarihi=f"{t_yil}-{ay:02d}-15",
            )
            taksitler.append(asdict(taksit))
        plan.taksitler = taksitler
        self.save_taksit_plani(plan)
        return plan

    # --- Odeme Kayitlari ---
    def get_odeme_kayitlari(self, student_id: str = "", plan_id: str = "") -> list[dict]:
        data = self._load("odeme_kayitlari")
        if student_id:
            data = [d for d in data if d.get("student_id") == student_id]
        if plan_id:
            data = [d for d in data if d.get("plan_id") == plan_id]
        return data

    def odeme_yap(self, plan_id: str, taksit_id: str, tutar: float,
                  yontem: str = "nakit", islem_yapan: str = "") -> OdemeKaydi:
        """Taksit odemesi yap — taksit durumunu guncelle."""
        planlar = self._load("taksit_planlari")
        plan = next((p for p in planlar if p.get("id") == plan_id), None)
        if not plan:
            raise ValueError(f"Plan bulunamadi: {plan_id}")

        # Taksiti bul ve guncelle
        taksit = next((t for t in plan.get("taksitler", []) if t.get("id") == taksit_id), None)
        if not taksit:
            raise ValueError(f"Taksit bulunamadi: {taksit_id}")

        taksit["durum"] = "odendi"
        taksit["odeme_tarihi"] = date.today().isoformat()
        taksit["odeme_tutari"] = tutar
        taksit["odeme_yontemi"] = yontem
        taksit["makbuz_no"] = f"MKB-{uuid.uuid4().hex[:6].upper()}"

        # Plan durumunu kontrol et
        tum_odendi = all(t.get("durum") == "odendi" for t in plan.get("taksitler", []))
        if tum_odendi:
            plan["durum"] = "tamamlandi"

        self._save("taksit_planlari", planlar)

        # Odeme kaydi olustur
        kayit = OdemeKaydi(
            student_id=plan.get("student_id", ""),
            plan_id=plan_id,
            taksit_id=taksit_id,
            tutar=tutar,
            odeme_yontemi=yontem,
            makbuz_no=taksit["makbuz_no"],
            islem_yapan=islem_yapan,
        )
        data = self._load("odeme_kayitlari")
        data.append(asdict(kayit))
        self._save("odeme_kayitlari", data)
        return kayit

    # --- Ozet / Rapor ---
    def get_odeme_ozet(self, donem: str = "") -> dict:
        """Genel odeme ozeti — yonetici dashboard icin."""
        planlar = self.get_taksit_planlari(donem=donem)
        toplam_borc = sum(p.get("net_tutar", 0) for p in planlar)
        toplam_odenen = 0
        toplam_geciken = 0
        today = date.today().isoformat()

        for p in planlar:
            for t in p.get("taksitler", []):
                if t.get("durum") == "odendi":
                    toplam_odenen += t.get("odeme_tutari", 0)
                elif t.get("vade_tarihi", "") < today and t.get("durum") == "bekliyor":
                    toplam_geciken += t.get("tutar", 0)
                    t["durum"] = "gecikti"

        return {
            "toplam_ogrenci": len(planlar),
            "toplam_borc": round(toplam_borc, 2),
            "toplam_odenen": round(toplam_odenen, 2),
            "kalan_borc": round(toplam_borc - toplam_odenen, 2),
            "geciken_tutar": round(toplam_geciken, 2),
            "tahsilat_orani": round(toplam_odenen / max(toplam_borc, 1) * 100, 1),
        }
