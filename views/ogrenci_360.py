"""
Öğrenci 360° Profil Ekranı
============================
Bir öğrencinin A'dan Z'ye TÜM verilerini tek sayfada gösterir.
Tüm modüllerden CrossModuleLoader + doğrudan store ile veri çeker.
"""

from __future__ import annotations
import streamlit as st
import os
from datetime import date
import plotly.graph_objects as go

# ────────────────────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────────────────────

def _inject_360_css():
    if st.session_state.get("_360_css"):
        return
    st.session_state["_360_css"] = True
    st.markdown("""<style>
    .s360-hero{background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;
        padding:22px 26px;margin-bottom:18px;border:1px solid rgba(99,102,241,.15);position:relative;overflow:hidden;}
    .s360-hero::before{content:'';position:absolute;top:-40px;right:-40px;width:160px;height:160px;
        background:radial-gradient(circle,rgba(99,102,241,.12),transparent 70%);border-radius:50%;}
    .s360-hero h2{margin:0;font-size:22px;color:#fff;font-weight:800;}
    .s360-hero .sub{color:#94a3b8;font-size:13px;margin-top:3px;}
    .s360-hero .badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;
        font-weight:700;color:#fff;margin-left:8px;}
    .s360-stat{background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;
        border-radius:12px;padding:12px 14px;text-align:center;}
    .s360-stat .num{font-size:22px;font-weight:800;color:#fff;}
    .s360-stat .lbl{font-size:11px;color:#94a3b8;margin-top:2px;}
    .s360-sec{background:#0f172a;border:1px solid #1e293b;border-radius:12px;
        padding:14px 18px;margin:8px 0;border-left:3px solid var(--clr,#6366f1);}
    .s360-sec h4{margin:0 0 8px;font-size:15px;color:#e2e8f0;font-weight:700;}
    .s360-row{display:flex;justify-content:space-between;padding:4px 0;
        border-bottom:1px solid #1e293b;font-size:13px;color:#cbd5e1;}
    .s360-row:last-child{border-bottom:none;}
    .s360-row .val{font-weight:600;}
    .s360-alert{background:#ef444410;border-left:3px solid #ef4444;border-radius:0 8px 8px 0;
        padding:6px 12px;margin:4px 0;font-size:12px;color:#fca5a5;}
    .s360-ok{background:#22c55e10;border-left:3px solid #22c55e;border-radius:0 8px 8px 0;
        padding:6px 12px;margin:4px 0;font-size:12px;color:#86efac;}
    .s360-warn{background:#f59e0b10;border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;
        padding:6px 12px;margin:4px 0;font-size:12px;color:#fcd34d;}
    </style>""", unsafe_allow_html=True)


def _sec(title, icon, color, content_html):
    """Seksion wrapper."""
    st.markdown(f'<div class="s360-sec" style="--clr:{color};"><h4>{icon} {title}</h4>{content_html}</div>',
                unsafe_allow_html=True)


def _row(label, value, color=""):
    clr = f'color:{color};' if color else ''
    return f'<div class="s360-row"><span>{label}</span><span class="val" style="{clr}">{value}</span></div>'


def _alert(text):
    return f'<div class="s360-alert">⚠️ {text}</div>'


def _ok(text):
    return f'<div class="s360-ok">✅ {text}</div>'


def _warn(text):
    return f'<div class="s360-warn">⚡ {text}</div>'


# ────────────────────────────────────────────────────────────
# VERİ TOPLAMA
# ────────────────────────────────────────────────────────────

def _collect_student_data(sid: str, stu: dict) -> dict:
    """Tüm modüllerden öğrenci verisini topla."""
    from models.erken_uyari import CrossModuleLoader as CML

    d: dict = {"stu": stu, "sid": sid}
    name = f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip()
    d["name"] = name

    # ── Akademik ──
    d["grades"] = [g for g in CML.load_grades() if g.get("student_id") == sid]
    d["attendance"] = [a for a in CML.load_attendance() if a.get("student_id") == sid]
    d["exams"] = [e for e in CML.load_exam_results() if e.get("student_id") == sid]
    d["hw_subs"] = [h for h in CML.load_homework_submissions() if h.get("student_id") == sid]

    # ── Kazanım & Telafi ──
    d["borc"] = [b for b in CML.load_kazanim_borclari() if b.get("student_id") == sid]
    d["telafi"] = [t for t in CML.load_telafi_tasks() if t.get("student_id") == sid]

    # ── Rehberlik ──
    d["vakalar"] = [v for v in CML.load_rehberlik_vakalar() if v.get("ogrenci_id") == sid]
    d["gorusmeler"] = [g for g in CML.load_rehberlik_gorusmeler() if g.get("ogrenci_id") == sid]
    d["rhb_testler"] = CML.load_rehberlik_testler()
    d["rhb_oturumlar"] = [o for o in CML.load_rehberlik_test_oturumlari() if o.get("ogrenci_id") == sid]
    d["rhb_cevaplar"] = [c for c in CML.load_rehberlik_test_cevaplari() if c.get("ogrenci_id") == sid]

    # ── Aile Bilgi ──
    d["aile_bilgi"] = [f for f in CML.load_aile_bilgi_formlari() if f.get("ogrenci_id") == sid]

    # ── MEB Dijital Formlar ──
    all_meb = CML.load_all_meb_forms()
    meb_ogr: dict[str, list] = {}
    for sk, flist in all_meb.items():
        for f in flist:
            if f.get("ogrenci_id") == sid:
                meb_ogr.setdefault(sk, []).append(f)
    d["meb_forms"] = meb_ogr
    d["meb_total"] = sum(len(v) for v in meb_ogr.values())

    # ── Sağlık ──
    d["saglik"] = [s for s in CML.load_saglik_ziyaretleri() if s.get("ogrenci_id") == sid]

    # ── Yabancı Dil ──
    d["yd_results"] = [r for r in CML.load_yd_results() if r.get("student_id") == sid]
    d["cefr_mock"] = [r for r in CML.load_cefr_mock_results() if r.get("student_id") == sid]
    try:
        from models.cefr_exam import CEFRPlacementStore
        _cp = CEFRPlacementStore()
        d["cefr_placement"] = [r for r in _cp._load(_cp._results_path) if r.get("student_id") == sid]
    except Exception:
        d["cefr_placement"] = []

    # ── Erken Uyarı ──
    try:
        from models.erken_uyari import ErkenUyariStore
        eu = ErkenUyariStore()
        all_risks = eu.load_risks()
        ogr_risks = [r for r in all_risks if r.get("student_id") == sid]
        d["risk_history"] = sorted(ogr_risks, key=lambda x: x.get("calculated_at", ""), reverse=True)
        d["latest_risk"] = d["risk_history"][0] if d["risk_history"] else None
    except Exception:
        d["risk_history"] = []
        d["latest_risk"] = None

    # ── Eğitim Koçluğu (tam veri) ──
    try:
        from models.egitim_koclugu import get_ek_store
        ek = get_ek_store()
        all_ogr = ek.load_list("ogrenciler") if hasattr(ek, "load_list") else []
        d["kocluk"] = None
        for o in all_ogr:
            od = o if isinstance(o, dict) else (o.to_dict() if hasattr(o, "to_dict") else {})
            if od.get("ogrenci_id") == sid or (name and name.upper() in (od.get("ad", "") + " " + od.get("soyad", "")).upper()):
                d["kocluk"] = od
                break
        d["ek_gorusmeler"] = ek.get_by_ogrenci("gorusmeler", sid)
        d["ek_hedefler"] = ek.get_by_ogrenci("hedefler", sid)
        d["ek_haftalik_planlar"] = ek.get_by_ogrenci("haftalik_planlar", sid)
        d["ek_motivasyon"] = ek.get_by_ogrenci("motivasyon", sid)
        d["ek_deneme"] = ek.get_by_ogrenci("deneme_analizleri", sid)
        d["ek_veli_raporlari"] = ek.get_by_ogrenci("veli_raporlari", sid)
        d["ek_calisma_takvim"] = ek.get_by_ogrenci("calisma_takvim", sid)
        d["ek_odevler"] = ek.get_by_ogrenci("odevler", sid)
        d["ek_canli_dersler"] = ek.get_by_ogrenci("canli_dersler", sid)
        d["ek_soru_kutusu"] = ek.get_by_ogrenci("soru_kutusu", sid)
        d["ek_online_testler"] = ek.get_by_ogrenci("online_testler", sid)
    except Exception:
        d["kocluk"] = None
        for _k in ("ek_gorusmeler", "ek_hedefler", "ek_haftalik_planlar", "ek_motivasyon",
                    "ek_deneme", "ek_veli_raporlari", "ek_calisma_takvim", "ek_odevler",
                    "ek_canli_dersler", "ek_soru_kutusu", "ek_online_testler"):
            d[_k] = []

    # ── KYT ──
    d["kyt"] = [k for k in CML.load_kyt_answers() if k.get("student_id") == sid]

    # ── Kayıt Modülü Testleri (9 tür: Çoklu Zeka, VARK, Seviye, CEFR, HHT-1, Checkup) ──
    d["kayit_testler"] = CML.load_kayit_testler(ogrenci_adi=name)

    # ── TÜM TEST SONUÇLARI BİRLEŞİK (Rehberlik + Kayıt) ──
    d["tum_testler"] = CML.load_all_student_tests(ogrenci_id=sid, ogrenci_adi=name)

    # ── Akademik Takip Ek Veriler (müdahale, destek planı, öğretmen önerileri, sertifikalar) ──
    try:
        from models.akademik_takip import get_akademik_store
        at = get_akademik_store()
        d["mudahaleler"] = at.get_mudahaleler(student_id=sid) if hasattr(at, "get_mudahaleler") else []
        d["destek_planlari"] = at.get_destek_planlari(student_id=sid) if hasattr(at, "get_destek_planlari") else []
        d["ogretmen_onerileri"] = at.get_ogretmen_onerileri(student_id=sid) if hasattr(at, "get_ogretmen_onerileri") else []
        d["sertifikalar"] = at.get_certificates(student_id=sid) if hasattr(at, "get_certificates") else []
    except Exception:
        d["mudahaleler"] = []
        d["destek_planlari"] = []
        d["ogretmen_onerileri"] = []
        d["sertifikalar"] = []

    # ── Kütüphane (ödünç geçmişi) ──
    try:
        from models.kutuphane import KutuphaneDataStore
        from utils.tenant import get_data_path
        ktp = KutuphaneDataStore(get_data_path("kutuphane"))
        all_odunc = ktp.load_list("odunc_islemleri")
        d["kutuphane_odunc"] = [o for o in all_odunc if o.get("odunc_alan_id") == sid]
    except Exception:
        d["kutuphane_odunc"] = []

    # ── Servis (ulaşım bilgisi) ──
    try:
        from models.servis_yonetimi import get_servis_store
        srv = get_servis_store()
        all_hatlar = srv.load_list("hatlar")
        stu_hatlar = [h for h in all_hatlar if sid in (h.get("ogrenci_ids") or [])]
        d["servis_hatlar"] = stu_hatlar
        all_binis = srv.load_list("binis")
        d["servis_binis"] = [b for b in all_binis if b.get("ogrenci_id") == sid]
    except Exception:
        d["servis_hatlar"] = []
        d["servis_binis"] = []

    # ── Sosyal Etkinlik & Kulüpler ──
    try:
        from models.sosyal_etkinlik import SosyalEtkinlikDataStore
        from utils.tenant import get_data_path
        se = SosyalEtkinlikDataStore(get_data_path("sosyal_etkinlik"))
        all_kulupler = se.load_list("kulupler")
        d["kulup_uyelikleri"] = [k for k in all_kulupler
                                  if any(sid in str(u) or name.upper() in str(u).upper()
                                         for u in (k.get("katilimcilar") or []))]
        all_etkinlikler = se.load_list("etkinlikler")
        d["etkinlik_katilim"] = [e for e in all_etkinlikler
                                  if any(sid in str(u) or name.upper() in str(u).upper()
                                         for u in (e.get("katilimcilar") or []))]
    except Exception:
        d["kulup_uyelikleri"] = []
        d["etkinlik_katilim"] = []

    # ── Gamification (rozet, XP, sıralama) ──
    try:
        from models.gamification import GamificationStore
        gam = GamificationStore()
        gam_profile = gam.get_or_create(sid)
        d["gamification"] = gam_profile.to_dict() if hasattr(gam_profile, "to_dict") else (gam_profile if isinstance(gam_profile, dict) else {})
    except Exception:
        d["gamification"] = {}

    # ── Matematik Dünyası ──
    try:
        from models.matematik_dunyasi import MatematikDataStore
        mat = MatematikDataStore()
        d["matematik_profil"] = mat.get_profile(sid) or {}
        d["matematik_oyunlar"] = mat.get_game_sessions(student_id=sid) if hasattr(mat, "get_game_sessions") else []
        d["matematik_dikkat"] = mat.get_dikkat_profili(sid) if hasattr(mat, "get_dikkat_profili") else None
    except Exception:
        d["matematik_profil"] = {}
        d["matematik_oyunlar"] = []
        d["matematik_dikkat"] = None

    # ── Bilişim Vadisi ──
    try:
        from models.bilisim_vadisi import BilisimDataStore
        bil = BilisimDataStore()
        d["bilisim_profil"] = bil.get_profil(sid) or {}
    except Exception:
        d["bilisim_profil"] = {}

    # ── Sanat Sokağı ──
    try:
        from models.sanat_sokagi import SanatDataStore
        snt = SanatDataStore()
        d["sanat_profil"] = snt.get_profil(sid) or {}
        d["sanat_eserler"] = snt.get_eserler(student_id=sid) if hasattr(snt, "get_eserler") else []
    except Exception:
        d["sanat_profil"] = {}
        d["sanat_eserler"] = []

    # ── English Progress & Speaking ──
    try:
        from models.english_progress import EnglishProgressStore
        ep = EnglishProgressStore()
        d["eng_completions"] = ep.get_student_completions(sid)
        d["eng_streak"] = ep.calculate_streak(sid) if hasattr(ep, "calculate_streak") else 0
    except Exception:
        d["eng_completions"] = []
        d["eng_streak"] = 0

    try:
        from models.speaking_assessment import SpeakingStore
        spk = SpeakingStore()
        d["speaking_stats"] = spk.get_student_speaking_stats(sid) if hasattr(spk, "get_student_speaking_stats") else {}
    except Exception:
        d["speaking_stats"] = {}

    # ── Randevu & Ziyaretçi (veli görüşmeleri) ──
    try:
        from models.randevu_ziyaretci import RZYDataStore
        from utils.tenant import get_data_path
        rzy = RZYDataStore(get_data_path("akademik"))
        if hasattr(rzy, "find_by_field"):
            d["randevular"] = rzy.find_by_field("randevular", "student_id", sid)
        else:
            all_r = rzy.load_list("randevular") if hasattr(rzy, "load_list") else []
            d["randevular"] = [r for r in all_r if r.get("student_id") == sid]
    except Exception:
        d["randevular"] = []

    # ── TREND ANALİZİ (yıl/ay bazlı) ──
    d["trend"] = _compute_trends(d)

    return d


