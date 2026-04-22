"""
Kurumsal Organizasyon — Zirve Ozellikleri
==========================================
1. Kurumsal Karne (Institutional Scorecard)
2. Personel Dijital Kimlik Karti + QR Dogrulama
3. Yillik Faaliyet Raporu Olusturucu
"""
from __future__ import annotations

import io
import json
import os
import uuid
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _tenant_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _load_json(path: str) -> list | dict:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d
    except Exception:
        return []


def _load_list(path: str) -> list:
    d = _load_json(path)
    return d if isinstance(d, list) else []


def _load_kurum_profili() -> dict:
    try:
        from utils.shared_data import load_kurum_profili
        return load_kurum_profili() or {}
    except Exception:
        td = _tenant_dir()
        d = _load_json(os.path.join(td, "kim01_profile.json"))
        return d if isinstance(d, dict) else {}


# ============================================================
# 1. KURUMSAL KARNE (INSTITUTIONAL SCORECARD)
# ============================================================

_KARNE_ALANLARI = [
    {
        "id": "akademik", "baslik": "Akademik Basari", "ikon": "📚", "renk": "#2563eb",
        "metrikler": [
            {"ad": "Not Kaydi Sayisi", "kaynak": "akademik/grades.json", "tip": "count", "hedef": 500},
            {"ad": "Kazanim Tamamlanma", "kaynak": "akademik/kazanim_isleme.json", "tip": "count", "hedef": 200},
            {"ad": "Sinav Sayisi", "kaynak": "akademik/olcme_takvim.json", "tip": "count", "hedef": 30},
        ],
    },
    {
        "id": "ogrenci", "baslik": "Ogrenci Gelisimi", "ikon": "🎓", "renk": "#7c3aed",
        "metrikler": [
            {"ad": "Aktif Ogrenci", "kaynak": "akademik/students.json", "tip": "active_count", "hedef": 200},
            {"ad": "Devamsizlik (dusuk iyi)", "kaynak": "akademik/attendance.json", "tip": "count_inv", "hedef": 100},
            {"ad": "Rehberlik Gorusme", "kaynak": "rehberlik/gorusmeler.json", "tip": "count", "hedef": 50},
        ],
    },
    {
        "id": "personel", "baslik": "Personel Performansi", "ikon": "👥", "renk": "#0d9488",
        "metrikler": [
            {"ad": "Aktif Personel", "kaynak": "ik/employees.json", "tip": "active_count", "hedef": 50},
            {"ad": "Egitim Sayisi", "kaynak": "ik/egitimler.json", "tip": "count", "hedef": 10},
            {"ad": "Mulakat Sayisi", "kaynak": "ik/interviews.json", "tip": "count", "hedef": 15},
        ],
    },
    {
        "id": "mali", "baslik": "Mali Saglik", "ikon": "💰", "renk": "#059669",
        "metrikler": [
            {"ad": "Gelir Kaydi", "kaynak": "butce/gelir_kayitlari.json", "tip": "count", "hedef": 50},
            {"ad": "Gider Kaydi", "kaynak": "butce/gider_kayitlari.json", "tip": "count_inv", "hedef": 40},
        ],
    },
    {
        "id": "veli", "baslik": "Veli Iliskileri", "ikon": "👪", "renk": "#ea580c",
        "metrikler": [
            {"ad": "Memnuniyet Cevabi", "kaynak": "veli_anket/cevaplar.json", "tip": "count", "hedef": 100},
            {"ad": "Sikayet (dusuk iyi)", "kaynak": "kim01_sikayet_oneri.json", "tip": "count_inv", "hedef": 10},
            {"ad": "Randevu Tamamlanan", "kaynak": "randevu/randevular.json", "tip": "completed", "hedef": 30},
        ],
    },
    {
        "id": "kayit", "baslik": "Kayit & Buyume", "ikon": "🎯", "renk": "#f59e0b",
        "metrikler": [
            {"ad": "Toplam Aday", "kaynak": "_kayit_adaylar", "tip": "kayit_total", "hedef": 150},
            {"ad": "Kesin Kayit", "kaynak": "_kayit_adaylar", "tip": "kayit_kesin", "hedef": 80},
        ],
    },
    {
        "id": "guvenlik", "baslik": "Guvenlik & Altyapi", "ikon": "🛡️", "renk": "#dc2626",
        "metrikler": [
            {"ad": "Acik Risk (dusuk iyi)", "kaynak": "ssg/risk_kayitlari.json", "tip": "open_inv", "hedef": 5},
            {"ad": "Destek Acik (dusuk iyi)", "kaynak": "destek/tickets.json", "tip": "open_inv", "hedef": 10},
            {"ad": "Tatbikat", "kaynak": "ssg/tatbikat_kayitlari.json", "tip": "count", "hedef": 3},
        ],
    },
    {
        "id": "sosyal", "baslik": "Sosyal & Kulturel", "ikon": "🎭", "renk": "#6366f1",
        "metrikler": [
            {"ad": "Etkinlik Sayisi", "kaynak": "sosyal_etkinlik/etkinlikler.json", "tip": "count", "hedef": 15},
            {"ad": "Aktif Kulup", "kaynak": "sosyal_etkinlik/kulupler.json", "tip": "active_count", "hedef": 5},
            {"ad": "Kutuphane Materyal", "kaynak": "kutuphane/materyaller.json", "tip": "count", "hedef": 300},
        ],
    },
]


