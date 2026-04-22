"""
AI Destek Modulu — SmartCampus Merkez Beyni
=============================================
Yonetici: 18 modulden veri toplayan dashboard + AI analiz + yol haritasi
Diger roller: Sesli/yazili chatbot asistani (Smarti)
"""
from __future__ import annotations

import hashlib
import io
import os
import time
from typing import Any

import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utils.ui_common import (
    inject_common_css, inject_pro_css,
    styled_header, styled_section, styled_stat_row, styled_info_banner,
)
import plotly.graph_objects as go
from utils.ai_rules import inject_rules as _ai_inject_rules
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG

# Maskot avatar yolu
_MASCOT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "assets", "mascot.png")


# ===================== INJECT CSS =====================

def _inject_css():
    st.markdown("""<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #111827 0%, #1A2035 50%, #111827 100%);
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #94A3B8;
    }
    </style>""", unsafe_allow_html=True)


# ===================== ENV YUKLE =====================

def _ensure_env():
    """Ensure .env is loaded for OPENAI_API_KEY."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")


# ===================== OPENAI CLIENT =====================

def _get_client():
    """OpenAI client olustur."""
    _ensure_env()
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


# ===================== VERİ BAĞLAMI =====================

def _build_data_context(auth_user: dict) -> str:
    """Kullanıcı rolüne göre sistemden veri çekip bağlam metni oluştur."""
    from models.akademik_takip import AkademikDataStore
    from models.olcme_degerlendirme import DataStore as OlcmeDataStore

    ak = AkademikDataStore()
    od = OlcmeDataStore()
    role = auth_user.get("role", "")
    username = auth_user.get("username", "")
    name = auth_user.get("name", "")
    lines: list[str] = []

    try:
        if role == "Veli":
            lines.append("=== VELİ VERİ PANELİ ===")
            # Velinin çocuğunu bul
            all_students = ak.get_students()
            children = [s for s in all_students
                        if s.veli_adi and name.lower() in s.veli_adi.lower()]
            if not children:
                # Username'den eşleştirmeyi dene
                children = [s for s in all_students
                            if s.veli_telefon and username in str(s.veli_telefon)]
            if not children:
                lines.append("Kayıtlı öğrenci bulunamadı.")
                return "\n".join(lines)

            for child in children:
                lines.append(f"\nÖğrenci: {child.tam_ad} | Sınıf: {child.sinif}/{child.sube} | No: {child.numara}")

                # Notlar
                grades = ak.get_grades(student_id=child.id)
                if grades:
                    lines.append("\n--- NOTLAR ---")
                    ders_notlar: dict[str, list] = {}
                    for g in grades:
                        ders_notlar.setdefault(g.ders, []).append(f"{g.not_turu}-{g.not_sirasi}: {g.puan}")
                    for ders, notlar in ders_notlar.items():
                        lines.append(f"  {ders}: {', '.join(notlar)}")

                # Devamsızlık
                attendance = ak.get_attendance(student_id=child.id)
                if attendance:
                    ozurlu = sum(1 for a in attendance if a.turu == "ozurlu")
                    ozursuz = sum(1 for a in attendance if a.turu == "ozursuz")
                    toplam = len(attendance)
                    lines.append(f"\n--- DEVAMSIZLIK ---")
                    lines.append(f"  Toplam: {toplam} gün (Özürlü: {ozurlu}, Özürsüz: {ozursuz})")

                # Sınav sonuçları
                results = od.get_results(student_id=child.id)
                if results:
                    lines.append(f"\n--- SINAV SONUÇLARI ---")
                    for r in results[-10:]:  # son 10
                        lines.append(f"  Puan: {r.score:.0f} | "
                                     f"Doğru: {r.correct_count} | "
                                     f"Yanlış: {r.wrong_count} | "
                                     f"Boş: {r.empty_count} | "
                                     f"Net: {r.net_score:.1f}")

                # Telafi görevleri
                telafi = od.get_telafi_tasks(student_id=child.id)
                if telafi:
                    aktif = [t for t in telafi if t.status in ("assigned", "in_progress")]
                    if aktif:
                        lines.append(f"\n--- TELAFİ GÖREVLERİ ({len(aktif)} aktif) ---")
                        for t in aktif[:5]:
                            lines.append(f"  {t.outcome_text} | "
                                         f"Bant: {t.color_band} | "
                                         f"Durum: {t.status}")

        elif role == "Öğrenci":
            lines.append("=== ÖĞRENCİ VERİ PANELİ ===")
            all_students = ak.get_students()
            student = None
            for s in all_students:
                if name.lower() in s.tam_ad.lower():
                    student = s
                    break
            if not student:
                lines.append("Öğrenci kaydı bulunamadı.")
                return "\n".join(lines)

            lines.append(f"Öğrenci: {student.tam_ad} | Sınıf: {student.sinif}/{student.sube}")

            grades = ak.get_grades(student_id=student.id)
            if grades:
                lines.append("\n--- NOTLARIM ---")
                ders_notlar: dict[str, list] = {}
                for g in grades:
                    ders_notlar.setdefault(g.ders, []).append(f"{g.not_turu}-{g.not_sirasi}: {g.puan}")
                for ders, notlar in ders_notlar.items():
                    lines.append(f"  {ders}: {', '.join(notlar)}")

            attendance = ak.get_attendance(student_id=student.id)
            if attendance:
                toplam = len(attendance)
                ozursuz = sum(1 for a in attendance if a.turu == "ozursuz")
                lines.append(f"\n--- DEVAMSIZLIĞIM ---")
                lines.append(f"  Toplam: {toplam} gün | Özürsüz: {ozursuz}")

            results = od.get_results(student_id=student.id)
            if results:
                lines.append(f"\n--- SINAV SONUÇLARIM ---")
                for r in results[-10:]:
                    lines.append(f"  Puan: {r.score:.0f} | "
                                 f"Net: {r.net_score:.1f} | "
                                 f"Doğru: {r.correct_count}")

        elif role == "Öğretmen":
            lines.append("=== ÖĞRETMEN VERİ PANELİ ===")
            all_students = ak.get_students(durum="aktif")
            lines.append(f"Toplam aktif öğrenci: {len(all_students)}")

            # Sınıf bazlı özet
            sinif_sayilari: dict[str, int] = {}
            for s in all_students:
                key = f"{s.sinif}/{s.sube}"
                sinif_sayilari[key] = sinif_sayilari.get(key, 0) + 1
            if sinif_sayilari:
                lines.append("\n--- SINIF MEVCUTLARI ---")
                for k, v in sorted(sinif_sayilari.items()):
                    lines.append(f"  {k}: {v} öğrenci")

            # Son sınav sonuçları
            all_results = od.get_results()
            if all_results:
                lines.append(f"\n--- SON SINAVLAR ({len(all_results)} sonuç) ---")
                for r in all_results[-5:]:
                    lines.append(f"  {r.student_name} | "
                                 f"Puan: {r.score:.0f} | "
                                 f"Net: {r.net_score:.1f}")

        elif role == "Yonetici":
            lines.append("=== YÖNETİCİ VERİ PANELİ ===")
            all_students = ak.get_students()
            aktif = [s for s in all_students if s.durum == "aktif"]
            lines.append(f"Toplam öğrenci: {len(all_students)} | Aktif: {len(aktif)}")

            teachers = ak.get_teachers()
            lines.append(f"Toplam öğretmen: {len(teachers)}")

            # Sınıf bazlı mevcutlar
            sinif_sayilari: dict[str, int] = {}
            for s in aktif:
                key = f"{s.sinif}/{s.sube}"
                sinif_sayilari[key] = sinif_sayilari.get(key, 0) + 1
            if sinif_sayilari:
                lines.append("\n--- SINIF MEVCUTLARI ---")
                for k, v in sorted(sinif_sayilari.items()):
                    lines.append(f"  {k}: {v} öğrenci")

            # Devamsızlık özeti
            all_attendance = ak.get_attendance()
            if all_attendance:
                ozursuz = sum(1 for a in all_attendance if a.turu == "ozursuz")
                lines.append(f"\n--- DEVAMSIZLIK ÖZETİ ---")
                lines.append(f"  Toplam kayıt: {len(all_attendance)} | Özürsüz: {ozursuz}")

            # Sınav istatistikleri
            all_results = od.get_results()
            if all_results:
                scores = [r.score for r in all_results if r.score is not None]
                if scores:
                    avg = sum(scores) / len(scores)
                    lines.append(f"\n--- SINAV İSTATİSTİKLERİ ---")
                    lines.append(f"  Toplam sonuç: {len(scores)}")
                    lines.append(f"  Ortalama puan: {avg:.1f}")
                    lines.append(f"  En yüksek: {max(scores):.0f} | En düşük: {min(scores):.0f}")

            # Soru bankası
            all_q = od.get_questions()
            if all_q:
                approved = sum(1 for q in all_q if q.status == "approved")
                lines.append(f"\n--- SORU BANKASI ---")
                lines.append(f"  Toplam: {len(all_q)} | Onaylı: {approved}")

    except Exception:
        lines.append("(Veri yüklenirken hata oluştu)")

    return "\n".join(lines) if lines else ""


# ═══════════════════════════════════════════════════════════════════════════════
# MERKEZ BEYİN — 18 MODÜLDEN VERİ TOPLAMA
# ═══════════════════════════════════════════════════════════════════════════════

def _collect_all_module_data() -> dict:
    """18 modulden veri topla. Session cache (5dk TTL)."""
    _ck = "_ai_brain_data"
    _ts = "_ai_brain_ts"
    now = time.time()
    if _ck in st.session_state and now - st.session_state.get(_ts, 0) < 300:
        return st.session_state[_ck]

    from utils.tenant import get_tenant_dir
    td = get_tenant_dir()
    data: dict[str, dict] = {}

    def _safe(fn):
        try:
            return fn()
        except Exception:
            return []

    def _safe_list(store, key):
        try:
            return store.load_list(key) if hasattr(store, "load_list") else store._load(getattr(store, f"_{key}_path", ""))
        except Exception:
            return []

    # 1. Akademik Takip
    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        students = _safe(lambda: ak.get_students())
        aktif = [s for s in students if getattr(s, "durum", "aktif") == "aktif"]
        teachers = _safe(lambda: ak.get_teachers())
        grades = _safe(lambda: ak.get_grades())
        attendance = _safe(lambda: ak.get_attendance())
        odevler = _safe(lambda: ak.get_odevler())
        etut = _safe(lambda: ak.get_etut_kayitlari())
        data["akademik"] = {
            "students": students, "students_aktif": len(aktif),
            "teachers": teachers, "teachers_count": len(teachers),
            "grades": grades, "attendance": attendance,
            "odevler": odevler, "etut": etut,
        }
    except Exception:
        data["akademik"] = {"students": [], "students_aktif": 0, "teachers": [], "teachers_count": 0,
                            "grades": [], "attendance": [], "odevler": [], "etut": []}

    # 2. Olcme Degerlendirme
    try:
        from models.olcme_degerlendirme import DataStore as ODS
        od = ODS()
        questions = _safe(lambda: od.get_questions())
        results = _safe(lambda: od.get_results())
        telafi = _safe(lambda: od.get_telafi_tasks())
        data["olcme"] = {
            "questions": questions, "questions_count": len(questions),
            "results": results, "telafi": telafi,
            "approved_q": sum(1 for q in questions if getattr(q, "status", "") == "approved"),
        }
    except Exception:
        data["olcme"] = {"questions": [], "questions_count": 0, "results": [], "telafi": [],
                         "approved_q": 0}

    # 3. Insan Kaynaklari
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        employees = _safe(lambda: ik.load_list("employees"))
        aktif_emp = [e for e in employees if e.get("durum", "aktif") == "aktif"]
        candidates = _safe(lambda: ik.load_list("candidates"))
        positions = _safe(lambda: ik.load_list("positions"))
        perf = _safe(lambda: ik.load_list("performance_reviews"))
        izinler = _safe(lambda: ik.load_list("izinler"))
        data["ik"] = {
            "employees": employees, "employees_aktif": len(aktif_emp),
            "candidates": candidates, "positions": positions,
            "performance": perf, "izinler": izinler,
        }
    except Exception:
        data["ik"] = {"employees": [], "employees_aktif": 0, "candidates": [],
                      "positions": [], "performance": [], "izinler": []}

    # 4. Rehberlik
    try:
        from models.rehberlik import RehberlikDataStore
        rh = RehberlikDataStore(os.path.join(td, "rehberlik"))
        gorusmeler = _safe(lambda: rh.load_list("gorusme_kayitlari"))
        vakalar = _safe(lambda: rh.load_list("vaka_kayitlari"))
        bep = _safe(lambda: rh.load_list("bep_kayitlari"))
        data["rehberlik"] = {"gorusmeler": gorusmeler, "vakalar": vakalar, "bep": bep}
    except Exception:
        data["rehberlik"] = {"gorusmeler": [], "vakalar": [], "bep": []}

    # 5. Okul Sagligi
    try:
        from models.okul_sagligi import SaglikDataStore
        sg = SaglikDataStore(os.path.join(td, "saglik"))
        revir = _safe(lambda: sg.load_list("revir_ziyaretleri"))
        kaza = _safe(lambda: sg.load_list("kaza_olaylari"))
        data["saglik"] = {"revir": revir, "kaza": kaza}
    except Exception:
        data["saglik"] = {"revir": [], "kaza": []}

    # 6. Butce Gelir Gider
    try:
        from models.butce_gelir_gider import BGGDataStore
        bg = BGGDataStore(os.path.join(td, "butce"))
        gelir = _safe(lambda: bg.load_list("gelir_kayitlari"))
        gider = _safe(lambda: bg.load_list("gider_kayitlari"))
        t_gelir = sum(float(g.get("tutar", 0)) for g in gelir)
        t_gider = sum(float(g.get("tutar", 0)) for g in gider)
        data["butce"] = {"gelir": gelir, "gider": gider,
                         "toplam_gelir": t_gelir, "toplam_gider": t_gider}
    except Exception:
        data["butce"] = {"gelir": [], "gider": [], "toplam_gelir": 0, "toplam_gider": 0}

    # 7. Tuketim Demirbas
    try:
        from models.tuketim_demirbas import TDMDataStore
        tdm = TDMDataStore(os.path.join(td, "tdm"))
        urunler = _safe(lambda: tdm.load_list("tuketim_urunleri"))
        demirbaslar = _safe(lambda: tdm.load_list("demirbaslar"))
        satin_alma = _safe(lambda: tdm.load_list("satin_alma_talepleri"))
        data["tdm"] = {"urunler": urunler, "demirbaslar": demirbaslar, "satin_alma": satin_alma}
    except Exception:
        data["tdm"] = {"urunler": [], "demirbaslar": [], "satin_alma": []}

    # 8. Toplanti
    try:
        from models.toplanti_kurullar import ToplantiDataStore
        tp = ToplantiDataStore(os.path.join(td, "toplanti"))
        meetings = _safe(lambda: tp.load_list("meetings"))
        decisions = _safe(lambda: tp.load_list("decisions"))
        gorevler = _safe(lambda: tp.load_list("gorevler"))
        data["toplanti"] = {"meetings": meetings, "decisions": decisions, "gorevler": gorevler}
    except Exception:
        data["toplanti"] = {"meetings": [], "decisions": [], "gorevler": []}

    # 9. Sosyal Etkinlik
    try:
        from models.sosyal_etkinlik import SosyalEtkinlikDataStore
        se = SosyalEtkinlikDataStore(os.path.join(td, "sosyal_etkinlik"))
        kulupler = _safe(lambda: se.load_list("kulupler"))
        etkinlikler = _safe(lambda: se.load_list("etkinlikler"))
        data["sosyal"] = {"kulupler": kulupler, "etkinlikler": etkinlikler}
    except Exception:
        data["sosyal"] = {"kulupler": [], "etkinlikler": []}

    # 10. Destek Hizmetleri
    try:
        from models.destek_hizmetleri import DestekDataStore
        ds = DestekDataStore(os.path.join(td, "destek"))
        tickets = _safe(lambda: ds.load_list("tickets"))
        periyodik = _safe(lambda: ds.load_list("periyodik_gorevler"))
        data["destek"] = {"tickets": tickets, "periyodik": periyodik}
    except Exception:
        data["destek"] = {"tickets": [], "periyodik": []}

    # 11. Randevu Ziyaretci
    try:
        from models.randevu_ziyaretci import RZYDataStore
        rz = RZYDataStore(os.path.join(td, "randevu"))
        randevular = _safe(lambda: rz.load_list("randevular"))
        ziyaretler = _safe(lambda: rz.load_list("ziyaret_kayitlari"))
        data["randevu"] = {"randevular": randevular, "ziyaretler": ziyaretler}
    except Exception:
        data["randevu"] = {"randevular": [], "ziyaretler": []}

    # 12. Sivil Savunma ISG
    try:
        from models.sivil_savunma_isg import SSGDataStore
        ss = SSGDataStore(os.path.join(td, "ssg"))
        tatbikat = _safe(lambda: ss.load_list("tatbikat_kayitlari"))
        riskler = _safe(lambda: ss.load_list("risk_kayitlari"))
        denetimler = _safe(lambda: ss.load_list("denetim_kayitlari"))
        data["ssg"] = {"tatbikat": tatbikat, "riskler": riskler, "denetimler": denetimler}
    except Exception:
        data["ssg"] = {"tatbikat": [], "riskler": [], "denetimler": []}

    # 13. Kutuphane
    try:
        from models.kutuphane import KutuphaneDataStore
        ku = KutuphaneDataStore(os.path.join(td, "kutuphane"))
        materyaller = _safe(lambda: ku.load_list("materyaller"))
        odunc = _safe(lambda: ku.load_list("odunc_islemleri"))
        data["kutuphane"] = {"materyaller": materyaller, "odunc": odunc}
    except Exception:
        data["kutuphane"] = {"materyaller": [], "odunc": []}

    # 14. Dijital Kutuphane
    try:
        from models.dijital_kutuphane import DijitalKutuphaneDataStore
        dk = DijitalKutuphaneDataStore(os.path.join(td, "dijital_kutuphane"))
        kaynaklar = _safe(lambda: dk.load_list("dijital_kaynaklar"))
        data["dijital_kutuphane"] = {"kaynaklar": kaynaklar}
    except Exception:
        data["dijital_kutuphane"] = {"kaynaklar": []}

    # 15. Egitim Koclugu
    try:
        from models.egitim_koclugu import get_ek_store
        ek = get_ek_store()
        ek_ogrenciler = _safe(lambda: ek.load_list("ogrenciler"))
        ek_gorusmeler = _safe(lambda: ek.load_list("gorusmeler"))
        ek_hedefler = _safe(lambda: ek.load_list("hedefler"))
        data["egitim_koclugu"] = {
            "ogrenciler": ek_ogrenciler, "gorusmeler": ek_gorusmeler,
            "hedefler": ek_hedefler,
        }
    except Exception:
        data["egitim_koclugu"] = {"ogrenciler": [], "gorusmeler": [], "hedefler": []}

    # 16. Erken Uyari
    try:
        from models.erken_uyari import ErkenUyariStore
        eu = ErkenUyariStore()
        risks = _safe(lambda: eu.get_latest_risks())
        alerts = _safe(lambda: eu.get_active_alerts())
        data["erken_uyari"] = {"risks": risks, "alerts": alerts}
    except Exception:
        data["erken_uyari"] = {"risks": [], "alerts": []}

    # 17. Kayit Modulu
    try:
        from models.kayit_modulu import get_kayit_store
        ky = get_kayit_store()
        adaylar = _safe(lambda: ky.load_all())
        data["kayit"] = {"adaylar": adaylar}
    except Exception:
        data["kayit"] = {"adaylar": []}

    # 18. CEFR Placement
    try:
        from models.cefr_exam import CEFRPlacementStore
        cp = CEFRPlacementStore()
        cp_results = _safe(lambda: cp._load(cp._results_path))
        cp_exams = _safe(lambda: cp._load(cp._exams_path))
        data["cefr"] = {"results": cp_results, "exams": cp_exams}
    except Exception:
        data["cefr"] = {"results": [], "exams": []}

    # 18b. CEFR Mock Exam Sonuclari
    try:
        from models.cefr_exam import CEFRExamStore
        _ce_store = CEFRExamStore()
        ce_results = _safe(lambda: _ce_store._load(_ce_store._results_path))
        ce_exams = _safe(lambda: _ce_store._load(_ce_store._exams_path))
        ce_scores = [float(r.get("percentage", 0)) for r in ce_results if r.get("percentage", 0)]
        ce_avg = sum(ce_scores) / len(ce_scores) if ce_scores else 0
        data["cefr_mock"] = {
            "results": ce_results, "exams": ce_exams,
            "total_results": len(ce_results), "avg_score": round(ce_avg, 1),
        }
    except Exception:
        data["cefr_mock"] = {"results": [], "exams": [], "total_results": 0, "avg_score": 0}

    # 18c. Yabanci Dil Quiz & Sinav Sonuclari
    try:
        from models.yd_assessment import YdAssessmentStore
        yd_store = YdAssessmentStore()
        yd_results = _safe(lambda: yd_store.get_results())
        yd_exams = _safe(lambda: yd_store.get_exams())
        # Kategori bazli gruplama
        yd_quiz_results = [r for r in yd_results if isinstance(r, dict) and r.get("exam_category") == "quiz"
                           or hasattr(r, "exam_category") and getattr(r, "exam_category", "") == "quiz"]
        yd_haftalik = [r for r in yd_results if isinstance(r, dict) and r.get("exam_category") == "haftalik"
                       or hasattr(r, "exam_category") and getattr(r, "exam_category", "") == "haftalik"]
        yd_all_scores = []
        for r in yd_results:
            s = r.get("score", 0) if isinstance(r, dict) else getattr(r, "score", 0)
            if s and float(s) > 0:
                yd_all_scores.append(float(s))
        yd_avg = sum(yd_all_scores) / len(yd_all_scores) if yd_all_scores else 0
        data["yd_sinav"] = {
            "results": yd_results, "exams": yd_exams,
            "quiz_count": len(yd_quiz_results), "haftalik_count": len(yd_haftalik),
            "total_results": len(yd_results), "avg_score": round(yd_avg, 1),
            "all_scores": yd_all_scores,
        }
    except Exception:
        data["yd_sinav"] = {"results": [], "exams": [], "quiz_count": 0, "haftalik_count": 0,
                            "total_results": 0, "avg_score": 0, "all_scores": []}

    # 18d. Rehberlik Test & Envanter
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_RT
        _rt_testler = _safe(lambda: _CML_RT.load_rehberlik_testler())
        _rt_oturumlar = _safe(lambda: _CML_RT.load_rehberlik_test_oturumlari())
        _rt_tamamlanan = [o for o in _rt_oturumlar if o.get("durum") == "TAMAMLANDI"]
        data["rhb_test"] = {
            "testler": _rt_testler, "test_count": len(_rt_testler),
            "oturum_count": len(_rt_oturumlar), "tamamlanan": len(_rt_tamamlanan),
        }
    except Exception:
        data["rhb_test"] = {"testler": [], "test_count": 0, "oturum_count": 0, "tamamlanan": 0}

    # 18d2. Tüm Test Sonuçları Birleşik (Rehberlik + Kayıt)
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_AT
        _all_tests = _safe(lambda: _CML_AT.load_all_student_tests()) or []
        _test_turleri = {}
        for _t in _all_tests:
            _test_turleri[_t.get("test_adi", "?")] = _test_turleri.get(_t.get("test_adi", "?"), 0) + 1
        data["tum_testler"] = {
            "toplam": len(_all_tests),
            "rehberlik": sum(1 for t in _all_tests if "Rehberlik" in t.get("kaynak", "")),
            "kayit": sum(1 for t in _all_tests if "Kayit" in t.get("kaynak", "")),
            "test_turleri": _test_turleri,
        }
    except Exception:
        data["tum_testler"] = {"toplam": 0, "rehberlik": 0, "kayit": 0, "test_turleri": {}}

    # 18e. Aile Bilgi Formlari (Rehberlik)
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_ABF
        abf_list = _safe(lambda: _CML_ABF.load_aile_bilgi_formlari())
        # Kritik risk faktörleri say
        _abf_kritik = 0
        for abf in abf_list:
            if abf.get("anne_birlikte_bosanmis") in ("Boşanmış", "Ayrı") or abf.get("baba_birlikte_bosanmis") in ("Boşanmış", "Ayrı"):
                _abf_kritik += 1
            elif abf.get("anne_sag_olu") == "Ölü" or abf.get("baba_sag_olu") == "Ölü":
                _abf_kritik += 1
            elif abf.get("etkisindeki_olay"):
                _abf_kritik += 1
            elif abf.get("bagimllik_durumu"):
                _abf_kritik += 1
        data["aile_bilgi"] = {
            "formlar": abf_list, "toplam": len(abf_list), "kritik_aile": _abf_kritik,
        }
    except Exception:
        data["aile_bilgi"] = {"formlar": [], "toplam": 0, "kritik_aile": 0}

    # 18f. MEB Dijital Formlar (35 form — toplu)
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_MEB
        _meb_stats = _safe(lambda: _CML_MEB.get_meb_form_stats()) or {}
        _meb_risk = _safe(lambda: _CML_MEB.get_meb_risk_factors()) or {}
        data["meb_formlar"] = {
            "form_sayilari": _meb_stats,
            "toplam_kayit": _meb_risk.get("toplam_kayit", 0),
            "kategori": _meb_risk.get("kategori", {}),
            "risk": _meb_risk.get("risk", {}),
        }
    except Exception:
        data["meb_formlar"] = {"form_sayilari": {}, "toplam_kayit": 0, "kategori": {}, "risk": {}}

    # 19. Kurumsal Organizasyon (KOI)
    try:
        from views.kim_organizational import load_profile
        profile = _safe(load_profile) or {}
        data["koi"] = {"profile": profile, "kurum_adi": profile.get("name", "")}
    except Exception:
        data["koi"] = {"profile": {}, "kurum_adi": ""}

    # 20. Halkla Iliskiler — sozlesmeler
    try:
        import json as _j
        _soz_path = os.path.join(td, "sozlesmeler.json")
        soz = []
        if os.path.exists(_soz_path):
            with open(_soz_path, "r", encoding="utf-8") as f:
                soz = _j.load(f)
        data["halkla_iliskiler"] = {"sozlesmeler": soz if isinstance(soz, list) else []}
    except Exception:
        data["halkla_iliskiler"] = {"sozlesmeler": []}

    # 21. Sosyal Medya
    try:
        _sm_path = os.path.join(td, "sosyal_medya")
        sm_hesaplar = []
        sm_paylasimlari = []
        for fname in ("hesaplar.json", "paylasimlar.json"):
            fp = os.path.join(_sm_path, fname)
            if os.path.exists(fp):
                import json as _j2
                with open(fp, "r", encoding="utf-8") as f:
                    items = _j2.load(f)
                if fname == "hesaplar.json":
                    sm_hesaplar = items if isinstance(items, list) else []
                else:
                    sm_paylasimlari = items if isinstance(items, list) else []
        data["sosyal_medya"] = {"hesaplar": sm_hesaplar, "paylasimlar": sm_paylasimlari}
    except Exception:
        data["sosyal_medya"] = {"hesaplar": [], "paylasimlar": []}

    # 22. Kurum Hizmetleri (yemek, servis, etkinlik)
    try:
        _kh_path = os.path.join(td, "kurum_hizmetleri")
        kh_data = {}
        for fname in ("yemek_menu.json", "servis_rotalari.json", "etkinlik_duyurular.json"):
            fp = os.path.join(_kh_path, fname)
            if os.path.exists(fp):
                import json as _j3
                with open(fp, "r", encoding="utf-8") as f:
                    kh_data[fname.replace(".json", "")] = _j3.load(f)
        data["kurum_hizmetleri"] = kh_data if kh_data else {"yemek_menu": [], "servis_rotalari": []}
    except Exception:
        data["kurum_hizmetleri"] = {}

    # 23. Kullanici Yonetimi
    try:
        from utils.auth import _load_users
        users = _safe(_load_users) or []
        role_counts = {}
        for u in users:
            r = u.get("role", "?")
            role_counts[r] = role_counts.get(r, 0) + 1
        data["kullanici"] = {"users": users, "role_counts": role_counts, "total": len(users)}
    except Exception:
        data["kullanici"] = {"users": [], "role_counts": {}, "total": 0}

    # 24. Mezunlar
    try:
        _mez_path = os.path.join(td, "mezunlar")
        mez = []
        fp = os.path.join(_mez_path, "mezunlar.json")
        if os.path.exists(fp):
            import json as _j4
            with open(fp, "r", encoding="utf-8") as f:
                mez = _j4.load(f)
        data["mezunlar"] = {"mezunlar": mez if isinstance(mez, list) else []}
    except Exception:
        data["mezunlar"] = {"mezunlar": []}

    st.session_state[_ck] = data
    st.session_state[_ts] = now
    return data


def _safe_len(obj):
    """Guvenli len — list/dict/object."""
    if isinstance(obj, (list, dict)):
        return len(obj)
    return 0


def _next_chart_key(prefix="ch"):
    """Her plotly_chart icin benzersiz key uret."""
    if "_ai_chart_seq" not in st.session_state:
        st.session_state["_ai_chart_seq"] = 0
    st.session_state["_ai_chart_seq"] += 1
    return f"_ai_{prefix}_{st.session_state['_ai_chart_seq']}"


def _donut(labels, values, colors=None, center="", height=280):
    """Donut grafik helper — bos veri kontrollu, unique key."""
    if not values or sum(values) == 0:
        st.info("Bu alanda henuz veri bulunmuyor.")
        return
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors or SC_COLORS[:len(labels)],
                    line=dict(color="#1e293b", width=2)),
    ))
    sc_pie(fig, height=height, center_text=center)
    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG,
                    key=_next_chart_key("donut"))


def _bar(x, y, colors=None, height=280, horizontal=False):
    """Bar grafik helper — bos veri kontrollu, unique key."""
    if not y or sum(y) == 0:
        st.info("Bu alanda henuz veri bulunmuyor.")
        return
    if horizontal:
        fig = go.Figure(go.Bar(y=x, x=y, orientation="h",
                               marker_color=colors or SC_COLORS[0], text=y, textposition="auto"))
    else:
        fig = go.Figure(go.Bar(x=x, y=y,
                               marker_color=colors or SC_COLORS[0], text=y, textposition="auto"))
    sc_bar(fig, height=height, horizontal=horizontal)
    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG,
                    key=_next_chart_key("bar"))


def _gauge(value: float, max_val: float, label: str, color: str = "#6366f1"):
    """SVG gauge — kurum skoru icin."""
    pct = min(value / max_val * 100, 100) if max_val > 0 else 0
    arc_len = 141.37 * pct / 100
    val_display = f"{value:.0f}"
    st.markdown(
        f'<div style="text-align:center;padding:8px">'
        f'<svg width="160" height="100" viewBox="0 0 110 85">'
        f'<path d="M 10 55 A 45 45 0 0 1 100 55" fill="none" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M 10 55 A 45 45 0 0 1 100 55" fill="none" stroke="{color}" stroke-width="10" '
        f'stroke-linecap="round" stroke-dasharray="{arc_len} 141.37" style="transition:stroke-dasharray 1s ease"/>'
        f'<text x="55" y="48" text-anchor="middle" font-size="22" font-weight="800" fill="{color}">{val_display}</text>'
        f'<text x="55" y="66" text-anchor="middle" font-size="9" fill="#94a3b8" font-weight="600">{label}</text>'
        f'<text x="10" y="75" text-anchor="middle" font-size="7" fill="#475569">0</text>'
        f'<text x="100" y="75" text-anchor="middle" font-size="7" fill="#475569">{max_val:.0f}</text>'
        f'</svg></div>',
        unsafe_allow_html=True,
    )


def _score_card(title: str, score: float, max_score: float, icon: str, color: str):
    """Premium skor karti — yuzde gostergeli."""
    pct = round(score / max_score * 100, 1) if max_score > 0 else 0
    bar_color = "#22c55e" if pct >= 70 else ("#f59e0b" if pct >= 40 else "#ef4444")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
    padding:16px;border:1px solid {color}30;margin:4px 0;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:1.3rem;">{icon}</span>
    <span style="color:{color};font-weight:800;font-size:1.2rem;">%{pct}</span>
    </div>
    <div style="color:#c7d2fe;font-weight:700;font-size:.9rem;margin:6px 0 4px;">{title}</div>
    <div style="background:#1e293b;border-radius:6px;height:8px;overflow:hidden;">
    <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:6px;transition:width .5s;"></div>
    </div>
    <div style="color:#64748b;font-size:.7rem;margin-top:4px;">{score:.0f} / {max_score:.0f}</div>
    </div>""", unsafe_allow_html=True)


def _compute_institution_score(data: dict) -> dict:
    """Kurum saglik skoru hesapla — 0-100 arasi, 7 boyutlu."""
    scores = {}

    # 1. Akademik Doluluk (ogrenci + ogretmen var mi)
    ak = data.get("akademik", {})
    stu = ak.get("students_aktif", 0)
    tch = ak.get("teachers_count", 0)
    scores["Akademik Kadro"] = min(100, (min(stu, 200) / 200 * 60) + (min(tch, 30) / 30 * 40))

    # 2. Olcme & Degerlendirme (soru + sinav)
    od = data.get("olcme", {})
    q_count = od.get("questions_count", 0)
    r_count = _safe_len(od.get("results", []))
    scores["Olcme Degerlendirme"] = min(100, (min(q_count, 500) / 500 * 50) + (min(r_count, 200) / 200 * 50))

    # 3. IK Doluluk
    ik = data.get("ik", {})
    emp = ik.get("employees_aktif", 0)
    scores["Insan Kaynaklari"] = min(100, min(emp, 50) / 50 * 100)

    # 4. Mali Saglik (gelir > gider?)
    bu = data.get("butce", {})
    gelir, gider = bu.get("toplam_gelir", 0), bu.get("toplam_gider", 0)
    if gelir + gider > 0:
        scores["Mali Durum"] = min(100, max(0, (gelir / (gelir + gider)) * 100))
    else:
        scores["Mali Durum"] = 50  # veri yok = nötr

    # 5. Destek & Operasyon (ticket cozum orani)
    ds = data.get("destek", {})
    tickets = ds.get("tickets", [])
    if tickets:
        cozulen = sum(1 for t in tickets if t.get("durum") in ("cozuldu", "kapandi", "tamamlandi"))
        scores["Operasyonel"] = round(cozulen / len(tickets) * 100)
    else:
        scores["Operasyonel"] = 50

    # 6. Risk Durumu (dusuk risk = yuksek skor)
    eu = data.get("erken_uyari", {})
    risks = eu.get("risks", [])
    if risks:
        high_risk = sum(1 for r in risks if r.get("risk_level") in ("HIGH", "CRITICAL"))
        scores["Risk Yonetimi"] = max(0, 100 - (high_risk / len(risks) * 100))
    else:
        scores["Risk Yonetimi"] = 80

    # 7. Yabanci Dil Performansi (CEFR Placement + CEFR Mock + Quiz)
    yd = data.get("yd_sinav", {})
    cefr = data.get("cefr", {})
    cefr_mock = data.get("cefr_mock", {})
    yd_score_val = yd.get("avg_score", 0)
    cefr_count = _safe_len(cefr.get("results", []))
    mock_count = cefr_mock.get("total_results", 0)
    mock_avg = cefr_mock.get("avg_score", 0)
    yd_result_count = yd.get("total_results", 0)
    if yd_result_count > 0 or cefr_count > 0 or mock_count > 0:
        yd_puan_skor = min(100, yd_score_val * 1.2) if yd_score_val > 0 else 40
        cefr_skor = min(100, cefr_count * 20) if cefr_count > 0 else 30
        mock_skor = min(100, mock_avg * 1.1) if mock_avg > 0 else 30
        scores["Yabanci Dil"] = round(yd_puan_skor * 0.4 + cefr_skor * 0.3 + mock_skor * 0.3)
    else:
        scores["Yabanci Dil"] = 30  # veri yok = dusuk

    # 8. Veri Giris Kapsami (kac modul aktif veri girmis)
    active_modules = 0
    for mod, vals in data.items():
        total = sum(_safe_len(v) for v in vals.values() if isinstance(v, list))
        if total > 0:
            active_modules += 1
    scores["Veri Kapsami"] = round(active_modules / 20 * 100)

    overall = round(sum(scores.values()) / len(scores), 1) if scores else 0
    return {"scores": scores, "overall": overall}


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — KURUM PANORAMASI
# ═══════════════════════════════════════════════════════════════════════════════

def _smart_verdict(value, thresholds: list[tuple], reverse=False) -> tuple[str, str, str]:
    """Akilli yorum motoru — deger + esik → emoji + renk + yorum.
    thresholds: [(esik, emoji, renk, yorum), ...] buyukten kucuge siralanmis.
    reverse=True ise dusuk deger iyi demek (orn: devamsizlik).
    """
    for threshold, emoji, color, comment in thresholds:
        if (not reverse and value >= threshold) or (reverse and value <= threshold):
            return emoji, color, comment
    last = thresholds[-1]
    return last[1], last[2], last[3]


def _verdict_card(label: str, value, unit: str, thresholds: list[tuple], reverse=False):
    """Akilli yorum kartı — deger goster + otomatik emoji + renk + yorum."""
    # Guvenli float donusum — %, 1: gibi prefixleri temizle
    raw = str(value).replace("%", "").replace(",", "").strip()
    try:
        num = float(raw)
    except (ValueError, TypeError):
        num = 0
    emoji, color, comment = _smart_verdict(num, thresholds, reverse)
    st.markdown(f"""<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
    padding:16px;border:1.5px solid {color}30;margin:4px 0;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
    <div style="font-size:.72rem;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">{label}</div>
    <div style="font-size:1.6rem;font-weight:900;color:{color};margin:4px 0;">{value} <span style="font-size:.7rem;color:#475569;">{unit}</span></div>
    </div>
    <span style="font-size:1.8rem;">{emoji}</span>
    </div>
    <div style="font-size:.78rem;color:{color};margin-top:4px;padding-top:6px;
    border-top:1px solid {color}20;">{comment}</div>
    </div>""", unsafe_allow_html=True)


# Standart esik setleri
_TH_RATIO = [(25, "🔴", "#ef4444", "Kritik: Oran cok yuksek — ogretmen sayisi arttirilmali"),
              (20, "🟠", "#f97316", "Yuksek: Sinif mevcutlari idealin ustunde"),
              (15, "🟡", "#f59e0b", "Orta: Kabul edilebilir ama iyilestirilebilir"),
              (10, "🟢", "#22c55e", "Ideal: Mukemmel ogretmen/ogrenci dengesı"),
              (0, "🏆", "#6366f1", "Ustun: Bireysel ilgi imkani cok yuksek")]

_TH_SCORE = [(85, "🏆", "#6366f1", "Ustun basari — tebrikler!"),
              (70, "🟢", "#22c55e", "Iyi: Hedeflerin ustunde performans"),
              (55, "🟡", "#f59e0b", "Orta: Gelisime acik alanlar var"),
              (40, "🟠", "#f97316", "Dusuk: Acil iyilestirme gerekli"),
              (0, "🔴", "#ef4444", "Kritik: Kapsamli mudahale plani sart")]

_TH_COUNT_LOW = [(0, "🟢", "#22c55e", "Temiz: Kayit yok — iyi isaret"),
                  (3, "🟡", "#f59e0b", "Az: Takip edilmeli"),
                  (10, "🟠", "#f97316", "Orta: Dikkat gerektiriyor"),
                  (20, "🔴", "#ef4444", "Yuksek: Acil mudahale gerekli")]

_TH_COVERAGE = [(90, "🏆", "#6366f1", "Tam kapsam — sistem tam kapasite calisiyor"),
                 (70, "🟢", "#22c55e", "Iyi kapsam — cogu modul aktif"),
                 (50, "🟡", "#f59e0b", "Orta kapsam — bazi moduller bos"),
                 (30, "🟠", "#f97316", "Dusuk kapsam — modullerin cogu kullanilmiyor"),
                 (0, "🔴", "#ef4444", "Kritik — sistem potansiyelinin altinda")]


def _student_segmentation(data: dict) -> dict[str, list]:
    """Ogrenci segmentasyonu — 4 kume: Yildiz, Stabil, Potansiyel, Risk.
    Not ortalamasi + devamsizlik + risk skoru kombinasyonu."""
    ak = data.get("akademik", {})
    eu = data.get("erken_uyari", {})
    grades = ak.get("grades", [])
    attendance = ak.get("attendance", [])
    students = ak.get("students", [])

    if not students:
        return {"yildiz": [], "stabil": [], "potansiyel": [], "risk": []}

    # Ogrenci bazli metrikler
    stu_not: dict[str, float] = {}
    for g in grades:
        sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        try:
            stu_not.setdefault(sid, []).append(float(puan))
        except (TypeError, ValueError):
            pass

    stu_dev: dict[str, int] = {}
    for a in attendance:
        sid = getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")
        turu = getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")
        if turu == "ozursuz":
            stu_dev[sid] = stu_dev.get(sid, 0) + 1

    risk_map = {}
    for r in eu.get("risks", []):
        risk_map[r.get("student_id", "")] = r.get("risk_score", 0)

    segments: dict[str, list] = {"yildiz": [], "stabil": [], "potansiyel": [], "risk": []}

    for s in students:
        durum = getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")
        if durum != "aktif":
            continue
        sid = getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "")
        ad = getattr(s, "tam_ad", "") if not isinstance(s, dict) else f"{s.get('ad', '')} {s.get('soyad', '')}"
        sinif = getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", "")
        sube = getattr(s, "sube", "") if not isinstance(s, dict) else s.get("sube", "")

        notlar = stu_not.get(sid, [])
        ort = sum(notlar) / len(notlar) if notlar else 50  # veri yoksa orta varsay
        dev = stu_dev.get(sid, 0)
        risk = risk_map.get(sid, 25)

        entry = {"ad": ad, "sinif": f"{sinif}/{sube}", "ort": round(ort, 1), "dev": dev, "risk": round(risk, 1)}

        if ort >= 80 and dev <= 2 and risk < 30:
            segments["yildiz"].append(entry)
        elif ort >= 60 and dev <= 5 and risk < 50:
            segments["stabil"].append(entry)
        elif ort >= 50 and (ort < 80) and risk < 60:
            segments["potansiyel"].append(entry)
        else:
            segments["risk"].append(entry)

    return segments


def _render_segmentation(segments: dict[str, list]):
    """Ogrenci segmentasyonunu gorsel olarak render et."""
    seg_info = [
        ("yildiz", "🌟 Yildiz Ogrenciler", "#6366f1", "Yuksek basari, dusuk risk — olimpiyat/proje yonlendirin"),
        ("stabil", "✅ Stabil Ogrenciler", "#22c55e", "Dengeli performans — motivasyonu koruyun"),
        ("potansiyel", "⚡ Potansiyel Ogrenciler", "#f59e0b", "Kapasitesi yuksek ama kullanmiyor — bireysel destek verin"),
        ("risk", "🔴 Risk Grubu", "#ef4444", "Acil mudahale — veli gorusmesi + rehberlik + etut"),
    ]

    # Donut
    labels = []
    values = []
    colors = []
    for key, label, color, _ in seg_info:
        cnt = len(segments.get(key, []))
        if cnt > 0:
            labels.append(label.split(" ", 1)[1])
            values.append(cnt)
            colors.append(color)
    total_stu = sum(values)
    if values:
        _donut(labels, values, colors,
               center=f"<b>{total_stu}</b><br><span style='font-size:10px;color:#64748b'>Ogrenci</span>")

    # Segment kartlari
    cols = st.columns(4)
    for i, (key, label, color, desc) in enumerate(seg_info):
        with cols[i]:
            cnt = len(segments.get(key, []))
            pct = round(cnt / total_stu * 100) if total_stu > 0 else 0
            st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;
            text-align:center;border:2px solid {color}40;">
            <div style="font-size:1.8rem;font-weight:900;color:{color};">{cnt}</div>
            <div style="font-size:.75rem;color:#94a3b8;">%{pct} — {label.split(' ',1)[1]}</div>
            </div>""", unsafe_allow_html=True)

    # Detay expander'lar
    for key, label, color, desc in seg_info:
        items = segments.get(key, [])
        if items:
            with st.expander(f"{label} ({len(items)} ogrenci) — {desc}", expanded=False):
                import pandas as pd
                df = pd.DataFrame(items)
                st.dataframe(df, use_container_width=True, height=min(200, len(items)*40+50))


def _institution_index(data: dict) -> dict:
    """Kurum Karsilastirma Endeksi — 0-1000 arasi skor.
    Turkiye ozel okul sektoru referanslariyla karsilastirma."""
    score = _compute_institution_score(data)
    ak = data.get("akademik", {})
    od = data.get("olcme", {})
    s_cnt = ak.get("students_aktif", 0)
    t_cnt = ak.get("teachers_count", 0)

    # 10 boyutlu endeks (her biri 0-100, toplam 0-1000)
    dims = {}

    # 1. Akademik Kadro (ogretmen/ogrenci orani)
    ratio = s_cnt / max(t_cnt, 1)
    dims["Ogretmen Orani"] = max(0, min(100, 100 - (ratio - 12) * 5))  # ideal=12, her +1 icin -5 puan

    # 2. Soru Bankasi Zenginligi
    q = od.get("questions_count", 0)
    dims["Soru Bankasi"] = min(100, q / 100)  # 10000 soru = 100

    # 3. Dijital Olgunluk
    active = sum(1 for vals in data.values()
                 if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0
                 or any(isinstance(v, (str, dict)) and v for v in vals.values()))
    dims["Dijital Olgunluk"] = round(active / max(len(data), 1) * 100)

    # 4. Risk Yonetimi
    dims["Risk Yonetimi"] = score["scores"].get("Risk Yonetimi", 50)

    # 5. Mali Saglik
    dims["Mali Saglik"] = score["scores"].get("Mali Durum", 50)

    # 6. Operasyonel
    dims["Operasyonel"] = score["scores"].get("Operasyonel", 50)

    # 7. Akademik Basari
    grades = ak.get("grades", [])
    if grades:
        puanlar = []
        for g in grades:
            try:
                puanlar.append(float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)))
            except (TypeError, ValueError):
                pass
        dims["Akademik Basari"] = round(sum(puanlar) / len(puanlar)) if puanlar else 50
    else:
        dims["Akademik Basari"] = 50

    # 8. Ogrenci Katilim (devamsizlik tersi)
    att = ak.get("attendance", [])
    ozursuz = sum(1 for a in att if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
    dev_oran = ozursuz / max(s_cnt, 1) * 100
    dims["Ogrenci Katilim"] = max(0, min(100, 100 - dev_oran * 5))

    # 9. Zenginlestirme (kulup + etkinlik)
    se = data.get("sosyal", {})
    kulup = _safe_len(se.get("kulupler", []))
    etkinlik = _safe_len(se.get("etkinlikler", []))
    dims["Zenginlestirme"] = min(100, (kulup * 15 + etkinlik * 10))

    # 10. Iletisim & Seffaflik (kullanici sayisi vs beklenen)
    kul = data.get("kullanici", {}).get("total", 0)
    beklenen = s_cnt + t_cnt + ak.get("teachers_count", 0)
    dims["Iletisim"] = min(100, round(kul / max(beklenen, 1) * 100))

    total_index = round(sum(dims.values()) / len(dims) * 10)  # 0-1000 arasi
    return {"dims": dims, "index": total_index}


def _render_institution_index(idx: dict):
    """Kurum endeksini premium gorsel olarak render et."""
    index = idx["index"]
    dims = idx["dims"]

    # Endeks seviyesi
    if index >= 800: grade, color, emoji = "A+", "#6366f1", "🏆"
    elif index >= 650: grade, color, emoji = "A", "#22c55e", "🟢"
    elif index >= 500: grade, color, emoji = "B", "#10b981", "✅"
    elif index >= 350: grade, color, emoji = "C", "#f59e0b", "🟡"
    elif index >= 200: grade, color, emoji = "D", "#f97316", "🟠"
    else: grade, color, emoji = "F", "#ef4444", "🔴"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border-radius:16px;
    padding:20px;text-align:center;border:2px solid {color}40;margin:8px 0;">
    <div style="font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:1px;">
    Kurum Karsilastirma Endeksi</div>
    <div style="font-size:3rem;font-weight:900;color:{color};margin:8px 0;">
    {emoji} {index}<span style="font-size:1rem;color:#475569;">/1000</span></div>
    <div style="font-size:1.2rem;color:{color};font-weight:700;">Derece: {grade}</div>
    </div>""", unsafe_allow_html=True)

    # 10 boyut bar chart
    fig_idx = go.Figure()
    sorted_dims = sorted(dims.items(), key=lambda x: -x[1])
    fig_idx.add_trace(go.Bar(
        y=[d[0] for d in sorted_dims],
        x=[d[1] for d in sorted_dims],
        orientation="h",
        marker_color=[("#22c55e" if v >= 70 else ("#f59e0b" if v >= 40 else "#ef4444")) for _, v in sorted_dims],
        text=[f"{v:.0f}" for _, v in sorted_dims],
        textposition="auto",
    ))
    fig_idx.update_layout(
        height=350, margin=dict(l=120, r=20, t=10, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 100], gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
        yaxis=dict(tickfont=dict(color="#c7d2fe", size=10)),
        font=dict(color="#94a3b8"),
    )
    st.plotly_chart(fig_idx, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))


def _cost_benefit_analysis(data: dict) -> list[dict]:
    """Maliyet-Fayda Analizi — her aksiyonun tahmini maliyeti ve beklenen getirisi.
    ROI (Return on Investment) tahmini ile onceliklendirme."""
    items = []
    ak = data.get("akademik", {})
    bu = data.get("butce", {})
    tdm = data.get("tdm", {})
    ik = data.get("ik", {})
    s_cnt = ak.get("students_aktif", 0)

    # 1. Stok satin alma
    urunler = tdm.get("urunler", [])
    kritik = [u for u in urunler
              if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
              and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0]
    if kritik:
        maliyet = sum((u.get("min_stok", 0) - u.get("stok", 0)) * u.get("birim_fiyat", 0)
                      for u in kritik if u.get("birim_fiyat"))
        items.append({
            "aksiyon": "Kritik stok satin alma",
            "maliyet": maliyet,
            "maliyet_str": f"{maliyet:,.0f} TL",
            "fayda": "Operasyonel sureklilik, egitim aksamasi engellenir",
            "roi": "YUKSEK — stoksuzluk maliyeti satin almadan 3-5x fazla",
            "oncelik": "ACIL",
            "sure": "1 Hafta",
            "risk_azaltma": 85,
        })

    # 2. IK personel kaydı tamamlama
    emp = ik.get("employees_aktif", 0)
    if emp < 10 and s_cnt > 30:
        items.append({
            "aksiyon": "IK personel kaydini tamamlama",
            "maliyet": 0,
            "maliyet_str": "0 TL (veri girisi)",
            "fayda": "Performans takibi, izin yonetimi, bordro sistemi aktif olur",
            "roi": "COK YUKSEK — sifir maliyet, tam operasyonel kazanim",
            "oncelik": "ACIL",
            "sure": "3 Gun",
            "risk_azaltma": 70,
        })

    # 3. CEFR seviye tespiti
    if not data.get("cefr", {}).get("exams"):
        items.append({
            "aksiyon": "CEFR sene basi seviye tespiti",
            "maliyet": 0,
            "maliyet_str": "0 TL (sistem icinde)",
            "fayda": f"{s_cnt} ogrencinin Ingilizce seviyesi belirlenir, bireysel plan yapilir",
            "roi": "YUKSEK — dil egitimi verimi %30-40 artar",
            "oncelik": "YUKSEK",
            "sure": "2 Hafta",
            "risk_azaltma": 40,
        })

    # 4. Rehberlik baslatma
    if not data.get("rehberlik", {}).get("gorusmeler") and s_cnt > 30:
        items.append({
            "aksiyon": "Rehberlik programi baslatma",
            "maliyet": 0,
            "maliyet_str": "0 TL (mevcut kadro)",
            "fayda": "Riskli ogrenci erken tespit, vaka yonetimi, BEP ihtiyaci belirleme",
            "roi": "COK YUKSEK — ogrenci kaybi onlenir, memnuniyet artar",
            "oncelik": "YUKSEK",
            "sure": "2 Hafta",
            "risk_azaltma": 65,
        })

    # 5. Tatbikat
    if not data.get("ssg", {}).get("tatbikat"):
        items.append({
            "aksiyon": "Tahliye tatbikati planlama ve uygulama",
            "maliyet": 500,
            "maliyet_str": "~500 TL (malzeme + organizasyon)",
            "fayda": "Yasal zorunluluk karsilanir, ogrenci/personel guvenligi artar",
            "roi": "ZORUNLU — yapilmamasi cezai yaptirima yol acar",
            "oncelik": "YUKSEK",
            "sure": "1 Ay",
            "risk_azaltma": 90,
        })

    # 6. Kulup cesitliligi
    kulupler = data.get("sosyal", {}).get("kulupler", [])
    if len(kulupler) < 3 and s_cnt > 30:
        items.append({
            "aksiyon": "5 yeni kulup acma (spor, sanat, bilim, drama, muzik)",
            "maliyet": 2000,
            "maliyet_str": "~2,000 TL (malzeme + etkinlik)",
            "fayda": "Ogrenci bagliligi %25+ artar, okul tercihi sebebi olur",
            "roi": "ORTA-YUKSEK — kayit oranini dogrudan etkiler",
            "oncelik": "ORTA",
            "sure": "1 Ay",
            "risk_azaltma": 30,
        })

    # 7. Dijital kutuphane
    if not data.get("dijital_kutuphane", {}).get("kaynaklar"):
        items.append({
            "aksiyon": "Dijital kutuphane icerik ekleme (50+ kaynak)",
            "maliyet": 0,
            "maliyet_str": "0 TL (acik kaynaklar + mevcut icerik)",
            "fayda": "Ogrenci erisimi 7/24, ogrenme esnekligi, veli memnuniyeti",
            "roi": "YUKSEK — sifir maliyetle buyuk etki",
            "oncelik": "ORTA",
            "sure": "2 Hafta",
            "risk_azaltma": 20,
        })

    return sorted(items, key=lambda x: -x["risk_azaltma"])


def _render_cost_benefit(items: list[dict]):
    """Maliyet-fayda tablosunu premium render."""
    if not items:
        return

    # Ozet
    toplam_maliyet = sum(i["maliyet"] for i in items)
    ort_risk = round(sum(i["risk_azaltma"] for i in items) / len(items))
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
    padding:16px 20px;margin:8px 0;border:1px solid rgba(99,102,241,0.2);">
    <div style="display:flex;justify-content:space-around;text-align:center;">
    <div><div style="font-size:.7rem;color:#64748b;">Toplam Aksiyon</div>
    <div style="font-size:1.5rem;font-weight:900;color:#6366f1;">{len(items)}</div></div>
    <div><div style="font-size:.7rem;color:#64748b;">Tahmini Maliyet</div>
    <div style="font-size:1.5rem;font-weight:900;color:#f59e0b;">{toplam_maliyet:,.0f} TL</div></div>
    <div><div style="font-size:.7rem;color:#64748b;">Ort Risk Azaltma</div>
    <div style="font-size:1.5rem;font-weight:900;color:#22c55e;">%{ort_risk}</div></div>
    </div></div>""", unsafe_allow_html=True)

    # Her aksiyon
    for i, item in enumerate(items):
        clr = {"ACIL": "#ef4444", "YUKSEK": "#f97316", "ORTA": "#f59e0b", "DUSUK": "#22c55e"}.get(item["oncelik"], "#64748b")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px 18px;
        margin:6px 0;border-left:4px solid {clr};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="font-size:.92rem;font-weight:700;color:#e2e8f0;">{item['aksiyon']}</div>
        <div style="display:flex;gap:12px;align-items:center;">
        <span style="font-size:.75rem;color:{clr};font-weight:700;padding:2px 8px;
        background:{clr}15;border-radius:4px;">{item['oncelik']}</span>
        <span style="font-size:.75rem;color:#64748b;">{item['sure']}</span>
        </div></div>
        <div style="display:flex;gap:20px;margin-top:8px;font-size:.8rem;">
        <div><span style="color:#64748b;">Maliyet:</span> <span style="color:#f59e0b;font-weight:600;">{item['maliyet_str']}</span></div>
        <div><span style="color:#64748b;">Risk Azaltma:</span> <span style="color:#22c55e;font-weight:600;">%{item['risk_azaltma']}</span></div>
        </div>
        <div style="color:#94a3b8;font-size:.78rem;margin-top:4px;">{item['fayda']}</div>
        <div style="color:#818cf8;font-size:.75rem;margin-top:2px;">ROI: {item['roi']}</div>
        </div>""", unsafe_allow_html=True)

    # ROI scatter — maliyet vs risk azaltma
    if len(items) >= 3:
        fig_roi = go.Figure()
        fig_roi.add_trace(go.Scatter(
            x=[i["maliyet"] for i in items],
            y=[i["risk_azaltma"] for i in items],
            mode="markers+text",
            text=[i["aksiyon"][:25] for i in items],
            textposition="top center",
            textfont=dict(size=8, color="#c7d2fe"),
            marker=dict(size=18,
                        color=[i["risk_azaltma"] for i in items],
                        colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#22c55e"]],
                        showscale=True,
                        colorbar=dict(title=dict(text="Risk%", font=dict(color="#94a3b8")),
                                      tickfont=dict(color="#94a3b8")),
                        line=dict(width=1, color="#334155")),
        ))
        fig_roi.update_layout(
            height=320, margin=dict(l=50, r=20, t=20, b=50),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Maliyet (TL)", gridcolor="#1e293b",
                       tickfont=dict(color="#94a3b8")),
            yaxis=dict(title="Risk Azaltma (%)", gridcolor="#1e293b",
                       tickfont=dict(color="#94a3b8")),
            font=dict(color="#94a3b8"),
        )
        # Ideal zon — sag ust (dusuk maliyet, yuksek etki)
        fig_roi.add_annotation(x=0, y=90, text="IDEAL ZON<br>(Dusuk maliyet, Yuksek etki)",
                               showarrow=False, font=dict(size=9, color="rgba(34,197,94,0.25)"))
        st.plotly_chart(fig_roi, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))


def _parent_priority_list(data: dict) -> list[dict]:
    """Veli Iletisim Oncelik Siralamasi — hangi velilerle once gorusulmeli?
    Ogrenci risk skoru + devamsizlik + not dusuklugu + telafi borcu."""
    ak = data.get("akademik", {})
    eu = data.get("erken_uyari", {})
    grades = ak.get("grades", [])
    attendance = ak.get("attendance", [])
    students = ak.get("students", [])

    stu_metrics: dict[str, dict] = {}
    for s in students:
        durum = getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")
        if durum != "aktif":
            continue
        sid = getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "")
        ad = getattr(s, "tam_ad", "") if not isinstance(s, dict) else f"{s.get('ad', '')} {s.get('soyad', '')}"
        sinif = getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", "")
        sube = getattr(s, "sube", "") if not isinstance(s, dict) else s.get("sube", "")
        veli_adi = getattr(s, "veli_adi", "") if not isinstance(s, dict) else s.get("veli_adi", "")
        veli_tel = getattr(s, "veli_telefon", "") if not isinstance(s, dict) else s.get("veli_telefon", "")
        stu_metrics[sid] = {"ad": ad, "sinif": f"{sinif}/{sube}", "veli": veli_adi, "tel": veli_tel,
                             "ort": 0, "dev": 0, "risk": 0, "aciliyet": 0, "neden": []}

    # Notlar
    for g in grades:
        sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
        if sid in stu_metrics:
            try:
                p = float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0))
                if stu_metrics[sid]["ort"] == 0:
                    stu_metrics[sid]["ort"] = p
                else:
                    stu_metrics[sid]["ort"] = (stu_metrics[sid]["ort"] + p) / 2
            except (TypeError, ValueError):
                pass

    # Devamsizlik
    for a in attendance:
        sid = getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")
        turu = getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")
        if sid in stu_metrics and turu == "ozursuz":
            stu_metrics[sid]["dev"] += 1

    # Risk
    for r in eu.get("risks", []):
        sid = r.get("student_id", "")
        if sid in stu_metrics:
            stu_metrics[sid]["risk"] = r.get("risk_score", 0)

    # Aciliyet hesapla
    for sid, m in stu_metrics.items():
        score = 0
        nedenler = []
        if m["ort"] > 0 and m["ort"] < 50:
            score += 40
            nedenler.append(f"Not ortalamasi dusuk ({m['ort']:.0f})")
        elif m["ort"] > 0 and m["ort"] < 60:
            score += 20
            nedenler.append(f"Not ortalamasi gelismeli ({m['ort']:.0f})")
        if m["dev"] >= 5:
            score += 30
            nedenler.append(f"Devamsizlik yuksek ({m['dev']} gun)")
        elif m["dev"] >= 3:
            score += 15
            nedenler.append(f"Devamsizlik ({m['dev']} gun)")
        if m["risk"] >= 55:
            score += 30
            nedenler.append(f"Risk yuksek (%{m['risk']:.0f})")
        m["aciliyet"] = score
        m["neden"] = nedenler

    # Sadece aciliyeti > 0 olanlari dondur
    result = [m for m in stu_metrics.values() if m["aciliyet"] > 0]
    return sorted(result, key=lambda x: -x["aciliyet"])


def _render_parent_priority(items: list[dict]):
    """Veli iletisim oncelik listesini render et."""
    if not items:
        st.info("Tum ogrenciler iyi durumda — acil veli gorusmesi gerekmiyor.")
        return

    st.markdown(f"**{len(items)} veli ile gorusme onerilir:**")
    for i, item in enumerate(items[:15]):
        urgency = item["aciliyet"]
        clr = "#ef4444" if urgency >= 40 else ("#f59e0b" if urgency >= 20 else "#3b82f6")
        nedenler = " | ".join(item["neden"]) if item["neden"] else "Genel takip"

        st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;padding:8px 0;
        border-bottom:1px solid #1e293b;">
        <div style="min-width:28px;text-align:center;font-size:1rem;font-weight:800;color:{clr};">{i+1}</div>
        <div style="flex:1;">
        <div style="color:#e2e8f0;font-weight:600;font-size:.88rem;">
        {item['ad']} <span style="color:#64748b;font-size:.75rem;">({item['sinif']})</span></div>
        <div style="color:#94a3b8;font-size:.78rem;">Veli: {item['veli'] or '-'} | Tel: {item['tel'] or '-'}</div>
        <div style="color:{clr};font-size:.75rem;margin-top:2px;">{nedenler}</div>
        </div>
        <div style="min-width:50px;text-align:center;">
        <div style="font-size:1.1rem;font-weight:800;color:{clr};">{urgency}</div>
        <div style="font-size:.6rem;color:#475569;">aciliyet</div>
        </div>
        </div>""", unsafe_allow_html=True)


def _projection_model(data: dict) -> dict:
    """Gelecek Projeksiyon Modeli — mevcut verilerden 3 ay sonrasi tahmini.
    Kurum skoru + endeks + risk trendini tahmin eder."""
    inst = _compute_institution_score(data)
    idx = _institution_index(data)
    current_score = inst["overall"]
    current_index = idx["index"]

    # Iyilestirme potansiyeli — bos modullerin doldurulma etkisi
    active = sum(1 for vals in data.values()
                 if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0
                 or any(isinstance(v, (str, dict)) and v for v in vals.values()))
    total_mods = max(len(data), 1)
    bos_mod_cnt = total_mods - active

    # Senaryo 1: Hicbir sey yapilmazsa (status quo)
    sq_score = max(current_score - 2, 0)  # hafif dusus (veri eskir)
    sq_index = max(current_index - 20, 0)

    # Senaryo 2: Temel aksiyonlar yapilirsa (IK + Butce + Rehberlik)
    base_boost = min(25, bos_mod_cnt * 3)
    base_score = min(100, current_score + base_boost)
    base_index = min(1000, current_index + base_boost * 8)

    # Senaryo 3: Tam aksiyon plani uygulanirsa
    full_boost = min(45, bos_mod_cnt * 5 + 10)
    full_score = min(100, current_score + full_boost)
    full_index = min(1000, current_index + full_boost * 10)

    return {
        "current": {"score": current_score, "index": current_index},
        "status_quo": {"score": sq_score, "index": sq_index, "label": "Hicbir sey yapilmazsa"},
        "base": {"score": base_score, "index": base_index, "label": "Temel aksiyonlar"},
        "full": {"score": full_score, "index": full_index, "label": "Tam aksiyon plani"},
    }


def _render_projection(proj: dict):
    """Projeksiyon modelini gorsel olarak render et."""
    scenarios = [
        ("Mevcut", proj["current"]["score"], proj["current"]["index"], "#94a3b8"),
        (proj["status_quo"]["label"], proj["status_quo"]["score"], proj["status_quo"]["index"], "#ef4444"),
        (proj["base"]["label"], proj["base"]["score"], proj["base"]["index"], "#f59e0b"),
        (proj["full"]["label"], proj["full"]["score"], proj["full"]["index"], "#22c55e"),
    ]

    # Bar chart — 3 senaryo karsilastirma
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[s[0] for s in scenarios],
        y=[s[1] for s in scenarios],
        marker_color=[s[3] for s in scenarios],
        text=[f"%{s[1]:.0f}" for s in scenarios],
        textposition="auto",
        name="Kurum Skoru",
    ))
    fig.update_layout(
        height=280, margin=dict(l=40, r=20, t=30, b=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[0, 100], gridcolor="#1e293b", title="Kurum Skoru (%)",
                   tickfont=dict(color="#94a3b8")),
        xaxis=dict(tickfont=dict(color="#c7d2fe", size=10)),
        font=dict(color="#94a3b8"), showlegend=False,
        title=dict(text="3 Ay Sonra Kurum Skoru Projeksiyonu", font=dict(size=12, color="#818cf8")),
    )
    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # Endeks karsilastirma
    cols = st.columns(4)
    for i, (label, score, index, color) in enumerate(scenarios):
        grade = "A+" if index >= 800 else ("A" if index >= 650 else ("B" if index >= 500 else ("C" if index >= 350 else "D")))
        with cols[i]:
            st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:12px;
            text-align:center;border:2px solid {color}30;">
            <div style="font-size:.65rem;color:#64748b;text-transform:uppercase;">{label}</div>
            <div style="font-size:1.6rem;font-weight:900;color:{color};">{index}</div>
            <div style="font-size:.7rem;color:#475569;">Endeks | Derece: {grade}</div>
            </div>""", unsafe_allow_html=True)


def _semester_comparison(data: dict) -> dict:
    """Donem Karsilastirma Analizi — 1. Donem vs 2. Donem.
    Not ortalamalari, devamsizlik, sinav sonuclari donemsel karsilastirma."""
    ak = data.get("akademik", {})
    grades = ak.get("grades", [])
    attendance = ak.get("attendance", [])

    d1_notlar = []
    d2_notlar = []
    d1_dev = 0
    d2_dev = 0

    for g in grades:
        donem = getattr(g, "donem", "") if not isinstance(g, dict) else g.get("donem", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        try:
            p = float(puan)
            if "1" in str(donem):
                d1_notlar.append(p)
            elif "2" in str(donem):
                d2_notlar.append(p)
            else:
                # Donem bilgisi yoksa tarihe gore tahmin
                tarih = getattr(g, "tarih", "") if not isinstance(g, dict) else g.get("tarih", "")
                ay = int(str(tarih)[5:7]) if tarih and len(str(tarih)) >= 7 else 0
                if 9 <= ay <= 1 or ay == 12 or ay == 11 or ay == 10:
                    d1_notlar.append(p)
                else:
                    d2_notlar.append(p)
        except (TypeError, ValueError):
            pass

    for a in attendance:
        turu = getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")
        tarih = getattr(a, "tarih", "") if not isinstance(a, dict) else a.get("tarih", "")
        if turu != "ozursuz":
            continue
        try:
            ay = int(str(tarih)[5:7]) if tarih and len(str(tarih)) >= 7 else 0
            if 9 <= ay <= 12 or ay == 1:
                d1_dev += 1
            else:
                d2_dev += 1
        except (ValueError, TypeError):
            pass

    d1_ort = round(sum(d1_notlar) / len(d1_notlar), 1) if d1_notlar else 0
    d2_ort = round(sum(d2_notlar) / len(d2_notlar), 1) if d2_notlar else 0
    delta_ort = round(d2_ort - d1_ort, 1) if d1_ort and d2_ort else 0
    delta_dev = d2_dev - d1_dev

    # Ders bazli donem karsilastirma
    ders_d1: dict[str, list] = {}
    ders_d2: dict[str, list] = {}
    for g in grades:
        ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
        donem = getattr(g, "donem", "") if not isinstance(g, dict) else g.get("donem", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        try:
            p = float(puan)
            if "1" in str(donem):
                ders_d1.setdefault(ders, []).append(p)
            elif "2" in str(donem):
                ders_d2.setdefault(ders, []).append(p)
        except (TypeError, ValueError):
            pass

    ders_comp = []
    all_dersler = set(list(ders_d1.keys()) + list(ders_d2.keys()))
    for d in sorted(all_dersler):
        d1 = round(sum(ders_d1.get(d, [])) / len(ders_d1[d]), 1) if d in ders_d1 and ders_d1[d] else 0
        d2 = round(sum(ders_d2.get(d, [])) / len(ders_d2[d]), 1) if d in ders_d2 and ders_d2[d] else 0
        delta = round(d2 - d1, 1) if d1 and d2 else 0
        ders_comp.append({"ders": d, "d1": d1, "d2": d2, "delta": delta})

    return {
        "d1_ort": d1_ort, "d2_ort": d2_ort, "delta_ort": delta_ort,
        "d1_not_cnt": len(d1_notlar), "d2_not_cnt": len(d2_notlar),
        "d1_dev": d1_dev, "d2_dev": d2_dev, "delta_dev": delta_dev,
        "ders_comp": ders_comp,
        "has_data": bool(d1_notlar or d2_notlar),
    }


def _render_semester_comparison(comp: dict):
    """Donem karsilastirma sonuclarini render et."""
    if not comp["has_data"]:
        st.info("Donem bazli karsilastirma icin yeterli veri yok. Notlarda donem bilgisi girildiginde aktif olacak.")
        return

    # Genel karsilastirma kartlari
    c1, c2, c3 = st.columns(3)
    with c1:
        delta = comp["delta_ort"]
        clr = "#22c55e" if delta > 0 else ("#ef4444" if delta < 0 else "#94a3b8")
        arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;
        text-align:center;border:1px solid {clr}30;">
        <div style="font-size:.7rem;color:#64748b;">Not Ortalamasi</div>
        <div style="display:flex;justify-content:center;gap:16px;margin:8px 0;">
        <div><span style="color:#94a3b8;font-size:.65rem;">1.Donem</span><br>
        <span style="font-size:1.3rem;font-weight:800;color:#c7d2fe;">{comp['d1_ort']}</span></div>
        <div style="font-size:1.5rem;color:{clr};font-weight:900;">{arrow}</div>
        <div><span style="color:#94a3b8;font-size:.65rem;">2.Donem</span><br>
        <span style="font-size:1.3rem;font-weight:800;color:{clr};">{comp['d2_ort']}</span></div>
        </div>
        <div style="color:{clr};font-size:.85rem;font-weight:700;">{delta:+.1f} puan</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        delta_d = comp["delta_dev"]
        clr_d = "#22c55e" if delta_d < 0 else ("#ef4444" if delta_d > 0 else "#94a3b8")
        arrow_d = "↓" if delta_d < 0 else ("↑" if delta_d > 0 else "→")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;
        text-align:center;border:1px solid {clr_d}30;">
        <div style="font-size:.7rem;color:#64748b;">Ozursuz Devamsizlik</div>
        <div style="display:flex;justify-content:center;gap:16px;margin:8px 0;">
        <div><span style="color:#94a3b8;font-size:.65rem;">1.Donem</span><br>
        <span style="font-size:1.3rem;font-weight:800;color:#c7d2fe;">{comp['d1_dev']}</span></div>
        <div style="font-size:1.5rem;color:{clr_d};font-weight:900;">{arrow_d}</div>
        <div><span style="color:#94a3b8;font-size:.65rem;">2.Donem</span><br>
        <span style="font-size:1.3rem;font-weight:800;color:{clr_d};">{comp['d2_dev']}</span></div>
        </div>
        <div style="color:{clr_d};font-size:.85rem;font-weight:700;">{delta_d:+d} gun</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        # Genel yorum
        if comp["delta_ort"] > 3:
            yorum, emoji, yorum_clr = "Basari yukseliste!", "📈", "#22c55e"
        elif comp["delta_ort"] < -3:
            yorum, emoji, yorum_clr = "Basari dususte — mudahale gerekli!", "📉", "#ef4444"
        elif comp["d1_ort"] == 0 or comp["d2_ort"] == 0:
            yorum, emoji, yorum_clr = "Tek donem verisi — karsilastirma sinirli", "📊", "#f59e0b"
        else:
            yorum, emoji, yorum_clr = "Stabil performans", "➡️", "#94a3b8"
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;
        text-align:center;border:1px solid {yorum_clr}30;">
        <div style="font-size:.7rem;color:#64748b;">Donem Degerlendirme</div>
        <div style="font-size:2rem;margin:8px 0;">{emoji}</div>
        <div style="color:{yorum_clr};font-size:.88rem;font-weight:700;">{yorum}</div>
        </div>""", unsafe_allow_html=True)

    # Ders bazli karsilastirma bar chart
    ders_comp = comp.get("ders_comp", [])
    valid_comp = [d for d in ders_comp if d["d1"] > 0 or d["d2"] > 0]
    if valid_comp:
        st.markdown("#### Ders Bazli Donem Karsilastirma")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[d["ders"] for d in valid_comp],
            y=[d["d1"] for d in valid_comp],
            name="1. Donem", marker_color="#6366f1",
            text=[f"{d['d1']}" for d in valid_comp], textposition="auto",
        ))
        fig.add_trace(go.Bar(
            x=[d["ders"] for d in valid_comp],
            y=[d["d2"] for d in valid_comp],
            name="2. Donem", marker_color="#22c55e",
            text=[f"{d['d2']}" for d in valid_comp], textposition="auto",
        ))
        fig.update_layout(
            barmode="group", height=300,
            margin=dict(l=40, r=20, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
            xaxis=dict(tickfont=dict(color="#c7d2fe")),
            legend=dict(font=dict(color="#94a3b8")),
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))


def _goal_tracker(data: dict) -> dict:
    """Hedef Takip Motoru — kurum hedeflerini otomatik olc, sapma analizi yap.
    10 standart kurum hedefi + gerceklesen + sapma."""
    ak = data.get("akademik", {})
    od = data.get("olcme", {})
    ik = data.get("ik", {})
    bu = data.get("butce", {})

    s_cnt = ak.get("students_aktif", 0)
    t_cnt = ak.get("teachers_count", 0)
    grades = ak.get("grades", [])
    attendance = ak.get("attendance", [])

    # Genel not ortalamasi
    puanlar = []
    for g in grades:
        try:
            puanlar.append(float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)))
        except (TypeError, ValueError):
            pass
    genel_ort = round(sum(puanlar) / len(puanlar), 1) if puanlar else 0

    # Ozursuz devamsizlik
    ozursuz = sum(1 for a in attendance
                  if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
    dev_per_stu = round(ozursuz / s_cnt, 1) if s_cnt > 0 else 0

    # Modul kapsam
    active = sum(1 for vals in data.values()
                 if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0
                 or any(isinstance(v, (str, dict)) and v for v in vals.values()))
    kapsam_pct = round(active / max(len(data), 1) * 100)

    goals = [
        {"hedef": "Not Ortalamasi", "target": 75, "actual": genel_ort,
         "unit": "puan", "icon": "📝",
         "yorum_iyi": "Akademik basari hedefte", "yorum_kotu": "Not ortalamasi dusuk — etut programi planlayin"},
        {"hedef": "Ogretmen/Ogrenci Orani", "target": 15, "actual": round(s_cnt / max(t_cnt, 1), 1),
         "unit": "1:N", "icon": "👨‍🏫", "reverse": True,
         "yorum_iyi": "Ideal sinif mevcudu", "yorum_kotu": "Ogretmen sayisi arttirilmali"},
        {"hedef": "Devamsizlik (kisi basina)", "target": 3, "actual": dev_per_stu,
         "unit": "gun", "icon": "📋", "reverse": True,
         "yorum_iyi": "Devamsizlik kontrol altinda", "yorum_kotu": "Devamsizlik yuksek — veli iletisimi artirin"},
        {"hedef": "Soru Bankasi", "target": 5000, "actual": od.get("questions_count", 0),
         "unit": "soru", "icon": "❓",
         "yorum_iyi": "Zengin soru bankasi", "yorum_kotu": "Soru bankasini zenginlestirin"},
        {"hedef": "Dijital Modul Kapsami", "target": 80, "actual": kapsam_pct,
         "unit": "%", "icon": "📊",
         "yorum_iyi": "Dijital donusum hedefte", "yorum_kotu": "Bos modulleri aktiflestirinS"},
        {"hedef": "Aktif Personel Kaydi", "target": max(t_cnt + 5, 15), "actual": ik.get("employees_aktif", 0),
         "unit": "kisi", "icon": "👥",
         "yorum_iyi": "Kadro kaydi tamam", "yorum_kotu": "IK'ya tum personeli kaydedin"},
        {"hedef": "Butce Dengesı (Gelir/Gider)", "target": 100, "actual": round(
             bu.get("toplam_gelir", 0) / max(bu.get("toplam_gider", 0), 1) * 100),
         "unit": "%", "icon": "💰",
         "yorum_iyi": "Mali denge saglandi", "yorum_kotu": "Gelir artirmali veya gider azaltilmali"},
        {"hedef": "Sosyal Kulup Sayisi", "target": 5, "actual": _safe_len(data.get("sosyal", {}).get("kulupler", [])),
         "unit": "kulup", "icon": "🎭",
         "yorum_iyi": "Zengin kulup yelpazesi", "yorum_kotu": "Kulup cesitliligini artirin"},
        {"hedef": "Kutuphane Materyal", "target": 500, "actual": _safe_len(data.get("kutuphane", {}).get("materyaller", [])),
         "unit": "adet", "icon": "📚",
         "yorum_iyi": "Zengin kutuphane", "yorum_kotu": "Kutuphane envanterini sisteme girin"},
        {"hedef": "Kurum Endeksi", "target": 800, "actual": _institution_index(data)["index"],
         "unit": "/1000", "icon": "🏆",
         "yorum_iyi": "A+ derecesi — tebrikler!", "yorum_kotu": "Eksik modulleri tamamlayin"},
    ]

    return {"goals": goals}


def _render_goal_tracker(tracker: dict):
    """Hedef takip motorunu premium render et."""
    goals = tracker.get("goals", [])
    if not goals:
        return

    # Ozet: kac hedef tuttu?
    tuttu = 0
    for g in goals:
        reverse = g.get("reverse", False)
        if (not reverse and g["actual"] >= g["target"]) or (reverse and g["actual"] <= g["target"]):
            tuttu += 1
    pct = round(tuttu / len(goals) * 100)
    ov_color = "#22c55e" if pct >= 70 else ("#f59e0b" if pct >= 40 else "#ef4444")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
    padding:16px 20px;margin:8px 0;border:1.5px solid {ov_color}40;text-align:center;">
    <div style="font-size:.75rem;color:#64748b;text-transform:uppercase;">Hedef Gerceklesme Orani</div>
    <div style="font-size:2.5rem;font-weight:900;color:{ov_color};">{tuttu}/{len(goals)}</div>
    <div style="font-size:.85rem;color:{ov_color};">%{pct} hedef karsilandi</div>
    </div>""", unsafe_allow_html=True)

    # Her hedef
    for g in goals:
        reverse = g.get("reverse", False)
        reached = (not reverse and g["actual"] >= g["target"]) or (reverse and g["actual"] <= g["target"])
        clr = "#22c55e" if reached else "#ef4444"
        emoji = "✅" if reached else "❌"
        yorum = g.get("yorum_iyi", "") if reached else g.get("yorum_kotu", "")

        if g["target"] > 0:
            if reverse:
                fill_pct = min(100, max(0, (1 - (g["actual"] - g["target"]) / max(g["target"], 1)) * 100)) if g["actual"] > 0 else 100
            else:
                fill_pct = min(100, round(g["actual"] / g["target"] * 100))
        else:
            fill_pct = 100 if reached else 0

        st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:12px 16px;
        margin:4px 0;border-left:4px solid {clr};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:1.1rem;">{g['icon']}</span>
        <span style="color:#e2e8f0;font-weight:600;font-size:.88rem;">{g['hedef']}</span>
        </div>
        <div style="display:flex;align-items:center;gap:12px;">
        <span style="color:#94a3b8;font-size:.78rem;">Hedef: {g['target']} {g['unit']}</span>
        <span style="color:{clr};font-weight:800;font-size:1rem;">{g['actual']} {g['unit']}</span>
        <span>{emoji}</span>
        </div></div>
        <div style="background:#1e293b;border-radius:4px;height:6px;margin:6px 0;overflow:hidden;">
        <div style="width:{fill_pct}%;height:100%;background:{clr};border-radius:4px;"></div></div>
        <div style="color:{clr};font-size:.75rem;">{yorum}</div>
        </div>""", unsafe_allow_html=True)


def _gap_analysis(data: dict) -> list[dict]:
    """OLMASI GEREKEN vs MEVCUT DURUM — Gap Analizi.
    Her boyut: ideal standart, mevcut deger, fark, kapatma stratejisi, timeline, maliyet, etki skoru."""
    ak = data.get("akademik", {})
    od = data.get("olcme", {})
    ik = data.get("ik", {})
    rh = data.get("rehberlik", {})
    sg = data.get("saglik", {})
    bu = data.get("butce", {})
    tdm = data.get("tdm", {})
    se = data.get("sosyal", {})
    ds = data.get("destek", {})
    eu = data.get("erken_uyari", {})
    ku = data.get("kutuphane", {})
    dk = data.get("dijital_kutuphane", {})
    kul = data.get("kullanici", {})

    s_cnt = ak.get("students_aktif", 0)
    t_cnt = ak.get("teachers_count", 0)

    # Not ortalamasi
    puanlar = []
    for g in ak.get("grades", []):
        try:
            puanlar.append(float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)))
        except (TypeError, ValueError):
            pass
    genel_ort = round(sum(puanlar) / len(puanlar), 1) if puanlar else 0

    # Ozursuz devamsizlik
    ozursuz = sum(1 for a in ak.get("attendance", [])
                  if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
    dev_per_stu = round(ozursuz / max(s_cnt, 1), 2)

    # Kritik stok
    urunler = tdm.get("urunler", [])
    kritik = sum(1 for u in urunler
                 if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
                 and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0)
    kritik_pct = round(kritik / max(len(urunler), 1) * 100)

    # Modul kapsam
    active = sum(1 for vals in data.values()
                 if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0
                 or any(isinstance(v, (str, dict)) and v for v in vals.values()))
    kapsam = round(active / max(len(data), 1) * 100)

    # Not per ogrenci
    not_per_stu = round(len(puanlar) / max(s_cnt, 1), 1)

    gaps = [
        {
            "alan": "Akademik Basari",
            "ideal": "Not ortalamasi 75+, tum derslerde %60 ustu",
            "mevcut": f"Ortalama {genel_ort}, {len(puanlar)} not kaydi",
            "ideal_val": 75, "mevcut_val": genel_ort,
            "gap": round(75 - genel_ort, 1) if genel_ort < 75 else 0,
            "gap_pct": round(max(0, (75 - genel_ort) / 75 * 100), 1),
            "durum": "OK" if genel_ort >= 75 else ("RISK" if genel_ort < 60 else "GELISMELI"),
            "cozum": [
                "Dusuk basarili derslere haftalik etut programi baslatin",
                "Her ders icin en az 2 odev/hafta verin — odev basariyi %15-20 arttirir",
                "KYT ile haftalik kazanim yoklamasi yapin",
                "Zayif ogrencilere bireysel kocluk atayin (Egitim Koclugu modulu)",
            ],
            "timeline": "2-4 Hafta", "maliyet": "0 TL", "etki": 85,
            "icon": "📝", "color": "#2563eb",
        },
        {
            "alan": "Ogretmen/Ogrenci Dengesi",
            "ideal": "1 ogretmen : 12-15 ogrenci",
            "mevcut": f"1:{round(s_cnt/max(t_cnt,1),1)} ({t_cnt} ogretmen, {s_cnt} ogrenci)",
            "ideal_val": 15, "mevcut_val": round(s_cnt / max(t_cnt, 1), 1),
            "gap": max(0, round(s_cnt / max(t_cnt, 1), 1) - 15),
            "gap_pct": max(0, round((s_cnt / max(t_cnt, 1) - 15) / 15 * 100, 1)),
            "durum": "OK" if s_cnt / max(t_cnt, 1) <= 15 else "GELISMELI",
            "cozum": [
                "Mevcut oran ideal — bu dengeyi koruyun",
                "Sinif mevcutlarini 20'nin altinda tutun",
            ] if s_cnt / max(t_cnt, 1) <= 15 else [
                "Ek ogretmen kadrosu alin",
                "Sinif bolme yaparak mevcudu dusurun",
            ],
            "timeline": "Surekli", "maliyet": "0 TL" if s_cnt / max(t_cnt, 1) <= 15 else "Personel maliyeti",
            "etki": 70, "icon": "👨‍🏫", "color": "#7c3aed",
        },
        {
            "alan": "Devamsizlik Kontrolu",
            "ideal": "Ogrenci basina yillik max 3 gun ozursuz",
            "mevcut": f"Ogrenci basina {dev_per_stu} gun ozursuz ({ozursuz} toplam)",
            "ideal_val": 3, "mevcut_val": dev_per_stu,
            "gap": max(0, round(dev_per_stu - 3, 1)),
            "gap_pct": max(0, round((dev_per_stu - 3) / 3 * 100, 1)) if dev_per_stu > 3 else 0,
            "durum": "OK" if dev_per_stu <= 3 else ("RISK" if dev_per_stu > 10 else "GELISMELI"),
            "cozum": [
                "Devamsiz ogrenci velileriyle ayni gun iletisime gecin",
                "3 gun ozursuz sonrasi otomatik rehberlik yonlendirmesi",
                "Yoklama sistemi ile gunluk takip — akademik takipten",
                "Odul sistemi: tam devam yapan ogrencilere sertifika",
            ],
            "timeline": "Surekli", "maliyet": "0 TL", "etki": 75,
            "icon": "📋", "color": "#f59e0b",
        },
        {
            "alan": "IK & Personel Yonetimi",
            "ideal": f"Tum kadro ({max(t_cnt + 5, 15)}+ kisi) IK'ya kayitli, performans degerlendirme aktif",
            "mevcut": f"{ik.get('employees_aktif', 0)} personel kayitli, performans: {'Var' if ik.get('performance') else 'Yok'}",
            "ideal_val": max(t_cnt + 5, 15), "mevcut_val": ik.get("employees_aktif", 0),
            "gap": max(0, max(t_cnt + 5, 15) - ik.get("employees_aktif", 0)),
            "gap_pct": round(max(0, (max(t_cnt + 5, 15) - ik.get("employees_aktif", 0)) / max(t_cnt + 5, 15) * 100)),
            "durum": "RISK" if ik.get("employees_aktif", 0) < 5 else "GELISMELI",
            "cozum": [
                "IK > Kurum Aktif Calisanlar'dan tum personeli kaydedin",
                "Her personele pozisyon ve departman atamasi yapin",
                "Donem sonunda performans degerlendirme dongusu baslatin",
                "Izin yonetimini aktiflestirinz — yillik/mazeret/rapor",
                "Bordro modulu ile maas takibi yapin",
            ],
            "timeline": "1 Hafta (kayit) + 1 Ay (performans)", "maliyet": "0 TL",
            "etki": 80, "icon": "👥", "color": "#8b5cf6",
        },
        {
            "alan": "Mali Yonetim",
            "ideal": "Gelir >= Gider, butce takibi aktif, tum kalemler kayitli",
            "mevcut": f"Gelir: {bu.get('toplam_gelir', 0):,.0f} TL, Gider: {bu.get('toplam_gider', 0):,.0f} TL",
            "ideal_val": 100, "mevcut_val": round(bu.get("toplam_gelir", 0) / max(bu.get("toplam_gider", 0), 1) * 100),
            "gap": 100 - round(bu.get("toplam_gelir", 0) / max(bu.get("toplam_gider", 0), 1) * 100),
            "gap_pct": 100 if bu.get("toplam_gelir", 0) == 0 else max(0, 100 - round(bu.get("toplam_gelir", 0) / max(bu.get("toplam_gider", 0), 1) * 100)),
            "durum": "RISK" if bu.get("toplam_gelir", 0) == 0 else ("GELISMELI" if bu.get("toplam_gelir", 0) < bu.get("toplam_gider", 0) else "OK"),
            "cozum": [
                "Butce > Gelir Kayit'tan tum gelir kalemlerini girin (ogretim ucreti, bagis, etkinlik)",
                "Aylik gelir-gider mutabakati yapin",
                "Butce plani olusturup tahmini vs gerceklesen takibi yapin",
                "Gider kalemlerini analiz edin — tasarruf alanlari belirleyin",
            ],
            "timeline": "3 Gun (kayit) + Surekli (takip)", "maliyet": "0 TL",
            "etki": 90, "icon": "💰", "color": "#059669",
        },
        {
            "alan": "Stok Yonetimi",
            "ideal": "Kritik stok orani < %10, tum urunler min stok ustunde",
            "mevcut": f"{kritik}/{len(urunler)} urun kritik (%{kritik_pct})",
            "ideal_val": 10, "mevcut_val": kritik_pct,
            "gap": max(0, kritik_pct - 10),
            "gap_pct": max(0, kritik_pct - 10),
            "durum": "RISK" if kritik_pct > 50 else ("GELISMELI" if kritik_pct > 10 else "OK"),
            "cozum": [
                "TDM > Satin Alma'dan oncelikli urunler icin toplu siparis olusturun",
                "Min stok seviyelerini gozden gecirin — gerekirse dusururun",
                "Haftalik stok kontrol rutini olusturun",
                "Tedarikci sozlesmeleri ile otomatik yenileme sistemi kurun",
            ],
            "timeline": "1 Hafta (acil siparis) + 1 Ay (sistem)", "maliyet": "~21,770 TL (tahmini)",
            "etki": 85, "icon": "📦", "color": "#f97316",
        },
        {
            "alan": "Rehberlik & Psikolojik Destek",
            "ideal": f"Her sinifa donemde 2+ gorusme, risk ogrencilere BEP, vaka takibi",
            "mevcut": f"{_safe_len(rh.get('gorusmeler', []))} gorusme, {_safe_len(rh.get('vakalar', []))} vaka, {_safe_len(rh.get('bep', []))} BEP",
            "ideal_val": s_cnt, "mevcut_val": _safe_len(rh.get("gorusmeler", [])),
            "gap": max(0, 10 - _safe_len(rh.get("gorusmeler", []))),
            "gap_pct": 100 if not rh.get("gorusmeler") else 0,
            "durum": "RISK" if not rh.get("gorusmeler") else "GELISMELI",
            "cozum": [
                "Her sinif icin tanitim gorusmesi planlayin (2 hafta icinde)",
                "Erken Uyari'dan riskli ogrencileri rehberlige yonlendirin",
                "BEP ihtiyaci olan ogrencileri belirleyin",
                "Veli gorusmesi takvimi olusturun — donemde en az 2 kez",
                "Test ve envanter uygulamalari baslatin",
            ],
            "timeline": "2 Hafta (baslangic) + Surekli", "maliyet": "0 TL",
            "etki": 80, "icon": "📋", "color": "#10b981",
        },
        {
            "alan": "Guvenlik & Sivil Savunma",
            "ideal": "Yilda 2+ tatbikat, risk degerlendirme tamamlanmis, ISG egitimi",
            "mevcut": f"{_safe_len(data.get('ssg', {}).get('tatbikat', []))} tatbikat, "
                      f"{_safe_len(data.get('ssg', {}).get('riskler', []))} risk kaydi",
            "ideal_val": 2, "mevcut_val": _safe_len(data.get("ssg", {}).get("tatbikat", [])),
            "gap": max(0, 2 - _safe_len(data.get("ssg", {}).get("tatbikat", []))),
            "gap_pct": 100 if not data.get("ssg", {}).get("tatbikat") else 0,
            "durum": "RISK" if not data.get("ssg", {}).get("tatbikat") else "OK",
            "cozum": [
                "Deprem + yangin tahliye tatbikati planlayin (yasal zorunluluk)",
                "Risk degerlendirme tablosu olusturun",
                "ISG egitimi tum personele verin",
                "Acil durum iletisim agaci olusturun",
                "Ilk yardim dolaplari kontrolu yapin",
            ],
            "timeline": "1 Ay", "maliyet": "~500 TL",
            "etki": 95, "icon": "🚨", "color": "#ef4444",
        },
        {
            "alan": "Dijital Donusum",
            "ideal": "35 modulun %80+'i aktif, tum roller sistemi kullaniyor",
            "mevcut": f"{active}/{len(data)} modul aktif (%{kapsam})",
            "ideal_val": 80, "mevcut_val": kapsam,
            "gap": max(0, 80 - kapsam),
            "gap_pct": max(0, round((80 - kapsam) / 80 * 100)),
            "durum": "GELISMELI" if kapsam < 80 else "OK",
            "cozum": [
                "Her hafta 2 yeni modulu aktiflestirecek plan olusturun",
                "Hafta 1-2: IK + Butce | Hafta 3-4: Rehberlik + Saglik",
                "Hafta 5-6: Kutuphane + SSG | Hafta 7-8: CEFR + Kocluk",
                "Tum ogretmenlere sistem egitimi verin",
                "Ogrenci/veli kullanici hesaplarini aktiflestiirin",
            ],
            "timeline": "3 Ay", "maliyet": "0 TL",
            "etki": 70, "icon": "📊", "color": "#6366f1",
        },
        {
            "alan": "Sosyal Yasam & Zenginlestirme",
            "ideal": "5+ kulup, donemde 5+ etkinlik, AI Treni/Matematik/Sanat/Bilisim aktif",
            "mevcut": f"{_safe_len(se.get('kulupler', []))} kulup, {_safe_len(se.get('etkinlikler', []))} etkinlik",
            "ideal_val": 5, "mevcut_val": _safe_len(se.get("kulupler", [])),
            "gap": max(0, 5 - _safe_len(se.get("kulupler", []))),
            "gap_pct": max(0, round((5 - _safe_len(se.get("kulupler", []))) / 5 * 100)),
            "durum": "GELISMELI" if _safe_len(se.get("kulupler", [])) < 5 else "OK",
            "cozum": [
                "Spor, sanat, bilim, drama, muzik — 5 temel kulup acin",
                "Her kulube danisman ogretmen atayin",
                "Donemde en az 2 okul geneli etkinlik planlayin (gezi, yarısma)",
                "Matematik Koyu, Sanat Sokagi, Bilisim Vadisi'ni haftalik programa alin",
                "AI Treni ile eglenceli ogrenme seanslari duzenleyin",
            ],
            "timeline": "1 Ay", "maliyet": "~2,000 TL",
            "etki": 60, "icon": "🎭", "color": "#ec4899",
        },
        # ── Yabanci Dil Performansi ──
        {
            "alan": "Yabanci Dil Performansi",
            "ideal": "Quiz ortalamasi 70+, CEFR seviye tespiti yapilmis, unite bazli takip aktif",
            "mevcut": f"Quiz ort: {data.get('yd_sinav', {}).get('avg_score', 0)}, "
                      f"{data.get('yd_sinav', {}).get('total_results', 0)} sinav sonucu, "
                      f"{_safe_len(data.get('cefr', {}).get('results', []))} CEFR tespit",
            "ideal_val": 70,
            "mevcut_val": data.get("yd_sinav", {}).get("avg_score", 0),
            "gap": round(max(0, 70 - data.get("yd_sinav", {}).get("avg_score", 0)), 1),
            "gap_pct": round(max(0, (70 - data.get("yd_sinav", {}).get("avg_score", 0)) / 70 * 100), 1)
                      if data.get("yd_sinav", {}).get("avg_score", 0) < 70 else 0,
            "durum": "OK" if data.get("yd_sinav", {}).get("avg_score", 0) >= 70 else (
                "RISK" if data.get("yd_sinav", {}).get("avg_score", 0) < 50 else "GELISMELI"),
            "cozum": [
                "Her unite sonunda quiz uygulayarak surekliligi saglayin",
                "CEFR seviye tespit sinavini tum ogrencilere uygulatin",
                "Zayif unitelerde telafi quizleri olusturun",
                "Beceri bazli (vocabulary/grammar) eksikleri AI tavsiyelerle kapatın",
                "Unite bazli ilerleme haritasini veli panelinde paylasın",
            ],
            "timeline": "2 Ay", "maliyet": "~500 TL",
            "etki": 75, "icon": "🌍", "color": "#2563eb",
        },
    ]
    return gaps


def _generate_kurum_karnesi_pdf(data: dict, gaps: list[dict]) -> bytes | None:
    """Kurum Karnesi — tek sayfada tum skorlar, gap ozeti, endeks. A4 kurumsal format."""
    try:
        import io as _io
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from utils.shared_data import ensure_turkish_pdf_fonts

        fn, fb = ensure_turkish_pdf_fonts()
        buf = _io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.2*cm, bottomMargin=1.5*cm,
                                leftMargin=1.5*cm, rightMargin=1.5*cm)
        pw = A4[0] - 3*cm
        els = []

        def _t(text):
            return str(text) if fn != "Helvetica" else str(text).translate(
                str.maketrans("ıİğĞüÜşŞöÖçÇ", "iIgGuUsSoOcC"))

        s_title = ParagraphStyle("KT", fontName=fb, fontSize=18, leading=22,
                                  alignment=1, textColor=rl.HexColor("#1e1b4b"), spaceAfter=4)
        s_sub = ParagraphStyle("KS", fontName=fn, fontSize=9, leading=12,
                                alignment=1, textColor=rl.HexColor("#64748b"), spaceAfter=10)
        s_h2 = ParagraphStyle("KH2", fontName=fb, fontSize=11, leading=14,
                               textColor=rl.HexColor("#1e1b4b"), spaceBefore=8, spaceAfter=4)
        s_body = ParagraphStyle("KB", fontName=fn, fontSize=8, leading=11, spaceAfter=2)
        s_small = ParagraphStyle("KSm", fontName=fn, fontSize=7, leading=9, textColor=rl.HexColor("#64748b"))

        hdr_s = ParagraphStyle("KHdr", fontName=fb, fontSize=7.5, leading=10,
                                textColor=rl.white, alignment=1)
        cell_s = ParagraphStyle("KCell", fontName=fn, fontSize=7.5, leading=10, alignment=1)

        # Kurum adi
        kurum = data.get("koi", {}).get("kurum_adi", "SmartCampus AI")
        inst = _compute_institution_score(data)
        idx = _institution_index(data)

        els.append(Paragraph(_t(f"{kurum}"), s_title))
        els.append(Paragraph(_t("Kurum Karnesi"), ParagraphStyle(
            "KCover", fontName=fb, fontSize=13, leading=16, alignment=1,
            textColor=rl.HexColor("#6366f1"), spaceAfter=6)))
        els.append(Paragraph(_t(f"Tarih: {time.strftime('%d.%m.%Y')} | "
                                f"Kurum Skoru: %{inst['overall']:.0f} | "
                                f"Endeks: {idx['index']}/1000"), s_sub))

        # Skor tablosu — 7 boyut
        score_data = [[Paragraph(_t("<b>Boyut</b>"), hdr_s), Paragraph(_t("<b>Skor</b>"), hdr_s),
                        Paragraph(_t("<b>Durum</b>"), hdr_s)]]
        for dim, val in inst["scores"].items():
            durum = "Iyi" if val >= 70 else ("Orta" if val >= 40 else "Dusuk")
            score_data.append([Paragraph(_t(dim), cell_s), Paragraph(_t(f"%{val:.0f}"), cell_s),
                               Paragraph(_t(durum), cell_s)])
        tbl = Table(score_data, colWidths=[pw*0.5, pw*0.25, pw*0.25])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#1e1b4b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, rl.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("FONTNAME", (0, 1), (-1, -1), fn), ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ]))
        els.append(tbl)
        els.append(Spacer(1, 0.3*cm))

        # Gap tablosu
        els.append(Paragraph(_t("Gap Analizi — Olmasi Gereken vs Mevcut"), s_h2))
        gap_data = [[Paragraph(_t("<b>Alan</b>"), hdr_s), Paragraph(_t("<b>Durum</b>"), hdr_s),
                      Paragraph(_t("<b>Gap %</b>"), hdr_s), Paragraph(_t("<b>Etki</b>"), hdr_s),
                      Paragraph(_t("<b>Cozum</b>"), hdr_s)]]
        for g in sorted(gaps, key=lambda x: -x["gap_pct"]):
            gap_data.append([
                Paragraph(_t(g["alan"]), cell_s),
                Paragraph(_t(g["durum"]), cell_s),
                Paragraph(_t(f"%{g['gap_pct']:.0f}"), cell_s),
                Paragraph(_t(f"%{g['etki']}"), cell_s),
                Paragraph(_t(g["cozum"][0][:50] + "..." if g["cozum"] else "-"),
                           ParagraphStyle("KCellS", fontName=fn, fontSize=6.5, leading=8, alignment=0)),
            ])
        gap_tbl = Table(gap_data, colWidths=[pw*0.2, pw*0.12, pw*0.1, pw*0.1, pw*0.48])
        gap_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#312e81")),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (-1, 1), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.3, rl.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("FONTNAME", (0, 1), (-1, -1), fn), ("FONTSIZE", (0, 1), (-1, -1), 7),
        ]))
        els.append(gap_tbl)
        els.append(Spacer(1, 0.3*cm))

        # Projeksiyon
        proj = _projection_model(data)
        els.append(Paragraph(_t("3 Ay Projeksiyon"), s_h2))
        els.append(Paragraph(_t(
            f"Mevcut: %{proj['current']['score']:.0f} (Endeks {proj['current']['index']}) | "
            f"Temel Aksiyon: %{proj['base']['score']:.0f} ({proj['base']['index']}) | "
            f"Tam Plan: %{proj['full']['score']:.0f} ({proj['full']['index']})"), s_body))

        # Oncelikli 5 aksiyon
        els.append(Spacer(1, 0.2*cm))
        els.append(Paragraph(_t("Oncelikli 5 Aksiyon"), s_h2))
        analysis = _deep_rule_analysis(data)
        for i, (pri, tf, title, detail) in enumerate(analysis["roadmap"][:5]):
            els.append(Paragraph(_t(f"{i+1}. [{pri}] {title} ({tf}) — {detail}"), s_small))

        # Footer
        els.append(Spacer(1, 0.3*cm))
        els.append(Paragraph(_t(f"SmartCampus AI — Kurum Karnesi | {time.strftime('%d.%m.%Y %H:%M')}"),
                              ParagraphStyle("KFoot", fontName=fn, fontSize=6, leading=8,
                                             alignment=1, textColor=rl.HexColor("#94a3b8"))))

        doc.build(els)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"Karne PDF hatasi: {e}")
        return None


def _kurum_rontgeni(data: dict) -> dict:
    """19 motorun ciktisini birlestiren mega analiz — tek bakista kurum durumu.
    Her motor sonucunu toplar, cross-reference yapar, tek skor uretir."""
    inst = _compute_institution_score(data)
    idx = _institution_index(data)
    gaps = _gap_analysis(data)
    analysis = _deep_rule_analysis(data)
    anomalies = _anomaly_detection(data)
    segments = _student_segmentation(data)
    proj = _projection_model(data)
    tracker = _goal_tracker(data)
    cb = _cost_benefit_analysis(data)
    tch_eff = _teacher_effectiveness(data)
    mod_act = _module_activity_score(data)
    stok = _stock_value_analysis(data)
    tch_work = _teacher_workload(data)

    # Hesaplamalar
    gap_ok = sum(1 for g in gaps if g["durum"] == "OK")
    gap_risk = sum(1 for g in gaps if g["durum"] == "RISK")
    hedef_tuttu = sum(1 for g in tracker["goals"]
                      if (not g.get("reverse") and g["actual"] >= g["target"])
                      or (g.get("reverse") and g["actual"] <= g["target"]))
    anomali_kritik = sum(1 for a in anomalies if a.get("type") == "critical")
    pasif_ogretmen = sum(1 for t in tch_work if t["durum"] == "Pasif") if tch_work else 0
    aktif_modul = sum(1 for m in mod_act if m["seviye"] != "Pasif")
    toplam_maliyet = sum(i["maliyet"] for i in cb)
    yildiz_stu = len(segments.get("yildiz", []))
    risk_stu = len(segments.get("risk", []))

    # Mega skor — tum motorlarin agirliklı ortalaması
    mega = round((
        inst["overall"] * 0.15 +
        (idx["index"] / 10) * 0.15 +
        (gap_ok / max(len(gaps), 1) * 100) * 0.15 +
        (hedef_tuttu / max(len(tracker["goals"]), 1) * 100) * 0.10 +
        (100 - anomali_kritik * 15) * 0.10 +
        proj["full"]["score"] * 0.10 +
        (aktif_modul / max(len(mod_act), 1) * 100) * 0.10 +
        (100 - pasif_ogretmen / max(len(tch_work), 1) * 100 if tch_work else 50) * 0.05 +
        (100 - risk_stu / max(sum(len(v) for v in segments.values()), 1) * 100) * 0.10
    ), 1)

    return {
        "mega_skor": min(100, max(0, mega)),
        "kurum_skoru": inst["overall"],
        "endeks": idx["index"],
        "gap_ok": gap_ok, "gap_risk": gap_risk, "gap_total": len(gaps),
        "hedef_tuttu": hedef_tuttu, "hedef_total": len(tracker["goals"]),
        "bulgu": len(analysis["findings"]), "roadmap": len(analysis["roadmap"]),
        "anomali": len(anomalies), "anomali_kritik": anomali_kritik,
        "segment_yildiz": yildiz_stu, "segment_risk": risk_stu,
        "projeksiyon_tam": proj["full"]["score"],
        "aktif_modul": aktif_modul, "toplam_modul": len(mod_act),
        "pasif_ogretmen": pasif_ogretmen, "toplam_ogretmen": len(tch_work) if tch_work else 0,
        "stok_deger": stok["toplam_deger"], "stok_kritik": stok["kritik_deger"],
        "aksiyon_maliyet": toplam_maliyet,
        "cross_insights": analysis.get("cross_insights", []),
    }


def _kurum_dna(data: dict) -> dict:
    """Kurum DNA Profili — kurumun genetik haritasi.
    Guclu genler (ustun alanlar) + Zayif genler (risk alanlari) + Mutasyon (degisim potansiyeli)."""
    inst = _compute_institution_score(data)
    gaps = _gap_analysis(data)
    idx = _institution_index(data)

    # Guclu genler — %70 ustu alanlar
    guclu = []
    for dim, val in inst["scores"].items():
        if val >= 70:
            guclu.append({"gen": dim, "skor": val, "aciklama": f"{dim} alani guclu — %{val:.0f} skor"})
    for dim, val in idx["dims"].items():
        if val >= 70 and not any(g["gen"] == dim for g in guclu):
            guclu.append({"gen": dim, "skor": val, "aciklama": f"{dim} endekste ustun"})

    # Zayif genler — %30 alti
    zayif = []
    for dim, val in inst["scores"].items():
        if val < 30:
            zayif.append({"gen": dim, "skor": val, "aciklama": f"{dim} kritik dusuk — acil mudahale"})
    for dim, val in idx["dims"].items():
        if val < 30 and not any(z["gen"] == dim for z in zayif):
            zayif.append({"gen": dim, "skor": val, "aciklama": f"{dim} endekste zayif"})

    # Mutasyon potansiyeli — gap'leri kapatma ile kazanilacak skor
    proj = _projection_model(data)
    mutasyon = round(proj["full"]["score"] - proj["current"]["score"], 1)

    # Kurum karakteri — en guclu 3 gen
    if guclu:
        karakter_genleri = sorted(guclu, key=lambda x: -x["skor"])[:3]
        karakter = " + ".join(g["gen"] for g in karakter_genleri)
    else:
        karakter = "Henuz belirlenmedi"

    return {
        "guclu": guclu, "zayif": zayif,
        "mutasyon": mutasyon, "karakter": karakter,
        "guclu_cnt": len(guclu), "zayif_cnt": len(zayif),
    }


def _smart_daily_recommendations(data: dict, role: str) -> list[dict]:
    """Her role her gun farkli 3 oneri — veriye dayali, baglama duyarli."""
    from datetime import datetime
    day = datetime.now().weekday()  # 0=Pzt, 4=Cuma
    recs = []

    ak = data.get("akademik", {})
    s_cnt = ak.get("students_aktif", 0)
    grades = ak.get("grades", [])
    eu = data.get("erken_uyari", {})

    if role in ("Yonetici", "SuperAdmin"):
        # Gune gore degisen oneriler
        day_recs = [
            [  # Pazartesi
                {"icon": "📊", "title": "Haftalik performans kontrolu", "detail": "Gecen haftanin KPI'larini inceleyin, gap'leri kontrol edin", "modul": "AI Destek"},
                {"icon": "👥", "title": "Ogretmen toplantisi planla", "detail": "Haftalik hedefleri belirleyin, gecen haftayi degerlendirin", "modul": "Toplanti Kurullar"},
                {"icon": "💰", "title": "Mali durum kontrolu", "detail": "Haftalik gelir-gider kontrolu, odenmemis faturalar", "modul": "Butce Gelir Gider"},
            ],
            [  # Sali
                {"icon": "📋", "title": "Devamsizlik raporu incele", "detail": "Dunden bugunun devamsizlik kaydini kontrol edin", "modul": "Akademik Takip"},
                {"icon": "🔧", "title": "Destek taleplerini kontrol et", "detail": "Acik talepleri inceleyin, atama yapin", "modul": "Destek Hizmetleri"},
                {"icon": "📞", "title": "Oncelikli veli aramalari", "detail": "Risk grubu ogrenci velileriyle iletisim", "modul": "KOI Iletisim"},
            ],
            [  # Carsamba
                {"icon": "🎯", "title": "Hedef takip kontrolu", "detail": "10 kurum hedefinden hangisi geride?", "modul": "AI Destek"},
                {"icon": "📦", "title": "Stok durumu kontrolu", "detail": "Kritik stok uyarilarini inceleyin", "modul": "Tuketim Demirbas"},
                {"icon": "🏥", "title": "Saglik raporlari", "detail": "Haftalik revir ziyaret ozeti", "modul": "Okul Sagligi"},
            ],
            [  # Persembe
                {"icon": "🤖", "title": "AI kurum analizi calistir", "detail": "18 modul verisiyle kapsamli rapor uret", "modul": "AI Destek"},
                {"icon": "📅", "title": "Gelecek hafta planlama", "detail": "Toplanti, etkinlik, sinav takvimini kontrol edin", "modul": "Akademik Takvim"},
                {"icon": "🎭", "title": "Sosyal etkinlik kontrolu", "detail": "Kulup faaliyetleri ve planlanan etkinlikler", "modul": "Sosyal Etkinlik"},
            ],
            [  # Cuma
                {"icon": "📈", "title": "Haftalik degerlendirme", "detail": "Kurum rontgenini inceleyin, mega skoru kontrol edin", "modul": "AI Destek"},
                {"icon": "📄", "title": "Kurum karnesi PDF olustur", "detail": "Haftalik raporu indirip arsivleyin", "modul": "AI Destek"},
                {"icon": "🚀", "title": "Gelecek hafta icin 3 oncelik belirle", "detail": "Gap analizinden en kritik 3 aksiyonu secin", "modul": "AI Destek"},
            ],
        ]
        recs = day_recs[day] if day < 5 else day_recs[4]  # haftasonu = cuma tekrar

    elif role == "Öğretmen":
        base = [
            {"icon": "📝", "title": "Bugunun yoklamasini gir", "detail": "Akademik Takip > Yoklama sekmesinden", "modul": "Akademik Takip"},
            {"icon": "📊", "title": "KYT kazanim yoklamasi", "detail": "Bu haftanin kazanimlarini test et", "modul": "Akademik Takip > KYT"},
        ]
        if day == 0:  # Pazartesi
            base.append({"icon": "📓", "title": "Bu hafta odevlerini planla", "detail": "Odev modulunden yeni odev olustur", "modul": "Akademik Takip > Odev"})
        elif day == 2:  # Carsamba
            base.append({"icon": "🌍", "title": "Ingilizce ders isleme", "detail": "Yabanci Dil > Ders Isleme Motorunu kullan", "modul": "Yabanci Dil"})
        elif day == 4:  # Cuma
            base.append({"icon": "📈", "title": "Haftalik ogrenci ilerleme", "detail": "AI Destek'ten sinif analizini kontrol et", "modul": "AI Destek"})
        else:
            base.append({"icon": "📖", "title": "Ders defteri guncelle", "detail": "Bugun islenen konulari kaydet", "modul": "Akademik Takip > Ders Defteri"})
        recs = base

    elif role == "Veli":
        recs = [
            {"icon": "📊", "title": "Cocugunuzun durumunu kontrol edin", "detail": "AI Destek'ten akademik raporu inceleyin", "modul": "AI Destek"},
            {"icon": "📖", "title": "Birlikte 30dk kitap okuyun", "detail": "Okuma aliskanligi basariyi %20 arttirir", "modul": "Dijital Kutuphane"},
            {"icon": "🌍", "title": "15dk Ingilizce pratik yaptirin", "detail": "Yabanci Dil > SRS Kelime Tekrar", "modul": "Yabanci Dil"},
        ]

    elif role in ("Öğrenci", "Ogrenci"):
        if day < 5:  # haftaici
            recs = [
                {"icon": "📝", "title": "Odevlerini kontrol et", "detail": "Teslim tarihi yaklasan odevler var mi?", "modul": "Ogrenci Paneli"},
                {"icon": "📖", "title": "30dk kitap oku", "detail": "Gunun okuma hedefini tamamla", "modul": "Okuma Kutuphanesi"},
                {"icon": ["🧮", "💻", "🎨", "🌍", "🚂"][day], "title": ["Matematik Koyu", "Bilisim Vadisi", "Sanat Sokagi", "Ingilizce", "AI Treni"][day],
                 "detail": "Bugunku zenginlestirme aktiviteni tamamla!", "modul": ["Matematik Koyu", "Bilisim Vadisi", "Sanat Sokagi", "Yabanci Dil", "AI Treni"][day]},
            ]
        else:
            recs = [
                {"icon": "📖", "title": "Hafta sonu okuma zamani", "detail": "Bir kitap bitir — hayaller kur!", "modul": "Dijital Kutuphane"},
                {"icon": "📝", "title": "Pazartesi odevlerini simdiden yap", "detail": "Erken bitir, ozgurce oyna!", "modul": "Ogrenci Paneli"},
                {"icon": "🎯", "title": "Hedeflerini gozden gecir", "detail": "Bu hafta ne basardin? Gelecek hafta ne hedefliyorsun?", "modul": "AI Destek"},
            ]

    return recs


def _render_daily_recommendations(recs: list[dict]):
    """Gunluk onerileri premium kartlarla render et."""
    if not recs:
        return
    from datetime import datetime
    gun_adi = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"][datetime.now().weekday()]

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border-radius:14px;
    padding:14px 18px;margin:8px 0;border:1px solid rgba(99,102,241,0.2);">
    <div style="font-size:.85rem;font-weight:700;color:#818cf8;margin-bottom:8px;">
    📅 {gun_adi} — Bugunun 3 Onceligi</div>""", unsafe_allow_html=True)

    for i, r in enumerate(recs[:3]):
        st.markdown(f"""
    <div style="display:flex;gap:10px;align-items:center;padding:6px 0;
    {'border-top:1px solid #1e293b;' if i > 0 else ''}">
    <span style="font-size:1.5rem;">{r['icon']}</span>
    <div style="flex:1;">
    <div style="color:#e2e8f0;font-weight:600;font-size:.88rem;">{r['title']}</div>
    <div style="color:#94a3b8;font-size:.75rem;">{r['detail']}</div>
    </div>
    <span style="font-size:.65rem;color:#475569;background:#1e293b;padding:2px 6px;
    border-radius:4px;">{r['modul']}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _ai_kurumsal_vizyon(client, data: dict) -> str | None:
    """AI Kurumsal Vizyon — GPT'ye tum veriyi ver, 5 yillik stratejik vizyon yazdır.
    Sadece analiz degil — HAYAL KURDURAN, ilham veren, somut ama cesur bir gelecek resmi."""
    cache_key = "_ai_vizyon"
    if cache_key in st.session_state:
        return st.session_state[cache_key]
    if not client:
        return None
    try:
        rontgen = _kurum_rontgeni(data)
        dna = _kurum_dna(data)
        gaps = _gap_analysis(data)
        idx = _institution_index(data)
        proj = _projection_model(data)

        gap_ozet = "\n".join(f"- {g['alan']}: {g['durum']} (gap %{g['gap_pct']})" for g in gaps)
        dna_ozet = f"Guclu: {', '.join(g['gen'] for g in dna['guclu'][:3])}. Zayif: {', '.join(z['gen'] for z in dna['zayif'][:3])}"

        prompt = f"""Sen Turkiye'nin en vizyoner egitim danismanisin. Asagidaki kurum verisine bakarak
5 YILLIK STRATEJIK VIZYON yaz. Bu bir rapor degil — bir ILHAM KAYNAGI.

KURUM VERISI:
- Mega Skor: {rontgen['mega_skor']}/100
- Endeks: {idx['index']}/1000 (Derece: {'A+' if idx['index']>=800 else 'A' if idx['index']>=650 else 'B' if idx['index']>=500 else 'C'})
- {data.get('akademik',{}).get('students_aktif',0)} ogrenci, {data.get('akademik',{}).get('teachers_count',0)} ogretmen
- DNA: {dna_ozet}
- Mutasyon Potansiyeli: %{dna['mutasyon']}
- Projeksiyon: Mevcut %{proj['current']['score']} → Tam aksiyon %{proj['full']['score']}
- Gap Ozeti:
{gap_ozet}

YAZIM KURALLARI:
1. "5 Yillik Vizyon" basligi ile basla
2. Her yil icin 1 paragraf yaz (2025-2030)
3. Her yilda somut, olculebilir, cesur ama ulasilabilir hedefler koy
4. Kurumun guclu genlerini (DNA) kaldırac olarak kullan
5. Zayif genleri firsat olarak goster — "bunu dusunun: ..." diyerek
6. Son paragrafta 2030'da kurumun nasil gorunecegini CANLANDIR — ogrenci, ogretmen, veli gozunden
7. Duygusal, motive edici, profesyonel ama CESUR yaz
8. Emoji kullan ama abartma
9. Turkce yaz, 400-500 kelime"""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Turkiye'nin en vizyoner egitim stratejisti. Cesur, ilham verici, somut."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500, temperature=0.85,
        )
        text = resp.choices[0].message.content or ""
        st.session_state[cache_key] = text
        return text
    except Exception:
        return None


def _render_kurum_rontgeni(rontgen: dict):
    """Kurum rontgenini ultra premium render — tek bakista her sey."""
    mega = rontgen["mega_skor"]
    if mega >= 75: grade, color, emoji = "A", "#22c55e", "🏆"
    elif mega >= 55: grade, color, emoji = "B", "#10b981", "✅"
    elif mega >= 35: grade, color, emoji = "C", "#f59e0b", "⚡"
    else: grade, color, emoji = "D", "#ef4444", "🔴"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 30%,#312e81 60%,#4c1d95 100%);
    border-radius:20px;padding:28px 32px;margin:16px 0;
    border:2px solid {color}40;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-60px;right:-60px;width:200px;height:200px;
    background:radial-gradient(circle,{color}08,transparent);border-radius:50%;"></div>
    <div style="text-align:center;">
    <div style="font-size:.8rem;color:#818cf8;letter-spacing:2px;text-transform:uppercase;
    font-weight:700;">SmartCampus AI — Kurum Rontgeni</div>
    <div style="font-size:4rem;font-weight:900;color:{color};margin:8px 0;
    text-shadow:0 0 30px {color}30;">{emoji} {mega:.0f}</div>
    <div style="font-size:1.2rem;color:{color};font-weight:700;">Mega Skor: Derece {grade}</div>
    <div style="font-size:.78rem;color:#64748b;margin-top:4px;">
    19 analiz motorunun agirlikli bilesik skoru (0-100)</div>
    </div></div>""", unsafe_allow_html=True)

    # 4x3 grid — tum metrikleri tek bakista
    st.markdown("""<style>
    .rg-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0;}
    .rg-card{background:#0f172a;border-radius:10px;padding:12px;text-align:center;
    border:1px solid rgba(99,102,241,0.15);}
    .rg-val{font-size:1.4rem;font-weight:900;margin:4px 0;}
    .rg-label{font-size:.65rem;color:#64748b;text-transform:uppercase;letter-spacing:.3px;}
    </style>""", unsafe_allow_html=True)

    cards = [
        (f"%{rontgen['kurum_skoru']:.0f}", "Kurum Skoru", "#6366f1"),
        (f"{rontgen['endeks']}", "Endeks/1000", "#8b5cf6"),
        (f"{rontgen['gap_ok']}/{rontgen['gap_total']}", "Gap Hedefte", "#22c55e"),
        (f"{rontgen['hedef_tuttu']}/{rontgen['hedef_total']}", "Hedef Tuttu", "#10b981"),
        (f"{rontgen['bulgu']}", "Bulgu", "#f59e0b"),
        (f"{rontgen['anomali']}", "Anomali", "#ef4444" if rontgen["anomali_kritik"] > 0 else "#f59e0b"),
        (f"{rontgen['segment_yildiz']}", "Yildiz Ogrenci", "#6366f1"),
        (f"%{rontgen['projeksiyon_tam']:.0f}", "Tam Aksiyon Proj.", "#22c55e"),
        (f"{rontgen['aktif_modul']}/{rontgen['toplam_modul']}", "Aktif Modul", "#0d9488"),
        (f"{rontgen['pasif_ogretmen']}", "Pasif Ogretmen", "#ef4444" if rontgen["pasif_ogretmen"] > 3 else "#22c55e"),
        (f"{rontgen['stok_deger']:,.0f}", "Stok Deger TL", "#f59e0b"),
        (f"{rontgen['aksiyon_maliyet']:,.0f}", "Aksiyon Maliyet TL", "#ef4444"),
    ]

    html = '<div class="rg-grid">'
    for val, label, clr in cards:
        html += (f'<div class="rg-card"><div class="rg-val" style="color:{clr};">{val}</div>'
                 f'<div class="rg-label">{label}</div></div>')
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_gap_analysis(gaps: list[dict], prefix: str = "t1"):
    """Gap analizini ultra premium gorsel olarak render et."""
    if not gaps:
        return

    # Genel skor
    ok_cnt = sum(1 for g in gaps if g["durum"] == "OK")
    risk_cnt = sum(1 for g in gaps if g["durum"] == "RISK")
    gel_cnt = sum(1 for g in gaps if g["durum"] == "GELISMELI")
    ort_etki = round(sum(g["etki"] for g in gaps) / len(gaps))

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);border-radius:16px;
    padding:20px 24px;margin:12px 0;border:1.5px solid rgba(99,102,241,0.3);">
    <div style="font-size:1.1rem;font-weight:900;color:#c7d2fe;margin-bottom:12px;">
    Olmasi Gereken vs Mevcut Durum — {len(gaps)} Boyutlu Gap Analizi</div>
    <div style="display:flex;justify-content:space-around;text-align:center;">
    <div><div style="font-size:2rem;font-weight:900;color:#22c55e;">{ok_cnt}</div>
    <div style="font-size:.7rem;color:#64748b;">Hedefte</div></div>
    <div><div style="font-size:2rem;font-weight:900;color:#f59e0b;">{gel_cnt}</div>
    <div style="font-size:.7rem;color:#64748b;">Gelismeli</div></div>
    <div><div style="font-size:2rem;font-weight:900;color:#ef4444;">{risk_cnt}</div>
    <div style="font-size:.7rem;color:#64748b;">Risk</div></div>
    <div><div style="font-size:2rem;font-weight:900;color:#6366f1;">%{ort_etki}</div>
    <div style="font-size:.7rem;color:#64748b;">Ort Etki</div></div>
    </div></div>""", unsafe_allow_html=True)

    # Gap donut
    _donut(["Hedefte", "Gelismeli", "Risk"], [ok_cnt, gel_cnt, risk_cnt],
           ["#22c55e", "#f59e0b", "#ef4444"],
           center=f"<b>{len(gaps)}</b><br><span style='font-size:10px;color:#64748b'>Boyut</span>")

    # Her gap detay
    for g in sorted(gaps, key=lambda x: -x["gap_pct"]):
        durum_clr = {"OK": "#22c55e", "GELISMELI": "#f59e0b", "RISK": "#ef4444"}.get(g["durum"], "#64748b")
        durum_emoji = {"OK": "✅", "GELISMELI": "⚡", "RISK": "🔴"}.get(g["durum"], "⚪")
        fill = min(100, max(5, 100 - g["gap_pct"])) if g["gap_pct"] > 0 else 100

        with st.expander(f"{g['icon']} {g['alan']} — {durum_emoji} {g['durum']} | Gap: %{g['gap_pct']}", expanded=(g["durum"] == "RISK")):
            # Ideal vs Mevcut yan yana
            ic1, ic2 = st.columns(2)
            with ic1:
                st.markdown(f"""<div style="background:#052e16;border:1px solid #22c55e40;
                border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:.7rem;color:#86efac;text-transform:uppercase;">Olmasi Gereken</div>
                <div style="color:#e2e8f0;font-size:.85rem;margin-top:6px;">{g['ideal']}</div>
                </div>""", unsafe_allow_html=True)
            with ic2:
                st.markdown(f"""<div style="background:#1c0505;border:1px solid {durum_clr}40;
                border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:.7rem;color:{durum_clr};text-transform:uppercase;">Mevcut Durum</div>
                <div style="color:#e2e8f0;font-size:.85rem;margin-top:6px;">{g['mevcut']}</div>
                </div>""", unsafe_allow_html=True)

            # Gap bar
            st.markdown(f"""<div style="margin:8px 0;">
            <div style="display:flex;justify-content:space-between;font-size:.75rem;color:#94a3b8;">
            <span>Gap: %{g['gap_pct']}</span><span>Gerceklesme: %{100-g['gap_pct']:.0f}</span></div>
            <div style="background:#1e293b;border-radius:6px;height:10px;overflow:hidden;margin-top:4px;">
            <div style="width:{fill}%;height:100%;background:linear-gradient(90deg,{durum_clr},{g['color']});
            border-radius:6px;"></div></div></div>""", unsafe_allow_html=True)

            # Cozumler
            st.markdown(f"**Kapatma Stratejisi:** ({g['timeline']} | {g['maliyet']} | Etki: %{g['etki']})")
            for i, c in enumerate(g["cozum"]):
                st.markdown(f"""<div style="display:flex;gap:8px;padding:3px 0;">
                <span style="color:{g['color']};font-weight:700;min-width:20px;">{i+1}.</span>
                <span style="color:#cbd5e1;font-size:.85rem;">{c}</span></div>""", unsafe_allow_html=True)

            # Aksiyon butonu — ilgili modüle yonlendir
            modul_map = {
                "Akademik Basari": "Akademik Takip",
                "Ogretmen/Ogrenci Dengesi": "Insan Kaynaklari Yonetimi",
                "Devamsizlik Kontrolu": "Akademik Takip",
                "IK & Personel Yonetimi": "Insan Kaynaklari Yonetimi",
                "Mali Yonetim": "Butce Gelir Gider",
                "Stok Yonetimi": "Tuketim ve Demirbas",
                "Rehberlik & Psikolojik Destek": "Rehberlik",
                "Guvenlik & Sivil Savunma": "Sivil Savunma ve IS Guvenligi",
                "Dijital Donusum": "Ana Sayfa",
                "Sosyal Yasam & Zenginlestirme": "Sosyal Etkinlik ve Kulupler",
            }
            target_mod = modul_map.get(g["alan"], "")
            bc1, bc2 = st.columns(2)
            with bc1:
                if target_mod and g["durum"] != "OK":
                    if st.button(f"🚀 {target_mod} Modulune Git", key=f"gap_go_{prefix}_{g['alan'][:10]}",
                                   use_container_width=True, type="primary"):
                        st.session_state["_sidebar_secim"] = target_mod
                        st.rerun()
            with bc2:
                # AI ozel gap raporu
                ai_gap_key = f"_ai_gap_{g['alan'][:10]}"
                if st.button(f"🤖 AI Detay Rapor", key=f"gap_ai_{prefix}_{g['alan'][:10]}",
                               use_container_width=True):
                    try:
                        client = _get_client()
                        if client:
                            with st.spinner("AI gap raporu olusturuluyor..."):
                                resp = client.chat.completions.create(
                                    model="gpt-4o-mini",
                                    messages=[
                                        {"role": "system", "content": "Turkce. Egitim kurumu yonetim danismani. "
                                         "Verilen gap icin detayli analiz + 5 adimli aksiyon plani yaz."},
                                        {"role": "user", "content": f"Gap: {g['alan']}\n"
                                         f"Ideal: {g['ideal']}\nMevcut: {g['mevcut']}\n"
                                         f"Gap: %{g['gap_pct']}\nMaliyet: {g['maliyet']}\n"
                                         f"Mevcut cozumler: {'; '.join(g['cozum'])}"},
                                    ],
                                    max_tokens=500, temperature=0.7,
                                )
                                st.session_state[ai_gap_key] = resp.choices[0].message.content or ""
                                st.rerun()
                    except Exception:
                        pass
                if st.session_state.get(ai_gap_key):
                    st.markdown(st.session_state[ai_gap_key])


def _subject_correlation(data: dict) -> list[dict]:
    """Ders-ders korelasyon analizi — bir ogrencinin dersleri arasindaki iliski.
    Orn: Matematik iyi olan Fen de iyi mi?"""
    grades = data.get("akademik", {}).get("grades", [])
    if not grades:
        return []
    stu_ders: dict[str, dict[str, float]] = {}
    for g in grades:
        sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
        ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        try:
            stu_ders.setdefault(sid, {})[ders] = float(puan)
        except (TypeError, ValueError):
            pass

    # En az 2 dersi olan ogrenciler
    multi = {sid: dersler for sid, dersler in stu_ders.items() if len(dersler) >= 2}
    if not multi:
        return []

    # Her ders cifti icin korelasyon
    all_dersler = sorted(set(d for dersler in multi.values() for d in dersler))
    correlations = []
    for i, d1 in enumerate(all_dersler):
        for d2 in all_dersler[i+1:]:
            pairs = [(dersler[d1], dersler[d2]) for dersler in multi.values()
                     if d1 in dersler and d2 in dersler]
            if len(pairs) >= 1:
                avg_d1 = sum(p[0] for p in pairs) / len(pairs)
                avg_d2 = sum(p[1] for p in pairs) / len(pairs)
                diff = abs(avg_d1 - avg_d2)
                direction = "pozitif" if avg_d1 > 50 and avg_d2 > 50 else ("negatif" if diff > 20 else "notr")
                correlations.append({
                    "ders1": d1, "ders2": d2,
                    "ort1": round(avg_d1, 1), "ort2": round(avg_d2, 1),
                    "fark": round(diff, 1), "ornek": len(pairs),
                    "direction": direction,
                })
    return sorted(correlations, key=lambda x: -x["fark"])


def _stock_value_analysis(data: dict) -> dict:
    """Stok deger analizi — urun bazli maliyet, kategori dagilimi, kritik maliyet."""
    urunler = data.get("tdm", {}).get("urunler", [])
    if not urunler:
        return {"toplam_deger": 0, "kritik_deger": 0, "kategori": {}, "en_pahali": []}

    toplam_deger = 0
    kritik_deger = 0
    kategori_deger: dict[str, float] = {}
    urun_deger = []

    for u in urunler:
        stok = u.get("stok", 0) if isinstance(u.get("stok"), (int, float)) else 0
        fiyat = u.get("birim_fiyat", 0) if isinstance(u.get("birim_fiyat"), (int, float)) else 0
        min_stok = u.get("min_stok", 0) if isinstance(u.get("min_stok"), (int, float)) else 0
        kat = u.get("kategori", "Diger")
        deger = stok * fiyat
        toplam_deger += deger

        kategori_deger[kat] = kategori_deger.get(kat, 0) + deger

        if stok < min_stok and min_stok > 0:
            eksik = (min_stok - stok) * fiyat
            kritik_deger += eksik

        urun_deger.append({"urun": u.get("urun_adi", "?"), "deger": round(deger, 2),
                            "stok": stok, "fiyat": fiyat, "kategori": kat})

    en_pahali = sorted(urun_deger, key=lambda x: -x["deger"])[:10]
    return {"toplam_deger": round(toplam_deger, 2), "kritik_deger": round(kritik_deger, 2),
            "kategori": kategori_deger, "en_pahali": en_pahali}


def _teacher_workload(data: dict) -> list[dict]:
    """Ogretmen yuklenme analizi — brans, ogrenci sayisi, not girisi."""
    teachers = data.get("akademik", {}).get("teachers", [])
    grades = data.get("akademik", {}).get("grades", [])
    odevler = data.get("akademik", {}).get("odevler", [])
    if not teachers:
        return []

    brans_not: dict[str, int] = {}
    brans_odev: dict[str, int] = {}
    for g in grades:
        ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
        brans_not[ders] = brans_not.get(ders, 0) + 1
    for o in odevler:
        ders = getattr(o, "ders", "") if not isinstance(o, dict) else o.get("ders", "")
        brans_odev[ders] = brans_odev.get(ders, 0) + 1

    results = []
    for t in teachers:
        ad = (getattr(t, "ad", "") if not isinstance(t, dict) else t.get("ad", "")) + " " + \
             (getattr(t, "soyad", "") if not isinstance(t, dict) else t.get("soyad", ""))
        brans = getattr(t, "brans", "") if not isinstance(t, dict) else t.get("brans", "")
        not_cnt = brans_not.get(brans, 0)
        odev_cnt = brans_odev.get(brans, 0)
        yuklenme = not_cnt * 2 + odev_cnt * 3  # basit yuklenme skoru
        results.append({"ad": ad.strip(), "brans": brans,
                         "not_girisi": not_cnt, "odev_verme": odev_cnt,
                         "yuklenme_skor": yuklenme,
                         "durum": "Aktif" if not_cnt + odev_cnt > 0 else "Pasif"})

    return sorted(results, key=lambda x: -x["yuklenme_skor"])


def _module_activity_score(data: dict) -> list[dict]:
    """Modul aktivite skoru — her modulun kayit yogunlugu, cesitliligi, guncelligi."""
    mod_names = {
        "akademik": "Akademik Takip", "olcme": "Olcme Degerlendirme",
        "ik": "Insan Kaynaklari", "rehberlik": "Rehberlik",
        "saglik": "Okul Sagligi", "butce": "Butce Gelir Gider",
        "tdm": "Tuketim Demirbas", "toplanti": "Toplanti Kurullar",
        "sosyal": "Sosyal Etkinlik", "destek": "Destek Hizmetleri",
        "randevu": "Randevu Ziyaretci", "ssg": "Sivil Savunma",
        "kutuphane": "Kutuphane", "dijital_kutuphane": "Dijital Kutuphane",
        "egitim_koclugu": "Egitim Koclugu", "erken_uyari": "Erken Uyari",
        "kayit": "Kayit Modulu", "cefr": "CEFR Placement",
        "koi": "Kurumsal Org", "halkla_iliskiler": "Halkla Iliskiler",
        "sosyal_medya": "Sosyal Medya", "kurum_hizmetleri": "Kurum Hizmetleri",
        "kullanici": "Kullanici Yonetimi", "mezunlar": "Mezunlar",
    }
    results = []
    for key, label in mod_names.items():
        vals = data.get(key, {})
        total = sum(_safe_len(v) for v in vals.values() if isinstance(v, list))
        field_cnt = len(vals)
        filled_fields = sum(1 for v in vals.values()
                            if (isinstance(v, list) and len(v) > 0) or
                            (isinstance(v, (int, float)) and v > 0) or
                            (isinstance(v, str) and v))
        completeness = round(filled_fields / max(field_cnt, 1) * 100)
        # Aktivite skoru: kayit yogunlugu + alan dolulugu
        score = min(100, total * 2 + completeness)

        if score >= 80: level, color = "Ustun", "#6366f1"
        elif score >= 50: level, color = "Aktif", "#22c55e"
        elif score >= 20: level, color = "Temel", "#f59e0b"
        elif score > 0: level, color = "Baslangic", "#f97316"
        else: level, color = "Pasif", "#ef4444"

        results.append({"modul": label, "key": key, "kayit": total, "alan": field_cnt,
                         "dolu_alan": filled_fields, "doluluk": completeness,
                         "skor": min(100, score), "seviye": level, "color": color})
    return sorted(results, key=lambda x: -x["skor"])


def _student_potential_analysis(data: dict) -> list[dict]:
    """Ogrenci potansiyel analizi — en yuksek notu ile en dusuk notu karsilastir.
    Buyuk fark = potansiyel var ama kullanilmiyor."""
    ak = data.get("akademik", {})
    grades = ak.get("grades", [])
    if not grades:
        return []

    stu_grades: dict[str, dict] = {}
    for g in grades:
        sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
        try:
            p = float(puan)
            if sid not in stu_grades:
                stu_grades[sid] = {"puanlar": [], "dersler": {}, "ad": ""}
            stu_grades[sid]["puanlar"].append(p)
            stu_grades[sid]["dersler"][ders] = p
        except (TypeError, ValueError):
            pass

    # Isim eslestir
    for s in ak.get("students", []):
        sid = getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "")
        ad = getattr(s, "tam_ad", "") if not isinstance(s, dict) else f"{s.get('ad', '')} {s.get('soyad', '')}"
        if sid in stu_grades:
            stu_grades[sid]["ad"] = ad

    results = []
    for sid, info in stu_grades.items():
        puanlar = info["puanlar"]
        if len(puanlar) < 2:
            continue
        mx = max(puanlar)
        mn = min(puanlar)
        fark = mx - mn
        ort = sum(puanlar) / len(puanlar)

        # Potansiyel analizi
        if fark >= 25 and mn < 60:
            en_iyi_ders = max(info["dersler"].items(), key=lambda x: x[1])
            en_kotu_ders = min(info["dersler"].items(), key=lambda x: x[1])
            results.append({
                "ad": info["ad"], "sid": sid, "ort": round(ort, 1),
                "max": mx, "min": mn, "fark": fark,
                "en_iyi": f"{en_iyi_ders[0]} ({en_iyi_ders[1]:.0f})",
                "en_kotu": f"{en_kotu_ders[0]} ({en_kotu_ders[1]:.0f})",
                "yorum": f"{info['ad']}: {en_iyi_ders[0]}'de {en_iyi_ders[1]:.0f} alabiliyorsa "
                         f"{en_kotu_ders[0]}'de de {mn:.0f}'dan yuksek olabilir. "
                         f"Potansiyel fark: {fark:.0f} puan.",
            })

    return sorted(results, key=lambda x: -x["fark"])


def _class_comparison(data: dict) -> list[dict]:
    """Sinif karsilastirma — en iyi vs en kotu sinif, neden?"""
    ak = data.get("akademik", {})
    grades = ak.get("grades", [])
    students = ak.get("students", [])
    attendance = ak.get("attendance", [])
    if not grades or not students:
        return []

    # Sinif bazli ogrenci ID'leri
    sinif_ids: dict[str, set] = {}
    for s in students:
        durum = getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")
        if durum != "aktif":
            continue
        sinif = str(getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", ""))
        sube = str(getattr(s, "sube", "") if not isinstance(s, dict) else s.get("sube", ""))
        sid = getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "")
        key = f"{sinif}/{sube}"
        sinif_ids.setdefault(key, set()).add(sid)

    # Sinif bazli metrikleri hesapla
    sinif_data = []
    for key, ids in sinif_ids.items():
        puanlar = []
        for g in grades:
            sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
            if sid in ids:
                try:
                    puanlar.append(float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)))
                except (TypeError, ValueError):
                    pass
        devamsiz = sum(1 for a in attendance
                       if (getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")) in ids
                       and (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")

        if puanlar:
            sinif_data.append({
                "sinif": key, "ogrenci": len(ids),
                "ort": round(sum(puanlar) / len(puanlar), 1),
                "not_sayisi": len(puanlar),
                "devamsiz": devamsiz,
                "dev_per_stu": round(devamsiz / len(ids), 1) if ids else 0,
            })

    return sorted(sinif_data, key=lambda x: -x["ort"])


def _teacher_effectiveness(data: dict) -> list[dict]:
    """Ogretmen etkinlik skoru — bransindaki ogrenci basarisindan hesapla."""
    ak = data.get("akademik", {})
    grades = ak.get("grades", [])
    teachers = ak.get("teachers", [])
    if not grades or not teachers:
        return []

    brans_puanlar: dict[str, list] = {}
    for g in grades:
        ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        try:
            brans_puanlar.setdefault(ders, []).append(float(puan))
        except (TypeError, ValueError):
            pass

    brans_ogretmen: dict[str, str] = {}
    for t in teachers:
        brans = getattr(t, "brans", "") if not isinstance(t, dict) else t.get("brans", "")
        ad = (getattr(t, "ad", "") if not isinstance(t, dict) else t.get("ad", "")) + " " + \
             (getattr(t, "soyad", "") if not isinstance(t, dict) else t.get("soyad", ""))
        if brans:
            brans_ogretmen[brans] = ad.strip()

    results = []
    for brans, puanlar in brans_puanlar.items():
        ort = sum(puanlar) / len(puanlar)
        ogretmen = brans_ogretmen.get(brans, "-")
        # Etkinlik skoru: 0-100
        skor = min(100, max(0, ort * 1.1))  # Not ortalamasini etkinlige cevir
        results.append({
            "ogretmen": ogretmen, "brans": brans,
            "ort": round(ort, 1), "not_sayisi": len(puanlar),
            "skor": round(skor, 1),
            "durum": "Ustun" if skor >= 85 else ("Iyi" if skor >= 70 else ("Gelismeli" if skor >= 55 else "Destek Gerekli")),
        })
    return sorted(results, key=lambda x: -x["skor"])


def _weekly_action_plan(data: dict, role: str) -> list[dict]:
    """Her rol icin otomatik haftalik aksiyon plani."""
    actions = []
    ak = data.get("akademik", {})
    s_cnt = ak.get("students_aktif", 0)

    if role == "Yonetici":
        # Acil isler
        if data.get("butce", {}).get("toplam_gelir", 0) == 0:
            actions.append({"gun": "Pazartesi", "icon": "💰", "gorev": "Butce gelir kayitlarini girin",
                            "modul": "Butce Gelir Gider", "oncelik": "ACIL"})
        if data.get("ik", {}).get("employees_aktif", 0) < 5:
            actions.append({"gun": "Pazartesi", "icon": "👥", "gorev": "Tum personeli IK'ya kaydedin",
                            "modul": "Insan Kaynaklari", "oncelik": "ACIL"})
        if not data.get("rehberlik", {}).get("gorusmeler"):
            actions.append({"gun": "Sali", "icon": "📋", "gorev": "Rehberlik birimini aktiflestiirin",
                            "modul": "Rehberlik", "oncelik": "YUKSEK"})
        if not data.get("ssg", {}).get("tatbikat"):
            actions.append({"gun": "Carsamba", "icon": "🚨", "gorev": "Tahliye tatbikati planlayin",
                            "modul": "Sivil Savunma", "oncelik": "YUKSEK"})
        actions.append({"gun": "Persembe", "icon": "📊", "gorev": "AI Analiz raporunu inceleyin",
                        "modul": "AI Destek", "oncelik": "ORTA"})
        actions.append({"gun": "Cuma", "icon": "📅", "gorev": "Haftalik degerlendirme toplantisi",
                        "modul": "Toplanti Kurullar", "oncelik": "ORTA"})

    elif role == "Ogretmen":
        actions.append({"gun": "Pazartesi", "icon": "📝", "gorev": "Bu hafta verilecek odevleri planla",
                        "modul": "Akademik Takip > Odev", "oncelik": "YUKSEK"})
        actions.append({"gun": "Sali", "icon": "📋", "gorev": "Devamsiz ogrenci velilerini ara",
                        "modul": "KOI > Iletisim", "oncelik": "YUKSEK"})
        actions.append({"gun": "Carsamba", "icon": "📊", "gorev": "KYT kazanim yoklama testi uygula",
                        "modul": "Akademik Takip > KYT", "oncelik": "ORTA"})
        actions.append({"gun": "Persembe", "icon": "🌍", "gorev": "CEFR seviye tespit sinavi olustur",
                        "modul": "Yabanci Dil > CEFR", "oncelik": "ORTA"})
        actions.append({"gun": "Cuma", "icon": "📈", "gorev": "Haftalik ogrenci ilerleme kontrolu",
                        "modul": "AI Destek", "oncelik": "ORTA"})

    elif role == "Veli":
        actions.append({"gun": "Pazartesi", "icon": "📖", "gorev": "Cocugunuzla 30dk kitap okuyun",
                        "modul": "Kutuphane / Dijital Kutuphane", "oncelik": "GUNLUK"})
        actions.append({"gun": "Sali", "icon": "📝", "gorev": "Odev durumunu kontrol edin",
                        "modul": "Ogrenci Paneli", "oncelik": "YUKSEK"})
        actions.append({"gun": "Carsamba", "icon": "🌍", "gorev": "15dk Ingilizce pratik yaptirin",
                        "modul": "Yabanci Dil > SRS Kelime", "oncelik": "ORTA"})
        actions.append({"gun": "Persembe", "icon": "🧮", "gorev": "Matematik Koyu'nde alistirma",
                        "modul": "Matematik Koyu", "oncelik": "ORTA"})
        actions.append({"gun": "Cuma", "icon": "📊", "gorev": "Haftalik gelisim raporunu inceleyin",
                        "modul": "AI Destek", "oncelik": "ORTA"})

    elif role in ("Ogrenci", "Öğrenci"):
        actions.append({"gun": "Her gun", "icon": "📖", "gorev": "30dk kitap oku",
                        "modul": "Okuma Kutuphanesi", "oncelik": "GUNLUK"})
        actions.append({"gun": "Her gun", "icon": "🌍", "gorev": "15dk Ingilizce kelime calis",
                        "modul": "Yabanci Dil > SRS", "oncelik": "GUNLUK"})
        actions.append({"gun": "Pazartesi", "icon": "📝", "gorev": "Odevlerini kontrol et ve planla",
                        "modul": "Ogrenci Paneli", "oncelik": "YUKSEK"})
        actions.append({"gun": "Carsamba", "icon": "🧮", "gorev": "Matematik Koyu alistirmasi",
                        "modul": "Matematik Koyu", "oncelik": "ORTA"})
        actions.append({"gun": "Persembe", "icon": "💻", "gorev": "Bilisim Vadisi'nde kodlama",
                        "modul": "Bilisim Vadisi", "oncelik": "ORTA"})
        actions.append({"gun": "Cuma", "icon": "🎨", "gorev": "Sanat Sokagi etkinligi",
                        "modul": "Sanat Sokagi", "oncelik": "DUSUK"})

    return actions


def _render_weekly_plan(actions: list[dict]):
    """Haftalik aksiyon planini premium kartlarla render et."""
    if not actions:
        return
    st.markdown("#### Bu Hafta Yapilacaklar")
    pri_colors = {"ACIL": "#ef4444", "YUKSEK": "#f97316", "ORTA": "#f59e0b",
                  "DUSUK": "#22c55e", "GUNLUK": "#6366f1"}
    for a in actions:
        clr = pri_colors.get(a["oncelik"], "#64748b")
        st.markdown(f"""<div style="display:flex;gap:10px;align-items:center;padding:8px 0;
        border-bottom:1px solid #1e293b;">
        <div style="min-width:28px;font-size:1.3rem;">{a['icon']}</div>
        <div style="min-width:85px;padding:3px 8px;background:{clr}20;border-radius:6px;
        text-align:center;font-size:.7rem;color:{clr};font-weight:700;border:1px solid {clr}40;">
        {a['gun']}</div>
        <div style="flex:1;">
        <div style="color:#e2e8f0;font-weight:600;font-size:.88rem;">{a['gorev']}</div>
        <div style="color:#64748b;font-size:.7rem;">{a['modul']}</div>
        </div>
        <div style="font-size:.6rem;color:{clr};font-weight:700;">{a['oncelik']}</div>
        </div>""", unsafe_allow_html=True)


def _deep_rule_analysis(data: dict) -> dict:
    """Kural bazli derin analiz motoru — AI cagirmadan veriyi yorumlar.
    Her modulu inceler, cross-module iliskileri tespit eder, yol haritasi uretir.
    Returns: {findings: [...], roadmap: [...], cross_insights: [...], risk_matrix: [...]}
    """
    findings = []  # (severity, icon, title, detail, action)
    roadmap = []   # (priority, timeframe, title, detail)
    cross = []     # Cross-module insight
    risk_mx = []   # Risk matrix entries

    ak = data.get("akademik", {})
    od = data.get("olcme", {})
    ik = data.get("ik", {})
    rh = data.get("rehberlik", {})
    sg = data.get("saglik", {})
    bu = data.get("butce", {})
    tdm = data.get("tdm", {})
    tp = data.get("toplanti", {})
    se = data.get("sosyal", {})
    ds = data.get("destek", {})
    eu = data.get("erken_uyari", {})
    kul = data.get("kullanici", {})

    s_cnt = ak.get("students_aktif", 0)
    t_cnt = ak.get("teachers_count", 0)

    # ═══ 1. AKADEMIK DERIN ANALIZ ═══
    grades = ak.get("grades", [])
    if grades:
        ders_puanlar: dict[str, list] = {}
        for g in grades:
            ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
            puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
            try:
                ders_puanlar.setdefault(ders, []).append(float(puan))
            except (TypeError, ValueError):
                pass

        # En dusuk ders
        if ders_puanlar:
            en_dusuk = min(ders_puanlar.items(), key=lambda x: sum(x[1])/len(x[1]))
            en_yuksek = max(ders_puanlar.items(), key=lambda x: sum(x[1])/len(x[1]))
            dusuk_ort = sum(en_dusuk[1]) / len(en_dusuk[1])
            yuksek_ort = sum(en_yuksek[1]) / len(en_yuksek[1])
            fark = yuksek_ort - dusuk_ort

            if dusuk_ort < 60:
                findings.append(("critical", "📉", f"{en_dusuk[0]} dersi kritik: Ort {dusuk_ort:.1f}",
                    f"En basarili ders {en_yuksek[0]} (ort {yuksek_ort:.1f}) ile arasinda {fark:.1f} puan fark var.",
                    f"{en_dusuk[0]} ogretmeni ile gorusun, ek ders/etut planlayin"))
                roadmap.append(("ACIL", "1 Hafta", f"{en_dusuk[0]} icin acil destek plani",
                    f"Etut programi + odev takibi + veli bilgilendirme"))

            if fark > 20:
                findings.append(("warning", "⚖️", f"Dersler arasi dengesizlik: {fark:.0f} puan fark",
                    f"{en_dusuk[0]} ({dusuk_ort:.1f}) vs {en_yuksek[0]} ({yuksek_ort:.1f})",
                    "Dusuk performansli derslere ek kaynak ayirin"))

    # Not sayisi ogrenci sayisina gore yeterli mi?
    if s_cnt > 0 and len(grades) > 0:
        not_per_ogrenci = len(grades) / s_cnt
        if not_per_ogrenci < 0.5:
            findings.append(("warning", "📝", f"Not girisi yetersiz: Ogrenci basina {not_per_ogrenci:.1f} not",
                f"{s_cnt} ogrenci icin sadece {len(grades)} not kaydi var.",
                "Not girislerini hizlandirin — en az 4 not/ogrenci/donem hedefleyin"))

    # ═══ 2. DEVAMSIZLIK ANALIZ ═══
    attendance = ak.get("attendance", [])
    if attendance and s_cnt > 0:
        ozursuz = sum(1 for a in attendance
            if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
        devamsiz_oran = ozursuz / s_cnt * 100

        if devamsiz_oran > 10:
            findings.append(("critical", "📋", f"Ozursuz devamsizlik orani yuksek: %{devamsiz_oran:.1f}",
                f"{s_cnt} ogrencide {ozursuz} ozursuz gun. MEB limiti ogrenci basina 20 gun.",
                "Devamsiz ogrenci velileriyle iletisime gecin"))
            roadmap.append(("YUKSEK", "2 Hafta", "Devamsizlik mudahale programi",
                "Veli gorusmeleri + rehberlik yonlendirmesi + yoklama takibi siklastirma"))

    # ═══ 3. IK ANALIZ ═══
    emp_cnt = ik.get("employees_aktif", 0)
    if emp_cnt < 5 and s_cnt > 30:
        findings.append(("critical", "👥", f"IK modulu neredeyse bos: {emp_cnt} personel kayitli",
            f"{s_cnt} ogrenciye hizmet veren tum kadro IK'ya kayitli olmali.",
            "IK > Kurum Aktif Calisanlar'dan tum personeli ekleyin"))
        roadmap.append(("ACIL", "1 Hafta", "IK personel kaydini tamamlama",
            "Tum ogretmen + idari personel + destek kadrosunu sisteme girin"))

    if not ik.get("performance"):
        findings.append(("info", "⭐", "Performans degerlendirmesi yapilmamis",
            "Donem sonu performans degerlendirmesi yapilmasi yasal zorunluluktur.",
            "IK > Performans sekmesinden donemsel degerlendirme baslatin"))
        roadmap.append(("ORTA", "1 Ay", "Performans degerlendirme dongusu",
            "Kriterler belirle → Ogrenciden geri bildirim → 360 derece → Sonuc paylasimi"))

    # ═══ 4. MALI ANALIZ ═══
    gelir = bu.get("toplam_gelir", 0)
    gider = bu.get("toplam_gider", 0)
    net = gelir - gider

    if gelir == 0 and gider > 0:
        findings.append(("critical", "💸", f"Gelir kaydi sifir — gider {gider:,.0f} TL",
            "Butce modulunde gelir girisi yapilmamis. Mali tablo eksik.",
            "Butce > Gelir Kayit'tan ogretim ucreti, bagis vb. gelir girisi yapin"))
        roadmap.append(("ACIL", "3 Gun", "Butce gelir kaydi girisi",
            "Tum gelir kalemleri (ucret, bagis, etkinlik, diger) sisteme girilmeli"))

    if net < 0 and gelir > 0:
        acik_oran = abs(net) / gelir * 100 if gelir > 0 else 0
        findings.append(("critical", "📊", f"Butce acigi: {net:,.0f} TL (%{acik_oran:.0f} acik)",
            f"Gelir {gelir:,.0f} TL, Gider {gider:,.0f} TL.",
            "Gider kalemlerini inceleyin, tasarruf plani olusturun"))

    # ═══ 5. STOK ANALIZ ═══
    urunler = tdm.get("urunler", [])
    kritik_stok = [u for u in urunler
        if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
        and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0]
    if urunler:
        kritik_oran = len(kritik_stok) / len(urunler) * 100
        if kritik_oran > 50:
            toplam_maliyet = sum(
                (u.get("min_stok", 0) - u.get("stok", 0)) * u.get("birim_fiyat", 0)
                for u in kritik_stok if u.get("birim_fiyat"))
            findings.append(("critical", "📦", f"Stok krizi: {len(kritik_stok)}/{len(urunler)} urun kritik (%{kritik_oran:.0f})",
                f"Tahmini satin alma maliyeti: {toplam_maliyet:,.0f} TL",
                "TDM > Satin Alma'dan toplu siparis olusturun"))
            roadmap.append(("ACIL", "1 Hafta", f"Toplu satin alma: ~{toplam_maliyet:,.0f} TL",
                "Kritik urunleri oncelik sirasina gore siparis edin"))

    # ═══ 6. REHBERLIK ANALIZ ═══
    if s_cnt > 50 and not rh.get("gorusmeler") and not rh.get("vakalar"):
        findings.append(("warning", "📋", "Rehberlik modulu tamamen bos",
            f"{s_cnt} ogrenci var ama hicbir rehberlik gorusmesi/vakasi kayitli degil.",
            "Rehberlik birimini aktif kullanima gecirin"))
        roadmap.append(("YUKSEK", "2 Hafta", "Rehberlik programi baslatma",
            "Her sinif icin tanitim gorusmesi + risk taramasi + BEP ihtiyaci belirleme"))

    # ═══ 6b. MEB DIJITAL FORMLAR ANALIZ ═══
    meb = data.get("meb_formlar", {})
    meb_risk = meb.get("risk", {})
    meb_toplam = meb.get("toplam_kayit", 0)
    # Acil müdahale gerektiren durumlar
    acil = meb_risk.get("acil_mudahale", 0)
    if acil > 0:
        findings.append(("critical", "🚨", f"MEB Formlar: {acil} ACIL mudahale gerektiren durum",
            f"Psikolojik yonlendirme veya ev ziyareti formlarindan acil vakalar tespit edildi.",
            "Rehberlik > MEB Formlar'dan ilgili kayitlari inceleyin ve mudahale planini baslatin"))
        roadmap.append(("ACIL", "Hemen", f"{acil} ogrenci icin acil mudahale",
            "Psikolojik destek + aile bilgilendirme + gerekirse saglik kurulusuna yonlendirme"))
    # DEHB/ÖÖG şüpheleri
    dehb = meb_risk.get("dehb_suphe", 0)
    oog = meb_risk.get("oog_suphe", 0)
    if dehb + oog > 0:
        findings.append(("warning", "🧠", f"MEB Formlar: {dehb} DEHB + {oog} OOG suplesi — yonlendirme onerilmis",
            "Gozlem formlari sonucu RAM veya saglik kurulusuna yonlendirme onerilen ogrenciler var.",
            "Rehberlik > Yonlendirme sekmesinden takip surecini baslatin"))
        roadmap.append(("YUKSEK", "2 Hafta", f"DEHB/OOG yonlendirme takibi ({dehb+oog} ogrenci)",
            "RAM basvurusu + aile bilgilendirme + okul ici destek plani"))
    # Disiplin olayları
    disiplin = meb_risk.get("disiplin_olay", 0)
    if disiplin >= 3:
        findings.append(("warning", "⚖️", f"MEB Formlar: {disiplin} disiplin gorusmesi kaydi",
            "Disiplin olaylarinda artis gozleniyor. Onleyici rehberlik programi gerekli.",
            "Grup rehberligi + sinif ici sosyal beceri programi planlayin"))
    # Form doluluk analizi
    if s_cnt > 30 and meb_toplam == 0:
        findings.append(("info", "📄", "MEB dijital formlar henuz kullanilmamis",
            f"{s_cnt} ogrenci var ama 35 MEB formundan hicbiri doldurulmamis.",
            "Rehberlik > MEB Formlar sekmesinden oncelikli formlari doldurun (risk taramasi, gorusme, gozlem)"))
        roadmap.append(("ORTA", "1 Ay", "MEB dijital form sistemi aktif kullanima gecirme",
            "1) Ogrenci On Gorusme, 2) Sinif Risk Haritasi, 3) Ihtiyac Belirleme formlariyla baslatin"))

    # ═══ 7. GUVENLIK ANALIZ ═══
    ssg = data.get("ssg", {})
    if not ssg.get("tatbikat") and s_cnt > 0:
        findings.append(("warning", "🚨", "Sivil savunma tatbikati yapilmamis",
            "MEB mevzuatina gore yilda en az 2 tahliye tatbikati zorunludur.",
            "SSG > Tatbikat Planlama'dan tahliye tatbikati planlayin"))
        roadmap.append(("YUKSEK", "1 Ay", "Tahliye tatbikati planlama",
            "Deprem + yangin senaryolari + tahliye plani + ogrenci/personel egitimi"))

    # ═══ 8. CROSS-MODULE INSIGHTS ═══
    # Devamsizlik + Dusuk Not iliskisi
    if grades and attendance:
        devamsiz_ids = set()
        for a in attendance:
            sid = getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")
            turu = getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")
            if turu == "ozursuz":
                devamsiz_ids.add(sid)
        if devamsiz_ids:
            devamsiz_puanlar = []
            diger_puanlar = []
            for g in grades:
                sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
                puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
                try:
                    p = float(puan)
                    if sid in devamsiz_ids:
                        devamsiz_puanlar.append(p)
                    else:
                        diger_puanlar.append(p)
                except (TypeError, ValueError):
                    pass
            if devamsiz_puanlar and diger_puanlar:
                dev_ort = sum(devamsiz_puanlar) / len(devamsiz_puanlar)
                dig_ort = sum(diger_puanlar) / len(diger_puanlar)
                fark = dig_ort - dev_ort
                if fark > 5:
                    cross.append(f"📊 Devamsiz ogrencilerin not ortalamasi {dev_ort:.1f}, "
                                 f"diger ogrencilerin {dig_ort:.1f} — {fark:.1f} puan fark. "
                                 f"Devamsizlik basariyi dogrudan etkiliyor.")

    # Odev sayisi + Not iliskisi
    odevler = ak.get("odevler", [])
    if odevler and grades and s_cnt > 0:
        odev_per_stu = len(odevler) / s_cnt
        if odev_per_stu < 0.5:
            cross.append(f"📝 Ogrenci basina {odev_per_stu:.1f} odev — yetersiz. "
                         f"Arastirmalar odev verilen derslerde %15-20 daha yuksek basari gosteriyor.")

    # Kullanici sayisi vs ogrenci+personel
    kul_total = kul.get("total", 0)
    beklenen = s_cnt + t_cnt + emp_cnt
    if beklenen > 0 and kul_total < beklenen * 0.5:
        cross.append(f"🔑 Sistemde {kul_total} kullanici var ama beklenen ~{beklenen}+. "
                     f"Ogrenci/veli/personel kullanici hesaplari olusturulmali.")

    # Etkinlik yoklugu
    if s_cnt > 50 and _safe_len(se.get("etkinlikler", [])) == 0:
        cross.append("🎭 Sosyal etkinlik/kulup kaydi yok. Ogrenci bagliligi ve motivasyonu icin "
                     "en az 3 kulup + donemde 2 etkinlik planlanmali.")

    # ═══ 9. RISK MATRIX ═══
    # (etki, olasilik, baslik)
    if gelir == 0:
        risk_mx.append((5, 5, "Mali: Gelir kaydi yok"))
    if len(kritik_stok) > len(urunler) * 0.5:
        risk_mx.append((4, 5, "Operasyonel: Stok krizi"))
    if emp_cnt < 5:
        risk_mx.append((4, 4, "IK: Personel kaydi eksik"))
    if not rh.get("gorusmeler"):
        risk_mx.append((3, 4, "Akademik: Rehberlik pasif"))
    if not ssg.get("tatbikat"):
        risk_mx.append((5, 3, "Guvenlik: Tatbikat yapilmamis"))
    if not ik.get("performance"):
        risk_mx.append((3, 3, "IK: Performans degerlendirme yok"))

    # ═══ 10. KAYIT MODULU ═══
    kayit_adaylar = data.get("kayit", {}).get("adaylar", [])
    hi_soz = data.get("halkla_iliskiler", {}).get("sozlesmeler", [])
    if not kayit_adaylar and not hi_soz:
        findings.append(("info", "🎯", "Kayit modulu bos — aday pipeline yok",
            "Ogrenci kayit sureci dijitallestirilmemis. Aday takibi, gorusme, fiyat teklifi sisteme girilmeli.",
            "Kayit Modulu'nden yeni aday girisi baslatin"))
        roadmap.append(("ORTA", "2 Hafta", "Kayit pipeline dijitallestirme",
            "Mevcut adaylari sisteme girin → gorusme planlama → fiyat teklifi → sozlesme akisi"))
    elif hi_soz:
        kesin = sum(1 for s in hi_soz if s.get("kayit_sonucu") == "Kesin Kayıt")
        if kesin > 0:
            cross.append(f"🎯 {len(hi_soz)} sozlesme kaydi var, {kesin} kesin kayit. "
                         f"Donusum orani: %{round(kesin/len(hi_soz)*100) if hi_soz else 0}")

    # ═══ 11. YABANCI DIL ═══
    cefr_exams = data.get("cefr", {}).get("exams", [])
    cefr_results = data.get("cefr", {}).get("results", [])
    if not cefr_exams and s_cnt > 0:
        findings.append(("info", "🌍", "CEFR seviye tespit sinavi yapilmamis",
            f"{s_cnt} ogrenci var ama Ingilizce seviye tespiti yapilmamis. "
            "Sene basi CEFR sinavi ile ogrenci seviyeleri belirlenmeli.",
            "Yabanci Dil > CEFR Seviye Tespit'ten sinav olusturun"))
        roadmap.append(("YUKSEK", "2 Hafta", "CEFR sene basi seviye tespiti",
            "Her sinif icin placement sinavi olustur → ogrencilere cozdur → seviye raporu al"))
    elif cefr_results:
        below_target = sum(1 for r in cefr_results if r.get("is_below_target"))
        if below_target > 0:
            cross.append(f"🌍 {below_target}/{len(cefr_results)} ogrenci CEFR hedef seviyesinin altinda. "
                         f"Yabanci dil destek programi planlanmali.")

    # ═══ 12. DIJITAL KUTUPHANE ═══
    dk = data.get("dijital_kutuphane", {})
    if not dk.get("kaynaklar") and s_cnt > 0:
        findings.append(("info", "📱", "Dijital kutuphane bos",
            "Dijital egitim kaynaklari tanimlanmamis. Video, PDF, interaktif icerik eklenebilir.",
            "Dijital Kutuphane modulunden kademe bazli kaynaklar tanimlayin"))
        roadmap.append(("DUSUK", "1 Ay", "Dijital kaynak ekleme",
            "Her kademe icin en az 10 dijital kaynak (video/PDF/interaktif) tanimlayin"))

    # ═══ 13. KUTUPHANE ═══
    ku = data.get("kutuphane", {})
    if not ku.get("materyaller") and s_cnt > 0:
        findings.append(("info", "📚", "Kutuphane kaydi yok",
            "Fiziksel kutuphane envanteri sisteme girilmemis.",
            "Kutuphane > Yeni Materyal Kaydi'ndan envanter girisi yapin"))

    # ═══ 14. EGITIM KOCLUGU ═══
    ek = data.get("egitim_koclugu", {})
    if not ek.get("ogrenciler") and s_cnt > 30:
        findings.append(("info", "🎯", "Egitim koclugu programi baslatilmamis",
            "Bireysel ogrenci koclugu, hedef belirleme ve takip sistemi kullanilmiyor.",
            "Egitim Koclugu > Ogrenci Eslestirme'den koc-ogrenci atamasi yapin"))
        roadmap.append(("ORTA", "1 Ay", "Bireysel kocluk programi",
            "Risk grubu ogrencilere koc ata → haftalik gorusme → hedef takibi"))

    # ═══ 15. TOPLANTI ANALIZ ═══
    toplanti_gorevler = tp.get("gorevler", [])
    toplanti_meetings = tp.get("meetings", [])
    if toplanti_meetings and not toplanti_gorevler:
        findings.append(("warning", "📅", f"{len(toplanti_meetings)} toplanti var ama gorev/karar kaydi yok",
            "Toplanti yapiliyor ama alinan kararlar ve gorevler sisteme girilmiyor.",
            "Toplanti Yurutme'den karar ve gorev kaydi girin"))

    # ═══ 16. SOSYAL ETKINLIK ═══
    kulupler = se.get("kulupler", [])
    etkinlikler = se.get("etkinlikler", [])
    if s_cnt > 50 and len(kulupler) < 3:
        findings.append(("info", "🎭", f"Kulup sayisi yetersiz: {len(kulupler)}",
            f"{s_cnt} ogrenci icin en az 5 farkli kulup olmali. "
            "Kulup cesitliligi ogrenci bagliligi ve motivasyonunu arttirir.",
            "Sosyal Etkinlik > Kulupler'den yeni kulup olusturun (spor, sanat, bilim, drama, muzik)"))
        roadmap.append(("DUSUK", "1 Ay", "Kulup cesitliligini arttirma",
            "En az 5 farkli kategoride kulup ac → danisman ata → uye kaydi baslat"))

    # ═══ 17. DESTEK HIZMETLERI ═══
    if ds.get("tickets"):
        acik = sum(1 for t in ds["tickets"] if t.get("durum") in ("acik", "beklemede"))
        if acik > 5:
            findings.append(("warning", "🔧", f"{acik} acik destek talebi birikmis",
                "Destek taleplerinin hizli cozumu kurum memnuniyetini dogrudan etkiler.",
                "Destek Hizmetleri > Talepler'den acik talepleri atama yaparak kapatın"))

    # ═══ 18. SAGLIK ANALIZ ═══
    revir = sg.get("revir", [])
    if revir:
        sikayet_sayisi = len(revir)
        if sikayet_sayisi > 10:
            cross.append(f"🏥 {sikayet_sayisi} revir ziyareti — ogrenci sayisina gore "
                         f"oran: %{round(sikayet_sayisi/s_cnt*100) if s_cnt else 0}. "
                         f"Yuksekse saglik taramasi + hijyen egitimi planlayin.")

    # ═══ 19. RANDEVU ═══
    if not data.get("randevu", {}).get("randevular") and not data.get("randevu", {}).get("ziyaretler"):
        findings.append(("info", "📆", "Randevu ve ziyaretci modulu kullanilmiyor",
            "Veli randevulari ve ziyaretci takibi dijitallestirilmemis.",
            "Randevu > Randevu Yonetimi'nden randevu sistemi aktiflestirilmeli"))

    # ═══ 20. AI TRENI + MATEMATIK + SANAT + BILISIM ═══
    enrichment_active = 0
    for mod_name in ["AI Treni", "Matematik Koyu", "Sanat Sokagi", "Bilisim Vadisi"]:
        enrichment_active += 1  # Hepsi kod olarak var, aktif
    cross.append(f"🚀 4 zenginlestirme modulu (AI Treni, Matematik Koyu, Sanat Sokagi, Bilisim Vadisi) "
                 f"aktif. Ogrencilerin bu modulleri duzenli kullanmasi icin haftalik plan olusturun.")

    # ═══ 21. KISISEL DIL GELISIMI ═══
    cross.append("🌐 Kisisel Dil Gelisimi modulu bireysel dil ogrenme icin tasarlandi. "
                 "Ogrencilere SRS kelime tekrar programi + AI konusma pratiği atanabilir.")

    # ═══ 22. YABANCI DIL PERFORMANSI (Quiz + CEFR) ═══
    _yd = data.get("yd_sinav", {})
    _cefr = data.get("cefr", {})
    _yd_avg = _yd.get("avg_score", 0)
    _yd_total = _yd.get("total_results", 0)
    _yd_quiz_cnt = _yd.get("quiz_count", 0)
    _cefr_cnt = _safe_len(_cefr.get("results", []))

    if _yd_total == 0 and s_cnt > 0:
        findings.append(("warning", "🌍", "Yabanci dil degerlendirmesi yapilmamis",
            f"{s_cnt} ogrenci var ama henuz YD quiz/sinav sonucu girilmemis.",
            "Unite bazli quiz olusturun ve ogrencilere gonderin"))
        roadmap.append(("YUKSEK", "2 Hafta", "YD unite quiz sistemini aktiflestirilmeli",
            "Yabanci Dil > Unite Quiz > Quiz Olustur'dan ilk quizi hazirlayip gonderin"))

    if _yd_avg > 0 and _yd_avg < 50:
        findings.append(("critical", "🔴", f"Yabanci dil ortalamasi kritik: {_yd_avg:.1f}",
            f"{_yd_total} sinav sonucunun ortalamasi %50'nin altinda. "
            f"Beceri bazli (kelime/dilbilgisi) eksikler tespit edilmeli.",
            "Zayif unitelerde telafi quizleri olusturun, SRS kelime tekrar programini aktiflestirilmeli"))
        risk_mx.append(("YUKSEK", "Yabanci Dil", f"Ortalama {_yd_avg:.1f} — kritik seviye",
            "Unite bazli pekistirme + AI destekli kelime calismalari"))
    elif _yd_avg > 0 and _yd_avg < 70:
        findings.append(("warning", "🟡", f"Yabanci dil ortalamasi gelismeli: {_yd_avg:.1f}",
            f"{_yd_total} sinav sonucu, quiz sayisi: {_yd_quiz_cnt}. "
            f"Hedef %70+ icin ek pekistirme gerekli.",
            "Haftalik quiz uygulamayi surdurun, zayif unitelerde ek alistirma atanmalidir"))

    if _cefr_cnt == 0 and s_cnt > 0:
        findings.append(("info", "🌐", "CEFR seviye tespit sinavi yapilmamis",
            f"Ogrencilerin yabanci dil seviyesi belirlenmemis. "
            f"CEFR Seviye Tespit Sinavi ile bireysel seviyeleri belirleyin.",
            "Yabanci Dil > CEFR Seviye Tespit Sinavi'ndan sinav olusturup uygulatin"))
        roadmap.append(("ORTA", "1 Ay", "CEFR seviye tespiti tum ogrencilere uygulanmali",
            "Sene basi + sene sonu olmak uzere 2 kez CEFR tespit uygulatin"))

    # ═══ 23. REHBERLİK TEST & ENVANTER ANALİZİ ═══
    _rt = data.get("rhb_test", {})
    _rt_cnt = _rt.get("test_count", 0)
    _rt_tmm = _rt.get("tamamlanan", 0)
    _rt_otr = _rt.get("oturum_count", 0)

    if _rt_cnt == 0 and s_cnt > 0:
        findings.append(("info", "📝", "Rehberlik psikolojik test/envanter oluşturulmamış",
            "Öğrenci tanıma, risk tespiti ve bireysel farklılıkları anlamak için test envanterleri kullanılmalı.",
            "Rehberlik > Test ve Envanter sekmesinden online test oluşturun"))
    elif _rt_cnt > 0 and _rt_tmm == 0:
        findings.append(("warning", "📝", f"{_rt_cnt} test oluşturulmuş ama henüz uygulama yapılmamış",
            f"{_rt_otr} oturum başlamış ancak tamamlanan yok. Testlerin uygulanması takip edilmeli.",
            "Rehberlik öğretmeni test uygulama planı oluşturmalı"))
    elif _rt_tmm > 0:
        cross.append(f"📝 Rehberlik Test & Envanter: {_rt_cnt} test, {_rt_tmm} tamamlanan oturum. "
                     f"Test sonuçları erken uyarı risk hesabına dahil ediliyor.")

    # ═══ 24. AİLE BİLGİ FORMU ANALİZİ ═══
    _abf = data.get("aile_bilgi", {})
    _abf_toplam = _abf.get("toplam", 0)
    _abf_kritik = _abf.get("kritik_aile", 0)

    if _abf_toplam == 0 and s_cnt > 0:
        findings.append(("warning", "📋", "Aile Bilgi Formu doldurulmamış",
            f"{s_cnt} öğrenci var ama hiçbiri için Aile Bilgi Formu kaydı yok. "
            f"Rehberlik servisi veli görüşmelerinde MEB B.K.G.1.c formunu doldurmalı.",
            "Rehberlik > Aile Bilgi Formu sekmesinden formları doldurun"))
        roadmap.append(("YUKSEK", "1 Ay", "Tüm öğrenciler için Aile Bilgi Formu doldurulmalı",
            "Rehberlik öğretmeni sınıf bazlı veli görüşmeleri planlayarak formu tamamlamalı"))
    elif _abf_toplam > 0 and _abf_toplam < s_cnt * 0.5:
        findings.append(("info", "📋", f"Aile Bilgi Formu kapsam düşük: {_abf_toplam}/{s_cnt} öğrenci",
            f"Öğrencilerin sadece %{round(_abf_toplam / max(s_cnt, 1) * 100)}'i için form doldurulmuş.",
            "Eksik öğrenciler için de form doldurulmalı"))

    if _abf_kritik > 0:
        findings.append(("warning", "⚠️", f"{_abf_kritik} öğrencide kritik aile risk faktörü tespit edildi",
            f"Boşanma, ebeveyn kaybı, travma, bağımlılık gibi faktörler mevcut. "
            f"Bu öğrenciler rehberlik takibinde öncelikli olmalı.",
            "Erken Uyarı > Risk Değerlendirme ile bu öğrencileri yakından takip edin"))
        risk_mx.append(("YUKSEK", "Aile Yapısı", f"{_abf_kritik} kritik aile durumu",
            "Rehberlik yoğun takip + veli işbirliği + psikososyal destek"))

    # Aile bilgi cross-module
    if _abf_toplam > 0:
        cross.append(f"📋 Aile Bilgi Formu: {_abf_toplam} form, {_abf_kritik} kritik aile. "
                     f"Bu veriler Erken Uyarı risk skoruna dahil ediliyor — boşanma, kayıp, travma "
                     f"gibi faktörler otomatik risk artışına neden olur.")

    # CEFR Mock Exam kontrolleri
    _mock = data.get("cefr_mock", {})
    _mock_cnt = _mock.get("total_results", 0)
    _mock_avg = _mock.get("avg_score", 0)
    if _mock_cnt > 0 and _mock_avg < 50:
        findings.append(("warning", "🏆", f"CEFR Mock Exam ortalamasi dusuk: {_mock_avg:.1f}",
            f"{_mock_cnt} mock exam sonucu — beceri bazli (Listening/Reading/Writing/Speaking) "
            f"eksikler tespit edilmeli.",
            "CEFR Mock Exam sonuclarini beceri bazli inceleyip zayif alanlarda ek calisma planlayin"))
    if _mock_cnt == 0 and s_cnt > 0 and _cefr_cnt > 0:
        findings.append(("info", "🏆", "CEFR seviye tespiti yapilmis ama Mock Exam uygulanmamis",
            "Ogrencilerin Cambridge formatinda pratik yapmasi icin Mock Exam sinavi uygulanmali.",
            "Yabanci Dil > CEFR Mock Exam'den sinav olusturup yayinlayin"))

    # Cross-module YD insights
    _all_yd_sources = []
    if _yd_avg > 0:
        _all_yd_sources.append(f"Quiz ort: {_yd_avg:.1f}")
    if _cefr_cnt > 0:
        _all_yd_sources.append(f"{_cefr_cnt} CEFR tespiti")
    if _mock_cnt > 0:
        _all_yd_sources.append(f"{_mock_cnt} Mock Exam (ort: {_mock_avg:.1f})")
    if _all_yd_sources:
        cross.append(f"🌍 Yabanci Dil: {' | '.join(_all_yd_sources)}. "
                     f"Tum kaynaklari birlestirerek bireysel gelisim planlari olusturun.")
    elif s_cnt > 0:
        cross.append("🌍 Yabanci Dil: Hicbir degerlendirme yapilmamis — Quiz + CEFR + Mock Exam aktiflestirilmeli.")

    # ═══ GENEL OLGUNLUK YORUMU ═══
    active_count = sum(1 for vals in data.values()
                       if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0
                       or any(isinstance(v, (str, dict)) and v for v in vals.values()))
    if active_count < len(data) * 0.5:
        findings.append(("warning", "📊", f"Dijital olgunluk dusuk: {active_count}/{len(data)} modul aktif",
            f"Sistemin tam potansiyelini kullanmak icin en az %75 modul kapsamina ulasilmali.",
            "Her hafta 2 yeni modulu aktiflestirecek plan olusturun"))
        roadmap.append(("ORTA", "3 Ay", f"Dijital olgunluk hedefi: %75+ modul aktif",
            "Hafta 1-2: IK+Butce | Hafta 3-4: Rehberlik+Saglik | Hafta 5-6: Kutuphane+SSG | "
            "Hafta 7-8: CEFR+Kocluk | Hafta 9-12: Dijital Ktp+Kayit+Randevu"))

    return {"findings": findings, "roadmap": roadmap, "cross_insights": cross, "risk_matrix": risk_mx}


def _render_deep_analysis(analysis: dict):
    """Derin analiz sonuclarini premium kartlarla render et."""
    findings = analysis.get("findings", [])
    roadmap = analysis.get("roadmap", [])
    cross = analysis.get("cross_insights", [])
    risk_mx = analysis.get("risk_matrix", [])

    # ── BULGULAR ──
    if findings:
        st.markdown("#### Otomatik Bulgular")
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        for sev, icon, title, detail, action in sorted(findings, key=lambda x: severity_order.get(x[0], 9)):
            bg = {"critical": "linear-gradient(135deg,#1c0505,#3b0f0f)",
                  "warning": "linear-gradient(135deg,#1c1305,#3b2a0f)",
                  "info": "linear-gradient(135deg,#050c1c,#0f1e3b)"}.get(sev, "")
            border = {"critical": "#ef4444", "warning": "#f59e0b", "info": "#3b82f6"}.get(sev, "#64748b")
            title_c = {"critical": "#fca5a5", "warning": "#fcd34d", "info": "#93c5fd"}.get(sev, "#c7d2fe")

            st.markdown(f"""<div style="background:{bg};border-radius:12px;padding:14px 18px;
            margin:6px 0;border-left:4px solid {border};">
            <div style="font-size:.92rem;font-weight:700;color:{title_c};">{icon} {title}</div>
            <div style="font-size:.8rem;color:#cbd5e1;margin:4px 0;">{detail}</div>
            <div style="font-size:.78rem;color:#a5b4fc;padding:5px 10px;background:rgba(0,0,0,0.2);
            border-radius:6px;margin-top:6px;">💡 {action}</div>
            </div>""", unsafe_allow_html=True)

    # ── CROSS-MODULE INSIGHTS ──
    if cross:
        st.markdown("#### Moduller Arasi Iliskiler")
        for insight in cross:
            st.markdown(f"""<div style="background:linear-gradient(135deg,#0c1929,#1a2744);
            border-radius:10px;padding:12px 16px;margin:4px 0;border:1px solid rgba(59,130,246,0.2);">
            <span style="color:#93c5fd;font-size:.85rem;">{insight}</span>
            </div>""", unsafe_allow_html=True)

    # ── RISK MATRISI (Etki x Olasilik) ──
    if risk_mx:
        st.markdown("#### Risk Matrisi (Etki x Olasilik)")
        fig_rm = go.Figure()
        texts = [r[2] for r in risk_mx]
        x_vals = [r[1] for r in risk_mx]  # olasilik
        y_vals = [r[0] for r in risk_mx]  # etki
        scores = [x * y for x, y in zip(x_vals, y_vals)]
        fig_rm.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode="markers+text",
            text=texts, textposition="top center",
            textfont=dict(size=9, color="#c7d2fe"),
            marker=dict(size=[max(20, s * 3) for s in scores],
                        color=scores,
                        colorscale=[[0, "#22c55e"], [0.5, "#f59e0b"], [1, "#ef4444"]],
                        showscale=True,
                        colorbar=dict(title=dict(text="Risk", font=dict(color="#94a3b8")),
                                      tickfont=dict(color="#94a3b8")),
                        line=dict(width=1, color="#334155")),
        ))
        fig_rm.update_layout(
            height=350, margin=dict(l=50, r=20, t=20, b=50),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Olasilik (1-5)", range=[0, 6], gridcolor="#1e293b",
                       dtick=1, tickfont=dict(color="#94a3b8")),
            yaxis=dict(title="Etki (1-5)", range=[0, 6], gridcolor="#1e293b",
                       dtick=1, tickfont=dict(color="#94a3b8")),
            font=dict(color="#94a3b8"),
        )
        # Arka plan zonlari
        fig_rm.add_shape(type="rect", x0=0, y0=0, x1=2.5, y1=2.5,
                         fillcolor="rgba(34,197,94,0.05)", line=dict(width=0))
        fig_rm.add_shape(type="rect", x0=2.5, y0=2.5, x1=5, y1=5,
                         fillcolor="rgba(239,68,68,0.05)", line=dict(width=0))
        st.plotly_chart(fig_rm, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── YOL HARITASI ──
    if roadmap:
        st.markdown("#### Aksiyon Yol Haritasi")
        priority_order = {"ACIL": 0, "YUKSEK": 1, "ORTA": 2, "DUSUK": 3}
        priority_colors = {"ACIL": "#ef4444", "YUKSEK": "#f97316", "ORTA": "#f59e0b", "DUSUK": "#22c55e"}
        priority_icons = {"ACIL": "🔴", "YUKSEK": "🟠", "ORTA": "🟡", "DUSUK": "🟢"}

        for pri, timeframe, title, detail in sorted(roadmap, key=lambda x: priority_order.get(x[0], 9)):
            clr = priority_colors.get(pri, "#64748b")
            icon = priority_icons.get(pri, "⚪")
            st.markdown(f"""<div style="display:flex;gap:12px;align-items:flex-start;padding:8px 0;
            border-bottom:1px solid #1e293b;">
            <div style="min-width:70px;text-align:center;">
            <div style="font-size:1.1rem;">{icon}</div>
            <div style="font-size:.65rem;color:{clr};font-weight:700;">{pri}</div>
            <div style="font-size:.6rem;color:#475569;">{timeframe}</div>
            </div>
            <div style="flex:1;">
            <div style="font-size:.88rem;font-weight:700;color:#e2e8f0;">{title}</div>
            <div style="font-size:.78rem;color:#94a3b8;margin-top:2px;">{detail}</div>
            </div></div>""", unsafe_allow_html=True)


def _auto_executive_summary(client, data: dict) -> str | None:
    """Sayfa acildiginda otomatik 3 cumlelik executive summary ureten AI fonksiyonu."""
    cache_key = "_ai_exec_summary"
    if cache_key in st.session_state:
        return st.session_state[cache_key]
    if not client:
        return None
    try:
        inst = _compute_institution_score(data)
        ak = data.get("akademik", {})
        od = data.get("olcme", {})
        eu = data.get("erken_uyari", {})
        bu = data.get("butce", {})
        tdm = data.get("tdm", {})

        risk_high = sum(1 for r in eu.get("risks", []) if r.get("risk_level") in ("HIGH", "CRITICAL"))
        kritik_stok = sum(1 for u in tdm.get("urunler", [])
                          if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
                          and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0)
        net = bu.get("toplam_gelir", 0) - bu.get("toplam_gider", 0)

        prompt = (f"Kurum skoru %{inst['overall']:.0f}. "
                  f"{ak.get('students_aktif', 0)} ogrenci, {ak.get('teachers_count', 0)} ogretmen. "
                  f"Net bakiye {net:,.0f} TL. {risk_high} yuksek riskli ogrenci. "
                  f"{kritik_stok} kritik stok urunu. "
                  f"{od.get('questions_count', 0)} soru bankasi. "
                  f"Boyutlar: {', '.join(f'{k} %{v:.0f}' for k, v in inst['scores'].items())}. "
                  f"SADECE 3 CUMLE YAZ: 1) Genel durum, 2) En kritik sorun, 3) Oncelikli aksiyon. "
                  f"Turkce, profesyonel, yonetici perspektifi.")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Kisa, net, aksiyona donuk. Turkce. 3 cumle."},
                      {"role": "user", "content": prompt}],
            max_tokens=200, temperature=0.5,
        )
        text = resp.choices[0].message.content or ""
        st.session_state[cache_key] = text
        return text
    except Exception:
        return None


def _anomaly_detection(data: dict) -> list[dict]:
    """Basit anomali tespiti — esik degerlere gore uyari ureten motor."""
    anomalies = []

    # 1. Tum ogrenci riski LOW — bu anormal mi?
    risks = data.get("erken_uyari", {}).get("risks", [])
    if risks:
        all_low = all(r.get("risk_level") == "LOW" for r in risks)
        if all_low and len(risks) > 20:
            anomalies.append({
                "type": "info", "icon": "📊",
                "title": "Tum ogrenciler dusuk risk seviyesinde",
                "detail": f"{len(risks)} ogrencinin tamami LOW risk. Veri girisi yeterli mi kontrol edin.",
                "action": "Erken Uyari modulunden tarama baslatin",
            })

    # 2. Kritik stok orani > %80
    urunler = data.get("tdm", {}).get("urunler", [])
    kritik = sum(1 for u in urunler
                 if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
                 and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0)
    if urunler and kritik / len(urunler) > 0.8:
        anomalies.append({
            "type": "critical", "icon": "🚨",
            "title": f"Stok krizi: {kritik}/{len(urunler)} urun kritik seviyede (%{round(kritik/len(urunler)*100)})",
            "detail": "Urunlerin buyuk cogunlugu minimum stok altinda. Acil satin alma gerekli.",
            "action": "Tuketim & Demirbas > Satin Alma sekmesinden toplu siparis olusturun",
        })

    # 3. Gelir 0 ama gider var
    bu = data.get("butce", {})
    if bu.get("toplam_gelir", 0) == 0 and bu.get("toplam_gider", 0) > 0:
        anomalies.append({
            "type": "warning", "icon": "💸",
            "title": "Gelir kaydi girilmemis — gider var",
            "detail": f"Gider: {bu['toplam_gider']:,.0f} TL kayitli ama gelir kaydi sifir.",
            "action": "Butce > Gelir Kayit sekmesinden gelir girisi yapin",
        })

    # 4. IK'da 5'ten az personel
    emp = data.get("ik", {}).get("employees_aktif", 0)
    if emp < 5:
        anomalies.append({
            "type": "warning", "icon": "👥",
            "title": f"IK modulunde sadece {emp} personel kayitli",
            "detail": "Personel kadrounun tamamini IK modulune kaydetmeniz onerilir.",
            "action": "IK > Kurum Aktif Calisanlar sekmesinden personel ekleyin",
        })

    # 5. 8+ modul bos
    active_mods = sum(1 for vals in data.values()
                      if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0)
    bos = 18 - active_mods
    if bos >= 8:
        anomalies.append({
            "type": "warning", "icon": "📋",
            "title": f"{bos}/18 modul bos — veri kapsami dusuk (%{round(active_mods/18*100)})",
            "detail": "Sistemin tam potansiyelini kullanmak icin tum modullere veri girisi yapilmali.",
            "action": "Her modul icin en az temel verileri girin",
        })

    # 6. Rehberlik tamamen bos (ogrenci sayisi > 50 ise sorun)
    rh = data.get("rehberlik", {})
    stu_cnt = data.get("akademik", {}).get("students_aktif", 0)
    if stu_cnt > 50 and not rh.get("gorusmeler") and not rh.get("vakalar"):
        anomalies.append({
            "type": "warning", "icon": "📋",
            "title": "Rehberlik modulu tamamen bos",
            "detail": f"{stu_cnt} ogrenci var ama rehberlik gorusmesi/vaka kaydi yok.",
            "action": "Rehberlik > Gorusme Kayitlari sekmesinden gorusme baslatin",
        })

    # 6b. MEB Dijital Formlar anomali tespiti
    _meb_anom = data.get("meb_formlar", {})
    _meb_risk_anom = _meb_anom.get("risk", {})
    _acil_anom = _meb_risk_anom.get("acil_mudahale", 0)
    if _acil_anom > 0:
        anomalies.append({
            "type": "critical", "icon": "🚨",
            "title": f"MEB Formlar: {_acil_anom} acil mudahale gerektiren ogrenci",
            "detail": "Psikolojik yonlendirme (siddetli/acil) veya ev ziyareti (acil takip) formlari tespit edildi.",
            "action": "Rehberlik > MEB Formlar > Yonlendirme kategorisinden ilgili kayitlari inceleyin",
        })
    _psy_anom = _meb_risk_anom.get("psikolojik_yonlendirme", 0)
    _sag_anom = _meb_risk_anom.get("saglik_yonlendirme", 0)
    if _psy_anom + _sag_anom > 5:
        anomalies.append({
            "type": "warning", "icon": "🧭",
            "title": f"Yuksek yonlendirme hacmi: {_psy_anom} psikolojik + {_sag_anom} saglik",
            "detail": "Yonlendirme sayisi yuksek. Kurum ici destek mekanizmalarinin guclendrilmesi onerilir.",
            "action": "Rehberlik plani + BEP + grup calisma programi gozden gecirin",
        })

    # 7. Yabanci dil quiz ortalamasi kritik
    _yd_anom = data.get("yd_sinav", {})
    _yd_avg_anom = _yd_anom.get("avg_score", 0)
    if _yd_avg_anom > 0 and _yd_avg_anom < 40:
        anomalies.append({
            "type": "critical", "icon": "🌍",
            "title": f"Yabanci dil ortalamasi kritik: {_yd_avg_anom:.1f}",
            "detail": f"{_yd_anom.get('total_results', 0)} sinav sonucunun genel ortalamasi %40'in altinda. "
                      f"Acil mudahale gereklidir.",
            "action": "Yabanci Dil > Unite Quiz'den pekistirme quizleri olusturun, SRS kelime tekrari aktiflestirilmeli",
        })

    # 8. CEFR + quiz uyumsuzlugu
    _cefr_anom = data.get("cefr", {})
    if _yd_anom.get("total_results", 0) > 0 and _safe_len(_cefr_anom.get("results", [])) == 0 and stu_cnt > 10:
        anomalies.append({
            "type": "info", "icon": "🌐",
            "title": "YD quiz var ama CEFR tespiti yapilmamis",
            "detail": f"{_yd_anom.get('total_results', 0)} quiz sonucu mevcut ancak CEFR seviye tespiti "
                      f"hicbir ogrenciye uygulanmamis. Bireysel seviye takibi icin CEFR gerekli.",
            "action": "Yabanci Dil > CEFR Seviye Tespit Sinavi'ndan tum ogrencilere sinav uygulatin",
        })

    return anomalies


def _render_anomalies(anomalies: list[dict]):
    """Anomali kartlarini render et — tip bazli renk kodlu."""
    if not anomalies:
        return
    st.markdown("#### Akilli Anomali Tespiti")
    for a in anomalies:
        bg = {"critical": "linear-gradient(135deg,#450a0a,#7f1d1d)",
              "warning": "linear-gradient(135deg,#422006,#78350f)",
              "info": "linear-gradient(135deg,#0c1929,#1e3a5f)"}.get(a["type"], "linear-gradient(135deg,#0f172a,#1e293b)")
        border = {"critical": "rgba(239,68,68,0.4)", "warning": "rgba(245,158,11,0.4)",
                  "info": "rgba(59,130,246,0.3)"}.get(a["type"], "rgba(99,102,241,0.2)")
        title_c = {"critical": "#fca5a5", "warning": "#fcd34d", "info": "#93c5fd"}.get(a["type"], "#c7d2fe")
        detail_c = {"critical": "#fecaca", "warning": "#fef3c7", "info": "#dbeafe"}.get(a["type"], "#e2e8f0")

        st.markdown(f"""
        <div style="background:{bg};border-radius:12px;padding:14px 18px;margin:6px 0;
        border:1px solid {border};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
        <div style="font-size:.95rem;font-weight:700;color:{title_c};">{a['icon']} {a['title']}</div>
        <div style="font-size:.8rem;color:{detail_c};margin-top:3px;">{a['detail']}</div>
        </div>
        </div>
        <div style="margin-top:8px;padding:6px 12px;background:rgba(0,0,0,0.2);border-radius:8px;
        font-size:.78rem;color:#a5b4fc;">
        Aksiyon: {a['action']}</div>
        </div>""", unsafe_allow_html=True)


def _hero_banner(data: dict):
    """Animated hero KPI banner — executive dashboard en ust."""
    ak = data.get("akademik", {})
    ik = data.get("ik", {})
    bu = data.get("butce", {})
    eu = data.get("erken_uyari", {})
    od = data.get("olcme", {})

    stu = ak.get("students_aktif", 0)
    tch = ak.get("teachers_count", 0)
    emp = ik.get("employees_aktif", 0)
    net = bu.get("toplam_gelir", 0) - bu.get("toplam_gider", 0)
    risk_high = sum(1 for r in eu.get("risks", []) if r.get("risk_level") in ("HIGH", "CRITICAL"))
    q_count = od.get("questions_count", 0)

    st.markdown(f"""
    <style>
    @keyframes countUp {{ from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }} }}
    .hero-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin: 16px 0; }}
    .hero-card {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 16px; padding: 20px 16px; text-align: center;
    border: 1px solid rgba(99,102,241,0.15);
    animation: countUp 0.6s ease-out; position: relative; overflow: hidden; }}
    .hero-card::after {{ content: ''; position: absolute; top: -50%; right: -50%;
    width: 100%; height: 100%; background: radial-gradient(circle, rgba(99,102,241,0.06) 0%, transparent 70%);
    pointer-events: none; }}
    .hero-num {{ font-size: 2rem; font-weight: 900; letter-spacing: -1px;
    background: linear-gradient(135deg, #c7d2fe, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .hero-label {{ font-size: 0.72rem; color: #64748b; margin-top: 4px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px; }}
    .hero-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}
    .hero-card.alert {{ border-color: rgba(239,68,68,0.3); }}
    .hero-card.alert .hero-num {{ background: linear-gradient(135deg, #fca5a5, #ef4444);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .hero-card.money {{ border-color: rgba(16,185,129,0.3); }}
    .hero-card.money .hero-num {{ background: linear-gradient(135deg, #6ee7b7, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
    <div class="hero-grid">
    <div class="hero-card"><div class="hero-icon">🎓</div>
    <div class="hero-num">{stu}</div><div class="hero-label">Aktif Ogrenci</div></div>
    <div class="hero-card"><div class="hero-icon">👨‍🏫</div>
    <div class="hero-num">{tch}</div><div class="hero-label">Ogretmen</div></div>
    <div class="hero-card"><div class="hero-icon">👥</div>
    <div class="hero-num">{emp}</div><div class="hero-label">Personel</div></div>
    <div class="hero-card money"><div class="hero-icon">💰</div>
    <div class="hero-num">{net:,.0f}</div><div class="hero-label">Net Bakiye (TL)</div></div>
    <div class="hero-card {'alert' if risk_high > 5 else ''}"><div class="hero-icon">⚠️</div>
    <div class="hero-num">{risk_high}</div><div class="hero-label">Yuksek Risk</div></div>
    <div class="hero-card"><div class="hero-icon">❓</div>
    <div class="hero-num">{q_count:,}</div><div class="hero-label">Soru Bankasi</div></div>
    </div>""", unsafe_allow_html=True)


def _critical_alerts(data: dict):
    """Acil dikkat gerektiren uyarilar — kirmizi banner."""
    alerts = []
    # Stok kritik
    for u in data.get("tdm", {}).get("urunler", []):
        stok = u.get("stok", 0)
        min_stok = u.get("min_stok", 0)
        if isinstance(stok, (int, float)) and isinstance(min_stok, (int, float)):
            if stok < min_stok and min_stok > 0:
                alerts.append(f"📦 Kritik Stok: {u.get('urun_adi', '?')} — {stok}/{min_stok}")

    # Yuksek riskli ogrenci
    risk_critical = [r for r in data.get("erken_uyari", {}).get("risks", [])
                     if r.get("risk_level") == "CRITICAL"]
    if risk_critical:
        alerts.append(f"🔴 {len(risk_critical)} ogrenci KRiTiK risk seviyesinde!")

    # Acik destek talebi
    open_t = sum(1 for t in data.get("destek", {}).get("tickets", [])
                 if t.get("durum") in ("acik", "beklemede"))
    if open_t > 0:
        alerts.append(f"🔧 {open_t} acik destek talebi bekliyor")

    # Ozursuz devamsizlik yuksek
    att = data.get("akademik", {}).get("attendance", [])
    ozursuz = sum(1 for a in att if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
    if ozursuz > 20:
        alerts.append(f"📋 {ozursuz} ozursuz devamsizlik kaydi — takip gerekiyor")

    if alerts:
        alerts_html = "".join(f"<div style='padding:4px 0;'>• {a}</div>" for a in alerts[:6])
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#450a0a,#7f1d1d);border-radius:14px;
        padding:16px 20px;margin:12px 0;border:1.5px solid rgba(239,68,68,0.4);">
        <div style="font-size:1rem;font-weight:800;color:#fca5a5;margin-bottom:6px;">
        🚨 Acil Dikkat Gerektiren Konular ({len(alerts)})</div>
        <div style="color:#fecaca;font-size:.85rem;">{alerts_html}</div>
        </div>""", unsafe_allow_html=True)


def _render_tab_panorama(data: dict):
    styled_section("Kurum Genel Bakis — Tum Moduller", "#6366f1")

    # ── KURUM RONTGENI — 19 MOTOR BILESIK (cache'li) ──
    _rk = "_ai_rontgen_cache"
    if _rk not in st.session_state:
        with st.spinner("Kurum analizi yapiliyor..."):
            st.session_state[_rk] = _kurum_rontgeni(data)
    rontgen = st.session_state[_rk]
    _render_kurum_rontgeni(rontgen)

    # ── KURUM DNA (cache'li) ──
    _dk = "_ai_dna_cache"
    if _dk not in st.session_state:
        st.session_state[_dk] = _kurum_dna(data)
    dna = st.session_state[_dk]
    with st.expander(f"🧬 Kurum DNA — {dna['guclu_cnt']} guclu gen, {dna['zayif_cnt']} zayif gen, "
                      f"%{dna['mutasyon']:.0f} mutasyon potansiyeli", expanded=False):
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.markdown("##### 🟢 Guclu Genler")
            for g in dna["guclu"]:
                st.markdown(f"- **{g['gen']}** (%{g['skor']:.0f})")
            if not dna["guclu"]:
                st.info("Henuz guclu gen tanimlanamadi.")
        with dc2:
            st.markdown("##### 🔴 Zayif Genler")
            for z in dna["zayif"]:
                st.markdown(f"- **{z['gen']}** (%{z['skor']:.0f})")
            if not dna["zayif"]:
                st.success("Zayif gen yok — tum alanlar %30+")
        with dc3:
            st.markdown("##### 🧬 Kurum Karakteri")
            st.markdown(f"**{dna['karakter']}**")
            st.markdown(f"Mutasyon Potansiyeli: **%{dna['mutasyon']:.0f}**")
            st.caption("Tum gap'ler kapatildiginda kazanilacak skor artisi")

    # ── GUNLUK ONERILER ──
    daily_recs = _smart_daily_recommendations(data, "Yonetici")
    _render_daily_recommendations(daily_recs)

    # ── EXECUTIVE SUMMARY — AI otomatik 3 cumle ──
    try:
        client = _get_client()
        summary = _auto_executive_summary(client, data)
        if summary:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);border-radius:16px;
            padding:20px 24px;margin-bottom:16px;border:1.5px solid rgba(99,102,241,0.3);">
            <div style="font-size:.78rem;color:#818cf8;font-weight:700;letter-spacing:1px;
            text-transform:uppercase;margin-bottom:8px;">AI Executive Summary</div>
            <div style="font-size:.95rem;color:#e2e8f0;line-height:1.6;">{summary}</div>
            </div>""", unsafe_allow_html=True)
    except Exception:
        pass

    # HERO BANNER
    _hero_banner(data)

    # ANOMALY DETECTION
    anomalies = _anomaly_detection(data)
    _render_anomalies(anomalies)

    # CRITICAL ALERTS
    _critical_alerts(data)

    # ── DERIN ANALIZ (cache'li) ──
    _dak = "_ai_deep_cache"
    if _dak not in st.session_state:
        st.session_state[_dak] = _deep_rule_analysis(data)
    analysis = st.session_state[_dak]
    with st.expander(f"🧠 Derin Analiz — {len(analysis['findings'])} Bulgu, "
                      f"{len(analysis['roadmap'])} Aksiyon, "
                      f"{len(analysis['cross_insights'])} Cross-Insight", expanded=True):
        _render_deep_analysis(analysis)

    # ── GAP ANALIZI — OLMASI GEREKEN vs MEVCUT (cache'li) ──
    st.markdown("---")
    _gk = "_ai_gap_cache"
    if _gk not in st.session_state:
        st.session_state[_gk] = _gap_analysis(data)
    gaps = st.session_state[_gk]
    _render_gap_analysis(gaps)
    st.markdown("---")

    # ── KURUM ENDEKSI ──
    idx = _institution_index(data)
    _render_institution_index(idx)

    # ── GELECEK PROJEKSIYONU ──
    st.markdown("#### 3 Ay Sonra — Senaryo Analizi")
    proj = _projection_model(data)
    _render_projection(proj)

    # ── MALIYET-FAYDA ANALIZI ──
    with st.expander("💰 Maliyet-Fayda Analizi — Her Aksiyonun ROI'si", expanded=False):
        cb = _cost_benefit_analysis(data)
        _render_cost_benefit(cb)

    # ── VELI ILETISIM ONCELIK ──
    with st.expander("📞 Veli Iletisim Oncelik Siralamasi", expanded=False):
        parents = _parent_priority_list(data)
        _render_parent_priority(parents)

    # ── MODUL AKTIVITE SKORU ──
    with st.expander("📊 Modul Aktivite Skoru — Detayli Kullanim Analizi", expanded=False):
        mod_scores = _module_activity_score(data)
        for m in mod_scores:
            fill = min(100, m["skor"])
            st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:4px 0;
            border-bottom:1px solid #1e293b;">
            <span style="width:160px;color:#c7d2fe;font-weight:600;font-size:.82rem;">{m['modul']}</span>
            <div style="flex:1;background:#1e293b;border-radius:4px;height:8px;overflow:hidden;">
            <div style="width:{fill}%;height:100%;background:{m['color']};border-radius:4px;"></div></div>
            <span style="width:35px;text-align:right;color:{m['color']};font-weight:700;font-size:.82rem;">{m['skor']}</span>
            <span style="width:55px;font-size:.7rem;color:#475569;">{m['seviye']}</span>
            <span style="width:50px;font-size:.7rem;color:#64748b;">{m['kayit']} kayit</span>
            </div>""", unsafe_allow_html=True)

    # ── HEDEF TAKIP MOTORU ──
    with st.expander("🎯 Kurum Hedef Takip Motoru — 10 Hedef", expanded=False):
        tracker = _goal_tracker(data)
        _render_goal_tracker(tracker)

    # ── OGRENCI SEGMENTASYONU ──
    segments = _student_segmentation(data)
    total_seg = sum(len(v) for v in segments.values())
    if total_seg > 0:
        st.markdown("#### Ogrenci Segmentasyonu")
        _render_segmentation(segments)

    # ── HAFTALIK AKSIYON PLANI ──
    weekly = _weekly_action_plan(data, "Yonetici")
    _render_weekly_plan(weekly)

    # ── SINIF KARSILASTIRMA ──
    class_comp = _class_comparison(data)
    if class_comp and len(class_comp) > 1:
        with st.expander(f"📊 Sinif Karsilastirma Tablosu ({len(class_comp)} sinif)", expanded=False):
            import pandas as pd
            df_cc = pd.DataFrame(class_comp)
            st.dataframe(df_cc, use_container_width=True)
            best = class_comp[0]
            worst = class_comp[-1]
            st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:12px;margin-top:8px;">
            <span style="color:#22c55e;font-weight:700;">En Basarili: {best['sinif']} (ort {best['ort']})</span> |
            <span style="color:#ef4444;font-weight:700;">En Dusuk: {worst['sinif']} (ort {worst['ort']})</span> |
            <span style="color:#94a3b8;">Fark: {best['ort'] - worst['ort']:.1f} puan</span>
            </div>""", unsafe_allow_html=True)

    # ── OGRETMEN ETKINLIK ──
    tch_eff = _teacher_effectiveness(data)
    if tch_eff:
        with st.expander(f"👨‍🏫 Ogretmen Etkinlik Skoru ({len(tch_eff)} ogretmen)", expanded=False):
            for t in tch_eff:
                clr = "#22c55e" if t["skor"] >= 70 else ("#f59e0b" if t["skor"] >= 55 else "#ef4444")
                st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;padding:6px 0;
                border-bottom:1px solid #1e293b;">
                <span style="color:#c7d2fe;flex:1;font-weight:600;">{t['ogretmen']}</span>
                <span style="color:#94a3b8;font-size:.8rem;">{t['brans']}</span>
                <span style="color:{clr};font-weight:800;font-size:1.1rem;">{t['skor']}</span>
                <span style="color:#64748b;font-size:.7rem;">{t['durum']}</span>
                </div>""", unsafe_allow_html=True)

    # ── OGRENCI POTANSIYEL ANALIZI ──
    potentials = _student_potential_analysis(data)
    if potentials:
        with st.expander(f"⚡ Potansiyel Analizi — {len(potentials)} ogrenci kapasitesinin altinda", expanded=False):
            for p in potentials[:10]:
                st.markdown(f"""<div style="background:#0f172a;border-left:3px solid #f59e0b;
                border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;">
                <div style="color:#fcd34d;font-weight:700;">{p['ad']} — {p['fark']:.0f} puan fark</div>
                <div style="color:#94a3b8;font-size:.82rem;margin-top:2px;">{p['yorum']}</div>
                <div style="color:#64748b;font-size:.75rem;">En iyi: {p['en_iyi']} | En kotu: {p['en_kotu']}</div>
                </div>""", unsafe_allow_html=True)

    # ── KURUM SKOR PANELİ ──
    inst_score = _compute_institution_score(data)
    overall = inst_score["overall"]
    score_color = "#22c55e" if overall >= 70 else ("#f59e0b" if overall >= 40 else "#ef4444")

    gs1, gs2 = st.columns([1, 2])
    with gs1:
        _gauge(overall, 100, "Kurum Saglik Skoru", score_color)
    with gs2:
        # Radar chart — 7 boyutlu kurum skoru
        categories = list(inst_score["scores"].keys())
        values = list(inst_score["scores"].values())
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba({int(score_color[1:3],16)},{int(score_color[3:5],16)},{int(score_color[5:7],16)},0.12)",
            line=dict(color=score_color, width=2),
            marker=dict(size=6, color=score_color),
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                                gridcolor="#1e293b"),
                angularaxis=dict(tickfont=dict(size=10, color="#94a3b8"),
                                 gridcolor="#1e293b"),
                bgcolor="rgba(0,0,0,0)",
            ),
            showlegend=False,
            margin=dict(l=60, r=60, t=20, b=20),
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # Skor kartlari — 7 boyut yan yana
    score_icons = {"Akademik Kadro": "🎓", "Olcme Degerlendirme": "📝",
                   "Insan Kaynaklari": "👥", "Mali Durum": "💰",
                   "Operasyonel": "🔧", "Risk Yonetimi": "⚠️", "Veri Kapsami": "📊"}
    score_colors = {"Akademik Kadro": "#2563eb", "Olcme Degerlendirme": "#10b981",
                    "Insan Kaynaklari": "#7c3aed", "Mali Durum": "#059669",
                    "Operasyonel": "#f59e0b", "Risk Yonetimi": "#ef4444", "Veri Kapsami": "#6366f1"}
    score_cols = st.columns(len(inst_score["scores"]))
    for i, (dim, val) in enumerate(inst_score["scores"].items()):
        with score_cols[i]:
            _score_card(dim, val, 100, score_icons.get(dim, "📊"), score_colors.get(dim, "#6366f1"))

    st.markdown("---")

    ak = data.get("akademik", {})
    ik = data.get("ik", {})
    bu = data.get("butce", {})
    ds = data.get("destek", {})
    eu = data.get("erken_uyari", {})
    rh = data.get("rehberlik", {})

    # KPI Row 1
    net = bu.get("toplam_gelir", 0) - bu.get("toplam_gider", 0)
    styled_stat_row([
        ("Aktif Ogrenci", str(ak.get("students_aktif", 0)), "#2563eb", "🎓"),
        ("Ogretmen", str(ak.get("teachers_count", 0)), "#7c3aed", "👨‍🏫"),
        ("Aktif Personel", str(ik.get("employees_aktif", 0)), "#10b981", "👥"),
        ("Toplam Gelir", f"{bu.get('toplam_gelir', 0):,.0f} TL", "#059669", "💰"),
        ("Toplam Gider", f"{bu.get('toplam_gider', 0):,.0f} TL", "#ef4444", "💸"),
        ("Net Bakiye", f"{net:,.0f} TL", "#059669" if net >= 0 else "#ef4444", "📊"),
    ])

    # ── AKILLI YORUM KARTLARI ──
    st.markdown("#### Akilli Durum Degerlendirmesi")
    vc1, vc2, vc3, vc4 = st.columns(4)
    t_cnt = ak.get("teachers_count", 0)
    s_cnt = ak.get("students_aktif", 0)
    ratio = round(s_cnt / t_cnt, 1) if t_cnt > 0 else 0
    with vc1:
        _verdict_card("Ogretmen/Ogrenci", str(ratio), f"1:{ratio} oran", _TH_RATIO)
    with vc2:
        _verdict_card("Kurum Skoru", f"%{inst_score['overall']:.0f}", "puan", _TH_SCORE)
    with vc3:
        active_mod_pct = round(sum(1 for vals in data.values()
            if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0
            or any(isinstance(v, (str, dict)) and v for v in vals.values())) / max(len(data), 1) * 100)
        _verdict_card("Modul Kapsami", f"%{active_mod_pct}", "aktif", _TH_COVERAGE)
    with vc4:
        risk_high_cnt = sum(1 for r in eu.get("risks", []) if r.get("risk_level") in ("HIGH", "CRITICAL"))
        _verdict_card("Yuksek Risk", str(risk_high_cnt), "ogrenci",
                      [(0, "🏆", "#22c55e", "Mukemmel: Yuksek riskli ogrenci yok"),
                       (3, "🟡", "#f59e0b", "Dikkat: Birkac ogrenci izlenmeli"),
                       (10, "🟠", "#f97316", "Uyari: Ciddi risk grubu var"),
                       (20, "🔴", "#ef4444", "Kritik: Acil mudahale gerekli")],
                      reverse=True)

    # KPI Row 2
    open_tickets = sum(1 for t in ds.get("tickets", []) if t.get("durum") in ("acik", "beklemede", "atandi"))
    risk_high = sum(1 for r in eu.get("risks", []) if r.get("risk_level") in ("HIGH", "CRITICAL"))
    open_cases = sum(1 for v in rh.get("vakalar", []) if v.get("durum") in ("acik", "takipte"))
    active_odunc = sum(1 for o in data.get("kutuphane", {}).get("odunc", [])
                       if not o.get("iade_tarihi"))
    styled_stat_row([
        ("Acik Destek Talebi", str(open_tickets), "#f59e0b", "🔧"),
        ("Riskli Ogrenci", str(risk_high), "#ef4444", "⚠️"),
        ("Aktif Vaka", str(open_cases), "#dc2626", "📋"),
        ("Kutuphane Odunc", str(active_odunc), "#0d9488", "📚"),
    ])

    # Grafikler
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### Modul Veri Dagilimi")
        mod_labels = []
        mod_values = []
        mod_map = [
            ("Ogrenci", ak.get("students_aktif", 0)),
            ("Not Kaydi", _safe_len(ak.get("grades", []))),
            ("Devamsizlik", _safe_len(ak.get("attendance", []))),
            ("Sinav Sonucu", _safe_len(data.get("olcme", {}).get("results", []))),
            ("Soru Bankasi", data.get("olcme", {}).get("questions_count", 0)),
            ("Personel", ik.get("employees_aktif", 0)),
            ("Rehberlik", _safe_len(rh.get("gorusmeler", []))),
            ("Destek Talep", _safe_len(ds.get("tickets", []))),
            ("Toplanti", _safe_len(data.get("toplanti", {}).get("meetings", []))),
            ("Etkinlik", _safe_len(data.get("sosyal", {}).get("etkinlikler", []))),
        ]
        for lbl, val in mod_map:
            if val > 0:
                mod_labels.append(lbl)
                mod_values.append(val)
        total_records = sum(mod_values)
        _donut(mod_labels, mod_values,
               center=f"<b>{total_records}</b><br><span style='font-size:10px;color:#64748b'>Toplam Kayit</span>")

    with ch2:
        st.markdown("#### Sinif Mevcutlari")
        sinif_counts: dict[str, int] = {}
        for s in ak.get("students", []):
            sinif = getattr(s, "sinif", None) or s.get("sinif", "") if isinstance(s, dict) else getattr(s, "sinif", "")
            sube = getattr(s, "sube", None) or s.get("sube", "") if isinstance(s, dict) else getattr(s, "sube", "")
            durum = getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")
            if durum == "aktif":
                key = f"{sinif}/{sube}"
                sinif_counts[key] = sinif_counts.get(key, 0) + 1
        if sinif_counts:
            sorted_items = sorted(sinif_counts.items())
            _bar([k for k, _ in sorted_items], [v for _, v in sorted_items],
                 colors=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(sorted_items))])

    # Butce donut + Personel dagilimi
    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown("#### Butce Ozeti")
        g, gi = bu.get("toplam_gelir", 0), bu.get("toplam_gider", 0)
        if g > 0 or gi > 0:
            _donut(["Gelir", "Gider"], [g, gi], ["#10b981", "#ef4444"],
                   center=f"<b>{net:,.0f}</b><br><span style='font-size:10px;color:#64748b'>Net TL</span>")

    with ch4:
        st.markdown("#### 18 Modul Saglik Tablosu")
        all_mods = [
            ("Akademik Takip", ak.get("students_aktif", 0), "Ogrenci, ogretmen, not, devamsizlik"),
            ("Olcme Degerlendirme", data.get("olcme", {}).get("questions_count", 0), "Soru bankasi, sinav, telafi"),
            ("Insan Kaynaklari", ik.get("employees_aktif", 0), "Personel, pozisyon, performans"),
            ("Rehberlik", _safe_len(rh.get("gorusmeler", [])), "Gorusme, vaka, BEP"),
            ("Okul Sagligi", _safe_len(data.get("saglik", {}).get("revir", [])), "Revir, kaza, ilac"),
            ("Butce Gelir Gider", _safe_len(bu.get("gelir", [])) + _safe_len(bu.get("gider", [])), "Gelir, gider, plan"),
            ("Tuketim Demirbas", _safe_len(data.get("tdm", {}).get("urunler", [])), "Stok, demirbas, satin alma"),
            ("Toplanti Kurullar", _safe_len(data.get("toplanti", {}).get("meetings", [])), "Toplanti, karar, gorev"),
            ("Sosyal Etkinlik", _safe_len(data.get("sosyal", {}).get("kulupler", [])), "Kulup, etkinlik"),
            ("Destek Hizmetleri", _safe_len(ds.get("tickets", [])), "Talep, periyodik, bakim"),
            ("Randevu Ziyaretci", _safe_len(data.get("randevu", {}).get("randevular", [])), "Randevu, ziyaret"),
            ("Sivil Savunma ISG", _safe_len(data.get("ssg", {}).get("tatbikat", [])), "Tatbikat, risk, denetim"),
            ("Kutuphane", _safe_len(data.get("kutuphane", {}).get("materyaller", [])), "Materyal, odunc"),
            ("Dijital Kutuphane", _safe_len(data.get("dijital_kutuphane", {}).get("kaynaklar", [])), "Dijital kaynak"),
            ("Egitim Koclugu", _safe_len(data.get("egitim_koclugu", {}).get("ogrenciler", [])), "Ogrenci, gorusme, hedef"),
            ("Erken Uyari", _safe_len(eu.get("risks", [])), "Risk kaydi, uyari"),
            ("Kayit Modulu", _safe_len(data.get("kayit", {}).get("adaylar", [])), "Aday pipeline"),
            ("CEFR Placement", _safe_len(data.get("cefr", {}).get("results", [])), "Seviye tespit sinav/sonuc"),
            ("Kurumsal Org (KOI)", 1 if data.get("koi", {}).get("kurum_adi") else 0, "Kurum profili, organizasyon"),
            ("Halkla Iliskiler", _safe_len(data.get("halkla_iliskiler", {}).get("sozlesmeler", [])), "Sozlesme, aday, kampanya"),
            ("Sosyal Medya", _safe_len(data.get("sosyal_medya", {}).get("hesaplar", [])), "Hesap, paylasim"),
            ("Kurum Hizmetleri", len(data.get("kurum_hizmetleri", {})), "Yemek, servis, duyuru"),
            ("Kullanici Yonetimi", data.get("kullanici", {}).get("total", 0), "Kullanici, rol, yetki"),
            ("Mezunlar", _safe_len(data.get("mezunlar", {}).get("mezunlar", [])), "Mezun havuzu, kariyer"),
            ("Yabanci Dil", 1, "Ders isleme, CEFR, kitap uretici"),
            ("Okul Oncesi-Ilkokul", 1, "Gunluk bulten, ilkokul rapor"),
            ("AI Bireysel Egitim", 1, "Adaptif ogrenme"),
            ("AI Treni", 1, "Bilgi treni, ogrenme oyunlari"),
            ("Matematik Koyu", 1, "Matematik oyun, alistirma"),
            ("Sanat Sokagi", 1, "Sanat etkinlikleri, sergi"),
            ("Bilisim Vadisi", 1, "Kodlama, robotik"),
            ("Kisisel Dil Gelisimi", 1, "Bireysel dil ogrenme, SRS"),
            ("Yonetim Tek Ekran", 1, "Yonetici KPI dashboard"),
            ("Kurum Yonetimi", 1, "Sistem ayarlari, tenant"),
            ("Akademik Takvim", 1, "Egitim takvimi, tatiller"),
        ]
        for name, count, desc in all_mods:
            if count > 0:
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
                <span style="color:#22c55e;">🟢</span>
                <span style="color:#e2e8f0;font-weight:600;width:160px;font-size:.82rem;">{name}</span>
                <span style="color:#818cf8;font-weight:700;width:50px;text-align:right;">{count}</span>
                <span style="color:#475569;font-size:.72rem;margin-left:8px;">{desc}</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:3px 0;opacity:0.6;">
                <span style="color:#ef4444;">🔴</span>
                <span style="color:#94a3b8;font-weight:600;width:160px;font-size:.82rem;">{name}</span>
                <span style="color:#64748b;font-weight:700;width:50px;text-align:right;">0</span>
                <span style="color:#475569;font-size:.72rem;margin-left:8px;">{desc}</span>
                </div>""", unsafe_allow_html=True)

    # ── Kritik Metrikler ──
    st.markdown("---")
    st.markdown("#### Kritik Performans Metrikleri")
    mc1, mc2, mc3, mc4 = st.columns(4)

    with mc1:
        # Ogretmen-Ogrenci Orani
        t_count = ak.get("teachers_count", 0)
        s_count = ak.get("students_aktif", 0)
        ratio = round(s_count / t_count, 1) if t_count > 0 else 0
        ideal = "iyi" if ratio <= 15 else ("orta" if ratio <= 25 else "yuksek")
        r_color = "#22c55e" if ratio <= 15 else ("#f59e0b" if ratio <= 25 else "#ef4444")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid {r_color}30;">
        <div style="font-size:.75rem;color:#94a3b8;">Ogretmen/Ogrenci Orani</div>
        <div style="font-size:1.8rem;font-weight:800;color:{r_color};">1:{ratio}</div>
        <div style="font-size:.7rem;color:#64748b;">Durum: {ideal}</div>
        </div>""", unsafe_allow_html=True)

    with mc2:
        # Devamsizlik Orani
        att = ak.get("attendance", [])
        ozursuz = sum(1 for a in att if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
        att_rate = round(ozursuz / s_count * 100, 1) if s_count > 0 else 0
        a_color = "#22c55e" if att_rate < 5 else ("#f59e0b" if att_rate < 15 else "#ef4444")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid {a_color}30;">
        <div style="font-size:.75rem;color:#94a3b8;">Ozursuz Devamsizlik Orani</div>
        <div style="font-size:1.8rem;font-weight:800;color:{a_color};">%{att_rate}</div>
        <div style="font-size:.7rem;color:#64748b;">{ozursuz} ozursuz / {s_count} ogrenci</div>
        </div>""", unsafe_allow_html=True)

    with mc3:
        # Odev Tamamlanma
        odevler = ak.get("odevler", [])
        odev_count = _safe_len(odevler)
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid #6366f130;">
        <div style="font-size:.75rem;color:#94a3b8;">Toplam Odev</div>
        <div style="font-size:1.8rem;font-weight:800;color:#6366f1;">{odev_count}</div>
        <div style="font-size:.7rem;color:#64748b;">Aktif odev sayisi</div>
        </div>""", unsafe_allow_html=True)

    with mc4:
        # Etut
        etut = ak.get("etut", [])
        etut_count = _safe_len(etut)
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid #0d948830;">
        <div style="font-size:.75rem;color:#94a3b8;">Etut/Destek Ders</div>
        <div style="font-size:1.8rem;font-weight:800;color:#0d9488;">{etut_count}</div>
        <div style="font-size:.7rem;color:#64748b;">Toplam etut kaydi</div>
        </div>""", unsafe_allow_html=True)

    # ── En Riskli 5 Ogrenci ──
    eu_risks = eu.get("risks", [])
    if eu_risks:
        st.markdown("#### En Riskli 5 Ogrenci")
        sorted_risks = sorted(eu_risks, key=lambda r: r.get("risk_score", 0), reverse=True)[:5]
        for i, r in enumerate(sorted_risks):
            lvl = r.get("risk_level", "LOW")
            score = r.get("risk_score", 0)
            name = r.get("student_name", "?")
            lvl_color = {"LOW": "#22c55e", "MEDIUM": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444"}.get(lvl, "#64748b")
            lvl_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}.get(lvl, "⚪")
            st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;padding:6px 12px;
            background:#0f172a;border-radius:8px;margin:3px 0;border-left:4px solid {lvl_color};">
            <span style="font-weight:700;color:#c7d2fe;width:20px;">{i+1}.</span>
            <span>{lvl_icon}</span>
            <span style="color:#e2e8f0;flex:1;">{name}</span>
            <span style="color:{lvl_color};font-weight:700;">%{score:.0f}</span>
            <span style="color:#64748b;font-size:.75rem;">{lvl}</span>
            </div>""", unsafe_allow_html=True)

    # ── Modul Veri Yogunlugu (Treemap stilinde) ──
    st.markdown("#### Modul Veri Yogunlugu")
    mod_data_map = []
    mod_names = {
        "akademik": "Akademik", "olcme": "Olcme", "ik": "IK", "rehberlik": "Rehberlik",
        "saglik": "Saglik", "butce": "Butce", "tdm": "Tuketim", "toplanti": "Toplanti",
        "sosyal": "Sosyal", "destek": "Destek", "randevu": "Randevu", "ssg": "Guvenlik",
        "kutuphane": "Kutuphane", "dijital_kutuphane": "Dijital Ktp", "egitim_koclugu": "Kocluk",
        "erken_uyari": "Erken Uyari", "kayit": "Kayit", "cefr": "CEFR",
        "koi": "KOI", "halkla_iliskiler": "Kayit/HI", "sosyal_medya": "Sos.Medya",
        "kurum_hizmetleri": "Kurum Hiz.", "kullanici": "Kullanici", "mezunlar": "Mezunlar",
    }
    for mod_key, mod_label in mod_names.items():
        vals = data.get(mod_key, {})
        total = sum(_safe_len(v) for v in vals.values() if isinstance(v, list))
        if total > 0:
            mod_data_map.append((mod_label, total))
    if mod_data_map:
        sorted_mod = sorted(mod_data_map, key=lambda x: -x[1])
        fig_tree = go.Figure(go.Treemap(
            labels=[m[0] for m in sorted_mod],
            values=[m[1] for m in sorted_mod],
            parents=[""] * len(sorted_mod),
            marker=dict(colors=SC_COLORS[:len(sorted_mod)]),
            textinfo="label+value",
            textfont=dict(size=14),
        ))
        fig_tree.update_layout(
            margin=dict(l=0, r=0, t=0, b=0), height=300,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_tree, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # Kayit Modulu Pipeline — Funnel
    ky = data.get("kayit", {})
    adaylar = ky.get("adaylar", [])
    if adaylar:
        st.markdown("#### Kayit Pipeline (Donusum Hunisi)")
        pipeline: dict[str, int] = {}
        for a in adaylar:
            asama = a.get("asama", "aday") if isinstance(a, dict) else getattr(a, "asama", "aday")
            pipeline[asama] = pipeline.get(asama, 0) + 1
        stage_order = ["aday", "arandi", "randevu", "gorusme", "fiyat_verildi", "sozlesme", "kesin_kayit"]
        stage_labels = {"aday": "Aday", "arandi": "Arandi", "randevu": "Randevu",
                        "gorusme": "Gorusme", "fiyat_verildi": "Fiyat", "sozlesme": "Sozlesme",
                        "kesin_kayit": "Kesin Kayit"}
        f_labels = [stage_labels.get(s, s) for s in stage_order if s in pipeline]
        f_vals = [pipeline[s] for s in stage_order if s in pipeline]
        if f_vals:
            fig_funnel = go.Figure(go.Funnel(
                y=f_labels, x=f_vals,
                marker=dict(color=SC_COLORS[:len(f_labels)]),
                textinfo="value+percent previous",
                textfont=dict(size=12),
            ))
            fig_funnel.update_layout(
                margin=dict(l=0, r=0, t=10, b=10), height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig_funnel, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))
        # Olumsuz ayri goster
        olumsuz = pipeline.get("olumsuz", 0)
        if olumsuz:
            st.markdown(f"<span style='color:#ef4444;font-weight:700;'>Olumsuz Kapanan: {olumsuz}</span>",
                        unsafe_allow_html=True)

    # ── Kullanici & Kurum Ozet ──
    kul = data.get("kullanici", {})
    koi = data.get("koi", {})
    hi = data.get("halkla_iliskiler", {})
    sm = data.get("sosyal_medya", {})

    kurum_adi = koi.get("kurum_adi", "")
    if kurum_adi:
        st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:10px 16px;
        margin:8px 0;border:1px solid #6366f130;text-align:center;">
        <span style="color:#818cf8;font-size:.8rem;">Kurum:</span>
        <span style="color:#c7d2fe;font-weight:700;font-size:1rem;margin-left:6px;">{kurum_adi}</span>
        </div>""", unsafe_allow_html=True)

    styled_stat_row([
        ("Sistem Kullanici", str(kul.get("total", 0)), "#6366f1", "🔑"),
        ("Sozlesme", str(_safe_len(hi.get("sozlesmeler", []))), "#10b981", "📝"),
        ("SM Hesap", str(_safe_len(sm.get("hesaplar", []))), "#ec4899", "📱"),
        ("SM Paylasim", str(_safe_len(sm.get("paylasimlar", []))), "#8b5cf6", "📤"),
    ])

    # Kullanici rol dagilimi
    role_counts = kul.get("role_counts", {})
    if role_counts:
        st.markdown("#### Kullanici Rol Dagilimi")
        _donut(list(role_counts.keys()), list(role_counts.values()),
               center=f"<b>{kul.get('total', 0)}</b><br><span style='font-size:10px;color:#64748b'>Kullanici</span>")

    # ── Indicator Kartlar — Veri Yoğunluk Özeti ──
    st.markdown("#### Modul Veri Yogunluk Gostergeleri")
    ind_data = [
        ("Ogrenci", ak.get("students_aktif", 0), 200, "🎓", "#2563eb"),
        ("Not Kaydi", _safe_len(ak.get("grades", [])), 500, "📝", "#10b981"),
        ("Soru Bankasi", data.get("olcme", {}).get("questions_count", 0), 1000, "❓", "#8b5cf6"),
        ("Personel", ik.get("employees_aktif", 0), 30, "👥", "#7c3aed"),
        ("Stok Kalem", _safe_len(data.get("tdm", {}).get("urunler", [])), 100, "📦", "#f59e0b"),
        ("Risk Kaydi", _safe_len(eu.get("risks", [])), 100, "⚠️", "#ef4444"),
    ]
    ind_cols = st.columns(len(ind_data))
    for i, (label, val, target, icon, color) in enumerate(ind_data):
        pct = min(100, round(val / target * 100)) if target > 0 else 0
        status = "Hedefte" if pct >= 80 else ("Gelisiyor" if pct >= 40 else "Baslangic")
        with ind_cols[i]:
            fig_ind = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val,
                title=dict(text=f"{icon} {label}", font=dict(size=11, color="#c7d2fe")),
                number=dict(font=dict(size=22, color=color)),
                gauge=dict(
                    axis=dict(range=[0, target], tickfont=dict(size=8, color="#475569")),
                    bar=dict(color=color),
                    bgcolor="#0f172a",
                    bordercolor="#1e293b",
                    steps=[
                        dict(range=[0, target*0.4], color="#1e293b"),
                        dict(range=[target*0.4, target*0.8], color="#1e293b"),
                    ],
                    threshold=dict(line=dict(color="#22c55e", width=2),
                                    thickness=0.8, value=target*0.8),
                ),
            ))
            fig_ind.update_layout(
                height=160, margin=dict(l=20, r=20, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig_ind, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── MODUL OLGUNLUK MODELI — Level 1-5 ──
    st.markdown("#### Modul Dijital Olgunluk Seviyesi")
    st.caption("Level 1: Kurulum | Level 2: Temel Veri | Level 3: Aktif Kullanim | "
                "Level 4: Analitik | Level 5: AI Entegre")

    def _maturity(mod_key):
        # UI-only moduller (kodu var, data store yok) — Level 3 Aktif
        if mod_key.startswith("_"):
            return 3, "Aktif"
        vals = data.get(mod_key, {})
        total = sum(_safe_len(v) for v in vals.values() if isinstance(v, list))
        extra = sum(1 for v in vals.values() if isinstance(v, (str, dict)) and v)
        if total == 0 and extra == 0: return 1, "Kurulum"
        if total < 5: return 2, "Temel Veri"
        if total < 50: return 3, "Aktif"
        if total < 500: return 4, "Analitik"
        return 5, "AI Entegre"

    mat_mods = [
        ("Akademik", "akademik"), ("Olcme", "olcme"), ("IK", "ik"),
        ("Rehberlik", "rehberlik"), ("Saglik", "saglik"), ("Butce", "butce"),
        ("TDM", "tdm"), ("Toplanti", "toplanti"), ("Sosyal", "sosyal"),
        ("Destek", "destek"), ("Randevu", "randevu"), ("Guvenlik", "ssg"),
        ("Kutuphane", "kutuphane"), ("Dijital Ktp", "dijital_kutuphane"),
        ("Kocluk", "egitim_koclugu"), ("Erken Uyari", "erken_uyari"),
        ("Kayit", "kayit"), ("CEFR", "cefr"),
        ("KOI", "koi"), ("Sos.Medya", "sosyal_medya"),
        ("Kurum Hiz.", "kurum_hizmetleri"), ("Kullanici", "kullanici"),
        ("Mezunlar", "mezunlar"), ("HI/Kayit", "halkla_iliskiler"),
        ("Yabanci Dil", "_yd_active"), ("Okul Oncesi", "_oo_active"),
        ("AI Egitim", "_ai_edu"), ("AI Treni", "_ai_treni"),
        ("Matematik", "_mat"), ("Sanat", "_sanat"),
        ("Bilisim", "_bilisim"), ("Dil Gelisim", "_dil_gel"),
        ("Yonetim", "_yonetim"), ("Ak.Takvim", "_ak_takvim"),
    ]

    mat_html = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin:8px 0;">'
    level_colors = {1: "#ef4444", 2: "#f97316", 3: "#f59e0b", 4: "#10b981", 5: "#6366f1"}
    for name, key in mat_mods:
        lvl, label = _maturity(key)
        clr = level_colors[lvl]
        dots = "●" * lvl + "○" * (5 - lvl)
        mat_html += (f'<div style="background:#0f172a;border-radius:8px;padding:8px;text-align:center;'
                     f'border:1px solid {clr}30;">'
                     f'<div style="font-size:.7rem;color:#94a3b8;">{name}</div>'
                     f'<div style="color:{clr};font-size:.85rem;letter-spacing:2px;">{dots}</div>'
                     f'<div style="font-size:.6rem;color:#475569;">L{lvl} {label}</div>'
                     f'</div>')
    mat_html += '</div>'
    st.markdown(mat_html, unsafe_allow_html=True)

    # AI mini insight — Panorama
    try:
        client = _get_client()
        _mini_ai_insight(client,
                         f"Kurum skoru %{_compute_institution_score(data)['overall']:.0f}, "
                         f"{ak.get('students_aktif', 0)} ogrenci, {ak.get('teachers_count', 0)} ogretmen, "
                         f"Net bakiye {bu.get('toplam_gelir', 0) - bu.get('toplam_gider', 0):,.0f} TL, "
                         f"{risk_high} yuksek riskli ogrenci, "
                         f"{sum(1 for u in data.get('tdm', {}).get('urunler', []) if isinstance(u.get('stok'), (int,float)) and isinstance(u.get('min_stok'), (int,float)) and u.get('stok', 0) < u.get('min_stok', 0))} kritik stok",
                         "panorama_tab")
    except Exception:
        pass

    # ── KURUMSAL ZAMAN CIZELGESI — Son Olaylar ──
    events = []
    # Toplanti
    for m in data.get("toplanti", {}).get("meetings", []):
        tarih = m.get("tarih", "")
        if tarih:
            events.append({"tarih": str(tarih)[:10], "modul": "Toplanti",
                           "olay": m.get("baslik", "?"), "icon": "📅", "color": "#6366f1"})
    # Destek
    for t in data.get("destek", {}).get("tickets", []):
        tarih = t.get("olusturma_tarihi", t.get("istenen_tarih_saat", ""))
        if tarih:
            events.append({"tarih": str(tarih)[:10], "modul": "Destek",
                           "olay": f"Talep #{t.get('ticket_no', '?')}: {t.get('aciklama', '')[:40]}",
                           "icon": "🔧", "color": "#f59e0b"})
    # Saglik
    for r in data.get("saglik", {}).get("revir", []):
        tarih = r.get("basvuru_tarihi", "")
        if tarih:
            events.append({"tarih": str(tarih)[:10], "modul": "Saglik",
                           "olay": f"{r.get('ogrenci_adi', '?')}: {r.get('sikayet', '')[:40]}",
                           "icon": "🏥", "color": "#10b981"})
    # Etkinlik
    for e in data.get("sosyal", {}).get("etkinlikler", []):
        tarih = e.get("tarih_baslangic", e.get("tarih", ""))
        if tarih:
            events.append({"tarih": str(tarih)[:10], "modul": "Etkinlik",
                           "olay": e.get("baslik", "?"), "icon": "🎉", "color": "#ec4899"})

    if events:
        sorted_events = sorted(events, key=lambda x: x["tarih"], reverse=True)[:12]
        st.markdown("#### Kurumsal Zaman Cizelgesi — Son Olaylar")
        for ev in sorted_events:
            st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;padding:6px 0;
            border-left:3px solid {ev['color']};padding-left:12px;margin:3px 0;">
            <span style="font-size:1.1rem;">{ev['icon']}</span>
            <span style="color:#475569;font-size:.75rem;width:80px;">{ev['tarih']}</span>
            <span style="color:#c7d2fe;font-size:.85rem;flex:1;">{ev['olay']}</span>
            <span style="color:#64748b;font-size:.7rem;">{ev['modul']}</span>
            </div>""", unsafe_allow_html=True)

    # CEFR Placement Ozet
    cf = data.get("cefr", {})
    cf_results = cf.get("results", [])
    if cf_results:
        st.markdown("#### CEFR Seviye Tespit Ozeti")
        cefr_dist: dict[str, int] = {}
        for r in cf_results:
            placed = r.get("placed_cefr", "?")
            cefr_dist[placed] = cefr_dist.get(placed, 0) + 1
        if cefr_dist:
            _donut(list(cefr_dist.keys()), list(cefr_dist.values()),
                   center=f"<b>{len(cf_results)}</b><br><span style='font-size:10px;color:#64748b'>Toplam</span>")

    # ═══ KURUMSAL VIZYON — Son mucize ═══
    st.markdown("---")
    try:
        client = _get_client()
        if client:
            vizyon_text = st.session_state.get("_ai_vizyon")
            if vizyon_text:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 30%,#312e81 60%,#4c1d95 100%);
                border-radius:20px;padding:28px 32px;margin:16px 0;
                border:2px solid rgba(139,92,246,0.3);position:relative;overflow:hidden;">
                <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;
                background:radial-gradient(circle,rgba(139,92,246,0.08),transparent);border-radius:50%;"></div>
                <div style="font-size:1rem;font-weight:900;color:#c4b5fd;margin-bottom:12px;
                letter-spacing:1px;">🔮 KURUMSAL VIZYON 2025-2030</div>
                <div style="color:#e2e8f0;font-size:.9rem;line-height:1.7;">{vizyon_text}</div>
                </div>""", unsafe_allow_html=True)
            else:
                if st.button("🔮 5 Yillik Kurumsal Vizyon Olustur", key="ai_vizyon_btn",
                               type="primary", use_container_width=True):
                    with st.spinner("AI kurumsal vizyon olusturuyor — 5 yillik strateji..."):
                        result = _ai_kurumsal_vizyon(client, data)
                        if result:
                            st.rerun()
                        else:
                            st.error("Vizyon olusturulamadi. OpenAI API'yi kontrol edin.")
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AKADEMİK ANALİZ
# ═══════════════════════════════════════════════════════════════════════════════

def _mini_ai_insight(client, context: str, cache_key: str):
    """Her bolume mini AI insight — tek cumle, cache'li."""
    if not client:
        return
    full_key = f"_ai_mini_{cache_key}"
    if full_key not in st.session_state:
        st.session_state[full_key] = None

    if st.session_state[full_key]:
        st.markdown(f"""<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);
        border-radius:10px;padding:10px 16px;margin:8px 0;border:1px solid rgba(139,92,246,0.2);">
        <span style="color:#a5b4fc;font-size:.82rem;">🤖 <b>AI Insight:</b> {st.session_state[full_key]}</span>
        </div>""", unsafe_allow_html=True)
    else:
        if st.button("🤖 AI Insight", key=f"btn_{full_key}", type="secondary"):
            with st.spinner("AI dusunuyor..."):
                try:
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Turkce, tek cumle, somut, aksiyona donuk. Egitim kurumu yonetici perspektifi. Emoji kullan."},
                            {"role": "user", "content": f"Bu veriyi degerlendir ve tek cumle tavsiye ver:\n{context}"},
                        ],
                        max_tokens=150, temperature=0.7,
                    )
                    st.session_state[full_key] = resp.choices[0].message.content or ""
                    st.rerun()
                except Exception:
                    pass


def _render_tab_akademik(data: dict):
    styled_section("Akademik Derinlemesine Analiz", "#2563eb")

    # Sinif filtresi
    ak = data.get("akademik", {})
    students = ak.get("students", [])
    sinif_set = sorted(set(
        str(getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", ""))
        for s in students
        if (getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")) == "aktif"
    ))
    f1, f2 = st.columns([1, 3])
    with f1:
        sinif_filter = st.selectbox("Sinif Filtre", ["Tumu"] + sinif_set, key="ak_tab_sinif")

    ak = data.get("akademik", {})
    od = data.get("olcme", {})

    odevler = ak.get("odevler", [])
    etut = ak.get("etut", [])
    styled_stat_row([
        ("Ogrenci", str(ak.get("students_aktif", 0)), "#2563eb", "🎓"),
        ("Ogretmen", str(ak.get("teachers_count", 0)), "#7c3aed", "👨‍🏫"),
        ("Not Kaydi", str(_safe_len(ak.get("grades", []))), "#10b981", "📝"),
        ("Devamsizlik", str(_safe_len(ak.get("attendance", []))), "#f59e0b", "📋"),
        ("Odev", str(_safe_len(odevler)), "#6366f1", "📓"),
        ("Sinav Sonucu", str(_safe_len(od.get("results", []))), "#ef4444", "📊"),
        ("Soru Bankasi", str(od.get("questions_count", 0)), "#0d9488", "❓"),
        ("Telafi", str(_safe_len(od.get("telafi", []))), "#dc2626", "🔄"),
    ])

    # ── Ogretmen-Ogrenci Orani + Ders Bazli Not Ozeti ──
    t_cnt = ak.get("teachers_count", 0)
    s_cnt = ak.get("students_aktif", 0)
    ratio = round(s_cnt / t_cnt, 1) if t_cnt > 0 else 0

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        r_color = "#22c55e" if ratio <= 15 else ("#f59e0b" if ratio <= 25 else "#ef4444")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid {r_color}30;">
        <div style="font-size:.75rem;color:#94a3b8;">Ogretmen/Ogrenci Orani</div>
        <div style="font-size:1.8rem;font-weight:800;color:{r_color};">1:{ratio}</div>
        </div>""", unsafe_allow_html=True)
    with mc2:
        ozursuz = sum(1 for a in ak.get("attendance", [])
                      if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid #f59e0b30;">
        <div style="font-size:.75rem;color:#94a3b8;">Ozursuz Devamsizlik</div>
        <div style="font-size:1.8rem;font-weight:800;color:#f59e0b;">{ozursuz}</div>
        </div>""", unsafe_allow_html=True)
    with mc3:
        # Genel not ortalamasi
        all_puanlar = []
        for g in ak.get("grades", []):
            try:
                p = float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0))
                all_puanlar.append(p)
            except (TypeError, ValueError):
                pass
        genel_ort = round(sum(all_puanlar) / len(all_puanlar), 1) if all_puanlar else 0
        ort_color = "#22c55e" if genel_ort >= 70 else ("#f59e0b" if genel_ort >= 50 else "#ef4444")
        st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;text-align:center;
        border:1px solid {ort_color}30;">
        <div style="font-size:.75rem;color:#94a3b8;">Genel Not Ortalamasi</div>
        <div style="font-size:1.8rem;font-weight:800;color:{ort_color};">{genel_ort}</div>
        </div>""", unsafe_allow_html=True)

    # ── Ders Bazli Detay Tablosu ──
    grades = ak.get("grades", [])
    if grades:
        st.markdown("#### Ders Bazli Not Analizi")
        ders_data: dict[str, list] = {}
        for g in grades:
            ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
            puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
            try:
                ders_data.setdefault(ders, []).append(float(puan))
            except (TypeError, ValueError):
                pass
        if ders_data:
            import pandas as pd
            df_ders = pd.DataFrame([{
                "Ders": d,
                "Not Sayisi": len(p),
                "Ortalama": round(sum(p)/len(p), 1),
                "En Dusuk": min(p),
                "En Yuksek": max(p),
                "Durum": "Basarili" if sum(p)/len(p) >= 60 else "Risk",
            } for d, p in sorted(ders_data.items())])
            st.dataframe(df_ders, use_container_width=True, height=min(250, len(df_ders)*40+50))

    # Akilli akademik verdict
    vc1, vc2, vc3 = st.columns(3)
    with vc1:
        _verdict_card("Genel Ortalama", f"{genel_ort}", "puan", _TH_SCORE)
    with vc2:
        ozursuz_cnt = sum(1 for a in ak.get("attendance", [])
                          if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
        _verdict_card("Ozursuz Devamsizlik", str(ozursuz_cnt), "gun",
                      _TH_COUNT_LOW, reverse=True)
    with vc3:
        odev_cnt = _safe_len(odevler)
        _verdict_card("Aktif Odev", str(odev_cnt), "odev",
                      [(20, "🟢", "#22c55e", "Yeterli odev yuklemesi yapiliyor"),
                       (10, "🟡", "#f59e0b", "Orta: Daha fazla odev verilebilir"),
                       (5, "🟠", "#f97316", "Az: Odev sayisi arttirilmali"),
                       (0, "🔴", "#ef4444", "Yetersiz: Odev modulu kullanilmiyor")])

    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### Not Dagilimi")
        grades = ak.get("grades", [])
        ranges = {"0-44 Basarisiz": 0, "45-54 Gecer": 0, "55-69 Orta": 0,
                  "70-84 Iyi": 0, "85-100 Pekiyi": 0}
        for g in grades:
            puan = getattr(g, "puan", None) or (g.get("puan") if isinstance(g, dict) else 0)
            try:
                p = float(puan)
            except (TypeError, ValueError):
                continue
            if p < 45: ranges["0-44 Basarisiz"] += 1
            elif p < 55: ranges["45-54 Gecer"] += 1
            elif p < 70: ranges["55-69 Orta"] += 1
            elif p < 85: ranges["70-84 Iyi"] += 1
            else: ranges["85-100 Pekiyi"] += 1
        _donut(list(ranges.keys()), list(ranges.values()),
               ["#ef4444", "#f97316", "#f59e0b", "#10b981", "#2563eb"])

    with ch2:
        st.markdown("#### Devamsizlik Dagilimi")
        att = ak.get("attendance", [])
        ozurlu = sum(1 for a in att if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozurlu")
        ozursuz = sum(1 for a in att if (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
        other = len(att) - ozurlu - ozursuz
        labels = ["Ozurlu", "Ozursuz"]
        vals = [ozurlu, ozursuz]
        if other > 0:
            labels.append("Diger")
            vals.append(other)
        _donut(labels, vals, ["#10b981", "#ef4444", "#f59e0b"])

    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown("#### Ders Bazli Not Ortalamasi")
        ders_puanlar: dict[str, list] = {}
        for g in grades:
            ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
            puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
            try:
                p = float(puan)
                if ders:
                    ders_puanlar.setdefault(ders, []).append(p)
            except (TypeError, ValueError):
                continue
        if ders_puanlar:
            sorted_ders = sorted(ders_puanlar.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)[:12]
            _bar([d for d, _ in sorted_ders],
                 [round(sum(p)/len(p), 1) for _, p in sorted_ders],
                 colors=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(sorted_ders))])

    with ch4:
        st.markdown("#### Erken Uyari Risk Dagilimi")
        eu = data.get("erken_uyari", {})
        risk_counts = {"Dusuk": 0, "Orta": 0, "Yuksek": 0, "Kritik": 0}
        for r in eu.get("risks", []):
            lvl = r.get("risk_level", "LOW")
            if lvl == "LOW": risk_counts["Dusuk"] += 1
            elif lvl == "MEDIUM": risk_counts["Orta"] += 1
            elif lvl == "HIGH": risk_counts["Yuksek"] += 1
            elif lvl == "CRITICAL": risk_counts["Kritik"] += 1
        _donut(list(risk_counts.keys()), list(risk_counts.values()),
               ["#22c55e", "#f59e0b", "#f97316", "#ef4444"])

    # Alt bolum — Sinav Sonuclari + Telafi + Soru Bankasi
    ch5, ch6 = st.columns(2)

    with ch5:
        st.markdown("#### Soru Bankasi Durumu")
        questions = od.get("questions", [])
        q_status: dict[str, int] = {}
        for q in questions:
            s = getattr(q, "status", "") if not isinstance(q, dict) else q.get("status", "draft")
            q_status[s] = q_status.get(s, 0) + 1
        if q_status:
            _donut(list(q_status.keys()), list(q_status.values()))

    with ch6:
        st.markdown("#### Telafi Gorevi Renk Bandi")
        telafi = od.get("telafi", [])
        band_counts: dict[str, int] = {}
        for t in telafi:
            band = getattr(t, "color_band", "") if not isinstance(t, dict) else t.get("color_band", "?")
            if band:
                band_counts[band] = band_counts.get(band, 0) + 1
        if band_counts:
            band_colors = {"RED": "#ef4444", "YELLOW": "#f59e0b", "GREEN": "#22c55e", "BLUE": "#3b82f6"}
            _donut(list(band_counts.keys()), list(band_counts.values()),
                   [band_colors.get(b, "#64748b") for b in band_counts.keys()])

    # ── SINIF KARNESI — Her sinifin tek kartlik ozeti ──
    students = ak.get("students", [])
    aktif_students = [s for s in students
                      if (getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")) == "aktif"]
    if sinif_filter != "Tumu":
        aktif_students = [s for s in aktif_students
                          if str(getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", "")) == sinif_filter]

    sinif_groups: dict[str, list] = {}
    for s in aktif_students:
        sinif_v = str(getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", ""))
        sube_v = str(getattr(s, "sube", "") if not isinstance(s, dict) else s.get("sube", ""))
        key = f"{sinif_v}/{sube_v}"
        sinif_groups.setdefault(key, []).append(s)

    if sinif_groups and len(sinif_groups) > 1:
        st.markdown("#### Sinif Karnesi")
        karne_cols = st.columns(min(4, len(sinif_groups)))
        for i, (key, stus) in enumerate(sorted(sinif_groups.items())):
            with karne_cols[i % min(4, len(sinif_groups))]:
                s_ids = set()
                for s in stus:
                    s_ids.add(getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", ""))

                # Sinifin notlari
                sinif_puanlar = []
                for g in grades:
                    sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
                    if sid in s_ids:
                        try:
                            sinif_puanlar.append(float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)))
                        except (TypeError, ValueError):
                            pass
                sinif_ort = round(sum(sinif_puanlar) / len(sinif_puanlar), 1) if sinif_puanlar else 0
                sinif_devamsiz = sum(1 for a in ak.get("attendance", [])
                                    if (getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")) in s_ids)
                ort_color = "#22c55e" if sinif_ort >= 70 else ("#f59e0b" if sinif_ort >= 50 else "#ef4444")

                st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:12px;
                border:1px solid {ort_color}30;margin:4px 0;">
                <div style="font-size:1rem;font-weight:800;color:#c7d2fe;">{key}</div>
                <div style="font-size:.75rem;color:#64748b;margin:2px 0;">{len(stus)} ogrenci</div>
                <div style="display:flex;justify-content:space-between;margin-top:6px;">
                <div><span style="font-size:.65rem;color:#94a3b8;">Ortalama</span><br>
                <span style="font-size:1.1rem;font-weight:700;color:{ort_color};">{sinif_ort}</span></div>
                <div><span style="font-size:.65rem;color:#94a3b8;">Not</span><br>
                <span style="font-size:1.1rem;font-weight:700;color:#818cf8;">{len(sinif_puanlar)}</span></div>
                <div><span style="font-size:.65rem;color:#94a3b8;">Devamsiz</span><br>
                <span style="font-size:1.1rem;font-weight:700;color:#f59e0b;">{sinif_devamsiz}</span></div>
                </div></div>""", unsafe_allow_html=True)

    # ── OGRETMEN ETKINLIK ANALIZI ──
    teachers = ak.get("teachers", [])
    if teachers and grades:
        st.markdown("#### Ogretmen Bazli Ogrenci Basarisi")
        st.caption("Ogretmenin bransindaki ogrenci not ortalamasi — ogretmen etkinlik gostergesi")

        # Brans → not eslestirme
        brans_puanlar: dict[str, list] = {}
        brans_ogretmen: dict[str, str] = {}
        for t in teachers:
            brans = getattr(t, "brans", "") if not isinstance(t, dict) else t.get("brans", "")
            ad = (getattr(t, "ad", "") if not isinstance(t, dict) else t.get("ad", "")) + " " + \
                 (getattr(t, "soyad", "") if not isinstance(t, dict) else t.get("soyad", ""))
            if brans:
                brans_ogretmen[brans] = ad.strip()

        for g in grades:
            ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
            puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
            try:
                brans_puanlar.setdefault(ders, []).append(float(puan))
            except (TypeError, ValueError):
                pass

        if brans_puanlar:
            ogr_data = []
            for brans, puanlar in sorted(brans_puanlar.items()):
                ogretmen = brans_ogretmen.get(brans, "-")
                ort = round(sum(puanlar) / len(puanlar), 1)
                ogr_data.append({"Brans": brans, "Ogretmen": ogretmen,
                                  "Ogrenci Ort": ort, "Not Sayisi": len(puanlar)})
            if ogr_data:
                import pandas as pd
                st.dataframe(pd.DataFrame(ogr_data), use_container_width=True,
                             height=min(250, len(ogr_data) * 40 + 50))

    # ── Devamsizlik vs Basari Korelasyonu (Scatter) ──
    if grades and ak.get("attendance"):
        st.markdown("#### Devamsizlik vs Basari Iliskisi")
        st.caption("Her nokta bir ogrenci. X=ozursuz devamsizlik, Y=not ortalamasi. "
                    "Sag ust = az devamsiz+basarili. Sol alt = cok devamsiz+basarisiz.")
        # Ogrenci bazli ozet
        stu_grade_avg: dict[str, float] = {}
        stu_att_count: dict[str, int] = {}
        stu_names_map: dict[str, str] = {}

        for g in grades:
            sid = getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")
            puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
            try:
                stu_grade_avg.setdefault(sid, []).append(float(puan)) if isinstance(stu_grade_avg.get(sid), list) else None
                if sid not in stu_grade_avg:
                    stu_grade_avg[sid] = [float(puan)]
                elif isinstance(stu_grade_avg[sid], list):
                    stu_grade_avg[sid].append(float(puan))
            except (TypeError, ValueError):
                pass

        for a in ak.get("attendance", []):
            sid = getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")
            turu = getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")
            if turu == "ozursuz":
                stu_att_count[sid] = stu_att_count.get(sid, 0) + 1

        # Isim eslestir
        for s in students:
            sid = getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "")
            ad = getattr(s, "tam_ad", "") if not isinstance(s, dict) else f"{s.get('ad','')} {s.get('soyad','')}"
            stu_names_map[sid] = ad

        scatter_ids = set(stu_grade_avg.keys()) | set(stu_att_count.keys())
        if scatter_ids:
            x_vals = []
            y_vals = []
            names = []
            for sid in scatter_ids:
                ga = stu_grade_avg.get(sid, [])
                if isinstance(ga, list) and ga:
                    avg = sum(ga) / len(ga)
                    att_c = stu_att_count.get(sid, 0)
                    x_vals.append(att_c)
                    y_vals.append(round(avg, 1))
                    names.append(stu_names_map.get(sid, sid[:8]))

            if x_vals:
                fig_scatter = go.Figure()
                fig_scatter.add_trace(go.Scatter(
                    x=x_vals, y=y_vals, mode="markers+text",
                    text=names, textposition="top center",
                    textfont=dict(size=8, color="#94a3b8"),
                    marker=dict(
                        size=12, color=y_vals,
                        colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#22c55e"]],
                        showscale=True,
                        colorbar=dict(title=dict(text="Ort", font=dict(color="#94a3b8")),
                                      tickfont=dict(color="#94a3b8")),
                    ),
                ))
                fig_scatter.update_layout(
                    height=350, margin=dict(l=50, r=20, t=20, b=50),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(title="Ozursuz Devamsizlik (gun)", gridcolor="#1e293b",
                               tickfont=dict(color="#94a3b8")),
                    yaxis=dict(title="Not Ortalamasi", gridcolor="#1e293b",
                               tickfont=dict(color="#94a3b8")),
                    font=dict(color="#94a3b8"),
                )
                st.plotly_chart(fig_scatter, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── Ogrenci Hiyerarsi — Sunburst (Kademe > Sinif > Sube) ──
    if students:
        st.markdown("#### Ogrenci Dagilimi — Hiyerarsi")
        sb_labels = ["SmartCampus"]
        sb_parents = [""]
        sb_values = [0]

        sinif_sube_counts: dict[str, dict[str, int]] = {}
        for s in students:
            durum = getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")
            if durum != "aktif":
                continue
            sinif = str(getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", ""))
            sube = str(getattr(s, "sube", "") if not isinstance(s, dict) else s.get("sube", ""))
            sinif_sube_counts.setdefault(sinif, {}).setdefault(sube, 0)
            sinif_sube_counts[sinif][sube] += 1

        for sinif, subes in sorted(sinif_sube_counts.items()):
            sinif_total = sum(subes.values())
            sb_labels.append(f"{sinif}. Sinif")
            sb_parents.append("SmartCampus")
            sb_values.append(sinif_total)
            for sube, cnt in sorted(subes.items()):
                sb_labels.append(f"{sinif}/{sube}")
                sb_parents.append(f"{sinif}. Sinif")
                sb_values.append(cnt)

        if len(sb_labels) > 1:
            fig_sun = go.Figure(go.Sunburst(
                labels=sb_labels, parents=sb_parents, values=sb_values,
                branchvalues="total",
                marker=dict(colors=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(sb_labels))]),
                textinfo="label+value",
                insidetextorientation="radial",
            ))
            fig_sun.update_layout(
                height=400, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c7d2fe"),
            )
            st.plotly_chart(fig_sun, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── Sinif Bazli Not Karsilastirma (Box Plot konsepti) ──
    st.markdown("#### Sinif Bazli Not Karsilastirma")
    sinif_grades: dict[str, list] = {}
    for g in grades:
        sinif_val = getattr(g, "sinif", "") if not isinstance(g, dict) else g.get("sinif", "")
        sube_val = getattr(g, "sube", "") if not isinstance(g, dict) else g.get("sube", "")
        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
        try:
            p = float(puan)
            key = f"{sinif_val}/{sube_val}"
            sinif_grades.setdefault(key, []).append(p)
        except (TypeError, ValueError):
            continue
    if sinif_grades:
        sorted_sg = sorted(sinif_grades.items())[:15]
        fig_box = go.Figure()
        for i, (key, puanlar) in enumerate(sorted_sg):
            fig_box.add_trace(go.Box(
                y=puanlar, name=key,
                marker_color=SC_COLORS[i % len(SC_COLORS)],
                boxmean="sd",
            ))
        fig_box.update_layout(
            showlegend=False, height=300,
            margin=dict(l=40, r=20, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#1e293b", title="Puan"),
            xaxis=dict(tickfont=dict(color="#94a3b8")),
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig_box, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── Devamsizlik Ay Bazli Trend ──
    att_all = ak.get("attendance", [])
    if att_all:
        st.markdown("#### Devamsizlik Ay Bazli Trend")
        ay_counts: dict[str, int] = {}
        for a in att_all:
            tarih = getattr(a, "tarih", "") if not isinstance(a, dict) else a.get("tarih", "")
            if tarih and len(str(tarih)) >= 7:
                ay = str(tarih)[:7]  # YYYY-MM
                ay_counts[ay] = ay_counts.get(ay, 0) + 1
        if ay_counts:
            sorted_ay = sorted(ay_counts.items())
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=[a[0] for a in sorted_ay], y=[a[1] for a in sorted_ay],
                mode="lines+markers+text", text=[str(a[1]) for a in sorted_ay],
                textposition="top center",
                line=dict(color="#ef4444", width=3),
                marker=dict(size=8, color="#ef4444"),
                fill="tozeroy", fillcolor="rgba(239,68,68,0.1)",
            ))
            fig_trend.update_layout(
                height=250, margin=dict(l=40, r=20, t=20, b=40),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
                yaxis=dict(gridcolor="#1e293b", title="Devamsizlik"),
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig_trend, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── Erken Uyari Risk Heatmap (Sinif x Risk) ──
    eu_risks = eu.get("risks", [])
    if eu_risks:
        st.markdown("#### Risk Yogunluk Haritasi (Sinif Bazli)")
        sinif_risk: dict[str, dict[str, int]] = {}
        for r in eu_risks:
            sinif = f"{r.get('sinif', '?')}/{r.get('sube', '?')}"
            lvl = r.get("risk_level", "LOW")
            sinif_risk.setdefault(sinif, {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0})
            if lvl in sinif_risk[sinif]:
                sinif_risk[sinif][lvl] += 1
        if sinif_risk:
            sorted_sinif = sorted(sinif_risk.keys())
            risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            z_data = [[sinif_risk.get(s, {}).get(l, 0) for s in sorted_sinif] for l in risk_levels]
            fig_hm = go.Figure(go.Heatmap(
                z=z_data, x=sorted_sinif, y=["Dusuk", "Orta", "Yuksek", "Kritik"],
                colorscale=[[0, "#0f172a"], [0.25, "#22c55e"], [0.5, "#f59e0b"],
                            [0.75, "#f97316"], [1, "#ef4444"]],
                text=[[str(v) for v in row] for row in z_data],
                texttemplate="%{text}", textfont=dict(size=12, color="#fff"),
                showscale=False,
            ))
            fig_hm.update_layout(
                height=200, margin=dict(l=80, r=20, t=10, b=40),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(tickfont=dict(color="#94a3b8", size=10)),
                yaxis=dict(tickfont=dict(color="#94a3b8", size=10)),
            )
            st.plotly_chart(fig_hm, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # Egitim Koclugu + Rehberlik Ozet
    ek = data.get("egitim_koclugu", {})
    rh = data.get("rehberlik", {})
    # ── PREDIKTİF RISK TAHMİNİ ──
    eu_data = data.get("erken_uyari", {})
    eu_risks = eu_data.get("risks", [])
    if eu_risks:
        # En yuksek risk skoru olanlari "potansiyel risk" olarak goster
        rising_risk = sorted(eu_risks, key=lambda r: r.get("risk_score", 0), reverse=True)[:5]
        avg_score = sum(r.get("risk_score", 0) for r in eu_risks) / len(eu_risks) if eu_risks else 0
        above_avg = [r for r in eu_risks if r.get("risk_score", 0) > avg_score * 1.3]

        if above_avg:
            st.markdown("#### Prediktif Risk Tahmini")
            st.caption(f"Kurum ortalama risk skoru: {avg_score:.1f} — Ortalamanin %30+ ustundeki ogrenciler izlenmeli")
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1c1917,#422006);border-radius:12px;
            padding:14px 18px;margin:8px 0;border:1px solid rgba(245,158,11,0.3);">
            <div style="font-size:.9rem;font-weight:700;color:#fcd34d;">
            ⚡ {len(above_avg)} ogrenci ortalamanin %30 ustunde risk tasiyor</div>
            <div style="font-size:.78rem;color:#fef3c7;margin-top:4px;">
            Bu ogrenciler icin onleyici mudahale onerilir — Erken Uyari modulunden aksiyon planlayin.</div>
            </div>""", unsafe_allow_html=True)

            # Risk radar — en yuksek 3 ogrenci
            with st.expander("📊 Yuksek Riskli Ogrenci Radar Analizi", expanded=False):
                for r in rising_risk[:3]:
                    st.markdown(f"**{r.get('student_name', '?')}** — Risk: %{r.get('risk_score', 0):.0f}")
                    cats = ["Not", "Devamsizlik", "Sinav", "Odev", "Kazanim",
                            "Rehberlik", "Saglik", "Trend", "Davranis"]
                    vals = [r.get("grade_risk", 0), r.get("attendance_risk", 0),
                            r.get("exam_risk", 0), r.get("homework_risk", 0),
                            r.get("outcome_debt_risk", 0), r.get("counseling_risk", 0),
                            r.get("health_risk", 0), r.get("trend_risk", 0),
                            r.get("behavior_risk", 0)]
                    fig_sr = go.Figure()
                    fig_sr.add_trace(go.Scatterpolar(
                        r=vals + [vals[0]], theta=cats + [cats[0]],
                        fill="toself",
                        fillcolor="rgba(239,68,68,0.15)",
                        line=dict(color="#ef4444", width=2),
                        marker=dict(size=5),
                    ))
                    fig_sr.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100],
                                            showticklabels=False, gridcolor="#1e293b"),
                            angularaxis=dict(tickfont=dict(size=9, color="#94a3b8"),
                                             gridcolor="#1e293b"),
                            bgcolor="rgba(0,0,0,0)",
                        ),
                        showlegend=False, height=250,
                        margin=dict(l=60, r=60, t=10, b=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(fig_sr, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))
                    st.markdown("---")

    # ── Ogrenci Drill-Down ──
    aktif_students = [s for s in students
                      if (getattr(s, "durum", "aktif") if not isinstance(s, dict) else s.get("durum", "aktif")) == "aktif"]
    if sinif_filter != "Tumu":
        aktif_students = [s for s in aktif_students
                          if str(getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", "")) == sinif_filter]

    if aktif_students:
        with st.expander(f"👨‍🎓 Ogrenci Detay Drill-Down ({len(aktif_students)} ogrenci)", expanded=False):
            stu_names = {}
            for s in aktif_students:
                ad = getattr(s, "tam_ad", "") if not isinstance(s, dict) else f"{s.get('ad','')} {s.get('soyad','')}"
                sid = getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "")
                sinif_v = getattr(s, "sinif", "") if not isinstance(s, dict) else s.get("sinif", "")
                sube_v = getattr(s, "sube", "") if not isinstance(s, dict) else s.get("sube", "")
                stu_names[f"{ad} — {sinif_v}/{sube_v}"] = sid

            sel_stu = st.selectbox("Ogrenci Secin", [""] + list(stu_names.keys()), key="ak_drill_stu")
            if sel_stu and sel_stu in stu_names:
                s_id = stu_names[sel_stu]
                # Bu ogrencinin notlari
                stu_grades = [g for g in grades
                              if (getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")) == s_id]
                stu_att = [a for a in ak.get("attendance", [])
                           if (getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")) == s_id]

                dc1, dc2 = st.columns(2)
                with dc1:
                    st.markdown(f"**Notlar ({len(stu_grades)}):**")
                    for g in stu_grades:
                        ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
                        puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
                        tur = getattr(g, "not_turu", "") if not isinstance(g, dict) else g.get("not_turu", "")
                        st.markdown(f"- {ders}: **{puan}** ({tur})")
                with dc2:
                    st.markdown(f"**Devamsizlik ({len(stu_att)}):**")
                    for a in stu_att:
                        tarih = getattr(a, "tarih", "") if not isinstance(a, dict) else a.get("tarih", "")
                        turu = getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")
                        st.markdown(f"- {tarih}: {turu}")
                    if not stu_att:
                        st.markdown("Devamsizlik kaydi yok.")

                # Risk bilgisi
                eu_risks = data.get("erken_uyari", {}).get("risks", [])
                stu_risk = next((r for r in eu_risks if r.get("student_id") == s_id), None)
                if stu_risk:
                    lvl = stu_risk.get("risk_level", "?")
                    sc = stu_risk.get("risk_score", 0)
                    lvl_colors = {"LOW": "#22c55e", "MEDIUM": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444"}
                    st.markdown(f"**Risk:** <span style='color:{lvl_colors.get(lvl, '#64748b')};font-weight:700'>"
                                f"{lvl} (%{sc:.0f})</span>", unsafe_allow_html=True)

    # AI mini insight
    try:
        client = _get_client()
        _mini_ai_insight(client,
                         f"83 ogrenci, {_safe_len(grades)} not, genel ort {genel_ort}, "
                         f"{_safe_len(ak.get('attendance',[]))} devamsizlik, {_safe_len(odevler)} odev",
                         "akademik_tab")
    except Exception:
        pass

    # ── ODEV ANALIZI ──
    odevler_list = ak.get("odevler", [])
    if odevler_list:
        st.markdown("#### Odev Analizi")
        odev_ders: dict[str, int] = {}
        odev_tur: dict[str, int] = {}
        for o in odevler_list:
            d = getattr(o, "ders", "") if not isinstance(o, dict) else o.get("ders", "")
            t = getattr(o, "odev_turu", "") if not isinstance(o, dict) else o.get("odev_turu", "")
            if d: odev_ders[d] = odev_ders.get(d, 0) + 1
            if t: odev_tur[t] = odev_tur.get(t, 0) + 1

        od_c1, od_c2 = st.columns(2)
        with od_c1:
            st.markdown("##### Ders Bazli Odev")
            if odev_ders:
                _bar(list(odev_ders.keys()), list(odev_ders.values()),
                     colors=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(odev_ders))])
        with od_c2:
            st.markdown("##### Odev Tur Dagilimi")
            if odev_tur:
                _donut(list(odev_tur.keys()), list(odev_tur.values()))

    # ── SAGLIK SIKAYET KATEGORI ANALIZI ──
    sg = data.get("saglik", {})
    revir = sg.get("revir", [])
    if revir:
        st.markdown("#### Revir Ziyaret Analizi")
        sikayet_kat: dict[str, int] = {}
        for r in revir:
            kat = r.get("sikayet_kategorisi", r.get("sikayet", "Diger"))
            if kat:
                sikayet_kat[kat] = sikayet_kat.get(kat, 0) + 1
        if sikayet_kat:
            sg_c1, sg_c2 = st.columns(2)
            with sg_c1:
                _donut(list(sikayet_kat.keys()), list(sikayet_kat.values()),
                       center=f"<b>{len(revir)}</b><br><span style='font-size:10px;color:#64748b'>Ziyaret</span>")
            with sg_c2:
                # Son 5 ziyaret detay
                st.markdown("##### Son Ziyaretler")
                for r in revir[-5:]:
                    tarih = r.get("basvuru_tarihi", "-")
                    ad = r.get("ogrenci_adi", "?")
                    sikayet = r.get("sikayet", "-")
                    st.markdown(f"- {tarih} | **{ad}** — {sikayet[:50]}")

    # ── ERKEN UYARI RECOMMENDATIONS (AI onerilerini goster) ──
    eu_risks = data.get("erken_uyari", {}).get("risks", [])
    all_recs = []
    for r in eu_risks:
        recs = r.get("recommendations", [])
        for rec in recs:
            if rec and rec not in all_recs:
                all_recs.append(rec)
    if all_recs:
        with st.expander(f"📋 Erken Uyari Sisteminin Otomatik Onerileri ({len(all_recs)})", expanded=False):
            for rec in all_recs[:15]:
                st.markdown(f"- {rec}")

    # ── CROSS-MODULE INSIGHT — Not vs Devamsizlik iliskisi sinif bazli ──
    if sinif_groups and grades:
        cross_data = []
        for key, stus in sinif_groups.items():
            s_ids = set(getattr(s, "id", "") if not isinstance(s, dict) else s.get("id", "") for s in stus)
            sinif_puanlar = [float(getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0))
                             for g in grades
                             if (getattr(g, "student_id", "") if not isinstance(g, dict) else g.get("student_id", "")) in s_ids]
            sinif_devamsiz = sum(1 for a in ak.get("attendance", [])
                                if (getattr(a, "student_id", "") if not isinstance(a, dict) else a.get("student_id", "")) in s_ids
                                and (getattr(a, "turu", "") if not isinstance(a, dict) else a.get("turu", "")) == "ozursuz")
            if sinif_puanlar:
                cross_data.append({"sinif": key, "ort": round(sum(sinif_puanlar)/len(sinif_puanlar), 1),
                                    "devamsiz": sinif_devamsiz, "ogrenci": len(stus)})

        if cross_data and len(cross_data) > 1:
            st.markdown("#### Cross-Module: Not Ortalamasi vs Devamsizlik (Sinif Bazli)")
            st.caption("Balon buyuklugu = ogrenci sayisi. Kirmizi = dusuk ortalama + yuksek devamsizlik.")
            fig_bubble = go.Figure()
            fig_bubble.add_trace(go.Scatter(
                x=[d["devamsiz"] for d in cross_data],
                y=[d["ort"] for d in cross_data],
                mode="markers+text",
                text=[d["sinif"] for d in cross_data],
                textposition="top center",
                textfont=dict(size=10, color="#c7d2fe"),
                marker=dict(
                    size=[max(15, d["ogrenci"] * 3) for d in cross_data],
                    color=[d["ort"] for d in cross_data],
                    colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#22c55e"]],
                    showscale=True,
                    colorbar=dict(title=dict(text="Ort", font=dict(color="#94a3b8")),
                                  tickfont=dict(color="#94a3b8")),
                    line=dict(width=1, color="#334155"),
                ),
            ))
            fig_bubble.update_layout(
                height=320, margin=dict(l=50, r=20, t=20, b=50),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="Ozursuz Devamsizlik", gridcolor="#1e293b",
                           tickfont=dict(color="#94a3b8")),
                yaxis=dict(title="Not Ortalamasi", gridcolor="#1e293b",
                           tickfont=dict(color="#94a3b8")),
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig_bubble, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    # ── DERS x OGRETMEN x BASARI MATRISI ──
    teachers_data = ak.get("teachers", [])
    if grades and teachers_data:
        st.markdown("#### Ders × Ogretmen × Basari Analizi")
        st.caption("Her dersin not ortalamasi + o dersi veren ogretmen + odev sayisi — odev-basari iliskisi")

        ders_analiz: dict[str, dict] = {}
        for g in grades:
            ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
            puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
            try:
                p = float(puan)
                if ders not in ders_analiz:
                    ders_analiz[ders] = {"puanlar": [], "ogretmen": "-", "odev": 0}
                ders_analiz[ders]["puanlar"].append(p)
            except (TypeError, ValueError):
                pass

        # Ogretmen eslestir
        brans_ogretmen = {}
        for t in teachers_data:
            brans = getattr(t, "brans", "") if not isinstance(t, dict) else t.get("brans", "")
            ad = (getattr(t, "ad", "") if not isinstance(t, dict) else t.get("ad", "")) + " " + \
                 (getattr(t, "soyad", "") if not isinstance(t, dict) else t.get("soyad", ""))
            if brans:
                brans_ogretmen[brans] = ad.strip()
        for ders in ders_analiz:
            ders_analiz[ders]["ogretmen"] = brans_ogretmen.get(ders, "-")

        # Odev eslestir
        for o in ak.get("odevler", []):
            d = getattr(o, "ders", "") if not isinstance(o, dict) else o.get("ders", "")
            if d in ders_analiz:
                ders_analiz[d]["odev"] += 1

        if ders_analiz:
            import pandas as pd
            rows = []
            for ders, info in sorted(ders_analiz.items(), key=lambda x: sum(x[1]["puanlar"])/len(x[1]["puanlar"]) if x[1]["puanlar"] else 0, reverse=True):
                p = info["puanlar"]
                ort = round(sum(p)/len(p), 1)
                color_label = "Basarili" if ort >= 75 else ("Orta" if ort >= 60 else "Risk")
                rows.append({
                    "Ders": ders, "Ogretmen": info["ogretmen"],
                    "Ortalama": ort, "Not Sayisi": len(p),
                    "Min": min(p), "Max": max(p),
                    "Odev Sayisi": info["odev"],
                    "Durum": color_label,
                })
            df_dx = pd.DataFrame(rows)
            st.dataframe(df_dx, use_container_width=True, height=min(300, len(rows)*40+50))

            # Odev-basari korelasyon yorumu
            odev_basari = [(r["Odev Sayisi"], r["Ortalama"]) for r in rows if r["Odev Sayisi"] > 0]
            if len(odev_basari) >= 2:
                en_cok_odev = max(rows, key=lambda x: x["Odev Sayisi"])
                en_az_odev = min([r for r in rows if r["Odev Sayisi"] > 0], key=lambda x: x["Odev Sayisi"])
                fark = en_cok_odev["Ortalama"] - en_az_odev["Ortalama"]
                if fark > 5:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#0c1929,#1e3a5f);
                    border-radius:10px;padding:12px 16px;margin:8px 0;border:1px solid rgba(59,130,246,0.2);">
                    <span style="color:#93c5fd;font-size:.85rem;">
                    📊 <b>Korelasyon:</b> {en_cok_odev['Ders']} ({en_cok_odev['Odev Sayisi']} odev → ort {en_cok_odev['Ortalama']}) vs
                    {en_az_odev['Ders']} ({en_az_odev['Odev Sayisi']} odev → ort {en_az_odev['Ortalama']}).
                    Odev sayisi yuksek olan derste {fark:.0f} puan daha yuksek basari. Odev vermeye devam edin!</span>
                    </div>""", unsafe_allow_html=True)

    # ── RISK FAKTOR ANALIZI ──
    eu_data = data.get("erken_uyari", {})
    eu_risks = eu_data.get("risks", [])
    if eu_risks:
        st.markdown("#### Risk Faktor Dagilim Analizi")
        st.caption("Tum ogrencilerin risk faktor ortalamasi — hangi alan en yuksek risk tasiyor?")

        faktorler = [
            ("Not Riski", "grade_risk", "#ef4444"),
            ("Devamsizlik", "attendance_risk", "#f97316"),
            ("Sinav", "exam_risk", "#f59e0b"),
            ("Odev", "homework_risk", "#eab308"),
            ("Kazanim Borcu", "outcome_debt_risk", "#84cc16"),
            ("Rehberlik", "counseling_risk", "#22c55e"),
            ("Saglik", "health_risk", "#06b6d4"),
            ("Trend", "trend_risk", "#6366f1"),
            ("Davranis", "behavior_risk", "#8b5cf6"),
        ]

        f_avgs = []
        for label, key, color in faktorler:
            vals = [r.get(key, 0) for r in eu_risks]
            avg = round(sum(vals) / len(vals), 1) if vals else 0
            mx = max(vals) if vals else 0
            f_avgs.append({"label": label, "avg": avg, "max": mx, "color": color})

        # Bar chart — risk faktor ortalama
        fig_rf = go.Figure()
        fig_rf.add_trace(go.Bar(
            x=[f["label"] for f in f_avgs],
            y=[f["avg"] for f in f_avgs],
            marker_color=[f["color"] for f in f_avgs],
            text=[f"{f['avg']:.0f}" for f in f_avgs],
            textposition="auto",
        ))
        fig_rf.update_layout(
            height=280, margin=dict(l=40, r=20, t=20, b=60),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[0, 100], gridcolor="#1e293b", tickfont=dict(color="#94a3b8"),
                       title="Risk Skoru (0-100)"),
            xaxis=dict(tickfont=dict(color="#c7d2fe", size=9), tickangle=-30),
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig_rf, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

        # Yorum
        en_yuksek = max(f_avgs, key=lambda x: x["avg"])
        en_dusuk = min(f_avgs, key=lambda x: x["avg"])
        st.markdown(f"""<div style="background:linear-gradient(135deg,#1c0505,#3b0f0f);
        border-radius:10px;padding:12px 16px;margin:4px 0;border:1px solid rgba(239,68,68,0.2);">
        <span style="color:#fca5a5;font-size:.85rem;">
        🎯 <b>En yuksek risk faktoru:</b> {en_yuksek['label']} (ort %{en_yuksek['avg']:.0f}, max %{en_yuksek['max']:.0f})
        — Bu alanda oncelikli iyilestirme gerekiyor.</span></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:linear-gradient(135deg,#052e16,#14532d);
        border-radius:10px;padding:12px 16px;margin:4px 0;border:1px solid rgba(34,197,94,0.2);">
        <span style="color:#86efac;font-size:.85rem;">
        ✅ <b>En dusuk risk faktoru:</b> {en_dusuk['label']} (ort %{en_dusuk['avg']:.0f})
        — Bu alan kontrol altinda.</span></div>""", unsafe_allow_html=True)

        # Dengesizlik uyarisi
        fark = en_yuksek["avg"] - en_dusuk["avg"]
        if fark > 30:
            st.markdown(f"""<div style="background:linear-gradient(135deg,#422006,#78350f);
            border-radius:10px;padding:12px 16px;margin:4px 0;border:1px solid rgba(245,158,11,0.3);">
            <span style="color:#fcd34d;font-size:.85rem;">
            ⚠️ <b>Risk Dengesizligi:</b> En yuksek ({en_yuksek['label']} %{en_yuksek['avg']:.0f}) ile
            en dusuk ({en_dusuk['label']} %{en_dusuk['avg']:.0f}) arasinda {fark:.0f} puan fark var.
            Bu dengesizlik bazi alanlarin ihmal edildigini gosterir.</span></div>""", unsafe_allow_html=True)

    # ── DERS KORELASYON ──
    corr = _subject_correlation(data)
    if corr:
        with st.expander(f"🔗 Ders-Ders Korelasyon Analizi ({len(corr)} cift)", expanded=False):
            st.caption("Ayni ogrencinin farkli derslerdeki basarisi arasindaki iliski")
            import pandas as pd
            df_corr = pd.DataFrame(corr)
            st.dataframe(df_corr, use_container_width=True)
            # Yorum
            if corr:
                max_fark = corr[0]
                st.markdown(f"""<div style="background:#0f172a;border-left:3px solid #6366f1;
                border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;color:#a5b4fc;font-size:.85rem;">
                En buyuk fark: {max_fark['ders1']} ({max_fark['ort1']}) vs {max_fark['ders2']} ({max_fark['ort2']})
                — {max_fark['fark']:.0f} puan. Bu ogrenci(ler) {max_fark['ders2']}'de destek bekliyor olabilir.</div>""",
                unsafe_allow_html=True)

    # ── OGRETMEN YUKLENME ──
    tch_work = _teacher_workload(data)
    if tch_work:
        with st.expander(f"👨‍🏫 Ogretmen Yuklenme Analizi ({len(tch_work)} ogretmen)", expanded=False):
            import pandas as pd
            df_tw = pd.DataFrame(tch_work)
            st.dataframe(df_tw, use_container_width=True)
            aktif = sum(1 for t in tch_work if t["durum"] == "Aktif")
            pasif = sum(1 for t in tch_work if t["durum"] == "Pasif")
            if pasif > 0:
                st.markdown(f"""<div style="background:#422006;border-radius:8px;padding:8px 14px;
                margin:4px 0;color:#fcd34d;font-size:.85rem;">
                ⚠️ {pasif} ogretmen pasif — hic not girisi veya odev vermemis.
                Bu ogretmenlerin sistemi aktif kullanmasi saglanmali.</div>""", unsafe_allow_html=True)

    # ── DONEM KARSILASTIRMA ──
    with st.expander("📊 Donem Karsilastirma — 1. Donem vs 2. Donem", expanded=False):
        sem_comp = _semester_comparison(data)
        _render_semester_comparison(sem_comp)

    st.markdown("#### Akademik Destek & Rehberlik & Yabanci Dil")
    cf = data.get("cefr", {})
    ky = data.get("kayit", {})
    styled_stat_row([
        ("Kocluk Ogrenci", str(_safe_len(ek.get("ogrenciler", []))), "#8b5cf6", "🎯"),
        ("Kocluk Gorusme", str(_safe_len(ek.get("gorusmeler", []))), "#7c3aed", "🤝"),
        ("Rehberlik Gorusme", str(_safe_len(rh.get("gorusmeler", []))), "#2563eb", "📋"),
        ("Aktif Vaka", str(_safe_len(rh.get("vakalar", []))), "#ef4444", "📁"),
        ("BEP", str(_safe_len(rh.get("bep", []))), "#10b981", "📝"),
        ("CEFR Sinav", str(_safe_len(cf.get("exams", []))), "#6366f1", "🌍"),
        ("CEFR Sonuc", str(_safe_len(cf.get("results", []))), "#0d9488", "📊"),
    ])

    # CEFR Placement detay
    cf_results = cf.get("results", [])
    if cf_results:
        st.markdown("#### CEFR Seviye Dagilimi")
        cefr_dist: dict[str, int] = {}
        for r in cf_results:
            placed = r.get("placed_cefr", "?")
            cefr_dist[placed] = cefr_dist.get(placed, 0) + 1
        _donut(list(cefr_dist.keys()), list(cefr_dist.values()),
               center=f"<b>{len(cf_results)}</b><br><span style='font-size:10px;color:#64748b'>Ogrenci</span>")

    # Kayit Modulu Ozet
    adaylar = ky.get("adaylar", [])
    if adaylar:
        kesin = sum(1 for a in adaylar
                    if (a.get("asama") if isinstance(a, dict) else getattr(a, "asama", "")) == "kesin_kayit")
        st.markdown(f"#### Kayit Modulu: {len(adaylar)} aday, {kesin} kesin kayit")

    # Bos akademik alanlar
    # ── YABANCI DIL DEGERLENDIRMESI ──
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e1b4b,#4338ca);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin:12px 0;">'
        '<h4 style="margin:0;font-size:16px;">🌍 Yabancı Dil Değerlendirmesi</h4>'
        '<p style="margin:3px 0 0;font-size:12px;opacity:.85;">'
        'Quiz · CEFR Tespit · Mock Exam · Kurum Geneli Analiz</p></div>',
        unsafe_allow_html=True,
    )
    _yd_d = data.get("yd_sinav", {})
    _cf_d = data.get("cefr", {})
    _mk_d = data.get("cefr_mock", {})

    _yd_cols = st.columns(6)
    _yd_stats = [
        ("Quiz Sonuc", str(_yd_d.get("quiz_count", 0)), "#d97706"),
        ("Haftalik", str(_yd_d.get("haftalik_count", 0)), "#0891b2"),
        ("Quiz Ort.", f"{_yd_d.get('avg_score', 0):.1f}", "#2563eb"),
        ("CEFR Tespit", str(_safe_len(_cf_d.get("results", []))), "#8b5cf6"),
        ("Mock Exam", str(_mk_d.get("total_results", 0)), "#6d28d9"),
        ("Mock Ort.", f"{_mk_d.get('avg_score', 0):.1f}", "#7c3aed"),
    ]
    for i, (label, val, clr) in enumerate(_yd_stats):
        with _yd_cols[i]:
            st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:10px;
            text-align:center;border:1px solid {clr}30;">
            <div style="font-size:.7rem;color:#94a3b8;">{label}</div>
            <div style="font-size:1.1rem;font-weight:700;color:{clr};">{val}</div></div>""",
                        unsafe_allow_html=True)

    # YD Plotly Grafikler
    _yd_gc1, _yd_gc2 = st.columns(2)
    with _yd_gc1:
        _yd_avg_chart = _yd_d.get("avg_score", 0)
        if _yd_avg_chart > 0:
            _yd_fig = go.Figure(go.Indicator(
                mode="gauge+number", value=_yd_avg_chart,
                title=dict(text="Quiz Ortalaması", font=dict(size=14, color="#e2e8f0")),
                number=dict(font=dict(size=28, color="#e2e8f0")),
                gauge=dict(axis=dict(range=[0, 100], tickcolor="#64748b"),
                           bar=dict(color="#6366f1"), bgcolor="#131825",
                           borderwidth=2, bordercolor="#1e293b",
                           steps=[dict(range=[0, 29], color="rgba(34,197,94,.15)"),
                                  dict(range=[30, 54], color="rgba(245,158,11,.15)"),
                                  dict(range=[55, 74], color="rgba(249,115,22,.15)"),
                                  dict(range=[75, 100], color="rgba(239,68,68,.15)")],
                           threshold=dict(line=dict(color="#ef4444", width=3), thickness=0.8, value=70)),
            ))
            _yd_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=10), height=260)
            st.plotly_chart(_yd_fig, use_container_width=True, key="aid_yd_gauge")
    with _yd_gc2:
        _mk_avg_chart = _mk_d.get("avg_score", 0)
        if _mk_avg_chart > 0:
            _mk_fig = go.Figure(go.Indicator(
                mode="gauge+number", value=_mk_avg_chart,
                title=dict(text="Mock Exam Ortalaması", font=dict(size=14, color="#e2e8f0")),
                number=dict(font=dict(size=28, color="#e2e8f0")),
                gauge=dict(axis=dict(range=[0, 100], tickcolor="#64748b"),
                           bar=dict(color="#8b5cf6"), bgcolor="#131825",
                           borderwidth=2, bordercolor="#1e293b",
                           steps=[dict(range=[0, 29], color="rgba(34,197,94,.15)"),
                                  dict(range=[30, 54], color="rgba(245,158,11,.15)"),
                                  dict(range=[55, 74], color="rgba(249,115,22,.15)"),
                                  dict(range=[75, 100], color="rgba(239,68,68,.15)")]),
            ))
            _mk_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=10), height=260)
            st.plotly_chart(_mk_fig, use_container_width=True, key="aid_mk_gauge")

    # YD Durum tespiti + tavsiye
    _yd_avg = _yd_d.get("avg_score", 0)
    _yd_tvs = []
    if _yd_d.get("total_results", 0) == 0:
        _yd_tvs.append(("⚠️", "Yabancı dil değerlendirmesi yapılmamış — Ünite Quiz sistemi aktifleştirilmeli", "#f59e0b"))
    elif _yd_avg < 50:
        _yd_tvs.append(("🔴", f"Kurum geneli YD ortalaması kritik ({_yd_avg:.1f}) — acil müdahale planı", "#ef4444"))
    elif _yd_avg < 70:
        _yd_tvs.append(("🟡", f"YD ortalaması geliştirilmeli ({_yd_avg:.1f}) — düzenli quiz uygulaması", "#f59e0b"))
    else:
        _yd_tvs.append(("✅", f"YD ortalaması iyi ({_yd_avg:.1f}) — sürdürülebilir takip", "#22c55e"))

    if _safe_len(_cf_d.get("results", [])) == 0:
        _yd_tvs.append(("📋", "CEFR Seviye Tespiti yapılmamış — öğrenci seviyeleri belirsiz", "#f59e0b"))
    if _mk_d.get("total_results", 0) == 0:
        _yd_tvs.append(("🏆", "CEFR Mock Exam uygulanmamış — Cambridge formatında pratik sınav önerilir", "#8b5cf6"))
    elif _mk_d.get("avg_score", 0) < 50:
        _yd_tvs.append(("🏆", f"Mock Exam ortalaması düşük ({_mk_d.get('avg_score', 0):.1f}) — beceri bazlı destek", "#f97316"))

    for icon, text, clr in _yd_tvs:
        st.markdown(f"""<div style="background:{clr}08;border-left:3px solid {clr};
        border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;">
        <span style="margin-right:6px;">{icon}</span>
        <span style="color:#e2e8f0;font-size:.85rem;">{text}</span></div>""", unsafe_allow_html=True)

    bos_ak = []
    if not rh.get("gorusmeler") and not rh.get("vakalar"):
        bos_ak.append("Rehberlik — Gorusme ve vaka kaydi girilmemis")
    if not ek.get("ogrenciler"):
        bos_ak.append("Egitim Koclugu — Ogrenci eslestirmesi yapilmamis")
    if not cf.get("exams"):
        bos_ak.append("CEFR Seviye Tespit — Henuz sinav olusturulmamis")
    if bos_ak:
        st.markdown("#### Eksik Akademik Veriler")
        for item in bos_ak:
            st.markdown(f"""<div style="background:#0f172a;border-left:3px solid #f59e0b;
            border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;color:#fbbf24;font-size:.85rem;">
            {item}</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — İNSAN KAYNAKLARI
# ═══════════════════════════════════════════════════════════════════════════════

def _render_tab_ik(data: dict):
    styled_section("Insan Kaynaklari & Kadro Analizi", "#7c3aed")

    ik = data.get("ik", {})
    styled_stat_row([
        ("Aktif Personel", str(ik.get("employees_aktif", 0)), "#7c3aed", "👥"),
        ("Pozisyon", str(_safe_len(ik.get("positions", []))), "#2563eb", "📋"),
        ("Aday Havuzu", str(_safe_len(ik.get("candidates", []))), "#10b981", "🎯"),
        ("Performans", str(_safe_len(ik.get("performance", []))), "#f59e0b", "⭐"),
        ("Izin Kaydi", str(_safe_len(ik.get("izinler", []))), "#0d9488", "📅"),
    ])

    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### Personel Durum Dagilimi")
        emp = ik.get("employees", [])
        durum_counts: dict[str, int] = {}
        for e in emp:
            d = e.get("durum", "aktif") if isinstance(e, dict) else "aktif"
            durum_counts[d] = durum_counts.get(d, 0) + 1
        if durum_counts:
            _donut(list(durum_counts.keys()), list(durum_counts.values()))

    with ch2:
        st.markdown("#### Departman Bazli Kadro")
        dept_counts: dict[str, int] = {}
        for e in emp:
            dept = e.get("departman", e.get("pozisyon_kategorisi", "Diger")) if isinstance(e, dict) else "Diger"
            if dept:
                dept_counts[dept] = dept_counts.get(dept, 0) + 1
        if dept_counts:
            sorted_dept = sorted(dept_counts.items(), key=lambda x: -x[1])[:10]
            _bar([d for d, _ in sorted_dept], [v for _, v in sorted_dept],
                 colors=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(sorted_dept))],
                 horizontal=True)

    # Alt bolum — Performans + Izin
    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown("#### Performans Degerlendirme")
        perf = ik.get("performance", [])
        if perf:
            perf_scores: dict[str, int] = {}
            for p in perf:
                label = p.get("genel_degerlendirme", p.get("sonuc", "Belirtilmemis")) if isinstance(p, dict) else "?"
                if label:
                    perf_scores[label] = perf_scores.get(label, 0) + 1
            if perf_scores:
                _donut(list(perf_scores.keys()), list(perf_scores.values()))
            else:
                st.info("Performans verisi henuz girilmemis.")
        else:
            st.info("Performans degerlendirme kaydi yok.")

    with ch4:
        st.markdown("#### Izin Tur Dagilimi")
        izinler = ik.get("izinler", [])
        if izinler:
            izin_types: dict[str, int] = {}
            for iz in izinler:
                tur = iz.get("izin_turu", iz.get("tur", "Diger")) if isinstance(iz, dict) else "Diger"
                if tur:
                    izin_types[tur] = izin_types.get(tur, 0) + 1
            if izin_types:
                _donut(list(izin_types.keys()), list(izin_types.values()))
        else:
            st.info("Izin kaydi henuz girilmemis.")

    # Aday havuzu
    cands = ik.get("candidates", [])
    if cands:
        st.markdown("#### Aday Havuzu Durumu")
        cand_status: dict[str, int] = {}
        for c in cands:
            s = c.get("durum", c.get("status", "basvuru")) if isinstance(c, dict) else "?"
            cand_status[s] = cand_status.get(s, 0) + 1
        if cand_status:
            _bar(list(cand_status.keys()), list(cand_status.values()),
                 colors=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(cand_status))])

    # IK Detay Tablosu — Aktif calisanlar
    if emp:
        st.markdown("#### Aktif Personel Listesi")
        import pandas as pd
        emp_rows = []
        for e in emp[:30]:
            if isinstance(e, dict):
                emp_rows.append({
                    "Ad Soyad": f"{e.get('ad', '')} {e.get('soyad', '')}".strip(),
                    "Pozisyon": e.get("pozisyon", e.get("unvan", "-")),
                    "Departman": e.get("departman", e.get("pozisyon_kategorisi", "-")),
                    "Durum": e.get("durum", "aktif"),
                    "Telefon": e.get("telefon", "-"),
                })
        if emp_rows:
            st.dataframe(pd.DataFrame(emp_rows), use_container_width=True, height=min(300, len(emp_rows) * 40 + 50))

    # ── Pozisyon Hiyerarsi ──
    positions = ik.get("positions", [])
    if positions:
        st.markdown("#### Pozisyon Yapisi")
        for p in positions[:10]:
            baslik = p.get("baslik", p.get("ad", "?")) if isinstance(p, dict) else "?"
            kategori = p.get("kategori", "-") if isinstance(p, dict) else "-"
            st.markdown(f"- **{baslik}** — {kategori}")

    # ── Aday Pipeline ──
    cands = ik.get("candidates", [])
    if cands:
        st.markdown("#### Aday Surec Durumu")
        with st.expander(f"Aday Detay ({len(cands)} aday)", expanded=False):
            import pandas as pd
            cand_rows = []
            for c in cands[:20]:
                if isinstance(c, dict):
                    cand_rows.append({
                        "Ad Soyad": f"{c.get('ad', '')} {c.get('soyad', '')}".strip(),
                        "Pozisyon": c.get("basvuru_pozisyon", c.get("pozisyon", "-")),
                        "Durum": c.get("durum", c.get("status", "-")),
                        "Tarih": c.get("basvuru_tarihi", "-"),
                    })
            if cand_rows:
                st.dataframe(pd.DataFrame(cand_rows), use_container_width=True)

    # AI mini insight
    try:
        client = _get_client()
        _mini_ai_insight(client,
                         f"{ik.get('employees_aktif', 0)} aktif personel, "
                         f"{_safe_len(ik.get('candidates', []))} aday, "
                         f"{_safe_len(ik.get('performance', []))} performans, "
                         f"{_safe_len(ik.get('izinler', []))} izin, "
                         f"{_safe_len(positions)} pozisyon",
                         "ik_tab")
    except Exception:
        pass

    # Bos alanlara rehber
    bos_ik = []
    if not ik.get("performance"):
        bos_ik.append("Performans Degerlendirme — IK > Performans sekmesinden donem degerlendirmesi yapin")
    if not ik.get("izinler"):
        bos_ik.append("Izin Yonetimi — IK > Izin Yonetimi sekmesinden izin talebi olusturun")
    if not ik.get("positions"):
        bos_ik.append("Pozisyon Tanimlari — IK > Genel Bakis'tan pozisyon tanimlayin")
    if bos_ik:
        st.markdown("#### Henuz Veri Girilmemis Alanlar")
        for item in bos_ik:
            st.markdown(f"""<div style="background:#0f172a;border-left:3px solid #f59e0b;
            border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;color:#fbbf24;font-size:.85rem;">
            {item}</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MALİ & OPERASYONEL
# ═══════════════════════════════════════════════════════════════════════════════

def _render_tab_mali(data: dict):
    styled_section("Mali & Operasyonel Gorunum", "#059669")

    bu = data.get("butce", {})
    ds = data.get("destek", {})
    tdm = data.get("tdm", {})
    ku = data.get("kutuphane", {})
    sg = data.get("saglik", {})
    ssg = data.get("ssg", {})
    tp = data.get("toplanti", {})
    se = data.get("sosyal", {})
    rz = data.get("randevu", {})

    net = bu.get("toplam_gelir", 0) - bu.get("toplam_gider", 0)
    styled_stat_row([
        ("Gelir", f"{bu.get('toplam_gelir', 0):,.0f} TL", "#059669", "💰"),
        ("Gider", f"{bu.get('toplam_gider', 0):,.0f} TL", "#ef4444", "💸"),
        ("Net", f"{net:,.0f} TL", "#059669" if net >= 0 else "#ef4444", "📊"),
        ("Demirbas", str(_safe_len(tdm.get("demirbaslar", []))), "#2563eb", "🏢"),
        ("Destek Talep", str(_safe_len(ds.get("tickets", []))), "#f59e0b", "🔧"),
        ("Materyal", str(_safe_len(ku.get("materyaller", []))), "#0d9488", "📚"),
    ])

    # Mali verdict kartlari
    mv1, mv2, mv3 = st.columns(3)
    with mv1:
        gelir_v = bu.get("toplam_gelir", 0)
        gider_v = bu.get("toplam_gider", 0)
        oran = round(gelir_v / gider_v * 100) if gider_v > 0 else 0
        _verdict_card("Gelir/Gider Orani", f"%{oran}", "karsılama",
                      [(120, "🏆", "#6366f1", "Ustun: Gelir gideri %20+ asiyor"),
                       (100, "🟢", "#22c55e", "Dengeli: Gelir gideri karsilayor"),
                       (80, "🟡", "#f59e0b", "Dikkat: Gelir gideri tam karsilamiyor"),
                       (50, "🟠", "#f97316", "Risk: Ciddi acik var"),
                       (0, "🔴", "#ef4444", "Kritik: Gelir yetersiz veya girilmemis")])
    with mv2:
        kritik_cnt = len(kritik) if 'kritik' in dir() else sum(1 for u in tdm.get("urunler", [])
            if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
            and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0)
        _verdict_card("Kritik Stok", str(kritik_cnt), "urun",
                      [(0, "🏆", "#22c55e", "Temiz: Tum stoklar yeterli"),
                       (5, "🟡", "#f59e0b", "Az: Birkac urun takip edilmeli"),
                       (20, "🟠", "#f97316", "Cok: Satin alma hizlandirilmali"),
                       (50, "🔴", "#ef4444", "Kriz: Toplu satin alma acil!")],
                      reverse=True)
    with mv3:
        open_t = sum(1 for t in ds.get("tickets", []) if t.get("durum") in ("acik", "beklemede"))
        _verdict_card("Acik Talep", str(open_t), "destek",
                      [(0, "🏆", "#22c55e", "Temiz: Tum talepler kapatilmis"),
                       (3, "🟡", "#f59e0b", "Normal: Birkac talep bekliyor"),
                       (10, "🟠", "#f97316", "Yogun: Talep birikimi var"),
                       (20, "🔴", "#ef4444", "Kritik: Destek ekibi yetersiz")],
                      reverse=True)

    # Mali alarm
    if net < 0:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#450a0a,#7f1d1d);border-radius:14px;
        padding:14px 20px;margin:8px 0;border:1.5px solid rgba(239,68,68,0.4);">
        <div style="font-size:1rem;font-weight:800;color:#fca5a5;">
        🚨 Mali Uyari — Net bakiye negatif: {net:,.0f} TL</div>
        <div style="color:#fecaca;font-size:.82rem;margin-top:3px;">
        Gelir: {bu.get('toplam_gelir',0):,.0f} TL | Gider: {bu.get('toplam_gider',0):,.0f} TL
        {'| Gelir kaydi girilmemis!' if bu.get('toplam_gelir',0) == 0 else ''}</div>
        </div>""", unsafe_allow_html=True)
    elif bu.get("toplam_gelir", 0) == 0 and bu.get("toplam_gider", 0) == 0:
        st.markdown("""
        <div style="background:#0f172a;border-left:3px solid #f59e0b;
        border-radius:0 8px 8px 0;padding:10px 14px;margin:8px 0;color:#fbbf24;font-size:.85rem;">
        Butce modulune henuz gelir/gider girisi yapilmamis. Butce > Gelir Kayit sekmesinden baslatin.</div>""",
        unsafe_allow_html=True)

    # ── Butce Waterfall — Gelir/Gider/Net ──
    gelir_v = bu.get("toplam_gelir", 0)
    gider_v = bu.get("toplam_gider", 0)
    if gelir_v > 0 or gider_v > 0:
        st.markdown("#### Butce Akis — Waterfall")
        fig_wf = go.Figure(go.Waterfall(
            x=["Gelir", "Gider", "Net Bakiye"],
            y=[gelir_v, -gider_v, net],
            measure=["relative", "relative", "total"],
            text=[f"{gelir_v:,.0f}", f"-{gider_v:,.0f}", f"{net:,.0f}"],
            textposition="outside",
            connector=dict(line=dict(color="#334155", width=1)),
            increasing=dict(marker=dict(color="#22c55e")),
            decreasing=dict(marker=dict(color="#ef4444")),
            totals=dict(marker=dict(color="#6366f1")),
        ))
        fig_wf.update_layout(
            height=260, margin=dict(l=40, r=20, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
            xaxis=dict(tickfont=dict(color="#c7d2fe", size=12)),
            font=dict(color="#94a3b8"),
            showlegend=False,
        )
        st.plotly_chart(fig_wf, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### Gelir Kategori Dagilimi")
        gelir_cats: dict[str, float] = {}
        for g in bu.get("gelir", []):
            cat = g.get("kategori", g.get("tur", "Diger"))
            gelir_cats[cat] = gelir_cats.get(cat, 0) + float(g.get("tutar", 0))
        if gelir_cats:
            _donut(list(gelir_cats.keys()), list(gelir_cats.values()))

    with ch2:
        st.markdown("#### Gider Kategori Dagilimi")
        gider_cats: dict[str, float] = {}
        for g in bu.get("gider", []):
            cat = g.get("kategori", g.get("tur", "Diger"))
            gider_cats[cat] = gider_cats.get(cat, 0) + float(g.get("tutar", 0))
        if gider_cats:
            _donut(list(gider_cats.keys()), list(gider_cats.values()))

    # ── Gelir vs Gider Ay Bazli Trend ──
    gelir_list = bu.get("gelir", [])
    gider_list = bu.get("gider", [])
    if gelir_list or gider_list:
        st.markdown("#### Gelir vs Gider Ay Bazli Trend")
        ay_gelir: dict[str, float] = {}
        ay_gider: dict[str, float] = {}
        for g in gelir_list:
            tarih = g.get("tarih", "")
            if tarih and len(str(tarih)) >= 7:
                ay = str(tarih)[:7]
                ay_gelir[ay] = ay_gelir.get(ay, 0) + float(g.get("tutar", 0))
        for g in gider_list:
            tarih = g.get("tarih", "")
            if tarih and len(str(tarih)) >= 7:
                ay = str(tarih)[:7]
                ay_gider[ay] = ay_gider.get(ay, 0) + float(g.get("tutar", 0))
        all_months = sorted(set(list(ay_gelir.keys()) + list(ay_gider.keys())))
        if all_months:
            fig_fin = go.Figure()
            fig_fin.add_trace(go.Scatter(
                x=all_months, y=[ay_gelir.get(m, 0) for m in all_months],
                mode="lines+markers", name="Gelir",
                line=dict(color="#22c55e", width=3), marker=dict(size=7),
                fill="tozeroy", fillcolor="rgba(34,197,94,0.1)",
            ))
            fig_fin.add_trace(go.Scatter(
                x=all_months, y=[ay_gider.get(m, 0) for m in all_months],
                mode="lines+markers", name="Gider",
                line=dict(color="#ef4444", width=3), marker=dict(size=7),
                fill="tozeroy", fillcolor="rgba(239,68,68,0.1)",
            ))
            fig_fin.update_layout(
                height=280, margin=dict(l=40, r=20, t=20, b=40),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
                yaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
                legend=dict(font=dict(color="#94a3b8")),
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig_fin, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown("#### Destek Talep Durumu")
        ticket_status: dict[str, int] = {}
        for t in ds.get("tickets", []):
            s = t.get("durum", "acik")
            ticket_status[s] = ticket_status.get(s, 0) + 1
        if ticket_status:
            _donut(list(ticket_status.keys()), list(ticket_status.values()))

    with ch4:
        st.markdown("#### Operasyonel Ozet")
        ops_items = [
            ("Revir Ziyareti", _safe_len(sg.get("revir", [])), "🏥"),
            ("Kaza/Olay", _safe_len(sg.get("kaza", [])), "⚠️"),
            ("Tatbikat", _safe_len(ssg.get("tatbikat", [])), "🚨"),
            ("Risk Kaydi", _safe_len(ssg.get("riskler", [])), "📋"),
            ("Denetim", _safe_len(ssg.get("denetimler", [])), "🔍"),
            ("Toplanti", _safe_len(tp.get("meetings", [])), "📅"),
            ("Karar", _safe_len(tp.get("decisions", [])), "✅"),
            ("Kulup", _safe_len(se.get("kulupler", [])), "🎭"),
            ("Etkinlik", _safe_len(se.get("etkinlikler", [])), "🎉"),
            ("Randevu", _safe_len(rz.get("randevular", [])), "📆"),
            ("Ziyaretci", _safe_len(rz.get("ziyaretler", [])), "🚪"),
            ("Satin Alma", _safe_len(tdm.get("satin_alma", [])), "🛒"),
        ]
        for name, count, icon in ops_items:
            clr = "#10b981" if count > 0 else "#475569"
            st.markdown(f"<span style='color:{clr};font-weight:600'>{icon} {name}: {count}</span>",
                        unsafe_allow_html=True)

    # Alt bolum — Kutuphane + Toplanti + Saglik detay
    ch5, ch6 = st.columns(2)

    with ch5:
        st.markdown("#### Kutuphane Durum")
        mat = ku.get("materyaller", [])
        odn = ku.get("odunc", [])
        aktif_odunc = sum(1 for o in odn if not o.get("iade_tarihi"))
        geciken = sum(1 for o in odn if not o.get("iade_tarihi") and o.get("bitis_tarihi", "9999") < time.strftime("%Y-%m-%d"))
        if mat or odn:
            _donut(["Materyal", "Aktif Odunc", "Geciken Iade"],
                   [len(mat), aktif_odunc, geciken],
                   ["#0d9488", "#f59e0b", "#ef4444"],
                   center=f"<b>{len(mat)}</b><br><span style='font-size:10px;color:#64748b'>Materyal</span>")
        else:
            st.info("Kutuphane verisi henuz girilmemis.")

    with ch6:
        st.markdown("#### Toplanti Gorev Durumu")
        gorevler = tp.get("gorevler", [])
        if gorevler:
            gorev_status: dict[str, int] = {}
            for g in gorevler:
                s = g.get("durum", g.get("status", "beklemede")) if isinstance(g, dict) else "?"
                gorev_status[s] = gorev_status.get(s, 0) + 1
            if gorev_status:
                _donut(list(gorev_status.keys()), list(gorev_status.values()))
        else:
            st.info("Toplanti gorev kaydi yok.")

    # Demirbas ve satin alma
    ch7, ch8 = st.columns(2)
    with ch7:
        st.markdown("#### Demirbas Durum Dagilimi")
        demirbaslar = tdm.get("demirbaslar", [])
        if demirbaslar:
            db_status: dict[str, int] = {}
            for d in demirbaslar:
                s = d.get("durum", "aktif") if isinstance(d, dict) else "aktif"
                db_status[s] = db_status.get(s, 0) + 1
            _donut(list(db_status.keys()), list(db_status.values()))
        else:
            st.info("Demirbas kaydi yok.")

    # ── Stok Deger Analizi ──
    stok_val = _stock_value_analysis(data)
    if stok_val["toplam_deger"] > 0 or stok_val["kritik_deger"] > 0:
        with st.expander(f"💎 Stok Deger Analizi — Toplam: {stok_val['toplam_deger']:,.0f} TL | "
                          f"Kritik Eksik: {stok_val['kritik_deger']:,.0f} TL", expanded=False):
            sv1, sv2 = st.columns(2)
            with sv1:
                st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;
                text-align:center;border:1px solid #10b98130;">
                <div style="font-size:.7rem;color:#64748b;">Mevcut Stok Degeri</div>
                <div style="font-size:1.6rem;font-weight:900;color:#10b981;">
                {stok_val['toplam_deger']:,.0f} TL</div></div>""", unsafe_allow_html=True)
            with sv2:
                st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:14px;
                text-align:center;border:1px solid #ef444430;">
                <div style="font-size:.7rem;color:#64748b;">Eksik Stok Maliyeti</div>
                <div style="font-size:1.6rem;font-weight:900;color:#ef4444;">
                {stok_val['kritik_deger']:,.0f} TL</div></div>""", unsafe_allow_html=True)

            # Kategori dagilimi
            if stok_val["kategori"]:
                st.markdown("**Kategori Bazli Stok Degeri:**")
                kat_sorted = sorted(stok_val["kategori"].items(), key=lambda x: -x[1])
                _donut([k for k, _ in kat_sorted], [v for _, v in kat_sorted],
                       center=f"<b>{stok_val['toplam_deger']:,.0f}</b><br><span style='font-size:9px;color:#64748b'>TL</span>")

            # En pahali 5 urun
            if stok_val["en_pahali"]:
                st.markdown("**En Degerli 5 Urun:**")
                for u in stok_val["en_pahali"][:5]:
                    st.markdown(f"- **{u['urun']}** ({u['kategori']}): {u['stok']} adet × {u['fiyat']:.2f} TL = "
                                f"**{u['deger']:,.2f} TL**")

    # ── Kritik Stok Uyarilari ──
    urunler = tdm.get("urunler", [])
    kritik = [u for u in urunler
              if isinstance(u.get("stok"), (int, float)) and isinstance(u.get("min_stok"), (int, float))
              and u.get("stok", 0) < u.get("min_stok", 0) and u.get("min_stok", 0) > 0]
    stok_oran = round(len(kritik) / len(urunler) * 100) if urunler else 0

    if kritik:
        stk_color = "#ef4444" if stok_oran > 50 else ("#f59e0b" if stok_oran > 20 else "#22c55e")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#450a0a,#7f1d1d);border-radius:14px;
        padding:16px 20px;margin:12px 0;border:1.5px solid rgba(239,68,68,0.4);">
        <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
        <div style="font-size:1.1rem;font-weight:800;color:#fca5a5;">
        🚨 Kritik Stok Uyarisi</div>
        <div style="color:#fecaca;font-size:.85rem;margin-top:4px;">
        {len(kritik)}/{len(urunler)} urun minimum stok seviyesinin altinda (%{stok_oran})</div>
        </div>
        <div style="font-size:2.5rem;font-weight:900;color:#ef4444;">{len(kritik)}</div>
        </div></div>""", unsafe_allow_html=True)

        st.markdown(f"#### Kritik Stok Detay (Ilk 25)")
        import pandas as pd
        df_kritik = pd.DataFrame([{
            "Urun": u.get("urun_adi", "?"),
            "Kategori": u.get("kategori", "-"),
            "Stok": int(u.get("stok", 0)),
            "Min Stok": int(u.get("min_stok", 0)),
            "Eksik": int(u.get("min_stok", 0) - u.get("stok", 0)),
            "Birim Fiyat": f"{u.get('birim_fiyat', 0):.2f} TL",
        } for u in sorted(kritik, key=lambda x: x.get("min_stok", 0) - x.get("stok", 0), reverse=True)[:25]])
        st.dataframe(df_kritik, use_container_width=True, height=min(350, len(df_kritik)*40+50))

        # Stok kategori dagilimi
        kat_counts: dict[str, int] = {}
        for u in kritik:
            k = u.get("kategori", "Diger")
            kat_counts[k] = kat_counts.get(k, 0) + 1
        if kat_counts:
            st.markdown("#### Kritik Stok Kategori Dagilimi")
            _donut(list(kat_counts.keys()), list(kat_counts.values()),
                   center=f"<b>{len(kritik)}</b><br><span style='font-size:10px;color:#ef4444'>Kritik</span>")

    with ch8:
        st.markdown("#### Guvenlik & Saglik Ozeti")
        sg_items = [
            ("Revir Ziyareti", _safe_len(sg.get("revir", [])), "#059669"),
            ("Kaza/Olay", _safe_len(sg.get("kaza", [])), "#ef4444"),
            ("Tatbikat", _safe_len(ssg.get("tatbikat", [])), "#f59e0b"),
            ("Acik Risk", _safe_len(ssg.get("riskler", [])), "#dc2626"),
            ("Denetim", _safe_len(ssg.get("denetimler", [])), "#2563eb"),
        ]
        labels_sg = [s[0] for s in sg_items if s[1] > 0]
        vals_sg = [s[1] for s in sg_items if s[1] > 0]
        colors_sg = [s[2] for s in sg_items if s[1] > 0]
        if vals_sg:
            _bar(labels_sg, vals_sg, colors=colors_sg, horizontal=True)
        else:
            st.info("Guvenlik/saglik kaydi yok.")

    # ── Toplanti Detay ──
    meetings = tp.get("meetings", [])
    if meetings:
        with st.expander(f"📅 Toplanti Detay ({len(meetings)} toplanti)", expanded=False):
            import pandas as pd
            m_rows = []
            for m in meetings[:20]:
                m_rows.append({
                    "Baslik": m.get("baslik", "?"),
                    "Tur": m.get("category", m.get("type_code", "-")),
                    "Tarih": m.get("tarih", "-"),
                    "Saat": m.get("saat_baslangic", "-"),
                    "Durum": m.get("durum", "-"),
                })
            if m_rows:
                st.dataframe(pd.DataFrame(m_rows), use_container_width=True)

    # ── Destek Talep Detay ──
    tickets = ds.get("tickets", [])
    if tickets:
        with st.expander(f"🔧 Destek Talep Detay ({len(tickets)} talep)", expanded=False):
            import pandas as pd
            t_rows = []
            for t in tickets[:20]:
                t_rows.append({
                    "No": t.get("ticket_no", "?"),
                    "Alan": t.get("hizmet_alani_kodu", "-"),
                    "Oncelik": t.get("oncelik", "-"),
                    "Durum": t.get("durum", "-"),
                    "Lokasyon": t.get("lokasyon", "-"),
                })
            if t_rows:
                st.dataframe(pd.DataFrame(t_rows), use_container_width=True)

    # ── Sosyal Etkinlik & Kulupler ──
    se = data.get("sosyal", {})
    kulupler = se.get("kulupler", [])
    etkinlikler = se.get("etkinlikler", [])
    if kulupler or etkinlikler:
        st.markdown("#### Sosyal Yasam")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.metric("Aktif Kulup", len(kulupler))
            for k in kulupler[:5]:
                ad = k.get("ad", "?") if isinstance(k, dict) else getattr(k, "ad", "?")
                st.markdown(f"- {ad}")
        with sc2:
            st.metric("Etkinlik", len(etkinlikler))
            for e in etkinlikler[:5]:
                baslik = e.get("baslik", "?") if isinstance(e, dict) else getattr(e, "baslik", "?")
                st.markdown(f"- {baslik}")

    # ── Randevu & Ziyaretci ──
    rz_r = rz.get("randevular", [])
    rz_z = rz.get("ziyaretler", [])
    if rz_r or rz_z:
        st.markdown("#### Randevu & Ziyaretci")
        styled_stat_row([
            ("Randevu", str(len(rz_r)), "#6366f1", "📆"),
            ("Ziyaretci", str(len(rz_z)), "#10b981", "🚪"),
        ])

    # AI mini insight
    try:
        client = _get_client()
        net_str = f"Net bakiye: {net:,.0f} TL" if net != 0 else "Butce verisi yok"
        kritik_str = f"{len(kritik)} kritik stok" if kritik else "Stok verisi yok"
        _mini_ai_insight(client,
                         f"{net_str}, {kritik_str}, "
                         f"{_safe_len(ds.get('tickets', []))} destek talebi, "
                         f"{_safe_len(ssg.get('riskler', []))} guvenlik riski",
                         "mali_tab")
    except Exception:
        pass

    # ── Bos Modul Rehberi ──
    bos_mali = []
    if not data.get("kutuphane", {}).get("materyaller"):
        bos_mali.append("Kutuphane — Kutuphane modulunden materyal kaydi yapin")
    if not data.get("dijital_kutuphane", {}).get("kaynaklar"):
        bos_mali.append("Dijital Kutuphane — Dijital kaynaklari tanimlayin")
    if not rz_r and not rz_z:
        bos_mali.append("Randevu & Ziyaretci — Randevu modulunden kayit baslatin")
    if not data.get("ssg", {}).get("tatbikat") and not data.get("ssg", {}).get("riskler"):
        bos_mali.append("Sivil Savunma & ISG — Tatbikat ve risk degerlendirme tanimlayin")
    if not bu.get("gelir"):
        bos_mali.append("Gelir Kaydi — Butce modulunden gelir girisi yapin")

    if bos_mali:
        st.markdown("#### Eksik Veri Alanlari — Aksiyon Gerekli")
        for item in bos_mali:
            st.markdown(f"""<div style="background:#0f172a;border-left:3px solid #f59e0b;
            border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;color:#fbbf24;font-size:.85rem;">
            {item}</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — AI DEĞERLENDİRME & YOL HARİTASI
# ═══════════════════════════════════════════════════════════════════════════════

def _build_ai_kpi_summary(data: dict) -> str:
    """AI icin tum modullerin KPI ozetini metin olarak uretir."""
    ak = data.get("akademik", {})
    od = data.get("olcme", {})
    ik = data.get("ik", {})
    rh = data.get("rehberlik", {})
    sg = data.get("saglik", {})
    bu = data.get("butce", {})
    tdm = data.get("tdm", {})
    tp = data.get("toplanti", {})
    se = data.get("sosyal", {})
    ds = data.get("destek", {})
    rz = data.get("randevu", {})
    ssg = data.get("ssg", {})
    ku = data.get("kutuphane", {})
    dk = data.get("dijital_kutuphane", {})
    ek = data.get("egitim_koclugu", {})
    eu = data.get("erken_uyari", {})
    ky = data.get("kayit", {})
    cf = data.get("cefr", {})

    net = bu.get("toplam_gelir", 0) - bu.get("toplam_gider", 0)
    open_tickets = sum(1 for t in ds.get("tickets", []) if t.get("durum") in ("acik", "beklemede"))
    risk_high = sum(1 for r in eu.get("risks", []) if r.get("risk_level") in ("HIGH", "CRITICAL"))

    lines = [
        "SMARTCAMPUS AI — KURUM KPI OZETI (TUM MODULLER)",
        "=" * 60,
        f"\n1. AKADEMIK: {ak.get('students_aktif', 0)} aktif ogrenci, {ak.get('teachers_count', 0)} ogretmen, "
        f"{_safe_len(ak.get('grades', []))} not kaydi, {_safe_len(ak.get('attendance', []))} devamsizlik, "
        f"{_safe_len(ak.get('odevler', []))} odev",
        f"2. OLCME & DEGERLENDIRME: {od.get('questions_count', 0)} soru ({od.get('approved_q', 0)} onayli), "
        f"{_safe_len(od.get('results', []))} sinav sonucu, {_safe_len(od.get('telafi', []))} telafi gorevi",
        f"3. INSAN KAYNAKLARI: {ik.get('employees_aktif', 0)} aktif personel, "
        f"{_safe_len(ik.get('candidates', []))} aday, {_safe_len(ik.get('positions', []))} pozisyon, "
        f"{_safe_len(ik.get('performance', []))} performans, {_safe_len(ik.get('izinler', []))} izin",
        f"4. REHBERLIK: {_safe_len(rh.get('gorusmeler', []))} gorusme, "
        f"{_safe_len(rh.get('vakalar', []))} vaka, {_safe_len(rh.get('bep', []))} BEP",
        f"5. OKUL SAGLIGI: {_safe_len(sg.get('revir', []))} revir ziyareti, "
        f"{_safe_len(sg.get('kaza', []))} kaza/olay",
        f"6. BUTCE: Gelir {bu.get('toplam_gelir', 0):,.0f} TL, Gider {bu.get('toplam_gider', 0):,.0f} TL, "
        f"Net {net:,.0f} TL",
        f"7. TUKETIM & DEMIRBAS: {_safe_len(tdm.get('urunler', []))} urun, "
        f"{_safe_len(tdm.get('demirbaslar', []))} demirbas, {_safe_len(tdm.get('satin_alma', []))} satin alma",
        f"8. TOPLANTI: {_safe_len(tp.get('meetings', []))} toplanti, "
        f"{_safe_len(tp.get('decisions', []))} karar, {_safe_len(tp.get('gorevler', []))} gorev",
        f"9. SOSYAL ETKINLIK: {_safe_len(se.get('kulupler', []))} kulup, "
        f"{_safe_len(se.get('etkinlikler', []))} etkinlik",
        f"10. DESTEK HIZMETLERI: {_safe_len(ds.get('tickets', []))} talep ({open_tickets} acik), "
        f"{_safe_len(ds.get('periyodik', []))} periyodik gorev",
        f"11. RANDEVU & ZIYARETCI: {_safe_len(rz.get('randevular', []))} randevu, "
        f"{_safe_len(rz.get('ziyaretler', []))} ziyaret",
        f"12. SIVIL SAVUNMA & ISG: {_safe_len(ssg.get('tatbikat', []))} tatbikat, "
        f"{_safe_len(ssg.get('riskler', []))} risk, {_safe_len(ssg.get('denetimler', []))} denetim",
        f"13. KUTUPHANE: {_safe_len(ku.get('materyaller', []))} materyal, "
        f"{_safe_len(ku.get('odunc', []))} odunc",
        f"14. DIJITAL KUTUPHANE: {_safe_len(dk.get('kaynaklar', []))} dijital kaynak",
        f"15. EGITIM KOCLUGU: {_safe_len(ek.get('ogrenciler', []))} ogrenci, "
        f"{_safe_len(ek.get('gorusmeler', []))} gorusme, {_safe_len(ek.get('hedefler', []))} hedef",
        f"16. ERKEN UYARI: {_safe_len(eu.get('risks', []))} risk kaydi ({risk_high} yuksek/kritik), "
        f"{_safe_len(eu.get('alerts', []))} aktif uyari",
        f"17. KAYIT MODULU: {_safe_len(ky.get('adaylar', []))} aday",
        f"18. CEFR PLACEMENT: {_safe_len(cf.get('exams', []))} sinav, "
        f"{_safe_len(cf.get('results', []))} sonuc",
        f"18b. CEFR MOCK EXAM: {data.get('cefr_mock', {}).get('total_results', 0)} sonuc, "
        f"Ortalama: {data.get('cefr_mock', {}).get('avg_score', 0):.1f}",
        f"18c. YABANCI DIL QUIZ & SINAV: {data.get('yd_sinav', {}).get('total_results', 0)} sonuc, "
        f"Quiz: {data.get('yd_sinav', {}).get('quiz_count', 0)}, "
        f"Haftalik: {data.get('yd_sinav', {}).get('haftalik_count', 0)}, "
        f"Ortalama: {data.get('yd_sinav', {}).get('avg_score', 0):.1f}",
        f"18d. REHBERLIK TEST & ENVANTER: {data.get('rhb_test', {}).get('test_count', 0)} test, "
        f"{data.get('rhb_test', {}).get('tamamlanan', 0)} tamamlanan oturum",
        f"18d2. TUM TEST SONUCLARI: Toplam {data.get('tum_testler', {}).get('toplam', 0)} test | "
        f"Rehberlik: {data.get('tum_testler', {}).get('rehberlik', 0)} | "
        f"Kayit: {data.get('tum_testler', {}).get('kayit', 0)} | "
        f"Turler: {data.get('tum_testler', {}).get('test_turleri', {})}",
        f"18e. AILE BILGI FORMU: {data.get('aile_bilgi', {}).get('toplam', 0)} form, "
        f"{data.get('aile_bilgi', {}).get('kritik_aile', 0)} kritik aile durumu (bosanmis/kayip/travma/bagimlilik)",
        # ── MEB Dijital Formlar (35 form) ──
        f"18f. MEB DIJITAL FORMLAR: Toplam {data.get('meb_formlar', {}).get('toplam_kayit', 0)} kayit | "
        f"Kategoriler: {', '.join(f'{k}:{v}' for k,v in data.get('meb_formlar', {}).get('kategori', {}).items()) or 'Henuz veri yok'} | "
        f"RISK GOSTERGELERI: "
        f"DEHB suplesi {data.get('meb_formlar', {}).get('risk', {}).get('dehb_suphe', 0)}, "
        f"OOG suplesi {data.get('meb_formlar', {}).get('risk', {}).get('oog_suphe', 0)}, "
        f"Disiplin olayi {data.get('meb_formlar', {}).get('risk', {}).get('disiplin_olay', 0)}, "
        f"Psikolojik yonlendirme {data.get('meb_formlar', {}).get('risk', {}).get('psikolojik_yonlendirme', 0)}, "
        f"Saglik yonlendirme {data.get('meb_formlar', {}).get('risk', {}).get('saglik_yonlendirme', 0)}, "
        f"Ev ziyareti risk {data.get('meb_formlar', {}).get('risk', {}).get('ev_risk', 0)}, "
        f"Sinif risk ogrenci {data.get('meb_formlar', {}).get('risk', {}).get('sinif_risk_ogrenci', 0)}, "
        f"ACIL MUDAHALE {data.get('meb_formlar', {}).get('risk', {}).get('acil_mudahale', 0)}",
        f"19. KURUMSAL ORG (KOI): Kurum adi: {data.get('koi', {}).get('kurum_adi', '-')}",
        f"20. KAYIT MODULU (eski HI): {_safe_len(ky.get('adaylar', []))} aday pipeline",
        f"21. SOSYAL MEDYA: {_safe_len(data.get('sosyal_medya', {}).get('hesaplar', []))} hesap, "
        f"{_safe_len(data.get('sosyal_medya', {}).get('paylasimlar', []))} paylasim",
        f"22. KURUM HIZMETLERI: {len(data.get('kurum_hizmetleri', {}))} alan (yemek/servis/duyuru)",
        f"23. KULLANICI YONETIMI: {data.get('kullanici', {}).get('total', 0)} kullanici",
        f"24. MEZUNLAR: {_safe_len(data.get('mezunlar', {}).get('mezunlar', []))} mezun",
        f"25. YABANCI DIL: Ders isleme motoru, CEFR sinav, 36 hafta plan (bagimsiz modul)",
        f"26. OKUL ONCESI - ILKOKUL: Gunluk bulten, ilkokul rapor, veli geri bildirim",
        f"27. AI BIREYSEL EGITIM: Adaptif ogrenme, bireysel ders planlamasi",
        f"28. AI TRENI: Bilgi treni, interaktif ogrenme oyunlari",
        f"29. MATEMATIK KOYU: Matematik oyunlari, alistirmalar, yarisma",
        f"30. SANAT SOKAGI: Sanat etkinlikleri, sergi, portfolyo",
        f"31. BILISIM VADISI: Kodlama, robotik, dijital vatandaslik",
        f"32. KISISEL DIL GELISIMI: Bireysel dil ogrenme, SRS tekrar",
        f"33. YONETIM TEK EKRAN: Yonetici KPI dashboard, hizli erisim",
        f"34. KURUM YONETIMI: Sistem ayarlari, tenant yonetimi",
        f"35. AKADEMIK TAKVIM: Egitim takvimi, tatil gunleri, etkinlik plani",
    ]
    return "\n".join(lines)


def _render_tab_ai_eval(client, data: dict):
    styled_section("AI Destekli Kurum Degerlendirmesi & Yol Haritasi", "#8b5cf6")

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);color:#a5b4fc;'
        'padding:14px 20px;border-radius:12px;margin-bottom:16px;font-size:0.88rem;">'
        'Bu sekme tum SmartCampus AI modullerinden toplanan verileri AI ile analiz eder. '
        '18 modulun KPI ozetini GPT-4o-mini\'ye gonderir ve kurum icin kapsamli bir '
        'degerlendirme + yol haritasi + tavsiyeler uretir.</div>',
        unsafe_allow_html=True,
    )

    ai_cache_key = "_ai_brain_analysis"

    # Kurum skoru ozeti
    inst_score = _compute_institution_score(data)
    gs1, gs2 = st.columns([1, 3])
    with gs1:
        _gauge(inst_score["overall"], 100, "Kurum Skoru",
               "#22c55e" if inst_score["overall"] >= 70 else ("#f59e0b" if inst_score["overall"] >= 40 else "#ef4444"))
    with gs2:
        for dim, val in inst_score["scores"].items():
            bar_c = "#22c55e" if val >= 70 else ("#f59e0b" if val >= 40 else "#ef4444")
            st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
            <span style="width:160px;color:#94a3b8;font-size:.82rem;">{dim}</span>
            <div style="flex:1;background:#1e293b;border-radius:6px;height:14px;overflow:hidden;">
            <div style="width:{val}%;height:100%;background:{bar_c};border-radius:6px;"></div></div>
            <span style="width:40px;text-align:right;color:{bar_c};font-weight:700;font-size:.82rem;">%{val:.0f}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Gap Analizi
    gaps = st.session_state.get("_ai_gap_cache") or _gap_analysis(data)
    with st.expander(f"🎯 Gap Analizi — {sum(1 for g in gaps if g['durum']!='OK')}/{len(gaps)} alanda gap var", expanded=False):
        _render_gap_analysis(gaps, prefix="t5")

    # Kural bazli derin analiz
    analysis = _deep_rule_analysis(data)
    with st.expander(f"🧠 Kural Bazli Analiz — {len(analysis['findings'])} Bulgu, "
                      f"{len(analysis['roadmap'])} Aksiyon", expanded=False):
        _render_deep_analysis(analysis)

    # Anomali ozeti
    anomalies = _anomaly_detection(data)
    if anomalies:
        st.markdown(f"#### Tespit Edilen Anomaliler ({len(anomalies)})")
        _render_anomalies(anomalies)
        st.markdown("---")

    # Benchmark Karsilastirma (Turkiye ortalamalari — referans degerler)
    st.markdown("#### Benchmark Karsilastirma")
    st.caption("Turkiye ozel okul sektoru referans degerleri ile kurumunuzun karsilastirmasi")
    benchmarks = [
        ("Ogretmen/Ogrenci Orani", f"1:{round(data.get('akademik',{}).get('students_aktif',0) / max(data.get('akademik',{}).get('teachers_count',1),1),1)}", "1:12-15", "#2563eb"),
        ("Not Ortalamasi", f"{sum(float(getattr(g,'puan',0) if not isinstance(g,dict) else g.get('puan',0)) for g in data.get('akademik',{}).get('grades',[])) / max(len(data.get('akademik',{}).get('grades',[])),1):.1f}", "70-80", "#10b981"),
        ("Soru Bankasi", f"{data.get('olcme',{}).get('questions_count',0):,}", "5,000+", "#8b5cf6"),
        ("Dijital Modul Kullanimi", f"{sum(1 for v in data.values() if sum(_safe_len(x) for x in v.values() if isinstance(x,list))>0)}/18", "15/18+", "#6366f1"),
        ("Kurum Skoru", f"%{inst_score['overall']:.0f}", "%70+", "#f59e0b"),
    ]
    bm_cols = st.columns(len(benchmarks))
    for i, (label, val, ref, color) in enumerate(benchmarks):
        with bm_cols[i]:
            st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:12px;
            text-align:center;border:1px solid {color}30;">
            <div style="font-size:.7rem;color:#64748b;text-transform:uppercase;">{label}</div>
            <div style="font-size:1.2rem;font-weight:800;color:{color};margin:4px 0;">{val}</div>
            <div style="font-size:.65rem;color:#475569;">Referans: {ref}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🤖 AI Kurum Analizi Baslat", key="ai_brain_analyze",
                   type="primary", use_container_width=True):
        with st.spinner("18 modulden veri analiz ediliyor... (bu islem 15-30 saniye surebilir)"):
            kpi_text = _build_ai_kpi_summary(data)
            # Kurum skorunu da ekle
            kpi_text += f"\n\nKURUM SAGLIK SKORU: %{inst_score['overall']:.0f}\n"
            for dim, val in inst_score["scores"].items():
                kpi_text += f"  {dim}: %{val:.0f}\n"
            messages = [
                {"role": "system", "content": _ai_inject_rules(
                    "Sen bir egitim kurumu yonetim danismanisin. Turkce analiz yaz. "
                    "Asagidaki verileri analiz ederek KAPSAMLI bir kurum degerlendirmesi yap. "
                    "Yanitini su bolumlerle yapilandir:\n\n"
                    "## 1. Genel Degerlendirme\n2-3 paragraf kurum ozeti.\n\n"
                    "## 2. Guclu Yonler\nEn az 5 madde.\n\n"
                    "## 3. Iyilestirme Gereken Alanlar\nEn az 5 madde, somut gozlemler.\n\n"
                    "## 4. Kisa Vadeli Aksiyonlar (1-3 Ay)\nEn az 5 somut adim.\n\n"
                    "## 5. Stratejik Yol Haritasi (6-12 Ay)\nEn az 5 stratejik hedef.\n\n"
                    "## 6. Modul Bazli Tavsiyeler\n18 modul icin birer tavsiye.\n\n"
                    "## 7. Risk Uyarilari\nAcil mudahale gerektiren noktalar.\n\n"
                    "Veri yoksa o modulu 'henuz veri girilmemis' olarak belirt. "
                    "Her bolumde emoji kullan. Somut, uygulanabilir, olculebilir tavsiyeler ver."
                )},
                {"role": "user", "content": kpi_text},
            ]
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=3000,
                    temperature=0.7,
                )
                ai_text = response.choices[0].message.content or ""
                st.session_state[ai_cache_key] = ai_text
            except Exception as e:
                st.error(f"AI analiz olusturulamadi: {e}")

    # Cache'den goster
    if st.session_state.get(ai_cache_key):
        st.markdown("---")
        # Rapor basligini premium kart olarak goster
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:14px;
        padding:16px 20px;margin-bottom:16px;border:1.5px solid rgba(139,92,246,0.3);">
        <div style="font-size:1.1rem;font-weight:800;color:#c7d2fe;">
        🤖 SmartCampus AI — Kurum Analiz Raporu</div>
        <div style="font-size:.78rem;color:#a5b4fc;margin-top:3px;">
        18 modul verisi incelendi | GPT-4o-mini tarafindan uretildi</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(st.session_state[ai_cache_key])

        # Rapor alt bilgi
        st.markdown(f"""
        <div style="background:#0f172a;border-radius:10px;padding:10px 16px;margin-top:16px;
        border:1px solid #1e293b;text-align:center;">
        <span style="color:#475569;font-size:.75rem;">
        Bu rapor SmartCampus AI Merkez Beyni tarafindan otomatik uretilmistir.
        Veriler {time.strftime('%d.%m.%Y %H:%M')} itibariyladir.
        </span></div>""", unsafe_allow_html=True)
    else:
        # Otomatik analiz tetikle (ilk acilista)
        auto_key = "_ai_brain_auto_done"
        if not st.session_state.get(auto_key):
            st.session_state[auto_key] = True
            st.info("Otomatik AI analiz baslatiliyor... Yukaridaki butona tiklayin veya sayfayi yenileyin.")

    # ── PDF RAPOR & KILAVUZ ──
    st.markdown("---")
    st.markdown("#### SmartCampus AI — PDF Rapor & Kilavuz")

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        if st.button("📄 Kurumsal Kilavuz PDF", key="ai_brain_pdf_guide",
                       type="secondary", use_container_width=True):
            with st.spinner("Kilavuz PDF olusturuluyor..."):
                pdf_bytes = _generate_guide_pdf(data)
                if pdf_bytes:
                    st.download_button("⬇ Kilavuz Indir", data=pdf_bytes,
                                        file_name="SmartCampusAI_Kilavuz.pdf",
                                        mime="application/pdf", key="ai_brain_pdf_dl")

    with pc2:
        if st.button("🤖 AI Analiz Raporu PDF", key="ai_brain_pdf_analysis",
                       type="primary", use_container_width=True):
            ai_text = st.session_state.get("_ai_brain_analysis", "")
            if not ai_text:
                st.warning("Once AI analiz olusturun, sonra PDF indirebilirsiniz.")
            else:
                with st.spinner("AI Analiz Raporu PDF olusturuluyor..."):
                    pdf_bytes = _generate_ai_analysis_pdf(data, ai_text)
                    if pdf_bytes:
                        st.download_button("⬇ AI Rapor Indir", data=pdf_bytes,
                                            file_name="SmartCampusAI_AI_Analiz_Raporu.pdf",
                                            mime="application/pdf", key="ai_brain_pdf_ai_dl")

    with pc3:
        if st.button("🏆 Kurum Karnesi PDF", key="ai_brain_pdf_karne",
                       type="primary", use_container_width=True):
            with st.spinner("Kurum Karnesi olusturuluyor..."):
                gaps = _gap_analysis(data)
                pdf_bytes = _generate_kurum_karnesi_pdf(data, gaps)
                if pdf_bytes:
                    st.download_button("⬇ Karne Indir", data=pdf_bytes,
                                        file_name="SmartCampusAI_Kurum_Karnesi.pdf",
                                        mime="application/pdf", key="ai_brain_pdf_karne_dl")


# ═══════════════════════════════════════════════════════════════════════════════
# KURUMSAL KILAVUZ PDF
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_guide_pdf(data: dict) -> bytes | None:
    """SmartCampus AI tam kilavuz — 18 modul, ne ise yarar, mevcut durum, tavsiyeler."""
    try:
        import io as _io
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, Image,
        )
        from utils.shared_data import ensure_turkish_pdf_fonts

        fn, fb = ensure_turkish_pdf_fonts()
        buf = _io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                topMargin=1.5*cm, bottomMargin=2*cm,
                                leftMargin=2*cm, rightMargin=2*cm)
        pw = A4[0] - 4*cm
        els = []

        # Stiller
        styles = getSampleStyleSheet()
        s_title = ParagraphStyle("GT", fontName=fb, fontSize=22, leading=28,
                                  alignment=1, textColor=rl.HexColor("#1e1b4b"), spaceAfter=6)
        s_sub = ParagraphStyle("GS", fontName=fn, fontSize=11, leading=14,
                                alignment=1, textColor=rl.HexColor("#64748b"), spaceAfter=20)
        s_h1 = ParagraphStyle("GH1", fontName=fb, fontSize=16, leading=20,
                               textColor=rl.HexColor("#1e1b4b"), spaceBefore=16, spaceAfter=8)
        s_h2 = ParagraphStyle("GH2", fontName=fb, fontSize=12, leading=15,
                               textColor=rl.HexColor("#6366f1"), spaceBefore=10, spaceAfter=4)
        s_body = ParagraphStyle("GB", fontName=fn, fontSize=9, leading=13, spaceAfter=4)
        s_small = ParagraphStyle("GSm", fontName=fn, fontSize=7.5, leading=10,
                                  textColor=rl.HexColor("#64748b"))
        s_bullet = ParagraphStyle("GBul", fontName=fn, fontSize=9, leading=13,
                                   leftIndent=20, bulletIndent=8, spaceAfter=2)

        def _t(text):
            return str(text) if fn != "Helvetica" else str(text).translate(
                str.maketrans("ıİğĞüÜşŞöÖçÇ", "iIgGuUsSoOcC"))

        # ═══ KAPAK SAYFASI ═══
        els.append(Spacer(1, 3*cm))
        els.append(Paragraph(_t("SmartCampus AI"), s_title))
        els.append(Paragraph(_t("Kurumsal Yazilim Kilavuzu"), ParagraphStyle(
            "GCover", fontName=fb, fontSize=14, leading=18, alignment=1,
            textColor=rl.HexColor("#6366f1"), spaceAfter=12)))
        els.append(Spacer(1, 0.5*cm))

        # Kurum skoru
        inst = _compute_institution_score(data)
        els.append(Paragraph(_t(f"Kurum Saglik Skoru: %{inst['overall']:.0f}"), ParagraphStyle(
            "GScore", fontName=fb, fontSize=18, leading=24, alignment=1,
            textColor=rl.HexColor("#22c55e" if inst["overall"] >= 60 else "#f59e0b"),
            spaceAfter=8)))

        score_text = " | ".join(f"{k}: %{v:.0f}" for k, v in inst["scores"].items())
        els.append(Paragraph(_t(score_text), ParagraphStyle(
            "GScoreD", fontName=fn, fontSize=8, leading=11, alignment=1,
            textColor=rl.HexColor("#64748b"), spaceAfter=20)))

        total_records = sum(sum(_safe_len(v) for v in vals.values() if isinstance(v, list))
                            for vals in data.values())
        active_mods = sum(1 for vals in data.values()
                          if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0)
        els.append(Paragraph(_t(f"{active_mods}/18 Aktif Modul | {total_records:,} Toplam Kayit"),
                              s_sub))
        els.append(Paragraph(_t(f"Olusturma Tarihi: {time.strftime('%d.%m.%Y %H:%M')}"), s_small))
        els.append(PageBreak())

        # ═══ ICINDEKILER ═══
        els.append(Paragraph(_t("Icindekiler"), s_h1))
        toc_items = [
            "1. Genel Bakis ve Kurum Skoru",
            "2. Akademik Takip Modulu",
            "3. Olcme ve Degerlendirme Modulu",
            "4. Insan Kaynaklari Yonetimi",
            "5. Rehberlik Modulu",
            "6. Okul Sagligi Takip",
            "7. Butce Gelir Gider",
            "8. Tuketim ve Demirbas",
            "9. Toplanti ve Kurullar",
            "10. Sosyal Etkinlik ve Kulupler",
            "11. Destek Hizmetleri Takip",
            "12. Randevu ve Ziyaretci",
            "13. Sivil Savunma ve IS Guvenligi",
            "14. Kutuphane",
            "15. Dijital Kutuphane",
            "16. Egitim Koclugu",
            "17. Erken Uyari Sistemi",
            "18. Kayit Modulu",
            "19. CEFR Seviye Tespit",
            "20. AI Destek — Merkez Beyni",
            "21. Yabanci Dil Modulu",
            "22. Tavsiyeler ve Yol Haritasi",
        ]
        for item in toc_items:
            els.append(Paragraph(_t(item), s_bullet))
        els.append(PageBreak())

        # ═══ KURUM DURUM TABLOSU ═══
        els.append(Paragraph(_t("Kurum Durum Ozeti"), s_h1))

        # Gercek veri tablosu
        tbl_header_style = ParagraphStyle("THdr", fontName=fb, fontSize=8, leading=10,
                                           textColor=rl.white, alignment=1)
        tbl_cell_style = ParagraphStyle("TCell", fontName=fn, fontSize=7.5, leading=10, alignment=1)

        mod_summary = [
            ["Akademik Takip", str(data.get("akademik", {}).get("students_aktif", 0)), "ogrenci"],
            ["Olcme Degerlendirme", str(data.get("olcme", {}).get("questions_count", 0)), "soru"],
            ["Insan Kaynaklari", str(data.get("ik", {}).get("employees_aktif", 0)), "personel"],
            ["Rehberlik", str(_safe_len(data.get("rehberlik", {}).get("gorusmeler", []))), "gorusme"],
            ["Okul Sagligi", str(_safe_len(data.get("saglik", {}).get("revir", []))), "ziyaret"],
            ["Butce", f"{data.get('butce', {}).get('toplam_gelir', 0):,.0f} / {data.get('butce', {}).get('toplam_gider', 0):,.0f}", "gelir/gider TL"],
            ["Tuketim Demirbas", str(_safe_len(data.get("tdm", {}).get("urunler", []))), "urun"],
            ["Toplanti", str(_safe_len(data.get("toplanti", {}).get("meetings", []))), "toplanti"],
            ["Sosyal Etkinlik", str(_safe_len(data.get("sosyal", {}).get("kulupler", []))), "kulup"],
            ["Destek Hizmetleri", str(_safe_len(data.get("destek", {}).get("tickets", []))), "talep"],
            ["Erken Uyari", str(_safe_len(data.get("erken_uyari", {}).get("risks", []))), "risk kaydi"],
            ["CEFR Placement", str(_safe_len(data.get("cefr", {}).get("results", []))), "sonuc"],
        ]

        tbl_data = [[Paragraph(_t("<b>Modul</b>"), tbl_header_style),
                      Paragraph(_t("<b>Deger</b>"), tbl_header_style),
                      Paragraph(_t("<b>Birim</b>"), tbl_header_style)]]
        for row in mod_summary:
            tbl_data.append([Paragraph(_t(row[0]), tbl_cell_style),
                             Paragraph(_t(row[1]), tbl_cell_style),
                             Paragraph(_t(row[2]), tbl_cell_style)])

        tbl = Table(tbl_data, colWidths=[pw*0.45, pw*0.3, pw*0.25], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#1e1b4b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, rl.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("FONTNAME", (0, 1), (-1, -1), fn),
            ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ]))
        # Zebra rows
        for i in range(2, len(tbl_data), 2):
            tbl.setStyle(TableStyle([("BACKGROUND", (0, i), (-1, i), rl.HexColor("#f8fafc"))]))
        els.append(tbl)
        els.append(Spacer(1, 0.5*cm))

        # Ders bazli not tablosu
        grades_pdf = data.get("akademik", {}).get("grades", [])
        if grades_pdf:
            els.append(Paragraph(_t("Ders Bazli Not Analizi"), s_h2))
            ders_puanlar: dict[str, list] = {}
            for g in grades_pdf:
                ders = getattr(g, "ders", "") if not isinstance(g, dict) else g.get("ders", "")
                puan = getattr(g, "puan", 0) if not isinstance(g, dict) else g.get("puan", 0)
                try:
                    ders_puanlar.setdefault(ders, []).append(float(puan))
                except (TypeError, ValueError):
                    pass
            if ders_puanlar:
                dtbl_data = [[Paragraph(_t("<b>Ders</b>"), tbl_header_style),
                              Paragraph(_t("<b>Not Sayisi</b>"), tbl_header_style),
                              Paragraph(_t("<b>Ortalama</b>"), tbl_header_style),
                              Paragraph(_t("<b>Min</b>"), tbl_header_style),
                              Paragraph(_t("<b>Max</b>"), tbl_header_style)]]
                for d, p in sorted(ders_puanlar.items()):
                    dtbl_data.append([
                        Paragraph(_t(d), tbl_cell_style),
                        Paragraph(_t(str(len(p))), tbl_cell_style),
                        Paragraph(_t(f"{sum(p)/len(p):.1f}"), tbl_cell_style),
                        Paragraph(_t(f"{min(p):.0f}"), tbl_cell_style),
                        Paragraph(_t(f"{max(p):.0f}"), tbl_cell_style),
                    ])
                dtbl = Table(dtbl_data, colWidths=[pw*0.3, pw*0.15, pw*0.2, pw*0.15, pw*0.2], repeatRows=1)
                dtbl.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#2563eb")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), rl.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.4, rl.HexColor("#e2e8f0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("FONTNAME", (0, 1), (-1, -1), fn),
                    ("FONTSIZE", (0, 1), (-1, -1), 7.5),
                ]))
                els.append(dtbl)
                els.append(Spacer(1, 0.3*cm))

        els.append(PageBreak())

        # ═══ MODUL DETAYLARI ═══
        modules_info = [
            ("Akademik Takip", "akademik",
             "Ogrenci yonetimi, not takibi, devamsizlik, ders programi, ogretmen yonetimi, "
             "odev takip, yoklama, kazanim izleme ve raporlama.",
             ["Kadro & Ogrenci — Ogrenci/ogretmen kayit ve yonetim",
              "Nobet Yonetimi — Ogretmen nobet cizelgesi",
              "Zaman Cizelgesi — Gunluk program (ders, teneffus, ogle, etut)",
              "Ders & Program — Otomatik ders dagitimi, ogretmen atama",
              "Ogretim & Planlama — Yillik/aylik/haftalik plan, mufredat agaci",
              "Ders Defteri — Gunluk ders kaydi, kurumsal karne",
              "Dijital Ogrenme & Online Ders — LMS entegrasyonu",
              "Odev Takip — Odev verme, online teslim (dosya/link/video/QR)",
              "Yoklama & Devamsizlik — Gunluk/ders bazli, 3 seviye uyari",
              "Not Girisi — Tekli/toplu, donem bazli",
              "Raporlar — Karne, siralama, devamsizlik, ders analizi",
              "Erken Uyari — Riskli ogrenci tespiti, mudahale plani",
              "Kazanim Takip (KYT) — Kazanim izleme, soru havuzu, test"]),
            ("Olcme ve Degerlendirme", "olcme",
             "Soru bankasi, sinav olusturma, otomatik puanlama, sonuc analizi, "
             "AI ile soru uretimi, MEB yillik plan entegrasyonu.",
             ["Kazanim Yonetimi — CRUD, import, MEB uyumlu",
              "Soru Olusturma Sihirbazi — 5 adim, 7 soru tipi",
              "Kalite Degerlendirme — Otomatik kalite skoru",
              "Soru Bankasi — Kategori sistemi, ay filtresi",
              "Sinav Blueprint — Sablon sistemi, AI ile 20 kademe",
              "Online Sinav — Ogrenci girisi, sinav cozme, tab guvenlik",
              "Otomatik Puanlama — Negatif puanlama destegi",
              "Sonuc Analizi — Istatistik, siralama, zorluk",
              "PDF Sinav Export — OSYM tarzi 2 sutunlu, optik form",
              "Telafi Sistemi — RED/YELLOW/GREEN/BLUE renk bandi",
              "Stok Kontrol — Otomatik soru uretimi ile doldurma"]),
            ("Insan Kaynaklari Yonetimi", "ik",
             "Personel yonetimi, ise alim, performans degerlendirme, izin takibi, "
             "maas bordro, egitim ve disiplin yonetimi.",
             ["Genel Bakis — KPI dashboard",
              "Aday Havuzu — Basvuru yonetimi, CV arsivi",
              "Mulakat — Planlama, form, degerlendirme",
              "Onboarding — Oryantasyon, belge toplama",
              "Aktif Calisanlar — Personel listesi, pozisyon",
              "Performans — 360 derece degerlendirme",
              "Izin Yonetimi — Talep, onay, bakiye",
              "Maas & Bordro — Hesaplama, ek odeme, kesinti",
              "Egitim & Sertifika — Kurum ici egitim, takvim",
              "Disiplin — Uyari, tutanak, surec takibi",
              "Offboarding — Devir teslim, cikis mulakati"]),
            ("Rehberlik", "rehberlik",
             "Bireysel gorusme, vaka takip, aile gorusmesi, BEP, "
             "test/envanter, risk degerlendirme.",
             ["Dashboard — Genel bakis, istatistikler",
              "Gorusme Kayitlari — Bireysel, notlar, takip plani",
              "Vaka Takip — Acma/kapama, mudahale plani",
              "Aile Gorusmeleri — Veli gorusme, kararlar",
              "Yonlendirme — RAM, hastane, uzman",
              "BEP — Bireysellestirilmis Egitim Programi",
              "Test ve Envanter — Psikolojik test uygulama",
              "Risk Degerlendirme — Riskli ogrenci tespiti"]),
            ("Okul Sagligi Takip", "saglik",
             "Saglik karti, revir ziyareti, ilac uygulama, kaza/olay kaydi, envanter.",
             ["Saglik Karti — Alerji, kronik hastalik, asi takibi",
              "Revir Ziyareti — Kayit, teshis, yonlendirme",
              "Ilac Uygulama — Dozaj, veli izin formu",
              "Kaza/Olay — Tutanak, bildirim",
              "Envanter — Tibbi malzeme stok takibi",
              "Ilk Yardim Dolaplari — Kontrol, son kullanma tarihi"]),
            ("Butce Gelir Gider", "butce",
             "Yillik butce planlama, gelir/gider kaydi, tahmini-gerceklesen karsilastirma.",
             ["Butce Planlama — Yillik/donemsel, kalem bazli",
              "Gelir Kayit — Ogretim ucreti, bagis, etkinlik",
              "Gider Kayit — Personel, kira, malzeme, bakim",
              "Tahmini vs Gerceklesen — Sapma analizi",
              "Aylik Takip — Nakit akis tablosu",
              "Raporlar — Finansal analiz, trend grafikleri"]),
            ("Tuketim ve Demirbas", "tdm",
             "Gunluk tuketim takibi, stok yonetimi, demirbas envanter, zimmet, satin alma.",
             ["Gunluk Tuketim — Malzeme tuketim kaydi",
              "Stok Durumu — Anlik stok, min stok uyari",
              "Demirbas Kayit — Barkod, lokasyon, durum",
              "Zimmet Yonetimi — Personel zimmet atama/iade",
              "Satin Alma — Talep, onay, tedarikci secimi",
              "AI Tavsiye — Stok ve satin alma onerileri"]),
            ("Toplanti ve Kurullar", "toplanti",
             "Toplanti planlama, gundem takibi, karar kaydi, aksiyon atama.",
             ["Toplanti Yonetimi — Tur, tarih, katilimci, gundem",
              "Toplanti Yurutme — Yoklama, karar, aksiyon",
              "Raporlar — Istatistik, aksiyon takibi",
              "Sablonlar — Gundem ve tutanak sablonlari"]),
            ("Sosyal Etkinlik ve Kulupler", "sosyal",
             "Kulup yonetimi, sosyal etkinlik planlama, katilim takibi.",
             ["Kulupler — Olusturma, danisman, uye yonetimi",
              "Etkinlikler — Gezi, toren, yarisma, konser",
              "Raporlar — Katilim analizi, performans"]),
            ("Destek Hizmetleri Takip", "destek",
             "Ariza/tadilat/temizlik talep yonetimi, periyodik isler, denetim.",
             ["Talepler — Olusturma, oncelik, atama, durum",
              "Periyodik Isler — Tekrarlayan gorev, hatirlatma",
              "Denetimler — Denetim formu, puanlama, aksiyon",
              "Periyodik Bakim — Ekipman bakim takvimi",
              "Firma Havuzu — Dis hizmet firma kayitlari"]),
            ("Randevu ve Ziyaretci", "randevu",
             "Randevu yonetimi, ziyaretci giris/cikis, gorusme notlari.",
             ["Randevu Yonetimi — Olusturma, onay/red",
              "Ziyaretci Giris/Cikis — Kayit, kimlik",
              "Gorusme Notlari — Kayit, takip plani"]),
            ("Sivil Savunma ve IS Guvenligi", "ssg",
             "Tatbikat planlama, risk degerlendirme, ISG egitimi, olay kaydi.",
             ["Tatbikat — Planlama, kayit, tahliye plani",
              "ISG — Risk degerlendirme, koruyucu ekipman",
              "Olay Kayitlari — Guvenlik olayi, tutanak",
              "Denetimler — Eylem planlari"]),
            ("Kutuphane", "kutuphane",
             "Materyal kaydi, odunc islemleri, stok takibi.",
             ["Kayitli Materyaller — Kitap/dergi/DVD, barkod",
              "Odunc Islemleri — Verme, iade, uzatma",
              "Odunc Takip — Geciken iade, hatirlatma",
              "Analiz — Okuma istatistikleri, populer kitaplar"]),
            ("Dijital Kutuphane", "dijital_kutuphane",
             "Dijital egitim kaynaklari, kademe bazli erisim.",
             ["Dijital Kaynaklar — Video, PDF, interaktif icerik",
              "Kullanim Loglari — Erisim takibi"]),
            ("Egitim Koclugu", "egitim_koclugu",
             "Bireysel ogrenci koclugu, hedef belirleme, deneme analizi.",
             ["Ogrenci Eslestirme — Koc-ogrenci atama",
              "Gorusmeler — Bireysel kocluk gorusmesi",
              "Hedefler — Hedef belirleme ve takip",
              "Deneme Analizleri — Deneme sinav analiz"]),
            ("Erken Uyari Sistemi", "erken_uyari",
             "9 farkli risk faktoru ile ogrenci risk tespiti, otomatik uyari.",
             ["Risk Hesaplama — Not, devamsizlik, sinav, odev, kazanim borcu, "
              "rehberlik, saglik, trend, davranis + CEFR verisi",
              "Risk Seviyeleri — Dusuk/Orta/Yuksek/Kritik",
              "Otomatik Uyari — Esik asiminda uyari uretimi",
              "Mudahale Plani — Aksiyon onerisi"]),
            ("Kayit Modulu", "kayit",
             "Ogrenci kayit surec takibi — aday, arama, gorusme, fiyat, sozlesme, kesin kayit.",
             ["Pipeline — 7 asamali surec (aday → kesin kayit)",
              "Arama Takibi — 5 arama hakki, ulasim durumu",
              "Gorusme Planlama — Tarih, saat, not",
              "Fiyat Teklifi — Hesaplama, ek hizmetler",
              "Sozlesme — MEB format, PDF uretimi",
              "Sinif Listesine Aktarim — Otomatik ogrenci olusturma"]),
            ("CEFR Seviye Tespit", "cefr",
             "Sene Basi / Sene Sonu CEFR seviye olcumu — 4 beceri, seviye bazli puanlama.",
             ["Sinav Olusturma — Sinif/donem bazli, otomatik soru uretimi",
              "4 Bolum — Listening, Reading, Use of English, Writing",
              "Coklu Seviye — Hedef CEFR +/- 1 seviye test",
              "Otomatik Puanlama — Seviye bazli %60 esik",
              "AI Degerlendirme — GPT ile bireysel analiz raporu",
              "Karsilastirma — Sene Basi vs Sene Sonu ilerleme"]),
            ("AI Destek — Merkez Beyni", None,
             "35 modulden veri toplayan merkezi dashboard — 21 analiz motoru, 4 rol, 3 PDF.",
             ["YONETICI: 6 tab — Kurum Rontgeni (mega skor), DNA Profili, Gap Analizi (10 boyut), "
              "Kurum Endeksi (0-1000), Projeksiyon (3 senaryo), Maliyet-Fayda, Hedef Takip (10 hedef), "
              "Haftalik Plan, Segmentasyon, Anomali Tespiti, Derin Analiz (15 bulgu), "
              "Risk Matrisi, Benchmark, AI Rapor + 3 PDF",
              "OGRETMEN: 4 tab — Sinif Analizi, Ogrenci Drill-Down (radar+risk+tablo), "
              "Potansiyel Analizi, Haftalik Plan, AI Tavsiye",
              "VELI: 4 tab — Cocuk Not/Devamsizlik/Telafi verdict, Ders Radar, "
              "Gelisim Raporu (risk+CEFR), Haftalik Plan, Evde Yapilabilecekler",
              "OGRENCI: 4 tab — Kisisel Ders Radar, Motivasyonel Verdict, "
              "6 Hedef, 6 Adimli Gelisim Yolu, Haftalik Plan",
              "21 Analiz Motoru: Derin Analiz, Anomali, Segmentasyon, Endeks, "
              "Maliyet-Fayda, Veli Oncelik, Projeksiyon, Donem Karsilastirma, "
              "Hedef Takip, Haftalik Plan, Gap Analizi, Potansiyel, Sinif Karsilastirma, "
              "Ogretmen Etkinlik, Verdict, Ders Korelasyon, Stok Deger, "
              "Ogretmen Yuklenme, Modul Aktivite, Kurum DNA, Gunluk Oneri",
              "3 PDF: Kurumsal Kilavuz (72 KB) + AI Analiz Raporu (46 KB) + Kurum Karnesi (45 KB)",
              "Smarti Asistan — Sesli/yazili AI sohbet (tum roller)"]),
            ("Yabanci Dil Modulu", None,
             "Kurumsal dil ogretim platformu — CEFR uyumlu, 1-12. sinif, "
             "interaktif ders isleme, kitap uretimi.",
             ["Ders Isleme Motoru — Plan + 4 kitap + etkilesimli alistirma",
              "Kademe Bazli Icerik — Okul Oncesi, Ilkokul, Ortaokul, Lise",
              "36 Haftalik Plan — Yillik ders plani PDF",
              "Kitap Uretici — Main Course, Workbook, Reading, Vocabulary PDF",
              "Kelime Sistemi — SRS tekrar, AI konusma",
              "Okuma Kutuphanesi — Seviye bazli kitaplar",
              "Sinav/Degerlendirme — 36 hafta olcme, CEFR mock exam"]),
        ]

        for mod_name, data_key, desc, features in modules_info:
            els.append(Paragraph(_t(mod_name), s_h1))

            # Mevcut durum
            if data_key and data_key in data:
                mod_data = data[data_key]
                total = sum(_safe_len(v) for v in mod_data.values() if isinstance(v, list))
                status = "AKTIF" if total > 0 else "VERI GIRILMEMIS"
                s_clr = "#22c55e" if total > 0 else "#f59e0b"
                els.append(Paragraph(
                    _t(f'<font color="{s_clr}">Durum: {status} | {total} kayit</font>'),
                    s_body))

            els.append(Paragraph(_t(desc), s_body))

            # Akilli durum yorumu
            if data_key and data_key in data:
                mod_d = data[data_key]
                total = sum(_safe_len(v) for v in mod_d.values() if isinstance(v, list))
                if total == 0:
                    verdict = "AKSIYON GEREKLI: Bu modulde henuz veri girilmemis. Modulu aktif kullanima alin."
                    v_color = "#f59e0b"
                elif total < 5:
                    verdict = f"BASLANGIC: {total} kayit var. Veri girisi arttirilmali."
                    v_color = "#f97316"
                elif total < 50:
                    verdict = f"AKTIF: {total} kayit. Modul aktif kullaniliyor."
                    v_color = "#22c55e"
                else:
                    verdict = f"OLGUN: {total} kayit. Analitik ve raporlama icin yeterli veri."
                    v_color = "#6366f1"
                els.append(Paragraph(
                    _t(f'<font color="{v_color}">Yorum: {verdict}</font>'), s_body))

            els.append(Spacer(1, 0.2*cm))
            els.append(Paragraph(_t("Ozellikler ve Sekmeler:"), s_h2))
            for feat in features:
                els.append(Paragraph(_t(f"• {feat}"), s_bullet))
            els.append(Spacer(1, 0.3*cm))

        # ═══ TAVSİYELER ═══
        els.append(PageBreak())
        # ═══ DERİN ANALİZ BULGULARI ═══
        analysis = _deep_rule_analysis(data)

        # ═══ GAP ANALİZİ ═══
        gaps = _gap_analysis(data)
        els.append(Paragraph(_t("Olmasi Gereken vs Mevcut Durum — Gap Analizi"), s_h1))
        ok_g = sum(1 for g in gaps if g["durum"] == "OK")
        risk_g = sum(1 for g in gaps if g["durum"] == "RISK")
        gel_g = sum(1 for g in gaps if g["durum"] == "GELISMELI")
        els.append(Paragraph(_t(f"Hedefte: {ok_g} | Gelismeli: {gel_g} | Risk: {risk_g} — Toplam {len(gaps)} boyut"), s_body))
        els.append(Spacer(1, 0.2*cm))

        for g in sorted(gaps, key=lambda x: -x["gap_pct"]):
            d_label = {"OK": "HEDEFTE", "GELISMELI": "GELISMELI", "RISK": "RISK"}.get(g["durum"], "?")
            d_color = {"OK": "#22c55e", "GELISMELI": "#f59e0b", "RISK": "#ef4444"}.get(g["durum"], "#64748b")
            els.append(Paragraph(_t(f'<font color="{d_color}">[{d_label}] {g["alan"]} — Gap: %{g["gap_pct"]}</font>'), s_body))
            els.append(Paragraph(_t(f'  Ideal: {g["ideal"]}'), s_small))
            els.append(Paragraph(_t(f'  Mevcut: {g["mevcut"]}'), s_small))
            els.append(Paragraph(_t(f'  Sure: {g["timeline"]} | Maliyet: {g["maliyet"]} | Etki: %{g["etki"]}'), s_small))
            for c in g["cozum"][:3]:
                els.append(Paragraph(_t(f'    - {c}'), s_small))
            els.append(Spacer(1, 0.15*cm))

        els.append(PageBreak())
        els.append(Paragraph(_t("Otomatik Analiz Bulgulari"), s_h1))
        for sev, icon, title, detail, action in analysis.get("findings", []):
            sev_label = {"critical": "KRITIK", "warning": "UYARI", "info": "BILGI"}.get(sev, "")
            sev_color = {"critical": "#ef4444", "warning": "#f59e0b", "info": "#3b82f6"}.get(sev, "#64748b")
            els.append(Paragraph(_t(f'<font color="{sev_color}">[{sev_label}] {title}</font>'), s_body))
            els.append(Paragraph(_t(f'  {detail}'), s_small))
            els.append(Paragraph(_t(f'  Aksiyon: {action}'), s_small))
            els.append(Spacer(1, 0.15*cm))

        if analysis.get("cross_insights"):
            els.append(Spacer(1, 0.3*cm))
            els.append(Paragraph(_t("Moduller Arasi Iliskiler"), s_h2))
            for ci in analysis["cross_insights"]:
                els.append(Paragraph(_t(f'  {ci}'), s_body))

        if analysis.get("risk_matrix"):
            els.append(Spacer(1, 0.3*cm))
            els.append(Paragraph(_t("Risk Matrisi"), s_h2))
            for etki, olasilik, baslik in sorted(analysis["risk_matrix"], key=lambda x: x[0]*x[1], reverse=True):
                risk_skor = etki * olasilik
                els.append(Paragraph(_t(f'  [{risk_skor}/25] {baslik} (Etki:{etki} x Olasilik:{olasilik})'), s_body))

        els.append(PageBreak())
        els.append(Paragraph(_t("Tavsiyeler ve Yol Haritasi"), s_h1))

        # Derin analiz roadmap
        if analysis.get("roadmap"):
            els.append(Paragraph(_t("Oncelikli Aksiyon Plani (Kural Bazli)"), s_h2))
            for pri, timeframe, title, detail in analysis["roadmap"]:
                pri_color = {"ACIL": "#ef4444", "YUKSEK": "#f97316", "ORTA": "#f59e0b"}.get(pri, "#64748b")
                els.append(Paragraph(
                    _t(f'<font color="{pri_color}">[{pri} — {timeframe}]</font> {title}: {detail}'), s_body))
            els.append(Spacer(1, 0.3*cm))

        bos_moduls = []
        for mod_name, data_key, _, _ in modules_info:
            if data_key and data_key in data:
                total = sum(_safe_len(v) for v in data[data_key].values() if isinstance(v, list))
                if total == 0:
                    bos_moduls.append(mod_name)

        if bos_moduls:
            els.append(Paragraph(_t("Veri Girilmemis Moduller:"), s_h2))
            for m in bos_moduls:
                els.append(Paragraph(_t(f"• {m} — Bu modulde henuz veri girilmemis. "
                                        f"Aktif kullanima alinmasi onerilir."), s_bullet))

        els.append(Spacer(1, 0.5*cm))
        els.append(Paragraph(_t("Kisa Vadeli Aksiyonlar (1-3 Ay):"), s_h2))
        short_term = [
            "Tum modullere veri girisi baslatin — bos moduller sistemin degerini dusurur",
            "Erken Uyari Sistemi sonuclarini inceleyin — riskli ogrenciler icin mudahale plani olusturun",
            "CEFR Seviye Tespit sinavlarini baslatin — Sene Basi olcumu yapin",
            "IK modulunde tum personeli kaydedin — performans ve izin takibi icin",
            "Butce modulune gelir kayitlarini girin — mali durum analizi icin",
        ]
        for item in short_term:
            els.append(Paragraph(_t(f"• {item}"), s_bullet))

        els.append(Spacer(1, 0.5*cm))
        els.append(Paragraph(_t("Uzun Vadeli Hedefler (6-12 Ay):"), s_h2))
        long_term = [
            "Tum 18 modulun aktif kullanima alinmasi — %100 veri kapsami hedefi",
            "AI Destek Merkez Beyni ile duzenli kurum analizi — aylik rapor dongusu",
            "Veli ve ogrenci panellerinin aktif kullanimi — iletisim ve takip",
            "Sivil Savunma tatbikatlarinin planlanmasi — yasal zorunluluk",
            "Dijital Kutuphane iceriklerinin zenginlestirilmesi",
            "Egitim Koclugu programinin baslatilmasi — bireysel destek",
        ]
        for item in long_term:
            els.append(Paragraph(_t(f"• {item}"), s_bullet))

        # ═══ FOOTER ═══
        def _footer(canvas, doc_obj):
            canvas.saveState()
            canvas.setFont(fn, 7)
            canvas.setFillColor(rl.HexColor("#94A3B8"))
            canvas.drawString(2*cm, 1.2*cm,
                              _t(f"SmartCampus AI — Kurumsal Kilavuz | {time.strftime('%d.%m.%Y')}"))
            canvas.drawRightString(A4[0] - 2*cm, 1.2*cm, _t(f"Sayfa {doc_obj.page}"))
            canvas.setStrokeColor(rl.HexColor("#e2e8f0"))
            canvas.setLineWidth(0.5)
            canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)
            canvas.restoreState()

        doc.build(els, onFirstPage=_footer, onLaterPages=_footer)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"PDF olusturma hatasi: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SMARTİ ASISTAN (MEVCUT CHAT)
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_ai_analysis_pdf(data: dict, ai_text: str) -> bytes | None:
    """AI analiz raporunu kurumsal PDF olarak uret — kurum skoru + KPI + AI metin."""
    try:
        import io as _io
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from utils.shared_data import ensure_turkish_pdf_fonts

        fn, fb = ensure_turkish_pdf_fonts()
        buf = _io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                topMargin=1.5*cm, bottomMargin=2*cm,
                                leftMargin=2*cm, rightMargin=2*cm)
        pw = A4[0] - 4*cm
        els = []

        s_title = ParagraphStyle("AT", fontName=fb, fontSize=20, leading=26,
                                  alignment=1, textColor=rl.HexColor("#1e1b4b"), spaceAfter=6)
        s_sub = ParagraphStyle("AS", fontName=fn, fontSize=10, leading=13,
                                alignment=1, textColor=rl.HexColor("#64748b"), spaceAfter=16)
        s_h1 = ParagraphStyle("AH1", fontName=fb, fontSize=14, leading=18,
                               textColor=rl.HexColor("#1e1b4b"), spaceBefore=14, spaceAfter=6)
        s_h2 = ParagraphStyle("AH2", fontName=fb, fontSize=11, leading=14,
                               textColor=rl.HexColor("#6366f1"), spaceBefore=8, spaceAfter=4)
        s_body = ParagraphStyle("AB", fontName=fn, fontSize=9, leading=13, spaceAfter=4)
        s_small = ParagraphStyle("ASm", fontName=fn, fontSize=7.5, leading=10,
                                  textColor=rl.HexColor("#64748b"))

        def _t(text):
            return str(text) if fn != "Helvetica" else str(text).translate(
                str.maketrans("ıİğĞüÜşŞöÖçÇ", "iIgGuUsSoOcC"))

        # Kapak
        els.append(Spacer(1, 2.5*cm))
        els.append(Paragraph(_t("SmartCampus AI"), s_title))
        els.append(Paragraph(_t("AI Destekli Kurum Analiz Raporu"), ParagraphStyle(
            "ACover", fontName=fb, fontSize=13, leading=17, alignment=1,
            textColor=rl.HexColor("#6366f1"), spaceAfter=12)))

        inst = _compute_institution_score(data)
        els.append(Paragraph(_t(f"Kurum Saglik Skoru: %{inst['overall']:.0f}"),
                              ParagraphStyle("AScore", fontName=fb, fontSize=18, leading=24,
                                             alignment=1, textColor=rl.HexColor(
                                                 "#22c55e" if inst["overall"] >= 60 else "#f59e0b"),
                                             spaceAfter=8)))

        score_text = " | ".join(f"{k}: %{v:.0f}" for k, v in inst["scores"].items())
        els.append(Paragraph(_t(score_text), s_small))
        els.append(Spacer(1, 0.5*cm))
        els.append(Paragraph(_t(f"Rapor Tarihi: {time.strftime('%d.%m.%Y %H:%M')}"), s_small))
        els.append(Paragraph(_t("GPT-4o-mini tarafindan 18 modul verisi analiz edilmistir."), s_small))
        els.append(PageBreak())

        # KPI Tablosu
        els.append(Paragraph(_t("Modul KPI Ozeti"), s_h1))
        kpi_text = _build_ai_kpi_summary(data)
        for line in kpi_text.split("\n"):
            line = line.strip()
            if line and not line.startswith("="):
                els.append(Paragraph(_t(line), s_body))
        els.append(PageBreak())

        # AI Analiz Metni
        els.append(Paragraph(_t("AI Destekli Degerlendirme"), s_h1))
        # Markdown'u basit paragraflara cevir
        for line in ai_text.split("\n"):
            line = line.strip()
            if not line:
                els.append(Spacer(1, 0.2*cm))
            elif line.startswith("## "):
                els.append(Paragraph(_t(line[3:]), s_h2))
            elif line.startswith("# "):
                els.append(Paragraph(_t(line[2:]), s_h1))
            elif line.startswith("- ") or line.startswith("* "):
                els.append(Paragraph(_t(f"  {line}"), s_body))
            else:
                # Markdown bold/italic temizle
                clean = line.replace("**", "").replace("*", "").replace("###", "").replace("##", "")
                els.append(Paragraph(_t(clean), s_body))

        # Footer
        def _footer(canvas, doc_obj):
            canvas.saveState()
            canvas.setFont(fn, 7)
            canvas.setFillColor(rl.HexColor("#94A3B8"))
            canvas.drawString(2*cm, 1.2*cm,
                              _t(f"SmartCampus AI — AI Analiz Raporu | {time.strftime('%d.%m.%Y')}"))
            canvas.drawRightString(A4[0] - 2*cm, 1.2*cm, _t(f"Sayfa {doc_obj.page}"))
            canvas.setStrokeColor(rl.HexColor("#e2e8f0"))
            canvas.setLineWidth(0.5)
            canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)
            canvas.restoreState()

        doc.build(els, onFirstPage=_footer, onLaterPages=_footer)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"AI PDF olusturma hatasi: {e}")
        return None


def _render_tab_chat(client, system_msg, mascot_avatar):
    """Mevcut Smarti sohbet arayuzu — aynen korundu."""
    # Session state
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
    if "ai_audio_cache" not in st.session_state:
        st.session_state.ai_audio_cache = {}
    if "ai_voice_mode" not in st.session_state:
        st.session_state.ai_voice_mode = False
    if "ai_last_audio_hash" not in st.session_state:
        st.session_state.ai_last_audio_hash = None
    if "ai_greeted" not in st.session_state:
        st.session_state.ai_greeted = False

    # Kontroller
    ctrl1, ctrl2, ctrl3 = st.columns([1.5, 1.5, 3])
    with ctrl1:
        if st.session_state.ai_voice_mode:
            if st.button("Sesli Konusmayi Durdur", key="ai_stop_voice",
                         type="secondary", use_container_width=True):
                st.session_state.ai_voice_mode = False
                st.session_state.ai_last_audio_hash = None
                st.rerun()
        else:
            if st.button("Sesli Konusmayi Baslat", key="ai_start_voice",
                         type="primary", use_container_width=True):
                st.session_state.ai_voice_mode = True
                st.session_state.ai_last_audio_hash = None
                st.rerun()
    with ctrl2:
        if st.button("Sohbeti Temizle", key="ai_clear_chat", use_container_width=True):
            st.session_state.ai_chat_history = []
            st.session_state.ai_audio_cache = {}
            st.session_state.ai_last_audio_hash = None
            st.session_state.ai_greeted = False
            st.rerun()

    st.markdown("---")

    # Otomatik karsilama
    from datetime import datetime as _dt
    _saat = _dt.now().hour
    if _saat < 6: _zaman = "Iyi geceler"
    elif _saat < 12: _zaman = "Gunaydin"
    elif _saat < 17: _zaman = "Iyi gunler"
    elif _saat < 21: _zaman = "Iyi aksamlar"
    else: _zaman = "Iyi geceler"

    auth_user = st.session_state.get("auth_user", {})
    hitap = auth_user.get("name", "Kullanici").split()[0]

    greeting_text = f"{_zaman} {hitap}! Ben Smarti, senin dijital egitim arkadasin! Bugün sana nasil yardimci olabilirim?"

    with st.chat_message("assistant", avatar=mascot_avatar):
        st.markdown(f"**{_zaman}, {hitap}!**\n\nBen **Smarti**, senin dijital egitim arkadasin! "
                    f"Yazarak ya da **sesli konusarak** sohbet edebilirsin.")

    if not st.session_state.ai_greeted:
        st.session_state.ai_greeted = True
        with st.spinner("Smarti hazirlaniyor..."):
            greeting_audio = _text_to_speech(client, greeting_text)
        if greeting_audio:
            st.session_state.ai_audio_cache["greeting"] = greeting_audio
            st.audio(greeting_audio, format="audio/mp3", autoplay=True)
    elif "greeting" in st.session_state.ai_audio_cache:
        st.audio(st.session_state.ai_audio_cache["greeting"], format="audio/mp3")

    # Gecmis mesajlar
    for i, msg in enumerate(st.session_state.ai_chat_history):
        avatar = mascot_avatar if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and not st.session_state.ai_voice_mode:
                audio_key = f"audio_{i}"
                if audio_key in st.session_state.ai_audio_cache:
                    st.audio(st.session_state.ai_audio_cache[audio_key], format="audio/mp3")
                else:
                    if st.button("Seslendir", key=f"tts_btn_{i}"):
                        with st.spinner("Ses olusturuluyor..."):
                            audio = _text_to_speech(client, msg["content"])
                            if audio:
                                st.session_state.ai_audio_cache[audio_key] = audio
                                st.audio(audio, format="audio/mp3", autoplay=True)

    # Sesli konusma modu
    if st.session_state.ai_voice_mode:
        st.markdown(
            '<div class="voice-active-banner">'
            'Sesli Konusma Aktif - Konusmaya baslayin'
            '<div class="subtitle">Konusmaniz bitince otomatik algilanacak</div>'
            '</div>', unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            text="", recording_color="#ef4444", neutral_color="#7c3aed",
            icon_size="3x", pause_threshold=2.5, auto_start=True, key="ai_voice_recorder")
        if audio_bytes:
            current_hash = _audio_hash(audio_bytes)
            if current_hash != st.session_state.ai_last_audio_hash:
                st.session_state.ai_last_audio_hash = current_hash
                with st.spinner("Ses taniniyor..."):
                    voice_text = _speech_to_text(client, audio_bytes)
                if voice_text:
                    _process_user_input(client, voice_text, system_msg, mascot_avatar)
                    st.rerun()
                else:
                    st.info("Ses anlasilamadi, lutfen tekrar deneyin.")
    else:
        text_input = st.chat_input("Mesajinizi yazin...", key="ai_chat_input")
        if text_input:
            _process_user_input(client, text_input, system_msg, mascot_avatar)


# ═══════════════════════════════════════════════════════════════════════════════
# YONETICI DASHBOARD — ANA ORKESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# OGRETMEN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def _render_teacher_dashboard(client, system_msg, mascot_avatar, auth_user):
    """Ogretmen: Kendi siniflarinin analizi + ogrenci basarisi + odev + tavsiye."""
    inject_pro_css("ai_teacher")
    from models.akademik_takip import AkademikDataStore
    ak = AkademikDataStore()
    name = auth_user.get("name", "")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e3a5f,#1e1b4b);border-radius:16px;
    padding:20px 24px;margin-bottom:16px;border:1.5px solid rgba(59,130,246,0.3);">
    <div style="font-size:1.3rem;font-weight:900;color:#93c5fd;">Ogretmen Analiz Paneli</div>
    <div style="font-size:.85rem;color:#60a5fa;margin-top:4px;">
    Siniflarinizin performansi, ogrenci analizleri ve kisisel gelisim yol haritasi</div>
    </div>""", unsafe_allow_html=True)

    # Gunluk oneriler
    daily = _smart_daily_recommendations(data={}, role="Öğretmen")
    _render_daily_recommendations(daily)

    tabs = st.tabs(["📊 Sinif Analizim", "👨‍🎓 Ogrenci Detay", "🤖 AI Tavsiyeler", "📚 Ders Planı Copilot", "💬 Smarti"])

    # ── TAB 1: Sinif Analizi ──
    with tabs[0]:
        students = ak.get_students(durum="aktif")
        grades = ak.get_grades()
        attendance = ak.get_attendance()
        teachers = ak.get_teachers()
        odevler = ak.get_odevler()

        styled_stat_row([
            ("Toplam Ogrenci", str(len(students)), "#2563eb", "🎓"),
            ("Toplam Ogretmen", str(len(teachers)), "#7c3aed", "👨‍🏫"),
            ("Not Kaydi", str(len(grades)), "#10b981", "📝"),
            ("Devamsizlik", str(len(attendance)), "#f59e0b", "📋"),
            ("Odev", str(len(odevler)), "#6366f1", "📓"),
        ])

        # Ders bazli not analizi
        if grades:
            st.markdown("#### Ders Bazli Basari Analizi")
            ders_puanlar: dict[str, list] = {}
            for g in grades:
                ders = getattr(g, "ders", "")
                puan = getattr(g, "puan", 0)
                try:
                    ders_puanlar.setdefault(ders, []).append(float(puan))
                except (TypeError, ValueError):
                    pass

            if ders_puanlar:
                import pandas as pd
                df = pd.DataFrame([{
                    "Ders": d, "Not": len(p), "Ort": round(sum(p)/len(p), 1),
                    "Min": min(p), "Max": max(p),
                    "Durum": "Basarili" if sum(p)/len(p) >= 60 else "Gelismeli",
                } for d, p in sorted(ders_puanlar.items())])
                st.dataframe(df, use_container_width=True)

                # Verdict
                genel = sum(sum(p) for p in ders_puanlar.values()) / sum(len(p) for p in ders_puanlar.values())
                _verdict_card("Sinif Genel Ortalamasi", f"{genel:.1f}", "puan", _TH_SCORE)

            # Devamsizlik ozet
            if attendance:
                ozursuz = sum(1 for a in attendance if a.turu == "ozursuz")
                _verdict_card("Ozursuz Devamsizlik", str(ozursuz), "gun", _TH_COUNT_LOW, reverse=True)

        # Mini AI insight
        _mini_ai_insight(client,
                         f"Ogretmen {name}: {len(students)} ogrenci, {len(grades)} not, "
                         f"{len(attendance)} devamsizlik, {len(odevler)} odev",
                         "teacher_sinif")

    # ── TAB 2: Ogrenci Detay — Premium Drill-Down ──
    with tabs[1]:
        st.markdown("#### Ogrenci Secin — Bireysel Derin Analiz")

        # Sinif filtresi
        sinif_set = sorted(set(str(s.sinif) for s in students))
        ft1, ft2 = st.columns([1, 3])
        with ft1:
            tch_sinif = st.selectbox("Sinif", ["Tumu"] + sinif_set, key="tch_sinif_f")

        filtered_students = students if tch_sinif == "Tumu" else [s for s in students if str(s.sinif) == tch_sinif]
        stu_opts = {f"{s.tam_ad} ({s.sinif}/{s.sube})": s for s in filtered_students}
        sel = st.selectbox("Ogrenci", [""] + list(stu_opts.keys()), key="tch_stu_sel")

        if sel and sel in stu_opts:
            stu = stu_opts[sel]
            stu_grades = ak.get_grades(student_id=stu.id)
            stu_att = ak.get_attendance(student_id=stu.id)
            ozursuz_stu = sum(1 for a in stu_att if a.turu == "ozursuz")
            stu_ort = sum(g.puan for g in stu_grades) / len(stu_grades) if stu_grades else 0

            st.markdown(f"### {stu.tam_ad} — {stu.sinif}/{stu.sube} No:{stu.numara}")

            # Verdict satirı
            vc1, vc2, vc3 = st.columns(3)
            with vc1:
                _verdict_card("Not Ortalamasi", f"{stu_ort:.1f}", "puan", _TH_SCORE)
            with vc2:
                _verdict_card("Devamsizlik", str(len(stu_att)), "gun", _TH_COUNT_LOW, reverse=True)
            with vc3:
                _verdict_card("Ozursuz", str(ozursuz_stu), "gun",
                              [(0, "🏆", "#22c55e", "Temiz!"),
                               (3, "🟡", "#f59e0b", "Takip et"),
                               (10, "🔴", "#ef4444", "Veli gorusmesi gerekli")],
                              reverse=True)

            # Ders bazli not radar
            if stu_grades:
                st.markdown("#### Ders Bazli Performans Radari")
                ders_map: dict[str, list] = {}
                for g in stu_grades:
                    ders_map.setdefault(g.ders, []).append(g.puan)
                ders_ort = {d: round(sum(p)/len(p), 1) for d, p in ders_map.items()}

                fig_r = go.Figure()
                cats = list(ders_ort.keys())
                vals = list(ders_ort.values())
                fig_r.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]], theta=cats + [cats[0]],
                    fill="toself",
                    fillcolor="rgba(99,102,241,0.15)",
                    line=dict(color="#818cf8", width=2),
                    marker=dict(size=6),
                ))
                fig_r.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1e293b", showticklabels=False),
                               angularaxis=dict(tickfont=dict(size=10, color="#94a3b8"), gridcolor="#1e293b"),
                               bgcolor="rgba(0,0,0,0)"),
                    showlegend=False, height=300,
                    margin=dict(l=60, r=60, t=20, b=20),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_r, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

                # Not detay tablosu
                import pandas as pd
                df_stu = pd.DataFrame([{"Ders": d, "Ortalama": ort, "Not Sayisi": len(ders_map[d]),
                                         "Durum": "Basarili" if ort >= 60 else "Risk"}
                                        for d, ort in sorted(ders_ort.items())])
                st.dataframe(df_stu, use_container_width=True)

            # Risk bilgisi
            try:
                from models.erken_uyari import ErkenUyariStore
                eu_s = ErkenUyariStore()
                all_risks = eu_s.get_latest_risks()
                stu_risk = next((r for r in all_risks if r.get("student_id") == stu.id), None)
                if stu_risk:
                    st.markdown("#### Risk Profili")
                    r_cats = ["Not", "Devamsiz", "Sinav", "Odev", "Kazanim", "Rehberlik", "Saglik", "Trend", "Davranis"]
                    r_vals = [stu_risk.get("grade_risk", 0), stu_risk.get("attendance_risk", 0),
                              stu_risk.get("exam_risk", 0), stu_risk.get("homework_risk", 0),
                              stu_risk.get("outcome_debt_risk", 0), stu_risk.get("counseling_risk", 0),
                              stu_risk.get("health_risk", 0), stu_risk.get("trend_risk", 0),
                              stu_risk.get("behavior_risk", 0)]
                    fig_rr = go.Figure()
                    fig_rr.add_trace(go.Scatterpolar(
                        r=r_vals + [r_vals[0]], theta=r_cats + [r_cats[0]],
                        fill="toself", fillcolor="rgba(239,68,68,0.12)",
                        line=dict(color="#ef4444", width=2), marker=dict(size=5)))
                    fig_rr.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="#1e293b"),
                                   angularaxis=dict(tickfont=dict(size=9, color="#94a3b8"), gridcolor="#1e293b"),
                                   bgcolor="rgba(0,0,0,0)"),
                        showlegend=False, height=280,
                        margin=dict(l=60, r=60, t=10, b=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_rr, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

                    recs = stu_risk.get("recommendations", [])
                    if recs:
                        st.markdown("**Sistem Onerileri:**")
                        for rec in recs:
                            st.markdown(f"- {rec}")
            except Exception:
                pass

            _mini_ai_insight(client,
                             f"Ogrenci {stu.tam_ad}: ort={stu_ort:.1f}, "
                             f"{len(stu_att)} devamsizlik ({ozursuz_stu} ozursuz), "
                             f"dersler: {', '.join(f'{d}:{o}' for d, o in ders_ort.items()) if stu_grades else 'yok'}",
                             f"tch_stu_{stu.id}")

    # ── TAB 3: AI Tavsiyeler + Haftalik Plan ──
    with tabs[2]:
        styled_section("Ogretmen Gelisim ve Aksiyon Plani", "#6366f1")

        # Haftalik plan
        weekly = _weekly_action_plan({}, "Ogretmen")
        _render_weekly_plan(weekly)

        st.markdown("---")

        # Potansiyel analizi — kendi ogrencileri
        st.markdown("#### Potansiyel Analizi")
        st.caption("Guclu dersleri var ama zayif derslerde dusuk — kapasitesi yuksek ama kullanmiyor.")
        potentials = _student_potential_analysis({"akademik": {"grades": grades, "students": students}})
        if potentials:
            for p in potentials[:5]:
                st.markdown(f"""<div style="background:#0f172a;border-left:3px solid #f59e0b;
                border-radius:0 8px 8px 0;padding:8px 14px;margin:4px 0;">
                <div style="color:#fcd34d;font-weight:700;">{p['ad']} — {p['fark']:.0f} puan fark</div>
                <div style="color:#94a3b8;font-size:.82rem;">{p['yorum']}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Potansiyel farki olan ogrenci tespit edilemedi — daha fazla not girisi gerekli.")

        st.markdown("---")
        st.markdown("#### Yapabilecekleriniz")
        advice = [
            ("📝", "Odev modulunden duzenli odev verin", "Basariyi %15-20 arttirir"),
            ("📋", "Devamsiz ogrenci velileriyle iletisim kurun", "KOI > Iletisim'den mesaj gonderin"),
            ("📊", "KYT ile haftalik kazanim takibi yapin", "Akademik Takip > KYT sekmesi"),
            ("🌍", "CEFR Seviye Tespit sinavi uygulatin", "Yabanci Dil > CEFR Seviye Tespit"),
            ("🎯", "Risk grubu ogrencilere bireysel destek", "Egitim Koclugu modulunu kullanin"),
            ("🚀", "AI Treni, Matematik Koyu, Bilisim Vadisi onerin", "Ogrencilere zenginlestirme"),
            ("📖", "Okuma Kutuphanesi'nden kitap onerin", "Her ogrenci haftada 1 kitap"),
            ("🎨", "Sanat Sokagi etkinliklerine yonlendirin", "Yaraticilik ve motivasyon"),
        ]
        for icon, title, detail in advice:
            st.markdown(f"""<div style="display:flex;gap:10px;align-items:center;padding:6px 0;">
            <span style="font-size:1.2rem;">{icon}</span>
            <div><span style="color:#e2e8f0;font-weight:600;">{title}</span>
            <span style="color:#64748b;font-size:.78rem;margin-left:8px;">{detail}</span></div>
            </div>""", unsafe_allow_html=True)

        _mini_ai_insight(client,
                         f"Ogretmen {name}, {len(students)} ogrenci, "
                         f"hangi alanlarda gelisim onerilir?",
                         "teacher_advice")

    # ── TAB 4: Ders Planı Copilot ──
    with tabs[3]:
        try:
            from views._ders_plani_copilot import render_ders_plani_copilot
            render_ders_plani_copilot()
        except ImportError:
            st.info("Ders Planı Copilot modülü yüklü değil.")
        except Exception as _e:
            st.error(f"Ders Planı Copilot yüklenemedi: {_e}")

    # ── TAB 5: Smarti ──
    with tabs[4]:
        _render_tab_chat(client, system_msg, mascot_avatar)


# ═══════════════════════════════════════════════════════════════════════════════
# VELI DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def _render_parent_dashboard(client, system_msg, mascot_avatar, auth_user):
    """Veli: Cocugunun tam analizi + tavsiyeler + yol haritasi."""
    inject_pro_css("ai_parent")
    from models.akademik_takip import AkademikDataStore
    from models.olcme_degerlendirme import DataStore as ODS
    ak = AkademikDataStore()
    od = ODS()
    name = auth_user.get("name", "")
    username = auth_user.get("username", "")

    # Cocugu bul
    all_students = ak.get_students()
    children = [s for s in all_students if s.veli_adi and name.lower() in s.veli_adi.lower()]
    if not children:
        children = [s for s in all_students if s.veli_telefon and username in str(s.veli_telefon)]

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#14532d,#1e3a2f);border-radius:16px;
    padding:20px 24px;margin-bottom:16px;border:1.5px solid rgba(34,197,94,0.3);">
    <div style="font-size:1.3rem;font-weight:900;color:#86efac;">Veli Analiz Paneli</div>
    <div style="font-size:.85rem;color:#4ade80;margin-top:4px;">
    Cocugunuzun akademik durumu, gelisimi ve size ozel tavsiyeler</div>
    </div>""", unsafe_allow_html=True)

    if not children:
        st.warning("Sisteme kayitli cocugunuz bulunamadi. Lutfen okul yonetimiyle iletisime gecin.")
        _render_tab_chat(client, system_msg, mascot_avatar)
        return

    # Gunluk oneriler
    daily = _smart_daily_recommendations(data={}, role="Veli")
    _render_daily_recommendations(daily)

    tabs = st.tabs(["📊 Akademik Durum", "📈 Gelisim Raporu", "🤖 AI Tavsiyeler", "💬 Smarti"])

    for child in children:
        grades = ak.get_grades(student_id=child.id)
        att = ak.get_attendance(student_id=child.id)
        results = od.get_results(student_id=child.id)
        telafi = od.get_telafi_tasks(student_id=child.id)

        with tabs[0]:
            st.markdown(f"### {child.tam_ad} — {child.sinif}/{child.sube}")

            # KPI
            ort = sum(g.puan for g in grades) / len(grades) if grades else 0
            ozursuz = sum(1 for a in att if a.turu == "ozursuz")
            aktif_telafi = len([t for t in telafi if t.status in ("assigned", "in_progress")])

            vc1, vc2, vc3 = st.columns(3)
            with vc1:
                _verdict_card("Not Ortalamasi", f"{ort:.1f}", "puan", _TH_SCORE)
            with vc2:
                _verdict_card("Ozursuz Devamsizlik", str(ozursuz), "gun",
                              [(0, "🏆", "#22c55e", "Mukemmel: Devamsizlik yok"),
                               (3, "🟡", "#f59e0b", "Dikkat: Takip edin"),
                               (10, "🟠", "#f97316", "Uyari: Ciddi devamsizlik"),
                               (20, "🔴", "#ef4444", "Kritik: MEB limiti yaklasti")],
                              reverse=True)
            with vc3:
                _verdict_card("Telafi Gorevi", str(aktif_telafi), "aktif",
                              [(0, "🏆", "#22c55e", "Temiz: Telafi yok"),
                               (2, "🟡", "#f59e0b", "Az: Tamamlanmasi gerekiyor"),
                               (5, "🔴", "#ef4444", "Cok: Cocugunuz destek bekliyor")],
                              reverse=True)

            # Not detay + Ders Radar
            if grades:
                st.markdown("#### Ders Bazli Notlar")
                ders_map: dict[str, list] = {}
                for g in grades:
                    ders_map.setdefault(g.ders, []).append(g.puan)
                    color = "#22c55e" if g.puan >= 70 else ("#f59e0b" if g.puan >= 50 else "#ef4444")
                    st.markdown(f"- **{g.ders}**: <span style='color:{color};font-weight:700;font-size:1.1rem'>"
                                f"{g.puan}</span> ({g.not_turu})", unsafe_allow_html=True)

                # Ders performans radar
                if len(ders_map) >= 3:
                    st.markdown("#### Ders Performans Radari")
                    ders_ort = {d: round(sum(p)/len(p), 1) for d, p in ders_map.items()}
                    cats = list(ders_ort.keys())
                    vals = list(ders_ort.values())
                    fig_vr = go.Figure()
                    fig_vr.add_trace(go.Scatterpolar(
                        r=vals + [vals[0]], theta=cats + [cats[0]],
                        fill="toself", fillcolor="rgba(34,197,94,0.15)",
                        line=dict(color="#22c55e", width=2), marker=dict(size=6)))
                    fig_vr.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="#1e293b"),
                                   angularaxis=dict(tickfont=dict(size=10, color="#94a3b8"), gridcolor="#1e293b"),
                                   bgcolor="rgba(0,0,0,0)"),
                        showlegend=False, height=300,
                        margin=dict(l=60, r=60, t=20, b=20),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_vr, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

                # Not tablosu
                if ders_map:
                    import pandas as pd
                    df_veli = pd.DataFrame([{
                        "Ders": d, "Ortalama": round(sum(p)/len(p), 1),
                        "Not Sayisi": len(p), "Min": min(p), "Max": max(p),
                        "Durum": "Basarili" if sum(p)/len(p) >= 60 else "Gelismeli",
                    } for d, p in sorted(ders_map.items())])
                    st.dataframe(df_veli, use_container_width=True)

                # Ders donut — guclu vs zayif
                guclu = sum(1 for p in ders_map.values() if sum(p)/len(p) >= 70)
                zayif = len(ders_map) - guclu
                if guclu + zayif > 0:
                    _donut(["Basarili Ders", "Gelismeli Ders"], [guclu, zayif],
                           ["#22c55e", "#f59e0b"],
                           center=f"<b>{len(ders_map)}</b><br><span style='font-size:10px;color:#64748b'>Ders</span>")

        with tabs[1]:
            st.markdown(f"### {child.tam_ad} — Gelisim Raporu")

            # Erken uyari
            try:
                from models.erken_uyari import ErkenUyariStore
                eu_store = ErkenUyariStore()
                risks = eu_store.get_latest_risks()
                child_risk = next((r for r in risks if r.get("student_id") == child.id), None)
                if child_risk:
                    score = child_risk.get("risk_score", 0)
                    level = child_risk.get("risk_level", "LOW")
                    _verdict_card("Risk Durumu", f"%{score:.0f}", level,
                                  [(30, "🟢", "#22c55e", "Dusuk risk — endise edilecek durum yok"),
                                   (55, "🟡", "#f59e0b", "Orta risk — bazi alanlarda dikkat gerekli"),
                                   (75, "🟠", "#f97316", "Yuksek risk — okulla iletisime gecin"),
                                   (100, "🔴", "#ef4444", "Kritik — acil gorusme talep edin")])

                    # Risk faktorleri
                    recs = child_risk.get("recommendations", [])
                    if recs:
                        st.markdown("#### Sistem Onerileri")
                        for rec in recs:
                            st.markdown(f"- {rec}")
            except Exception:
                pass

            # CEFR
            try:
                from models.cefr_exam import CEFRPlacementStore
                cp = CEFRPlacementStore()
                cefr_results = cp.get_student_results(child.id)
                if cefr_results:
                    last = max(cefr_results, key=lambda r: r.submitted_at)
                    st.markdown(f"#### Ingilizce CEFR Seviyesi: **{last.placed_cefr}** (%{last.percentage})")
            except Exception:
                pass

        with tabs[2]:
            st.markdown(f"### {child.tam_ad} — AI Tavsiyeler & Haftalik Plan")

            # Haftalik plan
            weekly = _weekly_action_plan({}, "Veli")
            _render_weekly_plan(weekly)
            st.markdown("---")

            findings = []
            if ort < 60:
                findings.append("📉 Not ortalamasi dusuk — etut/ozel ders dusunun")
            if ort >= 85:
                findings.append("🏆 Basarili! Zenginlestirme programlarina (olimpiyat, proje) yonlendirin")
            if ozursuz > 5:
                findings.append("📋 Devamsizlik yuksek — nedenini arastirin, okul rehberligiyle gorusun")
            if aktif_telafi > 0:
                findings.append(f"🔄 {aktif_telafi} telafi gorevi var — tamamlanmasi icin destek verin")
            if not findings:
                findings.append("✅ Genel durum iyi. Duzenli takip etmeye devam edin.")

            st.markdown("#### Evde Yapilabilecekler")
            advice = [
                "Her gun en az 30 dk kitap okuma aliskanligi kazandirin",
                "Odevleri birlikte takip edin — SmartCampus Ogrenci Paneli'nden kontrol",
                "Dijital Kutuphane'deki kaynaklari kesfettirin",
                "AI Treni ile eglenceli ogrenme seansları duzenlein",
                "Matematik Koyu ve Bilisim Vadisi'ni haftalik rutine ekleyin",
                "Yabanci Dil modulunden gunluk 15 dk Ingilizce pratik",
            ]
            for f in findings:
                st.markdown(f"- {f}")
            st.markdown("---")
            for a in advice:
                st.markdown(f"- {a}")

            _mini_ai_insight(client,
                             f"Veli: Cocuk {child.tam_ad}, sinif {child.sinif}/{child.sube}, "
                             f"ort {ort:.1f}, {ozursuz} ozursuz devamsizlik, {aktif_telafi} telafi",
                             f"parent_{child.id}")

    with tabs[3]:
        _render_tab_chat(client, system_msg, mascot_avatar)


# ═══════════════════════════════════════════════════════════════════════════════
# OGRENCI DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def _render_student_dashboard(client, system_msg, mascot_avatar, auth_user):
    """Ogrenci: Kendi performansi + hedefler + motivasyon + yol haritasi."""
    inject_pro_css("ai_student")
    from models.akademik_takip import AkademikDataStore
    from models.olcme_degerlendirme import DataStore as ODS
    ak = AkademikDataStore()
    od = ODS()
    name = auth_user.get("name", "")

    # Ogrenciyi bul
    all_students = ak.get_students()
    student = None
    for s in all_students:
        if name.lower() in s.tam_ad.lower():
            student = s
            break

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#312e81,#4c1d95);border-radius:16px;
    padding:20px 24px;margin-bottom:16px;border:1.5px solid rgba(139,92,246,0.3);">
    <div style="font-size:1.3rem;font-weight:900;color:#c4b5fd;">Kisisel Gelisim Panelim</div>
    <div style="font-size:.85rem;color:#a78bfa;margin-top:4px;">
    Notlarin, devamsizligin, hedeflerin ve sana ozel yol haritasi</div>
    </div>""", unsafe_allow_html=True)

    if not student:
        st.warning("Ogrenci kaydiniz bulunamadi.")
        _render_tab_chat(client, system_msg, mascot_avatar)
        return

    # Günlük Duygu Check-in widget — öğrenci dashboard üstünde
    try:
        from views._mood_checkin import render_mood_quick_widget
        render_mood_quick_widget()
    except Exception:
        pass

    grades = ak.get_grades(student_id=student.id)
    att = ak.get_attendance(student_id=student.id)
    results = od.get_results(student_id=student.id)
    telafi = od.get_telafi_tasks(student_id=student.id)
    ort = sum(g.puan for g in grades) / len(grades) if grades else 0
    ozursuz = sum(1 for a in att if a.turu == "ozursuz")

    # Gunluk oneriler
    daily = _smart_daily_recommendations(data={}, role="Öğrenci")
    _render_daily_recommendations(daily)

    tabs = st.tabs(["📊 Durumum", "🎯 Hedeflerim", "🚀 Gelisim Yolu", "💬 Smarti"])

    with tabs[0]:
        st.markdown(f"### Merhaba {student.ad}! Iste durumun:")

        vc1, vc2, vc3 = st.columns(3)
        with vc1:
            _verdict_card("Not Ortalaman", f"{ort:.1f}", "puan",
                          [(90, "🏆", "#6366f1", "Harika! Sen bir yildizsin!"),
                           (75, "🟢", "#22c55e", "Cok iyi gidiyorsun!"),
                           (60, "🟡", "#f59e0b", "Fena degil ama daha iyisini yapabilirsin!"),
                           (40, "🟠", "#f97316", "Biraz daha gayret — yapabilirsin!"),
                           (0, "💪", "#ef4444", "Birlikte calisacagiz, hadi basla!")])
        with vc2:
            _verdict_card("Devamsizligin", str(len(att)), "gun",
                          [(0, "🏆", "#22c55e", "Tam devam — mukemmel!"),
                           (3, "🟡", "#f59e0b", "Az devamsizlik — dikkat et"),
                           (10, "🟠", "#f97316", "Dersleri kaciriyorsun!"),
                           (20, "🔴", "#ef4444", "Cok fazla — her ders onemli!")],
                          reverse=True)
        with vc3:
            sinav_cnt = len(results)
            _verdict_card("Sinav Sonucum", str(sinav_cnt), "sinav",
                          [(5, "🟢", "#22c55e", "Duzgun sinav takibi!"),
                           (2, "🟡", "#f59e0b", "Daha fazla pratik yap"),
                           (0, "🟠", "#f97316", "Henuz sinav sonucun yok")])

        # Not detay + radar
        if grades:
            st.markdown("#### Derslerim")
            ders_map_s: dict[str, list] = {}
            for g in grades:
                ders_map_s.setdefault(g.ders, []).append(g.puan)
                emoji = "🌟" if g.puan >= 85 else ("✅" if g.puan >= 70 else ("⚡" if g.puan >= 50 else "📚"))
                color = "#22c55e" if g.puan >= 70 else ("#f59e0b" if g.puan >= 50 else "#ef4444")
                st.markdown(f"{emoji} **{g.ders}**: <span style='color:{color};font-weight:800;"
                            f"font-size:1.2rem;'>{g.puan}</span>", unsafe_allow_html=True)

            # Ogrenci ders radar
            if len(ders_map_s) >= 3:
                st.markdown("#### Ders Performans Radarim")
                d_ort = {d: round(sum(p)/len(p), 1) for d, p in ders_map_s.items()}
                cats = list(d_ort.keys())
                vals = list(d_ort.values())
                fig_sr = go.Figure()
                fig_sr.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]], theta=cats + [cats[0]],
                    fill="toself", fillcolor="rgba(139,92,246,0.15)",
                    line=dict(color="#a78bfa", width=2), marker=dict(size=6)))
                fig_sr.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="#1e293b"),
                               angularaxis=dict(tickfont=dict(size=10, color="#c4b5fd"), gridcolor="#1e293b"),
                               bgcolor="rgba(0,0,0,0)"),
                    showlegend=False, height=300,
                    margin=dict(l=60, r=60, t=20, b=20),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_sr, use_container_width=True, config=SC_CHART_CFG, key=_next_chart_key("pc"))

            # Basari donut
            guclu = sum(1 for p in ders_map_s.values() if sum(p)/len(p) >= 70)
            zayif = len(ders_map_s) - guclu
            if guclu + zayif > 0:
                # Not tablosu
                if ders_map_s:
                    import pandas as pd
                    df_stu = pd.DataFrame([{
                        "Ders": d, "Ortalama": round(sum(p)/len(p), 1),
                        "Durum": "Guclu" if sum(p)/len(p) >= 70 else "Calismali",
                    } for d, p in sorted(ders_map_s.items())])
                    st.dataframe(df_stu, use_container_width=True)

                _donut(["Guclu Derslerim", "Calismam Gereken"], [guclu, zayif],
                       ["#8b5cf6", "#f59e0b"],
                       center=f"<b>{len(grades)}</b><br><span style='font-size:10px;color:#64748b'>Not</span>")

    with tabs[1]:
        st.markdown("### Hedeflerini Belirle!")

        # Haftalik plan
        weekly = _weekly_action_plan({}, "Ogrenci")
        _render_weekly_plan(weekly)
        st.markdown("---")

        # Otomatik hedefler
        hedefler = []
        if ort < 70:
            hedefler.append(("📈", "Not ortalamani 70'in uzerine cikar", f"Simdi: {ort:.1f} → Hedef: 70+"))
        elif ort < 85:
            hedefler.append(("🚀", "Not ortalamani 85'in uzerine cikar", f"Simdi: {ort:.1f} → Hedef: 85+"))
        else:
            hedefler.append(("🏆", "Ortalamani koru ve olimpiyatlara hazirlan", f"Simdi: {ort:.1f} — Harika!"))

        if ozursuz > 0:
            hedefler.append(("📋", "Devamsizligi sifira indir", f"Simdi: {ozursuz} gun → Hedef: 0"))
        else:
            hedefler.append(("✅", "Tam devami surdur", "Mukemmel — devam et!"))

        hedefler.append(("📚", "Her gun 30 dakika kitap oku", "Okuma Kutuphanesi'nden kitap sec"))
        hedefler.append(("🌍", "Ingilizce pratik yap", "Yabanci Dil > SRS Kelime Tekrar kullan"))
        hedefler.append(("🧮", "Matematik Koyu'nde haftada 3 alistirma", "Eglenirken ogren!"))
        hedefler.append(("💻", "Bilisim Vadisi'nde kodlama dene", "Gelecek teknolojide!"))

        for emoji, title, detail in hedefler:
            st.markdown(f"""<div style="background:#0f172a;border-radius:10px;padding:12px 16px;
            margin:4px 0;border-left:4px solid #8b5cf6;">
            <span style="font-size:1.2rem;margin-right:8px;">{emoji}</span>
            <span style="color:#e2e8f0;font-weight:700;">{title}</span>
            <div style="color:#94a3b8;font-size:.8rem;margin-top:2px;margin-left:32px;">{detail}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("### Gelisim Yol Haritan")

        steps = [
            ("1. Hafta", "Her dersten eksik konularini belirle", "Ogretmenlerinle konus, KYT sonuclarini incele"),
            ("2. Hafta", "Gunluk calisma rutini olustur", "Her gun 2 saat: 1s ders + 30dk okuma + 30dk pratik"),
            ("3. Hafta", "Zayif derslere odaklan", "AI Treni + Matematik Koyu'nden ekstra calis"),
            ("4. Hafta", "Ilk degerlendirme", "Odev + quiz sonuclarini kontrol et — ilerlemeyi gor!"),
            ("2. Ay", "Hedef kontrol", "Not ortalamanin yukseldigini gor — motivasyonunu artir!"),
            ("Donem Sonu", "Basari raporu", "CEFR sinavi + karne + portfolyo — hepsini topla!"),
        ]
        for period, title, detail in steps:
            st.markdown(f"""<div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #1e293b;">
            <div style="min-width:80px;padding:6px 10px;background:#312e81;border-radius:8px;
            text-align:center;font-size:.75rem;color:#c4b5fd;font-weight:700;">{period}</div>
            <div><div style="color:#e2e8f0;font-weight:700;font-size:.9rem;">{title}</div>
            <div style="color:#94a3b8;font-size:.78rem;">{detail}</div></div>
            </div>""", unsafe_allow_html=True)

        _mini_ai_insight(client,
                         f"Ogrenci {student.tam_ad}, sinif {student.sinif}, ort {ort:.1f}, "
                         f"{ozursuz} ozursuz devamsizlik — motivasyon ve gelisim tavsiyesi ver",
                         f"student_{student.id}")

    with tabs[3]:
        _render_tab_chat(client, system_msg, mascot_avatar)


def _render_brain_dashboard(client, system_msg, mascot_avatar):
    """Yonetici icin 6 tab'li merkez beyni dashboard."""
    inject_pro_css("ai_brain")
    st.session_state["_ai_chart_seq"] = 0  # Chart key counter sifirla
    data = _collect_all_module_data()

    # Executive Header
    inst_score = _compute_institution_score(data)
    overall = inst_score["overall"]
    s_color = "#22c55e" if overall >= 70 else ("#f59e0b" if overall >= 40 else "#ef4444")
    s_label = "Mukemmel" if overall >= 80 else ("Iyi" if overall >= 60 else ("Gelismeli" if overall >= 40 else "Kritik"))
    active_mods = sum(1 for vals in data.values()
                      if sum(_safe_len(v) for v in vals.values() if isinstance(v, list)) > 0)
    total_records = sum(sum(_safe_len(v) for v in vals.values() if isinstance(v, list))
                        for vals in data.values())

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#312e81 100%);
    border-radius:18px;padding:24px 28px;margin-bottom:20px;
    border:1.5px solid rgba(99,102,241,0.25);position:relative;overflow:hidden;">
    <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
    background:radial-gradient(circle,rgba(99,102,241,0.08),transparent);border-radius:50%;"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div>
    <div style="font-size:1.4rem;font-weight:900;color:#c7d2fe;letter-spacing:-0.5px;">
    SmartCampus AI — Merkez Beyni</div>
    <div style="font-size:.85rem;color:#818cf8;margin-top:4px;">
    {active_mods}/18 aktif modul | {total_records:,} toplam kayit | Gercek zamanli analiz</div>
    </div>
    <div style="text-align:center;">
    <div style="font-size:2.2rem;font-weight:900;color:{s_color};">%{overall:.0f}</div>
    <div style="font-size:.75rem;color:#64748b;font-weight:600;">{s_label}</div>
    </div>
    </div></div>""", unsafe_allow_html=True)

    # Veri yenileme butonu
    rc1, rc2 = st.columns([3, 1])
    with rc2:
        if st.button("🔄 Veriyi Yenile", key="ai_brain_refresh", use_container_width=True):
            # Tum cache'leri temizle
            for k in list(st.session_state.keys()):
                if k.startswith("_ai_"):
                    del st.session_state[k]
            st.rerun()
    with rc1:
        ts = st.session_state.get("_ai_brain_ts", 0)
        if ts:
            from datetime import datetime as _dt2
            st.markdown(f"<span style='color:#64748b;font-size:.8rem;'>Son guncelleme: "
                        f"{_dt2.fromtimestamp(ts).strftime('%H:%M:%S')}</span>",
                        unsafe_allow_html=True)

    tabs = st.tabs([
        "📊 Kurum Panoramasi",
        "🎓 Akademik Analiz",
        "👥 Insan Kaynaklari",
        "💰 Mali & Operasyonel",
        "🤖 AI Degerlendirme & Yol Haritasi",
        "💬 Smarti Asistan",
    ])

    with tabs[0]:
        _render_tab_panorama(data)
    with tabs[1]:
        _render_tab_akademik(data)
    with tabs[2]:
        _render_tab_ik(data)
    with tabs[3]:
        _render_tab_mali(data)
    with tabs[4]:
        _render_tab_ai_eval(client, data)
    with tabs[5]:
        _render_tab_chat(client, system_msg, mascot_avatar)


# ===================== SISTEM PROMPT =====================

SYSTEM_PROMPT = """Sen SmartCampus AI platformunun yapay zekâ asistanısın. Adın "Smarti".

Kendini tanıtırken "Ben Smarti!" de. Genç, enerjik, heyecanlı ve süper yardımsever bir kişiliğe sahipsin.
Sanki öğrencilerin en yakın arkadaşı, velilerin en güvendiği rehber gibisin.

Konuşma Tarzı (ÇOK ÖNEMLİ):
- Her zaman düzgün, akıcı ve doğru Türkçe kullan. İmla ve dil bilgisi kurallarına uy.
- Kısa, net ama sıcak cümle kur. Monoton olma, heyecanını hissettir!
- Genç ve samimi bir dil kullan ama saygılı ol. "Harika!", "Çok iyi gidiyorsun!", "Birlikte başaracağız!" gibi motive edici ifadeler kullan.
- Emoji kullanabilirsin ama abartma (cümle başına en fazla 1).
- Uzun paragraflar yerine kısa maddeler ve başlıklar kullan, okunabilirliği artır.
- Soru sorarak karşılıklı sohbet başlat: "Hangi ders hakkında konuşalım?", "Bugün nasıl hissediyorsun?"
- Başka dillere kaçma, her zaman Türkçe konuşmaya devam et.

CEVAP VERME KURALLARI (ÇOK ÖNEMLİ):
- Her zaman TAM ve KAPSAMLI cevap ver. Eksik veya yarım bilgi verme.
- Bir özellik veya modül sorulduğunda TÜM alt başlıkları, sekmeleri ve detayları eksiksiz listele.
- "Neler görebilirim?", "Ne yapabilirim?", "Bu modülde ne var?" gibi sorularda İLGİLİ TÜM özellikleri say, asla 3-4 maddeyle sınırlama.
- Madde madde, başlık başlık, düzenli ve eksiksiz yanıt ver.
- Kullanıcı bir modül veya panel hakkında sorduğunda aşağıdaki detaylı bilgileri kullan.

Görevlerin:
- Kullanıcılara SmartCampus AI platformu hakkında yardım etmek
- Eğitim, okul yönetimi ve akademik konularda destek vermek
- Platform modüllerini tanımak ve kullanıcıları yönlendirmek
- Her zaman Türkçe konuşmak
- Motivasyon vermek, cesaretlendirmek, pozitif enerji yaymak

==============================
PLATFORM MODÜLLERİ (DETAYLI - TÜM SEKMELER VE ALT SEKMELER)
==============================

1. KURUMSAL ORGANİZASYON VE İLETİŞİM (KOİ)
   Sekmeler: Dashboard | Kurum Profili | Organizasyon | Çalışanlar | İletişim | Şikayet/Öneri | Sertifikalar | Kullanıcı Yönetimi | Sosyal Medya | SWOT Analizi | Veli Memnuniyet Anketi | Smarti
   a) Dashboard: Kurum genel bakış, hızlı istatistikler, özet kartlar
   b) Kurum Profili: Kurum adı, slogan, vizyon, misyon, değerler, tarihçe, kurucu mesajı, yönetim kurulu, iletişim bilgileri (telefon/e-posta/adres/fax), logo, sosyal medya hesapları (Instagram, Facebook, YouTube, Twitter, LinkedIn, TikTok)
   c) Organizasyon Şeması: Pozisyon yönetimi, hiyerarşik yapı görselleştirme, 8 pozisyon kategorisi (Yönetim Kurulu, Üst Yönetim, Okul Yönetimi, Akademik Liderlik, İdari Birimler, Destek Hizmetleri, Öğretim Kadrosu, Diğer), Graphviz şema üretimi, PDF export
   d) Çalışan Yönetimi: Kadro listesi, yeni personel ekleme, departman atama, pozisyon takibi
   e) İletişim & Mesajlaşma: Alt sekmeler → Gelen Kutusu, Mesaj Gönder, SMS Transferleri, Giden Kutusu, Ayarlar, Panel Mesajları. Veli mesajlaşma, duyuru kategorileri, toplu mesaj, şablon bazlı mesajlar
   f) Şikayet / Öneri Takip: Alt sekmeler → Kayıt Listesi, Yeni Kayıt, İstatistikler ve SLA
      - Kayıt Listesi: Filtreler (tür/durum/kategori/öncelik/SLA), tablo görünümü, SLA badge, detay paneli, sonuç aşamaları (1-Geri Dönüş Yapıldı, 2-Çözüldü ve Bilgi Verildi / Çözüm İçin Harekete Geçildi, 3-Kalıcı Olarak Çözüldü / Çözülemedi+neden), yönlendirme yazışmaları (chat thread)
      - Yeni Kayıt: Tarih/saat, tür (şikayet/öneri/talep), kategori (10 adet: akademik, idari, temizlik, güvenlik, yemek, ulaşım, iletişim, tesis, teknoloji, diğer), öncelik (düşük/normal/yüksek/acil), kaynak (veli/öğrenci/çalışan/ziyaretçi/diğer), kanal (e-posta/telefon/SMS/yüz yüze/WhatsApp/sosyal medya/2.kişi vasıtasıyla/diğer), şikayeti alan kişi (IK aktif çalışanlar), yönlendirme
      - SLA Performans Kriterleri: Acil→2-4s dönüş/24s çözüm, Yüksek→24s dönüş/48s çözüm, Normal→24s dönüş/72s çözüm, Düşük→48s dönüş/120s çözüm
      - İstatistikler: SLA performans özeti, öncelik bazlı SLA durumu (stacked bar), SLA donut, tür/durum/kategori/kaynak/kanal dağılım grafikleri, günlük trend, sonuç aşamaları özeti, çözülemeyen kayıtlar ve nedenleri
   g) Sertifika Sistemi: 10+ sertifika türü (Başarı, Derece, Katılım, Spor, Sanat vb.), özelleştirilebilir tasarımlar, toplu üretim ve yazdırma, arşiv yönetimi
   h) Kullanıcı Yönetimi: Kullanıcı oluşturma/silme, şifre üretme/sıfırlama, rol atama (Yönetici/Öğretmen/Çalışan/Öğrenci/Veli), aktif/pasif yönetimi, toplu kullanıcı import, modül yetki yönetimi
   i) Sosyal Medya: Hesap yönetimi ve içerik paylaşımı
   j) SWOT Analizi: Güçlü yönler, zayıf yönler, fırsatlar, tehditler analizi
   k) Veli Memnuniyet Anketi: Anket oluşturma, dağıtım ve sonuç analizi

2. HALKLA İLİŞKİLER VE TANITIM
   Kategoriler: Kampanya | Aday Yönetimi | Kayıt İşlemleri | Rapor & Araçlar | Veli Erişim | Smarti
   a) Kampanya: Planlama, Yeni Kampanya, Aylık Kampanya. Kampanya oluşturma, takip, performans ölçümü
   b) Aday Yönetimi: Aday Girişi, Aday Arama (5 arama takibi), Günlük Takip, Görüşme Planlama. 18+ aday durumu, otomatik takip zamanlama, 30+ kayıt görüşmesi
   c) Kayıt İşlemleri: Fiyat Teklifi, Sözleşme, Kesin Kayıt. Fiyat teklifi hesaplama, sözleşme yönetimi, ödeme takibi
   d) Rapor & Araçlar: KPI Dashboard, Dönüşüm Hunisi, Testler (8 entegre test: Çoklu Zeka, Dil Yerleştirme, VARK Öğrenme Stili, HHT1, Ortaokul Check-up, Metropolitan Olgunluk, Ortaokul/Lise Sınav Testi), Kampanya Kütüphanesi, Eğitim Materyalleri
   e) Veli Erişim: Veli giriş portalı, başvuru takibi, aday takip formu, yetenek değerlendirmesi

3. AKADEMİK TAKİP
   Sekmeler: Kadro & Öğrenci | Nöbet Yönetimi | Zaman Çizelgesi | Ders & Program | Öğretim & Planlama | Ders Defteri | Dijital Öğrenme & Online Ders | Ödev Takip | Yoklama & Notlar | AT Raporlar | Erken Uyarı & Destek | Ölçme & Değerlendirme | Kazanım Takip (KYT) | Kurum Hizmetleri | Smarti
   a) Kadro & Öğrenci: Alt sekmeler → Akademik Kadro, Sınıf Listesi, Öğrenci Yönetimi, Öğretmen Detay. Öğrenci import, ekleme, düzenleme, toplu işlemler
   b) Nöbet Yönetimi: Nöbet çizelgesi, öğretmen nöbet takibi, raporlama, takvim görünümü
   c) Zaman Çizelgesi: Günlük program yönetimi (ders, teneffüs, öğle arası, etüt saatleri), zaman dilimi tanımlama
   d) Ders & Program: Alt sekmeler → Ders Programı (5 alt sekme: Otomatik Dağıtım, Öğretmen Atama, Sınıf Programı, Öğretmen Programı, Program Raporları)
   e) Öğretim & Planlama: Alt sekmeler → Akademik Planlama (yıllık/aylık/haftalık), Uygulama Takibi, müfredat ağacı görselleştirme
   f) Ders Defteri: Günlük ders kaydı, kurumsal karneler, ders işlenme takibi
   g) Dijital Öğrenme & Online Ders: 7 alt sekme → Platform Linkleri, Online Ders Yönetimi, Ders Durumu, Planlama, Raporlar, Giriş Analitiği, Ayarlar
   h) Ödev Takip: Ödev verme, takip, değerlendirme, online teslim sistemi (dosya/link/video/QR)
   i) Yoklama & Notlar: Yoklama & Devamsızlık (7 alt sekme: Günlük Yoklama, Ders Bazlı, Devamsızlık Özeti, Uyarılar, Toplu Giriş, İzin Takibi, Raporlar), Not Girişi (tekli/toplu), devamsızlık uyarıları (3 seviye)
   j) AT Raporlar: Karne, öğrenci sıralaması, devamsızlık raporu, ders analizi
   k) Erken Uyarı & Destek: Riskli öğrenci tespiti, müdahale kaydı, destek planı oluşturma, öğretmen önerileri
   l) Ölçme & Değerlendirme: Sınav ve değerlendirme entegrasyonu
   m) Kazanım Takip (KYT): 6 alt sekme → Kazanım İzleme, Soru Havuzu, Test Oluştur, Sonuçlar, Sınıf Analizi, Raporlar
   n) Kurum Hizmetleri: Randevu talepleri, belge talepleri yönetimi

4. REHBERLİK
   Sekmeler: Dashboard | Görüşme Kayıtları | Vaka Takip | Aile Görüşmeleri | Yönlendirme | BEP | Test ve Envanter | Rehberlik Planı | Risk Değerlendirme | RHB Raporlar | Smarti
   a) Dashboard: Genel bakış, aktif vaka sayısı, bekleyen görüşmeler, istatistik kartları
   b) Görüşme Kayıtları: Bireysel görüşme kaydı, görüşme türü, notlar, takip planı
   c) Vaka Takip: Vaka açma/kapama, vaka durumu (açık/takipte/kapalı), müdahale planları, süreç takibi
   d) Aile Görüşmeleri: Veli görüşme kayıtları, katılımcılar, kararlar, takip
   e) Yönlendirme: Öğrenci yönlendirme (RAM, hastane, uzman), yönlendirme takibi
   f) BEP: Bireyselleştirilmiş Eğitim Programı hazırlama, takip, güncelleme
   g) Test ve Envanter: Test uygulama, test oturumu oluşturma, sonuç analizi, çeşitli psikolojik testler
   h) Rehberlik Planı: Yıllık rehberlik planı, haftalık/aylık etkinlikler, uygulama takibi
   i) Risk Değerlendirme: Riskli öğrenci tespiti, risk seviyeleri, müdahale planları
   j) RHB Raporlar: Görüşme raporları, vaka istatistikleri, dönemsel analizler

5. İNSAN KAYNAKLARI YÖNETİMİ
   Sekmeler: Genel Bakış | Aday Havuzu | Mülakat | Onboarding | Kurum Aktif Çalışanları | Performans | İzin Yönetimi | Maaş & Bordro | Eğitim & Sertifika | Disiplin | Offboarding | IKY Raporlar | Ayarlar | Smarti
   a) Genel Bakış: Aktif personel sayısı, aday havuzu, planlanan mülakatlar, izin özeti, KPI kartları
   b) Aday Havuzu: Aday kaydı, aday durumu takibi, başvuru yönetimi, CV arşivi
   c) Mülakat: Mülakat planlama, mülakat formu, değerlendirme, sonuçlar
   d) Onboarding: İşe alım süreci, oryantasyon, belge toplama, görev atama
   e) Kurum Aktif Çalışanları: Personel listesi, pozisyon, departman, iletişim bilgileri, profil detayları
   f) Performans: Performans değerlendirme, hedef belirleme, dönemsel puanlama, 360° değerlendirme
   g) İzin Yönetimi: İzin talebi, onay süreci, izin bakiyesi, yıllık/mazeret/rapor izinleri
   h) Maaş & Bordro: Maaş hesaplama, bordro oluşturma, ek ödemeler, kesintiler
   i) Eğitim & Sertifika: Kurum içi eğitim planı, sertifika takibi, eğitim takvimi
   j) Disiplin: Disiplin kaydı, uyarı, tutanak, süreç takibi
   k) Offboarding: İşten ayrılma süreci, devir teslim, çıkış mülakatı
   l) IKY Raporlar: Personel istatistikleri, izin raporları, performans analizleri

6. OKUL SAĞLIĞI TAKİP
   Sekmeler: Dashboard | Sağlık Kartı | Revir Ziyareti | İlaç Uygulama | Kaza/Olay | Envanter | İlk Yardım Dolapları (dinamik sekmeler)
   a) Dashboard: Günlük revir ziyaretleri, ilaç uygulamaları, kaza/olay sayıları, kritik stok uyarıları
   b) Sağlık Kartı: Öğrenci sağlık bilgileri, alerji, kronik hastalık, kan grubu, aşı takibi
   c) Revir Ziyareti: Ziyaret kaydı, şikayet, teşhis, uygulanan işlem, yönlendirme
   d) İlaç Uygulama: İlaç kayıt, uygulama takibi, dozaj, veli izin formu
   e) Kaza/Olay: Olay kaydı, olay türü, müdahale, tutanak, bildirim
   f) Envanter: Tıbbi malzeme stok takibi, kritik seviye uyarıları, sipariş
   g) İlk Yardım Dolapları: Dolap lokasyonları, malzeme kontrolü, son kullanma tarihi takibi

7. TÜKETİM VE DEMİRBAŞ
   Sekmeler: Dashboard | Günlük Tüketim | Stok Durumu | Tüketim Raporları | Demirbaş Kayıt | Zimmet Yönetimi | Satın Alma | AI Tavsiye | Ayarlar | Smarti
   a) Dashboard: Stok durumu özeti, tüketim trendi, kritik stok uyarıları
   b) Günlük Tüketim: Günlük malzeme tüketim kaydı, tüketim onayı
   c) Stok Durumu: Anlık stok seviyeleri, minimum stok uyarıları, stok hareketleri
   d) Tüketim Raporları: Dönemsel tüketim analizi, maliyet raporları, trend grafikleri
   e) Demirbaş Kayıt: Demirbaş envanter kaydı, barkod/seri no, lokasyon, durum
   f) Zimmet Yönetimi: Personel zimmet atama, zimmet iade, zimmet geçmişi
   g) Satın Alma: Satın alma talebi, onay süreci, tedarikçi seçimi, hedef teslim tarihi
   h) AI Tavsiye: Yapay zeka destekli stok ve satın alma önerileri

8. RANDEVU VE ZİYARETÇİ
   Sekmeler: Dashboard | Randevu Yönetimi | Ziyaretçi Giriş/Çıkış | Ziyaretçi Rehberi | Randevularım | Görüşme Notları | RZ Raporlar | Ayarlar | Smarti
   a) Dashboard: Günlük randevu özeti, ziyaretçi sayısı, bekleyen randevular
   b) Randevu Yönetimi: Randevu oluşturma, onay/red, tarih/saat, görüşülecek kişi (IK aktif çalışanlar), görüşülecek unvan, format (yüz yüze/online)
   c) Ziyaretçi Giriş/Çıkış: Ziyaretçi kaydı, giriş/çıkış saati, ziyaret nedeni, kimlik bilgisi
   d) Ziyaretçi Rehberi: Ziyaretçi bilgilendirme, kurum haritası
   e) Randevularım: Kişisel randevu listesi
   f) Görüşme Notları: Görüşme kayıtları, notlar, takip planı
   g) RZ Raporlar: Randevu istatistikleri, ziyaretçi analizleri

9. DESTEK HİZMETLERİ TAKİP
   Sekmeler: Dashboard | Talepler | Periyodik İşler | Denetimler | Periyodik Bakım (PBK) | Firma Havuzu | Tedarikçiler | DH Raporlar | Ayarlar | Smarti
   a) Dashboard: Açık talep sayısı, tamamlanan, bekleyen periyodik işler, denetim takvimi
   b) Talepler: Destek talebi oluşturma (arıza/tadilat/temizlik/güvenlik vb.), öncelik, istenen tarih, atama, durum takibi
   c) Periyodik İşler: Tekrarlayan görev tanımlama, plan tarihi, otomatik hatırlatma, durum
   d) Denetimler: Denetim formu oluşturma, denetim tarihi, puanlama, aksiyon planı
   e) Periyodik Bakım (PBK): Ekipman bakım takvimi, bakım kaydı, sonraki bakım tarihi
   f) Firma Havuzu: Dış hizmet firma kayıtları, iletişim, uzmanlık alanı
   g) Tedarikçiler: Tedarikçi yönetimi, sözleşme takibi
   h) DH Raporlar: Talep istatistikleri, çözüm süreleri, performans analizi

10. SİVİL SAVUNMA VE İŞ GÜVENLİĞİ
    Sekmeler: Dashboard | A) Sivil Savunma | B) İSG | C) Okul/Öğrenci Güvenliği | Olay Kayıtları | SSG Raporlar | Ayarlar | Smarti
    a) Dashboard: Tatbikat takvimi, açık riskler, olay sayıları, checklist durumu
    b) Sivil Savunma: Tatbikat planlama ve kaydı, tahliye planları, acil durum prosedürleri
    c) İSG (İş Sağlığı ve Güvenliği): Risk değerlendirme, İSG eğitimleri, koruyucu ekipman takibi
    d) Okul/Öğrenci Güvenliği: Güvenlik protokolleri, kamera sistemleri, giriş/çıkış kontrolü
    e) Olay Kayıtları: Güvenlik olayı kaydı, olay türü, müdahale, sonuç
    f) SSG Raporlar: Tatbikat raporları, risk analizleri, olay istatistikleri

11. TOPLANTI VE KURULLAR
    Sekmeler: Dashboard | Toplantı Yönetimi | Toplantı Yürütme | TK Raporlar | Şablonlar | Ayarlar | Smarti
    a) Dashboard: Planlanan/tamamlanan toplantılar, bekleyen aksiyonlar, katılım oranları
    b) Toplantı Yönetimi: Toplantı oluşturma, tür (kurul/komisyon/veli/personel), tarih, katılımcılar, gündem, konum, tekrar, hatırlatma
    c) Toplantı Yürütme: Yoklama, gündem takibi, karar kaydı, aksiyon atama, tutanak
    d) TK Raporlar: Toplantı istatistikleri, aksiyon takibi, katılım analizleri
    e) Şablonlar: Toplantı gündem şablonları, tutanak şablonları

12. SOSYAL ETKİNLİK VE KULÜPLER
    Sekmeler: Dashboard | Kulüpler | Sosyal Etkinlikler | SE Raporlar | Smarti
    a) Dashboard: Aktif kulüp sayısı, planlanan etkinlikler, katılım oranları
    b) Kulüpler: Kulüp oluşturma, danışman atama, üye yönetimi, faaliyet planlama, kulüp faaliyetleri
    c) Sosyal Etkinlikler: Etkinlik oluşturma (gezi/tören/yarışma/konser vb.), tarih, konum, bütçe, katılımcı listesi, durum takibi
    d) SE Raporlar: Etkinlik istatistikleri, kulüp performansları, katılım analizleri

13. BÜTÇE GELİR GİDER
    Sekmeler: Dashboard | Bütçe Planlama | Gelir Kayıt | Gider Kayıt | Tahmini vs Gerçekleşen | Aylık Takip | Raporlar | Ayarlar | Smarti
    a) Dashboard: Toplam gelir/gider, net bakiye, bütçe gerçekleşme oranı, trend grafikleri
    b) Bütçe Planlama: Yıllık/dönemsel bütçe oluşturma, kalem bazlı planlama
    c) Gelir Kayıt: Gelir türleri (öğrenim ücreti, bağış, etkinlik, diğer), tarih, tutar, açıklama
    d) Gider Kayıt: Gider türleri (personel, kira, malzeme, bakım vb.), tarih, tutar, fatura
    e) Tahmini vs Gerçekleşen: Bütçe-gerçekleşen karşılaştırma, sapma analizi, grafikler
    f) Aylık Takip: Ay bazlı gelir/gider takibi, nakit akış tablosu
    g) Raporlar: Finansal raporlar, gelir/gider analizleri, trend grafikleri

14. KÜTÜPHANE
    Sekmeler: Dashboard | Kayıtlı Materyaller | Yeni Materyal Kaydı | Ödünç İşlemleri | Ödünç Takip | Analiz | Raporlar | Ayarlar | Smarti
    a) Dashboard: Toplam materyal, aktif ödünç, geciken iade, en çok okunan
    b) Kayıtlı Materyaller: Kitap/dergi/DVD/dijital kayıtları, arama, filtreleme, barkod
    c) Yeni Materyal Kaydı: Materyal ekleme (ISBN, yazar, yayınevi, kategori, raf)
    d) Ödünç İşlemleri: Ödünç verme, iade alma, süre uzatma
    e) Ödünç Takip: Aktif ödünçler, geciken iadeler, hatırlatma gönderimi
    f) Analiz: Okuma istatistikleri, popüler kitaplar, öğrenci bazlı analiz
    g) Raporlar: Kütüphane kullanım raporları, envanter raporu

15. MEZUNLAR VE KARİYER YÖNETİMİ
    Sekmeler: Dashboard | Mezun Havuzu | İletişim & Duyuru | MK Raporlar | Mezun Portalı | Anketler | Etkinlikler | Staj & İş | Mentor | Tavsiye Kayıt | Bağış & Sponsorluk | Ayarlar | Smarti
    a) Dashboard: Mezun sayısı, etkinlikler, mentorluk, bağış özeti
    b) Mezun Havuzu: Mezun dizini, arama/filtreleme, toplu etiketleme, profil yönetimi, KVKK uyumu
    c) İletişim & Duyuru: Mezun mesajlaşma, duyurular, toplu bildirim
    d) MK Raporlar: Mezun istatistikleri ve analiz
    e) Mezun Portalı: Kişisel mezun profil erişimi
    f) Anketler: Anket oluşturma ve dağıtım
    g) Etkinlikler: Mezun etkinlik yönetimi (buluşma, seminer, kariyer günü)
    h) Staj & İş: İş ve staj fırsatları yönetimi
    i) Mentor: Mentorluk programı yönetimi, mentor-mentee eşleştirme
    j) Tavsiye Kayıt: Mezun tavsiye ve referans kaydı
    k) Bağış & Sponsorluk: Bağış ve sponsorluk takibi, bağışçı yönetimi

16. ÖLÇME VE DEĞERLENDİRME
    a) Soru Hazırla: Kazanım yönetimi (CRUD, MEB yıllık plandan import), AI soru üretimi (20 kademe blueprint), soru bankası (kalite puanlama, benzerlik kontrolü, inceleme kuyruğu: taslak→inceleme→onaylı), PDF soru import (AI destekli)
    b) Sınav Oluştur: Hızlı sınav, hazır sınav, şablon/blueprint sistemi, yeterlilik sınavı, sınav arşivi, 18+ sınav türü (TYT, AYT, LGS, okul sınavları, projeler vb.)
    c) Online Sınav: Öğrenci sınav girişi, sınav yönetimi/kontrol, oturum takibi, gerçek zamanlı izleme, süre yönetimi
    d) Değerlendirme: Optik form oluşturma, manuel cevap girişi, AI ile optik okuma, toplu değerlendirme, otomatik puanlama (net: doğru - yanlış/4), kazanım bazlı performans analizi
    e) Telafi Sistemi: RED bant (0-49%): Özet + anlık quiz + 48 saat quiz, YELLOW bant (50-69%): 5 soruluk pekiştirme, GREEN bant (70-84%): Haftalık 8 soruluk tekrar, BLUE bant (85-100%): 5 zor soru + 10 hız çalışması
    f) Sonuçlar & Raporlar: Öğrenci sıralaması, zorluk analizi, kazanım performans raporları, istatistiksel analiz, PDF export (şifreli), kurumsal raporlar, sınıf ve ders analitiği
    g) Stok Kontrol: Otomatik soru stoğu kontrolü ve doldurma
    h) MEB Entegrasyonu: 6.839+ MEB yıllık plan kazanımı (14 ders, 1-12. sınıf)

17. YÖNETİM TEK EKRAN
    Sekmeler: Dashboard | Gün Başı Raporu | Gün Sonu Raporu | Performans | Modül Özetleri | E-posta Ayarları | Raporlar | Ayarlar | Smarti
    a) Dashboard: Bugünün KPI'ları (planlanan/tamamlanan/iptal/ertelenen/gelmeyen), tamamlanma oranı donut chart, modül bazlı pasta grafik, haftalık trend, kritik/geciken uyarılar
    b) Gün Başı Raporu: Tarih seçici, tüm modüllerden o güne ait aktiviteleri toplama (GünlükToplayıcı), saate göre timeline görünümü, modül renkleriyle kartlar, filtreler
    c) Gün Sonu Raporu: Alt sekmeler → Görev Güncelleme, Rapor Oluştur, PDF & E-posta. Durum güncelleme (Planlı→Tamamlandı/İptal/Ertelendi/Gelmedi), gerçekleşme pasta chart, AI önerileri (OpenAI değerlendirme)
    d) Performans: Dönem seçici (Son 7/30/90 Gün + Tarih Aralığı), gerçekleşme oranı trend, modül performans sıralaması (grouped bar)
    e) Modül Özetleri: 16 modülün güncel KPI'ları, her modülde pasta grafiği, veri durumu özeti
    f) E-posta Ayarları: Alıcı CRUD, test e-posta, zamanlama ayarları
    g) Raporlar: Alt sekmeler → Modül Raporları (16 modülden raporlar), Geçmiş Günlük Raporlar. Tarih aralığı filtresi, trend grafikleri, PDF export
    h) Ayarlar: Rapor saati, plan saati, AI değerlendirme toggle, modül dahil etme toggle'ları

18. AI DESTEK
    Sesli ve yazılı AI asistan (Smarti). Sesli konuşma (OpenAI TTS + Whisper STT), platform bilgisi, akademik destek, kişiselleştirilmiş rehberlik. Rol bazlı veri erişimi (Veli→kendi çocuğu, Öğrenci→kendi bilgileri, Öğretmen→sınıf bilgileri, Yönetici→tüm veriler)

==============================
ANA SAYFA
==============================
Kart bazlı modül paneli. 16 modül kartı, 4 sütunlu grid görünümü. Her kart: modül ikonu + başlık + alt menü linkleri. Arama fonksiyonu (modül ve menü bazlı filtreleme). Yetki bazlı modül gösterimi. Kart tıklamasıyla ilgili modüle yönlendirme

==============================
VELİ PANELİ (16 SEKME - DETAYLI)
==============================
Veliler panellerinde şu 16 sekmeyi görebilir ve kullanabilir:

1. Günlük Rapor: Bugünün özet istatistikleri (yoklama, ödev, işlenen kazanım, KYT cevaplanan soru), genel akademik performans radar grafiği (notlar, sınav ortalaması, KYT başarısı, ödev teslim, devamsızlık puanı), bugünkü yoklama, bugün teslim edilecek ödevler, bugün işlenen kazanımlar, bugünkü KYT sonuçları, AI destekli analiz ve öğretmen önerileri
2. Notlar: Ders bazlı not tablosu (tüm sınavlar, yazılılar, sözlüler, performans notları)
3. Devamsızlık: Tarih bazlı devamsızlık kayıtları, özürlü/özürsüz ayrımı, devamsızlık istatistikleri ve grafikleri
4. Ödevler: Aktif ödevler listesi, teslim durumu takibi, teslim tarihleri, ders bilgisi, dosya/link/video/QR ekleri
5. Sınav Sonuçları: Sınav puanları, doğru/yanlış/boş sayıları, net puanları, performans grafikleri, sınav geçmişi ve trend analizi
6. KYT Performans: KYT başarı yüzdesi, doğru/yanlış soru istatistikleri, ders bazlı KYT performans analizi, grafikler
7. Telafi Görevleri: Renk bantlı telafi görevleri (RED/YELLOW/GREEN/BLUE), görev durumu ve ilerleme takibi, her bant için özel görev türleri
8. Akademik Yönlendirme: Risk uyarıları (devamsızlık, not düşüşü, ödev eksikliği, sınav trendi), destek planları, öğretmen gözlemleri, müdahale kayıtları
9. Mesajlar: Gelen kutusu (okunmuş/okunmamış), gönderilen mesajlar, yeni mesaj yazma (öğretmen/yönetim/rehberlik servisi), mesaj kategorileri (akademik, davranış, sağlık vb.), yanıt özelliği
10. Ders Programı: Haftalık ders programı (gün ve saat bazlı), ders ve öğretmen bilgileri, öğretmen branş/uzmanlık bilgisi
11. Etkinlik & Duyurular: Okul duyuruları (tarih, saat, yer), aylık etkinlik takvimi, duyuru türleri (haber, etkinlik, toplantı, tatil), sınıf seviyesine göre filtreleme
12. Yemek Menüsü: Aylık yemek menüsü takvimi, ay/yıl seçici, günlük yemek detayları
13. Servis Takibi: Servis kaydı bilgileri, güzergah bilgisi, biniş/iniş noktaları, servis saatleri
14. Randevu Sistemi: Aktif randevular, yeni randevu talebi (öğretmen/yönetim/rehberlik seçimi, tarih/saat, konu, format: yüz yüze veya online Zoom), geçmiş randevular
15. Belge Talep: 10 belge türü (öğrenci belgesi, transkript, devamsızlık belgesi, nakil belgesi, burs belgesi, kayıt belgesi, askerlik tecil, disiplin durumu, mezuniyet belgesi, diğer), kopya sayısı, acil talep seçeneği
16. Smarti AI: Sesli ve yazılı AI asistan, sesli konuşma (ses tanıma + sesli yanıt), akademik performans soruları, ödev ve sınav desteği, kişiselleştirilmiş rehberlik

Ek Özellikler: Özet dashboard kartları (not ortalaması, devamsızlık, son sınav, bekleyen ödev, KYT başarısı, okunmamış mesajlar), çoklu çocuk seçimi

==============================
ÖĞRENCİ PANELİ
==============================
Öğrenciler kendi panellerinde şunları görebilir:
- Kendi notları (ders bazlı detaylı tablo)
- Devamsızlık geçmişi ve istatistikleri
- Ödev listesi ve online teslim
- Sınav sonuçları (puan, net, doğru/yanlış)
- Ders programı
- Duyurular ve etkinlikler
- KYT soru çözme (kazanım bazlı interaktif test)
- Telafi görevleri
- Günlük rapor
- Akademik yönlendirme
- Mesajlar
- Yemek menüsü
- Servis takibi
- Randevu sistemi
- Belge talep
- Smarti AI asistan (sesli ve yazılı)

==============================
PLATFORM TEKNOLOJİLERİ
==============================
- AI destekli soru üretimi (GPT-4o-mini, 20 kademe blueprint)
- PDF sınav oluşturma ve çıkarma (PyMuPDF, ReportLab)
- MEB yıllık plan entegrasyonu (6.839 kazanım, 14 ders, 1-12. sınıf)
- Çoklu SMS sağlayıcı desteği (NetGSM, İletiMerkezi, Mutlucell, Twilio)
- WhatsApp ve E-posta bildirim sistemi
- Sertifika tasarlama ve toplu üretim
- Optik form oluşturma ve AI ile okuma
- Sesli AI asistan (OpenAI TTS + Whisper STT)
- Rol bazlı erişim kontrolü (Yönetici, Öğretmen, Çalışan, Öğrenci, Veli)

Kurum Bilgileri:
- Kurum: {kurum_adi}
- Kullanıcı: {kullanici_adi} ({kullanici_rol})

Hitap Kuralları:
- Kullanıcıya her zaman "{kullanici_adi}" diye hitap et
- Bu isimde zaten Hanım/Bey varsa aynen kullan
- Öğrencilere sadece isimleriyle hitap et, Hanım/Bey deme

İçerik Kuralları (KESİNLİKLE UYULMASI GEREKEN):
- SADECE SmartCampus AI platformu, eğitim ve akademik konularda bilgi ver
- Konu dışı sorularda kibarca "Bu konuda yardımcı olamıyorum, ancak platform ve eğitimle ilgili sorularınıza yardımcı olabilirim" de
- ASLA küfür, argo, hakaret veya kaba ifadeler kullanma
- ASLA cinsel içerik, müstehcen içerik veya uygunsuz konularda bilgi verme
- ASLA olumsuz, yıkıcı, zarar verici veya tehlikeli bilgi paylaşma
- ASLA siyasi, dini veya ayrımcı içerik üretme
- Kullanıcı uygunsuz içerik isterse kibarca reddet ve konuyu eğitim/platforma yönlendir
- Her zaman pozitif, yapıcı ve eğitici ol
- Bir eğitim platformu asistanı olarak sadece faydalı ve güvenli içerik sun

Veri Erişim Kuralları:
- Aşağıda sana sunulan VERİ PANELİ bilgilerini kullanarak kullanıcının sorularına rakamsal ve detaylı cevap ver
- Veli sadece kendi çocuğunun bilgilerine erişebilir: notlar, devamsızlık, sınav sonuçları, telafi görevleri
- Öğrenci sadece kendi bilgilerine erişebilir: notları, devamsızlığı, sınav sonuçları
- Öğretmen: sınıf mevcutları, öğrenci listesi, sınav sonuçları
- Yönetici: tüm veriler - öğrenci/öğretmen sayıları, sınıf mevcutları, devamsızlık özeti, sınav istatistikleri, soru bankası
- Bilgi istendiğinde VERİ PANELİ'ndeki rakamları direkt kullan, net ve sayısal cevap ver
- Rapor formatında sun: başlıklar, maddeler, sayılar
- Veri yoksa kibarca "Bu konuda henüz kayıt bulunmuyor" de

{veri_paneli}
"""


# ===================== TTS =====================

def _text_to_speech(client, text: str) -> bytes | None:
    """OpenAI TTS ile metni sese cevir."""
    try:
        if len(text) > 4000:
            text = text[:4000] + "..."
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
            speed=1.05,
        )
        return response.content
    except Exception as e:
        st.warning(f"Ses oluşturulamadı: {e}")
        return None


# ===================== STT (Whisper) =====================

def _speech_to_text(client, audio_bytes: bytes) -> str | None:
    """OpenAI Whisper ile sesi metne cevir."""
    try:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "recording.wav"
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="tr",
        )
        return transcript.text.strip() if transcript.text else None
    except Exception as e:
        st.warning(f"Ses tanıma hatası: {e}")
        return None


def _audio_hash(audio_bytes: bytes) -> str:
    """Ses verisinin hash'ini hesapla (tekrar islemeyi onlemek icin)."""
    return hashlib.md5(audio_bytes).hexdigest()


# ===================== KONUSMA SINIRI =====================

MAX_CONTEXT_MESSAGES = 20


def _trim_context(messages: list[dict]) -> list[dict]:
    """Sistem prompt + son MAX_CONTEXT_MESSAGES mesaji dondurur."""
    if len(messages) <= 1:
        return messages
    system = messages[:1]
    history = messages[1:]
    if len(history) > MAX_CONTEXT_MESSAGES:
        history = history[-MAX_CONTEXT_MESSAGES:]
    return system + history


# ===================== CHAT =====================

def _get_ai_response(client, messages: list[dict]) -> str:
    """OpenAI chat completion ile yanit al."""
    try:
        trimmed = _trim_context(messages)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=trimmed,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Hata oluştu: {e}"


def _process_user_input(client, user_input: str, system_msg: dict,
                        mascot_avatar: Any) -> None:
    """Kullanici girdisini isle: gecmise ekle, AI yaniti al, TTS olustur."""
    # Kullanici mesajini ekle
    st.session_state.ai_chat_history.append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # AI yaniti al
    messages = [system_msg] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.ai_chat_history
    ]

    with st.chat_message("assistant", avatar=mascot_avatar):
        with st.spinner("Düşünüyor..."):
            response_text = _get_ai_response(client, messages)

        st.markdown(response_text)

        # Sesli yanit (TTS) - sesli konusma modunda her zaman aktif
        if response_text:
            with st.spinner("Ses oluşturuluyor..."):
                audio = _text_to_speech(client, response_text)
                if audio:
                    msg_idx = len(st.session_state.ai_chat_history)
                    st.session_state.ai_audio_cache[f"audio_{msg_idx}"] = audio
                    st.audio(audio, format="audio/mp3", autoplay=True)

    # Yaniti gecmise ekle
    st.session_state.ai_chat_history.append({
        "role": "assistant",
        "content": response_text,
    })


# ===================== CSS =====================

def _inject_chat_css():
    st.markdown("""<style>
    .ai-header {
        background: linear-gradient(135deg, #94A3B8 0%, #7c3aed 100%);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.3);
        position: relative;
        overflow: hidden;
    }
    .ai-header::before {
        content: '';
        position: absolute;
        top: -30px;
        right: -30px;
        width: 120px;
        height: 120px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .ai-header h2 {
        color: white;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 800;
    }
    .ai-header p {
        color: rgba(255,255,255,0.7);
        margin: 4px 0 0 0;
        font-size: 0.85rem;
    }
    .voice-active-banner {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 16px;
        text-align: center;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        animation: pulse-glow 2s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 10px rgba(124, 58, 237, 0.3); }
        50% { box-shadow: 0 0 25px rgba(124, 58, 237, 0.6); }
    }
    .voice-active-banner .subtitle {
        font-weight: 400;
        font-size: 0.8rem;
        opacity: 0.85;
        margin-top: 4px;
    }
    </style>""", unsafe_allow_html=True)


# ===================== ANA RENDER =====================

def render_ai_destek() -> None:
    """AI Destek modulu ana fonksiyonu."""
    _inject_css()
    try:
        from utils.ui_common import ultra_premium_baslat
        ultra_premium_baslat("default")
    except Exception:
        pass
    styled_header(
        title="Smarti AI Asistan",
        subtitle="Yapay zeka destekli sesli ve yazili akilli asistan",
        icon="\U0001f916",
    )
    _inject_chat_css()

    # Mascot avatar
    mascot_avatar = _MASCOT_PATH if os.path.exists(_MASCOT_PATH) else "🤖"

    # --- Kullanici bilgileri (header için erken yukle) ---
    auth_user = st.session_state.get("auth_user", {})
    kullanici_adi = auth_user.get("name", "Kullanıcı")
    kullanici_cinsiyet = auth_user.get("cinsiyet", "").strip().lower()
    kullanici_rol = auth_user.get("role", "Misafir")

    ilk_isim = kullanici_adi.split()[0] if kullanici_adi.split() else kullanici_adi
    if kullanici_rol == "Öğrenci":
        hitap = ilk_isim
    elif kullanici_cinsiyet in ("erkek", "e", "bay"):
        hitap = f"{ilk_isim} Bey"
    elif kullanici_cinsiyet in ("kadin", "k", "bayan", "kadın"):
        hitap = f"{ilk_isim} Hanım"
    else:
        hitap = kullanici_adi

    from datetime import datetime as _dt
    _saat = _dt.now().hour
    if _saat < 6:
        _zaman_sel = "İyi geceler"
        _zaman_emoji = "🌙"
    elif _saat < 12:
        _zaman_sel = "Günaydın"
        _zaman_emoji = "☀️"
    elif _saat < 17:
        _zaman_sel = "İyi günler"
        _zaman_emoji = "🌤️"
    elif _saat < 21:
        _zaman_sel = "İyi akşamlar"
        _zaman_emoji = "🌆"
    else:
        _zaman_sel = "İyi geceler"
        _zaman_emoji = "🌙"

    # Header with mascot + kişisel selamlama
    hdr_cols = st.columns([1, 4])
    with hdr_cols[0]:
        if os.path.exists(_MASCOT_PATH):
            st.image(_MASCOT_PATH, width=160)
    with hdr_cols[1]:
        st.markdown(f"""
        <div class="ai-header">
            <h2>{_zaman_emoji} {_zaman_sel}, {hitap}!</h2>
            <p>Ben <strong>Smarti</strong>, senin dijital eğitim arkadaşın! Sana nasıl yardımcı olabilirim?</p>
        </div>
        """, unsafe_allow_html=True)

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("ai_destek_egitim_yili")

    # Client kontrol
    client = _get_client()
    if not client:
        st.error("OpenAI API anahtarı bulunamadı. Lütfen .env dosyasında OPENAI_API_KEY tanımlayın.")
        return

    # Kurum bilgileri
    from views.kim_organizational import load_profile
    profile = load_profile()
    kurum_adi = profile.get("name", "SmartCampus AI")

    # Kullanici rolune gore veri baglami olustur
    veri_paneli = _build_data_context(auth_user)

    system_msg = {
        "role": "system",
        "content": SYSTEM_PROMPT.format(
            kurum_adi=kurum_adi,
            kullanici_adi=hitap,
            kullanici_rol=kullanici_rol,
            veri_paneli=veri_paneli,
        ),
    }

    # ═══════════════════════════════════════════════════════════════
    # ROL BAZLI GORUNUM
    # ═══════════════════════════════════════════════════════════════
    if kullanici_rol in ("Yonetici", "SuperAdmin"):
        _render_brain_dashboard(client, system_msg, mascot_avatar)
    elif kullanici_rol == "Öğretmen":
        _render_teacher_dashboard(client, system_msg, mascot_avatar, auth_user)
    elif kullanici_rol == "Veli":
        _render_parent_dashboard(client, system_msg, mascot_avatar, auth_user)
    elif kullanici_rol in ("Öğrenci", "Ogrenci"):
        _render_student_dashboard(client, system_msg, mascot_avatar, auth_user)
    else:
        _render_tab_chat(client, system_msg, mascot_avatar)
