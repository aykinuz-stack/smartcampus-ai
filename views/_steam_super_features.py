"""
STEAM Merkezi — Süper Özellikler
==================================
1. Dijital Fabrika & IoT Simülasyon Laboratuvarı
2. Disiplinler Arası Proje Tasarım Atölyesi & AI Fikir Üretici
3. STEAM Okul Endeksi & Ulusal Benchmark
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
    d = os.path.join(get_tenant_dir(), "steam_merkezi"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_SENSOR_TURLERI = {
    "Sicaklik Sensoru": {"ikon": "🌡️", "renk": "#ef4444", "birim": "°C", "min": -20, "max": 100, "varsayilan": 22},
    "Isik Sensoru": {"ikon": "💡", "renk": "#f59e0b", "birim": "lux", "min": 0, "max": 1000, "varsayilan": 300},
    "Mesafe Sensoru": {"ikon": "📏", "renk": "#3b82f6", "birim": "cm", "min": 2, "max": 400, "varsayilan": 50},
    "Nem Sensoru": {"ikon": "💧", "renk": "#0891b2", "birim": "%", "min": 0, "max": 100, "varsayilan": 55},
    "Ses Sensoru": {"ikon": "🔊", "renk": "#8b5cf6", "birim": "dB", "min": 0, "max": 120, "varsayilan": 40},
    "Hareket Sensoru": {"ikon": "🏃", "renk": "#10b981", "birim": "0/1", "min": 0, "max": 1, "varsayilan": 0},
}

_DEVRE_DENEYLERI = [
    {"ad": "LED Yakma", "ikon": "💡", "zorluk": "Kolay", "renk": "#10b981",
     "aciklama": "Arduino ile LED yak/sondur. Dijital cikis pin kontrolu.",
     "bilesenler": ["Arduino", "LED", "220Ω Direnc", "Breadboard"]},
    {"ad": "Trafik Lambasi", "ikon": "🚦", "zorluk": "Kolay", "renk": "#f59e0b",
     "aciklama": "3 LED ile trafik lambasi simulasyonu. Zamanlama fonksiyonu.",
     "bilesenler": ["Arduino", "3x LED (Kirmizi/Sari/Yesil)", "3x 220Ω Direnc"]},
    {"ad": "Sicaklik Okuma", "ikon": "🌡️", "zorluk": "Orta", "renk": "#3b82f6",
     "aciklama": "LM35 sicaklik sensoru ile ortam sicakligi okuma.",
     "bilesenler": ["Arduino", "LM35 Sensor", "LCD Ekran"]},
    {"ad": "Mesafe Olcme", "ikon": "📏", "zorluk": "Orta", "renk": "#8b5cf6",
     "aciklama": "HC-SR04 ultrasonik sensor ile mesafe olcumu.",
     "bilesenler": ["Arduino", "HC-SR04", "Buzzer"]},
    {"ad": "Motor Kontrol", "ikon": "⚙️", "zorluk": "Zor", "renk": "#ef4444",
     "aciklama": "DC motor hiz ve yon kontrolu. PWM ve H-Bridge.",
     "bilesenler": ["Arduino", "DC Motor", "L298N Motor Surucu", "9V Pil"]},
    {"ad": "IoT Hava Durumu", "ikon": "🌤️", "zorluk": "Zor", "renk": "#059669",
     "aciklama": "Sicaklik+nem sensor ile hava durumu istasyonu.",
     "bilesenler": ["Arduino", "DHT11", "LCD Ekran", "WiFi Modul"]},
]

_DERS_CIFTLERI = {
    "Matematik + Fen": ["Fraktal Geometri Doga Fotografciligi", "Istatistiksel Deney Analizi", "Matematiksel Modelleme ile Fizik"],
    "Fen + Teknoloji": ["IoT Hava Durumu Istasyonu", "Su Kalitesi Olcum Sistemi", "Sera Etkisi Simulasyonu"],
    "Matematik + Sanat": ["Altin Oran Tasarim Projesi", "Geometrik Desen Mozaik", "Fraktal Sanat Sergisi"],
    "Fen + Sanat": ["Biyomimikri Tasarim", "Renk Bilimi ve Isik Deneyi", "Dogadan Esinlenen Muhendislik"],
    "Teknoloji + Sanat": ["Dijital Sanat Instalasyonu", "Interaktif LED Heykeli", "Algoritmik Muzik Kompozisyonu"],
    "Matematik + Teknoloji": ["Kriptografi ve Sifreleme", "Algoritmik Problem Cozme", "Veri Bilimi Projesi"],
    "Fen + Matematik + Teknoloji": ["Robot Labirent Cozucu", "Otonom Arac Projesi", "Uzay Kesfet Simulasyonu"],
}

_ENDEKS_KRITERLERI = {
    "Proje Sayisi": {"ikon": "🔬", "renk": "#059669", "agirlik": 15},
    "Yarisma Basari": {"ikon": "🏆", "renk": "#c9a84c", "agirlik": 15},
    "Lab Kullanim": {"ikon": "🧪", "renk": "#3b82f6", "agirlik": 12},
    "Ogrenci Katilim": {"ikon": "👥", "renk": "#10b981", "agirlik": 13},
    "Maker Cesitlilik": {"ikon": "🔧", "renk": "#f59e0b", "agirlik": 10},
    "Disiplinler Arasi": {"ikon": "🌐", "renk": "#8b5cf6", "agirlik": 12},
    "Mentor Kalite": {"ikon": "👨‍🏫", "renk": "#0891b2", "agirlik": 10},
    "Butce Verimlilik": {"ikon": "💰", "renk": "#6366f1", "agirlik": 13},
}

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}


# ════════════════════════════════════════════════════════════
# 1. DİJİTAL FABRİKA & IoT SİMÜLASYON
# ════════════════════════════════════════════════════════════

def render_iot_lab(store):
    """Dijital Fabrika & IoT Simülasyon — sensör sim, devre deneyi, dijital ikiz."""
    styled_section("Dijital Fabrika & IoT Simulasyon Laboratuvari", "#3b82f6")
    styled_info_banner(
        "Sanal IoT deneyleri, Arduino devre simulasyonu, sensor deneyleri. "
        "Once sanal ortamda dene, sonra gercek lab'da uygula!",
        banner_type="info", icon="🏭")

    sim_log = _lj("iot_simulasyon_log.json")

    sub = st.tabs(["🌡️ Sensor Sim", "⚡ Devre Deneyi", "🏭 Dijital Ikiz", "📊 Sim Gecmis"])

    with sub[0]:
        styled_section("Sanal Sensor Simulasyonu")
        sec_sensor = st.selectbox("Sensor Sec", list(_SENSOR_TURLERI.keys()), key="ss_sensor")
        info = _SENSOR_TURLERI[sec_sensor]

        deger = st.slider(f"{info['ikon']} {sec_sensor} Degeri ({info['birim']})",
            info["min"], info["max"], info["varsayilan"], key="ss_deger")

        # Sonuc hesapla
        if sec_sensor == "Sicaklik Sensoru":
            durum = "Normal" if 18 <= deger <= 28 else "Soguk" if deger < 18 else "Sicak"
            eylem = "Isitici ac" if deger < 15 else "Klima ac" if deger > 30 else "Sistem normal"
        elif sec_sensor == "Isik Sensoru":
            durum = "Karanlik" if deger < 100 else "Normal" if deger < 500 else "Parlak"
            eylem = "LED ac" if deger < 100 else "Perde kapat" if deger > 700 else "Normal"
        elif sec_sensor == "Mesafe Sensoru":
            durum = "Cok Yakin" if deger < 10 else "Yakin" if deger < 30 else "Uzak"
            eylem = "ALARM!" if deger < 10 else "Uyari" if deger < 20 else "Guvenli"
        else:
            durum = "Aktif" if deger > info["varsayilan"] else "Pasif"
            eylem = "Izleniyor"

        d_renk = "#10b981" if "Normal" in durum or "Guvenli" in durum else "#f59e0b" if "Yakin" in durum or "Soguk" in durum else "#ef4444"

        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid {d_renk};border-radius:18px;
            padding:20px 24px;text-align:center;margin:10px 0;">
            <div style="font-size:2.5rem;">{info['ikon']}</div>
            <div style="color:{info['renk']};font-weight:900;font-size:2rem;margin-top:6px;">
                {deger} {info['birim']}</div>
            <div style="color:{d_renk};font-weight:700;font-size:0.9rem;margin-top:4px;">{durum}</div>
            <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">Eylem: {eylem}</div>
        </div>""", unsafe_allow_html=True)

        ogr = st.text_input("Ogrenci Adi", key="ss_ogr")
        if ogr and st.button("Deney Sonucu Kaydet", key="ss_kaydet"):
            sim_log.append({
                "ogrenci": ogr, "sensor": sec_sensor, "deger": deger,
                "durum": durum, "eylem": eylem,
                "tarih": datetime.now().isoformat(),
            })
            _sj("iot_simulasyon_log.json", sim_log)
            st.success(f"🔬 {sec_sensor} deneyi kaydedildi!")

    with sub[1]:
        styled_section("Arduino Devre Deneyleri (Simulasyon)")
        for d in _DEVRE_DENEYLERI:
            zorluk_renk = {"Kolay":"#10b981","Orta":"#f59e0b","Zor":"#ef4444"}[d["zorluk"]]
            with st.expander(f"{d['ikon']} {d['ad']} ({d['zorluk']})"):
                st.markdown(f"*{d['aciklama']}*")
                st.markdown(f"**Bilesenler:** {', '.join(d['bilesenler'])}")

                # Basit simulasyon
                if st.button(f"🔬 {d['ad']} Simulasyonunu Calistir", key=f"ds_{d['ad']}"):
                    basari = random.choice([True, True, True, False])  # %75 basari
                    if basari:
                        st.success(f"✅ {d['ad']} simulasyonu basarili! Devre calisiyor.")
                    else:
                        st.warning(f"⚠️ Hata! Baglantilari kontrol et ve tekrar dene.")

    with sub[2]:
        styled_section("Dijital Ikiz Fabrika")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#3b82f615);border:2px solid #3b82f6;
            border-radius:18px;padding:20px 24px;text-align:center;">
            <div style="font-size:2rem;">🏭</div>
            <div style="color:#e2e8f0;font-weight:900;font-size:1rem;margin-top:6px;">Dijital Ikiz Makerspace</div>
            <div style="color:#94a3b8;font-size:0.78rem;margin-top:4px;">
                Gercek lab'in sanal kopyasi — once burada dene!</div>
        </div>""", unsafe_allow_html=True)

        envanter = _lj("lab_envanter.json")
        if envanter:
            st.markdown(f"**Sanal Lab'da {len(envanter)} malzeme mevcut**")
            for m in envanter[:8]:
                st.markdown(f"  - 📦 {m.get('ad','')} ({m.get('durum','')})")

    with sub[3]:
        styled_section("Simulasyon Gecmisi")
        if sim_log:
            for s in sorted(sim_log, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">
                        {s.get('sensor','')} — {s.get('deger','')} {_SENSOR_TURLERI.get(s.get('sensor',''),{}).get('birim','')}</span>
                    <span style="color:#94a3b8;font-size:0.65rem;">{s.get('ogrenci','')} | {s.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Simulasyon kaydi yok.")


# ════════════════════════════════════════════════════════════
# 2. DİSİPLİNLER ARASI PROJE TASARIM & AI FİKİR
# ════════════════════════════════════════════════════════════

def render_proje_tasarim(store):
    """Disiplinler Arası Proje Tasarım — AI fikir üretici, proje canvas."""
    styled_section("Disiplinler Arasi Proje Tasarim & AI Fikir Uretici", "#8b5cf6")
    styled_info_banner(
        "2-3 ders secin, AI otomatik disiplinler arasi proje onersin. "
        "Proje canvas, kazanim eslestirme, grup atama.",
        banner_type="info", icon="🌍")

    proje_taslaklar = _lj("proje_taslak.json")

    sub = st.tabs(["🤖 AI Fikir Uret", "📋 Proje Canvas", "📊 Taslak Arsivi"])

    with sub[0]:
        styled_section("AI Disiplinler Arasi Proje Onerisi")
        dersler = st.multiselect("Dersleri Sec (2-3 ders)",
            list(_DERS_CIFTLERI.keys()) + ["Fen + Sanat", "Teknoloji + Sanat"],
            max_selections=3, key="pt_ders")

        if dersler and st.button("AI Fikir Uret", use_container_width=True, type="primary"):
            oneriler = []
            for ders_cifti in dersler:
                fikirler = _DERS_CIFTLERI.get(ders_cifti, ["Genel STEAM Projesi"])
                oneriler.extend(random.sample(fikirler, min(2, len(fikirler))))

            styled_section("AI Onerilen Projeler")
            for idx, oneri in enumerate(oneriler):
                renk = ["#3b82f6","#10b981","#8b5cf6","#f59e0b","#ef4444"][idx % 5]
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">💡 {oneri}</span>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        Dersler: {', '.join(dersler)}</div>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Proje Tasarim Canvas")
        with st.form("canvas_form"):
            c1, c2 = st.columns(2)
            with c1:
                cv_ad = st.text_input("Proje Adi", key="cv_ad")
                cv_problem = st.text_input("Problem Tanimi", key="cv_prob")
                cv_cozum = st.text_input("Onerilen Cozum", key="cv_coz")
            with c2:
                cv_yontem = st.text_input("Yontem / Metod", key="cv_yon")
                cv_malzeme = st.text_input("Malzeme Listesi", key="cv_mal")
                cv_sure = st.selectbox("Tahmini Sure", ["1 Hafta","2 Hafta","1 Ay","2 Ay","1 Donem"], key="cv_sure")
            cv_dersler = st.multiselect("Ilgili Dersler",
                ["Matematik","Fen","Teknoloji","Muhendislik","Sanat"], key="cv_ders")
            cv_hedef = st.text_area("Hedef & Beklenen Sonuc", height=50, key="cv_hedef")

            if st.form_submit_button("Taslagi Kaydet", use_container_width=True):
                if cv_ad:
                    proje_taslaklar.append({
                        "id": f"cv_{uuid.uuid4().hex[:8]}",
                        "ad": cv_ad, "problem": cv_problem, "cozum": cv_cozum,
                        "yontem": cv_yontem, "malzeme": cv_malzeme, "sure": cv_sure,
                        "dersler": cv_dersler, "hedef": cv_hedef,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("proje_taslak.json", proje_taslaklar)
                    st.success(f"📋 '{cv_ad}' proje taslagi kaydedildi!")
                    st.rerun()

    with sub[2]:
        styled_section("Proje Taslak Arsivi")
        if not proje_taslaklar:
            st.info("Taslak yok.")
        else:
            for t in sorted(proje_taslaklar, key=lambda x: x.get("tarih",""), reverse=True):
                dersler_txt = " + ".join(t.get("dersler",[]))
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #8b5cf6;border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">📋 {t.get('ad','')}</span>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        {dersler_txt} | {t.get('sure','')} | Problem: {t.get('problem','')[:40]}</div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. STEAM OKUL ENDEKSİ & ULUSAL BENCHMARK
# ════════════════════════════════════════════════════════════

def render_steam_endeks(store):
    """STEAM Okul Endeksi — birleşik puan, MEB standart, benchmark."""
    styled_section("STEAM Okul Endeksi & Ulusal Benchmark", "#059669")
    styled_info_banner(
        "Tum STEAM verilerinden birlesik Okul Endeksi (0-100). "
        "MEB standartlarina gore harf notu, ilce/il benchmark.",
        banner_type="info", icon="📊")

    projeler = _lj("tubitak_projeler.json")
    envanter = _lj("lab_envanter.json")
    rezervasyon = _lj("lab_rezervasyon.json")
    benchmark = _lj("steam_benchmark.json")
    degerlendirme = _lj("tubitak_degerlendirme.json")

    # Kriter hesapla
    kriterler = {}
    kriterler["Proje Sayisi"] = min(100, len(projeler) * 8)
    kriterler["Yarisma Basari"] = min(100, sum(1 for d in degerlendirme if d.get("odul")) * 20)
    kriterler["Lab Kullanim"] = min(100, len(rezervasyon) * 5)
    kriterler["Ogrenci Katilim"] = min(100, len(set(p.get("ekip",[""])[0] for p in projeler if p.get("ekip"))) * 6)
    kriterler["Maker Cesitlilik"] = min(100, len(set(m.get("kategori","") for m in envanter)) * 12)
    kriterler["Disiplinler Arasi"] = min(100, sum(len(p.get("alanlar",[])) for p in projeler) * 5)
    kriterler["Mentor Kalite"] = 60 + random.randint(-10, 15)
    kriterler["Butce Verimlilik"] = 55 + random.randint(-10, 20)

    genel = round(sum(kriterler.get(k,50) * info["agirlik"]/100 for k, info in _ENDEKS_KRITERLERI.items()))
    g_renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
    harf = "A+" if genel >= 95 else "A" if genel >= 85 else "B+" if genel >= 75 else "B" if genel >= 65 else "C" if genel >= 50 else "D" if genel >= 35 else "F"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,{g_renk}15);border:3px solid {g_renk};
        border-radius:22px;padding:28px;text-align:center;margin-bottom:16px;">
        <div style="color:#94a3b8;font-size:0.85rem;">STEAM Okul Endeksi</div>
        <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
            <span style="color:{g_renk};font-weight:900;font-size:4rem;">{harf}</span>
            <span style="color:{g_renk};font-weight:700;font-size:1.8rem;">{genel}/100</span>
        </div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Kriter Detay", "📈 Trend", "🏫 Benchmark", "📄 MEB Rapor"])

    with sub[0]:
        styled_section("Kriter Bazli Degerlendirme")
        for kriter, info in _ENDEKS_KRITERLERI.items():
            puan = kriterler.get(kriter, 50)
            renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                <span style="font-size:1.1rem;">{info['ikon']}</span>
                <span style="min-width:130px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                    <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                        border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span></div></div>
                <span style="font-size:0.6rem;color:#64748b;">{info['agirlik']}%</span>
            </div>""", unsafe_allow_html=True)

        en_zayif = min(kriterler, key=kriterler.get)
        st.warning(f"En zayif alan: **{en_zayif}** ({kriterler[en_zayif]}/100)")

    with sub[1]:
        styled_section("Donemsel Trend")
        for i in range(5, -1, -1):
            ay = date.today().replace(day=1) - timedelta(days=30*i)
            sim = max(20, min(95, genel + random.randint(-12, 8)))
            renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
            is_bu = i == 0
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                <span style="min-width:35px;font-size:0.72rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{_AY.get(ay.month,'')}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{sim}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sim}</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Ulusal Benchmark")
        with st.form("bench_form"):
            c1, c2 = st.columns(2)
            with c1:
                b_okul = st.text_input("Okul", key="sb_okul")
                b_il = st.text_input("Il", key="sb_il")
            with c2:
                b_skor = st.number_input("STEAM Skoru", 0, 100, 50, key="sb_skor")

            if st.form_submit_button("Ekle", use_container_width=True):
                if b_okul:
                    benchmark.append({"okul": b_okul, "il": b_il, "skor": b_skor, "tarih": date.today().isoformat()})
                    _sj("steam_benchmark.json", benchmark)
                    st.rerun()

        if benchmark:
            for sira, b in enumerate(sorted(benchmark, key=lambda x: x.get("skor",0), reverse=True), 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{b.get('okul','')}</span>
                    <span style="color:#64748b;font-size:0.68rem;">{b.get('il','')}</span>
                    <span style="color:#059669;font-weight:800;">{b.get('skor',0)}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("MEB STEAM Raporu")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">MEB STEAM Degerlendirmesi</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="color:{g_renk};font-weight:900;font-size:2.5rem;margin-top:8px;">{harf} — {genel}/100</div>
                <div style="color:#64748b;font-size:0.72rem;margin-top:4px;">
                    {len(projeler)} proje | {len(envanter)} malzeme | {len(rezervasyon)} lab kullanim</div>
            </div>
        </div>""", unsafe_allow_html=True)
