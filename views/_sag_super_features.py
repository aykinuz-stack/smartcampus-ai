"""
Okul Sağlığı — Süper Özellikler
=================================
1. Acil Durum Yönetim Merkezi & Alerji/Kronik Alarm
2. Beslenme & Hijyen Takip Sistemi
3. Spor Muafiyeti & Fiziksel Aktivite Uygunluk
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta

import streamlit as st

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _sag_dir() -> str:
    d = os.path.join(get_tenant_dir(), "saglik")
    os.makedirs(d, exist_ok=True)
    return d

def _lj(n: str) -> list:
    p = os.path.join(_sag_dir(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: return []

def _sj(n: str, d: list) -> None:
    with open(os.path.join(_sag_dir(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def _ogr_sec(key: str) -> dict | None:
    students = load_shared_students()
    if not students:
        st.warning("Ogrenci verisi yok.")
        return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None


# ════════════════════════════════════════════════════════════
# SABİTLER
# ════════════════════════════════════════════════════════════

_ALERJI_TURLERI = {
    "Gida": {"ikon": "🍎", "renk": "#ef4444", "ornekler": ["Findik", "Yer fistigi", "Sut", "Yumurta", "Gluten", "Balik", "Kabuklu deniz urunu", "Soya", "Susam"]},
    "Ilac": {"ikon": "💊", "renk": "#8b5cf6", "ornekler": ["Penisilin", "Aspirin", "Ibuprofen", "Sulfonamid"]},
    "Bocek": {"ikon": "🐝", "renk": "#f59e0b", "ornekler": ["Ari sokması", "Sivrisinek", "Kene"]},
    "Cevresel": {"ikon": "🌿", "renk": "#10b981", "ornekler": ["Toz", "Polen", "Kuf", "Hayvan tüyü", "Lateks"]},
}

_KRONIK_HASTALIKLAR = {
    "Diyabet (Tip 1)": {"ikon": "🩸", "renk": "#ef4444", "acil_protokol": [
        "Hipoglisemi belirtilerini kontrol et (titreme, terleme, bas donmesi)",
        "Bilinci aciksa: seker/meyve suyu ver",
        "Bilinci kapaniyorsa: 112'yi ara, yan yatir",
        "Kan sekeri olcumu yap (varsa glukometre)",
        "Veliyi bilgilendir",
    ]},
    "Epilepsi": {"ikon": "⚡", "renk": "#8b5cf6", "acil_protokol": [
        "Panik yapma — nobet genellikle 1-3 dk surer",
        "Ogrenciyi yere yatir, basini koru",
        "Agzina hicbir sey koyma",
        "Etrafindaki sert cisimleri uzaklastir",
        "Nobet 5 dk'yi gecerse 112'yi ara",
        "Nobet bitince yan yatir, sakinlestir",
    ]},
    "Astim": {"ikon": "🫁", "renk": "#3b82f6", "acil_protokol": [
        "Ogrenciyi oturt, one egdir",
        "Nefes almasini kolaylastir (yaka dugmesi, kemer geysetme)",
        "Kendi inhaler'ini kullanmasina yardim et",
        "Derin ve yavas nefes almasini soyle",
        "Duzelmezse 112'yi ara",
    ]},
    "Kalp Hastaligi": {"ikon": "❤️", "renk": "#dc2626", "acil_protokol": [
        "Fiziksel aktiviteyi durdur",
        "Oturtarak dinlendir",
        "Gögüs agrisi varsa hemen 112'yi ara",
        "Veliyi bilgilendir",
    ]},
    "Gida Alerjisi (Anafilaksi Riski)": {"ikon": "🚨", "renk": "#dc2626", "acil_protokol": [
        "Hemen 112'yi ara",
        "Epipen varsa uygulamasina yardim et (dis uylugun disina)",
        "Ogrenciyi sirt ustu yatir, bacaklarini yukari kaldir",
        "Kusuyorsa yan cevir",
        "Nefes yolunu acik tut",
        "Veliyi bilgilendir",
    ]},
}

_HIJYEN_ALANLARI = [
    "Sinif Temizligi", "Tuvalet Hijyeni", "Yemekhane Temizligi",
    "Spor Salonu", "El Yikama Istasyonlari", "Kantin Denetimi",
    "Cöp Kutulari", "Havalandirma",
]

_HIJYEN_PUANLAMA = {"Cok Iyi": 5, "Iyi": 4, "Orta": 3, "Yetersiz": 2, "Kritik": 1}
_HIJYEN_RENK = {"Cok Iyi": "#10b981", "Iyi": "#34d399", "Orta": "#f59e0b", "Yetersiz": "#ef4444", "Kritik": "#dc2626"}

_MUAFIYET_TURLERI = ["Tam Muaf", "Kisitli Katilim", "Gecici Muaf", "Gozlemci"]
_MUAFIYET_RENK = {"Tam Muaf": "#ef4444", "Kisitli Katilim": "#f59e0b", "Gecici Muaf": "#3b82f6", "Gozlemci": "#8b5cf6"}

_KISITLAMA_SECENEKLERI = [
    "Kosamaz", "Yüzemez", "Top sporlarindan muaf", "Jimnastik yapamazmaaz",
    "Agir kaldirmaz", "Uzun sureli efor yasakli", "Sadece yuruyus",
    "Dis mekan aktivite yasakli", "Diger",
]


# ════════════════════════════════════════════════════════════
# 1. ACİL DURUM YÖNETİM MERKEZİ & ALERJİ/KRONİK ALARM
# ════════════════════════════════════════════════════════════

def render_acil_durum_merkezi(store):
    """Acil Durum Yönetim Merkezi — alerji/kronik kart, acil protokol, 112 takip."""
    styled_section("Acil Durum Yonetim Merkezi", "#dc2626")
    styled_info_banner(
        "Alerji, diyabet, epilepsi, astim gibi kritik durumu olan ogrencilerin "
        "acil mudahale kartlari. Ders programina entegre alarm sistemi.",
        banner_type="warning", icon="🚨")

    acil_kartlar = _lj("acil_durum_kartlari.json")
    acil_olaylar = _lj("acil_olaylar.json")

    # KPI
    toplam_kart = len(acil_kartlar)
    alerji_sayi = sum(1 for k in acil_kartlar if k.get("alerjiler"))
    kronik_sayi = sum(1 for k in acil_kartlar if k.get("kronik_hastalik"))
    olay_bu_ay = sum(1 for o in acil_olaylar if o.get("tarih", "")[:7] == date.today().strftime("%Y-%m"))

    styled_stat_row([
        ("Acil Kart", str(toplam_kart), "#dc2626", "🆘"),
        ("Alerjili", str(alerji_sayi), "#ef4444", "🍎"),
        ("Kronik", str(kronik_sayi), "#8b5cf6", "💊"),
        ("Bu Ay Olay", str(olay_bu_ay), "#f59e0b", "🚑"),
    ])

    sub = st.tabs(["🆘 Acil Kart Olustur", "📋 Acil Kart Listesi", "🚑 Olay Kaydi", "📖 Protokol Rehberi", "⚠️ Gunluk Alarm"])

    # ── ACİL KART OLUŞTUR ──
    with sub[0]:
        styled_section("Yeni Acil Durum Karti")
        with st.form("acil_kart_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("ac_ogr")
                kronik = st.selectbox("Kronik Hastalik", ["Yok"] + list(_KRONIK_HASTALIKLAR.keys()), key="ac_kronik")
                kan_grubu = st.selectbox("Kan Grubu", ["Bilinmiyor", "A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"], key="ac_kan")
            with c2:
                alerji_turu = st.multiselect("Alerji Turleri", list(_ALERJI_TURLERI.keys()), key="ac_alerji_tur")
                alerji_detay = st.text_input("Alerji Detay (ornek: Findik, Penisilin)", key="ac_alerji_det")
                epipen = st.checkbox("Epipen Tasiyormu?", key="ac_epipen")

            veli_tel = st.text_input("Veli Acil Telefon", key="ac_veli_tel")
            doktor_tel = st.text_input("Doktor / Hastane Telefon", key="ac_doktor_tel")
            ozel_not = st.text_area("Ozel Talimatlar", height=60, key="ac_ozel",
                placeholder="Insülin dozu, nöbet ilacı saati, diyet kısıtlamaları...")

            if st.form_submit_button("Acil Karti Kaydet", use_container_width=True, type="primary"):
                if ogr:
                    kart = {
                        "id": f"ac_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif": ogr.get("sinif", ""),
                        "sube": ogr.get("sube", ""),
                        "kronik_hastalik": kronik if kronik != "Yok" else "",
                        "alerjiler": alerji_detay,
                        "alerji_turleri": alerji_turu,
                        "epipen": epipen,
                        "kan_grubu": kan_grubu,
                        "veli_tel": veli_tel,
                        "doktor_tel": doktor_tel,
                        "ozel_not": ozel_not,
                        "created_at": datetime.now().isoformat(),
                    }
                    acil_kartlar.append(kart)
                    _sj("acil_durum_kartlari.json", acil_kartlar)
                    st.success(f"Acil durum karti olusturuldu!")
                    st.rerun()

    # ── ACİL KART LİSTESİ ──
    with sub[1]:
        styled_section("Acil Durum Kartlari")
        if not acil_kartlar:
            st.info("Henuz acil kart yok.")
        else:
            for k in acil_kartlar:
                kronik = k.get("kronik_hastalik", "")
                alerji = k.get("alerjiler", "")
                has_epipen = k.get("epipen", False)
                renk = "#dc2626" if kronik or alerji else "#10b981"
                kronik_info = _KRONIK_HASTALIKLAR.get(kronik, {})

                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid {renk};border-left:6px solid {renk};
                    border-radius:0 14px 14px 0;padding:14px 18px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#fca5a5;font-weight:900;font-size:1rem;">🆘 {k.get('ogrenci_ad','')}</span>
                            <span style="color:#64748b;font-size:0.75rem;margin-left:8px;">{k.get('sinif','')}/{k.get('sube','')}</span>
                        </div>
                        <span style="color:#94a3b8;font-size:0.7rem;">Kan: {k.get('kan_grubu','?')}</span>
                    </div>
                    <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">
                        {f'<span style="background:#dc262620;color:#dc2626;padding:3px 10px;border-radius:6px;font-size:0.7rem;font-weight:700;">{kronik_info.get("ikon","")} {kronik}</span>' if kronik else ''}
                        {f'<span style="background:#ef444420;color:#ef4444;padding:3px 10px;border-radius:6px;font-size:0.7rem;font-weight:700;">🍎 Alerji: {alerji}</span>' if alerji else ''}
                        {f'<span style="background:#f59e0b20;color:#f59e0b;padding:3px 10px;border-radius:6px;font-size:0.7rem;font-weight:700;">💉 Epipen Var</span>' if has_epipen else ''}
                    </div>
                    <div style="color:#64748b;font-size:0.68rem;margin-top:6px;">
                        Veli: {k.get('veli_tel','-')} | Doktor: {k.get('doktor_tel','-')}
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── OLAY KAYDI ──
    with sub[2]:
        styled_section("Acil Olay Kaydi")
        with st.form("acil_olay_form"):
            c1, c2 = st.columns(2)
            with c1:
                ao_ogr = _ogr_sec("ao_ogr")
                ao_tur = st.selectbox("Olay Turu",
                    ["Anafilaksi", "Diyabetik Kriz", "Epilepsi Nobet", "Astim Krizi",
                     "Düşme/Yaralanma", "Bayilma", "112 Cagrildi", "Diger"], key="ao_tur")
            with c2:
                ao_tarih = st.date_input("Tarih", key="ao_tarih")
                ao_saat = st.time_input("Saat", key="ao_saat")

            ao_aciklama = st.text_area("Olay Aciklamasi", height=60, key="ao_acik")
            ao_mudahale = st.text_area("Yapilan Mudahale", height=60, key="ao_mud")
            ao_ambulans = st.checkbox("Ambulans cagrildi mi?", key="ao_amb")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if ao_ogr:
                    olay = {
                        "id": f"ao_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ao_ogr.get("id", ""),
                        "ogrenci_ad": f"{ao_ogr.get('ad','')} {ao_ogr.get('soyad','')}",
                        "tur": ao_tur,
                        "tarih": ao_tarih.isoformat(),
                        "saat": str(ao_saat),
                        "aciklama": ao_aciklama,
                        "mudahale": ao_mudahale,
                        "ambulans": ao_ambulans,
                        "created_at": datetime.now().isoformat(),
                    }
                    acil_olaylar.append(olay)
                    _sj("acil_olaylar.json", acil_olaylar)
                    st.success("Acil olay kaydedildi!")
                    st.rerun()

    # ── PROTOKOL REHBERİ ──
    with sub[3]:
        styled_section("Kronik Hastalik Acil Protokolleri")
        for hastalik, info in _KRONIK_HASTALIKLAR.items():
            with st.expander(f"{info['ikon']} {hastalik}"):
                for i, adim in enumerate(info["acil_protokol"], 1):
                    st.markdown(f"""
                    <div style="display:flex;gap:8px;padding:4px 0;padding-left:10px;border-left:3px solid {info['renk']};">
                        <span style="background:{info['renk']};color:#fff;min-width:22px;height:22px;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.65rem;">{i}</span>
                        <span style="color:#e2e8f0;font-size:0.82rem;">{adim}</span>
                    </div>""", unsafe_allow_html=True)

    # ── GÜNLÜK ALARM ──
    with sub[4]:
        styled_section("Bugunun Acil Durum Alarmlari")
        if not acil_kartlar:
            st.success("Acil kart kaydi yok — alarm yok.")
        else:
            # Sinif bazli uyarilar
            sinif_grp = defaultdict(list)
            for k in acil_kartlar:
                sinif_grp[f"{k.get('sinif','')}/{k.get('sube','')}"].append(k)

            for sinif, kartlar in sorted(sinif_grp.items()):
                alerji_list = [k for k in kartlar if k.get("alerjiler")]
                kronik_list = [k for k in kartlar if k.get("kronik_hastalik")]

                if alerji_list or kronik_list:
                    st.markdown(f"""
                    <div style="background:#dc262610;border:1px solid #dc262630;border-left:5px solid #dc2626;
                        border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                        <div style="color:#fca5a5;font-weight:800;font-size:0.85rem;">⚠️ Sinif {sinif}</div>
                        <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                            {''.join(f"🍎 <b>{k.get('ogrenci_ad','')}</b>: {k.get('alerjiler','')} | " for k in alerji_list)}
                            {''.join(f"{_KRONIK_HASTALIKLAR.get(k.get('kronik_hastalik',''),{}).get('ikon','')} <b>{k.get('ogrenci_ad','')}</b>: {k.get('kronik_hastalik','')} | " for k in kronik_list)}
                        </div>
                    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. BESLENME & HİJYEN TAKİP SİSTEMİ
