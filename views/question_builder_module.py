"""
Soru Olusturma Modulu (LEGACY MONOLITH)
========================================
DIKKAT: Bu dosya views/question_builder/ paketine refactor edilme surecindedir.
Temel fonksiyonlar (_constants, _helpers, _paths, _io, _state) pakete tasindi
ancak render ve PDF fonksiyonlari hala buradan import edilmektedir.
Silinmemelidir — views/question_builder/__init__.py tarafindan kullanilmaktadir.
"""

from __future__ import annotations

import io
import os
import random
import re
import base64
import textwrap
import math
import zipfile
import json
import hashlib
import glob
import tempfile
import subprocess
import html
from datetime import datetime

import base64
import pandas as pd
import streamlit as st

from services.question_generation import GenerationRequest, GenerationResult, generate_question_batch
from utils.learning_outcomes import load_outcomes_from_excels, MONTHS_TR
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("olcme_degerlendirme")
except Exception:
    pass
from views import assessment_evaluation as measure_eval
from views.pdf_question_importer import render_pdf_question_importer

DEFAULT_EXAM_TYPES = [
    "Deneme Sınavı",
    "TYT",
    "Okul Yazilisi",
    "Bursluluk Sınavı",
    "Seviye Tespit Sınavı",
]

DEFAULT_QUESTION_TYPES = [
    "Çoktan Secmeli (ABCD)",
    "Çoktan Secmeli (ABCDE)",
    "Dogru/Yanlis",
    "Bosluk Doldurma",
    "Açık Uclu",
    "Klasik",
    "Karisik",
]

DEFAULT_SUBJECTS = [
    "Matematik",
    "Fizik",
    "Kimya",
    "Biyoloji",
    "Turk Dili ve Edebiyati",
    "Tarih",
    "Cografya",
    "Felsefe",
    "Ingilizce",
    "Din Kulturu",
    "Psikoloji",
    "Sosyoloji",
]

TENANT_ROOT = os.path.join("data", "tenants")

DEFAULT_COVER_RULES = [
    "Cevap kagidi uzerindeki kodlamalari kursun kalemle yapiniz.",
    "Degistirmek istediginiz bir cevabi, yumusak silgiyle cevap kagidini orselemeden temizce siliniz ve yeni cevabinizi kodlayiniz.",
    "Kitapcik turunu cevap kagidinizdaki ilgili alana kodlayiniz.",
    "Soru kitapcigi uzerinde yapilip cevap kagidina isaretlenmeyen cevaplar degerlendirmeye alinmaz.",
    "Puanlama; her test için yanlis cevap sayisinin ucte biri dogru cevap sayisindan cikarilarak yapilir.",
]


# ==================== STATE ====================

def init_question_state() -> None:
    if "question_bank" not in st.session_state:
        st.session_state.question_bank = []
    if "question_bank_loaded" not in st.session_state:
        st.session_state.question_bank_loaded = False
    if "gen01_auto_imported" not in st.session_state:
        st.session_state.gen01_auto_imported = False
    if "tenant_name" not in st.session_state:
        st.session_state.tenant_name = "UZ Koleji"
    if "loaded_tenant" not in st.session_state:
        st.session_state.loaded_tenant = ""
    if "exam_types" not in st.session_state:
        st.session_state.exam_types = DEFAULT_EXAM_TYPES.copy()
    else:
        if "TYT" not in st.session_state.exam_types:
            st.session_state.exam_types.append("TYT")
    if "question_types" not in st.session_state:
        st.session_state.question_types = DEFAULT_QUESTION_TYPES.copy()
    if "uploaded_sources" not in st.session_state:
        st.session_state.uploaded_sources = []
    if "latest_exam" not in st.session_state:
        st.session_state.latest_exam = None
    if "outcomes_data" not in st.session_state:
        st.session_state.outcomes_data = []
    if "outcomes_errors" not in st.session_state:
        st.session_state.outcomes_errors = []
    if "selected_outcome_ids" not in st.session_state:
        st.session_state.selected_outcome_ids = []
    if "outcomes_loaded_once" not in st.session_state:
        st.session_state.outcomes_loaded_once = False
    if "selected_exam_types" not in st.session_state:
        st.session_state.selected_exam_types = []
    if "selected_subjects" not in st.session_state:
        st.session_state.selected_subjects = []
    if "selected_question_types" not in st.session_state:
        st.session_state.selected_question_types = []
    if "subject_question_counts" not in st.session_state:
        st.session_state.subject_question_counts = {}
    if "selected_level" not in st.session_state:
        st.session_state.selected_level = "Lise"
    if "selected_grade" not in st.session_state:
        st.session_state.selected_grade = 9
    if "ai_question_prompt" not in st.session_state:
        st.session_state.ai_question_prompt = ""
    if "ai_question_result" not in st.session_state:
        st.session_state.ai_question_result = None
    if "ai_question_count" not in st.session_state:
        st.session_state.ai_question_count = 5
    if "ai_question_include_diagram" not in st.session_state:
        st.session_state.ai_question_include_diagram = True
    if "selected_section" not in st.session_state:
        st.session_state.selected_section = "A"
    if "school_name" not in st.session_state:
        st.session_state.school_name = st.session_state.tenant_name
    if "school_logo_bytes" not in st.session_state:
        st.session_state.school_logo_bytes = None
    if "brand_primary" not in st.session_state:
        st.session_state.brand_primary = "#0F4C81"
    if "brand_secondary" not in st.session_state:
        st.session_state.brand_secondary = "#F2A900"
    if "booklet_type" not in st.session_state:
        st.session_state.booklet_type = "A"
    if "include_topic_distribution" not in st.session_state:
        st.session_state.include_topic_distribution = True
    if "cover_two_column" not in st.session_state:
        st.session_state.cover_two_column = True
    if "cover_instructions" not in st.session_state:
        st.session_state.cover_instructions = DEFAULT_COVER_RULES.copy()
    if "fast_graph_mode" not in st.session_state:
        st.session_state.fast_graph_mode = True
    if "store_generated_questions" not in st.session_state:
        st.session_state.store_generated_questions = True
    if "pdf_subjects_prefilled" not in st.session_state:
        st.session_state.pdf_subjects_prefilled = False
    if "pdf_import_report" not in st.session_state:
        st.session_state.pdf_import_report = None
    if "pdf_external_use_pool" not in st.session_state:
        st.session_state.pdf_external_use_pool = True
    if "pdf_external_allow_upload" not in st.session_state:
        st.session_state.pdf_external_allow_upload = True
    if "external_prefill_done" not in st.session_state:
        st.session_state.external_prefill_done = False
    if "builder_started" not in st.session_state:
        st.session_state.builder_started = False
    if "bank_source_filter" not in st.session_state:
        st.session_state.bank_source_filter = "all"
    if "store_bulk_questions" not in st.session_state:
        st.session_state.store_bulk_questions = False
    if "use_bank_questions" not in st.session_state:
        st.session_state.use_bank_questions = True
    if "bank_min_score" not in st.session_state:
        st.session_state.bank_min_score = 0
    if "selected_difficulty" not in st.session_state:
        st.session_state.selected_difficulty = "Karisik"
    if "ai_last_error" not in st.session_state:
        st.session_state.ai_last_error = ""
    if "question_count" not in st.session_state:
        st.session_state.question_count = 20
    if "student_list" not in st.session_state:
        st.session_state.student_list = []
    if "selected_student_ids" not in st.session_state:
        st.session_state.selected_student_ids = []

    if st.session_state.tenant_name != st.session_state.loaded_tenant:
        settings = load_tenant_settings(st.session_state.tenant_name)
        st.session_state.school_name = settings.get("school_name", st.session_state.tenant_name)
        st.session_state.brand_primary = settings.get("brand_primary", st.session_state.brand_primary)
        st.session_state.brand_secondary = settings.get("brand_secondary", st.session_state.brand_secondary)
        st.session_state.booklet_type = settings.get("booklet_type", st.session_state.booklet_type)
        st.session_state.include_topic_distribution = settings.get(
            "include_topic_distribution",
            st.session_state.include_topic_distribution,
        )
        st.session_state.cover_instructions = settings.get(
            "cover_instructions",
            st.session_state.cover_instructions,
        )
        st.session_state.question_bank = load_question_bank(st.session_state.tenant_name)
        st.session_state.loaded_tenant = st.session_state.tenant_name
        st.session_state.question_bank_loaded = True


def render_cover_settings() -> None:
    st.subheader("Sınav Kapagi")
    st.session_state.school_name = st.session_state.tenant_name
    st.text_input(
        "Okul adi",
        value=st.session_state.school_name,
        disabled=True,
    )
    logo_file = st.file_uploader(
        "Okul logosu (PNG/JPG)",
        type=["png", "jpg", "jpeg"],
    )
    if logo_file is not None:
        from utils.security import validate_upload
        _ok, _msg = validate_upload(logo_file, allowed_types=["png", "jpg", "jpeg"], max_mb=50)
        if not _ok:
            st.error(f"⚠️ {_msg}")
            logo_file = None
    if logo_file is not None:
        st.session_state.school_logo_bytes = logo_file.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.brand_primary = st.color_picker(
            "Kurumsal ana renk",
            value=st.session_state.brand_primary,
        )
    with col2:
        st.session_state.brand_secondary = st.color_picker(
            "Kurumsal ikincil renk",
            value=st.session_state.brand_secondary,
        )

    st.session_state.booklet_type = st.selectbox(
        "Kitapcik tipi",
        ["A", "B", "C", "D"],
        index=["A", "B", "C", "D"].index(st.session_state.booklet_type),
    )
    st.session_state.include_topic_distribution = st.checkbox(
        "Konu dagilimi sayfasi ekle",
        value=st.session_state.include_topic_distribution,
    )
    st.session_state.cover_two_column = st.checkbox(
        "Kapak iki sutun yerlesim",
        value=st.session_state.cover_two_column,
    )
    instructions_text = st.text_area(
        "Kapak uyarilari (her satir bir madde)",
        value="\n".join(st.session_state.cover_instructions),
        height=140,
    )
    st.session_state.cover_instructions = [
        line.strip() for line in instructions_text.splitlines() if line.strip()
    ]

    if st.session_state.school_logo_bytes:
        st.image(st.session_state.school_logo_bytes, width=120)
    if st.session_state.school_name:
        st.markdown(f"**{st.session_state.school_name}**")

    save_tenant_settings(
        st.session_state.tenant_name,
        {
            "school_name": st.session_state.school_name,
            "brand_primary": st.session_state.brand_primary,
            "brand_secondary": st.session_state.brand_secondary,
            "booklet_type": st.session_state.booklet_type,
            "include_topic_distribution": st.session_state.include_topic_distribution,
            "cover_instructions": st.session_state.cover_instructions,
        },
    )


def compute_quality_score(question: dict) -> int:
    score = 0
    source = question.get("source", "")
    if source == "ai":
        score += 40
    elif source == "graph":
        score += 30
    else:
        score += 15
    if question.get("image_bytes"):
        score += 20
    if len(question.get("options", [])) >= 4:
        score += 10
    if question.get("outcomes"):
        score += 10
    if question.get("question_type") == "Çoktan Secmeli (ABCD)":
        score += 5
    return min(score, 100)


def load_question_bank(tenant_name: str) -> list[dict]:
    try:
        path = get_question_bank_path(tenant_name)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            if isinstance(data, list):
                for item in data:
                    if "quality_score" not in item:
                        item["quality_score"] = compute_quality_score(item)
                    if "difficulty" not in item:
                        item["difficulty"] = "medium"
                return data
    except Exception:
        return []
    return []


