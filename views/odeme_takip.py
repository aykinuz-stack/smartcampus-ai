"""
Odeme Takip Modulu - UI
========================
Kolej ucret yonetimi, taksit planlari, odeme takibi,
tahsilat raporlari ve borc yonetimi.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from models.odeme_takip import (
    OdemeDataStore, UcretKalemi, TaksitPlani, Taksit, OdemeKaydi,
)
from utils.ui_common import (
    inject_common_css, styled_header, styled_section,
    styled_stat_row, styled_info_banner,
)

# ══════════════════════════════════════════════════════════════
# SABITLER
# ══════════════════════════════════════════════════════════════

ODEME_YONTEMLERI = ["Nakit", "Havale/EFT", "Kredi Karti", "POS", "Diger"]
ODEME_YONTEM_MAP = {
    "Nakit": "nakit", "Havale/EFT": "havale", "Kredi Karti": "kredi_karti",
    "POS": "pos", "Diger": "diger",
}
ODEME_YONTEM_REVERSE = {v: k for k, v in ODEME_YONTEM_MAP.items()}

UCRET_KATEGORILERI = [
    "Ogretim Ucreti", "Yemek", "Servis", "Kiyafet",
    "Etkinlik", "Materyal", "Diger",
]
KATEGORI_MAP = {
    "Ogretim Ucreti": "ogretim", "Yemek": "yemek", "Servis": "servis",
    "Kiyafet": "kiyafet", "Etkinlik": "etkinlik", "Materyal": "materyal",
    "Diger": "diger",
}
KATEGORI_REVERSE = {v: k for k, v in KATEGORI_MAP.items()}

SINIFLAR = [str(i) for i in range(1, 13)]
AY_ISIMLERI = {
    1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis",
    6: "Haziran", 7: "Temmuz", 8: "Agustos", 9: "Eylul",
    10: "Ekim", 11: "Kasim", 12: "Aralik",
}

DURUM_RENK = {
    "bekliyor": "#f59e0b",
    "odendi": "#10b981",
    "gecikti": "#ef4444",
    "iptal": "#6b7280",
}
DURUM_LABEL = {
    "bekliyor": "Bekliyor",
    "odendi": "Odendi",
    "gecikti": "Gecikti",
    "iptal": "Iptal",
}
PLAN_DURUM_LABEL = {
    "aktif": "Aktif",
    "tamamlandi": "Tamamlandi",
    "iptal": "Iptal",
}


# ══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ══════════════════════════════════════════════════════════════

def _get_akademik_yil() -> str:
    today = date.today()
    if today.month >= 9:
        return f"{today.year}-{today.year + 1}"
    return f"{today.year - 1}-{today.year}"


def _get_donem_secenekleri() -> list[str]:
    yil = date.today().year
    return [f"{y}-{y+1}" for y in range(yil - 2, yil + 2)]


def _load_students() -> list[dict]:
    """data/akademik/students.json dosyasindan ogrenci listesini yukle."""
    path = os.path.join("data", "akademik", "students.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _get_store() -> OdemeDataStore:
    """Session-state tabanli singleton."""
    if "odeme_store" not in st.session_state:
        st.session_state["odeme_store"] = OdemeDataStore()
    return st.session_state["odeme_store"]


def _format_tutar(tutar: float) -> str:
    """Para formatla: 12.500,00 TL"""
    return f"{tutar:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")


def _durum_badge(durum: str) -> str:
    """Durum icin renkli badge HTML."""
    renk = DURUM_RENK.get(durum, "#6b7280")
    label = DURUM_LABEL.get(durum, durum)
    return (
        f'<span style="background:{renk}20;color:{renk};padding:3px 10px;'
        f'border-radius:12px;font-size:0.8rem;font-weight:600;'
        f'border:1px solid {renk}40">{label}</span>'
    )


def _inject_odeme_css():
    """Odeme modulu ek CSS — metric kartlar, badge, tablo."""
    st.markdown("""<style>
    .odeme-metric {
        background: linear-gradient(135deg, #131825, #1a2035);
        padding: 20px; border-radius: 12px;
        border-left: 4px solid #6366F1;
        border: 1px solid rgba(99,102,241,.12);
        text-align: center; transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,.2);
    }
    .odeme-metric:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.3); }
    .odeme-metric .value { font-size: 1.8rem; font-weight: 800; color: #e2e8f0; margin: 0; }
    .odeme-metric .label { font-size: 0.8rem; color: #94a3b8; margin-top: 4px;
        text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
    .odeme-metric.green { border-left-color: #10b981; }
    .odeme-metric.red { border-left-color: #ef4444; }
    .odeme-metric.yellow { border-left-color: #f59e0b; }
    .odeme-metric.purple { border-left-color: #7c3aed; }
    .odeme-warning-banner {
        background: rgba(239,68,68,.08); border-left: 4px solid #ef4444;
        padding: 14px 18px; border-radius: 10px; margin: 12px 0;
        color: #fca5a5; font-weight: 500;
    }
    .taksit-row {
        display: flex; align-items: center; gap: 12px;
        padding: 10px 14px; border-radius: 8px; margin: 4px 0;
        background: rgba(15,20,32,.6); border: 1px solid rgba(99,102,241,.08);
    }
    .taksit-row:hover { background: rgba(99,102,241,.05); }
    </style>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ══════════════════════════════════════════════════════════════

def _render_dashboard(store: OdemeDataStore):
    """Ana dashboard — ozet metrikler + tahsilat trendi."""
    donem = _get_akademik_yil()

    styled_header("Odeme Dashboard", f"{donem} donemi genel ozet", icon="", accent_color="#6366F1")

    ozet = store.get_odeme_ozet(donem=donem)

    # --- Metrik kartlar ---
    tahsilat_orani = ozet.get("tahsilat_orani", 0)
    styled_stat_row([
        ("Toplam Borc", _format_tutar(ozet.get("toplam_borc", 0)), "#6366F1", "$"),
        ("Odenen", _format_tutar(ozet.get("toplam_odenen", 0)), "#10b981", "$"),
        ("Kalan Borc", _format_tutar(ozet.get("kalan_borc", 0)), "#f59e0b", "$"),
        ("Tahsilat Orani", f"%{tahsilat_orani}", "#7c3aed", "$"),
    ])

    # --- Geciken tutar uyarisi ---
    geciken = ozet.get("geciken_tutar", 0)
    if geciken > 0:
        styled_info_banner(
            f"Geciken toplam tutar: {_format_tutar(geciken)} — "
            f"{ozet.get('toplam_ogrenci', 0)} ogrenci planinda gecikme mevcut.",
            banner_type="error", icon="!"
        )

    st.markdown("---")

    # --- Tahsilat trendi (aylik) ---
    styled_section("Aylik Tahsilat Trendi", "#6366F1")

    kayitlar = store.get_odeme_kayitlari()
    if kayitlar:
        df_kayit = pd.DataFrame(kayitlar)
        df_kayit["ay"] = pd.to_datetime(df_kayit["odeme_tarihi"], errors="coerce").dt.to_period("M")
        aylik = df_kayit.groupby("ay")["tutar"].sum().reset_index()
        aylik.columns = ["Ay", "Tahsilat"]
        aylik["Ay"] = aylik["Ay"].astype(str)
        st.bar_chart(aylik.set_index("Ay"), use_container_width=True)
    else:
        # Mock data for empty state
        mock_aylar = []
        bugun = date.today()
        for i in range(6):
            ay = bugun.month - 5 + i
            yil = bugun.year
            if ay <= 0:
                ay += 12
                yil -= 1
            mock_aylar.append({"Ay": f"{yil}-{ay:02d}", "Tahsilat": 0})
        df_mock = pd.DataFrame(mock_aylar)
        st.bar_chart(df_mock.set_index("Ay"), use_container_width=True)
        styled_info_banner("Henuz odeme kaydi bulunmuyor. Tahsilat trendi bos gorunuyor.", "info")

    # --- Hizli istatistik ---
    styled_section("Donem Ozeti", "#10b981")
    col1, col2, col3 = st.columns(3)
    planlar = store.get_taksit_planlari(donem=donem)
    aktif = sum(1 for p in planlar if p.get("durum") == "aktif")
    tamamlanan = sum(1 for p in planlar if p.get("durum") == "tamamlandi")
    col1.metric("Toplam Plan", len(planlar))
    col2.metric("Aktif Plan", aktif)
    col3.metric("Tamamlanan", tamamlanan)


# ══════════════════════════════════════════════════════════════
# TAB 2: TAKSIT PLANLARI
# ══════════════════════════════════════════════════════════════

def _render_taksit_planlari(store: OdemeDataStore):
    """Taksit planlari listesi + detay + odeme alma."""
    styled_header("Taksit Planlari", "Ogrenci bazli taksit takibi ve odeme islemleri",
                  icon="", accent_color="#2563eb")

    # --- Filtreler ---
    col_f1, col_f2 = st.columns(2)
    donemler = _get_donem_secenekleri()
    aktif_donem = _get_akademik_yil()
    default_idx = donemler.index(aktif_donem) if aktif_donem in donemler else 0
    secili_donem = col_f1.selectbox("Donem", donemler, index=default_idx, key="tp_donem")
    sinif_filtre = col_f2.selectbox("Sinif Filtresi", ["Tumu"] + SINIFLAR, key="tp_sinif")

    planlar = store.get_taksit_planlari(donem=secili_donem)
    if sinif_filtre != "Tumu":
        planlar = [p for p in planlar if str(p.get("sinif", "")) == sinif_filtre]

    if not planlar:
        styled_info_banner("Bu donem/sinif icin taksit plani bulunmuyor.", "info")
        return

    # --- Ozet tablo ---
    styled_section(f"{len(planlar)} Taksit Plani", "#2563eb")

    for plan in planlar:
        taksitler = plan.get("taksitler", [])
        odenen_toplam = sum(t.get("odeme_tutari", 0) for t in taksitler if t.get("durum") == "odendi")
        kalan = plan.get("net_tutar", 0) - odenen_toplam
        plan_durum = plan.get("durum", "aktif")

        # Plan ozet satiri
        durum_label = PLAN_DURUM_LABEL.get(plan_durum, plan_durum)
        durum_renk = {"aktif": "#2563eb", "tamamlandi": "#10b981", "iptal": "#6b7280"}.get(plan_durum, "#6b7280")

        header_text = (
            f"**{plan.get('student_adi', '?')}** — "
            f"{plan.get('sinif', '?')}/{plan.get('sube', '?')} | "
            f"Toplam: {_format_tutar(plan.get('net_tutar', 0))} | "
            f"Odenen: {_format_tutar(odenen_toplam)} | "
            f"Kalan: {_format_tutar(kalan)}"
        )

        with st.expander(header_text, expanded=False):
            # Durum badge
            st.markdown(
                f'<div style="margin-bottom:10px">'
                f'<span style="background:{durum_renk}20;color:{durum_renk};padding:4px 12px;'
                f'border-radius:12px;font-size:0.8rem;font-weight:600;'
                f'border:1px solid {durum_renk}40">{durum_label}</span>'
                f' &nbsp; Indirim: %{plan.get("indirim_orani", 0)} '
                f'({_format_tutar(plan.get("indirim_tutari", 0))})'
                f'</div>',
                unsafe_allow_html=True
            )

            # Taksit tablosu
            if taksitler:
                for t in taksitler:
                    t_durum = t.get("durum", "bekliyor")
                    vade = t.get("vade_tarihi", "")
                    # Gecikme kontrolu
                    if t_durum == "bekliyor" and vade and vade < date.today().isoformat():
                        t_durum = "gecikti"

                    renk = DURUM_RENK.get(t_durum, "#6b7280")
                    label = DURUM_LABEL.get(t_durum, t_durum)

                    cols = st.columns([1, 2, 2, 2, 2, 2])
                    cols[0].markdown(f"**{t.get('sira', '')}.**")
                    cols[1].markdown(f"{_format_tutar(t.get('tutar', 0))}")
                    cols[2].markdown(f"Vade: {vade}")
                    cols[3].markdown(
                        f'<span style="color:{renk};font-weight:600">{label}</span>',
                        unsafe_allow_html=True
                    )

                    if t_durum == "odendi":
                        cols[4].markdown(f"Odeme: {t.get('odeme_tarihi', '-')}")
                        cols[5].markdown(f"Makbuz: {t.get('makbuz_no', '-')}")
                    elif t_durum in ("bekliyor", "gecikti") and plan_durum == "aktif":
                        btn_key = f"odeme_btn_{plan.get('id')}_{t.get('id')}"
                        if cols[5].button("Odeme Al", key=btn_key, type="primary"):
                            st.session_state["odeme_form_plan"] = plan.get("id")
                            st.session_state["odeme_form_taksit"] = t.get("id")
                            st.session_state["odeme_form_tutar"] = t.get("tutar", 0)
                            st.session_state["odeme_form_ogrenci"] = plan.get("student_adi", "")

            # Odeme formu (secili taksit icin)
            if (st.session_state.get("odeme_form_plan") == plan.get("id")
                    and st.session_state.get("odeme_form_taksit")):
                st.markdown("---")
                styled_section("Odeme Al", "#10b981")
                st.info(
                    f"Ogrenci: **{st.session_state.get('odeme_form_ogrenci', '')}** | "
                    f"Taksit Tutari: {_format_tutar(st.session_state.get('odeme_form_tutar', 0))}"
                )

                form_key = f"odeme_form_{plan.get('id')}_{st.session_state.get('odeme_form_taksit')}"
                with st.form(form_key):
                    f_tutar = st.number_input(
                        "Odeme Tutari (TL)",
                        value=float(st.session_state.get("odeme_form_tutar", 0)),
                        min_value=0.0, step=0.01,
                        key=f"f_tutar_{form_key}"
                    )
                    f_yontem = st.selectbox(
                        "Odeme Yontemi", ODEME_YONTEMLERI,
                        key=f"f_yontem_{form_key}"
                    )
                    f_aciklama = st.text_input(
                        "Aciklama (opsiyonel)", "",
                        key=f"f_aciklama_{form_key}"
                    )

                    col_s, col_c = st.columns(2)
                    submitted = col_s.form_submit_button("Odemeyi Kaydet", type="primary")
                    cancelled = col_c.form_submit_button("Iptal")

                    if submitted:
                        try:
                            yontem_kod = ODEME_YONTEM_MAP.get(f_yontem, "nakit")
                            kayit = store.odeme_yap(
                                plan_id=plan.get("id"),
                                taksit_id=st.session_state["odeme_form_taksit"],
                                tutar=f_tutar,
                                yontem=yontem_kod,
                                islem_yapan="admin",
                            )
                            st.success(
                                f"Odeme basariyla kaydedildi! Makbuz No: {kayit.makbuz_no}"
                            )
                            # Formu temizle
                            st.session_state.pop("odeme_form_plan", None)
                            st.session_state.pop("odeme_form_taksit", None)
                            st.session_state.pop("odeme_form_tutar", None)
                            st.session_state.pop("odeme_form_ogrenci", None)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Odeme kaydedilemedi: {e}")

                    if cancelled:
                        st.session_state.pop("odeme_form_plan", None)
                        st.session_state.pop("odeme_form_taksit", None)
                        st.session_state.pop("odeme_form_tutar", None)
                        st.session_state.pop("odeme_form_ogrenci", None)
                        st.rerun()


# ══════════════════════════════════════════════════════════════
# TAB 3: UCRET KALEMLERI
# ══════════════════════════════════════════════════════════════

def _render_ucret_kalemleri(store: OdemeDataStore):
    """Ucret kalemleri yonetimi — CRUD."""
    styled_header("Ucret Kalemleri", "Donem bazli ucret tanimlari",
                  icon="", accent_color="#7c3aed")

    # --- Filtre ---
    donemler = _get_donem_secenekleri()
    aktif_donem = _get_akademik_yil()
    default_idx = donemler.index(aktif_donem) if aktif_donem in donemler else 0
    secili_donem = st.selectbox("Donem", donemler, index=default_idx, key="uk_donem")

    kalemler = store.get_ucret_kalemleri(donem=secili_donem)

    # --- Tablo ---
    if kalemler:
        styled_section(f"{len(kalemler)} Ucret Kalemi", "#7c3aed")

        rows = []
        for k in kalemler:
            zorunlu_badge = "Zorunlu" if k.get("zorunlu") else "Opsiyonel"
            rows.append({
                "Ad": k.get("ad", ""),
                "Kategori": KATEGORI_REVERSE.get(k.get("kategori", ""), k.get("kategori", "")),
                "Tutar": _format_tutar(k.get("tutar", 0)),
                "Zorunlu": zorunlu_badge,
                "Aciklama": k.get("aciklama", ""),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Duzenle/Sil
        secim = st.selectbox(
            "Duzenlenecek Kalem",
            ["-- Sec --"] + [k.get("ad", "") for k in kalemler],
            key="uk_edit_sec"
        )
        if secim != "-- Sec --":
            secili = next((k for k in kalemler if k.get("ad") == secim), None)
            if secili:
                _render_ucret_form(store, secili_donem, existing=secili)
    else:
        styled_info_banner("Bu donem icin ucret kalemi tanimlanmamis.", "info")

    # --- Yeni ekle ---
    st.markdown("---")
    styled_section("Yeni Ucret Kalemi Ekle", "#10b981")
    _render_ucret_form(store, secili_donem, existing=None)


def _render_ucret_form(store: OdemeDataStore, donem: str, existing: dict | None = None):
    """Ucret kalemi ekleme/duzenleme formu."""
    prefix = "edit" if existing else "new"
    form_key = f"uk_form_{prefix}_{existing.get('id', 'yeni') if existing else 'yeni'}"

    with st.form(form_key):
        default_ad = existing.get("ad", "") if existing else ""
        default_kat = existing.get("kategori", "ogretim") if existing else "ogretim"
        default_tutar = existing.get("tutar", 0.0) if existing else 0.0
        default_zorunlu = existing.get("zorunlu", True) if existing else True
        default_aciklama = existing.get("aciklama", "") if existing else ""

        kat_label = KATEGORI_REVERSE.get(default_kat, "Ogretim Ucreti")
        kat_idx = UCRET_KATEGORILERI.index(kat_label) if kat_label in UCRET_KATEGORILERI else 0

        f_ad = st.text_input("Ucret Kalemi Adi", value=default_ad, key=f"uk_ad_{form_key}")
        f_kat = st.selectbox("Kategori", UCRET_KATEGORILERI, index=kat_idx, key=f"uk_kat_{form_key}")
        f_tutar = st.number_input("Tutar (TL)", value=float(default_tutar),
                                   min_value=0.0, step=100.0, key=f"uk_tutar_{form_key}")
        f_zorunlu = st.checkbox("Zorunlu", value=default_zorunlu, key=f"uk_zorunlu_{form_key}")
        f_aciklama = st.text_input("Aciklama", value=default_aciklama, key=f"uk_aciklama_{form_key}")

        btn_label = "Guncelle" if existing else "Ekle"
        submitted = st.form_submit_button(btn_label, type="primary")

        if submitted:
            if not f_ad.strip():
                st.error("Ucret kalemi adi bos olamaz.")
                return
            kalemi = UcretKalemi(
                id=existing.get("id", "") if existing else "",
                ad=f_ad.strip(),
                kategori=KATEGORI_MAP.get(f_kat, "diger"),
                tutar=f_tutar,
                donem=donem,
                aciklama=f_aciklama,
                zorunlu=f_zorunlu,
            )
            store.save_ucret_kalemi(kalemi)
            st.success(f"Ucret kalemi {'guncellendi' if existing else 'eklendi'}: {f_ad}")
            st.rerun()


# ══════════════════════════════════════════════════════════════
# TAB 4: YENI PLAN OLUSTUR
# ══════════════════════════════════════════════════════════════

def _render_yeni_plan(store: OdemeDataStore):
    """Yeni taksit plani olusturma wizardi."""
    styled_header("Yeni Taksit Plani", "Ogrenci icin taksit plani olusturun",
                  icon="", accent_color="#059669")

    students = _load_students()
    if not students:
        styled_info_banner(
            "Ogrenci verisi bulunamadi (data/akademik/students.json). "
            "Oncelikle Akademik Takip modulunden ogrenci giriniz.", "warning"
        )
        return

    # --- Ogrenci secimi ---
    aktif_ogrenciler = [s for s in students if s.get("durum", "aktif") == "aktif"]
    ogrenci_options = {
        f"{s.get('ad', '')} {s.get('soyad', '')} — {s.get('sinif', '')}/{s.get('sube', '')} ({s.get('numara', '')})": s
        for s in aktif_ogrenciler
    }

    if not ogrenci_options:
        styled_info_banner("Aktif ogrenci bulunamadi.", "warning")
        return

    secili_ogrenci_label = st.selectbox(
        "Ogrenci Secin", list(ogrenci_options.keys()), key="yp_ogrenci"
    )
    secili_ogrenci = ogrenci_options.get(secili_ogrenci_label, {})

    # --- Plan parametreleri ---
    col1, col2 = st.columns(2)
    donemler = _get_donem_secenekleri()
    aktif_donem = _get_akademik_yil()
    default_idx = donemler.index(aktif_donem) if aktif_donem in donemler else 0
    secili_donem = col1.selectbox("Donem", donemler, index=default_idx, key="yp_donem")

    # Ucret kalemleri toplamini oner
    kalemler = store.get_ucret_kalemleri(donem=secili_donem)
    zorunlu_toplam = sum(k.get("tutar", 0) for k in kalemler if k.get("zorunlu"))
    tum_toplam = sum(k.get("tutar", 0) for k in kalemler)

    if kalemler:
        st.info(
            f"Donem ucret kalemleri — Zorunlu: {_format_tutar(zorunlu_toplam)} | "
            f"Toplam: {_format_tutar(tum_toplam)}"
        )

    varsayilan_tutar = zorunlu_toplam if zorunlu_toplam > 0 else 50000.0

    toplam_tutar = col2.number_input(
        "Toplam Tutar (TL)", value=varsayilan_tutar,
        min_value=0.0, step=1000.0, key="yp_toplam"
    )

    col3, col4 = st.columns(2)
    taksit_sayisi = col3.number_input(
        "Taksit Sayisi", value=10, min_value=1, max_value=24, step=1, key="yp_taksit"
    )
    indirim_orani = col4.number_input(
        "Indirim Orani (%)", value=0.0, min_value=0.0, max_value=100.0,
        step=5.0, key="yp_indirim"
    )

    baslangic_ay = st.selectbox(
        "Baslangic Ayi",
        options=list(range(1, 13)),
        format_func=lambda x: AY_ISIMLERI.get(x, str(x)),
        index=8,  # Eylul (index 8 = value 9)
        key="yp_baslangic_ay"
    )

    # --- On izleme ---
    st.markdown("---")
    styled_section("Taksit On Izleme", "#059669")

    indirim_tutari = toplam_tutar * indirim_orani / 100
    net_tutar = toplam_tutar - indirim_tutari

    col_o1, col_o2, col_o3 = st.columns(3)
    col_o1.metric("Toplam Tutar", _format_tutar(toplam_tutar))
    col_o2.metric("Indirim", _format_tutar(indirim_tutari))
    col_o3.metric("Net Tutar", _format_tutar(net_tutar))

    if taksit_sayisi > 0 and net_tutar > 0:
        aylik = round(net_tutar / taksit_sayisi, 2)
        donem_yil = int(secili_donem.split("-")[0]) if "-" in secili_donem else date.today().year

        preview_rows = []
        for i in range(taksit_sayisi):
            ay = (baslangic_ay + i - 1) % 12 + 1
            t_yil = donem_yil if ay >= baslangic_ay else donem_yil + 1
            vade = f"{t_yil}-{ay:02d}-15"
            preview_rows.append({
                "Sira": i + 1,
                "Ay": AY_ISIMLERI.get(ay, str(ay)),
                "Tutar": _format_tutar(aylik),
                "Vade Tarihi": vade,
            })
        df_preview = pd.DataFrame(preview_rows)
        st.dataframe(df_preview, use_container_width=True, hide_index=True)

    # --- Olustur butonu ---
    st.markdown("")
    if st.button("Taksit Planini Olustur", type="primary", key="yp_olustur"):
        if toplam_tutar <= 0:
            st.error("Toplam tutar sifirdan buyuk olmalidir.")
            return

        # Mevcut plan kontrolu
        mevcut = store.get_taksit_planlari(
            student_id=secili_ogrenci.get("id", ""), donem=secili_donem
        )
        aktif_mevcut = [p for p in mevcut if p.get("durum") == "aktif"]
        if aktif_mevcut:
            st.warning(
                f"Bu ogrencinin {secili_donem} doneminde zaten aktif bir plani var. "
                f"Yeni plan olusturmak icin mevcut plani iptal edin."
            )
            return

        plan = store.taksit_plani_olustur(
            student_id=secili_ogrenci.get("id", ""),
            student_adi=f"{secili_ogrenci.get('ad', '')} {secili_ogrenci.get('soyad', '')}",
            sinif=str(secili_ogrenci.get("sinif", "")),
            sube=secili_ogrenci.get("sube", ""),
            donem=secili_donem,
            toplam=toplam_tutar,
            taksit_sayisi=taksit_sayisi,
            indirim_orani=indirim_orani,
            baslangic_ay=baslangic_ay,
        )
        st.success(
            f"Taksit plani olusturuldu! "
            f"Ogrenci: {plan.student_adi} | Net: {_format_tutar(plan.net_tutar)} | "
            f"{plan.taksit_sayisi} taksit"
        )
        st.balloons()


# ══════════════════════════════════════════════════════════════
# TAB 5: ODEME GECMISI
# ══════════════════════════════════════════════════════════════

def _render_odeme_gecmisi(store: OdemeDataStore):
    """Odeme gecmisi — filtreleme + export."""
    styled_header("Odeme Gecmisi", "Tum odeme kayitlarinin takibi",
                  icon="", accent_color="#0d9488")

    # --- Filtreler ---
    col_f1, col_f2 = st.columns(2)
    bugun = date.today()
    baslangic = col_f1.date_input(
        "Baslangic Tarihi",
        value=bugun - timedelta(days=90),
        key="og_baslangic"
    )
    bitis = col_f2.date_input(
        "Bitis Tarihi",
        value=bugun,
        key="og_bitis"
    )

    # Ogrenci filtresi
    students = _load_students()
    ogrenci_isimleri = ["Tumu"] + [
        f"{s.get('ad', '')} {s.get('soyad', '')} ({s.get('id', '')})"
        for s in students
    ]
    secili_ogrenci = st.selectbox("Ogrenci Filtresi", ogrenci_isimleri, key="og_ogrenci")

    # Veri cek
    student_id_filter = ""
    if secili_ogrenci != "Tumu" and "(" in secili_ogrenci:
        student_id_filter = secili_ogrenci.split("(")[-1].rstrip(")")

    kayitlar = store.get_odeme_kayitlari(student_id=student_id_filter)

    # Tarih filtresi
    baslangic_str = baslangic.isoformat()
    bitis_str = bitis.isoformat()
    kayitlar = [
        k for k in kayitlar
        if baslangic_str <= k.get("odeme_tarihi", "")[:10] <= bitis_str
    ]

    if not kayitlar:
        styled_info_banner("Secili filtrelere uygun odeme kaydi bulunamadi.", "info")
        return

    styled_section(f"{len(kayitlar)} Odeme Kaydi", "#0d9488")

    # Ogrenci ad'ini coz (student_id -> isim)
    student_map = {s.get("id", ""): f"{s.get('ad', '')} {s.get('soyad', '')}" for s in students}

    rows = []
    for k in kayitlar:
        rows.append({
            "Tarih": k.get("odeme_tarihi", "")[:10],
            "Ogrenci": student_map.get(k.get("student_id", ""), k.get("student_id", "")),
            "Tutar": _format_tutar(k.get("tutar", 0)),
            "Yontem": ODEME_YONTEM_REVERSE.get(k.get("odeme_yontemi", ""), k.get("odeme_yontemi", "")),
            "Makbuz No": k.get("makbuz_no", "-"),
            "Islem Yapan": k.get("islem_yapan", "-"),
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Toplam ---
    toplam = sum(k.get("tutar", 0) for k in kayitlar)
    st.markdown(f"**Toplam Tahsilat:** {_format_tutar(toplam)}")

    # --- CSV Export ---
    st.markdown("---")
    csv_data = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        "CSV Olarak Indir",
        data=csv_data,
        file_name=f"odeme_gecmisi_{baslangic_str}_{bitis_str}.csv",
        mime="text/csv",
        key="og_csv_export"
    )


# ══════════════════════════════════════════════════════════════
# TAB 6: RAPORLAR
# ══════════════════════════════════════════════════════════════

def _render_raporlar(store: OdemeDataStore):
    """Tahsilat raporlari — sinif bazli, geciken, indirim."""
    styled_header("Odeme Raporlari", "Detayli analiz ve raporlama",
                  icon="", accent_color="#ec4899")

    donemler = _get_donem_secenekleri()
    aktif_donem = _get_akademik_yil()
    default_idx = donemler.index(aktif_donem) if aktif_donem in donemler else 0
    secili_donem = st.selectbox("Donem", donemler, index=default_idx, key="rp_donem")

    planlar = store.get_taksit_planlari(donem=secili_donem)

    if not planlar:
        styled_info_banner("Bu donem icin veri bulunmuyor.", "info")
        return

    # ---- 1) Sinif Bazli Tahsilat Ozeti ----
    styled_section("Sinif Bazli Tahsilat Ozeti", "#2563eb")

    sinif_data = {}
    for p in planlar:
        sinif = str(p.get("sinif", "?"))
        if sinif not in sinif_data:
            sinif_data[sinif] = {"toplam_borc": 0, "toplam_odenen": 0, "ogrenci_sayisi": 0}
        sinif_data[sinif]["toplam_borc"] += p.get("net_tutar", 0)
        sinif_data[sinif]["ogrenci_sayisi"] += 1
        for t in p.get("taksitler", []):
            if t.get("durum") == "odendi":
                sinif_data[sinif]["toplam_odenen"] += t.get("odeme_tutari", 0)

    sinif_rows = []
    for sinif in sorted(sinif_data.keys(), key=lambda x: int(x) if x.isdigit() else 99):
        d = sinif_data[sinif]
        kalan = d["toplam_borc"] - d["toplam_odenen"]
        oran = round(d["toplam_odenen"] / max(d["toplam_borc"], 1) * 100, 1)
        sinif_rows.append({
            "Sinif": f"{sinif}. Sinif",
            "Ogrenci Sayisi": d["ogrenci_sayisi"],
            "Toplam Borc": _format_tutar(d["toplam_borc"]),
            "Odenen": _format_tutar(d["toplam_odenen"]),
            "Kalan": _format_tutar(kalan),
            "Tahsilat %": f"%{oran}",
        })

    if sinif_rows:
        df_sinif = pd.DataFrame(sinif_rows)
        st.dataframe(df_sinif, use_container_width=True, hide_index=True)

    # ---- 2) Geciken Odemeler ----
    st.markdown("---")
    styled_section("Geciken Odemeler", "#ef4444")

    bugun = date.today().isoformat()
    geciken_rows = []
    for p in planlar:
        if p.get("durum") == "iptal":
            continue
        for t in p.get("taksitler", []):
            vade = t.get("vade_tarihi", "")
            if t.get("durum") in ("bekliyor", "gecikti") and vade and vade < bugun:
                gecik_gun = (date.today() - date.fromisoformat(vade)).days
                geciken_rows.append({
                    "Ogrenci": p.get("student_adi", "?"),
                    "Sinif": f"{p.get('sinif', '?')}/{p.get('sube', '?')}",
                    "Taksit No": t.get("sira", 0),
                    "Tutar": _format_tutar(t.get("tutar", 0)),
                    "Vade Tarihi": vade,
                    "Gecikme (Gun)": gecik_gun,
                })

    if geciken_rows:
        # Gecikme gunune gore sirala (coktan aza)
        geciken_rows.sort(key=lambda x: x["Gecikme (Gun)"], reverse=True)
        df_geciken = pd.DataFrame(geciken_rows)
        st.dataframe(
            df_geciken,
            use_container_width=True, hide_index=True,
            column_config={
                "Gecikme (Gun)": st.column_config.NumberColumn(format="%d gun"),
            }
        )
        toplam_geciken = sum(
            t.get("tutar", 0)
            for p in planlar if p.get("durum") != "iptal"
            for t in p.get("taksitler", [])
            if t.get("durum") in ("bekliyor", "gecikti")
            and t.get("vade_tarihi", "") < bugun
        )
        st.error(f"Toplam geciken tutar: {_format_tutar(toplam_geciken)}")
    else:
        styled_info_banner("Geciken odeme bulunmuyor.", "success")

    # ---- 3) Indirim Raporu ----
    st.markdown("---")
    styled_section("Indirim Raporu", "#7c3aed")

    indirim_rows = []
    toplam_indirim = 0
    for p in planlar:
        indirim = p.get("indirim_tutari", 0)
        if indirim > 0:
            toplam_indirim += indirim
            indirim_rows.append({
                "Ogrenci": p.get("student_adi", "?"),
                "Sinif": f"{p.get('sinif', '?')}/{p.get('sube', '?')}",
                "Toplam Tutar": _format_tutar(p.get("toplam_tutar", 0)),
                "Indirim Orani": f"%{p.get('indirim_orani', 0)}",
                "Indirim Tutari": _format_tutar(indirim),
                "Net Tutar": _format_tutar(p.get("net_tutar", 0)),
            })

    if indirim_rows:
        df_indirim = pd.DataFrame(indirim_rows)
        st.dataframe(df_indirim, use_container_width=True, hide_index=True)

        col_i1, col_i2 = st.columns(2)
        col_i1.metric("Toplam Indirim", _format_tutar(toplam_indirim))
        col_i2.metric("Indirimli Ogrenci", len(indirim_rows))
    else:
        styled_info_banner("Indirim uygulanan plan bulunmuyor.", "info")


# ══════════════════════════════════════════════════════════════
# ANA RENDER FONKSIYONU
# ══════════════════════════════════════════════════════════════

def render_odeme_takip():
    """Odeme Takip modulu ana giris noktasi."""
    # CSS enjekte
    inject_common_css("odeme_takip")
    _inject_odeme_css()

    # Baslik
    styled_header(
        "Odeme Takip Sistemi",
        "Kolej ucret yonetimi, taksit planlari ve tahsilat takibi",
        icon="$",
        accent_color="#6366F1"
    )

    store = _get_store()

    # Tab yapisi
    tabs = st.tabs([
        "Dashboard",
        "Taksit Planlari",
        "Ucret Kalemleri",
        "Yeni Plan Olustur",
        "Odeme Gecmisi",
        "Raporlar",
    ])

    with tabs[0]:
        _render_dashboard(store)

    with tabs[1]:
        _render_taksit_planlari(store)

    with tabs[2]:
        _render_ucret_kalemleri(store)

    with tabs[3]:
        _render_yeni_plan(store)

    with tabs[4]:
        _render_odeme_gecmisi(store)

    with tabs[5]:
        _render_raporlar(store)