def _get_egitim_yili(tarih_str: str) -> str:
    """Tarihten eğitim yılını hesapla (Eylül-Ağustos). '2025-11-03' → '2025-2026'"""
    try:
        parts = str(tarih_str)[:10].split("-")
        y, m = int(parts[0]), int(parts[1])
        if m >= 9:
            return f"{y}-{y+1}"
        else:
            return f"{y-1}-{y}"
    except Exception:
        return "?"


def _get_ay(tarih_str: str) -> str:
    """'2025-11-03' → '2025-11'"""
    return str(tarih_str)[:7] if tarih_str else ""


def _compute_trends(d: dict) -> dict:
    """Yıl/ay bazlı trend verileri hesapla."""
    t: dict = {
        "yil_bazli": {},      # {egitim_yili: {ort, devamsiz, sinav_ort, risk, gorusme, ...}}
        "ay_bazli_not": {},   # {ay: ortalama}
        "ay_bazli_devam": {}, # {ay: ozursuz_gun}
        "risk_trend": [],     # [{tarih, skor, seviye}]
        "donum_noktalari": [],# [{tarih, olay, etki}]
        "mudahale_etkinlik": [],  # [{mudahale, oncesi, sonrasi, etki}]
    }

    # ── Yıl Bazlı Gruplama ──
    yillar: dict[str, dict] = {}

    # Notlar
    for g in d.get("grades", []):
        tarih = g.get("tarih", g.get("date", g.get("created_at", "")))
        ey = _get_egitim_yili(tarih)
        yillar.setdefault(ey, {"notlar": [], "devamsiz": [], "sinav": [], "gorusme": 0, "vaka": 0, "test": 0})
        try:
            yillar[ey]["notlar"].append(float(g.get("puan", 0)))
        except (ValueError, TypeError):
            pass

    # Devamsızlık
    for a in d.get("attendance", []):
        tarih = a.get("tarih", a.get("date", ""))
        ey = _get_egitim_yili(tarih)
        yillar.setdefault(ey, {"notlar": [], "devamsiz": [], "sinav": [], "gorusme": 0, "vaka": 0, "test": 0})
        ozursuz = "ozursuz" in str(a.get("turu", "")).lower()
        yillar[ey]["devamsiz"].append({"tarih": tarih, "ozursuz": ozursuz})
        # Ay bazlı
        ay = _get_ay(tarih)
        if ay and ozursuz:
            t["ay_bazli_devam"][ay] = t["ay_bazli_devam"].get(ay, 0) + 1

    # Sınav
    for e in d.get("exams", []):
        tarih = e.get("tarih", e.get("date", ""))
        ey = _get_egitim_yili(tarih)
        yillar.setdefault(ey, {"notlar": [], "devamsiz": [], "sinav": [], "gorusme": 0, "vaka": 0, "test": 0})
        try:
            yillar[ey]["sinav"].append(float(e.get("score", e.get("puan", 0))))
        except (ValueError, TypeError):
            pass

    # Görüşmeler
    for g in d.get("gorusmeler", []):
        tarih = g.get("tarih", "")
        ey = _get_egitim_yili(tarih)
        yillar.setdefault(ey, {"notlar": [], "devamsiz": [], "sinav": [], "gorusme": 0, "vaka": 0, "test": 0})
        yillar[ey]["gorusme"] += 1

    # Vakalar
    for v in d.get("vakalar", []):
        tarih = v.get("tarih", v.get("created_at", ""))
        ey = _get_egitim_yili(tarih)
        yillar.setdefault(ey, {"notlar": [], "devamsiz": [], "sinav": [], "gorusme": 0, "vaka": 0, "test": 0})
        yillar[ey]["vaka"] += 1

    # Yıl bazlı özet
    for ey, data in sorted(yillar.items()):
        notlar = data["notlar"]
        devam = data["devamsiz"]
        sinav = data["sinav"]
        t["yil_bazli"][ey] = {
            "not_ort": round(sum(notlar) / len(notlar), 1) if notlar else 0,
            "not_sayisi": len(notlar),
            "devamsiz_toplam": len(devam),
            "devamsiz_ozursuz": sum(1 for d2 in devam if d2.get("ozursuz")),
            "sinav_ort": round(sum(sinav) / len(sinav), 1) if sinav else 0,
            "sinav_sayisi": len(sinav),
            "gorusme": data["gorusme"],
            "vaka": data["vaka"],
        }

    # Ay bazlı not ortalaması
    for g in d.get("grades", []):
        tarih = g.get("tarih", g.get("date", g.get("created_at", "")))
        ay = _get_ay(tarih)
        if ay:
            t["ay_bazli_not"].setdefault(ay, [])
            try:
                t["ay_bazli_not"][ay].append(float(g.get("puan", 0)))
            except (ValueError, TypeError):
                pass
    # Ortalamalara çevir
    t["ay_bazli_not"] = {ay: round(sum(v) / len(v), 1) for ay, v in sorted(t["ay_bazli_not"].items()) if v}

    # ── Risk Trend ──
    for r in sorted(d.get("risk_history", []), key=lambda x: x.get("calculated_at", "")):
        t["risk_trend"].append({
            "tarih": r.get("calculated_at", "")[:10],
            "skor": r.get("risk_score", 0),
            "seviye": r.get("risk_level", "?"),
        })

    # ── Dönüm Noktası Tespiti ──
    # Yıllar arası büyük değişimleri bul
    yil_list = sorted(t["yil_bazli"].items())
    for i in range(1, len(yil_list)):
        prev_ey, prev = yil_list[i - 1]
        curr_ey, curr = yil_list[i]
        # Not düşüşü > 10 puan
        if prev["not_ort"] > 0 and curr["not_ort"] > 0:
            diff = curr["not_ort"] - prev["not_ort"]
            if diff < -10:
                t["donum_noktalari"].append({
                    "tarih": curr_ey, "olay": f"Not ortalamasi {abs(diff):.0f} puan dustu",
                    "etki": f"{prev_ey}: {prev['not_ort']:.0f} → {curr_ey}: {curr['not_ort']:.0f}",
                    "tur": "akademik_dusus",
                })
        # Devamsızlık artışı > %100
        if prev["devamsiz_ozursuz"] > 0 and curr["devamsiz_ozursuz"] > prev["devamsiz_ozursuz"] * 2:
            t["donum_noktalari"].append({
                "tarih": curr_ey, "olay": "Ozursuz devamsizlik 2 kattan fazla artti",
                "etki": f"{prev_ey}: {prev['devamsiz_ozursuz']} gun → {curr_ey}: {curr['devamsiz_ozursuz']} gun",
                "tur": "devamsizlik_artis",
            })
        # Vaka açılması
        if curr["vaka"] > 0 and prev["vaka"] == 0:
            t["donum_noktalari"].append({
                "tarih": curr_ey, "olay": f"{curr['vaka']} yeni rehberlik vakasi acildi",
                "etki": "Psikososyal mudahale basladi",
                "tur": "rehberlik_vaka",
            })

    # ── Müdahale Etkinliği Analizi ──
    # Koçluk atanmış mı? Atandıysa sonrası nasıl?
    kocluk = d.get("kocluk")
    if kocluk and len(yil_list) >= 2:
        son = yil_list[-1][1]
        onceki = yil_list[-2][1]
        etki = "olumlu" if son["not_ort"] > onceki["not_ort"] else "olumsuz" if son["not_ort"] < onceki["not_ort"] else "notr"
        t["mudahale_etkinlik"].append({
            "mudahale": f"Egitim kocu atandi: {kocluk.get('koc_adi', '?')}",
            "oncesi": f"Not ort: {onceki['not_ort']:.0f}",
            "sonrasi": f"Not ort: {son['not_ort']:.0f}",
            "etki": etki,
        })

    # Görüşme yoğunluğu artışı → risk değişimi
    if len(yil_list) >= 2:
        son = yil_list[-1][1]
        onceki = yil_list[-2][1]
        if son["gorusme"] > onceki["gorusme"] * 2 and onceki["gorusme"] > 0:
            t["mudahale_etkinlik"].append({
                "mudahale": f"Gorusme yogunlugu artirildi ({onceki['gorusme']} → {son['gorusme']})",
                "oncesi": f"Onceki yil gorusme: {onceki['gorusme']}",
                "sonrasi": f"Bu yil gorusme: {son['gorusme']}",
                "etki": "takip_artirildi",
            })

    return t


# ────────────────────────────────────────────────────────────
# SEKSİYON RENDERER'LAR
# ────────────────────────────────────────────────────────────

