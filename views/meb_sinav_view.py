# -*- coding: utf-8 -*-
"""
MEB/ÖSYM Tarzı Soru & Sınav Üretim UI — v2 (3 adım, hızlı)
=============================================================
3 adımlı wizard: Ayarlar → Üretim → Sonuçlar
"""

import streamlit as st
import os
import json
import io
import re
import uuid
from datetime import datetime

from models.olcme_degerlendirme import DataStore, get_store, Question
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("olcme_degerlendirme")
except Exception:
    pass
from models.meb_sinav_motoru import (
    MebSinavMotoru, select_engine, get_blueprint_profile,
    get_grade_band, get_choice_count, get_choice_letters,
    build_blueprint, validate_hard,
    ENGINE_TYPE_MAP, ENGINE_LABELS, BLUEPRINT_PROFILES,
    SORU_TIPI_SABLONLARI, BECERI_ETIKETLERI,
)

# ============================================================
# STİL
# ============================================================



def _styled_badge(text, color="#2563eb"):
    return f"<span style='background:{color}15;color:{color};padding:4px 12px;border-radius:20px;font-size:0.75rem;font-weight:600'>{text}</span>"


def _grade_label(g):
    if g is None: return "Tümü"
    if isinstance(g, str): return g
    return f"{g}. Sınıf"


def _grade_sort_key(g):
    if isinstance(g, int): return g
    if g == "Hazırlık": return 8.5
    return 99


def _render_veri_tablosu_html(vt: dict) -> str:
    if not vt or not isinstance(vt, dict): return ""
    sutunlar = vt.get("sutunlar", [])
    satirlar = vt.get("satirlar", [])
    baslik = vt.get("baslik", "")
    if not sutunlar or not satirlar: return ""
    html = '<div style="margin:8px 0 12px 0;overflow-x:auto">'
    if baslik:
        html += f'<div style="font-size:0.85rem;font-weight:600;color:#94A3B8;margin-bottom:4px;text-align:center">{baslik}</div>'
    html += '<table style="border-collapse:collapse;width:100%;font-size:0.85rem;border:1px solid #d1d5db;border-radius:6px;overflow:hidden"><thead><tr>'
    for c in sutunlar:
        html += f'<th style="background:#f0f4ff;color:#1e3a5f;padding:8px 12px;border:1px solid #d1d5db;font-weight:700;text-align:center">{c}</th>'
    html += '</tr></thead><tbody>'
    for ri, row in enumerate(satirlar):
        bg = "#ffffff" if ri % 2 == 0 else "#0F1420"
        html += f'<tr style="background:{bg}">'
        cells = row if isinstance(row, list) else [row]
        for val in cells:
            html += f'<td style="padding:6px 12px;border:1px solid #e5e7eb;text-align:center">{val}</td>'
        for _ in range(len(sutunlar) - len(cells)):
            html += '<td style="padding:6px 12px;border:1px solid #e5e7eb;text-align:center">-</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    return html


# ============================================================
# SABİTLER & STATE
# ============================================================

SUBJECTS = [
    "Matematik", "Turkce", "Fen Bilimleri", "Sosyal Bilgiler", "Ingilizce", "Din Kulturu",
    "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya", "Felsefe", "Edebiyat",
    "Geometri", "Almanca", "Fransizca"
]
GRADES = [1, 2, 3, 4, 5, 6, 7, 8, "Hazırlık", 9, 10, 11, 12]

_MEB_DEFAULTS = {
    "meb_step": 1,
    "meb_grade": None,
    "meb_subject": None,
    "meb_engine": None,
    "meb_kazanimlar": [],
    "meb_count": 10,
    "meb_zorluk_dist": None,
    "meb_tur_dist": None,
    "meb_results": None,
    "meb_generating": False,
    "meb_selected_questions": [],
    "meb_exam_saved": False,
    "meb_model": "gpt-4o-mini",
    "meb_input_mode": "kazanim",
    "meb_pdf_context": "",
    "meb_pdf_filename": "",
    "meb_pdf_images": [],
    "meb_cozumlu": False,
}


def _init_state():
    for key, val in _MEB_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val


def _reset_state():
    keys_to_delete = [k for k in st.session_state if k.startswith("meb_")]
    for k in keys_to_delete:
        del st.session_state[k]
    for key, val in _MEB_DEFAULTS.items():
        st.session_state[key] = val


# ============================================================
# PLAN HİYERARŞİ CACHE (hızlı UI için)
# ============================================================

