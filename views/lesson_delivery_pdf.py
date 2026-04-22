# -*- coding: utf-8 -*-
"""
SmartCampusAI — 🎓 Ders İşleme Motoru PDF
==========================================
0-12. sınıf tüm kademeler için günlük ders anlatım PDF'i.
Öğretmen Ders Planı + Öğrenci Çalışma Kağıdı = Tek Premium PDF.
GOLD+NAVY Diamond kurumsal tasarım.
"""

from __future__ import annotations

import io
import os
from datetime import datetime

import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════════
# RENK PALETİ — GOLD + NAVY DIAMOND
# ═══════════════════════════════════════════════════════════════════════════════

_GOLD = "#C8952E"
_GOLD_LIGHT = "#E8C975"
_GOLD_BG = "#FFF8E1"
_NAVY = "#0f2744"
_NAVY_MED = "#1e3a5f"
_NAVY_LIGHT = "#2d4a6f"
_INDIGO = "#6366F1"
_SLATE = "#475569"
_TEXT = "#1e293b"
_TEXT_LIGHT = "#64748b"
_WHITE = "#FFFFFF"
_ZEBRA = "#FFFBF0"

# Gün renkleri
_DAY_COLORS = {
    "mon": "#1e40af", "tue": "#059669", "wed": "#7c3aed",
    "thu": "#f59e0b", "fri": "#dc2626",
}
_DAY_NAMES = {
    "mon": "Pazartesi", "tue": "Salı", "wed": "Çarşamba",
    "thu": "Perşembe", "fri": "Cuma",
}

# Faz bilgileri
_PHASE_INFO = {
    "warmup":    {"icon": "🌟", "label": "Warm-up · Isınma",       "minutes": 5,  "lesson": 1},
    "vocabulary":{"icon": "📚", "label": "Vocabulary · Kelime",    "minutes": 15, "lesson": 1},
    "grammar":   {"icon": "📝", "label": "Grammar · Dilbilgisi",   "minutes": 15, "lesson": 1},
    "listening": {"icon": "🎧", "label": "Listening & Speaking",   "minutes": 5,  "lesson": 1},
    "reading":   {"icon": "📖", "label": "Reading · Okuma",        "minutes": 10, "lesson": 2},
    "writing":   {"icon": "✍️", "label": "Writing · Yazma",        "minutes": 10, "lesson": 2},
    "song":      {"icon": "🎵", "label": "Song & Culture",         "minutes": 5,  "lesson": 2},
    "exercises": {"icon": "📝", "label": "Exercises · Alıştırma",  "minutes": 10, "lesson": 2},
    "review":    {"icon": "🏆", "label": "Review · Tekrar",        "minutes": 5,  "lesson": 2},
}

# Öğretmen rehber notları
_TEACHER_GUIDES = {
    "warmup": [
        "Sınıfı selamla: 'Good morning/afternoon, class!'",
        "Günün sorusu sor: 'How are you today?'",
        "Fun Fact'i oku veya projeksiyonda göster",
        "Anahtar kelimeleri tahtaya yaz, tekrarlat",
    ],
    "vocabulary": [
        "Kelimeleri birer birer tanıt: söyle → tekrarlat → anlamını sor",
        "Her kelimeyi 3 kez sesli tekrarlat (choral repetition)",
        "Cümle içinde kullandır: 'Make a sentence with [word]'",
        "Defterlerine yazdır: kelime + anlam + örnek cümle",
    ],
    "grammar": [
        "Kuralı tahtaya yaz veya projeksiyonda göster",
        "2-3 örnek cümle yaz, öğrencilerden de örnek iste",
        "Yanlış örnek ver, 'What's wrong?' diye sor",
        "Fill in the blanks alıştırmasını bireysel yaptır",
    ],
    "listening": [
        "Diyalogu önce dinletin, kitap kapalı",
        "'What did you hear?' — genel anlama sorusu sor",
        "İkinci dinlemede metni göster, takip ettir",
        "Pair work: Öğrenciler ikili diyalog pratik yapsın",
    ],
    "reading": [
        "Önce başlık ve resimlere bak: 'What do you think?'",
        "Sessiz okuma (2 dk), sonra sesli okuma",
        "Anlama sorularını sözlü sor, sonra yazılı yaptır",
        "Bilmediği kelimeleri işaretlettir, birlikte çözün",
    ],
    "writing": [
        "Önce sözlü beyin fırtınası yap",
        "Tahtada örnek cümle yazın (model writing)",
        "Öğrenciler bireysel yazsın (5-7 dk sessiz)",
        "2-3 gönüllü sınıfa okusun",
    ],
    "song": [
        "Şarkıyı önce dinletin, sonra sözlerle birlikte",
        "Hep birlikte söyleyin (en az 2 kez)",
        "Kültür köşesini okuyun, Türkiye ile karşılaştırın",
    ],
    "exercises": [
        "İlk soruyu birlikte çözün (örnek göster)",
        "Kalanı bireysel çözsünler (5-7 dk)",
        "Sınıfça kontrol: 'Number 1, who has the answer?'",
    ],
    "review": [
        "'What did we learn today?' sorusu ile başlat",
        "Mini quiz'i projeksiyonda göster",
        "Ödev varsa açıkla",
        "'Well done, class! See you next time!'",
    ],
}


