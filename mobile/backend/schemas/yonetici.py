"""Yonetici schemalari."""
from __future__ import annotations

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    toplam_ogrenci: int
    toplam_ogretmen: int
    bugun_yoklama_alinan_sinif: int
    bugun_devamsiz: int
    acik_vaka: int
    bekleyen_ihbar: int
    kritik_risk_ogrenci: int
    bekleyen_onay: int


class RiskOzetResponse(BaseModel):
    kategori: str  # akademik / davranissal / zorbalik / intihar / madde vs
    izlenen: int
    yuksek: int
    kritik: int
    toplam: int


class OnayIstegiItem(BaseModel):
    id: str
    tur: str           # randevu / belge / izin / odev_teslim_gec
    baslik: str
    aciklama: str
    talep_eden: str
    tarih: str
    durum: str         # bekliyor / onaylandi / reddedildi


class OnayAksiyonRequest(BaseModel):
    onay_id: str
    aksiyon: str       # onayla / reddet
    not_metni: str = ""