def _get_plan_hierarchy(store):
    """Yıllık planları {grade: {subject: {unite: [kazanimlar]}}} hiyerarşisine çevir.
    Session state'te cache'le — her rerun'da yeniden hesaplamaz."""
    key = "_meb_plan_cache"
    if key in st.session_state:
        return st.session_state[key]

    all_plans = store.get_annual_plans()
    hierarchy = {}
    siniflar = set()
    for p in all_plans:
        siniflar.add(p.grade)
        g = hierarchy.setdefault(p.grade, {})
        s = g.setdefault(p.subject, {})
        u = p.unit if p.unit else "Diger"
        kaz_list = s.setdefault(u, [])
        for lo in p.learning_outcomes:
            lo_s = lo.strip()
            if lo_s and len(lo_s) >= 10 and lo_s not in kaz_list:
                kaz_list.append(lo_s)

    sorted_siniflar = sorted(siniflar, key=_grade_sort_key)
    result = {"hierarchy": hierarchy, "siniflar": sorted_siniflar}
    st.session_state[key] = result
    return result


# ============================================================
# PDF YARDIMCILARI
# ============================================================

_INTRO_PATTERNS = [
    "istiklal marsi", "istiklal marşı", "istiklâl marşı",
    "korkma sonmez", "korkma sönmez",
    "icindekiler", "içindekiler",
    "ders kitabi", "ders kitabı",
    "milli egitim bakanligi", "millî eğitim bakanlığı", "milli eğitim bakanlığı",
    "talim ve terbiye", "t.c. milli", "t.c. millî",
    "isbn", "baski", "baskı", "basim", "basım",
    "telif hakki", "telif hakkı",
    "komisyon", "hazirlayanlar", "hazırlayanlar",
    "editör", "redaksiyon", "önsöz", "onsoz", "sunuş", "sunus",
    "bu kitap", "bu kitabı", "bu kitabi",
    "ogretim programi", "öğretim programı",
    "kazanim tablosu", "kazanım tablosu",
    "konu basliklari", "konu başlıkları",
    "unite ", "ünite ",
]


def _detect_content_start(pdf_bytes, max_scan=15):
    try:
        import fitz
    except ImportError:
        return 1
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total = len(doc)
    for page_idx in range(min(total, max_scan)):
        page_text = doc[page_idx].get_text("text").strip()
        if not page_text:
            continue
        lower = page_text.lower().replace("İ", "i").replace("I", "ı")
        if re.search(r'(?:soru\s*1[.\s)]|^1[.)]\s)', lower, re.MULTILINE):
            doc.close()
            return page_idx + 1
        is_intro = len(page_text) < 100
        if not is_intro:
            for pat in _INTRO_PATTERNS:
                if pat in lower:
                    is_intro = True
                    break
        if not is_intro:
            doc.close()
            return page_idx + 1
    doc.close()
    return 1


def _extract_pdf_text_for_context(pdf_bytes, start_page=None, end_page=None):
    """PDF'den seçilen sayfa aralığının TAMAMINI çıkarır (limit yok).
    Pipeline her batch için farklı bölümü kullanır → kitabın tamamından soru üretilir.
    """
    try:
        import fitz
    except ImportError:
        return "", 0, 0
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)
    s = max(0, (start_page - 1) if start_page else 0)
    e = min(total_pages, end_page if end_page else total_pages)
    text_parts = []
    extracted = 0
    for pn in range(s, e):
        pt = doc[pn].get_text("text").strip()
        if not pt:
            continue
        text_parts.append(pt)
        extracted += 1
    doc.close()
    return "\n\n".join(text_parts), total_pages, extracted


# ============================================================
# ANA GİRİŞ — 3 ADIMLI WIZARD
# ============================================================

def render_meb_osym_tab(store: DataStore = None):
    inject_common_css("msv")
    if store is None:
        store = get_store()
    _init_state()

    step = st.session_state.meb_step

    # Üst bar: başlık + sıfırla
    c_title, c_reset = st.columns([0.85, 0.15])
    with c_title:
        styled_section("MEB/ÖSYM Soru Uretici", "#4a148c")
    with c_reset:
        if step > 1:
            if st.button("Sifirla", key="meb_reset", use_container_width=True):
                _reset_state()
                st.rerun()

    # 3 adım göstergesi
    labels = ["Ayarlar", "Uretim", "Sonuclar"]
    cols = st.columns(3)
    for i, (col, lbl) in enumerate(zip(cols, labels), 1):
        with col:
            if i < step:
                clr, ic = "#10b981", "✅"
            elif i == step:
                clr, ic = "#2563eb", f"<b>{i}</b>"
            else:
                clr, ic = "#94a3b8", str(i)
            op = "1" if i <= step else "0.4"
            st.markdown(
                f'<div style="text-align:center;opacity:{op}">'
                f'<div style="width:30px;height:30px;border-radius:50%;background:{clr};'
                f'color:#fff;display:inline-flex;align-items:center;justify-content:center;'
                f'font-size:0.8rem;font-weight:700;margin-bottom:2px">{ic}</div>'
                f'<div style="font-size:0.75rem;font-weight:600;color:{clr}">{lbl}</div>'
                f'</div>', unsafe_allow_html=True)

    st.markdown("---")

    if step == 1:
        _step1_ayarlar(store)
    elif step == 2:
        _step2_uretim(store)
    elif step == 3:
        _step3_sonuclar(store)


