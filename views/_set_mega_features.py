"""
Sosyal Etkinlik ve Kulüpler — Mega Özellikler
===============================================
1. Gamifiye Sosyal Katılım & Rozet Sistemi
2. Sosyal Sorumluluk Projeleri & Toplum Hizmeti
3. Etkinlik Otomasyon & Akıllı İş Akışı Motoru
"""
from __future__ import annotations
import json, os, uuid
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

_XP_TABLOSU = {
    (0, 50): ("Yeni Uye", "🟤", "#78716c"),
    (50, 150): ("Aktif", "🥉", "#a8a29e"),
    (150, 300): ("Kaptan", "🥈", "#94a3b8"),
    (300, 500): ("Yildiz", "🥇", "#f59e0b"),
    (500, 800): ("Lider", "👑", "#c9a84c"),
    (800, 99999): ("Efsane", "💎", "#8b5cf6"),
}

_ROZETLER = [
    {"ad": "Ilk Adim", "ikon": "🌱", "kosul": "ilk_katilim", "hedef": 1, "xp": 5, "renk": "#10b981",
     "aciklama": "Ilk kulup faaliyetine katil"},
    {"ad": "Kulup Krali", "ikon": "👑", "kosul": "katilim_20", "hedef": 20, "xp": 30, "renk": "#c9a84c",
     "aciklama": "20 faaliyet katilimi"},
    {"ad": "Cok Yonlu", "ikon": "🌈", "kosul": "kulup_3", "hedef": 3, "xp": 25, "renk": "#6366f1",
     "aciklama": "3 farkli kulupte aktif"},
    {"ad": "Turnuva Sampiyonu", "ikon": "🏆", "kosul": "turnuva_derece", "hedef": 1, "xp": 40, "renk": "#ef4444",
     "aciklama": "Turnuvada derece al"},
    {"ad": "Gonullu Kahraman", "ikon": "🦸", "kosul": "gonullu_10", "hedef": 10, "xp": 35, "renk": "#059669",
     "aciklama": "10 saat gonullu calisma"},
    {"ad": "Sosyal Kelebek", "ikon": "🦋", "kosul": "etkinlik_10", "hedef": 10, "xp": 20, "renk": "#8b5cf6",
     "aciklama": "10 farkli etkinlige katil"},
    {"ad": "Organizator", "ikon": "🎪", "kosul": "organizasyon_3", "hedef": 3, "xp": 30, "renk": "#f59e0b",
     "aciklama": "3 etkinlik organize et"},
    {"ad": "Proje Ustasi", "ikon": "🔨", "kosul": "proje_2", "hedef": 2, "xp": 35, "renk": "#0891b2",
     "aciklama": "2 sosyal sorumluluk projesi tamamla"},
    {"ad": "Takim Oyuncusu", "ikon": "🤝", "kosul": "takim_5", "hedef": 5, "xp": 15, "renk": "#10b981",
     "aciklama": "5 takim etkinligine katil"},
    {"ad": "Sadik Uye", "ikon": "💎", "kosul": "ardisik_8", "hedef": 8, "xp": 25, "renk": "#3b82f6",
     "aciklama": "8 ardisik hafta katilim"},
    {"ad": "Mentor", "ikon": "🧑‍🏫", "kosul": "mentor_3", "hedef": 3, "xp": 30, "renk": "#7c3aed",
     "aciklama": "3 yeni uyeye mentorle"},
    {"ad": "Efsane", "ikon": "💫", "kosul": "xp_500", "hedef": 500, "xp": 50, "renk": "#c9a84c",
     "aciklama": "500 XP topla"},
]

_XP_PUANLARI = {
    "Kulup Katilim": 3, "Etkinlik Katilim": 5, "Turnuva Katilim": 8,
    "Turnuva Derece": 15, "Gonullu Saat": 4, "Proje Katilim": 10,
    "Organizasyon": 12, "Mentor": 8,
}

_PROJE_KATEGORILERI = [
    "Cevre / Dogma", "Egitim Destegi", "Saglik / Hijyen", "Hayvan Haklari",
    "Yasli/Engelli Ziyareti", "Kan Bagisi", "Kitap Toplama", "Gida Yardimi",
    "Teknoloji Okuryazarligi", "Sanat / Kultur", "Diger",
]
_PROJE_DURUMLARI = ["Planlandi", "Devam Ediyor", "Tamamlandi", "Ertelendi"]
_PROJE_DURUM_RENK = {"Planlandi": "#3b82f6", "Devam Ediyor": "#f59e0b", "Tamamlandi": "#10b981", "Ertelendi": "#94a3b8"}

