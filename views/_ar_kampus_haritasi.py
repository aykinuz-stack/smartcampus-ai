"""
AR Kampüs Haritası — Interaktif Kampüs Rehberi
=====================================================
Ziyaretçiler ve yeni veliler için kampüs haritası.
QR kod tarayınca AR overlay — "9-A bu yönde 20m", "Revir 2. kat" vb.
Şimdilik interaktif SVG harita ve QR bazlı konum sistemi.
"""
from __future__ import annotations

import json
import os
import base64
from datetime import datetime
from io import BytesIO

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# KAMPUS LOKASYONLARI — Varsayılan
# ══════════════════════════════════════════════════════════════

DEFAULT_LOKASYONLAR = [
    {"id": "LOC-001", "ad": "Müdür Odası", "kat": 1, "bina": "Ana Bina",
     "ikon": "🏛️", "renk": "#4F46E5", "aciklama": "Müdür ve müdür yardımcıları",
     "yon": "ileri", "mesafe_m": 10},
    {"id": "LOC-002", "ad": "Rehberlik Servisi", "kat": 1, "bina": "Ana Bina",
     "ikon": "🧠", "renk": "#7C3AED", "aciklama": "PDR ve rehber öğretmenler",
     "yon": "sag", "mesafe_m": 15},
    {"id": "LOC-003", "ad": "Revir", "kat": 1, "bina": "Ana Bina",
     "ikon": "🏥", "renk": "#059669", "aciklama": "Sağlık hizmetleri",
     "yon": "sag", "mesafe_m": 20},
    {"id": "LOC-004", "ad": "Yemekhane", "kat": 0, "bina": "Ana Bina",
     "ikon": "🍽️", "renk": "#D97706", "aciklama": "Öğle yemeği 12:00-13:00",
     "yon": "asagi", "mesafe_m": 25},
    {"id": "LOC-005", "ad": "Kütüphane", "kat": 2, "bina": "Ana Bina",
     "ikon": "📚", "renk": "#7C3AED", "aciklama": "Okuma salonu ve ödünç",
     "yon": "yukari", "mesafe_m": 30},
    {"id": "LOC-006", "ad": "Spor Salonu", "kat": 0, "bina": "B Bina",
     "ikon": "⚽", "renk": "#DC2626", "aciklama": "Beden eğitimi ve kulüpler",
     "yon": "ileri_saga", "mesafe_m": 80},
    {"id": "LOC-007", "ad": "Fen Laboratuvarı", "kat": 2, "bina": "Ana Bina",
     "ikon": "🔬", "renk": "#0D9488", "aciklama": "Fizik, kimya, biyoloji",
     "yon": "yukari", "mesafe_m": 35},
    {"id": "LOC-008", "ad": "Bilgisayar Lab", "kat": 3, "bina": "Ana Bina",
     "ikon": "💻", "renk": "#0284C7", "aciklama": "BİLİŞİM ve kodlama dersleri",
     "yon": "yukari", "mesafe_m": 45},
    {"id": "LOC-009", "ad": "Konferans Salonu", "kat": 1, "bina": "Ana Bina",
     "ikon": "🎤", "renk": "#EC4899", "aciklama": "Büyük toplantılar ve sunumlar",
     "yon": "sol", "mesafe_m": 40},
    {"id": "LOC-010", "ad": "Öğretmen Odası", "kat": 1, "bina": "Ana Bina",
     "ikon": "👨‍🏫", "renk": "#64748B", "aciklama": "Öğretmen dinlenme ve çalışma",
     "yon": "sol_geri", "mesafe_m": 25},
    {"id": "LOC-011", "ad": "Sınıf 9-A", "kat": 2, "bina": "Ana Bina",
     "ikon": "📖", "renk": "#4F46E5", "aciklama": "9. sınıf A şubesi",
     "yon": "yukari_sag", "mesafe_m": 40},
    {"id": "LOC-012", "ad": "Sınıf 10-B", "kat": 2, "bina": "Ana Bina",
     "ikon": "📖", "renk": "#4F46E5", "aciklama": "10. sınıf B şubesi",
     "yon": "yukari_sag", "mesafe_m": 42},
    {"id": "LOC-013", "ad": "Tuvalet (Kadın)", "kat": 1, "bina": "Ana Bina",
     "ikon": "🚻", "renk": "#EC4899", "aciklama": "Her katta mevcut",
     "yon": "sol", "mesafe_m": 5},
    {"id": "LOC-014", "ad": "Tuvalet (Erkek)", "kat": 1, "bina": "Ana Bina",
     "ikon": "🚻", "renk": "#0284C7", "aciklama": "Her katta mevcut",
     "yon": "sag", "mesafe_m": 5},
    {"id": "LOC-015", "ad": "Çıkış (Ana Kapı)", "kat": 0, "bina": "Ana Bina",
     "ikon": "🚪", "renk": "#059669", "aciklama": "Ana giriş/çıkış kapısı",
     "yon": "geri", "mesafe_m": 50},
]


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _ar_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "ar_kampus")
    except Exception:
        d = os.path.join("data", "ar_kampus")
    os.makedirs(d, exist_ok=True)
    return d


