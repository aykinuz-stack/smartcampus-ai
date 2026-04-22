"""
Sosyal Etkinlik ve Kulüpler — Süper Özellikler
================================================
1. Turnuva & Yarışma Yönetim Merkezi
2. Etkinlik Galeri & Dijital Arşiv Sistemi
3. AI Etkinlik Planlama Asistanı & Trend Analizi
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _sd():
    d = os.path.join(get_tenant_dir(), "sosyal_etkinlik"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_sd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_sd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}

_TURNUVA_TURLERI = [
    "Futbol", "Basketbol", "Voleybol", "Masa Tenisi", "Satranc", "Badminton",
    "Bilgi Yarismasi", "Munazara", "Resim Yarismasi", "Siir Okuma",
    "Matematik Olimpiyadi", "Fen Olimpiyadi", "Robotik Yarisma",
    "Kodlama Yarismasi", "Kompozisyon", "Muzik / Koro", "Tiyatro", "Diger",
]
_TURNUVA_KAPSAMLARI = ["Okul Ici", "Ilce", "Il", "Bolge", "Turkiye", "Uluslararasi"]
_TURNUVA_DURUMLARI = ["Planlandi", "Devam Ediyor", "Tamamlandi", "Ertelendi", "Iptal"]
_TURNUVA_DURUM_RENK = {"Planlandi": "#3b82f6", "Devam Ediyor": "#f59e0b", "Tamamlandi": "#10b981", "Ertelendi": "#94a3b8", "Iptal": "#ef4444"}

_ETKINLIK_TIPLERI = ["Kermes", "Konser", "Sergi", "Gösteri", "Tiyatro", "Bilim Fuari",
    "Mezuniyet Toreni", "Kutlama / Anma", "Gezi", "Kamp", "Seminer", "Panel", "Diger"]

_MEMNUNIYET_SORULARI = [
    "Etkinlik beklentilerimi karsiladi",
    "Organizasyon basarili idi",
    "Tekrar katilmak isterim",
    "Arkadaslarima tavsiye ederim",
]


# ════════════════════════════════════════════════════════════
# 1. TURNUVA & YARIŞMA YÖNETİM MERKEZİ
# ════════════════════════════════════════════════════════════

def render_turnuva_merkezi(store):
    """Turnuva & Yarışma Yönetim Merkezi — fikstür, puan tablosu, ödül arşivi."""
    styled_section("Turnuva & Yarisma Yonetim Merkezi", "#c9a84c")
    styled_info_banner(
        "Okul ici/disi turnuvalar, yarisma takvimi, takim olusturma, "
        "fikstur/puan tablosu, odul arsivi, sertifika olusturma.",
        banner_type="info", icon="🏅")

    turnuvalar = _lj("turnuvalar.json")
    sonuclar = _lj("turnuva_sonuclari.json")
    oduller = _lj("odul_arsivi.json")

    # KPI
    tamamlanan = sum(1 for t in turnuvalar if t.get("durum") == "Tamamlandi")
    aktif = sum(1 for t in turnuvalar if t.get("durum") in ("Planlandi", "Devam Ediyor"))
    toplam_odul = len(oduller)
    ilce_derece = sum(1 for o in oduller if o.get("kapsam") in ("Ilce", "Il", "Bolge", "Turkiye"))

    styled_stat_row([
        ("Toplam Turnuva", str(len(turnuvalar)), "#c9a84c", "🏆"),
        ("Aktif", str(aktif), "#3b82f6", "🔵"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
        ("Odul/Derece", str(toplam_odul), "#f59e0b", "🥇"),
        ("Dis Derece", str(ilce_derece), "#8b5cf6", "🌟"),
    ])

    sub = st.tabs(["➕ Yeni Turnuva", "📋 Turnuva Listesi", "🏆 Puan Tablosu", "🥇 Odul Arsivi", "📜 Sertifika"])

    # ── YENİ TURNUVA ──
    with sub[0]:
        styled_section("Yeni Turnuva / Yarisma Olustur")
        with st.form("turnuva_form"):
            c1, c2 = st.columns(2)
            with c1:
                t_ad = st.text_input("Turnuva Adi", placeholder="2026 Okul Ici Satranc Turnuvasi", key="tr_ad")
                t_tur = st.selectbox("Tur", _TURNUVA_TURLERI, key="tr_tur")
                t_kapsam = st.selectbox("Kapsam", _TURNUVA_KAPSAMLARI, key="tr_kapsam")
            with c2:
                t_tarih = st.date_input("Baslangic", key="tr_tarih")
                t_bitis = st.date_input("Bitis", key="tr_bitis")
                t_konum = st.text_input("Konum", key="tr_konum")
            t_aciklama = st.text_area("Aciklama / Kurallar", height=60, key="tr_acik")
            t_takimlar = st.text_area("Takimlar / Katilimcilar (her satira bir)", height=60, key="tr_takim")

            if st.form_submit_button("Turnuva Olustur", use_container_width=True, type="primary"):
                if t_ad:
                    takimlar = [t.strip() for t in t_takimlar.split("\n") if t.strip()]
                    kayit = {
                        "id": f"tr_{uuid.uuid4().hex[:8]}",
                        "ad": t_ad, "tur": t_tur, "kapsam": t_kapsam,
                        "tarih": t_tarih.isoformat(), "bitis": t_bitis.isoformat(),
                        "konum": t_konum, "aciklama": t_aciklama,
                        "takimlar": takimlar, "durum": "Planlandi",
                        "created_at": datetime.now().isoformat(),
                    }
                    turnuvalar.append(kayit)
                    _sj("turnuvalar.json", turnuvalar)
                    st.success(f"'{t_ad}' turnuvasi olusturuldu! ({len(takimlar)} takim)")
                    st.rerun()

    # ── TURNUVA LİSTESİ ──
    with sub[1]:
        styled_section("Turnuva & Yarisma Listesi")
        if not turnuvalar:
            st.info("Henuz turnuva yok.")
        else:
            for t in sorted(turnuvalar, key=lambda x: x.get("tarih",""), reverse=True):
                d_renk = _TURNUVA_DURUM_RENK.get(t.get("durum",""), "#94a3b8")
                kapsam_badge = "🌍" if t.get("kapsam") in ("Turkiye","Uluslararasi") else "🏫" if t.get("kapsam") == "Okul Ici" else "🏛️"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {d_renk}30;border-left:5px solid {d_renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🏆 {t.get('ad','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:3px 10px;border-radius:8px;
                            font-size:0.7rem;font-weight:700;">{t.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        {kapsam_badge} {t.get('kapsam','')} | {t.get('tur','')} | {t.get('tarih','')[:10]} — {t.get('bitis','')[:10]}
                        | {len(t.get('takimlar',[]))} takim</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {t.get('id','')}", expanded=False):
                    yeni_durum = st.selectbox("Durum", _TURNUVA_DURUMLARI,
                        index=_TURNUVA_DURUMLARI.index(t.get("durum","Planlandi")) if t.get("durum") in _TURNUVA_DURUMLARI else 0,
                        key=f"tr_d_{t['id']}")
                    if st.button("Guncelle", key=f"tr_g_{t['id']}"):
                        t["durum"] = yeni_durum
                        _sj("turnuvalar.json", turnuvalar)
                        st.rerun()

    # ── PUAN TABLOSU ──
    with sub[2]:
        styled_section("Turnuva Sonuc & Puan Tablosu")
        with st.form("sonuc_form"):
            c1, c2 = st.columns(2)
            with c1:
                if turnuvalar:
                    s_turnuva = st.selectbox("Turnuva", [t.get("ad","") for t in turnuvalar], key="sn_tr")
                else:
                    s_turnuva = st.text_input("Turnuva", key="sn_tr")
                s_takim = st.text_input("Takim / Ogrenci", key="sn_takim")
            with c2:
                s_siralama = st.number_input("Siralama", min_value=1, value=1, key="sn_sira")
                s_puan = st.number_input("Puan", min_value=0, value=100, key="sn_puan")

            if st.form_submit_button("Sonuc Kaydet", use_container_width=True):
                if s_takim:
                    sonuclar.append({
                        "id": f"sn_{uuid.uuid4().hex[:8]}",
                        "turnuva": s_turnuva, "takim": s_takim,
                        "siralama": s_siralama, "puan": s_puan,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("turnuva_sonuclari.json", sonuclar)
                    st.success(f"{s_takim}: {s_siralama}. sirada!")
                    st.rerun()

        if sonuclar:
            # Turnuva bazli grupla
            tr_grp = defaultdict(list)
            for s in sonuclar:
                tr_grp[s.get("turnuva","?")].append(s)

            for tr_ad, tr_sonuc in tr_grp.items():
                styled_section(f"🏆 {tr_ad}")
                sirali = sorted(tr_sonuc, key=lambda x: x.get("siralama", 99))
                for s in sirali:
                    sira = s.get("siralama", 0)
                    madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                    renk = "#c9a84c" if sira <= 3 else "#94a3b8"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                        background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                        <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{s.get('takim','')}</span>
                        <span style="color:#c9a84c;font-weight:800;">{s.get('puan','')} puan</span>
                    </div>""", unsafe_allow_html=True)

    # ── ÖDÜL ARŞİVİ ──
    with sub[3]:
        styled_section("Odul & Derece Arsivi")
        with st.form("odul_form"):
            c1, c2 = st.columns(2)
            with c1:
                o_ogr = st.text_input("Ogrenci / Takim", key="od_ogr")
                o_yarisma = st.text_input("Yarisma Adi", key="od_yar")
            with c2:
                o_derece = st.selectbox("Derece", ["1. (Birincilik)", "2. (Ikincilik)", "3. (Ucunculuk)",
                    "Mansiyon", "Ozel Odul", "Katilim"], key="od_der")
                o_kapsam = st.selectbox("Kapsam", _TURNUVA_KAPSAMLARI, key="od_kapsam")
            o_tarih = st.date_input("Tarih", key="od_tarih")

            if st.form_submit_button("Odul Kaydet", use_container_width=True):
                if o_ogr:
                    oduller.append({
                        "id": f"od_{uuid.uuid4().hex[:8]}",
                        "ogrenci": o_ogr, "yarisma": o_yarisma,
                        "derece": o_derece, "kapsam": o_kapsam,
                        "tarih": o_tarih.isoformat(),
                    })
                    _sj("odul_arsivi.json", oduller)
                    st.success(f"🏆 {o_ogr} — {o_derece} kaydedildi!")
                    st.rerun()

        if oduller:
            for o in sorted(oduller, key=lambda x: x.get("tarih",""), reverse=True)[:15]:
                derece_emoji = "🥇" if "1." in o.get("derece","") else "🥈" if "2." in o.get("derece","") else "🥉" if "3." in o.get("derece","") else "🏅"
                kapsam_badge = "🌍" if o.get("kapsam") in ("Turkiye","Uluslararasi") else "🏛️" if o.get("kapsam") in ("Il","Bolge") else "🏫"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                    background:#c9a84c08;border:1px solid #c9a84c30;border-left:4px solid #c9a84c;border-radius:0 10px 10px 0;">
                    <span style="font-size:1.2rem;">{derece_emoji}</span>
                    <div style="flex:1;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{o.get('ogrenci','')}</span>
                        <div style="color:#94a3b8;font-size:0.7rem;">{o.get('yarisma','')} | {kapsam_badge} {o.get('kapsam','')}</div>
                    </div>
                    <span style="color:#c9a84c;font-weight:700;font-size:0.75rem;">{o.get('derece','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── SERTİFİKA ──
    with sub[4]:
        styled_section("Katilim & Basari Sertifikasi")
        if oduller:
            st.caption("Odul alan ogrenciler icin sertifika hazirlama:")
            for o in oduller[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 10px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #c9a84c;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-size:0.78rem;flex:1;">{o.get('ogrenci','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{o.get('yarisma','')}</span>
                    <span style="color:#c9a84c;font-size:0.65rem;">📜 Sertifika Hazir</span>
                </div>""", unsafe_allow_html=True)
            st.caption("Sertifika PDF icin Kurumsal Org > Sertifikalar sekmesini kullanabilirsiniz.")
        else:
            st.info("Odul kaydi yok.")


# ════════════════════════════════════════════════════════════
# 2. ETKİNLİK GALERİ & DİJİTAL ARŞİV SİSTEMİ
# ════════════════════════════════════════════════════════════

def render_etkinlik_galeri(store):
    """Etkinlik Galeri & Dijital Arşiv — fotoğraf, anket, gelir-gider, veli bilgilendirme."""
    styled_section("Etkinlik Galeri & Dijital Arsiv", "#8b5cf6")
    styled_info_banner(
        "Her etkinlige fotograf/video, katilimci memnuniyet anketi, "
        "gelir-gider takibi, yillik dijital arsiv, veli bilgilendirme.",
        banner_type="info", icon="📸")

    arsiv = _lj("etkinlik_arsiv.json")
    anketler = _lj("etkinlik_anketleri.json")
    gelir_gider = _lj("etkinlik_gelir_gider.json")

    etkinlikler = store.load_objects("etkinlikler")

    styled_stat_row([
        ("Arsiv Kaydi", str(len(arsiv)), "#8b5cf6", "📸"),
        ("Anket Yaniti", str(len(anketler)), "#3b82f6", "📝"),
        ("Gelir-Gider", str(len(gelir_gider)), "#10b981", "💰"),
    ])

    sub = st.tabs(["📸 Arsiv Kaydi", "📝 Memnuniyet Anketi", "💰 Gelir-Gider", "📅 Kronolojik Arsiv", "📨 Veli Bildirim"])

    # ── ARŞİV KAYDI ──
    with sub[0]:
        styled_section("Etkinlik Arsiv Kaydi Ekle")
        with st.form("arsiv_form"):
            if etkinlikler:
                a_etkinlik = st.selectbox("Etkinlik",
                    [f"{e.baslik} ({e.tarih_baslangic[:10]})" for e in etkinlikler], key="ar_etk")
            else:
                a_etkinlik = st.text_input("Etkinlik", key="ar_etk")
            a_foto_link = st.text_input("Fotograf/Video Linki (Google Drive, OneDrive, vb.)", key="ar_foto")
            a_aciklama = st.text_area("Aciklama / Onemli Anlar", height=60, key="ar_acik")
            a_katilimci = st.number_input("Katilimci Sayisi", min_value=0, value=50, key="ar_kat")

            if st.form_submit_button("Arsive Ekle", use_container_width=True):
                arsiv.append({
                    "id": f"ar_{uuid.uuid4().hex[:8]}",
                    "etkinlik": a_etkinlik,
                    "foto_link": a_foto_link,
                    "aciklama": a_aciklama,
                    "katilimci": a_katilimci,
                    "tarih": datetime.now().isoformat(),
                })
                _sj("etkinlik_arsiv.json", arsiv)
                st.success("Arsive eklendi!")
                st.rerun()

    # ── MEMNUNİYET ANKETİ ──
    with sub[1]:
        styled_section("Katilimci Memnuniyet Anketi")
        with st.form("anket_form"):
            if etkinlikler:
                an_etkinlik = st.selectbox("Etkinlik",
                    [f"{e.baslik}" for e in etkinlikler], key="an_etk")
            else:
                an_etkinlik = st.text_input("Etkinlik", key="an_etk")
            an_ad = st.text_input("Katilimci Adi", key="an_ad")

            puanlar = {}
            for soru in _MEMNUNIYET_SORULARI:
                puanlar[soru] = st.select_slider(soru,
                    options=["Kesinlikle Hayir (1)", "Hayir (2)", "Kararsiz (3)", "Evet (4)", "Kesinlikle Evet (5)"],
                    key=f"an_{soru[:15]}")

            an_yorum = st.text_area("Acik Yorum", height=40, key="an_yorum")

            if st.form_submit_button("Anketi Gonder", use_container_width=True):
                puan_map = {"Kesinlikle Hayir (1)": 1, "Hayir (2)": 2, "Kararsiz (3)": 3, "Evet (4)": 4, "Kesinlikle Evet (5)": 5}
                sayisal = {s: puan_map.get(p, 3) for s, p in puanlar.items()}
                ort = round(sum(sayisal.values()) / max(len(sayisal), 1), 1)
                anketler.append({
                    "etkinlik": an_etkinlik, "katilimci": an_ad,
                    "puanlar": sayisal, "ortalama": ort, "yorum": an_yorum,
                    "tarih": datetime.now().isoformat(),
                })
                _sj("etkinlik_anketleri.json", anketler)
                st.success(f"Memnuniyet: {ort}/5")

        # Ozet
        if anketler:
            styled_section("Anket Sonuclari Ozet")
            etk_grp = defaultdict(list)
            for a in anketler:
                etk_grp[a.get("etkinlik","?")].append(a.get("ortalama", 3))

            for etk, puanlar_l in sorted(etk_grp.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
                ort = round(sum(puanlar_l) / max(len(puanlar_l), 1), 1)
                renk = "#10b981" if ort >= 4 else "#f59e0b" if ort >= 3 else "#ef4444"
                pct = round(ort / 5 * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                    <span style="min-width:180px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{etk[:35]}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{ort}/5</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(puanlar_l)} yanit</span>
                </div>""", unsafe_allow_html=True)

    # ── GELİR-GİDER ──
    with sub[2]:
        styled_section("Etkinlik Gelir-Gider Takibi")
        with st.form("gg_form"):
            c1, c2 = st.columns(2)
            with c1:
                gg_etkinlik = st.text_input("Etkinlik", placeholder="Kermes, Konser...", key="gg_etk")
                gg_tip = st.selectbox("Tip", ["Gelir", "Gider"], key="gg_tip")
            with c2:
                gg_tutar = st.number_input("Tutar (TL)", min_value=0.0, value=0.0, step=100.0, key="gg_tutar")
                gg_kalem = st.text_input("Kalem", placeholder="Bilet satisi, yemek, ulasim...", key="gg_kalem")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if gg_etkinlik:
                    gelir_gider.append({
                        "etkinlik": gg_etkinlik, "tip": gg_tip,
                        "tutar": gg_tutar, "kalem": gg_kalem,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("etkinlik_gelir_gider.json", gelir_gider)
                    st.success(f"{gg_tip}: {gg_tutar:,.0f} TL")
                    st.rerun()

        if gelir_gider:
            toplam_gelir = sum(g.get("tutar",0) for g in gelir_gider if g.get("tip") == "Gelir")
            toplam_gider = sum(g.get("tutar",0) for g in gelir_gider if g.get("tip") == "Gider")
            kar = toplam_gelir - toplam_gider
            renk = "#10b981" if kar >= 0 else "#ef4444"

            styled_stat_row([
                ("Gelir", f"{toplam_gelir:,.0f} TL", "#10b981", "💵"),
                ("Gider", f"{toplam_gider:,.0f} TL", "#ef4444", "💳"),
                ("Net", f"{kar:,.0f} TL", renk, "📊"),
            ])

    # ── KRONOLOJİK ARŞİV ──
    with sub[3]:
        styled_section("Yillik Etkinlik Arsivi")
        if not arsiv:
            st.info("Arsiv kaydi yok.")
        else:
            for a in sorted(arsiv, key=lambda x: x.get("tarih",""), reverse=True):
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #8b5cf6;border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">📸 {a.get('etkinlik','')[:40]}</span>
                        <span style="color:#64748b;font-size:0.68rem;">{a.get('tarih','')[:10]}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {a.get('aciklama','')[:80]} | {a.get('katilimci',0)} katilimci</div>
                    {f"<div style='color:#8b5cf6;font-size:0.68rem;margin-top:2px;'>🔗 {a.get('foto_link','')[:50]}</div>" if a.get('foto_link') else ''}
                </div>""", unsafe_allow_html=True)

    # ── VELİ BİLDİRİM ──
    with sub[4]:
        styled_section("Veli Bilgilendirme")
        st.caption("Etkinlik sonrasi velilere otomatik bildirim gonderin.")
        if etkinlikler:
            tamamlanan = [e for e in etkinlikler if e.durum == "TAMAMLANDI"]
            if tamamlanan:
                for e in tamamlanan[:5]:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                        background:#8b5cf610;border:1px solid #8b5cf630;border-radius:10px;">
                        <span style="color:#e2e8f0;font-size:0.78rem;flex:1;">📨 {e.baslik}</span>
                        <span style="color:#8b5cf6;font-size:0.68rem;">Bildirim Gonder</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Tamamlanan etkinlik yok.")
        else:
            st.info("Etkinlik yok.")


# ════════════════════════════════════════════════════════════
# 3. AI ETKİNLİK PLANLAMA ASİSTANI & TREND ANALİZİ
# ════════════════════════════════════════════════════════════

_MEVSIM_ETKINLIK = {
    "Eylul": ["Tanis Etkinligi", "Kulup Kayit Fuari", "Hosbulduk Pikniği"],
    "Ekim": ["29 Ekim Kutlamasi", "Sonbahar Gezisi", "Bilim Haftasi"],
    "Kasim": ["10 Kasim Anma", "Kitap Fuari", "Satranc Turnuvasi"],
    "Aralik": ["Yeni Yil Kermesi", "Kis Konseri", "Kodlama Haftasi"],
    "Ocak": ["Yariyil Kapanisi", "Karne Gunu Etkinligi"],
    "Subat": ["2. Donem Acilis", "Deger Egitimi Haftasi"],
    "Mart": ["Bahar Senligi", "Bilim Fuari", "Pi Gunu"],
    "Nisan": ["23 Nisan Kutlamasi", "Dunya Kitap Gunu", "Sanat Sergisi"],
    "Mayis": ["19 Mayis Kutlamasi", "Anneler Gunu", "Spor Senligi"],
    "Haziran": ["Mezuniyet Toreni", "Yil Sonu Gosterisi", "Odul Toreni"],
}


def render_ai_etkinlik_planlama(store):
    """AI Etkinlik Planlama Asistanı & Trend Analizi."""
    styled_section("AI Etkinlik Planlama Asistani & Trend Analizi", "#059669")
    styled_info_banner(
        "Gecmis verilerden AI ile etkinlik onerisi, mevsimsel harita, "
        "kademe bazli ilgi analizi, butce optimizasyonu.",
        banner_type="info", icon="🤖")

    etkinlikler = store.load_objects("etkinlikler")
    anketler = _lj("etkinlik_anketleri.json")
    butce = _lj("etkinlik_butce.json")

    sub = st.tabs(["💡 AI Oneriler", "📊 Trend Analizi", "📅 Mevsimsel Harita", "⚖️ Karsilastirma"])

    # ── AI ÖNERİLER ──
    with sub[0]:
        styled_section("AI Etkinlik Onerileri")

        # Kategori bazli analiz
        kat_say = Counter()
        kat_katilim = defaultdict(list)
        for e in etkinlikler:
            kat_say[e.kategori] += 1

        # Anket bazli memnuniyet
        etk_memn = defaultdict(list)
        for a in anketler:
            etk_memn[a.get("etkinlik","?")].append(a.get("ortalama", 3))

        # Oneriler uret
        oneriler = []

        # En populer kategori
        if kat_say:
            en_populer = kat_say.most_common(1)[0]
            oneriler.append(("🌟 En Populer", f"'{en_populer[0]}' kategorisi {en_populer[1]} etkinlikle en cok tercih edilen. Devam edin!", "#10b981"))

        # En az etkinlik yapilan kategori
        if kat_say:
            en_az = kat_say.most_common()[-1]
            oneriler.append(("📌 Firsat", f"'{en_az[0]}' kategorisinde sadece {en_az[1]} etkinlik — cesitlendirme oneririz.", "#f59e0b"))

        # Mevsimsel oneri
        bugun = date.today()
        ay = bugun.strftime("%B")
        mevsim_oner = _MEVSIM_ETKINLIK.get(ay, [])
        if mevsim_oner:
            oneriler.append(("📅 Mevsimsel", f"{ay} icin onerileler: {', '.join(mevsim_oner)}", "#3b82f6"))

        # Memnuniyet bazli
        if etk_memn:
            en_begeni = max(etk_memn.items(), key=lambda x: sum(x[1])/len(x[1]))
            ort = round(sum(en_begeni[1])/len(en_begeni[1]), 1)
            oneriler.append(("⭐ En Begenilen", f"'{en_begeni[0]}' ({ort}/5 memnuniyet) — tekrar planlayin!", "#c9a84c"))

        if not oneriler:
            st.info("Oneri icin daha fazla etkinlik verisi gerekli.")
        else:
            for baslik, mesaj, renk in oneriler:
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:6px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.82rem;">{baslik}</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:3px;">{mesaj}</div>
                </div>""", unsafe_allow_html=True)

    # ── TREND ANALİZİ ──
    with sub[1]:
        styled_section("Etkinlik Trendi")
        if not etkinlikler:
            st.info("Veri yok.")
        else:
            # Aylik dagilim
            ay_say = Counter()
            for e in etkinlikler:
                ay = e.tarih_baslangic[:7] if e.tarih_baslangic else ""
                if ay:
                    ay_say[ay] += 1

            if ay_say:
                max_val = max(ay_say.values())
                for ay in sorted(ay_say.keys())[-12:]:
                    sayi = ay_say[ay]
                    pct = round(sayi / max(max_val, 1) * 100)
                    renk = "#10b981" if sayi >= 3 else "#f59e0b" if sayi >= 1 else "#94a3b8"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:55px;font-size:0.72rem;color:#94a3b8;">{ay}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

            # Kategori dagilimi
            styled_section("Kategori Dagilimi")
            if kat_say:
                toplam = max(sum(kat_say.values()), 1)
                for kat, sayi in kat_say.most_common():
                    pct = round(sayi / toplam * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                        <span style="min-width:140px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{kat}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:#8b5cf6;border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi} (%{pct})</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── MEVSIMSEL HARİTA ──
    with sub[2]:
        styled_section("Mevsimsel Etkinlik Haritasi")
        for ay_adi, etk_list in _MEVSIM_ETKINLIK.items():
            is_bu_ay = ay_adi == date.today().strftime("%B")
            renk = "#c9a84c" if is_bu_ay else "#334155"
            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                padding:8px 14px;margin:4px 0;{'border:1px solid #c9a84c;' if is_bu_ay else ''}">
                <span style="color:{'#c9a84c' if is_bu_ay else '#e2e8f0'};font-weight:{'900' if is_bu_ay else '600'};
                    font-size:0.85rem;">{'📌 ' if is_bu_ay else ''}{ay_adi}</span>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">{', '.join(etk_list)}</div>
            </div>""", unsafe_allow_html=True)

    # ── KARŞILAŞTIRMA ──
    with sub[3]:
        styled_section("Donem Karsilastirmasi")
        if len(etkinlikler) >= 2:
            bu_donem = sum(1 for e in etkinlikler if e.tarih_baslangic[:4] == str(date.today().year))
            gecen_donem = sum(1 for e in etkinlikler if e.tarih_baslangic[:4] == str(date.today().year - 1))
            fark = bu_donem - gecen_donem
            renk = "#10b981" if fark > 0 else "#ef4444" if fark < 0 else "#94a3b8"

            st.markdown(f"""
            <div style="display:flex;gap:16px;margin:14px 0;">
                <div style="flex:1;background:#0f172a;border:1px solid #334155;border-radius:16px;padding:16px;text-align:center;">
                    <div style="color:#94a3b8;font-size:0.75rem;">Gecen Yil</div>
                    <div style="color:#3b82f6;font-weight:900;font-size:2rem;">{gecen_donem}</div>
                </div>
                <div style="flex:1;background:#0f172a;border:2px solid {renk};border-radius:16px;padding:16px;text-align:center;">
                    <div style="color:#94a3b8;font-size:0.75rem;">Bu Yil</div>
                    <div style="color:{renk};font-weight:900;font-size:2rem;">{bu_donem}</div>
                </div>
            </div>
            <div style="text-align:center;color:{renk};font-weight:700;">
                {'+' if fark > 0 else ''}{fark} etkinlik farki</div>""", unsafe_allow_html=True)
        else:
            st.info("Karsilastirma icin en az 2 donem verisi gerekli.")