_GOREV_SABLONLARI = {
    "Bilim Fuari": ["Salon ayarla", "Afis hazirla", "Veli bilgilendir", "Juryi belirle", "Odul hazirla", "Fotograf cek", "Rapor yaz", "Anket gonder"],
    "Konser / Gosteri": ["Sahne kur", "Ses sistemi kontrol", "Program hazirla", "Davetiye gonder", "Fotograf/video", "Rapor yaz"],
    "Gezi": ["Otobus ayarla", "Izin formu topla", "Yemek/su planla", "Rehber belirle", "Ilk yardim cantasi", "Rapor yaz"],
    "Turnuva": ["Fikstur hazirla", "Hakem belirle", "Salon/saha ayarla", "Odul siparis", "Sonuc kaydet", "Sertifika hazirla"],
    "Kermes": ["Stant planla", "Malzeme listesi", "Fiyat belirle", "Kasa hazirla", "Temizlik", "Gelir-gider raporu"],
    "Genel": ["Planlama toplantisi", "Gorev dagitimi", "Malzeme temini", "Uygulama", "Degerlendirme", "Rapor"],
}
_GOREV_DURUMLARI = ["Bekliyor", "Devam Ediyor", "Tamamlandi"]
_GOREV_DURUM_RENK = {"Bekliyor": "#f59e0b", "Devam Ediyor": "#3b82f6", "Tamamlandi": "#10b981"}
_ONAY_ADIMLARI = ["Ogretmen", "Mudur Yardimcisi", "Okul Muduru"]


def _seviye(xp):
    for (lo, hi), (ad, ikon, renk) in _XP_TABLOSU.items():
        if lo <= xp < hi:
            pct = round((xp - lo) / max(hi - lo, 1) * 100)
            return ad, ikon, renk, hi, pct
    return "Efsane", "💎", "#8b5cf6", 99999, 100


# ════════════════════════════════════════════════════════════
# 1. GAMİFİYE SOSYAL KATILIM & ROZET SİSTEMİ
# ════════════════════════════════════════════════════════════

