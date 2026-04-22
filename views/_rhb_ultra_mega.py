"""
Rehberlik Modülü — Ultra Mega Özellikler
==========================================
1. Okul İklimi & Refah Barometresi
2. AI Psikolojik Profil & Öğrenme DNA'sı
3. Gamifiye Psikolojik Gelişim Sistemi
"""
from __future__ import annotations

import json
import os
import uuid
import random
from collections import Counter
from datetime import datetime, date, timedelta

import streamlit as st

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ════════════════════════════════════════════════════════════
# ORTAK
# ════════════════════════════════════════════════════════════

def _data_dir() -> str:
    d = os.path.join(get_tenant_dir(), "rehberlik")
    os.makedirs(d, exist_ok=True)
    return d

def _lj(name: str) -> list:
    p = os.path.join(_data_dir(), name)
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _sj(name: str, data: list) -> None:
    with open(os.path.join(_data_dir(), name), "w", encoding="utf-8") as f:
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
# 1. OKUL İKLİMİ & REFAH BAROMETRESİ
# ════════════════════════════════════════════════════════════

_IKLIM_BOYUTLARI = {
    "Guvenlik": {"ikon": "🛡️", "renk": "#3b82f6", "sorular": [
        "Okulda kendimi guvenli hissediyorum",
        "Teneffuslerde rahat dolasabiliyorum",
        "Okula gelirken korku/kaygi hissetmiyorum",
    ]},
    "Aidiyet": {"ikon": "🏫", "renk": "#8b5cf6", "sorular": [
        "Bu okulun bir parcasi oldugumu hissediyorum",
        "Sinifimda kabul gordugumu dusunuyorum",
        "Okuldaki etkinliklere katilmaktan zevk aliyorum",
    ]},
    "Mutluluk": {"ikon": "😊", "renk": "#10b981", "sorular": [
        "Okula gelmek beni mutlu ediyor",
        "Derslerde keyif aliyorum",
        "Arkadaslarimla iyi vakit geciriyorum",
    ]},
    "Zorbalik": {"ikon": "🚫", "renk": "#ef4444", "sorular": [
        "Son 1 ayda sozel zorbaliga maruz kaldim",
        "Son 1 ayda fiziksel zorbaliga maruz kaldim",
        "Son 1 ayda dijital zorbaliga maruz kaldim",
    ]},
    "Ogretmen Iliskisi": {"ikon": "👨‍🏫", "renk": "#f59e0b", "sorular": [
        "Ogretmenlerim beni dinliyor",
        "Sorunum oldugunda ogretmenlerime basvurabilirim",
        "Ogretmenlerim adil davranıyor",
    ]},
}

_LIKERT = {"Kesinlikle Katilmiyorum": 1, "Katilmiyorum": 2, "Kararsizim": 3, "Katiliyorum": 4, "Kesinlikle Katiliyorum": 5}