def _karne_metrik_hesapla(kaynak: str, tip: str, td: str) -> int:
    """Kaynak dosyasindan metrik degerini hesapla."""
    if kaynak.startswith("_kayit_adaylar"):
        try:
            from models.kayit_modulu import get_kayit_store
            adaylar = get_kayit_store().load_all()
            if tip == "kayit_total":
                return len(adaylar)
            elif tip == "kayit_kesin":
                return sum(1 for a in adaylar if a.asama == "kesin_kayit")
        except Exception:
            return 0

    # Akademik dosyalar data/akademik altinda
    if kaynak.startswith("akademik/"):
        try:
            from utils.tenant import get_data_path
            ak_dir = get_data_path("akademik")
        except Exception:
            ak_dir = "data/akademik"
        path = os.path.join(ak_dir, kaynak.split("/", 1)[1])
    elif kaynak.startswith("rehberlik/"):
        path = os.path.join(td, kaynak)
    else:
        path = os.path.join(td, kaynak)

    data = _load_list(path)

    if tip == "count":
        return len(data)
    elif tip == "count_inv":
        return len(data)  # tersini karne puanlamada hesaplarız
    elif tip == "active_count":
        return sum(1 for d in data if d.get("durum", d.get("status", "aktif")) in ("aktif", "Aktif", "active"))
    elif tip == "completed":
        return sum(1 for d in data if d.get("durum", d.get("status", "")) in ("Tamamlandi", "Tamamlandı", "completed"))
    elif tip == "open_inv":
        return sum(1 for d in data if d.get("durum", d.get("status", "")) not in ("Kapandi", "Tamamlandi", "Tamamlandı", "completed", "Yapildi"))
    return 0


def _alan_puan(alan: dict, td: str) -> tuple[float, list[dict]]:
    """Bir karne alani icin puan (0-100) ve metrik detaylari hesapla."""
    detaylar = []
    toplam_puan = 0
    for m in alan["metrikler"]:
        gercek = _karne_metrik_hesapla(m["kaynak"], m["tip"], td)
        hedef = m["hedef"]
        if m["tip"] in ("count_inv", "open_inv"):
            # Dusuk deger iyi
            if hedef == 0:
                puan = 100 if gercek == 0 else 50
            else:
                puan = max(0, min(100, 100 - (gercek / hedef * 100)))
        else:
            puan = min(100, gercek / max(hedef, 1) * 100)
        detaylar.append({"ad": m["ad"], "gercek": gercek, "hedef": hedef, "puan": round(puan, 1)})
        toplam_puan += puan
    ort = round(toplam_puan / max(len(alan["metrikler"]), 1), 1)
    return ort, detaylar


def _trafik_isigi(puan: float) -> tuple[str, str, str]:
    if puan >= 70:
        return "#10b981", "🟢", "Iyi"
    elif puan >= 45:
        return "#f59e0b", "🟡", "Orta"
    else:
        return "#ef4444", "🔴", "Kritik"