def generate_lesson_pdf(
    grade_num: int,
    week: int,
    day_key: str,
    curriculum_data: dict | None = None,
    ai_content: dict | None = None,
    weekly_plan_day: dict | None = None,
) -> bytes:
    """Günlük ders anlatım PDF'i üret — Öğretmen Planı + Öğrenci Çalışma Kağıdı."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl
        from reportlab.lib.units import cm, mm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, KeepTogether, HRFlowable,
        )
        from reportlab.graphics.shapes import Drawing, Rect, String
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()

    # Türkçe karakter güvenliği
    def _t(text):
        return str(text) if text else ""

    # ── Veri hazırlığı ──
    cur = curriculum_data or {}
    theme = cur.get("theme", f"Week {week}")
    theme_tr = cur.get("theme_tr", "")
    vocab = cur.get("vocab", [])
    structure = cur.get("structure", "")
    day_name = _DAY_NAMES.get(day_key, day_key)
    day_color_hex = _DAY_COLORS.get(day_key, _NAVY)

    # Kademe bilgisi
    if grade_num == 0:
        grade_label = "Okul Öncesi"
        cefr = "Pre-A1"
    elif grade_num <= 4:
        grade_label = f"{grade_num}. Sınıf — İlkokul"
        cefr = "A1"
    elif grade_num <= 8:
        grade_label = f"{grade_num}. Sınıf — Ortaokul"
        cefr = "A2"
    else:
        grade_label = f"{grade_num}. Sınıf — Lise"
        cefr = "B1"

    unit_num = ((week - 1) // 4) + 1
    now_str = datetime.now().strftime("%d.%m.%Y")

    # Kurum bilgisi
    try:
        from utils.report_utils import get_institution_info
        info = get_institution_info()
        kurum_adi = info.get("name", "SmartCampus AI")
    except Exception:
        kurum_adi = "SmartCampus AI"

    # ── ReportLab renkleri ──
    C_GOLD = rl.HexColor(_GOLD)
    C_GOLD_LIGHT = rl.HexColor(_GOLD_LIGHT)
    C_GOLD_BG = rl.HexColor(_GOLD_BG)
    C_NAVY = rl.HexColor(_NAVY)
    C_NAVY_MED = rl.HexColor(_NAVY_MED)
    C_INDIGO = rl.HexColor(_INDIGO)
    C_DAY = rl.HexColor(day_color_hex)
    C_TEXT = rl.HexColor(_TEXT)
    C_TEXT_LIGHT = rl.HexColor(_TEXT_LIGHT)
    C_WHITE = rl.white
    C_ZEBRA = rl.HexColor(_ZEBRA)
    C_BORDER = rl.HexColor("#e2e8f0")

    # ── Stiller ──
    s_cover_title = ParagraphStyle("CoverTitle", fontName=font_bold, fontSize=24,
                                    leading=30, alignment=TA_CENTER, textColor=C_WHITE, spaceAfter=6)
    s_cover_sub = ParagraphStyle("CoverSub", fontName=font_name, fontSize=13,
                                  leading=17, alignment=TA_CENTER, textColor=C_GOLD_LIGHT, spaceAfter=4)
    s_cover_info = ParagraphStyle("CoverInfo", fontName=font_name, fontSize=10,
                                   leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#cbd5e1"))
    s_section = ParagraphStyle("Section", fontName=font_bold, fontSize=14,
                                leading=18, textColor=C_NAVY, spaceAfter=6, spaceBefore=12)
    s_phase_title = ParagraphStyle("PhaseTitle", fontName=font_bold, fontSize=11,
                                    leading=14, textColor=C_WHITE, spaceAfter=2)
    s_body = ParagraphStyle("Body", fontName=font_name, fontSize=9,
                             leading=12.5, textColor=C_TEXT, spaceAfter=3)
    s_body_sm = ParagraphStyle("BodySm", fontName=font_name, fontSize=8,
                                leading=11, textColor=C_TEXT_LIGHT, spaceAfter=2)
    s_bullet = ParagraphStyle("Bullet", fontName=font_name, fontSize=8.5,
                               leading=12, textColor=C_TEXT, leftIndent=12, spaceAfter=2)
    s_vocab_word = ParagraphStyle("VocabWord", fontName=font_bold, fontSize=10,
                                   leading=13, textColor=C_NAVY, alignment=TA_CENTER)
    s_vocab_def = ParagraphStyle("VocabDef", fontName=font_name, fontSize=8,
                                  leading=11, textColor=C_TEXT_LIGHT, alignment=TA_CENTER)
    s_student_title = ParagraphStyle("StudentTitle", fontName=font_bold, fontSize=16,
                                      leading=20, alignment=TA_CENTER, textColor=C_NAVY, spaceAfter=8)
    s_exercise_q = ParagraphStyle("ExQ", fontName=font_name, fontSize=9.5,
                                   leading=13, textColor=C_TEXT, spaceAfter=4)
    s_line_write = ParagraphStyle("LineWrite", fontName=font_name, fontSize=9,
                                   leading=18, textColor=C_TEXT_LIGHT, spaceAfter=1)
    s_footer = ParagraphStyle("Footer", fontName=font_name, fontSize=7,
                               leading=9, alignment=TA_CENTER, textColor=C_TEXT_LIGHT)

    pw = A4[0] - 3.6 * cm  # available width

    elements = []

    # ══════════════════════════════════════════════════════════════════
    # BÖLÜM 1: KAPAK SAYFASI
    # ══════════════════════════════════════════════════════════════════
    # Üst gold çizgi
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD, spaceAfter=0, spaceBefore=0))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=20, spaceBefore=2))

    # Kurum adı
    elements.append(Spacer(1, 2 * cm))
    elements.append(
        Table(
            [[Paragraph(_t(kurum_adi), s_cover_info)]],
            colWidths=[pw],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("ROUNDEDCORNERS", [8, 8, 8, 8]),
            ]),
        )
    )
    elements.append(Spacer(1, 1.5 * cm))

    # Ana başlık
    elements.append(
        Table(
            [
                [Paragraph(_t("🎓 DERS İŞLEME MOTORU"), s_cover_title)],
                [Paragraph(_t("Günlük Ders Planı + Öğrenci Çalışma Kağıdı"), s_cover_sub)],
            ],
            colWidths=[pw],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_NAVY_MED),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (0, 0), 20),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 16),
                ("ROUNDEDCORNERS", [12, 12, 12, 12]),
                ("LINEABOVE", (0, 0), (-1, 0), 2, C_GOLD),
                ("LINEBELOW", (0, -1), (-1, -1), 2, C_GOLD),
            ]),
        )
    )
    elements.append(Spacer(1, 1.2 * cm))

    # Bilgi kartları
    info_data = [
        [
            Paragraph(_t(f"📘 {grade_label}"), s_cover_info),
            Paragraph(_t(f"📅 Hafta {week} · {day_name}"), s_cover_info),
        ],
        [
            Paragraph(_t(f"📚 Ünite {unit_num}: {theme}"), s_cover_info),
            Paragraph(_t(f"🎯 CEFR: {cefr}"), s_cover_info),
        ],
        [
            Paragraph(_t(f"📝 {structure[:80]}") if structure else Paragraph("", s_cover_info), s_cover_info),
            Paragraph(_t(f"📅 {now_str}"), s_cover_info),
        ],
    ]
    elements.append(
        Table(info_data, colWidths=[pw * 0.5, pw * 0.5],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), rl.HexColor("#111827")),
                  ("TEXTCOLOR", (0, 0), (-1, -1), C_WHITE),
                  ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                  ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                  ("TOPPADDING", (0, 0), (-1, -1), 8),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                  ("GRID", (0, 0), (-1, -1), 0.5, rl.HexColor("#1e3a5f")),
                  ("ROUNDEDCORNERS", [8, 8, 8, 8]),
              ]))
    )
    elements.append(Spacer(1, 1 * cm))

    # Kelime listesi (kapakta)
    if vocab:
        vocab_str = " · ".join(vocab[:12])
        elements.append(
            Table(
                [[Paragraph(_t(f"📚 Kelimeler: {vocab_str}"), s_cover_info)]],
                colWidths=[pw],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), rl.HexColor("#0c1222")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("BOX", (0, 0), (-1, -1), 1, C_GOLD),
                    ("ROUNDEDCORNERS", [8, 8, 8, 8]),
                ]))
        )

    # Alt gold çizgi
    elements.append(Spacer(1, 2 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=2, spaceBefore=0))
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD, spaceAfter=0, spaceBefore=0))

    elements.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════
    # BÖLÜM 2: ÖĞRETMEN DERS PLANI
    # ══════════════════════════════════════════════════════════════════

    # Bölüm başlığı
    elements.append(
        Table(
            [[Paragraph(_t("📋 ÖĞRETMEN DERS PLANI"), s_phase_title)]],
            colWidths=[pw],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LINEBELOW", (0, 0), (-1, -1), 2, C_GOLD),
                ("ROUNDEDCORNERS", [10, 10, 0, 0]),
            ]),
        )
    )
    elements.append(Spacer(1, 6))

    # Ders özet tablosu
    l1_phases = [k for k, v in _PHASE_INFO.items() if v["lesson"] == 1]
    l2_phases = [k for k, v in _PHASE_INFO.items() if v["lesson"] == 2]
    l1_total = sum(_PHASE_INFO[k]["minutes"] for k in l1_phases)
    l2_total = sum(_PHASE_INFO[k]["minutes"] for k in l2_phases)

    overview_rows = [
        [
            Paragraph(_t("1. Ders (Ana Ders)"), ParagraphStyle("", fontName=font_bold, fontSize=9, textColor=C_WHITE)),
            Paragraph(_t(f"{l1_total} dk"), ParagraphStyle("", fontName=font_name, fontSize=9, textColor=C_GOLD_LIGHT)),
            Paragraph(_t("2. Ders (Beceri Lab)"), ParagraphStyle("", fontName=font_bold, fontSize=9, textColor=C_WHITE)),
            Paragraph(_t(f"{l2_total} dk"), ParagraphStyle("", fontName=font_name, fontSize=9, textColor=C_GOLD_LIGHT)),
        ]
    ]
    elements.append(
        Table(overview_rows, colWidths=[pw * 0.3, pw * 0.2, pw * 0.3, pw * 0.2],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), C_NAVY_MED),
                  ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                  ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                  ("TOPPADDING", (0, 0), (-1, -1), 6),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                  ("BOX", (0, 0), (-1, -1), 0.5, C_GOLD),
              ]))
    )
    elements.append(Spacer(1, 10))

    # ── Her faz için detaylı plan ──
    all_phases = l1_phases + l2_phases
    for pi, phase_key in enumerate(all_phases):
        pinfo = _PHASE_INFO[phase_key]
        icon = pinfo["icon"]
        label = pinfo["label"]
        minutes = pinfo["minutes"]
        lesson = pinfo["lesson"]
        guides = _TEACHER_GUIDES.get(phase_key, [])

        # Faz başlık
        bg_color = C_NAVY if lesson == 1 else rl.HexColor("#1a1a3e")
        accent = C_GOLD if lesson == 1 else C_INDIGO

        phase_header = Table(
            [[
                Paragraph(_t(f"{icon} {label}"), s_phase_title),
                Paragraph(_t(f"⏱ {minutes} dk"), ParagraphStyle("", fontName=font_name, fontSize=9,
                           textColor=C_GOLD_LIGHT, alignment=TA_RIGHT)),
            ]],
            colWidths=[pw * 0.7, pw * 0.3],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("RIGHTPADDING", (1, 0), (1, 0), 10),
                ("LINEBELOW", (0, 0), (-1, -1), 1.5, accent),
            ]),
        )

        # Rehber adımları
        guide_elements = []
        for gi, step in enumerate(guides):
            zebra = C_ZEBRA if gi % 2 == 0 else C_WHITE
            guide_elements.append(
                Table(
                    [[Paragraph(_t(f"  {gi+1}. {step}"), s_bullet)]],
                    colWidths=[pw],
                    style=TableStyle([
                        ("BACKGROUND", (0, 0), (-1, -1), zebra),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]),
                )
            )

        # AI içerikten faz verisi
        ai_section = _build_ai_phase_content(phase_key, ai_content, vocab, structure, theme,
                                              s_body, s_body_sm, s_bullet, s_vocab_word, s_vocab_def,
                                              pw, C_GOLD, C_NAVY, C_GOLD_BG, C_BORDER, C_ZEBRA, C_WHITE,
                                              font_name, font_bold, rl, TA_CENTER, TA_LEFT)

        block = [phase_header, Spacer(1, 3)]
        block.extend(guide_elements)
        if ai_section:
            block.append(Spacer(1, 4))
            block.extend(ai_section)
        block.append(Spacer(1, 8))

        elements.append(KeepTogether(block))

    # Weekly plan day etkinlikleri (varsa)
    if weekly_plan_day and weekly_plan_day.get("hours"):
        elements.append(Spacer(1, 10))
        elements.append(
            Table(
                [[Paragraph(_t("📅 HAFTALIK PLAN ETKİNLİKLERİ"), s_phase_title)]],
                colWidths=[pw],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LINEBELOW", (0, 0), (-1, -1), 2, C_GOLD),
                ]),
            )
        )
        for hr in weekly_plan_day["hours"]:
            slot = hr.get("slot", "")
            focus = hr.get("focus", "")
            elements.append(Paragraph(_t(f"<b>{hr.get('hour', '')}. Saat — {slot}:</b> {focus}"), s_body))
            for act in hr.get("activity", []):
                elements.append(Paragraph(_t(f"    • {act}"), s_body_sm))
            if hr.get("tips"):
                elements.append(Paragraph(_t(f"    💡 İpucu: {hr['tips']}"), s_body_sm))
            elements.append(Spacer(1, 4))

        # Ödev
        hw = weekly_plan_day.get("homework", [])
        if hw:
            elements.append(Paragraph(_t("<b>📝 Ödev:</b>"), s_body))
            for h in hw:
                elements.append(Paragraph(_t(f"    • {h}"), s_body_sm))

    elements.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════
    # BÖLÜM 3: ÖĞRENCİ ÇALIŞMA KAĞIDI
    # ══════════════════════════════════════════════════════════════════

    # Başlık
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD, spaceAfter=2))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=10))

    elements.append(
        Table(
            [
                [Paragraph(_t("✏️ ÖĞRENCİ ÇALIŞMA KAĞIDI"), s_student_title)],
                [Paragraph(_t(f"Unit {unit_num}: {theme} ({theme_tr}) — {grade_label} — Hafta {week} {day_name}"),
                           ParagraphStyle("", fontName=font_name, fontSize=9, textColor=C_TEXT_LIGHT,
                                          alignment=TA_CENTER))],
            ],
            colWidths=[pw],
            style=TableStyle([
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
                ("LINEBELOW", (0, -1), (-1, -1), 1, C_GOLD),
            ]),
        )
    )

    # Ad Soyad / Sınıf satırı
    elements.append(Spacer(1, 8))
    elements.append(
        Table(
            [[
                Paragraph(_t("Ad Soyad: ________________________________"), s_body),
                Paragraph(_t(f"Sınıf / Şube: {grade_num} / ____"), s_body),
                Paragraph(_t(f"Tarih: {now_str}"), s_body),
            ]],
            colWidths=[pw * 0.4, pw * 0.3, pw * 0.3],
            style=TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 0), (-1, -1), C_GOLD_BG),
            ]),
        )
    )
    elements.append(Spacer(1, 12))

    # ── A) Kelime Bölümü ──
    if vocab:
        elements.append(Paragraph(_t("📚 A) VOCABULARY — Kelimeleri öğren ve yaz"), s_section))

        ve = (ai_content or {}).get("vocabulary_enrichment", {})
        defs = ve.get("definitions", []) if isinstance(ve, dict) else []

        vocab_rows = []
        row = []
        cols_per_row = 3
        for vi, w in enumerate(vocab[:12]):
            d = next((dd for dd in defs if dd.get("word", "").lower() == w.lower()), None)
            meaning = d.get("turkish_hint", d.get("definition", "")) if d else ""
            cell_content = Paragraph(_t(f"<b>{w}</b><br/><font size='7' color='#64748b'>{meaning[:40]}</font>"),
                                      ParagraphStyle("", fontName=font_name, fontSize=9, textColor=C_NAVY,
                                                      alignment=TA_CENTER, leading=13))
            row.append(cell_content)
            if len(row) == cols_per_row:
                vocab_rows.append(row)
                row = []
        if row:
            while len(row) < cols_per_row:
                row.append(Paragraph("", s_body))
            vocab_rows.append(row)

        if vocab_rows:
            cw = pw / cols_per_row
            elements.append(
                Table(vocab_rows, colWidths=[cw] * cols_per_row,
                      style=TableStyle([
                          ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
                          ("BACKGROUND", (0, 0), (-1, -1), C_GOLD_BG),
                          ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                          ("TOPPADDING", (0, 0), (-1, -1), 8),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                      ]))
            )
        elements.append(Spacer(1, 10))

    # ── B) Dilbilgisi Bölümü ──
    gf = (ai_content or {}).get("grammar_focus", {})
    if isinstance(gf, dict) and gf.get("rule"):
        elements.append(Paragraph(_t("📝 B) GRAMMAR — Dilbilgisi kuralı"), s_section))
        elements.append(
            Table(
                [[Paragraph(_t(f"<b>Kural:</b> {gf['rule']}"), s_body)]],
                colWidths=[pw],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), rl.HexColor("#f0fdf4")),
                    ("BOX", (0, 0), (-1, -1), 1, rl.HexColor("#059669")),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ]),
            )
        )
        if gf.get("examples"):
            for ei, ex in enumerate(gf["examples"][:4]):
                elements.append(Paragraph(_t(f"    ✅ {ex}"), s_bullet))
        elements.append(Spacer(1, 10))

    # ── C) Alıştırmalar ──
    ex = (ai_content or {}).get("exercises", {})
    if isinstance(ex, dict):
        elements.append(Paragraph(_t("✍️ C) EXERCISES — Alıştırmalar"), s_section))

        # Fill in the blanks
        fb = ex.get("fill_blanks", [])
        if fb:
            elements.append(Paragraph(_t("<b>Fill in the blanks:</b>"), s_body))
            for fi, item in enumerate(fb[:6]):
                sent = item.get("sentence", "") if isinstance(item, dict) else str(item)
                elements.append(Paragraph(_t(f"  {fi+1}) {sent}"), s_exercise_q))

        # Matching
        match = ex.get("matching", [])
        if match:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(_t("<b>Match the columns:</b>"), s_body))
            match_rows = []
            for mi, m in enumerate(match[:8]):
                if isinstance(m, dict):
                    match_rows.append([
                        Paragraph(_t(f"{mi+1}. {m.get('left', '')}"), s_body),
                        Paragraph(_t("___"), s_body),
                        Paragraph(_t(f"{chr(65+mi)}. {m.get('right', '')}"), s_body),
                    ])
            if match_rows:
                elements.append(
                    Table(match_rows, colWidths=[pw * 0.4, pw * 0.1, pw * 0.5],
                          style=TableStyle([
                              ("GRID", (0, 0), (-1, -1), 0.3, C_BORDER),
                              ("TOPPADDING", (0, 0), (-1, -1), 4),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                          ]))
                )

        # Writing prompt
        wp = ex.get("writing_prompt", "")
        if wp:
            elements.append(Spacer(1, 8))
            elements.append(Paragraph(_t(f"<b>✍️ Writing:</b> {wp}"), s_body))
            for _ in range(5):
                elements.append(Paragraph(_t("_" * 80), s_line_write))

        elements.append(Spacer(1, 10))

    # ── D) Okuma Metni ──
    rp = (ai_content or {}).get("reading_passage", {})
    if isinstance(rp, dict) and rp.get("text"):
        elements.append(Paragraph(_t("📖 D) READING — Okuma Parçası"), s_section))
        elements.append(
            Table(
                [
                    [Paragraph(_t(f"<b>{rp.get('title', 'Reading Passage')}</b>"),
                               ParagraphStyle("", fontName=font_bold, fontSize=10, textColor=C_NAVY))],
                    [Paragraph(_t(rp["text"][:600]), s_body)],
                ],
                colWidths=[pw],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), rl.HexColor("#f8fafc")),
                    ("BOX", (0, 0), (-1, -1), 1, C_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("LINEBELOW", (0, 0), (0, 0), 0.5, C_GOLD),
                ]),
            )
        )
        # Sorular
        qs = rp.get("questions", [])
        if qs:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(_t("<b>Comprehension Questions:</b>"), s_body))
            for qi, q in enumerate(qs[:5]):
                elements.append(Paragraph(_t(f"  {qi+1}) {q}"), s_exercise_q))
                elements.append(Paragraph(_t("    _______________________________________"), s_line_write))

    # Footer
    elements.append(Spacer(1, 1.5 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=4))
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD, spaceAfter=6))
    elements.append(Paragraph(
        _t(f"{kurum_adi} — 🎓 Ders İşleme Motoru — {grade_label} — {now_str}"),
        s_footer,
    ))

    # ── PDF oluştur ──
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title=f"Ders Isleme Motoru - {grade_label} - Hafta {week} {day_name}",
        author=kurum_adi,
    )
    doc.build(elements)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
# YILLIK PLAN PDF — SLOT BAZLI (MAIN COURSE / SKILLS LAB / NATIVE SPEAKER)
# ═══════════════════════════════════════════════════════════════════════════════

_SLOT_STYLES = {
    "MAIN COURSE": {"icon": "📗", "label": "Main Course — Ana Ders", "color": "#1e40af", "bg": "#eff6ff"},
    "SKILLS LAB": {"icon": "📕", "label": "Skills Lab — Beceri Lab", "color": "#7c3aed", "bg": "#f5f3ff"},
    "NATIVE SPEAKER": {"icon": "🌍", "label": "Native Speaker", "color": "#b45309", "bg": "#fffbeb"},
}

_MONTH_NAMES = {
    1: "Eylül", 2: "Eylül", 3: "Eylül", 4: "Eylül",
    5: "Ekim", 6: "Ekim", 7: "Ekim", 8: "Ekim",
    9: "Kasım", 10: "Kasım", 11: "Kasım", 12: "Kasım",
    13: "Aralık", 14: "Aralık", 15: "Aralık", 16: "Aralık",
    17: "Ocak", 18: "Ocak", 19: "Ocak", 20: "Ocak",
    21: "Şubat", 22: "Şubat", 23: "Şubat", 24: "Şubat",
    25: "Mart", 26: "Mart", 27: "Mart", 28: "Mart",
    29: "Nisan", 30: "Nisan", 31: "Nisan", 32: "Nisan",
    33: "Mayıs", 34: "Mayıs", 35: "Mayıs", 36: "Mayıs",
}


def generate_yearly_plan_pdf(grade_num: int, slot_filter: str | None = None) -> bytes:
    """36 haftalık yıllık plan PDF'i — slot bazlı filtrelenmiş."""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors as rl
        from reportlab.lib.units import cm, mm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, KeepTogether, HRFlowable,
        )
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        return b""

    import json as _json
    from views.yd_core import _WP_PATH

    font_name, font_bold = ensure_turkish_pdf_fonts()
    _t = lambda text: str(text) if text else ""

    # Weekly plans yükle
    try:
        with open(_WP_PATH, "r", encoding="utf-8") as f:
            all_plans = _json.load(f)
        grade_plans = all_plans.get(str(grade_num), [])
    except Exception:
        return b""
    if not grade_plans:
        return b""

    # Kurum bilgisi
    try:
        from utils.report_utils import get_institution_info
        kurum_adi = get_institution_info().get("name", "SmartCampus AI")
    except Exception:
        kurum_adi = "SmartCampus AI"

    # Kademe
    if grade_num == 0:
        grade_label = "Okul Öncesi"
    elif grade_num <= 4:
        grade_label = f"{grade_num}. Sınıf — İlkokul"
    elif grade_num <= 8:
        grade_label = f"{grade_num}. Sınıf — Ortaokul"
    else:
        grade_label = f"{grade_num}. Sınıf — Lise"

    slot_style = _SLOT_STYLES.get(slot_filter, {"icon": "📦", "label": "Tüm Dersler", "color": "#0f2744", "bg": "#f8fafc"})
    now_str = datetime.now().strftime("%d.%m.%Y")

    # Renkler
    C_GOLD = rl.HexColor(_GOLD)
    C_GOLD_LIGHT = rl.HexColor(_GOLD_LIGHT)
    C_NAVY = rl.HexColor(_NAVY)
    C_NAVY_MED = rl.HexColor(_NAVY_MED)
    C_WHITE = rl.white
    C_BORDER = rl.HexColor("#e2e8f0")
    C_ZEBRA = rl.HexColor(_ZEBRA)
    C_SLOT = rl.HexColor(slot_style["color"])
    C_SLOT_BG = rl.HexColor(slot_style["bg"])

    # Stiller
    s_cover_title = ParagraphStyle("YCT", fontName=font_bold, fontSize=22,
                                    leading=28, alignment=TA_CENTER, textColor=C_WHITE, spaceAfter=6)
    s_cover_sub = ParagraphStyle("YCS", fontName=font_name, fontSize=12,
                                  leading=16, alignment=TA_CENTER, textColor=C_GOLD_LIGHT)
    s_cover_info = ParagraphStyle("YCI", fontName=font_name, fontSize=10,
                                   leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#cbd5e1"))
    s_week_title = ParagraphStyle("YWT", fontName=font_bold, fontSize=11,
                                   leading=14, textColor=C_WHITE, spaceAfter=2)
    s_day_title = ParagraphStyle("YDT", fontName=font_bold, fontSize=9,
                                  leading=12, textColor=C_SLOT)
    s_body = ParagraphStyle("YB", fontName=font_name, fontSize=8,
                             leading=11, textColor=rl.HexColor(_TEXT))
    s_body_sm = ParagraphStyle("YBS", fontName=font_name, fontSize=7,
                                leading=9.5, textColor=rl.HexColor(_TEXT_LIGHT))
    s_cell = ParagraphStyle("YC", fontName=font_name, fontSize=7.5,
                             leading=10, textColor=rl.HexColor(_TEXT))
    s_cell_bold = ParagraphStyle("YCB", fontName=font_bold, fontSize=7.5,
                                  leading=10, textColor=rl.HexColor(_NAVY))
    s_footer = ParagraphStyle("YF", fontName=font_name, fontSize=7,
                               leading=9, alignment=TA_CENTER, textColor=rl.HexColor(_TEXT_LIGHT))

    pw = A4[0] - 3.6 * cm

    elements = []

    # ══════════════════════════════════════════════════════════════════
    # KAPAK
    # ══════════════════════════════════════════════════════════════════
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD, spaceAfter=0))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=20))
    elements.append(Spacer(1, 2 * cm))

    elements.append(
        Table([[Paragraph(_t(kurum_adi), s_cover_info)]],
              colWidths=[pw],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                  ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                  ("TOPPADDING", (0, 0), (-1, -1), 8),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
              ]))
    )
    elements.append(Spacer(1, 1.5 * cm))

    elements.append(
        Table([
            [Paragraph(_t(f"{slot_style['icon']} YILLIK DERS PLANI"), s_cover_title)],
            [Paragraph(_t(f"{slot_style['label']}"), s_cover_sub)],
            [Paragraph(_t(f"{grade_label} — 36 Hafta — 2025-2026 Eğitim Öğretim Yılı"), s_cover_info)],
        ], colWidths=[pw],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_NAVY_MED),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (0, 0), 20),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 16),
                ("LINEABOVE", (0, 0), (-1, 0), 2, C_GOLD),
                ("LINEBELOW", (0, -1), (-1, -1), 2, C_GOLD),
            ]))
    )
    elements.append(Spacer(1, 1.5 * cm))

    # İçindekiler özeti
    summary_rows = []
    for w_num in range(1, 37):
        wp = next((w for w in grade_plans if w.get("week") == w_num), None)
        if not wp:
            continue
        theme = wp.get("unit_theme", wp.get("theme", ""))
        month = _MONTH_NAMES.get(w_num, "")
        unit = ((w_num - 1) // 4) + 1
        # Bu haftada kaç saat bu slot'tan var?
        hour_count = 0
        for dk in ["mon", "tue", "wed", "thu", "fri"]:
            day = wp.get("days", {}).get(dk, {})
            for hr in day.get("hours", []):
                if slot_filter is None or hr.get("slot", "") == slot_filter:
                    hour_count += 1
        if hour_count == 0 and slot_filter:
            continue
        bg = C_ZEBRA if w_num % 2 == 0 else C_WHITE
        summary_rows.append([
            Paragraph(_t(f"H{w_num}"), s_cell_bold),
            Paragraph(_t(month), s_cell),
            Paragraph(_t(f"Ü{unit}"), s_cell),
            Paragraph(_t(theme[:40]), s_cell),
            Paragraph(_t(f"{hour_count} saat"), s_cell),
        ])

    if summary_rows:
        header = [
            Paragraph(_t("Hafta"), s_cell_bold),
            Paragraph(_t("Ay"), s_cell_bold),
            Paragraph(_t("Ünite"), s_cell_bold),
            Paragraph(_t("Tema"), s_cell_bold),
            Paragraph(_t("Saat"), s_cell_bold),
        ]
        elements.append(
            Table([header] + summary_rows,
                  colWidths=[pw * 0.1, pw * 0.12, pw * 0.1, pw * 0.55, pw * 0.13],
                  style=TableStyle([
                      ("GRID", (0, 0), (-1, -1), 0.3, C_BORDER),
                      ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
                      ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
                      ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                      ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                      ("TOPPADDING", (0, 0), (-1, -1), 3),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                      ("FONTSIZE", (0, 0), (-1, -1), 7),
                  ] + [("BACKGROUND", (0, i+1), (-1, i+1), C_ZEBRA if i % 2 == 0 else C_WHITE)
                       for i in range(len(summary_rows))]))
        )

    elements.append(Spacer(1, 1 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=2))
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD))
    elements.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════
    # HAFTALIK DETAYLAR — 36 HAFTA
    # ══════════════════════════════════════════════════════════════════
    for w_num in range(1, 37):
        wp = next((w for w in grade_plans if w.get("week") == w_num), None)
        if not wp:
            continue

        theme = wp.get("unit_theme", wp.get("theme", ""))
        grammar = wp.get("grammar_focus", "")
        unit = ((w_num - 1) // 4) + 1
        month = _MONTH_NAMES.get(w_num, "")

        # Bu haftada filtreye uyan ders var mı?
        has_hours = False
        for dk in ["mon", "tue", "wed", "thu", "fri"]:
            day = wp.get("days", {}).get(dk, {})
            for hr in day.get("hours", []):
                if slot_filter is None or hr.get("slot", "") == slot_filter:
                    has_hours = True
                    break
            if has_hours:
                break
        if not has_hours:
            continue

        # Hafta başlık
        week_block = []
        week_block.append(
            Table([[
                Paragraph(_t(f"📅 Hafta {w_num} — Ünite {unit}: {theme}"), s_week_title),
                Paragraph(_t(f"{month} | {grammar[:50]}"),
                           ParagraphStyle("", fontName=font_name, fontSize=8, textColor=C_GOLD_LIGHT,
                                          alignment=TA_RIGHT)),
            ]], colWidths=[pw * 0.6, pw * 0.4],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (0, 0), 10),
                    ("RIGHTPADDING", (1, 0), (1, 0), 10),
                    ("LINEBELOW", (0, 0), (-1, -1), 2, C_GOLD),
                ]))
        )
        week_block.append(Spacer(1, 4))

        # Günler
        for dk in ["mon", "tue", "wed", "thu", "fri"]:
            day = wp.get("days", {}).get(dk, {})
            day_name = day.get("day_name", _DAY_NAMES.get(dk, dk))
            hours = day.get("hours", [])
            filtered_hours = [h for h in hours if slot_filter is None or h.get("slot", "") == slot_filter]
            if not filtered_hours:
                continue

            day_color = rl.HexColor(_DAY_COLORS.get(dk, _NAVY))

            for hr in filtered_hours:
                slot = hr.get("slot", "")
                focus = hr.get("focus", "")
                duration = hr.get("duration", "40 dk")
                activities = hr.get("activity", [])
                materials = hr.get("materials", [])
                tips = hr.get("tips", "")

                # Saat başlık satırı
                hour_header = Table([[
                    Paragraph(_t(f"{day_name} — {hr.get('hour', '')}. Saat"),
                               ParagraphStyle("", fontName=font_bold, fontSize=8, textColor=day_color)),
                    Paragraph(_t(f"[{slot}] {duration}"),
                               ParagraphStyle("", fontName=font_name, fontSize=7.5, textColor=C_SLOT,
                                              alignment=TA_RIGHT)),
                ]], colWidths=[pw * 0.45, pw * 0.55],
                    style=TableStyle([
                        ("BACKGROUND", (0, 0), (-1, -1), C_SLOT_BG),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ("LEFTPADDING", (0, 0), (0, 0), 8),
                        ("RIGHTPADDING", (1, 0), (1, 0), 8),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.5, C_SLOT),
                    ]))
                week_block.append(hour_header)

                # Odak
                week_block.append(Paragraph(_t(f"<b>Odak:</b> {focus}"), s_body))

                # Etkinlikler
                for ai_idx, act in enumerate(activities):
                    zebra = C_ZEBRA if ai_idx % 2 == 0 else C_WHITE
                    week_block.append(
                        Table([[Paragraph(_t(f"  • {act}"), s_body_sm)]],
                              colWidths=[pw],
                              style=TableStyle([
                                  ("BACKGROUND", (0, 0), (-1, -1), zebra),
                                  ("TOPPADDING", (0, 0), (-1, -1), 2),
                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 12),
                              ]))
                    )

                # Materyaller
                if materials:
                    mat_str = " | ".join(materials)
                    week_block.append(Paragraph(_t(f"  📦 <i>Materyaller: {mat_str}</i>"), s_body_sm))

                # İpucu
                if tips:
                    week_block.append(Paragraph(_t(f"  💡 <i>{tips[:150]}</i>"), s_body_sm))

                week_block.append(Spacer(1, 4))

            # Ödev
            hw = day.get("homework", [])
            if hw:
                for h in hw:
                    week_block.append(Paragraph(_t(f"  📝 {h[:150]}"), s_body_sm))

        week_block.append(Spacer(1, 6))

        # Hafta separator
        week_block.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=6))

        elements.extend(week_block)

        # Her 4 haftada sayfa kır (ünite sonu)
        if w_num % 4 == 0 and w_num < 36:
            elements.append(PageBreak())

    # Footer
    elements.append(Spacer(1, 1 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_NAVY, spaceAfter=2))
    elements.append(HRFlowable(width="100%", thickness=3, color=C_GOLD, spaceAfter=4))
    elements.append(Paragraph(
        _t(f"{kurum_adi} — {slot_style['icon']} {slot_style['label']} — {grade_label} — {now_str}"),
        s_footer,
    ))

    # PDF oluştur
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title=f"Yillik Plan - {grade_label} - {slot_style['label']}",
        author=kurum_adi,
    )
    doc.build(elements)
    return buf.getvalue()


