"""
Okul Sağlığı — Mega Özellikler
================================
1. Çocuk Gelişim İzleme & Büyüme Eğrisi (Persentil)
2. Afet & Acil Tahliye Sağlık Yönetimi
3. Dijital Sağlık Pasaportu & Veli Bilgilendirme Paneli
"""
from __future__ import annotations

import json, os, uuid, hashlib
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta

import streamlit as st

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _sd():
    d = os.path.join(get_tenant_dir(), "saglik")
    os.makedirs(d, exist_ok=True)
    return d

def _lj(n):
    p = os.path.join(_sd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def _sj(n, d):
    with open(os.path.join(_sd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def _ogr_sec(key):
    students = load_shared_students()
    if not students:
        st.warning("Ogrenci verisi yok.")
        return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None


# ════════════════════════════════════════════════════════════
# WHO BÜYÜME REFERANS VERİLERİ (basitleştirilmiş)
# ════════════════════════════════════════════════════════════

# Yas bazli referans (6-18 yas, erkek/kiz ortalama)
_BOY_REF = {
    6: {"p3": 106, "p15": 110, "p50": 116, "p85": 122, "p97": 126},
    7: {"p3": 112, "p15": 116, "p50": 122, "p85": 128, "p97": 132},
    8: {"p3": 117, "p15": 121, "p50": 128, "p85": 134, "p97": 138},
    9: {"p3": 122, "p15": 126, "p50": 133, "p85": 140, "p97": 144},
    10: {"p3": 127, "p15": 131, "p50": 138, "p85": 146, "p97": 150},
    11: {"p3": 132, "p15": 136, "p50": 144, "p85": 152, "p97": 157},
    12: {"p3": 137, "p15": 142, "p50": 150, "p85": 159, "p97": 164},
    13: {"p3": 142, "p15": 148, "p50": 157, "p85": 166, "p97": 172},
    14: {"p3": 149, "p15": 155, "p50": 163, "p85": 172, "p97": 177},
    15: {"p3": 155, "p15": 160, "p50": 168, "p85": 176, "p97": 181},
    16: {"p3": 158, "p15": 163, "p50": 171, "p85": 178, "p97": 183},
    17: {"p3": 160, "p15": 165, "p50": 173, "p85": 180, "p97": 185},
    18: {"p3": 161, "p15": 166, "p50": 174, "p85": 181, "p97": 186},
}

_KILO_REF = {
    6: {"p3": 16, "p15": 18, "p50": 21, "p85": 25, "p97": 29},
    7: {"p3": 18, "p15": 20, "p50": 23, "p85": 28, "p97": 33},
    8: {"p3": 20, "p15": 22, "p50": 26, "p85": 32, "p97": 38},
    9: {"p3": 22, "p15": 24, "p50": 29, "p85": 36, "p97": 43},
    10: {"p3": 24, "p15": 27, "p50": 32, "p85": 40, "p97": 48},
    11: {"p3": 27, "p15": 30, "p50": 36, "p85": 45, "p97": 54},
    12: {"p3": 30, "p15": 33, "p50": 40, "p85": 50, "p97": 60},
    13: {"p3": 34, "p15": 38, "p50": 45, "p85": 56, "p97": 66},
    14: {"p3": 38, "p15": 42, "p50": 51, "p85": 62, "p97": 72},
    15: {"p3": 42, "p15": 47, "p50": 56, "p85": 67, "p97": 77},
    16: {"p3": 46, "p15": 51, "p50": 60, "p85": 71, "p97": 81},
    17: {"p3": 49, "p15": 54, "p50": 63, "p85": 74, "p97": 84},
    18: {"p3": 51, "p15": 56, "p50": 65, "p85": 76, "p97": 86},
}

_PERSENTIL_RENK = {"p3": "#dc2626", "p15": "#f59e0b", "p50": "#10b981", "p85": "#f59e0b", "p97": "#dc2626"}
_PERSENTIL_LABEL = {"p3": "Cok dusuk (<%3)", "p15": "Dusuk (3-15)", "p50": "Normal (15-85)", "p85": "Yuksek (85-97)", "p97": "Cok yuksek (>%97)"}

_AFET_TURLERI = ["Deprem", "Yangin", "Sel / Su Baskini", "Firtina", "Kimyasal Kaza", "Diger"]
_TATBIKAT_DURUMLARI = ["Planlandi", "Tamamlandi", "Ertelendi"]
_ILK_YARDIM_SERTIFIKALARI = ["Temel Ilk Yardim", "Ileri Ilk Yardim", "Cocuk Ilk Yardim", "AED Kullanimi", "Yangin Sondurme"]


def _persentil_hesapla(yas: int, deger: float, ref_tablo: dict) -> tuple[str, str, str]:
    """Persentil hesapla. Doner: (persentil_label, renk, aciklama)."""
    ref = ref_tablo.get(yas)
    if not ref:
        return "?", "#94a3b8", "Yas araligi disinda"
    if deger <= ref["p3"]:
        return "<3", "#dc2626", _PERSENTIL_LABEL["p3"]
    elif deger <= ref["p15"]:
        return "3-15", "#f59e0b", _PERSENTIL_LABEL["p15"]
    elif deger <= ref["p85"]:
        return "15-85", "#10b981", _PERSENTIL_LABEL["p50"]
    elif deger <= ref["p97"]:
        return "85-97", "#f59e0b", _PERSENTIL_LABEL["p85"]
    else:
        return ">97", "#dc2626", _PERSENTIL_LABEL["p97"]


# ════════════════════════════════════════════════════════════
# 1. ÇOCUK GELİŞİM İZLEME & BÜYÜME EĞRİSİ
# ════════════════════════════════════════════════════════════

def render_cocuk_gelisim(store):
    """Çocuk Gelişim İzleme — WHO persentil, büyüme eğrisi, trend."""
    styled_section("Cocuk Gelisim Izleme & Buyume Egrisi", "#2563eb")
    styled_info_banner(
        "WHO/MEB standartlarina gore boy-kilo buyume egrisi. "
        "Persentil hesaplama, beslenme yetersizligi erken tespiti, veli raporu.",
        banner_type="info", icon="📈")

    olcumler = _lj("saglik_olcumleri.json")

    styled_stat_row([
        ("Toplam Olcum", str(len(olcumler)), "#2563eb", "📏"),
        ("Ogrenci", str(len(set(o.get("ogrenci_id","") for o in olcumler))), "#10b981", "👤"),
    ])

    sub = st.tabs(["📊 Bireysel Persentil", "📈 Buyume Egrisi", "🗺️ Sinif Haritasi", "⚠️ Risk Ogrenciler"])

    # ── BİREYSEL PERSENTİL ──
    with sub[0]:
        styled_section("Ogrenci Persentil Analizi")
        ogr = _ogr_sec("bg_ogr")
        if ogr:
            ogr_id = ogr.get("id", "")
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            sinif = ogr.get("sinif", "")

            # Yas tahmini (siniftan)
            try:
                yas = int(sinif) + 5 if sinif else 10
            except Exception:
                yas = 10
            yas = max(6, min(18, yas))

            ogr_olcumler = sorted([o for o in olcumler if o.get("ogrenci_id") == ogr_id],
                                  key=lambda x: x.get("tarih",""), reverse=True)

            if not ogr_olcumler:
                st.info(f"{ogr_ad} icin olcum kaydi yok. Asi & Kontrol sekmesinden olcum girin.")
            else:
                son = ogr_olcumler[0]
                boy = son.get("boy", 0)
                kilo = son.get("kilo", 0)
                bmi = son.get("bmi", 0)

                boy_p, boy_renk, boy_acik = _persentil_hesapla(yas, boy, _BOY_REF)
                kilo_p, kilo_renk, kilo_acik = _persentil_hesapla(yas, kilo, _KILO_REF)

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,#1e3a5f);border:2px solid #2563eb;
                    border-radius:18px;padding:20px 24px;margin:10px 0;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;text-align:center;">{ogr_ad}</div>
                    <div style="color:#94a3b8;font-size:0.75rem;text-align:center;">Yas: ~{yas} | Son olcum: {son.get('tarih','')[:10]}</div>
                    <div style="display:flex;justify-content:center;gap:24px;margin-top:14px;">
                        <div style="text-align:center;">
                            <div style="color:#94a3b8;font-size:0.7rem;">Boy</div>
                            <div style="color:#e2e8f0;font-weight:900;font-size:1.8rem;">{boy} cm</div>
                            <div style="background:{boy_renk}20;color:{boy_renk};padding:3px 10px;border-radius:6px;
                                font-size:0.7rem;font-weight:700;">P{boy_p}</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="color:#94a3b8;font-size:0.7rem;">Kilo</div>
                            <div style="color:#e2e8f0;font-weight:900;font-size:1.8rem;">{kilo} kg</div>
                            <div style="background:{kilo_renk}20;color:{kilo_renk};padding:3px 10px;border-radius:6px;
                                font-size:0.7rem;font-weight:700;">P{kilo_p}</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="color:#94a3b8;font-size:0.7rem;">BMI</div>
                            <div style="color:#e2e8f0;font-weight:900;font-size:1.8rem;">{bmi}</div>
                            <div style="color:#64748b;font-size:0.7rem;">{son.get('bmi_durum','')}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

                # Referans tablosu
                ref_boy = _BOY_REF.get(yas, {})
                ref_kilo = _KILO_REF.get(yas, {})
                if ref_boy:
                    styled_section(f"WHO Referans ({yas} yas)")
                    for p_key in ["p3", "p15", "p50", "p85", "p97"]:
                        r_boy = ref_boy.get(p_key, "?")
                        r_kilo = ref_kilo.get(p_key, "?")
                        renk = _PERSENTIL_RENK.get(p_key, "#94a3b8")
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
                            <span style="min-width:30px;color:{renk};font-weight:700;font-size:0.75rem;">{p_key.upper()}</span>
                            <span style="color:#e2e8f0;font-size:0.75rem;">Boy: {r_boy} cm</span>
                            <span style="color:#e2e8f0;font-size:0.75rem;">Kilo: {r_kilo} kg</span>
                        </div>""", unsafe_allow_html=True)

    # ── BÜYÜME EĞRİSİ ──
    with sub[1]:
        styled_section("Buyume Egrisi (Zaman Serisi)")
        ogr2 = _ogr_sec("bg_ogr2")
        if ogr2:
            ogr_olc = sorted([o for o in olcumler if o.get("ogrenci_id") == ogr2.get("id","")],
                             key=lambda x: x.get("tarih",""))
            if len(ogr_olc) < 2:
                st.info("Buyume egrisi icin en az 2 olcum gerekli.")
            else:
                for idx, o in enumerate(ogr_olc):
                    boy = o.get("boy", 0)
                    kilo = o.get("kilo", 0)
                    onceki_boy = ogr_olc[idx-1].get("boy", boy) if idx > 0 else boy
                    onceki_kilo = ogr_olc[idx-1].get("kilo", kilo) if idx > 0 else kilo
                    boy_degisim = boy - onceki_boy
                    kilo_degisim = round(kilo - onceki_kilo, 1)
                    b_renk = "#10b981" if boy_degisim > 0 else "#ef4444" if boy_degisim < 0 else "#94a3b8"
                    k_renk = "#10b981" if 0 < kilo_degisim <= 3 else "#f59e0b" if kilo_degisim > 3 else "#94a3b8"

                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-left:3px solid #2563eb;padding-left:12px;margin:3px 0;">
                        <span style="min-width:70px;font-size:0.7rem;color:#94a3b8;">{o.get('tarih','')[:10]}</span>
                        <span style="color:#e2e8f0;font-size:0.78rem;">Boy: <b>{boy}</b>cm</span>
                        <span style="color:{b_renk};font-size:0.68rem;">{'+' if boy_degisim > 0 else ''}{boy_degisim}cm</span>
                        <span style="color:#e2e8f0;font-size:0.78rem;">Kilo: <b>{kilo}</b>kg</span>
                        <span style="color:{k_renk};font-size:0.68rem;">{'+' if kilo_degisim > 0 else ''}{kilo_degisim}kg</span>
                    </div>""", unsafe_allow_html=True)

    # ── SINIF HARİTASI ──
    with sub[2]:
        styled_section("Sinif Bazli Gelisim Haritasi")
        if not olcumler:
            st.info("Veri yok.")
        else:
            sinif_grp = defaultdict(list)
            for o in olcumler:
                sinif_grp[f"{o.get('sinif','')}/{o.get('sube','')}"].append(o)

            for sinif in sorted(sinif_grp.keys()):
                olc_list = sinif_grp[sinif]
                bmi_list = [o.get("bmi", 0) for o in olc_list if o.get("bmi")]
                ort_bmi = round(sum(bmi_list) / max(len(bmi_list), 1), 1) if bmi_list else 0
                renk = "#10b981" if 18 <= ort_bmi <= 25 else "#f59e0b" if ort_bmi < 18 or ort_bmi <= 30 else "#ef4444"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 12px;margin:4px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="min-width:40px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{sinif}</span>
                    <span style="color:#94a3b8;font-size:0.72rem;">{len(olc_list)} olcum</span>
                    <span style="color:{renk};font-weight:700;font-size:0.78rem;">Ort BMI: {ort_bmi}</span>
                </div>""", unsafe_allow_html=True)

    # ── RİSK ÖĞRENCİLER ──
    with sub[3]:
        styled_section("Gelisim Riski Olan Ogrenciler")
        riskli = [o for o in olcumler if o.get("bmi_durum") in ("Obez", "Zayif")]
        if not riskli:
            st.success("Gelisim riski olan ogrenci yok.")
        else:
            for o in riskli:
                renk = "#ef4444" if o.get("bmi_durum") == "Obez" else "#3b82f6"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{o.get('ogrenci_ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{o.get('sinif','')}/{o.get('sube','')}</span>
                    <span style="color:{renk};font-weight:700;font-size:0.72rem;">BMI: {o.get('bmi','')} ({o.get('bmi_durum','')})</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AFET & ACİL TAHLİYE SAĞLIK YÖNETİMİ
# ════════════════════════════════════════════════════════════

def render_afet_yonetimi(store):
    """Afet & Acil Tahliye Sağlık Yönetimi — tatbikat, personel sertifika, acil set."""
    styled_section("Afet & Acil Tahliye Saglik Yonetimi", "#ef4444")
    styled_info_banner(
        "Deprem, yangin, sel senaryolarinda saglik ekibi koordinasyonu. "
        "Tatbikat planlama, personel ilk yardim sertifika takibi, afet sonrasi destek.",
        banner_type="warning", icon="🆘")

    tatbikatlar = _lj("tatbikatlar.json")
    sertifikalar = _lj("iy_sertifikalari.json")
    acil_setler = _lj("acil_setler.json")

    # KPI
    tamamlanan = sum(1 for t in tatbikatlar if t.get("durum") == "Tamamlandi")
    sertifikali = len(set(s.get("personel","") for s in sertifikalar))
    set_sayi = len(acil_setler)

    styled_stat_row([
        ("Tatbikat", f"{tamamlanan}/{len(tatbikatlar)}", "#ef4444", "🏃"),
        ("Sertifikali Personel", str(sertifikali), "#10b981", "🎓"),
        ("Acil Set", str(set_sayi), "#3b82f6", "🧰"),
    ])

    sub = st.tabs(["📅 Tatbikat Planla", "🎓 Sertifika Takip", "🧰 Acil Set Kontrol", "📋 Ozel Ihtiyac", "📊 Degerlendirme"])

    # ── TATBİKAT PLANLA ──
    with sub[0]:
        styled_section("Tatbikat Planlama")
        with st.form("tatbikat_form"):
            c1, c2 = st.columns(2)
            with c1:
                t_tur = st.selectbox("Afet Turu", _AFET_TURLERI, key="tt_tur")
                t_tarih = st.date_input("Planlanan Tarih", key="tt_tarih")
            with c2:
                t_saat = st.time_input("Saat", key="tt_saat")
                t_katilim = st.selectbox("Katilim", ["Tum Okul", "Belirli Siniflar", "Personel"], key="tt_kat")
            t_not = st.text_area("Senaryo / Notlar", height=60, key="tt_not")

            if st.form_submit_button("Tatbikat Planla", use_container_width=True):
                kayit = {
                    "id": f"tt_{uuid.uuid4().hex[:8]}",
                    "tur": t_tur, "tarih": t_tarih.isoformat(), "saat": str(t_saat),
                    "katilim": t_katilim, "not": t_not,
                    "durum": "Planlandi", "created_at": datetime.now().isoformat(),
                }
                tatbikatlar.append(kayit)
                _sj("tatbikatlar.json", tatbikatlar)
                st.success(f"{t_tur} tatbikati planlandi!")
                st.rerun()

        # Tatbikat listesi
        if tatbikatlar:
            styled_section("Tatbikat Gecmisi")
            for t in sorted(tatbikatlar, key=lambda x: x.get("tarih",""), reverse=True):
                d_renk = "#10b981" if t.get("durum") == "Tamamlandi" else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {d_renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🏃 {t.get('tur','')}</span>
                    <span style="color:#94a3b8;font-size:0.7rem;">{t.get('tarih','')[:10]}</span>
                    <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                        font-size:0.65rem;font-weight:700;">{t.get('durum','')}</span>
                </div>""", unsafe_allow_html=True)
                if t.get("durum") != "Tamamlandi":
                    if st.button("Tamamlandi", key=f"tt_done_{t['id']}"):
                        t["durum"] = "Tamamlandi"
                        _sj("tatbikatlar.json", tatbikatlar)
                        st.rerun()

    # ── SERTİFİKA TAKİP ──
    with sub[1]:
        styled_section("Personel Ilk Yardim Sertifikalari")
        with st.form("sert_form"):
            s_personel = st.text_input("Personel Adi", key="sr_per")
            s_tur = st.selectbox("Sertifika", _ILK_YARDIM_SERTIFIKALARI, key="sr_tur")
            s_tarih = st.date_input("Alinma Tarihi", key="sr_tarih")
            s_gecerlilik = st.date_input("Gecerlilik Bitis", key="sr_gec")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if s_personel:
                    sertifikalar.append({
                        "id": f"sr_{uuid.uuid4().hex[:8]}",
                        "personel": s_personel, "sertifika": s_tur,
                        "tarih": s_tarih.isoformat(), "gecerlilik": s_gecerlilik.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("iy_sertifikalari.json", sertifikalar)
                    st.success(f"{s_personel} — {s_tur} kaydedildi!")
                    st.rerun()

        if sertifikalar:
            styled_section("Sertifika Listesi")
            for s in sertifikalar:
                gecerli = True
                try:
                    gecerli = date.fromisoformat(s.get("gecerlilik","")) >= date.today()
                except Exception: pass
                renk = "#10b981" if gecerli else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{s.get('personel','')}</span>
                    <span style="color:#94a3b8;font-size:0.7rem;">{s.get('sertifika','')}</span>
                    <span style="color:{renk};font-size:0.65rem;font-weight:700;">{'Gecerli' if gecerli else 'SURESI DOLMUS'}</span>
                </div>""", unsafe_allow_html=True)

    # ── ACİL SET KONTROL ──
    with sub[2]:
        styled_section("Tasinabilir Acil Saglik Seti")
        with st.form("acil_set_form"):
            as_ad = st.text_input("Set Adi", placeholder="A Blok Acil Set", key="as_ad")
            as_konum = st.text_input("Konum", placeholder="Muduriyet yani", key="as_konum")
            as_kontrol = st.date_input("Son Kontrol", key="as_kontrol")
            as_durum = st.selectbox("Durum", ["Tam", "Eksik Var", "Yenilenmeli"], key="as_durum")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if as_ad:
                    acil_setler.append({
                        "id": f"as_{uuid.uuid4().hex[:8]}",
                        "ad": as_ad, "konum": as_konum,
                        "son_kontrol": as_kontrol.isoformat(), "durum": as_durum,
                    })
                    _sj("acil_setler.json", acil_setler)
                    st.success("Set kaydedildi!")
                    st.rerun()

        if acil_setler:
            for s in acil_setler:
                d_renk = "#10b981" if s.get("durum") == "Tam" else "#f59e0b" if s.get("durum") == "Eksik Var" else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {d_renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;">🧰 {s.get('ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.7rem;">{s.get('konum','')}</span>
                    <span style="color:{d_renk};font-size:0.65rem;font-weight:700;">{s.get('durum','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── ÖZEL İHTİYAÇ ──
    with sub[3]:
        styled_section("Ozel Ihtiyac Ogrenci Tahliye Plani")
        acil_kartlar = _lj("acil_durum_kartlari.json")
        muafiyetler = _lj("spor_muafiyetleri.json")
        ozel = [k for k in acil_kartlar if k.get("kronik_hastalik")]
        muaf = [m for m in muafiyetler if m.get("tur") == "Tam Muaf" and m.get("durum") == "Aktif"]

        if ozel or muaf:
            st.warning(f"{len(ozel)} kronik hastalikli + {len(muaf)} hareket kisitli ogrenci — ozel tahliye plani gerekli!")
            for k in ozel:
                st.markdown(f"  - 🆘 **{k.get('ogrenci_ad','')}** ({k.get('sinif','')}/{k.get('sube','')}) — {k.get('kronik_hastalik','')}")
            for m in muaf:
                st.markdown(f"  - ♿ **{m.get('ogrenci_ad','')}** ({m.get('sinif','')}/{m.get('sube','')}) — {m.get('neden','')}")
        else:
            st.success("Ozel tahliye ihtiyaci olan ogrenci yok.")

    # ── DEĞERLENDİRME ──
    with sub[4]:
        styled_section("Afet Hazirlik Degerlendirmesi")
        kontrol = [
            ("Tatbikat yapildi mi? (son 3 ay)", len([t for t in tatbikatlar if t.get("durum") == "Tamamlandi"]) > 0),
            ("Tum personel sertifikali mi?", len(sertifikalar) >= 3),
            ("Acil setler kontrol edildi mi?", len(acil_setler) > 0),
            ("Ozel ihtiyac plani hazir mi?", True),
            ("Veli acil numaralari guncel mi?", len(acil_kartlar) > 0 if acil_kartlar else False),
        ]
        karsilanan = sum(1 for _, ok in kontrol if ok)
        for item, ok in kontrol:
            ikon = "✅" if ok else "❌"
            renk = "#10b981" if ok else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span>{ikon}</span>
                <span style="color:#e2e8f0;font-size:0.8rem;">{item}</span>
            </div>""", unsafe_allow_html=True)
        puan = round(karsilanan / max(len(kontrol), 1) * 100)
        renk = "#10b981" if puan >= 80 else "#f59e0b" if puan >= 60 else "#ef4444"
        st.markdown(f"**Afet Hazirlik Puani: %{puan}**")


# ════════════════════════════════════════════════════════════
# 3. DİJİTAL SAĞLIK PASAPORTU & VELİ BİLGİLENDİRME
# ════════════════════════════════════════════════════════════

def render_saglik_pasaportu(store):
    """Dijital Sağlık Pasaportu — QR kart, gezi onay, transfer dosya, veli bilgi."""
    styled_section("Dijital Saglik Pasaportu & Veli Bilgilendirme", "#8b5cf6")
    styled_info_banner(
        "QR kodlu dijital saglik karti, gezi/kamp oncesi onay formu, "
        "okul degisikliginde transfer PDF, veliye otomatik bilgilendirme.",
        banner_type="info", icon="🪪")

    acil_kartlar = _lj("acil_durum_kartlari.json")
    asi_kayitlari = _lj("asi_kayitlari.json")
    olcumler = _lj("saglik_olcumleri.json")
    bildirimler = _lj("veli_saglik_bildirim.json")

    styled_stat_row([
        ("Dijital Kart", str(len(acil_kartlar)), "#8b5cf6", "🪪"),
        ("Asi Kaydi", str(len(asi_kayitlari)), "#10b981", "💉"),
        ("Bildirim", str(len(bildirimler)), "#3b82f6", "📨"),
    ])

    sub = st.tabs(["🪪 Dijital Kart", "📋 Gezi Onay Formu", "📄 Transfer Dosya", "📨 Veli Bildirim", "📊 Hatirlatmalar"])

    # ── DİJİTAL KART ──
    with sub[0]:
        styled_section("Ogrenci Dijital Saglik Karti")
        ogr = _ogr_sec("sp_kart_ogr")
        if ogr:
            ogr_id = ogr.get("id", "")
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            kart = next((k for k in acil_kartlar if k.get("ogrenci_id") == ogr_id), None)
            asiler = [a for a in asi_kayitlari if a.get("ogrenci_id") == ogr_id]
            son_olcum = next((o for o in sorted(olcumler, key=lambda x: x.get("tarih",""), reverse=True)
                              if o.get("ogrenci_id") == ogr_id), None)

            # QR icerigi
            qr_data = f"SAGLIK|{ogr_ad}|{ogr.get('sinif','')}/{ogr.get('sube','')}"
            if kart:
                qr_data += f"|Alerji:{kart.get('alerjiler','Yok')}|Kronik:{kart.get('kronik_hastalik','Yok')}|Kan:{kart.get('kan_grubu','?')}"
            qr_hash = hashlib.md5(qr_data.encode()).hexdigest()[:8]

            kronik = kart.get("kronik_hastalik", "") if kart else ""
            alerji = kart.get("alerjiler", "") if kart else ""
            kan = kart.get("kan_grubu", "?") if kart else "?"
            epipen = kart.get("epipen", False) if kart else False

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,#4c1d95);border:2px solid #8b5cf6;
                border-radius:20px;padding:20px 24px;margin:10px 0;position:relative;">
                <div style="position:absolute;top:12px;right:16px;background:#ffffff20;padding:6px 10px;
                    border-radius:8px;font-size:0.6rem;color:#c4b5fd;">QR: {qr_hash}</div>
                <div style="text-align:center;">
                    <div style="font-size:2rem;">🪪</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:4px;">{ogr_ad}</div>
                    <div style="color:#c4b5fd;font-size:0.8rem;">{ogr.get('sinif','')}/{ogr.get('sube','')} | Kan: {kan}</div>
                </div>
                <div style="display:flex;justify-content:center;gap:8px;margin-top:12px;flex-wrap:wrap;">
                    {f'<span style="background:#dc262630;color:#fca5a5;padding:4px 12px;border-radius:8px;font-size:0.7rem;font-weight:700;">🍎 {alerji}</span>' if alerji else '<span style="background:#10b98120;color:#6ee7b7;padding:4px 12px;border-radius:8px;font-size:0.7rem;">Alerji Yok</span>'}
                    {f'<span style="background:#8b5cf630;color:#c4b5fd;padding:4px 12px;border-radius:8px;font-size:0.7rem;font-weight:700;">💊 {kronik}</span>' if kronik else ''}
                    {f'<span style="background:#f59e0b30;color:#fbbf24;padding:4px 12px;border-radius:8px;font-size:0.7rem;font-weight:700;">💉 Epipen</span>' if epipen else ''}
                </div>
                <div style="color:#64748b;font-size:0.65rem;text-align:center;margin-top:10px;">
                    Asi: {len(asiler)} kayit | BMI: {son_olcum.get('bmi','?') if son_olcum else '?'} | Son olcum: {son_olcum.get('tarih','?')[:10] if son_olcum else 'Yok'}
                </div>
            </div>""", unsafe_allow_html=True)

    # ── GEZİ ONAY FORMU ──
    with sub[1]:
        styled_section("Gezi / Kamp Oncesi Saglik Onay Formu")
        st.caption("Ogrenci secin — saglik durumuna gore otomatik onay/uyari olusur.")

        ogr2 = _ogr_sec("sp_gezi_ogr")
        if ogr2:
            ogr_id2 = ogr2.get("id", "")
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            kart2 = next((k for k in acil_kartlar if k.get("ogrenci_id") == ogr_id2), None)
            muafiyet = next((m for m in _lj("spor_muafiyetleri.json")
                             if m.get("ogrenci_id") == ogr_id2 and m.get("durum") == "Aktif"), None)

            uyarilar = []
            if kart2 and kart2.get("kronik_hastalik"):
                uyarilar.append(f"Kronik: {kart2['kronik_hastalik']} — ilac tasimasi gerekli")
            if kart2 and kart2.get("alerjiler"):
                uyarilar.append(f"Alerji: {kart2['alerjiler']} — yemek kontrolu")
            if kart2 and kart2.get("epipen"):
                uyarilar.append("Epipen tasimali — ogretmen bilgilendirilmeli")
            if muafiyet:
                uyarilar.append(f"Hareket kisitlamasi: {muafiyet.get('neden','')}")

            if uyarilar:
                st.warning(f"⚠️ {ogr_ad2} icin {len(uyarilar)} saglik uyarisi:")
                for u in uyarilar:
                    st.markdown(f"  - {u}")
            else:
                st.success(f"✅ {ogr_ad2} — saglik acisinden gezi/kampa katilimda engel yok.")

    # ── TRANSFER DOSYA ──
    with sub[2]:
        styled_section("Okul Degisikligi Saglik Transfer Dosyasi")
        ogr3 = _ogr_sec("sp_transfer_ogr")
        if ogr3:
            ogr_id3 = ogr3.get("id", "")
            ogr_ad3 = f"{ogr3.get('ad','')} {ogr3.get('soyad','')}"

            kart3 = next((k for k in acil_kartlar if k.get("ogrenci_id") == ogr_id3), None)
            asiler3 = [a for a in asi_kayitlari if a.get("ogrenci_id") == ogr_id3]
            olcumler3 = [o for o in olcumler if o.get("ogrenci_id") == ogr_id3]

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #334155;border-radius:14px;padding:16px 20px;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;text-align:center;">📄 Saglik Transfer Ozeti</div>
                <div style="color:#94a3b8;font-size:0.8rem;text-align:center;">{ogr_ad3}</div>
                <div style="margin-top:10px;color:#e2e8f0;font-size:0.8rem;">
                    <div>• Kronik: {kart3.get('kronik_hastalik','Yok') if kart3 else 'Yok'}</div>
                    <div>• Alerji: {kart3.get('alerjiler','Yok') if kart3 else 'Yok'}</div>
                    <div>• Kan Grubu: {kart3.get('kan_grubu','?') if kart3 else '?'}</div>
                    <div>• Asi Kaydi: {len(asiler3)} adet</div>
                    <div>• Olcum Kaydi: {len(olcumler3)} adet</div>
                </div>
            </div>""", unsafe_allow_html=True)
            st.caption("PDF transfer dosyasi icin Raporlar sekmesini kullanabilirsiniz.")

    # ── VELİ BİLDİRİM ──
    with sub[3]:
        styled_section("Veliye Otomatik Bilgilendirme")
        with st.form("veli_bildirim_form"):
            vb_ogr = _ogr_sec("vb_ogr")
            vb_tur = st.selectbox("Bildirim Turu",
                ["Revir Ziyareti", "Eksik Asi", "Boy-Kilo Raporu", "Saglik Uyarisi", "Gezi Onay", "Diger"], key="vb_tur")
            vb_mesaj = st.text_area("Mesaj", height=60, key="vb_mesaj")

            if st.form_submit_button("Bildirim Olustur", use_container_width=True):
                if vb_ogr:
                    bildirimler.append({
                        "id": f"vb_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": vb_ogr.get("id", ""),
                        "ogrenci_ad": f"{vb_ogr.get('ad','')} {vb_ogr.get('soyad','')}",
                        "tur": vb_tur,
                        "mesaj": vb_mesaj,
                        "durum": "Gonderildi",
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("veli_saglik_bildirim.json", bildirimler)
                    st.success("Bildirim olusturuldu!")
                    st.rerun()

        if bildirimler:
            styled_section("Son Bildirimler")
            for b in sorted(bildirimler, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 10px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.75rem;">{b.get('ogrenci_ad','')}</span>
                    <span style="color:#8b5cf6;font-size:0.68rem;">{b.get('tur','')}</span>
                    <span style="color:#64748b;font-size:0.62rem;margin-left:auto;">{b.get('tarih','')[:16]}</span>
                </div>""", unsafe_allow_html=True)

    # ── HATIRLATMALAR ──
    with sub[4]:
        styled_section("Otomatik Hatirlatmalar")

        hatirlatmalar = []
        # Eksik asi
        students = load_shared_students()
        asi_yapilan = set(a.get("ogrenci_id","") for a in asi_kayitlari)
        eksik_asi = [s for s in students if s.get("id","") not in asi_yapilan]
        if eksik_asi:
            hatirlatmalar.append(("💉 Eksik Asi", f"{len(eksik_asi)} ogrencinin asi kaydi yok", "#ef4444"))

        # Eksik olcum
        olcum_yapilan = set(o.get("ogrenci_id","") for o in olcumler)
        eksik_olcum = [s for s in students if s.get("id","") not in olcum_yapilan]
        if eksik_olcum:
            hatirlatmalar.append(("📏 Eksik Olcum", f"{len(eksik_olcum)} ogrencinin olcumu yok", "#f59e0b"))

        # Suresi dolan sertifika
        gecen_sert = [s for s in sertifikalar
                      if s.get("gecerlilik") and s["gecerlilik"] < date.today().isoformat()]
        if gecen_sert:
            hatirlatmalar.append(("🎓 Sertifika", f"{len(gecen_sert)} personelin sertifikasi dolmus", "#8b5cf6"))

        if not hatirlatmalar:
            st.success("Aktif hatirlatma yok!")
        else:
            for baslik, mesaj, renk in hatirlatmalar:
                st.markdown(f"""
                <div style="background:{renk}10;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:10px 14px;margin:5px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.8rem;">{baslik}</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{mesaj}</div>
                </div>""", unsafe_allow_html=True)