def save_question_bank(tenant_name: str, bank: list[dict]) -> None:
    path = get_question_bank_path(tenant_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        cleaned = [sanitize_question_for_storage(item) for item in bank]
        json.dump(cleaned, handle, ensure_ascii=False, indent=2)


def list_original_pdfs(tenant_name: str) -> list[str]:
    originals_dir = os.path.join(get_tenant_dir(tenant_name), "uploads", "originals")
    if not os.path.isdir(originals_dir):
        return []
    return sorted(
        file
        for file in os.listdir(originals_dir)
        if file.lower().endswith(".pdf")
    )


def add_to_question_bank(items: list[dict]) -> None:
    if not items:
        return
    existing = {q.get("text", "").strip() for q in st.session_state.question_bank}
    for item in items:
        item = sanitize_question_for_storage(item)
        text_key = item.get("text", "").strip()
        if not text_key or text_key in existing:
            continue
        if "quality_score" not in item:
            item["quality_score"] = compute_quality_score(item)
        if "difficulty" not in item:
            item["difficulty"] = "medium"
        st.session_state.question_bank.append(item)
        existing.add(text_key)
    save_question_bank(st.session_state.tenant_name, st.session_state.question_bank)


def sanitize_question_for_storage(question: dict) -> dict:
    cleaned = dict(question)
    for key, value in list(cleaned.items()):
        if isinstance(value, (bytes, bytearray)):
            cleaned.pop(key)
    return cleaned


def import_pdf_visual_questions(
    pdf_path: str,
    subject_label: str,
    exam_type_tag: str | None = None,
    subject_tags: list[str] | None = None,
    question_type_override: str | None = None,
    grade_override: int | None = None,
    subject_rule: str | None = None,
    force_rebuild: bool = False,
) -> int:
    ok, reason = measure_eval.check_processing_prereqs()
    if not ok:
        st.error(f"PDF isleme hazir degil: {reason}")
        return 0
    words, _, _ = measure_eval.extract_words_bbox(pdf_path, 1)
    if not words:
        tesseract_exe = measure_eval.find_tesseract_exe()
        if not tesseract_exe:
            st.warning("PDF metin katmani yok. OCR bulunamadı; otomatik bolme sabit kesimle denenecek.")
        else:
            ocr_words, _, _ = measure_eval._extract_words_ocr(pdf_path, 1)
            if not ocr_words:
                st.warning("OCR sonuc vermedi. Sabit kesimle denenecek.")
            else:
                st.warning("PDF metin katmani yok. OCR ile deneniyor, sonuc degisebilir.")
    doc_id = os.path.basename(pdf_path)
    items = measure_eval.load_question_items()
    saved, _ = measure_eval.auto_process_pdf(
        pdf_path,
        "",
        "",
        None,
        subject_label,
        "",
        force_rebuild=force_rebuild,
    )
    if not saved:
        existing = [item for item in items if item.get("doc_id") == doc_id]
        if not existing:
            st.warning("PDF'den soru bulunamadı veya isleme yapilamadi.")
            st.info("Olası neden: PDF metin katmani yoksa otomatik bolme calismaz.")
            return 0
        st.info("Bu PDF daha once islenmis. Var olan sorular havuza aktariliyor.")
    items = measure_eval.load_question_items()
    img_dir = os.path.join(measure_eval.get_module_root(), "question_images")
    questions = []
    rr_index = 0
    subject_override = subject_label if subject_label else None
    if subject_tags and len(subject_tags) == 1:
        subject_override = subject_tags[0]
    for item in items:
        if item.get("doc_id") != doc_id:
            continue
        image_file = item.get("image_file")
        if not image_file:
            continue
        asset_path = os.path.join(img_dir, image_file)
        if not os.path.exists(asset_path):
            continue
        qid = f"pdfimg-{doc_id}-{item.get('page_no')}-{item.get('question_no')}-{item.get('column')}"
        subject_value = subject_label or "PDF"
        if subject_override:
            subject_value = subject_override
        elif subject_tags:
            rule = subject_rule or "Tespit edilen dersi koru"
            if rule == "Rastgele dagit":
                subject_value = subject_tags[rr_index % len(subject_tags)]
                rr_index += 1
            elif rule == "Bilinmiyor olarak isaretle":
                subject_value = "Bilinmiyor"
            else:
                subject_value = subject_tags[0]
        questions.append(
            {
                "id": qid,
                "grade": grade_override if grade_override is not None else st.session_state.selected_grade,
                "subject": subject_value,
                "question_type": question_type_override or "Çoktan Secmeli (ABCD)",
                "difficulty": "medium",
                "text": f"[PDF] {doc_id} {item.get('page_no')}-{item.get('question_no')}",
                "options": [],
                "answer": "",
                "source": "pdf_image",
                "source_pdf": pdf_path,
                "asset_path": asset_path,
            }
        )
        if exam_type_tag:
            questions[-1]["exam_type"] = exam_type_tag
        if subject_tags:
            questions[-1]["subject_tags"] = subject_tags
    if questions:
        add_to_question_bank(questions)
    return len(questions)


def get_gen01_assets_dirs(tenant_name: str) -> list[str]:
    key = tenant_key(tenant_name)
    candidates = []
    base = os.getcwd()
    candidates.append(os.path.join(base, "data", "assets", "tenants", key, "questions"))
    candidates.append(
        os.path.join(
            base,
            "GEN-01_TamPaket",
            "02_Import",
            "python_generator",
            "data",
            "assets",
            "tenants",
            key,
            "questions",
        )
    )
    return [path for path in candidates if os.path.isdir(path)]


def resolve_asset_path(question_id: str, alt_text: str | None, tenant_name: str) -> str | None:
    if not question_id:
        return None
    asset_dirs = get_gen01_assets_dirs(tenant_name)
    if alt_text and alt_text.startswith("FIGURE:"):
        rel = alt_text.split(":", 1)[-1].strip()
        for asset_dir in asset_dirs:
            candidate = os.path.join(asset_dir, os.path.basename(rel))
            if os.path.exists(candidate):
                return candidate
    for asset_dir in asset_dirs:
        candidate = os.path.join(asset_dir, f"{question_id}.png")
        if os.path.exists(candidate):
            return candidate
    return None


def map_gen01_template_to_internal(template_id: str) -> str | None:
    if not template_id:
        return None
    def normalize_template(value: str) -> str:
        table = str.maketrans({
            "Ğ": "G", "ğ": "g",
            "İ": "I", "ı": "i",
            "Ş": "S", "ş": "s",
            "Ç": "C", "ç": "c",
            "Ö": "O", "ö": "o",
            "Ü": "U", "ü": "u",
        })
        return value.translate(table).upper().strip()

    value = normalize_template(template_id)
    mapping = {
        "MAT-LINEAR_GRAPH-01": "COORD_LINE",
        "MAT-PARABOLA-02": "COORD_PARABOLA",
        "MAT-TRIANGLE-03": "GEOM_TRIANGLE",
        "MAT-NUMBER_LINE-04": "INEQ_SHADE",
        "FIZ-VT_GRAPH-01": "KINEMATICS_GRAPH",
        "FIZ-LINEAR_GRAPH-02": "COORD_LINE",
        "KIM-ENERGY_PROFILE-01": "ENERGY_PROFILE",
        "KIM-PH_SCALE-02": "PH_SCALE",
        "BIY-CELL_DIAGRAM-01": "CELL_DIAGRAM",
        "BIY-PUNNETT-02": "GENETICS_PUNNETT",
        "COĞ-CLIMOGRAPH-01": "CLIMOGRAPH",
        "COĞ-POPULATION_PYRAMID-02": "POP_PYRAMID",
        "TAR-TIMELINE-01": "TIMELINE",
    }
    if value in mapping:
        return mapping[value]
    if value.startswith("MAT-") and "LINEAR_GRAPH" in value:
        return "COORD_LINE"
    if value.startswith("MAT-") and "PARABOLA" in value:
        return "COORD_PARABOLA"
    if value.startswith("MAT-") and "TRIANGLE" in value:
        return "GEOM_TRIANGLE"
    if value.startswith("MAT-") and "NUMBER_LINE" in value:
        return "INEQ_SHADE"
    if value.startswith("FIZ-") and "VT_GRAPH" in value:
        return "KINEMATICS_GRAPH"
    if value.startswith("FIZ-") and "LINEAR_GRAPH" in value:
        return "COORD_LINE"
    if value.startswith("KIM-") and "ENERGY_PROFILE" in value:
        return "ENERGY_PROFILE"
    if value.startswith("KIM-") and "PH_SCALE" in value:
        return "PH_SCALE"
    if "CELL_DIAGRAM" in value:
        return "CELL_DIAGRAM"
    if "PUNNETT" in value:
        return "GENETICS_PUNNETT"
    if "CLIMOGRAPH" in value:
        return "CLIMOGRAPH"
    if "POPULATION_PYRAMID" in value:
        return "POP_PYRAMID"
    if "TIMELINE" in value:
        return "TIMELINE"
    if "TABLE_GENERIC" in value:
        return "TRUTH_TABLE"
    return None


def parse_template_id_from_alt_text(alt_text: str | None) -> str | None:
    if not alt_text:
        return None
    if alt_text.startswith("FIGURE:"):
        return None
    raw = alt_text.strip()
    candidate = None
    if "|" in raw:
        parts = [part.strip() for part in raw.split("|") if part.strip()]
        if len(parts) >= 2:
            candidate = parts[1]
    if not candidate:
        match = re.search(r"[A-Z]{2,3}-[A-Z0-9_]+-\d{2}", raw)
        if match:
            candidate = match.group(0)
    if not candidate:
        return None
    return map_gen01_template_to_internal(candidate)


def build_qr_bytes(value: str) -> bytes | None:
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(value)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


# ==================== OUTCOMES ====================

def _normalize_folder_name(value: str) -> str:
    table = str.maketrans({
        "ç": "c",
        "Ç": "c",
        "ğ": "g",
        "Ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "Ö": "o",
        "ş": "s",
        "Ş": "s",
        "ü": "u",
        "Ü": "u",
    })
    return value.translate(table).lower()


def get_outcome_base_dir() -> str:
    cwd = os.getcwd()
    tenant_dir = get_tenant_outcomes_dir(st.session_state.tenant_name)
    if os.path.isdir(tenant_dir):
        return tenant_dir
    direct = os.path.join(cwd, "kazanımlar")
    if os.path.isdir(direct):
        return direct

    # Fallback: find any folder starting with 'kazan' that has Excel files.
    for name in os.listdir(cwd):
        path = os.path.join(cwd, name)
        if not os.path.isdir(path):
            continue
        if not _normalize_folder_name(name).startswith("kazan"):
            continue
        has_excel = any(
            fname.lower().endswith((".xlsx", ".xls"))
            for fname in os.listdir(path)
        )
        if has_excel:
            return path

    return direct


def list_outcome_files(base_dir: str) -> list[str]:
    if not os.path.isdir(base_dir):
        return []
    files = [
        name for name in os.listdir(base_dir)
        if name.lower().endswith((".xlsx", ".xls"))
    ]
    return sorted(files)


def load_outcomes(selected_files: list[str] | None = None) -> None:
    base_dir = get_outcome_base_dir()
    outcomes, errors = load_outcomes_from_excels(base_dir, selected_files=selected_files)
    st.session_state.outcomes_data = outcomes
    st.session_state.outcomes_errors = errors


def get_outcome_map() -> dict:
    return {item["id"]: item for item in st.session_state.outcomes_data}


def get_subjects_from_outcomes() -> list[str]:
    subjects = sorted({item["subject"] for item in st.session_state.outcomes_data})
    if subjects:
        filtered = [subject for subject in subjects if not is_excluded_subject(subject)]
        return filtered
    return DEFAULT_SUBJECTS


def normalize_subject_label(value: str) -> str:
    table = str.maketrans({
        "\u2021": "c",
        "\u20ac": "c",
        "\u00a7": "g",
        "\u00a6": "g",
        "\u008d": "i",
        "\u02dc": "i",
        "\u201d": "o",
        "\u2122": "o",
        "\u0178": "s",
        "\u017e": "s",
        "\u0081": "u",
        "\u0161": "u",
        "\u00e7": "c",
        "\u00c7": "c",
        "\u011f": "g",
        "\u011e": "g",
        "\u0131": "i",
        "\u0130": "i",
        "\u00f6": "o",
        "\u00d6": "o",
        "\u015f": "s",
        "\u015e": "s",
        "\u00fc": "u",
        "\u00dc": "u",
    })
    return str(value).translate(table).lower().strip()


SUBJECT_LABEL_MAP = {
    "tde": "Turk Dili ve Edebiyati",
    "turkdilivedebiyati": "Turk Dili ve Edebiyati",
    "turkdili": "Turk Dili ve Edebiyati",
    "edebiyat": "Turk Dili ve Edebiyati",
    "mat": "Matematik",
    "matematik": "Matematik",
    "fiz": "Fizik",
    "fizik": "Fizik",
    "kim": "Kimya",
    "kimya": "Kimya",
    "bio": "Biyoloji",
    "biyoloji": "Biyoloji",
    "cog": "Cografya",
    "cografya": "Cografya",
    "tar": "Tarih",
    "tarih": "Tarih",
    "ing": "Ingilizce",
    "ingilizce": "Ingilizce",
    "alm": "Almanca",
    "almanca": "Almanca",
    "fr": "Fransizca",
    "fransizca": "Fransizca",
    "fel": "Felsefe",
    "felsefe": "Felsefe",
    "dkab": "Din Kulturu ve Ahlak Bilgisi",
    "din": "Din Kulturu ve Ahlak Bilgisi",
}


def display_subject_label(value: str) -> str:
    norm = normalize_subject_label(value)
    key = re.sub(r"[^a-z0-9]+", "", norm)
    return SUBJECT_LABEL_MAP.get(key, value)


def normalize_subject_key(value: str) -> str:
    norm = normalize_subject_label(value)
    key = re.sub(r"[^a-z0-9]+", "", norm)
    key = re.sub(r"\d+$", "", key)
    mapped = SUBJECT_LABEL_MAP.get(key, value)
    norm2 = normalize_subject_label(mapped)
    key2 = re.sub(r"[^a-z0-9]+", "", norm2)
    return re.sub(r"\d+$", "", key2)


def subject_matches(left: str, right: str) -> bool:
    return normalize_subject_key(left) == normalize_subject_key(right)


def subject_matches_question(question: dict, subject: str) -> bool:
    if subject_matches(question.get("subject", ""), subject):
        return True
    tags = question.get("subject_tags") or []
    return any(subject_matches(tag, subject) for tag in tags)


def is_excluded_subject(value: str) -> bool:
    norm = normalize_subject_label(value)
    return (
        "beden" in norm
        or "spor" in norm
        or "muzik" in norm
        or "gorsel" in norm
        or "sanat" in norm
        or "psikoloji" in norm
        or "sosyoloji" in norm
        or "din" in norm
        or "dkab" in norm
        or "ingiliz" in norm
        or "ing" in norm
    )


def subject_key(value: str) -> str:
    sanitized = normalize_subject_label(value)
    sanitized = re.sub(r"[^a-z0-9]+", "_", sanitized)
    return sanitized.strip("_") or "ders"


def graph_render_settings() -> tuple[float, float, int]:
    fast = st.session_state.get("fast_graph_mode", True)
    if fast:
        return (3.2, 2.2, 80)
    return (4.0, 2.6, 120)


def hex_to_rgb(color: str) -> tuple[float, float, float]:
    value = (color or "").lstrip("#")
    if len(value) != 6:
        return (0, 0, 0)
    r = int(value[0:2], 16) / 255.0
    g = int(value[2:4], 16) / 255.0
    b = int(value[4:6], 16) / 255.0
    return (r, g, b)


def tenant_key(value: str) -> str:
    sanitized = normalize_subject_label(value)
    sanitized = re.sub(r"[^a-z0-9]+", "_", sanitized)
    return sanitized.strip("_") or "tenant"


def get_tenant_dir(name: str) -> str:
    return os.path.join(TENANT_ROOT, tenant_key(name))


def get_question_bank_path(tenant_name: str) -> str:
    return os.path.join(get_tenant_dir(tenant_name), "question_bank.json")


def get_tenant_settings_path(tenant_name: str) -> str:
    return os.path.join(get_tenant_dir(tenant_name), "settings.json")

def get_generation_plan_path(tenant_name: str) -> str:
    return os.path.join(get_tenant_dir(tenant_name), "generation_plan.json")


def get_tenant_outcomes_dir(tenant_name: str) -> str:
    return os.path.join(get_tenant_dir(tenant_name), "kazanımlar")


def load_tenant_settings(tenant_name: str) -> dict:
    path = get_tenant_settings_path(tenant_name)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_tenant_settings(tenant_name: str, payload: dict) -> None:
    path = get_tenant_settings_path(tenant_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def load_generation_plan(tenant_name: str) -> list[dict]:
    path = get_generation_plan_path(tenant_name)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_generation_plan(tenant_name: str, plan: list[dict]) -> None:
    path = get_generation_plan_path(tenant_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, ensure_ascii=False, indent=2)


def list_tenants() -> list[str]:
    tenants = set()
    tenants.add("UZ Koleji")
    if os.path.isdir(TENANT_ROOT):
        for name in os.listdir(TENANT_ROOT):
            path = os.path.join(TENANT_ROOT, name)
            if not os.path.isdir(path):
                continue
            settings_path = os.path.join(path, "settings.json")
            tenant_name = name
            if os.path.exists(settings_path):
                try:
                    with open(settings_path, "r", encoding="utf-8") as handle:
                        data = json.load(handle)
                        tenant_name = data.get("school_name", tenant_name)
                except Exception:
                    pass
            tenants.add(tenant_name)
    return sorted(tenants)


def create_tenant(name: str) -> None:
    if not name:
        return
    payload = {
        "school_name": name,
        "brand_primary": st.session_state.brand_primary,
        "brand_secondary": st.session_state.brand_secondary,
        "booklet_type": st.session_state.booklet_type,
        "include_topic_distribution": st.session_state.include_topic_distribution,
        "cover_instructions": st.session_state.cover_instructions,
    }
    save_tenant_settings(name, payload)


def read_csv_with_fallback(path: str) -> pd.DataFrame:
    for enc in ("utf-8-sig", "cp1254", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    return pd.read_csv(path, encoding="utf-8", errors="ignore")


def map_question_type(value: str) -> str:
    norm = normalize_subject_label(value)
    if "abcde" in norm or "5li" in norm or "5" in norm and "coktan" in norm:
        return "Çoktan Secmeli (ABCDE)"
    if "coktansecmeli" in norm or "coktan" in norm:
        return "Çoktan Secmeli (ABCD)"
    if "dogru" in norm or "yanlis" in norm:
        return "Dogru/Yanlis"
    if "bosluk" in norm:
        return "Bosluk Doldurma"
    if "acik" in norm:
        return "Açık Uclu"
    if "klasik" in norm:
        return "Klasik"
    return "Çoktan Secmeli (ABCD)"


def map_difficulty(value: str) -> str:
    norm = normalize_subject_label(value)
    if "kolay" in norm:
        return "easy"
    if "orta" in norm:
        return "medium"
    if "zor" in norm:
        return "hard"
    return "medium"


def import_questions_from_csv(path: str) -> tuple[list[dict], list[dict]]:
    df = read_csv_with_fallback(path)
    records = []
    errors = []
    seen = set()
    for index, row in df.iterrows():
        fixes = []
        grade = int(row.get("sinif_duzeyi", 0) or 0)
        subject = str(row.get("brans", "")).strip()
        text = str(row.get("soru_metni", "")).strip()
        qtype = map_question_type(str(row.get("soru_tipi", "")))
        difficulty = map_difficulty(str(row.get("zorluk", "")))
        alt_text = str(row.get("alt_text", "")).strip()

        if not text:
            errors.append(
                {
                    "row": index + 1,
                    "reason": "Soru metni bos (satir atlandi).",
                    "status": "error",
                }
            )
            continue
        if not subject:
            subject = "Genel"
            fixes.append("Branş bos -> Genel")
        if grade <= 0:
            grade = 9
            fixes.append("Sınıf bos -> 9")

        options = []
        if qtype == "Çoktan Secmeli (ABCD)":
            options = [
                str(row.get("secenek_a", "")).strip(),
                str(row.get("secenek_b", "")).strip(),
                str(row.get("secenek_c", "")).strip(),
                str(row.get("secenek_d", "")).strip(),
            ]
            options = [opt for opt in options if opt]
            while len(options) < 4:
                options.append("Yukaridakilerin hicbiri")
            if len(options) > 4:
                options = options[:4]
                fixes.append("Fazla secenek -> 4'e kisaltildi")
        elif qtype == "Dogru/Yanlis":
            options = ["Dogru", "Yanlis"]

        answer = ""
        if qtype == "Çoktan Secmeli (ABCD)":
            answer = str(row.get("dogru_secenek", "")).strip().upper()[:1]
            if answer not in {"A", "B", "C", "D"}:
                answer = "A"
                fixes.append("Dogru secenek bos/hatalı -> A")
        elif qtype == "Dogru/Yanlis":
            val = str(row.get("dogru_yanlis_dogru_mu", "")).strip().lower()
            answer = "Dogru" if val in {"true", "1", "dogru"} else "Yanlis"
        elif qtype == "Bosluk Doldurma":
            answer = str(row.get("bosluk_doldurma_cevap", "")).strip()
            if not answer:
                answer = " "
                fixes.append("Bosluk doldurma cevabi eksik -> bos")

        signature = f"{grade}|{subject}|{text}|{'|'.join(options)}"
        if signature in seen:
            errors.append(
                {
                    "row": index + 1,
                    "reason": "Tekrarlayan soru (metin+secenek).",
                    "status": "error",
                }
            )
            continue
        seen.add(signature)

        outcome_text = str(row.get("kazanim_aciklama", "")).strip()
        outcome_code = str(row.get("kazanim_kodu", "")).strip()
        outcomes = []
        if outcome_text:
            if outcome_code:
                outcomes = [f"{outcome_code} - {outcome_text}"]
            else:
                outcomes = [outcome_text]

        template_id = parse_template_id_from_alt_text(alt_text)
        asset_path = resolve_asset_path(
            str(row.get("question_id", "")).strip(),
            alt_text,
            st.session_state.tenant_name,
        )
        record = {
            "id": str(row.get("question_id", "")).strip() or f"csv-{len(records)+1}",
            "grade": grade,
            "subject": subject,
            "question_type": qtype,
            "difficulty": difficulty,
            "text": text,
            "options": options,
            "answer": answer,
            "source": "csv_import",
            "outcome_ids": [],
            "outcomes": outcomes,
            "alt_text": alt_text,
            "template_id": template_id,
            "asset_path": asset_path,
        }
        records.append(record)
        if fixes:
            errors.append(
                {
                    "row": index + 1,
                    "reason": "; ".join(fixes),
                    "status": "fixed",
                }
            )
    return records, errors


def parse_tyt_pdf_answers(pdf_path: str) -> dict[str, dict[int, str]]:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        return {}

    reader = PdfReader(pdf_path)
    answers: dict[str, dict[int, str]] = {}

    subject_keywords = {
        "turk": "Turkce",
        "tork": "Turkce",
        "matematik": "Matematik",
        "fizik": "Fizik",
        "kimya": "Kimya",
        "biyoloji": "Biyoloji",
        "tarih": "Tarih",
        "cografya": "Cografya",
        "felsefe": "Felsefe",
    }

    current_subject = ""
    current_page_number = 1
    for page_index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if not text:
            continue
        current_page_number = page_index + 1
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            norm = normalize_subject_label(line)
            for key, label in subject_keywords.items():
                if key in norm:
                    current_subject = label
                    break
            for number, letter in re.findall(r"(\d+)\.?\s*([A-E])", line):
                if not current_subject:
                    continue
                answers.setdefault(current_subject, {})[int(number)] = letter

    return answers


def parse_tyt_pdf_questions(pdf_path: str) -> list[dict]:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        return []

    reader = PdfReader(pdf_path)
    questions: list[dict] = []
    current_subject = "TYT"
    answers_map = parse_tyt_pdf_answers(pdf_path)
    current_page_number = 1

    subject_keywords = {
        "turkce": "Turkce",
        "matematik": "Matematik",
        "fizik": "Fizik",
        "kimya": "Kimya",
        "biyoloji": "Biyoloji",
        "tarih": "Tarih",
        "cografya": "Cografya",
        "felsefe": "Felsefe",
    }
    skip_markers = {
        "cevap anahtari",
        "soru dagilim tablosu",
        "ogrenme alani",
        "temel yeterlilik testi",
        "tyt cikmis sorular",
        "yks cikmis sorular",
    }

    question_text: list[str] = []
    options: dict[str, str] = {}
    last_option = ""
    current_number: int | None = None

    def flush_question() -> None:
        nonlocal question_text, options, last_option, current_number
        if len(options) < 4:
            question_text = []
            options = {}
            last_option = ""
            current_number = None
            return
        ordered = [options.get("A", ""), options.get("B", ""), options.get("C", ""), options.get("D", "")]
        if "E" in options:
            ordered.append(options.get("E", ""))
        ordered = [opt for opt in ordered if opt]
        joined_text = " ".join(question_text).strip()
        norm_joined = normalize_subject_label(joined_text)
        if any(marker in norm_joined for marker in skip_markers):
            question_text = []
            options = {}
            last_option = ""
            current_number = None
            return
        qtype = "Çoktan Secmeli (ABCDE)" if len(ordered) >= 5 else "Çoktan Secmeli (ABCD)"
        qid = f"tyt-{len(questions)+1}"
        answer = ""
        if current_number is not None:
            answer = answers_map.get(current_subject or "TYT", {}).get(current_number, "")
        questions.append(
            {
                "id": qid,
                "grade": 12,
                "subject": current_subject or "TYT",
                "question_type": qtype,
                "difficulty": "medium",
                "text": joined_text,
                "options": ordered,
                "answer": answer,
                "source_number": current_number,
                "source": "pdf_import",
                "source_pdf": pdf_path,
                "source_page": current_page_number,
                "outcome_ids": [],
                "outcomes": [],
            }
        )
        question_text = []
        options = {}
        last_option = ""
        current_number = None

    for page_index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if not text:
            continue
        current_page_number = page_index + 1
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            norm = normalize_subject_label(line)
            if any(marker in norm for marker in skip_markers):
                question_text = []
                options = {}
                last_option = ""
                current_number = None
                continue
            if re.match(r"^\d{4}-ayt", norm) and not re.search(r"ayt\\s*\\d", norm):
                continue
            for key, label in subject_keywords.items():
                if key in norm and len(norm) <= 20:
                    current_subject = label
                    break
            m_q = re.match(r"^(\d+)[\.\)]\s*(.+)$", line)
            if m_q:
                number = int(m_q.group(1))
                if number <= 0:
                    continue
                flush_question()
                question_text = [m_q.group(2).strip()]
                current_number = number
                options = {}
                last_option = ""
                continue
            m_opt = re.match(r"^([A-E])[\)\.\-]\s*(.+)$", line)
            if m_opt:
                last_option = m_opt.group(1)
                options[last_option] = m_opt.group(2).strip()
                continue
            if options and last_option:
                if any(marker in norm for marker in skip_markers):
                    question_text = []
                    options = {}
                    last_option = ""
                    current_number = None
                    continue
                options[last_option] = f"{options[last_option]} {line}".strip()
            else:
                question_text.append(line)

    flush_question()
    return questions


def _ayt_subject_patterns() -> list[tuple[str, str]]:
    patterns = [
        ("turk dili ve edebiyati", "Turk Dili ve Edebiyati"),
        ("turk dili", "Turk Dili ve Edebiyati"),
        ("edebiyat", "Turk Dili ve Edebiyati"),
        ("tarih-1", "Tarih-1"),
        ("tarih 1", "Tarih-1"),
        ("tarih-2", "Tarih-2"),
        ("tarih 2", "Tarih-2"),
        ("cografya-1", "Cografya-1"),
        ("cografya 1", "Cografya-1"),
        ("cografya-2", "Cografya-2"),
        ("cografya 2", "Cografya-2"),
        ("cografya", "Cografya"),
        ("tarih", "Tarih"),
        ("matematik", "Matematik"),
        ("fizik", "Fizik"),
        ("kimya", "Kimya"),
        ("biyoloji", "Biyoloji"),
        ("felsefe", "Felsefe"),
        ("mantik", "Mantik"),
        ("psikoloji", "Psikoloji"),
        ("sosyoloji", "Sosyoloji"),
        ("din kulturu", "Din Kulturu ve Ahlak Bilgisi"),
        ("dkab", "Din Kulturu ve Ahlak Bilgisi"),
    ]
    patterns.sort(key=lambda item: len(item[0]), reverse=True)
    return patterns


def _detect_ayt_subject(line: str) -> str | None:
    norm = normalize_subject_label(line)
    if not norm:
        return None
    if "?" in norm:
        norm = norm.replace("?", "i")
    if re.match(r"^\d{1,3}\b", norm):
        return None
    header_like = (
        len(norm) <= 25
        or "ayt" in norm
        or "testi" in norm
        or "sorular" in norm
        or "alan" in norm
        or "cevap" in norm
        or "anahtar" in norm
    )
    if not header_like:
        return None
    for pattern, label in _ayt_subject_patterns():
        if pattern in norm:
            if is_excluded_subject(label):
                return None
            return label
    return None


def parse_ayt_pdf_answers(pdf_path: str) -> dict[str, dict[int, str]]:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        return {}

    reader = PdfReader(pdf_path)
    answers: dict[str, dict[int, str]] = {}
    current_subject = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        norm_page = normalize_subject_label(page_text)
        if "cevap anahtari" not in norm_page:
            continue
        lines = [line.strip() for line in page_text.splitlines() if line.strip()]
        for line in lines:
            subject = _detect_ayt_subject(line)
            if subject:
                current_subject = subject
            for number, letter in re.findall(r"(\d{1,3})\s*\.?\s*([A-E])", line):
                if not current_subject:
                    continue
                answers.setdefault(current_subject, {})[int(number)] = letter

    return answers


def parse_ayt_pdf_questions(pdf_path: str, track_label: str) -> list[dict]:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        return []

    reader = PdfReader(pdf_path)
    questions: list[dict] = []
    current_subject = ""
    answers_map = parse_ayt_pdf_answers(pdf_path)
    allowed_subjects = {
        "SAY": {"Matematik", "Fizik", "Kimya", "Biyoloji"},
        "EA": {"Matematik", "Turk Dili ve Edebiyati", "Tarih-1", "Cografya-1"},
        "SOZ": {
            "Turk Dili ve Edebiyati",
            "Tarih-1",
            "Cografya-1",
            "Tarih-2",
            "Cografya-2",
            "Felsefe",
            "Mantik",
        },
    }
    allowed = allowed_subjects.get(track_label.upper(), set())
    skip_markers = {
        "cevap anahtari",
        "soru dagilim tablosu",
        "ogrenme alani",
        "yks cikmis sorular",
        "ayt cikmis sorular",
        "alan yeterlilik testi",
        "icindekiler",
    }

    question_text: list[str] = []
    options: dict[str, str] = {}
    last_option = ""
    current_number: int | None = None

    def flush_question() -> None:
        nonlocal question_text, options, last_option, current_number
        if len(options) < 4:
            question_text = []
            options = {}
            last_option = ""
            current_number = None
            return
        ordered = [options.get("A", ""), options.get("B", ""), options.get("C", ""), options.get("D", "")]
        if "E" in options:
            ordered.append(options.get("E", ""))
        ordered = [opt for opt in ordered if opt]
        joined_text = " ".join(question_text).strip()
        norm_joined = normalize_subject_label(joined_text)
        if any(marker in norm_joined for marker in skip_markers):
            question_text = []
            options = {}
            last_option = ""
            current_number = None
            return
        subject_label = current_subject or f"AYT-{track_label}"
        if allowed and subject_label not in allowed:
            question_text = []
            options = {}
            last_option = ""
            current_number = None
            return
        if is_excluded_subject(subject_label):
            question_text = []
            options = {}
            last_option = ""
            current_number = None
            return
        qtype = "Çoktan Secmeli (ABCDE)" if len(ordered) >= 5 else "Çoktan Secmeli (ABCD)"
        qid = f"ayt-{track_label.lower()}-{len(questions)+1}"
        answer = ""
        if current_number is not None:
            answer = answers_map.get(subject_label, {}).get(current_number, "")
        questions.append(
            {
                "id": qid,
                "grade": 12,
                "subject": subject_label,
                "question_type": qtype,
                "difficulty": "medium",
                "text": joined_text,
                "options": ordered,
                "answer": answer,
                "source_number": current_number,
                "source": f"pdf_import_ayt_{track_label.lower()}",
                "source_pdf": pdf_path,
                "source_page": current_page_number,
                "outcome_ids": [],
                "outcomes": [],
            }
        )
        question_text = []
        options = {}
        last_option = ""
        current_number = None

    def extract_inline_options(line: str) -> dict[str, str]:
        if "A)" not in line and "B)" not in line:
            return {}
        matches = list(re.finditer(r"([A-E])\)\s*", line))
        if len(matches) < 2:
            return {}
        extracted: dict[str, str] = {}
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
            text = line[start:end].strip()
            if text:
                extracted[match.group(1)] = text
        return extracted

    for page in reader.pages:
        text = page.extract_text() or ""
        if not text:
            continue
        norm_text = normalize_subject_label(text)
        if "cevap anahtari" in norm_text:
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            norm = normalize_subject_label(line)
            if any(marker in norm for marker in skip_markers):
                question_text = []
                options = {}
                last_option = ""
                current_number = None
                continue
            subject = _detect_ayt_subject(line)
            if subject:
                if not allowed or subject in allowed:
                    current_subject = subject
                continue
            m_q = re.match(r"^(\d{1,3})[.)]\s*(.*)$", line)
            if not m_q:
                m_q_any = re.search(r"(?:SAY|EA|S[ÖO]Z|AYT)\s*(\d{1,3})[.)]\s*(.*)", line, flags=re.IGNORECASE)
                if not m_q_any:
                    m_q_any = re.search(r"(?:SAY|EA|S[ÖO]Z|AYT)\s*(\d{1,3})\s+(.+)", line, flags=re.IGNORECASE)
                if m_q_any:
                    m_q = m_q_any
            if m_q:
                flush_question()
                text_part = m_q.group(2).strip()
                question_text = [text_part] if text_part else []
                current_number = int(m_q.group(1))
                options = {}
                last_option = ""
                continue
            inline_options = extract_inline_options(line)
            if inline_options:
                options.update(inline_options)
                last_option = sorted(inline_options.keys())[-1]
                continue
            m_opt = re.match(r"^([A-E])[)\.\-]\s*(.+)$", line)
            if m_opt:
                last_option = m_opt.group(1)
                options[last_option] = m_opt.group(2).strip()
                continue
            if options and last_option:
                if any(marker in norm for marker in skip_markers):
                    question_text = []
                    options = {}
                    last_option = ""
                    current_number = None
                    continue
                options[last_option] = f"{options[last_option]} {line}".strip()
            else:
                question_text.append(line)

    flush_question()
    return questions


def import_generation_plan_from_csv(path: str) -> list[dict]:
    df = read_csv_with_fallback(path)
    plan = []
    for _, row in df.iterrows():
        grade = int(row.get("grade", 0) or 0)
        subject = str(row.get("course", "")).strip()
        outcome_text = str(row.get("outcome_text", "")).strip()
        outcome_uid = str(row.get("outcome_uid", "")).strip()
        if not grade or not subject or not outcome_text:
            continue
        plan.append(
            {
                "grade": grade,
                "subject": subject,
                "outcome_uid": outcome_uid,
                "outcome_text": outcome_text,
                "mcq": int(row.get("mcq_count", 0) or 0),
                "tf": int(row.get("true_false_count", 0) or 0),
                "blank": int(row.get("fill_blank_count", 0) or 0),
                "open": int(row.get("open_ended_count", 0) or 0),
                "classic": int(row.get("classic_count", 0) or 0),
            }
        )
    return plan


def find_generation_plan_csv(tenant_name: str) -> str | None:
    base = os.getcwd()
    key = tenant_key(tenant_name)
    for name in os.listdir(base):
        lower_name = name.lower()
        is_lse = any(token in lower_name for token in ["lse-100", "lse_100", "lise 100", "lise-100", "lise_100"])
        is_gen01 = "gen-01" in lower_name or "gen_01" in lower_name
        if is_lse:
            candidate = os.path.join(
                base,
                name,
                "02_Import",
                "data",
                "tenants",
                key,
                "question_generation",
                "Lise_9-12_HerOutcome_100Soru_UretimPlani.csv",
            )
            if os.path.exists(candidate):
                return candidate
        if is_gen01:
            candidate = os.path.join(
                base,
                name,
                "02_Import",
                "example_data",
                "tenants",
                key,
                "question_generation",
                "Lise_9-12_HerOutcome_100Soru_UretimPlani.csv",
            )
            if os.path.exists(candidate):
                return candidate
    return None


def find_import_csvs_for_tenant(tenant_name: str) -> list[str]:
    base = os.getcwd()
    key = tenant_key(tenant_name)
    csvs: list[str] = []
    for name in os.listdir(base):
        if "SORU-YUKLE" not in name:
            continue
        if key not in name:
            continue
        tenant_dir = os.path.join(base, name, "02_Import", "data", "tenants", key)
        if not os.path.isdir(tenant_dir):
            continue
        for filename in os.listdir(tenant_dir):
            if filename.lower().endswith(".csv"):
                csvs.append(os.path.join(tenant_dir, filename))
    csvs.sort(key=lambda path: (os.path.basename(path).lower() != "questions.csv", os.path.basename(path).lower()))
    return csvs


def find_gen01_output_csvs(tenant_name: str) -> list[str]:
    base = os.getcwd()
    key = tenant_key(tenant_name)
    candidate_dir = os.path.join(base, "data", "tenants", key, "imports", "GEN-01")
    csvs: list[str] = []
    if os.path.isdir(candidate_dir):
        for name in os.listdir(candidate_dir):
            if name.lower().endswith(".csv"):
                csvs.append(os.path.join(candidate_dir, name))
    csvs.sort()
    return csvs


def find_import_csv_for_tenant(tenant_name: str) -> str | None:
    csvs = find_import_csvs_for_tenant(tenant_name)
    return csvs[0] if csvs else None


def create_chart_image(title: str, labels: list[str], values: list[int]) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        width, height, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        ax.bar(labels, values, color="#4C72B0")
        ax.set_title(title)
        ax.set_ylabel("Deger")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_triangle_image(sides: tuple[int, int, int]) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon

        width, height, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        tri = [(0, 0), (3, 0), (1.2, 2.2)]
        polygon = Polygon(tri, closed=True, fill=None, edgecolor="#2E6F9E", linewidth=2)
        ax.add_patch(polygon)
        ax.text(1.5, -0.2, str(sides[0]), ha="center", va="top", fontsize=9)
        ax.text(2.4, 1.1, str(sides[1]), ha="left", va="center", fontsize=9)
        ax.text(0.4, 1.1, str(sides[2]), ha="right", va="center", fontsize=9)
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.6, 2.8)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_rectangle_image(width: int, height: int) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        rect = Rectangle((0.4, 0.3), 2.6, 1.6, fill=None, edgecolor="#2E6F9E", linewidth=2)
        ax.add_patch(rect)
        ax.text(1.7, 0.1, str(width), ha="center", va="top", fontsize=9)
        ax.text(3.1, 1.1, str(height), ha="left", va="center", fontsize=9)
        ax.set_xlim(0, 3.4)
        ax.set_ylim(0, 2.2)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_circle_image(radius: int) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle

        fig_w, fig_h, dpi = graph_render_settings()
        size = min(fig_w, fig_h)
        fig, ax = plt.subplots(figsize=(size, size), dpi=dpi)
        circ = Circle((0, 0), radius=1.0, fill=None, edgecolor="#2E6F9E", linewidth=2)
        ax.add_patch(circ)
        ax.text(0, -1.2, f"r = {radius}", ha="center", va="top", fontsize=9)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_cell_diagram_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle

        fig_w, fig_h, dpi = graph_render_settings()
        size = min(fig_w, fig_h)
        fig, ax = plt.subplots(figsize=(size, size), dpi=dpi)
        cell = Circle((0, 0), radius=1.0, fill=False, edgecolor="#2E6F9E", linewidth=2)
        nucleus = Circle((0.2, 0.1), radius=0.35, fill=False, edgecolor="#C44E52", linewidth=2)
        ax.add_patch(cell)
        ax.add_patch(nucleus)
        ax.text(-0.9, 0.9, "Huc. zari", fontsize=8)
        ax.text(0.35, 0.25, "Cekirdek", fontsize=8)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_parabola_plot_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        xs = [x / 2 for x in range(-6, 7)]
        ys = [x * x / 4 for x in xs]
        ax.plot(xs, ys, color="#2E6F9E")
        ax.axhline(0, color="#999", linewidth=0.5)
        ax.axvline(0, color="#999", linewidth=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_inequality_shade_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        xs = [x / 2 for x in range(-6, 7)]
        ys = [x + 1 for x in xs]
        ax.plot(xs, ys, color="#2E6F9E")
        ax.fill_between(xs, ys, [max(ys) + 2] * len(xs), color="#9CC3D5", alpha=0.5)
        ax.set_xlim(-4, 4)
        ax.set_ylim(-2, 6)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_box_diagram(labels: list[str], title: str | None = None) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.axis("off")
        positions = [(0.5, 2.6), (2.3, 2.6), (0.5, 0.8), (2.3, 0.8)]
        for (x, y), label in zip(positions, labels):
            rect = Rectangle((x, y), 1.2, 0.8, fill=False, edgecolor="#2E6F9E", linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x + 0.6, y + 0.4, label, ha="center", va="center", fontsize=8)
        if title:
            ax.text(2, 3.7, title, ha="center", va="top", fontsize=9)
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_freebody_diagram_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        rect = Rectangle((1.2, 1.2), 1.6, 1.0, fill=False, edgecolor="#2E6F9E", linewidth=2)
        ax.add_patch(rect)
        ax.arrow(2, 2.2, 0, 0.8, head_width=0.1, head_length=0.15, color="#C44E52")
        ax.arrow(2, 1.2, 0, -0.8, head_width=0.1, head_length=0.15, color="#C44E52")
        ax.arrow(1.2, 1.7, -0.8, 0, head_width=0.1, head_length=0.15, color="#C44E52")
        ax.arrow(2.8, 1.7, 0.8, 0, head_width=0.1, head_length=0.15, color="#C44E52")
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_circuit_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.plot([0.5, 3.5], [2.5, 2.5], color="#2E6F9E", linewidth=2)
        ax.plot([0.5, 0.5], [2.5, 1.0], color="#2E6F9E", linewidth=2)
        ax.plot([3.5, 3.5], [2.5, 1.0], color="#2E6F9E", linewidth=2)
        ax.plot([0.5, 3.5], [1.0, 1.0], color="#2E6F9E", linewidth=2)
        ax.plot([1.4, 1.6], [2.5, 2.5], color="#C44E52", linewidth=2)
        ax.plot([1.7, 1.9], [2.5, 2.5], color="#C44E52", linewidth=4)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_optics_ray_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.plot([2, 2], [0.5, 3.5], color="#2E6F9E", linewidth=2)
        ax.plot([0.5, 2], [2.5, 2.0], color="#C44E52", linewidth=2)
        ax.plot([0.5, 2], [1.5, 2.0], color="#C44E52", linewidth=2)
        ax.plot([2, 3.5], [2.0, 2.8], color="#C44E52", linewidth=2)
        ax.plot([2, 3.5], [2.0, 1.2], color="#C44E52", linewidth=2)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_field_lines_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        for angle in range(0, 360, 45):
            x = 2 + 1.2 * math.cos(math.radians(angle))
            y = 2 + 1.2 * math.sin(math.radians(angle))
            ax.arrow(2, 2, x - 2, y - 2, head_width=0.08, head_length=0.12, color="#2E6F9E")
        ax.scatter([2], [2], color="#C44E52", s=30)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_lewis_molecule_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.text(1, 2, "H", fontsize=10)
        ax.text(2, 2, "O", fontsize=10)
        ax.text(3, 2, "H", fontsize=10)
        ax.plot([1.2, 1.9], [2, 2], color="#2E6F9E", linewidth=2)
        ax.plot([2.1, 2.8], [2, 2], color="#2E6F9E", linewidth=2)
        ax.scatter([2, 2], [2.3, 1.7], color="#C44E52", s=10)
        ax.set_xlim(0.5, 3.5)
        ax.set_ylim(1.2, 2.8)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_energy_profile_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        xs = [0, 1, 2, 3, 4]
        ys = [1, 2.5, 3.2, 2.0, 1.2]
        ax.plot(xs, ys, color="#2E6F9E", linewidth=2)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_ph_scale_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.barh([0], [14], color="#9CC3D5", height=0.6)
        ax.text(0.5, 0, "0", va="center", fontsize=8)
        ax.text(13.2, 0, "14", va="center", fontsize=8)
        ax.text(7, 0.2, "pH", ha="center", fontsize=9)
        ax.set_xlim(0, 14)
        ax.set_ylim(-0.5, 0.8)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_punnett_square_image() -> bytes | None:
    headers = ["", "A", "a"]
    rows = [
        ["A", "AA", "Aa"],
        ["a", "Aa", "aa"],
    ]
    return create_table_image(headers, rows)


def create_division_flow_image() -> bytes | None:
    return create_box_diagram(["G1", "S", "G2", "M"], title="Mitoz/Mayoz")


def create_food_web_image() -> bytes | None:
    return create_box_diagram(["Bitki", "Otcul", "Etcil", "Ayris"], title="Besin Ağı")


def create_contour_section_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        xs = [0, 1, 2, 3, 4]
        ys = [1.2, 2.2, 1.8, 2.6, 1.4]
        ax.plot(xs, ys, color="#2E6F9E", linewidth=2)
        ax.fill_between(xs, ys, 0.8, color="#9CC3D5", alpha=0.4)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_climograph_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax1 = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        months = ["O", "S", "M", "N"]
        temps = [10, 12, 8, 6]
        rain = [40, 60, 50, 30]
        ax1.bar(months, rain, color="#9CC3D5")
        ax2 = ax1.twinx()
        ax2.plot(months, temps, color="#C44E52", marker="o")
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax2.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_population_pyramid_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        groups = ["0-14", "15-64", "65+"]
        male = [-20, -40, -10]
        female = [18, 35, 12]
        ax.barh(groups, male, color="#9CC3D5")
        ax.barh(groups, female, color="#C44E52")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_timeline_image() -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.plot([0, 4], [2, 2], color="#2E6F9E", linewidth=2)
        for idx, label in enumerate(["I", "II", "III", "IV"]):
            ax.scatter([idx + 0.5], [2], color="#C44E52", s=20)
            ax.text(idx + 0.5, 2.3, label, ha="center", fontsize=8)
        ax.set_xlim(0, 4.5)
        ax.set_ylim(1.5, 3)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_cause_effect_table_image() -> bytes | None:
    headers = ["Sebep", "Sonuc"]
    rows = [
        ["A", "B"],
        ["C", "D"],
    ]
    return create_table_image(headers, rows)


def create_concept_map_image() -> bytes | None:
    return create_box_diagram(["Kavram 1", "Kavram 2", "Kavram 3", "Kavram 4"], title="Kavram Haritasi")


def create_argument_map_image() -> bytes | None:
    return create_box_diagram(["Oncul 1", "Oncul 2", "Sonuc", "Destek"], title="Arguman Haritasi")


def create_map_image(points: dict[str, tuple[int, int]]) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 6)
        ax.axhline(0, color="#999", linewidth=0.5)
        ax.axvline(0, color="#999", linewidth=0.5)
        ax.text(0.1, -0.5, "Merkez", fontsize=8)
        for label, (x, y) in points.items():
            ax.scatter([x], [y], color="#3B7EA1")
            ax.text(x + 0.1, y + 0.1, label, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(True)
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_line_chart_image(labels: list[str], values: list[int], title: str) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.plot(labels, values, marker="o", color="#2E6F9E")
        ax.set_title(title)
        ax.set_ylabel("Deger")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_pie_chart_image(labels: list[str], values: list[int], title: str) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.pie(values, labels=labels, autopct="%1.0f%%")
        ax.set_title(title)
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_histogram_image(values: list[int], title: str) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.hist(values, bins=5, color="#4C72B0", edgecolor="#2E6F9E")
        ax.set_title(title)
        ax.set_ylabel("Frekans")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_angle_image(angle_deg: int) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import math

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.plot([0, 3], [0, 0], color="#2E6F9E", linewidth=2)
        rad = math.radians(angle_deg)
        ax.plot([0, 3 * math.cos(rad)], [0, 3 * math.sin(rad)], color="#2E6F9E", linewidth=2)
        ax.text(0.4, 0.2, f"{angle_deg}°", fontsize=10)
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 3.0)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_venn_image(a_only: int, b_only: int, inter: int) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        left = Circle((1.2, 1.2), 0.9, fill=False, edgecolor="#2E6F9E", linewidth=2)
        right = Circle((2.2, 1.2), 0.9, fill=False, edgecolor="#2E6F9E", linewidth=2)
        ax.add_patch(left)
        ax.add_patch(right)
        ax.text(0.8, 1.2, str(a_only), ha="center", va="center", fontsize=10)
        ax.text(2.6, 1.2, str(b_only), ha="center", va="center", fontsize=10)
        ax.text(1.7, 1.2, str(inter), ha="center", va="center", fontsize=10)
        ax.set_xlim(0, 3.2)
        ax.set_ylim(0.2, 2.2)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_function_plot_image(a: int, b: int) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 200)
        y = a * x + b
        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.plot(x, y, color="#2E6F9E")
        ax.axhline(0, color="#999", linewidth=0.6)
        ax.axvline(0, color="#999", linewidth=0.6)
        ax.set_xlim(-3, 3)
        ax.set_ylim(min(y) - 1, max(y) + 1)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_table_image(headers: list[str], rows: list[list[str]]) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        ax.axis("off")
        table = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2)
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_prism_image(length: int, width: int, height: int) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        fig_w, fig_h, dpi = graph_render_settings()
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        front = Rectangle((0.5, 0.6), 2.0, 1.2, fill=None, edgecolor="#2E6F9E", linewidth=2)
        top = Rectangle((1.0, 1.2), 2.0, 1.0, fill=None, edgecolor="#2E6F9E", linewidth=2)
        side = Rectangle((2.5, 0.6), 1.0, 1.2, fill=None, edgecolor="#2E6F9E", linewidth=2)
        ax.add_patch(front)
        ax.add_patch(top)
        ax.add_patch(side)
        ax.text(1.5, 0.4, str(length), ha="center", va="top", fontsize=9)
        ax.text(3.6, 1.2, str(width), ha="left", va="center", fontsize=9)
        ax.text(0.3, 1.2, str(height), ha="right", va="center", fontsize=9)
        ax.set_xlim(0, 4.2)
        ax.set_ylim(0, 2.4)
        ax.axis("off")
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def create_coordinate_image(points: dict[str, tuple[int, int]]) -> bytes | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(3.6, 2.6), dpi=120)
        ax.axhline(0, color="#999", linewidth=0.6)
        ax.axvline(0, color="#999", linewidth=0.6)
        ax.set_xlim(-5, 6)
        ax.set_ylim(-5, 6)
        for label, (x, y) in points.items():
            ax.scatter([x], [y], color="#3B7EA1")
            ax.text(x + 0.2, y + 0.2, label, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(True)
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


def build_graph_question(subject: str) -> dict:
    category = subject_category(subject)
    if category == "math":
        pick = random.choice(["triangle", "rectangle", "circle", "coordinate", "prism", "angle", "function", "venn", "table"])
        if pick == "triangle":
            side = random.randint(4, 9)
            alt = random.randint(5, 9)
            sides = (side, side, alt)
            image_bytes = create_triangle_image(sides)
            if sides[0] == sides[1] == sides[2]:
                answer = "Eskenar"
            elif sides[0] == sides[1] or sides[1] == sides[2] or sides[0] == sides[2]:
                answer = "Ikizkenar"
            else:
                answer = "Cesitkenar"
            options = ["Eskenar", "Ikizkenar", "Cesitkenar", "Dik ucgen"]
            question = "Sekilde verilen ucgenin kenar uzunluklarina gore turu hangisidir?"
            return {
                "text": question,
                "options": options,
                "answer": answer,
                "image_bytes": image_bytes,
            }
        if pick == "rectangle":
            width = random.randint(4, 9)
            height = random.randint(3, 7)
            image_bytes = create_rectangle_image(width, height)
            area = width * height
            options = [str(area - height), str(area), str(area + width), str(area + height)]
            answer = "B"
            question = "Sekilde verilen dikdortgenin alani kactir?"
            return {
                "text": question,
                "options": options,
                "answer": answer,
                "image_bytes": image_bytes,
            }
        if pick == "circle":
            radius = random.randint(3, 7)
            image_bytes = create_circle_image(radius)
            answer = f"{2 * radius}π"
            options = [f"{radius}π", f"{2 * radius}π", f"{3 * radius}π", f"{4 * radius}π"]
            question = "Sekilde verilen dairenin cevresi kactir? (π ile)"
            return {
                "text": question,
                "options": options,
                "answer": "B",
                "image_bytes": image_bytes,
            }
        if pick == "prism":
            length = random.randint(4, 9)
            width = random.randint(3, 7)
            height = random.randint(2, 6)
            image_bytes = create_prism_image(length, width, height)
            volume = length * width * height
            options = [str(volume - width), str(volume), str(volume + length), str(volume + height)]
            question = "Sekilde verilen dikdortgen prizmanin hacmi kactir?"
            return {
                "text": question,
                "options": options,
                "answer": "B",
                "image_bytes": image_bytes,
            }
        if pick == "angle":
            angle = random.choice([30, 45, 60, 90, 120])
            image_bytes = create_angle_image(angle)
            options = [str(angle - 15), str(angle), str(angle + 15), str(angle + 30)]
            question = "Sekilde gosterilen acinin olcusu kactir?"
            return {
                "text": question,
                "options": options,
                "answer": "B",
                "image_bytes": image_bytes,
            }
        if pick == "function":
            a = random.choice([1, 2, -1])
            b = random.randint(-2, 2)
            image_bytes = create_function_plot_image(a, b)
            options = [str(b - 1), str(b), str(b + 1), str(b + 2)]
            question = "Grafikteki dogrunun y-ekseni kesisimi kactir?"
            return {
                "text": question,
                "options": options,
                "answer": "B",
                "image_bytes": image_bytes,
            }
        if pick == "venn":
            a_only = random.randint(3, 9)
            b_only = random.randint(3, 9)
            inter = random.randint(1, 6)
            image_bytes = create_venn_image(a_only, b_only, inter)
            options = [str(inter - 1), str(inter), str(inter + 1), str(inter + 2)]
            question = "Venn diyagraminda kesisim bolgesindeki eleman sayisi kactir?"
            return {
                "text": question,
                "options": options,
                "answer": "B",
                "image_bytes": image_bytes,
            }
        if pick == "table":
            headers = ["Gün", "Sicaklik"]
            rows = [
                ["Pzt", str(random.randint(10, 20))],
                ["Sal", str(random.randint(10, 20))],
                ["Car", str(random.randint(10, 20))],
                ["Per", str(random.randint(10, 20))],
            ]
            image_bytes = create_table_image(headers, rows)
            max_day = max(rows, key=lambda r: int(r[1]))[0]
            options = [r[0] for r in rows]
            question = "Tabloya gore en yuksek sicaklik hangi gundedir?"
            return {
                "text": question,
                "options": options,
                "answer": max_day,
                "image_bytes": image_bytes,
            }
        points = {
            "A": (random.randint(-4, 4), random.randint(-4, 4)),
            "B": (random.randint(-4, 4), random.randint(-4, 4)),
            "C": (random.randint(-4, 4), random.randint(-4, 4)),
            "D": (random.randint(-4, 4), random.randint(-4, 4)),
        }
        distances = {k: abs(v[0]) + abs(v[1]) for k, v in points.items()}
        closest = min(distances, key=distances.get)
        image_bytes = create_coordinate_image(points)
        question = "Koordinat duzleminde orjine en yakin nokta hangisidir?"
        return {
            "text": question,
            "options": ["A", "B", "C", "D"],
            "answer": closest,
            "image_bytes": image_bytes,
        }

    if category == "geo":
        pick = random.choice(["map", "line", "pie"])
        if pick == "map":
            points = {
                "A": (random.randint(1, 5), random.randint(1, 5)),
                "B": (random.randint(1, 5), random.randint(1, 5)),
                "C": (random.randint(1, 5), random.randint(1, 5)),
                "D": (random.randint(1, 5), random.randint(1, 5)),
            }
            distances = {k: (v[0] ** 2 + v[1] ** 2) for k, v in points.items()}
            closest = min(distances, key=distances.get)
            image_bytes = create_map_image(points)
            question = "Haritadaki noktalardan hangisi merkeze en yakindir?"
            options = ["A", "B", "C", "D"]
            return {
                "text": question,
                "options": options,
                "answer": closest,
                "image_bytes": image_bytes,
            }
        if pick == "pie":
            labels = ["A", "B", "C", "D"]
            values = [random.randint(10, 40) for _ in labels]
            image_bytes = create_pie_chart_image(labels, values, f"{subject} dagilimi")
            max_value = max(values)
            correct = labels[values.index(max_value)]
            question = "Pasta grafikte en buyuk pay hangi kategoridedir?"
            options = labels
            return {
                "text": question,
                "options": options,
                "answer": correct,
                "image_bytes": image_bytes,
            }
        labels = ["Pzt", "Sal", "Car", "Per"]
        values = [random.randint(10, 40) for _ in labels]
        image_bytes = create_line_chart_image(labels, values, f"{subject} sicaklik degisimi")
        max_value = max(values)
        correct = labels[values.index(max_value)]
        question = "Cizgi grafikte en yuksek deger hangi gunde gorulmektedir?"
        options = labels
        return {
            "text": question,
            "options": options,
            "answer": correct,
            "image_bytes": image_bytes,
        }

    if category == "physics":
        pick = random.choice(["line", "hist"])
        if pick == "hist":
            values = [random.randint(1, 20) for _ in range(20)]
            image_bytes = create_histogram_image(values, "Olcum Dagilimi")
            bins = [0, 5, 10, 15, 20]
            counts = [0, 0, 0, 0]
            for val in values:
                if val <= 5:
                    counts[0] += 1
                elif val <= 10:
                    counts[1] += 1
                elif val <= 15:
                    counts[2] += 1
                else:
                    counts[3] += 1
            max_idx = counts.index(max(counts))
            options = ["0-5", "6-10", "11-15", "16-20"]
            answer = ["A", "B", "C", "D"][max_idx]
            question = "Histogramda verilerin en yogun oldugu aralik hangisidir?"
            return {
                "text": question,
                "options": options,
                "answer": answer,
                "image_bytes": image_bytes,
            }
        labels = ["t1", "t2", "t3", "t4"]
        values = [random.randint(2, 9) for _ in labels]
        image_bytes = create_line_chart_image(labels, values, "Hiz-Zaman Grafigi")
        max_value = max(values)
        correct = labels[values.index(max_value)]
        question = "Hiz-zaman grafiiginde en yuksek hiz hangi anda gorulur?"
        options = labels
        return {
            "text": question,
            "options": options,
            "answer": correct,
            "image_bytes": image_bytes,
        }

    if category == "bio":
        labels = ["Bitki", "Hayvan", "Mantar", "Bakteri"]
    elif category == "chem":
        labels = ["Cozelti 1", "Cozelti 2", "Cozelti 3", "Cozelti 4"]
    elif category == "history":
        labels = ["I. Donem", "II. Donem", "III. Donem", "IV. Donem"]
    else:
        labels = ["Grup 1", "Grup 2", "Grup 3", "Grup 4"]
    values = [random.randint(10, 40) for _ in labels]
    title = f"{subject} veri grafigi"
    image_bytes = create_chart_image(title, labels, values)
    variants = []
    max_value = max(values)
    min_value = min(values)
    max_label = labels[values.index(max_value)]
    min_label = labels[values.index(min_value)]
    variants.append(
        {
            "q": "Asagidaki sutun grafiiginde en yuksek deger hangi grupta gorulur?",
            "options": labels,
            "answer": max_label,
        }
    )
    variants.append(
        {
            "q": "Asagidaki sutun grafiiginde en dusuk deger hangi grupta gorulur?",
            "options": labels,
            "answer": min_label,
        }
    )
    diff = max_value - min_value
    variants.append(
        {
            "q": "Grafikte en yuksek deger ile en dusuk deger arasindaki fark kactir?",
            "options": [str(diff - 2), str(diff), str(diff + 2), str(diff + 4)],
            "answer": "B",
        }
    )
    pair_idx = random.sample(range(len(labels)), 2)
    pair_sum = values[pair_idx[0]] + values[pair_idx[1]]
    variants.append(
        {
            "q": f"{labels[pair_idx[0]]} ile {labels[pair_idx[1]]} toplam degeri kactir?",
            "options": [str(pair_sum - 3), str(pair_sum), str(pair_sum + 3), str(pair_sum + 6)],
            "answer": "B",
        }
    )
    pick = random.choice(variants)
    return {
        "text": pick["q"],
        "options": pick["options"],
        "answer": pick["answer"],
        "image_bytes": image_bytes,
    }


def build_visual_from_hint(subject: str, hint: str) -> bytes | None:
    hint_norm = normalize_subject_label(hint)
    if not hint_norm or "yok" in hint_norm:
        return None
    if "harita" in hint_norm:
        points = {label: (random.randint(1, 5), random.randint(1, 5)) for label in ["A", "B", "C", "D"]}
        return create_map_image(points)
    if "pasta" in hint_norm:
        labels = ["A", "B", "C", "D"]
        values = [random.randint(10, 40) for _ in labels]
        return create_pie_chart_image(labels, values, f"{subject} dagilimi")
    if "cizgi" in hint_norm or "line" in hint_norm:
        labels = ["Pzt", "Sal", "Car", "Per"]
        values = [random.randint(10, 40) for _ in labels]
        return create_line_chart_image(labels, values, f"{subject} degisimi")
    if "hist" in hint_norm:
        values = [random.randint(1, 20) for _ in range(20)]
        return create_histogram_image(values, "Olcum Dagilimi")
    if "hiz" in hint_norm:
        labels = ["t1", "t2", "t3", "t4"]
        values = [random.randint(2, 9) for _ in labels]
        return create_line_chart_image(labels, values, "Hiz-Zaman Grafigi")
    if "grafik" in hint_norm:
        labels = ["Grup 1", "Grup 2", "Grup 3", "Grup 4"]
        values = [random.randint(10, 40) for _ in labels]
        return create_chart_image(f"{subject} veri grafigi", labels, values)
    if "ucgen" in hint_norm:
        side = random.randint(4, 9)
        alt = random.randint(5, 9)
        return create_triangle_image((side, side, alt))
    if "dikdortgen" in hint_norm:
        return create_rectangle_image(random.randint(4, 9), random.randint(3, 7))
    if "daire" in hint_norm:
        return create_circle_image(random.randint(3, 7))
    if "koordinat" in hint_norm:
        points = {
            "A": (random.randint(-4, 4), random.randint(-4, 4)),
            "B": (random.randint(-4, 4), random.randint(-4, 4)),
            "C": (random.randint(-4, 4), random.randint(-4, 4)),
            "D": (random.randint(-4, 4), random.randint(-4, 4)),
        }
        return create_coordinate_image(points)
    if "prizma" in hint_norm:
        return create_prism_image(random.randint(4, 9), random.randint(3, 7), random.randint(2, 6))
    if "aci" in hint_norm:
        return create_angle_image(random.choice([30, 45, 60, 90, 120]))
    if "fonksiyon" in hint_norm:
        return create_function_plot_image(random.choice([1, 2, -1]), random.randint(-2, 2))
    if "venn" in hint_norm:
        return create_venn_image(random.randint(3, 9), random.randint(3, 9), random.randint(1, 6))
    if "tablo" in hint_norm:
        headers = ["Gün", "Deger"]
        rows = [
            ["Pzt", str(random.randint(10, 20))],
            ["Sal", str(random.randint(10, 20))],
            ["Car", str(random.randint(10, 20))],
            ["Per", str(random.randint(10, 20))],
        ]
        return create_table_image(headers, rows)
    if "hucre" in hint_norm:
        return create_cell_diagram_image()
    return None


def find_gen01_template_catalog() -> str | None:
    base = os.getcwd()
    for name in os.listdir(base):
        if name.lower().startswith("gen-01"):
            config_dir = os.path.join(
                base,
                name,
                "02_Import",
                "python_generator",
                "config",
            )
            if not os.path.isdir(config_dir):
                continue
            candidates = [
                "template_catalog_lise_9_12.json",
                "template_catalog_lise_9_12_v6_7ders_60.json",
                "template_catalog_lise_9_12_v2.json",
            ]
            for filename in candidates:
                candidate = os.path.join(config_dir, filename)
                if os.path.exists(candidate):
                    return candidate
            for filename in os.listdir(config_dir):
                if filename.startswith("template_catalog_lise_9_12") and filename.lower().endswith(".json"):
                    return os.path.join(config_dir, filename)
    return None


def load_template_catalog() -> dict | None:
    path = find_gen01_template_catalog()
    if (
        "template_catalog" in st.session_state
        and st.session_state.template_catalog is not None
        and st.session_state.get("template_catalog_path") == path
    ):
        return st.session_state.template_catalog
    if not path:
        st.session_state.template_catalog = None
        st.session_state.template_catalog_path = None
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            catalog = json.load(handle)
    except Exception:
        try:
            with open(path, "r", encoding="cp1254") as handle:
                catalog = json.load(handle)
        except Exception:
            with open(path, "r", encoding="latin-1") as handle:
                catalog = json.load(handle)
    st.session_state.template_catalog = catalog
    st.session_state.template_catalog_path = path
    return catalog


def normalize_regex_pattern(pattern: str) -> str:
    return normalize_subject_label(pattern)


def select_template_from_catalog(subject: str, outcome_text: str) -> str | None:
    catalog = load_template_catalog()
    if not catalog:
        return None
    courses = catalog.get("courses", {})
    subject_key = normalize_subject_label(display_subject_label(subject))
    norm_text = normalize_subject_label(outcome_text)
    if "matematik" in subject_key and "aci" in norm_text:
        return "GEOM_ANGLE"
    matched_course = None
    for name, data in courses.items():
        if normalize_subject_label(name) == subject_key:
            matched_course = data
            break
    if not matched_course:
        for name, data in courses.items():
            if subject_key in normalize_subject_label(name):
                matched_course = data
                break
    if not matched_course:
        return None

    rules = matched_course.get("rules", [])
    for rule in rules:
        pattern = rule.get("regex", "")
        if not pattern:
            continue
        try:
            if re.search(pattern, outcome_text, re.IGNORECASE):
                return rule.get("template")
        except Exception:
            pass
        norm_pattern = normalize_regex_pattern(pattern)
        try:
            if re.search(norm_pattern, norm_text, re.IGNORECASE):
                return rule.get("template")
        except Exception:
            continue
    return matched_course.get("default")


def build_visual_from_template(template_id: str | None, subject: str) -> bytes | None:
    if not template_id:
        return None
    if template_id == "READING_PASSAGE":
        return None
    mapping = {
        "COORD_LINE": lambda: create_function_plot_image(1, 0),
        "COORD_PARABOLA": create_parabola_plot_image,
        "INEQ_SHADE": create_inequality_shade_image,
        "GEOM_TRIANGLE": lambda: create_triangle_image((6, 6, 8)),
        "GEOM_CIRCLE": lambda: create_circle_image(5),
        "GEOM_RECTANGLE": lambda: create_rectangle_image(6, 4),
        "GEOM_PRISM": lambda: create_prism_image(6, 4, 3),
        "GEOM_ANGLE": lambda: create_angle_image(random.choice([30, 45, 60, 90, 120])),
        "STATS_BAR": lambda: create_chart_image(f"{subject} veri grafigi", ["A", "B", "C", "D"], [12, 18, 9, 15]),
        "STATS_LINE": lambda: create_line_chart_image(["t1", "t2", "t3", "t4"], [3, 6, 5, 7], f"{subject} degisimi"),
        "TRUTH_TABLE": lambda: create_table_image(["p", "q", "p∧q"], [["D", "D", "D"], ["D", "Y", "Y"], ["Y", "D", "Y"], ["Y", "Y", "Y"]]),
        "KINEMATICS_GRAPH": lambda: create_line_chart_image(["t1", "t2", "t3", "t4"], [2, 5, 3, 6], "Hiz-Zaman"),
        "FREEBODY_VECTOR": create_freebody_diagram_image,
        "CIRCUIT_BASIC": create_circuit_image,
        "OPTICS_RAY": create_optics_ray_image,
        "FIELD_LINES": create_field_lines_image,
        "PERIODIC_SNIPPET": lambda: create_table_image(["H", "He"], [["1", "2"]]),
        "LEWIS_MOLECULE": create_lewis_molecule_image,
        "ENERGY_PROFILE": create_energy_profile_image,
        "PH_SCALE": create_ph_scale_image,
        "CONC_TIME": lambda: create_line_chart_image(["t1", "t2", "t3", "t4"], [5, 4, 3, 2], "Derişim-Zaman"),
        "CELL_DIAGRAM": create_cell_diagram_image,
        "GENETICS_PUNNETT": create_punnett_square_image,
        "DIVISION_FLOW": create_division_flow_image,
        "FOOD_WEB": create_food_web_image,
        "POPULATION_GRAPH": lambda: create_chart_image("Populasyon", ["A", "B", "C", "D"], [20, 35, 25, 18]),
        "MAP_SCHEMATIC": lambda: create_map_image({"A": (1, 1), "B": (4, 2), "C": (2, 4), "D": (5, 5)}),
        "CONTOUR_SECTION": create_contour_section_image,
        "CLIMOGRAPH": create_climograph_image,
        "POP_PYRAMID": create_population_pyramid_image,
        "TIMELINE": create_timeline_image,
        "CAUSE_EFFECT_TABLE": create_cause_effect_table_image,
        "CONCEPT_MAP": create_concept_map_image,
        "ARGUMENT_MAP": create_argument_map_image,
    }
    if template_id in mapping:
        return mapping[template_id]()
    catalog = load_template_catalog() or {}
    templates = catalog.get("templates", {})
    kind = templates.get(template_id, {}).get("kind")
    if kind == "chart":
        return create_chart_image(f"{subject} veri grafigi", ["A", "B", "C", "D"], [10, 14, 8, 12])
    if kind == "plot":
        return create_line_chart_image(["t1", "t2", "t3", "t4"], [2, 4, 3, 5], f"{subject} grafigi")
    if kind == "table":
        return create_table_image(["A", "B"], [["1", "2"], ["3", "4"]])
    if kind == "geometry":
        return create_triangle_image((5, 6, 7))
    if kind == "diagram":
        return create_box_diagram(["A", "B", "C", "D"], title=subject)
    return None


def select_template_from_text(text: str) -> str | None:
    norm = normalize_subject_label(text)
    if "ucgen" in norm:
        return "GEOM_TRIANGLE"
    if "dikdortgen" in norm:
        return "GEOM_RECTANGLE"
    if "daire" in norm or "cember" in norm:
        return "GEOM_CIRCLE"
    if "prizma" in norm:
        return "GEOM_PRISM"
    if "aci" in norm:
        return "GEOM_ANGLE"
    if "grafik" in norm:
        return "STATS_LINE"
    if "tablo" in norm:
        return "TRUTH_TABLE"
    if "harita" in norm:
        return "MAP_SCHEMATIC"
    return None


def varied_text(question: str, outcome_text: str) -> str:
    if outcome_text:
        return f"{question} (Kazanim: {outcome_text})"
    return question


def display_question_text(question: dict) -> str:
    text = (question.get("text") or "").strip()
    if question.get("source_pdf") and question.get("image_bytes"):
        return ""
    if question.get("source_pdf"):
        text = re.sub(r"^\s*\d{1,3}[\.\)]\s*", "", text)
        text = re.sub(r"^\s*soru\s*\d{1,3}[\.\)]?\s*", "", text, flags=re.IGNORECASE)
    if not question.get("image_bytes"):
        text = re.sub(r"^\[?grafik\]?\s*", "", text, flags=re.IGNORECASE)
    return text


def _find_poppler_bin() -> str | None:
    candidates = []
    env_paths = os.environ.get("PATH", "").split(os.pathsep)
    for path in env_paths:
        if not path:
            continue
        if os.path.exists(os.path.join(path, "pdftoppm.exe")):
            return path
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        pattern = os.path.join(
            local,
            "Microsoft",
            "WinGet",
            "Packages",
            "oschwartz10612.Poppler*",
            "poppler-*",
            "Library",
            "bin",
        )
        candidates.extend(glob.glob(pattern))
    for path in candidates:
        if os.path.exists(os.path.join(path, "pdftoppm.exe")):
            return path
    return None


def _extract_pdf_words(pdf_path: str, page_number: int) -> tuple[list[dict], float, float]:
    poppler_bin = _find_poppler_bin()
    if not poppler_bin:
        return [], 0.0, 0.0
    pdftotext = os.path.join(poppler_bin, "pdftotext.exe")
    if not os.path.exists(pdftotext):
        return [], 0.0, 0.0
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "page.html")
        cmd = [
            pdftotext,
            "-bbox",
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            pdf_path,
            out_path,
        ]
        subprocess.run(cmd, check=False, capture_output=True)
        if not os.path.exists(out_path):
            return [], 0.0, 0.0
        content = ""
        with open(out_path, "r", encoding="utf-8", errors="ignore") as handle:
            content = handle.read()
    page_match = re.search(r'<page[^>]*width="([0-9\\.]+)"[^>]*height="([0-9\\.]+)"', content)
    page_width = float(page_match.group(1)) if page_match else 0.0
    page_height = float(page_match.group(2)) if page_match else 0.0
    words = []
    for match in re.finditer(
        r'<word[^>]*xMin="([0-9\\.]+)"[^>]*yMin="([0-9\\.]+)"[^>]*xMax="([0-9\\.]+)"[^>]*yMax="([0-9\\.]+)".*?>(.*?)</word>',
        content,
        flags=re.DOTALL,
    ):
        text = html.unescape(match.group(5)).strip()
        if not text:
            continue
        words.append(
            {
                "text": text,
                "xMin": float(match.group(1)),
                "yMin": float(match.group(2)),
                "xMax": float(match.group(3)),
                "yMax": float(match.group(4)),
            }
        )
    return words, page_width, page_height


