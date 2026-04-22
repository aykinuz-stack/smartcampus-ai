"""
10 Saatlik Haftalik Ders Plani PDF Generator — Diamond 3D Premium Edition
=========================================================================
Baskiya hazir, kitap standartinda mizanpaj:
- B5 (176x250mm) kitap boyutu
- Ic/dis margin (sirt payi) ile cilt uyumu
- Profesyonel tipografi: baslik hiyerarsisi, satir araligi
- Tutarli renk paleti, gorsel hiyerarsi
- Hafta kapak sayfalari, unite kapak sayfalari
- Sayfa numaralama, ust/alt bilgi bandi
- Her hafta: 5 gun x 2 saat = 10 ders saati detayli plani
"""
from __future__ import annotations
import json, os
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


_GRADE_INFO = {
    "1": {"label": "1. Sinif", "cefr": "A1.1", "school": "Ilkokul"},
    "2": {"label": "2. Sinif", "cefr": "A1.2", "school": "Ilkokul"},
    "3": {"label": "3. Sinif", "cefr": "A1.3", "school": "Ilkokul"},
    "4": {"label": "4. Sinif", "cefr": "A1+",  "school": "Ilkokul"},
    "5": {"label": "5. Sinif", "cefr": "A2.1", "school": "Ortaokul"},
    "6": {"label": "6. Sinif", "cefr": "A2.2", "school": "Ortaokul"},
    "7": {"label": "7. Sinif", "cefr": "A2.3", "school": "Ortaokul"},
    "8": {"label": "8. Sinif", "cefr": "A2.4", "school": "Ortaokul"},
}

_SLOT_META = {
    "MAIN COURSE":    {"tr": "ANA DERS",          "icon": "M", "hue": "green"},
    "SKILLS LAB":     {"tr": "BECERI LABORATUVARI", "icon": "S", "hue": "purple"},
    "NATIVE SPEAKER": {"tr": "ANADILI INGILIZCE",  "icon": "N", "hue": "red"},
}

_DAY_TR = {
    "mon": "Pazartesi", "tue": "Sali", "wed": "Carsamba",
    "thu": "Persembe", "fri": "Cuma",
}
_DAY_ORDER = ["mon", "tue", "wed", "thu", "fri"]

_PHASE_TR = {
    "Tanitim": "Tanitim", "Gelistirme": "Gelistirme",
    "Pekistirme": "Pekistirme", "Degerlendirme": "Degerlendirme",
}


# ─────────────────────────────────────────────────────────────────
# CONTENT BANK LOADER (Grade-specific content for daily plans)
# ─────────────────────────────────────────────────────────────────

_CB_BANK_NAMES = [
    ("STORY_BANK", "Hikaye", "story"),
    ("CULTURE_CORNER_BANK", "Kultur Kosesi", "culture"),
    ("TURKEY_CORNER_BANK", "Turkiye Kosesi", "turkey"),
    ("COMIC_STRIP_BANK", "Cizgi Roman", "comic"),
    ("MISSION_BANK", "Gorev", "mission"),
    ("ESCAPE_ROOM_BANK", "Kacis Odasi", "escape"),
    ("FAMILY_CORNER_BANK", "Aile Kosesi", "family"),
    ("SEL_BANK", "SEL", "sel"),
    ("STEAM_BANK", "STEAM", "steam"),
    ("PODCAST_BANK", "Podcast", "podcast"),
    ("PROJECT_BANK", "Proje", "project"),
    ("FUN_FACTS_BANK", "Ilginc Bilgiler", "funfacts"),
    ("PROGRESS_CHECK_BANK", "Ilerleme Kontrolu", "progress"),
    ("MODEL_WRITING_BANK", "Yazma Modeli", "writing"),
    ("WORKBOOK_BANK", "Calisma Kitabi", "workbook"),
    ("PRONUNCIATION_BANK", "Telaffuz", "pronunciation"),
]

# Day -> which content bank types to show in PDF
_DAY_CB_MAP = {
    "mon": ["story", "culture", "pronunciation"],
    "tue": ["podcast", "comic", "turkey"],
    "wed": ["writing", "workbook", "steam"],
    "thu": ["project", "sel", "family"],
    "fri": ["escape", "funfacts", "progress", "mission"],
}


def _load_cb_for_grade(grade_num: int) -> dict:
    """Content bank verilerini grade dosyasindan yukler. Returns {bank_key: {unit: data}}"""
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
            _banks_map = {
                "story": _STORY_BANK, "culture": _CULTURE_CORNER_BANK,
                "turkey": _TURKEY_CORNER_BANK, "comic": _COMIC_STRIP_BANK,
                "mission": _MISSION_BANK, "escape": _ESCAPE_ROOM_BANK,
                "family": _FAMILY_CORNER_BANK, "sel": _SEL_BANK,
                "steam": _STEAM_BANK, "podcast": _PODCAST_BANK,
                "project": _PROJECT_BANK, "funfacts": _FUN_FACTS_BANK,
                "progress": _PROGRESS_CHECK_BANK, "writing": _MODEL_WRITING_BANK,
                "workbook": _WORKBOOK_BANK, "pronunciation": _PRONUNCIATION_BANK,
            }
        else:
            mod = __import__(f"views.content_banks.grade{grade_num}", fromlist=["__all__"])
            _banks_map = {}
            for attr_name, _tr, key in _CB_BANK_NAMES:
                bank = getattr(mod, attr_name, None)
                if bank and isinstance(bank, dict):
                    _banks_map[key] = bank
        for key, bank in _banks_map.items():
            grade_data = bank.get(grade_num, bank)
            if isinstance(grade_data, dict) and any(isinstance(k, int) for k in grade_data.keys()):
                result[key] = grade_data
    except Exception:
        pass
    return result


def _week_to_unit(week_num: int) -> int:
    """Hafta numarasini unite numarasina cevirir (1-10)."""
    if week_num <= 0:
        return 1
    _breaks = [4, 7, 11, 14, 18, 22, 25, 29, 32, 37]
    for i, brk in enumerate(_breaks):
        if week_num < brk:
            return i + 1
    return 10


def _get_cb_title(data: dict) -> str:
    """Content bank verisinden baslik cikarir."""
    if not data or not isinstance(data, dict):
        return ""
    return str(data.get("title", data.get("topic", data.get("mission", ""))))[:50]