# ============================================================
# ADIM 1: AYARLAR (sınıf + ders + kaynak + soru sayısı)
# ============================================================

def _step1_ayarlar(store):
    # Cache'li hiyerarşi kullan — her rerun'da yeniden hesaplamaz
    plan_cache = _get_plan_hierarchy(store)
    hierarchy = plan_cache["hierarchy"]
    siniflar = plan_cache["siniflar"]

    # --- Sınıf & Ders ---
    c1, c2 = st.columns(2)
    with c1:
        if siniflar:
            grade = st.selectbox("Sinif", siniflar, format_func=_grade_label, key="meb_s1_grade")
        else:
            grade = st.selectbox("Sinif", GRADES, index=7, format_func=_grade_label, key="meb_s1_grade_2")
    with c2:
        grade_data = hierarchy.get(grade, {})
        dersler = sorted(grade_data.keys()) if grade_data else SUBJECTS
        subject = st.selectbox("Ders", dersler, key="meb_s1_subject")

    # --- Kaynak modu ---
    st.markdown("---")
    input_mode = st.radio(
        "Kaynak",
        ["kazanim", "pdf_upload", "paste"],
        format_func=lambda x: {"kazanim": "Kazanim Bazli", "pdf_upload": "PDF Yukle", "paste": "Metin Yapistir"}[x],
        horizontal=True, key="meb_s1_mode",
    )

    kazanimlar = []

    if input_mode == "kazanim":
        # Kazanım seçimi — cache'den hızlı
        uniteler = hierarchy.get(grade, {}).get(subject, {})
        if uniteler:
            tum_kaz = []
            for kaz_list in uniteler.values():
                tum_kaz.extend(kaz_list)

            secilen_unite = st.multiselect(
                f"Unite Secin ({len(uniteler)} unite, {len(tum_kaz)} kazanim)",
                list(uniteler.keys()), key="meb_s1_unite")
            if secilen_unite:
                for u in secilen_unite:
                    kazanimlar.extend(uniteler.get(u, []))
            else:
                kazanimlar = tum_kaz
            st.caption(f"{len(kazanimlar)} kazanim secildi")
        if not kazanimlar:
            manual = st.text_area("Manuel kazanim girin (satir basina bir kazanim)", height=100, key="meb_s1_manual")
            if manual:
                kazanimlar = [l.strip() for l in manual.strip().split("\n") if l.strip() and len(l.strip()) >= 10]

    elif input_mode == "pdf_upload":
        uploaded = st.file_uploader("PDF yukleyin", type=["pdf"], key="meb_s1_pdf")
        if uploaded:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded, allowed_types=["pdf"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded = None
        if uploaded:
            pdf_bytes = uploaded.getvalue()

            # Sayfa sayısı + auto_start (sadece yeni dosyada hesapla)
            if st.session_state.get("_meb_pdf_name") != uploaded.name:
                try:
                    import fitz
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    st.session_state["_meb_pdf_pages"] = len(doc)
                    doc.close()
                except Exception:
                    st.session_state["_meb_pdf_pages"] = 100
                st.session_state["_meb_pdf_auto"] = _detect_content_start(pdf_bytes)
                st.session_state["_meb_pdf_name"] = uploaded.name

            total_pages = st.session_state.get("_meb_pdf_pages", 100)
            auto_start = st.session_state.get("_meb_pdf_auto", 1)

            if auto_start > 1:
                st.caption(f"Giris sayfalari atlandi, sayfa {auto_start}'dan basliyor.")

            cp1, cp2 = st.columns(2)
            with cp1:
                start_p = st.number_input("Baslangic", 1, total_pages, auto_start, key="meb_s1_sp")
            with cp2:
                end_p = st.number_input("Bitis", 1, total_pages, total_pages, key="meb_s1_ep")

            # Metin çıkarma — CACHE'li (aynı dosya+aralık tekrar çıkarılmaz)
            txt_key = f"{uploaded.name}_{start_p}_{end_p}"
            if st.session_state.get("_meb_txt_key") != txt_key:
                text, pc, ext = _extract_pdf_text_for_context(pdf_bytes, start_p, end_p)
                st.session_state.meb_pdf_context = text
                st.session_state["_meb_txt_pc"] = pc
                st.session_state["_meb_txt_ext"] = ext
                st.session_state["_meb_txt_key"] = txt_key
            else:
                text = st.session_state.meb_pdf_context
                pc = st.session_state.get("_meb_txt_pc", 0)
                ext = st.session_state.get("_meb_txt_ext", 0)
            st.session_state.meb_pdf_filename = uploaded.name

            if text:
                st.caption(f"{pc} sayfa PDF — {ext} sayfa islendi, {len(text):,} karakter (tamamı yüklendi)")
                kazanimlar = [f"PDF: {uploaded.name}"]

                # Görsel çıkarma (sadece dosya/aralık değişince — yavaş)
                img_key = f"{uploaded.name}_{start_p}_{end_p}"
                if st.session_state.get("_meb_img_key") != img_key:
                    try:
                        from utils.gorsel_utils import extract_images_from_pdf
                        pr = max(1, end_p - start_p + 1)
                        images = extract_images_from_pdf(pdf_bytes, start_p, end_p, 100, 100, pr * 5)
                        st.session_state.meb_pdf_images = images
                    except Exception:
                        st.session_state.meb_pdf_images = []
                    st.session_state["_meb_img_key"] = img_key
                imgs = st.session_state.get("meb_pdf_images", [])
                if imgs:
                    st.caption(f"{len(imgs)} gorsel cikarildi")
            else:
                st.warning("PDF'den metin cikarilamadi.")
        else:
            st.session_state.meb_pdf_context = ""
            st.session_state.meb_pdf_images = []

    elif input_mode == "paste":
        pasted = st.text_area(
            "Metin yapistirin",
            height=200,
            placeholder="Ders kitabindan veya kaynaktan konu metnini yapistirin...",
            key="meb_s1_paste",
        )
        if pasted and pasted.strip():
            st.session_state.meb_pdf_context = pasted.strip()
            st.session_state.meb_pdf_filename = "yapistirilan_metin"
            st.session_state.meb_pdf_images = []
            kazanimlar = ["Yapistirilan metin"]
            st.caption(f"{len(pasted.strip())} karakter")
        else:
            st.session_state.meb_pdf_context = ""
            st.session_state.meb_pdf_images = []

    # --- Soru sayısı & Model ---
    st.markdown("---")
    cs1, cs2, cs3 = st.columns([2, 1, 1])
    with cs1:
        count = st.slider("Soru Sayisi", 1, 100, 10, 1, key="meb_s1_count")
    with cs2:
        model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], key="meb_s1_model")
    with cs3:
        engine = select_engine(subject)
        eng_info = ENGINE_LABELS.get(engine, ENGINE_LABELS["SOZEL_MADDE"])
        st.markdown(
            f'<div style="background:{eng_info["color"]}12;border-radius:10px;padding:8px;text-align:center;margin-top:25px">'
            f'{eng_info["emoji"]} <b style="font-size:0.8rem">{eng_info["label"]}</b></div>',
            unsafe_allow_html=True)

    # --- Başlat ---
    st.markdown("")
    is_pdf = input_mode in ("pdf_upload", "paste")
    has_source = bool(kazanimlar) if not is_pdf else bool(st.session_state.get("meb_pdf_context", "").strip())

    if not has_source:
        styled_info_banner("Devam etmek icin bir kaynak secin veya yukleyin.", "warning")

    if st.button("Soru Uret", key="meb_s1_start", type="primary",
                  use_container_width=True, disabled=not has_source):
        profile = get_blueprint_profile(engine, grade, subject)
        st.session_state.meb_grade = grade
        st.session_state.meb_subject = subject
        st.session_state.meb_engine = engine
        st.session_state.meb_kazanimlar = kazanimlar
        st.session_state.meb_count = count
        st.session_state.meb_model = model
        st.session_state.meb_input_mode = "pdf" if is_pdf else "kazanim"
        st.session_state.meb_zorluk_dist = profile.get("zorluk_dagilim", {"Kolay": 40, "Orta": 40, "Zor": 20})
        st.session_state.meb_tur_dist = profile.get("tur_dagilim", {})
        st.session_state.meb_results = None
        st.session_state.meb_generating = True
        st.session_state.meb_step = 2
        st.rerun()


