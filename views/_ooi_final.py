"""
Okul Oncesi & Ilkokul — ZIRVE (Final) Ozellikleri
====================================================
1. Sinif Karmasi Optimizatoru (AI Class Balancer)
2. Cocuk Mutluluk Barometresi (Kid Happiness Index)
3. Okula Hazirlik Endeksi + Gecis Raporu
"""
from __future__ import annotations

import json
import os
import random
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _td() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


def _ogrenci_sec(store, key_prefix: str):
    try:
        from utils.shared_data import get_student_display_options
        students = get_student_display_options(include_empty=False)
    except Exception:
        students = {}
    if not students:
        st.warning("Ogrenci verisi bulunamadi.")
        return None, None
    sel = st.selectbox("Ogrenci Secin", [""] + list(students.keys()), key=f"{key_prefix}_sel")
    if not sel:
        return None, None
    return sel, students.get(sel, {})


# ============================================================
# 1. SINIF KARMASI OPTİMİZATÖRÜ
# ============================================================

def render_sinif_karmasi(store):
    """AI ile adil sinif/sube dagilimi."""
    styled_section("Sinif Karmasi Optimizatoru", "#6366f1")
    styled_info_banner(
        "Yeni doneme ogrencileri sube bazli dagitmak icin AI optimizasyonu. "
        "Cinsiyet dengesi, davranis profili, milestone seviyeleri — adil dagilim.",
        banner_type="info", icon="🧮")

    ak = _ak_dir()
    td = _td()

    col1, col2 = st.columns(2)
    with col1:
        sinif = st.selectbox("Sinif", ["Anasinifi 3 Yas", "Anasinifi 4 Yas", "Anasinifi 5 Yas",
                                         "1. Sinif", "2. Sinif", "3. Sinif", "4. Sinif"], key="sk_sinif")
    with col2:
        sube_sayisi = st.number_input("Sube Sayisi", 2, 6, 3, key="sk_sube")

    students = _lj(os.path.join(ak, "students.json"))
    sinif_ogr = [s for s in students if str(s.get("sinif", "")) == str(sinif) and s.get("durum", "aktif") == "aktif"]

    if not sinif_ogr:
        styled_info_banner(f"{sinif} sinifinda ogrenci bulunamadi.", banner_type="warning", icon="👤")
        return

    # Cinsiyet dagilimi
    erkek = sum(1 for s in sinif_ogr if s.get("cinsiyet", "").lower() in ("erkek", "e"))
    kiz = len(sinif_ogr) - erkek

    styled_stat_row([
        ("Toplam Ogrenci", str(len(sinif_ogr)), "#6366f1", "👤"),
        ("Erkek", str(erkek), "#3b82f6", "👦"),
        ("Kiz", str(kiz), "#ec4899", "👧"),
        ("Sube Basi", str(len(sinif_ogr) // sube_sayisi), "#10b981", "📊"),
    ])

    if st.button("AI ile Optimal Dagilim Olustur", key="sk_btn", type="primary", use_container_width=True):
        # Basit dengeleme algoritmasi
        subeler = {chr(65 + i): [] for i in range(sube_sayisi)}  # A, B, C...

        # Cinsiyet bazli ayir
        erkekler = [s for s in sinif_ogr if s.get("cinsiyet", "").lower() in ("erkek", "e")]
        kizlar = [s for s in sinif_ogr if s.get("cinsiyet", "").lower() not in ("erkek", "e")]

        # Karistir
        random.shuffle(erkekler)
        random.shuffle(kizlar)

        # Round-robin dagit
        sube_keys = list(subeler.keys())
        for i, s in enumerate(erkekler):
            subeler[sube_keys[i % sube_sayisi]].append(s)
        for i, s in enumerate(kizlar):
            subeler[sube_keys[i % sube_sayisi]].append(s)

        # Sonuc goster
        styled_section("Optimal Dagilim Sonucu")
        cols = st.columns(sube_sayisi)
        for idx, (sube, ogrenciler) in enumerate(subeler.items()):
            with cols[idx]:
                s_erkek = sum(1 for s in ogrenciler if s.get("cinsiyet", "").lower() in ("erkek", "e"))
                s_kiz = len(ogrenciler) - s_erkek

                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid #6366f1;border-radius:14px;
                            padding:14px;text-align:center;margin-bottom:8px;">
                    <div style="font-size:18px;font-weight:900;color:#6366f1;">{sinif}-{sube}</div>
                    <div style="font-size:24px;font-weight:800;color:#e2e8f0;margin:6px 0;">{len(ogrenciler)}</div>
                    <div style="font-size:10px;color:#94a3b8;">
                        👦 {s_erkek} erkek · 👧 {s_kiz} kiz</div>
                </div>""", unsafe_allow_html=True)

                for s in ogrenciler:
                    c_ikon = "👦" if s.get("cinsiyet", "").lower() in ("erkek", "e") else "👧"
                    st.markdown(f"<div style='font-size:11px;color:#94a3b8;padding:2px 0;'>"
                                f"{c_ikon} {s.get('ad', '')} {s.get('soyad', '')}</div>",
                                unsafe_allow_html=True)

        # Denge skoru
        boyutlar = [len(ogrenciler) for ogrenciler in subeler.values()]
        max_fark = max(boyutlar) - min(boyutlar)
        denge_skor = 100 - max_fark * 10
        d_renk = "#10b981" if denge_skor >= 80 else "#f59e0b" if denge_skor >= 60 else "#ef4444"
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid {d_renk};border-radius:14px;
                    padding:14px;text-align:center;margin-top:12px;">
            <div style="font-size:10px;color:#94a3b8;">Denge Skoru</div>
            <div style="font-size:36px;font-weight:900;color:{d_renk};">{denge_skor}</div>
            <div style="font-size:10px;color:#64748b;">Max fark: {max_fark} ogrenci</div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. ÇOCUK MUTLULUK BAROMETRESİ
# ============================================================

def _mutluluk_hesapla(bultenler: list) -> float:
    """Bultenlerden mutluluk skoru (0-100)."""
    if not bultenler:
        return 50
    mutlu = 0
    for b in bultenler:
        ruh = str(b.get("ruh_hali", b.get("duygu", b.get("genel_durum", "")))).lower()
        if any(w in ruh for w in ("iyi", "mutlu", "neseli", "harika")):
            mutlu += 1
        elif any(w in ruh for w in ("uzgun", "mutsuz", "aglamali")):
            mutlu -= 0.5
    return round(max(0, min(100, (mutlu / len(bultenler)) * 100 + 50)))


def render_mutluluk_barometresi(store):
    """Cocuk + sinif bazli mutluluk endeksi."""
    styled_section("Cocuk Mutluluk Barometresi", "#f59e0b")
    styled_info_banner(
        "Her cocugun ve tum sinifin mutluluk endeksi. "
        "Gunluk trend + haftalik analiz + AI oneri.",
        banner_type="info", icon="😊")

    ak = _ak_dir()

    col1, col2 = st.columns(2)
    with col1:
        sinif = st.selectbox("Sinif", ["Anasinifi 3 Yas", "Anasinifi 4 Yas", "Anasinifi 5 Yas",
                                         "1. Sinif", "2. Sinif", "3. Sinif", "4. Sinif"], key="mb_sinif")
    with col2:
        sube = st.selectbox("Sube", ["A", "B", "C", "D"], key="mb_sube")

    students = _lj(os.path.join(ak, "students.json"))
    sinif_ogr = [s for s in students if str(s.get("sinif", "")) == str(sinif) and s.get("sube", "") == sube
                  and s.get("durum", "aktif") == "aktif"]

    tum_bulten = _lj(os.path.join(ak, "gunluk_bulten.json")) + _lj(os.path.join(ak, "ilkokul_gunluk.json"))
    son_30g = (date.today() - timedelta(days=30)).isoformat()

    if not sinif_ogr:
        styled_info_banner("Bu sinifta ogrenci yok.", banner_type="warning", icon="👤")
        return

    # Her ogrenci icin mutluluk skoru
    ogr_skorlari = []
    for s in sinif_ogr:
        sid = s.get("id", "")
        ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
        ogr_bulten = [b for b in tum_bulten if b.get("student_id") == sid and b.get("tarih", "") >= son_30g]
        skor = _mutluluk_hesapla(ogr_bulten)
        ogr_skorlari.append({"ad": ad, "sid": sid, "skor": skor, "bulten": len(ogr_bulten)})

    # Sinif ortalamasi
    sinif_ort = round(sum(o["skor"] for o in ogr_skorlari) / max(len(ogr_skorlari), 1))
    en_mutlu = max(ogr_skorlari, key=lambda x: x["skor"]) if ogr_skorlari else {"ad": "-", "skor": 0}
    en_az = min(ogr_skorlari, key=lambda x: x["skor"]) if ogr_skorlari else {"ad": "-", "skor": 0}
    s_renk = "#10b981" if sinif_ort >= 70 else "#f59e0b" if sinif_ort >= 50 else "#ef4444"

    styled_stat_row([
        ("Sinif Mevcudu", str(len(sinif_ogr)), "#f59e0b", "👤"),
        ("Sinif Mutluluk", str(sinif_ort), s_renk, "😊"),
        ("En Mutlu", en_mutlu["ad"].split()[0] if en_mutlu["ad"] != "-" else "-", "#10b981", "🌟"),
        ("Dikkat", en_az["ad"].split()[0] if en_az["ad"] != "-" else "-", "#ef4444", "⚠️"),
    ])

    # ── HERO TERMOMETRE ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#78350f 0%,#92400e 100%);
                border:2px solid {s_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {s_renk}30;text-align:center;">
        <div style="font-size:10px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;">
            {sinif} {sube} Sinif Mutluluk Endeksi</div>
        <div style="font-size:64px;font-weight:900;color:{s_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{sinif_ort}</div>
        <div style="margin:12px auto 0;max-width:300px;">
            <div style="background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);
                        border-radius:6px;height:12px;position:relative;">
                <div style="position:absolute;left:{min(sinif_ort, 100)}%;top:-3px;transform:translateX(-50%);
                            width:4px;height:18px;background:#fff;border-radius:2px;box-shadow:0 0 8px #fff;"></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── BİREYSEL SIRALAMA ──
    styled_section("Ogrenci Mutluluk Siralamasi")
    ogr_skorlari.sort(key=lambda x: -x["skor"])
    for sira, o in enumerate(ogr_skorlari, 1):
        renk = "#10b981" if o["skor"] >= 70 else "#f59e0b" if o["skor"] >= 50 else "#ef4444"
        emoji = "😊" if o["skor"] >= 70 else "😐" if o["skor"] >= 50 else "😢"
        bar_w = min(o["skor"], 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="min-width:24px;font-size:12px;color:#94a3b8;text-align:right;">#{sira}</span>
            <span style="font-size:14px;">{emoji}</span>
            <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">{o['ad']}</span>
            <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                    <span style="font-size:9px;color:#fff;font-weight:700;">{o['skor']}</span></div></div>
            <span style="font-size:9px;color:#64748b;min-width:40px;">{o['bulten']} gn</span>
        </div>""", unsafe_allow_html=True)

    # ── HAFTALIK TREND ──
    styled_section("Haftalik Sinif Mutluluk Trendi")
    for i in range(3, -1, -1):
        h_bas = date.today() - timedelta(weeks=i, days=date.today().weekday())
        h_bit = h_bas + timedelta(days=4)
        h_bulten = [b for b in tum_bulten
                      if b.get("student_id") in [s.get("id") for s in sinif_ogr]
                      and h_bas.isoformat() <= b.get("tarih", "") <= h_bit.isoformat()]
        h_skor = _mutluluk_hesapla(h_bulten) if h_bulten else 0
        h_renk = "#10b981" if h_skor >= 70 else "#f59e0b" if h_skor >= 50 else "#ef4444"
        is_current = i == 0

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="min-width:70px;font-size:11px;color:{'#fbbf24' if is_current else '#94a3b8'};
                        font-weight:{'800' if is_current else '400'};">{'Bu Hafta' if is_current else f'{4-i} H. Once'}</span>
            <div style="flex:1;background:#1e293b;border-radius:4px;height:18px;overflow:hidden;">
                <div style="width:{min(h_skor, 100)}%;height:100%;background:{h_renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                    <span style="font-size:9px;color:#fff;font-weight:700;">{h_skor}</span></div></div>
            <span style="font-size:10px;color:#64748b;">{len(h_bulten)} blt</span>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. OKULA HAZIRLIK ENDEKSİ + GEÇİŞ RAPORU
# ============================================================

_HAZIRLIK_BOYUTLARI = [
    {"id": "bilissel", "label": "Bilissel Hazirlik", "ikon": "🧠", "agirlik": 25},
    {"id": "dil", "label": "Dil Hazirlik", "ikon": "🗣️", "agirlik": 20},
    {"id": "motor", "label": "Motor Hazirlik", "ikon": "🤸", "agirlik": 15},
    {"id": "sosyal", "label": "Sosyal Hazirlik", "ikon": "👫", "agirlik": 20},
    {"id": "oz_bakim", "label": "Oz Bakim", "ikon": "🧹", "agirlik": 10},
    {"id": "yaraticilik", "label": "Yaraticilik", "ikon": "🎨", "agirlik": 10},
]


def render_hazirlik_endeksi(store):
    """Siniftan sinifa gecis hazirlik endeksi + devir raporu."""
    styled_section("Okula Hazirlik Endeksi", "#059669")
    styled_info_banner(
        "Cocugun bir ust sinifa gecmeye ne kadar hazir oldugunu olcun. "
        "Milestone + davranis + bulten verilerinden bilesik endeks + devir raporu.",
        banner_type="info", icon="🎓")

    sel, stu_data = _ogrenci_sec(store, "hz")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    sinif = stu_data.get("sinif", "")
    ak = _ak_dir()
    td = _td()

    # Milestone verisi
    milestones = next((k for k in _lj(os.path.join(td, "akademik", "milestone_takip.json")) if k.get("student_id") == sid), None)
    ms_data = milestones.get("milestones", {}) if milestones else {}

    # Davranis DNA verisi (bultenlerden)
    tum_bulten = _lj(os.path.join(ak, "gunluk_bulten.json")) + _lj(os.path.join(ak, "ilkokul_gunluk.json"))
    ogr_bulten = [b for b in tum_bulten if b.get("student_id") == sid]

    # Her boyut icin puan hesapla
    boyut_puanlari = {}
    for boyut in _HAZIRLIK_BOYUTLARI:
        bid = boyut["id"]
        alan_ms = {k: v for k, v in ms_data.items() if k.startswith(bid)}
        if alan_ms:
            tamam = sum(1 for v in alan_ms.values() if v == "tamamlandi")
            gelisiyor = sum(1 for v in alan_ms.values() if v == "gelisiyor")
            toplam = len(alan_ms)
            puan = round((tamam * 100 + gelisiyor * 50) / max(toplam, 1))
        else:
            puan = 50  # varsayilan
        boyut_puanlari[bid] = puan

    # Bilesik hazirlik endeksi
    toplam_agirlik = sum(b["agirlik"] for b in _HAZIRLIK_BOYUTLARI)
    hazirlik = round(sum(boyut_puanlari.get(b["id"], 50) * b["agirlik"] for b in _HAZIRLIK_BOYUTLARI) / toplam_agirlik)
    h_renk = "#10b981" if hazirlik >= 75 else "#f59e0b" if hazirlik >= 50 else "#ef4444"
    h_etiket = "Hazir" if hazirlik >= 75 else "Gelisiyor" if hazirlik >= 50 else "Destek Gerekli"

    # Mutluluk skoru
    mutluluk = _mutluluk_hesapla(ogr_bulten[-30:]) if ogr_bulten else 50

    styled_stat_row([
        ("Hazirlik Endeksi", str(hazirlik), h_renk, "🎓"),
        ("Mutluluk", str(mutluluk), "#f59e0b", "😊"),
        ("Bulten Sayisi", str(len(ogr_bulten)), "#2563eb", "📝"),
        ("Milestone", str(len(ms_data)), "#7c3aed", "🧒"),
    ])

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#052e16 0%,#065f46 100%);
                border:2px solid {h_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {h_renk}30;text-align:center;">
        <div style="font-size:10px;color:#6ee7b7;letter-spacing:3px;text-transform:uppercase;">
            {ad} — Hazirlik Endeksi</div>
        <div style="font-size:64px;font-weight:900;color:{h_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{hazirlik}</div>
        <div style="background:{h_renk}20;color:{h_renk};display:inline-block;padding:4px 16px;
                    border-radius:8px;font-size:12px;font-weight:800;">{h_etiket}</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:6px;">{sinif} → Bir ust sinifa gecis</div>
    </div>""", unsafe_allow_html=True)

    # ── BOYUT BAZLI PUAN ──
    styled_section("Hazirlik Boyutlari")
    for boyut in _HAZIRLIK_BOYUTLARI:
        puan = boyut_puanlari.get(boyut["id"], 50)
        renk = "#10b981" if puan >= 75 else "#f59e0b" if puan >= 50 else "#ef4444"
        bar_w = min(puan, 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:18px;min-width:24px;">{boyut['ikon']}</span>
            <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:700;">{boyut['label']}</span>
            <div style="flex:1;background:#1e293b;border-radius:4px;height:22px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:8px;">
                    <span style="font-size:10px;color:#fff;font-weight:800;">{puan}</span></div></div>
            <span style="font-size:9px;color:#64748b;">%{boyut['agirlik']} agirlik</span>
        </div>""", unsafe_allow_html=True)

    # ── AI DEVİR RAPORU ──
    st.divider()
    styled_section("AI Gecis Raporu")
    if st.button("AI Devir Raporu Olustur", key=f"hz_ai_{sid}", type="primary", use_container_width=True):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                boyut_ozet = ", ".join(f"{b['label']}:{boyut_puanlari.get(b['id'], 50)}" for b in _HAZIRLIK_BOYUTLARI)
                ms_tamam = sum(1 for v in ms_data.values() if v == "tamamlandi")
                ms_henuz = sum(1 for v in ms_data.values() if v == "henuz")

                with st.spinner("AI devir raporu hazirlaniyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul oncesi/ilkokul gelisim uzmanisin. Cocugun gelisim verilerine dayanarak yeni ogretmene hitaben devir raporu yaz: 1) Genel degerlendirme 2) Guclu yonler 3) Gelisim alanlari 4) Oneriler 5) Dikkat edilecekler. Turkce, profesyonel."},
                            {"role": "user", "content": f"Cocuk: {ad}, Sinif: {sinif}, Yas: {stu_data.get('sinif', '')}\nHazirlik: {hazirlik}/100, Mutluluk: {mutluluk}/100\nBoyutlar: {boyut_ozet}\nMilestone: {ms_tamam} tamam, {ms_henuz} henuz\nBulten: {len(ogr_bulten)} gun kaydi"},
                        ],
                        max_tokens=600, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#052e16,#065f46);border:1px solid #059669;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#6ee7b7;font-weight:700;margin-bottom:6px;">
                            AI Devir Raporu — {ad} ({sinif})</div>
                        <div style="font-size:12px;color:#d1fae5;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