# ─────────────────────────────────────────────────────────────────
# BASKI-HAZIR PDF GENERATOR
# ─────────────────────────────────────────────────────────────────
def generate_weekly_plan_pdf(
    grade_key: str,
    start_week: int = 1,
    end_week: int = 36,
) -> bytes:
    from reportlab.lib.pagesizes import B5
    from reportlab.lib import colors as rl
    from reportlab.lib.units import cm, mm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, PageBreak,
                                     KeepTogether)
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
        _m = {"\u0131": "i", "\u0130": "I", "\u011f": "g", "\u011e": "G",
              "\u00fc": "u", "\u00dc": "U", "\u015f": "s", "\u015e": "S",
              "\u00f6": "o", "\u00d6": "O", "\u00e7": "c", "\u00c7": "C"}
        return str(text).translate(str.maketrans(_m))

    wp_all = _load_weekly_plans()
    weeks = wp_all.get(grade_key, [])
    if not weeks:
        return b""

    gi = _GRADE_INFO.get(grade_key, {})
    glabel = gi.get("label", f"{grade_key}. Sinif")
    cefr = gi.get("cefr", "")
    school = gi.get("school", "")
    now_str = datetime.now().strftime("%d.%m.%Y")
    today = datetime.now().date()
    acad_s = today.year if today.month >= 9 else today.year - 1
    acad_year = f"{acad_s}-{acad_s + 1}"
    kurum = info.get("name", "")

    # Content bank verilerini yukle
    _grade_int = int(grade_key) if grade_key.isdigit() else 0
    _cb_data = _load_cb_for_grade(_grade_int)

    buf = BytesIO()
    W, H = B5  # 176mm x 250mm

    # Kitap cilt payi
    M_IN = 2.2 * cm
    M_OUT = 1.6 * cm
    M_TOP = 1.4 * cm
    M_BOT = 1.8 * cm
    pw = W - M_IN - M_OUT

    # ── RENK PALETI — Baski uyumlu CMYK-yakin ──
    C_BLACK    = rl.HexColor("#1a1a2e")
    C_NAVY     = rl.HexColor("#0B0F19")
    C_DARK     = rl.HexColor("#94A3B8")
    C_GOLD     = rl.HexColor("#B8860B")
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
    C_BLUE_BG  = rl.HexColor("#EFF6FF")

    SLOT_C = {
        "green":  (C_GREEN, C_GREEN_L, C_MINT),
        "purple": (C_PURPLE, C_PURPLE_L, C_LAVEN),
        "red":    (C_RED, C_RED_L, C_ROSE),
    }

    DAY_COLORS = {
        "mon": C_BLUE, "tue": C_GREEN, "wed": C_PURPLE,
        "thu": C_ORANGE, "fri": C_RED,
    }

    # ── TIPOGRAFI ──
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
    # Section
    S_SEC       = _s("se", fontName=fb, fontSize=9, leading=12, textColor=C_WHITE)
    S_SEC_SM    = _s("ss", fontName=fb, fontSize=8, leading=11, textColor=C_WHITE)
    # Govde
    S_BODY      = _s("bo", fontSize=9, leading=13, alignment=TA_JUSTIFY)
    S_BODY_SM   = _s("bs", fontSize=8, leading=11.5)
    S_BODY_XS   = _s("bx", fontSize=7, leading=10, textColor=C_GRAY)
    S_BOLD      = _s("bd", fontName=fb, fontSize=9, leading=13)
    S_BOLD_SM   = _s("bds", fontName=fb, fontSize=8, leading=11.5)
    S_BOLD_XS   = _s("bdx", fontName=fb, fontSize=7, leading=10)
    S_CELL_W    = _s("cw", fontSize=7.5, leading=10, textColor=C_WHITE)
    S_CELL_WB   = _s("cwb", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)
    S_FOOTER    = _s("ft", fontSize=6, leading=8, textColor=C_GRAY_L)

    elements = []

    # ═══════════════════════════════════════════════════════
    # YARDIMCI FONKSIYONLAR
    # ═══════════════════════════════════════════════════════
    def _rule(color=C_GOLD, thickness=1.5):
        t = Table([[""]], colWidths=[pw], rowHeights=[thickness])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), color),
            ("TOPPADDING", (0, 0), (0, 0), 0),
            ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ]))
        return t

    def _sec_hdr(title, color, accent=C_GOLD):
        t = Table(
            [["", Paragraph(_t(f"<b>{title}</b>"), S_SEC)]],
            colWidths=[4, pw - 4], rowHeights=[20])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), accent),
            ("BACKGROUND", (1, 0), (1, 0), color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("ROUNDEDCORNERS", [0, 4, 4, 0]),
        ]))
        return t

    def _mini_hdr(title, color):
        t = Table(
            [["", Paragraph(_t(f"<b>{title}</b>"), S_SEC_SM)]],
            colWidths=[3, pw - 3], rowHeights=[16])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), C_GOLD),
            ("BACKGROUND", (1, 0), (1, 0), color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (1, 0), (1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("ROUNDEDCORNERS", [0, 3, 3, 0]),
        ]))
        return t

    def _info_pill(text, bg=C_LIGHT2, tc=C_TEXT2, fs=7):
        t = Table([[Paragraph(_t(text), _s("ip", fontSize=fs, leading=fs + 3, textColor=tc))]],
                  colWidths=[pw], rowHeights=[fs + 6])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), bg),
            ("LEFTPADDING", (0, 0), (0, 0), 6),
            ("TOPPADDING", (0, 0), (0, 0), 1),
            ("BOTTOMPADDING", (0, 0), (0, 0), 1),
            ("ROUNDEDCORNERS", [3, 3, 3, 3]),
        ]))
        return t

    # ═══════════════════════════════════════════════════════
    # KAPAK SAYFASI
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 2.5 * cm))

    if kurum:
        elements.append(Paragraph(_t(kurum), _s(
            "kr", fontName=fb, fontSize=14, leading=18,
            textColor=C_TEXT, alignment=TA_CENTER, spaceAfter=4)))
    elements.append(Paragraph(_t(f"{acad_year} Egitim-Ogretim Yili"), _s(
        "yr", fontSize=10, leading=14, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=16)))

    elements.append(Spacer(1, 1 * cm))
    elements.append(_rule(C_GOLD, 2))

    # Ana baslik blogu
    cv_rows = [
        [Paragraph(_t("DIAMOND 3D PREMIUM EDITION"), _s(
            "d3d", fontName=fb, fontSize=9, leading=12,
            textColor=C_GOLD_L, alignment=TA_CENTER, spaceBefore=4))],
        [Spacer(1, 6)],
        [Paragraph(_t("HAFTALIK DERS PLANI"), S_COV_TITLE)],
        [Paragraph(_t("10 SAATLIK WEEKLY LESSON PLAN"), _s(
            "wlp", fontSize=13, leading=17, textColor=rl.HexColor("#B9F2FF"),
            alignment=TA_CENTER))],
        [Spacer(1, 8)],
        [Paragraph(_t(f"{glabel} — {school}"), S_COV_SUB)],
        [Paragraph(_t(f"CEFR {cefr}"), S_COV_INFO)],
        [Spacer(1, 6)],
        [Paragraph(_t("36 Hafta  |  360 Ders Saati  |  5 Gun/Hafta  |  2x40dk/Gun"), _s(
            "det", fontSize=8, leading=11, textColor=rl.HexColor("#64748B"),
            alignment=TA_CENTER))],
    ]
    cv = Table(cv_rows, colWidths=[pw])
    cv.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (0, 0), 16),
        ("BOTTOMPADDING", (0, -1), (0, -1), 16),
    ]))
    elements.append(cv)
    elements.append(_rule(C_GOLD, 2))

    elements.append(Spacer(1, 1.2 * cm))

    # Bilgi kutusu
    ib_rows = [
        [Paragraph(_t("Main Course (4 saat) + Skills Lab (4 saat) + Native Speaker (2 saat)"), _s(
            "ib", fontName=fb, fontSize=8.5, leading=12, textColor=C_GOLD, alignment=TA_CENTER))],
        [Paragraph(_t("Haftalik 10 saat, 4 fazli unite dongusu, 5 gun detayli ders plani"), _s(
            "ib2", fontSize=7.5, leading=10.5, textColor=C_TEXT2, alignment=TA_CENTER))],
    ]
    ibt = Table(ib_rows, colWidths=[pw])
    ibt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_CREAM),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.75, C_GOLD),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, -1), (0, -1), 8),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    elements.append(ibt)

    elements.append(Spacer(1, 1.5 * cm))
    elements.append(Paragraph(_t(now_str), _s(
        "dt", fontSize=8, leading=11, textColor=C_GRAY, alignment=TA_CENTER)))

    cp = []
    if info.get("address"):
        cp.append(info["address"])
    if info.get("phone"):
        cp.append(f"Tel: {info['phone']}")
    if info.get("web"):
        cp.append(info["web"])
    if cp:
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(_t(" | ".join(cp)), _s(
            "ct2", fontSize=6.5, leading=9, textColor=C_GRAY_L, alignment=TA_CENTER)))

    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # KUNYE / KOLOFON SAYFASI
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 6 * cm))
    kol_items = [
        f"<b>Kitap Adi:</b> {glabel} Ingilizce Haftalik Ders Plani — Diamond 3D Premium Edition",
        f"<b>Seviye:</b> CEFR {cefr} | {school}",
        f"<b>Kapsam:</b> 36 Hafta, 360 Ders Saati, 5 Gun/Hafta",
        f"<b>Ders Modeli:</b> Main Course (4h) + Skills Lab (4h) + Native Speaker (2h)",
        f"<b>Akademik Yil:</b> {acad_year}",
        f"<b>Uretim Tarihi:</b> {now_str}",
        f"<b>Platform:</b> SmartCampus AI — Akilli Kampus Egitim Yonetim Sistemi",
    ]
    if kurum:
        kol_items.insert(0, f"<b>Kurum:</b> {kurum}")
    for ki in kol_items:
        elements.append(Paragraph(_t(ki), _s("kl", fontSize=8, leading=13, textColor=C_TEXT2)))
        elements.append(Spacer(1, 0.1 * cm))
    elements.append(Spacer(1, 1 * cm))
    elements.append(_rule(C_BORDER, 0.5))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(
        _t("Bu kitap SmartCampus AI platformu tarafindan otomatik olarak uretilmistir. "
           "Icerikler MEB mufredat kazanimlarina ve CEFR dil cercevesine uygun olarak "
           "haftalik ders planlariyla es gudumlu hazirlanmistir. Her hafta 10 ders saati "
           "detayli etkinlik akisi, materyal ve arac bilgisi ile birlikte sunulmaktadir."),
        _s("kl2", fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_JUSTIFY)))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # ICINDEKILER
    # ═══════════════════════════════════════════════════════
    sw = max(1, min(start_week, len(weeks)))
    ew = max(sw, min(end_week, len(weeks)))

    toc_hdr = Table(
        [["", Paragraph(_t("<b>ICINDEKILER</b>"), S_TOC_H)]],
        colWidths=[4, pw - 4], rowHeights=[26])
    toc_hdr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), C_GOLD),
        ("BACKGROUND", (1, 0), (1, 0), C_NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("ROUNDEDCORNERS", [0, 6, 6, 0]),
    ]))
    elements.append(toc_hdr)
    elements.append(Spacer(1, 0.4 * cm))

    toc_rows = []
    for wi in range(sw - 1, ew):
        wk = weeks[wi]
        wn = wk.get("week", wi + 1)
        toc_rows.append([
            Paragraph(_t(f"<b>Hafta {wn}</b>"), S_TOC_B),
            Paragraph(_t(f"Unite {wk.get('unit', 1)}: {wk.get('unit_theme_tr', '')}"), S_TOC),
            Paragraph(_t(f"({wk.get('unit_theme', '')})"), _s(f"te{wn}", fontSize=7, leading=10, textColor=C_GRAY)),
            Paragraph(_t(wk.get("phase", "")), _s(f"tp{wn}", fontSize=7, leading=10, textColor=C_PURPLE)),
        ])
    if toc_rows:
        tt = Table(toc_rows, colWidths=[pw * .12, pw * .38, pw * .3, pw * .2])
        ts = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, C_BORDER),
        ]
        for ri in range(len(toc_rows)):
            if ri % 2 == 0:
                ts.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
        tt.setStyle(TableStyle(ts))
        elements.append(tt)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # HAFTA SAYFALARI
    # ═══════════════════════════════════════════════════════
    for wi in range(sw - 1, ew):
        wk = weeks[wi]
        wn = wk.get("week", wi + 1)
        unit_n = wk.get("unit", 1)
        theme = wk.get("unit_theme", "")
        theme_tr = wk.get("unit_theme_tr", "")
        phase = wk.get("phase", "")
        phase_en = wk.get("phase_en", "")
        gram = wk.get("grammar_focus", "")
        wdays = wk.get("days", {})
        summary = wk.get("summary", {})

        # ══════════════════════════════════════════════
        # HAFTA KAPAK SAYFASI
        # ══════════════════════════════════════════════
        elements.append(Spacer(1, 3 * cm))
        elements.append(_rule(C_GOLD, 2))

        wk_cv = [
            [Paragraph(_t("HAFTA"), _s(f"wl{wn}", fontName=fb, fontSize=10,
                        leading=13, textColor=C_GOLD_L, alignment=TA_CENTER))],
            [Paragraph(_t(f"{wn}"), S_WK_NUM)],
            [Spacer(1, 4)],
            [Paragraph(_t(f"Unite {unit_n}: {theme_tr}"), S_WK_THEME)],
            [Paragraph(_t(theme), _s(f"wte{wn}", fontSize=11, leading=15,
                        textColor=rl.HexColor("#232B3E"), alignment=TA_CENTER))],
            [Spacer(1, 8)],
            [Paragraph(_t(f"{_PHASE_TR.get(phase, phase)}  |  Gramer: {gram}"), S_WK_INFO)],
            [Paragraph(_t(f"CEFR {cefr}  |  10 Ders Saati  |  5 Gun  |  2x40dk"), _s(
                f"wci{wn}", fontSize=8.5, leading=12, textColor=C_GRAY_L, alignment=TA_CENTER))],
        ]
        wct = Table(wk_cv, colWidths=[pw])
        wct.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (0, 0), 20),
            ("BOTTOMPADDING", (0, -1), (0, -1), 20),
        ]))
        elements.append(wct)
        elements.append(_rule(C_GOLD, 2))

        # Hafta ozet tablosu
        elements.append(Spacer(1, 0.6 * cm))
        dist_hdr = [
            Paragraph(_t("<b>Gun</b>"), _s("dh1", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Slot</b>"), _s("dh2", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>1. Saat</b>"), _s("dh3", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>2. Saat</b>"), _s("dh4", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
        ]
        dist_rows = [dist_hdr]
        for dk in _DAY_ORDER:
            dd = wdays.get(dk, {})
            dn = dd.get("day_name", _DAY_TR.get(dk, dk))
            hrs = dd.get("hours", [])
            h1_focus = hrs[0].get("focus", "") if len(hrs) > 0 else ""
            h2_focus = hrs[1].get("focus", "") if len(hrs) > 1 else ""
            slot_name = hrs[0].get("slot", "MAIN COURSE") if len(hrs) > 0 else ""
            slot_short = _SLOT_META.get(slot_name, {}).get("tr", slot_name)[:10]
            dist_rows.append([
                Paragraph(_t(f"<b>{dn}</b>"), S_BOLD_XS),
                Paragraph(_t(slot_short), S_BODY_XS),
                Paragraph(_t(h1_focus[:45]), S_BODY_XS),
                Paragraph(_t(h2_focus[:45]), S_BODY_XS),
            ])
        dtt = Table(dist_rows, colWidths=[pw * .16, pw * .16, pw * .34, pw * .34])
        dts = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("BACKGROUND", (0, 0), (-1, 0), C_DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
            ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER),
        ]
        for ri in range(1, len(dist_rows)):
            if ri % 2 == 0:
                dts.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
            if ri == len(dist_rows) - 1:
                dts.append(("BACKGROUND", (0, ri), (-1, ri), C_ROSE))
        dtt.setStyle(TableStyle(dts))
        elements.append(dtt)

        # Hafta ozet bilgileri
        if summary:
            elements.append(Spacer(1, 0.3 * cm))
            main_h = summary.get("main_course_hours", 4)
            skills_h = summary.get("skills_lab_hours", 4)
            native_h = summary.get("native_speaker_hours", 2)
            total_h = summary.get("total_hours", 10)

            sum_data = [[
                Paragraph(_t(f"<b>Ana Ders:</b> {main_h}s"), _s("sm1", fontName=fn, fontSize=7, leading=10, textColor=C_GREEN)),
                Paragraph(_t(f"<b>Beceri Lab:</b> {skills_h}s"), _s("sm2", fontName=fn, fontSize=7, leading=10, textColor=C_PURPLE)),
                Paragraph(_t(f"<b>Native:</b> {native_h}s"), _s("sm3", fontName=fn, fontSize=7, leading=10, textColor=C_RED)),
                Paragraph(_t(f"<b>Toplam:</b> {total_h}s"), _s("sm4", fontName=fb, fontSize=7, leading=10, textColor=C_GOLD)),
            ]]
            sumt = Table(sum_data, colWidths=[pw * .27, pw * .27, pw * .23, pw * .23])
            sumt.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_CREAM),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOX", (0, 0), (-1, -1), 0.5, C_GOLD),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ]))
            elements.append(sumt)

        elements.append(PageBreak())

        # ══════════════════════════════════════════════
        # GUNLUK DETAYLI PLAN SAYFALARI
        # ══════════════════════════════════════════════
        gh = 0
        for dk in _DAY_ORDER:
            dd = wdays.get(dk, {})
            dn = dd.get("day_name", _DAY_TR.get(dk, dk))
            hrs = dd.get("hours", [])
            day_color = DAY_COLORS.get(dk, C_BLUE)

            if not hrs:
                continue

            # ── GUN BASLIK BANDI ──
            elements.append(_rule(C_GOLD, 1.5))

            day_hdr_l = Paragraph(_t(f"<b>HAFTA {wn}  |  {dn}</b>"), S_PG_TITLE)
            day_hdr_r = Paragraph(_t(f"{glabel}  |  CEFR {cefr}  |  2x40dk"), S_PG_SUB)
            day_hdr = Table([[day_hdr_l, day_hdr_r]], colWidths=[pw * .55, pw * .45], rowHeights=[22])
            day_hdr.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), day_color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("RIGHTPADDING", (1, 0), (1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            elements.append(day_hdr)

            # Unite + Faz bilgi bandi
            info_txt = f"Unite {unit_n}: {theme_tr}  ({theme})  |  {_PHASE_TR.get(phase, phase)}  |  Gramer: {gram}"
            ib = Table([[Paragraph(_t(info_txt), S_BODY_XS)]], colWidths=[pw], rowHeights=[13])
            ib.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), C_BLUE_BG),
                ("LEFTPADDING", (0, 0), (0, 0), 8),
                ("TOPPADDING", (0, 0), (0, 0), 1),
                ("BOTTOMPADDING", (0, 0), (0, 0), 1),
            ]))
            elements.append(ib)
            elements.append(_rule(C_GOLD, 0.75))
            elements.append(Spacer(1, 0.15 * cm))

            # ── HER SAAT DETAYI ──
            for hi, h in enumerate(hrs):
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
                sc_main, sc_light, sc_bg = SLOT_C.get(sc_key, SLOT_C["green"])

                # Saat baslik
                h_lbl = f"{hi + 1}. DERS — {sm['tr']} ({dur})"
                elements.append(_mini_hdr(h_lbl, sc_main))
                elements.append(Spacer(1, 0.06 * cm))

                # Ders odagi
                elements.append(_info_pill(f"<b>Odak:</b> {focus}", sc_bg, C_TEXT))
                elements.append(Spacer(1, 0.08 * cm))

                # Etkinlik akisi
                if acts:
                    a_rows = []
                    for ai, a in enumerate(acts):
                        a_rows.append([
                            Paragraph(_t(f"<b>{ai + 1}</b>"), _s(
                                f"an{gh}_{ai}", fontName=fb, fontSize=7, leading=10,
                                textColor=sc_main, alignment=TA_CENTER)),
                            Paragraph(_t(a), S_BODY_SM),
                        ])
                    at = Table(a_rows, colWidths=[0.5 * cm, pw - 0.5 * cm])
                    a_style = [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                        ("LINEBELOW", (0, 0), (-1, -2), 0.2, C_BORDER),
                    ]
                    for ri in range(len(a_rows)):
                        if ri % 2 == 0:
                            a_style.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
                    at.setStyle(TableStyle(a_style))
                    elements.append(at)
                    elements.append(Spacer(1, 0.06 * cm))

                # Araclar + Materyaller
                bottom_parts = []
                if insts:
                    bottom_parts.append(f"<b>Araclar:</b> {', '.join(insts[:6])}")
                if mats:
                    bottom_parts.append(f"<b>Materyal:</b> {' | '.join(mats[:4])}")
                if bottom_parts:
                    bp_text = "  |  ".join(bottom_parts)
                    elements.append(_info_pill(bp_text, C_LIGHT2, C_GRAY, 6.5))
                    elements.append(Spacer(1, 0.04 * cm))

                # Ogretmen notu
                if tips:
                    elements.append(Paragraph(
                        _t(f"<b>Ogretmen Notu:</b> {tips}"),
                        _s(f"tip{gh}", fontSize=6.5, leading=9, textColor=C_ORANGE, leftIndent=6)))
                    elements.append(Spacer(1, 0.04 * cm))

                # Saat arasi bosluk
                elements.append(Spacer(1, 0.12 * cm))

            # ── CONTENT BANK ETKINLIKLERI ──
            _unit_num = _week_to_unit(wn)
            _day_banks = _DAY_CB_MAP.get(dk, [])
            _cb_rows = []
            _cb_tr_map = {b[2]: b[1] for b in _CB_BANK_NAMES}
            for _bk in _day_banks:
                _bdata = _cb_data.get(_bk, {}).get(_unit_num)
                if _bdata:
                    _btitle = _get_cb_title(_bdata)
                    _blabel = _cb_tr_map.get(_bk, _bk)
                    _cb_rows.append([
                        Paragraph(_t(f"<b>{_blabel}</b>"), _s(
                            f"cbl{wn}{dk}{_bk}", fontName=fb, fontSize=6.5,
                            leading=9, textColor=C_TEAL)),
                        Paragraph(_t(_btitle), _s(
                            f"cbt{wn}{dk}{_bk}", fontSize=6.5, leading=9,
                            textColor=C_TEXT2)),
                    ])
            if _cb_rows:
                elements.append(Spacer(1, 0.08 * cm))
                _cb_hdr = Table(
                    [[Paragraph(_t("<b>ICERIK BANKASI ETKINLIKLERI</b>"),
                                _s(f"cbh{wn}{dk}", fontName=fb, fontSize=6.5,
                                   leading=9, textColor=C_WHITE))]],
                    colWidths=[pw], rowHeights=[12])
                _cb_hdr.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (0, 0), C_TEAL),
                    ("LEFTPADDING", (0, 0), (0, 0), 6),
                    ("TOPPADDING", (0, 0), (0, 0), 1),
                    ("BOTTOMPADDING", (0, 0), (0, 0), 1),
                    ("ROUNDEDCORNERS", [3, 3, 3, 3]),
                ]))
                elements.append(_cb_hdr)
                elements.append(Spacer(1, 0.04 * cm))
                _cbt = Table(_cb_rows, colWidths=[pw * .28, pw * .72])
                _cbt_s = [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                    ("LINEBELOW", (0, 0), (-1, -2), 0.2, C_BORDER),
                ]
                for _ri in range(len(_cb_rows)):
                    if _ri % 2 == 0:
                        _cbt_s.append(("BACKGROUND", (0, _ri), (-1, _ri), C_MINT))
                _cbt.setStyle(TableStyle(_cbt_s))
                elements.append(_cbt)
                elements.append(Spacer(1, 0.06 * cm))

            # ── GUN SONU — OGRETMEN NOTLARI ALANI ──
            elements.append(Spacer(1, 0.1 * cm))
            elements.append(_rule(C_BORDER, 0.4))
            elements.append(Spacer(1, 0.06 * cm))

            notes_hdr = Table(
                [[Paragraph(_t(f"<b>{dn} — Ogretmen Degerlendirmesi</b>"),
                            _s(f"nh{wn}{dk}", fontName=fb, fontSize=7, leading=10, textColor=C_GRAY))]],
                colWidths=[pw], rowHeights=[12])
            notes_hdr.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), C_LIGHT2),
                ("LEFTPADDING", (0, 0), (0, 0), 6),
                ("TOPPADDING", (0, 0), (0, 0), 1),
                ("BOTTOMPADDING", (0, 0), (0, 0), 1),
                ("ROUNDEDCORNERS", [3, 3, 3, 3]),
            ]))
            elements.append(notes_hdr)

            # 3 satir bos not alani
            for ni in range(3):
                elements.append(Paragraph(
                    _t(f"{'_' * 100}"),
                    _s(f"nl{wn}{dk}{ni}", fontSize=7, leading=14, textColor=C_GRAY_L)))

            elements.append(PageBreak())

        # ══════════════════════════════════════════════
        # HAFTA SONU OZET SAYFASI
        # ══════════════════════════════════════════════
        elements.append(_rule(C_GOLD, 1.5))
        sum_hdr = Table(
            [[Paragraph(_t(f"<b>HAFTA {wn} — OZET</b>"), S_PG_TITLE),
              Paragraph(_t(f"Unite {unit_n}: {theme_tr}  |  {_PHASE_TR.get(phase, phase)}"), S_PG_SUB)]],
            colWidths=[pw * .45, pw * .55], rowHeights=[22])
        sum_hdr.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C_DARK),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (0, 0), 10),
            ("RIGHTPADDING", (1, 0), (1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        elements.append(sum_hdr)
        elements.append(_rule(C_GOLD, 0.75))
        elements.append(Spacer(1, 0.2 * cm))

        # 10 saat ozet tablosu
        oz_hdr = [
            Paragraph(_t("<b>Saat</b>"), _s("oh1", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Gun</b>"), _s("oh2", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Slot</b>"), _s("oh3", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Odak</b>"), _s("oh4", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
        ]
        oz_rows = [oz_hdr]
        oz_i = 0
        for dk in _DAY_ORDER:
            dd = wdays.get(dk, {})
            dn = dd.get("day_name", _DAY_TR.get(dk, dk))
            for h in dd.get("hours", []):
                oz_i += 1
                slot = h.get("slot", "MAIN COURSE")
                slot_tr = _SLOT_META.get(slot, {}).get("tr", slot)[:12]
                focus = h.get("focus", "")
                oz_rows.append([
                    Paragraph(_t(f"{oz_i}"), _s(f"oi{oz_i}", fontName=fb, fontSize=7, leading=10, textColor=C_GOLD)),
                    Paragraph(_t(dn), _s(f"od{oz_i}", fontSize=7, leading=10)),
                    Paragraph(_t(slot_tr), _s(f"os{oz_i}", fontSize=7, leading=10, textColor=C_PURPLE)),
                    Paragraph(_t(focus[:55]), _s(f"of{oz_i}", fontSize=7, leading=10)),
                ])

        ozt = Table(oz_rows, colWidths=[pw * .08, pw * .16, pw * .2, pw * .56])
        oz_style = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
            ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.2, C_BORDER),
        ]
        for ri in range(1, len(oz_rows)):
            if ri % 2 == 0:
                oz_style.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
        ozt.setStyle(TableStyle(oz_style))
        elements.append(ozt)
        elements.append(Spacer(1, 0.3 * cm))

        # Gramer odagi
        if gram:
            elements.append(_sec_hdr(f"GRAMER ODAGI: {gram}", C_BLUE))
            elements.append(Spacer(1, 0.08 * cm))

        # Hafta degerlendirme alani
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(_sec_hdr("HAFTALIK DEGERLENDIRME", C_DARK))
        elements.append(Spacer(1, 0.08 * cm))

        eval_items = [
            ("Kazanim Gerceklesme Orani:", "[ ] %0-25   [ ] %26-50   [ ] %51-75   [ ] %76-100"),
            ("Ogrenci Katilimi:", "[ ] Dusuk   [ ] Orta   [ ] Iyi   [ ] Cok Iyi"),
            ("Materyal Yeterliligi:", "[ ] Yetersiz   [ ] Kismen Yeterli   [ ] Yeterli"),
            ("Plana Uyum:", "[ ] Sapma Oldu   [ ] Kismen Uyumlu   [ ] Tamamen Uyumlu"),
        ]
        ev_rows = []
        for elbl, eopt in eval_items:
            ev_rows.append([
                Paragraph(_t(f"<b>{elbl}</b>"), S_BOLD_XS),
                Paragraph(_t(eopt), S_BODY_XS),
            ])
        evt = Table(ev_rows, colWidths=[pw * .35, pw * .65])
        evt.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("BOX", (0, 0), (-1, -1), 0.4, C_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.2, C_BORDER),
            ("BACKGROUND", (0, 0), (0, -1), C_LIGHT2),
        ]))
        elements.append(evt)
        elements.append(Spacer(1, 0.15 * cm))

        # Notlar
        elements.append(Paragraph(_t("<b>Ogretmen Notlari:</b>"), S_BOLD_SM))
        for ni in range(4):
            elements.append(Paragraph(
                _t(f"{'_' * 110}"),
                _s(f"nf{wn}_{ni}", fontSize=7, leading=14, textColor=C_GRAY_L)))

        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(_t("<b>Gelecek Hafta Hazirliklari:</b>"), S_BOLD_SM))
        for ni in range(2):
            elements.append(Paragraph(
                _t(f"{'_' * 110}"),
                _s(f"gh{wn}_{ni}", fontSize=7, leading=14, textColor=C_GRAY_L)))

        # Imza alani
        elements.append(Spacer(1, 0.6 * cm))
        sig_data = [[
            Paragraph(_t("<b>Ogretmen Imza:</b>"), _s(
                f"si1_{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_CENTER)),
            Paragraph(_t(""), S_BODY_XS),
            Paragraph(_t("<b>Mudur Yrd. Imza:</b>"), _s(
                f"si2_{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_CENTER)),
        ]]
        sigt = Table(sig_data, colWidths=[pw * .35, pw * .3, pw * .35])
        sigt.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (0, 0), (0, 0), 0.5, C_GRAY_L),
            ("LINEBELOW", (2, 0), (2, 0), 0.5, C_GRAY_L),
        ]))
        elements.append(sigt)

        # Sayfa sonu (son hafta haric)
        if wi < ew - 1:
            elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PDF BUILD
    # ═══════════════════════════════════════════════════════
    doc = SimpleDocTemplate(
        buf, pagesize=B5,
        leftMargin=M_IN, rightMargin=M_OUT,
        topMargin=M_TOP, bottomMargin=M_BOT,
        title=f"{glabel} Haftalik Ders Plani — Diamond 3D Premium Edition",
        author="SmartCampus AI",
    )

    _fl = glabel
    _fy = acad_year

    def _footer(canvas, doc):
        canvas.saveState()
        _pw, _ph = B5
        y = 0.9 * cm
        canvas.setStrokeColor(rl.HexColor("#B8860B"))
        canvas.setLineWidth(0.8)
        canvas.line(M_IN, y + 12, _pw - M_OUT, y + 12)
        canvas.setFont(fn, 5.5)
        canvas.setFillColor(rl.HexColor("#64748B"))
        canvas.drawString(M_IN, y + 3,
                          f"SmartCampus AI  |  {_fl} Haftalik Ders Plani  |  Diamond 3D Premium  |  {_fy}")
        canvas.drawRightString(_pw - M_OUT, y + 3, f"Sayfa {doc.page}")
        canvas.restoreState()

    doc.build(elements, onFirstPage=_footer, onLaterPages=_footer)
    buf.seek(0)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════
