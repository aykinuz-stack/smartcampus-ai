"""
Olcme ve Degerlendirme Modulu
MVP-1 iskeleti: PDF yukleme, job takibi, bankaya hazirlik, sinav PDF ureti.
"""

from __future__ import annotations

import json
import os
import glob
import tempfile
import subprocess
import html
import uuid
import random
import io
import re
from datetime import datetime

import streamlit as st

from utils.tenant import tenant_key, get_tenant_dir
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("olcme_degerlendirme")
except Exception:
    pass

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    from PIL import Image
except Exception:
    Image = None


def get_exam_subject_packages(exam_type: str, ayt_track: str) -> list[str]:
    exam_type = (exam_type or "").upper()
    track = (ayt_track or "").upper()
    if exam_type == "LGS":
        return [
            "Turkce",
            "Matematik",
            "Inkilap Tarihi",
            "Fen Bilimleri",
            "Ingilizce",
            "Din Kulturu",
        ]
    if exam_type == "TYT":
        return [
            "Turk Dili ve Edebiyati",
            "Matematik",
            "Fen Bilimleri (Fizik Kimya Biyoloji)",
            "Sosyal Bilimler (Tarih Cografya Felsefe Din Kulturu)",
        ]
    if exam_type == "AYT":
        if track == "EA":
            return [
                "Turk Dili ve Edebiyati",
                "Sosyal Bilimler-1 (Tarih Cografya)",
                "Matematik",
            ]
        if track == "SAY":
            return [
                "Matematik",
                "Fen Bilimleri (Fizik Kimya Biyoloji)",
            ]
        if track == "SOZ":
            return [
                "Turk Dili ve Edebiyati",
                "Sosyal Bilimler-1 (Tarih Cografya)",
                "Sosyal Bilimler-2 (Tarih Cografya Felsefe Din Kulturu)",
            ]
    return []


def get_exam_subjects_for_custom(exam_type: str, ayt_track: str) -> list[str]:
    exam_type = (exam_type or "").upper()
    track = (ayt_track or "").upper()
    if exam_type == "LGS":
        return [
            "Turkce",
            "Inkilap Tarihi",
            "Din Kulturu",
            "Ingilizce",
            "Matematik",
            "Fen Bilimleri",
        ]
    if exam_type == "TYT":
        return [
            "Turkce",
            "Matematik",
            "Tarih",
            "Cografya",
            "Felsefe",
            "Din Kulturu",
            "Fizik",
            "Kimya",
            "Biyoloji",
        ]
    if exam_type == "AYT":
        if track == "EA":
            return [
                "Turk Dili ve Edebiyati",
                "Tarih",
                "Cografya",
                "Matematik",
            ]
        if track == "SAY":
            return [
                "Matematik",
                "Fizik",
                "Kimya",
                "Biyoloji",
            ]
        if track == "SOZ":
            return [
                "Turk Dili ve Edebiyati",
                "Tarih",
                "Cografya",
                "Tarih-2",
                "Cografya-2",
                "Felsefe Grubu",
                "Din Kulturu",
            ]
    return []


def get_module_root() -> str:
    tenant = tenant_key(st.session_state.get("tenant_name", "UZ Koleji"))
    return os.path.join(os.getcwd(), "data", "tenants", tenant, "measure_eval")


def get_job_store_path() -> str:
    return os.path.join(get_module_root(), "jobs.json")


def load_jobs() -> list[dict]:
    path = get_job_store_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_jobs(items: list[dict]) -> None:
    path = get_job_store_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)


def sync_jobs_with_uploads() -> None:
    uploads_dir = os.path.join(get_module_root(), "uploads")
    if not os.path.isdir(uploads_dir):
        return
    jobs = load_jobs()
    existing = {job.get("file_name") for job in jobs}
    pdf_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(".pdf")]
    created = 0
    for file_name in pdf_files:
        if file_name in existing:
            continue
        jobs.append(
            {
                "job_id": f"JOB-{len(jobs)+1:05d}",
                "file_name": file_name,
                "grade": None,
                "subject": "",
                "level": "",
                "exam_type": "",
                "ayt_track": "",
                "mode": "Soru cikar",
                "status": "hazir",
                "progress": 0,
                "page_count": 0,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "error": "",
            }
        )
        created += 1
    if created:
        save_jobs(jobs)


def update_job(file_name: str, progress: int | None = None, status: str | None = None, error: str | None = None) -> None:
    jobs = load_jobs()
    updated = False
    for job in jobs:
        if job.get("file_name") != file_name:
            continue
        if progress is not None:
            job["progress"] = int(progress)
        if status is not None:
            job["status"] = status
        if error is not None:
            job["error"] = error
        updated = True
        break
    if updated:
        save_jobs(jobs)


def get_job_by_file(file_name: str) -> dict | None:
    for job in load_jobs():
        if job.get("file_name") == file_name:
            return job
    return None


def refresh_job_status(doc_id: str) -> None:
    items = load_question_items()
    answers = load_answer_keys()
    has_questions = any(item.get("doc_id") == doc_id for item in items)
    has_answers = any(item.get("doc_id") == doc_id for item in answers)
    if has_questions and has_answers:
        update_job(doc_id, progress=100, status="tamam")
    elif has_questions:
        update_job(doc_id, progress=70, status="soru_hazir")
    elif has_answers:
        update_job(doc_id, progress=70, status="cevap_hazir")


def check_processing_prereqs() -> tuple[bool, str]:
    if PdfReader is None:
        return False, "PyPDF2 bulunamadı"
    if Image is None:
        return False, "PIL bulunamadı"
    if not find_poppler_bin():
        return False, "Poppler bulunamadı"
    return True, ""