def _render_hero(d: dict):
    """Üst başlık kartı."""
    stu = d["stu"]
    name = d["name"]
    sinif = f'{stu.get("sinif", "?")}/{stu.get("sube", "?")}'
    numara = stu.get("numara", "")
    risk = d.get("latest_risk")
    risk_score = risk.get("risk_score", 0) if risk else 0
    risk_level = risk.get("risk_level", "UNKNOWN") if risk else "UNKNOWN"

    level_colors = {"LOW": "#22c55e", "MEDIUM": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444", "UNKNOWN": "#64748b"}
    level_labels = {"LOW": "Düşük", "MEDIUM": "Orta", "HIGH": "Yüksek", "CRITICAL": "Kritik", "UNKNOWN": "Hesaplanmadı"}
    lc = level_colors.get(risk_level, "#64748b")
    ll = level_labels.get(risk_level, "?")

    st.markdown(
        f'<div class="s360-hero">'
        f'<h2>👤 {name} <span class="badge" style="background:{lc};">{ll} Risk — {risk_score:.0f}/100</span></h2>'
        f'<div class="sub">Sınıf: {sinif} | No: {numara} | '
        f'TC: {stu.get("tc_kimlik", "-")} | '
        f'Veli: {stu.get("veli_adi", "-")} {stu.get("veli_soyadi", "")} | '
        f'Tel: {stu.get("veli_tel", "-")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_stat_row(d: dict):
    """İstatistik kartları satırı."""
    # Akademik ortalama
    grades = d.get("grades", [])
    if grades:
        puanlar = [float(g.get("puan", 0)) for g in grades if g.get("puan")]
        ort = sum(puanlar) / len(puanlar) if puanlar else 0
    else:
        ort = 0

    # Devamsızlık
    att = d.get("attendance", [])
    ozursuz = sum(1 for a in att if "ozursuz" in str(a.get("turu", "")).lower() or "özürsüz" in str(a.get("turu", "")).lower())

    risk = d.get("latest_risk")
    risk_score = risk.get("risk_score", 0) if risk else 0
    risk_level = risk.get("risk_level", "-") if risk else "-"

    # YD
    yd = d.get("yd_results", [])
    yd_avg = 0
    if yd:
        yp = [float(r.get("score", r.get("puan", 0))) for r in yd if r.get("score") or r.get("puan")]
        yd_avg = sum(yp) / len(yp) if yp else 0

    cefr = d.get("cefr_placement", [])
    cefr_level = cefr[-1].get("cefr_level", "-") if cefr else "-"

    meb_total = d.get("meb_total", 0)
    abf_count = len(d.get("aile_bilgi", []))

    # Koçluk hedef
    ek_hdf = d.get("ek_hedefler", [])
    aktif_hedef = sum(1 for h in ek_hdf if h.get("durum") in ("Devam Ediyor", "Beklemede"))

    # Gamification
    gam = d.get("gamification", {})
    gam_xp = gam.get("total_xp", 0) if gam else 0

    # Kulüp
    kulup_cnt = len(d.get("kulup_uyelikleri", []))

    # Kütüphane
    odunc = d.get("kutuphane_odunc", [])
    kitap_cnt = len(odunc)

    cols = st.columns(9)
    stats = [
        ("📚 Akademik", f"{ort:.0f}", "#6366f1"),
        ("📅 Devamsız", f"{len(att)} ({ozursuz} öz.süz)", "#f59e0b" if ozursuz > 5 else "#22c55e"),
        ("⚠️ Risk", f"{risk_score:.0f} ({risk_level})", "#ef4444" if risk_score > 60 else "#f59e0b" if risk_score > 30 else "#22c55e"),
        ("🌍 YD", f"{yd_avg:.0f} / {cefr_level}", "#3b82f6"),
        ("🧭 Rehberlik", f"{len(d.get('vakalar', []))}V {len(d.get('gorusmeler', []))}G", "#0d9488"),
        ("🎓 Koçluk", f"{aktif_hedef} hedef", "#10b981"),
        ("🏆 XP", str(gam_xp), "#eab308"),
        ("🎭 Kulüp", str(kulup_cnt), "#f59e0b"),
        ("📖 Kitap", str(kitap_cnt), "#7c3aed"),
    ]
    for i, (lbl, val, clr) in enumerate(stats):
        with cols[i]:
            st.markdown(f'<div class="s360-stat"><div class="num" style="color:{clr};">{val}</div>'
                        f'<div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)


def _render_sec_akademik(d: dict):
    """1. Akademik — Notlar + Sınav."""
    h = ""
    grades = d.get("grades", [])
    if grades:
        # Ders bazlı ortalama
        ders_map: dict[str, list] = {}
        for g in grades:
            ders = g.get("ders", g.get("subject", "?"))
            try:
                ders_map.setdefault(ders, []).append(float(g.get("puan", 0)))
            except (ValueError, TypeError):
                pass
        for ders, puanlar in sorted(ders_map.items()):
            avg = sum(puanlar) / len(puanlar)
            clr = "#22c55e" if avg >= 70 else "#f59e0b" if avg >= 50 else "#ef4444"
            h += _row(f"{ders} ({len(puanlar)} not)", f"{avg:.0f}", clr)
    else:
        h += '<div style="color:#64748b;font-size:12px;">Not kaydı yok</div>'

    # Sınav sonuçları
    exams = d.get("exams", [])
    if exams:
        h += '<div style="margin-top:8px;font-weight:600;font-size:12px;color:#94a3b8;">Sınav Sonuçları:</div>'
        for e in sorted(exams, key=lambda x: x.get("tarih", ""), reverse=True)[:5]:
            sc = float(e.get("score", e.get("puan", 0)))
            clr = "#22c55e" if sc >= 70 else "#f59e0b" if sc >= 50 else "#ef4444"
            h += _row(e.get("exam_title", e.get("sinav_adi", "?"))[:30], f"{sc:.0f}", clr)
    _sec("Akademik Performans", "📚", "#6366f1", h)


def _render_sec_devamsizlik(d: dict):
    """2. Devamsızlık."""
    att = d.get("attendance", [])
    h = ""
    if att:
        ozurlu = sum(1 for a in att if "ozurlu" in str(a.get("turu", "")).lower() and "ozursuz" not in str(a.get("turu", "")).lower())
        ozursuz = sum(1 for a in att if "ozursuz" in str(a.get("turu", "")).lower() or "özürsüz" in str(a.get("turu", "")).lower())
        h += _row("Toplam Gün", str(len(att)))
        h += _row("Özürlü", str(ozurlu), "#22c55e")
        h += _row("Özürsüz", str(ozursuz), "#ef4444" if ozursuz > 5 else "#f59e0b")
        if ozursuz > 10:
            h += _alert(f"Özürsüz devamsızlık kritik: {ozursuz} gün")
        elif ozursuz > 5:
            h += _warn(f"Özürsüz devamsızlık dikkat: {ozursuz} gün")
    else:
        h += _ok("Devamsızlık kaydı yok")
    _sec("Devamsızlık", "📅", "#f59e0b", h)


def _render_sec_erken_uyari(d: dict):
    """3. Erken Uyarı — Risk."""
    risk = d.get("latest_risk")
    h = ""
    if risk:
        score = risk.get("risk_score", 0)
        level = risk.get("risk_level", "?")
        lc = {"LOW": "#22c55e", "MEDIUM": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444"}.get(level, "#64748b")
        h += _row("Risk Skoru", f"{score:.0f}/100", lc)
        h += _row("Risk Seviyesi", level, lc)

        # Alt risk bileşenleri
        components = [
            ("Not Riski", "grade_risk"), ("Devamsızlık Riski", "attendance_risk"),
            ("Sınav Riski", "exam_risk"), ("Ödev Riski", "homework_risk"),
            ("Kazanım Borcu", "outcome_debt_risk"), ("Rehberlik", "counseling_risk"),
            ("Sağlık", "health_risk"), ("Trend", "trend_risk"),
            ("Davranış", "behavior_risk"), ("Yabancı Dil", "foreign_lang_risk"),
        ]
        h += '<div style="margin-top:6px;font-size:11px;color:#64748b;">Alt Bileşenler:</div>'
        for lbl, key in components:
            val = risk.get(key, 0)
            if val > 0:
                vc = "#ef4444" if val > 60 else "#f59e0b" if val > 30 else "#22c55e"
                h += _row(f"  {lbl}", f"{val:.0f}", vc)

        # Trend
        history = d.get("risk_history", [])
        if len(history) >= 2:
            prev = history[1].get("risk_score", 0)
            diff = score - prev
            if diff > 5:
                h += _alert(f"Risk artıyor: +{diff:.0f} puan")
            elif diff < -5:
                h += _ok(f"Risk azalıyor: {diff:.0f} puan")

        # fl_perf detayları
        fl = risk.get("foreign_lang_performance", {})
        if fl.get("dehb_yonlendirme"):
            h += _alert("DEHB yönlendirme önerilmiş")
        if fl.get("oog_yonlendirme"):
            h += _alert("ÖÖG yönlendirme önerilmiş")
        if fl.get("psikolojik_acil"):
            h += _alert("Psikolojik destek — ACİL")
        if fl.get("ev_ziyareti_acil"):
            h += _alert("Ev ziyareti — acil takip")
        if fl.get("ebeveyn_kaybi"):
            h += _alert("Ebeveyn kaybı")
        if fl.get("aile_bosanmis"):
            h += _warn("Aile boşanmış/ayrı")
        if fl.get("travmatik_olay"):
            h += _alert(f"Travma: {fl['travmatik_olay']}")
    else:
        h += '<div style="color:#64748b;font-size:12px;">Risk henüz hesaplanmadı</div>'
    _sec("Erken Uyarı & Risk", "⚠️", "#ef4444", h)


def _render_sec_yabanci_dil(d: dict):
    """4. Yabancı Dil."""
    h = ""
    yd = d.get("yd_results", [])
    cefr = d.get("cefr_placement", [])
    mock = d.get("cefr_mock", [])

    if cefr:
        last = cefr[-1]
        h += _row("CEFR Seviye", last.get("cefr_level", "-"), "#3b82f6")
        h += _row("Yerleştirme Puanı", str(last.get("total_score", "-")))

    if yd:
        yp = [float(r.get("score", r.get("puan", 0))) for r in yd if r.get("score") or r.get("puan")]
        avg = sum(yp) / len(yp) if yp else 0
        clr = "#22c55e" if avg >= 70 else "#f59e0b" if avg >= 50 else "#ef4444"
        h += _row(f"Quiz/Sınav ({len(yd)} adet)", f"Ort: {avg:.0f}", clr)
        # Son 5
        h += '<div style="margin-top:4px;font-size:11px;color:#64748b;">Son Sınavlar:</div>'
        for r in sorted(yd, key=lambda x: x.get("tarih", x.get("date", "")), reverse=True)[:5]:
            sc = float(r.get("score", r.get("puan", 0)))
            vc = "#22c55e" if sc >= 70 else "#f59e0b" if sc >= 50 else "#ef4444"
            h += _row(f'  {r.get("exam_type", r.get("tur", "?"))} — {str(r.get("tarih", r.get("date", "")))[:10]}', f"{sc:.0f}", vc)

    if mock:
        h += f'<div style="margin-top:4px;">{_row("CEFR Mock Sınav", f"{len(mock)} adet")}</div>'

    if not yd and not cefr and not mock:
        h += '<div style="color:#64748b;font-size:12px;">YD verisi yok</div>'
    _sec("Yabancı Dil Gelişimi", "🌍", "#3b82f6", h)


def _render_sec_rehberlik(d: dict):
    """5. Rehberlik — Vaka + Görüşme + Test."""
    h = ""
    vakalar = d.get("vakalar", [])
    gorusmeler = d.get("gorusmeler", [])

    if vakalar:
        h += f'<div style="font-weight:600;font-size:12px;color:#94a3b8;margin-bottom:4px;">Vakalar ({len(vakalar)}):</div>'
        for v in vakalar:
            dur = v.get("durum", "?")
            dc = "#ef4444" if dur in ("ACIK", "TAKIPTE") else "#22c55e"
            h += _row(v.get("vaka_basligi", v.get("konu", "?"))[:40], dur, dc)

    if gorusmeler:
        h += f'<div style="font-weight:600;font-size:12px;color:#94a3b8;margin-top:6px;">Görüşmeler ({len(gorusmeler)}):</div>'
        for g in sorted(gorusmeler, key=lambda x: x.get("tarih", ""), reverse=True)[:5]:
            h += _row(g.get("gorusme_konusu", g.get("konu", "?"))[:40], str(g.get("tarih", ""))[:10])

    # Testler
    oturumlar = d.get("rhb_oturumlar", [])
    if oturumlar:
        tst_map = {t.get("id", ""): t for t in d.get("rhb_testler", [])}
        cevaplar = d.get("rhb_cevaplar", [])
        h += f'<div style="font-weight:600;font-size:12px;color:#94a3b8;margin-top:6px;">Testler ({len(oturumlar)}):</div>'
        for o in oturumlar:
            tst = tst_map.get(o.get("test_id", ""), {})
            durum = o.get("durum", "?")
            dc = "#22c55e" if durum == "TAMAMLANDI" else "#f59e0b"
            oc = [c for c in cevaplar if c.get("oturum_id") == o.get("id")]
            pp = [float(c.get("puan", 0)) for c in oc if c.get("puan")]
            avg_t = f" — Ort: {sum(pp)/len(pp):.1f}" if pp else ""
            h += _row(tst.get("test_adi", "?")[:35], f"{durum}{avg_t}", dc)

    if not vakalar and not gorusmeler and not oturumlar:
        h += '<div style="color:#64748b;font-size:12px;">Rehberlik kaydı yok</div>'
    _sec("Rehberlik (Vaka & Görüşme & Test)", "🧭", "#0d9488", h)


def _render_sec_aile_bilgi(d: dict):
    """6. Aile Bilgi Formu."""
    abf_list = d.get("aile_bilgi", [])
    h = ""
    if abf_list:
        abf = abf_list[-1]
        h += _row("Anne", f'{abf.get("anne_adi_soyadi", "-")} ({abf.get("anne_sag_olu", "?")} / {abf.get("anne_birlikte_bosanmis", "?")})')
        h += _row("Baba", f'{abf.get("baba_adi_soyadi", "-")} ({abf.get("baba_sag_olu", "?")} / {abf.get("baba_birlikte_bosanmis", "?")})')
        h += _row("Yaşam", abf.get("kiminle_nerede_yasiyor", "-"))
        h += _row("Kardeş", f'Öz: {abf.get("kardes_oz_sayisi", 0)}, Üvey: {abf.get("kardes_uvey_sayisi", 0)}')
        h += _row("Gelir", abf.get("ortalama_gelir", "-"))
        if abf.get("suregen_hastalik"):
            h += _alert(f"Süreğen hastalık: {abf['suregen_hastalik']}")
        if abf.get("etkisindeki_olay"):
            h += _alert(f"Travma: {abf['etkisindeki_olay']}")
        if abf.get("bagimllik_durumu"):
            h += _alert(f"Ailede bağımlılık: {abf['bagimllik_durumu']}")
        if abf.get("suca_karismis_birey"):
            h += _alert(f"Ailede suç: {abf['suca_karismis_birey']}")
    else:
        h += '<div style="color:#64748b;font-size:12px;">Aile bilgi formu doldurulmamış</div>'
    _sec("Aile Bilgi Formu (B.K.G.1.c)", "👨‍👩‍👧", "#0d9488", h)


def _render_sec_meb_formlar(d: dict):
    """7. MEB Dijital Formlar."""
    meb = d.get("meb_forms", {})
    h = ""
    if meb:
        try:
            from models.meb_formlar import MEB_FORM_SCHEMAS
        except ImportError:
            MEB_FORM_SCHEMAS = {}
        for sk, forms in meb.items():
            schema = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == sk), None)
            fname = schema["title"] if schema else sk
            ficon = schema.get("icon", "📄") if schema else "📄"
            clr = "#3b82f6"
            if sk in ("dehb_gozlem_formlari", "ozel_ogrenme_guclugu_formlari", "psikolojik_yonlendirme_formlari"):
                clr = "#ef4444"
            elif sk in ("disiplin_gorusme_formlari", "ev_ziyareti_formlari"):
                clr = "#f59e0b"
            h += _row(f"{ficon} {fname}", f"{len(forms)} kayıt", clr)
            # Son formdan önemli alanlar
            last = forms[-1]
            for key in ("yonlendirme_onerisi", "belirti_siddeti", "genel_degerlendirme",
                        "rehber_degerlendirme", "sonuc_oneri", "takip_gerekliligi"):
                val = last.get(key, "")
                if val and str(val).strip() and val != "Gözlenmedi":
                    label = key.replace("_", " ").title()
                    h += f'<div style="font-size:11px;color:#94a3b8;padding-left:16px;">└ {label}: {str(val)[:60]}</div>'
    else:
        h += '<div style="color:#64748b;font-size:12px;">MEB dijital form kaydı yok</div>'
    _sec("MEB Dijital Formlar", "📄", "#8b5cf6", h)


def _render_sec_saglik(d: dict):
    """8. Sağlık."""
    saglik = d.get("saglik", [])
    h = ""
    if saglik:
        h += _row("Ziyaret Sayısı", str(len(saglik)))
        takip = sum(1 for s in saglik if s.get("takip_gerekiyor"))
        if takip:
            h += _row("Takip Gereken", str(takip), "#f59e0b")
        for s in sorted(saglik, key=lambda x: x.get("basvuru_tarihi", ""), reverse=True)[:3]:
            h += _row(s.get("sikayet_kategorisi", "?"), str(s.get("basvuru_tarihi", ""))[:10])
    else:
        h += _ok("Sağlık ziyareti yok")
    _sec("Okul Sağlığı", "🏥", "#ec4899", h)


def _render_sec_telafi(d: dict):
    """9. Kazanım Borcu & Telafi."""
    borc = d.get("borc", [])
    telafi = d.get("telafi", [])
    h = ""
    if borc:
        acik = [b for b in borc if b.get("durum") == "borc_var"]
        h += _row("Açık Borç", str(len(acik)), "#ef4444" if acik else "#22c55e")
        h += _row("Kapatılan", str(len(borc) - len(acik)), "#22c55e")
        for b in acik[:3]:
            h += f'<div style="font-size:11px;color:#fca5a5;padding-left:10px;">• {b.get("ders","")} — {b.get("kazanim_kodu","")}</div>'
    if telafi:
        comp = sum(1 for t in telafi if t.get("status") == "completed")
        bands: dict[str, int] = {}
        for t in telafi:
            cb = t.get("color_band", "?")
            bands[cb] = bands.get(cb, 0) + 1
        h += _row("Telafi Görevi", f"{len(telafi)} ({comp} tamamlanan)")
        bs = " | ".join(f'{k}: {v}' for k, v in bands.items())
        h += f'<div style="font-size:11px;color:#94a3b8;">{bs}</div>'
    if not borc and not telafi:
        h += _ok("Kazanım borcu ve telafi görevi yok")
    _sec("Kazanım Borcu & Telafi", "🔄", "#f97316", h)


def _render_sec_kocluk(d: dict):
    """10. Eğitim Koçluğu (genişletilmiş)."""
    k = d.get("kocluk")
    h = ""
    if k:
        h += _row("Koç", k.get("koc_adi", "-"))
        h += _row("Motivasyon", f'{k.get("motivasyon_seviyesi", "-")}/5')
        h += _row("Hedef Sınav", f'{k.get("hedef_sinav", "-")} {k.get("hedef_puan", "")}')
        h += _row("Güçlü Dersler", k.get("guclu_dersler", "-"))
        h += _row("Zayıf Dersler", k.get("zayif_dersler", "-"))
    else:
        h += '<div style="color:#64748b;font-size:12px;">Koçluk kaydı yok</div>'

    # Görüşmeler
    grs = d.get("ek_gorusmeler", [])
    if grs:
        h += f'<div style="font-size:11px;font-weight:700;color:#10b981;margin:6px 0 2px;">Görüşmeler ({len(grs)})</div>'
        for g in sorted(grs, key=lambda x: x.get("tarih", ""), reverse=True)[:3]:
            h += _row(str(g.get("tarih", ""))[:10], f'{g.get("turu", "")} — {g.get("durum", "")}')

    # Hedefler
    hdf = d.get("ek_hedefler", [])
    if hdf:
        aktif = [x for x in hdf if x.get("durum") in ("Devam Ediyor", "Beklemede")]
        tamam = [x for x in hdf if x.get("durum") == "Tamamlandi"]
        h += _row("Hedefler", f"{len(aktif)} aktif / {len(tamam)} tamamlandı")

    # Motivasyon trendi
    mot = d.get("ek_motivasyon", [])
    if mot:
        last = sorted(mot, key=lambda x: x.get("tarih", ""), reverse=True)[0]
        h += _row("Son Motivasyon", f'{last.get("motivasyon", "-")}/5 ({str(last.get("tarih", ""))[:10]})')

    # Haftalık plan
    hpl = d.get("ek_haftalik_planlar", [])
    if hpl:
        h += _row("Haftalık Plan", f"{len(hpl)} plan")

    # Deneme analiz
    dnm = d.get("ek_deneme", [])
    if dnm:
        son = sorted(dnm, key=lambda x: x.get("tarih", ""), reverse=True)[0]
        h += _row("Son Deneme", f'{son.get("puan", "-")} puan ({str(son.get("tarih", ""))[:10]})')
        h += _row("Toplam Deneme", str(len(dnm)))

    # Canlı ders & soru kutusu
    cd = d.get("ek_canli_dersler", [])
    sk = d.get("ek_soru_kutusu", [])
    ot = d.get("ek_online_testler", [])
    extras = []
    if cd:
        extras.append(f"{len(cd)} canlı ders")
    if sk:
        extras.append(f"{len(sk)} soru")
    if ot:
        extras.append(f"{len(ot)} online test")
    if extras:
        h += _row("Etkinlik", " · ".join(extras))

    _sec("Eğitim Koçluğu", "🎓", "#10b981", h)


def _render_sec_odev_kyt(d: dict):
    """11. Ödev & KYT."""
    hw = d.get("hw_subs", [])
    kyt = d.get("kyt", [])
    h = ""
    if hw:
        teslim = sum(1 for s in hw if s.get("durum") in ("teslim_edildi", "degerlendirildi"))
        h += _row("Ödev Teslimi", f"{teslim}/{len(hw)}")
    if kyt:
        dogru = sum(1 for k in kyt if k.get("dogru"))
        h += _row("KYT Cevap", f"{len(kyt)} ({dogru} doğru)")
    if not hw and not kyt:
        h += '<div style="color:#64748b;font-size:12px;">Ödev/KYT kaydı yok</div>'
    _sec("Ödev & KYT", "📝", "#64748b", h)


def _render_sec_kayit_testler(d: dict):
    """12. TÜM TEST SONUÇLARI (Rehberlik + Kayıt birleşik)."""
    kt = d.get("tum_testler", []) or d.get("kayit_testler", [])
    h = ""
    if kt:
        test_types = {}
        for t in kt:
            test_types[t.get("test_adi", "?")] = test_types.get(t.get("test_adi", "?"), 0) + 1
        h += _row("Toplam Test", str(len(kt)))
        h += _row("Test Türleri", str(len(test_types)))
        for tn, cnt in sorted(test_types.items()):
            h += _row(f"  {tn}", str(cnt))
        # Her test detayı
        # Kaynak bazlı grupla
        rhb_tests = [t for t in kt if "Rehberlik" in t.get("kaynak", t.get("test_adi", ""))]
        km_tests = [t for t in kt if "Kayit" in t.get("kaynak", "")]
        if rhb_tests:
            h += f'<div style="font-size:11px;font-weight:600;color:#2dd4bf;margin:4px 0;">Rehberlik Testleri ({len(rhb_tests)}):</div>'
        if km_tests:
            h += f'<div style="font-size:11px;font-weight:600;color:#a78bfa;margin:4px 0;">Kayıt Modülü Testleri ({len(km_tests)}):</div>'

        for t in sorted(kt, key=lambda x: x.get("tarih", ""), reverse=True):
            kaynak = t.get("kaynak", "")
            k_clr = "#2dd4bf" if "Rehberlik" in kaynak else "#a78bfa"
            h += f'<div style="margin-top:4px;padding:5px 8px;background:#1e293b;border-radius:6px;border-left:3px solid {k_clr};">'
            h += f'<div style="font-size:12px;font-weight:600;color:{k_clr};">{t.get("test_adi", "?")} — {str(t.get("tarih", ""))[:10]}</div>'
            durum = t.get("durum", t.get("sonuc", "-"))
            h += f'<div style="font-size:10px;color:#94a3b8;">Durum: {durum} | Kaynak: {kaynak}</div>'
            # Genel ortalama
            if t.get("genel_ortalama"):
                h += f'<div style="font-size:10px;color:#fbbf24;">Genel Ort: {t["genel_ortalama"]}</div>'
            # Skorlar
            skorlar = t.get("skorlar", {})
            if skorlar:
                items = []
                for sk, sv in skorlar.items():
                    try:
                        val = float(sv)
                        clr = "#22c55e" if val >= 7 else "#f59e0b" if val >= 5 else "#ef4444"
                    except (ValueError, TypeError):
                        clr = "#94a3b8"
                    items.append(f'<span style="color:{clr};">{sk}: {sv}</span>')
                h += f'<div style="font-size:10px;">{" | ".join(items)}</div>'
            # Ölçek puanları
            olcek_p = t.get("olcek_puanlari", {})
            if olcek_p:
                items = [f'{ok}: {ov}' for ok, ov in olcek_p.items()]
                h += f'<div style="font-size:10px;color:#93c5fd;">Ölçek: {" | ".join(items)}</div>'
            # Top 3
            top3 = t.get("top3", [])
            if top3:
                for item in top3:
                    h += f'<div style="font-size:10px;color:#86efac;">★ {item.get("alan", "?")}: {item.get("skor", "-")} ({item.get("seviye", "")})</div>'
            h += '</div>'
    else:
        h += '<div style="color:#64748b;font-size:12px;">Henüz test uygulanmamış</div>'
    _sec("Tüm Test Sonuçları (Rehberlik + Kayıt)", "🧪", "#8b5cf6", h)


def _render_sec_mudahale_destek(d: dict):
    """Müdahale Kayıtları & Destek Planları & Öğretmen Önerileri."""
    mud = d.get("mudahaleler", [])
    dsp = d.get("destek_planlari", [])
    onr = d.get("ogretmen_onerileri", [])
    srt = d.get("sertifikalar", [])
    h = ""
    if mud:
        aktif = [m for m in mud if m.get("status") != "tamamlandi"]
        h += _row("Müdahale", f"{len(mud)} kayıt ({len(aktif)} aktif)")
        for m in sorted(mud, key=lambda x: x.get("created_at", ""), reverse=True)[:3]:
            h += _row(str(m.get("created_at", ""))[:10], m.get("mudahale_turu", m.get("type", "-")))
    if dsp:
        h += _row("Destek Planı", f"{len(dsp)} plan")
        for p in dsp[:2]:
            h += _row(p.get("plan_adi", "-"), p.get("status", "-"))
    if onr:
        h += _row("Öğretmen Önerisi", f"{len(onr)} öneri")
        for o in onr[:2]:
            h += _row(o.get("teacher_name", "-"), str(o.get("oneri", o.get("content", "-")))[:60])
    if srt:
        h += _row("Sertifika", f"{len(srt)} adet")
    if not mud and not dsp and not onr and not srt:
        h += '<div style="color:#64748b;font-size:12px;">Müdahale/destek kaydı yok</div>'
    _sec("Müdahale & Destek", "🛡️", "#dc2626", h)


def _render_sec_kutuphane(d: dict):
    """Kütüphane ödünç geçmişi."""
    odunc = d.get("kutuphane_odunc", [])
    h = ""
    if odunc:
        iade_bekleyen = [o for o in odunc if not o.get("iade_tarihi")]
        h += _row("Toplam Ödünç", str(len(odunc)))
        h += _row("İade Bekleyen", str(len(iade_bekleyen)), "#f59e0b" if iade_bekleyen else "")
        for o in sorted(odunc, key=lambda x: x.get("odunc_tarihi", ""), reverse=True)[:3]:
            durum = "📖 Okuyor" if not o.get("iade_tarihi") else "✅ İade"
            h += _row(o.get("materyal_adi", "-"), f'{durum} ({str(o.get("odunc_tarihi", ""))[:10]})')
    else:
        h += '<div style="color:#64748b;font-size:12px;">Kütüphane kaydı yok</div>'
    _sec("Kütüphane", "📚", "#7c3aed", h)


def _render_sec_servis(d: dict):
    """Servis/ulaşım bilgisi."""
    hatlar = d.get("servis_hatlar", [])
    binis = d.get("servis_binis", [])
    h = ""
    if hatlar:
        for ht in hatlar:
            h += _row("Güzergah", ht.get("hat_adi", ht.get("ad", "-")))
            duraklar = ht.get("duraklar", [])
            if duraklar:
                h += _row("Durak Sayısı", str(len(duraklar)))
    if binis:
        h += _row("Biniş Kaydı", f"{len(binis)} kayıt")
    if not hatlar and not binis:
        h += '<div style="color:#64748b;font-size:12px;">Servis kaydı yok</div>'
    _sec("Servis & Ulaşım", "🚌", "#0891b2", h)


def _render_sec_sosyal(d: dict):
    """Sosyal etkinlik & kulüp katılımı."""
    kulupler = d.get("kulup_uyelikleri", [])
    etkinlikler = d.get("etkinlik_katilim", [])
    h = ""
    if kulupler:
        h += _row("Kulüp Üyeliği", f"{len(kulupler)} kulüp")
        for k in kulupler:
            h += _row(k.get("kulup_adi", k.get("ad", "-")), k.get("durum", "Aktif"))
    if etkinlikler:
        h += _row("Etkinlik Katılımı", f"{len(etkinlikler)} etkinlik")
        for e in sorted(etkinlikler, key=lambda x: x.get("tarih", ""), reverse=True)[:3]:
            h += _row(e.get("baslik", e.get("ad", "-")), str(e.get("tarih", ""))[:10])
    if not kulupler and not etkinlikler:
        h += '<div style="color:#64748b;font-size:12px;">Etkinlik/kulüp kaydı yok</div>'
    _sec("Sosyal & Kulüpler", "🎭", "#f59e0b", h)


def _render_sec_gamification(d: dict):
    """Gamification — rozet, XP, seviye."""
    g = d.get("gamification", {})
    h = ""
    if g and g.get("total_xp", 0) > 0:
        h += _row("Seviye", f'{g.get("level", 1)} — {g.get("level_name", "")}')
        h += _row("Toplam XP", str(g.get("total_xp", 0)))
        h += _row("Haftalık XP", str(g.get("weekly_xp", 0)))
        h += _row("Seri", f'{g.get("streak_days", 0)} gün')
        h += _row("Doğruluk", f'{g.get("accuracy", 0):.0f}%')
        badges = g.get("badges_earned", [])
        if badges:
            h += _row("Rozet", f"{len(badges)} adet")
    else:
        h += '<div style="color:#64748b;font-size:12px;">Gamification kaydı yok</div>'
    _sec("Gamification", "🏆", "#eab308", h)


def _render_sec_icerik_modulleri(d: dict):
    """Matematik Dünyası + Bilişim Vadisi + Sanat Sokağı."""
    mat = d.get("matematik_profil", {})
    bil = d.get("bilisim_profil", {})
    snt = d.get("sanat_profil", {})
    eserler = d.get("sanat_eserler", [])
    oyunlar = d.get("matematik_oyunlar", [])
    dikkat = d.get("matematik_dikkat")
    h = ""

    # Matematik
    if mat and (mat.get("toplam_problemler") or mat.get("toplam_cozum")):
        h += f'<div style="font-size:11px;font-weight:700;color:#3b82f6;margin:4px 0;">🔢 Matematik Dünyası</div>'
        h += _row("Çözülen", str(mat.get("toplam_problemler", mat.get("toplam_cozum", 0))))
        h += _row("Doğru", str(mat.get("dogru_sayisi", mat.get("dogru", 0))))
        if mat.get("seviye"):
            h += _row("Seviye", str(mat.get("seviye", "-")))
    if oyunlar:
        h += _row("Oyun Oturumu", f"{len(oyunlar)} oturum")
    if dikkat:
        h += _row("Dikkat Profili", "✅ Mevcut")

    # Bilişim
    if bil and (bil.get("toplam_proje") or bil.get("basari_skoru")):
        h += f'<div style="font-size:11px;font-weight:700;color:#10b981;margin:6px 0 2px;">💻 Bilişim Vadisi</div>'
        h += _row("Proje", f'{bil.get("tamamlanan_proje", 0)}/{bil.get("toplam_proje", 0)}')
        if bil.get("basari_skoru"):
            h += _row("Başarı", f'{bil.get("basari_skoru", 0)}')

    # Sanat
    if snt and (snt.get("toplam_aktivite") or eserler):
        h += f'<div style="font-size:11px;font-weight:700;color:#f59e0b;margin:6px 0 2px;">🎨 Sanat Sokağı</div>'
        if snt.get("toplam_aktivite"):
            h += _row("Aktivite", str(snt.get("toplam_aktivite", 0)))
            h += _row("Süre", f'{snt.get("toplam_sure_dk", 0)} dk')
        if eserler:
            h += _row("Eser", f"{len(eserler)} adet")

    if not mat and not bil and not snt and not oyunlar and not eserler:
        h += '<div style="color:#64748b;font-size:12px;">İçerik modülü kaydı yok</div>'
    _sec("İçerik Modülleri", "🎮", "#6366f1", h)


def _render_sec_eng_speaking(d: dict):
    """English Progress & Speaking Assessment."""
    comp = d.get("eng_completions", [])
    streak = d.get("eng_streak", 0)
    spk = d.get("speaking_stats", {})
    h = ""
    if comp:
        h += _row("Tamamlanan Alıştırma", str(len(comp)))
        if streak:
            h += _row("Çalışma Serisi", f"{streak} gün")
    if spk and spk.get("total_attempts", 0) > 0:
        h += f'<div style="font-size:11px;font-weight:700;color:#0891b2;margin:4px 0;">🎤 Speaking</div>'
        h += _row("Deneme", str(spk.get("total_attempts", 0)))
        h += _row("Ort. Skor", f'{spk.get("avg_score", 0):.0f}')
        h += _row("Ort. WPM", f'{spk.get("avg_wpm", 0):.0f}')
        if spk.get("last_cefr"):
            h += _row("Son CEFR", spk.get("last_cefr", "-"))
        if spk.get("best_score"):
            h += _row("En İyi", f'{spk.get("best_score", 0):.0f}')
    if not comp and not (spk and spk.get("total_attempts")):
        h += '<div style="color:#64748b;font-size:12px;">English progress kaydı yok</div>'
    _sec("English Progress", "🗣️", "#0891b2", h)


def _render_sec_randevu(d: dict):
    """Veli-öğretmen randevu geçmişi."""
    rdv = d.get("randevular", [])
    h = ""
    if rdv:
        h += _row("Toplam Randevu", str(len(rdv)))
        tamam = sum(1 for r in rdv if r.get("durum") == "Tamamlandi")
        iptal = sum(1 for r in rdv if r.get("durum") in ("Iptal", "Gelmedi"))
        h += _row("Tamamlanan", str(tamam))
        if iptal:
            h += _row("İptal/Gelmedi", str(iptal), "#ef4444")
        for r in sorted(rdv, key=lambda x: x.get("tarih", ""), reverse=True)[:3]:
            h += _row(str(r.get("tarih", ""))[:10],
                       f'{r.get("randevu_turu", "-")} — {r.get("durum", "-")}')
    else:
        h += '<div style="color:#64748b;font-size:12px;">Randevu kaydı yok</div>'
    _sec("Veli Randevuları", "📅", "#7c3aed", h)


# ────────────────────────────────────────────────────────────
# AI 360° MEGA DEĞERLENDİRME
# ────────────────────────────────────────────────────────────

def _build_360_prompt(d: dict) -> str:
    """Tum ogrenci verisini AI promptu olarak formatla.
    Her veri kaynagi acik belirtilir, hicbir alan atlanmaz.
    AI bu veriye dayanarak analiz yapar — uydurma yasak."""
    L = []
    _a = L.append
    stu = d.get("stu", {})
    name = d.get("name", "?")

    _a(f"=== OGRENCI 360 — TAM VERI DOKUMU ===")
    _a(f"Ad Soyad: {name}")
    _a(f"Sinif/Sube/No: {stu.get('sinif','?')}/{stu.get('sube','?')}/{stu.get('numara','-')}")
    _a(f"TC: {stu.get('tc_kimlik', '-')}")
    _a(f"Veli: {stu.get('veli_adi', '-')} {stu.get('veli_soyadi', '')} | Tel: {stu.get('veli_tel', '-')}")
    _a("")

    # ── 1. AKADEMIK NOTLAR (Kaynak: Akademik Takip Modulu) ──
    grades = d.get("grades", [])
    _a(f"[KAYNAK: Akademik Takip > Notlar] ({len(grades)} kayit)")
    if grades:
        ders_map: dict[str, list] = {}
        for g in grades:
            ders = g.get("ders", g.get("subject", "?"))
            try:
                ders_map.setdefault(ders, []).append(float(g.get("puan", 0)))
            except (ValueError, TypeError):
                pass
        for dn, vals in sorted(ders_map.items()):
            avg = sum(vals) / len(vals)
            _a(f"  {dn}: {len(vals)} not, Ort={avg:.1f}, Min={min(vals):.0f}, Max={max(vals):.0f}")
        # Tek tek notlar
        _a(f"  Detay:")
        for g in grades:
            _a(f"    {g.get('ders','?')} | {g.get('not_turu','-')} | Puan: {g.get('puan','-')}")
    else:
        _a("  Veri yok")
    _a("")

    # ── 2. SINAV SONUCLARI (Kaynak: Olcme Degerlendirme) ──
    exams = d.get("exams", [])
    _a(f"[KAYNAK: Olcme Degerlendirme > Sinav Sonuclari] ({len(exams)} kayit)")
    for e in sorted(exams, key=lambda x: x.get("tarih", ""), reverse=True):
        sc = e.get("score", e.get("puan", "-"))
        _a(f"  {e.get('exam_title', e.get('sinav_adi', '?'))} | Puan: {sc} | Tarih: {str(e.get('tarih',''))[:10]}")
    if not exams:
        _a("  Veri yok")
    _a("")

    # ── 3. DEVAMSIZLIK (Kaynak: Akademik Takip > Yoklama) ──
    att = d.get("attendance", [])
    ozursuz = sum(1 for a in att if "ozursuz" in str(a.get("turu", "")).lower())
    ozurlu = len(att) - ozursuz
    _a(f"[KAYNAK: Akademik Takip > Devamsizlik] ({len(att)} gun)")
    _a(f"  Ozurlu: {ozurlu} gun | Ozursuz: {ozursuz} gun | Toplam: {len(att)} gun")
    for a in sorted(att, key=lambda x: x.get("tarih", ""), reverse=True):
        _a(f"  {str(a.get('tarih',''))[:10]} — {a.get('turu', '-')}")
    if not att:
        _a("  Veri yok")
    _a("")

    # ── 4. ODEV & KYT (Kaynak: Akademik Takip) ──
    hw = d.get("hw_subs", [])
    kyt = d.get("kyt", [])
    _a(f"[KAYNAK: Akademik Takip > Odev] ({len(hw)} kayit)")
    if hw:
        teslim = sum(1 for s in hw if s.get("durum") in ("teslim_edildi", "degerlendirildi"))
        _a(f"  Teslim: {teslim}/{len(hw)} (%{teslim/len(hw)*100:.0f})")
    _a(f"[KAYNAK: Olcme Degerlendirme > KYT] ({len(kyt)} cevap)")
    if kyt:
        dogru = sum(1 for k in kyt if k.get("dogru"))
        _a(f"  Dogru: {dogru}/{len(kyt)} (%{dogru/len(kyt)*100:.0f})")
    _a("")

    # ── 5. KAZANIM BORCU & TELAFI (Kaynak: Olcme Degerlendirme) ──
    borc = d.get("borc", [])
    telafi = d.get("telafi", [])
    _a(f"[KAYNAK: Olcme Degerlendirme > Kazanim Borcu] ({len(borc)} kayit)")
    acik = [b for b in borc if b.get("durum") == "borc_var"]
    _a(f"  Acik borc: {len(acik)}, Kapatilan: {len(borc) - len(acik)}")
    for b in acik:
        _a(f"  ACIK: {b.get('ders','')} — {b.get('kazanim_kodu','')}")
    _a(f"[KAYNAK: Olcme Degerlendirme > Telafi Gorevleri] ({len(telafi)} kayit)")
    if telafi:
        comp = sum(1 for t in telafi if t.get("status") == "completed")
        bands: dict[str, int] = {}
        for t in telafi:
            bands[t.get("color_band", "?")] = bands.get(t.get("color_band", "?"), 0) + 1
        _a(f"  Tamamlanan: {comp}/{len(telafi)} | Bantlar: {bands}")
    _a("")

    # ── 6. ERKEN UYARI (Kaynak: Erken Uyari Sistemi) ──
    risk = d.get("latest_risk")
    _a(f"[KAYNAK: Erken Uyari Sistemi > Risk Hesaplama]")
    if risk:
        _a(f"  Risk Skoru: {risk.get('risk_score',0):.0f}/100")
        _a(f"  Risk Seviyesi: {risk.get('risk_level','?')}")
        _a(f"  Hesaplama Tarihi: {risk.get('calculated_at','?')}")
        comps = ["grade_risk", "attendance_risk", "exam_risk", "homework_risk",
                 "outcome_debt_risk", "counseling_risk", "health_risk",
                 "trend_risk", "behavior_risk", "foreign_lang_risk"]
        for ck in comps:
            val = risk.get(ck, 0)
            if val > 0:
                _a(f"  {ck}: {val:.0f}/100")
        fl = risk.get("foreign_lang_performance", {})
        active_flags = {k: v for k, v in fl.items()
                        if v and k not in ("quiz_avg", "quiz_count", "rhb_test_count", "rhb_test_avg",
                                           "placed_cefr", "is_below")}
        if active_flags:
            _a(f"  Risk Flagleri: {active_flags}")
        # Trend
        history = d.get("risk_history", [])
        if len(history) >= 2:
            prev = history[1].get("risk_score", 0)
            cur = history[0].get("risk_score", 0)
            _a(f"  Trend: {prev:.0f} -> {cur:.0f} (degisim: {cur-prev:+.0f})")
    else:
        _a("  Henuz hesaplanmadi")
    _a("")

    # ── 7. YABANCI DIL (Kaynak: Yabanci Dil Modulu) ──
    yd = d.get("yd_results", [])
    cefr = d.get("cefr_placement", [])
    mock = d.get("cefr_mock", [])
    _a(f"[KAYNAK: Yabanci Dil Modulu] (Quiz/Sinav: {len(yd)}, CEFR: {len(cefr)}, Mock: {len(mock)})")
    if cefr:
        last = cefr[-1]
        _a(f"  CEFR Seviye: {last.get('cefr_level', '?')} | Puan: {last.get('total_score', '-')}")
    if yd:
        ydp = [float(r.get("score", r.get("puan", 0))) for r in yd if r.get("score") or r.get("puan")]
        avg = sum(ydp) / len(ydp) if ydp else 0
        _a(f"  Quiz/Sinav Ortalama: {avg:.1f}")
        for r in sorted(yd, key=lambda x: x.get("tarih", x.get("date", "")), reverse=True):
            sc = r.get("score", r.get("puan", 0))
            _a(f"  {r.get('exam_type', r.get('tur','?'))} | Puan: {sc} | {str(r.get('tarih', r.get('date','')))[:10]}")
    if not yd and not cefr:
        _a("  Veri yok")
    _a("")

    # ── 8. REHBERLIK (Kaynak: Rehberlik Modulu) ──
    vakalar = d.get("vakalar", [])
    gorusmeler = d.get("gorusmeler", [])
    _a(f"[KAYNAK: Rehberlik > Vakalar] ({len(vakalar)} kayit)")
    for v in vakalar:
        _a(f"  {v.get('vaka_basligi', v.get('konu','?'))} | Durum: {v.get('durum','?')} | Oncelik: {v.get('oncelik','-')}")
    _a(f"[KAYNAK: Rehberlik > Gorusmeler] ({len(gorusmeler)} kayit)")
    for g in sorted(gorusmeler, key=lambda x: x.get("tarih", ""), reverse=True):
        _a(f"  {g.get('gorusme_konusu', g.get('konu','?'))} | Tarih: {str(g.get('tarih',''))[:10]}")
    # Testler
    oturumlar = d.get("rhb_oturumlar", [])
    cevaplar = d.get("rhb_cevaplar", [])
    tst_map = {t.get("id", ""): t for t in d.get("rhb_testler", [])}
    _a(f"[KAYNAK: Rehberlik > Test & Envanter] ({len(oturumlar)} oturum)")
    for o in oturumlar:
        tst = tst_map.get(o.get("test_id", ""), {})
        oc = [cc for cc in cevaplar if cc.get("oturum_id") == o.get("id")]
        pp = [float(cc.get("puan", 0)) for cc in oc if cc.get("puan")]
        avg = f"{sum(pp)/len(pp):.1f}" if pp else "-"
        _a(f"  {tst.get('test_adi','?')} | Durum: {o.get('durum','?')} | Cevap: {len(oc)} | Ort Puan: {avg}")
    _a("")

    # ── 9. AILE BILGI FORMU (Kaynak: Rehberlik > MEB Formlari) ──
    abf = d.get("aile_bilgi", [])
    _a(f"[KAYNAK: Rehberlik > Aile Bilgi Formu B.K.G.1.c] ({len(abf)} form)")
    if abf:
        a = abf[-1]
        # TUM ALANLAR — hicbir sey atlanmaz
        skip = {"id", "olusturma_zamani", "guncelleme_zamani", "ogrenci_id"}
        for key, val in a.items():
            if key in skip:
                continue
            label = key.replace("_", " ").title()
            display = str(val) if val and str(val).strip() else "Bos/Belirtilmemis"
            _a(f"  {label}: {display}")
    else:
        _a("  Form doldurulmamis")
    _a("")

    # ── 10. MEB DIJITAL FORMLAR (Kaynak: Rehberlik > MEB Formlari) ──
    meb = d.get("meb_forms", {})
    total_meb = sum(len(v) for v in meb.values())
    _a(f"[KAYNAK: Rehberlik > MEB Dijital Formlar] ({total_meb} kayit)")
    if meb:
        try:
            from models.meb_formlar import MEB_FORM_SCHEMAS
        except ImportError:
            MEB_FORM_SCHEMAS = {}
        for sk, forms in meb.items():
            schema = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == sk), None)
            fname = schema["title"] if schema else sk
            _a(f"  --- {fname} ({len(forms)} kayit) ---")
            for fi, f in enumerate(forms[-2:]):  # Son 2 kayit detayli
                _a(f"  [Kayit {fi+1}]")
                skip = {"id", "olusturma_zamani", "guncelleme_zamani", "ogrenci_id", "ogrenci_adi_soyadi"}
                for key, val in f.items():
                    if key in skip:
                        continue
                    if val and str(val).strip() and val not in ("", "Gozlenmedi", 0, "0", False, "False"):
                        _a(f"    {key}: {str(val)[:100]}")
    else:
        _a("  MEB form kaydi yok")
    _a("")

    # ── 11. SAGLIK (Kaynak: Okul Sagligi Modulu) ──
    saglik = d.get("saglik", [])
    _a(f"[KAYNAK: Okul Sagligi > Revir Ziyaretleri] ({len(saglik)} kayit)")
    for s in saglik:
        takip = "TAKIP GEREKLI" if s.get("takip_gerekiyor") else "Takip gerekmiyor"
        _a(f"  {s.get('sikayet_kategorisi','?')} | {str(s.get('basvuru_tarihi',''))[:10]} | {takip}")
    if not saglik:
        _a("  Veri yok")
    _a("")

    # ── 12. EGITIM KOCLUGU (Kaynak: Egitim Koclugu Modulu — TAM VERİ) ──
    kc = d.get("kocluk")
    _a(f"[KAYNAK: Egitim Koclugu]")
    if kc:
        _a(f"  Koc: {kc.get('koc_adi', '-')}")
        _a(f"  Motivasyon: {kc.get('motivasyon_seviyesi', '-')}/5")
        _a(f"  Hedef Sinav: {kc.get('hedef_sinav', '-')} {kc.get('hedef_puan', '')}")
        _a(f"  Guclu Dersler: {kc.get('guclu_dersler', '-')}")
        _a(f"  Zayif Dersler: {kc.get('zayif_dersler', '-')}")
    else:
        _a("  Kocluk kaydi yok")
    ek_grs = d.get("ek_gorusmeler", [])
    if ek_grs:
        _a(f"  Kocluk Gorusmeleri: {len(ek_grs)} kayit")
        for g in ek_grs[-3:]:
            _a(f"    {str(g.get('tarih',''))[:10]} | {g.get('turu','-')} | {g.get('durum','-')} | {str(g.get('notlar',''))[:80]}")
    ek_hdf = d.get("ek_hedefler", [])
    if ek_hdf:
        aktif = [x for x in ek_hdf if x.get("durum") in ("Devam Ediyor", "Beklemede")]
        _a(f"  Hedefler: {len(ek_hdf)} toplam, {len(aktif)} aktif")
        for h in ek_hdf:
            _a(f"    {h.get('hedef_adi', h.get('baslik','-'))} | {h.get('durum','-')} | {h.get('oncelik','-')}")
    ek_mot = d.get("ek_motivasyon", [])
    if ek_mot:
        last_m = sorted(ek_mot, key=lambda x: x.get("tarih", ""), reverse=True)[0]
        _a(f"  Son Motivasyon: {last_m.get('motivasyon','-')}/5 | Stres: {last_m.get('stres','-')} | Odak: {last_m.get('odak','-')}")
    ek_dnm = d.get("ek_deneme", [])
    if ek_dnm:
        _a(f"  Deneme Analizleri: {len(ek_dnm)} sinav")
        for dn in ek_dnm[-3:]:
            _a(f"    {dn.get('sinav_adi','-')} | Puan: {dn.get('puan','-')} | Net: {dn.get('net','-')}")
    _a("")

    # ── 13. TUM TEST SONUCLARI BIRLESIK (Rehberlik + Kayit) ──
    tum_t = d.get("tum_testler", [])
    _a(f"[KAYNAK: TUM TEST SONUCLARI — Rehberlik + Kayit Birlesik] ({len(tum_t)} test)")
    if tum_t:
        # Kaynak bazli ozet
        rhb_cnt = sum(1 for t in tum_t if "Rehberlik" in t.get("kaynak", ""))
        km_cnt = sum(1 for t in tum_t if "Kayit" in t.get("kaynak", ""))
        _a(f"  Rehberlik Testleri: {rhb_cnt} | Kayit Modulu Testleri: {km_cnt}")
        _a(f"  Uygulanan Test Turleri: {', '.join(sorted(set(t.get('test_adi','?') for t in tum_t)))}")
        _a("")
        for t in tum_t:
            _a(f"  === {t.get('test_adi', '?')} ===")
            _a(f"    Kaynak: {t.get('kaynak', '?')}")
            _a(f"    Kategori: {t.get('test_kategorisi', '-')}")
            _a(f"    Tarih: {str(t.get('tarih', ''))[:10]}")
            _a(f"    Durum: {t.get('durum', '-')}")
            if t.get("olcekler"):
                _a(f"    Olcekler: {', '.join(t['olcekler'])}")
            if t.get("genel_ortalama"):
                _a(f"    Genel Ortalama: {t['genel_ortalama']}")
            if t.get("cevap_sayisi"):
                _a(f"    Cevap Sayisi: {t['cevap_sayisi']}")
            skorlar = t.get("skorlar", {})
            if skorlar:
                _a(f"    Skor Detayi:")
                for sk, sv in skorlar.items():
                    _a(f"      {sk}: {sv}")
            olcek_p = t.get("olcek_puanlari", {})
            if olcek_p:
                _a(f"    Olcek Puanlari:")
                for ok, ov in olcek_p.items():
                    _a(f"      {ok}: {ov}")
            top3 = t.get("top3", [])
            if top3:
                _a(f"    En Guclu 3 Alan:")
                for item in top3:
                    _a(f"      {item.get('alan','?')}: {item.get('skor','-')} ({item.get('seviye','')})")
            _a("")
    else:
        _a("  Hicbir test uygulanmamis (Rehberlik veya Kayit)")
    _a("")

    # ── 14. TREND ANALIZI (Yil bazli) ──
    tr = d.get("trend", {})
    yil_bazli = tr.get("yil_bazli", {})
    _a(f"[KAYNAK: TREND ANALIZI — Yil Bazli Karsilastirma] ({len(yil_bazli)} egitim yili)")
    if yil_bazli:
        for ey, data in sorted(yil_bazli.items()):
            _a(f"  {ey}: Not Ort={data['not_ort']:.0f} ({data['not_sayisi']} not) | "
               f"Devamsiz={data['devamsiz_toplam']} gun ({data['devamsiz_ozursuz']} ozursuz) | "
               f"Sinav Ort={data['sinav_ort']:.0f} ({data['sinav_sayisi']} sinav) | "
               f"Gorusme={data['gorusme']} | Vaka={data['vaka']}")
    risk_trend = tr.get("risk_trend", [])
    if risk_trend:
        rt_str = " -> ".join(f'{r.get("skor", 0):.0f}({r.get("seviye", "?")})' for r in risk_trend)
        _a(f"  Risk Trendi: {rt_str}")
    donum = tr.get("donum_noktalari", [])
    if donum:
        _a(f"  DONUM NOKTALARI ({len(donum)}):")
        for dn in donum:
            _a(f"    [{dn['tarih']}] {dn['olay']} — {dn['etki']}")
    mudahale = tr.get("mudahale_etkinlik", [])
    if mudahale:
        _a(f"  MUDAHALE ETKINLIGI ({len(mudahale)}):")
        for m in mudahale:
            _a(f"    {m['mudahale']} | Oncesi: {m['oncesi']} | Sonrasi: {m['sonrasi']} | Etki: {m['etki']}")
    _a("")

    # ── 15. MUDAHALE & DESTEK (Kaynak: Akademik Takip) ──
    mud = d.get("mudahaleler", [])
    dsp = d.get("destek_planlari", [])
    onr = d.get("ogretmen_onerileri", [])
    srt = d.get("sertifikalar", [])
    _a(f"[KAYNAK: Akademik Takip > Mudahale/Destek] (Mudahale: {len(mud)}, Destek: {len(dsp)}, Oneri: {len(onr)}, Sertifika: {len(srt)})")
    for m in mud[-3:]:
        _a(f"  Mudahale: {m.get('mudahale_turu', m.get('type','-'))} | {str(m.get('created_at',''))[:10]} | {m.get('status','-')}")
    for p in dsp[-2:]:
        _a(f"  Destek Plani: {p.get('plan_adi','-')} | {p.get('status','-')}")
    for o in onr[-2:]:
        _a(f"  Ogretmen Onerisi: {o.get('teacher_name','-')} — {str(o.get('oneri', o.get('content','')))[:80]}")
    if srt:
        _a(f"  Sertifikalar: {len(srt)} adet")
    _a("")

    # ── 16. KUTUPHANE (Kaynak: Kutuphane Modulu) ──
    odunc = d.get("kutuphane_odunc", [])
    _a(f"[KAYNAK: Kutuphane > Odunc Islemleri] ({len(odunc)} kayit)")
    if odunc:
        iade_bekleyen = [o for o in odunc if not o.get("iade_tarihi")]
        _a(f"  Toplam: {len(odunc)} | Iade Bekleyen: {len(iade_bekleyen)}")
        for o in odunc[-3:]:
            _a(f"  {o.get('materyal_adi','-')} | Odunc: {str(o.get('odunc_tarihi',''))[:10]} | Iade: {str(o.get('iade_tarihi','Bekliyor'))[:10]}")
    _a("")

    # ── 17. SERVIS (Kaynak: Servis Yonetimi) ──
    s_hat = d.get("servis_hatlar", [])
    s_bin = d.get("servis_binis", [])
    _a(f"[KAYNAK: Servis Yonetimi] (Hat: {len(s_hat)}, Binis: {len(s_bin)})")
    for h in s_hat:
        _a(f"  Guzergah: {h.get('hat_adi', h.get('ad','-'))}")
    _a("")

    # ── 18. SOSYAL ETKINLIK & KULUPLER (Kaynak: Sosyal Etkinlik Modulu) ──
    kul = d.get("kulup_uyelikleri", [])
    etk = d.get("etkinlik_katilim", [])
    _a(f"[KAYNAK: Sosyal Etkinlik] (Kulup: {len(kul)}, Etkinlik: {len(etk)})")
    for k in kul:
        _a(f"  Kulup: {k.get('kulup_adi', k.get('ad','-'))}")
    for e in etk[-3:]:
        _a(f"  Etkinlik: {e.get('baslik', e.get('ad','-'))} | {str(e.get('tarih',''))[:10]}")
    _a("")

    # ── 19. GAMIFICATION (Kaynak: Gamification Modulu) ──
    gam = d.get("gamification", {})
    _a(f"[KAYNAK: Gamification]")
    if gam and gam.get("total_xp", 0) > 0:
        _a(f"  Seviye: {gam.get('level',1)} ({gam.get('level_name','')})")
        _a(f"  XP: {gam.get('total_xp',0)} | Haftalik: {gam.get('weekly_xp',0)}")
        _a(f"  Seri: {gam.get('streak_days',0)} gun | Dogruluk: {gam.get('accuracy',0):.0f}%")
        _a(f"  Rozetler: {len(gam.get('badges_earned',[]))}")
    else:
        _a("  Gamification verisi yok")
    _a("")

    # ── 20. ICERIK MODULLERI (Matematik/Bilisim/Sanat) ──
    mat = d.get("matematik_profil", {})
    bil = d.get("bilisim_profil", {})
    snt_p = d.get("sanat_profil", {})
    _a(f"[KAYNAK: Icerik Modulleri]")
    if mat and (mat.get("toplam_problemler") or mat.get("toplam_cozum")):
        _a(f"  Matematik: Cozulen={mat.get('toplam_problemler', mat.get('toplam_cozum',0))}, Dogru={mat.get('dogru_sayisi',0)}, Seviye={mat.get('seviye','-')}")
    if bil and (bil.get("toplam_proje") or bil.get("basari_skoru")):
        _a(f"  Bilisim: Proje={bil.get('tamamlanan_proje',0)}/{bil.get('toplam_proje',0)}, Skor={bil.get('basari_skoru','-')}")
    if snt_p and snt_p.get("toplam_aktivite"):
        _a(f"  Sanat: Aktivite={snt_p.get('toplam_aktivite',0)}, Sure={snt_p.get('toplam_sure_dk',0)} dk")
    if not mat and not bil and not snt_p:
        _a("  Icerik modulu verisi yok")
    _a("")

    # ── 21. ENGLISH PROGRESS & SPEAKING (Kaynak: English Progress + Speaking) ──
    eng = d.get("eng_completions", [])
    spk = d.get("speaking_stats", {})
    _a(f"[KAYNAK: English Progress] (Alistirma: {len(eng)}, Seri: {d.get('eng_streak',0)} gun)")
    if spk and spk.get("total_attempts", 0) > 0:
        _a(f"  Speaking: {spk.get('total_attempts',0)} deneme, Ort Skor={spk.get('avg_score',0):.0f}, WPM={spk.get('avg_wpm',0):.0f}, CEFR={spk.get('last_cefr','-')}")
    _a("")

    # ── 22. RANDEVULAR (Kaynak: Randevu Ziyaretci) ──
    rdv = d.get("randevular", [])
    _a(f"[KAYNAK: Randevu & Ziyaretci > Veli Randevulari] ({len(rdv)} kayit)")
    for r in rdv[-3:]:
        _a(f"  {str(r.get('tarih',''))[:10]} | {r.get('randevu_turu','-')} | {r.get('durum','-')}")
    _a("")

    _a("=== VERI DOKUMU SONU ===")

    text = "\n".join(L)
    if len(text) > 10000:
        text = text[:10000] + "\n[...veri kisaltildi]"
    return text


