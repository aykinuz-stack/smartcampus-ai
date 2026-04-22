"""
Başarı Duvarı
=================
Öğrencinin kişisel Instagram tarzı başarı vitrini.
Rozetler, yarışma dereceleri, proje sunumları, olumlu davranışlar.
Veliler görür, mezuniyet dosyası otomatik.
"""
from __future__ import annotations

import json
import os
from datetime import datetime

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# ROZET KATALOĞU
# ══════════════════════════════════════════════════════════════

ROZET_KATALOGU = {
    # Akademik
    "yildiz_ogrenci":   {"ad": "Yıldız Öğrenci", "ikon": "⭐", "renk": "#D97706", "kategori": "Akademik",
                         "sart": "Dönem sonu ortalaması 90+"},
    "bilge":            {"ad": "Bilge", "ikon": "🦉", "renk": "#7C3AED", "kategori": "Akademik",
                         "sart": "Tüm derslerde 85+"},
    "matematik_ustasi": {"ad": "Matematik Ustası", "ikon": "📐", "renk": "#0284C7", "kategori": "Akademik",
                         "sart": "Matematik notu 95+"},
    "edebiyat_askigi":  {"ad": "Edebiyat Aşığı", "ikon": "📚", "renk": "#EC4899", "kategori": "Akademik",
                         "sart": "Kompozisyon yarışması 1.liği"},
    "bilim_kasifi":     {"ad": "Bilim Kaşifi", "ikon": "🔬", "renk": "#059669", "kategori": "Akademik",
                         "sart": "Fen projesi sunumu"},

    # Sosyal
    "lider":            {"ad": "Lider", "ikon": "👑", "renk": "#DC2626", "kategori": "Sosyal",
                         "sart": "Sınıf başkanlığı"},
    "takim_oyuncusu":   {"ad": "Takım Oyuncusu", "ikon": "🤝", "renk": "#4F46E5", "kategori": "Sosyal",
                         "sart": "Grup projesinde en katkılı"},
    "yardimsever":      {"ad": "Yardımsever", "ikon": "💝", "renk": "#EC4899", "kategori": "Sosyal",
                         "sart": "Akran yardımı / mentorluk"},
    "barisin_sesi":     {"ad": "Barışın Sesi", "ikon": "🕊️", "renk": "#0D9488", "kategori": "Sosyal",
                         "sart": "Arabuluculuk yaptı"},

    # Sanat
    "sanatci_ruhu":     {"ad": "Sanatçı Ruhu", "ikon": "🎨", "renk": "#9333EA", "kategori": "Sanat",
                         "sart": "Resim sergisi"},
    "muzik_perisi":     {"ad": "Müzik Perisi", "ikon": "🎵", "renk": "#EC4899", "kategori": "Sanat",
                         "sart": "Okul korosu"},
    "sahnenin_yildizi": {"ad": "Sahnenin Yıldızı", "ikon": "🎭", "renk": "#DC2626", "kategori": "Sanat",
                         "sart": "Tiyatro oyunu"},

    # Spor
    "sampiyon":         {"ad": "Şampiyon", "ikon": "🏆", "renk": "#D97706", "kategori": "Spor",
                         "sart": "Spor yarışmasında derece"},
    "fairplay":         {"ad": "Fair Play", "ikon": "🤲", "renk": "#059669", "kategori": "Spor",
                         "sart": "Sporcu davranışı"},
    "takim_kaptani":    {"ad": "Takım Kaptanı", "ikon": "⚽", "renk": "#0284C7", "kategori": "Spor",
                         "sart": "Okul takımı kaptanlığı"},

    # Özel
    "mezuniyet":        {"ad": "Mezun", "ikon": "🎓", "renk": "#4F46E5", "kategori": "Özel",
                         "sart": "Okulumuzdan mezun oldu"},
    "tam_devam":        {"ad": "Tam Devam", "ikon": "📅", "renk": "#059669", "kategori": "Özel",
                         "sart": "Yıl boyunca devamsızlık yok"},
    "olimpiyat":        {"ad": "Olimpiyat Madalyası", "ikon": "🥇", "renk": "#D97706", "kategori": "Özel",
                         "sart": "Olimpiyat katılımı"},
    "proje_sampiyonu":  {"ad": "Proje Şampiyonu", "ikon": "🎯", "renk": "#DC2626", "kategori": "Özel",
                         "sart": "TÜBİTAK vb. proje derecesi"},
    "kitapkurdu":       {"ad": "Kitap Kurdu", "ikon": "🐛", "renk": "#7C3AED", "kategori": "Özel",
                         "sart": "Yılda 30+ kitap okudu"},

    # Karakter
    "durustluk":        {"ad": "Dürüstlük", "ikon": "✨", "renk": "#0D9488", "kategori": "Karakter",
                         "sart": "Örnek dürüstlük davranışı"},
    "sorumluluk":       {"ad": "Sorumluluk", "ikon": "💪", "renk": "#4F46E5", "kategori": "Karakter",
                         "sart": "Görev bilinci"},
    "saygi":            {"ad": "Saygı", "ikon": "🙏", "renk": "#7C3AED", "kategori": "Karakter",
                         "sart": "Saygı örneği"},
}


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _duvar_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "basari_duvari")
    except Exception:
        d = os.path.join("data", "basari_duvari")
    os.makedirs(d, exist_ok=True)
    return d