def auto_process_pdf(
    pdf_path: str,
    exam_type: str,
    ayt_track: str,
    grade: int | None,
    subject: str,
    level: str,
    force_rebuild: bool = False,
) -> tuple[int, int]:
    ok, _ = check_processing_prereqs()
    if not ok:
        return 0, 0
    try:
        reader = PdfReader(pdf_path)
    except Exception:
        return 0, 0
    doc_id = os.path.basename(pdf_path)
    total_pages = len(reader.pages)
    store = load_question_items()
    if force_rebuild:
        img_dir = os.path.join(get_module_root(), "question_images")
        to_remove = [item for item in store if item.get("doc_id") == os.path.basename(pdf_path)]
        for item in to_remove:
            image_file = item.get("image_file")
            if image_file:
                file_path = os.path.join(img_dir, image_file)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass
        store = [item for item in store if item.get("doc_id") != os.path.basename(pdf_path)]
    existing_keys = {
        (
            item.get("doc_id"),
            item.get("page_no"),
            item.get("question_no"),
            item.get("column"),
        )
        for item in store
    }
    img_dir = os.path.join(get_module_root(), "question_images")
    os.makedirs(img_dir, exist_ok=True)
    saved = 0
    found_any = False
    skip_markers = {
        "adaylarin dikkatine",
        "sinav kodu",
        "kitapcik tipi",
        "adi ve soyadi",
        "sinifi / sube",
        "ders soru sayisi",
    }
    for page_no in range(1, total_pages + 1):
        try:
            page_text = reader.pages[page_no - 1].extract_text() or ""
        except Exception:
            page_text = ""
        norm_text = page_text.lower().replace("ı", "i")
        if any(marker in norm_text for marker in skip_markers):
            continue
        words, page_w, page_h = extract_words_bbox(pdf_path, page_no)
        bboxes = build_autosplit_bboxes(words, page_w, page_h, 0.10, 0.06)
        page_bytes = render_pdf_page(pdf_path, page_no, dpi=RENDER_DPI)
        if not page_bytes:
            continue
        if bboxes and len(bboxes) < 6:
            # Too few splits -> likely missed numbers, fallback to image segmentation.
            bboxes = []
        if not bboxes:
            if not Image:
                continue
            img = Image.open(io.BytesIO(page_bytes))
            page_w = img.width * (72.0 / RENDER_DPI)
            page_h = img.height * (72.0 / RENDER_DPI)
            bboxes = build_image_segment_bboxes(page_bytes, page_w, page_h)
            if not bboxes:
                bboxes = build_fallback_bboxes(page_w, page_h)
        if not bboxes:
            continue
        found_any = True
        crops = crop_bboxes_from_page(page_bytes, bboxes, page_w, page_h, dpi=CROP_DPI)
        for crop, box in zip(crops, bboxes):
            file_id = f"{os.path.splitext(doc_id)[0]}_{page_no}_{box['question_no']}_{box['column']}.png"
            file_path = os.path.join(img_dir, file_id)
            with open(file_path, "wb") as handle:
                handle.write(crop)
            key = (doc_id, page_no, box["question_no"], box["column"])
            if key in existing_keys:
                continue
            existing_keys.add(key)
            store.append(
                {
                    "doc_id": doc_id,
                    "page_no": page_no,
                    "question_no": box["question_no"],
                    "column": box["column"],
                    "image_file": file_id,
                    "status": "ACTIVE",
                    "needs_manual_check": box["needs_manual_check"],
                    "grade": grade,
                    "subject": subject,
                    "level": level,
                    "exam_type": exam_type,
                    "ayt_track": ayt_track,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )
            saved += 1
        progress = int((page_no / max(total_pages, 1)) * 80)
        update_job(doc_id, progress=progress, status="isleniyor")
    save_question_items(store)
    parsed_answers = parse_answer_key_from_pdf(pdf_path)
    if parsed_answers:
        answers_store = [item for item in load_answer_keys() if item.get("doc_id") != doc_id]
        for item in parsed_answers:
            answers_store.append(
                {
                    "doc_id": doc_id,
                    "question_no": item["question_no"],
                    "correct_choice": item["correct_choice"],
                    "confidence": item["confidence"],
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )
        save_answer_keys(answers_store)
    refresh_job_status(doc_id)
    if not found_any:
        update_job(doc_id, status="hata", error="OCR sonuc yok")
    return saved, len(parsed_answers)


def find_poppler_bin() -> str | None:
    for path in os.environ.get("PATH", "").split(os.pathsep):
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
        for candidate in glob.glob(pattern):
            if os.path.exists(os.path.join(candidate, "pdftoppm.exe")):
                return candidate
    return None


def find_tesseract_exe() -> str | None:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        if not path:
            continue
        candidate = os.path.join(path, "tesseract.exe")
        if os.path.exists(candidate):
            return candidate
    candidates = [
        os.path.join(os.environ.get("ProgramFiles", ""), "Tesseract-OCR", "tesseract.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Tesseract-OCR", "tesseract.exe"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def render_pdf_page(pdf_path: str, page_number: int, dpi: int = 300) -> bytes | None:
    poppler_bin = find_poppler_bin()
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
        matches = glob.glob(f"{out_prefix}-*.png")
        if not matches:
            return None
        with open(matches[0], "rb") as handle:
            return handle.read()


def extract_words_bbox(pdf_path: str, page_number: int) -> tuple[list[dict], float, float]:
    poppler_bin = find_poppler_bin()
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
    if words:
        return words, page_width, page_height
    # OCR fallback for scanned PDFs (numbers only extraction)
    ocr_words, ocr_w, ocr_h = _extract_words_ocr(pdf_path, page_number)
    return ocr_words, ocr_w, ocr_h


def _extract_words_ocr(pdf_path: str, page_number: int) -> tuple[list[dict], float, float]:
    try:
        import pytesseract
    except Exception:
        return [], 0.0, 0.0
    tesseract_exe = find_tesseract_exe()
    if not tesseract_exe:
        return [], 0.0, 0.0
    pytesseract.pytesseract.tesseract_cmd = tesseract_exe
    page_bytes = render_pdf_page(pdf_path, page_number, dpi=OCR_DPI)
    if not page_bytes or not Image:
        return [], 0.0, 0.0
    img = Image.open(io.BytesIO(page_bytes)).convert("L")
    try:
        from PIL import ImageFilter
        img = img.filter(ImageFilter.MedianFilter(size=3))
    except Exception:
        pass
    img = img.point(lambda x: 0 if x < 180 else 255)
    lang = "eng"
    try:
        langs = pytesseract.get_languages(config="")
        if "tur" in langs:
            lang = "tur+eng"
    except Exception:
        pass
    data = pytesseract.image_to_data(
        img,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.",
        lang=lang,
    )
    words = []
    scale = 72.0 / OCR_DPI
    for text, x, y, w, h in zip(
        data.get("text", []),
        data.get("left", []),
        data.get("top", []),
        data.get("width", []),
        data.get("height", []),
    ):
        cleaned = str(text).strip()
        if not cleaned:
            continue
        words.append(
            {
                "text": cleaned,
                "xMin": float(x) * scale,
                "yMin": float(y) * scale,
                "xMax": float(x + w) * scale,
                "yMax": float(y + h) * scale,
            }
        )
    page_width = img.width * scale
    page_height = img.height * scale
    return words, page_width, page_height


def build_autosplit_bboxes(
    words: list[dict],
    page_width: float,
    page_height: float,
    header_ratio: float = 0.08,
    footer_ratio: float = 0.04,
) -> list[dict]:
    if not words or not page_width or not page_height:
        return []
    y0 = page_height * header_ratio
    y1 = page_height * (1 - footer_ratio)
    left_x0, left_x1 = page_width * 0.03, page_width * 0.50
    right_x0, right_x1 = page_width * 0.50, page_width * 0.97
    left_nums = []
    right_nums = []
    for word in words:
        text = word["text"]
        if not re.match(r"^\d{1,3}\.?$", text):
            continue
        if word["yMin"] < y0 or word["yMin"] > y1:
            continue
        if word["xMin"] >= left_x0 and word["xMin"] <= left_x1 * 0.35:
            left_nums.append((int(re.sub(r"\D", "", text)), word["yMin"]))
        elif word["xMin"] >= right_x0 and word["xMin"] <= right_x0 + (page_width * 0.10):
            right_nums.append((int(re.sub(r"\D", "", text)), word["yMin"]))
    left_nums = sorted({(n, y) for n, y in left_nums}, key=lambda item: item[1])
    right_nums = sorted({(n, y) for n, y in right_nums}, key=lambda item: item[1])

    def trim_to_first_one(numbers: list[tuple[int, float]]) -> list[tuple[int, float]]:
        for idx, (num, _) in enumerate(numbers):
            if num == 1:
                return numbers[idx:]
        return numbers

    left_nums = trim_to_first_one(left_nums)
    right_nums = trim_to_first_one(right_nums)

    # If right column numbers are missing, treat as single column layout.
    if left_nums and not right_nums:
        left_x0, left_x1 = page_width * 0.04, page_width * 0.96

    def median_gap(numbers: list[tuple[int, float]]) -> float:
        if len(numbers) < 2:
            return page_height
        ys = [y for _, y in numbers]
        gaps = [ys[idx + 1] - ys[idx] for idx in range(len(ys) - 1)]
        gaps = [g for g in gaps if g > 0]
        if not gaps:
            return page_height
        gaps.sort()
        mid = len(gaps) // 2
        return gaps[mid]

    gap_left = median_gap(left_nums)
    gap_right = median_gap(right_nums)
    small_gap_threshold = page_height * 0.03
    if gap_left < small_gap_threshold and (not right_nums or gap_right < small_gap_threshold):
        return []

    pad_top = page_height * 0.01
    pad_bottom = page_height * 0.04

    def make_boxes(numbers: list[tuple[int, float]], x0: float, x1: float, column: str) -> list[dict]:
        boxes = []
        for idx, (num, y) in enumerate(numbers):
            y_start = max(y0, y - pad_top)
            if idx + 1 < len(numbers):
                y_end = numbers[idx + 1][1] - pad_top + pad_bottom
                y_end = max(y_start + page_height * 0.08, y_end)
                y_end = min(y_end, y1)
            else:
                y_end = y1
            if y_end - y_start < page_height * 0.08:
                needs_check = True
            else:
                needs_check = False
            boxes.append(
                {
                    "question_no": num,
                    "x0": x0,
                    "x1": x1,
                    "y0": y_start,
                    "y1": y_end,
                    "column": column,
                    "needs_manual_check": needs_check,
                }
            )
        return boxes

    return make_boxes(left_nums, left_x0, left_x1, "L") + make_boxes(right_nums, right_x0, right_x1, "R")


def build_fallback_bboxes(
    page_width: float,
    page_height: float,
    rows_per_col: int = 12,
    header_ratio: float = 0.06,
    footer_ratio: float = 0.04,
) -> list[dict]:
    if not page_width or not page_height or rows_per_col <= 0:
        return []
    y0 = page_height * header_ratio
    y1 = page_height * (1 - footer_ratio)
    left_x0, left_x1 = page_width * 0.03, page_width * 0.50
    right_x0, right_x1 = page_width * 0.50, page_width * 0.97
    rows = max(1, rows_per_col)
    row_h = (y1 - y0) / rows
    boxes = []
    for col_idx, (x0, x1, col) in enumerate([(left_x0, left_x1, "L"), (right_x0, right_x1, "R")]):
        for r in range(rows):
            q_no = col_idx * rows + r + 1
            y_start = y0 + r * row_h
            y_end = y0 + (r + 1) * row_h
            boxes.append({
                "question_no": q_no,
                "x0": x0,
                "x1": x1,
                "y0": y_start,
                "y1": y_end,
                "column": col,
                "needs_manual_check": True,
            })
    return boxes


def build_image_segment_bboxes(
    page_bytes: bytes,
    page_width: float,
    page_height: float,
    header_ratio: float = 0.08,
    footer_ratio: float = 0.04,
) -> list[dict]:
    if not Image or not page_bytes:
        return []
    img = Image.open(io.BytesIO(page_bytes)).convert("L")
    target_w = 800
    if img.width > target_w:
        scale_down = target_w / img.width
        img = img.resize((int(img.width * scale_down), int(img.height * scale_down)))
    w, h = img.size
    y0 = int(h * header_ratio)
    y1 = int(h * (1 - footer_ratio))
    col_bounds = [
        (int(w * 0.04), int(w * 0.495), "L"),
        (int(w * 0.505), int(w * 0.96), "R"),
    ]
    boxes = []
    x_scale = page_width / w if w else 1.0
    y_scale = page_height / h if h else 1.0
    threshold_ratio = 0.015
    min_seg_h = max(12, int(h * 0.015))
    pad = 10
    pixels = img.load()
    for x0, x1, col in col_bounds:
        col_w = max(1, x1 - x0)
        row_ink = []
        for y in range(y0, y1):
            ink = 0
            for x in range(x0, x1):
                if pixels[x, y] < 200:
                    ink += 1
            row_ink.append(ink)
        threshold = int(col_w * threshold_ratio)
        segments = []
        in_seg = False
        seg_start = y0
        for idx, ink in enumerate(row_ink):
            y = y0 + idx
            if ink > threshold and not in_seg:
                in_seg = True
                seg_start = y
            elif ink <= threshold and in_seg:
                seg_end = y
                if seg_end - seg_start >= min_seg_h:
                    segments.append((seg_start, seg_end))
                in_seg = False
        if in_seg:
            seg_end = y1
            if seg_end - seg_start >= min_seg_h:
                segments.append((seg_start, seg_end))
        split_segments = []
        max_seg_h = int(h * 0.30)
        for seg_start, seg_end in segments:
            if seg_end - seg_start > max_seg_h:
                count = max(2, int((seg_end - seg_start) / max_seg_h) + 1)
                chunk = max(1, int((seg_end - seg_start) / count))
                for idx in range(count):
                    s = seg_start + idx * chunk
                    e = seg_start + (idx + 1) * chunk if idx + 1 < count else seg_end
                    split_segments.append((s, e))
            else:
                split_segments.append((seg_start, seg_end))

        for seg_start, seg_end in split_segments:
            y_start = max(y0, seg_start - pad)
            y_end = min(y1, seg_end + pad)
            boxes.append(
                {
                    "question_no": len(boxes) + 1,
                    "x0": x0 * x_scale,
                    "x1": x1 * x_scale,
                    "y0": y_start * y_scale,
                    "y1": y_end * y_scale,
                    "column": col,
                    "needs_manual_check": True,
                }
            )
    return boxes


def crop_bboxes_from_page(
    page_bytes: bytes,
    bboxes: list[dict],
    page_width: float,
    page_height: float,
    dpi: int = 150,
) -> list[bytes]:
    if not Image:
        return []
    img = Image.open(io.BytesIO(page_bytes))
    scale = dpi / 72.0
    crops = []
    pad_x = 14
    pad_y = 18
    def trim_whitespace(img: "Image.Image", pad: int = 6) -> "Image.Image":
        gray = img.convert("L")
        bbox = gray.point(lambda x: 0 if x < 245 else 255, "1").getbbox()
        if not bbox:
            return img
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0 - pad)
        y0 = max(0, y0 - pad)
        x1 = min(img.width, x1 + pad)
        y1 = min(img.height, y1 + pad)
        return img.crop((x0, y0, x1, y1))

    for box in bboxes:
        x0 = int(box["x0"] * scale) - pad_x
        y0 = int(box["y0"] * scale) - pad_y
        x1 = int(box["x1"] * scale) + pad_x
        y1 = int(box["y1"] * scale) + pad_y
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(img.width, x1)
        y1 = min(img.height, y1)
        if x1 <= x0 or y1 <= y0:
            continue
        cropped = img.crop((x0, y0, x1, y1))
        cropped = trim_whitespace(cropped, pad=6)
        buffer = io.BytesIO()
        cropped.save(buffer, format="PNG")
        buffer.seek(0)
        crops.append(buffer.read())
    return crops


def get_question_store_path() -> str:
    return os.path.join(get_module_root(), "question_items.json")


def load_question_items() -> list[dict]:
    path = get_question_store_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_question_items(items: list[dict]) -> None:
    path = get_question_store_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)


def _question_image_path(image_file: str) -> str:
    return os.path.join(get_module_root(), "question_images", image_file)


def _load_question_image(item: dict) -> "Image.Image | None":
    if not Image:
        return None
    image_file = item.get("image_file")
    if not image_file:
        return None
    file_path = _question_image_path(image_file)
    if not os.path.exists(file_path):
        return None
    return Image.open(file_path)


def _save_question_image(img: "Image.Image") -> str:
    img_dir = os.path.join(get_module_root(), "question_images")
    os.makedirs(img_dir, exist_ok=True)
    file_id = f"manual_{uuid.uuid4().hex[:12]}.png"
    file_path = _question_image_path(file_id)
    img.save(file_path, format="PNG")
    return file_id


def _auto_trim_image(img: "Image.Image", pad: int = 6) -> "Image.Image":
    gray = img.convert("L")
    bbox = gray.point(lambda x: 0 if x < 245 else 255, "1").getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(img.width, x1 + pad)
    y1 = min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1))