def _find_question_bbox(
    words: list[dict],
    page_width: float,
    page_height: float,
    question_number: int,
) -> tuple[float, float, float, float] | None:
    if not words or not page_width:
        return None
    number_pattern = re.compile(rf"^{question_number}[\\.)]?$")
    left_threshold = page_width * 0.25
    start_index = None
    for idx, word in enumerate(words):
        if word["xMin"] > left_threshold:
            continue
        if number_pattern.match(word["text"]):
            start_index = idx
            break
    if start_index is None:
        return None
    next_index = None
    for idx in range(start_index + 1, len(words)):
        word = words[idx]
        if word["xMin"] > left_threshold:
            continue
        if re.match(r"^\\d{1,3}[\\.)]?$", word["text"]):
            next_index = idx
            break
    y_min = words[start_index]["yMin"] - 4
    if next_index is not None:
        y_max = words[next_index]["yMin"] - 2
    else:
        y_max = page_height
    y_min = max(0, y_min)
    y_max = min(page_height, y_max)
    return (0.0, y_min, page_width, y_max)


def _render_pdf_page(pdf_path: str, page_number: int, dpi: int = 150) -> bytes | None:
    poppler_bin = _find_poppler_bin()
    if not poppler_bin:
        return None
    pdftoppm = os.path.join(poppler_bin, "pdftoppm.exe")
    if not os.path.exists(pdftoppm):
        return None
    with tempfile.TemporaryDirectory() as tmpdir:
        out_prefix = os.path.join(tmpdir, "page")
        cmd = [
            pdftoppm,
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            "-r",
            str(dpi),
            "-png",
            pdf_path,
            out_prefix,
        ]
        subprocess.run(cmd, check=False, capture_output=True)
        candidates = glob.glob(f"{out_prefix}-*.png")
        if not candidates:
            return None
        image_path = candidates[0]
        with open(image_path, "rb") as handle:
            return handle.read()