# OKUL ONCESI (5-6 Yas) — HAFTALIK DERS PLANI PDF
# 36 Hafta x 10 Saat = 360 Saat | Diamond 3D Premium Edition
# ═══════════════════════════════════════════════════════════════════════

_PRESCHOOL_SLOT_MODEL = {
    "mon": [
        {"slot": "ANA DERS", "color": "green",  "focus_key": 0},
        {"slot": "BECERI LAB", "color": "purple", "focus_key": 1},
    ],
    "tue": [
        {"slot": "ANA DERS", "color": "green",  "focus_key": 0},
        {"slot": "BECERI LAB", "color": "purple", "focus_key": 1},
    ],
    "wed": [
        {"slot": "ANA DERS", "color": "green",  "focus_key": 0},
        {"slot": "BECERI LAB", "color": "purple", "focus_key": 1},
    ],
    "thu": [
        {"slot": "ANA DERS", "color": "green",  "focus_key": 0},
        {"slot": "BECERI LAB", "color": "purple", "focus_key": 1},
    ],
    "fri": [
        {"slot": "NATIVE SPEAKER", "color": "red", "focus_key": 0},
        {"slot": "NATIVE SPEAKER", "color": "red", "focus_key": 1},
    ],
}


def generate_preschool_weekly_plan_pdf(
    start_week: int = 1,
    end_week: int = 36,
) -> bytes:
    """Okul Oncesi 10 Saatlik Haftalik Ders Plani — B5 baski-hazir PDF."""
    from reportlab.lib.pagesizes import B5
    from reportlab.lib import colors as rl
    from reportlab.lib.units import cm, mm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, PageBreak,
                                     KeepTogether)
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
        _m = {"\u0131": "i", "\u0130": "I", "\u011f": "g", "\u011e": "G",
              "\u00fc": "u", "\u00dc": "U", "\u015f": "s", "\u015e": "S",
              "\u00f6": "o", "\u00d6": "O", "\u00e7": "c", "\u00c7": "C"}
        return str(text).translate(str.maketrans(_m))

    # Preschool curriculum import
    from views.curriculum_okul_oncesi import CURRICULUM_PRESCHOOL as _CURRICULUM_PRESCHOOL
    weeks = _CURRICULUM_PRESCHOOL
    if not weeks:
        return b""

    # Content bank verilerini yukle (grade 0 = preschool)
    _cb_data = _load_cb_for_grade(0)

    now_str = datetime.now().strftime("%d.%m.%Y")
    today = datetime.now().date()
    acad_s = today.year if today.month >= 9 else today.year - 1
    acad_year = f"{acad_s}-{acad_s + 1}"
    kurum = info.get("name", "")

    buf = BytesIO()
    W, H = B5

    M_IN = 2.2 * cm
    M_OUT = 1.6 * cm
    M_TOP = 1.4 * cm
    M_BOT = 1.8 * cm
    pw = W - M_IN - M_OUT

    # Renk paleti
    C_BLACK    = rl.HexColor("#1a1a2e")
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
    C_BLUE_BG  = rl.HexColor("#EFF6FF")
    C_AMBER_BG = rl.HexColor("#FFFBEB")

    SLOT_C = {
        "green":  (C_GREEN, C_GREEN_L, C_MINT),
        "purple": (C_PURPLE, C_PURPLE_L, C_LAVEN),
        "red":    (C_RED, C_RED_L, C_ROSE),
    }

    DAY_COLORS = {
        "mon": C_BLUE, "tue": C_GREEN, "wed": C_PURPLE,
        "thu": C_ORANGE, "fri": C_RED,
    }

    def _s(name, **kw):
        kw.setdefault("fontName", fn)
        kw.setdefault("fontSize", 9)
        kw.setdefault("leading", 13)
        kw.setdefault("textColor", C_TEXT)
        return ParagraphStyle(name, **kw)

    S_COV_TITLE = _s("pct", fontName=fb, fontSize=26, leading=32, alignment=TA_CENTER, textColor=C_WHITE)
    S_COV_SUB   = _s("pcs", fontName=fb, fontSize=14, leading=18, alignment=TA_CENTER, textColor=C_AMBER_L)
    S_COV_INFO  = _s("pci", fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#232B3E"))
    S_WK_NUM    = _s("pwn", fontName=fb, fontSize=36, leading=40, alignment=TA_CENTER, textColor=C_WHITE)
    S_WK_THEME  = _s("pwt", fontName=fb, fontSize=16, leading=20, alignment=TA_CENTER, textColor=C_AMBER_L)
    S_WK_INFO   = _s("pwi", fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl.HexColor("#232B3E"))
    S_PG_TITLE  = _s("ppt", fontName=fb, fontSize=10, leading=13, textColor=C_WHITE)
    S_PG_SUB    = _s("pps", fontSize=7.5, leading=10, textColor=rl.HexColor("#232B3E"), alignment=TA_RIGHT)
    S_SEC       = _s("pse", fontName=fb, fontSize=9, leading=12, textColor=C_WHITE)
    S_SEC_SM    = _s("pss", fontName=fb, fontSize=8, leading=11, textColor=C_WHITE)
    S_BODY      = _s("pbo", fontSize=9, leading=13, alignment=TA_JUSTIFY)
    S_BODY_SM   = _s("pbs", fontSize=8, leading=11.5)
    S_BODY_XS   = _s("pbx", fontSize=7, leading=10, textColor=C_GRAY)
    S_BOLD      = _s("pbd", fontName=fb, fontSize=9, leading=13)
    S_BOLD_SM   = _s("pbds", fontName=fb, fontSize=8, leading=11.5)
    S_BOLD_XS   = _s("pbdx", fontName=fb, fontSize=7, leading=10)
    S_TOC_H     = _s("pth", fontName=fb, fontSize=13, leading=17, textColor=C_WHITE)
    S_TOC       = _s("ptc", fontSize=8, leading=11)
    S_TOC_B     = _s("ptb", fontName=fb, fontSize=8, leading=11)

    elements = []

    def _rule(color=C_AMBER, thickness=1.5):
        t = Table([[""]], colWidths=[pw], rowHeights=[thickness])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), color),
            ("TOPPADDING", (0, 0), (0, 0), 0),
            ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ]))
        return t

    def _sec_hdr(title, color, accent=C_AMBER):
        t = Table(
            [["", Paragraph(_t(f"<b>{title}</b>"), S_SEC)]],
            colWidths=[4, pw - 4], rowHeights=[20])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), accent),
            ("BACKGROUND", (1, 0), (1, 0), color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("ROUNDEDCORNERS", [0, 4, 4, 0]),
        ]))
        return t

    def _mini_hdr(title, color):
        t = Table(
            [["", Paragraph(_t(f"<b>{title}</b>"), S_SEC_SM)]],
            colWidths=[3, pw - 3], rowHeights=[16])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), C_AMBER),
            ("BACKGROUND", (1, 0), (1, 0), color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (1, 0), (1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("ROUNDEDCORNERS", [0, 3, 3, 0]),
        ]))
        return t

    def _info_pill(text, bg=C_LIGHT2, tc=C_TEXT2, fs=7):
        t = Table([[Paragraph(_t(text), _s("pip", fontSize=fs, leading=fs + 3, textColor=tc))]],
                  colWidths=[pw], rowHeights=[fs + 6])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), bg),
            ("LEFTPADDING", (0, 0), (0, 0), 6),
            ("TOPPADDING", (0, 0), (0, 0), 1),
            ("BOTTOMPADDING", (0, 0), (0, 0), 1),
            ("ROUNDEDCORNERS", [3, 3, 3, 3]),
        ]))
        return t

    # ═══════════════════════════════════════════════════════
    # KAPAK SAYFASI
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 2.5 * cm))

    if kurum:
        elements.append(Paragraph(_t(kurum), _s(
            "pkr", fontName=fb, fontSize=14, leading=18,
            textColor=C_TEXT, alignment=TA_CENTER, spaceAfter=4)))
    elements.append(Paragraph(_t(f"{acad_year} Egitim-Ogretim Yili"), _s(
        "pyr", fontSize=10, leading=14, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=16)))

    elements.append(Spacer(1, 1 * cm))
    elements.append(_rule(C_AMBER, 2))

    cv_rows = [
        [Paragraph(_t("DIAMOND 3D PREMIUM EDITION"), _s(
            "pd3d", fontName=fb, fontSize=9, leading=12,
            textColor=C_AMBER_L, alignment=TA_CENTER, spaceBefore=4))],
        [Spacer(1, 6)],
        [Paragraph(_t("OKUL ONCESI"), S_COV_TITLE)],
        [Paragraph(_t("HAFTALIK DERS PLANI"), _s(
            "phfp", fontName=fb, fontSize=20, leading=26, textColor=C_WHITE, alignment=TA_CENTER))],
        [Paragraph(_t("10 SAATLIK WEEKLY LESSON PLAN"), _s(
            "pwlp", fontSize=13, leading=17, textColor=rl.HexColor("#B9F2FF"),
            alignment=TA_CENTER))],
        [Spacer(1, 8)],
        [Paragraph(_t("5-6 Yas Grubu — Pre-A1"), S_COV_SUB)],
        [Paragraph(_t("Okuma-Yazma Bilmiyor | Gorsel + Isitsel + Kinestetik"), S_COV_INFO)],
        [Spacer(1, 6)],
        [Paragraph(_t("36 Hafta  |  360 Ders Saati  |  5 Gun/Hafta  |  2x40dk/Gun"), _s(
            "pdet", fontSize=8, leading=11, textColor=rl.HexColor("#64748B"),
            alignment=TA_CENTER))],
    ]
    cv = Table(cv_rows, colWidths=[pw])
    cv.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (0, 0), 16),
        ("BOTTOMPADDING", (0, -1), (0, -1), 16),
    ]))
    elements.append(cv)
    elements.append(_rule(C_AMBER, 2))

    elements.append(Spacer(1, 1 * cm))

    ib_rows = [
        [Paragraph(_t("Ana Ders (4 saat) + Beceri Lab (4 saat) + Native Speaker (2 saat)"), _s(
            "pib", fontName=fb, fontSize=8.5, leading=12, textColor=C_AMBER, alignment=TA_CENTER))],
        [Paragraph(_t("Haftalik 10 saat, 36 tematik hafta, TPR + gorsel + oyun temelli ogretim"), _s(
            "pib2", fontSize=7.5, leading=10.5, textColor=C_TEXT2, alignment=TA_CENTER))],
    ]
    ibt = Table(ib_rows, colWidths=[pw])
    ibt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_CREAM),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.75, C_AMBER),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, -1), (0, -1), 8),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    elements.append(ibt)

    elements.append(Spacer(1, 1.5 * cm))
    elements.append(Paragraph(_t(now_str), _s(
        "pdt", fontSize=8, leading=11, textColor=C_GRAY, alignment=TA_CENTER)))

    cp = []
    if info.get("address"):
        cp.append(info["address"])
    if info.get("phone"):
        cp.append(f"Tel: {info['phone']}")
    if info.get("web"):
        cp.append(info["web"])
    if cp:
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(_t(" | ".join(cp)), _s(
            "pct2", fontSize=6.5, leading=9, textColor=C_GRAY_L, alignment=TA_CENTER)))

    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # KUNYE
    # ═══════════════════════════════════════════════════════
    elements.append(Spacer(1, 6 * cm))
    kol_items = [
        "<b>Kitap Adi:</b> Okul Oncesi Ingilizce Haftalik Ders Plani — Diamond 3D Premium Edition",
        "<b>Seviye:</b> Pre-A1 | 5-6 Yas | Okul Oncesi",
        "<b>Kapsam:</b> 36 Hafta, 360 Ders Saati, 5 Gun/Hafta",
        "<b>Ders Modeli:</b> Ana Ders (4s) + Beceri Lab (4s) + Native Speaker (2s)",
        f"<b>Yakasim:</b> TPR, Gorsel Ogrenme, Oyun Temelli, Sarki ve Hareket",
        f"<b>Akademik Yil:</b> {acad_year}",
        f"<b>Uretim Tarihi:</b> {now_str}",
        "<b>Platform:</b> SmartCampus AI — Akilli Kampus Egitim Yonetim Sistemi",
    ]
    if kurum:
        kol_items.insert(0, f"<b>Kurum:</b> {kurum}")
    for ki in kol_items:
        elements.append(Paragraph(_t(ki), _s("pkl", fontSize=8, leading=13, textColor=C_TEXT2)))
        elements.append(Spacer(1, 0.1 * cm))
    elements.append(Spacer(1, 1 * cm))
    elements.append(_rule(C_BORDER, 0.5))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(
        _t("Bu kitap SmartCampus AI platformu tarafindan otomatik olarak uretilmistir. "
           "Icerikler 5-6 yas okul oncesi seviyesine uygun olarak tasarlanmistir. "
           "Okuma-yazma bilmeyen ogrenciler icin tamamen gorsel, isitsel ve kinestetik "
           "yaklasimla hazirlanmis haftalik ders planlari sunulmaktadir. "
           "Her hafta 10 ders saati detayli etkinlik akisi icermektedir."),
        _s("pkl2", fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_JUSTIFY)))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # ICINDEKILER
    # ═══════════════════════════════════════════════════════
    sw = max(1, min(start_week, len(weeks)))
    ew = max(sw, min(end_week, len(weeks)))

    toc_hdr = Table(
        [["", Paragraph(_t("<b>ICINDEKILER</b>"), S_TOC_H)]],
        colWidths=[4, pw - 4], rowHeights=[26])
    toc_hdr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), C_AMBER),
        ("BACKGROUND", (1, 0), (1, 0), C_NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("ROUNDEDCORNERS", [0, 6, 6, 0]),
    ]))
    elements.append(toc_hdr)
    elements.append(Spacer(1, 0.4 * cm))

    toc_rows = []
    for wi in range(sw - 1, ew):
        wk = weeks[wi]
        wn = wk.get("week", wi + 1)
        toc_rows.append([
            Paragraph(_t(f"<b>Hafta {wn}</b>"), S_TOC_B),
            Paragraph(_t(f"{wk.get('theme_tr', '')}"), S_TOC),
            Paragraph(_t(f"({wk.get('theme', '')})"), _s(f"pte{wn}", fontSize=7, leading=10, textColor=C_GRAY)),
            Paragraph(_t(f"{len(wk.get('vocab', []))} kelime"), _s(f"ptv{wn}", fontSize=7, leading=10, textColor=C_AMBER)),
        ])
    if toc_rows:
        tt = Table(toc_rows, colWidths=[pw * .15, pw * .35, pw * .3, pw * .2])
        ts = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, C_BORDER),
        ]
        for ri in range(len(toc_rows)):
            if ri % 2 == 0:
                ts.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
        tt.setStyle(TableStyle(ts))
        elements.append(tt)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # HAFTA SAYFALARI
    # ═══════════════════════════════════════════════════════
    for wi in range(sw - 1, ew):
        wk = weeks[wi]
        wn = wk.get("week", wi + 1)
        theme = wk.get("theme", "")
        theme_tr = wk.get("theme_tr", "")
        vocab = wk.get("vocab", [])
        structure = wk.get("structure", "")
        skills = wk.get("skills", {})
        linked = wk.get("linked_content", {})
        wdays = wk.get("days", {})
        assessment = wk.get("assessment", "")

        # ══════════════════════════════════════════════
        # HAFTA KAPAK SAYFASI
        # ══════════════════════════════════════════════
        elements.append(Spacer(1, 3 * cm))
        elements.append(_rule(C_AMBER, 2))

        wk_cv = [
            [Paragraph(_t("HAFTA"), _s(f"pwl{wn}", fontName=fb, fontSize=10,
                        leading=13, textColor=C_AMBER_L, alignment=TA_CENTER))],
            [Paragraph(_t(f"{wn}"), S_WK_NUM)],
            [Spacer(1, 4)],
            [Paragraph(_t(f"{theme_tr}"), S_WK_THEME)],
            [Paragraph(_t(theme), _s(f"pwte{wn}", fontSize=11, leading=15,
                        textColor=rl.HexColor("#232B3E"), alignment=TA_CENTER))],
            [Spacer(1, 8)],
            [Paragraph(_t(f"Kalip: {structure}"), S_WK_INFO)],
            [Paragraph(_t(f"Pre-A1  |  10 Ders Saati  |  5 Gun  |  2x40dk"), _s(
                f"pwci{wn}", fontSize=8.5, leading=12, textColor=C_GRAY_L, alignment=TA_CENTER))],
        ]
        wct = Table(wk_cv, colWidths=[pw])
        wct.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (0, 0), 20),
            ("BOTTOMPADDING", (0, -1), (0, -1), 20),
        ]))
        elements.append(wct)
        elements.append(_rule(C_AMBER, 2))
        elements.append(Spacer(1, 0.4 * cm))

        # Kelime kartlari tablosu
        vocab_txt = "  |  ".join(vocab)
        elements.append(_info_pill(f"<b>Kelimeler:</b> {vocab_txt}", C_AMBER_BG, C_AMBER, 7))
        elements.append(Spacer(1, 0.15 * cm))

        # Beceri hedefleri
        if skills:
            sk_rows = []
            sk_map = {"listening": "Dinleme", "speaking": "Konusma",
                      "pre_reading": "On-Okuma", "pre_writing": "On-Yazma"}
            for sk, slbl in sk_map.items():
                sv = skills.get(sk, "")
                if sv and sv != "—":
                    sk_rows.append([
                        Paragraph(_t(f"<b>{slbl}:</b>"), S_BOLD_XS),
                        Paragraph(_t(sv), S_BODY_XS),
                    ])
            if sk_rows:
                skt = Table(sk_rows, colWidths=[pw * .18, pw * .82])
                skt.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ("BOX", (0, 0), (-1, -1), 0.3, C_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.2, C_BORDER),
                    ("BACKGROUND", (0, 0), (0, -1), C_LIGHT2),
                ]))
                elements.append(skt)
                elements.append(Spacer(1, 0.1 * cm))

        # Hafta ozet tablosu — 5 gun x 2 saat
        dist_hdr = [
            Paragraph(_t("<b>Gun</b>"), _s(f"pdh1{wn}", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Slot</b>"), _s(f"pdh2{wn}", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>1. Saat</b>"), _s(f"pdh3{wn}", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>2. Saat</b>"), _s(f"pdh4{wn}", fontName=fb, fontSize=7.5, leading=10, textColor=C_WHITE)),
        ]
        dist_rows = [dist_hdr]
        for dk in _DAY_ORDER:
            dd_texts = wdays.get(dk, [])
            dn = _DAY_TR.get(dk, dk)
            slots = _PRESCHOOL_SLOT_MODEL.get(dk, [])
            slot_name = slots[0]["slot"] if slots else "ANA DERS"
            h1 = dd_texts[0][:50] if len(dd_texts) > 0 else ""
            h2 = dd_texts[1][:50] if len(dd_texts) > 1 else ""
            dist_rows.append([
                Paragraph(_t(f"<b>{dn}</b>"), S_BOLD_XS),
                Paragraph(_t(slot_name[:10]), S_BODY_XS),
                Paragraph(_t(h1), S_BODY_XS),
                Paragraph(_t(h2), S_BODY_XS),
            ])
        dtt = Table(dist_rows, colWidths=[pw * .16, pw * .14, pw * .35, pw * .35])
        dts = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("BACKGROUND", (0, 0), (-1, 0), C_DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
            ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER),
        ]
        for ri in range(1, len(dist_rows)):
            if ri % 2 == 0:
                dts.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
            if ri == len(dist_rows) - 1:
                dts.append(("BACKGROUND", (0, ri), (-1, ri), C_ROSE))
        dtt.setStyle(TableStyle(dts))
        elements.append(dtt)
        elements.append(PageBreak())

        # ══════════════════════════════════════════════
        # GUNLUK DETAYLI PLAN SAYFALARI (Her saat 1 sayfa)
        # ══════════════════════════════════════════════
        gh = 0
        for dk in _DAY_ORDER:
            dd_texts = wdays.get(dk, [])
            dn = _DAY_TR.get(dk, dk)
            day_color = DAY_COLORS.get(dk, C_BLUE)
            slots = _PRESCHOOL_SLOT_MODEL.get(dk, [])

            for hi, slot_info in enumerate(slots):
                gh += 1
                slot_name = slot_info["slot"]
                sc_key = slot_info["color"]
                sc_main, sc_light, sc_bg = SLOT_C.get(sc_key, SLOT_C["green"])

                # Ders aciklamasi
                hour_text = dd_texts[hi] if hi < len(dd_texts) else ""

                # GUN + SAAT BASLIK BANDI
                elements.append(_rule(C_AMBER, 1.5))

                day_hdr_l = Paragraph(_t(f"<b>HAFTA {wn}  |  {dn}  |  {hi + 1}. DERS</b>"), S_PG_TITLE)
                day_hdr_r = Paragraph(_t(f"Pre-A1  |  {slot_name}  |  40dk"), S_PG_SUB)
                day_hdr = Table([[day_hdr_l, day_hdr_r]], colWidths=[pw * .55, pw * .45], rowHeights=[22])
                day_hdr.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), day_color),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (0, 0), 10),
                    ("RIGHTPADDING", (1, 0), (1, 0), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                elements.append(day_hdr)

                # Tema bilgi bandi
                info_txt = f"Tema: {theme_tr} ({theme})  |  Kalip: {structure}  |  {slot_name}"
                ib = Table([[Paragraph(_t(info_txt), S_BODY_XS)]], colWidths=[pw], rowHeights=[13])
                ib.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (0, 0), C_AMBER_BG),
                    ("LEFTPADDING", (0, 0), (0, 0), 8),
                    ("TOPPADDING", (0, 0), (0, 0), 1),
                    ("BOTTOMPADDING", (0, 0), (0, 0), 1),
                ]))
                elements.append(ib)
                elements.append(_rule(C_AMBER, 0.75))
                elements.append(Spacer(1, 0.15 * cm))

                # Ders slot baslik
                h_lbl = f"{hi + 1}. DERS — {slot_name} (40 dk)"
                elements.append(_mini_hdr(h_lbl, sc_main))
                elements.append(Spacer(1, 0.08 * cm))

                # Ders icerigi
                if hour_text:
                    elements.append(_info_pill(f"<b>Etkinlik:</b> {hour_text}", sc_bg, C_TEXT))
                    elements.append(Spacer(1, 0.1 * cm))

                # Kelimeler
                elements.append(_info_pill(f"<b>Kelimeler:</b> {vocab_txt}", C_LIGHT2, C_GRAY, 6.5))
                elements.append(Spacer(1, 0.1 * cm))

                # Etkinlik akisi (4 asamali okul oncesi yapisi)
                _pk_stages = []
                if "Ana Ders" in slot_name or "ANA" in slot_name:
                    _pk_stages = [
                        f"Isinma (5dk): TPR ile selamla, hareket sarkisi, onceki kelimeleri tekrarla",
                        f"Tanitim (10dk): {theme_tr} konusunda flashcard ile yeni kelimeleri tanitim — gorselle eslestirme",
                        f"Pekistirme (15dk): Kukla/oyun/drama ile kelime pratigi — {structure}",
                        f"Kapani (10dk): Sarki/tekerleme ile tekrar, hafiza oyunu, temel kontrol",
                    ]
                elif "BECERI" in slot_name:
                    _pk_stages = [
                        f"Isinma (5dk): Kisa sarki/chant ile motivasyon, {theme_tr} temali el hareketleri",
                        f"Beceri (15dk): Oyun temelli etkinlik — eslestirme, boyama, kesme-yapistirma",
                        f"Yaratici (10dk): {theme_tr} konusunda sanat etkinligi / dramatizasyon",
                        f"Kapani (10dk): Grup oyunu ile kelime tekrari + TPR pekistirme",
                    ]
                else:  # NATIVE
                    _pk_stages = [
                        f"Isinma (5dk): Native ile selamlasma, gunun temasini tanitim",
                        f"Konusma (15dk): {theme_tr} konusunda native ile serbest konusma + telaffuz",
                        f"Kultur (10dk): Kulturel oyun/sarki — ingilizce kultur ogelerinin tanitimi",
                        f"Kapani (10dk): Haftalik tekrar, telaffuz oyunlari, eglenceli review sarkilar",
                    ]

                a_rows = []
                for ai, act in enumerate(_pk_stages):
                    a_rows.append([
                        Paragraph(_t(f"<b>{ai + 1}</b>"), _s(
                            f"pan{wn}{dk}{hi}_{ai}", fontName=fb, fontSize=7, leading=10,
                            textColor=sc_main, alignment=TA_CENTER)),
                        Paragraph(_t(act), S_BODY_SM),
                    ])
                at = Table(a_rows, colWidths=[0.5 * cm, pw - 0.5 * cm])
                a_style = [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ("LINEBELOW", (0, 0), (-1, -2), 0.2, C_BORDER),
                ]
                for ri in range(len(a_rows)):
                    if ri % 2 == 0:
                        a_style.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
                at.setStyle(TableStyle(a_style))
                elements.append(at)
                elements.append(Spacer(1, 0.1 * cm))

                # Materyaller
                mats = "Flashcard, kukla, sarki CD/speaker, boyama kagidi, renkli kalem, makas, yapistirici"
                elements.append(_info_pill(f"<b>Materyaller:</b> {mats}", C_LIGHT2, C_GRAY, 6.5))
                elements.append(Spacer(1, 0.1 * cm))

                # ── CONTENT BANK ETKINLIKLERI (son saat icin) ──
                if hi == len(slots) - 1:
                    _unit_num = _week_to_unit(wn)
                    _day_banks = _DAY_CB_MAP.get(dk, [])
                    _cb_rows = []
                    _cb_tr_map = {b[2]: b[1] for b in _CB_BANK_NAMES}
                    for _bk in _day_banks:
                        _bdata = _cb_data.get(_bk, {}).get(_unit_num)
                        if _bdata:
                            _btitle = _get_cb_title(_bdata)
                            _blabel = _cb_tr_map.get(_bk, _bk)
                            _cb_rows.append([
                                Paragraph(_t(f"<b>{_blabel}</b>"), _s(
                                    f"pcbl{wn}{dk}{_bk}", fontName=fb, fontSize=6.5,
                                    leading=9, textColor=C_TEAL)),
                                Paragraph(_t(_btitle), _s(
                                    f"pcbt{wn}{dk}{_bk}", fontSize=6.5, leading=9,
                                    textColor=C_TEXT2)),
                            ])
                    if _cb_rows:
                        elements.append(Spacer(1, 0.08 * cm))
                        _cb_hdr = Table(
                            [[Paragraph(_t("<b>ICERIK BANKASI ETKINLIKLERI</b>"),
                                        _s(f"pcbh{wn}{dk}", fontName=fb, fontSize=6.5,
                                           leading=9, textColor=C_WHITE))]],
                            colWidths=[pw], rowHeights=[12])
                        _cb_hdr.setStyle(TableStyle([
                            ("BACKGROUND", (0, 0), (0, 0), C_TEAL),
                            ("LEFTPADDING", (0, 0), (0, 0), 6),
                            ("TOPPADDING", (0, 0), (0, 0), 1),
                            ("BOTTOMPADDING", (0, 0), (0, 0), 1),
                            ("ROUNDEDCORNERS", [3, 3, 3, 3]),
                        ]))
                        elements.append(_cb_hdr)
                        elements.append(Spacer(1, 0.04 * cm))
                        _cbt = Table(_cb_rows, colWidths=[pw * .28, pw * .72])
                        _cbt_s = [
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 4),
                            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                            ("LINEBELOW", (0, 0), (-1, -2), 0.2, C_BORDER),
                        ]
                        for _ri in range(len(_cb_rows)):
                            if _ri % 2 == 0:
                                _cbt_s.append(("BACKGROUND", (0, _ri), (-1, _ri), C_MINT))
                        _cbt.setStyle(TableStyle(_cbt_s))
                        elements.append(_cbt)
                        elements.append(Spacer(1, 0.06 * cm))

                # Ogretmen notu alani
                elements.append(Spacer(1, 0.15 * cm))
                elements.append(_rule(C_BORDER, 0.4))
                elements.append(Spacer(1, 0.06 * cm))

                notes_hdr = Table(
                    [[Paragraph(_t(f"<b>{dn} {hi + 1}. Ders — Ogretmen Degerlendirmesi</b>"),
                                _s(f"pnh{wn}{dk}{hi}", fontName=fb, fontSize=7, leading=10, textColor=C_GRAY))]],
                    colWidths=[pw], rowHeights=[12])
                notes_hdr.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (0, 0), C_LIGHT2),
                    ("LEFTPADDING", (0, 0), (0, 0), 6),
                    ("TOPPADDING", (0, 0), (0, 0), 1),
                    ("BOTTOMPADDING", (0, 0), (0, 0), 1),
                    ("ROUNDEDCORNERS", [3, 3, 3, 3]),
                ]))
                elements.append(notes_hdr)

                for ni in range(4):
                    elements.append(Paragraph(
                        _t(f"{'_' * 100}"),
                        _s(f"pnl{wn}{dk}{hi}{ni}", fontSize=7, leading=14, textColor=C_GRAY_L)))

                elements.append(PageBreak())

        # ══════════════════════════════════════════════
        # HAFTA SONU OZET + DEGERLENDIRME
        # ══════════════════════════════════════════════
        elements.append(_rule(C_AMBER, 1.5))
        sum_hdr = Table(
            [[Paragraph(_t(f"<b>HAFTA {wn} — OZET</b>"), S_PG_TITLE),
              Paragraph(_t(f"{theme_tr} ({theme})"), S_PG_SUB)]],
            colWidths=[pw * .4, pw * .6], rowHeights=[22])
        sum_hdr.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C_DARK),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (0, 0), 10),
            ("RIGHTPADDING", (1, 0), (1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        elements.append(sum_hdr)
        elements.append(_rule(C_AMBER, 0.75))
        elements.append(Spacer(1, 0.2 * cm))

        # 10 saat ozet
        oz_hdr = [
            Paragraph(_t("<b>Saat</b>"), _s(f"poh1{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Gun</b>"), _s(f"poh2{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Slot</b>"), _s(f"poh3{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
            Paragraph(_t("<b>Odak</b>"), _s(f"poh4{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_WHITE)),
        ]
        oz_rows = [oz_hdr]
        oz_i = 0
        for dk in _DAY_ORDER:
            dd_texts = wdays.get(dk, [])
            dn = _DAY_TR.get(dk, dk)
            slots = _PRESCHOOL_SLOT_MODEL.get(dk, [])
            for hi, si in enumerate(slots):
                oz_i += 1
                ht = dd_texts[hi][:55] if hi < len(dd_texts) else ""
                oz_rows.append([
                    Paragraph(_t(f"{oz_i}"), _s(f"poi{wn}_{oz_i}", fontName=fb, fontSize=7, leading=10, textColor=C_AMBER)),
                    Paragraph(_t(dn), _s(f"pod{wn}_{oz_i}", fontSize=7, leading=10)),
                    Paragraph(_t(si["slot"][:12]), _s(f"pos{wn}_{oz_i}", fontSize=7, leading=10, textColor=C_PURPLE)),
                    Paragraph(_t(ht), _s(f"pof{wn}_{oz_i}", fontSize=7, leading=10)),
                ])
        ozt = Table(oz_rows, colWidths=[pw * .08, pw * .16, pw * .18, pw * .58])
        oz_style = [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
            ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.2, C_BORDER),
        ]
        for ri in range(1, len(oz_rows)):
            if ri % 2 == 0:
                oz_style.append(("BACKGROUND", (0, ri), (-1, ri), C_LIGHT))
        ozt.setStyle(TableStyle(oz_style))
        elements.append(ozt)
        elements.append(Spacer(1, 0.2 * cm))

        # Degerlendirme kriteri
        if assessment:
            elements.append(_info_pill(f"<b>Degerlendirme:</b> {assessment}", C_AMBER_BG, C_AMBER, 7))
            elements.append(Spacer(1, 0.1 * cm))

        # Hafta degerlendirme formu
        elements.append(_sec_hdr("HAFTALIK DEGERLENDIRME", C_DARK))
        elements.append(Spacer(1, 0.08 * cm))

        eval_items = [
            ("Kelime Ogrenme Durumu:", "[ ] Hic   [ ] 1-3 kelime   [ ] 4-6 kelime   [ ] Tamamini"),
            ("Katilim ve Motivasyon:", "[ ] Dusuk   [ ] Orta   [ ] Iyi   [ ] Cok Iyi"),
            ("TPR Tepki Hizi:", "[ ] Yavas   [ ] Normal   [ ] Hizli"),
            ("Plana Uyum:", "[ ] Sapma Oldu   [ ] Kismen   [ ] Tamamen Uyumlu"),
        ]
        ev_rows = []
        for elbl, eopt in eval_items:
            ev_rows.append([
                Paragraph(_t(f"<b>{elbl}</b>"), S_BOLD_XS),
                Paragraph(_t(eopt), S_BODY_XS),
            ])
        evt = Table(ev_rows, colWidths=[pw * .35, pw * .65])
        evt.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("BOX", (0, 0), (-1, -1), 0.4, C_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.2, C_BORDER),
            ("BACKGROUND", (0, 0), (0, -1), C_LIGHT2),
        ]))
        elements.append(evt)
        elements.append(Spacer(1, 0.15 * cm))

        # Notlar + imza
        elements.append(Paragraph(_t("<b>Ogretmen Notlari:</b>"), S_BOLD_SM))
        for ni in range(3):
            elements.append(Paragraph(
                _t(f"{'_' * 110}"),
                _s(f"pnf{wn}_{ni}", fontSize=7, leading=14, textColor=C_GRAY_L)))

        elements.append(Spacer(1, 0.4 * cm))
        sig_data = [[
            Paragraph(_t("<b>Ogretmen Imza:</b>"), _s(
                f"psi1_{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_CENTER)),
            Paragraph(_t(""), S_BODY_XS),
            Paragraph(_t("<b>Mudur Yrd. Imza:</b>"), _s(
                f"psi2_{wn}", fontName=fb, fontSize=7, leading=10, textColor=C_GRAY, alignment=TA_CENTER)),
        ]]
        sigt = Table(sig_data, colWidths=[pw * .35, pw * .3, pw * .35])
        sigt.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (0, 0), (0, 0), 0.5, C_GRAY_L),
            ("LINEBELOW", (2, 0), (2, 0), 0.5, C_GRAY_L),
        ]))
        elements.append(sigt)

        if wi < ew - 1:
            elements.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PDF BUILD
    # ═══════════════════════════════════════════════════════
    doc = SimpleDocTemplate(
        buf, pagesize=B5,
        leftMargin=M_IN, rightMargin=M_OUT,
        topMargin=M_TOP, bottomMargin=M_BOT,
        title="Okul Oncesi Haftalik Ders Plani — Diamond 3D Premium Edition",
        author="SmartCampus AI",
    )

    _fl = "Okul Oncesi"
    _fy = acad_year

    def _footer(canvas, doc):
        canvas.saveState()
        _pw, _ph = B5
        y = 0.9 * cm
        canvas.setStrokeColor(rl.HexColor("#D97706"))
        canvas.setLineWidth(0.8)
        canvas.line(M_IN, y + 12, _pw - M_OUT, y + 12)
        canvas.setFont(fn, 5.5)
        canvas.setFillColor(rl.HexColor("#64748B"))
        canvas.drawString(M_IN, y + 3,
                          f"SmartCampus AI  |  {_fl} Haftalik Ders Plani  |  Diamond 3D Premium  |  {_fy}")
        canvas.drawRightString(_pw - M_OUT, y + 3, f"Sayfa {doc.page}")
        canvas.restoreState()

    doc.build(elements, onFirstPage=_footer, onLaterPages=_footer)
    buf.seek(0)
    return buf.getvalue()
