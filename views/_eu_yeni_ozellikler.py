"""
Erken Uyarı — Yeni Özellikler
================================
1. Otomatik Alarm & Tırmanma (Escalation) Motoru
2. Koruyucu Faktör & Destek Programı Yönetimi
3. AI Dropout Tahmin & Proaktif Müdahale Senaryoları
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner
from views._eu_common import eu_data_dir as _dd, eu_load_json as _lj, eu_save_json as _sj, eu_ogrenci_sec as _ogr_sec

_ESCALATION_SEVIYELERI = {
    1: {"ad": "Seviye 1 — Sinif Ogretmeni", "hedef": "Sinif Ogretmeni", "renk": "#f59e0b", "ikon": "🟡", "sure_saat": 48},
    2: {"ad": "Seviye 2 — Rehber Ogretmen", "hedef": "Rehber Ogretmen", "renk": "#f97316", "ikon": "🟠", "sure_saat": 24},
    3: {"ad": "Seviye 3 — Mudur + Veli", "hedef": "Okul Muduru + Veli", "renk": "#ef4444", "ikon": "🔴", "sure_saat": 12},
    4: {"ad": "Seviye 4 — RAM / Sosyal Hizmet", "hedef": "RAM + Sosyal Hizmet", "renk": "#dc2626", "ikon": "🚨", "sure_saat": 6},
}

_ALARM_TETIKLEYICILER = [
    {"ad": "Devamsizlik 5+ gun", "kosul": "devamsizlik", "esik": 5, "seviye": 2},
    {"ad": "Not ortalamasi 40 alti", "kosul": "not_dusuk", "esik": 40, "seviye": 2},
    {"ad": "Ardisik 3 sinav basarisiz", "kosul": "sinav_basarisiz", "esik": 3, "seviye": 2},
    {"ad": "Davranis olayi 3+", "kosul": "davranis", "esik": 3, "seviye": 3},
    {"ad": "Devamsizlik 10+ gun", "kosul": "devamsizlik_ciddi", "esik": 10, "seviye": 3},
    {"ad": "Kriz bildirimi", "kosul": "kriz", "esik": 1, "seviye": 4},
    {"ad": "Intihar/kendine zarar riski", "kosul": "intihar_risk", "esik": 1, "seviye": 4},
]

_KORUYUCU_FAKTORLER = {
    "Mentor Atamasi": {"ikon": "🧑‍🏫", "renk": "#3b82f6", "etki": 15},
    "Akran Destek (Buddy)": {"ikon": "🤝", "renk": "#10b981", "etki": 10},
    "Haftalik Gorusme": {"ikon": "💬", "renk": "#8b5cf6", "etki": 12},
    "Akademik Destek Plani": {"ikon": "📚", "renk": "#059669", "etki": 15},
    "Davranis Sozlesmesi": {"ikon": "📝", "renk": "#f59e0b", "etki": 8},
    "Veli Isbirligi Aktif": {"ikon": "👨‍👩‍👧", "renk": "#0891b2", "etki": 12},
    "Etut/Telafi Dersi": {"ikon": "📖", "renk": "#6366f1", "etki": 10},
    "Psikososyal Destek": {"ikon": "🧠", "renk": "#dc2626", "etki": 18},
}

_DROPOUT_RISK_FAKTORLERI = [
    "Devamsizlik trendi yukseliyor", "Not ortalamasi dusuyor", "Arkadaslik iliskileri zayif",
    "Aile desteği yetersiz", "Ekonomik zorluk", "Davranış sorunları artıyor",
    "Motivasyon kaybı", "Okula aidiyet hissi dusuk",
]

_MEVSIM_RISK = {
    "Eylul": "Uyum sorunu — yeni ogrenciler, okul degistiren",
    "Kasim": "1. sinav donemi stresi, devamsizlik artisi",
    "Ocak": "Yariyil tatili sonrasi donus zorlugu",
    "Subat": "2. donem uyum, motivasyon dusuk",
    "Mayis": "Sinav kaygisi, LGS/YKS stresi",
    "Haziran": "Yil sonu yorgunluk, not kaygisi",
}


# ════════════════════════════════════════════════════════════
# 1. OTOMATİK ALARM & TIRMANMA (ESCALATION) MOTORU
# ════════════════════════════════════════════════════════════

def render_escalation_motoru(store, loader):
    """Otomatik Alarm & Tırmanma — seviyeli bildirim, izleme listesi, müdahale süresi."""
    styled_section("Otomatik Alarm & Tirmanma (Escalation) Motoru", "#ef4444")
    styled_info_banner(
        "Risk skoru esigi gectiginde otomatik alarm zinciri. "
        "4 seviye tirmandirma, izleme listesi, mudahale suresi olcumu.",
        banner_type="warning", icon="🚨")

    alarmlar = _lj("escalation_alarmlar.json")
    watchlist = _lj("watchlist.json")

    # KPI
    aktif = sum(1 for a in alarmlar if a.get("durum") == "Aktif")
    sev3_4 = sum(1 for a in alarmlar if a.get("seviye", 0) >= 3 and a.get("durum") == "Aktif")
    mudahale_beklenen = sum(1 for a in alarmlar if a.get("durum") == "Aktif" and not a.get("mudahale_yapildi"))

    styled_stat_row([
        ("Aktif Alarm", str(aktif), "#ef4444", "🚨"),
        ("Sev 3-4 (Kritik)", str(sev3_4), "#dc2626", "🔴"),
        ("Mudahale Bekleyen", str(mudahale_beklenen), "#f59e0b", "⏳"),
        ("Watchlist", str(len(watchlist)), "#8b5cf6", "👁️"),
    ])

    sub = st.tabs(["🚨 Yeni Alarm", "📋 Aktif Alarmlar", "👁️ Watchlist", "⚙️ Tetikleyiciler", "📊 Mudahale Suresi"])

    # ── YENİ ALARM ──
    with sub[0]:
        styled_section("Yeni Alarm Olustur")
        with st.form("alarm_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("ea_ogr")
                a_neden = st.selectbox("Alarm Nedeni",
                    [t["ad"] for t in _ALARM_TETIKLEYICILER], key="ea_neden")
                a_seviye = st.selectbox("Alarm Seviyesi", [1, 2, 3, 4],
                    format_func=lambda x: _ESCALATION_SEVIYELERI[x]["ad"], key="ea_sev")
            with c2:
                a_tarih = st.date_input("Tarih", key="ea_tarih")
                a_bildiren = st.text_input("Bildiren Kisi", key="ea_bildiren")
            a_aciklama = st.text_area("Aciklama", height=60, key="ea_acik")

            if st.form_submit_button("🚨 ALARM OLUSTUR", use_container_width=True, type="primary"):
                if ogr:
                    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
                    sev_info = _ESCALATION_SEVIYELERI[a_seviye]
                    alarm = {
                        "id": f"al_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "sinif": f"{ogr.get('sinif','')}/{ogr.get('sube','')}",
                        "neden": a_neden, "seviye": a_seviye,
                        "hedef": sev_info["hedef"],
                        "max_sure_saat": sev_info["sure_saat"],
                        "aciklama": a_aciklama, "bildiren": a_bildiren,
                        "durum": "Aktif", "mudahale_yapildi": False,
                        "tarih": a_tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    alarmlar.append(alarm)
                    _sj("escalation_alarmlar.json", alarmlar)
                    st.error(f"🚨 {sev_info['ikon']} {sev_info['ad']} — {ogr_ad}")
                    st.warning(f"Bildirim hedefi: {sev_info['hedef']} | Mudahale suresi: {sev_info['sure_saat']} saat")
                    st.rerun()

    # ── AKTİF ALARMLAR ──
    with sub[1]:
        styled_section("Aktif Alarmlar")
        aktif_list = [a for a in alarmlar if a.get("durum") == "Aktif"]
        if not aktif_list:
            st.success("Aktif alarm yok.")
        else:
            for a in sorted(aktif_list, key=lambda x: x.get("seviye",0), reverse=True):
                sev = a.get("seviye", 1)
                sev_info = _ESCALATION_SEVIYELERI.get(sev, _ESCALATION_SEVIYELERI[1])
                # Gecen sure hesapla
                try:
                    baslangic = datetime.fromisoformat(a.get("created_at",""))
                    gecen_saat = round((datetime.now() - baslangic).total_seconds() / 3600, 1)
                    gecikme = gecen_saat > sev_info["sure_saat"]
                except Exception:
                    gecen_saat, gecikme = 0, False

                border = "3px solid #dc2626" if gecikme else f"2px solid {sev_info['renk']}"

                st.markdown(f"""
                <div style="background:#0f172a;border:{border};border-left:6px solid {sev_info['renk']};
                    border-radius:0 14px 14px 0;padding:14px 18px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#fca5a5;font-weight:900;font-size:0.95rem;">
                            {sev_info['ikon']} {a.get('ogrenci','')}</span>
                        <span style="background:{sev_info['renk']}20;color:{sev_info['renk']};padding:3px 12px;
                            border-radius:8px;font-size:0.72rem;font-weight:800;">{sev_info['ad']}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">
                        {a.get('neden','')} | {a.get('sinif','')} | Hedef: {sev_info['hedef']}</div>
                    <div style="color:{'#dc2626' if gecikme else '#64748b'};font-size:0.7rem;margin-top:3px;
                        {'font-weight:800;' if gecikme else ''}">
                        {'⚠️ GECİKME! ' if gecikme else ''}Gecen: {gecen_saat}h / Max: {sev_info['sure_saat']}h
                        {'| Mudahale: ✅' if a.get('mudahale_yapildi') else '| Mudahale: ⏳ BEKLİYOR'}
                    </div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {a.get('id','')}", expanded=False):
                    mc1, mc2, mc3 = st.columns(3)
                    with mc1:
                        if st.button("Mudahale Yapildi", key=f"ea_mud_{a['id']}"):
                            a["mudahale_yapildi"] = True
                            a["mudahale_tarih"] = datetime.now().isoformat()
                            _sj("escalation_alarmlar.json", alarmlar)
                            st.rerun()
                    with mc2:
                        if st.button("Seviye Yukselt", key=f"ea_yuk_{a['id']}"):
                            if a["seviye"] < 4:
                                a["seviye"] += 1
                                _sj("escalation_alarmlar.json", alarmlar)
                                st.rerun()
                    with mc3:
                        if st.button("Alarmi Kapat", key=f"ea_kap_{a['id']}"):
                            a["durum"] = "Kapandi"
                            _sj("escalation_alarmlar.json", alarmlar)
                            st.rerun()

    # ── WATCHLIST ──
    with sub[2]:
        styled_section("Izleme Listesi (Watchlist)")
        with st.form("wl_form"):
            wl_ogr = _ogr_sec("wl_ogr")
            wl_neden = st.text_input("Izleme Nedeni", key="wl_neden")
            wl_sure = st.selectbox("Izleme Suresi", ["1 Hafta", "2 Hafta", "1 Ay", "Donem Sonuna Kadar"], key="wl_sure")

            if st.form_submit_button("Watchlist'e Ekle", use_container_width=True):
                if wl_ogr:
                    watchlist.append({
                        "ogrenci": f"{wl_ogr.get('ad','')} {wl_ogr.get('soyad','')}",
                        "sinif": f"{wl_ogr.get('sinif','')}/{wl_ogr.get('sube','')}",
                        "neden": wl_neden, "sure": wl_sure,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("watchlist.json", watchlist)
                    st.success("Watchlist'e eklendi!")
                    st.rerun()

        if watchlist:
            for w in watchlist:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">👁️ {w.get('ogrenci','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{w.get('neden','')}</span>
                    <span style="color:#8b5cf6;font-size:0.65rem;font-weight:700;">{w.get('sure','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── TETİKLEYİCİLER ──
    with sub[3]:
        styled_section("Otomatik Alarm Tetikleyicileri")
        for t in _ALARM_TETIKLEYICILER:
            sev = t["seviye"]
            sev_info = _ESCALATION_SEVIYELERI[sev]
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                background:#0f172a;border-left:4px solid {sev_info['renk']};border-radius:0 10px 10px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{t['ad']}</span>
                <span style="background:{sev_info['renk']}20;color:{sev_info['renk']};padding:2px 8px;
                    border-radius:6px;font-size:0.68rem;font-weight:700;">{sev_info['ikon']} Sev {sev}</span>
            </div>""", unsafe_allow_html=True)

    # ── MÜDAHALE SÜRESİ ──
    with sub[4]:
        styled_section("Mudahale Suresi Analizi")
        mudahale_yapilan = [a for a in alarmlar if a.get("mudahale_yapildi")]
        if not mudahale_yapilan:
            st.info("Mudahale kaydi yok.")
        else:
            sureler = []
            for a in mudahale_yapilan:
                try:
                    bas = datetime.fromisoformat(a.get("created_at",""))
                    mud = datetime.fromisoformat(a.get("mudahale_tarih",""))
                    saat = round((mud - bas).total_seconds() / 3600, 1)
                    sureler.append(saat)
                except Exception: pass

            if sureler:
                ort = round(sum(sureler) / len(sureler), 1)
                en_hizli = min(sureler)
                en_yavas = max(sureler)
                styled_stat_row([
                    ("Ort Sure", f"{ort}h", "#3b82f6", "⏱️"),
                    ("En Hizli", f"{en_hizli}h", "#10b981", "🏃"),
                    ("En Yavas", f"{en_yavas}h", "#ef4444", "🐢"),
                    ("Toplam", str(len(sureler)), "#8b5cf6", "📋"),
                ])


# ════════════════════════════════════════════════════════════
# 2. KORUYUCU FAKTÖR & DESTEK PROGRAMI YÖNETİMİ
# ════════════════════════════════════════════════════════════

def render_koruyucu_faktor(store, loader):
    """Koruyucu Faktör — mentor atama, buddy, destek planı, etkinlik ölçümü."""
    styled_section("Koruyucu Faktor & Destek Programi Yonetimi", "#059669")
    styled_info_banner(
        "Risk tespitinin otesinde koruyucu faktorleri takip edin. "
        "Mentor atama, akran destek, akademik plan, etkinlik olcumu.",
        banner_type="info", icon="🛡️")

    destek_kayitlari = _lj("koruyucu_faktorler.json")

    # KPI
    aktif_destek = sum(1 for d in destek_kayitlari if d.get("durum") == "Aktif")
    mentor_sayi = sum(1 for d in destek_kayitlari if d.get("faktor") == "Mentor Atamasi" and d.get("durum") == "Aktif")

    styled_stat_row([
        ("Aktif Destek", str(aktif_destek), "#059669", "🛡️"),
        ("Mentor", str(mentor_sayi), "#3b82f6", "🧑‍🏫"),
        ("Toplam Kayit", str(len(destek_kayitlari)), "#8b5cf6", "📋"),
    ])

    sub = st.tabs(["➕ Destek Ata", "📋 Aktif Destekler", "📊 Koruyucu Skor", "📈 Etkinlik Olcumu"])

    # ── DESTEK ATA ──
    with sub[0]:
        styled_section("Koruyucu Faktor / Destek Ata")
        with st.form("kf_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("kf_ogr")
                kf_faktor = st.selectbox("Destek Turu", list(_KORUYUCU_FAKTORLER.keys()), key="kf_tur")
            with c2:
                kf_sorumlu = st.text_input("Sorumlu Kisi", key="kf_sor")
                kf_baslangic = st.date_input("Baslangic", key="kf_bas")
            kf_not = st.text_area("Aciklama / Plan", height=60, key="kf_not")

            if st.form_submit_button("Destek Ata", use_container_width=True, type="primary"):
                if ogr:
                    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
                    destek_kayitlari.append({
                        "id": f"kf_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "sinif": f"{ogr.get('sinif','')}/{ogr.get('sube','')}",
                        "faktor": kf_faktor, "sorumlu": kf_sorumlu,
                        "aciklama": kf_not, "durum": "Aktif",
                        "baslangic": kf_baslangic.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("koruyucu_faktorler.json", destek_kayitlari)
                    info = _KORUYUCU_FAKTORLER[kf_faktor]
                    st.success(f"{info['ikon']} {kf_faktor} — {ogr_ad} icin atandi!")
                    st.rerun()

    # ── AKTİF DESTEKLER ──
    with sub[1]:
        styled_section("Aktif Destek Programlari")
        aktif_list = [d for d in destek_kayitlari if d.get("durum") == "Aktif"]
        if not aktif_list:
            st.info("Aktif destek yok.")
        else:
            for d in aktif_list:
                info = _KORUYUCU_FAKTORLER.get(d.get("faktor",""), {"ikon":"📋","renk":"#94a3b8"})
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {info['renk']};border-radius:0 12px 12px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">
                            {info['ikon']} {d.get('ogrenci','')}</span>
                        <span style="color:{info['renk']};font-weight:700;font-size:0.78rem;">{d.get('faktor','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        Sorumlu: {d.get('sorumlu','')} | {d.get('baslangic','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    # ── KORUYUCU SKOR ──
    with sub[2]:
        styled_section("Ogrenci Koruyucu Faktor Skoru")
        ogr2 = _ogr_sec("kf_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            ogr_destek = [d for d in destek_kayitlari if d.get("ogrenci") == ogr_ad2 and d.get("durum") == "Aktif"]

            toplam_etki = sum(_KORUYUCU_FAKTORLER.get(d.get("faktor",""), {}).get("etki", 0) for d in ogr_destek)
            skor = min(100, toplam_etki)
            renk = "#10b981" if skor >= 60 else "#f59e0b" if skor >= 30 else "#ef4444"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,{renk}15);border:2px solid {renk};
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad2}</div>
                <div style="color:{renk};font-weight:900;font-size:2.5rem;margin-top:6px;">{skor}/100</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Koruyucu Faktor Skoru | {len(ogr_destek)} aktif destek</div>
            </div>""", unsafe_allow_html=True)

            for d in ogr_destek:
                info = _KORUYUCU_FAKTORLER.get(d.get("faktor",""), {"ikon":"📋","renk":"#94a3b8","etki":0})
                st.markdown(f"  {info['ikon']} **{d.get('faktor','')}** — etki: +{info['etki']} puan")

    # ── ETKİNLİK ÖLÇÜMÜ ──
    with sub[3]:
        styled_section("Mudahale Etkinlik Olcumu")
        if not destek_kayitlari:
            st.info("Destek verisi yok.")
        else:
            faktor_say = Counter(d.get("faktor","") for d in destek_kayitlari)
            for faktor, sayi in faktor_say.most_common():
                info = _KORUYUCU_FAKTORLER.get(faktor, {"ikon":"📋","renk":"#94a3b8"})
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="font-size:1rem;">{info['ikon']}</span>
                    <span style="min-width:160px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{faktor}</span>
                    <span style="color:{info['renk']};font-weight:700;">{sayi} atama</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. AI DROPOUT TAHMİN & PROAKTİF MÜDAHALE
# ════════════════════════════════════════════════════════════

def render_dropout_tahmin(store, loader):
    """AI Dropout Tahmin — okul terk riski, what-if, mevsimsel risk takvimi."""
    styled_section("AI Dropout Tahmin & Proaktif Mudahale", "#dc2626")
    styled_info_banner(
        "Devamsizlik trendi, not dususu, davranis olaylari ve sosyo-duygusal "
        "veriden okul terk riski (dropout) tahmini. What-if senaryolari.",
        banner_type="warning", icon="🔮")

    tahminler = _lj("dropout_tahminler.json")
    students = load_shared_students()

    sub = st.tabs(["🔮 Bireysel Tahmin", "🗺️ Sinif Risk Haritasi", "🔄 What-If", "📅 Mevsimsel Takvim"])

    # ── BİREYSEL TAHMİN ──
    with sub[0]:
        styled_section("Ogrenci Dropout Risk Tahmini")
        ogr = _ogr_sec("dt_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            # Basit risk hesaplama (gercek uygulamada cross-module veri kullanilir)
            destek = _lj("koruyucu_faktorler.json")
            alarmlar = _lj("escalation_alarmlar.json")

            ogr_alarm = sum(1 for a in alarmlar if a.get("ogrenci") == ogr_ad)
            ogr_destek = sum(1 for d in destek if d.get("ogrenci") == ogr_ad and d.get("durum") == "Aktif")

            # Risk skoru (0-100)
            base_risk = 15 + ogr_alarm * 12 - ogr_destek * 8
            risk = max(0, min(100, base_risk + random.randint(-5, 10)))
            risk_renk = "#dc2626" if risk >= 50 else "#ef4444" if risk >= 30 else "#f59e0b" if risk >= 15 else "#10b981"
            risk_label = "Cok Yuksek" if risk >= 50 else "Yuksek" if risk >= 30 else "Orta" if risk >= 15 else "Dusuk"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a0a0a,{risk_renk}15);border:2px solid {risk_renk};
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Dropout Risk Tahmini</div>
                <div style="color:{risk_renk};font-weight:900;font-size:3rem;margin-top:8px;">%{risk}</div>
                <div style="color:{risk_renk};font-weight:700;font-size:0.9rem;">{risk_label} Risk</div>
                <div style="color:#64748b;font-size:0.7rem;margin-top:6px;">
                    Alarm: {ogr_alarm} | Destek: {ogr_destek} aktif</div>
            </div>""", unsafe_allow_html=True)

            # Risk faktorleri
            if risk >= 15:
                styled_section("Risk Faktorleri")
                gosterilen = random.sample(_DROPOUT_RISK_FAKTORLERI, min(3, len(_DROPOUT_RISK_FAKTORLERI)))
                for rf in gosterilen:
                    st.markdown(f"""
                    <div style="padding:5px 12px;margin:2px 0;border-left:3px solid {risk_renk};
                        background:{risk_renk}08;border-radius:0 8px 8px 0;">
                        <span style="color:#fca5a5;font-size:0.78rem;">⚠️ {rf}</span>
                    </div>""", unsafe_allow_html=True)

            # Kaydet
            if st.button("Tahmini Kaydet", key="dt_kaydet"):
                tahminler.append({
                    "ogrenci": ogr_ad, "risk": risk, "label": risk_label,
                    "alarm_sayi": ogr_alarm, "destek_sayi": ogr_destek,
                    "tarih": date.today().isoformat(),
                })
                _sj("dropout_tahminler.json", tahminler)
                st.success("Tahmin kaydedildi!")

    # ── SINIF RİSK HARİTASI ──
    with sub[1]:
        styled_section("Sinif Bazli Dropout Risk Haritasi")
        if not students:
            st.info("Ogrenci yok.")
        else:
            ss = get_sinif_sube_listesi()
            sec_s = st.selectbox("Sinif", ["Tumu"] + ss.get("siniflar", []), key="dt_sinif")
            filtered = students if sec_s == "Tumu" else [s for s in students if str(s.get("sinif","")) == sec_s]

            risk_list = []
            for s in filtered[:40]:
                ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
                alarm_s = sum(1 for a in _lj("escalation_alarmlar.json") if a.get("ogrenci") == ogr_ad)
                destek_s = sum(1 for d in _lj("koruyucu_faktorler.json") if d.get("ogrenci") == ogr_ad and d.get("durum") == "Aktif")
                risk = max(0, min(100, 15 + alarm_s * 12 - destek_s * 8 + random.randint(-3, 5)))
                risk_list.append({"ad": ogr_ad, "sinif": f"{s.get('sinif','')}/{s.get('sube','')}", "risk": risk})

            risk_list.sort(key=lambda x: x["risk"], reverse=True)

            yuksek = sum(1 for r in risk_list if r["risk"] >= 30)
            orta = sum(1 for r in risk_list if 15 <= r["risk"] < 30)
            dusuk = sum(1 for r in risk_list if r["risk"] < 15)

            styled_stat_row([
                ("Yuksek Risk", str(yuksek), "#ef4444", "🔴"),
                ("Orta Risk", str(orta), "#f59e0b", "🟡"),
                ("Dusuk Risk", str(dusuk), "#10b981", "🟢"),
            ])

            for r in risk_list[:20]:
                renk = "#dc2626" if r["risk"] >= 50 else "#ef4444" if r["risk"] >= 30 else "#f59e0b" if r["risk"] >= 15 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{r['ad']}</span>
                    <span style="color:#64748b;font-size:0.65rem;">{r['sinif']}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.72rem;">%{r['risk']}</span>
                </div>""", unsafe_allow_html=True)

    # ── WHAT-IF ──
    with sub[2]:
        styled_section("What-If Mudahale Senaryolari")
        ogr2 = _ogr_sec("dt_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            alarm_s = sum(1 for a in _lj("escalation_alarmlar.json") if a.get("ogrenci") == ogr_ad2)
            destek_s = sum(1 for d in _lj("koruyucu_faktorler.json") if d.get("ogrenci") == ogr_ad2 and d.get("durum") == "Aktif")
            mevcut_risk = max(0, min(100, 15 + alarm_s * 12 - destek_s * 8))

            st.markdown(f"**{ogr_ad2}** — Mevcut risk: **%{mevcut_risk}**")

            senaryolar = []
            for faktor, info in _KORUYUCU_FAKTORLER.items():
                yeni_risk = max(0, mevcut_risk - info["etki"])
                azalma = mevcut_risk - yeni_risk
                senaryolar.append((faktor, info, yeni_risk, azalma))

            senaryolar.sort(key=lambda x: x[3], reverse=True)

            for faktor, info, yeni, azalma in senaryolar:
                renk = "#10b981" if azalma >= 12 else "#3b82f6" if azalma >= 8 else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1rem;">{info['ikon']}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{faktor}</span>
                    <span style="color:#ef4444;font-size:0.72rem;">%{mevcut_risk}</span>
                    <span style="color:#94a3b8;">→</span>
                    <span style="color:#10b981;font-weight:800;font-size:0.78rem;">%{yeni}</span>
                    <span style="color:{renk};font-size:0.65rem;font-weight:700;">(-{azalma})</span>
                </div>""", unsafe_allow_html=True)

    # ── MEVSIMSEL TAKVİM ──
    with sub[3]:
        styled_section("Mevsimsel Risk Takvimi")
        for ay, risk_aciklama in _MEVSIM_RISK.items():
            is_bu_ay = ay.lower()[:3] == date.today().strftime("%B").lower()[:3]
            renk = "#c9a84c" if is_bu_ay else "#334155"
            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                padding:8px 14px;margin:4px 0;{'border:1px solid #c9a84c;' if is_bu_ay else ''}">
                <span style="color:{'#c9a84c' if is_bu_ay else '#e2e8f0'};font-weight:{'900' if is_bu_ay else '600'};
                    font-size:0.85rem;">{'📌 ' if is_bu_ay else ''}{ay}</span>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">⚠️ {risk_aciklama}</div>
            </div>""", unsafe_allow_html=True)