def extract_question_image_from_pdf(
    pdf_path: str,
    page_number: int,
    question_number: int | None,
    dpi: int = 150,
) -> bytes | None:
    if not pdf_path or not page_number or not question_number:
        return None
    try:
        from PIL import Image
    except Exception:
        return None
    words, page_width, page_height = _extract_pdf_words(pdf_path, page_number)
    bbox = _find_question_bbox(words, page_width, page_height, int(question_number))
    if not bbox:
        return None
    page_bytes = _render_pdf_page(pdf_path, page_number, dpi=dpi)
    if not page_bytes:
        return None
    img = Image.open(io.BytesIO(page_bytes))
    scale = dpi / 72.0
    x0, y0, x1, y1 = bbox
    crop_box = (
        int(x0 * scale),
        int(y0 * scale),
        int(x1 * scale),
        int(y1 * scale),
    )
    crop_box = (
        max(0, crop_box[0]),
        max(0, crop_box[1]),
        min(img.width, crop_box[2]),
        min(img.height, crop_box[3]),
    )
    if crop_box[2] <= crop_box[0] or crop_box[3] <= crop_box[1]:
        return None
    cropped = img.crop(crop_box)
    buffer = io.BytesIO()
    cropped.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def apply_visual_policy(
    question: dict,
    subject: str,
    outcome_text: str,
    visual_hint: str | None = None,
) -> None:
    if question.get("image_bytes"):
        return

    asset_path = question.get("asset_path")
    if not asset_path:
        asset_path = resolve_asset_path(
            str(question.get("id", "")),
            question.get("alt_text"),
            st.session_state.tenant_name,
        )
    if asset_path and os.path.exists(asset_path):
        try:
            with open(asset_path, "rb") as handle:
                question["image_bytes"] = handle.read()
                question["asset_path"] = asset_path
                return
        except Exception:
            pass

    template_id = question.get("template_id") or parse_template_id_from_alt_text(
        question.get("alt_text")
    )
    if template_id:
        question["template_id"] = template_id
        image_bytes = build_visual_from_template(template_id, subject)
        if image_bytes:
            question["image_bytes"] = image_bytes
            return

    if outcome_text:
        template_id = select_template_from_catalog(subject, outcome_text)
        if template_id:
            question["template_id"] = template_id
            image_bytes = build_visual_from_template(template_id, subject)
            if image_bytes:
                question["image_bytes"] = image_bytes
                return

    if visual_hint:
        hint_norm = normalize_subject_label(visual_hint)
        if "yok" not in hint_norm:
            image_bytes = build_visual_from_hint(subject, visual_hint)
            if image_bytes:
                question["image_bytes"] = image_bytes
                return

    template_id = select_template_from_text(question.get("text", ""))
    if template_id:
        question["template_id"] = template_id
        image_bytes = build_visual_from_template(template_id, subject)
        if image_bytes:
            question["image_bytes"] = image_bytes


def ensure_exam_visuals(exam: dict) -> None:
    for question in exam.get("questions", []):
        if question.get("image_bytes"):
            continue
        if question.get("source_pdf") and question.get("source_page"):
            image_bytes = extract_question_image_from_pdf(
                question.get("source_pdf"),
                int(question.get("source_page", 0) or 0),
                question.get("source_number"),
            )
            if image_bytes:
                question["image_bytes"] = image_bytes
                continue
        subject = question.get("subject", "")
        outcome_text = ""
        if question.get("outcomes"):
            outcome_text = question["outcomes"][0]
        apply_visual_policy(question, subject, outcome_text)


def get_visual_match_debug(question: dict) -> tuple[str | None, str]:
    subject = question.get("subject", "")
    outcome_text = ""
    if question.get("outcomes"):
        outcome_text = question["outcomes"][0]
    catalog = load_template_catalog()
    if catalog is None:
        return None, "Katalog yuklenemedi"
    template_id = None
    if outcome_text:
        template_id = select_template_from_catalog(subject, outcome_text)
        if template_id:
            return template_id, "Kazanim metni"
    template_id = select_template_from_text(question.get("text", ""))
    if template_id:
        return template_id, "Soru metni"
    return None, "Tetikleyici yok"



def subject_category(subject: str) -> str:
    norm = normalize_subject_label(subject)
    if "matematik" in norm:
        return "math"
    if "fizik" in norm:
        return "physics"
    if "kimya" in norm:
        return "chem"
    if "biyoloji" in norm:
        return "bio"
    if "edebiyat" in norm or "turk" in norm:
        return "turkish"
    if "tarih" in norm:
        return "history"
    if "cografya" in norm:
        return "geo"
    return "general"


def build_difficulty_slots(total: int, weights: tuple[float, float, float]) -> list[str]:
    easy = int(round(total * weights[0]))
    medium = int(round(total * weights[1]))
    hard = total - easy - medium
    if hard < 0:
        hard = 0
        medium = total - easy
    slots = ["easy"] * easy + ["medium"] * medium + ["hard"] * hard
    random.shuffle(slots)
    return slots


def distribute_subject_counts(subjects: list[str], total: int, overrides: dict) -> dict:
    if overrides:
        return overrides
    if not subjects:
        return {}
    base = total // len(subjects)
    remainder = total % len(subjects)
    counts = {subject: base for subject in subjects}
    for subject in subjects[:remainder]:
        counts[subject] += 1
    return counts


def select_outcome_for_subject(outcomes: list[dict], subject: str) -> dict | None:
    filtered = [item for item in outcomes if item.get("subject") == subject]
    if filtered:
        return random.choice(filtered)
    if outcomes:
        return random.choice(outcomes)
    return None



def rule_based_question(grade: int, qtype: str, subject: str, outcome_text: str, difficulty: str) -> dict:
    category = subject_category(subject)
    rng = random.Random()

    if qtype == "Çoktan Secmeli (ABCD)":
        if category == "math":
            templates = []
            a = rng.randint(2, 6)
            b = rng.randint(1, 9)
            x = rng.randint(1, 5)
            templates.append(
                {
                    "q": f"f(x) = {a}x + {b} için x = {x} iken f(x) kac olur?",
                    "options": [str(a * x + b - 2), str(a * x + b - 1), str(a * x + b), str(a * x + b + 1)],
                    "answer": "C",
                }
            )
            n = rng.randint(30, 90)
            p = rng.choice([10, 20, 25, 30])
            correct = round(n * p / 100)
            templates.append(
                {
                    "q": f"{n} sayisinin % {p}'i kactir?",
                    "options": [str(correct - 2), str(correct), str(correct + 2), str(correct + 4)],
                    "answer": "B",
                }
            )
            m = rng.randint(2, 9)
            d = rng.randint(2, 6)
            templates.append(
                {
                    "q": f"{m * d} sayisinin {d}'ye bolumu kactir?",
                    "options": [str(m - 1), str(m), str(m + 1), str(m + 2)],
                    "answer": "B",
                }
            )
            base = rng.randint(2, 8)
            exp = rng.randint(2, 3)
            value = base ** exp
            templates.append(
                {
                    "q": f"{base}^{exp} ifadesinin degeri kactir?",
                    "options": [str(value - 1), str(value), str(value + 1), str(value + 2)],
                    "answer": "B",
                }
            )
            pick = rng.choice(templates)
            question = pick["q"]
            options = pick["options"]
            answer = pick["answer"]
        elif category == "physics":
            v = rng.randint(3, 8)
            t = rng.randint(2, 6)
            s = v * t
            q1 = {
                "q": f"Bir arac {v} m/s hizla {t} s hareket ediyor. Alinan yol kac metredir?",
                "options": [str(s - v), str(s), str(s + v), str(s + 2 * v)],
                "answer": "B",
            }
            m = rng.randint(1, 5)
            a = rng.randint(2, 6)
            f = m * a
            q2 = {
                "q": f"Kutlesi {m} kg olan cisme {a} m/s^2 ivme veriliyor. Uygulanan kuvvet kactir?",
                "options": [str(f - a), str(f), str(f + a), str(f + 2 * a)],
                "answer": "B",
            }
            e = rng.randint(10, 40)
            q3 = {
                "q": f"{e} J is yapan bir kuvvet sonucu yapilan is miktari kactir?",
                "options": [str(e - 5), str(e), str(e + 5), str(e + 10)],
                "answer": "B",
            }
            pick = rng.choice([q1, q2, q3])
            question = pick["q"]
            options = pick["options"]
            answer = pick["answer"]
        elif category == "chem":
            solute = rng.randint(5, 15)
            solvent = rng.randint(50, 95)
            total = solute + solvent
            percent = round((solute / total) * 100)
            q1 = {
                "q": f"{solute} g tuz, {solvent} g su icinde cozunuyor. Cozeltinin kutlece yuzde derisimi kactir?",
                "options": [f"%{max(1, percent-5)}", f"%{percent}", f"%{percent+5}", f"%{percent+10}"],
                "answer": "B",
            }
            mol = rng.randint(1, 4)
            vol = rng.choice([0.5, 1, 2])
            mval = mol / vol
            q2 = {
                "q": f"{mol} mol cozunen, {vol} L cozeltide molarite kactir?",
                "options": [str(mval - 1), str(mval), str(mval + 1), str(mval + 2)],
                "answer": "B",
            }
            q3 = {
                "q": "Asagidakilerden hangisi asidik ozellik gosterir?",
                "options": ["Sirke", "Sabun", "Amonyak", "Camasir suyu"],
                "answer": "A",
            }
            pick = rng.choice([q1, q2, q3])
            question = pick["q"]
            options = pick["options"]
            answer = pick["answer"]
        elif category == "bio":
            q1 = {
                "q": "Hucresel solunumda ATP uretiminin en fazla gerceklestigi organel hangisidir?",
                "options": ["Mitokondri", "Ribozom", "Golgi", "Lizozom"],
                "answer": "A",
            }
            q2 = {
                "q": "Mitoz bolunmenin sonucu olarak hangisi gorulur?",
                "options": ["Buyume ve onarim", "Gamet olusumu", "Krossing-over", "Yarilanma"],
                "answer": "A",
            }
            q3 = {
                "q": "DNA'nin kendini eslemesi hangi evrede gerceklesir?",
                "options": ["Interfaz", "Profaz", "Metafaz", "Anafaz"],
                "answer": "A",
            }
            pick = rng.choice([q1, q2, q3])
            question = pick["q"]
            options = pick["options"]
            answer = pick["answer"]
        elif category == "geo":
            q1 = {
                "q": "Asagidakilerden hangisi iklimi etkileyen bir unsurdur?",
                "options": ["Yukselti", "Nufus", "Sanayi", "Goc"],
                "answer": "A",
            }
            q2 = {
                "q": "Paralel ve meridyenlerin temel gorevi nedir?",
                "options": ["Konum belirtmek", "Nufus saymak", "Dag sayisi", "Bitki ortusu"],
                "answer": "A",
            }
            pick = rng.choice([q1, q2])
            question = pick["q"]
            options = pick["options"]
            answer = pick["answer"]
        elif category == "history":
            q1 = {
                "q": "Asagidakilerden hangisi Kurtulus Savasi sonrasi imzalanmistir?",
                "options": ["Lozan", "Sevr", "Mondros", "Berlin"],
                "answer": "A",
            }
            q2 = {
                "q": "Osmanli Devleti'nin ilk anayasasi hangisidir?",
                "options": ["Kanun-i Esasi", "Teokratik Yasa", "Tanzimat", "Islahat"],
                "answer": "A",
            }
            pick = rng.choice([q1, q2])
            question = pick["q"]
            options = pick["options"]
            answer = pick["answer"]
        else:
            q1 = {
                "q": "Asagidakilerden hangisi verilen kazanima uygun bir ornektir?",
                "options": [
                    "Kazanima dogrudan uygun durum",
                    "Kazanima kismen uygun durum",
                    "Kazanima uygun olmayan durum",
                    "Kazanima ters dusen durum",
                ],
                "answer": "A",
            }
            question = q1["q"]
            options = q1["options"]
            answer = q1["answer"]

        question = varied_text(question, outcome_text)
        return {"text": question, "options": options, "answer": answer}

    if qtype == "Dogru/Yanlis":
        statements = {
            "math": [
                ("Bir sayinin karesi, sayinin kendisiyle carpimidir.", "Dogru"),
                ("Bir sayiyi 0 ile carpinca sayi degismez.", "Yanlis"),
            ],
            "physics": [
                ("Hiz = yol / zaman ifadesi dogrudur.", "Dogru"),
                ("Surtunme kuvveti her zaman harekete destek olur.", "Yanlis"),
            ],
            "chem": [
                ("Sicaklik arttikca kimyasal tepkime hizi genellikle artar.", "Dogru"),
                ("Asitler mavi turnusol kagidini mavi yapar.", "Yanlis"),
            ],
            "bio": [
                ("Fotosentez olayi yalnizca bitkilerin yapraklarinda gerceklesir.", "Yanlis"),
                ("DNA hucre cekirdegi icinde bulunabilir.", "Dogru"),
            ],
            "geo": [
                ("Iklimi etkileyen faktorlerden biri yukselti farkidir.", "Dogru"),
                ("Ekvatora yaklastikca sicaklik azalir.", "Yanlis"),
            ],
            "history": [
                ("Lozan Antlasmasi Kurtulus Savasindan sonra imzalanmistir.", "Dogru"),
                ("Tanzimat Fermani Osmanli Devleti kurulmadan once ilan edilmistir.", "Yanlis"),
            ],
        }
        pool = statements.get(category, [("Bilimsel yontem gozleme dayanir.", "Dogru")])
        statement, answer = rng.choice(pool)
        statement = varied_text(statement, outcome_text)
        return {"text": statement, "options": ["Dogru", "Yanlis"], "answer": answer}

    if qtype == "Bosluk Doldurma":
        blanks = {
            "math": [
                ("Bir sayinin karesi, sayinin kendisiyle ________ edilmesiyle bulunur.", "carpim"),
                ("Bir dogrunun egimi, degisim / ________ olarak bulunur.", "degisim"),
            ],
            "physics": [
                ("Bir maddenin sicakligi artinca taneciklerinin ortalama kinetik enerjisi ________.", "artar"),
                ("Is, bir kuvvetin yol boyunca yaptigi ________ olarak tanimlanir.", "enerji aktarimi"),
            ],
            "chem": [
                ("Asitler mavi turnusol kagidini ________ renge cevirir.", "kirmizi"),
                ("Su molekulu H2O olarak ________ atomu icerir.", "iki hidrojen"),
            ],
            "bio": [
                ("Fotosentezde klorofil ________ enerjisini kullanir.", "isik"),
                ("Proteinlerin yapi tasi ________ asittir.", "amino"),
            ],
            "geo": [
                ("Dunyanin kendi ekseni etrafinda donmesi sonucunda ________ olusur.", "gece ve gunduz"),
                ("Yeryuzunde yukselti arttikca sicaklik genellikle ________.", "azalir"),
            ],
        }
        pool = blanks.get(category, [("Bilimsel yontem gozleme dayanir.", "gozlem")])
        text_q, ans = rng.choice(pool)
        text_q = varied_text(text_q, outcome_text)
        return {"text": text_q, "options": [], "answer": ans}

    if qtype == "Açık Uclu":
        prompts = [
            "Asagidaki kazanimi aciklayiniz ve bir ornek veriniz.",
            "Konu ile ilgili iki temel kavrami aciklayiniz.",
            "Verilen kazanimi gunluk hayattan bir ornekle destekleyiniz.",
        ]
        text_q = rng.choice(prompts)
        text_q = varied_text(text_q, outcome_text)
        return {"text": text_q, "options": [], "answer": ""}

    if qtype == "Klasik":
        prompts = {
            "math": [
                "Tablo: x=1->3, x=2->5, x=3->7. Oruntuyu bulunuz.",
                "Bir sayinin 3 fazlasinin 2 katini ifade eden cebirsel ifade nedir?",
            ],
            "physics": [
                "Gündelik hayatta enerji donusumune bir ornek veriniz.",
                "Hareket, hiz ve ivme kavramlarini kisaca aciklayiniz.",
            ],
            "chem": [
                "Asit ve bazlara iki farkli ornek veriniz.",
                "Cozunme ve erime kavramlarini karsilastiriniz.",
            ],
            "bio": [
                "Hucrede bulunan organellerden iki tanesini aciklayiniz.",
                "Fotosentezin canlilar için onemini yaziniz.",
            ],
            "geo": [
                "Iklim ve hava durumu arasindaki farki aciklayiniz.",
                "Goclerin nedenlerine iki ornek veriniz.",
            ],
            "history": [
                "Kurtulus Savasi surecinden bir olayi yaziniz.",
                "Tanzimat doneminin iki onemli sonucunu yaziniz.",
            ],
        }
        pool = prompts.get(category, ["Tablodaki verileri kullanarak sonucu yorumlayiniz."])
        text_q = rng.choice(pool)
        text_q = varied_text(text_q, outcome_text)
        return {"text": text_q, "options": [], "answer": ""}

    return {"text": varied_text(f"{subject} dersi için soru.", outcome_text), "options": [], "answer": ""}


