"""
STEAM Merkezi — Yeni Özellikler
=================================
1. Makerspace & Lab Envanter Yönetimi
2. TÜBİTAK & Bilim Fuarı Proje Yönetim
3. STEAM Portfolyo & Disiplinler Arası Kazanım Haritası
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
def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None

_MALZEME_KATEGORILERI = ["Elektronik", "Robotik", "3D Baski", "Mekanik", "Kimya/Biyoloji",
    "Kodlama/Bilisim", "Sanat/Tasarim", "Genel Lab", "Guvenlik Ekipmani"]
_MALZEME_DURUMLARI = ["Mevcut", "Oduncte", "Bakimda", "Bozuk", "Siparis"]
_MALZEME_DURUM_RENK = {"Mevcut":"#10b981","Oduncte":"#3b82f6","Bakimda":"#f59e0b","Bozuk":"#ef4444","Siparis":"#8b5cf6"}

_GUVENLIK_CHECKLIST = [
    "Koruyucu gozluk takti", "Is eldiveni giydi", "Calisma alani temizlendi",
    "Alet kontrolu yapildi", "Yangin sonduruce erisilebilir", "Ilk yardim cantasi hazir",
    "Havalandirma acik", "Ogretmen onay verdi",
]

_PROJE_PIPELINE = ["Fikir", "Arastirma", "Tasarim", "Prototip", "Test", "Sunum", "Yarisma", "Odul"]
_PROJE_RENK = {"Fikir":"#94a3b8","Arastirma":"#3b82f6","Tasarim":"#8b5cf6","Prototip":"#f59e0b",
    "Test":"#059669","Sunum":"#0891b2","Yarisma":"#ef4444","Odul":"#c9a84c"}

_YARISMA_TURLERI = ["TUBİTAK 4006", "TUBİTAK 4007", "Bilim Fuari", "Robotik Yarisma",
    "Hackathon", "Kodlama Yarismasi", "Mucit Cocuklar", "FLL (First Lego League)",
    "Maker Faire", "Ulusal Bilim Olimpiyadi", "Diger"]

_KAZANIM_MAP = {
    "Robotik": {"Fen": ["F.7.3.1","F.8.2.1"], "Matematik": ["M.7.2.4"], "Bilisim": ["B.7.1.2","B.8.1.3"]},
    "3D Tasarim": {"Matematik": ["M.6.3.1","M.7.3.2"], "Gorsel Sanatlar": ["GS.6.1.1"], "Bilisim": ["B.7.2.1"]},
    "Kodlama": {"Bilisim": ["B.5.1.1","B.6.1.2","B.7.1.1"], "Matematik": ["M.6.1.3"]},
    "Elektronik": {"Fen": ["F.6.4.1","F.7.4.2"], "Teknoloji": ["T.7.1.1"]},
    "Biyoloji Deneyi": {"Fen": ["F.5.3.1","F.6.3.2","F.7.3.1"]},
    "Kimya Deneyi": {"Fen": ["F.6.4.1","F.7.4.1","F.8.4.1"]},
    "Sanat+Teknoloji": {"Gorsel Sanatlar": ["GS.7.1.1"], "Bilisim": ["B.7.2.1"], "Muzik": ["MZ.7.1.1"]},
}

_STEAM_ALANLARI = {
    "Science": {"ikon":"🔬","renk":"#10b981"},
    "Technology": {"ikon":"💻","renk":"#3b82f6"},
    "Engineering": {"ikon":"🔧","renk":"#f59e0b"},
    "Art": {"ikon":"🎨","renk":"#8b5cf6"},
    "Mathematics": {"ikon":"🧮","renk":"#ef4444"},
}


# ════════════════════════════════════════════════════════════
# 1. MAKERSPACE & LAB ENVANTER YÖNETİMİ
# ════════════════════════════════════════════════════════════

def render_makerspace(store):
    """Makerspace & Lab Envanter — malzeme takip, ödünç, güvenlik, rezervasyon."""
    styled_section("Makerspace & Lab Envanter Yonetimi", "#f59e0b")
    styled_info_banner(
        "3D yazici, Arduino, robotik kit, devre malzemeleri envanter takibi. "
        "Odunc ver/iade, stok uyarisi, is guvenligi checklist, lab rezervasyon.",
        banner_type="info", icon="🔧")

    envanter = _lj("lab_envanter.json")
    odunc_log = _lj("lab_odunc.json")
    guvenlik_log = _lj("guvenlik_checklist.json")
    rezervasyonlar = _lj("lab_rezervasyon.json")

    mevcut = sum(1 for m in envanter if m.get("durum") == "Mevcut")
    oduncte = sum(1 for m in envanter if m.get("durum") == "Oduncte")
    bozuk = sum(1 for m in envanter if m.get("durum") in ("Bozuk","Bakimda"))

    styled_stat_row([
        ("Toplam Malzeme", str(len(envanter)), "#f59e0b", "📦"),
        ("Mevcut", str(mevcut), "#10b981", "✅"),
        ("Oduncte", str(oduncte), "#3b82f6", "🔄"),
        ("Bozuk/Bakim", str(bozuk), "#ef4444", "⚠️"),
    ])

    sub = st.tabs(["📦 Envanter", "🔄 Odunc/Iade", "🛡️ Guvenlik", "📅 Rezervasyon", "📊 Stok Analiz"])

    with sub[0]:
        styled_section("Lab Malzeme Envanter")
        with st.form("env_form"):
            c1, c2 = st.columns(2)
            with c1:
                m_ad = st.text_input("Malzeme Adi", placeholder="Arduino Mega 2560", key="env_ad")
                m_kat = st.selectbox("Kategori", _MALZEME_KATEGORILERI, key="env_kat")
                m_adet = st.number_input("Adet", 1, 100, 1, key="env_adet")
            with c2:
                m_konum = st.text_input("Konum", placeholder="Raf A-3, Dolap 2", key="env_konum")
                m_durum = st.selectbox("Durum", _MALZEME_DURUMLARI, key="env_durum")
                m_seri = st.text_input("Seri No (opsiyonel)", key="env_seri")

            if st.form_submit_button("Malzeme Ekle", use_container_width=True):
                if m_ad:
                    envanter.append({
                        "id": f"env_{uuid.uuid4().hex[:8]}",
                        "ad": m_ad, "kategori": m_kat, "adet": m_adet,
                        "konum": m_konum, "durum": m_durum, "seri_no": m_seri,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("lab_envanter.json", envanter)
                    st.success(f"📦 {m_ad} x{m_adet} eklendi!")
                    st.rerun()

        if envanter:
            kat_filtre = st.selectbox("Kategori Filtre", ["Tumu"] + _MALZEME_KATEGORILERI, key="env_f")
            filtreli = envanter if kat_filtre == "Tumu" else [m for m in envanter if m.get("kategori") == kat_filtre]

            for m in filtreli:
                d_renk = _MALZEME_DURUM_RENK.get(m.get("durum",""), "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {d_renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{m.get('ad','')} x{m.get('adet',1)}</span>
                    <span style="color:#94a3b8;font-size:0.65rem;">{m.get('kategori','')} | {m.get('konum','')}</span>
                    <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                        font-size:0.62rem;font-weight:700;">{m.get('durum','')}</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Malzeme Odunc Ver / Iade Al")
        with st.form("odunc_form"):
            c1, c2 = st.columns(2)
            with c1:
                o_malzeme = st.selectbox("Malzeme",
                    [m.get("ad","") for m in envanter if m.get("durum") == "Mevcut"] if envanter else ["--"],
                    key="od_mal")
                o_alan = st.text_input("Odunc Alan", key="od_alan")
            with c2:
                o_islem = st.selectbox("Islem", ["Odunc Ver", "Iade Al"], key="od_islem")
                o_tarih = st.date_input("Tarih", key="od_tarih")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if o_malzeme and o_alan:
                    odunc_log.append({
                        "malzeme": o_malzeme, "alan": o_alan,
                        "islem": o_islem, "tarih": o_tarih.isoformat(),
                    })
                    _sj("lab_odunc.json", odunc_log)
                    # Envanter guncelle
                    for m in envanter:
                        if m.get("ad") == o_malzeme:
                            m["durum"] = "Oduncte" if o_islem == "Odunc Ver" else "Mevcut"
                    _sj("lab_envanter.json", envanter)
                    st.success(f"{'📤' if o_islem == 'Odunc Ver' else '📥'} {o_malzeme} — {o_islem}")
                    st.rerun()

    with sub[2]:
        styled_section("Is Guvenligi Checklist")
        ogr = st.text_input("Ogrenci Adi", key="gv_ogr")
        if ogr:
            with st.form("guvenlik_form"):
                tamamlanan = []
                for i, madde in enumerate(_GUVENLIK_CHECKLIST):
                    if st.checkbox(madde, key=f"gv_{i}"):
                        tamamlanan.append(madde)

                if st.form_submit_button("Kontrol Tamamla", use_container_width=True):
                    guvenlik_log.append({
                        "ogrenci": ogr, "tamamlanan": tamamlanan,
                        "toplam": len(_GUVENLIK_CHECKLIST),
                        "puan": round(len(tamamlanan) / len(_GUVENLIK_CHECKLIST) * 100),
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("guvenlik_checklist.json", guvenlik_log)
                    puan = round(len(tamamlanan) / len(_GUVENLIK_CHECKLIST) * 100)
                    renk = "#10b981" if puan == 100 else "#f59e0b" if puan >= 75 else "#ef4444"
                    st.markdown(f"Guvenlik: **%{puan}** {'✅ Tamam!' if puan == 100 else '⚠️ Eksik var!'}")

    with sub[3]:
        styled_section("Lab Rezervasyon")
        with st.form("rez_form"):
            c1, c2 = st.columns(2)
            with c1:
                r_ogr = st.text_input("Ogrenci/Grup", key="rz_ogr")
                r_lab = st.selectbox("Lab", ["Makerspace", "Robotik Lab", "3D Baski", "Elektronik Lab", "Bilisim Lab"], key="rz_lab")
            with c2:
                r_tarih = st.date_input("Tarih", key="rz_tarih")
                r_saat = st.selectbox("Saat", ["09:00-10:00","10:00-11:00","11:00-12:00","13:00-14:00","14:00-15:00","15:00-16:00"], key="rz_saat")

            if st.form_submit_button("Rezerve Et", use_container_width=True):
                if r_ogr:
                    rezervasyonlar.append({
                        "ogrenci": r_ogr, "lab": r_lab,
                        "tarih": r_tarih.isoformat(), "saat": r_saat,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("lab_rezervasyon.json", rezervasyonlar)
                    st.success(f"📅 {r_lab} — {r_tarih} {r_saat} rezerve edildi!")
                    st.rerun()

        if rezervasyonlar:
            styled_section("Aktif Rezervasyonlar")
            for r in sorted(rezervasyonlar, key=lambda x: x.get("tarih",""))[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-size:0.78rem;flex:1;">🔧 {r.get('lab','')} — {r.get('ogrenci','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{r.get('tarih','')[:10]} {r.get('saat','')}</span>
                </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Stok Analizi & Uyari")
        if envanter:
            kat_say = Counter(m.get("kategori","") for m in envanter)
            for kat, sayi in kat_say.most_common():
                mevcut_s = sum(1 for m in envanter if m.get("kategori") == kat and m.get("durum") == "Mevcut")
                renk = "#10b981" if mevcut_s >= 5 else "#f59e0b" if mevcut_s >= 2 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:130px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{kat}</span>
                    <span style="color:{renk};font-weight:700;">{mevcut_s}/{sayi} mevcut</span>
                </div>""", unsafe_allow_html=True)

            az_kalan = [m for m in envanter if m.get("durum") == "Mevcut" and m.get("adet",1) <= 1]
            if az_kalan:
                st.warning(f"⚠️ {len(az_kalan)} malzeme kritik stokta!")