def _render_ai_360(d: dict):
    """AI 360° Mega Değerlendirme."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff;'
        'padding:16px 20px;border-radius:12px;margin:12px 0;">'
        '<h3 style="margin:0;font-size:18px;">🤖 AI 360° Mega Değerlendirme</h3>'
        '<p style="margin:3px 0 0;font-size:12px;opacity:.85;">'
        'Tüm modüllerden toplanan veriyi GPT-4o-mini ile analiz eder — '
        'kapsamlı öğrenci raporu üretir</p></div>',
        unsafe_allow_html=True,
    )

    cache_key = f"ai360_{d['sid']}"
    if cache_key in st.session_state:
        st.markdown(st.session_state[cache_key])
        if st.button("🔄 Yeniden Analiz Et", key=f"ai360_refresh_{d['sid']}"):
            del st.session_state[cache_key]
            st.rerun()
        return

    if st.button("🤖 AI 360° Analiz Başlat", key=f"ai360_btn_{d['sid']}",
                  type="primary", use_container_width=True):
        prompt_text = _build_360_prompt(d)
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error("OPENAI_API_KEY bulunamadı.")
            return

        system = """Sen Turkiye'nin en deneyimli egitim uzmani, okul muduru ve rehber ogretmenisin.
Sana bir ogrencinin TUM veri dokumu verilecek. Bu veriler gercek sistem kayitlarindan cekilmistir.
Her veri kaynagi [KAYNAK: ...] etiketi ile belirtilmistir.