def render_gamifiye_sosyal(store):
    """Gamifiye Sosyal Katılım — XP, seviye, rozet, liderlik tablosu."""
    styled_section("Gamifiye Sosyal Katilim & Rozet Sistemi", "#c9a84c")
    styled_info_banner(
        "Kulup katilimi, etkinlik gonullulugu, turnuva basarilari icin XP kazan! "
        "6 seviye, 12 rozet, sinif/okul liderlik tablosu.",
        banner_type="info", icon="🎮")

    katilim = _lj("kulup_katilim.json")
    oduller = _lj("odul_arsivi.json")
    gonullu = _lj("gonullu_saatler.json")

    sub = st.tabs(["👤 Profil Kartim", "🏆 Liderlik", "🎖️ Rozet Vitrini", "📊 XP Tablosu"])

    # ── PROFİL KARTIM ──
    with sub[0]:
        styled_section("Oyuncu Profili")
        students = load_shared_students()
        if not students:
            st.info("Ogrenci yok.")
            return
        ogr_opts = [f"{s.get('ad','')} {s.get('soyad','')}" for s in students]
        sec = st.selectbox("Ogrenci", ogr_opts, key="gm_ogr")

        # XP hesapla
        xp = 0
        ogr_katilim = sum(1 for k in katilim if sec in k.get("katilanlar", []))
        xp += ogr_katilim * _XP_PUANLARI["Kulup Katilim"]

        ogr_odul = sum(1 for o in oduller if sec in o.get("ogrenci", ""))
        xp += ogr_odul * _XP_PUANLARI["Turnuva Derece"]

        ogr_gonullu = sum(g.get("saat", 0) for g in gonullu if g.get("ogrenci") == sec)
        xp += ogr_gonullu * _XP_PUANLARI["Gonullu Saat"]

        # Rozet kontrol
        kazanilan = []
        for r in _ROZETLER:
            kazandi = False
            if r["kosul"] == "ilk_katilim" and ogr_katilim >= 1: kazandi = True
            elif r["kosul"] == "katilim_20" and ogr_katilim >= 20: kazandi = True
            elif r["kosul"] == "turnuva_derece" and ogr_odul >= 1: kazandi = True
            elif r["kosul"] == "gonullu_10" and ogr_gonullu >= 10: kazandi = True
            elif r["kosul"] == "etkinlik_10" and ogr_katilim >= 10: kazandi = True
            elif r["kosul"] == "xp_500" and xp >= 500: kazandi = True
            if kazandi:
                xp += r["xp"]
                kazanilan.append(r)

        sev_ad, sev_ikon, sev_renk, sev_max, sev_pct = _seviye(xp)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,{sev_renk}20);border:2px solid {sev_renk};
            border-radius:20px;padding:24px;text-align:center;">
            <div style="font-size:3rem;">{sev_ikon}</div>
            <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">{sec}</div>
            <div style="color:{sev_renk};font-weight:800;font-size:1rem;">{sev_ad}</div>
            <div style="color:{sev_renk};font-weight:900;font-size:2rem;margin-top:6px;">{xp} XP</div>
            <div style="background:#1e293b;border-radius:6px;height:12px;margin:10px 20px;overflow:hidden;">
                <div style="width:{sev_pct}%;height:100%;background:{sev_renk};border-radius:6px;"></div>
            </div>
            <div style="color:#64748b;font-size:0.7rem;">{len(kazanilan)} rozet | {ogr_katilim} katilim | {ogr_gonullu}h gonullu</div>
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
        students = load_shared_students()
        lider = []
        for s in students[:60]:
            ad = f"{s.get('ad','')} {s.get('soyad','')}"
            xp_s = sum(1 for k in katilim if ad in k.get("katilanlar", [])) * _XP_PUANLARI["Kulup Katilim"]
            xp_s += sum(1 for o in oduller if ad in o.get("ogrenci","")) * _XP_PUANLARI["Turnuva Derece"]
            xp_s += sum(g.get("saat",0) for g in gonullu if g.get("ogrenci") == ad) * _XP_PUANLARI["Gonullu Saat"]
            if xp_s > 0:
                lider.append({"ad": ad, "xp": xp_s, "sinif": f"{s.get('sinif','')}/{s.get('sube','')}"})

        lider.sort(key=lambda x: x["xp"], reverse=True)
        for sira, l in enumerate(lider[:20], 1):
            _, s_ikon, s_renk, _, _ = _seviye(l["xp"])
            madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                background:#0f172a;border-left:4px solid {s_renk};border-radius:0 10px 10px 0;">
                <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{l['ad']}</span>
                <span style="font-size:0.75rem;">{s_ikon}</span>
                <span style="color:{s_renk};font-weight:800;">{l['xp']} XP</span>
            </div>""", unsafe_allow_html=True)

        if not lider:
            st.info("Henuz XP kazanilmamis.")

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
                    <div style="color:#94a3b8;font-size:0.62rem;">{r['aciklama']}</div>
                    <div style="color:#c9a84c;font-size:0.68rem;font-weight:700;margin-top:3px;">+{r['xp']} XP</div>
                </div>""", unsafe_allow_html=True)

    # ── XP TABLOSU ──
    with sub[3]:
        styled_section("Aktivite XP Tablosu")
        for akt, puan in sorted(_XP_PUANLARI.items(), key=lambda x: x[1], reverse=True):
            bar_w = round(puan / 15 * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                <span style="min-width:130px;font-size:0.8rem;color:#e2e8f0;font-weight:600;">{akt}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#c9a84c;border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">+{puan}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. SOSYAL SORUMLULUK PROJELERİ & TOPLUM HİZMETİ
# ════════════════════════════════════════════════════════════

def render_sosyal_sorumluluk(store):
    """Sosyal Sorumluluk Projeleri — proje takip, gönüllü saat, etki raporu."""
    styled_section("Sosyal Sorumluluk Projeleri & Toplum Hizmeti", "#059669")
    styled_info_banner(
        "Ogrencilerin sosyal sorumluluk projelerini planlayin. "
        "Gonullu saat takibi, toplam etki raporu, gonulluluk belgesi.",
        banner_type="info", icon="🌍")

    projeler = _lj("sosyal_projeler.json")
    gonullu_saatler = _lj("gonullu_saatler.json")

    # KPI
    aktif = sum(1 for p in projeler if p.get("durum") in ("Planlandi", "Devam Ediyor"))
    tamamlanan = sum(1 for p in projeler if p.get("durum") == "Tamamlandi")
    toplam_saat = sum(g.get("saat", 0) for g in gonullu_saatler)
    toplam_gonullu = len(set(g.get("ogrenci","") for g in gonullu_saatler))

    styled_stat_row([
        ("Aktif Proje", str(aktif), "#059669", "🌍"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
        ("Toplam Saat", str(toplam_saat), "#3b82f6", "⏱️"),
        ("Gonullu", str(toplam_gonullu), "#8b5cf6", "🦸"),
    ])

    sub = st.tabs(["➕ Yeni Proje", "📋 Proje Listesi", "⏱️ Gonullu Saat", "📊 Etki Raporu", "📜 Belge"])

    # ── YENİ PROJE ──
    with sub[0]:
        styled_section("Yeni Sosyal Sorumluluk Projesi")
        with st.form("proje_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_ad = st.text_input("Proje Adi", key="pr_ad")
                p_kat = st.selectbox("Kategori", _PROJE_KATEGORILERI, key="pr_kat")
                p_bas = st.date_input("Baslangic", key="pr_bas")
            with c2:
                p_hedef = st.text_input("Hedef", placeholder="100 kitap toplamak", key="pr_hedef")
                p_sorumlu = st.text_input("Proje Sorumlusu", key="pr_sor")
                p_bit = st.date_input("Bitis", key="pr_bit")
            p_aciklama = st.text_area("Proje Aciklamasi", height=60, key="pr_acik")
            p_gonulluler = st.text_area("Gonullu Ogrenciler (her satira bir)", height=60, key="pr_gon")

            if st.form_submit_button("Proje Olustur", use_container_width=True, type="primary"):
                if p_ad:
                    gonulluler = [g.strip() for g in p_gonulluler.split("\n") if g.strip()]
                    projeler.append({
                        "id": f"pr_{uuid.uuid4().hex[:8]}",
                        "ad": p_ad, "kategori": p_kat,
                        "hedef": p_hedef, "sorumlu": p_sorumlu,
                        "baslangic": p_bas.isoformat(), "bitis": p_bit.isoformat(),
                        "aciklama": p_aciklama, "gonulluler": gonulluler,
                        "durum": "Planlandi", "created_at": datetime.now().isoformat(),
                    })
                    _sj("sosyal_projeler.json", projeler)
                    st.success(f"'{p_ad}' projesi olusturuldu! ({len(gonulluler)} gonullu)")
                    st.rerun()

    # ── PROJE LİSTESİ ──
    with sub[1]:
        styled_section("Proje Takibi")
        if not projeler:
            st.info("Proje yok.")
        else:
            for p in sorted(projeler, key=lambda x: x.get("baslangic",""), reverse=True):
                d_renk = _PROJE_DURUM_RENK.get(p.get("durum",""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {d_renk};border-radius:0 14px 14px 0;
                    padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🌍 {p.get('ad','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:3px 10px;border-radius:8px;
                            font-size:0.7rem;font-weight:700;">{p.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        {p.get('kategori','')} | {p.get('baslangic','')[:10]} → {p.get('bitis','')[:10]}
                        | {len(p.get('gonulluler',[]))} gonullu | Hedef: {p.get('hedef','')}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {p.get('id','')}", expanded=False):
                    yeni = st.selectbox("Durum", _PROJE_DURUMLARI,
                        index=_PROJE_DURUMLARI.index(p.get("durum","Planlandi")) if p.get("durum") in _PROJE_DURUMLARI else 0,
                        key=f"pr_d_{p['id']}")
                    if st.button("Guncelle", key=f"pr_g_{p['id']}"):
                        p["durum"] = yeni
                        _sj("sosyal_projeler.json", projeler)
                        st.rerun()

    # ── GÖNÜLLÜ SAAT ──
    with sub[2]:
        styled_section("Gonullu Saat Kaydi")
        with st.form("gonullu_form"):
            c1, c2 = st.columns(2)
            with c1:
                g_ogr = st.text_input("Ogrenci Adi", key="gn_ogr")
                g_proje = st.selectbox("Proje", [p.get("ad","") for p in projeler] if projeler else ["--"], key="gn_pr")
            with c2:
                g_saat = st.number_input("Saat", min_value=0.5, value=2.0, step=0.5, key="gn_saat")
                g_tarih = st.date_input("Tarih", key="gn_tarih")
            g_aciklama = st.text_input("Yapilan Is", key="gn_acik")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if g_ogr:
                    gonullu_saatler.append({
                        "id": f"gn_{uuid.uuid4().hex[:8]}",
                        "ogrenci": g_ogr, "proje": g_proje,
                        "saat": g_saat, "aciklama": g_aciklama,
                        "tarih": g_tarih.isoformat(),
                    })
                    _sj("gonullu_saatler.json", gonullu_saatler)
                    st.success(f"{g_ogr}: {g_saat} saat kaydedildi!")
                    st.rerun()

        # Liderlik
        if gonullu_saatler:
            styled_section("Gonullu Saat Liderligi")
            ogr_saat = defaultdict(float)
            for g in gonullu_saatler:
                ogr_saat[g.get("ogrenci","")] += g.get("saat", 0)
            for sira, (ad, saat) in enumerate(sorted(ogr_saat.items(), key=lambda x: x[1], reverse=True)[:10], 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ad}</span>
                    <span style="color:#059669;font-weight:800;font-size:0.82rem;">{saat}h</span>
                </div>""", unsafe_allow_html=True)

    # ── ETKİ RAPORU ──
    with sub[3]:
        styled_section("Toplam Etki Raporu")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#05966920);border:2px solid #059669;
            border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
            <div style="color:#6ee7b7;font-size:0.85rem;">Toplum Hizmeti Etki Ozeti</div>
            <div style="display:flex;justify-content:center;gap:30px;margin-top:12px;">
                <div><div style="color:#10b981;font-weight:900;font-size:2rem;">{len(projeler)}</div><div style="color:#64748b;font-size:0.68rem;">Proje</div></div>
                <div><div style="color:#3b82f6;font-weight:900;font-size:2rem;">{toplam_gonullu}</div><div style="color:#64748b;font-size:0.68rem;">Gonullu</div></div>
                <div><div style="color:#8b5cf6;font-weight:900;font-size:2rem;">{toplam_saat}</div><div style="color:#64748b;font-size:0.68rem;">Saat</div></div>
                <div><div style="color:#f59e0b;font-weight:900;font-size:2rem;">{tamamlanan}</div><div style="color:#64748b;font-size:0.68rem;">Tamamlanan</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        if projeler:
            kat_say = Counter(p.get("kategori","") for p in projeler)
            styled_section("Kategori Dagilimi")
            for kat, sayi in kat_say.most_common():
                st.markdown(f"- 🌍 **{kat}**: {sayi} proje")

    # ── BELGE ──
    with sub[4]:
        styled_section("Gonulluluk Belgesi")
        if gonullu_saatler:
            ogr_toplam = defaultdict(float)
            for g in gonullu_saatler:
                ogr_toplam[g.get("ogrenci","")] += g.get("saat", 0)
            for ad, saat in sorted(ogr_toplam.items(), key=lambda x: x[1], reverse=True)[:15]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 10px;margin:2px 0;
                    background:#05966910;border:1px solid #05966930;border-radius:8px;">
                    <span style="color:#e2e8f0;font-size:0.78rem;flex:1;">{ad}</span>
                    <span style="color:#059669;font-weight:700;font-size:0.75rem;">{saat} saat</span>
                    <span style="color:#059669;font-size:0.65rem;">📜 Belge Hazir</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Gonullu kaydi yok.")


# ════════════════════════════════════════════════════════════
# 3. ETKİNLİK OTOMASYON & AKILLI İŞ AKIŞI MOTORU
# ════════════════════════════════════════════════════════════

def render_etkinlik_otomasyon(store):
    """Etkinlik Otomasyon — onay akışı, otomatik görev, hatırlatma, checklist."""
    styled_section("Etkinlik Otomasyon & Akilli Is Akisi", "#6366f1")
    styled_info_banner(
        "Etkinlik planlama surecini otomasyona alin. Onay akisi, "
        "otomatik gorev atama, hatirlatma, etkinlik sonrasi checklist.",
        banner_type="info", icon="🔄")

    is_akislari = _lj("etkinlik_is_akislari.json")
    gorevler = _lj("etkinlik_gorevleri.json")

    # KPI
    bekleyen_onay = sum(1 for ia in is_akislari if ia.get("onay_durum") == "Bekliyor")
    aktif_gorev = sum(1 for g in gorevler if g.get("durum") == "Bekliyor")
    tamamlanan_gorev = sum(1 for g in gorevler if g.get("durum") == "Tamamlandi")

    styled_stat_row([
        ("Bekleyen Onay", str(bekleyen_onay), "#f59e0b", "⏳"),
        ("Aktif Gorev", str(aktif_gorev), "#3b82f6", "📋"),
        ("Tamamlanan", str(tamamlanan_gorev), "#10b981", "✅"),
        ("Toplam Akis", str(len(is_akislari)), "#6366f1", "🔄"),
    ])

    sub = st.tabs(["🔄 Onay Akisi", "📋 Otomatik Gorev", "⏰ Hatirlatmalar", "✅ Checklist"])

    # ── ONAY AKIŞI ──
    with sub[0]:
        styled_section("Etkinlik Onay Akisi")
        st.caption("Etkinlik planlama → Ogretmen → Mudur Yardimcisi → Mudur")

        with st.form("onay_form"):
            c1, c2 = st.columns(2)
            with c1:
                o_etkinlik = st.text_input("Etkinlik Adi", key="oa_etk")
                o_talep_eden = st.text_input("Talep Eden", key="oa_talep")
            with c2:
                o_tarih = st.date_input("Planlanan Tarih", key="oa_tarih")
                o_tur = st.selectbox("Etkinlik Turu", list(_GOREV_SABLONLARI.keys()), key="oa_tur")
            o_aciklama = st.text_area("Aciklama", height=60, key="oa_acik")

            if st.form_submit_button("Onay Sureci Baslat", use_container_width=True, type="primary"):
                if o_etkinlik:
                    ia = {
                        "id": f"ia_{uuid.uuid4().hex[:8]}",
                        "etkinlik": o_etkinlik, "talep_eden": o_talep_eden,
                        "tarih": o_tarih.isoformat(), "tur": o_tur,
                        "aciklama": o_aciklama,
                        "onay_adimlari": {a: "Bekliyor" for a in _ONAY_ADIMLARI},
                        "onay_durum": "Bekliyor",
                        "created_at": datetime.now().isoformat(),
                    }
                    is_akislari.append(ia)
                    _sj("etkinlik_is_akislari.json", is_akislari)

                    # Otomatik gorev olustur
                    sablon = _GOREV_SABLONLARI.get(o_tur, _GOREV_SABLONLARI["Genel"])
                    for g_ad in sablon:
                        gorevler.append({
                            "id": f"eg_{uuid.uuid4().hex[:8]}",
                            "is_akis_id": ia["id"],
                            "etkinlik": o_etkinlik,
                            "gorev": g_ad, "sorumlu": "",
                            "durum": "Bekliyor",
                            "created_at": datetime.now().isoformat(),
                        })
                    _sj("etkinlik_gorevleri.json", gorevler)
                    st.success(f"Onay sureci baslatildi + {len(sablon)} gorev otomatik atandi!")
                    st.rerun()

        # Onay bekleyenler
        if is_akislari:
            styled_section("Onay Bekleyen Etkinlikler")
            for ia in sorted(is_akislari, key=lambda x: x.get("created_at",""), reverse=True):
                onaylar = ia.get("onay_adimlari", {})
                onay_tamamlanan = sum(1 for v in onaylar.values() if v == "Onaylandi")
                toplam_adim = max(len(onaylar), 1)
                pct = round(onay_tamamlanan / toplam_adim * 100)
                renk = "#10b981" if pct == 100 else "#f59e0b" if pct > 0 else "#3b82f6"

                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">🔄 {ia.get('etkinlik','')}</span>
                        <span style="color:{renk};font-size:0.7rem;font-weight:700;">{onay_tamamlanan}/{toplam_adim} onay</span>
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:8px;margin-top:6px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Onay Detay: {ia.get('id','')}", expanded=False):
                    for adim, durum in onaylar.items():
                        d_renk = "#10b981" if durum == "Onaylandi" else "#ef4444" if durum == "Reddedildi" else "#f59e0b"
                        ikon = "✅" if durum == "Onaylandi" else "❌" if durum == "Reddedildi" else "⏳"
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.markdown(f"{ikon} **{adim}** — {durum}")
                        with c2:
                            if durum == "Bekliyor":
                                if st.button("Onayla", key=f"oa_o_{ia['id']}_{adim}"):
                                    ia["onay_adimlari"][adim] = "Onaylandi"
                                    if all(v == "Onaylandi" for v in ia["onay_adimlari"].values()):
                                        ia["onay_durum"] = "Onaylandi"
                                    _sj("etkinlik_is_akislari.json", is_akislari)
                                    st.rerun()

    # ── OTOMATİK GÖREV ──
    with sub[1]:
        styled_section("Etkinlik Gorevleri")
        if not gorevler:
            st.info("Gorev yok.")
        else:
            # Etkinlik bazli grupla
            etk_grp = defaultdict(list)
            for g in gorevler:
                etk_grp[g.get("etkinlik","?")].append(g)

            for etk, g_list in etk_grp.items():
                tamamlanan_g = sum(1 for g in g_list if g.get("durum") == "Tamamlandi")
                pct = round(tamamlanan_g / max(len(g_list), 1) * 100)
                renk = "#10b981" if pct == 100 else "#f59e0b" if pct > 0 else "#3b82f6"

                st.markdown(f"**{etk}** — {tamamlanan_g}/{len(g_list)} gorev (%{pct})")
                for g in g_list:
                    g_renk = _GOREV_DURUM_RENK.get(g.get("durum",""), "#94a3b8")
                    g_ikon = "✅" if g.get("durum") == "Tamamlandi" else "🔄" if g.get("durum") == "Devam Ediyor" else "⬜"
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"{g_ikon} {g.get('gorev','')}")
                    with c2:
                        if g.get("durum") != "Tamamlandi":
                            if st.button("✓", key=f"eg_d_{g['id']}"):
                                g["durum"] = "Tamamlandi"
                                _sj("etkinlik_gorevleri.json", gorevler)
                                st.rerun()
                st.markdown("---")

    # ── HATIRLATMALAR ──
    with sub[2]:
        styled_section("Otomatik Hatirlatmalar")
        bugun = date.today()
        yaklasan = [ia for ia in is_akislari
                    if ia.get("onay_durum") == "Onaylandi"
                    and ia.get("tarih","") >= bugun.isoformat()
                    and ia.get("tarih","") <= (bugun + timedelta(days=7)).isoformat()]

        if yaklasan:
            for ia in yaklasan:
                try:
                    etk_tarih = date.fromisoformat(ia.get("tarih",""))
                    kalan = (etk_tarih - bugun).days
                except Exception:
                    kalan = "?"
                renk = "#ef4444" if isinstance(kalan, int) and kalan <= 1 else "#f59e0b" if isinstance(kalan, int) and kalan <= 3 else "#3b82f6"
                st.markdown(f"""
                <div style="background:{renk}10;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:10px 14px;margin:5px 0;">
                    <span style="color:{renk};font-weight:800;">⏰ {kalan} gun kaldi!</span>
                    <span style="color:#e2e8f0;font-weight:600;margin-left:8px;">{ia.get('etkinlik','')}</span>
                    <div style="color:#64748b;font-size:0.7rem;margin-top:2px;">{ia.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Yaklasan etkinlik hatirlatmasi yok.")

        # Eksik gorevler
        eksik = [g for g in gorevler if g.get("durum") == "Bekliyor"]
        if eksik:
            styled_section(f"Tamamlanmamis Gorevler ({len(eksik)})")
            for g in eksik[:10]:
                st.markdown(f"  - ⬜ **{g.get('etkinlik','')}**: {g.get('gorev','')}")

    # ── CHECKLİST ──
    with sub[3]:
        styled_section("Etkinlik Sonrasi Checklist")
        checklist = [
            "Katilimci memnuniyet anketi gonderildi",
            "Fotograflar/videolar yuklendi",
            "Gelir-gider raporu tamamlandi",
            "Veli bilgilendirme yapildi",
            "Etkinlik degerlendirme formu dolduruldu",
            "Sosyal medya paylasimi yapildi",
            "Odeme/faturalar tamamlandi",
            "Arsiv kaydi olusturuldu",
        ]
        st.caption("Etkinlik sonrasinda tamamlanmasi gereken isler:")
        for i, item in enumerate(checklist):
            checked = st.checkbox(item, key=f"cl_{i}")
        tamamlanan_cl = sum(1 for i in range(len(checklist)) if st.session_state.get(f"cl_{i}", False))
        st.markdown(f"**Tamamlanan: {tamamlanan_cl}/{len(checklist)}**")