# ════════════════════════════════════════════════════════════

def render_beslenme_hijyen(store):
    """Beslenme & Hijyen Takip — menü alerjen kontrolü, hijyen puanlama."""
    styled_section("Beslenme & Hijyen Takip Sistemi", "#059669")
    styled_info_banner(
        "Yemekhane menu alerjen kontrolu, kantin denetimi, hijyen gozlem, "
        "sinif temizlik puanlamasi. Otomatik alerji uyarisi.",
        banner_type="info", icon="🍎")

    hijyen_kayitlari = _lj("hijyen_kayitlari.json")
    menu_kayitlari = _lj("menu_kayitlari.json")
    acil_kartlar = _lj("acil_durum_kartlari.json")

    styled_stat_row([
        ("Hijyen Kaydi", str(len(hijyen_kayitlari)), "#059669", "🧹"),
        ("Menu Kaydi", str(len(menu_kayitlari)), "#f59e0b", "🍽️"),
        ("Alerjili Ogrenci", str(sum(1 for k in acil_kartlar if k.get("alerjiler"))), "#ef4444", "⚠️"),
    ])

    sub = st.tabs(["🍽️ Menu & Alerjen", "🧹 Hijyen Gozlem", "📊 Hijyen Raporu", "⚠️ Alerjen Alarm"])

    # ── MENÜ & ALERJEN ──
    with sub[0]:
        styled_section("Gunluk Menu Kaydi & Alerjen Kontrolu")
        with st.form("menu_form"):
            m_tarih = st.date_input("Tarih", value=date.today(), key="mn_tarih")
            m_corba = st.text_input("Corba", key="mn_corba")
            m_ana = st.text_input("Ana Yemek", key="mn_ana")
            m_yan = st.text_input("Yan Yemek / Pilav", key="mn_yan")
            m_tatli = st.text_input("Tatli / Meyve", key="mn_tatli")
            m_alerjenler = st.multiselect("Icerdigi Alerjenler",
                ["Findik", "Yer fistigi", "Sut", "Yumurta", "Gluten", "Balik", "Soya", "Susam", "Kabuklu deniz urunu"],
                key="mn_alerjen")

            if st.form_submit_button("Menuyu Kaydet", use_container_width=True):
                kayit = {
                    "id": f"mn_{uuid.uuid4().hex[:8]}",
                    "tarih": m_tarih.isoformat(),
                    "corba": m_corba, "ana": m_ana, "yan": m_yan, "tatli": m_tatli,
                    "alerjenler": m_alerjenler,
                    "created_at": datetime.now().isoformat(),
                }
                menu_kayitlari.append(kayit)
                _sj("menu_kayitlari.json", menu_kayitlari)

                # Alerjen uyarisi
                if m_alerjenler:
                    riskli = []
                    for k in acil_kartlar:
                        if k.get("alerjiler"):
                            for alerjen in m_alerjenler:
                                if alerjen.lower() in k.get("alerjiler", "").lower():
                                    riskli.append((k.get("ogrenci_ad",""), alerjen, k.get("sinif",""), k.get("sube","")))
                    if riskli:
                        st.error(f"🚨 ALERJEN UYARISI: {len(riskli)} ogrenci risk altinda!")
                        for ad, alj, sinif, sube in riskli:
                            st.warning(f"  ⚠️ {ad} ({sinif}/{sube}) — {alj} alerjisi var!")
                    else:
                        st.success("Alerjen kontrolu tamam — riskli ogrenci yok.")
                else:
                    st.success("Menu kaydedildi!")
                st.rerun()

    # ── HİJYEN GÖZLEM ──
    with sub[1]:
        styled_section("Hijyen Gozlem Kaydi")
        with st.form("hijyen_form"):
            h_tarih = st.date_input("Tarih", key="hj_tarih")
            h_alan = st.selectbox("Gozlem Alani", _HIJYEN_ALANLARI, key="hj_alan")
            h_puan = st.selectbox("Deger", list(_HIJYEN_PUANLAMA.keys()), key="hj_puan")
            h_not = st.text_area("Gozlem Notu", height=60, key="hj_not")

            if st.form_submit_button("Kaydet", use_container_width=True):
                kayit = {
                    "id": f"hj_{uuid.uuid4().hex[:8]}",
                    "tarih": h_tarih.isoformat(),
                    "alan": h_alan,
                    "puan": h_puan,
                    "puan_sayi": _HIJYEN_PUANLAMA.get(h_puan, 3),
                    "not": h_not,
                    "created_at": datetime.now().isoformat(),
                }
                hijyen_kayitlari.append(kayit)
                _sj("hijyen_kayitlari.json", hijyen_kayitlari)
                st.success(f"{h_alan}: {h_puan}")
                st.rerun()

    # ── HİJYEN RAPORU ──
    with sub[2]:
        styled_section("Hijyen Puanlama Raporu")
        if not hijyen_kayitlari:
            st.info("Veri yok.")
        else:
            alan_ort = defaultdict(list)
            for h in hijyen_kayitlari:
                alan_ort[h.get("alan","?")].append(h.get("puan_sayi", 3))

            genel_puan = 0
            toplam = 0
            for alan in _HIJYEN_ALANLARI:
                puanlar = alan_ort.get(alan, [])
                if puanlar:
                    ort = round(sum(puanlar) / len(puanlar), 1)
                    genel_puan += ort
                    toplam += 1
                    pct = round(ort / 5 * 100)
                    renk = "#10b981" if ort >= 4 else "#f59e0b" if ort >= 3 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin:5px 0;">
                        <span style="min-width:160px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{alan}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                                display:flex;align-items:center;padding-left:8px;">
                                <span style="font-size:0.6rem;color:#fff;font-weight:800;">{ort}/5</span>
                            </div>
                        </div>
                        <span style="font-size:0.65rem;color:#64748b;">{len(puanlar)} gozlem</span>
                    </div>""", unsafe_allow_html=True)

            if toplam > 0:
                genel = round(genel_puan / toplam, 1)
                g_renk = "#10b981" if genel >= 4 else "#f59e0b" if genel >= 3 else "#ef4444"
                st.markdown(f"""
                <div style="text-align:center;margin-top:12px;color:{g_renk};font-weight:900;font-size:1.2rem;">
                    Genel Hijyen Puani: {genel}/5</div>""", unsafe_allow_html=True)

    # ── ALERJEN ALARM ──
    with sub[3]:
        styled_section("Alerjen Alarm Paneli")
        # Bugunun menusu
        bugun = date.today().isoformat()
        bugun_menu = next((m for m in menu_kayitlari if m.get("tarih") == bugun), None)

        if bugun_menu and bugun_menu.get("alerjenler"):
            alerjenler = bugun_menu["alerjenler"]
            st.warning(f"Bugunku menude alerjenler: **{', '.join(alerjenler)}**")

            riskli = []
            for k in acil_kartlar:
                if k.get("alerjiler"):
                    for alj in alerjenler:
                        if alj.lower() in k.get("alerjiler","").lower():
                            riskli.append(k)
                            break

            if riskli:
                st.error(f"🚨 {len(riskli)} ogrenci risk altinda!")
                for k in riskli:
                    st.markdown(f"""
                    <div style="background:#dc262615;border:1px solid #dc2626;border-radius:10px;
                        padding:8px 14px;margin:4px 0;">
                        <span style="color:#fca5a5;font-weight:800;">⚠️ {k.get('ogrenci_ad','')}</span>
                        <span style="color:#94a3b8;font-size:0.72rem;"> — {k.get('sinif','')}/{k.get('sube','')} — Alerji: {k.get('alerjiler','')}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("Alerjili ogrenci icin risk yok.")
        elif bugun_menu:
            st.success("Bugunku menude alerjen bildirilmemis.")
        else:
            st.info("Bugunku menu henuz girilmemis.")


