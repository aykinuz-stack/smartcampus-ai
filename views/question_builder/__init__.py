"""
Soru Olusturma Modulu
=====================
Bu package, sinav sorusu olusturma ve yonetim islevlerini icerir.

Modul yapisi:
- _constants.py: Sabitler (DEFAULT_EXAM_TYPES, DEFAULT_SUBJECTS, vb.)
- _helpers.py: Yardimci fonksiyonlar (normalize_subject_label, subject_key, vb.)
- _paths.py: Dosya yolu fonksiyonlari (get_tenant_dir, get_question_bank_path, vb.)
- _io.py: JSON I/O fonksiyonlari (load_question_bank, save_question_bank, vb.)
- _state.py: Session state baslangic fonksiyonu (init_question_state)
"""

# Sabitler
from ._constants import (
    TENANT_ROOT,
    DEFAULT_EXAM_TYPES,
    DEFAULT_QUESTION_TYPES,
    DEFAULT_SUBJECTS,
    DEFAULT_COVER_RULES,
    TR_CHAR_MAP,
    EXCLUDED_SUBJECTS,
)

# Yardimci fonksiyonlar
from ._helpers import (
    normalize_subject_label,
    display_subject_label,
    normalize_subject_key,
    subject_matches,
    subject_matches_question,
    is_excluded_subject,
    subject_key,
    tenant_key,
    graph_render_settings,
    hex_to_rgb,
    SUBJECT_LABEL_MAP,
)

# Dosya yollari
from ._paths import (
    get_tenant_dir,
    get_question_bank_path,
    get_tenant_settings_path,
    get_generation_plan_path,
    get_tenant_outcomes_dir,
    list_original_pdfs,
)

# I/O fonksiyonlari
from ._io import (
    load_tenant_settings,
    save_tenant_settings,
    load_generation_plan,
    save_generation_plan,
    list_tenants,
    create_tenant,
    compute_quality_score,
    sanitize_question_for_storage,
    load_question_bank,
    save_question_bank,
    add_to_question_bank,
)

# State fonksiyonlari
from ._state import init_question_state

# Ana moduldeki diger fonksiyonlari import et
# (henuz modularize edilmemis karmasik fonksiyonlar)
from views.question_builder_module import (
    # Render fonksiyonlari
    render_question_builder,
    render_cover_settings,
    render_ai_question_creator,
    render_question_bank,
    render_outcomes_selector,
    # PDF import
    import_pdf_visual_questions,
    # Sinav islemleri
    generate_exam_payload,
    build_exam_pdf,
    build_answer_sheet_pdf,
    # Subject islemleri
    get_subjects_from_outcomes,
    # Import islemleri
    parse_tyt_pdf_questions,
    parse_tyt_pdf_answers,
    parse_ayt_pdf_questions,
    parse_ayt_pdf_answers,
    import_questions_from_csv,
    # Outcome islemleri
    load_outcomes,
    get_outcome_map,
)

__all__ = [
    # Sabitler
    "TENANT_ROOT",
    "DEFAULT_EXAM_TYPES",
    "DEFAULT_QUESTION_TYPES",
    "DEFAULT_SUBJECTS",
    "DEFAULT_COVER_RULES",
    "TR_CHAR_MAP",
    "EXCLUDED_SUBJECTS",
    # Yardimci fonksiyonlar
    "normalize_subject_label",
    "display_subject_label",
    "normalize_subject_key",
    "subject_matches",
    "subject_matches_question",
    "is_excluded_subject",
    "subject_key",
    "tenant_key",
    "graph_render_settings",
    "hex_to_rgb",
    "SUBJECT_LABEL_MAP",
    # Dosya yollari
    "get_tenant_dir",
    "get_question_bank_path",
    "get_tenant_settings_path",
    "get_generation_plan_path",
    "get_tenant_outcomes_dir",
    "list_original_pdfs",
    # I/O fonksiyonlari
    "load_tenant_settings",
    "save_tenant_settings",
    "load_generation_plan",
    "save_generation_plan",
    "list_tenants",
    "create_tenant",
    "compute_quality_score",
    "sanitize_question_for_storage",
    "load_question_bank",
    "save_question_bank",
    "add_to_question_bank",
    # State fonksiyonlari
    "init_question_state",
    # Render fonksiyonlari
    "render_question_builder",
    "render_cover_settings",
    "render_ai_question_creator",
    "render_question_bank",
    "render_outcomes_selector",
    # PDF import
    "import_pdf_visual_questions",
    # Sinav islemleri
    "generate_exam_payload",
    "build_exam_pdf",
    "build_answer_sheet_pdf",
    # Subject islemleri
    "get_subjects_from_outcomes",
    # Import islemleri
    "parse_tyt_pdf_questions",
    "parse_tyt_pdf_answers",
    "parse_ayt_pdf_questions",
    "parse_ayt_pdf_answers",
    "import_questions_from_csv",
    # Outcome islemleri
    "load_outcomes",
    "get_outcome_map",
]