def _build_ai_phase_content(phase_key, ai, vocab, structure, theme,
                             s_body, s_body_sm, s_bullet, s_vocab_word, s_vocab_def,
                             pw, C_GOLD, C_NAVY, C_GOLD_BG, C_BORDER, C_ZEBRA, C_WHITE,
                             font_name, font_bold, rl, TA_CENTER, TA_LEFT):
    """AI içerikten faz bazlı PDF elementleri üret."""
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph, Table, Spacer

    if not ai:
        return []

    elements = []

    if phase_key == "vocabulary":
        ve = ai.get("vocabulary_enrichment", {})
        defs = ve.get("definitions", []) if isinstance(ve, dict) else []
        if defs:
            rows = []
            for d in defs[:10]:
                rows.append([
                    Paragraph(str(d.get("word", "")), ParagraphStyle("", fontName=font_bold, fontSize=8.5,
                              textColor=rl.HexColor("#0f2744"), alignment=TA_LEFT)),
                    Paragraph(str(d.get("definition", "")), s_body_sm),
                    Paragraph(str(d.get("example", "")), ParagraphStyle("", fontName=font_name, fontSize=7.5,
                              textColor=rl.HexColor("#64748b"), leading=10)),
                ])
            if rows:
                t = Table(rows, colWidths=[pw * 0.2, pw * 0.35, pw * 0.45],
                          style=[
                              ("GRID", (0, 0), (-1, -1), 0.3, C_BORDER),
                              ("BACKGROUND", (0, 0), (0, -1), C_GOLD_BG),
                              ("TOPPADDING", (0, 0), (-1, -1), 3),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                              ("LEFTPADDING", (0, 0), (-1, -1), 4),
                          ])
                elements.append(t)

    elif phase_key == "grammar":
        gf = ai.get("grammar_focus", {})
        if isinstance(gf, dict) and gf.get("rule"):
            elements.append(
                Table(
                    [[Paragraph(f"<b>Kural:</b> {gf['rule']}", s_body)]],
                    colWidths=[pw],
                    style=[
                        ("BACKGROUND", (0, 0), (-1, -1), rl.HexColor("#f0fdf4")),
                        ("BOX", (0, 0), (-1, -1), 0.5, rl.HexColor("#059669")),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ],
                )
            )
            for ex in (gf.get("examples") or [])[:3]:
                elements.append(Paragraph(f"  ✅ {ex}", s_bullet))

    elif phase_key == "listening":
        dlg = ai.get("dialogue", {})
        if isinstance(dlg, dict) and dlg.get("lines"):
            speakers = dlg.get("speakers", ["A", "B"])
            for line in dlg["lines"][:8]:
                sp = speakers[line.get("speaker", 0)] if line.get("speaker", 0) < len(speakers) else "?"
                elements.append(Paragraph(f"<b>{sp}:</b> {line.get('text', '')}", s_body_sm))

    elif phase_key == "reading":
        rp = ai.get("reading_passage", ai.get("story", {}))
        if isinstance(rp, dict) and rp.get("text"):
            elements.append(Paragraph(f"<b>{rp.get('title', '')}</b>", s_body))
            elements.append(Paragraph(str(rp["text"])[:300] + "...", s_body_sm))

    elif phase_key == "song":
        sc = ai.get("song_chant", {})
        if isinstance(sc, dict) and sc.get("lyrics"):
            elements.append(Paragraph(f"<b>🎵 {sc.get('title', 'Song')}</b>", s_body))
            for line in str(sc["lyrics"]).split("\n")[:6]:
                elements.append(Paragraph(f"  ♪ {line}", s_body_sm))

    elif phase_key == "warmup":
        ff = ai.get("fun_fact", "")
        if ff:
            elements.append(Paragraph(f"<b>💡 Fun Fact:</b> {str(ff)[:200]}", s_body_sm))

    return elements


