"""
STEAM Merkezi — Final Özellikler
==================================
1. STEAM Sertifikasyon & Dijital Rozet Sistemi
2. STEAM Araştırma Günlüğü & Bilimsel Süreç Takipçisi
3. STEAM Etki Ölçümü & Sürdürülebilirlik Endeksi
"""
from __future__ import annotations
import json, os, uuid, random, hashlib
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

_SERTIFIKALAR = [
    {"ad": "Arduino Temel", "ikon": "⚡", "alan": "Technology", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "LED+sensor projesi tamamla", "proje_sayi": 3},
    {"ad": "Arduino Ileri", "ikon": "⚡", "alan": "Technology", "seviye": "Gumus", "renk": "#c0c0c0",
     "kosul": "IoT projesi + motor kontrolu", "proje_sayi": 5},
    {"ad": "3D Tasarim Temel", "ikon": "🖨️", "alan": "Engineering", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "Tinkercad 5 tasarim", "proje_sayi": 5},
    {"ad": "3D Tasarim Ileri", "ikon": "🖨️", "alan": "Engineering", "seviye": "Gumus", "renk": "#c0c0c0",
     "kosul": "Fusion 360 + fonksiyonel parca", "proje_sayi": 8},
    {"ad": "Kodlama Temel", "ikon": "💻", "alan": "Technology", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "Scratch/Python 5 proje", "proje_sayi": 5},
    {"ad": "Kodlama Ileri", "ikon": "💻", "alan": "Technology", "seviye": "Gumus", "renk": "#c0c0c0",
     "kosul": "Python + API/veri analizi", "proje_sayi": 10},
    {"ad": "Robotik Temel", "ikon": "🤖", "alan": "Engineering", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "Basit robot montaj + hareket", "proje_sayi": 3},
    {"ad": "Bilim Arastirmaci", "ikon": "🔬", "alan": "Science", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "3 bilimsel deney raporu", "proje_sayi": 3},
    {"ad": "Dijital Sanatci", "ikon": "🎨", "alan": "Art", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "5 dijital tasarim/sanat eseri", "proje_sayi": 5},
    {"ad": "Matematik Modelleci", "ikon": "🧮", "alan": "Mathematics", "seviye": "Bronz", "renk": "#cd7f32",
     "kosul": "3 matematik modelleme projesi", "proje_sayi": 3},
    {"ad": "STEAM Master", "ikon": "👑", "alan": "Hepsi", "seviye": "Altin", "renk": "#c9a84c",
     "kosul": "5 farkli alanda sertifika", "proje_sayi": 20},
    {"ad": "Platin Maker", "ikon": "💎", "alan": "Hepsi", "seviye": "Platin", "renk": "#8b5cf6",
     "kosul": "30+ proje + 3 yarisma odulu", "proje_sayi": 30},
]

_SEVIYE_RENK = {"Bronz": "#cd7f32", "Gumus": "#c0c0c0", "Altin": "#c9a84c", "Platin": "#8b5cf6"}

_BILIMSEL_ADIMLAR = [
    ("1. Gozlem", "Dogada veya cevrende ne fark ettin? Neyi merak ediyorsun?"),
    ("2. Soru", "Arastirma sorun ne? 'Neden...?', 'Nasil...?', 'Ne olur...?'"),
    ("3. Hipotez", "Tahminin ne? 'Eger ... ise, ... olur' formatinda yaz."),
    ("4. Deney", "Hipotezini test etmek icin ne yaptin? Malzemeler, adimlar."),
    ("5. Analiz", "Verilerin ne gosteriyor? Grafik, tablo, karsilastirma."),
    ("6. Sonuc", "Hipotezin dogrulandi mi? Ne ogrendin? Yeni sorular?"),
]

