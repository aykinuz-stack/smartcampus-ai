"""
Yeni PDF soru yukleme ekrani.
PDF'lerden soru kartlari olusturup havuza kaydeder.
"""

from __future__ import annotations

import os
import shutil
import json
import io
import time

import streamlit as st

from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("olcme_degerlendirme")
except Exception:
    pass


def render_pdf_question_importer(embedded: bool = False) -> None:
    from views import question_builder as qb
    from views import assessment_evaluation as ae
    from utils import pdf_pipeline

    def _build_subject_report(questions: list[dict]) -> dict:
        report = {"toplam": 0, "dersler": {}, "eslenmeyen": 0}
        for question in questions:
            report["toplam"] += 1
            label = qb.display_subject_label(question.get("subject", ""))
            report["dersler"][label] = report["dersler"].get(label, 0) + 1
            if question.get("subject") in {"Bilinmiyor", "PDF"}:
                report["eslenmeyen"] += 1
        return report

    def _apply_pdf_tags(
        questions: list[dict],
        grade: int,
        exam_types: list[str],
        subject_tags: list[str],
        question_types: list[str],
        subject_rule: str,
    ) -> list[dict]:
        subject_override = subject_tags[0] if len(subject_tags) == 1 else None
        preferred_qtype = question_types[0] if question_types else None
        rr_index = 0
        for question in questions:
            question["grade"] = grade
            if subject_override:
                question["subject"] = subject_override
            elif subject_tags:
                current_subject = question.get("subject")
                if current_subject in subject_tags:
                    pass
                elif subject_rule == "Rastgele dagit":
                    question["subject"] = subject_tags[rr_index % len(subject_tags)]
                    rr_index += 1
                elif subject_rule == "Bilinmiyor olarak isaretle":
                    question["subject"] = "Bilinmiyor"
                else:
                    question["subject"] = subject_tags[0]
            if exam_types:
                question["exam_type"] = exam_types[0]
            if preferred_qtype:
                question["question_type"] = preferred_qtype
            if subject_tags:
                question["subject_tags"] = subject_tags
        return questions

    inject_common_css("pqi")
    if embedded:
        st.subheader("Yeni Soru PDF Ekle")
        st.caption("PDF yukleyerek soru havuzu olusturun. Sinav olusturma bu ekranda yoktur.")
    else:
        styled_header("Yeni Soru PDF Ekle", "PDF yukleyerek soru havuzu olusturun", icon="📄")
        st.caption("Sinav olusturma bu ekranda yoktur.")

    qb.init_question_state()

    if not embedded:
        st.subheader("Tenant Secimi")
        tenants = qb.list_tenants()
        selected_tenant = st.selectbox(
            "Okul/Tenant",
            tenants,
            index=tenants.index(st.session_state.tenant_name) if st.session_state.tenant_name in tenants else 0,
            key="pdf_import_tenant",
        )
        if selected_tenant != st.session_state.tenant_name:
            st.session_state.tenant_name = selected_tenant
            st.rerun()
        new_tenant = st.text_input("Yeni tenant adi", key="pdf_import_new_tenant")
        if st.button("Yeni tenant olustur", key="pdf_import_new_tenant_btn"):
            cleaned = new_tenant.strip()
            if cleaned:
                qb.create_tenant(cleaned)
                st.session_state.tenant_name = cleaned
                st.rerun()
            else:
                st.warning("Gecerli bir tenant adi girin.")

    st.divider()
    st.subheader("PDF Etiketleri")

    exam_type_options = [
        "TYT",
        "AYT EA",
        "AYT SAY",
        "AYT SOZ",
        "LGS",
        "Deneme Sınavı",
        "Okul Yazilisi",
        "Bursluluk Sınavı",
        "Seviye Tespit Sınavı",
    ]
    selected_exam_types = []
    for idx, exam_type in enumerate(exam_type_options):
        if st.checkbox(exam_type, key=f"pdf_import_exam_type_{idx}"):
            selected_exam_types.append(exam_type)
    if not selected_exam_types:
        st.info("Sınav turu seçilmedi. PDF etiketinde sinav turu bos kalir.")

    grade = st.selectbox("Sınıf", [5, 6, 7, 8, 9, 10, 11, 12], index=4, key="pdf_import_grade")
    sections = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "İ", "J", "K", "L", "M", "N", "Ş",
    ]
    selected_section = st.selectbox("Şube", sections, index=0, key="pdf_import_section")

    subject_options = [subject for subject in qb.get_subjects_from_outcomes() if not qb.is_excluded_subject(subject)]
    subject_options = list(dict.fromkeys(subject_options))
    st.markdown("**Dersler**")
    col_sel, col_clear = st.columns(2)
    with col_sel:
        select_all = st.checkbox("Tüm dersleri sec", key="pdf_import_select_all")
    with col_clear:
        clear_all = st.checkbox("Tüm secimleri kaldir", key="pdf_import_clear_all")
    if select_all:
        for idx, subject in enumerate(subject_options):
            st.session_state[f"pdf_import_subject_{qb.subject_key(subject)}_{idx}"] = True
    if clear_all:
        for idx, subject in enumerate(subject_options):
            st.session_state[f"pdf_import_subject_{qb.subject_key(subject)}_{idx}"] = False
    selected_subjects = []
    for idx, subject in enumerate(subject_options):
        if st.checkbox(
            qb.display_subject_label(subject),
            key=f"pdf_import_subject_{qb.subject_key(subject)}_{idx}",
        ):
            selected_subjects.append(subject)
    if not selected_subjects:
        st.warning("Ders seçilmedi. PDF sorulari genel etikete duser.")

    if len(selected_subjects) > 1:
        subject_rule = st.radio(
            "Ders dagitma kurali",
            ["Tespit edilen dersi koru", "Rastgele dagit", "Bilinmiyor olarak isaretle"],
            index=0,
            key="pdf_import_subject_rule",
            horizontal=True,
        )
    else:
        subject_rule = "Tespit edilen dersi koru"

    st.divider()
    st.subheader("PDF Yükle")
    upload_mode = st.radio(
        "Yükleme tipi",
        ["Gorsel (onerilen)", "TYT metinli (text layer)"],
        index=0,
        horizontal=True,
        key="pdf_import_upload_mode",
    )
    tyt_selected = any(exam_type.strip().lower() == "tyt" for exam_type in selected_exam_types)
    question_type_options = [
        "Çoktan Secmeli (ABCDE)" if tyt_selected or upload_mode.startswith("Gorsel") else "Çoktan Secmeli (ABCD)",
        "Dogru/Yanlis",
        "Bosluk Doldurma",
        "Açık Uclu",
        "Klasik",
    ]
    st.markdown("**Soru Turu**")
    selected_question_types = []
    for idx, qtype in enumerate(question_type_options):
        default_checked = qtype == "Çoktan Secmeli (ABCDE)"
        if st.checkbox(qtype, value=default_checked, key=f"pdf_import_qtype_{idx}"):
            selected_question_types.append(qtype)
    uploaded_files = st.file_uploader(
        "PDF dosyalari",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_import_upload_files",
    )
    force_rebuild = st.checkbox(
        "PDF'yi yeniden isle (eski soru kartlarini sil)",
        value=False,
        key="pdf_import_force_rebuild",
    )
    auto_mode = st.checkbox(
        "Tam otomatik (auto-trim + otomatik onay)",
        value=True,
        key="pdf_import_auto_mode",
    )
    keep_original = st.checkbox(
        "Orjinal PDF'i koru (ayri kopya)",
        value=False,
        key="pdf_import_keep_original",
    )
    if uploaded_files:
        from utils.security import validate_upload
        _valid_files = []
        for _f in uploaded_files:
            _ok, _msg = validate_upload(_f, allowed_types=["pdf"], max_mb=100)
            if _ok:
                _valid_files.append(_f)
            else:
                st.warning(f"⚠️ {_f.name}: {_msg}")
        uploaded_files = _valid_files

    if st.button("PDF'leri havuza aktar", key="pdf_import_run"):
        if not uploaded_files:
            st.warning("PDF seçilmedi.")
        else:
            upload_dir = os.path.join(qb.get_tenant_dir(st.session_state.tenant_name), "uploads")
            originals_dir = os.path.join(upload_dir, "originals")
            pipeline_root = os.path.join(qb.get_tenant_dir(st.session_state.tenant_name), "pdf_pipeline")
            os.makedirs(upload_dir, exist_ok=True)
            added_total = 0
            report_items = []
            all_questions = []
            progress = st.progress(0.0, text="İşleme baslatiliyor...")
            status_box = st.empty()
            for file in uploaded_files:
                status_lines = [
                    f"PDF: {file.name}",
                    "1) Yükleme",
                    "2) Render",
                    "3) Soru bolme",
                    "4) Kirma/Kaydet",
                    "5) Havuz guncelle",
                ]
                status_box.info("\n".join(status_lines))
                dest = os.path.join(upload_dir, file.name)
                with open(dest, "wb") as handle:
                    handle.write(file.getvalue())
                if keep_original:
                    os.makedirs(originals_dir, exist_ok=True)
                    name_root, ext = os.path.splitext(file.name)
                    original_name = file.name
                    original_path = os.path.join(originals_dir, original_name)
                    if os.path.exists(original_path):
                        original_name = f"{name_root}__orig_{int(time.time() * 1000)}{ext}"
                        original_path = os.path.join(originals_dir, original_name)
                    shutil.copy2(dest, original_path)
                status_lines[1] = "1) Yükleme ✅"
                status_box.info("\n".join(status_lines))
                if upload_mode.startswith("Gorsel"):
                    status_lines[2] = "2) Render (otomatik) ..."
                    status_lines[3] = "3) Soru bolme (otomatik) ..."
                    status_lines[4] = "4) Kirma/Kaydet (otomatik) ..."
                    status_box.info("\n".join(status_lines))

                    doc_id = os.path.splitext(os.path.basename(dest))[0]
                    out_dir = os.path.join(pipeline_root, doc_id)
                    if force_rebuild and os.path.isdir(out_dir):
                        shutil.rmtree(out_dir, ignore_errors=True)
                    if force_rebuild:
                        cleaned = []
                        for item in st.session_state.question_bank:
                            source_pdf = item.get("source_pdf", "")
                            if os.path.basename(source_pdf) != os.path.basename(dest):
                                cleaned.append(item)
                        st.session_state.question_bank = cleaned
                        qb.save_question_bank(st.session_state.tenant_name, cleaned)

                    extracted = pdf_pipeline.extract_questions_from_pdf(
                        dest,
                        out_dir,
                        dpi=300,
                        auto_trim=auto_mode,
                    )
                    if not extracted:
                        count = qb.import_pdf_visual_questions(
                            dest,
                            selected_subjects[0] if len(selected_subjects) == 1 else "PDF",
                            exam_type_tag=selected_exam_types[0] if selected_exam_types else None,
                            subject_tags=selected_subjects,
                            question_type_override=selected_question_types[0] if selected_question_types else None,
                            grade_override=grade,
                            subject_rule=subject_rule,
                            force_rebuild=force_rebuild,
                        )
                        status_lines[2] = "2) Render OK"
                        status_lines[3] = "3) Soru bolme OK"
                        status_lines[4] = "4) Kirma/Kaydet OK"
                        added_total += count
                        report_items.append({"PDF": file.name, "Soru": count})
                        if auto_mode and count:
                            items = ae.load_question_items()
                            changed = False
                            for item in items:
                                if item.get("doc_id") != os.path.basename(dest):
                                    continue
                                if item.get("status") == "DELETED":
                                    continue
                                img = ae._load_question_image(item)
                                if img:
                                    trimmed = ae._auto_trim_image(img, pad=6)
                                    item["image_file"] = ae._save_question_image(trimmed)
                                    item["status"] = "APPROVED"
                                    item["needs_manual_check"] = False
                                    changed = True
                        if changed:
                            ae.save_question_items(items)
                        continue
                    answer_key = pdf_pipeline.parse_answer_key(dest)
                    os.makedirs(out_dir, exist_ok=True)
                    with open(os.path.join(out_dir, "answer_key.json"), "w", encoding="utf-8") as handle:
                        json.dump(answer_key, handle, ensure_ascii=False, indent=2)
                    report_path = os.path.join(out_dir, "answer_key_report.json")
                    report = pdf_pipeline.build_answer_key_report(
                        extracted,
                        answer_key,
                        report_path,
                    )
                    needs_review = report.get("needs_review", False)
                    missing_list = report.get("missing_questions", [])
                    if needs_review:
                        st.warning(
                            f"Cevap anahtari uyusmazligi: eksikler {missing_list}. "
                            "Sorular NEEDS_REVIEW olarak isaretlenecek."
                        )
                    try:
                        from PIL import Image
                    except Exception:
                        Image = None
                    questions = []
                    rr_index = 0
                    for extracted_item in extracted:
                        subject_value = selected_subjects[0] if selected_subjects else "PDF"
                        if len(selected_subjects) > 1:
                            if subject_rule == "Rastgele dagit":
                                subject_value = selected_subjects[rr_index % len(selected_subjects)]
                                rr_index += 1
                            elif subject_rule == "Bilinmiyor olarak isaretle":
                                subject_value = "Bilinmiyor"
                        qid = (
                            f"pdfpipe-{doc_id}-{extracted_item.get('page')}-"
                            f"{extracted_item.get('question_no')}-{extracted_item.get('column')}"
                        )
                        needs_flag = needs_review
                        flag_reasons = []
                        if needs_review:
                            flag_reasons.append("answer_key_mismatch")
                        image_path = extracted_item.get("image_path")
                        if Image and image_path and os.path.exists(image_path):
                            try:
                                with Image.open(image_path) as img:
                                    if img.width < 200 or img.height < 120:
                                        needs_flag = True
                                        flag_reasons.append("small_crop")
                            except Exception:
                                needs_flag = True
                                flag_reasons.append("image_open_error")
                        questions.append(
                            {
                                "id": qid,
                                "grade": grade,
                                "subject": subject_value,
                                "question_type": selected_question_types[0]
                                if selected_question_types
                                else "Çoktan Secmeli (ABCDE)",
                                "difficulty": "medium",
                                "text": (
                                    f"[PDF] {doc_id} {extracted_item.get('page')}-"
                                    f"{extracted_item.get('question_no')}"
                                ),
                                "options": [],
                                "answer": "",
                                "source": "pdf_image",
                                "source_pdf": dest,
                                "asset_path": image_path,
                                "source_page": extracted_item.get("page"),
                                "source_number": extracted_item.get("question_no"),
                                "subject_tags": selected_subjects,
                                "needs_manual_check": needs_flag,
                                "flag_reasons": flag_reasons,
                            }
                        )
                        if selected_exam_types:
                            questions[-1]["exam_type"] = selected_exam_types[0]
                    if questions:
                        report["flagged_items"] = [
                            {
                                "question_no": item.get("source_number"),
                                "page": item.get("source_page"),
                                "reasons": item.get("flag_reasons", []),
                            }
                            for item in questions
                            if item.get("needs_manual_check")
                        ]
                        report["inactive_count"] = sum(
                            1 for item in questions if item.get("needs_manual_check")
                        )
                        with open(report_path, "w", encoding="utf-8") as handle:
                            json.dump(report, handle, ensure_ascii=False, indent=2)
                        st.caption("Cevap anahtari raporu")
                        st.json(report)
                        flagged = report.get("flagged_items", [])
                        if flagged:
                            st.markdown("**Flag Filtreleri**")
                            pages = sorted({str(item.get("page", "")) for item in flagged if item.get("page")})
                            qnos = sorted({str(item.get("question_no", "")) for item in flagged if item.get("question_no")})
                            reasons = sorted({reason for item in flagged for reason in item.get("reasons", [])})
                            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
                            with f_col1:
                                filter_pages = st.multiselect(
                                    "Sayfa",
                                    pages,
                                    key=f"pdf_import_flag_page_{doc_id}",
                                )
                            with f_col2:
                                filter_qnos = st.multiselect(
                                    "Soru no",
                                    qnos,
                                    key=f"pdf_import_flag_qno_{doc_id}",
                                )
                            with f_col3:
                                filter_reasons = st.multiselect(
                                    "Neden",
                                    reasons,
                                    key=f"pdf_import_flag_reason_{doc_id}",
                                )
                            with f_col4:
                                if st.button("Temizle", key=f"pdf_import_flag_clear_{doc_id}"):
                                    st.session_state[f"pdf_import_flag_page_{doc_id}"] = []
                                    st.session_state[f"pdf_import_flag_qno_{doc_id}"] = []
                                    st.session_state[f"pdf_import_flag_reason_{doc_id}"] = []
                                    st.rerun()
                            filtered = []
                            for item in flagged:
                                page_ok = not filter_pages or str(item.get("page", "")) in filter_pages
                                qno_ok = not filter_qnos or str(item.get("question_no", "")) in filter_qnos
                                reason_list = item.get("reasons", []) or []
                                reason_ok = not filter_reasons or any(r in reason_list for r in filter_reasons)
                                if page_ok and qno_ok and reason_ok:
                                    filtered.append(item)
                            st.dataframe(filtered, use_container_width=True)
                            reason_counts_ui = {}
                            for item in filtered:
                                for reason in item.get("reasons", []) or []:
                                    reason_counts_ui[reason] = reason_counts_ui.get(reason, 0) + 1
                            if reason_counts_ui:
                                st.bar_chart(reason_counts_ui)
                        st.download_button(
                            "Raporu indir (JSON)",
                            data=json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"),
                            file_name=f"{doc_id}_answer_key_report.json",
                            mime="application/json",
                            key=f"pdf_import_report_download_{doc_id}",
                        )
                        # PDF raporu
                        try:
                            from reportlab.pdfgen import canvas
                            from reportlab.lib.pagesizes import A4
                            from reportlab.pdfbase import pdfmetrics
                            from reportlab.pdfbase.ttfonts import TTFont
                        except Exception:
                            canvas = None
                        if canvas:
                            buffer = io.BytesIO()
                            pdf = canvas.Canvas(buffer, pagesize=A4)
                            width, height = A4
                            y = height - 40
                            from utils.shared_data import ensure_turkish_pdf_fonts
                            font_regular, font_bold = ensure_turkish_pdf_fonts()
                            pdf.setFont(font_bold, 12)
                            pdf.drawString(40, y, "Cevap Anahtari Raporu")
                            y -= 20
                            pdf.setFont(font_regular, 10)
                            pdf.drawString(40, y, f"PDF: {doc_id}")
                            y -= 16
                            pdf.drawString(40, y, f"Eksik soru sayisi: {len(report.get('missing_questions', []))}")
                            y -= 16
                            pdf.drawString(40, y, f"Flagli soru sayisi: {len(report.get('flagged_items', []))}")
                            y -= 20
                            pdf.setFont(font_bold, 10)
                            pdf.drawString(40, y, "Flag Özeti:")
                            y -= 14
                            pdf.setFont(font_regular, 9)
                            reason_counts = {}
                            for item in report.get("flagged_items", []):
                                for reason in item.get("reasons", []):
                                    reason_counts[reason] = reason_counts.get(reason, 0) + 1
                            for reason, count in sorted(reason_counts.items()):
                                line = f"{reason}: {count}"
                                if y < 40:
                                    pdf.showPage()
                                    y = height - 40
                                    pdf.setFont(font_regular, 9)
                                pdf.drawString(40, y, line[:120])
                                y -= 12
                            y -= 8
                            pdf.setFont(font_bold, 10)
                            pdf.drawString(40, y, "Flagli Sorular:")
                            y -= 16
                            pdf.setFont(font_regular, 9)
                            for item in report.get("flagged_items", []):
                                line = (
                                    f"Soru: {item.get('question_no')} | Sayfa: {item.get('page')} | "
                                    f"Neden: {', '.join(item.get('reasons', []))}"
                                )
                                if y < 40:
                                    pdf.showPage()
                                    y = height - 40
                                    pdf.setFont(font_regular, 9)
                                pdf.drawString(40, y, line[:120])
                                y -= 12
                            pdf.save()
                            buffer.seek(0)
                            st.download_button(
                                "Raporu indir (PDF)",
                                data=buffer.getvalue(),
                                file_name=f"{doc_id}_answer_key_report.pdf",
                                mime="application/pdf",
                                key=f"pdf_import_report_download_pdf_{doc_id}",
                            )
                    qb.add_to_question_bank(questions)
                    count = len(questions)
                    status_lines[2] = "2) Render OK"
                    status_lines[3] = "3) Soru bolme OK"
                    status_lines[4] = "4) Kirma/Kaydet OK"
                    added_total += count
                    report_items.append({"PDF": file.name, "Soru": count})
                else:
                    status_lines[2] = "2) Metin katmani okuma ⏳"
                    status_lines[3] = "3) Soru bolme (metin) ⏳"
                    status_lines[4] = "4) Kaydet ⏳"
                    status_box.info("\n".join(status_lines))
                    questions = qb.parse_tyt_pdf_questions(dest)
                    questions = _apply_pdf_tags(
                        questions,
                        grade,
                        selected_exam_types,
                        selected_subjects,
                        selected_question_types,
                        subject_rule,
                    )
                    qb.add_to_question_bank(questions)
                    status_lines[2] = "2) Metin katmani okuma ✅"
                    status_lines[3] = "3) Soru bolme (metin) ✅"
                    status_lines[4] = "4) Kaydet ✅"
                    added_total += len(questions)
                    report_items.append({"PDF": file.name, "Soru": len(questions)})
                    all_questions.extend(questions)
                status_lines[5 - 1] = "5) Havuz guncelle ✅"
                status_box.success("\n".join(status_lines))
                progress.progress(min(added_total / max(len(uploaded_files), 1), 1.0))

            st.success(f"Havuza eklenen toplam soru: {added_total}")
            if report_items:
                st.dataframe(report_items, use_container_width=True)

            if upload_mode.startswith("TYT"):
                st.info("TYT metinli modda PDF metin katmani yoksa soru bulunamayabilir.")

            if all_questions:
                st.caption("Ders dagilimi raporu (son yukleme)")
                report = _build_subject_report(all_questions)
                rows = [{"Ders": label, "Soru": count} for label, count in report["dersler"].items()]
                st.dataframe(rows, use_container_width=True)

    st.divider()
    st.subheader("Soru Kırpma Stüdyosu (Sırayla Mod)")
    items = ae.load_question_items()
    if not items:
        st.info("Henuz kirpilmis soru yok.")
        return

    doc_ids = sorted({item.get("doc_id") for item in items if item.get("doc_id")})
    if not doc_ids:
        st.info("Henuz kirpilmis soru yok.")
        return
    selected_doc = st.selectbox("PDF sec", doc_ids, key="pdf_import_seq_doc")
    only_flagged = st.checkbox("Sadece flagli sorulari goster", value=False, key="pdf_import_seq_flagged_only")
    seq_items = [item for item in items if item.get("doc_id") == selected_doc]
    if only_flagged:
        seq_items = [item for item in seq_items if item.get("needs_manual_check")]
    seq_items.sort(key=lambda x: (x.get("page_no", 0), x.get("question_no", 0), x.get("column", "")))
    if not seq_items:
        st.info("Bu PDF için soru bulunamadı.")
        return

    if "pdf_import_seq_index" not in st.session_state:
        st.session_state.pdf_import_seq_index = 0
    st.session_state.pdf_import_seq_index = max(
        0, min(st.session_state.pdf_import_seq_index, len(seq_items) - 1)
    )
    current = seq_items[st.session_state.pdf_import_seq_index]

    left_col, mid_col, right_col = st.columns([1, 2, 1])
    with left_col:
        st.markdown("**Soru Listesi**")
        rows = []
        for idx, item in enumerate(seq_items, start=1):
            rows.append(
                {
                    "#": idx,
                    "Soru": item.get("question_no"),
                    "Sayfa": item.get("page_no"),
                    "Kolon": item.get("column"),
                    "Durum": item.get("status", "DRAFT"),
                    "Flag": "Evet" if item.get("needs_manual_check") else "Hayir",
                    "Neden": ", ".join(item.get("flag_reasons", []) or []),
                }
            )
        st.dataframe(rows, use_container_width=True, height=420)

    with mid_col:
        st.markdown(f"**Secili Soru:** {st.session_state.pdf_import_seq_index + 1}/{len(seq_items)}")
        img = ae._load_question_image(current)
        if img:
            st.image(img, use_container_width=True)
        else:
            st.warning("Gorsel bulunamadı.")

        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            if st.button("Önceki", key="pdf_import_seq_prev"):
                st.session_state.pdf_import_seq_index = max(0, st.session_state.pdf_import_seq_index - 1)
                st.rerun()
        with nav2:
            if st.button("Sonraki", key="pdf_import_seq_next"):
                st.session_state.pdf_import_seq_index = min(len(seq_items) - 1, st.session_state.pdf_import_seq_index + 1)
                st.rerun()
        with nav3:
            if st.button("Onayla + Sonraki", key="pdf_import_seq_approve"):
                current["status"] = "APPROVED"
                current["needs_manual_check"] = False
                ae.save_question_items(items)
                st.session_state.pdf_import_seq_index = min(len(seq_items) - 1, st.session_state.pdf_import_seq_index + 1)
                st.rerun()
        if only_flagged:
            if st.button("Sonraki flagli", key="pdf_import_seq_next_flagged"):
                flagged_indices = [
                    idx for idx, item in enumerate(seq_items)
                    if item.get("needs_manual_check")
                ]
                if flagged_indices:
                    current_index = st.session_state.pdf_import_seq_index
                    next_indices = [idx for idx in flagged_indices if idx > current_index]
                    target = next_indices[0] if next_indices else flagged_indices[0]
                    st.session_state.pdf_import_seq_index = target
                    st.rerun()

    with right_col:
        st.markdown("**Meta**")
        st.write(
            f"Sayfa: {current.get('page_no')} | Soru: {current.get('question_no')} | Kolon: {current.get('column')}"
        )
        st.write(f"Durum: {current.get('status', 'DRAFT')}")
        st.write(f"Flag: {'Evet' if current.get('needs_manual_check') else 'Hayir'}")

        st.markdown("**BBox Düzenleme (Canvas)**")
        try:
            from streamlit_drawable_canvas import st_canvas
            canvas_available = True
        except Exception:
            canvas_available = False
        if not canvas_available:
            st.info("Canvas için streamlit-drawable-canvas gerekli.")
        else:
            img = ae._load_question_image(current)
            if img:
                try:
                    canvas = st_canvas(
                        background_image=img,
                        drawing_mode="rect",
                        stroke_width=2,
                        stroke_color="#FF4B4B",
                        fill_color="rgba(255, 0, 0, 0.1)",
                        height=img.height,
                        width=img.width,
                        key="pdf_import_bbox_canvas",
                    )
                except Exception:
                    canvas = None
                    st.info("Canvas bu Streamlit surumunde desteklenmiyor. Manuel trim kullanin.")
                if canvas is not None and st.button("Canvas bbox uygula", key="pdf_import_bbox_apply"):
                    if canvas.json_data and canvas.json_data.get("objects"):
                        obj = canvas.json_data["objects"][-1]
                        x0 = int(obj.get("left", 0))
                        y0 = int(obj.get("top", 0))
                        x1 = x0 + int(obj.get("width", 0))
                        y1 = y0 + int(obj.get("height", 0))
                        if x1 > x0 and y1 > y0:
                            cropped = img.crop((x0, y0, x1, y1))
                            current["image_file"] = ae._save_question_image(cropped)
                            current["status"] = "EDITED"
                            ae.save_question_items(items)
                            st.success("BBox uygulandi.")
                        else:
                            st.warning("Gecerli bir bbox cizin.")
                    else:
                        st.warning("Önce bir kutu cizin.")

        if st.button("Auto-trim uygula", key="pdf_import_seq_trim"):
            img = ae._load_question_image(current)
            if img:
                trimmed = ae._auto_trim_image(img, pad=6)
                current["image_file"] = ae._save_question_image(trimmed)
                current["status"] = "EDITED"
                ae.save_question_items(items)
                st.success("Auto-trim uygulandi.")

        if st.button("Sil / Atla", key="pdf_import_seq_delete"):
            current["status"] = "DELETED"
            ae.save_question_items(items)
            st.session_state.pdf_import_seq_index = min(len(seq_items) - 1, st.session_state.pdf_import_seq_index + 1)
            st.rerun()
        if only_flagged:
            if st.button("Flaglilari pasife al", key="pdf_import_seq_deactivate_flagged"):
                for item in items:
                    if item.get("doc_id") != selected_doc:
                        continue
                    if not item.get("needs_manual_check"):
                        continue
                    item["status"] = "INACTIVE"
                ae.save_question_items(items)
                st.session_state.pdf_import_seq_index = 0
                st.rerun()
            if st.button("Pasifleri tekrar aktif et", key="pdf_import_seq_activate_flagged"):
                for item in items:
                    if item.get("doc_id") != selected_doc:
                        continue
                    if item.get("status") != "INACTIVE":
                        continue
                    item["status"] = "APPROVED"
                    item["needs_manual_check"] = False
                ae.save_question_items(items)
                st.session_state.pdf_import_seq_index = 0
                st.rerun()

        st.markdown("**Birlesitir / Bol**")
        if st.button("Merge sonraki", key="pdf_import_seq_merge"):
            if st.session_state.pdf_import_seq_index + 1 < len(seq_items):
                next_item = seq_items[st.session_state.pdf_import_seq_index + 1]
                img1 = ae._load_question_image(current)
                img2 = ae._load_question_image(next_item)
                if ae.Image is None:
                    st.warning("PIL bulunamadı.")
                elif img1 and img2:
                    merged = ae.Image.new(
                        "RGB",
                        (max(img1.width, img2.width), img1.height + img2.height),
                        "white",
                    )
                    merged.paste(img1, (0, 0))
                    merged.paste(img2, (0, img1.height))
                    current["image_file"] = ae._save_question_image(merged)
                    current["status"] = "MERGED"
                    next_item["status"] = "MERGED_INTO"
                    next_item["merged_into"] = current.get("question_no")
                    ae.save_question_items(items)
                    st.success("Birlesitirildi.")
                else:
                    st.warning("Gorsel bulunamadı.")

        split_y = st.number_input("Split Y (px)", min_value=10, value=200, step=10, key="pdf_import_seq_split_y")
        manual_no = st.text_input("Yeni soru no (opsiyonel)", key="pdf_import_seq_manual_no")
        if st.button("Split", key="pdf_import_seq_split"):
            img = ae._load_question_image(current)
            if ae.Image is None:
                st.warning("PIL bulunamadı.")
            elif img and 0 < split_y < img.height:
                top = img.crop((0, 0, img.width, int(split_y)))
                bottom = img.crop((0, int(split_y), img.width, img.height))
                current["image_file"] = ae._save_question_image(top)
                current["status"] = "SPLIT"
                new_item = dict(current)
                new_item["image_file"] = ae._save_question_image(bottom)
                new_item["status"] = "SPLIT_NEW"
                new_item["question_no"] = manual_no or f"{current.get('question_no')}-2"
                seq_items.insert(st.session_state.pdf_import_seq_index + 1, new_item)
                ae.save_question_items(items)
                st.success("Bolundu.")
            else:
                st.warning("Gecerli split_y girin.")
