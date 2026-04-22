"""
SmartCampusAI — Premium Book PDF Engine
========================================
4 PDF book generators: Main Course, Workbook, Reading Book, Vocabulary Book.
Her ünite ~20 sayfa — basıma hazır profesyonel kalite.
book_design_system.py ile tam entegre.

Sayfa kayması sorunu çözüldü: KeepTogether ile section gruplandırma.
"""

from __future__ import annotations

import io
import math
import random
from typing import Any

from reportlab.lib import colors as rl_colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, NextPageTemplate, CondPageBreak,
)

from utils.shared_data import ensure_turkish_pdf_fonts
from utils.book_design_system import (
    FONT_FAMILY, GRADE_TIERS, COLORS, SECTION_COLORS,
    UNIT_COLOR_SEQUENCE, PAGE_LAYOUT, BOX_STYLES, TABLE_STYLES,
    HEADER_FOOTER, COVER_DESIGN, GRADE_CEFR, UNIT_SECTIONS,
    BASE_TYPOGRAPHY,
    get_tier_for_grade, get_color_hex, get_section_colors,
    get_unit_color, get_grade_config, get_tier_name,
    get_sections_for_grade, build_reportlab_colors,
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

BOOK_TITLES: dict[int, dict[str, str]] = {
    0:  {"main": "Early Steps",     "workbook": "Early Steps Workbook",     "reading": "Early Steps Reading",     "vocab": "Early Steps Vocabulary"},
    1:  {"main": "Bright Start 1",  "workbook": "Bright Start 1 Workbook", "reading": "Bright Start 1 Reading",  "vocab": "Bright Start 1 Vocabulary"},
    2:  {"main": "Bright Start 2",  "workbook": "Bright Start 2 Workbook", "reading": "Bright Start 2 Reading",  "vocab": "Bright Start 2 Vocabulary"},
    3:  {"main": "Bright Start 3",  "workbook": "Bright Start 3 Workbook", "reading": "Bright Start 3 Reading",  "vocab": "Bright Start 3 Vocabulary"},
    4:  {"main": "Bright Start 4",  "workbook": "Bright Start 4 Workbook", "reading": "Bright Start 4 Reading",  "vocab": "Bright Start 4 Vocabulary"},
    5:  {"main": "Next Level 5",    "workbook": "Next Level 5 Workbook",   "reading": "Next Level 5 Reading",    "vocab": "Next Level 5 Vocabulary"},
    6:  {"main": "Next Level 6",    "workbook": "Next Level 6 Workbook",   "reading": "Next Level 6 Reading",    "vocab": "Next Level 6 Vocabulary"},
    7:  {"main": "Next Level 7",    "workbook": "Next Level 7 Workbook",   "reading": "Next Level 7 Reading",    "vocab": "Next Level 7 Vocabulary"},
    8:  {"main": "Next Level 8",    "workbook": "Next Level 8 Workbook",   "reading": "Next Level 8 Reading",    "vocab": "Next Level 8 Vocabulary"},
    9:  {"main": "English Core 9",  "workbook": "English Core 9 Workbook", "reading": "English Core 9 Reading",  "vocab": "English Core 9 Vocabulary"},
    10: {"main": "English Core 10", "workbook": "English Core 10 Workbook","reading": "English Core 10 Reading", "vocab": "English Core 10 Vocabulary"},
    11: {"main": "English Core 11", "workbook": "English Core 11 Workbook","reading": "English Core 11 Reading", "vocab": "English Core 11 Vocabulary"},
    12: {"main": "English Core 12", "workbook": "English Core 12 Workbook","reading": "English Core 12 Reading", "vocab": "English Core 12 Vocabulary"},
}

GRADE_COLORS: dict[int, tuple[str, str]] = {
    0: ("#EC4899", "#FDF2F8"), 1: ("#0EA5E9", "#F0F9FF"), 2: ("#22C55E", "#F0FDF4"),
    3: ("#8B5CF6", "#F5F3FF"), 4: ("#F97316", "#FFF7ED"), 5: ("#06B6D4", "#ECFEFF"),
    6: ("#8B5CF6", "#F5F3FF"), 7: ("#EC4899", "#FDF2F8"), 8: ("#14B8A6", "#F0FDFA"),
    9: ("#F43F5E", "#FFF1F2"), 10: ("#3B82F6", "#EFF6FF"), 11: ("#10B981", "#ECFDF5"),
    12: ("#F59E0B", "#FFFBEB"),
}

_GRADE_LABELS: dict[int, str] = {
    0: "Preschool", 1: "Grade 1", 2: "Grade 2", 3: "Grade 3", 4: "Grade 4",
    5: "Grade 5", 6: "Grade 6", 7: "Grade 7", 8: "Grade 8",
    9: "Grade 9", 10: "Grade 10", 11: "Grade 11", 12: "Grade 12",
}

_PW = A4[0] - 4 * cm  # Page content width
_PH = A4[1] - 4 * cm  # Page content height


# ═══════════════════════════════════════════════════════════════════════════════
# COLOR & STYLE HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _hex(h: str) -> rl_colors.Color:
    """Hex string -> ReportLab Color."""
    h = h.lstrip("#")
    return rl_colors.Color(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


def _hex_alpha(h: str, alpha: float) -> rl_colors.Color:
    """Hex with alpha."""
    h = h.lstrip("#")
    return rl_colors.Color(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, alpha)


def _lighten(h: str, factor: float = 0.85) -> rl_colors.Color:
    """Lighten a hex color."""
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    r = r + (1 - r) * factor
    g = g + (1 - g) * factor
    b = b + (1 - b) * factor
    return rl_colors.Color(min(r, 1), min(g, 1), min(b, 1))


def _darken(h: str, factor: float = 0.3) -> rl_colors.Color:
    """Darken a hex color."""
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    return rl_colors.Color(r * (1 - factor), g * (1 - factor), b * (1 - factor))


# ═══════════════════════════════════════════════════════════════════════════════
# UNIT GROUPING
# ═══════════════════════════════════════════════════════════════════════════════

def _group_units(curriculum_weeks: list[dict], target: int = 10) -> list[dict]:
    """Group weeks into exactly `target` units (default 10)."""
    if not curriculum_weeks:
        return []
    n = len(curriculum_weeks)
    units: list[dict] = []
    for i in range(target):
        start = i * n // target
        end = (i + 1) * n // target
        uw = curriculum_weeks[start:end]
        if not uw:
            continue
        units.append({
            "num": i + 1,
            "title": uw[0].get("theme", ""),
            "title_tr": uw[0].get("theme_tr", ""),
            "weeks": uw,
        })
    return units


# ═══════════════════════════════════════════════════════════════════════════════
# DATA EXTRACTION HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _collect_vocab(weeks: list[dict]) -> list[str]:
    words: list[str] = []
    for w in weeks:
        for v in w.get("vocab", []):
            if v not in words:
                words.append(v)
    return words


def _collect_structures(weeks: list[dict]) -> list[str]:
    structs: list[str] = []
    for w in weeks:
        s = w.get("structure", "")
        if s and s not in structs:
            structs.append(s)
    return structs


def _collect_skills(weeks: list[dict]) -> dict:
    """Merge skills from all weeks."""
    merged: dict[str, list[str]] = {}
    for w in weeks:
        for k, v in w.get("skills", {}).items():
            if k not in merged:
                merged[k] = []
            if v and v not in merged[k]:
                merged[k].append(v)
    return merged


def _week_range(weeks: list[dict]) -> str:
    nums = [w.get("week", 0) for w in weeks]
    if not nums:
        return ""
    return f"Week {min(nums)}–{max(nums)}" if len(nums) > 1 else f"Week {nums[0]}"


def _is_young(grade: int) -> bool:
    return grade <= 4


def _body_size(grade: int) -> int:
    return 14 if _is_young(grade) else 11


# ═══════════════════════════════════════════════════════════════════════════════
# STYLE FACTORY — Uses book_design_system typography
# ═══════════════════════════════════════════════════════════════════════════════

def _make_styles(fn: str, fb: str, grade: int, accent: str) -> dict:
    """Build comprehensive ParagraphStyle dictionary using design system."""
    tier = get_tier_for_grade(grade)
    sc = tier["font_scale"]
    ac = _hex(accent)
    ac_light = _lighten(accent, 0.85)
    ac_dark = _darken(accent, 0.3)
    _bsz = _body_size(grade)  # base body font size for this grade
    navy = _hex(get_color_hex("navy"))
    text_c = _hex("#1e293b")  # Dark slate for readability
    sub_c = _hex("#64748b")

    def _sz(key: str) -> tuple[float, float]:
        b = BASE_TYPOGRAPHY.get(key, {"size": 10, "leading": 14})
        return round(b["size"] * sc, 1), round(b["leading"] * sc, 1)

    sz, ld = _sz("cover_title")
    s: dict[str, ParagraphStyle] = {}

    # Cover
    s["cover_title"] = ParagraphStyle("ct", fontName=fb, fontSize=sz, leading=ld,
                                       alignment=TA_CENTER, textColor=rl_colors.white)
    sz, ld = _sz("cover_subtitle")
    s["cover_sub"] = ParagraphStyle("csub", fontName=fn, fontSize=sz, leading=ld,
                                     alignment=TA_CENTER, textColor=_hex("#93c5fd"))
    sz, ld = _sz("cover_info")
    s["cover_info"] = ParagraphStyle("ci", fontName=fn, fontSize=sz, leading=ld,
                                      alignment=TA_CENTER, textColor=_hex("#CBD5E1"))

    # Unit title
    sz, ld = _sz("unit_title")
    s["unit_title"] = ParagraphStyle("ut", fontName=fb, fontSize=sz, leading=ld,
                                      textColor=rl_colors.white)
    sz, ld = _sz("unit_subtitle")
    s["unit_sub"] = ParagraphStyle("us", fontName=fn, fontSize=sz, leading=ld,
                                    textColor=_hex("#bae6fd"))

    # Section title (colored bar)
    sz, ld = _sz("section_title")
    s["sec_title"] = ParagraphStyle("st", fontName=fb, fontSize=sz, leading=ld,
                                     textColor=rl_colors.white)

    # Heading hierarchy
    sz, ld = _sz("h1")
    s["h1"] = ParagraphStyle("h1", fontName=fb, fontSize=sz, leading=ld,
                              textColor=navy, spaceBefore=12, spaceAfter=6)
    sz, ld = _sz("h2")
    s["h2"] = ParagraphStyle("h2", fontName=fb, fontSize=sz, leading=ld,
                              textColor=ac, spaceBefore=10, spaceAfter=5)
    sz, ld = _sz("h3")
    s["h3"] = ParagraphStyle("h3", fontName=fb, fontSize=sz, leading=ld,
                              textColor=text_c, spaceBefore=8, spaceAfter=4)

    # Body text
    sz, ld = _sz("body")
    s["body"] = ParagraphStyle("body", fontName=fn, fontSize=sz, leading=ld,
                                textColor=text_c, spaceAfter=3)
    s["body_j"] = ParagraphStyle("bj", fontName=fn, fontSize=sz, leading=round(ld * 1.05, 1),
                                  textColor=text_c, alignment=TA_JUSTIFY, spaceAfter=4)
    s["body_c"] = ParagraphStyle("bc", fontName=fn, fontSize=sz, leading=ld,
                                  textColor=text_c, alignment=TA_CENTER, spaceAfter=3)

    # Small/caption
    sz, ld = _sz("body_small")
    s["small"] = ParagraphStyle("sm", fontName=fn, fontSize=sz, leading=ld, textColor=sub_c)
    sz, ld = _sz("caption")
    s["caption"] = ParagraphStyle("cap", fontName=fn, fontSize=sz, leading=ld, textColor=sub_c)

    # Instruction (bold)
    sz, ld = _sz("instruction")
    s["instr"] = ParagraphStyle("ins", fontName=fb, fontSize=sz, leading=ld,
                                 textColor=text_c, spaceBefore=6, spaceAfter=4)

    # Exercise
    sz, ld = _sz("exercise")
    s["ex"] = ParagraphStyle("ex", fontName=fn, fontSize=sz, leading=ld,
                              textColor=text_c, leftIndent=10, spaceAfter=3)

    # Dialogue
    sz, ld = _sz("dialogue_name")
    s["dlg_name"] = ParagraphStyle("dn", fontName=fb, fontSize=sz, leading=ld,
                                    textColor=_hex("#1e40af"))
    sz, ld = _sz("dialogue_line")
    s["dlg_line"] = ParagraphStyle("dl", fontName=fn, fontSize=sz, leading=ld, textColor=text_c)

    # Song
    sz, ld = _sz("song")
    s["song"] = ParagraphStyle("song", fontName=fn, fontSize=sz, leading=ld,
                                textColor=navy, alignment=TA_CENTER)

    # Cell styles
    sz, ld = _sz("cell")
    s["cell"] = ParagraphStyle("cl", fontName=fn, fontSize=sz, leading=ld, textColor=text_c)
    s["cell_w"] = ParagraphStyle("cw", fontName=fn, fontSize=sz, leading=ld, textColor=rl_colors.white)
    s["cell_b"] = ParagraphStyle("cb", fontName=fb, fontSize=sz, leading=ld, textColor=text_c)
    sz, ld = _sz("cell_header")
    s["cell_hdr"] = ParagraphStyle("ch", fontName=fb, fontSize=sz, leading=ld, textColor=rl_colors.white)

    # Tip/box
    sz, ld = _sz("tip_title")
    s["tip_t"] = ParagraphStyle("tt", fontName=fb, fontSize=sz, leading=ld, textColor=rl_colors.white)
    sz, ld = _sz("tip_body")
    s["tip_b"] = ParagraphStyle("tb", fontName=fn, fontSize=sz, leading=ld, textColor=text_c)

    # TOC
    sz, ld = _sz("toc")
    s["toc"] = ParagraphStyle("toc", fontName=fn, fontSize=sz, leading=ld,
                               textColor=text_c, spaceAfter=4)
    s["toc_b"] = ParagraphStyle("tocb", fontName=fb, fontSize=sz, leading=ld,
                                 textColor=navy, spaceAfter=4)

    # Page number / footer
    sz, ld = _sz("page_number")
    s["page_num"] = ParagraphStyle("pn", fontName=fn, fontSize=sz, leading=ld,
                                    textColor=sub_c, alignment=TA_CENTER)

    # Fact box
    s["fact_t"] = ParagraphStyle("ftt", fontName=fb, fontSize=round(9.5 * sc, 1),
                                  leading=round(13 * sc, 1), textColor=_hex("#92400e"))
    s["fact_b"] = ParagraphStyle("ftb", fontName=fn, fontSize=round(9 * sc, 1),
                                  leading=round(12 * sc, 1), textColor=_hex("#78350f"))

    return s


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT BUILDER WITH HEADER/FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

class _BookTemplate:
    """Custom document template with professional headers/footers."""

    def __init__(self, buf: io.BytesIO, grade: int, book_title: str,
                 fn: str, fb: str, accent: str):
        self.grade = grade
        self.book_title = book_title
        self.fn = fn
        self.fb = fb
        self.accent = accent
        self.tier = get_tier_for_grade(grade)
        self.sc = self.tier["font_scale"]
        self._current_unit = ""

        ml = PAGE_LAYOUT["margin_left"] * mm
        mr = PAGE_LAYOUT["margin_right"] * mm
        mt = PAGE_LAYOUT["margin_top"] * mm
        mb = PAGE_LAYOUT["margin_bottom"] * mm

        frame = Frame(ml, mb, A4[0] - ml - mr, A4[1] - mt - mb,
                      id="main", topPadding=6, bottomPadding=6)

        self.doc = BaseDocTemplate(
            buf, pagesize=A4,
            leftMargin=ml, rightMargin=mr,
            topMargin=mt, bottomMargin=mb,
        )

        # Two templates: cover (no header/footer) and content (with)
        cover_tmpl = PageTemplate(id="cover", frames=[frame],
                                   onPage=self._on_cover_page)
        content_tmpl = PageTemplate(id="content", frames=[frame],
                                     onPage=self._on_content_page)

        self.doc.addPageTemplates([cover_tmpl, content_tmpl])

    def set_current_unit(self, title: str):
        self._current_unit = title

    def _on_cover_page(self, canvas, doc):
        """Cover pages: no header/footer."""
        pass

    def _on_content_page(self, canvas, doc):
        """Content pages: professional header line + footer."""
        canvas.saveState()
        page_w, page_h = A4
        pg = doc.page
        sc = self.sc
        font_sz = round(7.5 * sc, 1)

        ml = PAGE_LAYOUT["margin_left"] * mm
        mr = PAGE_LAYOUT["margin_right"] * mm
        x_left = ml
        x_right = page_w - mr

        # ── Header line ──
        y_hdr = page_h - PAGE_LAYOUT["margin_top"] * mm + 4 * mm
        canvas.setStrokeColor(_hex(get_color_hex("border")))
        canvas.setLineWidth(0.4)
        canvas.line(x_left, y_hdr, x_right, y_hdr)

        canvas.setFont(self.fn, font_sz)
        canvas.setFillColor(_hex("#64748b"))

        if pg % 2 == 0:  # even (left page)
            canvas.drawString(x_left, y_hdr + 3 * mm, str(pg))
            if self._current_unit:
                canvas.drawRightString(x_right, y_hdr + 3 * mm, self._current_unit[:50])
        else:  # odd (right page)
            canvas.drawString(x_left, y_hdr + 3 * mm, self.book_title)
            canvas.drawRightString(x_right, y_hdr + 3 * mm, str(pg))

        # ── Footer ──
        y_ftr = PAGE_LAYOUT["margin_bottom"] * mm - 4 * mm
        canvas.setFont(self.fn, font_sz)
        canvas.setFillColor(_hex("#94A3B8"))
        footer = f"{self.book_title}  ·  Page {pg}"
        canvas.drawCentredString(page_w / 2, y_ftr, footer)

        # ── Accent line at bottom ──
        canvas.setStrokeColor(_hex(self.accent))
        canvas.setLineWidth(0.6)
        canvas.line(x_left, y_ftr + 3 * mm, x_right, y_ftr + 3 * mm)

        canvas.restoreState()

    def build(self, elements: list):
        self.doc.build(elements)


# ═══════════════════════════════════════════════════════════════════════════════
# PREMIUM COMPONENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def _section_header(title: str, section_key: str, pw: float, fb: str, grade: int) -> Table:
    """Professional colored section header bar with rounded top corners."""
    dark_hex, _ = get_section_colors(section_key)
    bg = _hex(dark_hex)
    tier = get_tier_for_grade(grade)
    sc = tier["font_scale"]
    sz = round(13 * sc, 1)

    hdr_style = ParagraphStyle("shdr", fontName=fb, fontSize=sz,
                                leading=round(17 * sc, 1), textColor=rl_colors.white)
    h = Table([[Paragraph(f"<b>{title}</b>", hdr_style)]], colWidths=[pw], rowHeights=[30])
    h.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS", [8, 8, 0, 0]),
    ]))
    return h


