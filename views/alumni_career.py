"""
Mezunlar ve Kariyer Yonetimi Modulu
===================================
Mezun takibi, iletisim, kariyer ve mentorluk yonetim sistemi.
"""

import json
import os
import io
from typing import Any

import pandas as pd
import streamlit as st

from utils.tenant import tenant_key, get_tenant_dir
from utils.report_utils import ReportStyler
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("mezunlar")
except Exception:
    pass


MEZ01_BASE = os.path.join(
    ".streamlit",
    "MEZ-01_TamPaket",
    "MEZ-01_TamPaket_Import_UAT_Checklist_FINAL_v2",
)


# ===================== YARDIMCI YOLLAR =====================


def get_mez01_component_settings_path() -> str:
    return os.path.join(get_tenant_dir(), "mez01_components.json")


def get_alumni_store_path() -> str:
    return os.path.join(get_tenant_dir(), "mezunlar.json")


def get_campaign_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_iletisim_kampanyalari.json")


def get_campaign_group_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_hedef_gruplar.json")


def get_event_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_etkinlikleri.json")


def get_mentorship_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_mentorluk.json")


def get_survey_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_anketleri.json")


def get_job_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_staj_is.json")


def get_template_store_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_iletisim_sablonlari.json")


def get_tavsiye_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_tavsiye_adaylari.json")


def get_bagis_log_path() -> str:
    return os.path.join(get_tenant_dir(), "mezun_bagis_sponsorluk.json")


# ===================== JSON YARDIMCILARI =====================


def load_alumni_store() -> list[dict]:
    path = get_alumni_store_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_alumni_store(items: list[dict]) -> None:
    path = get_alumni_store_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)