def get_answer_store_path() -> str:
    return os.path.join(get_module_root(), "answer_keys.json")


def load_answer_keys() -> list[dict]:
    path = get_answer_store_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_answer_keys(items: list[dict]) -> None:
    path = get_answer_store_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)


def get_usage_log_path() -> str:
    return os.path.join(get_module_root(), "question_usage.json")


def load_usage_log() -> list[dict]:
    path = get_usage_log_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_usage_log(items: list[dict]) -> None:
    path = get_usage_log_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)


def parse_answer_key_from_pdf(pdf_path: str) -> list[dict]:
    if PdfReader is None:
        return []
    try:
        reader = PdfReader(pdf_path)
    except Exception:
        return []
    started = False
    results = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if not text:
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            if "CEVAP ANAHTARI" in line.upper():
                started = True
            if not started:
                continue
            for number, letter in re.findall(r"(\d{1,3})\s*\.?\s*([A-E])", line):
                results.append(
                    {
                        "question_no": int(number),
                        "correct_choice": letter,
                        "confidence": 1.0,
                    }
                )
    return results


def _register_pdf_fonts() -> tuple[str, str]:
    from utils.shared_data import ensure_turkish_pdf_fonts
    return ensure_turkish_pdf_fonts()


def build_exam_pdf_from_images(title: str, image_paths: list[str]) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
    except Exception:
        return None
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 60
    font_regular, font_bold = _register_pdf_fonts()
    c.setFont(font_bold, 14)
    c.drawString(40, height - 40, title)
    c.setFont(font_regular, 10)
    for idx, path in enumerate(image_paths, start=1):
        if not os.path.exists(path):
            continue
        if y < 120:
            c.showPage()
            y = height - 60
        try:
            img = ImageReader(path)
            img_width, img_height = img.getSize()
            max_width = width - 80
            scale = min(max_width / img_width, 1.0)
            draw_height = img_height * scale
            if y - draw_height < 60:
                c.showPage()
                y = height - 60
            c.drawString(40, y, f"{idx}.")
            c.drawImage(img, 60, y - draw_height + 10, width=img_width * scale, height=draw_height, preserveAspectRatio=True)
            y -= draw_height + 20
        except Exception:
            c.drawString(40, y, f"{idx}. [Görsel okunamadı]")
            y -= 20
    c.save()
    buffer.seek(0)
    return buffer.read()


def build_answer_key_pdf(title: str, answers: list[dict]) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except Exception:
        return None
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    font_regular, font_bold = _register_pdf_fonts()
    c.setFont(font_bold, 14)
    c.drawString(40, height - 40, title)
    c.setFont(font_regular, 10)
    y = height - 70
    line = []
    for item in answers:
        line.append(f"{item['order']}-{item['answer']}")
        if len(line) >= 6:
            c.drawString(40, y, "  ".join(line))
            line = []
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 40
    if line:
        c.drawString(40, y, "  ".join(line))
    c.save()
    buffer.seek(0)
    return buffer.read()


