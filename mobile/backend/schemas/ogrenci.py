"""Ogrenci odakli Pydantic schemalari — not, devamsizlik, odev."""
from __future__ import annotations

from pydantic import BaseModel


# ── Notlar ─────────────────────────────────────────────────────
class GradeItem(BaseModel):
    id: str
    ders: str
    donem: str
    not_turu: str   # yazili / sozlu / proje / performans
    not_sirasi: int
    puan: float
    tarih: str
    aciklama: str = ""


class GradeSummary(BaseModel):
    ders: str
    ortalama: float
    not_sayisi: int
    en_yuksek: float
    en_dusuk: float


class GradesResponse(BaseModel):
    notlar: list[GradeItem]
    donem_ortalamasi: float
    genel_ortalama: float
    ders_ozetleri: list[GradeSummary]


# ── Devamsizlik ────────────────────────────────────────────────
class AttendanceItem(BaseModel):
    id: str
    tarih: str
    ders: str
    ders_saati: int
    turu: str          # devamsiz / gec / izinli / raporlu
    aciklama: str = ""


class AttendanceResponse(BaseModel):
    kayitlar: list[AttendanceItem]
    toplam_ders_saati: int     # ozursuz devam etmedigi ders saati
    ozursuz: int
    ozurlu: int
    gec: int
    oran: float               # ozursuz / toplam
    son_30_gun: int


# ── Odev ───────────────────────────────────────────────────────
class OdevItem(BaseModel):
    id: str
    baslik: str
    ders: str
    ogretmen_adi: str
    tur: str              # link / dosya / video / yazili
    aciklama: str
    verilis_tarihi: str
    teslim_tarihi: str
    durum: str            # aktif / pasif
    # Teslim durumu
    teslim_edildi: bool = False
    teslim_tarih: str | None = None
    puan: float | None = None
    gec_teslim: bool = False


class OdevListResponse(BaseModel):
    bekleyen: list[OdevItem]     # teslim edilmemis + suresi gecmemis
    geciken: list[OdevItem]      # teslim edilmemis + suresi gecmis
    teslim_edilen: list[OdevItem]
    toplam: int


class OdevTeslimRequest(BaseModel):
    odev_id: str
    dosya_url: str | None = None
    not_: str = ""
