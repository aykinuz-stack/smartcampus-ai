"""Rehber schemalari — vaka, gorusme, aile formu, ihbar inceleme."""
from __future__ import annotations

from pydantic import BaseModel, Field


# ── Vaka ───────────────────────────────────────────────────────
VAKA_KONULARI = [
    "Sosyal uyum",
    "Akran zorbaligi",
    "Dikkat eksikligi",
    "Sinav kaygisi",
    "Motivasyon dusuklugu",
    "Okula devamsizlik",
    "Ders basarisizligi",
    "Aile sorunlari",
]


class VakaItem(BaseModel):
    id: str
    student_id: str
    ogrenci_adi: str
    sinif: int | str
    sube: str
    konu: str
    aciklama: str
    oncelik: str   # dusuk / orta / yuksek / kritik
    durum: str     # acik / devam / cozuldu
    acilis_tarihi: str
    kapatis_tarihi: str | None = None


class VakaCreateRequest(BaseModel):
    student_id: str
    konu: str = Field(..., description=f"Listeden: {VAKA_KONULARI}")
    aciklama: str = Field(..., min_length=10)
    oncelik: str = "orta"


# ── Gorusme ────────────────────────────────────────────────────
class GorusmeItem(BaseModel):
    id: str
    vaka_id: str | None = None
    student_id: str
    tarih: str
    sure_dakika: int
    gorusen: str
    notlar: str
    sonraki_adim: str


class GorusmeCreateRequest(BaseModel):
    student_id: str
    vaka_id: str | None = None
    sure_dakika: int = 30
    notlar: str = Field(..., min_length=10)
    sonraki_adim: str = ""


# ── Aile Formu ─────────────────────────────────────────────────
class AileFormItem(BaseModel):
    id: str
    student_id: str
    ogrenci_adi: str
    anne_egitim: str = ""
    baba_egitim: str = ""
    anne_meslek: str = ""
    baba_meslek: str = ""
    kardes_sayisi: int = 0
    aile_durumu: str = "birlikte"  # birlikte / ayri / vefat
    ev_durumu: str = ""
    ozel_durum: str = ""
    tarih: str


class AileFormCreateRequest(BaseModel):
    student_id: str
    anne_egitim: str = ""
    baba_egitim: str = ""
    anne_meslek: str = ""
    baba_meslek: str = ""
    kardes_sayisi: int = 0
    aile_durumu: str = "birlikte"
    ev_durumu: str = ""
    ozel_durum: str = ""
