"""
Ölçme Değerlendirme — Mega Özellikler
=======================================
1. Öğrenci Dijital Portfolyo & Yetkinlik Haritası
2. Formatif Değerlendirme & Anlık Geri Bildirim Motoru
3. Karşılaştırmalı Sınav Cockpit & Okul Kıyaslama
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner
from utils.tenant import get_data_path


def _store():
    try:
        from models.olcme_degerlendirme import get_store
        return get_store()
    except Exception:
        return None


def _dd() -> str:
    d = os.path.join(get_data_path(), "olcme")
    os.makedirs(d, exist_ok=True)
    return d


def _lj(name: str) -> list:
    p = os.path.join(_dd(), name)
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _sj(name: str, data: list) -> None:
    with open(os.path.join(_dd(), name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


_MASTERY = {
    (0, 30): ("Baslangic", "#ef4444", "🔴"),
    (30, 60): ("Gelisen", "#f59e0b", "🟡"),
    (60, 80): ("Yetkin", "#3b82f6", "🔵"),
    (80, 101): ("Uzman", "#10b981", "🟢"),
}


def _mastery_label(puan: float) -> tuple[str, str, str]:
    for (lo, hi), (label, renk, ikon) in _MASTERY.items():
        if lo <= puan < hi:
            return label, renk, ikon
    return "?", "#94a3b8", "⚪"


_SUBJECTS = ["Matematik", "Turkce", "Fen Bilimleri", "Sosyal Bilgiler", "Ingilizce",
             "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya"]


# ════════════════════════════════════════════════════════════
# 1. ÖĞRENCİ DİJİTAL PORTFOLYO & YETKİNLİK HARİTASI
# ════════════════════════════════════════════════════════════

def render_dijital_portfolyo():
    """Öğrenci Dijital Portfolyo — kazanım mastery, yetkinlik haritası, zaman evrimi."""
    styled_section("Ogrenci Dijital Portfolyo & Yetkinlik Haritasi", "#6366f1")
    styled_info_banner(
        "Her ogrencinin sinav sonuclari, kazanim ilerlemesi, proje/performans notlari "
        "tek portfolyo kartinda. Ders bazli yetkinlik haritasi + mastery seviyesi.",
        banner_type="info", icon="📂")

    store = _store()
    results = []
    exams = []
    if store:
        try:
            results = store.get_results()
            exams = store.get_exams()
        except Exception:
            pass

    portfolyolar = _lj("portfolyolar.json")

    if not results:
        st.info("Portfolyo icin sinav sonucu verisi gerekli.")
        return

    # Ogrenci listesi
    ogr_map = {}
    for r in results:
        sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
        sname = getattr(r, 'student_name', '') or (r.get('student_name','') if isinstance(r, dict) else '')
        if sid and sname:
            ogr_map[sid] = sname

    if not ogr_map:
        st.info("Ogrenci verisi yok.")
        return

    styled_stat_row([
        ("Ogrenci", str(len(ogr_map)), "#6366f1", "👤"),
        ("Sinav Sonucu", str(len(results)), "#3b82f6", "📊"),
        ("Portfolyo", str(len(portfolyolar)), "#10b981", "📂"),
    ])

    sub = st.tabs(["👤 Portfolyo Kart", "🗺️ Yetkinlik Haritasi", "📈 Zaman Evrimi", "📄 Paylas & Rapor"])

    # ── PORTFOLYO KART ──
    with sub[0]:
        styled_section("Ogrenci Portfolyo Karti")
        ogr_opts = [f"{name} ({sid[:8]})" for sid, name in ogr_map.items()]
        sec = st.selectbox("Ogrenci Sec", ogr_opts, key="pf_ogr")
        sec_idx = ogr_opts.index(sec) if sec else 0
        sec_sid = list(ogr_map.keys())[sec_idx]
        sec_ad = ogr_map[sec_sid]

        # Bu ogrencinin sonuclari
        ogr_results = []
        for r in results:
            sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
            if sid == sec_sid:
                ogr_results.append(r)

        puanlar = []
        ders_puanlar = defaultdict(list)
        for r in ogr_results:
            puan = getattr(r, 'score', 0) or (r.get('score', 0) if isinstance(r, dict) else 0)
            exam_id = getattr(r, 'exam_id', '') or (r.get('exam_id', '') if isinstance(r, dict) else '')
            if isinstance(puan, (int, float)):
                puanlar.append(puan)
                # Ders bilgisi
                exam = next((e for e in exams if getattr(e, 'id', '') == exam_id), None)
                if exam:
                    ders = getattr(exam, 'subject', '') or getattr(exam, 'exam_type', 'Genel')
                    ders_puanlar[ders].append(puan)

        ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0
        en_yuksek = max(puanlar) if puanlar else 0
        en_dusuk = min(puanlar) if puanlar else 0
        m_label, m_renk, m_ikon = _mastery_label(ort)

        # Hero kart
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b,#6366f130);border:2px solid #6366f1;
            border-radius:20px;padding:24px 28px;margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">📂 {sec_ad}</div>
                    <div style="color:#94a3b8;font-size:0.8rem;">{len(ogr_results)} sinav | {len(ders_puanlar)} ders</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:{m_renk};font-weight:900;font-size:2.5rem;">{ort}</div>
                    <div style="background:{m_renk}20;color:{m_renk};padding:3px 12px;border-radius:8px;
                        font-size:0.75rem;font-weight:800;">{m_ikon} {m_label}</div>
                </div>
            </div>
            <div style="display:flex;gap:20px;margin-top:12px;color:#64748b;font-size:0.75rem;">
                <span>En Yuksek: <b style="color:#10b981;">{en_yuksek}</b></span>
                <span>En Dusuk: <b style="color:#ef4444;">{en_dusuk}</b></span>
                <span>Sinav: <b>{len(puanlar)}</b></span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Ders bazli mastery
        if ders_puanlar:
            styled_section("Ders Bazli Yetkinlik")
            for ders, dp in sorted(ders_puanlar.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
                d_ort = round(sum(dp) / max(len(dp), 1), 1)
                d_label, d_renk, d_ikon = _mastery_label(d_ort)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="min-width:130px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                        <div style="width:{d_ort}%;height:100%;background:{d_renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{d_ort}</span>
                        </div>
                    </div>
                    <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                        font-size:0.65rem;font-weight:700;min-width:65px;text-align:center;">{d_ikon} {d_label}</span>
                </div>""", unsafe_allow_html=True)

    # ── YETKİNLİK HARİTASI ──
    with sub[1]:
        styled_section("Sinif Geneli Yetkinlik Haritasi")
        if not ders_puanlar and not results:
            st.info("Veri yok.")
        else:
            # Tum ogrenciler icin ders bazli ortalama
            genel_ders = defaultdict(list)
            for r in results:
                puan = getattr(r, 'score', 0) or (r.get('score', 0) if isinstance(r, dict) else 0)
                exam_id = getattr(r, 'exam_id', '') or (r.get('exam_id', '') if isinstance(r, dict) else '')
                exam = next((e for e in exams if getattr(e, 'id', '') == exam_id), None)
                if exam and isinstance(puan, (int, float)):
                    ders = getattr(exam, 'subject', '') or getattr(exam, 'exam_type', 'Genel')
                    genel_ders[ders].append(puan)

            styled_section("Ders Bazli Okul Ortalamalari")
            for ders in sorted(genel_ders.keys()):
                dp = genel_ders[ders]
                d_ort = round(sum(dp) / max(len(dp), 1), 1)
                _, d_renk, d_ikon = _mastery_label(d_ort)
                ogr_say = len(set(
                    getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
                    for r in results
                    if (getattr(r, 'exam_id', '') or (r.get('exam_id','') if isinstance(r, dict) else ''))
                    in [getattr(e, 'id', '') for e in exams if (getattr(e, 'subject', '') or getattr(e, 'exam_type', '')) == ders]
                ))
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:5px 0;">
                    <span style="min-width:130px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{d_ort}%;height:100%;background:{d_renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{d_ort}</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(dp)} sonuc | {ogr_say} ogr</span>
                </div>""", unsafe_allow_html=True)

    # ── ZAMAN EVRİMİ ──
    with sub[2]:
        styled_section("Basari Evrimi (Zaman Serisi)")
        if not ogr_map:
            st.info("Veri yok.")
        else:
            sec2 = st.selectbox("Ogrenci", list(ogr_map.values()), key="pf_evrim")
            sec2_sid = [sid for sid, name in ogr_map.items() if name == sec2]
            if sec2_sid:
                sec2_sid = sec2_sid[0]
                ogr_r = []
                for r in results:
                    sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
                    if sid == sec2_sid:
                        puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
                        tarih = getattr(r, 'created_at', '') or (r.get('created_at','') if isinstance(r, dict) else '')
                        if isinstance(puan, (int, float)):
                            ogr_r.append({"puan": puan, "tarih": tarih})

                ogr_r.sort(key=lambda x: x["tarih"])
                if ogr_r:
                    for idx, r in enumerate(ogr_r):
                        renk = "#10b981" if r["puan"] >= 70 else "#f59e0b" if r["puan"] >= 50 else "#ef4444"
                        trend = ""
                        if idx > 0:
                            diff = r["puan"] - ogr_r[idx-1]["puan"]
                            trend = f"↑{diff}" if diff > 0 else f"↓{abs(diff)}" if diff < 0 else "→"
                            trend_renk = "#10b981" if diff > 0 else "#ef4444" if diff < 0 else "#94a3b8"
                        else:
                            trend_renk = "#94a3b8"
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                            <span style="min-width:20px;font-size:0.7rem;color:#64748b;">{idx+1}</span>
                            <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                                <div style="width:{r['puan']}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                                    <span style="font-size:0.6rem;color:#fff;font-weight:700;">{r['puan']}</span>
                                </div>
                            </div>
                            <span style="color:{trend_renk};font-size:0.7rem;font-weight:700;min-width:35px;">{trend}</span>
                            <span style="font-size:0.6rem;color:#64748b;">{r['tarih'][:10]}</span>
                        </div>""", unsafe_allow_html=True)

    # ── PAYLAŞ ──
    with sub[3]:
        styled_section("Portfolyo Paylasim & Rapor")
        st.info("Portfolyo PDF raporu olusturma ve veli/ogretmen paylasim linki yakinda aktif olacak.")
        st.caption("Su an icin Raporlar sekmesinden PDF indirebilirsiniz.")


