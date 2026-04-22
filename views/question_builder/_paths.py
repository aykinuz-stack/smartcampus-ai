"""
Soru Olusturma - Dosya Yollari
==============================
Tenant ve soru bankasi dosya yollarini yoneten fonksiyonlar.
"""

from __future__ import annotations

import os

from ._constants import TENANT_ROOT
from ._helpers import tenant_key


def get_tenant_dir(name: str) -> str:
    """Tenant dizin yolunu dondur."""
    return os.path.join(TENANT_ROOT, tenant_key(name))


def get_question_bank_path(tenant_name: str) -> str:
    """Soru bankasi JSON dosyasinin yolunu dondur."""
    return os.path.join(get_tenant_dir(tenant_name), "question_bank.json")


def get_tenant_settings_path(tenant_name: str) -> str:
    """Tenant ayarlar dosyasinin yolunu dondur."""
    return os.path.join(get_tenant_dir(tenant_name), "settings.json")


def get_generation_plan_path(tenant_name: str) -> str:
    """Olusturma plani dosyasinin yolunu dondur."""
    return os.path.join(get_tenant_dir(tenant_name), "generation_plan.json")


def get_tenant_outcomes_dir(tenant_name: str) -> str:
    """Tenant kazanimlar dizininin yolunu dondur."""
    return os.path.join(get_tenant_dir(tenant_name), "kazanimlar")


def list_original_pdfs(tenant_name: str) -> list[str]:
    """Yuklenen orijinal PDF dosyalarini listele."""
    originals_dir = os.path.join(get_tenant_dir(tenant_name), "uploads", "originals")
    if not os.path.isdir(originals_dir):
        return []
    return sorted(
        file
        for file in os.listdir(originals_dir)
        if file.lower().endswith(".pdf")
    )
