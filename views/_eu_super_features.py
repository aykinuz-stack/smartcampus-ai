"""
Erken Uyarı — Süper Özellikler
================================
1. Zorbalık & Dijital Güvenlik Erken Tespit
2. Geçiş Dönemi Risk Yönetimi & Uyum Takip
3. Davranış Tarama & Psikometrik Erken Uyarı
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

_ZORBALIK_TURLERI = ["Fiziksel Zorbalik", "Sozel Zorbalik", "Sosyal Dislama", "Siber Zorbalik",
    "Esya Alma/Bozma", "Tehdit/Siddet", "Cinsel Taciz", "Diger"]
_ZORBALIK_RENK = {"Fiziksel Zorbalik": "#ef4444", "Sozel Zorbalik": "#f59e0b", "Sosyal Dislama": "#8b5cf6",
    "Siber Zorbalik": "#3b82f6", "Esya Alma/Bozma": "#6366f1", "Tehdit/Siddet": "#dc2626",
    "Cinsel Taciz": "#dc2626", "Diger": "#94a3b8"}
_ZORBALIK_DURUMLARI = ["Bildirildi", "Inceleniyor", "Mudahale Yapildi", "Cozuldu", "Izleniyor"]

_GECIS_TURLERI = ["Ilkokuldan Ortaokula", "Ortaokuldan Liseye", "Okul Degisikligi",
    "Goc/Multeci Uyum", "Ozel Egitim Gecisi", "Yurt Disindan Donus"]
_UYUM_GOSTERGELERI = ["Devamsizlik", "Not Degisimi", "Sosyal Iliski", "Okula Aidiyet",
    "Ders Katilim", "Davranis Uyum", "Veli Geri Bildirim"]

_SDQ_ALANLARI = {
    "Duygusal Sorunlar": {"ikon": "😢", "renk": "#8b5cf6", "sorular": [
        "Sik sik basagrilari/karni agrilari olur", "Cok endiselidir", "Sik sik mutsuz/aglamaklıdır",
        "Yeni durumlarda korkak/guvensizdir", "Kolay korkar"]},
    "Davranis Sorunlari": {"ikon": "😤", "renk": "#ef4444", "sorular": [
        "Sik sik ofke nöbetleri olur", "Genellikle sozu dinlemez", "Sik sik kavga eder",
        "Sik sik yalan soyledigine rastlanir", "Calar veya zorbalik yapar"]},
    "Hiperaktivite": {"ikon": "⚡", "renk": "#f59e0b", "sorular": [
        "Yerinde duramaz", "Surekli kipirdanir", "Kolay dikkat dagilir",
        "Eyleme gecmeden dusunmez", "Basladigi isi bitiremez"]},
    "Akran Sorunlari": {"ikon": "👥", "renk": "#3b82f6", "sorular": [
        "Genellikle yalniz oynar", "En az bir iyi arkadasi yoktur",
        "Yasitiyla gecinsiz", "Diger cocuklar tarafindan itilir", "Buyuklerle daha iyi gecinir"]},
    "Prososyal Davranis": {"ikon": "🤝", "renk": "#10b981", "sorular": [
        "Baskalarinin duygularini dikkate alir", "Gönüllü olarak paylaşır",
        "Uzgun birine yardim etmeye calisir", "Kucuklere karsi naziktir", "Genellikle gonullu yardim eder"]},
}


# ════════════════════════════════════════════════════════════
# 1. ZORBALIK & DİJİTAL GÜVENLİK ERKEN TESPİT
# ════════════════════════════════════════════════════════════

def render_zorbalik_tespit(store, loader):
    """Zorbalık & Dijital Güvenlik — anonim ihbar, takip, fail-mağdur profili."""
    styled_section("Zorbalik & Dijital Guvenlik Erken Tespit", "#dc2626")
    styled_info_banner(
        "Akran zorbaligi, siber zorbalik, sosyal dislama risk taramasi. "
        "Anonim ihbar kutusu, tekrarlayan olay tespiti, magdur-fail profili.",
        banner_type="warning", icon="🛡️")

    bildirimler = _lj("zorbalik_bildirimler.json")
    anonim = _lj("anonim_ihbar.json")

    aktif = sum(1 for b in bildirimler if b.get("durum") in ("Bildirildi", "Inceleniyor"))
    siber = sum(1 for b in bildirimler if b.get("tur") == "Siber Zorbalik")
    bu_ay = sum(1 for b in bildirimler if b.get("tarih","")[:7] == date.today().strftime("%Y-%m"))

    styled_stat_row([
        ("Aktif Vaka", str(aktif), "#dc2626", "🔴"),
        ("Siber Zorbalik", str(siber), "#3b82f6", "💻"),
        ("Bu Ay", str(bu_ay), "#f59e0b", "📅"),
        ("Anonim Ihbar", str(len(anonim)), "#8b5cf6", "📩"),
    ])

    sub = st.tabs(["📝 Bildirim", "📩 Anonim Ihbar", "📋 Vaka Takip", "📊 Analiz", "🛡️ Siber Guvenlik"])

    with sub[0]:
        styled_section("Zorbalik Bildirimi")
        with st.form("zb_form"):
            c1, c2 = st.columns(2)
            with c1:
                z_magdur = _ogr_sec("zb_mag")
                z_tur = st.selectbox("Zorbalik Turu", _ZORBALIK_TURLERI, key="zb_tur")
                z_tarih = st.date_input("Olay Tarihi", key="zb_tarih")
            with c2:
                z_fail = st.text_input("Fail (varsa)", key="zb_fail")
                z_konum = st.text_input("Olay Yeri", key="zb_konum")
                z_tanik = st.text_input("Taniklar", key="zb_tanik")
            z_aciklama = st.text_area("Olay Aciklamasi", height=60, key="zb_acik")
            z_tekrar = st.checkbox("Tekrarlayan olay mi?", key="zb_tekrar")

            if st.form_submit_button("Bildir", use_container_width=True, type="primary"):
                if z_magdur:
                    bildirimler.append({
                        "id": f"zb_{uuid.uuid4().hex[:8]}",
                        "magdur": f"{z_magdur.get('ad','')} {z_magdur.get('soyad','')}",
                        "sinif": f"{z_magdur.get('sinif','')}/{z_magdur.get('sube','')}",
                        "fail": z_fail, "tur": z_tur, "konum": z_konum,
                        "tanik": z_tanik, "aciklama": z_aciklama,
                        "tekrar": z_tekrar, "durum": "Bildirildi",
                        "tarih": z_tarih.isoformat(), "created_at": datetime.now().isoformat(),
                    })
                    _sj("zorbalik_bildirimler.json", bildirimler)
                    st.error(f"Zorbalik bildirimi kaydedildi — {'TEKRARLAYAN!' if z_tekrar else ''}")
                    st.rerun()

    with sub[1]:
        styled_section("Anonim Ihbar Kutusu")
        st.caption("Kimlik bilgisi istenmez — guvenli sekilde bildirim yapin.")
        with st.form("anonim_form"):
            a_mesaj = st.text_area("Ihbariniz", height=80, key="an_mesaj",
                placeholder="Okulda yasadiginiz veya gordugu bir olayi guvenle bildirebilirsiniz...")
            a_sinif = st.text_input("Sinif (opsiyonel)", key="an_sinif")

            if st.form_submit_button("Anonim Gonder", use_container_width=True):
                if a_mesaj:
                    anonim.append({
                        "id": f"an_{uuid.uuid4().hex[:8]}",
                        "mesaj": a_mesaj, "sinif": a_sinif,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("anonim_ihbar.json", anonim)
                    st.success("Ihbariniz anonim olarak kaydedildi. Tesekkurler!")
                    st.rerun()

        if anonim:
            styled_section(f"Anonim Ihbarlar ({len(anonim)})")
            for a in sorted(anonim, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="background:#8b5cf610;border:1px solid #8b5cf630;border-left:4px solid #8b5cf6;
                    border-radius:0 10px 10px 0;padding:10px 14px;margin:5px 0;">
                    <span style="color:#c4b5fd;font-weight:700;font-size:0.78rem;">📩 Anonim</span>
                    <span style="color:#64748b;font-size:0.65rem;float:right;">{a.get('tarih','')[:10]}</span>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:4px;">{a.get('mesaj','')[:120]}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Vaka Takip")
        if not bildirimler:
            st.success("Bildirim yok.")
        else:
            for b in sorted(bildirimler, key=lambda x: x.get("tarih",""), reverse=True):
                renk = _ZORBALIK_RENK.get(b.get("tur",""), "#94a3b8")
                d_renk = {"Bildirildi":"#ef4444","Inceleniyor":"#f59e0b","Mudahale Yapildi":"#3b82f6",
                    "Cozuldu":"#10b981","Izleniyor":"#8b5cf6"}.get(b.get("durum",""),"#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 12px 12px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#fca5a5;font-weight:800;font-size:0.85rem;">{b.get('tur','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{b.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        Magdur: {b.get('magdur','')} | Fail: {b.get('fail','-')} | {b.get('tarih','')[:10]}
                        {'| ⚠️ TEKRARLAYAN' if b.get('tekrar') else ''}</div>
                </div>""", unsafe_allow_html=True)
                with st.expander(f"Durum: {b.get('id','')}", expanded=False):
                    yeni = st.selectbox("Durum", _ZORBALIK_DURUMLARI,
                        index=_ZORBALIK_DURUMLARI.index(b.get("durum","Bildirildi")) if b.get("durum") in _ZORBALIK_DURUMLARI else 0,
                        key=f"zb_d_{b['id']}")
                    if st.button("Guncelle", key=f"zb_g_{b['id']}"):
                        b["durum"] = yeni
                        _sj("zorbalik_bildirimler.json", bildirimler)
                        st.rerun()

    with sub[3]:
        styled_section("Zorbalik Analizi")
        if bildirimler:
            tur_say = Counter(b.get("tur","") for b in bildirimler)
            for tur, sayi in tur_say.most_common():
                renk = _ZORBALIK_RENK.get(tur, "#94a3b8")
                pct = round(sayi / max(len(bildirimler), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                    <span style="min-width:140px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{tur}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi} (%{pct})</span></div></div>
                </div>""", unsafe_allow_html=True)

            tekrar_say = sum(1 for b in bildirimler if b.get("tekrar"))
            if tekrar_say:
                st.error(f"⚠️ {tekrar_say} tekrarlayan zorbalik vakasi — oncelikli mudahale gerekli!")

    with sub[4]:
        styled_section("Siber Guvenlik Farkindalik")
        ipuclari = [
            ("🔒 Sifre Guvenligi", "Guclu sifre kullan, kimseyle paylasma"),
            ("📱 Sosyal Medya", "Ozel bilgilerini paylasma, tanımadıgın kisiyi kabul etme"),
            ("📸 Gorsel Paylasim", "Izinsiz fotograf/video paylasma, ekran goruntusu alma"),
            ("💬 Mesajlasma", "Kırıcı mesaj gonderme, gruplarda dislama yapma"),
            ("🚫 Siber Zorbalık", "Birisini gorursen ogretmenine/ailene soyle"),
            ("🛡️ Gizlilik", "Konum bilgini kapatmali, profili gizli tutmali"),
        ]
        for baslik, aciklama in ipuclari:
            st.markdown(f"""
            <div style="background:#3b82f608;border:1px solid #3b82f630;border-left:4px solid #3b82f6;
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <span style="color:#93c5fd;font-weight:700;font-size:0.82rem;">{baslik}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. GEÇİŞ DÖNEMİ RİSK YÖNETİMİ & UYUM TAKİP
# ════════════════════════════════════════════════════════════

def render_gecis_donemi(store, loader):
    """Geçiş Dönemi Risk — kademe geçişi, göçmen uyum, adaptasyon izleme."""
    styled_section("Gecis Donemi Risk Yonetimi & Uyum Takip", "#f59e0b")
    styled_info_banner(
        "Kademe gecislerinde risk takibi. Ilk 3 ay adaptasyon izleme, "
        "gocmen/multeci uyum, aile yapisi risk faktorleri.",
        banner_type="info", icon="🔀")

    gecis_kayitlari = _lj("gecis_donemi.json")
    uyum_kayitlari = _lj("uyum_takip.json")

    styled_stat_row([
        ("Gecis Kaydi", str(len(gecis_kayitlari)), "#f59e0b", "🔀"),
        ("Uyum Takip", str(len(uyum_kayitlari)), "#3b82f6", "📊"),
    ])

    sub = st.tabs(["➕ Gecis Kaydi", "📊 Uyum Degerlendirme", "📋 Takip Listesi", "⚠️ Risk Faktorleri"])

    with sub[0]:
        styled_section("Yeni Gecis Kaydi")
        with st.form("gecis_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("gd_ogr")
                g_tur = st.selectbox("Gecis Turu", _GECIS_TURLERI, key="gd_tur")
            with c2:
                g_tarih = st.date_input("Gecis Tarihi", key="gd_tarih")
                g_onceki = st.text_input("Onceki Okul/Kademe", key="gd_onceki")
            g_risk = st.multiselect("Risk Faktorleri",
                ["Aile parcalanmasi", "Ekonomik zorluk", "Goc/multeci", "Dil bariyeri",
                 "Ozel egitim ihtiyaci", "Travma/yas", "Sosyal izolasyon", "Akademik gecikme"],
                key="gd_risk")
            g_not = st.text_area("Not", height=50, key="gd_not")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if ogr:
                    gecis_kayitlari.append({
                        "id": f"gd_{uuid.uuid4().hex[:8]}",
                        "ogrenci": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif": f"{ogr.get('sinif','')}/{ogr.get('sube','')}",
                        "tur": g_tur, "onceki": g_onceki,
                        "risk_faktorleri": g_risk, "not": g_not,
                        "tarih": g_tarih.isoformat(), "created_at": datetime.now().isoformat(),
                    })
                    _sj("gecis_donemi.json", gecis_kayitlari)
                    st.success(f"Gecis kaydi olusturuldu! ({len(g_risk)} risk faktoru)")
                    st.rerun()

    with sub[1]:
        styled_section("Uyum Degerlendirmesi (Ilk 3 Ay)")
        if not gecis_kayitlari:
            st.info("Gecis kaydi yok.")
        else:
            sec = st.selectbox("Ogrenci",
                [f"{g.get('ogrenci','')} ({g.get('tur','')})" for g in gecis_kayitlari], key="gd_uyum")

            with st.form("uyum_form"):
                puanlar = {}
                for gosterge in _UYUM_GOSTERGELERI:
                    puanlar[gosterge] = st.slider(gosterge, 1, 10, 5, key=f"uy_{gosterge}")

                if st.form_submit_button("Degerlendir", use_container_width=True):
                    ort = round(sum(puanlar.values()) / max(len(puanlar), 1), 1)
                    uyum_kayitlari.append({
                        "ogrenci": sec, "puanlar": puanlar, "ortalama": ort,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("uyum_takip.json", uyum_kayitlari)
                    renk = "#10b981" if ort >= 7 else "#f59e0b" if ort >= 5 else "#ef4444"
                    durum = "Iyi Uyum" if ort >= 7 else "Dikkat" if ort >= 5 else "Risk"
                    st.success(f"Uyum: {ort}/10 — {durum}")

    with sub[2]:
        styled_section("Gecis Takip Listesi")
        for g in sorted(gecis_kayitlari, key=lambda x: x.get("tarih",""), reverse=True):
            risk_say = len(g.get("risk_faktorleri", []))
            renk = "#ef4444" if risk_say >= 3 else "#f59e0b" if risk_say >= 1 else "#10b981"
            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                padding:10px 14px;margin:5px 0;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">🔀 {g.get('ogrenci','')}</span>
                    <span style="color:{renk};font-size:0.7rem;font-weight:700;">{risk_say} risk</span>
                </div>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                    {g.get('tur','')} | {g.get('onceki','')} → {g.get('sinif','')} | {g.get('tarih','')[:10]}</div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Aile Yapisi & Gecis Risk Faktorleri")
        if gecis_kayitlari:
            risk_say = Counter()
            for g in gecis_kayitlari:
                for r in g.get("risk_faktorleri", []):
                    risk_say[r] += 1
            for risk, sayi in risk_say.most_common():
                st.markdown(f"  - ⚠️ **{risk}**: {sayi} ogrenci")
        else:
            st.info("Gecis verisi yok.")


# ════════════════════════════════════════════════════════════
# 3. DAVRANIŞ TARAMA & PSİKOMETRİK ERKEN UYARI
# ════════════════════════════════════════════════════════════

def render_davranis_tarama(store, loader):
    """Davranış Tarama — SDQ benzeri tarama, sınıf risk haritası, yönlendirme."""
    styled_section("Davranis Tarama & Psikometrik Erken Uyari", "#8b5cf6")
    styled_info_banner(
        "Yilda 2 kez toplu davranis taramasi (SDQ benzeri). "
        "Depresyon/kaygi/davranis bozuklugu erken tespiti, sinif risk haritasi.",
        banner_type="info", icon="📊")

    taramalar = _lj("davranis_tarama.json")

    styled_stat_row([
        ("Tarama", str(len(taramalar)), "#8b5cf6", "📊"),
        ("Alan", str(len(_SDQ_ALANLARI)), "#3b82f6", "📐"),
    ])

    sub = st.tabs(["📝 Tarama Uygula", "📊 Sonuc Analizi", "🗺️ Sinif Haritasi", "🔔 Yonlendirme Listesi"])

    with sub[0]:
        styled_section("SDQ Davranis Taramasi (Guclukler & Gucler)")
        ogr = _ogr_sec("dt_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            with st.form("sdq_form"):
                alan_puanlar = {}
                for alan, info in _SDQ_ALANLARI.items():
                    st.markdown(f"**{info['ikon']} {alan}**")
                    alan_toplam = 0
                    for soru in info["sorular"]:
                        p = st.radio(soru, ["Dogru Degil (0)", "Biraz Dogru (1)", "Kesinlikle Dogru (2)"],
                            horizontal=True, key=f"sdq_{alan}_{soru[:15]}")
                        puan_map = {"Dogru Degil (0)": 0, "Biraz Dogru (1)": 1, "Kesinlikle Dogru (2)": 2}
                        alan_toplam += puan_map.get(p, 0)
                    alan_puanlar[alan] = alan_toplam

                if st.form_submit_button("Taramayi Tamamla", use_container_width=True, type="primary"):
                    # Toplam zorluk skoru (Prososyal haric)
                    zorluk = sum(v for k, v in alan_puanlar.items() if k != "Prososyal Davranis")
                    prososyal = alan_puanlar.get("Prososyal Davranis", 0)

                    # Klinik esik: zorluk >= 17 = anormal, 14-16 = sinirda
                    if zorluk >= 17:
                        seviye, s_renk = "Anormal", "#dc2626"
                    elif zorluk >= 14:
                        seviye, s_renk = "Sinirda", "#f59e0b"
                    else:
                        seviye, s_renk = "Normal", "#10b981"

                    taramalar.append({
                        "id": f"sdq_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "sinif": f"{ogr.get('sinif','')}/{ogr.get('sube','')}",
                        "alan_puanlar": alan_puanlar,
                        "zorluk_toplam": zorluk, "prososyal": prososyal,
                        "seviye": seviye,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("davranis_tarama.json", taramalar)

                    st.markdown(f"""
                    <div style="background:{s_renk}15;border:2px solid {s_renk};border-radius:16px;
                        padding:20px;text-align:center;margin:10px 0;">
                        <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">{ogr_ad}</div>
                        <div style="color:{s_renk};font-weight:900;font-size:2rem;margin-top:6px;">{zorluk}/40</div>
                        <div style="color:{s_renk};font-weight:700;font-size:0.9rem;">{seviye}</div>
                        <div style="color:#64748b;font-size:0.72rem;margin-top:4px;">Prososyal: {prososyal}/10</div>
                    </div>""", unsafe_allow_html=True)
                    st.rerun()

    with sub[1]:
        styled_section("Tarama Sonuc Analizi")
        if not taramalar:
            st.info("Tarama verisi yok.")
        else:
            for t in sorted(taramalar, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                sev = t.get("seviye","?")
                s_renk = "#dc2626" if sev == "Anormal" else "#f59e0b" if sev == "Sinirda" else "#10b981"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {s_renk};border-radius:0 12px 12px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{t.get('ogrenci','')}</span>
                        <span style="background:{s_renk}20;color:{s_renk};padding:2px 10px;border-radius:8px;
                            font-size:0.72rem;font-weight:800;">{sev} ({t.get('zorluk_toplam',0)}/40)</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">{t.get('sinif','')} | {t.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                # Alan detay
                with st.expander(f"Alan Detay: {t.get('ogrenci','')}", expanded=False):
                    for alan, puan in t.get("alan_puanlar", {}).items():
                        info = _SDQ_ALANLARI.get(alan, {"ikon":"","renk":"#94a3b8"})
                        max_p = 10
                        pct = round(puan / max_p * 100)
                        # Prososyal icin ters: yuksek = iyi
                        if alan == "Prososyal Davranis":
                            renk = "#10b981" if puan >= 6 else "#f59e0b" if puan >= 4 else "#ef4444"
                        else:
                            renk = "#ef4444" if puan >= 7 else "#f59e0b" if puan >= 5 else "#10b981"
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                            <span style="font-size:0.9rem;">{info['ikon']}</span>
                            <span style="min-width:130px;color:#e2e8f0;font-size:0.75rem;font-weight:600;">{alan}</span>
                            <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                                <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                            </div>
                            <span style="color:{renk};font-size:0.68rem;font-weight:700;">{puan}/{max_p}</span>
                        </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Sinif Bazli Tarama Haritasi")
        if not taramalar:
            st.info("Tarama verisi yok.")
        else:
            seviye_say = Counter(t.get("seviye","") for t in taramalar)
            normal = seviye_say.get("Normal", 0)
            sinirda = seviye_say.get("Sinirda", 0)
            anormal = seviye_say.get("Anormal", 0)

            styled_stat_row([
                ("Normal", str(normal), "#10b981", "🟢"),
                ("Sinirda", str(sinirda), "#f59e0b", "🟡"),
                ("Anormal", str(anormal), "#ef4444", "🔴"),
            ])

            if anormal > 0:
                st.error(f"🔴 {anormal} ogrenci klinik esik ustunde — bireysel degerlendirme gerekli!")

    with sub[3]:
        styled_section("Yonlendirme Listesi")
        yonlendir = [t for t in taramalar if t.get("seviye") in ("Anormal", "Sinirda")]
        if not yonlendir:
            st.success("Yonlendirme gerektiren ogrenci yok.")
        else:
            st.warning(f"{len(yonlendir)} ogrenci icin yonlendirme onerilir:")
            for t in sorted(yonlendir, key=lambda x: x.get("zorluk_toplam",0), reverse=True):
                sev = t.get("seviye","")
                renk = "#dc2626" if sev == "Anormal" else "#f59e0b"
                oneri = "Bireysel degerlendirme + RAM yonlendirme" if sev == "Anormal" else "Yakin izleme + rehberlik gorusmesi"
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.85rem;">
                        {'🔴' if sev == 'Anormal' else '🟡'} {t.get('ogrenci','')}</span>
                    <span style="color:#64748b;font-size:0.68rem;margin-left:8px;">{t.get('sinif','')}</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:4px;">
                        Skor: {t.get('zorluk_toplam',0)}/40 | Oneri: {oneri}</div>
                </div>""", unsafe_allow_html=True)
