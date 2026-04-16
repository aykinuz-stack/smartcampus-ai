"""Ogretmen schemalari — yoklama, not girisi, ders defteri."""
from __future__ import annotations

from pydantic import BaseModel, Field


# ── Sinif Listesi ──────────────────────────────────────────────
class SinifOgrenci(BaseModel):
    id: str
    ad_soyad: str
    numara: str
    sinif: str
    sube: str


class SinifListResponse(BaseModel):
    sinif: str
    sube: str
    ogrenciler: list[SinifOgrenci]


# ── Yoklama ────────────────────────────────────────────────────
class YoklamaGiris(BaseModel):
    student_id: str
    turu: str           # devam / devamsiz / gec / izinli / raporlu
    aciklama: str = ""


class YoklamaBatchRequest(BaseModel):
    sinif: str
    sube: str
    ders: str
    ders_saati: int
    tarih: str = Field(..., description="YYYY-MM-DD")
    yoklamalar: list[YoklamaGiris]


class YoklamaBatchResponse(BaseModel):
    eklenen: int
    guncellenen: int
    tarih: str


# ── Not Girisi ─────────────────────────────────────────────────
class NotGirisi(BaseModel):
    student_id: str
    puan: float = Field(..., ge=0, le=100)
    aciklama: str = ""


class NotBatchRequest(BaseModel):
    sinif: str
    sube: str
    ders: str
    donem: str           # "1. Donem" / "2. Donem"
    not_turu: str        # yazili / sozlu / proje / performans
    not_sirasi: int
    tarih: str
    notlar: list[NotGirisi]


class NotBatchResponse(BaseModel):
    eklenen: int
    tarih: str


# ── Ders Defteri ───────────────────────────────────────────────
class DersDefteriRequest(BaseModel):
    sinif: str
    sube: str
    ders: str
    ders_saati: int
    tarih: str
    islenen_konu: str = Field(..., min_length=3, max_length=500)
    ozel_not: str = ""
    online_link: str = ""
    kazanimlar: list[str] = []


class DersDefteriItem(BaseModel):
    id: str
    sinif: str
    sube: str
    ders: str
    ders_saati: int
    tarih: str
    islenen_konu: str
    ozel_not: str = ""
    online_link: str = ""
    ogretmen_id: str
    ogretmen_adi: str


# ── Odev Atama ─────────────────────────────────────────────────
class OdevAtaRequest(BaseModel):
    baslik: str = Field(..., min_length=3)
    ders: str
    sinif: str
    sube: str
    tur: str             # link / dosya / video / yazili
    aciklama: str = ""
    verilis_tarihi: str
    teslim_tarihi: str
    kaynak_url: str = ""