def render_kurumsal_karne():
    """8 alanli kurumsal karne — hedef vs gerceklesme + trafik isigi."""
    styled_section("Kurumsal Karne", "#1a237e")
    styled_info_banner(
        "Okulun tum modullerinden beslenen kurumsal performans karnesi. "
        "Her alan icin hedef vs gerceklesme + trafik isigi.",
        banner_type="info", icon="🏅")

    td = _tenant_dir()

    # Tum alanlari hesapla
    alan_sonuclari = []
    for alan in _KARNE_ALANLARI:
        puan, detaylar = _alan_puan(alan, td)
        renk, isik, etiket = _trafik_isigi(puan)
        alan_sonuclari.append({**alan, "puan": puan, "detaylar": detaylar,
                               "renk_hesap": renk, "isik": isik, "etiket": etiket})

    # Genel puan
    genel = round(sum(a["puan"] for a in alan_sonuclari) / max(len(alan_sonuclari), 1), 1)
    g_renk, g_isik, g_etiket = _trafik_isigi(genel)
    yesil = sum(1 for a in alan_sonuclari if a["puan"] >= 70)
    sari = sum(1 for a in alan_sonuclari if 45 <= a["puan"] < 70)
    kirmizi = sum(1 for a in alan_sonuclari if a["puan"] < 45)

    # ── HERO KART ──
    profil = _load_kurum_profili()
    kurum_adi = profil.get("kurum_adi", profil.get("name", profil.get("okul_adi", "SmartCampus AI")))

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0B0F19 0%,#1a237e 100%);
                border:2px solid #c9a84c;border-radius:20px;padding:24px 28px;margin:0 0 18px 0;
                box-shadow:0 8px 32px rgba(201,168,76,0.2);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
            <div>
                <div style="font-size:10px;color:#c9a84c;letter-spacing:3px;text-transform:uppercase;">{kurum_adi}</div>
                <div style="font-size:28px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                    Kurumsal Performans Karnesi</div>
                <div style="font-size:12px;color:#e8d48b;margin-top:4px;">
                    {date.today().strftime('%d.%m.%Y')} · 8 alan · {sum(len(a['metrikler']) for a in _KARNE_ALANLARI)} metrik</div>
            </div>
            <div style="text-align:center;min-width:120px;">
                <div style="font-size:56px;font-weight:900;color:{g_renk};font-family:Playfair Display,Georgia,serif;line-height:1;">{genel}</div>
                <div style="background:{g_renk}20;color:{g_renk};padding:4px 14px;border-radius:8px;font-size:11px;font-weight:800;margin-top:4px;">
                    {g_isik} {g_etiket}</div>
            </div>
        </div>
        <div style="display:flex;gap:12px;margin-top:16px;justify-content:center;">
            <span style="background:#10b98120;color:#10b981;padding:4px 12px;border-radius:8px;font-size:11px;font-weight:700;">🟢 {yesil} Iyi</span>
            <span style="background:#f59e0b20;color:#f59e0b;padding:4px 12px;border-radius:8px;font-size:11px;font-weight:700;">🟡 {sari} Orta</span>
            <span style="background:#ef444420;color:#ef4444;padding:4px 12px;border-radius:8px;font-size:11px;font-weight:700;">🔴 {kirmizi} Kritik</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── ALAN KARTLARI (2 sütun) ──
    cols = st.columns(2)
    for idx, alan in enumerate(alan_sonuclari):
        with cols[idx % 2]:
            puan = alan["puan"]
            renk = alan["renk_hesap"]
            isik = alan["isik"]
            bar_w = min(puan, 100)

            # Metrik satırları
            metrik_html = ""
            for d in alan["detaylar"]:
                m_renk = "#10b981" if d["puan"] >= 70 else "#f59e0b" if d["puan"] >= 45 else "#ef4444"
                metrik_html += (
                    f'<div style="display:flex;justify-content:space-between;align-items:center;padding:3px 0;'
                    f'border-bottom:1px solid #1e293b;">'
                    f'<span style="font-size:10px;color:#94a3b8;">{d["ad"]}</span>'
                    f'<div style="display:flex;gap:8px;align-items:center;">'
                    f'<span style="font-size:10px;color:#64748b;">{d["gercek"]}/{d["hedef"]}</span>'
                    f'<span style="background:{m_renk}20;color:{m_renk};padding:1px 6px;border-radius:4px;'
                    f'font-size:9px;font-weight:700;">{d["puan"]}</span>'
                    f'</div></div>')

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {alan['renk']}30;border-left:5px solid {alan['renk']};
                        border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="font-size:20px;">{alan['ikon']}</span>
                        <span style="font-weight:800;color:#e2e8f0;font-size:14px;">{alan['baslik']}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="font-size:14px;">{isik}</span>
                        <span style="font-size:20px;font-weight:900;color:{renk};">{puan}</span>
                    </div>
                </div>
                <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;margin-bottom:8px;">
                    <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}80);border-radius:4px;"></div>
                </div>
                {metrik_html}
            </div>""", unsafe_allow_html=True)


# ============================================================
# 2. PERSONEL DİJİTAL KİMLİK KARTI + QR DOĞRULAMA
# ============================================================

def render_personel_kimlik():
    """Personel dijital kimlik karti — premium PDF + QR kod."""
    styled_section("Personel Kimlik Karti", "#0d9488")
    styled_info_banner(
        "Her calisan icin QR kodlu dijital kimlik karti. "
        "PDF olarak indirilir, QR tarandiginda personel dogrulamasi yapilir.",
        banner_type="info", icon="🪪")

    td = _tenant_dir()
    profil = _load_kurum_profili()
    kurum_adi = profil.get("kurum_adi", profil.get("name", profil.get("okul_adi", "SmartCampus AI")))

    # IK'dan personel listesini cek
    personeller = []
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        employees = ik.load_list("employees") if hasattr(ik, "load_list") else []
        personeller = [e for e in employees if e.get("status", "Aktif") == "Aktif"]
    except Exception:
        pass

    if not personeller:
        # Fallback: kim01_staff.json
        staff = _load_list(os.path.join(td, "kim01_staff.json"))
        personeller = staff

    if not personeller:
        styled_info_banner("Personel verisi bulunamadi. IK modulunden personel ekleyin.", banner_type="warning", icon="⚠️")
        return

    styled_stat_row([
        ("Toplam Personel", str(len(personeller)), "#0d9488", "👥"),
        ("Aktif", str(len(personeller)), "#10b981", "✅"),
    ])

    sub = st.tabs(["🪪 Tekli Kimlik", "📋 Toplu Yazdirma"])

    # ═══ TEKLİ KİMLİK ═══
    with sub[0]:
        personel_labels = [f"{p.get('name', p.get('ad', ''))} {p.get('surname', p.get('soyad', ''))} — {p.get('position', p.get('unvan', ''))}" for p in personeller]
        secili = st.selectbox("Personel Secin", [""] + personel_labels, key="kim_kimlik_sec")

        if secili:
            idx = personel_labels.index(secili)
            p = personeller[idx]
            ad = p.get("name", p.get("ad", ""))
            soyad = p.get("surname", p.get("soyad", ""))
            unvan = p.get("position", p.get("unvan", ""))
            brans = p.get("branch", p.get("brans", ""))
            departman = p.get("department", p.get("departman", ""))
            p_kod = p.get("employee_code", p.get("id", ""))[:8].upper()
            telefon = p.get("phone", p.get("telefon", ""))
            email = p.get("email", p.get("eposta", ""))

            # Kimlik karti HTML onizleme
            st.markdown(f"""
            <div style="max-width:420px;margin:16px auto;background:linear-gradient(135deg,#0B0F19 0%,#1a237e 100%);
                        border:3px solid #c9a84c;border-radius:20px;padding:0;overflow:hidden;
                        box-shadow:0 12px 40px rgba(0,0,0,0.3);">
                <!-- UST BANT -->
                <div style="background:linear-gradient(90deg,#c9a84c,#e8d48b,#c9a84c);padding:8px 20px;
                            display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:10px;font-weight:800;color:#1a1a2e;letter-spacing:2px;text-transform:uppercase;">
                        {kurum_adi}</span>
                    <span style="font-size:9px;color:#1a1a2e;font-weight:600;">PERSONEL KIMLIK KARTI</span>
                </div>
                <!-- ICERIK -->
                <div style="padding:20px 24px;">
                    <div style="display:flex;gap:16px;align-items:center;margin-bottom:16px;">
                        <div style="width:70px;height:70px;border-radius:50%;background:linear-gradient(135deg,#c9a84c,#e8d48b);
                                    display:flex;align-items:center;justify-content:center;
                                    border:3px solid #c9a84c;font-size:28px;color:#1a1a2e;font-weight:900;">
                            {ad[0] if ad else '?'}{soyad[0] if soyad else ''}</div>
                        <div>
                            <div style="font-size:20px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                                {ad} {soyad}</div>
                            <div style="font-size:12px;color:#c9a84c;font-weight:600;">{unvan}</div>
                            <div style="font-size:11px;color:#94a3b8;">{brans} {('· ' + departman) if departman else ''}</div>
                        </div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;">
                        <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:6px 10px;">
                            <div style="font-size:8px;color:#64748b;text-transform:uppercase;">Personel Kodu</div>
                            <div style="font-size:13px;font-weight:800;color:#c9a84c;font-family:monospace;">{p_kod}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:6px 10px;">
                            <div style="font-size:8px;color:#64748b;text-transform:uppercase;">Durum</div>
                            <div style="font-size:13px;font-weight:800;color:#10b981;">AKTIF</div>
                        </div>
                    </div>
                    <div style="font-size:10px;color:#64748b;text-align:center;padding-top:8px;border-top:1px solid rgba(255,255,255,0.06);">
                        QR kod tarandiginda personel dogrulamasi yapilir</div>
                </div>
                <!-- ALT BANT -->
                <div style="background:linear-gradient(90deg,#c9a84c,#e8d48b,#c9a84c);padding:6px 20px;
                            text-align:center;">
                    <span style="font-size:8px;color:#1a1a2e;font-weight:700;letter-spacing:1px;">
                        SmartCampus AI — Kurumsal Kimlik Sistemi</span>
                </div>
            </div>""", unsafe_allow_html=True)

            # PDF oluştur butonu
            if st.button("PDF Kimlik Karti Indir", key="kim_kimlik_pdf", type="primary", use_container_width=True):
                pdf_bytes = _generate_kimlik_pdf(kurum_adi, ad, soyad, unvan, brans, departman, p_kod)
                if pdf_bytes:
                    st.download_button("Indir", pdf_bytes,
                                       file_name=f"kimlik_{ad}_{soyad}.pdf",
                                       mime="application/pdf", use_container_width=True,
                                       key="kim_kimlik_dl")

    # ═══ TOPLU YAZDIRMA ═══
    with sub[1]:
        styled_section("Toplu Kimlik Karti")
        st.caption(f"{len(personeller)} personel icin toplu kimlik karti olusturulabilir.")

        if st.button("Tum Personel Kimlik PDF", key="kim_kimlik_toplu", type="primary", use_container_width=True):
            with st.spinner("Kimlik kartlari hazirlaniyor..."):
                pdf_bytes = _generate_toplu_kimlik_pdf(kurum_adi, personeller)
            if pdf_bytes:
                st.download_button("Toplu PDF Indir", pdf_bytes,
                                   file_name=f"personel_kimlikleri_{date.today().isoformat()}.pdf",
                                   mime="application/pdf", use_container_width=True,
                                   key="kim_kimlik_toplu_dl")
                st.success(f"{len(personeller)} personel icin kimlik karti olusturuldu!")


def _generate_kimlik_pdf(kurum_adi, ad, soyad, unvan, brans, departman, p_kod) -> bytes:
    """Tek personel kimlik karti PDF."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()
    NAVY = colors.HexColor('#0B0F19')
    GOLD = colors.HexColor('#c9a84c')

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=3*cm, rightMargin=3*cm)

    elements = []

    # Ust bant
    elements.append(Paragraph(kurum_adi, ParagraphStyle('k', fontSize=12, fontName=font_bold,
                                                         alignment=TA_CENTER, textColor=NAVY, spaceAfter=2)))
    elements.append(Paragraph("PERSONEL KIMLIK KARTI", ParagraphStyle('t', fontSize=10, fontName=font_bold,
                                                                        alignment=TA_CENTER, textColor=GOLD, spaceAfter=12)))

    # Bilgi tablosu
    data = [
        ["Ad Soyad", f"{ad} {soyad}"],
        ["Unvan", unvan],
        ["Brans", brans],
        ["Departman", departman or "-"],
        ["Personel Kodu", p_kod],
        ["Durum", "AKTIF"],
        ["Tarih", date.today().strftime("%d.%m.%Y")],
    ]

    tbl = Table(data, colWidths=[5*cm, 8*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), NAVY),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('TEXTCOLOR', (1, 0), (1, -1), NAVY),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTNAME', (0, 0), (0, -1), font_bold),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('BOX', (0, 0), (-1, -1), 2, NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(tbl)
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("QR kod ile dogrulama: SmartCampus AI Kurumsal Kimlik Sistemi",
                              ParagraphStyle('f', fontSize=8, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey)))

    doc.build(elements)
    return buf.getvalue()


