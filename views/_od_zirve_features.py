"""
Ölçme Değerlendirme — Zirve Özellikler
========================================
1. AI Öğrenme Koçu & Kişiselleştirilmiş Yol Haritası
2. Gamifiye Sınav Deneyimi & Liderlik Tablosu
3. What-If Sınav Simülatörü & Senaryo Motoru
"""
from __future__ import annotations

import json
import os
import uuid
import math
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

def _lj(n: str) -> list:
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: return []

def _sj(n: str, d: list) -> None:
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════════════════════
# 1. AI ÖĞRENME KOÇU & KİŞİSELLEŞTİRİLMİŞ YOL HARİTASI
# ════════════════════════════════════════════════════════════

_DERS_KONULARI = {
    "Matematik": ["Cebir", "Geometri", "Olasilik", "Istatistik", "Sayilar", "Fonksiyonlar", "Denklemler", "Ucgenler"],
    "Turkce": ["Dil Bilgisi", "Anlama", "Yazma", "Sozcuk Bilgisi", "Paragraf", "Ses Bilgisi"],
    "Fen Bilimleri": ["Fizik", "Kimya", "Biyoloji", "Yer Bilimi", "Astronomi"],
    "Sosyal Bilgiler": ["Tarih", "Cografya", "Vatandaslik", "Ekonomi"],
    "Ingilizce": ["Grammar", "Vocabulary", "Reading", "Listening", "Writing", "Speaking"],
}

_AKTIVITE_TIPLERI = [
    ("Konu Tekrari", "📖", 20),
    ("Soru Cozmesi", "✏️", 15),
    ("Video Izleme", "🎬", 10),
    ("Deneme Sinavi", "📝", 30),
    ("Flash Kart", "🃏", 10),
    ("Ozet Cikarma", "📋", 15),
]

_HAFTA_GUNLERI = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]


def _ogrenci_zayif_konular(ogr_id: str, results: list, exams: list) -> dict:
    """Ogrencinin ders bazli zayif konularini tespit et."""
    ders_puanlar = defaultdict(list)
    for r in results:
        sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
        if sid != ogr_id:
            continue
        puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
        eid = getattr(r, 'exam_id', '') or (r.get('exam_id','') if isinstance(r, dict) else '')
        exam = next((e for e in exams if getattr(e, 'id', '') == eid), None)
        if exam and isinstance(puan, (int, float)):
            ders = getattr(exam, 'subject', '') or getattr(exam, 'exam_type', 'Genel')
            ders_puanlar[ders].append(puan)

    zayiflar = {}
    for ders, puanlar in ders_puanlar.items():
        ort = sum(puanlar) / max(len(puanlar), 1)
        if ort < 70:
            konular = _DERS_KONULARI.get(ders, ["Genel Tekrar"])
            # Oranla zayif konu sayisi belirle
            zayif_konu_sayi = max(1, min(len(konular), round((70 - ort) / 15)))
            zayiflar[ders] = {
                "ort": round(ort, 1),
                "konular": konular[:zayif_konu_sayi],
                "sinav_sayi": len(puanlar),
            }
    return zayiflar


