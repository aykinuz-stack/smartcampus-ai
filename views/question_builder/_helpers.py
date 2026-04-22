"""
Soru Olusturma - Yardimci Fonksiyonlar
======================================
Ders etiketleri ve diger yardimci fonksiyonlar.
"""

from __future__ import annotations

import re
import streamlit as st


def normalize_subject_label(value: str) -> str:
    """Turkce karakterleri ASCII'ye donustur ve kucuk harfe cevir."""
    table = str.maketrans({
        "\u2021": "c",
        "\u20ac": "c",
        "\u00a7": "g",
        "\u00a6": "g",
        "\u008d": "i",
        "\u02dc": "i",
        "\u201d": "o",
        "\u2122": "o",
        "\u0178": "s",
        "\u017e": "s",
        "\u0081": "u",
        "\u0161": "u",
        "\u00e7": "c",
        "\u00c7": "c",
        "\u011f": "g",
        "\u011e": "g",
        "\u0131": "i",
        "\u0130": "i",
        "\u00f6": "o",
        "\u00d6": "o",
        "\u015f": "s",
        "\u015e": "s",
        "\u00fc": "u",
        "\u00dc": "u",
    })
    return str(value).translate(table).lower().strip()


# Ders etiketi donusum haritasi
SUBJECT_LABEL_MAP = {
    "tde": "Turk Dili ve Edebiyati",
    "turkdilivedebiyati": "Turk Dili ve Edebiyati",
    "turkdili": "Turk Dili ve Edebiyati",
    "edebiyat": "Turk Dili ve Edebiyati",
    "mat": "Matematik",
    "matematik": "Matematik",
    "fiz": "Fizik",
    "fizik": "Fizik",
    "kim": "Kimya",
    "kimya": "Kimya",
    "bio": "Biyoloji",
    "biyoloji": "Biyoloji",
    "cog": "Cografya",
    "cografya": "Cografya",
    "tar": "Tarih",
    "tarih": "Tarih",
    "ing": "Ingilizce",
    "ingilizce": "Ingilizce",
    "alm": "Almanca",
    "almanca": "Almanca",
    "fr": "Fransizca",
    "fransizca": "Fransizca",
    "fel": "Felsefe",
    "felsefe": "Felsefe",
    "dkab": "Din Kulturu ve Ahlak Bilgisi",
    "din": "Din Kulturu ve Ahlak Bilgisi",
}


def display_subject_label(value: str) -> str:
    """Ders etiketini gosterim formatina cevir."""
    norm = normalize_subject_label(value)
    key = re.sub(r"[^a-z0-9]+", "", norm)
    return SUBJECT_LABEL_MAP.get(key, value)


def normalize_subject_key(value: str) -> str:
    """Ders etiketini karsilastirma icin normalize et."""
    norm = normalize_subject_label(value)
    key = re.sub(r"[^a-z0-9]+", "", norm)
    key = re.sub(r"\d+$", "", key)
    mapped = SUBJECT_LABEL_MAP.get(key, value)
    norm2 = normalize_subject_label(mapped)
    key2 = re.sub(r"[^a-z0-9]+", "", norm2)
    return re.sub(r"\d+$", "", key2)


def subject_matches(left: str, right: str) -> bool:
    """Iki ders etiketinin eslesip eslesmedigini kontrol et."""
    return normalize_subject_key(left) == normalize_subject_key(right)


def subject_matches_question(question: dict, subject: str) -> bool:
    """Sorunun belirtilen dersle eslestip eslesmedigini kontrol et."""
    if subject_matches(question.get("subject", ""), subject):
        return True
    tags = question.get("subject_tags") or []
    return any(subject_matches(tag, subject) for tag in tags)


def is_excluded_subject(value: str) -> bool:
    """Dersin sinav olusturmadan haric tutulup tutulmayacagini kontrol et."""
    norm = normalize_subject_label(value)
    return (
        "beden" in norm
        or "spor" in norm
        or "muzik" in norm
        or "gorsel" in norm
        or "sanat" in norm
        or "psikoloji" in norm
        or "sosyoloji" in norm
        or "din" in norm
        or "dkab" in norm
        or "ingiliz" in norm
        or "ing" in norm
    )


def subject_key(value: str) -> str:
    """Ders etiketini dosya sistemi icin guvenli anahtara cevir."""
    sanitized = normalize_subject_label(value)
    sanitized = re.sub(r"[^a-z0-9]+", "_", sanitized)
    return sanitized.strip("_") or "ders"


def tenant_key(value: str) -> str:
    """Tenant ismini dosya sistemi icin guvenli anahtara cevir."""
    sanitized = normalize_subject_label(value)
    sanitized = re.sub(r"[^a-z0-9]+", "_", sanitized)
    return sanitized.strip("_") or "tenant"


def graph_render_settings() -> tuple[float, float, int]:
    """Grafik render ayarlarini dondur (genislik, yukseklik, DPI)."""
    fast = st.session_state.get("fast_graph_mode", True)
    if fast:
        return (3.2, 2.2, 80)
    return (4.0, 2.6, 120)


def hex_to_rgb(color: str) -> tuple[float, float, float]:
    """Hex renk kodunu RGB tuple'a cevir (0-1 araliginda)."""
    value = (color or "").lstrip("#")
    if len(value) != 6:
        return (0, 0, 0)
    r = int(value[0:2], 16) / 255.0
    g = int(value[2:4], 16) / 255.0
    b = int(value[4:6], 16) / 255.0
    return (r, g, b)