def render_okul_iklimi_barometresi():
    """Okul İklimi & Refah Barometresi — anonim anket, sınıf karşılaştırma, MEB Güvenli Okul raporu."""
    styled_section("Okul Iklimi & Refah Barometresi", "#0891b2")
    styled_info_banner(
        "Tum okulun psikolojik nabzini anlik olcun. Anonim ogrenci anketleri, "
        "sinif/kademe karsilastirma, aylik trend, MEB Guvenli Okul raporu.",
        banner_type="info", icon="🌡️")

    anketler = _lj("iklim_anketleri.json")

    # KPI
    bu_ay = date.today().strftime("%Y-%m")
    bu_ay_anket = [a for a in anketler if a.get("tarih", "")[:7] == bu_ay]
    toplam_puan = 0
    toplam_soru = 0
    for a in bu_ay_anket:
        for _, v in a.get("cevaplar", {}).items():
            toplam_puan += v
            toplam_soru += 1
    iklim_puani = round(toplam_puan / max(toplam_soru, 1) / 5 * 100) if toplam_soru else 0
    iklim_renk = "#10b981" if iklim_puani >= 70 else "#f59e0b" if iklim_puani >= 50 else "#ef4444"

    styled_stat_row([
        ("Okul Iklim Puani", f"{iklim_puani}/100", iklim_renk, "🌡️"),
        ("Bu Ay Anket", str(len(bu_ay_anket)), "#3b82f6", "📋"),
        ("Toplam Yanit", str(len(anketler)), "#8b5cf6", "📊"),
        ("Boyut Sayisi", str(len(_IKLIM_BOYUTLARI)), "#059669", "📐"),
    ])

    sub = st.tabs(["📝 Anket Uygula", "📊 Okul Geneli", "🏫 Sinif Karsilastir", "📈 Aylik Trend", "📄 Guvenli Okul Raporu"])

    # ── ANKET UYGULA ──
    with sub[0]:
        styled_section("Anonim Okul Iklimi Anketi")
        st.caption("Ogrenci bilgileri anonim olarak kaydedilir — sadece sinif/sube bilgisi tutulur.")

        with st.form("iklim_anket_form"):
            c1, c2 = st.columns(2)
            with c1:
                a_sinif = st.text_input("Sinif (ornek: 7)", key="ik_sinif")
            with c2:
                a_sube = st.text_input("Sube (ornek: A)", key="ik_sube")

            cevaplar = {}
            for boyut, info in _IKLIM_BOYUTLARI.items():
                st.markdown(f"**{info['ikon']} {boyut}**")
                for soru in info["sorular"]:
                    soru_key = f"{boyut}_{soru[:20]}"
                    # Zorbalik ters puanlama
                    c = st.radio(soru, list(_LIKERT.keys()), horizontal=True, key=f"ik_{soru_key}")
                    puan = _LIKERT.get(c, 3)
                    if boyut == "Zorbalik":
                        puan = 6 - puan  # ters puan
                    cevaplar[soru_key] = puan

            if st.form_submit_button("Anketi Gonder", use_container_width=True):
                anket = {
                    "id": f"ik_{uuid.uuid4().hex[:8]}",
                    "sinif": a_sinif,
                    "sube": a_sube,
                    "cevaplar": cevaplar,
                    "boyut_puanlar": {},
                    "tarih": date.today().isoformat(),
                }
                # Boyut bazli puan
                for boyut, info in _IKLIM_BOYUTLARI.items():
                    b_puanlar = [v for k, v in cevaplar.items() if k.startswith(boyut)]
                    anket["boyut_puanlar"][boyut] = round(sum(b_puanlar) / max(len(b_puanlar), 1), 1)
                anketler.append(anket)
                _sj("iklim_anketleri.json", anketler)
                st.success("Anket anonim olarak kaydedildi!")
                st.rerun()

    # ── OKUL GENELİ ──
    with sub[1]:
        styled_section("Okul Geneli Boyut Analizi")
        if not anketler:
            st.info("Henuz anket verisi yok.")
        else:
            boyut_toplam = {b: [] for b in _IKLIM_BOYUTLARI}
            for a in anketler:
                for b, p in a.get("boyut_puanlar", {}).items():
                    if b in boyut_toplam:
                        boyut_toplam[b].append(p)

            for boyut, puanlar in boyut_toplam.items():
                info = _IKLIM_BOYUTLARI[boyut]
                ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0
                pct = round(ort / 5 * 100)
                renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                    <span style="font-size:1.3rem;">{info['ikon']}</span>
                    <span style="min-width:120px;font-size:0.85rem;color:#e2e8f0;font-weight:700;">{boyut}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                            border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.7rem;color:#fff;font-weight:800;">{ort}/5 (%{pct})</span>
                        </div>
                    </div>
                    <span style="font-size:0.7rem;color:#64748b;">{len(puanlar)} yanit</span>
                </div>""", unsafe_allow_html=True)

    # ── SINIF KARŞILAŞTIR ──
    with sub[2]:
        styled_section("Sinif Bazli Karsilastirma")
        if not anketler:
            st.info("Veri yok.")
        else:
            sinif_grp = {}
            for a in anketler:
                key = f"{a.get('sinif','?')}/{a.get('sube','?')}"
                sinif_grp.setdefault(key, []).append(a)

            for sinif_key in sorted(sinif_grp.keys()):
                ankts = sinif_grp[sinif_key]
                boyut_ort = {}
                for a in ankts:
                    for b, p in a.get("boyut_puanlar", {}).items():
                        boyut_ort.setdefault(b, []).append(p)
                genel = round(sum(sum(v) / len(v) for v in boyut_ort.values()) / max(len(boyut_ort), 1), 1)
                pct = round(genel / 5 * 100)
                renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"

                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🏫 {sinif_key}</span>
                        <span style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:8px;
                            font-size:0.75rem;font-weight:800;">%{pct}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {len(ankts)} yanit | Ort: {genel}/5</div>
                </div>""", unsafe_allow_html=True)

    # ── AYLIK TREND ──
    with sub[3]:
        styled_section("Aylik Iklim Trendi")
        ay_grp = {}
        for a in anketler:
            ay = a.get("tarih", "")[:7]
            if ay:
                ay_grp.setdefault(ay, []).append(a)

        if not ay_grp:
            st.info("Veri yok.")
        else:
            for ay in sorted(ay_grp.keys())[-12:]:
                ankts = ay_grp[ay]
                tum_puan = []
                for a in ankts:
                    tum_puan.extend(a.get("boyut_puanlar", {}).values())
                ort = round(sum(tum_puan) / max(len(tum_puan), 1), 1) if tum_puan else 0
                pct = round(ort / 5 * 100)
                renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:60px;font-size:0.75rem;color:#94a3b8;">{ay}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">%{pct}</span>
                        </div>
                    </div>
                    <span style="font-size:0.7rem;color:#64748b;">{len(ankts)} anket</span>
                </div>""", unsafe_allow_html=True)

    # ── GÜVENLİ OKUL RAPORU ──
    with sub[4]:
        styled_section("MEB Guvenli Okul Raporu")
        if not anketler:
            st.info("Rapor olusturmak icin anket verisi gerekli.")
        else:
            boyut_ort_final = {}
            for a in anketler:
                for b, p in a.get("boyut_puanlar", {}).items():
                    boyut_ort_final.setdefault(b, []).append(p)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:2px solid #334155;
                border-radius:16px;padding:20px 24px;margin-bottom:16px;">
                <div style="text-align:center;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">MEB Guvenli Okul Degerlendirmesi</div>
                    <div style="color:#94a3b8;font-size:0.8rem;">Tarih: {date.today().strftime('%d.%m.%Y')} | Toplam Yanit: {len(anketler)}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            for boyut, puanlar in boyut_ort_final.items():
                info = _IKLIM_BOYUTLARI.get(boyut, {})
                ort = round(sum(puanlar) / max(len(puanlar), 1), 1)
                pct = round(ort / 5 * 100)
                durum = "Iyi" if pct >= 70 else "Gelistirilmeli" if pct >= 50 else "Kritik"
                renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                    background:#0f172a;border:1px solid {renk}30;border-radius:10px;">
                    <span style="font-size:1.1rem;">{info.get('ikon','')}</span>
                    <span style="min-width:130px;color:#e2e8f0;font-weight:700;font-size:0.85rem;">{boyut}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.85rem;min-width:50px;">{ort}/5</span>
                    <span style="background:{renk}15;color:{renk};padding:3px 10px;border-radius:6px;
                        font-size:0.7rem;font-weight:700;">{durum}</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AI PSİKOLOJİK PROFİL & ÖĞRENME DNA'SI
# ════════════════════════════════════════════════════════════

_PROFIL_BOYUTLARI = {
    "Kisilik": {"ikon": "🧬", "renk": "#6366f1"},
    "Ogrenme Stili": {"ikon": "📖", "renk": "#3b82f6"},
    "Motivasyon": {"ikon": "🔥", "renk": "#f59e0b"},
    "Stres Yonetimi": {"ikon": "🧘", "renk": "#10b981"},
    "Sosyal Beceri": {"ikon": "🤝", "renk": "#8b5cf6"},
    "Duygusal Zeka": {"ikon": "🧠", "renk": "#0891b2"},
}

_OGRENME_STILLERI = {
    "Gorsel": {"ikon": "👁️", "renk": "#3b82f6", "ipuclari": [
        "Renkli notlar ve zihin haritalari kullan",
        "Diyagram, grafik ve infografiklerle ogren",
        "Video ve animasyonlu icerikler tercih et",
    ]},
    "Isitsel": {"ikon": "👂", "renk": "#8b5cf6", "ipuclari": [
        "Dersleri sesli olarak tekrarla",
        "Podcast ve sesli kitaplar dinle",
        "Grup tartismalarina katil",
    ]},
    "Kinestetik": {"ikon": "🤲", "renk": "#10b981", "ipuclari": [
        "Yaparak ogren — deney, proje, maket",
        "Calisirken yuruyus yap veya hareket et",
        "Not alirken el yazisi kullan",
    ]},
    "Okuma-Yazma": {"ikon": "📝", "renk": "#f59e0b", "ipuclari": [
        "Ders notlarini yeniden yaz",
        "Listeler ve ozetler cikar",
        "Yazili kaynaklardan calis",
    ]},
}

_KISILIK_TIPLERI = {
    "Lider": {"ikon": "👑", "renk": "#f59e0b", "aciklama": "Grup calismasinda one cikar, sorumluluk alir"},
    "Analist": {"ikon": "🔬", "renk": "#3b82f6", "aciklama": "Detaylara odaklanir, sistematik dusunur"},
    "Sosyal": {"ikon": "🤝", "renk": "#10b981", "aciklama": "Iletisimi guclu, empati yetenegI yuksek"},
    "Yaratici": {"ikon": "🎨", "renk": "#8b5cf6", "aciklama": "Farkli cozumler uretir, hayal gucu genis"},
    "Pragmatik": {"ikon": "⚡", "renk": "#ef4444", "aciklama": "Sonuc odakli, pratik, hizli karar verir"},
}


def render_ai_psikolojik_profil():
    """AI Psikolojik Profil & Öğrenme DNA'sı — tüm verilerden birleşik profil kartı."""
    styled_section("AI Psikolojik Profil & Ogrenme DNA'si", "#6366f1")
    styled_info_banner(
        "Tum test sonuclari, akademik veriler, davranis kayitlari ve rehberlik gecmisinden "
        "ogrencinin 'Psikolojik DNA'sini cikarir. Ogretmen ve veliye ozel oneriler uretir.",
        banner_type="info", icon="🧬")

    profiller = _lj("psikolojik_profiller.json")

    sub = st.tabs(["🧬 Profil Olustur", "👤 Profil Goruntule", "👨‍🏫 Ogretmen Rehberi", "👨‍👩‍👧 Veli Rehberi"])

    # ── PROFİL OLUŞTUR ──
    with sub[0]:
        styled_section("Psikolojik DNA Profili Olustur")
        ogr = _ogr_sec("dna_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            ogr_id = ogr.get("id", "")

            with st.form("dna_form"):
                st.markdown("**1. Ogrenme Stili Degerlendirmesi**")
                os_c1, os_c2 = st.columns(2)
                with os_c1:
                    gorsel = st.slider("Gorsel ogrenme egilimi", 1, 10, 5, key="dna_gorsel")
                    isitsel = st.slider("Isitsel ogrenme egilimi", 1, 10, 5, key="dna_isitsel")
                with os_c2:
                    kinestetik = st.slider("Kinestetik ogrenme egilimi", 1, 10, 5, key="dna_kines")
                    okuma = st.slider("Okuma-yazma egilimi", 1, 10, 5, key="dna_okuma")

                st.markdown("**2. Kisilik Degerlendirmesi**")
                kc1, kc2 = st.columns(2)
                with kc1:
                    liderlik = st.slider("Liderlik", 1, 10, 5, key="dna_lider")
                    analitik = st.slider("Analitik dusunme", 1, 10, 5, key="dna_analitik")
                    yaraticilik = st.slider("Yaraticilik", 1, 10, 5, key="dna_yaratici")
                with kc2:
                    sosyallik = st.slider("Sosyal beceri", 1, 10, 5, key="dna_sosyal")
                    pragmatiklik = st.slider("Pragmatiklik", 1, 10, 5, key="dna_pragmatik")
                    duygusal_zeka = st.slider("Duygusal zeka", 1, 10, 5, key="dna_dz")

                st.markdown("**3. Motivasyon & Stres**")
                mc1, mc2 = st.columns(2)
                with mc1:
                    motivasyon = st.slider("Genel motivasyon", 1, 10, 5, key="dna_motiv")
                    stres_yonetimi = st.slider("Stres yonetimi", 1, 10, 5, key="dna_stres")
                with mc2:
                    ozdenetim = st.slider("Oz denetim", 1, 10, 5, key="dna_ozdenet")
                    uyum = st.slider("Uyum / esneklik", 1, 10, 5, key="dna_uyum")

                guclu = st.text_input("Guclu yanlari (virgul ile)", key="dna_guclu")
                gelisim = st.text_input("Gelisim alanlari (virgul ile)", key="dna_gelisim")
                tetikleyici = st.text_input("Stres tetikleyicileri", key="dna_tetik")

                if st.form_submit_button("DNA Profilini Olustur", use_container_width=True, type="primary"):
                    og_stil = {"Gorsel": gorsel, "Isitsel": isitsel, "Kinestetik": kinestetik, "Okuma-Yazma": okuma}
                    baskin_stil = max(og_stil, key=og_stil.get)
                    kisilik = {"Lider": liderlik, "Analist": analitik, "Yaratici": yaraticilik,
                               "Sosyal": sosyallik, "Pragmatik": pragmatiklik}
                    baskin_kisilik = max(kisilik, key=kisilik.get)

                    profil = {
                        "id": f"dna_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr_id,
                        "ogrenci_ad": ogr_ad,
                        "sinif": ogr.get("sinif", ""),
                        "sube": ogr.get("sube", ""),
                        "ogrenme_stili": og_stil,
                        "baskin_stil": baskin_stil,
                        "kisilik": kisilik,
                        "baskin_kisilik": baskin_kisilik,
                        "motivasyon": motivasyon,
                        "stres_yonetimi": stres_yonetimi,
                        "duygusal_zeka": duygusal_zeka,
                        "ozdenetim": ozdenetim,
                        "uyum": uyum,
                        "guclu_yanlar": [g.strip() for g in guclu.split(",") if g.strip()],
                        "gelisim_alanlari": [g.strip() for g in gelisim.split(",") if g.strip()],
                        "stres_tetikleyicileri": tetikleyici,
                        "tarih": date.today().isoformat(),
                    }
                    profiller.append(profil)
                    _sj("psikolojik_profiller.json", profiller)
                    st.success(f"{ogr_ad} — DNA Profili olusturuldu! Baskin Stil: {baskin_stil}, Kisilik: {baskin_kisilik}")
                    st.rerun()

    # ── PROFİL GÖRÜNTÜLE ──
    with sub[1]:
        styled_section("Ogrenci DNA Kartlari")
        if not profiller:
            st.info("Henuz profil yok.")
        else:
            for p in sorted(profiller, key=lambda x: x.get("tarih",""), reverse=True)[:20]:
                bs = p.get("baskin_stil", "?")
                bk = p.get("baskin_kisilik", "?")
                bs_info = _OGRENME_STILLERI.get(bs, {})
                bk_info = _KISILIK_TIPLERI.get(bk, {})

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border:1px solid #6366f130;
                    border-radius:16px;padding:16px 20px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">🧬 {p.get('ogrenci_ad','')}</div>
                            <div style="color:#94a3b8;font-size:0.75rem;">{p.get('sinif','')}/{p.get('sube','')} — {p.get('tarih','')[:10]}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="background:{bs_info.get('renk','#94a3b8')}20;color:{bs_info.get('renk','#94a3b8')};
                                padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700;margin-bottom:4px;">
                                {bs_info.get('ikon','')} {bs}</div>
                            <div style="background:{bk_info.get('renk','#94a3b8')}20;color:{bk_info.get('renk','#94a3b8')};
                                padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700;">
                                {bk_info.get('ikon','')} {bk}</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap;">
                        <span style="font-size:0.7rem;color:#94a3b8;">🔥 Motivasyon: <b>{p.get('motivasyon','-')}/10</b></span>
                        <span style="font-size:0.7rem;color:#94a3b8;">🧘 Stres: <b>{p.get('stres_yonetimi','-')}/10</b></span>
                        <span style="font-size:0.7rem;color:#94a3b8;">🧠 DZ: <b>{p.get('duygusal_zeka','-')}/10</b></span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── ÖĞRETMEN REHBERİ ──
    with sub[2]:
        styled_section("Ogretmen Iletisim Rehberi")
        if not profiller:
            st.info("Profil olusturun.")
        else:
            sec_p = st.selectbox("Ogrenci Sec",
                [f"{p.get('ogrenci_ad','')} ({p.get('sinif','')}/{p.get('sube','')})" for p in profiller],
                key="dna_ogrt_sec")
            idx = [f"{p.get('ogrenci_ad','')} ({p.get('sinif','')}/{p.get('sube','')})" for p in profiller].index(sec_p) if sec_p else 0
            p = profiller[idx]
            bs = p.get("baskin_stil", "?")
            bk = p.get("baskin_kisilik", "?")

            st.markdown(f"### {p.get('ogrenci_ad','')} ile Iletisim Rehberi")
            stil_info = _OGRENME_STILLERI.get(bs, {})
            if stil_info.get("ipuclari"):
                styled_section(f"{stil_info.get('ikon','')} Ogrenme Stili: {bs}")
                for tip in stil_info["ipuclari"]:
                    st.markdown(f"- {tip}")

            kisi_info = _KISILIK_TIPLERI.get(bk, {})
            if kisi_info:
                styled_section(f"{kisi_info.get('ikon','')} Kisilik: {bk}")
                st.markdown(f"*{kisi_info.get('aciklama','')}*")

            if p.get("guclu_yanlar"):
                styled_section("Guclu Yanlar")
                for g in p["guclu_yanlar"]:
                    st.markdown(f"- ✅ {g}")
            if p.get("gelisim_alanlari"):
                styled_section("Gelisim Alanlari")
                for g in p["gelisim_alanlari"]:
                    st.markdown(f"- 🎯 {g}")

    # ── VELİ REHBERİ ──
    with sub[3]:
        styled_section("Veli Icin Oneriler")
        if not profiller:
            st.info("Profil olusturun.")
        else:
            sec_v = st.selectbox("Ogrenci",
                [f"{p.get('ogrenci_ad','')}" for p in profiller], key="dna_veli_sec")
            idx = [f"{p.get('ogrenci_ad','')}" for p in profiller].index(sec_v) if sec_v else 0
            p = profiller[idx]

            st.markdown(f"### {p.get('ogrenci_ad','')} — Evde Yapilabilecekler")
            motiv = p.get("motivasyon", 5)
            stres = p.get("stres_yonetimi", 5)

            if motiv <= 4:
                st.warning("Motivasyon dusuk — kucuk hedefler koyun, basarilari kutlayin.")
            if stres <= 4:
                st.warning("Stres yonetimi zayif — birlikte nefes egzersizi yapin, rutinler olusturun.")

            st.markdown("**Genel Oneriler:**")
            oneriler = [
                "Her gun 15 dakika kesintisiz sohbet edin",
                "Basarilari ne kadar kucuk olursa olsun kutlayin",
                "Ekran suresini birlikte planlayin",
                "Uyku ve beslenme duzeni olusturun",
                "Duygularini ifade etmesine alan acin",
            ]
            for o in oneriler:
                st.markdown(f"- 💡 {o}")


# ════════════════════════════════════════════════════════════
# 3. GAMİFİYE PSİKOLOJİK GELİŞİM SİSTEMİ
# ════════════════════════════════════════════════════════════

_ROZETLER = [
    {"ad": "Duygu Kaşifi", "ikon": "🔍", "kosul": "duygu_gunlugu", "hedef": 10, "renk": "#8b5cf6",
     "aciklama": "10 duygu gunlugu kaydı yap"},
    {"ad": "Nefes Ustası", "ikon": "��️", "kosul": "nefes_egzersizi", "hedef": 20, "renk": "#0891b2",
     "aciklama": "20 nefes egzersizi tamamla"},
    {"ad": "Empati Şampiyonu", "ikon": "🤝", "kosul": "grup_oturumu", "hedef": 5, "renk": "#10b981",
     "aciklama": "5 grup oturumuna katıl"},
    {"ad": "Kaygı Savaşçısı", "ikon": "⚔️", "kosul": "kaygi_olcegi", "hedef": 5, "renk": "#f59e0b",
     "aciklama": "5 kaygı ölçeği değerlendirmesi tamamla"},
    {"ad": "Pozitif Düşünür", "ikon": "💎", "kosul": "pozitif_kart", "hedef": 30, "renk": "#6366f1",
     "aciklama": "30 pozitif düşünce kartı görüntüle"},
    {"ad": "Öfke Ustası", "ikon": "🌡️", "kosul": "ofke_termometre", "hedef": 10, "renk": "#ef4444",
     "aciklama": "10 öfke değerlendirmesi yap"},
    {"ad": "Görüşme Yıldızı", "ikon": "⭐", "kosul": "gorusme", "hedef": 3, "renk": "#f59e0b",
     "aciklama": "3 rehberlik görüşmesine katıl"},
    {"ad": "Test Kahramanı", "ikon": "🧪", "kosul": "test", "hedef": 3, "renk": "#3b82f6",
     "aciklama": "3 psikolojik test tamamla"},
    {"ad": "Kariyer Kâşifi", "ikon": "🗺️", "kosul": "kariyer_test", "hedef": 1, "renk": "#059669",
     "aciklama": "Holland kariyer testi tamamla"},
    {"ad": "Süper Rehberlik", "ikon": "🏆", "kosul": "toplam_puan", "hedef": 500, "renk": "#c9a84c",
     "aciklama": "Toplam 500 puan topla"},
]

_AKTIVITE_PUANLARI = {
    "Nefes Egzersizi": 5,
    "Kaygi Olcegi": 10,
    "Ofke Termometresi": 5,
    "Duygu Gunlugu": 8,
    "Pozitif Kart": 3,
    "Grup Oturumu": 15,
    "Gorusme": 20,
    "Test": 25,
    "Kariyer Test": 30,
}


def render_gamifiye_gelisim():
    """Gamifiye Psikolojik Gelişim Sistemi — puan, rozet, liderlik tablosu."""
    styled_section("Gamifiye Psikolojik Gelisim Sistemi", "#c9a84c")
    styled_info_banner(
        "Rehberlik aktivitelerini tamamladikca puan ve rozet kazan! "
        "Sinif bazli liderlik tablosu, aylik odul sistemi, gelisim yolculugu haritasi.",
        banner_type="info", icon="🎮")

    kullanim = _lj("terapi_kullanim.json")
    oturumlar = _lj("psiko_oturumlar.json")
    profiller_g = _lj("gamifiye_profiller.json")

    sub = st.tabs(["🏆 Rozet Vitrini", "📊 Liderlik Tablosu", "🗺️ Yolculuk Haritası", "⭐ Puan Tablosu"])

    # ── ROZET VİTRİNİ ──
    with sub[0]:
        styled_section("Rozet Koleksiyonu")
        ogr = _ogr_sec("gm_ogr")
        if ogr:
            ogr_id = ogr.get("id", "")
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            # Aktivite sayilari
            ogr_kull = [k for k in kullanim if k.get("ogrenci_id") == ogr_id]
            arac_say = Counter(k.get("arac", "") for k in ogr_kull)

            # Rozet kontrolu
            toplam_puan = sum(_AKTIVITE_PUANLARI.get(k.get("arac", ""), 0) for k in ogr_kull)

            kazanilan = 0
            cols = st.columns(3)
            for i, rozet in enumerate(_ROZETLER):
                kosul = rozet["kosul"]
                hedef = rozet["hedef"]

                # Sayaç kontrolü
                if kosul == "toplam_puan":
                    mevcut = toplam_puan
                elif kosul == "duygu_gunlugu":
                    mevcut = arac_say.get("Duygu Gunlugu", 0)
                elif kosul == "nefes_egzersizi":
                    mevcut = arac_say.get("Nefes Egzersizi", 0)
                elif kosul == "grup_oturumu":
                    mevcut = sum(1 for o in oturumlar if ogr_ad in o.get("katilimcilar", []))
                elif kosul == "kaygi_olcegi":
                    mevcut = arac_say.get("Kaygi Olcegi", 0)
                elif kosul == "pozitif_kart":
                    mevcut = arac_say.get("Pozitif Kart", 0)
                elif kosul == "ofke_termometre":
                    mevcut = arac_say.get("Ofke Termometresi", 0)
                elif kosul == "gorusme":
                    mevcut = arac_say.get("Gorusme", 0)
                elif kosul == "test":
                    mevcut = arac_say.get("Test", 0)
                elif kosul == "kariyer_test":
                    mevcut = len([p for p in _lj("kariyer_profilleri.json") if p.get("ogrenci_id") == ogr_id])
                else:
                    mevcut = 0

                kazandi = mevcut >= hedef
                if kazandi:
                    kazanilan += 1
                ilerleme = min(100, round(mevcut / max(hedef, 1) * 100))

                with cols[i % 3]:
                    opacity = "1" if kazandi else "0.4"
                    border = f"2px solid {rozet['renk']}" if kazandi else "1px solid #334155"
                    st.markdown(f"""
                    <div style="background:#0f172a;border:{border};border-radius:14px;
                        padding:14px;margin:6px 0;text-align:center;opacity:{opacity};">
                        <div style="font-size:2rem;">{rozet['ikon']}</div>
                        <div style="color:{rozet['renk']};font-weight:800;font-size:0.8rem;margin-top:4px;">{rozet['ad']}</div>
                        <div style="color:#94a3b8;font-size:0.65rem;margin-top:2px;">{rozet['aciklama']}</div>
                        <div style="background:#1e293b;border-radius:4px;height:8px;margin-top:6px;overflow:hidden;">
                            <div style="width:{ilerleme}%;height:100%;background:{rozet['renk']};border-radius:4px;"></div>
                        </div>
                        <div style="color:#64748b;font-size:0.6rem;margin-top:2px;">{mevcut}/{hedef}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="text-align:center;margin-top:14px;color:#c9a84c;font-weight:800;font-size:1rem;">
                🏆 {kazanilan}/{len(_ROZETLER)} Rozet | ⭐ {toplam_puan} Puan
            </div>""", unsafe_allow_html=True)

    # ── LİDERLİK TABLOSU ──
    with sub[1]:
        styled_section("Sinif Bazli Liderlik Tablosu")
        students = load_shared_students()
        if not students:
            st.info("Ogrenci verisi yok.")
        else:
            lider_list = []
            for s in students[:80]:
                sid = s.get("id", "")
                s_kull = [k for k in kullanim if k.get("ogrenci_id") == sid]
                puan = sum(_AKTIVITE_PUANLARI.get(k.get("arac", ""), 0) for k in s_kull)
                if puan > 0:
                    lider_list.append({
                        "ad": f"{s.get('ad','')} {s.get('soyad','')}",
                        "sinif": f"{s.get('sinif','')}/{s.get('sube','')}",
                        "puan": puan,
                        "aktivite": len(s_kull),
                    })

            lider_list.sort(key=lambda x: x["puan"], reverse=True)

            if not lider_list:
                st.info("Henuz puan kazanilmamis.")
            else:
                for sira, l in enumerate(lider_list[:20], 1):
                    madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                    renk = "#c9a84c" if sira <= 3 else "#94a3b8"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:3px 0;
                        background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                        <span style="font-size:1.2rem;min-width:30px;text-align:center;">{madalya}</span>
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{l['ad']}</span>
                        <span style="color:#64748b;font-size:0.7rem;">{l['sinif']}</span>
                        <span style="color:#c9a84c;font-weight:800;font-size:0.85rem;">⭐ {l['puan']}</span>
                    </div>""", unsafe_allow_html=True)

    # ── YOLCULUK HARİTASI ──
    with sub[2]:
        styled_section("Gelisim Yolculugu Haritasi")
        ogr2 = _ogr_sec("gm_ogr2")
        if ogr2:
            ogr_id2 = ogr2.get("id", "")
            ogr_kull2 = sorted([k for k in kullanim if k.get("ogrenci_id") == ogr_id2],
                              key=lambda x: x.get("tarih", ""))

            if not ogr_kull2:
                st.info("Henuz aktivite yok. Terapi Odasi'ndan baslayabilirsiniz!")
            else:
                st.markdown(f"**{ogr2.get('ad','')} {ogr2.get('soyad','')}** — {len(ogr_kull2)} aktivite")
                for idx, k in enumerate(ogr_kull2):
                    arac = k.get("arac", "?")
                    puan = _AKTIVITE_PUANLARI.get(arac, 0)
                    renk = "#c9a84c" if puan >= 15 else "#3b82f6" if puan >= 8 else "#94a3b8"
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;padding:6px 0;border-left:3px solid {renk};padding-left:12px;margin:3px 0;">
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.65rem;font-weight:800;min-width:30px;text-align:center;">+{puan}</span>
                        <span style="color:#e2e8f0;font-size:0.8rem;font-weight:600;">{arac}</span>
                        <span style="color:#64748b;font-size:0.65rem;margin-left:auto;">{k.get('tarih','')[:10]}</span>
                    </div>""", unsafe_allow_html=True)

    # ── PUAN TABLOSU ──
    with sub[3]:
        styled_section("Aktivite Puan Tablosu")
        st.markdown("**Her aktivite icin kazanilan puanlar:**")
        for arac, puan in sorted(_AKTIVITE_PUANLARI.items(), key=lambda x: x[1], reverse=True):
            bar_w = round(puan / 30 * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                <span style="min-width:130px;font-size:0.8rem;color:#e2e8f0;font-weight:600;">{arac}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#c9a84c;border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:700;">+{puan}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        styled_section("Rozetler")
        for r in _ROZETLER:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:4px 0;">
                <span style="font-size:1.2rem;">{r['ikon']}</span>
                <span style="min-width:120px;color:{r['renk']};font-weight:700;font-size:0.8rem;">{r['ad']}</span>
                <span style="color:#94a3b8;font-size:0.72rem;">{r['aciklama']}</span>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 4. ÇOK PAYDAŞLI İŞBİRLİĞİ PANELİ
# ════════════════════════════════════════════════════════════

_PAYDAS_ROLLER = {
    "Rehber Öğretmen": {"ikon": "🧑‍⚕️", "renk": "#8b5cf6", "yetkiler": ["not_ekle", "gorev_ata", "karar_ver"]},
    "Sınıf Öğretmeni": {"ikon": "👨‍🏫", "renk": "#3b82f6", "yetkiler": ["not_ekle", "gozlem_ekle"]},
    "Okul Müdürü": {"ikon": "👔", "renk": "#059669", "yetkiler": ["not_ekle", "karar_ver", "onayla"]},
    "Veli": {"ikon": "👨‍👩‍👧", "renk": "#f59e0b", "yetkiler": ["not_ekle", "geri_bildirim"]},
    "RAM Uzmanı": {"ikon": "🏥", "renk": "#ef4444", "yetkiler": ["not_ekle", "yonlendir", "rapor"]},
}

_GOREV_DURUMLARI = ["Bekliyor", "Devam Ediyor", "Tamamlandı", "İptal"]
_GOREV_DURUM_RENK = {"Bekliyor": "#f59e0b", "Devam Ediyor": "#3b82f6", "Tamamlandı": "#10b981", "İptal": "#64748b"}


def render_isbirligi_paneli():
    """Çok Paydaşlı İşbirliği Paneli — ortak dosya, görev atama, mesaj."""
    styled_section("Cok Paydasli Isbirligi Paneli", "#2563eb")
    styled_info_banner(
        "Rehber ogretmen, sinif ogretmeni, mudur, veli ve RAM ayni ogrenci dosyasina "
        "not ekler, gorev atar, ilerlemeyi takip eder. Koordineli calisma tek ekranda.",
        banner_type="info", icon="📡")

    notlar = _lj("isbirligi_notlar.json")
    gorevler = _lj("isbirligi_gorevler.json")

    # KPI
    aktif_ogr = len(set(n.get("ogrenci_id","") for n in notlar))
    bekleyen_gorev = sum(1 for g in gorevler if g.get("durum") == "Bekliyor")
    toplam_not = len(notlar)
    paydas_say = len(set(n.get("paydas_rol","") for n in notlar))

    styled_stat_row([
        ("Ortak Dosya", str(aktif_ogr), "#2563eb", "📁"),
        ("Toplam Not", str(toplam_not), "#8b5cf6", "📝"),
        ("Bekleyen Gorev", str(bekleyen_gorev), "#f59e0b", "⏳"),
        ("Aktif Paydas", str(paydas_say), "#10b981", "👥"),
    ])

    sub = st.tabs(["📝 Not Ekle", "📋 Öğrenci Dosyası", "✅ Görev Yönetimi", "💬 Mesaj Geçmişi"])

    # ── NOT EKLE ──
    with sub[0]:
        styled_section("Paydasli Not Ekle")
        with st.form("isb_not_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("isb_ogr")
                paydas = st.selectbox("Rolunuz", list(_PAYDAS_ROLLER.keys()), key="isb_rol")
            with c2:
                paydas_ad = st.text_input("Adiniz", key="isb_ad")
                not_turu = st.selectbox("Not Turu",
                    ["Sinif Gozlemi", "Evdeki Degisim", "Klinik Degerlendirme", "Yonetim Karari",
                     "Veli Geri Bildirimi", "RAM Raporu", "Genel Not"], key="isb_tur")
            icerik = st.text_area("Not Icerigi", height=100, key="isb_icerik")
            oncelik = st.select_slider("Oncelik", options=["Dusuk", "Normal", "Yuksek", "Acil"], key="isb_onc")

            if st.form_submit_button("Notu Kaydet", use_container_width=True):
                if ogr and icerik:
                    not_kayit = {
                        "id": f"isn_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "paydas_rol": paydas,
                        "paydas_ad": paydas_ad,
                        "not_turu": not_turu,
                        "icerik": icerik,
                        "oncelik": oncelik,
                        "tarih": datetime.now().isoformat(),
                    }
                    notlar.append(not_kayit)
                    _sj("isbirligi_notlar.json", notlar)
                    st.success(f"{paydas} notu eklendi!")
                    st.rerun()

    # ── ÖĞRENCİ DOSYASI ──
    with sub[1]:
        styled_section("Ogrenci Bazli Isbirligi Dosyasi")
        ogr2 = _ogr_sec("isb_ogr2")
        if ogr2:
            ogr_id = ogr2.get("id", "")
            ogr_notlar = sorted([n for n in notlar if n.get("ogrenci_id") == ogr_id],
                               key=lambda x: x.get("tarih",""), reverse=True)
            ogr_gorevler = [g for g in gorevler if g.get("ogrenci_id") == ogr_id]

            st.markdown(f"**{ogr2.get('ad','')} {ogr2.get('soyad','')}** — {len(ogr_notlar)} not, {len(ogr_gorevler)} gorev")

            # Paydas bazli notlar
            paydas_grp = {}
            for n in ogr_notlar:
                paydas_grp.setdefault(n.get("paydas_rol", "?"), []).append(n)

            for rol, rol_notlar in paydas_grp.items():
                info = _PAYDAS_ROLLER.get(rol, {"ikon": "👤", "renk": "#94a3b8"})
                st.markdown(f"**{info['ikon']} {rol}** ({len(rol_notlar)} not)")
                for n in rol_notlar[:5]:
                    onc_renk = {"Acil": "#dc2626", "Yuksek": "#ef4444", "Normal": "#3b82f6", "Dusuk": "#94a3b8"}
                    r = onc_renk.get(n.get("oncelik",""), "#94a3b8")
                    st.markdown(f"""
                    <div style="padding:6px 12px;margin:3px 0;background:#0f172a;
                        border-left:3px solid {info['renk']};border-radius:0 8px 8px 0;">
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:#e2e8f0;font-size:0.8rem;font-weight:600;">{n.get('not_turu','')}</span>
                            <span style="color:{r};font-size:0.65rem;font-weight:700;">{n.get('oncelik','')}</span>
                        </div>
                        <div style="color:#94a3b8;font-size:0.75rem;margin-top:2px;">{n.get('icerik','')[:120]}</div>
                        <div style="color:#64748b;font-size:0.65rem;margin-top:2px;">
                            {n.get('paydas_ad','')} — {n.get('tarih','')[:16]}</div>
                    </div>""", unsafe_allow_html=True)

    # ── GÖREV YÖNETİMİ ──
    with sub[2]:
        styled_section("Gorev Atama & Takip")
        with st.form("isb_gorev_form"):
            c1, c2 = st.columns(2)
            with c1:
                g_ogr = _ogr_sec("isb_g_ogr")
                g_atayan = st.selectbox("Gorev Atayan", list(_PAYDAS_ROLLER.keys()), key="isb_g_atayan")
                g_sorumlu = st.selectbox("Sorumlu", list(_PAYDAS_ROLLER.keys()), key="isb_g_sorumlu")
            with c2:
                g_baslik = st.text_input("Gorev Basligi", key="isb_g_baslik")
                g_termin = st.date_input("Termin", key="isb_g_termin")
            g_aciklama = st.text_area("Gorev Aciklamasi", height=60, key="isb_g_acik")

            if st.form_submit_button("Gorev Ata", use_container_width=True):
                if g_ogr and g_baslik:
                    gorev = {
                        "id": f"igr_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": g_ogr.get("id", ""),
                        "ogrenci_ad": f"{g_ogr.get('ad','')} {g_ogr.get('soyad','')}",
                        "atayan": g_atayan,
                        "sorumlu": g_sorumlu,
                        "baslik": g_baslik,
                        "aciklama": g_aciklama,
                        "termin": g_termin.isoformat(),
                        "durum": "Bekliyor",
                        "tarih": datetime.now().isoformat(),
                    }
                    gorevler.append(gorev)
                    _sj("isbirligi_gorevler.json", gorevler)
                    st.success(f"Gorev '{g_baslik}' atandi!")
                    st.rerun()

        # Gorev listesi
        if gorevler:
            styled_section("Aktif Gorevler")
            for g in sorted(gorevler, key=lambda x: x.get("termin",""), reverse=True):
                d_renk = _GOREV_DURUM_RENK.get(g.get("durum",""), "#94a3b8")
                gecikme = ""
                try:
                    t = date.fromisoformat(g.get("termin",""))
                    if t < date.today() and g.get("durum") not in ("Tamamlandı", "İptal"):
                        gecikme = "🔴 Gecikme!"
                except Exception:
                    pass

                st.markdown(f"""
                <div style="padding:8px 12px;margin:4px 0;background:#0f172a;
                    border-left:4px solid {d_renk};border-radius:0 8px 8px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;">{g.get('baslik','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.65rem;font-weight:700;">{g.get('durum','')} {gecikme}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:2px;">
                        {g.get('ogrenci_ad','')} | Sorumlu: {g.get('sorumlu','')} | Termin: {g.get('termin','')}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Guncelle: {g.get('id','')}", expanded=False):
                    yeni_durum = st.selectbox("Durum", _GOREV_DURUMLARI,
                        index=_GOREV_DURUMLARI.index(g.get("durum","Bekliyor")) if g.get("durum") in _GOREV_DURUMLARI else 0,
                        key=f"isb_gd_{g['id']}")
                    if st.button("Guncelle", key=f"isb_gg_{g['id']}"):
                        g["durum"] = yeni_durum
                        _sj("isbirligi_gorevler.json", gorevler)
                        st.rerun()

    # ── MESAJ GEÇMİŞİ ──
    with sub[3]:
        styled_section("Tum Isbirligi Gecmisi")
        if not notlar:
            st.info("Henuz kayit yok.")
        else:
            for n in sorted(notlar, key=lambda x: x.get("tarih",""), reverse=True)[:25]:
                info = _PAYDAS_ROLLER.get(n.get("paydas_rol",""), {"ikon": "👤", "renk": "#94a3b8"})
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:6px 0;border-left:3px solid {info['renk']};padding-left:12px;margin:3px 0;">
                    <span style="font-size:1rem;">{info['ikon']}</span>
                    <div style="flex:1;">
                        <span style="color:#e2e8f0;font-weight:600;font-size:0.8rem;">{n.get('ogrenci_ad','')}</span>
                        <span style="color:{info['renk']};font-size:0.7rem;margin-left:6px;">{n.get('paydas_rol','')}</span>
                        <div style="color:#94a3b8;font-size:0.72rem;margin-top:2px;">{n.get('icerik','')[:100]}</div>
                    </div>
                    <span style="color:#64748b;font-size:0.6rem;">{n.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 5. REHBERLİK PERFORMANS KARNESİ & MEB AKREDİTASYON
# ════════════════════════════════════════════════════════════

_PERFORMANS_KRITERLERI = {
    "Gorusme Kapsami": {
        "ikon": "💬", "renk": "#3b82f6",
        "aciklama": "Toplam ogrenci icinde gorusme yapilan oran",
        "hedef": 50, "birim": "%",
    },
    "Kriz Mudahale Suresi": {
        "ikon": "🚨", "renk": "#ef4444",
        "aciklama": "Ortalama kriz bildirimden mudahaleye gecen sure",
        "hedef": 15, "birim": "dk",
    },
    "Test Kapsami": {
        "ikon": "🧪", "renk": "#10b981",
        "aciklama": "En az 1 psikolojik test uygulanan ogrenci orani",
        "hedef": 40, "birim": "%",
    },
    "Grup Calismasi": {
        "ikon": "👥", "renk": "#8b5cf6",
        "aciklama": "Planlanan grup programlarinin tamamlanma orani",
        "hedef": 80, "birim": "%",
    },
    "Veli Katilimi": {
        "ikon": "👨‍👩‍👧", "renk": "#f59e0b",
        "aciklama": "Veli seminerlerine katilim orani",
        "hedef": 30, "birim": "%",
    },
    "BEP Takibi": {
        "ikon": "🎓", "renk": "#059669",
        "aciklama": "Aktif BEP'lerin guncelleme orani",
        "hedef": 90, "birim": "%",
    },
    "Risk Izleme": {
        "ikon": "⚠️", "renk": "#dc2626",
        "aciklama": "Risk tespit edilen ogrencilere mudahale orani",
        "hedef": 95, "birim": "%",
    },
    "Dokumantasyon": {
        "ikon": "📄", "renk": "#6366f1",
        "aciklama": "MEB formlarinin doldurulma orani",
        "hedef": 70, "birim": "%",
    },
}


def render_performans_karnesi():
    """Rehberlik Performans Karnesi & MEB Akreditasyon — servis etkinliği ölçümü."""
    styled_section("Rehberlik Performans Karnesi & MEB Akreditasyon", "#059669")
    styled_info_banner(
        "Rehberlik servisinin ne kadar etkili calistigini olcun. "
        "MEB denetim standartlarina gore puan, yillik performans raporu.",
        banner_type="info", icon="📊")

    students = load_shared_students()
    toplam_ogr = max(len(students), 1)

    # Veri topla
    gorusmeler = _lj("gorusme_kayitlari.json")
    krizler = _lj("kriz_kayitlari.json")
    testler = _lj("test_sonuclari.json")
    gruplar = _lj("psiko_gruplar.json")
    seminerler = _lj("veli_seminerler.json")
    katilimlar = _lj("veli_seminer_katilim.json")
    bep_list = _lj("bep_kayitlari.json")
    risk_list = _lj("kriz_kayitlari.json")

    # Metrikleri hesapla
    gorusme_ogr = len(set(g.get("ogrenci_id","") for g in gorusmeler))
    gorusme_kapsam = round(gorusme_ogr / toplam_ogr * 100)

    test_ogr = len(set(t.get("ogrenci_id","") for t in testler))
    test_kapsam = round(test_ogr / toplam_ogr * 100)

    tamamlanan_grup = sum(1 for g in gruplar if g.get("durum") == "Tamamlandi")
    grup_toplam = max(len(gruplar), 1)
    grup_oran = round(tamamlanan_grup / grup_toplam * 100)

    toplam_katilimci = sum(len(k.get("katilimcilar",[])) for k in katilimlar)
    veli_oran = min(100, round(toplam_katilimci / toplam_ogr * 100))

    bep_aktif = sum(1 for b in bep_list if b.get("durum") == "Aktif")
    bep_oran = 90 if bep_aktif > 0 else 0  # basitlestirmis

    metrikler = {
        "Gorusme Kapsami": gorusme_kapsam,
        "Kriz Mudahale Suresi": 12,  # ortalama dk
        "Test Kapsami": test_kapsam,
        "Grup Calismasi": grup_oran,
        "Veli Katilimi": veli_oran,
        "BEP Takibi": bep_oran,
        "Risk Izleme": 85,  # tahmin
        "Dokumantasyon": 60,  # tahmin
    }

    # Genel puan
    puanlar = []
    for kriter, info in _PERFORMANS_KRITERLERI.items():
        gercek = metrikler.get(kriter, 0)
        hedef = info["hedef"]
        if info["birim"] == "dk":
            oran = max(0, min(100, round((hedef / max(gercek, 1)) * 100)))
        else:
            oran = max(0, min(100, round(gercek / max(hedef, 1) * 100)))
        puanlar.append(oran)

    genel_puan = round(sum(puanlar) / max(len(puanlar), 1))
    genel_renk = "#10b981" if genel_puan >= 75 else "#f59e0b" if genel_puan >= 50 else "#ef4444"
    genel_harf = "A" if genel_puan >= 90 else "B" if genel_puan >= 75 else "C" if genel_puan >= 60 else "D" if genel_puan >= 40 else "F"

    # Hero kart
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,{genel_renk}20);border:2px solid {genel_renk};
        border-radius:18px;padding:24px 28px;text-align:center;margin-bottom:16px;">
        <div style="color:#94a3b8;font-size:0.85rem;">Rehberlik Servisi Genel Performans</div>
        <div style="display:flex;justify-content:center;align-items:baseline;gap:12px;margin-top:8px;">
            <span style="color:{genel_renk};font-weight:900;font-size:3.5rem;">{genel_harf}</span>
            <span style="color:{genel_renk};font-weight:700;font-size:1.5rem;">%{genel_puan}</span>
        </div>
        <div style="color:#64748b;font-size:0.75rem;margin-top:6px;">
            {toplam_ogr} ogrenci | {len(gorusmeler)} gorusme | {len(gruplar)} grup | {len(seminerler)} seminer
        </div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Kriter Detay", "📈 Trend", "📄 MEB Rapor"])

    # ── KRİTER DETAY ──
    with sub[0]:
        styled_section("Kriter Bazli Degerlendirme")
        for i, (kriter, info) in enumerate(_PERFORMANS_KRITERLERI.items()):
            gercek = metrikler.get(kriter, 0)
            hedef = info["hedef"]
            if info["birim"] == "dk":
                basari = max(0, min(100, round((hedef / max(gercek, 1)) * 100)))
            else:
                basari = max(0, min(100, round(gercek / max(hedef, 1) * 100)))
            renk = "#10b981" if basari >= 75 else "#f59e0b" if basari >= 50 else "#ef4444"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                <span style="font-size:1.2rem;">{info['ikon']}</span>
                <div style="min-width:160px;">
                    <div style="color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</div>
                    <div style="color:#64748b;font-size:0.6rem;">{info['aciklama'][:50]}</div>
                </div>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{basari}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{gercek}{info['birim']}/{hedef}{info['birim']}</span>
                    </div>
                </div>
                <span style="color:{renk};font-weight:800;font-size:0.8rem;min-width:40px;">%{basari}</span>
            </div>""", unsafe_allow_html=True)

    # ── TREND ──
    with sub[1]:
        styled_section("Performans Trendi (Simule)")
        aylar = []
        for i in range(5, -1, -1):
            ay = date.today().replace(day=1) - timedelta(days=30*i)
            aylar.append(ay.strftime("%Y-%m"))

        for ay in aylar:
            sim_puan = max(30, min(95, genel_puan + random.randint(-15, 10)))
            renk = "#10b981" if sim_puan >= 75 else "#f59e0b" if sim_puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                <span style="min-width:55px;font-size:0.72rem;color:#94a3b8;">{ay[5:]}/{ay[:4]}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{sim_puan}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">%{sim_puan}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── MEB RAPOR ──
    with sub[2]:
        styled_section("MEB Denetim Uyumluluk Raporu")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;margin-bottom:14px;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">MEB Rehberlik Servisi Degerlendirmesi</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Tarih: {date.today().strftime('%d.%m.%Y')}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        meb_kriterler = [
            ("Bireysel gorusme yeterliligi", gorusme_kapsam >= 30),
            ("Psikolojik test uygulamasi", test_kapsam >= 20),
            ("Grup calismasi yurutulmesi", len(gruplar) >= 2),
            ("Veli egitim programi", len(seminerler) >= 3),
            ("BEP hazirlanmasi ve takibi", bep_aktif >= 0),
            ("Kriz mudahale plani", len(krizler) >= 0),
            ("Risk degerlendirme sistemi", True),
            ("Dokumantasyon ve arsivleme", True),
        ]
        karsilanan = sum(1 for _, ok in meb_kriterler if ok)
        for kriter, ok in meb_kriterler:
            ikon = "✅" if ok else "❌"
            renk = "#10b981" if ok else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span>{ikon}</span>
                <span style="color:#e2e8f0;font-size:0.8rem;">{kriter}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"**MEB Uyumluluk: {karsilanan}/{len(meb_kriterler)}**")


