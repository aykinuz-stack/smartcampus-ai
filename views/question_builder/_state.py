"""
Soru Olusturma - Session State
==============================
Streamlit session state baslangic fonksiyonu.
"""

from __future__ import annotations

import streamlit as st

from ._constants import (
    DEFAULT_EXAM_TYPES,
    DEFAULT_QUESTION_TYPES,
    DEFAULT_COVER_RULES,
)
from ._io import load_tenant_settings, load_question_bank


def init_question_state() -> None:
    """Session state degiskenlerini baslat."""
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

    # Tenant degisikliginde ayarlari yukle
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