_SDG_HEDEFLER = {
    "SDG 4": {"ad": "Nitelikli Egitim", "ikon": "📚", "renk": "#c5192d"},
    "SDG 6": {"ad": "Temiz Su ve Sanitasyon", "ikon": "💧", "renk": "#26bde2"},
    "SDG 7": {"ad": "Erisilebilir Temiz Enerji", "ikon": "⚡", "renk": "#fcc30b"},
    "SDG 9": {"ad": "Sanayi, Inovasyon, Altyapi", "ikon": "🏭", "renk": "#f36d25"},
    "SDG 11": {"ad": "Surdurulebilir Sehirler", "ikon": "🏙️", "renk": "#fd9d24"},
    "SDG 12": {"ad": "Sorumlu Uretim ve Tuketim", "ikon": "♻️", "renk": "#bf8b2e"},
    "SDG 13": {"ad": "Iklim Eylemi", "ikon": "🌍", "renk": "#3f7e44"},
    "SDG 15": {"ad": "Karasal Yasam", "ikon": "🌳", "renk": "#56c02b"},
}


# ════════════════════════════════════════════════════════════
# 1. STEAM SERTİFİKASYON & DİJİTAL ROZET
# ════════════════════════════════════════════════════════════

def render_steam_sertifika(store):
    """STEAM Sertifikasyon — mikro sertifika, seviye ağacı, QR doğrulama."""
    styled_section("STEAM Sertifikasyon & Dijital Rozet Sistemi", "#c9a84c")
    styled_info_banner(
        "Her STEAM becerisi icin dijital mikro-sertifika. "
        "Bronz→Gumus→Altin→Platin seviye agaci, QR dogrulama.",
        banner_type="info", icon="🎓")

    verilen_sertifikalar = _lj("steam_sertifikalar.json")

    sub = st.tabs(["🎓 Sertifika Ver", "📋 Sertifika Katalogu", "👤 Ogrenci Sertifika", "🌳 Seviye Agaci"])

    with sub[0]:
        styled_section("Sertifika Ver")
        with st.form("sert_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("ss_ogr")
                s_sert = st.selectbox("Sertifika",
                    [f"{s['ikon']} {s['ad']} ({s['seviye']})" for s in _SERTIFIKALAR], key="ss_sert")
            with c2:
                s_tarih = st.date_input("Verilis Tarihi", key="ss_tarih")
                s_veren = st.text_input("Veren Ogretmen", key="ss_veren")

            if st.form_submit_button("Sertifika Ver", use_container_width=True, type="primary"):
                if ogr:
                    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
                    idx = [f"{s['ikon']} {s['ad']} ({s['seviye']})" for s in _SERTIFIKALAR].index(s_sert)
                    sert = _SERTIFIKALAR[idx]
                    dogrulama = hashlib.md5(f"{ogr_ad}{sert['ad']}{s_tarih}".encode()).hexdigest()[:10].upper()

                    verilen_sertifikalar.append({
                        "id": f"ss_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "sertifika": sert["ad"],
                        "seviye": sert["seviye"], "alan": sert["alan"],
                        "veren": s_veren, "dogrulama_kodu": dogrulama,
                        "tarih": s_tarih.isoformat(),
                    })
                    _sj("steam_sertifikalar.json", verilen_sertifikalar)
                    st.success(f"🎓 {sert['ikon']} {sert['ad']} ({sert['seviye']}) — {ogr_ad}")
                    st.markdown(f"Dogrulama Kodu: **{dogrulama}**")
                    st.rerun()

    with sub[1]:
        styled_section("STEAM Sertifika Katalogu")
        for s in _SERTIFIKALAR:
            renk = _SEVIYE_RENK.get(s["seviye"], "#94a3b8")
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                border-radius:0 14px 14px 0;padding:10px 14px;margin:5px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{s['ikon']} {s['ad']}</span>
                    <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:8px;
                        font-size:0.7rem;font-weight:800;">{s['seviye']}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                    Alan: {s['alan']} | Kosul: {s['kosul']} | Min {s['proje_sayi']} proje</div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Ogrenci Sertifika Koleksiyonu")
        if not verilen_sertifikalar:
            st.info("Verilen sertifika yok.")
        else:
            ogr_grp = defaultdict(list)
            for vs in verilen_sertifikalar:
                ogr_grp[vs.get("ogrenci","")].append(vs)

            for ogr_ad, sertler in sorted(ogr_grp.items()):
                st.markdown(f"**🎓 {ogr_ad}** — {len(sertler)} sertifika")
                for vs in sertler:
                    renk = _SEVIYE_RENK.get(vs.get("seviye",""), "#94a3b8")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;padding:4px 12px 4px 24px;margin:2px 0;
                        border-left:2px solid {renk};background:{renk}08;border-radius:0 6px 6px 0;">
                        <span style="color:{renk};font-weight:700;font-size:0.75rem;flex:1;">{vs.get('sertifika','')}</span>
                        <span style="color:#64748b;font-size:0.6rem;">{vs.get('seviye','')}</span>
                        <span style="font-family:monospace;color:#94a3b8;font-size:0.58rem;">{vs.get('dogrulama_kodu','')}</span>
                    </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("STEAM Seviye Agaci")
        for seviye, renk in _SEVIYE_RENK.items():
            sev_sertler = [s for s in _SERTIFIKALAR if s["seviye"] == seviye]
            st.markdown(f"""
            <div style="background:{renk}10;border:2px solid {renk};border-radius:14px;
                padding:10px 16px;margin:6px 0;">
                <span style="color:{renk};font-weight:900;font-size:0.9rem;">{seviye} ({len(sev_sertler)} sertifika)</span>
            </div>""", unsafe_allow_html=True)
            for s in sev_sertler:
                st.markdown(f"  - {s['ikon']} {s['ad']} ({s['alan']})")