def _content_box(text: str, section_key: str, pw: float, fn: str, grade: int,
                 style_override: ParagraphStyle | None = None) -> Table:
    """Content box with light background matching section color."""
    _, light_hex = get_section_colors(section_key)
    dark_hex, _ = get_section_colors(section_key)
    bg = _hex(light_hex)
    border = _hex(dark_hex)

    tier = get_tier_for_grade(grade)
    sc = tier["font_scale"]
    sz = round(10 * sc, 1)

    body_style = style_override or ParagraphStyle(
        "cbox", fontName=fn, fontSize=sz, leading=round(14 * sc, 1),
        textColor=_hex("#1e293b"))

    b = Table([[Paragraph(text, body_style)]], colWidths=[pw])
    b.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.5, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [0, 0, 8, 8]),
    ]))
    return b


def _tip_box(title: str, text: str, box_type: str, pw: float,
             fn: str, fb: str, grade: int) -> Table:
    """Styled tip/warning/info/fact/story box."""
    spec = BOX_STYLES.get(box_type, BOX_STYLES["info"])
    bg = _hex(get_color_hex(spec["bg"])) if spec["bg"] else _hex("#f8fafc")
    border = _hex(get_color_hex(spec["border"])) if spec["border"] else _hex("#e2e8f0")
    radius = spec["corner_radius"]
    pad = spec["padding"]

    icon = spec.get("icon", "")
    header_text = f"{icon}  {title}" if icon else title

    tier = get_tier_for_grade(grade)
    sc = tier["font_scale"]

    hdr_style = ParagraphStyle("tbh", fontName=fb, fontSize=round(9.5 * sc, 1),
                                leading=round(13 * sc, 1), textColor=rl_colors.white)
    body_style = ParagraphStyle("tbb", fontName=fn, fontSize=round(9 * sc, 1),
                                 leading=round(12.5 * sc, 1), textColor=_hex("#1e293b"))

    rows = [
        [Paragraph(f"<b>{header_text}</b>", hdr_style)],
        [Paragraph(text, body_style)],
    ]
    t = Table(rows, colWidths=[pw])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), border),
        ("BACKGROUND", (0, 1), (-1, 1), bg),
        ("BOX", (0, 0), (-1, -1), spec["border_width"], border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad["left"]),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad["right"]),
        ("TOPPADDING", (0, 0), (-1, -1), pad["top"]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad["bottom"]),
        ("ROUNDEDCORNERS", [radius, radius, radius, radius]),
    ]))
    return t


def _data_table(data: list[list[str]], col_widths: list[float],
                fn: str, fb: str, accent: str, grade: int,
                header_bg: str | None = None) -> Table:
    """Professional data table with zebra striping."""
    ac = _hex(header_bg or accent)
    tier = get_tier_for_grade(grade)
    sc = tier["font_scale"]
    bs = round(9 * sc, 1)
    ld = round(12 * sc, 1)

    styled_rows = []
    for r, row in enumerate(data):
        styled_row = []
        for cell in row:
            if r == 0:
                st = ParagraphStyle("th", fontName=fb, fontSize=bs, leading=ld,
                                    textColor=rl_colors.white)
            else:
                st = ParagraphStyle("td", fontName=fn, fontSize=bs, leading=ld,
                                    textColor=_hex("#1e293b"))
            styled_row.append(Paragraph(str(cell), st))
        styled_rows.append(styled_row)

    t = Table(styled_rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ac),
        ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, _hex("#e2e8f0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl_colors.white, _hex("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    return t


def _numbered_list(items: list[str], style: ParagraphStyle, start: int = 1) -> list:
    """Generate numbered list paragraphs."""
    els = []
    for i, item in enumerate(items, start):
        els.append(Paragraph(f"<b>{i}.</b> {item}", style))
    return els


def _bullet_list(items: list[str], style: ParagraphStyle, bullet: str = "\u2022") -> list:
    """Generate bullet list paragraphs."""
    return [Paragraph(f"{bullet} {item}", style) for item in items]


def _writing_lines(count: int, pw: float) -> Table:
    """Dotted writing lines for student responses."""
    rows = [[""] for _ in range(count)]
    t = Table(rows, colWidths=[pw], rowHeights=[24] * count)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, i), (-1, i), 0.3, _hex("#cbd5e1")) for i in range(count)
    ] + [
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def _divider(pw: float, color: str = "#e2e8f0") -> Table:
    """Thin horizontal divider line."""
    t = Table([[""]], colWidths=[pw], rowHeights=[1])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, _hex(color))]))
    return t


def _gold_accent_bar(pw: float, height: int = 4) -> Table:
    """Gold accent bar (brand element)."""
    bar = Table([[""]], colWidths=[pw], rowHeights=[height])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), _hex(get_color_hex("brand_gold"))),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    return bar


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-CONTENT GENERATORS (fallback when AI content missing)
# ═══════════════════════════════════════════════════════════════════════════════

def _auto_story(theme: str, vocab: list[str], grade: int) -> str:
    rng = random.Random(hash(theme) & 0xFFFFFFFF)
    if not vocab:
        return f"This unit is about {theme}. It is very interesting. Let's learn more about it together."
    picked = vocab[:min(len(vocab), 10 if grade >= 5 else 6)]
    lines = [f"This is a story about {theme}."]
    templates = [
        "I really like {w}.", "The {w} is wonderful.", "Do you know about {w}?",
        "We can learn about {w} in school.", "Look at the {w}!", "{w} is very important.",
        "Can you find the {w}?", "My friend also likes {w}.",
        "Everyone should know about {w}.", "Let's talk about {w} today.",
    ]
    rng.shuffle(templates)
    for i, w in enumerate(picked):
        lines.append(templates[i % len(templates)].format(w=w))
    lines.append(f"Learning about {theme} is always fun and exciting!")
    return " ".join(lines)


def _auto_dialogue(theme: str, vocab: list[str]) -> list[dict]:
    vw = vocab[:4] if vocab else ["hello"]
    return [
        {"speaker": 0, "text": f"Hi! Do you like {theme}?"},
        {"speaker": 1, "text": f"Yes, I do! I know about {vw[0]}."},
        {"speaker": 0, "text": f"That's great. What about {vw[1] if len(vw) > 1 else theme}?"},
        {"speaker": 1, "text": f"Sure! I also like {vw[2] if len(vw) > 2 else vw[0]}."},
        {"speaker": 0, "text": f"Wonderful. Let's learn more about {theme} together."},
        {"speaker": 1, "text": "Good idea! It will be fun."},
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE (PREMIUM)
# ═══════════════════════════════════════════════════════════════════════════════

def _premium_cover(elements: list, book_title: str, grade: int, cover_type: str,
                   styles: dict, accent: str, fn: str, fb: str,
                   units: list[dict] | None = None):
    """Professional front cover with gradient band, CEFR info, and unit preview."""
    ac = _hex(accent)
    tier = get_tier_for_grade(grade)
    cfg = get_grade_config(grade)
    pw = _PW

    # Switch to cover template
    elements.append(NextPageTemplate("cover"))

    # Top gold accent bar
    elements.append(_gold_accent_bar(pw, 5))
    elements.append(Spacer(1, 0.3 * cm))

    # Series identity
    elements.append(Paragraph("SmartCampus English Series", ParagraphStyle(
        "series", fontName=fn, fontSize=9, leading=12, alignment=TA_CENTER,
        textColor=_hex("#64748b"))))
    elements.append(Spacer(1, 0.5 * cm))

    # Main color band
    band_data = [
        [Spacer(1, 1.2 * cm)],
        [Paragraph(book_title, ParagraphStyle(
            "bt", fontName=fb, fontSize=round(32 * tier["font_scale"], 0),
            leading=round(40 * tier["font_scale"], 0),
            alignment=TA_CENTER, textColor=rl_colors.white))],
        [Spacer(1, 0.4 * cm)],
        [Paragraph(cover_type, ParagraphStyle(
            "ct2", fontName=fn, fontSize=round(14 * tier["font_scale"], 0),
            leading=round(18 * tier["font_scale"], 0),
            alignment=TA_CENTER, textColor=_hex("#bae6fd")))],
        [Spacer(1, 0.4 * cm)],
        [Paragraph(f'{_GRADE_LABELS.get(grade, f"Grade {grade}")}  ·  {cfg["cefr"]}', ParagraphStyle(
            "cefr", fontName=fn, fontSize=round(12 * tier["font_scale"], 0),
            leading=round(16 * tier["font_scale"], 0),
            alignment=TA_CENTER, textColor=_hex("#93c5fd")))],
        [Spacer(1, 0.3 * cm)],
        [Paragraph(f'<i>{cfg["desc"]}</i>', ParagraphStyle(
            "desc", fontName=fn, fontSize=round(9.5 * tier["font_scale"], 0),
            leading=round(13 * tier["font_scale"], 0),
            alignment=TA_CENTER, textColor=_hex("#cbd5e1")))],
        [Spacer(1, 1.2 * cm)],
    ]
    bt = Table(band_data, colWidths=[pw])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ac),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
    ]))
    elements.append(bt)
    elements.append(Spacer(1, 0.5 * cm))

    # Unit preview grid (2 rows × 5 cols)
    if units:
        grid_data: list[list] = []
        row: list = []
        col_w = pw / 5
        for u in units[:10]:
            u_color = _hex(get_unit_color(u["num"]))
            cell_content = Paragraph(
                f'<b>Unit {u["num"]}</b><br/><font size="7">{u["title"][:18]}</font>',
                ParagraphStyle("ug", fontName=fn, fontSize=8, leading=11,
                               alignment=TA_CENTER, textColor=rl_colors.white))
            row.append(cell_content)
            if len(row) == 5:
                grid_data.append(row)
                row = []
        if row:
            while len(row) < 5:
                row.append("")
            grid_data.append(row)

        if grid_data:
            gt = Table(grid_data, colWidths=[col_w] * 5, rowHeights=[40] * len(grid_data))
            style_cmds: list = [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 1, rl_colors.white),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ]
            # Color each cell
            for ri, r_data in enumerate(grid_data):
                for ci in range(5):
                    u_idx = ri * 5 + ci
                    if u_idx < len(units):
                        u_clr = _hex(get_unit_color(units[u_idx]["num"]))
                        style_cmds.append(("BACKGROUND", (ci, ri), (ci, ri), u_clr))
                    else:
                        style_cmds.append(("BACKGROUND", (ci, ri), (ci, ri), _hex("#f1f5f9")))
            gt.setStyle(TableStyle(style_cmds))
            elements.append(gt)
            elements.append(Spacer(1, 0.5 * cm))

    # Bottom section
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph("SmartCampusAI", ParagraphStyle(
        "brand", fontName=fb, fontSize=18, alignment=TA_CENTER, textColor=ac)))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph("2025 – 2026", ParagraphStyle(
        "year", fontName=fn, fontSize=12, alignment=TA_CENTER, textColor=_hex("#64748b"))))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(_gold_accent_bar(pw, 5))
    elements.append(PageBreak())

    # Switch to content template
    elements.append(NextPageTemplate("content"))


def _premium_toc(elements: list, units: list[dict], styles: dict, grade: int,
                 fn: str, fb: str, accent: str):
    """Professional table of contents with unit colors."""
    pw = _PW
    young = _is_young(grade)

    elements.append(Spacer(1, 0.5 * cm))
    elements.append(_gold_accent_bar(pw, 3))
    elements.append(Spacer(1, 0.4 * cm))

    toc_title = "TABLE OF CONTENTS"
    elements.append(Paragraph(toc_title, ParagraphStyle(
        "toch", fontName=fb, fontSize=18, leading=24,
        alignment=TA_CENTER, textColor=_hex(accent))))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(_gold_accent_bar(pw, 3))
    elements.append(Spacer(1, 0.8 * cm))

    for u in units:
        u_color = _hex(get_unit_color(u["num"]))
        prefix = "\u2B50 " if young else ""

        # Unit number badge + title
        badge = Table(
            [[Paragraph(f'<b>{u["num"]}</b>', ParagraphStyle(
                "badge", fontName=fb, fontSize=11, leading=14,
                alignment=TA_CENTER, textColor=rl_colors.white))]],
            colWidths=[30], rowHeights=[24])
        badge.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), u_color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ]))

        title_text = f'{prefix}<b>Unit {u["num"]}:</b> {u["title"]}'
        if u.get("title_tr"):
            title_text += f'  <i>({u["title_tr"]})</i>'

        row = Table(
            [[badge, Paragraph(title_text, styles["toc"]),
              Paragraph(_week_range(u["weeks"]), styles["caption"])]],
            colWidths=[40, pw - 120, 80])
        row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(row)

    elements.append(PageBreak())


def _premium_unit_opener(elements: list, unit: dict, styles: dict, grade: int,
                         fn: str, fb: str, accent: str, vocab: list[str],
                         skills: dict) -> None:
    """Full-page premium unit opener with banner + objectives."""
    pw = _PW
    u_color_hex = get_unit_color(unit["num"])
    u_color = _hex(u_color_hex)
    gold = _hex(get_color_hex("brand_gold"))
    young = _is_young(grade)

    # Gold top bar
    bar_top = Table([[""]], colWidths=[pw], rowHeights=[5])
    bar_top.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), gold),
        ("ROUNDEDCORNERS", [6, 6, 0, 0]),
    ]))
    elements.append(bar_top)

    # Main banner
    pfx = "\U0001F31F " if young else ""
    banner_rows = [
        [Spacer(1, 1.5 * cm)],
        [Paragraph(f"UNIT {unit['num']}", ParagraphStyle(
            "unum", fontName=fb, fontSize=16, leading=20,
            textColor=_hex("#93c5fd")))],
        [Paragraph(f"{pfx}{unit['title'].upper()}", ParagraphStyle(
            "utitle", fontName=fb, fontSize=28, leading=34,
            textColor=rl_colors.white))],
        [Spacer(1, 6)],
    ]
    if unit.get("title_tr"):
        banner_rows.append([Paragraph(unit["title_tr"], ParagraphStyle(
            "utr", fontName=fn, fontSize=13, leading=17,
            textColor=_hex("#bae6fd")))])
    banner_rows.append([Spacer(1, 6)])
    banner_rows.append([Paragraph(_week_range(unit["weeks"]), ParagraphStyle(
        "uweek", fontName=fn, fontSize=11, leading=14,
        textColor=_hex("#93c5fd")))])
    banner_rows.append([Spacer(1, 1.5 * cm)])

    bt = Table(banner_rows, colWidths=[pw])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), u_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(bt)

    # Gold bottom bar
    bar_bot = Table([[""]], colWidths=[pw], rowHeights=[5])
    bar_bot.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), gold),
        ("ROUNDEDCORNERS", [0, 0, 6, 6]),
    ]))
    elements.append(bar_bot)
    elements.append(Spacer(1, 0.8 * cm))

    # Learning Objectives box
    obj_items = []
    for sk, descs in skills.items():
        label = {"listening": "Listening", "speaking": "Speaking",
                 "reading": "Reading", "writing": "Writing"}.get(sk, sk.title())
        for d in descs[:2]:
            obj_items.append(f"<b>{label}:</b> {d}")

    if obj_items:
        obj_hdr = Table(
            [[Paragraph("<b>LEARNING OBJECTIVES</b>", ParagraphStyle(
                "objh", fontName=fb, fontSize=round(10 * get_tier_for_grade(grade)["font_scale"], 1),
                leading=14, textColor=rl_colors.white))]],
            colWidths=[pw], rowHeights=[28])
        obj_hdr.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), u_color),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [8, 8, 0, 0]),
        ]))
        elements.append(obj_hdr)

        obj_text = "<br/>".join(f"&bull; {o}" for o in obj_items)
        obj_body = Table(
            [[Paragraph(obj_text, ParagraphStyle(
                "objb", fontName=fn, fontSize=round(9.5 * get_tier_for_grade(grade)["font_scale"], 1),
                leading=14, textColor=_hex("#1e293b")))]],
            colWidths=[pw])
        obj_body.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, _hex("#e2e8f0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [0, 0, 8, 8]),
        ]))
        elements.append(obj_body)
        elements.append(Spacer(1, 0.5 * cm))

    # Key vocabulary preview
    if vocab:
        preview_words = vocab[:12]
        elements.append(Paragraph("<b>KEY VOCABULARY</b>", styles["h3"]))
        word_text = "  ·  ".join(f"<b>{w}</b>" for w in preview_words)
        elements.append(Paragraph(word_text, styles["body_c"]))

    elements.append(PageBreak())


def _back_cover(elements: list, styles: dict, accent: str, grade: int,
                fn: str, fb: str):
    """Professional back cover."""
    pw = _PW
    ac = _hex(accent)
    cfg = get_grade_config(grade)

    elements.append(Spacer(1, 4 * cm))
    elements.append(_gold_accent_bar(pw, 3))
    elements.append(Spacer(1, 2 * cm))

    elements.append(Paragraph("SmartCampusAI", ParagraphStyle(
        "bc1", fontName=fb, fontSize=24, alignment=TA_CENTER, textColor=ac)))
    elements.append(Spacer(1, 0.4 * cm))
    elements.append(Paragraph("English Language Education Series", ParagraphStyle(
        "bc2", fontName=fn, fontSize=12, alignment=TA_CENTER, textColor=_hex("#64748b"))))
    elements.append(Spacer(1, 0.8 * cm))
    elements.append(Paragraph(f'{_GRADE_LABELS.get(grade, "")}  ·  CEFR {cfg["cefr"]}',
                               ParagraphStyle("bc3", fontName=fn, fontSize=11,
                                              alignment=TA_CENTER, textColor=_hex("#94A3B8"))))
    elements.append(Spacer(1, 0.4 * cm))
    elements.append(Paragraph("2025 – 2026", ParagraphStyle(
        "bc4", fontName=fn, fontSize=11, alignment=TA_CENTER, textColor=_hex("#94A3B8"))))
    elements.append(Spacer(1, 2 * cm))
    elements.append(_gold_accent_bar(pw, 3))
    elements.append(Spacer(1, 1.5 * cm))
    elements.append(Paragraph("www.smartcampusai.com", ParagraphStyle(
        "bc5", fontName=fn, fontSize=9, alignment=TA_CENTER, textColor=_hex("#94A3B8"))))


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTION 1: MAIN COURSE BOOK — ~20 pages per unit
# ═══════════════════════════════════════════════════════════════════════════════