# ============================================================
# ADIM 2: ÜRETİM (otomatik başlat + progress)
# ============================================================

def _step2_uretim(store):
    grade = st.session_state.meb_grade
    subject = st.session_state.meb_subject
    engine = st.session_state.meb_engine
    count = st.session_state.meb_count

    styled_stat_row([
        ("Sinif", _grade_label(grade), "#2563eb", "🏫"),
        ("Ders", subject, "#8b5cf6", "📘"),
        ("Soru", str(count), "#10b981", "📝"),
        ("Model", st.session_state.meb_model, "#f59e0b", "🤖"),
    ])

    # Sonuçlar varsa direkt Step 3'e geç
    if st.session_state.meb_results:
        st.session_state.meb_step = 3
        st.rerun()
        return

    # API key kontrol
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("OPENAI_API_KEY bulunamadi. .env dosyanizi kontrol edin.")
        if st.button("Geri", key="meb_s2_back"):
            st.session_state.meb_step = 1
            st.rerun()
        return

    # Otomatik başlat
    st.markdown("")
    progress_bar = st.progress(0)
    pct_display = st.empty()
    status_text = st.empty()

    pct_display.markdown(
        '<div style="text-align:center;font-size:2.5rem;font-weight:800;color:#2563eb;margin:8px 0">%0</div>',
        unsafe_allow_html=True)

    def _prog(current, total, text):
        pct = current / total if total > 0 else 0
        pi = int(pct * 100)
        progress_bar.progress(pct)
        clr = "#10b981" if pi >= 80 else "#2563eb" if pi >= 40 else "#f59e0b"
        pct_display.markdown(
            f'<div style="text-align:center;font-size:2.5rem;font-weight:800;color:{clr};margin:8px 0">%{pi}</div>',
            unsafe_allow_html=True)
        status_text.markdown(f"🔄 {text}")

    try:
        motor = MebSinavMotoru(api_key=api_key, model=st.session_state.meb_model)

        pdf_context = None
        pdf_images = None
        if st.session_state.get("meb_input_mode") == "pdf":
            pdf_context = st.session_state.get("meb_pdf_context", "")
            pdf_images = st.session_state.get("meb_pdf_images", []) or None

        results = motor.pipeline(
            kazanimlar=st.session_state.meb_kazanimlar,
            grade=grade, subject=subject, count=count,
            zorluk_dist=st.session_state.meb_zorluk_dist,
            tur_dist=st.session_state.meb_tur_dist,
            progress_callback=_prog,
            pdf_context=pdf_context,
            pdf_images=pdf_images,
        )

        st.session_state.meb_results = results
        st.session_state.meb_generating = False
        st.session_state.meb_step = 3
        st.rerun()

    except Exception as e:
        st.error(f"Uretim hatasi: {e}")
        if st.button("Geri", key="meb_s2_err_back"):
            st.session_state.meb_generating = False
            st.session_state.meb_step = 1
            st.rerun()