KRITIK KURALLAR:
1. SADECE verilen verilere dayanarak analiz yap. Veride olmayan bir sey hakkinda yorum YAPMA.
2. Her tespitinin kaynagini belirt: "(Kaynak: Akademik Takip > Notlar)" gibi.
3. Veri yoksa "Bu alanda veri bulunmamaktadir" yaz, tahmin yurutme.
4. Sayisal verileri aynen kullan — yuvarlama veya tahmin yapma.
5. Gercek notlari, gercek sinav puanlarini, gercek risk skorlarini referans goster.
6. Her formdaki her detayi degerlendir — ozellikle Aile Bilgi Formundaki tum alanlar.
7. MEB formlarindaki uzman degerlendirmelerini (rehber_degerlendirme, genel_degerlendirme, yonlendirme_onerisi) aynen al.
8. Bu resmi bir okul raporu — profesyonel, somut, olculebilir ifadeler kullan.

YANITINI su formatta ver (Turkce, detayli, EN AZ 2000 kelime):

## OGRENCI 360 PROFILI
(Butunsel ozet — akademik, sosyal, ailevi, psikolojik boyutlar. Verideki gercek rakamlara dayan.)

## AKADEMIK ANALIZ
- Ders bazli not ortalamalari (gercek rakamlarla, kaynak belirterek)
- Guclu ve zayif dersler (somut not ortalamalariyla kanitla)
- Sinav performansi trendi (tarih sirali, puan degisimi)
- Odev teslim orani ve KYT basari orani
- Kazanim borclari (hangi ders, hangi kazanim)
- Devamsizlik etkisi analizi

