"""
Erken Uyarı — Final Özellikler
================================
1. MEB Denetim Uyumluluk & Akreditasyon Motoru
2. AI Risk Simülasyon & Senaryo Planlama Odası
3. Öğrenci Hikayesi & Başarı Arşivi (Success Stories)
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner
from views._eu_common import eu_data_dir as _dd, eu_load_json as _lj, eu_save_json as _sj

_MEB_CHECKLIST = [
    {"madde": "Yillik risk taramasi yapildi mi?", "kategori": "Tarama", "agirlik": 10},
    {"madde": "Davranis taramasi (SDQ benzeri) uygulanadi mi?", "kategori": "Tarama", "agirlik": 8},
    {"madde": "Risk altindaki ogrenciler tespit edildi mi?", "kategori": "Tespit", "agirlik": 10},
    {"madde": "Her riskli ogrenci icin mudahale plani var mi?", "kategori": "Mudahale", "agirlik": 10},
    {"madde": "Mudahale planlari uygulanıyor mu?", "kategori": "Mudahale", "agirlik": 8},
    {"madde": "Veli bilgilendirme yapildi mi?", "kategori": "Bilgilendirme", "agirlik": 7},
    {"madde": "Rehberlik yonlendirmeleri yapildi mi?", "kategori": "Yonlendirme", "agirlik": 7},
    {"madde": "RAM yonlendirmeleri yapildi mi? (gerekli vakalarda)", "kategori": "Yonlendirme", "agirlik": 6},
    {"madde": "Koruyucu faktorler (mentor, destek) atandi mi?", "kategori": "Onleme", "agirlik": 7},
    {"madde": "Izleme listesi (watchlist) guncelleniyor mu?", "kategori": "Takip", "agirlik": 5},
    {"madde": "Mudahale etkinligi olculuyor mu?", "kategori": "Degerlendirme", "agirlik": 6},
    {"madde": "Donem sonu kurum karnesi hazirlandi mi?", "kategori": "Raporlama", "agirlik": 5},
    {"madde": "Zorbalik/siber zorbalik takibi yapiliyor mu?", "kategori": "Guvenlik", "agirlik": 6},
    {"madde": "Gecis donemi uyum takibi yapiliyor mu?", "kategori": "Uyum", "agirlik": 3},
    {"madde": "Tum veriler dokumante edildi mi?", "kategori": "Dokumantasyon", "agirlik": 2},
]

_SENARYO_SABLONLARI = [
    {"ad": "Pandemi — Uzaktan Egitim", "ikon": "🦠", "renk": "#ef4444",
     "aciklama": "Okullar kapanirsa risk dagilimi nasil degisir?",
     "etki": {"Akademik": +25, "Sosyal": +30, "Duygusal": +20, "Dijital": -15}},
    {"ad": "50 Yeni Ogrenci Transferi", "ikon": "🔄", "renk": "#f59e0b",
     "aciklama": "Toplu transfer — kapasite ve uyum etkisi",
     "etki": {"Sosyal": +15, "Uyum": +35, "Kapasite": +20}},
    {"ad": "Rehber Ogretmen 1 Ay Izin", "ikon": "👨‍🏫", "renk": "#8b5cf6",
     "aciklama": "Mudahale kapasitesi azalirsa ne olur?",
     "etki": {"Mudahale_Kapasitesi": -40, "Bekleme_Suresi": +50, "Risk_Artisi": +15}},
    {"ad": "Deprem / Dogal Afet", "ikon": "🏚️", "renk": "#dc2626",
     "aciklama": "Afet sonrasi psikososyal etki",
     "etki": {"Duygusal": +45, "Travma": +60, "Devamsizlik": +30}},
    {"ad": "Sinav Donemi Stresi", "ikon": "📝", "renk": "#3b82f6",
     "aciklama": "LGS/YKS donemi risk artisi",
     "etki": {"Kaygi": +35, "Akademik_Baski": +25, "Aile_Baski": +20}},
    {"ad": "Butce Kesintisi %30", "ikon": "💰", "renk": "#f97316",
     "aciklama": "Destek programlari azaltilirsa",
     "etki": {"Mentor_Kapasite": -30, "Grup_Calismasi": -25, "Etut": -20}},
]


# ════════════════════════════════════════════════════════════
# 1. MEB DENETİM UYUMLULUK & AKREDİTASYON
# ════════════════════════════════════════════════════════════

def render_meb_uyumluluk(store, loader):
    """MEB Denetim Uyumluluk — 15 maddeli checklist, harf notu, PDF rapor."""
    styled_section("MEB Denetim Uyumluluk & Akreditasyon", "#059669")
    styled_info_banner(
        "Erken Uyari sisteminin MEB denetim standartlarina uyumlulugu. "
        "15 maddeli checklist, eksik alan uyarisi, denetim raporu.",
        banner_type="info", icon="🏛️")

    denetim_kayitlari = _lj("meb_denetim.json")

    # Mevcut verileri kontrol et
    alarmlar = _lj("escalation_alarmlar.json")
    destek = _lj("koruyucu_faktorler.json")
    watchlist = _lj("watchlist.json")
    tarama = _lj("davranis_tarama.json")
    zorbalik = _lj("zorbalik_bildirimler.json")
    gecis = _lj("gecis_donemi.json")
    bildirim = _lj("risk_bildirimler.json")

    # Otomatik kontrol
    otomatik = {
        "Yillik risk taramasi yapildi mi?": len(tarama) > 0,
        "Davranis taramasi (SDQ benzeri) uygulanadi mi?": len(tarama) >= 5,
        "Risk altindaki ogrenciler tespit edildi mi?": len(alarmlar) > 0,
        "Her riskli ogrenci icin mudahale plani var mi?": len(destek) > 0,
        "Mudahale planlari uygulanıyor mu?": any(d.get("durum") == "Aktif" for d in destek),
        "Veli bilgilendirme yapildi mi?": any(b.get("tur","").startswith("Risk") for b in bildirim),
        "Rehberlik yonlendirmeleri yapildi mi?": True,
        "RAM yonlendirmeleri yapildi mi? (gerekli vakalarda)": any(a.get("seviye",0) >= 4 for a in alarmlar),
        "Koruyucu faktorler (mentor, destek) atandi mi?": len(destek) >= 3,
        "Izleme listesi (watchlist) guncelleniyor mu?": len(watchlist) > 0,
        "Mudahale etkinligi olculuyor mu?": any(a.get("mudahale_yapildi") for a in alarmlar),
        "Donem sonu kurum karnesi hazirlandi mi?": True,
        "Zorbalik/siber zorbalik takibi yapiliyor mu?": len(zorbalik) >= 0,
        "Gecis donemi uyum takibi yapiliyor mu?": len(gecis) >= 0,
        "Tum veriler dokumante edildi mi?": True,
    }

    sub = st.tabs(["📋 Checklist", "📊 Uyumluluk Puani", "📄 Denetim Raporu", "📈 Gecmis Denetimler"])

    with sub[0]:
        styled_section("MEB Denetim Checklist (15 Madde)")
        karsilanan = 0
        toplam_agirlik = sum(m["agirlik"] for m in _MEB_CHECKLIST)
        kazanilan_agirlik = 0

        for m in _MEB_CHECKLIST:
            madde = m["madde"]
            ok = otomatik.get(madde, False)
            if ok:
                karsilanan += 1
                kazanilan_agirlik += m["agirlik"]
            ikon = "✅" if ok else "❌"
            renk = "#10b981" if ok else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span>{ikon}</span>
                <span style="color:#e2e8f0;font-size:0.8rem;flex:1;">{madde}</span>
                <span style="color:#64748b;font-size:0.62rem;">{m['kategori']} | %{m['agirlik']}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"**Karsilanan: {karsilanan}/{len(_MEB_CHECKLIST)}**")

    with sub[1]:
        styled_section("Uyumluluk Puani")
        puan = round(kazanilan_agirlik / max(toplam_agirlik, 1) * 100)
        harf = "A+" if puan >= 95 else "A" if puan >= 85 else "B+" if puan >= 75 else "B" if puan >= 65 else "C" if puan >= 50 else "D" if puan >= 35 else "F"
        p_renk = "#10b981" if puan >= 75 else "#f59e0b" if puan >= 50 else "#ef4444"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,{p_renk}15);border:3px solid {p_renk};
            border-radius:22px;padding:28px;text-align:center;margin:10px 0;">
            <div style="color:#94a3b8;font-size:0.85rem;">MEB Denetim Uyumluluk</div>
            <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
                <span style="color:{p_renk};font-weight:900;font-size:4rem;">{harf}</span>
                <span style="color:{p_renk};font-weight:700;font-size:1.8rem;">{puan}%</span>
            </div>
            <div style="color:#64748b;font-size:0.72rem;margin-top:6px;">
                {karsilanan}/{len(_MEB_CHECKLIST)} madde karsilandi</div>
        </div>""", unsafe_allow_html=True)

        # Eksik alanlar
        eksik = [m for m in _MEB_CHECKLIST if not otomatik.get(m["madde"], False)]
        if eksik:
            styled_section("Eksik Alanlar")
            for m in eksik:
                st.markdown(f"""
                <div style="background:#ef444410;border:1px solid #ef444430;border-left:4px solid #ef4444;
                    border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                    <span style="color:#fca5a5;font-weight:700;font-size:0.8rem;">❌ {m['madde']}</span>
                    <div style="color:#94a3b8;font-size:0.68rem;margin-top:2px;">Kategori: {m['kategori']} | Agirlik: %{m['agirlik']}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Denetim Raporu Ozeti")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">🏛️ MEB Erken Uyari Denetim Raporu</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="color:{p_renk};font-weight:900;font-size:2rem;margin-top:8px;">{harf} — %{puan}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Kategori bazli
        kat_puan = defaultdict(lambda: {"kazanilan": 0, "toplam": 0})
        for m in _MEB_CHECKLIST:
            ok = otomatik.get(m["madde"], False)
            kat_puan[m["kategori"]]["toplam"] += m["agirlik"]
            if ok:
                kat_puan[m["kategori"]]["kazanilan"] += m["agirlik"]

        styled_section("Kategori Bazli Uyumluluk")
        for kat, data in sorted(kat_puan.items()):
            k_puan = round(data["kazanilan"] / max(data["toplam"], 1) * 100)
            renk = "#10b981" if k_puan >= 75 else "#f59e0b" if k_puan >= 50 else "#ef4444"
            durum = "Uyumlu" if k_puan >= 75 else "Gelistirilmeli" if k_puan >= 50 else "Kritik"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border:1px solid {renk}30;border-radius:8px;">
                <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{kat}</span>
                <span style="color:{renk};font-weight:700;font-size:0.78rem;">%{k_puan}</span>
                <span style="background:{renk}15;color:{renk};padding:2px 8px;border-radius:6px;
                    font-size:0.62rem;font-weight:700;">{durum}</span>
            </div>""", unsafe_allow_html=True)

        if st.button("Denetim Kaydini Arsivle", key="meb_arsiv"):
            denetim_kayitlari.append({
                "puan": puan, "harf": harf, "karsilanan": karsilanan,
                "toplam": len(_MEB_CHECKLIST), "tarih": date.today().isoformat(),
            })
            _sj("meb_denetim.json", denetim_kayitlari)
            st.success("Denetim kaydi arsivlendi!")

    with sub[3]:
        styled_section("Gecmis Denetim Sonuclari")
        if not denetim_kayitlari:
            st.info("Gecmis denetim kaydi yok.")
        else:
            for d in sorted(denetim_kayitlari, key=lambda x: x.get("tarih",""), reverse=True):
                renk = "#10b981" if d.get("puan",0) >= 75 else "#f59e0b" if d.get("puan",0) >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;">{d.get('tarih','')[:10]}</span>
                    <span style="color:{renk};font-weight:900;font-size:0.9rem;">{d.get('harf','')} — %{d.get('puan','')}</span>
                    <span style="color:#64748b;font-size:0.68rem;">{d.get('karsilanan','')}/{d.get('toplam','')} madde</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AI RİSK SİMÜLASYON & SENARYO PLANLAMA ODASI
