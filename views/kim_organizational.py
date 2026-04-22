"""
Kurumsal Organizasyon ve İletişim Modulu
====================
Kurum profili ve organizasyon şeması yonetimi.
Pozisyon CRUD, hiyerarsi, Graphviz sema ve PDF rapor.
"""

from __future__ import annotations

import io
import json
import os
import re
import uuid
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("kurumsal_org")
except Exception:
    pass
from utils.ui_kit import confirm_action

from utils.tenant import tenant_key, get_tenant_dir, get_data_path
from utils.shared_data import (
    load_shared_staff, get_all_staff_options,
    load_shared_students, get_student_display_options,
    get_veli_display_options, get_sinif_sube_listesi,
    get_sinif_ogrenci_listesi,
    get_ik_employee_names, get_ik_employee_name_with_position, load_ik_active_employees,
    load_kesin_kayit_adaylari, mark_kesin_kayit_transferred,
    SINIF_LISTESI,
)
from utils.messaging import send_message as _send_message_real
from utils.auth import (
    ROLES, STAFF_CATEGORY_TO_ROLE,
    generate_password, generate_username, get_all_users,
    add_user, add_users_batch, delete_user, reset_password,
    toggle_user_active, user_exists, find_user_by_source,
    _normalize_tr,
)
from models.akademik_takip import (
    AkademikDataStore, Certificate, CertificateTemplate,
    SERTIFIKA_TURLERI, SERTIFIKA_BASLIK_MAP, PRESET_CERT_TEMPLATES,
    VeliMesaj, MESAJ_KATEGORILERI, get_akademik_store,
)
# Sosyal Medya artik bagimsiz modul olarak app.py'den erisiliyor
from views.swot_analizi import render_swot_analizi
from views.veli_memnuniyet import render_veli_memnuniyet
from utils.report_utils import ReportStyler
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG

KIM01_BASE = os.path.join(".streamlit", "KIM-01_TamPaket")

# ===================== KATEGORI TANIMLARI =====================

ORG_CATEGORIES = [
    ("yonetim_kurulu", "Yönetim Kurulu", "#1a237e"),
    ("ust_yonetim", "Üst Yönetim", "#0d47a1"),
    ("okul_yoneticileri", "Okul Yoneticileri", "#1b5e20"),
    ("akademik", "Akademik Liderlik", "#bf360c"),
    ("idari", "İdari Birimler", "#4a148c"),
    ("destek", "Destek Hizmetleri", "#37474f"),
    ("ogretim", "Öğretim Kadrosu", "#006064"),
    ("diger", "Diğer", "#616161"),
]

_CAT_MAP = {c[0]: {"label": c[1], "color": c[2]} for c in ORG_CATEGORIES}
_CAT_IDS = [c[0] for c in ORG_CATEGORIES]
_CAT_LABELS = [c[1] for c in ORG_CATEGORIES]

# IK role_scope -> KOI category eslestirmesi
_ROLE_SCOPE_TO_CAT = {
    "MANAGEMENT": "ust_yonetim",
    "TEACHER": "ogretim",
    "ADMIN": "idari",
    "SUPPORT": "destek",
    "ALL": "diger",
}


# ===================== VERI FONKSIYONLARI =====================

def get_profile_path() -> str:
    return os.path.join(get_tenant_dir(), "kim01_profile.json")


def get_org_path() -> str:
    return os.path.join(get_tenant_dir(), "kim01_org_simple.json")


def load_profile() -> dict:
    path = get_profile_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_profile(payload: dict) -> None:
    os.makedirs(os.path.dirname(get_profile_path()), exist_ok=True)
    with open(get_profile_path(), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def save_profile_logo(logo_file) -> str:
    if logo_file is None:
        return ""
    ext = os.path.splitext(logo_file.name)[1].lower()
    if ext not in {".png", ".jpg", ".jpeg"}:
        ext = ".png"
    logo_path = os.path.join(get_tenant_dir(), f"kim01_logo{ext}")
    os.makedirs(os.path.dirname(logo_path), exist_ok=True)
    with open(logo_path, "wb") as f:
        f.write(logo_file.getvalue())
    return logo_path


def load_base_titles() -> list[str]:
    csv_path = os.path.join(KIM01_BASE, "KIM-01_IMPORT_OrganizasyonSemasi_Nodes.csv")
    titles: list[str] = []
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            for value in df.get("node_name", []):
                if isinstance(value, str) and value.strip():
                    titles.append(value.strip())
        except Exception:
            pass
    # CSV'den gelen + varsayilan pozisyonlari birlestir (tekrarsiz)
    combined = list(dict.fromkeys(titles + DEFAULT_ORG_TITLES))
    return combined


# ===================== POZISYON FONKSIYONLARI =====================

def _gen_pos_id() -> str:
    return f"pos_{uuid.uuid4().hex[:8]}"


def _infer_category(title: str) -> str:
    """Unvan metninden otomatik kategori tahmini."""
    norm = title.lower()
    checks = [
        ("yonetim_kurulu", ["yonetim kurulu", "kurucu", "mutevelli",
                            "yönetim kurulu", "mütevelli"]),
        ("ust_yonetim", ["genel mudur", "genel müdür", "genel koordinat"]),
        ("okul_yoneticileri", ["mudur", "müdür", "koordinat"]),
        ("akademik", ["akademik", "zumre", "zümre", "bolum bas", "bölüm baş"]),
        ("idari", ["idari", "muhasebe", "finans", "insan kaynak"]),
        ("destek", ["guvenlik", "güvenlik", "temizlik", "kantin",
                     "servis", "teknik"]),
        ("ogretim", ["ogretmen", "öğretmen", "rehber"]),
    ]
    for cat_id, keywords in checks:
        if any(k in norm for k in keywords):
            return cat_id
    return "diger"


def _load_positions() -> list[dict]:
    """Pozisyonlari yukle. Eski format varsa otomatik donustur."""
    path = get_org_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return []
        # Yeni format
        if "positions" in data:
            return data["positions"]
        # Eski format -> migrasyon
        if "items" in data:
            selected = [it for it in data.get("items", []) if it.get("selected")]
            positions = []
            title_to_id = {}
            for item in selected:
                pid = _gen_pos_id()
                t = item.get("title", "")
                title_to_id[t] = pid
                positions.append({
                    "id": pid,
                    "title": t,
                    "person_name": "",
                    "department": "",
                    "parent_id": None,
                    "category": _infer_category(t),
                    "order": len(positions),
                })
            for i, item in enumerate(selected):
                parents = item.get("parents", [])
                if parents and parents[0] in title_to_id:
                    positions[i]["parent_id"] = title_to_id[parents[0]]
            _save_positions(positions)
            return positions
    except Exception:
        pass
    return []


def _save_positions(positions: list[dict]) -> None:
    os.makedirs(os.path.dirname(get_org_path()), exist_ok=True)
    with open(get_org_path(), "w", encoding="utf-8") as f:
        json.dump({"positions": positions}, f, ensure_ascii=False, indent=2)


# ===================== CALISAN TANIMLARI =====================

MEZUNIYET_OPTIONS = [
    "Okur Yazar",
    "İlkokul",
    "Ortaokul",
    "Lise",
    "Universite",
    "Yuksek Lisans",
    "Doktora",
    "Docent",
    "Profesor",
]

STAFF_UNVAN_OPTIONS = [
    # Yonetim Kurulu
    "Kurucu / Yönetim Kurulu Baskani",
    "Yönetim Kurulu Uyesi",
    # Ust Yonetim
    "Genel Mudur",
    "Genel Mudur Yardimcisi",
    "Egitim Koordinatoru",
    "Mali Isler Muduru",
    "Insan Kaynaklari Muduru",
    # Okul Yoneticileri
    "Okul Muduru",
    "Mudur Yardimcisi",
    "Mudur Basyardimcisi",
    # Akademik Liderlik
    "Akademik Kurul Baskani",
    "Bolum Baskani",
    "Zumre Baskani - Yabancilar Diller",
    "Zumre Baskani - Uygulamali Dersler",
    "Zumre Baskani - Rehberlik / PDR",
    "Zumre Baskani - Sozel",
    "Zumre Baskani - Sayısal",
    # Ogretim Kadrosu
    "Anaokulu Öğretmeni",
    "İlkokul Öğretmeni",
    "Ortaokul Öğretmeni",
    "Lise Öğretmeni",
    "Branş Öğretmeni",
    "Rehber Öğretmen / PDR Uzmani",
    "Özel Egitim Öğretmeni",
    "Stajyer Öğretmen",
    # Idari Birimler
    "Muhasebe / Finans",
    "Öğrenci Isleri",
    "Insan Kaynaklari Uzmani",
    "Bilgi İşlem / IT",
    "Kutuphane Sorumlusu",
    "Laboratuvar Sorumlusu",
    "Halkla Iliskiler / Tanitim",
    "Sekreter / Yazici",
    # Destek Hizmetleri
    "Temizlik Personeli",
    "Guvenlik Personeli",
    "Servis / Soforu",
    "Asci / Mutfak Personeli",
    "Saglik Personeli / Hemsire",
    "Bahcivan / Teknik Bakim",
]

# Organizasyon semasi için ek pozisyon onerileri (CSV bulunamazsa kullanilir)
DEFAULT_ORG_TITLES = [
    "Kurucu / Yönetim Kurulu Baskani",
    "Yönetim Kurulu Uyesi",
    "Genel Mudur",
    "Genel Mudur Yardimcisi",
    "Egitim Koordinatoru",
    "Mali Isler Muduru",
    "Insan Kaynaklari Muduru",
    "Okul Muduru",
    "Mudur Yardimcisi",
    "Mudur Basyardimcisi",
    "Akademik Kurul Baskani",
    "Bolum Baskani",
    "Zumre Baskani - Yabanci Diller",
    "Zumre Baskani - Uygulamali Dersler",
    "Zumre Baskani - Rehberlik / PDR",
    "Zumre Baskani - Sozel",
    "Zumre Baskani - Sayısal",
    "Anaokulu Öğretmenleri",
    "İlkokul Öğretmenleri",
    "Ortaokul Öğretmenleri",
    "Lise Öğretmenleri",
    "Rehberlik / PDR Birimi",
    "Özel Egitim Birimi",
    "Muhasebe / Finans",
    "Öğrenci Isleri",
    "Insan Kaynaklari",
    "Bilgi İşlem / IT",
    "Kutuphane",
    "Laboratuvar",
    "Halkla Iliskiler / Tanitim",
    "Temizlik Hizmetleri",
    "Guvenlik Hizmetleri",
    "Servis / Ulasim",
    "Yemekhane / Mutfak",
    "Saglik Birimi",
]


def get_staff_path() -> str:
    return os.path.join(get_tenant_dir(), "kim01_staff.json")


def _gen_staff_id() -> str:
    return f"staff_{uuid.uuid4().hex[:8]}"


def _load_staff() -> list[dict]:
    path = get_staff_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and "staff" in data:
            items = data["staff"]
        else:
            return []
        # Ensure every staff record has an id (migration)
        for item in items:
            if not item.get("id"):
                item["id"] = _gen_staff_id()
        return items
    except Exception:
        return []


def _save_staff(staff: list[dict]) -> None:
    os.makedirs(os.path.dirname(get_staff_path()), exist_ok=True)
    with open(get_staff_path(), "w", encoding="utf-8") as f:
        json.dump({"staff": staff}, f, ensure_ascii=False, indent=2)


# ===================== ILETISIM TANIMLARI =====================

KANAL_OPTIONS = [
    ("panel", "Kurumsal Panel", "#1e40af"),
    ("sms", "SMS", "#10b981"),
    ("whatsapp", "WhatsApp", "#25d366"),
    ("email", "E-posta", "#2563eb"),
]
_KANAL_MAP = {k[0]: {"label": k[1], "color": k[2]} for k in KANAL_OPTIONS}

SABLON_TIPLERI = [
    ("toplanti", "Toplanti Duyurusu"),
    ("genel_duyuru", "Genel Duyuru"),
    ("toren", "Toren Duyurusu"),
    ("sinav", "Sınav Bilgilendirme"),
    ("veli_bilgi", "Veli Bilgilendirme"),
    ("etkinlik", "Etkinlik Daveti"),
    ("acil", "Acil Duyuru"),
    ("tanitim", "Tanitim"),
    ("ozel", "Serbest Mesaj"),
]

SABLON_ICERIK = {
    "toplanti": "Sayın {alici},\n\n{tarih} tarihinde saat {saat}'de {yer} adresinde toplanti yapilacaktir.\n\nGündem: {gundem}\n\nKatiliminizi bekleriz.\n\nSaygilarimizla,\n{gonderen}",
    "genel_duyuru": "Sayın {alici},\n\n{icerik}\n\nBilgilerinize sunariz.\n\nSaygilarimizla,\n{gonderen}",
    "toren": "Sayın {alici},\n\n{tarih} tarihinde duzenlenen {toren_adi} torenine davetlisiniz.\n\nYer: {yer}\nSaat: {saat}\n\nKatiliminizi bekleriz.\n\nSaygilarimizla,\n{gonderen}",
    "sinav": "Sayın {alici},\n\n{sinav_adi} sinavi {tarih} tarihinde yapilacaktir.\n\nDers: {ders}\nSaat: {saat}\n\nBaşarılar dileriz.\n\nSaygilarimizla,\n{gonderen}",
    "veli_bilgi": "Sayın {alici},\n\nÖğrenciniz {ogrenci} hakkinda bilgilendirme:\n\n{icerik}\n\nSaygilarimizla,\n{gonderen}",
    "etkinlik": "Sayın {alici},\n\n{etkinlik_adi} etkinligine davetlisiniz.\n\nTarih: {tarih}\nYer: {yer}\nSaat: {saat}\n\n{icerik}\n\nSaygilarimizla,\n{gonderen}",
    "acil": "ACIL DUYURU\n\nSayın {alici},\n\n{icerik}\n\nIvedi bilgilerinize sunariz.\n\n{gonderen}",
    "tanitim": "Sayın {alici},\n\n{icerik}\n\nDetayli bilgi icin: {iletisim}\n\nSaygilarimizla,\n{gonderen}",
    "ozel": "",
}

MESAJ_DURUM = [
    ("iletildi", "İletildi", "#10b981"),
    ("iletilemedi", "İletilemedi", "#ef4444"),
    ("beklemede", "Beklemede", "#f59e0b"),
]

KURUM_ICI_GRUPLAR = [
    ("tumu", "Tüm Personel"),
    ("yonetim_kurulu", "Yönetim Kurulu"),
    ("ust_yonetim", "Üst Yönetim"),
    ("okul_yoneticileri", "Okul Yoneticileri"),
    ("akademik", "Akademik Liderlik"),
    ("idari", "İdari Birimler"),
    ("destek", "Destek Hizmetleri"),
    ("ogretim", "Öğretim Kadrosu"),
]

KADEME_OPTIONS = [
    "Anasınıfı (4 Yaş)", "Anasınıfı (5 Yaş)", "Anasınıfı (Hazırlık)",
    "1. Sınıf", "2. Sınıf", "3. Sınıf", "4. Sınıf",
    "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf",
    "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf",
]

SUBE_OPTIONS = ["A", "B", "C", "D", "E", "F"]


def get_messages_path() -> str:
    return os.path.join(get_tenant_dir(), "kim01_messages.json")


def _gen_msg_id() -> str:
    return f"msg_{uuid.uuid4().hex[:8]}"


def _load_messages() -> list[dict]:
    path = get_messages_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "messages" in data:
            return data["messages"]
        return []
    except Exception:
        return []


def _save_messages(messages: list[dict]) -> None:
    os.makedirs(os.path.dirname(get_messages_path()), exist_ok=True)
    with open(get_messages_path(), "w", encoding="utf-8") as f:
        json.dump({"messages": messages}, f, ensure_ascii=False, indent=2)


# ===================== SIKAYET / ONERI TAKIP =====================

SIKAYET_KATEGORILERI = [
    ("akademik", "Akademik"),
    ("idari", "İdari"),
    ("temizlik", "Temizlik / Hijyen"),
    ("guvenlik", "Guvenlik"),
    ("yemek", "Yemek / Kantin"),
    ("ulasim", "Servis / Ulasim"),
    ("iletisim", "İletişim"),
    ("tesis", "Tesis / Altyapi"),
    ("teknoloji", "Teknoloji / BT"),
    ("diger", "Diğer"),
]
_SIKAYET_KAT_MAP = dict(SIKAYET_KATEGORILERI)

# ISO 10002 Sikayet Yonetimi Surec Asamalari
SIKAYET_DURUM = [
    # --- Takip Asamalari (Aktif) ---
    ("kayit_alindi", "Kayıt Alındı", "#3b82f6"),             # 1. Receipt: Basvuru sisteme kaydedildi
    ("bilgilendirme", "Bilgilendirme Yapıldı", "#3b82f6"),   # 2. Acknowledgement: Basvuru sahibine teyit verildi
    ("degerlendirme", "Değerlendiriliyor", "#f59e0b"),        # 3. Assessment: Siniflandirma, onceliklendirme
    ("inceleme", "İnceleme / Araştırma", "#8b5cf6"),          # 4. Investigation: Kok neden analizi
    ("aksiyon_planlandi", "Aksiyon Planlandı", "#a855f7"),    # 5. Action Planning: Duzeltici faaliyet belirlendi
    ("uygulamada", "Uygulamada", "#14b8a6"),                  # 6. Implementation: Duzeltici faaliyet uygulaniyor
    # --- Sonuc Asamalari (Kapali) ---
    ("cozumlendi", "Çözümlendi", "#10b981"),                  # 7a. Resolved: Sorun tamamen cozuldu
    ("kismen_cozumlendi", "Kısmen Çözümlendi", "#84cc16"),    # 7b. Partially Resolved: Kismi cozum saglandi
    ("cozulemedi", "Çözümlenemedi", "#ef4444"),               # 7c. Unresolved: Cozum saglanamadi (neden belirtilir)
    ("reddedildi", "Reddedildi", "#f97316"),                  # 7d. Rejected: Kapsam disi veya gecersiz
    ("kapandi", "Kapandı / Arşivlendi", "#64748b"),           # 8. Closure: Dogrulama yapildi, arsivlendi
]
_SIKAYET_DURUM_MAP = {d[0]: d[1] for d in SIKAYET_DURUM}
_SIKAYET_DURUM_RENK = {d[0]: d[2] for d in SIKAYET_DURUM}

SIKAYET_ONCELIK = [
    ("dusuk", "Dusuk", "#94a3b8"),
    ("normal", "Normal", "#3b82f6"),
    ("yuksek", "Yuksek", "#f59e0b"),
    ("acil", "Acil", "#ef4444"),
]
_SIKAYET_ONC_RENK = {o[0]: o[2] for o in SIKAYET_ONCELIK}

# SLA sureleri (saat cinsinden): (donus_suresi, cozum_suresi)
SIKAYET_SLA = {
    "normal": {"donus_saat": 24, "cozum_saat": 72, "label": "24 saat donus / 72 saat cozum"},
    "yuksek":  {"donus_saat": 24, "cozum_saat": 48, "label": "24 saat donus / 48 saat cozum"},
    "acil":    {"donus_saat": 4,  "cozum_saat": 24, "label": "2-4 saat donus / 24 saat cozum"},
    "dusuk":   {"donus_saat": 48, "cozum_saat": 120, "label": "48 saat donus / 120 saat cozum"},
}

SIKAYET_TUR = [("sikayet", "Sikayet"), ("oneri", "Oneri"), ("talep", "Talep")]
SIKAYET_KAYNAK = [
    ("veli", "Veli"), ("ogrenci", "Öğrenci"), ("calisan", "Çalışan"),
    ("ziyaretci", "Ziyaretçi"), ("diger", "Diğer"),
]
SIKAYET_KANAL = [
    ("mail", "E-posta"),
    ("telefon", "Telefon"),
    ("sms", "SMS"),
    ("yuzyuze", "Yuz Yuze"),
    ("whatsapp", "WhatsApp"),
    ("sosyal_medya", "Sosyal Medya Mesaji / Yorumu"),
    ("ikinci_kisi", "2. Kişi Vasıtasıyla"),
    ("diger", "Diğer"),
]

# Sonuc asamalari aciklama
# ISO 10002 Sonuc Asamasi Aciklamalari
_SONUC_ASAMALARI = {
    "cozumlendi": "Çözümlendi — Sorun tamamen giderildi, basvuru sahibi bilgilendirildi ve dogrulama yapildi",
    "kismen_cozumlendi": "Kısmen Çözümlendi — Kismi iyilestirme saglandi, tam cozum icin ek adimlar planlanabilir",
    "cozulemedi": "Çözümlenemedi — Mevcut kosullarda cozum saglanamadi, neden ve alternatifler belirtildi",
    "reddedildi": "Reddedildi — Basvuru kapsam disi, yetkisiz veya gecersiz bulundu, gerekce bildirildi",
    "kapandi": "Kapandı / Arşivlendi — Surec tamamlandi, etki analizi yapildi ve kayit arsivlendi",
}

# Aktif durumlar — Takip sekmesinde gorünür (ISO 10002: Receipt → Implementation)
_TAKIP_DURUMLARI = {"kayit_alindi", "bilgilendirme", "degerlendirme", "inceleme", "aksiyon_planlandi", "uygulamada"}
# Sonuçlanmış durumlar — Sonuç Ekraninda gorünür (ISO 10002: Resolution → Closure)
_SONUC_DURUMLARI = {"cozumlendi", "kismen_cozumlendi", "cozulemedi", "reddedildi", "kapandi"}


def _hesapla_sla_durumu(record: dict) -> dict:
    """SLA performansini hesapla. Donus ve cozum suresi kontrolu."""
    oncelik = record.get("oncelik", "normal")
    sla = SIKAYET_SLA.get(oncelik, SIKAYET_SLA["normal"])
    kayit_str = record.get("kayit_tarih_saat", "") or record.get("created_at", "")
    sonuc = {"donus_durum": "bekliyor", "cozum_durum": "bekliyor",
             "donus_gecen_saat": 0, "cozum_gecen_saat": 0,
             "donus_sla_saat": sla["donus_saat"], "cozum_sla_saat": sla["cozum_saat"]}
    if not kayit_str:
        return sonuc
    try:
        kayit_dt = datetime.fromisoformat(kayit_str)
    except Exception:
        return sonuc
    now = datetime.now()
    durum = record.get("durum", "kayit_alindi")
    # Donus suresi kontrolu (bilgilendirme asamasina gecis = ilk donus)
    donus_dt_str = record.get("donus_tarihi", "")
    if donus_dt_str:
        try:
            donus_dt = datetime.fromisoformat(donus_dt_str)
            gecen = (donus_dt - kayit_dt).total_seconds() / 3600
            sonuc["donus_gecen_saat"] = round(gecen, 1)
            sonuc["donus_durum"] = "zamaninda" if gecen <= sla["donus_saat"] else "gecikti"
        except Exception:
            pass
    elif durum not in ("kayit_alindi",):
        sonuc["donus_durum"] = "belirsiz"
    else:
        gecen = (now - kayit_dt).total_seconds() / 3600
        sonuc["donus_gecen_saat"] = round(gecen, 1)
        sonuc["donus_durum"] = "bekliyor" if gecen <= sla["donus_saat"] else "gecikti"
    # Cozum suresi kontrolu
    cozum_dt_str = record.get("cozum_tarihi", "")
    if cozum_dt_str:
        try:
            cozum_dt = datetime.fromisoformat(cozum_dt_str)
            gecen = (cozum_dt - kayit_dt).total_seconds() / 3600
            sonuc["cozum_gecen_saat"] = round(gecen, 1)
            sonuc["cozum_durum"] = "zamaninda" if gecen <= sla["cozum_saat"] else "gecikti"
        except Exception:
            pass
    elif durum in _SONUC_DURUMLARI:
        sonuc["cozum_durum"] = "belirsiz"
    else:
        gecen = (now - kayit_dt).total_seconds() / 3600
        sonuc["cozum_gecen_saat"] = round(gecen, 1)
        sonuc["cozum_durum"] = "bekliyor" if gecen <= sla["cozum_saat"] else "gecikti"
    return sonuc


def _get_sikayet_path() -> str:
    return os.path.join(get_tenant_dir(), "kim01_sikayet_oneri.json")


def _gen_sikayet_id() -> str:
    return f"so_{uuid.uuid4().hex[:8]}"


# Eski durum key → yeni ISO 10002 durum key migrasyon tablosu
_DURUM_MIGRASYON = {
    "yeni": "kayit_alindi",
    "inceleniyor": "degerlendirme",
    "atandi": "inceleme",
    "sonuc1": "bilgilendirme",
    "sonuc2_cozuldu": "cozumlendi",
    "sonuc2_harekete": "uygulamada",
    "sonuc3_kalici": "cozumlendi",
    "sonuc3_cozulemedi": "cozulemedi",
}


def _load_sikayetler() -> list[dict]:
    path = _get_sikayet_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        # Eski durum degerlerini otomatik migrate et
        migrated = False
        for rec in data:
            eski = rec.get("durum", "")
            if eski in _DURUM_MIGRASYON:
                rec["durum"] = _DURUM_MIGRASYON[eski]
                migrated = True
        if migrated:
            _save_sikayetler(data)
        return data
    except Exception:
        return []


def _save_sikayetler(records: list[dict]) -> None:
    os.makedirs(os.path.dirname(_get_sikayet_path()), exist_ok=True)
    with open(_get_sikayet_path(), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def _upsert_sikayet(record: dict) -> None:
    records = _load_sikayetler()
    rid = record.get("id", "")
    for i, r in enumerate(records):
        if r.get("id") == rid:
            records[i] = record
            _save_sikayetler(records)
            return
    records.append(record)
    _save_sikayetler(records)


def _delete_sikayet(record_id: str) -> None:
    records = _load_sikayetler()
    _save_sikayetler([r for r in records if r.get("id") != record_id])


# ===================== GRAPHVIZ SEMA =====================

def _compute_levels(positions: list[dict]) -> dict[str, int]:
    """BFS ile her pozisyonun hiyerarsi seviyesini hesapla."""
    valid_ids = {p["id"] for p in positions}
    child_map: dict[str, list[str]] = {}
    for p in positions:
        pid = p.get("parent_id")
        if pid and pid in valid_ids:
            child_map.setdefault(pid, []).append(p["id"])
    roots = [p["id"] for p in positions
             if not p.get("parent_id") or p["parent_id"] not in valid_ids]
    levels: dict[str, int] = {}
    queue = list(roots)
    for r in roots:
        levels[r] = 0
    while queue:
        cur = queue.pop(0)
        for ch in child_map.get(cur, []):
            if ch not in levels:
                levels[ch] = levels[cur] + 1
                queue.append(ch)
    for p in positions:
        if p["id"] not in levels:
            levels[p["id"]] = (max(levels.values()) + 1) if levels else 0
    return levels


def _escape_dot(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("<", "\\<").replace(">", "\\>")


def _build_org_dot(positions: list[dict]) -> str:
    """Graphviz DOT formatinda organizasyon şeması olustur."""
    lines = [
        'digraph OrgChart {',
        '  rankdir=TB;',
        '  graph [bgcolor="transparent", pad="0.5", nodesep="0.7", ranksep="1.0"];',
        '  node [shape=box, style="rounded,filled", fontname="Arial,Helvetica,sans-serif",'
        ' fontsize=10, margin="0.25,0.12", penwidth=0];',
        '  edge [color="#64748b", arrowsize=0.8, penwidth=1.5];',
    ]
    valid_ids = {p["id"] for p in positions}

    for pos in positions:
        cat = _CAT_MAP.get(pos.get("category", "diger"), _CAT_MAP["diger"])
        parts = [_escape_dot(pos["title"])]
        if pos.get("person_name"):
            parts.append(_escape_dot(pos["person_name"]))
        if pos.get("department"):
            parts.append("(" + _escape_dot(pos["department"]) + ")")
        label = "\\n".join(parts)
        lines.append(
            f'  "{pos["id"]}" [label="{label}",'
            f' fillcolor="{cat["color"]}", fontcolor="white"];'
        )

    for pos in positions:
        pid = pos.get("parent_id")
        if pid and pid in valid_ids:
            lines.append(f'  "{pid}" -> "{pos["id"]}";')

    lines.append('}')
    return '\n'.join(lines)


# ===================== PDF RAPOR =====================

def _setup_pdf_fonts():
    """PDF için font ayarla. DejaVuSans > Segoe UI > Helvetica."""
    from utils.shared_data import ensure_turkish_pdf_fonts
    return ensure_turkish_pdf_fonts()


def _generate_org_pdf(positions: list[dict]) -> bytes | None:
    """A4 yatay profesyonel organizasyon şeması PDF'i."""
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.colors import HexColor, white
    except ImportError:
        return None

    fn, fb = _setup_pdf_fonts()

    buf = io.BytesIO()
    pw, ph = landscape(A4)
    c = rl_canvas.Canvas(buf, pagesize=landscape(A4))

    # ---- Hiyerarsi hesapla ----
    valid_ids = {p["id"] for p in positions}
    child_map: dict[str, list[str]] = {}
    for p in positions:
        pid = p.get("parent_id")
        if pid and pid in valid_ids:
            child_map.setdefault(pid, []).append(p["id"])

    levels = _compute_levels(positions)
    max_lvl = max(levels.values()) if levels else 0
    max_per_lvl = max(
        (sum(1 for _, lv in levels.items() if lv == l) for l in range(max_lvl + 1)),
        default=1
    )

    # ---- Boyut hesabi ----
    margin_x = 40
    margin_top = 75
    usable_w = pw - 2 * margin_x
    h_gap = 12
    box_w = min(170, max(85, (usable_w - (max_per_lvl - 1) * h_gap) / max_per_lvl))
    box_h = 48
    v_gap = 30

    # ---- Header ----
    c.setFillColor(HexColor("#1a237e"))
    c.rect(0, ph - 52, pw, 52, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(fb, 16)
    profile = load_profile()
    school_name = profile.get("name", "Organizasyon Şeması")
    c.drawCentredString(pw / 2, ph - 24, school_name)
    c.setFont(fn, 9)
    c.drawCentredString(
        pw / 2, ph - 40,
        f"Kurumsal Organizasyon Şeması  -  {datetime.now().strftime('%d.%m.%Y')}"
    )

    # ---- Diyagram alaninin yetip yetmedigini kontrol et ----
    chart_height = (max_lvl + 1) * (box_h + v_gap) - v_gap
    available_height = ph - margin_top - 50  # footer için 50px birak
    if chart_height > available_height and max_lvl > 0:
        scale = available_height / chart_height
        v_gap = int(v_gap * scale)
        box_h = int(box_h * scale)

    # ---- Node pozisyonlari ----
    node_xy: dict[str, tuple[float, float]] = {}
    for lv in range(max_lvl + 1):
        lvl_nodes = [nid for nid, l in levels.items() if l == lv]
        n = len(lvl_nodes)
        tw = n * box_w + (n - 1) * h_gap
        sx = max(margin_x, (pw - tw) / 2)
        cy = ph - margin_top - lv * (box_h + v_gap)
        for i, nid in enumerate(lvl_nodes):
            cx = sx + i * (box_w + h_gap) + box_w / 2
            node_xy[nid] = (cx, cy)

    # ---- Kenarlar (orthogonal cizgiler) ----
    c.setStrokeColor(HexColor("#94a3b8"))
    c.setLineWidth(1.2)
    for p in positions:
        pid = p.get("parent_id")
        if pid and pid in valid_ids and pid in node_xy and p["id"] in node_xy:
            px, py = node_xy[pid]
            cx, cy = node_xy[p["id"]]
            mid_y = (py - box_h + cy) / 2
            c.line(px, py - box_h, px, mid_y)
            c.line(px, mid_y, cx, mid_y)
            c.line(cx, mid_y, cx, cy)

    # ---- Kutular ----
    max_chars = max(10, int(box_w / 5.2))
    for p in positions:
        if p["id"] not in node_xy:
            continue
        cx, cy = node_xy[p["id"]]
        x = cx - box_w / 2
        y = cy - box_h

        cat = _CAT_MAP.get(p.get("category", "diger"), _CAT_MAP["diger"])

        # Golge
        c.setFillColor(HexColor("#d0d0d0"))
        c.roundRect(x + 2, y - 2, box_w, box_h, 5, fill=1, stroke=0)

        # Ana kutu
        c.setFillColor(HexColor(cat["color"]))
        c.roundRect(x, y, box_w, box_h, 5, fill=1, stroke=0)

        # Baslik
        c.setFillColor(white)
        c.setFont(fb, 8)
        title = p["title"]
        if len(title) > max_chars:
            title = title[:max_chars - 2] + ".."
        c.drawCentredString(cx, cy - 15, title)

        # Kisi adi
        if p.get("person_name"):
            c.setFont(fn, 7)
            nm = p["person_name"]
            if len(nm) > max_chars + 2:
                nm = nm[:max_chars] + ".."
            c.drawCentredString(cx, cy - 27, nm)

        # Departman
        if p.get("department"):
            c.setFont(fn, 6)
            dp = p["department"]
            if len(dp) > max_chars + 4:
                dp = dp[:max_chars + 2] + ".."
            c.drawCentredString(cx, cy - 37, f"({dp})")

    # ---- Legenda ----
    ly = 20
    c.setFont(fb, 7)
    c.setFillColor(HexColor("#333333"))
    c.drawString(margin_x, ly, "Kategoriler:")
    lx = margin_x + 55
    for cat_id, cat_info in _CAT_MAP.items():
        c.setFillColor(HexColor(cat_info["color"]))
        c.roundRect(lx, ly - 1, 8, 8, 2, fill=1, stroke=0)
        c.setFillColor(HexColor("#333333"))
        c.setFont(fn, 6)
        c.drawString(lx + 11, ly, cat_info["label"])
        lx += 82

    # ---- Footer ----
    c.setFont(fn, 7)
    c.setFillColor(HexColor("#999999"))
    c.drawRightString(pw - margin_x, ly, "SmartCampus AI - Kurumsal Organizasyon ve İletişim")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()


# ===================== STIL FONKSIYONLARI =====================

def _inject_css():
    """SaaS dashboard CSS - AT/OD ile ayni tasarim dili."""
    inject_common_css("kim")
    st.markdown("""<style>
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(180deg, #0B0F19 0%, #131825 100%);
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #0f172a; color: #e2e8f0; border: 1px solid #334155; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease; border-left: 4px solid #2563eb;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; font-size: 0.75rem !important;
        font-weight: 600 !important; text-transform: uppercase !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0B0F19 !important; font-weight: 800 !important; font-size: 1.5rem !important; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        border: none !important; border-radius: 10px !important; font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important; transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover { box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
        transform: translateY(-2px) !important; }
    .stButton > button:not([kind]) { border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important;
        font-weight: 500 !important; }
    .stButton > button:not([kind]):hover { border-color: #2563eb !important; background: #eff6ff !important; }
    details[data-testid="stExpander"] { border: 1px solid #334155 !important;
        border-radius: 12px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
    details[data-testid="stExpander"] summary { font-weight: 600 !important; padding: 12px 16px !important; }
    div[data-baseweb="select"] > div, .stTextInput > div > div > input,
    .stTextArea > div > div > textarea { border-radius: 10px !important; border-color: #e2e8f0 !important; }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #2563eb !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important; }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; box-shadow: 0 4px 12px rgba(5,150,105,0.25) !important;
    }
    hr { border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #cbd5e1 50%, transparent 100%) !important; }
    .stAlert { border-radius: 10px !important; }

    /* ─── KIM Modülü: Ana sekmeler kompakt görünüm (10 sekme tek satıra/wrap) ─── */
    /* Sadece ≥10 sekmeli ana tab listesini hedefle, alt sekmeleri etkileme */
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab-list"],
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) div[role="tablist"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 4px !important;
        padding: 6px !important;
        background: #0f172a !important;
        border-radius: 10px !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab"],
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) button[role="tab"] {
        padding: 5px 10px !important;
        min-height: 28px !important;
        height: 28px !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        border-radius: 6px !important;
        background: #1e293b !important;
        color: #cbd5e1 !important;
        border: 1px solid #334155 !important;
        flex: 0 0 auto !important;
        margin: 0 !important;
        line-height: 1.1 !important;
    }
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab"] p,
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) button[role="tab"] p {
        font-size: 0.7rem !important;
        margin: 0 !important;
        color: #cbd5e1 !important;
        line-height: 1.1 !important;
    }
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab"]:hover,
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) button[role="tab"]:hover {
        background: #334155 !important;
        border-color: #2563eb !important;
        color: #fff !important;
    }
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        border-color: #2563eb !important;
        color: #fff !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.35) !important;
    }
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab"][aria-selected="true"] p,
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) button[role="tab"][aria-selected="true"] p {
        color: #fff !important;
        font-weight: 800 !important;
    }
    /* Aktif sekmenin altındaki indicator çizgisini gizle (bizim background gösterimi var) */
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    div[data-testid="stTabs"]:has([data-baseweb="tab"]:nth-child(10)) [data-baseweb="tab-border"] {
        display: none !important;
    }
    </style>""", unsafe_allow_html=True)


def _bk_info_row(label: str, value: str) -> str:
    """Bilgi karti için etiket-deger satiri HTML'i dondurur."""
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;'
        f'padding:3px 0;border-bottom:1px solid #1A2035">'
        f'<span style="font-size:0.78rem;color:#94a3b8;font-weight:500">{label}</span>'
        f'<span style="font-size:0.82rem;color:#0B0F19;font-weight:600;text-align:right;'
        f'max-width:60%;word-break:break-word">{value}</span>'
        f'</div>'
    )


def _styled_card(title: str, content: str, icon: str = "", color: str = "#2563eb"):
    """Card component for profile sections."""
    st.markdown(f"""<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:14px;
    padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-top:3px solid {color};
    margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
    <span style="font-size:1.1rem">{icon}</span>
    <span style="font-weight:700;color:#0B0F19;font-size:0.95rem">{title}</span></div>
    <div style="color:#94a3b8;font-size:0.85rem;line-height:1.6;white-space:pre-wrap">{content or '<span style=color:#94a3b8>Henuz girilmedi</span>'}</div>
    </div>""", unsafe_allow_html=True)


# ===================== SERTIFIKA YARDIMCI FONKSIYONLAR =====================

SERTIFIKA_GRUPLARI = ["Öğrenci", "Çalışan", "Veli", "Disardan Katilimci"]
SERTIFIKA_VEREN_SECENEKLERI = [
    "Okul Muduru",
    "Kampus Muduru",
    "Genel Mudur Yardimcisi",
    "Genel Mudur",
    "Kurucu",
    "Yönetim Kurulu Baskani",
]


def _cert_load_grup_data(grup: str) -> dict[str, dict]:
    """Sertifika grubuna gore kisi seceneklerini yukle."""
    if grup == "Öğrenci":
        return get_student_display_options(include_empty=True)
    elif grup == "Çalışan":
        return get_all_staff_options()
    elif grup == "Veli":
        return get_veli_display_options(include_empty=True)
    return {}


def _cert_load_bulk_list(grup: str, sinif_filtre=None, sube_filtre=None) -> list[dict]:
    """Toplu sertifika için kisi listesi yukle."""
    if grup == "Öğrenci":
        students = load_shared_students()
        if sinif_filtre:
            students = [s for s in students if str(s.get("sinif", "")) == str(sinif_filtre)]
        if sube_filtre:
            students = [s for s in students if s.get("sube", "") == sube_filtre]
        return [{"ad": f'{s.get("ad", "")} {s.get("soyad", "")}'.strip(),
                 "id": s.get("id", ""), "sinif": str(s.get("sinif", "")),
                 "sube": s.get("sube", "")} for s in students if f'{s.get("ad", "")} {s.get("soyad", "")}'.strip()]
    elif grup == "Çalışan":
        staff = load_shared_staff()
        result = []
        for s in staff:
            tam_ad = f'{s.get("ad", "")} {s.get("soyad", "")}'.strip()
            if not tam_ad:
                continue
            brans = s.get("brans", "")
            unvan = s.get("unvan", "")
            if unvan and brans:
                display = f"{tam_ad} ({unvan} - {brans})"
            elif brans:
                display = f"{tam_ad} ({brans})"
            elif unvan:
                display = f"{tam_ad} ({unvan})"
            else:
                display = tam_ad
            result.append({"ad": display, "id": s.get("id", ""), "sinif": "", "sube": ""})
        return result
    elif grup == "Veli":
        students = load_shared_students()
        result = []
        for s in students:
            veli = s.get("veli_adi", "")
            if not veli:
                anne = f'{s.get("anne_adi", "")} {s.get("anne_soyadi", "")}'.strip()
                baba = f'{s.get("baba_adi", "")} {s.get("baba_soyadi", "")}'.strip()
                veli = anne or baba
            if veli:
                result.append({"ad": veli, "id": s.get("id", ""),
                               "sinif": str(s.get("sinif", "")), "sube": s.get("sube", "")})
        return result
    return []


def _generate_certificate_from_template(
    template: dict,
    kurum_adi: str,
    logo_path: str,
    sertifika_turu: str,
    alici_adi: str,
    sinif_sube: str,
    verilis_tarihi: str,
    verilis_nedeni: str,
    aciklama: str = "",
    sertifika_veren: str = "",
) -> bytes:
    """Template-driven sertifika PDF uretimi."""
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.pagesizes import A4, landscape, portrait
    from reportlab.lib.colors import HexColor

    fn, fn_bold = _setup_pdf_fonts()

    tpl = CertificateTemplate.from_dict(template)
    main_color_hex = tpl.get_effective_color(sertifika_turu)
    main_color = HexColor(main_color_hex)

    buf = io.BytesIO()
    orientation = landscape if tpl.page_orientation == "landscape" else portrait
    page_w, page_h = orientation(A4)
    c = rl_canvas.Canvas(buf, pagesize=orientation(A4))

    # Arka plan
    c.setFillColor(HexColor(tpl.background_color))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Cerceve
    if tpl.border_enabled:
        if tpl.border_width_outer > 0:
            c.setStrokeColor(main_color)
            c.setLineWidth(tpl.border_width_outer)
            m = tpl.border_margin_outer
            c.rect(m, m, page_w - 2 * m, page_h - 2 * m, fill=0, stroke=1)
        if tpl.border_width_inner > 0:
            c.setLineWidth(tpl.border_width_inner)
            m2 = tpl.border_margin_inner
            c.rect(m2, m2, page_w - 2 * m2, page_h - 2 * m2, fill=0, stroke=1)

    # Kose susleri
    if tpl.corner_decorations and tpl.corner_dot_radius > 0:
        m = tpl.border_margin_outer
        offset = 8
        for cx_c, cy_c in [(m + offset, m + offset), (page_w - m - offset, m + offset),
                           (m + offset, page_h - m - offset), (page_w - m - offset, page_h - m - offset)]:
            c.setFillColor(main_color)
            c.circle(cx_c, cy_c, tpl.corner_dot_radius, fill=1, stroke=0)

    cx_mid = page_w / 2

    # Ust dekoratif cizgi
    if tpl.decorative_lines:
        y_top = page_h - 60
        c.setStrokeColor(main_color)
        c.setLineWidth(2)
        lw = tpl.decorative_line_width
        c.line(cx_mid - lw, y_top, cx_mid + lw, y_top)
        c.setLineWidth(0.5)
        c.line(cx_mid - lw + 20, y_top - 4, cx_mid + lw - 20, y_top - 4)

    # --- Icerik yuksekligini hesapla (dikey ortalama icin) ---
    has_logo = tpl.logo_enabled and logo_path and os.path.exists(logo_path)
    title_text = tpl.title_text or SERTIFIKA_BASLIK_MAP.get(
        sertifika_turu, f"{sertifika_turu.upper()} SERTIFIKASI")
    neden_text = verilis_nedeni or aciklama or ""

    # Neden satirlarini onceden hesapla
    neden_lines = []
    if neden_text:
        max_text_w = page_w - 200
        words = neden_text.split()
        current = ""
        for w in words:
            test = f"{current} {w}".strip()
            if c.stringWidth(test, fn, tpl.reason_font_size) < max_text_w:
                current = test
            else:
                if current:
                    neden_lines.append(current)
                current = w
        if current:
            neden_lines.append(current)
        neden_lines = neden_lines[:tpl.reason_max_lines]

    # Toplam icerik yuksekligi
    total_h = 0.0
    if has_logo:
        total_h += tpl.logo_height + 10
    total_h += tpl.institution_font_size + 14  # kurum adi
    total_h += tpl.title_font_size + 11  # baslik
    total_h += 15  # baslik alt cizgi
    if tpl.body_prefix:
        total_h += tpl.body_font_size + 18
    total_h += tpl.recipient_font_size + 2  # alici adi
    if sinif_sube:
        total_h += tpl.class_font_size + 14
    else:
        total_h += 10
    if neden_lines:
        total_h += (tpl.reason_font_size + 5) * len(neden_lines) + 5
    total_h += tpl.body_font_size + 23  # alt metin
    total_h += tpl.date_font_size + 29  # tarih
    if tpl.signature_enabled:
        total_h += 30  # imza alani

    # Kullanilabilir alan: cerceve/dekoratif cizgi icinde
    margin_top = 80
    margin_bot = 90 if tpl.decorative_lines else 70
    usable_h = page_h - margin_top - margin_bot
    y_cursor = margin_bot + usable_h / 2 + total_h / 2

    # Logo
    if has_logo:
        try:
            l_w, l_h = tpl.logo_width, tpl.logo_height
            c.drawImage(logo_path, cx_mid - l_w / 2, y_cursor - l_h,
                        width=l_w, height=l_h, preserveAspectRatio=True, mask='auto')
            y_cursor -= l_h + 10
        except Exception:
            y_cursor -= 10

    # Kurum adi
    c.setFont(fn_bold, tpl.institution_font_size)
    c.setFillColor(HexColor(tpl.institution_color))
    c.drawCentredString(cx_mid, y_cursor, kurum_adi or "")
    y_cursor -= tpl.institution_font_size + 14

    # Baslik
    title_color = HexColor(tpl.title_color) if tpl.title_color else main_color
    c.setFont(fn_bold, tpl.title_font_size)
    c.setFillColor(title_color)
    c.drawCentredString(cx_mid, y_cursor, title_text)
    y_cursor -= tpl.title_font_size + 11

    # Baslik alt cizgi
    c.setStrokeColor(main_color)
    c.setLineWidth(1.5)
    c.line(cx_mid - 120, y_cursor + 5, cx_mid + 120, y_cursor + 5)
    y_cursor -= 15

    # Ust metin
    if tpl.body_prefix:
        c.setFont(fn, tpl.body_font_size)
        c.setFillColor(HexColor(tpl.body_color))
        c.drawCentredString(cx_mid, y_cursor, tpl.body_prefix)
        y_cursor -= tpl.body_font_size + 18

    # Alici adi
    c.setFont(fn_bold, tpl.recipient_font_size)
    c.setFillColor(HexColor(tpl.recipient_color))
    c.drawCentredString(cx_mid, y_cursor, alici_adi)
    y_cursor -= tpl.recipient_font_size + 2

    # Sinif/Sube
    if sinif_sube:
        c.setFont(fn, tpl.class_font_size)
        c.setFillColor(HexColor(tpl.class_color))
        c.drawCentredString(cx_mid, y_cursor, sinif_sube)
        y_cursor -= tpl.class_font_size + 14
    else:
        y_cursor -= 10

    # Neden
    if neden_lines:
        c.setFont(fn, tpl.reason_font_size)
        c.setFillColor(HexColor(tpl.reason_color))
        for line in neden_lines:
            c.drawCentredString(cx_mid, y_cursor, line)
            y_cursor -= tpl.reason_font_size + 5
        y_cursor -= 5

    # Alt metin
    c.setFont(fn, tpl.body_font_size)
    c.setFillColor(HexColor(tpl.body_color))
    c.drawCentredString(cx_mid, y_cursor, tpl.body_suffix)
    y_cursor -= tpl.body_font_size + 23

    # Tarih
    c.setFont(fn, tpl.date_font_size)
    c.setFillColor(HexColor(tpl.date_color))
    c.drawCentredString(cx_mid, y_cursor, f"{tpl.date_prefix}{verilis_tarihi}")
    y_cursor -= tpl.date_font_size + 29

    # Imza alani
    if tpl.signature_enabled:
        sig_line_w = 60
        # sertifika_veren parametresi varsa imza etiketinde onu kullan
        effective_sig_label = sertifika_veren if sertifika_veren else tpl.signature_label
        if tpl.second_signature_enabled:
            left_x = page_w * 0.25
            right_x = page_w * 0.75
            for sig_x, sig_label in [(left_x, tpl.second_signature_label), (right_x, effective_sig_label)]:
                c.setStrokeColor(HexColor(tpl.signature_line_color))
                c.setLineWidth(0.8)
                c.line(sig_x - sig_line_w, y_cursor + 15, sig_x + sig_line_w, y_cursor + 15)
                c.setFont(fn, 10)
                c.setFillColor(HexColor(tpl.body_color))
                c.drawCentredString(sig_x, y_cursor, sig_label)
        else:
            pos_map = {"left": page_w * 0.2, "center": cx_mid, "right": page_w - 200}
            sig_x = pos_map.get(tpl.signature_position, page_w - 200)
            c.setStrokeColor(HexColor(tpl.signature_line_color))
            c.setLineWidth(0.8)
            c.line(sig_x - sig_line_w, y_cursor + 15, sig_x + sig_line_w, y_cursor + 15)
            c.setFont(fn, 10)
            c.setFillColor(HexColor(tpl.body_color))
            c.drawCentredString(sig_x, y_cursor, effective_sig_label)

    # Alt dekoratif cizgi
    if tpl.decorative_lines:
        y_bot = 50
        lw = tpl.decorative_line_width
        c.setStrokeColor(main_color)
        c.setLineWidth(2)
        c.line(cx_mid - lw, y_bot, cx_mid + lw, y_bot)
        c.setLineWidth(0.5)
        c.line(cx_mid - lw + 20, y_bot + 4, cx_mid + lw - 20, y_bot + 4)

    # Alt orta sus (ornamental flourish)
    if tpl.bottom_ornament:
        orn_color = HexColor(tpl.ornament_color) if tpl.ornament_color else main_color
        orn_y = 65 if tpl.decorative_lines else 50
        orn_style = getattr(tpl, 'ornament_style', 'classic')

        if orn_style == "diamond":
            # Elmas + yatay cizgiler
            c.setStrokeColor(orn_color)
            c.setFillColor(orn_color)
            c.setLineWidth(1.2)
            # Sol cizgi
            c.line(cx_mid - 100, orn_y, cx_mid - 12, orn_y)
            # Sag cizgi
            c.line(cx_mid + 12, orn_y, cx_mid + 100, orn_y)
            # Merkez elmas (rotated square)
            p = c.beginPath()
            p.moveTo(cx_mid, orn_y + 8)
            p.lineTo(cx_mid + 8, orn_y)
            p.lineTo(cx_mid, orn_y - 8)
            p.lineTo(cx_mid - 8, orn_y)
            p.close()
            c.drawPath(p, fill=1, stroke=1)
            # Kucuk yan elmaslar
            for dx in [-55, 55]:
                p2 = c.beginPath()
                p2.moveTo(cx_mid + dx, orn_y + 4)
                p2.lineTo(cx_mid + dx + 4, orn_y)
                p2.lineTo(cx_mid + dx, orn_y - 4)
                p2.lineTo(cx_mid + dx - 4, orn_y)
                p2.close()
                c.drawPath(p2, fill=1, stroke=0)

        elif orn_style == "medal":
            # Altin madalyon + kirmizi kurdele (Canva stili)
            medal_r = 22
            # Kirmizi kurdele (V seklinde)
            c.setFillColor(HexColor("#c41e1e"))
            c.setStrokeColor(HexColor("#8b1515"))
            c.setLineWidth(0.5)
            ribbon = c.beginPath()
            ribbon.moveTo(cx_mid - 8, orn_y - 2)
            ribbon.lineTo(cx_mid - 18, orn_y - 32)
            ribbon.lineTo(cx_mid - 10, orn_y - 26)
            ribbon.lineTo(cx_mid, orn_y - 34)
            ribbon.lineTo(cx_mid + 10, orn_y - 26)
            ribbon.lineTo(cx_mid + 18, orn_y - 32)
            ribbon.lineTo(cx_mid + 8, orn_y - 2)
            ribbon.close()
            c.drawPath(ribbon, fill=1, stroke=1)
            # Dis halka (koyu altin)
            c.setStrokeColor(HexColor("#6366F1"))
            c.setFillColor(HexColor("#6366F1"))
            c.setLineWidth(2)
            c.circle(cx_mid, orn_y, medal_r, fill=1, stroke=1)
            # Orta halka
            c.setStrokeColor(HexColor("#d4b85c"))
            c.setLineWidth(1.5)
            c.circle(cx_mid, orn_y, medal_r - 4, fill=0, stroke=1)
            # Ic daire (parlak altin)
            c.setFillColor(HexColor("#e8d48b"))
            c.circle(cx_mid, orn_y, medal_r - 6, fill=1, stroke=0)
            # Merkez parlaklik efekti
            c.setFillColor(HexColor("#f5e6a3"))
            c.circle(cx_mid - 3, orn_y + 3, medal_r - 12, fill=1, stroke=0)
            # Dis cember disli kenar efekti
            c.setStrokeColor(HexColor("#a08030"))
            c.setLineWidth(0.5)
            import math
            for i in range(24):
                angle = i * (2 * math.pi / 24)
                x1 = cx_mid + (medal_r - 1) * math.cos(angle)
                y1 = orn_y + (medal_r - 1) * math.sin(angle)
                x2 = cx_mid + (medal_r + 2) * math.cos(angle)
                y2 = orn_y + (medal_r + 2) * math.sin(angle)
                c.line(x1, y1, x2, y2)

        elif orn_style == "laurel":
            # Defne yapragi stili: merkez daire + iki tarafta yaprak deseni
            c.setStrokeColor(orn_color)
            c.setFillColor(orn_color)
            # Merkez daire
            c.circle(cx_mid, orn_y, 6, fill=0, stroke=1)
            c.circle(cx_mid, orn_y, 3, fill=1, stroke=0)
            c.setLineWidth(1.0)
            # Sol yapraklar
            for i in range(5):
                lx = cx_mid - 20 - i * 16
                angle_off = i * 3
                p = c.beginPath()
                p.moveTo(lx, orn_y)
                p.curveTo(lx - 4, orn_y + 10 + angle_off,
                          lx - 10, orn_y + 10 + angle_off,
                          lx - 8, orn_y)
                p.curveTo(lx - 10, orn_y - 10 - angle_off,
                          lx - 4, orn_y - 10 - angle_off,
                          lx, orn_y)
                c.drawPath(p, fill=1, stroke=0)
            # Sag yapraklar (simetrik)
            for i in range(5):
                rx = cx_mid + 20 + i * 16
                angle_off = i * 3
                p = c.beginPath()
                p.moveTo(rx, orn_y)
                p.curveTo(rx + 4, orn_y + 10 + angle_off,
                          rx + 10, orn_y + 10 + angle_off,
                          rx + 8, orn_y)
                p.curveTo(rx + 10, orn_y - 10 - angle_off,
                          rx + 4, orn_y - 10 - angle_off,
                          rx, orn_y)
                c.drawPath(p, fill=1, stroke=0)

        else:  # classic - scrollwork flourish
            c.setStrokeColor(orn_color)
            c.setFillColor(orn_color)
            c.setLineWidth(1.5)
            # Merkez daire
            c.circle(cx_mid, orn_y, 5, fill=1, stroke=0)
            c.circle(cx_mid, orn_y, 8, fill=0, stroke=1)
            # Sol scroll
            p = c.beginPath()
            p.moveTo(cx_mid - 10, orn_y)
            p.curveTo(cx_mid - 30, orn_y + 18,
                      cx_mid - 55, orn_y + 15,
                      cx_mid - 70, orn_y + 5)
            c.drawPath(p, fill=0, stroke=1)
            p2 = c.beginPath()
            p2.moveTo(cx_mid - 10, orn_y)
            p2.curveTo(cx_mid - 30, orn_y - 18,
                       cx_mid - 55, orn_y - 15,
                       cx_mid - 70, orn_y - 5)
            c.drawPath(p2, fill=0, stroke=1)
            # Sol uc kivirim
            p3 = c.beginPath()
            p3.moveTo(cx_mid - 70, orn_y + 5)
            p3.curveTo(cx_mid - 80, orn_y + 10,
                       cx_mid - 85, orn_y + 5,
                       cx_mid - 80, orn_y - 2)
            c.drawPath(p3, fill=0, stroke=1)
            p4 = c.beginPath()
            p4.moveTo(cx_mid - 70, orn_y - 5)
            p4.curveTo(cx_mid - 80, orn_y - 10,
                       cx_mid - 85, orn_y - 5,
                       cx_mid - 80, orn_y + 2)
            c.drawPath(p4, fill=0, stroke=1)
            # Sag scroll (simetrik)
            p5 = c.beginPath()
            p5.moveTo(cx_mid + 10, orn_y)
            p5.curveTo(cx_mid + 30, orn_y + 18,
                       cx_mid + 55, orn_y + 15,
                       cx_mid + 70, orn_y + 5)
            c.drawPath(p5, fill=0, stroke=1)
            p6 = c.beginPath()
            p6.moveTo(cx_mid + 10, orn_y)
            p6.curveTo(cx_mid + 30, orn_y - 18,
                       cx_mid + 55, orn_y - 15,
                       cx_mid + 70, orn_y - 5)
            c.drawPath(p6, fill=0, stroke=1)
            # Sag uc kivirim
            p7 = c.beginPath()
            p7.moveTo(cx_mid + 70, orn_y + 5)
            p7.curveTo(cx_mid + 80, orn_y + 10,
                       cx_mid + 85, orn_y + 5,
                       cx_mid + 80, orn_y - 2)
            c.drawPath(p7, fill=0, stroke=1)
            p8 = c.beginPath()
            p8.moveTo(cx_mid + 70, orn_y - 5)
            p8.curveTo(cx_mid + 80, orn_y - 10,
                       cx_mid + 85, orn_y - 5,
                       cx_mid + 80, orn_y + 2)
            c.drawPath(p8, fill=0, stroke=1)
            # Yatay uzanti cizgileri
            c.setLineWidth(0.8)
            c.line(cx_mid - 85, orn_y, cx_mid - 120, orn_y)
            c.line(cx_mid + 85, orn_y, cx_mid + 120, orn_y)

    # ========== EMBOSSED SEAL (Kabartma Muhur) ==========
    # Tum sertifikalarda otomatik gorunur - sol alt konum
    import math
    seal_r = 38  # Muhur yaricapi
    seal_x = page_w * 0.18  # Sol taraf
    seal_y = 75  # Alt kisim
    # Ana renk: hafif transparan gri tonlari (kabartma efekti)
    seal_base = HexColor("#b8b8b8")
    seal_light = HexColor("#d0d0d0")
    seal_dark = HexColor("#8a8a8a")
    seal_highlight = HexColor("#e8e8e8")

    c.saveState()

    # Golge efekti (hafif offset ile derinlik hissi)
    c.setFillColor(HexColor("#c8c8c8"))
    c.circle(seal_x + 1.5, seal_y - 1.5, seal_r + 1, fill=1, stroke=0)

    # Dis halka (kalin, koyu gri)
    c.setStrokeColor(seal_dark)
    c.setFillColor(seal_light)
    c.setLineWidth(2.5)
    c.circle(seal_x, seal_y, seal_r, fill=1, stroke=1)

    # Disli kenar efekti (32 cikinti)
    c.setStrokeColor(seal_dark)
    c.setLineWidth(1.2)
    for i in range(32):
        angle = i * (2 * math.pi / 32)
        x1 = seal_x + (seal_r - 2) * math.cos(angle)
        y1 = seal_y + (seal_r - 2) * math.sin(angle)
        x2 = seal_x + (seal_r + 1.5) * math.cos(angle)
        y2 = seal_y + (seal_r + 1.5) * math.sin(angle)
        c.line(x1, y1, x2, y2)

    # Ikinci halka (ince, ic cerceve)
    c.setStrokeColor(seal_dark)
    c.setLineWidth(1.5)
    c.circle(seal_x, seal_y, seal_r - 5, fill=0, stroke=1)

    # Yazi halkasi (kurumsal isim - daire etrafinda)
    seal_text = kurum_adi.upper() if kurum_adi else "RESMI BELGE"
    # Maksimum 30 karakter
    if len(seal_text) > 30:
        seal_text = seal_text[:30]
    c.setFillColor(seal_dark)
    c.setFont(fn_bold, 5.5)
    text_r = seal_r - 10  # Yazi dairesi yaricapi
    # Ust yari daire boyunca yazi yaz
    total_arc = math.pi * 0.85  # ~153 derece
    start_angle = math.pi / 2 + total_arc / 2  # Soldan basla
    if len(seal_text) > 1:
        angle_step = total_arc / (len(seal_text) - 1)
    else:
        angle_step = 0
    for idx, ch in enumerate(seal_text):
        a = start_angle - idx * angle_step
        tx = seal_x + text_r * math.cos(a)
        ty = seal_y + text_r * math.sin(a)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(math.degrees(a) - 90)
        c.drawCentredString(0, 0, ch)
        c.restoreState()

    # Alt yazi (sertifika turu) - alt yari daire
    alt_text = sertifika_turu.upper() if sertifika_turu else "SERTIFIKA"
    if len(alt_text) > 20:
        alt_text = alt_text[:20]
    c.setFont(fn_bold, 4.8)
    alt_arc = math.pi * 0.65
    alt_start = -math.pi / 2 - alt_arc / 2
    if len(alt_text) > 1:
        alt_step = alt_arc / (len(alt_text) - 1)
    else:
        alt_step = 0
    for idx, ch in enumerate(alt_text):
        a = alt_start + idx * alt_step
        tx = seal_x + text_r * math.cos(a)
        ty = seal_y + text_r * math.sin(a)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(math.degrees(a) + 90)
        c.drawCentredString(0, 0, ch)
        c.restoreState()

    # Uc yildiz (ust yazi baslangic ve bitis + alt orta)
    c.setFillColor(seal_dark)
    for star_angle in [math.pi / 2 + total_arc / 2 + 0.12,
                       math.pi / 2 - total_arc / 2 - 0.12,
                       -math.pi / 2]:
        sx = seal_x + text_r * math.cos(star_angle)
        sy = seal_y + text_r * math.sin(star_angle)
        # Kucuk yildiz (5 kose)
        star_size = 2.5
        sp = c.beginPath()
        for si in range(10):
            sa = si * (math.pi / 5) - math.pi / 2
            sr = star_size if si % 2 == 0 else star_size * 0.4
            spx = sx + sr * math.cos(sa)
            spy = sy + sr * math.sin(sa)
            if si == 0:
                sp.moveTo(spx, spy)
            else:
                sp.lineTo(spx, spy)
        sp.close()
        c.drawPath(sp, fill=1, stroke=0)

    # Ic daire (parlak alan)
    c.setFillColor(seal_highlight)
    c.circle(seal_x, seal_y, seal_r - 17, fill=1, stroke=0)
    c.setStrokeColor(seal_dark)
    c.setLineWidth(0.8)
    c.circle(seal_x, seal_y, seal_r - 17, fill=0, stroke=1)

    # Merkez amblem - kartal/kalkan stili emblem
    emblem_r = seal_r - 20
    # Kalkan sekli
    shield = c.beginPath()
    shield.moveTo(seal_x, seal_y + emblem_r)
    shield.curveTo(seal_x + emblem_r * 0.9, seal_y + emblem_r * 0.8,
                   seal_x + emblem_r, seal_y + emblem_r * 0.3,
                   seal_x + emblem_r * 0.85, seal_y - emblem_r * 0.1)
    shield.curveTo(seal_x + emblem_r * 0.6, seal_y - emblem_r * 0.7,
                   seal_x + emblem_r * 0.2, seal_y - emblem_r * 0.9,
                   seal_x, seal_y - emblem_r)
    shield.curveTo(seal_x - emblem_r * 0.2, seal_y - emblem_r * 0.9,
                   seal_x - emblem_r * 0.6, seal_y - emblem_r * 0.7,
                   seal_x - emblem_r * 0.85, seal_y - emblem_r * 0.1)
    shield.curveTo(seal_x - emblem_r, seal_y + emblem_r * 0.3,
                   seal_x - emblem_r * 0.9, seal_y + emblem_r * 0.8,
                   seal_x, seal_y + emblem_r)
    c.setFillColor(seal_base)
    c.setStrokeColor(seal_dark)
    c.setLineWidth(0.6)
    c.drawPath(shield, fill=1, stroke=1)

    # Kalkan icinde yildiz
    c.setFillColor(seal_light)
    center_star = c.beginPath()
    star_pts = 5
    for si in range(star_pts * 2):
        sa = si * (math.pi / star_pts) - math.pi / 2
        sr = emblem_r * 0.55 if si % 2 == 0 else emblem_r * 0.22
        spx = seal_x + sr * math.cos(sa)
        spy = seal_y + sr * math.sin(sa)
        if si == 0:
            center_star.moveTo(spx, spy)
        else:
            center_star.lineTo(spx, spy)
    center_star.close()
    c.drawPath(center_star, fill=1, stroke=1)

    # Kabartma highlight efekti (sol ust isigin yansimasi)
    c.setFillColor(HexColor("#f0f0f0"))
    c.setStrokeColor(HexColor("#f0f0f0"))
    c.setLineWidth(0)
    highlight = c.beginPath()
    highlight.moveTo(seal_x - seal_r * 0.15, seal_y + seal_r * 0.65)
    highlight.curveTo(seal_x - seal_r * 0.5, seal_y + seal_r * 0.5,
                      seal_x - seal_r * 0.6, seal_y + seal_r * 0.2,
                      seal_x - seal_r * 0.45, seal_y - seal_r * 0.05)
    highlight.curveTo(seal_x - seal_r * 0.3, seal_y + seal_r * 0.3,
                      seal_x - seal_r * 0.1, seal_y + seal_r * 0.5,
                      seal_x - seal_r * 0.15, seal_y + seal_r * 0.65)
    c.drawPath(highlight, fill=1, stroke=0)

    c.restoreState()

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()


def _generate_certificate_pdf(
    kurum_adi: str, logo_path: str, sertifika_turu: str,
    alici_adi: str, sinif_sube: str, verilis_tarihi: str,
    verilis_nedeni: str, aciklama: str = "",
) -> bytes:
    """Backward-compat wrapper - Klasik preset kullanir."""
    return _generate_certificate_from_template(
        template=PRESET_CERT_TEMPLATES[0],
        kurum_adi=kurum_adi, logo_path=logo_path,
        sertifika_turu=sertifika_turu, alici_adi=alici_adi,
        sinif_sube=sinif_sube, verilis_tarihi=verilis_tarihi,
        verilis_nedeni=verilis_nedeni, aciklama=aciklama,
    )


def _render_sablon_galerisi(store, templates: list[dict], kurum_adi: str, logo_path: str) -> None:
    """Renderforest tarzi sertifika sablon galerisi."""
    styled_section("Şablon Galerisi", "#8b5cf6")

    st.markdown("""<div style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:12px;
    padding:14px 18px;margin-bottom:16px;font-size:12px;color:#5b21b6;border-left:4px solid #8b5cf6;">
    Hazir sablonlardan birini secip sertifika olusturabilir veya kopyalayarak kendi tasariminizi yapabilirsiniz.
    <b>Onizleme</b> ile sablon gorunumunu inceleyebilir, <b>Kopyala & Duzenle</b> ile kendi versiyonunuzu olusturabilirsiniz.
    </div>""", unsafe_allow_html=True)

    # Kategori filtreleri
    _GALERI_KATEGORILER = {
        "Tümü": lambda t: True,
        "Yatay": lambda t: t.get("page_orientation") == "landscape",
        "Dikey": lambda t: t.get("page_orientation") == "portrait",
        "Altın / Lüks": lambda t: any(k in t.get("name", "").lower() for k in ("altin", "altın", "luks", "lüks", "elegans", "zarif", "gul")),
        "Koyu Tema": lambda t: any(k in t.get("name", "").lower() for k in ("koyu", "siyah", "lacivert")),
        "Minimalist": lambda t: any(k in t.get("name", "").lower() for k in ("minimal", "modern", "sade", "pastel")),
        "Klasik / Resmi": lambda t: any(k in t.get("name", "").lower() for k in ("klasik", "resmi", "akademik", "kurumsal", "kahve")),
    }

    fil_col1, fil_col2 = st.columns([3, 1])
    with fil_col1:
        secilen_kat = st.radio("Kategori", list(_GALERI_KATEGORILER.keys()),
                               horizontal=True, key="galeri_kat")
    with fil_col2:
        onizleme_turu = st.selectbox("Önizleme Türü", SERTIFIKA_TURLERI, key="galeri_prev_type")

    filtre_fn = _GALERI_KATEGORILER[secilen_kat]
    filtrelenmis = [t for t in templates if filtre_fn(t)]

    st.caption(f"{len(filtrelenmis)} sablon listeleniyor")

    if not filtrelenmis:
        st.info("Bu kategoride sablon bulunamadi.")
        return

    # Onizleme secimi (session state)
    if "galeri_onizleme_id" not in st.session_state:
        st.session_state["galeri_onizleme_id"] = None

    # --- Grid: 3 kolon ---
    for row_start in range(0, len(filtrelenmis), 3):
        row_items = filtrelenmis[row_start:row_start + 3]
        cols = st.columns(3)
        for col_idx, tpl in enumerate(row_items):
            with cols[col_idx]:
                tpl_id = tpl.get("id", "")
                t_name = tpl.get("name", "Isimsiz")
                t_desc = tpl.get("description", "")
                t_border = tpl.get("border_color", "#2563eb")
                t_bg = tpl.get("background_color", "#fefefe")
                t_orient = tpl.get("page_orientation", "landscape")
                orient_badge = "Yatay" if t_orient == "landscape" else "Dikey"
                orient_icon = "🖼️" if t_orient == "landscape" else "📄"
                has_corner = tpl.get("corner_decorations", False)
                has_deco = tpl.get("decorative_lines", False)
                has_sig2 = tpl.get("second_signature_enabled", False)
                orn_style = tpl.get("ornament_style", "classic")
                orn_labels = {"classic": "Klasik", "diamond": "Elmas", "laurel": "Defne", "medal": "Madalyon"}
                is_preset = tpl.get("is_preset", False)

                # Ozellik badge'leri
                badges_html = ""
                if has_corner:
                    badges_html += '<span style="background:#dbeafe;color:#2563eb;padding:1px 5px;border-radius:3px;font-size:8px;margin-right:3px;">Köse</span>'
                if has_deco:
                    badges_html += '<span style="background:#fef3c7;color:#fbbf24;padding:1px 5px;border-radius:3px;font-size:8px;margin-right:3px;">Deko</span>'
                if has_sig2:
                    badges_html += '<span style="background:#ede9fe;color:#7c3aed;padding:1px 5px;border-radius:3px;font-size:8px;margin-right:3px;">2 Imza</span>'
                badges_html += f'<span style="background:#ecfdf5;color:#059669;padding:1px 5px;border-radius:3px;font-size:8px;">{orn_labels.get(orn_style, "")}</span>'

                # Mini sertifika gorsel onizleme (HTML mockup)
                inner_border = f"border:2px solid {t_border};" if tpl.get("border_enabled", True) else ""
                corner_dots = ""
                if has_corner:
                    corner_dots = (
                        f'<div style="position:absolute;top:3px;left:3px;width:5px;height:5px;background:{t_border};border-radius:50%;"></div>'
                        f'<div style="position:absolute;top:3px;right:3px;width:5px;height:5px;background:{t_border};border-radius:50%;"></div>'
                        f'<div style="position:absolute;bottom:3px;left:3px;width:5px;height:5px;background:{t_border};border-radius:50%;"></div>'
                        f'<div style="position:absolute;bottom:3px;right:3px;width:5px;height:5px;background:{t_border};border-radius:50%;"></div>'
                    )

                # Tur bazli renk overlay cemberleri
                try:
                    type_colors = json.loads(tpl.get("type_color_overrides", "{}"))
                except (json.JSONDecodeError, TypeError):
                    type_colors = {}
                color_dots = ""
                for tc in list(type_colors.values())[:4]:
                    color_dots += f'<span style="display:inline-block;width:10px;height:10px;background:{tc};border-radius:50%;margin-right:3px;border:1px solid #fff;"></span>'

                card_h = "100px" if t_orient == "landscape" else "130px"
                card_w = "100%"

                st.markdown(f"""
                <div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:12px;overflow:hidden;margin-bottom:10px;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);transition:all 0.2s;">
                    <!-- Mini Preview -->
                    <div style="background:{t_bg};{inner_border}border-radius:8px;margin:10px;height:{card_h};
                    position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;">
                        {corner_dots}
                        <div style="width:14px;height:14px;background:#e2e8f0;border-radius:50%;margin-bottom:4px;"></div>
                        <div style="font-size:6px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;">Kurum Adi</div>
                        <div style="font-size:9px;font-weight:800;color:{t_border};margin:3px 0;letter-spacing:1px;">
                        {onizleme_turu.upper()} SERTİFİKASI</div>
                        <div style="width:40px;height:1px;background:{t_border};margin:2px 0;"></div>
                        <div style="font-size:7px;font-weight:700;color:#0B0F19;">Ornek Isim</div>
                        <div style="font-size:5px;color:#94a3b8;margin-top:2px;">Tarih: 19.02.2026</div>
                    </div>
                    <!-- Info -->
                    <div style="padding:8px 12px 10px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:13px;font-weight:700;color:#94A3B8;">{t_name}</span>
                            <span style="background:{t_border}15;color:{t_border};padding:2px 6px;border-radius:4px;
                            font-size:9px;font-weight:600;">{orient_icon} {orient_badge}</span>
                        </div>
                        <div style="font-size:10px;color:#94a3b8;margin:4px 0;">{t_desc}</div>
                        <div style="display:flex;align-items:center;gap:4px;margin-top:4px;">
                            {color_dots}
                            <span style="font-size:8px;color:#94a3b8;margin-left:4px;">{badges_html}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Butonlar
                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("Önizle", key=f"galeri_prev_{tpl_id}", use_container_width=True):
                        st.session_state["galeri_onizleme_id"] = tpl_id
                with btn2:
                    if is_preset:
                        if st.button("Kopyala", key=f"galeri_dup_{tpl_id}", use_container_width=True):
                            result = store.duplicate_cert_template(tpl_id)
                            if result:
                                st.success(f"'{result['name']}' kopyalandi! Şablon Tasarımcısı'nda duzenleyebilirsiniz.")
                                st.rerun()
                    else:
                        if st.button("Düzenle", key=f"galeri_edit_{tpl_id}", use_container_width=True):
                            st.info(f"'{t_name}' sablonunu duzenlemek icin Şablon Tasarımcısı sekmesine gecin.")

    # --- Onizleme Paneli ---
    onizleme_id = st.session_state.get("galeri_onizleme_id")
    if onizleme_id:
        onizleme_tpl = next((t for t in templates if t.get("id") == onizleme_id), None)
        if onizleme_tpl:
            st.divider()
            styled_section(f"Önizleme: {onizleme_tpl.get('name', '')}", "#8b5cf6")

            prev_c1, prev_c2 = st.columns([2, 1])
            with prev_c1:
                try:
                    preview_bytes = _generate_certificate_from_template(
                        template=onizleme_tpl,
                        kurum_adi=kurum_adi or "Ornek Kurum",
                        logo_path=logo_path,
                        sertifika_turu=onizleme_turu,
                        alici_adi="Ornek Ogrenci",
                        sinif_sube="10/A",
                        verilis_tarihi=datetime.now().strftime("%d.%m.%Y"),
                        verilis_nedeni="Bu sertifika ornek onizleme amaclidir.",
                    )
                    import fitz
                    doc = fitz.open(stream=preview_bytes, filetype="pdf")
                    page = doc[0]
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")
                    doc.close()
                    st.image(img_bytes, use_container_width=True)
                except Exception:
                    st.warning("PDF onizleme olusturulamadi.")

            with prev_c2:
                t_data = onizleme_tpl
                st.markdown(f"**Şablon:** {t_data.get('name', '')}")
                st.markdown(f"**Aciklama:** {t_data.get('description', '-')}")
                st.markdown(f"**Sayfa:** {'Yatay (Landscape)' if t_data.get('page_orientation') == 'landscape' else 'Dikey (Portrait)'}")
                st.markdown(f"**Cerceve:** {'Aktif' if t_data.get('border_enabled') else 'Pasif'}")
                st.markdown(f"**Kose Susleri:** {'Var' if t_data.get('corner_decorations') else 'Yok'}")
                st.markdown(f"**Dekoratif Cizgi:** {'Var' if t_data.get('decorative_lines') else 'Yok'}")
                st.markdown(f"**Imza Alani:** {'Cift' if t_data.get('second_signature_enabled') else 'Tek'}")
                st.markdown(f"**Alt Sus:** {t_data.get('ornament_style', 'classic').title()}")

                # Renk paleti
                try:
                    tc = json.loads(t_data.get("type_color_overrides", "{}"))
                except (json.JSONDecodeError, TypeError):
                    tc = {}
                palette_html = ""
                for tur, renk in tc.items():
                    palette_html += (
                        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">'
                        f'<span style="width:14px;height:14px;background:{renk};border-radius:3px;border:1px solid #334155;"></span>'
                        f'<span style="font-size:10px;color:#94a3b8;">{tur}</span></div>')
                if palette_html:
                    st.markdown(f"**Renk Paleti:**")
                    st.markdown(palette_html, unsafe_allow_html=True)

                st.markdown("")
                if t_data.get("is_preset"):
                    if st.button("Kopyala & Düzenle", key="galeri_prev_dup", type="primary", use_container_width=True):
                        result = store.duplicate_cert_template(onizleme_id)
                        if result:
                            st.success(f"'{result['name']}' kopyalandi!")
                            st.rerun()
                else:
                    st.markdown("""<div style="background:#1e293b;border-radius:8px;padding:8px 12px;font-size:10px;color:#93c5fd;">
                    Bu sablon özel sablondur. Şablon Tasarımcısı sekmesinde duzenleyebilirsiniz.
                    </div>""", unsafe_allow_html=True)

                if st.button("Önizlemeyi Kapat", key="galeri_prev_close", use_container_width=True):
                    st.session_state["galeri_onizleme_id"] = None
                    st.rerun()


def _render_sertifikalar() -> None:
    """Sertifika yonetimi ana fonksiyonu."""
    store = AkademikDataStore()
    profile = load_profile()
    kurum_adi = profile.get("name", "")
    logo_path = profile.get("logo_path", "")

    styled_section("Sertifika Yönetimi", "#8b5cf6")

    # Sertifika tipleri (sabit + custom)
    custom_types = store.get_custom_cert_types()
    all_types = SERTIFIKA_TURLERI + [t for t in custom_types if t not in SERTIFIKA_TURLERI]

    # Şablon listesi
    templates = store.get_cert_templates()
    tpl_names = {t['id']: t.get('name', t['id']) for t in templates}

    sub1, sub2, sub3, sub_galeri, sub4 = st.tabs([
        "🏆 Sertifika Oluştur", "📋 Toplu Sertifika", "📜 Sertifika Geçmişi", "🎨 Şablon Galerisi", "✏️ Şablon Tasarımcısı"
    ])

    # ---- ALT SEKME 1: Tekli Sertifika ----
    with sub1:
        st.markdown("")
        col_form, col_prev = st.columns([1, 1])

        with col_form:
            styled_section("Sertifika Bilgileri", "#2563eb")

            # Grup secimi
            grup = st.radio("Alici Grubu", SERTIFIKA_GRUPLARI, horizontal=True, key="cert_grup_tek")

            # Kisi secimi
            alici_adi = ""
            alici_sinif = ""
            alici_sube = ""
            alici_id = ""

            if grup == "Disardan Katilimci":
                alici_adi = st.text_input("Katilimci Adi Soyadi", key="cert_ext_name")
            else:
                secenekler = _cert_load_grup_data(grup)
                kisi_col, ekle_col = st.columns([4, 1])
                with kisi_col:
                    secim = st.selectbox("Kisi Secin", list(secenekler.keys()), key="cert_kisi_tek")
                with ekle_col:
                    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
                    kisi_ekle_ac = st.button("+ Kisi Ekle", key="cert_kisi_ekle_btn", use_container_width=True)

                # --- Hizli Kisi Ekle Formu ---
                if kisi_ekle_ac:
                    st.session_state["cert_kisi_ekle_open"] = not st.session_state.get("cert_kisi_ekle_open", False)

                if st.session_state.get("cert_kisi_ekle_open", False):
                    with st.expander("Yeni Kisi Ekle", expanded=True):
                        if grup == "Öğrenci":
                            ek_ad = st.text_input("Ad", key="cert_ek_ad")
                            ek_soyad = st.text_input("Soyad", key="cert_ek_soyad")
                            ek_c1, ek_c2, ek_c3 = st.columns(3)
                            with ek_c1:
                                ek_sinif = st.selectbox("Sınıf", SINIF_LISTESI, index=min(7, len(SINIF_LISTESI) - 1), key="cert_ek_sinif")
                            with ek_c2:
                                ek_sube = st.selectbox("Şube", ["A", "B", "C", "D", "E"], key="cert_ek_sube")
                            with ek_c3:
                                ek_numara = st.text_input("Numara", key="cert_ek_numara")
                            if st.button("Öğrenci Kaydet", key="cert_ek_save_ogr", type="primary", use_container_width=True):
                                if ek_ad and ek_soyad:
                                    from models.akademik_takip import Student
                                    yeni = Student(ad=ek_ad, soyad=ek_soyad, sinif=ek_sinif, sube=ek_sube, numara=ek_numara)
                                    store.save_student(yeni)
                                    st.session_state["cert_kisi_ekle_open"] = False
                                    st.success(f"{ek_ad} {ek_soyad} eklendi!")
                                    st.rerun()
                                else:
                                    st.warning("Ad ve Soyad zorunludur.")

                        elif grup == "Çalışan":
                            st.info("Çalışan eklemek için Insan Kaynaklari Yönetimi modulunu kullanin. "
                                    "Eklenen calisanlar otomatik olarak burada gorunecektir.")

                        elif grup == "Veli":
                            st.info("Veli eklemek için once Öğrenci grubundan ogrenci ekleyin, veli bilgisi ogrenci kaydinda tutulur.")
                if secim and secim != "-- Secim yapin --":
                    kisi = secenekler[secim]
                    if grup == "Öğrenci":
                        alici_adi = f'{kisi.get("ad", "")} {kisi.get("soyad", "")}'.strip()
                        alici_sinif = str(kisi.get("sinif", ""))
                        alici_sube = kisi.get("sube", "")
                        alici_id = kisi.get("id", "")
                        # Ogrenci bilgi karti
                        numara = kisi.get("numara", "")
                        tc = kisi.get("tc_kimlik", kisi.get("tc", ""))
                        veli = kisi.get("veli_adi", "")
                        if not veli:
                            veli = f'{kisi.get("baba_adi", "")} {kisi.get("baba_soyadi", "")}'.strip()
                        info_rows = f"<b>Ad Soyad:</b> {alici_adi}"
                        info_rows += f"<br><b>Sınıf/Şube:</b> {alici_sinif}/{alici_sube}"
                        if numara:
                            info_rows += f"<br><b>Numara:</b> {numara}"
                        if tc:
                            info_rows += f"<br><b>TC:</b> {tc}"
                        if veli:
                            info_rows += f"<br><b>Veli:</b> {veli}"
                        st.markdown(
                            f'<div style="background:#1e293b; color:#e2e8f0;border:1px solid #bae6fd;border-radius:10px;'
                            f'padding:12px 16px;margin:8px 0;font-size:0.85rem;color:#0c4a6e;line-height:1.7">'
                            f'{info_rows}</div>', unsafe_allow_html=True)

                    elif grup == "Çalışan":
                        alici_adi = f'{kisi.get("ad", "")} {kisi.get("soyad", "")}'.strip()
                        alici_id = kisi.get("id", "")
                        # Calisan bilgi karti
                        unvan = kisi.get("unvan", "")
                        brans = kisi.get("brans", "")
                        email = kisi.get("email", "")
                        tel = kisi.get("telefon", kisi.get("tel", ""))
                        info_rows = f"<b>Ad Soyad:</b> {alici_adi}"
                        if unvan:
                            info_rows += f"<br><b>Unvan:</b> {unvan}"
                        if brans:
                            info_rows += f"<br><b>Branş:</b> {brans}"
                        if email:
                            info_rows += f"<br><b>E-posta:</b> {email}"
                        if tel:
                            info_rows += f"<br><b>Telefon:</b> {tel}"
                        st.markdown(
                            f'<div style="background:#1e293b;border:1px solid #bbf7d0;border-radius:10px;'
                            f'padding:12px 16px;margin:8px 0;font-size:0.85rem;color:#14532d;line-height:1.7">'
                            f'{info_rows}</div>', unsafe_allow_html=True)

                    elif grup == "Veli":
                        alici_adi = secim.split(" (")[0] if " (" in secim else secim
                        alici_id = kisi.get("id", "")
                        # Veli bilgi karti
                        ogr_ad = f'{kisi.get("ad", "")} {kisi.get("soyad", "")}'.strip()
                        ogr_sinif = str(kisi.get("sinif", ""))
                        ogr_sube = kisi.get("sube", "")
                        veli_tel = kisi.get("veli_telefon", kisi.get("baba_tel", kisi.get("anne_tel", "")))
                        info_rows = f"<b>Veli:</b> {alici_adi}"
                        info_rows += f"<br><b>Öğrenci:</b> {ogr_ad}"
                        if ogr_sinif and ogr_sube:
                            info_rows += f" ({ogr_sinif}/{ogr_sube})"
                        if veli_tel:
                            info_rows += f"<br><b>Telefon:</b> {veli_tel}"
                        st.markdown(
                            f'<div style="background:#fefce8;border:1px solid #fde68a;border-radius:10px;'
                            f'padding:12px 16px;margin:8px 0;font-size:0.85rem;color:#713f12;line-height:1.7">'
                            f'{info_rows}</div>', unsafe_allow_html=True)

            # Sertifika turu
            tur_opts = all_types + ["-- Yeni Ekle --"]
            tur_sec = st.selectbox("Sertifika Turu", tur_opts, key="cert_tur_tek")
            if tur_sec == "-- Yeni Ekle --":
                yeni_tur = st.text_input("Yeni Sertifika Turu Adi", key="cert_yeni_tur")
                if yeni_tur and st.button("Turu Kaydet", key="cert_save_tur"):
                    store.save_custom_cert_type(yeni_tur)
                    st.success(f"'{yeni_tur}' eklendi!")
                    st.rerun()
                tur_sec = yeni_tur if yeni_tur else ""

            # Şablon secimi
            selected_tpl_id = st.selectbox(
                "Şablon", list(tpl_names.keys()),
                format_func=lambda x: tpl_names[x], key="cert_tpl_tek"
            )
            selected_template = store.get_cert_template(selected_tpl_id) or PRESET_CERT_TEMPLATES[0]

            # Tarih ve neden
            tarih = st.date_input("Verilis Tarihi", key="cert_tarih_tek")
            tarih_str = tarih.strftime("%d.%m.%Y") if tarih else ""
            neden = st.text_area("Verilis Nedeni / Açıklama", key="cert_neden_tek", height=80)

            # Sertifika veren
            sertifika_veren = st.selectbox(
                "Sertifikayi Veren", SERTIFIKA_VEREN_SECENEKLERI, key="cert_veren_tek"
            )

            # Butonlar
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                preview_btn = st.button("Onizleme", key="cert_preview_tek", use_container_width=True)
            with btn_col2:
                save_btn = st.button("Oluştur & Kaydet", key="cert_save_tek",
                                     use_container_width=True, type="primary")

        with col_prev:
            styled_section("Onizleme", "#8b5cf6")
            sinif_sube = f"{alici_sinif}/{alici_sube}" if alici_sinif and alici_sube else ""

            if preview_btn or save_btn:
                if not alici_adi:
                    st.warning("Alici adi giriniz.")
                elif not tur_sec:
                    st.warning("Sertifika turu seciniz.")
                else:
                    pdf_bytes = _generate_certificate_from_template(
                        template=selected_template,
                        kurum_adi=kurum_adi, logo_path=logo_path,
                        sertifika_turu=tur_sec, alici_adi=alici_adi,
                        sinif_sube=sinif_sube, verilis_tarihi=tarih_str,
                        verilis_nedeni=neden,
                        sertifika_veren=sertifika_veren,
                    )
                    st.download_button(
                        "PDF Indir", data=pdf_bytes,
                        file_name=f"sertifika_{alici_adi.replace(' ', '_')}.pdf",
                        mime="application/pdf", key="cert_dl_tek"
                    )

                    if save_btn:
                        cert = Certificate(
                            ogrenci_id=alici_id, ogrenci_adi=alici_adi,
                            sinif=alici_sinif, sube=alici_sube,
                            sertifika_turu=tur_sec, verilis_nedeni=neden,
                            verilis_tarihi=tarih_str, aciklama=neden,
                            template_id=selected_tpl_id,
                        )
                        store.save_certificate(cert.to_dict())
                        st.success(f"Sertifika kaydedildi: {alici_adi}")

    # ---- ALT SEKME 2: Toplu Sertifika ----
    with sub2:
        st.markdown("")
        styled_section("Toplu Sertifika Oluştur", "#059669")

        grup_bulk = st.radio("Alici Grubu", SERTIFIKA_GRUPLARI, horizontal=True, key="cert_grup_bulk")

        sinif_filtre = None
        sube_filtre = None
        if grup_bulk in ("Öğrenci", "Veli"):
            sinif_sube_data = get_sinif_sube_listesi()
            fc1, fc2 = st.columns(2)
            with fc1:
                sinif_opts = ["Tümü"] + sinif_sube_data.get("siniflar", [])
                sinif_sel = st.selectbox("Sınıf", sinif_opts, key="cert_bulk_sinif")
                sinif_filtre = sinif_sel if sinif_sel != "Tümü" else None
            with fc2:
                sube_opts = ["Tümü"] + sinif_sube_data.get("subeler", [])
                sube_sel = st.selectbox("Şube", sube_opts, key="cert_bulk_sube")
                sube_filtre = sube_sel if sube_sel != "Tümü" else None

        if grup_bulk == "Disardan Katilimci":
            ext_names = st.text_area("Katilimci Adlarini Girin (her satira bir isim)", key="cert_bulk_ext", height=120)
            kisiler = [{"ad": n.strip(), "id": "", "sinif": "", "sube": ""}
                       for n in ext_names.split("\n") if n.strip()] if ext_names else []
        else:
            kisiler = _cert_load_bulk_list(grup_bulk, sinif_filtre, sube_filtre)

        if kisiler:
            isim_listesi = [k["ad"] for k in kisiler]
            tumunu_sec = st.checkbox("Tümünu Sec", key="cert_bulk_all")
            if tumunu_sec:
                secili = st.multiselect("Kisiler", isim_listesi, default=isim_listesi, key="cert_bulk_sel")
            else:
                secili = st.multiselect("Kisiler", isim_listesi, key="cert_bulk_sel2")

            st.markdown(f"**{len(secili)}** kisi secildi")

            tur_bulk = st.selectbox("Sertifika Turu", all_types, key="cert_tur_bulk")
            bulk_tpl_id = st.selectbox(
                "Şablon", list(tpl_names.keys()),
                format_func=lambda x: tpl_names[x], key="cert_tpl_bulk"
            )
            bulk_template = store.get_cert_template(bulk_tpl_id) or PRESET_CERT_TEMPLATES[0]
            tarih_bulk = st.date_input("Verilis Tarihi", key="cert_tarih_bulk")
            tarih_bulk_str = tarih_bulk.strftime("%d.%m.%Y") if tarih_bulk else ""
            neden_bulk = st.text_area("Verilis Nedeni / Açıklama", key="cert_neden_bulk", height=80)
            veren_bulk = st.selectbox(
                "Sertifikayi Veren", SERTIFIKA_VEREN_SECENEKLERI, key="cert_veren_bulk"
            )

            if st.button("Toplu Sertifika Oluştur", key="cert_bulk_create", type="primary"):
                if not secili:
                    st.warning("En az bir kisi seciniz.")
                else:
                    import zipfile
                    zip_buf = io.BytesIO()
                    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                        progress = st.progress(0)
                        for i, isim in enumerate(secili):
                            kisi_data = next((k for k in kisiler if k["ad"] == isim), {})
                            sinif_s = kisi_data.get("sinif", "")
                            sube_s = kisi_data.get("sube", "")
                            ss = f"{sinif_s}/{sube_s}" if sinif_s and sube_s else ""

                            pdf_data = _generate_certificate_from_template(
                                template=bulk_template,
                                kurum_adi=kurum_adi, logo_path=logo_path,
                                sertifika_turu=tur_bulk, alici_adi=isim,
                                sinif_sube=ss, verilis_tarihi=tarih_bulk_str,
                                verilis_nedeni=neden_bulk,
                                sertifika_veren=veren_bulk,
                            )
                            safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", isim)
                            zf.writestr(f"sertifika_{safe_name}.pdf", pdf_data)

                            cert = Certificate(
                                ogrenci_id=kisi_data.get("id", ""),
                                ogrenci_adi=isim, sinif=sinif_s, sube=sube_s,
                                sertifika_turu=tur_bulk, verilis_nedeni=neden_bulk,
                                verilis_tarihi=tarih_bulk_str, aciklama=neden_bulk,
                                template_id=bulk_tpl_id,
                            )
                            store.save_certificate(cert.to_dict())
                            progress.progress((i + 1) / len(secili))

                    zip_buf.seek(0)
                    st.download_button(
                        f"ZIP Indir ({len(secili)} sertifika)", data=zip_buf.getvalue(),
                        file_name="sertifikalar_toplu.zip", mime="application/zip",
                        key="cert_bulk_dl"
                    )
                    st.success(f"{len(secili)} sertifika oluşturuldu ve kaydedildi!")
        else:
            if grup_bulk != "Disardan Katilimci":
                st.info("Bu grupta kayitli kisi bulunamadı.")

    # ---- ALT SEKME 3: Sertifika Gecmisi ----
    with sub3:
        st.markdown("")
        styled_section("Geçmiş Sertifikalar", "#f59e0b")

        certs = store.get_certificates()

        # Filtreler
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filtre_tur = st.selectbox("Tur Filtresi", ["Tümü"] + all_types, key="cert_hist_tur")
        with fc2:
            filtre_arama = st.text_input("Isim Ara", key="cert_hist_ara")
        with fc3:
            filtre_tarih = st.date_input("Tarih (sonrasi)", value=None, key="cert_hist_tarih")

        if filtre_tur != "Tümü":
            certs = [c for c in certs if c.get("sertifika_turu") == filtre_tur]
        if filtre_arama:
            arama_lower = filtre_arama.lower()
            certs = [c for c in certs if arama_lower in c.get("ogrenci_adi", "").lower()]
        if filtre_tarih:
            tarih_str_f = filtre_tarih.strftime("%d.%m.%Y")
            certs = [c for c in certs if c.get("verilis_tarihi", "") >= tarih_str_f]

        if certs:
            st.markdown(f"**{len(certs)}** sertifika bulundu")
            for idx, cert_item in enumerate(certs):
                with st.expander(f'{cert_item.get("ogrenci_adi", "?")} - {cert_item.get("sertifika_turu", "")} '
                    f'({cert_item.get("verilis_tarihi", "")})', expanded=False
                ):
                    mc1, mc2 = st.columns([2, 1])
                    with mc1:
                        st.markdown(f'**Alici:** {cert_item.get("ogrenci_adi", "")}')
                        ss_txt = ""
                        if cert_item.get("sinif") and cert_item.get("sube"):
                            ss_txt = f' ({cert_item["sinif"]}/{cert_item["sube"]})'
                        if ss_txt:
                            st.markdown(f'**Sınıf/Şube:** {ss_txt}')
                        st.markdown(f'**Tur:** {cert_item.get("sertifika_turu", "")}')
                        st.markdown(f'**Tarih:** {cert_item.get("verilis_tarihi", "")}')
                        if cert_item.get("verilis_nedeni"):
                            st.markdown(f'**Neden:** {cert_item.get("verilis_nedeni", "")}')

                    with mc2:
                        if st.button("PDF Indir", key=f"cert_hist_dl_{idx}"):
                            ss_h = ""
                            if cert_item.get("sinif") and cert_item.get("sube"):
                                ss_h = f'{cert_item["sinif"]}/{cert_item["sube"]}'
                            hist_tpl_id = cert_item.get("template_id", "ctpl_preset_klasik")
                            hist_tpl = store.get_cert_template(hist_tpl_id) or PRESET_CERT_TEMPLATES[0]
                            # Use backward-compat wrapper for preset templates
                            if hist_tpl_id == "ctpl_preset_klasik":
                                pdf_b = _generate_certificate_pdf(
                                    kurum_adi=kurum_adi, logo_path=logo_path,
                                    sertifika_turu=cert_item.get("sertifika_turu", ""),
                                    alici_adi=cert_item.get("ogrenci_adi", ""),
                                    sinif_sube=ss_h,
                                    verilis_tarihi=cert_item.get("verilis_tarihi", ""),
                                    verilis_nedeni=cert_item.get("verilis_nedeni", ""),
                                )
                            else:
                                pdf_b = _generate_certificate_from_template(
                                    template=hist_tpl,
                                    kurum_adi=kurum_adi, logo_path=logo_path,
                                    sertifika_turu=cert_item.get("sertifika_turu", ""),
                                    alici_adi=cert_item.get("ogrenci_adi", ""),
                                    sinif_sube=ss_h,
                                    verilis_tarihi=cert_item.get("verilis_tarihi", ""),
                                    verilis_nedeni=cert_item.get("verilis_nedeni", ""),
                                )
                            st.download_button(
                                "Indir", data=pdf_b,
                                file_name=f'sertifika_{cert_item.get("ogrenci_adi", "").replace(" ", "_")}.pdf',
                                mime="application/pdf",
                                key=f"cert_hist_dlbtn_{idx}"
                            )
                        if confirm_action("Sil", "Bu sertifikayı silmek istediğinize emin misiniz?", key=f"cert_hist_del_{idx}"):
                            store.delete_certificate(cert_item.get("id", ""))
                            st.success("Sertifika silindi!")
                            st.rerun()
        else:
            st.info("Henuz sertifika kaydedilmemiş.")

    # ---- ALT SEKME 4: Şablon Galerisi ----
    with sub_galeri:
        _render_sablon_galerisi(store, templates, kurum_adi, logo_path)

    # ---- ALT SEKME 5: Şablon Tasarımcısı ----
    with sub4:
        st.markdown("")
        styled_section("Şablon Tasarımcısı", "#7c3aed")

        # Şablon secici satiri
        sc1, sc2, sc3, sc4 = st.columns([3, 1, 1, 1])
        with sc1:
            selected_tpl_design = st.selectbox(
                "Şablon Seç", list(tpl_names.keys()),
                format_func=lambda x: tpl_names[x], key="tpl_select"
            )
        with sc2:
            if st.button("Kopyala", key="tpl_dup", use_container_width=True):
                result = store.duplicate_cert_template(selected_tpl_design)
                if result:
                    st.success(f"'{result['name']}' kopyalandi!")
                    st.rerun()
        with sc3:
            if st.button("Yeni Bos", key="tpl_new", use_container_width=True):
                new_tpl = CertificateTemplate(name="Yeni Şablon").to_dict()
                store.save_cert_template(new_tpl)
                st.success("Yeni sablon eklendi!")
                st.rerun()
        with sc4:
            current_tpl = next((t for t in templates if t['id'] == selected_tpl_design), {})
            if current_tpl.get('is_preset'):
                st.button("Sil", disabled=True, key="tpl_del", use_container_width=True,
                           help="Preset sablonlar silinemez")
            else:
                if confirm_action("Sil", "Bu şablonu silmek istediğinize emin misiniz?"):
                    store.delete_cert_template(selected_tpl_design)
                    st.success("Şablon silindi!")
                    st.rerun()

        tpl_data = store.get_cert_template(selected_tpl_design)
        if not tpl_data:
            st.warning("Şablon bulunamadı.")
        else:
            is_preset = tpl_data.get('is_preset', False)
            if is_preset:
                st.info("Preset sablon - degisiklik yapmak için 'Kopyala' ile kopyalayabilirsiniz.")

            col_form, col_preview = st.columns([1, 1])

            with col_form:
                with st.expander("Genel Ayarlar", expanded=True):
                    tpl_name = st.text_input("Şablon Adı", tpl_data.get('name', ''),
                                              disabled=is_preset, key="tpl_name")
                    tpl_desc = st.text_input("Açıklama", tpl_data.get('description', ''),
                                              disabled=is_preset, key="tpl_desc")
                    tpl_orient = st.selectbox("Sayfa Yonu", ["landscape", "portrait"],
                                               index=0 if tpl_data.get('page_orientation') == 'landscape' else 1,
                                               disabled=is_preset, key="tpl_orient")
                    tpl_bg = st.color_picker("Arka Plan Rengi",
                                              tpl_data.get('background_color', '#fefefe'),
                                              disabled=is_preset, key="tpl_bg")

                with st.expander("Cerceve Ayarlari"):
                    tpl_border = st.checkbox("Cerceve Aktif", tpl_data.get('border_enabled', True),
                                              disabled=is_preset, key="tpl_border")
                    tpl_theme = st.color_picker("Tema Rengi (Ana Renk)",
                                                 tpl_data.get('border_color', '#2563eb'),
                                                 disabled=is_preset, key="tpl_theme")
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        tpl_bw_out = st.number_input("Dis Cizgi Kal.", 0.0, 10.0,
                                                      tpl_data.get('border_width_outer', 3.0),
                                                      step=0.5, disabled=is_preset, key="tpl_bwo")
                    with bc2:
                        tpl_bw_in = st.number_input("Ic Cizgi Kal.", 0.0, 10.0,
                                                     tpl_data.get('border_width_inner', 1.0),
                                                     step=0.5, disabled=is_preset, key="tpl_bwi")
                    tpl_corners = st.checkbox("Kose Susleri", tpl_data.get('corner_decorations', True),
                                               disabled=is_preset, key="tpl_corners")
                    tpl_deco = st.checkbox("Dekoratif Cizgiler", tpl_data.get('decorative_lines', True),
                                            disabled=is_preset, key="tpl_deco")

                with st.expander("Logo Ayarlari"):
                    tpl_logo_on = st.checkbox("Logo Göster", tpl_data.get('logo_enabled', True),
                                               disabled=is_preset, key="tpl_logo")
                    lc1, lc2 = st.columns(2)
                    with lc1:
                        tpl_logo_w = st.number_input("Genislik", 20.0, 200.0,
                                                      tpl_data.get('logo_width', 70.0),
                                                      step=5.0, disabled=is_preset, key="tpl_lw")
                    with lc2:
                        tpl_logo_h = st.number_input("Yukseklik", 20.0, 200.0,
                                                      tpl_data.get('logo_height', 70.0),
                                                      step=5.0, disabled=is_preset, key="tpl_lh")

                with st.expander("Başlık Ayarlari"):
                    tpl_title = st.text_input("Özel Başlık Metni (bos = otomatik)",
                                               tpl_data.get('title_text', ''),
                                               disabled=is_preset, key="tpl_title")
                    tpl_title_size = st.slider("Başlık Font Boyutu", 14, 36,
                                                int(tpl_data.get('title_font_size', 24)),
                                                disabled=is_preset, key="tpl_tsz")
                    tpl_title_clr = st.color_picker("Başlık Rengi",
                                                     tpl_data.get('title_color', '') or tpl_data.get('border_color', '#2563eb'),
                                                     disabled=is_preset, key="tpl_tclr")

                with st.expander("Alici & Govde Metni"):
                    tpl_prefix = st.text_input("Üst Metin", tpl_data.get('body_prefix', 'Bu belge'),
                                                disabled=is_preset, key="tpl_prefix")
                    tpl_suffix = st.text_input("Alt Metin", tpl_data.get('body_suffix', 'olarak verilmistir.'),
                                                disabled=is_preset, key="tpl_suffix")
                    tpl_recip_sz = st.slider("Alici Font Boyutu", 14, 32,
                                              int(tpl_data.get('recipient_font_size', 20)),
                                              disabled=is_preset, key="tpl_rsz")
                    tpl_recip_clr = st.color_picker("Alici Rengi",
                                                     tpl_data.get('recipient_color', '#0B0F19'),
                                                     disabled=is_preset, key="tpl_rclr")
                    tpl_date_prefix = st.text_input("Tarih Oneki",
                                                     tpl_data.get('date_prefix', 'Tarih: '),
                                                     disabled=is_preset, key="tpl_dpfx")

                with st.expander("Imza Alani"):
                    tpl_sig_on = st.checkbox("Imza Alani Aktif", tpl_data.get('signature_enabled', True),
                                              disabled=is_preset, key="tpl_sig")
                    tpl_sig_lbl = st.text_input("Imza Etiketi",
                                                 tpl_data.get('signature_label', 'Okul Muduru'),
                                                 disabled=is_preset, key="tpl_siglbl")
                    tpl_sig_pos = st.selectbox("Imza Konumu", ["right", "center", "left"],
                                                index=["right", "center", "left"].index(
                                                    tpl_data.get('signature_position', 'right')),
                                                disabled=is_preset, key="tpl_sigpos")
                    tpl_sig2 = st.checkbox("2. Imza Alani", tpl_data.get('second_signature_enabled', False),
                                            disabled=is_preset, key="tpl_sig2")
                    tpl_sig2_lbl = ""
                    if tpl_sig2:
                        tpl_sig2_lbl = st.text_input("2. Imza Etiketi",
                                                      tpl_data.get('second_signature_label', 'Mudur Yardimcisi'),
                                                      disabled=is_preset, key="tpl_sig2lbl")

                with st.expander("Alt Orta Sus"):
                    tpl_orn_on = st.checkbox("Alt Orta Sus Aktif", tpl_data.get('bottom_ornament', True),
                                              disabled=is_preset, key="tpl_orn")
                    orn_opts = ["classic", "diamond", "laurel", "medal"]
                    orn_labels = {"classic": "Klasik Scroll", "diamond": "Elmas", "laurel": "Defne Yapragi", "medal": "Altin Madalyon"}
                    tpl_orn_style = st.selectbox("Sus Stili", orn_opts,
                                                   index=orn_opts.index(tpl_data.get('ornament_style', 'classic'))
                                                   if tpl_data.get('ornament_style', 'classic') in orn_opts else 0,
                                                   format_func=lambda x: orn_labels.get(x, x),
                                                   disabled=is_preset, key="tpl_ornstyle")
                    tpl_orn_clr = st.color_picker("Sus Rengi",
                                                    tpl_data.get('ornament_color', '') or tpl_data.get('border_color', '#2563eb'),
                                                    disabled=is_preset, key="tpl_ornclr")

                with st.expander("Sertifika Turu Renkleri"):
                    try:
                        existing_overrides = json.loads(tpl_data.get('type_color_overrides', '{}'))
                    except (json.JSONDecodeError, TypeError):
                        existing_overrides = {}
                    type_colors = {}
                    for turu in SERTIFIKA_TURLERI:
                        type_colors[turu] = st.color_picker(
                            f"{turu}", existing_overrides.get(turu, tpl_data.get('border_color', '#2563eb')),
                            disabled=is_preset, key=f"tpl_tc_{turu}"
                        )

                # Kaydet butonu
                if not is_preset:
                    if st.button("Şablonu Kaydet", type="primary", key="tpl_save", use_container_width=True):
                        updated = dict(tpl_data)
                        updated['name'] = tpl_name
                        updated['description'] = tpl_desc
                        updated['page_orientation'] = tpl_orient
                        updated['background_color'] = tpl_bg
                        updated['border_enabled'] = tpl_border
                        updated['border_color'] = tpl_theme
                        updated['border_width_outer'] = tpl_bw_out
                        updated['border_width_inner'] = tpl_bw_in
                        updated['corner_decorations'] = tpl_corners
                        updated['decorative_lines'] = tpl_deco
                        updated['logo_enabled'] = tpl_logo_on
                        updated['logo_width'] = tpl_logo_w
                        updated['logo_height'] = tpl_logo_h
                        updated['title_text'] = tpl_title
                        updated['title_font_size'] = float(tpl_title_size)
                        updated['title_color'] = tpl_title_clr if tpl_title_clr != tpl_theme else ""
                        updated['body_prefix'] = tpl_prefix
                        updated['body_suffix'] = tpl_suffix
                        updated['recipient_font_size'] = float(tpl_recip_sz)
                        updated['recipient_color'] = tpl_recip_clr
                        updated['date_prefix'] = tpl_date_prefix
                        updated['signature_enabled'] = tpl_sig_on
                        updated['signature_label'] = tpl_sig_lbl
                        updated['signature_position'] = tpl_sig_pos
                        updated['second_signature_enabled'] = tpl_sig2
                        updated['second_signature_label'] = tpl_sig2_lbl
                        updated['bottom_ornament'] = tpl_orn_on
                        updated['ornament_style'] = tpl_orn_style
                        updated['ornament_color'] = tpl_orn_clr if tpl_orn_clr != tpl_theme else ""
                        updated['type_color_overrides'] = json.dumps(type_colors)
                        store.save_cert_template(updated)
                        st.success(f"'{tpl_name}' kaydedildi!")
                        st.rerun()

            with col_preview:
                styled_section("Canli Onizleme", "#8b5cf6")
                preview_type = st.selectbox("Onizleme Turu", SERTIFIKA_TURLERI, key="tpl_prev_type")

                preview_bytes = _generate_certificate_from_template(
                    template=tpl_data,
                    kurum_adi=kurum_adi or "Ornek Kurum",
                    logo_path=logo_path,
                    sertifika_turu=preview_type,
                    alici_adi="Ornek Öğrenci",
                    sinif_sube="10/A",
                    verilis_tarihi=datetime.now().strftime("%d.%m.%Y"),
                    verilis_nedeni="Ornek verilis nedeni metni buraya gelecektir.",
                )
                try:
                    import fitz
                    doc = fitz.open(stream=preview_bytes, filetype="pdf")
                    page = doc[0]
                    pix = page.get_pixmap(dpi=120)
                    img_bytes = pix.tobytes("png")
                    st.image(img_bytes, use_container_width=True)
                    doc.close()
                except Exception:
                    st.download_button("PDF Onizleme Indir", data=preview_bytes,
                                       file_name="sablon_onizleme.pdf", mime="application/pdf",
                                       key="tpl_prev_dl")



# ===================== DASHBOARD =====================

def _render_kim_dashboard() -> None:
    """Kurumsal dashboard: KPI kartlari, kategori dagilimi, son mesajlar, kurum bilgileri."""
    profile = load_profile()
    positions = _load_positions()
    staff = load_ik_active_employees()
    messages = _load_messages()
    users = get_all_users()

    # --- Profil doluluk hesabi ---
    prof_fields = ["name", "vision", "mission", "values", "phone", "email", "website", "instagram", "slogan"]
    filled_count = sum(1 for k in prof_fields if profile.get(k))
    doluluk_pct = int(filled_count / len(prof_fields) * 100) if prof_fields else 0

    kurum_adi = profile.get("name", "Belirtilmedi")
    if len(kurum_adi) > 20:
        kurum_adi = kurum_adi[:20] + ".."

    # --- KPI stat kartlari ---
    styled_stat_row([
        ("Kurum Adi", kurum_adi, "#1a237e", "🏫"),
        ("Pozisyon", str(len(positions)), "#0d47a1", "📋"),
        ("Personel", str(len(staff)), "#1b5e20", "👥"),
        ("Mesaj", str(len(messages)), "#4a148c", "💬"),
        ("Kullanıcı", str(len(users)), "#006064", "🔑"),
        ("Profil Doluluk", f"%{doluluk_pct}", "#10b981", "📊"),
    ])
    st.markdown("")

    # --- 2 Kolon: Kategori dagilimi + Son mesajlar ---
    col_left, col_right = st.columns(2)

    with col_left:
        styled_section("Pozisyon Kategori Dağılımı", "#0d47a1")
        cat_label_map = {cid: clabel for cid, clabel, _ in ORG_CATEGORIES}
        cat_color_map = {cid: ccolor for cid, _, ccolor in ORG_CATEGORIES}

        cat_counts: dict[str, int] = {}
        for p in positions:
            cat = p.get("category", "diger")
            label = cat_label_map.get(cat, cat)
            cat_counts[label] = cat_counts.get(label, 0) + 1

        if cat_counts:
            chart_colors = []
            for p_cat_id in cat_counts:
                matched_color = "#616161"
                for cid, clabel, ccolor in ORG_CATEGORIES:
                    if clabel == p_cat_id:
                        matched_color = ccolor
                        break
                chart_colors.append(matched_color)
            svg = ReportStyler.donut_chart_svg(cat_counts, colors=chart_colors, size=175)
            st.markdown(svg, unsafe_allow_html=True)
        else:
            st.info("Henuz pozisyon kaydi bulunmuyor.")

    with col_right:
        styled_section("Son Mesajlar", "#4a148c")
        if messages:
            last_msgs = sorted(messages, key=lambda m: m.get("date", ""), reverse=True)[:5]
            msg_colors = ["#1a237e", "#0d47a1", "#1b5e20", "#bf360c", "#4a148c"]
            for idx, msg in enumerate(last_msgs):
                border_color = msg_colors[idx % len(msg_colors)]
                sender = msg.get("sender", msg.get("from", "Bilinmiyor"))
                subject = msg.get("subject", msg.get("title", "Konu yok"))
                date = msg.get("date", msg.get("created_at", "-"))
                if isinstance(date, str) and len(date) > 10:
                    date = date[:10]
                st.markdown(f"""<div style="border-left:4px solid {border_color};
                    background:#111827;border-radius:0 10px 10px 0;padding:10px 14px;
                    margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,0.04)">
                    <div style="font-weight:700;color:#0B0F19;font-size:0.88rem">{subject}</div>
                    <div style="display:flex;justify-content:space-between;margin-top:4px">
                    <span style="font-size:0.78rem;color:#94a3b8">👤 {sender}</span>
                    <span style="font-size:0.75rem;color:#94a3b8">📅 {date}</span>
                    </div></div>""", unsafe_allow_html=True)
        else:
            st.info("Henuz mesaj bulunmuyor.")

    # --- Kurum bilgileri ozet banner ---
    st.markdown("")
    phone = profile.get("phone", "-")
    email = profile.get("email", "-")
    website = profile.get("website", "-")
    instagram = profile.get("instagram", "-")

    st.markdown(f"""<div style="background:linear-gradient(135deg,#1a237e08 0%,#0d47a108 100%);
        border:1px solid #334155;border-radius:14px;padding:18px 24px;
        box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-top:4px">
        <div style="font-weight:700;color:#1a237e;font-size:0.95rem;margin-bottom:10px">
        🏛️ Kurum İletişim Bilgileri</div>
        <div style="display:flex;flex-wrap:wrap;gap:24px">
        <div style="display:flex;align-items:center;gap:6px">
        <span style="font-size:0.85rem">📞</span>
        <span style="font-size:0.83rem;color:#94a3b8;font-weight:600">{phone}</span></div>
        <div style="display:flex;align-items:center;gap:6px">
        <span style="font-size:0.85rem">📧</span>
        <span style="font-size:0.83rem;color:#94a3b8;font-weight:600">{email}</span></div>
        <div style="display:flex;align-items:center;gap:6px">
        <span style="font-size:0.85rem">🌐</span>
        <span style="font-size:0.83rem;color:#94a3b8;font-weight:600">{website}</span></div>
        <div style="display:flex;align-items:center;gap:6px">
        <span style="font-size:0.85rem">📸</span>
        <span style="font-size:0.83rem;color:#94a3b8;font-weight:600">{instagram}</span></div>
        </div></div>""", unsafe_allow_html=True)


# ===================== ANA RENDER =====================

def render_kim_organizational() -> None:
    _inject_css()
    styled_header("Kurumsal Organizasyon ve İletişim", "Kurum profili, organizasyon şeması, personel ve iletişim yönetimi", "🏛️")

    render_smarti_welcome("kim_organizational")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("kim_organizational_egitim_yili")

    tab_dashboard, tab_profile, tab_org, tab_staff, tab_iletisim, tab_sikayet, tab_sert, tab_swot, tab_anket, tab_vyb, tab_karne, tab_kimlik, tab_faaliyet, tab_crm, tab_hafiza, tab_okr, tab_itibar, tab_senaryo, tab_workflow, tab_smarti = st.tabs([
        "📊 Dashboard", "🏢 Kurum Profili", "🏗️ Organizasyon", "👥 Çalışanlar",
        "📨 İletişim", "📝 Şikayet / Öneri", "🏆 Sertifikalar", "📊 SWOT Analizi",
        "📋 Veli Memnuniyet", "💼 Veli Yetenek Bankası",
        "🏅 Kurumsal Karne", "🪪 Kimlik Kartı", "📑 Faaliyet Raporu",
        "👤 360° CRM", "🧠 Kurum Hafızası", "🎯 OKR Takip",
        "🌡️ İtibar Endeksi", "🔮 Senaryo", "✅ Onay Akışı",
        "🤖 Smarti",
    ])

    # ==================== VELİ YETENEK BANKASI ====================
    with tab_vyb:
        try:
            from views._veli_yetenek_bankasi import render_veli_yetenek_bankasi
            render_veli_yetenek_bankasi()
        except ImportError:
            st.info("Veli Yetenek Bankası modülü yüklü değil.")
        except Exception as _e:
            st.error(f"Veli Yetenek Bankası yüklenemedi: {_e}")

    # ==================== DASHBOARD ====================
    with tab_dashboard:
        _render_kim_dashboard()

    # ==================== KURUM PROFILI ====================
    with tab_profile:
        profile = load_profile()

        # Profil ozet kartlari
        prof_name = profile.get("name", "")
        prof_slogan = profile.get("slogan", "")
        filled = sum(1 for k in ["vision", "mission", "values", "phone", "email",
                                  "website", "instagram"] if profile.get(k))
        styled_stat_row([
            ("Kurum", prof_name or "Belirtilmedi", "#1a237e", "🏫"),
            ("Slogan", prof_slogan[:20] + ".." if len(prof_slogan) > 20 else (prof_slogan or "-"), "#8b5cf6", "💬"),
            ("Doluluk", f"%{int(filled / 7 * 100)}", "#10b981", "📊"),
            ("Son Güncelleme", profile.get("updated_at", "-")[:10] if profile.get("updated_at") else "-", "#f59e0b", "📅"),
        ])
        st.markdown("")

        # Duzenleme modu
        view_mode = st.radio(
            "Mod", ["Görüntüle", "Düzenle"],
            horizontal=True, key="kim01_prof_mode", label_visibility="collapsed"
        )

        if view_mode == "Görüntüle":
            # ---- GORUNTULEME MODU ----
            logo_path = profile.get("logo_path", "")

            # Kurum baslik karti
            logo_html = ""
            if logo_path and os.path.exists(logo_path):
                import base64
                with open(logo_path, "rb") as img_f:
                    b64 = base64.b64encode(img_f.read()).decode()
                ext = os.path.splitext(logo_path)[1].lower().replace(".", "")
                if ext == "jpg":
                    ext = "jpeg"
                logo_html = (f'<img src="data:image/{ext};base64,{b64}" '
                             f'style="width:80px;height:80px;border-radius:14px;'
                             f'object-fit:cover;border:2px solid #e2e8f0" />')

            st.markdown(f"""<div style="background:linear-gradient(135deg,#111827 0%,#e2e8f0 100%);
            border-radius:16px;padding:24px;border:1px solid #334155;margin-bottom:16px;
            display:flex;align-items:center;gap:20px">
            {logo_html or '<div style="width:80px;height:80px;border-radius:14px;background:linear-gradient(135deg,#1e40af,#3b82f6);display:flex;align-items:center;justify-content:center"><span style=font-size:2rem>🏫</span></div>'}
            <div>
            <h3 style="margin:0;color:#0B0F19;font-size:1.4rem;font-weight:800">{prof_name or 'Kurum Adi Girilmedi'}</h3>
            <p style="margin:4px 0 0 0;color:#94a3b8;font-size:0.9rem;font-style:italic">{prof_slogan or ''}</p>
            </div></div>""", unsafe_allow_html=True)

            # Vizyon / Misyon / Degerler
            vc1, vc2, vc3 = st.columns(3)
            with vc1:
                _styled_card("Vizyon", profile.get("vision", ""), "🎯", "#2563eb")
            with vc2:
                _styled_card("Misyon", profile.get("mission", ""), "🚀", "#8b5cf6")
            with vc3:
                _styled_card("Degerler", profile.get("values", ""), "💎", "#10b981")

            # Tarihce / Kurucu / Yonetim
            tc1, tc2 = st.columns(2)
            with tc1:
                _styled_card("Tarihce", profile.get("history", ""), "📜", "#f59e0b")
                _styled_card("Kurucu Mesaji", profile.get("founder_message", ""), "✉️", "#0d9488")
            with tc2:
                _styled_card("Yönetim Kurulu", profile.get("board", ""), "👥", "#1a237e")

                # İletişim ozet karti (using _bk_info_row for structured display)
                contact_rows_html = ""
                if profile.get("phone"):
                    contact_rows_html += _bk_info_row("Telefon", profile['phone'])
                if profile.get("email"):
                    contact_rows_html += _bk_info_row("E-posta", profile['email'])
                if profile.get("website"):
                    contact_rows_html += _bk_info_row("Website", profile['website'])
                if profile.get("address"):
                    contact_rows_html += _bk_info_row("Adres", profile['address'])
                if contact_rows_html:
                    st.markdown(f'<div style="background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;margin-bottom:8px;">{contact_rows_html}</div>', unsafe_allow_html=True)
                contact_lines = []
                if profile.get("phone"):
                    contact_lines.append(f"📞 {profile['phone']}")
                if profile.get("email"):
                    contact_lines.append(f"📧 {profile['email']}")
                if profile.get("website"):
                    contact_lines.append(f"🌐 {profile['website']}")
                if profile.get("address"):
                    contact_lines.append(f"📍 {profile['address']}")
                if profile.get("fax"):
                    contact_lines.append(f"📠 {profile['fax']}")
                if profile.get("vergi_no"):
                    contact_lines.append(f"🧾 {profile['vergi_no']}")
                _styled_card("İletişim", "\n".join(contact_lines), "📋", "#ef4444")

            # Sosyal medya
            socials = []
            for key, icon, label in [
                ("instagram", "📸", "Instagram"), ("facebook", "📘", "Facebook"),
                ("youtube", "🎬", "YouTube"), ("twitter", "🐦", "X/Twitter"),
                ("linkedin", "💼", "LinkedIn"), ("tiktok", "🎵", "TikTok"),
            ]:
                if profile.get(key):
                    socials.append(f"{icon} <b>{label}:</b> {profile[key]}")
            if socials:
                styled_section("Sosyal Medya", "#8b5cf6")
                st.markdown(
                    '<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:12px;'
                    'padding:16px;display:flex;flex-wrap:wrap;gap:16px">'
                    + "".join(f'<span style="font-size:0.85rem;color:#475569">{s}</span>' for s in socials)
                    + '</div>',
                    unsafe_allow_html=True
                )

        else:
            # ---- DUZENLEME MODU ----
            styled_section("Logo ve Kurum Bilgileri", "#1a237e")
            logo_path = profile.get("logo_path", "")
            lc1, lc2 = st.columns([1, 3])
            with lc1:
                logo_file = st.file_uploader("Kurum Logosu", type=["png", "jpg", "jpeg"],
                                              key="kim01_logo_upload")
                if logo_file is not None:
                    from utils.security import validate_upload
                    _ok, _msg = validate_upload(logo_file, allowed_types=["png", "jpg", "jpeg"], max_mb=50)
                    if not _ok:
                        st.error(f"⚠️ {_msg}")
                        logo_file = None
                if logo_file is not None:
                    logo_path = save_profile_logo(logo_file)
                if logo_path and os.path.exists(logo_path):
                    st.image(logo_path, width=100)
            with lc2:
                name = st.text_input("Kurum Adi", value=profile.get("name", ""),
                                      placeholder="Ornek: UZ Koleji", key="kim_organi_m1")
                slogan = st.text_input("Kurum Slogani", value=profile.get("slogan", ""),
                                        placeholder="Ornek: Gelecegi Sekillendiren Egitim", key="kim_organi_m2")

            styled_section("Vizyon, Misyon ve Degerler", "#2563eb")
            vision = st.text_area("Vizyon", value=profile.get("vision", ""), height=80, key="kim_organi_3")

            mission = st.text_area("Misyon", value=profile.get("mission", ""), height=80, key="kim_organi_4")

            values = st.text_area("Degerler", value=profile.get("values", ""), height=80, key="kim_organi_5")


            styled_section("Tarihce ve Yönetim", "#f59e0b")
            history = st.text_area("Tarihce", value=profile.get("history", ""), height=80, key="kim_organi_6")

            founder_message = st.text_area("Kurucu Mesaji",
                                            value=profile.get("founder_message", ""), height=80, key="kim_organi_m3")
            board = st.text_area("Yönetim Kurulu", value=profile.get("board", ""), height=80, key="kim_organi_8")


            styled_section("İletişim Bilgileri", "#ef4444")
            ic1, ic2 = st.columns(2)
            with ic1:
                phone = st.text_input("Telefon", value=profile.get("phone", ""),
                                       placeholder="+90 212 555 00 00", key="kim_organi_m4")
                email = st.text_input("E-posta", value=profile.get("email", ""),
                                       placeholder="info@okul.edu.tr", key="kim_organi_m5")
                website = st.text_input("Web Sitesi", value=profile.get("website", ""),
                                         placeholder="www.okul.edu.tr", key="kim_organi_m6")
            with ic2:
                address = st.text_area("Adres", value=profile.get("address", ""), height=68,
                                        placeholder="Ataturk Cad. No:1, Istanbul", key="kim_organi_m7")
                fax = st.text_input("Faks", value=profile.get("fax", ""),
                                     placeholder="+90 212 555 00 01", key="kim_organi_m8")
                vergi_no = st.text_input("Vergi No / Vergi Dairesi", value=profile.get("vergi_no", ""),
                                          placeholder="Ornek: 1234567890 / Kadikoy VD", key="kim_organi_m9")

            styled_section("Sosyal Medya", "#8b5cf6")
            sc1, sc2 = st.columns(2)
            with sc1:
                instagram = st.text_input("Instagram", value=profile.get("instagram", ""),
                                           placeholder="@okul", key="kim_organi_m10")
                facebook = st.text_input("Facebook", value=profile.get("facebook", ""),
                                          placeholder="facebook.com/okul", key="kim_organi_m11")
                youtube = st.text_input("YouTube", value=profile.get("youtube", ""),
                                         placeholder="youtube.com/@okul", key="kim_organi_m12")
            with sc2:
                twitter = st.text_input("X (Twitter)", value=profile.get("twitter", ""),
                                         placeholder="@okul", key="kim_organi_m13")
                linkedin = st.text_input("LinkedIn", value=profile.get("linkedin", ""),
                                          placeholder="linkedin.com/company/okul", key="kim_organi_m14")
                tiktok = st.text_input("TikTok", value=profile.get("tiktok", ""),
                                        placeholder="@okul", key="kim_organi_m15")

            st.markdown("")
            if st.button("Profili Kaydet", key="kim01_profile_save", type="primary",
                         use_container_width=True):
                payload = {
                    "name": name.strip(), "slogan": slogan.strip(),
                    "vision": vision.strip(), "mission": mission.strip(),
                    "values": values.strip(), "history": history.strip(),
                    "founder_message": founder_message.strip(), "board": board.strip(),
                    "phone": phone.strip(), "email": email.strip(),
                    "website": website.strip(), "address": address.strip(),
                    "fax": fax.strip(), "vergi_no": vergi_no.strip(),
                    "instagram": instagram.strip(),
                    "facebook": facebook.strip(), "youtube": youtube.strip(),
                    "twitter": twitter.strip(), "linkedin": linkedin.strip(),
                    "tiktok": tiktok.strip(), "logo_path": logo_path,
                    "updated_at": datetime.utcnow().isoformat(),
                }
                save_profile(payload)
                st.success("Kurum profili kaydedildi.")
                st.rerun()

    # ==================== ORGANIZASYON YAPISI ====================
    with tab_org:
        positions = _load_positions()
        base_titles = load_base_titles()

        # Dashboard istatistikleri
        if positions:
            _lvls = _compute_levels(positions)
            n_roots = sum(1 for p in positions if not p.get("parent_id"))
            max_depth = max(_lvls.values(), default=0) + 1
            cats_used = len(set(p.get("category", "diger") for p in positions))
            styled_stat_row([
                ("Toplam Pozisyon", str(len(positions)), "#2563eb", "👤"),
                ("Kok Pozisyon", str(n_roots), "#1a237e", "🏢"),
                ("Hiyerarsi Seviyesi", str(max_depth), "#10b981", "📊"),
                ("Kategori", str(cats_used), "#8b5cf6", "🏷️"),
            ])
            st.markdown("")

        sub1, sub2, sub3, sub4, sub5, sub6 = st.tabs([
            "📋 Pozisyon Yönetimi",
            "🏗️ Organizasyon Şeması",
            "📈 KOİ Raporlar",
            "🎯 İnteraktif Şema",
            "🛡️ Yedekleme Planı",
            "⏰ Zaman Makinesi",
        ])

        # ---------- ALT SEKME 1: POZISYON YONETIMI ----------
        with sub1:
            styled_section("Yeni Pozisyon Ekle", "#10b981")

            with st.form("kim01_add_pos_form", clear_on_submit=True):
                # ═══ ADIM 1: Kişi Bilgileri ═══
                st.markdown("**1️⃣ Kişi Bilgileri**")
                p1_c1, p1_c2 = st.columns(2)
                with p1_c1:
                    new_person = st.text_input(
                        "👤 Kişi Adı Soyadı *", key="kim01_pos_person",
                        placeholder="Ornek: Ahmet Yilmaz"
                    )
                with p1_c2:
                    new_dept = st.text_input(
                        "🏢 Birim / Departman (Opsiyonel)", key="kim01_pos_dept",
                        placeholder="Ornek: Akademik Isler"
                    )

                st.markdown("---")
                # ═══ ADIM 2: Ünvan ═══
                st.markdown("**2️⃣ Ünvan / Görev**")
                p2_c1, p2_c2 = st.columns(2)
                with p2_c1:
                    if base_titles:
                        suggest = st.selectbox(
                            "📋 Hazır Ünvan Listesi",
                            ["-- Serbest giriş --"] + base_titles,
                            key="kim01_pos_suggest"
                        )
                    else:
                        suggest = "-- Serbest giriş --"
                with p2_c2:
                    new_title = st.text_input(
                        "✏️ Ünvan / Görev *", key="kim01_pos_title",
                        placeholder="Ornek: Genel Mudur"
                    )

                st.markdown("---")
                # ═══ ADIM 3: Bağlı Olduğu Pozisyon ═══
                st.markdown("**3️⃣ Bağlı Olduğu Pozisyon**")
                parent_opts = ["-- Üst pozisyon yok (kök) --"]
                for p in positions:
                    lbl = p["title"]
                    if p.get("person_name"):
                        lbl += f" ({p['person_name']})"
                    parent_opts.append(lbl)
                new_parent_sel = st.selectbox(
                    "🔗 Bağlı Olduğu Pozisyon", parent_opts, key="kim01_pos_parent"
                )

                st.markdown("---")
                # ═══ ADIM 4: Kategori ═══
                st.markdown("**4️⃣ Kategori**")
                cat_c1, cat_c2 = st.columns([2, 1])
                with cat_c1:
                    new_cat_idx = st.selectbox(
                        "🏷️ Mevcut Kategori Seç", range(len(_CAT_LABELS)),
                        format_func=lambda i: _CAT_LABELS[i], key="kim01_pos_cat"
                    )
                with cat_c2:
                    new_custom_cat = st.text_input(
                        "➕ Yeni Kategori (opsiyonel)", key="kim01_pos_new_cat",
                        placeholder="Ornek: Proje Ekibi"
                    )

                st.markdown("")
                submitted = st.form_submit_button("✅ Pozisyon Ekle", type="primary", use_container_width=True)
                if submitted:
                    final_title = new_title.strip()
                    if not final_title and suggest != "-- Serbest giris --":
                        final_title = suggest
                    if final_title:
                        parent_id = None
                        if new_parent_sel != parent_opts[0]:
                            p_idx = parent_opts.index(new_parent_sel) - 1
                            if 0 <= p_idx < len(positions):
                                parent_id = positions[p_idx]["id"]
                        # Kategori: yeni girilmişse onu kullan, yoksa seçileni
                        if new_custom_cat.strip():
                            cat_id = new_custom_cat.strip().lower().replace(" ", "_").replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("ş", "s").replace("ç", "c").replace("ğ", "g")
                            # Yeni kategoriyi listeye ekle (varsa atlama)
                            if cat_id not in _CAT_IDS:
                                ORG_CATEGORIES.append((cat_id, new_custom_cat.strip(), "#6366f1"))
                                _CAT_IDS.append(cat_id)
                                _CAT_LABELS.append(new_custom_cat.strip())
                                _CAT_MAP[cat_id] = {"label": new_custom_cat.strip(), "color": "#6366f1"}
                            final_cat = cat_id
                        else:
                            final_cat = _CAT_IDS[new_cat_idx]
                        positions.append({
                            "id": _gen_pos_id(), "title": final_title,
                            "person_name": new_person.strip(),
                            "department": new_dept.strip(),
                            "parent_id": parent_id,
                            "category": final_cat,
                            "order": len(positions),
                        })
                        _save_positions(positions)
                        st.success(f"'{final_title}' pozisyonu eklendi.")
                        st.rerun()
                    else:
                        st.error("Unvan alani zorunludur.")

            if positions:
                _pos_key = "_kim_pos_list_open"
                if _pos_key not in st.session_state:
                    st.session_state[_pos_key] = False
                _pos_open = st.session_state[_pos_key]
                _pos_icon = "🔽" if _pos_open else "▶️"
                if st.button(f"{_pos_icon} Mevcut Pozisyonlar ({len(positions)})", key="kim01_pos_toggle",
                             use_container_width=True):
                    st.session_state[_pos_key] = not _pos_open
                    st.rerun()

                if not st.session_state[_pos_key]:
                    pass
                else:
                    pos_lookup = {p["id"]: p for p in positions}

                    for i, pos in enumerate(positions):
                        parent_name = "Kok (ust yok)"
                        if pos.get("parent_id") and pos["parent_id"] in pos_lookup:
                            parent_name = pos_lookup[pos["parent_id"]]["title"]
                        cat = _CAT_MAP.get(pos.get("category", "diger"), _CAT_MAP["diger"])

                        header = pos["title"]
                        if pos.get("person_name"):
                            header += f"  |  {pos['person_name']}"

                        with st.expander(header, expanded=False):
                            ec1, ec2 = st.columns(2)
                            with ec1:
                                ed_title = st.text_input("Unvan", value=pos["title"],
                                                          key=f"kim01_ed_t_{pos['id']}")
                                ed_person = st.text_input("Kisi Adi", value=pos.get("person_name", ""),
                                                           key=f"kim01_ed_p_{pos['id']}")
                                ed_dept = st.text_input("Birim", value=pos.get("department", ""),
                                                         key=f"kim01_ed_d_{pos['id']}")
                            with ec2:
                                cur_cat = pos.get("category", "diger")
                                cur_cat_idx = _CAT_IDS.index(cur_cat) if cur_cat in _CAT_IDS else len(_CAT_IDS) - 1
                                ed_cat = st.selectbox("Kategori", range(len(_CAT_LABELS)),
                                                       index=cur_cat_idx,
                                                       format_func=lambda idx: _CAT_LABELS[idx],
                                                       key=f"kim01_ed_c_{pos['id']}")
                                par_opts = ["-- Ust pozisyon yok --"]
                                cur_par_idx = 0
                                other_positions = [p for p in positions if p["id"] != pos["id"]]
                                for j, p2 in enumerate(other_positions):
                                    lbl2 = p2["title"]
                                    if p2.get("person_name"):
                                        lbl2 += f" ({p2['person_name']})"
                                    par_opts.append(lbl2)
                                    if pos.get("parent_id") == p2["id"]:
                                        cur_par_idx = len(par_opts) - 1
                                ed_parent = st.selectbox("Bagli Pozisyon", par_opts,
                                                          index=cur_par_idx,
                                                          key=f"kim01_ed_pr_{pos['id']}")
                                st.markdown(
                                    f'<div style="margin-top:8px">'
                                    f'<span style="background:{cat["color"]};color:white;'
                                    f'padding:4px 12px;border-radius:8px;font-size:12px;font-weight:600">'
                                    f'{cat["label"]}</span>'
                                    f'<span style="color:#94a3b8;font-size:12px;margin-left:10px">'
                                    f'Bagli: {parent_name}</span></div>',
                                    unsafe_allow_html=True
                                )
                            bc1, bc2, bc3 = st.columns([2, 2, 1])
                            with bc1:
                                if st.button("Güncelle", key=f"kim01_upd_{pos['id']}",
                                             type="primary"):
                                    pos["title"] = ed_title.strip() or pos["title"]
                                    pos["person_name"] = ed_person.strip()
                                    pos["department"] = ed_dept.strip()
                                    pos["category"] = _CAT_IDS[ed_cat]
                                    if ed_parent == par_opts[0]:
                                        pos["parent_id"] = None
                                    else:
                                        p_idx2 = par_opts.index(ed_parent) - 1
                                        if 0 <= p_idx2 < len(other_positions):
                                            pos["parent_id"] = other_positions[p_idx2]["id"]
                                    _save_positions(positions)
                                    st.success("Güncellendi.")
                                    st.rerun()
                            with bc3:
                                if st.button("Sil", key=f"kim01_del_{pos['id']}"):
                                    for p2 in positions:
                                        if p2.get("parent_id") == pos["id"]:
                                            p2["parent_id"] = pos.get("parent_id")
                                    positions = [p2 for p2 in positions if p2["id"] != pos["id"]]
                                    _save_positions(positions)
                                    st.rerun()

                    st.markdown("")
                    tc1, tc2 = st.columns(2)
                    with tc1:
                        if st.button("Tüm Pozisyonlari Sil", key="kim01_del_all"):
                            _save_positions([])
                            st.rerun()
                    with tc2:
                        st.download_button(
                            "Pozisyonlari JSON Indir",
                            data=json.dumps(positions, ensure_ascii=False, indent=2).encode("utf-8"),
                            file_name="pozisyonlar.json", mime="application/json",
                            key="kim01_dl_pos_json"
                        )
                # --- Organizasyon Şeması Oluştur Butonu ---
                st.markdown("")
                if st.button("🏗️ Bu Bilgilere Göre Organizasyon Şeması Oluştur",
                             key="kim01_gen_org_chart", type="primary", use_container_width=True):
                    st.session_state["_kim_org_chart_ready"] = True
                    st.success("Organizasyon şeması oluşturuldu! 'Organizasyon Şeması' sekmesine geçin.")

            else:
                st.markdown("""<div style="background:#111827;border:2px dashed #e2e8f0;
                border-radius:16px;padding:40px;text-align:center;margin:20px 0">
                <div style="font-size:3rem;margin-bottom:12px">🏢</div>
                <div style="font-size:1.1rem;font-weight:600;color:#94a3b8;margin-bottom:6px">
                Henuz pozisyon eklenmedi</div>
                <div style="font-size:0.85rem;color:#94a3b8">
                Yukaridaki formu kullanarak organizasyon yapisini olusturun</div>
                </div>""", unsafe_allow_html=True)

        # ---------- ALT SEKME 2: ORGANIZASYON SEMASI ----------
        with sub2:
            if positions:
                if st.session_state.get("_kim_org_chart_ready"):
                    styled_section("Interaktif Organizasyon Şeması", "#1a237e")

                    # Özet bilgi banner
                    root_count = sum(1 for p in positions if not p.get("parent_id") or p["parent_id"] not in {pp["id"] for pp in positions})
                    cat_counts = {}
                    for p in positions:
                        cat_name = _CAT_MAP.get(p.get("category", "diger"), _CAT_MAP["diger"])["label"]
                        cat_counts[cat_name] = cat_counts.get(cat_name, 0) + 1
                    cat_summary = " • ".join(f"{k}: {v}" for k, v in cat_counts.items())

                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;'
                        f'border-radius:12px;padding:16px 20px;margin-bottom:16px">'
                        f'<div style="display:flex;gap:24px;flex-wrap:wrap;align-items:center">'
                        f'<div style="font-size:0.85rem;color:#94a3b8">'
                        f'📊 <b style="color:#e2e8f0">{len(positions)}</b> Pozisyon &nbsp;|&nbsp; '
                        f'🏛️ <b style="color:#e2e8f0">{root_count}</b> Üst Düzey &nbsp;|&nbsp; '
                        f'📂 {cat_summary}</div></div></div>',
                        unsafe_allow_html=True
                    )

                    dot_str = _build_org_dot(positions)
                    st.graphviz_chart(dot_str, use_container_width=True)

                    # Legenda
                    st.markdown(
                        '<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:12px;'
                        'padding:14px 20px;margin-top:12px;display:flex;flex-wrap:wrap;gap:16px;'
                        'align-items:center">'
                        '<span style="font-weight:700;color:#94a3b8;font-size:0.8rem;margin-right:4px">'
                        'Kategoriler:</span>'
                        + "".join(
                            f'<span style="display:flex;align-items:center;gap:5px">'
                            f'<span style="width:10px;height:10px;border-radius:3px;background:{c[2]}"></span>'
                            f'<span style="font-size:0.75rem;color:#cbd5e1">{c[1]}</span></span>'
                            for c in ORG_CATEGORIES
                        )
                        + '</div>',
                        unsafe_allow_html=True
                    )

                    # Yeniden oluştur butonu
                    st.markdown("")
                    if st.button("🔄 Şemayı Güncelle", key="kim01_refresh_org"):
                        st.rerun()
                else:
                    st.markdown("""<div style="background:#111827;border:2px dashed #3b82f6;
                    border-radius:16px;padding:40px;text-align:center;margin:20px 0">
                    <div style="font-size:3rem;margin-bottom:12px">🏗️</div>
                    <div style="font-size:1.1rem;font-weight:600;color:#93c5fd;margin-bottom:6px">
                    Organizasyon Şeması Henüz Oluşturulmadı</div>
                    <div style="font-size:0.85rem;color:#94a3b8">
                    Pozisyon Yönetimi sekmesinde pozisyonları ekledikten sonra<br>
                    <b style="color:#60a5fa">"Bu Bilgilere Göre Organizasyon Şeması Oluştur"</b>
                    butonuna tıklayın</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div style="background:#111827;border:2px dashed #e2e8f0;
                border-radius:16px;padding:40px;text-align:center;margin:20px 0">
                <div style="font-size:3rem;margin-bottom:12px">📊</div>
                <div style="font-size:1.1rem;font-weight:600;color:#475569">
                Organizasyon semasini goruntulemek için pozisyon ekleyin</div>
                </div>""", unsafe_allow_html=True)

        # ---------- ALT SEKME 3: RAPORLAR ----------
        with sub3:
            if positions:
                styled_section("PDF Organizasyon Şeması", "#059669")
                st.markdown("""<div style="background:#1e293b;border:1px solid #bbf7d0;
                border-radius:12px;padding:14px 18px;margin-bottom:12px;font-size:0.85rem;color:#86efac">
                A4 yatay formatta, renkli kutular ve hiyerarsi cizgileriyle profesyonel PDF olusturur.
                </div>""", unsafe_allow_html=True)

                if st.button("PDF Oluştur ve Indir", key="kim01_gen_pdf", type="primary",
                             use_container_width=True):
                    pdf_data = _generate_org_pdf(positions)
                    if pdf_data:
                        st.download_button(
                            "PDF Indir",
                            data=pdf_data,
                            file_name=f"organizasyon_semasi_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf", key="kim01_dl_pdf"
                        )
                    else:
                        st.error("PDF olusturulamadi. reportlab kutuphanesi bulunamadı.")



            else:
                st.markdown("""<div style="background:#111827;border:2px dashed #e2e8f0;
                border-radius:16px;padding:40px;text-align:center;margin:20px 0">
                <div style="font-size:3rem;margin-bottom:12px">📄</div>
                <div style="font-size:1.1rem;font-weight:600;color:#475569">
                Rapor olusturmak için pozisyon ekleyin</div>
                </div>""", unsafe_allow_html=True)

        # ---------- ALT SEKME 4: INTERAKTIF SEMA ----------
        with sub4:
            try:
                from views._kim_org_zirve import render_interaktif_sema
                render_interaktif_sema(positions)
            except Exception as _e:
                st.error(f"Interaktif sema yuklenemedi: {_e}")

        # ---------- ALT SEKME 5: YEDEKLEME PLANI ----------
        with sub5:
            try:
                from views._kim_org_zirve import render_yedekleme_plani
                render_yedekleme_plani(positions)
            except Exception as _e:
                st.error(f"Yedekleme plani yuklenemedi: {_e}")

        # ---------- ALT SEKME 6: ZAMAN MAKINESI ----------
        with sub6:
            try:
                from views._kim_org_zirve import render_zaman_makinesi
                render_zaman_makinesi(positions)
            except Exception as _e:
                st.error(f"Zaman makinesi yuklenemedi: {_e}")

    # ==================== KURUM CALISANLARI ====================
    with tab_staff:
        # Veri Kaynagi: IK Aktif Calisanlar
        staff = load_ik_active_employees()

        # Bilgi banner
        st.markdown(
            '<div style="background:linear-gradient(135deg,#0d9488 0%,#0f766e 100%);'
            'color:white;padding:12px 20px;border-radius:12px;margin-bottom:16px;'
            'display:flex;align-items:center;gap:10px;font-size:0.9rem">'
            '<span style="font-size:1.3rem">🏢</span>'
            '<span><b>Veri Kaynagi:</b> Insan Kaynaklari Yönetimi &rarr; Kurum Aktif Çalışanları</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        def _ik_cat(s):
            return _ROLE_SCOPE_TO_CAT.get(s.get("role_scope", ""), "diger")

        # Dashboard istatistikleri
        pozisyon_counts: dict[str, int] = {}
        cat_counts: dict[str, int] = {}
        for s in staff:
            cat_key = _ik_cat(s)
            c_lbl = _CAT_MAP.get(cat_key, _CAT_MAP["diger"])["label"]
            cat_counts[c_lbl] = cat_counts.get(c_lbl, 0) + 1
            pn = s.get("position_name", "Belirtilmedi") or "Belirtilmedi"
            pozisyon_counts[pn] = pozisyon_counts.get(pn, 0) + 1
        top_cat = max(cat_counts, key=cat_counts.get) if cat_counts else "-"
        top_poz = max(pozisyon_counts, key=pozisyon_counts.get) if pozisyon_counts else "-"
        styled_stat_row([
            ("Toplam Çalışan", str(len(staff)), "#2563eb", "\U0001f465"),
            ("Pozisyon Cesidi", str(len(pozisyon_counts)), "#8b5cf6", "\U0001f3f7\ufe0f"),
            ("En Kalabalik Pozisyon", top_poz, "#10b981", "\U0001f4ca"),
            ("Kategori Sayısı", str(len(cat_counts)), "#f59e0b", "\U0001f4c1"),
        ])

        # Gauge charts
        if staff:
            total_s = len(staff)
            yonetim_cnt = sum(1 for s in staff if _ik_cat(s) in ("yonetim_kurulu", "ust_yonetim", "okul_yoneticileri"))
            ogretim_cnt = sum(1 for s in staff if _ik_cat(s) in ("ogretim", "akademik"))
            idari_cnt = sum(1 for s in staff if _ik_cat(s) == "idari")
            destek_cnt = sum(1 for s in staff if _ik_cat(s) in ("destek", "diger"))
            _gc1, _gc2, _gc3, _gc4 = st.columns(4)
            def _kim_gauge(val, mx, lbl, clr):
                pct = min(val / mx * 100, 100) if mx > 0 else 0
                arc = 141.37 * pct / 100
                return (f'<div style="background:#0f172a; color:#e2e8f0;border:1px solid {clr}30;border-radius:14px;'
                        f'padding:18px 22px;margin:8px 0;box-shadow:0 2px 10px rgba(0,0,0,0.06);text-align:center">'
                        f'<svg width="130" height="85" viewBox="0 0 110 85">'
                        f'<path d="M 10 55 A 45 45 0 0 1 100 55" fill="none" stroke="#e2e8f0" stroke-width="8" stroke-linecap="round"/>'
                        f'<path d="M 10 55 A 45 45 0 0 1 100 55" fill="none" stroke="{clr}" stroke-width="8" '
                        f'stroke-linecap="round" stroke-dasharray="{arc} 141.37"/>'
                        f'<text x="55" y="50" text-anchor="middle" font-size="18" font-weight="800" fill="#94A3B8">{val}</text>'
                        f'<text x="55" y="66" text-anchor="middle" font-size="8" fill="#64748b" font-weight="600">{lbl}</text>'
                        f'<text x="10" y="75" text-anchor="middle" font-size="6" fill="#94a3b8">0</text>'
                        f'<text x="100" y="75" text-anchor="middle" font-size="6" fill="#94a3b8">{mx}</text>'
                        f'</svg></div>')
            with _gc1:
                st.markdown(_kim_gauge(yonetim_cnt, total_s, "Yönetim", "#1a237e"), unsafe_allow_html=True)
            with _gc2:
                st.markdown(_kim_gauge(ogretim_cnt, total_s, "Öğretim", "#006064"), unsafe_allow_html=True)
            with _gc3:
                st.markdown(_kim_gauge(idari_cnt, total_s, "İdari", "#4a148c"), unsafe_allow_html=True)
            with _gc4:
                st.markdown(_kim_gauge(destek_cnt, total_s, "Destek", "#37474f"), unsafe_allow_html=True)

        st.markdown("")

        if staff:
            styled_section("Çalışan Tablosu", "#1a237e")

            # Tablo verisi olustur
            table_data = []
            for s in staff:
                cat_key = _ik_cat(s)
                cat_info = _CAT_MAP.get(cat_key, _CAT_MAP["diger"])
                table_data.append({
                    "Personel Kodu": s.get("employee_code", ""),
                    "Ad": s.get("ad", ""),
                    "Soyad": s.get("soyad", ""),
                    "Pozisyon": s.get("position_name", ""),
                    "Kategori": cat_info["label"],
                    "Kampus": s.get("kampus", ""),
                    "Kademe": s.get("kademe", ""),
                    "Telefon": s.get("telefon", ""),
                    "E-posta": s.get("email", ""),
                    "Ise Baslama": s.get("ise_baslama_tarihi", "")[:10] if s.get("ise_baslama_tarihi") else "",
                })
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # ---- GRAFIKLER ----
            styled_section("Pozisyona Gore Çalışan Sayısı", "#2563eb")
            poz_sorted = sorted(pozisyon_counts.items(), key=lambda x: x[1])
            fig_bar_poz = go.Figure(go.Bar(
                x=[v for _, v in poz_sorted],
                y=[k for k, _ in poz_sorted],
                orientation='h',
                marker_color=SC_COLORS[0],
                text=[str(v) for _, v in poz_sorted],
                textposition='outside',
            ))
            sc_bar(fig_bar_poz, height=max(280, len(poz_sorted) * 32), horizontal=True)
            st.plotly_chart(fig_bar_poz, use_container_width=True, key="ch_poz_bar", config=SC_CHART_CFG)

            # Kategori + Kampus Donut
            gr1, gr2 = st.columns(2)
            with gr1:
                styled_section("Kategori Dağılımı", "#8b5cf6")
                cat_dist: dict[str, int] = {}
                cat_colors: dict[str, str] = {}
                for s in staff:
                    cat_key = _ik_cat(s)
                    ci = _CAT_MAP.get(cat_key, _CAT_MAP["diger"])
                    cat_dist[ci["label"]] = cat_dist.get(ci["label"], 0) + 1
                    cat_colors[ci["label"]] = ci["color"]
                cat_labels = list(cat_dist.keys())
                cat_values = list(cat_dist.values())
                cat_clrs = [cat_colors.get(l, "#64748b") for l in cat_labels]
                fig_donut_cat = go.Figure(go.Pie(
                    labels=cat_labels, values=cat_values,
                    hole=0.55,
                    marker=dict(colors=cat_clrs, line=dict(color="#fff", width=2)),
                    textinfo='label+value+percent',
                    textposition='outside',
                    pull=[0.03] * len(cat_labels),
                ))
                sc_pie(fig_donut_cat, height=350)
                st.plotly_chart(fig_donut_cat, use_container_width=True, key="ch_cat_donut", config=SC_CHART_CFG)

            with gr2:
                styled_section("Kampüs Dağılımı", "#0d9488")
                kmp_dist: dict[str, int] = {}
                for s in staff:
                    kl = s.get("kampus", "Belirtilmedi") or "Belirtilmedi"
                    kmp_dist[kl] = kmp_dist.get(kl, 0) + 1
                kmp_labels = list(kmp_dist.keys())
                kmp_values = list(kmp_dist.values())
                fig_donut_kmp = go.Figure(go.Pie(
                    labels=kmp_labels, values=kmp_values,
                    hole=0.55,
                    marker=dict(colors=SC_COLORS[:len(kmp_labels)], line=dict(color="#fff", width=2)),
                    textinfo='label+value+percent',
                    textposition='outside',
                    pull=[0.03] * len(kmp_labels),
                ))
                sc_pie(fig_donut_kmp, height=350)
                st.plotly_chart(fig_donut_kmp, use_container_width=True, key="ch_kmp_donut", config=SC_CHART_CFG)

            # Sunburst: Kategori > Pozisyon
            styled_section("Kategori - Pozisyon Sunburst", "#1a237e")
            sb_labels, sb_parents, sb_values, sb_colors = [], [], [], []
            sb_labels.append("Kurum")
            sb_parents.append("")
            sb_values.append(0)
            sb_colors.append("#0B0F19")
            for cat_label, cat_count in cat_dist.items():
                sb_labels.append(cat_label)
                sb_parents.append("Kurum")
                sb_values.append(0)
                sb_colors.append(cat_colors.get(cat_label, "#64748b"))
            cat_poz: dict[str, dict[str, int]] = {}
            for s in staff:
                cat_key = _ik_cat(s)
                ci = _CAT_MAP.get(cat_key, _CAT_MAP["diger"])
                u = s.get("position_name", "Belirtilmedi") or "Belirtilmedi"
                cat_poz.setdefault(ci["label"], {})
                cat_poz[ci["label"]][u] = cat_poz[ci["label"]].get(u, 0) + 1
            for cat_l, pozlar in cat_poz.items():
                for poz_l, cnt in pozlar.items():
                    sb_labels.append(f"{poz_l}")
                    sb_parents.append(cat_l)
                    sb_values.append(cnt)
                    sb_colors.append(cat_colors.get(cat_l, "#64748b"))
            fig_sunburst = go.Figure(go.Sunburst(
                labels=sb_labels, parents=sb_parents, values=sb_values,
                marker=dict(colors=sb_colors),
                branchvalues="total",
                textinfo="label+value",
                insidetextorientation='radial',
            ))
            fig_sunburst.update_layout(
                height=450, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11),
            )
            st.plotly_chart(fig_sunburst, use_container_width=True, key="ch_sunburst")

            # Calisma yili ortalamasi (kategoriye gore)
            styled_section("Ortalama Calisma Suresi (Yil)", "#f59e0b")
            now = datetime.now()
            cat_years: dict[str, list[float]] = {}
            for s in staff:
                if s.get("ise_baslama_tarihi"):
                    try:
                        start = datetime.fromisoformat(s["ise_baslama_tarihi"])
                        years = (now - start).days / 365.25
                        cat_key = _ik_cat(s)
                        ci = _CAT_MAP.get(cat_key, _CAT_MAP["diger"])
                        cat_years.setdefault(ci["label"], []).append(years)
                    except Exception:
                        pass
            if cat_years:
                avg_labels = list(cat_years.keys())
                avg_values = [round(sum(v) / len(v), 1) for v in cat_years.values()]
                fig_bar_years = go.Figure(go.Bar(
                    x=avg_labels, y=avg_values,
                    marker_color=SC_COLORS[0],
                    text=[f"{v} yil" for v in avg_values],
                    textposition='outside',
                ))
                sc_bar(fig_bar_years, height=320)
                st.plotly_chart(fig_bar_years, use_container_width=True, key="ch_years_bar", config=SC_CHART_CFG)
            else:
                st.info("Calisma suresi hesaplamak için ise baslama tarihi girilmeli.")

            # Indir
            st.markdown("")
            dc1, dc2 = st.columns(2)
            with dc1:
                csv_data = df.to_csv(index=False).encode("utf-8-sig")
                st.download_button("CSV Indir", data=csv_data,
                                     file_name=f"kurum_calisanlari_{datetime.now().strftime('%Y%m%d')}.csv",
                                     mime="text/csv", key="kim01_dl_staff_csv")
            with dc2:
                json_data = json.dumps(staff, ensure_ascii=False, indent=2).encode("utf-8")
                st.download_button("JSON Indir", data=json_data,
                                     file_name=f"kurum_calisanlari_{datetime.now().strftime('%Y%m%d')}.json",
                                     mime="application/json", key="kim01_dl_staff_json")
        else:
            st.markdown("""<div style="background:#111827;border:2px dashed #e2e8f0;
            border-radius:16px;padding:40px;text-align:center;margin:20px 0">
            <div style="font-size:3rem;margin-bottom:12px">\U0001f465</div>
            <div style="font-size:1.1rem;font-weight:600;color:#94a3b8;margin-bottom:6px">
            Henuz aktif calisan bulunmuyor</div>
            <div style="font-size:0.85rem;color:#94a3b8">
            Insan Kaynaklari modulunden calisan ekleyin</div>
            </div>""", unsafe_allow_html=True)


    # ==================== ILETISIM ====================
    with tab_iletisim:
        messages = _load_messages()
        all_staff = load_ik_active_employees()
        all_students = load_shared_students()
        profile = load_profile()
        gonderen_ad = profile.get("name", "Kurum")

        # Dashboard
        total_msg = len(messages)
        iletildi_cnt = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("durum") == "iletildi")
        okundu_cnt = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("okundu"))
        cevap_cnt = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("cevap"))
        styled_stat_row([
            ("Toplam Mesaj", str(total_msg), "#2563eb", "📨"),
            ("İletildi", str(iletildi_cnt), "#10b981", "✅"),
            ("Okundu", str(okundu_cnt), "#8b5cf6", "👁️"),
            ("Cevaplandi", str(cevap_cnt), "#f59e0b", "💬"),
        ])
        st.markdown("")

        msg_gelen, msg_giden, msg_yeni_olustur, msg_sub0, msg_sub_sinif, msg_sub1, msg_sub2, msg_sub3, msg_sub4, msg_panel = st.tabs([
            "📥 Gelen Mesaj", "📤 Giden Mesaj", "✉️ Yeni Mesaj Oluştur",
            "💻 Bilgi İşlem", "📋 Sınıf Listeleri",
            "📨 Toplu Mesaj", "📤 Gönderilen", "📈 KOİ Raporlar", "⚙️ Ayarlar",
            "💬 Panel Mesajları",
        ])

        # ---------- GELEN MESAJ ----------
        with msg_gelen:
            _render_gelen_mesaj()

        # ---------- GIDEN MESAJ ----------
        with msg_giden:
            _render_giden_mesaj()

        # ---------- YENI MESAJ OLUSTUR ----------
        with msg_yeni_olustur:
            _render_yeni_mesaj_olustur()

        # ---------- BILGI ISLEM ----------
        with msg_sub0:
            styled_section("Sistem Durumu", "#f59e0b")
            total_msg = len(messages)
            total_staff = len(all_staff)
            total_stu = len(all_students)
            total_ek = sum(len(m.get("ekler", [])) for m in messages)
            sc1, sc2, sc3, sc4 = st.columns(4)
            with sc1:
                st.metric("Toplam Mesaj", total_msg)
            with sc2:
                st.metric("Kayıtli Personel", total_staff)
            with sc3:
                st.metric("Kayıtli Öğrenci", total_stu)
            with sc4:
                st.metric("Dosya Eki", total_ek)

            # ---------- OGRENCI BILGI KARTI ----------
            with st.expander("Öğrenci Bilgi Karti", expanded=False):

                if not all_students:
                    st.info("Henuz kayitli ogrenci bulunmamaktadir. Akademik Takip modulunden ogrenci ekleyin.")
                else:
                    # Arama ve filtreleme
                    bk_c1, bk_c2, bk_c3 = st.columns([2, 1, 1])
                    with bk_c1:
                        bk_arama = st.text_input("Öğrenci Ara (Ad, Soyad veya TC)", key="bk_ogrenci_ara", placeholder="Adi, soyadi veya TC no girin...")
                    with bk_c2:
                        sinif_listesi = sorted(set(str(s.get("sinif", "")) for s in all_students if s.get("sinif")))
                        bk_sinif = st.selectbox("Sınıf Filtrele", ["Tümü"] + sinif_listesi, key="bk_sinif_f")
                    with bk_c3:
                        sube_listesi = sorted(set(s.get("sube", "") for s in all_students if s.get("sube")))
                        bk_sube = st.selectbox("Şube Filtrele", ["Tümü"] + sube_listesi, key="bk_sube_f")

                    # Filtreleme uygula
                    filtered_stu = all_students
                    if bk_arama:
                        q = bk_arama.lower()
                        filtered_stu = [s for s in filtered_stu if
                                        q in s.get("ad", "").lower() or
                                        q in s.get("soyad", "").lower() or
                                        q in s.get("tc_no", "").lower() or
                                        q in f'{s.get("ad", "")} {s.get("soyad", "")}'.lower()]
                    if bk_sinif != "Tümü":
                        filtered_stu = [s for s in filtered_stu if str(s.get("sinif", "")) == bk_sinif]
                    if bk_sube != "Tümü":
                        filtered_stu = [s for s in filtered_stu if s.get("sube", "") == bk_sube]

                    st.caption(f"{len(filtered_stu)} ogrenci listeleniyor")

                    if filtered_stu:
                        # Ogrenci secimi
                        stu_options = {f'{s.get("ad", "")} {s.get("soyad", "")} - {s.get("sinif", "")}/{s.get("sube", "")}': s for s in filtered_stu}
                        secili = st.selectbox("Öğrenci Seçin", list(stu_options.keys()), key="bk_stu_sec")
                        stu = stu_options[secili]
                        stu_id = stu.get("id", "")

                        # Bilgi Karti - Header
                        ad_soyad = f'{stu.get("ad", "")} {stu.get("soyad", "")}'
                        sinif_sube = f'{stu.get("sinif", "")}/{stu.get("sube", "")}'
                        numara = stu.get("numara", "-")
                        durum = stu.get("durum", "aktif")
                        durum_renk = "#22c55e" if durum == "aktif" else "#ef4444" if durum == "pasif" else "#f59e0b"
                        durum_txt = durum.capitalize()

                        st.markdown(
                            f'<div style="background:linear-gradient(135deg,#94A3B8,#334155);border-radius:16px;'
                            f'padding:24px 28px;margin:12px 0 16px 0;color:white">'
                            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">'
                            f'<div>'
                            f'<div style="font-size:1.4rem;font-weight:800;margin-bottom:4px">{ad_soyad}</div>'
                            f'<div style="display:flex;gap:10px;flex-wrap:wrap">'
                            f'<span style="background:rgba(59,130,246,0.3);padding:4px 12px;border-radius:8px;font-size:0.8rem">Sınıf: {sinif_sube}</span>'
                            f'<span style="background:rgba(139,92,246,0.3);padding:4px 12px;border-radius:8px;font-size:0.8rem">No: {numara}</span>'
                            f'<span style="background:{durum_renk};padding:4px 12px;border-radius:8px;font-size:0.8rem;font-weight:600">{durum_txt}</span>'
                            f'</div></div>'
                            f'<div style="text-align:right">'
                            f'<div style="font-size:0.75rem;color:#94a3b8">TC Kimlik No</div>'
                            f'<div style="font-size:1.1rem;font-weight:700;letter-spacing:1px">{stu.get("tc_no", "-") or "-"}</div>'
                            f'</div></div></div>',
                            unsafe_allow_html=True
                        )

                        # Duzenlenebilir Bilgi Karti Formu
                        with st.form(key=f"bk_form_{stu_id}"):
                            # KISISEL BILGILER
                            styled_section("Kisisel Bilgiler", "#3b82f6")
                            kb_r1c1, kb_r1c2, kb_r1c3, kb_r1c4 = st.columns(4)
                            with kb_r1c1:
                                f_tc = st.text_input("TC Kimlik No", value=stu.get("tc_no", ""), key=f"bkf_tc_{stu_id}")
                            with kb_r1c2:
                                f_ad = st.text_input("Ad", value=stu.get("ad", ""), key=f"bkf_ad_{stu_id}")
                            with kb_r1c3:
                                f_soyad = st.text_input("Soyad", value=stu.get("soyad", ""), key=f"bkf_soyad_{stu_id}")
                            with kb_r1c4:
                                cinsiyet_opts = ["", "Erkek", "Kiz"]
                                cin_idx = cinsiyet_opts.index(stu.get("cinsiyet", "")) if stu.get("cinsiyet", "") in cinsiyet_opts else 0
                                f_cinsiyet = st.selectbox("Cinsiyet", cinsiyet_opts, index=cin_idx, key=f"bkf_cin_{stu_id}")

                            kb_r2c1, kb_r2c2, kb_r2c3, kb_r2c4 = st.columns(4)
                            with kb_r2c1:
                                f_dogum_tarihi = st.text_input("Dogum Tarihi", value=stu.get("dogum_tarihi", ""), key=f"bkf_dt_{stu_id}", placeholder="GG.AA.YYYY")
                            with kb_r2c2:
                                f_dogum_yeri = st.text_input("Dogum Yeri", value=stu.get("dogum_yeri", ""), key=f"bkf_dy_{stu_id}")
                            with kb_r2c3:
                                f_uyruk = st.text_input("Uyruk", value=stu.get("uyruk", "T.C."), key=f"bkf_uy_{stu_id}")
                            with kb_r2c4:
                                kan_opts = ["", "A Rh+", "A Rh-", "B Rh+", "B Rh-", "AB Rh+", "AB Rh-", "0 Rh+", "0 Rh-"]
                                kan_idx = kan_opts.index(stu.get("kan_grubu", "")) if stu.get("kan_grubu", "") in kan_opts else 0
                                f_kan = st.selectbox("Kan Grubu", kan_opts, index=kan_idx, key=f"bkf_kan_{stu_id}")

                            kb_r3c1, kb_r3c2, kb_r3c3, kb_r3c4 = st.columns(4)
                            with kb_r3c1:
                                f_sinif = st.number_input("Sınıf", value=int(stu.get("sinif", 5)), min_value=1, max_value=12, key=f"bkf_sinif_{stu_id}")
                            with kb_r3c2:
                                f_sube = st.text_input("Şube", value=stu.get("sube", ""), key=f"bkf_sube_{stu_id}")
                            with kb_r3c3:
                                f_numara = st.text_input("Okul No", value=stu.get("numara", ""), key=f"bkf_no_{stu_id}")
                            with kb_r3c4:
                                durum_opts = ["aktif", "pasif", "mezun"]
                                dur_idx = durum_opts.index(stu.get("durum", "aktif")) if stu.get("durum", "aktif") in durum_opts else 0
                                f_durum = st.selectbox("Durum", durum_opts, index=dur_idx, key=f"bkf_dur_{stu_id}")

                            f_saglik = st.text_input("Saglik Notu / Alerji", value=stu.get("saglik_notu", ""), key=f"bkf_sag_{stu_id}")

                            # ANNE BILGILERI
                            styled_section("Anne Bilgileri", "#8b5cf6")
                            ab_r1c1, ab_r1c2, ab_r1c3 = st.columns(3)
                            with ab_r1c1:
                                f_anne_adi = st.text_input("Anne Adi", value=stu.get("anne_adi", ""), key=f"bkf_aad_{stu_id}")
                            with ab_r1c2:
                                f_anne_soyadi = st.text_input("Anne Soyadi", value=stu.get("anne_soyadi", ""), key=f"bkf_asoy_{stu_id}")
                            with ab_r1c3:
                                f_anne_meslek = st.text_input("Anne Meslek", value=stu.get("anne_meslek", ""), key=f"bkf_ames_{stu_id}")
                            ab_r2c1, ab_r2c2 = st.columns(2)
                            with ab_r2c1:
                                f_anne_tel = st.text_input("Anne Telefon", value=stu.get("anne_telefon", ""), key=f"bkf_atel_{stu_id}")
                            with ab_r2c2:
                                f_anne_email = st.text_input("Anne E-posta", value=stu.get("anne_email", ""), key=f"bkf_amail_{stu_id}")

                            # BABA BILGILERI
                            styled_section("Baba Bilgileri", "#6d28d9")
                            bb_r1c1, bb_r1c2, bb_r1c3 = st.columns(3)
                            with bb_r1c1:
                                f_baba_adi = st.text_input("Baba Adi", value=stu.get("baba_adi", ""), key=f"bkf_bad_{stu_id}")
                            with bb_r1c2:
                                f_baba_soyadi = st.text_input("Baba Soyadi", value=stu.get("baba_soyadi", ""), key=f"bkf_bsoy_{stu_id}")
                            with bb_r1c3:
                                f_baba_meslek = st.text_input("Baba Meslek", value=stu.get("baba_meslek", ""), key=f"bkf_bmes_{stu_id}")
                            bb_r2c1, bb_r2c2 = st.columns(2)
                            with bb_r2c1:
                                f_baba_tel = st.text_input("Baba Telefon", value=stu.get("baba_telefon", ""), key=f"bkf_btel_{stu_id}")
                            with bb_r2c2:
                                f_baba_email = st.text_input("Baba E-posta", value=stu.get("baba_email", ""), key=f"bkf_bmail_{stu_id}")

                            # VELI BILGILERI
                            styled_section("Veli / İletişim Bilgileri", "#f59e0b")
                            vb_r1c1, vb_r1c2, vb_r1c3 = st.columns(3)
                            with vb_r1c1:
                                f_veli_adi = st.text_input("Veli Adi Soyadi", value=stu.get("veli_adi", ""), key=f"bkf_vad_{stu_id}")
                            with vb_r1c2:
                                f_veli_tel = st.text_input("Veli Telefon", value=stu.get("veli_telefon", ""), key=f"bkf_vtel_{stu_id}")
                            with vb_r1c3:
                                f_veli_email = st.text_input("Veli E-posta", value=stu.get("veli_email", ""), key=f"bkf_vmail_{stu_id}")

                            # ILETISIM & ADRES
                            styled_section("İletişim & Adres", "#10b981")
                            ia_r1c1, ia_r1c2 = st.columns(2)
                            with ia_r1c1:
                                f_ogr_tel = st.text_input("Öğrenci Telefon", value=stu.get("ogrenci_telefon", ""), key=f"bkf_otel_{stu_id}")
                            with ia_r1c2:
                                f_ogr_email = st.text_input("Öğrenci E-posta", value=stu.get("ogrenci_email", ""), key=f"bkf_omail_{stu_id}")
                            f_adres = st.text_area("Adres", value=stu.get("adres", ""), key=f"bkf_adres_{stu_id}", height=68)
                            ia_r2c1, ia_r2c2 = st.columns(2)
                            with ia_r2c1:
                                f_ilce = st.text_input("Ilce", value=stu.get("ilce", ""), key=f"bkf_ilce_{stu_id}")
                            with ia_r2c2:
                                f_il = st.text_input("Il", value=stu.get("il", ""), key=f"bkf_il_{stu_id}")

                            # OKUL BILGILERI
                            styled_section("Okul Bilgileri", "#0ea5e9")
                            f_geldigi_okul = st.text_input("Geldigi Okul", value=stu.get("geldigi_okul", ""), key=f"bkf_gokul_{stu_id}")

                            # KAYDET BUTONU
                            bk_submit = st.form_submit_button("Bilgileri Kaydet", type="primary", use_container_width=True)

                        if bk_submit:
                            # Ogrenciyi guncelle
                            stu_path = get_data_path("akademik", "students.json")
                            try:
                                with open(stu_path, "r", encoding="utf-8") as _f:
                                    stu_data = json.load(_f)
                                stu_list = stu_data if isinstance(stu_data, list) else stu_data.get("students", stu_data.get("records", []))

                                for s in stu_list:
                                    if s.get("id") == stu_id:
                                        s["tc_no"] = f_tc
                                        s["ad"] = f_ad
                                        s["soyad"] = f_soyad
                                        s["cinsiyet"] = f_cinsiyet
                                        s["dogum_tarihi"] = f_dogum_tarihi
                                        s["dogum_yeri"] = f_dogum_yeri
                                        s["uyruk"] = f_uyruk
                                        s["kan_grubu"] = f_kan
                                        s["sinif"] = f_sinif
                                        s["sube"] = f_sube
                                        s["numara"] = f_numara
                                        s["durum"] = f_durum
                                        s["saglik_notu"] = f_saglik
                                        s["anne_adi"] = f_anne_adi
                                        s["anne_soyadi"] = f_anne_soyadi
                                        s["anne_telefon"] = f_anne_tel
                                        s["anne_email"] = f_anne_email
                                        s["anne_meslek"] = f_anne_meslek
                                        s["baba_adi"] = f_baba_adi
                                        s["baba_soyadi"] = f_baba_soyadi
                                        s["baba_telefon"] = f_baba_tel
                                        s["baba_email"] = f_baba_email
                                        s["baba_meslek"] = f_baba_meslek
                                        s["veli_adi"] = f_veli_adi
                                        s["veli_telefon"] = f_veli_tel
                                        s["veli_email"] = f_veli_email
                                        s["ogrenci_telefon"] = f_ogr_tel
                                        s["ogrenci_email"] = f_ogr_email
                                        s["adres"] = f_adres
                                        s["il"] = f_il
                                        s["ilce"] = f_ilce
                                        s["geldigi_okul"] = f_geldigi_okul
                                        s["updated_at"] = datetime.now().isoformat()
                                        break

                                if isinstance(stu_data, list):
                                    save_data = stu_list
                                else:
                                    key = "students" if "students" in stu_data else "records"
                                    stu_data[key] = stu_list
                                    save_data = stu_data

                                with open(stu_path, "w", encoding="utf-8") as _f:
                                    json.dump(save_data, _f, ensure_ascii=False, indent=2)
                                st.success(f"{f_ad} {f_soyad} bilgileri basariyla kaydedildi.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Kaydetme hatasi: {e}")
                    else:
                        st.warning("Arama kriterlerine uygun ogrenci bulunamadı.")


        # ---------- SINIF LISTELERI ----------
        with msg_sub_sinif:
            styled_section("Sınıf ve Şube Listeleri", "#1565c0")

            st.markdown(
                '<div style="background:linear-gradient(135deg,#1565c0 0%,#0d47a1 100%);'
                'color:white;padding:12px 20px;border-radius:12px;margin-bottom:16px;'
                'display:flex;align-items:center;gap:10px;font-size:0.9rem">'
                '<span style="font-size:1.3rem">🏫</span>'
                '<span><b>Merkezi Veri Tabani:</b> Tüm modullerdeki ogrenci ve veli verileri bu kaynaktan saglanir</span>'
                '</div>',
                unsafe_allow_html=True,
            )

            if not all_students:
                st.info("Henuz kayitli ogrenci bulunmamaktadir. Asagidaki 'Öğrenci Ekle' veya 'Excel Import' sekmesini kullanin.")

            # Alt sekmeler
            sl_main_tab_kesin, sl_main_tab1, sl_main_tab_pdf, sl_main_tab_atama, sl_main_tab2, sl_main_tab3 = st.tabs([
                "🎓 Kesin Aday", "📋 Listeler", "📄 Sınıf Listeleri",
                "👨‍🏫 Danisman & Yönetim", "➕ Öğrenci Ekle", "📥 Excel/PDF Import"
            ])

            # ---- KESIN ADAY (HI -> Sinif Listesi Transfer) ----
            with sl_main_tab_kesin:
                styled_section("Kesin Kayıt Adaylari", "#15803d")

                st.markdown(
                    '<div style="background:linear-gradient(135deg,#15803d 0%,#16a34a 100%);'
                    'color:white;padding:12px 20px;border-radius:12px;margin-bottom:16px;'
                    'display:flex;align-items:center;gap:10px;font-size:0.9rem">'
                    '<span style="font-size:1.3rem">🎓</span>'
                    '<span><b>Kesin Kayıt Adaylari:</b> Halkla Iliskiler modulunden kesin kayit olarak gelen ogrenciler. '
                    'Sınıf, sube ve okul numarasi atayarak kalici ogrenci kaydina donusturun.</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                # Adaylari yukle
                kesin_adaylar = load_kesin_kayit_adaylari()

                if not kesin_adaylar:
                    st.info(
                        "Henuz aktarilacak kesin kayit adayi bulunmamaktadir. "
                        "Halkla Iliskiler > Kayıt İşlemleri > Kesin Kayıt ekranindan "
                        "kayit tamamlandıginda adaylar otomatik olarak burada gorunecektir."
                    )
                else:
                    # Istatistik
                    styled_stat_row([
                        ("Bekleyen Aday", str(len(kesin_adaylar)), "#15803d", "🎓"),
                        ("Mevcut Öğrenci", str(len(all_students)), "#2563eb", "👨‍🎓"),
                    ])

                    st.markdown("")

                    # Her aday için expander
                    for _ka_idx, _ka_aday in enumerate(kesin_adaylar):
                        _ka_ad = _ka_aday.get("ogrenci_adi", "Bilinmiyor")
                        _ka_sinif_str = _ka_aday.get("kayit_sinifi", "-")
                        _ka_veli = _ka_aday.get("veli_adi", "-")
                        _ka_tarih = _ka_aday.get("kayit_tarihi", "-")

                        with st.expander(f"🎓 {_ka_ad}  |  Kayıt Sınıfı: {_ka_sinif_str}  |  "
                            f"Veli: {_ka_veli}  |  Kayıt: {_ka_tarih}", expanded=False,
                        ):
                            # Bilgi gosterimi
                            _ka_c1, _ka_c2 = st.columns(2)
                            with _ka_c1:
                                st.markdown(f"**Öğrenci Adi:** {_ka_ad}")
                                st.markdown(f"**TC Kimlik:** {_ka_aday.get('ogrenci_tc', '-') or '-'}")
                                st.markdown(f"**Cinsiyet:** {_ka_aday.get('cinsiyet', '-') or '-'}")
                                st.markdown(f"**Dogum Yeri:** {_ka_aday.get('dogum_yeri', '-') or '-'}")
                                st.markdown(f"**Geldigi Okul:** {_ka_aday.get('geldigi_okul', '-') or '-'}")
                            with _ka_c2:
                                st.markdown(f"**Veli Adi:** {_ka_veli}")
                                st.markdown(f"**Veli TC:** {_ka_aday.get('veli_tc', '-') or '-'}")
                                st.markdown(f"**Veli Telefon:** {_ka_aday.get('veli_telefon', '-') or '-'}")
                                st.markdown(f"**Veli Email:** {_ka_aday.get('veli_email', '-') or '-'}")
                                st.markdown(f"**Kayıt Tarihi:** {_ka_tarih}")
                                st.markdown(f"**Egitim Yili:** {_ka_aday.get('egitim_yili', '-') or '-'}")

                            st.markdown("---")
                            st.markdown("##### Sınıf Atama")

                            # Kayit sinifini SINIF_LISTESI indeksine cevir
                            import re as _re
                            _ka_ks = _ka_sinif_str.strip()
                            _ka_default_idx = 7  # varsayilan: "5" (index 7)

                            # Oncelikle direkt eslesme (orn: "Anasınıfı (5 Yaş)")
                            _ka_ks_lower = _ka_ks.lower()
                            if "anasınıfı" in _ka_ks_lower or "anasinifi" in _ka_ks_lower or "anaokul" in _ka_ks_lower:
                                if "4" in _ka_ks:
                                    _ka_default_idx = SINIF_LISTESI.index("Anasınıfı (4 Yaş)") if "Anasınıfı (4 Yaş)" in SINIF_LISTESI else 0
                                elif "5" in _ka_ks:
                                    _ka_default_idx = SINIF_LISTESI.index("Anasınıfı (5 Yaş)") if "Anasınıfı (5 Yaş)" in SINIF_LISTESI else 1
                                elif "hazırlık" in _ka_ks_lower or "hazirlik" in _ka_ks_lower:
                                    _ka_default_idx = SINIF_LISTESI.index("Anasınıfı (Hazırlık)") if "Anasınıfı (Hazırlık)" in SINIF_LISTESI else 2
                                else:
                                    _ka_default_idx = 0
                            else:
                                # Sayisal sinif (orn: "5. Sınıf" -> 5)
                                _sinif_m = _re.search(r"(\d+)\.\s*[Ss]", _ka_ks)
                                _ka_parsed = 0
                                if _sinif_m:
                                    _ka_parsed = int(_sinif_m.group(1))
                                elif _re.search(r"(\d+)", _ka_ks):
                                    _ka_parsed = int(_re.search(r"(\d+)", _ka_ks).group(1))
                                if _ka_parsed > 0:
                                    _ka_str = str(_ka_parsed)
                                    if _ka_str in SINIF_LISTESI:
                                        _ka_default_idx = SINIF_LISTESI.index(_ka_str)

                            _ka_ac1, _ka_ac2, _ka_ac3 = st.columns(3)
                            with _ka_ac1:
                                _ka_sinif_sec = st.selectbox(
                                    "Sınıf *",
                                    SINIF_LISTESI,
                                    index=_ka_default_idx,
                                    key=f"ka_sinif_{_ka_idx}",
                                )
                            with _ka_ac2:
                                _ka_sube_sec = st.selectbox(
                                    "Şube *",
                                    ["A", "B", "C", "D", "E"],
                                    key=f"ka_sube_{_ka_idx}",
                                )
                            with _ka_ac3:
                                # Otomatik numara onerisi
                                _mevcut_numaralar = [
                                    s.get("numara", "")
                                    for s in all_students
                                    if s.get("sinif") == _ka_sinif_sec and s.get("sube") == _ka_sube_sec
                                ]
                                _max_no = 0
                                for _n in _mevcut_numaralar:
                                    try:
                                        _max_no = max(_max_no, int(_n))
                                    except (ValueError, TypeError):
                                        pass
                                _suggested = str(_max_no + 1)

                                _ka_numara = st.text_input(
                                    "Okul No *",
                                    value=_suggested,
                                    key=f"ka_numara_{_ka_idx}",
                                )

                            # Kaydet butonu
                            if st.button(
                                f"✅ Kaydet - {_ka_ad}",
                                type="primary",
                                key=f"ka_kaydet_{_ka_idx}",
                                use_container_width=True,
                            ):
                                if not _ka_numara.strip():
                                    st.error("Okul numarasi zorunludur.")
                                else:
                                    # Tekrar kontrolu
                                    _tekrar = [
                                        s for s in all_students
                                        if s.get("sinif") == _ka_sinif_sec
                                        and s.get("sube") == _ka_sube_sec
                                        and str(s.get("numara", "")) == _ka_numara.strip()
                                    ]
                                    if _tekrar:
                                        st.error(
                                            f"{_ka_sinif_sec}/{_ka_sube_sec} sinifinda "
                                            f"{_ka_numara} numarali ogrenci zaten kayitli."
                                        )
                                    else:
                                        import uuid as _uuid

                                        # Ad/soyad ayir
                                        _name_parts = _ka_ad.strip().rsplit(" ", 1)
                                        _ad = _name_parts[0] if len(_name_parts) > 1 else _ka_ad
                                        _soyad = _name_parts[-1] if len(_name_parts) > 1 else ""

                                        # Cinsiyet normalize
                                        _cin_raw = _ka_aday.get("cinsiyet", "")
                                        _cinsiyet = ""
                                        if _cin_raw.lower() in ("kiz", "kız"):
                                            _cinsiyet = "kiz"
                                        elif _cin_raw.lower() == "erkek":
                                            _cinsiyet = "erkek"

                                        _yeni_ogr = {
                                            "id": f"stu_{_uuid.uuid4().hex[:8]}",
                                            "tc_no": _ka_aday.get("ogrenci_tc", ""),
                                            "ad": _ad,
                                            "soyad": _soyad,
                                            "sinif": _ka_sinif_sec,
                                            "sube": _ka_sube_sec,
                                            "numara": _ka_numara.strip(),
                                            "cinsiyet": _cinsiyet,
                                            "dogum_tarihi": "",
                                            "dogum_yeri": _ka_aday.get("dogum_yeri", ""),
                                            "uyruk": "T.C.",
                                            "anne_adi": "", "anne_soyadi": "",
                                            "anne_telefon": "", "anne_email": "",
                                            "anne_meslek": "",
                                            "baba_adi": "", "baba_soyadi": "",
                                            "baba_telefon": "", "baba_email": "",
                                            "baba_meslek": "",
                                            "veli_adi": _ka_aday.get("veli_adi", ""),
                                            "veli_cinsiyet": "",
                                            "veli_telefon": _ka_aday.get("veli_telefon", ""),
                                            "veli_email": _ka_aday.get("veli_email", ""),
                                            "adres": _ka_aday.get("adres", ""),
                                            "il": "", "ilce": "",
                                            "ogrenci_telefon": "",
                                            "ogrenci_email": "",
                                            "geldigi_okul": _ka_aday.get("geldigi_okul", ""),
                                            "kan_grubu": "", "saglik_notu": "",
                                            "durum": "aktif",
                                            "kaynak": "kesin_kayit",
                                            "sozlesme_ref": _ka_aday.get("sozlesme_ref", ""),
                                            "egitim_yili": _ka_aday.get("egitim_yili", ""),
                                            "created_at": datetime.now().isoformat(),
                                            "updated_at": datetime.now().isoformat(),
                                        }

                                        # students.json'a kaydet
                                        _stu_path = get_data_path("akademik", "students.json")
                                        os.makedirs(os.path.dirname(_stu_path), exist_ok=True)
                                        try:
                                            with open(_stu_path, "r", encoding="utf-8") as _f:
                                                _stu_data = json.load(_f)
                                            if not isinstance(_stu_data, list):
                                                _stu_data = _stu_data.get("students", _stu_data.get("records", []))
                                        except Exception:
                                            _stu_data = []

                                        _stu_data.append(_yeni_ogr)
                                        with open(_stu_path, "w", encoding="utf-8") as _f:
                                            json.dump(_stu_data, _f, ensure_ascii=False, indent=2)

                                        # Sozlesmeyi aktarildi olarak isaretle
                                        mark_kesin_kayit_transferred(_ka_aday.get("sozlesme_ref", ""))

                                        st.success(
                                            f"✅ {_ad} {_soyad} basariyla {_ka_sinif_sec}/{_ka_sube_sec} "
                                            f"sinifina {_ka_numara} numarasi ile kaydedildi!"
                                        )
                                        st.rerun()

            # ---- SINIF LISTESI AL (PDF) ----
            with sl_main_tab_pdf:
                styled_section("Sınıf Listeleri (PDF)", "#7c3aed")
                from utils.shared_data import render_sinif_listesi_al_ui
                render_sinif_listesi_al_ui(key_prefix="koi")

            # ---- OGRENCI EKLE ----
            with sl_main_tab2:
                styled_section("Yeni Öğrenci Ekle", "#10b981")
                st.info("Buradan eklenen ogrenciler tum SmartCampus AI modullerinde "
                       "(Akademik Takip, Olcme Değerlendirme, Rehberlik, vb.) otomatik olarak kullanilir.")
                with st.form("koi_ogr_ekle_form"):
                    oe_c1, oe_c2 = st.columns(2)
                    with oe_c1:
                        oe_ad = st.text_input("Ad *", key="koi_oe_ad")
                        oe_sinif = st.selectbox("Sınıf *", SINIF_LISTESI, index=min(7, len(SINIF_LISTESI) - 1), key="koi_oe_sinif")
                        oe_numara = st.text_input("Okul No *", key="koi_oe_numara")
                        oe_veli_adi = st.text_input("Veli Adi", key="koi_oe_veli")
                        oe_veli_tel = st.text_input("Veli Telefon", key="koi_oe_veli_tel")
                    with oe_c2:
                        oe_soyad = st.text_input("Soyad *", key="koi_oe_soyad")
                        oe_sube = st.selectbox("Şube *", ["A", "B", "C", "D", "E"], key="koi_oe_sube")
                        oe_tc = st.text_input("TC Kimlik No", key="koi_oe_tc")
                        oe_veli_cinsiyet = st.selectbox("Veli Cinsiyet", ["", "Erkek", "Kadin"],
                                                         format_func=lambda x: x or "Seciniz", key="koi_oe_vc")
                        oe_veli_email = st.text_input("Veli E-posta", key="koi_oe_vemail")

                    if st.form_submit_button("Öğrenci Ekle", type="primary"):
                        if oe_ad and oe_soyad and oe_numara:
                            # Ayni numara kontrolu
                            tekrar = [s for s in all_students
                                      if s.get("sinif") == oe_sinif and s.get("sube") == oe_sube
                                      and s.get("numara") == oe_numara]
                            if tekrar:
                                st.error(f"{oe_sinif}/{oe_sube} sinifinda {oe_numara} numarali ogrenci zaten kayitli.")
                            else:
                                import uuid as _uuid
                                yeni_ogr = {
                                    "id": f"stu_{_uuid.uuid4().hex[:8]}",
                                    "tc_no": oe_tc, "ad": oe_ad, "soyad": oe_soyad,
                                    "sinif": oe_sinif, "sube": oe_sube, "numara": oe_numara,
                                    "cinsiyet": "", "dogum_tarihi": "", "dogum_yeri": "",
                                    "uyruk": "T.C.", "anne_adi": "", "anne_soyadi": "",
                                    "anne_telefon": "", "anne_email": "", "anne_meslek": "",
                                    "baba_adi": "", "baba_soyadi": "", "baba_telefon": "",
                                    "baba_email": "", "baba_meslek": "",
                                    "veli_adi": oe_veli_adi, "veli_cinsiyet": oe_veli_cinsiyet,
                                    "veli_telefon": oe_veli_tel, "veli_email": oe_veli_email,
                                    "adres": "", "il": "", "ilce": "",
                                    "ogrenci_telefon": "", "ogrenci_email": "",
                                    "geldigi_okul": "", "kan_grubu": "", "saglik_notu": "",
                                    "durum": "aktif",
                                    "created_at": datetime.now().isoformat(),
                                    "updated_at": datetime.now().isoformat(),
                                }
                                # Merkezi dosyaya ekle
                                _stu_path = get_data_path("akademik", "students.json")
                                os.makedirs(os.path.dirname(_stu_path), exist_ok=True)
                                try:
                                    with open(_stu_path, "r", encoding="utf-8") as _f:
                                        _stu_data = json.load(_f)
                                    if not isinstance(_stu_data, list):
                                        _stu_data = _stu_data.get("students", _stu_data.get("records", []))
                                except Exception:
                                    _stu_data = []
                                _stu_data.append(yeni_ogr)
                                with open(_stu_path, "w", encoding="utf-8") as _f:
                                    json.dump(_stu_data, _f, ensure_ascii=False, indent=2)
                                st.success(f"{oe_ad} {oe_soyad} ({oe_sinif}/{oe_sube}) basariyla eklendi! "
                                           "Tüm modullere otomatik yansiyacaktir.")
                                st.rerun()
                        else:
                            st.error("Ad, Soyad ve Okul No alanlari zorunludur.")

            # ---- DANISMAN & YONETIM ATAMASI ----
            with sl_main_tab_atama:
                styled_section("Danisman Öğretmen & Yönetim Atamasi", "#0d47a1")

                st.markdown(
                    '<div style="background:linear-gradient(135deg,#0d47a1 0%,#1565c0 100%);'
                    'color:white;padding:12px 20px;border-radius:12px;margin-bottom:16px;'
                    'display:flex;align-items:center;gap:10px;font-size:0.9rem">'
                    '<span style="font-size:1.3rem">👨‍🏫</span>'
                    '<span><b>Danisman & Yönetim:</b> Her sinif/sube için danisman ogretmen, '
                    'mudur yardimcisi ve okul muduru atamasi yapin. '
                    'Bu bilgiler PDF sinif listelerinde otomatik gorunur.</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                # Veri dosyasi yukle/olustur
                _atama_path = get_data_path("akademik", "sinif_yonetim.json")
                os.makedirs(os.path.dirname(_atama_path), exist_ok=True)
                try:
                    with open(_atama_path, "r", encoding="utf-8") as _af:
                        _atama_data = json.load(_af)
                    if not isinstance(_atama_data, dict):
                        _atama_data = {}
                except Exception:
                    _atama_data = {}

                # IK'dan ogretmen ve yonetici listesi
                _ik_employees = load_ik_active_employees()
                _ogretmenler = [
                    e for e in _ik_employees
                    if e.get("role_scope") == "TEACHER"
                ]
                _yoneticiler = [
                    e for e in _ik_employees
                    if e.get("role_scope") in ("MANAGEMENT", "ADMIN")
                ]
                _tum_personel = _ik_employees

                _ogr_adlar = ["-- Secim yapin --"] + sorted([
                    f"{e.get('ad', '')} {e.get('soyad', '')} - {e.get('position_name', '')}".strip()
                    for e in _ogretmenler
                    if f"{e.get('ad', '')} {e.get('soyad', '')}".strip()
                ])
                _yon_adlar = ["-- Secim yapin --"] + sorted([
                    f"{e.get('ad', '')} {e.get('soyad', '')} - {e.get('position_name', '')}".strip()
                    for e in _tum_personel
                    if f"{e.get('ad', '')} {e.get('soyad', '')}".strip()
                ])

                # ==================== OKUL MUDURU & MUDUR YARDIMCISI ====================
                st.markdown("#### 🏫 Okul Yönetimi")

                _ym_c1, _ym_c2 = st.columns(2)
                with _ym_c1:
                    _mevcut_mudur = _atama_data.get("okul_muduru", "-- Secim yapin --")
                    _mudur_idx = 0
                    if _mevcut_mudur in _yon_adlar:
                        _mudur_idx = _yon_adlar.index(_mevcut_mudur)
                    _okul_muduru = st.selectbox(
                        "Okul Muduru",
                        _yon_adlar,
                        index=_mudur_idx,
                        key="atama_okul_muduru",
                    )
                with _ym_c2:
                    _mevcut_my = _atama_data.get("mudur_yardimcisi", "-- Secim yapin --")
                    _my_idx = 0
                    if _mevcut_my in _yon_adlar:
                        _my_idx = _yon_adlar.index(_mevcut_my)
                    _mudur_yardimcisi = st.selectbox(
                        "Mudur Yardimcisi",
                        _yon_adlar,
                        index=_my_idx,
                        key="atama_mudur_yardimcisi",
                    )

                # Kaydet butonu (yonetim)
                if st.button("💾 Yönetim Bilgilerini Kaydet", key="atama_yon_kaydet", type="primary"):
                    _atama_data["okul_muduru"] = _okul_muduru if _okul_muduru != "-- Secim yapin --" else ""
                    _atama_data["mudur_yardimcisi"] = _mudur_yardimcisi if _mudur_yardimcisi != "-- Secim yapin --" else ""
                    with open(_atama_path, "w", encoding="utf-8") as _af:
                        json.dump(_atama_data, _af, ensure_ascii=False, indent=2)
                    st.success("✅ Okul yonetim bilgileri kaydedildi!")
                    st.rerun()

                st.markdown("---")

                # ==================== DANISMAN OGRETMEN ATAMASI ====================
                st.markdown("#### 👨‍🏫 Danisman Öğretmen Atamasi")

                if not all_students:
                    st.info("Henuz kayitli ogrenci bulunmamaktadir.")
                else:
                    # Mevcut sinif/sube kombinasyonlari
                    _sinif_sube_set = sorted(set(
                        f"{s.get('sinif', '')}/{s.get('sube', '')}"
                        for s in all_students
                        if s.get("sinif") and s.get("sube")
                    ), key=lambda x: (
                        int(x.split("/")[0]) if x.split("/")[0].isdigit() else 0,
                        x.split("/")[1] if "/" in x else ""
                    ))

                    _danismanlar = _atama_data.get("danisman_ogretmenler", {})
                    _degisti = False

                    # Her sinif/sube için atama
                    for _ss in _sinif_sube_set:
                        _mevcut = _danismanlar.get(_ss, "-- Secim yapin --")
                        _dn_idx = 0
                        if _mevcut in _ogr_adlar:
                            _dn_idx = _ogr_adlar.index(_mevcut)
                        _ss_key = _ss.replace("/", "_")

                        _dc1, _dc2 = st.columns([1, 3])
                        with _dc1:
                            st.markdown(f"**{_ss}**")
                        with _dc2:
                            _secilen = st.selectbox(
                                f"Danisman - {_ss}",
                                _ogr_adlar,
                                index=_dn_idx,
                                key=f"atama_dan_{_ss_key}",
                                label_visibility="collapsed",
                            )
                            if _secilen != _mevcut:
                                _danismanlar[_ss] = _secilen if _secilen != "-- Secim yapin --" else ""
                                _degisti = True

                    if st.button("💾 Danisman Öğretmenleri Kaydet", key="atama_dan_kaydet", type="primary", use_container_width=True):
                        # Mevcut danisman secimlerini oku
                        for _ss in _sinif_sube_set:
                            _ss_key = _ss.replace("/", "_")
                            _val = st.session_state.get(f"atama_dan_{_ss_key}", "-- Secim yapin --")
                            _danismanlar[_ss] = _val if _val != "-- Secim yapin --" else ""
                        _atama_data["danisman_ogretmenler"] = _danismanlar
                        with open(_atama_path, "w", encoding="utf-8") as _af:
                            json.dump(_atama_data, _af, ensure_ascii=False, indent=2)
                        st.success("✅ Danisman ogretmen atamalari kaydedildi!")
                        st.rerun()

                    # Mevcut atamalarin ozeti
                    _atanmis = {k: v for k, v in _danismanlar.items() if v and v != "-- Secim yapin --"}
                    if _atanmis:
                        st.markdown("---")
                        st.markdown("##### Mevcut Atamalar")
                        _atama_rows = []
                        for _ak, _av in sorted(_atanmis.items()):
                            _parts = _av.split(" - ", 1)
                            _atama_rows.append({
                                "Sınıf/Şube": _ak,
                                "Danisman Öğretmen": _parts[0] if _parts else _av,
                                "Branş": _parts[1] if len(_parts) > 1 else "",
                            })
                        st.dataframe(pd.DataFrame(_atama_rows), use_container_width=True, hide_index=True)

            # ---- EXCEL / PDF IMPORT ----
            with sl_main_tab3:
                styled_section("Excel / PDF ile Toplu Öğrenci Import", "#2563eb")

                st.markdown(
                    '<div style="background:linear-gradient(135deg,#1e40af 0%,#2563eb 100%);'
                    'color:white;padding:12px 20px;border-radius:12px;margin-bottom:16px;'
                    'display:flex;align-items:center;gap:10px;font-size:0.9rem">'
                    '<span style="font-size:1.3rem">📥</span>'
                    '<span><b>Toplu Import:</b> Excel, CSV veya PDF dosyanizdan öğrenci ve veli bilgilerini '
                    'sisteme toplu olarak ekleyin. Eklenen veriler tüm modüllerde otomatik kullanılır.</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                st.info(
                    "**Excel/CSV** dosyaniz su sütunlari icermelidir:\n\n"
                    "**Zorunlu:** `ad`, `soyad`, `sinif`, `sube`, `numara`\n\n"
                    "**Opsiyonel:** `tc_no`, `cinsiyet`, `veli_adi`, `veli_telefon`, `veli_email`, "
                    "`anne_adi`, `anne_telefon`, `baba_adi`, `baba_telefon`"
                )

                # Ornek sablon indirme
                _ogr_sablon_cols = ["ad", "soyad", "sinif", "sube", "numara", "tc_no",
                                    "cinsiyet", "veli_adi", "veli_telefon", "veli_email"]
                _ogr_sablon_df = pd.DataFrame(columns=_ogr_sablon_cols)
                _ogr_sablon_df.loc[0] = ["Ali", "Yilmaz", "9", "A", "101", "12345678901",
                                          "Erkek", "Mehmet Yilmaz", "05321234567", "mehmet@email.com"]
                _ogr_sablon_csv = _ogr_sablon_df.to_csv(index=False).encode("utf-8")
                st.download_button("📄 Örnek Şablon İndir (CSV)", _ogr_sablon_csv,
                                   "ogrenci_import_sablon.csv", "text/csv", key="koi_imp_sablon")

                st.markdown("")

                koi_imp = st.file_uploader(
                    "Excel / CSV / PDF Dosyasi Yükle",
                    type=["xlsx", "xls", "csv", "pdf"],
                    key="koi_sl_import",
                )

                if koi_imp:
                    from utils.security import validate_upload
                    _ok, _msg = validate_upload(koi_imp, allowed_types=["xlsx", "xls", "csv", "pdf"], max_mb=100)
                    if not _ok:
                        st.error(f"⚠️ {_msg}")
                        koi_imp = None
                if koi_imp:
                    imp_df = None
                    _koi_imp_error = None

                    try:
                        if koi_imp.name.lower().endswith(".csv"):
                            imp_df = pd.read_csv(koi_imp)
                        elif koi_imp.name.lower().endswith((".xlsx", ".xls")):
                            imp_df = pd.read_excel(koi_imp)
                        elif koi_imp.name.lower().endswith(".pdf"):
                            try:
                                import tabula
                                _tables = tabula.read_pdf(koi_imp, pages="all", multiple_tables=True)
                                if _tables:
                                    imp_df = pd.concat(_tables, ignore_index=True)
                                else:
                                    _koi_imp_error = "PDF dosyasinda tablo bulunamadi."
                            except ImportError:
                                try:
                                    import pdfplumber
                                    _pages_data = []
                                    koi_imp.seek(0)
                                    with pdfplumber.open(koi_imp) as _pdf:
                                        for _page in _pdf.pages:
                                            _tbl = _page.extract_table()
                                            if _tbl and len(_tbl) > 1:
                                                _hdr = _tbl[0]
                                                for _row in _tbl[1:]:
                                                    _pages_data.append(dict(zip(_hdr, _row)))
                                    if _pages_data:
                                        imp_df = pd.DataFrame(_pages_data)
                                    else:
                                        _koi_imp_error = "PDF dosyasinda tablo bulunamadi."
                                except ImportError:
                                    _koi_imp_error = ("PDF import icin `pdfplumber` paketi gereklidir. "
                                                      "`pip install pdfplumber` ile yukleyin.")
                    except Exception as e:
                        _koi_imp_error = f"Dosya okuma hatasi: {e}"

                    if _koi_imp_error:
                        st.error(_koi_imp_error)
                    elif imp_df is not None and not imp_df.empty:
                        # Sutun isimlerini normalize et
                        imp_df.columns = [c.strip().lower().replace(" ", "_") for c in imp_df.columns]

                        st.success(f"**{len(imp_df)} kayit** bulundu:")
                        st.dataframe(imp_df.head(15), use_container_width=True, hide_index=True)

                        _has_ad = "ad" in imp_df.columns
                        _has_soyad = "soyad" in imp_df.columns
                        if not _has_ad or not _has_soyad:
                            st.warning("Dosyada **ad** ve **soyad** sütunlari bulunamadi. "
                                       "Sütun basliklarini kontrol edin.")
                        else:
                            st.markdown(f"**{len(imp_df)}** öğrenci import edilecek.")

                            if st.button("Tümünü Import Et", type="primary",
                                         use_container_width=True, key="koi_sl_import_btn"):
                                import uuid as _uuid
                                _stu_path = get_data_path("akademik", "students.json")
                                os.makedirs(os.path.dirname(_stu_path), exist_ok=True)
                                try:
                                    with open(_stu_path, "r", encoding="utf-8") as _f:
                                        _stu_data = json.load(_f)
                                    if not isinstance(_stu_data, list):
                                        _stu_data = _stu_data.get("students", _stu_data.get("records", []))
                                except Exception:
                                    _stu_data = []

                                _eklenen = 0
                                _hatalar = []
                                for i, row in imp_df.iterrows():
                                    try:
                                        _ad = str(row.get("ad", "")).strip()
                                        _soyad = str(row.get("soyad", "")).strip()
                                        if not _ad or not _soyad or _ad == "nan":
                                            continue

                                        yeni = {
                                            "id": f"stu_{_uuid.uuid4().hex[:8]}",
                                            "ad": _ad,
                                            "soyad": _soyad,
                                            "sinif": str(row.get("sinif", "9")).strip(),
                                            "sube": str(row.get("sube", "A")).strip(),
                                            "numara": str(row.get("numara", "")).strip(),
                                            "tc_no": str(row.get("tc_no", "")).strip(),
                                            "cinsiyet": str(row.get("cinsiyet", "")).strip(),
                                            "veli_adi": str(row.get("veli_adi", "")).strip(),
                                            "veli_telefon": str(row.get("veli_telefon", "")).strip(),
                                            "veli_email": str(row.get("veli_email", "")).strip(),
                                            "anne_adi": str(row.get("anne_adi", "")).strip(),
                                            "anne_telefon": str(row.get("anne_telefon", "")).strip(),
                                            "baba_adi": str(row.get("baba_adi", "")).strip(),
                                            "baba_telefon": str(row.get("baba_telefon", "")).strip(),
                                            "durum": "aktif",
                                            "created_at": datetime.now().isoformat(),
                                            "updated_at": datetime.now().isoformat(),
                                        }
                                        # nan temizligi
                                        for _k, _v in yeni.items():
                                            if str(_v).lower() == "nan":
                                                yeni[_k] = ""

                                        _stu_data.append(yeni)
                                        _eklenen += 1
                                    except Exception as e:
                                        _hatalar.append(f"Satir {i+1}: {e}")

                                with open(_stu_path, "w", encoding="utf-8") as _f:
                                    json.dump(_stu_data, _f, ensure_ascii=False, indent=2)
                                st.success(f"✅ {_eklenen} öğrenci başarıyla import edildi! "
                                           "Tüm modüllere otomatik yansıyacaktır.")
                                if _hatalar:
                                    with st.expander(f"⚠️ {len(_hatalar)} hata"):
                                        for h in _hatalar[:20]:
                                            st.warning(h)
                                st.rerun()
                    else:
                        st.warning("Dosyada veri bulunamadi.")

            # ---- LISTELER ----
            with sl_main_tab1:
                if not all_students:
                    st.info("Henuz kayitli ogrenci yok. 'Öğrenci Ekle' veya 'Excel Import' sekmesini kullanin.")
                else:
                    # Kademe -> sinif eslesmesi (SINIF_LISTESI degerlerine gore)
                    _KADEME_MAP = {
                        "Anasınıfı (4 Yaş)": ["Anasınıfı (4 Yaş)"],
                        "Anasınıfı (5 Yaş)": ["Anasınıfı (5 Yaş)"],
                        "Anasınıfı (Hazırlık)": ["Anasınıfı (Hazırlık)"],
                        "İlkokul (1-4)": ["1", "2", "3", "4"],
                        "Ortaokul (5-8)": ["5", "6", "7", "8"],
                        "Lise (9-12)": ["Hazırlık", "9", "10", "11", "12"],
                    }
                    _KADEME_SIRA = list(_KADEME_MAP.keys())

                    # Mevcut sinif ve subeleri topla
                    _sl_mevcut = set(str(s.get("sinif", "")) for s in all_students if s.get("sinif"))
                    _sl_subeler = sorted(set(s.get("sube", "") for s in all_students if s.get("sube")))

                    # Mevcut kademeleri bul (ogrencisi olan)
                    _sl_mevcut_kademeler = []
                    for _kd_ad in _KADEME_SIRA:
                        _kd_siniflar = _KADEME_MAP[_kd_ad]
                        if any(sn in _sl_mevcut for sn in _kd_siniflar):
                            _sl_mevcut_kademeler.append(_kd_ad)

                    sl_c1, sl_c2, sl_c3 = st.columns(3)
                    with sl_c1:
                        sl_kademe = st.selectbox("Kademe", ["Tümü"] + _sl_mevcut_kademeler, key="sl_kademe_sec")
                    with sl_c2:
                        # Kademeye gore sinif listesini filtrele
                        if sl_kademe == "Tümü":
                            _sl_siniflar = [s for s in SINIF_LISTESI if s in _sl_mevcut] or sorted(_sl_mevcut)
                        else:
                            _sl_siniflar = [s for s in _KADEME_MAP.get(sl_kademe, []) if s in _sl_mevcut]
                        sl_sinif = st.selectbox("Sınıf", ["Tümü"] + _sl_siniflar, key="sl_sinif_sec")
                    with sl_c3:
                        sl_sube = st.selectbox("Şube", ["Tümü"] + _sl_subeler, key="sl_sube_sec")

                    # Filtrele
                    sl_filtered = all_students
                    if sl_kademe != "Tümü" and sl_sinif == "Tümü":
                        _kademe_sinif_set = set(_KADEME_MAP.get(sl_kademe, []))
                        sl_filtered = [s for s in sl_filtered if str(s.get("sinif", "")) in _kademe_sinif_set]
                    if sl_sinif != "Tümü":
                        sl_filtered = [s for s in sl_filtered if str(s.get("sinif", "")) == sl_sinif]
                    if sl_sube != "Tümü":
                        sl_filtered = [s for s in sl_filtered if s.get("sube", "") == sl_sube]

                    sl_filtered = sorted(sl_filtered, key=lambda x: (str(x.get("sinif", "")), x.get("sube", ""), x.get("soyad", ""), x.get("ad", "")))

                    # Baslik olustur
                    baslik = ""
                    if sl_kademe != "Tümü" and sl_sinif == "Tümü":
                        baslik = sl_kademe
                    elif sl_sinif != "Tümü":
                        _sl_lower = sl_sinif.lower()
                        if _sl_lower.startswith("ana") or _sl_lower.startswith("anasınıfı") or _sl_lower.startswith("hazırlık"):
                            baslik = sl_sinif
                        else:
                            baslik = f"{sl_sinif}. Sınıf"
                    if sl_sube != "Tümü":
                        baslik = f"{baslik} {sl_sube} Şubesi" if baslik else f"{sl_sube} Şubesi"
                    if not baslik:
                        baslik = "Tüm Öğrenciler"

                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#94A3B8,#334155);color:white;'
                        f'padding:12px 20px;border-radius:10px;margin:10px 0;display:flex;'
                        f'justify-content:space-between;align-items:center">'
                        f'<span style="font-weight:700">{baslik or "Tüm Öğrenciler"}</span>'
                        f'<span style="background:rgba(59,130,246,0.3);padding:4px 14px;border-radius:8px;'
                        f'font-size:0.85rem">{len(sl_filtered)} ogrenci</span></div>',
                        unsafe_allow_html=True,
                    )

                    # ---- Ogrenci ve Veli alt sekmeleri ----
                    sl_tab_ogr, sl_tab_veli = st.tabs(["👨‍🎓 Öğrenci Listesi", "👪 Veli Listesi"])

                    # ---- OGRENCI LISTESI ----
                    with sl_tab_ogr:
                        if sl_filtered:
                            ogr_tbl = []
                            for idx, s in enumerate(sl_filtered, 1):
                                ogr_tbl.append({
                                    "No": idx,
                                    "Ad": s.get("ad", ""),
                                    "Soyad": s.get("soyad", ""),
                                    "Sınıf": str(s.get("sinif", "")),
                                    "Şube": s.get("sube", ""),
                                    "Okul No": s.get("numara", ""),
                                    "Cinsiyet": s.get("cinsiyet", ""),
                                    "Durum": (s.get("durum", "aktif") or "aktif").capitalize(),
                                })
                            df_ogr = pd.DataFrame(ogr_tbl)
                            st.dataframe(df_ogr, use_container_width=True, hide_index=True)

                            # CSV indir
                            csv_ogr = df_ogr.to_csv(index=False).encode("utf-8-sig")
                            st.download_button(
                                "Öğrenci Listesi CSV Indir", data=csv_ogr,
                                file_name=f"ogrenci_listesi_{sl_sinif}_{sl_sube}_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv", key="sl_ogr_csv",
                            )
                        else:
                            st.warning("Secilen kriterlere uygun ogrenci bulunamadı.")

                    # ---- VELI LISTESI ----
                    with sl_tab_veli:
                        if sl_filtered:
                            veli_tbl = []
                            for idx, s in enumerate(sl_filtered, 1):
                                ad_soyad = f'{s.get("ad", "")} {s.get("soyad", "")}'.strip()
                                veli_adi = s.get("veli_adi", "")
                                veli_tel = s.get("veli_telefon", "")
                                veli_email = s.get("veli_email", "")
                                anne_adi = f'{s.get("anne_adi", "")} {s.get("anne_soyadi", "")}'.strip()
                                anne_tel = s.get("anne_telefon", "")
                                baba_adi = f'{s.get("baba_adi", "")} {s.get("baba_soyadi", "")}'.strip()
                                baba_tel = s.get("baba_telefon", "")
                                veli_tbl.append({
                                    "No": idx,
                                    "Öğrenci": ad_soyad,
                                    "Sınıf": f'{s.get("sinif", "")}/{s.get("sube", "")}',
                                    "Veli": veli_adi,
                                    "Veli Tel": veli_tel,
                                    "Veli E-posta": veli_email,
                                    "Anne": anne_adi,
                                    "Anne Tel": anne_tel,
                                    "Baba": baba_adi,
                                    "Baba Tel": baba_tel,
                                })
                            df_veli = pd.DataFrame(veli_tbl)
                            st.dataframe(df_veli, use_container_width=True, hide_index=True)

                            # CSV indir
                            csv_veli = df_veli.to_csv(index=False).encode("utf-8-sig")
                            st.download_button(
                                "Veli Listesi CSV Indir", data=csv_veli,
                                file_name=f"veli_listesi_{sl_sinif}_{sl_sube}_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv", key="sl_veli_csv",
                            )
                        else:
                            st.warning("Secilen kriterlere uygun ogrenci bulunamadı.")

        # ---------- YENI MESAJ ----------
        with msg_sub1:
            styled_section("Mesaj Oluştur", "#10b981")

            # Kanal secimi
            kc1, kc2, kc3 = st.columns(3)
            with kc1:
                kanal = st.selectbox("Gonderim Kanali", [k[0] for k in KANAL_OPTIONS],
                                      format_func=lambda x: _KANAL_MAP[x]["label"],
                                      key="msg_kanal")
            with kc2:
                sablon_key = st.selectbox("Mesaj Şablonu", [s[0] for s in SABLON_TIPLERI],
                                            format_func=lambda x: dict(SABLON_TIPLERI)[x],
                                            key="msg_sablon")
            with kc3:
                oncelik = st.selectbox("Öncelik", ["Normal", "Yuksek", "Acil"], key="msg_oncelik")

            # Gonderen bilgisi
            styled_section("Gonderen", "#1a237e")
            gc1, gc2, gc3 = st.columns(3)
            with gc1:
                g_ad = st.text_input("Gonderen Adi", value=profile.get("name", ""), key="msg_g_ad")
            with gc2:
                g_unvan = st.text_input("Gonderen Unvani", value="Kurum Yönetimi", key="msg_g_unvan")
            with gc3:
                g_iletisim = st.text_input("Gonderen İletişim",
                                            value=profile.get("phone", "") if kanal == "sms"
                                            else profile.get("email", ""),
                                            key="msg_g_iletisim")

            # Alici secimi
            styled_section("Alicilar", "#2563eb")
            alici_tipi = st.radio("Alici Tipi", ["Kurum Ici", "Kurum Disi (Veliler)"],
                                   horizontal=True, key="msg_alici_tipi")

            secilen_alicilar: list[dict] = []

            if alici_tipi == "Kurum Ici":
                ai_secim = st.radio("Secim Yontemi", ["Kategori", "Bireysel"],
                                     horizontal=True, key="msg_ki_secim")

                if ai_secim == "Kategori":
                    sec_cats = st.multiselect("Kategori Sec", [g[1] for g in KURUM_ICI_GRUPLAR[1:]],
                                               key="msg_ki_cat")
                    cat_id_map = {g[1]: g[0] for g in KURUM_ICI_GRUPLAR}
                    for s in all_staff:
                        cat_label = _CAT_MAP.get(s.get("category", "diger"), _CAT_MAP["diger"])["label"]
                        if cat_label in sec_cats:
                            secilen_alicilar.append({
                                "ad": s.get("ad", ""), "soyad": s.get("soyad", ""),
                                "iletisim": s.get("telefon", "") if kanal in ("sms", "whatsapp") else s.get("email", ""),
                                "unvan": s.get("unvan", ""), "tip": "kurum_ici"
                            })
                    if sec_cats:
                        st.info(f"Secilen kategorilerde {len(secilen_alicilar)} kisi")

                else:  # Bireysel
                    kisi_opts = [f"{s.get('ad', '')} {s.get('soyad', '')} - {s.get('unvan', '')}" for s in all_staff]
                    sec_kisiler = st.multiselect("Kisi Sec", kisi_opts, key="msg_ki_birey")
                    for i, s in enumerate(all_staff):
                        if kisi_opts[i] in sec_kisiler:
                            secilen_alicilar.append({
                                "ad": s.get("ad", ""), "soyad": s.get("soyad", ""),
                                "iletisim": s.get("telefon", "") if kanal in ("sms", "whatsapp") else s.get("email", ""),
                                "unvan": s.get("unvan", ""), "tip": "kurum_ici"
                            })

            else:  # Kurum Disi
                ad_secim = st.radio("Secim Yontemi",
                                     ["Sınıf/Şube", "Kademe", "Bireysel", "Tümü", "Tanitim"],
                                     horizontal=True, key="msg_kd_secim")

                if ad_secim == "Tümü":
                    for stu in all_students:
                        veli_tel = stu.get("veli_telefon", stu.get("parent_phone", ""))
                        veli_email = stu.get("veli_email", stu.get("parent_email", ""))
                        veli_ad = stu.get("veli_adi", stu.get("parent_name", "Veli"))
                        secilen_alicilar.append({
                            "ad": veli_ad, "soyad": "",
                            "iletisim": veli_tel if kanal in ("sms", "whatsapp") else veli_email,
                            "unvan": f"Veli ({stu.get('ad', '')} {stu.get('soyad', '')})",
                            "tip": "kurum_disi"
                        })
                    st.info(f"Tüm veliler secildi: {len(secilen_alicilar)} kisi")

                elif ad_secim == "Sınıf/Şube":
                    ss1, ss2 = st.columns(2)
                    with ss1:
                        sec_siniflar = st.multiselect("Sınıf", KADEME_OPTIONS, key="msg_kd_sinif")
                    with ss2:
                        sec_subeler = st.multiselect("Şube", SUBE_OPTIONS, key="msg_kd_sube")
                    # Secilen siniflari ogrenci sinif degerleriyle eslestirmek icin harita
                    _sec_sinif_keys = set()
                    for _ss in sec_siniflar:
                        if _ss.startswith("Anasınıfı"):
                            _sec_sinif_keys.add(_ss)  # Direkt eslesme
                        else:
                            _sec_sinif_keys.add(_ss.split(".")[0].strip())  # "5. Sınıf" -> "5"
                    for stu in all_students:
                        stu_sinif = stu.get("sinif", stu.get("grade", ""))
                        stu_sube = stu.get("sube", stu.get("section", ""))
                        sinif_match = not sec_siniflar or str(stu_sinif) in _sec_sinif_keys
                        sube_match = not sec_subeler or str(stu_sube).upper() in sec_subeler
                        if sinif_match and sube_match:
                            veli_tel = stu.get("veli_telefon", stu.get("parent_phone", ""))
                            veli_email = stu.get("veli_email", stu.get("parent_email", ""))
                            veli_ad = stu.get("veli_adi", stu.get("parent_name", "Veli"))
                            secilen_alicilar.append({
                                "ad": veli_ad, "soyad": "",
                                "iletisim": veli_tel if kanal in ("sms", "whatsapp") else veli_email,
                                "unvan": f"Veli ({stu.get('ad', '')} {stu.get('soyad', '')} {stu_sinif}/{stu_sube})",
                                "tip": "kurum_disi"
                            })
                    if sec_siniflar or sec_subeler:
                        st.info(f"Secilen sinif/subelerde {len(secilen_alicilar)} veli")

                elif ad_secim == "Kademe":
                    _msg_kademe_opts = [
                        "Anasınıfı (4 Yaş)", "Anasınıfı (5 Yaş)", "Anasınıfı (Hazırlık)",
                        "İlkokul (1-4)", "Ortaokul (5-8)", "Lise (9-12)",
                    ]
                    sec_kademe = st.multiselect("Kademe", _msg_kademe_opts, key="msg_kd_kademe")
                    # Kademe -> ogrenci sinif eslesmesi (SINIF_LISTESI degerleriyle)
                    _msg_kademe_map = {
                        "Anasınıfı (4 Yaş)": ["Anasınıfı (4 Yaş)"],
                        "Anasınıfı (5 Yaş)": ["Anasınıfı (5 Yaş)"],
                        "Anasınıfı (Hazırlık)": ["Anasınıfı (Hazırlık)"],
                        "İlkokul (1-4)": ["1", "2", "3", "4"],
                        "Ortaokul (5-8)": ["5", "6", "7", "8"],
                        "Lise (9-12)": ["Hazırlık", "9", "10", "11", "12"],
                    }
                    _allowed_siniflar = set()
                    for k in sec_kademe:
                        _allowed_siniflar.update(_msg_kademe_map.get(k, []))
                    for stu in all_students:
                        _stu_sinif = str(stu.get("sinif", stu.get("grade", ""))).strip()
                        if _stu_sinif in _allowed_siniflar:
                            veli_tel = stu.get("veli_telefon", stu.get("parent_phone", ""))
                            veli_email = stu.get("veli_email", stu.get("parent_email", ""))
                            veli_ad = stu.get("veli_adi", stu.get("parent_name", "Veli"))
                            secilen_alicilar.append({
                                "ad": veli_ad, "soyad": "",
                                "iletisim": veli_tel if kanal in ("sms", "whatsapp") else veli_email,
                                "unvan": f"Veli ({stu.get('ad', '')} {stu.get('soyad', '')})",
                                "tip": "kurum_disi"
                            })
                    if sec_kademe:
                        st.info(f"Secilen kademede {len(secilen_alicilar)} veli")

                elif ad_secim == "Bireysel":
                    veli_opts = [
                        f"{stu.get('veli_adi', stu.get('parent_name', 'Veli'))} - ({stu.get('ad', '')} {stu.get('soyad', '')})"
                        for stu in all_students
                    ]
                    sec_veliler = st.multiselect("Veli Sec", veli_opts, key="msg_kd_birey")
                    for i, stu in enumerate(all_students):
                        if i < len(veli_opts) and veli_opts[i] in sec_veliler:
                            veli_tel = stu.get("veli_telefon", stu.get("parent_phone", ""))
                            veli_email = stu.get("veli_email", stu.get("parent_email", ""))
                            veli_ad = stu.get("veli_adi", stu.get("parent_name", "Veli"))
                            secilen_alicilar.append({
                                "ad": veli_ad, "soyad": "",
                                "iletisim": veli_tel if kanal in ("sms", "whatsapp") else veli_email,
                                "unvan": f"Veli ({stu.get('ad', '')} {stu.get('soyad', '')})",
                                "tip": "kurum_disi"
                            })

                else:  # Tanitim
                    st.markdown("""<div style="background:#1e293b;border:1px solid #bfdbfe;
                    border-radius:10px;padding:12px 16px;font-size:0.85rem;color:#93c5fd">
                    Tanitim amacli mesaj gondermek için alici bilgilerini manuel girin.
                    </div>""", unsafe_allow_html=True)
                    tan_icerik = st.text_area("Alici Listesi (her satira bir numara/email)",
                                               key="msg_tan_list", height=100,
                                               placeholder="05XX XXX XX XX\n05YY YYY YY YY")
                    if tan_icerik:
                        for line in tan_icerik.strip().split("\n"):
                            line = line.strip()
                            if line:
                                secilen_alicilar.append({
                                    "ad": "Tanitim", "soyad": "",
                                    "iletisim": line, "unvan": "Tanitim", "tip": "tanitim"
                                })

            # Secilen alicilar ozeti
            if secilen_alicilar:
                st.markdown(
                    f'<div style="background:#1e293b;border:1px solid #bbf7d0;border-radius:10px;'
                    f'padding:10px 16px;margin:8px 0;font-size:0.85rem;color:#86efac">'
                    f'<b>{len(secilen_alicilar)}</b> alici secildi  |  '
                    f'Kanal: <b>{_KANAL_MAP[kanal]["label"]}</b>  |  '
                    f'Şablon: <b>{dict(SABLON_TIPLERI)[sablon_key]}</b></div>',
                    unsafe_allow_html=True
                )

            # Mesaj icerigi
            styled_section("Mesaj Icerigi", "#8b5cf6")
            msg_konu = st.text_input("Konu", key="msg_konu",
                                      placeholder="Mesaj konusunu girin")
            default_icerik = SABLON_ICERIK.get(sablon_key, "")
            msg_icerik = st.text_area("Mesaj Metni", value=default_icerik, height=180,
                                       key="msg_icerik",
                                       placeholder="Mesaj icerigini yazin...")

            # Dosya eki
            styled_section("Dosya Eki", "#059669")
            ek_dosyalar = st.file_uploader(
                "Dosya Ekle (PDF, Word, Excel, Resim vb.)",
                type=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
                      "jpg", "jpeg", "png", "gif", "bmp", "zip", "rar", "txt", "csv"],
                accept_multiple_files=True,
                key="msg_ekler",
            )
            if ek_dosyalar:
                from utils.security import validate_upload
                _valid_ekler = []
                for ef in ek_dosyalar:
                    _ok, _msg = validate_upload(ef, allowed_types=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "jpg", "jpeg", "png", "gif", "bmp", "zip", "rar", "txt", "csv"], max_mb=50)
                    if _ok:
                        _valid_ekler.append(ef)
                    else:
                        st.warning(f"⚠️ {ef.name}: {_msg}")
                ek_dosyalar = _valid_ekler
            if ek_dosyalar:
                ek_info = []
                for ef in ek_dosyalar:
                    size_kb = len(ef.getvalue()) / 1024
                    size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB"
                    ek_info.append(f"<span style='background:#1e293b;border:1px solid #bbf7d0;"
                                   f"border-radius:8px;padding:4px 10px;font-size:12px;color:#86efac'>"
                                   f"📎 {ef.name} ({size_str})</span>")
                st.markdown(
                    f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:4px 0">'
                    + "".join(ek_info) + '</div>', unsafe_allow_html=True
                )

            st.markdown("")
            bc1, bc2 = st.columns([3, 1])
            with bc1:
                if st.button("Mesaji Gonder", key="msg_gonder", type="primary",
                             use_container_width=True):
                    if not msg_konu.strip():
                        st.error("Mesaj konusu zorunludur.")
                    elif not msg_icerik.strip():
                        st.error("Mesaj icerigi zorunludur.")
                    elif not secilen_alicilar:
                        st.error("En az bir alici secmelisiniz.")
                    else:
                        alicilar_kayit = []
                        gonderim_basarili = 0
                        gonderim_basarisiz = 0
                        gonderim_hatalari = []

                        progress_bar = st.progress(0, text="Mesajlar gonderiliyor...")
                        toplam = len(secilen_alicilar)

                        for idx, alici in enumerate(secilen_alicilar):
                            iletisim_bilgi = alici.get("iletisim", "")
                            durum = "iletilemedi"
                            gonderim_sonuc = ""
                            iletim_zamani = ""

                            # Gercek gonderim yap
                            if kanal == "panel":
                                # Panel kanali: VeliMesaj olarak kaydet
                                try:
                                    _panel_store = get_akademik_store()
                                    _auth = st.session_state.get("auth_user", {})
                                    _s_type = {"Yonetici": "yonetici", "Öğretmen": "ogretmen",
                                               "Çalışan": "calisan"}.get(_auth.get("role", ""), "yonetici")
                                    _r_id = alici.get("username", alici.get("iletisim", ""))
                                    _r_name = f"{alici.get('ad', '')} {alici.get('soyad', '')}".strip()
                                    _panel_msg = VeliMesaj(
                                        sender_type=_s_type,
                                        sender_id=_auth.get("username", ""),
                                        sender_name=_auth.get("name", ""),
                                        receiver_type=alici.get("tip", "veli"),
                                        receiver_id=_r_id,
                                        receiver_name=_r_name,
                                        konu=msg_konu.strip(),
                                        icerik=msg_icerik.strip(),
                                        kategori="duyuru",
                                    )
                                    _panel_msg.conversation_id = _panel_msg.id
                                    _panel_store.save_veli_mesaj(_panel_msg)
                                    durum = "iletildi"
                                    gonderim_basarili += 1
                                    gonderim_sonuc = "Panel mesaji gonderildi"
                                    iletim_zamani = datetime.utcnow().isoformat()
                                except Exception as e:
                                    durum = "hata"
                                    gonderim_basarisiz += 1
                                    gonderim_sonuc = str(e)
                                    gonderim_hatalari.append(f"{alici.get('ad', '')} {alici.get('soyad', '')}: {e}")
                            elif iletisim_bilgi and iletisim_bilgi.strip():
                                try:
                                    ok, info = _send_message_real(
                                        kanal,
                                        iletisim_bilgi.strip(),
                                        msg_konu.strip(),
                                        msg_icerik.strip(),
                                    )
                                    if ok:
                                        durum = "iletildi"
                                        gonderim_basarili += 1
                                        gonderim_sonuc = info
                                        iletim_zamani = datetime.utcnow().isoformat()
                                    else:
                                        durum = "hata"
                                        gonderim_basarisiz += 1
                                        gonderim_sonuc = info
                                        gonderim_hatalari.append(f"{alici.get('ad', '')} {alici.get('soyad', '')}: {info}")
                                except Exception as e:
                                    durum = "hata"
                                    gonderim_basarisiz += 1
                                    gonderim_sonuc = str(e)
                                    gonderim_hatalari.append(f"{alici.get('ad', '')} {alici.get('soyad', '')}: {e}")
                            else:
                                durum = "iletilemedi"
                                gonderim_sonuc = "İletişim bilgisi bos"

                            alicilar_kayit.append({
                                "ad": alici["ad"],
                                "soyad": alici.get("soyad", ""),
                                "unvan": alici.get("unvan", ""),
                                "iletisim": iletisim_bilgi,
                                "tip": alici.get("tip", ""),
                                "durum": durum,
                                "gonderim_sonuc": gonderim_sonuc,
                                "okundu": False,
                                "cevap": False,
                                "iletim_zamani": iletim_zamani,
                                "okunma_zamani": "",
                                "cevap_zamani": "",
                            })

                            progress_bar.progress(
                                (idx + 1) / toplam,
                                text=f"Gonderiliyor... {idx + 1}/{toplam}"
                            )

                        progress_bar.empty()

                        # Dosya eklerini kaydet
                        ekler_bilgi = []
                        if ek_dosyalar:
                            ek_dir = os.path.join(get_tenant_dir(), "msg_attachments")
                            os.makedirs(ek_dir, exist_ok=True)
                            for ef in ek_dosyalar:
                                dosya_id = uuid.uuid4().hex[:8]
                                ext = os.path.splitext(ef.name)[1].lower()
                                dosya_adi = f"{dosya_id}{ext}"
                                dosya_yolu = os.path.join(ek_dir, dosya_adi)
                                with open(dosya_yolu, "wb") as df:
                                    df.write(ef.getvalue())
                                ekler_bilgi.append({
                                    "orijinal_ad": ef.name,
                                    "dosya_adi": dosya_adi,
                                    "dosya_yolu": dosya_yolu,
                                    "boyut": len(ef.getvalue()),
                                    "tip": ef.type or "",
                                })

                        yeni_mesaj = {
                            "id": _gen_msg_id(),
                            "kanal": kanal,
                            "sablon": sablon_key,
                            "oncelik": oncelik,
                            "konu": msg_konu.strip(),
                            "icerik": msg_icerik.strip(),
                            "ekler": ekler_bilgi,
                            "gonderen": {
                                "ad": g_ad.strip(),
                                "unvan": g_unvan.strip(),
                                "iletisim": g_iletisim.strip(),
                            },
                            "alici_tipi": alici_tipi,
                            "alicilar": alicilar_kayit,
                            "toplam_alici": len(alicilar_kayit),
                            "iletildi_sayisi": gonderim_basarili,
                            "hata_sayisi": gonderim_basarisiz,
                            "created_at": datetime.utcnow().isoformat(),
                        }
                        messages.append(yeni_mesaj)
                        _save_messages(messages)

                        # Sonuc ozeti
                        if gonderim_basarili > 0:
                            st.success(f"{gonderim_basarili} aliciya basariyla gonderildi.")
                        if gonderim_basarisiz > 0:
                            st.warning(f"{gonderim_basarisiz} aliciya gonderilemedi.")
                            with st.expander("Hata Detaylari"):
                                for h in gonderim_hatalari:
                                    st.text(h)
                        if gonderim_basarili == 0 and gonderim_basarisiz == 0:
                            st.info("İletişim bilgisi olan alici bulunamadı.")
                        st.rerun()
            with bc2:
                if st.button("Temizle", key="msg_temizle", use_container_width=True):
                    st.rerun()

        # ---------- GONDERILEN MESAJLAR ----------
        with msg_sub2:
            if messages:
                styled_section("Gonderim Geçmişi", "#1a237e")

                # Filtre
                fc1, fc2, fc3 = st.columns(3)
                with fc1:
                    f_kanal = st.selectbox("Kanal", ["Tümü"] + [k[1] for k in KANAL_OPTIONS],
                                            key="msg_f_kanal")
                with fc2:
                    f_sablon = st.selectbox("Şablon", ["Tümü"] + [s[1] for s in SABLON_TIPLERI],
                                             key="msg_f_sablon")
                with fc3:
                    f_tip = st.selectbox("Alici Tipi", ["Tümü", "Kurum Ici", "Kurum Disi"],
                                          key="msg_f_tip")

                filtered_msgs = list(reversed(messages))
                if f_kanal != "Tümü":
                    kanal_id = [k[0] for k in KANAL_OPTIONS if k[1] == f_kanal]
                    if kanal_id:
                        filtered_msgs = [m for m in filtered_msgs if m.get("kanal") == kanal_id[0]]
                if f_sablon != "Tümü":
                    sablon_id = [s[0] for s in SABLON_TIPLERI if s[1] == f_sablon]
                    if sablon_id:
                        filtered_msgs = [m for m in filtered_msgs if m.get("sablon") == sablon_id[0]]
                if f_tip != "Tümü":
                    filtered_msgs = [m for m in filtered_msgs if m.get("alici_tipi") == f_tip]

                st.caption(f"{len(filtered_msgs)} mesaj gosteriliyor")

                for msg in filtered_msgs:
                    kanal_info = _KANAL_MAP.get(msg.get("kanal", "sms"), _KANAL_MAP["sms"])
                    sablon_label = dict(SABLON_TIPLERI).get(msg.get("sablon", "ozel"), "Serbest")
                    tarih = msg.get("created_at", "")[:16].replace("T", " ")
                    toplam = msg.get("toplam_alici", 0)
                    iletildi = sum(1 for a in msg.get("alicilar", []) if a.get("durum") == "iletildi")
                    okundu = sum(1 for a in msg.get("alicilar", []) if a.get("okundu"))
                    cevap = sum(1 for a in msg.get("alicilar", []) if a.get("cevap"))

                    header = f"{kanal_info['label']} | {msg.get('konu', '-')} | {tarih} | {iletildi}/{toplam} iletildi"

                    with st.expander(header, expanded=False):
                        # Mesaj detay
                        st.markdown(
                            f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px">'
                            f'<span style="background:{kanal_info["color"]};color:white;padding:4px 12px;'
                            f'border-radius:8px;font-size:12px;font-weight:600">{kanal_info["label"]}</span>'
                            f'<span style="background:#1e293b;color:#93c5fd;padding:4px 12px;'
                            f'border-radius:8px;font-size:12px">{sablon_label}</span>'
                            f'<span style="background:#fef3c7;color:#fbbf24;padding:4px 12px;'
                            f'border-radius:8px;font-size:12px">{msg.get("oncelik", "Normal")}</span>'
                            f'<span style="background:#0B0F19;color:#94a3b8;padding:4px 12px;'
                            f'border-radius:8px;font-size:12px">{msg.get("alici_tipi", "")}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        # Gonderen
                        gnd = msg.get("gonderen", {})
                        st.markdown(
                            f'<div style="background:#111827;border-radius:8px;padding:10px;'
                            f'margin-bottom:8px;font-size:0.85rem">'
                            f'<b>Gonderen:</b> {gnd.get("ad", "")} - {gnd.get("unvan", "")}'
                            f'</div>', unsafe_allow_html=True
                        )

                        # Mesaj icerigi
                        st.text_area("Mesaj", value=msg.get("icerik", ""), height=100,
                                      disabled=True, key=f"msg_view_{msg['id']}")

                        # Durum istatistikleri
                        dc1, dc2, dc3, dc4 = st.columns(4)
                        with dc1:
                            st.metric("Toplam Alici", toplam)
                        with dc2:
                            st.metric("İletildi", iletildi)
                        with dc3:
                            st.metric("Okundu", okundu)
                        with dc4:
                            st.metric("Cevaplandi", cevap)

                        # Alici detay tablosu
                        if msg.get("alicilar"):
                            alici_rows = []
                            for a in msg["alicilar"]:
                                alici_rows.append({
                                    "Ad Soyad": f"{a.get('ad', '')} {a.get('soyad', '')}".strip(),
                                    "Unvan": a.get("unvan", ""),
                                    "İletişim": a.get("iletisim", ""),
                                    "Durum": "İletildi" if a.get("durum") == "iletildi" else "İletilemedi",
                                    "Okundu": "Evet" if a.get("okundu") else "Hayir",
                                    "Cevap": "Evet" if a.get("cevap") else "Hayir",
                                })
                            df_alici = pd.DataFrame(alici_rows)
                            st.dataframe(df_alici, use_container_width=True, hide_index=True)

                        # Dosya ekleri
                        if msg.get("ekler"):
                            styled_section("Dosya Ekleri", "#0d9488")
                            ek_chips = []
                            for ek in msg["ekler"]:
                                boyut = ek.get("boyut", 0)
                                b_str = f"{boyut / 1024:.0f} KB" if boyut < 1048576 else f"{boyut / 1048576:.1f} MB"
                                ek_chips.append(
                                    f"<span style='background:#1e293b;border:1px solid #bbf7d0;"
                                    f"border-radius:8px;padding:5px 12px;font-size:12px;color:#86efac'>"
                                    f"📎 {ek.get('orijinal_ad', '')} ({b_str})</span>"
                                )
                            st.markdown(
                                '<div style="display:flex;flex-wrap:wrap;gap:8px">'
                                + "".join(ek_chips) + '</div>', unsafe_allow_html=True
                            )
                            # Dosya indirme
                            for ek in msg["ekler"]:
                                yol = ek.get("dosya_yolu", "")
                                if yol and os.path.exists(yol):
                                    with open(yol, "rb") as ef:
                                        st.download_button(
                                            f"Indir: {ek.get('orijinal_ad', '')}",
                                            data=ef.read(),
                                            file_name=ek.get("orijinal_ad", "dosya"),
                                            mime=ek.get("tip", "application/octet-stream"),
                                            key=f"dl_ek_{msg['id']}_{ek.get('dosya_adi', '')}",
                                        )

                        # Durum guncelleme
                        styled_section("Durum Güncelle", "#059669")
                        uc1, uc2, uc3 = st.columns(3)
                        with uc1:
                            if st.button("Tümünu Okundu Yap", key=f"msg_ok_{msg['id']}"):
                                for a in msg.get("alicilar", []):
                                    if a.get("durum") == "iletildi":
                                        a["okundu"] = True
                                        a["okunma_zamani"] = datetime.utcnow().isoformat()
                                _save_messages(messages)
                                st.rerun()
                        with uc2:
                            if st.button("Tümünu Cevaplandi Yap", key=f"msg_cv_{msg['id']}"):
                                for a in msg.get("alicilar", []):
                                    if a.get("okundu"):
                                        a["cevap"] = True
                                        a["cevap_zamani"] = datetime.utcnow().isoformat()
                                _save_messages(messages)
                                st.rerun()
                        with uc3:
                            if st.button("Mesaji Sil", key=f"msg_del_{msg['id']}"):
                                messages = [m for m in messages if m["id"] != msg["id"]]
                                _save_messages(messages)
                                st.rerun()
            else:
                st.markdown("""<div style="background:#111827;border:2px dashed #e2e8f0;
                border-radius:16px;padding:40px;text-align:center;margin:20px 0">
                <div style="font-size:3rem;margin-bottom:12px">📨</div>
                <div style="font-size:1.1rem;font-weight:600;color:#94a3b8;margin-bottom:6px">
                Henuz mesaj gonderilmedi</div>
                <div style="font-size:0.85rem;color:#94a3b8">
                Yeni Mesaj sekmesinden ilk mesajinizi gonderin</div>
                </div>""", unsafe_allow_html=True)

        # ---------- RAPORLAR ----------
        with msg_sub3:
            if messages:
                styled_section("Genel İletişim Raporu", "#1a237e")

                # Toplam istatistikler
                total_alici = sum(len(m.get("alicilar", [])) for m in messages)
                total_iletildi = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("durum") == "iletildi")
                total_iletilemedi = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("durum") == "iletilemedi")
                total_okundu = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("okundu"))
                total_cevap = sum(1 for m in messages for a in m.get("alicilar", []) if a.get("cevap"))

                iletim_oran = int(total_iletildi / total_alici * 100) if total_alici > 0 else 0
                okunma_oran = int(total_okundu / total_iletildi * 100) if total_iletildi > 0 else 0
                cevap_oran = int(total_cevap / total_okundu * 100) if total_okundu > 0 else 0

                styled_stat_row([
                    ("Iletim Orani", f"%{iletim_oran}", "#10b981", "📤"),
                    ("Okunma Orani", f"%{okunma_oran}", "#2563eb", "👁️"),
                    ("Cevap Orani", f"%{cevap_oran}", "#8b5cf6", "💬"),
                    ("İletilemedi", str(total_iletilemedi), "#ef4444", "❌"),
                ])
                st.markdown("")

                # ---- PLOTLY GRAFIKLER ----
                # Iletim / Okunma / Cevap Donut Charts
                styled_section("Durum Analizi", "#0d9488")
                dr1, dr2, dr3 = st.columns(3)
                total_okunmadi = total_iletildi - total_okundu
                total_cevaplanmadi = total_okundu - total_cevap

                with dr1:
                    fig_d_iletim = go.Figure(go.Pie(
                        labels=["İletildi", "İletilemedi"],
                        values=[total_iletildi, total_iletilemedi],
                        hole=0.55,
                        marker=dict(colors=SC_COLORS[:2], line=dict(color="#fff", width=2)),
                        textinfo='label+value+percent',
                        textposition='outside',
                    ))
                    sc_pie(fig_d_iletim, height=280)
                    fig_d_iletim.update_layout(title=dict(text="Iletim Durumu", x=0.5, font=dict(size=13)))
                    st.plotly_chart(fig_d_iletim, use_container_width=True, key="ch_iletim_d", config=SC_CHART_CFG)

                with dr2:
                    fig_d_okunma = go.Figure(go.Pie(
                        labels=["Okundu", "Okunmadi"],
                        values=[total_okundu, max(0, total_okunmadi)],
                        hole=0.55,
                        marker=dict(colors=SC_COLORS[:2], line=dict(color="#fff", width=2)),
                        textinfo='label+value+percent',
                        textposition='outside',
                    ))
                    sc_pie(fig_d_okunma, height=280)
                    fig_d_okunma.update_layout(title=dict(text="Okunma Durumu", x=0.5, font=dict(size=13)))
                    st.plotly_chart(fig_d_okunma, use_container_width=True, key="ch_okunma_d", config=SC_CHART_CFG)

                with dr3:
                    fig_d_cevap = go.Figure(go.Pie(
                        labels=["Cevaplandi", "Cevaplanmadi"],
                        values=[total_cevap, max(0, total_cevaplanmadi)],
                        hole=0.55,
                        marker=dict(colors=SC_COLORS[:2], line=dict(color="#fff", width=2)),
                        textinfo='label+value+percent',
                        textposition='outside',
                    ))
                    sc_pie(fig_d_cevap, height=280)
                    fig_d_cevap.update_layout(title=dict(text="Cevap Durumu", x=0.5, font=dict(size=13)))
                    st.plotly_chart(fig_d_cevap, use_container_width=True, key="ch_cevap_d", config=SC_CHART_CFG)

                # Kanal + Şablon bar charts
                kr1, kr2 = st.columns(2)
                sablon_map = dict(SABLON_TIPLERI)
                with kr1:
                    styled_section("Kanal Dağılımı", "#10b981")
                    kanal_dist: dict[str, int] = {}
                    for m in messages:
                        ki = _KANAL_MAP.get(m.get("kanal", "sms"), _KANAL_MAP["sms"])
                        kanal_dist[ki["label"]] = kanal_dist.get(ki["label"], 0) + 1
                    fig_kanal = go.Figure(go.Bar(
                        x=list(kanal_dist.keys()), y=list(kanal_dist.values()),
                        marker_color=SC_COLORS[0],
                        text=list(kanal_dist.values()), textposition='outside',
                    ))
                    sc_bar(fig_kanal, height=300)
                    st.plotly_chart(fig_kanal, use_container_width=True, key="ch_kanal_bar", config=SC_CHART_CFG)

                with kr2:
                    styled_section("Şablon Dağılımı", "#8b5cf6")
                    sablon_dist: dict[str, int] = {}
                    for m in messages:
                        sl = sablon_map.get(m.get("sablon", "ozel"), "Serbest")
                        sablon_dist[sl] = sablon_dist.get(sl, 0) + 1
                    sb_sorted = sorted(sablon_dist.items(), key=lambda x: x[1])
                    fig_sablon = go.Figure(go.Bar(
                        x=[v for _, v in sb_sorted],
                        y=[k for k, _ in sb_sorted],
                        orientation='h',
                        marker_color=SC_COLORS[2],
                        text=[str(v) for _, v in sb_sorted], textposition='outside',
                    ))
                    sc_bar(fig_sablon, height=300, horizontal=True)
                    st.plotly_chart(fig_sablon, use_container_width=True, key="ch_sablon_bar", config=SC_CHART_CFG)

                # Sunburst: Alici Tipi > Kanal > Şablon
                styled_section("Mesaj Dağılım Sunburst", "#1a237e")
                sb_l, sb_p, sb_v, sb_c = ["Tüm Mesajlar"], [""], [0], ["#0B0F19"]
                # Level 1: Alici tipi
                tip_dist: dict[str, int] = {}
                for m in messages:
                    tl = m.get("alici_tipi", "Bilinmiyor")
                    tip_dist[tl] = tip_dist.get(tl, 0) + 1
                tip_clr = {"Kurum Ici": "#2563eb", "Kurum Disi": "#f59e0b", "Bilinmiyor": "#94a3b8"}
                for tl, cnt in tip_dist.items():
                    sb_l.append(tl)
                    sb_p.append("Tüm Mesajlar")
                    sb_v.append(0)
                    sb_c.append(tip_clr.get(tl, "#64748b"))
                # Level 2: Kanal per tip
                tip_kanal: dict[str, dict[str, int]] = {}
                for m in messages:
                    tl = m.get("alici_tipi", "Bilinmiyor")
                    ki = _KANAL_MAP.get(m.get("kanal", "sms"), _KANAL_MAP["sms"])
                    tip_kanal.setdefault(tl, {})
                    tip_kanal[tl][ki["label"]] = tip_kanal[tl].get(ki["label"], 0) + 1
                for tl, kanals in tip_kanal.items():
                    for kl, cnt in kanals.items():
                        sb_l.append(f"{kl} ({tl[:5]})")
                        sb_p.append(tl)
                        sb_v.append(cnt)
                        sb_c.append(kanal_clrs.get(kl, "#64748b"))
                fig_msg_sb = go.Figure(go.Sunburst(
                    labels=sb_l, parents=sb_p, values=sb_v,
                    marker=dict(colors=sb_c),
                    branchvalues="total",
                    textinfo="label+value",
                    insidetextorientation='radial',
                ))
                fig_msg_sb.update_layout(
                    height=420, margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)', font=dict(size=11),
                )
                st.plotly_chart(fig_msg_sb, use_container_width=True, key="ch_msg_sunburst")

                # Kimlere atilmis - alici bazli bar chart
                styled_section("Kimlere Mesaj Atildi", "#059669")
                alici_agg: dict[str, dict[str, int]] = {}
                for m in messages:
                    for a in m.get("alicilar", []):
                        name = f"{a.get('ad', '')} {a.get('soyad', '')}".strip() or "Bilinmiyor"
                        if name not in alici_agg:
                            alici_agg[name] = {"iletildi": 0, "iletilemedi": 0, "okundu": 0, "cevap": 0}
                        if a.get("durum") == "iletildi":
                            alici_agg[name]["iletildi"] += 1
                        else:
                            alici_agg[name]["iletilemedi"] += 1
                        if a.get("okundu"):
                            alici_agg[name]["okundu"] += 1
                        if a.get("cevap"):
                            alici_agg[name]["cevap"] += 1
                # Top 20 alici
                top_alici = sorted(alici_agg.items(), key=lambda x: sum(x[1].values()), reverse=True)[:20]
                if top_alici:
                    ta_names = [t[0] for t in reversed(top_alici)]
                    fig_alici = go.Figure()
                    fig_alici.add_trace(go.Bar(
                        y=ta_names, x=[alici_agg[n]["iletildi"] for n in ta_names],
                        name="İletildi", orientation='h', marker_color=SC_COLORS[1],
                        text=[alici_agg[n]["iletildi"] for n in ta_names], textposition='outside',
                    ))
                    fig_alici.add_trace(go.Bar(
                        y=ta_names, x=[alici_agg[n]["iletilemedi"] for n in ta_names],
                        name="İletilemedi", orientation='h', marker_color=SC_COLORS[4],
                        text=[alici_agg[n]["iletilemedi"] for n in ta_names], textposition='outside',
                    ))
                    fig_alici.add_trace(go.Bar(
                        y=ta_names, x=[alici_agg[n]["okundu"] for n in ta_names],
                        name="Okundu", orientation='h', marker_color=SC_COLORS[0],
                        text=[alici_agg[n]["okundu"] for n in ta_names], textposition='outside',
                    ))
                    fig_alici.add_trace(go.Bar(
                        y=ta_names, x=[alici_agg[n]["cevap"] for n in ta_names],
                        name="Cevaplandi", orientation='h', marker_color=SC_COLORS[2],
                        text=[alici_agg[n]["cevap"] for n in ta_names], textposition='outside',
                    ))
                    fig_alici.update_layout(
                        barmode='group',
                        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
                    )
                    sc_bar(fig_alici, height=max(300, len(top_alici) * 36), horizontal=True)
                    st.plotly_chart(fig_alici, use_container_width=True, key="ch_alici_bar", config=SC_CHART_CFG)

                # Detay tablosu
                styled_section("Mesaj Detay Tablosu", "#2563eb")
                rapor_rows = []
                for m in messages:
                    m_alici = m.get("alicilar", [])
                    rapor_rows.append({
                        "Tarih": m.get("created_at", "")[:16].replace("T", " "),
                        "Kanal": _KANAL_MAP.get(m.get("kanal", ""), {}).get("label", ""),
                        "Konu": m.get("konu", ""),
                        "Şablon": sablon_map.get(m.get("sablon", ""), ""),
                        "Alici Tipi": m.get("alici_tipi", ""),
                        "Toplam": len(m_alici),
                        "İletildi": sum(1 for a in m_alici if a.get("durum") == "iletildi"),
                        "Okundu": sum(1 for a in m_alici if a.get("okundu")),
                        "Cevap": sum(1 for a in m_alici if a.get("cevap")),
                    })
                df_rapor = pd.DataFrame(rapor_rows)
                st.dataframe(df_rapor, use_container_width=True, hide_index=True)

                # Indir
                st.markdown("")
                rc1, rc2 = st.columns(2)
                with rc1:
                    csv_rapor = df_rapor.to_csv(index=False).encode("utf-8-sig")
                    st.download_button("Rapor CSV Indir", data=csv_rapor,
                                         file_name=f"iletisim_raporu_{datetime.now().strftime('%Y%m%d')}.csv",
                                         mime="text/csv", key="msg_dl_csv")
                with rc2:
                    json_rapor = json.dumps(messages, ensure_ascii=False, indent=2).encode("utf-8")
                    st.download_button("Tüm Veriler JSON Indir", data=json_rapor,
                                         file_name=f"iletisim_verileri_{datetime.now().strftime('%Y%m%d')}.json",
                                         mime="application/json", key="msg_dl_json")

                # ---- Performans Karsilastirma ----
                try:
                    from utils.report_utils import (ai_recommendations_html, period_comparison_row_html,
                                                     generate_module_pdf, render_pdf_download_button,
                                                     render_report_kunye_html, ReportStyler)
                    from datetime import timedelta as _td_koi
                    _now_koi = datetime.now()
                    _cur_month_koi = _now_koi.strftime("%Y-%m")
                    _prev_month_koi = (_now_koi.replace(day=1) - _td_koi(days=1)).strftime("%Y-%m")

                    st.markdown(ReportStyler.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

                    # Monthly iletisim count
                    cur_msg = sum(1 for m in messages if str(m.get("created_at", "")).startswith(_cur_month_koi))
                    prev_msg = sum(1 for m in messages if str(m.get("created_at", "")).startswith(_prev_month_koi))

                    # Monthly duyuru count (sablon=duyuru)
                    cur_duyuru = sum(1 for m in messages if str(m.get("created_at", "")).startswith(_cur_month_koi) and m.get("sablon") == "duyuru")
                    prev_duyuru = sum(1 for m in messages if str(m.get("created_at", "")).startswith(_prev_month_koi) and m.get("sablon") == "duyuru")

                    # Monthly document/alici count
                    cur_alici = sum(len(m.get("alicilar", [])) for m in messages if str(m.get("created_at", "")).startswith(_cur_month_koi))
                    prev_alici = sum(len(m.get("alicilar", [])) for m in messages if str(m.get("created_at", "")).startswith(_prev_month_koi))

                    koi_comparisons = [
                        {"label": "İletişim Sayısı", "current": cur_msg, "previous": prev_msg},
                        {"label": "Duyuru Sayısı", "current": cur_duyuru, "previous": prev_duyuru},
                        {"label": "Toplam Alici", "current": cur_alici, "previous": prev_alici},
                    ]
                    st.markdown(period_comparison_row_html(koi_comparisons), unsafe_allow_html=True)

                    # ---- AI Onerileri ----
                    koi_insights = []
                    total_msg_koi = len(messages)
                    if total_iletilemedi > total_alici * 0.1:
                        koi_insights.append({
                            "icon": "⚠️", "title": "Iletim Başarısızlik Orani Yuksek",
                            "text": f"Mesajlarin %{int(total_iletilemedi / max(total_alici, 1) * 100)}'i iletilemedi. İletişim bilgilerini guncelleyin.",
                            "color": "#ef4444"
                        })
                    if okunma_oran < 50:
                        koi_insights.append({
                            "icon": "👁️", "title": "Dusuk Okunma Orani",
                            "text": f"Okunma orani %{okunma_oran}. Mesaj basliklarini daha dikkat cekici hale getirin.",
                            "color": "#f59e0b"
                        })
                    if cevap_oran < 20:
                        koi_insights.append({
                            "icon": "💬", "title": "Dusuk Cevap Orani",
                            "text": f"Cevap orani %{cevap_oran}. Etkileşimli mesaj sablonlari kullanmayi deneyin.",
                            "color": "#8b5cf6"
                        })
                    koi_insights.append({
                        "icon": "📋", "title": "İletişim Kanalı Optimizasyonu",
                        "text": "Farkli kanallardaki erisim oranlarini karsilastirin ve en etkili kanali onceliklendirin.",
                        "color": "#2563eb"
                    })
                    koi_insights.append({
                        "icon": "🔄", "title": "Periyodik Güncelleme",
                        "text": "İletişim bilgileri duzenli olarak guncellenmelidir. Gecersiz numaralari ve e-postalari temizleyin.",
                        "color": "#0d9488"
                    })

                    st.markdown(ai_recommendations_html(koi_insights), unsafe_allow_html=True)

                    # ---- Kurumsal Kunye ----
                    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

                    # ---- PDF Export ----
                    st.markdown(ReportStyler.section_divider_html("PDF Rapor", "#1e40af"), unsafe_allow_html=True)
                    if st.button("📥 KOI İletişim Raporu (PDF)", key="koi_pdf_btn", use_container_width=True):
                        koi_pdf_sections = [
                            {
                                "title": "İletişim Özet İstatistikleri",
                                "metrics": [
                                    ("Toplam Mesaj", total_msg_koi, "#2563eb"),
                                    ("Iletim Orani", f"%{iletim_oran}", "#10b981"),
                                    ("Okunma Orani", f"%{okunma_oran}", "#8b5cf6"),
                                    ("Cevap Orani", f"%{cevap_oran}", "#f59e0b"),
                                ],
                                "text": f"Bu ay {cur_msg} mesaj gonderildi, {cur_alici} aliciya ulasildi.",
                            },
                            {
                                "title": "Mesaj Detay Tablosu",
                                "table": df_rapor,
                                "table_color": "#1a237e",
                            },
                        ]
                        koi_pdf_bytes = generate_module_pdf("KOI İletişim Raporu", koi_pdf_sections)
                        render_pdf_download_button(koi_pdf_bytes, "koi_iletisim_raporu.pdf", "KOI İletişim Raporu", "koi_dl")
                except Exception as _koi_err:
                    st.caption(f"Rapor bilesenleri yuklenemedi: {_koi_err}")

            else:
                st.markdown("""<div style="background:#111827;border:2px dashed #e2e8f0;
                border-radius:16px;padding:40px;text-align:center;margin:20px 0">
                <div style="font-size:3rem;margin-bottom:12px">📊</div>
                <div style="font-size:1.1rem;font-weight:600;color:#475569">
                Raporlar için en az bir mesaj gonderin</div>
                </div>""", unsafe_allow_html=True)

        # ---------- AYARLAR ----------
        with msg_sub4:
            styled_section("İletişim Kanalları", "#1a237e")
            for ko in KANAL_OPTIONS:
                k_id, k_label, k_color = ko
                st.markdown(
                    f'<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:12px;'
                    f'padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:14px;'
                    f'border-left:4px solid {k_color}">'
                    f'<div style="background:{k_color};color:white;padding:8px 14px;border-radius:10px;'
                    f'font-weight:700;font-size:0.85rem;min-width:130px;text-align:center">{k_label}</div>'
                    f'<div style="font-size:0.82rem;color:#475569">'
                    + ("SmartCampus AI dahili bildirim sistemi. Kullanıcılara platform uzerinden anlik bildirim gonderir."
                       if k_id == "panel" else
                       "Kisa mesaj servisi ile cep telefonuna mesaj gonderir."
                       if k_id == "sms" else
                       "WhatsApp uzerinden mesaj gonderir."
                       if k_id == "whatsapp" else
                       "E-posta ile mesaj gonderir.")
                    + '</div></div>',
                    unsafe_allow_html=True
                )

            styled_section("Mesaj Şablonları", "#8b5cf6")
            for si, (s_id, s_label) in enumerate(SABLON_TIPLERI):
                icerik_on = SABLON_ICERIK.get(s_id, "")
                preview = icerik_on[:80].replace("\n", " ") + "..." if len(icerik_on) > 80 else icerik_on.replace("\n", " ")
                if not preview:
                    preview = "Serbest format - kullanici icerik yazar"
                st.markdown(
                    f'<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:10px;'
                    f'padding:10px 14px;margin-bottom:6px;display:flex;align-items:center;gap:12px">'
                    f'<span style="background:#1e293b;color:#93c5fd;padding:4px 12px;border-radius:8px;'
                    f'font-size:12px;font-weight:600;min-width:140px;text-align:center">{s_label}</span>'
                    f'<span style="font-size:0.78rem;color:#94a3b8">{preview}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            styled_section("Alici Gruplari", "#059669")
            aygr1, aygr2 = st.columns(2)
            with aygr1:
                st.markdown(
                    '<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:12px;'
                    'padding:16px;border-top:3px solid #2563eb">'
                    '<div style="font-weight:700;color:#0B0F19;margin-bottom:8px;font-size:0.9rem">'
                    'Kurum Ici</div>'
                    '<div style="font-size:0.82rem;color:#94a3b8;line-height:1.8">'
                    + "".join(
                        f'<div style="display:flex;align-items:center;gap:6px">'
                        f'<span style="width:8px;height:8px;border-radius:50%;'
                        f'background:{_CAT_MAP.get(g[0], _CAT_MAP["diger"])["color"]}"></span>'
                        f'{g[1]}</div>'
                        for g in KURUM_ICI_GRUPLAR
                    )
                    + '</div></div>',
                    unsafe_allow_html=True
                )
            with aygr2:
                st.markdown(
                    '<div style="background:#0f172a; color:#e2e8f0;border:1px solid #334155;border-radius:12px;'
                    'padding:16px;border-top:3px solid #f59e0b">'
                    '<div style="font-weight:700;color:#0B0F19;margin-bottom:8px;font-size:0.9rem">'
                    'Kurum Disi</div>'
                    '<div style="font-size:0.82rem;color:#94a3b8;line-height:1.8">'
                    '<div>Sınıf / Şube bazli veli secimi</div>'
                    '<div>Kademe bazli veli secimi (İlkokul/Ortaokul/Lise)</div>'
                    '<div>Bireysel veli secimi</div>'
                    '<div>Tüm veliler</div>'
                    '<div>Tanitim amacli (manuel liste)</div>'
                    '</div></div>',
                    unsafe_allow_html=True
                )

        # ---------- PANEL MESAJLARI ----------
        with msg_panel:
            _render_panel_mesajlari()

    # ==================== SIKAYET / ONERI ====================
    with tab_sikayet:
        _render_sikayet_oneri()

    # ==================== SERTIFIKALAR ====================
    with tab_sert:
        _render_sertifikalar()

    # ==================== SWOT ANALIZI ====================
    with tab_swot:
        render_swot_analizi()

    # ==================== VELI MEMNUNIYET ANKETI ====================
    with tab_anket:
        render_veli_memnuniyet()

    # ==================== KURUMSAL KARNE ====================
    with tab_karne:
        try:
            from views._kim_zirve import render_kurumsal_karne
            render_kurumsal_karne()
        except Exception as _e:
            st.error(f"Kurumsal Karne yüklenemedi: {_e}")

    # ==================== PERSONEL KIMLIK KARTI ====================
    with tab_kimlik:
        try:
            from views._kim_zirve import render_personel_kimlik
            render_personel_kimlik()
        except Exception as _e:
            st.error(f"Kimlik Kartı yüklenemedi: {_e}")

    # ==================== YILLIK FAALİYET RAPORU ====================
    with tab_faaliyet:
        try:
            from views._kim_zirve import render_faaliyet_raporu
            render_faaliyet_raporu()
        except Exception as _e:
            st.error(f"Faaliyet Raporu yüklenemedi: {_e}")

    # ==================== PAYDAŞ 360° CRM ====================
    with tab_crm:
        try:
            from views._kim_mega import render_paydas_crm
            render_paydas_crm()
        except Exception as _e:
            st.error(f"360° CRM yüklenemedi: {_e}")

    # ==================== KURUM HAFIZASI ====================
    with tab_hafiza:
        try:
            from views._kim_mega import render_kurum_hafizasi
            render_kurum_hafizasi()
        except Exception as _e:
            st.error(f"Kurum Hafızası yüklenemedi: {_e}")

    # ==================== OKR TAKİP ====================
    with tab_okr:
        try:
            from views._kim_mega import render_okr_takip
            render_okr_takip()
        except Exception as _e:
            st.error(f"OKR Takip yüklenemedi: {_e}")

    # ==================== İTİBAR ENDEKSİ ====================
    with tab_itibar:
        try:
            from views._kim_ultra import render_itibar_endeksi
            render_itibar_endeksi()
        except Exception as _e:
            st.error(f"İtibar Endeksi yüklenemedi: {_e}")

    # ==================== SENARYO SİMÜLATÖRÜ ====================
    with tab_senaryo:
        try:
            from views._kim_ultra import render_senaryo_simulatoru
            render_senaryo_simulatoru()
        except Exception as _e:
            st.error(f"Senaryo Simülatörü yüklenemedi: {_e}")

    # ==================== ONAY AKIŞI (WORKFLOW) ====================
    with tab_workflow:
        try:
            from views._kim_ultra import render_onay_akisi
            render_onay_akisi()
        except Exception as _e:
            st.error(f"Onay Akışı yüklenemedi: {_e}")

    # ==================== SMARTI ====================
    with tab_smarti:
        def _kim_smarti_context() -> str:
            try:
                profile = load_profile()
                profile_name = profile.get("name", "Belirtilmedi")
                positions = _load_positions()
                pos_count = len(positions)
                staff = load_ik_active_employees()
                staff_count = len(staff)
                return (
                    f"Kurum: {profile_name}. "
                    f"Toplam pozisyon: {pos_count}. "
                    f"Toplam personel: {staff_count}."
                )
            except Exception:
                return "Kurumsal veri yuklenemedi."
        render_smarti_chat("kim_organizational", _kim_smarti_context)


# ===================== KURUM ICI MESAJLASMA =====================

def _render_gelen_mesaj():
    """Kurum ici gelen mesajlar (panel mesajlasma)."""
    from utils.auth import AuthManager
    user = AuthManager.get_current_user()
    username = user.get("username", "")
    styled_section("Gelen Mesajlar", "#2563eb")

    ak_store = get_akademik_store()
    gelen = ak_store.get_panel_gelen_kutusu(username)
    okunmamis = sum(1 for m in gelen if not m.okundu)
    okunmus = len(gelen) - okunmamis

    styled_stat_row([
        ("Toplam", str(len(gelen)), "#2563eb", "📨"),
        ("Okunmamis", str(okunmamis), "#ef4444", "🔴"),
        ("Okunmus", str(okunmus), "#10b981", "✅"),
    ])

    if not gelen:
        st.info("Gelen kutunuz bos. Henuz mesaj almadınız.")
        return

    # Filtreler
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_kat = st.selectbox("Kategori", ["Tümü"] + [k[1] for k in MESAJ_KATEGORILERI], key="gm_f_kat")
    with fc2:
        f_okunma = st.selectbox("Durum", ["Tümü", "Okunmamis", "Okunmus"], key="gm_f_okunma")
    with fc3:
        f_gonderici = st.selectbox("Gonderici Tipi", ["Tümü", "Yonetici", "Ogretmen", "Veli", "Calisan"], key="gm_f_tip")

    filtered = list(gelen)
    if f_kat != "Tümü":
        kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == f_kat), "")
        filtered = [m for m in filtered if m.kategori == kat_key]
    if f_okunma == "Okunmamis":
        filtered = [m for m in filtered if not m.okundu]
    elif f_okunma == "Okunmus":
        filtered = [m for m in filtered if m.okundu]
    if f_gonderici != "Tümü":
        f_tip_key = f_gonderici.lower()
        filtered = [m for m in filtered if m.sender_type == f_tip_key]

    st.caption(f"{len(filtered)} mesaj listeleniyor")

    # Mesaj tablosu
    rows_html = ""
    for m in filtered[:100]:
        okundu_badge = ('<span style="background:#1e293b;color:#ef4444;padding:2px 8px;border-radius:6px;'
                        'font-size:10px;font-weight:700;">Yeni</span>' if not m.okundu
                        else '<span style="background:#ecfdf5;color:#10b981;padding:2px 8px;border-radius:6px;'
                             'font-size:10px;">Okundu</span>')
        kat_label = dict(MESAJ_KATEGORILERI).get(m.kategori, m.kategori)
        tarih = m.created_at[:16].replace("T", " ") if m.created_at else "-"
        konu = m.konu[:50] if m.konu else "-"
        font_w = "700" if not m.okundu else "400"
        bg = "#eff6ff" if not m.okundu else "#fff"
        tip_badge = f'<span style="background:#0B0F19;color:#94a3b8;padding:2px 6px;border-radius:4px;font-size:9px;">{m.sender_type.title()}</span>'
        grup_badge = ""
        if m.is_group_message:
            grup_badge = ' <span style="background:#fef3c7;color:#fbbf24;padding:1px 6px;border-radius:4px;font-size:9px;">Grup</span>'

        rows_html += (
            f'<tr style="border-bottom:1px solid #1A2035;background:{bg};">'
            f'<td style="padding:8px 6px;font-size:11px;font-weight:{font_w};">{m.sender_name}{grup_badge}</td>'
            f'<td style="padding:8px 6px;font-size:11px;font-weight:{font_w};">{konu}</td>'
            f'<td style="padding:8px 6px;font-size:11px;">{kat_label}</td>'
            f'<td style="padding:8px 6px;font-size:11px;color:#94a3b8;">{tarih}</td>'
            f'<td style="padding:8px 6px;">{tip_badge}</td>'
            f'<td style="padding:8px 6px;">{okundu_badge}</td>'
            f'</tr>')

    if rows_html:
        st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:linear-gradient(135deg,#0f1d36,#1a2d4a);">
        <th style="padding:8px 6px;text-align:left;color:#93c5fd;font-size:10px;">Gönderen</th>
        <th style="padding:8px 6px;text-align:left;color:#93c5fd;font-size:10px;">Konu</th>
        <th style="padding:8px 6px;text-align:left;color:#93c5fd;font-size:10px;">Kategori</th>
        <th style="padding:8px 6px;text-align:left;color:#93c5fd;font-size:10px;">Tarih</th>
        <th style="padding:8px 6px;text-align:left;color:#93c5fd;font-size:10px;">Tip</th>
        <th style="padding:8px 6px;text-align:left;color:#93c5fd;font-size:10px;">Durum</th>
        </tr></thead><tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)

    # Detay goruntuleme
    st.divider()
    styled_section("Mesaj Detay", "#0d9488")
    secenekler = {}
    for m in filtered:
        lbl = f"{'🔴 ' if not m.okundu else ''}{m.sender_name} | {m.konu[:40]} | {m.created_at[:16]}"
        secenekler[lbl] = m.id
    sec = st.selectbox("Mesaj Seçin", [""] + list(secenekler.keys()), key="gm_detay_sec")
    if sec and sec in secenekler:
        msg_id = secenekler[sec]
        msg = next((m for m in filtered if m.id == msg_id), None)
        if msg:
            # Bilgi karti
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Gönderen:** {msg.sender_name} ({msg.sender_type.title()})")
                st.markdown(f"**Konu:** {msg.konu}")
                st.markdown(f"**Kategori:** {dict(MESAJ_KATEGORILERI).get(msg.kategori, msg.kategori)}")
            with col2:
                st.markdown(f"**Tarih:** {msg.created_at[:16].replace('T', ' ')}")
                st.markdown(f"**Durum:** {'Okundu' if msg.okundu else 'Okunmamis'}")
                if msg.is_group_message:
                    st.markdown(f"**Grup:** {msg.group_target}")

            # Mesaj icerigi
            st.markdown(f"""<div style="background:linear-gradient(135deg,#111827,#1A2035);border-radius:12px;
            padding:16px 20px;margin:12px 0;font-size:13px;color:#94A3B8;border-left:4px solid #2563eb;
            line-height:1.7;">{msg.icerik}</div>""", unsafe_allow_html=True)

            # Butonlar
            bc1, bc2 = st.columns(2)
            with bc1:
                if not msg.okundu:
                    if st.button("Okundu Isaretle", key="gm_okundu_btn", type="primary", use_container_width=True):
                        if msg.is_group_message:
                            ak_store.mark_grup_mesaj_okundu(msg.id, username)
                        else:
                            ak_store.mark_mesaj_okundu(msg.id)
                        st.success("Mesaj okundu olarak isaretlendi!")
                        st.rerun()
                else:
                    st.markdown('<div style="background:#ecfdf5;border-radius:8px;padding:8px 12px;text-align:center;'
                                'color:#059669;font-size:12px;font-weight:600;">✅ Okundu</div>', unsafe_allow_html=True)
            with bc2:
                if st.button("Yanitla", key="gm_yanitla_btn", use_container_width=True):
                    st.session_state["gm_yanitla_id"] = msg.id
                    st.session_state["gm_yanitla_kisi"] = msg.sender_id
                    st.session_state["gm_yanitla_ad"] = msg.sender_name
                    st.session_state["gm_yanitla_tip"] = msg.sender_type
                    st.session_state["gm_yanitla_konu"] = f"Re: {msg.konu}"
                    st.session_state["gm_yanitla_conv"] = msg.conversation_id or msg.id
                    st.rerun()

            # Yanitla formu
            if st.session_state.get("gm_yanitla_id") == msg.id:
                st.divider()
                styled_section("Yanıt Yaz", "#6366f1")

                # Gönderen adı zorunluluğu
                _gm_raw_name = (user.get("name") or "").strip()
                if _gm_raw_name:
                    st.markdown(
                        f'<div style="background:#1e293b;border:1px solid #bbf7d0;border-radius:8px;'
                        f'padding:8px 12px;font-size:0.88rem;color:#86efac;margin-bottom:8px">'
                        f'✅ <b>Yanıtlayan:</b> {_gm_raw_name}'
                        f'<span style="opacity:.65;font-size:.78rem;margin-left:6px">'
                        f'(oturumdan otomatik)</span></div>',
                        unsafe_allow_html=True,
                    )
                    _gm_sender_name = _gm_raw_name
                else:
                    _gm_sender_name = st.text_input(
                        "Adınız Soyadınız *(zorunlu)*",
                        key="gm_yanit_gonderen_adi",
                        placeholder="Ad ve soyadınızı giriniz",
                    )
                    if not _gm_sender_name.strip():
                        st.warning("⚠️ Yanıt göndermek için adınızı ve soyadınızı girmelisiniz.")

                yanit_icerik = st.text_area("Yanıtınız *", key="gm_yanit_icerik", height=100,
                                             placeholder="Yanıtınızı yazın...")
                if st.button("📤 Yanıtı Gönder", key="gm_yanit_gonder", type="primary", use_container_width=True):
                    _yanit_errors = []
                    if not (_gm_sender_name or "").strip():
                        _yanit_errors.append("Gönderen adı soyadı zorunludur.")
                    if not yanit_icerik.strip():
                        _yanit_errors.append("Yanıt içeriği boş olamaz.")
                    if _yanit_errors:
                        for _ye in _yanit_errors:
                            st.error(_ye)
                    else:
                        yanit = VeliMesaj(
                            sender_type=user.get("role", "calisan").lower(),
                            sender_id=username,
                            sender_name=_gm_sender_name.strip(),
                            receiver_type=st.session_state["gm_yanitla_tip"],
                            receiver_id=st.session_state["gm_yanitla_kisi"],
                            receiver_name=st.session_state["gm_yanitla_ad"],
                            konu=st.session_state["gm_yanitla_konu"],
                            icerik=yanit_icerik.strip(),
                            kategori=msg.kategori,
                            parent_message_id=msg.id,
                            conversation_id=st.session_state["gm_yanitla_conv"],
                        )
                        ak_store.save_veli_mesaj(yanit)
                        try:
                            from utils.messaging import send_panel_mesaj_bildirimi
                            send_panel_mesaj_bildirimi(
                                receiver_id=yanit.receiver_id,
                                receiver_type=yanit.receiver_type,
                                receiver_name=yanit.receiver_name,
                                sender_name=yanit.sender_name,
                                konu=yanit.konu,
                                icerik=yanit.icerik,
                            )
                        except Exception:
                            pass
                        for k in ["gm_yanitla_id", "gm_yanitla_kisi", "gm_yanitla_ad",
                                   "gm_yanitla_tip", "gm_yanitla_konu", "gm_yanitla_conv"]:
                            st.session_state.pop(k, None)
                        st.success("Yanıt gönderildi!")
                        st.rerun()


def _render_giden_mesaj():
    """Kurum ici giden mesajlar (panel mesajlasma)."""
    from utils.auth import AuthManager
    user = AuthManager.get_current_user()
    username = user.get("username", "")
    styled_section("Giden Mesajlar", "#8b5cf6")

    ak_store = get_akademik_store()
    giden = ak_store.get_veli_giden_kutusu(username)

    # Grup mesajlarini da ekle
    all_data = ak_store._load(ak_store.veli_mesajlar_file)
    grup_giden = [VeliMesaj.from_dict(item) for item in all_data
                  if item.get("is_group_message") and item.get("sender_id") == username]
    # Tekrar olmasin
    giden_ids = {m.id for m in giden}
    for gm in grup_giden:
        if gm.id not in giden_ids:
            giden.append(gm)
    giden.sort(key=lambda m: m.created_at, reverse=True)

    toplam = len(giden)
    okunan = sum(1 for m in giden if m.okundu)

    styled_stat_row([
        ("Toplam Giden", str(toplam), "#8b5cf6", "📤"),
        ("Okunan", str(okunan), "#10b981", "👁️"),
        ("Okunmayan", str(toplam - okunan), "#f59e0b", "⏳"),
    ])

    if not giden:
        st.info("Henuz mesaj gondermediniz. 'Yeni Mesaj Oluştur' sekmesinden gonderin.")
        return

    # Filtre
    fc1, fc2 = st.columns(2)
    with fc1:
        f_kat = st.selectbox("Kategori", ["Tümü"] + [k[1] for k in MESAJ_KATEGORILERI], key="gdm_f_kat")
    with fc2:
        f_tip = st.selectbox("Mesaj Tipi", ["Tümü", "Birebir", "Grup"], key="gdm_f_tip")

    filtered = list(giden)
    if f_kat != "Tümü":
        kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == f_kat), "")
        filtered = [m for m in filtered if m.kategori == kat_key]
    if f_tip == "Birebir":
        filtered = [m for m in filtered if not m.is_group_message]
    elif f_tip == "Grup":
        filtered = [m for m in filtered if m.is_group_message]

    st.caption(f"{len(filtered)} mesaj listeleniyor")

    # Tablo
    rows_html = ""
    for m in filtered[:100]:
        kat_label = dict(MESAJ_KATEGORILERI).get(m.kategori, m.kategori)
        tarih = m.created_at[:16].replace("T", " ") if m.created_at else "-"
        konu = m.konu[:50] if m.konu else "-"
        alici_ad = m.receiver_name if not m.is_group_message else f"Grup: {m.group_target}"
        okundu_badge = ('<span style="background:#ecfdf5;color:#10b981;padding:2px 6px;border-radius:4px;'
                        'font-size:9px;font-weight:600;">Okundu</span>' if m.okundu
                        else '<span style="background:#fef3c7;color:#fbbf24;padding:2px 6px;border-radius:4px;'
                             'font-size:9px;">Bekliyor</span>')
        tip_badge = ""
        if m.is_group_message:
            tip_badge = '<span style="background:#ede9fe;color:#7c3aed;padding:2px 6px;border-radius:4px;font-size:9px;font-weight:600;">Grup</span>'

        rows_html += (
            f'<tr style="border-bottom:1px solid #1A2035;">'
            f'<td style="padding:8px 6px;font-size:11px;font-weight:600;">{alici_ad}</td>'
            f'<td style="padding:8px 6px;font-size:11px;">{konu}</td>'
            f'<td style="padding:8px 6px;font-size:11px;">{kat_label}</td>'
            f'<td style="padding:8px 6px;font-size:11px;color:#94a3b8;">{tarih}</td>'
            f'<td style="padding:8px 6px;">{okundu_badge}</td>'
            f'<td style="padding:8px 6px;">{tip_badge}</td>'
            f'</tr>')

    if rows_html:
        st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);">
        <th style="padding:8px 6px;text-align:left;color:#5b21b6;font-size:10px;">Alici</th>
        <th style="padding:8px 6px;text-align:left;color:#5b21b6;font-size:10px;">Konu</th>
        <th style="padding:8px 6px;text-align:left;color:#5b21b6;font-size:10px;">Kategori</th>
        <th style="padding:8px 6px;text-align:left;color:#5b21b6;font-size:10px;">Tarih</th>
        <th style="padding:8px 6px;text-align:left;color:#5b21b6;font-size:10px;">Durum</th>
        <th style="padding:8px 6px;text-align:left;color:#5b21b6;font-size:10px;">Tip</th>
        </tr></thead><tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)

    # Detay
    st.divider()
    styled_section("Mesaj Detay", "#6366f1")
    sec_map = {}
    for m in filtered:
        alici = m.receiver_name if not m.is_group_message else f"Grup: {m.group_target}"
        lbl = f"{alici} | {m.konu[:40]} | {m.created_at[:16]}"
        sec_map[lbl] = m.id
    sec = st.selectbox("Mesaj Seçin", [""] + list(sec_map.keys()), key="gdm_detay_sec")
    if sec and sec in sec_map:
        msg_id = sec_map[sec]
        msg = next((m for m in filtered if m.id == msg_id), None)
        if msg:
            col1, col2 = st.columns(2)
            with col1:
                if msg.is_group_message:
                    st.markdown(f"**Alici:** Grup — {msg.group_target}")
                    st.markdown(f"**Alici Sayisi:** {len(msg.group_recipients)}")
                else:
                    st.markdown(f"**Alici:** {msg.receiver_name} ({msg.receiver_type.title()})")
                st.markdown(f"**Konu:** {msg.konu}")
            with col2:
                st.markdown(f"**Kategori:** {dict(MESAJ_KATEGORILERI).get(msg.kategori, msg.kategori)}")
                st.markdown(f"**Tarih:** {msg.created_at[:16].replace('T', ' ')}")
                st.markdown(f"**Durum:** {'Okundu' if msg.okundu else 'Okunmadi'}")

            st.markdown(f"""<div style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:12px;
            padding:16px 20px;margin:12px 0;font-size:13px;color:#94A3B8;border-left:4px solid #8b5cf6;
            line-height:1.7;">{msg.icerik}</div>""", unsafe_allow_html=True)


def _render_yeni_mesaj_olustur():
    """Kurum ici yeni mesaj olusturma (panel mesajlasma)."""
    from utils.auth import AuthManager
    user = AuthManager.get_current_user()
    username = user.get("username", "")
    _raw_name = (user.get("name") or "").strip()
    user_role = user.get("role", "Calisan").lower()
    styled_section("Yeni Mesaj Oluştur", "#10b981")

    # ── Gönderen adı zorunluluğu ──────────────────────────────────────────
    if _raw_name:
        st.markdown(
            f'<div style="background:#1e293b;border:1px solid #bbf7d0;border-radius:10px;'
            f'padding:10px 14px;margin-bottom:12px;font-size:0.9rem;color:#86efac">'
            f'✅ <b>Gönderen:</b> {_raw_name}'
            f'<span style="opacity:.65;font-size:.78rem;margin-left:8px">'
            f'(oturumdan otomatik alındı)</span></div>',
            unsafe_allow_html=True,
        )
        user_name = _raw_name
    else:
        st.markdown(
            '<div style="background:#1e293b;border:1px solid #fecaca;border-radius:10px;'
            'padding:10px 14px;margin-bottom:12px;font-size:0.88rem;color:#7f1d1d">'
            '⚠️ Hesabınızda ad/soyad bilgisi bulunamadı. '
            'Mesaj göndermek için adınızı ve soyadınızı girmeniz zorunludur.</div>',
            unsafe_allow_html=True,
        )
        user_name = st.text_input(
            "Adınız Soyadınız *(zorunlu)*",
            key="ym_gonderen_adi",
            placeholder="Ad ve soyadınızı eksiksiz giriniz",
        )

    st.markdown("""<div style="background:linear-gradient(135deg,#0f2a1f,#1a3a2a);border-radius:10px;
    padding:12px 16px;margin-bottom:16px;font-size:12px;color:#86efac;border-left:4px solid #10b981;">
    ✉️ Kurum ici kullanicilara birebir veya grup mesaj gonderin.
    Mesajlar alicinin Gelen Mesaj kutusuna aninda duser.
    </div>""", unsafe_allow_html=True)

    ak_store = get_akademik_store()

    # Mesaj tipi
    mesaj_tipi = st.radio("Mesaj Tipi", ["Birebir", "Grup"], horizontal=True, key="ym_tipi")

    if mesaj_tipi == "Birebir":
        # Alici turu secimi
        alici_turu = st.radio(
            "Alıcı Türü", ["Personel (IK)", "Öğrenci", "Veli"],
            horizontal=True, key="ym_alici_turu")

        alici_secenekleri: dict[str, str] = {}

        if alici_turu == "Personel (IK)":
            # IK Modulu Aktif Calisanlar
            _ym_employees = load_ik_active_employees()
            for e in sorted(_ym_employees, key=lambda x: f"{x.get('ad', '')} {x.get('soyad', '')}"):
                _ym_ad = f"{e.get('ad', '')} {e.get('soyad', '')}".strip()
                if not _ym_ad:
                    continue
                _ym_pos = e.get("position_name", "")
                _ym_label = f"{_ym_ad} - {_ym_pos}" if _ym_pos else _ym_ad
                # IK employee id'sini alici olarak kullan
                _ym_eid = e.get("id", _ym_ad)
                alici_secenekleri[_ym_label] = _ym_eid

        elif alici_turu == "Öğrenci":
            # Sinif Listeleri'nden ogrenci
            _ym_ss = get_sinif_sube_listesi()
            _ym_siniflar = _ym_ss.get("siniflar", [])
            _ym_ss_list = _ym_ss.get("sinif_sube", [])
            _ym_c1, _ym_c2 = st.columns(2)
            with _ym_c1:
                _ym_sinif = st.selectbox("Sınıf", ["Tümü"] + _ym_siniflar, key="ym_ogr_sinif")
            with _ym_c2:
                _ym_subeler: list[str] = []
                if _ym_sinif != "Tümü":
                    _ym_subeler = sorted(set(
                        ss.split("/")[1] for ss in _ym_ss_list if ss.startswith(f"{_ym_sinif}/")))
                _ym_sube = st.selectbox("Şube", ["Tümü"] + _ym_subeler, key="ym_ogr_sube")

            _ym_students = load_shared_students()
            if _ym_sinif != "Tümü":
                _ym_students = [s for s in _ym_students if str(s.get("sinif", "")) == _ym_sinif]
            if _ym_sube != "Tümü":
                _ym_students = [s for s in _ym_students if s.get("sube", "") == _ym_sube]

            for s in sorted(_ym_students, key=lambda x: (str(x.get("sinif", "")), x.get("sube", ""), x.get("soyad", ""))):
                _s_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                if not _s_ad:
                    continue
                _s_sinif = s.get("sinif", "")
                _s_sube = s.get("sube", "")
                _s_label = f"{_s_ad} - {_s_sinif}/{_s_sube}"
                alici_secenekleri[_s_label] = s.get("id", _s_ad)

        else:  # Veli
            # Sinif Listeleri'ndeki ogrenci kayitlarindan veli bilgileri
            _ym_ss = get_sinif_sube_listesi()
            _ym_siniflar = _ym_ss.get("siniflar", [])
            _ym_ss_list = _ym_ss.get("sinif_sube", [])
            _ym_c1, _ym_c2 = st.columns(2)
            with _ym_c1:
                _ym_sinif = st.selectbox("Sınıf", ["Tümü"] + _ym_siniflar, key="ym_veli_sinif")
            with _ym_c2:
                _ym_subeler_v: list[str] = []
                if _ym_sinif != "Tümü":
                    _ym_subeler_v = sorted(set(
                        ss.split("/")[1] for ss in _ym_ss_list if ss.startswith(f"{_ym_sinif}/")))
                _ym_sube = st.selectbox("Şube", ["Tümü"] + _ym_subeler_v, key="ym_veli_sube")

            _ym_students = load_shared_students()
            if _ym_sinif != "Tümü":
                _ym_students = [s for s in _ym_students if str(s.get("sinif", "")) == _ym_sinif]
            if _ym_sube != "Tümü":
                _ym_students = [s for s in _ym_students if s.get("sube", "") == _ym_sube]

            for s in sorted(_ym_students, key=lambda x: (str(x.get("sinif", "")), x.get("sube", ""), x.get("soyad", ""))):
                _v_ad = s.get("veli_adi", "")
                if not _v_ad:
                    _v_ad = f'{s.get("anne_adi", "")} {s.get("anne_soyadi", "")}'.strip()
                if not _v_ad:
                    _v_ad = f'{s.get("baba_adi", "")} {s.get("baba_soyadi", "")}'.strip()
                if not _v_ad:
                    continue
                _ogr_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                _s_sinif = s.get("sinif", "")
                _s_sube = s.get("sube", "")
                _v_label = f"{_v_ad} (Velisi: {_ogr_ad} - {_s_sinif}/{_s_sube})"
                alici_secenekleri[_v_label] = s.get("id", _v_ad)

        alici_label = st.selectbox("Alıcı *", [""] + list(alici_secenekleri.keys()), key="ym_alici")
    else:
        # Grup secimi
        grup_secenekleri = [
            ("tum_ogretmenler", "Tüm Ogretmenler"),
            ("tum_veliler", "Tüm Veliler"),
            ("tum_yoneticiler", "Tüm Yoneticiler"),
            ("tum_calisanlar", "Tüm Calisanlar"),
            ("tum_kullanicilar", "Tüm Kullanicilar"),
        ]
        grup_label = st.selectbox("Grup *", [g[1] for g in grup_secenekleri], key="ym_grup")
        grup_key = next((g[0] for g in grup_secenekleri if g[1] == grup_label), "tum_kullanicilar")

    with st.form("ym_form"):
        konu = st.text_input("Konu *", key="ym_konu")
        kategori_label = st.selectbox("Kategori", [k[1] for k in MESAJ_KATEGORILERI], key="ym_kat")
        icerik = st.text_area("Mesaj Icerigi *", height=150, key="ym_icerik",
                               placeholder="Mesajinizi buraya yazin...")
        submitted = st.form_submit_button("Gonder", use_container_width=True, type="primary")

    if submitted:
        _errors = []
        if not (user_name or "").strip():
            _errors.append("⚠️ Gönderen adı soyadı zorunludur — lütfen adınızı ve soyadınızı girin.")
        if not konu or not konu.strip():
            _errors.append("Konu alanı zorunludur.")
        if not icerik.strip():
            _errors.append("Mesaj içeriği boş olamaz.")
        if _errors:
            for _e in _errors:
                st.error(_e)
            return

        kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == kategori_label), "genel")

        if mesaj_tipi == "Birebir":
            if not alici_label or alici_label not in alici_secenekleri:
                st.error("Alıcı seçmelisiniz.")
                return
            alici_id = alici_secenekleri[alici_label]
            # Alici adini label'dan cikar
            alici_ad = alici_label.split(" - ")[0].split(" (")[0].strip()
            # Alici rolunu belirle
            _alici_turu_map = {"Personel (IK)": "personel", "Öğrenci": "ogrenci", "Veli": "veli"}
            alici_role = _alici_turu_map.get(alici_turu, "personel")

            mesaj = VeliMesaj(
                sender_type=user_role,
                sender_id=username,
                sender_name=user_name,
                receiver_type=alici_role,
                receiver_id=alici_id,
                receiver_name=alici_ad,
                konu=konu.strip(),
                icerik=icerik.strip(),
                kategori=kat_key,
            )
            mesaj.conversation_id = mesaj.id
            ak_store.save_veli_mesaj(mesaj)
            try:
                from utils.messaging import send_panel_mesaj_bildirimi
                send_panel_mesaj_bildirimi(
                    receiver_id=mesaj.receiver_id,
                    receiver_type=mesaj.receiver_type,
                    receiver_name=mesaj.receiver_name,
                    sender_name=mesaj.sender_name,
                    konu=mesaj.konu,
                    icerik=mesaj.icerik,
                )
            except Exception:
                pass
            st.success(f"Mesaj '{alici_ad}' adlı kişiye gönderildi!")
            st.rerun()
        else:
            # Grup mesaj
            from utils.auth import get_all_users
            tum = get_all_users()
            role_map = {
                "tum_ogretmenler": "Ogretmen",
                "tum_veliler": "Veli",
                "tum_yoneticiler": "Yonetici",
                "tum_calisanlar": "Calisan",
            }
            hedef_role = role_map.get(grup_key, None)
            if hedef_role:
                recipients = [{"id": u["username"], "ad": u["name"], "tip": u["role"]}
                              for u in tum if u.get("role") == hedef_role
                              and u.get("username") != username and u.get("active", True)]
            else:
                recipients = [{"id": u["username"], "ad": u["name"], "tip": u["role"]}
                              for u in tum if u.get("username") != username and u.get("active", True)]

            if not recipients:
                st.warning("Secilen grupta alici bulunamadi.")
                return

            ak_store.send_grup_mesaj(
                sender_type=user_role,
                sender_id=username,
                sender_name=user_name,
                group_target=grup_key,
                recipients=recipients,
                konu=konu.strip(),
                icerik=icerik.strip(),
                kategori=kat_key,
            )
            try:
                from utils.messaging import send_grup_mesaj_bildirimleri
                send_grup_mesaj_bildirimleri(
                    recipients=recipients,
                    sender_name=user_name,
                    konu=konu.strip(),
                    icerik=icerik.strip(),
                )
            except Exception:
                pass
            st.success(f"Grup mesaji {len(recipients)} kişiye gonderildi!")
            st.rerun()


# ===================== SIKAYET ONERI TAKIP RENDER =====================

def _render_sikayet_oneri():
    """Sikayet / Oneri / Talep takip sekmesi."""
    styled_section("Sikayet, Oneri ve Talep Takibi", "#8b5cf6")

    records = _load_sikayetler()

    sub = st.tabs(["📊 Dashboard", "📝 Yeni Kayıt", "🔍 Takip", "📋 Sonuç Ekranı", "📈 İstatistikler ve SLA"])

    # ---- Alt Sekme 1: Dashboard ----
    with sub[0]:
        _render_sikayet_dashboard(records)

    # ---- Alt Sekme 2: Yeni Kayit ----
    with sub[1]:
        _render_sikayet_yeni()

    # ---- Alt Sekme 3: Takip (aktif kayitlar) ----
    with sub[2]:
        _render_sikayet_takip(records)

    # ---- Alt Sekme 4: Sonuc Ekrani ----
    with sub[3]:
        _render_sikayet_sonuc(records)

    # ---- Alt Sekme 5: Istatistikler ----
    with sub[4]:
        _render_sikayet_istatistik(records)


def _render_sikayet_dashboard(records: list[dict]):
    """Sikayet/Oneri/Talep ozet dashboard."""
    # Istatistik hesaplamalari
    toplam = len(records)
    kayit_alindi = sum(1 for r in records if r.get("durum") == "kayit_alindi")
    surecte = sum(1 for r in records if r.get("durum") in ("bilgilendirme", "degerlendirme", "inceleme", "aksiyon_planlandi", "uygulamada"))
    cozulen = sum(1 for r in records if r.get("durum") in ("cozumlendi", "kismen_cozumlendi", "kapandi"))
    cozulemedi = sum(1 for r in records if r.get("durum") in ("cozulemedi", "reddedildi"))
    sla_ihlal = 0
    for r in records:
        sla = _hesapla_sla_durumu(r)
        if sla["donus_durum"] == "gecikti" or sla["cozum_durum"] == "gecikti":
            sla_ihlal += 1

    styled_stat_row([
        ("Toplam", str(toplam), "#2563eb", "📋"),
        ("Kayit Alindi", str(kayit_alindi), "#3b82f6", "🆕"),
        ("Süreçte", str(surecte), "#f59e0b", "🔄"),
        ("Çözülen", str(cozulen), "#10b981", "✅"),
    ])
    styled_stat_row([
        ("Çözülemedi/Red", str(cozulemedi), "#ef4444", "❌"),
        ("SLA Ihlali", str(sla_ihlal), "#dc2626", "⏰"),
        ("Çözüm Orani", f"%{round(cozulen / toplam * 100) if toplam else 0}", "#059669", "📊"),
        ("Aktif Takip", str(kayit_alindi + surecte), "#8b5cf6", "📌"),
    ])

    # --- Acil Ilgilenilmesi Gerekenler ---
    acil_kayitlar = [r for r in records
                     if r.get("durum") in _TAKIP_DURUMLARI
                     and r.get("oncelik") in ("acil", "yuksek")]
    sla_ihlal_kayitlar = []
    for r in records:
        if r.get("durum") in _TAKIP_DURUMLARI:
            sla = _hesapla_sla_durumu(r)
            if sla["donus_durum"] == "gecikti" or sla["cozum_durum"] == "gecikti":
                sla_ihlal_kayitlar.append(r)

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        styled_section("Acil / Yuksek Oncelikli Aktif Kayitlar", "#ef4444")
        if acil_kayitlar:
            for r in acil_kayitlar[:10]:
                onc = r.get("oncelik", "normal")
                onc_renk = "#ef4444" if onc == "acil" else "#f59e0b"
                onc_label = "ACİL" if onc == "acil" else "YUKSEK"
                tur_label = dict(SIKAYET_TUR).get(r.get("tur", ""), "")
                durum_label = _SIKAYET_DURUM_MAP.get(r.get("durum", ""), "")
                ts = r.get("kayit_tarih_saat", "")[:10]
                st.markdown(
                    f'<div style="background:#0f172a; color:#e2e8f0;border:1px solid #fee2e2;border-left:4px solid {onc_renk};'
                    f'border-radius:8px;padding:10px 14px;margin-bottom:6px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-size:12px;font-weight:700;color:#94A3B8;">{r.get("konu", "")[:45]}</span>'
                    f'<span style="background:{onc_renk}15;color:{onc_renk};padding:2px 8px;border-radius:6px;'
                    f'font-size:9px;font-weight:700;">{onc_label}</span></div>'
                    f'<div style="font-size:10px;color:#94a3b8;margin-top:4px;">'
                    f'{tur_label} | {durum_label} | {r.get("bildiren_adi", "-")} | {ts}</div>'
                    f'</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#ecfdf5;border-radius:10px;padding:16px;text-align:center;'
                        'color:#059669;font-size:12px;">Acil veya yuksek oncelikli aktif kayit yok.</div>',
                        unsafe_allow_html=True)

    with col_d2:
        styled_section("SLA Ihlali Olan Kayitlar", "#dc2626")
        if sla_ihlal_kayitlar:
            for r in sla_ihlal_kayitlar[:10]:
                sla = _hesapla_sla_durumu(r)
                geciken = "Donus" if sla["donus_durum"] == "gecikti" else "Cozum"
                tur_label = dict(SIKAYET_TUR).get(r.get("tur", ""), "")
                ts = r.get("kayit_tarih_saat", "")[:10]
                st.markdown(
                    f'<div style="background:#0f172a; color:#e2e8f0;border:1px solid #fef2f2;border-left:4px solid #dc2626;'
                    f'border-radius:8px;padding:10px 14px;margin-bottom:6px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-size:12px;font-weight:700;color:#94A3B8;">{r.get("konu", "")[:45]}</span>'
                    f'<span style="background:#1e293b;color:#ef4444;padding:2px 8px;border-radius:6px;'
                    f'font-size:9px;font-weight:700;">{geciken} GECIKTI</span></div>'
                    f'<div style="font-size:10px;color:#94a3b8;margin-top:4px;">'
                    f'{tur_label} | {r.get("bildiren_adi", "-")} | {ts}</div>'
                    f'</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#ecfdf5;border-radius:10px;padding:16px;text-align:center;'
                        'color:#059669;font-size:12px;">SLA ihlali olan kayit yok.</div>',
                        unsafe_allow_html=True)

    # --- Son Eklenen Kayitlar ---
    st.markdown("")
    styled_section("Son Eklenen Kayitlar", "#2563eb")
    son_kayitlar = sorted(records, key=lambda r: r.get("kayit_tarih_saat", r.get("created_at", "")), reverse=True)[:8]
    if son_kayitlar:
        rows = ""
        for r in son_kayitlar:
            tur_label = dict(SIKAYET_TUR).get(r.get("tur", ""), "")
            d_key = r.get("durum", "kayit_alindi")
            d_label = _SIKAYET_DURUM_MAP.get(d_key, d_key)
            d_renk = _SIKAYET_DURUM_RENK.get(d_key, "#64748b")
            onc_key = r.get("oncelik", "normal")
            onc_renk = _SIKAYET_ONC_RENK.get(onc_key, "#3b82f6")
            ts = r.get("kayit_tarih_saat", "")[:16].replace("T", " ") if r.get("kayit_tarih_saat") else "-"
            rows += (
                f'<tr style="border-bottom:1px solid #1A2035;">'
                f'<td style="padding:6px;font-size:11px;color:#94a3b8;">{ts}</td>'
                f'<td style="padding:6px;font-size:11px;font-weight:600;">{tur_label}</td>'
                f'<td style="padding:6px;font-size:11px;">{r.get("konu", "")[:40]}</td>'
                f'<td style="padding:6px;font-size:11px;">{r.get("bildiren_adi", "-")}</td>'
                f'<td style="padding:6px;"><span style="background:{onc_renk}15;color:{onc_renk};'
                f'padding:2px 6px;border-radius:4px;font-size:9px;font-weight:600;">{onc_key.title()}</span></td>'
                f'<td style="padding:6px;"><span style="background:{d_renk}15;color:{d_renk};'
                f'padding:2px 8px;border-radius:6px;font-size:10px;font-weight:700;">{d_label}</span></td>'
                f'</tr>')
        st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">
        <thead><tr style="background:linear-gradient(135deg,#111827,#eef2ff);">
        <th style="padding:6px;text-align:left;color:#94a3b8;font-size:10px;">Tarih</th>
        <th style="padding:6px;text-align:left;color:#94a3b8;font-size:10px;">Tür</th>
        <th style="padding:6px;text-align:left;color:#94a3b8;font-size:10px;">Konu</th>
        <th style="padding:6px;text-align:left;color:#94a3b8;font-size:10px;">Bildiren</th>
        <th style="padding:6px;text-align:left;color:#94a3b8;font-size:10px;">Öncelik</th>
        <th style="padding:6px;text-align:left;color:#94a3b8;font-size:10px;">Durum</th>
        </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)
    else:
        st.info("Henuz kayit bulunmuyor.")

    # --- SLA Kriterleri (compact) ---
    st.markdown("")
    st.markdown("""<div style="background:linear-gradient(135deg,#2a1f0f,#3a2a1a);border-radius:10px;padding:12px 16px;font-size:11px;color:#fbbf24;">
    <b>SLA Kriterleri:</b> &nbsp;
    <span style="color:#ef4444;">Acil: 2-4s donus / 24s cozum</span> &nbsp;|&nbsp;
    <span style="color:#f59e0b;">Yuksek: 24s donus / 48s cozum</span> &nbsp;|&nbsp;
    <span style="color:#3b82f6;">Normal: 24s donus / 72s cozum</span> &nbsp;|&nbsp;
    <span style="color:#94a3b8;">Dusuk: 48s donus / 120s cozum</span>
    </div>""", unsafe_allow_html=True)


def _render_sikayet_takip(records: list[dict]):
    """Aktif kayitlarin takibi: filtre + expander bazli detay/güncelle."""
    styled_section("Aktif Kayit Takibi", "#2563eb")

    aktif_records = [r for r in records if r.get("durum", "kayit_alindi") in _TAKIP_DURUMLARI]

    if not aktif_records:
        st.info("Takip edilecek aktif kayit bulunmuyor. 'Yeni Kayıt' sekmesinden ekleyebilirsiniz.")
        return

    # Filtreler (compact)
    aktif_durum_labels = [d[1] for d in SIKAYET_DURUM if d[0] in _TAKIP_DURUMLARI]
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
    with col_f1:
        f_tur = st.selectbox("Tür", ["Tümü"] + [t[1] for t in SIKAYET_TUR], key="so_f_tur")
    with col_f2:
        f_durum = st.selectbox("Durum", ["Tümü"] + aktif_durum_labels, key="so_f_durum")
    with col_f3:
        f_kat = st.selectbox("Kategori", ["Tümü"] + [k[1] for k in SIKAYET_KATEGORILERI], key="so_f_kat")
    with col_f4:
        f_onc = st.selectbox("Öncelik", ["Tümü"] + [o[1] for o in SIKAYET_ONCELIK], key="so_f_onc")
    with col_f5:
        f_sla = st.selectbox("SLA", ["Tümü", "Zamaninda", "Gecikti", "Bekliyor"], key="so_f_sla")

    filtered = aktif_records[:]
    if f_tur != "Tümü":
        tur_key = next((t[0] for t in SIKAYET_TUR if t[1] == f_tur), "")
        filtered = [r for r in filtered if r.get("tur") == tur_key]
    if f_durum != "Tümü":
        durum_key = next((d[0] for d in SIKAYET_DURUM if d[1] == f_durum), "")
        filtered = [r for r in filtered if r.get("durum") == durum_key]
    if f_kat != "Tümü":
        kat_key = next((k[0] for k in SIKAYET_KATEGORILERI if k[1] == f_kat), "")
        filtered = [r for r in filtered if r.get("kategori") == kat_key]
    if f_onc != "Tümü":
        onc_key = next((o[0] for o in SIKAYET_ONCELIK if o[1] == f_onc), "")
        filtered = [r for r in filtered if r.get("oncelik") == onc_key]
    if f_sla != "Tümü":
        sla_f = []
        for r in filtered:
            sla_info = _hesapla_sla_durumu(r)
            if f_sla == "Gecikti" and (sla_info["donus_durum"] == "gecikti" or sla_info["cozum_durum"] == "gecikti"):
                sla_f.append(r)
            elif f_sla == "Zamaninda" and sla_info["donus_durum"] == "zamaninda" and sla_info["cozum_durum"] in ("zamaninda", "bekliyor"):
                sla_f.append(r)
            elif f_sla == "Bekliyor" and sla_info["donus_durum"] == "bekliyor":
                sla_f.append(r)
        filtered = sla_f

    filtered.sort(key=lambda r: r.get("kayit_tarih_saat", r.get("created_at", "")), reverse=True)
    st.caption(f"{len(filtered)} aktif kayit")

    # --- Her kayit icin expander ---
    ik_calisanlar = get_ik_employee_name_with_position()
    calisan_sec = [""] + ik_calisanlar

    for idx, rec in enumerate(filtered[:50]):
        tur_label = dict(SIKAYET_TUR).get(rec.get("tur", ""), "")
        d_key = rec.get("durum", "kayit_alindi")
        d_label = _SIKAYET_DURUM_MAP.get(d_key, d_key)
        d_renk = _SIKAYET_DURUM_RENK.get(d_key, "#64748b")
        onc_key = rec.get("oncelik", "normal")
        onc_renk = _SIKAYET_ONC_RENK.get(onc_key, "#3b82f6")
        sla_info = _hesapla_sla_durumu(rec)
        sla_icon = "🔴" if sla_info["donus_durum"] == "gecikti" or sla_info["cozum_durum"] == "gecikti" else "🟢" if sla_info["donus_durum"] == "zamaninda" else "🔵"
        ts = rec.get("kayit_tarih_saat", "")[:10]

        exp_title = f"{sla_icon} {onc_key.upper()} | {tur_label} | {rec.get('konu', '')[:45]} | {rec.get('bildiren_adi', '-')} | {ts} | {d_label}"

        with st.expander(exp_title, expanded=False):
            # Bilgi karti
            ci1, ci2, ci3 = st.columns(3)
            with ci1:
                st.markdown(f"**Konu:** {rec.get('konu', '')}")
                st.markdown(f"**Açıklama:** {rec.get('aciklama', '-')}")
                st.markdown(f"**Bildiren:** {rec.get('bildiren_adi', '-')} ({dict(SIKAYET_KAYNAK).get(rec.get('kaynak', ''), '')})")
                st.markdown(f"**İletişim:** {rec.get('bildiren_iletisim', '-')}")
            with ci2:
                kayit_ts = rec.get("kayit_tarih_saat", rec.get("created_at", ""))
                st.markdown(f"**Kayıt Tarihi:** {kayit_ts[:16].replace('T', ' ') if kayit_ts else '-'}")
                st.markdown(f"**Kanal:** {dict(SIKAYET_KANAL).get(rec.get('kanal', ''), '-')}")
                st.markdown(f"**Sikayeti Alan:** {rec.get('sikayeti_alan', '-')}")
                st.markdown(f"**Yönlendirilen:** {rec.get('yonlendirilen_kisi', '-')}")
                if rec.get("konum"):
                    st.markdown(f"**Konum:** {rec['konum']}")
            with ci3:
                sla_lbl = SIKAYET_SLA.get(rec.get("oncelik", "normal"), {}).get("label", "-")
                st.markdown(f"**SLA:** {sla_lbl}")
                d_r = "#10b981" if sla_info["donus_durum"] == "zamaninda" else "#ef4444" if sla_info["donus_durum"] == "gecikti" else "#3b82f6"
                c_r = "#10b981" if sla_info["cozum_durum"] == "zamaninda" else "#ef4444" if sla_info["cozum_durum"] == "gecikti" else "#3b82f6"
                st.markdown(f'**Dönüs:** <span style="color:{d_r};font-weight:700;">{sla_info["donus_durum"].upper()}</span> ({sla_info["donus_gecen_saat"]}s/{sla_info["donus_sla_saat"]}s)', unsafe_allow_html=True)
                st.markdown(f'**Çözüm:** <span style="color:{c_r};font-weight:700;">{sla_info["cozum_durum"].upper()}</span> ({sla_info["cozum_gecen_saat"]}s/{sla_info["cozum_sla_saat"]}s)', unsafe_allow_html=True)
                if rec.get("donus_tarihi"):
                    st.markdown(f"**Dönüs Tarihi:** {rec['donus_tarihi'][:16].replace('T', ' ')}")

            st.divider()

            # --- Guncelleme ---
            rec_id = rec.get("id", "")
            cg1, cg2 = st.columns(2)
            with cg1:
                durum_labels = [d[1] for d in SIKAYET_DURUM]
                cur_idx = next((i for i, d in enumerate(SIKAYET_DURUM) if d[0] == d_key), 0)
                yeni_durum_label = st.selectbox("Durum / Sonuç Asaması", durum_labels, index=cur_idx, key=f"so_d_{idx}")
                yeni_durum_key = next((d[0] for d in SIKAYET_DURUM if d[1] == yeni_durum_label), "kayit_alindi")

                cozulemedi_neden = ""
                reddedildi_neden = ""
                if yeni_durum_key == "cozulemedi":
                    cozulemedi_neden = st.text_area("Çözümlenememe Nedeni *", value=rec.get("cozulemedi_neden", ""),
                                                     key=f"so_cn_{idx}", height=60)
                elif yeni_durum_key == "reddedildi":
                    reddedildi_neden = st.text_area("Ret Gerekçesi *", value=rec.get("reddedildi_neden", ""),
                                                     key=f"so_rn_{idx}", height=60)

                cur_yon = rec.get("yonlendirilen_kisi", "")
                yon_idx = calisan_sec.index(cur_yon) if cur_yon in calisan_sec else 0
                yonlendirilen = st.selectbox("Yönlendir", calisan_sec, index=yon_idx, key=f"so_yon_{idx}")

            with cg2:
                cur_alan = rec.get("sikayeti_alan", "")
                alan_idx = calisan_sec.index(cur_alan) if cur_alan in calisan_sec else 0
                sikayeti_alan = st.selectbox("Sikayeti Alan", calisan_sec, index=alan_idx, key=f"so_al_{idx}")

                cevap = st.text_area("Yanit / Not", value=rec.get("cevap", ""), key=f"so_cv_{idx}", height=80)

            # Butonlar
            bb1, bb2, bb3 = st.columns(3)
            with bb1:
                if st.button("Güncelle", key=f"so_gu_{idx}", type="primary", use_container_width=True):
                    rec["durum"] = yeni_durum_key
                    rec["sikayeti_alan"] = sikayeti_alan
                    rec["yonlendirilen_kisi"] = yonlendirilen
                    rec["cevap"] = cevap
                    rec["updated_at"] = datetime.now().isoformat()
                    # Bilgilendirme asamasi = ilk donus (SLA donus suresi)
                    if yeni_durum_key == "bilgilendirme" and not rec.get("donus_tarihi"):
                        rec["donus_tarihi"] = datetime.now().isoformat()
                    # Sonuc asamalarina gecis = cozum tarihi
                    if yeni_durum_key in _SONUC_DURUMLARI and not rec.get("cozum_tarihi"):
                        rec["cozum_tarihi"] = datetime.now().isoformat()
                    if yeni_durum_key == "cozulemedi":
                        rec["cozulemedi_neden"] = cozulemedi_neden
                    if yeni_durum_key == "reddedildi":
                        rec["reddedildi_neden"] = reddedildi_neden
                    _upsert_sikayet(rec)
                    st.success("Kayıt güncellendi!")
                    st.rerun()
            with bb2:
                if st.button("Sil", key=f"so_si_{idx}", use_container_width=True):
                    _delete_sikayet(rec_id)
                    st.success("Kayıt silindi!")
                    st.rerun()
            with bb3:
                st.markdown("""<div style="background:#1e293b; color:#e2e8f0;border-radius:8px;padding:8px 12px;font-size:10px;color:#0369a1;">
                <b>ISO 10002 Süreç Akisi:</b><br>
                1️⃣ Kayit → 2️⃣ Bilgilendirme → 3️⃣ Degerlendirme<br>
                4️⃣ Inceleme → 5️⃣ Aksiyon → 6️⃣ Uygulama → Sonuç
                </div>""", unsafe_allow_html=True)

            # --- Yazismalar ---
            yazismalar = rec.get("yazismalar", [])
            st.divider()
            styled_section("Yazismalar", "#6366f1")
            if yazismalar:
                for msg in yazismalar:
                    msg_tarih = msg.get("tarih", "")[:16].replace("T", " ")
                    msg_yazan = msg.get("yazan", "-")
                    msg_icerik = msg.get("icerik", "")
                    msg_yon = msg.get("yon", "giden")
                    if msg_yon == "giden":
                        st.markdown(f"""<div style="display:flex;margin-bottom:8px;">
                        <div style="background:linear-gradient(135deg,#0f1d36,#1a2d4a);border-radius:10px 10px 10px 2px;
                        padding:8px 12px;max-width:85%;border-left:3px solid #3b82f6;">
                        <div style="font-size:9px;color:#3b82f6;font-weight:700;">➡️ {msg_yazan} <span style="color:#94a3b8;margin-left:6px;">{msg_tarih}</span></div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px;">{msg_icerik}</div>
                        </div></div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="display:flex;justify-content:flex-end;margin-bottom:8px;">
                        <div style="background:linear-gradient(135deg,#0f2a1f,#1a3a2a);border-radius:10px 10px 2px 10px;
                        padding:8px 12px;max-width:85%;border-right:3px solid #10b981;">
                        <div style="font-size:9px;color:#10b981;font-weight:700;">⬅️ {msg_yazan} <span style="color:#94a3b8;margin-left:6px;">{msg_tarih}</span></div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px;">{msg_icerik}</div>
                        </div></div>""", unsafe_allow_html=True)
            else:
                st.caption("Henuz yazisma yok.")

            # Yeni mesaj
            yz1, yz2 = st.columns([3, 1])
            with yz1:
                yeni_mesaj = st.text_area("Mesaj", key=f"so_yz_{idx}", height=60,
                                           placeholder="Not veya cevap yazin...")
            with yz2:
                yz_yazan = st.selectbox("Yazan", calisan_sec, key=f"so_yzy_{idx}")
                yz_yon = st.radio("Yön", ["Giden", "Gelen"], key=f"so_yzd_{idx}", horizontal=True)

            if st.button("Mesaj Gönder", key=f"so_yzb_{idx}", type="primary", use_container_width=True):
                if not yeni_mesaj.strip():
                    st.error("Mesaj bos olamaz.")
                elif not yz_yazan:
                    st.error("Yazan kisi secin.")
                else:
                    if "yazismalar" not in rec:
                        rec["yazismalar"] = []
                    rec["yazismalar"].append({
                        "tarih": datetime.now().isoformat(),
                        "yazan": yz_yazan,
                        "icerik": yeni_mesaj.strip(),
                        "yon": "giden" if yz_yon == "Giden" else "gelen",
                    })
                    rec["updated_at"] = datetime.now().isoformat()
                    _upsert_sikayet(rec)
                    st.success("Mesaj gonderildi!")
                    st.rerun()



def _render_sikayet_yeni():
    """Yeni sikayet / oneri / talep formu."""
    styled_section("Yeni Kayıt Oluştur", "#8b5cf6")

    # SLA bilgi
    st.markdown("""<div style="background:linear-gradient(135deg,#0f1d36,#1a2d4a);border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:11px;color:#93c5fd;">
    <b>SLA Performans Kriterleri:</b> &nbsp;
    <span style="color:#ef4444;">Acil: 2-4s donus / 24s cozum</span> &nbsp;|&nbsp;
    <span style="color:#f59e0b;">Yuksek: 24s donus / 48s cozum</span> &nbsp;|&nbsp;
    <span style="color:#3b82f6;">Normal: 24s donus / 72s cozum</span> &nbsp;|&nbsp;
    <span style="color:#94a3b8;">Dusuk: 48s donus / 120s cozum</span>
    </div>""", unsafe_allow_html=True)

    ik_calisanlar = get_ik_employee_name_with_position()
    calisan_sec = [""] + ik_calisanlar

    with st.form("so_yeni_form"):
        # Tarih ve Saat
        col_ts1, col_ts2 = st.columns(2)
        with col_ts1:
            kayit_tarih = st.date_input("Kayıt Tarihi *", value=datetime.now().date(), key="so_kayit_tarih")
        with col_ts2:
            kayit_saat = st.time_input("Kayıt Saati *", value=datetime.now().time(), key="so_kayit_saat")

        col1, col2 = st.columns(2)
        with col1:
            tur_label = st.selectbox("Tur *", [t[1] for t in SIKAYET_TUR], key="kim_organi_21")

            kategori_label = st.selectbox("Kategori *", [k[1] for k in SIKAYET_KATEGORILERI], key="kim_organi_22")

            oncelik_label = st.selectbox("Öncelik", [o[1] for o in SIKAYET_ONCELIK], index=1, key="kim_organi_23")

            kaynak_label = st.selectbox("Kaynak *", [k[1] for k in SIKAYET_KAYNAK], key="kim_organi_24")

            kanal_label = st.selectbox("Sikayet Kanali *", [k[1] for k in SIKAYET_KANAL], key="kim_organi_m16")
        with col2:
            bildiren_adi = st.text_input("Bildiren Adi *", key="kim_organi_m17")
            bildiren_iletisim = st.text_input("İletişim (Telefon/E-posta)", key="kim_organi_m18")
            sikayeti_alan = st.selectbox("Sikayeti Alan Kisi *", calisan_sec, key="so_alan_yeni")
            yonlendirilen = st.selectbox("Sikayeti Yonlendir", calisan_sec, key="so_yon_yeni")

        konu = st.text_input("Konu Başlığı *", key="kim_organi_25")

        konum = st.text_input("Konum / Mekan (Opsiyonel)", key="kim_organi_26")

        aciklama = st.text_area("Açıklama / Detay", height=120, key="kim_organi_27")


        submitted = st.form_submit_button("Kaydet", use_container_width=True, type="primary")

    if submitted:
        if not bildiren_adi or not konu or not sikayeti_alan:
            st.error("Bildiren adi, konu ve sikayeti alan kisi zorunludur.")
            return

        tur_key = next((t[0] for t in SIKAYET_TUR if t[1] == tur_label), "sikayet")
        kat_key = next((k[0] for k in SIKAYET_KATEGORILERI if k[1] == kategori_label), "diger")
        onc_key = next((o[0] for o in SIKAYET_ONCELIK if o[1] == oncelik_label), "normal")
        kay_key = next((k[0] for k in SIKAYET_KAYNAK if k[1] == kaynak_label), "diger")
        kanal_key = next((k[0] for k in SIKAYET_KANAL if k[1] == kanal_label), "diger")

        kayit_dt = datetime.combine(kayit_tarih, kayit_saat)

        yeni = {
            "id": _gen_sikayet_id(),
            "tur": tur_key,
            "kategori": kat_key,
            "oncelik": onc_key,
            "kaynak": kay_key,
            "kanal": kanal_key,
            "bildiren_adi": bildiren_adi.strip(),
            "bildiren_iletisim": bildiren_iletisim.strip(),
            "konu": konu.strip(),
            "aciklama": aciklama.strip(),
            "konum": konum.strip(),
            "durum": "kayit_alindi",
            "sikayeti_alan": sikayeti_alan,
            "yonlendirilen_kisi": yonlendirilen,
            "cevap": "",
            "cozulemedi_neden": "",
            "donus_tarihi": "",
            "cozum_tarihi": "",
            "kayit_tarih_saat": kayit_dt.isoformat(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        _upsert_sikayet(yeni)
        st.success(f"Kayıt oluşturuldu: {konu}")
        st.rerun()


def _render_sikayet_sonuc(records: list[dict]):
    """Sonuclanan kayitlarin expander-tabanli goruntulenmesi."""
    styled_section("Sonuç Ekranı", "#059669")

    sonuc_records = [r for r in records if r.get("durum", "") in _SONUC_DURUMLARI]

    if not sonuc_records:
        st.info("Henuz sonuclanan kayit bulunmuyor. Kayitlar çözüldükçe burada görünür.")
        return

    # --- Ozet istatistikler ---
    toplam_sonuc = len(sonuc_records)
    cozulen = sum(1 for r in sonuc_records if r.get("durum") in ("cozumlendi", "kismen_cozumlendi"))
    cozulemedi = sum(1 for r in sonuc_records if r.get("durum") == "cozulemedi")
    reddedilen = sum(1 for r in sonuc_records if r.get("durum") == "reddedildi")
    kapanan = sum(1 for r in sonuc_records if r.get("durum") == "kapandi")

    cozum_saatleri = []
    for r in sonuc_records:
        kayit_str = r.get("kayit_tarih_saat", "") or r.get("created_at", "")
        cozum_str = r.get("cozum_tarihi", "")
        if kayit_str and cozum_str:
            try:
                k_dt = datetime.fromisoformat(kayit_str)
                c_dt = datetime.fromisoformat(cozum_str)
                fark = (c_dt - k_dt).total_seconds() / 3600
                if fark >= 0:
                    cozum_saatleri.append(fark)
            except (ValueError, TypeError):
                pass
    ort_saat = round(sum(cozum_saatleri) / len(cozum_saatleri), 1) if cozum_saatleri else 0

    styled_stat_row([
        ("Toplam Sonuç", str(toplam_sonuc), "#2563eb", "📋"),
        ("Çözülen", str(cozulen), "#10b981", "✅"),
        ("Çözülemedi", str(cozulemedi), "#ef4444", "❌"),
        ("Reddedilen", str(reddedilen), "#f97316", "🚫"),
    ])
    styled_stat_row([
        ("Kapanan", str(kapanan), "#64748b", "🔒"),
        ("Ort. Çözüm Süresi", f"{ort_saat}s", "#8b5cf6", "⏱️"),
        ("Çözüm Orani", f"%{round(cozulen / toplam_sonuc * 100) if toplam_sonuc else 0}", "#059669", "📊"),
        ("Toplam", str(toplam_sonuc), "#0d9488", "📈"),
    ])

    # --- Filtreler ---
    sonuc_durum_labels = [d[1] for d in SIKAYET_DURUM if d[0] in _SONUC_DURUMLARI]
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        f_tur = st.selectbox("Tür", ["Tümü"] + [t[1] for t in SIKAYET_TUR], key="so_sn_f_tur")
    with col_f2:
        f_durum = st.selectbox("Sonuç Durumu", ["Tümü"] + sonuc_durum_labels, key="so_sn_f_durum")
    with col_f3:
        f_kat = st.selectbox("Kategori", ["Tümü"] + [k[1] for k in SIKAYET_KATEGORILERI], key="so_sn_f_kat")
    with col_f4:
        f_onc = st.selectbox("Öncelik", ["Tümü"] + [o[1] for o in SIKAYET_ONCELIK], key="so_sn_f_onc")

    filtered = sonuc_records[:]
    if f_tur != "Tümü":
        tur_key = next((t[0] for t in SIKAYET_TUR if t[1] == f_tur), "")
        filtered = [r for r in filtered if r.get("tur") == tur_key]
    if f_durum != "Tümü":
        durum_key = next((d[0] for d in SIKAYET_DURUM if d[1] == f_durum), "")
        filtered = [r for r in filtered if r.get("durum") == durum_key]
    if f_kat != "Tümü":
        kat_key = next((k[0] for k in SIKAYET_KATEGORILERI if k[1] == f_kat), "")
        filtered = [r for r in filtered if r.get("kategori") == kat_key]
    if f_onc != "Tümü":
        onc_key = next((o[0] for o in SIKAYET_ONCELIK if o[1] == f_onc), "")
        filtered = [r for r in filtered if r.get("oncelik") == onc_key]

    filtered.sort(key=lambda r: r.get("cozum_tarihi", r.get("updated_at", "")), reverse=True)
    st.caption(f"{len(filtered)} sonuçlanan kayit")

    # --- Her kayit icin expander ---
    for idx, rec in enumerate(filtered[:50]):
        tur_label = dict(SIKAYET_TUR).get(rec.get("tur", ""), "")
        d_key = rec.get("durum", "kapandi")
        d_label = _SIKAYET_DURUM_MAP.get(d_key, d_key)
        sla_info = _hesapla_sla_durumu(rec)
        # (Sonuc Ekrani expander)
        sla_icon = "🟢" if sla_info["cozum_durum"] == "zamaninda" else "🔴" if sla_info["cozum_durum"] == "gecikti" else "⚪"
        cozum_ts = rec.get("cozum_tarihi", "")
        cozum_str = cozum_ts[:10] if cozum_ts else "-"

        exp_title = f"{sla_icon} {tur_label} | {rec.get('konu', '')[:45]} | {d_label} | {cozum_str}"

        with st.expander(exp_title, expanded=False):
            # Bilgi karti
            ci1, ci2, ci3 = st.columns(3)
            with ci1:
                st.markdown(f"**Konu:** {rec.get('konu', '')}")
                st.markdown(f"**Açıklama:** {rec.get('aciklama', '-')}")
                st.markdown(f"**Bildiren:** {rec.get('bildiren_adi', '-')} ({dict(SIKAYET_KAYNAK).get(rec.get('kaynak', ''), '')})")
                st.markdown(f"**İletişim:** {rec.get('bildiren_iletisim', '-')}")
            with ci2:
                kayit_ts = rec.get("kayit_tarih_saat", rec.get("created_at", ""))
                st.markdown(f"**Kayıt Tarihi:** {kayit_ts[:16].replace('T', ' ') if kayit_ts else '-'}")
                st.markdown(f"**Kanal:** {dict(SIKAYET_KANAL).get(rec.get('kanal', ''), '-')}")
                st.markdown(f"**Sikayeti Alan:** {rec.get('sikayeti_alan', '-')}")
                st.markdown(f"**Yönlendirilen:** {rec.get('yonlendirilen_kisi', '-')}")
                if rec.get("konum"):
                    st.markdown(f"**Konum:** {rec['konum']}")
            with ci3:
                sla_lbl = SIKAYET_SLA.get(rec.get("oncelik", "normal"), {}).get("label", "-")
                st.markdown(f"**SLA:** {sla_lbl}")
                d_r = "#10b981" if sla_info["donus_durum"] == "zamaninda" else "#ef4444" if sla_info["donus_durum"] == "gecikti" else "#3b82f6"
                c_r = "#10b981" if sla_info["cozum_durum"] == "zamaninda" else "#ef4444" if sla_info["cozum_durum"] == "gecikti" else "#3b82f6"
                st.markdown(f'**Dönüs:** <span style="color:{d_r};font-weight:700;">{sla_info["donus_durum"].upper()}</span> ({sla_info["donus_gecen_saat"]}s/{sla_info["donus_sla_saat"]}s)', unsafe_allow_html=True)
                st.markdown(f'**Çözüm:** <span style="color:{c_r};font-weight:700;">{sla_info["cozum_durum"].upper()}</span> ({sla_info["cozum_gecen_saat"]}s/{sla_info["cozum_sla_saat"]}s)', unsafe_allow_html=True)
                if rec.get("donus_tarihi"):
                    st.markdown(f"**Dönüs Tarihi:** {rec['donus_tarihi'][:16].replace('T', ' ')}")
                if rec.get("cozum_tarihi"):
                    st.markdown(f"**Çözüm Tarihi:** {rec['cozum_tarihi'][:16].replace('T', ' ')}")

            # --- Sonuc Asamasi bilgisi ---
            sonuc_aciklama = _SONUC_ASAMALARI.get(d_key, "")
            if sonuc_aciklama:
                st.markdown(f"""<div style="background:linear-gradient(135deg,#0f2a1f,#1a3a2a);border-radius:8px;
                padding:10px 14px;margin-top:8px;font-size:11px;color:#86efac;">
                <b>Sonuç Asamasi:</b> {sonuc_aciklama}
                </div>""", unsafe_allow_html=True)

            # --- Cevap / Not ---
            if rec.get("cevap"):
                st.divider()
                st.markdown(f"""<div style="background:linear-gradient(135deg,#0f1d36,#1a2d4a);border-radius:10px;padding:12px 16px;
                font-size:12px;color:#94A3B8;border-left:4px solid #3b82f6;">
                <b>Verilen Yanit:</b><br>{rec['cevap']}</div>""", unsafe_allow_html=True)

            # --- Cozulemedi nedeni ---
            if rec.get("durum") == "cozulemedi" and rec.get("cozulemedi_neden"):
                st.markdown(f"""<div style="background:linear-gradient(135deg,#2a0f0f,#3a1a1a);border-radius:10px;padding:12px 16px;
                margin-top:8px;font-size:12px;color:#94A3B8;border-left:4px solid #ef4444;">
                <b>Çözülememe Nedeni:</b><br>{rec['cozulemedi_neden']}</div>""", unsafe_allow_html=True)

            # --- Reddedildi gerekce ---
            if rec.get("durum") == "reddedildi" and rec.get("reddedildi_neden"):
                st.markdown(f"""<div style="background:linear-gradient(135deg,#fff7ed,#fed7aa);border-radius:10px;padding:12px 16px;
                margin-top:8px;font-size:12px;color:#94A3B8;border-left:4px solid #f97316;">
                <b>Ret Gerekçesi:</b><br>{rec['reddedildi_neden']}</div>""", unsafe_allow_html=True)

            # --- Yazisma Gecmisi (salt okunur) ---
            yazismalar = rec.get("yazismalar", [])
            if yazismalar:
                st.divider()
                for msg in yazismalar:
                    msg_tarih = msg.get("tarih", "")[:16].replace("T", " ")
                    msg_yazan = msg.get("yazan", "-")
                    msg_icerik = msg.get("icerik", "")
                    msg_yon = msg.get("yon", "giden")
                    if msg_yon == "giden":
                        st.markdown(f"""<div style="display:flex;margin-bottom:6px;">
                        <div style="background:linear-gradient(135deg,#0f1d36,#1a2d4a);border-radius:10px 10px 10px 2px;
                        padding:8px 12px;max-width:85%;border-left:3px solid #3b82f6;">
                        <div style="font-size:9px;color:#3b82f6;font-weight:700;">➡️ {msg_yazan} <span style="color:#94a3b8;margin-left:6px;">{msg_tarih}</span></div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px;">{msg_icerik}</div>
                        </div></div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="display:flex;justify-content:flex-end;margin-bottom:6px;">
                        <div style="background:linear-gradient(135deg,#0f2a1f,#1a3a2a);border-radius:10px 10px 2px 10px;
                        padding:8px 12px;max-width:85%;border-right:3px solid #10b981;">
                        <div style="font-size:9px;color:#10b981;font-weight:700;">⬅️ {msg_yazan} <span style="color:#94a3b8;margin-left:6px;">{msg_tarih}</span></div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px;">{msg_icerik}</div>
                        </div></div>""", unsafe_allow_html=True)
                st.caption(f"{len(yazismalar)} mesaj")

            # --- Yeniden Ac butonu ---
            st.divider()
            if st.button("Yeniden Aç (Takibe Al)", key=f"so_sn_yac_{idx}", type="primary", use_container_width=True):
                rec["durum"] = "degerlendirme"
                rec["cozum_tarihi"] = ""
                rec["cozulemedi_neden"] = ""
                rec["reddedildi_neden"] = ""
                rec["updated_at"] = datetime.now().isoformat()
                _upsert_sikayet(rec)
                st.success("Kayit yeniden açildi ve Takip sekmesine taşindi!")
                st.rerun()


def _render_sikayet_istatistik(records: list[dict]):
    """Sikayet/oneri istatistikleri, SLA performansi ve grafikleri."""
    styled_section("İstatistikler ve SLA Performansi", "#059669")

    if not records:
        st.info("İstatistik için kayit bulunmuyor.")
        return

    from collections import Counter

    # ---- SLA Performans Ozeti ----
    styled_section("SLA Performans Özeti", "#dc2626")
    sla_zamaninda_donus = 0
    sla_gecikti_donus = 0
    sla_zamaninda_cozum = 0
    sla_gecikti_cozum = 0
    sla_bekliyor = 0
    ort_donus_saat = []
    ort_cozum_saat = []
    oncelik_sla = {k: {"zamaninda": 0, "gecikti": 0, "bekliyor": 0} for k, _, _ in SIKAYET_ONCELIK}

    for r in records:
        sla = _hesapla_sla_durumu(r)
        onc = r.get("oncelik", "normal")
        if sla["donus_durum"] == "zamaninda":
            sla_zamaninda_donus += 1
        elif sla["donus_durum"] == "gecikti":
            sla_gecikti_donus += 1
        if sla["cozum_durum"] == "zamaninda":
            sla_zamaninda_cozum += 1
        elif sla["cozum_durum"] == "gecikti":
            sla_gecikti_cozum += 1
        else:
            sla_bekliyor += 1
        if sla["donus_gecen_saat"] > 0 and sla["donus_durum"] != "bekliyor":
            ort_donus_saat.append(sla["donus_gecen_saat"])
        if sla["cozum_gecen_saat"] > 0 and sla["cozum_durum"] != "bekliyor":
            ort_cozum_saat.append(sla["cozum_gecen_saat"])
        if onc in oncelik_sla:
            if sla["cozum_durum"] == "zamaninda":
                oncelik_sla[onc]["zamaninda"] += 1
            elif sla["cozum_durum"] == "gecikti":
                oncelik_sla[onc]["gecikti"] += 1
            else:
                oncelik_sla[onc]["bekliyor"] += 1

    ort_d = round(sum(ort_donus_saat) / len(ort_donus_saat), 1) if ort_donus_saat else 0
    ort_c = round(sum(ort_cozum_saat) / len(ort_cozum_saat), 1) if ort_cozum_saat else 0

    styled_stat_row([
        ("Donus: Zamaninda", str(sla_zamaninda_donus), "#10b981", "✅"),
        ("Donus: Gecikti", str(sla_gecikti_donus), "#ef4444", "⏰"),
        ("Ort. Donus Suresi", f"{ort_d} saat", "#3b82f6", "↩️"),
        ("Ort. Cozum Suresi", f"{ort_c} saat", "#8b5cf6", "🔧"),
    ])
    styled_stat_row([
        ("Cozum: Zamaninda", str(sla_zamaninda_cozum), "#10b981", "✅"),
        ("Cozum: Gecikti", str(sla_gecikti_cozum), "#ef4444", "⏰"),
        ("Bekleyen", str(sla_bekliyor), "#3b82f6", "⏳"),
        ("SLA Başarı", f"%{round(sla_zamaninda_cozum/(sla_zamaninda_cozum+sla_gecikti_cozum)*100) if (sla_zamaninda_cozum+sla_gecikti_cozum) > 0 else 0}", "#059669", "📊"),
    ])

    # SLA - Oncelik bazli grafik
    col_sla1, col_sla2 = st.columns(2)
    with col_sla1:
        onc_labels = [l for _, l, _ in SIKAYET_ONCELIK]
        z_vals = [oncelik_sla[k]["zamaninda"] for k, _, _ in SIKAYET_ONCELIK]
        g_vals = [oncelik_sla[k]["gecikti"] for k, _, _ in SIKAYET_ONCELIK]
        b_vals = [oncelik_sla[k]["bekliyor"] for k, _, _ in SIKAYET_ONCELIK]
        fig_sla = go.Figure()
        fig_sla.add_trace(go.Bar(name="Zamaninda", y=onc_labels, x=z_vals, orientation="h",
                                  marker_color=SC_COLORS[1], text=z_vals, textposition="auto"))
        fig_sla.add_trace(go.Bar(name="Gecikti", y=onc_labels, x=g_vals, orientation="h",
                                  marker_color=SC_COLORS[4], text=g_vals, textposition="auto"))
        fig_sla.add_trace(go.Bar(name="Bekliyor", y=onc_labels, x=b_vals, orientation="h",
                                  marker_color=SC_COLORS[7], text=b_vals, textposition="auto"))
        fig_sla.update_layout(barmode="stack",
                               title=dict(text="Öncelik Bazli SLA Durumu", font=dict(size=13)),
                               legend=dict(orientation="h", y=-0.15))
        sc_bar(fig_sla, height=280, horizontal=True)
        st.plotly_chart(fig_sla, use_container_width=True, config=SC_CHART_CFG)

    with col_sla2:
        # SLA donut: zamaninda vs gecikti vs bekliyor
        sla_pie_vals = [sla_zamaninda_cozum, sla_gecikti_cozum, sla_bekliyor]
        sla_pie_lbls = ["Zamaninda", "Gecikti", "Bekliyor"]
        fig_sla_pie = go.Figure(go.Pie(
            labels=sla_pie_lbls, values=sla_pie_vals, hole=0.55,
            marker=dict(colors=SC_COLORS[:3], line=dict(color="#fff", width=2)),
            textinfo="label+value+percent", textfont=dict(size=11),
        ))
        sc_pie(fig_sla_pie, height=280)
        fig_sla_pie.update_layout(title=dict(text="Genel SLA Performansi", font=dict(size=13)))
        st.plotly_chart(fig_sla_pie, use_container_width=True, config=SC_CHART_CFG)

    st.divider()

    # ---- Genel Dagilim Grafikleri ----
    styled_section("Genel Dagilimlar", "#2563eb")

    col1, col2 = st.columns(2)

    with col1:
        # Tur dagilimi
        tur_counts = Counter(dict(SIKAYET_TUR).get(r.get("tur", ""), r.get("tur", "")) for r in records)
        if tur_counts:
            fig = go.Figure(go.Pie(
                labels=list(tur_counts.keys()), values=list(tur_counts.values()),
                hole=0.55, marker=dict(colors=SC_COLORS[:len(tur_counts)], line=dict(color="#fff", width=2)),
                textinfo="label+value", textfont=dict(size=11),
            ))
            sc_pie(fig, height=300)
            fig.update_layout(title=dict(text="Tür Dağılımı", font=dict(size=13)))
            st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

    with col2:
        # Durum / Sonuc dagilimi
        durum_counts = Counter(_SIKAYET_DURUM_MAP.get(r.get("durum", ""), r.get("durum", "")) for r in records)
        if durum_counts:
            labels = list(durum_counts.keys())
            values = list(durum_counts.values())
            fig2 = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.55,
                marker=dict(colors=SC_COLORS[:len(labels)], line=dict(color="#fff", width=2)),
                textinfo="label+value", textfont=dict(size=11),
            ))
            sc_pie(fig2, height=300)
            fig2.update_layout(title=dict(text="Durum / Sonuç Dağılımı", font=dict(size=13)))
            st.plotly_chart(fig2, use_container_width=True, config=SC_CHART_CFG)

    col3, col4 = st.columns(2)

    with col3:
        # Kategori dagilimi
        kat_counts = Counter(_SIKAYET_KAT_MAP.get(r.get("kategori", ""), r.get("kategori", "")) for r in records)
        if kat_counts:
            k_labels = list(kat_counts.keys())
            k_values = list(kat_counts.values())
            fig3 = go.Figure(go.Bar(
                y=k_labels, x=k_values, orientation="h",
                marker_color=SC_COLORS[0], text=k_values, textposition="outside",
            ))
            sc_bar(fig3, height=max(250, len(k_labels) * 35), horizontal=True)
            fig3.update_layout(title=dict(text="Kategori Dağılımı", font=dict(size=13)))
            st.plotly_chart(fig3, use_container_width=True, config=SC_CHART_CFG)

    with col4:
        # Kaynak dagilimi
        kaynak_counts = Counter(dict(SIKAYET_KAYNAK).get(r.get("kaynak", ""), r.get("kaynak", "")) for r in records)
        if kaynak_counts:
            ky_labels = list(kaynak_counts.keys())
            ky_values = list(kaynak_counts.values())
            fig4 = go.Figure(go.Bar(
                y=ky_labels, x=ky_values, orientation="h",
                marker_color=SC_COLORS[0], text=ky_values, textposition="outside",
            ))
            sc_bar(fig4, height=max(200, len(ky_labels) * 35), horizontal=True)
            fig4.update_layout(title=dict(text="Kaynak Dağılımı", font=dict(size=13)))
            st.plotly_chart(fig4, use_container_width=True, config=SC_CHART_CFG)

    # Kanal dagilimi
    col5, col6 = st.columns(2)
    with col5:
        kanal_counts = Counter(dict(SIKAYET_KANAL).get(r.get("kanal", ""), r.get("kanal", "-")) for r in records)
        if kanal_counts:
            kn_labels = list(kanal_counts.keys())
            kn_values = list(kanal_counts.values())
            fig5 = go.Figure(go.Bar(
                y=kn_labels, x=kn_values, orientation="h",
                marker_color=SC_COLORS[0], text=kn_values, textposition="outside",
            ))
            sc_bar(fig5, height=max(250, len(kn_labels) * 35), horizontal=True)
            fig5.update_layout(title=dict(text="Kanal Dağılımı", font=dict(size=13)))
            st.plotly_chart(fig5, use_container_width=True, config=SC_CHART_CFG)

    with col6:
        # Kanal donut
        if kanal_counts:
            fig6 = go.Figure(go.Pie(
                labels=kn_labels, values=kn_values, hole=0.55,
                marker=dict(colors=SC_COLORS[:len(kn_labels)], line=dict(color="#fff", width=2)),
                textinfo="label+value", textfont=dict(size=11),
            ))
            sc_pie(fig6, height=300)
            fig6.update_layout(title=dict(text="Kanal Orani", font=dict(size=13)))
            st.plotly_chart(fig6, use_container_width=True, config=SC_CHART_CFG)

    # Zaman bazli grafik - Haftalik/Aylik trend
    styled_section("Zaman Bazli Analiz", "#f59e0b")
    tarihli = []
    for r in records:
        ts = r.get("kayit_tarih_saat", r.get("created_at", ""))
        if ts:
            try:
                tarihli.append((datetime.fromisoformat(ts).date(), r))
            except Exception:
                pass
    if tarihli:
        tarihli.sort(key=lambda x: x[0])
        # Gunluk sikayet sayisi
        gun_counts = Counter(str(t[0]) for t in tarihli)
        gun_labels = sorted(gun_counts.keys())
        gun_values = [gun_counts[g] for g in gun_labels]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=gun_labels, y=gun_values, mode="lines+markers",
            line=dict(color="#8b5cf6", width=2), marker=dict(size=6),
            name="Günlük Kayıt",
        ))
        fig_trend.update_layout(height=300, margin=dict(t=30, b=10, l=40, r=10),
                                 title=dict(text="Günlük Sikayet/Oneri/Talep Trendi", font=dict(size=13)),
                                 paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                 xaxis=dict(title="Tarih"), yaxis=dict(title="Kayıt Sayısı"))
        st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # Oncelik dagilimi - metrik kartlari
    styled_section("Öncelik Dağılımı", "#f59e0b")
    onc_counts = Counter(r.get("oncelik", "normal") for r in records)
    onc_stats = []
    for key, label, renk in SIKAYET_ONCELIK:
        onc_stats.append((label, str(onc_counts.get(key, 0)), renk, "🔔" if key == "acil" else "📌"))
    styled_stat_row(onc_stats)

    # ISO 10002 Surec Asamalari Ozeti
    styled_section("Süreç Asamalari Özeti (ISO 10002)", "#10b981")
    s_kayit = sum(1 for r in records if r.get("durum") == "kayit_alindi")
    s_bilgi = sum(1 for r in records if r.get("durum") == "bilgilendirme")
    s_deger = sum(1 for r in records if r.get("durum") == "degerlendirme")
    s_incel = sum(1 for r in records if r.get("durum") == "inceleme")
    s_aksiy = sum(1 for r in records if r.get("durum") == "aksiyon_planlandi")
    s_uygul = sum(1 for r in records if r.get("durum") == "uygulamada")
    s_cozum = sum(1 for r in records if r.get("durum") == "cozumlendi")
    s_kisme = sum(1 for r in records if r.get("durum") == "kismen_cozumlendi")
    s_cozul = sum(1 for r in records if r.get("durum") == "cozulemedi")
    s_redde = sum(1 for r in records if r.get("durum") == "reddedildi")
    s_kapan = sum(1 for r in records if r.get("durum") == "kapandi")
    styled_stat_row([
        ("Kayıt Alındı", str(s_kayit), "#3b82f6", "1️⃣"),
        ("Bilgilendirme", str(s_bilgi), "#3b82f6", "2️⃣"),
        ("Değerlendirme", str(s_deger), "#f59e0b", "3️⃣"),
        ("İnceleme", str(s_incel), "#8b5cf6", "4️⃣"),
    ])
    styled_stat_row([
        ("Aksiyon Planlandı", str(s_aksiy), "#a855f7", "5️⃣"),
        ("Uygulamada", str(s_uygul), "#14b8a6", "6️⃣"),
        ("Çözümlendi", str(s_cozum + s_kisme), "#10b981", "✅"),
        ("Çözülemedi/Red", str(s_cozul + s_redde), "#ef4444", "❌"),
    ])
    styled_stat_row([
        ("Kapandı", str(s_kapan), "#64748b", "🔒"),
        ("Aktif Takip", str(s_kayit + s_bilgi + s_deger + s_incel + s_aksiy + s_uygul), "#f59e0b", "⏳"),
        ("Toplam", str(len(records)), "#2563eb", "📋"),
        ("Çözüm Oranı", f"%{round((s_cozum + s_kisme) / len(records) * 100) if records else 0}", "#059669", "📊"),
    ])

    # Cozulemeyenler + Reddedilenler listesi
    sorunlu = [r for r in records if r.get("durum") in ("cozulemedi", "reddedildi")]
    if sorunlu:
        styled_section("Çözülemeyen / Reddedilen Kayıtlar", "#ef4444")
        for r in sorunlu:
            if r.get("durum") == "cozulemedi":
                neden = r.get("cozulemedi_neden", "Belirtilmemis")
                badge_renk = "#ef4444"
                badge_text = "ÇÖZÜLEMEDI"
            else:
                neden = r.get("reddedildi_neden", "Belirtilmemis")
                badge_renk = "#f97316"
                badge_text = "REDDEDILDI"
            st.markdown(f"""<div style="background:#1e293b;border-left:4px solid {badge_renk};border-radius:8px;padding:10px 14px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
            <b>{r.get('konu', '-')}</b>
            <span style="background:{badge_renk}15;color:{badge_renk};padding:2px 8px;border-radius:6px;font-size:9px;font-weight:700;">{badge_text}</span>
            </div>
            <span style="color:#94a3b8;font-size:11px;">{r.get('kayit_tarih_saat', r.get('created_at', ''))[:10]}</span><br>
            <span style="color:#dc2626;font-size:12px;"><b>Neden:</b> {neden}</span>
            </div>""", unsafe_allow_html=True)


# ===================== PANEL MESAJLARI =====================

_GRUP_HEDEFLERI = [
    ("tum_ogretmenler", "Tüm Öğretmenler"),
    ("tum_veliler", "Tüm Veliler"),
    ("tum_calisanlar", "Tüm Çalışanlar"),
    ("tum_personel", "Tüm Personel (Öğretmen + Çalışan)"),
]


def _render_panel_mesajlari():
    """Kurum ici panel mesajlasma sistemi: gelen/giden/yeni mesaj + grup."""
    auth_user = st.session_state.get("auth_user", {})
    username = auth_user.get("username", "")
    user_name = auth_user.get("name", "")
    user_role = auth_user.get("role", "")

    store = get_akademik_store()

    # Okunmamis sayisi
    okunmamis = store.get_okunmamis_mesaj_sayisi(receiver_id=username)

    styled_section("Kurum Ici Panel Mesajlari", "#2563eb")
    if okunmamis > 0:
        st.warning(f"📩 {okunmamis} okunmamis mesajiniz var.")

    mesaj_modu = st.radio(
        "İşlem Secin",
        ["Gelen Kutusu", "Giden Kutusu", "Yeni Mesaj"],
        horizontal=True,
        key="kim_panel_mesaj_modu",
    )

    if mesaj_modu == "Gelen Kutusu":
        _render_panel_gelen(store, username)
    elif mesaj_modu == "Giden Kutusu":
        _render_panel_giden(store, username)
    else:
        _render_panel_yeni_mesaj(store, auth_user)


def _render_panel_gelen(store, username: str):
    """Panel gelen kutusu - birebir + grup mesajlari."""
    mesajlar = store.get_panel_gelen_kutusu(receiver_id=username)
    if not mesajlar:
        st.info("Gelen kutunuz bos.")
        return

    okunmamis = sum(1 for m in mesajlar if not m.okundu)
    toplam = len(mesajlar)

    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam", toplam)
    c2.metric("Okunmamis", okunmamis)
    c3.metric("Okunmus", toplam - okunmamis)
    st.markdown("---")

    kat_map = dict(MESAJ_KATEGORILERI)
    for i, m in enumerate(mesajlar):
        is_grup = m.is_group_message
        okundu_icon = "📧" if m.okundu else "📩"
        grup_tag = " [GRUP]" if is_grup else ""
        baslik = f"{okundu_icon} {m.sender_name} - {m.konu or '(Konu yok)'}{grup_tag}"
        if not m.okundu:
            baslik = f"**{baslik}**"

        with st.expander(baslik, expanded=False):
            if not m.okundu:
                if is_grup:
                    store.mark_grup_mesaj_okundu(m.id, username)
                else:
                    store.mark_mesaj_okundu(m.id)

            col_info, col_date = st.columns([3, 1])
            with col_info:
                st.write(f"**Gonderen:** {m.sender_name}")
                st.write(f"**Kategori:** {kat_map.get(m.kategori, m.kategori)}")
                if is_grup:
                    st.write(f"**Grup:** {m.group_target}")
            with col_date:
                st.write(f"**Tarih:** {m.created_at[:16] if m.created_at else '-'}")

            st.markdown("---")
            st.markdown(m.icerik or "(İçerik yok)")

            if not is_grup:
                if st.button("Yanitla", key=f"kim_reply_{m.id}_{i}"):
                    st.session_state["kim_reply_to"] = m
                    st.session_state["kim_panel_mesaj_modu"] = "Yeni Mesaj"
                    st.rerun()


def _render_panel_giden(store, username: str):
    """Panel giden kutusu."""
    mesajlar = store.get_veli_giden_kutusu(sender_id=username)
    if not mesajlar:
        st.info("Henuz mesaj gondermemissiniz.")
        return

    kat_map = dict(MESAJ_KATEGORILERI)
    for m in mesajlar:
        is_grup = m.is_group_message
        if is_grup:
            okundu_str = f"{len(m.group_recipients)} alici"
            icon = "📢"
            alici_label = m.group_target
        else:
            okundu_str = "Okundu" if m.okundu else "Okunmadi"
            icon = "✅" if m.okundu else "⏳"
            alici_label = m.receiver_name

        with st.expander(f"📤 {alici_label} - {m.konu or '(Konu yok)'} [{icon} {okundu_str}]"):
            st.write(f"**Alici:** {alici_label}")
            st.write(f"**Kategori:** {kat_map.get(m.kategori, m.kategori)}")
            st.write(f"**Tarih:** {m.created_at[:16] if m.created_at else '-'}")
            if is_grup:
                st.write(f"**Tip:** Grup Mesaji — {m.group_target}")
            st.markdown("---")
            st.markdown(m.icerik or "(İçerik yok)")


def _render_panel_yeni_mesaj(store, auth_user: dict):
    """Yeni mesaj: birebir veya grup."""
    username = auth_user.get("username", "")
    user_name = auth_user.get("name", "")
    user_role = auth_user.get("role", "")

    reply_to = st.session_state.pop("kim_reply_to", None)

    # Sender type
    role_map = {"Yonetici": "yonetici", "Öğretmen": "ogretmen", "Çalışan": "calisan"}
    sender_type = role_map.get(user_role, "yonetici")

    if reply_to:
        st.info(f"Yanit: {reply_to.sender_name} — {reply_to.konu}")
        mesaj_tipi = "birebir"
    else:
        mesaj_tipi = st.radio(
            "Mesaj Tipi", ["Birebir Mesaj", "Grup Mesaji"],
            horizontal=True, key="kim_mesaj_tipi",
        )
        mesaj_tipi = "birebir" if mesaj_tipi == "Birebir Mesaj" else "grup"

    if mesaj_tipi == "birebir":
        _render_birebir_mesaj_formu(store, auth_user, sender_type, reply_to)
    else:
        _render_grup_mesaj_formu(store, auth_user, sender_type)


def _render_birebir_mesaj_formu(store, auth_user: dict, sender_type: str,
                                 reply_to=None):
    """Birebir mesaj gonderme formu."""
    username = auth_user.get("username", "")
    user_name = auth_user.get("name", "")

    # Alici listesi
    teachers = store.get_teachers()
    students = store.get_students()
    staff = load_ik_active_employees()

    alici_map = {}
    # Ogretmenler
    for t in teachers:
        alici_map[f"ogr_{t.id}"] = (f"{t.ad} {t.soyad} (Öğretmen - {getattr(t, 'brans', '')})",
                                     "ogretmen", t.id)
    # Yonetim
    alici_map["yonetim"] = ("Okul Yönetimi", "yonetici", "yonetim")
    # Veliler (ogrenci adi ile)
    for s in students:
        if s.veli_adi:
            alici_map[f"veli_{s.id}"] = (f"{s.veli_adi} ({s.tam_ad} velisi)",
                                          "veli", s.veli_telefon or s.veli_email or s.veli_adi)

    with st.form("kim_birebir_mesaj", clear_on_submit=True):
        if reply_to:
            alici_id_key = reply_to.sender_id
            default_konu = f"Re: {reply_to.konu}"
            # Alici bilgilerini reply'dan al
            alici_tip = reply_to.sender_type
            alici_name = reply_to.sender_name
        else:
            secenekler = list(alici_map.keys())
            alici_id_key = st.selectbox(
                "Alici", secenekler,
                format_func=lambda x: alici_map[x][0],
                key="kim_birebir_alici",
            )
            default_konu = ""
            alici_name = alici_map[alici_id_key][0]
            alici_tip = alici_map[alici_id_key][1]
            alici_id_key = alici_map[alici_id_key][2] if not reply_to else alici_id_key

        konu = st.text_input("Konu", value=default_konu, key="kim_birebir_konu")
        kategori = st.selectbox(
            "Kategori", [k for k, _ in MESAJ_KATEGORILERI],
            format_func=lambda x: dict(MESAJ_KATEGORILERI).get(x, x),
            key="kim_birebir_kategori",
        )
        icerik = st.text_area("Mesaj Icerigi", height=150, key="kim_birebir_icerik")
        gonder = st.form_submit_button("Mesaji Gonder", type="primary",
                                        use_container_width=True)

    if gonder:
        if not konu or not icerik:
            st.error("Konu ve mesaj icerigi zorunludur.")
            return

        if reply_to:
            recv_id = reply_to.sender_id
            recv_name = reply_to.sender_name
            recv_type = reply_to.sender_type
        else:
            recv_id = alici_id_key
            recv_name = alici_name.split("(")[0].strip() if "(" in alici_name else alici_name
            recv_type = alici_tip

        mesaj = VeliMesaj(
            sender_type=sender_type,
            sender_id=username,
            sender_name=user_name,
            receiver_type=recv_type,
            receiver_id=recv_id,
            receiver_name=recv_name,
            konu=konu,
            icerik=icerik,
            kategori=kategori,
            parent_message_id=reply_to.id if reply_to else "",
            conversation_id=reply_to.conversation_id if reply_to else "",
        )
        if not mesaj.conversation_id:
            mesaj.conversation_id = mesaj.id
        store.save_veli_mesaj(mesaj)
        try:
            from utils.messaging import send_panel_mesaj_bildirimi
            send_panel_mesaj_bildirimi(
                receiver_id=mesaj.receiver_id,
                receiver_type=mesaj.receiver_type,
                receiver_name=mesaj.receiver_name,
                sender_name=mesaj.sender_name,
                konu=mesaj.konu,
                icerik=mesaj.icerik,
            )
        except Exception:
            pass
        st.success(f"Mesaj '{recv_name}' adresine gonderildi!")


def _render_grup_mesaj_formu(store, auth_user: dict, sender_type: str):
    """Grup mesaj gonderme formu."""
    username = auth_user.get("username", "")
    user_name = auth_user.get("name", "")

    styled_section("Grup Mesaj Gonder", "#7c3aed")

    # Hedef grup secimi
    students = store.get_students()
    siniflar = sorted(set(f"{s.sinif}/{s.sube}" for s in students if s.sinif and s.sube))
    sinif_gruplari = [(f"sinif_{s.replace('/', '_')}_veliler",
                       f"{s} Sınıfı Velileri") for s in siniflar]

    tum_hedefler = list(_GRUP_HEDEFLERI) + sinif_gruplari

    with st.form("kim_grup_mesaj", clear_on_submit=True):
        grup_hedef_key = st.selectbox(
            "Hedef Grup", [k for k, _ in tum_hedefler],
            format_func=lambda x: dict(tum_hedefler).get(x, x),
            key="kim_grup_hedef",
        )
        konu = st.text_input("Konu", key="kim_grup_konu")
        kategori = st.selectbox(
            "Kategori", [k for k, _ in MESAJ_KATEGORILERI],
            format_func=lambda x: dict(MESAJ_KATEGORILERI).get(x, x),
            key="kim_grup_kategori",
        )
        icerik = st.text_area("Mesaj Icerigi", height=150, key="kim_grup_icerik")
        gonder = st.form_submit_button("Grup Mesaji Gonder", type="primary",
                                        use_container_width=True)

    if gonder:
        if not konu or not icerik:
            st.error("Konu ve mesaj icerigi zorunludur.")
            return

        # Alicilari belirle
        recipients = _resolve_grup_recipients(store, grup_hedef_key)
        if not recipients:
            st.error("Secilen grupta alici bulunamadı.")
            return

        mesaj = store.send_grup_mesaj(
            sender_type=sender_type,
            sender_id=username,
            sender_name=user_name,
            group_target=dict(tum_hedefler).get(grup_hedef_key, grup_hedef_key),
            recipients=recipients,
            konu=konu,
            icerik=icerik,
            kategori=kategori,
        )
        try:
            from utils.messaging import send_grup_mesaj_bildirimleri
            send_grup_mesaj_bildirimleri(
                recipients=recipients,
                sender_name=user_name,
                konu=konu,
                icerik=icerik,
            )
        except Exception:
            pass
        st.success(f"Grup mesaji gonderildi! ({len(recipients)} alici)")
        with st.expander("Alicilar"):
            for r in recipients:
                st.write(f"• {r.get('ad', '-')} ({r.get('tip', '-')})")


def _resolve_grup_recipients(store, grup_key: str) -> list:
    """Grup anahtarina gore alici listesini coz."""
    from utils.auth import AuthManager

    all_users = AuthManager.get_all_users()
    students = store.get_students()
    teachers = store.get_teachers()
    staff = load_ik_active_employees()

    recipients = []

    if grup_key == "tum_ogretmenler":
        for u in all_users:
            if u.get("role") == "Öğretmen" and u.get("is_active", True):
                recipients.append({"id": u["username"], "ad": u.get("name", ""), "tip": "ogretmen"})

    elif grup_key == "tum_veliler":
        for u in all_users:
            if u.get("role") == "Veli" and u.get("is_active", True):
                recipients.append({"id": u["username"], "ad": u.get("name", ""), "tip": "veli"})

    elif grup_key == "tum_calisanlar":
        for u in all_users:
            if u.get("role") == "Çalışan" and u.get("is_active", True):
                recipients.append({"id": u["username"], "ad": u.get("name", ""), "tip": "calisan"})

    elif grup_key == "tum_personel":
        for u in all_users:
            if u.get("role") in ("Öğretmen", "Çalışan") and u.get("is_active", True):
                recipients.append({"id": u["username"], "ad": u.get("name", ""), "tip": u["role"].lower()})

    elif grup_key.startswith("sinif_") and grup_key.endswith("_veliler"):
        # sinif_9_A_veliler -> sinif=9, sube=A
        parts = grup_key.replace("sinif_", "").replace("_veliler", "").split("_")
        if len(parts) == 2:
            sinif_val, sube_val = parts
            sinif_ogrenciler = [s for s in students
                                if str(s.sinif) == sinif_val and s.sube == sube_val]
            for s in sinif_ogrenciler:
                if s.veli_adi:
                    # Veli kullanici hesabini bul
                    for u in all_users:
                        if u.get("role") == "Veli" and u.get("is_active", True):
                            veli_name = u.get("name", "").lower()
                            if s.veli_adi.lower() in veli_name or veli_name in s.veli_adi.lower():
                                recipients.append({
                                    "id": u["username"],
                                    "ad": f"{s.veli_adi} ({s.tam_ad} velisi)",
                                    "tip": "veli",
                                })
                                break

    # Tekrar edenleri kaldir
    seen = set()
    unique = []
    for r in recipients:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)
    return unique