# ════════════════════════════════════════════════════════════
# 2. STEAM ARAŞTIRMA GÜNLÜĞÜ & BİLİMSEL SÜREÇ
# ════════════════════════════════════════════════════════════

def render_arastirma_gunlugu(store):
    """STEAM Araştırma Günlüğü — bilimsel yöntem 6 adım, deney verisi, TÜBİTAK format."""
    styled_section("STEAM Arastirma Gunlugu & Bilimsel Surec Takipcisi", "#3b82f6")
    styled_info_banner(
        "Bilimsel yontemin 6 adimini takip eden dijital arastirma defteri. "
        "Deney verisi kayit, grafik, TUBITAK rapor formatina donusturme.",
        banner_type="info", icon="🔬")

    gunlukler = _lj("arastirma_gunlugu.json")

    sub = st.tabs(["📝 Yeni Arastirma", "📋 Gunluk Arsivi", "📊 Bilimsel Adimlar", "📄 TUBITAK Format"])

    with sub[0]:
        styled_section("Yeni Arastirma Gunlugu")
        with st.form("ag_form"):
            ag_ad = st.text_input("Arastirma Basligi", key="ag_ad")
            ag_ogr = st.text_input("Arastirmaci (Ogrenci/Takim)", key="ag_ogr")

            st.markdown("**Bilimsel Surec Adimlari:**")
            adimlar = {}
            for adim_ad, aciklama in _BILIMSEL_ADIMLAR:
                adimlar[adim_ad] = st.text_area(f"{adim_ad}", height=50, key=f"ag_{adim_ad[:5]}",
                    placeholder=aciklama)

            ag_sonuc = st.selectbox("Hipotez Sonucu",
                ["Dogrulandi", "Kismen Dogrulandi", "Yanlilandı", "Belirsiz"], key="ag_sonuc")

            if st.form_submit_button("Arastirmayi Kaydet", use_container_width=True, type="primary"):
                if ag_ad:
                    gunlukler.append({
                        "id": f"ag_{uuid.uuid4().hex[:8]}",
                        "baslik": ag_ad, "arastirmaci": ag_ogr,
                        "adimlar": adimlar, "hipotez_sonuc": ag_sonuc,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("arastirma_gunlugu.json", gunlukler)
                    st.success(f"🔬 '{ag_ad}' arastirma gunlugu kaydedildi!")
                    st.rerun()

    with sub[1]:
        styled_section("Arastirma Arsivi")
        if not gunlukler:
            st.info("Arastirma kaydi yok.")
        else:
            for g in sorted(gunlukler, key=lambda x: x.get("tarih",""), reverse=True):
                sonuc_renk = {"Dogrulandi":"#10b981","Kismen Dogrulandi":"#f59e0b","Yanlilandı":"#ef4444","Belirsiz":"#94a3b8"}
                renk = sonuc_renk.get(g.get("hipotez_sonuc",""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 14px 14px 0;
                    padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🔬 {g.get('baslik','')}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{g.get('hipotez_sonuc','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {g.get('arastirmaci','')} | {g.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Detay: {g.get('baslik','')}", expanded=False):
                    for adim_ad, icerik in g.get("adimlar", {}).items():
                        if icerik:
                            st.markdown(f"**{adim_ad}:** {icerik[:100]}")

    with sub[2]:
        styled_section("Bilimsel Yontem Adimlari Rehberi")
        for adim_ad, aciklama in _BILIMSEL_ADIMLAR:
            st.markdown(f"""
            <div style="background:#3b82f608;border:1px solid #3b82f630;border-left:4px solid #3b82f6;
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <span style="color:#93c5fd;font-weight:800;font-size:0.82rem;">{adim_ad}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("TUBITAK Rapor Formati")
        if gunlukler:
            sec = st.selectbox("Arastirma Sec",
                [g.get("baslik","") for g in gunlukler], key="ag_tubitak")
            idx = [g.get("baslik","") for g in gunlukler].index(sec) if sec else 0
            g = gunlukler[idx]

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #3b82f6;border-radius:16px;padding:20px 24px;">
                <div style="text-align:center;margin-bottom:14px;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">TUBITAK Proje Raporu</div>
                    <div style="color:#93c5fd;font-size:0.85rem;margin-top:4px;">{g.get('baslik','')}</div>
                    <div style="color:#94a3b8;font-size:0.72rem;">{g.get('arastirmaci','')} | {g.get('tarih','')[:10]}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            for adim_ad, icerik in g.get("adimlar", {}).items():
                if icerik:
                    st.markdown(f"**{adim_ad}**")
                    st.markdown(f"> {icerik}")
            st.markdown(f"**Sonuc:** {g.get('hipotez_sonuc','')}")
            st.caption("Bu format TUBITAK 4006/4007 rapor sablonuyla uyumludur.")


# ════════════════════════════════════════════════════════════
# 3. STEAM ETKİ ÖLÇÜMÜ & SÜRDÜRÜLEBİLİRLİK ENDEKSİ
# ════════════════════════════════════════════════════════════

def render_etki_olcumu(store):
    """STEAM Etki Ölçümü — toplumsal/çevresel etki, SDG eşleştirme, karbon."""
    styled_section("STEAM Etki Olcumu & Surdurulebilirlik Endeksi", "#10b981")
    styled_info_banner(
        "STEAM projelerinin toplumsal/cevresel etkisini olcun. "
        "BM Surdurulebilir Kalkinma Hedefleri eslestirme, etki raporu.",
        banner_type="info", icon="🌍")

    etki_kayitlari = _lj("steam_etki.json")

    sub = st.tabs(["📊 Etki Kaydet", "🌍 SDG Eslestir", "📈 Etki Raporu", "🌱 Surdurulebilirlik"])

    with sub[0]:
        styled_section("Proje Etki Kaydi")
        with st.form("etki_form"):
            c1, c2 = st.columns(2)
            with c1:
                e_proje = st.text_input("Proje Adi", key="et_proje")
                e_tur = st.selectbox("Etki Turu",
                    ["Cevresel", "Toplumsal", "Ekonomik", "Egitimsel", "Teknolojik"], key="et_tur")
            with c2:
                e_metrik = st.text_input("Olculebilir Metrik", placeholder="120kg atik toplandi, %15 su tasarrufu...", key="et_met")
                e_faydalanan = st.number_input("Faydalanan Kisi", 0, 10000, 50, key="et_fay")
            e_aciklama = st.text_area("Etki Aciklamasi", height=50, key="et_acik")
            e_sdg = st.multiselect("Ilgili SDG Hedefleri", list(_SDG_HEDEFLER.keys()), key="et_sdg")

            if st.form_submit_button("Etki Kaydet", use_container_width=True, type="primary"):
                if e_proje:
                    etki_kayitlari.append({
                        "id": f"et_{uuid.uuid4().hex[:8]}",
                        "proje": e_proje, "tur": e_tur, "metrik": e_metrik,
                        "faydalanan": e_faydalanan, "aciklama": e_aciklama,
                        "sdg": e_sdg, "tarih": date.today().isoformat(),
                    })
                    _sj("steam_etki.json", etki_kayitlari)
                    st.success(f"🌍 '{e_proje}' etki kaydi olusturuldu!")
                    st.rerun()

    with sub[1]:
        styled_section("BM Surdurulebilir Kalkinma Hedefleri (SDG)")
        if etki_kayitlari:
            sdg_say = Counter()
            for e in etki_kayitlari:
                for s in e.get("sdg", []):
                    sdg_say[s] += 1

            for sdg, info in _SDG_HEDEFLER.items():
                sayi = sdg_say.get(sdg, 0)
                aktif = sayi > 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                    background:{'#0f172a' if aktif else '#0f172a80'};border-left:5px solid {info['renk']};
                    border-radius:0 10px 10px 0;{'border:1px solid ' + info['renk'] + '30;' if aktif else ''}
                    opacity:{'1' if aktif else '0.5'};">
                    <span style="font-size:1.2rem;">{info['ikon']}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{sdg}: {info['ad']}</span>
                    <span style="color:{info['renk']};font-weight:800;font-size:0.78rem;">
                        {'✅ ' + str(sayi) + ' proje' if aktif else '—'}</span>
                </div>""", unsafe_allow_html=True)

            aktif_sdg = sum(1 for s in sdg_say if sdg_say[s] > 0)
            st.markdown(f"**Okulumuz {aktif_sdg}/{len(_SDG_HEDEFLER)} SDG hedefine katki sagliyor.**")
        else:
            for sdg, info in _SDG_HEDEFLER.items():
                st.markdown(f"  {info['ikon']} **{sdg}:** {info['ad']}")

    with sub[2]:
        styled_section("STEAM Toplumsal Etki Raporu")
        if not etki_kayitlari:
            st.info("Etki kaydi yok.")
        else:
            toplam_faydalanan = sum(e.get("faydalanan", 0) for e in etki_kayitlari)
            tur_say = Counter(e.get("tur","") for e in etki_kayitlari)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#10b98115);border:2px solid #10b981;
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#10b981;font-weight:900;font-size:1.1rem;">STEAM Toplumsal Etki</div>
                <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                    <div><div style="color:#10b981;font-weight:900;font-size:2rem;">{len(etki_kayitlari)}</div><div style="color:#64748b;font-size:0.62rem;">Proje</div></div>
                    <div><div style="color:#3b82f6;font-weight:900;font-size:2rem;">{toplam_faydalanan}</div><div style="color:#64748b;font-size:0.62rem;">Faydalanan</div></div>
                    <div><div style="color:#8b5cf6;font-weight:900;font-size:2rem;">{len(tur_say)}</div><div style="color:#64748b;font-size:0.62rem;">Etki Alani</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

            for e in sorted(etki_kayitlari, key=lambda x: x.get("faydalanan",0), reverse=True):
                sdg_txt = " ".join(_SDG_HEDEFLER.get(s,{}).get("ikon","") for s in e.get("sdg",[]))
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #10b981;border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">🌍 {e.get('proje','')}</span>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {e.get('tur','')} | {e.get('metrik','')} | {e.get('faydalanan',0)} kisi | {sdg_txt}</div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Surdurulebilirlik Endeksi")
        if etki_kayitlari:
            sdg_aktif = len(set(s for e in etki_kayitlari for s in e.get("sdg",[])))
            proje_sayi = len(etki_kayitlari)
            faydalanan = sum(e.get("faydalanan",0) for e in etki_kayitlari)

            # Surdurulebilirlik skoru
            skor = min(100, sdg_aktif * 10 + proje_sayi * 5 + faydalanan // 10)
            renk = "#10b981" if skor >= 70 else "#f59e0b" if skor >= 40 else "#ef4444"
            harf = "A" if skor >= 85 else "B" if skor >= 65 else "C" if skor >= 45 else "D"

            st.markdown(f"""
            <div style="background:{renk}15;border:3px solid {renk};border-radius:22px;
                padding:28px;text-align:center;">
                <div style="color:#94a3b8;font-size:0.85rem;">Surdurulebilirlik Endeksi</div>
                <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
                    <span style="color:{renk};font-weight:900;font-size:3.5rem;">{harf}</span>
                    <span style="color:{renk};font-weight:700;font-size:1.5rem;">{skor}/100</span>
                </div>
                <div style="color:#64748b;font-size:0.72rem;margin-top:6px;">
                    {sdg_aktif} SDG | {proje_sayi} proje | {faydalanan} faydalanan</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Surdurulebilirlik endeksi icin etki kaydi gerekli.")