# ════════════════════════════════════════════════════════════
# 2. FORMATİF DEĞERLENDİRME & ANLIK GERİ BİLDİRİM MOTORU
# ════════════════════════════════════════════════════════════

_FORMATIF_TURLERI = {
    "Exit Ticket": {"ikon": "🎫", "renk": "#3b82f6", "aciklama": "Ders sonu 1-2 soruluk hizli yoklama"},
    "Thumbs Up/Down": {"ikon": "👍", "renk": "#10b981", "aciklama": "Anlama durumu anlik anket"},
    "Kavram Kontrolu": {"ikon": "🔍", "renk": "#8b5cf6", "aciklama": "1 soruluk mini quiz"},
    "Oz Degerlendirme": {"ikon": "📝", "renk": "#f59e0b", "aciklama": "Ogrenci kendi ogrenme rubriği"},
    "Sinif Nabzi": {"ikon": "🌡️", "renk": "#ef4444", "aciklama": "Sinifin genel anlama seviyesi"},
}


def render_formatif_degerlendirme():
    """Formatif Değerlendirme & Anlık Geri Bildirim Motoru."""
    styled_section("Formatif Degerlendirme & Anlik Geri Bildirim", "#059669")
    styled_info_banner(
        "Sinav disi gunluk degerlendirme: exit ticket, anlik anket, kavram kontrolu, "
        "oz-degerlendirme. Ogretmen 30 saniyede 'sinif ne anladi?' verisini toplar.",
        banner_type="info", icon="🔄")

    formatifler = _lj("formatif_kayitlar.json")

    # KPI
    bugun = date.today().isoformat()
    bugun_kayit = sum(1 for f in formatifler if f.get("tarih", "")[:10] == bugun)
    bu_hafta_bas = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    hafta_kayit = sum(1 for f in formatifler if f.get("tarih", "")[:10] >= bu_hafta_bas)
    tur_say = len(set(f.get("tur", "") for f in formatifler))

    styled_stat_row([
        ("Bugun", str(bugun_kayit), "#059669", "📅"),
        ("Bu Hafta", str(hafta_kayit), "#3b82f6", "📊"),
        ("Toplam", str(len(formatifler)), "#8b5cf6", "📋"),
        ("Farkli Tur", str(tur_say), "#f59e0b", "🔄"),
    ])

    sub = st.tabs(["🎫 Hizli Yoklama", "📊 Sinif Nabzi", "📝 Oz Degerlendirme", "📈 Haftalik Analiz", "🗂️ Gecmis"])

    # ── HIZLI YOKLAMA (EXIT TICKET) ──
    with sub[0]:
        styled_section("Exit Ticket — Ders Sonu Hizli Yoklama")
        with st.form("fmt_exit_form"):
            c1, c2 = st.columns(2)
            with c1:
                f_ders = st.selectbox("Ders", _SUBJECTS, key="fmt_ders")
                f_sinif = st.text_input("Sinif/Sube", placeholder="8/A", key="fmt_sinif")
            with c2:
                f_konu = st.text_input("Konu / Kazanim", key="fmt_konu")
                f_tur = st.selectbox("Yoklama Turu", list(_FORMATIF_TURLERI.keys()), key="fmt_tur")

            f_soru = st.text_input("Soru (opsiyonel)", placeholder="Bugun ne ogrendin?", key="fmt_soru")

            st.markdown("**Sinif Sonuclari:**")
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                f_anladi = st.number_input("Anladi", min_value=0, value=0, key="fmt_anladi")
            with fc2:
                f_kismen = st.number_input("Kismen", min_value=0, value=0, key="fmt_kismen")
            with fc3:
                f_anlamadi = st.number_input("Anlamadi", min_value=0, value=0, key="fmt_anlamadi")

            if st.form_submit_button("Kaydet", use_container_width=True):
                toplam = f_anladi + f_kismen + f_anlamadi
                if toplam > 0:
                    anlama_orani = round(f_anladi / toplam * 100)
                    kayit = {
                        "id": f"fmt_{uuid.uuid4().hex[:8]}",
                        "ders": f_ders,
                        "sinif": f_sinif,
                        "konu": f_konu,
                        "tur": f_tur,
                        "soru": f_soru,
                        "anladi": f_anladi,
                        "kismen": f_kismen,
                        "anlamadi": f_anlamadi,
                        "toplam": toplam,
                        "anlama_orani": anlama_orani,
                        "tarih": datetime.now().isoformat(),
                    }
                    formatifler.append(kayit)
                    _sj("formatif_kayitlar.json", formatifler)

                    renk = "#10b981" if anlama_orani >= 70 else "#f59e0b" if anlama_orani >= 50 else "#ef4444"
                    st.success(f"Kaydedildi! Anlama orani: %{anlama_orani}")
                    if anlama_orani < 50:
                        st.error("Sinifin yarısından azı anladi — konuyu tekrar edin!")
                    elif anlama_orani < 70:
                        st.warning("Pekistirme etkinligi oneririz.")
                    st.rerun()

    # ── SINIF NABZI ──
    with sub[1]:
        styled_section("Sinif Nabzi — Anlik Durum")
        if not formatifler:
            st.info("Henuz kayit yok.")
        else:
            # Son 5 kayit
            son = sorted(formatifler, key=lambda x: x.get("tarih",""), reverse=True)[:10]
            for f in son:
                oran = f.get("anlama_orani", 0)
                renk = "#10b981" if oran >= 70 else "#f59e0b" if oran >= 50 else "#ef4444"
                tur_info = _FORMATIF_TURLERI.get(f.get("tur",""), {"ikon": "📋"})
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">
                            {tur_info['ikon']} {f.get('ders','')} — {f.get('sinif','')}</span>
                        <span style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:8px;
                            font-size:0.75rem;font-weight:800;">%{oran}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {f.get('konu','')} | {f.get('anladi',0)} anladi, {f.get('kismen',0)} kismen, {f.get('anlamadi',0)} anlamadi
                    </div>
                    <div style="color:#64748b;font-size:0.65rem;">{f.get('tarih','')[:16]}</div>
                </div>""", unsafe_allow_html=True)

    # ── ÖZ DEĞERLENDİRME ──
    with sub[2]:
        styled_section("Ogrenci Oz Degerlendirme Rubriği")
        st.caption("Ogrenciler kendi ogrenme durumlarini degerlendirir.")

        with st.form("fmt_oz_form"):
            oz_sinif = st.text_input("Sinif/Sube", key="fmt_oz_sinif")
            oz_ders = st.selectbox("Ders", _SUBJECTS, key="fmt_oz_ders")
            oz_konu = st.text_input("Konu", key="fmt_oz_konu")

            st.markdown("**Oz Degerlendirme Sonuclari (sinif toplami):**")
            oc1, oc2, oc3, oc4 = st.columns(4)
            with oc1:
                oz_1 = st.number_input("Hic anlamadim", min_value=0, value=0, key="fmt_oz1")
            with oc2:
                oz_2 = st.number_input("Biraz anladim", min_value=0, value=0, key="fmt_oz2")
            with oc3:
                oz_3 = st.number_input("Iyi anladim", min_value=0, value=0, key="fmt_oz3")
            with oc4:
                oz_4 = st.number_input("Cok iyi anladim", min_value=0, value=0, key="fmt_oz4")

            if st.form_submit_button("Kaydet", use_container_width=True):
                toplam = oz_1 + oz_2 + oz_3 + oz_4
                if toplam > 0:
                    oz_ort = round((oz_1*1 + oz_2*2 + oz_3*3 + oz_4*4) / toplam, 1)
                    kayit = {
                        "id": f"foz_{uuid.uuid4().hex[:8]}",
                        "ders": oz_ders, "sinif": oz_sinif, "konu": oz_konu,
                        "tur": "Oz Degerlendirme",
                        "seviye_1": oz_1, "seviye_2": oz_2, "seviye_3": oz_3, "seviye_4": oz_4,
                        "toplam": toplam, "ortalama": oz_ort,
                        "anlama_orani": round((oz_3 + oz_4) / toplam * 100),
                        "tarih": datetime.now().isoformat(),
                    }
                    formatifler.append(kayit)
                    _sj("formatif_kayitlar.json", formatifler)
                    st.success(f"Oz degerlendirme kaydedildi! Ort: {oz_ort}/4")
                    st.rerun()

    # ── HAFTALIK ANALİZ ──
    with sub[3]:
        styled_section("Haftalik Formatif Analiz")
        if not formatifler:
            st.info("Veri yok.")
        else:
            # Ders bazli haftalik ortalama
            ders_ort = defaultdict(list)
            hafta_kayitlar = [f for f in formatifler if f.get("tarih","")[:10] >= bu_hafta_bas]
            for f in hafta_kayitlar:
                ders_ort[f.get("ders","?")].append(f.get("anlama_orani", 0))

            if ders_ort:
                styled_section("Bu Hafta Ders Bazli Anlama Orani")
                for ders, oranlar in sorted(ders_ort.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
                    ort = round(sum(oranlar) / max(len(oranlar), 1))
                    renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin:5px 0;">
                        <span style="min-width:120px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                            <div style="width:{ort}%;height:100%;background:{renk};border-radius:6px;
                                display:flex;align-items:center;padding-left:8px;">
                                <span style="font-size:0.65rem;color:#fff;font-weight:800;">%{ort}</span>
                            </div>
                        </div>
                        <span style="font-size:0.65rem;color:#64748b;">{len(oranlar)} kayit</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Bu hafta formatif kayit yok.")

    # ── GEÇMİŞ ──
    with sub[4]:
        styled_section("Tum Formatif Gecmis")
        if formatifler:
            tur_say = Counter(f.get("tur","?") for f in formatifler)
            for tur, sayi in tur_say.most_common():
                info = _FORMATIF_TURLERI.get(tur, {"ikon": "📋", "renk": "#94a3b8"})
                st.markdown(f"""
                <div style="display:inline-block;background:{info['renk']}10;border:1px solid {info['renk']}30;
                    padding:6px 14px;border-radius:10px;margin:3px;font-size:0.8rem;">
                    {info['ikon']} {tur}: <b style="color:{info['renk']};">{sayi}</b>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. KARŞILAŞTIRMALI SINAV COCKPİT & OKUL KIYASLAMA