# ═══════════════════════════════════════════════════════════════════════════════
# STREAMLIT UI — PDF İndirme Ekranı
# ═══════════════════════════════════════════════════════════════════════════════

def render_lesson_pdf_tab():
    """🎓 Ders İşleme Motoru PDF — Streamlit UI."""
    from utils.ui_common import styled_header
    from views.yd_content import _CURRICULUM
    from views.yd_core import _WP_PATH

    styled_header("🎓 Ders İşleme Motoru PDF",
                  "0-12. Sınıf — Günlük Ders Planı + Öğrenci Çalışma Kağıdı — Premium Kurumsal PDF")

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f2744,#1e3a5f);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:14px;'
        'border:1.5px solid rgba(200,149,46,.3);">'
        '<div style="font-size:.88rem;color:#E8C975;">📋 Öğretmen ders planı (fazlar + rehber notları + AI içerik)'
        ' + ✏️ Öğrenci çalışma kağıdı (kelimeler + grammar + alıştırmalar + okuma)</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Sınıf seçimi ──
    grade_options = {"Okul Öncesi": 0, **{f"{i}. Sınıf": i for i in range(1, 13)}}
    c1, c2, c3 = st.columns(3)
    with c1:
        sel_label = st.selectbox("📘 Sınıf:", list(grade_options.keys()), index=5, key="lp_grade")
        sel_grade = grade_options[sel_label]
    level = f"grade{sel_grade}" if sel_grade > 0 else "preschool"
    curriculum = _CURRICULUM.get(level, [])

    with c2:
        max_week = len(curriculum) if curriculum else 36
        sel_week = st.selectbox("📅 Hafta:", list(range(1, max_week + 1)), key="lp_week")
    with c3:
        sel_day = st.selectbox("🗓️ Gün:", list(_DAY_NAMES.keys()),
                                format_func=lambda x: _DAY_NAMES[x], key="lp_day")

    if not curriculum:
        st.warning("Bu sınıf için müfredat bulunamadı.")
        return

    # Hafta verisi
    week_data = next((w for w in curriculum if w.get("week") == sel_week), None)
    if not week_data:
        week_data = curriculum[min(sel_week - 1, len(curriculum) - 1)]

    theme = week_data.get("theme", "")
    theme_tr = week_data.get("theme_tr", "")
    vocab = week_data.get("vocab", [])
    structure = week_data.get("structure", "")

    # Önizleme
    st.markdown(
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;'
        f'padding:12px 16px;margin:8px 0;">'
        f'<b>📚 Ünite:</b> {theme} ({theme_tr}) &nbsp;|&nbsp; '
        f'<b>📝 Gramer:</b> {structure[:60] if structure else "—"} &nbsp;|&nbsp; '
        f'<b>📚 Kelime:</b> {len(vocab)} adet</div>',
        unsafe_allow_html=True,
    )

    # AI içerik
    ai_content = None
    unit_num = ((sel_week - 1) // 4) + 1
    try:
        from models.lesson_delivery import load_unit_content
        ai_content = load_unit_content(sel_grade, unit_num)
    except Exception:
        pass

    # Weekly plan day verisi
    wp_day = None
    try:
        import json
        if os.path.exists(_WP_PATH):
            with open(_WP_PATH, "r", encoding="utf-8") as f:
                all_plans = json.load(f)
            grade_plans = all_plans.get(str(sel_grade), [])
            for wp in grade_plans:
                if wp.get("week") == sel_week:
                    wp_day = wp.get("days", {}).get(sel_day)
                    break
    except Exception:
        pass

    # ── PDF Üret ──
    _pc1, _pc2, _pc3 = st.columns([0.35, 0.35, 0.3])
    with _pc1:
        if st.button("📄 PDF Oluştur", key="lp_generate", type="primary", use_container_width=True):
            with st.spinner("Premium PDF oluşturuluyor..."):
                pdf_bytes = generate_lesson_pdf(
                    grade_num=sel_grade,
                    week=sel_week,
                    day_key=sel_day,
                    curriculum_data=week_data,
                    ai_content=ai_content,
                    weekly_plan_day=wp_day,
                )
                if pdf_bytes:
                    st.session_state["_lp_pdf"] = pdf_bytes
                    st.session_state["_lp_info"] = {
                        "grade": sel_grade, "week": sel_week,
                        "day": sel_day, "theme": theme,
                    }
                    st.success("✅ PDF hazır!")
                else:
                    st.error("PDF oluşturulamadı. ReportLab kurulu mu?")

    # İndir butonu
    pdf_data = st.session_state.get("_lp_pdf")
    if pdf_data:
        lp_info = st.session_state.get("_lp_info", {})
        fname = (f"Ders_Isleme_Sinif{lp_info.get('grade', sel_grade)}_"
                 f"H{lp_info.get('week', sel_week)}_{lp_info.get('day', sel_day)}.pdf")
        with _pc2:
            st.download_button(
                "📥 PDF İndir", pdf_data, file_name=fname,
                mime="application/pdf", key="lp_download", use_container_width=True,
            )

    # ── Toplu PDF (Tüm Hafta) ──
    st.markdown("---")
    st.markdown("##### 📦 Toplu PDF — Haftanın Tüm Günleri")
    if st.button("📦 Tüm Haftayı Oluştur (5 Gün)", key="lp_bulk"):
        with st.spinner("5 günlük PDF oluşturuluyor..."):
            try:
                from PyPDF2 import PdfMerger
                merger = PdfMerger()
                for dk in ["mon", "tue", "wed", "thu", "fri"]:
                    wp_d = None
                    try:
                        import json as _j2
                        if os.path.exists(_WP_PATH):
                            with open(_WP_PATH, "r", encoding="utf-8") as f2:
                                ap2 = _j2.load(f2)
                            gp2 = ap2.get(str(sel_grade), [])
                            for wp2 in gp2:
                                if wp2.get("week") == sel_week:
                                    wp_d = wp2.get("days", {}).get(dk)
                                    break
                    except Exception:
                        pass

                    pdf_b = generate_lesson_pdf(
                        grade_num=sel_grade, week=sel_week, day_key=dk,
                        curriculum_data=week_data, ai_content=ai_content,
                        weekly_plan_day=wp_d,
                    )
                    if pdf_b:
                        merger.append(io.BytesIO(pdf_b))

                out = io.BytesIO()
                merger.write(out)
                merger.close()
                bulk_bytes = out.getvalue()

                if bulk_bytes:
                    st.download_button(
                        "📥 Haftalık PDF İndir",
                        bulk_bytes,
                        file_name=f"Ders_Isleme_Sinif{sel_grade}_Hafta{sel_week}_TumGunler.pdf",
                        mime="application/pdf",
                        key="lp_bulk_dl",
                    )
                    st.success(f"✅ Hafta {sel_week} — 5 günlük PDF hazır!")
            except ImportError:
                st.error("PyPDF2 kurulu değil. `pip install PyPDF2` çalıştırın.")

    # ══════════════════════════════════════════════════════════════════
    # YILLIK PLAN PDF — MAIN COURSE / SKILLS LAB / NATIVE SPEAKER
    # ══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f2744,#1e3a5f);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:12px;'
        'border:1.5px solid rgba(200,149,46,.3);">'
        '<div style="font-size:1.05rem;font-weight:700;color:#E8C975;">'
        '📅 Yıllık Plan PDF — Slot Bazlı</div>'
        '<div style="font-size:.82rem;color:#cbd5e1;margin-top:3px;">'
        '36 hafta × gün gün — Main Course / Skills Lab / Native Speaker ayrı ayrı</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    _yp_c1, _yp_c2 = st.columns([0.5, 0.5])
    with _yp_c1:
        yp_grade_label = st.selectbox("📘 Sınıf:", list(grade_options.keys()), index=5, key="yp_grade")
        yp_grade = grade_options[yp_grade_label]
    with _yp_c2:
        yp_slot = st.selectbox(
            "📋 Plan Türü:",
            ["MAIN COURSE", "SKILLS LAB", "NATIVE SPEAKER", "TÜMÜ"],
            format_func=lambda x: {
                "MAIN COURSE": "📗 Main Course (Ana Ders)",
                "SKILLS LAB": "📕 Skills Lab (Beceri Lab)",
                "NATIVE SPEAKER": "🌍 Native Speaker",
                "TÜMÜ": "📦 Tümü (Birleşik)",
            }.get(x, x),
            key="yp_slot",
        )

    yp_cols = st.columns(3)
    with yp_cols[0]:
        if st.button("📄 Yıllık Plan PDF Oluştur", key="yp_generate", type="primary", use_container_width=True):
            with st.spinner(f"Yıllık plan oluşturuluyor — {yp_slot}..."):
                pdf_bytes = generate_yearly_plan_pdf(
                    grade_num=yp_grade,
                    slot_filter=yp_slot if yp_slot != "TÜMÜ" else None,
                )
                if pdf_bytes:
                    st.session_state["_yp_pdf"] = pdf_bytes
                    st.session_state["_yp_info"] = {"grade": yp_grade, "slot": yp_slot}
                    st.success("✅ Yıllık plan PDF hazır!")
                else:
                    st.error("PDF oluşturulamadı.")

    yp_pdf = st.session_state.get("_yp_pdf")
    if yp_pdf:
        yp_info = st.session_state.get("_yp_info", {})
        slot_tag = yp_info.get("slot", "ALL").replace(" ", "_")
        with yp_cols[1]:
            st.download_button(
                "📥 Yıllık Plan İndir",
                yp_pdf,
                file_name=f"Yillik_Plan_Sinif{yp_info.get('grade', yp_grade)}_{slot_tag}.pdf",
                mime="application/pdf",
                key="yp_download",
                use_container_width=True,
            )