def generate_basic_main_course_pdf(grade: int, curriculum_weeks: list[dict]) -> bytes | None:
    """Generate premium Main Course book — ~20 pages per unit, print-ready."""
    if not curriculum_weeks:
        return None
    fn, fb = ensure_turkish_pdf_fonts()
    accent, bg_hex = GRADE_COLORS.get(grade, ("#3B82F6", "#EFF6FF"))
    units = _group_units(curriculum_weeks)
    book_name = BOOK_TITLES.get(grade, BOOK_TITLES[5])["main"]
    styles = _make_styles(fn, fb, grade, accent)
    young = _is_young(grade)
    pw = _PW

    from views.book_content_ai import generate_unit_content, _load_cache, generate_all_units

    # Pre-generate all unit content if not cached (batch mode)
    _pre_gen = generate_all_units(grade, curriculum_weeks)
    # generate_all_units populates cache, so _load_cache will find it below

    buf = io.BytesIO()
    tmpl = _BookTemplate(buf, grade, f"Basic Main Course — {book_name}", fn, fb, accent)

    elements: list = []

    # ── Cover ──
    _premium_cover(elements, f"Basic Main Course — {book_name}", grade,
                   "Main Course Book", styles, accent, fn, fb, units)

    # ── TOC ──
    _premium_toc(elements, units, styles, grade, fn, fb, accent)

    for unit in units:
        vocab = _collect_vocab(unit["weeks"])
        structs = _collect_structures(unit["weeks"])
        skills = _collect_skills(unit["weeks"])

        tmpl.set_current_unit(f"Unit {unit['num']}: {unit['title']}")

        # AI content
        ai = _load_cache(grade, unit["num"])
        if not ai:
            ai = generate_unit_content(
                grade, unit["num"], unit["title"], vocab,
                unit["weeks"][0].get("structure", ""),
                unit["weeks"][0].get("skills", {}),
                unit.get("title_tr", ""),
            )

        # ═══ PAGE 1: Unit Opener (full page) ═══
        _premium_unit_opener(elements, unit, styles, grade, fn, fb, accent, vocab, skills)

        # ═══ PAGE 2-3: Theme Introduction + Warm-Up ═══
        sec = KeepTogether([
            _section_header("THEME INTRODUCTION", "reading", pw, fb, grade),
            _content_box(
                ai.get("theme_intro", f"In this unit, we will explore <b>{unit['title']}</b>. "
                       f"You will learn new vocabulary, practice reading and writing, "
                       f"and develop your communication skills.") if ai else
                f"In this unit, we will explore <b>{unit['title']}</b>.",
                "reading", pw, fn, grade),
            Spacer(1, 0.5 * cm),
        ])
        elements.append(sec)

        # Warm-up discussion
        elements.append(Paragraph("<b>WARM-UP DISCUSSION</b>", styles["h2"]))
        warmup_qs = [
            f"What do you already know about {unit['title'].lower()}?",
            f"Have you ever experienced something related to {unit['title'].lower()}?",
            "Look at the pictures on this page. What do you think this unit is about?",
        ]
        elements.extend(_bullet_list(warmup_qs, styles["body"]))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(_writing_lines(3, pw))
        elements.append(Spacer(1, 0.5 * cm))

        # Pre-teaching vocabulary preview
        elements.append(Paragraph("<b>VOCABULARY PREVIEW</b>", styles["h2"]))
        elements.append(Paragraph(
            "Before reading, look at these key words. Try to guess their meanings.",
            styles["body"]))
        elements.append(Spacer(1, 0.3 * cm))

        preview_words = vocab[:8]
        rows_p = [["Word", "My Guess", "Actual Meaning"]]
        for w in preview_words:
            rows_p.append([w, "", ""])
        elements.append(_data_table(rows_p, [pw * 0.25, pw * 0.35, pw * 0.35],
                                     fn, fb, accent, grade))
        elements.append(PageBreak())

        # ═══ PAGE 4-5: Key Vocabulary ═══
        elements.append(_section_header("VOCABULARY WORKSHOP", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        vocab_defs = ai.get("vocabulary_enrichment", {}).get("definitions", []) if ai else []
        if vocab_defs:
            # Split vocabulary into two pages if many words
            half = max(8, len(vocab_defs) // 2)
            for batch_idx, batch_start in enumerate([0, half]):
                batch = vocab_defs[batch_start:batch_start + half]
                if not batch:
                    break
                if batch_idx > 0:
                    elements.append(CondPageBreak(6 * cm))
                    elements.append(Paragraph(f"<b>VOCABULARY (continued)</b>", styles["h2"]))
                    elements.append(Spacer(1, 0.2 * cm))

                rows_v = [["#", "Word", "Definition", "Example Sentence"]]
                for idx, vd in enumerate(batch, batch_start + 1):
                    rows_v.append([
                        str(idx),
                        vd.get("word", ""),
                        vd.get("definition", ""),
                        vd.get("example", ""),
                    ])
                elements.append(_data_table(
                    rows_v,
                    [pw * 0.06, pw * 0.17, pw * 0.35, pw * 0.38],
                    fn, fb, accent, grade))
                elements.append(Spacer(1, 0.3 * cm))

            # Turkish hints box
            hints = [vd for vd in vocab_defs if vd.get("turkish_hint")]
            if hints:
                hint_text = "  |  ".join(
                    f'<b>{h.get("word", "")}</b>: {h.get("turkish_hint", "")}' for h in hints[:12])
                elements.append(_tip_box("Türkçe İpuçları / Turkish Hints", hint_text,
                                         "info", pw, fn, fb, grade))
                elements.append(Spacer(1, 0.3 * cm))
        else:
            rows_v = [["#", "Word", "Pronunciation", "Turkish", "My Sentence"]]
            for idx, w in enumerate(vocab, 1):
                rows_v.append([str(idx), w, f"/{w.lower()}/", "___________", ""])
            elements.append(_data_table(
                rows_v, [pw * 0.06, pw * 0.2, pw * 0.2, pw * 0.2, pw * 0.3],
                fn, fb, accent, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Word Families
        word_families = ai.get("vocabulary_enrichment", {}).get("word_families", []) if ai else []
        if word_families:
            elements.append(KeepTogether([
                Paragraph("<b>WORD FAMILIES</b>", styles["h2"]),
                Spacer(1, 0.2 * cm),
                _data_table(
                    [["Base Word", "Noun", "Verb", "Adjective"]] +
                    [[wf.get("base", ""), wf.get("noun", "—"), wf.get("verb", "—"),
                      wf.get("adjective", "—")] for wf in word_families],
                    [pw * 0.22, pw * 0.24, pw * 0.24, pw * 0.24],
                    fn, fb, get_color_hex("blue"), grade,
                    header_bg=get_color_hex("blue_dark")),
                Spacer(1, 0.5 * cm),
            ]))

        # Vocabulary exercises
        elements.append(KeepTogether([
            Paragraph("<b>VOCABULARY PRACTICE</b>", styles["h2"]),
            Paragraph("<b>A. Match the words with their definitions.</b>", styles["instr"]),
        ]))
        match_data = ai.get("exercises", {}).get("matching", []) if ai else []
        if match_data:
            rows_m = [["Column A", "Column B"]]
            for md in match_data[:8]:
                rows_m.append([md.get("left", ""), md.get("right", "")])
            elements.append(_data_table(rows_m, [pw * 0.45, pw * 0.45], fn, fb,
                                         get_color_hex("blue"), grade))
        else:
            rows_m = [["Column A", "Column B"]]
            rng = random.Random(hash(unit["title"]) & 0xFFFFFFFF)
            shuffled = vocab[:6].copy()
            rng.shuffle(shuffled)
            for i, w in enumerate(vocab[:6]):
                rows_m.append([w, shuffled[i] if i < len(shuffled) else ""])
            elements.append(_data_table(rows_m, [pw * 0.45, pw * 0.45], fn, fb,
                                         get_color_hex("blue"), grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(KeepTogether([
            Paragraph("<b>B. Fill in the blanks with the correct word.</b>", styles["instr"]),
            Spacer(1, 0.2 * cm),
        ]))
        fill_data = ai.get("exercises", {}).get("fill_blanks", []) if ai else []
        if fill_data:
            for i, fb_item in enumerate(fill_data[:6], 1):
                sent = fb_item.get("sentence", "")
                opts = fb_item.get("options", [])
                opts_str = f" ({' / '.join(opts)})" if opts else ""
                elements.append(Paragraph(f"<b>{i}.</b> {sent}{opts_str}", styles["ex"]))
        else:
            for i, w in enumerate(vocab[:6], 1):
                elements.append(Paragraph(f"<b>{i}.</b> I really like __________ very much. ({w})", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 6-7: Grammar Focus ═══
        elements.append(_section_header("GRAMMAR FOCUS", "grammar", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        gf = ai.get("grammar_focus", {}) if ai else {}
        if gf:
            # Grammar rule box
            rule_text = gf.get("rule", "")
            if rule_text:
                elements.append(_tip_box("Grammar Rule", rule_text, "rule", pw, fn, fb, grade))
                elements.append(Spacer(1, 0.4 * cm))

            # Examples
            examples = gf.get("examples", [])
            if examples:
                elements.append(Paragraph("<b>EXAMPLES</b>", styles["h2"]))
                for idx, ex in enumerate(examples, 1):
                    elements.append(Paragraph(
                        f'<b>{idx}.</b> <i>{ex}</i>', styles["body"]))
                elements.append(Spacer(1, 0.4 * cm))

            # Tip
            tip = gf.get("tip", "")
            if tip:
                elements.append(_tip_box("Remember!", tip, "tip", pw, fn, fb, grade))
                elements.append(Spacer(1, 0.4 * cm))
        elif structs:
            elements.append(Paragraph("<b>KEY STRUCTURES</b>", styles["h2"]))
            for s_item in structs:
                elements.append(Paragraph(f"\u2022 <i>{s_item}</i>", styles["body"]))
            elements.append(Spacer(1, 0.4 * cm))

        # Grammar practice
        elements.append(Paragraph("<b>GRAMMAR PRACTICE</b>", styles["h2"]))

        elements.append(KeepTogether([
            Paragraph("<b>A. Complete the sentences using the grammar rule above.</b>", styles["instr"]),
            Spacer(1, 0.2 * cm),
        ]))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(KeepTogether([
            Paragraph("<b>B. Correct the mistakes in these sentences.</b>", styles["instr"]),
            Spacer(1, 0.2 * cm),
        ]))
        for i in range(1, 5):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(KeepTogether([
            Paragraph("<b>C. Write your own sentences using the structure.</b>", styles["instr"]),
            Spacer(1, 0.2 * cm),
            _writing_lines(4, pw),
            Spacer(1, 0.3 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 8-9: Story Time ═══
        elements.append(_section_header("STORY TIME", "story", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        story = ai.get("story", {}) if ai else {}
        if story:
            elements.append(Paragraph(f'<b>{story.get("title", "A Story")}</b>', styles["h2"]))
            elements.append(Spacer(1, 0.2 * cm))

            # Story text in a styled box
            story_text = story.get("text", "")
            elements.append(_content_box(story_text, "story", pw, fn, grade))
            elements.append(Spacer(1, 0.3 * cm))

            moral = story.get("moral", "")
            if moral:
                elements.append(_tip_box("Moral of the Story", moral, "fact", pw, fn, fb, grade))
                elements.append(Spacer(1, 0.3 * cm))
        else:
            elements.append(Paragraph("<b>Story</b>", styles["h2"]))
            elements.append(_content_box(
                _auto_story(unit["title"], vocab, grade), "story", pw, fn, grade))
            elements.append(Spacer(1, 0.3 * cm))

        # Story comprehension
        elements.append(Paragraph("<b>READING COMPREHENSION</b>", styles["h2"]))
        elements.append(Paragraph(
            "<b>A. Answer the questions about the story.</b>", styles["instr"]))
        story_qs = [
            "What is the main idea of the story?",
            "Who are the characters in the story?",
            "What happened at the beginning?",
            "What happened at the end?",
            f"What new words did you learn from this story?",
        ]
        for i, q in enumerate(story_qs, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {q}", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        tf_items = [
            f"The story is about {unit['title'].lower()}.  ( T / F )",
            "There are no characters in the story.  ( T / F )",
            "The story teaches us something new.  ( T / F )",
        ]
        elements.append(KeepTogether([
            Paragraph("<b>B. True or False? Write T or F.</b>", styles["instr"]),
            Spacer(1, 0.2 * cm),
            *_numbered_list(tf_items, styles["ex"]),
            Spacer(1, 0.4 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 10-11: Reading Passage ═══
        rp = ai.get("reading_passage", {}) if ai else {}
        elements.append(_section_header("READING COMPREHENSION", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        if rp:
            elements.append(Paragraph(f'<b>{rp.get("title", "Reading Passage")}</b>', styles["h2"]))
            elements.append(_content_box(rp.get("text", ""), "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.4 * cm))

            questions = rp.get("questions", [])
            if questions:
                elements.append(Paragraph("<b>COMPREHENSION QUESTIONS</b>", styles["h2"]))
                for qi, q in enumerate(questions, 1):
                    elements.append(Paragraph(f"<b>{qi}.</b> {q}", styles["ex"]))
                    elements.append(Paragraph("_______________________________________________", styles["ex"]))
                elements.append(Spacer(1, 0.4 * cm))
        else:
            elements.append(Paragraph("<b>Reading Passage</b>", styles["h2"]))
            rp_text = (f"{unit['title']} is an important topic in our lives. "
                       f"Many people around the world learn about {unit['title'].lower()} every day. "
                       f"In this passage, we will explore key ideas about {unit['title'].lower()} "
                       f"and why it matters.")
            if vocab:
                rp_text += f" Key words include {', '.join(vocab[:5])}."
            elements.append(_content_box(rp_text, "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.3 * cm))

        # Critical thinking
        elements.append(KeepTogether([
            Paragraph("<b>CRITICAL THINKING</b>", styles["h2"]),
            Paragraph("Think about the reading passage and answer these questions.", styles["body"]),
            Spacer(1, 0.2 * cm),
            Paragraph(f"<b>1.</b> What is the author's main message?", styles["ex"]),
            _writing_lines(2, pw),
            Spacer(1, 0.2 * cm),
            Paragraph(f"<b>2.</b> Do you agree with the ideas in the text? Why or why not?", styles["ex"]),
            _writing_lines(2, pw),
            Spacer(1, 0.2 * cm),
            Paragraph(f"<b>3.</b> How does this topic relate to your own life?", styles["ex"]),
            _writing_lines(2, pw),
            Spacer(1, 0.3 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 12-13: Dialogue + Listening & Speaking ═══
        elements.append(_section_header("LISTENING & SPEAKING", "listening", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Dialogue
        dlg = ai.get("dialogue", {}) if ai else {}
        elements.append(Paragraph("<b>DIALOGUE</b>", styles["h2"]))
        if dlg:
            elements.append(Paragraph(f'<i>{dlg.get("title", "")}</i>', styles["body"]))
            elements.append(Spacer(1, 0.2 * cm))
            speakers = dlg.get("speakers", ["A", "B"])
            for line in dlg.get("lines", []):
                sp_idx = line.get("speaker", 0)
                sp = speakers[sp_idx] if sp_idx < len(speakers) else "?"
                color = "#1e40af" if sp_idx == 0 else "#059669"
                elements.append(Paragraph(
                    f'<font color="{color}"><b>{sp}:</b></font> {line.get("text", "")}',
                    styles["body"]))
        else:
            auto_dlg = _auto_dialogue(unit["title"], vocab)
            speakers = ["Speaker A", "Speaker B"]
            for line in auto_dlg:
                sp = speakers[line["speaker"]]
                elements.append(Paragraph(f"<b>{sp}:</b> {line['text']}", styles["body"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Practice dialogue
        elements.append(KeepTogether([
            Paragraph("<b>PRACTICE</b>", styles["h2"]),
            Paragraph("Practice the dialogue with a partner. Then create your own dialogue "
                      f"about {unit['title'].lower()} using the vocabulary from this unit.", styles["body"]),
            Spacer(1, 0.3 * cm),
            Paragraph("<b>Your Dialogue:</b>", styles["instr"]),
            Paragraph("<b>A:</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>B:</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>A:</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>B:</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>A:</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>B:</b> _______________________________________________", styles["ex"]),
            Spacer(1, 0.5 * cm),
        ]))

        # Speaking tasks
        elements.append(Paragraph("<b>SPEAKING TASKS</b>", styles["h2"]))
        speaking_tasks = [
            f"Tell your partner about {unit['title'].lower()} using at least 5 new words.",
            "Ask your partner 3 questions about the topic.",
            f"Present a short summary of what you learned about {unit['title'].lower()}.",
        ]
        for i, task in enumerate(speaking_tasks, 1):
            elements.append(Paragraph(f"<b>Task {i}:</b> {task}", styles["body"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Pronunciation
        elements.append(KeepTogether([
            Paragraph("<b>PRONUNCIATION CORNER</b>", styles["h2"]),
            Paragraph("Practice saying these words. Pay attention to the sounds.", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))
        pron_words = vocab[:6]
        rows_pr = [["Word", "Say it!", "Rhymes with..."]]
        for w in pron_words:
            rows_pr.append([w, f"/{w.lower()}/", "___________"])
        elements.append(_data_table(rows_pr, [pw * 0.3, pw * 0.3, pw * 0.3],
                                     fn, fb, get_color_hex("orange"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 14: Song / Chant ═══
        elements.append(_section_header("SONG / CHANT", "listening", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        song = ai.get("song_chant", {}) if ai else {}
        if song:
            elements.append(Paragraph(f'<b>{song.get("title", "Song")}</b>', styles["h2"]))
            elements.append(Spacer(1, 0.2 * cm))
            lyrics = song.get("lyrics", "")
            for lyric_line in lyrics.split("\n"):
                if lyric_line.strip():
                    elements.append(Paragraph(f"\u266B {lyric_line.strip()}", styles["song"]))
            elements.append(Spacer(1, 0.4 * cm))
        else:
            elements.append(Paragraph("<b>Let's Sing!</b>", styles["h2"]))
            elements.append(Paragraph(
                f"\u266B We are learning about {unit['title']}...", styles["song"]))
            elements.append(Paragraph(
                f"\u266B New words, new sounds every day...", styles["song"]))
            elements.append(Spacer(1, 0.4 * cm))

        # Song activities
        elements.append(KeepTogether([
            Paragraph("<b>SONG ACTIVITIES</b>", styles["h2"]),
            Paragraph("<b>A.</b> Underline the new words in the song.", styles["body"]),
            Paragraph("<b>B.</b> Clap the rhythm while singing.", styles["body"]),
            Paragraph(f"<b>C.</b> Write your own verse about {unit['title'].lower()}:", styles["body"]),
            Spacer(1, 0.2 * cm),
            _writing_lines(3, pw),
            Spacer(1, 0.5 * cm),
        ]))

        # ═══ PAGE 15: Culture Corner ═══
        elements.append(_section_header("CULTURE CORNER", "culture", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        cc = ai.get("culture_corner", {}) if ai else {}
        if cc:
            elements.append(Paragraph(f'<b>{cc.get("title", "Culture Corner")}</b>', styles["h2"]))
            elements.append(_content_box(cc.get("text", ""), "culture", pw, fn, grade))
        else:
            elements.append(Paragraph("<b>Did You Know?</b>", styles["h2"]))
            elements.append(_content_box(
                f"Different cultures have different perspectives on {unit['title'].lower()}. "
                f"Learning about these differences helps us understand the world better.",
                "culture", pw, fn, grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Fun Fact
        ff = ai.get("fun_fact", "") if ai else ""
        if ff:
            elements.append(_tip_box("Fun Fact", ff, "fact", pw, fn, fb, grade))
            elements.append(Spacer(1, 0.4 * cm))

        # Culture comparison
        elements.append(KeepTogether([
            Paragraph("<b>COMPARE CULTURES</b>", styles["h2"]),
            Paragraph("Think about how this topic is viewed in different cultures.", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))
        rows_cc = [["Question", "In Turkey", "In Another Country"]]
        rows_cc.append([f"How is {unit['title'].lower()} different?", "", ""])
        rows_cc.append(["What do people think about it?", "", ""])
        rows_cc.append(["What surprised you?", "", ""])
        elements.append(_data_table(rows_cc, [pw * 0.34, pw * 0.3, pw * 0.3],
                                     fn, fb, get_color_hex("blue_dark"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 16-17: Writing Workshop ═══
        elements.append(_section_header("WRITING WORKSHOP", "writing", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Writing model
        ex = ai.get("exercises", {}) if ai else {}
        wp = ex.get("writing_prompt", "")
        elements.append(Paragraph("<b>GUIDED WRITING</b>", styles["h2"]))

        if wp:
            elements.append(_tip_box("Writing Task", wp, "info", pw, fn, fb, grade))
        else:
            elements.append(_tip_box("Writing Task",
                                      f"Write a paragraph about {unit['title'].lower()} using "
                                      f"at least 5 new vocabulary words from this unit.",
                                      "info", pw, fn, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Writing plan
        elements.append(Paragraph("<b>PLAN YOUR WRITING</b>", styles["h2"]))
        plan_rows = [
            ["Section", "Your Notes"],
            ["Introduction", ""],
            ["Main Idea 1", ""],
            ["Main Idea 2", ""],
            ["Conclusion", ""],
        ]
        elements.append(_data_table(plan_rows, [pw * 0.25, pw * 0.7],
                                     fn, fb, get_color_hex("teal"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Writing space
        elements.append(Paragraph("<b>WRITE YOUR TEXT</b>", styles["h2"]))
        elements.append(Paragraph("Use your plan above to write your text.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(12, pw))
        elements.append(Spacer(1, 0.4 * cm))

        # Self-edit checklist
        elements.append(KeepTogether([
            Paragraph("<b>SELF-EDIT CHECKLIST</b>", styles["h2"]),
            Paragraph("\u2610 I used at least 5 new vocabulary words.", styles["body"]),
            Paragraph("\u2610 I checked my spelling.", styles["body"]),
            Paragraph(f"\u2610 I used the grammar structure from this unit.", styles["body"]),
            Paragraph("\u2610 My text has an introduction and conclusion.", styles["body"]),
            Paragraph("\u2610 I wrote at least 5 sentences.", styles["body"]),
            Spacer(1, 0.3 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 18: Project ═══
        elements.append(_section_header("PROJECT CORNER", "project", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} PROJECT</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Create a project about <b>{unit['title']}</b>. "
            f"You can work alone or with a partner.", styles["body"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Project options
        projects = [
            f"Make a poster about {unit['title'].lower()} with pictures and new words.",
            f"Create a mini-dictionary with all the vocabulary from this unit.",
            f"Write and perform a short skit about {unit['title'].lower()}.",
            f"Design a quiz about {unit['title'].lower()} for your classmates.",
        ]
        elements.append(Paragraph("<b>Choose one:</b>", styles["instr"]))
        for i, p in enumerate(projects, 1):
            elements.append(Paragraph(f"\u2610 <b>Option {i}:</b> {p}", styles["body"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Project planning
        elements.append(Paragraph("<b>PROJECT PLAN</b>", styles["h2"]))
        proj_plan = [
            ["Step", "What to Do", "Done?"],
            ["1. Research", f"Find information about {unit['title'].lower()}", "\u2610"],
            ["2. Organize", "Plan your project layout", "\u2610"],
            ["3. Create", "Make your project", "\u2610"],
            ["4. Present", "Share with the class", "\u2610"],
        ]
        elements.append(_data_table(proj_plan, [pw * 0.2, pw * 0.6, pw * 0.1],
                                     fn, fb, get_color_hex("gold"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Notes space
        elements.append(Paragraph("<b>MY PROJECT NOTES</b>", styles["h2"]))
        elements.append(_writing_lines(6, pw))
        elements.append(PageBreak())

        # ═══ PAGE 18-19: Extra Practice ═══
        elements.append(_section_header("EXTRA PRACTICE", "workbook", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Listening practice
        elements.append(Paragraph("<b>LISTENING PRACTICE</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Listen to your teacher read the text about {unit['title'].lower()}. "
            "Answer the questions below.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        listen_qs = [
            "What is the topic of the listening text?",
            "Name three key words you heard.",
            "What was the main message?",
            "Did you hear any words from this unit's vocabulary?",
            "Summarize what you heard in 2-3 sentences.",
        ]
        for i, q in enumerate(listen_qs, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {q}", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Extra exercises
        elements.append(Paragraph("<b>WORD BUILDING</b>", styles["h2"]))
        elements.append(Paragraph(
            "Make new words by adding prefixes or suffixes.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        wb_rows = [["Base Word", "+ Prefix/Suffix", "= New Word", "Meaning"]]
        for w in vocab[:6]:
            wb_rows.append([w, "", "", ""])
        elements.append(_data_table(wb_rows, [pw * 0.2, pw * 0.22, pw * 0.25, pw * 0.25],
                                     fn, fb, get_color_hex("purple"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Sentence transformation
        elements.append(Paragraph("<b>SENTENCE TRANSFORMATION</b>", styles["h2"]))
        elements.append(Paragraph(
            "Rewrite each sentence using the word in brackets.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 7):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph(
                "   \u2192 _______________________________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 19: Pair Work & Daily English ═══
        elements.append(_section_header("PAIR WORK & DAILY ENGLISH", "speaking", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Pair work activity
        elements.append(Paragraph("<b>PAIR WORK — INFORMATION GAP</b>", styles["h2"]))
        elements.append(Paragraph(
            "Work with a partner. Student A has information that Student B needs, "
            "and vice versa. Ask and answer questions to complete your table.",
            styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        gap_rows = [["Question", "Student A", "Student B"]]
        gap_questions = [
            f"What is your favorite thing about {unit['title'].lower()}?",
            "Which new word do you like most?",
            "Can you make a sentence with it?",
            "What did you learn today?",
        ]
        for gq in gap_questions:
            gap_rows.append([gq, "", ""])
        elements.append(_data_table(gap_rows, [pw * 0.4, pw * 0.25, pw * 0.25],
                                     fn, fb, get_color_hex("gold"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Role play
        elements.append(Paragraph("<b>ROLE PLAY</b>", styles["h2"]))
        elements.append(Paragraph(
            f"With your partner, act out a scene about {unit['title'].lower()}. "
            "Use at least 5 vocabulary words.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Setting:</b> ___________________________", styles["ex"]))
        elements.append(Paragraph("<b>Characters:</b> ___________________________", styles["ex"]))
        elements.append(Paragraph("<b>Situation:</b> ___________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Your Script:</b>", styles["instr"]))
        elements.append(_writing_lines(6, pw))
        elements.append(Spacer(1, 0.4 * cm))

        # Daily English expressions
        elements.append(Paragraph("<b>DAILY ENGLISH</b>", styles["h2"]))
        elements.append(Paragraph(
            "Useful expressions related to this unit:", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        daily_rows = [["Expression", "Turkish", "When to Use"]]
        daily_expressions = [
            [f"Let's talk about {unit['title'].lower()}.", "", "Starting a conversation"],
            ["I think that...", "", "Giving your opinion"],
            ["Can you explain...?", "", "Asking for help"],
            ["In my opinion...", "", "Sharing ideas"],
            ["I agree / I disagree because...", "", "Discussion"],
            ["That's a great point!", "", "Responding to others"],
        ]
        for de in daily_expressions:
            daily_rows.append(de)
        elements.append(_data_table(daily_rows, [pw * 0.35, pw * 0.25, pw * 0.3],
                                     fn, fb, get_color_hex("teal"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 20-21: Unit Review & Self-Assessment ═══
        elements.append(_section_header("UNIT REVIEW", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Quick review quiz
        elements.append(Paragraph("<b>REVIEW QUIZ</b>", styles["h2"]))
        elements.append(Paragraph(
            "Test yourself! Answer these questions without looking back.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))

        review_qs = [
            f"Name 5 vocabulary words from this unit.",
            f"What grammar structure did you learn?",
            f"What was the story about?",
            f"Write one sentence using a new word.",
            f"What was the most interesting thing you learned about {unit['title'].lower()}?",
        ]
        for i, q in enumerate(review_qs, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {q}", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Skills checklist
        elements.append(KeepTogether([
            Paragraph("<b>SKILLS CHECKLIST</b>", styles["h2"]),
            Paragraph("Check what you can do now:", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))

        skill_checks = []
        for sk, descs in skills.items():
            label = {"listening": "Listening", "speaking": "Speaking",
                     "reading": "Reading", "writing": "Writing"}.get(sk, sk.title())
            for d in descs[:2]:
                skill_checks.append(f"\u2610 <b>{label}:</b> {d}")

        if not skill_checks:
            skill_checks = [
                f"\u2610 I can understand texts about {unit['title'].lower()}.",
                f"\u2610 I can talk about {unit['title'].lower()} with my classmates.",
                f"\u2610 I can write about {unit['title'].lower()} using new words.",
                f"\u2610 I know the key vocabulary of this unit.",
            ]
        for sc_item in skill_checks:
            elements.append(Paragraph(sc_item, styles["body"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Self-assessment
        elements.append(KeepTogether([
            Paragraph("<b>SELF-ASSESSMENT</b>", styles["h2"]),
            Spacer(1, 0.2 * cm),
        ]))
        sa_rows = [["Skill", "\u2B50\u2B50\u2B50", "\u2B50\u2B50", "\u2B50"]]
        sa_rows.append(["Vocabulary", "\u2610 Excellent", "\u2610 Good", "\u2610 Need practice"])
        sa_rows.append(["Grammar", "\u2610 Excellent", "\u2610 Good", "\u2610 Need practice"])
        sa_rows.append(["Reading", "\u2610 Excellent", "\u2610 Good", "\u2610 Need practice"])
        sa_rows.append(["Writing", "\u2610 Excellent", "\u2610 Good", "\u2610 Need practice"])
        sa_rows.append(["Speaking", "\u2610 Excellent", "\u2610 Good", "\u2610 Need practice"])
        sa_rows.append(["Listening", "\u2610 Excellent", "\u2610 Good", "\u2610 Need practice"])
        elements.append(_data_table(sa_rows, [pw * 0.22, pw * 0.26, pw * 0.22, pw * 0.26],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Reflection
        elements.append(Paragraph("<b>MY REFLECTION</b>", styles["h2"]))
        elements.append(Paragraph("What I liked most about this unit:", styles["body"]))
        elements.append(_writing_lines(2, pw))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("What I want to practice more:", styles["body"]))
        elements.append(_writing_lines(2, pw))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("My goal for the next unit:", styles["body"]))
        elements.append(_writing_lines(2, pw))
        elements.append(PageBreak())

        # ═══ BONUS PAGE: Mini Test ═══
        elements.append(_section_header("UNIT TEST", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — MINI TEST</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        # Part A
        elements.append(Paragraph("<b>PART A: VOCABULARY (10 points)</b>", styles["h2"]))
        elements.append(Paragraph("Write the correct word for each definition.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________ : _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Part B
        elements.append(Paragraph("<b>PART B: GRAMMAR (10 points)</b>", styles["h2"]))
        elements.append(Paragraph("Complete the sentences with the correct form.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Part C
        elements.append(Paragraph("<b>PART C: WRITING (10 points)</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write 5 sentences about {unit['title'].lower()} using vocabulary and grammar "
            "from this unit.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(7, pw))
        elements.append(Spacer(1, 0.3 * cm))

        # Score
        score_rows = [
            ["Part", "Points", "My Score"],
            ["A: Vocabulary", "10", ""],
            ["B: Grammar", "10", ""],
            ["C: Writing", "10", ""],
            ["TOTAL", "30", ""],
        ]
        elements.append(_data_table(score_rows, [pw * 0.35, pw * 0.2, pw * 0.2],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(PageBreak())

    # ── Back Cover ──
    _back_cover(elements, styles, accent, grade, fn, fb)

    tmpl.build(elements)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTION 2: WORKBOOK — ~20 pages per unit
# ═══════════════════════════════════════════════════════════════════════════════

def generate_workbook_pdf(grade: int, curriculum_weeks: list[dict]) -> bytes | None:
    """Generate premium Workbook PDF — ~20 pages per unit with rich exercises."""
    if not curriculum_weeks:
        return None
    fn, fb = ensure_turkish_pdf_fonts()
    accent, bg_hex = GRADE_COLORS.get(grade, ("#3B82F6", "#EFF6FF"))
    units = _group_units(curriculum_weeks)
    book_name = BOOK_TITLES.get(grade, BOOK_TITLES[5])["workbook"]
    styles = _make_styles(fn, fb, grade, accent)
    young = _is_young(grade)
    pw = _PW
    rng = random.Random(42 + grade)

    from views.book_content_ai import _load_cache

    buf = io.BytesIO()
    tmpl = _BookTemplate(buf, grade, book_name, fn, fb, accent)

    elements: list = []

    _premium_cover(elements, book_name, grade, "English Workbook", styles, accent, fn, fb, units)
    _premium_toc(elements, units, styles, grade, fn, fb, accent)

    for unit in units:
        vocab = _collect_vocab(unit["weeks"])
        structs = _collect_structures(unit["weeks"])
        skills = _collect_skills(unit["weeks"])

        tmpl.set_current_unit(f"Unit {unit['num']}: {unit['title']}")

        ai = _load_cache(grade, unit["num"])
        ai_ex = ai.get("exercises", {}) if ai else {}
        ai_vocab = ai.get("vocabulary_enrichment", {}).get("definitions", []) if ai else []

        # ═══ PAGE 1: Unit Opener ═══
        _premium_unit_opener(elements, unit, styles, grade, fn, fb, accent, vocab, skills)

        # ═══ PAGE 2-3: Vocabulary Exercises ═══
        elements.append(_section_header("VOCABULARY EXERCISES", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 1: Match words
        elements.append(Paragraph("<b>Exercise 1 — Match the Words to Their Definitions</b>", styles["h2"]))
        elements.append(Paragraph("Draw a line from Column A to Column B.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        match_data = ai_ex.get("matching", []) if ai_ex else []
        if match_data:
            rows_m = [["Column A (Word)", "Column B (Definition)"]]
            for md in match_data[:10]:
                rows_m.append([md.get("left", ""), md.get("right", "")])
        else:
            rows_m = [["Column A (Word)", "Column B (Definition)"]]
            for w in vocab[:8]:
                rows_m.append([w, "_______________"])
        elements.append(_data_table(rows_m, [pw * 0.4, pw * 0.5], fn, fb, accent, grade))
        elements.append(Spacer(1, 0.5 * cm))

        # Exercise 2: Fill in the blanks
        elements.append(Paragraph("<b>Exercise 2 — Fill in the Blanks</b>", styles["h2"]))
        word_bank = ", ".join(vocab[:8])
        elements.append(_tip_box("Word Bank", word_bank, "info", pw, fn, fb, grade))
        elements.append(Spacer(1, 0.2 * cm))
        fill_data = ai_ex.get("fill_blanks", []) if ai_ex else []
        if fill_data:
            for i, fb_item in enumerate(fill_data[:8], 1):
                sent = fb_item.get("sentence", "")
                elements.append(Paragraph(f"<b>{i}.</b> {sent}", styles["ex"]))
        else:
            for i, w in enumerate(vocab[:8], 1):
                elements.append(Paragraph(
                    f"<b>{i}.</b> I like __________ very much.", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 3: Unscramble
        elements.append(KeepTogether([
            Paragraph("<b>Exercise 3 — Unscramble the Words</b>", styles["h2"]),
            Paragraph("Rearrange the letters to make a word from this unit.", styles["instr"]),
            Spacer(1, 0.2 * cm),
        ]))
        for i, w in enumerate(vocab[:8], 1):
            chars = list(w.upper())
            rng.shuffle(chars)
            scrambled = " ".join(chars)
            elements.append(Paragraph(
                f"<b>{i}.</b> {scrambled}  \u2192  _______________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 4-5: Grammar Exercises ═══
        elements.append(_section_header("GRAMMAR EXERCISES", "grammar", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Grammar rule reminder
        gf = ai.get("grammar_focus", {}) if ai else {}
        if gf and gf.get("rule"):
            elements.append(_tip_box("Remember the Rule", gf["rule"], "rule", pw, fn, fb, grade))
            elements.append(Spacer(1, 0.3 * cm))

        # Exercise 4: Reorder sentences
        elements.append(Paragraph("<b>Exercise 4 — Put the Words in Order</b>", styles["h2"]))
        elements.append(Paragraph("Rearrange the words to make correct sentences.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        reorder = ai_ex.get("reorder", []) if ai_ex else []
        if reorder:
            for i, ro in enumerate(reorder[:6], 1):
                words = ro.get("words", [])
                elements.append(Paragraph(
                    f"<b>{i}.</b> {' / '.join(words)}", styles["ex"]))
                elements.append(Paragraph("   \u2192 _______________________________________________", styles["ex"]))
        else:
            for i in range(1, 7):
                elements.append(Paragraph(
                    f"<b>{i}.</b> _______________________________________________", styles["ex"]))
                elements.append(Paragraph(
                    "   \u2192 _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 5: Correct the mistakes
        elements.append(Paragraph("<b>Exercise 5 — Find and Correct the Mistakes</b>", styles["h2"]))
        elements.append(Paragraph("Each sentence has one mistake. Find and correct it.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 7):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph(
                "   Correction: _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 6: Complete with grammar structure
        elements.append(KeepTogether([
            Paragraph("<b>Exercise 6 — Complete the Sentences</b>", styles["h2"]),
            Paragraph("Use the correct form of the words in brackets.", styles["instr"]),
            Spacer(1, 0.2 * cm),
        ]))
        for i in range(1, 7):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 6-7: Reading Exercises ═══
        elements.append(_section_header("READING EXERCISES", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 7: Read and answer
        elements.append(Paragraph("<b>Exercise 7 — Read and Answer</b>", styles["h2"]))
        ai_rp = ai.get("reading_passage", {}) if ai else {}
        if ai_rp and ai_rp.get("text"):
            elements.append(_content_box(ai_rp["text"], "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.3 * cm))
            for qi, q in enumerate(ai_rp.get("questions", [])[:5], 1):
                elements.append(Paragraph(f"<b>{qi}.</b> {q}", styles["ex"]))
                elements.append(Paragraph("_______________________________________________", styles["ex"]))
        else:
            elements.append(_content_box(
                _auto_story(unit["title"], vocab[:6], grade), "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.3 * cm))
            for qi, q in enumerate([
                "What is the main idea?",
                "List 3 new words from the text.",
                f"Why is {unit['title'].lower()} important?",
            ], 1):
                elements.append(Paragraph(f"<b>{qi}.</b> {q}", styles["ex"]))
                elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 8: True or False
        elements.append(KeepTogether([
            Paragraph("<b>Exercise 8 — True or False?</b>", styles["h2"]),
            Paragraph("Read the text again and write T (True) or F (False).", styles["instr"]),
            Spacer(1, 0.2 * cm),
            Paragraph(f"<b>1.</b> The text is about {unit['title'].lower()}.  (    )", styles["ex"]),
            Paragraph("<b>2.</b> There are no new words in this text.  (    )", styles["ex"]),
            Paragraph("<b>3.</b> The text has useful information.  (    )", styles["ex"]),
            Paragraph(f"<b>4.</b> {unit['title']} is not important.  (    )", styles["ex"]),
            Paragraph("<b>5.</b> We can learn new things from this text.  (    )", styles["ex"]),
            Spacer(1, 0.4 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 8-9: Word Search + Crossword ═══
        elements.append(_section_header("WORD PUZZLES", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 9: Word search grid
        elements.append(Paragraph("<b>Exercise 9 — Word Search</b>", styles["h2"]))
        elements.append(Paragraph("Find these words in the grid:", styles["instr"]))
        ws_words = vocab[:8]
        elements.append(Paragraph(f"<b>{', '.join(ws_words)}</b>", styles["body_c"]))
        elements.append(Spacer(1, 0.3 * cm))

        grid_size = 10
        grid: list[list[str]] = []
        for r in range(grid_size):
            row = [chr(rng.randint(65, 90)) for _ in range(grid_size)]
            if r < len(ws_words):
                word = ws_words[r].upper()[:grid_size]
                start = rng.randint(0, max(0, grid_size - len(word)))
                for ci, ch in enumerate(word):
                    if start + ci < grid_size:
                        row[start + ci] = ch
            grid.append(row)

        cell_sz = min(1.2 * cm, pw / (grid_size + 1))
        t = Table(grid, colWidths=[cell_sz] * grid_size, rowHeights=[cell_sz] * grid_size)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, _hex("#cbd5e1")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), fb),
            ("FONTSIZE", (0, 0), (-1, -1), round(10 * get_tier_for_grade(grade)["font_scale"], 0)),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#f8fafc")),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.5 * cm))

        # Exercise 10: Crossword clues
        elements.append(Paragraph("<b>Exercise 10 — Crossword Clues</b>", styles["h2"]))
        clue_words = ai_vocab if ai_vocab else [
            {"word": w, "definition": f"Related to {unit['title'].lower()}"} for w in vocab]

        elements.append(Paragraph("<b>Across:</b>", styles["instr"]))
        for i, cw in enumerate(clue_words[:5], 1):
            word = cw.get("word", "")
            defn = cw.get("definition", "")
            blanks = word[0] + " _" * (len(word) - 1)
            elements.append(Paragraph(f"<b>{i}.</b> {defn}  ({blanks})", styles["ex"]))

        if len(clue_words) > 5:
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(Paragraph("<b>Down:</b>", styles["instr"]))
            for i, cw in enumerate(clue_words[5:10], 1):
                word = cw.get("word", "")
                defn = cw.get("definition", "")
                blanks = word[0] + " _" * (len(word) - 1)
                elements.append(Paragraph(f"<b>{i}.</b> {defn}  ({blanks})", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 10-11: Listening & Speaking Exercises ═══
        elements.append(_section_header("LISTENING & SPEAKING EXERCISES", "listening", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 11: Dialogue completion
        elements.append(Paragraph("<b>Exercise 11 — Complete the Dialogue</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Complete this dialogue about {unit['title'].lower()} using the words from the word bank.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        dlg_words = vocab[:4]
        elements.append(_tip_box("Word Bank", "  |  ".join(dlg_words), "info", pw, fn, fb, grade))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>A:</b> Hi! Do you know about __________?", styles["ex"]))
        elements.append(Paragraph("<b>B:</b> Yes! I really like __________.", styles["ex"]))
        elements.append(Paragraph("<b>A:</b> Me too! What about __________?", styles["ex"]))
        elements.append(Paragraph("<b>B:</b> That's interesting. I want to learn more about __________.", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 12: Create your dialogue
        elements.append(Paragraph("<b>Exercise 12 — Write Your Own Dialogue</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Create a dialogue about {unit['title'].lower()} with a partner. "
            "Use at least 4 vocabulary words.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(6):
            label = "A" if i % 2 == 0 else "B"
            elements.append(Paragraph(f"<b>{label}:</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 13: Speaking prompts
        elements.append(KeepTogether([
            Paragraph("<b>Exercise 13 — Speaking Practice</b>", styles["h2"]),
            Paragraph("Choose one topic and talk for 1 minute:", styles["instr"]),
            Spacer(1, 0.2 * cm),
            Paragraph(f"\u2610 <b>A.</b> Tell your partner 5 things about {unit['title'].lower()}.", styles["ex"]),
            Paragraph(f"\u2610 <b>B.</b> Describe {unit['title'].lower()} without using the word itself.", styles["ex"]),
            Paragraph(f"\u2610 <b>C.</b> Ask and answer 3 questions about {unit['title'].lower()} with your partner.", styles["ex"]),
            Spacer(1, 0.3 * cm),
        ]))

        # Exercise 14: Pronunciation
        elements.append(Paragraph("<b>Exercise 14 — Pronunciation Practice</b>", styles["h2"]))
        elements.append(Paragraph("Say each word 3 times. Then use it in a sentence.", styles["instr"]))
        pron_rows = [["#", "Word", "My Sentence"]]
        for i, w in enumerate(vocab[:6], 1):
            pron_rows.append([str(i), w, ""])
        elements.append(_data_table(pron_rows, [pw * 0.08, pw * 0.25, pw * 0.6],
                                     fn, fb, get_color_hex("orange"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 12-13: Writing Exercises ═══
        elements.append(_section_header("WRITING EXERCISES", "writing", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 15: Sentence building
        elements.append(Paragraph("<b>Exercise 15 — Build Sentences</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write sentences using each word. Follow the example.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        if vocab:
            elements.append(Paragraph(
                f'<b>Example:</b> <i>{vocab[0]}</i> \u2192 I learned about {vocab[0]} in class today.',
                styles["body"]))
            elements.append(Spacer(1, 0.2 * cm))
        for i, w in enumerate(vocab[:8], 1):
            elements.append(Paragraph(f"<b>{i}.</b> <i>{w}</i> \u2192 _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 16: Paragraph writing
        elements.append(Paragraph("<b>Exercise 16 — Write a Paragraph</b>", styles["h2"]))
        elements.append(_tip_box("Writing Task",
                                  f"Write a paragraph (6-8 sentences) about {unit['title'].lower()}. "
                                  f"Use at least 5 words from the vocabulary list.",
                                  "info", pw, fn, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(_writing_lines(10, pw))
        elements.append(PageBreak())

        # ═══ PAGE 14-15: Mixed Exercises ═══
        elements.append(_section_header("MIXED EXERCISES", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 17: Multiple choice
        elements.append(Paragraph("<b>Exercise 17 — Multiple Choice</b>", styles["h2"]))
        elements.append(Paragraph("Choose the correct answer.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 6):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("   a) __________  b) __________  c) __________", styles["ex"]))
            elements.append(Spacer(1, 0.2 * cm))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 18: Odd one out
        elements.append(Paragraph("<b>Exercise 18 — Odd One Out</b>", styles["h2"]))
        elements.append(Paragraph("Circle the word that doesn't belong.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 6):
            group = vocab[i * 3:(i * 3) + 4] if len(vocab) > i * 3 + 3 else vocab[:4]
            rng.shuffle(group)
            elements.append(Paragraph(
                f"<b>{i}.</b> {' — '.join(group[:4])}", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 19: Translation
        elements.append(Paragraph("<b>Exercise 19 — Translate</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write the Turkish meaning, then write an English sentence.", styles["instr"]))
        trans_rows = [["Word", "Turkish", "English Sentence"]]
        for w in vocab[:6]:
            trans_rows.append([w, "", ""])
        elements.append(_data_table(trans_rows, [pw * 0.2, pw * 0.25, pw * 0.45],
                                     fn, fb, get_color_hex("teal"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 16-17: Creative Activities ═══
        elements.append(_section_header("CREATIVE ACTIVITIES", "project", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Exercise 20: Draw and label
        elements.append(Paragraph("<b>Exercise 20 — Draw and Label</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Draw a picture related to {unit['title'].lower()} and label it with vocabulary words.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))

        # Drawing box
        draw_box = Table([[""]], colWidths=[pw], rowHeights=[8 * cm])
        draw_box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ]))
        elements.append(draw_box)
        elements.append(Spacer(1, 0.4 * cm))

        # Exercise 21: Mini story writing
        elements.append(Paragraph("<b>Exercise 21 — Write a Mini Story</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write a short story (5-8 sentences) about {unit['title'].lower()}. "
            "Use your imagination!", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Title:</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(8, pw))
        elements.append(PageBreak())

        # ═══ PAGE 18-19: Test Practice ═══
        elements.append(_section_header("TEST PRACTICE", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — PRACTICE TEST</b>", styles["h2"]))
        elements.append(Paragraph(
            "Complete this test to check your understanding of the unit.", styles["body"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Part A: Vocabulary
        elements.append(Paragraph("<b>PART A: VOCABULARY (10 points)</b>", styles["h2"]))
        for i in range(1, 6):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Part B: Grammar
        elements.append(Paragraph("<b>PART B: GRAMMAR (10 points)</b>", styles["h2"]))
        for i in range(1, 6):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Part C: Reading
        elements.append(Paragraph("<b>PART C: READING (10 points)</b>", styles["h2"]))
        if ai_rp and ai_rp.get("text"):
            short_text = ai_rp["text"][:200] + "..."
            elements.append(_content_box(short_text, "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 4):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Part D: Writing
        elements.append(Paragraph("<b>PART D: WRITING (10 points)</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write 5 sentences about {unit['title'].lower()} using new vocabulary.", styles["instr"]))
        elements.append(_writing_lines(6, pw))
        elements.append(Spacer(1, 0.3 * cm))

        # Score box
        score_rows = [
            ["Section", "Points", "My Score"],
            ["Part A: Vocabulary", "10", ""],
            ["Part B: Grammar", "10", ""],
            ["Part C: Reading", "10", ""],
            ["Part D: Writing", "10", ""],
            ["TOTAL", "40", ""],
        ]
        elements.append(_data_table(score_rows, [pw * 0.4, pw * 0.2, pw * 0.2],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(PageBreak())

        # ═══ EXTRA: Sentence Building & Transformation ═══
        elements.append(_section_header("SENTENCE WORKSHOP", "grammar", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Exercise 22 — Make Questions</b>", styles["h2"]))
        elements.append(Paragraph("Turn each sentence into a question.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 7):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("   ? _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 23 — Make Negatives</b>", styles["h2"]))
        elements.append(Paragraph("Rewrite each sentence in the negative form.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 7):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("   \u2192 _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 24 — Connect the Sentences</b>", styles["h2"]))
        elements.append(Paragraph(
            "Join each pair of sentences using: <b>and, but, because, so, or</b>", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 6):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("   + _______________________________________________", styles["ex"]))
            elements.append(Paragraph("   = _______________________________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ EXTRA: Listening & Dictation ═══
        elements.append(_section_header("LISTENING & DICTATION", "listening", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Exercise 25 — Dictation</b>", styles["h2"]))
        elements.append(Paragraph(
            "Listen to your teacher and write the sentences.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(8, pw))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 26 — Listen and Complete</b>", styles["h2"]))
        elements.append(Paragraph(
            "Listen to the dialogue and fill in the missing words.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>A:</b> Hi! Have you ever been to __________?", styles["ex"]))
        elements.append(Paragraph("<b>B:</b> Yes! I __________ it last __________.", styles["ex"]))
        elements.append(Paragraph("<b>A:</b> What did you think about __________?", styles["ex"]))
        elements.append(Paragraph("<b>B:</b> It was __________! I want to __________ again.", styles["ex"]))
        elements.append(Paragraph("<b>A:</b> That sounds __________. Can I __________ too?", styles["ex"]))
        elements.append(Paragraph("<b>B:</b> Of course! Let's __________ together.", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 27 — Spelling Bee</b>", styles["h2"]))
        elements.append(Paragraph(
            "Listen to your teacher spell these words. Write them correctly.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        spell_rows = [["#", "I heard...", "Correct spelling", "Meaning"]]
        for i in range(1, 9):
            spell_rows.append([str(i), "", "", ""])
        elements.append(_data_table(spell_rows, [pw * 0.06, pw * 0.28, pw * 0.28, pw * 0.3],
                                     fn, fb, get_color_hex("orange"), grade))
        elements.append(PageBreak())

        # ═══ EXTRA: Project & Creative Writing ═══
        elements.append(_section_header("CREATIVE CORNER", "project", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Exercise 28 — Design a Poster</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Design a poster about {unit['title'].lower()}. Include a title, "
            "pictures, and at least 8 vocabulary words.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        poster_box = Table([[""]], colWidths=[pw], rowHeights=[9 * cm])
        poster_box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ]))
        elements.append(poster_box)
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 29 — Letter Writing</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write a letter to a friend about {unit['title'].lower()}. "
            "Tell them what you learned and why it's interesting.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("Dear __________,", styles["ex"]))
        elements.append(_writing_lines(10, pw))
        elements.append(Paragraph("Your friend, __________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ EXTRA: Fun Activities ═══
        elements.append(_section_header("FUN ACTIVITIES", "gamification", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Word chain
        elements.append(Paragraph("<b>Exercise 30 — Word Chain</b>", styles["h2"]))
        elements.append(Paragraph(
            "The last letter of each word is the first letter of the next word. "
            "Complete the chain using unit vocabulary.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        if vocab:
            elements.append(Paragraph(
                f"<b>{vocab[0]}</b> \u2192 __________ \u2192 __________ \u2192 __________ "
                "\u2192 __________ \u2192 __________", styles["body"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Secret message
        elements.append(Paragraph("<b>Exercise 31 — Secret Message</b>", styles["h2"]))
        elements.append(Paragraph(
            "Use the first letter of each answer to reveal a secret word.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 7):
            elements.append(Paragraph(
                f"<b>{i}.</b> Clue: _______________  Answer: __ __ __ __ __ __", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("Secret word: __ __ __ __ __ __", styles["body_c"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Draw and describe
        elements.append(Paragraph("<b>Exercise 32 — Draw and Describe</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Draw something related to {unit['title'].lower()}, then describe it in 4 sentences.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        draw_box2 = Table([[""]], colWidths=[pw], rowHeights=[6 * cm])
        draw_box2.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ]))
        elements.append(draw_box2)
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(4, pw))
        elements.append(PageBreak())

        # ═══ EXTRA: Revision & Consolidation ═══
        elements.append(_section_header("REVISION & CONSOLIDATION", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Exercise 33 — Quick Quiz</b>", styles["h2"]))
        elements.append(Paragraph("Answer as fast as you can!", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        quiz_qs = [
            f"Write 3 words about {unit['title'].lower()}: __________",
            "Write the opposite of a word from this unit: __________",
            "Complete: I have __________ about this topic.",
            f"True or False: {unit['title']} is important. __________",
            "Write a question using a new word: __________",
            "Spell the hardest word from this unit: __________",
            "Name a word family from this unit: __________",
            "Write a sentence with 3 new words: __________",
        ]
        for i, q in enumerate(quiz_qs, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {q}", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 34 — Error Correction</b>", styles["h2"]))
        elements.append(Paragraph("Find and correct the mistake in each sentence.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 7):
            elements.append(Paragraph(f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("   Correction: _______________________________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ EXTRA: Pair & Group Work ═══
        elements.append(_section_header("PAIR & GROUP ACTIVITIES", "speaking", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Exercise 35 — Interview Your Partner</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Ask your partner these questions about {unit['title'].lower()}. "
            "Write their answers.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        int_rows = [["Question", "Partner's Answer"]]
        int_questions = [
            f"What do you know about {unit['title'].lower()}?",
            "Which new word is your favorite?",
            "Can you use it in a sentence?",
            "What was easy in this unit?",
            "What was difficult?",
        ]
        for iq in int_questions:
            int_rows.append([iq, ""])
        elements.append(_data_table(int_rows, [pw * 0.45, pw * 0.45],
                                     fn, fb, get_color_hex("gold"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>Exercise 36 — Group Presentation</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Work in groups of 3-4. Prepare a 2-minute presentation about {unit['title'].lower()}.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Topic:</b> ___________________________", styles["ex"]))
        elements.append(Paragraph("<b>Group members:</b> ___________________________", styles["ex"]))
        elements.append(Paragraph("<b>Key points:</b>", styles["instr"]))
        elements.append(Paragraph("1. _______________________________________________", styles["ex"]))
        elements.append(Paragraph("2. _______________________________________________", styles["ex"]))
        elements.append(Paragraph("3. _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Visual aids I will use:</b>", styles["instr"]))
        elements.append(_writing_lines(3, pw))
        elements.append(PageBreak())

        # ═══ Self-Assessment ═══
        elements.append(_section_header("SELF-ASSESSMENT", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — HOW DID I DO?</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        sa_rows = [["I can...", "\u2B50\u2B50\u2B50", "\u2B50\u2B50", "\u2B50"]]
        sa_items = [
            f"understand texts about {unit['title'].lower()}",
            f"use vocabulary from this unit correctly",
            f"use the grammar structure in sentences",
            f"talk about {unit['title'].lower()} with friends",
            f"write a paragraph about {unit['title'].lower()}",
            "spell the new words correctly",
        ]
        for item in sa_items:
            sa_rows.append([item, "\u2610", "\u2610", "\u2610"])
        elements.append(_data_table(sa_rows, [pw * 0.46, pw * 0.16, pw * 0.16, pw * 0.16],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(Spacer(1, 0.5 * cm))

        # Reflection
        elements.append(Paragraph("<b>MY NOTES</b>", styles["h2"]))
        elements.append(Paragraph("Words I need to practice more:", styles["body"]))
        elements.append(_writing_lines(3, pw))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("Things I did well:", styles["body"]))
        elements.append(_writing_lines(3, pw))
        elements.append(PageBreak())

    _back_cover(elements, styles, accent, grade, fn, fb)

    tmpl.build(elements)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTION 3: READING BOOK — ~20 pages per unit
# ═══════════════════════════════════════════════════════════════════════════════

def generate_reading_book_pdf(grade: int, curriculum_weeks: list[dict]) -> bytes | None:
    """Generate premium Reading Book PDF — ~20 pages per unit."""
    if not curriculum_weeks:
        return None
    fn, fb = ensure_turkish_pdf_fonts()
    accent, bg_hex = GRADE_COLORS.get(grade, ("#3B82F6", "#EFF6FF"))
    units = _group_units(curriculum_weeks)
    book_name = BOOK_TITLES.get(grade, BOOK_TITLES[5])["reading"]
    styles = _make_styles(fn, fb, grade, accent)
    young = _is_young(grade)
    pw = _PW

    from views.book_content_ai import _load_cache

    buf = io.BytesIO()
    tmpl = _BookTemplate(buf, grade, book_name, fn, fb, accent)

    elements: list = []

    _premium_cover(elements, book_name, grade, "Reading Book", styles, accent, fn, fb, units)
    _premium_toc(elements, units, styles, grade, fn, fb, accent)

    for unit in units:
        vocab = _collect_vocab(unit["weeks"])
        skills = _collect_skills(unit["weeks"])
        tmpl.set_current_unit(f"Unit {unit['num']}: {unit['title']}")

        ai = _load_cache(grade, unit["num"])

        # ═══ PAGE 1: Unit Opener ═══
        _premium_unit_opener(elements, unit, styles, grade, fn, fb, accent, vocab, skills)

        # ═══ PAGE 2: Pre-Reading ═══
        elements.append(_section_header("PRE-READING", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>BEFORE YOU READ</b>", styles["h2"]))
        elements.append(Paragraph(
            "Look at the title and think about these questions:", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        pre_qs = [
            f"What do you already know about {unit['title'].lower()}?",
            "What do you think the reading will be about?",
            "What words do you expect to see?",
        ]
        for q in pre_qs:
            elements.append(Paragraph(f"\u2022 {q}", styles["body"]))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>KEY VOCABULARY</b>", styles["h2"]))
        elements.append(Paragraph(
            "Learn these words before reading:", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))

        vocab_defs = ai.get("vocabulary_enrichment", {}).get("definitions", []) if ai else []
        if vocab_defs:
            rows_v = [["Word", "Meaning", "Turkish"]]
            for vd in vocab_defs[:10]:
                rows_v.append([vd.get("word", ""), vd.get("definition", ""),
                               vd.get("turkish_hint", "")])
            elements.append(_data_table(rows_v, [pw * 0.2, pw * 0.5, pw * 0.2],
                                         fn, fb, get_color_hex("green"), grade))
        else:
            for w in vocab[:8]:
                elements.append(Paragraph(f"\u2022 <b>{w}</b>", styles["body"]))
        elements.append(PageBreak())

        # ═══ PAGE 3-5: Reading 1 — Story ═══
        elements.append(_section_header("READING 1 — STORY", "story", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        ai_story = ai.get("story", {}) if ai else {}
        if ai_story:
            elements.append(Paragraph(f'<b>{ai_story.get("title", "Story")}</b>', styles["h2"]))
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(_content_box(ai_story.get("text", ""), "story", pw, fn, grade))

            moral = ai_story.get("moral", "")
            if moral:
                elements.append(Spacer(1, 0.3 * cm))
                elements.append(_tip_box("Moral", moral, "fact", pw, fn, fb, grade))
        else:
            elements.append(Paragraph("<b>Story</b>", styles["h2"]))
            elements.append(_content_box(
                _auto_story(unit["title"], vocab, grade), "story", pw, fn, grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Comprehension
        elements.append(Paragraph("<b>COMPREHENSION CHECK</b>", styles["h2"]))
        elements.append(Paragraph(
            "<b>A. Answer the questions.</b>", styles["instr"]))
        comp_qs = [
            "What is the main idea of the story?",
            "Who are the main characters?",
            "What happened at the beginning, middle, and end?",
            "What lesson did you learn?",
            f"How does this story relate to {unit['title'].lower()}?",
        ]
        for i, q in enumerate(comp_qs, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {q}", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(KeepTogether([
            Paragraph("<b>B. True or False?</b>", styles["instr"]),
            Spacer(1, 0.2 * cm),
            Paragraph(f"<b>1.</b> The story is about {unit['title'].lower()}.  ( T / F )", styles["ex"]),
            Paragraph("<b>2.</b> The characters learned something new.  ( T / F )", styles["ex"]),
            Paragraph("<b>3.</b> The story has a happy ending.  ( T / F )", styles["ex"]),
            Paragraph("<b>4.</b> There are no new vocabulary words.  ( T / F )", styles["ex"]),
            Paragraph("<b>5.</b> The moral of the story is important.  ( T / F )", styles["ex"]),
            Spacer(1, 0.3 * cm),
        ]))

        # Vocabulary from story
        elements.append(KeepTogether([
            Paragraph("<b>C. Vocabulary from the Story</b>", styles["instr"]),
            Paragraph("Find these words in the story and write the sentence they appear in.", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))
        for w in vocab[:5]:
            elements.append(Paragraph(f"<b>{w}:</b> _______________________________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 6-8: Reading 2 — Information Text ═══
        elements.append(_section_header("READING 2 — INFORMATION TEXT", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        ai_rp = ai.get("reading_passage", {}) if ai else {}
        if ai_rp and ai_rp.get("text"):
            elements.append(Paragraph(f'<b>{ai_rp.get("title", "Information Text")}</b>', styles["h2"]))
            elements.append(_content_box(ai_rp["text"], "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.4 * cm))

            questions = ai_rp.get("questions", [])
            if questions:
                elements.append(Paragraph("<b>COMPREHENSION QUESTIONS</b>", styles["h2"]))
                for qi, q in enumerate(questions, 1):
                    elements.append(Paragraph(f"<b>{qi}.</b> {q}", styles["ex"]))
                    elements.append(Paragraph("_______________________________________________", styles["ex"]))
                elements.append(Spacer(1, 0.3 * cm))
        else:
            info_text = (f"{unit['title']} is an important topic in our world. "
                         f"People around the globe learn about {unit['title'].lower()} every day. "
                         f"This text will help you understand why {unit['title'].lower()} matters.")
            if vocab:
                info_text += f" Key words: {', '.join(vocab[:5])}."
            elements.append(Paragraph("<b>Information Text</b>", styles["h2"]))
            elements.append(_content_box(info_text, "reading", pw, fn, grade))
            elements.append(Spacer(1, 0.3 * cm))

        # Graphic organizer
        elements.append(Paragraph("<b>GRAPHIC ORGANIZER</b>", styles["h2"]))
        elements.append(Paragraph("Complete the chart based on the reading.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        go_rows = [
            ["Main Topic", "Details", "My Opinion"],
            [f"{unit['title']}", "", ""],
            ["Key Facts", "", ""],
            ["New Words", "", ""],
        ]
        elements.append(_data_table(go_rows, [pw * 0.25, pw * 0.4, pw * 0.3],
                                     fn, fb, get_color_hex("green"), grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Summary writing
        elements.append(Paragraph("<b>WRITE A SUMMARY</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write a summary of the reading in your own words (3-5 sentences).", styles["instr"]))
        elements.append(_writing_lines(5, pw))
        elements.append(PageBreak())

        # ═══ PAGE 9-10: Culture Corner ═══
        elements.append(_section_header("CULTURE CORNER", "culture", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        ai_cc = ai.get("culture_corner", {}) if ai else {}
        if ai_cc:
            elements.append(Paragraph(f'<b>{ai_cc.get("title", "Culture Corner")}</b>', styles["h2"]))
            elements.append(_content_box(ai_cc.get("text", ""), "culture", pw, fn, grade))
        else:
            elements.append(Paragraph("<b>Around the World</b>", styles["h2"]))
            elements.append(_content_box(
                f"Different cultures have unique perspectives on {unit['title'].lower()}. "
                f"Understanding these differences helps us become global citizens.",
                "culture", pw, fn, grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Fun Fact
        ff = ai.get("fun_fact", "") if ai else ""
        if ff:
            elements.append(_tip_box("Did You Know?", ff, "fact", pw, fn, fb, grade))
            elements.append(Spacer(1, 0.4 * cm))

        # Discussion
        elements.append(Paragraph("<b>DISCUSSION QUESTIONS</b>", styles["h2"]))
        disc_qs = [
            f"What did you find most interesting about {unit['title'].lower()} in other cultures?",
            "How is this different from your own culture?",
            "What would you like to learn more about?",
            "How can understanding other cultures help you?",
        ]
        for i, q in enumerate(disc_qs, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {q}", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        # Culture comparison chart
        elements.append(KeepTogether([
            Paragraph("<b>CULTURE COMPARISON</b>", styles["h2"]),
            Paragraph("Compare how this topic is viewed in different places.", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))
        cc_rows = [
            ["Aspect", "Turkey", "UK / USA", "Another Country"],
            [f"{unit['title']}", "", "", ""],
            ["Traditions", "", "", ""],
            ["Language", "", "", ""],
        ]
        elements.append(_data_table(cc_rows, [pw * 0.2, pw * 0.24, pw * 0.24, pw * 0.24],
                                     fn, fb, get_color_hex("blue_dark"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 11-13: Extended Reading ═══
        elements.append(_section_header("EXTENDED READING", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Generate a second story/text
        elements.append(Paragraph("<b>READING 3 — EXPLORE MORE</b>", styles["h2"]))
        extended_text = _auto_story(f"more about {unit['title']}", vocab[4:12] if len(vocab) > 4 else vocab, grade)
        elements.append(_content_box(extended_text, "reading", pw, fn, grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Reading skills practice
        elements.append(Paragraph("<b>READING SKILLS PRACTICE</b>", styles["h2"]))

        elements.append(KeepTogether([
            Paragraph("<b>A. Main Idea</b>", styles["instr"]),
            Paragraph("What is the main idea of this text?", styles["ex"]),
            _writing_lines(2, pw),
            Spacer(1, 0.3 * cm),
        ]))

        elements.append(KeepTogether([
            Paragraph("<b>B. Supporting Details</b>", styles["instr"]),
            Paragraph("List 3 details that support the main idea.", styles["ex"]),
            Paragraph("<b>1.</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>2.</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>3.</b> _______________________________________________", styles["ex"]),
            Spacer(1, 0.3 * cm),
        ]))

        elements.append(KeepTogether([
            Paragraph("<b>C. Making Inferences</b>", styles["instr"]),
            Paragraph("What can you infer from the text? Write 2 inferences.", styles["ex"]),
            Paragraph("<b>1.</b> _______________________________________________", styles["ex"]),
            Paragraph("<b>2.</b> _______________________________________________", styles["ex"]),
            Spacer(1, 0.3 * cm),
        ]))

        elements.append(KeepTogether([
            Paragraph("<b>D. Author's Purpose</b>", styles["instr"]),
            Paragraph("Why did the author write this text?", styles["ex"]),
            _writing_lines(2, pw),
            Spacer(1, 0.3 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 14-15: Vocabulary in Context ═══
        elements.append(_section_header("VOCABULARY IN CONTEXT", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>WORDS FROM THE READINGS</b>", styles["h2"]))
        if vocab_defs:
            rows_vc = [["Word", "Definition", "Example from Text"]]
            for vd in vocab_defs[:12]:
                rows_vc.append([vd.get("word", ""), vd.get("definition", ""),
                                vd.get("example", "")])
            elements.append(_data_table(rows_vc, [pw * 0.18, pw * 0.35, pw * 0.4],
                                         fn, fb, get_color_hex("blue"), grade))
        else:
            rows_vc = [["Word", "I think it means...", "Dictionary meaning"]]
            for w in vocab[:10]:
                rows_vc.append([w, "", ""])
            elements.append(_data_table(rows_vc, [pw * 0.2, pw * 0.35, pw * 0.35],
                                         fn, fb, get_color_hex("blue"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Context clues exercise
        elements.append(Paragraph("<b>USING CONTEXT CLUES</b>", styles["h2"]))
        elements.append(Paragraph(
            "Read each sentence. Guess the meaning of the underlined word from the context.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph(
                "   I think it means: _______________________________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 16-17: Creative Reading Response ═══
        elements.append(_section_header("CREATIVE RESPONSE", "writing", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Book review style
        elements.append(Paragraph("<b>MY READING JOURNAL</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        journal_rows = [
            ["Question", "My Answer"],
            ["What did I read about?", ""],
            ["What was the most interesting part?", ""],
            ["What new words did I learn?", ""],
            ["How do I feel about this topic?", ""],
            ["What questions do I still have?", ""],
        ]
        elements.append(_data_table(journal_rows, [pw * 0.35, pw * 0.6],
                                     fn, fb, get_color_hex("teal"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Reader response
        elements.append(Paragraph("<b>MY RESPONSE</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write a response to one of the readings. Share your thoughts, feelings, "
            "and opinions.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(10, pw))
        elements.append(PageBreak())

        # ═══ PAGE 18-19: Poetry & Song ═══
        elements.append(_section_header("POETRY & SONG", "listening", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Song/Chant
        song = ai.get("song_chant", {}) if ai else {}
        if song:
            elements.append(Paragraph(f'<b>{song.get("title", "Song")}</b>', styles["h2"]))
            for lyric_line in song.get("lyrics", "").split("\n"):
                if lyric_line.strip():
                    elements.append(Paragraph(f"\u266B {lyric_line.strip()}", styles["song"]))
        else:
            elements.append(Paragraph("<b>A Poem</b>", styles["h2"]))
            elements.append(Paragraph(f"\u266B Learning about {unit['title']}...", styles["song"]))
            elements.append(Paragraph("\u266B Every word, every day...", styles["song"]))
            elements.append(Paragraph("\u266B Growing stronger along the way...", styles["song"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Write your own poem
        elements.append(Paragraph("<b>WRITE YOUR OWN POEM</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write a poem about {unit['title'].lower()} (at least 4 lines).", styles["instr"]))
        elements.append(_writing_lines(6, pw))
        elements.append(Spacer(1, 0.4 * cm))

        # Illustration space
        elements.append(Paragraph("<b>ILLUSTRATE YOUR POEM</b>", styles["h2"]))
        illus_box = Table([[""]], colWidths=[pw], rowHeights=[6 * cm])
        illus_box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ]))
        elements.append(illus_box)
        elements.append(PageBreak())

        # ═══ EXTRA: Reading & Writing Connection ═══
        elements.append(_section_header("READING & WRITING CONNECTION", "writing", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>BOOK REVIEW</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write a review of the readings in this unit.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        review_rows = [
            ["Question", "My Answer"],
            ["Title of my favorite reading", ""],
            ["What was it about?", ""],
            ["Did I like it? Why?", ""],
            ["Would I recommend it?", ""],
            ["Rating (1-5 stars)", ""],
        ]
        elements.append(_data_table(review_rows, [pw * 0.35, pw * 0.55],
                                     fn, fb, get_color_hex("teal"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>WRITE AN ALTERNATIVE ENDING</b>", styles["h2"]))
        elements.append(Paragraph(
            "Choose one of the stories from this unit. Write a different ending.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Story title:</b> ___________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>My new ending:</b>", styles["instr"]))
        elements.append(_writing_lines(8, pw))
        elements.append(PageBreak())

        # ═══ EXTRA: Extensive Reading ═══
        elements.append(_section_header("EXTENSIVE READING", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>READING 4 — EXTRA TEXT</b>", styles["h2"]))
        extra_text = _auto_story(f"discovering {unit['title']}", vocab[6:14] if len(vocab) > 6 else vocab, grade)
        elements.append(_content_box(extra_text, "reading", pw, fn, grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>SKIMMING & SCANNING</b>", styles["h2"]))
        elements.append(Paragraph("<b>A. Skimming:</b> Read quickly and answer:", styles["instr"]))
        elements.append(Paragraph("What is the text about? _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>B. Scanning:</b> Find specific information:", styles["instr"]))
        elements.append(Paragraph(f"<b>1.</b> Find a word that means the same as '{vocab[0] if vocab else 'learn'}': __________", styles["ex"]))
        elements.append(Paragraph("<b>2.</b> How many sentences are in the text? __________", styles["ex"]))
        elements.append(Paragraph("<b>3.</b> What is the last word of the text? __________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>READING LOG</b>", styles["h2"]))
        log_rows = [
            ["Date", "What I Read", "Pages", "New Words", "Rating"],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
        ]
        elements.append(_data_table(log_rows, [pw * 0.15, pw * 0.3, pw * 0.1, pw * 0.25, pw * 0.12],
                                     fn, fb, get_color_hex("green"), grade))
        elements.append(PageBreak())

        # ═══ EXTRA: Retelling & Dramatization ═══
        elements.append(_section_header("RETELLING & DRAMA", "speaking", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>STORY RETELLING</b>", styles["h2"]))
        elements.append(Paragraph(
            "Retell one of the stories from this unit in your own words. "
            "Use the chart below to organize your ideas.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        retell_rows = [
            ["Part", "What Happened"],
            ["Beginning", ""],
            ["Middle", ""],
            ["End", ""],
            ["Characters", ""],
            ["Setting", ""],
            ["My opinion", ""],
        ]
        elements.append(_data_table(retell_rows, [pw * 0.2, pw * 0.7],
                                     fn, fb, get_color_hex("purple"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>READER'S THEATRE</b>", styles["h2"]))
        elements.append(Paragraph(
            "Choose a dialogue or story from this unit. Turn it into a script "
            "and perform it with your classmates.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Characters:</b> ___________________________", styles["ex"]))
        elements.append(Paragraph("<b>Scene:</b> ___________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Script:</b>", styles["instr"]))
        elements.append(_writing_lines(8, pw))
        elements.append(PageBreak())

        # ═══ EXTRA: Comprehension Strategies ═══
        elements.append(_section_header("READING STRATEGIES", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>BEFORE, DURING & AFTER READING</b>", styles["h2"]))
        strat_rows = [
            ["Stage", "Strategy", "My Notes"],
            ["Before Reading", "Look at the title and pictures", ""],
            ["Before Reading", "Think about what I already know", ""],
            ["During Reading", "Underline new words", ""],
            ["During Reading", "Ask myself questions", ""],
            ["After Reading", "Summarize in my own words", ""],
            ["After Reading", "Share my opinion with a friend", ""],
        ]
        elements.append(_data_table(strat_rows, [pw * 0.2, pw * 0.38, pw * 0.34],
                                     fn, fb, get_color_hex("blue"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>TEXT CONNECTIONS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Connect the readings to your life, other texts, and the world.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        conn_rows = [
            ["Connection Type", "My Connection"],
            ["Text-to-Self: How does this relate to MY life?", ""],
            ["Text-to-Text: Does this remind me of another story?", ""],
            ["Text-to-World: How does this connect to the real world?", ""],
        ]
        elements.append(_data_table(conn_rows, [pw * 0.45, pw * 0.45],
                                     fn, fb, get_color_hex("blue_dark"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>VOCABULARY FROM READINGS</b>", styles["h2"]))
        elements.append(Paragraph("Write 5 new words you learned from the readings.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        vfr_rows = [["Word", "Sentence from Text", "My Own Sentence"]]
        for i in range(5):
            vfr_rows.append(["", "", ""])
        elements.append(_data_table(vfr_rows, [pw * 0.2, pw * 0.35, pw * 0.35],
                                     fn, fb, get_color_hex("green"), grade))
        elements.append(PageBreak())

        # ═══ EXTRA: Listening Comprehension ═══
        elements.append(_section_header("LISTENING COMPREHENSION", "listening", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>LISTEN AND COMPLETE</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Listen to your teacher read a text about {unit['title'].lower()}. "
            "Complete the notes below.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        listen_rows = [
            ["Topic", ""],
            ["Main idea", ""],
            ["Key details (3)", "1.\n2.\n3."],
            ["New words I heard", ""],
            ["My opinion", ""],
        ]
        listen_t = [["Note", "My Answer"]] + listen_rows
        elements.append(_data_table(listen_t, [pw * 0.3, pw * 0.6],
                                     fn, fb, get_color_hex("orange"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>DICTATION PRACTICE</b>", styles["h2"]))
        elements.append(Paragraph(
            "Listen and write the sentences you hear.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(8, pw))
        elements.append(PageBreak())

        # ═══ EXTRA: Reading Fluency ═══
        elements.append(_section_header("READING FLUENCY", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>TIMED READING</b>", styles["h2"]))
        elements.append(Paragraph(
            "Read the text below as quickly and accurately as you can. "
            "Your teacher will time you.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        fluency_text = _auto_story(f"learning about {unit['title']}", vocab[:8], grade)
        elements.append(_content_box(fluency_text, "reading", pw, fn, grade))
        elements.append(Spacer(1, 0.3 * cm))

        fluency_rows = [
            ["Attempt", "Time", "Errors", "Words Per Minute"],
            ["1st reading", "", "", ""],
            ["2nd reading", "", "", ""],
            ["3rd reading", "", "", ""],
        ]
        elements.append(_data_table(fluency_rows, [pw * 0.2, pw * 0.2, pw * 0.2, pw * 0.3],
                                     fn, fb, get_color_hex("green"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>READING ALOUD SELF-CHECK</b>", styles["h2"]))
        elements.append(Paragraph("\u2610 I read clearly and loudly.", styles["body"]))
        elements.append(Paragraph("\u2610 I pronounced all words correctly.", styles["body"]))
        elements.append(Paragraph("\u2610 I paused at commas and full stops.", styles["body"]))
        elements.append(Paragraph("\u2610 I used the right intonation for questions.", styles["body"]))
        elements.append(Paragraph("\u2610 My reading speed improved.", styles["body"]))
        elements.append(PageBreak())

        # ═══ EXTRA: Genre Study ═══
        elements.append(_section_header("GENRE STUDY", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>TYPES OF TEXTS</b>", styles["h2"]))
        elements.append(Paragraph(
            "In this unit you read different types of texts. Compare them.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        genre_rows = [
            ["Feature", "Story", "Information Text", "Dialogue"],
            ["Purpose", "", "", ""],
            ["Structure", "", "", ""],
            ["Language style", "", "", ""],
            ["I liked it?", "\u2610", "\u2610", "\u2610"],
        ]
        elements.append(_data_table(genre_rows, [pw * 0.2, pw * 0.24, pw * 0.24, pw * 0.24],
                                     fn, fb, get_color_hex("purple"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>WRITE YOUR OWN TEXT</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Choose a genre (story, report, letter, diary) and write about {unit['title'].lower()}.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("<b>Genre:</b> ___________________________", styles["ex"]))
        elements.append(Paragraph("<b>Title:</b> ___________________________", styles["ex"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(10, pw))
        elements.append(PageBreak())

        # ═══ EXTRA: Reading Test ═══
        elements.append(_section_header("READING TEST", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — READING TEST</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        elements.append(Paragraph("<b>Part A: Vocabulary in Context (10 points)</b>", styles["h2"]))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Part B: Comprehension (10 points)</b>", styles["h2"]))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
            elements.append(Paragraph("_______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Part C: Summary Writing (10 points)</b>", styles["h2"]))
        elements.append(Paragraph("Write a summary of your favorite reading.", styles["instr"]))
        elements.append(_writing_lines(6, pw))
        elements.append(Spacer(1, 0.3 * cm))

        score_r = [
            ["Part", "Points", "My Score"],
            ["A: Vocabulary", "10", ""],
            ["B: Comprehension", "10", ""],
            ["C: Summary", "10", ""],
            ["TOTAL", "30", ""],
        ]
        elements.append(_data_table(score_r, [pw * 0.35, pw * 0.2, pw * 0.2],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(PageBreak())

        # ═══ Unit Review ═══
        elements.append(_section_header("READING REVIEW", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — READING ASSESSMENT</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        # Reading skills assessment
        sa_rows = [["Reading Skill", "Excellent", "Good", "Needs Work"]]
        reading_skills = [
            "I can understand the main idea",
            "I can find details in the text",
            "I can make inferences",
            "I can use context clues for new words",
            "I can summarize what I read",
            "I can compare texts and cultures",
            "I can express my opinion about readings",
        ]
        for skill in reading_skills:
            sa_rows.append([skill, "\u2610", "\u2610", "\u2610"])
        elements.append(_data_table(sa_rows, [pw * 0.4, pw * 0.16, pw * 0.16, pw * 0.2],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Favorite reading
        elements.append(Paragraph("<b>MY FAVORITE READING</b>", styles["h2"]))
        elements.append(Paragraph("Which reading did you like best? Why?", styles["body"]))
        elements.append(_writing_lines(3, pw))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph("What will you read next about this topic?", styles["body"]))
        elements.append(_writing_lines(2, pw))
        elements.append(PageBreak())

    _back_cover(elements, styles, accent, grade, fn, fb)

    tmpl.build(elements)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTION 4: VOCABULARY BOOK — ~20 pages per unit
# ═══════════════════════════════════════════════════════════════════════════════

def generate_vocabulary_book_pdf(grade: int, curriculum_weeks: list[dict]) -> bytes | None:
    """Generate premium Vocabulary Book PDF — ~20 pages per unit."""
    if not curriculum_weeks:
        return None
    fn, fb = ensure_turkish_pdf_fonts()
    accent, bg_hex = GRADE_COLORS.get(grade, ("#3B82F6", "#EFF6FF"))
    units = _group_units(curriculum_weeks)
    book_name = BOOK_TITLES.get(grade, BOOK_TITLES[5])["vocab"]
    styles = _make_styles(fn, fb, grade, accent)
    young = _is_young(grade)
    pw = _PW
    rng = random.Random(99 + grade)

    from views.book_content_ai import _load_cache

    buf = io.BytesIO()
    tmpl = _BookTemplate(buf, grade, book_name, fn, fb, accent)

    elements: list = []

    _premium_cover(elements, book_name, grade, "Kelime Kitab\u0131 / Vocabulary Book",
                   styles, accent, fn, fb, units)
    _premium_toc(elements, units, styles, grade, fn, fb, accent)

    for unit in units:
        vocab = _collect_vocab(unit["weeks"])
        skills = _collect_skills(unit["weeks"])
        tmpl.set_current_unit(f"Unit {unit['num']}: {unit['title']}")

        ai = _load_cache(grade, unit["num"])
        ai_vocab = ai.get("vocabulary_enrichment", {}) if ai else {}
        ai_defs = ai_vocab.get("definitions", [])
        ai_families = ai_vocab.get("word_families", [])

        # ═══ PAGE 1: Unit Opener ═══
        _premium_unit_opener(elements, unit, styles, grade, fn, fb, accent, vocab, skills)

        # ═══ PAGE 2-4: Word List (detailed) ═══
        elements.append(_section_header("WORD LIST", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        if ai_defs:
            # Detailed word cards - 4 per page approx
            for idx, vd in enumerate(ai_defs):
                word = vd.get("word", "")
                defn = vd.get("definition", "")
                example = vd.get("example", "")
                turkish = vd.get("turkish_hint", "")

                card_data = [
                    [Paragraph(f'<b>{idx + 1}. {word}</b>', styles["h3"]),
                     Paragraph(f'<i>Türkçe: {turkish}</i>' if turkish else "", styles["caption"])],
                    [Paragraph(f'<b>Definition:</b> {defn}', styles["body"]),
                     ""],
                    [Paragraph(f'<b>Example:</b> <i>{example}</i>', styles["body"]),
                     ""],
                    [Paragraph('<b>My sentence:</b> ___________________________', styles["body"]),
                     ""],
                ]
                card = Table(card_data, colWidths=[pw * 0.7, pw * 0.25])
                card.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 0.5, _hex("#e2e8f0")),
                    ("BACKGROUND", (0, 0), (-1, -1), _hex("#f8fafc")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("ROUNDEDCORNERS", [6, 6, 6, 6]),
                    ("SPAN", (0, 1), (-1, 1)),
                    ("SPAN", (0, 2), (-1, 2)),
                    ("SPAN", (0, 3), (-1, 3)),
                ]))
                elements.append(KeepTogether([card, Spacer(1, 0.3 * cm)]))

                # Page break every 5 words
                if (idx + 1) % 5 == 0 and idx + 1 < len(ai_defs):
                    elements.append(CondPageBreak(4 * cm))
        else:
            rows_v = [["#", "English", "Pronunciation", "Turkish", "My Sentence"]]
            for idx, w in enumerate(vocab, 1):
                rows_v.append([str(idx), w, f"/{w.lower()}/", "___________", ""])
            elements.append(_data_table(
                rows_v, [pw * 0.06, pw * 0.2, pw * 0.2, pw * 0.2, pw * 0.28],
                fn, fb, accent, grade))
        elements.append(PageBreak())

        # ═══ PAGE 5-6: Word Families ═══
        elements.append(_section_header("WORD FAMILIES", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        if ai_families:
            elements.append(Paragraph(
                "Words belong to families. Learning word families helps you understand "
                "and use more words.", styles["body"]))
            elements.append(Spacer(1, 0.3 * cm))

            rows_f = [["Base Word", "Noun Form", "Verb Form", "Adjective Form"]]
            for wf in ai_families:
                rows_f.append([
                    wf.get("base", ""),
                    wf.get("noun", "—"),
                    wf.get("verb", "—"),
                    wf.get("adjective", "—"),
                ])
            elements.append(_data_table(
                rows_f, [pw * 0.22, pw * 0.24, pw * 0.24, pw * 0.24],
                fn, fb, get_color_hex("blue_dark"), grade))
            elements.append(Spacer(1, 0.4 * cm))

            # Word family exercise
            elements.append(Paragraph("<b>PRACTICE: Complete with the correct form.</b>", styles["h2"]))
            for i, wf in enumerate(ai_families[:5], 1):
                base = wf.get("base", "word")
                elements.append(Paragraph(
                    f"<b>{i}.</b> ({base}) The __________ was very __________. She can __________ well.",
                    styles["ex"]))
            elements.append(Spacer(1, 0.3 * cm))
        else:
            elements.append(Paragraph(
                "Group these words into categories:", styles["body"]))
            elements.append(Spacer(1, 0.2 * cm))
            cat_rows = [["Nouns", "Verbs", "Adjectives", "Other"]]
            cat_rows.append(["", "", "", ""])
            cat_rows.append(["", "", "", ""])
            cat_rows.append(["", "", "", ""])
            elements.append(_data_table(cat_rows, [pw * 0.22] * 4, fn, fb, accent, grade))

        # Synonyms and antonyms
        elements.append(KeepTogether([
            Paragraph("<b>SYNONYMS & ANTONYMS</b>", styles["h2"]),
            Paragraph("Write a synonym (similar word) and antonym (opposite word) for each.", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))
        sa_rows = [["Word", "Synonym", "Antonym"]]
        for w in vocab[:8]:
            sa_rows.append([w, "", ""])
        elements.append(_data_table(sa_rows, [pw * 0.25, pw * 0.3, pw * 0.3],
                                     fn, fb, get_color_hex("purple"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 7-8: Example Sentences + Usage ═══
        elements.append(_section_header("WORDS IN ACTION", "reading", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>EXAMPLE SENTENCES</b>", styles["h2"]))
        if ai_defs:
            for vd in ai_defs[:12]:
                ex = vd.get("example", "")
                word = vd.get("word", "")
                if ex:
                    elements.append(Paragraph(
                        f"\u2022 <b>{word}:</b> <i>{ex}</i>", styles["body"]))
        else:
            for w in vocab[:10]:
                elements.append(Paragraph(
                    f"\u2022 <b>{w}:</b> I like {w}.", styles["body"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Collocations
        elements.append(Paragraph("<b>COMMON COLLOCATIONS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Some words go together naturally. Match the words that go together.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        coll_rows = [["Word", "Goes with...", "Example"]]
        for w in vocab[:6]:
            coll_rows.append([w, "___________", ""])
        elements.append(_data_table(coll_rows, [pw * 0.2, pw * 0.25, pw * 0.45],
                                     fn, fb, get_color_hex("green"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Mini-dialogue with vocabulary
        elements.append(KeepTogether([
            Paragraph("<b>VOCABULARY IN CONVERSATION</b>", styles["h2"]),
            Paragraph("Complete the dialogue using words from this unit.", styles["instr"]),
            Spacer(1, 0.2 * cm),
            Paragraph("<b>A:</b> Hi! What did you learn about __________ today?", styles["ex"]),
            Paragraph("<b>B:</b> I learned that __________ is really interesting!", styles["ex"]),
            Paragraph("<b>A:</b> That's great! Can you use __________ in a sentence?", styles["ex"]),
            Paragraph("<b>B:</b> Sure! __________________________________________", styles["ex"]),
            Spacer(1, 0.3 * cm),
        ]))
        elements.append(PageBreak())

        # ═══ PAGE 9-11: Word Puzzles ═══
        elements.append(_section_header("WORD PUZZLES", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Crossword clues
        elements.append(Paragraph("<b>CROSSWORD CLUES</b>", styles["h2"]))
        clue_words = ai_defs if ai_defs else [
            {"word": w, "definition": f"Related to {unit['title'].lower()}"} for w in vocab]

        elements.append(Paragraph("<b>Across:</b>", styles["instr"]))
        for i, cw in enumerate(clue_words[:5], 1):
            word = cw.get("word", "")
            defn = cw.get("definition", "")
            blanks = word[0] + " _" * (len(word) - 1)
            elements.append(Paragraph(f"<b>{i}.</b> {defn}  ({blanks})", styles["ex"]))

        if len(clue_words) > 5:
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(Paragraph("<b>Down:</b>", styles["instr"]))
            for i, cw in enumerate(clue_words[5:10], 1):
                word = cw.get("word", "")
                defn = cw.get("definition", "")
                blanks = word[0] + " _" * (len(word) - 1)
                elements.append(Paragraph(f"<b>{i}.</b> {defn}  ({blanks})", styles["ex"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Word search
        elements.append(Paragraph("<b>WORD SEARCH</b>", styles["h2"]))
        ws_words = vocab[:8]
        elements.append(Paragraph(f"Find: <b>{', '.join(ws_words)}</b>", styles["body_c"]))
        elements.append(Spacer(1, 0.2 * cm))

        grid_size = 10
        grid: list[list[str]] = []
        for r in range(grid_size):
            row = [chr(rng.randint(65, 90)) for _ in range(grid_size)]
            if r < len(ws_words):
                word = ws_words[r].upper()[:grid_size]
                start = rng.randint(0, max(0, grid_size - len(word)))
                for ci, ch in enumerate(word):
                    if start + ci < grid_size:
                        row[start + ci] = ch
            grid.append(row)

        cell_sz = min(1.1 * cm, pw / (grid_size + 1))
        ws_table = Table(grid, colWidths=[cell_sz] * grid_size, rowHeights=[cell_sz] * grid_size)
        ws_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, _hex("#cbd5e1")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), fb),
            ("FONTSIZE", (0, 0), (-1, -1), round(10 * get_tier_for_grade(grade)["font_scale"], 0)),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#f8fafc")),
        ]))
        elements.append(ws_table)
        elements.append(Spacer(1, 0.4 * cm))

        # Unscramble
        elements.append(Paragraph("<b>UNSCRAMBLE</b>", styles["h2"]))
        for i, w in enumerate(vocab[:8], 1):
            chars = list(w.upper())
            rng.shuffle(chars)
            elements.append(Paragraph(
                f"<b>{i}.</b> {' '.join(chars)}  \u2192  _______________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ PAGE 12-13: Categorization & Mind Map ═══
        elements.append(_section_header("ORGANIZE YOUR WORDS", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Categorize
        elements.append(Paragraph("<b>CATEGORIZE THE WORDS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Put each word from this unit into the correct category.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        cat_rows2 = [["Nouns\n(things)", "Verbs\n(actions)", "Adjectives\n(describing)", "Other"]]
        for _ in range(5):
            cat_rows2.append(["", "", "", ""])
        elements.append(_data_table(cat_rows2, [pw * 0.22] * 4, fn, fb,
                                     get_color_hex("purple"), grade))
        elements.append(Spacer(1, 0.5 * cm))

        # Mind map template
        elements.append(Paragraph("<b>MIND MAP</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Create a mind map about <b>{unit['title']}</b>. Write the topic in the center "
            "and add related words around it.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))

        mind_box = Table([[""]], colWidths=[pw], rowHeights=[10 * cm])
        mind_box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ]))
        elements.append(mind_box)
        elements.append(PageBreak())

        # ═══ PAGE 14-15: Writing with Vocabulary ═══
        elements.append(_section_header("WRITING WITH VOCABULARY", "writing", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Sentence completion
        elements.append(Paragraph("<b>A. COMPLETE THE SENTENCES</b>", styles["h2"]))
        for i, w in enumerate(vocab[:8], 1):
            elements.append(Paragraph(
                f"<b>{i}.</b> ({w}) _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        # Short paragraph
        elements.append(Paragraph("<b>B. WRITE A SHORT PARAGRAPH</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write a paragraph (5-7 sentences) about {unit['title'].lower()} using "
            "at least 6 vocabulary words from this unit. Underline the vocabulary words.",
            styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(8, pw))
        elements.append(Spacer(1, 0.3 * cm))

        # Word count tracker
        elements.append(KeepTogether([
            Paragraph("<b>VOCABULARY TRACKER</b>", styles["h2"]),
            Paragraph("Check off each word you used in your paragraph:", styles["body"]),
            Spacer(1, 0.2 * cm),
        ]))
        check_text = "  ".join(f"\u2610 {w}" for w in vocab[:12])
        elements.append(Paragraph(check_text, styles["body"]))
        elements.append(PageBreak())

        # ═══ PAGE 16-17: Games & Activities ═══
        elements.append(_section_header("VOCABULARY GAMES", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        # Bingo card
        elements.append(Paragraph("<b>VOCABULARY BINGO</b>", styles["h2"]))
        elements.append(Paragraph(
            "Fill in the bingo card with words from this unit. Cross out words as your "
            "teacher calls them.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))

        bingo_size = 4
        bingo_data: list[list[str]] = []
        bingo_words = vocab[:bingo_size * bingo_size]
        rng.shuffle(bingo_words)
        for r in range(bingo_size):
            row = []
            for c in range(bingo_size):
                idx = r * bingo_size + c
                row.append(bingo_words[idx] if idx < len(bingo_words) else "")
            bingo_data.append(row)

        bingo_cell = pw / (bingo_size + 0.5)
        bt = Table(bingo_data, colWidths=[bingo_cell] * bingo_size,
                   rowHeights=[bingo_cell * 0.6] * bingo_size)
        bt.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, _hex(accent)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), fn),
            ("FONTSIZE", (0, 0), (-1, -1), round(9 * get_tier_for_grade(grade)["font_scale"], 0)),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#f8fafc")),
        ]))
        elements.append(bt)
        elements.append(Spacer(1, 0.5 * cm))

        # Memory game cards
        elements.append(Paragraph("<b>MEMORY GAME</b>", styles["h2"]))
        elements.append(Paragraph(
            "Cut out these cards. Match each word with its definition.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))

        mem_rows = [["Word Card", "Definition Card"]]
        for w in vocab[:8]:
            defn = ""
            for vd in ai_defs:
                if vd.get("word", "").lower() == w.lower():
                    defn = vd.get("definition", "")
                    break
            mem_rows.append([w, defn or f"About {unit['title'].lower()}"])
        elements.append(_data_table(mem_rows, [pw * 0.4, pw * 0.5], fn, fb,
                                     get_color_hex("gold"), grade))
        elements.append(PageBreak())

        # ═══ PAGE 18-19: My Words + Dictionary ═══
        elements.append(_section_header("MY PERSONAL DICTIONARY", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>MY WORDS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Add your own words related to this unit.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))

        my_rows = [["#", "My Word", "Meaning", "Example Sentence", "Drawing"]]
        for i in range(1, 11):
            my_rows.append([str(i), "", "", "", ""])
        elements.append(_data_table(
            my_rows, [pw * 0.06, pw * 0.17, pw * 0.25, pw * 0.3, pw * 0.15],
            fn, fb, accent, grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Word challenge
        elements.append(Paragraph("<b>WORD CHALLENGE</b>", styles["h2"]))
        elements.append(_tip_box("Challenge",
                                  f"Can you use all {min(len(vocab), 10)} vocabulary words in one story? "
                                  "Write a short story using as many unit words as possible!",
                                  "warning", pw, fn, fb, grade))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(8, pw))
        elements.append(PageBreak())

        # ═══ EXTRA: Spelling & Dictation ═══
        elements.append(_section_header("SPELLING WORKSHOP", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>SPELLING TEST</b>", styles["h2"]))
        elements.append(Paragraph(
            "Listen to your teacher and write the words correctly.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        spell_rows2 = [["#", "Word", "Correct?", "#", "Word", "Correct?"]]
        for i in range(1, 9):
            j = i + 8
            spell_rows2.append([str(i), "", "\u2610", str(j), "", "\u2610"])
        elements.append(_data_table(spell_rows2,
                                     [pw * 0.05, pw * 0.25, pw * 0.1, pw * 0.05, pw * 0.25, pw * 0.1],
                                     fn, fb, get_color_hex("purple"), grade))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(f"<b>Score:</b> _____ / 16", styles["body_c"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>LOOK, COVER, WRITE, CHECK</b>", styles["h2"]))
        elements.append(Paragraph(
            "Look at the word, cover it, write it from memory, then check.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        lcwc_rows = [["Word", "1st Try", "2nd Try", "3rd Try"]]
        for w in vocab[:10]:
            lcwc_rows.append([w, "", "", ""])
        elements.append(_data_table(lcwc_rows, [pw * 0.22, pw * 0.22, pw * 0.22, pw * 0.22],
                                     fn, fb, get_color_hex("blue"), grade))
        elements.append(PageBreak())

        # ═══ EXTRA: Word Associations & Idioms ═══
        elements.append(_section_header("WORD ASSOCIATIONS", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>WORD ASSOCIATIONS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write the first 3 words that come to mind for each vocabulary word.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        assoc_rows = [["Vocabulary Word", "Word 1", "Word 2", "Word 3"]]
        for w in vocab[:8]:
            assoc_rows.append([w, "", "", ""])
        elements.append(_data_table(assoc_rows, [pw * 0.25, pw * 0.22, pw * 0.22, pw * 0.22],
                                     fn, fb, get_color_hex("orange"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>WORD IN DIFFERENT CONTEXTS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Use each word in 3 different sentences (formal, informal, question).", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for w in vocab[:4]:
            elements.append(Paragraph(f"<b>{w}:</b>", styles["h3"]))
            elements.append(Paragraph("Formal: _______________________________________________", styles["ex"]))
            elements.append(Paragraph("Informal: _______________________________________________", styles["ex"]))
            elements.append(Paragraph("Question: _______________________________________________", styles["ex"]))
            elements.append(Spacer(1, 0.2 * cm))
        elements.append(PageBreak())

        # ═══ EXTRA: Picture Dictionary ═══
        elements.append(_section_header("PICTURE DICTIONARY", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>DRAW & LABEL</b>", styles["h2"]))
        elements.append(Paragraph(
            "Draw a picture for each word and write its meaning.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))

        # 2x3 grid of drawing boxes
        for row_idx in range(3):
            box_data = []
            label_data = []
            for col_idx in range(2):
                w_idx = row_idx * 2 + col_idx
                w = vocab[w_idx] if w_idx < len(vocab) else ""
                box_data.append("")
                label_data.append(Paragraph(f"<b>{w}</b>", ParagraphStyle(
                    "picl", fontName=fb, fontSize=9, leading=12, alignment=TA_CENTER,
                    textColor=_hex("#1e293b"))))
            pic_grid = Table([box_data, label_data],
                             colWidths=[pw * 0.45, pw * 0.45],
                             rowHeights=[3.5 * cm, 0.8 * cm])
            pic_grid.setStyle(TableStyle([
                ("BOX", (0, 0), (0, 0), 0.5, _hex("#cbd5e1")),
                ("BOX", (1, 0), (1, 0), 0.5, _hex("#cbd5e1")),
                ("BACKGROUND", (0, 0), (-1, 0), _hex("#fafafa")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(pic_grid)
            elements.append(Spacer(1, 0.2 * cm))
        elements.append(PageBreak())

        # ═══ EXTRA: Word Detective ═══
        elements.append(_section_header("WORD DETECTIVE", "vocabulary", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>FIND THE HIDDEN WORDS</b>", styles["h2"]))
        elements.append(Paragraph(
            "Each sentence contains a hidden vocabulary word. Circle it!", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i, w in enumerate(vocab[:8], 1):
            # Create a sentence with the word hidden in it
            elements.append(Paragraph(
                f"<b>{i}.</b> Can you find the word in this sentence about {unit['title'].lower()}? "
                f"Hint: it has {len(w)} letters.", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>WORD DETECTIVE CHALLENGE</b>", styles["h2"]))
        elements.append(Paragraph(
            "Use the clues to find the mystery words from this unit.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        det_rows = [["#", "Clue", "Letters", "Mystery Word"]]
        for i, w in enumerate(vocab[:8], 1):
            hint = f"{len(w)} letters, starts with '{w[0].upper()}'"
            det_rows.append([str(i), f"Related to {unit['title'].lower()}", hint, ""])
        elements.append(_data_table(det_rows, [pw * 0.06, pw * 0.35, pw * 0.28, pw * 0.23],
                                     fn, fb, get_color_hex("purple"), grade))
        elements.append(PageBreak())

        # ═══ EXTRA: Vocabulary in Real Life ═══
        elements.append(_section_header("VOCABULARY IN REAL LIFE", "speaking", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>WHERE DO YOU SEE THESE WORDS?</b>", styles["h2"]))
        elements.append(Paragraph(
            "Think about where you might see or hear these words in real life.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        real_rows = [["Word", "At school", "At home", "On TV/Internet", "In books"]]
        for w in vocab[:8]:
            real_rows.append([w, "\u2610", "\u2610", "\u2610", "\u2610"])
        elements.append(_data_table(real_rows, [pw * 0.2, pw * 0.17, pw * 0.17, pw * 0.2, pw * 0.17],
                                     fn, fb, get_color_hex("teal"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>MY VOCABULARY DIARY</b>", styles["h2"]))
        elements.append(Paragraph(
            "Write down every time you use a unit word outside class this week.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        diary_rows = [["Day", "Word I Used", "Situation", "Who I Talked To"]]
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            diary_rows.append([day, "", "", ""])
        elements.append(_data_table(diary_rows, [pw * 0.18, pw * 0.22, pw * 0.32, pw * 0.2],
                                     fn, fb, get_color_hex("gold"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>TEACH A FRIEND</b>", styles["h2"]))
        elements.append(Paragraph(
            "Choose 5 words and teach them to someone who doesn't know them. "
            "Write how you explained each word.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        for i, w in enumerate(vocab[:5], 1):
            elements.append(Paragraph(f"<b>{i}. {w}:</b> I explained it by saying ___________________________", styles["ex"]))
        elements.append(PageBreak())

        # ═══ EXTRA: Word Art & Creative ═══
        elements.append(_section_header("WORD ART & CREATIVITY", "project", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>WORD ART</b>", styles["h2"]))
        elements.append(Paragraph(
            "Choose your 3 favorite words from this unit. Write them in creative, "
            "artistic styles (big, colorful, decorated).", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        art_box = Table([[""]], colWidths=[pw], rowHeights=[7 * cm])
        art_box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ]))
        elements.append(art_box)
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>ACROSTIC POEM</b>", styles["h2"]))
        elements.append(Paragraph(
            f"Write an acrostic poem using the word <b>{unit['title'].upper()[:8]}</b>. "
            "Each line starts with a letter of the word.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        word_for_acrostic = unit['title'].upper()[:8]
        for ch in word_for_acrostic:
            elements.append(Paragraph(f"<b>{ch}</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph("<b>VOCABULARY COMIC STRIP</b>", styles["h2"]))
        elements.append(Paragraph(
            "Draw a 4-panel comic strip using at least 4 vocabulary words.", styles["instr"]))
        elements.append(Spacer(1, 0.2 * cm))
        comic_data = [["Panel 1", "Panel 2"], ["Panel 3", "Panel 4"]]
        comic_t = Table(comic_data, colWidths=[pw * 0.45, pw * 0.45],
                        rowHeights=[4 * cm, 4 * cm])
        comic_t.setStyle(TableStyle([
            ("BOX", (0, 0), (0, 0), 0.5, _hex("#cbd5e1")),
            ("BOX", (1, 0), (1, 0), 0.5, _hex("#cbd5e1")),
            ("BOX", (0, 1), (0, 1), 0.5, _hex("#cbd5e1")),
            ("BOX", (1, 1), (1, 1), 0.5, _hex("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), _hex("#fafafa")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, -1), fb),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (0, 0), (-1, -1), _hex("#94A3B8")),
        ]))
        elements.append(comic_t)
        elements.append(PageBreak())

        # ═══ EXTRA: Vocabulary Test ═══
        elements.append(_section_header("VOCABULARY TEST", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — VOCABULARY TEST</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        elements.append(Paragraph("<b>Part A: Definitions (10 points)</b>", styles["h2"]))
        elements.append(Paragraph("Write the word for each definition.", styles["instr"]))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________ : _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Part B: Fill in the Blanks (10 points)</b>", styles["h2"]))
        elements.append(Paragraph("Complete each sentence with a word from this unit.", styles["instr"]))
        for i in range(1, 6):
            elements.append(Paragraph(
                f"<b>{i}.</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph("<b>Part C: Use in Sentences (10 points)</b>", styles["h2"]))
        elements.append(Paragraph("Write a sentence using each word.", styles["instr"]))
        for w in vocab[:5]:
            elements.append(Paragraph(
                f"<b>{w}:</b> _______________________________________________", styles["ex"]))
        elements.append(Spacer(1, 0.3 * cm))

        score_v = [
            ["Part", "Points", "My Score"],
            ["A: Definitions", "10", ""],
            ["B: Fill in Blanks", "10", ""],
            ["C: Sentences", "10", ""],
            ["TOTAL", "30", ""],
        ]
        elements.append(_data_table(score_v, [pw * 0.35, pw * 0.2, pw * 0.2],
                                     fn, fb, get_color_hex("red"), grade))
        elements.append(PageBreak())

        # ═══ Self-Assessment ═══
        elements.append(_section_header("VOCABULARY REVIEW", "review", pw, fb, grade))
        elements.append(Spacer(1, 0.3 * cm))

        elements.append(Paragraph(f"<b>UNIT {unit['num']} — VOCABULARY ASSESSMENT</b>", styles["h2"]))
        elements.append(Spacer(1, 0.2 * cm))

        # Know / Don't know chart
        elements.append(Paragraph("<b>HOW WELL DO I KNOW THESE WORDS?</b>", styles["h2"]))
        know_rows = [["Word", "I know it well", "I know it a little", "I need to learn it"]]
        for w in vocab[:12]:
            know_rows.append([w, "\u2610", "\u2610", "\u2610"])
        elements.append(_data_table(
            know_rows, [pw * 0.28, pw * 0.22, pw * 0.22, pw * 0.22],
            fn, fb, get_color_hex("red"), grade))
        elements.append(Spacer(1, 0.4 * cm))

        # Vocabulary goal
        elements.append(Paragraph("<b>MY VOCABULARY GOAL</b>", styles["h2"]))
        elements.append(Paragraph(
            "Set a goal for improving your vocabulary:", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph(
            "I will learn __________ new words by __________.", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(Paragraph(
            "My strategy: _______________________________________________", styles["body"]))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_writing_lines(3, pw))
        elements.append(PageBreak())

    _back_cover(elements, styles, accent, grade, fn, fb)

    tmpl.build(elements)
    return buf.getvalue()