## YABANCI DIL GELISIM RAPORU
- CEFR seviyesi degerlendirmesi
- Quiz/sinav puanlari ve trend
- Sinif seviyesine uygunluk

## REHBERLIK DEGERLENDIRMESI
- Acik vakalar ve durumlari (tek tek)
- Gorusme gecmisi ve konulari
- Test sonuclari ve yorumlari (test adi, puan)
- MEB formlari analizi (her formun icerigi detayli — gozlem, gorusme, yonlendirme vb.)

## AILE & SOSYO-EKONOMIK DEGERLENDIRME
- Aile yapisi (anne-baba durumu, medeni hal, yasam kosullari — form verisine dayali)
- Sosyo-ekonomik durum (gelir, ev, yardim — gercek verilerle)
- Risk faktorleri (bosanma, travma, bagimlilik — formda ne yaziyorsa)
- Egitim ortami (calisma alani, ders destegi)

## RISK DEGERLENDIRMESI
- Erken uyari risk skoru ve bilesenleri (gercek puanlarla)
- Risk trendi (onceki skor vs mevcut)
- Tespit edilen risk flagleri (tek tek)
- Ciddiyet siralama: KRITIK / YUKSEK / ORTA / DUSUK
- Koruyucu faktorler

## BIREYSEL MUDAHALE PLANI
- Her risk/sorun icin somut aksiyon (kim, ne, ne zaman)
- Oncelik sirasi
- Mevcut mudahalelerin degerlendirilmesi (yapilan gorusmeler, yonlendirmeler)