# ════════════════════════════════════════════════════════════
# 2. TÜBİTAK & BİLİM FUARI PROJE YÖNETİM
# ════════════════════════════════════════════════════════════

def render_tubitak_merkez(store):
    """TÜBİTAK & Bilim Fuarı — proje pipeline, jüri, mentor, bütçe."""
    styled_section("TUBITAK & Bilim Fuari Proje Yonetim Merkezi", "#059669")
    styled_info_banner(
        "TUBITAK 4006, bilim fuari, hackathon, robotik yarisma projelerinin "
        "bastan sona yonetimi. Fikir → Prototip → Yarisma pipeline.",
        banner_type="info", icon="🏆")

    projeler = _lj("tubitak_projeler.json")
    degerlendirmeler = _lj("tubitak_degerlendirme.json")

    aktif = sum(1 for p in projeler if p.get("asama") not in ("Odul",""))
    odullu = sum(1 for d in degerlendirmeler if d.get("odul"))

    styled_stat_row([
        ("Toplam Proje", str(len(projeler)), "#059669", "🔬"),
        ("Aktif", str(aktif), "#3b82f6", "🔵"),
        ("Odullu", str(odullu), "#c9a84c", "🏆"),
    ])

    sub = st.tabs(["➕ Yeni Proje", "📋 Pipeline", "🏆 Juri & Odul", "👨‍🏫 Mentor", "💰 Butce"])

    with sub[0]:
        styled_section("Yeni STEAM Proje Olustur")
        with st.form("proje_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_ad = st.text_input("Proje Adi", key="tp_ad")
                p_ekip = st.text_input("Ekip Uyeleri (virgul ile)", key="tp_ekip")
                p_yarisma = st.selectbox("Hedef Yarisma", _YARISMA_TURLERI, key="tp_yar")
            with c2:
                p_alan = st.multiselect("STEAM Alanlari", list(_STEAM_ALANLARI.keys()), key="tp_alan")
                p_danisman = st.text_input("Danisman Ogretmen", key="tp_dan")
                p_butce = st.number_input("Tahmini Butce (TL)", 0, 50000, 500, key="tp_butce")
            p_ozet = st.text_area("Proje Ozeti", height=60, key="tp_ozet")

            if st.form_submit_button("Proje Olustur", use_container_width=True, type="primary"):
                if p_ad:
                    ekip = [e.strip() for e in p_ekip.split(",") if e.strip()]
                    projeler.append({
                        "id": f"tp_{uuid.uuid4().hex[:8]}",
                        "ad": p_ad, "ekip": ekip, "yarisma": p_yarisma,
                        "alanlar": p_alan, "danisman": p_danisman,
                        "butce": p_butce, "ozet": p_ozet,
                        "asama": "Fikir", "created_at": datetime.now().isoformat(),
                    })
                    _sj("tubitak_projeler.json", projeler)
                    st.success(f"🔬 '{p_ad}' projesi olusturuldu!")
                    st.rerun()

    with sub[1]:
        styled_section("Proje Pipeline")
        if not projeler:
            st.info("Proje yok.")
        else:
            # Asama dagilimi
            asama_say = Counter(p.get("asama","") for p in projeler)
            for asama in _PROJE_PIPELINE:
                sayi = asama_say.get(asama, 0)
                renk = _PROJE_RENK.get(asama, "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:80px;color:{renk};font-weight:700;font-size:0.82rem;">{asama}</span>
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            styled_section("Proje Listesi")
            for p in projeler:
                renk = _PROJE_RENK.get(p.get("asama",""), "#94a3b8")
                steam = " ".join(_STEAM_ALANLARI.get(a,{}).get("ikon","") for a in p.get("alanlar",[]))
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 12px 12px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">🔬 {p.get('ad','')}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{p.get('asama','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        {steam} | {p.get('yarisma','')} | Ekip: {', '.join(p.get('ekip',[])[:3])}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Asama Guncelle: {p.get('id','')}", expanded=False):
                    yeni = st.selectbox("Asama", _PROJE_PIPELINE,
                        index=_PROJE_PIPELINE.index(p.get("asama","Fikir")) if p.get("asama") in _PROJE_PIPELINE else 0,
                        key=f"tp_a_{p['id']}")
                    if st.button("Guncelle", key=f"tp_g_{p['id']}"):
                        p["asama"] = yeni
                        _sj("tubitak_projeler.json", projeler)
                        st.rerun()

    with sub[2]:
        styled_section("Juri Degerlendirme & Odul")
        if projeler:
            sunum = [p for p in projeler if p.get("asama") in ("Sunum","Yarisma","Odul")]
            if sunum:
                with st.form("juri_form"):
                    j_proje = st.selectbox("Proje", [p.get("ad","") for p in sunum], key="jr_proje")
                    c1, c2, c3 = st.columns(3)
                    with c1: j_bilimsellik = st.slider("Bilimsellik", 1, 10, 7, key="jr_bil")
                    with c2: j_yaraticilik = st.slider("Yaraticilik", 1, 10, 7, key="jr_yar")
                    with c3: j_sunum = st.slider("Sunum", 1, 10, 7, key="jr_sun")
                    j_odul = st.checkbox("Odul Verilsin Mi?", key="jr_odul")

                    if st.form_submit_button("Degerlendir", use_container_width=True):
                        toplam = round((j_bilimsellik + j_yaraticilik + j_sunum) / 3, 1)
                        degerlendirmeler.append({
                            "proje": j_proje, "bilimsellik": j_bilimsellik,
                            "yaraticilik": j_yaraticilik, "sunum": j_sunum,
                            "toplam": toplam, "odul": j_odul,
                            "tarih": datetime.now().isoformat(),
                        })
                        _sj("tubitak_degerlendirme.json", degerlendirmeler)
                        st.success(f"{'🏆 ODUL!' if j_odul else ''} {j_proje}: {toplam}/10")
            else:
                st.info("Sunum asamasinda proje yok.")

    with sub[3]:
        styled_section("Mentor Eslestirme")
        st.caption("Her projeye bir mentor (ogretmen/uzman) atanir.")
        if projeler:
            for p in projeler:
                st.markdown(f"  - 🔬 **{p.get('ad','')}** — Danisman: {p.get('danisman','Atanmadi')}")

    with sub[4]:
        styled_section("Proje Butce Takibi")
        if projeler:
            toplam_butce = sum(p.get("butce", 0) for p in projeler)
            st.markdown(f"**Toplam planlanan butce:** {toplam_butce:,} TL")
            for p in projeler:
                st.markdown(f"  - {p.get('ad','')}: {p.get('butce',0):,} TL")


# ════════════════════════════════════════════════════════════
# 3. STEAM PORTFOLYO & DİSİPLİNLER ARASI KAZANIM HARİTASI
# ════════════════════════════════════════════════════════════

def render_steam_portfolyo(store):
    """STEAM Portfolyo — proje, lab, yarışma, kazanım tek kartta."""
    styled_section("STEAM Portfolyo & Disiplinler Arasi Kazanim Haritasi", "#8b5cf6")
    styled_info_banner(
        "Her ogrencinin STEAM projeleri, lab calismalari, yarisma sonuclari, "
        "yetkinlikleri tek portfolyoda. MEB kazanim eslestirme, STEAM CV.",
        banner_type="info", icon="📂")

    projeler = _lj("tubitak_projeler.json")
    envanter = _lj("lab_envanter.json")

    sub = st.tabs(["👤 Portfolyo Kart", "🗺️ Kazanim Haritasi", "📊 STEAM Profil", "📄 STEAM CV"])

    with sub[0]:
        styled_section("Ogrenci STEAM Portfolyosu")
        ogr = _ogr_sec("sp_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            ogr_proje = [p for p in projeler if ogr_ad in " ".join(p.get("ekip",[]))]
            ogr_alan = set()
            for p in ogr_proje:
                ogr_alan.update(p.get("alanlar",[]))

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,#8b5cf630);border:2px solid #8b5cf6;
                border-radius:20px;padding:24px;text-align:center;margin:10px 0;">
                <div style="font-size:2rem;">📂</div>
                <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:4px;">{ogr_ad}</div>
                <div style="color:#c4b5fd;font-size:0.8rem;">STEAM Portfolyo</div>
                <div style="display:flex;justify-content:center;gap:16px;margin-top:12px;">
                    <div><div style="color:#8b5cf6;font-weight:900;font-size:1.5rem;">{len(ogr_proje)}</div><div style="color:#64748b;font-size:0.62rem;">Proje</div></div>
                    <div><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{len(ogr_alan)}</div><div style="color:#64748b;font-size:0.62rem;">STEAM Alan</div></div>
                </div>
                <div style="display:flex;justify-content:center;gap:6px;margin-top:10px;">
                    {"".join(f'<span style="background:{_STEAM_ALANLARI.get(a,{}).get("renk","#94a3b8")}20;color:{_STEAM_ALANLARI.get(a,{}).get("renk","#94a3b8")};padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700;">{_STEAM_ALANLARI.get(a,{}).get("ikon","")} {a}</span>' for a in ogr_alan)}
                </div>
            </div>""", unsafe_allow_html=True)

            if ogr_proje:
                styled_section("Projeler")
                for p in ogr_proje:
                    renk = _PROJE_RENK.get(p.get("asama",""), "#94a3b8")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                        background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🔬 {p.get('ad','')}</span>
                        <span style="color:{renk};font-size:0.68rem;font-weight:700;">{p.get('asama','')}</span>
                    </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Disiplinler Arasi Kazanim Haritasi")
        for proje_turu, dersler in _KAZANIM_MAP.items():
            with st.expander(f"🔬 {proje_turu}"):
                for ders, kazanimlar in dersler.items():
                    st.markdown(f"**{ders}:**")
                    for k in kazanimlar:
                        st.markdown(f"  - 🎯 {k}")

    with sub[2]:
        styled_section("STEAM Alan Profili")
        if projeler:
            alan_say = Counter()
            for p in projeler:
                for a in p.get("alanlar", []):
                    alan_say[a] += 1

            toplam = max(sum(alan_say.values()), 1)
            for alan, info in _STEAM_ALANLARI.items():
                sayi = alan_say.get(alan, 0)
                pct = round(sayi / toplam * 100) if sayi else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="font-size:1.2rem;">{info['ikon']}</span>
                    <span style="min-width:90px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{alan}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{info['renk']};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi} proje</span></div></div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("STEAM CV (Universite Basvurusu)")
        ogr2 = _ogr_sec("sp_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            ogr_proje2 = [p for p in projeler if ogr_ad2 in " ".join(p.get("ekip",[]))]

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #8b5cf6;border-radius:16px;padding:20px 24px;">
                <div style="text-align:center;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">📄 STEAM Aktivite CV</div>
                    <div style="color:#c4b5fd;font-size:0.8rem;">{ogr_ad2}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if ogr_proje2:
                styled_section("Projeler")
                for p in ogr_proje2:
                    alanlar = " ".join(_STEAM_ALANLARI.get(a,{}).get("ikon","") for a in p.get("alanlar",[]))
                    st.markdown(f"  - 🔬 **{p.get('ad','')}** — {p.get('yarisma','')} | {alanlar} | {p.get('asama','')}")

            st.caption("Bu bilgiler universite basvurusu, burs ve staj icin kullanilabilir.")