def render_ai_ogrenme_kocu():
    """AI Öğrenme Koçu — kişiselleştirilmiş haftalık çalışma planı."""
    styled_section("AI Ogrenme Kocu & Kisisel Yol Haritasi", "#6366f1")
    styled_info_banner(
        "Her ogrencinin sinav sonuclari ve kazanim eksiklerinden kisisel haftalik "
        "calisma plani uretir. Performansa gore otomatik guncellenir.",
        banner_type="info", icon="🧠")

    store = _store()
    results, exams = [], []
    if store:
        try:
            results = store.get_results()
            exams = store.get_exams()
        except Exception:
            pass

    planlar = _lj("koc_planlari.json")

    if not results:
        st.info("Koc icin sinav sonucu verisi gerekli.")
        return

    # Ogrenci map
    ogr_map = {}
    for r in results:
        sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
        sname = getattr(r, 'student_name', '') or (r.get('student_name','') if isinstance(r, dict) else '')
        if sid and sname:
            ogr_map[sid] = sname

    styled_stat_row([
        ("Ogrenci", str(len(ogr_map)), "#6366f1", "👤"),
        ("Uretilen Plan", str(len(planlar)), "#10b981", "📋"),
    ])

    sub = st.tabs(["🤖 Plan Uret", "📋 Aktif Planlar", "📊 Ilerleme Takip", "⚙️ Koc Ayarlari"])

    # ── PLAN ÜRET ──
    with sub[0]:
        styled_section("Kisisel Calisma Plani Uret")
        ogr_opts = [f"{name}" for sid, name in ogr_map.items()]
        sec = st.selectbox("Ogrenci Sec", ogr_opts, key="koc_ogr")
        sec_sid = list(ogr_map.keys())[ogr_opts.index(sec)] if sec else ""

        if sec_sid and st.button("AI Plan Uret", use_container_width=True, type="primary"):
            zayiflar = _ogrenci_zayif_konular(sec_sid, results, exams)

            if not zayiflar:
                st.success(f"{sec} tum derslerde 70+ — ek calisma planina gerek yok!")
            else:
                # Haftalik plan olustur
                aktiviteler = []
                gun_idx = 0
                for ders, info in zayiflar.items():
                    for konu in info["konular"]:
                        for akt_ad, akt_ikon, akt_dk in _AKTIVITE_TIPLERI[:3]:
                            gun = _HAFTA_GUNLERI[gun_idx % 5]  # haftaici
                            aktiviteler.append({
                                "gun": gun,
                                "ders": ders,
                                "konu": konu,
                                "aktivite": akt_ad,
                                "ikon": akt_ikon,
                                "sure_dk": akt_dk,
                                "tamamlandi": False,
                            })
                            gun_idx += 1

                plan = {
                    "id": f"koc_{uuid.uuid4().hex[:8]}",
                    "ogrenci_id": sec_sid,
                    "ogrenci_ad": sec,
                    "zayif_dersler": zayiflar,
                    "aktiviteler": aktiviteler,
                    "hafta": date.today().isocalendar()[1],
                    "durum": "Aktif",
                    "tarih": date.today().isoformat(),
                }
                planlar.append(plan)
                _sj("koc_planlari.json", planlar)
                st.success(f"{sec} icin {len(aktiviteler)} aktiviteli haftalik plan olusturuldu!")
                st.rerun()

        # Zayif konulari goster
        if sec_sid:
            zayiflar = _ogrenci_zayif_konular(sec_sid, results, exams)
            if zayiflar:
                styled_section(f"{sec} — Gelisim Gereken Alanlar")
                for ders, info in sorted(zayiflar.items(), key=lambda x: x[1]["ort"]):
                    renk = "#ef4444" if info["ort"] < 50 else "#f59e0b"
                    st.markdown(f"""
                    <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                        padding:10px 14px;margin:5px 0;">
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{ders}</span>
                            <span style="color:{renk};font-weight:800;font-size:0.8rem;">Ort: {info['ort']}</span>
                        </div>
                        <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                            Zayif konular: {', '.join(info['konular'])} | {info['sinav_sayi']} sinav</div>
                    </div>""", unsafe_allow_html=True)

    # ── AKTİF PLANLAR ──
    with sub[1]:
        styled_section("Aktif Calisma Planlari")
        aktif = [p for p in planlar if p.get("durum") == "Aktif"]
        if not aktif:
            st.info("Aktif plan yok. 'Plan Uret' sekmesinden baslatin.")
        else:
            for plan in aktif:
                akt_list = plan.get("aktiviteler", [])
                tamamlanan = sum(1 for a in akt_list if a.get("tamamlandi"))
                toplam = max(len(akt_list), 1)
                ilerleme = round(tamamlanan / toplam * 100)
                renk = "#10b981" if ilerleme >= 70 else "#f59e0b" if ilerleme >= 40 else "#3b82f6"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🧠 {plan.get('ogrenci_ad','')}</span>
                        <span style="color:{renk};font-weight:800;font-size:0.85rem;">%{ilerleme}</span>
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:10px;margin-top:8px;overflow:hidden;">
                        <div style="width:{ilerleme}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                    <div style="color:#64748b;font-size:0.65rem;margin-top:4px;">
                        {tamamlanan}/{toplam} aktivite | Hafta {plan.get('hafta','')} | {plan.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                # Gunluk plan
                with st.expander(f"Detay: {plan.get('ogrenci_ad','')}", expanded=False):
                    gun_grp = defaultdict(list)
                    for a in akt_list:
                        gun_grp[a.get("gun", "?")].append(a)

                    for gun in _HAFTA_GUNLERI[:5]:
                        gun_akt = gun_grp.get(gun, [])
                        if gun_akt:
                            st.markdown(f"**{gun}:**")
                            for a in gun_akt:
                                done = "✅" if a.get("tamamlandi") else "⬜"
                                st.markdown(f"  {done} {a.get('ikon','')} {a.get('ders','')} — {a.get('konu','')} ({a.get('aktivite','')}, {a.get('sure_dk',0)}dk)")

                    if st.button("Plani Tamamla", key=f"koc_done_{plan['id']}"):
                        plan["durum"] = "Tamamlandi"
                        _sj("koc_planlari.json", planlar)
                        st.rerun()

    # ── İLERLEME TAKİP ──
    with sub[2]:
        styled_section("Ogrenci Ilerleme Takibi")
        tamamlanan_plan = [p for p in planlar if p.get("durum") == "Tamamlandi"]
        if not tamamlanan_plan:
            st.info("Tamamlanan plan yok.")
        else:
            ogr_plan_say = Counter(p.get("ogrenci_ad","") for p in tamamlanan_plan)
            for ad, sayi in ogr_plan_say.most_common():
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #6366f1;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ad}</span>
                    <span style="color:#6366f1;font-weight:800;font-size:0.85rem;">{sayi} plan tamamlandi</span>
                </div>""", unsafe_allow_html=True)

    # ── AYARLAR ──
    with sub[3]:
        styled_section("Koc Motor Ayarlari")
        st.markdown("**Aktivite Tipleri ve Sureleri:**")
        for akt_ad, akt_ikon, akt_dk in _AKTIVITE_TIPLERI:
            st.markdown(f"- {akt_ikon} **{akt_ad}** — {akt_dk} dakika")
        st.markdown("**Ders Konu Havuzu:**")
        for ders, konular in _DERS_KONULARI.items():
            st.markdown(f"- **{ders}:** {', '.join(konular)}")


# ════════════════════════════════════════════════════════════
# 2. GAMİFİYE SINAV DENEYİMİ & LİDERLİK TABLOSU
# ════════════════════════════════════════════════════════════

_XP_TABLOSU = {
    (0, 100): ("Cirak", "🟤", "#78716c"),
    (100, 300): ("Kalfa", "🥉", "#a8a29e"),
    (300, 600): ("Usta", "🥈", "#94a3b8"),
    (600, 1000): ("Buyukusta", "🥇", "#f59e0b"),
    (1000, 2000): ("Efsane", "👑", "#c9a84c"),
    (2000, 99999): ("Titan", "💎", "#8b5cf6"),
}

_ROZETLER = [
    {"ad": "Ilk Adim", "ikon": "🌱", "kosul": "ilk_sinav", "hedef": 1, "xp": 10, "renk": "#10b981",
     "aciklama": "Ilk sinavini tamamla"},
    {"ad": "Matematik Krali", "ikon": "👑", "kosul": "mat_80", "hedef": 3, "xp": 50, "renk": "#3b82f6",
     "aciklama": "Matematikte ardisik 3 sinav 80+"},
    {"ad": "Fen Sampiyonu", "ikon": "🔬", "kosul": "fen_80", "hedef": 3, "xp": 50, "renk": "#10b981",
     "aciklama": "Fen Bilimlerinde ardisik 3 sinav 80+"},
    {"ad": "Turkce Ustasi", "ikon": "📖", "kosul": "tur_80", "hedef": 3, "xp": 50, "renk": "#8b5cf6",
     "aciklama": "Turkcede ardisik 3 sinav 80+"},
    {"ad": "Mukemmeliyetci", "ikon": "💯", "kosul": "puan_90", "hedef": 1, "xp": 30, "renk": "#c9a84c",
     "aciklama": "Herhangi bir sinavda 90+ al"},
    {"ad": "Surdurucu", "ikon": "🔥", "kosul": "ardisik_5", "hedef": 5, "xp": 40, "renk": "#ef4444",
     "aciklama": "Ardisik 5 sinavda 60+"},
    {"ad": "Gelisim Yildizi", "ikon": "⭐", "kosul": "gelisim_15", "hedef": 1, "xp": 35, "renk": "#f59e0b",
     "aciklama": "Bir sonraki sinavda 15+ puan artis"},
    {"ad": "Cok Yonlu", "ikon": "🌈", "kosul": "4_ders_70", "hedef": 4, "xp": 60, "renk": "#6366f1",
     "aciklama": "4 farkli derste 70+ ortalama"},
    {"ad": "Sinav Avcisi", "ikon": "🎯", "kosul": "toplam_10", "hedef": 10, "xp": 25, "renk": "#059669",
     "aciklama": "Toplam 10 sinav tamamla"},
    {"ad": "Efsane", "ikon": "🏆", "kosul": "toplam_xp_500", "hedef": 500, "xp": 100, "renk": "#c9a84c",
     "aciklama": "Toplam 500 XP topla"},
]


def _seviye_bilgi(xp: int) -> tuple[str, str, str, int, int]:
    """XP'ye gore seviye, ikon, renk, sonraki seviye XP, kalan XP."""
    for (lo, hi), (ad, ikon, renk) in _XP_TABLOSU.items():
        if lo <= xp < hi:
            return ad, ikon, renk, hi, hi - xp
    return "Titan", "💎", "#8b5cf6", 99999, 0


def _hesapla_xp(ogr_id: str, results: list, exams: list) -> dict:
    """Ogrenci icin XP, rozet, istatistik hesapla."""
    ogr_results = []
    for r in results:
        sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
        if sid == ogr_id:
            puan = getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
            eid = getattr(r, 'exam_id', '') or (r.get('exam_id','') if isinstance(r, dict) else '')
            tarih = getattr(r, 'created_at', '') or (r.get('created_at','') if isinstance(r, dict) else '')
            exam = next((e for e in exams if getattr(e, 'id', '') == eid), None)
            ders = getattr(exam, 'subject', '') if exam else 'Genel'
            if isinstance(puan, (int, float)):
                ogr_results.append({"puan": puan, "ders": ders, "tarih": tarih})

    ogr_results.sort(key=lambda x: x.get("tarih", ""))

    xp = 0
    kazanilan_rozetler = []

    # Temel XP: her sinav icin puan bazli
    for r in ogr_results:
        p = r["puan"]
        if p >= 90: xp += 15
        elif p >= 70: xp += 10
        elif p >= 50: xp += 5
        else: xp += 2

    # Rozet kontrol
    sinav_sayi = len(ogr_results)
    ders_ort = defaultdict(list)
    for r in ogr_results:
        ders_ort[r["ders"]].append(r["puan"])

    for rozet in _ROZETLER:
        kosul = rozet["kosul"]
        kazandi = False
        if kosul == "ilk_sinav" and sinav_sayi >= 1:
            kazandi = True
        elif kosul == "mat_80":
            mat = ders_ort.get("Matematik", [])
            if len(mat) >= 3 and all(p >= 80 for p in mat[-3:]):
                kazandi = True
        elif kosul == "fen_80":
            fen = ders_ort.get("Fen Bilimleri", [])
            if len(fen) >= 3 and all(p >= 80 for p in fen[-3:]):
                kazandi = True
        elif kosul == "tur_80":
            tur = ders_ort.get("Turkce", [])
            if len(tur) >= 3 and all(p >= 80 for p in tur[-3:]):
                kazandi = True
        elif kosul == "puan_90":
            kazandi = any(r["puan"] >= 90 for r in ogr_results)
        elif kosul == "ardisik_5":
            if len(ogr_results) >= 5:
                kazandi = all(ogr_results[-(i+1)]["puan"] >= 60 for i in range(5))
        elif kosul == "gelisim_15":
            if len(ogr_results) >= 2:
                kazandi = (ogr_results[-1]["puan"] - ogr_results[-2]["puan"]) >= 15
        elif kosul == "4_ders_70":
            ders_70 = sum(1 for d, puanlar in ders_ort.items() if sum(puanlar)/len(puanlar) >= 70)
            kazandi = ders_70 >= 4
        elif kosul == "toplam_10":
            kazandi = sinav_sayi >= 10
        elif kosul == "toplam_xp_500":
            kazandi = xp >= 500

        if kazandi:
            xp += rozet["xp"]
            kazanilan_rozetler.append(rozet)

    return {"xp": xp, "sinav": sinav_sayi, "rozetler": kazanilan_rozetler, "ders_ort": dict(ders_ort)}


def render_gamifiye_sinav():
    """Gamifiye Sınav Deneyimi — XP, seviye, rozet, liderlik tablosu."""
    styled_section("Gamifiye Sinav Deneyimi & Liderlik Tablosu", "#c9a84c")
    styled_info_banner(
        "Sinav basarisini oyunlastir: XP kazan, seviye atla, rozet topla! "
        "Sinif/okul liderlik tablosu, aylik en iyi ogrenci odulu.",
        banner_type="info", icon="🏆")

    store = _store()
    results, exams = [], []
    if store:
        try:
            results = store.get_results()
            exams = store.get_exams()
        except Exception:
            pass

    if not results:
        st.info("Gamifiye icin sinav sonucu gerekli.")
        return

    ogr_map = {}
    for r in results:
        sid = getattr(r, 'student_id', '') or (r.get('student_id','') if isinstance(r, dict) else '')
        sname = getattr(r, 'student_name', '') or (r.get('student_name','') if isinstance(r, dict) else '')
        if sid and sname:
            ogr_map[sid] = sname

    sub = st.tabs(["👤 Profil Kartim", "🏆 Liderlik", "🎖️ Rozet Vitrini", "📊 Istatistik"])

    # ── PROFİL KARTIM ──
    with sub[0]:
        styled_section("Oyuncu Profili")
        ogr_opts = list(ogr_map.values())
        sec = st.selectbox("Ogrenci", ogr_opts, key="gm_ogr")
        sec_sid = [s for s, n in ogr_map.items() if n == sec]
        if sec_sid:
            sec_sid = sec_sid[0]
            data = _hesapla_xp(sec_sid, results, exams)
            xp = data["xp"]
            seviye, s_ikon, s_renk, sonraki_xp, kalan = _seviye_bilgi(xp)
            ilerleme_pct = round((xp - (sonraki_xp - kalan - (sonraki_xp - kalan))) / max(kalan + (xp - (sonraki_xp - kalan)), 1) * 100) if kalan > 0 else 100
            # Basitlestirilmis ilerleme
            for (lo, hi), _ in _XP_TABLOSU.items():
                if lo <= xp < hi:
                    ilerleme_pct = round((xp - lo) / max(hi - lo, 1) * 100)
                    break

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1a2e,{s_renk}20);border:2px solid {s_renk};
                border-radius:20px;padding:24px 28px;text-align:center;">
                <div style="font-size:3rem;">{s_ikon}</div>
                <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:6px;">{sec}</div>
                <div style="color:{s_renk};font-weight:800;font-size:1rem;">{seviye}</div>
                <div style="color:{s_renk};font-weight:900;font-size:2rem;margin-top:8px;">{xp} XP</div>
                <div style="background:#1e293b;border-radius:6px;height:12px;margin:10px 20px;overflow:hidden;">
                    <div style="width:{ilerleme_pct}%;height:100%;background:{s_renk};border-radius:6px;"></div>
                </div>
                <div style="color:#64748b;font-size:0.7rem;">Sonraki seviye: {kalan} XP kaldi</div>
                <div style="color:#94a3b8;font-size:0.75rem;margin-top:6px;">
                    {data['sinav']} sinav | {len(data['rozetler'])} rozet</div>
            </div>""", unsafe_allow_html=True)

            # Rozetler
            if data["rozetler"]:
                styled_section("Kazanilan Rozetler")
                cols = st.columns(min(len(data["rozetler"]), 4))
                for i, r in enumerate(data["rozetler"]):
                    with cols[i % len(cols)]:
                        st.markdown(f"""
                        <div style="background:#0f172a;border:2px solid {r['renk']};border-radius:14px;
                            padding:12px;text-align:center;margin:4px 0;">
                            <div style="font-size:1.8rem;">{r['ikon']}</div>
                            <div style="color:{r['renk']};font-weight:800;font-size:0.75rem;">{r['ad']}</div>
                            <div style="color:#64748b;font-size:0.6rem;">+{r['xp']} XP</div>
                        </div>""", unsafe_allow_html=True)

    # ── LİDERLİK ──
    with sub[1]:
        styled_section("Okul Liderlik Tablosu")
        lider_list = []
        for sid, name in ogr_map.items():
            data = _hesapla_xp(sid, results, exams)
            lider_list.append({"ad": name, "xp": data["xp"], "sinav": data["sinav"],
                               "rozet": len(data["rozetler"])})

        lider_list.sort(key=lambda x: x["xp"], reverse=True)

        for sira, l in enumerate(lider_list[:20], 1):
            seviye, s_ikon, s_renk, _, _ = _seviye_bilgi(l["xp"])
            madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:3px 0;
                background:#0f172a;border-left:4px solid {s_renk};border-radius:0 10px 10px 0;
                {'border:1px solid #c9a84c;' if sira <= 3 else ''}">
                <span style="font-size:1.2rem;min-width:30px;text-align:center;">{madalya}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{l['ad']}</span>
                <span style="font-size:0.8rem;">{s_ikon}</span>
                <span style="color:{s_renk};font-weight:800;font-size:0.85rem;">{l['xp']} XP</span>
                <span style="color:#64748b;font-size:0.65rem;">{l['rozet']}🎖️</span>
            </div>""", unsafe_allow_html=True)

    # ── ROZET VİTRİNİ ──
    with sub[2]:
        styled_section("Tum Rozetler")
        cols = st.columns(3)
        for i, r in enumerate(_ROZETLER):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {r['renk']}30;border-radius:14px;
                    padding:14px;text-align:center;margin:4px 0;">
                    <div style="font-size:2rem;">{r['ikon']}</div>
                    <div style="color:{r['renk']};font-weight:800;font-size:0.8rem;margin-top:4px;">{r['ad']}</div>
                    <div style="color:#94a3b8;font-size:0.65rem;margin-top:2px;">{r['aciklama']}</div>
                    <div style="color:#c9a84c;font-size:0.7rem;font-weight:700;margin-top:4px;">+{r['xp']} XP</div>
                </div>""", unsafe_allow_html=True)

    # ── İSTATİSTİK ──
    with sub[3]:
        styled_section("Gamifiye Istatistikleri")
        tum_xp = []
        for sid in ogr_map:
            data = _hesapla_xp(sid, results, exams)
            tum_xp.append(data["xp"])
        if tum_xp:
            ort_xp = round(sum(tum_xp) / len(tum_xp))
            max_xp = max(tum_xp)
            seviye_dag = Counter()
            for xp in tum_xp:
                sev, _, _, _, _ = _seviye_bilgi(xp)
                seviye_dag[sev] += 1

            styled_stat_row([
                ("Ort XP", str(ort_xp), "#c9a84c", "⭐"),
                ("Max XP", str(max_xp), "#6366f1", "🔝"),
                ("Oyuncu", str(len(tum_xp)), "#3b82f6", "👥"),
            ])

            styled_section("Seviye Dagilimi")
            for (_, _), (sev, ikon, renk) in _XP_TABLOSU.items():
                sayi = seviye_dag.get(sev, 0)
                pct = round(sayi / max(len(tum_xp), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="font-size:1rem;">{ikon}</span>
                    <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{sev}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. WHAT-IF SINAV SİMÜLATÖRÜ & SENARYO MOTORU
# ════════════════════════════════════════════════════════���═══

def render_whatif_simulator():
    """What-If Sınav Simülatörü — puan simülasyonu, zorluk ayarlama, hedef hesaplayıcı."""
    styled_section("What-If Sinav Simulatoru & Senaryo Motoru", "#7c3aed")
    styled_info_banner(
        "'Bu sorulari dogru yapsaydim kac alirdim?' sorusunu yanitlar. "
        "Zorluk ayari, kazanim cikartma senaryolari, hedef puan hesaplayici.",
        banner_type="info", icon="🔮")

    store = _store()
    exams, results = [], []
    if store:
        try:
            exams = store.get_exams()
            results = store.get_results()
        except Exception:
            pass

    sub = st.tabs(["🎯 Puan Simulatoru", "⚖️ Zorluk Senaryosu", "🎯 Hedef Hesaplayici", "📊 Kazanim What-If"])

    # ── PUAN SİMÜLATÖRÜ ──
    with sub[0]:
        styled_section("Puan Simulatoru — 'Dogru Yapsaydim?'")
        st.caption("Bir sinav secin, kac soruyu dogru yapsaydiniz simule edin.")

        if not exams:
            st.info("Sinav verisi yok.")
        else:
            exam_opts = {f"{getattr(e,'name','') or getattr(e,'exam_type','')}": e for e in exams}
            sec_exam = st.selectbox("Sinav Sec", list(exam_opts.keys()), key="wi_exam")
            exam = exam_opts.get(sec_exam)

            if exam:
                soru_sayisi = getattr(exam, 'question_count', 0) or 20
                mevcut_puan = st.number_input("Mevcut Puaniniz", 0, 100, 60, key="wi_mevcut")
                ek_dogru = st.slider("Kac ek soru dogru olsaydi?", 0, max(soru_sayisi, 1), 3, key="wi_ek")

                soru_puan = 100 / max(soru_sayisi, 1)
                simule_puan = min(100, round(mevcut_puan + ek_dogru * soru_puan))
                fark = simule_puan - mevcut_puan

                mevcut_renk = "#10b981" if mevcut_puan >= 70 else "#f59e0b" if mevcut_puan >= 50 else "#ef4444"
                simule_renk = "#10b981" if simule_puan >= 70 else "#f59e0b" if simule_puan >= 50 else "#ef4444"

                st.markdown(f"""
                <div style="display:flex;gap:16px;margin:14px 0;">
                    <div style="flex:1;background:#0f172a;border:2px solid {mevcut_renk};border-radius:16px;
                        padding:16px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.75rem;">Mevcut</div>
                        <div style="color:{mevcut_renk};font-weight:900;font-size:2.5rem;">{mevcut_puan}</div>
                    </div>
                    <div style="display:flex;align-items:center;color:#94a3b8;font-size:1.5rem;">→</div>
                    <div style="flex:1;background:#0f172a;border:2px solid {simule_renk};border-radius:16px;
                        padding:16px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.75rem;">Simule (+{ek_dogru} dogru)</div>
                        <div style="color:{simule_renk};font-weight:900;font-size:2.5rem;">{simule_puan}</div>
                    </div>
                </div>
                <div style="text-align:center;color:#c9a84c;font-weight:700;font-size:0.9rem;">
                    +{ek_dogru} dogru = +{round(fark)} puan artis
                </div>""", unsafe_allow_html=True)

    # ── ZORLUK SENARYOSU ──
    with sub[1]:
        styled_section("Zorluk Ayari Senaryosu (Ogretmen)")
        st.caption("Sinav zorlugunu degistirseniz ortalama nasil etkilenir?")

        if not results:
            st.info("Sonuc verisi yok.")
        else:
            puanlar = [getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0)
                       for r in results]
            puanlar = [p for p in puanlar if isinstance(p, (int, float))]
            if puanlar:
                mevcut_ort = round(sum(puanlar) / len(puanlar), 1)
                zorluk_degisim = st.slider("Zorluk Degisimi (%)", -30, 30, 0, key="wi_zorluk")

                # Basit model: zorluk arttikca ortalama duser
                simule_ort = round(max(0, min(100, mevcut_ort - zorluk_degisim * 0.8)), 1)
                basari_mevcut = round(sum(1 for p in puanlar if p >= 50) / len(puanlar) * 100)
                basari_simule = round(max(0, min(100, basari_mevcut - zorluk_degisim * 1.2)))

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    <div style="background:#0f172a;border-radius:14px;padding:16px;text-align:center;border:1px solid #334155;">
                        <div style="color:#94a3b8;font-size:0.75rem;">Mevcut Ortalama</div>
                        <div style="color:#3b82f6;font-weight:900;font-size:2rem;">{mevcut_ort}</div>
                        <div style="color:#64748b;font-size:0.7rem;">Basari: %{basari_mevcut}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    renk = "#10b981" if simule_ort > mevcut_ort else "#ef4444" if simule_ort < mevcut_ort else "#94a3b8"
                    st.markdown(f"""
                    <div style="background:#0f172a;border-radius:14px;padding:16px;text-align:center;border:2px solid {renk};">
                        <div style="color:#94a3b8;font-size:0.75rem;">Simule ({'+' if zorluk_degisim > 0 else ''}{zorluk_degisim}% zorluk)</div>
                        <div style="color:{renk};font-weight:900;font-size:2rem;">{simule_ort}</div>
                        <div style="color:#64748b;font-size:0.7rem;">Basari: %{basari_simule}</div>
                    </div>""", unsafe_allow_html=True)

    # ── HEDEF HESAPLAYICI ──
    with sub[2]:
        styled_section("Hedef Puan Hesaplayici")
        st.caption("Hedef puana ulasmak icin kac soru dogru olmali?")

        soru_sayisi = st.number_input("Sinavdaki Toplam Soru", 5, 100, 20, key="wi_h_soru")
        hedef_puan = st.number_input("Hedef Puan", 0, 100, 70, key="wi_h_hedef")
        negatif = st.checkbox("Negatif puanlama var mi? (4 yanlis = 1 dogru)", key="wi_h_neg")

        soru_puan = 100 / max(soru_sayisi, 1)
        gereken_dogru = math.ceil(hedef_puan / soru_puan)

        if negatif:
            # 4 yanlis 1 dogruyu goturur
            max_yanlis = (soru_sayisi - gereken_dogru)
            net_kayip = max_yanlis // 4
            gereken_dogru_neg = gereken_dogru + net_kayip
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #7c3aed;border-radius:16px;
                padding:20px;text-align:center;margin:10px 0;">
                <div style="color:#94a3b8;font-size:0.8rem;">Hedef: {hedef_puan} puan ({soru_sayisi} soru, negatif)</div>
                <div style="color:#7c3aed;font-weight:900;font-size:3rem;margin-top:8px;">{min(gereken_dogru_neg, soru_sayisi)}</div>
                <div style="color:#e2e8f0;font-size:0.85rem;">dogru soru gerekli</div>
                <div style="color:#64748b;font-size:0.7rem;margin-top:6px;">
                    (Negatif kayip hesabiyla: {gereken_dogru} net + {net_kayip} telafi)</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #7c3aed;border-radius:16px;
                padding:20px;text-align:center;margin:10px 0;">
                <div style="color:#94a3b8;font-size:0.8rem;">Hedef: {hedef_puan} puan ({soru_sayisi} soru)</div>
                <div style="color:#7c3aed;font-weight:900;font-size:3rem;margin-top:8px;">{min(gereken_dogru, soru_sayisi)}</div>
                <div style="color:#e2e8f0;font-size:0.85rem;">dogru soru gerekli</div>
                <div style="color:#64748b;font-size:0.7rem;margin-top:6px;">
                    Her soru {round(soru_puan, 1)} puan degerinde</div>
            </div>""", unsafe_allow_html=True)

    # ── KAZANIM WHAT-IF ──
    with sub[3]:
        styled_section("Kazanim Bazli What-If")
        st.caption("Belirli kazanimlari cikartsaniz sinav ortalamasi nasil degisir?")

        if not exams:
            st.info("Sinav verisi yok.")
        else:
            sec_exam2 = st.selectbox("Sinav",
                [f"{getattr(e,'name','') or getattr(e,'exam_type','')}" for e in exams], key="wi_kz_exam")

            kazanim_sayisi = st.number_input("Sinavdaki Kazanim Sayisi", 1, 30, 8, key="wi_kz_sayi")
            cikarilacak = st.slider("Kac kazanim cikartilasin?", 0, kazanim_sayisi, 2, key="wi_kz_cikar")

            if results:
                puanlar = [getattr(r, 'score', 0) or (r.get('score',0) if isinstance(r, dict) else 0) for r in results]
                puanlar = [p for p in puanlar if isinstance(p, (int, float))]
                if puanlar:
                    mevcut_ort = round(sum(puanlar) / len(puanlar), 1)
                    # Kazanim cikartma etkisi: soru azalir, kalan sorulardaki ortalama artar
                    kalan_oran = (kazanim_sayisi - cikarilacak) / max(kazanim_sayisi, 1)
                    simule_ort = round(min(100, mevcut_ort / max(kalan_oran, 0.3)), 1)

                    renk = "#10b981" if simule_ort > mevcut_ort else "#ef4444"
                    fark = round(simule_ort - mevcut_ort, 1)

                    st.markdown(f"""
                    <div style="background:#0f172a;border-radius:14px;padding:16px;margin:10px 0;">
                        <div style="display:flex;justify-content:center;gap:30px;">
                            <div style="text-align:center;">
                                <div style="color:#94a3b8;font-size:0.72rem;">Mevcut ({kazanim_sayisi} kazanim)</div>
                                <div style="color:#3b82f6;font-weight:900;font-size:2rem;">{mevcut_ort}</div>
                            </div>
                            <div style="color:#94a3b8;font-size:1.5rem;align-self:center;">→</div>
                            <div style="text-align:center;">
                                <div style="color:#94a3b8;font-size:0.72rem;">Simule ({kazanim_sayisi - cikarilacak} kazanim)</div>
                                <div style="color:{renk};font-weight:900;font-size:2rem;">{simule_ort}</div>
                            </div>
                        </div>
                        <div style="text-align:center;color:{renk};font-weight:700;font-size:0.85rem;margin-top:8px;">
                            {cikarilacak} kazanim cikarildi → {'+' if fark > 0 else ''}{fark} puan fark</div>
                    </div>""", unsafe_allow_html=True)