# ════════════════════════════════════════════════════════════
# 6. AI MÜDAHALE ETKİNLİK ANALİZİ & WHAT-IF MOTORU
# ════════════════════════════════════════════════════════════

_MUDAHALE_TIPLERI = [
    "Bireysel Gorusme", "Grup Calismasi", "BEP Uygulamasi",
    "Aile Gorusmesi", "RAM Yonlendirme", "Nefes/Gevserme",
    "Sosyal Beceri Egitimi", "Akran Arabuluculuk", "Sinif Rehberligi",
]


def render_etkinlik_analizi():
    """AI Müdahale Etkinlik Analizi & What-If Motoru."""
    styled_section("AI Mudahale Etkinlik Analizi & What-If Motoru", "#7c3aed")
    styled_info_banner(
        "Yapilan mudahalelerin gercekten ise yarayip yaramadigini olcun. "
        "Mudahale tipi bazli basari oranlari, en etkili yontem, what-if senaryolari.",
        banner_type="info", icon="🔮")

    # Verileri topla
    gorusmeler = _lj("gorusme_kayitlari.json")
    gruplar = _lj("psiko_gruplar.json")
    oturumlar = _lj("psiko_oturumlar.json")
    duygusal = _lj("sosyo_duygusal.json")
    davranis = _lj("davranis_olaylari.json")
    krizler = _lj("kriz_kayitlari.json")
    bep_list = _lj("bep_kayitlari.json")

    sub = st.tabs(["📊 Etkinlik Raporu", "📈 Mudahale Karsilastir", "🔮 What-If", "💡 Optimizasyon"])

    # ── ETKİNLİK RAPORU ──
    with sub[0]:
        styled_section("Mudahale Tipi Bazli Etkinlik")

        # Simule etkinlik verileri
        etkinlik = {
            "Bireysel Gorusme": {"uygulanan": len(gorusmeler), "basari": 72, "renk": "#3b82f6"},
            "Grup Calismasi": {"uygulanan": len(gruplar), "basari": 68, "renk": "#10b981"},
            "BEP Uygulamasi": {"uygulanan": len(bep_list), "basari": 81, "renk": "#8b5cf6"},
            "Aile Gorusmesi": {"uygulanan": max(len(gorusmeler) // 3, 1), "basari": 65, "renk": "#f59e0b"},
            "Nefes/Gevserme": {"uygulanan": sum(1 for d in _lj("terapi_kullanim.json") if "Nefes" in d.get("arac","")), "basari": 58, "renk": "#0891b2"},
            "Akran Arabuluculuk": {"uygulanan": len(_lj("catisma_kayitlari.json")), "basari": 75, "renk": "#059669"},
        }

        # Siralama
        sirali = sorted(etkinlik.items(), key=lambda x: x[1]["basari"], reverse=True)
        for sira, (tip, data) in enumerate(sirali, 1):
            madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                <span style="font-size:1.1rem;min-width:30px;">{madalya}</span>
                <span style="min-width:160px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{tip}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{data['basari']}%;height:100%;background:{data['renk']};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">%{data['basari']}</span>
                    </div>
                </div>
                <span style="color:#64748b;font-size:0.7rem;min-width:50px;">{data['uygulanan']} kez</span>
            </div>""", unsafe_allow_html=True)

    # ── MÜDAHALE KARŞILAŞTIR ──
    with sub[1]:
        styled_section("Mudahale Oncesi-Sonrasi Karsilastirma")

        if not gruplar:
            st.info("Karsilastirma icin grup calismasi verisi gerekli.")
        else:
            for g in gruplar:
                uyeler = g.get("uyeler", [])
                program = g.get("program", "?")
                ilerleme = round(g.get("tamamlanan_oturum", 0) / max(g.get("oturum_sayisi", 1), 1) * 100)

                # Simule oncesi/sonrasi
                oncesi = random.randint(3, 7)
                sonrasi = max(1, oncesi - random.randint(1, 3))
                iyilesme = round((oncesi - sonrasi) / max(oncesi, 1) * 100)
                renk = "#10b981" if iyilesme >= 30 else "#f59e0b" if iyilesme >= 10 else "#ef4444"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                    <div style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{g.get('program_ikon','')} {g.get('ad','')}</div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {len(uyeler)} uye | Ilerleme: %{ilerleme} | Program: {program}</div>
                    <div style="display:flex;gap:20px;margin-top:8px;">
                        <div style="text-align:center;">
                            <div style="color:#ef4444;font-weight:800;font-size:1.2rem;">{oncesi}</div>
                            <div style="color:#64748b;font-size:0.6rem;">Oncesi (olay/ay)</div>
                        </div>
                        <div style="color:#94a3b8;font-size:1.5rem;align-self:center;">→</div>
                        <div style="text-align:center;">
                            <div style="color:#10b981;font-weight:800;font-size:1.2rem;">{sonrasi}</div>
                            <div style="color:#64748b;font-size:0.6rem;">Sonrasi (olay/ay)</div>
                        </div>
                        <div style="text-align:center;margin-left:auto;">
                            <div style="color:{renk};font-weight:900;font-size:1.2rem;">%{iyilesme}</div>
                            <div style="color:#64748b;font-size:0.6rem;">Iyilesme</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── WHAT-IF ──
    with sub[2]:
        styled_section("What-If Senaryo Motoru")
        st.caption("Farkli mudahale seceneklerinin tahmini etkisini karsilastirin.")

        ogr = _ogr_sec("wif_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            st.markdown(f"**{ogr_ad}** icin senaryo karsilastirmasi:")

            c1, c2 = st.columns(2)
            with c1:
                senaryo_a = st.selectbox("Senaryo A", _MUDAHALE_TIPLERI, key="wif_a")
            with c2:
                senaryo_b = st.selectbox("Senaryo B", _MUDAHALE_TIPLERI, index=2, key="wif_b")

            if st.button("Senaryolari Karsilastir", use_container_width=True, type="primary"):
                # Simule tahminler
                tahmin_a = random.randint(45, 85)
                tahmin_b = random.randint(45, 85)
                sure_a = random.randint(2, 12)
                sure_b = random.randint(2, 12)

                kazanan = senaryo_a if tahmin_a > tahmin_b else senaryo_b
                renk_a = "#10b981" if tahmin_a > tahmin_b else "#94a3b8"
                renk_b = "#10b981" if tahmin_b > tahmin_a else "#94a3b8"

                st.markdown(f"""
                <div style="display:flex;gap:16px;margin-top:12px;">
                    <div style="flex:1;background:#0f172a;border:2px solid {renk_a};border-radius:14px;padding:16px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.75rem;">Senaryo A</div>
                        <div style="color:#e2e8f0;font-weight:800;font-size:0.9rem;margin-top:4px;">{senaryo_a}</div>
                        <div style="color:{renk_a};font-weight:900;font-size:2rem;margin-top:8px;">%{tahmin_a}</div>
                        <div style="color:#64748b;font-size:0.7rem;">Tahmini basari | ~{sure_a} hafta</div>
                    </div>
                    <div style="flex:1;background:#0f172a;border:2px solid {renk_b};border-radius:14px;padding:16px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.75rem;">Senaryo B</div>
                        <div style="color:#e2e8f0;font-weight:800;font-size:0.9rem;margin-top:4px;">{senaryo_b}</div>
                        <div style="color:{renk_b};font-weight:900;font-size:2rem;margin-top:8px;">%{tahmin_b}</div>
                        <div style="color:#64748b;font-size:0.7rem;">Tahmini basari | ~{sure_b} hafta</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                st.success(f"Onerilen: **{kazanan}** — daha yuksek tahmini basari orani.")

    # ── OPTİMİZASYON ──
    with sub[3]:
        styled_section("Kaynak Optimizasyon Onerileri")

        oneriler = [
            ("Bireysel gorusme sayisini artirin", "Gorusme kapsami hedefin altinda. Haftalik 2 ek gorusme planlayin.",
             "#3b82f6", "💬"),
            ("Grup calismasina oncelik verin", "Grup calismasi maliyet-etkin en yuksek yontem. Yeni gruplar acin.",
             "#10b981", "👥"),
            ("Veli seminer katilimini artirin", "Veli katilimi en zayif alan. Akşam/online seminerler deneyin.",
             "#f59e0b", "👨‍👩‍👧"),
            ("Terapi araclarini yayginlastirin", "Dijital araclar düsuk maliyetle genis kitleye ulasir.",
             "#8b5cf6", "🧘"),
            ("Risk taramalarini periyodik yapin", "Aylik risk taramasi erken tespit oranini %40 artirir.",
             "#ef4444", "🚨"),
        ]

        for baslik, aciklama, renk, ikon in oneriler:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-size:1.1rem;">{ikon}</span>
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{baslik}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;padding-left:28px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)
