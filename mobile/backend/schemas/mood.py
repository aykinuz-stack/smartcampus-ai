"""Mood Check-in Pydantic schemalari."""
from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field


class MoodCheckinCreate(BaseModel):
    """Ogrenci mood girisi — gunluk 5 sn."""
    level: int = Field(..., ge=1, le=5, description="1=Cok kotu, 5=Harika")
    tags: list[str] = Field(default_factory=list, max_length=5)
    not_: str = Field(default="", max_length=500, alias="not")

    class Config:
        populate_by_name = True


class MoodCheckinResponse(BaseModel):
    id: str
    student_id: str
    student_name: str
    tarih: str  # YYYY-MM-DD
    level: int
    tags: list[str]
    not_: str
    olusturma: str


class MoodSummaryResponse(BaseModel):
    """Son 30 gun ozet."""
    ortalama_seviye: float
    toplam_checkin: int
    son_7_gun: list[dict]  # [{tarih, level, tags}]
    negatif_gun_sayisi: int
    trend: str  # "yukseliyor" | "stabil" | "dusuyor"
