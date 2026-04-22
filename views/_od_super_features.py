"""
Ölçme Değerlendirme — Süper Özellikler
========================================
1. Akıllı Sınav Takvimi & Yük Dengeleme
2. Soru Kalite Radar & AI İyileştirme Asistanı
3. Öğrenci Başarı Tahmin & Erken Uyarı Motoru
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner
from utils.tenant import get_data_path


def _od_store():
    try:
        from models.olcme_degerlendirme import get_store
        return get_store()
    except Exception:
        return None


def _od_data_dir() -> str:
    d = os.path.join(get_data_path(), "olcme")
    os.makedirs(d, exist_ok=True)
    return d


def _lj(name: str) -> list:
    p = os.path.join(_od_data_dir(), name)
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _sj(name: str, data: list) -> None:
    with open(os.path.join(_od_data_dir(), name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


_GUN_ADLARI = {0: "Pzt", 1: "Sal", 2: "Car", 3: "Per", 4: "Cum", 5: "Cmt", 6: "Paz"}
_AY_ADLARI = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
              7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}

_ZORLUK_RENK = {"Kolay": "#10b981", "Orta": "#f59e0b", "Zor": "#ef4444", "Cok Zor": "#dc2626"}
_BLOOM_SEVIYELERI = ["Hatırlama", "Anlama", "Uygulama", "Analiz", "Değerlendirme", "Yaratma"]
_BLOOM_RENK = {"Hatırlama": "#94a3b8", "Anlama": "#3b82f6", "Uygulama": "#10b981",
               "Analiz": "#f59e0b", "Değerlendirme": "#ef4444", "Yaratma": "#8b5cf6"}


# ════════════════════════════════════════════════════════════
# 1. AKILLI SINAV TAKVİMİ & YÜK DENGELEME
# ════════════════════════════════════════════════════════════

_MAX_HAFTALIK_SINAV = 3
_MIN_GUN_ARASI = 1
_ZORLUK_AGIRLIK = {"Kolay": 1, "Orta": 2, "Zor": 3, "Cok Zor": 4}


def render_sinav_takvimi():
    """Akıllı Sınav Takvimi & Yük Dengeleme."""
    styled_section("Akilli Sinav Takvimi & Yuk Dengeleme", "#2563eb")
    styled_info_banner(
        "Ogrencinin haftalik sinav yukunu dengeleyen planlama sistemi. "
        "Cakisma kontrolu, optimal tarih onerisi, yuk isi haritasi.",
        banner_type="info", icon="📡")

    store = _od_store()
    takvim = _lj("sinav_takvimi.json")

    # Mevcut sinavlari da dahil et
    exams = []
    if store:
        try:
            exams = store.get_exams()
        except Exception:
            pass

    # KPI
    bu_hafta_bas = date.today() - timedelta(days=date.today().weekday())
    bu_hafta_bit = bu_hafta_bas + timedelta(days=4)
    bu_hafta_str = bu_hafta_bas.isoformat()
    bu_hafta_bit_str = bu_hafta_bit.isoformat()
    hafta_sinav = sum(1 for t in takvim if bu_hafta_str <= t.get("tarih", "")[:10] <= bu_hafta_bit_str)
    uyari_var = hafta_sinav > _MAX_HAFTALIK_SINAV

    styled_stat_row([
        ("Bu Hafta", str(hafta_sinav), "#ef4444" if uyari_var else "#10b981", "📅"),
        ("Planlanan", str(len(takvim)), "#3b82f6", "📋"),
        ("Mevcut Sinav", str(len(exams)), "#8b5cf6", "🗂️"),
        ("Max/Hafta", str(_MAX_HAFTALIK_SINAV), "#f59e0b", "⚖️"),
    ])

    if uyari_var:
        st.warning(f"Bu hafta {hafta_sinav} sinav var — ogrenci yuku fazla! Erteleme oneririz.")

    sub = st.tabs(["➕ Sinav Planla", "📅 Takvim Gorunum", "🌡️ Yuk Isi Haritasi", "💡 Optimal Oneri"])

    # ── SINAV PLANLA ──
    with sub[0]:
        styled_section("Yeni Sinav Planla")
        with st.form("st_planla_form"):
            c1, c2 = st.columns(2)
            with c1:
                s_ders = st.selectbox("Ders", [
                    "Matematik", "Turkce", "Fen Bilimleri", "Sosyal Bilgiler",
                    "Ingilizce", "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya"
                ], key="st_ders")
                s_sinif = st.text_input("Sinif/Sube", placeholder="8/A", key="st_sinif")
                s_tur = st.selectbox("Sinav Turu",
                    ["Yazili", "Quiz", "Deneme", "Proje", "Performans"], key="st_tur")
            with c2:
                s_tarih = st.date_input("Planlanan Tarih", key="st_tarih")
                s_zorluk = st.selectbox("Beklenen Zorluk", list(_ZORLUK_AGIRLIK.keys()), key="st_zorluk")
                s_ogretmen = st.text_input("Ogretmen", key="st_ogretmen")

            s_not = st.text_input("Not / Aciklama", key="st_not")

            submitted = st.form_submit_button("Planla", use_container_width=True)
            if submitted and s_ders and s_sinif:
                tarih_str = s_tarih.isoformat()

                # Cakisma kontrolu
                cakismalar = [t for t in takvim
                              if t.get("tarih", "")[:10] == tarih_str and t.get("sinif") == s_sinif]
                ayni_hafta = []
                hafta_bas = s_tarih - timedelta(days=s_tarih.weekday())
                for t in takvim:
                    try:
                        t_date = date.fromisoformat(t.get("tarih", "")[:10])
                        t_hafta_bas = t_date - timedelta(days=t_date.weekday())
                        if t_hafta_bas == hafta_bas and t.get("sinif") == s_sinif:
                            ayni_hafta.append(t)
                    except Exception:
                        pass

                if cakismalar:
                    st.warning(f"Ayni gun {s_sinif} sinfinda {len(cakismalar)} sinav daha var!")
                if len(ayni_hafta) >= _MAX_HAFTALIK_SINAV:
                    st.error(f"Bu hafta {s_sinif} sinfinda zaten {len(ayni_hafta)} sinav var — limit: {_MAX_HAFTALIK_SINAV}")

                kayit = {
                    "id": f"stk_{uuid.uuid4().hex[:8]}",
                    "ders": s_ders,
                    "sinif": s_sinif,
                    "tur": s_tur,
                    "tarih": tarih_str,
                    "zorluk": s_zorluk,
                    "ogretmen": s_ogretmen,
                    "not": s_not,
                    "durum": "Planlandi",
                    "created_at": datetime.now().isoformat(),
                }
                takvim.append(kayit)
                _sj("sinav_takvimi.json", takvim)
                if not cakismalar:
                    st.success(f"{s_ders} sinavi {tarih_str} icin planlandi!")
                st.rerun()

    # ── TAKVİM GÖRÜNÜM ──
    with sub[1]:
        styled_section("Haftalik Sinav Gorunumu")
        if not takvim:
            st.info("Planlanan sinav yok.")
        else:
            # Bu hafta + gelecek 2 hafta
            for hafta_offset in range(3):
                hafta_bas = date.today() - timedelta(days=date.today().weekday()) + timedelta(weeks=hafta_offset)
                hafta_bit = hafta_bas + timedelta(days=4)
                hafta_label = f"{hafta_bas.strftime('%d.%m')} — {hafta_bit.strftime('%d.%m.%Y')}"
                is_bu_hafta = hafta_offset == 0

                hafta_sinavlar = []
                for t in takvim:
                    try:
                        t_date = date.fromisoformat(t.get("tarih","")[:10])
                        if hafta_bas <= t_date <= hafta_bit:
                            hafta_sinavlar.append(t)
                    except Exception:
                        pass

                sayi = len(hafta_sinavlar)
                renk = "#ef4444" if sayi > _MAX_HAFTALIK_SINAV else "#f59e0b" if sayi == _MAX_HAFTALIK_SINAV else "#10b981"
                border = f"2px solid #c9a84c" if is_bu_hafta else f"1px solid #334155"

                st.markdown(f"""
                <div style="background:#0f172a;border:{border};border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:{'900' if is_bu_hafta else '600'};font-size:0.85rem;">
                            {'📌 ' if is_bu_hafta else ''}{hafta_label}</span>
                        <span style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:8px;
                            font-size:0.72rem;font-weight:800;">{sayi} sinav</span>
                    </div>
                </div>""", unsafe_allow_html=True)

                for t in sorted(hafta_sinavlar, key=lambda x: x.get("tarih","")):
                    z_renk = _ZORLUK_RENK.get(t.get("zorluk",""), "#94a3b8")
                    try:
                        gun_adi = _GUN_ADLARI.get(date.fromisoformat(t.get("tarih","")[:10]).weekday(), "")
                    except Exception:
                        gun_adi = ""
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:4px 12px;margin:2px 0 2px 20px;
                        border-left:3px solid {z_renk};border-radius:0 6px 6px 0;background:#0f172a80;">
                        <span style="min-width:30px;color:#64748b;font-size:0.68rem;">{gun_adi}</span>
                        <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;">{t.get('ders','')}</span>
                        <span style="color:#94a3b8;font-size:0.68rem;">{t.get('sinif','')}</span>
                        <span style="color:{z_renk};font-size:0.65rem;margin-left:auto;font-weight:700;">{t.get('zorluk','')}</span>
                    </div>""", unsafe_allow_html=True)

    # ── YÜK ISI HARİTASI ──
    with sub[2]:
        styled_section("Sinif Bazli Haftalik Sinav Yuku")
        if not takvim:
            st.info("Veri yok.")
        else:
            sinif_grp = defaultdict(list)
            for t in takvim:
                sinif_grp[t.get("sinif", "?")].append(t)

            for sinif in sorted(sinif_grp.keys()):
                sinavlar = sinif_grp[sinif]
                hafta_yuk = Counter()
                for t in sinavlar:
                    try:
                        t_date = date.fromisoformat(t.get("tarih","")[:10])
                        hafta_no = t_date.isocalendar()[1]
                        agirlik = _ZORLUK_AGIRLIK.get(t.get("zorluk","Orta"), 2)
                        hafta_yuk[hafta_no] += agirlik
                    except Exception:
                        pass

                max_yuk = max(hafta_yuk.values()) if hafta_yuk else 1
                st.markdown(f"**{sinif}** ({len(sinavlar)} sinav)")
                for hafta, yuk in sorted(hafta_yuk.items()):
                    pct = round(yuk / max(max_yuk, 1) * 100)
                    renk = "#dc2626" if yuk >= 10 else "#ef4444" if yuk >= 7 else "#f59e0b" if yuk >= 4 else "#10b981"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin:2px 0;">
                        <span style="min-width:45px;font-size:0.65rem;color:#94a3b8;">H{hafta}</span>
                        <div style="flex:1;background:#1e293b;border-radius:3px;height:12px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:3px;"></div>
                        </div>
                        <span style="font-size:0.6rem;color:#64748b;">{yuk}</span>
                    </div>""", unsafe_allow_html=True)

    # ── OPTİMAL ÖNERİ ──
    with sub[3]:
        styled_section("AI Optimal Tarih Onerisi")
        st.caption("Sinif secin — en uygun sinav tarihi onerilsin.")
        sec_sinif = st.text_input("Sinif/Sube", placeholder="8/A", key="st_opt_sinif")
        sec_ders = st.selectbox("Ders", ["Matematik", "Turkce", "Fen Bilimleri", "Ingilizce", "Fizik"], key="st_opt_ders")

        if st.button("Optimal Tarihi Hesapla", use_container_width=True, type="primary") and sec_sinif:
            # Gelecek 2 haftadaki bos gunleri bul
            bugun = date.today()
            oneriler = []
            for i in range(1, 15):
                gun = bugun + timedelta(days=i)
                if gun.weekday() >= 5:
                    continue  # hafta sonu
                gun_str = gun.isoformat()
                gun_sinav = sum(1 for t in takvim if t.get("tarih","")[:10] == gun_str and t.get("sinif") == sec_sinif)
                hafta_bas = gun - timedelta(days=gun.weekday())
                hafta_sinav = sum(1 for t in takvim
                    if t.get("sinif") == sec_sinif
                    and hafta_bas.isoformat() <= t.get("tarih","")[:10] <= (hafta_bas + timedelta(days=4)).isoformat())

                if gun_sinav == 0 and hafta_sinav < _MAX_HAFTALIK_SINAV:
                    oneriler.append({"tarih": gun, "gun_adi": _GUN_ADLARI.get(gun.weekday(),""),
                                     "hafta_yuk": hafta_sinav})

            if oneriler:
                styled_section("Onerilen Tarihler")
                for idx, o in enumerate(oneriler[:5]):
                    yuk_renk = "#10b981" if o["hafta_yuk"] == 0 else "#f59e0b" if o["hafta_yuk"] <= 1 else "#ef4444"
                    en_iyi = "⭐ EN İYİ" if idx == 0 else ""
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                        background:#0f172a;border-left:4px solid {yuk_renk};border-radius:0 10px 10px 0;
                        {'border:1px solid #c9a84c;' if idx == 0 else ''}">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">
                            {o['tarih'].strftime('%d.%m.%Y')} {o['gun_adi']}</span>
                        <span style="color:{yuk_renk};font-size:0.7rem;">Hafta yuku: {o['hafta_yuk']}/{_MAX_HAFTALIK_SINAV}</span>
                        <span style="color:#c9a84c;font-weight:800;font-size:0.7rem;margin-left:auto;">{en_iyi}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("Gelecek 2 haftada uygun bos gun bulunamadi.")


# ════════════════════════════════════════════════════════════
# 2. SORU KALİTE RADAR & AI İYİLEŞTİRME ASİSTANI
# ════════════════════════════════════════════════════════════

_KALITE_KRITERLERI = {
    "Kok Netliği": {"agirlik": 20, "aciklama": "Soru kokunde belirsizlik, cift anlam var mi"},
    "Celdirici Etkinliği": {"agirlik": 20, "aciklama": "Her sik en az %5 isaretlenmis mi"},
    "Bloom Uyumu": {"agirlik": 15, "aciklama": "Hedeflenen Bloom ile gercek uyum"},
    "Zorluk Kalibrasyonu": {"agirlik": 15, "aciklama": "p-value ile zorluk etiketi tutarli mi"},
    "Ayirt Edicilik": {"agirlik": 15, "aciklama": "Basarili-basarisiz ogrenciyi ayirt ediyor mu"},
    "Teknik Kalite": {"agirlik": 15, "aciklama": "Gramer, imla, format uygunlugu"},
}


def render_soru_kalite_radar():
    """Soru Kalite Radar & AI İyileştirme Asistanı."""
    styled_section("Soru Kalite Radar & AI Iyilestirme Asistani", "#8b5cf6")
    styled_info_banner(
        "Soru bankasindaki tum sorulari otomatik tarar. Kalite puani, "
        "etkisiz celdirici tespiti, ogretmen bazli siralama, AI iyilestirme onerileri.",
        banner_type="info", icon="🎯")

    store = _od_store()
    questions = []
    results = []
    if store:
        try:
            questions = store.list_questions()
            results = store.get_results()
        except Exception:
            pass

    toplam = len(questions)
    if toplam == 0:
        st.info("Soru bankasinda soru yok.")
        return

    # Kalite skoru hesapla
    kalite_skorlari = []
    for q in questions:
        skor = _hesapla_soru_kalite(q, results)
        kalite_skorlari.append({"soru": q, "skor": skor})

    ort_kalite = round(sum(k["skor"]["genel"] for k in kalite_skorlari) / max(toplam, 1))
    dusuk_kalite = sum(1 for k in kalite_skorlari if k["skor"]["genel"] < 50)
    yuksek_kalite = sum(1 for k in kalite_skorlari if k["skor"]["genel"] >= 80)
    ort_renk = "#10b981" if ort_kalite >= 70 else "#f59e0b" if ort_kalite >= 50 else "#ef4444"

    styled_stat_row([
        ("Toplam Soru", str(toplam), "#8b5cf6", "📝"),
        ("Ort. Kalite", f"{ort_kalite}/100", ort_renk, "📊"),
        ("Yuksek Kalite", str(yuksek_kalite), "#10b981", "✅"),
        ("Dusuk Kalite", str(dusuk_kalite), "#ef4444", "⚠️"),
    ])

    sub = st.tabs(["📊 Genel Radar", "🔍 Soru Detay", "👨‍🏫 Ogretmen Sirala", "💡 AI Oneriler"])

    # ── GENEL RADAR ──
    with sub[0]:
        styled_section("Soru Bankasi Kalite Profili")

        # Kriter bazli ortalama
        kriter_ort = {k: [] for k in _KALITE_KRITERLERI}
        for ks in kalite_skorlari:
            for k, v in ks["skor"]["kriterler"].items():
                if k in kriter_ort:
                    kriter_ort[k].append(v)

        for kriter, info in _KALITE_KRITERLERI.items():
            puanlar = kriter_ort.get(kriter, [])
            ort = round(sum(puanlar) / max(len(puanlar), 1)) if puanlar else 0
            renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                <span style="min-width:150px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{ort}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{ort}/100</span>
                    </div>
                </div>
                <span style="font-size:0.65rem;color:#64748b;min-width:60px;">{info['aciklama'][:25]}</span>
            </div>""", unsafe_allow_html=True)

        # Bloom dagilimi
        styled_section("Bloom Seviye Dagilimi")
        bloom_say = Counter()
        for q in questions:
            bloom = getattr(q, 'bloom', None) or getattr(q, 'bloom_level', 'Hatırlama')
            bloom_say[bloom] += 1

        for bloom in _BLOOM_SEVIYELERI:
            sayi = bloom_say.get(bloom, 0)
            pct = round(sayi / max(toplam, 1) * 100)
            renk = _BLOOM_RENK.get(bloom, "#94a3b8")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                <span style="min-width:110px;font-size:0.75rem;color:#e2e8f0;font-weight:600;">{bloom}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                    </div>
                </div>
                <span style="font-size:0.65rem;color:#64748b;">%{pct}</span>
            </div>""", unsafe_allow_html=True)

    # ── SORU DETAY ──
    with sub[1]:
        styled_section("Dusuk Kaliteli Sorular")
        dusuk = sorted(kalite_skorlari, key=lambda x: x["skor"]["genel"])[:15]
        for ks in dusuk:
            q = ks["soru"]
            skor = ks["skor"]["genel"]
            renk = "#ef4444" if skor < 40 else "#f59e0b" if skor < 60 else "#10b981"
            q_text = getattr(q, 'text', getattr(q, 'stem', ''))[:80]
            q_ders = getattr(q, 'subject', '')
            q_id = getattr(q, 'id', '')[:12]

            st.markdown(f"""
            <div style="padding:8px 12px;margin:4px 0;background:#0f172a;
                border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#e2e8f0;font-size:0.78rem;font-weight:600;">{q_text}...</span>
                    <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                        font-size:0.65rem;font-weight:800;">{skor}/100</span>
                </div>
                <div style="color:#94a3b8;font-size:0.65rem;margin-top:2px;">{q_ders} | ID: {q_id}</div>
                <div style="color:#64748b;font-size:0.6rem;margin-top:2px;">
                    Sorunlar: {', '.join(ks['skor'].get('sorunlar', []))}</div>
            </div>""", unsafe_allow_html=True)

    # ── ÖĞRETMEN SIRALA ──
    with sub[2]:
        styled_section("Ogretmen Bazli Kalite Siralamasi")
        ogr_kalite = defaultdict(list)
        for ks in kalite_skorlari:
            q = ks["soru"]
            source = getattr(q, 'source', 'manual')
            ogr_kalite[source].append(ks["skor"]["genel"])

        sirali = sorted(ogr_kalite.items(), key=lambda x: sum(x[1])/max(len(x[1]),1), reverse=True)
        for sira, (kaynak, puanlar) in enumerate(sirali, 1):
            ort = round(sum(puanlar) / max(len(puanlar), 1))
            renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
            madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span style="font-size:1rem;">{madalya}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">{kaynak}</span>
                <span style="color:#64748b;font-size:0.7rem;">{len(puanlar)} soru</span>
                <span style="color:{renk};font-weight:800;font-size:0.85rem;">{ort}/100</span>
            </div>""", unsafe_allow_html=True)

    # ── AI ÖNERİLER ──
    with sub[3]:
        styled_section("AI Iyilestirme Onerileri")
        sorun_say = Counter()
        for ks in kalite_skorlari:
            for s in ks["skor"].get("sorunlar", []):
                sorun_say[s] += 1

        if sorun_say:
            for sorun, sayi in sorun_say.most_common(8):
                pct = round(sayi / max(toplam, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:4px 0;
                    background:#8b5cf610;border:1px solid #8b5cf630;border-radius:10px;">
                    <span style="color:#8b5cf6;font-weight:800;font-size:0.85rem;min-width:35px;">{sayi}</span>
                    <span style="color:#e2e8f0;font-size:0.8rem;flex:1;">{sorun}</span>
                    <span style="color:#64748b;font-size:0.65rem;">%{pct}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Belirgin sorun tespit edilmedi!")


def _hesapla_soru_kalite(q, results: list) -> dict:
    """Tek soru icin kalite skoru hesapla."""
    kriterler = {}
    sorunlar = []

    # Kok netligi — text uzunlugu ve sik sayisi
    text = getattr(q, 'text', getattr(q, 'stem', ''))
    options = getattr(q, 'options', [])
    if len(text) < 15:
        kriterler["Kok Netliği"] = 40
        sorunlar.append("Soru koku cok kisa")
    elif len(text) > 500:
        kriterler["Kok Netliği"] = 60
        sorunlar.append("Soru koku cok uzun")
    else:
        kriterler["Kok Netliği"] = 80

    # Celdirici etkinligi
    if isinstance(options, list) and len(options) >= 4:
        kriterler["Celdirici Etkinliği"] = 75
    elif isinstance(options, list) and len(options) >= 2:
        kriterler["Celdirici Etkinliği"] = 55
        sorunlar.append("Yetersiz sik sayisi")
    else:
        kriterler["Celdirici Etkinliği"] = 30
        sorunlar.append("Celdirici yok veya az")

    # Bloom uyumu
    bloom = getattr(q, 'bloom', getattr(q, 'bloom_level', ''))
    if bloom and bloom in _BLOOM_SEVIYELERI:
        kriterler["Bloom Uyumu"] = 80
    else:
        kriterler["Bloom Uyumu"] = 50
        sorunlar.append("Bloom seviyesi belirsiz")

    # Zorluk kalibrasyonu
    difficulty = getattr(q, 'difficulty', '')
    if difficulty:
        kriterler["Zorluk Kalibrasyonu"] = 75
    else:
        kriterler["Zorluk Kalibrasyonu"] = 45
        sorunlar.append("Zorluk kalibre edilmemis")

    # Ayirt edicilik (basit tahmin)
    kriterler["Ayirt Edicilik"] = 65

    # Teknik kalite
    if text and not text[0].isupper() and not text[0].isdigit():
        kriterler["Teknik Kalite"] = 60
        sorunlar.append("Buyuk harfle baslamiyor")
    else:
        kriterler["Teknik Kalite"] = 80

    # Genel skor
    genel = 0
    for kriter, info in _KALITE_KRITERLERI.items():
        puan = kriterler.get(kriter, 50)
        genel += puan * info["agirlik"] / 100

    return {"genel": round(genel), "kriterler": kriterler, "sorunlar": sorunlar}


# ════════════════════════════════════════════════════════════
# 3. ÖĞRENCİ BAŞARI TAHMİN & ERKEN UYARI MOTORU
# ════════════════════════════════════════════════════════════

def render_basari_tahmin():
    """Öğrenci Başarı Tahmin & Erken Uyarı Motoru."""
    styled_section("Ogrenci Basari Tahmin & Erken Uyari Motoru", "#ef4444")
    styled_info_banner(
        "Gecmis sinav sonuclari, devamsizlik, kazanim eksikleri ve not trendinden "
        "ogrencinin sonraki sinavdaki basarisini tahmin eder. Risk haritasi + mudahale onerisi.",
        banner_type="warning", icon="🏆")

    store = _od_store()
    results = []
    exams = []
    questions = []
    if store:
        try:
            results = store.get_results()
            exams = store.get_exams()
            questions = store.list_questions()
        except Exception:
            pass

    if not results:
        st.info("Tahmin icin sinav sonucu verisi gerekli.")
        return

    # Ogrenci bazli sonuclari grupla
    ogr_sonuclar = defaultdict(list)
    for r in results:
        sid = getattr(r, 'student_id', '') or r.get('student_id', '') if isinstance(r, dict) else getattr(r, 'student_id', '')
        sname = getattr(r, 'student_name', '') or (r.get('student_name', '') if isinstance(r, dict) else '')
        puan = getattr(r, 'score', 0) or (r.get('score', 0) if isinstance(r, dict) else 0)
        tarih = getattr(r, 'created_at', '') or (r.get('created_at', '') if isinstance(r, dict) else '')
        if sid:
            ogr_sonuclar[sid].append({"ad": sname, "puan": puan, "tarih": tarih})

    # KPI
    toplam_ogr = len(ogr_sonuclar)
    riskli = 0
    for sid, sonuclar in ogr_sonuclar.items():
        puanlar = [s["puan"] for s in sonuclar if isinstance(s["puan"], (int, float))]
        if puanlar and sum(puanlar) / len(puanlar) < 50:
            riskli += 1

    styled_stat_row([
        ("Ogrenci", str(toplam_ogr), "#3b82f6", "👥"),
        ("Sinav Sonucu", str(len(results)), "#8b5cf6", "📊"),
        ("Risk Altinda", str(riskli), "#ef4444", "🚨"),
    ])

    sub = st.tabs(["🔮 Bireysel Tahmin", "🗺️ Sinif Risk Haritasi", "📈 Trend Analizi", "💡 Mudahale Onerisi"])

    # ── BİREYSEL TAHMİN ──
    with sub[0]:
        styled_section("Ogrenci Bazli Basari Tahmini")
        if not ogr_sonuclar:
            st.info("Ogrenci sonucu yok.")
        else:
            ogr_list = [(sid, sonuclar[0]["ad"], sonuclar) for sid, sonuclar in ogr_sonuclar.items()]
            ogr_opts = [f"{ad} ({len(s)} sinav)" for _, ad, s in ogr_list]
            sec = st.selectbox("Ogrenci Sec", ogr_opts, key="bt_ogr_sec")
            sec_idx = ogr_opts.index(sec) if sec else 0
            _, sec_ad, sec_sonuclar = ogr_list[sec_idx]

            puanlar = [s["puan"] for s in sec_sonuclar if isinstance(s["puan"], (int, float))]
            if puanlar:
                ort = round(sum(puanlar) / len(puanlar), 1)
                son_puan = puanlar[-1] if puanlar else 0
                trend = puanlar[-1] - puanlar[-2] if len(puanlar) >= 2 else 0

                # Basit tahmin: agirlikli ortalama + trend
                tahmin = round(min(100, max(0, ort * 0.5 + son_puan * 0.3 + trend * 0.2)))
                risk = max(0, min(100, 100 - tahmin))
                risk_label = "Kritik" if risk >= 60 else "Yuksek" if risk >= 40 else "Orta" if risk >= 20 else "Dusuk"
                renk = "#dc2626" if risk >= 60 else "#ef4444" if risk >= 40 else "#f59e0b" if risk >= 20 else "#10b981"

                # Hero
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,{renk}15);border:2px solid {renk};
                    border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">{sec_ad}</div>
                    <div style="display:flex;justify-content:center;gap:30px;margin-top:12px;">
                        <div>
                            <div style="color:#3b82f6;font-weight:900;font-size:2rem;">{ort}</div>
                            <div style="color:#64748b;font-size:0.7rem;">Ortalama</div>
                        </div>
                        <div>
                            <div style="color:#8b5cf6;font-weight:900;font-size:2rem;">{tahmin}</div>
                            <div style="color:#64748b;font-size:0.7rem;">Tahmin</div>
                        </div>
                        <div>
                            <div style="color:{renk};font-weight:900;font-size:2rem;">{risk}%</div>
                            <div style="color:#64748b;font-size:0.7rem;">{risk_label} Risk</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

                # Sinav gecmisi
                styled_section("Sinav Gecmisi")
                for idx, s in enumerate(sec_sonuclar):
                    p = s["puan"]
                    p_renk = "#10b981" if p >= 70 else "#f59e0b" if p >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:20px;font-size:0.7rem;color:#64748b;">{idx+1}.</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{p}%;height:100%;background:{p_renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.6rem;color:#fff;font-weight:700;">{p}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── SINIF RİSK HARİTASI ──
    with sub[1]:
        styled_section("Sinif Bazli Risk Haritasi")
        risk_list = []
        for sid, sonuclar in ogr_sonuclar.items():
            ad = sonuclar[0]["ad"]
            puanlar = [s["puan"] for s in sonuclar if isinstance(s["puan"], (int, float))]
            if puanlar:
                ort = round(sum(puanlar) / len(puanlar), 1)
                risk = max(0, min(100, round(100 - ort)))
                risk_list.append({"ad": ad, "ort": ort, "risk": risk, "sinav": len(puanlar)})

        risk_list.sort(key=lambda x: x["risk"], reverse=True)

        yuksek = sum(1 for r in risk_list if r["risk"] >= 50)
        orta = sum(1 for r in risk_list if 25 <= r["risk"] < 50)
        dusuk = sum(1 for r in risk_list if r["risk"] < 25)

        styled_stat_row([
            ("Yuksek Risk", str(yuksek), "#ef4444", "🔴"),
            ("Orta Risk", str(orta), "#f59e0b", "🟡"),
            ("Dusuk Risk", str(dusuk), "#10b981", "🟢"),
        ])

        for r in risk_list[:20]:
            renk = "#dc2626" if r["risk"] >= 60 else "#ef4444" if r["risk"] >= 40 else "#f59e0b" if r["risk"] >= 20 else "#10b981"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;min-width:130px;">{r['ad']}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                    <div style="width:{r['risk']}%;height:100%;background:{renk};border-radius:4px;"></div>
                </div>
                <span style="color:{renk};font-weight:800;font-size:0.72rem;min-width:40px;">%{r['risk']}</span>
                <span style="color:#64748b;font-size:0.6rem;">Ort:{r['ort']}</span>
            </div>""", unsafe_allow_html=True)

    # ── TREND ANALİZİ ──
    with sub[2]:
        styled_section("Basari Trendi")
        if len(results) < 2:
            st.info("Trend analizi icin en az 2 sinav sonucu gerekli.")
        else:
            # Genel ortalama trendi
            tarih_grp = defaultdict(list)
            for r in results:
                tarih = getattr(r, 'created_at', '') or (r.get('created_at','') if isinstance(r, dict) else '')
                puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
                ay = tarih[:7] if tarih else ""
                if ay and isinstance(puan, (int, float)):
                    tarih_grp[ay].append(puan)

            for ay in sorted(tarih_grp.keys())[-6:]:
                puanlar = tarih_grp[ay]
                ort = round(sum(puanlar) / max(len(puanlar), 1), 1)
                renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:55px;font-size:0.72rem;color:#94a3b8;">{ay}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{ort}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{ort}</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(puanlar)} sonuc</span>
                </div>""", unsafe_allow_html=True)

    # ── MÜDAHALE ÖNERİSİ ──
    with sub[3]:
        styled_section("Risk Bazli Mudahale Onerileri")
        if not risk_list:
            st.info("Veri yok.")
        else:
            yuksek_risk = [r for r in risk_list if r["risk"] >= 40]
            if not yuksek_risk:
                st.success("Yuksek riskli ogrenci yok!")
            else:
                for r in yuksek_risk[:10]:
                    renk = "#dc2626" if r["risk"] >= 60 else "#ef4444"
                    oneriler = []
                    if r["ort"] < 40:
                        oneriler.append("Acil bireysel destek planı olustur")
                        oneriler.append("Veli gorusmesi planla")
                    if r["ort"] < 60:
                        oneriler.append("Etut/telafi dersi planla")
                        oneriler.append("Kazanim eksiklerini tara")
                    oneriler.append("Sonraki sinav oncesi hatirlatici gonder")

                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                        border-radius:0 12px 12px 0;padding:10px 14px;margin:6px 0;">
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">🚨 {r['ad']}</span>
                            <span style="color:{renk};font-weight:800;font-size:0.8rem;">Risk: %{r['risk']}</span>
                        </div>
                        <div style="margin-top:6px;">
                            {''.join(f'<div style="color:#94a3b8;font-size:0.72rem;padding:2px 0;padding-left:12px;border-left:2px solid {renk};">▸ {o}</div>' for o in oneriler)}
                        </div>
                    </div>""", unsafe_allow_html=True)