## YONLENDIRME KARARLARI
- RAM, saglik, psikolog, sosyal hizmet gerekliligi (formlardaki mevcut yonlendirmelere dayanarak)
- BEP gereksinimi
- Mevcut yonlendirmelerin takip durumu

## KOCLUK & MOTIVASYON STRATEJISI
- Ogretmenlere somut oneriler
- Veliye somut oneriler
- Ogrenciye yonelik stratejiler
- Kisa/orta/uzun vadeli hedefler (gercek puanlara dayali)

## TAKIP TAKVIMI
- Haftalik/aylik/donemlik plan
- Hangi formlar ne siklikla doldurulmali
- Sonraki degerlendirme tarihi

## TEST & ENVANTER DEGERLENDIRMESI (TUM TESTLER)
Bu bolumde 2 ayri kaynaktan gelen TUM testleri degerlendir:
A) REHBERLIK TESTLERI (Kaynak: Rehberlik > Test & Envanter): Beck, Ogrenme Stilleri vb.
B) KAYIT MODULU TESTLERI (Kaynak: Kayit Modulu > Testler): 9 tur:
   - Coklu Zeka Testi: 9 zeka alani, guclu/zayif alanlar, ogrenme stratejisi
   - VARK Ogrenme Stili: Gorsel/Isitsel/Okuma-Yazma/Kinestetik — ders calisma onerileri
   - Seviye Tespit Sinavi: Ortaokul/Lise, ders bazli seviye
   - CEFR Yabanci Dil Yerlestirme: Seviye, hedef, yol haritasi
   - HHT-1 Okula Hazirbulunusluk: Ogrenci + veli boyutu
   - Ortaokul Checkup: Turkce/Matematik/Fen skor analizi

Her test icin:
- Sonucu yorumla (gercek skorlara dayanarak)
- Guclu alanlari belirt
- Gelisim gereken alanlari belirt
- Test sonucuna ozel yol haritasi cikar
- Testler arasi korelasyon analizi yap (ornek: coklu zeka + VARK + notlar uyumu)
Test uygulanmamissa "Henuz uygulanmamistir, onerilir" yaz.

## YABANCI DIL YOL HARITASI
(CEFR seviyesi degerlendirmesi, sinif seviyesine uygunluk,
quiz/sinav trendi, hedef CEFR seviyesi icin yol haritasi,
haftalik/aylik calisma plani, kullanilacak kaynaklar.)

## DERS BAZLI YOL HARITASI
(Her ders icin: mevcut ortalama + hedef not + nasil ulasacak.
Ozellikle dusuk notlu dersler icin haftalik plan.
Guclu dersler icin ileri seviye onerileri.)

## DEVAMSIZLIK MUDAHALE PLANI
(Ozursuz gun sayisi, trendi, nedenleri tahmini,
aile ile iletisim plani, okul ici onlemler.)

## YILLAR ARASI TREND ANALIZI
(Verideki yil bazli karsilastirma tablosunu kullanarak:
- Her egitim yili icin: not ort, devamsizlik, sinav, gorusme sayisi karsilastirmasi
- Yillar arasi degisim yorumu — iyiye mi gidiyor kötüye mi?
- Hangi yil ne oldu — donum noktalarini kronolojik anlat)

## DONUM NOKTALARI VE NEDENSELLIK
(Verideki donum noktalari listesini kullanarak:
- Her donum noktasini analiz et
- Neden-sonuc iliskisi kur: "X oldu → Y degisti"
- Ornek: "2024-2025'te bosanma → devamsizlik %300 artti, notlar 15 puan dustu")

## MUDAHALE ETKINLIGI ANALIZI
(Verideki mudahale etkinligi verilerini kullanarak:
- Yapilan her mudahalenin oncesi-sonrasi karsilastirmasi
- Etkili mi etkisiz mi? Neden?
- Oneri: Hangi mudahale devam etmeli, hangisi degismeli?)

## GENEL SONUC
- En kritik 5 tespit (veriye dayali, kaynak belirterek)
- 3 yillik genel gidis yonu (iyiye mi kotuye mi)
- Basari potansiyeli degerlendirmesi
- Oncelikli 3 aksiyon (hemen yapilmasi gereken)
- KVKK uyarisi"""

        with st.spinner("AI 360° analiz yapılıyor... (tüm modüller)"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt_text},
                    ],
                    temperature=0.7,
                    max_tokens=4000,
                )
                result = resp.choices[0].message.content
                st.session_state[cache_key] = result
                st.markdown(result)
            except Exception as e:
                st.error(f"AI analiz hatası: {e}")


# ────────────────────────────────────────────────────────────
# AI TOPLAM GELİŞİM RAPORU (Geçmişten Günümüze)
# ────────────────────────────────────────────────────────────

def _render_ai_toplam_gelisim(d: dict):
    """AI Toplam Gelişim Raporu — tüm yılların birleşik analizi."""
    tr = d.get("trend", {})
    yil_bazli = tr.get("yil_bazli", {})
    if len(yil_bazli) < 2:
        return  # Tek yıl varsa toplam gelişim gösterme

    st.markdown(
        '<div style="background:linear-gradient(135deg,#C8952E,#a07824);color:#fff;'
        'padding:16px 20px;border-radius:12px;margin:12px 0;">'
        '<h3 style="margin:0;font-size:18px;">📜 AI Toplam Gelişim Raporu</h3>'
        '<p style="margin:3px 0 0;font-size:12px;opacity:.85;">'
        'Geçmişten günümüze TÜM yılların birleşik analizi — '
        'ilerleme, gerileme, dönüm noktaları, müdahale etkinliği</p></div>',
        unsafe_allow_html=True,
    )

    cache_key = f"ai_toplam_{d['sid']}"
    if cache_key in st.session_state:
        st.markdown(st.session_state[cache_key])
        if st.button("🔄 Yeniden Analiz Et", key=f"ai_toplam_refresh_{d['sid']}"):
            del st.session_state[cache_key]
            st.rerun()
        return

    if st.button("📜 Toplam Gelişim Analizi Başlat", key=f"ai_toplam_btn_{d['sid']}",
                  type="primary", use_container_width=True):
        prompt_text = _build_360_prompt(d)
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error("OPENAI_API_KEY bulunamadı.")
            return

        system = """Sen Turkiye'nin en deneyimli egitim uzmani ve ogrenci gelisim analistisin.
Sana bir ogrencinin YILLAR BAZLI TUM VERILERI verilecek. Bu veriler gercek sistem kayitlarindan cekilmistir.

GOREV: Bu ogrencinin okula ilk kaydoldugundan BUGUNE KADAR tum gelisim surecini analiz et.
Bu MEVCUT YIL degerlendirmesi DEGILDIR — bu TOPLAM GECMIS degerlendirmesidir.

KRITIK KURALLAR:
1. SADECE verilen verilere dayan. Uydurma YASAK.
2. Her tespitte kaynagini ve yilini belirt.
3. Yillar arasi karsilastirma ZORUNLU — her kriter icin gecmis vs bugun.

YANITINI su formatta ver (Turkce, EN AZ 2500 kelime):

## OGRENCI GELISIM OZETI (Ilk Gunden Bugune)
(Kac yildir bu okulda? Genel gidis yonu nedir? 5-6 cumle butunsel kronolojik ozet.)

## AKADEMIK GELISIM KRONOLOJISI
- Her egitim yili icin not ortalamasi, sinav ortalamasi (gercek rakamlar)
- Ders bazli gelisim/gerileme (hangi derslerde yukseldi, hangilerinde dustu)
- Yillar arasi degisim yuzdeleri
- Akademik kirilma noktalari ve nedenleri
- Genel yonu: ILERLEME mi GERILEME mi DALGALI mi?

## DEVAMSIZLIK GELISIM KRONOLOJISI
- Her yil: toplam gun, ozursuz gun, trend
- Devamsizlik artis/azalis nedenleri (diger verilerle korelasyon)
- Hangi donemlerde yogunlasti (ay bazli varsa)
- Genel yonu ve alarma duzeyi

## SOSYAL-DUYGUSAL GELISIM KRONOLOJISI
- Rehberlik gorusmeleri kronolojisi (ilk gorusmeden bugune)
- Vakalar: ne zaman acildi, neden, sonuclandi mi?
- Test sonuclari zaman icinde nasil degisti (kaygi, benlik saygisi vb.)
- MEB formlari ne gosteriyor (gorusme, gozlem, yonlendirme)
- Aile yapisi degisiklikleri ve etkileri

## TEST SONUCLARI GELISIM ANALIZI
- Tum testlerin kronolojik degerlendirmesi
- Testler arasi korelasyonlar (coklu zeka + notlar + ogrenme stili)
- Zaman icinde degisim var mi (ayni test tekrar yapildiysa)
- Test sonuclarina gore ogrenme stratejisi ne olmali

## RISK GELISIM KRONOLOJISI
- Risk skorunun yillar icindeki degisimi (gercek rakamlarla)
- Her artis/azalis icin neden analizi
- Hangi risk bilesenleri artti, hangileri azaldi
- Mevcut risk seviyesinin gecmise gore yorumu

## DONUM NOKTALARI ANALIZI
- Ogrencinin hayatinda/egitiminde yasanan kritik olaylar kronolojik sirala
- Her olayin oncesi-sonrasi etkisi (somut verilerle)
- Neden-sonuc zincirleri: "A oldu → B degisti → C etkilendi"

## MUDAHALE ETKINLIGI RAPORU
- Yapilan TUM mudahalelerin listesi (kocluk, gorusme, yonlendirme, test, form)
- Her mudahalenin oncesi-sonrasi karsilastirmasi
- Hangileri etkili oldu? Hangileri etkisiz kaldi? Neden?
- Yapilmasi gerekip YAPILMAYAN mudahaleler

## YABANCI DIL GELISIM KRONOLOJISI
- CEFR seviyesi degisimi (varsa)
- Quiz/sinav puanlari zaman icinde
- Sinif seviyesine uygunluk — iyiye mi gidiyor kotuye mi?

## KOCLUK & DESTEK DEGERLENDIRMESI
- Koc ne zaman atandi? Etkisi ne oldu?
- Telafi gorevleri ne durumda? Kazanim borclari kapandi mi?
- Destek programlari (etut, ek ders) etkili mi?

## GELECEK PROJEKSIYON
- Mevcut trendler devam ederse 1 yil sonra ne olur?
- En iyi senaryo (tum mudahaleler etkili olursa)
- En kotu senaryo (mudahale yapilmazsa)
- Gercekci senaryo

## TOPLAM DEGERLENDIRME & KARAR
- Ogrenci genel olarak ILERLIYOR mu GERILIYOR mu YERINDE mi?
- Her kriter icin tek satirlik durum:
  Akademik: ↑ ILERLEME / ↓ GERILEME / → DURAGAN
  Devamsizlik: ↑ / ↓ / →
  Sosyal-Duygusal: ↑ / ↓ / →
  Risk: ↑ / ↓ / →
  Yabanci Dil: ↑ / ↓ / →
  Motivasyon: ↑ / ↓ / →
- En acil 3 aksiyon (HEMEN yapilmasi gereken)
- Orta vadeli 3 hedef (3 ay)
- Uzun vadeli 3 hedef (1 yil)
- KVKK uyarisi