def load_json_list(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_json_list(path: str, items: list[dict]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)


def load_component_settings(defaults: dict[str, bool]) -> dict[str, bool]:
    path = get_mez01_component_settings_path()
    if not os.path.exists(path):
        return defaults
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            merged = defaults.copy()
            merged.update({k: bool(v) for k, v in data.items()})
            return merged
    except Exception:
        return defaults
    return defaults


def save_component_settings(settings: dict[str, bool]) -> None:
    path = get_mez01_component_settings_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(settings, handle, ensure_ascii=False, indent=2)


def read_csv_with_fallback(path: str) -> pd.DataFrame:
    for enc in ("utf-8-sig", "cp1254", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    return pd.read_csv(path, encoding="utf-8", errors="ignore")


def load_import_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(MEZ01_BASE, "02_Import", filename)
    if not os.path.exists(path):
        return pd.DataFrame()
    return read_csv_with_fallback(path)


def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return pd.DataFrame()
    data = uploaded_file.getvalue()
    for enc in ("utf-8-sig", "cp1254", "latin-1"):
        try:
            return pd.read_csv(io.BytesIO(data), encoding=enc)
        except Exception:
            continue
    return pd.read_csv(io.BytesIO(data), encoding="utf-8", errors="ignore")


# ===================== ROL & YETKI =====================


def role_permissions(role_code: str) -> set[str]:
    mapping = {
        "KURUCU": {"ALL"},
        "KAMPUS_MUDURU": {"ALL"},
        "MEZUN_KOORDINATORU": {"MEZUN_HAVUZU", "ILETISIM_YONETIMI", "ETKINLIK", "RAPORLAR"},
        "PDR_KARIYER": {"MEZUN_HAVUZU", "MENTORLUK", "STAJ_IS", "RAPORLAR"},
        "OGRETMEN": {"MEZUN_HAVUZU"},
        "MEZUN": {"MEZUN_PORTALI"},
    }
    return mapping.get(role_code, set())


def can_access_component(role_code: str, component_code: str) -> bool:
    perms = role_permissions(role_code)
    if "ALL" in perms:
        return True
    return component_code in perms


# ===================== CSS STIL SISTEMI =====================


def _inject_mez_css():
    """Dashboard-style modern CSS - diger modullerle ayni tasarim dili."""
    inject_common_css("mez")
    st.markdown("""<style>
    /* font: sistem fontu kullaniliyor */
    :root {
        --mez-primary: #2563eb;
        --mez-primary-dark: #A97B1F;
        --mez-primary-light: #3b82f6;
        --mez-success: #2E7D32;
        --mez-warning: #E67E22;
        --mez-danger: #C0392B;
        --mez-purple: #8b5cf6;
        --mez-teal: #2563eb;
        --mez-dark: #0B0F19;
        --mez-gray-50: #111827;
        --mez-gray-100: #1A2035;
        --mez-gray-200: #e2e8f0;
        --mez-gray-500: #64748b;
        --mez-gray-800: #94A3B8;
    }
    </style>""", unsafe_allow_html=True)


# ===================== PDF RAPOR =====================


def build_alumni_pdf_report(df: pd.DataFrame, title: str) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors as rl_colors
    except Exception:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_regular, font_bold = ensure_turkish_pdf_fonts()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Premium Header Banner ---
    banner_h = 60
    c.setFillColor(rl_colors.HexColor("#0B0F19"))
    c.rect(0, height - banner_h, width, banner_h, fill=1, stroke=0)
    # Accent line
    c.setFillColor(rl_colors.HexColor("#2563eb"))
    c.rect(0, height - banner_h, width, 3, fill=1, stroke=0)
    # Title on banner
    c.setFillColor(rl_colors.white)
    c.setFont(font_bold or font_regular, 16)
    c.drawString(50, height - 38, title)
    c.setFont(font_regular, 9)
    c.drawString(50, height - 52, f"Toplam Mezun: {len(df)}")
    c.setFillColor(rl_colors.black)

    y = height - banner_h - 30
    c.setFont(font_regular, 10)
    if "MezuniyetYili" in df.columns:
        c.setFont(font_bold or font_regular, 11)
        c.drawString(50, y, "Mezuniyet Yılı Dağılımı")
        y -= 18
        c.setFont(font_regular, 10)
        counts = df["MezuniyetYili"].value_counts().head(8)
        for year, count in counts.items():
            c.drawString(50, y, f"{year}: {count} mezun")
            y -= 14
            if y < 80:
                c.showPage()
                c.setFont(font_regular, 10)
                y = height - 40
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()


def build_alumni_list_pdf(df: pd.DataFrame, title: str, columns: list[str]) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors as rl_colors
    except Exception:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_regular, font_bold = ensure_turkish_pdf_fonts()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Premium Header Banner ---
    banner_h = 56
    c.setFillColor(rl_colors.HexColor("#0B0F19"))
    c.rect(0, height - banner_h, width, banner_h, fill=1, stroke=0)
    c.setFillColor(rl_colors.HexColor("#2563eb"))
    c.rect(0, height - banner_h, width, 3, fill=1, stroke=0)
    c.setFillColor(rl_colors.white)
    c.setFont(font_bold or font_regular, 14)
    c.drawString(40, height - 34, title)
    c.setFont(font_regular, 9)
    c.drawString(40, height - 48, f"Toplam: {len(df)}")
    c.setFillColor(rl_colors.black)

    y = height - banner_h - 20
    line_height = 14
    col_width = (width - 80) / max(len(columns), 1)

    # Table header row with background
    c.setFillColor(rl_colors.HexColor("#1A2035"))
    c.rect(35, y - 3, width - 70, line_height + 2, fill=1, stroke=0)
    c.setFillColor(rl_colors.HexColor("#94A3B8"))
    c.setFont(font_bold or font_regular, 8)
    for idx, col in enumerate(columns):
        c.drawString(40 + idx * col_width, y, col[:18])
    y -= line_height

    c.setFont(font_regular, 8)
    c.setFillColor(rl_colors.black)
    row_idx = 0
    for _, row in df.iterrows():
        if y < 60:
            c.showPage()
            # Repeat header on new page
            c.setFillColor(rl_colors.HexColor("#1A2035"))
            c.rect(35, height - 40 - 3, width - 70, line_height + 2, fill=1, stroke=0)
            c.setFillColor(rl_colors.HexColor("#94A3B8"))
            c.setFont(font_bold or font_regular, 8)
            y = height - 40
            for idx, col in enumerate(columns):
                c.drawString(40 + idx * col_width, y, col[:18])
            y -= line_height
            c.setFont(font_regular, 8)
            c.setFillColor(rl_colors.black)
            row_idx = 0
        # Alternating row background
        if row_idx % 2 == 1:
            c.setFillColor(rl_colors.HexColor("#111827"))
            c.rect(35, y - 3, width - 70, line_height, fill=1, stroke=0)
            c.setFillColor(rl_colors.black)
        for idx, col in enumerate(columns):
            value = str(row.get(col, ""))[:24]
            c.drawString(40 + idx * col_width, y, value)
        y -= line_height
        row_idx += 1

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()


# ===================== ANA RENDER =====================


def render_alumni_career() -> None:
    _inject_mez_css()
    styled_header(
        "Mezunlar ve Kariyer Yönetimi",
        "Mezun takibi, iletişim, kariyer ve mentorluk yönetim sistemi",
        "🎓",
    )

    if not os.path.isdir(MEZ01_BASE):
        styled_info_banner(
            "MEZ-01 paketi bulunamadı. Klasörü .streamlit içinde kontrol edin.",
            "error",
        )
        return

    # Veri yukle
    datasets = {
        "Bilesenler": "MEZ-01_IMPORT_Bilesenler.csv",
        "RollerYetkiler": "MEZ-01_IMPORT_RollerYetkiler.csv",
        "Ayarlar": "MEZ-01_IMPORT_Ayarlar.csv",
        "Etiketler": "MEZ-01_IMPORT_Etiketler.csv",
        "IletisimSablonlari": "MEZ-01_IMPORT_IletisimSablonlari.csv",
        "EtkinlikTurleri": "MEZ-01_IMPORT_EtkinlikTurleri.csv",
        "Anket_SoruBankasi": "MEZ-01_IMPORT_Anket_SoruBankasi.csv",
        "Mentor_Kriterleri": "MEZ-01_IMPORT_Mentor_Kriterleri.csv",
        "StajIs_Durumlari": "MEZ-01_IMPORT_StajIs_Durumlari.csv",
        "Mezun_KaynakKanallari": "MEZ-01_IMPORT_Mezun_KaynakKanallari.csv",
        "Ornek_Mezunlar": "MEZ-01_IMPORT_Ornek_Mezunlar.csv",
    }

    df_bilesen = load_import_csv(datasets["Bilesenler"])
    df_roles = load_import_csv(datasets["RollerYetkiler"])
    df_settings = load_import_csv(datasets["Ayarlar"])
    df_tags = load_import_csv(datasets["Etiketler"])
    df_templates = load_import_csv(datasets["IletisimSablonlari"])
    df_events = load_import_csv(datasets["EtkinlikTurleri"])
    df_surveys = load_import_csv(datasets["Anket_SoruBankasi"])
    df_mentors = load_import_csv(datasets["Mentor_Kriterleri"])
    df_internship = load_import_csv(datasets["StajIs_Durumlari"])
    df_sources = load_import_csv(datasets["Mezun_KaynakKanallari"])
    df_alumni = load_import_csv(datasets["Ornek_Mezunlar"])
    stored_alumni = load_alumni_store()
    df_stored = pd.DataFrame(stored_alumni)
    if df_alumni.empty and not df_stored.empty:
        df_all_alumni = df_stored
    elif not df_alumni.empty and df_stored.empty:
        df_all_alumni = df_alumni
    else:
        df_all_alumni = (
            pd.concat([df_alumni, df_stored], ignore_index=True)
            if not df_alumni.empty or not df_stored.empty
            else pd.DataFrame()
        )

    # Rol secimi
    role_options = ["KURUCU", "KAMPUS_MUDURU", "MEZUN_KOORDINATORU", "PDR_KARIYER", "OGRETMEN", "MEZUN"]
    role_labels = {
        "KURUCU": "Kurucu",
        "KAMPUS_MUDURU": "Kampüs Müdürü",
        "MEZUN_KOORDINATORU": "Mezun Koordinatörü",
        "PDR_KARIYER": "PDR / Kariyer",
        "OGRETMEN": "Öğretmen",
        "MEZUN": "Mezun",
    }
    col_role, col_spacer = st.columns([2, 4])
    with col_role:
        st.session_state.mez01_role = st.selectbox(
            "Aktif Rol",
            role_options,
            format_func=lambda x: f"👤 {role_labels.get(x, x)}",
            index=0,
            key="mez01_role_select",
        )

    # Bilesen ayarlari
    component_defaults: dict[str, bool] = {}
    if not df_bilesen.empty:
        for _, row in df_bilesen.iterrows():
            code = str(row.get("BilesenKodu", "")).strip()
            active = str(row.get("VarsayilanAktif(0/1)", "0")).strip() in {"1", "True", "true", "Evet"}
            if code:
                component_defaults[code] = active
    component_settings = load_component_settings(component_defaults)

    kvkk_required = False
    if not df_settings.empty:
        settings_map = {
            str(row.get("AyarKodu", "")).strip(): str(row.get("AyarDegeri", "")).strip()
            for _, row in df_settings.iterrows()
        }
        kvkk_required = settings_map.get("KVKK_ZORUNLU", "Hayir").lower() == "evet"

    def component_active(code: str) -> bool:
        return component_settings.get(code, False)

    def component_visible(code: str) -> bool:
        return component_active(code) and can_access_component(st.session_state.mez01_role, code)

    # Sekme yapisi
    tab_specs: list[tuple[str, str]] = []
    if st.session_state.mez01_role != "MEZUN":
        tab_specs.append(("📊 Dashboard", "GENEL"))
    if component_visible("MEZUN_HAVUZU"):
        tab_specs.append(("👥 Mezun Havuzu", "MEZUN_HAVUZU"))
    if component_visible("ILETISIM_YONETIMI"):
        tab_specs.append(("📨 İletişim & Duyuru", "ILETISIM_YONETIMI"))
    if component_visible("RAPORLAR"):
        tab_specs.append(("📊 MK Raporlar", "RAPORLAR"))
    if component_visible("MEZUN_PORTALI"):
        tab_specs.append(("🌐 Mezun Portali", "MEZUN_PORTALI"))
    if component_visible("ANKET"):
        tab_specs.append(("📋 Anketler", "ANKET"))
    if component_visible("ETKINLIK"):
        tab_specs.append(("🎉 Etkinlikler", "ETKINLIK"))
    if component_visible("STAJ_IS"):
        tab_specs.append(("💼 Staj & İş", "STAJ_IS"))
    if component_visible("MENTORLUK"):
        tab_specs.append(("🤝 Mentor", "MENTORLUK"))
    if component_visible("TAVSIYE_KAYIT_ADAYI"):
        tab_specs.append(("📣 Tavsiye Kayıt", "TAVSIYE_KAYIT_ADAYI"))
    if component_visible("BAGIS_SPONSORLUK"):
        tab_specs.append(("💎 Bağış & Sponsorluk", "BAGIS_SPONSORLUK"))
    if st.session_state.mez01_role != "MEZUN":
        tab_specs.append(("⚙️ Ayarlar", "AYARLAR"))
    tab_specs.append(("\U0001f916 Smarti", "SMARTI"))

    render_smarti_welcome("alumni_career")
    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("alumni_career_egitim_yili")

    if not tab_specs:
        styled_info_banner(
            "Görüntülenecek modul yok. Rol veya bilesen ayarlarini kontrol edin.",
            "warning",
        )
        return

    tabs = st.tabs([label for label, _ in tab_specs])
    tab_map = {key: idx for idx, (_, key) in enumerate(tab_specs)}

    # ==================== DASHBOARD ====================
    if "GENEL" in tab_map:
        with tabs[tab_map["GENEL"]]:
            # ---------- KPI Stat Kartlari ----------
            total_alumni = len(df_all_alumni) if not df_all_alumni.empty else 0
            uni_count = 0
            if not df_all_alumni.empty and "Universite" in df_all_alumni.columns:
                uni_count = int(df_all_alumni["Universite"].dropna().astype(str).apply(lambda x: x.strip() != "").sum())
            campaign_count = len(load_json_list(get_campaign_log_path()))
            mentor_count = len(load_json_list(get_mentorship_log_path()))
            event_count = len(load_json_list(get_event_log_path()))
            survey_count = len(load_json_list(get_survey_log_path()))

            styled_stat_row([
                ("Toplam Mezun", total_alumni, "#2563eb", "🎓"),
                ("Universite Mezunu", uni_count, "#8b5cf6", "🏫"),
                ("Kampanya", campaign_count, "#10b981", "📨"),
                ("Mentorluk", mentor_count, "#0d9488", "🤝"),
                ("Etkinlik", event_count, "#f59e0b", "🎉"),
                ("Anket", survey_count, "#ec4899", "📋"),
            ])

            st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

            # ---------- Row 1: Universite Dagilimi + Mezuniyet Yili ----------
            styled_section("Dagilim Grafikleri", "#2563eb")
            dash_r1c1, dash_r1c2 = st.columns(2)

            with dash_r1c1:
                styled_section("Universite Dagilimi", "#8b5cf6")
                if not df_all_alumni.empty and "Universite" in df_all_alumni.columns:
                    uni_vals = (
                        df_all_alumni["Universite"]
                        .dropna()
                        .astype(str)
                        .loc[lambda s: s.str.strip() != ""]
                        .value_counts()
                        .head(8)
                    )
                    if not uni_vals.empty:
                        uni_dict = uni_vals.to_dict()
                        donut_colors = [
                            "#2563eb", "#8b5cf6", "#10b981", "#0d9488",
                            "#f59e0b", "#ec4899", "#ef4444", "#3b82f6",
                        ]
                        st.markdown(
                            ReportStyler.donut_chart_svg(uni_dict, colors=donut_colors, size=175),
                            unsafe_allow_html=True,
                        )
                    else:
                        styled_info_banner("Universite verisi bulunamadı.", "info")
                else:
                    styled_info_banner("Universite bilgisi mevcut degil.", "info")

            with dash_r1c2:
                styled_section("Mezuniyet Yili Dagilimi", "#2563eb")
                if not df_all_alumni.empty and "MezuniyetYili" in df_all_alumni.columns:
                    year_vals = (
                        df_all_alumni["MezuniyetYili"]
                        .dropna()
                        .astype(int)
                        .loc[lambda s: s > 0]
                        .value_counts()
                        .sort_index()
                    )
                    if not year_vals.empty:
                        year_dict = {str(k): v for k, v in year_vals.items()}
                        st.markdown(
                            ReportStyler.horizontal_bar_html(year_dict, color="#2563eb"),
                            unsafe_allow_html=True,
                        )
                    else:
                        styled_info_banner("Mezuniyet yili verisi bulunamadı.", "info")
                else:
                    styled_info_banner("Mezuniyet yili bilgisi mevcut degil.", "info")

            st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

            # ---------- Row 2: Bolum Dagilimi + Ozet Bilgi ----------
            dash_r2c1, dash_r2c2 = st.columns(2)

            with dash_r2c1:
                styled_section("Bolum Dagilimi", "#10b981")
                if not df_all_alumni.empty and "Bolum" in df_all_alumni.columns:
                    bolum_vals = (
                        df_all_alumni["Bolum"]
                        .dropna()
                        .astype(str)
                        .loc[lambda s: s.str.strip() != ""]
                        .value_counts()
                        .head(8)
                    )
                    if not bolum_vals.empty:
                        bolum_dict = bolum_vals.to_dict()
                        bolum_colors = [
                            "#10b981", "#0d9488", "#2563eb", "#8b5cf6",
                            "#f59e0b", "#ec4899", "#ef4444", "#3b82f6",
                        ]
                        st.markdown(
                            ReportStyler.donut_chart_svg(bolum_dict, colors=bolum_colors, size=175),
                            unsafe_allow_html=True,
                        )
                    else:
                        styled_info_banner("Bolum verisi bulunamadı.", "info")
                else:
                    styled_info_banner("Bolum bilgisi mevcut degil.", "info")

            with dash_r2c2:
                styled_section("Genel Özet", "#0d9488")
                job_count = len(load_json_list(get_job_log_path()))

                # Summary cards as styled HTML
                st.markdown(f"""<div style="background:#111827;border-radius:14px;padding:18px 20px;
                border:1px solid #e2e8f0;margin-bottom:10px">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
                    <span style="font-size:1.4rem">💼</span>
                    <div>
                        <div style="font-size:0.75rem;color:#64748b;font-weight:600;text-transform:uppercase;
                        letter-spacing:0.5px">Staj & İş Ilanlari</div>
                        <div style="font-size:1.6rem;font-weight:800;color:#0d9488">{job_count}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
                    <span style="font-size:1.4rem">📨</span>
                    <div>
                        <div style="font-size:0.75rem;color:#64748b;font-weight:600;text-transform:uppercase;
                        letter-spacing:0.5px">Son Kampanyalar</div>
                        <div style="font-size:1.6rem;font-weight:800;color:#10b981">{campaign_count}</div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px">
                    <span style="font-size:1.4rem">🎉</span>
                    <div>
                        <div style="font-size:0.75rem;color:#64748b;font-weight:600;text-transform:uppercase;
                        letter-spacing:0.5px">Etkinlik & Anket</div>
                        <div style="font-size:1.6rem;font-weight:800;color:#8b5cf6">{event_count + survey_count}</div>
                    </div>
                </div>
                </div>""", unsafe_allow_html=True)

                styled_info_banner(
                    f"Toplam {total_alumni} mezun, {uni_count} universite mezunu, "
                    f"{mentor_count} mentorluk talebi kayitli.",
                    "success", "📊",
                )

            st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

            # ---------- Bilesen & Roller (Expander) ----------
            with st.expander("📦 Bilesen Durumu", expanded=False):
                if df_bilesen.empty:
                    styled_info_banner("Bilesen verisi bulunamadı.", "info")
                else:
                    st.dataframe(df_bilesen, use_container_width=True, hide_index=True)

            with st.expander("🔐 Roller & Yetkiler", expanded=False):
                if df_roles.empty:
                    styled_info_banner("Roller verisi bulunamadı.", "info")
                else:
                    st.dataframe(df_roles, use_container_width=True, hide_index=True)

    # ==================== MEZUN HAVUZU ====================
    if "MEZUN_HAVUZU" in tab_map:
        with tabs[tab_map["MEZUN_HAVUZU"]]:
            styled_section("Mezun Listesi", "#2563eb")
            if df_all_alumni.empty:
                styled_info_banner("Henuz mezun verisi bulunmuyor.", "info")
            else:
                filter_text = st.text_input(
                    "🔍 Ara (isim, bolum, firma)",
                    key="alumni_search",
                    placeholder="Mezun aramak için yazin...",
                )
                filtered = df_all_alumni
                if filter_text:
                    needle = filter_text.lower()
                    mask = df_all_alumni.apply(
                        lambda row: any(needle in str(val).lower() for val in row.values),
                        axis=1,
                    )
                    filtered = df_all_alumni[mask]
                if kvkk_required and "KVKK_IletisimIzni" in filtered.columns:
                    filtered = filtered[filtered["KVKK_IletisimIzni"].astype(str).str.lower() == "evet"]

                styled_info_banner(f"Toplam {len(filtered)} mezun listeleniyor.", "success", "📊")
                st.dataframe(filtered, use_container_width=True, hide_index=True)

            styled_section("Kaynak Kanalları", "#0d9488")
            if df_sources.empty:
                styled_info_banner("Kaynak kanalı verisi bulunamadı.", "info")
            else:
                st.dataframe(df_sources, use_container_width=True, hide_index=True)

            styled_section("Mezun Profili", "#8b5cf6")
            if df_all_alumni.empty:
                styled_info_banner("Profil görüntülemek için mezun kaydı gereklidir.", "info")
            else:
                ids = df_all_alumni["MezunID"].astype(str).tolist() if "MezunID" in df_all_alumni.columns else []
                selected_id = st.selectbox("Mezun seç", ids, key="alumni_profile_select")
                if selected_id:
                    row = df_all_alumni[df_all_alumni["MezunID"].astype(str) == selected_id]
                    if not row.empty:
                        st.dataframe(row, use_container_width=True, hide_index=True)

            styled_section("Toplu Etiket Ata", "#f59e0b")
            if df_all_alumni.empty:
                styled_info_banner("Toplu etiket için mezun verisi gereklidir.", "info")
            else:
                ids = df_all_alumni["MezunID"].astype(str).tolist() if "MezunID" in df_all_alumni.columns else []
                selected_ids = st.multiselect("Mezunlar", ids, key="bulk_tag_ids")
                tag_input = st.text_input("Etiketler (noktali virgul ile ayirin)", key="bulk_tag_value")
                if st.button("✏️ Etiketleri Uygula", key="apply_bulk_tags"):
                    if not selected_ids or not tag_input.strip():
                        styled_info_banner("Mezun ve etiket secin.", "warning")
                    else:
                        tag_list = [t.strip() for t in tag_input.split(";") if t.strip()]
                        updated = 0
                        for item in stored_alumni:
                            if item.get("MezunID") in selected_ids:
                                existing = [t.strip() for t in str(item.get("Etiketler", "")).split(";") if t.strip()]
                                merged = sorted(set(existing + tag_list))
                                item["Etiketler"] = ";".join(merged)
                                updated += 1
                        if updated:
                            save_alumni_store(stored_alumni)
                            st.success(f"✅ {updated} mezunun etiketleri güncellendi.")
                        else:
                            styled_info_banner("Secilen mezunlar demo kayitlarda olabilir.", "info")

            styled_section("Yeni Mezun Girişi", "#10b981")
            with st.form("alumni_create_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    mezun_id = st.text_input("Mezun ID (opsiyonel)")

                    ad = st.text_input("Ad *")

                    soyad = st.text_input("Soyad *")

                    mezuniyet = st.number_input("Mezuniyet Yili *", min_value=1990, max_value=2100, value=2024)

                    kademe = st.selectbox("Kademe", ["İlkokul", "Ortaokul", "Lise", "Universite"], index=2)

                    sinif_sube = st.text_input("Sınıf/Şube")

                with col2:
                    telefon = st.text_input("Telefon")

                    eposta = st.text_input("Eposta")

                    sehir = st.text_input("Sehir")

                    ulke = st.text_input("Ulke", value="Turkiye")

                    etiketler = st.text_input("Etiketler (noktali virgul)")

                    universite = st.text_input("Universite")

                col3, col4 = st.columns(2)
                with col3:
                    bolum = st.text_input("Bolum")

                    kvkk_izin = st.selectbox("KVKK İletişim İzni", ["Evet", "Hayır"], index=0)

                with col4:
                    kvkk_tarih = st.text_input("KVKK Tarih (YYYY-AA-GG)")

                    unvan = st.text_input("Unvan")

                sektor = st.text_input("Sektor")

                linkedin = st.text_input("LinkedIn")


                submitted = st.form_submit_button("🎓 Mezun Kaydet")
                if submitted:
                    errors = []
                    if not ad.strip():
                        errors.append("Ad zorunlu.")
                    if not soyad.strip():
                        errors.append("Soyad zorunlu.")
                    if not telefon.strip() and not eposta.strip():
                        errors.append("Telefon veya eposta gerekli.")
                    if errors:
                        for err in errors:
                            styled_info_banner(err, "error")
                    else:
                        if not mezun_id.strip():
                            mezun_id = f"MZ-{len(stored_alumni) + 1:04d}"
                        new_item = {
                            "MezunID": mezun_id.strip(),
                            "Ad": ad.strip(),
                            "Soyad": soyad.strip(),
                            "MezuniyetYili": int(mezuniyet),
                            "Kademe": kademe,
                            "SınıfŞube": sinif_sube.strip(),
                            "Telefon": telefon.strip(),
                            "Eposta": eposta.strip(),
                            "Sehir": sehir.strip(),
                            "Ulke": ulke.strip(),
                            "KVKK_IletisimIzni": kvkk_izin,
                            "KVKK_Tarih": kvkk_tarih.strip(),
                            "Etiketler": etiketler.strip(),
                            "Universite": universite.strip(),
                            "Bolum": bolum.strip(),
                            "UniGirişYili": 0,
                            "UniMezunYili": 0,
                            "Sektor": sektor.strip(),
                            "Unvan": unvan.strip(),
                            "LinkedIn": linkedin.strip(),
                        }
                        stored_alumni.append(new_item)
                        save_alumni_store(stored_alumni)
                        st.success("✅ Mezun kaydı eklendi.")

            styled_section("CSV ile Toplu Mezun Yükle", "#3b82f6")
            upload_file = st.file_uploader(
                "Mezun CSV dosyası yükle",
                type=["csv"],
                key="mezun_csv_upload",
            )
            if upload_file is not None:
                from utils.security import validate_upload
                _ok, _msg = validate_upload(upload_file, allowed_types=["csv"], max_mb=100)
                if not _ok:
                    st.error(f"⚠️ {_msg}")
                    upload_file = None
            if upload_file is not None:
                df_upload = read_uploaded_csv(upload_file)
                if df_upload.empty:
                    styled_info_banner("CSV dosyası okunamadı.", "error")
                else:
                    errors = []
                    added = 0
                    for idx, row in df_upload.iterrows():
                        r_ad = str(row.get("Ad", "")).strip()
                        r_soyad = str(row.get("Soyad", "")).strip()
                        r_telefon = str(row.get("Telefon", "")).strip()
                        r_eposta = str(row.get("Eposta", "")).strip()
                        r_mezuniyet = row.get("MezuniyetYili", "")
                        if not r_ad or not r_soyad:
                            errors.append({"Satir": idx + 2, "Sebep": "Ad/Soyad bos"})
                            continue
                        if not r_telefon and not r_eposta:
                            errors.append({"Satir": idx + 2, "Sebep": "Telefon veya eposta bos"})
                            continue
                        try:
                            r_mezuniyet = int(r_mezuniyet)
                        except Exception:
                            r_mezuniyet = 0
                        new_id = str(row.get("MezunID", "")).strip() or f"MZ-{len(stored_alumni) + 1:04d}"
                        stored_alumni.append({
                            "MezunID": new_id,
                            "Ad": r_ad,
                            "Soyad": r_soyad,
                            "MezuniyetYili": r_mezuniyet,
                            "Kademe": str(row.get("Kademe", "")).strip(),
                            "SınıfŞube": str(row.get("SınıfŞube", "")).strip(),
                            "Telefon": r_telefon,
                            "Eposta": r_eposta,
                            "Sehir": str(row.get("Sehir", "")).strip(),
                            "Ulke": str(row.get("Ulke", "")).strip(),
                            "KVKK_IletisimIzni": str(row.get("KVKK_IletisimIzni", "")).strip() or "Evet",
                            "KVKK_Tarih": str(row.get("KVKK_Tarih", "")).strip(),
                            "Etiketler": str(row.get("Etiketler", "")).strip(),
                            "Universite": str(row.get("Universite", "")).strip(),
                            "Bolum": str(row.get("Bolum", "")).strip(),
                            "UniGirişYili": int(row.get("UniGirişYili", 0) or 0),
                            "UniMezunYili": int(row.get("UniMezunYili", 0) or 0),
                            "Sektor": str(row.get("Sektor", "")).strip(),
                            "Unvan": str(row.get("Unvan", "")).strip(),
                            "LinkedIn": str(row.get("LinkedIn", "")).strip(),
                        })
                        added += 1
                    save_alumni_store(stored_alumni)
                    st.success(f"✅ Yüklenen mezun: {added}")
                    if errors:
                        styled_info_banner(f"{len(errors)} satirda hata tespit edildi.", "warning")
                        st.dataframe(pd.DataFrame(errors), use_container_width=True, hide_index=True)

    # ==================== ILETISIM & DUYURU ====================
    if "ILETISIM_YONETIMI" in tab_map:
        with tabs[tab_map["ILETISIM_YONETIMI"]]:
            styled_section("İletişim Şablonları", "#2563eb")
            if df_templates.empty:
                styled_info_banner("İletişim şablonu verisi bulunamadı.", "info")
            else:
                st.dataframe(df_templates, use_container_width=True, hide_index=True)

            styled_section("Etiketler", "#8b5cf6")
            if df_tags.empty:
                styled_info_banner("Etiket verisi bulunamadı.", "info")
            else:
                st.dataframe(df_tags, use_container_width=True, hide_index=True)

            styled_section("İletişim Kampanyası", "#10b981")
            if df_all_alumni.empty:
                styled_info_banner("Kampanya oluşturmak için mezun verisi gereklidir.", "info")
            else:
                template_options = df_templates["SablonKodu"].astype(str).tolist() if "SablonKodu" in df_templates.columns else []

                with st.expander("➕ Yeni Sablon Ekle", expanded=False):
                    new_code = st.text_input("Sablon Kodu", key="campaign_new_template_code")
                    new_title = st.text_input("Sablon Başlığı", key="campaign_new_template_title")
                    new_body = st.text_area("Şablon İçeriği", key="campaign_new_template_body")
                    if st.button("💾 Sablon Kaydet", key="campaign_new_template_save"):
                        if not new_code.strip() or not new_body.strip():
                            styled_info_banner("Şablon kodu ve içerik zorunludur.", "warning")
                        else:
                            tpl_list = load_json_list(get_template_store_path())
                            tpl_list.append({
                                "SablonKodu": new_code.strip(),
                                "Başlık": new_title.strip(),
                                "İçerik": new_body.strip(),
                            })
                            save_json_list(get_template_store_path(), tpl_list)
                            st.success("✅ Sablon eklendi.")
                            st.rerun()

                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    selected_template = st.selectbox("Sablon", template_options, key="campaign_template")
                with col_k2:
                    channel = st.selectbox("Kanal", ["SMS", "WhatsApp", "E-posta", "Uygulama"], key="campaign_channel")

                message = st.text_area("Mesaj", key="campaign_message", height=120)

                ids = df_all_alumni["MezunID"].astype(str).tolist() if "MezunID" in df_all_alumni.columns else []
                year_options: list[int] = []
                if "MezuniyetYili" in df_all_alumni.columns:
                    year_options = sorted(
                        {int(val) for val in df_all_alumni["MezuniyetYili"].fillna(0).astype(int).tolist() if val > 0}
                    )
                new_year = st.number_input("Yeni Mezuniyet Yili Ekle", min_value=1990, max_value=2100, value=2024)
                if st.button("➕ Yil Ekle", key="campaign_add_year"):
                    if int(new_year) not in year_options:
                        year_options.append(int(new_year))
                        year_options = sorted(year_options)
                selected_years = st.multiselect(
                    "Mezuniyet Yillari",
                    year_options,
                    default=year_options,
                    key="campaign_years",
                )
                if selected_years and "MezuniyetYili" in df_all_alumni.columns:
                    ids = df_all_alumni[
                        df_all_alumni["MezuniyetYili"].astype(int).isin(selected_years)
                    ]["MezunID"].astype(str).tolist()

                groups = load_json_list(get_campaign_group_path())
                group_names = [g.get("name") for g in groups if g.get("name")]
                year_groups: dict[str, int] = {}
                if "MezuniyetYili" in df_all_alumni.columns:
                    for year in sorted(
                        {int(val) for val in df_all_alumni["MezuniyetYili"].fillna(0).astype(int).tolist() if val > 0}
                    ):
                        year_groups[f"Mezun {year}"] = year
                if year_groups:
                    group_names = list(year_groups.keys()) + group_names
                selected_group = st.selectbox("Hedef Grup", ["Yok"] + group_names, key="campaign_group_select")
                select_all = st.checkbox("Tümünu sec", value=True, key="campaign_targets_all")
                default_targets = ids if select_all else []
                if selected_group != "Yok":
                    if selected_group in year_groups:
                        year_value = year_groups[selected_group]
                        default_targets = df_all_alumni[
                            df_all_alumni["MezuniyetYili"].astype(int) == int(year_value)
                        ]["MezunID"].astype(str).tolist()
                    group = next((g for g in groups if g.get("name") == selected_group), None)
                    if group:
                        default_targets = [mid for mid in group.get("targets", []) if mid in ids]
                target_ids = st.multiselect("Hedef Mezunlar", ids, default=default_targets, key="campaign_targets")

                with st.expander("📁 Hedef Grup Kaydet", expanded=False):
                    group_name = st.text_input("Grup Adi", key="campaign_new_group_name")
                    if st.button("💾 Grubu Kaydet", key="campaign_group_save"):
                        if not group_name.strip():
                            styled_info_banner("Grup adi gereklidir.", "warning")
                        elif not target_ids:
                            styled_info_banner("Hedef mezun secin.", "warning")
                        else:
                            groups = [g for g in groups if g.get("name") != group_name.strip()]
                            groups.append({"name": group_name.strip(), "targets": target_ids})
                            save_json_list(get_campaign_group_path(), groups)
                            st.success("✅ Hedef grup kaydedildi.")
                            st.rerun()

                if st.button("🚀 Kampanya Oluştur", key="campaign_create", type="primary"):
                    if not target_ids:
                        styled_info_banner("Hedef mezun seciniz.", "warning")
                    else:
                        if kvkk_required and "KVKK_IletisimIzni" in df_all_alumni.columns:
                            permitted = df_all_alumni[
                                df_all_alumni["KVKK_IletisimIzni"].astype(str).str.lower() == "evet"
                            ]["MezunID"].astype(str).tolist()
                            target_ids = [mid for mid in target_ids if mid in permitted]
                        payload = {
                            "template": selected_template,
                            "channel": channel,
                            "message": message,
                            "targets": target_ids,
                        }
                        logs = load_json_list(get_campaign_log_path())
                        logs.append(payload)
                        save_json_list(get_campaign_log_path(), logs)
                        st.success(f"✅ Kampanya oluşturuldu! {len(target_ids)} mezuna gonderilecek.")

    # ==================== RAPORLAR ====================
    if "RAPORLAR" in tab_map:
        with tabs[tab_map["RAPORLAR"]]:
            if df_all_alumni.empty:
                styled_info_banner("Rapor oluşturmak için mezun verisi gereklidir.", "info")
            else:
                # Özet stat kartları
                total = len(df_all_alumni)
                uni_names = 0
                bolum_count = 0
                if "Universite" in df_all_alumni.columns:
                    uni_names = df_all_alumni["Universite"].dropna().nunique()
                if "Bolum" in df_all_alumni.columns:
                    bolum_count = df_all_alumni["Bolum"].dropna().nunique()
                sehir_count = 0
                if "Sehir" in df_all_alumni.columns:
                    sehir_count = df_all_alumni["Sehir"].dropna().nunique()

                styled_stat_row([
                    ("Toplam Mezun", total, "#2563eb", "🎓"),
                    ("Farklı Üniversite", uni_names, "#8b5cf6", "🏫"),
                    ("Farklı Bölüm", bolum_count, "#10b981", "📚"),
                    ("Farklı Şehir", sehir_count, "#0d9488", "🌍"),
                ])

                st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

                styled_section("Bölüm Dağılımı", "#2563eb")
                if "Bolum" in df_all_alumni.columns:
                    bolum_counts = df_all_alumni["Bolum"].dropna().astype(str).value_counts().head(15)
                    bolum_dict = bolum_counts.to_dict()
                    c_sun, c_bar = st.columns(2)
                    with c_sun:
                        st.markdown(ReportStyler.sunburst_chart_svg(bolum_dict, size=280, title="Bölüm"), unsafe_allow_html=True)
                    with c_bar:
                        st.markdown(ReportStyler.horizontal_bar_html(bolum_dict, color="#2563eb"), unsafe_allow_html=True)
                else:
                    styled_info_banner("Bölüm bilgisi bulunamadı.", "info")

                styled_section("PDF Rapor", "#8b5cf6")
                pdf_bytes = build_alumni_pdf_report(df_all_alumni, "Mezunlar Yıllık Rapor")
                if pdf_bytes:
                    st.download_button(
                        "📥 PDF Rapor İndir",
                        data=pdf_bytes,
                        file_name="mezun_rapor.pdf",
                        mime="application/pdf",
                    )

                styled_section("Üniversite - Meslek Grafiği", "#0d9488")
                if "Universite" in df_all_alumni.columns and "Unvan" in df_all_alumni.columns:
                    uni_options = sorted(df_all_alumni["Universite"].dropna().astype(str).unique().tolist())
                    if uni_options:
                        selected_uni = st.selectbox("Üniversite seç", uni_options, key="uni_role_chart")
                        subset = df_all_alumni[df_all_alumni["Universite"].astype(str) == selected_uni]
                        if "Unvan" in subset.columns:
                            counts = subset["Unvan"].fillna("Bilinmiyor").astype(str).value_counts().head(15)
                            meslek_dict = counts.to_dict()
                            st.markdown(ReportStyler.horizontal_bar_html(meslek_dict, color="#0d9488"), unsafe_allow_html=True)
                    else:
                        styled_info_banner("Üniversite verisi bulunamadı.", "info")
                else:
                    styled_info_banner("Üniversite veya Unvan bilgisi eksik.", "info")

                styled_section("Mezun Olunan Üniversite Dağılımı", "#f59e0b")
                if "Universite" in df_all_alumni.columns:
                    uni_counts = (
                        df_all_alumni["Universite"]
                        .fillna("Bilinmiyor")
                        .astype(str)
                        .value_counts()
                        .head(20)
                    )
                    uni_dict = uni_counts.to_dict()
                    c_sun2, c_bar2 = st.columns(2)
                    with c_sun2:
                        st.markdown(ReportStyler.sunburst_chart_svg(uni_dict, size=300, title="Üniversite"), unsafe_allow_html=True)
                    with c_bar2:
                        st.markdown(ReportStyler.horizontal_bar_html(uni_dict, color="#f59e0b"), unsafe_allow_html=True)
                else:
                    styled_info_banner("Üniversite bilgisi eksik.", "info")

                styled_section("Mezun Listesi PDF", "#10b981")
                report_columns = [
                    "MezunID", "Ad", "Soyad", "MezuniyetYili", "Kademe",
                    "SınıfŞube", "Telefon", "Eposta", "Sehir", "Ulke",
                    "KVKK_IletisimIzni", "KVKK_Tarih", "Etiketler",
                    "Universite", "Bolum", "UniGirişYili", "UniMezunYili",
                    "Sektor", "Unvan", "LinkedIn",
                ]
                available_columns = [col for col in report_columns if col in df_all_alumni.columns]
                year_opts = sorted(
                    {int(val) for val in df_all_alumni["MezuniyetYili"].fillna(0).astype(int).tolist() if val > 0}
                )
                selected_year = st.selectbox("Mezuniyet Yılı", ["Tüm Yıllar"] + year_opts)

                if selected_year == "Tüm Yıllar":
                    df_report = df_all_alumni
                    file_name = "mezun_listesi.pdf"
                    pdf_title = "Mezun Listesi (Tüm Yıllar)"
                else:
                    df_report = df_all_alumni[df_all_alumni["MezuniyetYili"].astype(int) == int(selected_year)]
                    file_name = f"mezun_listesi_{selected_year}.pdf"
                    pdf_title = f"Mezun Listesi ({selected_year})"

                list_pdf = build_alumni_list_pdf(df_report, pdf_title, available_columns)
                if list_pdf:
                    st.download_button(
                        "📥 Mezun Listesini PDF İndir",
                        data=list_pdf,
                        file_name=file_name,
                        mime="application/pdf",
                    )

                # ---- Performans Karşılaştırma ----
                from utils.report_utils import (
                    ai_recommendations_html, period_comparison_row_html,
                    generate_module_pdf, render_pdf_download_button,
                    render_report_kunye_html,
                )
                from datetime import datetime as _mk_dt, timedelta as _mk_td

                st.markdown(ReportStyler.section_divider_html("Performans Karşılaştırma", "#0d9488"), unsafe_allow_html=True)

                try:
                    now = _mk_dt.now()
                    current_month = now.strftime("%Y-%m")
                    prev_month = (now.replace(day=1) - _mk_td(days=1)).strftime("%Y-%m")

                    alumni_list = load_alumni_store()
                    events_list = load_json_list(get_event_log_path())
                    mentors_list = load_json_list(get_mentorship_log_path())

                    def _mk_count_by_month(items, date_key, month_str):
                        count = 0
                        for item in items:
                            if isinstance(item, dict):
                                val = item.get(date_key, "") or ""
                                if val[:7] == month_str:
                                    count += 1
                        return count

                    alumni_cur = _mk_count_by_month(alumni_list, "created_at", current_month)
                    alumni_prev = _mk_count_by_month(alumni_list, "created_at", prev_month)
                    event_cur = _mk_count_by_month(events_list, "date", current_month)
                    event_prev = _mk_count_by_month(events_list, "date", prev_month)

                    comparisons = [
                        {"label": "Yeni Mezun Kaydı", "current": alumni_cur, "previous": alumni_prev},
                        {"label": "Etkinlik Katılım", "current": event_cur, "previous": event_prev},
                        {"label": "Toplam Mezun", "current": len(alumni_list), "previous": max(len(alumni_list) - alumni_cur, 0)},
                    ]
                    st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)
                except Exception:
                    st.caption("Performans karşılaştırma verisi yok.")

                # ---- AI Önerileri ----
                try:
                    insights = []

                    # 1) İletişim bilgisi eksik mezunlar
                    eksik_iletisim = 0
                    for a in alumni_list:
                        if isinstance(a, dict):
                            tel = a.get("Telefon", "") or a.get("telefon", "")
                            email = a.get("Eposta", "") or a.get("email", "")
                            if not tel and not email:
                                eksik_iletisim += 1
                    if eksik_iletisim > 0:
                        insights.append({
                            "icon": "📱", "title": "İletişim Bilgisi Eksik",
                            "text": f"{eksik_iletisim} mezunun telefon ve e-posta bilgisi eksik. İletişim güncelleme kampanyası düzenlenmesi öneriliyor.",
                            "color": "#f59e0b",
                        })

                    # 2) Mentorluk fırsatları
                    if len(mentors_list) < 3:
                        insights.append({
                            "icon": "🤝", "title": "Mentorluk Programı",
                            "text": f"Aktif mentorluk talebi sayısı ({len(mentors_list)}) düşük. Başarılı mezunları mentor olarak yönlendirmek öğrenci gelişimine katkı sağlar.",
                            "color": "#2563eb",
                        })

                    # 3) Etkinlik planlama
                    if len(events_list) < 2:
                        insights.append({
                            "icon": "🎉", "title": "Etkinlik Planlama",
                            "text": "Mezun etkinlik sayısı düşük. Yıllık buluşma, kariyer günleri veya sektörel söyleşi etkinlikleri planlanabilir.",
                            "color": "#8b5cf6",
                        })

                    # 4) Üniversite/Sektör dağılımı analizi
                    if "Sektor" in df_all_alumni.columns:
                        sektor_count = df_all_alumni["Sektor"].dropna().nunique()
                        if sektor_count > 5:
                            insights.append({
                                "icon": "🏢", "title": "Sektörel Çeşitlilik",
                                "text": f"Mezunlar {sektor_count} farklı sektörde yer alıyor. Sektörler arası ağ oluşturma etkinliği düzenlenmesi öneriliyor.",
                                "color": "#0d9488",
                            })

                    # 5) Genel durum
                    if not insights:
                        insights.append({
                            "icon": "✅", "title": "Genel Durum İyi",
                            "text": "Mezun takip sistemi güncel ve aktif görünüyor. İletişim ve etkinlik çalışmalarını sürdürün.",
                            "color": "#10b981",
                        })

                    st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)
                except Exception:
                    pass

                # ---- Kurumsal Künye ----
                st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

                # ---- PDF Export ----
                st.markdown(ReportStyler.section_divider_html("Toplu Mezun Raporu (PDF)", "#1e40af"), unsafe_allow_html=True)
                if st.button("📥 MK Genel Raporu (PDF)", key="mk_toplu_pdf_btn", use_container_width=True):
                    try:
                        sections = []
                        sections.append({
                            "title": "Mezun Genel Özet",
                            "metrics": [
                                ("Toplam Mezun", str(total), "#2563eb"),
                                ("Farklı Üniversite", str(uni_names), "#8b5cf6"),
                                ("Farklı Bölüm", str(bolum_count), "#10b981"),
                                ("Farklı Şehir", str(sehir_count), "#0d9488"),
                            ],
                            "text": f"Rapor Tarihi: {_mk_dt.now().strftime('%d.%m.%Y %H:%M')}",
                        })

                        # Bölüm dağılımı
                        if "Bolum" in df_all_alumni.columns:
                            bolum_top = df_all_alumni["Bolum"].dropna().astype(str).value_counts().head(10).to_dict()
                            if bolum_top:
                                sections.append({
                                    "title": "Bölüm Dağılımı",
                                    "bar_data": {k: float(v) for k, v in bolum_top.items()},
                                    "bar_title": "En Çok Tercih Edilen Bölümler",
                                    "bar_color": "#2563eb",
                                })

                        # Üniversite dağılımı
                        if "Universite" in df_all_alumni.columns:
                            uni_top = df_all_alumni["Universite"].dropna().astype(str).value_counts().head(10).to_dict()
                            if uni_top:
                                sections.append({
                                    "title": "Üniversite Dağılımı",
                                    "bar_data": {k: float(v) for k, v in uni_top.items()},
                                    "bar_title": "En Çok Mezun Veren Üniversiteler",
                                    "bar_color": "#f59e0b",
                                })

                        pdf_bytes = generate_module_pdf("MEZ-01 Mezunlar ve Kariyer Raporu", sections)
                        render_pdf_download_button(pdf_bytes, "mezun_genel_rapor.pdf", "MK Genel Raporu", "mk_toplu_dl")
                    except Exception as e:
                        st.error(f"PDF oluşturma hatası: {e}")

    # ==================== MEZUN PORTALI ====================
    if "MEZUN_PORTALI" in tab_map:
        with tabs[tab_map["MEZUN_PORTALI"]]:
            styled_section("Mezun Portalı", "#2563eb")
            styled_info_banner(
                "Mezun portalı üzerinden kişisel profil erişimi, duyurular ve etkinlik takibi yapılabilir.",
                "info", "🌐",
            )

            if not df_all_alumni.empty:
                # Profil Kartı
                styled_section("Mezun Profil Kartı", "#8b5cf6")
                ids = df_all_alumni["MezunID"].astype(str).tolist() if "MezunID" in df_all_alumni.columns else []
                names = []
                for _, r in df_all_alumni.iterrows():
                    ad = str(r.get("Ad", "")).strip()
                    soyad = str(r.get("Soyad", "")).strip()
                    mid = str(r.get("MezunID", "")).strip()
                    names.append(f"{mid} — {ad} {soyad}")
                selected_profile = st.selectbox("Mezun Seçin", names, key="portal_profile_select")
                if selected_profile and ids:
                    sel_id = selected_profile.split(" — ")[0].strip()
                    row = df_all_alumni[df_all_alumni["MezunID"].astype(str) == sel_id]
                    if not row.empty:
                        r = row.iloc[0]
                        ad = str(r.get("Ad", ""))
                        soyad = str(r.get("Soyad", ""))
                        mezuniyet = r.get("MezuniyetYili", "-")
                        kademe = str(r.get("Kademe", "-"))
                        uni = str(r.get("Universite", "-"))
                        bolum = str(r.get("Bolum", "-"))
                        sektor = str(r.get("Sektor", "-"))
                        unvan = str(r.get("Unvan", "-"))
                        sehir = str(r.get("Sehir", "-"))
                        linkedin = str(r.get("LinkedIn", ""))

                        st.markdown(f"""
                        <div style="background:#111827;border:1px solid #e2e8f0;border-radius:16px;padding:24px;margin:10px 0;">
                            <div style="display:flex;align-items:center;gap:18px;margin-bottom:16px;">
                                <div style="background:linear-gradient(135deg,#2563eb,#8b5cf6);width:64px;height:64px;border-radius:50%;
                                display:flex;align-items:center;justify-content:center;font-size:1.8rem;color:white;font-weight:800;">
                                    {ad[0] if ad else "?"}{soyad[0] if soyad else ""}
                                </div>
                                <div>
                                    <div style="font-size:1.4rem;font-weight:800;color:#e0e0e0;">{ad} {soyad}</div>
                                    <div style="color:#94A3B8;font-size:0.9rem;">{unvan} | {sektor}</div>
                                </div>
                            </div>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                                <div style="background:#1A2035;border-radius:10px;padding:10px 14px;">
                                    <span style="color:#64748b;font-size:0.75rem;">Mezuniyet</span>
                                    <div style="color:#e0e0e0;font-weight:600;">{mezuniyet} — {kademe}</div>
                                </div>
                                <div style="background:#1A2035;border-radius:10px;padding:10px 14px;">
                                    <span style="color:#64748b;font-size:0.75rem;">Üniversite / Bölüm</span>
                                    <div style="color:#e0e0e0;font-weight:600;">{uni} / {bolum}</div>
                                </div>
                                <div style="background:#1A2035;border-radius:10px;padding:10px 14px;">
                                    <span style="color:#64748b;font-size:0.75rem;">Şehir</span>
                                    <div style="color:#e0e0e0;font-weight:600;">{sehir}</div>
                                </div>
                                <div style="background:#1A2035;border-radius:10px;padding:10px 14px;">
                                    <span style="color:#64748b;font-size:0.75rem;">LinkedIn</span>
                                    <div style="color:#3b82f6;font-weight:600;">{linkedin if linkedin and linkedin != 'nan' else '-'}</div>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)

                # Güncel Duyurular
                styled_section("Güncel Duyurular", "#10b981")
                campaigns = load_json_list(get_campaign_log_path())
                if campaigns:
                    for c in campaigns[-5:]:
                        st.markdown(f"- **{c.get('channel','')}:** {c.get('message','')[:120]}...")
                else:
                    styled_info_banner("Henüz duyuru bulunmuyor.", "info")

                # Yaklaşan Etkinlikler
                styled_section("Yaklaşan Etkinlikler", "#f59e0b")
                portal_events = load_json_list(get_event_log_path())
                aktif_events = [e for e in portal_events if e.get("durum") in ("Planlandı", "Devam Ediyor", "Aktif", None)]
                if aktif_events:
                    for ev in aktif_events[-5:]:
                        st.markdown(f"- **{ev.get('name','')}** — {ev.get('date','')} | {ev.get('konum', ev.get('type',''))}")
                else:
                    styled_info_banner("Yaklaşan etkinlik bulunmuyor.", "info")

                # Aktif Staj/İş İlanları
                styled_section("Güncel Staj & İş İlanları", "#3b82f6")
                portal_jobs = load_json_list(get_job_log_path())
                aktif_jobs = [j for j in portal_jobs if j.get("durum") in ("Aktif", "Açık", None)]
                if aktif_jobs:
                    for jb in aktif_jobs[-5:]:
                        st.markdown(f"- **{jb.get('title','')}** — {jb.get('company','-')} | {jb.get('sehir','-')} | Son: {jb.get('son_basvuru','-')}")
                else:
                    styled_info_banner("Aktif ilan bulunmuyor.", "info")
            else:
                styled_info_banner("Portal içeriği için mezun verisi gereklidir.", "info")

    # ==================== ANKETLER ====================
    if "ANKET" in tab_map:
        with tabs[tab_map["ANKET"]]:
            existing_surveys = load_json_list(get_survey_log_path())

            an_aktif = sum(1 for s in existing_surveys if s.get("durum") == "Aktif")
            an_kapali = sum(1 for s in existing_surveys if s.get("durum") == "Kapandı")
            an_toplam_yanit = sum(int(s.get("yanit_sayisi", 0)) for s in existing_surveys)
            styled_stat_row([
                ("Toplam Anket", len(existing_surveys), "#8b5cf6", "📋"),
                ("Aktif", an_aktif, "#10b981", "🟢"),
                ("Kapandı", an_kapali, "#64748b", "🔒"),
                ("Toplam Yanıt", an_toplam_yanit, "#f59e0b", "💬"),
            ])

            styled_section("Soru Bankası (Referans)", "#8b5cf6")
            if df_surveys.empty:
                styled_info_banner("Anket soru bankası verisi bulunamadı.", "info")
            else:
                st.dataframe(df_surveys, use_container_width=True, hide_index=True)

            styled_section("Yeni Anket Oluştur", "#10b981")
            with st.form("survey_form", clear_on_submit=True):
                an_c1, an_c2 = st.columns(2)
                with an_c1:
                    s_title = st.text_input("Anket Başlığı *")
                    s_hedef = st.selectbox("Hedef Kitle", ["Tüm Mezunlar", "Son 5 Yıl Mezunları", "Üniversite Mezunları", "Lise Mezunları", "Belirli Dönem"], key="an_hedef")
                with an_c2:
                    s_tur = st.selectbox("Anket Türü", ["Memnuniyet", "Kariyer Takip", "İletişim Güncelleme", "Etkinlik Değerlendirme", "Genel"], key="an_tur")
                    s_bitis = st.date_input("Bitiş Tarihi", key="an_bitis")
                s_desc = st.text_area("Açıklama", height=60, key="an_aciklama")

                # Sorular
                st.markdown("**Sorular** (her satır bir soru)")
                s_sorular = st.text_area("Sorularınızı girin", height=100, key="an_sorular",
                                          placeholder="Okulumuzdan memnun musunuz?\nŞu anki mesleğiniz nedir?\nMentorluk yapmak ister misiniz?")

                submit_survey = st.form_submit_button("📋 Anket Oluştur", type="primary")
                if submit_survey:
                    if not s_title.strip():
                        styled_info_banner("Anket başlığı zorunludur.", "warning")
                    else:
                        from datetime import datetime as _dt6
                        sorular = [q.strip() for q in s_sorular.split("\n") if q.strip()]
                        existing_surveys.append({
                            "id": f"AN-{len(existing_surveys)+1:04d}",
                            "title": s_title.strip(),
                            "tur": s_tur,
                            "hedef": s_hedef,
                            "description": s_desc.strip(),
                            "sorular": sorular,
                            "bitis_tarihi": s_bitis.isoformat(),
                            "durum": "Aktif",
                            "yanit_sayisi": 0,
                            "created_at": _dt6.now().isoformat(),
                        })
                        save_json_list(get_survey_log_path(), existing_surveys)
                        st.success("Anket oluşturuldu.")
                        st.rerun()

            # Mevcut anketler
            if existing_surveys:
                styled_section("Oluşturulan Anketler", "#0d9488")
                for idx, an in enumerate(existing_surveys):
                    durum = an.get("durum", "Aktif")
                    durum_icon = {"Aktif": "🟢", "Kapandı": "🔒", "Taslak": "📝"}.get(durum, "⚪")
                    soru_count = len(an.get("sorular", []))
                    with st.expander(f"{durum_icon} {an.get('title','')} — {an.get('tur','-')} ({soru_count} soru, {an.get('yanit_sayisi',0)} yanıt)"):
                        st.markdown(f"**Tür:** {an.get('tur','-')} | **Hedef:** {an.get('hedef','-')} | **Bitiş:** {an.get('bitis_tarihi','-')}")
                        if an.get("description"):
                            st.markdown(f"**Açıklama:** {an.get('description')}")
                        if an.get("sorular"):
                            st.markdown("**Sorular:**")
                            for qi, q in enumerate(an.get("sorular", []), 1):
                                st.markdown(f"  {qi}. {q}")
                        anc1, anc2, anc3, anc4 = st.columns([2, 1, 1, 1])
                        with anc1:
                            new_an_durum = st.selectbox("Durum", ["Aktif", "Kapandı", "Taslak"],
                                                         index=["Aktif", "Kapandı", "Taslak"].index(durum) if durum in ["Aktif", "Kapandı", "Taslak"] else 0,
                                                         key=f"an_dur_{idx}")
                        with anc2:
                            new_an_yanit = st.number_input("Yanıt", min_value=0, value=int(an.get("yanit_sayisi", 0)), key=f"an_yt_{idx}")
                        with anc3:
                            if st.button("Güncelle", key=f"an_save_{idx}", type="primary"):
                                existing_surveys[idx]["durum"] = new_an_durum
                                existing_surveys[idx]["yanit_sayisi"] = new_an_yanit
                                save_json_list(get_survey_log_path(), existing_surveys)
                                st.success("Güncellendi.")
                                st.rerun()
                        with anc4:
                            if st.button("🗑️", key=f"an_del_{idx}"):
                                existing_surveys.pop(idx)
                                save_json_list(get_survey_log_path(), existing_surveys)
                                st.rerun()

    # ==================== ETKINLIKLER ====================
    if "ETKINLIK" in tab_map:
        with tabs[tab_map["ETKINLIK"]]:
            existing_events = load_json_list(get_event_log_path())

            # İstatistik
            et_planli = sum(1 for e in existing_events if e.get("durum") == "Planlandı")
            et_tamamlandi = sum(1 for e in existing_events if e.get("durum") == "Tamamlandı")
            et_toplam_katilimci = sum(int(e.get("katilimci_sayisi", 0)) for e in existing_events)
            styled_stat_row([
                ("Toplam Etkinlik", len(existing_events), "#ec4899", "🎉"),
                ("Planlandı", et_planli, "#2563eb", "📅"),
                ("Tamamlandı", et_tamamlandi, "#10b981", "✅"),
                ("Toplam Katılımcı", et_toplam_katilimci, "#8b5cf6", "👥"),
            ])

            styled_section("Etkinlik Türleri (Referans)", "#ec4899")
            if df_events.empty:
                styled_info_banner("Etkinlik türü verisi bulunamadı.", "info")
            else:
                st.dataframe(df_events, use_container_width=True, hide_index=True)

            styled_section("Yeni Etkinlik Oluştur", "#10b981")
            with st.form("event_form", clear_on_submit=True):
                ev_c1, ev_c2 = st.columns(2)
                with ev_c1:
                    event_name = st.text_input("Etkinlik Adı *")
                    event_type = st.selectbox(
                        "Tür",
                        df_events["EtkinlikTuru"].astype(str).tolist() if "EtkinlikTuru" in df_events.columns else ["Buluşma", "Kariyer Günü", "Söyleşi", "Gala", "Diğer"],
                    )
                    event_date = st.date_input("Tarih", key="ev_tarih")
                with ev_c2:
                    event_konum = st.text_input("Konum")
                    event_katilimci = st.number_input("Tahmini Katılımcı", min_value=0, value=0, key="ev_katilimci")
                    event_durum = st.selectbox("Durum", ["Planlandı", "Devam Ediyor", "Tamamlandı", "İptal"], key="ev_durum")
                event_aciklama = st.text_area("Açıklama", height=80, key="ev_aciklama")
                event_sorumlu = st.text_input("Sorumlu Kişi", key="ev_sorumlu")

                event_submit = st.form_submit_button("🎉 Etkinlik Kaydet", type="primary")
                if event_submit:
                    if not event_name.strip():
                        styled_info_banner("Etkinlik adı zorunludur.", "warning")
                    else:
                        from datetime import datetime as _dt3
                        existing_events.append({
                            "id": f"ET-{len(existing_events)+1:04d}",
                            "name": event_name.strip(),
                            "type": event_type,
                            "date": event_date.isoformat(),
                            "konum": event_konum.strip(),
                            "katilimci_sayisi": event_katilimci,
                            "durum": event_durum,
                            "aciklama": event_aciklama.strip(),
                            "sorumlu": event_sorumlu.strip(),
                            "created_at": _dt3.now().isoformat(),
                        })
                        save_json_list(get_event_log_path(), existing_events)
                        st.success("Etkinlik kaydedildi.")
                        st.rerun()

            # Mevcut etkinlikler
            if existing_events:
                styled_section("Oluşturulan Etkinlikler", "#8b5cf6")
                for idx, ev in enumerate(existing_events):
                    durum_icon = {"Planlandı": "📅", "Devam Ediyor": "🔄", "Tamamlandı": "✅", "İptal": "❌"}.get(ev.get("durum", ""), "⚪")
                    with st.expander(f"{durum_icon} {ev.get('name','')} — {ev.get('date','')} ({ev.get('durum', ev.get('type',''))})"):
                        st.markdown(f"**Tür:** {ev.get('type','-')} | **Konum:** {ev.get('konum','-')} | **Katılımcı:** {ev.get('katilimci_sayisi','-')}")
                        st.markdown(f"**Sorumlu:** {ev.get('sorumlu','-')}")
                        if ev.get("aciklama"):
                            st.markdown(f"**Açıklama:** {ev.get('aciklama')}")
                        evc1, evc2, evc3 = st.columns([2, 2, 1])
                        with evc1:
                            new_ev_durum = st.selectbox("Durum", ["Planlandı", "Devam Ediyor", "Tamamlandı", "İptal"],
                                                         index=["Planlandı", "Devam Ediyor", "Tamamlandı", "İptal"].index(ev.get("durum", "Planlandı")) if ev.get("durum", "Planlandı") in ["Planlandı", "Devam Ediyor", "Tamamlandı", "İptal"] else 0,
                                                         key=f"ev_dur_{idx}")
                            new_ev_kat = st.number_input("Gerçek Katılımcı", min_value=0, value=int(ev.get("katilimci_sayisi", 0)), key=f"ev_kat_{idx}")
                        with evc2:
                            if st.button("Güncelle", key=f"ev_save_{idx}", type="primary"):
                                existing_events[idx]["durum"] = new_ev_durum
                                existing_events[idx]["katilimci_sayisi"] = new_ev_kat
                                save_json_list(get_event_log_path(), existing_events)
                                st.success("Etkinlik güncellendi.")
                                st.rerun()
                        with evc3:
                            if st.button("🗑️ Sil", key=f"ev_del_{idx}"):
                                existing_events.pop(idx)
                                save_json_list(get_event_log_path(), existing_events)
                                st.rerun()

    # ==================== STAJ & IS ====================
    if "STAJ_IS" in tab_map:
        with tabs[tab_map["STAJ_IS"]]:
            existing_jobs = load_json_list(get_job_log_path())

            jb_aktif = sum(1 for j in existing_jobs if j.get("durum", j.get("status", "")) in ("Aktif", "Açık"))
            jb_staj = sum(1 for j in existing_jobs if j.get("ilan_turu") == "Staj")
            jb_is = sum(1 for j in existing_jobs if j.get("ilan_turu") == "İş")
            styled_stat_row([
                ("Toplam İlan", len(existing_jobs), "#3b82f6", "💼"),
                ("Staj", jb_staj, "#10b981", "🎓"),
                ("İş", jb_is, "#8b5cf6", "🏢"),
                ("Aktif", jb_aktif, "#f59e0b", "🟢"),
            ])

            styled_section("Durum Referansları", "#3b82f6")
            if df_internship.empty:
                styled_info_banner("Staj/İş durum verisi bulunamadı.", "info")
            else:
                st.dataframe(df_internship, use_container_width=True, hide_index=True)

            styled_section("Yeni Staj / İş İlanı", "#10b981")
            with st.form("job_form", clear_on_submit=True):
                jb_c1, jb_c2 = st.columns(2)
                with jb_c1:
                    job_title = st.text_input("İlan Başlığı *")
                    job_ilan_turu = st.selectbox("İlan Türü", ["Staj", "İş", "Part-time", "Freelance"], key="jb_tur")
                    job_company = st.text_input("Firma Adı")
                    job_sektor = st.text_input("Sektör")
                with jb_c2:
                    job_sehir = st.text_input("Şehir", key="jb_sehir")
                    job_maas = st.text_input("Maaş / Ücret Aralığı", key="jb_maas")
                    job_son_basvuru = st.date_input("Son Başvuru Tarihi", key="jb_son_basvuru")
                    job_link = st.text_input("Başvuru Linki / E-posta", key="jb_link")
                job_desc = st.text_area("İlan Açıklaması", height=80, key="jb_aciklama")
                job_kaynak_mezun = st.text_input("Paylaşan Mezun (opsiyonel)", key="jb_mezun")

                job_submit = st.form_submit_button("💼 İlan Kaydet", type="primary")
                if job_submit:
                    if not job_title.strip():
                        styled_info_banner("İlan başlığı zorunludur.", "warning")
                    else:
                        from datetime import datetime as _dt4
                        existing_jobs.append({
                            "id": f"JB-{len(existing_jobs)+1:04d}",
                            "title": job_title.strip(),
                            "ilan_turu": job_ilan_turu,
                            "company": job_company.strip(),
                            "sektor": job_sektor.strip(),
                            "sehir": job_sehir.strip(),
                            "maas": job_maas.strip(),
                            "son_basvuru": job_son_basvuru.isoformat(),
                            "basvuru_link": job_link.strip(),
                            "description": job_desc.strip(),
                            "kaynak_mezun": job_kaynak_mezun.strip(),
                            "durum": "Aktif",
                            "basvuru_sayisi": 0,
                            "created_at": _dt4.now().isoformat(),
                        })
                        save_json_list(get_job_log_path(), existing_jobs)
                        st.success("İlan kaydedildi.")
                        st.rerun()

            # Mevcut ilanlar
            if existing_jobs:
                styled_section("Yayınlanan İlanlar", "#8b5cf6")
                for idx, jb in enumerate(existing_jobs):
                    durum = jb.get("durum", jb.get("status", "Aktif"))
                    durum_icon = {"Aktif": "🟢", "Açık": "🟢", "Kapandı": "🔴", "İptal": "❌"}.get(durum, "⚪")
                    with st.expander(f"{durum_icon} {jb.get('title','')} — {jb.get('company','-')} ({jb.get('ilan_turu', '-')})"):
                        st.markdown(f"**Tür:** {jb.get('ilan_turu','-')} | **Sektör:** {jb.get('sektor','-')} | **Şehir:** {jb.get('sehir','-')}")
                        st.markdown(f"**Maaş:** {jb.get('maas','-')} | **Son Başvuru:** {jb.get('son_basvuru','-')} | **Başvuru:** {jb.get('basvuru_link','-')}")
                        if jb.get("kaynak_mezun"):
                            st.markdown(f"**Paylaşan Mezun:** {jb.get('kaynak_mezun')}")
                        if jb.get("description"):
                            st.markdown(f"**Açıklama:** {jb.get('description')}")
                        jbc1, jbc2, jbc3 = st.columns([2, 2, 1])
                        with jbc1:
                            new_jb_durum = st.selectbox("Durum", ["Aktif", "Kapandı", "İptal"],
                                                         index=["Aktif", "Kapandı", "İptal"].index(durum) if durum in ["Aktif", "Kapandı", "İptal"] else 0,
                                                         key=f"jb_dur_{idx}")
                        with jbc2:
                            if st.button("Güncelle", key=f"jb_save_{idx}", type="primary"):
                                existing_jobs[idx]["durum"] = new_jb_durum
                                save_json_list(get_job_log_path(), existing_jobs)
                                st.success("İlan güncellendi.")
                                st.rerun()
                        with jbc3:
                            if st.button("🗑️ Sil", key=f"jb_del_{idx}"):
                                existing_jobs.pop(idx)
                                save_json_list(get_job_log_path(), existing_jobs)
                                st.rerun()

    # ==================== MENTORLUK ====================
    if "MENTORLUK" in tab_map:
        with tabs[tab_map["MENTORLUK"]]:
            existing_mentors = load_json_list(get_mentorship_log_path())

            mt_aktif = sum(1 for m in existing_mentors if m.get("durum") == "Aktif")
            mt_tamamlandi = sum(1 for m in existing_mentors if m.get("durum") == "Tamamlandı")
            mt_oturum = sum(int(m.get("oturum_sayisi", 0)) for m in existing_mentors)
            styled_stat_row([
                ("Toplam Eşleşme", len(existing_mentors), "#0d9488", "🤝"),
                ("Aktif", mt_aktif, "#10b981", "🟢"),
                ("Tamamlandı", mt_tamamlandi, "#8b5cf6", "✅"),
                ("Toplam Oturum", mt_oturum, "#f59e0b", "📅"),
            ])

            styled_section("Mentor Kriterleri (Referans)", "#0d9488")
            if df_mentors.empty:
                styled_info_banner("Mentor kriter verisi bulunamadı.", "info")
            else:
                st.dataframe(df_mentors, use_container_width=True, hide_index=True)

            styled_section("Yeni Mentorluk Eşleştirmesi", "#10b981")
            with st.form("mentor_form", clear_on_submit=True):
                mt_c1, mt_c2 = st.columns(2)
                with mt_c1:
                    mentor_title = st.text_input("Başlık / Konu *")
                    mentor_ad = st.text_input("Mentor (Mezun) Adı")
                    mentor_id = st.text_input("Mentor Mezun ID")
                    mentor_alan = st.text_input("Uzmanlık Alanı")
                with mt_c2:
                    mentee_ad = st.text_input("Mentee (Öğrenci/Mezun) Adı")
                    mentee_sinif = st.text_input("Mentee Sınıf / Bölüm")
                    kriter = st.selectbox(
                        "Kriter",
                        df_mentors["KriterAdi"].astype(str).tolist() if "KriterAdi" in df_mentors.columns else ["Kariyer Yönlendirme", "Akademik Destek", "Sektör Deneyimi", "Kişisel Gelişim", "Diğer"],
                    )
                    mentor_sure = st.selectbox("Planlanan Süre", ["1 Ay", "3 Ay", "6 Ay", "1 Yıl"], key="mt_sure")
                mentor_notes = st.text_area("Notlar / Hedefler", height=60, key="mt_notlar")

                mentor_submit = st.form_submit_button("🤝 Eşleştirme Kaydet", type="primary")
                if mentor_submit:
                    if not mentor_title.strip():
                        styled_info_banner("Başlık zorunludur.", "warning")
                    else:
                        from datetime import datetime as _dt5
                        existing_mentors.append({
                            "id": f"MT-{len(existing_mentors)+1:04d}",
                            "title": mentor_title.strip(),
                            "mentor_ad": mentor_ad.strip(),
                            "mentor_id": mentor_id.strip(),
                            "mentor_alan": mentor_alan.strip(),
                            "mentee_ad": mentee_ad.strip(),
                            "mentee_sinif": mentee_sinif.strip(),
                            "kriter": kriter,
                            "sure": mentor_sure,
                            "durum": "Aktif",
                            "oturum_sayisi": 0,
                            "notes": mentor_notes.strip(),
                            "created_at": _dt5.now().isoformat(),
                        })
                        save_json_list(get_mentorship_log_path(), existing_mentors)
                        st.success("Mentorluk eşleştirmesi kaydedildi.")
                        st.rerun()

            # Mevcut eşleştirmeler
            if existing_mentors:
                styled_section("Mentorluk Eşleştirmeleri", "#8b5cf6")
                for idx, mt in enumerate(existing_mentors):
                    durum = mt.get("durum", "Aktif")
                    durum_icon = {"Aktif": "🟢", "Askıda": "⏸️", "Tamamlandı": "✅", "İptal": "❌"}.get(durum, "⚪")
                    with st.expander(f"{durum_icon} {mt.get('title', mt.get('kriter',''))} — {mt.get('mentor_ad','-')} ↔ {mt.get('mentee_ad','-')}"):
                        st.markdown(f"**Mentor:** {mt.get('mentor_ad','-')} (ID: {mt.get('mentor_id','-')}) | **Alan:** {mt.get('mentor_alan','-')}")
                        st.markdown(f"**Mentee:** {mt.get('mentee_ad','-')} | **Sınıf/Bölüm:** {mt.get('mentee_sinif','-')}")
                        st.markdown(f"**Kriter:** {mt.get('kriter','-')} | **Süre:** {mt.get('sure','-')} | **Oturum:** {mt.get('oturum_sayisi',0)}")
                        if mt.get("notes"):
                            st.markdown(f"**Notlar:** {mt.get('notes')}")
                        mtc1, mtc2, mtc3, mtc4 = st.columns([2, 1, 1, 1])
                        with mtc1:
                            new_mt_durum = st.selectbox("Durum", ["Aktif", "Askıda", "Tamamlandı", "İptal"],
                                                         index=["Aktif", "Askıda", "Tamamlandı", "İptal"].index(durum) if durum in ["Aktif", "Askıda", "Tamamlandı", "İptal"] else 0,
                                                         key=f"mt_dur_{idx}")
                        with mtc2:
                            new_mt_oturum = st.number_input("Oturum", min_value=0, value=int(mt.get("oturum_sayisi", 0)), key=f"mt_ot_{idx}")
                        with mtc3:
                            if st.button("Güncelle", key=f"mt_save_{idx}", type="primary"):
                                existing_mentors[idx]["durum"] = new_mt_durum
                                existing_mentors[idx]["oturum_sayisi"] = new_mt_oturum
                                save_json_list(get_mentorship_log_path(), existing_mentors)
                                st.success("Güncellendi.")
                                st.rerun()
                        with mtc4:
                            if st.button("🗑️", key=f"mt_del_{idx}"):
                                existing_mentors.pop(idx)
                                save_json_list(get_mentorship_log_path(), existing_mentors)
                                st.rerun()

    # ==================== TAVSIYE KAYIT ====================
    if "TAVSIYE_KAYIT_ADAYI" in tab_map:
        with tabs[tab_map["TAVSIYE_KAYIT_ADAYI"]]:
            styled_section("Tavsiye Kayıt Adayı", "#f59e0b")
            styled_info_banner(
                "Mezunlarınızın tavsiye ettiği potansiyel öğrenci adayları bu ekranda yönetilir.",
                "info", "📣",
            )

            tavsiye_list = load_json_list(get_tavsiye_log_path())

            # İstatistik
            tv_bekleyen = sum(1 for t in tavsiye_list if t.get("durum") == "Bekliyor")
            tv_gorusuldu = sum(1 for t in tavsiye_list if t.get("durum") == "Görüşüldü")
            tv_kayit = sum(1 for t in tavsiye_list if t.get("durum") == "Kayıt Oldu")
            styled_stat_row([
                ("Toplam Aday", len(tavsiye_list), "#f59e0b", "📣"),
                ("Bekliyor", tv_bekleyen, "#2563eb", "⏳"),
                ("Görüşüldü", tv_gorusuldu, "#8b5cf6", "📞"),
                ("Kayıt Oldu", tv_kayit, "#10b981", "✅"),
            ])

            styled_section("Yeni Tavsiye Adayı", "#10b981")
            with st.form("tavsiye_form", clear_on_submit=True):
                tv_c1, tv_c2 = st.columns(2)
                with tv_c1:
                    tv_aday_ad = st.text_input("Aday Ad Soyad *")
                    tv_aday_tel = st.text_input("Aday Telefon")
                    tv_aday_email = st.text_input("Aday E-posta")
                    tv_kademe = st.selectbox("Hedef Kademe", ["İlkokul", "Ortaokul", "Lise"], key="tv_kademe")
                with tv_c2:
                    tv_tavsiye_eden = st.text_input("Tavsiye Eden Mezun")
                    tv_tavsiye_mezun_id = st.text_input("Tavsiye Eden Mezun ID")
                    tv_yakinlik = st.selectbox("Yakınlık", ["Aile", "Arkadaş", "Komşu", "İş Arkadaşı", "Diğer"], key="tv_yakinlik")
                    tv_sinif = st.text_input("Hedef Sınıf/Yıl")
                tv_notlar = st.text_area("Notlar", height=80)

                if st.form_submit_button("📣 Aday Kaydet", type="primary"):
                    if not tv_aday_ad.strip():
                        styled_info_banner("Aday adı zorunludur.", "warning")
                    else:
                        from datetime import datetime as _dt
                        tavsiye_list.append({
                            "id": f"TV-{len(tavsiye_list)+1:04d}",
                            "aday_ad": tv_aday_ad.strip(),
                            "aday_telefon": tv_aday_tel.strip(),
                            "aday_email": tv_aday_email.strip(),
                            "kademe": tv_kademe,
                            "sinif": tv_sinif.strip(),
                            "tavsiye_eden": tv_tavsiye_eden.strip(),
                            "tavsiye_eden_id": tv_tavsiye_mezun_id.strip(),
                            "yakinlik": tv_yakinlik,
                            "durum": "Bekliyor",
                            "notlar": tv_notlar.strip(),
                            "created_at": _dt.now().isoformat(),
                        })
                        save_json_list(get_tavsiye_log_path(), tavsiye_list)
                        st.success("Tavsiye adayı kaydedildi.")
                        st.rerun()

            # Mevcut adaylar
            if tavsiye_list:
                styled_section("Tavsiye Adayları", "#f59e0b")
                for idx, tv in enumerate(tavsiye_list):
                    durum_icon = {"Bekliyor": "⏳", "Görüşüldü": "📞", "Kayıt Oldu": "✅", "Reddedildi": "❌"}.get(tv.get("durum", ""), "⚪")
                    with st.expander(f"{durum_icon} {tv.get('aday_ad','')} — {tv.get('kademe','')} ({tv.get('durum','')})"):
                        st.markdown(f"**Tavsiye Eden:** {tv.get('tavsiye_eden','-')} (ID: {tv.get('tavsiye_eden_id','-')}) | **Yakınlık:** {tv.get('yakinlik','-')}")
                        st.markdown(f"**Telefon:** {tv.get('aday_telefon','-')} | **E-posta:** {tv.get('aday_email','-')} | **Sınıf:** {tv.get('sinif','-')}")
                        if tv.get("notlar"):
                            st.markdown(f"**Notlar:** {tv.get('notlar')}")
                        tc1, tc2, tc3 = st.columns([2, 2, 1])
                        with tc1:
                            new_durum = st.selectbox("Durum", ["Bekliyor", "Görüşüldü", "Kayıt Oldu", "Reddedildi"],
                                                      index=["Bekliyor", "Görüşüldü", "Kayıt Oldu", "Reddedildi"].index(tv.get("durum", "Bekliyor")) if tv.get("durum", "Bekliyor") in ["Bekliyor", "Görüşüldü", "Kayıt Oldu", "Reddedildi"] else 0,
                                                      key=f"tv_dur_{idx}")
                        with tc2:
                            if st.button("Güncelle", key=f"tv_save_{idx}", type="primary"):
                                tavsiye_list[idx]["durum"] = new_durum
                                save_json_list(get_tavsiye_log_path(), tavsiye_list)
                                st.success("Durum güncellendi.")
                                st.rerun()
                        with tc3:
                            if st.button("🗑️ Sil", key=f"tv_del_{idx}"):
                                tavsiye_list.pop(idx)
                                save_json_list(get_tavsiye_log_path(), tavsiye_list)
                                st.rerun()

    # ==================== BAGIS & SPONSORLUK ====================
    if "BAGIS_SPONSORLUK" in tab_map:
        with tabs[tab_map["BAGIS_SPONSORLUK"]]:
            styled_section("Bağış & Sponsorluk", "#ec4899")
            styled_info_banner(
                "Mezunlarınızdan gelen bağış ve sponsorluk kayıtları bu ekranda takip edilir.",
                "info", "💎",
            )

            bagis_list = load_json_list(get_bagis_log_path())

            # İstatistik
            toplam_tutar = sum(float(b.get("tutar", 0)) for b in bagis_list)
            bagis_count = sum(1 for b in bagis_list if b.get("tur") == "Bağış")
            sponsor_count = sum(1 for b in bagis_list if b.get("tur") == "Sponsorluk")
            styled_stat_row([
                ("Toplam Kayıt", len(bagis_list), "#ec4899", "💎"),
                ("Bağış", bagis_count, "#10b981", "🎁"),
                ("Sponsorluk", sponsor_count, "#8b5cf6", "🤝"),
                ("Toplam Tutar", f"₺{toplam_tutar:,.0f}", "#f59e0b", "💰"),
            ])

            styled_section("Yeni Bağış / Sponsorluk", "#10b981")
            with st.form("bagis_form", clear_on_submit=True):
                bg_c1, bg_c2 = st.columns(2)
                with bg_c1:
                    bg_tur = st.selectbox("Tür", ["Bağış", "Sponsorluk"], key="bg_tur")
                    bg_mezun = st.text_input("Mezun Adı")
                    bg_mezun_id = st.text_input("Mezun ID")
                    bg_tutar = st.number_input("Tutar (₺)", min_value=0.0, value=0.0, step=100.0, key="bg_tutar")
                with bg_c2:
                    bg_konu = st.text_input("Konu / Amaç")
                    bg_tarih = st.date_input("Tarih", key="bg_tarih")
                    bg_odeme = st.selectbox("Ödeme Yöntemi", ["Havale/EFT", "Kredi Kartı", "Nakit", "Diğer"], key="bg_odeme")
                    bg_durum = st.selectbox("Durum", ["Taahhüt", "Ödendi", "Kısmi Ödeme", "İptal"], key="bg_durum")
                bg_not = st.text_area("Notlar", height=60, key="bg_not")

                if st.form_submit_button("💎 Kaydet", type="primary"):
                    if not bg_mezun.strip():
                        styled_info_banner("Mezun adı zorunludur.", "warning")
                    elif bg_tutar <= 0:
                        styled_info_banner("Tutar sıfırdan büyük olmalıdır.", "warning")
                    else:
                        from datetime import datetime as _dt2
                        bagis_list.append({
                            "id": f"BG-{len(bagis_list)+1:04d}",
                            "tur": bg_tur,
                            "mezun": bg_mezun.strip(),
                            "mezun_id": bg_mezun_id.strip(),
                            "tutar": bg_tutar,
                            "konu": bg_konu.strip(),
                            "tarih": bg_tarih.isoformat(),
                            "odeme_yontemi": bg_odeme,
                            "durum": bg_durum,
                            "notlar": bg_not.strip(),
                            "created_at": _dt2.now().isoformat(),
                        })
                        save_json_list(get_bagis_log_path(), bagis_list)
                        st.success("Bağış/Sponsorluk kaydedildi.")
                        st.rerun()

            # Mevcut kayıtlar
            if bagis_list:
                styled_section("Bağış & Sponsorluk Kayıtları", "#ec4899")
                for idx, bg in enumerate(bagis_list):
                    tur_icon = "🎁" if bg.get("tur") == "Bağış" else "🤝"
                    durum_icon = {"Taahhüt": "⏳", "Ödendi": "✅", "Kısmi Ödeme": "🔄", "İptal": "❌"}.get(bg.get("durum", ""), "⚪")
                    with st.expander(f"{tur_icon} {bg.get('mezun','')} — ₺{bg.get('tutar',0):,.0f} {durum_icon} ({bg.get('durum','')})"):
                        st.markdown(f"**Tür:** {bg.get('tur','')} | **Konu:** {bg.get('konu','-')} | **Tarih:** {bg.get('tarih','-')}")
                        st.markdown(f"**Mezun ID:** {bg.get('mezun_id','-')} | **Ödeme:** {bg.get('odeme_yontemi','-')}")
                        if bg.get("notlar"):
                            st.markdown(f"**Notlar:** {bg.get('notlar')}")
                        bgc1, bgc2, bgc3 = st.columns([2, 2, 1])
                        with bgc1:
                            new_bg_durum = st.selectbox("Durum", ["Taahhüt", "Ödendi", "Kısmi Ödeme", "İptal"],
                                                         index=["Taahhüt", "Ödendi", "Kısmi Ödeme", "İptal"].index(bg.get("durum", "Taahhüt")) if bg.get("durum", "Taahhüt") in ["Taahhüt", "Ödendi", "Kısmi Ödeme", "İptal"] else 0,
                                                         key=f"bg_dur_{idx}")
                        with bgc2:
                            if st.button("Güncelle", key=f"bg_save_{idx}", type="primary"):
                                bagis_list[idx]["durum"] = new_bg_durum
                                save_json_list(get_bagis_log_path(), bagis_list)
                                st.success("Durum güncellendi.")
                                st.rerun()
                        with bgc3:
                            if st.button("🗑️ Sil", key=f"bg_del_{idx}"):
                                bagis_list.pop(idx)
                                save_json_list(get_bagis_log_path(), bagis_list)
                                st.rerun()

    # ==================== AYARLAR ====================
    if "AYARLAR" in tab_map:
        with tabs[tab_map["AYARLAR"]]:
            styled_section("Genel Ayarlar", "#64748b")
            if df_settings.empty:
                styled_info_banner("Ayarlar verisi bulunamadı.", "info")
            else:
                st.dataframe(df_settings, use_container_width=True, hide_index=True)

            if not df_bilesen.empty:
                styled_section("Bilesen Ac / Kapat", "#2563eb")
                updated = False
                for _, row in df_bilesen.iterrows():
                    code = str(row.get("BilesenKodu", "")).strip()
                    name = str(row.get("BilesenAdi", "")).strip()
                    if not code:
                        continue
                    value = component_settings.get(code, False)
                    new_value = st.checkbox(
                        f"{name} ({code})",
                        value=value,
                        key=f"component_toggle_{code}",
                    )
                    if new_value != value:
                        component_settings[code] = new_value
                        updated = True
                if updated:
                    save_component_settings(component_settings)
                    st.success("✅ Bilesen ayarlari güncellendi.")

    # ==================== SMARTI ====================
    if "SMARTI" in tab_map:
        with tabs[tab_map["SMARTI"]]:
            def _mez_smarti_context():
                try:
                    mezun_count = len(load_json_list(get_alumni_store_path()))
                    event_count = len(load_json_list(get_event_log_path()))
                    mentoring_count = len(load_json_list(get_mentorship_log_path()))
                    return (
                        f"Mezun kaydı: {mezun_count}, Etkinlik kaydı: {event_count}, "
                        f"Mentorluk kaydı: {mentoring_count}"
                    )
                except Exception:
                    return ""
            render_smarti_chat("alumni_career", _mez_smarti_context)