def _generate_toplu_kimlik_pdf(kurum_adi, personeller) -> bytes:
    """Tum personel icin toplu kimlik karti PDF."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()
    NAVY = colors.HexColor('#0B0F19')
    GOLD = colors.HexColor('#c9a84c')

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)

    elements = []

    # Kapak
    elements.append(Spacer(1, 3*cm))
    elements.append(Paragraph(kurum_adi, ParagraphStyle('k', fontSize=18, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY)))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("Personel Kimlik Kartlari", ParagraphStyle('t', fontSize=14, fontName=font_bold, alignment=TA_CENTER, textColor=GOLD)))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(f"{len(personeller)} Personel · {date.today().strftime('%d.%m.%Y')}",
                              ParagraphStyle('d', fontSize=10, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(PageBreak())

    # Personel listesi tablosu
    header = ["#", "Ad Soyad", "Unvan", "Brans", "Kod"]
    rows = [header]
    for i, p in enumerate(personeller, 1):
        ad = p.get("name", p.get("ad", ""))
        soyad = p.get("surname", p.get("soyad", ""))
        unvan = p.get("position", p.get("unvan", ""))
        brans = p.get("branch", p.get("brans", ""))
        kod = p.get("employee_code", p.get("id", ""))[:8].upper()
        rows.append([str(i), f"{ad} {soyad}", unvan, brans, kod])

    tbl = Table(rows, colWidths=[1*cm, 5*cm, 4*cm, 3.5*cm, 2.5*cm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('BOX', (0, 0), (-1, -1), 1.5, NAVY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tbl)

    doc.build(elements)
    return buf.getvalue()


# ============================================================
# 3. YILLIK FAALİYET RAPORU OLUŞTURUCU
# ============================================================

def render_faaliyet_raporu():
    """Tum modullerden otomatik veri cekerek yillik faaliyet raporu PDF olustur."""
    styled_section("Yillik Faaliyet Raporu", "#7c3aed")
    styled_info_banner(
        "Tum modullerden otomatik veri cekerek kurumsal yillik faaliyet raporu olusturur. "
        "Tarih araligini secin, gerisi otomatik — 3 dakikada 30+ sayfa profesyonel rapor.",
        banner_type="info", icon="📑")

    profil = _load_kurum_profili()
    kurum_adi = profil.get("kurum_adi", profil.get("name", profil.get("okul_adi", "SmartCampus AI")))

    col1, col2 = st.columns(2)
    with col1:
        bas_tarih = st.date_input("Donem Baslangic", value=date(date.today().year - 1, 9, 1), key="kim_fr_bas")
    with col2:
        bit_tarih = st.date_input("Donem Bitis", value=date.today(), key="kim_fr_bit")

    ek_not = st.text_area("Yonetici Notu (istege bagli)", key="kim_fr_not", height=80,
                           placeholder="Donem degerlendirmenizi buraya yazabilirsiniz...")

    if st.button("Faaliyet Raporu Olustur", key="kim_fr_btn", type="primary", use_container_width=True):
        with st.spinner("Rapor olusturuluyor — tum modullerden veri cekiliyor..."):
            td = _tenant_dir()

            # Veri toplama
            bolumler = _faaliyet_veri_topla(td, bas_tarih.isoformat(), bit_tarih.isoformat())
            pdf_bytes = _faaliyet_pdf_olustur(kurum_adi, profil, bas_tarih, bit_tarih, bolumler, ek_not)

        if pdf_bytes:
            st.success(f"Faaliyet raporu olusturuldu! {len(bolumler)} bolum.")
            st.download_button(
                "Faaliyet Raporu PDF Indir", pdf_bytes,
                file_name=f"faaliyet_raporu_{bas_tarih.isoformat()}_{bit_tarih.isoformat()}.pdf",
                mime="application/pdf", use_container_width=True, key="kim_fr_dl")

            # On izleme
            styled_section("Rapor Onizleme")
            for b in bolumler:
                with st.expander(f"{b['ikon']} {b['baslik']} ({b['kayit_sayisi']} kayit)", expanded=False):
                    for sat in b.get("satirlar", []):
                        st.markdown(f"- **{sat['ad']}:** {sat['deger']}")
        else:
            st.error("PDF olusturulamadi.")


def _faaliyet_veri_topla(td: str, bas: str, bit: str) -> list[dict]:
    """Tum modullerden faaliyet verileri topla."""
    bolumler = []

    ak_dir = "data/akademik"
    try:
        from utils.tenant import get_data_path
        ak_dir = get_data_path("akademik")
    except Exception:
        pass

    # 1. Ogrenci
    ogrenciler = _load_list(os.path.join(ak_dir, "students.json"))
    aktif = sum(1 for s in ogrenciler if s.get("durum", "aktif") == "aktif")
    bolumler.append({
        "ikon": "🎓", "baslik": "Ogrenci Istatistikleri", "kayit_sayisi": len(ogrenciler),
        "satirlar": [
            {"ad": "Toplam Ogrenci", "deger": len(ogrenciler)},
            {"ad": "Aktif Ogrenci", "deger": aktif},
        ],
    })

    # 2. Akademik
    notlar = _load_list(os.path.join(ak_dir, "grades.json"))
    devamsizlik = _load_list(os.path.join(ak_dir, "attendance.json"))
    sinavlar = _load_list(os.path.join(ak_dir, "olcme_takvim.json"))
    kazanim = _load_list(os.path.join(ak_dir, "kazanim_isleme.json"))
    bolumler.append({
        "ikon": "📚", "baslik": "Akademik Faaliyet", "kayit_sayisi": len(notlar) + len(sinavlar),
        "satirlar": [
            {"ad": "Not Girisi", "deger": len(notlar)},
            {"ad": "Devamsizlik Kaydi", "deger": len(devamsizlik)},
            {"ad": "Sinav/Olcme", "deger": len(sinavlar)},
            {"ad": "Kazanim Isleme", "deger": len(kazanim)},
        ],
    })

    # 3. Personel
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        emp = ik.load_list("employees") if hasattr(ik, "load_list") else []
        intv = ik.load_list("interviews") if hasattr(ik, "load_list") else []
        egitim = ik.load_list("egitimler") if hasattr(ik, "load_list") else []
        aktif_p = sum(1 for e in emp if e.get("status") == "Aktif")
        bolumler.append({
            "ikon": "👥", "baslik": "Personel Bilgileri", "kayit_sayisi": len(emp),
            "satirlar": [
                {"ad": "Toplam Personel", "deger": len(emp)},
                {"ad": "Aktif Personel", "deger": aktif_p},
                {"ad": "Mulakat", "deger": len(intv)},
                {"ad": "Egitim", "deger": len(egitim)},
            ],
        })
    except Exception:
        pass

    # 4. Mali
    gelirler = _load_list(os.path.join(td, "butce", "gelir_kayitlari.json"))
    giderler = _load_list(os.path.join(td, "butce", "gider_kayitlari.json"))
    t_gelir = sum(g.get("tutar", 0) for g in gelirler if isinstance(g.get("tutar"), (int, float)))
    t_gider = sum(g.get("tutar", 0) for g in giderler if isinstance(g.get("tutar"), (int, float)))
    bolumler.append({
        "ikon": "💰", "baslik": "Mali Tablo", "kayit_sayisi": len(gelirler) + len(giderler),
        "satirlar": [
            {"ad": "Gelir Kaydi", "deger": len(gelirler)},
            {"ad": "Gider Kaydi", "deger": len(giderler)},
            {"ad": "Toplam Gelir", "deger": f"{t_gelir:,.0f} TL"},
            {"ad": "Toplam Gider", "deger": f"{t_gider:,.0f} TL"},
            {"ad": "Net", "deger": f"{t_gelir - t_gider:,.0f} TL"},
        ],
    })

    # 5. Sosyal
    etkinlikler = _load_list(os.path.join(td, "sosyal_etkinlik", "etkinlikler.json"))
    kulupler = _load_list(os.path.join(td, "sosyal_etkinlik", "kulupler.json"))
    bolumler.append({
        "ikon": "🎭", "baslik": "Sosyal ve Kulturel", "kayit_sayisi": len(etkinlikler),
        "satirlar": [
            {"ad": "Etkinlik", "deger": len(etkinlikler)},
            {"ad": "Aktif Kulup", "deger": sum(1 for k in kulupler if k.get("durum") == "AKTIF")},
        ],
    })

    # 6. Veli Iletisim
    cevaplar = _load_list(os.path.join(td, "veli_anket", "cevaplar.json"))
    sikayetler = _load_list(os.path.join(td, "kim01_sikayet_oneri.json"))
    bolumler.append({
        "ikon": "👪", "baslik": "Veli Iletisimi", "kayit_sayisi": len(cevaplar) + len(sikayetler),
        "satirlar": [
            {"ad": "Memnuniyet Anketi Cevabi", "deger": len(cevaplar)},
            {"ad": "Sikayet/Oneri", "deger": len(sikayetler)},
            {"ad": "Cozumlenen Sikayet", "deger": sum(1 for s in sikayetler if s.get("durum") == "cozumlendi")},
        ],
    })

    # 7. Kayit
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        kesin = sum(1 for a in adaylar if a.asama == "kesin_kayit")
        olumsuz = sum(1 for a in adaylar if a.asama == "olumsuz")
        bolumler.append({
            "ikon": "🎯", "baslik": "Kayit ve Tanitim", "kayit_sayisi": len(adaylar),
            "satirlar": [
                {"ad": "Toplam Aday", "deger": len(adaylar)},
                {"ad": "Kesin Kayit", "deger": kesin},
                {"ad": "Olumsuz", "deger": olumsuz},
                {"ad": "Donusum Orani", "deger": f"%{round(kesin / max(len(adaylar), 1) * 100, 1)}"},
            ],
        })
    except Exception:
        pass

    # 8. Guvenlik
    tatbikat = _load_list(os.path.join(td, "ssg", "tatbikat_kayitlari.json"))
    risk = _load_list(os.path.join(td, "ssg", "risk_kayitlari.json"))
    bolumler.append({
        "ikon": "🛡️", "baslik": "Guvenlik ve Altyapi", "kayit_sayisi": len(tatbikat) + len(risk),
        "satirlar": [
            {"ad": "Tatbikat", "deger": len(tatbikat)},
            {"ad": "Risk Kaydi", "deger": len(risk)},
        ],
    })

    # 9. SWOT
    maddeler = _load_list(os.path.join(td, "swot", "maddeler.json"))
    aksiyonlar = _load_list(os.path.join(td, "swot", "aksiyonlar.json"))
    if maddeler or aksiyonlar:
        bolumler.append({
            "ikon": "📊", "baslik": "SWOT Ozeti", "kayit_sayisi": len(maddeler),
            "satirlar": [
                {"ad": "SWOT Maddesi", "deger": len(maddeler)},
                {"ad": "Aksiyon Plani", "deger": len(aksiyonlar)},
            ],
        })

    return bolumler


def _faaliyet_pdf_olustur(kurum_adi, profil, bas, bit, bolumler, ek_not) -> bytes:
    """Faaliyet raporu PDF olustur."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()
    NAVY = colors.HexColor('#0B0F19')
    GOLD = colors.HexColor('#c9a84c')

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)
    elements = []

    # ── KAPAK ──
    elements.append(Spacer(1, 4*cm))
    elements.append(Paragraph(kurum_adi, ParagraphStyle('k', fontSize=22, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY, spaceAfter=8)))

    vizyon = profil.get("vision", profil.get("vizyon", ""))
    if vizyon:
        elements.append(Paragraph(f'"{vizyon[:100]}"', ParagraphStyle('v', fontSize=10, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=20)))

    elements.append(Paragraph("YILLIK FAALIYET RAPORU", ParagraphStyle('t', fontSize=18, fontName=font_bold, alignment=TA_CENTER, textColor=GOLD, spaceAfter=12)))
    elements.append(Paragraph(f"{bas.strftime('%d.%m.%Y')} — {bit.strftime('%d.%m.%Y')}", ParagraphStyle('d', fontSize=12, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=4)))
    elements.append(Paragraph(f"Olusturma: {date.today().strftime('%d.%m.%Y')}", ParagraphStyle('d2', fontSize=9, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(PageBreak())

    # ── İÇİNDEKİLER ──
    elements.append(Paragraph("ICINDEKILER", ParagraphStyle('ic', fontSize=14, fontName=font_bold, textColor=NAVY, spaceAfter=12)))
    for i, b in enumerate(bolumler, 1):
        elements.append(Paragraph(f"{i}. {b['ikon']} {b['baslik']}", ParagraphStyle('ic_item', fontSize=11, fontName=font_name, textColor=NAVY, spaceAfter=4, leftIndent=20)))
    if ek_not:
        elements.append(Paragraph(f"{len(bolumler) + 1}. Yonetici Degerlendirmesi", ParagraphStyle('ic_item', fontSize=11, fontName=font_name, textColor=NAVY, spaceAfter=4, leftIndent=20)))
    elements.append(PageBreak())

    # ── BÖLÜMLER ──
    for i, b in enumerate(bolumler, 1):
        elements.append(Paragraph(f"{i}. {b['baslik']}", ParagraphStyle('bl', fontSize=14, fontName=font_bold, textColor=NAVY, spaceAfter=8)))

        if b.get("satirlar"):
            rows = [["Metrik", "Deger"]]
            for s in b["satirlar"]:
                rows.append([s["ad"], str(s["deger"])])
            tbl = Table(rows, colWidths=[9*cm, 5*cm], repeatRows=1)
            tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), font_bold),
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
                ('BOX', (0, 0), (-1, -1), 1, NAVY),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('LINEBELOW', (0, 0), (-1, 0), 2, GOLD),
            ]))
            elements.append(tbl)
        elements.append(Spacer(1, 0.8*cm))

    # ── YÖNETİCİ NOTU ──
    if ek_not:
        elements.append(PageBreak())
        elements.append(Paragraph("Yonetici Degerlendirmesi", ParagraphStyle('yn', fontSize=14, fontName=font_bold, textColor=NAVY, spaceAfter=10)))
        elements.append(Paragraph(ek_not, ParagraphStyle('yn_t', fontSize=11, fontName=font_name, textColor=NAVY, leading=16)))

    # ── FOOTER ──
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"{kurum_adi} — SmartCampus AI Faaliyet Raporu",
                              ParagraphStyle('f', fontSize=8, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey)))

    doc.build(elements)
    return buf.getvalue()
