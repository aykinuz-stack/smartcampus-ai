"""
AI Treni (Bilgi Treni) — Süper Özellikler
============================================
1. Tren Yolculuğu Haritası & İstasyon Sistemi
2. Vagon Yarışı & Sınıflar Arası Turnuva
3. AI Adaptif İçerik Motoru & Günlük Görev
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
    d = os.path.join(get_tenant_dir(), "bilgi_treni"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_ISTASYONLAR = {
    "Matematik": {"ikon": "🧮", "renk": "#3b82f6", "duraklar": ["Sayilar","Islemler","Cebir","Geometri","Olasilik","Veri"]},
    "Turkce": {"ikon": "📖", "renk": "#8b5cf6", "duraklar": ["Dil Bilgisi","Paragraf","Anlama","Yazma","Sozcuk","Metin Turu"]},
    "Fen": {"ikon": "🔬", "renk": "#10b981", "duraklar": ["Fizik","Kimya","Biyoloji","Yer Bilimi","Astronomi"]},
    "Sosyal": {"ikon": "🌍", "renk": "#f59e0b", "duraklar": ["Tarih","Cografya","Vatandaslik","Ekonomi"]},
    "Ingilizce": {"ikon": "🇬🇧", "renk": "#ef4444", "duraklar": ["Grammar","Vocabulary","Reading","Listening","Writing"]},
    "Genel Kultur": {"ikon": "💡", "renk": "#059669", "duraklar": ["Bilim","Sanat","Spor","Doga","Teknoloji"]},
}

_GUNLUK_GOREVLER = [
    {"ad": "Fen Kasifi", "ikon": "🔬", "gorev": "1 Fen quizi coz", "xp": 10, "ders": "Fen"},
    {"ad": "Matematik Savascisi", "ikon": "🧮", "gorev": "1 Matematik oyunu oyna", "xp": 10, "ders": "Matematik"},
    {"ad": "Kultur Gezgini", "ikon": "💡", "gorev": "1 Genel Kultur oku", "xp": 8, "ders": "Genel Kultur"},
    {"ad": "Kelime Avcisi", "ikon": "🇬🇧", "gorev": "5 Ingilizce kelime ogren", "xp": 8, "ders": "Ingilizce"},
    {"ad": "Tarih Yolcusu", "ikon": "🌍", "gorev": "1 Tarihte Bugun oku", "xp": 6, "ders": "Sosyal"},
    {"ad": "Edebiyat Okuru", "ikon": "📖", "gorev": "1 siir veya roman ozeti oku", "xp": 8, "ders": "Turkce"},
    {"ad": "Beyin Jimnastigi", "ikon": "🧠", "gorev": "1 hafiza oyunu oyna", "xp": 6, "ders": "Genel"},
]

_ZORLUK_SEVIYELERI = ["Kolay", "Orta", "Zor", "Uzman"]


# ════════════════════════════════════════════════════════════
# 1. TREN YOLCULUĞU HARİTASI & İSTASYON SİSTEMİ
# ════════════════════════════════════════════════════════════

def render_yolculuk_haritasi():
    """Tren Yolculuğu Haritası — istasyon, durak, ilerleme, sertifika."""
    styled_section("Tren Yolculugu Haritasi & Istasyon Sistemi", "#6366f1")
    styled_info_banner(
        "Her ders bir istasyon, her konu bir durak. Duraklari tamamladikca ilerle! "
        "Gorsel harita, tamamlama yuzdesi, yil sonu sertifika.",
        banner_type="info", icon="🗺️")

    ilerleme = _lj("tren_ilerleme.json")

    sub = st.tabs(["🗺️ Harita", "👤 Bireysel Ilerleme", "📊 Istasyon Ozeti", "🏅 Sertifika"])

    with sub[0]:
        styled_section("Tren Guzergah Haritasi")
        for istasyon, info in _ISTASYONLAR.items():
            durak_say = len(info["duraklar"])
            # Tamamlanan durak say
            tamamlanan = sum(1 for il in ilerleme if il.get("istasyon") == istasyon and il.get("tamamlandi"))
            pct = round(tamamlanan / max(durak_say, 1) * 100)
            renk = "#10b981" if pct >= 80 else "#f59e0b" if pct >= 40 else "#3b82f6" if pct > 0 else "#334155"

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid {renk};border-left:6px solid {info['renk']};
                border-radius:0 16px 16px 0;padding:14px 18px;margin:8px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:900;font-size:1rem;">
                        {info['ikon']} {istasyon} Istasyonu</span>
                    <span style="color:{renk};font-weight:800;font-size:0.85rem;">%{pct}</span>
                </div>
                <div style="background:#1e293b;border-radius:6px;height:10px;margin:8px 0;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;"></div>
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px;">""", unsafe_allow_html=True)

            # Duraklar
            durak_html = ""
            for d_idx, durak in enumerate(info["duraklar"]):
                d_tamamlandi = any(il.get("istasyon") == istasyon and il.get("durak") == durak and il.get("tamamlandi") for il in ilerleme)
                d_renk = "#10b981" if d_tamamlandi else "#334155"
                d_ikon = "✅" if d_tamamlandi else f"🔵" if d_idx == tamamlanan else "⬜"
                durak_html += f'<span style="background:{d_renk}20;color:{d_renk};padding:3px 8px;border-radius:6px;font-size:0.65rem;font-weight:700;border:1px solid {d_renk}40;">{d_ikon} {durak}</span>'

            st.markdown(f"""{durak_html}</div></div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Bireysel Durak Tamamlama")
        ogr_ad = st.text_input("Ogrenci Adi", key="yh_ogr")
        if ogr_ad:
            ist_sec = st.selectbox("Istasyon", list(_ISTASYONLAR.keys()), key="yh_ist")
            duraklar = _ISTASYONLAR[ist_sec]["duraklar"]
            durak_sec = st.selectbox("Durak", duraklar, key="yh_durak")

            if st.button("Duragi Tamamla ✅", use_container_width=True, type="primary"):
                ilerleme.append({
                    "ogrenci": ogr_ad, "istasyon": ist_sec,
                    "durak": durak_sec, "tamamlandi": True,
                    "tarih": datetime.now().isoformat(),
                })
                _sj("tren_ilerleme.json", ilerleme)
                st.success(f"🚂 {ist_sec} > {durak_sec} duragi tamamlandi!")
                st.rerun()

    with sub[2]:
        styled_section("Istasyon Bazli Ozet")
        toplam_durak = sum(len(info["duraklar"]) for info in _ISTASYONLAR.values())
        tamamlanan_toplam = len(set((il.get("istasyon",""), il.get("durak","")) for il in ilerleme if il.get("tamamlandi")))
        genel_pct = round(tamamlanan_toplam / max(toplam_durak, 1) * 100)

        styled_stat_row([
            ("Toplam Durak", str(toplam_durak), "#6366f1", "🚏"),
            ("Tamamlanan", str(tamamlanan_toplam), "#10b981", "✅"),
            ("Ilerleme", f"%{genel_pct}", "#10b981" if genel_pct >= 70 else "#f59e0b", "📊"),
        ])

    with sub[3]:
        styled_section("Yolculuk Tamamlama Sertifikasi")
        if tamamlanan_toplam >= toplam_durak * 0.8:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#c9a84c10,#c9a84c05);border:3px solid #c9a84c;
                border-radius:20px;padding:28px;text-align:center;">
                <div style="font-size:3rem;">🏆</div>
                <div style="color:#c9a84c;font-weight:900;font-size:1.2rem;margin-top:8px;">Tren Yolculugu Sertifikasi</div>
                <div style="color:#e2e8f0;font-size:0.85rem;margin-top:6px;">
                    {tamamlanan_toplam}/{toplam_durak} durak tamamlandi (%{genel_pct})</div>
            </div>""", unsafe_allow_html=True)
        else:
            kalan = toplam_durak - tamamlanan_toplam
            st.info(f"Sertifika icin {kalan} durak daha tamamlanmali (%80 esik).")