def render_assessment_evaluation() -> None:
    # DEPRECATED: This is the legacy entry point. The new version is olcme_degerlendirme_v2.py.
    # Kept for backward compatibility.
    inject_common_css("ae")
    styled_header("Olcme ve Degerlendirme", "PDF -> SoruKarti Banka -> Cevap Anahtari -> Sinav PDF", icon="📊")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("assessment_evaluation_egitim_yili")

    tabs = st.tabs(
        [
            "📚 PDF Kaynak Kutuphanesi",
            "📤 PDF Yukle (Single/Batch)",
            "⏳ Batch Durum Paneli",
            "🔍 Sayfa Onizleme",
            "✂️ Soru Kırpma Stüdyosu",
            "🔑 Cevap Anahtari Eslesme",
            "🗃️ Soru Bankası (Görsel)",
            "📝 Sınav Oluşturucu",
        ]
    )

    sync_jobs_with_uploads()
    jobs = load_jobs()
    if not st.session_state.get("me_auto_run_once", False):
        pending_jobs = [
            job for job in jobs
            if job.get("mode") == "Soru cikar"
            and job.get("status") in {"isleniyor", "hazir"}
        ]
        if pending_jobs:
            ok, reason = check_processing_prereqs()
            if ok:
                for job in pending_jobs:
                    pdf_path = os.path.join(get_module_root(), "uploads", job.get("file_name"))
                    if os.path.exists(pdf_path):
                        update_job(job.get("file_name"), status="isleniyor", progress=0, error="")
                        auto_process_pdf(
                            pdf_path,
                            job.get("exam_type", ""),
                            job.get("ayt_track", ""),
                            job.get("grade"),
                            job.get("subject", ""),
                            job.get("level", ""),
                        )
                jobs = load_jobs()
            else:
                for job in pending_jobs:
                    update_job(job.get("file_name"), status="hata", error=reason)
                jobs = load_jobs()
        st.session_state.me_auto_run_once = True

    with tabs[0]:
        st.subheader("PDF Kaynak Kutuphanesi")
        if not jobs:
            st.info("Henuz yuklenen PDF yok.")
        else:
            items = load_question_items()
            answers = load_answer_keys()
            rows = []
            for job in jobs:
                doc_id = job.get("file_name")
                rows.append(
                    {
                        "PDF": doc_id,
                        "Sınıf": job.get("grade"),
                        "Ders": job.get("subject"),
                        "Sınav Turu": job.get("exam_type", ""),
                        "AYT": job.get("ayt_track", ""),
                        "Durum": job.get("status"),
                        "İlerleme": job.get("progress"),
                        "Sayfa": job.get("page_count", ""),
                        "Soru": len([i for i in items if i.get("doc_id") == doc_id]),
                        "Cevap": len([a for a in answers if a.get("doc_id") == doc_id]),
                        "Hata": job.get("error", ""),
                    }
                )
            st.dataframe(rows, use_container_width=True)

    with tabs[1]:
        st.subheader("PDF Yukle Sihirbazi")
        st.markdown("**TYT/AYT Yukleme**")
        exam_type = st.radio("Sınav Turu", ["TYT", "AYT", "LGS", "Diger"], index=3, horizontal=True, key="assessment_1")

        ayt_track = ""
        if exam_type == "AYT":
            ayt_track = st.selectbox("AYT Alani", ["SAY", "EA", "SOZ"], index=0, key="assessment_2")

        subject_packages = get_exam_subject_packages(exam_type, ayt_track)
        selected_package = ""
        if subject_packages:
            selected_package = st.selectbox("Ders Paketi", subject_packages, index=0, key="assessment_3")

        uploads_dir = os.path.join(get_module_root(), "uploads")
        st.caption(f"Yukleme dizini: {uploads_dir}")
        col1, col2 = st.columns(2)
        with col1:
            grade = None
            subject = selected_package
            level = ""
            if exam_type == "Diger":
                grade = st.selectbox("Sınıf", [9, 10, 11, 12], index=0, key="assessment_4")

                subject = st.text_input("Ders", key="assessment_5")

                level = st.selectbox("Seviye", ["Deneme", "Yazili", "Seviye Tespit"], index=0)
        with col2:
            mode = st.radio("Is tipi", ["Soru cikar", "Sadece sayfa arsivle"], index=0)

        single_pdf = st.file_uploader("Tek PDF sec", type=["pdf"], key="single_pdf")
        if single_pdf:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(single_pdf, allowed_types=["pdf"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                single_pdf = None
        batch_pdfs = st.file_uploader(
            "Çoklu PDF sec (batch)",
            type=["pdf"],
            accept_multiple_files=True,
            key="batch_pdf",
        )
        if batch_pdfs:
            from utils.security import validate_upload as _vu
            _valid_batch = []
            for _f in batch_pdfs:
                _ok, _msg = _vu(_f, allowed_types=["pdf"], max_mb=100)
                if _ok:
                    _valid_batch.append(_f)
                else:
                    st.warning(f"⚠️ {_f.name}: {_msg}")
            batch_pdfs = _valid_batch
        if os.path.isdir(uploads_dir):
            existing_pdfs = [f for f in os.listdir(uploads_dir) if f.lower().endswith(".pdf")]
            if existing_pdfs:
                st.caption(f"Kayıtli PDF sayisi: {len(existing_pdfs)}")
                st.write(existing_pdfs[:20])
        st.session_state.me_auto_process = st.checkbox(
            "Otomatik isleme basla (soru kes + cevap anahtari + ACTIVE + sinav PDF)",
            value=True,
        )
        st.session_state.me_auto_exam_count = st.number_input(
            "Otomatik sinav soru sayisi",
            min_value=5,
            max_value=200,
            value=20,
        )

        if st.button("Yuklemeyi Baslat", key="assessment_8"):

            upload_dir = os.path.join(get_module_root(), "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            created = 0
            payloads = []
            files = []
            if single_pdf is not None:
                files.append(single_pdf)
            if batch_pdfs:
                files.extend(batch_pdfs)
            auto_process = st.session_state.get("me_auto_process", True)
            auto_exam_count = int(st.session_state.get("me_auto_exam_count", 20))
            auto_exam_bytes = []
            auto_key_bytes = []
            progress_bar = st.progress(0.0)
            total_files = max(len(files), 1)
            for idx, file in enumerate(files, start=1):
                file_name = file.name
                dest = os.path.join(upload_dir, file_name)
                with open(dest, "wb") as handle:
                    handle.write(file.getvalue())
                page_count = 0
                if PdfReader is not None:
                    try:
                        reader = PdfReader(dest)
                        page_count = len(reader.pages)
                    except Exception:
                        page_count = 0
                payloads.append(
                    {
                        "job_id": f"JOB-{len(jobs)+created+1:05d}",
                        "file_name": file_name,
                        "grade": grade,
                        "subject": subject,
                        "level": level,
                        "exam_type": exam_type,
                        "ayt_track": ayt_track,
                        "mode": mode,
                        "status": "isleniyor",
                        "progress": 0,
                        "page_count": page_count,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "error": "",
                    }
                )
                created += 1
                if auto_process and mode == "Soru cikar":
                    ok, reason = check_processing_prereqs()
                    if not ok:
                        update_job(file_name, status="hata", error=reason)
                        st.error(f"{file_name} islenemedi: {reason}")
                        progress_bar.progress(min(idx / total_files, 1.0))
                        continue
                    saved, _ = auto_process_pdf(dest, exam_type, ayt_track, grade, subject, level)
                    if saved:
                        items = load_question_items()
                        pool = [item for item in items if item.get("doc_id") == file_name and item.get("status") == "ACTIVE"]
                        if len(pool) >= auto_exam_count:
                            chosen = random.sample(pool, auto_exam_count)
                            img_dir = os.path.join(get_module_root(), "question_images")
                            image_paths = [os.path.join(img_dir, item["image_file"]) for item in chosen]
                            exam_pdf = build_exam_pdf_from_images(f"{exam_type} Sınav", image_paths)
                            if exam_pdf:
                                auto_exam_bytes.append((file_name, exam_pdf))
                            answers_store = load_answer_keys()
                            answer_map = {
                                (item["doc_id"], item["question_no"]): item["correct_choice"]
                                for item in answers_store
                            }
                            answers = []
                            for order, item in enumerate(chosen, start=1):
                                choice = answer_map.get((item["doc_id"], item["question_no"]), "")
                                answers.append({"order": order, "answer": choice or "-"})
                            key_pdf = build_answer_key_pdf("Cevap Anahtari", answers)
                            if key_pdf:
                                auto_key_bytes.append((file_name, key_pdf))
                progress_bar.progress(min(idx / total_files, 1.0))
            if created:
                jobs.extend(payloads)
                save_jobs(jobs)
                st.session_state.me_auto_run_once = False
                st.success(f"{created} PDF yuklendi, job oluşturuldu.")
                if auto_exam_bytes:
                    st.subheader("Otomatik Sınav Ciktilari")
                    for file_name, exam_pdf in auto_exam_bytes:
                        st.download_button(
                            f"{file_name} - Sınav PDF indir",
                            data=exam_pdf,
                            file_name=f"{os.path.splitext(file_name)[0]}_sinav.pdf",
                            mime="application/pdf",
                            key=f"auto_exam_{file_name}",
                        )
                    for file_name, key_pdf in auto_key_bytes:
                        st.download_button(
                            f"{file_name} - Cevap Anahtari indir",
                            data=key_pdf,
                            file_name=f"{os.path.splitext(file_name)[0]}_cevap_anahtari.pdf",
                            mime="application/pdf",
                            key=f"auto_key_{file_name}",
                        )
            else:
                st.warning("PDF seçilmedi.")

    with tabs[2]:
        st.subheader("Batch Durum Paneli")
        if not jobs:
            st.info("Job bulunamadı.")
        else:
            items = load_question_items()
            answers = load_answer_keys()
            if st.button("Tüm isleri otomatik isle", key="assessment_9"):

                ok, reason = check_processing_prereqs()
                if not ok:
                    st.error(f"Otomatik isleme baslayamadi: {reason}")
                else:
                    for job in jobs:
                        if job.get("mode") != "Soru cikar":
                            continue
                        if job.get("status") in {"tamam"}:
                            continue
                        pdf_path = os.path.join(get_module_root(), "uploads", job.get("file_name"))
                        if not os.path.exists(pdf_path):
                            update_job(job.get("file_name"), status="hata", error="PDF bulunamadı")
                            continue
                        update_job(job.get("file_name"), status="isleniyor", progress=0, error="")
                        auto_process_pdf(
                            pdf_path,
                            job.get("exam_type", ""),
                            job.get("ayt_track", ""),
                            job.get("grade"),
                            job.get("subject", ""),
                            job.get("level", ""),
                        )
                    st.success("Otomatik isleme tamamlandı.")
                    st.rerun()
            for job in jobs:
                st.write(f"{job.get('file_name')} | {job.get('status')}")
                if job.get("page_count"):
                    st.caption(f"Sayfa: {job.get('page_count')}")
                st.progress(job.get("progress", 0) / 100 if job.get("progress") else 0.0)
                doc_id = job.get("file_name")
                st.caption(
                    f"Toplam Soru: {len([i for i in items if i.get('doc_id') == doc_id])} | "
                    f"Cevap: {len([a for a in answers if a.get('doc_id') == doc_id])}"
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Tekrar Dene", key=f"retry_{job.get('job_id')}"):
                        job["status"] = "isleniyor"
                        job["progress"] = 0
                        job["error"] = ""
                        save_jobs(jobs)
                        st.success("Job tekrar baslatildi.")
                        st.rerun()
                with col_b:
                    if st.button("Kaldigi yerden", key=f"resume_{job.get('job_id')}"):
                        job["status"] = "isleniyor"
                        save_jobs(jobs)
                        st.success("Job devam edecegi sekilde isaretlendi.")
                        st.rerun()

    with tabs[3]:
        st.subheader("Sayfa Onizleme")
        if not jobs:
            st.info("Onizleme için yuklenen PDF yok.")
        else:
            job_files = [job.get("file_name") for job in jobs]
            selected_file = st.selectbox("PDF sec", job_files, key="preview_pdf_select")
            pdf_path = os.path.join(get_module_root(), "uploads", selected_file)
            if not os.path.exists(pdf_path):
                st.error("PDF bulunamadı.")
            else:
                page_count = 1
                if PdfReader is not None:
                    try:
                        reader = PdfReader(pdf_path)
                        page_count = len(reader.pages)
                    except Exception:
                        page_count = 1
                page_number = st.number_input(
                    "Sayfa",
                    min_value=1,
                    max_value=page_count,
                    value=1,
                    step=1,
                )
                image_bytes = render_pdf_page(pdf_path, int(page_number), dpi=300)
                if image_bytes:
                    st.image(image_bytes, use_container_width=True)
                else:
                    st.info("Onizleme için Poppler gerekli veya PDF render edilemedi.")

    with tabs[4]:
        st.subheader("Soru Kırpma Stüdyosu")
        studio_tabs = st.tabs(["▶️ Sırayla Mod", "⚡ Otomatik Bölme"])
        with studio_tabs[0]:
            if not jobs:
                st.info("Kırpma için yüklenen PDF yok.")
            else:
                job_files = [job.get("file_name") for job in jobs]
                selected_file = st.selectbox("PDF sec", job_files, key="seq_crop_pdf")
                doc_id = selected_file
                items = [item for item in load_question_items() if item.get("doc_id") == doc_id]
                items.sort(key=lambda x: (x.get("page_no", 0), x.get("question_no", 0), x.get("column", "")))

                if not items:
                    st.info("Bu PDF için soru bulunamadı.")
                else:
                    if "seq_index" not in st.session_state:
                        st.session_state.seq_index = 0
                    st.session_state.seq_index = max(0, min(st.session_state.seq_index, len(items) - 1))

                    left_col, mid_col, right_col = st.columns([1, 2, 1])

                    with left_col:
                        st.markdown("**Soru Listesi**")
                        rows = []
                        for idx, item in enumerate(items, start=1):
                            status = item.get("status", "DRAFT")
                            rows.append(
                                {
                                    "#": idx,
                                    "Soru": item.get("question_no"),
                                    "Sayfa": item.get("page_no"),
                                    "Kolon": item.get("column"),
                                    "Durum": status,
                                }
                            )
                        st.dataframe(rows, use_container_width=True, height=420)

                    current = items[st.session_state.seq_index]
                    with mid_col:
                        st.markdown(f"**Secili Soru:** {st.session_state.seq_index + 1}/{len(items)}")
                        img = _load_question_image(current)
                        if img:
                            st.image(img, use_container_width=True)
                        else:
                            st.warning("Görsel bulunamadı.")

                        nav_col1, nav_col2, nav_col3 = st.columns(3)
                        with nav_col1:
                            if st.button("Önceki", key="seq_prev"):
                                st.session_state.seq_index = max(0, st.session_state.seq_index - 1)
                                st.rerun()
                        with nav_col2:
                            if st.button("Sonraki", key="seq_next"):
                                st.session_state.seq_index = min(len(items) - 1, st.session_state.seq_index + 1)
                                st.rerun()
                        with nav_col3:
                            if st.button("Onayla + Sonraki", key="seq_approve"):
                                current["status"] = "APPROVED"
                                current["needs_manual_check"] = False
                                save_question_items(items)
                                st.session_state.seq_index = min(len(items) - 1, st.session_state.seq_index + 1)
                                st.rerun()

                    with right_col:
                        st.markdown("**Meta**")
                        st.write(
                            f"Sayfa: {current.get('page_no')} | Soru: {current.get('question_no')} | Kolon: {current.get('column')}"
                        )
                        st.write(f"Durum: {current.get('status', 'DRAFT')}")
                        st.write(f"Flag: {'Evet' if current.get('needs_manual_check') else 'Hayir'}")

                        if st.button("Auto-trim uygula", key="seq_trim"):
                            img = _load_question_image(current)
                            if img:
                                trimmed = _auto_trim_image(img, pad=6)
                                current["image_file"] = _save_question_image(trimmed)
                                current["status"] = "EDITED"
                                save_question_items(items)
                                st.success("Auto-trim uygulandi.")

                        if st.button("Sil / Atla", key="seq_delete"):
                            current["status"] = "DELETED"
                            save_question_items(items)
                            st.session_state.seq_index = min(len(items) - 1, st.session_state.seq_index + 1)
                            st.rerun()

                        st.markdown("**Birlesitir / Bol**")
                        if st.button("Merge sonraki", key="seq_merge"):
                            if st.session_state.seq_index + 1 < len(items):
                                next_item = items[st.session_state.seq_index + 1]
                                img1 = _load_question_image(current)
                                img2 = _load_question_image(next_item)
                                if Image is None:
                                    st.warning("PIL bulunamadı.")
                                elif img1 and img2:
                                    merged = Image.new("RGB", (max(img1.width, img2.width), img1.height + img2.height), "white")
                                    merged.paste(img1, (0, 0))
                                    merged.paste(img2, (0, img1.height))
                                    current["image_file"] = _save_question_image(merged)
                                    current["status"] = "MERGED"
                                    next_item["status"] = "MERGED_INTO"
                                    next_item["merged_into"] = current.get("question_no")
                                    save_question_items(items)
                                    st.success("Birlesitirildi.")
                                else:
                                    st.warning("Görsel bulunamadı.")

                        split_y = st.number_input("Split Y (px)", min_value=10, value=200, step=10, key="seq_split_y")
                        manual_no = st.text_input("Yeni soru no (opsiyonel)", key="seq_manual_no")
                        if st.button("Split", key="seq_split"):
                            img = _load_question_image(current)
                            if Image is None:
                                st.warning("PIL bulunamadı.")
                            elif img and 0 < split_y < img.height:
                                top = img.crop((0, 0, img.width, int(split_y)))
                                bottom = img.crop((0, int(split_y), img.width, img.height))
                                current["image_file"] = _save_question_image(top)
                                current["status"] = "SPLIT"
                                new_item = dict(current)
                                new_item["image_file"] = _save_question_image(bottom)
                                new_item["status"] = "SPLIT_NEW"
                                new_item["question_no"] = manual_no or f"{current.get('question_no')}-2"
                                items.insert(st.session_state.seq_index + 1, new_item)
                                save_question_items(items)
                                st.success("Bolundu.")
                            else:
                                st.warning("Gecerli split_y girin.")

        with studio_tabs[1]:
            st.subheader("Soru Kırpma Stüdyosu (Otomatik Bölme)")
            if not jobs:
                st.info("Kırpma için yüklenen PDF yok.")
            else:
                job_files = [job.get("file_name") for job in jobs]
                selected_file = st.selectbox("PDF sec", job_files, key="crop_pdf_select")
            pdf_path = os.path.join(get_module_root(), "uploads", selected_file)
            if not os.path.exists(pdf_path):
                st.error("PDF bulunamadı.")
            else:
                page_count = 1
                if PdfReader is not None:
                    try:
                        reader = PdfReader(pdf_path)
                        page_count = len(reader.pages)
                    except Exception:
                        page_count = 1
                page_number = st.number_input(
                    "Sayfa",
                    min_value=1,
                    max_value=page_count,
                    value=1,
                    step=1,
                    key="crop_page",
                )
                header_ratio = st.slider("Header kesim (%)", 0.0, 0.2, 0.10, 0.01, key="assessment_12")

                footer_ratio = st.slider("Footer kesim (%)", 0.0, 0.2, 0.06, 0.01, key="assessment_13")

                if st.button("Otomatik bol", key="assessment_14"):

                    words, page_w, page_h = extract_words_bbox(pdf_path, int(page_number))
                    bboxes = build_autosplit_bboxes(words, page_w, page_h, header_ratio, footer_ratio)
                    st.session_state.autosplit_bboxes = bboxes
                    st.session_state.autosplit_page = {
                        "pdf": pdf_path,
                        "page": int(page_number),
                        "width": page_w,
                        "height": page_h,
                    }
                    st.success(f"Bulunan soru kutusu: {len(bboxes)}")

                bboxes = st.session_state.get("autosplit_bboxes", [])
                page_meta = st.session_state.get("autosplit_page", {})
                if bboxes and page_meta:
                    page_bytes = render_pdf_page(page_meta["pdf"], page_meta["page"], dpi=300)
                    if page_bytes:
                        crops = crop_bboxes_from_page(
                            page_bytes,
                            bboxes,
                            page_meta.get("width", 0.0),
                            page_meta.get("height", 0.0),
                            dpi=300,
                        )
                        st.write(f"Onizleme (ilk 8 soru): {min(len(crops), 8)}")
                        for idx, crop in enumerate(crops[:8]):
                            st.image(crop, use_container_width=True)
                        st.subheader("Kutular Listesi")
                        if bboxes:
                            table_rows = [
                                {
                                    "Soru": box["question_no"],
                                    "Kolon": box["column"],
                                    "y0": round(box["y0"], 1),
                                    "y1": round(box["y1"], 1),
                                    "Kontrol": "Evet" if box["needs_manual_check"] else "Hayir",
                                }
                                for box in bboxes
                            ]
                            st.dataframe(table_rows, use_container_width=True)
                        st.subheader("Manuel Düzenleme")
                        if bboxes:
                            options = [
                                f"{box['question_no']} ({box['column']})"
                                for box in bboxes
                            ]
                            selected_idx = st.selectbox(
                                "Düzenlenecek soru",
                                list(range(len(options))),
                                format_func=lambda idx: options[idx],
                                key="bbox_edit_select",
                            )
                            selected_box = bboxes[selected_idx]
                            col_a, col_b = st.columns(2)
                            with col_a:
                                x0 = st.number_input("x0", value=float(selected_box["x0"]), key="bbox_x0")
                                y0 = st.number_input("y0", value=float(selected_box["y0"]), key="bbox_y0")
                            with col_b:
                                x1 = st.number_input("x1", value=float(selected_box["x1"]), key="bbox_x1")
                                y1 = st.number_input("y1", value=float(selected_box["y1"]), key="bbox_y1")
                            if st.button("Güncelle ve Onizle", key="bbox_update"):
                                selected_box.update({"x0": x0, "y0": y0, "x1": x1, "y1": y1})
                                st.session_state.autosplit_bboxes = bboxes
                                preview_crop = crop_bboxes_from_page(
                                    page_bytes,
                                    [selected_box],
                                    page_meta.get("width", 0.0),
                                    page_meta.get("height", 0.0),
                                    dpi=300,
                                )
                                if preview_crop:
                                    st.image(preview_crop[0], use_container_width=True)
                            if st.button("Kutuyu sil", key="bbox_delete"):
                                bboxes.pop(selected_idx)
                                st.session_state.autosplit_bboxes = bboxes
                                st.success("Kutu silindi.")
                                st.rerun()
                        if st.button("Kirp ve kaydet", key="assessment_15"):

                            store = load_question_items()
                            doc_id = os.path.basename(pdf_path)
                            job_meta = get_job_by_file(doc_id) or {}
                            existing_keys = {
                                (
                                    item.get("doc_id"),
                                    item.get("page_no"),
                                    item.get("question_no"),
                                    item.get("column"),
                                )
                                for item in store
                            }
                            img_dir = os.path.join(get_module_root(), "question_images")
                            os.makedirs(img_dir, exist_ok=True)
                            saved = 0
                            for idx, crop in enumerate(crops):
                                box = bboxes[idx]
                                file_id = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{page_meta['page']}_{box['question_no']}_{box['column']}.png"
                                file_path = os.path.join(img_dir, file_id)
                                with open(file_path, "wb") as handle:
                                    handle.write(crop)
                                key = (
                                    doc_id,
                                    page_meta["page"],
                                    box["question_no"],
                                    box["column"],
                                )
                                if key in existing_keys:
                                    continue
                                existing_keys.add(key)
                                store.append(
                                    {
                                        "doc_id": doc_id,
                                        "page_no": page_meta["page"],
                                        "question_no": box["question_no"],
                                        "column": box["column"],
                                        "image_file": file_id,
                                        "status": "DRAFT",
                                        "needs_manual_check": box["needs_manual_check"],
                                        "grade": job_meta.get("grade"),
                                        "subject": job_meta.get("subject"),
                                        "exam_type": job_meta.get("exam_type"),
                                        "ayt_track": job_meta.get("ayt_track"),
                                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    }
                                )
                                saved += 1
                            save_question_items(store)
                            refresh_job_status(doc_id)
                            st.success(f"Kaydedilen soru: {saved}")
                    else:
                        st.info("Sayfa render edilemedi.")

    with tabs[5]:
        st.subheader("Cevap Anahtari Eslesme")
        if not jobs:
            st.info("Cevap anahtari için PDF yok.")
        else:
            job_files = [job.get("file_name") for job in jobs]
            selected_file = st.selectbox("PDF sec", job_files, key="answer_pdf_select")
            pdf_path = os.path.join(get_module_root(), "uploads", selected_file)
            if st.button("Cevap anahtarini parse et", key="assessment_16"):

                parsed = parse_answer_key_from_pdf(pdf_path)
                if not parsed:
                    st.error("Cevap anahtari bulunamadı.")
                else:
                    store = load_answer_keys()
                    doc_id = os.path.basename(pdf_path)
                    store = [item for item in store if item.get("doc_id") != doc_id]
                    for item in parsed:
                        store.append(
                            {
                                "doc_id": doc_id,
                                "question_no": item["question_no"],
                                "correct_choice": item["correct_choice"],
                                "confidence": item["confidence"],
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            }
                        )
                    save_answer_keys(store)
                    refresh_job_status(doc_id)
                    st.success(f"Kaydedilen cevap: {len(parsed)}")
            st.subheader("Kayıtli Cevaplar")
            answers = [a for a in load_answer_keys() if a.get("doc_id") == os.path.basename(pdf_path)]
            if answers:
                st.dataframe(answers, use_container_width=True)
                st.subheader("Eslesme Raporu")
                questions = [
                    item for item in load_question_items()
                    if item.get("doc_id") == os.path.basename(pdf_path)
                ]
                answer_numbers = {a.get("question_no") for a in answers}
                missing = sorted({q.get("question_no") for q in questions if q.get("question_no") not in answer_numbers})
                if missing:
                    st.warning(f"Eksik cevap sayisi: {len(missing)}")
                    st.write(", ".join(str(n) for n in missing[:50]))
                else:
                    st.success("Tüm sorular eslesti.")
                st.subheader("Manuel Duzeltme")
                answers_sorted = sorted(answers, key=lambda x: x.get("question_no", 0))
                idx = st.selectbox(
                    "Soru sec",
                    list(range(len(answers_sorted))),
                    format_func=lambda i: f"Soru {answers_sorted[i]['question_no']}",
                    key="answer_edit_select",
                )
                selected = answers_sorted[idx]
                new_choice = st.selectbox(
                    "Dogru cevap",
                    ["A", "B", "C", "D", "E"],
                    index=["A", "B", "C", "D", "E"].index(selected.get("correct_choice", "A")),
                    key="answer_edit_choice",
                )
                if st.button("Cevabi Güncelle", key="assessment_17"):

                    store = load_answer_keys()
                    for item in store:
                        if (
                            item.get("doc_id") == selected.get("doc_id")
                            and item.get("question_no") == selected.get("question_no")
                        ):
                            item["correct_choice"] = new_choice
                            item["confidence"] = 1.0
                            break
                    save_answer_keys(store)
                    st.success("Cevap güncellendi.")
                    st.rerun()
            else:
                st.info("Kayıtli cevap yok.")

    with tabs[6]:
        st.subheader("Soru Bankası (Görsel)")
        items = load_question_items()
        if not items:
            st.info("Kayıtli soru yok.")
        else:
            doc_options = sorted({item["doc_id"] for item in items})
            status_options = sorted({item.get("status", "DRAFT") for item in items})
            exam_options = sorted({item.get("exam_type") for item in items if item.get("exam_type")})
            doc_filter = st.selectbox("Kaynak PDF", ["Tüm"] + doc_options, key="assessment_18")

            status_filter = st.selectbox("Durum", ["Tüm"] + status_options, key="assessment_19")

            exam_filter = st.selectbox("Sınav Turu", ["Tüm"] + exam_options, key="assessment_20")

            question_filter = st.text_input("Soru No (opsiyonel)", key="assessment_21")

            filtered = items
            if doc_filter != "Tüm":
                filtered = [item for item in filtered if item["doc_id"] == doc_filter]
            if status_filter != "Tüm":
                filtered = [item for item in filtered if item.get("status") == status_filter]
            if exam_filter != "Tüm":
                filtered = [item for item in filtered if item.get("exam_type") == exam_filter]
            if question_filter.strip():
                filtered = [
                    item for item in filtered
                    if str(item.get("question_no")) == question_filter.strip()
                ]
            st.write(f"Toplam soru: {len(filtered)}")
            if st.button("Tümünu ACTIVE yap", key="activate_all_bank"):
                for item in items:
                    if doc_filter != "Tüm" and item["doc_id"] != doc_filter:
                        continue
                    item["status"] = "ACTIVE"
                save_question_items(items)
                st.success("Secili sorular ACTIVE yapildi.")
                st.rerun()

            img_dir = os.path.join(get_module_root(), "question_images")
            answer_store = load_answer_keys()
            answer_map = {
                (item["doc_id"], item["question_no"]): item["correct_choice"]
                for item in answer_store
            }
            preview_count = min(8, len(filtered))
            for item in filtered[:preview_count]:
                img_path = os.path.join(img_dir, item["image_file"])
                st.write(
                    f"{item['doc_id']} | Soru {item['question_no']} | {item['column']} | "
                    f"{item.get('status', 'DRAFT')} | "
                    f"Cevap: {answer_map.get((item['doc_id'], item['question_no']), '-')}"
                )
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    st.info("Görsel bulunamadı.")

            st.subheader("Durum Güncelle")
            if filtered:
                pick = st.selectbox(
                    "Soru sec",
                    list(range(len(filtered))),
                    format_func=lambda idx: f"{filtered[idx]['doc_id']} #{filtered[idx]['question_no']} ({filtered[idx]['column']})",
                    key="bank_item_select",
                )
                selected_item = filtered[pick]
                new_status = st.selectbox("Yeni durum", ["DRAFT", "ACTIVE"], key="bank_status_select")
                if st.button("Durumu guncelle", key="assessment_22"):

                    for item in items:
                        if (
                            item["doc_id"] == selected_item["doc_id"]
                            and item["page_no"] == selected_item["page_no"]
                            and item["question_no"] == selected_item["question_no"]
                            and item["column"] == selected_item["column"]
                        ):
                            item["status"] = new_status
                            break
                    save_question_items(items)
                    st.success("Durum güncellendi.")
                    st.rerun()

    with tabs[7]:
        st.subheader("Sınav Oluşturucu")
        items = load_question_items()
        if not items:
            st.info("Soru bankasi bos.")
        else:
            doc_options = sorted({item["doc_id"] for item in items})
            exam_options = sorted({item.get("exam_type") for item in items if item.get("exam_type")})
            selected_docs = st.multiselect("Kaynak PDF'ler", doc_options, default=doc_options[:1], key="assessment_23")

            question_count = st.number_input("Soru sayisi", min_value=5, max_value=200, value=20, key="assessment_24")

            title = st.text_input("Sınav Başlığı", value="Karma Sınav", key="assessment_25")

            no_repeat_days = st.number_input("Tekrar etme kurali (gun)", min_value=0, max_value=365, value=90, key="assessment_26")

            only_active = st.checkbox("Sadece ACTIVE sorular", value=True, key="assessment_27")

            exam_filter = st.selectbox("Sınav Turu", ["Tüm"] + exam_options, key="assessment_28")

            ayt_filter = ""
            if exam_filter == "AYT":
                ayt_filter = st.selectbox("AYT Alani", ["SAY", "EA", "SOZ"], index=0, key="assessment_29")

            subject_options = get_exam_subject_packages(exam_filter, ayt_filter) if exam_filter != "Tüm" else []
            selected_subjects = []
            if subject_options:
                selected_subjects = st.multiselect("Ders Paketleri", subject_options, default=subject_options, key="assessment_30")

            required_counts = {}
            custom_counts = {}
            custom_duration = None
            if exam_filter in {"LGS", "TYT", "AYT"}:
                mode_choice = st.radio(
                    "Ders/Soru/Sure Modu",
                    ["Orjinal", "Kullanıcı belirlesin"],
                    horizontal=True,
                )
                is_original = mode_choice == "Orjinal"
            else:
                is_original = True

            if exam_filter == "LGS" and is_original:
                st.markdown("**LGS Orjinal Dagilim**")
                required_counts = {
                    "Turkce": 20,
                    "Inkilap Tarihi": 10,
                    "Din Kulturu": 10,
                    "Ingilizce": 10,
                    "Matematik": 20,
                    "Fen Bilimleri": 20,
                }
                st.markdown("**LGS Sureleri**")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.write("Sozel Bolum: 75 dk")
                with col_s2:
                    st.write("Sayısal Bolum: 80 dk")
            if exam_filter == "TYT" and is_original:
                st.markdown("**TYT Orjinal Dagilim**")
                required_counts = {
                    "Turkce": 40,
                    "Matematik": 40,
                    "Tarih": 5,
                    "Cografya": 5,
                    "Felsefe": 5,
                    "Din Kulturu": 5,
                    "Fizik": 7,
                    "Kimya": 7,
                    "Biyoloji": 6,
                }
                st.markdown("**TYT Suresi**")
                st.write("165 dk")
            if exam_filter == "AYT" and ayt_filter == "EA" and is_original:
                st.markdown("**AYT EA Orjinal Dagilim**")
                required_counts = {
                    "Turk Dili ve Edebiyati": 24,
                    "Tarih": 10,
                    "Cografya": 6,
                    "Matematik": 40,
                }
                st.markdown("**AYT Suresi**")
                st.write("180 dk")
            if exam_filter == "AYT" and ayt_filter == "SAY" and is_original:
                st.markdown("**AYT SAY Orjinal Dagilim**")
                required_counts = {
                    "Matematik": 40,
                    "Fizik": 14,
                    "Kimya": 13,
                    "Biyoloji": 13,
                }
                st.markdown("**AYT Suresi**")
                st.write("180 dk")
            if exam_filter == "AYT" and ayt_filter == "SOZ" and is_original:
                st.markdown("**AYT SOZ Orjinal Dagilim**")
                required_counts = {
                    "Turk Dili ve Edebiyati": 24,
                    "Tarih": 10,
                    "Cografya": 6,
                    "Tarih-2": 11,
                    "Cografya-2": 11,
                    "Felsefe Grubu": 11,
                    "Din Kulturu": 6,
                }
                st.markdown("**AYT Suresi**")
                st.write("180 dk")

            if exam_filter in {"LGS", "TYT", "AYT"} and not is_original:
                st.markdown("**Kullanıcı Secimi**")
                custom_duration = st.number_input("Sınav Suresi (dk)", min_value=30, max_value=300, value=90, key="assessment_32")

                subject_list = get_exam_subjects_for_custom(exam_filter, ayt_filter)
                selected_custom_subjects = st.multiselect(
                    "Dersler",
                    subject_list,
                    default=subject_list,
                )
                for subj in selected_custom_subjects:
                    custom_counts[subj] = st.number_input(
                        f"{subj} soru sayisi",
                        min_value=0,
                        max_value=200,
                        value=0,
                        key=f"custom_count_{exam_filter}_{ayt_filter}_{subj}",
                    )
            q_min = st.number_input("Soru No min (opsiyonel)", min_value=0, max_value=999, value=0, key="assessment_35")

            q_max = st.number_input("Soru No max (opsiyonel)", min_value=0, max_value=999, value=0, key="assessment_36")

            if st.button("Sınav PDF Uret", key="assessment_37"):

                pool = [item for item in items if item["doc_id"] in selected_docs]
                if only_active:
                    pool = [item for item in pool if item.get("status") == "ACTIVE"]
                if exam_filter != "Tüm":
                    pool = [item for item in pool if item.get("exam_type") == exam_filter]
                if ayt_filter:
                    pool = [item for item in pool if item.get("ayt_track") == ayt_filter]
                if selected_subjects:
                    pool = [item for item in pool if item.get("subject") in selected_subjects]
                if q_min > 0:
                    pool = [item for item in pool if int(item.get("question_no", 0)) >= int(q_min)]
                if q_max > 0:
                    pool = [item for item in pool if int(item.get("question_no", 0)) <= int(q_max)]
                usage_log = load_usage_log()
                if no_repeat_days > 0:
                    cutoff = datetime.now().timestamp() - (int(no_repeat_days) * 86400)
                    recent = {
                        (u["doc_id"], u["question_no"])
                        for u in usage_log
                        if u.get("used_at") and float(u.get("used_at")) >= cutoff
                    }
                    pool = [item for item in pool if (item["doc_id"], item["question_no"]) not in recent]
                if required_counts or custom_counts:
                    chosen = []
                    missing_subjects = []
                    required = required_counts or custom_counts
                    fallback_map = {}
                    if required_counts and exam_filter == "TYT":
                        fallback_map = {
                            "Tarih": ["Sosyal Bilimler (Tarih Cografya Felsefe Din Kulturu)"],
                            "Cografya": ["Sosyal Bilimler (Tarih Cografya Felsefe Din Kulturu)"],
                            "Felsefe": ["Sosyal Bilimler (Tarih Cografya Felsefe Din Kulturu)"],
                            "Din Kulturu": ["Sosyal Bilimler (Tarih Cografya Felsefe Din Kulturu)"],
                            "Fizik": ["Fen Bilimleri (Fizik Kimya Biyoloji)"],
                            "Kimya": ["Fen Bilimleri (Fizik Kimya Biyoloji)"],
                            "Biyoloji": ["Fen Bilimleri (Fizik Kimya Biyoloji)"],
                        }
                    if required_counts and exam_filter == "AYT" and ayt_filter == "EA":
                        fallback_map = {
                            "Tarih": ["Sosyal Bilimler-1 (Tarih Cografya)"],
                            "Cografya": ["Sosyal Bilimler-1 (Tarih Cografya)"],
                            "Matematik": ["Matematik"],
                        }
                    if required_counts and exam_filter == "AYT" and ayt_filter == "SAY":
                        fallback_map = {
                            "Fizik": ["Fen Bilimleri (Fizik Kimya Biyoloji)"],
                            "Kimya": ["Fen Bilimleri (Fizik Kimya Biyoloji)"],
                            "Biyoloji": ["Fen Bilimleri (Fizik Kimya Biyoloji)"],
                            "Matematik": ["Matematik"],
                        }
                    if required_counts and exam_filter == "AYT" and ayt_filter == "SOZ":
                        fallback_map = {
                            "Tarih": ["Sosyal Bilimler-1 (Tarih Cografya)"],
                            "Cografya": ["Sosyal Bilimler-1 (Tarih Cografya)"],
                            "Tarih-2": ["Sosyal Bilimler-2 (Tarih Cografya Felsefe Din Kulturu)"],
                            "Cografya-2": ["Sosyal Bilimler-2 (Tarih Cografya Felsefe Din Kulturu)"],
                            "Felsefe Grubu": ["Sosyal Bilimler-2 (Tarih Cografya Felsefe Din Kulturu)"],
                            "Din Kulturu": ["Sosyal Bilimler-2 (Tarih Cografya Felsefe Din Kulturu)"],
                            "Turk Dili ve Edebiyati": ["Turk Dili ve Edebiyati"],
                        }
                    available_pool = pool[:]
                    for subject, count in required.items():
                        subject_pool = [item for item in available_pool if item.get("subject") == subject]
                        if len(subject_pool) < count and subject in fallback_map:
                            fallback_subjects = fallback_map.get(subject, [])
                            for fallback in fallback_subjects:
                                if len(subject_pool) >= count:
                                    break
                                fallback_pool = [item for item in available_pool if item.get("subject") == fallback]
                                if fallback_pool:
                                    subject_pool = fallback_pool
                                    break
                        if len(subject_pool) < count:
                            missing_subjects.append(subject)
                            continue
                        picked = random.sample(subject_pool, count)
                        chosen.extend(picked)
                        picked_set = set(id(item) for item in picked)
                        available_pool = [item for item in available_pool if id(item) not in picked_set]
                    if missing_subjects:
                        st.warning(
                            "Havuzda yeterli soru yok: "
                            + ", ".join(sorted(missing_subjects))
                        )
                        return
                else:
                    if len(pool) < int(question_count):
                        st.warning("Havuzda yeterli soru yok.")
                        return
                    chosen = random.sample(pool, int(question_count))
                img_dir = os.path.join(get_module_root(), "question_images")
                image_paths = [os.path.join(img_dir, item["image_file"]) for item in chosen]
                exam_pdf = build_exam_pdf_from_images(title, image_paths)
                if exam_pdf:
                    st.download_button(
                        "Sınav PDF indir",
                        data=exam_pdf,
                        file_name="sinav.pdf",
                        mime="application/pdf",
                    )
                answers_store = load_answer_keys()
                answer_map = {
                    (item["doc_id"], item["question_no"]): item["correct_choice"]
                    for item in answers_store
                }
                answers = []
                for order, item in enumerate(chosen, start=1):
                    choice = answer_map.get((item["doc_id"], item["question_no"]), "")
                    answers.append({"order": order, "answer": choice or "-"})
                key_pdf = build_answer_key_pdf("Cevap Anahtari", answers)
                if key_pdf:
                    st.download_button(
                        "Cevap Anahtari PDF indir",
                        data=key_pdf,
                        file_name="cevap_anahtari.pdf",
                        mime="application/pdf",
                    )
                for item in chosen:
                    usage_log.append(
                        {
                            "doc_id": item["doc_id"],
                                "question_no": item["question_no"],
                                "used_at": datetime.now().timestamp(),
                            }
                        )
                    save_usage_log(usage_log)
RENDER_DPI = 600
OCR_DPI = 500
CROP_DPI = 600

# Legacy alias — replaced by olcme_degerlendirme_v2.render_olcme_degerlendirme_v2
_LEGACY = [render_assessment_evaluation]
