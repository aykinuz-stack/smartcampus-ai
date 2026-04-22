"""
Okul Oncesi & Ilkokul — MEGA Ozellikleri
==========================================
1. Cocuk Dijital Gelisim Dosyasi
2. Akilli Aktivite Planlayici
3. Veli-Ogretmen Iletisim Koprusu
"""
from __future__ import annotations

import json
import os
import uuid
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


def _sj(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
# 1. ÇOCUK DİJİTAL GELİŞİM DOSYASI
# ============================================================

def render_gelisim_dosyasi(store):
    """Her cocugun tum gelisim hikayesi tek dosyada."""
    styled_section("Dijital Gelisim Dosyasi", "#7c3aed")
    styled_info_banner(
        "Cocugun okul oncesinden itibaren tum bultenler, milestone'lar, "
        "basarilar, fotoğraflar — hepsi tek dosyada.",
        banner_type="info", icon="📁")

    sel, stu_data = _ogrenci_sec(store, "gd")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    sinif = stu_data.get("sinif", "")
    ak = _ak_dir()
    td = _td()

    # Veri topla
    bultenler = [b for b in _lj(os.path.join(ak, "gunluk_bulten.json")) if b.get("student_id") == sid]
    ilkokul_r = [b for b in _lj(os.path.join(ak, "ilkokul_gunluk.json")) if b.get("student_id") == sid]
    milestones = next((k for k in _lj(os.path.join(td, "akademik", "milestone_takip.json")) if k.get("student_id") == sid), None)
    veli_fb = [v for v in _lj(os.path.join(ak, "veli_geri_bildirim.json")) if v.get("student_id") == sid]
    tum_bulten = bultenler + ilkokul_r

    # Milestone sayilari
    ms_data = milestones.get("milestones", {}) if milestones else {}
    ms_tamam = sum(1 for v in ms_data.values() if v == "tamamlandi")
    ms_gelisiyor = sum(1 for v in ms_data.values() if v == "gelisiyor")

    styled_stat_row([
        ("Toplam Bulten", str(len(tum_bulten)), "#7c3aed", "📝"),
        ("Veli Bildirim", str(len(veli_fb)), "#2563eb", "📩"),
        ("Milestone Tamam", str(ms_tamam), "#10b981", "✅"),
        ("Milestone Gelisiyor", str(ms_gelisiyor), "#f59e0b", "🔄"),
    ])

    # ── HERO DOSYA KARTI ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#312e81 0%,#4c1d95 100%);
                border:2px solid #a78bfa;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(167,139,250,0.25);text-align:center;">
        <div style="font-size:10px;color:#c4b5fd;letter-spacing:3px;text-transform:uppercase;">Dijital Gelisim Dosyasi</div>
        <div style="font-size:28px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;margin:6px 0;">{ad}</div>
        <div style="font-size:12px;color:#c4b5fd;">{sinif} · {len(tum_bulten)} gun kaydi · {ms_tamam} milestone</div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Ozet", "📅 Bulten Gecmisi", "🧒 Milestone Ozeti"])

    # ═══ ÖZET ═══
    with sub[0]:
        styled_section("Gelisim Ozeti")

        # Ruh hali trendi (son 30 bulten)
        if tum_bulten:
            ruh_sayac = Counter()
            for b in tum_bulten[-30:]:
                ruh = str(b.get("ruh_hali", b.get("duygu", b.get("genel_durum", "")))).lower()
                if "iyi" in ruh or "mutlu" in ruh:
                    ruh_sayac["Mutlu"] += 1
                elif "uzgun" in ruh or "mutsuz" in ruh:
                    ruh_sayac["Uzgun"] += 1
                else:
                    ruh_sayac["Normal"] += 1

            ruh_html = ""
            for ruh, sayi in [("Mutlu", ruh_sayac.get("Mutlu", 0)), ("Normal", ruh_sayac.get("Normal", 0)), ("Uzgun", ruh_sayac.get("Uzgun", 0))]:
                ikon = {"Mutlu": "😊", "Normal": "😐", "Uzgun": "😢"}[ruh]
                renk = {"Mutlu": "#10b981", "Normal": "#f59e0b", "Uzgun": "#ef4444"}[ruh]
                ruh_html += f'<div style="text-align:center;"><div style="font-size:24px;">{ikon}</div><div style="font-size:18px;font-weight:800;color:{renk};">{sayi}</div><div style="font-size:9px;color:#94a3b8;">{ruh}</div></div>'

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #7c3aed30;border-radius:14px;padding:16px;margin:8px 0;">
                <div style="font-size:11px;color:#c4b5fd;font-weight:700;margin-bottom:8px;">Son 30 Gun Ruh Hali</div>
                <div style="display:flex;justify-content:space-around;">{ruh_html}</div>
            </div>""", unsafe_allow_html=True)

        # Yas grubu karsilastirma
        if milestones:
            pct = round(ms_tamam / max(ms_tamam + ms_gelisiyor + sum(1 for v in ms_data.values() if v == "henuz"), 1) * 100)
            p_renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {p_renk}40;border-radius:12px;padding:14px;text-align:center;margin:8px 0;">
                <div style="font-size:36px;font-weight:900;color:{p_renk};">%{pct}</div>
                <div style="font-size:10px;color:#94a3b8;">Milestone Tamamlanma</div>
            </div>""", unsafe_allow_html=True)

    # ═══ BÜLTEN GEÇMİŞİ ═══
    with sub[1]:
        styled_section(f"Bulten Gecmisi ({len(tum_bulten)} kayit)")
        for b in sorted(tum_bulten, key=lambda x: x.get("tarih", ""), reverse=True)[:20]:
            tarih = b.get("tarih", "")[:10]
            yemek = str(b.get("yemek", b.get("beslenme", "-")))[:25]
            uyku = str(b.get("uyku", b.get("uyku_durumu", "-")))[:15]
            ruh = str(b.get("ruh_hali", b.get("duygu", b.get("genel_durum", "-"))))[:15]
            basari = str(b.get("basari", b.get("bugunku_basarisi", "-")))[:40]
            ruh_ikon = "😊" if "iyi" in ruh.lower() or "mutlu" in ruh.lower() else "😢" if "uzgun" in ruh.lower() else "😐"

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:8px 12px;margin-bottom:4px;">
                <div style="display:flex;gap:10px;align-items:center;font-size:11px;">
                    <span style="min-width:65px;color:#c4b5fd;font-weight:700;">{tarih}</span>
                    <span style="color:#94a3b8;">🍽️{yemek}</span>
                    <span style="color:#94a3b8;">😴{uyku}</span>
                    <span style="font-size:14px;">{ruh_ikon}</span>
                    <span style="color:#e2e8f0;flex:1;">{basari}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ MİLESTONE ÖZETİ ═══
    with sub[2]:
        styled_section("Milestone Durumu")
        if not milestones:
            styled_info_banner("Milestone takibi baslatilmamis. Gelisim Takip sekmesinden baslatin.", banner_type="info", icon="🧒")
        else:
            from views._ooi_zirve import _GELISIM_ALANLARI
            for alan_key, alan_info in _GELISIM_ALANLARI.items():
                alan_ms = {k: v for k, v in ms_data.items() if k.startswith(alan_key)}
                tamam = sum(1 for v in alan_ms.values() if v == "tamamlandi")
                gelisiyor = sum(1 for v in alan_ms.values() if v == "gelisiyor")
                toplam = len(alan_ms)
                if toplam == 0:
                    continue
                pct = round(tamam / toplam * 100)
                renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="font-size:16px;">{alan_info['ikon']}</span>
                    <span style="min-width:130px;font-size:12px;color:#e2e8f0;font-weight:600;">{alan_info['label']}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:8px;color:#fff;font-weight:700;">{tamam}/{toplam}</span></div></div>
                    <span style="font-size:10px;color:{renk};font-weight:700;">%{pct}</span>
                </div>""", unsafe_allow_html=True)


# ============================================================
# 2. AKILLI AKTİVİTE PLANLAYICI
# ============================================================

_AKTIVITELER = {
    "bilissel": [
        {"ad": "Hafiza Kartlari", "sure": "15 dk", "malzeme": "Resimli kartlar", "yas": "3-5"},
        {"ad": "Siralama Oyunu", "sure": "10 dk", "malzeme": "Renkli bloklar", "yas": "3-5"},
        {"ad": "Puzzle Yarisması", "sure": "20 dk", "malzeme": "Puzzle (50 parca)", "yas": "4-6"},
        {"ad": "Sayı Bulmaca", "sure": "15 dk", "malzeme": "Calisma kagidi", "yas": "5-7"},
        {"ad": "Kodlama Oyunu", "sure": "20 dk", "malzeme": "Bee-Bot / floor robot", "yas": "5-7"},
    ],
    "dil": [
        {"ad": "Hikaye Tamamlama", "sure": "15 dk", "malzeme": "Hikaye baslangic kartlari", "yas": "3-5"},
        {"ad": "Resim Bakip Anlatma", "sure": "10 dk", "malzeme": "Buyuk resimler", "yas": "3-5"},
        {"ad": "Kelime Avı", "sure": "15 dk", "malzeme": "Harf kartlari", "yas": "5-7"},
        {"ad": "Sarki Soyleme", "sure": "10 dk", "malzeme": "Muzik", "yas": "3-7"},
        {"ad": "Siir Ezberleme", "sure": "15 dk", "malzeme": "Siir kitabi", "yas": "5-7"},
    ],
    "motor": [
        {"ad": "Hamur ile Sekil Yapma", "sure": "20 dk", "malzeme": "Oyun hamuru", "yas": "3-5"},
        {"ad": "Makasla Kesme", "sure": "15 dk", "malzeme": "Makas + kagit", "yas": "4-6"},
        {"ad": "Engel Parkuru", "sure": "20 dk", "malzeme": "Sinif malzemeleri", "yas": "3-5"},
        {"ad": "Ip Atlama", "sure": "15 dk", "malzeme": "Atlama ipi", "yas": "5-7"},
        {"ad": "Boncuk Dizme", "sure": "15 dk", "malzeme": "Boncuk + ip", "yas": "3-6"},
    ],
    "sosyal": [
        {"ad": "Ikili Eslestirme Oyunu", "sure": "15 dk", "malzeme": "Esleme kartlari", "yas": "3-5"},
        {"ad": "Grup Puzzle", "sure": "20 dk", "malzeme": "Buyuk puzzle", "yas": "4-7"},
        {"ad": "Drama / Rol Yapma", "sure": "20 dk", "malzeme": "Kostum / aksesuar", "yas": "4-7"},
        {"ad": "Paylaşma Cemberi", "sure": "15 dk", "malzeme": "Yok", "yas": "3-5"},
        {"ad": "Takim Yarismasi", "sure": "20 dk", "malzeme": "Cesitli", "yas": "5-7"},
    ],
    "yaraticilik": [
        {"ad": "Parmak Boyasi", "sure": "20 dk", "malzeme": "Boya + kagit", "yas": "3-5"},
        {"ad": "Kolaj Yapma", "sure": "20 dk", "malzeme": "Dergi + makas + yapistirici", "yas": "4-7"},
        {"ad": "Muzik Ritim", "sure": "15 dk", "malzeme": "Ritim aletleri", "yas": "3-7"},
        {"ad": "Serbest Resim", "sure": "20 dk", "malzeme": "Boya + kagit", "yas": "3-7"},
        {"ad": "Origami", "sure": "20 dk", "malzeme": "Origami kagidi", "yas": "5-7"},
    ],
    "oz_bakim": [
        {"ad": "El Yikama Yarismasi", "sure": "10 dk", "malzeme": "Sabun + su", "yas": "3-5"},
        {"ad": "Giyinme Yarisi", "sure": "10 dk", "malzeme": "Kiyafetler", "yas": "3-5"},
        {"ad": "Sofra Hazirlama", "sure": "15 dk", "malzeme": "Tabak + bardak", "yas": "4-6"},
        {"ad": "Canta Hazirlama", "sure": "10 dk", "malzeme": "Okul cantasi", "yas": "5-7"},
        {"ad": "Oda Toplama Oyunu", "sure": "15 dk", "malzeme": "Sinif malzemeleri", "yas": "4-7"},
    ],
}


def render_aktivite_planlayici(store):
    """AI ile kisiye ozel gunluk aktivite onerisi."""
    styled_section("Akilli Aktivite Planlayici", "#ea580c")
    styled_info_banner(
        "Cocugun gelisim profiline gore kisisellestirilmis aktivite onerin. "
        "Zayif alanlara yonelik oyun + guclu alanlari besleyen challenge.",
        banner_type="info", icon="🎮")

    sel, stu_data = _ogrenci_sec(store, "akt")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    td = _td()

    # Milestone verisi
    milestones = next((k for k in _lj(os.path.join(td, "akademik", "milestone_takip.json")) if k.get("student_id") == sid), None)

    sub = st.tabs(["🎯 Kisisel Oneri", "📅 Haftalik Plan", "📋 Aktivite Katalogu"])

    # ═══ KİŞİSEL ÖNERİ ═══
    with sub[0]:
        styled_section(f"{ad} — Kisisel Aktivite Onerisi")

        if milestones:
            ms_data = milestones.get("milestones", {})
            # Zayif alanlar (en cok "henuz" olan)
            alan_zayiflik = {}
            from views._ooi_zirve import _GELISIM_ALANLARI
            for alan_key in _GELISIM_ALANLARI:
                alan_ms = {k: v for k, v in ms_data.items() if k.startswith(alan_key)}
                if alan_ms:
                    henuz = sum(1 for v in alan_ms.values() if v == "henuz")
                    alan_zayiflik[alan_key] = henuz

            zayiflar = sorted(alan_zayiflik.items(), key=lambda x: -x[1])[:2]
            gucluler = sorted(alan_zayiflik.items(), key=lambda x: x[1])[:1]

            if zayiflar:
                styled_section("Zayif Alanlara Yonelik Aktiviteler", "#ef4444")
                for alan_key, _ in zayiflar:
                    alan_info = _GELISIM_ALANLARI.get(alan_key, {})
                    aktiviteler = _AKTIVITELER.get(alan_key, [])
                    if aktiviteler:
                        st.markdown(f"**{alan_info.get('ikon', '')} {alan_info.get('label', alan_key)}** (gelisim onceligi)")
                        for akt in aktiviteler[:3]:
                            st.markdown(f"""
                            <div style="background:#0f172a;border:1px solid #ea580c30;border-left:3px solid #ea580c;
                                        border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:4px;">
                                <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{akt['ad']}</span>
                                <span style="color:#94a3b8;font-size:10px;margin-left:8px;">
                                    ⏱️{akt['sure']} · 🧸{akt['malzeme']} · 👶{akt['yas']}</span>
                            </div>""", unsafe_allow_html=True)

            if gucluler:
                styled_section("Guclu Alan Challenge", "#10b981")
                for alan_key, _ in gucluler:
                    alan_info = _GELISIM_ALANLARI.get(alan_key, {})
                    aktiviteler = _AKTIVITELER.get(alan_key, [])
                    if aktiviteler:
                        st.markdown(f"**{alan_info.get('ikon', '')} {alan_info.get('label', alan_key)}** (ileri seviye)")
                        akt = aktiviteler[-1]  # Son (en zor) aktivite
                        st.markdown(f"""
                        <div style="background:#052e16;border:1px solid #10b981;border-left:3px solid #10b981;
                                    border-radius:0 8px 8px 0;padding:8px 12px;">
                            <span style="font-weight:700;color:#6ee7b7;font-size:12px;">🏆 {akt['ad']}</span>
                            <span style="color:#94a3b8;font-size:10px;margin-left:8px;">
                                ⏱️{akt['sure']} · 🧸{akt['malzeme']}</span>
                        </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Kisisel oneri icin once Gelisim Takip sekmesinden milestone girin.", banner_type="warning", icon="🧒")
            # Genel oneri
            styled_section("Genel Aktivite Onerileri")
            import random
            for alan_key in list(_AKTIVITELER.keys())[:3]:
                akt = random.choice(_AKTIVITELER[alan_key])
                from views._ooi_zirve import _GELISIM_ALANLARI
                alan_info = _GELISIM_ALANLARI.get(alan_key, {})
                st.markdown(f"- {alan_info.get('ikon', '')} **{akt['ad']}** — {akt['sure']} · {akt['malzeme']}")

    # ═══ HAFTALIK PLAN ═══
    with sub[1]:
        styled_section("AI Haftalik Aktivite Plani")
        if st.button("AI ile Haftalik Plan Olustur", key=f"akt_ai_{sid}", type="primary"):
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    ms_ozet = ""
                    if milestones:
                        ms_data = milestones.get("milestones", {})
                        henuz_list = [k.split("_", 1)[1] if "_" in k else k for k, v in ms_data.items() if v == "henuz"][:10]
                        ms_ozet = f"Henuz kazanilmamis beceriler: {', '.join(henuz_list)}"

                    with st.spinner("AI plan olusturuyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir okul oncesi egitim uzmanisin. Cocugun gelisim durumuna gore Pazartesi-Cuma 5 gunluk aktivite plani olustur. Her gun 2 aktivite (1 zayif alan + 1 guclu alan). Aktivite adi, sure, malzeme belirt. Turkce."},
                                {"role": "user", "content": f"Cocuk: {ad}, Sinif: {stu_data.get('sinif', '')}\n{ms_ozet or 'Milestone verisi yok — genel plan olustur'}"},
                            ],
                            max_tokens=600, temperature=0.8,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#431407,#7c2d12);border:1px solid #ea580c;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#fdba74;font-weight:700;margin-bottom:6px;">AI Haftalik Plan — {ad}</div>
                            <div style="font-size:12px;color:#fed7aa;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")

    # ═══ AKTİVİTE KATALOĞU ═══
    with sub[2]:
        styled_section("Aktivite Katalogu (30+ Aktivite)")
        from views._ooi_zirve import _GELISIM_ALANLARI
        for alan_key, aktiviteler in _AKTIVITELER.items():
            alan_info = _GELISIM_ALANLARI.get(alan_key, {"label": alan_key, "ikon": "📋", "renk": "#64748b"})
            with st.expander(f"{alan_info['ikon']} {alan_info['label']} ({len(aktiviteler)} aktivite)", expanded=False):
                for akt in aktiviteler:
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;align-items:center;padding:4px 0;border-bottom:1px solid #1e293b;">
                        <span style="flex:1;font-size:12px;color:#e2e8f0;font-weight:600;">{akt['ad']}</span>
                        <span style="font-size:10px;color:#94a3b8;">⏱️{akt['sure']}</span>
                        <span style="font-size:10px;color:#94a3b8;">🧸{akt['malzeme'][:20]}</span>
                        <span style="font-size:10px;color:#64748b;">👶{akt['yas']}</span>
                    </div>""", unsafe_allow_html=True)


# ============================================================
# 3. VELİ-ÖĞRETMEN İLETİŞİM KÖPRÜSÜ
# ============================================================

def _kopru_path() -> str:
    return os.path.join(_td(), "akademik", "veli_kopru_mesaj.json")


def render_veli_koprusu(store):
    """Veli-ogretmen cocuk odakli iletisim platformu."""
    styled_section("Veli-Ogretmen Koprusu", "#059669")
    styled_info_banner(
        "Cocuk odakli yapilandirilmis iletisim. "
        "Ogretmen bulten girer → veli bildirim alir. Veli geri bildirim girer → ogretmen gorur.",
        banner_type="info", icon="🌉")

    sel, stu_data = _ogrenci_sec(store, "vk")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    ak = _ak_dir()

    mesajlar = _lj(_kopru_path())
    ogr_mesajlar = [m for m in mesajlar if m.get("student_id") == sid]

    sub = st.tabs(["💬 Mesajlar", "📤 Yeni Mesaj", "📋 Sablon Mesajlar"])

    # ═══ MESAJLAR ═══
    with sub[0]:
        styled_section(f"{ad} — Iletisim Gecmisi")
        if not ogr_mesajlar:
            styled_info_banner("Henuz mesaj yok.", banner_type="info", icon="💬")
        else:
            for m in sorted(ogr_mesajlar, key=lambda x: x.get("tarih", ""), reverse=True)[:20]:
                yon = m.get("yon", "ogretmen")
                yon_renk = "#059669" if yon == "ogretmen" else "#7c3aed"
                yon_ikon = "👨‍🏫" if yon == "ogretmen" else "👪"
                yon_label = "Ogretmen" if yon == "ogretmen" else "Veli"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {yon_renk}30;border-left:4px solid {yon_renk};
                            border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;
                            {'margin-left:30px;' if yon == 'veli' else ''}">
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;margin-bottom:4px;">
                        <span>{yon_ikon} {yon_label} · {m.get('gonderen', '-')}</span>
                        <span>{m.get('tarih', '')[:10]} {m.get('saat', '')}</span>
                    </div>
                    <div style="font-size:12px;color:#e2e8f0;">{m.get('mesaj', '')}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ YENİ MESAJ ═══
    with sub[1]:
        styled_section("Yeni Mesaj Gonder")
        with st.form("kopru_mesaj_form"):
            yon = st.radio("Gonderen", ["Ogretmen", "Veli"], horizontal=True, key="vk_yon")
            gonderen = st.text_input("Ad Soyad", key="vk_gonderen")
            kategori = st.selectbox("Kategori", ["Genel", "Basari", "Uyari", "Bilgi", "Acil", "Fotograf"], key="vk_kat")
            mesaj = st.text_area("Mesaj", key="vk_mesaj", height=80)

            if st.form_submit_button("Gonder", type="primary"):
                if mesaj.strip():
                    yeni = {
                        "id": f"vkm_{uuid.uuid4().hex[:8]}",
                        "student_id": sid, "ogrenci_adi": ad,
                        "yon": "ogretmen" if yon == "Ogretmen" else "veli",
                        "gonderen": gonderen, "kategori": kategori,
                        "mesaj": mesaj.strip(),
                        "tarih": date.today().isoformat(),
                        "saat": datetime.now().strftime("%H:%M"),
                    }
                    mesajlar.append(yeni)
                    _sj(_kopru_path(), mesajlar)
                    st.success(f"Mesaj gonderildi: {ad}")
                    st.rerun()

    # ═══ ŞABLON MESAJLAR ═══
    with sub[2]:
        styled_section("Hazir Mesaj Sablonlari")
        sablonlar = [
            {"ikon": "😊", "baslik": "Harika Gun", "mesaj": f"{ad} bugun harika bir gun gecirdi! Etkinliklere aktif katildi ve arkadaslariyla guzel vakit gecirdi."},
            {"ikon": "🏆", "baslik": "Yeni Basari", "mesaj": f"{ad} bugun yeni bir beceri ogrendi! Evde de desteklemenizi oneririz."},
            {"ikon": "😐", "baslik": "Biraz Keyifsiz", "mesaj": f"{ad} bugun biraz keyifsizdi. Evde ilgilenmenizi ve nedenini konusmanizi oneririz."},
            {"ikon": "🍽️", "baslik": "Beslenme Notu", "mesaj": f"{ad} bugun oglen yemegini az yedi. Evde beslenme duzenini kontrol etmenizi oneririz."},
            {"ikon": "⚠️", "baslik": "Dikkat Gerektiren", "mesaj": f"{ad} ile ilgili sizinle konusmamiz gereken bir konu var. Lutfen bize ulasın."},
            {"ikon": "📅", "baslik": "Etkinlik Hatirlatma", "mesaj": f"Yarin okul etkinligimiz var. {ad}'in [malzeme/kiyafet] getirmesini rica ederiz."},
        ]

        for s in sablonlar:
            with st.expander(f"{s['ikon']} {s['baslik']}"):
                st.text_area(f"Sablon — {s['baslik']}", value=s["mesaj"], height=60, key=f"vk_sab_{s['baslik']}")
                st.caption("Kopyalayip 'Yeni Mesaj' sekmesine yapistirabilirsiniz.")
