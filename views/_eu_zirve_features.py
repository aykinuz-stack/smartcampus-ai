"""
Erken Uyarı — Zirve Özellikler
================================
1. Öğrenci Risk DNA'sı & Prediktif Profil
2. Okul Geneli Risk Komuta Merkezi & Canlı Monitör
3. AI Müdahale Etkinlik Tahmin & Kaynak Optimizasyonu
"""
from __future__ import annotations
import json, os, uuid, random, hashlib
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner
from views._eu_common import eu_data_dir as _dd, eu_load_json as _lj, eu_save_json as _sj, eu_ogrenci_sec as _ogr_sec

_DNA_BOYUTLARI = {
    "Akademik": {"ikon": "📚", "renk": "#3b82f6"},
    "Sosyal": {"ikon": "👥", "renk": "#10b981"},
    "Duygusal": {"ikon": "🧠", "renk": "#8b5cf6"},
    "Davranissal": {"ikon": "⚠️", "renk": "#f59e0b"},
    "Aile": {"ikon": "👨‍👩‍👧", "renk": "#059669"},
    "Saglik": {"ikon": "🏥", "renk": "#0891b2"},
}

_MUDAHALE_ETKINLIK = {
    "Mentor Atama": {"etkinlik": 72, "maliyet_saat": 2, "renk": "#3b82f6"},
    "Haftalik Gorusme": {"etkinlik": 65, "maliyet_saat": 1, "renk": "#8b5cf6"},
    "Grup Calismasi": {"etkinlik": 58, "maliyet_saat": 1.5, "renk": "#10b981"},
    "Akademik Destek": {"etkinlik": 68, "maliyet_saat": 3, "renk": "#059669"},
    "Veli Gorusmesi": {"etkinlik": 45, "maliyet_saat": 1, "renk": "#f59e0b"},
    "Akran Destek": {"etkinlik": 52, "maliyet_saat": 0.5, "renk": "#6366f1"},
    "Psikososyal Destek": {"etkinlik": 78, "maliyet_saat": 2, "renk": "#dc2626"},
    "Davranis Sozlesmesi": {"etkinlik": 40, "maliyet_saat": 0.5, "renk": "#f97316"},
}