# ============================================================
# ADIM 3: SONUÇLAR (inceleme + PDF + kaydet — hepsi tek ekran)
# ============================================================

def _step3_sonuclar(store):
    results = st.session_state.meb_results
    if not results:
        st.warning("Uretim sonucu yok.")
        if st.button("Geri", key="meb_s3_nores"):
            st.session_state.meb_step = 1
            st.rerun()
        return

    grade = st.session_state.meb_grade
    subject = st.session_state.meb_subject
    engine = results.get("engine_type", st.session_state.meb_engine)
    sorular = results.get("results", [])

    onay = sum(1 for s in sorular if s.get("validator_status") == "ONAY")
    repair = sum(1 for s in sorular if s.get("validator_status") == "REPAIR")
    red = sum(1 for s in sorular if s.get("validator_status") in ("RED", "BASARISIZ"))

    styled_stat_row([
        ("Toplam", len(sorular), "#2563eb", "📝"),
        ("Onay", onay, "#10b981", "✅"),
        ("Onarim", repair, "#f59e0b", "🔧"),
        ("Red", red, "#ef4444", "❌"),
    ])

    st.markdown("")

    # --- PDF İndirme (en üstte, hemen erişilebilir) ---
    sinav_adi = f"MEB {_grade_label(grade)} {subject} - {datetime.now().strftime('%d.%m.%Y')}"

    # Tüm geçerli soruları otomatik seç
    gecerli = [s for s in sorular if s.get("validator_status") in ("ONAY", "REPAIR")]
    if not gecerli:
        gecerli = sorular  # hiç geçerli yoksa hepsini al

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        pdf_data = _generate_soru_pdf(gecerli, grade, subject, sinav_adi, engine, cozumlu=False)
        if pdf_data:
            st.download_button("📥 Soru PDF", data=pdf_data,
                               file_name=f"MEB_{subject}_{grade}_soru.pdf",
                               mime="application/pdf", key="meb_s3_pdf_soru",
                               use_container_width=True)
        else:
            st.error("PDF olusturulamadi")
    with col_p2:
        pdf_cozumlu = _generate_soru_pdf(gecerli, grade, subject, sinav_adi, engine, cozumlu=True)
        if pdf_cozumlu:
            st.download_button("📥 Cozumlu PDF", data=pdf_cozumlu,
                               file_name=f"MEB_{subject}_{grade}_cozumlu.pdf",
                               mime="application/pdf", key="meb_s3_pdf_cozumlu",
                               use_container_width=True)
    with col_p3:
        pdf_anahtar = _generate_cevap_anahtari_pdf(gecerli, grade, subject, sinav_adi)
        if pdf_anahtar:
            st.download_button("📥 Cevap Anahtari", data=pdf_anahtar,
                               file_name=f"MEB_{subject}_{grade}_cevap.pdf",
                               mime="application/pdf", key="meb_s3_pdf_cevap",
                               use_container_width=True)

    # --- Kaydetme ---
    st.markdown("")
    col_save1, col_save2 = st.columns(2)
    with col_save1:
        if st.button("💾 Soru Bankasina Kaydet", key="meb_s3_save", use_container_width=True):
            saved = 0
            for s in gecerli:
                try:
                    q = MebSinavMotoru.to_question_model(s, grade, subject)
                    q.status = "approved"
                    store.add_question(q)
                    saved += 1
                except Exception:
                    pass
            if saved:
                styled_info_banner(f"{saved} soru kaydedildi!", "success")
    with col_save2:
        if st.session_state.get("meb_exam_saved"):
            st.success("Sinav arsive kaydedildi!")
        else:
            if st.button("📋 Sinav Arsivine Kaydet", key="meb_s3_exam", use_container_width=True):
                exam = _build_exam_dict(gecerli, grade, subject, sinav_adi, engine)
                if _save_meb_exam(exam):
                    st.session_state.meb_exam_saved = True
                    st.rerun()

    # --- Soru Listesi ---
    st.markdown("---")
    styled_section("Sorular", "#2563eb")

    for idx, soru in enumerate(sorular):
        score = soru.get("validator_score", 0)
        status = soru.get("validator_status", "?")
        kok = soru.get("kok", "(Bos)")

        if score >= 85:
            bc = "#10b981"
        elif score >= 75:
            bc = "#f59e0b"
        else:
            bc = "#ef4444"

        zorluk = soru.get("zorluk", "")
        header = (
            f'<div style="border-left:4px solid {bc};border-radius:0 10px 10px 0;'
            f'padding:10px 14px;background:{bc}08;margin:4px 0">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="font-weight:700;color:#94A3B8">Soru {idx+1}</span>'
            f'<span>{_styled_badge(status, bc)} {_styled_badge(zorluk, "#8b5cf6")}</span>'
            f'</div></div>'
        )
        st.markdown(header, unsafe_allow_html=True)

        st.markdown(f"**{kok}**")

        # Görsel
        gorsel_bytes = soru.get("gorsel_bytes")
        if gorsel_bytes:
            st.image(gorsel_bytes, width=400)

        # Veri tablosu
        vt = soru.get("veri_tablosu")
        if vt and isinstance(vt, dict) and vt.get("sutunlar"):
            html = _render_veri_tablosu_html(vt)
            if html:
                st.markdown(html, unsafe_allow_html=True)
            if not gorsel_bytes and vt.get("satirlar"):
                try:
                    from utils.gorsel_utils import generate_chart_from_veri_tablosu
                    chart = generate_chart_from_veri_tablosu(vt)
                    if chart:
                        st.image(chart, width=500)
                except Exception:
                    pass

        # Şıklar
        secenekler = soru.get("secenekler", {})
        cevap = soru.get("cevap", "")
        for harf, metin in secenekler.items():
            marker = " ✓" if harf == cevap else ""
            st.markdown(f"**{harf})** {metin}{marker}")

        # Gerekçe
        gerekce = soru.get("gerekce", "")
        if gerekce:
            with st.expander("Cozum"):
                st.markdown(gerekce)

        st.markdown("")

    # --- Alt butonlar ---
    st.markdown("---")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🔄 Tekrar Uret", key="meb_s3_retry", use_container_width=True):
            st.session_state.meb_results = None
            st.session_state.meb_generating = True
            st.session_state.meb_exam_saved = False
            st.session_state.meb_step = 2
            st.rerun()
    with col_b2:
        if st.button("Yeni Sinav", key="meb_s3_new", use_container_width=True):
            _reset_state()
            st.rerun()


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def _build_exam_dict(sorular, grade, subject, sinav_adi, engine):
    exam_kod = f"MEB_{uuid.uuid4().hex[:6].upper()}"
    harf_sirasi = ["A", "B", "C", "D", "E"]
    questions_list = []
    for i, soru in enumerate(sorular, 1):
        sec_dict = soru.get("secenekler", {})
        sec_list = []
        dogru_idx = 0
        cevap_harf = soru.get("cevap", "A")
        for j, harf in enumerate(harf_sirasi):
            if harf in sec_dict:
                sec_list.append(sec_dict[harf])
                if harf == cevap_harf:
                    dogru_idx = j
        q = {
            "numara": i, "metin": soru.get("kok", ""),
            "secenekler": sec_list, "dogru": dogru_idx,
            "gerekce": soru.get("gerekce", ""),
            "zorluk": soru.get("zorluk", "Orta"),
            "soru_tipi": soru.get("soru_tipi", ""),
            "beceri_etiketi": soru.get("beceri_etiketi", ""),
            "validator_score": soru.get("validator_score", 0),
            "engine_type": soru.get("engine_type", engine),
        }
        vt = soru.get("veri_tablosu")
        if vt and isinstance(vt, dict) and vt.get("sutunlar"):
            q["veri_tablosu"] = vt
        questions_list.append(q)

    return {
        "kod": exam_kod, "ad": sinav_adi, "sinif": grade,
        "sinav_turu": "MEB/ÖSYM",
        "ders_dagilimi": {subject: len(questions_list)},
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "created_at": datetime.now().isoformat(),
        "toplam_soru": len(questions_list),
        "sorular": questions_list,
        "status": "draft", "source": "meb_pipeline",
        "engine": engine, "grade": grade, "subject": subject,
    }


