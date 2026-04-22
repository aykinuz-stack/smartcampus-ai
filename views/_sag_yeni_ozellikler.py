"""
Okul Sağlığı — Yeni Özellikler
================================
1. Salgın & Bulaşıcı Hastalık Takip Sistemi
2. Aşı & Periyodik Sağlık Kontrol Takvimi
3. Öğrenci Sağlık Risk Profili & AI Erken Uyarı
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

def _lj(name: str) -> list:
    p = os.path.join(_sag_dir(), name)
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _sj(name: str, data: list) -> None:
    with open(os.path.join(_sag_dir(), name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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

_BULASICI_HASTALIKLAR = [
    "Grip / Influenza",
    "COVID-19",
    "Su Cicegi (Varicella)",
    "El-Ayak-Agiz Hastaligi",
    "Kizamik",
    "Kabakulak",
    "Kizamikçik",
    "Ishal / Gastroenterit",
    "Bogmaca",
    "Konjonktivit (Goz Enfeksiyonu)",
    "Bit / Uyuz",
    "Hepatit A",
    "Streptokok Enfeksiyonu",
    "Diger",
]

_SALGIN_SEVIYELERI = {
    "Vaka": {"renk": "#f59e0b", "ikon": "🟡", "aciklama": "Tek tuk vakalar"},
    "Kume": {"renk": "#f97316", "ikon": "🟠", "aciklama": "Ayni sinifta 3+ vaka"},
    "Salgin": {"renk": "#ef4444", "ikon": "🔴", "aciklama": "Birden fazla sinifta yayilim"},
    "Ciddi Salgin": {"renk": "#dc2626", "ikon": "🚨", "aciklama": "Okul geneli, resmi bildirim gerekli"},
}

_KARANTINA_SURELERI = {
    "Grip / Influenza": 5,
    "COVID-19": 5,
    "Su Cicegi (Varicella)": 7,
    "El-Ayak-Agiz Hastaligi": 7,
    "Kizamik": 10,
    "Kabakulak": 9,
    "Kizamikçik": 7,
    "Ishal / Gastroenterit": 3,
    "Bogmaca": 5,
    "Konjonktivit (Goz Enfeksiyonu)": 3,
    "Bit / Uyuz": 2,
    "Hepatit A": 14,
}

_ASI_TAKVIMI = [
    {"asi": "BCG (Verem)", "donem": "Dogumda", "yas": 0, "zorunlu": True},
    {"asi": "Hepatit B - 1. Doz", "donem": "Dogumda", "yas": 0, "zorunlu": True},
    {"asi": "Hepatit B - 2. Doz", "donem": "1. Ay", "yas": 0, "zorunlu": True},
    {"asi": "Hepatit B - 3. Doz", "donem": "6. Ay", "yas": 0, "zorunlu": True},
    {"asi": "DaBT-IPA-Hib - 1. Doz", "donem": "2. Ay", "yas": 0, "zorunlu": True},
    {"asi": "KPA - 1. Doz", "donem": "2. Ay", "yas": 0, "zorunlu": True},
    {"asi": "OPA - 1. Doz", "donem": "6. Ay", "yas": 0, "zorunlu": True},
    {"asi": "KKK - 1. Doz", "donem": "12. Ay", "yas": 1, "zorunlu": True},
    {"asi": "KKK - 2. Doz", "donem": "1. Sinif", "yas": 6, "zorunlu": True},
    {"asi": "DaBT-IPA Rapel", "donem": "1. Sinif", "yas": 6, "zorunlu": True},
    {"asi": "Td Rapel", "donem": "8. Sinif", "yas": 13, "zorunlu": True},
    {"asi": "HPV - 1. Doz (Kiz)", "donem": "5-6. Sinif", "yas": 11, "zorunlu": False},
    {"asi": "HPV - 2. Doz (Kiz)", "donem": "5-6. Sinif", "yas": 11, "zorunlu": False},
]

_PERIYODIK_KONTROLLER = [
    {"kontrol": "Boy-Kilo Olcumu", "periyot": "Her donem", "siniflar": "Tumu"},
    {"kontrol": "Gorme Taramasi", "periyot": "Yilda 1", "siniflar": "1, 4, 8. sinif"},
    {"kontrol": "Isitme Taramasi", "periyot": "Yilda 1", "siniflar": "1. sinif"},
    {"kontrol": "Skolyoz Taramasi", "periyot": "Yilda 1", "siniflar": "5-8. sinif"},
    {"kontrol": "Dis Sagligi Taramasi", "periyot": "Yilda 1", "siniflar": "Tumu"},
    {"kontrol": "BMI Hesaplama", "periyot": "Her donem", "siniflar": "Tumu"},
]


# ════════════════════════════════════════════════════════════
# 1. SALGIN & BULAŞICI HASTALIK TAKİP SİSTEMİ
# ════════════════════════════════════════════════════════════

def render_salgin_takip(store):
    """Salgın & Bulaşıcı Hastalık Takip — vaka kayıt, temas izleme, salgın uyarı."""
    styled_section("Salgin & Bulasici Hastalik Takip", "#ef4444")
    styled_info_banner(
        "Bulasici hastaliklarin sinif/kademe bazli yayilma takibi. "
        "Temas izleme, karantina onerisi, Ilce Saglik Mudurlugu bildirimi.",
        banner_type="warning", icon="🌡️")

    vakalar = _lj("salgin_vakalari.json")

    # KPI
    bugun = date.today().isoformat()
    bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    aktif = sum(1 for v in vakalar if v.get("durum") == "Aktif")
    bu_hafta_sayi = sum(1 for v in vakalar if v.get("tarih", "")[:10] >= bu_hafta)
    hastalik_say = len(set(v.get("hastalik", "") for v in vakalar if v.get("durum") == "Aktif"))

    # Salgin seviye hesapla
    sinif_grp = defaultdict(int)
    for v in vakalar:
        if v.get("durum") == "Aktif":
            sinif_grp[v.get("sinif_sube", "?")] += 1
    max_sinif_vaka = max(sinif_grp.values()) if sinif_grp else 0
    coklu_sinif = sum(1 for s, c in sinif_grp.items() if c >= 2)

    if coklu_sinif >= 3:
        seviye = "Ciddi Salgin"
    elif coklu_sinif >= 2:
        seviye = "Salgin"
    elif max_sinif_vaka >= 3:
        seviye = "Kume"
    else:
        seviye = "Vaka"

    sev_info = _SALGIN_SEVIYELERI[seviye]

    styled_stat_row([
        ("Aktif Vaka", str(aktif), "#ef4444", "🦠"),
        ("Bu Hafta", str(bu_hafta_sayi), "#f59e0b", "📅"),
        ("Hastalik Turu", str(hastalik_say), "#8b5cf6", "🏷️"),
        ("Seviye", seviye, sev_info["renk"], sev_info["ikon"]),
    ])

    if seviye in ("Salgin", "Ciddi Salgin"):
        st.error(f"🚨 SALGIN UYARISI: {seviye} — {coklu_sinif} sinifta aktif vaka! Ilce Saglik bilgilendirilmeli.")

    sub = st.tabs(["➕ Vaka Kayit", "📋 Vaka Listesi", "🔍 Temas Izleme", "📊 Salgin Haritasi", "📄 Bildirim"])

    # ── VAKA KAYIT ──
    with sub[0]:
        styled_section("Yeni Vaka Kaydi")
        with st.form("salgin_vaka_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("sg_ogr")
                hastalik = st.selectbox("Hastalik", _BULASICI_HASTALIKLAR, key="sg_hastalik")
                tarih = st.date_input("Tespit Tarihi", value=date.today(), key="sg_tarih")
            with c2:
                belirtiler = st.text_input("Belirtiler", key="sg_belirti")
                doktor_onay = st.checkbox("Doktor Onayli Mi?", key="sg_doktor")
                karantina = st.checkbox("Karantinaya Alindi Mi?", key="sg_karantina")

            notlar = st.text_area("Ek Notlar", height=60, key="sg_not")

            if st.form_submit_button("Vakayi Kaydet", use_container_width=True):
                if ogr:
                    karantina_gun = _KARANTINA_SURELERI.get(hastalik, 5)
                    donus_tarih = (tarih + timedelta(days=karantina_gun)).isoformat()
                    vaka = {
                        "id": f"sv_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif_sube": f"{ogr.get('sinif','')}/{ogr.get('sube','')}",
                        "hastalik": hastalik,
                        "belirtiler": belirtiler,
                        "doktor_onay": doktor_onay,
                        "karantina": karantina,
                        "karantina_gun": karantina_gun,
                        "tahmini_donus": donus_tarih,
                        "notlar": notlar,
                        "durum": "Aktif",
                        "tarih": tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    vakalar.append(vaka)
                    _sj("salgin_vakalari.json", vakalar)
                    st.success(f"Vaka kaydedildi! Karantina suresi: {karantina_gun} gun, donus: {donus_tarih}")
                    st.rerun()

    # ── VAKA LİSTESİ ──
    with sub[1]:
        styled_section("Aktif Vakalar")
        aktif_list = [v for v in vakalar if v.get("durum") == "Aktif"]
        if not aktif_list:
            st.success("Aktif vaka yok.")
        else:
            for v in sorted(aktif_list, key=lambda x: x.get("tarih",""), reverse=True):
                renk = "#ef4444" if v.get("karantina") else "#f59e0b"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">
                            🦠 {v.get('ogrenci_ad','')} — {v.get('sinif_sube','')}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.7rem;font-weight:700;">{'Karantina' if v.get('karantina') else 'Aktif'}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {v.get('hastalik','')} | {v.get('tarih','')[:10]} | Donus: {v.get('tahmini_donus','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {v.get('id','')}", expanded=False):
                    if st.button("Iyilesti — Vakayi Kapat", key=f"sg_kapat_{v['id']}"):
                        v["durum"] = "Kapandi"
                        v["kapanma_tarihi"] = datetime.now().isoformat()
                        _sj("salgin_vakalari.json", vakalar)
                        st.success("Vaka kapatildi!")
                        st.rerun()

    # ── TEMAS İZLEME ──
    with sub[2]:
        styled_section("Temas Izleme")
        if not aktif_list:
            st.info("Aktif vaka yok.")
        else:
            # Sinif bazli temas
            for v in aktif_list:
                sinif_sube = v.get("sinif_sube", "")
                students = load_shared_students()
                temaslilar = [s for s in students
                              if f"{s.get('sinif','')}/{s.get('sube','')}" == sinif_sube
                              and f"{s.get('ad','')} {s.get('soyad','')}" != v.get("ogrenci_ad","")]

                st.markdown(f"**{v.get('ogrenci_ad','')}** ({v.get('hastalik','')}) — {sinif_sube}")
                if temaslilar:
                    st.caption(f"{len(temaslilar)} potansiyel temasli ogrenci:")
                    for t in temaslilar[:15]:
                        st.markdown(f"  - {t.get('ad','')} {t.get('soyad','')} — izlenmeli")
                else:
                    st.info("Sinif arkadasi bulunamadi.")
                st.markdown("---")

    # ── SALGIN HARİTASI ──
    with sub[3]:
        styled_section("Sinif Bazli Salgin Haritasi")
        if not vakalar:
            st.info("Veri yok.")
        else:
            hastalik_grp = defaultdict(lambda: defaultdict(int))
            for v in vakalar:
                if v.get("durum") == "Aktif":
                    hastalik_grp[v.get("hastalik","?")][v.get("sinif_sube","?")] += 1

            for hastalik, siniflar in hastalik_grp.items():
                toplam = sum(siniflar.values())
                renk = "#dc2626" if toplam >= 5 else "#ef4444" if toplam >= 3 else "#f59e0b"
                st.markdown(f"**🦠 {hastalik}** — {toplam} aktif vaka")
                for sinif, sayi in sorted(siniflar.items(), key=lambda x: x[1], reverse=True):
                    bar_w = min(sayi * 20, 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:2px 0;padding-left:20px;">
                        <span style="min-width:40px;font-size:0.72rem;color:#94a3b8;">{sinif}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                st.markdown("")

    # ── BİLDİRİM ──
    with sub[4]:
        styled_section("Ilce Saglik Mudurlugu Bildirimi")
        if aktif > 0:
            st.markdown(f"""
            <div style="background:#dc262615;border:2px solid #dc2626;border-radius:12px;padding:14px 18px;">
                <div style="color:#fca5a5;font-weight:800;">Bildirim Formu Ozeti</div>
                <div style="color:#e2e8f0;font-size:0.8rem;margin-top:6px;">
                    Aktif vaka: <b>{aktif}</b> | Hastalik turu: <b>{hastalik_say}</b> | Seviye: <b>{seviye}</b>
                </div>
            </div>""", unsafe_allow_html=True)

            hastalik_ozet = Counter(v.get("hastalik","") for v in vakalar if v.get("durum") == "Aktif")
            for h, s in hastalik_ozet.most_common():
                st.markdown(f"- **{h}**: {s} vaka")
            st.caption("Bu bilgiler Ilce Saglik Mudurlugu'ne iletilmelidir.")
        else:
            st.success("Bildirim gerektiren durum yok.")


# ════════════════════════════════════════════════════════════
# 2. AŞI & PERİYODİK SAĞLIK KONTROL TAKVİMİ
# ════════════════════════════════════════════════════════════

def render_asi_takvimi(store):
    """Aşı & Periyodik Sağlık Kontrol Takvimi — MEB zorunlu aşı, boy-kilo, BMI."""
    styled_section("Asi & Periyodik Saglik Kontrol Takvimi", "#2563eb")
    styled_info_banner(
        "MEB zorunlu asi takvimi takibi, boy-kilo-gorme-isitme periyodik olcum, "
        "BMI hesaplama, eksik asi/kontrol uyarilari.",
        banner_type="info", icon="📋")

    asi_kayitlari = _lj("asi_kayitlari.json")
    olcum_kayitlari = _lj("saglik_olcumleri.json")

    students = load_shared_students()
    toplam_ogr = len(students)

    # KPI
    asi_yapilan = len(set(a.get("ogrenci_id","") for a in asi_kayitlari))
    olcum_yapilan = len(set(o.get("ogrenci_id","") for o in olcum_kayitlari))
    eksik_asi_ogr = toplam_ogr - asi_yapilan

    styled_stat_row([
        ("Toplam Ogrenci", str(toplam_ogr), "#2563eb", "👥"),
        ("Asi Kayitli", str(asi_yapilan), "#10b981", "💉"),
        ("Olcum Yapilan", str(olcum_yapilan), "#8b5cf6", "📏"),
        ("Eksik Asi", str(max(eksik_asi_ogr, 0)), "#ef4444", "⚠️"),
    ])

    sub = st.tabs(["💉 Asi Kaydi", "📏 Olcum Kaydi", "📅 MEB Takvim", "⚠️ Eksik Kontrol", "📊 BMI Analiz"])

    # ── AŞI KAYDI ──
    with sub[0]:
        styled_section("Asi Kaydi Ekle")
        with st.form("asi_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("asi_ogr")
                asi = st.selectbox("Asi Turu", [a["asi"] for a in _ASI_TAKVIMI], key="asi_tur")
            with c2:
                asi_tarih = st.date_input("Uygulama Tarihi", key="asi_tarih")
                asi_kurum = st.text_input("Uygulayan Kurum", placeholder="ASM, hastane...", key="asi_kurum")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if ogr:
                    kayit = {
                        "id": f"asi_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif": ogr.get("sinif", ""),
                        "sube": ogr.get("sube", ""),
                        "asi": asi,
                        "tarih": asi_tarih.isoformat(),
                        "kurum": asi_kurum,
                        "created_at": datetime.now().isoformat(),
                    }
                    asi_kayitlari.append(kayit)
                    _sj("asi_kayitlari.json", asi_kayitlari)
                    st.success(f"{ogr.get('ad','')} icin {asi} kaydedildi!")
                    st.rerun()

        # Son kayitlar
        if asi_kayitlari:
            styled_section("Son Asi Kayitlari")
            for a in sorted(asi_kayitlari, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 10px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #10b981;border-radius:0 8px 8px 0;">
                    <span style="color:#10b981;">💉</span>
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;">{a.get('ogrenci_ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.7rem;">{a.get('asi','')}</span>
                    <span style="color:#64748b;font-size:0.65rem;margin-left:auto;">{a.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── ÖLÇÜM KAYDI ──
    with sub[1]:
        styled_section("Boy-Kilo-Gorme-Isitme Olcumu")
        with st.form("olcum_form"):
            c1, c2 = st.columns(2)
            with c1:
                o_ogr = _ogr_sec("olc_ogr")
                o_boy = st.number_input("Boy (cm)", 50, 200, 140, key="olc_boy")
                o_kilo = st.number_input("Kilo (kg)", 10.0, 150.0, 40.0, step=0.5, key="olc_kilo")
            with c2:
                o_gorme_sag = st.text_input("Gorme (Sag)", placeholder="10/10", key="olc_gs")
                o_gorme_sol = st.text_input("Gorme (Sol)", placeholder="10/10", key="olc_gsl")
                o_isitme = st.selectbox("Isitme", ["Normal", "Hafif Kayip", "Orta Kayip", "İleri Kayip"], key="olc_is")

            o_tarih = st.date_input("Olcum Tarihi", key="olc_tarih")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if o_ogr:
                    boy_m = o_boy / 100
                    bmi = round(o_kilo / (boy_m * boy_m), 1) if boy_m > 0 else 0
                    bmi_durum = "Normal" if 18.5 <= bmi <= 24.9 else "Zayif" if bmi < 18.5 else "Kilolu" if bmi < 30 else "Obez"

                    kayit = {
                        "id": f"olc_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": o_ogr.get("id", ""),
                        "ogrenci_ad": f"{o_ogr.get('ad','')} {o_ogr.get('soyad','')}",
                        "sinif": o_ogr.get("sinif", ""),
                        "sube": o_ogr.get("sube", ""),
                        "boy": o_boy,
                        "kilo": o_kilo,
                        "bmi": bmi,
                        "bmi_durum": bmi_durum,
                        "gorme_sag": o_gorme_sag,
                        "gorme_sol": o_gorme_sol,
                        "isitme": o_isitme,
                        "tarih": o_tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    olcum_kayitlari.append(kayit)
                    _sj("saglik_olcumleri.json", olcum_kayitlari)
                    bmi_renk = "#10b981" if bmi_durum == "Normal" else "#f59e0b" if bmi_durum in ("Zayif","Kilolu") else "#ef4444"
                    st.success(f"Olcum kaydedildi! BMI: {bmi} ({bmi_durum})")
                    st.rerun()

    # ── MEB TAKVİM ──
    with sub[2]:
        styled_section("MEB Zorunlu Asi Takvimi")
        for a in _ASI_TAKVIMI:
            zorunlu_badge = "🔴 Zorunlu" if a["zorunlu"] else "🔵 Onerilen"
            renk = "#ef4444" if a["zorunlu"] else "#3b82f6"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">💉 {a['asi']}</span>
                <span style="color:#94a3b8;font-size:0.7rem;">{a['donem']}</span>
                <span style="color:{renk};font-size:0.65rem;font-weight:700;">{zorunlu_badge}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        styled_section("Periyodik Saglik Kontrolleri")
        for k in _PERIYODIK_KONTROLLER:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid #2563eb;border-radius:0 8px 8px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">📋 {k['kontrol']}</span>
                <span style="color:#94a3b8;font-size:0.7rem;">{k['periyot']}</span>
                <span style="color:#64748b;font-size:0.65rem;">{k['siniflar']}</span>
            </div>""", unsafe_allow_html=True)

    # ── EKSİK KONTROL ──
    with sub[3]:
        styled_section("Eksik Asi & Kontrol Uyarilari")
        if not students:
            st.info("Ogrenci verisi yok.")
        else:
            asi_yapilan_set = set(a.get("ogrenci_id","") for a in asi_kayitlari)
            olcum_yapilan_set = set(o.get("ogrenci_id","") for o in olcum_kayitlari)

            eksik_asi = [s for s in students if s.get("id","") not in asi_yapilan_set]
            eksik_olcum = [s for s in students if s.get("id","") not in olcum_yapilan_set]

            if eksik_asi:
                st.warning(f"{len(eksik_asi)} ogrencinin asi kaydi yok!")
                for s in eksik_asi[:15]:
                    st.markdown(f"  - ⚠️ {s.get('ad','')} {s.get('soyad','')} ({s.get('sinif','')}/{s.get('sube','')})")

            if eksik_olcum:
                st.warning(f"{len(eksik_olcum)} ogrencinin saglik olcumu yok!")
                for s in eksik_olcum[:15]:
                    st.markdown(f"  - 📏 {s.get('ad','')} {s.get('soyad','')} ({s.get('sinif','')}/{s.get('sube','')})")

            if not eksik_asi and not eksik_olcum:
                st.success("Tum ogrencilerin asi ve olcum kaydi mevcut!")

    # ── BMI ANALİZ ──
    with sub[4]:
        styled_section("BMI Analizi")
        if not olcum_kayitlari:
            st.info("Olcum verisi yok.")
        else:
            bmi_grp = Counter(o.get("bmi_durum","?") for o in olcum_kayitlari)
            bmi_renk_map = {"Zayif": "#3b82f6", "Normal": "#10b981", "Kilolu": "#f59e0b", "Obez": "#ef4444"}
            toplam = max(len(olcum_kayitlari), 1)

            for durum, sayi in bmi_grp.most_common():
                pct = round(sayi / toplam * 100)
                renk = bmi_renk_map.get(durum, "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="min-width:60px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{durum}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi} (%{pct})</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Risk listesi
            riskli = [o for o in olcum_kayitlari if o.get("bmi_durum") in ("Obez", "Zayif")]
            if riskli:
                styled_section("Riskli Ogrenciler (Obez/Zayif)")
                for o in riskli[:15]:
                    renk = "#ef4444" if o.get("bmi_durum") == "Obez" else "#3b82f6"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:5px 10px;margin:2px 0;
                        background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;">{o.get('ogrenci_ad','')}</span>
                        <span style="color:#94a3b8;font-size:0.7rem;">BMI: {o.get('bmi','?')}</span>
                        <span style="color:{renk};font-size:0.65rem;font-weight:700;">{o.get('bmi_durum','')}</span>
                    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. ÖĞRENCİ SAĞLIK RİSK PROFİLİ & AI ERKEN UYARI