def parse_ai_mcq(text: str, option_count: int = 4) -> tuple[str, list[str], str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    options = {}
    answer = ""
    question_lines = []
    for line in lines:
        m = re.match(r"^([A-Ea-e])[\)\-\.:]\s*(.+)$", line)
        if m:
            options[m.group(1).upper()] = m.group(2).strip()
            continue
        if line.lower().startswith("cevap"):
            answer = line.split(":", 1)[-1].strip().upper()[:1]
            continue
        question_lines.append(line)
    question = " ".join(question_lines).strip() or text.strip()
    letters = ["A", "B", "C", "D", "E"]
    if option_count < 4:
        option_count = 4
    options_list = [options.get(letter, letter) for letter in letters[:option_count]]
    valid_answers = set(letters[:option_count])
    if answer not in valid_answers:
        answer = "A"
    return question, options_list, answer


def parse_ai_true_false(text: str) -> tuple[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    answer = ""
    question_lines = []
    for line in lines:
        if line.lower().startswith("cevap"):
            answer = line.split(":", 1)[-1].strip()
            continue
        question_lines.append(line)
    question = " ".join(question_lines).strip() or text.strip()
    if "dogru" in answer.lower():
        return question, "Dogru"
    if "yanlis" in answer.lower():
        return question, "Yanlis"
    if "dogru" in question.lower():
        return question, "Dogru"
    return question, "Yanlis"



def filter_outcomes(
    grade_filter: int | str,
    subject_filter: list[str],
    month_filter: list[str] | None = None,
    week_filter: list[int] | None = None,
) -> list[dict]:
    outcomes = st.session_state.outcomes_data
    filtered = []
    grade_value = None
    if grade_filter != "Tüm":
        try:
            grade_value = int(grade_filter)
        except Exception:
            grade_value = None
    for item in outcomes:
        if grade_value and item["grade"] != grade_value:
            continue
        if subject_filter and item["subject"] not in subject_filter:
            continue
        if month_filter:
            month = item.get("month") or "Belirsiz"
            if month not in month_filter:
                continue
        if week_filter:
            week = item.get("week")
            if week not in week_filter:
                continue
        filtered.append(item)
    return filtered


def build_outcome_dataframe(outcomes: list[dict], selected_ids: set) -> pd.DataFrame:
    rows = []
    for item in outcomes:
        rows.append(
            {
                "id": item["id"],
                "Sec": item["id"] in selected_ids,
                "Sınıf": item["grade"],
                "Ders": display_subject_label(item["subject"]),
                "Tur": item["outcome_type"],
                "Kazanım/Ogrenme Ciktisi": item["outcome"],
                "Kaynak": item["source_file"],
            }
        )
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows).set_index("id")
    return df


def render_outcomes_selector() -> None:
    with st.expander("Kazanım / Ogrenme Ciktilari (Excel)", expanded=True):
        base_dir = get_outcome_base_dir()
        st.caption(f"Klasor: {base_dir}")
        files = list_outcome_files(base_dir)
        if files:
            st.write(f"Bulunan dosya sayisi: {len(files)}")
            st.dataframe(files, use_container_width=True)
        else:
            st.warning("Excel dosyasi bulunamadı.")

        if files and not st.session_state.outcomes_data and not st.session_state.outcomes_loaded_once:
            load_outcomes()
            st.session_state.outcomes_loaded_once = True

        status_line = (
            f"Yuklenen kazanım sayisi: {len(st.session_state.outcomes_data)} | "
            f"Hata sayisi: {len(st.session_state.outcomes_errors)}"
        )
        st.caption(status_line)

        if st.button("Yuklemeyi Temizle"):

            st.session_state.outcomes_data = []
            st.session_state.outcomes_errors = []
            st.session_state.outcomes_loaded_once = False
            st.session_state.selected_outcome_ids = []
            st.info("Yukleme verileri temizlendi.")

        if st.button("Excel'den Yukle"):

            load_outcomes()
            st.session_state.outcomes_loaded_once = True
            if st.session_state.outcomes_data:
                st.success(f"{len(st.session_state.outcomes_data)} kazanım/ogrenme cikti yuklendi.")

        for error in st.session_state.outcomes_errors:
            st.error(error)

        if not st.session_state.outcomes_data:
            st.info("Kazanım/ogrenme ciktilari yuklenmedi.")
            return

        grade_filter = st.session_state.get("selected_grade", "Tüm")
        st.caption(f"Secilen sinif: {grade_filter}")

        subjects = st.session_state.selected_subjects or get_subjects_from_outcomes()
        subjects = [s for s in subjects if not is_excluded_subject(s)]
        if not subjects:
            st.info("Ders secimi yapilmadi. Önce ders secin.")
            return

        month_options = MONTHS_TR + ["Belirsiz"]
        month_filter = st.multiselect(
            "Sınav hangi aylari kapsayacak?",
            month_options,
            default=st.session_state.get("outcome_month_filter", MONTHS_TR),
            key="outcome_month_filter",
        )

        base_filtered = filter_outcomes(grade_filter, subjects)
        week_options = sorted({item.get("week") for item in base_filtered if item.get("week")})
        week_filter = None
        if week_options:
            week_filter = st.multiselect(
                "Sınav hangi haftalari kapsayacak?",
                week_options,
                default=st.session_state.get("outcome_week_filter", week_options),
                key="outcome_week_filter",
            )
        else:
            st.info("Hafta bilgisi bulunamadı. Yalnizca ay filtresi kullaniliyor.")

        filtered = filter_outcomes(grade_filter, subjects, month_filter, week_filter)
        if not filtered:
            st.info("Filtreye uygun kazanim bulunamadı.")
            return
        visible_ids = {item["id"] for item in filtered}
        # Build outcome dataframe for optional tabular view
        _outcome_df = build_outcome_dataframe(filtered, set(st.session_state.selected_outcome_ids))
        selected_ids = set(st.session_state.selected_outcome_ids) | set(visible_ids)
        new_selected = set(selected_ids - visible_ids)
        month_groups = {month: [] for month in MONTHS_TR}
        month_groups["Belirsiz"] = []
        for item in filtered:
            month = item.get("month") or "Belirsiz"
            if month not in month_groups:
                month_groups["Belirsiz"].append(item)
            else:
                month_groups[month].append(item)

        for month in MONTHS_TR + ["Belirsiz"]:
            group = month_groups.get(month, [])
            if not group:
                continue
            with st.expander(month, expanded=True):
                for item in group:
                    key = f"outcome_{item['id']}"
                    label = outcome_label(item)
                    checked = item["id"] in selected_ids
                    if st.checkbox(label, value=checked, key=key):
                        new_selected.add(item["id"])

        st.session_state.selected_outcome_ids = list(new_selected)
        st.caption(f"Secili kazanim sayisi: {len(st.session_state.selected_outcome_ids)}")


def get_selected_outcomes_for_grade(grade: int) -> list[dict]:
    selected_ids = set(st.session_state.selected_outcome_ids)
    return [
        item for item in st.session_state.outcomes_data
        if item["id"] in selected_ids and item["grade"] == grade
    ]


def outcome_label(outcome: dict) -> str:
    return f"{outcome['subject']} - {outcome['outcome']}"


# ==================== QUESTION GENERATION ====================

def normalize_question_types(selected_types: list[str]) -> list[str]:
    if "Karisik" in selected_types:
        return [qtype for qtype in st.session_state.question_types if qtype != "Karisik"]
    return selected_types


def get_openai_api_key() -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


def maybe_generate_ai_question(grade: int, qtype: str, subject: str, outcome_text: str, difficulty: str) -> dict | None:
    api_key = get_openai_api_key()
    if not api_key:
        st.session_state.ai_last_error = "OPENAI_API_KEY bulunamadı."
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        mcq_format = (
            "Eger Çoktan Secmeli ise su formati kullan:\n"
            "Soru: ...\nA) ...\nB) ...\nC) ...\nD) ...\nCevap: A/B/C/D\n"
        )
        if qtype == "Çoktan Secmeli (ABCDE)":
            mcq_format = (
                "Eger Çoktan Secmeli ise su formati kullan:\n"
                "Soru: ...\nA) ...\nB) ...\nC) ...\nD) ...\nE) ...\nCevap: A/B/C/D/E\n"
            )
        format_rules = (
            "Yanlis veya gereksiz aciklama YAZMA. Yalnizca istenen formatta cikti ver.\n"
            f"{mcq_format}"
            "Eger Dogru/Yanlis ise:\nSoru: ...\nCevap: Dogru/Yanlis\n"
            "Eger Bosluk Doldurma ise:\nSoru: ...\nCevap: ...\n"
            "Eger Açık Uclu/Klasik ise:\nSoru: ...\n"
            "Eger gorsel gerekiyorsa yeni satirda 'Gorsel: <tip>' yaz.\n"
            "Tipler: grafik, pasta, cizgi, histogram, harita, hiz-zaman, geometri-ucgen, geometri-daire, "
            "geometri-dikdortgen, koordinat, prizma, aci, fonksiyon, venn, tablo, hucre.\n"
            "Gorsel gerekmiyorsa 'Gorsel: yok' yaz.\n"
        )
        prompt = (
            f"{grade}. sinif {subject} dersi için {qtype} soru yaz. Zorluk: {difficulty}. "
            f"Kazanim/ogrenme cikti: {outcome_text}. "
            "Soru mutlaka bu kazanima dogrudan uygun olsun. "
            f"{format_rules}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen deneyimli bir ogretmensin. Sadece istenen formatta cikti ver."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        raw = response.choices[0].message.content.strip()
        st.session_state.ai_last_error = ""
        visual_hint = ""
        cleaned_lines = []
        for line in raw.splitlines():
            if line.strip().lower().startswith("gorsel"):
                visual_hint = line.split(":", 1)[-1].strip()
                continue
            cleaned_lines.append(line)
        cleaned_raw = "\n".join(cleaned_lines).strip()
        if qtype == "Çoktan Secmeli (ABCD)":
            question, options, answer = parse_ai_mcq(cleaned_raw, option_count=4)
            return {"text": question, "options": options, "answer": answer, "visual_hint": visual_hint}
        if qtype == "Çoktan Secmeli (ABCDE)":
            question, options, answer = parse_ai_mcq(cleaned_raw, option_count=5)
            return {"text": question, "options": options, "answer": answer, "visual_hint": visual_hint}
        if qtype == "Dogru/Yanlis":
            question, answer = parse_ai_true_false(cleaned_raw)
            return {"text": question, "options": ["Dogru", "Yanlis"], "answer": answer, "visual_hint": visual_hint}
        if qtype == "Bosluk Doldurma":
            parts = [line for line in cleaned_raw.splitlines() if line.strip()]
            question = parts[0].replace("Soru:", "").strip() if parts else (cleaned_raw or raw)
            answer = ""
            for line in parts:
                if line.lower().startswith("cevap"):
                    answer = line.split(":", 1)[-1].strip()
            return {"text": question, "options": [], "answer": answer, "visual_hint": visual_hint}
        return {"text": cleaned_raw.replace("Soru:", "").strip(), "options": [], "answer": "", "visual_hint": visual_hint}
    except Exception as exc:
        st.session_state.ai_last_error = str(exc)
        return None


def generate_random_question(
    grade: int,
    qtype: str,
    subject: str | None = None,
    outcome: dict | None = None,
    use_ai: bool = False,
    difficulty: str = "medium",
    force_graph: bool = False,
) -> dict:
    if outcome and not subject:
        subject = outcome["subject"]
    if not subject:
        subject = random.choice(get_subjects_from_outcomes())

    outcome_text = outcome["outcome"] if outcome else ""
    visual_hint = None

    if force_graph:
        qtype = "Çoktan Secmeli (ABCD)"
        rb = build_graph_question(subject)
        template_id = select_template_from_catalog(subject, outcome_text) if outcome_text else None
        image_bytes = build_visual_from_template(template_id, subject) or rb.get("image_bytes")
        question_text = varied_text(rb["text"], outcome_text)
        options = rb.get("options", [])
        answer = rb.get("answer", "")
        source = "graph"
    else:
        ai_payload = None
        if use_ai and not force_graph:
            ai_payload = maybe_generate_ai_question(
                grade,
                qtype,
                subject,
                outcome_text or "Genel kazanim",
                difficulty,
            )

        if ai_payload:
            question_text = ai_payload.get("text", "")
            options = ai_payload.get("options", [])
            answer = ai_payload.get("answer", "")
            visual_hint = ai_payload.get("visual_hint", "")
            image_bytes = None
            source = "ai"
        else:
            rb = rule_based_question(grade, qtype, subject, outcome_text, difficulty)
            question_text = rb["text"]
            options = rb.get("options", [])
            answer = rb.get("answer", "")
            source = "random"
            image_bytes = rb.get("image_bytes")

    base_id = f"{grade}-{subject}-{random.randint(1000, 9999)}"
    payload = {
        "id": base_id,
        "grade": grade,
        "subject": subject,
        "question_type": qtype,
        "difficulty": difficulty,
        "text": question_text,
        "options": options,
        "answer": answer,
        "source": source,
        "outcome_ids": [outcome["id"]] if outcome else [],
        "outcomes": [outcome_text] if outcome_text else [],
    }
    if image_bytes:
        payload["image_bytes"] = image_bytes
    apply_visual_policy(payload, subject, outcome_text, visual_hint if use_ai else None)
    return payload


def build_topic_distribution(exam: dict) -> dict[str, list[tuple[int, str]]]:
    topic_map: dict[str, list[tuple[int, str]]] = {}
    for idx, question in enumerate(exam.get("questions", []), start=1):
        subject = question.get("subject", "").strip()
        if not subject:
            continue
        topic = ""
        if question.get("outcomes"):
            topic = question["outcomes"][0]
        else:
            topic = question.get("text", "")
        topic = topic.replace("\n", " ").strip()
        if not topic:
            continue
        topic_map.setdefault(subject, []).append((idx, topic))
    return topic_map


def group_questions_by_subject(exam: dict) -> list[tuple[str, list[dict]]]:
    order = exam.get("subject_order") or []
    groups: dict[str, list[dict]] = {}
    for question in exam.get("questions", []):
        subject = question.get("subject", "").strip()
        if not subject:
            subject = "Genel"
        groups.setdefault(subject, []).append(question)
    ordered_subjects = [s for s in order if s in groups]
    for subject in sorted(groups.keys()):
        if subject not in ordered_subjects:
            ordered_subjects.append(subject)
    return [(subject, groups[subject]) for subject in ordered_subjects]



def build_exam_pdf(exam: dict) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib import colors

        if not exam.get("exam_code"):
            exam["exam_code"] = f"{exam.get('grade','')}{exam.get('section','')}-{random.randint(100000, 999999)}"
        if not exam.get("qr_bytes") and exam.get("exam_code"):
            exam["qr_bytes"] = build_qr_bytes(exam["exam_code"])

        from utils.shared_data import ensure_turkish_pdf_fonts
        font_regular, font_bold = ensure_turkish_pdf_fonts()

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 40

        subject_counts = exam.get("subject_counts") or {}
        if not subject_counts:
            for question in exam.get("questions", []):
                subject = question.get("subject", "")
                if subject:
                    subject_counts[subject] = subject_counts.get(subject, 0) + 1
        rules = exam.get("cover_instructions") or DEFAULT_COVER_RULES

        def draw_page_header() -> int:
            name = (exam.get("school_name", "") or "Okul Adi").strip()
            pdf.setFont(font_bold, 11)
            text_width = pdf.stringWidth(name, font_bold, 11)
            pdf.drawString((width - text_width) / 2, height - 30, name)
            return height - 50

        # Cover page
        cover_rgb = hex_to_rgb(exam.get("brand_primary", "#0F4C81"))
        accent_rgb = hex_to_rgb(exam.get("brand_secondary", "#F2A900"))
        pdf.setFillColor(colors.Color(*cover_rgb))
        pdf.rect(0, 0, width, height, stroke=0, fill=1)
        pdf.setFillColor(colors.Color(*accent_rgb))
        pdf.rect(0, 0, width, 32, stroke=0, fill=1)
        pdf.setFillColor(colors.white)
        pdf.setStrokeColor(colors.white)
        if exam.get("school_logo_bytes"):
            try:
                logo = ImageReader(io.BytesIO(exam["school_logo_bytes"]))
                pdf.drawImage(
                    logo, 40, height - 180, width=160, height=80,
                    preserveAspectRatio=True, mask='auto'
                )
            except Exception:
                pass
        if exam.get("qr_bytes"):
            try:
                qr = ImageReader(io.BytesIO(exam["qr_bytes"]))
                pdf.drawImage(
                    qr, width - 140, height - 165, width=90, height=90,
                    preserveAspectRatio=True, mask='auto'
                )
            except Exception:
                pass

        pdf.setFont(font_bold, 16)
        pdf.drawString(40, height - 200, (exam.get("exam_type") or "Deneme Sınavı").upper())
        pdf.setFont(font_bold, 14)
        pdf.drawString(40, height - 218, f"{exam['grade']}. SINIF")
        pdf.setFont(font_regular, 11)
        pdf.drawString(40, height - 234, exam.get("exam_name", ""))

        right_x = width - 200
        pdf.setFont(font_regular, 10)
        pdf.drawString(right_x, height - 205, f"Sınav Kodu: {exam.get('exam_code', '')}")
        pdf.drawString(right_x, height - 221, f"Kitapcik Tipi: {exam.get('booklet_type', 'A')}")
        pdf.drawString(right_x, height - 237, f"Sure: {exam.get('duration', '')} dk")

        y = height - 260
        pdf.setFont(font_bold, 10)
        for label in ["Adi ve Soyadi", "Sınıfı / Şube / Numara"]:
            pdf.drawString(40, y, label)
            pdf.line(200, y - 2, width - 40, y - 2)
            y -= 20

        items = sorted(subject_counts.items(), key=lambda item: item[0])
        if items:
            pdf.setFont(font_bold, 10)
            pdf.drawString(40, y, "Ders")
            pdf.drawString(180, y, "Soru Sayısı")
            pdf.drawString(300, y, "Ders")
            pdf.drawString(440, y, "Soru Sayısı")
            y -= 14
            pdf.setFont(font_regular, 10)
            half = (len(items) + 1) // 2
            left = items[:half]
            right = items[half:]
            rows = max(len(left), len(right))
            for i in range(rows):
                if i < len(left):
                    pdf.drawString(40, y, str(display_subject_label(left[i][0]))[:22])
                    pdf.drawString(180, y, str(left[i][1]))
                if i < len(right):
                    pdf.drawString(300, y, str(display_subject_label(right[i][0]))[:22])
                    pdf.drawString(440, y, str(right[i][1]))
                y -= 12
            y -= 8

        pdf.setFont(font_bold, 11)
        pdf.drawString(40, y, "ADAYLARIN DIKKATINE!")
        y -= 14
        pdf.setFont(font_regular, 9)
        for idx, rule in enumerate(rules, start=1):
            wrapped = textwrap.wrap(rule, width=110) or [rule]
            for line_idx, line in enumerate(wrapped):
                if y < 60:
                    pdf.showPage()
                    y = height - 40
                prefix = f"{idx}. " if line_idx == 0 else "   "
                pdf.drawString(40, y, f"{prefix}{line}")
                y -= 12

        pdf.showPage()
        pdf.setFillColor(colors.black)
        pdf.setStrokeColor(colors.black)
        y = draw_page_header()

        if exam.get("include_topic_distribution"):
            topic_map = build_topic_distribution(exam)
            pdf.setFont(font_bold, 14)
            pdf.drawString(40, height - 40, "Konu Dagilimi")
            y = height - 70
            for subject, entries in topic_map.items():
                if y < 80:
                    pdf.showPage()
                    y = draw_page_header()
                pdf.setFont(font_bold, 11)
                pdf.drawString(40, y, display_subject_label(subject))
                y -= 14
                pdf.setFont(font_regular, 9)
                for number, topic in entries:
                    if y < 60:
                        pdf.showPage()
                        y = height - 40
                    line = f"{number}. {topic}"
                    pdf.drawString(50, y, line[:120])
                    y -= 12
                y -= 8
            pdf.showPage()
            y = draw_page_header()

        question_no = 1
        subject_groups = group_questions_by_subject(exam)
        for subject_idx, (subject, questions) in enumerate(subject_groups):
            if subject_idx > 0:
                pdf.showPage()
                y = draw_page_header()
            display_subject = display_subject_label(subject)
            pdf.setFont(font_bold, 13)
            header_right = f"{exam.get('grade', '')}/{exam.get('section', '')}".strip()
            pdf.setFont(font_regular, 10)
            pdf.drawString(width - 200, y + 4, header_right)
            pdf.setFont(font_bold, 12)
            header_text = f"{display_subject} {exam.get('exam_name', '')} {exam.get('booklet_type', 'A')}"
            header_width = pdf.stringWidth(header_text, font_bold, 12)
            pdf.drawString((width - header_width) / 2, y, header_text)
            pdf.setFont(font_regular, 9)
            pdf.drawString(40, y - 14, f"Bu testte {len(questions)} soru vardir.")
            pdf.drawString(40, y - 26, "Cevaplarinizi cevap kagidina isaretleyiniz.")
            y -= 44

            for question in questions:
                if y < 80:
                    pdf.showPage()
                    y = draw_page_header()
                    pdf.setFont(font_bold, 12)
                    header_text = f"{display_subject} {exam.get('exam_name', '')} {exam.get('booklet_type', 'A')}"
                    header_width = pdf.stringWidth(header_text, font_bold, 12)
                    pdf.drawString((width - header_width) / 2, y, header_text)
                    pdf.setFont(font_regular, 9)
                    pdf.drawString(40, y - 14, f"Bu testte {len(questions)} soru vardir.")
                    pdf.drawString(40, y - 26, "Cevaplarinizi cevap kagidina isaretleyiniz.")
                    y -= 44

                is_pdf_image = bool(question.get("source_pdf") and question.get("image_bytes"))
                if not is_pdf_image:
                    pdf.setFont(font_regular, 10)
                    text = f"{question_no}. {display_question_text(question)}"
                    for line in textwrap.wrap(text, width=110):
                        pdf.drawString(40, y, line)
                        y -= 12

                if question.get('image_bytes'):
                    try:
                        img = ImageReader(io.BytesIO(question['image_bytes']))
                        img_w, img_h = img.getSize()
                        scale = min(320 / img_w, 180 / img_h)
                        draw_w = img_w * scale
                        draw_h = img_h * scale
                        if y - draw_h < 40:
                            pdf.showPage()
                            y = height - 40
                        pdf.drawImage(img, 40, y - draw_h, width=draw_w, height=draw_h)
                        y -= draw_h + 8
                    except Exception:
                        pass

                if question.get("options") and not is_pdf_image:
                    pdf.setFont(font_regular, 9)
                    options = question["options"]
                    if question["question_type"] == "Çoktan Secmeli (ABCD)":
                        labels = ["A", "B", "C", "D"]
                        for label, option in zip(labels, options):
                            line = f"{label}) {option}"
                            for wrapped in textwrap.wrap(line, width=100):
                                pdf.drawString(50, y, wrapped)
                                y -= 11
                    elif question["question_type"] == "Dogru/Yanlis":
                        pdf.drawString(50, y, "D) Dogru    Y) Yanlis")
                        y -= 12
                    else:
                        pdf.drawString(50, y, " / ".join(options))
                        y -= 12

                y -= 6
                question_no += 1

            footer_text = "Bu dersin sinavi bitti, yeni sinava geciniz."
            pdf.setFont(font_regular, 9)
            footer_width = pdf.stringWidth(footer_text, font_regular, 9)
            pdf.drawString((width - footer_width) / 2, 40, footer_text)
            if subject_idx == len(subject_groups) - 1:
                end_text = "Sınav bitti."
                end_width = pdf.stringWidth(end_text, font_regular, 9)
                pdf.drawString((width - end_width) / 2, 24, end_text)

        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        return None

# ==================== ANSWER SHEET ====================

def _parse_student_list(raw: str) -> list[dict]:
    students = []
    for line in (raw or "").splitlines():
        parts = [p.strip() for p in re.split(r"[;,]", line) if p.strip()]
        if not parts:
            continue
        record = {"id": parts[0]}
        if len(parts) > 1:
            record["name"] = parts[1]
        if len(parts) > 2:
            record["class"] = parts[2]
        students.append(record)
    return students


def _serialize_student_list(students: list[dict]) -> str:
    lines = []
    for student in students:
        sid = student.get("id", "").strip()
        name = student.get("name", "").strip()
        clazz = student.get("class", "").strip()
        parts = [sid, name, clazz]
        line = ", ".join([p for p in parts if p])
        if line:
            lines.append(line)
    return "\n".join(lines)


def build_answer_sheet_pdf(exam: dict, students: list[dict]) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib import colors

        from utils.shared_data import ensure_turkish_pdf_fonts
        font_regular, font_bold = ensure_turkish_pdf_fonts()

        subject_groups = group_questions_by_subject(exam)
        subject_number_map = {}
        question_no = 1
        for subject, questions in subject_groups:
            mcq_numbers = []
            mcq5_numbers = []
            tf_numbers = []
            for question in questions:
                if question.get("question_type") == "Dogru/Yanlis":
                    tf_numbers.append(question_no)
                elif question.get("question_type") == "Çoktan Secmeli (ABCDE)":
                    mcq5_numbers.append(question_no)
                elif question.get("question_type") == "Çoktan Secmeli (ABCD)":
                    mcq_numbers.append(question_no)
                question_no += 1
            subject_number_map[subject] = {
                "mcq": mcq_numbers,
                "mcq5": mcq5_numbers,
                "tf": tf_numbers,
            }

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        def draw_header(y_top: int, student: dict) -> int:
            pdf.setFont(font_bold, 13)
            title = f"{exam.get('school_name', '')} - Cevap Formu"
            title_width = pdf.stringWidth(title, font_bold, 13)
            pdf.drawString((width - title_width) / 2, y_top, title)
            pdf.setFont(font_regular, 10)
            pdf.drawString(40, y_top - 18, f"Sınav: {exam.get('exam_name', '')}")
            pdf.drawString(40, y_top - 32, f"Sınav Kodu: {exam.get('exam_code', '')}")
            pdf.drawString(40, y_top - 46, f"Sınıf/Şube: {exam.get('grade', '')}/{exam.get('section', '')}")

            pdf.setFont(font_regular, 10)
            pdf.drawString(40, y_top - 66, "Ad Soyad:")
            pdf.drawString(120, y_top - 66, student.get("name", "____________________"))
            pdf.drawString(40, y_top - 82, "Öğrenci ID:")
            pdf.drawString(120, y_top - 82, student.get("id", "____________________"))
            pdf.drawString(40, y_top - 98, "Sınıf/Şube:")
            pdf.drawString(120, y_top - 98, student.get("class", "____________________"))

            student_id = student.get("id") or "ANON"
            qr_payload = f"{exam.get('exam_code','')}|{student_id}"
            qr_bytes = build_qr_bytes(qr_payload)
            if qr_bytes:
                try:
                    qr = ImageReader(io.BytesIO(qr_bytes))
                    pdf.drawImage(qr, width - 140, y_top - 110, width=80, height=80, preserveAspectRatio=True, mask="auto")
                except Exception:
                    pass
            else:
                pdf.rect(width - 140, y_top - 110, 80, 80)
            return y_top - 130

        def draw_bubbles(start_x, start_y, numbers, labels):
            pdf.setFont(font_bold, 10)
            col_width = 120
            row_height = 16
            max_rows = 25
            cols = max(1, math.ceil(len(numbers) / max_rows))
            for col in range(cols):
                x = start_x + col * col_width
                y = start_y
                for row in range(max_rows):
                    idx = col * max_rows + row
                    if idx >= len(numbers):
                        break
                    num = numbers[idx]
                    pdf.setFont(font_regular, 9)
                    pdf.drawString(x, y, f"{num}.")
                    cx = x + 22
                    for label in labels:
                        pdf.circle(cx, y + 3, 5)
                        pdf.setFont(font_regular, 7)
                        pdf.drawCentredString(cx, y + 1.5, label)
                        cx += 18
                    y -= row_height
            return y

        for student in (students or [{}]):
            y = draw_header(height - 40, student)
            for subject, numbers in subject_number_map.items():
                display_subject = display_subject_label(subject)
                if y < 120:
                    pdf.showPage()
                    y = draw_header(height - 40, student)
                pdf.setFont(font_bold, 11)
                pdf.drawString(40, y, display_subject)
                y -= 18
                if numbers["mcq"]:
                    y = draw_bubbles(40, y, numbers["mcq"], ["A", "B", "C", "D"]) - 10
                if numbers["mcq5"]:
                    y = draw_bubbles(40, y, numbers["mcq5"], ["A", "B", "C", "D", "E"]) - 10
                if numbers["tf"]:
                    if y < 120:
                        pdf.showPage()
                        y = draw_header(height - 40, student)
                    pdf.setFont(font_regular, 10)
                    pdf.drawString(40, y, "Dogru / Yanlis")
                    y -= 14
                    y = draw_bubbles(40, y, numbers["tf"], ["D", "Y"]) - 10
            pdf.showPage()

        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        return None

# ==================== OUTPUT ====================

def build_exam_text(exam: dict) -> str:
    lines = [
        f"Okul: {exam.get('school_name', '')}",
        f"Sınav Kodu: {exam.get('exam_code', '')}",
        f"Kitapcik Tipi: {exam.get('booklet_type', 'A')}",
        f"Sınav Adi: {exam['exam_name']}",
        f"Sınıf/Şube: {exam['grade']}/{exam['section']}",
        f"Sınav Turu: {exam['exam_type']}",
        f"Soru Tipleri: {', '.join(exam['question_types'])}",
        f"Soru Sayısı: {exam['question_count']}",
        f"Sure (dk): {exam['duration']}",
        "-" * 40,
    ]
    for idx, question in enumerate(exam['questions'], start=1):
        subject = question.get('subject', '')
        lines.append(f"{idx}. ({question['question_type']}) {subject} - {display_question_text(question)}")
        if question.get('options'):
            option_line = " / ".join(question['options'])
            lines.append(f"   Secenekler: {option_line}")
        if question.get('outcomes'):
            lines.append(f"   Kazanim/Ogrenme: {', '.join(question['outcomes'])}")
        if question.get('answer'):
            lines.append(f"   Cevap: {question['answer']}")
        lines.append("")
    return "\n".join(lines).strip()


def generate_exam_payload(
    exam_name: str,
    grade: int,
    section: str,
    selected_exam_types: list[str],
    selected_question_types: list[str],
    question_count: int,
    duration: int,
    selected_outcomes: list[dict],
    use_selected_outcomes: bool,
    use_ai: bool,
    subjects: list[str],
    subject_counts: dict[str, int],
    progress_cb: callable | None = None,
    difficulty_pref: str = "Karisik",
    use_bank: bool = True,
    min_bank_score: int = 0,
    point_per_question: float | None = None,
    bank_source_filter: str = "all",
    require_exam_type_match: bool = False,
) -> dict:
    def question_signature(question: dict) -> str:
        text_key = question.get("text", "").strip()
        options = "|".join(question.get("options", []))
        image_bytes = question.get("image_bytes")
        image_hash = ""
        if isinstance(image_bytes, (bytes, bytearray)):
            image_hash = hashlib.sha1(image_bytes).hexdigest()
        return f"{text_key}|{options}|{image_hash}"

    def add_unique(question_list, question, seen):
        key = question_signature(question)
        if not question.get("text", "").strip() or key in seen:
            return False
        seen.add(key)
        question_list.append(question)
        return True

    def add_force(question_list, question):
        question_list.append(question)

    def pick_outcome(subject_name: str) -> dict | None:
        if use_selected_outcomes:
            return select_outcome_for_subject(selected_outcomes, subject_name)
        subject_outcomes = [
            item for item in st.session_state.outcomes_data
            if item.get("subject") == subject_name and item.get("grade") == grade
        ]
        if subject_outcomes:
            return random.choice(subject_outcomes)
        return None

    effective_types = normalize_question_types(selected_question_types)
    if bank_source_filter == "pdf_only":
        if "Çoktan Secmeli (ABCDE)" in effective_types and "Çoktan Secmeli (ABCD)" not in effective_types:
            effective_types.append("Çoktan Secmeli (ABCD)")
        if "Çoktan Secmeli (ABCD)" in effective_types and "Çoktan Secmeli (ABCDE)" not in effective_types:
            effective_types.append("Çoktan Secmeli (ABCDE)")
    use_tyt_bank = any(exam_type.strip().lower() == "tyt" for exam_type in selected_exam_types)
    ayt_track = None
    if any(exam_type.strip().upper() == "AYT SAY" for exam_type in selected_exam_types):
        ayt_track = "say"
    elif any(exam_type.strip().upper() == "AYT EA" for exam_type in selected_exam_types):
        ayt_track = "ea"
    elif any(exam_type.strip().upper() == "AYT SOZ" for exam_type in selected_exam_types):
        ayt_track = "soz"

    def is_pdf_source(source: str) -> bool:
        return source == "pdf_image" or source.startswith("pdf_import")

    def is_ayt_source(source: str, track: str) -> bool:
        if not source.startswith("pdf_import_ayt"):
            return False
        return track in source

    def bank_source_ok(question: dict) -> bool:
        source = question.get("source", "")
        if bank_source_filter == "pdf_only":
            if not is_pdf_source(source):
                return False
            if ayt_track:
                return is_ayt_source(source, ayt_track) or source == "pdf_image"
            if use_tyt_bank:
                return source == "pdf_import" or source == "pdf_image"
            return True
        if use_tyt_bank and not ayt_track:
            return not source.startswith("pdf_import_ayt_")
        return True
    selected_outcome_ids = {item["id"] for item in selected_outcomes}
    relax_grade = bank_source_filter == "pdf_only" and (use_tyt_bank or ayt_track)
    bank = [
        question
        for question in st.session_state.question_bank
        if bank_source_ok(question)
        and (question["grade"] == grade or relax_grade)
        and question["question_type"] in effective_types
    ]
    if require_exam_type_match and selected_exam_types:
        bank = [
            question for question in bank
            if question.get("exam_type") in selected_exam_types
            or (bank_source_filter == "pdf_only" and not question.get("exam_type"))
        ]
    if use_selected_outcomes and selected_outcome_ids:
        bank = [
            question for question in bank
            if set(question.get("outcome_ids", [])) & selected_outcome_ids
        ]

    random.shuffle(bank)
    selected_questions = []
    seen_questions = set()

    desired_counts = {
        subject: count
        for subject, count in subject_counts.items()
        if count > 0
    }
    subjects = subjects or get_subjects_from_outcomes()
    subjects = [s for s in subjects if not is_excluded_subject(s)]

    desired_counts = distribute_subject_counts(subjects, question_count, desired_counts)
    question_count = sum(desired_counts.values()) if desired_counts else question_count

    if difficulty_pref != "Karisik":
        difficulty_map = {
            "Kolay": "easy",
            "Orta": "medium",
            "Zor": "hard",
        }
        chosen = difficulty_map.get(difficulty_pref, "medium")
        difficulty_slots = [chosen] * question_count
    else:
        difficulty_slots = build_difficulty_slots(question_count, (0.3, 0.5, 0.2))
    graph_ratio = 0.0 if use_ai else 0.35
    graph_count = int(round(question_count * graph_ratio))
    graph_subjects = [s for s in subjects if subject_category(s) in {"math", "physics", "geo", "bio", "chem", "history"}]
    if graph_subjects and question_count >= len(graph_subjects):
        graph_count = max(graph_count, len(graph_subjects))
    graph_count = min(graph_count, question_count)

    specs = []
    for subject, count in desired_counts.items():
        for _ in range(count):
            difficulty = difficulty_slots.pop() if difficulty_slots else "medium"
            specs.append({"subject": subject, "difficulty": difficulty, "graph": False})

    if graph_count > 0 and specs:
        used_subjects = set()
        for spec in specs:
            if graph_count == 0:
                break
            if spec["subject"] not in used_subjects and spec["subject"] in graph_subjects:
                spec["graph"] = True
                used_subjects.add(spec["subject"])
                graph_count -= 1

        if graph_count > 0:
            remaining = [spec for spec in specs if not spec["graph"] and spec["subject"] in graph_subjects]
            random.shuffle(remaining)
            for spec in remaining[:graph_count]:
                spec["graph"] = True

    random.shuffle(specs)

    per_subject_counts = {subject: 0 for subject in desired_counts}

    if use_bank and st.session_state.question_bank:
        diff_map = {"Kolay": "easy", "Orta": "medium", "Zor": "hard"}
        target_diff = diff_map.get(difficulty_pref, None)
        for subject in desired_counts:
            candidate_pool = [
                q for q in st.session_state.question_bank
                if bank_source_ok(q)
                and (q.get("grade") == grade or relax_grade)
                and q.get("question_type") in effective_types
                and subject_matches_question(q, subject)
                and q.get("quality_score", 0) >= min_bank_score
            ]
            if require_exam_type_match and selected_exam_types:
                candidate_pool = [
                    q for q in candidate_pool
                    if q.get("exam_type") in selected_exam_types
                    or (bank_source_filter == "pdf_only" and not q.get("exam_type"))
                ]
            if target_diff:
                candidate_pool = [q for q in candidate_pool if q.get("difficulty") == target_diff]
            random.shuffle(candidate_pool)
            candidate_pool.sort(key=lambda q: q.get("quality_score", 0), reverse=True)
            for candidate in candidate_pool:
                if per_subject_counts[subject] >= desired_counts[subject]:
                    break
                candidate_copy = dict(candidate)
                outcome_text = ""
                if candidate_copy.get("outcomes"):
                    outcome_text = candidate_copy["outcomes"][0]
                apply_visual_policy(candidate_copy, subject, outcome_text)
                if add_unique(selected_questions, candidate_copy, seen_questions):
                    per_subject_counts[subject] += 1
                    if progress_cb:
                        progress_cb(len(selected_questions), question_count)

    for spec in specs:
        subject = spec["subject"]
        if per_subject_counts.get(subject, 0) >= desired_counts.get(subject, 0):
            continue
        difficulty = spec["difficulty"]
        force_graph = spec["graph"]
        outcome = pick_outcome(subject)
        candidate = generate_random_question(
            grade,
            random.choice(effective_types),
            subject=subject,
            outcome=outcome,
            use_ai=use_ai,
            difficulty=difficulty,
            force_graph=force_graph,
        )
        if add_unique(selected_questions, candidate, seen_questions):
            per_subject_counts[subject] += 1
            if progress_cb:
                progress_cb(len(selected_questions), question_count)

    # Fill remaining per subject strictly
    for subject, target in desired_counts.items():
        attempts = 0
        while per_subject_counts.get(subject, 0) < target and attempts < target * 5:
            attempts += 1
            difficulty = random.choice(["easy", "medium", "hard"])
            outcome = pick_outcome(subject)
            candidate = generate_random_question(
                grade,
                random.choice(effective_types),
                subject=subject,
                outcome=outcome,
                use_ai=use_ai,
                difficulty=difficulty,
                force_graph=not use_ai,
            )
            if add_unique(selected_questions, candidate, seen_questions):
                per_subject_counts[subject] += 1
                if progress_cb:
                    progress_cb(len(selected_questions), question_count)

        # Force fill if still short
        while per_subject_counts.get(subject, 0) < target:
            difficulty = random.choice(["easy", "medium", "hard"])
            outcome = pick_outcome(subject)
            candidate = generate_random_question(
                grade,
                random.choice(effective_types),
                subject=subject,
                outcome=outcome,
                use_ai=use_ai,
                difficulty=difficulty,
                force_graph=not use_ai,
            )
            add_force(selected_questions, candidate)
            per_subject_counts[subject] += 1
            if progress_cb:
                progress_cb(len(selected_questions), question_count)

    if bank_source_filter == "pdf_only":
        random.shuffle(selected_questions)

    ensure_exam_visuals({"questions": selected_questions})

    if point_per_question is not None:
        for question in selected_questions:
            question["points"] = point_per_question

    subject_counts = desired_counts.copy()
    return {
        "exam_name": exam_name.strip(),
        "grade": grade,
        "section": section.strip() or "A",
        "exam_type": ", ".join(selected_exam_types),
        "question_types": effective_types,
        "question_count": question_count,
        "duration": duration,
        "questions": selected_questions,
        "exam_code": "{}{}-{}".format(grade, section, random.randint(100000, 999999)),
        "school_name": st.session_state.school_name,
        "school_logo_bytes": st.session_state.school_logo_bytes,
        "brand_primary": st.session_state.brand_primary,
        "brand_secondary": st.session_state.brand_secondary,
        "booklet_type": st.session_state.booklet_type,
        "include_topic_distribution": st.session_state.include_topic_distribution,
        "cover_two_column": st.session_state.cover_two_column,
        "cover_instructions": st.session_state.cover_instructions,
        "subject_counts": subject_counts,
        "subject_order": subjects,
        "qr_bytes": None,
    }


def build_exam_doc_html(exam: dict) -> str:
    if not exam.get('exam_code'):
        exam['exam_code'] = f"{exam.get('grade','')}{exam.get('section','')}-{random.randint(100000, 999999)}"
    if not exam.get('qr_bytes') and exam.get('exam_code'):
        exam['qr_bytes'] = build_qr_bytes(exam['exam_code'])

    subject_counts = exam.get('subject_counts') or {}
    if not subject_counts:
        for question in exam.get('questions', []):
            subject = question.get('subject', '')
            if subject:
                subject_counts[subject] = subject_counts.get(subject, 0) + 1

    rules = exam.get('cover_instructions') or DEFAULT_COVER_RULES
    topic_map = build_topic_distribution(exam) if exam.get('include_topic_distribution') else {}

    cover_logo_html = ''
    if exam.get('school_logo_bytes'):
        encoded_logo = base64.b64encode(exam['school_logo_bytes']).decode('utf-8')
        cover_logo_html = (
            f"<img src=\"data:image/png;base64,{encoded_logo}\" "
            "style=\"max-width:160px;\"/>"
        )

    cover_qr_html = ''
    if exam.get('qr_bytes'):
        encoded_qr = base64.b64encode(exam['qr_bytes']).decode('utf-8')
        cover_qr_html = (
            f"<img src=\"data:image/png;base64,{encoded_qr}\" "
            "style=\"max-width:120px;\"/>"
        )
    if not cover_qr_html:
        cover_qr_html = (
            "<div style=\"width:120px; height:120px; border:1px solid #999; "
            "display:flex; align-items:center; justify-content:center; "
            "font-size:11px;\">QR KOD</div>"
        )

    school_name_html = exam.get('school_name', '') or 'Okul Adi'
    primary = exam.get('brand_primary', '#0F4C81')
    secondary = exam.get('brand_secondary', '#F2A900')

    question_blocks = []
    question_no = 1
    subject_groups = group_questions_by_subject(exam)
    for subject_idx, (subject, questions) in enumerate(subject_groups):
        if subject_idx > 0:
            question_blocks.append('<div style="page-break-before: always;"></div>')
        display_subject = display_subject_label(subject)
        question_blocks.append(
            f"""
            <div style="margin-top: 12px; font-weight:700; font-size:14px; text-align:center;">{exam.get('school_name', '')}</div>
            <div style="font-size:12px; text-align:center;">Sınıf/Şube: {exam.get('grade', '')}/{exam.get('section', '')}</div>
            <div style="font-size:12px; text-align:center;">Sınav Kodu: {exam.get('exam_code', '')}</div>
            <div style="margin-top: 6px; font-weight:700; text-align:center;">{display_subject} {exam.get('exam_name', '')} {exam.get('booklet_type', 'A')}</div>
            <div style="font-size:12px; text-align:center;">Bu testte {len(questions)} soru vardır.</div>
            <div style="font-size:12px; margin-bottom:8px; text-align:center;">Cevaplarınızı cevap kağıdına işaretleyiniz.</div>
            """
        )
        for question in questions:
            options_html = ''
            if question.get('options'):
                if question['question_type'] == 'Çoktan Secmeli (ABCD)':
                    labels = ['A', 'B', 'C', 'D']
                    option_items = ''.join(
                        f"<div>{label}) {option}</div>"
                        for label, option in zip(labels, question['options'])
                    )
                    options_html = f'<div style="margin-left:16px;">{option_items}</div>'
                elif question['question_type'] == 'Dogru/Yanlis':
                    options_html = '<div style="margin-left:16px;">D) Dogru &nbsp;&nbsp; Y) Yanlis</div>'
                else:
                    options_html = f"<div><strong>Secenekler:</strong> {' / '.join(question['options'])}</div>"

            image_html = ''
            if question.get('image_bytes'):
                encoded = base64.b64encode(question['image_bytes']).decode('utf-8')
                image_html = f'<div><img src="data:image/png;base64,{encoded}" style="max-width:480px;"/></div>'

            outcome_html = ''
            if question.get('outcomes'):
                outcome_html = f"<div><strong>Kazanim/Ogrenme:</strong> {', '.join(question['outcomes'])}</div>"

            question_blocks.append(
                f"""
                <div style="margin-bottom: 12px;">
                    <div><strong>{question_no}.</strong> {display_question_text(question)}</div>
                    {options_html}
                    {image_html}
                    {outcome_html}
                </div>
                """
            )
            question_no += 1
        question_blocks.append(
            "<div style=\"text-align:center; font-size:12px; margin-top:8px;\">"
            "Bu dersin sinavi bitti, yeni sinava geciniz."
            "</div>"
        )
    if subject_groups:
        question_blocks.append(
            "<div style=\"text-align:center; font-size:12px; margin-top:12px;\">Sınav bitti.</div>"
        )

    items = sorted(subject_counts.items())
    half = (len(items) + 1) // 2
    left = items[:half]
    right = items[half:]
    subject_rows = ''
    for idx in range(max(len(left), len(right))):
        left_subject, left_count = ('', '') if idx >= len(left) else left[idx]
        right_subject, right_count = ('', '') if idx >= len(right) else right[idx]
        subject_rows += (
            '<tr>'
            f'<td>{display_subject_label(left_subject)}</td><td style="text-align:center;">{left_count}</td>'
            f'<td>{display_subject_label(right_subject)}</td><td style="text-align:center;">{right_count}</td>'
            '</tr>'
        )

    rules_html = ''.join(f'<li>{rule}</li>' for rule in rules)

    topic_sections = ''
    if topic_map:
        parts = []
        for subject, entries in topic_map.items():
            display_subject = display_subject_label(subject)
            rows = ''.join(
                f'<tr><td style="width:60px;">{number}</td><td>{topic}</td></tr>'
                for number, topic in entries
            )
            parts.append(
                f"""
                <div style="margin-bottom: 16px;">
                    <div style="font-weight: 700; margin-bottom: 6px;">{display_subject}</div>
                    <table style="width:100%; border-collapse: collapse;" border="1" cellspacing="0" cellpadding="4">
                        <thead>
                            <tr><th style="width:60px;">Soru No</th><th>Konu</th></tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>
                """
            )
        topic_sections = f"""
            <div style="page-break-after: always;">
                <h3>Konu Dagilimi</h3>
                {''.join(parts)}
            </div>
        """
    topic_break = '<div style="page-break-after: always;"></div>' if topic_sections else ''

    return f"""
    <html>
        <head>
            <meta charset="utf-8" />
            <title>{exam['exam_name']}</title>
            <style>
                body {{ font-family: "Segoe UI", "Arial", sans-serif; }}
                h2, h3 {{ font-family: "Segoe UI", "Arial", sans-serif; }}
            </style>
        </head>
        <body>
            <div style="background: {primary}; color: #ffffff; padding: 16px; margin-bottom: 16px; border-bottom: 6px solid {secondary};">
                <table style="width:100%;">
                    <tr>
                        <td style="width:60%; vertical-align: top;">
                            {cover_logo_html}
                            <h2 style="color: #ffffff; margin: 8px 0;">{school_name_html}</h2>
                            <div style="color: #ffffff;"><strong>{exam['exam_type'].upper()}</strong></div>
                            <div style="font-weight:700;">{exam['grade']}. SINIF</div>
                            <div>{exam['exam_name']}</div>
                            <div style="margin-top:4px;"><strong>Sinav Kodu:</strong> {exam.get('exam_code', '')}</div>
                        </td>
                        <td style="width:40%; vertical-align: top; text-align:right;">
                            {cover_qr_html}
                            <div style="margin-top:2px;"><strong>Sinav Kodu:</strong> {exam.get('exam_code', '')}</div>
                            <div><strong>Kitapcik Tipi:</strong> {exam.get('booklet_type', 'A')}</div>
                            <div><strong>Sure:</strong> {exam['duration']} dk</div>
                        </td>
                    </tr>
                </table>
            </div>
            <table style="width:100%; margin-bottom: 12px;">
                <tr><td style="width:180px;"><strong>Adi ve Soyadi</strong></td><td>____________________________</td></tr>
                <tr><td><strong>Sinifi / Sube / Numara</strong></td><td>____________________________</td></tr>
            </table>
            <div style="margin-top: 12px;">
                <strong>Ders - Soru Sayisi</strong>
                <table style="width:100%; border-collapse: collapse; margin-top: 6px;" border="1" cellspacing="0" cellpadding="4">
                    <thead>
                        <tr>
                            <th>Ders</th><th style="width:80px;">Soru</th>
                            <th>Ders</th><th style="width:80px;">Soru</th>
                        </tr>
                    </thead>
                    <tbody>{subject_rows}</tbody>
                </table>
            </div>
            <div style="margin-top: 12px;">
                <strong>Adaylarin Dikkatine!</strong>
                <ol>{rules_html}</ol>
            </div>
            <div style="page-break-after: always;"></div>
            {topic_sections}
            {topic_break}
            {''.join(question_blocks)}
        </body>
    </html>
    """


def build_answer_key_doc_html(exam: dict) -> str:
    rows = []
    question_no = 1
    for subject, questions in group_questions_by_subject(exam):
        display_subject = display_subject_label(subject)
        rows.append(
            f'<tr><th colspan="3" style="text-align:left; background:#f2f2f2;">{display_subject}</th></tr>'
        )
        for question in questions:
            answer = question.get('answer', '') or '-'
            rows.append(
                f'<tr><td style="width:60px;">{question_no}</td>'
                f'<td style="width:120px;">{question.get("question_type","")}</td>'
                f"<td>{answer}</td></tr>"
            )
            question_no += 1
    rows_html = "\n".join(rows)
    return f"""
    <html>
        <head>
            <meta charset="utf-8" />
            <title>{exam['exam_name']} - Cevap Anahtari</title>
            <style>
                body {{ font-family: "Segoe UI", "Arial", sans-serif; }}
                h2 {{ font-family: "Segoe UI", "Arial", sans-serif; }}
            </style>
        </head>
        <body>
            <h2>{exam.get('school_name', '')}</h2>
            <div><strong>Sinav Adi:</strong> {exam['exam_name']}</div>
            <div><strong>Sinav Kodu:</strong> {exam.get('exam_code', '')}</div>
            <div><strong>Sinif/Sube:</strong> {exam['grade']}/{exam['section']}</div>
            <div><strong>Sinav Turu:</strong> {exam['exam_type']}</div>
            <hr />
            <table style="width:100%; border-collapse: collapse;" border="1" cellspacing="0" cellpadding="4">
                <thead>
                    <tr><th>No</th><th>Soru Tipi</th><th>Cevap</th></tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </body>
    </html>
    """
# ==================== RENDER ====================

def render_question_bank() -> None:
    if not st.session_state.gen01_auto_imported:
        gen01_csvs = find_gen01_output_csvs(st.session_state.tenant_name)
        if gen01_csvs:
            all_items = []
            all_errors = []
            for csv_path in gen01_csvs:
                items, errors = import_questions_from_csv(csv_path)
                all_items.extend(items)
                all_errors.extend(errors)
            add_to_question_bank(all_items)
            st.session_state.gen01_auto_imported = True
            st.info(f"GEN-01 ciktilari otomatik yuklendi: {len(all_items)} soru.")
            if all_errors:
                err_df = pd.DataFrame(all_errors)
                st.dataframe(err_df, use_container_width=True)
    if not st.session_state.question_bank:
        st.info("Soru bankasi bos. Yukleme veya manuel giris yapin.")
        return

    rows = []
    for question in st.session_state.question_bank:
        outcomes = question.get("outcomes", [])
        outcome_preview = ""
        if outcomes:
            outcome_preview = outcomes[0][:80]
            if len(outcomes) > 1:
                outcome_preview = f"{outcome_preview} (+)"
        rows.append(
            {
                "ID": question["id"],
                "Sınıf": question["grade"],
                "Ders": display_subject_label(question.get("subject", "")),
                "Soru Tipi": question["question_type"],
                "Kazanım/Ogrenme": outcome_preview,
                "Kaynak": question["source"],
                "Zorluk": question.get("difficulty", ""),
                "Kalite": question.get("quality_score", 0),
                "Soru": question["text"][:120],
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Havuzu CSV indir",
        data=csv_bytes,
        file_name="question_bank.csv",
        mime="text/csv",
        key="download_bank_csv",
    )

    with st.expander("CSV ile soru havuzu yukle", expanded=False):
        uploaded_csv = st.file_uploader(
            "CSV secin",
            type=["csv"],
            key="question_bank_csv_upload",
        )
        if uploaded_csv is not None:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded_csv, allowed_types=["csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded_csv = None
        if st.button("CSV’den sorulari yukle"):

            if uploaded_csv is None:
                st.warning("CSV seçilmedi.")
            else:
                temp_path = os.path.join("data", "temp_questions.csv")
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                with open(temp_path, "wb") as handle:
                    handle.write(uploaded_csv.getbuffer())
                items, errors = import_questions_from_csv(temp_path)
                add_to_question_bank(items)
                st.success(f"{len(items)} soru yuklendi.")
                if errors:
                    err_df = pd.DataFrame(errors)
                    st.dataframe(err_df, use_container_width=True)
                    err_csv = err_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Hata raporu indir (CSV)",
                        data=err_csv,
                        file_name="question_import_errors.csv",
                        mime="text/csv",
                        key="download_import_errors_csv",
                    )
        if st.button("Klasor paketinden yukle (hepsi)"):

            csv_paths = find_import_csvs_for_tenant(st.session_state.tenant_name)
            if not csv_paths:
                st.warning("Tenant için paket CSV bulunamadı.")
            else:
                all_items = []
                all_errors = []
                for csv_path in csv_paths:
                    items, errors = import_questions_from_csv(csv_path)
                    all_items.extend(items)
                    all_errors.extend(errors)
                add_to_question_bank(all_items)
                st.success(f"{len(all_items)} soru yuklendi: {', '.join(os.path.basename(p) for p in csv_paths)}")
                if all_errors:
                    err_df = pd.DataFrame(all_errors)
                    st.dataframe(err_df, use_container_width=True)
                    err_csv = err_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Hata raporu indir (CSV)",
                        data=err_csv,
                        file_name="question_import_errors.csv",
                        mime="text/csv",
                        key="download_import_errors_csv_folder",
                    )
        if st.button("GEN-01 ciktilarini havuza aktar"):

            gen01_csvs = find_gen01_output_csvs(st.session_state.tenant_name)
            if not gen01_csvs:
                st.warning("GEN-01 cikti CSV bulunamadı.")
            else:
                all_items = []
                all_errors = []
                for csv_path in gen01_csvs:
                    items, errors = import_questions_from_csv(csv_path)
                    all_items.extend(items)
                    all_errors.extend(errors)
                add_to_question_bank(all_items)
                st.success(f"{len(all_items)} soru yuklendi (GEN-01).")
                if all_errors:
                    err_df = pd.DataFrame(all_errors)
                    st.dataframe(err_df, use_container_width=True)
                    err_csv = err_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Hata raporu indir (CSV)",
                        data=err_csv,
                        file_name="question_import_errors_gen01.csv",
                        mime="text/csv",
                        key="download_import_errors_csv_gen01",
                    )

    with st.expander("Uretim Plani (LSE-100) ile havuz olustur", expanded=False):
        plan_path = find_generation_plan_csv(st.session_state.tenant_name)
        # Quick check: is there at least one import CSV?
        _first_csv = find_import_csv_for_tenant(st.session_state.tenant_name)
        csv_paths = find_import_csvs_for_tenant(st.session_state.tenant_name)
        if csv_paths:
            st.caption(f"Soru CSV bulundu: {', '.join(os.path.basename(p) for p in csv_paths)}")
        if plan_path:
            st.caption(f"Plan bulundu: {plan_path}")
        else:
            st.caption("Plan bulunamadı. LSE-100_TamPaket klasorunu kontrol edin.")
        if st.button("Tam paketi uygula (hepsi)"):

            if not csv_paths and not plan_path:
                st.warning("Paket için CSV veya plan bulunamadı.")
            else:
                all_items = []
                all_errors = []
                if csv_paths:
                    for csv_path in csv_paths:
                        items, errors = import_questions_from_csv(csv_path)
                        all_items.extend(items)
                        all_errors.extend(errors)
                    add_to_question_bank(all_items)
                if plan_path:
                    plan = import_generation_plan_from_csv(plan_path)
                    save_generation_plan(st.session_state.tenant_name, plan)
                st.success("Tam paket uygulandi.")
                if all_errors:
                    err_df = pd.DataFrame(all_errors)
                    st.dataframe(err_df, use_container_width=True)
                    err_csv = err_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Hata raporu indir (CSV)",
                        data=err_csv,
                        file_name="question_import_errors.csv",
                        mime="text/csv",
                        key="download_import_errors_csv_allinone",
                    )
        if st.button("Plani yukle"):

            if not plan_path:
                st.warning("Plan dosyasi bulunamadı.")
            else:
                plan = import_generation_plan_from_csv(plan_path)
                save_generation_plan(st.session_state.tenant_name, plan)
                st.success(f"Plan yuklendi. Outcome sayisi: {len(plan)}")
        plan = load_generation_plan(st.session_state.tenant_name)
        st.caption(f"Kalan outcome: {len(plan)}")
        available_subjects = sorted({item.get("subject", "") for item in plan if item.get("subject")})
        subject_filter = st.multiselect(
            "Yalnizca bu derslerde uret",
            available_subjects,
            default=[],
        )
        max_questions = st.number_input(
            "Bu sefer uretilecek toplam soru limiti",
            min_value=10,
            max_value=5000,
            value=200,
            step=10,
        )
        use_ai_plan = st.checkbox("Bu uretimde AI kullan", value=st.session_state.exam_mode.startswith("Otomatik"))

        min_quality = st.slider(
            "Minimum kalite skoru",
            min_value=0,
            max_value=100,
            value=40,
            step=5,
        )
        auto_batches = st.number_input(
            "Otomatik devam batch sayisi",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
        )
        if st.button("Plani calistir (batch)"):

            if not plan:
                st.warning("Plan bos. Önce plan yukleyin.")
            else:
                produced = []
                remaining_plan = []
                total_generated = 0
                progress = st.progress(0.0, text="Plan batch uretimi devam ediyor...")
                batches_done = 0
                current_plan = plan[:]
                while current_plan and batches_done < auto_batches:
                    batch_generated = 0
                    for item in current_plan:
                        if batch_generated >= max_questions:
                            remaining_plan.append(item)
                            continue
                        if subject_filter and item.get("subject") not in subject_filter:
                            remaining_plan.append(item)
                            continue
                        outcome = {
                            "id": item.get("outcome_uid"),
                            "grade": item["grade"],
                            "subject": item["subject"],
                            "outcome": item["outcome_text"],
                        }
                        remaining = {
                            "mcq": int(item.get("mcq", 0) or 0),
                            "tf": int(item.get("tf", 0) or 0),
                            "blank": int(item.get("blank", 0) or 0),
                            "open": int(item.get("open", 0) or 0),
                            "classic": int(item.get("classic", 0) or 0),
                        }
                        type_map = [
                            ("Çoktan Secmeli (ABCD)", "mcq"),
                            ("Dogru/Yanlis", "tf"),
                            ("Bosluk Doldurma", "blank"),
                            ("Açık Uclu", "open"),
                            ("Klasik", "classic"),
                        ]
                        for qtype, key in type_map:
                            count = remaining.get(key, 0)
                            for _ in range(count):
                                if batch_generated >= max_questions:
                                    break
                                question = generate_random_question(
                                    item["grade"],
                                    qtype,
                                    subject=item["subject"],
                                    outcome=outcome,
                                    use_ai=use_ai_plan,
                                    difficulty="medium",
                                    force_graph=False,
                                )
                                if compute_quality_score(question) >= min_quality:
                                    produced.append(question)
                                    batch_generated += 1
                                    total_generated += 1
                                remaining[key] = max(remaining[key] - 1, 0)
                                progress.progress(min(total_generated / (max_questions * auto_batches), 1.0))
                        if sum(remaining.values()) > 0:
                            updated = dict(item)
                            updated["mcq"] = remaining["mcq"]
                            updated["tf"] = remaining["tf"]
                            updated["blank"] = remaining["blank"]
                            updated["open"] = remaining["open"]
                            updated["classic"] = remaining["classic"]
                            remaining_plan.append(updated)
                    current_plan = remaining_plan
                    remaining_plan = []
                    batches_done += 1
                progress.empty()
                add_to_question_bank(produced)
                save_generation_plan(st.session_state.tenant_name, current_plan)
                st.success(f"{total_generated} soru uretildi ve havuza eklendi.")