def _ar_path() -> str:
    return os.path.join(_ar_dir(), "lokasyonlar.json")


def _load_lokasyonlar() -> list[dict]:
    p = _ar_path()
    if not os.path.exists(p):
        _save_lokasyonlar(DEFAULT_LOKASYONLAR.copy())
        return DEFAULT_LOKASYONLAR.copy()
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_LOKASYONLAR.copy()


def _save_lokasyonlar(data: list[dict]) -> None:
    with open(_ar_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# INTERAKTİF HARİTA
# ══════════════════════════════════════════════════════════════

def render_kampus_harita(lokasyonlar: list[dict]):
    """Kat bazlı interaktif kampüs haritası."""
    # Kat seçici
    katlar = sorted(set(loc.get("kat", 0) for loc in lokasyonlar))
    binalar = sorted(set(loc.get("bina", "Ana Bina") for loc in lokasyonlar))

    hc1, hc2 = st.columns(2)
    with hc1:
        sel_bina = st.selectbox("Bina", binalar, key="_ar_bina_widget")
    with hc2:
        sel_kat = st.selectbox(
            "Kat",
            katlar,
            format_func=lambda k: f"{k}. Kat" if k > 0 else "Zemin Kat",
            key="_ar_kat_widget",
        )

    # Filtrele
    filtered = [loc for loc in lokasyonlar
                if loc.get("bina") == sel_bina and loc.get("kat") == sel_kat]

    if not filtered:
        styled_info_banner(f"{sel_bina} — {sel_kat}. katta kayıtlı lokasyon yok.", "info")
        return

    # Görsel kat planı — SVG
    svg_items = []
    import math
    radius = 160
    center_x, center_y = 250, 180
    n = len(filtered)

    for i, loc in enumerate(filtered):
        angle = 2 * math.pi * i / max(n, 1) - math.pi / 2
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        ikon = loc.get("ikon", "📍")
        renk = loc.get("renk", "#4F46E5")
        ad = loc.get("ad", "")

        svg_items.append(f"""
        <g>
            <circle cx="{x:.0f}" cy="{y:.0f}" r="24" fill="{renk}" stroke="#FAFAFA" stroke-width="2" opacity="0.9"/>
            <text x="{x:.0f}" y="{y+6:.0f}" text-anchor="middle" font-size="20">{ikon}</text>
            <text x="{x:.0f}" y="{y+42:.0f}" text-anchor="middle" font-size="10" fill="#FAFAFA" font-weight="700">{ad[:12]}</text>
        </g>
        """)

    # Merkez (kullanıcı konumu)
    svg_items.append(f"""
    <g>
        <circle cx="{center_x}" cy="{center_y}" r="18" fill="#DC2626" stroke="#FAFAFA" stroke-width="3"/>
        <circle cx="{center_x}" cy="{center_y}" r="30" fill="none" stroke="#DC2626" stroke-width="2" opacity="0.5">
            <animate attributeName="r" from="18" to="60" dur="2s" repeatCount="indefinite"/>
            <animate attributeName="opacity" from="0.5" to="0" dur="2s" repeatCount="indefinite"/>
        </circle>
        <text x="{center_x}" y="{center_y+6}" text-anchor="middle" font-size="18">📍</text>
        <text x="{center_x}" y="{center_y+50}" text-anchor="middle" font-size="11" fill="#FAFAFA" font-weight="800">Konumun</text>
    </g>
    """)

    # Başlık
    svg_items.append(f"""
    <text x="{center_x}" y="30" text-anchor="middle" font-size="16" fill="#FAFAFA" font-weight="800">
        {sel_bina} — {sel_kat}. Kat
    </text>
    """)

    svg_content = "\n".join(svg_items)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#18181B,#27272A);border-radius:16px;padding:16px;
    margin:16px 0;border:1px solid rgba(255,255,255,0.1);">
        <svg viewBox="0 0 500 400" style="width:100%;max-width:500px;margin:0 auto;display:block;" xmlns="http://www.w3.org/2000/svg">
            {svg_content}
        </svg>
    </div>
    """, unsafe_allow_html=True)

    # Lokasyon listesi
    st.markdown("### 📋 Bu Kattaki Konumlar")
    for loc in filtered:
        yon_text = {
            "ileri": "↑ İleri",
            "geri": "↓ Geri",
            "sag": "→ Sağda",
            "sol": "← Solda",
            "yukari": "↑ Üst kat",
            "asagi": "↓ Alt kat",
            "ileri_saga": "↗ İleri-Sağ",
            "yukari_sag": "↗ Yukarı-Sağ",
            "sol_geri": "↙ Sol-Geri",
        }.get(loc.get("yon", ""), "📍")

        st.markdown(f"""
        <div style="background:#18181B;border-left:4px solid {loc.get('renk', '#4F46E5')};
        border-radius:8px;padding:10px 16px;margin:6px 0;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-size:1.4rem;">{loc.get('ikon', '📍')}</span>
                <strong style="color:#FAFAFA;margin-left:8px;">{loc.get('ad', '')}</strong>
                <div style="color:#94A3B8;font-size:0.82rem;margin-top:2px;">{loc.get('aciklama', '')}</div>
            </div>
            <div style="text-align:right;">
                <div style="color:{loc.get('renk', '#4F46E5')};font-weight:700;font-size:0.9rem;">{yon_text}</div>
                <div style="color:#64748B;font-size:0.78rem;">≈ {loc.get('mesafe_m', 0)}m</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# QR KOD ÜRETİMİ — Her lokasyon için
# ══════════════════════════════════════════════════════════════

def render_qr_kodlari(lokasyonlar: list[dict]):
    """Her lokasyon için printable QR kodları üret."""
    st.markdown("### 📱 Lokasyon QR Kodları")
    styled_info_banner(
        "Her QR'ı yazdırıp ilgili lokasyona yapıştırın. Telefonla tarayan kişi AR ipuçlarını görür.",
        "info", "🖨️",
    )

    # Filter
    cat_filter = st.selectbox(
        "Filtre",
        ["Tümü"] + sorted(set(loc.get("bina", "Ana Bina") for loc in lokasyonlar)),
        key="_ar_qr_filter_widget",
    )
    filtered = lokasyonlar if cat_filter == "Tümü" else [loc for loc in lokasyonlar if loc.get("bina") == cat_filter]

    # Grid — 3 sütunlu
    cols_per_row = 3
    for row_start in range(0, len(filtered), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, loc in zip(cols, filtered[row_start:row_start + cols_per_row]):
            with col:
                # QR üret
                qr_data = json.dumps({
                    "type": "scai_loc",
                    "id": loc.get("id"),
                    "ad": loc.get("ad"),
                    "bina": loc.get("bina"),
                    "kat": loc.get("kat"),
                }, ensure_ascii=False)

                try:
                    import qrcode
                    qr = qrcode.QRCode(version=1, box_size=6, border=1)
                    qr.add_data(qr_data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="#09090B", back_color="#FAFAFA")
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    b64 = base64.b64encode(buf.getvalue()).decode()
                    qr_html = f'<img src="data:image/png;base64,{b64}" style="width:140px;height:140px;border-radius:8px;" />'
                except ImportError:
                    qr_html = f'<div style="width:140px;height:140px;background:#FAFAFA;color:#09090B;border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:monospace;font-size:10px;padding:10px;text-align:center;">QR: {loc.get("id")}</div>'

                st.markdown(f"""
                <div style="background:#18181B;border:1px solid rgba(255,255,255,0.1);
                border-radius:12px;padding:12px;text-align:center;margin:6px 0;">
                    {qr_html}
                    <div style="margin-top:8px;font-weight:700;color:{loc.get('renk', '#4F46E5')};font-size:0.92rem;">
                        {loc.get('ikon', '📍')} {loc.get('ad', '')}
                    </div>
                    <div style="color:#94A3B8;font-size:0.72rem;">
                        {loc.get('bina', '')} · Kat {loc.get('kat', 0)}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# AR SIMÜLASYON — QR tarayınca ne görür?
# ══════════════════════════════════════════════════════════════

def render_ar_simulator(lokasyonlar: list[dict]):
    """Ziyaretçi QR taradığında görecekleri simülasyonu."""
    st.markdown("### 🔍 AR Önizleme (Ziyaretçi Görünümü)")
    styled_info_banner(
        "Ziyaretçi QR kodu tarayınca böyle görecek. Gerçek AR deneyimi için mobil uygulama gereklidir.",
        "info", "🔍",
    )

    loc_names = [f"{loc.get('ikon', '📍')} {loc.get('ad', '')}" for loc in lokasyonlar]
    sel_idx = st.selectbox(
        "Lokasyon",
        range(len(lokasyonlar)),
        format_func=lambda i: loc_names[i],
        key="_ar_sim_widget",
    )
    sel_loc = lokasyonlar[sel_idx]

    # AR mockup
    renk = sel_loc.get("renk", "#4F46E5")

    # Hedef seçimi (yön göstermek için)
    hedef_names = [f"{loc.get('ikon', '📍')} {loc.get('ad', '')}" for loc in lokasyonlar if loc.get("id") != sel_loc.get("id")]
    hedef_idx = st.selectbox("Nereye gitmek istiyorsun?", range(len(hedef_names)),
                              format_func=lambda i: hedef_names[i], key="_ar_hedef_widget")
    hedef_loc = [loc for loc in lokasyonlar if loc.get("id") != sel_loc.get("id")][hedef_idx]

    # Yön hesaplama (basit — aynı kat/bina ise)
    ayni_kat = sel_loc.get("kat") == hedef_loc.get("kat")
    ayni_bina = sel_loc.get("bina") == hedef_loc.get("bina")

    if not ayni_bina:
        yon_mesaj = f"🏢 **{hedef_loc.get('bina')}** binasına geçmeniz gerekiyor"
        mesafe = 100
    elif not ayni_kat:
        kat_fark = hedef_loc.get("kat", 0) - sel_loc.get("kat", 0)
        yon_mesaj = f"{'⬆️ ' + str(kat_fark) + ' kat yukarı' if kat_fark > 0 else '⬇️ ' + str(-kat_fark) + ' kat aşağı'} — **{hedef_loc.get('ad')}**"
        mesafe = abs(kat_fark) * 30
    else:
        yon_mesaj = f"↗️ Aynı katta — **{hedef_loc.get('ad')}**"
        mesafe = hedef_loc.get("mesafe_m", 20)

    # AR overlay simülasyonu
    st.markdown(f"""
    <div style="background:linear-gradient(180deg,#0B0F19 0%,#18181B 50%,#0B0F19 100%);
    border:2px solid {renk};border-radius:24px;padding:32px 24px;margin:20px 0;
    position:relative;overflow:hidden;min-height:400px;">

        <!-- Üst bilgi çubuğu -->
        <div style="background:rgba(0,0,0,0.6);backdrop-filter:blur(10px);
        border-radius:16px;padding:12px 18px;margin-bottom:20px;
        display:flex;justify-content:space-between;align-items:center;">
            <div style="color:#FAFAFA;font-size:0.82rem;">
                📍 Mevcut: <strong style="color:{renk};">{sel_loc.get('ad')}</strong>
            </div>
            <div style="color:#94A3B8;font-size:0.72rem;">SCAI-AR v1.0</div>
        </div>

        <!-- Ana AR göstergesi -->
        <div style="text-align:center;padding:40px 20px;">
            <div style="font-size:4rem;margin-bottom:12px;">{hedef_loc.get('ikon', '📍')}</div>
            <div style="background:{hedef_loc.get('renk', '#4F46E5')}40;
            border:2px solid {hedef_loc.get('renk', '#4F46E5')};border-radius:12px;
            padding:16px 24px;display:inline-block;">
                <div style="color:#FAFAFA;font-size:1.2rem;font-weight:800;">
                    {hedef_loc.get('ad')}
                </div>
                <div style="color:#E4E4E7;font-size:0.88rem;margin-top:6px;">
                    {yon_mesaj}
                </div>
                <div style="color:#D97706;font-weight:700;margin-top:8px;font-size:1.1rem;">
                    📏 ≈ {mesafe}m
                </div>
            </div>
        </div>

        <!-- Alt ipucu -->
        <div style="background:rgba(0,0,0,0.5);backdrop-filter:blur(10px);
        border-radius:12px;padding:10px 14px;margin-top:16px;color:#94A3B8;font-size:0.82rem;">
            💡 <strong style="color:#FAFAFA;">{hedef_loc.get('ad')}</strong> hakkında: {hedef_loc.get('aciklama', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# LOKASYON YÖNETİMİ
# ══════════════════════════════════════════════════════════════

def render_lokasyon_yonetim(lokasyonlar: list[dict]):
    """Lokasyonları ekle/düzenle/sil."""
    st.markdown("### ⚙️ Lokasyon Yönetimi")
    styled_info_banner(
        "Kampüsünüzdeki lokasyonları buradan yönetin. Yeni ekleyin, güncelleyin, silin.",
        "info",
    )

    tabs = st.tabs(["➕ Yeni Lokasyon", "📋 Mevcut Lokasyonlar", "🔄 Varsayılanlara Sıfırla"])

    # Yeni ekle
    with tabs[0]:
        with st.form("ar_yeni_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                loc_ad = st.text_input("Lokasyon Adı *", key="_ar_yeni_ad_widget")
                loc_bina = st.text_input("Bina", value="Ana Bina", key="_ar_yeni_bina_widget")
                loc_kat = st.number_input("Kat", -2, 10, 1, key="_ar_yeni_kat_widget")
            with c2:
                loc_ikon = st.text_input("İkon (emoji)", value="📍", key="_ar_yeni_ikon_widget")
                loc_renk = st.color_picker("Renk", value="#4F46E5", key="_ar_yeni_renk_widget")
                loc_mesafe = st.number_input("Mesafe (m)", 1, 500, 20, key="_ar_yeni_mesafe_widget")

            loc_aciklama = st.text_input("Açıklama", key="_ar_yeni_ac_widget")
            loc_yon = st.selectbox(
                "Yön (ana girişten)",
                ["ileri", "geri", "sag", "sol", "yukari", "asagi",
                 "ileri_saga", "yukari_sag", "sol_geri"],
                key="_ar_yeni_yon_widget",
            )

            if st.form_submit_button("➕ Lokasyon Ekle", type="primary"):
                if loc_ad.strip():
                    lokasyonlar.append({
                        "id": f"LOC-{len(lokasyonlar)+1:03d}",
                        "ad": loc_ad.strip(),
                        "bina": loc_bina.strip(),
                        "kat": loc_kat,
                        "ikon": loc_ikon,
                        "renk": loc_renk,
                        "aciklama": loc_aciklama.strip(),
                        "yon": loc_yon,
                        "mesafe_m": loc_mesafe,
                    })
                    _save_lokasyonlar(lokasyonlar)
                    st.success(f"✅ {loc_ad} eklendi.")
                    st.rerun()

    # Mevcut
    with tabs[1]:
        for i, loc in enumerate(lokasyonlar):
            with st.expander(f"{loc.get('ikon', '📍')} **{loc.get('ad', '')}** ({loc.get('bina', '')} · Kat {loc.get('kat', 0)})"):
                st.markdown(f"**Açıklama:** {loc.get('aciklama', '—')}")
                st.markdown(f"**Yön:** {loc.get('yon', '—')} · **Mesafe:** {loc.get('mesafe_m', 0)}m")
                st.markdown(f"**ID:** `{loc.get('id', '')}`")
                if st.button("🗑️ Sil", key=f"_ar_del_{loc.get('id')}"):
                    lokasyonlar.remove(loc)
                    _save_lokasyonlar(lokasyonlar)
                    st.rerun()

    # Sıfırla
    with tabs[2]:
        styled_info_banner(
            "Tüm lokasyonlar silinecek ve varsayılan 15 lokasyon geri yüklenecek.",
            "warning",
        )
        if st.button("🔄 Varsayılanlara Sıfırla", type="secondary", key="_ar_reset"):
            _save_lokasyonlar(DEFAULT_LOKASYONLAR.copy())
            st.success("✅ Sıfırlandı.")
            st.rerun()


# ══════════════════════════════════════════════════════════════
# ANA PANEL
# ══════════════════════════════════════════════════════════════

def render_ar_kampus_haritasi():
    """AR Kampüs Haritası ana paneli."""
    styled_section("🗺️ AR Kampüs Haritası", "#4F46E5")

    styled_info_banner(
        "Ziyaretçiler ve yeni veliler için kampüs rehberi. QR kod sistemi + interaktif harita. "
        "Gerçek AR için mobil uygulama entegrasyonu önerilir.",
        "info", "🗺️",
    )

    lokasyonlar = _load_lokasyonlar()

    # İstatistik
    binalar = set(loc.get("bina", "Ana Bina") for loc in lokasyonlar)
    katlar = set(loc.get("kat", 0) for loc in lokasyonlar)

    styled_stat_row([
        ("Toplam Lokasyon", str(len(lokasyonlar)), "#4F46E5", "📍"),
        ("Bina", str(len(binalar)), "#7C3AED", "🏢"),
        ("Kat Sayısı", str(len(katlar)), "#059669", "🏗️"),
        ("QR Sistem", "Aktif", "#D97706", "📱"),
    ])

    tabs = st.tabs(["🗺️ İnteraktif Harita", "📱 QR Kodları", "🔍 AR Önizleme", "⚙️ Yönetim"])

    with tabs[0]:
        render_kampus_harita(lokasyonlar)

    with tabs[1]:
        render_qr_kodlari(lokasyonlar)

    with tabs[2]:
        render_ar_simulator(lokasyonlar)

    with tabs[3]:
        render_lokasyon_yonetim(lokasyonlar)