# ════════════════════════════════════════════════════════════

_RISK_KATEGORILERI = {
    "Revir Sikligi": {"ikon": "🏥", "renk": "#ef4444", "agirlik": 25},
    "Kronik Hastalik": {"ikon": "💊", "renk": "#8b5cf6", "agirlik": 20},
    "Kaza Gecmisi": {"ikon": "🚑", "renk": "#f59e0b", "agirlik": 20},
    "BMI Risk": {"ikon": "📏", "renk": "#3b82f6", "agirlik": 15},
    "Bulasici Hastalik": {"ikon": "🦠", "renk": "#dc2626", "agirlik": 20},
}


def render_saglik_risk_profili(store):
    """Öğrenci Sağlık Risk Profili & AI Erken Uyarı."""
    styled_section("Ogrenci Saglik Risk Profili & AI Erken Uyari", "#dc2626")
    styled_info_banner(
        "Revir ziyaret sikligi, kronik hastalik, alerji, kaza gecmisi "
        "ve bulasici hastalik verilerinden ogrenci bazli saglik risk skoru.",
        banner_type="warning", icon="🧠")

    # Veri topla
    students = load_shared_students()
    saglik_kartlari = []
    revir_ziyaretleri = []
    kaza_olaylari = []
    try:
        saglik_kartlari = store.load_objects("saglik_kartlari")
    except Exception:
        pass
    try:
        revir_ziyaretleri = store.load_objects("revir_ziyaretleri")
    except Exception:
        pass
    try:
        kaza_olaylari = store.load_objects("kaza_olaylari")
    except Exception:
        pass

    salgin_vakalari = _lj("salgin_vakalari.json")
    olcum_kayitlari = _lj("saglik_olcumleri.json")

    bir_ay = (date.today() - timedelta(days=30)).isoformat()

    sub = st.tabs(["🎯 Bireysel Risk", "🗺️ Sinif Risk Haritasi", "📈 Mevsimsel Trend", "🚨 AI Uyarilar"])

    # ── BİREYSEL RİSK ──
    with sub[0]:
        styled_section("Ogrenci Saglik Risk Analizi")
        ogr = _ogr_sec("sr_ogr")
        if ogr:
            ogr_id = ogr.get("id", "")
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            # Revir sikligi
            revir_sayi = sum(1 for r in revir_ziyaretleri
                             if getattr(r, 'ogrenci_id', getattr(r, 'student_id', '')) == ogr_id)
            revir_son_ay = sum(1 for r in revir_ziyaretleri
                               if getattr(r, 'ogrenci_id', getattr(r, 'student_id', '')) == ogr_id
                               and getattr(r, 'tarih', getattr(r, 'ziyaret_tarihi', ''))[:10] >= bir_ay)

            # Kaza
            kaza_sayi = sum(1 for k in kaza_olaylari
                            if getattr(k, 'ogrenci_id', getattr(k, 'student_id', '')) == ogr_id)

            # Kronik/alerji
            kart = next((k for k in saglik_kartlari
                         if getattr(k, 'ogrenci_id', getattr(k, 'student_id', '')) == ogr_id), None)
            kronik = bool(kart and (getattr(kart, 'kronik_hastaliklar', '') or getattr(kart, 'chronic_conditions', '')))
            alerji = bool(kart and (getattr(kart, 'alerjiler', '') or getattr(kart, 'allergies', '')))

            # BMI
            olcum = next((o for o in sorted(olcum_kayitlari, key=lambda x: x.get("tarih",""), reverse=True)
                          if o.get("ogrenci_id") == ogr_id), None)
            bmi_risk = olcum and olcum.get("bmi_durum") in ("Obez", "Zayif") if olcum else False

            # Bulasici
            salgin_sayi = sum(1 for v in salgin_vakalari if v.get("ogrenci_id") == ogr_id)

            # Risk skoru
            skor = 0
            skor += min(40, revir_son_ay * 10)  # Revir sikligi
            skor += 15 if kronik else 0
            skor += min(20, kaza_sayi * 7)
            skor += 10 if bmi_risk else 0
            skor += min(15, salgin_sayi * 8)
            skor = min(100, skor)

            risk_renk = "#dc2626" if skor >= 60 else "#ef4444" if skor >= 40 else "#f59e0b" if skor >= 20 else "#10b981"
            risk_label = "Kritik" if skor >= 60 else "Yuksek" if skor >= 40 else "Orta" if skor >= 20 else "Dusuk"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,{risk_renk}15);border:2px solid {risk_renk};
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                <div style="color:{risk_renk};font-weight:900;font-size:2.5rem;margin-top:8px;">{skor}/100</div>
                <div style="color:{risk_renk};font-weight:700;font-size:0.9rem;">{risk_label} Saglik Riski</div>
                <div style="display:flex;justify-content:center;gap:16px;margin-top:10px;color:#94a3b8;font-size:0.72rem;">
                    <span>Revir: {revir_sayi} ({revir_son_ay} son ay)</span>
                    <span>Kaza: {kaza_sayi}</span>
                    <span>Kronik: {'Var' if kronik else 'Yok'}</span>
                    <span>BMI Risk: {'Var' if bmi_risk else 'Yok'}</span>
                </div>
            </div>""", unsafe_allow_html=True)

            if skor >= 40:
                st.warning("Bu ogrenci icin detayli saglik degerlendirmesi onerilir.")
            if revir_son_ay >= 3:
                st.error(f"Son 1 ayda {revir_son_ay} revir ziyareti — altta yatan sorun olabilir!")

    # ── SINIF RİSK HARİTASI ──
    with sub[1]:
        styled_section("Sinif Bazli Saglik Risk Haritasi")
        if not students:
            st.info("Ogrenci yok.")
        else:
            sinif_risk = defaultdict(list)
            for s in students[:80]:
                sid = s.get("id", "")
                sinif_sube = f"{s.get('sinif','')}/{s.get('sube','')}"
                revir = sum(1 for r in revir_ziyaretleri
                            if getattr(r, 'ogrenci_id', getattr(r, 'student_id', '')) == sid)
                sinif_risk[sinif_sube].append(revir)

            for sinif in sorted(sinif_risk.keys()):
                revir_list = sinif_risk[sinif]
                toplam_revir = sum(revir_list)
                ort = round(toplam_revir / max(len(revir_list), 1), 1)
                renk = "#ef4444" if ort >= 3 else "#f59e0b" if ort >= 1.5 else "#10b981"
                pct = min(100, round(ort * 15))

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:5px 0;">
                    <span style="min-width:45px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{sinif}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:800;">Ort: {ort}</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(revir_list)} ogr | {toplam_revir} revir</span>
                </div>""", unsafe_allow_html=True)

    # ── MEVSIMSEL TREND ──
    with sub[2]:
        styled_section("Mevsimsel Revir Ziyaret Trendi")
        ay_grp = Counter()
        for r in revir_ziyaretleri:
            tarih = getattr(r, 'tarih', getattr(r, 'ziyaret_tarihi', ''))
            if tarih:
                ay = tarih[:7]
                ay_grp[ay] += 1

        if ay_grp:
            max_val = max(ay_grp.values())
            for ay in sorted(ay_grp.keys())[-12:]:
                sayi = ay_grp[ay]
                pct = round(sayi / max(max_val, 1) * 100)
                renk = "#ef4444" if sayi >= 20 else "#f59e0b" if sayi >= 10 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                    <span style="min-width:55px;font-size:0.72rem;color:#94a3b8;">{ay}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Revir verisi yok.")

    # ── AI UYARILAR ──
    with sub[3]:
        styled_section("AI Saglik Uyarilari")

        uyarilar = []
        # Sik revir gelen
        ogr_revir = Counter()
        for r in revir_ziyaretleri:
            oid = getattr(r, 'ogrenci_id', getattr(r, 'student_id', ''))
            tarih = getattr(r, 'tarih', getattr(r, 'ziyaret_tarihi', ''))
            if oid and tarih and tarih[:10] >= bir_ay:
                ogr_revir[oid] += 1

        for oid, sayi in ogr_revir.most_common():
            if sayi >= 3:
                ogr = next((s for s in students if s.get("id") == oid), None)
                if ogr:
                    uyarilar.append({
                        "tip": "Sik Revir",
                        "mesaj": f"{ogr.get('ad','')} {ogr.get('soyad','')} son 1 ayda {sayi} kez revire geldi",
                        "renk": "#ef4444",
                        "ikon": "🏥",
                    })

        # Salgin uyarisi
        aktif_salgin = sum(1 for v in salgin_vakalari if v.get("durum") == "Aktif")
        if aktif_salgin >= 3:
            uyarilar.append({
                "tip": "Salgin Riski",
                "mesaj": f"{aktif_salgin} aktif bulasici hastalik vakasi — salgin riski!",
                "renk": "#dc2626",
                "ikon": "🦠",
            })

        # BMI uyarisi
        obez = sum(1 for o in olcum_kayitlari if o.get("bmi_durum") == "Obez")
        if obez >= 5:
            uyarilar.append({
                "tip": "Obezite Uyarisi",
                "mesaj": f"{obez} ogrenci obez kategorisinde — beslenme programi onerilir",
                "renk": "#f59e0b",
                "ikon": "📏",
            })

        if not uyarilar:
            st.success("Su anda AI uyarisi yok — saglik durumlari iyi!")
        else:
            for u in uyarilar:
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {u['renk']}30;border-left:5px solid {u['renk']};
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:6px 0;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="font-size:1.1rem;">{u['ikon']}</span>
                        <span style="color:{u['renk']};font-weight:800;font-size:0.8rem;">{u['tip']}</span>
                    </div>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:4px;padding-left:28px;">{u['mesaj']}</div>
                </div>""", unsafe_allow_html=True)
