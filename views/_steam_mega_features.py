"""
STEAM Merkezi — Mega Özellikler
=================================
1. AI STEAM Mentor & Proje Rehberlik Chatbot
2. STEAM Challenge & Maker Yarışma Motoru
3. STEAM Veli & Toplum Etkileşim Platformu
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

_AI_MENTOR_YANITLARI = {
    "robotik": [
        "Harika secim! Once servo motor mekanizmasini ogren → Arduino kodunu yaz → 3D baski ile govde hazirla.",
        "Robotik kol icin: 1) Tasarim ciz 2) Servo motor sec 3) Arduino baglanti 4) Kod yaz 5) Test et.",
    ],
    "elektronik": [
        "Devre tasarimi icin: 1) Sematik ciz 2) Breadboard'da prototip yap 3) Lehimle 4) Test et.",
        "LED projesi basit bir baslangic! Arduino + LED + direnc ile ilk devrenni kur.",
    ],
    "kodlama": [
        "Hangi dil? Python icin: Temel syntax → Donguler → Fonksiyonlar → Proje. Scratch icin: Blok kodlama ile basla!",
        "IoT projesi icin: Arduino IDE + WiFi modul + Sensor okuma + Veri gonderme adimlarini takip et.",
    ],
    "3d_baski": [
        "3D tasarim icin Tinkercad ile basla — ucretsiz ve kolay. Sonra Fusion 360'a gec.",
        "3D baski adimlari: 1) Tinkercad'de modelle 2) STL indir 3) Slicer'da ayarla 4) Yazicida bas.",
    ],
    "bilim": [
        "Bilim projesi icin: 1) Soru belirle 2) Hipotez kur 3) Deney tasarla 4) Veri topla 5) Sonuc cikar.",
        "TUBITAK projesi mi? Guncel bir problem sec, ozgun bir cozum onerisi gelistir, deneylerle kanitla.",
    ],
    "genel": [
        "STEAM projesi icin en onemli adim: gercek bir problemi cozmeye odaklanmak!",
        "Once ne yapmak istedigini belirle, sonra hangi STEAM alanlarini kullanacagina karar ver.",
    ],
}

_CHALLENGE_TURLERI = [
    {"ad": "Kagit Kule Challenge", "ikon": "🏗️", "renk": "#f59e0b", "sure": "30 dk",
     "aciklama": "Sadece kagit ve bantla en yuksek kuleyi yap!", "kategori": "Muhendislik"},
    {"ad": "Arduino LED Gosterisi", "ikon": "💡", "renk": "#3b82f6", "sure": "1 saat",
     "aciklama": "Arduino ile en yaratici LED animasyonunu kodla!", "kategori": "Teknoloji"},
    {"ad": "Geri Donusum Robotu", "ikon": "♻️", "renk": "#10b981", "sure": "1 hafta",
     "aciklama": "Geri donusum malzemelerinden calisan bir robot yap!", "kategori": "Muhendislik+Cevre"},
    {"ad": "Veri Gorsellestirme", "ikon": "📊", "renk": "#8b5cf6", "sure": "2 saat",
     "aciklama": "Okul verilerinden en anlamli grafigi olustur!", "kategori": "Matematik+Bilisim"},
    {"ad": "Biyomimikri Tasarim", "ikon": "🦎", "renk": "#059669", "sure": "1 hafta",
     "aciklama": "Dogadan esinlenerek bir muhendislik cozumu tasarla!", "kategori": "Fen+Muhendislik"},
    {"ad": "Muzik Enstrumani Yap", "ikon": "🎵", "renk": "#ef4444", "sure": "3 saat",
     "aciklama": "Geri donusum malzemeleriyle calisan bir enstruman yap!", "kategori": "Sanat+Fen"},
    {"ad": "IoT Hava Istasyonu", "ikon": "🌤️", "renk": "#0891b2", "sure": "2 hafta",
     "aciklama": "Sicaklik+nem sensoru ile hava durumu izleme sistemi kur!", "kategori": "Teknoloji+Fen"},
    {"ad": "3D Baski Tasarim", "ikon": "🖨️", "renk": "#6366f1", "sure": "1 hafta",
     "aciklama": "Okul icin faydali bir nesne tasarla ve 3D yaziciyla bas!", "kategori": "Tasarim+Teknoloji"},
]

_ETKINLIK_TURLERI = ["Acik Kapi Gunu", "Bilim Fuari", "Maker Gunu", "STEAM Sergisi",
    "Veli Workshop", "Muhendis Bulusmasi", "Universite Ziyareti", "Staj Programi"]


# ════════════════════════════════════════════════════════════
# 1. AI STEAM MENTOR & PROJE REHBERLİK CHATBOT
# ════════════════════════════════════════════════════════════

def render_ai_steam_mentor(store):
    """AI STEAM Mentor — proje rehberlik, malzeme önerisi, hata çözme."""
    styled_section("AI STEAM Mentor & Proje Rehberlik Chatbot", "#6366f1")
    styled_info_banner(
        "Proje fikrinizi anlatin, AI adim adim rehberlik etsin. "
        "Malzeme onerisi, hata cozme, ogretmene etkilesim ozeti.",
        banner_type="info", icon="🤖")

    sohbetler = _lj("steam_mentor_sohbet.json")

    sub = st.tabs(["💬 AI Mentorla Konus", "📋 Sohbet Gecmisi", "📊 Etkilesim Ozeti"])

    with sub[0]:
        styled_section("AI STEAM Mentor'a Sor")
        ogr = st.text_input("Ogrenci Adi", key="sm_ogr")
        alan = st.selectbox("STEAM Alani",
            ["Robotik", "Elektronik", "Kodlama", "3D Baski", "Bilim", "Genel"], key="sm_alan")
        soru = st.text_area("Sorun / Proje Fikrin", height=60, key="sm_soru",
            placeholder="Robotik kol yapmak istiyorum, nereden baslamaliyim?")

        if st.button("AI Mentor'a Sor", use_container_width=True, type="primary") and ogr and soru:
            alan_key = alan.lower().replace(" ", "_").replace("ı", "i")
            yanitlar = _AI_MENTOR_YANITLARI.get(alan_key, _AI_MENTOR_YANITLARI["genel"])
            yanit = random.choice(yanitlar)

            sohbetler.append({
                "ogrenci": ogr, "alan": alan, "soru": soru, "yanit": yanit,
                "tarih": datetime.now().isoformat(),
            })
            _sj("steam_mentor_sohbet.json", sohbetler)

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:16px 20px;margin:10px 0;">
                <div style="background:#3b82f610;border:1px solid #3b82f630;border-radius:12px 12px 0 12px;
                    padding:10px 14px;margin-bottom:8px;">
                    <span style="color:#93c5fd;font-weight:600;font-size:0.72rem;">🧑‍🎓 {ogr} ({alan})</span>
                    <div style="color:#e2e8f0;font-size:0.85rem;margin-top:3px;">{soru}</div>
                </div>
                <div style="background:#6366f110;border:1px solid #6366f130;border-radius:12px 12px 12px 0;
                    padding:10px 14px;">
                    <span style="color:#a5b4fc;font-weight:600;font-size:0.72rem;">🤖 AI STEAM Mentor</span>
                    <div style="color:#e2e8f0;font-size:0.85rem;margin-top:3px;">{yanit}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Sohbet Gecmisi")
        if not sohbetler:
            st.info("Sohbet yok.")
        else:
            for s in sorted(sohbetler, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="padding:6px 12px;margin:3px 0;background:#0f172a;
                    border-left:3px solid #6366f1;border-radius:0 8px 8px 0;">
                    <span style="color:#a5b4fc;font-size:0.68rem;">{s.get('ogrenci','')} ({s.get('alan','')}) — {s.get('tarih','')[:10]}</span>
                    <div style="color:#e2e8f0;font-size:0.72rem;margin-top:2px;">{s.get('soru','')[:60]}...</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Ogretmen Icin Etkilesim Ozeti")
        if sohbetler:
            alan_say = Counter(s.get("alan","") for s in sohbetler)
            ogr_say = Counter(s.get("ogrenci","") for s in sohbetler)

            styled_section("Alan Dagilimi")
            for alan, sayi in alan_say.most_common():
                st.markdown(f"  - **{alan}**: {sayi} sohbet")

            styled_section("En Aktif Ogrenciler")
            for ad, sayi in ogr_say.most_common(5):
                st.markdown(f"  - {ad}: {sayi} soru")


# ════════════════════════════════════════════════════════════
# 2. STEAM CHALLENGE & MAKER YARIŞMA MOTORU
# ════════════════════════════════════════════════════════════

def render_steam_challenge(store):
    """STEAM Challenge — haftalık/aylık challenge, katılım, jüri, galeri."""
    styled_section("STEAM Challenge & Maker Yarisma Motoru", "#ef4444")
    styled_info_banner(
        "Haftalik/aylik STEAM challenge! Katilim kayit, juri puanlama, "
        "siniflar arasi maker yarisi, en iyi proje galerisi.",
        banner_type="info", icon="🏗️")

    challenge_log = _lj("challenge_kayitlari.json")
    katilimlar = _lj("challenge_katilim.json")

    bu_ay = date.today().strftime("%Y-%m")
    bu_ay_ch = [c for c in challenge_log if c.get("tarih","")[:7] == bu_ay]

    styled_stat_row([
        ("Toplam Challenge", str(len(challenge_log)), "#ef4444", "🏗️"),
        ("Bu Ay", str(len(bu_ay_ch)), "#f59e0b", "📅"),
        ("Katilim", str(len(katilimlar)), "#10b981", "👥"),
    ])

    sub = st.tabs(["🏗️ Aktif Challenge", "➕ Yeni Challenge", "📋 Katilim", "🏆 Sonuclar", "📸 Galeri"])

    with sub[0]:
        styled_section("Hazir STEAM Challenge'lar")
        for ch in _CHALLENGE_TURLERI:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {ch['renk']}30;border-left:5px solid {ch['renk']};
                border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">{ch['ikon']} {ch['ad']}</span>
                    <span style="color:{ch['renk']};font-size:0.7rem;font-weight:700;">⏱️ {ch['sure']}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">{ch['aciklama']}</div>
                <div style="color:#64748b;font-size:0.65rem;margin-top:2px;">Kategori: {ch['kategori']}</div>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Yeni Challenge Baslat")
        with st.form("ch_form"):
            c1, c2 = st.columns(2)
            with c1:
                ch_ad = st.text_input("Challenge Adi", key="ch_ad")
                ch_kategori = st.selectbox("Kategori",
                    ["Muhendislik","Teknoloji","Bilim","Sanat","Matematik","Karma"], key="ch_kat")
            with c2:
                ch_sure = st.selectbox("Sure", ["30 dk","1 saat","3 saat","1 gun","1 hafta","2 hafta","1 ay"], key="ch_sure")
                ch_termin = st.date_input("Son Katilim", key="ch_termin")
            ch_aciklama = st.text_area("Challenge Aciklamasi", height=60, key="ch_acik")

            if st.form_submit_button("Challenge Baslat", use_container_width=True, type="primary"):
                if ch_ad:
                    challenge_log.append({
                        "id": f"ch_{uuid.uuid4().hex[:8]}",
                        "ad": ch_ad, "kategori": ch_kategori,
                        "sure": ch_sure, "termin": ch_termin.isoformat(),
                        "aciklama": ch_aciklama, "durum": "Aktif",
                        "tarih": date.today().isoformat(),
                    })
                    _sj("challenge_kayitlari.json", challenge_log)
                    st.success(f"🏗️ '{ch_ad}' challenge baslatildi!")
                    st.rerun()

    with sub[2]:
        styled_section("Challenge Katilim Kaydi")
        aktif_ch = [c for c in challenge_log if c.get("durum") == "Aktif"]
        if aktif_ch:
            with st.form("ch_kat_form"):
                c1, c2 = st.columns(2)
                with c1:
                    k_ch = st.selectbox("Challenge", [c.get("ad","") for c in aktif_ch], key="ck_ch")
                    k_ogr = st.text_input("Ogrenci/Takim", key="ck_ogr")
                with c2:
                    k_proje = st.text_input("Proje Adi", key="ck_proje")
                    k_puan = st.number_input("Juri Puani (0-100)", 0, 100, 0, key="ck_puan")

                if st.form_submit_button("Katilim Kaydet", use_container_width=True):
                    if k_ogr:
                        katilimlar.append({
                            "challenge": k_ch, "ogrenci": k_ogr,
                            "proje": k_proje, "puan": k_puan,
                            "tarih": datetime.now().isoformat(),
                        })
                        _sj("challenge_katilim.json", katilimlar)
                        st.success(f"✅ {k_ogr} katilimi kaydedildi!")
                        st.rerun()

    with sub[3]:
        styled_section("Challenge Sonuclari")
        if katilimlar:
            ch_grp = defaultdict(list)
            for k in katilimlar:
                ch_grp[k.get("challenge","")].append(k)

            for ch_ad, kat_list in ch_grp.items():
                sirali = sorted(kat_list, key=lambda x: x.get("puan",0), reverse=True)
                st.markdown(f"**🏗️ {ch_ad}** — {len(sirali)} katilimci")
                for sira, k in enumerate(sirali[:5], 1):
                    madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:4px 12px;margin:2px 0;
                        background:#0f172a;border-left:3px solid #ef4444;border-radius:0 8px 8px 0;">
                        <span style="font-size:1rem;">{madalya}</span>
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{k.get('ogrenci','')}</span>
                        <span style="color:#94a3b8;font-size:0.65rem;">{k.get('proje','')}</span>
                        <span style="color:#ef4444;font-weight:800;">{k.get('puan',0)}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("Katilim kaydi yok.")

    with sub[4]:
        styled_section("En Iyi Proje Galerisi")
        if katilimlar:
            en_iyiler = sorted(katilimlar, key=lambda x: x.get("puan",0), reverse=True)[:6]
            cols = st.columns(2)
            for i, k in enumerate(en_iyiler):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid #ef444430;border-radius:14px;
                        padding:14px;text-align:center;margin:4px 0;">
                        <div style="font-size:1.5rem;">🏗️</div>
                        <div style="color:#e2e8f0;font-weight:800;font-size:0.82rem;margin-top:4px;">{k.get('proje','')}</div>
                        <div style="color:#94a3b8;font-size:0.68rem;">{k.get('ogrenci','')} | {k.get('challenge','')}</div>
                        <div style="color:#ef4444;font-weight:900;font-size:1rem;margin-top:4px;">{k.get('puan',0)}/100</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Galeri bos.")


# ════════════════════════════════════════════════════════════
# 3. STEAM VELİ & TOPLUM ETKİLEŞİM PLATFORMU
# ════════════════════════════════════════════════════════════

def render_steam_toplum(store):
    """STEAM Veli & Toplum — veli bilgi, mentor ağı, açık kapı, sosyal medya."""
    styled_section("STEAM Veli & Toplum Etkilesim Platformu", "#059669")
    styled_info_banner(
        "Veli bilgilendirme, toplum katki programi, sanayi/universite mentor, "
        "acik kapi gunu planlama, sosyal medya paylasim.",
        banner_type="info", icon="📡")

    veli_bildirim = _lj("steam_veli_bildirim.json")
    mentorler = _lj("steam_dis_mentorler.json")
    etkinlikler = _lj("steam_toplum_etkinlik.json")

    styled_stat_row([
        ("Veli Bildirim", str(len(veli_bildirim)), "#059669", "📨"),
        ("Dis Mentor", str(len(mentorler)), "#3b82f6", "👨‍🏫"),
        ("Toplum Etkinlik", str(len(etkinlikler)), "#8b5cf6", "🏛️"),
    ])

    sub = st.tabs(["📨 Veli Bildirim", "👨‍🏫 Mentor Agi", "🏛️ Etkinlik Planla", "📱 Sosyal Medya"])

    with sub[0]:
        styled_section("Veli Bilgilendirme")
        with st.form("vb_form"):
            c1, c2 = st.columns(2)
            with c1:
                v_ogr = st.text_input("Ogrenci", key="vb_ogr")
                v_tur = st.selectbox("Bildirim Turu",
                    ["Proje Ilerleme", "Lab Calismasi", "Yarisma Sonucu", "Yeni Beceri", "Genel"], key="vb_tur")
            with c2:
                v_mesaj = st.text_area("Mesaj", height=60, key="vb_mesaj",
                    placeholder="Cocugunuz bu hafta Arduino ile ilk devresini kurdu!")

            if st.form_submit_button("Bildirim Gonder", use_container_width=True):
                if v_ogr and v_mesaj:
                    veli_bildirim.append({
                        "ogrenci": v_ogr, "tur": v_tur, "mesaj": v_mesaj,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("steam_veli_bildirim.json", veli_bildirim)
                    st.success("Veli bildirim gonderildi!")
                    st.rerun()

        if veli_bildirim:
            for v in sorted(veli_bildirim, key=lambda x: x.get("tarih",""), reverse=True)[:8]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:6px;padding:5px 10px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="color:#10b981;font-size:0.68rem;min-width:80px;">{v.get('tur','')}</span>
                    <span style="color:#e2e8f0;font-size:0.72rem;flex:1;">{v.get('ogrenci','')} — {v.get('mesaj','')[:50]}</span>
                    <span style="color:#64748b;font-size:0.6rem;">{v.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Sanayi / Universite Mentor Agi")
        with st.form("mentor_form"):
            c1, c2 = st.columns(2)
            with c1:
                m_ad = st.text_input("Mentor Adi", key="dm_ad")
                m_uzmanlik = st.text_input("Uzmanlik", placeholder="Robotik, IoT, Yazilim...", key="dm_uz")
            with c2:
                m_kurum = st.text_input("Kurum", placeholder="XYZ Sirket, ABC Univ.", key="dm_kurum")
                m_iletisim = st.text_input("Iletisim", key="dm_il")

            if st.form_submit_button("Mentor Ekle", use_container_width=True):
                if m_ad:
                    mentorler.append({
                        "ad": m_ad, "uzmanlik": m_uzmanlik,
                        "kurum": m_kurum, "iletisim": m_iletisim,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("steam_dis_mentorler.json", mentorler)
                    st.success(f"👨‍🏫 {m_ad} mentor agina eklendi!")
                    st.rerun()

        if mentorler:
            for m in mentorler:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">👨‍🏫 {m.get('ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{m.get('uzmanlik','')} | {m.get('kurum','')}</span>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Toplum Etkinligi Planla")
        with st.form("etkinlik_form"):
            c1, c2 = st.columns(2)
            with c1:
                e_ad = st.text_input("Etkinlik Adi", key="te_ad")
                e_tur = st.selectbox("Tur", _ETKINLIK_TURLERI, key="te_tur")
            with c2:
                e_tarih = st.date_input("Tarih", key="te_tarih")
                e_katilimci = st.number_input("Beklenen Katilimci", 10, 500, 50, key="te_kat")
            e_aciklama = st.text_area("Aciklama", height=50, key="te_acik")

            if st.form_submit_button("Etkinlik Planla", use_container_width=True):
                if e_ad:
                    etkinlikler.append({
                        "id": f"te_{uuid.uuid4().hex[:8]}",
                        "ad": e_ad, "tur": e_tur, "tarih": e_tarih.isoformat(),
                        "katilimci": e_katilimci, "aciklama": e_aciklama,
                        "durum": "Planlandi", "created_at": datetime.now().isoformat(),
                    })
                    _sj("steam_toplum_etkinlik.json", etkinlikler)
                    st.success(f"🏛️ '{e_ad}' etkinligi planlandi!")
                    st.rerun()

        if etkinlikler:
            for e in sorted(etkinlikler, key=lambda x: x.get("tarih",""), reverse=True):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🏛️ {e.get('ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{e.get('tur','')} | {e.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Sosyal Medya Paylasim Paketi")
        st.caption("STEAM etkinliklerinizi sosyal medyada paylasin!")

        projeler = _lj("tubitak_projeler.json")
        if projeler:
            styled_section("Paylasilabilir Projeler")
            for p in projeler[:5]:
                st.markdown(f"""
                <div style="background:#05966910;border:1px solid #05966930;border-radius:10px;
                    padding:8px 14px;margin:4px 0;">
                    <span style="color:#10b981;font-weight:700;font-size:0.78rem;">📱 {p.get('ad','')}</span>
                    <div style="color:#94a3b8;font-size:0.68rem;margin-top:2px;">
                        #{p.get('yarisma','').replace(' ','_')} #STEAM #SmartCampus</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("**Hashtag Onerileri:** #STEAM #Maker #TUBİTAK #BilimFuarı #Robotik #SmartCampus #KodlamaOgreniyorum")