def _save_meb_exam(exam_dict):
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "data", "olcme", "saved_exams.json")
        exams = []
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    exams = json.load(f)
            except (json.JSONDecodeError, ValueError):
                exams = []
        found = False
        for i, e in enumerate(exams):
            if e.get('kod') == exam_dict.get('kod'):
                exams[i] = exam_dict
                found = True
                break
        if not found:
            exams.append(exam_dict)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(exams, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


# ============================================================
# PDF ÜRETİMİ
# ============================================================

def _generate_soru_pdf(sorular, grade, subject, sinav_adi, engine, cozumlu=False):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        return None
    try:
        from utils.shared_data import ensure_turkish_pdf_fonts
        font_name, font_bold = ensure_turkish_pdf_fonts()
    except Exception:
        font_name, font_bold = "Helvetica", "Helvetica-Bold"

    try:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                                leftMargin=2*cm, rightMargin=2*cm)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='MEB_Baslik', fontSize=16, leading=20,
                                  alignment=TA_CENTER, spaceAfter=12, fontName=font_bold))
        styles.add(ParagraphStyle(name='MEB_Alt', fontSize=10, leading=14,
                                  alignment=TA_CENTER, spaceAfter=20, textColor=colors.grey, fontName=font_name))
        styles.add(ParagraphStyle(name='MEB_Soru', fontSize=10, leading=14,
                                  spaceAfter=8, fontName=font_name))
        styles.add(ParagraphStyle(name='MEB_Sec', fontSize=10, leading=13,
                                  leftIndent=20, fontName=font_name))
        styles.add(ParagraphStyle(name='MEB_Dogru', fontSize=10, leading=13,
                                  leftIndent=20, fontName=font_bold, textColor=colors.HexColor('#059669')))
        styles.add(ParagraphStyle(name='MEB_CozB', fontSize=10, leading=13, leftIndent=20,
                                  fontName=font_bold, textColor=colors.HexColor('#1e40af'), spaceBefore=6, spaceAfter=2))
        styles.add(ParagraphStyle(name='MEB_CozM', fontSize=9, leading=12, leftIndent=30,
                                  fontName=font_name, textColor=colors.HexColor('#4b5563'), spaceAfter=6))

        els = []
        els.append(Paragraph(sinav_adi, styles['MEB_Baslik']))
        lbl = "COZUMLU" if cozumlu else "SORU"
        els.append(Paragraph(
            f"{_grade_label(grade)} | {subject} | {datetime.now().strftime('%d.%m.%Y')} | {len(sorular)} Soru | {lbl}",
            styles['MEB_Alt']))
        els.append(Spacer(1, 0.5*cm))

        info = Table([["Ad Soyad:", "______________________", "No:", "________"]],
                     colWidths=[3*cm, 6*cm, 2*cm, 4*cm])
        info.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), font_name),
                                  ('FONTSIZE', (0,0), (-1,-1), 10),
                                  ('BOTTOMPADDING', (0,0), (-1,-1), 8)]))
        els.append(info)
        els.append(Spacer(1, 0.5*cm))

        if cozumlu:
            styles.add(ParagraphStyle(name='MEB_CozNot', fontSize=9, leading=12, fontName=font_bold,
                                      textColor=colors.HexColor('#1e40af'), alignment=TA_CENTER, spaceAfter=10))
            els.append(Paragraph("( COZUMLU )", styles['MEB_CozNot']))

        for i, soru in enumerate(sorular, 1):
            kok = soru.get("kok", "")
            cvp = soru.get("cevap", "")
            els.append(Paragraph(f"<b>Soru {i}.</b> {kok}", styles['MEB_Soru']))

            # Veri tablosu
            vt = soru.get("veri_tablosu")
            if vt and isinstance(vt, dict):
                vt_s = vt.get("sutunlar", [])
                vt_r = vt.get("satirlar", [])
                vt_b = vt.get("baslik", "")
                if vt_s and vt_r:
                    if vt_b:
                        bs = ParagraphStyle(name=f'VTB_{i}', parent=styles['MEB_Soru'],
                                            fontSize=9, alignment=TA_CENTER, fontName=font_bold, spaceBefore=4, spaceAfter=4)
                        els.append(Paragraph(vt_b, bs))
                    hdr = [Paragraph(f"<b>{str(c)}</b>", styles['MEB_Sec']) for c in vt_s]
                    td = [hdr]
                    for row in vt_r:
                        cells = row if isinstance(row, list) else [row]
                        r = [Paragraph(str(v), styles['MEB_Sec']) for v in cells]
                        while len(r) < len(vt_s): r.append(Paragraph("-", styles['MEB_Sec']))
                        td.append(r)
                    cw = (A4[0] - 5*cm) / len(vt_s)
                    t = Table(td, colWidths=[cw]*len(vt_s))
                    t.setStyle(TableStyle([
                        ('FONTNAME', (0,0), (-1,0), font_bold), ('FONTNAME', (0,1), (-1,-1), font_name),
                        ('FONTSIZE', (0,0), (-1,-1), 9),
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#131825')),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fb')]),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 5), ('TOPPADDING', (0,0), (-1,-1), 5),
                    ]))
                    els.append(t)
                    els.append(Spacer(1, 0.2*cm))

            # Görsel
            gb = soru.get("gorsel_bytes")
            if gb:
                try:
                    from utils.gorsel_utils import create_reportlab_image
                    img = create_reportlab_image(gb, 14, 8)
                    if img: els.append(img); els.append(Spacer(1, 0.2*cm))
                except Exception: pass
            elif vt and isinstance(vt, dict) and vt.get("satirlar"):
                try:
                    from utils.gorsel_utils import generate_chart_from_veri_tablosu, create_reportlab_image
                    cpng = generate_chart_from_veri_tablosu(vt)
                    if cpng:
                        ci = create_reportlab_image(cpng, 14, 7)
                        if ci: els.append(ci); els.append(Spacer(1, 0.2*cm))
                except Exception: pass

            # Şıklar
            for h, m in soru.get("secenekler", {}).items():
                if cozumlu and h == cvp:
                    els.append(Paragraph(f"{h}) {m}  ✓", styles['MEB_Dogru']))
                else:
                    els.append(Paragraph(f"{h}) {m}", styles['MEB_Sec']))

            if cozumlu:
                g = soru.get("gerekce", "")
                if g:
                    els.append(Paragraph("Cozum:", styles['MEB_CozB']))
                    els.append(Paragraph(g, styles['MEB_CozM']))

            els.append(Spacer(1, 0.3*cm))

        doc.build(els)
        return buf.getvalue()
    except Exception:
        import traceback
        traceback.print_exc()
        return None


