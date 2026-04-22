"""
Erken Uyari — Shared Helpers
=============================
Tum _eu_*.py dosyalarinin paylastigi ortak fonksiyonlar.
Tekrar eden kodlari tek noktada toplar.
"""
from __future__ import annotations

import json
import os

import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students


# ── Veri Dizini ──
def eu_data_dir() -> str:
    """Tenant-aware erken uyari veri dizini."""
    d = os.path.join(get_tenant_dir(), "erken_uyari")
    os.makedirs(d, exist_ok=True)
    return d


# ── JSON I/O ──
def eu_load_json(filename: str) -> list:
    """Erken uyari dizininden JSON dosyasi yukler."""
    p = os.path.join(eu_data_dir(), filename)
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def eu_save_json(filename: str, data: list) -> None:
    """Erken uyari dizinine JSON dosyasi yazar."""
    with open(os.path.join(eu_data_dir(), filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Ogrenci Secici ──
def eu_ogrenci_sec(key: str):
    """Paylasilmis ogrenci listesinden secim widget'i. None veya dict doner."""
    students = load_shared_students()
    if not students:
        st.warning("Ogrenci verisi yok.")
        return None
    opts = ["-- Secin --"] + [
        f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}"
        for s in students
    ]
    idx = st.selectbox(
        "Ogrenci", range(len(opts)),
        format_func=lambda i: opts[i], key=key,
    )
    return students[idx - 1] if idx > 0 else None


# ── Risk Bileşen Etiketleri (tek kaynak) ──
COMP_LABELS: dict[str, str] = {
    "grade_risk": "Not Ort.",
    "attendance_risk": "Devamsızlık",
    "exam_risk": "Sınav",
    "homework_risk": "Ödev",
    "outcome_debt_risk": "Kazanım Borcu",
    "counseling_risk": "Rehberlik",
    "health_risk": "Sağlık",
    "trend_risk": "Trend",
    "behavior_risk": "Davranış",
    "foreign_lang_risk": "Yabancı Dil",
}

# ── Renk Yardımcıları ──
def risk_color(val: float) -> str:
    """Risk skoru (0-100, yuksek=kotu) icin renk."""
    if val < 30:
        return "#22c55e"
    if val < 55:
        return "#f59e0b"
    if val < 75:
        return "#f97316"
    return "#ef4444"


def grade_color(val: float) -> str:
    """Not/basari skoru (0-100, yuksek=iyi) icin renk."""
    if val >= 70:
        return "#22c55e"
    if val >= 50:
        return "#f59e0b"
    return "#ef4444"


# ── Öncelik Renkleri (tutarlı Türkçe karakter) ──
PRIORITY_COLORS: dict[str, str] = {
    "ACİL": "#ef4444",
    "ACIL": "#ef4444",   # Türkçe-olmayan variant (geriye uyumluluk)
    "YÜKSEK": "#f97316",
    "YUKSEK": "#f97316",
    "ORTA": "#f59e0b",
    "DÜŞÜK": "#3b82f6",
    "DUSUK": "#3b82f6",
}
