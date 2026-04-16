"""Anonim ihbar hatti schemalari."""
from __future__ import annotations

from pydantic import BaseModel, Field


IHBAR_KATEGORILERI = [
    "akran_zorbaligi",
    "intihar_riski",
    "madde_kullanim",
    "cinsel_taciz",
    "aile_ici_siddet",
    "akademik_kopya",
    "personel_sikayet",
    "diger",
]


class IhbarCreateRequest(BaseModel):
    """Tamamen anonim — kimlik bilgisi YOK."""
    kategori: str = Field(..., description="8 kategoriden biri")
    alt_kategori: str = Field(default="")
    aciklama: str = Field(..., min_length=20, max_length=2000)
    nerede: str = Field(default="")
    ne_zaman: str = Field(default="")
    kim_icin: str = Field(default="Kendim hakkinda")
    geri_donus_istiyor: bool = False


class IhbarCreateResponse(BaseModel):
    """Ihbar alindi onayi — ogrenci takip kodu alir (opsiyonel)."""
    anonim_id: str
    takip_kodu: str = ""
    mesaj: str = "Ihbariniz güvenli bir sekilde iletildi. Rehber ekibi değerlendirecek."


class IhbarStatusRequest(BaseModel):
    takip_kodu: str = Field(..., min_length=4)


class IhbarStatusResponse(BaseModel):
    anonim_id: str
    kategori: str
    durum: str
    rehber_notu: str = ""
    olusturma_tarihi: str