def _generate_cevap_anahtari_pdf(sorular, grade, subject, sinav_adi):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER
    except ImportError:
        return None
    try:
        from utils.shared_data import ensure_turkish_pdf_fonts
        font_name, font_bold = ensure_turkish_pdf_fonts()
    except Exception:
        font_name, font_bold = "Helvetica", "Helvetica-Bold"

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CA_B', fontSize=16, leading=20,
                              alignment=TA_CENTER, spaceAfter=8, fontName=font_bold))
    styles.add(ParagraphStyle(name='CA_S', fontSize=11, leading=14,
                              alignment=TA_CENTER, spaceAfter=6, textColor=colors.HexColor('#dc2626'), fontName=font_bold))
    styles.add(ParagraphStyle(name='CA_I', fontSize=10, leading=14,
                              alignment=TA_CENTER, spaceAfter=20, textColor=colors.grey, fontName=font_name))

    els = []
    els.append(Paragraph(sinav_adi, styles['CA_B']))
    els.append(Paragraph("CEVAP ANAHTARI", styles['CA_S']))
    els.append(Paragraph(
        f"{_grade_label(grade)} | {subject} | {datetime.now().strftime('%d.%m.%Y')} | {len(sorular)} Soru",
        styles['CA_I']))
    els.append(Spacer(1, 0.5*cm))

    cevaplar = [(i+1, s.get("cevap", "")) for i, s in enumerate(sorular)]
    rc = (len(cevaplar) + 4) // 5
    td = [["No", "Cvp", "No", "Cvp", "No", "Cvp", "No", "Cvp", "No", "Cvp"]]
    for r in range(rc):
        row = []
        for c in range(5):
            idx = r + c * rc
            if idx < len(cevaplar):
                sno, cv = cevaplar[idx]
                row.extend([str(sno), cv])
            else:
                row.extend(["", ""])
        td.append(row)

    t = Table(td, colWidths=[1.5*cm, 1.5*cm] * 5)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), font_bold), ('FONTNAME', (0,1), (-1,-1), font_name),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8), ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    els.append(t)
    doc.build(els)
    return buf.getvalue()