# ════════════════════════════════════════════════════════════
# 3. SPOR MUAFİYETİ & FİZİKSEL AKTİVİTE UYGUNLUK
# ════════════════════════════════════════════════════════════

def render_spor_muafiyet(store):
    """Spor Muafiyeti & Fiziksel Aktivite Uygunluk — muafiyet takip, bilgilendirme."""
    styled_section("Spor Muafiyeti & Fiziksel Aktivite Uygunluk", "#f59e0b")
    styled_info_banner(
        "Saglik raporu gerektiren ogrencilerin spor muafiyet takibi, "
        "beden egitimi kisitlama listesi, ogretmen bilgilendirme.",
        banner_type="info", icon="🏃")

    muafiyetler = _lj("spor_muafiyetleri.json")

    # KPI
    aktif = [m for m in muafiyetler if m.get("durum") == "Aktif"]
    tam_muaf = sum(1 for m in aktif if m.get("tur") == "Tam Muaf")
    kisitli = sum(1 for m in aktif if m.get("tur") == "Kisitli Katilim")
    gecici = sum(1 for m in aktif if m.get("tur") == "Gecici Muaf")

    styled_stat_row([
        ("Aktif Muafiyet", str(len(aktif)), "#f59e0b", "🏃"),
        ("Tam Muaf", str(tam_muaf), "#ef4444", "🔴"),
        ("Kisitli", str(kisitli), "#f59e0b", "🟡"),
        ("Gecici", str(gecici), "#3b82f6", "🔵"),
    ])

    sub = st.tabs(["➕ Muafiyet Ekle", "📋 Muafiyet Listesi", "👨‍🏫 Ogretmen Bilgilendirme", "📊 Sinif Ozeti"])

    # ── MUAFİYET EKLE ──
    with sub[0]:
        styled_section("Yeni Spor Muafiyeti")
        with st.form("muaf_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("sp_ogr")
                m_tur = st.selectbox("Muafiyet Turu", _MUAFIYET_TURLERI, key="sp_tur")
                m_neden = st.text_input("Neden / Tani", placeholder="Kirik, astim, ameliyat sonrasi...", key="sp_neden")
            with c2:
                m_baslangic = st.date_input("Baslangic", key="sp_bas")
                m_bitis = st.date_input("Bitis (gecici icin)", key="sp_bit")
                m_kisitlar = st.multiselect("Kisitlamalar", _KISITLAMA_SECENEKLERI, key="sp_kisit")

            m_rapor = st.checkbox("Saglik raporu mevcut mu?", key="sp_rapor")
            m_not = st.text_area("Ek Notlar", height=60, key="sp_not")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if ogr:
                    kayit = {
                        "id": f"sp_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif": ogr.get("sinif", ""),
                        "sube": ogr.get("sube", ""),
                        "tur": m_tur,
                        "neden": m_neden,
                        "kisitlamalar": m_kisitlar,
                        "baslangic": m_baslangic.isoformat(),
                        "bitis": m_bitis.isoformat() if m_tur == "Gecici Muaf" else "",
                        "rapor_var": m_rapor,
                        "not": m_not,
                        "durum": "Aktif",
                        "created_at": datetime.now().isoformat(),
                    }
                    muafiyetler.append(kayit)
                    _sj("spor_muafiyetleri.json", muafiyetler)
                    st.success(f"{m_tur} muafiyeti kaydedildi!")
                    st.rerun()

    # ── MUAFİYET LİSTESİ ──
    with sub[1]:
        styled_section("Aktif Muafiyetler")
        if not aktif:
            st.success("Aktif muafiyet yok.")
        else:
            for m in aktif:
                renk = _MUAFIYET_RENK.get(m.get("tur",""), "#94a3b8")
                # Gecici muafiyet bitis kontrolu
                gecikme = ""
                if m.get("tur") == "Gecici Muaf" and m.get("bitis"):
                    try:
                        bitis = date.fromisoformat(m["bitis"])
                        if bitis < date.today():
                            gecikme = " — SURESI DOLDU!"
                            renk = "#dc2626"
                    except Exception:
                        pass

                st.markdown(f"""
                <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 12px 12px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">
                            🏃 {m.get('ogrenci_ad','')}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.7rem;font-weight:700;">{m.get('tur','')}{gecikme}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {m.get('sinif','')}/{m.get('sube','')} | Neden: {m.get('neden','')} |
                        {m.get('baslangic','')[:10]}{f" → {m.get('bitis','')[:10]}" if m.get('bitis') else ' (surekli)'}</div>
                    {"<div style='color:#64748b;font-size:0.65rem;margin-top:2px;'>Kisitlamalar: " + ", ".join(m.get("kisitlamalar",[])) + "</div>" if m.get("kisitlamalar") else ""}
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {m.get('id','')}", expanded=False):
                    if st.button("Muafiyeti Kapat", key=f"sp_kapat_{m['id']}"):
                        m["durum"] = "Kapandi"
                        _sj("spor_muafiyetleri.json", muafiyetler)
                        st.success("Muafiyet kapatildi!")
                        st.rerun()

    # ── ÖĞRETMEN BİLGİLENDİRME ──
    with sub[2]:
        styled_section("Beden Egitimi Ogretmenine Bilgilendirme")
        if not aktif:
            st.success("Bildirilecek muafiyet yok.")
        else:
            sinif_grp = defaultdict(list)
            for m in aktif:
                sinif_grp[f"{m.get('sinif','')}/{m.get('sube','')}"].append(m)

            for sinif, muaf_list in sorted(sinif_grp.items()):
                tam = sum(1 for m in muaf_list if m.get("tur") == "Tam Muaf")
                kisit = sum(1 for m in muaf_list if m.get("tur") == "Kisitli Katilim")

                st.markdown(f"""
                <div style="background:#f59e0b10;border:1px solid #f59e0b30;border-left:4px solid #f59e0b;
                    border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0;">
                    <div style="color:#fbbf24;font-weight:800;font-size:0.85rem;">🏫 Sinif {sinif}</div>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:4px;">
                        {tam} tam muaf, {kisit} kisitli katilim</div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        {''.join(f"• <b>{m.get('ogrenci_ad','')}</b>: {m.get('tur','')} ({m.get('neden','')}) " for m in muaf_list)}
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── SINIF ÖZETİ ──
    with sub[3]:
        styled_section("Sinif Bazli Muafiyet Ozeti")
        if not muafiyetler:
            st.info("Veri yok.")
        else:
            tur_say = Counter(m.get("tur","?") for m in aktif)
            for tur, sayi in tur_say.most_common():
                renk = _MUAFIYET_RENK.get(tur, "#94a3b8")
                st.markdown(f"""
                <div style="display:inline-block;background:{renk}15;color:{renk};padding:8px 18px;
                    border-radius:12px;border:1px solid {renk}30;margin:4px;font-size:0.85rem;font-weight:800;">
                    {tur}: {sayi}
                </div>""", unsafe_allow_html=True)

            # Neden dagilimi
            styled_section("Muafiyet Nedeni Dagilimi")
            neden_say = Counter(m.get("neden","?") for m in aktif if m.get("neden"))
            if neden_say:
                for neden, sayi in neden_say.most_common(8):
                    st.markdown(f"- **{neden}**: {sayi} ogrenci")
