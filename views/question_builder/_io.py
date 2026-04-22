"""
Soru Olusturma - Dosya I/O
==========================
JSON dosya okuma/yazma islemleri.
"""

from __future__ import annotations

import json
import os
from typing import Any

import streamlit as st

from ._paths import (
    get_tenant_dir,
    get_question_bank_path,
    get_tenant_settings_path,
    get_generation_plan_path,
)
from ._constants import TENANT_ROOT


def load_tenant_settings(tenant_name: str) -> dict:
    """Tenant ayarlarini yukle."""
    path = get_tenant_settings_path(tenant_name)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_tenant_settings(tenant_name: str, payload: dict) -> None:
    """Tenant ayarlarini kaydet."""
    path = get_tenant_settings_path(tenant_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def load_generation_plan(tenant_name: str) -> list[dict]:
    """Olusturma planini yukle."""
    path = get_generation_plan_path(tenant_name)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_generation_plan(tenant_name: str, plan: list[dict]) -> None:
    """Olusturma planini kaydet."""
    path = get_generation_plan_path(tenant_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, ensure_ascii=False, indent=2)


def list_tenants() -> list[str]:
    """Mevcut tum tenant'lari listele."""
    tenants = set()
    tenants.add("UZ Koleji")
    if os.path.isdir(TENANT_ROOT):
        for name in os.listdir(TENANT_ROOT):
            path = os.path.join(TENANT_ROOT, name)
            if not os.path.isdir(path):
                continue
            settings_path = os.path.join(path, "settings.json")
            tenant_name = name
            if os.path.exists(settings_path):
                try:
                    with open(settings_path, "r", encoding="utf-8") as handle:
                        data = json.load(handle)
                        tenant_name = data.get("school_name", tenant_name)
                except Exception:
                    pass
            tenants.add(tenant_name)
    return sorted(tenants)


def create_tenant(name: str) -> None:
    """Yeni tenant olustur."""
    if not name:
        return
    payload = {
        "school_name": name,
        "brand_primary": st.session_state.get("brand_primary", "#0F4C81"),
        "brand_secondary": st.session_state.get("brand_secondary", "#F2A900"),
        "booklet_type": st.session_state.get("booklet_type", "A"),
        "include_topic_distribution": st.session_state.get("include_topic_distribution", True),
        "cover_instructions": st.session_state.get("cover_instructions", []),
    }
    save_tenant_settings(name, payload)


def compute_quality_score(question: dict) -> int:
    """Soru kalite puanini hesapla (0-100)."""
    score = 0
    source = question.get("source", "")
    if source == "ai":
        score += 40
    elif source == "graph":
        score += 30
    else:
        score += 15
    if question.get("image_bytes"):
        score += 20
    if len(question.get("options", [])) >= 4:
        score += 10
    if question.get("outcomes"):
        score += 10
    if question.get("question_type") == "Coktan Secmeli (ABCD)":
        score += 5
    return min(score, 100)


def sanitize_question_for_storage(question: dict) -> dict:
    """Soruyu depolama icin temizle (binary verileri kaldir)."""
    cleaned = dict(question)
    for key, value in list(cleaned.items()):
        if isinstance(value, (bytes, bytearray)):
            cleaned.pop(key)
    return cleaned


def load_question_bank(tenant_name: str) -> list[dict]:
    """Soru bankasini yukle."""
    try:
        path = get_question_bank_path(tenant_name)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            if isinstance(data, list):
                for item in data:
                    if "quality_score" not in item:
                        item["quality_score"] = compute_quality_score(item)
                    if "difficulty" not in item:
                        item["difficulty"] = "medium"
                return data
    except Exception:
        return []
    return []


def save_question_bank(tenant_name: str, bank: list[dict]) -> None:
    """Soru bankasini kaydet."""
    path = get_question_bank_path(tenant_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        cleaned = [sanitize_question_for_storage(item) for item in bank]
        json.dump(cleaned, handle, ensure_ascii=False, indent=2)


def add_to_question_bank(items: list[dict]) -> None:
    """Soru bankasina yeni sorular ekle."""
    if not items:
        return
    existing = {q.get("text", "").strip() for q in st.session_state.question_bank}
    for item in items:
        item = sanitize_question_for_storage(item)
        text_key = item.get("text", "").strip()
        if not text_key or text_key in existing:
            continue
        if "quality_score" not in item:
            item["quality_score"] = compute_quality_score(item)
        if "difficulty" not in item:
            item["difficulty"] = "medium"
        st.session_state.question_bank.append(item)
        existing.add(text_key)
    save_question_bank(st.session_state.tenant_name, st.session_state.question_bank)