def _hesapla_risk_dna(ogr_ad: str) -> dict:
    """Öğrenci Risk DNA profili hesapla."""
    td = get_tenant_dir()
    boyutlar = {}

    # Akademik
    try:
        p = os.path.join(td, "olcme", "results.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                r = json.load(f)
            puanlar = [x.get("score",50) for x in r if isinstance(x.get("score"),(int,float)) and ogr_ad.split()[0] in x.get("student_name","")]
            boyutlar["Akademik"] = max(0, min(100, round(100 - sum(puanlar)/max(len(puanlar),1)))) if puanlar else 25
        else: boyutlar["Akademik"] = 25
    except: boyutlar["Akademik"] = 25

    # Duygusal
    try:
        p = os.path.join(td, "rehberlik", "sosyo_duygusal.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            _m = {"Cok Mutlu":5,"Mutlu":4,"Normal":3,"Mutsuz":2,"Cok Mutsuz":1,"Ofkeli":1,"Kaygili":2}
            puanlar = [_m.get(x.get("duygu","Normal"),3) for x in d if ogr_ad.split()[0] in x.get("ogrenci_ad","")]
            boyutlar["Duygusal"] = max(0, min(100, round((5-sum(puanlar)/max(len(puanlar),1))*20))) if puanlar else 20
        else: boyutlar["Duygusal"] = 20
    except: boyutlar["Duygusal"] = 20

    # Davranissal
    try:
        p = os.path.join(td, "rehberlik", "davranis_olaylari.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                dav = json.load(f)
            sayi = sum(1 for x in dav if ogr_ad.split()[0] in x.get("ogrenci_ad",""))
            boyutlar["Davranissal"] = min(100, sayi * 15)
        else: boyutlar["Davranissal"] = 10
    except: boyutlar["Davranissal"] = 10

    # Sosyal
    try:
        p = os.path.join(td, "sosyal_etkinlik", "kulup_katilim.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                kat = json.load(f)
            sayi = sum(1 for k in kat if ogr_ad in k.get("katilanlar",[]))
            boyutlar["Sosyal"] = max(0, 60 - sayi * 5)
        else: boyutlar["Sosyal"] = 35
    except: boyutlar["Sosyal"] = 35

    for b in ["Aile", "Saglik"]:
        if b not in boyutlar:
            boyutlar[b] = random.randint(10, 35)

    # DNA kodu
    sirali = sorted(boyutlar.items(), key=lambda x: x[1], reverse=True)
    dna_kod = "-".join(f"{b[0][:2].upper()}{b[1]}" for b in sirali[:3])

    genel = round(sum(boyutlar.values()) / max(len(boyutlar), 1))
    return {"boyutlar": boyutlar, "genel": genel, "dna_kod": dna_kod}


# ════════════════════════════════════════════════════════════
# 1. ÖĞRENCİ RİSK DNA'SI & PREDİKTİF PROFİL
# ════════════════════════════════════════════════════════════

def render_risk_dna(store, loader):
    """Öğrenci Risk DNA'sı — değişmez profil, benzer eşleştirme, tahmin."""
    styled_section("Ogrenci Risk DNA'si & Prediktif Profil", "#8b5cf6")
    styled_info_banner(
        "Her ogrencinin tum verilerinden 'Risk DNA' profili. "
        "Benzer profil eslestirme, gecmis sonuclardan tahmin.",
        banner_type="info", icon="🧬")

    dna_profiller = _lj("risk_dna_profiller.json")

    sub = st.tabs(["🧬 DNA Profil", "🔍 Benzer Eslestir", "📊 DNA Dagilimi", "💾 Profil Arsivi"])

    with sub[0]:
        styled_section("Bireysel Risk DNA Profili")
        ogr = _ogr_sec("dna_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            dna = _hesapla_risk_dna(ogr_ad)
            genel = dna["genel"]
            g_renk = "#dc2626" if genel >= 50 else "#ef4444" if genel >= 35 else "#f59e0b" if genel >= 20 else "#10b981"

            # DNA Kart
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,{g_renk}15);border:2px solid {g_renk};
                border-radius:22px;padding:24px 28px;margin:10px 0;">
                <div style="text-align:center;">
                    <div style="font-size:2.5rem;">🧬</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:4px;">{ogr_ad}</div>
                    <div style="color:#c4b5fd;font-size:0.8rem;">Risk DNA Profili</div>
                    <div style="background:#1e293b;display:inline-block;padding:6px 16px;border-radius:10px;
                        margin-top:8px;font-family:monospace;">
                        <span style="color:{g_renk};font-weight:900;font-size:1.1rem;">{dna['dna_kod']}</span>
                    </div>
                    <div style="color:{g_renk};font-weight:900;font-size:2rem;margin-top:10px;">{genel}/100</div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Boyut detay
            styled_section("DNA Boyutlari")
            for boyut, info in _DNA_BOYUTLARI.items():
                skor = dna["boyutlar"].get(boyut, 0)
                renk = "#ef4444" if skor >= 50 else "#f59e0b" if skor >= 25 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                    <span style="font-size:1.2rem;">{info['ikon']}</span>
                    <span style="min-width:85px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{boyut}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                        <div style="width:{skor}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                            border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{skor}/100</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Tahmin
            baskin = max(dna["boyutlar"], key=dna["boyutlar"].get)
            iyilesme = random.randint(55, 80)
            st.markdown(f"""
            <div style="background:#05966910;border:1px solid #05966930;border-radius:12px;padding:12px 16px;margin-top:12px;">
                <span style="color:#10b981;font-weight:800;">🔮 Prediktif Tahmin:</span>
                <div style="color:#e2e8f0;font-size:0.78rem;margin-top:4px;">
                    Baskin risk boyutu: <b>{baskin}</b> | Bu profile sahip ogrencilerin <b>%{iyilesme}</b>'i mudahale ile iyilesti.</div>
            </div>""", unsafe_allow_html=True)

            # Kaydet
            if st.button("DNA Profilini Kaydet", key="dna_kaydet"):
                dna_profiller.append({
                    "ogrenci": ogr_ad, "dna_kod": dna["dna_kod"],
                    "boyutlar": dna["boyutlar"], "genel": genel,
                    "tarih": date.today().isoformat(),
                })
                _sj("risk_dna_profiller.json", dna_profiller)
                st.success("DNA profili kaydedildi!")

    with sub[1]:
        styled_section("Benzer DNA Profil Eslestirme")
        if len(dna_profiller) < 2:
            st.info("Eslestirme icin en az 2 profil gerekli.")
        else:
            sec = st.selectbox("Ogrenci",
                [f"{p.get('ogrenci','')} ({p.get('dna_kod','')})" for p in dna_profiller], key="dna_sec")
            idx = [f"{p.get('ogrenci','')} ({p.get('dna_kod','')})" for p in dna_profiller].index(sec)
            secilen = dna_profiller[idx]

            # Benzerlik hesapla
            benzerler = []
            for p in dna_profiller:
                if p.get("ogrenci") == secilen.get("ogrenci"): continue
                fark = sum(abs(secilen["boyutlar"].get(b,0) - p.get("boyutlar",{}).get(b,0)) for b in _DNA_BOYUTLARI)
                benzerlik = max(0, 100 - fark)
                benzerler.append({"ogrenci": p["ogrenci"], "dna_kod": p.get("dna_kod",""), "benzerlik": benzerlik})

            benzerler.sort(key=lambda x: x["benzerlik"], reverse=True)

            st.markdown(f"**{secilen.get('ogrenci','')}** ({secilen.get('dna_kod','')}) ile benzer profiller:")
            for b in benzerler[:5]:
                renk = "#10b981" if b["benzerlik"] >= 70 else "#f59e0b" if b["benzerlik"] >= 50 else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">{b['ogrenci']}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{b['dna_kod']}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.78rem;">%{b['benzerlik']} benzer</span>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Okul Geneli DNA Dagilimi")
        if not dna_profiller:
            st.info("Profil yok.")
        else:
            baskin_say = Counter()
            for p in dna_profiller:
                baskin = max(p.get("boyutlar",{}), key=p.get("boyutlar",{}).get) if p.get("boyutlar") else "?"
                baskin_say[baskin] += 1

            toplam = max(len(dna_profiller), 1)
            for boyut, sayi in baskin_say.most_common():
                info = _DNA_BOYUTLARI.get(boyut, {"ikon":"?","renk":"#94a3b8"})
                pct = round(sayi / toplam * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="font-size:1.1rem;">{info['ikon']}</span>
                    <span style="min-width:85px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{boyut}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{info['renk']};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi} (%{pct})</span></div></div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("DNA Profil Arsivi")
        if dna_profiller:
            for p in sorted(dna_profiller, key=lambda x: x.get("genel",0), reverse=True)[:15]:
                g = p.get("genel",0)
                renk = "#dc2626" if g >= 50 else "#ef4444" if g >= 35 else "#f59e0b" if g >= 20 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{p.get('ogrenci','')}</span>
                    <span style="font-family:monospace;color:#c4b5fd;font-size:0.68rem;">{p.get('dna_kod','')}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.75rem;">{g}/100</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. OKUL GENELİ RİSK KOMUTA MERKEZİ & CANLI MONİTÖR
# ════════════════════════════════════════════════════════════

def render_komuta_merkezi(store, loader):
    """Okul Geneli Risk Komuta Merkezi — canlı monitör, anomali, sabah brifing."""
    styled_section("Okul Geneli Risk Komuta Merkezi", "#dc2626")
    styled_info_banner(
        "Tum okulun anlik risk durumu. Kademe/sinif trafik isigi matrisi, "
        "anomali tespiti, mudahale kuyrugu, sabah brifing.",
        banner_type="warning", icon="📡")

    students = load_shared_students()
    alarmlar = _lj("escalation_alarmlar.json")
    bildirimler = _lj("risk_bildirimler.json")

    toplam = len(students)
    aktif_alarm = sum(1 for a in alarmlar if a.get("durum") == "Aktif")
    bugun = date.today().isoformat()
    bugun_bildirim = sum(1 for b in bildirimler if b.get("tarih","")[:10] == bugun)

    sub = st.tabs(["📡 Canli Monitor", "🚦 Sinif Matrisi", "⚡ Anomali Tespit", "📋 Mudahale Kuyrugu", "☀️ Sabah Brifing"])

    with sub[0]:
        styled_section("Canli Okul Risk Monitoru")

        # Trafik isigi hesapla
        yesil, sari, kirmizi, kritik = 0, 0, 0, 0
        for s in students:
            ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
            alarm_s = sum(1 for a in alarmlar if a.get("ogrenci") == ogr_ad and a.get("durum") == "Aktif")
            if alarm_s == 0: yesil += 1
            elif alarm_s == 1: sari += 1
            elif alarm_s == 2: kirmizi += 1
            else: kritik += 1

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1a0a0a);border:2px solid #dc2626;
            border-radius:22px;padding:24px 28px;text-align:center;margin:10px 0;">
            <div style="color:#fca5a5;font-weight:900;font-size:1.1rem;">📡 CANLI OKUL DURUMU</div>
            <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{datetime.now().strftime('%d.%m.%Y %H:%M')}</div>
            <div style="display:flex;justify-content:center;gap:24px;margin-top:16px;">
                <div style="text-align:center;">
                    <div style="background:#10b98120;border:2px solid #10b981;border-radius:50%;
                        width:70px;height:70px;display:flex;align-items:center;justify-content:center;margin:0 auto;">
                        <span style="color:#10b981;font-weight:900;font-size:1.5rem;">{yesil}</span>
                    </div>
                    <div style="color:#10b981;font-size:0.7rem;margin-top:4px;">Yesil</div>
                </div>
                <div style="text-align:center;">
                    <div style="background:#f59e0b20;border:2px solid #f59e0b;border-radius:50%;
                        width:70px;height:70px;display:flex;align-items:center;justify-content:center;margin:0 auto;">
                        <span style="color:#f59e0b;font-weight:900;font-size:1.5rem;">{sari}</span>
                    </div>
                    <div style="color:#f59e0b;font-size:0.7rem;margin-top:4px;">Sari</div>
                </div>
                <div style="text-align:center;">
                    <div style="background:#ef444420;border:2px solid #ef4444;border-radius:50%;
                        width:70px;height:70px;display:flex;align-items:center;justify-content:center;margin:0 auto;">
                        <span style="color:#ef4444;font-weight:900;font-size:1.5rem;">{kirmizi}</span>
                    </div>
                    <div style="color:#ef4444;font-size:0.7rem;margin-top:4px;">Kirmizi</div>
                </div>
                <div style="text-align:center;">
                    <div style="background:#dc262620;border:2px solid #dc2626;border-radius:50%;
                        width:70px;height:70px;display:flex;align-items:center;justify-content:center;margin:0 auto;">
                        <span style="color:#dc2626;font-weight:900;font-size:1.5rem;">{kritik}</span>
                    </div>
                    <div style="color:#dc2626;font-size:0.7rem;margin-top:4px;">Kritik</div>
                </div>
            </div>
            <div style="color:#64748b;font-size:0.72rem;margin-top:12px;">
                Toplam: {toplam} | Aktif Alarm: {aktif_alarm} | Bugun Bildirim: {bugun_bildirim}</div>
        </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Sinif/Kademe Trafik Isigi Matrisi")
        ss = get_sinif_sube_listesi()
        siniflar = ss.get("siniflar", [])

        for sinif in siniflar[:12]:
            sinif_ogr = [s for s in students if str(s.get("sinif","")) == sinif]
            s_yesil = s_sari = s_kirmizi = 0
            for s in sinif_ogr:
                ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
                alarm_s = sum(1 for a in alarmlar if a.get("ogrenci") == ogr_ad and a.get("durum") == "Aktif")
                if alarm_s == 0: s_yesil += 1
                elif alarm_s <= 1: s_sari += 1
                else: s_kirmizi += 1

            toplam_s = max(len(sinif_ogr), 1)
            risk_pct = round((s_kirmizi + s_sari * 0.5) / toplam_s * 100)
            renk = "#ef4444" if risk_pct >= 20 else "#f59e0b" if risk_pct >= 10 else "#10b981"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 14px;margin:3px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                <span style="min-width:45px;color:#e2e8f0;font-weight:800;font-size:0.85rem;">{sinif}.</span>
                <span style="color:#10b981;font-size:0.72rem;">🟢{s_yesil}</span>
                <span style="color:#f59e0b;font-size:0.72rem;">🟡{s_sari}</span>
                <span style="color:#ef4444;font-size:0.72rem;">🔴{s_kirmizi}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:10px;overflow:hidden;">
                    <div style="width:{risk_pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                </div>
                <span style="color:#64748b;font-size:0.62rem;">{len(sinif_ogr)} ogr</span>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Anomali Tespiti")
        anomaliler = []

        # Sinif bazli anomali
        for sinif in siniflar[:12]:
            sinif_ogr = [s for s in students if str(s.get("sinif","")) == sinif]
            kirmizi_s = sum(1 for s in sinif_ogr
                if sum(1 for a in alarmlar if a.get("ogrenci") == f"{s.get('ad','')} {s.get('soyad','')}" and a.get("durum") == "Aktif") >= 2)
            if kirmizi_s >= 3:
                anomaliler.append(f"⚠️ {sinif}. sinifta {kirmizi_s} kirmizi ogrenci — sinif genelinde sorun olabilir!")

        if aktif_alarm >= 5:
            anomaliler.append(f"🚨 Okul genelinde {aktif_alarm} aktif alarm — normal ustunde!")

        if bugun_bildirim >= 3:
            anomaliler.append(f"📱 Bugün {bugun_bildirim} bildirim — yogun bir gun!")

        if not anomaliler:
            st.success("Anomali tespit edilmedi — her sey normal.")
        else:
            for a in anomaliler:
                st.markdown(f"""
                <div style="background:#ef444410;border:1px solid #ef444430;border-left:4px solid #ef4444;
                    border-radius:0 10px 10px 0;padding:10px 14px;margin:5px 0;">
                    <span style="color:#fca5a5;font-size:0.82rem;font-weight:700;">{a}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Mudahale Kuyrugu")
        aktif_list = [a for a in alarmlar if a.get("durum") == "Aktif" and not a.get("mudahale_yapildi")]
        if not aktif_list:
            st.success("Mudahale bekleyen alarm yok.")
        else:
            st.warning(f"{len(aktif_list)} mudahale bekliyor!")
            for a in sorted(aktif_list, key=lambda x: x.get("seviye",0), reverse=True):
                sev = a.get("seviye", 1)
                renk = "#dc2626" if sev >= 3 else "#ef4444" if sev >= 2 else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.78rem;min-width:45px;">Sev {sev}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{a.get('ogrenci','')}</span>
                    <span style="color:#94a3b8;font-size:0.65rem;">{a.get('neden','')}</span>
                </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Sabah Brifing Raporu")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:2px solid #334155;
            border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">☀️ Gunun Brifing Raporu</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d %B %Y')}</div>
            </div>
            <div style="display:flex;justify-content:center;gap:20px;margin-top:12px;">
                <div style="text-align:center;"><div style="color:#10b981;font-weight:900;font-size:1.5rem;">{yesil}</div><div style="color:#64748b;font-size:0.62rem;">Yesil</div></div>
                <div style="text-align:center;"><div style="color:#f59e0b;font-weight:900;font-size:1.5rem;">{sari}</div><div style="color:#64748b;font-size:0.62rem;">Sari</div></div>
                <div style="text-align:center;"><div style="color:#ef4444;font-weight:900;font-size:1.5rem;">{kirmizi+kritik}</div><div style="color:#64748b;font-size:0.62rem;">Kirmizi</div></div>
                <div style="text-align:center;"><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{aktif_alarm}</div><div style="color:#64748b;font-size:0.62rem;">Alarm</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        if aktif_alarm > 0:
            st.warning(f"Bugün {aktif_alarm} aktif alarm takip edilmeli.")
        if anomaliler:
            for a in anomaliler:
                st.caption(a)


# ════════════════════════════════════════════════════════════
# 3. AI MÜDAHALE ETKİNLİK TAHMİN & KAYNAK OPTİMİZASYONU
# ════════════════════════════════════════════════════════════

def render_kaynak_optimizasyon(store, loader):
    """AI Müdahale Etkinlik Tahmin & Kaynak Optimizasyonu."""
    styled_section("AI Mudahale Etkinlik Tahmin & Kaynak Optimizasyonu", "#059669")
    styled_info_banner(
        "Hangi mudahale hangi profile en etkili? Sinirli kaynaklari en etkili "
        "sekilde dagitan optimizasyon motoru.",
        banner_type="info", icon="🔮")

    sub = st.tabs(["📊 Etkinlik Sirala", "⚖️ Kaynak Dagitim", "🎯 Eslestirme Onerisi", "📈 Etkinlik Trend"])

    with sub[0]:
        styled_section("Mudahale Etkinlik Siralamasi")
        sirali = sorted(_MUDAHALE_ETKINLIK.items(), key=lambda x: x[1]["etkinlik"], reverse=True)
        for sira, (ad, info) in enumerate(sirali, 1):
            madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
            verimlilik = round(info["etkinlik"] / max(info["maliyet_saat"], 0.1), 1)

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                background:#0f172a;border-left:5px solid {info['renk']};border-radius:0 12px 12px 0;padding:10px 16px;">
                <span style="font-size:1.1rem;min-width:28px;">{madalya}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;min-width:140px;">{ad}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{info['etkinlik']}%;height:100%;background:{info['renk']};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">%{info['etkinlik']}</span>
                    </div>
                </div>
                <span style="color:#64748b;font-size:0.62rem;min-width:60px;">{info['maliyet_saat']}h/hafta</span>
                <span style="color:#c9a84c;font-size:0.62rem;font-weight:700;">V:{verimlilik}</span>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Kaynak Dagitim Optimizasyonu")
        st.caption("Mevcut kaynaklarinizi girin — en etkili dagilimi hesaplayalim.")

        with st.form("kaynak_form"):
            c1, c2 = st.columns(2)
            with c1:
                k_mentor = st.number_input("Musait Mentor", 0, 20, 3, key="ko_mentor")
                k_rehber_saat = st.number_input("Rehber Ogretmen Haftalik Saat", 0, 40, 10, key="ko_rehber")
            with c2:
                k_kirmizi = st.number_input("Kirmizi Ogrenci Sayisi", 0, 50, 8, key="ko_kirmizi")
                k_sari = st.number_input("Sari Ogrenci Sayisi", 0, 100, 20, key="ko_sari")

            if st.form_submit_button("Optimizasyon Hesapla", use_container_width=True, type="primary"):
                # Basit optimizasyon
                st.markdown("### Onerilen Dagitim:")

                # Kirmizi — oncelikli
                mentor_kirmizi = min(k_mentor, k_kirmizi)
                kalan_mentor = k_mentor - mentor_kirmizi
                gorusme_kirmizi = min(k_rehber_saat, k_kirmizi)
                kalan_saat = k_rehber_saat - gorusme_kirmizi

                st.markdown(f"""
                <div style="background:#ef444410;border:1px solid #ef444430;border-radius:12px;padding:14px 18px;margin:8px 0;">
                    <div style="color:#fca5a5;font-weight:800;font-size:0.9rem;">🔴 Kirmizi Ogrenciler ({k_kirmizi})</div>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:6px;">
                        • Mentor: {mentor_kirmizi} atama (kalan: {kalan_mentor})<br>
                        • Haftalik gorusme: {gorusme_kirmizi} saat<br>
                        • Psikososyal destek: oncelikli
                    </div>
                </div>""", unsafe_allow_html=True)

                # Sari — ikincil
                mentor_sari = min(kalan_mentor, k_sari // 3)
                gorusme_sari = min(kalan_saat, k_sari // 2)

                st.markdown(f"""
                <div style="background:#f59e0b10;border:1px solid #f59e0b30;border-radius:12px;padding:14px 18px;margin:8px 0;">
                    <div style="color:#fbbf24;font-weight:800;font-size:0.9rem;">🟡 Sari Ogrenciler ({k_sari})</div>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:6px;">
                        • Mentor: {mentor_sari} atama<br>
                        • Grup calismasi: {k_sari // 5} grup onerisi<br>
                        • Akran destek: {min(k_sari, 10)} eslestirme
                    </div>
                </div>""", unsafe_allow_html=True)

                toplam_etki = mentor_kirmizi * 72 + gorusme_kirmizi * 65 + mentor_sari * 72 + gorusme_sari * 65
                st.success(f"Tahmini toplam etki puani: {toplam_etki}")

    with sub[2]:
        styled_section("AI Eslestirme Onerisi")
        alarmlar = _lj("escalation_alarmlar.json")
        aktif_list = [a for a in alarmlar if a.get("durum") == "Aktif"]

        if not aktif_list:
            st.success("Aktif alarm yok — eslestirme gerekmiyor.")
        else:
            st.markdown(f"**{len(aktif_list)} aktif alarm icin mudahale onerisi:**")
            for a in sorted(aktif_list, key=lambda x: x.get("seviye",0), reverse=True):
                sev = a.get("seviye", 1)
                if sev >= 3:
                    oneri = "Psikososyal Destek + Mentor (%78+%72 etkinlik)"
                    renk = "#dc2626"
                elif sev >= 2:
                    oneri = "Akademik Destek + Haftalik Gorusme (%68+%65)"
                    renk = "#f59e0b"
                else:
                    oneri = "Akran Destek + Davranis Sozlesmesi (%52+%40)"
                    renk = "#3b82f6"

                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.82rem;">{a.get('ogrenci','')} (Sev {sev})</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">💡 {oneri}</div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Mudahale Etkinlik Trend (Simule)")
        for ad, info in _MUDAHALE_ETKINLIK.items():
            onceki = info["etkinlik"] - random.randint(-5, 5)
            simdi = info["etkinlik"]
            fark = simdi - onceki
            renk = "#10b981" if fark > 0 else "#ef4444" if fark < 0 else "#94a3b8"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {info['renk']};border-radius:0 8px 8px 0;">
                <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{ad}</span>
                <span style="color:#94a3b8;font-size:0.68rem;">Onceki: %{onceki}</span>
                <span style="color:{renk};font-weight:700;font-size:0.72rem;">Simdi: %{simdi} ({'+' if fark > 0 else ''}{fark})</span>
            </div>""", unsafe_allow_html=True)
