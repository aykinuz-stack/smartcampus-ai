"""
Plan-Uyumlu Etkinlik Kitabi PDF Generator — Diamond 3D Premium Edition
======================================================================
Baskiya hazir, kitap standartinda mizanpaj:
- B5 (176x250mm) kitap boyutu
- Ic/dis margin (sirt payi) ile cilt uyumu
- Profesyonel tipografi: baslık hiyerarsisi, satir araligi, karakter araligi
- Tutarli renk paleti, gorsel hiyerarsi
- Hafta ayirici sayfalari, unite kapak sayfalari
- Sayfa numaralama, ust/alt bilgi bandi
- Her saat icin en az 1 sayfa — icerige gore tasabilir
"""
from __future__ import annotations
import json, os, random
from io import BytesIO
from pathlib import Path
from datetime import datetime

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "english"


def _load_json(name: str) -> dict:
    p = _DATA_DIR / name
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _load_weekly_plans() -> dict:
    return _load_json("weekly_plans.json")


def _load_content_data(gk: str) -> dict:
    out = {}
    gd = _load_json("grammar_data.json")
    out["grammar"] = gd.get(gk, {}).get("topics", [])
    vd = _load_json("vocabulary_data.json")
    out["vocabulary"] = vd.get(gk, {}).get("sets", [])
    ld = _load_json("listening_data.json")
    out["listening"] = ld.get(gk, [])
    rd = _load_json("reading_data.json")
    out["reading"] = rd.get(gk, [])
    wd = _load_json("writing_data.json")
    out["writing"] = wd.get(gk, {}).get("tasks", [])
    sd = _load_json("speaking_data.json")
    sp = sd.get(gk, {})
    out["speaking"] = sp.get("prompts", []) if isinstance(sp, dict) else []
    spd = _load_json("spelling_data.json")
    sp2 = spd.get(gk, {})
    out["spelling_words"] = sp2.get("words", []) if isinstance(sp2, dict) else []
    out["spelling_patterns"] = sp2.get("patterns", []) if isinstance(sp2, dict) else []
    prd = _load_json("pronunciation_data.json")
    pr = prd.get(gk, {})
    out["pron_pairs"] = pr.get("pairs", []) if isinstance(pr, dict) else []
    out["pron_stress"] = pr.get("stress", []) if isinstance(pr, dict) else []
    fld = _load_json("functional_lang_data.json")
    out["functional"] = fld.get(gk, {}).get("situations", []) if isinstance(fld.get(gk), dict) else []
    csd = _load_json("comm_strategies_data.json")
    out["comm_strategies"] = csd.get(gk, {}).get("strategies", []) if isinstance(csd.get(gk), dict) else []
    return out


_GRADE_INFO = {
    "1":  {"label": "1. Sinif",  "cefr": "A1.1", "school": "Ilkokul"},
    "2":  {"label": "2. Sinif",  "cefr": "A1.2", "school": "Ilkokul"},
    "3":  {"label": "3. Sinif",  "cefr": "A1.3", "school": "Ilkokul"},
    "4":  {"label": "4. Sinif",  "cefr": "A1+",  "school": "Ilkokul"},
    "5":  {"label": "5. Sinif",  "cefr": "A2.1", "school": "Ortaokul"},
    "6":  {"label": "6. Sinif",  "cefr": "A2.2", "school": "Ortaokul"},
    "7":  {"label": "7. Sinif",  "cefr": "A2.3", "school": "Ortaokul"},
    "8":  {"label": "8. Sinif",  "cefr": "A2.4", "school": "Ortaokul"},
    "9":  {"label": "9. Sinif",  "cefr": "B1.1", "school": "Lise"},
    "10": {"label": "10. Sinif", "cefr": "B1.2", "school": "Lise"},
    "11": {"label": "11. Sinif", "cefr": "B2.1", "school": "Lise"},
    "12": {"label": "12. Sinif", "cefr": "B2.2", "school": "Lise"},
}


# ── Content Bank Loading ─────────────────────────────────────────────────────
_CB_BANK_ATTRS = [
    ("STORY_BANK", "story"), ("CULTURE_CORNER_BANK", "culture"),
    ("TURKEY_CORNER_BANK", "turkey"), ("COMIC_STRIP_BANK", "comic"),
    ("MISSION_BANK", "mission"), ("ESCAPE_ROOM_BANK", "escape"),
    ("FAMILY_CORNER_BANK", "family"), ("SEL_BANK", "sel"),
    ("STEAM_BANK", "steam"), ("PODCAST_BANK", "podcast"),
    ("PROJECT_BANK", "project"), ("FUN_FACTS_BANK", "funfacts"),
    ("PROGRESS_CHECK_BANK", "progress"), ("MODEL_WRITING_BANK", "writing"),
    ("WORKBOOK_BANK", "workbook"), ("PRONUNCIATION_BANK", "pronunciation"),
]

_CB_TR = {
    "story": "Hikaye", "culture": "Kultur Kosesi", "turkey": "Turkiye Kosesi",
    "comic": "Cizgi Roman", "mission": "Gorev", "escape": "Kacis Odasi",
    "family": "Aile Kosesi", "sel": "SEL", "steam": "STEAM",
    "podcast": "Podcast", "project": "Proje", "funfacts": "Ilginc Bilgiler",
    "progress": "Ilerleme Testi", "writing": "Yazma Modeli",
    "workbook": "Calisma Kitabi", "pronunciation": "Telaffuz",
}

_DAY_CB_MAP = {
    "mon": ["story", "culture", "pronunciation"],
    "tue": ["podcast", "comic", "turkey"],
    "wed": ["writing", "workbook", "steam"],
    "thu": ["project", "sel", "family"],
    "fri": ["escape", "funfacts", "progress", "mission"],
}

_UNIT_BREAKS = [4, 7, 11, 14, 18, 22, 25, 29, 32, 37]


def _week_to_unit_ab(week: int) -> int:
    for i, brk in enumerate(_UNIT_BREAKS):
        if week < brk:
            return i + 1
    return 10


def _load_content_banks(grade_num: int) -> dict:
    """Load content bank data for a grade. Returns {bank_key: {unit: data}}."""
    result = {}
    try:
        if grade_num == 5:
            from views.textbook_grade5 import (
                _STORY_BANK, _CULTURE_CORNER_BANK, _TURKEY_CORNER_BANK,
                _COMIC_STRIP_BANK, _MISSION_BANK, _ESCAPE_ROOM_BANK,
                _FAMILY_CORNER_BANK, _SEL_BANK, _STEAM_BANK, _PODCAST_BANK,
                _PROJECT_BANK, _FUN_FACTS_BANK, _PROGRESS_CHECK_BANK,
                _MODEL_WRITING_BANK, _WORKBOOK_BANK, _PRONUNCIATION_BANK,
            )
            _bmap = {"story": _STORY_BANK, "culture": _CULTURE_CORNER_BANK,
                     "turkey": _TURKEY_CORNER_BANK, "comic": _COMIC_STRIP_BANK,
                     "mission": _MISSION_BANK, "escape": _ESCAPE_ROOM_BANK,
                     "family": _FAMILY_CORNER_BANK, "sel": _SEL_BANK,
                     "steam": _STEAM_BANK, "podcast": _PODCAST_BANK,
                     "project": _PROJECT_BANK, "funfacts": _FUN_FACTS_BANK,
                     "progress": _PROGRESS_CHECK_BANK, "writing": _MODEL_WRITING_BANK,
                     "workbook": _WORKBOOK_BANK, "pronunciation": _PRONUNCIATION_BANK}
        else:
            mod = __import__(f"views.content_banks.grade{grade_num}", fromlist=["__all__"])
            _bmap = {}
            for attr_name, key in _CB_BANK_ATTRS:
                bank = getattr(mod, attr_name, None)
                if bank and isinstance(bank, dict):
                    _bmap[key] = bank
        for key, bank in _bmap.items():
            grade_data = bank.get(grade_num, bank)
            if isinstance(grade_data, dict) and any(isinstance(k, int) for k in grade_data.keys()):
                result[key] = grade_data
    except Exception:
        pass
    return result


def _get_cb_title(bank_key: str, data: dict) -> str:
    """Extract a short title from content bank data."""
    if isinstance(data, dict):
        for k in ("title", "name", "topic", "theme"):
            v = data.get(k)
            if v and isinstance(v, str):
                return v[:60]
    return _CB_TR.get(bank_key, bank_key)

_SLOT_META = {
    "MAIN COURSE":    {"tr": "ANA DERS",           "short": "M", "hue": "green"},
    "SKILLS LAB":     {"tr": "BECERI LAB",          "short": "S", "hue": "purple"},
    "NATIVE SPEAKER": {"tr": "ANADILI INGILIZCE",  "short": "N", "hue": "red"},
}

_DAY_TR = {"mon": "Pazartesi", "tue": "Sali", "wed": "Carsamba",
           "thu": "Persembe", "fri": "Cuma"}

_PHASE_TR = {"Tanitim": "Tanitim", "Gelistirme": "Gelistirme",
             "Pekistirme": "Pekistirme", "Degerlendirme": "Degerlendirme"}


def _safe_get(data, idx, default=None):
    if isinstance(data, list) and data:
        return data[idx % len(data)]
    return default


def _pick_content(hour_data, week_data, content):
    instruments = set(hour_data.get("instruments", []))
    ci = week_data.get("content_indices", {})
    wn = week_data.get("week", 1)
    out = {}

    if instruments & {"vocabulary_set", "flashcard"}:
        vi = ci.get("vocabulary", 0)
        vset = _safe_get(content.get("vocabulary", []), vi, {})
        if isinstance(vset, dict):
            out["vocab_words"] = vset.get("words", [])[:12]
            out["vocab_cat"] = vset.get("cat", "")

    if "grammar_exercise" in instruments:
        topics = content.get("grammar", [])
        gf = week_data.get("grammar_focus", "").lower()
        matched = None
        for t in topics:
            if gf and gf in t.get("name", "").lower():
                matched = t
                break
        if not matched:
            matched = _safe_get(topics, wn - 1)
        if matched and isinstance(matched, dict):
            out["grammar_topic"] = matched.get("name", "")
            out["grammar_rules"] = matched.get("rules", [])[:4]
            out["grammar_examples"] = matched.get("examples", [])[:6]
            out["grammar_exercises"] = matched.get("exercises", [])[:6]

    if "listening_player" in instruments:
        p = _safe_get(content.get("listening", []), ci.get("listening", 0))
        if p and isinstance(p, dict):
            out["listening_text"] = p.get("text", "")
            out["listening_qs"] = p.get("qs", [])[:5]

    if "reading_passage" in instruments:
        p = _safe_get(content.get("reading", []), ci.get("reading", 0))
        if p and isinstance(p, dict):
            out["reading_title"] = p.get("title", "")
            out["reading_text"] = p.get("text", "")
            out["reading_qs"] = p.get("qs", [])[:5]

    if "writing_task" in instruments:
        t = _safe_get(content.get("writing", []), ci.get("writing", 0))
        if t and isinstance(t, dict):
            out["writing_title"] = t.get("title", "")
            out["writing_prompt"] = t.get("prompt", "")
            out["writing_hints"] = t.get("hints", [])[:6]
            out["writing_target"] = t.get("word_target", 0)

    if instruments & {"speaking_prompt", "role_play"}:
        sp = _safe_get(content.get("speaking", []), ci.get("speaking", 0))
        if sp:
            out["speaking_prompt"] = sp.get("prompt", "") if isinstance(sp, dict) else str(sp)
            if isinstance(sp, dict):
                out["speaking_expected"] = sp.get("expected", "")

    if "spelling_practice" in instruments:
        words = content.get("spelling_words", [])
        si = ci.get("spelling_start", 0)
        if words:
            out["spelling_words"] = words[si:si + 12] if si < len(words) else words[:12]

    if "pronunciation_pairs" in instruments:
        pairs = content.get("pron_pairs", [])
        pi = ci.get("pronunciation", 0)
        if pairs:
            out["pron_pairs"] = pairs[pi:pi + 6] if pi < len(pairs) else pairs[:6]
    if "pronunciation_stress" in instruments:
        stress = content.get("pron_stress", [])
        pi = ci.get("pronunciation", 0)
        if stress:
            out["pron_stress"] = stress[pi:pi + 8] if pi < len(stress) else stress[:8]

    if "functional_dialogue" in instruments:
        s = _safe_get(content.get("functional", []), ci.get("functional", 0))
        if s and isinstance(s, dict):
            out["functional_situation"] = s

    if "comm_strategy" in instruments:
        s = _safe_get(content.get("comm_strategies", []), ci.get("comm_strategy", 0))
        if s:
            out["comm_strategy"] = s

    return out


