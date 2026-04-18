"""Bilgi Yarışmaları Koleksiyonu — 4 tür quiz endpoint'i."""
from __future__ import annotations

import random
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..core.data_adapter import DataAdapter
from ..core.deps import get_current_user, get_data_adapter

router = APIRouter(prefix="/quiz-koleksiyon", tags=["Bilgi Yarışmaları"])


# ══════════════════════════════════════════════════════════════
# YARDIMCI
# ══════════════════════════════════════════════════════════════

def _load_quiz_data(adapter: DataAdapter, filename: str):
    """data/quiz/ altından JSON yükle."""
    return adapter.load(f"quiz/{filename}")


# ══════════════════════════════════════════════════════════════
# TÜRLER LİSTESİ
# ══════════════════════════════════════════════════════════════

@router.get("/turler")
async def quiz_turleri(
    user: Annotated[dict, Depends(get_current_user)],
):
    """4 yarışma türünü listele."""
    return [
        {
            "id": "genel-kultur",
            "baslik": "Genel Kültür",
            "aciklama": "Tarih, Coğrafya, Bilim, Edebiyat, Spor, Türkiye",
            "ikon": "school",
            "renk": "#7C3AED",
            "soru_sayisi": 250,
            "seviyeler": ["karisik", "Tarih", "Coğrafya", "Bilim", "Edebiyat", "Spor", "Türkiye"],
        },
        {
            "id": "kim-milyoner",
            "baslik": "Kim Milyoner",
            "aciklama": "15 soru, 3 joker, artan zorluk",
            "ikon": "emoji_events",
            "renk": "#F59E0B",
            "soru_sayisi": 1997,
            "seviyeler": ["ilkokul", "ortaokul", "lise", "yetiskin"],
        },
        {
            "id": "bilgi-yarismasi",
            "baslik": "Bilgi Yarışması",
            "aciklama": "20 soru, kategori bazlı skor",
            "ikon": "quiz",
            "renk": "#10B981",
            "soru_sayisi": 1500,
            "seviyeler": ["ilkokul", "ortaokul", "lise"],
        },
        {
            "id": "kazanim-pekistirme",
            "baslik": "Kazanım Pekiştirme",
            "aciklama": "Ders/ünite bazlı soru bankası",
            "ikon": "auto_fix_high",
            "renk": "#3B82F6",
            "soru_sayisi": 0,
            "seviyeler": ["ilkokul", "ortaokul", "lise"],
        },
    ]


# ══════════════════════════════════════════════════════════════
# GENEL KÜLTÜR
# ══════════════════════════════════════════════════════════════

@router.get("/genel-kultur")
async def genel_kultur(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    kategori: str = "karisik",
    adet: int = Query(default=10, ge=5, le=30),
):
    """Genel kültür soruları döndür."""
    all_q = _load_quiz_data(adapter, "genel_kultur.json") or []
    if kategori and kategori != "karisik":
        all_q = [q for q in all_q if q.get("k", "") == kategori]
    random.shuffle(all_q)
    return {"sorular": all_q[:adet], "toplam": len(all_q)}


# ══════════════════════════════════════════════════════════════
# KİM MİLYONER
# ══════════════════════════════════════════════════════════════

@router.get("/kim-milyoner")
async def kim_milyoner(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    seviye: str = "ortaokul",
):
    """Kim Milyoner soruları — 15 soru (kolay→zor)."""
    all_data = _load_quiz_data(adapter, "kim_milyoner.json") or {}
    pool = all_data.get(seviye, all_data.get("ortaokul", []))
    random.shuffle(pool)
    # 15 soru seç (5 kolay + 5 orta + 5 zor)
    selected = pool[:15]
    return {"sorular": selected, "toplam": len(pool)}


# ══════════════════════════════════════════════════════════════
# BİLGİ YARIŞMASI
# ══════════════════════════════════════════════════════════════

@router.get("/bilgi-yarismasi")
async def bilgi_yarismasi(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    seviye: str = "ortaokul",
    adet: int = Query(default=20, ge=5, le=30),
):
    """Bilgi yarışması soruları — seviye bazlı."""
    all_data = _load_quiz_data(adapter, "bilgi_yarismasi.json") or {}
    pool = all_data.get(seviye, all_data.get("ortaokul", []))
    random.shuffle(pool)
    return {"sorular": pool[:adet], "toplam": len(pool)}


# ══════════════════════════════════════════════════════════════
# KAZANIM PEKİŞTİRME
# ══════════════════════════════════════════════════════════════

@router.get("/kazanim-pekistirme/dersler")
async def kp_dersler(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    sinif: int = Query(default=9, ge=1, le=12),
):
    """Sınıf bazlı ders listesi."""
    KADEME = {
        range(1, 5): ["Türkçe", "Hayat Bilgisi", "Matematik", "Fen Bilimleri",
                       "Sosyal Bilgiler", "Din Kültürü", "İngilizce"],
        range(5, 9): ["Türkçe", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
                       "Din Kültürü", "İngilizce", "İnkılap Tarihi"],
        range(9, 13): ["Edebiyat", "Matematik", "Fizik", "Kimya", "Biyoloji",
                        "Tarih", "Coğrafya", "Felsefe", "Din Kültürü", "İngilizce"],
    }
    for r, dersler in KADEME.items():
        if sinif in r:
            return {"sinif": sinif, "dersler": dersler}
    return {"sinif": sinif, "dersler": []}


@router.get("/kazanim-pekistirme/sorular")
async def kp_sorular(
    user: Annotated[dict, Depends(get_current_user)],
    adapter: Annotated[DataAdapter, Depends(get_data_adapter)],
    sinif: int = 9,
    ders: str = "Matematik",
    adet: int = Query(default=10, ge=5, le=20),
):
    """Kazanım pekiştirme soruları — soru bankasından çek."""
    all_q = adapter.load("olcme/questions.json") or []
    pool = [
        q for q in all_q
        if q.get("question_type") == "mcq"
        and q.get("status") in ("approved", "in_review")
        and int(q.get("grade", 0) or 0) == sinif
        and ders.lower() in (q.get("subject", "") or "").lower()
    ]
    random.shuffle(pool)
    # Standart formata çevir
    sorular = []
    for q in pool[:adet]:
        choices = q.get("choices", {})
        opts = [choices.get(k, "") for k in ["A", "B", "C", "D"]]
        correct = {"A": 0, "B": 1, "C": 2, "D": 3}.get(q.get("correct_choice", "A"), 0)
        sorular.append({
            "s": q.get("stem", ""),
            "o": opts,
            "d": correct,
            "a": q.get("explanation", ""),
            "k": q.get("subject", ders),
        })
    return {"sorular": sorular, "toplam": len(pool)}
