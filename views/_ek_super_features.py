"""
Eğitim Koçluğu — Süper Özellikler
====================================
1. AI Sınav Kaygısı Yönetimi & Psikolojik Hazırlık
2. Akran Koçluk & Grup Dinamiği Paneli
3. Koçluk Döngüsü & Etkinlik Ölçüm Motoru
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "egitim_koclugu"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else d.get("items", d.get("data", []))
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_KAYGI_SORULARI = [
    "Sinav oncesi uyuyamiyorum",
    "Sinav sorularini okurken aklim karisyor",
    "Calistigim halde basaramayacagimi dusunuyorum",
    "Sinav sirasinda ellerim titriyor / terliyorum",
    "Sinav gunu midem bulaniyor / basim agriyor",
    "Arkadaslarim benden iyi yapacak diye korkuyorum",
    "Calisma programima odaklanamiyorum",
    "Sinav sonucunu dusununce panik oluyorum",
    "Ailemi hayal kirikligina ugraatacagimi dusunuyorum",
    "Sinav bittikten sonra bile rahatlamiyorum",
]

_KAYGI_SEVIYELERI = {
    (0, 8): ("Dusuk Kaygi", "#10b981", "Sakin — normal stres seviyesi"),
    (8, 15): ("Orta Kaygi", "#f59e0b", "Dikkat — bazi tekniklere ihtiyac var"),
    (15, 22): ("Yuksek Kaygi", "#ef4444", "Mudahale gerekli — program oneriliyor"),
    (22, 31): ("Cok Yuksek Kaygi", "#dc2626", "Acil — uzman destegi onerilir"),
}

_BASA_CIKMA = {
    "Dusuk Kaygi": ["Duzeni koru", "Sinav gunu rutinini planla", "Olumlu dusun"],
    "Orta Kaygi": ["Gunluk 10dk nefes egzersizi", "Calisma programini kuculte", "Pozitif vizualizasyon", "Yeterli uyku"],
    "Yuksek Kaygi": ["Haftalik koc gorusmesi", "4-7-8 nefes teknigi (gunluk)", "Bilissel yeniden yapilandirma", "Fiziksel aktivite artir", "Kafein/seker azalt"],
    "Cok Yuksek Kaygi": ["Psikolog/rehber gorusmesi (acil)", "Gevserme programi (gunluk 20dk)", "Sinav simulasyonu (duyarsizlastirma)", "Aile bilgilendirme", "Gerekirse tibbi destek"],
}

_SINAV_GUNU_RUTINI = [
    ("06:30", "Uyan — 8 saat uyku sonrasi"),
    ("06:45", "Hafif kahvalti — protein agirlikli"),
    ("07:15", "10 dk nefes egzersizi"),
    ("07:30", "Formul/ozet gozden gecir (MAX 15dk)"),
    ("07:50", "Okula yol — muzik/podcast (rahatlatici)"),
    ("08:15", "Sinav yeri — sakin otur, derin nefes"),
    ("08:30", "Sinav — once kolay sorulari yap"),
]

_KOCLUK_YAKLASIMLARI = {
    "Direktif": {"ikon": "📋", "renk": "#3b82f6", "aciklama": "Koc yonlendirir, plan verir, takip eder"},
    "Kesfettirici": {"ikon": "🔍", "renk": "#8b5cf6", "aciklama": "Sorularla dusundurur, ogrenci kesfeder"},
    "Karma": {"ikon": "🔄", "renk": "#10b981", "aciklama": "Duruma gore her iki yaklasim"},
    "Motivasyonel": {"ikon": "💪", "renk": "#f59e0b", "aciklama": "Motivasyon ve ozguven odakli"},
}


# ════════════════════════════════════════════════════════════
# 1. AI SINAV KAYGISI YÖNETİMİ
# ════════════════════════════════════════════════════════════

def render_sinav_kaygisi(store):
    """AI Sınav Kaygısı — kaygı ölçeği, başa çıkma planı, sınav günü rutini."""
    styled_section("AI Sinav Kaygisi Yonetimi & Psikolojik Hazirlik", "#8b5cf6")
    styled_info_banner(
        "Sinav oncesi kaygi olcegi, kisiye ozel basa cikma plani, "
        "sinav gunu rutini, nefes egzersizi, koc takibi.",
        banner_type="info", icon="🧠")

    kaygi_kayitlari = _lj("kaygi_olcekleri.json")

    sub = st.tabs(["📊 Kaygi Olcegi", "💡 Basa Cikma Plani", "📅 Sinav Gunu Rutini", "📈 Kaygi Trend", "🌬️ Nefes Egzersizi"])

    with sub[0]:
        styled_section("Sinav Kaygisi Olcegi (10 Soru)")
        ogrenciler = _lj("ogrenciler.json")
        if ogrenciler:
            ogr_opts = [f"{o.get('ad','')} {o.get('soyad','')}" for o in ogrenciler]
            sec = st.selectbox("Ogrenci", ogr_opts, key="sk_ogr")

            with st.form("kaygi_form"):
                toplam = 0
                for i, soru in enumerate(_KAYGI_SORULARI):
                    p = st.radio(soru, ["Hic (0)", "Bazen (1)", "Sik (2)", "Her zaman (3)"],
                        horizontal=True, key=f"sk_{i}")
                    puan_map = {"Hic (0)": 0, "Bazen (1)": 1, "Sik (2)": 2, "Her zaman (3)": 3}
                    toplam += puan_map.get(p, 0)

                if st.form_submit_button("Sonucu Hesapla", use_container_width=True, type="primary"):
                    for (lo, hi), (seviye, renk, aciklama) in _KAYGI_SEVIYELERI.items():
                        if lo <= toplam < hi:
                            break
                    else:
                        seviye, renk, aciklama = "?", "#94a3b8", ""

                    kaygi_kayitlari.append({
                        "ogrenci": sec, "puan": toplam,
                        "seviye": seviye, "tarih": date.today().isoformat(),
                    })
                    _sj("kaygi_olcekleri.json", kaygi_kayitlari)

                    st.markdown(f"""
                    <div style="background:{renk}15;border:2px solid {renk};border-radius:16px;
                        padding:20px;text-align:center;margin:10px 0;">
                        <div style="color:{renk};font-weight:900;font-size:2.5rem;">{toplam}/30</div>
                        <div style="color:{renk};font-weight:700;font-size:1rem;">{seviye}</div>
                        <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{aciklama}</div>
                    </div>""", unsafe_allow_html=True)
                    st.rerun()
        else:
            st.info("Ogrenci kaydi yok.")

    with sub[1]:
        styled_section("Kisiye Ozel Basa Cikma Plani")
        if not kaygi_kayitlari:
            st.info("Once kaygi olcegi uygulayin.")
        else:
            sec2 = st.selectbox("Ogrenci",
                [f"{k.get('ogrenci','')} ({k.get('seviye','')} — {k.get('puan','')}/30)" for k in kaygi_kayitlari],
                key="sk_plan")
            idx = [f"{k.get('ogrenci','')} ({k.get('seviye','')} — {k.get('puan','')}/30)" for k in kaygi_kayitlari].index(sec2) if sec2 else 0
            kayit = kaygi_kayitlari[idx]
            seviye = kayit.get("seviye", "Dusuk Kaygi")
            teknikler = _BASA_CIKMA.get(seviye, [])

            for (_, _), (sev, renk, _) in _KAYGI_SEVIYELERI.items():
                if sev == seviye: break
            else: renk = "#94a3b8"

            st.markdown(f"**{kayit.get('ogrenci','')}** — {seviye} ({kayit.get('puan','')}/30)")
            for t in teknikler:
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                    <span style="color:#e2e8f0;font-size:0.82rem;">💡 {t}</span>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Sinav Gunu Ideal Rutini")
        for saat, eylem in _SINAV_GUNU_RUTINI:
            st.markdown(f"""
            <div style="display:flex;gap:12px;padding:6px 0;border-left:3px solid #8b5cf6;padding-left:12px;margin:3px 0;">
                <span style="background:#8b5cf620;color:#8b5cf6;padding:3px 10px;border-radius:6px;
                    font-size:0.72rem;font-weight:800;min-width:45px;text-align:center;">{saat}</span>
                <span style="color:#e2e8f0;font-size:0.82rem;">{eylem}</span>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Kaygi Seviyesi Trend")
        if not kaygi_kayitlari:
            st.info("Veri yok.")
        else:
            ogr_grp = defaultdict(list)
            for k in kaygi_kayitlari:
                ogr_grp[k.get("ogrenci","")].append(k)

            for ogr, kayitlar in ogr_grp.items():
                st.markdown(f"**{ogr}** — {len(kayitlar)} olcum")
                for k in sorted(kayitlar, key=lambda x: x.get("tarih","")):
                    puan = k.get("puan", 0)
                    renk = "#10b981" if puan < 8 else "#f59e0b" if puan < 15 else "#ef4444" if puan < 22 else "#dc2626"
                    pct = round(puan / 30 * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin:2px 0;">
                        <span style="min-width:60px;color:#64748b;font-size:0.65rem;">{k.get('tarih','')[:10]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                        </div>
                        <span style="color:{renk};font-size:0.65rem;font-weight:700;">{puan}/30</span>
                    </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Nefes Egzersizi — 4-7-8 Teknigi")
        st.markdown("""
        **4-7-8 Nefes Teknigi:**
        1. 4 saniye burundan nefes al
        2. 7 saniye nefesi tut
        3. 8 saniye agizdan yavasca ver
        4. 4 kez tekrarla
        """)
        st.markdown(f"""
        <div style="background:#8b5cf610;border:2px solid #8b5cf6;border-radius:50%;
            width:150px;height:150px;display:flex;align-items:center;justify-content:center;
            margin:20px auto;">
            <div style="text-align:center;">
                <div style="color:#8b5cf6;font-weight:900;font-size:1.5rem;">4-7-8</div>
                <div style="color:#94a3b8;font-size:0.7rem;">Nefes Al-Tut-Ver</div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.caption("Sinav oncesi 5 dk, sinav sirasinda panik aninda 1 tur uygulayabilirsiniz.")


# ════════════════════════════════════════════════════════════
# 2. AKRAN KOÇLUK & GRUP DİNAMİĞİ PANELİ
# ════════════════════════════════════════════════════════════

def render_akran_kocluk(store):
    """Akran Koçluk — peer coaching, grup çalışma, eşleştirme, dinamik analiz."""
    styled_section("Akran Kocluk & Grup Dinamigi Paneli", "#059669")
    styled_info_banner(
        "Basarili ogrencilerin dusuk performanslilara kocluk yaptigi sistem. "
        "Akran eslestirme, grup calisma odalari, grup hedefi.",
        banner_type="info", icon="📊")

    akran_eslestirmeler = _lj("akran_eslestirme.json")
    grup_calisma = _lj("grup_calisma.json")

    sub = st.tabs(["🤝 Akran Eslestir", "👥 Grup Olustur", "📊 Grup Dinamigi", "🏆 En Etkili Gruplar"])

    with sub[0]:
        styled_section("Akran Koc Eslestirme")
        with st.form("akran_form"):
            c1, c2 = st.columns(2)
            with c1:
                a_koc = st.text_input("Akran Koc (basarili ogrenci)", key="ak_koc")
                a_ders = st.selectbox("Ders",
                    ["Matematik","Turkce","Fen","Sosyal","Ingilizce","Fizik","Kimya","Biyoloji"], key="ak_ders")
            with c2:
                a_ogrenci = st.text_input("Koçluk Alan Ogrenci", key="ak_ogr")
                a_hedef = st.text_input("Hedef", placeholder="Geometri netini 5 artirmak", key="ak_hedef")

            if st.form_submit_button("Eslesme Olustur", use_container_width=True):
                if a_koc and a_ogrenci:
                    akran_eslestirmeler.append({
                        "id": f"ak_{uuid.uuid4().hex[:8]}",
                        "koc": a_koc, "ogrenci": a_ogrenci,
                        "ders": a_ders, "hedef": a_hedef,
                        "durum": "Aktif", "tarih": date.today().isoformat(),
                    })
                    _sj("akran_eslestirme.json", akran_eslestirmeler)
                    st.success(f"🤝 {a_koc} → {a_ogrenci} eslesmesi olusturuldu!")
                    st.rerun()

        if akran_eslestirmeler:
            styled_section("Aktif Eslesmeler")
            for a in akran_eslestirmeler:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="color:#10b981;font-weight:700;font-size:0.8rem;">🤝 {a.get('koc','')}</span>
                    <span style="color:#94a3b8;">→</span>
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.8rem;">{a.get('ogrenci','')}</span>
                    <span style="color:#64748b;font-size:0.68rem;margin-left:auto;">{a.get('ders','')} | {a.get('hedef','')[:25]}</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Grup Calisma Odasi Olustur")
        with st.form("grup_form"):
            c1, c2 = st.columns(2)
            with c1:
                g_ad = st.text_input("Grup Adi", placeholder="Geometri Calisma Grubu", key="gc_ad")
                g_ders = st.selectbox("Ders", ["Matematik","Turkce","Fen","Sosyal","Ingilizce"], key="gc_ders")
            with c2:
                g_hedef = st.text_input("Grup Hedefi", key="gc_hedef")
                g_gun = st.selectbox("Calisma Gunu", ["Pazartesi","Sali","Carsamba","Persembe","Cuma","Cumartesi"], key="gc_gun")
            g_uyeler = st.text_area("Uyeler (her satira bir)", height=60, key="gc_uye")

            if st.form_submit_button("Grup Olustur", use_container_width=True):
                if g_ad:
                    uyeler = [u.strip() for u in g_uyeler.split("\n") if u.strip()]
                    grup_calisma.append({
                        "id": f"gc_{uuid.uuid4().hex[:8]}",
                        "ad": g_ad, "ders": g_ders, "hedef": g_hedef,
                        "gun": g_gun, "uyeler": uyeler,
                        "oturum_sayisi": 0, "durum": "Aktif",
                        "tarih": date.today().isoformat(),
                    })
                    _sj("grup_calisma.json", grup_calisma)
                    st.success(f"👥 {g_ad} — {len(uyeler)} uye ile olusturuldu!")
                    st.rerun()

        if grup_calisma:
            for g in grup_calisma:
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #059669;border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">👥 {g.get('ad','')}</span>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {g.get('ders','')} | {g.get('gun','')} | {len(g.get('uyeler',[]))} uye | Hedef: {g.get('hedef','')[:30]}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Grup Dinamigi Analizi")
        if grup_calisma:
            for g in grup_calisma:
                uye_say = len(g.get("uyeler", []))
                oturum = g.get("oturum_sayisi", 0)
                st.markdown(f"**{g.get('ad','')}**: {uye_say} uye, {oturum} oturum")
        else:
            st.info("Grup yok.")

    with sub[3]:
        styled_section("En Etkili Calisma Gruplari")
        if grup_calisma:
            sirali = sorted(grup_calisma, key=lambda x: x.get("oturum_sayisi",0), reverse=True)
            for sira, g in enumerate(sirali[:5], 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{g.get('ad','')}</span>
                    <span style="color:#059669;font-weight:700;">{g.get('oturum_sayisi',0)} oturum</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Grup verisi yok.")


# ════════════════════════════════════════════════════════════
# 3. KOÇLUK DÖNGÜSÜ & ETKİNLİK ÖLÇÜM MOTORU
# ════════════════════════════════════════════════════════════

def render_kocluk_dongusu(store):
    """Koçluk Döngüsü — başlangıç→müdahale→sonuç→etkinlik skoru."""
    styled_section("Kocluk Dongusu & Etkinlik Olcum Motoru", "#f59e0b")
    styled_info_banner(
        "Her kocluk surecinin sistematik olcumu: Baslangic → Mudahale → Sonuc → Etkinlik. "
        "Yontem karsilastirma, donem sonu etki raporu.",
        banner_type="info", icon="🔄")

    dongular = _lj("kocluk_donguleri.json")

    sub = st.tabs(["➕ Yeni Dongu", "📋 Dongu Takip", "📊 Yontem Karsilastir", "📈 Donem Raporu"])

    with sub[0]:
        styled_section("Yeni Kocluk Dongusu Baslat")
        with st.form("dongu_form"):
            c1, c2 = st.columns(2)
            with c1:
                d_ogr = st.text_input("Ogrenci", key="kd_ogr")
                d_yaklasim = st.selectbox("Kocluk Yaklasimi", list(_KOCLUK_YAKLASIMLARI.keys()), key="kd_yak")
                d_bas_net = st.number_input("Baslangic Net", 0.0, 100.0, 20.0, step=0.5, key="kd_bnet")
            with c2:
                d_bas_motivasyon = st.slider("Baslangic Motivasyon (1-10)", 1, 10, 5, key="kd_bmot")
                d_bas_devamsizlik = st.number_input("Baslangic Devamsizlik (gun)", 0, 30, 5, key="kd_bdev")
                d_sure = st.selectbox("Planlanan Sure", ["4 Hafta","8 Hafta","12 Hafta","1 Donem"], key="kd_sure")
            d_hedef = st.text_input("Hedef", placeholder="Net 30'a cikmak, motivasyon 8+", key="kd_hedef")

            if st.form_submit_button("Donguyu Baslat", use_container_width=True, type="primary"):
                if d_ogr:
                    dongular.append({
                        "id": f"kd_{uuid.uuid4().hex[:8]}",
                        "ogrenci": d_ogr, "yaklasim": d_yaklasim,
                        "baslangic": {"net": d_bas_net, "motivasyon": d_bas_motivasyon, "devamsizlik": d_bas_devamsizlik},
                        "sonuc": None, "hedef": d_hedef, "sure": d_sure,
                        "durum": "Devam Ediyor",
                        "tarih": date.today().isoformat(),
                    })
                    _sj("kocluk_donguleri.json", dongular)
                    st.success(f"🔄 {d_ogr} — {d_yaklasim} kocluk dongusu baslatildi!")
                    st.rerun()

    with sub[1]:
        styled_section("Kocluk Dongusu Takip")
        if not dongular:
            st.info("Dongu yok.")
        else:
            for d in sorted(dongular, key=lambda x: x.get("tarih",""), reverse=True):
                yak_info = _KOCLUK_YAKLASIMLARI.get(d.get("yaklasim",""), {"ikon":"🔄","renk":"#94a3b8"})
                bas = d.get("baslangic", {})
                sonuc = d.get("sonuc")

                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {yak_info['renk']};border-radius:0 14px 14px 0;
                    padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">{yak_info['ikon']} {d.get('ogrenci','')}</span>
                        <span style="color:{yak_info['renk']};font-size:0.72rem;font-weight:700;">{d.get('yaklasim','')} | {d.get('sure','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        Baslangic: Net {bas.get('net',0)} | Motivasyon {bas.get('motivasyon',0)}/10 | Devamsizlik {bas.get('devamsizlik',0)}g</div>
                    {f"<div style='color:#10b981;font-size:0.72rem;margin-top:2px;'>Sonuc: Net {sonuc.get('net',0)} | Motivasyon {sonuc.get('motivasyon',0)}/10 | Devamsizlik {sonuc.get('devamsizlik',0)}g</div>" if sonuc else "<div style='color:#f59e0b;font-size:0.68rem;margin-top:2px;'>Devam ediyor...</div>"}
                </div>""", unsafe_allow_html=True)

                if d.get("durum") == "Devam Ediyor":
                    with st.expander(f"Sonuc Gir: {d.get('id','')}", expanded=False):
                        with st.form(f"sonuc_{d['id']}"):
                            sc1, sc2 = st.columns(2)
                            with sc1:
                                s_net = st.number_input("Sonuc Net", 0.0, 100.0, bas.get("net",0)+5, step=0.5, key=f"sn_{d['id']}")
                                s_mot = st.slider("Sonuc Motivasyon", 1, 10, min(bas.get("motivasyon",5)+2, 10), key=f"sm_{d['id']}")
                            with sc2:
                                s_dev = st.number_input("Sonuc Devamsizlik", 0, 30, max(bas.get("devamsizlik",5)-2, 0), key=f"sd_{d['id']}")

                            if st.form_submit_button("Sonucu Kaydet"):
                                d["sonuc"] = {"net": s_net, "motivasyon": s_mot, "devamsizlik": s_dev}
                                d["durum"] = "Tamamlandi"

                                # Etkinlik skoru hesapla
                                net_artis = s_net - bas.get("net", 0)
                                mot_artis = s_mot - bas.get("motivasyon", 0)
                                dev_azalma = bas.get("devamsizlik", 0) - s_dev
                                etkinlik = round(min(100, max(0, net_artis * 3 + mot_artis * 5 + dev_azalma * 4)))
                                d["etkinlik_skoru"] = etkinlik

                                _sj("kocluk_donguleri.json", dongular)
                                renk = "#10b981" if etkinlik >= 60 else "#f59e0b" if etkinlik >= 30 else "#ef4444"
                                st.success(f"Etkinlik Skoru: {etkinlik}/100")
                                st.rerun()

    with sub[2]:
        styled_section("Kocluk Yaklasimi Karsilastirmasi")
        tamamlanan = [d for d in dongular if d.get("durum") == "Tamamlandi" and d.get("etkinlik_skoru") is not None]
        if not tamamlanan:
            st.info("Tamamlanan dongu yok.")
        else:
            yak_etkinlik = defaultdict(list)
            for d in tamamlanan:
                yak_etkinlik[d.get("yaklasim","")].append(d.get("etkinlik_skoru", 0))

            sirali = sorted(yak_etkinlik.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
            for sira, (yak, skorlar) in enumerate(sirali, 1):
                ort = round(sum(skorlar) / max(len(skorlar), 1))
                info = _KOCLUK_YAKLASIMLARI.get(yak, {"ikon":"🔄","renk":"#94a3b8"})
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                renk = "#10b981" if ort >= 60 else "#f59e0b" if ort >= 30 else "#ef4444"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                    background:#0f172a;border-left:5px solid {info['renk']};border-radius:0 12px 12px 0;padding:10px 16px;">
                    <span style="font-size:1.1rem;">{madalya}</span>
                    <span style="font-size:1rem;">{info['ikon']}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{yak}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{ort}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">%{ort}</span></div></div>
                    <span style="color:#64748b;font-size:0.65rem;">{len(skorlar)} dongu</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Donem Sonu Kocluk Etki Raporu")
        tamamlanan = [d for d in dongular if d.get("durum") == "Tamamlandi"]
        if not tamamlanan:
            st.info("Tamamlanan dongu yok.")
        else:
            toplam_net = sum(d.get("sonuc",{}).get("net",0) - d.get("baslangic",{}).get("net",0) for d in tamamlanan)
            toplam_mot = sum(d.get("sonuc",{}).get("motivasyon",0) - d.get("baslangic",{}).get("motivasyon",0) for d in tamamlanan)
            ort_etkinlik = round(sum(d.get("etkinlik_skoru",0) for d in tamamlanan) / max(len(tamamlanan), 1))
            renk = "#10b981" if ort_etkinlik >= 60 else "#f59e0b" if ort_etkinlik >= 30 else "#ef4444"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,{renk}15);border:2px solid {renk};
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">Donem Kocluk Etki Raporu</div>
                <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                    <div><div style="color:#3b82f6;font-weight:900;font-size:1.8rem;">{len(tamamlanan)}</div><div style="color:#64748b;font-size:0.62rem;">Dongu</div></div>
                    <div><div style="color:#10b981;font-weight:900;font-size:1.8rem;">+{round(toplam_net,1)}</div><div style="color:#64748b;font-size:0.62rem;">Toplam Net Artis</div></div>
                    <div><div style="color:#8b5cf6;font-weight:900;font-size:1.8rem;">+{toplam_mot}</div><div style="color:#64748b;font-size:0.62rem;">Motivasyon Artis</div></div>
                    <div><div style="color:{renk};font-weight:900;font-size:1.8rem;">{ort_etkinlik}%</div><div style="color:#64748b;font-size:0.62rem;">Ort Etkinlik</div></div>
                </div>
            </div>""", unsafe_allow_html=True)