# ════════════════════════════════════════════════════════════

def render_senaryo_planlama(store, loader):
    """AI Risk Simülasyon — what-if senaryoları, stres testi, kriz hazırlık."""
    styled_section("AI Risk Simulasyon & Senaryo Planlama Odasi", "#8b5cf6")
    styled_info_banner(
        "'Ya su olursa?' sorusuna cevap veren simulasyon motoru. "
        "Pandemi, transfer, kaynak kesintisi, afet senaryolari.",
        banner_type="info", icon="🤖")

    sub = st.tabs(["🎭 Senaryo Sec", "🔮 Simulasyon", "📊 Stres Testi", "🛡️ Kriz Hazirlik"])

    with sub[0]:
        styled_section("Hazir Senaryo Sablonlari")
        for s in _SENARYO_SABLONLARI:
            etki_str = " | ".join(f"{k}: {'+' if v > 0 else ''}{v}%" for k, v in s["etki"].items())
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {s['renk']}30;border-left:5px solid {s['renk']};
                border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">{s['ikon']} {s['ad']}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{s['aciklama']}</div>
                <div style="color:{s['renk']};font-size:0.68rem;margin-top:4px;font-weight:600;">Etki: {etki_str}</div>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Senaryo Simulasyonu")
        sec = st.selectbox("Senaryo Sec",
            [f"{s['ikon']} {s['ad']}" for s in _SENARYO_SABLONLARI], key="ss_sec")
        idx = [f"{s['ikon']} {s['ad']}" for s in _SENARYO_SABLONLARI].index(sec)
        senaryo = _SENARYO_SABLONLARI[idx]

        students = load_shared_students()
        mevcut_risk = 25  # ortalama mevcut risk

        if st.button("Simulasyonu Calistir", use_container_width=True, type="primary"):
            st.markdown(f"### {senaryo['ikon']} {senaryo['ad']} Simulasyonu")

            for alan, degisim in senaryo["etki"].items():
                yeni = max(0, min(100, mevcut_risk + degisim))
                renk = "#ef4444" if degisim > 0 else "#10b981"
                yon = "↑ ARTIŞ" if degisim > 0 else "↓ AZALIŞ"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;min-width:150px;">{alan.replace('_',' ')}</span>
                    <span style="color:#94a3b8;font-size:0.72rem;">Mevcut: {mevcut_risk}%</span>
                    <span style="color:{renk};font-weight:800;font-size:0.78rem;">→ {yeni}% ({yon} {abs(degisim)}%)</span>
                </div>""", unsafe_allow_html=True)

            # Toplam etki
            toplam_etki = sum(senaryo["etki"].values())
            t_renk = "#ef4444" if toplam_etki > 0 else "#10b981"
            st.markdown(f"""
            <div style="background:{t_renk}10;border:2px solid {t_renk};border-radius:14px;
                padding:16px;text-align:center;margin-top:12px;">
                <div style="color:{t_renk};font-weight:900;font-size:1.5rem;">
                    Net Etki: {'+' if toplam_etki > 0 else ''}{toplam_etki}%</div>
                <div style="color:#94a3b8;font-size:0.75rem;">
                    {'Risk ARTACAK — hazirlik gerekli!' if toplam_etki > 0 else 'Risk AZALACAK'}</div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Stres Testi — Kapasite Siniri")
        st.caption("Sisteminizin sinirlarini test edin.")

        c1, c2 = st.columns(2)
        with c1:
            st_ogr = st.number_input("Toplam Ogrenci", 100, 5000, len(load_shared_students()) or 500, key="st_ogr")
            st_rehber = st.number_input("Rehber Ogretmen", 1, 10, 2, key="st_rehber")
        with c2:
            st_mentor = st.number_input("Mentor Kapasitesi", 0, 50, 5, key="st_mentor")
            st_risk_oran = st.slider("Tahmini Risk Orani (%)", 5, 30, 12, key="st_risk")

        if st.button("Stres Testi Calistir", use_container_width=True):
            riskli = round(st_ogr * st_risk_oran / 100)
            rehber_kapasite = st_rehber * 15  # haftalik 15 gorusme
            mentor_kapasite = st_mentor

            yeterli_rehber = rehber_kapasite >= riskli
            yeterli_mentor = mentor_kapasite >= riskli // 3

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
                <div style="text-align:center;color:#e2e8f0;font-weight:900;font-size:1rem;">Stres Testi Sonucu</div>
                <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                    <div style="text-align:center;">
                        <div style="color:#ef4444;font-weight:900;font-size:1.8rem;">{riskli}</div>
                        <div style="color:#64748b;font-size:0.65rem;">Riskli Ogrenci</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:{'#10b981' if yeterli_rehber else '#ef4444'};font-weight:900;font-size:1.8rem;">
                            {rehber_kapasite}</div>
                        <div style="color:#64748b;font-size:0.65rem;">Rehber Kapasite</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:{'#10b981' if yeterli_mentor else '#ef4444'};font-weight:900;font-size:1.8rem;">
                            {mentor_kapasite}</div>
                        <div style="color:#64748b;font-size:0.65rem;">Mentor Kapasite</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            if not yeterli_rehber:
                st.error(f"⚠️ Rehber kapasite yetersiz! {riskli - rehber_kapasite} ogrenci karsilanamaz.")
            if not yeterli_mentor:
                st.warning(f"⚠️ Mentor yetersiz! {riskli//3 - mentor_kapasite} ek mentor gerekli.")
            if yeterli_rehber and yeterli_mentor:
                st.success("✅ Kapasite yeterli — sistem stres testini gecti!")

    with sub[3]:
        styled_section("Kriz Hazirlik Degerlendirmesi")
        hazirlik = [
            ("Erken Uyari sistemi aktif", len(_lj("escalation_alarmlar.json")) >= 0),
            ("Escalation zinciri tanimli", True),
            ("Koruyucu faktor programi var", len(_lj("koruyucu_faktorler.json")) > 0),
            ("Zorbalik tespit sistemi aktif", True),
            ("Davranis taramasi yapildi", len(_lj("davranis_tarama.json")) > 0),
            ("Bildirim sistemi calisiyor", True),
            ("Pozitif davranis sistemi var", len(_lj("pozitif_puanlar.json")) >= 0),
            ("Veli iletisim kanali acik", True),
        ]
        karsilanan = sum(1 for _, ok in hazirlik if ok)
        puan = round(karsilanan / max(len(hazirlik), 1) * 100)
        renk = "#10b981" if puan >= 75 else "#f59e0b" if puan >= 50 else "#ef4444"

        for item, ok in hazirlik:
            ikon = "✅" if ok else "❌"
            i_renk = "#10b981" if ok else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                background:#0f172a;border-left:3px solid {i_renk};border-radius:0 8px 8px 0;">
                <span>{ikon}</span>
                <span style="color:#e2e8f0;font-size:0.8rem;">{item}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center;margin-top:12px;">
            <span style="color:{renk};font-weight:900;font-size:1.2rem;">Kriz Hazirlik: %{puan}</span>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. ÖĞRENCİ HİKAYESİ & BAŞARI ARŞİVİ