ONEMLI: Bu rapor okul yonetimine sunulacak resmi bir belgedir. Somut, veriye dayali, profesyonel yaz."""

        with st.spinner("AI Toplam Gelişim Raporu oluşturuluyor... (tüm yıllar analiz ediliyor)"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt_text},
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                )
                result = resp.choices[0].message.content
                st.session_state[cache_key] = result
                st.markdown(result)
            except Exception as e:
                st.error(f"AI analiz hatası: {e}")


# ────────────────────────────────────────────────────────────
# ANA RENDER FONKSİYONU
# ────────────────────────────────────────────────────────────

def render_ogrenci_360():
    """Öğrenci 360° Profil Ekranı — Ana entry point."""
    _inject_360_css()

    # Smarti AI welcome
    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("ogrenci_360")
    except Exception:
        pass

    st.markdown(
        '<div style="background:linear-gradient(135deg,#4f46e5,#6366f1);color:#fff;'
        'padding:20px 24px;border-radius:14px;margin-bottom:16px;">'
        '<h2 style="margin:0;font-size:24px;font-weight:800;">📊 Öğrenci 360° Profil</h2>'
        '<p style="margin:4px 0 0;font-size:13px;opacity:.85;">'
        'Bir öğrencinin A\'dan Z\'ye tüm verilerini tek ekranda görün — '
        'akademik, rehberlik, risk, yabancı dil, MEB formlar, AI analiz</p></div>',
        unsafe_allow_html=True,
    )

    # Öğrenci seçimi
    try:
        from utils.shared_data import get_student_display_options
        students = get_student_display_options(include_empty=False)
    except Exception:
        students = {}

    if not students:
        st.warning("Öğrenci verisi bulunamadı. Akademik Takip > Sınıf Listesi'nden öğrenci ekleyin.")
        return

    sel = st.selectbox("👤 Öğrenci Seçin:", [""] + list(students.keys()), key="s360_stu_sel")

    # Split view secenegi
    try:
        from utils.ui_common import split_view_header
        if st.checkbox("🔀 İki öğrenciyi karşılaştır", key="s360_split_mode"):
            sel2 = st.selectbox("👤 İkinci Öğrenci:", [""] + list(students.keys()), key="s360_stu_sel2")
            if sel and sel2 and sel != sel2:
                split_view_header(
                    sel.split(" - ")[0] if " - " in sel else sel,
                    sel2.split(" - ")[0] if " - " in sel2 else sel2,
                )
    except Exception:
        pass

    if not sel:
        st.info("Yukarıdan bir öğrenci seçin.")
        return

    stu_data = students.get(sel, {})
    sid = stu_data.get("id", "")
    if not sid:
        st.error("Öğrenci ID bulunamadı.")
        return

    # Veri toplama
    with st.spinner("Tüm modüllerden veri toplanıyor..."):
        d = _collect_student_data(sid, stu_data)

    # ── Render ──
    _render_hero(d)

    try:
        from utils.ui_common import qr_ogrenci_link
        with st.expander("📱 QR Kod — Öğrenci Profil Bağlantısı", expanded=False):
            qr_ogrenci_link(sid, d.get("name", ""))
            st.caption("Bu QR kodu tarayarak öğrenci profiline hızlı erişim sağlayabilirsiniz.")
    except Exception:
        pass

    _render_stat_row(d)

    st.markdown("---")

    # 2 sütunlu layout
    col1, col2 = st.columns(2)
    with col1:
        _render_sec_akademik(d)
        _render_sec_devamsizlik(d)
        _render_sec_yabanci_dil(d)
        _render_sec_eng_speaking(d)
        _render_sec_odev_kyt(d)
        _render_sec_kocluk(d)
        _render_sec_saglik(d)
        _render_sec_kutuphane(d)
        _render_sec_servis(d)
        _render_sec_gamification(d)
    with col2:
        _render_sec_erken_uyari(d)
        _render_sec_mudahale_destek(d)
        _render_sec_rehberlik(d)
        _render_sec_kayit_testler(d)
        _render_sec_icerik_modulleri(d)
        _render_sec_aile_bilgi(d)
        _render_sec_meb_formlar(d)
        _render_sec_telafi(d)
        _render_sec_sosyal(d)
        _render_sec_randevu(d)

    # ── TREND ANALİZİ SEKSİYONU ──
    st.markdown("---")
    _render_sec_trend(d)

    # Zaman cizelgesi
    try:
        from utils.ui_common import ogrenci_zaman_cizelgesi
        timeline_olaylar = []
        kayit_tarihi = stu_data.get("kayit_tarihi", "")
        if kayit_tarihi:
            timeline_olaylar.append({"tarih": kayit_tarihi, "baslik": "Okula Kayit", "detay": f"{stu_data.get('sinif','')}-{stu_data.get('sube','')}", "ikon": "📝", "renk": "#6366F1"})
        for g in d.get("grades", [])[:3]:
            timeline_olaylar.append({"tarih": g.get("tarih", ""), "baslik": f"{g.get('ders','')} Notu", "detay": f"Puan: {g.get('puan','')}", "ikon": "📊", "renk": "#10B981"})
        for v in d.get("vakalar", [])[:2]:
            timeline_olaylar.append({"tarih": v.get("tarih", ""), "baslik": "Rehberlik", "detay": v.get("konu", v.get("vaka_basligi","")), "ikon": "🧠", "renk": "#7C3AED"})
        if timeline_olaylar:
            ogrenci_zaman_cizelgesi(timeline_olaylar)
    except Exception:
        pass


def _render_sec_trend(d: dict):
    """Yıl bazlı trend analizi — karşılaştırma + grafikler + dönüm noktaları."""
    tr = d.get("trend", {})
    yil_bazli = tr.get("yil_bazli", {})

    if not yil_bazli or len(yil_bazli) < 1:
        return

    st.markdown(
        '<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;'
        'padding:16px 20px;border-radius:12px;margin:8px 0;">'
        '<h3 style="margin:0;font-size:18px;">📈 Yıl Bazlı Trend Analizi</h3>'
        '<p style="margin:3px 0 0;font-size:12px;opacity:.85;">'
        'Eğitim yılları arası karşılaştırma — akademik, devamsızlık, sınav, rehberlik</p></div>',
        unsafe_allow_html=True,
    )

    # ── 1. Yıl Karşılaştırma Tablosu ──
    yillar = sorted(yil_bazli.keys())
    if len(yillar) >= 2:
        st.markdown("#### Yıl Bazlı Karşılaştırma")
        cols = st.columns(len(yillar))
        for i, ey in enumerate(yillar):
            data = yil_bazli[ey]
            with cols[i]:
                st.markdown(f"**{ey}**")
                # Not trend rengi
                nc = "#22c55e" if data["not_ort"] >= 70 else "#f59e0b" if data["not_ort"] >= 50 else "#ef4444"
                st.markdown(f'<div style="background:{nc}15;border-left:3px solid {nc};padding:6px 10px;border-radius:0 6px 6px 0;margin:3px 0;">'
                            f'<b style="color:{nc};">Not Ort: {data["not_ort"]:.0f}</b> ({data["not_sayisi"]} not)</div>',
                            unsafe_allow_html=True)
                dc = "#ef4444" if data["devamsiz_ozursuz"] > 10 else "#f59e0b" if data["devamsiz_ozursuz"] > 5 else "#22c55e"
                st.markdown(f'<div style="background:{dc}15;border-left:3px solid {dc};padding:6px 10px;border-radius:0 6px 6px 0;margin:3px 0;">'
                            f'<b style="color:{dc};">Devamsız: {data["devamsiz_toplam"]}</b> ({data["devamsiz_ozursuz"]} özürsüz)</div>',
                            unsafe_allow_html=True)
                if data["sinav_sayisi"] > 0:
                    st.markdown(f"Sınav Ort: **{data['sinav_ort']:.0f}** ({data['sinav_sayisi']})")
                st.markdown(f"Görüşme: **{data['gorusme']}** | Vaka: **{data['vaka']}**")

    # ── 2. Trend Grafikleri (Plotly) ──
    if len(yillar) >= 2:
        st.markdown("#### Trend Grafikleri")
        col1, col2 = st.columns(2)

        with col1:
            # Not ortalaması trend
            not_vals = [yil_bazli[ey]["not_ort"] for ey in yillar]
            fig_not = go.Figure()
            fig_not.add_trace(go.Scatter(x=yillar, y=not_vals, mode='lines+markers+text',
                                          text=[f"{v:.0f}" for v in not_vals], textposition="top center",
                                          line=dict(color='#6366f1', width=3),
                                          marker=dict(size=10, color='#6366f1')))
            fig_not.update_layout(title="Not Ortalaması Trendi", height=280,
                                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(color='#cbd5e1'), yaxis=dict(range=[0, 100]),
                                   margin=dict(l=30, r=10, t=40, b=30))
            st.plotly_chart(fig_not, use_container_width=True, key=f"trend_not_{d['sid']}")

        with col2:
            # Devamsızlık trend
            dev_vals = [yil_bazli[ey]["devamsiz_ozursuz"] for ey in yillar]
            fig_dev = go.Figure()
            fig_dev.add_trace(go.Bar(x=yillar, y=dev_vals, text=[str(v) for v in dev_vals],
                                      textposition='outside',
                                      marker_color=['#22c55e' if v <= 5 else '#f59e0b' if v <= 10 else '#ef4444' for v in dev_vals]))
            fig_dev.update_layout(title="Özürsüz Devamsızlık Trendi", height=280,
                                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(color='#cbd5e1'),
                                   margin=dict(l=30, r=10, t=40, b=30))
            st.plotly_chart(fig_dev, use_container_width=True, key=f"trend_dev_{d['sid']}")

        # Risk trend
        risk_trend = tr.get("risk_trend", [])
        if len(risk_trend) >= 2:
            col3, col4 = st.columns(2)
            with col3:
                r_dates = [r["tarih"] for r in risk_trend]
                r_vals = [r["skor"] for r in risk_trend]
                r_colors = ['#22c55e' if v < 30 else '#f59e0b' if v < 60 else '#f97316' if v < 75 else '#ef4444' for v in r_vals]
                fig_risk = go.Figure()
                fig_risk.add_trace(go.Scatter(x=r_dates, y=r_vals, mode='lines+markers+text',
                                               text=[f"{v:.0f}" for v in r_vals], textposition="top center",
                                               line=dict(color='#ef4444', width=3),
                                               marker=dict(size=10, color=r_colors)))
                fig_risk.update_layout(title="Risk Skoru Trendi", height=280,
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        font=dict(color='#cbd5e1'), yaxis=dict(range=[0, 100]),
                                        margin=dict(l=30, r=10, t=40, b=30))
                st.plotly_chart(fig_risk, use_container_width=True, key=f"trend_risk_{d['sid']}")

            with col4:
                # Sınav ortalaması trend
                sinav_vals = [yil_bazli[ey]["sinav_ort"] for ey in yillar if yil_bazli[ey]["sinav_ort"] > 0]
                sinav_yillar = [ey for ey in yillar if yil_bazli[ey]["sinav_ort"] > 0]
                if sinav_vals:
                    fig_sinav = go.Figure()
                    fig_sinav.add_trace(go.Scatter(x=sinav_yillar, y=sinav_vals, mode='lines+markers+text',
                                                     text=[f"{v:.0f}" for v in sinav_vals], textposition="top center",
                                                     line=dict(color='#8b5cf6', width=3),
                                                     marker=dict(size=10, color='#8b5cf6')))
                    fig_sinav.update_layout(title="Sınav Ortalaması Trendi", height=280,
                                             plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                             font=dict(color='#cbd5e1'), yaxis=dict(range=[0, 100]),
                                             margin=dict(l=30, r=10, t=40, b=30))
                    st.plotly_chart(fig_sinav, use_container_width=True, key=f"trend_sinav_{d['sid']}")

    # Ay bazlı not grafiği
    ay_not = tr.get("ay_bazli_not", {})
    if len(ay_not) >= 3:
        st.markdown("#### Aylık Not Ortalaması")
        aylar = sorted(ay_not.keys())
        vals = [ay_not[a] for a in aylar]
        fig_ay = go.Figure()
        fig_ay.add_trace(go.Scatter(x=aylar, y=vals, mode='lines+markers', fill='tozeroy',
                                     line=dict(color='#6366f1', width=2),
                                     fillcolor='rgba(99,102,241,0.1)'))
        fig_ay.update_layout(height=250, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='#cbd5e1'), margin=dict(l=30, r=10, t=10, b=30))
        st.plotly_chart(fig_ay, use_container_width=True, key=f"trend_ay_{d['sid']}")

    # ── 3. Dönüm Noktaları ──
    donum = tr.get("donum_noktalari", [])
    if donum:
        st.markdown("#### ⚡ Dönüm Noktaları")
        for dn in donum:
            tur_clr = {"akademik_dusus": "#ef4444", "devamsizlik_artis": "#f59e0b", "rehberlik_vaka": "#8b5cf6"}.get(dn.get("tur"), "#64748b")
            st.markdown(f'<div style="background:{tur_clr}10;border-left:3px solid {tur_clr};'
                        f'padding:8px 12px;border-radius:0 8px 8px 0;margin:4px 0;">'
                        f'<b style="color:{tur_clr};">[{dn["tarih"]}] {dn["olay"]}</b>'
                        f'<div style="color:#94a3b8;font-size:12px;">{dn["etki"]}</div></div>',
                        unsafe_allow_html=True)

    # ── 4. Müdahale Etkinliği ──
    mudahale = tr.get("mudahale_etkinlik", [])
    if mudahale:
        st.markdown("#### 🔍 Müdahale Etkinliği Analizi")
        for m in mudahale:
            etki_clr = "#22c55e" if m["etki"] == "olumlu" else "#ef4444" if m["etki"] == "olumsuz" else "#f59e0b"
            etki_txt = {"olumlu": "OLUMLU ETKİ ↑", "olumsuz": "OLUMSUZ / ETKİSİZ ↓", "notr": "NÖTR →"}.get(m["etki"], m["etki"])
            st.markdown(f'<div style="background:#1e293b;border-left:3px solid {etki_clr};'
                        f'padding:8px 12px;border-radius:0 8px 8px 0;margin:4px 0;">'
                        f'<b>{m["mudahale"]}</b>'
                        f'<div style="font-size:12px;color:#94a3b8;">Öncesi: {m["oncesi"]} → Sonrası: {m["sonrasi"]}</div>'
                        f'<div style="color:{etki_clr};font-weight:700;font-size:13px;">{etki_txt}</div></div>',
                        unsafe_allow_html=True)

    # ── ZİRVE: Benchmark + Yolculuk + Müdahale Önerici ──
    st.markdown("---")
    try:
        from views._o360_zirve import render_benchmark, render_gelisim_yolculugu, render_mudahale_onerici
        render_benchmark(d, students)
        st.markdown("---")
        render_gelisim_yolculugu(d)
        st.markdown("---")
        render_mudahale_onerici(d)
    except Exception:
        pass

    # ── MEGA: Portfolyo + Buddy + Tahmin ──
    st.markdown("---")
    try:
        from views._o360_mega import render_portfolyo, render_buddy_sistemi, render_gelecek_tahmini
        render_portfolyo(d)
        st.markdown("---")
        render_buddy_sistemi(d, students)
        st.markdown("---")
        render_gelecek_tahmini(d)
    except Exception:
        pass

    # ── AI Mevcut Yıl Değerlendirmesi ──
    st.markdown("---")
    _render_ai_360(d)

    # ── AI Toplam Gelişim Raporu (Geçmişten Günümüze) ──
    st.markdown("---")
    _render_ai_toplam_gelisim(d)

    # ── PDF Rapor İndirme ──
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#C8952E,#a07824);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin:8px 0;">'
        '<b>📥 Ultra Premium PDF Rapor</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Baskıya hazır, grafikli, kategorili tam öğrenci raporu — kapak + 5 sayfa + AI değerlendirme + imza alanı</p></div>',
        unsafe_allow_html=True,
    )
    ai_cache = st.session_state.get(f"ai360_{d['sid']}", "")
    ai_toplam_cache = st.session_state.get(f"ai_toplam_{d['sid']}", "")
    # İki AI metnini birleştir
    combined_ai = ""
    if ai_cache:
        combined_ai += "=== MEVCUT YIL DEGERLENDIRMESI ===\n\n" + ai_cache + "\n\n"
    if ai_toplam_cache:
        combined_ai += "=== TOPLAM GELISIM RAPORU (GECMISTEN GUNUMUZE) ===\n\n" + ai_toplam_cache
    if not combined_ai:
        combined_ai = ai_cache  # fallback

    if st.button("📥 PDF Rapor Oluştur & İndir", key=f"s360_pdf_{d['sid']}",
                  type="primary", use_container_width=True):
        with st.spinner("Ultra Premium PDF oluşturuluyor..."):
            try:
                from views.ogrenci_360_pdf import generate_ogrenci_360_pdf
                pdf_bytes = generate_ogrenci_360_pdf(d, ai_text=combined_ai)
                safe_name = d["name"].replace(" ", "_")
                st.download_button(
                    label="📥 PDF İndir",
                    data=pdf_bytes,
                    file_name=f"Ogrenci_360_{safe_name}_{date.today().isoformat()}.pdf",
                    mime="application/pdf",
                    key=f"s360_dl_{d['sid']}",
                )
                st.success("PDF hazır — yukarıdaki butona tıklayarak indirin.")
            except Exception as e:
                st.error(f"PDF oluşturma hatası: {e}")