# ════════════════════════════════════════════════════════════
# 2. VAGON YARIŞI & SINIFLAR ARASI TURNUVA
# ════════════════════════════════════════════════════════════

def render_vagon_yarisi():
    """Vagon Yarışı — sınıflar arası haftalık bilgi yarışması, skor tablosu."""
    styled_section("Vagon Yarisi & Siniflar Arasi Turnuva", "#c9a84c")
    styled_info_banner(
        "Siniflar (vagonlar) arasi haftalik bilgi yarismasi. "
        "Canli skor tablosu, sampiyon vagon rozeti, bilgi analizi.",
        banner_type="info", icon="🏆")

    yarisma_kayitlari = _lj("vagon_yarisi.json")

    sub = st.tabs(["🏆 Skor Tablosu", "➕ Puan Kaydet", "📊 Ders Analizi", "🗓️ Haftalik Sampiyon"])

    with sub[0]:
        styled_section("Vagon (Sinif) Skor Tablosu")
        if not yarisma_kayitlari:
            st.info("Yarisma kaydi yok. 'Puan Kaydet' sekmesinden baslatin.")
        else:
            sinif_puan = defaultdict(lambda: {"xp": 0, "quiz": 0, "katilim": 0})
            for y in yarisma_kayitlari:
                sinif = y.get("sinif", "?")
                sinif_puan[sinif]["xp"] += y.get("xp", 0)
                sinif_puan[sinif]["quiz"] += 1
                sinif_puan[sinif]["katilim"] += y.get("katilimci", 0)

            sirali = sorted(sinif_puan.items(), key=lambda x: x[1]["xp"], reverse=True)

            for sira, (sinif, data) in enumerate(sirali, 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                renk = "#c9a84c" if sira <= 3 else "#94a3b8"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 16px;margin:4px 0;
                    background:#0f172a;border-left:5px solid {renk};border-radius:0 12px 12px 0;
                    {'border:1px solid #c9a84c;' if sira <= 3 else ''}">
                    <span style="font-size:1.3rem;min-width:30px;text-align:center;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:900;font-size:0.95rem;flex:1;">🚃 {sinif}. Sinif Vagonu</span>
                    <span style="color:#c9a84c;font-weight:900;font-size:1rem;">{data['xp']} XP</span>
                    <span style="color:#64748b;font-size:0.65rem;">{data['quiz']} quiz | {data['katilim']} katilimci</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Vagon Puani Kaydet")
        with st.form("vy_form"):
            c1, c2 = st.columns(2)
            with c1:
                v_sinif = st.selectbox("Sinif (Vagon)", list(range(1, 13)), key="vy_sinif")
                v_ders = st.selectbox("Ders", list(_ISTASYONLAR.keys()), key="vy_ders")
            with c2:
                v_xp = st.number_input("Kazanilan XP", 0, 500, 100, key="vy_xp")
                v_katilimci = st.number_input("Katilimci Sayisi", 1, 40, 25, key="vy_kat")
            v_quiz = st.text_input("Quiz / Yarisma Adi", key="vy_quiz")

            if st.form_submit_button("Puan Kaydet", use_container_width=True, type="primary"):
                yarisma_kayitlari.append({
                    "sinif": v_sinif, "ders": v_ders,
                    "xp": v_xp, "katilimci": v_katilimci,
                    "quiz": v_quiz, "tarih": date.today().isoformat(),
                })
                _sj("vagon_yarisi.json", yarisma_kayitlari)
                st.success(f"🚃 {v_sinif}. Sinif Vagonu: +{v_xp} XP!")
                st.rerun()

    with sub[2]:
        styled_section("Ders Bazli Vagon Analizi")
        if yarisma_kayitlari:
            ders_say = Counter(y.get("ders","") for y in yarisma_kayitlari)
            for ders, sayi in ders_say.most_common():
                info = _ISTASYONLAR.get(ders, {"ikon":"📚","renk":"#94a3b8"})
                pct = round(sayi / max(len(yarisma_kayitlari), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                    <span style="font-size:1rem;">{info['ikon']}</span>
                    <span style="min-width:100px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{info['renk']};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi} quiz</span></div></div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Haftalik Sampiyon Vagon")
        if yarisma_kayitlari:
            bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
            hafta_kayit = [y for y in yarisma_kayitlari if y.get("tarih","") >= bu_hafta]
            if hafta_kayit:
                hafta_sinif = Counter()
                for y in hafta_kayit:
                    hafta_sinif[y.get("sinif",0)] += y.get("xp", 0)
                sampiyon = hafta_sinif.most_common(1)[0]
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#c9a84c10,#c9a84c05);border:3px solid #c9a84c;
                    border-radius:20px;padding:24px;text-align:center;">
                    <div style="font-size:2.5rem;">🏆</div>
                    <div style="color:#c9a84c;font-weight:900;font-size:1.2rem;margin-top:6px;">
                        Bu Haftanin Sampiyonu</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.5rem;margin-top:4px;">
                        🚃 {sampiyon[0]}. Sinif Vagonu — {sampiyon[1]} XP</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("Bu hafta yarisma kaydi yok.")
        else:
            st.info("Yarisma verisi yok.")


# ════════════════════════════════════════════════════════════
# 3. AI ADAPTİF İÇERİK MOTORU & GÜNLÜK GÖREV
# ════════════════════════════════════════════════════════════

def render_adaptif_motor():
    """AI Adaptif İçerik — zorluk ayarlama, günlük görev, kazanım eşleştirme."""
    styled_section("AI Adaptif Icerik Motoru & Gunluk Gorev", "#059669")
    styled_info_banner(
        "Dogru/yanlis gecmisinden zorluk seviyesini otomatik ayarlar. "
        "Gunluk 3 gorev, MEB kazanim eslestirme.",
        banner_type="info", icon="🤖")

    gorev_log = _lj("gunluk_gorev_log.json")
    adaptif_log = _lj("adaptif_log.json")

    bugun = date.today().isoformat()
    bugun_gorev = sum(1 for g in gorev_log if g.get("tarih","")[:10] == bugun)

    styled_stat_row([
        ("Bugun Gorev", f"{bugun_gorev}/3", "#059669" if bugun_gorev >= 3 else "#f59e0b", "✅"),
        ("Toplam Gorev", str(len(gorev_log)), "#3b82f6", "📋"),
        ("Adaptif Kayit", str(len(adaptif_log)), "#8b5cf6", "🤖"),
    ])

    sub = st.tabs(["📋 Gunluk Gorev", "🤖 Adaptif Zorluk", "🎯 Kazanim Eslestir", "📈 Gorev Trend"])

    with sub[0]:
        styled_section("Bugunun 3 Gorevi")
        ogr = st.text_input("Ogrenci Adi", key="gg_ogr")

        # Her gun ayni 3 gorev (seed)
        random.seed(hash(bugun + (ogr or "")))
        gunun = random.sample(_GUNLUK_GOREVLER, min(3, len(_GUNLUK_GOREVLER)))

        tamamlanan = set(g.get("gorev","") for g in gorev_log
            if g.get("ogrenci","") == ogr and g.get("tarih","")[:10] == bugun)

        for g in gunun:
            done = g["ad"] in tamamlanan
            renk = "#10b981" if done else "#f59e0b"
            ikon = "✅" if done else g["ikon"]

            st.markdown(f"""
            <div style="background:#0f172a;border:{'2px solid #10b981' if done else '1px solid #334155'};
                border-left:5px solid {renk};border-radius:0 14px 14px 0;
                padding:12px 16px;margin:6px 0;{'opacity:0.7;' if done else ''}">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">{ikon} {g['ad']}</span>
                    <span style="color:#c9a84c;font-weight:800;">+{g['xp']} XP</span>
                </div>
                <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{g['gorev']}</div>
            </div>""", unsafe_allow_html=True)

            if not done and ogr:
                if st.button(f"Tamamladim! {g['ad']}", key=f"gg_{g['ad']}"):
                    gorev_log.append({
                        "ogrenci": ogr, "gorev": g["ad"],
                        "ders": g["ders"], "xp": g["xp"],
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("gunluk_gorev_log.json", gorev_log)
                    st.success(f"✅ {g['ad']} tamamlandi! +{g['xp']} XP")
                    st.rerun()

        if bugun_gorev >= 3:
            st.markdown(f"""
            <div style="background:#10b98115;border:2px solid #10b981;border-radius:14px;
                padding:14px;text-align:center;margin-top:10px;">
                <span style="color:#10b981;font-weight:900;font-size:1rem;">🎉 Bugunun 3 gorevi tamamlandi!</span>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Adaptif Zorluk Ayarlama")
        st.caption("Dogru/yanlis gecmisinize gore zorluk otomatik ayarlanir.")

        with st.form("adaptif_form"):
            a_ogr = st.text_input("Ogrenci", key="ad_ogr")
            a_ders = st.selectbox("Ders", list(_ISTASYONLAR.keys()), key="ad_ders")
            c1, c2 = st.columns(2)
            with c1:
                a_dogru = st.number_input("Dogru Cevap", 0, 50, 7, key="ad_dogru")
            with c2:
                a_yanlis = st.number_input("Yanlis Cevap", 0, 50, 3, key="ad_yanlis")

            if st.form_submit_button("Zorluk Hesapla", use_container_width=True):
                toplam = a_dogru + a_yanlis
                if toplam > 0:
                    oran = round(a_dogru / toplam * 100)
                    if oran >= 85:
                        seviye = "Uzman"
                        oneri = "Zorluk arttirildi — challenge sorular gelecek!"
                    elif oran >= 65:
                        seviye = "Zor"
                        oneri = "Iyi gidiyorsun — biraz daha zorlayalim."
                    elif oran >= 45:
                        seviye = "Orta"
                        oneri = "Normal seviyede devam — pekistirme gerekli."
                    else:
                        seviye = "Kolay"
                        oneri = "Zorluk dusuruldu — temel konulari tekrar edelim."

                    sev_renk = {"Kolay":"#10b981","Orta":"#f59e0b","Zor":"#ef4444","Uzman":"#8b5cf6"}[seviye]

                    adaptif_log.append({
                        "ogrenci": a_ogr, "ders": a_ders,
                        "dogru": a_dogru, "yanlis": a_yanlis,
                        "oran": oran, "seviye": seviye,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("adaptif_log.json", adaptif_log)

                    st.markdown(f"""
                    <div style="background:{sev_renk}15;border:2px solid {sev_renk};border-radius:16px;
                        padding:16px;text-align:center;margin:10px 0;">
                        <div style="color:{sev_renk};font-weight:900;font-size:1.5rem;">{seviye}</div>
                        <div style="color:#e2e8f0;font-size:0.82rem;margin-top:4px;">
                            Basari: %{oran} ({a_dogru}/{toplam})</div>
                        <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{oneri}</div>
                    </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("MEB Kazanim Eslestirme")
        kazanim_map = {
            "Matematik": ["M.5.1.1 Dogal sayilari okur ve yazar", "M.6.2.3 Cebirsel ifadeler", "M.7.3.1 Oran-orantti"],
            "Turkce": ["T.5.1.1 Dinleme stratejileri", "T.6.2.1 Paragraf analizi", "T.7.3.1 Metin turleri"],
            "Fen": ["F.5.1.1 Madde ve ozellikleri", "F.6.2.1 Kuvvet ve hareket", "F.7.3.1 Isik ve ses"],
            "Sosyal": ["S.5.1.1 Bireysel farkliliklar", "S.6.2.1 Kultur ve miras", "S.7.3.1 Ekonomi"],
        }
        for ders, kazanimlar in kazanim_map.items():
            info = _ISTASYONLAR.get(ders, {"ikon":"📚","renk":"#94a3b8"})
            with st.expander(f"{info['ikon']} {ders} Kazanimlari"):
                for k in kazanimlar:
                    st.markdown(f"  - 🎯 {k}")

    with sub[3]:
        styled_section("Gunluk Gorev Tamamlama Trendi")
        if gorev_log:
            gun_say = Counter(g.get("tarih","")[:10] for g in gorev_log)
            for gun in sorted(gun_say.keys())[-7:]:
                sayi = gun_say[gun]
                is_bugun = gun == bugun
                renk = "#10b981" if sayi >= 3 else "#f59e0b" if sayi >= 1 else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:3px 0;
                    {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bugun else ''}">
                    <span style="min-width:65px;font-size:0.72rem;color:{'#c9a84c' if is_bugun else '#94a3b8'};">{gun[5:]}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{min(sayi*33,100)}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}/3</span></div></div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Gorev verisi yok.")
