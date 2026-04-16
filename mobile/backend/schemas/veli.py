"""Veli odakli schemalari."""
from __future__ import annotations

from pydantic import BaseModel, Field


# ── Cocuk Profili ──────────────────────────────────────────────
class CocukOzetResponse(BaseModel):
    student_id: str
    ad_soyad: str
    sinif: str
    sube: str
    numara: str
    # Bu donem ozet
    not_ortalamasi: float
    devamsizlik_sayisi: int
    bekleyen_odev: int
    geciken_odev: int
    bu_ay_mood_ortalamasi: float     # 0 ise veri yok
    son_kapsul_tarih: str | None = None
    # Flag'lar
    risk_var: bool = False
    risk_seviyesi: str = ""          # LOW / MEDIUM / HIGH / CRITICAL


# ── Gunluk Kapsul ──────────────────────────────────────────────
class GunlukKapsulItem(BaseModel):
    id: str
    tarih: str
    student_id: str
    student_name: str
    # 6 bolum
    akademik: dict = {}
    sosyal_duygusal: dict = {}
    etkinlik: dict = {}
    yarin_hazirlik: dict = {}
    ozel_an: dict = {}
    mood: dict = {}
    # AI ozet
    ai_ozet: str = ""
    olusturma: str


class KapsulListResponse(BaseModel):
    kapsuller: list[GunlukKapsulItem]
    bugunku: GunlukKapsulItem | None = None


# ── Randevu ────────────────────────────────────────────────────
class RandevuItem(BaseModel):
    id: str
    student_id: str
    veli_adi: str
    ogretmen_id: str
    ogretmen_adi: str
    tarih: str
    saat: str
    konu: str
    durum: str     # beklemede / onaylandi / iptal / tamamlandi
    notlar: str = ""


class RandevuAlRequest(BaseModel):
    student_id: str | None = None
    ogretmen_id: str
    ogretmen_adi: str = ""
    tarih: str = Field(..., description="YYYY-MM-DD")
    saat: str = Field(..., description="HH:MM")
    konu: str = Field(..., min_length=3, max_length=200)


class RandevuListResponse(BaseModel):
    aktif: list[RandevuItem]       # beklemede + onaylandi
    gecmis: list[RandevuItem]      # tamamlandi + iptal


# ── Belge Talebi ───────────────────────────────────────────────
BELGE_TURLERI = [
    "Ogrenci Belgesi",
    "Devam Durumu Belgesi",
    "Not Durumu Belgesi",
    "Transkript",
    "Disiplin Durum Belgesi",
    "Saglik Durumu Belgesi",
    "Diger",
]


class BelgeTalebiRequest(BaseModel):
    student_id: str | None = None
    belge_turu: str
    aciklama: str = ""


class BelgeTalebiItem(BaseModel):
    id: str
    student_id: str
    veli_adi: str
    belge_turu: str
    aciklama: str
    durum: str          # bekliyor / hazirlaniyor / hazir / teslim_edildi / iptal
    talep_tarihi: str
    teslim_tarihi: str | None = None


class BelgeTalepListResponse(BaseModel):
    talepler: list[BelgeTalebiItem]


# ── Geri Bildirim ──────────────────────────────────────────────
class GeriBildirimRequest(BaseModel):
    kategori: str = Field(..., description="memnuniyet / oneri / sikayet / tesekkur")
    puan: int | None = Field(None, ge=1, le=5)
    mesaj: str = Field(..., min_length=5, max_length=2000)
    student_id: str | None = None