def render_ai_question_creator() -> None:
    st.subheader("Yapay Zeka ile Soru Hazırlama")
    st.caption("OPENAI_API_KEY tanımlı ise AI'yi kullanarak anlık soru üretin ve sonucu kopyalayın.")

    subject_choices = get_subjects_from_outcomes() or DEFAULT_SUBJECTS
    st.session_state.setdefault("ai_question_subject", subject_choices[0])
    question_type_choices = st.session_state.question_types or DEFAULT_QUESTION_TYPES
    st.session_state.setdefault("ai_question_type", question_type_choices[0])
    st.session_state.setdefault("ai_question_grade", 9)
    st.session_state.setdefault("ai_question_difficulty", "medium")
    st.session_state.setdefault("ai_question_outcome", "Bir kazanım veya öğrenme çıktısı yazın.")

    difficulty_options = ["kolay", "medium", "zor"]

    with st.form("ai_question_form"):
        grade = st.slider(
            "Sınıf",
            min_value=4,
            max_value=12,
            value=max(4, min(12, st.session_state.ai_question_grade)),
            key="ai_question_grade",
        )
        subject = st.selectbox(
            "Ders",
            subject_choices,
            index=subject_choices.index(st.session_state.ai_question_subject)
            if st.session_state.ai_question_subject in subject_choices
            else 0,
            key="ai_question_subject",
        )
        qtype = st.selectbox(
            "Soru Türü",
            question_type_choices,
            index=question_type_choices.index(st.session_state.ai_question_type)
            if st.session_state.ai_question_type in question_type_choices
            else 0,
            key="ai_question_type",
        )
        difficulty = st.selectbox(
            "Zorluk",
            difficulty_options,
            index=difficulty_options.index(st.session_state.ai_question_difficulty)
            if st.session_state.ai_question_difficulty in difficulty_options
            else 1,
            key="ai_question_difficulty",
        )
        outcome_text = st.text_area(
            "Kazanım / Açıklama",
            value=st.session_state.ai_question_outcome,
            key="ai_question_outcome",
            height=100,
            help="Bu kazanım AI prompt'unun temelini oluşturur.",
        )
        submitted = st.form_submit_button("AI ile soru oluştur")

    question_count = st.slider(
        "Üretilecek Soru Sayısı",
        min_value=1,
        max_value=10,
        value= st.session_state.get("ai_question_count", 5),
        key="ai_question_count",
    )
    include_diagram = st.checkbox(
        "Şekilli soru iste", value=True, key="ai_question_include_diagram"
    )

    if submitted:
        st.session_state.ai_last_error = ""
        try:
            payload = GenerationRequest(
                grade=grade,
                subject=subject,
                question_types=[qtype],
                difficulty=difficulty,
                question_count=question_count,
                include_diagram=include_diagram,
                outcome_text=outcome_text or "Genel kazanım",
            )
            result = generate_question_batch(payload)
            st.session_state.ai_question_result = result
        except Exception as exc:
            st.session_state.ai_question_result = None
            st.session_state.ai_last_error = str(exc)
            result = None
        st.session_state.ai_question_prompt = outcome_text
    else:
        result = st.session_state.ai_question_result

    if st.session_state.ai_last_error:
        st.error(st.session_state.ai_last_error)
    elif isinstance(result, GenerationResult) and result.questions:
        st.markdown("**Üretilen Sorular**")
        for idx, question in enumerate(result.questions, start=1):
            st.markdown(f"**{idx}. {question.text}**")
            if question.options:
                st.caption("Seçenekler: " + " / ".join(question.options))
            st.write(f"Cevap: {question.answer}")
            if question.diagram_spec:
                st.caption("Diagram spec: " + question.diagram_spec)
            if question.supporting_hint:
                st.caption("Ipucu: " + question.supporting_hint)
            st.divider()
        if result.rendered_pdf_base64:
            pdf_bytes = base64.b64decode(result.rendered_pdf_base64)
            st.download_button(
                "PDF olarak indir",
                data=pdf_bytes,
                file_name="ai_sorular.pdf",
                mime="application/pdf",
                key="ai_question_pdf_download",
            )