# ─────────────────────────────────────────────────────────────────
# BASKI-HAZIR PDF GENERATOR
# ─────────────────────────────────────────────────────────────────
def generate_activity_book_pdf(
    grade_key: str,
    start_week: int = 1,
    end_week: int = 36,
    day_filter: str | None = None,
) -> bytes:
    from reportlab.lib.pagesizes import B5
    from reportlab.lib import colors as rl
    from reportlab.lib.units import cm, mm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, PageBreak,
                                     KeepTogether, NextPageTemplate,
                                     PageTemplate, Frame)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus.doctemplate import BaseDocTemplate
    try:
        from utils.shared_data import ensure_turkish_pdf_fonts
        from utils.report_utils import get_institution_info
        fn, fb = ensure_turkish_pdf_fonts()
        info = get_institution_info()
    except Exception:
        fn, fb = "Helvetica", "Helvetica-Bold"
        info = {}

    font_ok = fn != "Helvetica"

    def _t(text):
        if font_ok:
            return str(text)
        _m = {"\u0131":"i","\u0130":"I","\u011f":"g","\u011e":"G",
              "\u00fc":"u","\u00dc":"U","\u015f":"s","\u015e":"S",
              "\u00f6":"o","\u00d6":"O","\u00e7":"c","\u00c7":"C"}
        return str(text).translate(str.maketrans(_m))

    wp_all = _load_weekly_plans()
    weeks = wp_all.get(grade_key, [])
    if not weeks:
        return b""

    cdata = _load_content_data(grade_key)
    # Content banks
    _gnum = int(grade_key) if grade_key.isdigit() else 0
    _cb_all = _load_content_banks(_gnum)
    gi = _GRADE_INFO.get(grade_key, {})
    glabel = gi.get("label", f"{grade_key}. Sinif")
    cefr = gi.get("cefr", "")
    school = gi.get("school", "")
    now_str = datetime.now().strftime("%d.%m.%Y")
    today = datetime.now().date()
    acad_s = today.year if today.month >= 9 else today.year - 1
    acad_year = f"{acad_s}-{acad_s+1}"
    kurum = info.get("name", "")

    buf = BytesIO()
    W, H = B5  # 176mm x 250mm — standart kitap boyutu

    # Kitap cilt payi icin ic margin buyuk
    M_IN = 2.2 * cm   # ic (sirt) margin
    M_OUT = 1.6 * cm   # dis margin
    M_TOP = 1.4 * cm
    M_BOT = 1.8 * cm
    pw = W - M_IN - M_OUT  # kullanilabilir genislik

    # ── RENK PALETI — Baski uyumlu CMYK-yakin renkler ──
    C_BLACK    = rl.HexColor("#1a1a2e")
    C_NAVY     = rl.HexColor("#0B0F19")
    C_DARK     = rl.HexColor("#94A3B8")
    C_GOLD     = rl.HexColor("#B8860B")  # DarkGoldenrod — baski uyumlu
    C_GOLD_L   = rl.HexColor("#DAA520")
    C_GREEN    = rl.HexColor("#1B7340")
    C_GREEN_L  = rl.HexColor("#2D9B5A")
    C_PURPLE   = rl.HexColor("#5B21B6")
    C_PURPLE_L = rl.HexColor("#7C3AED")
    C_RED      = rl.HexColor("#B91C1C")
    C_RED_L    = rl.HexColor("#DC2626")
    C_BLUE     = rl.HexColor("#1D4ED8")
    C_BLUE_L   = rl.HexColor("#3B82F6")
    C_TEAL     = rl.HexColor("#0F766E")
    C_ORANGE   = rl.HexColor("#B45309")
    C_WHITE    = rl.white
    C_TEXT     = rl.HexColor("#1F2937")
    C_TEXT2    = rl.HexColor("#94A3B8")
    C_GRAY     = rl.HexColor("#94A3B8")
    C_GRAY_L   = rl.HexColor("#64748B")
    C_LIGHT    = rl.HexColor("#F9FAFB")
    C_LIGHT2   = rl.HexColor("#151B2B")
    C_BORDER   = rl.HexColor("#232B3E")
    C_CREAM    = rl.HexColor("#FFFBEB")
    C_MINT     = rl.HexColor("#ECFDF5")
    C_LAVEN    = rl.HexColor("#F5F3FF")
    C_ROSE     = rl.HexColor("#FFF1F2")

    SLOT_C = {
        "green":  (C_GREEN, C_GREEN_L, C_MINT, "ANA DERS"),
        "purple": (C_PURPLE, C_PURPLE_L, C_LAVEN, "BECERI LAB"),
        "red":    (C_RED, C_RED_L, C_ROSE, "NATIVE SPEAKER"),
    }

    # ── TIPOGRAFI — Profesyonel kitap stili ──
    def _s(name, **kw):
        kw.setdefault("fontName", fn)
        kw.setdefault("fontSize", 9)
        kw.setdefault("leading", 13)
        kw.setdefault("textColor", C_TEXT)
        return ParagraphStyle(name, **kw)

    # Kapak
    S_COV_TITLE = _s("ct", fontName=fb, fontSize=28, leading=34, alignment=TA_CENTER, textColor=C_WHITE)
    S_COV_SUB   = _s("cs", fontName=fb, fontSize=14, leading=18, alignment=TA_CENTER, textColor=C_GOLD_L)
    S_COV_INFO  = _s("ci", fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#232B3E"))
    # Icindekiler
    S_TOC_H     = _s("th", fontName=fb, fontSize=13, leading=17, textColor=C_WHITE)
    S_TOC       = _s("tc", fontSize=8, leading=11)
    S_TOC_B     = _s("tb", fontName=fb, fontSize=8, leading=11)
    # Hafta kapak
    S_WK_NUM    = _s("wn", fontName=fb, fontSize=36, leading=40, alignment=TA_CENTER, textColor=C_WHITE)
    S_WK_THEME  = _s("wt", fontName=fb, fontSize=16, leading=20, alignment=TA_CENTER, textColor=C_GOLD_L)
    S_WK_INFO   = _s("wi", fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#232B3E"))
    # Sayfa basliklari
    S_PG_TITLE  = _s("pt", fontName=fb, fontSize=10, leading=13, textColor=C_WHITE)
    S_PG_SUB    = _s("ps", fontSize=7.5, leading=10, textColor=rl.HexColor("#232B3E"), alignment=TA_RIGHT)
    # Sectionlar
    S_SEC       = _s("se", fontName=fb, fontSize=9, leading=12, textColor=C_WHITE)
    S_SEC_SM    = _s("ss", fontName=fb, fontSize=8, leading=11, textColor=C_WHITE)
    # Govde
    S_BODY      = _s("bo", fontSize=9, leading=13, alignment=TA_JUSTIFY)
    S_BODY_SM   = _s("bs", fontSize=8, leading=11.5)
    S_BODY_XS   = _s("bx", fontSize=7, leading=10, textColor=C_GRAY)
    S_BOLD      = _s("bd", fontName=fb, fontSize=9, leading=13)
    S_BOLD_SM   = _s("bds", fontName=fb, fontSize=8, leading=11.5)
    # Sorular
    S_Q         = _s("q", fontSize=8.5, leading=12, leftIndent=6)
    S_ANS       = _s("an", fontSize=8, leading=20, textColor=C_GRAY_L)
    # Diger
    S_TIP       = _s("ti", fontSize=7, leading=10, textColor=C_ORANGE, leftIndent=8)
    S_FOOTER    = _s("ft", fontSize=6, leading=8, textColor=C_GRAY_L)

    elements = []

    # Gun filtresi
    _day_order = [day_filter] if day_filter else ["mon", "tue", "wed", "thu", "fri"]

    # ═══════════════════════════════════════════════════════
    # YARDIMCI FONKSIYONLAR
    # ═══════════════════════════════════════════════════════
    def _rule(color=C_GOLD, thickness=1.5):
        t = Table([[""]], colWidths=[pw], rowHeights=[thickness])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),color),
            ("TOPPADDING",(0,0),(0,0),0),("BOTTOMPADDING",(0,0),(0,0),0),
        ]))
        return t

    def _sec_hdr(title, color, accent=C_GOLD):
        t = Table(
            [["", Paragraph(_t(f"<b>{title}</b>"), S_SEC)]],
            colWidths=[4, pw-4], rowHeights=[20])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),accent),
            ("BACKGROUND",(1,0),(1,0),color),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(1,0),(1,0),10),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("ROUNDEDCORNERS",[0,4,4,0]),
        ]))
        return t

    def _lines(n=3, label=""):
        rows = []
        if label:
            rows.append([Paragraph(_t(f"<b>{label}</b>"), S_BOLD_SM)])
        for i in range(n):
            pfx = f"{i+1}. " if n > 1 else ""
            rows.append([Paragraph(_t(f"{pfx}{'_'*90}"), S_ANS)])
        t = Table(rows, colWidths=[pw])
        t.setStyle(TableStyle([
            ("LEFTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),0),
            ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ]))
        return t

    def _mcq(q_text, opts, num=1):
        rows = [[Paragraph(_t(f"<b>{num}.</b> {q_text}"), S_Q)]]
        abc = "ABCDEFGH"
        cells = [Paragraph(_t(f"  {abc[i]}) {o}"), S_BODY_SM) for i, o in enumerate(opts[:4])]
        if len(cells) == 4:
            rows.append([Table([[cells[0],cells[1]],[cells[2],cells[3]]],
                                colWidths=[pw*.48, pw*.48])])
        elif len(cells) >= 2:
            rows.append([Table([[cells[0],cells[1]]], colWidths=[pw*.48, pw*.48])])
        t = Table(rows, colWidths=[pw])
        t.setStyle(TableStyle([
            ("LEFTPADDING",(0,0),(-1,-1),4),
            ("TOPPADDING",(0,0),(-1,-1),2),
            ("BOTTOMPADDING",(0,0),(-1,-1),2),
        ]))
        return t

    # ═══════════════════════════════════════════════════════
    # KAPAK SAYFASI
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 2.5*cm))

    # Kurum
    if kurum:
        elements.append(Paragraph(_t(kurum), _s(
            "kr", fontName=fb, fontSize=14, leading=18,
            textColor=C_TEXT, alignment=TA_CENTER, spaceAfter=4)))
    elements.append(Paragraph(_t(f"{acad_year} Egitim-Ogretim Yili"), _s(
        "yr", fontSize=10, leading=14, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=16)))

    elements.append(Spacer(1, 1*cm))

    # Ust dekoratif cizgi
    elements.append(_rule(C_GOLD, 2))

    # Ana baslik blogu
    cv_rows = [
        [Paragraph(_t("DIAMOND 3D PREMIUM EDITION"), _s(
            "d3d", fontName=fb, fontSize=9, leading=12,
            textColor=C_GOLD_L, alignment=TA_CENTER, spaceBefore=4))],
        [Spacer(1,6)],
        [Paragraph(_t("ETKINLIK KITABI"), S_COV_TITLE)],
        [Paragraph(_t("ACTIVITY BOOK"), _s(
            "ab", fontSize=13, leading=17, textColor=rl.HexColor("#B9F2FF"),
            alignment=TA_CENTER))],
        [Spacer(1,8)],
        [Paragraph(_t(f"{glabel} — {school}"), S_COV_SUB)],
        [Paragraph(_t(f"CEFR {cefr}"), S_COV_INFO)],
        [Spacer(1,6)],
        [Paragraph(_t(f"{min(end_week,len(weeks))-max(1,start_week)+1} Hafta  |  {(min(end_week,len(weeks))-max(1,start_week)+1)*len(_day_order)*2} Ders Saati  |  10 Beceri Alani"
                      + (f"  |  {_DAY_TR.get(day_filter,'')}" if day_filter else "")), _s(
            "det", fontSize=8, leading=11, textColor=rl.HexColor("#64748B"),
            alignment=TA_CENTER))],
    ]
    cv = Table(cv_rows, colWidths=[pw])
    cv.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_NAVY),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(0,0),16),
        ("BOTTOMPADDING",(0,-1),(0,-1),16),
    ]))
    elements.append(cv)

    # Altin alt cizgi
    elements.append(_rule(C_GOLD, 2))

    elements.append(Spacer(1, 1.2*cm))

    # Bilgi kutusu
    ib_rows = [
        [Paragraph(_t("Main Course (4 saat) + Skills Lab (4 saat) + Native Speaker (2 saat)"), _s(
            "ib", fontName=fb, fontSize=8.5, leading=12, textColor=C_GOLD, alignment=TA_CENTER))],
        [Paragraph(_t("Haftalik 10 saat, 4 fazli unite dongusu, 10 beceri alaninda etkinlik"), _s(
            "ib2", fontSize=7.5, leading=10.5, textColor=C_TEXT2, alignment=TA_CENTER))],
    ]
    ibt = Table(ib_rows, colWidths=[pw])
    ibt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CREAM),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("BOX",(0,0),(-1,-1),0.75,C_GOLD),
        ("TOPPADDING",(0,0),(0,0),8),
        ("BOTTOMPADDING",(0,-1),(0,-1),8),
        ("ROUNDEDCORNERS",[6,6,6,6]),
    ]))
    elements.append(ibt)

    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph(_t(now_str), _s(
        "dt", fontSize=8, leading=11, textColor=C_GRAY, alignment=TA_CENTER)))

    cp = []
    if info.get("address"): cp.append(info["address"])
    if info.get("phone"): cp.append(f"Tel: {info['phone']}")
    if info.get("web"): cp.append(info["web"])
    if cp:
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(_t(" | ".join(cp)), _s(
            "ct2", fontSize=6.5, leading=9, textColor=C_GRAY_L, alignment=TA_CENTER)))

    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # KUNYE / KOLOFON SAYFASI
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 6*cm))
    kol_items = [
        f"<b>Kitap Adi:</b> {glabel} Ingilizce Etkinlik Kitabi — Diamond 3D Premium Edition",
        f"<b>Seviye:</b> CEFR {cefr} | {school}",
        f"<b>Kapsam:</b> 36 Hafta, 360 Ders Saati, 10 Beceri Alani",
        f"<b>Ders Modeli:</b> Main Course (4h) + Skills Lab (4h) + Native Speaker (2h)",
        f"<b>Akademik Yil:</b> {acad_year}",
        f"<b>Uretim Tarihi:</b> {now_str}",
        f"<b>Platform:</b> SmartCampus AI — Akilli Kampus Egitim Yonetim Sistemi",
    ]
    if kurum:
        kol_items.insert(0, f"<b>Kurum:</b> {kurum}")
    for ki in kol_items:
        elements.append(Paragraph(_t(ki), _s("kl", fontSize=8, leading=13, textColor=C_TEXT2)))
        elements.append(Spacer(1, 0.1*cm))
    elements.append(Spacer(1, 1*cm))
    elements.append(_rule(C_BORDER, 0.5))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(
        _t("Bu kitap SmartCampus AI platformu tarafindan otomatik olarak uretilmistir. "
           "Icerikler MEB mufredat kazanimlarina ve CEFR dil cercevesine uygun olarak "
           "haftalik ders planlariyla es gudumlu hazirlanmistir."),
        _s("kl2", fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_JUSTIFY)))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # ICINDEKILER
    # ═══════════════════════════════════════════════════════
    sw = max(1, min(start_week, len(weeks)))
    ew = max(sw, min(end_week, len(weeks)))

    toc_hdr = Table(
        [["", Paragraph(_t("<b>ICINDEKILER</b>"), S_TOC_H)]],
        colWidths=[4, pw-4], rowHeights=[26])
    toc_hdr.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),C_GOLD),
        ("BACKGROUND",(1,0),(1,0),C_NAVY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(1,0),(1,0),12),
        ("ROUNDEDCORNERS",[0,6,6,0]),
    ]))
    elements.append(toc_hdr)
    elements.append(Spacer(1, 0.4*cm))

    toc_rows = []
    for wi in range(sw-1, ew):
        wk = weeks[wi]
        wn = wk.get("week", wi+1)
        toc_rows.append([
            Paragraph(_t(f"<b>Hafta {wn}</b>"), S_TOC_B),
            Paragraph(_t(f"Unite {wk.get('unit',1)}: {wk.get('unit_theme_tr','')}"), S_TOC),
            Paragraph(_t(f"({wk.get('unit_theme','')})"), _s(f"te{wn}", fontSize=7, leading=10, textColor=C_GRAY)),
            Paragraph(_t(wk.get("phase","")), _s(f"tp{wn}", fontSize=7, leading=10, textColor=C_PURPLE)),
        ])
    if toc_rows:
        tt = Table(toc_rows, colWidths=[pw*.12, pw*.38, pw*.3, pw*.2])
        ts = [
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LINEBELOW",(0,0),(-1,-2),0.3,C_BORDER),
        ]
        for ri in range(len(toc_rows)):
            if ri % 2 == 0:
                ts.append(("BACKGROUND",(0,ri),(-1,ri),C_LIGHT))
        tt.setStyle(TableStyle(ts))
        elements.append(tt)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # HAFTA SAYFALARI
    # ═══════════════════════════════════════════════════════
    for wi in range(sw-1, ew):
        wk = weeks[wi]
        wn = wk.get("week", wi+1)
        unit_n = wk.get("unit", 1)
        theme = wk.get("unit_theme", "")
        theme_tr = wk.get("unit_theme_tr", "")
        phase = wk.get("phase", "")
        gram = wk.get("grammar_focus", "")
        wdays = wk.get("days", {})

        # ── HAFTA KAPAK SAYFASI ──
        elements.append(Spacer(1, 3*cm))
        elements.append(_rule(C_GOLD, 2))

        wk_cv = [
            [Paragraph(_t(f"HAFTA"), _s(f"wl{wn}", fontName=fb, fontSize=10,
                        leading=13, textColor=C_GOLD_L, alignment=TA_CENTER))],
            [Paragraph(_t(f"{wn}"), S_WK_NUM)],
            [Spacer(1, 4)],
            [Paragraph(_t(f"Unite {unit_n}: {theme_tr}"), S_WK_THEME)],
            [Paragraph(_t(theme), _s(f"wte{wn}", fontSize=11, leading=15,
                        textColor=rl.HexColor("#232B3E"), alignment=TA_CENTER))],
            [Spacer(1, 8)],
            [Paragraph(_t(f"{_PHASE_TR.get(phase,phase)}  |  Gramer: {gram}"), S_WK_INFO)],
            [Paragraph(_t(f"CEFR {cefr}  |  10 Ders Saati  |  5 Gun"), _s(
                f"wci{wn}", fontSize=8.5, leading=12, textColor=C_GRAY_L, alignment=TA_CENTER))],
        ]
        wct = Table(wk_cv, colWidths=[pw])
        wct.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_NAVY),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(0,0),20),
            ("BOTTOMPADDING",(0,-1),(0,-1),20),
        ]))
        elements.append(wct)
        elements.append(_rule(C_GOLD, 2))

        # Hafta ders dagitim tablosu
        elements.append(Spacer(1, 0.6*cm))
        dist_hdr = [
            Paragraph(_t("<b>Gun</b>"), S_BOLD_SM),
            Paragraph(_t("<b>1. Saat</b>"), S_BOLD_SM),
            Paragraph(_t("<b>2. Saat</b>"), S_BOLD_SM),
        ]
        dist_rows = [dist_hdr]
        for dk in _day_order:
            dd = wdays.get(dk, {})
            dn = dd.get("day_name", _DAY_TR.get(dk, dk))
            hrs = dd.get("hours", [])
            h1 = hrs[0].get("focus","") if len(hrs)>0 else ""
            h2 = hrs[1].get("focus","") if len(hrs)>1 else ""
            h1_slot = hrs[0].get("slot","") if len(hrs)>0 else ""
            slot_pfx = ""
            if dk == "fri":
                slot_pfx = "N: "
            elif "SKILLS" in (hrs[1].get("slot","") if len(hrs)>1 else ""):
                pass
            dist_rows.append([
                Paragraph(_t(f"<b>{dn}</b>"), S_BOLD_SM),
                Paragraph(_t(h1[:50]), S_BODY_SM),
                Paragraph(_t(h2[:50]), S_BODY_SM),
            ])
        dtt = Table(dist_rows, colWidths=[pw*.18, pw*.41, pw*.41])
        dts = [
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),5),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("BACKGROUND",(0,0),(-1,0),C_DARK),
            ("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
            ("BOX",(0,0),(-1,-1),0.5,C_BORDER),
            ("INNERGRID",(0,0),(-1,-1),0.3,C_BORDER),
        ]
        for ri in range(1, len(dist_rows)):
            if ri % 2 == 0:
                dts.append(("BACKGROUND",(0,ri),(-1,ri),C_LIGHT))
            if ri == len(dist_rows)-1:  # Cuma
                dts.append(("BACKGROUND",(0,ri),(-1,ri),C_ROSE))
        dtt.setStyle(TableStyle(dts))
        elements.append(dtt)
        elements.append(PageBreak())

        # ── HER SAAT ICIN ETKINLIK SAYFALARI ──
        gh = 0
        for dk in _day_order:
            dd = wdays.get(dk, {})
            dn = dd.get("day_name", _DAY_TR.get(dk, dk))
            hrs = dd.get("hours", [])

            for h in hrs:
                gh += 1
                hnum = h.get("hour", gh)
                slot = h.get("slot", "MAIN COURSE")
                sc_key = h.get("slot_color", "green")
                focus = h.get("focus", "")
                dur = h.get("duration", "40 dk")
                acts = h.get("activity", [])
                insts = h.get("instruments", [])
                mats = h.get("materials", [])
                tips = h.get("tips", "")
                sm = _SLOT_META.get(slot, _SLOT_META["MAIN COURSE"])
                sc_main, sc_light, sc_bg, sc_label = SLOT_C.get(sc_key, SLOT_C["green"])

                hc = _pick_content(h, wk, cdata)

                # ── SAYFA UST KUNYE ──
                elements.append(_rule(C_GOLD, 1.5))

                # Baslik bandi
                hdr_l = Paragraph(_t(f"<b>Hafta {wn}  |  {dn}  |  Saat {hnum}</b>"), S_PG_TITLE)
                hdr_r = Paragraph(_t(f"{glabel}  |  CEFR {cefr}  |  {dur}"), S_PG_SUB)
                hdr = Table([[hdr_l, hdr_r]], colWidths=[pw*.6, pw*.4], rowHeights=[20])
                hdr.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,-1),sc_main),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("LEFTPADDING",(0,0),(0,0),8),
                    ("RIGHTPADDING",(1,0),(1,0),8),
                    ("TOPPADDING",(0,0),(-1,-1),3),
                    ("BOTTOMPADDING",(0,0),(-1,-1),3),
                ]))
                elements.append(hdr)

                # Slot + Unite bilgi bandi
                info_l = Paragraph(_t(f"<b>{sc_label}</b>  |  Unite {unit_n}: {theme_tr}"), S_BODY_XS)
                info_r = Paragraph(_t(f"{_PHASE_TR.get(phase,phase)}  |  {gram}"),
                                   _s("ir", fontSize=6.5, leading=9, textColor=C_GRAY, alignment=TA_RIGHT))
                ib = Table([[info_l, info_r]], colWidths=[pw*.55, pw*.45], rowHeights=[13])
                ib.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,-1),sc_bg),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("LEFTPADDING",(0,0),(0,0),8),
                    ("RIGHTPADDING",(1,0),(1,0),8),
                    ("TOPPADDING",(0,0),(-1,-1),1),
                    ("BOTTOMPADDING",(0,0),(-1,-1),1),
                ]))
                elements.append(ib)
                elements.append(_rule(C_GOLD, 0.75))

                # Ad Soyad
                elements.append(Spacer(1, 0.15*cm))
                nr = Table([
                    [Paragraph(_t("Ad Soyad: ____________________________________"), S_BODY_SM),
                     Paragraph(_t("Tarih: ___/___/______   No: _____"),
                               _s("nr", fontSize=7.5, leading=10, textColor=C_TEXT, alignment=TA_RIGHT))]
                ], colWidths=[pw*.55, pw*.45], rowHeights=[13])
                nr.setStyle(TableStyle([
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("LINEBELOW",(0,0),(-1,-1),0.4,C_BORDER),
                ]))
                elements.append(nr)
                elements.append(Spacer(1, 0.15*cm))

                # ── DERS ODAGI ──
                elements.append(_sec_hdr(f"DERS ODAGI: {focus}", sc_main))
                elements.append(Spacer(1, 0.08*cm))

                # ── DERS AKISI ──
                elements.append(_sec_hdr("DERS AKISI", C_DARK))
                elements.append(Spacer(1, 0.04*cm))
                a_rows = []
                for ai, a in enumerate(acts):
                    a_rows.append([
                        Paragraph(_t(f"<b>{ai+1}</b>"), _s(
                            f"an{ai}", fontName=fb, fontSize=7.5, leading=10,
                            textColor=sc_main, alignment=TA_CENTER)),
                        Paragraph(_t(a), S_BODY_SM),
                    ])
                if a_rows:
                    at = Table(a_rows, colWidths=[0.6*cm, pw-0.6*cm])
                    ast = [
                        ("VALIGN",(0,0),(-1,-1),"TOP"),
                        ("LEFTPADDING",(0,0),(-1,-1),3),
                        ("TOPPADDING",(0,0),(-1,-1),2),
                        ("BOTTOMPADDING",(0,0),(-1,-1),2),
                        ("LINEBELOW",(0,0),(-1,-2),0.2,C_BORDER),
                    ]
                    for ri in range(len(a_rows)):
                        if ri % 2 == 0:
                            ast.append(("BACKGROUND",(0,ri),(-1,ri),C_LIGHT))
                    at.setStyle(TableStyle(ast))
                    elements.append(at)
                elements.append(Spacer(1, 0.12*cm))

                # ── DINAMIK ICERIK BLOKLARI ──
                sn = 0

                # VOCABULARY
                vw = hc.get("vocab_words", [])
                if vw:
                    sn += 1
                    vc = hc.get("vocab_cat", "Vocabulary")
                    elements.append(_sec_hdr(f"{sn}. KELIME CALISMASI — {vc}", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    vcells = [Paragraph(_t(f"<b>{i+1}.</b> {w}  = __________________"), S_BODY_SM)
                              for i, w in enumerate(vw[:12])]
                    mid = (len(vcells)+1)//2
                    vr = []
                    for i in range(max(mid, len(vcells)-mid)):
                        c1 = vcells[i] if i < mid else Paragraph("", S_BODY_SM)
                        c2 = vcells[mid+i] if mid+i < len(vcells) else Paragraph("", S_BODY_SM)
                        vr.append([c1, c2])
                    if vr:
                        vt = Table(vr, colWidths=[pw*.5, pw*.5])
                        vt.setStyle(TableStyle([
                            ("VALIGN",(0,0),(-1,-1),"TOP"),
                            ("LEFTPADDING",(0,0),(-1,-1),5),
                            ("TOPPADDING",(0,0),(-1,-1),1),
                            ("BOTTOMPADDING",(0,0),(-1,-1),1),
                            ("BOX",(0,0),(-1,-1),0.4,C_BORDER),
                            ("INNERGRID",(0,0),(-1,-1),0.2,C_BORDER),
                            ("BACKGROUND",(0,0),(-1,-1),C_LAVEN),
                        ]))
                        elements.append(vt)
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(_t("<b>Cumle Tamamla:</b> Kelimeleri kullanarak cumleler yazin."), S_BOLD_SM))
                    elements.append(_lines(3))
                    elements.append(Spacer(1, 0.08*cm))

                # GRAMMAR
                gt = hc.get("grammar_topic", "")
                if gt:
                    sn += 1
                    elements.append(_sec_hdr(f"{sn}. GRAMER — {gt}", C_BLUE))
                    elements.append(Spacer(1, 0.06*cm))
                    for r in hc.get("grammar_rules", [])[:3]:
                        elements.append(Paragraph(_t(f"  * {r}"), S_BODY_SM))
                    for e in hc.get("grammar_examples", [])[:4]:
                        elements.append(Paragraph(_t(f"    <i>{e}</i>"), S_BODY_SM))
                    exs = hc.get("grammar_exercises", [])
                    if exs:
                        elements.append(Spacer(1, 0.06*cm))
                        elements.append(Paragraph(_t("<b>Alishtirmalar:</b>"), S_BOLD_SM))
                        for qi, ex in enumerate(exs[:5]):
                            q = ex.get("q","") if isinstance(ex,dict) else str(ex)
                            opts = ex.get("opts",[]) if isinstance(ex,dict) else []
                            if opts:
                                elements.append(_mcq(q, opts, qi+1))
                            else:
                                elements.append(Paragraph(_t(f"<b>{qi+1}.</b> {q}"), S_Q))
                                elements.append(_lines(1))
                    elements.append(Spacer(1, 0.04*cm))
                    elements.append(Paragraph(_t("<b>Kendi cumlelerinizi yazin:</b>"), S_BOLD_SM))
                    elements.append(_lines(3))
                    elements.append(Spacer(1, 0.08*cm))

                # LISTENING
                lt = hc.get("listening_text", "")
                if lt:
                    sn += 1
                    elements.append(_sec_hdr(f"{sn}. DINLEME (Listening)", C_TEAL))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(_t(lt[:500]), _s(
                        "lt", fontSize=8, leading=11, borderWidth=0.4, borderColor=C_BORDER,
                        borderPadding=5, backColor=C_LIGHT2, alignment=TA_JUSTIFY)))
                    for qi, lq in enumerate(hc.get("listening_qs",[])[:4]):
                        if isinstance(lq,dict):
                            q, opts = lq.get("q",""), lq.get("opts",[])
                        else:
                            q, opts = str(lq), []
                        if opts:
                            elements.append(_mcq(q, opts, qi+1))
                        else:
                            elements.append(Paragraph(_t(f"<b>{qi+1}.</b> {q}"), S_Q))
                            elements.append(_lines(1))
                    elements.append(Spacer(1, 0.08*cm))

                # READING
                rt = hc.get("reading_text", "")
                if rt:
                    sn += 1
                    rtitle = hc.get("reading_title", "Reading")
                    elements.append(_sec_hdr(f"{sn}. OKUMA — {rtitle}", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(_t(rt[:600]), _s(
                        "rt", fontSize=8, leading=11, borderWidth=0.4, borderColor=C_BORDER,
                        borderPadding=5, backColor=C_MINT, alignment=TA_JUSTIFY)))
                    for qi, rq in enumerate(hc.get("reading_qs",[])[:4]):
                        if isinstance(rq,dict):
                            q, opts = rq.get("q",""), rq.get("opts",[])
                        else:
                            q, opts = str(rq), []
                        if opts:
                            elements.append(_mcq(q, opts, qi+1))
                        else:
                            elements.append(Paragraph(_t(f"<b>{qi+1}.</b> {q}"), S_Q))
                            elements.append(_lines(1))
                    elements.append(Spacer(1, 0.08*cm))

                # WRITING
                wp_t = hc.get("writing_prompt", "")
                if wp_t:
                    sn += 1
                    wt = hc.get("writing_title", "Writing")
                    wtar = hc.get("writing_target", 0)
                    tgt = f" ({wtar} kelime)" if wtar else ""
                    elements.append(_sec_hdr(f"{sn}. YAZMA — {wt}{tgt}", C_ORANGE))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(_t(f"<b>Gorev:</b> {wp_t}"), S_BODY))
                    for ht in hc.get("writing_hints",[])[:4]:
                        elements.append(Paragraph(_t(f"  * {ht}"), S_BODY_XS))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(_lines(8, "Yazinizi buraya yazin:"))
                    elements.append(Spacer(1, 0.08*cm))

                # SPEAKING
                sp = hc.get("speaking_prompt", "")
                if sp:
                    sn += 1
                    elements.append(_sec_hdr(f"{sn}. KONUSMA (Speaking)", C_RED))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(_t(f"<b>Gorev:</b> {sp}"), S_BODY))
                    se = hc.get("speaking_expected", "")
                    if se:
                        elements.append(Paragraph(_t(f"<b>Beklenen:</b> {se}"), S_BODY_XS))
                    elements.append(Spacer(1, 0.04*cm))
                    elements.append(Paragraph(_t("<b>Diyalog Pratigi:</b>"), S_BOLD_SM))
                    for lbl in ["A:","B:","A:","B:"]:
                        elements.append(Paragraph(_t(f"{lbl} {'_'*75}"), S_ANS))
                    elements.append(_lines(2, "Notlar:"))
                    elements.append(Spacer(1, 0.08*cm))

                # SPELLING
                sw_l = hc.get("spelling_words", [])
                if sw_l:
                    sn += 1
                    elements.append(_sec_hdr(f"{sn}. HECELEME (Spelling)", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    scells = [Paragraph(_t(f"<b>{i+1}.</b> {(w if isinstance(w,str) else str(w))}  > _____________"), S_BODY_SM)
                              for i, w in enumerate(sw_l[:10])]
                    mid = (len(scells)+1)//2
                    sr = []
                    for i in range(max(mid, len(scells)-mid)):
                        c1 = scells[i] if i < mid else Paragraph("", S_BODY_SM)
                        c2 = scells[mid+i] if mid+i < len(scells) else Paragraph("", S_BODY_SM)
                        sr.append([c1, c2])
                    if sr:
                        st = Table(sr, colWidths=[pw*.5, pw*.5])
                        st.setStyle(TableStyle([
                            ("VALIGN",(0,0),(-1,-1),"TOP"),
                            ("LEFTPADDING",(0,0),(-1,-1),5),
                            ("TOPPADDING",(0,0),(-1,-1),1),
                            ("BOTTOMPADDING",(0,0),(-1,-1),1),
                            ("BOX",(0,0),(-1,-1),0.4,C_BORDER),
                        ]))
                        elements.append(st)
                    elements.append(Spacer(1, 0.08*cm))

                # PRONUNCIATION
                pp = hc.get("pron_pairs", [])
                ps = hc.get("pron_stress", [])
                if pp or ps:
                    sn += 1
                    elements.append(_sec_hdr(f"{sn}. TELAFFUZ (Pronunciation)", C_TEAL))
                    elements.append(Spacer(1, 0.06*cm))
                    if pp:
                        elements.append(Paragraph(_t("<b>Minimal Pairs:</b>"), S_BOLD_SM))
                        for pair in pp[:5]:
                            if isinstance(pair, (list,tuple)) and len(pair) >= 2:
                                elements.append(Paragraph(_t(f"  [ ] {pair[0]}   —   [ ] {pair[1]}"), S_BODY_SM))
                    if ps:
                        elements.append(Paragraph(_t("<b>Word Stress:</b>"), S_BOLD_SM))
                        for sw2 in ps[:6]:
                            elements.append(Paragraph(_t(f"  {sw2 if isinstance(sw2,str) else str(sw2)}  > vurgu: ______"), S_BODY_SM))
                    elements.append(Spacer(1, 0.08*cm))

                # FUNCTIONAL LANGUAGE
                fl = hc.get("functional_situation", {})
                if fl and isinstance(fl, dict):
                    sn += 1
                    sn_name = fl.get("situation", fl.get("name",""))
                    elements.append(_sec_hdr(f"{sn}. ISLEVSEL DIL — {sn_name}", C_BLUE_L))
                    elements.append(Spacer(1, 0.06*cm))
                    phrases = fl.get("phrases", fl.get("expressions",[]))
                    if isinstance(phrases, list):
                        for p in phrases[:6]:
                            elements.append(Paragraph(_t(f"  * {p}"), S_BODY_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    elements.append(Paragraph(_t("<b>Kendi diyalogunuzu yazin:</b>"), S_BOLD_SM))
                    for lbl in ["A:","B:","A:","B:"]:
                        elements.append(Paragraph(_t(f"{lbl} {'_'*75}"), S_ANS))
                    elements.append(Spacer(1, 0.08*cm))

                # COMM STRATEGY
                cs = hc.get("comm_strategy")
                if cs:
                    sn += 1
                    csn = cs.get("strategy",cs.get("name","")) if isinstance(cs,dict) else str(cs)
                    elements.append(_sec_hdr(f"{sn}. ILETISIM STRATEJISI — {csn}", C_DARK))
                    elements.append(Spacer(1, 0.06*cm))
                    if isinstance(cs, dict):
                        tip = cs.get("tip", cs.get("description",""))
                        if tip:
                            elements.append(Paragraph(_t(tip), S_BODY_SM))
                        exs = cs.get("examples", cs.get("example",[]))
                        if isinstance(exs, str): exs = [exs]
                        if isinstance(exs, list):
                            for ex in exs[:3]:
                                elements.append(Paragraph(_t(f"  > {ex}"), S_BODY_SM))
                    elements.append(_lines(2, "Bu stratejiyi kullanarak yazin:"))
                    elements.append(Spacer(1, 0.08*cm))

                # ── ICERIK BANKASI ETKINLIKLERI ──
                _ab_unit = _week_to_unit_ab(wn)
                _ab_day_banks = _DAY_CB_MAP.get(dk, [])
                _ab_cb_rows = []
                for _bk in _ab_day_banks:
                    _bdata = _cb_all.get(_bk, {}).get(_ab_unit)
                    if isinstance(_bdata, list) and _bdata:
                        _bdata = _bdata[0] if isinstance(_bdata[0], dict) else {"text": str(_bdata[0])}
                    if _bdata and isinstance(_bdata, dict):
                        _btitle = _get_cb_title(_bk, _bdata)
                        _btr = _CB_TR.get(_bk, _bk)
                        _ab_cb_rows.append((_btr, _btitle, _bdata, _bk))
                if _ab_cb_rows:
                    sn += 1
                    elements.append(_sec_hdr(f"{sn}. ICERIK BANKASI ETKINLIKLERI", C_TEAL))
                    elements.append(Spacer(1, 0.06*cm))
                    for _btr, _btitle, _bdata, _bk in _ab_cb_rows:
                        # Bank header row
                        elements.append(Paragraph(_t(f"<b>{_btr}:</b> {_btitle}"), S_BOLD_SM))
                        # Extract content based on bank type
                        if _bk == "story":
                            ep = _bdata.get("episode", "")
                            if ep:
                                elements.append(Paragraph(_t(ep[:300] + ("..." if len(ep)>300 else "")), S_BODY_SM))
                                elements.append(_lines(2, "Hikaye hakkinda yaz:"))
                        elif _bk in ("culture", "turkey", "funfacts"):
                            info_t = _bdata.get("info", _bdata.get("text", _bdata.get("content", "")))
                            if isinstance(info_t, str) and info_t:
                                elements.append(Paragraph(_t(info_t[:250] + ("..." if len(str(info_t))>250 else "")), S_BODY_SM))
                            elif isinstance(info_t, list):
                                for _fi in info_t[:3]:
                                    elements.append(Paragraph(_t(f"  * {_fi}"), S_BODY_SM))
                            elements.append(_lines(2, "Notlarin:"))
                        elif _bk == "comic":
                            panels = _bdata.get("panels", [])
                            for _pi, _p in enumerate(panels[:3]):
                                _ptxt = _p.get("text", _p.get("dialogue", "")) if isinstance(_p, dict) else str(_p)
                                elements.append(Paragraph(_t(f"  Kare {_pi+1}: {_ptxt}"), S_BODY_SM))
                            elements.append(_lines(1, "Devamini yaz:"))
                        elif _bk == "writing":
                            wp = _bdata.get("prompt", _bdata.get("task", ""))
                            if wp:
                                elements.append(Paragraph(_t(f"Gorev: {wp}"), S_BODY_SM))
                            model = _bdata.get("model", _bdata.get("example", ""))
                            if model:
                                elements.append(Paragraph(_t(f"Ornek: {str(model)[:200]}"), S_BODY_SM))
                            elements.append(_lines(4, "Yazini buraya yaz:"))
                        elif _bk == "workbook":
                            exs = _bdata.get("exercises", _bdata.get("tasks", []))
                            if isinstance(exs, list):
                                for _ei, _ex in enumerate(exs[:3]):
                                    _etxt = _ex.get("instruction", _ex.get("q", str(_ex))) if isinstance(_ex, dict) else str(_ex)
                                    elements.append(Paragraph(_t(f"  {_ei+1}. {_etxt}"), S_BODY_SM))
                                    elements.append(_lines(1))
                        elif _bk in ("mission", "escape", "project"):
                            desc = _bdata.get("description", _bdata.get("scenario", _bdata.get("brief", "")))
                            if desc:
                                elements.append(Paragraph(_t(desc[:250]), S_BODY_SM))
                            steps = _bdata.get("steps", _bdata.get("tasks", _bdata.get("stages", [])))
                            if isinstance(steps, list):
                                for _si, _st in enumerate(steps[:4]):
                                    _stxt = _st.get("task", str(_st)) if isinstance(_st, dict) else str(_st)
                                    elements.append(Paragraph(_t(f"  {_si+1}. {_stxt}"), S_BODY_SM))
                            elements.append(_lines(2, "Notlar:"))
                        elif _bk == "sel":
                            topic = _bdata.get("topic", _bdata.get("theme", ""))
                            if topic:
                                elements.append(Paragraph(_t(f"Konu: {topic}"), S_BODY_SM))
                            activity = _bdata.get("activity", _bdata.get("discussion", ""))
                            if activity:
                                elements.append(Paragraph(_t(str(activity)[:200]), S_BODY_SM))
                            elements.append(_lines(2, "Duygu/Dusunce:"))
                        elif _bk == "family":
                            act = _bdata.get("activity", _bdata.get("task", ""))
                            if act:
                                elements.append(Paragraph(_t(str(act)[:200]), S_BODY_SM))
                            elements.append(_lines(2, "Aile ile birlikte:"))
                        elif _bk == "steam":
                            desc = _bdata.get("description", _bdata.get("experiment", ""))
                            if desc:
                                elements.append(Paragraph(_t(str(desc)[:250]), S_BODY_SM))
                            steps = _bdata.get("steps", [])
                            if isinstance(steps, list):
                                for _si, _st in enumerate(steps[:4]):
                                    _stxt = str(_st.get("step", _st)) if isinstance(_st, dict) else str(_st)
                                    elements.append(Paragraph(_t(f"  {_si+1}. {_stxt}"), S_BODY_SM))
                            elements.append(_lines(2, "Sonuc/Gozlem:"))
                        elif _bk == "podcast":
                            topic = _bdata.get("topic", _bdata.get("title", ""))
                            if topic:
                                elements.append(Paragraph(_t(f"Konu: {topic}"), S_BODY_SM))
                            qs = _bdata.get("discussion_questions", _bdata.get("questions", []))
                            if isinstance(qs, list):
                                for _qi, _q in enumerate(qs[:3]):
                                    elements.append(Paragraph(_t(f"  {_qi+1}. {_q}"), S_BODY_SM))
                            elements.append(_lines(2, "Cevaplarin:"))
                        elif _bk == "progress":
                            items = _bdata.get("items", _bdata.get("questions", _bdata.get("tasks", [])))
                            if isinstance(items, list):
                                for _qi, _q in enumerate(items[:5]):
                                    _qtxt = _q.get("q", str(_q)) if isinstance(_q, dict) else str(_q)
                                    elements.append(Paragraph(_t(f"  {_qi+1}. {_qtxt}"), S_BODY_SM))
                                    opts = _q.get("opts", []) if isinstance(_q, dict) else []
                                    if opts:
                                        elements.append(_mcq(_qtxt, opts, _qi+1))
                                    else:
                                        elements.append(_lines(1))
                        elif _bk == "pronunciation":
                            sounds = _bdata.get("sounds", _bdata.get("pairs", _bdata.get("words", [])))
                            if isinstance(sounds, list):
                                for _si in sounds[:6]:
                                    _stxt = str(_si.get("word", _si)) if isinstance(_si, dict) else str(_si)
                                    elements.append(Paragraph(_t(f"  * {_stxt}"), S_BODY_SM))
                        else:
                            txt = str(_bdata)[:200] if not isinstance(_bdata, dict) else ""
                            if txt:
                                elements.append(Paragraph(_t(txt), S_BODY_SM))
                        elements.append(Spacer(1, 0.06*cm))

                # Bos icerik fallback
                if sn == 0:
                    elements.append(_sec_hdr("CALISMA ALANI", sc_main))
                    elements.append(_lines(8, "Notlarinizi buraya yazin:"))

                # ── ALT BILGI ──
                if insts or mats:
                    elements.append(Spacer(1, 0.04*cm))
                    parts = []
                    if insts: parts.append(f"Araclar: {', '.join(insts[:5])}")
                    if mats: parts.append(f"Materyal: {' | '.join(mats[:3])}")
                    ft = Table([[Paragraph(_t("  |  ".join(parts)), S_BODY_XS)]],
                               colWidths=[pw], rowHeights=[11])
                    ft.setStyle(TableStyle([
                        ("BACKGROUND",(0,0),(0,0),C_LIGHT2),
                        ("LEFTPADDING",(0,0),(0,0),5),
                        ("TOPPADDING",(0,0),(0,0),1),
                        ("BOTTOMPADDING",(0,0),(0,0),1),
                        ("ROUNDEDCORNERS",[3,3,3,3]),
                    ]))
                    elements.append(ft)

                if tips:
                    elements.append(Spacer(1, 0.03*cm))
                    elements.append(Paragraph(_t(f"Ogretmen Notu: {tips}"), S_TIP))

                elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PDF BUILD
    # ═══════════════════════════════════════════════════════
    doc = SimpleDocTemplate(
        buf, pagesize=B5,
        leftMargin=M_IN, rightMargin=M_OUT,
        topMargin=M_TOP, bottomMargin=M_BOT,
        title=f"{glabel} Etkinlik Kitabi — Diamond 3D Premium Edition",
        author="SmartCampus AI",
    )

    _fl = glabel
    _fy = acad_year

    def _footer(canvas, doc):
        canvas.saveState()
        _pw, _ph = B5
        y = 0.9*cm
        # Alt gold cizgi
        canvas.setStrokeColor(rl.HexColor("#B8860B"))
        canvas.setLineWidth(0.8)
        canvas.line(M_IN, y+12, _pw-M_OUT, y+12)
        # Sol: branding
        canvas.setFont(fn, 5.5)
        canvas.setFillColor(rl.HexColor("#64748B"))
        canvas.drawString(M_IN, y+3,
                          f"SmartCampus AI  |  {_fl} Etkinlik Kitabi  |  Diamond 3D Premium  |  {_fy}")
        # Sag: sayfa
        canvas.drawRightString(_pw-M_OUT, y+3, f"{doc.page}")
        # Ust ince cizgi
        canvas.setStrokeColor(rl.HexColor("#232B3E"))
        canvas.setLineWidth(0.4)
        canvas.line(M_IN, _ph-M_TOP+0.2*cm, _pw-M_OUT, _ph-M_TOP+0.2*cm)
        canvas.restoreState()

    doc.build(elements, onFirstPage=_footer, onLaterPages=_footer)
    buf.seek(0)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════
# OKUL ONCESI ETKINLIK KITABI — Diamond 3D Premium Edition
# 36 Hafta x 10 Saat = 360 Etkinlik Sayfasi
# 5-6 Yas — Okuma yazma bilmeyen cocuklar icin gorsel etkinlikler
# ═══════════════════════════════════════════════════════════════════════

# Slot modeli: Pzt-Per (Ana Ders + Beceri Lab), Cuma (Native x2)
_PK_SLOT_MODEL = {
    "mon": [("ANA DERS", "green"), ("BECERI LAB", "purple")],
    "tue": [("ANA DERS", "green"), ("BECERI LAB", "purple")],
    "wed": [("ANA DERS", "green"), ("BECERI LAB", "purple")],
    "thu": [("ANA DERS", "green"), ("BECERI LAB", "purple")],
    "fri": [("NATIVE SPEAKER", "red"), ("NATIVE SPEAKER", "red")],
}

_PK_DAY_TR = {"mon": "Pazartesi", "tue": "Sali", "wed": "Carsamba",
              "thu": "Persembe", "fri": "Cuma"}

# Her gun+saat icin etkinlik sablonu (10 farkli tip, haftanin gunune/saatine gore)
_PK_ACTIVITY_TEMPLATES = {
    # (gun_key, saat_idx) -> etkinlik_tipi
    ("mon", 0): "flashcard_match",     # Ana Ders: Kelime tanitim + eslestirme
    ("mon", 1): "listen_and_sing",     # Beceri Lab: Sarki dinle tekrarla
    ("tue", 0): "tpr_action",          # Ana Ders: TPR hareket
    ("tue", 1): "memory_game",         # Beceri Lab: Hafiza oyunu / eslestirme
    ("wed", 0): "story_sequence",      # Ana Ders: Hikaye siralama
    ("wed", 1): "color_and_craft",     # Beceri Lab: Boyama / el isi
    ("thu", 0): "word_review",         # Ana Ders: Kelime tekrari + kalip
    ("thu", 1): "drama_movement",      # Beceri Lab: Drama / hareket
    ("fri", 0): "native_conversation", # Native: Serbest konusma
    ("fri", 1): "native_review",       # Native: Tekrar + sarki
}

# Etkinlik tiplerine gore gorsel icerik uretici
_PK_ACTIVITY_CONTENT = {
    "flashcard_match": {
        "title_tr": "GORSEL ESLESTIRME",
        "title_en": "Picture Match",
        "icon": "M",
        "instruction_tr": "Resmi bul ve dogru kelimeyle eslestir!",
        "sections": [
            ("Eslestir", "Resmi bul, yandaki kelimeyle cizgiyle birlestir."),
            ("Daire Icine Al", "Dogru resmi daire icine al."),
            ("Boya", "Kelimeyi soyle ve resmini boya."),
        ],
    },
    "listen_and_sing": {
        "title_tr": "DINLE VE SOYLE",
        "title_en": "Listen & Sing",
        "icon": "S",
        "instruction_tr": "Sarkiyi dinle, hareketleri yap ve tekrarla!",
        "sections": [
            ("Dinle ve Isaretle", "Sarkida gecen kelimelerin resimlerini isaretle."),
            ("Hareketler", "Her kelime icin hareketi yap."),
            ("Tekrarla", "Ogretmenin soyledigi kelimeleri tekrarla."),
        ],
    },
    "tpr_action": {
        "title_tr": "HAREKET ZAMANI",
        "title_en": "TPR Actions",
        "icon": "M",
        "instruction_tr": "Ogretmenin soyledigini yap! (Stand up, sit down, jump!)",
        "sections": [
            ("Komutu Dinle", "Ogretmen soyledi, sen yap!"),
            ("Goster", "Dokunarak kelimenin resmini bul."),
            ("Canlandir", "Kelimeyi vucudunla anlat."),
        ],
    },
    "memory_game": {
        "title_tr": "HAFIZA OYUNU",
        "title_en": "Memory Game",
        "icon": "S",
        "instruction_tr": "Kartlari esle! Ayni resimleri bul!",
        "sections": [
            ("Eslestir", "Ayni resimleri cizgiyle birlestir."),
            ("Hatirla", "Kapatilan 3 resimden hangisi eksik?"),
            ("Soyle", "Her resmi gosterip adini soyle."),
        ],
    },
    "story_sequence": {
        "title_tr": "HIKAYE SIRALAMA",
        "title_en": "Story Sequence",
        "icon": "M",
        "instruction_tr": "Hikayeyi dinle, resimleri dogru siraya koy!",
        "sections": [
            ("Dinle", "Hikayeyi dinle ve resimlere bak."),
            ("Sirala", "Resimlerin altina 1-2-3 yaz."),
            ("Anlat", "Resme bakarak hikayeyi kendi sozcuklerinle anlat."),
        ],
    },
    "color_and_craft": {
        "title_tr": "BOYA VE YARAT",
        "title_en": "Color & Craft",
        "icon": "S",
        "instruction_tr": "Temaya uygun boyama ve el isi etkinligi!",
        "sections": [
            ("Boya", "Resmi soylenen renkle boya."),
            ("Kes-Yapistir", "Resimleri kes ve dogru yere yapistir."),
            ("Ciz", "Ogrendigin kelimeyle ilgili resim ciz."),
        ],
    },
    "word_review": {
        "title_tr": "KELIME TEKRARI",
        "title_en": "Word Review",
        "icon": "M",
        "instruction_tr": "Bu haftanin kelimelerini tekrarla ve pratik yap!",
        "sections": [
            ("Soyle", "Her resme bakip kelimesini soyle."),
            ("Kalip Pratigi", "Kalip cumleyi tekrarla."),
            ("Daire Icine Al", "Dogru resmi bul ve daire icine al."),
        ],
    },
    "drama_movement": {
        "title_tr": "DRAMA VE HAREKET",
        "title_en": "Drama & Movement",
        "icon": "S",
        "instruction_tr": "Canlandir, hareket et, role-play yap!",
        "sections": [
            ("Rol Yap", "Arkadasinla dialog canlandir."),
            ("Hareket Et", "Kelimeleri hareketlerle goster."),
            ("Sinif Gezi", "Sinifta kelimelerin yazdigi kartlari bul."),
        ],
    },
    "native_conversation": {
        "title_tr": "NATIVE SPEAKER ILE KONUSMA",
        "title_en": "Native Conversation",
        "icon": "N",
        "instruction_tr": "Anadili Ingilizce olan ogretmenle konusma pratigi!",
        "sections": [
            ("Dinle", "Native speaker'i dinle, ne dedigini anlamaya calis."),
            ("Tekrarla", "Soylenen cumleleri tekrarla."),
            ("Soru-Cevap", "Basit sorulara cevap ver (Yes/No)."),
        ],
    },
    "native_review": {
        "title_tr": "NATIVE SPEAKER ILE TEKRAR",
        "title_en": "Native Review",
        "icon": "N",
        "instruction_tr": "Haftanin kelimelerini native speaker ile tekrarla ve sarki soyle!",
        "sections": [
            ("Kelime Tekrari", "Haftanin tum kelimelerini soyle."),
            ("Sarki", "Haftanin sarkisini birlikte soyle."),
            ("Oyun", "Kelime oyunu oyna (bul-dokun, at-yakala)."),
        ],
    },
}


def generate_preschool_activity_book_pdf(
    start_week: int = 1,
    end_week: int = 36,
    day_filter: str | None = None,
) -> bytes:
    """Okul oncesi etkinlik kitabi PDF — Diamond 3D Premium Edition.
    36 Hafta x 10 Saat = 360 Etkinlik Sayfasi.
    B5 baski-hazir format, ayni tasarim dili."""

    from reportlab.lib.pagesizes import B5
    from reportlab.lib import colors as rl
    from reportlab.lib.units import cm, mm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, PageBreak)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    try:
        from utils.shared_data import ensure_turkish_pdf_fonts
        from utils.report_utils import get_institution_info
        fn, fb = ensure_turkish_pdf_fonts()
        info = get_institution_info()
    except Exception:
        fn, fb = "Helvetica", "Helvetica-Bold"
        info = {}

    font_ok = fn != "Helvetica"

    def _t(text):
        if font_ok:
            return str(text)
        _m = {"\u0131":"i","\u0130":"I","\u011f":"g","\u011e":"G",
              "\u00fc":"u","\u00dc":"U","\u015f":"s","\u015e":"S",
              "\u00f6":"o","\u00d6":"O","\u00e7":"c","\u00c7":"C"}
        return str(text).translate(str.maketrans(_m))

    # Mufredat verisini yukle
    try:
        from views.yabanci_dil import _CURRICULUM_PRESCHOOL
    except Exception:
        return b""

    weeks_all = _CURRICULUM_PRESCHOOL
    if not weeks_all:
        return b""

    # Preschool content banks (grade 0)
    _pk_cb_all = _load_content_banks(0)

    sw = max(1, min(start_week, len(weeks_all)))
    ew = max(sw, min(end_week, len(weeks_all)))

    now_str = datetime.now().strftime("%d.%m.%Y")
    today = datetime.now().date()
    acad_s = today.year if today.month >= 9 else today.year - 1
    acad_year = f"{acad_s}-{acad_s+1}"
    kurum = info.get("name", "")

    buf = BytesIO()
    W, H = B5
    M_IN = 2.2 * cm
    M_OUT = 1.6 * cm
    M_TOP = 1.4 * cm
    M_BOT = 1.8 * cm
    pw = W - M_IN - M_OUT

    # Renk paleti — Amber aksanli (okul oncesi)
    C_NAVY     = rl.HexColor("#0B0F19")
    C_DARK     = rl.HexColor("#94A3B8")
    C_GOLD     = rl.HexColor("#B8860B")
    C_GOLD_L   = rl.HexColor("#DAA520")
    C_AMBER    = rl.HexColor("#D97706")
    C_AMBER_L  = rl.HexColor("#F59E0B")
    C_GREEN    = rl.HexColor("#1B7340")
    C_GREEN_L  = rl.HexColor("#2D9B5A")
    C_PURPLE   = rl.HexColor("#5B21B6")
    C_PURPLE_L = rl.HexColor("#7C3AED")
    C_RED      = rl.HexColor("#B91C1C")
    C_RED_L    = rl.HexColor("#DC2626")
    C_BLUE     = rl.HexColor("#1D4ED8")
    C_TEAL     = rl.HexColor("#0F766E")
    C_ORANGE   = rl.HexColor("#B45309")
    C_WHITE    = rl.white
    C_TEXT     = rl.HexColor("#1F2937")
    C_TEXT2    = rl.HexColor("#94A3B8")
    C_GRAY     = rl.HexColor("#94A3B8")
    C_GRAY_L   = rl.HexColor("#64748B")
    C_LIGHT    = rl.HexColor("#F9FAFB")
    C_LIGHT2   = rl.HexColor("#151B2B")
    C_BORDER   = rl.HexColor("#232B3E")
    C_CREAM    = rl.HexColor("#FFFBEB")
    C_MINT     = rl.HexColor("#ECFDF5")
    C_LAVEN    = rl.HexColor("#F5F3FF")
    C_ROSE     = rl.HexColor("#FFF1F2")
    C_SKY      = rl.HexColor("#E0F2FE")

    SLOT_C = {
        "green":  (C_GREEN, C_GREEN_L, C_MINT, "ANA DERS"),
        "purple": (C_PURPLE, C_PURPLE_L, C_LAVEN, "BECERI LAB"),
        "red":    (C_RED, C_RED_L, C_ROSE, "NATIVE SPEAKER"),
    }

    # Tipografi
    def _s(name, **kw):
        kw.setdefault("fontName", fn)
        kw.setdefault("fontSize", 9)
        kw.setdefault("leading", 13)
        kw.setdefault("textColor", C_TEXT)
        return ParagraphStyle(name, **kw)

    S_COV_TITLE = _s("ct", fontName=fb, fontSize=26, leading=32, alignment=TA_CENTER, textColor=C_WHITE)
    S_COV_SUB   = _s("cs", fontName=fb, fontSize=13, leading=17, alignment=TA_CENTER, textColor=C_AMBER_L)
    S_COV_INFO  = _s("ci", fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#232B3E"))
    S_TOC_H     = _s("th", fontName=fb, fontSize=13, leading=17, textColor=C_WHITE)
    S_TOC       = _s("tc", fontSize=8, leading=11)
    S_TOC_B     = _s("tb", fontName=fb, fontSize=8, leading=11)
    S_WK_NUM    = _s("wn", fontName=fb, fontSize=36, leading=40, alignment=TA_CENTER, textColor=C_WHITE)
    S_WK_THEME  = _s("wt", fontName=fb, fontSize=15, leading=19, alignment=TA_CENTER, textColor=C_AMBER_L)
    S_WK_INFO   = _s("wi", fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#232B3E"))
    S_PG_TITLE  = _s("pt", fontName=fb, fontSize=10, leading=13, textColor=C_WHITE)
    S_PG_SUB    = _s("ps", fontSize=7.5, leading=10, textColor=rl.HexColor("#232B3E"), alignment=TA_RIGHT)
    S_SEC       = _s("se", fontName=fb, fontSize=9, leading=12, textColor=C_WHITE)
    S_BODY      = _s("bo", fontSize=9, leading=13, alignment=TA_JUSTIFY)
    S_BODY_SM   = _s("bs", fontSize=8, leading=11.5)
    S_BODY_LG   = _s("bl", fontSize=14, leading=20)
    S_BODY_XS   = _s("bx", fontSize=7, leading=10, textColor=C_GRAY)
    S_BOLD      = _s("bd", fontName=fb, fontSize=9, leading=13)
    S_BOLD_SM   = _s("bds", fontName=fb, fontSize=8, leading=11.5)
    S_BOLD_LG   = _s("bdl", fontName=fb, fontSize=12, leading=16)
    S_ANS       = _s("an", fontSize=8, leading=20, textColor=C_GRAY_L)
    S_TIP       = _s("ti", fontSize=7, leading=10, textColor=C_ORANGE, leftIndent=8)
    S_EMOJI     = _s("em", fontSize=18, leading=24, alignment=TA_CENTER)
    S_WORD      = _s("wd", fontName=fb, fontSize=11, leading=15, alignment=TA_CENTER, textColor=C_TEXT)

    elements = []
    _day_order = [day_filter] if day_filter else ["mon", "tue", "wed", "thu", "fri"]

    # ── Yardimci fonksiyonlar ──
    def _rule(color=C_AMBER, thickness=1.5):
        t = Table([[""]], colWidths=[pw], rowHeights=[thickness])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),color),
            ("TOPPADDING",(0,0),(0,0),0),("BOTTOMPADDING",(0,0),(0,0),0),
        ]))
        return t

    def _sec_hdr(title, color, accent=C_AMBER):
        t = Table(
            [["", Paragraph(_t(f"<b>{title}</b>"), S_SEC)]],
            colWidths=[4, pw-4], rowHeights=[20])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),accent),
            ("BACKGROUND",(1,0),(1,0),color),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(1,0),(1,0),10),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("ROUNDEDCORNERS",[0,4,4,0]),
        ]))
        return t

    def _picture_card(word, emoji_char):
        """Buyuk emoji + kelime karti (5-6 yas icin gorsel)."""
        rows = [
            [Paragraph(emoji_char, S_EMOJI)],
            [Paragraph(_t(f"<b>{word}</b>"), S_WORD)],
        ]
        t = Table(rows, colWidths=[pw*0.22], rowHeights=[30, 18])
        t.setStyle(TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("BOX",(0,0),(-1,-1),0.8,C_BORDER),
            ("BACKGROUND",(0,0),(-1,-1),C_CREAM),
            ("ROUNDEDCORNERS",[6,6,6,6]),
            ("TOPPADDING",(0,0),(-1,-1),4),
            ("BOTTOMPADDING",(0,0),(-1,-1),2),
        ]))
        return t

    def _circle_task_row(words, emojis, instruction):
        """Daire icine alma / isaretleme gorevi — buyuk gorsel."""
        cells = []
        for w, e in zip(words[:4], emojis[:4]):
            cell_rows = [
                [Paragraph(e, _s("ce", fontSize=22, leading=28, alignment=TA_CENTER))],
                [Paragraph(_t(f"<b>{w}</b>"), _s("cw", fontName=fb, fontSize=10,
                           leading=14, alignment=TA_CENTER, textColor=C_TEXT))],
                [Paragraph("O", _s("co", fontSize=20, leading=24,
                           alignment=TA_CENTER, textColor=C_GRAY_L))],
            ]
            ct = Table(cell_rows, colWidths=[pw*0.22], rowHeights=[32, 16, 22])
            ct.setStyle(TableStyle([
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("BOX",(0,0),(-1,-1),0.6,C_BORDER),
                ("BACKGROUND",(0,0),(-1,-1),C_SKY),
                ("ROUNDEDCORNERS",[8,8,8,8]),
            ]))
            cells.append(ct)
        while len(cells) < 4:
            cells.append(Paragraph("", S_BODY))
        t = Table([cells], colWidths=[pw*0.24]*4)
        t.setStyle(TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ]))
        return t

    def _match_lines(left_items, right_items):
        """Sol-sag eslestirme (cizgi cekme) — gorsel."""
        rows = []
        for i in range(max(len(left_items), len(right_items))):
            l = left_items[i] if i < len(left_items) else ""
            r = right_items[i] if i < len(right_items) else ""
            rows.append([
                Paragraph(_t(f"<b>{l}</b>"), _s(f"ml{i}", fontName=fb, fontSize=11,
                          leading=15, alignment=TA_CENTER, textColor=C_TEXT)),
                Paragraph(_t("----------"), _s(f"md{i}", fontSize=8, leading=12,
                          alignment=TA_CENTER, textColor=C_GRAY_L)),
                Paragraph(r, _s(f"mr{i}", fontSize=18, leading=24,
                          alignment=TA_CENTER)),
            ])
        if rows:
            t = Table(rows, colWidths=[pw*0.3, pw*0.35, pw*0.3])
            t.setStyle(TableStyle([
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("TOPPADDING",(0,0),(-1,-1),4),
                ("BOTTOMPADDING",(0,0),(-1,-1),4),
                ("LINEBELOW",(0,0),(-1,-2),0.3,C_BORDER),
                ("BOX",(0,0),(-1,-1),0.5,C_BORDER),
                ("BACKGROUND",(0,0),(-1,-1),C_CREAM),
            ]))
            return t
        return Spacer(1, 0.1*cm)

    def _coloring_area(instruction, height=3.5):
        """Boyama / cizim alani — cerceveli bos alan."""
        rows = [
            [Paragraph(_t(f"<b>{instruction}</b>"), S_BOLD_SM)],
            [Spacer(1, height*cm)],
        ]
        t = Table(rows, colWidths=[pw])
        t.setStyle(TableStyle([
            ("BOX",(0,0),(-1,-1),1,C_AMBER),
            ("BACKGROUND",(0,1),(0,1),C_WHITE),
            ("BACKGROUND",(0,0),(0,0),C_CREAM),
            ("LEFTPADDING",(0,0),(-1,-1),8),
            ("TOPPADDING",(0,0),(0,0),6),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("ROUNDEDCORNERS",[8,8,8,8]),
        ]))
        return t

    def _sequence_boxes(n=3):
        """Siralama kutulari (1-2-3)."""
        cells = []
        for i in range(n):
            box = Table(
                [[Paragraph(_t(f"{i+1}"), _s(f"sb{i}", fontName=fb, fontSize=9,
                            leading=12, alignment=TA_CENTER, textColor=C_GRAY))],
                 [Spacer(1, 2*cm)]],
                colWidths=[pw/n - 0.3*cm],
            )
            box.setStyle(TableStyle([
                ("BOX",(0,0),(-1,-1),1,C_AMBER),
                ("BACKGROUND",(0,0),(-1,-1),C_WHITE),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("ROUNDEDCORNERS",[6,6,6,6]),
            ]))
            cells.append(box)
        t = Table([cells], colWidths=[pw/n]*n)
        t.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")]))
        return t

    # Emoji haritasi
    _WORD_EMOJI = {
        "hello":"(Hi!)", "goodbye":"(Bye!)", "yes":"(Yes)", "no":"(No)",
        "please":"(Pls)", "thank you":"(Thx)", "sorry":"(!)", "teacher":"(T)",
        "friend":"(F)", "name":"(N)", "old":"(#)", "I am":"(I)",
        "boy":"(B)", "girl":"(G)", "my":"(my)", "your":"(yr)", "how":"(?)",
        "red":"[R]", "blue":"[B]", "green":"[G]", "yellow":"[Y]",
        "orange":"[O]", "purple":"[P]", "pink":"[Pk]", "white":"[W]",
        "black":"[Bk]", "brown":"[Br]", "color":"[C]", "this is":"(=)",
        "what":"(?)", "look":"(>>)", "see":"(oo)",
        "one":"(1)", "two":"(2)", "three":"(3)", "four":"(4)", "five":"(5)",
        "six":"(6)", "seven":"(7)", "eight":"(8)", "nine":"(9)", "ten":"(10)",
        "cat":"(Cat)", "dog":"(Dog)", "bird":"(Bird)", "fish":"(Fish)",
        "rabbit":"(Rab)", "mouse":"(Mse)", "elephant":"(Elph)", "lion":"(Lion)",
        "bear":"(Bear)", "monkey":"(Mnk)", "horse":"(Hrs)", "cow":"(Cow)",
        "mother":"(Mom)", "father":"(Dad)", "sister":"(Sis)", "brother":"(Bro)",
        "baby":"(Bby)", "family":"(Fam)", "grandma":"(Gma)", "grandpa":"(Gpa)",
        "happy":"(Hpy)", "sad":"(Sad)", "angry":"(Ang)", "scared":"(Scr)",
        "tired":"(Trd)", "hungry":"(Hng)", "love":"(Luv)",
        "apple":"(Apl)", "banana":"(Bna)", "milk":"(Mlk)", "water":"(Wtr)",
        "bread":"(Brd)", "egg":"(Egg)", "juice":"(Jce)", "cookie":"(Cke)",
        "head":"(Hd)", "eye":"(Ey)", "ear":"(Er)", "nose":"(Ns)",
        "mouth":"(Mth)", "hand":"(Hnd)", "foot":"(Ft)", "body":"(Bd)",
        "big":"(BIG)", "small":"(sml)", "long":"(lng)", "short":"(srt)",
        "hot":"(HOT)", "cold":"(CLD)", "fast":"(FST)", "slow":"(SLW)",
        "sun":"(Sun)", "rain":"(Rn)", "cloud":"(Cld)", "wind":"(Wnd)",
        "snow":"(Snw)", "tree":"(Tre)", "flower":"(Flw)", "star":"(Str)",
        "car":"(Car)", "bus":"(Bus)", "bike":"(Bke)", "train":"(Trn)",
        "ball":"(Bal)", "doll":"(Dll)", "book":"(Bk)", "toy":"(Ty)",
        "house":"(Hse)", "door":"(Dr)", "window":"(Wdw)", "table":"(Tbl)",
        "chair":"(Chr)", "bed":"(Bed)", "cup":"(Cup)", "plate":"(Plt)",
        "shirt":"(Srt)", "pants":"(Pnt)", "shoes":"(She)", "hat":"(Hat)",
        "dress":"(Drs)", "jacket":"(Jkt)", "socks":"(Sox)", "bag":"(Bag)",
        "circle":"(O)", "square":"([])", "triangle":"(/\\)", "rectangle":"([=])",
        "morning":"(AM)", "night":"(PM)", "day":"(Day)", "sleep":"(Zzz)",
        "eat":"(Eat)", "drink":"(Drk)", "play":"(Ply)", "run":"(Run)",
        "walk":"(Wlk)", "jump":"(Jmp)", "dance":"(Dnc)", "swim":"(Swm)",
        "sing":"(Sng)", "draw":"(Drw)", "read":"(Rd)", "write":"(Wr)",
        "school":"(Sch)", "classroom":"(Cls)", "playground":"(Plg)", "park":"(Prk)",
    }

    def _emoji(word):
        return _WORD_EMOJI.get(word.lower(), _WORD_EMOJI.get(word, f"({word[:3]})"))

    # ═══════════════════════════════════════════════════════
    # KAPAK SAYFASI
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 2.5*cm))
    if kurum:
        elements.append(Paragraph(_t(kurum), _s(
            "kr", fontName=fb, fontSize=14, leading=18,
            textColor=C_TEXT, alignment=TA_CENTER, spaceAfter=4)))
    elements.append(Paragraph(_t(f"{acad_year} Egitim-Ogretim Yili"), _s(
        "yr", fontSize=10, leading=14, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=16)))
    elements.append(Spacer(1, 1*cm))
    elements.append(_rule(C_AMBER, 2))

    cv_rows = [
        [Paragraph(_t("DIAMOND 3D PREMIUM EDITION"), _s(
            "d3d", fontName=fb, fontSize=9, leading=12,
            textColor=C_AMBER_L, alignment=TA_CENTER, spaceBefore=4))],
        [Spacer(1,6)],
        [Paragraph(_t("ETKINLIK KITABI"), S_COV_TITLE)],
        [Paragraph(_t("ACTIVITY BOOK"), _s(
            "ab", fontSize=13, leading=17, textColor=rl.HexColor("#B9F2FF"),
            alignment=TA_CENTER))],
        [Spacer(1,8)],
        [Paragraph(_t("Okul Oncesi (5-6 Yas)"), S_COV_SUB)],
        [Paragraph(_t("CEFR Pre-A1 — Dil Farkindaligi"), S_COV_INFO)],
        [Spacer(1,6)],
        [Paragraph(_t(f"{ew-sw+1} Hafta  |  {(ew-sw+1)*len(_day_order)*2} Ders Saati  |  Gorsel Etkinlikler"
                      + (f"  |  {_PK_DAY_TR.get(day_filter,'')}" if day_filter else "")), _s(
            "det", fontSize=8, leading=11, textColor=rl.HexColor("#64748B"),
            alignment=TA_CENTER))],
    ]
    cv = Table(cv_rows, colWidths=[pw])
    cv.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_NAVY),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(0,0),16),
        ("BOTTOMPADDING",(0,-1),(0,-1),16),
    ]))
    elements.append(cv)
    elements.append(_rule(C_AMBER, 2))
    elements.append(Spacer(1, 1.2*cm))

    # Bilgi kutusu
    ib_rows = [
        [Paragraph(_t("Ana Ders (4 saat) + Beceri Lab (4 saat) + Native Speaker (2 saat)"), _s(
            "ib", fontName=fb, fontSize=8.5, leading=12, textColor=C_AMBER, alignment=TA_CENTER))],
        [Paragraph(_t("Gorsel, oyun tabanli, TPR destekli — Okuma yazma gerektirmeyen etkinlikler"), _s(
            "ib2", fontSize=7.5, leading=10.5, textColor=C_TEXT2, alignment=TA_CENTER))],
    ]
    ibt = Table(ib_rows, colWidths=[pw])
    ibt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CREAM),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("BOX",(0,0),(-1,-1),0.75,C_AMBER),
        ("TOPPADDING",(0,0),(0,0),8),
        ("BOTTOMPADDING",(0,-1),(0,-1),8),
        ("ROUNDEDCORNERS",[6,6,6,6]),
    ]))
    elements.append(ibt)
    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph(_t(now_str), _s(
        "dt", fontSize=8, leading=11, textColor=C_GRAY, alignment=TA_CENTER)))

    cp = []
    if info.get("address"): cp.append(info["address"])
    if info.get("phone"): cp.append(f"Tel: {info['phone']}")
    if info.get("web"): cp.append(info["web"])
    if cp:
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(_t(" | ".join(cp)), _s(
            "ct2", fontSize=6.5, leading=9, textColor=C_GRAY_L, alignment=TA_CENTER)))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # KUNYE
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 6*cm))
    kol_items = [
        f"<b>Kitap Adi:</b> Okul Oncesi Ingilizce Etkinlik Kitabi — Diamond 3D Premium Edition",
        f"<b>Seviye:</b> CEFR Pre-A1 | Okul Oncesi (5-6 Yas)",
        f"<b>Kapsam:</b> 36 Hafta, 360 Ders Saati, Gorsel Etkinlikler",
        f"<b>Ders Modeli:</b> Ana Ders (4h) + Beceri Lab (4h) + Native Speaker (2h)",
        f"<b>Yaklasim:</b> TPR, Oyun Tabanli, Gorsel-Isitsel, Okuma Yazma Gerektirmeyen",
        f"<b>Akademik Yil:</b> {acad_year}",
        f"<b>Uretim Tarihi:</b> {now_str}",
        f"<b>Platform:</b> SmartCampus AI — Akilli Kampus Egitim Yonetim Sistemi",
    ]
    if kurum:
        kol_items.insert(0, f"<b>Kurum:</b> {kurum}")
    for ki in kol_items:
        elements.append(Paragraph(_t(ki), _s("kl", fontSize=8, leading=13, textColor=C_TEXT2)))
        elements.append(Spacer(1, 0.1*cm))
    elements.append(Spacer(1, 1*cm))
    elements.append(_rule(C_BORDER, 0.5))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(
        _t("Bu kitap SmartCampus AI platformu tarafindan otomatik olarak uretilmistir. "
           "Icerikler 5-6 yas grubu okul oncesi ogrencilerin dil farkindaligi ve temel "
           "Ingilizce becerilerini gelistirmeye yonelik gorsel, oyun tabanli ve TPR "
           "yaklasimli etkinliklerden olusmaktadir. Okuma-yazma gerektirmez."),
        _s("kl2", fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_JUSTIFY)))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # ICINDEKILER
    # ═══════════════════════════════════════════════════════
    toc_hdr = Table(
        [["", Paragraph(_t("<b>ICINDEKILER</b>"), S_TOC_H)]],
        colWidths=[4, pw-4], rowHeights=[26])
    toc_hdr.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),C_AMBER),
        ("BACKGROUND",(1,0),(1,0),C_NAVY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(1,0),(1,0),12),
        ("ROUNDEDCORNERS",[0,6,6,0]),
    ]))
    elements.append(toc_hdr)
    elements.append(Spacer(1, 0.4*cm))

    toc_rows = []
    for wi in range(sw-1, ew):
        wk = weeks_all[wi]
        wn = wk.get("week", wi+1)
        vocab = wk.get("vocab", [])
        toc_rows.append([
            Paragraph(_t(f"<b>Hafta {wn}</b>"), S_TOC_B),
            Paragraph(_t(wk.get("theme_tr", "")), S_TOC),
            Paragraph(_t(f"({wk.get('theme', '')})"), _s(f"te{wn}", fontSize=7, leading=10, textColor=C_GRAY)),
            Paragraph(_t(f"{len(vocab)} kelime"), _s(f"tv{wn}", fontSize=7, leading=10, textColor=C_PURPLE)),
        ])
    if toc_rows:
        tt = Table(toc_rows, colWidths=[pw*.12, pw*.35, pw*.33, pw*.20])
        ts = [
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LINEBELOW",(0,0),(-1,-2),0.3,C_BORDER),
        ]
        for ri in range(len(toc_rows)):
            if ri % 2 == 0:
                ts.append(("BACKGROUND",(0,ri),(-1,ri),C_LIGHT))
        tt.setStyle(TableStyle(ts))
        elements.append(tt)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # HAFTA SAYFALARI
    # ═══════════════════════════════════════════════════════
    for wi in range(sw-1, ew):
        wk = weeks_all[wi]
        wn = wk.get("week", wi+1)
        theme = wk.get("theme", "")
        theme_tr = wk.get("theme_tr", "")
        vocab = wk.get("vocab", [])
        structure = wk.get("structure", "")
        skills = wk.get("skills", {})
        assessment = wk.get("assessment", "")
        wdays = wk.get("days", {})

        # ── HAFTA KAPAK SAYFASI ──
        elements.append(Spacer(1, 3*cm))
        elements.append(_rule(C_AMBER, 2))

        wk_cv = [
            [Paragraph(_t("HAFTA"), _s(f"wl{wn}", fontName=fb, fontSize=10,
                        leading=13, textColor=C_AMBER_L, alignment=TA_CENTER))],
            [Paragraph(_t(f"{wn}"), S_WK_NUM)],
            [Spacer(1, 4)],
            [Paragraph(_t(theme_tr), S_WK_THEME)],
            [Paragraph(_t(theme), _s(f"wte{wn}", fontSize=11, leading=15,
                        textColor=rl.HexColor("#232B3E"), alignment=TA_CENTER))],
            [Spacer(1, 8)],
            [Paragraph(_t(f"Kelimeler: {', '.join(vocab[:6])}"), S_WK_INFO)],
            [Paragraph(_t(f"Kalip: {structure}  |  10 Ders Saati  |  5 Gun"), _s(
                f"wci{wn}", fontSize=8.5, leading=12, textColor=C_GRAY_L, alignment=TA_CENTER))],
        ]
        wct = Table(wk_cv, colWidths=[pw])
        wct.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_NAVY),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(0,0),20),
            ("BOTTOMPADDING",(0,-1),(0,-1),20),
        ]))
        elements.append(wct)
        elements.append(_rule(C_AMBER, 2))

        # Hafta ders dagitim tablosu
        elements.append(Spacer(1, 0.6*cm))
        dist_hdr = [
            Paragraph(_t("<b>Gun</b>"), S_BOLD_SM),
            Paragraph(_t("<b>1. Saat (Ana Ders / Native)</b>"), S_BOLD_SM),
            Paragraph(_t("<b>2. Saat (Beceri Lab / Native)</b>"), S_BOLD_SM),
        ]
        dist_rows = [dist_hdr]
        for dk in _day_order:
            dd = wdays.get(dk, [])
            dn = _PK_DAY_TR.get(dk, dk)
            if isinstance(dd, list):
                h1 = dd[0][:55] if len(dd) > 0 else ""
                h2 = dd[1][:55] if len(dd) > 1 else ""
            else:
                h1, h2 = str(dd)[:55], ""
            # Prefix kaldir
            for pfx in ["Ana Ders: ", "Beceri Lab: ", "Native Speaker: "]:
                h1 = h1.replace(pfx, "", 1) if h1.startswith(pfx) else h1
                h2 = h2.replace(pfx, "", 1) if h2.startswith(pfx) else h2
            dist_rows.append([
                Paragraph(_t(f"<b>{dn}</b>"), S_BOLD_SM),
                Paragraph(_t(h1), S_BODY_XS),
                Paragraph(_t(h2), S_BODY_XS),
            ])
        dtt = Table(dist_rows, colWidths=[pw*.16, pw*.42, pw*.42])
        dts = [
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),4),
            ("TOPPADDING",(0,0),(-1,-1),2),
            ("BOTTOMPADDING",(0,0),(-1,-1),2),
            ("BACKGROUND",(0,0),(-1,0),C_DARK),
            ("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
            ("BOX",(0,0),(-1,-1),0.5,C_BORDER),
            ("INNERGRID",(0,0),(-1,-1),0.3,C_BORDER),
        ]
        for ri in range(1, len(dist_rows)):
            if ri % 2 == 0:
                dts.append(("BACKGROUND",(0,ri),(-1,ri),C_LIGHT))
            if ri == len(dist_rows)-1:
                dts.append(("BACKGROUND",(0,ri),(-1,ri),C_ROSE))
        dtt.setStyle(TableStyle(dts))
        elements.append(dtt)

        # Beceri hedefleri
        elements.append(Spacer(1, 0.3*cm))
        sk_rows = [
            [Paragraph(_t("<b>Beceri</b>"), S_BOLD_SM),
             Paragraph(_t("<b>Hedef</b>"), S_BOLD_SM)],
        ]
        for sk_name, sk_key in [("Dinleme", "listening"), ("Konusma", "speaking"),
                                 ("On-Okuma", "pre_reading"), ("On-Yazma", "pre_writing")]:
            sv = skills.get(sk_key, "")
            if sv and sv != "-":
                sk_rows.append([
                    Paragraph(_t(f"<b>{sk_name}</b>"), S_BOLD_SM),
                    Paragraph(_t(sv), S_BODY_SM),
                ])
        if len(sk_rows) > 1:
            skt = Table(sk_rows, colWidths=[pw*0.2, pw*0.8])
            skt.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),C_AMBER),
                ("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("LEFTPADDING",(0,0),(-1,-1),5),
                ("TOPPADDING",(0,0),(-1,-1),2),
                ("BOTTOMPADDING",(0,0),(-1,-1),2),
                ("BOX",(0,0),(-1,-1),0.5,C_BORDER),
                ("INNERGRID",(0,0),(-1,-1),0.3,C_BORDER),
            ]))
            elements.append(skt)

        elements.append(PageBreak())

        # ── HER SAAT ICIN ETKINLIK SAYFALARI (10 saat) ──
        gh = 0
        for dk in _day_order:
            dd = wdays.get(dk, [])
            dn = _PK_DAY_TR.get(dk, dk)
            slots = _PK_SLOT_MODEL.get(dk, [])

            for si, (slot_name, slot_color) in enumerate(slots):
                gh += 1
                sc_main, sc_light, sc_bg, sc_label = SLOT_C.get(slot_color, SLOT_C["green"])
                act_type = _PK_ACTIVITY_TEMPLATES.get((dk, si), "flashcard_match")
                act_info = _PK_ACTIVITY_CONTENT.get(act_type, _PK_ACTIVITY_CONTENT["flashcard_match"])

                # Ders icerigini al
                if isinstance(dd, list) and si < len(dd):
                    lesson_text = dd[si]
                    for pfx in ["Ana Ders: ", "Beceri Lab: ", "Native Speaker: "]:
                        if lesson_text.startswith(pfx):
                            lesson_text = lesson_text[len(pfx):]
                            break
                else:
                    lesson_text = ""

                # ── SAYFA UST KUNYE ──
                elements.append(_rule(C_AMBER, 1.5))

                hdr_l = Paragraph(_t(f"<b>Hafta {wn}  |  {dn}  |  Saat {gh}</b>"), S_PG_TITLE)
                hdr_r = Paragraph(_t(f"Okul Oncesi  |  Pre-A1  |  40 dk"), S_PG_SUB)
                hdr = Table([[hdr_l, hdr_r]], colWidths=[pw*.6, pw*.4], rowHeights=[20])
                hdr.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,-1),sc_main),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("LEFTPADDING",(0,0),(0,0),8),
                    ("RIGHTPADDING",(1,0),(1,0),8),
                    ("TOPPADDING",(0,0),(-1,-1),3),
                    ("BOTTOMPADDING",(0,0),(-1,-1),3),
                ]))
                elements.append(hdr)

                # Slot + Tema bilgi bandi
                info_l = Paragraph(_t(f"<b>{sc_label}</b>  |  {theme_tr} ({theme})"), S_BODY_XS)
                info_r = Paragraph(_t(f"Kalip: {structure}"),
                                   _s(f"ir{gh}", fontSize=6.5, leading=9, textColor=C_GRAY, alignment=TA_RIGHT))
                ib = Table([[info_l, info_r]], colWidths=[pw*.6, pw*.4], rowHeights=[13])
                ib.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,-1),sc_bg),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("LEFTPADDING",(0,0),(0,0),8),
                    ("RIGHTPADDING",(1,0),(1,0),8),
                    ("TOPPADDING",(0,0),(-1,-1),1),
                    ("BOTTOMPADDING",(0,0),(-1,-1),1),
                ]))
                elements.append(ib)
                elements.append(_rule(C_AMBER, 0.75))

                # Ad Soyad
                elements.append(Spacer(1, 0.15*cm))
                nr = Table([
                    [Paragraph(_t("Ad Soyad: ____________________________________"), S_BODY_SM),
                     Paragraph(_t("Tarih: ___/___/______"),
                               _s(f"nr{gh}", fontSize=7.5, leading=10, textColor=C_TEXT, alignment=TA_RIGHT))]
                ], colWidths=[pw*.6, pw*.4], rowHeights=[13])
                nr.setStyle(TableStyle([
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("LINEBELOW",(0,0),(-1,-1),0.4,C_BORDER),
                ]))
                elements.append(nr)
                elements.append(Spacer(1, 0.15*cm))

                # ── ETKINLIK BASLIGI ──
                elements.append(_sec_hdr(
                    f"{act_info['title_tr']} — {act_info['title_en']}", sc_main))
                elements.append(Spacer(1, 0.06*cm))

                # Yonerge
                elements.append(Paragraph(
                    _t(f"<b>Yonerge:</b> {act_info['instruction_tr']}"), S_BOLD_SM))
                elements.append(Spacer(1, 0.08*cm))

                # ── DERS AKISI ──
                elements.append(_sec_hdr("DERS ICERIGI", C_DARK))
                elements.append(Spacer(1, 0.04*cm))
                elements.append(Paragraph(_t(lesson_text), S_BODY_SM))
                elements.append(Spacer(1, 0.12*cm))

                # ── KELIME KARTLARI (tum saatlerde) ──
                elements.append(_sec_hdr(f"HAFTANIN KELIMELERI — {theme_tr}", C_AMBER))
                elements.append(Spacer(1, 0.06*cm))

                # 4'lu gorsel kart gridi
                v_cards = []
                for v in vocab[:8]:
                    em = _emoji(v)
                    v_cards.append(_picture_card(v, em))

                # 4'lu satirlar
                for row_start in range(0, len(v_cards), 4):
                    row = v_cards[row_start:row_start+4]
                    while len(row) < 4:
                        row.append(Paragraph("", S_BODY))
                    t = Table([row], colWidths=[pw*0.24]*4)
                    t.setStyle(TableStyle([
                        ("ALIGN",(0,0),(-1,-1),"CENTER"),
                        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ]))
                    elements.append(t)
                    elements.append(Spacer(1, 0.08*cm))

                # ── ETKINLIK TURU BAZLI ICERIK ──
                if act_type == "flashcard_match":
                    # Eslestirme etkinligi
                    elements.append(_sec_hdr("ESLESTIRME ETKINLIGI", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Kelimeyi resmiyle eslestir — cizgi cek!</b>"), S_BOLD_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    # Karistir ve eslestir
                    import random as _rnd
                    left = vocab[:5]
                    right_e = [_emoji(v) for v in left]
                    _rnd.seed(wn * 100 + gh)
                    right_shuffled = right_e[:]
                    _rnd.shuffle(right_shuffled)
                    elements.append(_match_lines(left, right_shuffled))

                elif act_type == "listen_and_sing":
                    # Sarki dinle isaretle
                    elements.append(_sec_hdr("DINLE VE ISARETLE", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Sarkida hangi kelimeleri duydun? Isaretini koy!</b>"), S_BOLD_SM))
                    emojis = [_emoji(v) for v in vocab[:4]]
                    elements.append(_circle_task_row(vocab[:4], emojis,
                        "Duydugun kelimeyi daire icine al."))
                    elements.append(Spacer(1, 0.1*cm))
                    elements.append(_sec_hdr("HAREKETLER", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    for i, v in enumerate(vocab[:4]):
                        elements.append(Paragraph(
                            _t(f"<b>{i+1}.</b> \"{v}\" duyunca > _____________________________ (hareketi yaz/ciz)"),
                            S_BODY_SM))
                        elements.append(Spacer(1, 0.04*cm))

                elif act_type == "tpr_action":
                    # TPR hareket etkinligi
                    elements.append(_sec_hdr("TPR — HAREKET ET!", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    tpr_cmds = [
                        f"Stand up and say '{vocab[0] if vocab else 'hello'}'!",
                        f"Touch something '{vocab[1] if len(vocab)>1 else 'blue'}'!",
                        f"Point to '{vocab[2] if len(vocab)>2 else 'the door'}'!",
                        f"Jump and say '{vocab[3] if len(vocab)>3 else 'yes'}'!",
                    ]
                    for i, cmd in enumerate(tpr_cmds):
                        elements.append(Paragraph(
                            _t(f"<b>{i+1}.</b> {cmd}  [  ]"), S_BODY))
                        elements.append(Spacer(1, 0.04*cm))
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(Paragraph(
                        _t("<b>Dogru kelimenin resmini daire icine al:</b>"), S_BOLD_SM))
                    emojis = [_emoji(v) for v in vocab[:4]]
                    elements.append(_circle_task_row(vocab[:4], emojis, ""))

                elif act_type == "memory_game":
                    # Hafiza eslestirme
                    elements.append(_sec_hdr("HAFIZA ESLESTIRME OYUNU", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Ayni resimleri bul ve cizgiyle birlestir!</b>"), S_BOLD_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    left_m = vocab[:4]
                    right_m = [_emoji(v) for v in left_m]
                    import random as _rnd2
                    _rnd2.seed(wn * 200 + gh)
                    right_m_s = right_m[:]
                    _rnd2.shuffle(right_m_s)
                    elements.append(_match_lines(
                        [_emoji(v) for v in left_m], [v.upper() for v in left_m]))
                    elements.append(Spacer(1, 0.1*cm))
                    elements.append(Paragraph(
                        _t("<b>Eksik resmi ciz:</b> 3 resimden biri kapali — hangisi?"), S_BOLD_SM))
                    elements.append(_coloring_area("Eksik resmi buraya ciz:", 2.5))

                elif act_type == "story_sequence":
                    # Hikaye siralama
                    elements.append(_sec_hdr("HIKAYE SIRALAMA", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Hikayeyi dinle, resimleri dogru siraya koy! (1-2-3)</b>"), S_BOLD_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    elements.append(_sequence_boxes(3))
                    elements.append(Spacer(1, 0.1*cm))
                    elements.append(_sec_hdr("HIKAYEYI ANLAT", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t(f"<b>Tema:</b> {theme_tr} ({theme})"), S_BODY))
                    elements.append(Paragraph(
                        _t("<b>Resme bak ve hikayeyi kendi sozlerinle anlat.</b>"), S_BOLD_SM))
                    elements.append(_coloring_area(
                        f"Hikayeden en sevdigin sahneyi ciz: {theme_tr}", 3))

                elif act_type == "color_and_craft":
                    # Boyama ve el isi
                    elements.append(_sec_hdr("BOYA VE YARAT", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    if len(vocab) > 2:
                        elements.append(Paragraph(
                            _t(f"<b>'{vocab[0]}' resmini boya, '{vocab[1]}' resmini kes-yapistir!</b>"),
                            S_BOLD_SM))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(_coloring_area(
                        f"{theme_tr} temali resim boya:", 4))
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(_sec_hdr("KES VE YAPISTIR", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Asagidaki resimleri kes ve dogru kutuya yapistir:</b>"), S_BOLD_SM))
                    elements.append(_sequence_boxes(4))

                elif act_type == "word_review":
                    # Kelime tekrari
                    elements.append(_sec_hdr("KELIME TEKRARI", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Her resme bak ve kelimesini soyle!</b>"), S_BOLD_SM))
                    emojis = [_emoji(v) for v in vocab[:4]]
                    elements.append(_circle_task_row(vocab[:4], emojis,
                        "Soyledigini ogretmene isaretle."))
                    elements.append(Spacer(1, 0.1*cm))
                    elements.append(_sec_hdr(f"KALIP PRATIGI: {structure}", C_GREEN))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t(f"<b>Kalibi tekrarla:</b> {structure}"), S_BOLD))
                    for i, v in enumerate(vocab[:4]):
                        elements.append(Paragraph(
                            _t(f"  {i+1}. {structure.split('/')[0].strip()} _______ ({v})"),
                            S_BODY))
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(Paragraph(
                        _t("<b>Dogru eslestirmeyi bul:</b>"), S_BOLD_SM))
                    elements.append(_match_lines(
                        vocab[:4], [_emoji(v) for v in vocab[:4]]))

                elif act_type == "drama_movement":
                    # Drama ve hareket
                    elements.append(_sec_hdr("DRAMA VE ROL YAPMA", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t(f"<b>Arkadasinla '{theme_tr}' konusunda dialog canlandir!</b>"),
                        S_BOLD_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    elements.append(Paragraph(_t("Ogrenci A: ________________________________"), S_ANS))
                    elements.append(Paragraph(_t("Ogrenci B: ________________________________"), S_ANS))
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(_sec_hdr("SINIF ICINDE BUL!", C_PURPLE))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Sinifta dolasip kelimelerin yazili oldugu kartlari bul ve isaretle:</b>"),
                        S_BOLD_SM))
                    for i, v in enumerate(vocab[:5]):
                        elements.append(Paragraph(
                            _t(f"  [  ]  {v}  —  Buldum!"), S_BODY))
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(_coloring_area(
                        f"Canlandirdigin sahneyi ciz:", 2.5))

                elif act_type == "native_conversation":
                    # Native speaker ile konusma
                    elements.append(_sec_hdr("NATIVE SPEAKER ILE KONUSMA", C_RED))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Native speaker'i dinle ve tekrarla!</b>"), S_BOLD_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    elements.append(Paragraph(
                        _t(f"<b>Konu:</b> {theme_tr} ({theme})"), S_BODY))
                    elements.append(Spacer(1, 0.06*cm))
                    qs = [
                        f"Do you know '{vocab[0] if vocab else 'hello'}'?  [Yes] [No]",
                        f"Can you say '{vocab[1] if len(vocab)>1 else 'goodbye'}'?  [Yes] [No]",
                        f"Show me '{vocab[2] if len(vocab)>2 else 'red'}'!  [Did it]",
                    ]
                    for i, q in enumerate(qs):
                        elements.append(Paragraph(_t(f"<b>{i+1}.</b> {q}"), S_BODY))
                        elements.append(Spacer(1, 0.04*cm))
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(Paragraph(
                        _t("<b>Soru-Cevap:</b> Native speaker soruyor, sen cevapla!"), S_BOLD_SM))
                    elements.append(Paragraph(
                        _t("Q: ________________________________"), S_ANS))
                    elements.append(Paragraph(
                        _t("A: ________________________________"), S_ANS))

                elif act_type == "native_review":
                    # Native speaker ile tekrar
                    elements.append(_sec_hdr("HAFTALIK TEKRAR VE SARKI", C_RED))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(Paragraph(
                        _t("<b>Haftanin tum kelimelerini soyle!</b>"), S_BOLD_SM))
                    elements.append(Spacer(1, 0.04*cm))
                    for i, v in enumerate(vocab[:6]):
                        em = _emoji(v)
                        elements.append(Paragraph(
                            _t(f"  {i+1}. {em}  {v}  [Soyledim: ___]"), S_BODY))
                    elements.append(Spacer(1, 0.08*cm))
                    lc = wk.get("linked_content", {})
                    songs = lc.get("songs", [])
                    elements.append(_sec_hdr("SARKI ZAMANI", C_RED))
                    elements.append(Spacer(1, 0.06*cm))
                    if songs:
                        elements.append(Paragraph(
                            _t(f"<b>Sarki:</b> {songs[0]}"), S_BOLD))
                    elements.append(Paragraph(
                        _t("<b>Sarkiyi soyle ve hareketleri yap!</b>"), S_BOLD_SM))
                    elements.append(Spacer(1, 0.06*cm))
                    elements.append(_coloring_area("Sarki sirasindaki en sevdigin ani ciz:", 2.5))

                # ── ICERIK BANKASI ETKINLIKLERI (Okul Oncesi) ──
                _pk_unit = _week_to_unit_ab(wn)
                _pk_day_banks = _DAY_CB_MAP.get(dk, [])
                _pk_cb_items = []
                for _bk in _pk_day_banks:
                    _bdata = _pk_cb_all.get(_bk, {}).get(_pk_unit)
                    if isinstance(_bdata, list) and _bdata:
                        _bdata = _bdata[0] if isinstance(_bdata[0], dict) else {"text": str(_bdata[0])}
                    if _bdata and isinstance(_bdata, dict):
                        _btitle = _get_cb_title(_bk, _bdata)
                        _btr = _CB_TR.get(_bk, _bk)
                        _pk_cb_items.append((_btr, _btitle, _bdata, _bk))
                if _pk_cb_items:
                    elements.append(Spacer(1, 0.08*cm))
                    elements.append(_sec_hdr("ICERIK BANKASI", C_TEAL))
                    elements.append(Spacer(1, 0.04*cm))
                    for _btr, _btitle, _bdata, _bk in _pk_cb_items:
                        elements.append(Paragraph(_t(f"<b>{_btr}:</b> {_btitle}"), S_BOLD_SM))
                        if _bk == "story":
                            ep = _bdata.get("episode", "")
                            if ep:
                                elements.append(Paragraph(_t(ep[:200] + ("..." if len(ep)>200 else "")), S_BODY_SM))
                        elif _bk in ("culture", "turkey", "funfacts"):
                            info_t = _bdata.get("info", _bdata.get("text", _bdata.get("content", "")))
                            if isinstance(info_t, str) and info_t:
                                elements.append(Paragraph(_t(info_t[:200]), S_BODY_SM))
                            elif isinstance(info_t, list):
                                for _fi in info_t[:2]:
                                    elements.append(Paragraph(_t(f"  * {_fi}"), S_BODY_SM))
                        elif _bk == "sel":
                            topic = _bdata.get("topic", _bdata.get("theme", ""))
                            if topic:
                                elements.append(Paragraph(_t(f"Konu: {topic}"), S_BODY_SM))
                        elif _bk == "family":
                            act = _bdata.get("activity", _bdata.get("task", ""))
                            if act:
                                elements.append(Paragraph(_t(str(act)[:150]), S_BODY_SM))
                        elif _bk == "steam":
                            desc = _bdata.get("description", _bdata.get("experiment", ""))
                            if desc:
                                elements.append(Paragraph(_t(str(desc)[:150]), S_BODY_SM))
                        elif _bk in ("mission", "escape", "project"):
                            desc = _bdata.get("description", _bdata.get("scenario", _bdata.get("brief", "")))
                            if desc:
                                elements.append(Paragraph(_t(str(desc)[:150]), S_BODY_SM))
                        elif _bk == "podcast":
                            topic = _bdata.get("topic", _bdata.get("title", ""))
                            if topic:
                                elements.append(Paragraph(_t(f"Konu: {topic}"), S_BODY_SM))
                        elif _bk == "progress":
                            items = _bdata.get("items", _bdata.get("questions", []))
                            if isinstance(items, list):
                                for _qi, _q in enumerate(items[:3]):
                                    _qtxt = _q.get("q", str(_q)) if isinstance(_q, dict) else str(_q)
                                    elements.append(Paragraph(_t(f"  {_qi+1}. {_qtxt}"), S_BODY_SM))
                        else:
                            txt = _bdata.get("title", _bdata.get("topic", ""))
                            if txt:
                                elements.append(Paragraph(_t(str(txt)[:100]), S_BODY_SM))
                        elements.append(Spacer(1, 0.04*cm))

                # ── DEGERLENDIRME NOTU ──
                elements.append(Spacer(1, 0.1*cm))
                eval_rows = [
                    [Paragraph(_t("<b>Ogretmen Degerlendirmesi</b>"), _s(
                        f"ev{gh}", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE))],
                    [Table([
                        [Paragraph(_t("Cok Iyi"), _s(f"e1{gh}", fontName=fb, fontSize=7,
                                   leading=10, alignment=TA_CENTER, textColor=C_GREEN)),
                         Paragraph(_t("Iyi"), _s(f"e2{gh}", fontName=fb, fontSize=7,
                                   leading=10, alignment=TA_CENTER, textColor=C_BLUE)),
                         Paragraph(_t("Gelisiyor"), _s(f"e3{gh}", fontName=fb, fontSize=7,
                                   leading=10, alignment=TA_CENTER, textColor=C_ORANGE)),
                         Paragraph(_t("Destek"), _s(f"e4{gh}", fontName=fb, fontSize=7,
                                   leading=10, alignment=TA_CENTER, textColor=C_RED))],
                        [Paragraph("O", _s(f"r1{gh}", fontSize=14, leading=18,
                                   alignment=TA_CENTER, textColor=C_GRAY_L)),
                         Paragraph("O", _s(f"r2{gh}", fontSize=14, leading=18,
                                   alignment=TA_CENTER, textColor=C_GRAY_L)),
                         Paragraph("O", _s(f"r3{gh}", fontSize=14, leading=18,
                                   alignment=TA_CENTER, textColor=C_GRAY_L)),
                         Paragraph("O", _s(f"r4{gh}", fontSize=14, leading=18,
                                   alignment=TA_CENTER, textColor=C_GRAY_L))],
                    ], colWidths=[pw*0.24]*4)],
                ]
                evt = Table(eval_rows, colWidths=[pw])
                evt.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(0,0),C_DARK),
                    ("BOX",(0,0),(-1,-1),0.5,C_BORDER),
                    ("TOPPADDING",(0,0),(-1,-1),3),
                    ("BOTTOMPADDING",(0,0),(-1,-1),3),
                    ("ROUNDEDCORNERS",[4,4,4,4]),
                ]))
                elements.append(evt)

                elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PDF BUILD
    # ═══════════════════════════════════════════════════════
    doc = SimpleDocTemplate(
        buf, pagesize=B5,
        leftMargin=M_IN, rightMargin=M_OUT,
        topMargin=M_TOP, bottomMargin=M_BOT,
        title="Okul Oncesi Etkinlik Kitabi — Diamond 3D Premium Edition",
        author="SmartCampus AI",
    )

    def _footer(canvas, doc):
        canvas.saveState()
        _pw, _ph = B5
        y = 0.9*cm
        canvas.setStrokeColor(rl.HexColor("#D97706"))
        canvas.setLineWidth(0.8)
        canvas.line(M_IN, y+12, _pw-M_OUT, y+12)
        canvas.setFont(fn, 5.5)
        canvas.setFillColor(rl.HexColor("#64748B"))
        canvas.drawString(M_IN, y+3,
                          f"SmartCampus AI  |  Okul Oncesi Etkinlik Kitabi  |  Diamond 3D Premium  |  {acad_year}")
        canvas.drawRightString(_pw-M_OUT, y+3, f"{doc.page}")
        canvas.setStrokeColor(rl.HexColor("#232B3E"))
        canvas.setLineWidth(0.4)
        canvas.line(M_IN, _ph-M_TOP+0.2*cm, _pw-M_OUT, _ph-M_TOP+0.2*cm)
        canvas.restoreState()

    doc.build(elements, onFirstPage=_footer, onLaterPages=_footer)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "pk":
        sw = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        ew = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        print(f"Generating Preschool Activity Book, Weeks {sw}-{ew}...")
        pdf = generate_preschool_activity_book_pdf(sw, ew)
        out = f"etkinlik_kitabi_okul_oncesi_H{sw}-{ew}_premium.pdf"
        with open(out, "wb") as f:
            f.write(pdf)
        print(f"Done! {len(pdf)} bytes -> {out}")
    else:
        grade = sys.argv[1] if len(sys.argv) > 1 else "3"
        sw = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        ew = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        print(f"Generating Activity Book for Grade {grade}, Weeks {sw}-{ew}...")
        pdf = generate_activity_book_pdf(grade, sw, ew)
        out = f"etkinlik_kitabi_grade{grade}_H{sw}-{ew}_premium.pdf"
        with open(out, "wb") as f:
            f.write(pdf)
        print(f"Done! {len(pdf)} bytes -> {out}")