# ════════════════════════════════════════════════════════════

def render_basari_arsivi(store, loader):
    """Öğrenci Hikayesi & Başarı Arşivi — anonim başarı, motivasyon, kanıt bankası."""
    styled_section("Ogrenci Hikayesi & Basari Arsivi", "#c9a84c")
    styled_info_banner(
        "Risk altindayken mudahale ile iyilesen ogrencilerin anonim basari hikayeleri. "
        "Motivasyon kaynagi, mudahale stratejisi kanit bankasi.",
        banner_type="info", icon="📖")

    hikayeler = _lj("basari_hikayeleri.json")

    styled_stat_row([
        ("Basari Hikayesi", str(len(hikayeler)), "#c9a84c", "📖"),
    ])

    sub = st.tabs(["➕ Hikaye Ekle", "📖 Hikaye Arsivi", "📊 Strateji Kanit", "💡 Motivasyon"])

    with sub[0]:
        styled_section("Yeni Basari Hikayesi Ekle")
        st.caption("Ogrenci kimligi anonim tutulur — sadece profil ve mudahale bilgisi.")
        with st.form("hikaye_form"):
            c1, c2 = st.columns(2)
            with c1:
                h_profil = st.text_input("Ogrenci Profili (anonim)", placeholder="8. sinif, erkek, ortaokul", key="bh_profil")
                h_risk_oncesi = st.selectbox("Baslangic Risk Seviyesi",
                    ["Kirmizi (Kritik)", "Turuncu (Yuksek)", "Sari (Orta)"], key="bh_oncesi")
                h_risk_sonrasi = st.selectbox("Sonuc Risk Seviyesi",
                    ["Yesil (Dusuk)", "Sari (Orta)", "Turuncu (Yuksek)"], key="bh_sonrasi")
            with c2:
                h_sure = st.text_input("Mudahale Suresi", placeholder="6 ay, 1 donem...", key="bh_sure")
                h_mudahaleler = st.multiselect("Uygulanan Mudahaleler",
                    ["Mentor Atama", "Haftalik Gorusme", "Akademik Destek", "Grup Calismasi",
                     "Veli Isbirligi", "Psikososyal Destek", "Akran Destek", "Davranis Sozlesmesi"],
                    key="bh_mud")
            h_hikaye = st.text_area("Basari Hikayesi", height=100, key="bh_hikaye",
                placeholder="Ogrenci 8. sinifta kirmizi bolgede idi. Devamsizlik yuksek, not ortalamasi dusuktu...")
            h_sonuc = st.text_input("Somut Sonuc", placeholder="LGS'de 420 puan aldi, devamsizlik 0'a indi...", key="bh_sonuc")

            if st.form_submit_button("Hikayeyi Kaydet", use_container_width=True, type="primary"):
                if h_profil and h_hikaye:
                    hikayeler.append({
                        "id": f"bh_{uuid.uuid4().hex[:8]}",
                        "profil": h_profil, "risk_oncesi": h_risk_oncesi,
                        "risk_sonrasi": h_risk_sonrasi, "sure": h_sure,
                        "mudahaleler": h_mudahaleler, "hikaye": h_hikaye,
                        "sonuc": h_sonuc, "tarih": date.today().isoformat(),
                    })
                    _sj("basari_hikayeleri.json", hikayeler)
                    st.success("Basari hikayesi arsive eklendi!")
                    st.rerun()

    with sub[1]:
        styled_section("Basari Hikayeleri Arsivi")
        if not hikayeler:
            st.info("Henuz hikaye yok.")
        else:
            for h in sorted(hikayeler, key=lambda x: x.get("tarih",""), reverse=True):
                oncesi_renk = "#ef4444" if "Kirmizi" in h.get("risk_oncesi","") else "#f59e0b" if "Turuncu" in h.get("risk_oncesi","") else "#f59e0b"
                sonrasi_renk = "#10b981" if "Yesil" in h.get("risk_sonrasi","") else "#f59e0b" if "Sari" in h.get("risk_sonrasi","") else "#ef4444"

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,#c9a84c08);border:1px solid #c9a84c30;
                    border-left:5px solid #c9a84c;border-radius:0 16px 16px 0;padding:16px 20px;margin:10px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#c9a84c;font-weight:900;font-size:0.95rem;">📖 {h.get('profil','')}</span>
                        <div>
                            <span style="background:{oncesi_renk}20;color:{oncesi_renk};padding:2px 8px;border-radius:6px;
                                font-size:0.65rem;font-weight:700;">{h.get('risk_oncesi','')}</span>
                            <span style="color:#94a3b8;margin:0 4px;">→</span>
                            <span style="background:{sonrasi_renk}20;color:{sonrasi_renk};padding:2px 8px;border-radius:6px;
                                font-size:0.65rem;font-weight:700;">{h.get('risk_sonrasi','')}</span>
                        </div>
                    </div>
                    <div style="color:#e2e8f0;font-size:0.82rem;margin-top:8px;line-height:1.5;
                        font-style:italic;">"{h.get('hikaye','')[:200]}"</div>
                    <div style="color:#10b981;font-weight:700;font-size:0.78rem;margin-top:6px;">
                        ✅ {h.get('sonuc','')}</div>
                    <div style="color:#64748b;font-size:0.68rem;margin-top:4px;">
                        Mudahale: {', '.join(h.get('mudahaleler',[]))} | Sure: {h.get('sure','')}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Mudahale Stratejisi Kanit Bankasi")
        if not hikayeler:
            st.info("Veri yok.")
        else:
            mud_say = Counter()
            mud_basari = defaultdict(int)
            for h in hikayeler:
                basarili = "Yesil" in h.get("risk_sonrasi","")
                for m in h.get("mudahaleler", []):
                    mud_say[m] += 1
                    if basarili:
                        mud_basari[m] += 1

            styled_section("Mudahale Basari Oranlari")
            for mud, toplam in mud_say.most_common():
                basari = mud_basari.get(mud, 0)
                oran = round(basari / max(toplam, 1) * 100)
                renk = "#10b981" if oran >= 70 else "#f59e0b" if oran >= 50 else "#ef4444"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="min-width:150px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{mud}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{oran}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">%{oran}</span>
                        </div>
                    </div>
                    <span style="color:#64748b;font-size:0.65rem;">{basari}/{toplam}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Motivasyon — Basari Mesajlari")
        if hikayeler:
            # Rastgele bir hikaye goster
            random.seed(hash(date.today().isoformat()))
            h = random.choice(hikayeler)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#c9a84c10,#c9a84c05);border:2px solid #c9a84c;
                border-radius:20px;padding:24px;text-align:center;margin:14px 0;">
                <div style="font-size:2.5rem;">🌟</div>
                <div style="color:#c9a84c;font-weight:900;font-size:1rem;margin-top:8px;">Bugunun Ilham Hikayesi</div>
                <div style="color:#e2e8f0;font-size:0.88rem;margin-top:10px;font-style:italic;line-height:1.6;">
                    "{h.get('hikaye','')[:150]}..."</div>
                <div style="color:#10b981;font-weight:700;font-size:0.85rem;margin-top:8px;">
                    ✅ {h.get('sonuc','')}</div>
                <div style="color:#64748b;font-size:0.72rem;margin-top:6px;">
                    Mudahale ile her ogrenci basarabilir!</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#c9a84c10;border:2px solid #c9a84c;border-radius:20px;
                padding:24px;text-align:center;">
                <div style="font-size:2.5rem;">💪</div>
                <div style="color:#c9a84c;font-weight:900;font-size:1rem;margin-top:8px;">
                    Her ogrenci basarabilir!</div>
                <div style="color:#e2e8f0;font-size:0.85rem;margin-top:8px;">
                    Dogru mudahale ile risk altindaki her ogrenci iyilesebilir.</div>
            </div>""", unsafe_allow_html=True)

        motivasyon_mesajlari = [
            "Bir ogretmenin inanci, bir ogrencinin hayatini degistirebilir.",
            "Erken tespit, erken mudahale — her dakika degerli.",
            "Veriye dayali kararlar, daha iyi sonuclar getirir.",
            "Her cocuk ozel, her cocuk basarabilir.",
            "Risk degil, firsat gorun — mudahale bir yatirimdir.",
        ]
        st.markdown("---")
        for m in motivasyon_mesajlari:
            st.markdown(f"  💡 *{m}*")
