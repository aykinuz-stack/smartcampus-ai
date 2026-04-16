"""Mesajlasma schemalari — ogretmen <> veli."""
from __future__ import annotations

from pydantic import BaseModel, Field


class MesajItem(BaseModel):
    id: str
    student_id: str
    veli_adi: str
    ogretmen_id: str
    ogretmen_adi: str
    tarih: str
    mesaj: str
    yon: str     # "ogretmen_to_veli" / "veli_to_ogretmen" / "ogretmen_to_ogrenci"
    okundu: bool = False


class MesajGonderRequest(BaseModel):
    alici_rol: str = Field(..., description="ogretmen / veli / ogrenci")
    alici_id: str = Field(..., description="Alicinin ID'si")
    mesaj: str = Field(..., min_length=1, max_length=2000)
    student_id: str | None = None   # Konu olan ogrenci (varsa)


class MesajListResponse(BaseModel):
    mesajlar: list[MesajItem]
    toplam: int
    okunmamis: int
