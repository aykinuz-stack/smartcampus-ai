"""JSON Dosya Adapter — Streamlit ile aynı veriyi paylasir.

Tum modullerin JSON dosyalarini okuma/yazma icin TEK merkezi katman.
Tenant-aware: kullanicinin tenant_id'sine gore dogru dizine yazar.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import settings


class DataAdapter:
    """JSON dosya yazma/okuma — thread-safe degil (kisa ascenye)."""

    def __init__(self, tenant_id: str = "default"):
        self.tenant_id = tenant_id
        self.base = self._resolve_base(tenant_id)

    @staticmethod
    def _resolve_base(tenant_id: str) -> Path:
        """Tenant-aware veri dizini."""
        # Multi-tenant oldugunda: data/tenants/<tid>/
        tenant_dir = settings.DATA_DIR / "tenants" / tenant_id
        if tenant_dir.exists():
            return tenant_dir
        return settings.DATA_DIR

    def load(self, relative_path: str) -> list | dict:
        """Veri dosyasini oku. Yoksa bos liste/dict dondur."""
        p = self.base / relative_path
        if not p.exists():
            return []
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save(self, relative_path: str, data: list | dict) -> bool:
        """Veri dosyasini yaz."""
        p = self.base / relative_path
        p.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as _:
            return False

    def append(self, relative_path: str, item: dict) -> bool:
        """Listeye eleman ekle + kaydet."""
        data = self.load(relative_path)
        if not isinstance(data, list):
            data = []
        data.append(item)
        return self.save(relative_path, data)

    def update_by_id(self, relative_path: str, item_id: str, patch: dict) -> bool:
        """ID ile eleman guncelle."""
        data = self.load(relative_path)
        if not isinstance(data, list):
            return False
        for i, it in enumerate(data):
            if it.get("id") == item_id:
                data[i].update(patch)
                return self.save(relative_path, data)
        return False

    def delete_by_id(self, relative_path: str, item_id: str) -> bool:
        """ID ile eleman sil."""
        data = self.load(relative_path)
        if not isinstance(data, list):
            return False
        new_data = [it for it in data if it.get("id") != item_id]
        if len(new_data) == len(data):
            return False
        return self.save(relative_path, new_data)

    def find_by(self, relative_path: str, **filters) -> list[dict]:
        """Filtreli arama — {key: value} eslesme."""
        data = self.load(relative_path)
        if not isinstance(data, list):
            return []
        out = []
        for it in data:
            match = all(it.get(k) == v for k, v in filters.items())
            if match:
                out.append(it)
        return out


# ──────────────────────────────────────────────────────────────────────
# Kisayol dosya yollari — her modul icin
# ──────────────────────────────────────────────────────────────────────

class DataPaths:
    """Kullanilan tum dosya yollari — tek merkezde."""

    # Akademik
    STUDENTS = "akademik/students.json"
    TEACHERS = "akademik/teachers.json"
    ATTENDANCE = "akademik/attendance.json"
    GRADES = "akademik/grades.json"
    HOMEWORK = "akademik/odevler.json"
    HOMEWORK_SUBMISSIONS = "akademik/odev_teslim.json"
    INTERVENTIONS = "akademik/mudahale_kayitlari.json"
    DISCIPLINE = "akademik/disiplin_olaylari.json"

    # Mood
    MOOD_CHECKINS = "mood_checkin/checkins.json"

    # Ihbar
    IHBAR = "ihbar_hatti/ihbarlar.json"

    # Rehberlik
    VAKA = "rehberlik/vaka_kayitlari.json"
    GORUSME = "rehberlik/gorusme_kayitlari.json"
    AILE_FORM = "rehberlik/aile_bilgi_formlari.json"

    # Saglik
    REVIR = "saglik/revir_ziyaretleri.json"

    # Sosyal
    KULUPLER = "sosyal_etkinlik/kulupler.json"
    ETKINLIKLER = "sosyal_etkinlik/etkinlikler.json"

    # Erken uyari + davranissal risk
    EU_RISK = "erken_uyari/risk_records.json"
    DVR_RISK = "davranissal_risk/risk_records.json"
    DVR_PROTOCOL = "davranissal_risk/protocols.json"
    DVR_AUDIT = "davranissal_risk/audit_log.json"

    # Kurum
    POZISYONLAR = "kurumsal/pozisyonlar.json"
    DUYURULAR = "akademik/etkinlik_duyurular.json"
    YEMEK = "akademik/yemek_menusu.json"

    # Toplanti / Randevu
    TOPLANTILAR = "toplanti/toplantilar.json"
    RANDEVULAR = "akademik/veli_randevular.json"

    # Mezunlar
    MEZUNLAR = "mezunlar/mezunlar.json"
