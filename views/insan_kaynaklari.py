"""
KIM-03 Insan Kaynaklari Yonetimi Modulu
========================================
Aday havuzu, mulakat yonetimi, onboarding, performans degerlendirme,
offboarding, izin, bordro, egitim, disiplin ve raporlar.
"""

from __future__ import annotations

import csv
import io
import json
import os
import uuid
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st
import pandas as pd

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("insan_kaynaklari")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("insan_kaynaklari",
        "AI destekli ise alim, ozluk, izin, bordro, performans degerlendirme",
        [("65", "Calisan"), ("AI", "Ise Alim")])
except Exception:
    pass

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_staff, get_staff_display_options, sync_employee_to_shared_staff, remove_employee_from_shared_staff, OGRETMEN_BRANSLARI
from utils.report_utils import ReportStyler, ReportPDFGenerator, get_institution_info
from models.tuketim_demirbas import TDMDataStore
from models.akademik_takip import AkademikDataStore
from models.insan_kaynaklari import (
    IKDataStore, IKSettings,
    Candidate, Position, Application, Interview, InterviewScore,
    QuestionSet, InterviewQuestion, DocumentTemplate, CandidateDocument,
    Employee, PerformanceCriterion, PerformanceReview, OffboardingRecord,
    AuditLogEntry,
    QuestionSetSelector, PerformanceCalculator, OnboardingChecker,
    OffboardingChecker, AuditLogger,
    CANDIDATE_STATUSES, INTERVIEW_DECISIONS, INTERVIEW_TYPES, INTERVIEW_STATUSES,
    DOCUMENT_STATUSES, ROLE_SCOPES, EMPLOYEE_STATUSES, OFFBOARDING_TYPES,
    PERFORMANCE_PERIOD_TYPES_IDARI, PERFORMANCE_PERIOD_TYPES_OGRETMEN,
    PERFORMANCE_PERIOD_LABELS, PERFORMANCE_SCORE_LABELS, DEGERLENDIREN_UNVANLAR,
    IZIN_TIPLERI, IZIN_VARSAYILAN_GUN, EGITIM_TURLERI,
    DISIPLIN_ISLEM_TURLERI, KATEGORI_MAP, CATEGORY_TO_ROLE_SCOPE,
    ISE_ALIM_EVRAKLARI, ISTEN_CIKIS_EVRAKLARI, AYRILMA_SEKILLERI, UZLASMA_DURUMLARI,
)
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome


# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_ik_store() -> IKDataStore:
    base = os.path.join(get_tenant_dir(), "ik")
    store = IKDataStore(base)
    # Varsayilan soru setlerini otomatik yukle (yoksa)
    _pop_key = "ik_default_qs_populated"
    if _pop_key not in st.session_state:
        store.auto_populate_default_questions()
        st.session_state[_pop_key] = True
    # Varsayilan performans kriterlerini otomatik yukle / guncelle
    _pc_key = "ik_default_pc_v2"
    if _pc_key not in st.session_state:
        store.auto_populate_default_criteria()
        st.session_state[_pc_key] = True
    return store


def _gen_local_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _now_str() -> str:
    return datetime.now().isoformat()


def _today_str() -> str:
    return date.today().isoformat()


def _get_personel_options() -> list[dict]:
    return load_shared_staff()


def _personel_selectbox(key: str, label: str = "Personel Secin") -> dict | None:
    staff = _get_personel_options()
    if not staff:
        st.warning("Henuz personel kaydi yok. Önce KIM modulunden personel ekleyin.")
        return None
    options = ["-- Secim yapin --"] + [
        f"{s.get('ad', '')} {s.get('soyad', '')} - {s.get('unvan', s.get('category', ''))}"
        for s in staff
    ]
    idx = st.selectbox(label, range(len(options)), format_func=lambda i: options[i], key=key)
    return staff[idx - 1] if idx > 0 else None


def _calc_kidem(ise_baslama: str) -> str:
    if not ise_baslama:
        return "Bilinmiyor"
    try:
        start = datetime.strptime(ise_baslama[:10], "%Y-%m-%d").date()
        delta = date.today() - start
        yil, kalan = divmod(delta.days, 365)
        ay = kalan // 30
        parts = []
        if yil:
            parts.append(f"{yil} yil")
        if ay:
            parts.append(f"{ay} ay")
        return " ".join(parts) if parts else "Yeni basladi"
    except Exception:
        return "Bilinmiyor"


def _get_tdm_store() -> TDMDataStore:
    base = os.path.join(get_tenant_dir(), "tdm")
    return TDMDataStore(base)


def _get_akademik_store() -> AkademikDataStore:
    base = os.path.join(get_tenant_dir(), "akademik")
    return AkademikDataStore(base)


def _get_demirbas_teslim_durumu(personel_adi: str) -> dict:
    """TDM modulunden calisanin demirbas zimmet/iade durumunu getirir."""
    try:
        tdm = _get_tdm_store()
        zimmetler = tdm.load_objects("zimmet_kayitlari")
        tuketim_zimmetler = tdm.load_objects("tuketim_zimmetleri")

        personel_lower = personel_adi.strip().lower()

        # Demirbas zimmetleri
        kisi_zimmet = [z for z in zimmetler
                       if z.personel_adi.strip().lower() == personel_lower]

        aktif_demirbas = [z for z in kisi_zimmet if z.durum == "Aktif"]
        iade_demirbas = [z for z in kisi_zimmet if z.durum == "İade Edildi"]

        # Tuketim zimmetleri
        kisi_tuketim = [z for z in tuketim_zimmetler
                        if z.personel_adi.strip().lower() == personel_lower]

        aktif_tuketim = [z for z in kisi_tuketim if z.durum == "Aktif"]
        iade_tuketim = [z for z in kisi_tuketim if z.durum == "İade Edildi"]

        toplam_aktif = len(aktif_demirbas) + len(aktif_tuketim)
        toplam_iade = len(iade_demirbas) + len(iade_tuketim)
        toplam = len(kisi_zimmet) + len(kisi_tuketim)

        return {
            "toplam": toplam,
            "aktif": toplam_aktif,
            "iade": toplam_iade,
            "teslim_tamam": toplam > 0 and toplam_aktif == 0,
            "zimmet_yok": toplam == 0,
            "aktif_demirbas": aktif_demirbas,
            "iade_demirbas": iade_demirbas,
            "aktif_tuketim": aktif_tuketim,
            "iade_tuketim": iade_tuketim,
        }
    except Exception:
        return {"toplam": 0, "aktif": 0, "iade": 0, "teslim_tamam": False,
                "zimmet_yok": True, "aktif_demirbas": [], "iade_demirbas": [],
                "aktif_tuketim": [], "iade_tuketim": []}


def _analyze_cv_with_ai(pdf_path: str) -> str:
    """PDF CV dosyasini okur ve OpenAI ile analiz eder."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            return ""

        # OpenAI client
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")

        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return ""

        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""Asagidaki CV metnini analiz et ve su basliklar altinda ozetle.
Turkce yaz. Kisa ve net bilgiler ver.

**Genel Bilgiler:**
- Yas (tahmin)
- Cinsiyet (tahmin)
- Iletisim bilgileri

**Egitim:**
- Universite / Fakulte / Bolum
- Mezuniyet yili
- Ek egitimler / sertifikalar

**Is Deneyimi:**
- Toplam calisma yili (tahmin)
- Calistigi yerler (kurum adi - pozisyon - sure)

**Yetkinlikler:**
- Yabanci diller
- Bilgisayar / teknik beceriler
- Diger onemli yetkinlikler

**Genel Degerlendirme:**
- Guclu yonleri
- Dikkat edilmesi gereken noktalar

CV Metni:
{text[:4000]}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen bir insan kaynaklari uzmanisin. CV'leri analiz edip ozet bilgi cikartiyorsun."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"CV analiz hatasi: {str(e)}"


# ============================================================
# CSS & STIL
# ============================================================

def _inject_ik_css():
    inject_common_css("ik")
    st.markdown("""
    <style>
    :root {
        --ik-primary: #2563eb;
        --ik-primary-dark: #1e40af;
        --ik-primary-light: #60a5fa;
        --ik-success: #10b981;
        --ik-warning: #f59e0b;
        --ik-danger: #ef4444;
        --ik-purple: #8b5cf6;
        --ik-teal: #0d9488;
        --ik-dark: #0B0F19;
    }
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(180deg, #0B0F19 0%, #131825 100%);
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease; border-left: 4px solid #2563eb;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important; font-size: 0.75rem !important;
        font-weight: 600 !important; text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0B0F19 !important; font-weight: 800 !important; font-size: 1.5rem !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
    }
    .stButton > button:not([kind]):hover {
        border-color: #2563eb !important; background: #eff6ff !important;
    }
    details[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important; border-radius: 12px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }
    div[data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important; border-color: #e2e8f0 !important;
    }
    .stDataFrame {
        border-radius: 12px !important; overflow: hidden !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        font-weight: 600 !important;
    }
    hr { border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #cbd5e1 50%, transparent 100%) !important; }
    .stAlert { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# SEKME 1: GENEL BAKIS (DASHBOARD)
# ============================================================

def _render_dashboard(store: IKDataStore):
    candidates = store.load_list("candidates")
    applications = store.load_list("applications")
    interviews = store.load_list("interviews")
    employees = store.load_list("employees")
    reviews = store.load_list("performance_reviews")
    offboardings = store.load_list("offboarding")
    izinler = store.load_list("izinler")

    aktif_adaylar = sum(1 for c in candidates if c.get("status") not in ("Ret", "Ise Alindi"))
    planlanan_mul = sum(1 for i in interviews if i.get("status") in ("Planlandi", "Devam Ediyor"))
    aktif_calisanlar = sum(1 for e in employees if e.get("status") == "Aktif")
    bekleyen_izin = sum(1 for i in izinler if i.get("durum") == "beklemede")

    styled_stat_row([
        ("Aktif Adaylar", aktif_adaylar, "#2563eb", "\U0001f464"),
        ("Planlanan Mulakat", planlanan_mul, "#8b5cf6", "\U0001f3a4"),
        ("Aktif Çalışanlar", aktif_calisanlar, "#10b981", "\U0001f465"),
        ("Bekleyen İzin", bekleyen_izin, "#f59e0b", "\U0001f4cb"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        styled_section("Aday Durum Dagilimi", "#2563eb")
        if candidates:
            status_counts: dict[str, float] = {}
            for cd in candidates:
                s = cd.get("status", "Yeni")
                status_counts[s] = status_counts.get(s, 0) + 1
            st.markdown(
                ReportStyler.donut_chart_svg(status_counts, size=155),
                unsafe_allow_html=True
            )
        else:
            styled_info_banner("Henuz aday kaydi yok.", "info")

    with c2:
        styled_section("Mülakat Karar Dagilimi", "#8b5cf6")
        if interviews:
            karar_counts: dict[str, float] = {}
            for mi in interviews:
                k = mi.get("decision", "") or "Kararsiz"
                karar_counts[k] = karar_counts.get(k, 0) + 1
            st.markdown(
                ReportStyler.donut_chart_svg(karar_counts, size=155),
                unsafe_allow_html=True
            )
        else:
            styled_info_banner("Henuz mulakat kaydi yok.", "info")

    c3, c4 = st.columns(2)
    with c3:
        styled_section("Performans Dagilimi", "#10b981")
        if reviews:
            labels: dict[str, float] = {}
            for r in reviews:
                lb = r.get("label", "?")
                labels[lb] = labels.get(lb, 0) + 1
            st.markdown(
                ReportStyler.horizontal_bar_html(labels, color="#4472C4"),
                unsafe_allow_html=True
            )
        else:
            styled_info_banner("Henuz performans degerlendirmesi yok.", "info")

    with c4:
        styled_section("Son Mulakatlar", "#8b5cf6")
        if interviews:
            son = sorted(interviews, key=lambda x: x.get("interview_date", ""), reverse=True)[:5]
            for m in son:
                st.markdown(f"**{m.get('interview_code', '')}** | Asama {m.get('stage', '')} | "
                            f"{m.get('interview_date', '')} | {m.get('status', '')}")
        else:
            styled_info_banner("Henuz mulakat kaydi yok.", "info")

    # Personel Dagilimi - Sunburst
    staff = _get_personel_options()
    if staff:
        styled_section("Personel Dagilimi (KIM)", "#0d9488")
        cat_counts: dict[str, float] = {}
        cat_persons: dict[str, list[tuple[str, float]]] = {}
        for s in staff:
            cat = s.get("category", "diger")
            label = KATEGORI_MAP.get(cat, ("Diger", "#616161"))[0]
            cat_counts[label] = cat_counts.get(label, 0) + 1
            pname = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or "?"
            cat_persons.setdefault(label, []).append((pname, 1))

        st.markdown(
            ReportStyler.sunburst_chart_svg(
                cat_counts, cat_persons, size=380, title="Personel Kategori Dagilimi"
            ),
            unsafe_allow_html=True
        )


# ============================================================
# SEKME 2: ADAY HAVUZU
# ============================================================

def _render_aday_havuzu(store: IKDataStore):
    sub = st.tabs(["🔍 Aday Arama", "➕ Yeni Aday", "📋 Aday Listesi", "🗄️ Yedek Havuzu"])

    # ---- Aday Arama ----
    with sub[0]:
        styled_section("Aday Arama", "#2563eb")
        arama_tipi = st.radio("Arama Tipi", ["TC Kimlik No", "Ad Soyad"], horizontal=True, key="ik_aday_arama_tip")
        if arama_tipi == "TC Kimlik No":
            tc = st.text_input("TC Kimlik No", key="ik_aday_ara_tc", max_chars=11)
            if tc and len(tc) >= 3:
                sonuclar = store.search_candidates_by_tc(tc)
                if sonuclar:
                    for c in sonuclar:
                        st.markdown(f"**{c.candidate_code}** | {c.tam_ad} | TC: {c.tc_no} | "
                                    f"Tel: {c.telefon} | Durum: {c.status}")
                else:
                    styled_info_banner("Sonuc bulunamadı.", "info")
        else:
            isim = st.text_input("Ad veya Soyad", key="ik_aday_ara_isim")
            if isim and len(isim) >= 2:
                sonuclar = store.search_candidates_by_name(isim)
                if sonuclar:
                    for c in sonuclar:
                        st.markdown(f"**{c.candidate_code}** | {c.tam_ad} | TC: {c.tc_no} | "
                                    f"Tel: {c.telefon} | Durum: {c.status}")
                else:
                    styled_info_banner("Sonuc bulunamadı.", "info")

    # ---- Yeni Aday ----
    with sub[1]:
        styled_section("Yeni Aday Kaydi", "#10b981")

        # Kisisel Bilgiler
        styled_section("Kisisel Bilgiler", "#2563eb")
        k1, k2, k3 = st.columns(3)
        with k1:
            tc_no = st.text_input("TC Kimlik No *", key="ik_aday_tc", max_chars=11)
            ad = st.text_input("Ad *", key="ik_aday_ad")
            soyad = st.text_input("Soyad *", key="ik_aday_soyad")
        with k2:
            cinsiyet = st.selectbox("Cinsiyet", ["", "Erkek", "Kadin"], key="ik_aday_cinsiyet")
            dogum_tarihi = st.date_input("Dogum Tarihi", value=None, key="ik_aday_dogum",
                                          min_value=date(1960, 1, 1), max_value=date.today())
            telefon = st.text_input("Telefon", key="ik_aday_tel")
        with k3:
            email = st.text_input("Email", key="ik_aday_email")
            sehir = st.text_input("Sehir", key="ik_aday_sehir")
            notlar = st.text_area("Notlar", key="ik_aday_notlar", height=80)

        # Egitim Bilgileri
        styled_section("Egitim Bilgileri", "#8b5cf6")
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            universite = st.text_input("Mezun Oldugu Universite", key="ik_aday_uni")
        with e2:
            fakulte = st.text_input("Fakulte", key="ik_aday_fakulte")
        with e3:
            bolum = st.text_input("Bolum", key="ik_aday_bolum")
        with e4:
            mezuniyet_yili = st.text_input("Mezuniyet Yili", key="ik_aday_mezyil", max_chars=4,
                                            help="Ornek: 2020")

        # CV Yükleme & AI Analiz
        styled_section("CV Yükleme & AI Analiz", "#0d9488")
        cv_file = st.file_uploader("CV Dosyası Yükle (PDF)", type=["pdf"], key="ik_aday_cv")

        if cv_file is not None:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(cv_file, allowed_types=["pdf"], max_mb=50)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                cv_file = None

        cv_analiz_text = ""
        if cv_file is not None:
            # CV kaydet
            cv_dir = os.path.join(store.base_path, "cv_dosyalari")
            os.makedirs(cv_dir, exist_ok=True)
            cv_fname = f"cv_{tc_no or 'tmp'}_{uuid.uuid4().hex[:6]}.pdf"
            cv_full_path = os.path.join(cv_dir, cv_fname)
            with open(cv_full_path, "wb") as f:
                f.write(cv_file.getvalue())
            styled_info_banner(f"CV yuklendi: {cv_fname}", "success")

            # AI Analiz butonu
            if st.button("AI ile CV Analiz Et", key="ik_aday_cv_ai", type="secondary"):
                with st.spinner("CV analiz ediliyor..."):
                    cv_analiz_text = _analyze_cv_with_ai(cv_full_path)
                    if cv_analiz_text:
                        st.session_state["ik_cv_analiz_sonuc"] = cv_analiz_text
                    else:
                        st.warning("CV analiz edilemedi. OpenAI API anahtarini kontrol edin.")

            # Onceki analiz sonucunu goster
            if st.session_state.get("ik_cv_analiz_sonuc"):
                cv_analiz_text = st.session_state["ik_cv_analiz_sonuc"]
                st.markdown(f"""<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);
                border-radius:14px;padding:20px;margin:10px 0;border-left:5px solid #10b981;">
                <div style="font-weight:700;font-size:1rem;color:#059669;margin-bottom:8px;">
                AI CV Analiz Sonucu</div>
                <div style="font-size:0.9rem;color:#94A3B8;white-space:pre-wrap;">{cv_analiz_text}</div>
                </div>""", unsafe_allow_html=True)
        else:
            cv_full_path = ""

        # Basvuru bilgileri
        styled_section("Basvuru Bilgileri", "#8b5cf6")

        # Pozisyon listesi: Varsayilan okul pozisyonlari + IK pozisyonlari + Yeni Pozisyon Ekle
        positions = store.load_objects("positions")
        aktif_pos = [p for p in positions if p.is_active]

        # Varsayilan okul pozisyonlari (label, scope)
        _DEFAULT_POSITIONS = [
            ("Kurucu", "MANAGEMENT"),
            ("Genel Müdür", "MANAGEMENT"),
            ("Genel Müdür Yardımcısı", "MANAGEMENT"),
            ("Kampüs Müdürü", "MANAGEMENT"),
            ("Kurucu Danışmanı", "MANAGEMENT"),
            ("Stajer", "TEACHER"),
            ("Öğretmen", "TEACHER"),
            ("Ücretli Öğretmen", "TEACHER"),
            ("Usta Öğretici", "TEACHER"),
            ("Uzman Öğretici", "TEACHER"),
            ("Danışman", "ADMIN"),
        ]

        # IK pozisyon isimlerini al (cakisma onleme)
        ik_pos_names = {p.position_name.lower() for p in aktif_pos}

        # Varsayilan pozisyonlari olustur (IK'da olmayanlari ekle)
        default_items = []  # (label, name, scope)
        for pos_name, scope in _DEFAULT_POSITIONS:
            if pos_name.lower() not in ik_pos_names:
                default_items.append((pos_name, pos_name, scope))

        # Birlestir: Bos + IK + Varsayilan + Yeni Ekle
        _pos_options = []  # (label, type, data)
        _pos_options.append(("-- Pozisyon secin --", "none", None))
        for p in aktif_pos:
            _pos_options.append((f"{p.position_code} - {p.position_name}", "ik", p))
        for label, name, scope in default_items:
            _pos_options.append((label, "default", {"name": name, "scope": scope}))
        _pos_options.append(("+ Yeni Pozisyon Ekle", "new", None))

        pos_labels = [opt[0] for opt in _pos_options]
        pos_idx = st.selectbox("Pozisyon *", range(len(pos_labels)),
                               format_func=lambda i: pos_labels[i], key="ik_aday_poz")
        _sel_type = _pos_options[pos_idx][1]
        _sel_data = _pos_options[pos_idx][2]

        # Yeni Pozisyon inline form
        new_pos_input = {}
        if _sel_type == "new":
            styled_section("Yeni Pozisyon Tanımla", "#10b981")
            np1, np2, np3 = st.columns(3)
            with np1:
                new_pos_input["name"] = st.text_input("Pozisyon Adi *", key="ik_aday_newpos_name")
            with np2:
                new_pos_input["cat"] = st.text_input("Kategori", key="ik_aday_newpos_cat")
            with np3:
                new_pos_input["scope"] = st.selectbox("Role Scope", ROLE_SCOPES, key="ik_aday_newpos_scope")

        # Ogretmen pozisyonu mu kontrol et
        _is_teacher_pos = False
        if _sel_type == "ik" and _sel_data:
            _is_teacher_pos = getattr(_sel_data, "role_scope", "") == "TEACHER"
        elif _sel_type == "default" and isinstance(_sel_data, dict):
            _is_teacher_pos = _sel_data.get("scope") == "TEACHER"

        # Brans secimi - Ogretmen pozisyonunda dropdown, digerleri text
        if _is_teacher_pos:
            _BRANSLAR = ["-- Branş Seçin --"] + list(OGRETMEN_BRANSLARI) + ["+ Yeni Branş Ekle"]
            brans_idx = st.selectbox("Branş *", range(len(_BRANSLAR)),
                                     format_func=lambda i: _BRANSLAR[i], key="ik_aday_brans_sel")
            if brans_idx > 0 and _BRANSLAR[brans_idx] == "+ Yeni Branş Ekle":
                brans = st.text_input("Yeni Branş Adi *", key="ik_aday_brans_yeni",
                                      placeholder="Ornegin: Arapca, Japonca vb.")
            elif brans_idx > 0:
                brans = _BRANSLAR[brans_idx]
            else:
                brans = ""
        else:
            brans = st.text_input("Branşı", key="ik_aday_brans",
                                  help="Ornegin: Matematik, Turkce, Ingilizce vb.")

        cb1, cb2 = st.columns(2)
        with cb1:
            kampus = st.text_input("Kampus", value="TUMU", key="ik_aday_kampus")
        with cb2:
            kademe = st.text_input("Kademe", value="TUMU", key="ik_aday_kademe")

        if st.button("Aday Kaydet", type="primary", key="ik_aday_kaydet"):
            if not tc_no or not ad or not soyad:
                st.error("TC Kimlik No, Ad ve Soyad zorunludur.")
            elif len(tc_no) != 11:
                st.error("TC Kimlik No 11 haneli olmalidir.")
            elif _sel_type == "none":
                st.error("Pozisyon secimi zorunludur.")
            elif _sel_type == "new" and not new_pos_input.get("name"):
                st.error("Yeni pozisyon adi zorunludur.")
            elif _is_teacher_pos and not brans:
                st.error("Öğretmen pozisyonu için brans secimi zorunludur.")
            else:
                is_blocked, msg = store.check_duplicate_candidate(tc_no, ad, soyad, telefon, email)
                if is_blocked:
                    st.error(msg)
                else:
                    if msg:
                        st.warning(msg)
                    cand = Candidate(
                        candidate_code=store.next_candidate_code(),
                        tc_no=tc_no, ad=ad, soyad=soyad,
                        cinsiyet=cinsiyet,
                        dogum_tarihi=dogum_tarihi.isoformat() if dogum_tarihi else "",
                        telefon=telefon, email=email, sehir=sehir,
                        brans=brans,
                        universite=universite, fakulte=fakulte,
                        bolum=bolum, mezuniyet_yili=mezuniyet_yili,
                        cv_path=cv_full_path if cv_file else "",
                        cv_analiz=cv_analiz_text or st.session_state.get("ik_cv_analiz_sonuc", ""),
                        notlar=notlar,
                    )
                    store.upsert("candidates", cand)
                    AuditLogger.log(store, "aday_eklendi", "candidate", cand.id, cand.tam_ad)

                    # Pozisyon belirle ve basvuru olustur
                    pos_to_use = None

                    if _sel_type == "ik":
                        # Mevcut IK pozisyonu
                        pos_to_use = _sel_data

                    elif _sel_type == "default" and isinstance(_sel_data, dict):
                        # Varsayilan pozisyon -> IK'ya otomatik ekle
                        existing = store.get_by_field("positions", "position_name", _sel_data["name"])
                        if existing:
                            pos_to_use = Position.from_dict(existing) if isinstance(existing, dict) else existing
                        else:
                            all_codes = [d.get("position_code", "") for d in store.load_list("positions")]
                            nums = []
                            for c in all_codes:
                                try:
                                    nums.append(int(c.split("-")[-1]))
                                except (ValueError, IndexError):
                                    pass
                            nxt = max(nums) + 1 if nums else 1
                            pos_to_use = Position(
                                position_code=f"POS-{str(nxt).zfill(3)}",
                                position_name=_sel_data["name"],
                                category="diger",
                                role_scope=_sel_data["scope"],
                            )
                            store.upsert("positions", pos_to_use)

                    elif _sel_type == "new" and new_pos_input.get("name"):
                        # Yeni pozisyon olustur
                        all_codes = [d.get("position_code", "") for d in store.load_list("positions")]
                        nums = []
                        for c in all_codes:
                            try:
                                nums.append(int(c.split("-")[-1]))
                            except (ValueError, IndexError):
                                pass
                        nxt = max(nums) + 1 if nums else 1
                        pos_to_use = Position(
                            position_code=f"POS-{str(nxt).zfill(3)}",
                            position_name=new_pos_input["name"],
                            category=new_pos_input.get("cat", ""),
                            role_scope=new_pos_input.get("scope", "ALL"),
                        )
                        store.upsert("positions", pos_to_use)

                    if pos_to_use:
                        app = Application(
                            application_code=store.next_application_code(),
                            candidate_id=cand.id, candidate_code=cand.candidate_code,
                            position_id=pos_to_use.id, position_code=pos_to_use.position_code,
                            kampus=kampus, kademe=kademe,
                        )
                        store.upsert("applications", app)
                        AuditLogger.log(store, "basvuru_oluşturuldu", "application", app.id, app.application_code)
                        cand.status = "Mulakat Planlandi"
                        cand.updated_at = _now_str()
                        store.upsert("candidates", cand)

                    styled_info_banner(f"Aday kaydedildi: {cand.candidate_code} - {cand.tam_ad}", "success")
                    st.rerun()

    # ---- Aday Listesi ----
    with sub[2]:
        styled_section("Aday Listesi", "#1e40af")
        candidates = store.load_objects("candidates")

        # Istatistikler
        if candidates:
            durum_counts: dict[str, int] = {}
            for cd in candidates:
                durum_counts[cd.status] = durum_counts.get(cd.status, 0) + 1
            styled_stat_row([
                ("Toplam Aday", len(candidates), "#2563eb", "\U0001f464"),
                ("Yeni", durum_counts.get("Yeni", 0), "#10b981", "\U0001f195"),
                ("Mulakatta", durum_counts.get("Mulakat Planlandi", 0), "#8b5cf6", "\U0001f3a4"),
                ("Ise Alindi", durum_counts.get("Ise Alindi", 0), "#059669", "\u2705"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

        fc1, fc2 = st.columns(2)
        with fc1:
            durum_f = st.selectbox("Durum Filtre", ["Tümü"] + CANDIDATE_STATUSES, key="ik_aday_liste_durum")
        with fc2:
            arama_f = st.text_input("Ara (ad/soyad)", key="ik_aday_liste_ara")

        filtered = candidates
        if durum_f != "Tümü":
            filtered = [cd for cd in filtered if cd.status == durum_f]
        if arama_f:
            q = arama_f.lower()
            filtered = [cd for cd in filtered if q in cd.tam_ad.lower()]

        if filtered:
            df = pd.DataFrame([{
                "Kod": cd.candidate_code,
                "Ad Soyad": cd.tam_ad,
                "Cinsiyet": getattr(cd, "cinsiyet", "") or "-",
                "Telefon": cd.telefon or "-",
                "Email": cd.email or "-",
                "Universite": getattr(cd, "universite", "") or "-",
                "Bolum": getattr(cd, "bolum", "") or "-",
                "Durum": cd.status,
            } for cd in filtered])
            st.dataframe(df, hide_index=True, use_container_width=True)

            # Aday Detay
            styled_section("Aday Detay", "#8b5cf6")
            aday_labels = [f"{cd.candidate_code} - {cd.tam_ad}" for cd in filtered]
            sel_idx = st.selectbox("Aday secin", range(len(aday_labels)),
                                   format_func=lambda i: aday_labels[i], key="ik_aday_gunc_sec")
            sel_cand = filtered[sel_idx]

            # Bilgi karti
            _cin = getattr(sel_cand, "cinsiyet", "") or "-"
            _dog = getattr(sel_cand, "dogum_tarihi", "") or "-"
            _uni = getattr(sel_cand, "universite", "") or "-"
            _fak = getattr(sel_cand, "fakulte", "") or "-"
            _bol = getattr(sel_cand, "bolum", "") or "-"
            _mez = getattr(sel_cand, "mezuniyet_yili", "") or "-"

            st.markdown(f"""<div style="background:linear-gradient(135deg,#0B0F19 0%,#e2e8f0 100%);
            border-radius:14px;padding:20px;margin:10px 0;border-left:5px solid #2563eb;">
            <div style="font-weight:800;font-size:1.2rem;color:#94A3B8;">{sel_cand.tam_ad}</div>
            <div style="font-size:0.85rem;color:#64748b;margin-top:2px;">
            {sel_cand.candidate_code} | TC: {sel_cand.tc_no} | Durum: {sel_cand.status}
            </div></div>""", unsafe_allow_html=True)

            dc1, dc2, dc3 = st.columns(3)
            with dc1:
                st.markdown("**Kisisel Bilgiler**")
                st.write(f"**Cinsiyet:** {_cin}")
                st.write(f"**Dogum Tarihi:** {_dog}")
                st.write(f"**Telefon:** {sel_cand.telefon or '-'}")
                st.write(f"**Email:** {sel_cand.email or '-'}")
                st.write(f"**Sehir:** {sel_cand.sehir or '-'}")
            with dc2:
                st.markdown("**Egitim Bilgileri**")
                st.write(f"**Universite:** {_uni}")
                st.write(f"**Fakulte:** {_fak}")
                st.write(f"**Bolum:** {_bol}")
                st.write(f"**Mezuniyet Yili:** {_mez}")
                st.write(f"**Branş:** {sel_cand.brans or '-'}")
            with dc3:
                st.markdown("**Basvuru Bilgileri**")
                st.write(f"**Durum:** {sel_cand.status}")
                st.write(f"**Kayıt Tarihi:** {sel_cand.created_at[:10] if sel_cand.created_at else '-'}")
                if sel_cand.notlar:
                    st.write(f"**Notlar:** {sel_cand.notlar}")

            # CV Analiz Sonucu
            _cv_analiz = getattr(sel_cand, "cv_analiz", "") or ""
            if _cv_analiz:
                styled_section("AI CV Analiz Sonucu", "#0d9488")
                st.markdown(f"""<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);
                border-radius:12px;padding:16px;margin:8px 0;border-left:5px solid #10b981;">
                <div style="font-size:0.9rem;color:#94A3B8;white-space:pre-wrap;">{_cv_analiz}</div>
                </div>""", unsafe_allow_html=True)

            # Durum guncelleme
            st.markdown("---")
            gu_c1, gu_c2 = st.columns([2, 1])
            with gu_c1:
                yeni_durum = st.selectbox("Yeni Durum", CANDIDATE_STATUSES, key="ik_aday_gunc_durum")
            with gu_c2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Durumu Güncelle", key="ik_aday_gunc_btn", type="primary"):
                    sel_cand.status = yeni_durum
                    sel_cand.updated_at = _now_str()
                    store.upsert("candidates", sel_cand)
                    styled_info_banner(f"{sel_cand.tam_ad} durumu güncellendi: {yeni_durum}", "success")
                    st.rerun()
        else:
            styled_info_banner("Aday bulunamadı.", "info")

    # ---- Yedek Havuzu ----
    with sub[3]:
        styled_section("Yedek Havuzu", "#f59e0b")
        yedekler = [cd for cd in store.load_objects("candidates") if cd.status == "Yedek"]
        if yedekler:
            df = pd.DataFrame([{
                "Kod": cd.candidate_code,
                "Ad Soyad": cd.tam_ad,
                "TC": cd.tc_no,
                "Telefon": cd.telefon,
                "Universite": getattr(cd, "universite", "") or "-",
                "Bolum": getattr(cd, "bolum", "") or "-",
                "Notlar": cd.notlar,
            } for cd in yedekler])
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Yedek havuzunda aday yok.", "info")


# ============================================================
# SEKME 3: MULAKAT YONETIMI
# ============================================================


def _generate_ai_oneri(puan_pct: float, score_objs: list, stage: int,
                       combined_pct: float | None = None) -> str:
    """Mulakat puanlarina gore AI onerisi uretir."""
    total_q = len(score_objs)
    if total_q == 0:
        return "Puan verisi bulunamadı."
    excellent = sum(1 for s in score_objs if s.score >= 4)
    good = sum(1 for s in score_objs if s.score == 3)
    poor = sum(1 for s in score_objs if s.score <= 2)

    # Kategori bazli analiz
    std_scores = [s for s in score_objs if s.set_code not in ("REASK", "CUSTOM")]
    reask_scores = [s for s in score_objs if s.set_code == "REASK"]
    custom_scores = [s for s in score_objs if s.set_code == "CUSTOM"]

    lines = []

    # Genel degerlendirme
    if puan_pct >= 80:
        lines.append(f"<b>Güçlü Performans:</b> Aday %{puan_pct:.0f} basari orani ile guclu bir mulakat performansi sergilemistir.")
        lines.append(f"{total_q} sorudan {excellent} tanesinde yuksek puan (4-5/5) almistir.")
    elif puan_pct >= 65:
        lines.append(f"<b>Iyi Performans:</b> Aday %{puan_pct:.0f} basari orani ile ortalamanin uzerinde performans gostermistir.")
        if poor > 0:
            lines.append(f"Ancak {poor} soruda dusuk puan almistir; bu alanlar degerlendirilmelidir.")
    elif puan_pct >= 50:
        lines.append(f"<b>Orta Performans:</b> Aday %{puan_pct:.0f} basari orani ile orta duzey performans gostermistir.")
        lines.append(f"{poor} soruda zayif, {excellent} soruda guclu puan almistir.")
    else:
        lines.append(f"<b>Dusuk Performans:</b> Aday %{puan_pct:.0f} basari orani ile beklentilerin altinda kalmistir.")
        lines.append(f"{poor} soruda yetersiz puan almistir.")

    # Tekrar sorulan soru analizi
    if reask_scores:
        reask_avg = sum(s.score for s in reask_scores) / len(reask_scores)
        if std_scores:
            std_avg = sum(s.score for s in std_scores) / len(std_scores)
            diff = reask_avg - std_avg
            if diff > 0.5:
                lines.append(f"Tekrar sorulan sorularda onceki mulakattan daha iyi performans gostermistir (Ort: {reask_avg:.1f}/5).")
            elif diff < -0.5:
                lines.append(f"Tekrar sorulan sorularda onceki mulakattan daha dusuk performans gostermistir (Ort: {reask_avg:.1f}/5).")
            else:
                lines.append(f"Tekrar sorulan sorularda tutarli performans sergilemistir (Ort: {reask_avg:.1f}/5).")

    # Yeni soru analizi
    if custom_scores:
        custom_avg = sum(s.score for s in custom_scores) / len(custom_scores)
        lines.append(f"Ek sorularda ortalama {custom_avg:.1f}/5 puan almistir.")

    # Tum mulakat ortalamasi
    if combined_pct is not None:
        if combined_pct >= 70:
            lines.append(f"<b>Genel Değerlendirme:</b> Tüm mulakatlar genelinde %{combined_pct:.0f} basari orani ile guclu bir aday profili cikmaktadir.")
        elif combined_pct >= 50:
            lines.append(f"<b>Genel Değerlendirme:</b> Tüm mulakatlar genelinde %{combined_pct:.0f} basari orani ile orta duzeyde bir performans sergilemistir.")
        else:
            lines.append(f"<b>Genel Değerlendirme:</b> Tüm mulakatlar genelinde %{combined_pct:.0f} basari oraniyla dusuk performans gorulmektedir.")

    # Oneri
    lines.append("")
    if puan_pct >= 75:
        lines.append("<b>Oneri:</b> Ise alim için uygun gorulmektedir.")
    elif puan_pct >= 60 and stage < 3:
        lines.append(f"<b>Oneri:</b> Ek degerlendirme için {stage + 1}. mulakat yapilmasi onerilir.")
    elif puan_pct >= 50:
        lines.append("<b>Oneri:</b> Karar için ek mulakat veya referans kontrolu onerilir.")
    else:
        lines.append("<b>Oneri:</b> Ise alim onerilmemektedir.")

    return "<br>".join(lines)


def _render_mulakat_stage_results(store: IKDataStore, target_stage: int):
    """Belirli bir asama için tamamlanmis mulakat sonuclarini gosterir."""
    _stage_colors = {1: "#2563eb", 2: "#8b5cf6", 3: "#0d9488"}
    _stg_clr = _stage_colors.get(target_stage, "#2563eb")
    _key_pfx = f"mr{target_stage}"

    interviews = store.load_objects("interviews")
    sonuc_intvs = [i for i in interviews if i.stage == target_stage and
                   (i.status == "Tamamlandı" or i.decision)]
    if not sonuc_intvs:
        return

    st.markdown("---")
    styled_section(f"{target_stage}. Mulakat Sonuclari", _stg_clr)

    candidates = store.load_objects("candidates")
    cand_map = {c.id: c for c in candidates}
    applications = store.load_objects("applications")
    app_map = {a.candidate_id: a for a in applications}
    positions = store.load_objects("positions")
    pos_map = {p.position_code: p for p in positions}

    # Aday listesi
    s_labels = []
    for iv in sonuc_intvs:
        c = cand_map.get(iv.candidate_id)
        karar_badge = f" [{iv.decision}]" if iv.decision else ""
        s_labels.append(f"{iv.interview_code} - {c.tam_ad if c else '?'}{karar_badge}")
    s_idx = st.selectbox("Sonuc Görüntüle", range(len(s_labels)),
                         format_func=lambda i: s_labels[i], key=f"ik_{_key_pfx}_sec")
    sel_intv = sonuc_intvs[s_idx]
    sel_cand = cand_map.get(sel_intv.candidate_id)

    # Pozisyon/Brans bilgi karti
    _app = app_map.get(sel_intv.candidate_id)
    _pos = pos_map.get(_app.position_code) if _app else None
    _pos_name = _pos.position_name if _pos else "-"
    _brans = sel_cand.brans if sel_cand else "-"
    _kat = ", ".join(sel_intv.interviewer_names) if sel_intv.interviewer_names else "-"

    _res_info_html = (
        f'<div style="background:linear-gradient(135deg,#111827 0%,#1A2035 100%);'
        f'border-radius:14px;padding:16px 20px;margin:10px 0;border-left:5px solid {_stg_clr};">'
        f'<div style="display:flex;gap:24px;flex-wrap:wrap;">'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ADAY</div>'
        f'<div style="font-size:15px;font-weight:700;color:#94A3B8;">{sel_cand.tam_ad if sel_cand else "?"}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">POZISYON</div>'
        f'<div style="font-size:15px;font-weight:700;color:#2563eb;">{_pos_name}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">BRANS</div>'
        f'<div style="font-size:15px;font-weight:700;color:#8b5cf6;">{_brans or "-"}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">MULAKATCILAR</div>'
        f'<div style="font-size:13px;font-weight:600;color:#94A3B8;">{_kat}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">TARIH</div>'
        f'<div style="font-size:13px;font-weight:600;color:#94A3B8;">{sel_intv.interview_date or "-"} {sel_intv.interview_time or ""}</div></div>'
        f'</div></div>'
    )
    st.markdown(_res_info_html, unsafe_allow_html=True)

    # Puanlar
    raw_scores = store.find_by_field("interview_scores", "interview_id", sel_intv.id)
    if not raw_scores:
        styled_info_banner("Bu mulakat için puan kaydi bulunamadı.", "warning")
        return

    score_objs = sorted(
        [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in raw_scores],
        key=lambda x: x.order_no
    )
    total = sum(s.score for s in score_objs)
    max_puan = len(score_objs) * 5
    avg = total / len(score_objs) if score_objs else 0
    puan_pct = (total / max_puan * 100) if max_puan > 0 else 0
    puan_clr = "#10b981" if puan_pct >= 70 else ("#f59e0b" if puan_pct >= 50 else "#ef4444")

    # Stat kartlari
    styled_stat_row([
        ("Toplam Puan", f"{total}/{max_puan}", puan_clr, "\U0001f4ca"),
        ("Ortalama", f"{avg:.2f}/5", "#2563eb", "\U0001f4c8"),
        ("Başarı", f"%{puan_pct:.0f}", puan_clr, "\U0001f3af"),
        ("Soru Sayısı", len(score_objs), "#8b5cf6", "\U0001f4dd"),
    ])

    # ---- Tum mulakatlarin ortalamasi (birden fazla mulakat varsa) ----
    all_cand_intvs = sorted(
        [iv for iv in interviews if iv.candidate_id == sel_intv.candidate_id
         and (iv.status == "Tamamlandı" or iv.decision)],
        key=lambda x: x.stage
    )
    combined_pct = None
    if len(all_cand_intvs) > 1:
        _all_scores = []
        _stage_summaries = []
        for iv in all_cand_intvs:
            iv_raw = store.find_by_field("interview_scores", "interview_id", iv.id)
            if iv_raw:
                iv_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in iv_raw]
                _all_scores.extend(iv_objs)
                iv_total = sum(s.score for s in iv_objs)
                iv_max = len(iv_objs) * 5
                iv_pct = (iv_total / iv_max * 100) if iv_max > 0 else 0
                iv_clr = "#10b981" if iv_pct >= 70 else ("#f59e0b" if iv_pct >= 50 else "#ef4444")
                _stage_summaries.append(
                    f"<span style='font-weight:600;'>{iv.stage}. Mulakat:</span> "
                    f"<span style='color:{iv_clr};font-weight:700;'>{iv_total}/{iv_max} (%{iv_pct:.0f})</span>"
                )
        if _all_scores:
            c_total = sum(s.score for s in _all_scores)
            c_max = len(_all_scores) * 5
            c_avg = c_total / len(_all_scores)
            combined_pct = (c_total / c_max * 100) if c_max > 0 else 0
            c_clr = "#10b981" if combined_pct >= 70 else ("#f59e0b" if combined_pct >= 50 else "#ef4444")
            _comb_html = (
                f'<div style="background:linear-gradient(135deg,#fefce8 0%,#fef9c3 100%);'
                f'border-radius:12px;padding:16px 20px;margin:12px 0;border-left:5px solid #eab308;">'
                f'<div style="font-weight:700;color:#854d0e;font-size:14px;margin-bottom:8px;">'
                f'Tüm Mulakatlarin Ortalaması ({len(all_cand_intvs)} mulakat)</div>'
                f'<div style="display:flex;gap:28px;flex-wrap:wrap;margin-bottom:8px;">'
                f'<div>Toplam: <b>{c_total}/{c_max}</b></div>'
                f'<div>Ortalama: <b style="color:{c_clr};">{c_avg:.2f}/5</b></div>'
                f'<div>Başarı: <b style="color:{c_clr};">%{combined_pct:.0f}</b></div>'
                f'</div>'
                f'<div style="font-size:12px;color:#78350f;">{"&nbsp;|&nbsp;".join(_stage_summaries)}</div>'
                f'</div>'
            )
            st.markdown(_comb_html, unsafe_allow_html=True)

    # ---- Grafikler ----
    gc1, gc2 = st.columns(2)

    with gc1:
        # Donut: Kategori bazli puan dagilimi
        cat_totals = {}
        cat_max = {}
        for s in score_objs:
            cat = {"REASK": "Tekrar Soru", "CUSTOM": "Yeni Soru"}.get(s.set_code, "Standart Soru")
            cat_totals[cat] = cat_totals.get(cat, 0) + s.score
            cat_max[cat] = cat_max.get(cat, 0) + 5
        st.markdown(
            ReportStyler.donut_chart_svg(cat_totals, size=155),
            unsafe_allow_html=True
        )

    with gc2:
        # Bar: Soru bazli puanlar
        q_data = {}
        for s in score_objs[:20]:
            label = f"S{s.order_no}"
            q_data[label] = float(s.score)
        if q_data:
            st.markdown(
                ReportStyler.horizontal_bar_html(q_data, color=_stg_clr, max_width_px=300),
                unsafe_allow_html=True
            )

    # Puan dagilimi bar (5/5, 4/5, 3/5, 2/5, 1/5, 0/5)
    dist = {}
    for p in range(5, -1, -1):
        cnt = sum(1 for s in score_objs if s.score == p)
        if cnt > 0:
            dist[f"{p}/5 Puan"] = float(cnt)
    if dist:
        st.markdown(
            ReportStyler.horizontal_bar_html(dist, color="#64748b", max_width_px=400),
            unsafe_allow_html=True
        )

    # ---- Genel not ----
    if sel_intv.general_note:
        _gnot_html = (
            f'<div style="background:#111827;border-radius:10px;padding:10px 14px;margin:8px 0;'
            f'border:1px solid #e2e8f0;">'
            f'<span style="font-size:11px;color:#64748b;font-weight:600;">GENEL NOT:</span>'
            f'<div style="font-size:13px;color:#94A3B8;margin-top:4px;">{sel_intv.general_note}</div>'
            f'</div>'
        )
        st.markdown(_gnot_html, unsafe_allow_html=True)

    # ---- AI Onerisi ----
    styled_section("AI Onerisi", "#1e40af")
    oneri = _generate_ai_oneri(puan_pct, score_objs, target_stage, combined_pct)
    _ai_html = (
        f'<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 100%);'
        f'border-radius:14px;padding:18px 22px;margin:10px 0;border-left:5px solid #1e40af;">'
        f'<div style="font-size:13px;color:#94A3B8;line-height:1.8;">{oneri}</div>'
        f'</div>'
    )
    st.markdown(_ai_html, unsafe_allow_html=True)

    # ---- Karar ver (karar verilmemisse) ----
    if not sel_intv.decision:
        styled_section("Karar Ver", "#10b981")

        _KARAR_RENK = {
            "Ise Alindi": ("#10b981", "#059669", "\u2705"),
            "2. Mülakata Devam": ("#2563eb", "#1d4ed8", "\u27a1\ufe0f"),
            "3. Mülakata Devam": ("#0d9488", "#0f766e", "\u27a1\ufe0f"),
            "Beklemede": ("#f59e0b", "#d97706", "\u23f3"),
            "Ret": ("#ef4444", "#dc2626", "\u274c"),
            "Yedek": ("#8b5cf6", "#7c3aed", "\U0001f4cb"),
        }
        _uygun = {}
        for k, v in _KARAR_RENK.items():
            if k == "2. Mülakata Devam" and target_stage >= 2:
                continue
            if k == "3. Mülakata Devam" and target_stage >= 3:
                continue
            _uygun[k] = v

        # Renkli karar kartlari
        _karar_cards = "".join([
            f'<div style="background:linear-gradient(135deg,{v[0]} 0%,{v[1]} 100%);'
            f'border-radius:10px;padding:10px 14px;flex:1;min-width:110px;text-align:center;">'
            f'<div style="font-size:1.2rem;">{v[2]}</div>'
            f'<div style="font-weight:700;color:#fff;font-size:0.8rem;">{k}</div></div>'
            for k, v in _uygun.items()
        ])
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0;">{_karar_cards}</div>',
            unsafe_allow_html=True
        )

        karar = st.selectbox("Karar", list(_uygun.keys()), key=f"ik_{_key_pfx}_karar")
        karar_notu = st.text_area("Karar Notu", key=f"ik_{_key_pfx}_knot", height=60)

        if st.button("Karari Kaydet", type="primary", key=f"ik_{_key_pfx}_kbtn"):
            sel_intv.decision = karar
            if karar_notu:
                sel_intv.general_note = (sel_intv.general_note or "") + f"\n\nKarar Notu: {karar_notu}"
            sel_intv.updated_at = _now_str()
            store.upsert("interviews", sel_intv)

            cand = cand_map.get(sel_intv.candidate_id)
            if karar in ("2. Mülakata Devam", "3. Mülakata Devam"):
                yeni_asama = 2 if karar == "2. Mülakata Devam" else 3
                yeni_intv = Interview(
                    interview_code=store.next_interview_code(),
                    application_id=sel_intv.application_id,
                    application_code=sel_intv.application_code,
                    candidate_id=sel_intv.candidate_id,
                    stage=yeni_asama,
                    status="Planlandi",
                )
                store.upsert("interviews", yeni_intv)
                if cand:
                    cand.status = f"{yeni_asama}. Mulakat Planlandi"
                    cand.updated_at = _now_str()
                    store.upsert("candidates", cand)
                styled_info_banner(f"{karar} - {yeni_intv.interview_code} oluşturuldu.", "success")
            else:
                if cand:
                    _status_map = {"Ise Alindi": "Ise Alindi", "Ret": "Ret",
                                   "Yedek": "Yedek", "Beklemede": "Beklemede"}
                    cand.status = _status_map.get(karar, cand.status)
                    cand.updated_at = _now_str()
                    store.upsert("candidates", cand)
                styled_info_banner(f"Karar kaydedildi: {karar}", "success")

            AuditLogger.log(store, "karar_verildi", "interview", sel_intv.id,
                            f"{sel_intv.interview_code}: {karar}")
            st.rerun()
    elif sel_intv.decision:
        # Karar verilmis - goster
        _d_icon = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                    "Beklemede": "\u23f3", "2. Mülakata Devam": "\u27a1\ufe0f",
                    "3. Mülakata Devam": "\u27a1\ufe0f"}.get(sel_intv.decision, "")
        _d_clr = {"Ise Alindi": "#10b981", "Ret": "#ef4444", "Yedek": "#8b5cf6",
                   "Beklemede": "#f59e0b"}.get(sel_intv.decision, "#2563eb")
        _dec_html = (
            f'<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);'
            f'border-radius:12px;padding:14px 18px;margin:12px 0;border-left:5px solid {_d_clr};">'
            f'<span style="font-size:1.3rem;">{_d_icon}</span>'
            f'<span style="font-size:15px;font-weight:700;color:{_d_clr};margin-left:8px;">'
            f'Karar: {sel_intv.decision}</span>'
            f'</div>'
        )
        st.markdown(_dec_html, unsafe_allow_html=True)


def _render_mulakat_stage_scoring(store: IKDataStore, target_stage: int):
    """Belirli bir asama için mulakat puanlama ekranini olusturur.

    target_stage: 1, 2 veya 3
    """
    _stage_colors = {1: "#2563eb", 2: "#8b5cf6", 3: "#0d9488"}
    _stg_clr = _stage_colors.get(target_stage, "#2563eb")
    _key_pfx = f"ms{target_stage}"

    interviews = store.load_objects("interviews")
    puanlanacak = [i for i in interviews if i.status in ("Planlandi", "Devam Ediyor") and i.stage == target_stage]

    if not puanlanacak:
        styled_info_banner(f"{target_stage}. mulakat puanlanacak aday yok.", "info")
        return

    candidates = store.load_objects("candidates")
    cand_map = {c.id: c for c in candidates}
    int_labels = []
    for iv in puanlanacak:
        c = cand_map.get(iv.candidate_id)
        int_labels.append(f"{iv.interview_code} - {c.tam_ad if c else '?'}")
    int_idx = st.selectbox("Mulakat Secin", range(len(int_labels)),
                           format_func=lambda i: int_labels[i], key=f"ik_{_key_pfx}_sec")
    sel_intv = puanlanacak[int_idx]

    # Pozisyon ve soru seti bul
    app = store.get_by_id("applications", sel_intv.application_id)
    if not app:
        app = store.get_by_field("applications", "application_code", sel_intv.application_code)
    position = None
    _pos_name = "-"
    _brans_val = "-"
    if app:
        app_obj = Application.from_dict(app) if isinstance(app, dict) else app
        position = store.get_by_field("positions", "position_code", app_obj.position_code)
        if position and isinstance(position, dict):
            position = Position.from_dict(position)
        if position:
            _pos_name = position.position_name

    _cand = cand_map.get(sel_intv.candidate_id)
    if _cand:
        _brans_val = _cand.brans or "-"

    # Bilgi karti
    _info_card_html = (
        f'<div style="background:linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%);'
        f'border-radius:14px;padding:16px 20px;margin:10px 0;border-left:5px solid {_stg_clr};">'
        f'<div style="display:flex;gap:30px;flex-wrap:wrap;">'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ADAY</div>'
        f'<div style="font-size:15px;font-weight:700;color:#94A3B8;">{_cand.tam_ad if _cand else "?"}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">POZISYON</div>'
        f'<div style="font-size:15px;font-weight:700;color:#2563eb;">{_pos_name}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">BRANS</div>'
        f'<div style="font-size:15px;font-weight:700;color:#8b5cf6;">{_brans_val}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ASAMA</div>'
        f'<div style="font-size:15px;font-weight:700;color:{_stg_clr};">{target_stage}. Mulakat</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">TARIH</div>'
        f'<div style="font-size:15px;font-weight:700;color:#94A3B8;">{sel_intv.interview_date or "-"} {sel_intv.interview_time or ""}</div></div>'
        f'</div></div>'
    )
    st.markdown(_info_card_html, unsafe_allow_html=True)

    # Mulakatci bilgisi
    if sel_intv.interviewer_names:
        _kat_html = " | ".join([f"<b>{n}</b>" for n in sel_intv.interviewer_names])
        _mkat_html = (
            f'<div style="background:#111827;border-radius:10px;padding:10px 16px;margin:6px 0;'
            f'border:1px solid #e2e8f0;">'
            f'<span style="font-size:11px;color:#64748b;font-weight:600;">MULAKATCILAR:</span> '
            f'<span style="font-size:13px;color:#94A3B8;">{_kat_html}</span></div>'
        )
        st.markdown(_mkat_html, unsafe_allow_html=True)

    # ======= VERI TOPLAYICILAR =======
    _reask_scores = {}
    _reask_notes = {}
    _reask_q_info = {}
    _new_q_data = {}
    scores = {}
    notes = {}

    # ======= ONCEKI MULAKAT SORULARI + AYNI SORUYU SOR (2./3. mulakat) =======
    if target_stage > 1:
        styled_section("Önceki Mulakat Sorulari", "#64748b")
        _prev_intvs = sorted(
            [iv for iv in interviews if iv.candidate_id == sel_intv.candidate_id and iv.stage < target_stage],
            key=lambda x: x.stage
        )
        for prev_iv in _prev_intvs:
            _ps = store.find_by_field("interview_scores", "interview_id", prev_iv.id)
            if not _ps:
                _no_score_html = (
                    f'<div style="background:#1A2035;border-radius:10px;padding:10px 14px;margin:6px 0;'
                    f'border-left:4px solid #94a3b8;">'
                    f'<b>{prev_iv.stage}. Mulakat</b> - {prev_iv.interview_date or "-"} - Puan kaydi yok'
                    f'</div>'
                )
                st.markdown(_no_score_html, unsafe_allow_html=True)
                continue
            _ps_objs = sorted(
                [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in _ps],
                key=lambda x: x.order_no
            )
            _ps_total = sum(s.score for s in _ps_objs)
            _ps_max = len(_ps_objs) * 5
            _ps_pct = (_ps_total / _ps_max * 100) if _ps_max > 0 else 0
            _ps_clr = "#10b981" if _ps_pct >= 70 else ("#f59e0b" if _ps_pct >= 50 else "#ef4444")
            _ps_kat = ", ".join(prev_iv.interviewer_names) if prev_iv.interviewer_names else "-"

            # Mulakat baslik karti
            _gnote_html = f'<div style="font-size:12px;color:#475569;margin-top:2px;">{prev_iv.general_note}</div>' if prev_iv.general_note else ''
            _header_html = (
                f'<div style="background:linear-gradient(135deg,#0B0F19 0%,#e2e8f0 100%);'
                f'border-radius:12px;padding:14px 18px;margin:14px 0 6px;border-left:5px solid {_ps_clr};">'
                f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;align-items:center;">'
                f'<div style="font-weight:700;color:#94A3B8;font-size:15px;">'
                f'{prev_iv.stage}. Mulakat - {prev_iv.interview_date} {prev_iv.interview_time}</div>'
                f'<div style="font-weight:700;color:{_ps_clr};font-size:14px;">'
                f'{_ps_total}/{_ps_max} (%{_ps_pct:.0f})</div>'
                f'</div>'
                f'<div style="font-size:12px;color:#64748b;margin-top:3px;">'
                f'Mulakatcilar: {_ps_kat} | Karar: {prev_iv.decision or "-"}</div>'
                f'{_gnote_html}'
                f'</div>'
            )
            st.markdown(_header_html, unsafe_allow_html=True)

            # Her soru - salt okunur + ayni soruyu sor secenegi
            for q in _ps_objs:
                _q_clr = "#10b981" if q.score >= 4 else ("#f59e0b" if q.score >= 3 else "#ef4444")
                _rk = f"rsk_{prev_iv.stage}_{q.question_code}"

                # Salt okunur soru karti
                _qnote_html = f'<div style="font-size:11px;color:#64748b;margin-top:4px;padding-left:18px;">Not: {q.note}</div>' if q.note else ''
                _qcard_html = (
                    f'<div style="background:#fff;border-radius:10px;padding:10px 14px;'
                    f'margin:3px 0;border:1px solid #e2e8f0;border-left:4px solid {_q_clr};">'
                    f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;align-items:center;">'
                    f'<div style="flex:1;font-size:13px;color:#94A3B8;">'
                    f'<span style="font-weight:700;color:#94A3B8;">{q.order_no}.</span> {q.question_text}</div>'
                    f'<div style="display:flex;gap:8px;align-items:center;margin-left:12px;">'
                    f'<span style="background:{_q_clr};color:#fff;padding:2px 10px;border-radius:12px;'
                    f'font-size:12px;font-weight:700;">{q.score}/5</span></div>'
                    f'</div>'
                    f'{_qnote_html}'
                    f'</div>'
                )
                st.markdown(_qcard_html, unsafe_allow_html=True)

                # "Ayni soruyu sor" secenegi
                _do_reask = st.checkbox("Ayni soruyu sor", key=f"ik_reask_{_key_pfx}_{_rk}")
                if _do_reask:
                    _reask_q_info[_rk] = (q.question_text, q.order_no, q.question_code)
                    _rc1, _rc2 = st.columns([1, 3])
                    with _rc1:
                        _reask_scores[_rk] = st.number_input(
                            "Puan (0-5)", min_value=0, max_value=5, value=0, step=1,
                            key=f"ik_rsp_{_key_pfx}_{_rk}")
                    with _rc2:
                        _reask_notes[_rk] = st.text_input(
                            "Not", key=f"ik_rnp_{_key_pfx}_{_rk}",
                            placeholder="Bu soru için degerlendirmeniz...")

    # ======= STANDART SORU SETLERI =======
    selector = QuestionSetSelector()
    gen_q, role_q = selector.select_questions(position, store)

    if gen_q or role_q:
        _std_ctx = (st.expander("Standart Soru Setleri (Opsiyonel)", expanded=False)
                    if target_stage > 1 else st.container())
        with _std_ctx:
            if gen_q:
                styled_section(f"Blok 1: Genel Sorular ({len(gen_q)} soru)", "#2563eb")
                for q in gen_q:
                    with st.container():
                        _gen_q_html = (
                            f'<div style="background:#111827;border-radius:10px;padding:12px 16px;'
                            f'margin:6px 0;border-left:4px solid #2563eb;">'
                            f'<span style="font-weight:700;color:#94A3B8;">{q.order_no}.</span> '
                            f'<span style="color:#94A3B8;">{q.question_text}</span></div>'
                        )
                        st.markdown(_gen_q_html, unsafe_allow_html=True)
                        sc1, sc2 = st.columns([1, 3])
                        with sc1:
                            scores[q.question_code] = st.number_input(
                                "Puan (0-5)", min_value=0, max_value=5, value=0, step=1,
                                key=f"ik_{_key_pfx}_s_{q.question_code}")
                        with sc2:
                            notes[q.question_code] = st.text_input(
                                "Not", key=f"ik_{_key_pfx}_n_{q.question_code}",
                                placeholder="Değerlendirme notunuz...")
            if role_q:
                scope_label = position.role_scope if position else "Genel"
                styled_section(f"Blok 2: {scope_label} Sorulari ({len(role_q)} soru)", "#8b5cf6")
                for q in role_q:
                    with st.container():
                        _role_q_html = (
                            f'<div style="background:#faf5ff;border-radius:10px;padding:12px 16px;'
                            f'margin:6px 0;border-left:4px solid #8b5cf6;">'
                            f'<span style="font-weight:700;color:#94A3B8;">{q.order_no}.</span> '
                            f'<span style="color:#94A3B8;">{q.question_text}</span></div>'
                        )
                        st.markdown(_role_q_html, unsafe_allow_html=True)
                        sc1, sc2 = st.columns([1, 3])
                        with sc1:
                            scores[q.question_code] = st.number_input(
                                "Puan (0-5)", min_value=0, max_value=5, value=0, step=1,
                                key=f"ik_{_key_pfx}_s_{q.question_code}")
                        with sc2:
                            notes[q.question_code] = st.text_input(
                                "Not", key=f"ik_{_key_pfx}_n_{q.question_code}",
                                placeholder="Değerlendirme notunuz...")
    elif target_stage == 1:
        styled_info_banner("Soru seti bulunamadı. Ayarlar sekmesinden soru setlerini import edin.", "warning")

    # ======= YENI SORU EKLE (2./3. mulakat) =======
    if target_stage > 1:
        styled_section("Yeni Soru Ekle", "#0d9488")
        _ys_key = f"ik_ys_cnt_{_key_pfx}_{sel_intv.id}"
        if _ys_key not in st.session_state:
            st.session_state[_ys_key] = 0

        for _yi in range(st.session_state[_ys_key]):
            _ys_html = (
                f'<div style="background:linear-gradient(135deg,#f0fdfa 0%,#ccfbf1 100%);'
                f'border-radius:10px;padding:10px 14px;margin:6px 0;border-left:4px solid #0d9488;">'
                f'<span style="font-weight:700;color:#0d9488;">Yeni Soru {_yi + 1}</span></div>'
            )
            st.markdown(_ys_html, unsafe_allow_html=True)
            _yq_text = st.text_input("Soru Metni *", key=f"ik_ys_t_{_key_pfx}_{sel_intv.id}_{_yi}",
                                     placeholder="Soruyu yazin...")
            _yc1, _yc2 = st.columns([1, 3])
            with _yc1:
                _yq_puan = st.number_input("Puan (0-5)", 0, 5, 0, step=1,
                                           key=f"ik_ys_p_{_key_pfx}_{sel_intv.id}_{_yi}")
            with _yc2:
                _yq_not = st.text_input("Not", key=f"ik_ys_n_{_key_pfx}_{sel_intv.id}_{_yi}",
                                        placeholder="Değerlendirme notunuz...")
            _new_q_data[_yi] = {"text": _yq_text, "puan": _yq_puan, "not": _yq_not}

        if st.button("+ Yeni Soru Ekle", key=f"ik_ys_add_{_key_pfx}"):
            st.session_state[_ys_key] = st.session_state.get(_ys_key, 0) + 1
            st.rerun()

    # ======= GENEL DEGERLENDIRME + KAYDET =======
    _can_save = (target_stage > 1) or bool(gen_q or role_q)
    if _can_save:
        styled_section("Genel Değerlendirme", "#10b981")
        genel_not = st.text_area("Genel Değerlendirme Notu (ZORUNLU)", key=f"ik_{_key_pfx}_gnot", height=100)

        if st.button("Puanlamayi Kaydet", type="primary", key=f"ik_{_key_pfx}_save"):
            if not genel_not.strip():
                st.error("Genel degerlendirme notu zorunludur.")
            else:
                # 1. Standart soru puanlari
                all_q = (gen_q or []) + (role_q or [])
                for q in all_q:
                    if q.question_code in scores:
                        isc = InterviewScore(
                            interview_id=sel_intv.id,
                            question_code=q.question_code,
                            set_code=q.set_code,
                            order_no=q.order_no,
                            question_text=q.question_text,
                            score=scores.get(q.question_code, 0),
                            note=notes.get(q.question_code, ""),
                        )
                        store.upsert("interview_scores", isc)

                # 2. Tekrar sorulan sorular (Ayni soruyu sor)
                for _rk, _rpuan in _reask_scores.items():
                    _rinfo = _reask_q_info.get(_rk)
                    if _rinfo:
                        isc = InterviewScore(
                            interview_id=sel_intv.id,
                            question_code=f"REASK_{_rinfo[2]}",
                            set_code="REASK",
                            order_no=_rinfo[1],
                            question_text=_rinfo[0],
                            score=_rpuan,
                            note=_reask_notes.get(_rk, ""),
                        )
                        store.upsert("interview_scores", isc)

                # 3. Yeni eklenen sorular
                for _yi, _yd in _new_q_data.items():
                    if _yd["text"].strip():
                        isc = InterviewScore(
                            interview_id=sel_intv.id,
                            question_code=f"CUSTOM_{_yi + 1}",
                            set_code="CUSTOM",
                            order_no=900 + _yi,
                            question_text=_yd["text"],
                            score=_yd["puan"],
                            note=_yd["not"],
                        )
                        store.upsert("interview_scores", isc)

                sel_intv.status = "Tamamlandı"
                sel_intv.general_note = genel_not
                sel_intv.updated_at = _now_str()
                store.upsert("interviews", sel_intv)
                AuditLogger.log(store, "mulakat_puanlandi", "interview", sel_intv.id, sel_intv.interview_code)
                styled_info_banner("Puanlama kaydedildi.", "success")
                st.rerun()


def _render_coklu_aday_karsilastirma(store: IKDataStore):
    """Ayni pozisyon/brans için birden fazla adayin karsilastirmali raporu ve son karar ekrani."""
    styled_section("Çoklu Aday Karşılaştırma", "#7c3aed")
    styled_info_banner(
        "Ayni pozisyona (ogretmenler için ayni brans) basvuran adaylarin "
        "mulakat puanlarini karsilastirin ve son ise alim kararini bu ekranda verin.",
        "info", "\U0001f4ca"
    )

    interviews = store.load_objects("interviews")
    candidates = store.load_objects("candidates")
    applications = store.load_objects("applications")
    positions = store.load_objects("positions")
    cand_map = {c.id: c for c in candidates}
    pos_map = {p.position_code: p for p in positions}
    app_map = {a.candidate_id: a for a in applications}

    # Mulakati tamamlanmis veya karari verilmis adaylari bul
    completed_intvs = [iv for iv in interviews if iv.status == "Tamamlandı" or iv.decision]
    if not completed_intvs:
        styled_info_banner("Henuz tamamlanmis mulakat yok.", "warning")
        return

    # Pozisyon+Brans bazli gruplama
    # key: (position_code, brans) -> [candidate_id, ...]
    groups: dict[tuple[str, str], set[str]] = {}
    for iv in completed_intvs:
        cand = cand_map.get(iv.candidate_id)
        app = app_map.get(iv.candidate_id)
        if not cand or not app:
            continue
        pos = pos_map.get(app.position_code)
        brans_key = cand.brans if (pos and pos.role_scope == "TEACHER") else ""
        grp_key = (app.position_code, brans_key)
        if grp_key not in groups:
            groups[grp_key] = set()
        groups[grp_key].add(iv.candidate_id)

    # Sadece 1'den fazla adayi olan gruplari goster
    multi_groups = {k: v for k, v in groups.items() if len(v) > 1}
    if not multi_groups:
        styled_info_banner(
            "Ayni pozisyona birden fazla aday mulakata girmemis. "
            "En az 2 aday mulakat tamamlamalidir.",
            "info"
        )
        return

    # Grup secimi
    grp_labels = []
    grp_keys = list(multi_groups.keys())
    for pos_code, brans in grp_keys:
        pos = pos_map.get(pos_code)
        pos_name = pos.position_name if pos else pos_code
        label = f"{pos_name}"
        if brans:
            label += f" - {brans}"
        label += f" ({len(multi_groups[(pos_code, brans)])} aday)"
        grp_labels.append(label)

    grp_idx = st.selectbox(
        "Pozisyon / Branş Secin", range(len(grp_labels)),
        format_func=lambda i: grp_labels[i], key="ik_coklu_grp_sec"
    )
    sel_key = grp_keys[grp_idx]
    sel_pos_code, sel_brans = sel_key
    sel_pos = pos_map.get(sel_pos_code)
    sel_cand_ids = list(multi_groups[sel_key])

    # Pozisyon bilgi karti
    _pos_name = sel_pos.position_name if sel_pos else sel_pos_code
    _scope = sel_pos.role_scope if sel_pos else "ALL"
    _brans_txt = sel_brans or "-"
    _grp_info_html = (
        f'<div style="background:linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%);'
        f'border-radius:14px;padding:16px 20px;margin:12px 0;border-left:5px solid #7c3aed;">'
        f'<div style="display:flex;gap:30px;flex-wrap:wrap;">'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">POZISYON</div>'
        f'<div style="font-size:16px;font-weight:700;color:#2563eb;">{_pos_name}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">BRANS</div>'
        f'<div style="font-size:16px;font-weight:700;color:#8b5cf6;">{_brans_txt}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">SCOPE</div>'
        f'<div style="font-size:14px;font-weight:600;color:#0d9488;">{_scope}</div></div>'
        f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ADAY SAYISI</div>'
        f'<div style="font-size:16px;font-weight:700;color:#7c3aed;">{len(sel_cand_ids)}</div></div>'
        f'</div></div>'
    )
    st.markdown(_grp_info_html, unsafe_allow_html=True)

    # ---- Her aday için puan hesapla ----
    aday_verileri = []
    for cid in sel_cand_ids:
        cand = cand_map.get(cid)
        if not cand:
            continue
        cand_intvs = sorted(
            [iv for iv in completed_intvs if iv.candidate_id == cid],
            key=lambda x: x.stage
        )
        all_scores = []
        stage_data = []
        for iv in cand_intvs:
            raw = store.find_by_field("interview_scores", "interview_id", iv.id)
            if raw:
                objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in raw]
                iv_total = sum(s.score for s in objs)
                iv_max = len(objs) * 5
                iv_pct = (iv_total / iv_max * 100) if iv_max > 0 else 0
                stage_data.append({
                    "stage": iv.stage, "total": iv_total, "max": iv_max,
                    "pct": iv_pct, "count": len(objs), "decision": iv.decision,
                    "interview": iv, "scores": objs,
                })
                all_scores.extend(objs)

        grand_total = sum(s.score for s in all_scores) if all_scores else 0
        grand_max = len(all_scores) * 5 if all_scores else 0
        grand_pct = (grand_total / grand_max * 100) if grand_max > 0 else 0
        grand_avg = grand_total / len(all_scores) if all_scores else 0
        excellent = sum(1 for s in all_scores if s.score >= 4)
        poor = sum(1 for s in all_scores if s.score <= 2)
        last_decision = next(
            (sd["decision"] for sd in reversed(stage_data) if sd["decision"]),
            None
        )

        aday_verileri.append({
            "cand": cand,
            "stages": stage_data,
            "all_scores": all_scores,
            "grand_total": grand_total,
            "grand_max": grand_max,
            "grand_pct": grand_pct,
            "grand_avg": grand_avg,
            "excellent": excellent,
            "poor": poor,
            "last_decision": last_decision,
            "mulakat_sayisi": len(stage_data),
        })

    # Siralama: grand_pct'ye gore buyukten kucuge
    aday_verileri.sort(key=lambda x: x["grand_pct"], reverse=True)

    # ---- Özet Karşılaştırma Tablosu ----
    styled_section("Karşılaştırma Tablosu", "#2563eb")
    rows = []
    for i, av in enumerate(aday_verileri, 1):
        c = av["cand"]
        pct_clr = "#10b981" if av["grand_pct"] >= 70 else ("#f59e0b" if av["grand_pct"] >= 50 else "#ef4444")
        stage_details = " | ".join([
            f"{sd['stage']}.M: %{sd['pct']:.0f}" for sd in av["stages"]
        ])
        rows.append({
            "Sira": i,
            "Aday": c.tam_ad,
            "Branş": c.brans or "-",
            "Mulakat": av["mulakat_sayisi"],
            "Toplam": f"{av['grand_total']}/{av['grand_max']}",
            "Ortalama": f"{av['grand_avg']:.2f}/5",
            "Başarı %": f"%{av['grand_pct']:.0f}",
            "Güçlü (4-5)": av["excellent"],
            "Zayif (0-2)": av["poor"],
            "Asamalar": stage_details,
            "Karar": av["last_decision"] or "Bekliyor",
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    # ---- Görsel Karşılaştırma ----
    styled_section("Görsel Karşılaştırma", "#8b5cf6")

    gc1, gc2 = st.columns(2)
    with gc1:
        # Bar chart: Adaylarin genel basari yuzdeleri
        bar_data = {}
        for av in aday_verileri:
            bar_data[av["cand"].tam_ad[:20]] = av["grand_pct"]
        if bar_data:
            st.markdown("**Genel Başarı (%)**")
            st.markdown(
                ReportStyler.horizontal_bar_html(bar_data, color="#7c3aed", max_width_px=350),
                unsafe_allow_html=True
            )

    with gc2:
        # Donut: Aday bazli toplam puan dagilimi
        donut_data = {}
        for av in aday_verileri:
            donut_data[av["cand"].tam_ad[:18]] = float(av["grand_total"])
        if donut_data:
            st.markdown("**Toplam Puan Dagilimi**")
            st.markdown(
                ReportStyler.donut_chart_svg(donut_data, size=155),
                unsafe_allow_html=True
            )

    # ---- Asama bazli karsilastirma ----
    max_stage = max((sd["stage"] for av in aday_verileri for sd in av["stages"]), default=1)
    if max_stage > 1:
        styled_section("Aşama Bazlı Karşılaştırma", "#0d9488")
        for stg in range(1, max_stage + 1):
            stg_bar = {}
            for av in aday_verileri:
                sd = next((s for s in av["stages"] if s["stage"] == stg), None)
                if sd:
                    stg_bar[av["cand"].tam_ad[:20]] = sd["pct"]
            if stg_bar:
                st.markdown(f"**{stg}. Mulakat Başarı (%)**")
                _stg_clrs = {1: "#2563eb", 2: "#8b5cf6", 3: "#0d9488"}
                st.markdown(
                    ReportStyler.horizontal_bar_html(
                        stg_bar, color=_stg_clrs.get(stg, "#64748b"), max_width_px=400
                    ),
                    unsafe_allow_html=True
                )

    # ---- Aday Detay Kartlari + AI Tavsiyesi ----
    styled_section("Aday Detaylari ve AI Tavsiyesi", "#1e40af")

    for rank, av in enumerate(aday_verileri, 1):
        c = av["cand"]
        pct = av["grand_pct"]
        pct_clr = "#10b981" if pct >= 70 else ("#f59e0b" if pct >= 50 else "#ef4444")

        # Siralama badge
        rank_bg = "#10b981" if rank == 1 else ("#2563eb" if rank == 2 else "#64748b")
        rank_icon = {1: "\U0001f947", 2: "\U0001f948", 3: "\U0001f949"}.get(rank, f"#{rank}")

        # Aday kart basligi
        _cand_header_html = (
            f'<div style="background:linear-gradient(135deg,#111827 0%,#1A2035 100%);'
            f'border-radius:14px;padding:16px 20px;margin:16px 0 6px;'
            f'border-left:5px solid {pct_clr};box-shadow:0 2px 6px rgba(0,0,0,0.06);">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">'
            f'<div style="display:flex;align-items:center;gap:14px;">'
            f'<div style="background:{rank_bg};color:#fff;width:36px;height:36px;'
            f'border-radius:50%;display:flex;align-items:center;justify-content:center;'
            f'font-size:16px;font-weight:800;">{rank_icon}</div>'
            f'<div>'
            f'<div style="font-size:16px;font-weight:700;color:#94A3B8;">{c.tam_ad}</div>'
            f'<div style="font-size:12px;color:#64748b;">'
            f'{c.brans or "-"} | {c.universite or "-"} | {c.telefon or "-"}</div>'
            f'</div></div>'
            f'<div style="text-align:right;">'
            f'<div style="font-size:22px;font-weight:800;color:{pct_clr};">%{pct:.0f}</div>'
            f'<div style="font-size:12px;color:#64748b;">'
            f'{av["grand_total"]}/{av["grand_max"]} ({av["mulakat_sayisi"]} mulakat)</div>'
            f'</div></div>'
        )

        # Asama detaylari
        _stage_badges = ""
        for sd in av["stages"]:
            sd_clr = "#10b981" if sd["pct"] >= 70 else ("#f59e0b" if sd["pct"] >= 50 else "#ef4444")
            dec_txt = f" - {sd['decision']}" if sd["decision"] else ""
            _stage_badges += (
                f'<span style="display:inline-block;background:{sd_clr}15;border:1px solid {sd_clr};'
                f'border-radius:8px;padding:3px 10px;margin:3px 4px;font-size:12px;'
                f'font-weight:600;color:{sd_clr};">'
                f'{sd["stage"]}.M: {sd["total"]}/{sd["max"]} (%{sd["pct"]:.0f}){dec_txt}</span>'
            )

        _cand_stages_html = (
            f'<div style="margin:6px 0 4px 50px;">{_stage_badges}</div>'
        )

        # Karar durumu
        _dec_html = ""
        if av["last_decision"]:
            _d_icons = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                        "Beklemede": "\u23f3"}
            _d_clrs = {"Ise Alindi": "#10b981", "Ret": "#ef4444", "Yedek": "#8b5cf6",
                        "Beklemede": "#f59e0b"}
            _d_icon = _d_icons.get(av["last_decision"], "")
            _d_clr = _d_clrs.get(av["last_decision"], "#64748b")
            _dec_html = (
                f'<div style="margin:4px 0 0 50px;">'
                f'<span style="background:{_d_clr};color:#fff;padding:3px 12px;'
                f'border-radius:12px;font-size:12px;font-weight:700;">'
                f'{_d_icon} {av["last_decision"]}</span></div>'
            )

        _card_html = _cand_header_html + _cand_stages_html + _dec_html + '</div>'
        st.markdown(_card_html, unsafe_allow_html=True)

        # AI Tavsiyesi
        last_stage = av["stages"][-1]["stage"] if av["stages"] else 1
        combined_pct = av["grand_pct"] if av["mulakat_sayisi"] > 1 else None
        ai_oneri = _generate_ai_oneri(pct, av["all_scores"], last_stage, combined_pct)
        _ai_card_html = (
            f'<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 100%);'
            f'border-radius:10px;padding:12px 16px;margin:2px 0 12px 50px;'
            f'border-left:4px solid #1e40af;">'
            f'<div style="font-size:11px;font-weight:700;color:#1e40af;margin-bottom:4px;">'
            f'AI TAVSIYESI</div>'
            f'<div style="font-size:12px;color:#94A3B8;line-height:1.7;">{ai_oneri}</div>'
            f'</div>'
        )
        st.markdown(_ai_card_html, unsafe_allow_html=True)

    # ---- GENEL AI SIRALAMASINI GOSTER ----
    styled_section("AI Sıralama Onerisi", "#059669")
    _ranking_lines = []
    for i, av in enumerate(aday_verileri, 1):
        c = av["cand"]
        pct = av["grand_pct"]
        if pct >= 75:
            _verdict = "Ise alim için guclu aday"
            _v_clr = "#10b981"
        elif pct >= 60:
            _verdict = "Değerlendirmeye deger"
            _v_clr = "#2563eb"
        elif pct >= 50:
            _verdict = "Sinirda - ek degerlendirme onerilir"
            _v_clr = "#f59e0b"
        else:
            _verdict = "Onerilmez"
            _v_clr = "#ef4444"
        _ranking_lines.append(
            f'<div style="display:flex;align-items:center;gap:12px;padding:8px 12px;'
            f'margin:3px 0;background:#111827;border-radius:8px;'
            f'border-left:4px solid {_v_clr};">'
            f'<div style="font-weight:800;font-size:16px;color:#94A3B8;width:28px;">{i}.</div>'
            f'<div style="flex:1;">'
            f'<span style="font-weight:700;color:#94A3B8;">{c.tam_ad}</span>'
            f'<span style="font-size:12px;color:#64748b;margin-left:8px;">'
            f'({c.brans or "-"} | %{pct:.0f} | {av["mulakat_sayisi"]} mulakat)</span></div>'
            f'<div style="font-weight:700;font-size:12px;color:{_v_clr};">{_verdict}</div>'
            f'</div>'
        )
    _ranking_html = (
        f'<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);'
        f'border-radius:12px;padding:16px 20px;margin:10px 0;border-left:5px solid #059669;">'
        f'<div style="font-weight:700;color:#065f46;font-size:14px;margin-bottom:10px;">'
        f'Başarı Sıralamasına Gore Adaylar</div>'
        f'{"".join(_ranking_lines)}'
        f'</div>'
    )
    st.markdown(_ranking_html, unsafe_allow_html=True)

    # ---- SON KARAR EKRANI ----
    styled_section("Son Karar", "#dc2626")

    # Sadece henuz karari verilmemis adaylari goster
    kararsiz = [av for av in aday_verileri if not av["last_decision"]]
    kararli = [av for av in aday_verileri if av["last_decision"]]

    if kararli:
        st.markdown("**Karari verilmis adaylar:**")
        for av in kararli:
            _d_icons = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                        "Beklemede": "\u23f3"}
            _ic = _d_icons.get(av["last_decision"], "")
            st.write(f"{_ic} **{av['cand'].tam_ad}** - {av['last_decision']} (%{av['grand_pct']:.0f})")

    if not kararsiz:
        styled_info_banner("Tüm adaylarin karari verilmis.", "success")
    else:
        st.markdown(f"**Karar bekleyen {len(kararsiz)} aday:**")
        for av in kararsiz:
            c = av["cand"]
            pct = av["grand_pct"]
            pct_clr = "#10b981" if pct >= 70 else ("#f59e0b" if pct >= 50 else "#ef4444")

            _kc_html = (
                f'<div style="background:#fff;border-radius:10px;padding:12px 16px;'
                f'margin:8px 0;border:1px solid #e2e8f0;border-left:4px solid {pct_clr};">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div style="font-weight:700;color:#94A3B8;">{c.tam_ad}'
                f'<span style="font-size:12px;color:#64748b;margin-left:8px;">'
                f'{c.brans or "-"}</span></div>'
                f'<div style="font-weight:800;color:{pct_clr};font-size:16px;">%{pct:.0f}</div>'
                f'</div></div>'
            )
            st.markdown(_kc_html, unsafe_allow_html=True)

            kc1, kc2, kc3 = st.columns([2, 2, 1])
            with kc1:
                _KARAR_OPT = ["Ise Alindi", "Beklemede", "Yedek", "Ret"]
                # Stage-specific options
                last_stg = av["stages"][-1]["stage"] if av["stages"] else 1
                if last_stg < 2:
                    _KARAR_OPT.insert(1, "2. Mülakata Devam")
                if last_stg < 3:
                    _KARAR_OPT.insert(min(2, len(_KARAR_OPT)), "3. Mülakata Devam")
                karar = st.selectbox(
                    "Karar", _KARAR_OPT,
                    key=f"ik_coklu_karar_{c.id}"
                )
            with kc2:
                karar_notu = st.text_input(
                    "Not", key=f"ik_coklu_knot_{c.id}",
                    placeholder="Karar notu..."
                )
            with kc3:
                if st.button("Kaydet", type="primary", key=f"ik_coklu_kbtn_{c.id}"):
                    # Son mulakatin kararini guncelle
                    last_iv = av["stages"][-1]["interview"] if av["stages"] else None
                    if last_iv:
                        last_iv.decision = karar
                        if karar_notu:
                            last_iv.general_note = (
                                (last_iv.general_note or "") +
                                f"\n\nÇoklu Aday Karar Notu: {karar_notu}"
                            )
                        last_iv.updated_at = _now_str()
                        store.upsert("interviews", last_iv)

                        # Aday statusunu guncelle
                        if karar in ("2. Mülakata Devam", "3. Mülakata Devam"):
                            yeni_asama = 2 if karar == "2. Mülakata Devam" else 3
                            yeni_intv = Interview(
                                interview_code=store.next_interview_code(),
                                application_id=last_iv.application_id,
                                application_code=last_iv.application_code,
                                candidate_id=last_iv.candidate_id,
                                stage=yeni_asama,
                                status="Planlandi",
                            )
                            store.upsert("interviews", yeni_intv)
                            c.status = f"{yeni_asama}. Mulakat Planlandi"
                        else:
                            _status_map = {
                                "Ise Alindi": "Ise Alindi",
                                "Ret": "Ret",
                                "Yedek": "Yedek",
                                "Beklemede": "Beklemede",
                            }
                            c.status = _status_map.get(karar, c.status)
                        c.updated_at = _now_str()
                        store.upsert("candidates", c)

                        AuditLogger.log(
                            store, "coklu_aday_karar", "interview",
                            last_iv.id, f"{c.tam_ad}: {karar}"
                        )
                        styled_info_banner(f"{c.tam_ad} - Karar: {karar}", "success")
                        st.rerun()


def _render_mulakat_yonetimi(store: IKDataStore):
    sub = st.tabs(["📋 Mülakat Planlama", "1️⃣ 1. Mülakat", "2️⃣ 2. Mülakat", "3️⃣ 3. Mülakat",
                   "👥 Çoklu Aday", "✅ Mülakat Karar", "🎉 İşe Alınanlar", "📜 Mülakat Geçmişi"])

    # ---- Mülakat Planlama ----
    with sub[0]:
        styled_section("Mülakat Planlama", "#2563eb")
        applications = store.load_objects("applications")
        candidates = store.load_objects("candidates")
        cand_map = {c.id: c for c in candidates}

        # 2./3. mulakattan gelen, tarih atanmamis bekleyen mulakatlar
        _all_intvs = store.load_objects("interviews")
        _bekleyen_intvs = [iv for iv in _all_intvs
                           if iv.status == "Planlandi" and iv.stage > 1 and not iv.interview_date]
        if _bekleyen_intvs:
            styled_section("Tarih Bekleyen Mulakatlar", "#f59e0b")
            for biv in _bekleyen_intvs:
                bc = cand_map.get(biv.candidate_id)
                _biv_html = (
                    f'<div style="background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);'
                    f'border-radius:10px;padding:12px 16px;margin:4px 0;border-left:4px solid #f59e0b;">'
                    f'<b>{biv.interview_code}</b> - {bc.tam_ad if bc else "?"} - '
                    f'<span style="color:#d97706;font-weight:700;">{biv.stage}. Mulakat</span>'
                    f' - Tarih/saat ve katilimci atanmasi bekleniyor'
                    f'</div>'
                )
                st.markdown(_biv_html, unsafe_allow_html=True)

            _biv_labels = []
            for iv in _bekleyen_intvs:
                _bc = cand_map.get(iv.candidate_id)
                _biv_labels.append(f"{iv.interview_code} - {_bc.tam_ad if _bc else '?'} - {iv.stage}. Mulakat")

            biv_idx = st.selectbox("Bekleyen Mulakat", range(len(_biv_labels)),
                                    format_func=lambda i: _biv_labels[i], key="ik_mul_plan_biv")
            sel_biv = _bekleyen_intvs[biv_idx]

            bc1, bc2, bc3 = st.columns(3)
            with bc1:
                b_tarih = st.date_input("Tarih", key="ik_mul_plan_biv_tarih")
                b_saat = st.time_input("Saat", key="ik_mul_plan_biv_saat")
            with bc2:
                b_tip = st.selectbox("Tip", INTERVIEW_TYPES, key="ik_mul_plan_biv_tip")
            with bc3:
                bstaff = _get_personel_options()
                bstaff_labels = [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('unvan','')}" for s in bstaff]
                b_selected = st.multiselect("Katilimcilar", bstaff_labels, key="ik_mul_plan_biv_kat")

            b_ek_kat = st.text_input("Ek Katilimci", key="ik_mul_plan_biv_ek")

            if st.button("Mulakati Planla", type="primary", key="ik_mul_plan_biv_btn"):
                b_names = list(b_selected)
                if b_ek_kat:
                    b_names.extend([n.strip() for n in b_ek_kat.split(",") if n.strip()])
                sel_biv.interview_date = b_tarih.isoformat()
                sel_biv.interview_time = b_saat.strftime("%H:%M")
                sel_biv.interview_type = b_tip
                sel_biv.interviewer_names = b_names
                sel_biv.updated_at = _now_str()
                store.upsert("interviews", sel_biv)
                AuditLogger.log(store, "mulakat_planlandi", "interview", sel_biv.id, sel_biv.interview_code)
                styled_info_banner(f"{sel_biv.stage}. Mulakat planlandi: {sel_biv.interview_code}", "success")
                st.rerun()

            st.markdown("---")

        # Yeni 1. mulakat planlama
        styled_section("Yeni Mulakat Planla", "#2563eb")
        aktif_app = [a for a in applications if a.status not in ("Ret",)]
        if not aktif_app:
            styled_info_banner("Basvuru bulunamadı. Önce Aday Havuzundan aday ve basvuru ekleyin.", "warning")
        else:
            app_labels = []
            for a in aktif_app:
                c = cand_map.get(a.candidate_id)
                app_labels.append(f"{a.application_code} - {c.tam_ad if c else '?'} - Poz: {a.position_code}")
            app_idx = st.selectbox("Basvuru Secin", range(len(app_labels)),
                                   format_func=lambda i: app_labels[i], key="ik_mul_plan_app")
            sel_app = aktif_app[app_idx]

            # Aday + Pozisyon + Brans bilgi karti
            sel_cand = cand_map.get(sel_app.candidate_id)
            sel_pos = store.get_by_field("positions", "position_code", sel_app.position_code)
            if sel_pos and isinstance(sel_pos, dict):
                sel_pos = Position.from_dict(sel_pos)

            _pos_name = sel_pos.position_name if sel_pos else sel_app.position_code
            _pos_scope = sel_pos.role_scope if sel_pos else "ALL"
            _brans = sel_cand.brans if sel_cand else ""

            # Soru seti eslesmesi
            _all_sets = store.load_objects("question_sets")
            _matched_role_set = None
            for _qs in _all_sets:
                if _qs.set_type == "POSITION" and _qs.is_active and _qs.role_scope == _pos_scope:
                    _matched_role_set = _qs
                    break
            if not _matched_role_set:
                for _qs in _all_sets:
                    if _qs.set_type == "CATEGORY" and _qs.is_active and _qs.role_scope == _pos_scope:
                        _matched_role_set = _qs
                        break
            _gen_set = next((s for s in _all_sets if s.set_code == store.get_settings().default_general_set_code), None)

            _gen_set_txt = f"{_gen_set.set_name} ({_gen_set.question_count})" if _gen_set else "Genel: -"
            _role_set_txt = f" + {_matched_role_set.set_name} ({_matched_role_set.question_count})" if _matched_role_set else ""
            _plan_info_html = (
                f'<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 100%);'
                f'border-radius:14px;padding:18px 22px;margin:12px 0;border-left:5px solid #2563eb;">'
                f'<div style="display:flex;gap:30px;flex-wrap:wrap;">'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ADAY</div>'
                f'<div style="font-size:15px;font-weight:700;color:#94A3B8;">{sel_cand.tam_ad if sel_cand else "?"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">POZISYON</div>'
                f'<div style="font-size:15px;font-weight:700;color:#2563eb;">{_pos_name}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">BRANS</div>'
                f'<div style="font-size:15px;font-weight:700;color:#8b5cf6;">{_brans or "-"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">SORU SETi</div>'
                f'<div style="font-size:13px;font-weight:600;color:#0d9488;">'
                f'{_gen_set_txt}{_role_set_txt}</div></div>'
                f'</div></div>'
            )
            st.markdown(_plan_info_html, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                asama = st.selectbox("Mulakat Asamasi", [1, 2, 3], key="ik_mul_plan_asama")
            with c2:
                tarih = st.date_input("Mulakat Tarihi", key="ik_mul_plan_tarih")
                saat = st.time_input("Saat", key="ik_mul_plan_saat")
            with c3:
                tip = st.selectbox("Mulakat Tipi", INTERVIEW_TYPES, key="ik_mul_plan_tip")

            # Katilimcilar
            styled_section("Katilimcilar", "#8b5cf6")
            staff = _get_personel_options()
            staff_labels = [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('unvan','')}" for s in staff]
            if staff_labels:
                selected_staff = st.multiselect("Katilimci Secin", staff_labels, key="ik_mul_plan_kat")
            else:
                selected_staff = []
                st.info("KIM'den personel yukleyin veya isim girin.")
            ek_katilimci = st.text_input("Ek Katilimci (virgul ile)", key="ik_mul_plan_ek_kat")

            if st.button("Mulakat Planla", type="primary", key="ik_mul_plan_btn"):
                interviewer_names = list(selected_staff)
                if ek_katilimci:
                    interviewer_names.extend([n.strip() for n in ek_katilimci.split(",") if n.strip()])

                intv = Interview(
                    interview_code=store.next_interview_code(),
                    application_id=sel_app.id,
                    application_code=sel_app.application_code,
                    candidate_id=sel_app.candidate_id,
                    stage=asama,
                    interview_date=tarih.isoformat(),
                    interview_time=saat.strftime("%H:%M"),
                    interview_type=tip,
                    interviewer_names=interviewer_names,
                    status="Planlandi",
                )
                store.upsert("interviews", intv)

                # Aday durumunu guncelle
                cand = cand_map.get(sel_app.candidate_id)
                if cand and cand.status == "Yeni":
                    cand.status = "Mulakat Planlandi"
                    cand.updated_at = _now_str()
                    store.upsert("candidates", cand)

                AuditLogger.log(store, "mulakat_planlandi", "interview", intv.id, intv.interview_code)
                styled_info_banner(f"Mulakat planlandi: {intv.interview_code} - Asama {asama}", "success")
                st.rerun()

    # ---- 1. Mülakat ----
    with sub[1]:
        styled_section("1. Mülakat", "#2563eb")
        _render_mulakat_stage_scoring(store, 1)
        _render_mulakat_stage_results(store, 1)

    # ---- 2. Mülakat ----
    with sub[2]:
        styled_section("2. Mülakat", "#8b5cf6")
        _render_mulakat_stage_scoring(store, 2)
        _render_mulakat_stage_results(store, 2)

    # ---- 3. Mülakat ----
    with sub[3]:
        styled_section("3. Mülakat", "#0d9488")
        _render_mulakat_stage_scoring(store, 3)
        _render_mulakat_stage_results(store, 3)

    # ---- Çoklu Aday Karşılaştırma ----
    with sub[4]:
        _render_coklu_aday_karsilastirma(store)

    # ---- Mülakat Karar ----
    with sub[5]:
        styled_section("Mülakat Karar", "#10b981")
        interviews = store.load_objects("interviews")
        tamamlanan = [i for i in interviews if i.status == "Tamamlandı" and not i.decision]

        if not tamamlanan:
            styled_info_banner("Karar bekleyen mulakat yok.", "info")
        else:
            candidates = store.load_objects("candidates")
            cand_map = {c.id: c for c in candidates}
            applications = store.load_objects("applications")
            app_map_k = {a.candidate_id: a for a in applications}
            positions = store.load_objects("positions")
            pos_map_k = {p.position_code: p for p in positions}

            k_labels = []
            for iv in tamamlanan:
                c = cand_map.get(iv.candidate_id)
                k_labels.append(f"{iv.interview_code} - {c.tam_ad if c else '?'} - {iv.stage}. Mulakat")
            k_idx = st.selectbox("Mulakat Secin", range(len(k_labels)),
                                 format_func=lambda i: k_labels[i], key="ik_mul_karar_sec")
            sel_intv = tamamlanan[k_idx]
            sel_cand = cand_map.get(sel_intv.candidate_id)

            # Aday + Pozisyon + Brans bilgi karti
            _k_app = app_map_k.get(sel_intv.candidate_id)
            _k_pos = pos_map_k.get(_k_app.position_code) if _k_app else None
            _k_pos_name = _k_pos.position_name if _k_pos else (_k_app.position_code if _k_app else "-")
            _k_brans = sel_cand.brans if sel_cand else "-"

            _karar_info_html = (
                f'<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);'
                f'border-radius:14px;padding:18px 22px;margin:10px 0;border-left:5px solid #10b981;">'
                f'<div style="display:flex;gap:28px;flex-wrap:wrap;">'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ADAY</div>'
                f'<div style="font-size:16px;font-weight:700;color:#94A3B8;">{sel_cand.tam_ad if sel_cand else "?"}</div>'
                f'<div style="font-size:12px;color:#64748b;">TC: {sel_cand.tc_no or "-"} | {sel_cand.telefon or "-"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">POZISYON</div>'
                f'<div style="font-size:15px;font-weight:700;color:#2563eb;">{_k_pos_name}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">BRANS</div>'
                f'<div style="font-size:15px;font-weight:700;color:#8b5cf6;">{_k_brans or "-"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ASAMA</div>'
                f'<div style="font-size:15px;font-weight:700;color:#10b981;">{sel_intv.stage}. Mulakat</div></div>'
                f'</div></div>'
            )
            st.markdown(_karar_info_html, unsafe_allow_html=True)

            # Mulakatci bilgisi
            if sel_intv.interviewer_names:
                kat_html = " | ".join([f"<b>{n}</b>" for n in sel_intv.interviewer_names])
                _mkat2_html = (
                    f'<div style="background:#111827;border-radius:10px;padding:10px 16px;margin:6px 0;'
                    f'border:1px solid #e2e8f0;">'
                    f'<span style="font-size:11px;color:#64748b;font-weight:600;">MULAKATCILAR:</span> '
                    f'<span style="font-size:13px;color:#94A3B8;">{kat_html}</span></div>'
                )
                st.markdown(_mkat2_html, unsafe_allow_html=True)

            # Onceki mulakat sonuclari timeline
            _all_cand_intv = sorted(
                [iv for iv in interviews if iv.candidate_id == sel_intv.candidate_id],
                key=lambda x: x.stage
            )
            if len(_all_cand_intv) > 1 or sel_intv.stage > 1:
                styled_section("Önceki Mulakat Sonuclari", "#64748b")
                for prev_iv in _all_cand_intv:
                    if prev_iv.id == sel_intv.id:
                        continue
                    _prev_scores = store.find_by_field("interview_scores", "interview_id", prev_iv.id)
                    _prev_total = 0
                    _prev_max = 0
                    _prev_avg = 0.0
                    if _prev_scores:
                        _ps_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in _prev_scores]
                        _prev_total = sum(s.score for s in _ps_objs)
                        _prev_max = len(_ps_objs) * 5
                        _prev_avg = _prev_total / len(_ps_objs) if _ps_objs else 0
                    _prev_pct = (_prev_total / _prev_max * 100) if _prev_max > 0 else 0
                    _prev_clr = "#10b981" if _prev_pct >= 70 else ("#f59e0b" if _prev_pct >= 50 else "#ef4444")
                    _prev_kat = ", ".join(prev_iv.interviewer_names) if prev_iv.interviewer_names else "-"
                    _prev_karar_icon = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                                        "Beklemede": "\u23f3", "2. Mülakata Devam": "\u27a1\ufe0f",
                                        "3. Mülakata Devam": "\u27a1\ufe0f"}.get(prev_iv.decision, "\u2796")
                    _prev_gnote = f'<div style="font-size:12px;color:#475569;margin-top:4px;">{prev_iv.general_note}</div>' if prev_iv.general_note else ''
                    _prev_html = (
                        f'<div style="background:#1A2035;border-radius:10px;padding:12px 16px;margin:4px 0;'
                        f'border-left:4px solid {_prev_clr};">'
                        f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;">'
                        f'<div><b>{prev_iv.stage}. Mulakat</b> - {prev_iv.interview_date} {prev_iv.interview_time}'
                        f' ({prev_iv.interview_type})</div>'
                        f'<div style="font-weight:700;color:{_prev_clr};">{_prev_total}/{_prev_max} (%{_prev_pct:.0f})'
                        f' {_prev_karar_icon} {prev_iv.decision or "-"}</div>'
                        f'</div>'
                        f'<div style="font-size:12px;color:#64748b;margin-top:4px;">Mulakatcilar: {_prev_kat}</div>'
                        f'{_prev_gnote}'
                        f'</div>'
                    )
                    st.markdown(_prev_html, unsafe_allow_html=True)

            # Mevcut mulakat puan ozeti
            styled_section(f"{sel_intv.stage}. Mulakat Puan Özeti", "#2563eb")
            scores = store.find_by_field("interview_scores", "interview_id", sel_intv.id)
            if scores:
                score_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in scores]
                total = sum(s.score for s in score_objs)
                avg = total / len(score_objs) if score_objs else 0
                max_puan = len(score_objs) * 5
                puan_yuzde = (total / max_puan * 100) if max_puan > 0 else 0
                puan_renk = "#10b981" if puan_yuzde >= 70 else ("#f59e0b" if puan_yuzde >= 50 else "#ef4444")
                styled_stat_row([
                    ("Toplam Puan", f"{total}/{max_puan}", puan_renk, "\U0001f4ca"),
                    ("Ortalama", f"{avg:.2f}/5", "#2563eb", "\U0001f4c8"),
                    ("Soru Sayısı", len(score_objs), "#8b5cf6", "\U0001f4dd"),
                    ("Başarı", f"%{puan_yuzde:.0f}", puan_renk, "\U0001f3af"),
                ])

            if sel_intv.general_note:
                st.markdown(f"**Genel Not:** {sel_intv.general_note}")

            # Karar secimi - renkli kartlar
            styled_section("Karar Ver", "#1e40af")

            # Asama bazli karar secenekleri
            _KARAR_RENK = {
                "Ise Alindi": ("#10b981", "#059669", "\u2705", "Aday ise alinir, Onboarding baslar."),
                "2. Mülakata Devam": ("#2563eb", "#1d4ed8", "\u27a1\ufe0f", "Aday 2. mulakat asamasina alinir."),
                "3. Mülakata Devam": ("#0d9488", "#0f766e", "\u27a1\ufe0f", "Aday 3. mulakat asamasina alinir."),
                "Beklemede": ("#f59e0b", "#d97706", "\u23f3", "Karar ertelenir, havuzda kalir."),
                "Ret": ("#ef4444", "#dc2626", "\u274c", "Aday reddedilir."),
                "Yedek": ("#8b5cf6", "#7c3aed", "\U0001f4cb", "Yedek listeye alinir."),
            }

            # Asamaya gore uygun kararlari filtrele
            _uygun_kararlar = {}
            for k, v in _KARAR_RENK.items():
                if k == "2. Mülakata Devam" and sel_intv.stage >= 2:
                    continue
                if k == "3. Mülakata Devam" and sel_intv.stage >= 3:
                    continue
                _uygun_kararlar[k] = v

            _kk_cards = "".join([
                f'<div style="background:linear-gradient(135deg,{renk[0]} 0%,{renk[1]} 100%);'
                f'border-radius:10px;padding:12px 16px;flex:1;min-width:130px;text-align:center;">'
                f'<div style="font-size:1.3rem;">{renk[2]}</div>'
                f'<div style="font-weight:700;color:#fff;font-size:0.85rem;">{k}</div>'
                f'<div style="font-size:0.65rem;color:rgba(255,255,255,0.8);">{renk[3]}</div></div>'
                for k, renk in _uygun_kararlar.items()
            ])
            st.markdown(
                f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin:8px 0;">{_kk_cards}</div>',
                unsafe_allow_html=True
            )

            _karar_opts = list(_uygun_kararlar.keys())
            karar = st.selectbox("Karar", _karar_opts, key="ik_mul_karar_val")
            karar_notu = st.text_area("Karar Notu", key="ik_mul_karar_not", height=80)

            if st.button("Karari Kaydet", type="primary", key="ik_mul_karar_btn"):
                sel_intv.decision = karar
                if karar_notu:
                    sel_intv.general_note = (sel_intv.general_note or "") + f"\n\nKarar Notu: {karar_notu}"
                sel_intv.updated_at = _now_str()
                store.upsert("interviews", sel_intv)

                cand = cand_map.get(sel_intv.candidate_id)

                # 2. veya 3. mulakata devam -> otomatik yeni mulakat olustur
                if karar in ("2. Mülakata Devam", "3. Mülakata Devam"):
                    yeni_asama = 2 if karar == "2. Mülakata Devam" else 3
                    yeni_intv = Interview(
                        interview_code=store.next_interview_code(),
                        application_id=sel_intv.application_id,
                        application_code=sel_intv.application_code,
                        candidate_id=sel_intv.candidate_id,
                        stage=yeni_asama,
                        status="Planlandi",
                    )
                    store.upsert("interviews", yeni_intv)
                    if cand:
                        cand.status = f"{yeni_asama}. Mulakat Planlandi"
                        cand.updated_at = _now_str()
                        store.upsert("candidates", cand)
                    AuditLogger.log(store, f"mulakat_{yeni_asama}_oluşturuldu", "interview",
                                    yeni_intv.id, yeni_intv.interview_code)
                    styled_info_banner(
                        f"{karar}: {yeni_intv.interview_code} oluşturuldu. "
                        f"Mülakat Planlama sekmesinden tarih/saat/tip belirleyin.",
                        "success"
                    )
                else:
                    # Diger kararlar
                    if cand:
                        if karar == "Ise Alindi":
                            cand.status = "Ise Alindi"
                        elif karar == "Ret":
                            cand.status = "Ret"
                        elif karar == "Yedek":
                            cand.status = "Yedek"
                        elif karar == "Beklemede":
                            cand.status = "Beklemede"
                        cand.updated_at = _now_str()
                        store.upsert("candidates", cand)
                    styled_info_banner(f"Karar kaydedildi: {karar}", "success")

                AuditLogger.log(store, "karar_verildi", "interview", sel_intv.id,
                                f"{sel_intv.interview_code}: {karar}")
                st.rerun()

        # Karar verilmis mulakat ozeti
        styled_section("Son Kararlar", "#64748b")
        all_interviews = store.load_objects("interviews")
        kararli = [i for i in all_interviews if i.decision]
        if kararli:
            candidates = store.load_objects("candidates")
            cand_map2 = {c.id: c for c in candidates}
            son_kararlar = sorted(kararli, key=lambda x: x.updated_at or "", reverse=True)[:10]
            rows = []
            for iv in son_kararlar:
                c = cand_map2.get(iv.candidate_id)
                rows.append({
                    "Kod": iv.interview_code,
                    "Aday": c.tam_ad if c else "?",
                    "Asama": iv.stage,
                    "Karar": iv.decision,
                    "Katilimcilar": ", ".join(iv.interviewer_names) if iv.interviewer_names else "-",
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz karar verilmis mulakat yok.", "info")

    # ---- İşe Alınanlar ----
    with sub[6]:
        styled_section("İşe Alınanlar", "#059669")
        styled_info_banner(
            "Mulakat sonucu 'Ise Alindi' karari verilen adaylar burada listelenir. "
            "Evraklar tamamlaninca 'Kurum Aktif Çalışanları' sekmesine otomatik eklenir.",
            "info", "\U0001f389"
        )

        candidates = store.load_objects("candidates")
        ise_alinanlar = [c for c in candidates if c.status == "Ise Alindi"]
        evrak_data = store.load_list("ise_alim_evraklari")
        evrak_map = {e.get("candidate_id", ""): e for e in evrak_data}

        if not ise_alinanlar:
            styled_info_banner("Henuz ise alinan aday yok.", "warning")
        else:
            # Evrak tamamlanan sayisi
            evrak_tamam_sayisi = sum(
                1 for c in ise_alinanlar
                if evrak_map.get(c.id, {}).get("tamamlandı", False)
            )
            styled_stat_row([
                ("Ise Alinan", len(ise_alinanlar), "#10b981", "\u2705"),
                ("Evrak Tamam", evrak_tamam_sayisi, "#2563eb", "\U0001f4c4"),
                ("Evrak Eksik", len(ise_alinanlar) - evrak_tamam_sayisi, "#f59e0b", "\u23f3"),
                ("Ret / Yedek", sum(1 for c in candidates if c.status in ("Ret", "Yedek")), "#ef4444", "\U0001f4cb"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            # Ise alinan aday tablosu
            all_interviews = store.load_objects("interviews")
            applications = store.load_objects("applications")
            positions = store.load_objects("positions")
            pos_map = {p.position_code: p for p in positions}
            app_map = {a.candidate_id: a for a in applications}

            rows = []
            for c in ise_alinanlar:
                cand_interviews = [iv for iv in all_interviews if iv.candidate_id == c.id and iv.decision == "Ise Alindi"]
                son_mulakat = max(cand_interviews, key=lambda x: x.interview_date or "", default=None)
                puan_str = "-"
                if son_mulakat:
                    scores = store.find_by_field("interview_scores", "interview_id", son_mulakat.id)
                    if scores:
                        score_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in scores]
                        total = sum(s.score for s in score_objs)
                        max_p = len(score_objs) * 5
                        puan_str = f"{total}/{max_p} (%{total/max_p*100:.0f})" if max_p > 0 else "-"
                app = app_map.get(c.id)
                poz_adi = "-"
                if app:
                    pos = pos_map.get(app.position_code)
                    poz_adi = pos.position_name if pos else app.position_code
                evrak_durumu = "Tamam" if evrak_map.get(c.id, {}).get("tamamlandı", False) else "Eksik"
                rows.append({
                    "Aday Kodu": c.candidate_code,
                    "Ad Soyad": c.tam_ad,
                    "Pozisyon": poz_adi,
                    "Mulakat Puan": puan_str,
                    "Evrak Durumu": evrak_durumu,
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True, use_container_width=True)

            # Aday secimi - evrak takibi
            styled_section("Ise Alim Evrak Takibi", "#1e40af")
            det_labels = [f"{c.candidate_code} - {c.tam_ad}" for c in ise_alinanlar]
            det_idx = st.selectbox("Aday secin", range(len(det_labels)),
                                    format_func=lambda i: det_labels[i], key="ik_mul_isa_det")
            det_cand = ise_alinanlar[det_idx]

            # Kisisel bilgiler
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Ad Soyad:** {det_cand.tam_ad}")
                st.write(f"**TC No:** {det_cand.tc_no or '-'}")
                st.write(f"**Telefon:** {det_cand.telefon or '-'}")
            with c2:
                st.write(f"**Email:** {det_cand.email or '-'}")
                st.write(f"**Sehir:** {det_cand.sehir or '-'}")
                st.write(f"**Branş:** {det_cand.brans or '-'}")

            # Evrak kutucuklari
            styled_section("Ise Alim Belgeleri", "#059669")
            mevcut_evrak = evrak_map.get(det_cand.id, {})
            evrak_values = mevcut_evrak.get("evraklar", {})
            evrak_tamamlandı = mevcut_evrak.get("tamamlandı", False)

            # Kutucuklar - 2 sutun
            evrak_checks = {}
            col_a, col_b = st.columns(2)
            for i, (key, label) in enumerate(ISE_ALIM_EVRAKLARI):
                with col_a if i % 2 == 0 else col_b:
                    evrak_checks[key] = st.checkbox(
                        f"\U0001f4c4 {label}",
                        value=evrak_values.get(key, False),
                        key=f"ik_isa_evrak_{det_cand.id}_{key}",
                        disabled=evrak_tamamlandı,
                    )

            # Diger evrak notu
            diger_not = st.text_input(
                "Diger Belge Açıklaması",
                value=mevcut_evrak.get("diger_not", ""),
                key=f"ik_isa_evrak_diger_not_{det_cand.id}",
                disabled=evrak_tamamlandı,
            )

            # Evrak ozet goster
            teslim_edilen = sum(1 for v in evrak_checks.values() if v)
            toplam_evrak = len(ISE_ALIM_EVRAKLARI)
            eksik = toplam_evrak - teslim_edilen
            if eksik == 0:
                styled_info_banner(f"Tüm belgeler teslim edildi ({teslim_edilen}/{toplam_evrak}).", "success")
            else:
                eksik_listesi = [label for (key, label), v in zip(ISE_ALIM_EVRAKLARI, evrak_checks.values()) if not v]
                styled_info_banner(
                    f"{teslim_edilen}/{toplam_evrak} belge teslim edildi. "
                    f"Eksik: {', '.join(eksik_listesi)}",
                    "warning"
                )

            # Kaydet + Tamamlandı butonlari
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if not evrak_tamamlandı:
                    if st.button("Evraklari Kaydet", key=f"ik_isa_evrak_kaydet_{det_cand.id}",
                                 type="primary", use_container_width=True):
                        kayit = {
                            "id": mevcut_evrak.get("id", _gen_local_id("iae")),
                            "candidate_id": det_cand.id,
                            "candidate_code": det_cand.candidate_code,
                            "candidate_name": det_cand.tam_ad,
                            "evraklar": evrak_checks,
                            "diger_not": diger_not,
                            "tamamlandı": False,
                            "tamamlandı_tarih": "",
                            "updated_at": _now_str(),
                        }
                        # Upsert
                        found = False
                        for i, e in enumerate(evrak_data):
                            if e.get("candidate_id") == det_cand.id:
                                evrak_data[i] = kayit
                                found = True
                                break
                        if not found:
                            evrak_data.append(kayit)
                        store.save_list("ise_alim_evraklari", evrak_data)
                        styled_info_banner("Evrak durumu kaydedildi.", "success")
                        st.rerun()

            with btn_col2:
                if not evrak_tamamlandı:
                    if st.button("Evraklar Tamamlandı", key=f"ik_isa_evrak_tamam_{det_cand.id}",
                                 use_container_width=True):
                        kayit = {
                            "id": mevcut_evrak.get("id", _gen_local_id("iae")),
                            "candidate_id": det_cand.id,
                            "candidate_code": det_cand.candidate_code,
                            "candidate_name": det_cand.tam_ad,
                            "evraklar": evrak_checks,
                            "diger_not": diger_not,
                            "tamamlandı": True,
                            "tamamlandı_tarih": _now_str(),
                            "updated_at": _now_str(),
                        }
                        found = False
                        for i, e in enumerate(evrak_data):
                            if e.get("candidate_id") == det_cand.id:
                                evrak_data[i] = kayit
                                found = True
                                break
                        if not found:
                            evrak_data.append(kayit)
                        store.save_list("ise_alim_evraklari", evrak_data)

                        # Employee olustur (Kurum Aktif Calisani)
                        mevcut_emp = store.get_by_field("employees", "candidate_id", det_cand.id)
                        if not mevcut_emp:
                            app = app_map.get(det_cand.id)
                            pos_code = ""
                            pos_name = ""
                            role_scope = "ALL"
                            kampus = ""
                            kademe = ""
                            if app:
                                pos_code = app.position_code
                                kampus = app.kampus
                                kademe = app.kademe
                                pos = pos_map.get(app.position_code)
                                if pos:
                                    pos_name = pos.position_name
                                    role_scope = pos.role_scope

                            emp = Employee(
                                employee_code=store.next_employee_code(),
                                candidate_id=det_cand.id,
                                candidate_code=det_cand.candidate_code,
                                tc_no=det_cand.tc_no,
                                ad=det_cand.ad,
                                soyad=det_cand.soyad,
                                telefon=det_cand.telefon,
                                email=det_cand.email,
                                position_code=pos_code,
                                position_name=pos_name,
                                role_scope=role_scope,
                                brans=det_cand.brans,
                                kampus=kampus,
                                kademe=kademe,
                                ise_baslama_tarihi=date.today().isoformat(),
                                status="Aktif",
                            )
                            store.upsert("employees", emp)

                            # Tum modullere otomatik ekle (kim01_staff.json)
                            staff_id = sync_employee_to_shared_staff(emp.to_dict())
                            if staff_id:
                                emp.staff_id = staff_id
                                store.upsert("employees", emp)

                            AuditLogger.log(store, "ise_baslatildi", "employee", emp.id,
                                            f"{emp.employee_code} - {emp.tam_ad} (evrak tamamlandı)")

                        styled_info_banner(
                            f"Evraklar tamamlandı! {det_cand.tam_ad} Kurum Aktif Çalışanları'na ve tum modullere eklendi.",
                            "success"
                        )
                        st.rerun()
                else:
                    styled_info_banner(
                        f"Evraklar tamamlandı ({mevcut_evrak.get('tamamlandı_tarih', '')[:10]}). "
                        f"Bu aday Kurum Aktif Çalışanları sekmesinde gorunur.",
                        "success"
                    )

            # Mulakat gecmisi
            styled_section("Mülakat Geçmişi", "#8b5cf6")
            cand_all_intv = sorted(
                [iv for iv in all_interviews if iv.candidate_id == det_cand.id],
                key=lambda x: x.stage
            )
            if cand_all_intv:
                for iv in cand_all_intv:
                    k_icon = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                              "Beklemede": "\u23f3"}.get(iv.decision, "\u2796")
                    st.write(f"{k_icon} **Asama {iv.stage}** | {iv.interview_date} | "
                             f"{iv.interview_type} | Karar: {iv.decision or 'Bekliyor'}")
                    scores = store.find_by_field("interview_scores", "interview_id", iv.id)
                    if scores:
                        score_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in scores]
                        total = sum(s.score for s in score_objs)
                        avg = total / len(score_objs) if score_objs else 0
                        st.caption(f"Puan: {total}/{len(score_objs)*5} (Ort: {avg:.2f}/5)")
            else:
                st.write("Mulakat kaydi yok.")

    # ---- Mülakat Geçmişi ----
    with sub[7]:
        styled_section("Aday Bazli Mülakat Geçmişi", "#64748b")
        interviews = store.load_objects("interviews")
        candidates = store.load_objects("candidates")
        cand_map = {c.id: c for c in candidates}
        applications = store.load_objects("applications")
        _gc_app_map = {a.candidate_id: a for a in applications}
        positions = store.load_objects("positions")
        _gc_pos_map = {p.position_code: p for p in positions}

        if not interviews:
            styled_info_banner("Henuz mulakat kaydi yok.", "info")
        else:
            # Adaylari grupla
            _cand_ids_with_intv = list(dict.fromkeys(iv.candidate_id for iv in interviews))
            _gc_labels = []
            for cid in _cand_ids_with_intv:
                c = cand_map.get(cid)
                intv_count = len([iv for iv in interviews if iv.candidate_id == cid])
                _gc_labels.append(f"{c.tam_ad if c else '?'} ({intv_count} mulakat)")
            gc_idx = st.selectbox("Aday Secin", range(len(_gc_labels)),
                                   format_func=lambda i: _gc_labels[i], key="ik_mul_gecmis_aday")
            _gc_cand_id = _cand_ids_with_intv[gc_idx]
            _gc_cand = cand_map.get(_gc_cand_id)

            # Aday bilgi karti
            _gc_app = _gc_app_map.get(_gc_cand_id)
            _gc_pos = _gc_pos_map.get(_gc_app.position_code) if _gc_app else None
            _gc_info_html = (
                f'<div style="background:linear-gradient(135deg,#0B0F19 0%,#e2e8f0 100%);'
                f'border-radius:14px;padding:16px 20px;margin:10px 0;border-left:5px solid #64748b;">'
                f'<div style="display:flex;gap:28px;flex-wrap:wrap;">'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">ADAY</div>'
                f'<div style="font-size:16px;font-weight:700;color:#94A3B8;">{_gc_cand.tam_ad if _gc_cand else "?"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">POZISYON</div>'
                f'<div style="font-size:15px;font-weight:700;color:#2563eb;">{_gc_pos.position_name if _gc_pos else "-"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">BRANS</div>'
                f'<div style="font-size:15px;font-weight:700;color:#8b5cf6;">{_gc_cand.brans if _gc_cand else "-"}</div></div>'
                f'<div><div style="font-size:11px;color:#64748b;font-weight:600;">DURUM</div>'
                f'<div style="font-size:15px;font-weight:700;color:#0d9488;">{_gc_cand.status if _gc_cand else "-"}</div></div>'
                f'</div></div>'
            )
            st.markdown(_gc_info_html, unsafe_allow_html=True)

            # Tum mulakatlari timeline olarak goster
            _gc_intvs = sorted(
                [iv for iv in interviews if iv.candidate_id == _gc_cand_id],
                key=lambda x: x.stage
            )

            for iv in _gc_intvs:
                _gc_scores = store.find_by_field("interview_scores", "interview_id", iv.id)
                _gc_total = 0
                _gc_max = 0
                _gc_score_objs = []
                if _gc_scores:
                    _gc_score_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in _gc_scores]
                    _gc_total = sum(s.score for s in _gc_score_objs)
                    _gc_max = len(_gc_score_objs) * 5
                _gc_pct = (_gc_total / _gc_max * 100) if _gc_max > 0 else 0
                _gc_clr = "#10b981" if _gc_pct >= 70 else ("#f59e0b" if _gc_pct >= 50 else "#ef4444")
                if iv.status == "Planlandi":
                    _gc_clr = "#94a3b8"

                _gc_karar_icon = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                                  "Beklemede": "\u23f3", "2. Mülakata Devam": "\u27a1\ufe0f",
                                  "3. Mülakata Devam": "\u27a1\ufe0f"}.get(iv.decision, "")
                _gc_kat = ", ".join(iv.interviewer_names) if iv.interviewer_names else "Henuz atanmadi"

                _gc_durum_badge = {
                    "Planlandi": ("#94a3b8", "Planlandi"),
                    "Devam Ediyor": ("#f59e0b", "Devam Ediyor"),
                    "Tamamlandı": ("#10b981", "Tamamlandı"),
                    "Iptal": ("#ef4444", "Iptal"),
                }.get(iv.status, ("#64748b", iv.status))

                _gc_puan_txt = f'{_gc_total}/{_gc_max} (%{_gc_pct:.0f})' if _gc_max > 0 else 'Puan yok'
                _gc_karar_txt = f' {_gc_karar_icon} {iv.decision}' if iv.decision else ''
                _gc_gnote = f'<div style="margin-top:6px;font-size:12px;color:#94A3B8;background:#1A2035;padding:8px 12px;border-radius:8px;">{iv.general_note}</div>' if iv.general_note else ''
                _gc_tl_html = (
                    f'<div style="background:linear-gradient(135deg,#fff 0%,#111827 100%);'
                    f'border-radius:14px;padding:16px 20px;margin:10px 0;border-left:5px solid {_gc_clr};'
                    f'box-shadow:0 1px 3px rgba(0,0,0,0.06);">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">'
                    f'<div style="font-size:16px;font-weight:700;color:#94A3B8;">{iv.stage}. Mulakat'
                    f' <span style="background:{_gc_durum_badge[0]};color:#fff;font-size:11px;padding:2px 10px;'
                    f'border-radius:20px;margin-left:8px;">{_gc_durum_badge[1]}</span></div>'
                    f'<div style="font-size:14px;font-weight:700;color:{_gc_clr};">'
                    f'{_gc_puan_txt}{_gc_karar_txt}</div>'
                    f'</div>'
                    f'<div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:8px;font-size:13px;color:#475569;">'
                    f'<div>Tarih: <b>{iv.interview_date or "-"} {iv.interview_time or ""}</b></div>'
                    f'<div>Tip: <b>{iv.interview_type or "-"}</b></div>'
                    f'<div>Kod: <b>{iv.interview_code}</b></div>'
                    f'</div>'
                    f'<div style="margin-top:6px;font-size:12px;color:#64748b;">'
                    f'Mulakatcilar: <b>{_gc_kat}</b></div>'
                    f'{_gc_gnote}'
                    f'</div>'
                )
                st.markdown(_gc_tl_html, unsafe_allow_html=True)

                # Soru puanlari expander
                if _gc_score_objs:
                    with st.expander(f"{iv.stage}. Mulakat - Soru Puanlari ({len(_gc_score_objs)} soru)"):
                        _gc_s_rows = []
                        for s in sorted(_gc_score_objs, key=lambda x: x.order_no):
                            _set_label = {"REASK": "Tekrar", "CUSTOM": "Yeni"}.get(s.set_code, "Standart")
                            _gc_s_rows.append({
                                "No": s.order_no,
                                "Tip": _set_label,
                                "Soru": s.question_text[:70],
                                "Puan": f"{s.score}/5",
                                "Not": s.note or "-",
                            })
                        st.dataframe(pd.DataFrame(_gc_s_rows), hide_index=True, use_container_width=True)


# ============================================================
# SEKME 4: ONBOARDING (STUB)
# ============================================================

def _render_onboarding(store: IKDataStore):
    sub = st.tabs(["📄 Evrak Takibi", "🚀 İşe Başlatma"])

    # ---- Evrak Takibi ----
    with sub[0]:
        styled_section("Onboarding Evrak Takibi", "#10b981")
        candidates = store.load_objects("candidates")
        ise_alinan = [c for c in candidates if c.status == "Ise Alindi"]

        if not ise_alinan:
            styled_info_banner("'Ise Alindi' durumunda aday yok. Önce mulakat kararini verin.", "warning")
        else:
            cand_labels = [f"{c.candidate_code} - {c.tam_ad}" for c in ise_alinan]
            cand_idx = st.selectbox("Aday Secin", range(len(cand_labels)),
                                    format_func=lambda i: cand_labels[i], key="ik_onb_cand")
            sel_cand = ise_alinan[cand_idx]

            # Pozisyon bul -> role_scope
            app = store.get_by_field("applications", "candidate_id", sel_cand.id)
            role_scope = "ALL"
            if app:
                app_obj = Application.from_dict(app) if isinstance(app, dict) else app
                pos = store.get_by_field("positions", "position_code", app_obj.position_code)
                if pos:
                    pos_obj = Position.from_dict(pos) if isinstance(pos, dict) else pos
                    role_scope = pos_obj.role_scope

            # Zorunlu evraklari getir
            required_docs = OnboardingChecker.get_required_documents(role_scope, store, "ONBOARDING")
            all_templates = store.load_objects("document_templates")
            onb_templates = [t for t in all_templates if t.phase == "ONBOARDING" and t.is_active
                             and t.applies_to_role_scope in ("ALL", role_scope)]

            # Mevcut evrak kayitlari
            cand_docs = store.find_by_field("candidate_documents", "candidate_id", sel_cand.id)
            doc_status_map = {}
            for cd in cand_docs:
                cd_obj = CandidateDocument.from_dict(cd) if isinstance(cd, dict) else cd
                doc_status_map[cd_obj.document_code] = cd_obj

            styled_section(f"Evrak Listesi ({role_scope})", "#2563eb")
            for t in onb_templates:
                existing = doc_status_map.get(t.document_code)
                status = existing.status if existing else "Bekleniyor"
                is_required = t.required_rule in ("ALWAYS", "CONDITIONAL")
                req_label = "ZORUNLU" if is_required else "Opsiyonel"
                color = {"Onaylandi": "#10b981", "Bekleniyor": "#f59e0b", "Reddedildi": "#ef4444",
                         "Yuklendi": "#2563eb", "Eksik": "#ef4444"}.get(status, "#64748b")

                with st.expander(f"{t.document_code} - {t.document_name} [{req_label}] | Durum: {status}"):
                    new_status = st.selectbox("Durum", DOCUMENT_STATUSES,
                                              index=DOCUMENT_STATUSES.index(status) if status in DOCUMENT_STATUSES else 0,
                                              key=f"ik_onb_doc_{t.document_code}")
                    check_note = st.text_input("Not", value=existing.check_note if existing else "",
                                               key=f"ik_onb_note_{t.document_code}")
                    if st.button("Güncelle", key=f"ik_onb_btn_{t.document_code}"):
                        if existing:
                            existing.status = new_status
                            existing.check_note = check_note
                            existing.updated_at = _now_str()
                            store.upsert("candidate_documents", existing)
                        else:
                            cd = CandidateDocument(
                                candidate_id=sel_cand.id,
                                candidate_code=sel_cand.candidate_code,
                                document_code=t.document_code,
                                document_name=t.document_name,
                                phase="ONBOARDING",
                                status=new_status,
                                check_note=check_note,
                            )
                            store.upsert("candidate_documents", cd)
                        AuditLogger.log(store, f"evrak_{new_status.lower()}", "document",
                                        t.document_code, f"{sel_cand.tam_ad} - {t.document_name}")
                        styled_info_banner(f"{t.document_name} güncellendi: {new_status}", "success")
                        st.rerun()

    # ---- İşe Başlatma ----
    with sub[1]:
        styled_section("İşe Başlatma", "#059669")
        candidates = store.load_objects("candidates")
        ise_alinan = [c for c in candidates if c.status == "Ise Alindi"]

        if not ise_alinan:
            styled_info_banner("'Ise Alindi' durumunda aday yok.", "warning")
        else:
            cand_labels = [f"{c.candidate_code} - {c.tam_ad}" for c in ise_alinan]
            cand_idx = st.selectbox("Aday Secin", range(len(cand_labels)),
                                    format_func=lambda i: cand_labels[i], key="ik_onb_ise_cand")
            sel_cand = ise_alinan[cand_idx]

            # role_scope bul
            app = store.get_by_field("applications", "candidate_id", sel_cand.id)
            role_scope = "ALL"
            pos_code = ""
            pos_name = ""
            kampus = ""
            kademe = ""
            if app:
                app_obj = Application.from_dict(app) if isinstance(app, dict) else app
                pos_code = app_obj.position_code
                kampus = app_obj.kampus
                kademe = app_obj.kademe
                pos = store.get_by_field("positions", "position_code", pos_code)
                if pos:
                    pos_obj = Position.from_dict(pos) if isinstance(pos, dict) else pos
                    role_scope = pos_obj.role_scope
                    pos_name = pos_obj.position_name

            # Kilit kontrolu
            can_start, missing = OnboardingChecker.can_start_employment(sel_cand.id, role_scope, store)

            if missing:
                styled_info_banner(f"KILIT: {len(missing)} zorunlu evrak eksik/onaysiz:", "error")
                for m in missing:
                    st.markdown(f"- {m}")
                st.button("Ise Baslat", disabled=True, key="ik_onb_ise_btn_disabled")
            else:
                styled_info_banner("Tüm zorunlu evraklar onaylandi. Ise baslatilabilir.", "success")
                st.write(f"**Aday:** {sel_cand.tam_ad}")
                st.write(f"**Pozisyon:** {pos_code} - {pos_name}")
                st.write(f"**Kampus:** {kampus} | **Kademe:** {kademe}")

                ise_bas_tarih = st.date_input("Ise Baslama Tarihi", key="ik_onb_ise_tarih")

                if st.button("Ise Baslat", type="primary", key="ik_onb_ise_btn"):
                    emp = Employee(
                        employee_code=store.next_employee_code(),
                        candidate_id=sel_cand.id,
                        candidate_code=sel_cand.candidate_code,
                        tc_no=sel_cand.tc_no,
                        ad=sel_cand.ad,
                        soyad=sel_cand.soyad,
                        telefon=sel_cand.telefon,
                        email=sel_cand.email,
                        position_code=pos_code,
                        position_name=pos_name,
                        role_scope=role_scope,
                        brans=sel_cand.brans,
                        kampus=kampus,
                        kademe=kademe,
                        ise_baslama_tarihi=ise_bas_tarih.isoformat(),
                        status="Aktif",
                    )
                    store.upsert("employees", emp)

                    # Tum modullere otomatik ekle (kim01_staff.json)
                    staff_id = sync_employee_to_shared_staff(emp.to_dict())
                    if staff_id:
                        emp.staff_id = staff_id
                        store.upsert("employees", emp)

                    AuditLogger.log(store, "ise_baslatildi", "employee", emp.id,
                                    f"{emp.employee_code} - {emp.tam_ad}")
                    styled_info_banner(
                        f"Çalışan oluşturuldu: {emp.employee_code} - {emp.tam_ad}. Tüm modullere eklendi.",
                        "success"
                    )
                    st.rerun()


# ============================================================
# SEKME 5: PERFORMANS (STUB)
# ============================================================

def _render_performans(store: IKDataStore):
    sub = st.tabs([
        "📋 Değerlendirme Listesi", "➕ Yeni Değerlendirme",
        "🎓 Öğretmen Karnesi", "🤖 AI Analiz", "📊 Performans Analizi",
    ])

    # ---- 1) Değerlendirme Listesi ----
    with sub[0]:
        styled_section("Performans Değerlendirmeleri", "#8b5cf6")
        reviews = store.load_objects("performance_reviews")
        if reviews:
            # Filtreler
            f1, f2 = st.columns(2)
            with f1:
                calisan_isimleri = sorted(set(r.employee_name for r in reviews))
                filtre_calisan = st.selectbox("Çalışan Filtre", ["Tümü"] + calisan_isimleri,
                                              key="prf_flt_cal")
            with f2:
                filtre_no = st.selectbox("Değerlendirme No", ["Tümü", "1", "2", "3"],
                                          key="prf_flt_no")

            filtered = reviews
            if filtre_calisan != "Tümü":
                filtered = [r for r in filtered if r.employee_name == filtre_calisan]
            if filtre_no != "Tümü":
                filtered = [r for r in filtered if r.degerlendirme_no == int(filtre_no)]

            if filtered:
                rows = []
                for r in filtered:
                    rows.append({
                        "Çalışan": r.employee_name,
                        "Degerlendiren": r.degerlendiren_unvan or r.manager_name,
                        "No": f"{r.degerlendirme_no}.",
                        "Periyot": PERFORMANCE_PERIOD_LABELS.get(r.period_type, r.period_type),
                        "CORE": f"{r.core_avg:.2f}",
                        "ROLE": f"{r.role_avg:.2f}",
                        "Skor/100": f"{r.score_100:.1f}",
                        "Etiket": r.label,
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                styled_info_banner("Filtreye uygun degerlendirme bulunamadı.", "info")
        else:
            styled_info_banner("Henuz performans degerlendirmesi yok.", "info")

    # ---- 2) Yeni Değerlendirme ----
    with sub[1]:
        styled_section("Yeni Performans Değerlendirme", "#10b981")
        employees = store.load_objects("employees")
        aktif_emp = [e for e in employees if e.status == "Aktif"]

        if not aktif_emp:
            styled_info_banner("Aktif calisan yok. Önce ise baslatma yapin.", "warning")
        else:
            emp_labels = [f"{e.employee_code} - {e.tam_ad} ({e.role_scope})" for e in aktif_emp]
            emp_idx = st.selectbox("Çalışan Secin", range(len(emp_labels)),
                                   format_func=lambda i: emp_labels[i], key="ik_prf_emp")
            sel_emp = aktif_emp[emp_idx]

            # Degerlendiren unvan + degerlendirme no
            d1, d2 = st.columns(2)
            with d1:
                deg_unvan = st.selectbox("Değerlendirmeyi Yapan",
                                          DEGERLENDIREN_UNVANLAR, key="ik_prf_unvan")
            with d2:
                deg_no = st.selectbox("Kacinci Değerlendirme",
                                       [1, 2, 3],
                                       format_func=lambda x: f"{x}. Değerlendirme",
                                       key="ik_prf_deg_no")

            # Periyot secimi
            if sel_emp.role_scope in ("ADMIN", "SUPPORT"):
                period_options = PERFORMANCE_PERIOD_TYPES_IDARI
            else:
                period_options = PERFORMANCE_PERIOD_TYPES_OGRETMEN
            period_labels = [PERFORMANCE_PERIOD_LABELS.get(p, p) for p in period_options]
            period_idx = st.selectbox("Değerlendirme Periyodu", range(len(period_labels)),
                                      format_func=lambda i: period_labels[i], key="ik_prf_period")
            sel_period = period_options[period_idx]

            c1, c2 = st.columns(2)
            with c1:
                period_start = st.date_input("Periyot Başlangıç", key="ik_prf_start")
            with c2:
                period_end = st.date_input("Periyot Bitis", key="ik_prf_end")

            # Kriterleri yukle
            criteria = store.load_objects("performance_criteria")
            role_criteria = [c for c in criteria if c.group_type == "ROLE" and c.is_active
                             and c.role_scope == sel_emp.role_scope]

            all_scores: dict[str, int] = {}
            if role_criteria:
                # Kategorilere ayir
                cat_order: list[str] = []
                cat_map: dict[str, list] = {}
                for cr in role_criteria:
                    cat = cr.category or "Genel"
                    if cat not in cat_map:
                        cat_order.append(cat)
                        cat_map[cat] = []
                    cat_map[cat].append(cr)

                cat_colors = [
                    "#2563eb", "#8b5cf6", "#0d9488", "#ea580c", "#dc2626",
                    "#16a34a", "#ca8a04", "#7c3aed", "#0891b2", "#be185d",
                    "#4f46e5", "#059669", "#d97706", "#9333ea",
                ]
                for ci, cat in enumerate(cat_order):
                    cat_crs = cat_map[cat]
                    cat_weight = sum(c.weight for c in cat_crs)
                    c_color = cat_colors[ci % len(cat_colors)]
                    styled_section(f"{cat} (%{cat_weight:.0f})", c_color)
                    cols = st.columns(2)
                    for i, cr in enumerate(cat_crs):
                        with cols[i % 2]:
                            all_scores[cr.criterion_code] = st.number_input(
                                f"{cr.criterion_code}: {cr.criterion_name} (%{cr.weight:.0f})",
                                min_value=0, max_value=5, value=3, step=1,
                                key=f"ik_prf_{cr.criterion_code}")
            else:
                styled_info_banner(
                    f"{sel_emp.role_scope} için performans kriterleri bulunamadı. "
                    f"Ayarlar > Performans Kriterleri sekmesinden import edin.", "warning")

            styled_section("Değerlendirme Notu", "#0d9488")
            manager_note = st.text_area("Değerlendirme Notu (ZORUNLU)", key="ik_prf_mnote", height=100)
            action_plan = st.text_area("Aksiyon Plani (opsiyonel)", key="ik_prf_action", height=80)

            # Onizleme
            if all_scores and role_criteria:
                w_avg, score_100, label = PerformanceCalculator.calculate_weighted(
                    all_scores, role_criteria)
                color = PerformanceCalculator.get_label_color(label)
                st.markdown(
                    f'<div style="background:{color}15;border:2px solid {color};border-radius:12px;'
                    f'padding:16px;text-align:center;margin:12px 0">'
                    f'<div style="font-size:2rem;font-weight:800;color:{color}">{score_100:.1f}/100</div>'
                    f'<div style="font-size:1.1rem;font-weight:600;color:{color}">{label}</div>'
                    f'<div style="font-size:0.85rem;color:#64748b;margin-top:4px">'
                    f'Agirlikli Ortalama: {w_avg:.2f}/5</div>'
                    f'</div>', unsafe_allow_html=True,
                )

            if st.button("Değerlendirmeyi Kaydet", type="primary", key="ik_prf_kaydet"):
                if not manager_note.strip():
                    st.error("Değerlendirme notu zorunludur.")
                elif not all_scores:
                    st.error("Kriter puani girilmedi.")
                else:
                    w_avg, score_100, label = PerformanceCalculator.calculate_weighted(
                        all_scores, role_criteria)
                    review = PerformanceReview(
                        employee_id=sel_emp.id,
                        employee_code=sel_emp.employee_code,
                        employee_name=sel_emp.tam_ad,
                        role_scope=sel_emp.role_scope,
                        period_type=sel_period,
                        period_start=period_start.isoformat(),
                        period_end=period_end.isoformat(),
                        core_scores={},
                        role_scores=all_scores,
                        core_avg=0.0,
                        role_avg=w_avg,
                        score_100=score_100,
                        label=label,
                        manager_note=manager_note,
                        manager_name=deg_unvan,
                        action_plan=action_plan,
                        degerlendiren_unvan=deg_unvan,
                        degerlendirme_no=deg_no,
                        status="Tamamlandı",
                    )
                    store.upsert("performance_reviews", review)
                    AuditLogger.log(store, "performans_tamamlandı", "performance_review", review.id,
                                    f"{sel_emp.tam_ad}: {score_100:.1f} ({label})")
                    styled_info_banner(
                        f"Değerlendirme kaydedildi: {score_100:.1f}/100 - {label} "
                        f"({deg_unvan}, {deg_no}. Değerlendirme)", "success",
                    )
                    st.rerun()

    # ---- 3) Öğretmen Karnesi ----
    with sub[2]:
        styled_section("Öğretmen Performans Karnesi", "#1e40af")
        employees = store.load_objects("employees")
        aktif_ogretmenler = [e for e in employees if e.status == "Aktif"]
        if not aktif_ogretmenler:
            styled_info_banner("Aktif calisan bulunamadı.", "warning")
        else:
            ogr_labels = [f"{e.employee_code} - {e.tam_ad} ({e.role_scope})" for e in aktif_ogretmenler]
            ogr_idx = st.selectbox("Çalışan Secin", range(len(ogr_labels)),
                                    format_func=lambda i: ogr_labels[i], key="prf_karne_ogr")
            sel_ogr = aktif_ogretmenler[ogr_idx]

            all_reviews = store.load_objects("performance_reviews")
            ogr_reviews = [r for r in all_reviews if r.employee_id == sel_ogr.id]

            # Periyot filtre
            if ogr_reviews:
                periyotlar = sorted(set(r.period_type for r in ogr_reviews))
                per_labels = ["Tümü"] + [PERFORMANCE_PERIOD_LABELS.get(p, p) for p in periyotlar]
                per_sec = st.selectbox("Periyot Filtre", per_labels, key="prf_karne_per")
                if per_sec != "Tümü":
                    per_key = [k for k, v in PERFORMANCE_PERIOD_LABELS.items() if v == per_sec]
                    if per_key:
                        ogr_reviews = [r for r in ogr_reviews if r.period_type == per_key[0]]

            if not ogr_reviews:
                styled_info_banner("Bu calisan için henuz degerlendirme yapilmamis.", "info")
            else:
                # Ortalama hesapla
                ort_skor = sum(r.score_100 for r in ogr_reviews) / len(ogr_reviews)
                ort_core = sum(r.core_avg for r in ogr_reviews) / len(ogr_reviews)
                ort_role = sum(r.role_avg for r in ogr_reviews) / len(ogr_reviews)
                ort_label = PerformanceCalculator.get_label(ort_skor)
                ort_color = PerformanceCalculator.get_label_color(ort_label)

                # Ozet stat kartlar
                styled_stat_row([
                    ("Değerlendirme", len(ogr_reviews), "#2563eb", "📋"),
                    ("Ortalama Skor", f"{ort_skor:.1f}", ort_color, "🎯"),
                    ("CORE Ort", f"{ort_core:.2f}", "#0d9488", "📊"),
                    ("ROLE Ort", f"{ort_role:.2f}", "#8b5cf6", "📈"),
                ])

                # Ortalama sonuc karti
                st.markdown(
                    f'<div style="background:{ort_color}15;border:2px solid {ort_color};'
                    f'border-radius:12px;padding:16px;text-align:center;margin:12px 0">'
                    f'<div style="font-size:0.85rem;color:#64748b">GENEL ORTALAMA</div>'
                    f'<div style="font-size:2.5rem;font-weight:800;color:{ort_color}">'
                    f'{ort_skor:.1f}/100</div>'
                    f'<div style="font-size:1.2rem;font-weight:600;color:{ort_color}">'
                    f'{ort_label}</div></div>',
                    unsafe_allow_html=True,
                )

                # Her degerlendirme ayri kart
                styled_section("Değerlendirme Detaylari", "#2563eb")
                for r in sorted(ogr_reviews, key=lambda x: x.degerlendirme_no):
                    r_color = PerformanceCalculator.get_label_color(r.label)
                    r_unvan = r.degerlendiren_unvan or r.manager_name or "-"
                    st.markdown(
                        f'<div style="background:#111827;border:1px solid #e2e8f0;'
                        f'border-radius:10px;padding:14px 18px;margin:8px 0">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;'
                        f'flex-wrap:wrap;gap:8px">'
                        f'<div>'
                        f'<span style="font-weight:700;color:#94A3B8;font-size:1rem">'
                        f'{r.degerlendirme_no}. Değerlendirme</span>'
                        f'<span style="margin-left:12px;background:#64748b15;color:#64748b;'
                        f'padding:2px 8px;border-radius:6px;font-size:0.8rem">{r_unvan}</span>'
                        f'<span style="margin-left:8px;font-size:0.8rem;color:#94a3b8">'
                        f'{PERFORMANCE_PERIOD_LABELS.get(r.period_type, r.period_type)} | '
                        f'{r.period_start} - {r.period_end}</span>'
                        f'</div>'
                        f'<div style="text-align:right">'
                        f'<span style="font-size:1.4rem;font-weight:800;color:{r_color}">'
                        f'{r.score_100:.1f}</span>'
                        f'<span style="font-size:0.8rem;color:{r_color};margin-left:4px">'
                        f'{r.label}</span>'
                        f'</div></div>'
                        f'<div style="font-size:0.8rem;color:#64748b;margin-top:6px">'
                        f'Agirlikli Ort: {r.role_avg:.2f}/5'
                        f'</div>'
                        f'{"<div style=" + chr(34) + "font-size:0.8rem;color:#475569;margin-top:4px;font-style:italic" + chr(34) + ">" + r.manager_note + "</div>" if r.manager_note else ""}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # Grafikler
                st.markdown("<br>", unsafe_allow_html=True)
                gc1, gc2 = st.columns(2)
                with gc1:
                    styled_section("Değerlendirme Bazli Skorlar", "#4472C4")
                    deg_data = {}
                    for r in ogr_reviews:
                        deg_key = f"{r.degerlendirme_no}. ({r.degerlendiren_unvan or '-'})"
                        deg_data[deg_key] = r.score_100
                    st.markdown(
                        ReportStyler.horizontal_bar_html(deg_data, color="#4472C4", max_val=100.0),
                        unsafe_allow_html=True,
                    )

                with gc2:
                    styled_section("Kategori Bazli Ortalama", "#264478")
                    criteria = store.load_objects("performance_criteria")
                    # Kategori bazli ortalama hesapla
                    cat_scores: dict[str, list[float]] = {}
                    for r in ogr_reviews:
                        for code, val in {**r.core_scores, **r.role_scores}.items():
                            cr_obj = next((c for c in criteria if c.criterion_code == code), None)
                            cat = cr_obj.category if cr_obj and cr_obj.category else "Genel"
                            cat_scores.setdefault(cat, []).append(float(val))
                    kriter_data = {}
                    for cat, vals in cat_scores.items():
                        kriter_data[cat] = round(sum(vals) / len(vals), 2)
                    if kriter_data:
                        st.markdown(
                            ReportStyler.horizontal_bar_html(kriter_data, color="#264478", max_val=5.0),
                            unsafe_allow_html=True,
                        )

                # PDF Rapor
                styled_section("PDF Rapor", "#10b981")
                if st.button("Öğretmen Karnesi PDF Oluştur", type="primary", key="prf_karne_pdf"):
                    try:
                        info = get_institution_info()
                        pdf = ReportPDFGenerator(
                            f"Performans Karnesi - {sel_ogr.tam_ad}",
                            subtitle=f"Değerlendirme Sayısı: {len(ogr_reviews)}",
                        )
                        pdf.add_header(kurum_adi=info.get("name", ""))
                        pdf.add_section("Genel Özet")
                        pdf.add_metrics([
                            ("Çalışan", sel_ogr.tam_ad, "#2563eb"),
                            ("Ortalama Skor", f"{ort_skor:.1f}/100", ort_color),
                            ("Etiket", ort_label, ort_color),
                            ("Değerlendirme Sayısı", str(len(ogr_reviews)), "#64748b"),
                        ])

                        for r in sorted(ogr_reviews, key=lambda x: x.degerlendirme_no):
                            r_unvan = r.degerlendiren_unvan or r.manager_name or "-"
                            pdf.add_section(
                                f"{r.degerlendirme_no}. Değerlendirme - {r_unvan}",
                                color=PerformanceCalculator.get_label_color(r.label),
                            )
                            pdf.add_metrics([
                                ("Skor", f"{r.score_100:.1f}/100",
                                 PerformanceCalculator.get_label_color(r.label)),
                                ("Etiket", r.label,
                                 PerformanceCalculator.get_label_color(r.label)),
                                ("Agirlikli Ort.", f"{r.role_avg:.2f}/5", "#8b5cf6"),
                            ])
                            if r.manager_note:
                                pdf.add_text(f"Not: {r.manager_note}")
                            if r.action_plan:
                                pdf.add_text(f"Aksiyon Plani: {r.action_plan}")

                        pdf.add_section("Skor Grafigi")
                        if deg_data:
                            pdf.add_bar_chart(deg_data, "Değerlendirme Skorlari", "#2563eb")
                        if kriter_data:
                            pdf.add_section("Kategori Bazli Ortalama")
                            pdf.add_bar_chart(kriter_data, "Kategori Ortalamalari (0-5)", "#264478")

                        pdf_bytes = pdf.generate()
                        st.download_button(
                            "PDF Indir",
                            pdf_bytes,
                            file_name=f"performans_karne_{sel_ogr.tam_ad.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key="prf_karne_dl",
                        )
                        st.success("PDF oluşturuldu!")
                    except Exception as e:
                        st.error(f"PDF olusturma hatasi: {e}")

    # ---- 4) AI Analiz ----
    with sub[3]:
        styled_section("AI Performans Analizi", "#8b5cf6")
        employees = store.load_objects("employees")
        aktif_all = [e for e in employees if e.status == "Aktif"]
        if not aktif_all:
            styled_info_banner("Aktif calisan bulunamadı.", "warning")
        else:
            ai_labels = [f"{e.employee_code} - {e.tam_ad}" for e in aktif_all]
            ai_idx = st.selectbox("Çalışan Secin", range(len(ai_labels)),
                                   format_func=lambda i: ai_labels[i], key="prf_ai_ogr")
            sel_ai = aktif_all[ai_idx]

            all_reviews = store.load_objects("performance_reviews")
            ai_reviews = [r for r in all_reviews if r.employee_id == sel_ai.id]

            if not ai_reviews:
                styled_info_banner("Bu calisan için henuz degerlendirme yok.", "info")
            else:
                # Veri ozeti
                ort = sum(r.score_100 for r in ai_reviews) / len(ai_reviews)
                deg_ozet = "\n".join([
                    f"- {r.degerlendirme_no}. Değerlendirme ({r.degerlendiren_unvan or '-'}): "
                    f"Skor={r.score_100:.1f}/100, Etiket={r.label}, "
                    f"Agirlikli Ort={r.role_avg:.2f}/5, "
                    f"Not: {r.manager_note or '-'}"
                    for r in ai_reviews
                ])

                criteria = store.load_objects("performance_criteria")
                kriter_ozet_parts = []
                for r in ai_reviews:
                    for code, val in {**r.core_scores, **r.role_scores}.items():
                        cr_obj = next((c for c in criteria if c.criterion_code == code), None)
                        cat = f"[{cr_obj.category}] " if cr_obj and cr_obj.category else ""
                        kriter_ozet_parts.append(
                            f"{cat}{cr_obj.criterion_name if cr_obj else code}: {val}/5"
                        )

                if st.button("AI Analiz Oluştur", type="primary", key="prf_ai_gen"):
                    with st.spinner("AI analiz raporu olusturuluyor..."):
                        try:
                            from openai import OpenAI
                            client = OpenAI()
                            prompt = (
                                f"Bir okul yoneticisi olarak asagidaki ogretmen performans "
                                f"degerlendirme verilerini analiz et.\n\n"
                                f"OGRETMEN: {sel_ai.tam_ad}\n"
                                f"POZISYON: {sel_ai.role_scope}\n"
                                f"DEGERLENDIRME SAYISI: {len(ai_reviews)}\n"
                                f"GENEL ORTALAMA: {ort:.1f}/100\n\n"
                                f"DEGERLENDIRMELER:\n{deg_ozet}\n\n"
                                f"KRITER PUANLARI:\n" + ", ".join(kriter_ozet_parts[:30]) + "\n\n"
                                f"Lutfen su basliklarda detayli analiz yap:\n"
                                f"1. GENEL DEGERLENDIRME\n"
                                f"2. GUCLU YONLER\n"
                                f"3. GELISIM ALANLARI\n"
                                f"4. AKSIYON ONERILERI\n"
                                f"5. KARSILASTIRMALI ANALIZ "
                                f"(degerlendirmeler arasi farklar, tutarlilik)\n\n"
                                f"Turkce yaz, somut ve yapici oneriler sun."
                            )
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system",
                                     "content": "Sen bir egitim uzmani ve okul danismanisin. "
                                                "Öğretmen performans degerlendirmelerini analiz edip "
                                                "somut oneriler sunuyorsun."},
                                    {"role": "user", "content": prompt},
                                ],
                                temperature=0.7,
                                max_tokens=2500,
                            )
                            ai_text = response.choices[0].message.content or ""
                            st.session_state["prf_ai_rapor"] = ai_text
                            st.session_state["prf_ai_name"] = sel_ai.tam_ad
                            st.success("AI analiz raporu oluşturuldu!")
                        except Exception as e:
                            st.error(f"AI analiz olusturulamadi: {e}")
                            st.info("OpenAI API anahtarinin dogru ayarlandigindan emin olun.")

                if "prf_ai_rapor" in st.session_state and st.session_state.get("prf_ai_name") == sel_ai.tam_ad:
                    st.markdown("---")
                    st.markdown(st.session_state["prf_ai_rapor"])
                    st.download_button(
                        "AI Raporu Indir (TXT)",
                        st.session_state["prf_ai_rapor"],
                        file_name=f"performans_ai_{sel_ai.tam_ad.replace(' ', '_')}.txt",
                        mime="text/plain",
                        key="prf_ai_dl",
                    )

    # ---- 5) Performans Analizi ----
    with sub[4]:
        styled_section("Performans Analizi", "#1e40af")
        reviews = store.load_objects("performance_reviews")
        if reviews:
            # Etiket dagilimi
            label_counts: dict[str, int] = {}
            for r in reviews:
                label_counts[r.label] = label_counts.get(r.label, 0) + 1
            styled_stat_row([
                ("Çok Iyi", label_counts.get("Çok Iyi", 0), "#10b981", "\u2B50"),
                ("Iyi", label_counts.get("Iyi", 0), "#2563eb", "\U0001f44d"),
                ("Gelismeli", label_counts.get("Gelismeli", 0), "#f59e0b", "\U0001f4dd"),
                ("Yetersiz", label_counts.get("Yetersiz", 0), "#ef4444", "\u26a0\ufe0f"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            pa_c1, pa_c2 = st.columns(2)
            with pa_c1:
                styled_section("Etiket Dagilimi", "#8b5cf6")
                st.markdown(
                    ReportStyler.donut_chart_svg(
                        {k: float(v) for k, v in label_counts.items()}, size=155
                    ),
                    unsafe_allow_html=True,
                )
            with pa_c2:
                styled_section("Çalışan Performans Skorlari", "#4472C4")
                calisan_skorlar = {r.employee_name: r.score_100 for r in reviews}
                st.markdown(
                    ReportStyler.horizontal_bar_html(calisan_skorlar, color="#4472C4", max_val=100.0),
                    unsafe_allow_html=True,
                )

            styled_section("Performans Sunburst", "#264478")
            etiket_inner: dict[str, float] = {}
            etiket_outer: dict[str, list[tuple[str, float]]] = {}
            for r in reviews:
                etiket_inner[r.label] = etiket_inner.get(r.label, 0) + 1
                etiket_outer.setdefault(r.label, []).append((r.employee_name, r.score_100))
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    etiket_inner, etiket_outer, size=380,
                    title="Performans Değerlendirme Dagilimi",
                ),
                unsafe_allow_html=True,
            )

            styled_section("Detay Tablo", "#64748b")
            df = pd.DataFrame([{
                "Çalışan": r.employee_name,
                "Degerlendiren": r.degerlendiren_unvan or r.manager_name,
                "No": r.degerlendirme_no,
                "Periyot": PERFORMANCE_PERIOD_LABELS.get(r.period_type, r.period_type),
                "Skor": r.score_100,
                "Etiket": r.label,
            } for r in reviews])
            st.dataframe(df, hide_index=True, use_container_width=True)

            styled_section("Role Scope Bazinda Ortalama", "#8b5cf6")
            scope_scores: dict[str, list[float]] = {}
            for r in reviews:
                scope_scores.setdefault(r.role_scope, []).append(r.score_100)
            scope_avg_data = {k: round(sum(v) / len(v), 1) for k, v in scope_scores.items()}
            st.markdown(
                ReportStyler.horizontal_bar_html(scope_avg_data, color="#264478", max_val=100.0),
                unsafe_allow_html=True,
            )

            # PDF Export
            styled_section("PDF Rapor", "#10b981")
            if st.button("Genel Performans Raporu PDF", type="primary", key="prf_genel_pdf"):
                try:
                    info = get_institution_info()
                    pdf = ReportPDFGenerator("Performans Değerlendirme Genel Raporu")
                    pdf.add_header(kurum_adi=info.get("name", ""))
                    pdf.add_section("Etiket Dagilimi")
                    pdf.add_metrics([
                        ("Çok Iyi", str(label_counts.get("Çok Iyi", 0)), "#10b981"),
                        ("Iyi", str(label_counts.get("Iyi", 0)), "#2563eb"),
                        ("Gelismeli", str(label_counts.get("Gelismeli", 0)), "#f59e0b"),
                        ("Yetersiz", str(label_counts.get("Yetersiz", 0)), "#ef4444"),
                    ])
                    pdf.add_section("Çalışan Skorlari")
                    pdf.add_bar_chart(calisan_skorlar, "Performans Skorlari (0-100)", "#2563eb")
                    pdf.add_section("Detay Tablosu")
                    pdf.add_table(df, "#1565c0")
                    if scope_avg_data:
                        pdf.add_section("Role Scope Ortalaması")
                        pdf.add_bar_chart(scope_avg_data, "Role Scope Bazinda Ortalama", "#264478")
                    pdf_bytes = pdf.generate()
                    st.download_button(
                        "PDF Indir",
                        pdf_bytes,
                        file_name="performans_genel_rapor.pdf",
                        mime="application/pdf",
                        key="prf_genel_dl",
                    )
                    st.success("PDF oluşturuldu!")
                except Exception as e:
                    st.error(f"PDF olusturma hatasi: {e}")
        else:
            styled_info_banner("Henuz performans verisi yok.", "info")


# ============================================================
# SEKME 6: IZIN YONETIMI (STUB)
# ============================================================

def _render_izin_yonetimi(store: IKDataStore):
    izinler = store.load_list("izinler")
    sub = st.tabs(["📋 İzin Talepleri", "➕ Yeni İzin Talebi", "💰 İzin Bakiye", "📅 İzin Takvimi",
                    "📝 Rapor Yönetimi", "❌ Devamsızlık", "⏰ Geç Kalma", "📊 Performans Alt Raporu"])

    with sub[0]:
        styled_section("İzin Talepleri", "#f59e0b")
        c1, c2, c3 = st.columns(3)
        with c1:
            durum_f = st.selectbox("Durum", ["Tümü", "Beklemede", "Onaylandi", "Reddedildi"], key="ik_izin_durum")
        with c2:
            tip_f = st.selectbox("İzin Tipi", ["Tümü"] + list(IZIN_TIPLERI.values()), key="ik_izin_tip")
        with c3:
            per_f = st.text_input("Personel Ara", key="ik_izin_per_ara")

        filtered = izinler
        if durum_f != "Tümü":
            d_map = {"Beklemede": "beklemede", "Onaylandi": "onaylandi", "Reddedildi": "reddedildi"}
            filtered = [i for i in filtered if i.get("durum") == d_map.get(durum_f)]
        if tip_f != "Tümü":
            t_key = next((k for k, v in IZIN_TIPLERI.items() if v == tip_f), None)
            if t_key:
                filtered = [i for i in filtered if i.get("izin_tipi") == t_key]
        if per_f:
            filtered = [i for i in filtered if per_f.lower() in i.get("personel_adi", "").lower()]

        if filtered:
            df = pd.DataFrame([{
                "Personel": i.get("personel_adi", ""),
                "İzin Tipi": IZIN_TIPLERI.get(i.get("izin_tipi", ""), ""),
                "Başlangıç": i.get("baslangic", ""),
                "Bitis": i.get("bitis", ""),
                "Gün": i.get("gun_sayisi", 0),
                "Gerekçe": i.get("aciklama", "-"),
                "Durum": i.get("durum", "").capitalize(),
            } for i in filtered])
            st.dataframe(df, hide_index=True, use_container_width=True)

            bekleyen = [i for i in filtered if i.get("durum") == "beklemede"]
            if bekleyen:
                styled_section("Onay / Red", "#2563eb")
                sec_l = [f"{b.get('personel_adi')} - {IZIN_TIPLERI.get(b.get('izin_tipi',''),'')} ({b.get('baslangic')})"
                         for b in bekleyen]
                sec_i = st.selectbox("Talep", range(len(sec_l)), format_func=lambda i: sec_l[i], key="ik_izin_onay_sec")
                onay_notu = st.text_input("Not", key="ik_izin_onay_notu")
                o1, o2 = st.columns(2)
                with o1:
                    if st.button("Onayla", type="primary", key="ik_izin_onayla"):
                        for iz in izinler:
                            if iz.get("id") == bekleyen[sec_i].get("id"):
                                iz["durum"] = "onaylandi"
                                iz["onay_notu"] = onay_notu
                                iz["updated_at"] = _now_str()
                        store.save_list("izinler", izinler)
                        st.rerun()
                with o2:
                    if st.button("Reddet", key="ik_izin_reddet"):
                        for iz in izinler:
                            if iz.get("id") == bekleyen[sec_i].get("id"):
                                iz["durum"] = "reddedildi"
                                iz["onay_notu"] = onay_notu
                                iz["updated_at"] = _now_str()
                        store.save_list("izinler", izinler)
                        st.rerun()
        else:
            styled_info_banner("İzin talebi bulunamadı.", "info")

    with sub[1]:
        styled_section("Yeni İzin Talebi", "#10b981")
        secili = _personel_selectbox("ik_izin_personel", "Personel Secin")
        c1, c2 = st.columns(2)
        with c1:
            izin_tipi = st.selectbox("İzin Tipi", list(IZIN_TIPLERI.keys()),
                                     format_func=lambda k: IZIN_TIPLERI[k], key="ik_izin_tipi")
            baslangic = st.date_input("Başlangıç", key="ik_izin_bas")
        with c2:
            bitis = st.date_input("Bitis", key="ik_izin_bit")
            aciklama = st.text_area("Açıklama", key="ik_izin_aciklama", height=80)

        if secili:
            gun = (bitis - baslangic).days + 1
            st.info(f"Toplam: **{gun} gun**")

        if st.button("İzin Talebi Oluştur", type="primary", key="ik_izin_olustur"):
            if not secili:
                st.error("Personel secin.")
            elif bitis < baslangic:
                st.error("Bitis tarihi baslangictan once olamaz.")
            else:
                gun = (bitis - baslangic).days + 1
                yeni = {
                    "id": _gen_local_id("izn"),
                    "personel_id": secili.get("id", ""),
                    "personel_adi": f"{secili.get('ad', '')} {secili.get('soyad', '')}",
                    "izin_tipi": izin_tipi, "baslangic": baslangic.isoformat(),
                    "bitis": bitis.isoformat(), "gun_sayisi": gun,
                    "aciklama": aciklama, "durum": "beklemede",
                    "onay_notu": "", "created_at": _now_str(), "updated_at": _now_str(),
                }
                izinler.append(yeni)
                store.save_list("izinler", izinler)
                styled_info_banner(f"İzin talebi oluşturuldu ({gun} gun).", "success")
                st.rerun()

    with sub[2]:
        styled_section("İzin Bakiyeleri", "#8b5cf6")
        staff = _get_personel_options()
        if staff:
            rows = []
            for s in staff:
                pid = s.get("id", "")
                kisi_izin = [i for i in izinler if i.get("personel_id") == pid and i.get("durum") == "onaylandi"]
                yillik_kull = sum(i.get("gun_sayisi", 0) for i in kisi_izin if i.get("izin_tipi") == "yillik")
                hak = IZIN_VARSAYILAN_GUN.get("yillik", 14)
                rows.append({
                    "Personel": f"{s.get('ad', '')} {s.get('soyad', '')}",
                    "Yıllık Hak": hak, "Kullanilan": yillik_kull, "Kalan": hak - yillik_kull,
                    "Toplam İzin": sum(i.get("gun_sayisi", 0) for i in kisi_izin),
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Personel yok.", "warning")

    with sub[3]:
        styled_section("İzin Takvimi", "#0d9488")
        onaylilar = [i for i in izinler if i.get("durum") == "onaylandi"]
        if onaylilar:
            ay_sec = st.selectbox("Ay", [f"2026-{str(m).zfill(2)}" for m in range(1, 13)],
                                  index=datetime.now().month - 1, key="ik_izin_takvim_ay")
            ay_izinler = [i for i in onaylilar
                          if i.get("baslangic", "")[:7] <= ay_sec and i.get("bitis", "")[:7] >= ay_sec]
            for iz in ay_izinler:
                st.markdown(f"**{iz.get('personel_adi','')}** | {IZIN_TIPLERI.get(iz.get('izin_tipi',''),'')} | "
                            f"{iz.get('baslangic','')} - {iz.get('bitis','')} ({iz.get('gun_sayisi',0)} gun)")
            if not ay_izinler:
                styled_info_banner("Bu ayda onaylanmis izin yok.", "info")
        else:
            styled_info_banner("Onaylanmis izin yok.", "info")

    with sub[4]:
        _render_rapor_yonetimi(store)

    with sub[5]:
        _render_devamsizlik(store)

    with sub[6]:
        _render_gec_kalma(store)

    with sub[7]:
        _render_performans_alt_raporu(store)


def _render_rapor_yonetimi(store: IKDataStore):
    """Sağlık raporu / istirahat raporu yönetimi."""
    raporlar = store.load_list("raporlar")

    RAPOR_TURLERI = {
        "istirahat": "İstirahat Raporu",
        "hastalik": "Hastalık Raporu",
        "is_kazasi": "İş Kazası Raporu",
        "hamilelik": "Hamilelik / Doğum Raporu",
        "heyet": "Sağlık Kurulu (Heyet) Raporu",
        "diger": "Diğer",
    }

    RAPOR_DURUMLARI = {
        "aktif": ("Aktif", "#10b981"),
        "bitti": ("Süresi Doldu", "#64748b"),
        "iptal": ("İptal", "#ef4444"),
    }

    r_sub = st.tabs(["📋 Rapor Listesi", "➕ Yeni Rapor Girişi"])

    # ───── RAPOR LİSTESİ ─────
    with r_sub[0]:
        styled_section("Rapor Kayıtları", "#0d9488")

        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            rp_durum_f = st.selectbox("Durum", ["Tümü", "Aktif", "Süresi Doldu", "İptal"], key="ik_rp_durum")
        with rc2:
            rp_tur_f = st.selectbox("Rapor Türü", ["Tümü"] + list(RAPOR_TURLERI.values()), key="ik_rp_tur")
        with rc3:
            rp_per_f = st.text_input("Personel Ara", key="ik_rp_per_ara")

        filtered_r = raporlar

        if rp_durum_f != "Tümü":
            d_map_r = {"Aktif": "aktif", "Süresi Doldu": "bitti", "İptal": "iptal"}
            filtered_r = [r for r in filtered_r if r.get("durum") == d_map_r.get(rp_durum_f)]
        if rp_tur_f != "Tümü":
            t_key_r = next((k for k, v in RAPOR_TURLERI.items() if v == rp_tur_f), None)
            if t_key_r:
                filtered_r = [r for r in filtered_r if r.get("rapor_turu") == t_key_r]
        if rp_per_f:
            filtered_r = [r for r in filtered_r if rp_per_f.lower() in r.get("personel_adi", "").lower()]

        # Özet kartlar
        aktif_r = len([r for r in raporlar if r.get("durum") == "aktif"])
        toplam_gun = sum(r.get("gun_sayisi", 0) for r in raporlar)
        styled_stat_row([
            ("Toplam Rapor", len(raporlar), "#0d9488", "📋"),
            ("Aktif Rapor", aktif_r, "#f59e0b", "⏳"),
            ("Toplam Gün", toplam_gun, "#8b5cf6", "📅"),
        ])
        st.markdown("<br>", unsafe_allow_html=True)

        if filtered_r:
            filtered_r.sort(key=lambda r: r.get("rapor_tarihi", ""), reverse=True)
            df_r = pd.DataFrame([{
                "Personel": r.get("personel_adi", ""),
                "Rapor Türü": RAPOR_TURLERI.get(r.get("rapor_turu", ""), ""),
                "Rapor Tarihi": r.get("rapor_tarihi", ""),
                "Başlangıç": r.get("baslangic_tarihi", ""),
                "Bitiş": r.get("bitis_tarihi", ""),
                "Gün": r.get("gun_sayisi", 0),
                "Gerekçe / Tanı": r.get("tani", "-"),
                "Veren Kurum": r.get("veren_kurum", ""),
                "Durum": RAPOR_DURUMLARI.get(r.get("durum", ""), ("", ""))[0],
            } for r in filtered_r])
            st.dataframe(df_r, hide_index=True, use_container_width=True)

            # Detay görüntüleme
            styled_section("Rapor Detayı", "#2563eb")
            det_labels = [
                f"{r.get('personel_adi', '')} - {RAPOR_TURLERI.get(r.get('rapor_turu', ''), '')} ({r.get('rapor_tarihi', '')})"
                for r in filtered_r
            ]
            det_idx = st.selectbox("Rapor Seç", range(len(det_labels)),
                                    format_func=lambda i: det_labels[i], key="ik_rp_det_sec")
            sel_r = filtered_r[det_idx]

            dc1, dc2 = st.columns(2)
            with dc1:
                st.write(f"**Personel:** {sel_r.get('personel_adi', '')}")
                st.write(f"**Rapor Türü:** {RAPOR_TURLERI.get(sel_r.get('rapor_turu', ''), '')}")
                st.write(f"**Rapor Tarihi:** {sel_r.get('rapor_tarihi', '')}")
                st.write(f"**Başlangıç:** {sel_r.get('baslangic_tarihi', '')}")
                st.write(f"**Bitiş:** {sel_r.get('bitis_tarihi', '')}")
                st.write(f"**Gün Sayısı:** {sel_r.get('gun_sayisi', 0)}")
            with dc2:
                st.write(f"**Veren Kurum:** {sel_r.get('veren_kurum', '')}")
                st.write(f"**Doktor Adı:** {sel_r.get('doktor_adi', '')}")
                st.write(f"**Rapor No / Protokol:** {sel_r.get('rapor_no', '')}")
                st.write(f"**Tanı / Açıklama:** {sel_r.get('tani', '')}")
                st.write(f"**Göreve Başlama Tarihi:** {sel_r.get('goreve_baslama_tarihi', '')}")
                _durum_label, _durum_renk = RAPOR_DURUMLARI.get(sel_r.get("durum", ""), ("", "#64748b"))
                st.markdown(f"**Durum:** <span style='color:{_durum_renk};font-weight:700;'>{_durum_label}</span>",
                            unsafe_allow_html=True)

            if sel_r.get("notlar"):
                st.write(f"**Notlar:** {sel_r.get('notlar', '')}")

            # Durum güncelleme
            yeni_durum = st.selectbox("Durum Güncelle", list(RAPOR_DURUMLARI.keys()),
                                       format_func=lambda k: RAPOR_DURUMLARI[k][0], key="ik_rp_durum_guncelle")
            if st.button("Durumu Güncelle", key="ik_rp_durum_btn"):
                for rp in raporlar:
                    if rp.get("id") == sel_r.get("id"):
                        rp["durum"] = yeni_durum
                        rp["updated_at"] = _now_str()
                store.save_list("raporlar", raporlar)
                st.success("Rapor durumu güncellendi.")
                st.rerun()
        else:
            styled_info_banner("Rapor kaydı bulunamadı.", "info")

    # ───── YENİ RAPOR GİRİŞİ ─────
    with r_sub[1]:
        styled_section("Yeni Rapor Girişi", "#10b981")

        secili_rp = _personel_selectbox("ik_rp_personel", "Personel Seçin")

        c1, c2 = st.columns(2)
        with c1:
            rapor_turu = st.selectbox("Rapor Türü *", list(RAPOR_TURLERI.keys()),
                                       format_func=lambda k: RAPOR_TURLERI[k], key="ik_rp_tur_yeni")
            rapor_tarihi = st.date_input("Rapor Tarihi *", key="ik_rp_tarih")
            baslangic_t = st.date_input("Rapor Başlangıç Tarihi *", key="ik_rp_bas")
            bitis_t = st.date_input("Rapor Bitiş Tarihi *", key="ik_rp_bit")
        with c2:
            veren_kurum = st.text_input("Raporu Veren Kurum *", key="ik_rp_kurum",
                                         placeholder="Örn: Şehir Hastanesi, Aile Sağlığı Merkezi")
            doktor_adi = st.text_input("Doktor Adı", key="ik_rp_doktor")
            rapor_no = st.text_input("Rapor No / Protokol No", key="ik_rp_no")
            goreve_baslama = st.date_input("Göreve Başlama Tarihi", key="ik_rp_goreve_bas",
                                            help="Raporun bitişinden sonra göreve başlayacağı tarih")

        tani = st.text_area("Tanı / Açıklama", key="ik_rp_tani", height=80,
                             placeholder="Rapor tanısı veya açıklama notu")
        notlar = st.text_area("Ek Notlar", key="ik_rp_notlar", height=60)

        if secili_rp and bitis_t >= baslangic_t:
            gun_sayisi = (bitis_t - baslangic_t).days + 1
            st.info(f"Rapor Süresi: **{gun_sayisi} gün** | Göreve Başlama: **{goreve_baslama.isoformat()}**")

        if st.button("Rapor Kaydet", type="primary", key="ik_rp_kaydet"):
            if not secili_rp:
                st.error("Personel seçin.")
            elif not veren_kurum.strip():
                st.error("Raporu veren kurum zorunludur.")
            elif bitis_t < baslangic_t:
                st.error("Bitiş tarihi başlangıçtan önce olamaz.")
            else:
                gun_sayisi = (bitis_t - baslangic_t).days + 1
                yeni_rapor = {
                    "id": _gen_local_id("rpr"),
                    "personel_id": secili_rp.get("id", ""),
                    "personel_adi": f"{secili_rp.get('ad', '')} {secili_rp.get('soyad', '')}",
                    "rapor_turu": rapor_turu,
                    "rapor_tarihi": rapor_tarihi.isoformat(),
                    "baslangic_tarihi": baslangic_t.isoformat(),
                    "bitis_tarihi": bitis_t.isoformat(),
                    "gun_sayisi": gun_sayisi,
                    "veren_kurum": veren_kurum.strip(),
                    "doktor_adi": doktor_adi.strip(),
                    "rapor_no": rapor_no.strip(),
                    "goreve_baslama_tarihi": goreve_baslama.isoformat(),
                    "tani": tani.strip(),
                    "notlar": notlar.strip(),
                    "durum": "aktif",
                    "created_at": _now_str(),
                    "updated_at": _now_str(),
                }
                raporlar.append(yeni_rapor)
                store.save_list("raporlar", raporlar)
                styled_info_banner(f"Rapor kaydedildi — {gun_sayisi} gün istirahat.", "success")
                st.rerun()


# ============================================================
# DEVAMSIZLIK YÖNETİMİ
# ============================================================

DEVAMSIZLIK_TURLERI = {
    "mazeretsiz": "Mazeretsiz Devamsızlık",
    "mazeretli": "Mazeretli Devamsızlık",
    "izinli": "İzinli (Rapor/İzin Kaynaklı)",
    "gorev": "Görevli / Seminer",
    "diger": "Diğer",
}


def _render_devamsizlik(store: IKDataStore):
    """Mazeretsiz devamsızlık, izinli/mazeretli devamsızlık takibi."""
    devamsizlik = store.load_list("devamsizlik")

    d_sub = st.tabs(["📋 Devamsızlık Listesi", "➕ Yeni Devamsızlık Girişi"])

    # ── LİSTE ──
    with d_sub[0]:
        styled_section("Devamsızlık Kayıtları", "#ef4444")

        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            d_tur_f = st.selectbox("Tür", ["Tümü"] + list(DEVAMSIZLIK_TURLERI.values()), key="ik_dev_tur")
        with dc2:
            d_ay_f = st.selectbox("Ay", ["Tümü"] + [f"2026-{str(m).zfill(2)}" for m in range(1, 13)],
                                  key="ik_dev_ay")
        with dc3:
            d_per_f = st.text_input("Personel Ara", key="ik_dev_per_ara")

        filtered_d = devamsizlik
        if d_tur_f != "Tümü":
            t_key = next((k for k, v in DEVAMSIZLIK_TURLERI.items() if v == d_tur_f), None)
            if t_key:
                filtered_d = [d for d in filtered_d if d.get("tur") == t_key]
        if d_ay_f != "Tümü":
            filtered_d = [d for d in filtered_d if d.get("tarih", "")[:7] == d_ay_f]
        if d_per_f:
            filtered_d = [d for d in filtered_d if d_per_f.lower() in d.get("personel_adi", "").lower()]

        # Özet
        mazeretsiz = len([d for d in devamsizlik if d.get("tur") == "mazeretsiz"])
        mazeretli = len([d for d in devamsizlik if d.get("tur") == "mazeretli"])
        toplam_gun = sum(d.get("gun_sayisi", 0) or 0 for d in devamsizlik)

        styled_stat_row([
            ("Toplam Devamsızlık", len(devamsizlik), "#ef4444", "📋"),
            ("Mazeretsiz", mazeretsiz, "#dc2626", "🚫"),
            ("Mazeretli", mazeretli, "#f59e0b", "📄"),
            ("Toplam Gün", toplam_gun, "#8b5cf6", "📅"),
        ])
        st.markdown("<br>", unsafe_allow_html=True)

        if filtered_d:
            filtered_d.sort(key=lambda d: d.get("tarih", ""), reverse=True)
            df_d = pd.DataFrame([{
                "Personel": d.get("personel_adi", ""),
                "Tarih": d.get("tarih", ""),
                "Bitiş": d.get("bitis_tarihi", d.get("tarih", "")),
                "Gün": d.get("gun_sayisi", 1),
                "Tür": DEVAMSIZLIK_TURLERI.get(d.get("tur", ""), ""),
                "Gerekçe": d.get("gerekce", "-"),
                "Belge": "Var" if d.get("belge_var") else "Yok",
            } for d in filtered_d])
            st.dataframe(df_d, hide_index=True, use_container_width=True)

            # Detay
            styled_section("Devamsızlık Detayı", "#2563eb")
            det_l = [f"{d.get('personel_adi', '')} - {d.get('tarih', '')} ({DEVAMSIZLIK_TURLERI.get(d.get('tur', ''), '')})"
                     for d in filtered_d]
            det_i = st.selectbox("Kayıt Seç", range(len(det_l)), format_func=lambda i: det_l[i], key="ik_dev_det")
            sel_d = filtered_d[det_i]
            sd1, sd2 = st.columns(2)
            with sd1:
                st.write(f"**Personel:** {sel_d.get('personel_adi', '')}")
                st.write(f"**Tür:** {DEVAMSIZLIK_TURLERI.get(sel_d.get('tur', ''), '')}")
                st.write(f"**Tarih:** {sel_d.get('tarih', '')} → {sel_d.get('bitis_tarihi', sel_d.get('tarih', ''))}")
                st.write(f"**Gün Sayısı:** {sel_d.get('gun_sayisi', 1)}")
            with sd2:
                st.write(f"**Gerekçe:** {sel_d.get('gerekce', '-')}")
                st.write(f"**Belge Mevcut:** {'Evet' if sel_d.get('belge_var') else 'Hayır'}")
                st.write(f"**Kaynak:** {sel_d.get('kaynak', 'Manuel')}")
                st.write(f"**Not:** {sel_d.get('not', '-')}")
        else:
            styled_info_banner("Devamsızlık kaydı bulunamadı.", "info")

    # ── YENİ GİRİŞ ──
    with d_sub[1]:
        styled_section("Yeni Devamsızlık Girişi", "#10b981")

        secili_dev = _personel_selectbox("ik_dev_personel", "Personel Seçin")

        c1, c2 = st.columns(2)
        with c1:
            dev_tur = st.selectbox("Devamsızlık Türü *", list(DEVAMSIZLIK_TURLERI.keys()),
                                   format_func=lambda k: DEVAMSIZLIK_TURLERI[k], key="ik_dev_tur_yeni")
            dev_tarih = st.date_input("Başlangıç Tarihi *", key="ik_dev_tarih")
            dev_bitis = st.date_input("Bitiş Tarihi *", key="ik_dev_bitis")
        with c2:
            dev_gerekce = st.text_area("Gerekçe / Açıklama *", key="ik_dev_gerekce", height=80,
                                       placeholder="Devamsızlık sebebi detaylı yazılmalıdır")
            dev_belge = st.checkbox("Belge / Evrak mevcut mu?", key="ik_dev_belge")
            dev_not = st.text_input("Ek Not", key="ik_dev_not")

        if secili_dev and dev_bitis >= dev_tarih:
            gun = (dev_bitis - dev_tarih).days + 1
            renk = "#ef4444" if dev_tur == "mazeretsiz" else "#f59e0b"
            st.markdown(
                f'<div style="background:{renk}15;border-left:4px solid {renk};padding:10px 16px;'
                f'border-radius:0 8px 8px 0;margin:8px 0">'
                f'<strong>{DEVAMSIZLIK_TURLERI.get(dev_tur, "")}</strong> — {gun} gün</div>',
                unsafe_allow_html=True)

        if st.button("Devamsızlık Kaydet", type="primary", key="ik_dev_kaydet"):
            if not secili_dev:
                st.error("Personel seçin.")
            elif not dev_gerekce.strip():
                st.error("Gerekçe zorunludur.")
            elif dev_bitis < dev_tarih:
                st.error("Bitiş tarihi başlangıçtan önce olamaz.")
            else:
                gun = (dev_bitis - dev_tarih).days + 1
                yeni_dev = {
                    "id": _gen_local_id("dev"),
                    "personel_id": secili_dev.get("id", ""),
                    "personel_adi": f"{secili_dev.get('ad', '')} {secili_dev.get('soyad', '')}",
                    "tur": dev_tur,
                    "tarih": dev_tarih.isoformat(),
                    "bitis_tarihi": dev_bitis.isoformat(),
                    "gun_sayisi": gun,
                    "gerekce": dev_gerekce.strip(),
                    "belge_var": dev_belge,
                    "not": dev_not.strip(),
                    "kaynak": "Manuel",
                    "created_at": _now_str(),
                    "updated_at": _now_str(),
                }
                devamsizlik.append(yeni_dev)
                store.save_list("devamsizlik", devamsizlik)
                styled_info_banner(f"Devamsızlık kaydedildi — {DEVAMSIZLIK_TURLERI.get(dev_tur, '')} ({gun} gün).", "success")
                st.rerun()


# ============================================================
# GEÇ KALMA YÖNETİMİ
# ============================================================

def _render_gec_kalma(store: IKDataStore):
    """Geç kalma takibi — Manuel giriş + Kart okuma sistemi import."""
    gec_kalma = store.load_list("gec_kalma")

    g_sub = st.tabs(["📋 Geç Kalma Listesi", "✏️ Manuel Giriş", "💳 Kart Okuma Sistemi (İmport)"])

    # ── LİSTE ──
    with g_sub[0]:
        styled_section("Geç Kalma Kayıtları", "#f59e0b")

        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            gk_ay = st.selectbox("Ay", ["Tümü"] + [f"2026-{str(m).zfill(2)}" for m in range(1, 13)],
                                 key="ik_gk_ay")
        with gc2:
            gk_per = st.text_input("Personel Ara", key="ik_gk_per_ara")
        with gc3:
            gk_kaynak = st.selectbox("Kaynak", ["Tümü", "Manuel", "Kart Okuma"], key="ik_gk_kaynak")

        filtered_gk = gec_kalma
        if gk_ay != "Tümü":
            filtered_gk = [g for g in filtered_gk if g.get("tarih", "")[:7] == gk_ay]
        if gk_per:
            filtered_gk = [g for g in filtered_gk if gk_per.lower() in g.get("personel_adi", "").lower()]
        if gk_kaynak != "Tümü":
            filtered_gk = [g for g in filtered_gk if g.get("kaynak", "Manuel") == gk_kaynak]

        # Özet istatistikler
        toplam_gk = len(gec_kalma)
        toplam_dk = sum(g.get("gec_kalma_dk", 0) or 0 for g in gec_kalma)
        bu_ay = datetime.now().strftime("%Y-%m")
        bu_ay_gk = [g for g in gec_kalma if g.get("tarih", "")[:7] == bu_ay]
        farkli_personel = len(set(g.get("personel_id") for g in gec_kalma if g.get("personel_id")))

        styled_stat_row([
            ("Toplam Geç Kalma", toplam_gk, "#f59e0b", "⏰"),
            ("Toplam Süre", f"{toplam_dk} dk", "#ef4444", "⏱️"),
            ("Bu Ay", len(bu_ay_gk), "#8b5cf6", "📅"),
            ("Personel Sayısı", farkli_personel, "#2563eb", "👥"),
        ])
        st.markdown("<br>", unsafe_allow_html=True)

        if filtered_gk:
            filtered_gk.sort(key=lambda g: g.get("tarih", ""), reverse=True)
            df_gk = pd.DataFrame([{
                "Personel": g.get("personel_adi", ""),
                "Tarih": g.get("tarih", ""),
                "Mesai Başlangıç": g.get("mesai_baslangic", "08:30"),
                "Giriş Saati": g.get("giris_saati", ""),
                "Geç Kalma (dk)": g.get("gec_kalma_dk", 0),
                "Gerekçe": g.get("gerekce", "-"),
                "Kaynak": g.get("kaynak", "Manuel"),
            } for g in filtered_gk])
            st.dataframe(df_gk, hide_index=True, use_container_width=True)

            # Personel bazlı özet
            styled_section("Personel Bazlı Geç Kalma Özeti", "#2563eb")
            per_ozet: dict[str, dict] = {}
            for g in filtered_gk:
                pid = g.get("personel_adi", "Bilinmiyor")
                if pid not in per_ozet:
                    per_ozet[pid] = {"sayi": 0, "toplam_dk": 0}
                per_ozet[pid]["sayi"] += 1
                per_ozet[pid]["toplam_dk"] += g.get("gec_kalma_dk", 0) or 0

            ozet_rows = [{"Personel": k, "Geç Kalma Sayısı": v["sayi"],
                          "Toplam Süre (dk)": v["toplam_dk"],
                          "Ortalama (dk)": round(v["toplam_dk"] / v["sayi"], 1) if v["sayi"] > 0 else 0}
                         for k, v in sorted(per_ozet.items(), key=lambda x: x[1]["sayi"], reverse=True)]
            st.dataframe(pd.DataFrame(ozet_rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Geç kalma kaydı bulunamadı.", "info")

    # ── MANUEL GİRİŞ ──
    with g_sub[1]:
        styled_section("Manuel Geç Kalma Girişi", "#10b981")

        secili_gk = _personel_selectbox("ik_gk_personel", "Personel Seçin")

        c1, c2 = st.columns(2)
        with c1:
            gk_tarih = st.date_input("Tarih *", key="ik_gk_tarih")
            gk_mesai = st.time_input("Mesai Başlangıç Saati", value=datetime.strptime("08:30", "%H:%M").time(),
                                      key="ik_gk_mesai")
        with c2:
            gk_giris = st.time_input("Giriş Saati *", key="ik_gk_giris")
            gk_gerekce = st.text_area("Gerekçe / Açıklama", key="ik_gk_gerekce", height=80,
                                       placeholder="Geç kalma sebebi")

        if secili_gk and gk_giris > gk_mesai:
            mesai_dt = datetime.combine(gk_tarih, gk_mesai)
            giris_dt = datetime.combine(gk_tarih, gk_giris)
            fark_dk = int((giris_dt - mesai_dt).total_seconds() / 60)
            saat = fark_dk // 60
            dk = fark_dk % 60
            sure_str = f"{saat} saat {dk} dk" if saat > 0 else f"{dk} dakika"
            renk = "#ef4444" if fark_dk > 30 else "#f59e0b"
            st.markdown(
                f'<div style="background:{renk}15;border-left:4px solid {renk};padding:10px 16px;'
                f'border-radius:0 8px 8px 0;margin:8px 0">'
                f'<strong>Geç Kalma Süresi:</strong> {sure_str} ({fark_dk} dakika)</div>',
                unsafe_allow_html=True)

        if st.button("Geç Kalma Kaydet", type="primary", key="ik_gk_kaydet"):
            if not secili_gk:
                st.error("Personel seçin.")
            elif gk_giris <= gk_mesai:
                st.error("Giriş saati mesai başlangıcından sonra olmalıdır.")
            else:
                mesai_dt = datetime.combine(gk_tarih, gk_mesai)
                giris_dt = datetime.combine(gk_tarih, gk_giris)
                fark_dk = int((giris_dt - mesai_dt).total_seconds() / 60)
                yeni_gk = {
                    "id": _gen_local_id("gk"),
                    "personel_id": secili_gk.get("id", ""),
                    "personel_adi": f"{secili_gk.get('ad', '')} {secili_gk.get('soyad', '')}",
                    "tarih": gk_tarih.isoformat(),
                    "mesai_baslangic": gk_mesai.strftime("%H:%M"),
                    "giris_saati": gk_giris.strftime("%H:%M"),
                    "gec_kalma_dk": fark_dk,
                    "gerekce": gk_gerekce.strip(),
                    "kaynak": "Manuel",
                    "created_at": _now_str(),
                    "updated_at": _now_str(),
                }
                gec_kalma.append(yeni_gk)
                store.save_list("gec_kalma", gec_kalma)
                styled_info_banner(f"Geç kalma kaydedildi — {fark_dk} dakika.", "success")
                st.rerun()

    # ── KART OKUMA SİSTEMİ İMPORT ──
    with g_sub[2]:
        styled_section("Kart Okuma Sistemi Veri Aktarımı", "#8b5cf6")

        st.markdown("""
        **Kart okuma sisteminizden gelen verileri CSV dosyası olarak yükleyin.**

        CSV dosyası aşağıdaki sütunları içermelidir:
        - `personel_adi` veya `ad_soyad` — Personel adı soyadı
        - `tarih` — Giriş tarihi (YYYY-MM-DD)
        - `giris_saati` — Kart okutma saati (HH:MM)
        - `mesai_baslangic` — (opsiyonel, varsayılan: 08:30)
        """)

        mesai_default = st.time_input("Varsayılan Mesai Başlangıç Saati",
                                       value=datetime.strptime("08:30", "%H:%M").time(),
                                       key="ik_gk_import_mesai")

        uploaded = st.file_uploader("CSV Dosyası Yükle", type=["csv"], key="ik_gk_import_csv")

        if uploaded:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded, allowed_types=["csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded = None
        if uploaded:
            try:
                csv_text = uploaded.getvalue().decode("utf-8")
                reader = csv.DictReader(io.StringIO(csv_text))
                rows = list(reader)

                if not rows:
                    st.warning("Dosya boş.")
                else:
                    st.info(f"**{len(rows)} satır** okundu. Önizleme:")
                    preview_df = pd.DataFrame(rows[:10])
                    st.dataframe(preview_df, hide_index=True, use_container_width=True)

                    # Personel eşleştirme
                    staff = _get_personel_options()
                    staff_map = {}
                    for s in staff:
                        full = f"{s.get('ad', '')} {s.get('soyad', '')}".strip().lower()
                        staff_map[full] = s

                    eslesen = 0
                    gec_kalanlar = []
                    for row in rows:
                        ad = (row.get("personel_adi") or row.get("ad_soyad") or "").strip()
                        tarih = row.get("tarih", "").strip()
                        giris = row.get("giris_saati", "").strip()
                        mesai_str = row.get("mesai_baslangic", "").strip() or mesai_default.strftime("%H:%M")

                        if not ad or not tarih or not giris:
                            continue

                        try:
                            giris_t = datetime.strptime(giris, "%H:%M").time()
                            mesai_t = datetime.strptime(mesai_str, "%H:%M").time()
                        except ValueError:
                            continue

                        if giris_t <= mesai_t:
                            continue

                        tarih_dt = datetime.strptime(tarih, "%Y-%m-%d").date()
                        fark = int((datetime.combine(tarih_dt, giris_t) -
                                    datetime.combine(tarih_dt, mesai_t)).total_seconds() / 60)

                        personel = staff_map.get(ad.lower(), {})
                        eslesen += 1 if personel else 0

                        gec_kalanlar.append({
                            "id": _gen_local_id("gk"),
                            "personel_id": personel.get("id", ""),
                            "personel_adi": ad,
                            "tarih": tarih,
                            "mesai_baslangic": mesai_str,
                            "giris_saati": giris,
                            "gec_kalma_dk": fark,
                            "gerekce": "Kart okuma sistemi",
                            "kaynak": "Kart Okuma",
                            "created_at": _now_str(),
                            "updated_at": _now_str(),
                        })

                    if gec_kalanlar:
                        st.warning(f"**{len(gec_kalanlar)}** geç kalma tespit edildi. ({eslesen} personel eşleşti)")

                        if st.button(f"{len(gec_kalanlar)} Kaydı İçe Aktar", type="primary", key="ik_gk_import_btn"):
                            gec_kalma.extend(gec_kalanlar)
                            store.save_list("gec_kalma", gec_kalma)
                            styled_info_banner(f"{len(gec_kalanlar)} geç kalma kaydı aktarıldı.", "success")
                            st.rerun()
                    else:
                        styled_info_banner("Geç kalma tespit edilmedi — tüm girişler mesai saatinde.", "success")
            except Exception as e:
                st.error(f"Dosya okuma hatası: {e}")


# ============================================================
# PERFORMANS ALT RAPORU
# ============================================================

def _render_performans_alt_raporu(store: IKDataStore):
    """İzin, rapor, devamsızlık ve geç kalma verilerini birleştiren performans alt raporu."""
    styled_section("Performans Alt Raporu", "#1e40af")

    izinler = store.load_list("izinler")
    raporlar = store.load_list("raporlar")
    devamsizlik = store.load_list("devamsizlik")
    gec_kalma = store.load_list("gec_kalma")
    employees = store.load_list("employees")
    aktif_emp = [e for e in employees if e.get("status") == "Aktif"]

    if not aktif_emp:
        styled_info_banner("Aktif çalışan bulunamadı.", "info")
        return

    # Dönem filtresi
    ay_sec = st.selectbox("Dönem", ["Tümü"] + [f"2026-{str(m).zfill(2)}" for m in range(1, 13)],
                          key="ik_prf_alt_ay")

    # Personel bazlı rapor tablosu
    rapor_rows = []
    for emp in aktif_emp:
        eid = emp.get("id", "")
        ad = f"{emp.get('ad', '')} {emp.get('soyad', '')}".strip()
        ad_lower = ad.lower()

        # Filtreleme
        def _ay_filtre(records, date_field="tarih"):
            if ay_sec == "Tümü":
                return records
            return [r for r in records if r.get(date_field, "")[:7] == ay_sec]

        p_izin = _ay_filtre([i for i in izinler if i.get("personel_id") == eid and i.get("durum") == "onaylandi"],
                            "baslangic")
        p_rapor = _ay_filtre([r for r in raporlar if r.get("personel_id") == eid], "baslangic_tarihi")
        p_devam = _ay_filtre([d for d in devamsizlik if d.get("personel_id") == eid])
        p_gk = _ay_filtre([g for g in gec_kalma if g.get("personel_id") == eid or
                            g.get("personel_adi", "").lower() == ad_lower])

        izin_gun = sum(i.get("gun_sayisi", 0) or 0 for i in p_izin)
        rapor_gun = sum(r.get("gun_sayisi", 0) or 0 for r in p_rapor)
        mazeretsiz = len([d for d in p_devam if d.get("tur") == "mazeretsiz"])
        mazeretsiz_gun = sum(d.get("gun_sayisi", 0) or 0 for d in p_devam if d.get("tur") == "mazeretsiz")
        gk_sayi = len(p_gk)
        gk_dk = sum(g.get("gec_kalma_dk", 0) or 0 for g in p_gk)

        # Performans puanı hesaplama (100 üzerinden, eksilmeli)
        puan = 100
        puan -= mazeretsiz_gun * 10  # Mazeretsiz devamsızlık: gün başına -10
        puan -= gk_sayi * 2          # Geç kalma: olay başına -2
        puan -= min(gk_dk // 60, 10) * 3  # Her 60 dk geç kalma: -3 (max -30)
        puan = max(0, min(100, puan))

        # Renk bandı
        if puan >= 90:
            band = "Mükemmel"
            band_renk = "#10b981"
        elif puan >= 75:
            band = "İyi"
            band_renk = "#2563eb"
        elif puan >= 60:
            band = "Orta"
            band_renk = "#f59e0b"
        elif puan >= 40:
            band = "Düşük"
            band_renk = "#ef4444"
        else:
            band = "Kritik"
            band_renk = "#dc2626"

        rapor_rows.append({
            "Personel": ad,
            "Pozisyon": emp.get("position_name", ""),
            "İzin (gün)": izin_gun,
            "Rapor (gün)": rapor_gun,
            "Mazeretsiz Dev.": mazeretsiz_gun,
            "Geç Kalma": gk_sayi,
            "Geç Kalma (dk)": gk_dk,
            "Puan": puan,
            "Değerlendirme": band,
            "_renk": band_renk,
        })

    # Sıralama
    rapor_rows.sort(key=lambda r: r["Puan"])

    # Genel özet
    toplam_kisi = len(rapor_rows)
    mukemmel = len([r for r in rapor_rows if r["Puan"] >= 90])
    dusuk = len([r for r in rapor_rows if r["Puan"] < 60])
    ort_puan = round(sum(r["Puan"] for r in rapor_rows) / toplam_kisi, 1) if toplam_kisi > 0 else 0

    styled_stat_row([
        ("Personel", toplam_kisi, "#2563eb", "👥"),
        ("Ortalama Puan", ort_puan, "#8b5cf6", "📊"),
        ("Mükemmel (90+)", mukemmel, "#10b981", "🌟"),
        ("Düşük (<60)", dusuk, "#ef4444", "⚠️"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)

    # Tablo
    if rapor_rows:
        display_rows = [{k: v for k, v in r.items() if k != "_renk"} for r in rapor_rows]
        df_perf = pd.DataFrame(display_rows)
        st.dataframe(df_perf, hide_index=True, use_container_width=True)

        # Detay kartları — en düşük puanlı personeller
        dusuk_per = [r for r in rapor_rows if r["Puan"] < 75]
        if dusuk_per:
            styled_section("Dikkat Gerektiren Personel", "#ef4444")
            for r in dusuk_per[:10]:
                renk = r["_renk"]
                st.markdown(
                    f'<div style="background:{renk}10;border-left:4px solid {renk};'
                    f'border-radius:0 10px 10px 0;padding:12px 16px;margin:6px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<div><strong style="color:#94A3B8">{r["Personel"]}</strong>'
                    f'<span style="color:#64748b;margin-left:8px;font-size:0.85rem">{r["Pozisyon"]}</span></div>'
                    f'<div style="font-size:1.3rem;font-weight:800;color:{renk}">{r["Puan"]}/100</div></div>'
                    f'<div style="font-size:0.8rem;color:#475569;margin-top:4px">'
                    f'Mazeretsiz: {r["Mazeretsiz Dev."]} gün | Geç Kalma: {r["Geç Kalma"]}x ({r["Geç Kalma (dk)"]} dk) | '
                    f'İzin: {r["İzin (gün)"]} gün | Rapor: {r["Rapor (gün)"]} gün</div>'
                    f'</div>',
                    unsafe_allow_html=True)

        # PDF Export
        styled_section("PDF Rapor", "#10b981")
        if st.button("Performans Alt Raporu PDF", type="primary", key="ik_prf_alt_pdf"):
            pdf_bytes = _generate_performans_alt_raporu_pdf(rapor_rows, ay_sec)
            if pdf_bytes:
                st.download_button(
                    "PDF Kaydet",
                    data=pdf_bytes,
                    file_name=f"performans_alt_raporu_{ay_sec or 'tumu'}.pdf",
                    mime="application/pdf",
                    key="ik_prf_alt_pdf_dl",
                )
    else:
        styled_info_banner("Veri bulunamadı.", "info")


def _generate_performans_alt_raporu_pdf(rapor_rows: list[dict], donem: str) -> bytes | None:
    """Performans Alt Raporu PDF."""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas as pdf_canvas
        from reportlab.lib.colors import HexColor
        from utils.shared_data import ensure_turkish_pdf_fonts

        font_name, font_bold = ensure_turkish_pdf_fonts()
        buf = io.BytesIO()
        w, h = landscape(A4)
        c = pdf_canvas.Canvas(buf, pagesize=landscape(A4))
        margin = 1.5 * cm
        y = h - margin

        NAVY = HexColor("#0B0F19")
        WHITE = HexColor("#ffffff")
        GRAY = HexColor("#64748b")
        DARK = HexColor("#94A3B8")
        page_num = [1]

        def _footer():
            c.setFont(font_name, 7)
            c.setFillColor(GRAY)
            c.drawString(margin, 0.8 * cm, f"Performans Alt Raporu — {donem or 'Tüm Dönem'}")
            c.drawRightString(w - margin, 0.8 * cm, f"Sayfa {page_num[0]} | {datetime.now().strftime('%d.%m.%Y')}")

        def _new_page():
            _footer()
            c.showPage()
            page_num[0] += 1
            return h - margin

        # Header
        c.setFillColor(NAVY)
        c.roundRect(margin, y - 1.6 * cm, w - 2 * margin, 1.8 * cm, 5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(font_bold, 14)
        c.drawString(margin + 0.5 * cm, y - 0.6 * cm, "PERFORMANS ALT RAPORU — IZIN / RAPOR / DEVAMSIZLIK / GEC KALMA")
        c.setFont(font_name, 9)
        c.drawString(margin + 0.5 * cm, y - 1.2 * cm, f"Dönem: {donem or 'Tüm Dönem'} | Oluşturma: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        y -= 2.5 * cm

        # Tablo başlığı
        cols = ["Personel", "Pozisyon", "İzin", "Rapor", "Maz.Dev.", "G.Kalma", "G.K.(dk)", "Puan", "Değer."]
        col_widths = [5.5 * cm, 4 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2.5 * cm, 2 * cm, 3 * cm]
        x_start = margin

        c.setFillColor(HexColor("#2563eb"))
        c.roundRect(x_start, y - 0.5 * cm, sum(col_widths), 0.7 * cm, 3, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(font_bold, 7.5)
        x = x_start + 0.2 * cm
        for i, col_name in enumerate(cols):
            c.drawString(x, y - 0.3 * cm, col_name)
            x += col_widths[i]
        y -= 0.9 * cm

        # Satırlar
        for row_idx, r in enumerate(rapor_rows):
            if y < 2 * cm:
                y = _new_page()
                # Tekrar başlık
                c.setFillColor(HexColor("#2563eb"))
                c.roundRect(x_start, y - 0.5 * cm, sum(col_widths), 0.7 * cm, 3, fill=1, stroke=0)
                c.setFillColor(WHITE)
                c.setFont(font_bold, 7.5)
                x = x_start + 0.2 * cm
                for i, col_name in enumerate(cols):
                    c.drawString(x, y - 0.3 * cm, col_name)
                    x += col_widths[i]
                y -= 0.9 * cm

            # Satır arka plan
            if row_idx % 2 == 0:
                c.setFillColor(HexColor("#111827"))
                c.rect(x_start, y - 0.4 * cm, sum(col_widths), 0.6 * cm, fill=1, stroke=0)

            c.setFont(font_name, 7)
            c.setFillColor(DARK)
            x = x_start + 0.2 * cm
            vals = [
                r.get("Personel", "")[:30],
                r.get("Pozisyon", "")[:22],
                str(r.get("İzin (gün)", 0)),
                str(r.get("Rapor (gün)", 0)),
                str(r.get("Mazeretsiz Dev.", 0)),
                str(r.get("Geç Kalma", 0)),
                str(r.get("Geç Kalma (dk)", 0)),
                str(r.get("Puan", 0)),
                r.get("Değerlendirme", ""),
            ]
            for i, val in enumerate(vals):
                if i == 7:  # Puan - renkli
                    renk = r.get("_renk", "#94A3B8")
                    c.setFillColor(HexColor(renk))
                    c.setFont(font_bold, 7.5)
                    c.drawString(x, y - 0.2 * cm, val)
                    c.setFont(font_name, 7)
                    c.setFillColor(DARK)
                elif i == 8:  # Değerlendirme - renkli
                    renk = r.get("_renk", "#94A3B8")
                    c.setFillColor(HexColor(renk))
                    c.setFont(font_bold, 7)
                    c.drawString(x, y - 0.2 * cm, val)
                    c.setFont(font_name, 7)
                    c.setFillColor(DARK)
                else:
                    c.drawString(x, y - 0.2 * cm, val)
                x += col_widths[i]
            y -= 0.55 * cm

        _footer()
        c.save()
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"PDF oluşturma hatası: {e}")
        return None


# ============================================================
# SEKME 7: MAAS & BORDRO
# ============================================================

def _render_maas_bordro(store: IKDataStore):
    bordrolar = store.load_list("maas_bordro")
    sub = st.tabs(["📋 Bordro Listesi", "➕ Yeni Bordro", "📜 Bordro Geçmişi"])

    with sub[0]:
        styled_section("Aylık Bordro Listesi", "#10b981")
        donem = st.selectbox("Donem", [f"2026-{str(m).zfill(2)}" for m in range(1, 13)],
                             index=datetime.now().month - 1, key="ik_brd_donem")
        d_brd = [b for b in bordrolar if b.get("donem") == donem]
        if d_brd:
            t_brut = sum(b.get("brut_maas", 0) for b in d_brd)
            t_net = sum(b.get("net_maas", 0) for b in d_brd)
            styled_stat_row([
                ("Toplam Brut", f"{t_brut:,.0f} TL", "#2563eb", "\U0001f4b0"),
                ("Toplam Net", f"{t_net:,.0f} TL", "#10b981", "\U0001f4b5"),
                ("Personel", len(d_brd), "#8b5cf6", "\U0001f465"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)
            df = pd.DataFrame([{
                "Personel": b.get("personel_adi", ""),
                "Brüt": f"{b.get('brut_maas', 0):,.2f}",
                "Net": f"{b.get('net_maas', 0):,.2f}",
                "Ek Ödeme": f"{b.get('ek_odemeler', 0):,.2f}",
                "Kesinti": f"{b.get('kesintiler', 0):,.2f}",
                "Ek Dosya": "Var" if b.get("bordro_eki") else "-",
            } for b in d_brd])
            st.dataframe(df, hide_index=True, use_container_width=True)

            # Bordro eki indirme
            ekli_bordrolar = [b for b in d_brd if b.get("bordro_eki")]
            if ekli_bordrolar:
                styled_section("Bordro Eki İndir", "#8b5cf6")
                ek_labels = [f"{b.get('personel_adi', '')} — {b.get('bordro_eki', '')}" for b in ekli_bordrolar]
                ek_idx = st.selectbox("Dosya Seç", range(len(ek_labels)),
                                      format_func=lambda i: ek_labels[i], key="ik_brd_ek_indir_sec")
                ek_file = ekli_bordrolar[ek_idx].get("bordro_eki", "")
                ek_path = os.path.join(store.base_path, "bordro_ekleri", ek_file)
                if os.path.exists(ek_path):
                    with open(ek_path, "rb") as ef:
                        st.download_button("Dosyayı İndir", data=ef.read(),
                                           file_name=ek_file, key="ik_brd_ek_dl")
                else:
                    st.caption("Dosya bulunamadı.")
        else:
            styled_info_banner(f"{donem} için bordro yok.", "info")

    with sub[1]:
        styled_section("Yeni Bordro Oluştur", "#2563eb")
        secili = _personel_selectbox("ik_brd_personel", "Personel Secin")
        c1, c2 = st.columns(2)
        with c1:
            brd_donem = st.selectbox("Donem", [f"2026-{str(m).zfill(2)}" for m in range(1, 13)], key="ik_brd_yeni_donem")
            brut = st.number_input("Brüt Maaş (TL)", min_value=0.0, step=100.0, key="ik_brut")
            net_input = st.number_input("Net Maaş (TL)", min_value=0.0, step=100.0, key="ik_net",
                                         help="Boş bırakılırsa brütten otomatik hesaplanır")
            ek_odeme = st.number_input("Ek Ödemeler (TL)", min_value=0.0, step=50.0, key="ik_ek")
        with c2:
            kesinti = st.number_input("Kesintiler (TL)", min_value=0.0, step=50.0, key="ik_kesinti")
            st.markdown("<br>", unsafe_allow_html=True)
            bordro_ek = st.file_uploader("Bordro Eki (PDF / Görsel)",
                                          type=["pdf", "png", "jpg", "jpeg"],
                                          key="ik_brd_ek",
                                          help="Bordro belgesini yükleyin")
            if bordro_ek is not None:
                from utils.security import validate_upload
                _ok, _msg = validate_upload(bordro_ek, allowed_types=["pdf", "png", "jpg", "jpeg"], max_mb=50)
                if not _ok:
                    st.error(f"⚠️ {_msg}")
                    bordro_ek = None

        if brut > 0:
            sgk_isci = brut * 0.14
            sgk_isveren = brut * 0.205
            gelir_v = (brut - sgk_isci) * 0.15
            damga_v = brut * 0.00759
            hesaplanan_net = brut - sgk_isci - gelir_v - damga_v + ek_odeme - kesinti
            net = net_input if net_input > 0 else hesaplanan_net

            if net_input > 0:
                st.info(f"Net Maaş (girilen): **{net_input:,.2f} TL** | Hesaplanan: {hesaplanan_net:,.2f} TL")
            else:
                st.info(f"Net Maaş (hesaplanan): **{hesaplanan_net:,.2f} TL**")

            if st.button("Bordroyu Kaydet", type="primary", key="ik_brd_kaydet"):
                if not secili:
                    st.error("Personel seçin.")
                else:
                    # Bordro eki kaydet
                    ek_dosya_adi = ""
                    if bordro_ek is not None:
                        ek_dir = os.path.join(store.base_path, "bordro_ekleri")
                        os.makedirs(ek_dir, exist_ok=True)
                        ek_dosya_adi = f"{brd_donem}_{secili.get('id', '')}_{bordro_ek.name}"
                        ek_path = os.path.join(ek_dir, ek_dosya_adi)
                        with open(ek_path, "wb") as f:
                            f.write(bordro_ek.getbuffer())

                    yeni = {
                        "id": _gen_local_id("brd"),
                        "personel_id": secili.get("id", ""),
                        "personel_adi": f"{secili.get('ad', '')} {secili.get('soyad', '')}",
                        "donem": brd_donem, "brut_maas": brut,
                        "sgk_isci": round(sgk_isci, 2), "sgk_isveren": round(sgk_isveren, 2),
                        "gelir_vergisi": round(gelir_v, 2), "damga_vergisi": round(damga_v, 2),
                        "ek_odemeler": ek_odeme, "kesintiler": kesinti,
                        "net_maas": round(net, 2),
                        "bordro_eki": ek_dosya_adi,
                        "created_at": _now_str(),
                    }
                    bordrolar.append(yeni)
                    store.save_list("maas_bordro", bordrolar)
                    msg = "Bordro kaydedildi."
                    if ek_dosya_adi:
                        msg += f" Ek dosya: {bordro_ek.name}"
                    styled_info_banner(msg, "success")
                    st.rerun()

    with sub[2]:
        styled_section("Bordro Geçmişi", "#8b5cf6")
        secili = _personel_selectbox("ik_brd_gecmis_per", "Personel Secin")
        if secili:
            kisi = sorted([b for b in bordrolar if b.get("personel_id") == secili.get("id", "")],
                          key=lambda x: x.get("donem", ""), reverse=True)
            if kisi:
                df = pd.DataFrame([{
                    "Donem": b.get("donem", ""), "Brut": f"{b.get('brut_maas',0):,.2f}",
                    "Net": f"{b.get('net_maas',0):,.2f}",
                } for b in kisi])
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                styled_info_banner("Bordro kaydi yok.", "info")


# ============================================================
# SEKME 8: EGITIM & SERTIFIKA
# ============================================================

def _render_egitim_sertifika(store: IKDataStore):
    egitimler = store.load_list("egitimler")
    sub = st.tabs(["📋 Eğitim Kayıtları", "➕ Yeni Eğitim", "🏅 Sertifika Takibi"])

    with sub[0]:
        styled_section("Eğitim Kayıtları", "#0d9488")
        tur_f = st.selectbox("Tur", ["Tümü"] + list(EGITIM_TURLERI.values()), key="ik_egt_tur")
        filtered = egitimler
        if tur_f != "Tümü":
            t_key = next((k for k, v in EGITIM_TURLERI.items() if v == tur_f), None)
            if t_key:
                filtered = [e for e in filtered if e.get("egitim_turu") == t_key]
        if filtered:
            df = pd.DataFrame([{
                "Personel": e.get("personel_adi", ""),
                "Egitim": e.get("egitim_adi", ""),
                "Tur": EGITIM_TURLERI.get(e.get("egitim_turu", ""), ""),
                "Tarih": e.get("tarih", ""),
                "Saat": e.get("sure_saat", 0),
            } for e in filtered])
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Egitim kaydi yok.", "info")

    with sub[1]:
        styled_section("Yeni Eğitim Kaydi", "#10b981")
        secili = _personel_selectbox("ik_egt_personel", "Personel Secin")
        c1, c2 = st.columns(2)
        with c1:
            egt_adi = st.text_input("Egitim Adi", key="ik_egt_adi")
            egt_turu = st.selectbox("Tur", list(EGITIM_TURLERI.keys()),
                                    format_func=lambda k: EGITIM_TURLERI[k], key="ik_egt_turu")
            kurum = st.text_input("Kurum", key="ik_egt_kurum")
        with c2:
            tarih = st.date_input("Tarih", key="ik_egt_tarih")
            sure = st.number_input("Sure (Saat)", min_value=1, value=8, key="ik_egt_sure")
            sert_no = st.text_input("Sertifika No", key="ik_egt_sert_no")
            gecerlilik = st.date_input("Gecerlilik Bitis (varsa)", key="ik_egt_gecerlilik", value=None)

        if st.button("Egitim Kaydet", type="primary", key="ik_egt_kaydet"):
            if not secili or not egt_adi:
                st.error("Personel ve egitim adi zorunlu.")
            else:
                yeni = {
                    "id": _gen_local_id("egt"),
                    "personel_id": secili.get("id", ""),
                    "personel_adi": f"{secili.get('ad', '')} {secili.get('soyad', '')}",
                    "egitim_adi": egt_adi, "egitim_turu": egt_turu, "kurum": kurum,
                    "tarih": tarih.isoformat(), "sure_saat": sure,
                    "sertifika_no": sert_no,
                    "gecerlilik_bitis": gecerlilik.isoformat() if gecerlilik else "",
                    "created_at": _now_str(),
                }
                egitimler.append(yeni)
                store.save_list("egitimler", egitimler)
                styled_info_banner("Egitim kaydi oluşturuldu.", "success")
                st.rerun()

    with sub[2]:
        styled_section("Sertifika Takibi", "#f59e0b")
        sertifikali = [e for e in egitimler if e.get("gecerlilik_bitis")]
        if sertifikali:
            bugun = date.today()
            rows = []
            for e in sertifikali:
                try:
                    g = datetime.strptime(e["gecerlilik_bitis"], "%Y-%m-%d").date()
                    kalan = (g - bugun).days
                    durum = "Gecerli" if kalan > 30 else ("Yakinda Dolacak" if kalan > 0 else "Suresi Dolmus")
                except Exception:
                    kalan, durum = 0, "Bilinmiyor"
                rows.append({"Personel": e.get("personel_adi",""), "Sertifika": e.get("egitim_adi",""),
                             "Bitis": e.get("gecerlilik_bitis",""), "Kalan Gün": kalan, "Durum": durum})
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Sertifika kaydi yok.", "info")


# ============================================================
# SEKME 9: DISIPLIN
# ============================================================

def _render_disiplin(store: IKDataStore):
    disiplinler = store.load_list("disiplin")
    sub = st.tabs(["📋 Disiplin Kayıtları", "➕ Yeni Kayıt"])

    with sub[0]:
        styled_section("Disiplin Kayıtları", "#ef4444")
        if disiplinler:
            df = pd.DataFrame([{
                "Personel": d.get("personel_adi", ""),
                "Tarih": d.get("tarih", ""),
                "İşlem": DISIPLIN_ISLEM_TURLERI.get(d.get("islem_turu", ""), ""),
                "Açıklama": d.get("olay_aciklamasi", ""),
            } for d in disiplinler])
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Disiplin kaydi yok.", "info")

    with sub[1]:
        styled_section("Yeni Disiplin Kaydi", "#dc2626")
        secili = _personel_selectbox("ik_dis_personel", "Personel Secin")
        c1, c2 = st.columns(2)
        with c1:
            tarih = st.date_input("Tarih", key="ik_dis_tarih")
            islem_turu = st.selectbox("İşlem Turu", list(DISIPLIN_ISLEM_TURLERI.keys()),
                                      format_func=lambda k: DISIPLIN_ISLEM_TURLERI[k], key="ik_dis_tur")
        with c2:
            olay = st.text_area("Olay Açıklaması", key="ik_dis_olay", height=100)
            notlar = st.text_area("Notlar", key="ik_dis_notlar", height=80)

        if st.button("Kaydi Oluştur", type="primary", key="ik_dis_kaydet"):
            if not secili or not olay:
                st.error("Personel ve olay aciklamasi zorunlu.")
            else:
                yeni = {
                    "id": _gen_local_id("dis"),
                    "personel_id": secili.get("id", ""),
                    "personel_adi": f"{secili.get('ad', '')} {secili.get('soyad', '')}",
                    "tarih": tarih.isoformat(), "olay_aciklamasi": olay,
                    "islem_turu": islem_turu, "notlar": notlar, "created_at": _now_str(),
                }
                disiplinler.append(yeni)
                store.save_list("disiplin", disiplinler)
                styled_info_banner("Disiplin kaydi oluşturuldu.", "success")
                st.rerun()


# ============================================================
# SEKME: KURUM AKTIF CALISANLARI
# ============================================================

def _calc_kidem_str(ise_baslama: str) -> str:
    if not ise_baslama:
        return "-"
    try:
        start = datetime.strptime(ise_baslama, "%Y-%m-%d").date()
        delta = (date.today() - start).days
        yil = delta // 365
        ay = (delta % 365) // 30
        if yil:
            return f"{yil} yil {ay} ay"
        if ay:
            return f"{ay} ay"
        return f"{delta} gun"
    except Exception:
        return "-"


def _render_aktif_calisanlar(store: IKDataStore):
    sub_tabs = st.tabs(["👥 Aktif Çalışanlar", "🚪 İşten Ayrılanlar", "📥 Excel/PDF Import"])

    employees = store.load_objects("employees")

    # ===== AKTIF CALISANLAR =====
    with sub_tabs[0]:
        styled_section("Kurum Aktif Çalışanları", "#059669")

        aktif = [e for e in employees if e.status == "Aktif"]
        ayrilanlar = [e for e in employees if e.status == "Ayrildi"]

        if not aktif:
            styled_info_banner("Henuz aktif calisan bulunmuyor. Ise alinanlar sekmesinden evraklari tamamlayin.", "warning")
        else:
            # Istatistikler
            role_counts = {}
            for e in aktif:
                rs = e.role_scope or "ALL"
                role_counts[rs] = role_counts.get(rs, 0) + 1

            styled_stat_row([
                ("Toplam Aktif", len(aktif), "#10b981", "\U0001f465"),
                ("Öğretmen", role_counts.get("TEACHER", 0), "#2563eb", "\U0001f468\u200d\U0001f3eb"),
                ("Yönetim", role_counts.get("MANAGEMENT", 0), "#8b5cf6", "\U0001f4bc"),
                ("Isten Ayrilan", len(ayrilanlar), "#ef4444", "\U0001f6aa"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            # Filtreleme
            c1, c2, c3 = st.columns(3)
            with c1:
                arama = st.text_input("Ad/Soyad Ara", key="ik_ac_ara")
            with c2:
                rs_list = ["Tümü"] + sorted(set(e.role_scope for e in aktif if e.role_scope))
                rs_filtre = st.selectbox("Rol", rs_list, key="ik_ac_rol")
            with c3:
                kampus_list = ["Tümü"] + sorted(set(e.kampus for e in aktif if e.kampus))
                kampus_filtre = st.selectbox("Kampus", kampus_list, key="ik_ac_kampus")

            filtered = aktif
            if arama:
                arama_l = arama.lower()
                filtered = [e for e in filtered if arama_l in e.tam_ad.lower()]
            if rs_filtre != "Tümü":
                filtered = [e for e in filtered if e.role_scope == rs_filtre]
            if kampus_filtre != "Tümü":
                filtered = [e for e in filtered if e.kampus == kampus_filtre]

            styled_section(f"Çalışan Listesi ({len(filtered)} kisi)", "#1e40af")
            rows = []
            for e in filtered:
                rows.append({
                    "Çalışan Kodu": e.employee_code,
                    "Ad Soyad": e.tam_ad,
                    "Pozisyon": e.position_name or e.position_code or "-",
                    "Rol": e.role_scope,
                    "Kampus": e.kampus or "-",
                    "Kademe": e.kademe or "-",
                    "Ise Baslama": e.ise_baslama_tarihi or "-",
                    "Kidem": _calc_kidem_str(e.ise_baslama_tarihi),
                    "Telefon": e.telefon or "-",
                    "Email": e.email or "-",
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True, use_container_width=True)

            # Calisan Detay
            if filtered:
                styled_section("Çalışan Detay & İşlemler", "#8b5cf6")
                det_labels = [f"{e.employee_code} - {e.tam_ad}" for e in filtered]
                det_idx = st.selectbox("Çalışan secin", range(len(det_labels)),
                                        format_func=lambda i: det_labels[i], key="ik_ac_det")
                det_emp = filtered[det_idx]

                # Bilgi karti
                st.markdown(f"""<div style="background:linear-gradient(135deg,#0B0F19 0%,#e2e8f0 100%);
                border-radius:14px;padding:20px;margin:10px 0;border-left:5px solid #059669;">
                <div style="font-weight:800;font-size:1.2rem;color:#94A3B8;">{det_emp.tam_ad}</div>
                <div style="font-size:0.85rem;color:#64748b;margin-top:2px;">
                {det_emp.employee_code} | {det_emp.position_name or det_emp.position_code or '-'} | {det_emp.role_scope}
                </div></div>""", unsafe_allow_html=True)

                # Detay - 3 sutun
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**Kisisel Bilgiler**")
                    st.write(f"**TC No:** {det_emp.tc_no or '-'}")
                    st.write(f"**Telefon:** {det_emp.telefon or '-'}")
                    st.write(f"**Email:** {det_emp.email or '-'}")
                with c2:
                    st.markdown("**Görev Bilgileri**")
                    st.write(f"**Pozisyon:** {det_emp.position_name or det_emp.position_code or '-'}")
                    st.write(f"**Rol:** {det_emp.role_scope}")
                    st.write(f"**Kampus:** {det_emp.kampus or '-'}")
                    st.write(f"**Kademe:** {det_emp.kademe or '-'}")
                with c3:
                    st.markdown("**Calisma Bilgileri**")
                    st.write(f"**Ise Baslama:** {det_emp.ise_baslama_tarihi or '-'}")
                    st.write(f"**Kidem:** {_calc_kidem_str(det_emp.ise_baslama_tarihi)}")
                    st.write(f"**Durum:** {det_emp.status}")
                    st.write(f"**Çalışan Kodu:** {det_emp.employee_code}")

                # Ise alim evraklari
                evrak_data = store.load_list("ise_alim_evraklari")
                emp_evrak = next((e for e in evrak_data if e.get("candidate_id") == det_emp.candidate_id), None)
                if emp_evrak:
                    styled_section("Ise Alim Evraklari", "#059669")
                    evraklar = emp_evrak.get("evraklar", {})
                    evrak_html = ""
                    for key, label in ISE_ALIM_EVRAKLARI:
                        durum = evraklar.get(key, False)
                        icon = "\u2705" if durum else "\u274c"
                        renk = "#10b981" if durum else "#ef4444"
                        evrak_html += (
                            f'<div style="display:inline-flex;align-items:center;gap:6px;margin:4px 12px;">'
                            f'<span>{icon}</span>'
                            f'<span style="font-size:0.85rem;color:{renk};font-weight:600;">{label}</span></div>'
                        )
                    st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin:4px 0;">{evrak_html}</div>',
                                unsafe_allow_html=True)

                # Mulakat bilgileri
                all_interviews = store.load_objects("interviews")
                cand_intvs = [iv for iv in all_interviews if iv.candidate_id == det_emp.candidate_id]
                if cand_intvs:
                    styled_section("Mülakat Geçmişi", "#2563eb")
                    for iv in sorted(cand_intvs, key=lambda x: x.stage):
                        k_icon = {"Ise Alindi": "\u2705", "Ret": "\u274c", "Yedek": "\U0001f4cb",
                                  "Beklemede": "\u23f3"}.get(iv.decision, "\u2796")
                        st.write(f"{k_icon} **Asama {iv.stage}** | {iv.interview_date} | "
                                 f"{iv.interview_type} | Karar: {iv.decision or '-'}")
                        scores = store.find_by_field("interview_scores", "interview_id", iv.id)
                        if scores:
                            score_objs = [InterviewScore.from_dict(s) if isinstance(s, dict) else s for s in scores]
                            total = sum(s.score for s in score_objs)
                            avg = total / len(score_objs) if score_objs else 0
                            st.caption(f"Puan: {total}/{len(score_objs)*5} (Ort: {avg:.2f}/5)")

                # Performans degerlendirmeleri
                reviews = store.find_by_field("performance_reviews", "employee_id", det_emp.id)
                if reviews:
                    styled_section("Performans Değerlendirmeleri", "#8b5cf6")
                    rev_objs = [PerformanceReview.from_dict(r) if isinstance(r, dict) else r for r in reviews]
                    for r in rev_objs:
                        renk = PerformanceCalculator.get_label_color(r.label)
                        st.markdown(
                            f"**{PERFORMANCE_PERIOD_LABELS.get(r.period_type, r.period_type)}** | "
                            f"Skor: **{r.score_100:.1f}/100** | "
                            f"<span style='color:{renk};font-weight:700;'>{r.label}</span>",
                            unsafe_allow_html=True
                        )

                # Izin ozeti
                izinler = store.load_list("izinler")
                kisi_izinler = [i for i in izinler if i.get("personel_id") == det_emp.staff_id
                                or f"{det_emp.ad} {det_emp.soyad}".strip() == i.get("personel_adi", "")]
                if kisi_izinler:
                    styled_section("İzin Özeti", "#f59e0b")
                    toplam_izin = sum(i.get("gun_sayisi", 0) for i in kisi_izinler if i.get("durum") == "onaylandi")
                    st.write(f"Toplam onaylanmis izin: **{toplam_izin} gun**")

                # ===== DEMIRBAS TESLIM DURUMU =====
                st.markdown("---")
                styled_section("Demirbas Teslim Durumu", "#6366f1")

                calisan_adi = f"{det_emp.ad} {det_emp.soyad}".strip()
                db_durum = _get_demirbas_teslim_durumu(calisan_adi)

                if db_durum["zimmet_yok"]:
                    st.markdown("""<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);
                    border-radius:12px;padding:16px;border-left:5px solid #10b981;">
                    <span style="font-size:1.1rem;">&#9989;</span>
                    <span style="font-weight:700;color:#059669;"> Bu calisanin zimmetli demirbasi bulunmuyor.</span>
                    </div>""", unsafe_allow_html=True)
                elif db_durum["teslim_tamam"]:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);
                    border-radius:12px;padding:16px;border-left:5px solid #10b981;">
                    <span style="font-size:1.1rem;">&#9989;</span>
                    <span style="font-weight:700;color:#059669;"> Demirbas Teslimi Yapildi</span>
                    <span style="color:#64748b;font-size:0.85rem;"> &mdash; {db_durum['iade']} kalem iade edildi</span>
                    </div>""", unsafe_allow_html=True)

                    # Iade edilen kalemlerin listesi
                    iade_items = db_durum["iade_demirbas"] + db_durum["iade_tuketim"]
                    if iade_items:
                        items_html = ""
                        for item in iade_items:
                            adi = getattr(item, "demirbas_adi", "") or getattr(item, "urun_adi", "")
                            kodu = getattr(item, "demirbas_kodu", "") or getattr(item, "urun_kodu", "")
                            iade_t = getattr(item, "iade_tarihi", "") or "-"
                            items_html += (
                                f'<div style="display:inline-flex;align-items:center;gap:6px;margin:4px 10px;">'
                                f'<span style="color:#10b981;">&#10003;</span>'
                                f'<span style="font-size:0.85rem;color:#94A3B8;font-weight:600;">{adi}</span>'
                                f'<span style="font-size:0.75rem;color:#94a3b8;">({kodu} | iade: {iade_t})</span></div>'
                            )
                        st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin:8px 0;">{items_html}</div>',
                                    unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#fef2f2 0%,#fee2e2 100%);
                    border-radius:12px;padding:16px;border-left:5px solid #ef4444;">
                    <span style="font-size:1.1rem;">&#9888;&#65039;</span>
                    <span style="font-weight:700;color:#dc2626;"> Bekleyen Demirbas Var</span>
                    <span style="color:#64748b;font-size:0.85rem;">
                    &mdash; {db_durum['aktif']} aktif zimmet, {db_durum['iade']} iade edildi (toplam {db_durum['toplam']})</span>
                    </div>""", unsafe_allow_html=True)

                    # Aktif (bekleyen) kalemlerin listesi
                    aktif_items = db_durum["aktif_demirbas"] + db_durum["aktif_tuketim"]
                    if aktif_items:
                        items_html = ""
                        for item in aktif_items:
                            adi = getattr(item, "demirbas_adi", "") or getattr(item, "urun_adi", "")
                            kodu = getattr(item, "demirbas_kodu", "") or getattr(item, "urun_kodu", "")
                            tarih = getattr(item, "zimmet_tarihi", "") or "-"
                            items_html += (
                                f'<div style="display:inline-flex;align-items:center;gap:6px;margin:4px 10px;">'
                                f'<span style="color:#ef4444;">&#10060;</span>'
                                f'<span style="font-size:0.85rem;color:#94A3B8;font-weight:600;">{adi}</span>'
                                f'<span style="font-size:0.75rem;color:#94a3b8;">({kodu} | zimmet: {tarih})</span></div>'
                            )
                        st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin:8px 0;">{items_html}</div>',
                                    unsafe_allow_html=True)
                    styled_info_banner(
                        "Çalışanın tum demirbas ve zimmetlerini TDM modulunden iade almayi unutmayin!",
                        "warning", "\u26a0\ufe0f"
                    )

                # ===== ISTEN AYRILDI FORMU =====
                st.markdown("---")
                styled_section("Isten Ayrilma İşlemi", "#ef4444")
                styled_info_banner(
                    "Bu calisan isten ayrildiginda asagidaki formu doldurun. "
                    "Çalışan aktif listeden cikarilip 'İşten Ayrılanlar' sekmesine tasitir.",
                    "warning", "\u26a0\ufe0f"
                )

                # Satir 1: Neden + Tarih + Ayrilma Sekli
                ay_c1, ay_c2, ay_c3 = st.columns(3)
                with ay_c1:
                    ayrilma_neden = st.selectbox(
                        "Ayrilma Nedeni",
                        ["Istifa", "Sozlesme Bitis", "Fesih", "Emeklilik", "Karsilikli Anlasma", "Diger"],
                        key=f"ik_ac_ay_neden_{det_emp.id}"
                    )
                with ay_c2:
                    ayrilma_tarih = st.date_input("Ayrilma Tarihi", key=f"ik_ac_ay_tarih_{det_emp.id}")
                with ay_c3:
                    ayrilma_sekli = st.selectbox(
                        "Ayrilma Sekli",
                        AYRILMA_SEKILLERI,
                        key=f"ik_ac_ay_sekil_{det_emp.id}"
                    )

                # Satir 2: Uzlasma + Not
                ay_c4, ay_c5 = st.columns(2)
                with ay_c4:
                    uzlasma = st.selectbox(
                        "Uzlasma Durumu",
                        UZLASMA_DURUMLARI,
                        key=f"ik_ac_ay_uzlasma_{det_emp.id}"
                    )
                with ay_c5:
                    ayrilma_not = st.text_area("Açıklama / Not", height=100,
                                                key=f"ik_ac_ay_not_{det_emp.id}")

                # ===== ISTEN CIKIS EVRAKLARI =====
                styled_section("Isten Çıkış Evraklari", "#8b5cf6")
                evrak_cols = st.columns(3)
                cikis_evrak_vals = {}
                for idx_e, (ekey, elabel) in enumerate(ISTEN_CIKIS_EVRAKLARI):
                    with evrak_cols[idx_e % 3]:
                        cikis_evrak_vals[ekey] = st.checkbox(
                            elabel, key=f"ik_ac_ce_{ekey}_{det_emp.id}"
                        )

                # Uzlasma durumu gosterge
                _uzl_renk = {"Uzlasarak Ayrildi": "#10b981", "Itilafli Ayrildi": "#ef4444", "Belirsiz": "#f59e0b"}
                _uzl_icon = {"Uzlasarak Ayrildi": "&#9989;", "Itilafli Ayrildi": "&#9888;&#65039;", "Belirsiz": "&#10067;"}
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#111827,#1A2035);'
                    f'border-radius:10px;padding:12px 16px;margin:10px 0;border-left:5px solid '
                    f'{_uzl_renk.get(uzlasma, "#64748b")};">'
                    f'<span>{_uzl_icon.get(uzlasma, "")}</span> '
                    f'<span style="font-weight:700;color:{_uzl_renk.get(uzlasma, "#64748b")};">'
                    f'{uzlasma}</span>'
                    f' <span style="color:#64748b;font-size:0.85rem;">| {ayrilma_sekli}</span></div>',
                    unsafe_allow_html=True
                )

                if st.button("Isten Ayrildi Olarak Isaretle", key=f"ik_ac_ay_btn_{det_emp.id}",
                             type="primary", use_container_width=True):
                    det_emp.status = "Ayrildi"
                    det_emp.ayrilma_tarihi = ayrilma_tarih.isoformat()
                    det_emp.ayrilma_nedeni = ayrilma_neden
                    det_emp.ayrilma_notu = ayrilma_not
                    det_emp.ayrilma_sekli = ayrilma_sekli
                    det_emp.uzlasma_durumu = uzlasma
                    det_emp.cikis_evraklari = cikis_evrak_vals
                    det_emp.updated_at = _now_str()
                    store.upsert("employees", det_emp)

                    # Tum modullerden otomatik cikar (kim01_staff.json)
                    remove_employee_from_shared_staff(
                        employee_id=det_emp.id,
                        ad=det_emp.ad,
                        soyad=det_emp.soyad,
                    )

                    AuditLogger.log(store, "cikis_tamamlandı", "employee", det_emp.id,
                                    f"{det_emp.employee_code} - {det_emp.tam_ad}: {ayrilma_neden} / {ayrilma_sekli}")
                    styled_info_banner(
                        f"{det_emp.tam_ad} isten ayrildi olarak isaretlendi. "
                        f"Tüm modullerden cikarildi. 'İşten Ayrılanlar' sekmesinde goruntulenir.",
                        "success"
                    )
                    st.rerun()

            # CSV export
            if rows:
                st.markdown("---")
                csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
                st.download_button("Aktif Çalışanlar CSV Indir", csv_data,
                                   "aktif_calisanlar.csv", "text/csv", key="ik_ac_csv")

    # ===== ISTEN AYRILANLAR =====
    with sub_tabs[1]:
        styled_section("İşten Ayrılanlar", "#ef4444")

        ayrilanlar = [e for e in employees if e.status == "Ayrildi"]

        if not ayrilanlar:
            styled_info_banner("Henuz isten ayrilan calisan yok.", "info")
        else:
            # Neden dagilimi
            neden_counts = {}
            for e in ayrilanlar:
                neden = getattr(e, "ayrilma_nedeni", "") or "Belirtilmedi"
                neden_counts[neden] = neden_counts.get(neden, 0) + 1

            styled_stat_row([
                ("Toplam Ayrilan", len(ayrilanlar), "#ef4444", "\U0001f6aa"),
                ("Istifa", neden_counts.get("Istifa", 0), "#f59e0b", "\U0001f4dd"),
                ("Sozlesme Bitis", neden_counts.get("Sozlesme Bitis", 0), "#64748b", "\U0001f4c4"),
                ("Fesih", neden_counts.get("Fesih", 0), "#dc2626", "\u274c"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            # Liste
            rows = []
            for e in sorted(ayrilanlar, key=lambda x: getattr(x, "ayrilma_tarihi", "") or "", reverse=True):
                rows.append({
                    "Çalışan Kodu": e.employee_code,
                    "Ad Soyad": e.tam_ad,
                    "Pozisyon": e.position_name or e.position_code or "-",
                    "Ayrilma Tarihi": getattr(e, "ayrilma_tarihi", "") or "-",
                    "Neden": getattr(e, "ayrilma_nedeni", "") or "-",
                    "Ayrilma Sekli": getattr(e, "ayrilma_sekli", "") or "-",
                    "Uzlasma": getattr(e, "uzlasma_durumu", "") or "-",
                    "Kidem": _calc_kidem_str(e.ise_baslama_tarihi),
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True, use_container_width=True)

            # Detay
            styled_section("Ayrilan Çalışan Detay", "#64748b")
            ay_labels = [f"{e.employee_code} - {e.tam_ad}" for e in ayrilanlar]
            ay_idx = st.selectbox("Çalışan secin", range(len(ay_labels)),
                                   format_func=lambda i: ay_labels[i], key="ik_ac_ay_det")
            ay_emp = ayrilanlar[ay_idx]

            # Bilgi karti
            ay_neden = getattr(ay_emp, "ayrilma_nedeni", "") or "-"
            ay_tarih = getattr(ay_emp, "ayrilma_tarihi", "") or "-"
            ay_not = getattr(ay_emp, "ayrilma_notu", "") or "-"
            ay_sekil = getattr(ay_emp, "ayrilma_sekli", "") or "-"
            ay_uzlasma = getattr(ay_emp, "uzlasma_durumu", "") or "-"

            # Uzlasma renk
            _uzl_map = {"Uzlasarak Ayrildi": ("#10b981", "&#9989;"),
                        "Itilafli Ayrildi": ("#ef4444", "&#9888;&#65039;"),
                        "Belirsiz": ("#f59e0b", "&#10067;")}
            _uzl_r, _uzl_i = _uzl_map.get(ay_uzlasma, ("#64748b", ""))

            st.markdown(f"""<div style="background:linear-gradient(135deg,#fef2f2 0%,#fee2e2 100%);
            border-radius:14px;padding:20px;margin:10px 0;border-left:5px solid #ef4444;">
            <div style="font-weight:800;font-size:1.2rem;color:#94A3B8;">{ay_emp.tam_ad}</div>
            <div style="font-size:0.85rem;color:#64748b;margin-top:2px;">
            {ay_emp.employee_code} | {ay_emp.position_name or '-'} | Ayrilis: {ay_tarih} | Neden: {ay_neden}
            </div>
            <div style="margin-top:6px;display:flex;gap:12px;flex-wrap:wrap;">
            <span style="background:{_uzl_r};color:#fff;padding:3px 10px;border-radius:8px;
            font-size:0.8rem;font-weight:700;">{_uzl_i} {ay_uzlasma}</span>
            <span style="background:#6366f1;color:#fff;padding:3px 10px;border-radius:8px;
            font-size:0.8rem;font-weight:700;">{ay_sekil}</span>
            </div></div>""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Kisisel Bilgiler**")
                st.write(f"**TC No:** {ay_emp.tc_no or '-'}")
                st.write(f"**Telefon:** {ay_emp.telefon or '-'}")
                st.write(f"**Email:** {ay_emp.email or '-'}")
            with c2:
                st.markdown("**Görev Bilgileri**")
                st.write(f"**Pozisyon:** {ay_emp.position_name or '-'}")
                st.write(f"**Rol:** {ay_emp.role_scope}")
                st.write(f"**Kampus:** {ay_emp.kampus or '-'}")
                st.write(f"**Kademe:** {ay_emp.kademe or '-'}")
            with c3:
                st.markdown("**Ayrilma Bilgileri**")
                st.write(f"**Ise Baslama:** {ay_emp.ise_baslama_tarihi or '-'}")
                st.write(f"**Ayrilma Tarihi:** {ay_tarih}")
                st.write(f"**Kidem:** {_calc_kidem_str(ay_emp.ise_baslama_tarihi)}")
                st.write(f"**Neden:** {ay_neden}")
                st.write(f"**Ayrilma Sekli:** {ay_sekil}")
                st.write(f"**Uzlasma:** {ay_uzlasma}")
                if ay_not and ay_not != "-":
                    st.write(f"**Not:** {ay_not}")

            # Isten cikis evraklari
            ay_cikis_evrak = getattr(ay_emp, "cikis_evraklari", {}) or {}
            if ay_cikis_evrak or True:  # her zaman goster
                styled_section("Isten Çıkış Evraklari", "#8b5cf6")
                cevrak_html = ""
                for ekey, elabel in ISTEN_CIKIS_EVRAKLARI:
                    durum = ay_cikis_evrak.get(ekey, False)
                    icon = "\u2705" if durum else "\u274c"
                    renk = "#10b981" if durum else "#ef4444"
                    cevrak_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:6px;margin:4px 12px;">'
                        f'<span>{icon}</span>'
                        f'<span style="font-size:0.85rem;color:{renk};font-weight:600;">{elabel}</span></div>'
                    )
                st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin:4px 0;">{cevrak_html}</div>',
                            unsafe_allow_html=True)

            # Ise alim evraklari
            evrak_data = store.load_list("ise_alim_evraklari")
            emp_evrak = next((e for e in evrak_data if e.get("candidate_id") == ay_emp.candidate_id), None)
            if emp_evrak:
                styled_section("Ise Alim Evraklari", "#64748b")
                evraklar = emp_evrak.get("evraklar", {})
                evrak_html = ""
                for key, label in ISE_ALIM_EVRAKLARI:
                    durum = evraklar.get(key, False)
                    icon = "\u2705" if durum else "\u274c"
                    renk = "#10b981" if durum else "#ef4444"
                    evrak_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:6px;margin:4px 12px;">'
                        f'<span>{icon}</span>'
                        f'<span style="font-size:0.85rem;color:{renk};font-weight:600;">{label}</span></div>'
                    )
                st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin:4px 0;">{evrak_html}</div>',
                            unsafe_allow_html=True)

            # Demirbas teslim durumu
            ay_calisan_adi = f"{ay_emp.ad} {ay_emp.soyad}".strip()
            ay_db_durum = _get_demirbas_teslim_durumu(ay_calisan_adi)

            if not ay_db_durum["zimmet_yok"]:
                styled_section("Demirbas Teslim Durumu", "#6366f1")
                if ay_db_durum["teslim_tamam"]:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);
                    border-radius:12px;padding:14px;border-left:5px solid #10b981;">
                    <span style="font-size:1.1rem;">&#9989;</span>
                    <span style="font-weight:700;color:#059669;"> Tum Demirbaslar Teslim Edildi</span>
                    <span style="color:#64748b;font-size:0.85rem;"> &mdash; {ay_db_durum['iade']} kalem</span>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#fef2f2 0%,#fee2e2 100%);
                    border-radius:12px;padding:14px;border-left:5px solid #ef4444;">
                    <span style="font-size:1.1rem;">&#9888;&#65039;</span>
                    <span style="font-weight:700;color:#dc2626;"> {ay_db_durum['aktif']} Kalem Teslim Edilmedi</span>
                    <span style="color:#64748b;font-size:0.85rem;"> &mdash; {ay_db_durum['iade']} iade, toplam {ay_db_durum['toplam']}</span>
                    </div>""", unsafe_allow_html=True)

                # Detay listesi
                all_items = (ay_db_durum["iade_demirbas"] + ay_db_durum["iade_tuketim"]
                             + ay_db_durum["aktif_demirbas"] + ay_db_durum["aktif_tuketim"])
                if all_items:
                    items_html = ""
                    for item in all_items:
                        adi = getattr(item, "demirbas_adi", "") or getattr(item, "urun_adi", "")
                        kodu = getattr(item, "demirbas_kodu", "") or getattr(item, "urun_kodu", "")
                        d = item.durum
                        if d == "İade Edildi":
                            icon, renk = "&#10003;", "#10b981"
                        else:
                            icon, renk = "&#10060;", "#ef4444"
                        items_html += (
                            f'<div style="display:inline-flex;align-items:center;gap:6px;margin:4px 10px;">'
                            f'<span style="color:{renk};">{icon}</span>'
                            f'<span style="font-size:0.85rem;color:#94A3B8;font-weight:600;">{adi}</span>'
                            f'<span style="font-size:0.75rem;color:#94a3b8;">({kodu} - {d})</span></div>'
                        )
                    st.markdown(f'<div style="display:flex;flex-wrap:wrap;margin:8px 0;">{items_html}</div>',
                                unsafe_allow_html=True)

            # CSV export
            if rows:
                st.markdown("---")
                csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
                st.download_button("İşten Ayrılanlar CSV Indir", csv_data,
                                   "isten_ayrilanlar.csv", "text/csv", key="ik_ac_ay_csv")

    # ===== EXCEL / PDF IMPORT =====
    with sub_tabs[2]:
        styled_section("Excel / PDF ile Toplu Çalışan Import", "#2563eb")

        st.markdown(
            '<div style="background:linear-gradient(135deg,#1e40af 0%,#2563eb 100%);'
            'color:white;padding:12px 20px;border-radius:12px;margin-bottom:16px;'
            'display:flex;align-items:center;gap:10px;font-size:0.9rem">'
            '<span style="font-size:1.3rem">📥</span>'
            '<span><b>Toplu Import:</b> Excel veya PDF dosyanizdan calisanlari sisteme toplu olarak ekleyin. '
            'Eklenen calisanlar tüm modullerde (Akademik Takip, Kurumsal Iletisim vb.) otomatik kullanilir.</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.info(
            "**Excel/CSV** dosyaniz su sütunlari icermelidir:\n\n"
            "**Zorunlu:** `ad`, `soyad`\n\n"
            "**Opsiyonel:** `tc_no`, `telefon`, `email`, `pozisyon`, `rol` "
            "(TEACHER/MANAGEMENT/ADMIN/SUPPORT), `brans`, `kampus`, `kademe`, `ise_baslama_tarihi`"
        )

        # Ornek sablon indirme
        _sablon_cols = ["ad", "soyad", "tc_no", "telefon", "email",
                        "pozisyon", "rol", "brans", "kampus", "kademe", "ise_baslama_tarihi"]
        _sablon_df = pd.DataFrame(columns=_sablon_cols)
        _sablon_df.loc[0] = ["Ahmet", "Yilmaz", "12345678901", "05321234567",
                              "ahmet@okul.com", "Matematik Ogretmeni", "TEACHER",
                              "Matematik", "Ana Kampus", "Ortaokul", "2024-09-01"]
        _sablon_csv = _sablon_df.to_csv(index=False).encode("utf-8")
        st.download_button("📄 Örnek Şablon İndir (CSV)", _sablon_csv,
                           "calisan_import_sablon.csv", "text/csv", key="ik_imp_sablon")

        st.markdown("")

        ik_imp_file = st.file_uploader(
            "Excel / CSV / PDF Dosyasi Yükle",
            type=["xlsx", "xls", "csv", "pdf"],
            key="ik_imp_upload",
        )

        if ik_imp_file:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(ik_imp_file, allowed_types=["xlsx", "xls", "csv", "pdf"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                ik_imp_file = None
        if ik_imp_file:
            _imp_df = None
            _imp_error = None

            try:
                if ik_imp_file.name.lower().endswith(".csv"):
                    _imp_df = pd.read_csv(ik_imp_file)
                elif ik_imp_file.name.lower().endswith((".xlsx", ".xls")):
                    _imp_df = pd.read_excel(ik_imp_file)
                elif ik_imp_file.name.lower().endswith(".pdf"):
                    # PDF'den tablo cikarma
                    try:
                        import tabula
                        _tables = tabula.read_pdf(ik_imp_file, pages="all", multiple_tables=True)
                        if _tables:
                            _imp_df = pd.concat(_tables, ignore_index=True)
                        else:
                            _imp_error = "PDF dosyasinda tablo bulunamadi."
                    except ImportError:
                        # tabula yoksa pdfplumber dene
                        try:
                            import pdfplumber
                            _pages_data = []
                            ik_imp_file.seek(0)
                            with pdfplumber.open(ik_imp_file) as _pdf:
                                for _page in _pdf.pages:
                                    _tbl = _page.extract_table()
                                    if _tbl and len(_tbl) > 1:
                                        _hdr = _tbl[0]
                                        for _row in _tbl[1:]:
                                            _pages_data.append(dict(zip(_hdr, _row)))
                            if _pages_data:
                                _imp_df = pd.DataFrame(_pages_data)
                            else:
                                _imp_error = "PDF dosyasinda tablo bulunamadi."
                        except ImportError:
                            _imp_error = ("PDF import icin `tabula-py` veya `pdfplumber` "
                                          "paketlerinden biri gereklidir. "
                                          "`pip install pdfplumber` ile yukleyin.")
            except Exception as e:
                _imp_error = f"Dosya okuma hatasi: {e}"

            if _imp_error:
                st.error(_imp_error)
            elif _imp_df is not None and not _imp_df.empty:
                # Sutun isimlendirmesini normalize et
                _imp_df.columns = [c.strip().lower().replace(" ", "_") for c in _imp_df.columns]

                st.success(f"**{len(_imp_df)} kayit** bulundu:")
                st.dataframe(_imp_df.head(15), use_container_width=True, hide_index=True)

                # Zorunlu sutun kontrolu
                _has_ad = "ad" in _imp_df.columns
                _has_soyad = "soyad" in _imp_df.columns
                if not _has_ad or not _has_soyad:
                    st.warning("Dosyada **ad** ve **soyad** sütunlari bulunamadi. "
                               "Sütun basliklarini kontrol edin.")
                else:
                    st.markdown(f"**{len(_imp_df)}** calisan import edilecek.")

                    if st.button("Tümünü Import Et", type="primary",
                                 use_container_width=True, key="ik_imp_btn"):
                        import uuid as _uuid
                        _mevcut = store.load_list("employees")
                        _mevcut_codes = {e.get("employee_code", "") for e in _mevcut}
                        _eklenen = 0
                        _hatalar = []

                        for _ri, _row in _imp_df.iterrows():
                            try:
                                _ad = str(_row.get("ad", "")).strip()
                                _soyad = str(_row.get("soyad", "")).strip()
                                if not _ad or not _soyad or _ad == "nan":
                                    continue

                                # Benzersiz employee_code uret
                                _code = f"EMP-{_uuid.uuid4().hex[:6].upper()}"
                                while _code in _mevcut_codes:
                                    _code = f"EMP-{_uuid.uuid4().hex[:6].upper()}"
                                _mevcut_codes.add(_code)

                                _rol = str(_row.get("rol", "ALL")).strip().upper()
                                if _rol not in ("TEACHER", "MANAGEMENT", "ADMIN", "SUPPORT", "ALL"):
                                    _rol = "ALL"

                                _new_emp = {
                                    "id": f"emp_{_uuid.uuid4().hex[:8]}",
                                    "employee_code": _code,
                                    "candidate_id": "",
                                    "candidate_code": "",
                                    "tc_no": str(_row.get("tc_no", "")).strip(),
                                    "ad": _ad,
                                    "soyad": _soyad,
                                    "telefon": str(_row.get("telefon", "")).strip(),
                                    "email": str(_row.get("email", "")).strip(),
                                    "position_id": "",
                                    "position_code": "",
                                    "position_name": str(_row.get("pozisyon", "")).strip(),
                                    "role_scope": _rol,
                                    "brans": str(_row.get("brans", "")).strip(),
                                    "kampus": str(_row.get("kampus", "")).strip(),
                                    "kademe": str(_row.get("kademe", "")).strip(),
                                    "ise_baslama_tarihi": str(_row.get("ise_baslama_tarihi", "")).strip(),
                                    "status": "Aktif",
                                    "has_asset_assignment": False,
                                    "staff_id": "",
                                    "ayrilma_tarihi": "",
                                    "ayrilma_nedeni": "",
                                    "ayrilma_notu": "",
                                    "ayrilma_sekli": "",
                                    "uzlasma_durumu": "",
                                    "cikis_evraklari": {},
                                    "created_at": datetime.now().isoformat(),
                                    "updated_at": datetime.now().isoformat(),
                                }
                                # nan temizligi
                                for _k, _v in _new_emp.items():
                                    if str(_v).lower() == "nan":
                                        _new_emp[_k] = ""

                                _mevcut.append(_new_emp)
                                _eklenen += 1
                            except Exception as _e:
                                _hatalar.append(f"Satir {_ri + 1}: {_e}")

                        store.save_list("employees", _mevcut)
                        st.success(f"✅ {_eklenen} çalışan başarıyla import edildi! "
                                   "Tüm modüllere otomatik yansıyacaktır.")
                        if _hatalar:
                            with st.expander(f"⚠️ {len(_hatalar)} hata"):
                                for _h in _hatalar[:20]:
                                    st.warning(_h)
                        st.rerun()
            else:
                st.warning("Dosyada veri bulunamadi.")


# ============================================================
# SEKME 10: OFFBOARDING (STUB)
# ============================================================

def _render_offboarding(store: IKDataStore):
    sub = st.tabs(["🚪 Çıkış Süreci Başlat", "📋 Mevcut Çıkış İşlemleri"])

    with sub[0]:
        styled_section("Çıkış Süreci Başlat", "#64748b")
        employees = store.load_objects("employees")
        aktif = [e for e in employees if e.status == "Aktif"]

        if not aktif:
            styled_info_banner("Aktif calisan yok.", "warning")
        else:
            emp_labels = [f"{e.employee_code} - {e.tam_ad}" for e in aktif]
            emp_idx = st.selectbox("Çalışan Secin", range(len(emp_labels)),
                                   format_func=lambda i: emp_labels[i], key="ik_off_emp")
            sel_emp = aktif[emp_idx]

            c1, c2 = st.columns(2)
            with c1:
                ayrilma_turu = st.selectbox("Ayrilma Turu", OFFBOARDING_TYPES, key="ik_off_tur")
                bildirim_tarihi = st.date_input("Bildirim Tarihi", key="ik_off_bildirim")
            with c2:
                son_gun = st.date_input("Son Calisma Günü", key="ik_off_son_gun")
                ayrilma_nedeni = st.text_input("Ayrilma Nedeni", key="ik_off_neden")

            aciklama = st.text_area("Açıklama", key="ik_off_aciklama", height=80)

            if sel_emp.has_asset_assignment:
                styled_info_banner("Bu calisanin zimmetli malzemesi var. İade edilmeden cikis tamamlanamaz.", "warning")

            if st.button("Çıkış Süreci Başlat", type="primary", key="ik_off_baslat"):
                off = OffboardingRecord(
                    employee_id=sel_emp.id,
                    employee_code=sel_emp.employee_code,
                    employee_name=sel_emp.tam_ad,
                    ayrilma_turu=ayrilma_turu,
                    ayrilma_nedeni=ayrilma_nedeni,
                    bildirim_tarihi=bildirim_tarihi.isoformat(),
                    son_calisma_gunu=son_gun.isoformat(),
                    aciklama=aciklama,
                    status="Baslatildi",
                )
                store.upsert("offboarding", off)
                AuditLogger.log(store, "cikis_basladi", "offboarding", off.id,
                                f"{sel_emp.tam_ad} - {ayrilma_turu}")
                styled_info_banner(f"Çıkış sureci baslatildi: {sel_emp.tam_ad}", "success")
                st.rerun()

    with sub[1]:
        styled_section("Mevcut Çıkış İşlemleri", "#1e40af")
        offboardings = store.load_objects("offboarding")
        if not offboardings:
            styled_info_banner("Çıkış islemi yok.", "info")
        else:
            rows = []
            for o in offboardings:
                rows.append({
                    "Çalışan": o.employee_name,
                    "Tur": o.ayrilma_turu,
                    "Bildirim": o.bildirim_tarihi,
                    "Son Gün": o.son_calisma_gunu,
                    "Durum": o.status,
                    "Zimmet İade": "Evet" if o.assets_returned else "Hayir",
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

            # Tamamlama
            devam_eden = [o for o in offboardings if o.status == "Baslatildi"]
            if devam_eden:
                styled_section("Çıkış Tamamla", "#10b981")
                off_labels = [f"{o.employee_name} - {o.ayrilma_turu}" for o in devam_eden]
                off_idx = st.selectbox("İşlem Secin", range(len(off_labels)),
                                       format_func=lambda i: off_labels[i], key="ik_off_tamam_sec")
                sel_off = devam_eden[off_idx]

                emp = store.get_by_id("employees", sel_off.employee_id)
                emp_obj = Employee.from_dict(emp) if isinstance(emp, dict) else emp

                zimmet_iade = st.checkbox("Zimmet İade Edildi", value=sel_off.assets_returned, key="ik_off_zimmet")

                can_complete, reasons = True, []
                if emp_obj and emp_obj.has_asset_assignment and not zimmet_iade:
                    can_complete = False
                    reasons.append("Zimmetli malzemeler iade edilmedi")

                if reasons:
                    for r in reasons:
                        styled_info_banner(r, "error")

                if st.button("Çıkış Tamamla", type="primary", disabled=not can_complete, key="ik_off_tamam_btn"):
                    sel_off.assets_returned = zimmet_iade
                    sel_off.status = "Tamamlandı"
                    sel_off.updated_at = _now_str()
                    store.upsert("offboarding", sel_off)

                    if emp_obj:
                        emp_obj.status = "Ayrildi"
                        emp_obj.updated_at = _now_str()
                        store.upsert("employees", emp_obj)

                    AuditLogger.log(store, "cikis_tamamlandı", "offboarding", sel_off.id, sel_off.employee_name)
                    styled_info_banner("Çıkış tamamlandı.", "success")
                    st.rerun()


# ============================================================
# SEKME: PERSONEL BILGI KARTI
# ============================================================

def _collect_personel_data(store: IKDataStore, emp: dict) -> dict:
    """Tum modullerden tek personele ait verileri toplar."""
    eid = emp.get("id", "")
    cid = emp.get("candidate_id", "")
    tam_ad = f"{emp.get('ad', '')} {emp.get('soyad', '')}".strip()
    tam_ad_lower = tam_ad.lower()

    data: dict[str, Any] = {"employee": emp, "tam_ad": tam_ad}

    # --- IK: Aday bilgisi ---
    if cid:
        cands = store.load_list("candidates")
        data["candidate"] = next((c for c in cands if c.get("id") == cid), None)
    else:
        data["candidate"] = None

    # --- IK: Mulakatlar ---
    interviews = store.load_list("interviews")
    data["interviews"] = [i for i in interviews if i.get("candidate_id") == cid] if cid else []

    # --- IK: Performans ---
    reviews = store.load_list("performance_reviews")
    data["performance_reviews"] = [r for r in reviews if r.get("employee_id") == eid]

    # --- IK: Izinler ---
    izinler = store.load_list("izinler")
    data["izinler"] = [iz for iz in izinler if iz.get("personel_id") == eid]

    # --- IK: Raporlar ---
    raporlar = store.load_list("raporlar")
    data["raporlar"] = [r for r in raporlar if r.get("personel_id") == eid]

    # --- IK: Devamsizlik ---
    devamsizlik = store.load_list("devamsizlik")
    data["devamsizlik"] = [d for d in devamsizlik if d.get("personel_id") == eid]

    # --- IK: Gec Kalma ---
    gec_kalma = store.load_list("gec_kalma")
    data["gec_kalma"] = [g for g in gec_kalma if g.get("personel_id") == eid or
                          g.get("personel_adi", "").lower() == tam_ad_lower]

    # --- IK: Disiplin ---
    disiplin = store.load_list("disiplin")
    data["disiplin"] = [d for d in disiplin if d.get("personel_id") == eid]

    # --- IK: Egitimler ---
    egitimler = store.load_list("egitimler")
    data["egitimler"] = [e for e in egitimler if e.get("personel_id") == eid]

    # --- IK: Maas/Bordro ---
    bordro = store.load_list("maas_bordro")
    data["bordro"] = [b for b in bordro if b.get("personel_id") == eid]

    # --- IK: Offboarding ---
    offboarding = store.load_list("offboarding")
    data["offboarding"] = [o for o in offboarding
                           if o.get("employee_id") == eid or o.get("employee_name", "").lower() == tam_ad_lower]

    # --- Akademik: Ogretmen eslestirme ---
    try:
        ak_store = _get_akademik_store()
        teachers = ak_store.get_teachers()
        teacher = None
        for t in teachers:
            if t.tam_ad.strip().lower() == tam_ad_lower:
                teacher = t
                break
        data["teacher"] = teacher

        if teacher:
            data["schedule"] = ak_store.get_schedule(ogretmen_id=teacher.id)
            try:
                nobet_gorevler = ak_store.get_nobet_gorevler()
                data["nobet_gorevler"] = [g for g in nobet_gorevler if g.ogretmen_id == teacher.id]
                nobet_kayitlar = ak_store.get_nobet_kayitlar()
                data["nobet_kayitlar"] = [k for k in nobet_kayitlar if k.ogretmen_id == teacher.id]
            except Exception:
                data["nobet_gorevler"] = []
                data["nobet_kayitlar"] = []

            # Devamsizlik kayitlari
            try:
                att_data = ak_store._load(ak_store.attendance_file)
                data["attendance"] = [a for a in att_data
                                      if a.get("ogretmen_id") == teacher.id or a.get("ogretmen") == tam_ad]
            except Exception:
                data["attendance"] = []
        else:
            data["schedule"] = []
            data["nobet_gorevler"] = []
            data["nobet_kayitlar"] = []
            data["attendance"] = []
    except Exception:
        data["teacher"] = None
        data["schedule"] = []
        data["nobet_gorevler"] = []
        data["nobet_kayitlar"] = []
        data["attendance"] = []

    # --- TDM: Zimmet ---
    try:
        tdm = _get_tdm_store()
        zimmetler = tdm.load_list("zimmet_kayitlari")
        data["zimmetler"] = [z for z in zimmetler if z.get("personel_adi", "").strip().lower() == tam_ad_lower]
        tuketim_z = tdm.load_list("tuketim_zimmetleri")
        data["tuketim_zimmetleri"] = [z for z in tuketim_z if z.get("personel_adi", "").strip().lower() == tam_ad_lower]
    except Exception:
        data["zimmetler"] = []
        data["tuketim_zimmetleri"] = []

    return data


def _render_personel_bilgi_karti(store: IKDataStore):
    """Personel Bilgi Karti - tum modullerden veri toplayan kapsamli personel raporu."""
    styled_section("Personel Bilgi Karti", "#1e40af")

    employees = store.load_list("employees")
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    tum_emp = aktif + [e for e in employees if e.get("status") != "Aktif"]

    if not tum_emp:
        styled_info_banner("Henuz kayitli calisan bulunmuyor.", "info")
        return

    options = ["-- Personel Secin --"] + [
        f"{e.get('ad', '')} {e.get('soyad', '')} - {e.get('position_name', '')} ({e.get('status', '')})"
        for e in tum_emp
    ]
    idx = st.selectbox("Personel", range(len(options)), format_func=lambda i: options[i], key="pbk_personel_sec")
    if idx == 0:
        styled_info_banner("Bilgi kartini goruntulemek icin bir personel secin.", "info")
        return

    emp = tum_emp[idx - 1]
    data = _collect_personel_data(store, emp)
    tam_ad = data["tam_ad"]

    # ---- PDF INDIR BUTONU ----
    pdf_col1, pdf_col2 = st.columns([3, 1])
    with pdf_col2:
        if st.button("PDF Indir", key="pbk_pdf_btn", type="primary"):
            pdf_bytes = _generate_personel_bilgi_karti_pdf(data)
            if pdf_bytes:
                st.download_button(
                    "PDF Kaydet",
                    data=pdf_bytes,
                    file_name=f"personel_bilgi_karti_{tam_ad.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key="pbk_pdf_download",
                )

    # ===== 1. KIMLIK & TEMEL BILGILER =====
    styled_section("Kimlik & Temel Bilgiler", "#1e40af")
    cand = data.get("candidate")
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"**Ad Soyad:** {tam_ad}")
        st.markdown(f"**TC Kimlik No:** {emp.get('tc_no', '-')}")
        st.markdown(f"**Personel Kodu:** {emp.get('employee_code', '-')}")
        st.markdown(f"**Brans:** {emp.get('brans', '-')}")
    with k2:
        st.markdown(f"**Pozisyon:** {emp.get('position_name', '-')}")
        st.markdown(f"**Rol Kapsamı:** {emp.get('role_scope', '-')}")
        st.markdown(f"**Kampus:** {emp.get('kampus', '-')}")
        st.markdown(f"**Kademe:** {emp.get('kademe', '-')}")
    with k3:
        st.markdown(f"**Ise Baslama:** {emp.get('ise_baslama_tarihi', '-')}")
        st.markdown(f"**Kidem:** {_calc_kidem(emp.get('ise_baslama_tarihi', ''))}")
        st.markdown(f"**Durum:** {emp.get('status', '-')}")
        st.markdown(f"**Telefon:** {emp.get('telefon', '-')}")

    if cand:
        with st.expander("Aday Kayit Bilgileri"):
            ac1, ac2 = st.columns(2)
            with ac1:
                st.markdown(f"**Aday Kodu:** {cand.get('candidate_code', '-')}")
                st.markdown(f"**Basvuru Tarihi:** {cand.get('basvuru_tarihi', '-')}")
                st.markdown(f"**Kaynak:** {cand.get('kaynak', '-')}")
            with ac2:
                st.markdown(f"**Email:** {cand.get('email', '-')}")
                st.markdown(f"**Cinsiyet:** {cand.get('cinsiyet', '-')}")
                st.markdown(f"**Dogum Tarihi:** {cand.get('dogum_tarihi', '-')}")
                st.markdown(f"**Adres:** {cand.get('adres', '-')}")

    # ===== 2. MULAKAT GECMISI =====
    styled_section("Mulakat Gecmisi", "#8b5cf6")
    ivs = data.get("interviews", [])
    if ivs:
        for iv in ivs:
            st.markdown(
                f"- **{iv.get('interview_date', '-')}** | Tur: {iv.get('interview_type', '-')} | "
                f"Karar: **{iv.get('decision', '-')}** | Puan: {iv.get('overall_score', '-')} | "
                f"Not: {iv.get('notes', '-')[:80]}"
            )
    else:
        st.info("Mulakat kaydi bulunamadi.")

    # ===== 3. PERFORMANS DEGERLENDIRMELERI =====
    styled_section("Performans Degerlendirmeleri", "#10b981")
    reviews = data.get("performance_reviews", [])
    if reviews:
        for rv in sorted(reviews, key=lambda x: x.get("created_at", ""), reverse=True):
            period = rv.get("period_label", rv.get("period_type", "-"))
            score = rv.get("overall_score", rv.get("puan", "-"))
            label = rv.get("score_label", "")
            st.markdown(
                f"- **{period}** | Puan: **{score}** {f'({label})' if label else ''} | "
                f"Degerlendiren: {rv.get('reviewer_name', '-')} | Tarih: {rv.get('created_at', '-')[:10]}"
            )
    else:
        st.info("Performans degerlendirmesi bulunamadi.")

    # ===== 4. IZIN BILGILERI =====
    styled_section("Izin Bilgileri", "#0d9488")
    izinler = data.get("izinler", [])
    if izinler:
        iz_stat = {}
        toplam_gun = 0
        for iz in izinler:
            tip = iz.get("izin_tipi", "Diger")
            gun = iz.get("gun_sayisi", 0) or 0
            iz_stat[tip] = iz_stat.get(tip, 0) + gun
            toplam_gun += gun

        cols = st.columns(min(len(iz_stat) + 1, 5))
        with cols[0]:
            st.metric("Toplam Izin", f"{toplam_gun} gun")
        for i, (tip, gun) in enumerate(iz_stat.items()):
            if i + 1 < len(cols):
                with cols[i + 1]:
                    st.metric(tip, f"{gun} gun")

        with st.expander(f"Izin Detaylari ({len(izinler)} kayit)"):
            for iz in sorted(izinler, key=lambda x: x.get("baslangic_tarihi", ""), reverse=True):
                st.markdown(
                    f"- {iz.get('baslangic_tarihi', '-')} → {iz.get('bitis_tarihi', '-')} | "
                    f"**{iz.get('izin_tipi', '-')}** | {iz.get('gun_sayisi', '-')} gun | "
                    f"Durum: {iz.get('durum', '-')}"
                )
    else:
        st.info("Izin kaydi bulunamadi.")

    # ===== 5. RAPOR (SAGLIK) =====
    styled_section("Saglik Raporlari", "#ef4444")
    raporlar = data.get("raporlar", [])
    if raporlar:
        toplam_rapor_gun = sum(r.get("gun_sayisi", 0) or 0 for r in raporlar)
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Toplam Rapor", f"{len(raporlar)} adet")
        with r2:
            st.metric("Toplam Rapor Gunu", f"{toplam_rapor_gun} gun")
        for rp in sorted(raporlar, key=lambda x: x.get("baslangic_tarihi", ""), reverse=True):
            st.markdown(
                f"- {rp.get('baslangic_tarihi', '-')} → {rp.get('bitis_tarihi', '-')} | "
                f"**{rp.get('rapor_turu', '-')}** | {rp.get('gun_sayisi', '-')} gun | "
                f"Kurum: {rp.get('veren_kurum', '-')} | Durum: {rp.get('durum', '-')}"
            )
    else:
        st.info("Saglik raporu bulunamadi.")

    # ===== 5b. DEVAMSIZLIK =====
    styled_section("Devamsizlik Kayitlari", "#dc2626")
    devamsizlik_data = data.get("devamsizlik", [])
    if devamsizlik_data:
        mazeretsiz_d = [d for d in devamsizlik_data if d.get("tur") == "mazeretsiz"]
        toplam_dev_gun = sum(d.get("gun_sayisi", 0) or 0 for d in devamsizlik_data)
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric("Toplam Devamsizlik", f"{len(devamsizlik_data)} kayit")
        with d2:
            st.metric("Mazeretsiz", f"{len(mazeretsiz_d)} kayit")
        with d3:
            st.metric("Toplam Gun", f"{toplam_dev_gun} gun")
        for dv in sorted(devamsizlik_data, key=lambda x: x.get("tarih", ""), reverse=True):
            st.markdown(
                f"- **{dv.get('tarih', '-')}** | {DEVAMSIZLIK_TURLERI.get(dv.get('tur', ''), dv.get('tur', '-'))} | "
                f"{dv.get('gun_sayisi', 1)} gun | Gerekce: {dv.get('gerekce', '-')[:80]}"
            )
    else:
        st.info("Devamsizlik kaydi bulunamadi.")

    # ===== 5c. GEC KALMA =====
    styled_section("Gec Kalma Kayitlari", "#f59e0b")
    gec_kalma_data = data.get("gec_kalma", [])
    if gec_kalma_data:
        toplam_gk_dk = sum(g.get("gec_kalma_dk", 0) or 0 for g in gec_kalma_data)
        g1, g2, g3 = st.columns(3)
        with g1:
            st.metric("Gec Kalma Sayisi", f"{len(gec_kalma_data)} kez")
        with g2:
            st.metric("Toplam Sure", f"{toplam_gk_dk} dk")
        with g3:
            ort = round(toplam_gk_dk / len(gec_kalma_data), 1) if gec_kalma_data else 0
            st.metric("Ortalama", f"{ort} dk")
        with st.expander(f"Gec Kalma Detaylari ({len(gec_kalma_data)} kayit)"):
            for gk in sorted(gec_kalma_data, key=lambda x: x.get("tarih", ""), reverse=True):
                st.markdown(
                    f"- **{gk.get('tarih', '-')}** | Mesai: {gk.get('mesai_baslangic', '-')} | "
                    f"Giris: {gk.get('giris_saati', '-')} | **{gk.get('gec_kalma_dk', 0)} dk** | "
                    f"Kaynak: {gk.get('kaynak', 'Manuel')}"
                )
    else:
        st.info("Gec kalma kaydi bulunamadi.")

    # ===== 6. DISIPLIN =====
    styled_section("Disiplin Islemleri", "#f59e0b")
    disiplin = data.get("disiplin", [])
    if disiplin:
        for ds in sorted(disiplin, key=lambda x: x.get("tarih", ""), reverse=True):
            st.markdown(
                f"- **{ds.get('tarih', '-')}** | Tur: {ds.get('islem_turu', '-')} | "
                f"Aciklama: {ds.get('aciklama', '-')[:100]} | Durum: {ds.get('durum', '-')}"
            )
    else:
        st.info("Disiplin kaydi bulunamadi.")

    # ===== 7. EGITIM & SERTIFIKA =====
    styled_section("Egitim & Sertifikalar", "#8b5cf6")
    egitimler = data.get("egitimler", [])
    if egitimler:
        for eg in egitimler:
            st.markdown(
                f"- **{eg.get('egitim_adi', '-')}** | Tur: {eg.get('egitim_turu', '-')} | "
                f"Tarih: {eg.get('tarih', '-')} | Sure: {eg.get('sure_saat', '-')} saat | "
                f"Durum: {eg.get('durum', '-')}"
            )
    else:
        st.info("Egitim/sertifika kaydi bulunamadi.")

    # ===== 8. MAAS & BORDRO =====
    styled_section("Maas & Bordro", "#059669")
    bordro = data.get("bordro", [])
    if bordro:
        son_bordro = sorted(bordro, key=lambda x: x.get("donem", ""), reverse=True)
        if son_bordro:
            sb = son_bordro[0]
            b1, b2, b3 = st.columns(3)
            with b1:
                st.metric("Son Donem", sb.get("donem", "-"))
            with b2:
                st.metric("Brut Maas", f"{sb.get('brut_maas', '-')} TL")
            with b3:
                st.metric("Net Maas", f"{sb.get('net_maas', '-')} TL")
        with st.expander(f"Bordro Gecmisi ({len(bordro)} kayit)"):
            for br in son_bordro:
                st.markdown(
                    f"- **{br.get('donem', '-')}** | Brut: {br.get('brut_maas', '-')} TL | "
                    f"Net: {br.get('net_maas', '-')} TL"
                )
    else:
        st.info("Bordro kaydi bulunamadi.")

    # ===== 9. HAFTALIK DERS PROGRAMI =====
    styled_section("Haftalik Ders Programi", "#2563eb")
    schedule = data.get("schedule", [])
    teacher = data.get("teacher")
    if schedule:
        gunler = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]
        gun_map: dict[str, list] = {g: [] for g in gunler}
        for slot in schedule:
            gun = getattr(slot, 'gun', '') if hasattr(slot, 'gun') else slot.get('gun', '') if isinstance(slot, dict) else ''
            ders = getattr(slot, 'ders', '') if hasattr(slot, 'ders') else slot.get('ders', '') if isinstance(slot, dict) else ''
            sinif = getattr(slot, 'sinif', '') if hasattr(slot, 'sinif') else slot.get('sinif', '') if isinstance(slot, dict) else ''
            sube = getattr(slot, 'sube', '') if hasattr(slot, 'sube') else slot.get('sube', '') if isinstance(slot, dict) else ''
            saat = getattr(slot, 'saat', '') if hasattr(slot, 'saat') else slot.get('saat', '') if isinstance(slot, dict) else ''
            if gun in gun_map:
                gun_map[gun].append(f"{saat}. {ders} ({sinif}/{sube})")

        toplam_saat = len(schedule)
        st.markdown(f"**Haftalik Toplam Ders Saati:** {toplam_saat}")
        gcols = st.columns(5)
        for i, gun in enumerate(gunler):
            with gcols[i]:
                st.markdown(f"**{gun}**")
                if gun_map[gun]:
                    for d in sorted(gun_map[gun]):
                        st.markdown(f"- {d}")
                else:
                    st.caption("Bos")
    elif teacher:
        st.info("Ders programi kaydi bulunamadi.")
    else:
        st.info("Bu personel akademik takip modulunde ogretmen olarak tanimli degil.")

    # ===== 10. NOBET BILGILERI =====
    styled_section("Nobet Bilgileri", "#64748b")
    nobet_g = data.get("nobet_gorevler", [])
    nobet_k = data.get("nobet_kayitlar", [])
    if nobet_g or nobet_k:
        n1, n2 = st.columns(2)
        with n1:
            st.metric("Nobet Gorevi", f"{len(nobet_g)} adet")
        with n2:
            st.metric("Tutulan Nobet", f"{len(nobet_k)} adet")

        if nobet_g:
            with st.expander("Nobet Gorev Detaylari"):
                for ng in nobet_g:
                    gun = getattr(ng, 'gun', '-') if hasattr(ng, 'gun') else '-'
                    alan = getattr(ng, 'alan', '-') if hasattr(ng, 'alan') else '-'
                    st.markdown(f"- **{gun}** | Alan: {alan}")
    else:
        st.info("Nobet kaydi bulunamadi.")

    # ===== 11. ZIMMET (DEMIRBAS & TUKETIM) =====
    styled_section("Zimmet & Demirbas", "#d97706")
    zimmetler = data.get("zimmetler", [])
    tuketim_z = data.get("tuketim_zimmetleri", [])
    aktif_z = [z for z in zimmetler if z.get("durum") == "Aktif"]
    iade_z = [z for z in zimmetler if z.get("durum") == "İade Edildi"]
    aktif_tz = [z for z in tuketim_z if z.get("durum") == "Aktif"]

    if zimmetler or tuketim_z:
        z1, z2, z3 = st.columns(3)
        with z1:
            st.metric("Aktif Demirbas Zimmet", len(aktif_z))
        with z2:
            st.metric("Iade Edilen", len(iade_z))
        with z3:
            st.metric("Tuketim Zimmet", len(aktif_tz))

        if aktif_z:
            with st.expander("Aktif Demirbas Zimmetleri"):
                for z in aktif_z:
                    st.markdown(
                        f"- **{z.get('demirbas_adi', '-')}** | Kod: {z.get('zimmet_kodu', '-')} | "
                        f"Tarih: {z.get('zimmet_tarihi', '-')}"
                    )
        if aktif_tz:
            with st.expander("Aktif Tuketim Zimmetleri"):
                for z in aktif_tz:
                    st.markdown(
                        f"- **{z.get('urun_adi', '-')}** | Miktar: {z.get('miktar', '-')} | "
                        f"Tarih: {z.get('zimmet_tarihi', '-')}"
                    )
    else:
        st.info("Zimmet kaydi bulunamadi.")

    # ===== 12. OFFBOARDING =====
    offboarding = data.get("offboarding", [])
    if offboarding:
        styled_section("Ayrilma / Offboarding", "#ef4444")
        for ob in offboarding:
            st.markdown(
                f"- **Ayrilma Tarihi:** {ob.get('exit_date', '-')} | "
                f"Sekli: {ob.get('exit_type', '-')} | "
                f"Nedeni: {ob.get('reason', '-')} | "
                f"Durum: {ob.get('status', '-')}"
            )


def _generate_personel_bilgi_karti_pdf(data: dict) -> bytes | None:
    """Personel Bilgi Karti PDF olusturur."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm, mm
        from reportlab.pdfgen import canvas as pdf_canvas
        from reportlab.lib.colors import HexColor
        from utils.shared_data import ensure_turkish_pdf_fonts

        font_name, font_bold = ensure_turkish_pdf_fonts()

        buf = io.BytesIO()
        w, h = A4
        c = pdf_canvas.Canvas(buf, pagesize=A4)
        margin = 2 * cm
        y = h - margin
        col_w = w - 2 * margin

        NAVY = HexColor("#0B0F19")
        BLUE = HexColor("#2563eb")
        LIGHT_BG = HexColor("#0B0F19")
        DARK_TEXT = HexColor("#94A3B8")
        GRAY = HexColor("#64748b")
        WHITE = HexColor("#ffffff")
        GREEN = HexColor("#10b981")
        RED = HexColor("#ef4444")
        GOLD = HexColor("#d97706")
        page_num = [1]

        emp = data["employee"]
        tam_ad = data["tam_ad"]

        def _draw_footer():
            c.setFont(font_name, 7)
            c.setFillColor(GRAY)
            c.drawString(margin, 1.2 * cm, f"Personel Bilgi Karti - {tam_ad}")
            c.drawRightString(w - margin, 1.2 * cm, f"Sayfa {page_num[0]} | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            c.setStrokeColor(HexColor("#e2e8f0"))
            c.line(margin, 1.5 * cm, w - margin, 1.5 * cm)

        def _new_page():
            _draw_footer()
            c.showPage()
            page_num[0] += 1
            return h - margin

        def _check_space(needed, current_y):
            if current_y - needed < 2.5 * cm:
                return _new_page()
            return current_y

        def _section_title(title, current_y, color=BLUE):
            current_y = _check_space(1.5 * cm, current_y)
            current_y -= 0.4 * cm
            c.setFillColor(color)
            c.roundRect(margin, current_y - 0.5 * cm, col_w, 0.7 * cm, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(font_bold, 10)
            c.drawString(margin + 0.4 * cm, current_y - 0.3 * cm, title)
            current_y -= 0.9 * cm
            return current_y

        def _text_line(label, value, current_y, indent=0):
            current_y = _check_space(0.5 * cm, current_y)
            x = margin + indent
            c.setFont(font_bold, 8)
            c.setFillColor(DARK_TEXT)
            c.drawString(x, current_y, f"{label}:")
            c.setFont(font_name, 8)
            c.setFillColor(GRAY)
            val_str = str(value) if value else "-"
            if len(val_str) > 90:
                val_str = val_str[:87] + "..."
            c.drawString(x + 4.5 * cm, current_y, val_str)
            current_y -= 0.45 * cm
            return current_y

        def _bullet_line(text, current_y, indent=0.3 * cm):
            current_y = _check_space(0.5 * cm, current_y)
            c.setFont(font_name, 7.5)
            c.setFillColor(DARK_TEXT)
            c.drawString(margin + indent, current_y, f"  {text[:120]}")
            current_y -= 0.4 * cm
            return current_y

        # ===== HEADER =====
        c.setFillColor(NAVY)
        c.roundRect(margin, y - 2.2 * cm, col_w, 2.4 * cm, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(font_bold, 16)
        c.drawString(margin + 0.6 * cm, y - 0.7 * cm, "PERSONEL BILGI KARTI")
        c.setFont(font_name, 10)
        c.drawString(margin + 0.6 * cm, y - 1.3 * cm, tam_ad)
        c.setFont(font_name, 8)
        c.setFillColor(HexColor("#94a3b8"))
        c.drawString(margin + 0.6 * cm, y - 1.8 * cm, f"{emp.get('position_name', '')} | {emp.get('employee_code', '')} | {emp.get('status', '')}")
        c.drawRightString(w - margin - 0.5 * cm, y - 0.7 * cm, datetime.now().strftime("%d.%m.%Y"))
        y -= 3 * cm

        # ===== 1. KIMLIK =====
        y = _section_title("KIMLIK & TEMEL BILGILER", y, NAVY)
        y = _text_line("Ad Soyad", tam_ad, y)
        y = _text_line("TC Kimlik No", emp.get("tc_no"), y)
        y = _text_line("Personel Kodu", emp.get("employee_code"), y)
        y = _text_line("Brans", emp.get("brans"), y)
        y = _text_line("Pozisyon", emp.get("position_name"), y)
        y = _text_line("Rol Kapsami", emp.get("role_scope"), y)
        y = _text_line("Kampus", emp.get("kampus"), y)
        y = _text_line("Kademe", emp.get("kademe"), y)
        y = _text_line("Ise Baslama", emp.get("ise_baslama_tarihi"), y)
        y = _text_line("Kidem", _calc_kidem(emp.get("ise_baslama_tarihi", "")), y)
        y = _text_line("Telefon", emp.get("telefon"), y)
        y = _text_line("Email", emp.get("email"), y)

        cand = data.get("candidate")
        if cand:
            y -= 0.2 * cm
            y = _text_line("Basvuru Tarihi", cand.get("basvuru_tarihi"), y, indent=0.3 * cm)
            y = _text_line("Kaynak", cand.get("kaynak"), y, indent=0.3 * cm)

        # ===== 2. MULAKAT =====
        ivs = data.get("interviews", [])
        if ivs:
            y = _section_title("MULAKAT GECMISI", y, HexColor("#8b5cf6"))
            for iv in ivs:
                y = _bullet_line(
                    f"{iv.get('interview_date', '-')} | {iv.get('interview_type', '-')} | "
                    f"Karar: {iv.get('decision', '-')} | Puan: {iv.get('overall_score', '-')}", y)

        # ===== 3. PERFORMANS =====
        reviews = data.get("performance_reviews", [])
        if reviews:
            y = _section_title("PERFORMANS DEGERLENDIRMELERI", y, GREEN)
            for rv in sorted(reviews, key=lambda x: x.get("created_at", ""), reverse=True)[:10]:
                period = rv.get("period_label", rv.get("period_type", "-"))
                score = rv.get("overall_score", rv.get("puan", "-"))
                y = _bullet_line(
                    f"{period} | Puan: {score} | Degerlendiren: {rv.get('reviewer_name', '-')} | "
                    f"{rv.get('created_at', '-')[:10]}", y)

        # ===== 4. IZINLER =====
        izinler = data.get("izinler", [])
        if izinler:
            y = _section_title("IZIN BILGILERI", y, HexColor("#0d9488"))
            toplam_gun = sum(iz.get("gun_sayisi", 0) or 0 for iz in izinler)
            y = _text_line("Toplam Izin", f"{toplam_gun} gun ({len(izinler)} kayit)", y)
            for iz in sorted(izinler, key=lambda x: x.get("baslangic_tarihi", ""), reverse=True)[:15]:
                y = _bullet_line(
                    f"{iz.get('baslangic_tarihi', '-')} - {iz.get('bitis_tarihi', '-')} | "
                    f"{iz.get('izin_tipi', '-')} | {iz.get('gun_sayisi', '-')} gun | {iz.get('durum', '-')}", y)

        # ===== 5. RAPORLAR =====
        raporlar = data.get("raporlar", [])
        if raporlar:
            y = _section_title("SAGLIK RAPORLARI", y, RED)
            toplam_rg = sum(r.get("gun_sayisi", 0) or 0 for r in raporlar)
            y = _text_line("Toplam Rapor", f"{len(raporlar)} adet, {toplam_rg} gun", y)
            for rp in sorted(raporlar, key=lambda x: x.get("baslangic_tarihi", ""), reverse=True)[:10]:
                y = _bullet_line(
                    f"{rp.get('baslangic_tarihi', '-')} - {rp.get('bitis_tarihi', '-')} | "
                    f"{rp.get('rapor_turu', '-')} | {rp.get('gun_sayisi', '-')} gun | {rp.get('veren_kurum', '-')}", y)

        # ===== 5b. DEVAMSIZLIK =====
        devamsizlik_pdf = data.get("devamsizlik", [])
        if devamsizlik_pdf:
            y = _section_title("DEVAMSIZLIK KAYITLARI", y, HexColor("#dc2626"))
            mazeretsiz_pdf = len([d for d in devamsizlik_pdf if d.get("tur") == "mazeretsiz"])
            toplam_d_gun = sum(d.get("gun_sayisi", 0) or 0 for d in devamsizlik_pdf)
            y = _text_line("Toplam", f"{len(devamsizlik_pdf)} kayit, {toplam_d_gun} gun (Mazeretsiz: {mazeretsiz_pdf})", y)
            for dv in sorted(devamsizlik_pdf, key=lambda x: x.get("tarih", ""), reverse=True)[:10]:
                y = _bullet_line(
                    f"{dv.get('tarih', '-')} | {dv.get('tur', '-')} | {dv.get('gun_sayisi', 1)} gun | "
                    f"Gerekce: {dv.get('gerekce', '-')[:60]}", y)

        # ===== 5c. GEC KALMA =====
        gk_pdf = data.get("gec_kalma", [])
        if gk_pdf:
            y = _section_title("GEC KALMA KAYITLARI", y, HexColor("#f59e0b"))
            t_gk_dk = sum(g.get("gec_kalma_dk", 0) or 0 for g in gk_pdf)
            y = _text_line("Toplam", f"{len(gk_pdf)} kez, {t_gk_dk} dakika", y)
            for gk in sorted(gk_pdf, key=lambda x: x.get("tarih", ""), reverse=True)[:15]:
                y = _bullet_line(
                    f"{gk.get('tarih', '-')} | Mesai: {gk.get('mesai_baslangic', '-')} | "
                    f"Giris: {gk.get('giris_saati', '-')} | {gk.get('gec_kalma_dk', 0)} dk | {gk.get('kaynak', 'Manuel')}", y)

        # ===== 6. DISIPLIN =====
        disiplin = data.get("disiplin", [])
        if disiplin:
            y = _section_title("DISIPLIN ISLEMLERI", y, HexColor("#f59e0b"))
            for ds in sorted(disiplin, key=lambda x: x.get("tarih", ""), reverse=True)[:10]:
                y = _bullet_line(
                    f"{ds.get('tarih', '-')} | {ds.get('islem_turu', '-')} | {ds.get('aciklama', '-')[:80]}", y)

        # ===== 7. EGITIM =====
        egitimler = data.get("egitimler", [])
        if egitimler:
            y = _section_title("EGITIM & SERTIFIKALAR", y, HexColor("#8b5cf6"))
            for eg in egitimler[:15]:
                y = _bullet_line(
                    f"{eg.get('egitim_adi', '-')} | {eg.get('egitim_turu', '-')} | "
                    f"{eg.get('tarih', '-')} | {eg.get('sure_saat', '-')} saat | {eg.get('durum', '-')}", y)

        # ===== 8. MAAS =====
        bordro = data.get("bordro", [])
        if bordro:
            y = _section_title("MAAS & BORDRO", y, HexColor("#059669"))
            son = sorted(bordro, key=lambda x: x.get("donem", ""), reverse=True)
            if son:
                y = _text_line("Son Donem", son[0].get("donem"), y)
                y = _text_line("Brut Maas", f"{son[0].get('brut_maas', '-')} TL", y)
                y = _text_line("Net Maas", f"{son[0].get('net_maas', '-')} TL", y)

        # ===== 9. DERS PROGRAMI =====
        schedule = data.get("schedule", [])
        if schedule:
            y = _section_title("HAFTALIK DERS PROGRAMI", y, BLUE)
            y = _text_line("Haftalik Ders Saati", str(len(schedule)), y)
            gunler = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]
            for gun in gunler:
                dersler = []
                for slot in schedule:
                    sg = getattr(slot, 'gun', '') if hasattr(slot, 'gun') else slot.get('gun', '') if isinstance(slot, dict) else ''
                    if sg == gun:
                        ders = getattr(slot, 'ders', '') if hasattr(slot, 'ders') else slot.get('ders', '') if isinstance(slot, dict) else ''
                        saat = getattr(slot, 'saat', '') if hasattr(slot, 'saat') else slot.get('saat', '') if isinstance(slot, dict) else ''
                        sinif = getattr(slot, 'sinif', '') if hasattr(slot, 'sinif') else slot.get('sinif', '') if isinstance(slot, dict) else ''
                        sube = getattr(slot, 'sube', '') if hasattr(slot, 'sube') else slot.get('sube', '') if isinstance(slot, dict) else ''
                        dersler.append(f"{saat}.saat {ders}({sinif}/{sube})")
                if dersler:
                    y = _bullet_line(f"{gun}: {', '.join(dersler)}", y)

        # ===== 10. NOBET =====
        nobet_g = data.get("nobet_gorevler", [])
        nobet_k = data.get("nobet_kayitlar", [])
        if nobet_g or nobet_k:
            y = _section_title("NOBET BILGILERI", y, HexColor("#64748b"))
            y = _text_line("Nobet Gorevi", f"{len(nobet_g)} adet", y)
            y = _text_line("Tutulan Nobet", f"{len(nobet_k)} adet", y)
            for ng in nobet_g[:10]:
                gun = getattr(ng, 'gun', '-') if hasattr(ng, 'gun') else '-'
                alan = getattr(ng, 'alan', '-') if hasattr(ng, 'alan') else '-'
                y = _bullet_line(f"{gun} | Alan: {alan}", y)

        # ===== 11. ZIMMET =====
        zimmetler = data.get("zimmetler", [])
        tuketim_z = data.get("tuketim_zimmetleri", [])
        if zimmetler or tuketim_z:
            y = _section_title("ZIMMET & DEMIRBAS", y, GOLD)
            aktif_z = [z for z in zimmetler if z.get("durum") == "Aktif"]
            y = _text_line("Aktif Demirbas", str(len(aktif_z)), y)
            y = _text_line("Tuketim Zimmet", str(len([z for z in tuketim_z if z.get("durum") == "Aktif"])), y)
            for z in aktif_z[:15]:
                y = _bullet_line(
                    f"{z.get('demirbas_adi', '-')} | {z.get('zimmet_kodu', '-')} | {z.get('zimmet_tarihi', '-')}", y)

        # ===== 12. OFFBOARDING =====
        offboarding = data.get("offboarding", [])
        if offboarding:
            y = _section_title("AYRILMA / OFFBOARDING", y, RED)
            for ob in offboarding[:5]:
                y = _bullet_line(
                    f"Tarih: {ob.get('exit_date', '-')} | {ob.get('exit_type', '-')} | "
                    f"Neden: {ob.get('reason', '-')[:60]}", y)

        _draw_footer()
        c.save()
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"PDF olusturma hatasi: {e}")
        return None


# ============================================================
# SEKME 11: RAPORLAR
# ============================================================

def _render_raporlar(store: IKDataStore):
    sub = st.tabs(["📊 Genel Özet", "🔍 Aday & Mülakat", "⭐ Performans", "👥 Personel & İzin", "📝 Audit Log"])

    # ---- Genel Özet ----
    with sub[0]:
        styled_section("Genel Özet", "#1e40af")
        candidates = store.load_list("candidates")
        employees = store.load_list("employees")
        interviews = store.load_list("interviews")
        reviews = store.load_list("performance_reviews")
        izinler_all = store.load_list("izinler")

        aktif_emp = sum(1 for e in employees if e.get("status") == "Aktif")
        ayrilan_emp = sum(1 for e in employees if e.get("status") == "Ayrildi")

        styled_stat_row([
            ("Toplam Aday", len(candidates), "#2563eb", "\U0001f464"),
            ("Toplam Mulakat", len(interviews), "#8b5cf6", "\U0001f3a4"),
            ("Aktif Çalışan", aktif_emp, "#10b981", "\U0001f465"),
            ("Değerlendirme", len(reviews), "#f59e0b", "\U0001f4c8"),
        ])
        st.markdown("<br>", unsafe_allow_html=True)

        # Sunburst: Genel IK Dagilimi
        ik_inner: dict[str, float] = {
            "Adaylar": float(len(candidates)),
            "Aktif Çalışanlar": float(aktif_emp),
            "Ayrilanlar": float(ayrilan_emp) if ayrilan_emp > 0 else 0,
            "Mulakatlar": float(len(interviews)),
        }
        ik_outer: dict[str, list[tuple[str, float]]] = {}

        # Aday durumlari
        if candidates:
            aday_durumlar: list[tuple[str, float]] = []
            aday_st: dict[str, int] = {}
            for cd in candidates:
                s = cd.get("status", "Yeni")
                aday_st[s] = aday_st.get(s, 0) + 1
            for s, cnt in aday_st.items():
                aday_durumlar.append((s, float(cnt)))
            ik_outer["Adaylar"] = aday_durumlar

        # Calisan rolleri
        if employees:
            rol_items: list[tuple[str, float]] = []
            rol_cnt: dict[str, int] = {}
            for e in employees:
                if e.get("status") == "Aktif":
                    rs = e.get("role_scope", "ALL")
                    rol_cnt[rs] = rol_cnt.get(rs, 0) + 1
            for rs, cnt in rol_cnt.items():
                rol_items.append((rs, float(cnt)))
            ik_outer["Aktif Çalışanlar"] = rol_items

        # Mulakat kararlari
        if interviews:
            mk_items: list[tuple[str, float]] = []
            mk_cnt: dict[str, int] = {}
            for mi in interviews:
                k = mi.get("decision", "") or "Kararsiz"
                mk_cnt[k] = mk_cnt.get(k, 0) + 1
            for k, cnt in mk_cnt.items():
                mk_items.append((k, float(cnt)))
            ik_outer["Mulakatlar"] = mk_items

        # Sifir degerleri kaldir
        ik_inner = {k: v for k, v in ik_inner.items() if v > 0}

        if ik_inner:
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    ik_inner, ik_outer, size=400,
                    title="Insan Kaynaklari Genel Dagilim"
                ),
                unsafe_allow_html=True
            )

    # ---- Aday & Mülakat ----
    with sub[1]:
        styled_section("Aday & Mülakat Raporu", "#2563eb")
        candidates = store.load_list("candidates")

        if candidates:
            rap_c1, rap_c2 = st.columns(2)

            with rap_c1:
                styled_section("Aday Durum Dagilimi", "#4472C4")
                status_counts: dict[str, float] = {}
                for cd in candidates:
                    s = cd.get("status", "Yeni")
                    status_counts[s] = status_counts.get(s, 0) + 1
                st.markdown(
                    ReportStyler.horizontal_bar_html(status_counts, color="#4472C4"),
                    unsafe_allow_html=True
                )

            with rap_c2:
                styled_section("Aday Durum Orani", "#264478")
                st.markdown(
                    ReportStyler.donut_chart_svg(status_counts, size=155),
                    unsafe_allow_html=True
                )
        else:
            styled_info_banner("Aday verisi yok.", "info")

        interviews = store.load_list("interviews")
        if interviews:
            styled_section("Mülakat Karar Dagilimi", "#8b5cf6")
            mk_c1, mk_c2 = st.columns(2)
            karar_counts: dict[str, float] = {}
            for mi in interviews:
                k = mi.get("decision", "") or "Kararsiz"
                karar_counts[k] = karar_counts.get(k, 0) + 1

            with mk_c1:
                st.markdown(
                    ReportStyler.donut_chart_svg(karar_counts, size=155),
                    unsafe_allow_html=True
                )
            with mk_c2:
                st.markdown(
                    ReportStyler.horizontal_bar_html(karar_counts, color="#8b5cf6"),
                    unsafe_allow_html=True
                )

            # Sunburst: Karar (ic) -> Adaylar (dis)
            styled_section("Mulakat Sonuc Sunburst", "#264478")
            mk_inner: dict[str, float] = {}
            mk_outer_data: dict[str, list[tuple[str, float]]] = {}
            for mi in interviews:
                k = mi.get("decision", "") or "Kararsiz"
                mk_inner[k] = mk_inner.get(k, 0) + 1
                cname = mi.get("candidate_code", "") or mi.get("interview_code", "?")
                mk_outer_data.setdefault(k, []).append((cname, 1))
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    mk_inner, mk_outer_data, size=380,
                    title="Mülakat Karar Detay"
                ),
                unsafe_allow_html=True
            )

    # ---- Performans ----
    with sub[2]:
        styled_section("Performans Raporu", "#8b5cf6")
        reviews = store.load_objects("performance_reviews")
        if reviews:
            avg_score = sum(r.score_100 for r in reviews) / len(reviews)
            styled_stat_row([
                ("Değerlendirme", len(reviews), "#2563eb", "\U0001f4c8"),
                ("Genel Ort.", round(avg_score, 1), "#4472C4", "\U0001f4ca"),
                ("En Yuksek", max(r.score_100 for r in reviews), "#10b981", "\u2B50"),
                ("En Dusuk", min(r.score_100 for r in reviews), "#ef4444", "\U0001f4c9"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            pr_c1, pr_c2 = st.columns(2)
            with pr_c1:
                styled_section("Etiket Dagilimi", "#4472C4")
                lbl_counts: dict[str, float] = {}
                for r in reviews:
                    lbl_counts[r.label] = lbl_counts.get(r.label, 0) + 1
                st.markdown(
                    ReportStyler.donut_chart_svg(
                        {k: float(v) for k, v in lbl_counts.items()}, size=155
                    ),
                    unsafe_allow_html=True
                )

            with pr_c2:
                styled_section("Çalışan Skorlari", "#264478")
                calisan_skor = {r.employee_name: r.score_100 for r in reviews}
                st.markdown(
                    ReportStyler.horizontal_bar_html(calisan_skor, color="#4472C4"),
                    unsafe_allow_html=True
                )

            # Sunburst: Role Scope (ic) -> Calisanlar (dis)
            styled_section("Role Scope Performans Sunburst", "#264478")
            rs_inner: dict[str, float] = {}
            rs_outer: dict[str, list[tuple[str, float]]] = {}
            for r in reviews:
                rs_inner[r.role_scope] = rs_inner.get(r.role_scope, 0) + 1
                rs_outer.setdefault(r.role_scope, []).append((r.employee_name, r.score_100))
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    rs_inner, rs_outer, size=380,
                    title="Role Scope Bazli Performans"
                ),
                unsafe_allow_html=True
            )

            styled_section("Detay Tablosu", "#64748b")
            df = pd.DataFrame([{
                "Çalışan": r.employee_name,
                "Periyot": PERFORMANCE_PERIOD_LABELS.get(r.period_type, r.period_type),
                "Skor": r.score_100,
                "Etiket": r.label,
                "Scope": r.role_scope,
            } for r in reviews])
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Performans verisi yok.", "info")

    # ---- Personel & İzin ----
    with sub[3]:
        styled_section("Personel & İzin Raporu", "#f59e0b")
        staff = _get_personel_options()
        izinler = store.load_list("izinler")

        if staff:
            pi_c1, pi_c2 = st.columns(2)
            cat_counts: dict[str, float] = {}
            cat_persons: dict[str, list[tuple[str, float]]] = {}
            for s in staff:
                cat = KATEGORI_MAP.get(s.get("category", "diger"), ("Diger", ""))[0]
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
                pname = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or "?"
                cat_persons.setdefault(cat, []).append((pname, 1))

            with pi_c1:
                styled_section("Kategori Dagilimi", "#4472C4")
                st.markdown(
                    ReportStyler.horizontal_bar_html(cat_counts, color="#4472C4"),
                    unsafe_allow_html=True
                )
            with pi_c2:
                styled_section("Kategori Orani", "#264478")
                st.markdown(
                    ReportStyler.donut_chart_svg(cat_counts, size=155),
                    unsafe_allow_html=True
                )

            # Personel Sunburst
            styled_section("Personel Sunburst", "#264478")
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    cat_counts, cat_persons, size=380,
                    title="Personel Kategori Dagilimi"
                ),
                unsafe_allow_html=True
            )

        if izinler:
            styled_section("İzin İstatistikleri", "#0d9488")
            onay_cnt = sum(1 for i in izinler if i.get("durum") == "onaylandi")
            red_cnt = sum(1 for i in izinler if i.get("durum") == "reddedildi")
            bek_cnt = sum(1 for i in izinler if i.get("durum") == "beklemede")

            styled_stat_row([
                ("Toplam Talep", len(izinler), "#2563eb", "\U0001f4cb"),
                ("Onaylanan", onay_cnt, "#10b981", "\u2705"),
                ("Reddedilen", red_cnt, "#ef4444", "\u274c"),
                ("Bekleyen", bek_cnt, "#f59e0b", "\u23f3"),
            ])
            st.markdown("<br>", unsafe_allow_html=True)

            iz_c1, iz_c2 = st.columns(2)
            with iz_c1:
                styled_section("İzin Durum Dagilimi", "#4472C4")
                izin_durum: dict[str, float] = {}
                for i in izinler:
                    d = i.get("durum", "?")
                    izin_durum[d] = izin_durum.get(d, 0) + 1
                st.markdown(
                    ReportStyler.donut_chart_svg(izin_durum, size=155),
                    unsafe_allow_html=True
                )
            with iz_c2:
                styled_section("İzin Tipi Dagilimi", "#264478")
                izin_tip: dict[str, float] = {}
                for i in izinler:
                    t = i.get("izin_tipi", "?")
                    tip_label = IZIN_TIPLERI.get(t, t)
                    izin_tip[tip_label] = izin_tip.get(tip_label, 0) + 1
                st.markdown(
                    ReportStyler.horizontal_bar_html(izin_tip, color="#ED7D31"),
                    unsafe_allow_html=True
                )

    # ---- Audit Log ----
    with sub[4]:
        styled_section("Audit Log", "#64748b")
        logs = store.load_list("audit_log")
        if logs:
            c1, c2 = st.columns(2)
            with c1:
                aksiyon_f = st.text_input("Aksiyon Filtre", key="ik_rap_log_aksiyon")
            with c2:
                limit = st.number_input("Son N kayit", min_value=10, max_value=500, value=50, key="ik_rap_log_limit")

            filtered = logs
            if aksiyon_f:
                filtered = [l for l in filtered if aksiyon_f.lower() in l.get("action", "").lower()]
            filtered = sorted(filtered, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]

            # Aksiyon dagilimi grafik
            aksiyon_counts: dict[str, float] = {}
            for l in logs:
                a = l.get("action", "?")
                aksiyon_counts[a] = aksiyon_counts.get(a, 0) + 1
            if aksiyon_counts:
                styled_section("Aksiyon Dagilimi", "#4472C4")
                st.markdown(
                    ReportStyler.horizontal_bar_html(
                        dict(sorted(aksiyon_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
                        color="#4472C4"
                    ),
                    unsafe_allow_html=True
                )

            styled_section("Log Detay", "#64748b")
            df = pd.DataFrame([{
                "Zaman": l.get("timestamp", "")[:19],
                "Aksiyon": l.get("action", ""),
                "Entity": l.get("entity_type", ""),
                "Detay": l.get("entity_label", ""),
                "Kullanıcı": l.get("user_name", ""),
            } for l in filtered])
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Audit log kaydi yok.", "info")

    # ================================================================
    # PERFORMANS KARSILASTIRMA + AI ONERILERI + KUNYE + PDF
    # ================================================================
    from utils.report_utils import (ai_recommendations_html, period_comparison_row_html,
                                     generate_module_pdf, render_pdf_download_button,
                                     render_report_kunye_html, ReportStyler as _RS)

    st.markdown(_RS.section_divider_html("Dönemsel Performans Karşılaştırma", "#0d9488"), unsafe_allow_html=True)

    from datetime import datetime as _dt, timedelta as _td
    _now = _dt.now()
    _cur_month = _now.strftime("%Y-%m")
    _prev_month = (_now.replace(day=1) - _td(days=1)).strftime("%Y-%m")

    try:
        _ik_candidates = store.load_list("candidates")
        _ik_employees = store.load_list("employees")
        _ik_interviews = store.load_list("interviews")
        _ik_reviews = store.load_list("performance_reviews")
        _ik_izinler = store.load_list("izinler")
        _ik_egitimler = store.load_list("egitimler")
    except Exception:
        _ik_candidates, _ik_employees, _ik_interviews = [], [], []
        _ik_reviews, _ik_izinler, _ik_egitimler = [], [], []

    def _ik_count_by_month(records, month_str, date_fields=("created_at", "basvuru_tarihi", "ise_baslama_tarihi")):
        c = 0
        for r in records:
            for df in date_fields:
                val = r.get(df, "")
                if val and val[:7] == month_str:
                    c += 1
                    break
        return c

    _ik_comparisons = [
        {"label": "Yeni Adaylar", "current": _ik_count_by_month(_ik_candidates, _cur_month), "previous": _ik_count_by_month(_ik_candidates, _prev_month)},
        {"label": "Mulakatlar", "current": _ik_count_by_month(_ik_interviews, _cur_month), "previous": _ik_count_by_month(_ik_interviews, _prev_month)},
        {"label": "Değerlendirmeler", "current": _ik_count_by_month(_ik_reviews, _cur_month), "previous": _ik_count_by_month(_ik_reviews, _prev_month)},
        {"label": "İzin Talepleri", "current": _ik_count_by_month(_ik_izinler, _cur_month), "previous": _ik_count_by_month(_ik_izinler, _prev_month)},
    ]
    st.markdown(period_comparison_row_html(_ik_comparisons), unsafe_allow_html=True)

    # ---- AI Onerileri ----
    _ik_insights = []

    _aktif_emp = sum(1 for e in _ik_employees if e.get("status") == "Aktif")
    _ayrilan_emp = sum(1 for e in _ik_employees if e.get("status") == "Ayrildi")
    _toplam_emp = len(_ik_employees)
    _turnover = round((_ayrilan_emp / _toplam_emp) * 100, 1) if _toplam_emp > 0 else 0
    _pending_reviews = sum(1 for rv in _ik_reviews if rv.get("status") in ("Beklemede", "Taslak", "pending"))
    _pending_candidates = sum(1 for c in _ik_candidates if c.get("status") in ("Yeni", "Basvurdu", "new"))
    _tamamlanan_egitim = sum(1 for eg in _ik_egitimler if eg.get("durum") in ("Tamamlandı", "tamamlandı"))
    _toplam_egitim = len(_ik_egitimler)
    _egitim_rate = round((_tamamlanan_egitim / _toplam_egitim) * 100, 1) if _toplam_egitim > 0 else 0

    if _turnover > 15:
        _ik_insights.append({
            "icon": "\u26a0\ufe0f", "title": "Yuksek Personel Devir Orani",
            "text": f"Personel devir orani %{_turnover:.0f} seviyesinde. Çıkış mulakatlari analiz edilerek elde tutma stratejileri gelistirilmesi onerilir.",
            "color": "#ef4444"
        })

    if _pending_reviews > 3:
        _ik_insights.append({
            "icon": "\U0001f4cb", "title": "Bekleyen Değerlendirmeler",
            "text": f"{_pending_reviews} adet performans degerlendirmesi beklemede. Zamaninda tamamlanmasi için yoneticilere hatirlatma gonderilmesi onerilir.",
            "color": "#f59e0b"
        })

    if _pending_candidates > 5:
        _ik_insights.append({
            "icon": "\U0001f464", "title": "Ise Alim Boru Hatti Yogunlugu",
            "text": f"{_pending_candidates} aday islenmemis durumda. Mulakat surecinin hizlandirilmasi ve eleme kriterlerinin gozden gecirilmesi onerilir.",
            "color": "#ea580c"
        })

    if _toplam_egitim > 0 and _egitim_rate < 60:
        _ik_insights.append({
            "icon": "\U0001f393", "title": "Egitim Tamamlanma Orani Dusuk",
            "text": f"Egitim tamamlanma orani %{_egitim_rate:.0f}. Personel gelisim planlarinin guncellenmesi ve zorunlu egitimlerin takip edilmesi onerilir.",
            "color": "#8b5cf6"
        })

    _ik_insights.append({
        "icon": "\U0001f4a1", "title": "Genel Oneri",
        "text": f"Aktif calisan: {_aktif_emp}, Ayrilan: {_ayrilan_emp}, Toplam aday: {len(_ik_candidates)}. Duzenli IK raporlamasi ve stratejik is gucunu planlama calismalarina devam edilmesi onerilir.",
        "color": "#2563eb"
    })

    _ik_insights.append({
        "icon": "\U0001f4c8", "title": "Performans Takibi",
        "text": "Yil sonu performans degerlendirme donemi için hedef belirleme ve ara degerlendirme surecleri planlanmalidir.",
        "color": "#0d9488"
    })

    st.markdown(ai_recommendations_html(_ik_insights), unsafe_allow_html=True)

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(_RS.section_divider_html("IK Genel PDF Raporu", "#1e40af"), unsafe_allow_html=True)
    if st.button("\U0001f4e5 Insan Kaynaklari Raporu Oluştur (PDF)", key="iky_full_pdf_btn", use_container_width=True):
        try:
            _sections = [
                {
                    "title": "IK Genel İstatistikler",
                    "metrics": [
                        ("Aktif Çalışan", _aktif_emp, "#10b981"),
                        ("Ayrilan", _ayrilan_emp, "#ef4444"),
                        ("Toplam Aday", len(_ik_candidates), "#2563eb"),
                        ("Mulakat", len(_ik_interviews), "#8b5cf6"),
                    ],
                    "text": f"Devir Orani: %{_turnover:.0f} | Egitim Tamamlanma: %{_egitim_rate:.0f} | Bekleyen Değerlendirme: {_pending_reviews}",
                },
                {
                    "title": "Dönemsel Karşılaştırma",
                    "text": " | ".join([f"{c['label']}: {c['current']} (onceki: {c['previous']})" for c in _ik_comparisons]),
                },
            ]
            _pdf_bytes = generate_module_pdf("Insan Kaynaklari Yönetimi Raporu", _sections)
            render_pdf_download_button(_pdf_bytes, "ik_raporu.pdf", "IK Raporu Indir", "iky_full_dl")
        except Exception as _e:
            st.error(f"PDF olusturulurken hata: {_e}")


# ============================================================
# SEKME 12: AYARLAR (STUB)
# ============================================================

def _render_ayarlar(store: IKDataStore):
    sub = st.tabs(["⚙️ Genel Ayarlar", "💼 Pozisyonlar", "❓ Soru Setleri", "📄 Evrak Şablonları",
                    "📊 Performans Kriterleri", "📥 CSV Import"])

    # ---- Genel Ayarlar ----
    with sub[0]:
        styled_section("Genel Ayarlar", "#2563eb")
        settings = store.get_settings()

        c1, c2 = st.columns(2)
        with c1:
            int_count = st.number_input("Zorunlu Mulakat Sayısı", 1, 3, settings.interview_count_required, key="ik_ay_int_count")
            int_3_opt = st.checkbox("3. Mülakat Opsiyonel", settings.interview_3_optional, key="ik_ay_int3")
            gen_set = st.text_input("Genel Soru Seti Kodu", settings.default_general_set_code, key="ik_ay_gen_set")
            fallback = st.selectbox("Soru Seti Fallback", ["CATEGORY", "POSITION"],
                                    index=0 if settings.default_position_set_fallback == "CATEGORY" else 1, key="ik_ay_fb")
        with c2:
            core_w = st.number_input("CORE Agirlik", 0.0, 1.0, settings.performance_core_weight, 0.05, key="ik_ay_core_w")
            role_w = st.number_input("ROLE Agirlik", 0.0, 1.0, settings.performance_role_weight, 0.05, key="ik_ay_role_w")
            mult = st.number_input("Skor 100 Carpan", 1, 100, settings.performance_score_to_100_multiplier, key="ik_ay_mult")
            note_req = st.checkbox("Yonetici Notu Zorunlu", settings.performance_general_note_required, key="ik_ay_note_req")

        if st.button("Ayarlari Kaydet", type="primary", key="ik_ay_kaydet"):
            settings.interview_count_required = int_count
            settings.interview_3_optional = int_3_opt
            settings.default_general_set_code = gen_set
            settings.default_position_set_fallback = fallback
            settings.performance_core_weight = core_w
            settings.performance_role_weight = role_w
            settings.performance_score_to_100_multiplier = mult
            settings.performance_general_note_required = note_req
            store.save_settings(settings)
            AuditLogger.log(store, "ayar_degistirildi", "settings", "ik_settings", "Genel ayarlar güncellendi")
            styled_info_banner("Ayarlar kaydedildi.", "success")

    # ---- Pozisyonlar ----
    with sub[1]:
        styled_section("Pozisyon Yönetimi", "#8b5cf6")
        positions = store.load_objects("positions")
        if positions:
            df = pd.DataFrame([{
                "Kod": p.position_code, "Pozisyon": p.position_name,
                "Kategori": p.category, "Scope": p.role_scope,
                "Aktif": "Evet" if p.is_active else "Hayir",
            } for p in positions])
            st.dataframe(df, hide_index=True, use_container_width=True)

        styled_section("Yeni Pozisyon Ekle", "#10b981")
        c1, c2 = st.columns(2)
        with c1:
            pos_code = st.text_input("Pozisyon Kodu", key="ik_ay_pos_code")
            pos_name = st.text_input("Pozisyon Adi", key="ik_ay_pos_name")
        with c2:
            pos_cat = st.text_input("Kategori", key="ik_ay_pos_cat")
            pos_scope = st.selectbox("Role Scope", ROLE_SCOPES, key="ik_ay_pos_scope")

        if st.button("Pozisyon Ekle", type="primary", key="ik_ay_pos_btn"):
            if pos_code and pos_name:
                p = Position(position_code=pos_code, position_name=pos_name,
                             category=pos_cat, role_scope=pos_scope)
                store.upsert("positions", p)
                styled_info_banner(f"Pozisyon eklendi: {pos_code}", "success")
                st.rerun()

    # ---- Soru Setleri ----
    with sub[2]:
        styled_section("Soru Setleri", "#0d9488")
        sets = store.load_objects("question_sets")
        questions = store.load_objects("questions")
        if sets:
            df = pd.DataFrame([{
                "Set Kodu": s.set_code, "Set Adi": s.set_name,
                "Tip": s.set_type, "Scope": s.role_scope,
                "Soru Sayısı": s.question_count,
                "Aktif": "Evet" if s.is_active else "Hayir",
            } for s in sets])
            st.dataframe(df, hide_index=True, use_container_width=True)

        if questions:
            styled_section("Soru Listesi", "#2563eb")
            set_filter = st.selectbox("Set Filtre", ["Tümü"] + [s.set_code for s in sets], key="ik_ay_q_filter")
            filtered_q = questions if set_filter == "Tümü" else [q for q in questions if q.set_code == set_filter]
            if filtered_q:
                df_q = pd.DataFrame([{
                    "Kod": q.question_code, "Set": q.set_code,
                    "Sira": q.order_no, "Soru": q.question_text[:60],
                } for q in sorted(filtered_q, key=lambda x: (x.set_code, x.order_no))])
                st.dataframe(df_q, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Soru bulunamadı. CSV Import ile yukleyin.", "info")

    # ---- Evrak Şablonları ----
    with sub[3]:
        styled_section("Evrak Şablonları", "#f59e0b")
        templates = store.load_objects("document_templates")
        if templates:
            df = pd.DataFrame([{
                "Kod": t.document_code, "Evrak": t.document_name,
                "Faz": t.phase, "Scope": t.applies_to_role_scope,
                "Kural": t.required_rule,
            } for t in templates])
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Evrak sablonu yok. CSV Import ile yukleyin.", "info")

    # ---- Performans Kriterleri ----
    with sub[4]:
        styled_section("Performans Kriterleri", "#8b5cf6")
        criteria = store.load_objects("performance_criteria")
        if criteria:
            total_weight = sum(c.weight for c in criteria if c.is_active)
            styled_info_banner(
                f"Toplam {len(criteria)} kriter | Toplam Agirlik: %{total_weight:.0f}", "info")
            df_all = pd.DataFrame([{
                "Kod": c.criterion_code,
                "Kategori": c.category or "-",
                "Kriter": c.criterion_name,
                "Agirlik %": f"%{c.weight:.0f}",
                "Scope": c.role_scope,
                "Aktif": "Evet" if c.is_active else "Hayir",
            } for c in criteria])
            st.dataframe(df_all, hide_index=True, use_container_width=True, height=600)
        else:
            styled_info_banner("Kriter yok. CSV Import ile yukleyin.", "info")

    # ---- CSV Import ----
    with sub[5]:
        styled_section("CSV Import", "#dc2626")
        styled_info_banner("KIM-03 paketindeki CSV dosyalarini import edin. Sira: "
                            "1) Ayarlar, 2) Performans Kriterleri, 3) Evrak Şablonları, "
                            "4) Soru Setleri SETS, 5) Soru QUESTIONS, 6) Pozisyonlar (UAT)", "info")

        import_type = st.selectbox("Import Tipi", [
            "Ayarlar", "Performans Kriterleri", "Evrak Şablonları",
            "Soru Setleri (SETS)", "Soru Satirlari (QUESTIONS)",
            "Pozisyonlar (UAT)", "Adaylar (UAT)", "Basvurular (UAT)",
        ], key="ik_ay_import_type")

        uploaded = st.file_uploader("CSV Dosyasi Yukle", type=["csv"], key="ik_ay_csv_file")

        if uploaded:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded, allowed_types=["csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded = None
        if uploaded and st.button("Import Baslat", type="primary", key="ik_ay_import_btn"):
            try:
                content = uploaded.read().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)
                count = 0

                if import_type == "Ayarlar":
                    settings = store.get_settings()
                    for row in rows:
                        key = row.get("setting_key", "").lower()
                        val = row.get("setting_value", "")
                        if hasattr(settings, key):
                            current = getattr(settings, key)
                            if isinstance(current, bool):
                                setattr(settings, key, val.lower() == "true")
                            elif isinstance(current, int):
                                setattr(settings, key, int(val))
                            elif isinstance(current, float):
                                setattr(settings, key, float(val))
                            else:
                                setattr(settings, key, val)
                            count += 1
                    store.save_settings(settings)

                elif import_type == "Performans Kriterleri":
                    for row in rows:
                        pc = PerformanceCriterion(
                            criterion_code=row.get("criterion_code", ""),
                            criterion_name=row.get("criterion_name", ""),
                            group_type=row.get("group_type", "ROLE"),
                            role_scope=row.get("role_scope", "TEACHER"),
                            category=row.get("category", ""),
                            weight=float(row.get("weight", 1)),
                            is_active=row.get("is_active", "True").lower() == "true",
                            score_min=int(row.get("score_min", 0)),
                            score_max=int(row.get("score_max", 5)),
                            notes_required=row.get("notes_required", "False").lower() == "true",
                        )
                        store.upsert("performance_criteria", pc)
                        count += 1

                elif import_type == "Evrak Şablonları":
                    for row in rows:
                        dt = DocumentTemplate(
                            document_code=row.get("document_code", ""),
                            document_name=row.get("document_name", ""),
                            phase=row.get("phase", "ONBOARDING"),
                            applies_to_role_scope=row.get("applies_to_role_scope", "ALL"),
                            required_rule=row.get("required_rule", "ALWAYS"),
                            condition_key=row.get("condition_key", ""),
                            is_active=row.get("is_active", "True").lower() == "true",
                        )
                        store.upsert("document_templates", dt)
                        count += 1

                elif import_type == "Soru Setleri (SETS)":
                    for row in rows:
                        qs = QuestionSet(
                            set_code=row.get("set_code", ""),
                            set_name=row.get("set_name", ""),
                            set_type=row.get("set_type", "GENERAL"),
                            role_scope=row.get("role_scope", "ALL"),
                            category_scope=row.get("category_scope", "ALL"),
                            question_count=int(row.get("question_count", 0)),
                            is_active=row.get("is_active", "True").lower() == "true",
                        )
                        store.upsert("question_sets", qs)
                        count += 1

                elif import_type == "Soru Satirlari (QUESTIONS)":
                    for row in rows:
                        iq = InterviewQuestion(
                            question_code=row.get("question_code", ""),
                            set_code=row.get("set_code", ""),
                            order_no=int(row.get("order_no", 0)),
                            question_text=row.get("question_text", ""),
                            is_required=row.get("is_required", "True").lower() == "true",
                            score_min=int(row.get("score_min", 0)),
                            score_max=int(row.get("score_max", 5)),
                            note_required=row.get("note_required", "False").lower() == "true",
                        )
                        store.upsert("questions", iq)
                        count += 1

                elif import_type == "Pozisyonlar (UAT)":
                    for row in rows:
                        p = Position(
                            position_code=row.get("position_code", ""),
                            position_name=row.get("position_name", ""),
                            category=row.get("category", ""),
                            role_scope=row.get("role_scope", "ALL"),
                            is_active=row.get("is_active", "True").lower() == "true",
                        )
                        store.upsert("positions", p)
                        count += 1

                elif import_type == "Adaylar (UAT)":
                    for row in rows:
                        c = Candidate(
                            candidate_code=row.get("candidate_code", ""),
                            tc_no=row.get("tc_no", ""),
                            ad=row.get("ad", ""),
                            soyad=row.get("soyad", ""),
                            telefon=row.get("telefon", ""),
                            email=row.get("email", ""),
                            sehir=row.get("sehir", ""),
                            status=row.get("status", "Yeni"),
                        )
                        store.upsert("candidates", c)
                        count += 1

                elif import_type == "Basvurular (UAT)":
                    for row in rows:
                        a = Application(
                            application_code=row.get("application_code", ""),
                            candidate_code=row.get("candidate_code", ""),
                            position_code=row.get("position_code", ""),
                            kampus=row.get("kampus", "TUMU"),
                            kademe=row.get("kademe", "TUMU"),
                            status=row.get("status", "Yeni"),
                        )
                        store.upsert("applications", a)
                        count += 1

                AuditLogger.log(store, "import_yapildi", "csv_import", import_type,
                                f"{count} kayit import edildi")
                styled_info_banner(f"Import tamamlandı: {count} kayit ({import_type})", "success")
                st.rerun()

            except Exception as e:
                st.error(f"Import hatasi: {e}")


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_insan_kaynaklari():
    """İnsan Kaynakları Yönetimi modülü giriş noktası."""
    _inject_ik_css()
    styled_header(
        "Insan Kaynaklari Yönetimi",
        "KIM-03 Ise Alim, Performans ve Personel Yönetim Sistemi",
        "\U0001f465"
    )

    render_smarti_welcome("insan_kaynaklari")

    # Veri dogrulama
    try:
        from utils.ui_common import veri_dogrulama_butonu, veri_dogrulama_sonucu
        _ik_store_vd = _get_ik_store()
        veri_dogrulama_butonu("insan_kaynaklari")
        if st.session_state.get("_veri_kontrol_aktif_insan_kaynaklari"):
            sorunlar = []
            _ik_emp = _ik_store_vd.load_list("employees")
            _ik_aktif = sum(1 for e in _ik_emp if e.get("status") == "Aktif")
            if _ik_aktif == 0:
                sorunlar.append({"tip": "eksik", "alan": "Aktif Calisan", "sayi": 0, "oncelik": "yuksek"})
            _no_email = sum(1 for e in _ik_emp if not e.get("email"))
            if _no_email > 0:
                sorunlar.append({"tip": "eksik", "alan": "Email Eksik Calisan", "sayi": _no_email, "oncelik": "orta"})
            veri_dogrulama_sonucu(sorunlar)
            st.session_state["_veri_kontrol_aktif_insan_kaynaklari"] = False
    except Exception:
        pass

    # -- Tab Gruplama (24 tab -> 4 grup) --
    _GRP_86627 = {
        "📋 Grup A": [("📊 Genel Bakış", 0), ("🔍 Aday Havuzu", 1), ("🎤 Mülakat", 2), ("📋 Onboarding", 3), ("👥 Aktif Çalışanlar", 4), ("⭐ Performans", 5), ("📅 İzin Yönetimi", 6)],
        "📊 Grup B": [("💰 Maaş & Bordro", 7), ("🎓 Eğitim & Sertifika", 8), ("📝 Disiplin", 9), ("🚪 Offboarding", 10), ("📇 Personel Bilgi Kartı", 11), ("📈 IK Raporlar", 12), ("⚙️ Ayarlar", 13)],
        "🔧 Grup C": [("🧩 Yetenek Haritası", 14), ("🔄 360° Feedback", 15), ("🎛️ İK Komuta", 16), ("👤 Dijital İkiz", 17), ("🤖 AI İşe Alım", 18), ("😊 Mutluluk", 19), ("🗺️ Kariyer Yol", 20)],
        "📈 Grup D": [("🏆 Performans Duvarı", 21), ("🎮 HR Simülasyon", 22), ("🤖 Smarti", 23)],
    }
    _sg_86627 = st.radio("", list(_GRP_86627.keys()), horizontal=True, label_visibility="collapsed", key="rg_86627")
    _gt_86627 = _GRP_86627[_sg_86627]
    _aktif_idx_86627 = set(t[1] for t in _gt_86627)
    _tab_names_86627 = [t[0] for t in _gt_86627]
    tabs = st.tabs(_tab_names_86627)
    _tab_real_86627 = {idx: t for idx, t in zip((t[1] for t in _gt_86627), tabs)}

    store = _get_ik_store()

    if 0 in _aktif_idx_86627:
      with _tab_real_86627[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_86627:
      with _tab_real_86627[1]:
        _render_aday_havuzu(store)
    if 2 in _aktif_idx_86627:
      with _tab_real_86627[2]:
        _render_mulakat_yonetimi(store)
    if 3 in _aktif_idx_86627:
      with _tab_real_86627[3]:
        _render_onboarding(store)
    if 4 in _aktif_idx_86627:
      with _tab_real_86627[4]:
        _render_aktif_calisanlar(store)
    if 5 in _aktif_idx_86627:
      with _tab_real_86627[5]:
        perf_tabs = st.tabs(["⭐ Performans Değerlendirme", "⚖️ İş Yükü Dengeleyici"])
        with perf_tabs[0]:
            _render_performans(store)
        with perf_tabs[1]:
            try:
                from views._is_yuku_dengeleyici import render_is_yuku_dengeleyici
                render_is_yuku_dengeleyici()
            except ImportError:
                st.info("İş Yükü Dengeleyici modülü yüklü değil.")
            except Exception as _e:
                st.error(f"İş Yükü Dengeleyici yüklenemedi: {_e}")
    if 6 in _aktif_idx_86627:
      with _tab_real_86627[6]:
        _render_izin_yonetimi(store)
    if 7 in _aktif_idx_86627:
      with _tab_real_86627[7]:
        _render_maas_bordro(store)
    if 8 in _aktif_idx_86627:
      with _tab_real_86627[8]:
        _render_egitim_sertifika(store)
    if 9 in _aktif_idx_86627:
      with _tab_real_86627[9]:
        _render_disiplin(store)
    if 10 in _aktif_idx_86627:
      with _tab_real_86627[10]:
        _render_offboarding(store)
    if 11 in _aktif_idx_86627:
      with _tab_real_86627[11]:
        _render_personel_bilgi_karti(store)
    if 12 in _aktif_idx_86627:
      with _tab_real_86627[12]:
        _render_raporlar(store)
    if 13 in _aktif_idx_86627:
      with _tab_real_86627[13]:
        _render_ayarlar(store)

    # ZIRVE: Yetenek Haritasi
    if 14 in _aktif_idx_86627:
      with _tab_real_86627[14]:
        try:
            from views._ik_zirve import render_yetenek_haritasi
            render_yetenek_haritasi(store)
        except Exception as _e:
            st.error(f"Yetenek Haritasi yuklenemedi: {_e}")

    # ZIRVE: 360 Feedback
    if 15 in _aktif_idx_86627:
      with _tab_real_86627[15]:
        try:
            from views._ik_zirve import render_360_feedback
            render_360_feedback(store)
        except Exception as _e:
            st.error(f"360 Feedback yuklenemedi: {_e}")

    # ZIRVE: IK Komuta Merkezi
    if 16 in _aktif_idx_86627:
      with _tab_real_86627[16]:
        try:
            from views._ik_zirve import render_ik_komuta
            render_ik_komuta(store)
        except Exception as _e:
            st.error(f"IK Komuta yuklenemedi: {_e}")

    # MEGA: Personel Dijital Ikiz
    if 17 in _aktif_idx_86627:
      with _tab_real_86627[17]:
        try:
            from views._ik_mega import render_dijital_ikiz
            render_dijital_ikiz(store)
        except Exception as _e:
            st.error(f"Dijital Ikiz yuklenemedi: {_e}")

    # MEGA: AI Ise Alim Asistani
    if 18 in _aktif_idx_86627:
      with _tab_real_86627[18]:
        try:
            from views._ik_mega import render_ai_ise_alim
            render_ai_ise_alim(store)
        except Exception as _e:
            st.error(f"AI Ise Alim yuklenemedi: {_e}")

    # MEGA: Mutluluk Barometresi
    if 19 in _aktif_idx_86627:
      with _tab_real_86627[19]:
        try:
            from views._ik_mega import render_mutluluk_barometresi
            render_mutluluk_barometresi(store)
        except Exception as _e:
            st.error(f"Mutluluk Barometresi yuklenemedi: {_e}")

    # ULTRA MEGA: Kariyer Yol Haritasi
    if 20 in _aktif_idx_86627:
      with _tab_real_86627[20]:
        try:
            from views._ik_ultra import render_kariyer_yol
            render_kariyer_yol(store)
        except Exception as _e:
            st.error(f"Kariyer Yol Haritasi yuklenemedi: {_e}")

    # ULTRA MEGA: Performans Duvari
    if 21 in _aktif_idx_86627:
      with _tab_real_86627[21]:
        try:
            from views._ik_ultra import render_performans_duvari
            render_performans_duvari(store)
        except Exception as _e:
            st.error(f"Performans Duvari yuklenemedi: {_e}")

    # ULTRA MEGA: HR Simulasyon
    if 22 in _aktif_idx_86627:
      with _tab_real_86627[22]:
        try:
            from views._ik_ultra import render_hr_simulasyon
            render_hr_simulasyon(store)
        except Exception as _e:
            st.error(f"HR Simulasyon yuklenemedi: {_e}")

    if 23 in _aktif_idx_86627:
      with _tab_real_86627[23]:
        def _ik_smarti_context():
            try:
                e = len(store.load_list("employees"))
                c = len(store.load_list("candidates"))
                r = len(store.load_list("performance_reviews"))
                return f"Toplam calisan: {e}, Toplam aday: {c}, Performans degerlendirme: {r}"
            except Exception:
                return ""
        render_smarti_chat("insan_kaynaklari", data_context_fn=_ik_smarti_context)