def render_question_builder() -> None:
    """Ana soru olusturma fonksiyonu - yeni modern arayuz kullanir."""
    inject_common_css("qbm")
    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("question_builder_egitim_yili")

    # Yeni modern arayuzu kullan (fallback: render_question_builder_legacy)
    try:
        from views.question_builder._ui_new import render_question_builder_new
        render_question_builder_new()
    except ImportError:
        render_question_builder_legacy()


def render_question_builder_legacy() -> None:
    """Eski arayuz (geriye donuk uyumluluk için saklanmistir)."""
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            font-family: "Segoe UI", "Arial", sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    styled_header("Soru Olusturma Modulu", "Sinif, sinav turu, soru tipi ve kazanim/ogrenme ciktilarina gore sinav olusturun", icon="✏️")

    init_question_state()
    if not st.session_state.builder_started:
        st.subheader("Oluştur/Indir")
        st.info("İşleme baslamak için once Oluştur/Indir butonuna tiklayin.")
        if st.button("Oluştur/Indir", key="builder_start_btn"):
            st.session_state.builder_started = True
            st.rerun()
        return
    # Tab tamamlanma durumlarini kontrol et
    has_subjects = bool(st.session_state.get("selected_subjects"))
    has_question_counts = sum(st.session_state.get("subject_question_counts", {}).values()) > 0

    # Tab etiketlerini tamamlanma durumuna gore olustur
    tab_labels = [
        "Tenant & Kapak",
        "Sınav Turu",
        "Sınıf/Şube",
        f"Dersler {'OK' if has_subjects else '(!)'}" if st.session_state.builder_started else "Dersler",
        "Soru Turu",
        "Zorluk",
        f"Soru Sayısı {'OK' if has_question_counts else '(!)'}" if (st.session_state.builder_started and has_subjects) else "Soru Sayısı",
        "Sure",
        "Uygulama/Yukle",
        "Yeni PDF Ekle",
        "Soru Bankasi",
        "Öğrenci",
        "Oluştur/Indir",
        "AI Destek",
    ]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        st.subheader("Tenant Secimi")
        tenants = list_tenants()
        selected_tenant = st.selectbox(
            "Okul/Tenant",
            tenants,
            index=tenants.index(st.session_state.tenant_name) if st.session_state.tenant_name in tenants else 0,
            key="tenant_selector",
        )
        if selected_tenant != st.session_state.tenant_name:
            st.session_state.tenant_name = selected_tenant
            st.rerun()
        new_tenant = st.text_input("Yeni tenant adi", key="new_tenant_name")
        if st.button("Yeni tenant olustur"):

            cleaned = new_tenant.strip()
            if cleaned:
                create_tenant(cleaned)
                st.session_state.tenant_name = cleaned
                st.rerun()
            else:
                st.warning("Gecerli bir tenant adi girin.")

        render_cover_settings()


    with tabs[1]:
        st.subheader("Sınav Turu")
        st.session_state.exam_types = [
            "Deneme Sınavı",
            "TYT",
            "AYT EA",
            "AYT SAY",
            "AYT SOZ",
            "LGS",
            "Okul Yazilisi",
            "Bursluluk Sınavı",
            "Seviye Tespit Sınavı",
        ]
        available_exam_types = list(dict.fromkeys(st.session_state.exam_types))
        selected_exam_types = []
        for idx, exam_type in enumerate(available_exam_types):
            if st.checkbox(exam_type, key=f"exam_type_{idx}"):
                selected_exam_types.append(exam_type)
        st.session_state.selected_exam_types = selected_exam_types


    with tabs[2]:
        st.subheader("Sınıf ve Şube")
        level_options = {
            "İlkokul": [1, 2, 3, 4],
            "Ortaokul": [5, 6, 7, 8],
            "Lise": [9, 10, 11, 12],
        }
        tyt_or_ayt = any(
            t in {"TYT", "AYT", "AYT EA", "AYT SAY", "AYT SOZ"}
            for t in st.session_state.selected_exam_types
        )
        if tyt_or_ayt:
            st.session_state.selected_level = "Lise"
            st.write("Kademeyi secin: Lise")
            grade_options = [11, 12]
            selected_grades = st.multiselect(
                "Sınıf secimi",
                grade_options,
                default=[11, 12],
                key="selected_grades",
            )
            if selected_grades:
                st.session_state.selected_grade = selected_grades[0]
        else:
            st.session_state.selected_level = st.radio(
                "Kademeyi secin",
                list(level_options.keys()),
                index=list(level_options.keys()).index(st.session_state.selected_level),
                horizontal=True,
            )
            grade_options = level_options[st.session_state.selected_level]
            st.session_state.selected_grade = st.selectbox(
                "Sınıf secimi",
                grade_options,
                index=grade_options.index(st.session_state.selected_grade)
                if st.session_state.selected_grade in grade_options
                else 0,
            )
        section_options = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "İ", "J", "K", "L", "M", "N", "Ş"
        ]
        selected_sections = st.multiselect(
            "Şube secimi",
            section_options,
            default=[st.session_state.selected_section]
            if st.session_state.selected_section in section_options
            else [section_options[0]],
            key="selected_sections",
        )
        if selected_sections:
            st.session_state.selected_section = selected_sections[0]


    with tabs[3]:
        st.subheader("Dersler")
        subject_options = [subject for subject in get_subjects_from_outcomes() if not is_excluded_subject(subject)]
        subject_options = list(dict.fromkeys(subject_options))
        if st.session_state.get("exam_mode", "").startswith("Disardan") and not st.session_state.pdf_subjects_prefilled:
            for idx, subject in enumerate(subject_options):
                st.session_state[f"subject_{subject_key(subject)}_{idx}"] = True
            st.session_state.pdf_subjects_prefilled = True
            st.rerun()
        selected_subjects = []
        col_select, col_clear = st.columns(2)
        with col_select:
            select_all = st.checkbox("Tüm dersleri sec", key="select_all_subjects")
        with col_clear:
            clear_all = st.checkbox("Tüm secimleri kaldir", key="clear_all_subjects")
        if select_all:
            for idx, subject in enumerate(subject_options):
                st.session_state[f"subject_{subject_key(subject)}_{idx}"] = True
        if clear_all:
            for idx, subject in enumerate(subject_options):
                st.session_state[f"subject_{subject_key(subject)}_{idx}"] = False
        for idx, subject in enumerate(subject_options):
            label = display_subject_label(subject)
            if st.checkbox(label, key=f"subject_{subject_key(subject)}_{idx}"):
                selected_subjects.append(subject)
        st.session_state.selected_subjects = selected_subjects


    with tabs[4]:
        st.subheader("Soru Turu")
        tyt_selected = any(
            exam_type.strip().lower() == "tyt"
            for exam_type in st.session_state.selected_exam_types
        )
        pdf_only = st.session_state.bank_source_filter == "pdf_only"
        question_type_options = [
            "Çoktan Secmeli (ABCDE)",
            "Dogru/Yanlis",
            "Bosluk Doldurma",
            "Açık Uclu",
            "Klasik",
        ]
        selected_question_types = []
        for idx, qtype in enumerate(question_type_options):
            default_checked = qtype.startswith("Çoktan Secmeli (ABCDE)")
            if st.checkbox(qtype, value=default_checked, key=f"qtype_{idx}"):
                selected_question_types.append(qtype)
        st.session_state.selected_question_types = selected_question_types


    with tabs[5]:
        st.subheader("Zorluk Seviyesi")
        st.session_state.selected_difficulty = st.selectbox(
            "Zorluk",
            ["Karisik", "Kolay", "Orta", "Zor"],
            index=["Karisik", "Kolay", "Orta", "Zor"].index(st.session_state.selected_difficulty),
        )


    with tabs[6]:
        st.subheader("Ders Bazli Soru Sayısı")
        subject_counts = {}
        if not st.session_state.selected_subjects:
            st.caption("Önce ders secin.")
        else:
            bulk_value = st.number_input(
                "Tüm dersler için ayni soru sayisi",
                min_value=0,
                max_value=1000,
                value=0,
                key="bulk_subject_count",
            )
            col_bulk_1, col_bulk_2 = st.columns(2)
            with col_bulk_1:
                apply_bulk = st.button("Tüm derslere uygula")

            with col_bulk_2:
                apply_500 = st.button("Ders basi 500 uygula")

            if apply_500:
                bulk_value = 500
                apply_bulk = True
            if apply_bulk:
                for subject in st.session_state.selected_subjects:
                    count_value = int(bulk_value)
                    st.session_state.subject_question_counts[subject] = count_value
                    st.session_state[f"subject_count_{subject_key(subject)}"] = count_value
                st.success("Tüm derslere uygulandi.")
                st.rerun()
            for subject in st.session_state.selected_subjects:
                default_value = st.session_state.subject_question_counts.get(subject, 0)
                subject_counts[subject] = st.number_input(
                    f"{display_subject_label(subject)} soru sayisi",
                    min_value=0,
                    max_value=1000,
                    value=int(default_value),
                    key=f"subject_count_{subject_key(subject)}",
                )
            total_questions = sum(subject_counts.values())
            if total_questions == 0:
                st.warning("Dikkat: Toplam soru sayisi 0. Lutfen en az bir ders için soru sayisi girin.")
            else:
                st.info(f"Toplam soru sayisi: {total_questions}")
        st.session_state.subject_question_counts = subject_counts


    with tabs[7]:
        st.subheader("Sınav Suresi (dk)")
        st.session_state.exam_duration = st.number_input(
            "Sure",
            min_value=5,
            max_value=180,
            value=int(st.session_state.get("exam_duration", 40)),
            key="exam_duration_input",
        )


    with tabs[8]:
        st.subheader("Sınav Uygulamasi")
        exam_mode = st.radio(
            "Sınav olusturma modu",
            [
                "Otomatik (AI destekli)",
                "Otomatik (AI desteksiz)",
                "Manuel (kazanımlar secilerek)",
            ],
            index=0,
        )
        st.session_state.exam_mode = exam_mode
        source_choice = st.radio(
            "Soru kaynagi",
            ["Tüm kaynaklar", "Sadece PDF yuklenenler"],
            index=0 if st.session_state.bank_source_filter == "all" else 1,
        )
        st.session_state.bank_source_filter = "all" if source_choice.startswith("Tüm") else "pdf_only"
        if st.session_state.bank_source_filter == "pdf_only":
            st.info("PDF secildi: AI/rasgele uretim kullanilmaz, sadece yuklenen PDF sorulari gelir.")
        if exam_mode == "Otomatik (AI desteksiz)":
            st.session_state.use_bank_questions = True
        if exam_mode.startswith("Otomatik (AI destekli)") and st.session_state.ai_last_error:
            st.error(f"AI hata: {st.session_state.ai_last_error}")
            if st.button("Hatayi temizle", key="clear_ai_error"):
                st.session_state.ai_last_error = ""
                st.rerun()
        st.session_state.fast_graph_mode = st.checkbox(
            "Hızlı gorsel uretim (dusuk kalite, daha hizli)",
            value=st.session_state.fast_graph_mode,
        )
        st.session_state.store_generated_questions = st.checkbox(
            "Oluşturulan sorulari havuza ekle",
            value=st.session_state.store_generated_questions,
        )
        st.session_state.use_bank_questions = True
        st.checkbox(
            "Sınav için havuzdan soru kullan (sabit)",
            value=True,
            disabled=True,
        )
        st.session_state.bank_min_score = st.slider(
            "Havuz kalite filtresi (min skor)",
            min_value=0,
            max_value=100,
            value=int(st.session_state.bank_min_score),
            step=5,
        )


    with tabs[9]:
        render_pdf_question_importer(embedded=True)


    with tabs[10]:
        st.subheader("Soru Bankasi")
        render_question_bank()

        st.divider()
        if st.session_state.exam_mode.startswith("Manuel"):
            render_outcomes_selector()


    with tabs[11]:
        st.subheader("Öğrenci Listesi")
        with st.form("student_form"):
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                student_name = st.text_input("Adi Soyadi", key="student_name")
            with col_s2:
                student_class = st.text_input("Sınıfı/Şube", key="student_class")
            with col_s3:
                student_id = st.text_input("Okul No / ID", key="student_id")
            add_student = st.form_submit_button("Öğrenci Ekle")
            if add_student:
                cleaned_id = student_id.strip()
                if not cleaned_id:
                    st.warning("Öğrenci ID zorunlu.")
                else:
                    st.session_state.student_list.append(
                        {
                            "id": cleaned_id,
                            "name": student_name.strip(),
                            "class": student_class.strip(),
                        }
                    )
                    st.session_state.student_name = ""
                    st.session_state.student_class = ""
                    st.session_state.student_id = ""
                    st.success("Öğrenci eklendi.")

        if st.session_state.student_list:
            student_df = pd.DataFrame(st.session_state.student_list)
            st.dataframe(student_df, use_container_width=True)
            class_options = sorted({item.get("class", "") for item in st.session_state.student_list if item.get("class")})
            if class_options:
                selected_classes = st.multiselect(
                    "Sınıf listeleri",
                    class_options,
                    default=class_options[:1],
                    key="student_class_filter",
                )
            else:
                selected_classes = []
            filtered_students = [
                s for s in st.session_state.student_list
                if not selected_classes or s.get("class") in selected_classes
            ]
            st.markdown("**Sınıf listesi (tikleyin):**")
            selected_ids = []
            for student in filtered_students:
                sid = student.get("id", "")
                label = f"{sid} - {student.get('name','')}"
                default_checked = sid in (st.session_state.selected_student_ids or [s['id'] for s in filtered_students])
                if st.checkbox(label, value=default_checked, key=f"student_select_{sid}"):
                    selected_ids.append(sid)
            st.session_state.selected_student_ids = selected_ids
            st.caption(f"Secili ogrenci sayisi: {len(selected_ids)}")
        else:
            st.info("Henuz ogrenci girilmedi.")

        if st.button("Ornek ogrenci ekle (9A-12A, her sinifa 5 kisi)"):

            first_names = ["Ali", "Ayse", "Mehmet", "Zeynep", "Ahmet", "Elif", "Can", "Ece"]
            last_names = ["Yilmaz", "Kaya", "Demir", "Celik", "Sahin", "Yildiz", "Arslan", "Tas"]
            existing_ids = {item.get("id") for item in st.session_state.student_list}
            for grade in [9, 10, 11, 12]:
                for idx in range(1, 6):
                    sid = f"{grade}A-{idx:02d}"
                    if sid in existing_ids:
                        continue
                    name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    st.session_state.student_list.append(
                        {
                            "id": sid,
                            "name": name,
                            "class": f"{grade}/A",
                        }
                    )
                    existing_ids.add(sid)
            st.success("Ornek ogrenciler eklendi.")


    with tabs[12]:
        st.subheader("Sınav Oluştur")

        api_key = get_openai_api_key()

        def render_downloads(exam: dict, key_suffix: str) -> None:
            st.markdown("### Indir")
            ensure_exam_visuals(exam)
            pdf_bytes = build_exam_pdf(exam)
            if pdf_bytes:
                st.download_button(
                    "PDF indir",
                    data=pdf_bytes,
                    file_name=f"{exam['exam_name']}.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_{key_suffix}",
                )
            else:
                st.error("PDF olusturulamadi. Lutfen tekrar deneyin.")

            answer_doc_html = build_answer_key_doc_html(exam)
            st.download_button(
                "Cevap anahtari (Word)",
                data=answer_doc_html.encode("utf-8"),
                file_name=f"{exam['exam_name']}_cevap_anahtari.doc",
                mime="application/msword",
                key=f"download_answer_doc_{key_suffix}",
            )

            doc_html = build_exam_doc_html(exam)
            st.download_button(
                "Word indir",
                data=doc_html.encode("utf-8"),
                file_name=f"{exam['exam_name']}.doc",
                mime="application/msword",
                key=f"download_doc_{key_suffix}",
            )
            # Plain text export
            exam_txt = build_exam_text(exam)
            st.download_button(
                "TXT indir",
                data=exam_txt.encode("utf-8"),
                file_name=f"{exam['exam_name']}.txt",
                mime="text/plain",
                key=f"download_txt_{key_suffix}",
            )
            st.markdown("### Cevap Formu (Optik)")
            default_list = _serialize_student_list(st.session_state.student_list)
            student_raw = st.text_area(
                "Öğrenci listesi (ID, Ad Soyad, Sınıf/Şube) - her satira 1 ogrenci",
                value=default_list,
                key=f"student_list_{key_suffix}",
                placeholder="12345, Ayse Yilmaz, 9/A",
            )
            students = _parse_student_list(student_raw)
            if students:
                default_selected = st.session_state.selected_student_ids or [s["id"] for s in students]
                selected_ids = st.multiselect(
                    "Cevap formu olusturulacak ogrenciler",
                    [s["id"] for s in students],
                    default=default_selected,
                    key=f"student_select_{key_suffix}",
                )
                students = [s for s in students if s.get("id") in set(selected_ids)]
            if not students:
                st.info("Öğrenci listesi girilmezse bos cevap formu olusur.")
            form_pdf = build_answer_sheet_pdf(exam, students)
            if form_pdf:
                st.download_button(
                    "Cevap formu PDF indir",
                    data=form_pdf,
                    file_name=f"{exam['exam_name']}_cevap_formu.pdf",
                    mime="application/pdf",
                    key=f"download_answer_sheet_{key_suffix}",
                )

        if st.session_state.bank_source_filter == "pdf_only":
            st.subheader("Orijinal PDF indir")
            originals = list_original_pdfs(st.session_state.tenant_name)
            if originals:
                selected_original = st.selectbox(
                    "Orijinal PDF secin",
                    originals,
                    key="original_pdf_select",
                )
                original_path = os.path.join(
                    get_tenant_dir(st.session_state.tenant_name),
                    "uploads",
                    "originals",
                    selected_original,
                )
                if os.path.exists(original_path):
                    with open(original_path, "rb") as handle:
                        original_bytes = handle.read()
                    st.download_button(
                        "Orijinal PDF indir",
                        data=original_bytes,
                        file_name=selected_original,
                        mime="application/pdf",
                        key="download_original_pdf_btn",
                    )
            else:
                st.info("Orijinal PDF bulunamadı. Yukleme ekraninda 'Orjinal PDF'i koru' secmelisiniz.")

            st.divider()
        exam_name = st.text_input("Sınav Adi", key="exam_name")
        st.subheader("Puanlama")
        scoring_system = st.selectbox(
            "Puanlama sistemi",
            [100, 500],
            index=0,
            key="scoring_system",
        )
        auto_point = round(scoring_system / max(st.session_state.question_count, 1), 2)
        auto_mode = st.checkbox(
            "Soru basi puan otomatik hesaplansin",
            value=True,
            key="auto_point_mode",
        )
        if auto_mode:
            st.text_input(
                "Soru basi puan",
                value=str(auto_point),
                disabled=True,
                key="point_per_question_display",
            )
            point_per_question = auto_point
        else:
            point_per_question = st.number_input(
                "Soru basi puan",
                min_value=0.0,
                max_value=float(scoring_system),
                value=float(st.session_state.get("point_per_question", auto_point)),
                step=0.25,
                key="point_per_question",
            )

        col1, col2 = st.columns(2)
        with col1:
            grade = int(st.session_state.selected_grade)
            section = st.session_state.selected_section
            st.caption(f"Sınıf/Şube: {grade}/{section}")
        with col2:
            auto_total = sum(st.session_state.subject_question_counts.values())
            if auto_total <= 0:
                auto_total = int(st.session_state.get("question_count", 20))
            st.session_state.question_count = auto_total
            question_count = st.number_input(
                "Soru Sayısı (derslerden otomatik)",
                min_value=1,
                max_value=5000,
                value=int(auto_total),
                key="question_count",
                disabled=True,
            )
            duration = int(st.session_state.get("exam_duration", 40))

        if st.session_state.exam_mode.startswith("Manuel"):
            selected_outcomes = get_selected_outcomes_for_grade(grade)
            use_selected_outcomes = st.checkbox(
                "Secili kazanimlari kullan",
                value=bool(selected_outcomes),
                key="use_selected_outcomes",
            )
        else:
            selected_outcomes = []
            use_selected_outcomes = False

        use_ai = st.session_state.exam_mode.startswith("Otomatik (AI destekli)")

        submitted = st.button("Sınavı Oluştur", key="create_exam_bottom")

        if submitted:
            if not exam_name.strip():
                exam_name = f"Sınav {grade}-{section}"
                st.info("Sınav adi bos oldugu için otomatik atanmistir.")

            selected_exam_types = st.session_state.selected_exam_types or DEFAULT_EXAM_TYPES
            if not st.session_state.selected_exam_types:
                st.info("Sınav turu seçilmedi. Varsayilan turler kullanildi.")

            selected_question_types = st.session_state.selected_question_types or [
                "Çoktan Secmeli (ABCD)",
                "Çoktan Secmeli (ABCDE)",
                "Dogru/Yanlis",
                "Bosluk Doldurma",
                "Açık Uclu",
                "Klasik",
            ]
            if not st.session_state.selected_question_types:
                st.info("Soru tipi seçilmedi. Varsayilan tipler kullanildi.")

            subjects = st.session_state.selected_subjects or get_subjects_from_outcomes()
            subjects = [s for s in subjects if not is_excluded_subject(s)]

            if not subjects:
                st.error("Lutfen en az bir ders secin! Dersler sekmesinden ders secimi yapabilirsiniz.")
                st.stop()

            subject_counts = {
                subject: count
                for subject, count in st.session_state.subject_question_counts.items()
                if count > 0
            }

            bank_source_filter = st.session_state.bank_source_filter
            if st.session_state.exam_mode.startswith("Disardan") and st.session_state.pdf_external_use_pool:
                bank_source_filter = "pdf_only"
            if bank_source_filter == "pdf_only":
                use_ai = False
                st.session_state.use_bank_questions = True
                effective_types = normalize_question_types(selected_question_types)

                def is_pdf_source(source: str) -> bool:
                    return source == "pdf_image" or source.startswith("pdf_import")

                ayt_track = None
                if "AYT SAY" in selected_exam_types:
                    ayt_track = "say"
                elif "AYT EA" in selected_exam_types:
                    ayt_track = "ea"
                elif "AYT SOZ" in selected_exam_types:
                    ayt_track = "soz"

                def pdf_source_ok(question: dict) -> bool:
                    source = question.get("source", "")
                    if not is_pdf_source(source):
                        return False
                    if ayt_track:
                        return source == f"pdf_import_ayt_{ayt_track}" or source == "pdf_image"
                    if "TYT" in selected_exam_types:
                        return source == "pdf_import" or source == "pdf_image"
                    return True

                relax_grade = (("TYT" in selected_exam_types) or ayt_track) and bank_source_filter == "pdf_only"
                bank_candidates = [
                    q for q in st.session_state.question_bank
                    if pdf_source_ok(q)
                    and (q.get("grade") == grade or relax_grade)
                    and q.get("question_type") in effective_types
                ]
                if use_selected_outcomes and selected_outcomes:
                    selected_outcome_ids = {item["id"] for item in selected_outcomes}
                    bank_candidates = [
                        q for q in bank_candidates
                        if set(q.get("outcome_ids", [])) & selected_outcome_ids
                    ]
                desired_counts = {
                    subject: count
                    for subject, count in subject_counts.items()
                    if count > 0
                }
                desired_counts = distribute_subject_counts(subjects, question_count, desired_counts)
                missing = {}
                for subject, target in desired_counts.items():
                    available = sum(1 for q in bank_candidates if subject_matches_question(q, subject))
                    if available < target:
                        missing[subject] = {"istenen": target, "mevcut": available}
                if missing:
                    st.error("PDF havuzunda yeterli soru yok. Eksikler:")
                    rows = []
                    for subject, data in missing.items():
                        rows.append(
                            {
                                "Ders": display_subject_label(subject),
                                "Istenen": data["istenen"],
                                "Mevcut": data["mevcut"],
                            }
                        )
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)
                    available_counts = {}
                    for q in bank_candidates:
                        label = display_subject_label(q.get("subject", ""))
                        available_counts[label] = available_counts.get(label, 0) + 1
                    if available_counts:
                        st.info("PDF havuzunda bulunan dersler:")
                        avail_rows = [
                            {"Ders": label, "Soru": count}
                            for label, count in sorted(
                                available_counts.items(),
                                key=lambda item: item[1],
                                reverse=True,
                            )
                        ]
                        st.dataframe(pd.DataFrame(avail_rows), use_container_width=True)
                    st.stop()

            if use_ai and not api_key:
                st.warning("AI için OPENAI_API_KEY gerekli. Sabit sablon kullanildi.")

            progress = st.progress(0.0, text="Sorular olusturuluyor...")

            def progress_cb(current, total):
                if total:
                    progress.progress(min(current / total, 1.0))

            try:
                exam = generate_exam_payload(
                    exam_name,
                    grade,
                    section,
                    selected_exam_types,
                    selected_question_types,
                    question_count,
                    duration,
                    selected_outcomes,
                    use_selected_outcomes,
                    use_ai,
                    subjects,
                    subject_counts,
                    progress_cb=progress_cb,
                    difficulty_pref=st.session_state.selected_difficulty,
                    use_bank=st.session_state.use_bank_questions,
                    min_bank_score=st.session_state.bank_min_score,
                    point_per_question=point_per_question,
                    bank_source_filter=st.session_state.bank_source_filter,
                    require_exam_type_match=(
                        st.session_state.exam_mode.startswith("Disardan")
                        or st.session_state.bank_source_filter == "pdf_only"
                    ),
                )
                exam["scoring_system"] = scoring_system
                exam["point_per_question"] = point_per_question
                progress.empty()
                exam["qr_bytes"] = build_qr_bytes(exam["exam_code"])
                st.session_state.latest_exam = exam
                if st.session_state.store_generated_questions:
                    add_to_question_bank(exam.get("questions", []))
                st.success("Sınav oluşturuldu.")
                render_downloads(exam, "after_generate")
            except Exception as e:
                progress.empty()
                st.error(f"Sınav olusturulurken hata olustu: {str(e)}")
                st.info("Lutfen ayarlarinizi kontrol edin ve tekrar deneyin. Soru havuzunda yeterli soru oldugundan emin olun.")
        st.subheader("Sınavı Görüntüle / Indir")
        if st.session_state.latest_exam:
            exam = st.session_state.latest_exam
            render_downloads(exam, "bottom")
            show_exam = st.checkbox("Sınavı Görüntüle", key="show_exam_bottom")

            if show_exam:
                ensure_exam_visuals(exam)
                st.markdown("### Kapak")
                if exam.get("school_logo_bytes"):
                    st.image(exam["school_logo_bytes"], width=140)
                if exam.get("qr_bytes"):
                    st.image(exam["qr_bytes"], width=120)
                st.markdown(f"**{exam.get('school_name', '') or 'Okul Adi'}**")
                st.markdown(f"**Sınav Adi:** {exam['exam_name']}")
                st.markdown(f"**Sınav Kodu:** {exam.get('exam_code', '')}")
                st.markdown(f"**Kitapcik Tipi:** {exam.get('booklet_type', 'A')}")
                st.markdown(f"**Uygulanan Sınıf:** {exam['grade']}. sinif")
                st.markdown(f"**Şube:** {exam['section']}")
                st.markdown(f"**Sınav Turu:** {exam['exam_type']}")
                st.markdown(f"**Sure (dk):** {exam['duration']}")
                if exam.get("subject_counts"):
                    st.markdown("**Ders - Soru Sayısı**")
                    for subject, count in sorted(exam["subject_counts"].items()):
                        st.write(f"{display_subject_label(subject)}: {count}")
                st.divider()
                st.markdown("### Sorular")
                st.write(
                    f"{exam['exam_name']} | {exam['grade']}/{exam['section']} | "
                    f"{exam['exam_type']} | {exam['duration']} dk"
                )
                for idx, question in enumerate(exam["questions"], start=1):
                    st.markdown(f"**{idx}. ({question['question_type']})** {display_question_text(question)}")
                    if question["options"]:
                        st.caption(f"Secenekler: {' / '.join(question['options'])}")
                    if question.get("image_bytes"):
                        st.image(question["image_bytes"], use_container_width=True)
                    if question.get("outcomes"):
                        st.caption(f"Kazanim/Ogrenme: {', '.join(question['outcomes'])}")
                sources = {}
                for question in exam["questions"]:
                    src = question.get("source", "unknown")
                    sources[src] = sources.get(src, 0) + 1
                st.markdown("**Kaynak Dagilimi**")
                for src, count in sorted(sources.items(), key=lambda item: item[0]):
                    st.write(f"{src}: {count}")
                with st.expander("Gorsel eslesme raporu", expanded=False):
                    rows = []
                    for idx, question in enumerate(exam["questions"], start=1):
                        if question.get("image_bytes"):
                            continue
                        template_id, reason = get_visual_match_debug(question)
                        rows.append(
                            {
                                "Soru No": idx,
                                "Ders": display_subject_label(question.get("subject", "")),
                                "Soru": display_question_text(question)[:80],
                                "Template": template_id or "-",
                                "Neden": reason,
                            }
                        )
                    if rows:
                        st.dataframe(pd.DataFrame(rows), use_container_width=True)
                    else:
                        st.info("Tüm sorularda gorsel mevcut veya tetikleyici yok.")

            if st.button("Yeni sinav olustur"):

                st.session_state.latest_exam = None
                st.session_state.builder_started = False
                if "exam_name" in st.session_state:
                    del st.session_state["exam_name"]
                st.rerun()
        else:
            st.info("Henuz sinav olusturulmadi. 'Sınavı Oluştur' butonuna basin.")

    with tabs[13]:
        render_ai_question_creator()


# Internal utilities referenced for module completeness
_UTILS = [get_outcome_map, parse_ayt_pdf_questions]
