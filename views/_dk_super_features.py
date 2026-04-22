"""
Dijital Kütüphane — Süper Özellikler
======================================
1. Kullanım Analitik & İçerik Trend Paneli
2. Öğretmen İçerik Atama & Kazanım Eşleştirme
3. Dijital Öğrenme Liderlik Tablosu & Başarı Portfolyosu
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "dijital_kutuphane"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}

_ICERIK_KATEGORILERI = [
    "Zeka Oyunlari", "3D Egitim", "Bilgi Yarismasi", "Kodlama", "Deney Lab",
    "Sanat Studyosu", "Sesli Kitap", "e-Kitaplik", "Okuma Maratonu", "Kitap Kulubu",
    "Masallar", "Radyo", "Canli TV", "Muze", "AI Asistan", "Diger",
]

_KAZANIM_ICERIK_MAP = {
    "Matematik": ["Zeka Oyunlari", "Kodlama", "3D Egitim"],
    "Turkce": ["Sesli Kitap", "Okuma Maratonu", "Hikaye Atolyesi", "Kitap Kulubu"],
    "Fen Bilimleri": ["Deney Lab", "3D Egitim", "AI Asistan"],
    "Sosyal Bilgiler": ["Muze", "3D Egitim", "Bilgi Yarismasi"],
    "Ingilizce": ["Kisisel Dil Gelisimi", "Sesli Kitap", "AI Asistan"],
    "Gorsel Sanatlar": ["Sanat Studyosu", "3D Egitim"],
    "Muzik": ["Radyo"],
    "Bilisim": ["Kodlama", "AI Asistan", "Zeka Oyunlari"],
}

_XP_AKTIVITE = {
    "Oyun Tamamla": 5, "Quiz Dogru": 3, "Kitap Oku": 8, "Deney Tamamla": 10,
    "Kod Projesi": 12, "Sanat Eseri": 7, "Yarisma Katilim": 6, "AI Sohbet": 4,
    "Video Izle": 2, "Sesli Kitap Dinle": 5, "Okuma Suresi (30dk)": 4,
}

_ROZETLER = [
    {"ad": "Ilk Giris", "ikon": "🌱", "kosul": "giris_1", "hedef": 1, "xp": 5, "renk": "#10b981"},
    {"ad": "Oyun Ustasi", "ikon": "🎮", "kosul": "oyun_20", "hedef": 20, "xp": 30, "renk": "#8b5cf6"},
    {"ad": "Kitap Kurdu", "ikon": "📚", "kosul": "kitap_10", "hedef": 10, "xp": 40, "renk": "#3b82f6"},
    {"ad": "Bilim Insani", "ikon": "🔬", "kosul": "deney_5", "hedef": 5, "xp": 25, "renk": "#059669"},
    {"ad": "Kodcu", "ikon": "💻", "kosul": "kod_5", "hedef": 5, "xp": 30, "renk": "#6366f1"},
    {"ad": "Sanatci", "ikon": "🎨", "kosul": "sanat_5", "hedef": 5, "xp": 20, "renk": "#f59e0b"},
    {"ad": "Cok Yonlu", "ikon": "🌈", "kosul": "kategori_5", "hedef": 5, "xp": 35, "renk": "#0891b2"},
    {"ad": "Maraton Kosucu", "ikon": "🏃", "kosul": "sure_300", "hedef": 300, "xp": 40, "renk": "#ef4444"},
    {"ad": "Yildiz Ogrenci", "ikon": "⭐", "kosul": "xp_300", "hedef": 300, "xp": 50, "renk": "#c9a84c"},
    {"ad": "Efsane", "ikon": "💎", "kosul": "xp_1000", "hedef": 1000, "xp": 100, "renk": "#8b5cf6"},
]

_SEVIYELER = {
    (0, 50): ("Kesfedici", "🟤"), (50, 150): ("Merakli", "🥉"),
    (150, 300): ("Ogrenci", "🥈"), (300, 600): ("Uzman", "🥇"),
    (600, 1000): ("Usta", "👑"), (1000, 99999): ("Efsane", "💎"),
}


# ════════════════════════════════════════════════════════════
# 1. KULLANIM ANALİTİK & İÇERİK TREND PANELİ
# ════════════════════════════════════════════════════════════

def render_dk_analitik():
    """Kullanım Analitik — hangi içerik popüler, zaman analizi, sınıf karşılaştırma."""
    styled_section("Kullanim Analitik & Icerik Trend Paneli", "#2563eb")
    styled_info_banner(
        "Hangi icerik en cok kullaniliyor, hangi sinif ne kadar aktif, "
        "haftalik/aylik trend, ogretmene icerik onerisi.",
        banner_type="info", icon="📊")

    kullanim = _lj("dk_kullanim_log.json")

    bugun = date.today().isoformat()
    bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    bu_ay = date.today().strftime("%Y-%m")

    bugun_sayi = sum(1 for k in kullanim if k.get("tarih","")[:10] == bugun)
    hafta_sayi = sum(1 for k in kullanim if k.get("tarih","")[:10] >= bu_hafta)
    ay_sayi = sum(1 for k in kullanim if k.get("tarih","")[:7] == bu_ay)
    aktif_ogr = len(set(k.get("ogrenci","") for k in kullanim if k.get("tarih","")[:7] == bu_ay))

    styled_stat_row([
        ("Bugun", str(bugun_sayi), "#2563eb", "📅"),
        ("Bu Hafta", str(hafta_sayi), "#3b82f6", "📊"),
        ("Bu Ay", str(ay_sayi), "#8b5cf6", "📈"),
        ("Aktif Ogrenci", str(aktif_ogr), "#10b981", "👥"),
        ("Toplam Log", str(len(kullanim)), "#f59e0b", "📋"),
    ])

    sub = st.tabs(["📊 En Populer", "📈 Haftalik Trend", "🏫 Sinif Analizi", "💡 Ogretmen Onerisi", "📝 Log Kaydet"])

    # ── EN POPÜLER ──
    with sub[0]:
        styled_section("En Cok Kullanilan Icerikler")
        if not kullanim:
            st.info("Kullanim verisi yok. 'Log Kaydet' sekmesinden veri girin.")
        else:
            kat_say = Counter(k.get("kategori","?") for k in kullanim)
            max_val = kat_say.most_common(1)[0][1] if kat_say else 1
            for kat, sayi in kat_say.most_common(12):
                pct = round(sayi / max(max_val, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                    <span style="min-width:140px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{kat}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#2563eb;border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── HAFTALIK TREND ──
    with sub[1]:
        styled_section("Haftalik Kullanim Trendi")
        if not kullanim:
            st.info("Veri yok.")
        else:
            hafta_grp = Counter()
            for k in kullanim:
                tarih = k.get("tarih","")[:10]
                if tarih:
                    try:
                        dt = date.fromisoformat(tarih)
                        hb = dt - timedelta(days=dt.weekday())
                        hafta_grp[hb.isoformat()] += 1
                    except Exception: pass

            if hafta_grp:
                max_h = max(hafta_grp.values())
                for h in sorted(hafta_grp.keys())[-8:]:
                    sayi = hafta_grp[h]
                    pct = round(sayi / max(max_h, 1) * 100)
                    is_bu = h == (date.today() - timedelta(days=date.today().weekday())).isoformat()
                    renk = "#c9a84c" if is_bu else "#3b82f6"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                        {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                        <span style="min-width:70px;font-size:0.7rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{h[5:]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── SINIF ANALİZİ ──
    with sub[2]:
        styled_section("Sinif Bazli Kullanim")
        if kullanim:
            sinif_grp = Counter(k.get("sinif","?") for k in kullanim)
            for sinif, sayi in sinif_grp.most_common(15):
                pct = round(sayi / max(len(kullanim), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;min-width:50px;">{sinif}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#3b82f6;border-radius:4px;"></div>
                    </div>
                    <span style="color:#64748b;font-size:0.68rem;">{sayi} (%{pct})</span>
                </div>""", unsafe_allow_html=True)

    # ── ÖĞRETMEN ÖNERİSİ ──
    with sub[3]:
        styled_section("Ogretmene Icerik Onerisi")
        for ders, icerikler in _KAZANIM_ICERIK_MAP.items():
            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid #2563eb;border-radius:0 10px 10px 0;
                padding:8px 14px;margin:5px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">📚 {ders}</span>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                    Onerilen: {' · '.join(icerikler)}</div>
            </div>""", unsafe_allow_html=True)

    # ── LOG KAYDET ──
    with sub[4]:
        styled_section("Kullanim Logu Kaydet")
        with st.form("dk_log_form"):
            c1, c2 = st.columns(2)
            with c1:
                l_ogr = st.text_input("Ogrenci Adi", key="dl_ogr")
                l_kat = st.selectbox("Icerik Kategorisi", _ICERIK_KATEGORILERI, key="dl_kat")
            with c2:
                l_sinif = st.text_input("Sinif/Sube", placeholder="7/A", key="dl_sinif")
                l_sure = st.number_input("Sure (dk)", min_value=1, value=15, key="dl_sure")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if l_ogr:
                    kullanim.append({
                        "ogrenci": l_ogr, "kategori": l_kat,
                        "sinif": l_sinif, "sure_dk": l_sure,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("dk_kullanim_log.json", kullanim)
                    st.success(f"{l_ogr}: {l_kat} — {l_sure}dk")
                    st.rerun()


# ════════════════════════════════════════════════════════════
# 2. ÖĞRETMEN İÇERİK ATAMA & KAZANIM EŞLEŞTİRME
# ════════════════════════════════════════════════════════════

def render_dk_icerik_atama():
    """Öğretmen İçerik Atama — ders entegrasyon, kazanım eşleştirme, tamamlanma takip."""
    styled_section("Ogretmen Icerik Atama & Kazanim Eslestirme", "#059669")
    styled_info_banner(
        "Dersiniz icin dijital kutuphaneden icerik secin ve sinifa atayin. "
        "MEB kazanimlariyla eslestirme, tamamlanma takibi, veli raporu.",
        banner_type="info", icon="🎓")

    atamalar = _lj("dk_icerik_atamalari.json")
    tamamlanmalar = _lj("dk_tamamlanma.json")

    styled_stat_row([
        ("Atama", str(len(atamalar)), "#059669", "📋"),
        ("Tamamlanma", str(len(tamamlanmalar)), "#10b981", "✅"),
    ])

    sub = st.tabs(["➕ Icerik Ata", "📋 Atama Listesi", "✅ Tamamlanma Takip", "📊 Kazanim Eslestirme"])

    # ── İÇERİK ATA ──
    with sub[0]:
        styled_section("Sinifa Icerik Ata")
        with st.form("atama_form"):
            c1, c2 = st.columns(2)
            with c1:
                a_sinif = st.text_input("Sinif/Sube", placeholder="7/A", key="ia_sinif")
                a_ders = st.selectbox("Ders", list(_KAZANIM_ICERIK_MAP.keys()), key="ia_ders")
                a_ogretmen = st.text_input("Ogretmen", key="ia_ogr")
            with c2:
                onerilen = _KAZANIM_ICERIK_MAP.get(a_ders, _ICERIK_KATEGORILERI) if a_ders else _ICERIK_KATEGORILERI
                a_icerikler = st.multiselect("Icerikler", _ICERIK_KATEGORILERI, default=onerilen[:2], key="ia_icerik")
                a_termin = st.date_input("Termin", key="ia_termin")
            a_kazanim = st.text_input("Kazanim (MEB kodu veya aciklama)", key="ia_kaz")
            a_aciklama = st.text_area("Talimat / Aciklama", height=50, key="ia_acik")

            if st.form_submit_button("Ata", use_container_width=True, type="primary"):
                if a_sinif and a_icerikler:
                    atamalar.append({
                        "id": f"ia_{uuid.uuid4().hex[:8]}",
                        "sinif": a_sinif, "ders": a_ders, "ogretmen": a_ogretmen,
                        "icerikler": a_icerikler, "kazanim": a_kazanim,
                        "termin": a_termin.isoformat(), "aciklama": a_aciklama,
                        "durum": "Aktif", "created_at": datetime.now().isoformat(),
                    })
                    _sj("dk_icerik_atamalari.json", atamalar)
                    st.success(f"{a_sinif} icin {len(a_icerikler)} icerik atandi!")
                    st.rerun()

    # ── ATAMA LİSTESİ ──
    with sub[1]:
        styled_section("Aktif Atamalar")
        if not atamalar:
            st.info("Atama yok.")
        else:
            for a in sorted(atamalar, key=lambda x: x.get("termin",""), reverse=True):
                renk = "#10b981" if a.get("durum") == "Tamamlandi" else "#059669"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">🎓 {a.get('sinif','')} — {a.get('ders','')}</span>
                        <span style="color:#64748b;font-size:0.68rem;">Termin: {a.get('termin','')[:10]}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        Icerik: {', '.join(a.get('icerikler',[]))} | Ogretmen: {a.get('ogretmen','')}</div>
                    {f"<div style='color:#10b981;font-size:0.68rem;margin-top:2px;'>Kazanim: {a.get('kazanim','')}</div>" if a.get('kazanim') else ''}
                </div>""", unsafe_allow_html=True)

    # ── TAMAMLANMA TAKİP ──
    with sub[2]:
        styled_section("Ogrenci Tamamlanma Takibi")
        with st.form("tamam_form"):
            c1, c2 = st.columns(2)
            with c1:
                t_ogr = st.text_input("Ogrenci", key="tm_ogr")
                if atamalar:
                    t_atama = st.selectbox("Atama",
                        [f"{a.get('sinif','')} {a.get('ders','')} ({a.get('termin','')[:10]})" for a in atamalar],
                        key="tm_atama")
                else:
                    t_atama = st.text_input("Atama", key="tm_atama")
            with c2:
                t_icerik = st.selectbox("Tamamlanan Icerik", _ICERIK_KATEGORILERI, key="tm_icerik")
                t_sure = st.number_input("Harcanan Sure (dk)", min_value=1, value=15, key="tm_sure")

            if st.form_submit_button("Tamamlandi", use_container_width=True):
                if t_ogr:
                    tamamlanmalar.append({
                        "ogrenci": t_ogr, "atama": t_atama,
                        "icerik": t_icerik, "sure_dk": t_sure,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("dk_tamamlanma.json", tamamlanmalar)
                    st.success(f"{t_ogr}: {t_icerik} tamamlandi!")
                    st.rerun()

        if tamamlanmalar:
            ogr_say = Counter(t.get("ogrenci","") for t in tamamlanmalar)
            styled_section("En Aktif Ogrenciler")
            for ogr, sayi in ogr_say.most_common(10):
                st.markdown(f"  - **{ogr}**: {sayi} icerik tamamladi")

    # ── KAZANIM EŞLEŞTİRME ──
    with sub[3]:
        styled_section("Ders — Dijital Icerik Eslestirme Haritasi")
        for ders, icerikler in _KAZANIM_ICERIK_MAP.items():
            st.markdown(f"""
            <div style="background:#0f172a;border-left:5px solid #059669;border-radius:0 12px 12px 0;
                padding:10px 14px;margin:6px 0;">
                <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">📚 {ders}</span>
                <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">
                    {''.join(f"<span style=\\'background:#05966920;color:#10b981;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:600;\\'>{ic}</span>" for ic in icerikler)}
                </div>
            </div>""".replace("\\'", "'"), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. DİJİTAL ÖĞRENME LİDERLİK TABLOSU & BAŞARI PORTFOLYOSU
# ════════════════════════════════════════════════════════════

def _seviye_bilgi(xp):
    for (lo, hi), (ad, ikon) in _SEVIYELER.items():
        if lo <= xp < hi:
            pct = round((xp - lo) / max(hi - lo, 1) * 100)
            return ad, ikon, pct, hi - xp
    return "Efsane", "💎", 100, 0


def render_dk_liderlik():
    """Dijital Öğrenme Liderlik Tablosu — XP, rozet, portfolyo."""
    styled_section("Dijital Ogrenme Liderlik Tablosu & Basari Portfolyosu", "#c9a84c")
    styled_info_banner(
        "Tum dijital kutuphane aktivitelerinden birlesik liderlik tablosu. "
        "XP, seviye, rozet koleksiyonu, kisisel basari portfolyosu.",
        banner_type="info", icon="🏆")

    kullanim = _lj("dk_kullanim_log.json")
    tamamlanmalar = _lj("dk_tamamlanma.json")

    sub = st.tabs(["👤 Profil", "🏆 Liderlik", "🎖️ Rozet Vitrini", "📊 XP Tablosu"])

    # ── PROFİL ──
    with sub[0]:
        styled_section("Kisisel Basari Portfolyosu")
        students = load_shared_students()
        if not students:
            ogr_opts = list(set(k.get("ogrenci","") for k in kullanim + tamamlanmalar))
        else:
            ogr_opts = [f"{s.get('ad','')} {s.get('soyad','')}" for s in students]

        if not ogr_opts:
            st.info("Ogrenci verisi yok.")
            return

        sec = st.selectbox("Ogrenci", ogr_opts, key="ldr_ogr")

        # XP hesapla
        ogr_kull = [k for k in kullanim if k.get("ogrenci") == sec]
        ogr_tam = [t for t in tamamlanmalar if t.get("ogrenci") == sec]

        xp = len(ogr_kull) * 3 + len(ogr_tam) * 8
        toplam_sure = sum(k.get("sure_dk", 0) for k in ogr_kull)
        kategori_say = len(set(k.get("kategori","") for k in ogr_kull))

        # Rozetler
        kazanilan = []
        for r in _ROZETLER:
            kazandi = False
            if r["kosul"] == "giris_1" and len(ogr_kull) >= 1: kazandi = True
            elif r["kosul"] == "oyun_20" and sum(1 for k in ogr_kull if "Oyun" in k.get("kategori","")) >= 20: kazandi = True
            elif r["kosul"] == "kitap_10" and sum(1 for k in ogr_kull if "Kitap" in k.get("kategori","") or "Okuma" in k.get("kategori","")) >= 10: kazandi = True
            elif r["kosul"] == "deney_5" and sum(1 for k in ogr_kull if "Deney" in k.get("kategori","")) >= 5: kazandi = True
            elif r["kosul"] == "kod_5" and sum(1 for k in ogr_kull if "Kodlama" in k.get("kategori","")) >= 5: kazandi = True
            elif r["kosul"] == "sanat_5" and sum(1 for k in ogr_kull if "Sanat" in k.get("kategori","")) >= 5: kazandi = True
            elif r["kosul"] == "kategori_5" and kategori_say >= 5: kazandi = True
            elif r["kosul"] == "sure_300" and toplam_sure >= 300: kazandi = True
            elif r["kosul"] == "xp_300" and xp >= 300: kazandi = True
            elif r["kosul"] == "xp_1000" and xp >= 1000: kazandi = True
            if kazandi:
                xp += r["xp"]
                kazanilan.append(r)

        sev_ad, sev_ikon, sev_pct, kalan = _seviye_bilgi(xp)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,#c9a84c15);border:2px solid #c9a84c;
            border-radius:20px;padding:24px;text-align:center;">
            <div style="font-size:3rem;">{sev_ikon}</div>
            <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">{sec}</div>
            <div style="color:#c9a84c;font-weight:800;">{sev_ad}</div>
            <div style="color:#c9a84c;font-weight:900;font-size:2rem;margin-top:6px;">{xp} XP</div>
            <div style="background:#1e293b;border-radius:6px;height:12px;margin:10px 20px;overflow:hidden;">
                <div style="width:{sev_pct}%;height:100%;background:#c9a84c;border-radius:6px;"></div>
            </div>
            <div style="color:#64748b;font-size:0.7rem;">{kalan} XP kaldi | {len(kazanilan)} rozet | {toplam_sure} dk | {kategori_say} kategori</div>
        </div>""", unsafe_allow_html=True)

        if kazanilan:
            styled_section("Rozetlerim")
            cols = st.columns(min(len(kazanilan), 4))
            for i, r in enumerate(kazanilan):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div style="background:#0f172a;border:2px solid {r['renk']};border-radius:14px;
                        padding:10px;text-align:center;margin:3px 0;">
                        <div style="font-size:1.5rem;">{r['ikon']}</div>
                        <div style="color:{r['renk']};font-weight:800;font-size:0.7rem;">{r['ad']}</div>
                    </div>""", unsafe_allow_html=True)

    # ── LİDERLİK ──
    with sub[1]:
        styled_section("Okul Liderlik Tablosu")
        tum_ogr = set(k.get("ogrenci","") for k in kullanim + tamamlanmalar)
        lider = []
        for ogr in tum_ogr:
            if not ogr: continue
            kull = sum(1 for k in kullanim if k.get("ogrenci") == ogr)
            tam = sum(1 for t in tamamlanmalar if t.get("ogrenci") == ogr)
            xp_s = kull * 3 + tam * 8
            lider.append({"ad": ogr, "xp": xp_s, "aktivite": kull + tam})

        lider.sort(key=lambda x: x["xp"], reverse=True)

        if not lider:
            st.info("Liderlik verisi yok.")
        else:
            for sira, l in enumerate(lider[:20], 1):
                _, s_ikon, _, _ = _seviye_bilgi(l["xp"])
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                renk = "#c9a84c" if sira <= 3 else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{l['ad']}</span>
                    <span style="font-size:0.75rem;">{s_ikon}</span>
                    <span style="color:#c9a84c;font-weight:800;">{l['xp']} XP</span>
                </div>""", unsafe_allow_html=True)

    # ── ROZET VİTRİNİ ──
    with sub[2]:
        styled_section("Tum Rozetler")
        cols = st.columns(3)
        for i, r in enumerate(_ROZETLER):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {r['renk']}30;border-radius:14px;
                    padding:12px;text-align:center;margin:4px 0;">
                    <div style="font-size:1.8rem;">{r['ikon']}</div>
                    <div style="color:{r['renk']};font-weight:800;font-size:0.75rem;margin-top:3px;">{r['ad']}</div>
                    <div style="color:#c9a84c;font-size:0.68rem;font-weight:700;margin-top:3px;">+{r['xp']} XP</div>
                </div>""", unsafe_allow_html=True)

    # ── XP TABLOSU ──
    with sub[3]:
        styled_section("Aktivite XP Tablosu")
        for akt, puan in sorted(_XP_AKTIVITE.items(), key=lambda x: x[1], reverse=True):
            bar_w = round(puan / 12 * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                <span style="min-width:150px;font-size:0.8rem;color:#e2e8f0;font-weight:600;">{akt}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#c9a84c;border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">+{puan}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        styled_section("Seviye Tablosu")
        for (lo, hi), (ad, ikon) in _SEVIYELER.items():
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 0;">
                <span style="font-size:1.2rem;">{ikon}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;min-width:80px;">{ad}</span>
                <span style="color:#64748b;font-size:0.72rem;">{lo} — {hi} XP</span>
            </div>""", unsafe_allow_html=True)
