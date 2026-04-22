"""
Sosyal Etkinlik ve Kulüpler — Zirve Özellikler
================================================
1. Okul Medya Merkezi & Dijital İçerik Stüdyosu
2. Okul Dışı İşbirliği & Kurumlar Arası Proje
3. İnovasyon & Girişimcilik Kulübü Ekosistemi
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

_ICERIK_TURLERI = ["Haber", "Roportaj", "Kose Yazisi", "Podcast", "Video", "Fotograf", "Infografik", "Blog Yazisi", "Dergi Makalesi", "Diger"]
_ICERIK_DURUMLARI = ["Taslak", "Editorde", "Onaylandi", "Yayinlandi"]
_ICERIK_DURUM_RENK = {"Taslak": "#94a3b8", "Editorde": "#f59e0b", "Onaylandi": "#3b82f6", "Yayinlandi": "#10b981"}
_MEDYA_ROLLER = ["Muhabir", "Editor", "Kameraman", "Fotografci", "Sunucu", "Grafiker", "Sosyal Medya", "Yayin Yonetmeni"]

_DIS_ETKINLIK_TURLERI = ["MUN (Model United Nations)", "TEDx", "Hackathon", "Bilim Olimpiyadi",
    "Spor Musabakasi", "Sanat Festivali", "Muzik Yarismasi", "Robotik Yarisma",
    "Debate / Munazara", "Ogrenci Degisimi", "Universite Ziyareti",
    "Staj / Is Deneyimi", "Sosyal Sorumluluk Ortakligi", "Diger"]
_ISBIRLIGI_DURUMLARI = ["Planlandi", "Aktif", "Tamamlandi", "Askiya Alindi"]
_ISBIRLIGI_DURUM_RENK = {"Planlandi": "#3b82f6", "Aktif": "#10b981", "Tamamlandi": "#8b5cf6", "Askiya Alindi": "#94a3b8"}

_FIKIR_ASAMALARI = ["Fikir", "Arastirma", "Prototip", "Test", "Sunum", "Uygulama"]
_FIKIR_ASAMA_RENK = {"Fikir": "#94a3b8", "Arastirma": "#3b82f6", "Prototip": "#f59e0b", "Test": "#8b5cf6", "Sunum": "#059669", "Uygulama": "#10b981"}
_INOVASYON_KATEGORILERI = ["Teknoloji", "Sosyal Etki", "Cevre / Surdurulebilirlik", "Egitim",
    "Saglik", "Sanat / Tasarim", "Gida / Tarim", "Finans", "Diger"]


# ════════════════════════════════════════════════════════════
# 1. OKUL MEDYA MERKEZİ & DİJİTAL İÇERİK STÜDYOSU
# ════════════════════════════════════════════════════════════

def render_medya_merkezi(store):
    """Okul Medya Merkezi — gazete, dergi, podcast, video, blog yönetimi."""
    styled_section("Okul Medya Merkezi & Dijital Icerik Studyosu", "#2563eb")
    styled_info_banner(
        "Ogrenci gazetesi, okul dergisi, podcast, YouTube, blog yonetimi. "
        "Icerik takvimi, editor onay akisi, yayin arsivi, basin karti.",
        banner_type="info", icon="📡")

    icerikler = _lj("medya_icerikler.json")
    ekip = _lj("medya_ekip.json")

    # KPI
    yayinlanan = sum(1 for i in icerikler if i.get("durum") == "Yayinlandi")
    bu_ay = sum(1 for i in icerikler if i.get("tarih","")[:7] == date.today().strftime("%Y-%m"))
    tur_say = len(set(i.get("tur","") for i in icerikler))

    styled_stat_row([
        ("Toplam Icerik", str(len(icerikler)), "#2563eb", "📝"),
        ("Yayinlanan", str(yayinlanan), "#10b981", "📢"),
        ("Bu Ay", str(bu_ay), "#f59e0b", "📅"),
        ("Icerik Turu", str(tur_say), "#8b5cf6", "🏷️"),
        ("Ekip Uyesi", str(len(ekip)), "#059669", "👥"),
    ])

    sub = st.tabs(["📝 Icerik Olustur", "📋 Yayin Listesi", "👥 Medya Ekibi", "📅 Icerik Takvimi", "📊 Analitik"])

    # ── İÇERİK OLUŞTUR ──
    with sub[0]:
        styled_section("Yeni Icerik Olustur")
        with st.form("icerik_form"):
            c1, c2 = st.columns(2)
            with c1:
                i_baslik = st.text_input("Baslik", key="md_baslik")
                i_tur = st.selectbox("Tur", _ICERIK_TURLERI, key="md_tur")
                i_yazar = st.text_input("Yazar / Muhabir", key="md_yazar")
            with c2:
                i_editor = st.text_input("Editor", key="md_editor")
                i_kanal = st.selectbox("Yayin Kanali",
                    ["Okul Gazetesi", "Okul Dergisi", "Podcast", "YouTube", "Instagram", "Blog", "Web Sitesi"],
                    key="md_kanal")
                i_tarih = st.date_input("Planlanan Yayin", key="md_tarih")

            i_ozet = st.text_area("Icerik Ozeti", height=80, key="md_ozet")
            i_link = st.text_input("Icerik Linki (varsa)", key="md_link")

            if st.form_submit_button("Olustur", use_container_width=True, type="primary"):
                if i_baslik:
                    icerikler.append({
                        "id": f"md_{uuid.uuid4().hex[:8]}",
                        "baslik": i_baslik, "tur": i_tur, "yazar": i_yazar,
                        "editor": i_editor, "kanal": i_kanal,
                        "ozet": i_ozet, "link": i_link,
                        "durum": "Taslak",
                        "tarih": i_tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("medya_icerikler.json", icerikler)
                    st.success(f"'{i_baslik}' taslak olarak olusturuldu!")
                    st.rerun()

    # ── YAYIN LİSTESİ ──
    with sub[1]:
        styled_section("Icerik & Yayin Listesi")
        if not icerikler:
            st.info("Icerik yok.")
        else:
            for i in sorted(icerikler, key=lambda x: x.get("tarih",""), reverse=True):
                d_renk = _ICERIK_DURUM_RENK.get(i.get("durum",""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {d_renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">📝 {i.get('baslik','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{i.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        {i.get('tur','')} | {i.get('kanal','')} | Yazar: {i.get('yazar','')} | {i.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Durum: {i.get('id','')}", expanded=False):
                    yeni = st.selectbox("Durum", _ICERIK_DURUMLARI,
                        index=_ICERIK_DURUMLARI.index(i.get("durum","Taslak")) if i.get("durum") in _ICERIK_DURUMLARI else 0,
                        key=f"md_d_{i['id']}")
                    if st.button("Guncelle", key=f"md_g_{i['id']}"):
                        i["durum"] = yeni
                        _sj("medya_icerikler.json", icerikler)
                        st.rerun()

    # ── MEDYA EKİBİ ──
    with sub[2]:
        styled_section("Medya Ekibi Yonetimi")
        with st.form("ekip_form"):
            c1, c2 = st.columns(2)
            with c1:
                e_ad = st.text_input("Ogrenci Adi", key="ek_ad")
                e_rol = st.selectbox("Rol", _MEDYA_ROLLER, key="ek_rol")
            with c2:
                e_sinif = st.text_input("Sinif/Sube", key="ek_sinif")

            if st.form_submit_button("Ekibe Ekle", use_container_width=True):
                if e_ad:
                    ekip.append({"ad": e_ad, "rol": e_rol, "sinif": e_sinif,
                                 "created_at": datetime.now().isoformat()})
                    _sj("medya_ekip.json", ekip)
                    st.success(f"{e_ad} — {e_rol} olarak eklendi!")
                    st.rerun()

        if ekip:
            rol_grp = defaultdict(list)
            for e in ekip:
                rol_grp[e.get("rol","?")].append(e)
            for rol, uyeler in rol_grp.items():
                st.markdown(f"**{rol}** ({len(uyeler)})")
                for u in uyeler:
                    st.markdown(f"  - {u.get('ad','')} ({u.get('sinif','')})")

    # ── İÇERİK TAKVİMİ ──
    with sub[3]:
        styled_section("Aylik Icerik Takvimi")
        if not icerikler:
            st.info("Icerik yok.")
        else:
            ay_grp = defaultdict(list)
            for i in icerikler:
                ay = i.get("tarih","")[:7]
                if ay:
                    ay_grp[ay].append(i)

            for ay in sorted(ay_grp.keys())[-6:]:
                items = ay_grp[ay]
                st.markdown(f"**{ay}** — {len(items)} icerik")
                for i in sorted(items, key=lambda x: x.get("tarih","")):
                    d_renk = _ICERIK_DURUM_RENK.get(i.get("durum",""), "#94a3b8")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;padding:3px 12px;margin:1px 0;
                        border-left:2px solid {d_renk};">
                        <span style="min-width:50px;color:#64748b;font-size:0.62rem;">{i.get('tarih','')[:10]}</span>
                        <span style="color:#e2e8f0;font-size:0.72rem;font-weight:600;flex:1;">{i.get('baslik','')[:35]}</span>
                        <span style="color:#94a3b8;font-size:0.6rem;">{i.get('tur','')}</span>
                    </div>""", unsafe_allow_html=True)

    # ── ANALİTİK ──
    with sub[4]:
        styled_section("Medya Analitikleri")
        if icerikler:
            tur_say = Counter(i.get("tur","") for i in icerikler)
            styled_section("Icerik Turu Dagilimi")
            for tur, sayi in tur_say.most_common():
                pct = round(sayi / max(len(icerikler), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:120px;font-size:0.78rem;color:#e2e8f0;font-weight:600;">{tur}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#2563eb;border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi} (%{pct})</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            kanal_say = Counter(i.get("kanal","") for i in icerikler)
            styled_section("Kanal Dagilimi")
            for kanal, sayi in kanal_say.most_common():
                st.markdown(f"""
                <div style="display:inline-block;background:#2563eb10;border:1px solid #2563eb30;
                    padding:6px 14px;border-radius:10px;margin:3px;font-size:0.8rem;">
                    📢 {kanal}: <b style="color:#2563eb;">{sayi}</b>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. OKUL DIŞI İŞBİRLİĞİ & KURUMLAR ARASI PROJE
# ════════════════════════════════════════════════════════════

def render_dis_isbirligi(store):
    """Okul Dışı İşbirliği — MUN, TEDx, hackathon, mezun ağı, protokol arşivi."""
    styled_section("Okul Disi Isbirligi & Kurumlar Arasi Proje", "#0891b2")
    styled_info_banner(
        "Diger okullarla ortak proje, MUN/TEDx/Hackathon katilim, "
        "universite isbirligi, mezun agi, protokol arsivi.",
        banner_type="info", icon="🌐")

    isbirlikler = _lj("dis_isbirlikler.json")
    katilimlar = _lj("dis_katilim.json")
    alumni = _lj("mezun_agi.json")

    # KPI
    aktif = sum(1 for i in isbirlikler if i.get("durum") == "Aktif")
    toplam_katilim = sum(k.get("ogrenci_sayi", 0) for k in katilimlar)

    styled_stat_row([
        ("Isbirligi", str(len(isbirlikler)), "#0891b2", "🤝"),
        ("Aktif", str(aktif), "#10b981", "🟢"),
        ("Dis Katilim", str(len(katilimlar)), "#3b82f6", "🌍"),
        ("Ogrenci", str(toplam_katilim), "#8b5cf6", "👥"),
        ("Mezun Agi", str(len(alumni)), "#f59e0b", "🎓"),
    ])

    sub = st.tabs(["🤝 Yeni Isbirligi", "📋 Isbirligi Listesi", "🌍 Dis Katilim", "🎓 Mezun Agi", "📄 Protokol Arsivi"])

    # ── YENİ İŞBİRLİĞİ ──
    with sub[0]:
        styled_section("Yeni Isbirligi / Protokol")
        with st.form("isb_form"):
            c1, c2 = st.columns(2)
            with c1:
                ib_kurum = st.text_input("Partner Kurum", placeholder="XYZ Koleji, ABC Universitesi...", key="ib_kurum")
                ib_tur = st.selectbox("Isbirligi Turu", _DIS_ETKINLIK_TURLERI, key="ib_tur")
                ib_bas = st.date_input("Baslangic", key="ib_bas")
            with c2:
                ib_sorumlu = st.text_input("Sorumlu", key="ib_sor")
                ib_kapsam = st.selectbox("Kapsam", ["Yerel", "Bolgesel", "Ulusal", "Uluslararasi"], key="ib_kapsam")
                ib_bit = st.date_input("Bitis", key="ib_bit")
            ib_aciklama = st.text_area("Aciklama / Hedefler", height=60, key="ib_acik")

            if st.form_submit_button("Kaydet", use_container_width=True, type="primary"):
                if ib_kurum:
                    isbirlikler.append({
                        "id": f"ib_{uuid.uuid4().hex[:8]}",
                        "kurum": ib_kurum, "tur": ib_tur, "kapsam": ib_kapsam,
                        "sorumlu": ib_sorumlu, "aciklama": ib_aciklama,
                        "baslangic": ib_bas.isoformat(), "bitis": ib_bit.isoformat(),
                        "durum": "Aktif", "created_at": datetime.now().isoformat(),
                    })
                    _sj("dis_isbirlikler.json", isbirlikler)
                    st.success(f"{ib_kurum} isbirligi kaydedildi!")
                    st.rerun()

    # ── İŞBİRLİĞİ LİSTESİ ──
    with sub[1]:
        styled_section("Isbirligi & Protokol Listesi")
        if not isbirlikler:
            st.info("Kayit yok.")
        else:
            for ib in sorted(isbirlikler, key=lambda x: x.get("baslangic",""), reverse=True):
                d_renk = _ISBIRLIGI_DURUM_RENK.get(ib.get("durum",""), "#94a3b8")
                kapsam_badge = "🌍" if ib.get("kapsam") == "Uluslararasi" else "🇹🇷" if ib.get("kapsam") == "Ulusal" else "🏛️"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {d_renk};border-radius:0 14px 14px 0;
                    padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🤝 {ib.get('kurum','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:3px 10px;border-radius:8px;
                            font-size:0.7rem;font-weight:700;">{ib.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        {kapsam_badge} {ib.get('kapsam','')} | {ib.get('tur','')} |
                        {ib.get('baslangic','')[:10]} → {ib.get('bitis','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    # ── DIŞ KATILIM ──
    with sub[2]:
        styled_section("Dis Etkinlik Katilim Kaydi")
        with st.form("dis_kat_form"):
            c1, c2 = st.columns(2)
            with c1:
                dk_etkinlik = st.text_input("Etkinlik Adi", placeholder="MUN Istanbul 2026", key="dk_etk")
                dk_tur = st.selectbox("Tur", _DIS_ETKINLIK_TURLERI, key="dk_tur")
            with c2:
                dk_tarih = st.date_input("Tarih", key="dk_tarih")
                dk_sayi = st.number_input("Katilan Ogrenci Sayisi", min_value=1, value=5, key="dk_sayi")
            dk_sonuc = st.text_input("Sonuc / Derece", placeholder="3. oldu, Mansiyon, Katilim...", key="dk_sonuc")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if dk_etkinlik:
                    katilimlar.append({
                        "id": f"dk_{uuid.uuid4().hex[:8]}",
                        "etkinlik": dk_etkinlik, "tur": dk_tur,
                        "tarih": dk_tarih.isoformat(), "ogrenci_sayi": dk_sayi,
                        "sonuc": dk_sonuc, "created_at": datetime.now().isoformat(),
                    })
                    _sj("dis_katilim.json", katilimlar)
                    st.success(f"{dk_etkinlik} katilimi kaydedildi!")
                    st.rerun()

        if katilimlar:
            for k in sorted(katilimlar, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #0891b2;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🌍 {k.get('etkinlik','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{k.get('ogrenci_sayi',0)} ogr</span>
                    <span style="color:#10b981;font-size:0.68rem;font-weight:700;">{k.get('sonuc','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── MEZUN AĞI ──
    with sub[3]:
        styled_section("Mezun Agi (Alumni)")
        with st.form("alumni_form"):
            c1, c2 = st.columns(2)
            with c1:
                al_ad = st.text_input("Mezun Adi", key="al_ad")
                al_mezuniyet = st.text_input("Mezuniyet Yili", key="al_mez")
            with c2:
                al_universite = st.text_input("Universite / Is", key="al_uni")
                al_alan = st.text_input("Alan / Bolum", key="al_alan")
            al_iletisim = st.text_input("Iletisim (email/telefon)", key="al_iletisim")
            al_mentor = st.checkbox("Mentorluk yapmak istiyor mu?", key="al_mentor")

            if st.form_submit_button("Ekle", use_container_width=True):
                if al_ad:
                    alumni.append({
                        "ad": al_ad, "mezuniyet": al_mezuniyet,
                        "universite": al_universite, "alan": al_alan,
                        "iletisim": al_iletisim, "mentor": al_mentor,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("mezun_agi.json", alumni)
                    st.success(f"{al_ad} mezun agina eklendi!")
                    st.rerun()

        if alumni:
            styled_section(f"Mezun Listesi ({len(alumni)})")
            for a in alumni:
                mentor_badge = "🧑‍🏫 Mentor" if a.get("mentor") else ""
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🎓 {a.get('ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{a.get('mezuniyet','')} | {a.get('universite','')}</span>
                    <span style="color:#f59e0b;font-size:0.62rem;font-weight:700;">{mentor_badge}</span>
                </div>""", unsafe_allow_html=True)

    # ── PROTOKOL ARŞİVİ ──
    with sub[4]:
        styled_section("Protokol & Anlasma Arsivi")
        if isbirlikler:
            tur_say = Counter(ib.get("tur","") for ib in isbirlikler)
            for tur, sayi in tur_say.most_common():
                st.markdown(f"- **{tur}**: {sayi} isbirligi")
            kapsam_say = Counter(ib.get("kapsam","") for ib in isbirlikler)
            styled_section("Kapsam Dagilimi")
            for kapsam, sayi in kapsam_say.most_common():
                badge = "🌍" if kapsam == "Uluslararasi" else "🇹🇷" if kapsam == "Ulusal" else "🏛️" if kapsam == "Bolgesel" else "🏫"
                st.markdown(f"  {badge} **{kapsam}**: {sayi}")
        else:
            st.info("Protokol kaydi yok.")


# ════════════════════════════════════════════════════════════
# 3. İNOVASYON & GİRİŞİMCİLİK KULÜBÜ EKOSİSTEMİ
# ════════════════════════════════════════════════════════════

def render_inovasyon_ekosistemi(store):
    """İnovasyon & Girişimcilik — startup fikir, prototip, pitch, mentor eşleştirme."""
    styled_section("Inovasyon & Girisimcilik Kulubu Ekosistemi", "#8b5cf6")
    styled_info_banner(
        "Ogrenci startup fikirleri, prototip gelistirme, pitch gunu, "
        "mentor eslestirme, juri degerlendirme.",
        banner_type="info", icon="🚀")

    fikirler = _lj("inovasyon_fikirler.json")
    mentorler = _lj("inovasyon_mentorler.json")
    degerlendirmeler = _lj("inovasyon_degerlendirme.json")

    # KPI
    prototip = sum(1 for f in fikirler if f.get("asama") in ("Prototip", "Test", "Sunum", "Uygulama"))
    odul = sum(1 for d in degerlendirmeler if d.get("odul"))

    styled_stat_row([
        ("Fikir", str(len(fikirler)), "#8b5cf6", "💡"),
        ("Prototip+", str(prototip), "#f59e0b", "🔨"),
        ("Mentor", str(len(mentorler)), "#059669", "🧑‍🏫"),
        ("Odul", str(odul), "#c9a84c", "🏆"),
    ])

    sub = st.tabs(["💡 Fikir Havuzu", "🔨 Proje Takip", "🧑‍🏫 Mentor", "📊 Juri & Pitch", "🏆 Basari Arsivi"])

    # ── FİKİR HAVUZU ──
    with sub[0]:
        styled_section("Startup Fikir Havuzu")
        with st.form("fikir_form"):
            c1, c2 = st.columns(2)
            with c1:
                f_ad = st.text_input("Proje Adi", key="fk_ad")
                f_ekip = st.text_input("Ekip Uyeleri", placeholder="Ali, Ayse, Mehmet", key="fk_ekip")
                f_kat = st.selectbox("Kategori", _INOVASYON_KATEGORILERI, key="fk_kat")
            with c2:
                f_problem = st.text_input("Cozulen Problem", key="fk_problem")
                f_cozum = st.text_input("Onerilen Cozum", key="fk_cozum")
                f_hedef = st.text_input("Hedef Kitle", key="fk_hedef")
            f_aciklama = st.text_area("Detayli Aciklama", height=60, key="fk_acik")

            if st.form_submit_button("Fikri Kaydet", use_container_width=True, type="primary"):
                if f_ad:
                    ekip_list = [e.strip() for e in f_ekip.split(",") if e.strip()]
                    fikirler.append({
                        "id": f"fk_{uuid.uuid4().hex[:8]}",
                        "ad": f_ad, "ekip": ekip_list, "kategori": f_kat,
                        "problem": f_problem, "cozum": f_cozum, "hedef_kitle": f_hedef,
                        "aciklama": f_aciklama, "asama": "Fikir",
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("inovasyon_fikirler.json", fikirler)
                    st.success(f"'{f_ad}' fikir havuzuna eklendi!")
                    st.rerun()

        if fikirler:
            styled_section("Fikir Listesi")
            for f in sorted(fikirler, key=lambda x: x.get("created_at",""), reverse=True):
                a_renk = _FIKIR_ASAMA_RENK.get(f.get("asama",""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {a_renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">💡 {f.get('ad','')}</span>
                        <span style="background:{a_renk}20;color:{a_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{f.get('asama','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        {f.get('kategori','')} | Ekip: {', '.join(f.get('ekip',[]))} | Problem: {f.get('problem','')[:40]}</div>
                </div>""", unsafe_allow_html=True)

    # ── PROJE TAKİP ──
    with sub[1]:
        styled_section("Proje Asama Takibi")
        if not fikirler:
            st.info("Fikir yok.")
        else:
            for f in fikirler:
                with st.expander(f"💡 {f.get('ad','')} ({f.get('asama','')})"):
                    # Asama pipeline
                    for idx, asama in enumerate(_FIKIR_ASAMALARI):
                        mevcut_idx = _FIKIR_ASAMALARI.index(f.get("asama","Fikir")) if f.get("asama") in _FIKIR_ASAMALARI else 0
                        renk = "#10b981" if idx <= mevcut_idx else "#334155"
                        ikon = "✅" if idx < mevcut_idx else "🔵" if idx == mevcut_idx else "⬜"
                        st.markdown(f"{ikon} **{asama}**")

                    yeni_asama = st.selectbox("Asamayi Guncelle", _FIKIR_ASAMALARI,
                        index=_FIKIR_ASAMALARI.index(f.get("asama","Fikir")) if f.get("asama") in _FIKIR_ASAMALARI else 0,
                        key=f"fk_a_{f['id']}")
                    if st.button("Guncelle", key=f"fk_g_{f['id']}"):
                        f["asama"] = yeni_asama
                        _sj("inovasyon_fikirler.json", fikirler)
                        st.rerun()

    # ── MENTOR ──
    with sub[2]:
        styled_section("Mentor Eslestirme")
        with st.form("mentor_form"):
            c1, c2 = st.columns(2)
            with c1:
                m_ad = st.text_input("Mentor Adi", key="mn_ad")
                m_uzmanlik = st.text_input("Uzmanlik Alani", key="mn_uz")
            with c2:
                m_kurum = st.text_input("Kurum / Sirket", key="mn_kurum")
                m_iletisim = st.text_input("Iletisim", key="mn_iletisim")

            if st.form_submit_button("Mentor Ekle", use_container_width=True):
                if m_ad:
                    mentorler.append({
                        "ad": m_ad, "uzmanlik": m_uzmanlik,
                        "kurum": m_kurum, "iletisim": m_iletisim,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("inovasyon_mentorler.json", mentorler)
                    st.success(f"{m_ad} mentor olarak eklendi!")
                    st.rerun()

        if mentorler:
            for m in mentorler:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🧑‍🏫 {m.get('ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{m.get('uzmanlik','')} | {m.get('kurum','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── JÜRİ & PİTCH ──
    with sub[3]:
        styled_section("Pitch Gunu & Juri Degerlendirme")
        if not fikirler:
            st.info("Fikir yok.")
        else:
            sunum_hazir = [f for f in fikirler if f.get("asama") in ("Sunum", "Uygulama")]
            if not sunum_hazir:
                st.info("Sunum asamasinda proje yok.")
            else:
                with st.form("juri_form"):
                    j_proje = st.selectbox("Proje", [f.get("ad","") for f in sunum_hazir], key="jr_proje")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        j_yenilik = st.slider("Yenilikcilik", 1, 10, 7, key="jr_yen")
                    with c2:
                        j_uygulanabilirlik = st.slider("Uygulanabilirlik", 1, 10, 7, key="jr_uyg")
                    with c3:
                        j_sunum = st.slider("Sunum Kalitesi", 1, 10, 7, key="jr_sun")
                    j_odul = st.checkbox("Odul Verilsin Mi?", key="jr_odul")
                    j_yorum = st.text_area("Juri Yorumu", height=40, key="jr_yorum")

                    if st.form_submit_button("Degerlendir", use_container_width=True):
                        toplam = round((j_yenilik + j_uygulanabilirlik + j_sunum) / 3, 1)
                        degerlendirmeler.append({
                            "proje": j_proje, "yenilik": j_yenilik,
                            "uygulanabilirlik": j_uygulanabilirlik, "sunum": j_sunum,
                            "toplam": toplam, "odul": j_odul, "yorum": j_yorum,
                            "tarih": datetime.now().isoformat(),
                        })
                        _sj("inovasyon_degerlendirme.json", degerlendirmeler)
                        st.success(f"{j_proje}: {toplam}/10{' 🏆 ODUL!' if j_odul else ''}")

        if degerlendirmeler:
            styled_section("Degerlendirme Sonuclari")
            for d in sorted(degerlendirmeler, key=lambda x: x.get("toplam",0), reverse=True):
                renk = "#c9a84c" if d.get("odul") else "#3b82f6"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">
                        {'🏆 ' if d.get('odul') else '💡 '}{d.get('proje','')}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.85rem;">{d.get('toplam','')}/10</span>
                </div>""", unsafe_allow_html=True)

    # ── BAŞARI ARŞİVİ ──
    with sub[4]:
        styled_section("Inovasyon Basari Arsivi")
        odullu = [d for d in degerlendirmeler if d.get("odul")]
        uygulamada = [f for f in fikirler if f.get("asama") == "Uygulama"]

        if odullu:
            styled_section("Odul Kazanan Projeler")
            for d in odullu:
                st.markdown(f"""
                <div style="background:#c9a84c08;border:1px solid #c9a84c30;border-left:5px solid #c9a84c;
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                    <span style="color:#c9a84c;font-weight:900;font-size:0.9rem;">🏆 {d.get('proje','')}</span>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">Puan: {d.get('toplam','')}/10</div>
                </div>""", unsafe_allow_html=True)

        if uygulamada:
            styled_section("Uygulama Asamasindaki Projeler")
            for f in uygulamada:
                st.markdown(f"- 🚀 **{f.get('ad','')}** — {', '.join(f.get('ekip',[]))}")

        # Asama dagilimi
        if fikirler:
            styled_section("Pipeline Ozeti")
            asama_say = Counter(f.get("asama","") for f in fikirler)
            for asama in _FIKIR_ASAMALARI:
                sayi = asama_say.get(asama, 0)
                renk = _FIKIR_ASAMA_RENK.get(asama, "#94a3b8")
                pct = round(sayi / max(len(fikirler), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:80px;font-size:0.78rem;color:#e2e8f0;font-weight:600;">{asama}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