# ════════════════════════════════════════════════════════════

def render_sinav_cockpit():
    """Karşılaştırmalı Sınav Cockpit — sınıf, şube, dönem, yıl karşılaştırma."""
    styled_section("Karsilastirmali Sinav Cockpit & Okul Kiyaslama", "#0891b2")
    styled_info_banner(
        "Siniflar arasi, subeler arasi, donemler arasi karsilastirma. "
        "Ders bazli heatmap, ilce/il ortalamasiyla kiyaslama, aksiyon onerisi.",
        banner_type="info", icon="🧮")

    store = _store()
    results = []
    exams = []
    if store:
        try:
            results = store.get_results()
            exams = store.get_exams()
        except Exception:
            pass

    if not results:
        st.info("Karsilastirma icin sinav sonucu verisi gerekli.")
        return

    kiyaslama = _lj("kiyaslama_verileri.json")

    styled_stat_row([
        ("Sinav Sonucu", str(len(results)), "#0891b2", "📊"),
        ("Sinav", str(len(exams)), "#3b82f6", "📋"),
    ])

    sub = st.tabs(["⚔️ Sinif Karsilastir", "📊 Ders Heatmap", "📅 Donem Karsilastir", "🏫 Il/Ilce Kiyasla"])

    # ── SINIF KARŞILAŞTIR ──
    with sub[0]:
        styled_section("Sinif / Sube Karsilastirmasi")
        if not exams:
            st.info("Sinav verisi yok.")
        else:
            # Sinav sec
            exam_opts = {f"{getattr(e,'name','') or getattr(e,'exam_type','')} ({getattr(e,'created_at','')[:10]})": e for e in exams}
            sec_exam_label = st.selectbox("Sinav Sec", list(exam_opts.keys()), key="ck_exam")
            sec_exam = exam_opts.get(sec_exam_label)
            if sec_exam:
                exam_id = getattr(sec_exam, 'id', '')
                exam_results = [r for r in results
                    if (getattr(r, 'exam_id', '') or (r.get('exam_id','') if isinstance(r, dict) else '')) == exam_id]

                if not exam_results:
                    st.info("Bu sinav icin sonuc yok.")
                else:
                    # Sınıf/sube bazli grupla (student_name'den cikar)
                    puanlar_all = []
                    for r in exam_results:
                        puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
                        if isinstance(puan, (int, float)):
                            puanlar_all.append(puan)

                    genel_ort = round(sum(puanlar_all) / max(len(puanlar_all), 1), 1)
                    en_yuksek = max(puanlar_all) if puanlar_all else 0
                    en_dusuk = min(puanlar_all) if puanlar_all else 0
                    basari = round(sum(1 for p in puanlar_all if p >= 50) / max(len(puanlar_all), 1) * 100)

                    styled_stat_row([
                        ("Ogrenci", str(len(puanlar_all)), "#0891b2", "👥"),
                        ("Ortalama", str(genel_ort), "#3b82f6", "📊"),
                        ("En Yuksek", str(en_yuksek), "#10b981", "🔝"),
                        ("En Dusuk", str(en_dusuk), "#ef4444", "🔻"),
                        ("Basari %", f"%{basari}", "#10b981" if basari >= 70 else "#f59e0b", "🎯"),
                    ])

                    # Puan dagilimi
                    styled_section("Puan Dagilimi")
                    araliklar = [(0,25,"0-24"), (25,50,"25-49"), (50,70,"50-69"), (70,85,"70-84"), (85,101,"85-100")]
                    aral_renk = ["#dc2626", "#ef4444", "#f59e0b", "#3b82f6", "#10b981"]
                    for (lo, hi, label), renk in zip(araliklar, aral_renk):
                        sayi = sum(1 for p in puanlar_all if lo <= p < hi)
                        pct = round(sayi / max(len(puanlar_all), 1) * 100)
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                            <span style="min-width:45px;font-size:0.72rem;color:#e2e8f0;font-weight:600;">{label}</span>
                            <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                                <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                                    <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                                </div>
                            </div>
                            <span style="font-size:0.65rem;color:#64748b;">%{pct}</span>
                        </div>""", unsafe_allow_html=True)

    # ── DERS HEATMAP ──
    with sub[1]:
        styled_section("Ders Bazli Basari Haritasi")
        ders_sonuc = defaultdict(list)
        for r in results:
            puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
            exam_id = getattr(r, 'exam_id', '') or (r.get('exam_id','') if isinstance(r, dict) else '')
            exam = next((e for e in exams if getattr(e, 'id', '') == exam_id), None)
            if exam and isinstance(puan, (int, float)):
                ders = getattr(exam, 'subject', '') or getattr(exam, 'exam_type', 'Genel')
                ders_sonuc[ders].append(puan)

        if ders_sonuc:
            for ders in sorted(ders_sonuc.keys(), key=lambda x: sum(ders_sonuc[x])/len(ders_sonuc[x]), reverse=True):
                dp = ders_sonuc[ders]
                ort = round(sum(dp) / max(len(dp), 1), 1)
                renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                basari_o = round(sum(1 for p in dp if p >= 50) / max(len(dp), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                    <span style="min-width:120px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{ort}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{ort}</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(dp)} sonuc | Basari: %{basari_o}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Ders bazli veri yok.")

    # ── DÖNEM KARŞILAŞTIR ──
    with sub[2]:
        styled_section("Donem Bazli Karsilastirma")
        ay_grp = defaultdict(list)
        for r in results:
            puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
            tarih = getattr(r, 'created_at', '') or (r.get('created_at','') if isinstance(r, dict) else '')
            ay = tarih[:7] if tarih else ""
            if ay and isinstance(puan, (int, float)):
                ay_grp[ay].append(puan)

        if ay_grp:
            for ay in sorted(ay_grp.keys()):
                puanlar = ay_grp[ay]
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
        else:
            st.info("Donem verisi yok.")

    # ── İL/İLÇE KIYASLA ──
    with sub[3]:
        styled_section("Il / Ilce Ortalamasiyla Kiyaslama")
        st.caption("Okul ortalamanizi ilce/il ortalamasiyla karsilastirin (manuel giris).")

        with st.form("ck_kiyasla_form"):
            kc1, kc2, kc3 = st.columns(3)
            with kc1:
                k_ders = st.selectbox("Ders", _SUBJECTS, key="ck_k_ders")
                k_okul = st.number_input("Okul Ortalamasi", min_value=0.0, max_value=100.0, value=65.0, key="ck_k_okul")
            with kc2:
                k_ilce = st.number_input("Ilce Ortalamasi", min_value=0.0, max_value=100.0, value=58.0, key="ck_k_ilce")
            with kc3:
                k_il = st.number_input("Il Ortalamasi", min_value=0.0, max_value=100.0, value=55.0, key="ck_k_il")

            if st.form_submit_button("Karsilastir", use_container_width=True):
                levels = [
                    ("Okul", k_okul, "#6366f1"),
                    ("Ilce", k_ilce, "#3b82f6"),
                    ("Il", k_il, "#0891b2"),
                ]
                en_yuksek_val = max(k_okul, k_ilce, k_il)
                for label, val, renk in levels:
                    pct = round(val / max(en_yuksek_val, 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                        <span style="min-width:50px;color:#e2e8f0;font-weight:700;font-size:0.85rem;">{label}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:24px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                                display:flex;align-items:center;padding-left:10px;">
                                <span style="font-size:0.7rem;color:#fff;font-weight:800;">{val}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                fark_ilce = round(k_okul - k_ilce, 1)
                fark_il = round(k_okul - k_il, 1)
                f_renk_ilce = "#10b981" if fark_ilce > 0 else "#ef4444"
                f_renk_il = "#10b981" if fark_il > 0 else "#ef4444"
                st.markdown(f"""
                <div style="background:#0f172a;border-radius:12px;padding:14px 18px;margin-top:10px;">
                    <div style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">📊 {k_ders} Kiyaslama Sonucu</div>
                    <div style="color:#94a3b8;font-size:0.78rem;margin-top:6px;">
                        Ilce farki: <b style="color:{f_renk_ilce};">{'+' if fark_ilce > 0 else ''}{fark_ilce}</b> |
                        Il farki: <b style="color:{f_renk_il};">{'+' if fark_il > 0 else ''}{fark_il}</b>
                    </div>
                </div>""", unsafe_allow_html=True)

                # Kaydet
                kiyaslama.append({
                    "ders": k_ders, "okul": k_okul, "ilce": k_ilce, "il": k_il,
                    "tarih": date.today().isoformat(),
                })
                _sj("kiyaslama_verileri.json", kiyaslama)
