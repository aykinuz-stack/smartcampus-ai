"""
Yabancı Dil — Süper Özellikler
================================
1. Dil Gelişim Cockpit & Öğretmen Kontrol Paneli
2. AI Konuşma Partneri & Günlük Diyalog Senaryoları
3. CEFR İlerleme Yol Haritası & Sertifika Hazırlık
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "yabanci_dil"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None

_CEFR = ["A1","A2","B1","B2","C1","C2"]
_CEFR_RENK = {"A1":"#ef4444","A2":"#f59e0b","B1":"#3b82f6","B2":"#10b981","C1":"#8b5cf6","C2":"#c9a84c"}
_CEFR_ACIKLAMA = {
    "A1": "Baslangic — temel ifadeler, kendini tanitma",
    "A2": "Temel — gunluk ifadeler, basit konusmalar",
    "B1": "Orta — seyahat, is, okul konulari",
    "B2": "Orta Ustu — akici konusma, karmasik metinler",
    "C1": "Ileri — akademik ve profesyonel yetkinlik",
    "C2": "Uzman — neredeyse anadil seviyesi",
}
_BECERILER = {
    "Listening": {"ikon": "👂", "renk": "#3b82f6"},
    "Speaking": {"ikon": "🗣️", "renk": "#10b981"},
    "Reading": {"ikon": "📖", "renk": "#8b5cf6"},
    "Writing": {"ikon": "✍️", "renk": "#f59e0b"},
    "Grammar": {"ikon": "📐", "renk": "#6366f1"},
    "Vocabulary": {"ikon": "📚", "renk": "#059669"},
}

_SENARYOLAR = [
    {"ad": "Restoran Siparisi", "ikon": "🍽️", "seviye": "A2", "renk": "#f59e0b",
     "diyalog": [
         ("Waiter", "Good evening! Welcome to our restaurant. Table for how many?"),
         ("You", "Table for two, please."),
         ("Waiter", "Right this way. Here's the menu. Can I get you something to drink?"),
         ("You", "I'd like a glass of water, please."),
         ("Waiter", "Are you ready to order?"),
         ("You", "Yes, I'll have the grilled chicken with salad, please."),
         ("Waiter", "Excellent choice! Anything for dessert?"),
         ("You", "Not right now, thank you."),
     ], "anahtar": ["Table for two", "I'd like", "I'll have", "please", "thank you"]},
    {"ad": "Havalimaninda", "ikon": "✈️", "seviye": "B1", "renk": "#3b82f6",
     "diyalog": [
         ("Agent", "Good morning. Passport and ticket, please."),
         ("You", "Here you are."),
         ("Agent", "How many bags are you checking in?"),
         ("You", "Just one suitcase."),
         ("Agent", "Window or aisle seat?"),
         ("You", "Window seat, please."),
         ("Agent", "Your gate is B12. Boarding starts at 2:30."),
         ("You", "Thank you. Where is the gate?"),
     ], "anahtar": ["Here you are", "Just one", "Window seat", "Where is"]},
    {"ad": "Alisveris", "ikon": "🛒", "seviye": "A2", "renk": "#10b981",
     "diyalog": [
         ("Clerk", "Hello! Can I help you?"),
         ("You", "Yes, I'm looking for a blue jacket."),
         ("Clerk", "What size do you need?"),
         ("You", "Medium, please."),
         ("Clerk", "Here you go. The fitting room is over there."),
         ("You", "How much is it?"),
         ("Clerk", "It's 49.99."),
         ("You", "I'll take it."),
     ], "anahtar": ["I'm looking for", "What size", "How much", "I'll take it"]},
    {"ad": "Doktorda", "ikon": "🏥", "seviye": "B1", "renk": "#ef4444",
     "diyalog": [
         ("Doctor", "What seems to be the problem?"),
         ("You", "I've had a headache for three days."),
         ("Doctor", "Do you have any other symptoms?"),
         ("You", "Yes, I feel tired and my throat is sore."),
         ("Doctor", "Let me check your temperature. It's 38.2."),
         ("You", "Is it serious?"),
         ("Doctor", "It looks like a common cold. I'll prescribe some medicine."),
         ("You", "Thank you, doctor."),
     ], "anahtar": ["I've had", "symptoms", "feel tired", "Is it serious"]},
    {"ad": "Otel Rezervasyonu", "ikon": "🏨", "seviye": "A2", "renk": "#8b5cf6",
     "diyalog": [
         ("Receptionist", "Good afternoon. How can I help you?"),
         ("You", "I'd like to book a room for two nights."),
         ("Receptionist", "Single or double?"),
         ("You", "Double room, please."),
         ("Receptionist", "That's 80 euros per night. Breakfast included."),
         ("You", "That sounds good. Do you accept credit cards?"),
     ], "anahtar": ["I'd like to book", "for two nights", "per night", "credit cards"]},
    {"ad": "Is Gorusmesi", "ikon": "💼", "seviye": "B2", "renk": "#6366f1",
     "diyalog": [
         ("Interviewer", "Tell me about yourself."),
         ("You", "I graduated from Istanbul University with a degree in computer science."),
         ("Interviewer", "What are your strengths?"),
         ("You", "I'm a quick learner and a good team player."),
         ("Interviewer", "Where do you see yourself in five years?"),
         ("You", "I see myself in a leadership role, contributing to innovative projects."),
     ], "anahtar": ["Tell me about", "graduated from", "strengths", "five years"]},
]

_SINAV_TURLERI = {
    "Cambridge (FCE/CAE)": {"seviye": "B2-C1", "beceri": ["Reading","Listening","Writing","Speaking","Use of English"], "sure_dk": 180},
    "IELTS": {"seviye": "B1-C2", "beceri": ["Listening","Reading","Writing","Speaking"], "sure_dk": 170},
    "TOEFL iBT": {"seviye": "B1-C1", "beceri": ["Reading","Listening","Speaking","Writing"], "sure_dk": 200},
    "YDS": {"seviye": "B2-C1", "beceri": ["Reading","Grammar","Vocabulary"], "sure_dk": 180},
    "YÖKDİL": {"seviye": "B2-C1", "beceri": ["Reading","Grammar","Vocabulary"], "sure_dk": 180},
}

_CEFR_HEDEFLER = {
    "A1": {"Vocabulary": 500, "Grammar": 20, "Listening_hr": 20, "Speaking_hr": 10, "Reading_hr": 15, "Writing_hr": 10},
    "A2": {"Vocabulary": 1000, "Grammar": 40, "Listening_hr": 40, "Speaking_hr": 25, "Reading_hr": 30, "Writing_hr": 20},
    "B1": {"Vocabulary": 2000, "Grammar": 60, "Listening_hr": 80, "Speaking_hr": 50, "Reading_hr": 60, "Writing_hr": 40},
    "B2": {"Vocabulary": 4000, "Grammar": 80, "Listening_hr": 150, "Speaking_hr": 100, "Reading_hr": 120, "Writing_hr": 80},
    "C1": {"Vocabulary": 8000, "Grammar": 95, "Listening_hr": 300, "Speaking_hr": 200, "Reading_hr": 250, "Writing_hr": 150},
    "C2": {"Vocabulary": 15000, "Grammar": 100, "Listening_hr": 500, "Speaking_hr": 400, "Reading_hr": 500, "Writing_hr": 300},
}


# ════════════════════════════════════════════════════════════
# 1. DİL GELİŞİM COCKPİT & ÖĞRETMEN KONTROL PANELİ
# ════════════════════════════════════════════════════════════

def render_yd_cockpit():
    """Dil Gelişim Cockpit — CEFR seviye, beceri analiz, sınıf ısı haritası."""
    styled_section("Dil Gelisim Cockpit & Ogretmen Kontrol Paneli", "#2563eb")
    styled_info_banner(
        "Tum ogrencilerin CEFR seviyesi, beceri skorlari, sinif bazli analiz. "
        "Zayif beceri tespiti, AI ders plani onerisi.",
        banner_type="info", icon="📊")

    profiller = _lj("yd_profiller.json")
    aktiviteler = _lj("yd_aktiviteler.json")

    styled_stat_row([
        ("Profil", str(len(profiller)), "#2563eb", "👤"),
        ("Aktivite", str(len(aktiviteler)), "#10b981", "📋"),
    ])

    sub = st.tabs(["🚦 Sinif Gorunumu", "👤 Bireysel Profil", "🌡️ Beceri Isi Haritasi", "💡 AI Oneri", "📝 Profil Kaydet"])

    # ── SINIF GÖRÜNÜMÜ ──
    with sub[0]:
        styled_section("Sinif Bazli CEFR Dagılımı")
        if not profiller:
            st.info("Profil verisi yok. 'Profil Kaydet' sekmesinden baslatin.")
        else:
            cefr_say = Counter(p.get("cefr","?") for p in profiller)
            toplam = max(len(profiller), 1)
            for seviye in _CEFR:
                sayi = cefr_say.get(seviye, 0)
                pct = round(sayi / toplam * 100)
                renk = _CEFR_RENK.get(seviye, "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="background:{renk};color:#fff;padding:4px 12px;border-radius:8px;
                        font-weight:800;font-size:0.85rem;min-width:30px;text-align:center;">{seviye}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi} ogr (%{pct})</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── BİREYSEL PROFİL ──
    with sub[1]:
        styled_section("Ogrenci Dil Profili")
        if not profiller:
            st.info("Profil yok.")
        else:
            sec = st.selectbox("Ogrenci",
                [f"{p.get('ogrenci','')} ({p.get('cefr','')})" for p in profiller], key="ydc_ogr")
            idx = [f"{p.get('ogrenci','')} ({p.get('cefr','')})" for p in profiller].index(sec) if sec else 0
            p = profiller[idx]
            cefr = p.get("cefr","?")
            renk = _CEFR_RENK.get(cefr, "#94a3b8")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,{renk}15);border:2px solid {renk};
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{p.get('ogrenci','')}</div>
                <div style="background:{renk};color:#fff;display:inline-block;padding:6px 20px;
                    border-radius:10px;font-weight:900;font-size:1.5rem;margin-top:8px;">{cefr}</div>
                <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{_CEFR_ACIKLAMA.get(cefr,'')}</div>
            </div>""", unsafe_allow_html=True)

            beceriler = p.get("beceriler", {})
            if beceriler:
                styled_section("Beceri Profili")
                for beceri, info in _BECERILER.items():
                    puan = beceriler.get(beceri, 50)
                    b_renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                        <span style="font-size:1.1rem;">{info['ikon']}</span>
                        <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{beceri}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                            <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{b_renk});
                                border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                                <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── BECERİ ISI HARİTASI ──
    with sub[2]:
        styled_section("Sinif Geneli Beceri Isi Haritasi")
        if not profiller:
            st.info("Veri yok.")
        else:
            beceri_ort = defaultdict(list)
            for p in profiller:
                for b, puan in p.get("beceriler", {}).items():
                    beceri_ort[b].append(puan)

            for beceri, info in _BECERILER.items():
                puanlar = beceri_ort.get(beceri, [])
                if puanlar:
                    ort = round(sum(puanlar) / len(puanlar))
                    renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                        background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                        <span style="font-size:1.1rem;">{info['ikon']}</span>
                        <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.85rem;">{beceri}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                            <div style="width:{ort}%;height:100%;background:{renk};border-radius:6px;
                                display:flex;align-items:center;padding-left:8px;">
                                <span style="font-size:0.65rem;color:#fff;font-weight:800;">{ort}/100</span>
                            </div>
                        </div>
                        <span style="font-size:0.65rem;color:#64748b;">{len(puanlar)} ogr</span>
                    </div>""", unsafe_allow_html=True)

            # En zayif
            if beceri_ort:
                en_zayif = min(beceri_ort, key=lambda b: sum(beceri_ort[b])/len(beceri_ort[b]))
                en_z_ort = round(sum(beceri_ort[en_zayif]) / len(beceri_ort[en_zayif]))
                st.warning(f"En zayif beceri: **{en_zayif}** ({en_z_ort}/100) — bu alanda pratik arttirilmali!")

    # ── AI ÖNERİ ──
    with sub[3]:
        styled_section("AI Ders Plani Onerisi")
        if not profiller:
            st.info("Profil verisi gerekli.")
        else:
            beceri_ort2 = {}
            for b in _BECERILER:
                puanlar = [p.get("beceriler",{}).get(b,50) for p in profiller]
                beceri_ort2[b] = round(sum(puanlar) / max(len(puanlar), 1))

            oneriler = []
            if beceri_ort2.get("Speaking", 100) < 50:
                oneriler.append(("🗣️ Speaking Guclendir", "Haftalik konusma pratigi artirin. AI diyalog senaryolari kullanin.", "#10b981"))
            if beceri_ort2.get("Listening", 100) < 50:
                oneriler.append(("👂 Listening Guclendir", "Podcast, sarki, film altyazili izleme etkinlikleri ekleyin.", "#3b82f6"))
            if beceri_ort2.get("Writing", 100) < 50:
                oneriler.append(("✍️ Writing Guclendir", "Haftalik paragraph yazma odevi, penpal projesi baslatin.", "#f59e0b"))
            if beceri_ort2.get("Vocabulary", 100) < 60:
                oneriler.append(("📚 Kelime Guclendir", "Gunluk 10 yeni kelime hedefi koyun. Flash kart kullanin.", "#059669"))

            if not oneriler:
                oneriler.append(("⭐ Harika!", "Tum beceriler iyi seviyede. Derinlestirme ve Challenge aktiviteleri onerin.", "#c9a84c"))

            for baslik, mesaj, renk in oneriler:
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:6px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.82rem;">{baslik}</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:3px;">{mesaj}</div>
                </div>""", unsafe_allow_html=True)

    # ── PROFİL KAYDET ──
    with sub[4]:
        styled_section("Ogrenci Dil Profili Kaydet")
        with st.form("yd_profil_form"):
            ogr = _ogr_sec("ydc_kayit_ogr")
            cefr = st.selectbox("CEFR Seviyesi", _CEFR, key="ydc_cefr")

            st.markdown("**Beceri Puanlari (0-100):**")
            beceriler = {}
            cols = st.columns(3)
            for i, (b, info) in enumerate(_BECERILER.items()):
                with cols[i % 3]:
                    beceriler[b] = st.slider(f"{info['ikon']} {b}", 0, 100, 50, key=f"ydc_b_{b}")

            if st.form_submit_button("Kaydet", use_container_width=True, type="primary"):
                if ogr:
                    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
                    profiller.append({
                        "id": f"ydp_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "sinif": ogr.get("sinif",""), "sube": ogr.get("sube",""),
                        "cefr": cefr, "beceriler": beceriler,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("yd_profiller.json", profiller)
                    st.success(f"{ogr_ad}: {cefr} profili kaydedildi!")
                    st.rerun()


# ════════════════════════════════════════════════════════════
# 2. AI KONUŞMA PARTNERİ & GÜNLÜK DİYALOG SENARYOLARI
# ════════════════════════════════════════════════════════════

def render_yd_konusma_partneri():
    """AI Konuşma Partneri — günlük senaryo, roleplay, anahtar cümle, geri bildirim."""
    styled_section("AI Konusma Partneri & Gunluk Diyalog", "#10b981")
    styled_info_banner(
        "Gunluk hayat senaryolarinda Ingilizce pratik. "
        "Roleplay modlari, anahtar cumleler, geri bildirim.",
        banner_type="info", icon="🗣️")

    pratik_log = _lj("konusma_pratik_log.json")

    styled_stat_row([
        ("Senaryo", str(len(_SENARYOLAR)), "#10b981", "📋"),
        ("Pratik Kaydi", str(len(pratik_log)), "#3b82f6", "💬"),
    ])

    sub = st.tabs(["🎭 Senaryo Sec", "💬 Diyalog Pratik", "📚 Anahtar Cumleler", "📊 Pratik Gecmis"])

    # ── SENARYO SEÇ ──
    with sub[0]:
        styled_section("Gunluk Hayat Senaryolari")
        for s in _SENARYOLAR:
            renk = s["renk"]
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">
                        {s['ikon']} {s['ad']}</span>
                    <span style="background:{_CEFR_RENK.get(s['seviye'],'#94a3b8')}20;
                        color:{_CEFR_RENK.get(s['seviye'],'#94a3b8')};padding:3px 10px;border-radius:8px;
                        font-size:0.72rem;font-weight:700;">{s['seviye']}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                    {len(s['diyalog'])} cumle | Anahtar: {', '.join(s['anahtar'][:3])}</div>
            </div>""", unsafe_allow_html=True)

    # ── DİYALOG PRATİK ──
    with sub[1]:
        styled_section("Diyalog Pratigi")
        sec_senaryo = st.selectbox("Senaryo Sec",
            [f"{s['ikon']} {s['ad']} ({s['seviye']})" for s in _SENARYOLAR], key="kp_sec")
        sec_idx = [f"{s['ikon']} {s['ad']} ({s['seviye']})" for s in _SENARYOLAR].index(sec_senaryo) if sec_senaryo else 0
        senaryo = _SENARYOLAR[sec_idx]

        st.markdown(f"### {senaryo['ikon']} {senaryo['ad']} — {senaryo['seviye']}")

        for konusmaci, cumle in senaryo["diyalog"]:
            if konusmaci == "You":
                st.markdown(f"""
                <div style="background:#10b98115;border:1px solid #10b98130;border-radius:12px 12px 0 12px;
                    padding:10px 14px;margin:6px 0 6px 40px;text-align:right;">
                    <span style="color:#6ee7b7;font-weight:600;font-size:0.72rem;">🧑‍🎓 You</span>
                    <div style="color:#e2e8f0;font-size:0.85rem;margin-top:3px;">{cumle}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#3b82f610;border:1px solid #3b82f630;border-radius:12px 12px 12px 0;
                    padding:10px 14px;margin:6px 40px 6px 0;">
                    <span style="color:#93c5fd;font-weight:600;font-size:0.72rem;">🤖 {konusmaci}</span>
                    <div style="color:#e2e8f0;font-size:0.85rem;margin-top:3px;">{cumle}</div>
                </div>""", unsafe_allow_html=True)

        ogr = _ogr_sec("kp_ogr")
        if ogr and st.button("Pratigi Tamamladim!", use_container_width=True, type="primary"):
            pratik_log.append({
                "ogrenci": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                "senaryo": senaryo["ad"], "seviye": senaryo["seviye"],
                "tarih": datetime.now().isoformat(),
            })
            _sj("konusma_pratik_log.json", pratik_log)
            st.success(f"🗣️ {senaryo['ad']} pratigi tamamlandi!")

    # ── ANAHTAR CÜMLELER ──
    with sub[2]:
        styled_section("Senaryo Bazli Anahtar Cumleler")
        for s in _SENARYOLAR:
            with st.expander(f"{s['ikon']} {s['ad']} — {s['seviye']}"):
                for ac in s["anahtar"]:
                    st.markdown(f"""
                    <div style="background:#10b98108;border:1px solid #10b98130;border-left:3px solid #10b981;
                        border-radius:0 8px 8px 0;padding:6px 12px;margin:3px 0;">
                        <span style="color:#6ee7b7;font-weight:700;font-size:0.85rem;">💬 {ac}</span>
                    </div>""", unsafe_allow_html=True)

    # ── PRATİK GEÇMİŞ ──
    with sub[3]:
        styled_section("Pratik Gecmisi")
        if not pratik_log:
            st.info("Pratik kaydi yok.")
        else:
            ogr_say = Counter(p.get("ogrenci","") for p in pratik_log)
            styled_section("En Aktif Konusmacilar")
            for sira, (ad, sayi) in enumerate(ogr_say.most_common(10), 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #10b981;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ad}</span>
                    <span style="color:#10b981;font-weight:800;">{sayi} pratik</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. CEFR İLERLEME YOL HARİTASI & SERTİFİKA HAZIRLIK
# ════════════════════════════════════════════════════════════

def render_yd_cefr_yol_haritasi():
    """CEFR İlerleme Yol Haritası — A1→C2, sertifika hazırlık, simülasyon."""
    styled_section("CEFR Ilerleme Yol Haritasi & Sertifika Hazirlik", "#8b5cf6")
    styled_info_banner(
        "A1→A2→B1→B2→C1→C2 yolculuk haritasi. Her seviye icin hedef + mastery. "
        "Cambridge/IELTS/TOEFL/YDS simulasyon, puan tahmini.",
        banner_type="info", icon="🏆")

    profiller = _lj("yd_profiller.json")
    sinav_sonuclari = _lj("yd_sinav_sonuclari.json")

    sub = st.tabs(["🗺️ Yol Haritasi", "📋 Seviye Hedefleri", "📝 Sinav Simulasyon", "📈 Ilerleme Takip"])

    # ── YOL HARİTASI ──
    with sub[0]:
        styled_section("CEFR Yolculuk Haritasi")
        ogr = _ogr_sec("yh_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            profil = next((p for p in profiller if p.get("ogrenci") == ogr_ad), None)
            mevcut = profil.get("cefr", "A1") if profil else "A1"
            mevcut_idx = _CEFR.index(mevcut) if mevcut in _CEFR else 0

            st.markdown(f"**{ogr_ad}** — Mevcut: **{mevcut}**")

            for idx, seviye in enumerate(_CEFR):
                renk = _CEFR_RENK[seviye]
                gecti = idx < mevcut_idx
                aktif = idx == mevcut_idx
                gelecek = idx > mevcut_idx

                opacity = "1" if gecti or aktif else "0.4"
                border = f"3px solid {renk}" if aktif else f"1px solid {renk}40"
                ikon = "✅" if gecti else "🔵" if aktif else "⬜"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:10px 16px;margin:4px 0;
                    background:#0f172a;border:{border};border-radius:14px;opacity:{opacity};">
                    <span style="font-size:1.2rem;">{ikon}</span>
                    <span style="background:{renk};color:#fff;padding:4px 14px;border-radius:8px;
                        font-weight:900;font-size:0.9rem;">{seviye}</span>
                    <span style="color:#e2e8f0;font-size:0.8rem;flex:1;">{_CEFR_ACIKLAMA[seviye]}</span>
                    {'<span style="color:#c9a84c;font-weight:800;font-size:0.72rem;">📌 Buradasin</span>' if aktif else ''}
                </div>""", unsafe_allow_html=True)

    # ── SEVİYE HEDEFLERİ ──
    with sub[1]:
        styled_section("Seviye Bazli Hedefler")
        sec_sev = st.selectbox("Seviye", _CEFR, key="yh_sev")
        hedefler = _CEFR_HEDEFLER.get(sec_sev, {})
        renk = _CEFR_RENK.get(sec_sev, "#94a3b8")

        st.markdown(f"### {sec_sev} Seviyesi Hedefleri")
        for hedef, deger in hedefler.items():
            birim = "kelime" if "Vocab" in hedef else "kural" if "Grammar" in hedef else "saat"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 14px;margin:4px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">
                    {hedef.replace('_hr',' (saat)').replace('_',' ')}</span>
                <span style="color:{renk};font-weight:800;font-size:0.85rem;">{deger:,} {birim}</span>
            </div>""", unsafe_allow_html=True)

    # ── SINAV SİMÜLASYON ──
    with sub[2]:
        styled_section("Uluslararasi Sinav Simulasyon")
        sec_sinav = st.selectbox("Sinav Turu", list(_SINAV_TURLERI.keys()), key="yh_sinav")
        sinav = _SINAV_TURLERI[sec_sinav]

        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #8b5cf6;border-radius:16px;padding:16px 20px;margin:10px 0;">
            <div style="color:#e2e8f0;font-weight:900;font-size:1rem;text-align:center;">📋 {sec_sinav}</div>
            <div style="color:#94a3b8;font-size:0.75rem;text-align:center;">
                Seviye: {sinav['seviye']} | Sure: {sinav['sure_dk']} dk | Beceri: {', '.join(sinav['beceri'])}</div>
        </div>""", unsafe_allow_html=True)

        with st.form("sinav_sim_form"):
            ogr2 = _ogr_sec("yh_sinav_ogr")
            st.markdown(f"**{sec_sinav} — Beceri Puanlari:**")
            puanlar = {}
            cols = st.columns(min(len(sinav["beceri"]), 3))
            for i, b in enumerate(sinav["beceri"]):
                with cols[i % len(cols)]:
                    puanlar[b] = st.number_input(b, 0, 100, 60, key=f"yh_s_{b}")

            if st.form_submit_button("Sonucu Kaydet", use_container_width=True):
                if ogr2:
                    ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
                    ort = round(sum(puanlar.values()) / max(len(puanlar), 1))
                    sinav_sonuclari.append({
                        "ogrenci": ogr_ad2, "sinav": sec_sinav,
                        "puanlar": puanlar, "ortalama": ort,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("yd_sinav_sonuclari.json", sinav_sonuclari)
                    st.success(f"{ogr_ad2}: {sec_sinav} — Ort: {ort}/100")
                    st.rerun()

        if sinav_sonuclari:
            styled_section("Son Sinav Sonuclari")
            for s in sorted(sinav_sonuclari, key=lambda x: x.get("tarih",""), reverse=True)[:5]:
                ort = s.get("ortalama", 0)
                renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">{s.get('ogrenci','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{s.get('sinav','')}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.82rem;">{ort}/100</span>
                </div>""", unsafe_allow_html=True)

    # ── İLERLEME TAKİP ──
    with sub[3]:
        styled_section("CEFR Ilerleme Takibi")
        if not profiller:
            st.info("Profil verisi yok.")
        else:
            for p in sorted(profiller, key=lambda x: _CEFR.index(x.get("cefr","A1")) if x.get("cefr") in _CEFR else 0, reverse=True)[:15]:
                cefr = p.get("cefr","?")
                renk = _CEFR_RENK.get(cefr, "#94a3b8")
                beceriler = p.get("beceriler", {})
                ort = round(sum(beceriler.values()) / max(len(beceriler), 1)) if beceriler else 50
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:6px;
                        font-weight:800;font-size:0.78rem;">{cefr}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{p.get('ogrenci','')}</span>
                    <span style="color:#64748b;font-size:0.68rem;">Ort: {ort}/100</span>
                </div>""", unsafe_allow_html=True)