def _duvar_path() -> str:
    return os.path.join(_duvar_dir(), "basarilar.json")


def _load_basarilar() -> list[dict]:
    p = _duvar_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_basarilar(data: list[dict]) -> None:
    with open(_duvar_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# ROZET VERME
# ══════════════════════════════════════════════════════════════

def rozet_ver(student_id: str, student_name: str, rozet_kod: str,
               not_text: str = "", veren: str = "") -> bool:
    """Öğrenciye rozet ver."""
    if rozet_kod not in ROZET_KATALOGU:
        return False
    basarilar = _load_basarilar()
    basarilar.append({
        "id": f"BSR-{len(basarilar)+1:06d}",
        "student_id": student_id,
        "student_name": student_name,
        "tip": "rozet",
        "rozet_kod": rozet_kod,
        "rozet_ad": ROZET_KATALOGU[rozet_kod]["ad"],
        "rozet_ikon": ROZET_KATALOGU[rozet_kod]["ikon"],
        "rozet_renk": ROZET_KATALOGU[rozet_kod]["renk"],
        "kategori": ROZET_KATALOGU[rozet_kod]["kategori"],
        "not": not_text,
        "veren": veren,
        "tarih": datetime.now().isoformat(),
        "begenen_sayisi": 0,
    })
    _save_basarilar(basarilar)
    return True


# ══════════════════════════════════════════════════════════════
# ÖĞRENCİ BAŞARI DUVARI VİTRİNİ
# ══════════════════════════════════════════════════════════════

def render_ogrenci_basari_duvari(student_id: str, student_name: str):
    """Instagram tarzı başarı vitrini."""
    basarilar = _load_basarilar()
    ogr_basarilar = [b for b in basarilar if b.get("student_id") == student_id]
    ogr_basarilar.sort(key=lambda x: x.get("tarih", ""), reverse=True)

    # Profil header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4F46E5 0%,#7C3AED 50%,#EC4899 100%);
    border-radius:16px;padding:24px;color:white;text-align:center;margin:12px 0;
    box-shadow:0 12px 40px rgba(79,70,229,0.3);">
        <div style="width:80px;height:80px;background:white;border-radius:50%;
        display:flex;align-items:center;justify-content:center;margin:0 auto 12px;
        font-size:2.5rem;color:#4F46E5;font-weight:900;">
            {student_name[0] if student_name else '?'}
        </div>
        <div style="font-size:1.5rem;font-weight:800;margin-bottom:4px;">{student_name}</div>
        <div style="font-size:0.88rem;opacity:0.9;">🏆 {len(ogr_basarilar)} başarı</div>
    </div>
    """, unsafe_allow_html=True)

    # Kategori breakdown
    from collections import Counter
    kategoriler = Counter(b.get("kategori", "Diğer") for b in ogr_basarilar)

    if kategoriler:
        styled_stat_row([
            (kat, str(sayi), "#D97706", "🏅")
            for kat, sayi in list(kategoriler.most_common(5))
        ])

    if not ogr_basarilar:
        styled_info_banner(
            "Henüz başarı yok. Her başarı buraya eklendikçe duvarın zenginleşir!",
            "info", "🌱",
        )
        return

    # Filter
    filter_cat = st.selectbox(
        "Kategori",
        ["Tümü"] + list(set(b.get("kategori", "Diğer") for b in ogr_basarilar)),
        key=f"_bsr_filter_{student_id}",
    )

    filtered = ogr_basarilar if filter_cat == "Tümü" else [b for b in ogr_basarilar if b.get("kategori") == filter_cat]

    # Instagram-style grid
    st.markdown("### 🏆 Başarı Vitrini")

    # 3 sütunlu grid
    cols_per_row = 3
    for row_start in range(0, len(filtered), cols_per_row):
        cols = st.columns(cols_per_row)
        row_items = filtered[row_start:row_start + cols_per_row]
        for col, item in zip(cols, row_items):
            with col:
                _render_basari_kart(item)


def _render_basari_kart(basari: dict):
    """Tek bir başarı kartı — post tarzı."""
    ikon = basari.get("rozet_ikon", "🏅")
    renk = basari.get("rozet_renk", "#D97706")
    ad = basari.get("rozet_ad", basari.get("baslik", "Başarı"))
    tarih = basari.get("tarih", "")[:10]
    not_text = basari.get("not", "")
    veren = basari.get("veren", "")
    begen = basari.get("begenen_sayisi", 0)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{renk}20,{renk}05);
    border:2px solid {renk}40;border-radius:16px;padding:16px;margin:8px 0;
    box-shadow:0 4px 14px rgba(0,0,0,0.1);text-align:center;
    transition:transform 0.2s;">
        <div style="font-size:3rem;margin-bottom:8px;">{ikon}</div>
        <div style="font-size:1rem;font-weight:700;color:{renk};margin-bottom:4px;">{ad}</div>
        <div style="font-size:0.75rem;color:#94A3B8;margin-bottom:8px;">📅 {tarih}</div>
        {f'<div style="font-size:0.85rem;color:#E4E4E7;margin-top:8px;padding:8px;background:rgba(0,0,0,0.2);border-radius:8px;">{not_text[:80]}{"..." if len(not_text) > 80 else ""}</div>' if not_text else ""}
        {f'<div style="font-size:0.72rem;color:#64748B;margin-top:6px;">— {veren}</div>' if veren else ""}
        <div style="margin-top:10px;font-size:0.78rem;color:#EC4899;">
            ❤️ {begen} beğeni
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ÖĞRETMEN PANELİ — Rozet Ver
# ══════════════════════════════════════════════════════════════

def render_ogretmen_rozet_ver_panel():
    """Öğretmen/müdür için rozet verme paneli."""
    styled_section("🏅 Rozet Ver (Öğretmen/Yönetim)", "#D97706")

    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        students = ak.get_students(durum="aktif")
    except Exception:
        students = []

    if not students:
        styled_info_banner("Öğrenci bulunamadı.", "warning")
        return

    try:
        auth = st.session_state.get("auth_user", {})
        veren_ad = auth.get("name", "Öğretmen")
    except Exception:
        veren_ad = "Öğretmen"

    with st.form("rozet_ver_form"):
        col1, col2 = st.columns(2)
        with col1:
            student_names = [f"{s.tam_ad} ({s.sinif}/{s.sube})" for s in students]
            sel_idx = st.selectbox(
                "Öğrenci",
                range(len(students)),
                format_func=lambda i: student_names[i],
                key="_bsr_ver_stu_widget",
            )

        with col2:
            # Kategori bazlı rozet seç
            kategoriler = list(set(r["kategori"] for r in ROZET_KATALOGU.values()))
            sel_kategori = st.selectbox("Kategori", sorted(kategoriler), key="_bsr_ver_kat_widget")

        # Kategoriye göre rozet
        kategori_rozetleri = {k: v for k, v in ROZET_KATALOGU.items() if v["kategori"] == sel_kategori}
        rozet_kod = st.selectbox(
            "Rozet",
            list(kategori_rozetleri.keys()),
            format_func=lambda x: f"{kategori_rozetleri[x]['ikon']} {kategori_rozetleri[x]['ad']} — {kategori_rozetleri[x]['sart']}",
            key="_bsr_ver_rozet_widget",
        )

        not_text = st.text_area(
            "Neden bu rozeti veriyorsun? (Öğrenci ve veli görecek)",
            placeholder="Örn: Matematik yarışmasında ikinci oldun, tebrikler!",
            height=80,
            key="_bsr_ver_not_widget",
        )

        if st.form_submit_button("🎖️ Rozeti Ver", type="primary"):
            if not not_text.strip():
                styled_info_banner("Açıklama zorunlu (öğrenci ve veli görecek).", "warning")
            else:
                stu = students[sel_idx]
                success = rozet_ver(stu.id, stu.tam_ad, rozet_kod, not_text.strip(), veren_ad)
                if success:
                    st.balloons()
                    rozet = ROZET_KATALOGU[rozet_kod]
                    st.success(f"✅ **{stu.tam_ad}** öğrencisine **{rozet['ikon']} {rozet['ad']}** rozeti verildi!")


# ══════════════════════════════════════════════════════════════
# ANA PANEL
# ══════════════════════════════════════════════════════════════

def render_basari_duvari():
    """Ana panel — öğrenci vitrini + öğretmen paneli."""
    styled_section("🏆 Başarı Duvarı", "#D97706")

    styled_info_banner(
        "Her öğrencinin kişisel başarı vitrini. Rozetler, yarışma dereceleri, özel davranışlar. "
        "Veliler görür. Mezuniyet dosyası otomatik oluşturulur.",
        "info", "🏆",
    )

    tabs = st.tabs(["👤 Öğrenci Vitrini", "🏅 Rozet Ver", "📚 Rozet Kataloğu", "📊 İstatistikler"])

    with tabs[0]:
        try:
            from models.akademik_takip import AkademikDataStore
            ak = AkademikDataStore()
            students = ak.get_students(durum="aktif")
        except Exception:
            students = []

        if not students:
            styled_info_banner("Öğrenci bulunamadı.", "warning")
        else:
            student_names = [f"{s.tam_ad} ({s.sinif}/{s.sube})" for s in students]
            sel_idx = st.selectbox(
                "Öğrenci seç",
                range(len(students)),
                format_func=lambda i: student_names[i],
                key="_bsr_vit_stu_widget",
            )
            selected = students[sel_idx]
            render_ogrenci_basari_duvari(selected.id, selected.tam_ad)

    with tabs[1]:
        render_ogretmen_rozet_ver_panel()

    with tabs[2]:
        styled_section("📚 Rozet Kataloğu", "#7C3AED")
        st.caption(f"{len(ROZET_KATALOGU)} farklı rozet, 6 kategori")

        kategoriler = {}
        for kod, r in ROZET_KATALOGU.items():
            kategoriler.setdefault(r["kategori"], []).append((kod, r))

        for kat, rozetler in sorted(kategoriler.items()):
            st.markdown(f"### {kat}")
            cols = st.columns(4)
            for i, (kod, r) in enumerate(rozetler):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="background:{r['renk']}15;border:2px solid {r['renk']}40;
                    border-radius:12px;padding:14px;text-align:center;margin:4px 0;">
                        <div style="font-size:2rem;margin-bottom:4px;">{r['ikon']}</div>
                        <div style="font-size:0.88rem;font-weight:700;color:{r['renk']};">{r['ad']}</div>
                        <div style="font-size:0.72rem;color:#94A3B8;margin-top:4px;">{r['sart']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with tabs[3]:
        basarilar = _load_basarilar()
        if not basarilar:
            styled_info_banner("Henüz başarı kaydı yok.", "info")
            return

        # Genel istatistik
        from collections import Counter
        kat_counts = Counter(b.get("kategori", "Diğer") for b in basarilar)
        rozet_counts = Counter(b.get("rozet_ad", "?") for b in basarilar)
        stu_counts = Counter(b.get("student_name", "?") for b in basarilar)

        styled_stat_row([
            ("Toplam Başarı", str(len(basarilar)), "#D97706", "🏆"),
            ("Farklı Kategori", str(len(kat_counts)), "#7C3AED", "🏅"),
            ("Rozetli Öğrenci", str(len(stu_counts)), "#4F46E5", "👥"),
            ("En Çok Verilen", rozet_counts.most_common(1)[0][0] if rozet_counts else "-", "#EC4899", "⭐"),
        ])

        # Top 10 öğrenci
        st.markdown("### 🏆 En Çok Rozet Alan 10 Öğrenci")
        for i, (ad, sayi) in enumerate(stu_counts.most_common(10), 1):
            st.markdown(f"**{i}.** {ad} — **{sayi} rozet**")
