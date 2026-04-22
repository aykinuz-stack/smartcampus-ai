"""
Smarti Dergi - Profesyonel 30-Sayfa Dergi PDF Ureticisi (Platypus)
=========================================================================
Aylik dijital dergi icin baski kalitesinde, 30 sayfalik profesyonel
magazin PDF uretir. ReportLab Platypus flowable sistemi kullanarak
sayfalari TAMAMEN doldurur - bos sayfa birakmaz.
"""
import streamlit as st
from io import BytesIO
import os

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage, KeepTogether,
    Flowable, CondPageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas

PAGE_W, PAGE_H = A4

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MASCOT_PATH = os.path.join(_BASE_DIR, "assets", "mascot.png")
DERGI_IMG_DIR = os.path.join(_BASE_DIR, "data", "dergi_gorseller")
os.makedirs(DERGI_IMG_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# AI GORSEL URETIM (DALL-E 3) + CACHE
# ---------------------------------------------------------------------------
def _get_dergi_image(prompt_key: str, prompt_text: str, size="1024x1024"):
    """Dergi icin gorsel uret veya cache'den yukle. Returns image path or None."""
    # Cache kontrol
    safe_key = "".join(c if c.isalnum() or c in "_-" else "_" for c in prompt_key)[:60]
    cached_path = os.path.join(DERGI_IMG_DIR, f"{safe_key}.png")
    if os.path.exists(cached_path) and os.path.getsize(cached_path) > 1000:
        return cached_path

    # DALL-E 3 ile uret
    try:
        from views.ai_destek import _ensure_env, _get_client
        import requests
        _ensure_env()
        client = _get_client()
        if not client:
            return None

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size=size,
            quality="hd",
            n=1
        )
        image_url = response.data[0].url
        img_response = requests.get(image_url, timeout=60)
        if img_response.status_code == 200 and len(img_response.content) > 1000:
            with open(cached_path, "wb") as f:
                f.write(img_response.content)
            return cached_path
    except Exception:
        pass
    return None


def generate_dergi_images(sayi_no: int, progress_callback=None):
    """Bir sayi icin tum gorselleri olustur. Returns dict of {section: path}."""
    data = DERGI_DATA.get(sayi_no)
    if not data:
        return {}

    tema = data.get("tema", "")
    ay = data.get("ay", "")
    images = {}

    # Makale basliklarindan detayli prompt uret
    bilim_baslik = data.get("bilim_teknik", [{}])[0].get("baslik", "bilim")
    bilim2_baslik = data.get("bilim_teknik", [{}, {}])[-1].get("baslik", "teknoloji") if len(data.get("bilim_teknik", [])) > 1 else ""
    tekno_baslik = data.get("teknoloji", {}).get("baslik", "teknoloji")
    tarih_baslik = data.get("tarih", {}).get("baslik", "tarih")
    gezi_yer = data.get("cografya_gezi", {}).get("yer", "sehir")
    gezi_ulke = data.get("cografya_gezi", {}).get("ulke", "ulke")
    doga_baslik = data.get("doga_cevre", {}).get("baslik", "doga")
    kitap_adi = data.get("edebiyat", {}).get("kitap", "kitap")
    kitap_yazar = data.get("edebiyat", {}).get("yazar", "yazar")
    spor_baslik = data.get("spor", {}).get("baslik", "spor")
    kultur_baslik = data.get("kultur_sanat", {}).get("baslik", "kultur")
    psi_baslik = data.get("psikoloji", {}).get("baslik", "psikoloji")

    prompts = {
        "kapak": (
            f"Ultra high quality professional magazine cover design. Theme: '{tema}'. "
            f"Beautiful editorial photography style, cinematic lighting, rich colors, "
            f"depth of field. The image should evoke the feeling of {tema.lower()} in an educational context. "
            f"Photorealistic, award-winning magazine cover quality. "
            f"NO TEXT, NO LETTERS, NO WORDS in the image. Pure visual art only."
        ),
        "bilim": (
            f"Scientific editorial illustration for magazine article titled '{bilim_baslik}'. "
            f"Photorealistic, detailed, showing the actual scientific concept. "
            f"Professional science magazine quality like National Geographic or Scientific American. "
            f"Cinematic lighting, rich detail, educational diagram elements blended with photography. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "teknoloji": (
            f"Technology editorial photograph for article '{tekno_baslik}'. "
            f"Cutting-edge tech visualization, realistic rendering of modern technology. "
            f"Professional tech magazine style like Wired or MIT Technology Review. "
            f"Clean, futuristic, showing real technological innovation. High detail. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "tarih": (
            f"Historical editorial illustration for article '{tarih_baslik}'. "
            f"Atmospheric, dramatic historical scene reconstruction. Museum quality artwork. "
            f"Rich period-accurate details, golden hour lighting, epic composition. "
            f"Style of historical documentary photography or oil painting. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "gezi": (
            f"Travel photography of {gezi_yer}, {gezi_ulke}. "
            f"Stunning aerial or panoramic view of the most iconic landmark. "
            f"Golden hour lighting, vibrant colors, professional travel magazine quality "
            f"like Conde Nast Traveler. Breathtaking composition showing the beauty of the place. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "doga": (
            f"Nature photography for article '{doga_baslik}'. "
            f"Award-winning wildlife or landscape photography style. "
            f"National Geographic quality, stunning natural beauty, perfect timing shot. "
            f"Rich colors, dramatic lighting, showing the wonder of nature. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "edebiyat": (
            f"Artistic editorial illustration for book review of '{kitap_adi}' by {kitap_yazar}. "
            f"Atmospheric, moody, literary scene that captures the essence of the novel. "
            f"Beautiful lighting, vintage library ambiance mixed with the book's theme. "
            f"Fine art photography or digital art style. Evocative and thoughtful. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "spor": (
            f"Dynamic sports photography for article '{spor_baslik}'. "
            f"Action shot, frozen moment, dramatic athletic achievement. "
            f"Professional sports magazine quality like Sports Illustrated. "
            f"High speed, motion blur background, sharp subject, stadium atmosphere. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "kultur": (
            f"Art and culture editorial photograph for article '{kultur_baslik}'. "
            f"Museum gallery, concert hall, or theater stage atmosphere. "
            f"Beautiful artistic composition showing the intersection of different art forms. "
            f"Warm, inviting, culturally rich. Gallery lighting, fine art quality. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "psikoloji": (
            f"Conceptual editorial illustration for psychology article '{psi_baslik}'. "
            f"Abstract visualization of the human mind, emotions, and personal growth. "
            f"Artistic, thoughtful, calming colors. Professional counseling magazine quality. "
            f"Symbolic imagery representing mental wellness, balance, and self-discovery. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "hobi": (
            f"Beautiful still life photography of creative hobbies: origami paper cranes, "
            f"macrame wall hanging, telescope pointed at starry sky, pressed flowers herbarium. "
            f"Warm lighting, artistic composition, magazine editorial quality. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "felsefe": (
            f"Philosophical concept art: ancient Greek thinker statue (like Rodin's The Thinker), "
            f"cosmic background, floating books, light of knowledge rays. "
            f"Dramatic lighting, contemplative mood, fine art quality. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "ingilizce": (
            f"English language learning editorial: Big Ben London, British flag colors, "
            f"open English textbook, vocabulary cards floating, warm classroom atmosphere. "
            f"Educational, welcoming, professional language school photography. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "almanca": (
            f"German language learning editorial: Brandenburg Gate Berlin, German flag colors, "
            f"German textbook, umlauts floating, cozy European study room atmosphere. "
            f"Educational, warm tones, professional language school photography. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
        "muzik": (
            f"Musical instruments artistic photograph: grand piano, violin, sheet music, "
            f"concert hall atmosphere, golden stage lighting, classical music ambiance. "
            f"Professional concert photography quality, warm tones. "
            f"NO TEXT, NO LETTERS, NO WORDS."
        ),
    }

    total = len(prompts)
    for idx, (key, prompt) in enumerate(prompts.items()):
        cache_key = f"sayi{sayi_no}_{key}"
        path = _get_dergi_image(cache_key, prompt)
        if path:
            images[key] = path
        if progress_callback:
            progress_callback((idx + 1) / total)

    return images


def _safe_image(path, width=None, height=None):
    """Gorsel varsa RLImage dondur, yoksa bos Spacer dondur."""
    if path and os.path.exists(path):
        try:
            kwargs = {}
            if width:
                kwargs["width"] = width
            if height:
                kwargs["height"] = height
            return RLImage(path, **kwargs)
        except Exception:
            pass
    return Spacer(1, 0)

# ---------------------------------------------------------------------------
# RENK PALETI
# ---------------------------------------------------------------------------
GOLD = HexColor("#c9a84c")
DARK_GOLD = HexColor("#b8860b")
NAVY = HexColor("#0d1b2a")
DARK_NAVY = HexColor("#050d18")
LIGHT_GRAY = HexColor("#f2f2f2")
CREAM = HexColor("#fdf5e6")
ACCENT_BLUE = HexColor("#2563eb")
SECTION_COLORS = {
    "bilim": HexColor("#1a73e8"),
    "teknoloji": HexColor("#7c3aed"),
    "tarih": HexColor("#b45309"),
    "gezi": HexColor("#059669"),
    "doga": HexColor("#16a34a"),
    "edebiyat": HexColor("#be185d"),
    "siir": HexColor("#7e22ce"),
    "psikoloji": HexColor("#0891b2"),
    "veli": HexColor("#ea580c"),
    "ogrenci": HexColor("#2563eb"),
    "kultur": HexColor("#c026d3"),
    "spor": HexColor("#dc2626"),
    "sozler": HexColor("#854d0e"),
    "bilmece": HexColor("#4f46e5"),
    "quiz": HexColor("#0d9488"),
}


# ---------------------------------------------------------------------------
# CUSTOM FLOWABLE: Colored Header Bar
# ---------------------------------------------------------------------------
class SectionHeaderBar(Flowable):
    """Renkli bant ile bolum basligi."""

    def __init__(self, title, bg_color, text_color=white, icon="", height=28, font_size=14):
        Flowable.__init__(self)
        self.title = title
        self.bg_color = bg_color
        self.text_color = text_color
        self.icon = icon
        self.bar_height = height
        self.font_size = font_size
        self.width = PAGE_W - 4 * cm
        self.height = height + 4

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg_color)
        c.roundRect(0, 0, self.width, self.bar_height, 4, fill=1, stroke=0)
        # Gold accent left
        c.setFillColor(GOLD)
        c.rect(0, 0, 5, self.bar_height, fill=1, stroke=0)
        # Text
        c.setFillColor(self.text_color)
        c.setFont("Helvetica-Bold", self.font_size)
        label = f"{self.icon}  {self.title}" if self.icon else self.title
        c.drawString(14, (self.bar_height - self.font_size) / 2 + 1, label)


class GoldLine(Flowable):
    """Gold dekoratif cizgi."""

    def __init__(self, width=None, thickness=1.5, color=GOLD):
        Flowable.__init__(self)
        self._width = width
        self.thickness = thickness
        self.color = color
        self.height = thickness + 4

    def wrap(self, availWidth, availHeight):
        w = self._width or availWidth
        return (w, self.height)

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.thickness)
        w = self._width or self.width
        c.line(0, self.height / 2, w, self.height / 2)


class InfoBox(Flowable):
    """Renkli bilgi kutusu."""

    def __init__(self, content_paragraphs, bg_color=HexColor("#f0f4ff"),
                 accent_color=ACCENT_BLUE, padding=10):
        Flowable.__init__(self)
        self.content_paragraphs = content_paragraphs
        self.bg_color = bg_color
        self.accent_color = accent_color
        self.padding = padding
        self._content_height = 0

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        total_h = 0
        for p in self.content_paragraphs:
            w, h = p.wrap(availWidth - 2 * self.padding - 6, availHeight)
            total_h += h
        self._content_height = total_h + 2 * self.padding
        self.height = self._content_height
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg_color)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        c.setFillColor(self.accent_color)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        y = self.height - self.padding
        for p in self.content_paragraphs:
            w, h = p.wrap(self.width - 2 * self.padding - 6, self.height)
            p.drawOn(c, self.padding + 6, y - h)
            y -= h


class PullQuote(Flowable):
    """Dekoratif alinti kutusu."""

    def __init__(self, quote_text, author, accent_color=GOLD):
        Flowable.__init__(self)
        self.quote_text = quote_text
        self.author = author
        self.accent_color = accent_color
        style = _get_styles()
        self.quote_para = Paragraph(f'<i>"{quote_text}"</i>', style["Quote"])
        self.author_para = Paragraph(f'<b>-- {author}</b>', style["QuoteAuthor"])

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        inner_w = availWidth - 40
        _, qh = self.quote_para.wrap(inner_w, availHeight)
        _, ah = self.author_para.wrap(inner_w, availHeight)
        self.height = qh + ah + 20
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        # Left gold bar
        c.setFillColor(self.accent_color)
        c.rect(15, 2, 3, self.height - 4, fill=1, stroke=0)
        # Big quote mark
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(Color(0.85, 0.65, 0.13, 0.3))
        c.drawString(2, self.height - 30, "\xe2\x80\x9c")
        # Content
        inner_w = self.width - 40
        _, qh = self.quote_para.wrap(inner_w, self.height)
        self.quote_para.drawOn(c, 28, self.height - qh - 4)
        _, ah = self.author_para.wrap(inner_w, self.height)
        self.author_para.drawOn(c, 28, 6)


# ---------------------------------------------------------------------------
# STYLES
# ---------------------------------------------------------------------------
_STYLES_CACHE = None


def _get_styles():
    global _STYLES_CACHE
    if _STYLES_CACHE is not None:
        return _STYLES_CACHE
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "MagazineTitle", parent=styles["Heading1"],
        fontSize=28, textColor=HexColor("#1a1a2e"), spaceAfter=6,
        fontName="Helvetica-Bold", alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        "SectionHeader", parent=styles["Heading2"],
        fontSize=18, textColor=GOLD, spaceAfter=8,
        spaceBefore=12, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(
        "ArticleTitle", parent=styles["Heading3"],
        fontSize=14, textColor=ACCENT_BLUE, spaceAfter=6,
        fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(
        "ArticleTitleColored", parent=styles["Heading3"],
        fontSize=14, textColor=HexColor("#1a1a2e"), spaceAfter=6,
        fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(
        "SubTitle", parent=styles["Heading4"],
        fontSize=12, textColor=HexColor("#374151"), spaceAfter=4,
        spaceBefore=8, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10, leading=14, textColor=HexColor("#333333"),
        alignment=TA_JUSTIFY, spaceAfter=6))
    styles.add(ParagraphStyle(
        "BodySmall", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=HexColor("#444444"),
        alignment=TA_JUSTIFY, spaceAfter=4))
    styles.add(ParagraphStyle(
        "Quote", parent=styles["Normal"],
        fontSize=11, leading=15, textColor=HexColor("#555555"),
        fontName="Times-Italic", leftIndent=20, rightIndent=20,
        spaceAfter=4, spaceBefore=4))
    styles.add(ParagraphStyle(
        "QuoteAuthor", parent=styles["Normal"],
        fontSize=10, textColor=HexColor("#777777"),
        fontName="Helvetica-Bold", alignment=TA_RIGHT,
        rightIndent=20, spaceAfter=6))
    styles.add(ParagraphStyle(
        "InfoTitle", parent=styles["Normal"],
        fontSize=10, textColor=ACCENT_BLUE, fontName="Helvetica-Bold",
        spaceAfter=4))
    styles.add(ParagraphStyle(
        "InfoBody", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=HexColor("#444444"),
        spaceAfter=3))
    styles.add(ParagraphStyle(
        "TOCEntry", parent=styles["Normal"],
        fontSize=10, leading=14, textColor=HexColor("#333333"),
        spaceAfter=2))
    styles.add(ParagraphStyle(
        "TOCPage", parent=styles["Normal"],
        fontSize=10, textColor=GOLD, fontName="Helvetica-Bold",
        alignment=TA_RIGHT))
    styles.add(ParagraphStyle(
        "PoemText", parent=styles["Normal"],
        fontSize=11, leading=16, textColor=HexColor("#2d2d2d"),
        fontName="Times-Italic", leftIndent=15, spaceAfter=4))
    styles.add(ParagraphStyle(
        "PoemTitle", parent=styles["Normal"],
        fontSize=13, textColor=HexColor("#7e22ce"), fontName="Helvetica-Bold",
        spaceAfter=4, spaceBefore=8))
    styles.add(ParagraphStyle(
        "PoemBio", parent=styles["Normal"],
        fontSize=8, leading=11, textColor=HexColor("#888888"),
        fontName="Times-Roman", spaceAfter=6))
    styles.add(ParagraphStyle(
        "QuizQ", parent=styles["Normal"],
        fontSize=10, leading=13, textColor=NAVY,
        fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=6))
    styles.add(ParagraphStyle(
        "QuizOpt", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=HexColor("#444444"),
        leftIndent=15, spaceAfter=1))
    styles.add(ParagraphStyle(
        "BulletItem", parent=styles["Normal"],
        fontSize=10, leading=13, textColor=HexColor("#333333"),
        spaceAfter=3, bulletIndent=10, leftIndent=22))
    styles.add(ParagraphStyle(
        "FooterStyle", parent=styles["Normal"],
        fontSize=8, textColor=HexColor("#999999"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Normal"],
        fontSize=48, textColor=white, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"],
        fontSize=18, textColor=GOLD, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=6))
    styles.add(ParagraphStyle(
        "Centered", parent=styles["Normal"],
        fontSize=10, leading=14, textColor=HexColor("#333333"),
        alignment=TA_CENTER, spaceAfter=6))
    styles.add(ParagraphStyle(
        "SmallGray", parent=styles["Normal"],
        fontSize=8, textColor=HexColor("#999999"), spaceAfter=2))
    styles.add(ParagraphStyle(
        "SectionTitle", parent=styles["Heading2"],
        fontSize=16, textColor=HexColor("#1a1a2e"), spaceAfter=8,
        spaceBefore=6, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(
        "TimelineYear", parent=styles["Normal"],
        fontSize=10, textColor=GOLD, fontName="Helvetica-Bold",
        spaceAfter=1))
    styles.add(ParagraphStyle(
        "TimelineEvent", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=HexColor("#333333"),
        leftIndent=15, spaceAfter=4))
    styles.add(ParagraphStyle(
        "GlossaryTerm", parent=styles["Normal"],
        fontSize=9, textColor=ACCENT_BLUE, fontName="Helvetica-Bold",
        spaceAfter=1))
    styles.add(ParagraphStyle(
        "GlossaryDef", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=HexColor("#555555"),
        leftIndent=10, spaceAfter=4))
    styles.add(ParagraphStyle(
        "BackCoverText", parent=styles["Normal"],
        fontSize=11, leading=15, textColor=HexColor("#eeeeee"),
        alignment=TA_CENTER, spaceAfter=6))

    _STYLES_CACHE = styles
    return styles


# ---------------------------------------------------------------------------
# COVER PAGE (canvas callback)
# ---------------------------------------------------------------------------
def _draw_cover_page(c, doc):
    """Kapak sayfasi - tam sayfa gradient + gold + mascot."""
    data = doc._dergi_data
    r_int, g_int, b_int = data["renk"]
    tc = Color(r_int / 255.0, g_int / 255.0, b_int / 255.0)
    tc_dark = Color(r_int / 255.0 * 0.5, g_int / 255.0 * 0.5, b_int / 255.0 * 0.5)

    # Gradient background
    steps = 50
    step_h = PAGE_H / steps
    for i in range(steps):
        ratio = i / float(steps)
        cr = tc_dark.red + (0.02 - tc_dark.red) * ratio
        cg = tc_dark.green + (0.05 - tc_dark.green) * ratio
        cb = tc_dark.blue + (0.15 - tc_dark.blue) * ratio
        c.setFillColor(Color(max(0, cr), max(0, cg), max(0, cb)))
        c.rect(0, PAGE_H - (i + 1) * step_h, PAGE_W, step_h + 1, fill=1, stroke=0)

    # Top gold bar
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 40, PAGE_W, 40, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(NAVY)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 28, "SmartCampus Egitim Platformu")

    # Smarti Dergi big title
    c.setFont("Helvetica-Bold", 52)
    c.setFillColor(white)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 120, "Smarti")

    # Decorative line
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(PAGE_W / 2 - 120, PAGE_H - 138, PAGE_W / 2 + 120, PAGE_H - 138)

    # Month / issue
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(GOLD)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 168, data["ay"])
    c.setFont("Helvetica", 13)
    c.setFillColor(Color(0.8, 0.8, 0.9))
    c.drawCentredString(PAGE_W / 2, PAGE_H - 188, f"Sayi {data['sayi']}  |  30 Sayfa  |  20+ Bolum")

    # Theme
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(white)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 230, f'Tema: "{data["tema"]}"')

    # Separator
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(60, PAGE_H - 252, PAGE_W - 60, PAGE_H - 252)

    # Mascot image
    mascot_y = PAGE_H - 340
    if os.path.exists(MASCOT_PATH):
        try:
            c.drawImage(MASCOT_PATH, PAGE_W / 2 - 35, mascot_y, width=70, height=70,
                        preserveAspectRatio=True, mask="auto")
        except Exception:
            pass

    # Teaser headlines
    teasers = data.get("kapak_teasers", [])
    y = PAGE_H - 370
    for teaser_text, teaser_page in teasers:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(white)
        c.drawString(75, y, f"> {teaser_text}")
        c.setFont("Helvetica", 10)
        c.setFillColor(GOLD)
        c.drawRightString(PAGE_W - 75, y, f"s. {teaser_page}")
        y -= 26

    # Bottom gold bar
    c.setFillColor(GOLD)
    c.rect(0, 0, PAGE_W, 50, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawCentredString(PAGE_W / 2, 28, "Aylik Egitim ve Kultur Dergisi")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 12, "SmartCampus Egitim Platformu | smartcampus.edu.tr")


def _draw_later_pages(c, doc):
    """Header ve footer - normal sayfalar icin."""
    data = doc._dergi_data
    r_int, g_int, b_int = data["renk"]
    tc = Color(r_int / 255.0, g_int / 255.0, b_int / 255.0)
    page = doc.page

    # Kuse kagit efekti - hafif krem arka plan
    c.saveState()
    c.setFillColor(Color(0.99, 0.98, 0.96, 0.4))  # Very subtle warm cream
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    # Header
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 28, PAGE_W, 28, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GOLD)
    c.drawString(1.5 * cm, PAGE_H - 20, f"Smarti Dergi  |  {data['ay']}  |  Sayi {data['sayi']}")
    c.drawRightString(PAGE_W - 1.5 * cm, PAGE_H - 20, f'Tema: {data["tema"]}')
    # Gold accent line under header
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(0, PAGE_H - 29, PAGE_W, PAGE_H - 29)

    # Footer
    c.setStrokeColor(HexColor("#cccccc"))
    c.setLineWidth(0.5)
    c.line(1.5 * cm, 1.2 * cm, PAGE_W - 1.5 * cm, 1.2 * cm)
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor("#999999"))
    c.drawCentredString(PAGE_W / 2, 0.7 * cm, f"Sayfa {page}  |  Smarti Dergi  |  {data['ay']}")


# ---------------------------------------------------------------------------
# HELPER: Build flowables
# ---------------------------------------------------------------------------
def _make_section_bar(title, color_key="bilim", icon=""):
    clr = SECTION_COLORS.get(color_key, ACCENT_BLUE)
    return SectionHeaderBar(title, clr, icon=icon)


def _make_info_box(title, items, accent_color=ACCENT_BLUE, bg="#f0f4ff"):
    """Bilgi kutusu olusturur."""
    styles = _get_styles()
    paras = [Paragraph(f"<b>{title}</b>", styles["InfoTitle"])]
    for item in items:
        paras.append(Paragraph(f"<bullet>&bull;</bullet> {item}", styles["InfoBody"]))
    return InfoBox(paras, bg_color=HexColor(bg), accent_color=accent_color)


def _make_glossary_table(terms):
    """Terim listesi tablosu olusturur."""
    styles = _get_styles()
    elements = []
    for term, defn in terms:
        elements.append(Paragraph(f"<b>{term}:</b> {defn}", styles["GlossaryDef"]))
    return elements


def _make_timeline(events):
    """Zaman cizelgesi olusturur."""
    styles = _get_styles()
    elements = []
    for year, event in events:
        elements.append(Paragraph(f"<b>{year}</b>", styles["TimelineYear"]))
        elements.append(Paragraph(event, styles["TimelineEvent"]))
    return elements


def _make_two_col_table(left_flowables, right_flowables, left_pct=0.55):
    """Iki sutunlu layout - Table olarak."""
    avail = PAGE_W - 4 * cm
    lw = avail * left_pct
    rw = avail * (1 - left_pct)
    data = [[left_flowables, right_flowables]]
    t = Table(data, colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (-1, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def _make_pull_quote(quote, author):
    return PullQuote(quote, author)


# ---------------------------------------------------------------------------
# DERGI VERI TABANI
# ---------------------------------------------------------------------------
DERGI_DATA = {
    # ===================== SAYI 1 - EYLUL 2025 =====================
    1: {
        "ay": "Eylul 2025", "sayi": 1, "tema": "Okula Donus",
        "renk": (37, 99, 235),
        "kapak_teasers": [
            ("Beynimiz Nasil Ogrenir?", 4),
            ("Yapay Zeka ve Egitimin Gelecegi", 5),
            ("Dunyanin En Eski Universiteleri", 9),
            ("Istanbul Gezi Rehberi", 11),
            ("Kucuk Prens - Kitap Tavsiyesi", 15),
            ("Olimpiyat Sporlari Rehberi", 26),
        ],
        "editorial": (
            "Degerli okuyucularimiz, yeni egitim-ogretim yilina merhaba! Smarti Dergi'nin "
            "ilk sayisiyla karsinizda olmaktan buyuk mutluluk duyuyoruz. Bu sayimizda beynimizin "
            "ogrenme mekanizmalarindan yapay zekanin egitimdeki rolune, sonbahar gocunden dunya "
            "edebiyatina kadar genis bir yelpazede sizlerle bulusuyoruz. Her sayfamizda bilgi ve "
            "ilham dolu icerikler sizi bekliyor.\n\n"
            "Her ay farkli bir temayla bilim, kultur, sanat ve spor dunyasindan en ilgi cekici "
            "konulari sizlere sunmaya devam edecegiz. Ilk sayimizin temasi 'Okula Donus' -- yeni "
            "donem icin ilham ve motivasyon dolu bir baslangic. Bu sayimizda 86 milyar noronun "
            "hikayesinden baslayarak beynimizin nasil ogrendigini kesfedecek, yapay zekanin egitim "
            "dunyasinda yarattigi devrimi inceleyeceksiniz.\n\n"
            "Dergimiz, ogrenciler, ogretmenler ve veliler icin hazirlanmistir. Her bolumde bilgi "
            "ve eglenceyi bir arada bulacaksiniz. Bilimden sanata, spordan edebiyata her alandan "
            "secme iceriklerle dolu 30 sayfalik bu yolculukta sizleri yalniz birakmiyoruz. Tarih "
            "bolumumuzdeki universite tarihcesinden cografya bolumumuzdeki Istanbul rehberine, siir "
            "kosemizden bulmacalarimiza kadar herkes icin bir sey var.\n\n"
            "Psikoloji ve rehberlik bolumumuzdeki okula donus stratejilerinden veli kosemizdeki "
            "pratik onerilere kadar ailenizin tum bireyleri bu dergiden faydalanabilir. Quiz "
            "bolumumuzdeki 15 soruyla kendinizi test etmeyi de unutmayin! Her sayimizda bilgi "
            "daginarcigimizi genisletmeye, yeni ufuklar acmaya devam edecegiz.\n\n"
            "Keyifli okumalar dileriz!\n\nSmarti Dergi Yayin Kurulu"
        ),
        "icerik_tablosu": [
            ("Editorden", 2), ("Editorden Devam", 3),
            ("Bilim: Beynimiz Nasil Ogrenir?", 4),
            ("Bilim: Yapay Zeka ve Egitim", 5),
            ("Bilim: Sozluk ve Bilgi Kutulari", 6),
            ("Teknoloji: Dijital Cagda Egitim", 7),
            ("Teknoloji: Haberler ve Gelecek", 8),
            ("Tarih: Dunyanin En Eski Universiteleri", 9),
            ("Tarih: Zaman Cizelgesi ve Bu Ay", 10),
            ("Cografya: Istanbul Gezi Rehberi", 11),
            ("Gezi: Gorulmesi Gereken Yerler", 12),
            ("Doga: Sonbahar Gocu", 13),
            ("Cevre: Tehlike Altindaki Turler", 14),
            ("Edebiyat: Kucuk Prens", 15),
            ("Edebiyat: Kitap Onerileri", 16),
            ("Siir Kosesi", 17),
            ("Psikoloji: Okula Donus", 18),
            ("Psikoloji: Stres ve Rehberlik", 19),
            ("Veli Kosesi: Yeni Donem Rehberi", 20),
            ("Veli: Beslenme ve Iletisim", 21),
            ("Ogrenci Tavsiyeleri", 22),
            ("Ogrenci: 10 Aliskanlik", 23),
            ("Kultur ve Sanat", 24),
            ("Kultur: Film, Muzik, Muze", 25),
            ("Spor Kosesi", 26),
            ("Ozlu Sozler", 27),
            ("Bilmeceler ve Bulmacalar", 28),
            ("Aylik Quiz", 29),
            ("Arka Kapak: Cevaplar", 30),
        ],
        "bilim_teknik": [
            {
                "baslik": "Beynimiz Nasil Ogrenir?",
                "giris": (
                    "Insan beyni, evrende bilinen en karmasik yapidir. 86 milyar noron ve "
                    "trilyonlarca sinaptik baglanti ile ogrenme, hatirlama ve yaraticilik "
                    "gibi mucizevi islevleri gerceklestirir."
                ),
                "icerik": (
                    "Insan beyni yaklasik 86 milyar norondan olusur ve bu noronlar arasindaki "
                    "sinaptik baglantilar ogrenmenin temelini olusturur. Noroplastisite adi verilen "
                    "bu ozellik sayesinde beyin, yeni deneyimlerle surekli yeniden sekillenir. "
                    "Her yeni bilgi ogrenildiginde noronlar arasinda yeni baglantilar kurulur ve "
                    "var olan baglantilar guclendirilir. Bu sure yasamimiz boyunca devam eder. "
                    "Beyin, vucut agirliginin yalnizca yuzde ikisini olustururken, toplam enerji "
                    "tuketiminin yuzde yirmisini tek basina kullanir.\n\n"
                    "Hafiza olusumu uc temel asamadan gecer: kodlama, depolama ve geri cagirma. "
                    "Kisa sureli hafiza yaklasik 20-30 saniye bilgi tutabilirken, tekrar ve anlam "
                    "yukleme ile bilgiler uzun sureli hafizaya aktarilir. Hipokampus bu surecte "
                    "kritik bir rol ustlenir. Uyku sirasinda beyin, gun icinde alinan bilgileri "
                    "siniflandirir ve uzun sureli hafizaya konsolide eder. Bu nedenle yeterli uyku "
                    "ogrenme icin vazgecilmezdir. Arastirmalar, uyku oncesi calisilan konularin "
                    "ertesi gun yuzde kirk daha iyi hatirlanadigini gostermektedir.\n\n"
                    "Etkili calisma teknikleri arasinda aralikli tekrar en one cikan yontemdir. "
                    "Bu teknikte bilgiler artan araliklarla tekrarlanir: 1 gun, 3 gun, 7 gun, "
                    "14 gun ve 30 gun sonra. Arastirmalar bu yontemin ogrenmeyi yuzde elliye kadar "
                    "artirabildigini gosterir. Aktif geri cagirma ise bilgiyi pasif olarak okumak "
                    "yerine bellekten aktif olarak cekmeye dayaniyor. Kendinize soru sorma, "
                    "konuyu baskasina anlatma veya zihin haritasi cikartma bu yonteme ornektir. "
                    "Bu tekniklerin bir arada kullanilmasi ogrenme verimliligini buyuk olcude arttirir.\n\n"
                    "Pomodoro teknigi de zaman yonetimi acisindan cok etkilidir. 25 dakikalik "
                    "odaklanmis calisma bloklari ve 5 dakikalik molalar seklinde organize edilir. "
                    "Her 4 Pomodoro'dan sonra 15-30 dakikalik uzun mola verilir. Bu yontem dikkat "
                    "dagiticilarla savasmada ve odaklanmayi artirmada bilimsel olarak kanitlanmistir. "
                    "Italyan universite ogrencisi Francesco Cirillo tarafindan gelistirilen bu teknik, "
                    "adini mutfaktaki domates bicimindeki zamanlayicidan almistir.\n\n"
                    "Norobilimdeki son gelismeler, fiziksel egzersizin beyinde BDNF (Beyin Kokenli "
                    "Notrofik Faktor) salgilanmasini artirarak ogrenme kapasitesini yukselttigini "
                    "ortaya koymustur. Gunluk 30 dakikalik aerobik egzersiz, hipokampusteki noron "
                    "uretimini hizlandirarak hafiza performansini onemli olcude iyilestirir. "
                    "Bunun yaninda meditasyon ve mindfulness uygulamalari da prefrontal korteksi "
                    "guclendirerek dikkat ve odaklanma kapasitesini artirmaktadir. Dusuk stres "
                    "ortaminda ogrenme daha verimli gerceklesir; kronik stres ise kortizol salgisini "
                    "artirarak hafiza olusumunu olumsuz etkiler."
                ),
                "biliyor_muydunuz": [
                    "Beyin vucut agirliginin %2'sini olusturur ama vucut enerjisinin %20'sini kullanir.",
                    "Bir noron saniyede 200'den fazla sinyal iletebilir.",
                    "Beyin uyku sirasinda gunduz ogrendiklerini duzenler ve kalici hafizaya aktarir.",
                    "Yeni bir sey ogrendiginizde beyninizde fiziksel olarak yeni baglantilar olusur.",
                    "Beyin saniyede 11 milyon bit bilgi alir ancak bunun yalnizca 50 bitinin farkindadir.",
                ],
            },
            {
                "baslik": "Yapay Zeka ve Egitimin Gelecegi",
                "giris": (
                    "Yapay zeka, egitim dunyasinda devrim yaratmaya devam ediyor. Kisisellestirilmis "
                    "ogrenme yollarindan otomatik degerlendirmeye, AI teknolojileri ogrenci ve "
                    "ogretmenlerin hayatini kolaylastiriyor."
                ),
                "icerik": (
                    "Yapay zeka destekli egitim sistemleri, her ogrencinin ogrenme hizina ve stiline "
                    "uyum saglayabilen kisisellestirilmis ogrenme deneyimleri sunmaktadir. AI tutorlar, "
                    "ogrencilerin guclu ve zayif yonlerini analiz ederek bireysel ogrenme planlari "
                    "olusturur. Bu sistemler, geleneksel sinif ortaminda mumkun olmayan bire bir "
                    "ilgiyi her ogrenciye saglayabilir. Khan Academy, Duolingo ve Coursera gibi "
                    "platformlar bu teknolojilerin en basarili ornekleri arasindadir. Her gun "
                    "milyonlarca ogrenci bu platformlarda kisisellestirilmis egitim almaktadir.\n\n"
                    "Adaptif ogrenme platformlari, ogrencinin performansina gore zorluk seviyesini "
                    "otomatik ayarlar. Bir ogrenci zorlandiginda sistem ek aciklamalar sunarken, "
                    "konuyu kavrayan ogrencilere ileri seviye icerikler onerir. Bu yaklasim, her "
                    "ogrencinin kendi hizinda ilerlemesini ve motivasyonunu kaybetmemesini saglar. "
                    "Makine ogrenimi algoritmalari, binlerce ogrencinin verilerinden ogrendigi "
                    "paternlere dayanarak hangi ogretim stratejisinin hangi ogrenci tipi icin en "
                    "etkili oldugunu belirleyebilir. Bu veriye dayali yaklasim geleneksel egitimin "
                    "sunmadig inanilmaz bir kisisellestime saglamaktadir.\n\n"
                    "Dogal dil isleme teknolojileri sayesinde AI sistemleri artik ogrencilerin "
                    "acik uclu yanitlarini degerlendirebilir ve aninda geri bildirim verebilir. "
                    "Bu teknoloji ogretmenlerin is yukunu onemli olcude azaltirken ogrencilere "
                    "hizli geri donus saglar. Dil ogreniminde AI destekli konusma pratigi "
                    "uygulamalari buyuk ilgi gormektedir. ChatGPT, Claude ve Gemini gibi buyuk "
                    "dil modelleri ogrencilerin karmasik konulari anlamasinda asistan gorevi "
                    "ustlenebilmektedir. Bu modeller sorulara detayli aciklamalar sunabilir ve "
                    "farkli ogretim yaklasimlarini deneyebilir.\n\n"
                    "Sanal gerceklik ve artirilmis gerceklik teknolojileri de egitimde devrimsel "
                    "degisiklikler yapmaktadir. Ogrenciler tarihi mekanlari sanal olarak gezebilir, "
                    "insan vucudunun icine uc boyutlu olarak bakabilir veya kimyasal reaksiyonlari "
                    "simule edebilir. Stanford Universitesi'nin arastirmalari, VR tabanli egitimlerin "
                    "geleneksel yontemlere kiyasla bilgi kaliciligini yuzde otuz bes artirdigini "
                    "gostermistir. Meta, Apple ve Google gibi teknoloji devleri egitim odakli VR "
                    "iceriklere buyuk yatirimlar yapmaktadir.\n\n"
                    "Gelecekte AI, ogretmenin yerini almak yerine onu destekleyen bir asistan rolu "
                    "ustlenecektir. Ogretmenler rutin degerlendirme islerinden kurtularak ogrencilerle "
                    "bire bir ilgilenmeye daha fazla zaman ayirabilecektir. AI, egitimde firsatlari "
                    "demokratiklestirme potansiyeline sahiptir. Uzak bolgelerden buyuk sehirlere "
                    "kadar her ogrenci ayni kalitede egitim icerigine erisebilecektir. Turkiye'de "
                    "MEB'in dijitallesme projeleri ve EBA platformu da bu vizyona hizmet etmektedir."
                ),
            },
        ],
        "bilim_sozlugu": [
            ("Noroplastisite", "Beynin yeni deneyimlerle yapisini degistirme yetenegi. Yeni bilgi ogrenildiginde noronlar arasinda yeni sinaptik baglantilar kurulur."),
            ("Sinaps", "Iki noron arasindaki baglanti noktasi. Elektriksel ve kimyasal sinapslar olarak ikiye ayrilir."),
            ("Hipokampus", "Beynin temporal lobunda yer alan ve hafiza olusumunda kritik rol oynayan yapidir. Hasar gordugunde yeni anilar olusturulamaz."),
            ("BDNF", "Beyin Kokenli Notrofik Faktor. Noronlarin buyumesini ve hayatta kalmasini destekleyen bir protein. Egzersizle salgisi artar."),
            ("Adaptif Ogrenme", "Ogrencinin seviyesine gore otomatik uyum saglayan egitim yontemi. Yapay zeka algoritmalari kullanilarak kisisellestirilir."),
            ("Pomodoro Teknigi", "25 dakika odakli calisma + 5 dakika mola seklinde uygulanan zaman yonetimi yontemi."),
        ],
        "teknoloji": {
            "baslik": "Dijital Cagda Egitim Teknolojileri",
            "icerik": (
                "Egitim teknolojileri son on yilda muazzam bir donusum gecirdi. Akilli tahtalar, "
                "tabletler ve online platformlar sinif ortamini tamamen degistirdi. Pandemi donemi "
                "bu donusumu daha da hizlandirarak uzaktan egitimi zorunlu bir alternatif haline "
                "getirdi. Dunya genelinde 1.6 milyar ogrenci bir donemde uzaktan egitim almak "
                "zorunda kaldi ve bu deneyim egitim teknolojilerine olan bakis acisini kokluden "
                "degistirdi.\n\n"
                "Sanal gerceklik (VR) ve artirilmis gerceklik (AR) teknolojileri egitimde yeni "
                "ufuklar aciyor. Ogrenciler tarihi mekanlari sanal olarak gezebilir, insan "
                "vucudunun icine 3D olarak bakabilir veya kimyasal reaksiyonlari simule edebilir. "
                "Bu immersif deneyimler, soyut kavramlarin somutlastirilmasinda buyuk avantaj "
                "saglar. Google Expeditions projesi ile ogrenciler Buyuk Set Mercan Resifi'ni, "
                "Mars yuzeyini ve antik Roma'yi siniflarinda deneyimleyebilmektedir. Medikal "
                "egitimde VR kullanarak ameliyat simulasyonu yapan universiteler ogrencilerinin "
                "beceri seviyesini geleneksel yontemlere gore cok daha hizli artirmaktadir.\n\n"
                "Bulut tabanli isbirligi araclari ogrencilerin proje bazli calismalarda birlikte "
                "uretmesini kolaylastirmaktadir. Google Classroom, Microsoft Teams ve Moodle gibi "
                "platformlar sinif yonetimini dijitallestirmektedir. Dijital portfolyolar ve "
                "e-degerlendirme sistemleri de ogrenme surecinin izlenmesinde yeni standartlar "
                "olusturmaktadir. Ogretmenler anlik geri bildirim verebilir, ogrenciler ise "
                "projelerini dunyanin her yerinden ekip arkadaslariyla birlikte gelistirebilir.\n\n"
                "Kodlama egitimi artik ilkokul seviyesinden itibaren mufredatlara girmektedir. "
                "Scratch, Python ve robotik kodlama ile ogrenciler algoritmik dusunme becerilerini "
                "erken yaslarda gelistirmektedir. Finlandiya, Estonya ve Guney Kore gibi egitimde "
                "lider ulkeler kodlamayi zorunlu ders olarak mufredatlarina eklemistir. Turkiye'de "
                "de MEB'in 'Bilisim Teknolojileri' dersleri guncellenerek kodlama icerikleri "
                "zenginlestirilmektedir. Robotik ve maker hareketi ogrencilerin yaraticiligini "
                "ve muhendislik dusunme becerilerini gelistirmektedir.\n\n"
                "Oyunlastirma (gamification) da egitim teknolojilerinde onemli bir trend olarak "
                "one cikmaktadir. Kahoot, Quizlet ve Classcraft gibi platformlar ogrenmeyi "
                "eglenceli bir deneyime donusturmektedir. Puan toplama, seviye atlama ve basarim "
                "rozeti kazanma mekanikleri ogrencilerin motivasyonunu artirmaktadir. Arastirmalar "
                "oyunlastirilmis ortamlarda ogrencilerin derse katiliminin yuzde kirk arttigini "
                "gostermektedir."
            ),
            "haberler": [
                "UNESCO, AI destekli egitim icin kuresel etik cerceve yayimladi.",
                "Turkiye'de 'Dijital Okul' projesi 10.000 okula yayildi.",
                "Meta, egitim odakli VR basligini 2025'te piyasaya surdu.",
                "Finlandiya, kodlamayi ilkokul mufredatina zorunlu olarak ekledi.",
                "Google, Classroom platformuna AI destekli degerlendirme ekledi.",
                "Microsoft, ozel egitim icin yeni erisebilirlik araclari gelistirdi.",
            ],
            "gelecekte_bu_var": (
                "2030 yilinda siniflar nasil olacak? Uzmanlar, holografik ogretmenlerin, "
                "beyine dogrudan bilgi aktarimi icin noroarayuzlerin ve tamamen kisisellestirilmis "
                "AI mufredat planlarinin gercek olabilecegini ongormektedir. Kuantum bilgisayarlar "
                "ile simule edilen devasa bilimsel deneylerde ogrenciler bizzat yer alabilecek. "
                "Elon Musk'in Neuralink projesi, beyinle bilgisayar arasinda dogrudan iletisimi "
                "hedefliyor. Her ne kadar bu teknolojiler henuz erken asamada olsa da, on yil "
                "icinde prototipler egitim alaninda test edilmeye baslayabilir. Yapay genel zeka "
                "(AGI) gerceklestiginde egitimin tamamen kisisellestirilmis, 7/24 erisilebilir "
                "ve her bireyin potansiyelini maksimize eden bir yapilanmaya kavusmasi bekleniyor."
            ),
        },
        "tarih": {
            "baslik": "Dunyanin En Eski Universiteleri",
            "icerik": (
                "Dunyanin en eski surekli faaliyet gosteren universitesi, 859 yilinda Fas'in Fez "
                "sehrinde kurulan El-Karaviyyin Universitesi'dir. Fatima el-Fihri tarafindan "
                "kurulan bu universite, UNESCO ve Guinness Rekorlar Kitabi tarafindan da "
                "taninmaktadir. Kurulusundan itibaren astronomi, matematik, kimya, tip, felsefe "
                "ve dini bilimler ogretilmistir. El-Karaviyyin, Avrupa'daki universiteler icin "
                "bir model teskil etmis ve bircok Avrupali bilgin burada egitim almistir. "
                "Gerbert d'Aurillac (sonraki Papa II. Silvester) burada matematik egitimi almis "
                "ve Arap rakamlarini Avrupa'ya tanitmistir.\n\n"
                "Avrupa'nin en eski universitesi 1088 yilinda kurulan Bologna Universitesi'dir. "
                "Hukuk egitimi ile un kazanan bu kurum, modern universite kavraminin temellerini "
                "atmistir. Bologna modeli, ogrenci odakli bir yonetim anlayisi benimsemis ve "
                "ogrenciler hocalarini kendileri secebilmistir. Oxford Universitesi ise 1096'dan "
                "beri kesintisiz egitim vermektedir. Cambridge Universitesi 1209'da, Oxford'dan "
                "ayrilank akademisyenler tarafindan kurulmustur. Bu iki universite arasindaki "
                "rekabet yuzyillardir bilimsel ilerlemenin itici gucu olmustur.\n\n"
                "El-Ezher Universitesi 970 yilinda Kahire'de kurulmus ve Islam dunyasinin en "
                "prestijli egitim kurumlarindan biri olmustur. Burada gerceklestirilen tercume "
                "faaliyetleri, antik Yunan eserlerinin Arapca'ya kazandirilmasini saglamistir. "
                "Bu ceviriler Avrupa Ronesansi'nin entelektuel temellerini olusturmustur. "
                "Aristoteles, Platon ve Iklid'in eserleri once Arapca'ya, ardindan Latince'ye "
                "cevrilerek Avrupali dusunurler tarafindan kesfedilmistir. Bilim tarihinde "
                "Islam medeniyetinin bu kopruleme rolu son derece kritik bir oneme sahiptir.\n\n"
                "Turkiye'de modern universite gelenegini Istanbul Darulfununu (1900) ve ardindan "
                "1933 universite reformu baslatmistir. Ataturk'un onderligi ile gerceklestirilen "
                "reform kapsaminda Nazi Almanyasi'ndan kacak akademisyenler Turkiye'ye davet "
                "edilmis ve Istanbul Universitesi yeniden yapilandirilmistir. Albert Malche "
                "tarafindan hazirlanan rapor dogrultusunda Darulfunun kapatilmis ve yerine "
                "modern universite kurulmustur. Bu reform Turkiye'nin bilimsel gelisiminde "
                "bir donum noktasi olmustur.\n\n"
                "Bugun dunya genelinde 30.000'den fazla universite bulunmaktadir. Times Higher "
                "Education, QS ve Shanghai siralamalarina gore ABD, Ingiltere ve Avrupa "
                "universiteleri listelere hakim olsa da, Asya universiteleri hizla yukselisini "
                "surdurmektedir. Turkiye'den ODTU, Bogazici, Sabanci ve Koc universiteleri "
                "uluslararasi siralamalarda istikrarli bir sekilde yukariya dogru ilerlemektedir."
            ),
            "zaman_cizelgesi": [
                ("MO 387", "Platon, Atina'da Akademia'yi kurdu - dunya tarihindeki ilk 'akademi'"),
                ("859", "El-Karaviyyin Universitesi kuruldu (Fez, Fas)"),
                ("970", "El-Ezher Universitesi kuruldu (Kahire, Misir)"),
                ("1088", "Bologna Universitesi kuruldu (Italya)"),
                ("1096", "Oxford Universitesi egitim faaliyetleri basladi"),
                ("1209", "Cambridge Universitesi kuruldu (Ingiltere)"),
                ("1257", "Sorbonne (Paris Universitesi) kuruldu"),
                ("1900", "Istanbul Darulfununu acildi"),
                ("1933", "Ataturk'un universite reformu gerceklestirildi"),
            ],
            "tarihte_bu_ay": [
                "1 Eylul 1939 - II. Dunya Savasi, Almanya'nin Polonya'yi isgali ile basladi.",
                "12 Eylul 1683 - Ikinci Viyana Kusatmasi sona erdi; Osmanli'nin Avrupa'daki ilerleyisinde donum noktasi.",
                "17 Eylul 1787 - ABD Anayasasi imzalandi; modern demokrasinin temel belgesi.",
                "19 Eylul 1881 - ABD Baskani James Garfield suikast sonucu hayatini kaybetti.",
                "23 Eylul 1846 - Neptun gezegeni matematiksel hesaplamalarla kesfedildi.",
            ],
            "tarih_sozu": {
                "soz": "Tarih tekerrurden ibarettir; cunku kimse tarihten ders almaz.",
                "kisi": "George Bernard Shaw",
            },
        },
        "cografya_gezi": {
            "yer": "Istanbul",
            "ulke": "Turkiye",
            "baskent_bilgi": {
                "nufus": "16+ milyon", "dil": "Turkce", "para": "Turk Lirasi (TRY)",
                "alan": "5.461 km2", "iklim": "Akdeniz-Karadeniz gecis iklimi",
            },
            "tanitim": (
                "Iki kitayi birbirine baglayan dunya uzerindeki tek sehir olan Istanbul, 8.500 "
                "yillik tarihiyle insanligin en eski yerlesim yerlerinden biridir. Bizans ve "
                "Osmanli imparatorluklarina baskentlik yapmis bu essiz sehir, bugun 16 milyonu "
                "askin nufusuyla Turkiye'nin en buyuk metropoludur. Roma, Bizans ve Osmanli "
                "medeniyetlerinin katmanli mirasini tasiyarak dunyanin en zengin kulturel "
                "birikimlerinden birine ev sahipligi yapmaktadir.\n\n"
                "Istanbul, Karadeniz'i Marmara Denizi'ne baglayan bogazi, tarihi yarimadasi, "
                "Halic'i ve Asya yakasi ile essiz bir cografyaya sahiptir. Sehir, 39 ilcesi ve "
                "yuzlerce mahallesiyle Avrupa ve Asya kitalarina yayilir. Tarihi eserleri, dogal "
                "guzellikleri, zengin mutfagi ve canli kultur hayati ile her yil 15 milyondan "
                "fazla turisti agirlar. Istanbul, dunyanin en cok ziyaret edilen 10 sehrinden "
                "biridir ve turizm gelirleri acisindan Turkiye ekonomisinin lokomotifidir.\n\n"
                "UNESCO Dunya Mirasi Listesi'nde yer alan tarihi yarimada; Ayasofya, Sultanahmet "
                "Camii, Topkapi Sarayi ve Yerebatan Sarnici gibi benzersiz yapilariyla dunya "
                "kulturel mirasinin en onemli parcalarindan birini olusturur. 537 yilinda insa "
                "edilen Ayasofya, yaklasik bin yil boyunca dunyanin en buyuk katedrali olma "
                "unvanini tasimistir. Mimar Sinan'in saheseri Suleymaniye Camii ise Osmanli "
                "mimarisinin zirvesi olarak kabul edilmektedir.\n\n"
                "Modern Istanbul, tarihi dokusuyla cagdas yasamin harmanlandigi dinamik bir "
                "sehirdir. Beyoglu'nun canli gece hayati, Kadikoy'un alternatif kultur mekanları, "
                "Nisantasi'nin luks alisveris caddeleri ve Balat'in renkli sokaklari farkli "
                "yasam tarzlarini bir arada sunmaktadir. Bogaz kiyisindaki yalilar, Adalar'in "
                "huzuru ve Belgrad Ormani'nin yesilligi sehrin dogal zenginliklerini olusturur.\n\n"
                "Istanbul'un yemek kulturu de dunyanin en zenginlerinden biridir. Kebaptan "
                "mezeye, borekten baklavaya, baliktan kokoreçe kadar binlerce cesit lezzet "
                "sunan sehir, gastronomi tutkunlari icin adeta bir acik hava muzesidir."
            ),
            "gorulmesi_gereken": [
                "Ayasofya - 537'de insa edilen dunya mimari tarihinin saheseri, 1500 yillik tarih",
                "Topkapi Sarayi - 400 yil boyunca Osmanli sultanlarinin ikametgahi, Kutsal Emanetler",
                "Kapali Carsi - 1461'den beri faaliyet gosteren 4.000 dukkaniyla dunyanin en buyuk kapali carsisi",
                "Galata Kulesi - 14. yuzyildan kalma, Istanbul panoramasi sunan ikonik kule",
                "Kiz Kulesi - Bogaz'in ortasindaki efsanevi yapi, Istanbul'un en romantik noktasi",
            ],
            "yemek_onerileri": [
                "Balik Ekmek - Eminonu'nde tarihi lezzetin simgesi, bogaz manzarasi esliginde",
                "Iskender Kebap - Osmanli mutfagindan modern sofraya ulasan et saheseri",
                "Kunefe - Hatay'dan Istanbul'a ulasan, peynirli sicak tatli keyfi",
                "Turk Kahvesi - UNESCO somut olmayan kultur mirasi, 500 yillik gelenek",
            ],
            "harita_aciklama": (
                "Istanbul, 41 derece kuzey enlemi ve 29 derece dogu boylaminda, Marmara Denizi'nin "
                "kuzeyinde, Karadeniz'in guneyinde yer alir. Avrupa ve Asya kitalarini Istanbul "
                "Bogazi ayirir. Bogaz 31.7 km uzunlugunda olup en dar noktasi 700 metredir."
            ),
        },
        "doga_cevre": {
            "baslik": "Sonbahar Gocu - Kuslar Nereye Gidiyor?",
            "icerik": (
                "Her sonbahar, dunyada yaklasik 50 milyar kus goc yolculuguna cikar. Bazi turler "
                "10.000 km'den fazla mesafe kat eder. Kuzey Kutbu sumru kusu, her yil yaklasik "
                "70.000 km yol alan sampiyondur. Bu mucizevi yolculuklar, kuslarin icgudusel "
                "navigasyon yeteneklerinin ne denli gelismis oldugunu gozler onune serer. Goc, "
                "milyonlarca yillik evrimsel adaptasyonun sonucudur ve kuslarin hayatta kalma "
                "stratejilerinin en etkileyici orneklerinden biridir.\n\n"
                "Gocmen kuslar yonlerini bulmak icin Dunya'nin manyetik alanini, gunes ve "
                "yildizlarin konumunu ve hatta koku duyularini kullanir. Gagalarindaki manyetit "
                "kristalleri bir tur dahili pusula gorevi gorur. Son arastirmalar, kuslarin "
                "kuantum dolanikligi kullanarak manyetik alanlari gorebildigini ortaya koymustur. "
                "Bu 'kuantum pusula' mekanizmasi, fizik ve biyoloji arasindaki en sasirtici "
                "kesisim noktalarindan biridir. Gocmen kuslar ayrica Gunes'in polarize isigini "
                "ve yildiz haritalarini navigasyon icin kullanabilmektedir.\n\n"
                "Turkiye, Avrupa ile Afrika arasindaki en onemli goc yollarindan birinin "
                "uzerinde yer alir. Istanbul Bogazi, her sonbahar binlerce yirtici kusun gecis "
                "noktasidir. Buyukada ve Camlica tepeleri goc gozlemi icin ideal noktalardir. "
                "Turkiye'nin goc rotasi uzerinde bulunmasi, ulkeyi kus gozlemciligi (birdwatching) "
                "icin dunyanin en cazip destinasyonlarindan biri yapmaktadir. Burdur Golu, Manyas "
                "Kus Cenneti ve Goksu Deltasi onemli kus gozlem alanlaridir.\n\n"
                "Iklim degisikligi goc oruntularini onemli olcude degistirmektedir. Bazi turler "
                "daha kisa mesafeler goc ederken, bazilari goc zamanlamalarini kaydirmaktadir. "
                "Akdeniz bolgesinde kislayan kuslarin sayisi artarken, Afrika'ya goc eden tUrlerin "
                "sayisi azalmaktadir. Bu degisimler ekosistemlerde zincirleme etkiler yaratabilir. "
                "Boçek populasyonlari, tozlasma ve tarim uzerindeki dolaylI etkiler bilim insanlarini "
                "endiselendiirmektedir.\n\n"
                "Kus gocunu korumak icin uluslararasi isbirligi sart. Ramsar Sozlesmesi ve Biyolojik "
                "Cesitlilik Sozlesmesi bu alandaki en onemli uluslararasi cercevelerdir. Turkiye, "
                "13 Ramsar alani ile gocmen kuslarin korunmasinda onemli bir rolle sahiptir."
            ),
            "nesli_tehlike": [
                ("Kelaynak", "Turkiye'de Birecik ve Sanlurfa'da koruma altinda. Dunyada yalnizca 700 birey kalmistir. Nesli en cok tehlike altindaki kus turlerinden biridir."),
                ("Akdeniz Foku", "Turkiye sahillerinde 100'den az bireyin yasadigi tahmin ediliyor. Habitat kaybi ve balikcilik aglari en buyuk tehditlerdir."),
                ("Anadolu Parsı", "Son gozlem 1974'te Hakkari'de yapildi. Nesli tukenme tehlikesiyle karsi karsiya olup var olup olmadigu tartismalidir."),
                ("Saz Kedisi", "Turkiye'de sulak alan tahribati nedeniyle populasyonu azalmaktadir. Cok az bireyin kaldigi tahmin edilmektedir."),
            ],
            "eko_ipuclari": [
                "Tek kullanimlik plastik yerine bez torba ve matara kullanin. Yilda 500 milyar plastik poset kullaniliyor.",
                "Gereksiz isiklari kapatarak enerji tasarrufu yapin. Bir LED ampul, akkor ampulden %85 daha az enerji harcar.",
                "Yiyecek atiklarini kompost yaparak toprak verimliligi artirin. Dunya gida uretiminin ucte biri cope gidiyor.",
                "Ulasimda toplu tasima veya bisiklet tercih edin. Kisisel arac kullanimi sehir emisyonlarinin %30'undan sorumlu.",
                "Yerli ve mevsiminde uretilen gidalar satin alin. Gida kilomentresini azaltmak karbon ayak izini dusurur.",
                "Agac dikin ve yesil alanlari koruyun. Bir agac yilda ortalama 22 kg karbondioksit emer.",
            ],
            "mevsim_gozlem": (
                "Eylul ayi, sonbaharin baslangicidir. Yapraklar sararip dokulmeye baslar, "
                "gocmen kuslar guneye yonelir. Mese palamutu ve kestane toplanma zamanidir. "
                "Gece ve gunduz esitlenmeye baslar (ekinoks: 22-23 Eylul). Bahcedeki son "
                "domatesleri ve biberleri toplayin, kis sebzelerinin tohumlarini ekin. "
                "Sonbahar, dogadaki en gorsel mevsimlerden biridir - yapraklarin sari, "
                "turuncu ve kirmizi tonlarinda boyanmasi orman yuruyusleri icin ideal ortam sunar."
            ),
        },
        "edebiyat": {
            "kitap": "Kucuk Prens",
            "yazar": "Antoine de Saint-Exupery",
            "tur": "Roman / Masal", "sayfa": 96,
            "tanitim": (
                "1943'te yayimlanan Kucuk Prens, dunya edebiyatinin en cok okunan kitaplarindandir. "
                "300'den fazla dile cevrilmis bu basyapit, bir pilotun Sahra colunde karsilastigi "
                "kucuk bir prensin hikayesini anlatir. Asteroidi B-612'den gelen prens, farkli "
                "gezegenlerde farkli karakterlerle karsilasir ve her birinden hayata dair bir ders "
                "cikarir. Kitap, ilk yayimlandigindan bu yana 200 milyondan fazla kopya satmis "
                "ve tum zamanlarin en cok satan kitaplari arasina girmistir.\n\n"
                "Dostluk, sevgi ve sorumluluk temalarini isleyen eser, hem cocuklara hem "
                "yetiskinlere hitap eder. 'Gozle gorulemez, ancak kalple gorulur' mesaji kitabin "
                "en bilinen satirlarindan biridir. Tilki ile Kucuk Prens arasindaki 'ehlillestirme' "
                "diyalogu dunya edebiyatinin en etkileyici sahnelerinden biridir. Tilki, Kucuk "
                "Prens'e 'Sen benim icin daha dunyalardaki butun erkek cocuklara benziyorsun. "
                "Ama eger beni ehlillestirirsen, birbirimize ihtiyacimiz olacak' der.\n\n"
                "Kitap, buyuklerin dunya gorusunu elestirirken cocuksu masumiyetin ve safligin "
                "onemini vurgular. Saint-Exupery, kendi suluboya resimleriyle kitabi illustre "
                "etmis ve bu resimler kitabin ayrilmaz bir parcasi olmustur. Kitaptaki 'Boa "
                "yilani bir fili yutmus' resmi ve 'koyun kutusu' resimleri ikonik hale gelmistir. "
                "Her yasi ve kulturden okuyucular bu kucuk kitapta kendi hayatlarina dair derin "
                "anlamlar bulmaktadir.\n\n"
                "Kitabin felsefesi, materyalizm elestirisinden dostlugun degerine, sorumlulugun "
                "onemine kadar genis bir alanda derinlesir. Prensin ziyaret ettigi gezegenler "
                "birer alegoridir: iktidar hirsi, kibirlilik, alkolizm, materyalizm, korlukce "
                "kurallara baglIlik ve yuzeysel bilgi birikimi elestrilir. Kitap, okuyucusunu "
                "cocukken sahip oldugu safliga ve merak duygusuna geri donmeye davet eder."
            ),
            "yazar_bio": (
                "Antoine de Saint-Exupery (1900-1944), Fransiz yazar ve pilot. Lyon'da soylu "
                "bir ailenin cocugu olarak dogdu. Genclik yillarinda havaciligin buyuledi ve "
                "Kuzey Afrika ile Guney Amerika'da posta pilotlugu yapti. Ucus deneyimleri "
                "eserlerine ilham kaynagi oldu. 'Gece Ucusu' (1931) adli romani buyuk basari "
                "kazandi ve Andre Gide'in onsozuyle yayimlandi. II. Dunya Savasi'nda Fransa'nin "
                "isgalinden sonra ABD'ye gitti ve Kucuk Prens'i 1943'te New York'ta yazdi. "
                "1944 yilinda Akdeniz uzerinde bir kesif ucusu sirasinda kayboldu. Ucaginin "
                "enkazI ancak 2000 yilinda Marsilya aciklarinda bulundu. Olumu edebiyat "
                "dunyasinda derin bir uzuntuye yol acmis, eserleri olumunden sonra daha da "
                "buyuk bir un kazanmistir."
            ),
            "bu_ay_okuyun": [
                {"kitap": "Bereketli Topraklar Uzerinde", "yazar": "Orhan Kemal", "tur": "Roman", "sayfa": 256},
                {"kitap": "Saatleri Ayarlama Enstitusu", "yazar": "Ahmet Hamdi Tanpinar", "tur": "Roman", "sayfa": 396},
                {"kitap": "1984", "yazar": "George Orwell", "tur": "Distopya", "sayfa": 328},
                {"kitap": "Serenad", "yazar": "Zulfu Livaneli", "tur": "Tarihi Roman", "sayfa": 360},
                {"kitap": "Fareler ve Insanlar", "yazar": "John Steinbeck", "tur": "Novella", "sayfa": 112},
            ],
            "edebi_soz": {
                "soz": "Bir kitabi actiginizda, yazarin aklinin icine giriyorsunuz.",
                "kisi": "Orhan Pamuk",
            },
        },
        "siir": [
            {
                "baslik": "Gel",
                "sair": "Mevlana Celaleddin-i Rumi",
                "metin": (
                    "Gel, gel, ne olursan ol yine gel,\n"
                    "Ister kafir, ister Mecusi, ister puta tapan ol yine gel,\n"
                    "Bizim dergahimiz umutsuzluk dergahi degildir,\n"
                    "Yuz kere tovbeni bozmus olsan da yine gel.\n\n"
                    "Gel, dosta gel, bahara gel,\n"
                    "Kosarak gel, adim adim gel,\n"
                    "Ne olursan ol, nasil olursan ol,\n"
                    "Yeter ki gel, yeter ki gel."
                ),
                "bio": (
                    "Mevlana Celaleddin-i Rumi (1207-1273), Konya'da yasayan buyuk mutasavvif, "
                    "sair ve dusunur. Belh'te (bugunki Afganistan) dogdu, ailesiyle birlikte "
                    "uzun bir goc yolculugundan sonra Konya'ya yerlesti. Mesnevi adli eseri "
                    "26.000 beyitten olusan dunya edebiyatinin en buyuk yapitlarindan biridir. "
                    "Divan-i Kebir, Fihi Ma Fih ve Mektubat diger onemli eserleridir. Dusunceleri "
                    "yuzyillar sonra bile evrensel insani degerlere ilham vermeye devam etmektedir."
                ),
            },
            {
                "baslik": "Sonnet 18",
                "sair": "William Shakespeare",
                "metin": (
                    "Seni bir yaz gunune benzeteyim mi?\n"
                    "Sen daha hos, daha itidallisin;\n"
                    "Sert ruzgarlar mayisin goncalarini savurur,\n"
                    "Ve yazin kirasi pek de kisa surer.\n\n"
                    "Gogun gozu kimi cok sicak parlar,\n"
                    "Kimi altin yuzu bulutlarla kapanir;\n"
                    "Her guzellik bir gun guzelliginden duser,\n"
                    "Dogayla ya da zamanla susu solar.\n\n"
                    "Ama senin ebedi yazin solmayacak,\n"
                    "Ne sahip oldugun o guzellik yitecek;\n"
                    "Ne olum seni golgesinde gezdirmekle ovunecek,\n"
                    "Ebedi dizelerde zamanla buyuyeceksin."
                ),
                "bio": (
                    "William Shakespeare (1564-1616), Ingiliz oyun yazari ve sair. Stratford-upon-Avon'da "
                    "dogdu. 37 oyun, 154 sone ve uzun siirler yazdi. Hamlet, Romeo ve Juliet, Othello, "
                    "Macbeth ve Kral Lear eserleriyle dunya edebiyatinin en buyuk isimleri arasindadir. "
                    "Ingiliz dilini zenginlestiren 1.700'den fazla yeni kelime uretmistir."
                ),
            },
        ],
        "psikoloji": {
            "baslik": "Okula Donus Psikolojisi: Yeni Doneme Hazir misiniz?",
            "icerik": (
                "Yaz tatilinin ardindan okula donus donemi, ogrenciler icin hem heyecan hem de "
                "kaygi yaratabilen bir gecis suresidir. Yeni sinif, yeni ogretmenler ve artan "
                "akademik beklentiler dogal bir stres kaynagi olabilir. Ancak bu gecis surecini "
                "saglikli yonetmek tamamen mumkundur. Arastirmalar, okulun ilk haftasindaki "
                "deneyimlerin tum akademik yilin tonunu belirledigini gostermektedir. Bu nedenle "
                "bu gecis donemini bilinçli bir sekilde planlamak buyuk onem tasimaktadir.\n\n"
                "Ilk haftalarda uyku duzenini yeniden olusturmak kritik onem tasir. Yaz boyunca "
                "bozulmus olan biyolojik saat, okul baslangicından 1-2 hafta once kademeli olarak "
                "ayarlanmalidir. Gece 10'da yatip sabah 7'de kalkmak ideal bir rutindir. Melatonin "
                "hormonu karanlikta salgilandigindan, yatmadan once ekran kullanimini sonlandirmak "
                "uyku kalitesini arttirir. Yeterli uyku (8-10 saat) ogrencilerin dikkat, hafiza "
                "ve duygusal duzenleme kapasitelerini dogrudan etkiler.\n\n"
                "Sosyal kaygi yasayan ogrenciler icin okuldaki bir etkinlige veya kulube katilmak "
                "yeni arkadasliklar kurmak icin guzel bir firsattir. Ogretmenler de sinifta icerik "
                "islemeye baslamadan once tanisma etkinlikleri duzenleyerek ogrencilerin "
                "kaynasmalarini saglayabilir. Arastirmalar, okulda en az bir yakIn arkadaslIgI "
                "olan ogrencilerin akademik basarilarinin daha yuksek oldugunu gostermektedir.\n\n"
                "Hedef belirleme, motivasyonu artirmanin en etkili yollarindan biridir. 'Bu donem "
                "matematik notumu yukseltecegim' gibi somut ve olculebilir hedefler koymak, "
                "ogrencinin odaklanmasini kolaylastirir. SMART hedef belirleme yontemi "
                "(Spesifik, Olculebilir, Ulasïlabilir, Relevant, Zamanli) gencler icin cok "
                "faydali bir cerceve sunmaktadir. Hedefleri yazili olarak belirlemek ve duzenli "
                "araliklarla gozden gecirmek basari olasiligini yuzde kirk artirmaktadir."
            ),
            "rehberlik": (
                "Kariyer planlama, lise yillarinda baslamalidir. Ogrencilerin ilgi alanlari, "
                "yetenekleri ve degerleri dogrultusunda meslekleri arastirmasi onemlidir. Meslek "
                "tanitimlari, is yeri gezileri ve gonullu calismalar kariyer kesfinde yardimci "
                "olur. Holland'in mesleki ilgi envanterleri, ogrencilerin hangi alanlarla uyumlu "
                "olduklarini kesfetmelerini saglar. Okul rehberlik servisinden bireysel gorusme "
                "randevusu alarak bu sureci profesyonel destekle yuruyebilirsiniz. Erken "
                "donemde kariyer kesfine baslayan ogrencilerin universite tercihlerinden "
                "memnuniyet oranlari daha yuksek olduguogostermektedir."
            ),
            "stres_ipuclari": [
                "Derin nefes egzersizi: 4 saniye nefes al, 4 saniye tut, 4 saniye ver (4-4-4 teknigi).",
                "Gunluk 20 dakika fiziksel aktivite stres hormonlarini azaltir ve endorfin salgilatir.",
                "Sosyal destek agin: Arkadaslarinla, ailenle konusmayi ihmal etme; paylasilan yuk hafifler.",
                "Mola vermek tembellik degildir; beyninizin toparlanmasi icin zorunludur.",
                "Mukemmelliyetcilikten kacinin; 'yeterince iyi' de son derece degerlidir.",
                "Gunluk tutun - dusunce ve duygularinizi yaziya dokmek zihinsel netlik saglar.",
                "Dogada vakit gecirin - 20 dakikalik yesil alan yuruyusu kortizol seviyesini dusurur.",
            ],
            "ozguven": (
                "Ozguven, basariyla birlikte gelir ama basari icin de ozguven gerekir. "
                "Bu donguden cikmak icin kucuk hedefler koyun ve her basariyi kutlayin. "
                "Kendinizi baskalariyla degil, dunku halinizle karsilastirin. Hatalar "
                "basarisizlik degil, ogrenme firsatidir. 'Sabit zihniyet' yerine 'buyume "
                "zihniyeti' (growth mindset) benimsemek ozguvenin temelidir. Carol Dweck'in "
                "arastirmalari, yeteneklerin gelistirilebilir olduguna inanan ogrencilerin "
                "daha yuksek basari gostermektedir."
            ),
            "soru_cevap": [
                ("Sinavlarda cok heyecanlaniyorum, ne yapabilirim?",
                 "Sinav oncesi gece yeterli uyuyun, sabah dengeli kahvalti yapin. Sinav sirasinda ilk 2 dakikada derin nefes alin. Bildiginiz sorulardan baslayin, zor sorulari sona birakin. Sinav kaygisi yasayan ogrencilerin yuzde sekseni bu basit adimlarla kaygilarini kontrol altina alabilmektedir."),
                ("Derslerimi planlamakta zorlaniyorum.",
                 "Haftalik calisma plani olusturun. Her gunu ayni saatte calismayi aliskanlik haline getirin. Kucuk parcalara bolun, her 25 dakikada 5 dakika mola verin (Pomodoro). Ajanda veya dijital planlama araci kullanin."),
                ("Arkadaslik kurmakta gucluk cekiyorum.",
                 "Okuldaki bir kulube veya etkinlige katilmayi deneyin. Ortak ilgi alanlari paylasmak arkadaslik kurmanin en dogal yoludur. Kucuk adimlarla baslayin: selamlasmak, soru sormak ve dinlemek."),
            ],
        },
        "veli": {
            "baslik": "Yeni Doneme Hazirlik: Velilere Kapsamli Rehber",
            "icerik": (
                "Cocugunuzun okula donus heyecanini ve kaygisini anlamak, saglikli bir gecis icin "
                "ilk adimdir. Evde olumlu bir ogrenme ortami olusturmak, akademik basarinin "
                "temelini atar. Cocugunuza guvendiginizi ve destekleyeceginizi hissettirin. "
                "Bu donemde cocuklarin duygusal ihtiyaclarini karsilamak, akademik beklentiler "
                "kadar onemlidir. Cocugunuzu dinleyin, duygularini ifade etmesine izin verin.\n\n"
                "Duzensiz calisma aliskanliklari, akademik basariyi olumsuz etkileyen en yaygin "
                "sorunlardan biridir. Cocugunuz icin sabit bir calisma saati belirleyin ve bu "
                "saatlerde televizyon, telefon gibi dikkat dagitici unsurlari ortadan kaldirin. "
                "Calisma masasi duzenli, aydinlik ve sessiz olmalidir. Arastirmalar, her gun "
                "ayni saatte ve ayni yerde calisan ogrencilerin yuzde otuz daha verimli "
                "oldugunu gostermektedir. Calisma rutini kurmak icin ilk 21 gun disiplin "
                "gerektirir, sonrasinda aliskanlik haline gelir.\n\n"
                "Okul-aile isbirligi basarinin en onemli belirleyicilerinden biridir. Ogretmenlerle "
                "duzenli iletisim kurmak, veli toplantilarina katilmak ve gerektiginde bireysel "
                "gorusmeler talep ederek cocugunuzun gelisimini yakindan takip edin. Ogretmenle "
                "isbirligi icinde olan velilerin cocuklari, hem akademik hem de sosyal acidan "
                "daha basarili olmaktadir.\n\n"
                "Dijital dunya da velilerin dikkatle yonetmesi gereken bir alandir. Ekran suresi "
                "sinirlamalari, uygun icerik filtreleri ve interneti birlikte kullanma aliskanligi "
                "cocugunuzun guvenligini saglar. Amerikan Pediatri Akademisi, okul cagi cocuklari "
                "icin gunluk 2 saatten fazla rekreasyonel ekran suresi onermemektedir. Yatmadan "
                "en az 1 saat once ekranlardan uzak durmak uyku kalitesini arttirir.\n\n"
                "Cocugunuzun sosyal gelisimini de desteklemeyi ihmal etmeyin. Arkadaslarina "
                "davet etmesine, okul disi etkinliklere katilmasina tesvik edin. Empati, "
                "paylasma ve catisma cozme becerileri aile ortaminda ogrenilir ve okulda "
                "pekistirilir."
            ),
            "ev_ortami": [
                "Sabit bir calisma kosesi olusturun - yatak odasindan farkli bir alan idealdir.",
                "Yeterli aydinlatma (dogal isik tercih edin) ve ergonomik oturma duzeni saglayin.",
                "Calisma saatlerinde ekran erisimini sinirlayin (telefon baska odada kalmali).",
                "Referans kitaplari ve sozlukler kolay erisilebilir olsun.",
                "Calisma sonrasi kisa bir mola ve kucuk odul sistemi uygulayin.",
                "Sessiz bir ortam saglayin - arka plan gurultusu konsantrasyonu yuzde kirk azaltir.",
            ],
            "iletisim": (
                "Cocugunuzla acik ve yargilayici olmayan bir iletisim kurun. 'Bugun okulda ne "
                "ogrendin?' yerine 'Bugun en cok neyin hosuna gitti?' gibi acik uclu sorular sorun. "
                "Basarisizlik anlarinda elestirmek yerine cozum odakli yaklasim gosterin. "
                "'Bu sefer olmadi ama bir dahaki sefere farkli ne yapabilirsin?' sorusu cocugunuza "
                "problem cozme becerisi kazandirir. Aktif dinleme teknigi uygulayarak cocugunuzun "
                "soylediklerini tekrarlayin ve duygularini yansityn: 'Anladim, bu seni uzmus.' "
                "Bu yaklasim cocugunuzun kendini degerli ve anlasilmis hissetmesini saglar."
            ),
            "beslenme": [
                "Kahvalti atlamamak: Beyinin ana yakiti glukozdur, sabah kahvaltisi performansi %20 arttirir.",
                "Omega-3 iceren gidalar: Balik, ceviz, keten tohumu - noronlar arasi iletisimi guclendirir.",
                "Yeterli su tuketimi: Gunluk 1.5-2 litre su, %2 dehidratasyon bile konsantrasyonu %25 dusurur.",
                "Seker tuketimini sinirlayin: Asiri seker ani enerji ve sonrasinda cokuse neden olur.",
                "Demir iceren gidalar: Kirmizi et, ispanak, mercimek - oksijen tasimasi icin kritik.",
                "B vitamini grubunu ihmal etmeyin: Tam tahillar, yumurta, sut - sinir sistemi icin onemli.",
            ],
            "aile_etkinlik": (
                "Hafta sonlari aile olarak bir muzey ziyareti, dogada yuruyus veya birlikte kitap "
                "okuma saati planlayabilirsiniz. Bu etkinlikler hem aile baglarini guclendirir hem "
                "de cocugunuzun kulturel ve entelektuel gelisimini destekler. Ayda bir 'aile film "
                "gecesi', haftada bir 'birlikte yemek pisirme' gibi gelenekler olusturun. "
                "Cocugunuzla board game oynamak stratejik dusunme ve sosyal becerileri gelistirir."
            ),
        },
        "ogrenci_tavsiye": {
            "baslik": "Yeni Doneme Guclu Bir Baslangic",
            "icerik": (
                "Basarili bir akademik donem icin ilk hafta kritik oneme sahiptir. Derslerinizin "
                "genel yapisini anlayin, ogretmenlerinizin beklentilerini ogreni ve defterlerinizi "
                "organize edin. Ilk haftanin ritmi genellikle tum doneme yansir. Bir ders icin ayri "
                "birer defter veya klasor kullanmak, not duzenliliginizi arttirir. Dijital not alma "
                "araclari (Notion, OneNote) da iyi alternatiflerdir ancak elle yazmak hafizayi daha "
                "iyi destekler.\n\n"
                "Not alma becerisi, akademik basarinin en onemli destekleyicilerinden biridir. "
                "Cornell not alma yontemi, ana fikirleri, destekleyici detaylari ve ozet bolumunu "
                "sistematik olarak duzenlemenizi saglar. Dersten sonra notlarinizi ayni gun gozden "
                "gecirmek, hatirlamayi yuzde altmis arttirir. Mind mapping (zihin haritalari) "
                "ozellikle gorsel ogrenenler icin cok etkili bir yontemdir. Konular arasindaki "
                "iliskileri gorsellestirerek buyuk resmi gormenizi saglar.\n\n"
                "Grup calismasi dogru uygulandiginda son derece etkilidir. 3-4 kisilik gruplar "
                "ideal boyuttadir. Her uye konunun farkli bir bolumunu hazirlar ve gruba sunar. "
                "Bu yontem hem ogretmeyi hem ogrenmeyi guclendirir. 'Feynman Teknigi' olarak "
                "bilinen bu yaklasimda, bir konuyu baskasina basit kelimelerle anlatabiliyorsaniz "
                "o konuyu gercekten anladiniz demektir. Grup calismasinda dikkat dagitici "
                "konusmalardan kacinmak icin oncelikle gundem belirleyin.\n\n"
                "Zaman yonetimi akademik basarinin temel tasidir. Eisenhower Matrisi ile "
                "gorevlerinizi 'Acil ve Onemli', 'Onemli ama Acil Degil', 'Acil ama Onemli "
                "Degil' ve 'Ne Acil Ne Onemli' kategorilerine ayirarak onceliklendirin. "
                "Cogu ogrenci zamanini ucuncu kategoride harcar; oysaki ikinci kategori "
                "uzun vadeli basari icin en kritik olandir.\n\n"
                "Fiziksel sagliginizi ihmal etmeyin. Gunluk 30 dakika egzersiz, 8 saat uyku "
                "ve dengeli beslenme beyin performansinizi dogrudan etkiler. Sabah erken "
                "kalkmak ve gune planli baslamak ustun basarili ogrencilerin ortak ozelligidir."
            ),
            "aliskanliklar": [
                "Her gun ayni saatte calisma rutini olusturun.",
                "Calisma oncesi 5 dakika hedef belirleyin, sonra o hedefe odaklanin.",
                "Tek seferde tek konuya odaklanin (multitasking verimsizdir).",
                "Ogrendiklerinizi baskasina anlatarak pekistirin (Feynman Teknigi).",
                "Gecmis konulari birikmeye birakmadan hemen tamamlayin.",
                "Yeni kelimeleri ve kavramlari bir sozluk defterinde takip edin.",
                "Sinav oncesi degil, her gun duzenli tekrar yapin.",
                "Hata yapmayi ogrenme firsati olarak gorun - buyume zihniyeti benimseyin.",
                "Rekabeti baskalariyla degil, kendinizle yapin.",
                "Her basariyi kutlayin, motivasyonunuzu yuksek tutun.",
            ],
            "sinav_hazirlik": (
                "Sinav hazirlik plani: 1) Sinav tarihinden 2 hafta once baslayin. "
                "2) Konulari kucuk parcalara bolun ve takvime dagintin. 3) Her gun 2-3 konu "
                "tekrar edin. 4) Kendinize mini testler uygulayin (aktif geri cagirma). "
                "5) Son 3 gun genel tekrar yapin. 6) Sinav oncesi gece yeni konu calismak "
                "yerine bildiklerinizi gozden gecirin ve erken yatin. 7) Sinav sabahi hafif "
                "kahvalti yapin ve 10 dakika erken gidin."
            ),
            "motivasyon_sozleri": [
                '"Basari, kucuk cabalarin her gun tekrarlanan toplamidir." - Robert Collier',
                '"Gelecegi tahmin etmenin en iyi yolu, onu olusturmaktir." - Abraham Lincoln',
                '"Bin millik yolculuk tek bir adimla baslar." - Lao Tzu',
                '"Basarisizlik, basariya giden yoldaki bir basamaktir." - C.S. Lewis',
                '"Eger bir ruyaniz varsa, onu gerceklestirecek guciniz de var demektir." - R.W. Emerson',
            ],
            "haftalik_plan": (
                "Pazartesi: Matematik + Fen (gunduz) | Sali: Turkce + Tarih | "
                "Carsamba: Ingilizce + Cografya | Persembe: Matematik + Fen tekrar | "
                "Cuma: Zayif konulara ek calisma | Cumartesi: Genel tekrar + test cozu | "
                "Pazar: Hafif okuma + dinlenme + gelecek hafta planlama"
            ),
        },
        "kultur_sanat": {
            "baslik": "Dunya Cocuk Edebiyatinin Donum Noktalari",
            "icerik": (
                "Cocuk edebiyatinin tarihi, 1658'de Jan Amos Comenius'un yazdigi 'Orbis Pictus' "
                "adli resimli ansiklopediye kadar uzanir. Bu eser, gorselleri egitim araci olarak "
                "kullanan ilk kitaplardan biri olarak kabul edilir. Comenius, cocuklarin gorsel "
                "uyaranlarla daha iyi ogrendigini kavramis ve bu anlayis bugun bile gecerliligini "
                "korumaktadir.\n\n"
                "Lewis Carroll'in 1865'te yazdigi 'Alice Harikalar Diyarinda' cocuk edebiyatinda "
                "bir devrim yaratti. Didaktik olmayan, tamamen hayal gucune dayanan bu eser modern "
                "cocuk edebiyatinin kapilarini araladi. Carroll, Oxford Universitesi'nde matematik "
                "profesoruydu ve kitabindaki mantik bulmacalari matematiksel dusunceyi yansitir. "
                "Ayna Ulkesindeki Alice ise dil felsefesi uzerine derin gondermelar icerir.\n\n"
                "20. yuzyilda Saint-Exupery'nin 'Kucuk Prens'i, Tolkien'in 'Hobbit'i ve "
                "Lindgren'in 'Pippi Uzuncrap'i cocuk edebiyatina yeni boyutlar kazandirdi. "
                "J.K. Rowling'in Harry Potter serisi ise 21. yuzyilin en buyuk edebiyat "
                "fenomenlerinden biri oldu ve 500 milyondan fazla kopya satti. Potter serisi "
                "cocuklari okumaya tesvik etmede dunyanin en etkili eseri olarak kabul edilir.\n\n"
                "Turk cocuk edebiyati da zengin bir gelenegedahiptir. Tevfik Fikret'in 'Sis' "
                "siiri, Eflatun Cem Guney'in masallari, Muzaffer Izgu'nun 'Okuldan Kacma Plani' "
                "ve Gulten Dayioglu'nun eserleri Turk cocuk edebiyatinin mihenk taslaridir. "
                "Cahit Sitki Taranci'nin cocukluk siirlerinden Fazil Husnu Daglarca'nin resimli "
                "kitaplarina kadar genis bir yelpaze bulunmaktadir.\n\n"
                "Gunumuzde cocuk edebiyati, cesitlilik ve kapsayicilik temiyle buyuk bir donusum "
                "yasemaktadir. Farkli kulturlerden, engelli bireylerden ve az temsil edilen "
                "gruplardan karakterler artik cocuk kitaplarinda daha fazla yer almaktadir. "
                "Dijital cagda interaktif e-kitaplar ve sesli kitaplar da yeni nesil okuyuculara "
                "ulasmanin yeni yollarini sunmaktadir."
            ),
            "film": {
                "ad": "Dead Poets Society (Olu Ozanlar Dernegi)",
                "yonetmen": "Peter Weir", "yil": 1989,
                "aciklama": (
                    "Robin Williams'in unutulmaz performansiyla hayat bulan bu film, bir edebiyat "
                    "ogretmeninin geleneksel bir erkek yatili okulunda ogrencilerini ozgur dusunmeye "
                    "tesvik etmesini anlatir. 'Carpe Diem - Gunu Yakala' sozuyle ikoniklesen film, "
                    "egitim ve bireysellesmeyi sorgulayan bir basyapittir. Film, ozellikle genç "
                    "izleyiciler uzerinde derin bir etki birakir ve ogretmen-ogrenci iliskisinin "
                    "donusturucu gucunu etkileyici bir sekilde gozler onune serer."
                ),
            },
            "muzik": {
                "baslik": "Klasik Muzige Giris",
                "aciklama": (
                    "Klasik muzik, yuzyillar boyunca gelisen zengin bir gelenegin urunudur. "
                    "Bach'in Brandenburger Koncerti, Mozart'in 40. Senfoni ve Beethoven'in "
                    "Ay Isigi Sonati giris icin ideal eserlerdir. Vivaldi'nin Dort Mevsim'i ise "
                    "dunya genelinde en cok taninan klasik eserlerden biridir. Turkiye'de Fazil "
                    "Say, dunya capinda taninan bir klasik piyanist ve besteci olarak ulkemizi "
                    "temsil etmektedir. Idil Biret de Turkiye'nin yetistirdigi en onemli "
                    "piyanistlerden biridir."
                ),
            },
            "sanat_eseri": {
                "ad": "Yildizli Gece",
                "sanatci": "Vincent van Gogh", "yil": 1889,
                "aciklama": (
                    "Van Gogh'un en unlu tablosu, Saint-Remy-de-Provence'deki akil hastanesinin "
                    "penceresinden gordugu gece manzarasini betimler. Sarmal bulutlar, parlak "
                    "yildizlar ve kucuk bir koy... Tabloda kullanilan canli renkler ve dinamik "
                    "firca darbeleri post-empresyonizmin en etkileyici orneklerinden birini "
                    "olusturur. Eser MoMA'da (New York Modern Sanat Muzesi) sergilenmektedir. "
                    "Van Gogh, yasaminda yalnizca bir tablo satmis olmasina ragmen, olumunden "
                    "sonra dunya tarihinin en etkili sanatcilarindan biri olarak kabul edilmistir."
                ),
            },
            "muze": (
                "Bu ay ziyaret onerisi: Istanbul Arkeoloji Muzeleri. 1891'de Osman Hamdi Bey "
                "tarafindan kurulmus olan muze kompleksi, uc ana binadan olusmaktadir: Arkeoloji "
                "Muzesi, Eski Sark Eserleri Muzesi ve Cinili Kosk. Dunyanin en zengin arkeoloji "
                "koleksiyonlarindan birini barindirir. Iskender Lahdi, Sidon Krallari Nekropolu "
                "eserleri ve Kadesh Antlasmasi tableti en onemli parcalar arasindadir. Kadesh "
                "Antlasmasi, dunya tarihinin bilinen ilk yazili baris antlasmasidir."
            ),
        },
        "spor": {
            "baslik": "Yeni Sezon Basliyor - Olimpiyat Sporlari Rehberi",
            "icerik": (
                "Modern Olimpiyat Oyunlari 1896 yilinda Atina'da Pierre de Coubertin'in onderligi "
                "ile basladi. Bugun 200'den fazla ulkeden 10.000'i askin sporcuyu bir araya getiren "
                "en buyuk uluslararasi spor organizasyonudur. Yaz Olimpiyatlari'nda 32 farkli "
                "dalda yarisma yapilir. Olimpiyat ruhu; mükemmellik, dostluk ve saygi degerleri "
                "uzerine kuruludur.\n\n"
                "Atletizm, yuzme ve jimnastik en cok takip edilen branslardir. Usain Bolt'un "
                "100 metredeki 9.58 saniyelik dunya rekoru insanligin hiz sinirlarini zorlamaktadir. "
                "Michael Phelps, 23 altin madalyasiyla tum zamanlarin en basarili Olimpiyat "
                "sporcusudur. Simone Biles jimnastikte devrim yaratmis, kendi adini tasiyan "
                "hareketlerle spor tarihine gecmistir.\n\n"
                "Turkiye, Olimpiyat tarihinde gures, halter ve tekvando dallarinda buyuk basarilar "
                "elde etmistir. Naim Suleymanoglu 3 kez ust uste Olimpiyat sampiyonu olarak 'Cep "
                "Herkulu' lakabini kazandi. Halil Mutlu da 3 altin madalyayla tarihe gecti. "
                "Busenaz Surmeneli, 2020 Tokyo Olimpiyatlari'nda boks dalinda altin madalya "
                "kazanarak Turk sporuna yeni bir basari ekledi.\n\n"
                "Okul sporlari, ogrencilerin fiziksel gelisimi yaninda takim calismasi, disiplin "
                "ve fair play gibi degerler kazanmasini saglar. Her ogrencinin en az bir spor "
                "dalinda aktif olmasi ozendirilmektedir. Okul takim sporlari (basketbol, voleybol, "
                "futbol) sosyallesme ve liderlik becerilerini gelistirmede cok etkilidir. Bireysel "
                "sporlar (yuzme, atletizm, tenis) ise ozguven ve oz-disiplin kazandirir.\n\n"
                "Spor psikolojisi, zihinsel hazirligin fiziksel performans kadar onemli oldugunu "
                "vurgulamaktadir. Gorsellestirme, olumlu ic konusma ve hedef belirleme teknikleri "
                "profesyonel sporcular tarafindan yaygin olarak kullanilmaktadir."
            ),
            "spor_tarihi": (
                "Antik Olimpiyat Oyunlari MO 776'da Yunanistan'in Olympia sehrinde basladi. "
                "Yaklasik 1.170 yil boyunca her dort yilda bir duzenlendi. Baslangiçta yalnizca "
                "kisa mesafe kosusu (stadion) varken zamanla boks, gures, arabya yarislari ve "
                "pentatlon eklendi. MS 393'te Bizans Imparatoru I. Theodosius tarafindan "
                "yasaklandi. 1.503 yil aranindan sonra Pierre de Coubertin'in gayretleriyle "
                "1896'da Atina'da modern Olimpiyatlar yeniden basladi."
            ),
            "ayin_sporcusu": {
                "ad": "Naim Suleymanoglu",
                "dal": "Halter",
                "bilgi": (
                    "1967-2017. Bulgaristan'da dogdu, 1986'da Turkiye'ye iltica etti. 1988 Seul, "
                    "1992 Barcelona ve 1996 Atlanta Olimpiyatlarinda altin madalya kazandi. 'Cep "
                    "Herkulu' ve 'Pocket Hercules' lakabiyla taninan Naim, vucut agirliginin 3 "
                    "katini kaldiran dunyanin tek halter sporcusuydu. 46 dunya rekoru kirdi ve "
                    "halterin dunyadaki en taninmis yuzu oldu. 2017'de hayatini kaybetmesiyle "
                    "Turkiye ve dunya spor camiasi buyuk bir kaybini yasadi."
                ),
            },
            "saglik_ipucu": (
                "Gunluk 60 dakika fiziksel aktivite, genc bedenler icin idealdir. Kisa ama "
                "duzenli egzersizler (10 dk sabah kosusu + 10 dk esneme), uzun ama duzensiz "
                "antrenmanlardan daha etkilidir. Bol su icmeyi ve egzersiz oncesi 5-10 dakika "
                "isinmayi unutmayin! Egzersiz sirasinda vucudunuzu dinleyin; agri hissederseniz "
                "durun. Spor oncesi ve sonrasi stretching yaralanma riskini yuzde elli azaltir."
            ),
        },
        "ozlu_sozler": [
            {"soz": "Bir kitabi bin kere okumak, bin kitabi bir kere okumaktan iyidir.", "kisi": "Mevlana", "kategori": "Edebiyat"},
            {"soz": "Egitim, bir kovaya su doldurmak degil, bir atesi yakmaktir.", "kisi": "W. B. Yeats", "kategori": "Egitim"},
            {"soz": "Hayatta en hakiki mursit ilimdir.", "kisi": "Mustafa Kemal Ataturk", "kategori": "Bilim"},
            {"soz": "Dusunuyorum, o halde varim.", "kisi": "Rene Descartes", "kategori": "Felsefe"},
            {"soz": "Bilgi guctur.", "kisi": "Francis Bacon", "kategori": "Bilim"},
            {"soz": "Ogrenmenin siniri yoktur.", "kisi": "Konfucyus", "kategori": "Egitim"},
            {"soz": "Kendini bil.", "kisi": "Sokrates", "kategori": "Felsefe"},
            {"soz": "Bir toplumu degistirmek istiyorsaniz, egitimi degistirin.", "kisi": "Nelson Mandela", "kategori": "Liderlik"},
            {"soz": "En buyuk zafer, kendini yenmektir.", "kisi": "Platon", "kategori": "Felsefe"},
            {"soz": "Ogretmenim diyen ogrenmeyi birakmistir.", "kisi": "Hz. Ali", "kategori": "Egitim"},
            {"soz": "Hayal gucu bilgiden daha onemlidir.", "kisi": "Albert Einstein", "kategori": "Bilim"},
            {"soz": "Kaleminizi kirmayin, cunku kalem kilictan keskindir.", "kisi": "II. Mahmud", "kategori": "Liderlik"},
            {"soz": "Dunya bir kitaptir ve seyahat etmeyenler yalnizca bir sayfasini okur.", "kisi": "Aziz Augustinus", "kategori": "Edebiyat"},
            {"soz": "Basarinin sirri, baslamaktir.", "kisi": "Mark Twain", "kategori": "Liderlik"},
            {"soz": "Zaman en iyi ogretmendir; ne yazik ki tum ogrencilerini oldurur.", "kisi": "Hector Berlioz", "kategori": "Felsefe"},
        ],
        "bilmeceler": [
            ("Dal ustunde iki satir, biri altin biri katir.", "Goz kapaklari ve kirpikler"),
            ("Bir koyun iki kuzu, biri ak biri boz kuzu.", "Dil ve dudaklar"),
            ("Karsi dagda bir agac, yapragi yok dali yok, dalinca meyve verir.", "Su kaynagi (pinar)"),
            ("Uc ayakli catal kasik, yemek yemez yorganli.", "Sacayagi"),
            ("Altindan aslan yukari cikar, yukaridaki aslan asagi iner.", "Terazi"),
            ("Ne kadar buyurse o kadar hafifler.", "Balon"),
            ("Girer bir delikten cikar bin delikten.", "Dugme"),
            ("Agzi var dili yok, dili var agzi yok.", "Mektup ve terazi"),
        ],
        "mantik_sorulari": [
            ("Bir coban 17 koyunu olan bir ciftciye gider. Yolda 9 koyun kacar. Kac koyun kalir?", "8 koyun kalir (17-9=8)"),
            ("Bir odada 3 lamba var. Disarida 3 dugme var. Odaya bir kez girebilirsiniz. Hangi dugme hangi lambayi aciyor nasil anlarsiniz?",
             "1. dugmeyi 5 dk acik tutun, kapatin. 2. dugmeyi acin. Odaya girin. Yanan lamba 2. dugmenin, sicak olan 1. dugmenin, soguk olan 3. dugmenindir."),
            ("Bir adam yagmurda sehir merkezinde yuruyordu. Semsiyesi yoktu, sapkasi yoktu. Ustu islandi ama saci islanmadi. Nasil?",
             "Adam keldi."),
        ],
        "matematik_bulmacalari": [
            "3 + 3 x 3 - 3 + 3 = ? (Islem onceligi kuralina dikkat!)",
            "123 + 456 + 789 = ? (Sonucu 5 saniyede hesaplayin)",
            "Bir sayinin 3 kati ile 5'in toplami 20'dir. Sayi kactir?",
            "1 + 2 + 3 + ... + 100 = ? (Gauss'un formulu!)",
        ],
        "matematik_cevaplar": ["12", "1368", "5", "5050"],
        "kim_bu": {
            "ipuclari": [
                "Turkiye Cumhuriyeti'nin kurucusudur.",
                "1881'de Selanik'te dogmustur.",
                "Modern Turkiye'nin temellerini atan reformlari gerceklestirmistir.",
                "Liderlik, vizyon ve kararlilik sembolu olarak tum dunya tarafindan taninir.",
            ],
            "cevap": "Mustafa Kemal Ataturk",
        },
        "quiz": [
            {"soru": "Insan beyni yaklasik kac norondan olusur?", "secenekler": ["A) 10 milyar", "B) 50 milyar", "C) 86 milyar", "D) 200 milyar"], "cevap": "C", "zorluk": 1},
            {"soru": "Noroplastisite ne demektir?", "secenekler": ["A) Beyin buyumesi", "B) Beynin yeniden sekillenmesi", "C) Hafiza kaybi", "D) Sinir iltihabi"], "cevap": "B", "zorluk": 2},
            {"soru": "Kuzey Kutbu sumru kusu yilda yaklasik kac km goc eder?", "secenekler": ["A) 10.000 km", "B) 30.000 km", "C) 50.000 km", "D) 70.000 km"], "cevap": "D", "zorluk": 2},
            {"soru": "Dunyanin en eski universitesi hangisidir?", "secenekler": ["A) Oxford", "B) Bologna", "C) El-Karaviyyin", "D) Cambridge"], "cevap": "C", "zorluk": 1},
            {"soru": "Modern Olimpiyat Oyunlari hangi yil basladi?", "secenekler": ["A) 1880", "B) 1896", "C) 1900", "D) 1912"], "cevap": "B", "zorluk": 1},
            {"soru": "'Kucuk Prens' kimin eseridir?", "secenekler": ["A) Victor Hugo", "B) Jules Verne", "C) Saint-Exupery", "D) Albert Camus"], "cevap": "C", "zorluk": 1},
            {"soru": "Istanbul Bogazi kac km uzunlugundadir?", "secenekler": ["A) 15.2 km", "B) 22.5 km", "C) 31.7 km", "D) 45.0 km"], "cevap": "C", "zorluk": 2},
            {"soru": "Aralikli tekrar teknigi ogrenmeyi ne kadar artirir?", "secenekler": ["A) %10", "B) %25", "C) %50", "D) %75"], "cevap": "C", "zorluk": 2},
            {"soru": "Hangi vitamin gunes isigiyla sentezlenir?", "secenekler": ["A) A vitamini", "B) B12 vitamini", "C) C vitamini", "D) D vitamini"], "cevap": "D", "zorluk": 1},
            {"soru": "Naim Suleymanoglu hangi dalda Olimpiyat sampiyonu olmustur?", "secenekler": ["A) Gures", "B) Halter", "C) Boks", "D) Tekvando"], "cevap": "B", "zorluk": 1},
            {"soru": "'Yildizli Gece' tablosu kimin eseridir?", "secenekler": ["A) Picasso", "B) Monet", "C) Van Gogh", "D) Da Vinci"], "cevap": "C", "zorluk": 1},
            {"soru": "Pomodoro teknikinde calisma suresi kac dakikadir?", "secenekler": ["A) 15 dk", "B) 20 dk", "C) 25 dk", "D) 30 dk"], "cevap": "C", "zorluk": 2},
            {"soru": "Kapali Carsi hangi yildan beri faaliyet gostermektedir?", "secenekler": ["A) 1326", "B) 1453", "C) 1461", "D) 1520"], "cevap": "C", "zorluk": 2},
            {"soru": "Omega-3 en cok hangi gidada bulunur?", "secenekler": ["A) Kirmizi et", "B) Balik", "C) Peynir", "D) Ekmek"], "cevap": "B", "zorluk": 1},
            {"soru": "Cornell not alma yonteminde kac bolum vardir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": "B", "zorluk": 3},
        ],
        "quiz_puan_rehberi": "0-5: Tekrar gerekli | 6-9: Iyi | 10-12: Cok Iyi | 13-15: Mukemmel!",
        "okuyucu_mektuplari": [
            {"ad": "Elif K., Ankara", "mesaj": "Derginin ilk sayisini sabrsizlikla bekliyorduk. Bilim yazilari cok bilgilendirici, tesekkurler!"},
            {"ad": "Mehmet A., Istanbul", "mesaj": "Bulmaca bolumu harika! Her ay daha fazla bulmaca olsun lutfen."},
            {"ad": "Zeynep D., Izmir", "mesaj": "Siir kosesi cok guzel. Genc sairlerin siirlerine de yer vermenizi isteriz."},
        ],
        # YENi BÖLÜMLER
        "hobi_kosesi": {
            "baslik": "Hobi Kosesi",
            "hobiler": [
                {"ad": "Origami", "aciklama": "Kagit katlama sanati Japonya'dan dunya'ya yayilmistir. Bir kare kagitla kus, cicek, yildiz gibi sekiller yapabilirsiniz. Origami el-goz koordinasyonunu gelistirir, sabrı ogretir ve yaraticilik kazandirir. Baslangic icin vinc (tsuru) modeli idealdir — Japonlarda bin vinc katlayana bir dilek hakkı verildigi inanilir.", "emoji": "🦢"},
                {"ad": "Makrome", "aciklama": "Dugum atma sanati olan makrome, dekoratif duvar susleri, bileklikler ve canta yapiminda kullanilir. Temel olarak dort dugum tipi vardir: duz dugum, spiral dugum, kare dugum ve yarım kare dugum. Dogal pamuk ipleri ile baslayabilirsiniz. Makrome meditasyon gibi rahatlatici bir etkiye sahiptir.", "emoji": "🧶"},
                {"ad": "Astronomi Gozlemi", "aciklama": "Gece gokyuzunu gozlemlemek en eski ve en buyuleyici hobilerden biridir. Basit bir duubuunle Ay'in kraterlerini, Jupiter'in uydularini gorebilirsiniz. Isik kirliligi az olan bolgeler en iyi gozlem noktalarıdır. Yildiz haritasi uygulamalari ile takimyildizlari tanimayi ogrenebilirsiniz.", "emoji": "🔭"},
                {"ad": "Herbaryum", "aciklama": "Bitki orneklerini kurutarak koleksiyon yapmak hem bilimsel hem sanatsal bir hobidir. Yapraklari agiir bir kitabin arasinda kurutun, etiketleyin ve bir deftere yapisstirin. Zaman icinde zengin bir bitki arsivi olusuusturabilirsiniz. Biyoloji derslerinde buyuk avantaj saglar.", "emoji": "🌿"},
            ],
            "ipucu": "Yeni bir hobi baslatmak icin sadece merak ve 15 dakikalik gunluk pratik yeterlidir. Kendinize baski yapmayin, sureci keyifli hale getirin.",
        },
        "ilginc_bilgiler": [
            "Bir insanin omru boyunca urettigi tukuruk miktari iki yuzme havuzunu doldurabilir.",
            "Dunyanin en uzun yer alti nehri Meksika'daki Sac Actun sistemidir — 350 km uzunlugunda.",
            "Bir sivrisinegin 47 disi vardir.",
            "Isik Gunes'ten Dunya'ya 8 dakika 20 saniyede ulasir.",
            "Bir insan beyni gunde yaklasik 20 watt enerji harcar — bir ampul kadar.",
            "Dunya uzerinde insanlardan daha fazla karinca yasamaktadir — tahminen 20 katrilyon.",
            "Bir kelebegin kanatlarindaki renkler pigment degildir, isik kirinimindan olusur.",
            "Venüs gezegeni kendi ekseni etrafinda donerek bir gunu tamamlamasi icin 243 Dunya gunu gerekir.",
            "Insan gozu yaklasik 10 milyon farkli rengi ayirt edebilir.",
            "Dunyanin en eski agaci 'Methuselah' adi verilen ciriis camıdır — 4.856 yasindadir.",
            "Bir buluttaki ortalama su miktari yaklasik 500 tondur.",
            "Einstein 4 yasina kadar konusamamisstir.",
            "Bir insan hayati boyunca ortalama 5 yilini yemek yiyerek gecirir.",
            "Ay her yil Dunya'dan 3.8 cm uzaklassmaktadir.",
            "Bir ahtapotun uc kalbi ve mavi kani vardir.",
        ],
        "eglence_kosesi": {
            "fikralar": [
                "Ogretmen: 'Dunyanin en buyuk nehri hangisidir?' Ogrenci: 'Bilemem hocam, dunyadaki tum nehirleri olcmedim ki!'",
                "Matematik ogretmeni: '5 elmaniz var, 3 tanesini verdiniz. Kac elmaniz kaldi?' Ogrenci: '5 elma. Kimseye vermem!'",
                "Baba: 'Okulda ne ogrendin?' Cocuk: 'Yeterince degil, yarin yine gitmem gerekiyor.'",
            ],
            "bilgi_yarismasi": [
                {"soru": "Dunyanin en kucuk ulkesi hangisidir?", "cevap": "Vatikan"},
                {"soru": "Insan vucudundaki en buyuk organ hangisidir?", "cevap": "Deri"},
                {"soru": "Hangi gezegen 'Kizil Gezegen' olarak bilinir?", "cevap": "Mars"},
                {"soru": "DNA'nin acilimi nedir?", "cevap": "Deoksiribonukleik Asit"},
                {"soru": "Dunyanin en derin okyanus cukuru hangisidir?", "cevap": "Mariana Cukuru"},
            ],
            "labirent_aciklama": "Asagidaki labirentte giris noktasindan (A) cikis noktasina (B) ulasmanin en kisa yolunu bulun. Dikkat: Bazi yollar cikmaz sokaklardir!",
        },
        "felsefe_kosesi": {
            "baslik": "Dusunce Dunyasi",
            "filozof": {"ad": "Sokrates", "donem": "MO 470-399", "ulke": "Antik Yunanistan",
                "biyografi": "Bati felsefesinin kurucusu kabul edilen Sokrates, hicbir yazi birakmamistir. Ogretileri ogrencisi Platon tarafindan aktarilmistir. 'Sorgulanan bir hayat yasanmaya degmez' sozuyle taninir. Diyalektik yontemiyle — sorular sorarak — muhatabini dusunmeye yonlendirirdi.",
                "temel_fikir": "Erdem bilgidir. Kimse bilerek kotu davranmaz. Gercek bilgelik, bilmedigini bilmektir.",
            },
            "dusunce_sorusu": "Bir ormanda bir agac devrilse ve onu duyan kimse olmasa, ses cikarir mi? Bu soru gerceklik ile algi arasindaki iliskiyi sorgular.",
            "sozler": [
                '"Tek bildigim, hicbir sey bilmedigimdir." - Sokrates',
                '"Hayat anlasilmak icin degil, yasanmak icin vardir." - Kierkegaard',
                '"Ozgurluk, zorunlulugu kavramaktir." - Hegel',
            ],
        },
        "muzik_kosesi": {
            "baslik": "Muzik Dunyasi",
            "sanatci": {"ad": "Ludwig van Beethoven", "donem": "1770-1827", "ulke": "Almanya",
                "bilgi": "Beethoven, klasik muzikten romantik muzige gecisi simgeleyen en onemli bestecilerden biridir. Isitme yetisini tamamen kaybettikten sonra bile bestelemeye devam etmis, 9. Senfoni'yi (Neseli Ode) sagir iken yazmistir. Toplam 9 senfoni, 32 piyano sonati, 5 piyano konsertosu ve bir opera (Fidelio) bestemistir.",
            },
            "tur_tanitimi": {
                "ad": "Klasik Muzik",
                "aciklama": "Bati klasik muzigi, ortacag doneminden gunumuze kadar uzanan zengin bir gelenektir. Barok (Bach, Vivaldi), Klasik (Mozart, Haydn), Romantik (Chopin, Liszt) ve Modern (Stravinsky, Debussy) olmak uzere dort ana doneme ayrilir.",
            },
            "dinleme_onerisi": "Bu ay dinleyin: Beethoven - Ay Isigi Sonati (Moonlight Sonata). 1801'de bestelenen bu eser, piyano edebiyatinin en taninmis parcalarindan biridir.",
        },
        "kelime_bulmacasi_50": {
            "baslik": "Mega Kelime Bulmacasi (50 Kelime)",
            "kelimeler": [
                "BILIM", "TARIH", "DOGA", "SANAT", "SPOR", "MUZIK", "FELSEFE", "EDEBIYAT",
                "ATOM", "HUCRE", "GEZEGEN", "GALAKSI", "NORON", "ENZIM", "GEN", "PROTEIN",
                "ROMA", "MISIR", "YUNAN", "OSMANLI", "SUMER", "HITIT", "SELCUKLU", "ANADOLU",
                "ORMAN", "OKYANUS", "VOLKAN", "DEPREM", "IKLIM", "KUTUP", "CORAL", "FIRTINA",
                "RESIM", "HEYKEL", "TIYATRO", "SINEMA", "OPERA", "BALE", "SERAMIK", "EBRU",
                "FUTBOL", "BASKETBOL", "YUZME", "ATLETIZM", "TENIS", "VOLEYBOL", "OKCULUK", "GURES",
                "PIYANO", "KEMAN",
            ],
            "ipucu": "Kelimeler yatay, dikey ve capraz olarak gizlenmistir. Tum 50 kelimeyi bulun!",
        },
        "zeka_sorulari": [
            {"soru": "Bir corba kasigina kac harf sigar?", "cevap": "4 harf: C-O-R-B-A... Hayir! Kasiga harf sigmaz, corba sigar!"},
            {"soru": "Bir saatin yelkovani ile akrebi gunde kac kez ust uste gelir?", "cevap": "22 kez (24 saatte 22 kez, cunku 11:59'dan sonra 12:00'da bulusurlar ama gece 12'den sonra ilk bulussma 1:05 civarindadir)."},
            {"soru": "3 tavuk 3 gunde 3 yumurta yapar. 12 tavuk 12 gunde kac yumurta yapar?", "cevap": "48 yumurta. Her tavuk gunde 1/3 yumurta yapar. 12 tavuk x 12 gun x 1/3 = 48."},
            {"soru": "Bir odada 4 kose vardir. Her kosede 1 kedi oturuyordur. Her kedinin onunde 3 kedi vardir. Odada toplam kac kedi vardir?", "cevap": "4 kedi. Her kedi digeer 3 kediyi goruyor."},
            {"soru": "Yanan bir mum 30 dakikada tukenir. 2 mum yakilir, 10 dakika sonra biri soondurulur. Ne kadar mum kalir?", "cevap": "1 tam mum + 2/3 mum. Sondurulen mum 2/3'u kalmis halde durur, yanan mum 20 dakika sonra biter."},
            {"soru": "Hangi kelime sozlukte yanlis yazilmistir?", "cevap": "'Yanlis' kelimesi."},
            {"soru": "Bir adam yagmurda semsiyesiz, sapkasiz yuruyor ama saclari islanmiyor. Nasil?", "cevap": "Adam keldir."},
            {"soru": "5 baligi 5 kedi 5 dakikada yer. 100 baligi 100 kedi kac dakikada yer?", "cevap": "5 dakikada. Her kedi 5 dakikada 1 balik yer."},
        ],
        "sonraki_sayi": {
            "tema": "Bilim ve Kesif",
            "teasers": [
                "Nobel Odulleri - Bilimin Zirvesi",
                "James Webb Uzay Teleskobu ile Evrenin Derinlikleri",
                "Antik Misir'in Gizemli Piramitleri",
                "Sonbahar Ormanlari ve Yaprak Dokme Bilimi",
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# SAYILAR 2-12: Sablon veri uretici
# ---------------------------------------------------------------------------
for _sn, _info in [
    (2, {"ay": "Ekim 2025", "tema": "Bilim ve Kesif", "renk": (124, 58, 237)}),
    (3, {"ay": "Kasim 2025", "tema": "Sanat ve Yaraticilik", "renk": (220, 38, 127)}),
    (4, {"ay": "Aralik 2025", "tema": "Kis Masallari ve Bilim", "renk": (16, 185, 129)}),
    (5, {"ay": "Ocak 2026", "tema": "Yeni Baslangiclar", "renk": (59, 130, 246)}),
    (6, {"ay": "Subat 2026", "tema": "Sevgi ve Bilim", "renk": (239, 68, 68)}),
    (7, {"ay": "Mart 2026", "tema": "Bahar ve Yenilenme", "renk": (34, 197, 94)}),
    (8, {"ay": "Nisan 2026", "tema": "Dunya ve Uzay", "renk": (99, 102, 241)}),
    (9, {"ay": "Mayis 2026", "tema": "Doga Ana", "renk": (16, 185, 129)}),
    (10, {"ay": "Haziran 2026", "tema": "Yaz ve Macera", "renk": (245, 158, 11)}),
    (11, {"ay": "Temmuz 2026", "tema": "Denizler ve Okyanuslar", "renk": (6, 182, 212)}),
    (12, {"ay": "Agustos 2026", "tema": "Tatil ve Kesif", "renk": (168, 85, 247)}),
]:
    _t = _info["tema"]
    _ay = _info["ay"]

    _bilim1_icerik = (
        f"{_t} temasinin bilimsel boyutlarini bu ayki sayimizda derinlemesine inceliyoruz. "
        f"Modern bilim, disiplinler arasi calisma ve is birligi ile buyuk ilerlemeler kaydetmektedir. "
        f"Temel bilimlerden uygulamali muhendislige, fizikten biyolojiye kadar her alan birbirini "
        f"destekleyerek yeni kesifler mumkun kılmaktadir. Turkiye'de TUBITAK, TUBA ve universitelerin "
        f"AR-GE merkezlerinde yurutulen calismalar uluslararasi duzeyere kalitede bilimsel uretim "
        f"ortaya koymaktadir.\n\n"
        f"Bilimsel yontem, gozlem, hipotez, deney, analiz ve sonuc asamalarindan olusan sistematik "
        f"bir surectir. Bu yontem sayesinde evrenin isleyisine dair bilgilerimiz surekli "
        f"derinlesmektedir. Newton'un yercekim teorisinden Einstein'in gorelilik kuramina, "
        f"Darwin'in evrim teorisinden Watson ve Crick'in DNA yapisinin kesfine kadar bilim "
        f"tarihi buyuk atilimlarla doludur. Her bir kesif insanligin dunya ve evren anlayisini "
        f"koklunden degistirmistir.\n\n"
        f"Kuantum mekanigindan nano teknolojiye, gen muhendisliginden yapay zekaya kadar "
        f"21. yuzyilin bilimsel gelismeleri gunluk hayatimizi hizla donusturmektedir. CRISPR "
        f"gen duzenleme teknolojisi genetik hastaliklarin tedavisinde devrim yapmaktadir. "
        f"Kuantum bilgisayarlar klasik bilgisayarlarin milyonlarca yilinda cozecegi problemleri "
        f"saniyeler icinde cozme potansiyeline sahiptir. Nanomalzemeler ile gelistirilen yeni "
        f"urunler sagliktan enerjiye her alanda inovasyon saglamaktadir.\n\n"
        f"Bilim okuryazarligi modern toplumun temel gerekliliklerinden biridir. Bilimsel "
        f"dusunme becerisi, soru sorma, kanit arama ve sonuclari elestirmek degerlendirebilme "
        f"yetkinligini kapsar. Ogrencilerin erken yaslarda bu becerileri kazanmasi, hem "
        f"akademik basarilari hem de hayat boyu ogrenme kapasiteleri icin kritik onem "
        f"tasimaktadir. Bilim festivalleri, deney kulupler ve bilim merkezleri bu becerileri "
        f"gelistirmek icin ideal ortamlar sunmaktadir.\n\n"
        f"Gelecek on yilda beklenen bilimsel gelismeler arasinda Mars'a insanli misyon, "
        f"fuzyon enerjisi, tam otonom araclar, yapay genel zeka ve kansere kesin tedavi "
        f"gibi cok onemli donumnoktallari bulunmaktadir. Bu gelismeleri takip eden ve "
        f"anlayan bir nesil yetistirmek, dergimizin en onemli misyonlarindan biridir.\n\n"
        f"Bilimsel etik de modern bilimin vazgecilmez bir boyutudur. Arastirmalarin "
        f"dürüst ve seffaf bir sekilde yurtuulmesi, verilerin manipule edilmemesi ve "
        f"sonuclarin nesnel olarak raporlanmasi bilimsel guvenilirligin temelidir. "
        f"Yapay zeka, gen teknolojileri ve iklim muhendisligi gibi alanlarda etik "
        f"sorular her gecen gun daha karmasik hale gelmektedir. Ogrencilerin bilimsel "
        f"etik konusunda farkindalik kazanmasi, geleceginksorumlu bilim insanlarinin "
        f"yetismesi icin buyuk onem tasimaktadir. Bilim toplumun hizmetinde olmalidir "
        f"ve insanlik yararina kullanilmalidir.\n\n"
        f"Disiplinler arasi calisma, modern bilimin en verimli yaklasimidir. Fizik ve "
        f"biyolojinin kesisiminde biyofizik, kimya ve bilgisayar biliminin birlesiminde "
        f"hesaplamali kimya, psikoloji ve ekonominin bulusmasinda davranissal ekonomi "
        f"gibi yeni alanlar dogmaktadir. Bu alanlar geleneksel disiplinlerin tek "
        f"basina cozemedigi karmasik problemlere yaratici cozumler sunmaktadir. "
        f"Ogrencilerin birden fazla alanda bilgi edinmesi ve bu bilgileri "
        f"birlestirme kapasitesi gelistirmesi, gelecekteki bilimsel atilimlar "
        f"icin buyuk onem tasimaktadir.\n\n"
        f"Vatandas bilimi (citizen science) kavrami, profesyonel olmayan bireylerin "
        f"bilimsel arastirmalara aktif katilimini ifade eder. Kus gozlemi, meteor "
        f"sayimi, hava durumu olcumu ve biyocesitlilik haritalamasi gibi projelerde "
        f"gönulluler degerli veriler toplayarak bilime katki saglamaktadir. eBird, "
        f"iNaturalist ve Galaxy Zoo gibi platformlar milyonlarca katilimcinin "
        f"bilimsel kesfiere katkilarini mumkun kilmaktadir. Ogrenciler de bu "
        f"projelere katilarak hem bilimsel yontemi pratikte ogrenebilir hem de "
        f"gercek bilimsel arastirmalara dogrudan katki saglayabilirler.\n\n"
        f"Bilim ve teknolojinin toplumsal etkileri uzerine dusunmek de bilimsel "
        f"okuryazarligin onemli bir boyutudur. Yapay zekanin is piyasasina etkileri, "
        f"genetik muhendisligin etik sinirlari, iklim muhendisliginin riskleri ve "
        f"dijital gozetimin bireysel ozgurlukler uzerindeki etkisi gibi konular "
        f"hem bilimsel bilgi hem de etik dusunme gerektirir. Ogrencilerin bu tur "
        f"karmasik konulari tartisabilme ve farkli bakis acilarini degerlendirme "
        f"becerisi kazanmasi, demokratik toplumun sagligi icin vazgecilmezdir."
    )

    _bilim2_icerik = (
        f"Bu ayin ozel bilim konusu olarak {_t.lower()} alaninda son gelismeleri ele aliyoruz. "
        f"Bilim dunyasi her gun yeni kesiflerle zenginlesmeye devam ediyor. Universite "
        f"laboratuvarlarindan sanayi AR-GE merkezlerine, uzay ajanslarin gozlemevlerine kadar "
        f"binlerce bilim insani insanligin sinirlarini genisletmek icin calismaktadir.\n\n"
        f"Turkiye'nin bilimsel cikti haritasina baktigimizda, tip, muhendislik, tarim ve "
        f"temel bilimler alanlarinda guçlu bir uretim gordugumuz gorulmektedir. Turk bilim "
        f"insanlari yurtdisinda da prestijli kurumlarda onemli pozisyonlarda gorev "
        f"yapmaktadir. Aziz Sancar'in 2015'te aldigi Nobel Kimya Odulu, Turk biliminin "
        f"uluslararasi basarisinin en parlak orneklerinden biridir.\n\n"
        f"Ogrencilerin bilimsel projelere katilimi, bilgi toplumunun insasinda kritik "
        f"bir rol oynamaktadir. TUBITAK 4006 Bilim Fuarlari, ulusal ve uluslararasi bilim "
        f"olimpiyatlari ve maker hareketi genc kusaklarin bilimle bulusmasini saglamaktadir. "
        f"Bilimsel merak ve arastirma ruhu, her ogrencide beslemenmesi gereken en degerli "
        f"ozelliktir. Einstein'in soyledigi gibi 'Merak, resmi egitimden sonra da hayatta "
        f"kalabilirse, bu bir mucizedir.'\n\n"
        f"Bilim iletisimi de gunumuzde onemli bir alan haline gelmistir. YouTube kanallari, "
        f"podcast'ler, bilim dergileri ve sosyal medya platformlari bilimsel bilgiyi genis "
        f"kitlelere ulastirmaktadir. Smarti Dergi olarak biz de bu misyonun bir "
        f"parcasi olarak her ay size en guncel ve ilgi cekici bilimsel gelismeleri sunuyoruz.\n\n"
        f"Bilimsel arastirma yontemlerini ogrenmek, ogrencilerin elestrel dusunme "
        f"becerilerini gelistirmelerinin en etkili yoludur. Deney tasarlama, veri "
        f"toplama, analiz etme ve sonuclardan cikarim yapma surecileri, yalnizca "
        f"bilim alaninda degil hayatin her alaninda uygulanabilecek becerilerdir.\n\n"
        f"Bilim tarihi, basarisizliklarin ve israrli calismanin onemini gosteren "
        f"sayisiz ornek sunmaktadir. Thomas Edison ampulu icat etmeden once binlerce "
        f"basarisiz deneme yapmistir. Marie Curie, radyoaktivite uzerine calismalariyla "
        f"iki Nobel odulu kazanan ilk bilim insani olmustur. Alexander Fleming "
        f"penisilin kesfini bir kaza sonucu yapmis, ancak bu kazayi bilimsel bir "
        f"kesfie donusturebilmesi onun bilimsel merak ve gozlem gucunun sonucudur. "
        f"Bu ornekler, bilimsel basarinin yalnizca zekadan degil, ayni zamanda "
        f"kararlilik, merak ve acik fikirlilikten kaynaklandigini gostermektedir."
    )

    _teknoloji_icerik = (
        f"Teknoloji dunnyasi {_ay} ayinda da hiz kesmeden gelismeye devam ediyor. "
        f"Yapay zeka, bulut bilisim, nesnelerin interneti (IoT) ve blok zincir teknolojileri "
        f"is dunyasindan egitiye, sagliktan ulasima her sektoru donusturmektedir. Bu ay "
        f"'{_t}' temasi cercevesinde teknolojinin hayatimiza etkilerini inceliyoruz.\n\n"
        f"Egitim teknolojileri alaninda yapay zeka destekli platformlar hizla yayginlasmaktadir. "
        f"Kisisellestirilmis ogrenme algoritmalari, her ogrencinin seviyesine ve ogrenme "
        f"stiline uygun icerikler sunarak egitimde firsat esitligini artirmaktadir. Sanal "
        f"siniflar, dijital tahtalar ve interaktif ders kitaplari artik standard egitim "
        f"araclari arasinda yerini almistir. Turkiye'de EBA platformu 20 milyondan fazla "
        f"kullaniciya ulasmistir.\n\n"
        f"Siber guvenlik, dijitallesen dunyada en onemli konulardan biri haline gelmistir. "
        f"Her gun milyonlarca siber saldiri gerceklestirilmekte ve kisisel verilerin "
        f"korunmasi hayati onem tasimaktadir. Ogrencilerin dijital okuryazarlik ve "
        f"siber guvenlik bilincine sahip olmasi artik bir secim degil, zorunluluktur. "
        f"Guclu sifreler kullanmak, iki faktorlu dogrulama etkinlestirmek ve supheli "
        f"baglantilara tiklamaktan kacinmak temel guvenlik adimlarindandir.\n\n"
        f"Robotik ve otomasyon alani da hizla ilerlemektedir. Endüstri 4.0 ile fabrikalar "
        f"akilli sistemlerle donatilmakta, yapay zeka destekli robotlar uretim hatlarinda "
        f"insanlarla birlikte calismaktadir. Otonom araclar, drone teslimat sistemleri ve "
        f"akilli sehir uygulamalari gunluk yasami donusturmeye devam etmektedir.\n\n"
        f"Yesil teknoloji ve surdurulebilirlik de teknoloji gundeminin on siralarindadir. "
        f"Gunes ve ruzgar enerjisi maliyetleri hizla dusurken, elektrikli araclar ve "
        f"batarya teknolojileri iklim degisikligiyle mucadelede kritik rol ustlenmektedir.\n\n"
        f"Blok zincir teknolojisi de finans sektorunun otesine gecmeye baslamistir. "
        f"Tedarik zinciri yonetimi, dijital kimlik dogrulama, akilli sozlesmeler ve "
        f"merkeziyetsiz uygulamalar blok zincirin kullanim alanlari arasindadir. "
        f"Egitim sektorunde diploma ve sertifika dogrulamasi icin blok zincir "
        f"kullanimini arastirmaktadir. Bu teknoloji sahtecilik ve dolandiriciligini "
        f"onlemede buyuk potansiyel tasiyor.\n\n"
        f"Uzay teknolojilerinde de heyecan verici gelismeler yasanmaktadir. SpaceX'in "
        f"yeniden kullanilabilir roketleri uzay erisim maliyetlerini drastik olarak "
        f"dusurmustur. Starlink uydu aglari dunyanin en ucra koselerine internet "
        f"erisimi saglamaktadir. James Webb Uzay Teleskobu evreni daha once hic "
        f"gorulmemis netlikte goruntulemeye devam etmektedir. Turkiye de TUBITAK UZAY "
        f"ve Turk Havacilik ve Uzay Sanayii ile kendi uzay programini gelistirmekte, "
        f"yerli uydular ve uzay teknolojileri uretmektedir. GOKTURK ve TURKSAT uydu "
        f"serileri bu alandaki ilerleminin somut gostergeleridir.\n\n"
        f"Yapay zeka ve makine ogrenimi, gunluk hayatimiza derinlemesine nufuz etmistir. "
        f"Sesli asistanlar, oneri sistemleri, otonom suruus teknolojileri, tibbi "
        f"goruntuleme analizi ve dil ceviri araclari yapay zekanin pratik uygulamalari "
        f"arasindadir. Buyuk dil modelleri metin uretimi, kod yazimi ve yaratici "
        f"icerik olusturmada devrim yapmistir. Ancak yapay zekanin etik kullanimi, "
        f"veri gizliligi ve algoritmik on yargi konulari da toplumsal tartismalarin "
        f"odagindadir. Ogrencilerin yapay zekayi bir arac olarak etkili kullanmayi "
        f"ogrenmesi, gelecek is piyasasinda onemli bir avantaj saglayacaktir."
    )

    _tarih_icerik = (
        f"Tarih, insanligin ortak hafizasidir ve gelecegi sekillendirmek icin en degerli "
        f"rehberimizdir. Bu ay '{_t}' temasiyla baglantili tarihi olaylari ve kisileri "
        f"inceliyoruz. Gecmisin derslerini anlamak, bugunun sorunlarina cozum uretmek "
        f"icin vazgecilmez bir beceridir.\n\n"
        f"Anadolu, insanlik tarihinin en eski ve en zengin medeniyetlerinin besigi olmustur. "
        f"Catalhoyuk'te MO 7500'lerde kurulan yerlesim yeri, dunyanin bilinen en eski "
        f"sehirlerinden biridir. Hitit, Frigya, Lidya, Urartu, Ionia, Roma, Bizans ve "
        f"Osmanli medeniyetleri Anadolu topraklarinda serpilip gelismistir. Her bir "
        f"medeniyet kendisinden sonrakine zengin bir kulturel miras birakmistir.\n\n"
        f"Osmanli Imparatorlugu, 600 yili askin suresiyle dunya tarihinin en uzun omurlu "
        f"devletlerinden biridir. Uc kitada hakimiyet kuran imparatorluk, adalet, hosgoru "
        f"ve kultur alanllarinda onemli miras birakmistir. Mimar Sinan'in eserleri, "
        f"Evliya Celebi'nin Seyahatnamesi ve divan edebiyatiniin zenginligi bu mirasin "
        f"en parlak ornekleridir.\n\n"
        f"Modern Turkiye'nin kurulusu, 20. yuzyilin en onemli donusum hikayelerinden "
        f"biridir. Mustafa Kemal Ataturk onderligi nde yurutulen Kurtulus Savasi ve "
        f"ardindan gerceklestirilen kopssamli reformlar, yeni bir devletin temellerini "
        f"atmistir. Cumhuriyet'in ilani, harf devrimi, kadin haklari ve egitim "
        f"reformlari Turkiye'yi modern dunya ile bulusturmustur.\n\n"
        f"Tarih bilinci, bir toplumun kimliginin ve birliginin temelidir. Genc "
        f"kusaklarin tarih bilincine sahip olmasi, hem kulturel mirasimizi korumak "
        f"hem de gelecekte dogru kararlari vermek acisindan buyuk onem tasimaktadir.\n\n"
        f"Tarih egitimi, ezbercilikten ziyade anallitik dusunme ve kaynak yorumlama "
        f"becerileri uzerine kurulmalidir. Birincil kaynaklarin incelenmesi, farkli "
        f"perspektiflerin karsilastirilmasi ve tarihsel olaylarin neden-sonuc iliskisi "
        f"icinde degerlendirilmesi ogrencilerin tarih bilincini derinlestirir. "
        f"Muzeler, tarihi mekanlar ve belgesel filmler bu surecte degerli egitim "
        f"araclaridir.\n\n"
        f"Sozlu tarih projeleri de ogrencilerin tarih bilincini gelistirmek icin "
        f"etkili bir aracdir. Buyuk ebeveynlerin ve yasli komsularin anillarini "
        f"kayit altina almak, hem aile tarihini hem de yerel tarihi canlandirir. "
        f"Bu calismalar, tarih derslerini somutlastirir ve ogrencilerin tarihi "
        f"kisisel bir deneyim olarak hissetmelerini saglar. Tarihi romanlar ve "
        f"tarih temali filmler de tarih bilincini pekistirmede etkili "
        f"araclardir.\n\n"
        f"Arkeolojik kesifler tarih anlayisimizi surekli yeniden sekillendirmektedir. "
        f"Gobeklitepe'nin kesfedilmesi, insanlik tarihinin bilinen ilk anit yapisinin "
        f"MO 10.000 yilina kadar geri gittigini ortaya koymustur. Bu kesif, yerlesik "
        f"hayata gecis ve tarim devrimine iliskin yerlesik teorileri temelden "
        f"sarsmistir. Turkiye'deki arkeolojik kazilarda her yil yeni buluntular gun "
        f"yuzune cikmakta ve Anadolu'nun insanlik tarihi icin ne kadar merkezi bir "
        f"oneme sahip oldugunu bir kez daha kanitlamaktadir.\n\n"
        f"Dunya tarihinde fikir akimlari ve entelektuel devrimler, siyasi devrimler "
        f"kadar belirleyici olmustur. Aydinlanma Cagi, akil ve bilimi esas alan "
        f"dusunce sistemiyle modern demokratik toplumlarin temellerini atmistir. "
        f"Ronesans, Avrupa'da sanat ve bilimin yeniden canlanmasini simgeler. "
        f"Sanayi Devrimi ise uretim bicimlerini, toplumsal yapiyi ve insan "
        f"iliskilerini koklunden degistirmistir. Bu buyuk donum noktalarina "
        f"bakmak, bugunun hizla degisen dunyasini daha iyi anlamamiza yardimci olur."
    )

    _gezi_icerik = (
        f"Bu ay gezi sayfalarimizda Turkiye'nin esiz guzelliklerini kesfediyoruz. "
        f"'{_t}' temasiyla uyumlu olarak sectigimiz rotalar, hem dogal guzellikler hem de "
        f"kulturel zenginlikler sunmaktadir. Turkiye, cografi konumu itibariyle dort "
        f"mevsim farkli guzelliklere ev sahipligi yapan essiz bir ulkedir.\n\n"
        f"Anadolu'nun her kosesi farkli bir hikaye anlatir. Kapadokya'nin peri bacalarinin "
        f"ve yeralti sehirleri, Pamukkale'nin beyaz traverten teraslari, Nemrut Dagi'nin "
        f"devasa heykelleri ve Sumela Manastiri'nin sarp kayaliklara tutunmus goruntusu "
        f"dunya genelinde essiz dogal ve kulturel miras alanlaridir. UNESCO listesinde "
        f"Turkiye'den 19 alan yer almaktadir.\n\n"
        f"Turkiye mutfagi, dunya gastronomi sahnesinin en zenginlerinden biridir. Her "
        f"bolgenin kendine ozgu lezzetleri, pismre teknikleri ve gelenekleri vardir. "
        f"Guneydogu'nun baharatli kebaplari, Ege'nin zeytinya glili ot yemekleri, "
        f"Karadeniz'in misir ve hamsi kulturu ve Ic Anadolu'nun etli ekmegi ve mantisi "
        f"bu zenginligin kucuk bir orneklemesidir.\n\n"
        f"Seyahat, en etkili egitim araclarindan biridir. Farkli kulturler, yasam "
        f"bicrmleri ve dogal ortamlarla dogrudan temas, kitaplardan ogrenilemeyecek "
        f"deneyimler kazandirir. Aile gezileri cocuklarin culturel farkindaliginI "
        f"arttirir, empati ve anlayis gelistirir. Bu ayki gezi onerillermiizi "
        f"uygularken fotograflar cekin, gezi guncesi tutun ve deneyimlerinizi "
        f"arkadaslarinizla paylasin.\n\n"
        f"Surdurulebilir turizm de gunumuzun onemli konularindan biridir. Gezdigimiz "
        f"yerlerin dogal ve kulturel degerlerini korumak hepimizin sorumlulugunddadir.\n\n"
        f"Seyahat planlamasinda dijital araclar cok faydalidir ancak spontan kesfler "
        f"ve yerel halkla dogrudan iletisim seyahatin en degerli yanlaridir. Gezi "
        f"guncesi tutmak, fotograflarla anilari olsturmak ve deneyimleri yakinlarla "
        f"paylassmak seyahatin kaliciliginni arttirir. Bir sonraki tatilinizdee "
        f"kesfedilmemis rotalari deneyin."
    )

    _doga_icerik = (
        f"Doga, en buyuk ogretmenimizdir. '{_t}' temasi cercevesinde bu ay dogayla ilgili "
        f"onemli konulari ele aliyoruz. Gezegenimizin biyolojik cesitliligi, ekosistemlerin "
        f"dengeleri ve iklim degisikligi gibi konular tum insanligin gelecegini dogruddan "
        f"ilgilendirmektedir.\n\n"
        f"Turkiye, cografi konumu itibariyle uc farkli biyocografik bolgenin (Avrupa-Sibirya, "
        f"Akdeniz ve Iran-Turan) kesisim noktasindadir. Bu durum ulkemizi biyolojik cesitlilik "
        f"acisindan dunyanin en zengin bolgelerinden biri yapmaktadir. Yaklasik 12.000 bitki "
        f"turu barindiran Turkiye'de, bunlarin 3.700'den fazlasi endemiktir, yani dunyanin "
        f"baska hicbir yerinde dogal olarak yetismemektedir.\n\n"
        f"Iklim degisikligi gezegenimizin karsi karsiya oldugu en buyuk tehdittir. Kuresel "
        f"sicaklik artisi, buzullarin erimesi, deniz seviyesinin yukselmesi ve asiri hava "
        f"olaylari her gecen gun daha belirgin hale gelmektedir. Paris Iklim Anlasmasi "
        f"cercevesinde ulkeler karbon emisyonlarini azaltma taahhutleri vermis olsa da "
        f"hedeflerlen henuz yeterince hizli ilerlenmemektedir.\n\n"
        f"Bireysel olarak da cevre korumaya katki saglayabiliriz. Enerji tasarrufu, geri "
        f"donusum, surdurulebilir ulasim tercihlerri ve bilinçli tuketim davranislari "
        f"toplam etkiyi onemli olcude azaltabilir. Okullarda cevre kulubler, agac dikme "
        f"kampanyalari ve atik toplama projeleri genc kusaklarin cevre bilincini "
        f"gelistirmek icin harika firsatlar sunmaktadir.\n\n"
        f"Dogal alanlari korumak, gelecek kusaklara karsi en onemli sorumlulugumuzdur. "
        f"Milli parklar, sulak alanlar ve koruma bolgelerini desteklemek hepimizin "
        f"gorevidir.\n\n"
        f"Cevre egitiimi okullardan baslamalidir. Okul bahcelerinndde permakueltur "
        f"projeleri, sinif icinde bitki yetistirme deneyleri ve doga gezileri "
        f"ogrencilerin cevre bilincini erken yaslarda gelistirir. Her okulun bir "
        f"cevre kulubu kurmasi ve yillik en az bir cevre projesi gerceklestirmesi "
        f"ozendirilmelidir."
    )

    _edebiyat_tanitim = (
        f"Bu ayin kitap onerimiz, {_t.lower()} temasina uygun olarak secilmis bir "
        f"dunya edebiyati klasigidir. Edebiyat, insanligin en eski ve en etkili iletisim "
        f"araclarirdan biridir. Hikayeler, romanlar ve siirler araciligiyla deneyimlerimizi "
        f"paylasiriz, baska hayatlari yasariz ve empati kurma becerimizi gelistiririz.\n\n"
        f"Duzenli kitap okuma aliskanligi, kelime dagarcigini genisletir, elestimrel "
        f"dusunme becerisini gelistirir ve hayal gucunu besler. Arastirmalar, haftada "
        f"en az 30 dakika kitap okuyan ogrencilerin akademik basarilarinin yuzde yirmi "
        f"bes daha yuksek oldugunu gostermektedir. Okuma aliskanligi ne kadar erken "
        f"kazanilirsa o kadar kalici olur.\n\n"
        f"Turk edebiyati, Divan edebiyatindan Tanzimat doneimine, Milli Edebiyat'tan "
        f"Cumhuriyet donemi edebiyatina kadar zengin bir geleneoge sahiptir. Yunus Emre, "
        f"Fuzuli, Namik Kemal, Halit Ziya, Yakup Kadri, Orhan Veli ve Yasar Kemal gibi "
        f"isimler bu zengin gelenegin mihenk taslaridir. Orhan Pamuk'un 2006'da kazandigi "
        f"Nobel Edebiyat Odulu, Turk edebiyatinin uluslararasi taninirrliginin doruk "
        f"noktalarindan biridir.\n\n"
        f"Dunya edebiyati da sinirsiz bir okuma evreni sunmaktadir. Homer'in Ilyada'sindan "
        f"Dostoyevski'nin Suc ve Ceza'sina, Garcia Marquez'in Yuz Yillik Yalnizlik'indan "
        f"Murakami'nin eselerine kadar her kulturden ve donemden basyapitler kesfetmenizi "
        f"beklemektedir.\n\n"
        f"Okuma aliskanligi kazanmak icin pratik oneriler: Her gun en az 20 dakika "
        f"okumaya zaman ayirin. Yaninizda her zaman bir kitap bulundurun. Okudugunuz "
        f"kitaplar hakkinda notlar alin ve arkadaslarinizla tartissin. Farkli turler "
        f"deneyin: bilim kurgu, tarih, biyografi, siir. Bir kitap kulubu kurmak da "
        f"motivasyonunuzu arttiracaktir."
    )

    _psikoloji_icerik = (
        f"Ruh sagligi, fiziksel saglik kadar onemlidir ve akademik basari psikolojik iyilik "
        f"haliyle dogrudan iliskilidir. '{_t}' temasini psikoloji perspektifinden ele alarak "
        f"ogrencilerimize ve velilerimize degerli bilgiler sunuyoruz. Psikolojik saglik, "
        f"yalnizca hastalik yoklugu degil, duygusal, sosyal ve bilisssel acidan tam bir "
        f"iyilik hali demektir.\n\n"
        f"Ergenlik donemi, bireyin kimlik arayisin en yogun yasadigi donemdir. Erik "
        f"Erikson'un psikososyal gelisim kuramina gore, ergenler 'kimlik ve kimlik "
        f"karmasasi' krizini yasarlar. Bu donemde gencler 'Ben kimim?', 'Hayatta ne "
        f"yapmak istiyorum?' gibi derin sorularla yuzyuze gelirler. Bu surecin saglikli "
        f"gecmesi icin destekleyici bir aile ve okul ortami buyuk onem tasimaktadir.\n\n"
        f"Stres yonetimi, modern yasamin temel becerilerinden biridir. Akademik baskılar, "
        f"sosyal medya etkisi, gelecek kaygisi ve aile beklentileri ogrenciler uzerinde "
        f"onemli bir stres kaynagi olusturabilir. Bilisssel davranisci terapi (BDT) "
        f"teknikleri, olumsuz dusunce kaliplarini tanimayi ve degistirmeyi ogretir. "
        f"Mindfulness (bilinçli farkindalik) uygulamalari ise ana odaklanarak kaygiyi "
        f"azaltmada etkili bir yontemdir.\n\n"
        f"Duygusal zeka (EQ), bireyin kendi duygularini ve baskalrinin duygularini "
        f"anlama ve yonetme becerisidir. Daniel Goleman'in arastirmalari, duygusal "
        f"zekanin is ve yasamda basari icin IQ kadar, hatta daha fazla onemli oldugunu "
        f"gostermistir. Empati, oz farkindalik, oz duzenleme, motivasyon ve sosyal "
        f"beceriler duygusal zekanin bes temel bilesenidir.\n\n"
        f"Okul rehberlik servisleri, ogrencilerin psikolojik destek ihtiyaclarinda "
        f"basvurabilecekleri en yakin kaynaklardir. Bireysel gorusme, grup calismalari "
        f"ve kariyer danismanligi hizmetleri sunulmaktadir.\n\n"
        f"Pozitif psikoloji yaklasiimi, bireylerin guclu yonlerini one cikartmayi ve "
        f"yasam kalitesini artirmayi hedefler. Martin Seligman'in PERMA modeli "
        f"(Olumlu duygular, Baglanim, Iliskiler, Anlam, Basari) mutluluk ve "
        f"tatminin bes temel bilesenini tanimlar. Ogrencilerin bu beseni "
        f"hayatlarinda gelistirmelerine yardimci olmak rehberligin temel "
        f"gorevlerinden biridir.\n\n"
        f"Uyku hijyeni, ogrenci psikolojisinde siklikla gozardi edilen kritik bir "
        f"faktortur. Arastirmalar, yeterli ve kaliteli uyku almayan ogrencilerin "
        f"dikkat, hafiza ve problem cozme becerilerinde belirgin dusus yasadigini "
        f"gostermektedir. Ergenlik doneminde biyolojik saat degisir ve gencler dogal "
        f"olarak gec yatip gec kalkmaya egilimlidir. Ancak okul saatleri buna uygun "
        f"olmadigi icin, uyku duzeni olusturmak buyuk onem tasir. Yatmadan en az bir "
        f"saat once ekranlardan uzak durmak, karanlik ve serin bir ortamda uyumak ve "
        f"her gun ayni saatte yatip kalkmak uyku kalitesini onemli olcude arttirir.\n\n"
        f"Akran baskisi ve sosyal medya etkileri, genc bireylerin psikolojik "
        f"sagligini derinden etkileyen cagdas sorunlardir. Sosyal medyada surekli "
        f"baskalariyla karsilastirma yapmak, ozguven dusurur ve yetersizlik hissi "
        f"yaratabilir. Gencler, cevrimici kimliklerin gercegi tam olarak "
        f"yansitmadigini kavramalidir. Sanal begeni sayilarinin gercek degeri "
        f"olcmedigi, herkesin yalnizca en iyi anlarini paylastigi ve gercek "
        f"iliskilerin dijital etkilesinlerden cok daha degerli oldugu "
        f"hatirlanmalidir. Dijital detoks gunleri planlamak ve yuzyuze sosyal "
        f"aktivitelere oncelik vermek psikolojik iyi olus halini destekler."
    )

    _veli_icerik = (
        f"Cocugunuzun gelisimini desteklemek icin '{_t}' temasiyla onerilerimizi "
        f"sunuyoruz. Ebeveynlik, dunyanin en zor ama en oduellendirici gorevidir. "
        f"Cocuklarinizin fiziksel, bilisssel, duygusal ve sosyal gelisimlerini "
        f"butunsel olarak desteklemek saglikli bireyler yetistirmenin temelidir.\n\n"
        f"Olumlu ebeveynlik yaklasimlari, cocuklarin ozguvenini ve oz-yeterlilik "
        f"inancini guclendirmektedir. Cocugunuzun cabalarini sonuc odakli degil "
        f"surec odakli ovun: 'Ne kadar akilli sin' yerine 'Cok emek verdin, harika' "
        f"demek buyume zihniyetini destekler. Carol Dweck'in arastirmalari, suc "
        f"odakli ovgunun cocuklarin motivasyonunu aslinda dusurdugunu gostermistir.\n\n"
        f"Cocugunuzla birlikte kaliteli vakit gecirmek, hediye veya maddi imkanlardan "
        f"cok daha degerlidir. Birlikte yemek pisirmek, oyun oynamak, kitap okumak "
        f"veya dogada yurumek guclu aile baglari olusturur. Arastirmalar, aileleriyle "
        f"duzencli birlikte yemek yiyen cocuklarin akademik basarilarinin ve duygusal "
        f"sagliklariniin daha iyi oldugunu gostermektedir.\n\n"
        f"Dijital cagda ebeveynlik yeni zorluklar getirmektedir. Sosyal medya, online "
        f"oyunlar ve ekran bagimliligi konullarinda cocuklarinizla acik diyalog "
        f"kurmak, yasaklamaktan daha etkilidir. Ekran suresi sinirlamalari belirleyin "
        f"ama bunun nedenini aciklayin. Dijital vatandaslik kavramini cocugunuza "
        f"ogretin: cevirimici ortamdaki davranislarinin da gercek hayattaki kadar "
        f"onemli oldugunu vurgulayin.\n\n"
        f"Cocugunuzun okul hayatinda aktif rol alin. Ogretmenlerle iletisim kurun, "
        f"veli toplantilarina katilinn ve ev odevlerine ilgi gosterin.\n\n"
        f"Cocugunuzun yeteneklerini ve ilgi alanlarini kesfetmesine firsat verin. "
        f"Farkli etkinlikler denemesine, hobiler edinmesine ve merak ettigi konulari "
        f"arastirmasina tesvik edin. Her cocugun benzersiz guclu yonleri vardir ve "
        f"bunlarin kesfedilmesi ozguvenin ve mutlulugun temelidir. Sabirli olun "
        f"ve surecin dogal akisina guvenin.\n\n"
        f"Sinav donemlerinde cocugunuzun uzerindeki baskiyi azaltmak ebeveynin en "
        f"onemli gorevlerinden biridir. 'Sen yapabilirsin, sana guveniyoruz' gibi "
        f"destekleyici mesajlar vermek, sonuca degil surece odaklanmak ve sinav "
        f"sonuclarina asiri tepki vermemek cocugunuzun sinav kaygisini azaltir. "
        f"Arastirmalar, ebeveyn baskisinin akademik performansi artirmak yerine "
        f"dusurdugunu gostermektedir. Cocugunuzun sinav oncesinde yeterli uyku "
        f"almasini, dengeli beslenmesini ve kisa molalar vermesini saglayin.\n\n"
        f"Kardes iliskileri ve aile dinamikleri de cocugun psikolojik gelisiminde "
        f"belirleyici bir rol oynar. Kardesler arasi kiskanclik ve rekabet dogal "
        f"olmakla birlikte, ebeveynlerin adaletli ve tutarli bir yaklasim sergilemesi "
        f"gerekir. Her cocugu kendine ozgu yetenekleri ve ozellikleriyle degerlendin, "
        f"kardesler arasi karsilastirma yapmaktan kacininn. Aile ici kurallarin tutarli "
        f"uygulanmasi, cocuklarda guvenlik duygusu ve adalet anlayisi gelisimini "
        f"destekler. Duzenlii aile toplantilari yaparak herkesin goruslerinin dinlendigi "
        f"demokratik bir aile ortami olusturmak da son derece faydalidir."
    )

    _ogrenci_icerik = (
        f"Akademik basari icin '{_t}' temasiyla ogrenclerimize ozel tavsiyelerimiz. "
        f"Basari, yetenek ile disiplinin bilesimidier. En yetenekli ogrenciler bile "
        f"duzenli calisma olmadan potansiyellerini gerceklestiremezler. Basarili "
        f"ogrencilerin ortak ozelligi, duzenli ve planli calisma aliskanligidir.\n\n"
        f"Etkili ogrenme icin farkli duyulari ve yontemleri bir arada kullannin. "
        f"Gorsel ogrenenler icin zihin haritalari ve infografikler, isitsel ogrenenler "
        f"icin sesli tekrar ve anlatim, kinestetik ogrenenler icin deney ve uygulama "
        f"faaliyetleri idealdir. Kendi ogrenme stilinizi kesfetmek, calisma "
        f"verimlilinizi onemli olcude arttiracaktir.\n\n"
        f"Teknoliojiyi ogrenme icin akıllıca kullanin. Quizlet ile flash kartlar "
        f"olusturun, Khan Academy videolari izleyin, Notion veya OneNote ile "
        f"notlarinizi duzenleyin. Ancak teknolojini dikkat dagitici yonlerinden "
        f"korunmak icin calisma sirasinda bildirimleri kapatIn ve sosyal medyaya "
        f"giris yapmayin.\n\n"
        f"Sosyal yasam ve akademik yasam dengesi kurun. Yalnizca ders calismak "
        f"tukenmislige yol acar. Hobilere zaman ayirmak, arkadaslarla vakit "
        f"gecirmek ve fiziksel aktivite yapmak beyin performansini artirir. "
        f"En basarili ogrenciler, calisma ve dinlenme arasinda saglikli "
        f"bir denge kurmayi basaranlardir.\n\n"
        f"Hedeflerinizi yazmak ve duzenli olarak gozden gecirmek motivasyonunuzu "
        f"yuksek tutar. Kisa vadeli (haftalik), orta vadeli (donemlik) ve uzun "
        f"vadeli (yillik) hedefler belirleyin.\n\n"
        f"Basarili ogrencilerin ortak ozelliklerinden biri de surekli ogrenmeye "
        f"acik olmalaridir. Derste ogrenilenlerin otesinde kitaplar okumak, belgeseller "
        f"izlemek, podcast'ler dinlemek ve online kurslara katilmak bilgi dagarciginizi "
        f"onemli olcude genisletir. Her gun en az bir yeni sey ogrenmeyi hedefleyin.\n\n"
        f"Sinav kaygisiyla basa cikmak, ogrenci hayatinin en onemli becerilerinden "
        f"biridir. Sinav oncesi asiri stres hissettiginnizde derin nefes egzersizleri "
        f"yapin, pozitif gorsellestirme tekniklerini uygulayin ve kendinize 'Bu konulari "
        f"calistim, hazirdim' gibi olumlu mesajlar verin. Sinav sirasinda once kolay "
        f"sorulardan baslayin, zor sorulara takilip kalmayin ve zaman yonetiminize dikkat "
        f"edin. Unutmayin ki tek bir sinav hayatinizin tamamini belirlemez; her sinav bir "
        f"ogrenme deneyimidir ve gelecekte daha iyisini yapmak icin firsat sunar.\n\n"
        f"Not tutma teknikleri akademik basarida buyuk fark yaratir. Cornell not alma "
        f"yontemi, not kagidini uc bolume ayirarak ana notlari, anahtar kelimeleri ve "
        f"ozet bolumunu ayri tutmayi icerir. Zihin haritalari ise konulari gorsel olarak "
        f"organize etmek icin mukemmel bir yontemdir. Derste aktif not almak, pasif "
        f"dinlemekten cok daha etkilidir cunku bilgiyi islerken ayni zamanda "
        f"kodlarsiniz. Aldiiginiz notlari ayni gun icinde gozden gecirmek, uzun sureli "
        f"hafizaya aktarim icin en etkili stratejidir. Kendi kelimelerinizle yeniden "
        f"yazmak ve ozetlemek anlama duzeyinizi onemli olcude arttirir."
    )

    _kultur_icerik = (
        f"Kultur ve sanat dunyasindan '{_t}' temasiyla secilmis icerikler. Sanat, "
        f"insanin yaratici ifadesinin en yuce bicimidir. Muzik, resim, heykel, "
        f"sinema, tiyatro ve edebiyat gibi sanat dallari, toplumlarinn kulturel "
        f"kimligini yansitir ve zenginlestirir.\n\n"
        f"Sanat egitiimi, yalnizca profesyonel sanatci yetistirmek icin degil, "
        f"yaratici dusunme, problem cozme ve duygusal ifade becerileri "
        f"kazandirmak icin de buyuk onem tasir. Arastirmalar, sanat egitimi "
        f"alan ogrencilerin akademik basarilarinin da yuzde on bes daha yuksek "
        f"oldugunu gostermektedir. Muzik egiitimi ozellikle matematiksel "
        f"dusunme ve dil becerilerini gelistirmektedir.\n\n"
        f"Sinema, 20. yuzyilin en etkili sanat ve iletisim aracidir. Lumiere "
        f"kardeslerinn 1895'teki ilk gosteriminden bugunun dijital film "
        f"yapimcilligina kadar buyuk bir yol kat edilmistir. Turk sinemasi da "
        f"Nuri Bilge Ceylan, Ferzan Ozpetek ve Zeki Demirkubuz gibi "
        f"yonetmenlerle uluslararasi arenada buyuk basarilar elde etmistir.\n\n"
        f"Muzeler, kulturel mirasin korunmasi ve nesiller arasi aktariminin "
        f"en onemli kurumlaridir. Turkiye, 400'den fazla muzesiyle dunyanin "
        f"en zengin muze ulkelerinden biridir. Istanbul Arkeoloji Muzeleri, "
        f"Ankara Anadolu Medeniyetleri Muzesi ve Goreme Acik Hava Muzesi "
        f"mutlaka goruelmesi gereken mekanlardan yalnizca birkacidir.\n\n"
        f"Bu ay kultur ve sanat sayfalarimizda sizler icin sectigimiz film, "
        f"muzik ve sanat eseri onerileriyle keyifli vakit gecirmenizi diliyoruz.\n\n"
        f"Sanat eserleri yaraatildiiklari donemin toplumsal, siyasi ve kulturel "
        f"yapisini yansitir. Bu nedenle sanat tarihi, insanlik tarihini anlamanin "
        f"en zengin yollarindan biridir. Sanat elesstirisi ve yorumlamak becerileri "
        f"elestrel dusunmeyi gelistiirir ve farkli bakis acilari kazandirir."
    )

    _spor_icerik = (
        f"Spor saglikli yasamin vazgecilmez bir parcasidir. '{_t}' temasiyla "
        f"spor dunyasindaki gelismeleri ve ogrencilerimize onerilerimizi "
        f"sunuyoruz. Duzenli fiziksel aktivite, bedensel sagligi korumanin "
        f"yani sira zihinsel sagligi da onemli olcude desteklemektedir.\n\n"
        f"Gencler icin spor, yalnizca fiziksel gelisim degil, karakter "
        f"egitimi anlamina da gelir. Takim sporlari isbirligi ve iletisim "
        f"becerileri kazandirirken, bireysel sporlar oz-disiplin ve "
        f"kararlilik gelistirir. Fair play anlayisi, sporun ogreettigi en "
        f"onemli degerlerden biridir ve hayatin her alanina yansir.\n\n"
        f"Turkiye'de spor kulturu giderek gelismektedir. Futbol, basketbol, "
        f"voleybol ve halter en populer branslar arasindadir. Turk voleybol "
        f"milli takimi dunya sahnesinde buyuk basarilar elde etmektedir. "
        f"Okul sporlari programlari genisleetilmekte ve her ogrencinin "
        f"en az bir spor dalinda aktif olmasi tesvik edilmektedir.\n\n"
        f"Beslenme ve spor performansi arasinda cok guclu bir iliski vardir. "
        f"Karbonhidratlar enerji saglarkeen, proteinler kas gelisimini "
        f"destekler. Yeterli su tuketimi ve vitamin-mineral dengesi de "
        f"spor performansi icin kritik onem tasir. Spor oncesi hafif "
        f"atistirmalik ve sonrasinda protein agirlikli beslenme idealdir.\n\n"
        f"Bu ay spor sayfamizda ayriica spor tarihinden ilginc bilgiler, "
        f"ayin sporcusu ve saglik ipuclari sizi bekliyor.\n\n"
        f"Spor psikolojisi, basarili sporcuların fiziksel yeteneklerinin yanissira "
        f"zihinsel dayaniklilik ve odaklanma kapasitelerinin de son derece gelismis "
        f"oldugunu ortaya koymaktadir. Gorsellestirme, pozitif ic konusma ve hedef "
        f"belirleme teknikleri hem profesyonel sporcular hem de ogrenci sporcular "
        f"icin cok faydalidir. Sporun bedensel sagligin otesinde zihinsel sagliga "
        f"da buyuk katki sagladigi bilimsel olarak kanitlanmistir."
    )

    DERGI_DATA[_sn] = {
        "ay": _info["ay"], "sayi": _sn, "tema": _t, "renk": _info["renk"],
        "kapak_teasers": [
            (_t + " - Ozel Dosya", 4),
            ("Bilimde Yeni Ufuklar", 5),
            ("Teknoloji Haberleri", 7),
            ("Tarih Kosesi", 9),
            ("Gezi Rehberi", 11),
            ("Spor Dunyasi", 26),
        ],
        "editorial": (
            f"Degerli okuyucularimiz, {_ay} sayimizda '{_t}' temasiyla karsinIzdayiz! "
            f"Her ay oldugu gibi bu sayimizda da bilimden sanata, spordan edebiyata "
            f"genis bir yelpazede zengin icerikler sizi bekliyor. {_t} temasini farkli "
            f"perspektiflerden ele alarak hem bilgilendirici hem de ilham verici "
            f"yazilar hazirladik.\n\n"
            f"Bilim ve teknik sayfalarimizda bu temayla baglantili en guncel "
            f"gelismeleri, arastirma sonuclarini ve merak uyandirici bilgileri "
            f"bulacaksiniz. Teknoloji bolumumuz dijital dunyadaki yenilikleri "
            f"sizlere sunuyor. Tarih sayfalarimiz gecmisin derslerini bugune "
            f"tasiyor, gezi bolumumuz ise yeni kesfler icin ilham veriyor.\n\n"
            f"Edebiyat ve siir kosemiz ruhunuzu besleyecek, psikoloji ve "
            f"rehberlik bolumumuz pratik oneriler sunacak. Veli kosemiz "
            f"ebeveynlere yol gosterirken, ogrenci tavsiyeleri sayfamiz "
            f"akademik basari icin somut stratejiler paylasacak. Kultur "
            f"ve sanat, spor, ozlu sozler ve bulmacalar bolumlerimiz de "
            f"her zamanki gibi keyifli vakit gecirmenizi saglayacak.\n\n"
            f"15 soruluk quiz bolumumuzle kendinizi test etmeyi unutmayin! "
            f"Gecen ay cevaplari ve okuyucu mektuplari arka kapagimizdaa.\n\n"
            f"Dergimiz, ogretmenlerimizin, ogrencilerimizin ve velilerimizin "
            f"katkilariyla her ay daha zengin bir icerik sunmayi hedeflemektedir. "
            f"Siz de goruslerinizi, onerilerinizi ve yazilarinizi bizimle "
            f"paylasmaktan cekinmeyin. SmartCampus platformu uzerinden bize "
            f"ulasabilirsiniz. Okuyucu mektuplari bolumumuzde sizin yazilariniza "
            f"da yer vermek istiyoruz.\n\n"
            f"Bu ayki sayimizda ozellikle bilim ve teknoloji bolumlerimize buyuk "
            f"emek verdik. Arastirmalardan elde edilen en guncel bilgiler, "
            f"uzman gorusleri ve pratik oneriler sizleri bekliyor. Her bolumun "
            f"sonundaki bilgi kutulari ve ipucu listeleri de ayriyetten "
            f"faydalanabileceginiz degerli kaynaklar icermektedir.\n\n"
            f"Keyifli okumalar dileriz!\nSmarti Dergi Yayin Kurulu"
        ),
        "icerik_tablosu": [
            ("Editorden", 2), ("Editorden Devam", 3),
            ("Bilim & Teknik", 4), ("Bilim Devam", 5), ("Bilim Sozluk", 6),
            ("Teknoloji", 7), ("Teknoloji Devam", 8),
            ("Tarih", 9), ("Tarih Devam", 10),
            ("Gezi", 11), ("Gezi Devam", 12),
            ("Doga ve Cevre", 13), ("Cevre Devam", 14),
            ("Edebiyat", 15), ("Edebiyat Devam", 16),
            ("Siir Kosesi", 17),
            ("Psikoloji", 18), ("Psikoloji Devam", 19),
            ("Veli Kosesi", 20), ("Veli Devam", 21),
            ("Ogrenci Tavsiyeleri", 22), ("Ogrenci Devam", 23),
            ("Kultur ve Sanat", 24), ("Kultur Devam", 25),
            ("Spor", 26), ("Ozlu Sozler", 27),
            ("Bilmeceler", 28), ("Quiz", 29),
            ("Arka Kapak", 30),
        ],
        "bilim_teknik": [
            {
                "baslik": _t + " ve Modern Bilim",
                "giris": f"Bu ay bilim dunyasinda {_t.lower()} temasini kapsamli olarak inceliyoruz.",
                "icerik": _bilim1_icerik,
                "biliyor_muydunuz": [
                    "Her gun 2.5 kentilyon byte veri uretiliyor - insanlik tarihinin tum bilgisinden fazla.",
                    "Isik hizi saniyede 299.792 km'dir - gunes isigi dunyaya 8 dakika 20 saniyede ulasir.",
                    "Beyin gunde yaklasik 70.000 dusunce uretir - bunlarin yuzde sekseni onceki gunle aynidir.",
                    "Insan DNA'si yaklasik 3 milyar baz ciftinden olusur ve yuzde 99.9'u tum insanlarda aynidir.",
                    "Evrendeki yildiz sayisi, dunyadaki tum kumtanelerinden fazladir.",
                ],
            },
            {
                "baslik": "Bilimde Son Gelismeler",
                "giris": f"Bu ayin bilimsel gelismeleri ve onemli kesifler.",
                "icerik": _bilim2_icerik,
            },
        ],
        "bilim_sozlugu": [
            ("Hipotez", "Bilimsel yontemle test edilebilir oneri. Gozlem ve veriye dayali tahmin."),
            ("Teori", "Cok sayida deney ve gozlemle desteklenmis bilimsel aciklama. Hipotezden farkli olarak kapsamli kanit temeline sahiptir."),
            ("Deney", "Kontrol ve gozlem gruplari kullanilarak hipotezin test edilmesi sureci."),
            ("Analiz", "Toplanan verilerin istatistiksel ve nitel yontemlerle incelenmesi."),
            ("Sentez", "Farkli bilgi ve bulgularin bir araya getirilerek yeni bir butun olusturulmasi."),
            ("Paradigma", "Bilimsel toplulugun paylastigi temel varsayimlar ve yontemler butunu."),
        ],
        "teknoloji": {
            "baslik": "Teknoloji Dunyasi",
            "icerik": _teknoloji_icerik,
            "haberler": [
                "AI destekli egitim platformlari kullanici sayisini ikiye katladi.",
                "5G altyapisi Turkiye genelinde yayginlasmaya devam ediyor.",
                "Elektrikli arac satislari bir onceki yila gore yuzde elli artti.",
                "Uzay turizmi ilk ticari ucuslarini gerceklestirdi.",
                "Kuantum bilgisayar ilk pratik uygulamasini basariyla tamamladi.",
                "Siber guvenlik yatirimlari rekor seviyeye ulasti.",
            ],
            "gelecekte_bu_var": (
                "Teknoloji on yilda hayatimizi koklunden degistirecek. Tam otonom araclar "
                "sehir icinde yayginlasacak, yapay genel zeka (AGI) gerceklesme yolunda "
                "onemli adimlar atilacak. Uzay madenciligi ve Mars kolonizasyonu artik "
                "bilim kurgu degil, planlanmakta olan projeler haline gelmistir. Beyin-"
                "bilgisayar arayuzleri ilk ticari uygulamalarini sunmaya baslayacak."
            ),
        },
        "tarih": {
            "baslik": "Tarihten Sayfalar",
            "icerik": _tarih_icerik,
            "zaman_cizelgesi": [
                ("MO 3000", "Sumerler yazıyı icat etti - insanlik tarihinin en buyuk donum noktası"),
                ("MO 776", "Antik Olimpiyat Oyunlari basladi"),
                ("1453", "Istanbul'un fethi - Orta Cag'in sonu"),
                ("1789", "Fransiz Devrimi - modern demokrasinin dogumu"),
                ("1923", "Turkiye Cumhuriyeti'nin ilani"),
                ("1969", "Ilk insanli Ay inisi - 'Insanlik icin dev bir adim'"),
            ],
            "tarihte_bu_ay": [
                f"{_ay} ayinda tarihte yasanan onemli olaylardan secmeler.",
                "Turkiye ve dunya tarihinde bu ayin onemli donum noktalari.",
                "Bilim ve kultur tarihinde bu ayda gerceklesen kesifler.",
            ],
            "tarih_sozu": {"soz": "Tarih insanligin hafizasidir.", "kisi": "Cicero"},
        },
        "cografya_gezi": {
            "yer": "Turkiye Kesif Rotasi",
            "ulke": "Turkiye",
            "baskent_bilgi": {"nufus": "85+ milyon", "dil": "Turkce", "para": "Turk Lirasi", "alan": "783.562 km2", "iklim": "Cesitli"},
            "tanitim": _gezi_icerik,
            "gorulmesi_gereken": [
                "Kapadokya - Peri bacalari, yeralti sehirleri ve balon turlari",
                "Pamukkale - Beyaz travertenler ve antik Hierapolis sehri",
                "Efes Antik Kenti - Roma donemi mimari harikasi",
                "Nemrut Dagi - Kommagene Kralligi'nin devasa heykelleri",
                "Sumela Manastiri - Sarp kayaliklardaki bin yillik manastir",
            ],
            "yemek_onerileri": [
                "Bolgesel lezzetler - Her sehrin kendine ozgu tadi",
                "Turk kahvaltisi - Dunyanin en zengin kahvalti sofrasi",
                "Sokak lezzetleri - Simit, midye dolma, kokoreç",
                "Geleneksel tatlilar - Baklava, kunefe, lokum",
            ],
            "harita_aciklama": "Turkiye, uc kit arasindaki stratejik konumuyla farkli iklimleri ve cografyalari bir arada barindirmaktadir.",
        },
        "doga_cevre": {
            "baslik": "Doga ve Cevre",
            "icerik": _doga_icerik,
            "nesli_tehlike": [
                ("Akdeniz Foku", "Dunyanin en nadir fok turu. Turkiye sahillerinde 100'den az birey yasadigi tahmin ediliyor."),
                ("Kelaynak", "Turkiye ve dunya genelinde koruma altinda. Birecik'teki koruma programi basarili sonuclar vermektedir."),
                ("Anadolu Ceylanı", "Iç Anadolu'da yasayan endemik tur. Populasyon koruma calismalarıyla toparlanmaya baslamistir."),
            ],
            "eko_ipuclari": [
                "Geri donusume katilin - cam, kagit, plastik ve metal atiklari ayri biriktirin.",
                "Su tasarrufu yapin - dis firçalarken muslugukapatmak yilda 12.000 litre su tasarrufu saglar.",
                "Enerji tasarrufu - LED ampuller kullanin, kullanilmayan cihazlarin fisini cekin.",
                "Toplu tasima tercih edin - karbon ayak izinizi yuzde elli azaltabilirsiniz.",
                "Yerli urun satin alin - gida kilometresini azaltarak cevreyikoruyun.",
                "Agac dikin - bir agac yilda 22 kg CO2 emer ve 120 kg oksijen uretir.",
            ],
            "mevsim_gozlem": f"{_ay} ayina ozgu mevsimsel degisimler ve doga gozlem onerileri. Bu donemde dogada neler oluyor, hangi canlilar aktif, hangi bitkiler cicek aciyor kesfedinn.",
        },
        "edebiyat": {
            "kitap": "Dunya Edebiyatindan Secme",
            "yazar": "Seckin Yazarlar",
            "tur": "Roman", "sayfa": 300,
            "tanitim": _edebiyat_tanitim,
            "yazar_bio": "Bu ayin yazari hakkinda detayli bilgi edebiyat sayfamizda.",
            "bu_ay_okuyun": [
                {"kitap": "Suc ve Ceza", "yazar": "Dostoyevski", "tur": "Roman", "sayfa": 671},
                {"kitap": "Yuz Yillik Yalnizlik", "yazar": "Garcia Marquez", "tur": "Roman", "sayfa": 417},
                {"kitap": "Tutunamayanlar", "yazar": "Oguz Atay", "tur": "Roman", "sayfa": 724},
                {"kitap": "Dune", "yazar": "Frank Herbert", "tur": "Bilim Kurgu", "sayfa": 412},
                {"kitap": "Sapiens", "yazar": "Yuval N. Harari", "tur": "Non-fiction", "sayfa": 464},
            ],
            "edebi_soz": {"soz": "Bir kitabi actiginizda yeni bir dunya kesfedersiniz.", "kisi": "Dunya Edebiyati"},
        },
        "siir": [
            {
                "baslik": "Davet",
                "sair": "Nazim Hikmet Ran",
                "metin": (
                    "Disarda yagmur ve kar,\n"
                    "bir atli geciyor uzaktan.\n"
                    "Guzel gunler gorecegiz, cocuklar,\n"
                    "gunesli gunler gorecegiz.\n\n"
                    "Motor sesleri duymayacagiz artik,\n"
                    "silah sesleri de duymayacagiz.\n"
                    "Guzel gunler gorecegiz, cocuklar,\n"
                    "aydinlik gunler gorecegiz.\n\n"
                    "Zeytin agaclari altinda\n"
                    "cicekler acilacak.\n"
                    "Guzel gunler gorecegiz, cocuklar,\n"
                    "hep birlikte gorecegiz."
                ),
                "bio": (
                    "Nazim Hikmet Ran (1902-1963), Turk siirinin en onemli isimlerinden biridir. "
                    "Eserleri 50'den fazla dile cevrilmistir. Serbest nazim tarzinin Turk "
                    "edebiyatindaki oncusu olarak kabul edilir. Umut ve insanlik sevgisi "
                    "temali siirleriyle dunya edebiyatinda onemli bir yer edinmistir."
                ),
            },
            {
                "baslik": "Serenad",
                "sair": "Orhan Veli Kanik",
                "metin": (
                    "Yagmurdan sonra bir gokkusagi,\n"
                    "Bir de sicak bir ekmek kokusu;\n"
                    "Sokaklarda bir sarkinin guzelligiyle\n"
                    "Dolar insan.\n\n"
                    "Bir de bakarsIn ki aksam olmus,\n"
                    "Pencereler yanmis, sokaklar aydinlik.\n"
                    "Hayat guzel bir sey be kardesim,\n"
                    "Yasanacak bir sey.\n\n"
                    "Bak iste cicekler acmis yine,\n"
                    "Kuslar konuyor agaclardan.\n"
                    "Bir de ruzgar var, serin serin,\n"
                    "Hep boyle gidecek sanirsin."
                ),
                "bio": (
                    "Orhan Veli Kanik (1914-1950), Garip akiminin kurucularindan biridir. "
                    "Turkce siiride devrim niteliginde yenilikler yapmis, gundelik dili ve "
                    "siradan insanin yasantisini siire tasimistir. Kisa omrune ragmen Turk "
                    "edebiyatinin en etkili sairlerinden biri olarak kabul edilmektedir."
                ),
            },
        ],
        "psikoloji": {
            "baslik": "Ogrenci Psikolojisi ve Rehberlik",
            "icerik": _psikoloji_icerik,
            "rehberlik": "Kariyer ve gelisim icin okul rehberlik servisinizden destek alin. Bireysel gorusme, grup calismalari ve meslek tanitimlari sunulmaktadir.",
            "stres_ipuclari": [
                "Derin nefes: 4 saniye nefes al, 7 saniye tut, 8 saniye ver (4-7-8 teknigi).",
                "Gunluk 30 dakika fiziksel aktivite endorfin salgilatarak ruh halinizi iyilestirir.",
                "Sosyal baglantilarinizi guclu tutun - yalnizlik en buyuk stres kaynaklarindan biridir.",
                "Gunluk tutun - duygularinizi yaziya dokmek zihinsel netlik saglar.",
                "Dogada vakit gecirin - yesil alanlar kortizol seviyesini olclebilir sekilde dusurur.",
                "Minnettarlik listesi yazin - her gun uc sey icin minnettar olun.",
                "Yeterli uyuyun - uyku eksikligi duygusal tepkiselligi yuzde altmis arttirir.",
            ],
            "ozguven": "Ozguven, kucuk basarilarin birikmesiyle olusur. Kendinize gercekci hedefler koyun ve her basariyi kutlayin. Buyume zihniyeti benimseyin: hatalar ogrenme firsatidir.",
            "soru_cevap": [
                ("Motivasyonumu kaybediyorum, ne yapabilirim?", "Kucuk, ulassilabilir hedefler belirleyin. Her tamamlanan gorevi kutlayin. Ilham verici insanlarin hikayelerini okuyun. Neden basladiginizi hatirlayiin."),
                ("Arkadaslik sorunlari yasiyorum.", "Empati kurun, dinleyin ve anlamaaya calisin. Ortak ilgi alanlari paylasin. Gerekirse okul rehberlik servisinden destek alin."),
            ],
        },
        "veli": {
            "baslik": "Velilere Oneriler",
            "icerik": _veli_icerik,
            "ev_ortami": [
                "Sabit calisma alanI - sessiz, aydinlik, duzenli.",
                "Ekran suresi sinirlamasi - calisma saatlerindee telefon baska odada.",
                "Birlikte okuma saati - ailece kitap okumak guzel bir gelenektir.",
                "Beslenme duzeni - saglikli atistirmaliklar hazir bulundurunn.",
                "Odul sistemi - basarilari kutlayin, motivasyonu destekleyin.",
                "Rutinler - her gun ayni saatte calisma, uyku ve yemek.",
            ],
            "iletisim": "Cocugunuzla acik ve yargilayici olmayan iletisim kurun. Acik uclu sorular sorun, aktif dinleme uygulayin ve duygularini yansitinn. Elestiri yerine cozum odakli yaklasim gosterin.",
            "beslenme": [
                "Kahvalti atlamamak - beyinin ana yakiti glukozdur.",
                "Omega-3 iceren gidalar - balik, ceviz, keten tohumu.",
                "Yeterli su - gunluk 1.5-2 litre.",
                "Seker sinirlamasi - asiri seker konsantrasyonu bozar.",
                "Demir ve B vitamini - ispanak, mercimek, yumurta.",
                "Meyve ve sebze - gunluk en az 5 porsiyon.",
            ],
            "aile_etkinlik": "Hafta sonu birlikte muzey, doga yuruyusu veya kitap okuma planlayiin. Ayda bir 'aile film gecesi' gelenegi olusturun. Birlikte yemek pisirmek guclu baglar kurar.",
        },
        "ogrenci_tavsiye": {
            "baslik": "Ogrencilere Tavsiyeler",
            "icerik": _ogrenci_icerik,
            "aliskanliklar": [
                "Her gun ayni saatte calisin - rutin basarinin temelidir.",
                "Calisma oncesi hedef belirleyin - ne ogreneceksinizi bilin.",
                "Tek konuya odaklanin - multitasking verimsizdir.",
                "Ogrendiklerinizi anlatarak pekistirin (Feynman Teknigi).",
                "Gecmis konulari ertelemeyin - birikim en buyuk dusmandir.",
                "Kelime ve kavram defteri tutun.",
                "Her gun tekrar yapin - sinav oncesi degil.",
                "Hatalardan ogrenin - buyume zihniyeti benimseyin.",
                "Kendinizle yarissn - baskalariyla degil.",
                "Basarilarinizi kutlayin!",
            ],
            "sinav_hazirlik": "2 hafta oncesinden baslayin, konulari bolun, gunluk 2-3 konu, mini testler uygulayin, son 3 gun genel tekrar, onceki gece erken yatin.",
            "motivasyon_sozleri": [
                '"Basari hazirlik ve firsatin bulusmasidir." - Seneca',
                '"Bin millik yolculuk tek adimla baslar." - Lao Tzu',
                '"Basariya giden yol her zaman duzeltme altindadir." - Lily Tomlin',
                '"Gelecegi sekillendirmenin en iyi yolu onu icat etmektir." - Alan Kay',
                '"Dusmanin yok ise talihsizsin, basarilarinni kimse kiskandmiyordur." - Anonim',
            ],
            "haftalik_plan": "Pzt: Matematik+Fen | Sali: Turkce+Tarih | Cars: Ing+Cog | Pers: Tekrar | Cuma: Zayif konular | Ctesi: Test | Pazar: Dinlenme+Planlama",
        },
        "kultur_sanat": {
            "baslik": "Kultur ve Sanat",
            "icerik": _kultur_icerik,
            "film": {"ad": "Bu Ayin Filmi", "yonetmen": "Yonetmen", "yil": 2024, "aciklama": "Egitim ve ilham temasiyla secilmis bu ayin film onerisi. Ogrenciler, ogretmenler ve aileler icin keyifli bir izleme deneyimi sunuyor."},
            "muzik": {"baslik": "Muzik Dunyasi", "aciklama": "Bu ay muzik koesemizde klasikten moderne, yerelden evrensele genis bir muzik yelpazesi sizi bekliyor. Muzik dinlemek stres azaltir ve yaraticiligni arttirir."},
            "sanat_eseri": {"ad": "Ayin Sanat Eseri", "sanatci": "Dunya Sanatcisi", "yil": 2000, "aciklama": "Bu ayin sanat eseri, hem teknik ustaligi hem de duygusal derinligiyle izleyiciyi etkileyen onemli bir yapittir."},
            "muze": "Bu ay bir muze ziyareti planlayin. Muzeler, kulturel mirasi kesfetmenin en etkili yollarindan biridir. Turkiye'nin 400'den fazla muzesinden birini ziyaret edin.",
        },
        "spor": {
            "baslik": "Spor Dunyasi",
            "icerik": _spor_icerik,
            "spor_tarihi": "Spor tarihi binlerce yillik bir gecmise sahiptir. Antik olimpiyatlardan modern yariismalara, spor her donemde insanlligin en heyecan verici etkinliklerinden biri olmustur.",
            "ayin_sporcusu": {"ad": "Ayin Sporcusu", "dal": "Spor Dali", "bilgi": "Bu ayin secilen sporcusu basari hikayesiyle genc sporculara ilham vermektedir. Disiplin, kararlilik ve tutku basarinin anahtarlaridir."},
            "saglik_ipucu": "Gunluk 60 dk aktivite, bol su, isinma ve soguma egzersizleri. Duzenli ama asiri olmayan egzersiz en iyi sonuclari verir.",
        },
        "ozlu_sozler": [
            {"soz": "Bilgi guctur.", "kisi": "Francis Bacon", "kategori": "Bilim"},
            {"soz": "Ogrenmenin siniri yoktur.", "kisi": "Konfucyus", "kategori": "Egitim"},
            {"soz": "Hayatta en hakiki mursit ilimdir.", "kisi": "Ataturk", "kategori": "Bilim"},
            {"soz": "Dusunuyorum, o halde varim.", "kisi": "Descartes", "kategori": "Felsefe"},
            {"soz": "Kendini bil.", "kisi": "Sokrates", "kategori": "Felsefe"},
            {"soz": "Basari, kucuk cabalarin her gun tekrarlanan toplamidir.", "kisi": "Robert Collier", "kategori": "Liderlik"},
            {"soz": "En buyuk zafer, kendini yenmektir.", "kisi": "Platon", "kategori": "Felsefe"},
            {"soz": "Bir toplumu degistirmek istiyorsaniz, egitimi degistirin.", "kisi": "Mandela", "kategori": "Liderlik"},
            {"soz": "Hayal gucu bilgiden daha onemlidir.", "kisi": "Einstein", "kategori": "Bilim"},
            {"soz": "Ogretmek iki kere ogrenmektir.", "kisi": "Joseph Joubert", "kategori": "Egitim"},
            {"soz": "Cesaret, korkmamaak degil; korkuna ragmen ileri gitmektir.", "kisi": "Nelson Mandela", "kategori": "Liderlik"},
            {"soz": "Kitaplar en sessiz ve en sadik dostlardir.", "kisi": "Victor Hugo", "kategori": "Edebiyat"},
            {"soz": "Her gun bir sey ogrenilmelidir.", "kisi": "Seneca", "kategori": "Felsefe"},
            {"soz": "Egitim gelecegi sekillendirmenin en guclu silahidir.", "kisi": "Nelson Mandela", "kategori": "Egitim"},
            {"soz": "Basarmak icin baslamak gerekir.", "kisi": "Mark Twain", "kategori": "Liderlik"},
        ],
        "bilmeceler": [
            ("Dal ustunde iki satir, biri altin biri katir.", "Goz kapaklari ve kirpikler"),
            ("Buyudukce hafifler, kuculdukce agirLasir.", "Balon"),
            ("Annesi beyaz, cocugu kirmizi.", "Dis ve dis eti"),
            ("Kolsuz sarilir, dilsiz konusur.", "Kitap"),
            ("Beyaz tarlaya siyah tohum ekerler.", "Kagit ve yazi"),
            ("Icinde ates yanar, kendisi yanmaz.", "Lamba"),
            ("Herkesle gider, herkesle gelir, ama baska bir sey degil.", "Golge"),
            ("Gokten sessizce gelir, yumumsak bir ortu serer.", "Kar"),
        ],
        "mantik_sorulari": [
            ("3 tavuk 3 gunde 3 yumurta yapar. 12 tavuk 12 gunde kac yumurta yapar?", "48 yumurta"),
            ("Bir babanin 3 kizi var, her kizin 1 erkek kardesi var. Ailede kac cocuk var?", "4 cocuk (3 kiz + 1 erkek)"),
            ("Saat 3'te saat kac kez calar? 12'de kac kez?", "3'te 3 kez, 12'de 12 kez"),
        ],
        "matematik_bulmacalari": [
            "3 + 3 x 3 = ? (Islem onceligi!)",
            "1 + 2 + 3 + ... + 10 = ?",
            "Bir sayinin yarisi 15 ise sayi kactir?",
            "4! (4 faktoriyel) = ?",
        ],
        "matematik_cevaplar": ["12", "55", "30", "24"],
        "kim_bu": {"ipuclari": ["Turkiye Cumhuriyeti'nin kurucusu.", "1881 Selanik dogumlu.", "Modern Turkiye'yi kuran lider.", "Ilke ve inkilaplariyla cag atlatti."], "cevap": "Mustafa Kemal Ataturk"},
        "quiz": [
            {"soru": f"{_t} temasinda hangi konu isklenmistir?", "secenekler": [f"A) {_t}", "B) Uzay", "C) Matematik", "D) Resim"], "cevap": "A", "zorluk": 1},
            {"soru": "Bilimsel yontemin ilk adiimi nedir?", "secenekler": ["A) Deney", "B) Gozlem", "C) Hipotez", "D) Sonuc"], "cevap": "B", "zorluk": 1},
            {"soru": "Dunyanin en eski universitesi hangisidir?", "secenekler": ["A) Oxford", "B) Bologna", "C) El-Karaviyyin", "D) Harvard"], "cevap": "C", "zorluk": 2},
            {"soru": "Modern Olimpiyatlar hangi yil basladi?", "secenekler": ["A) 1896", "B) 1900", "C) 1888", "D) 1912"], "cevap": "A", "zorluk": 1},
            {"soru": "Pomodoro teknikinde calisma suresi kac dakikadir?", "secenekler": ["A) 15", "B) 20", "C) 25", "D) 30"], "cevap": "C", "zorluk": 2},
            {"soru": "BDNF nedir?", "secenekler": ["A) Bir gen", "B) Beyin proteini", "C) Hormon", "D) Vitamin"], "cevap": "B", "zorluk": 2},
            {"soru": "Turkiye'den kac alan UNESCO listesindedir?", "secenekler": ["A) 12", "B) 15", "C) 19", "D) 25"], "cevap": "C", "zorluk": 2},
            {"soru": "Naim Suleymanoglu hangi daldda basarili olmustur?", "secenekler": ["A) Gures", "B) Halter", "C) Boks", "D) Atletizm"], "cevap": "B", "zorluk": 1},
            {"soru": "Cornell not alma yontemi kac bolumludur?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": "B", "zorluk": 2},
            {"soru": "Hangi vitamin gunes isigiyla sentezlenir?", "secenekler": ["A) A", "B) B12", "C) C", "D) D"], "cevap": "D", "zorluk": 1},
            {"soru": "Kuzey Kutbu sumru kusu yilda kac km goc eder?", "secenekler": ["A) 10.000", "B) 30.000", "C) 50.000", "D) 70.000"], "cevap": "D", "zorluk": 2},
            {"soru": "DNA'nin yapisi ne zaman kesfedildi?", "secenekler": ["A) 1943", "B) 1953", "C) 1963", "D) 1973"], "cevap": "B", "zorluk": 3},
            {"soru": "Isik hizi yaklasik saniyede kac km'dir?", "secenekler": ["A) 150.000", "B) 200.000", "C) 300.000", "D) 400.000"], "cevap": "C", "zorluk": 2},
            {"soru": "Harry Potter serisini kim yazmistir?", "secenekler": ["A) Tolkien", "B) Rowling", "C) Lewis", "D) Dahl"], "cevap": "B", "zorluk": 1},
            {"soru": "Feynman Teknigi neye dayanir?", "secenekler": ["A) Ezbere", "B) Baskasina anlatmaya", "C) Test cozmeye", "D) Not almaya"], "cevap": "B", "zorluk": 3},
        ],
        "quiz_puan_rehberi": "0-5: Tekrar gerekli | 6-9: Iyi | 10-12: Cok Iyi | 13-15: Mukemmel!",
        "okuyucu_mektuplari": [
            {"ad": "SmartCampus Okuyucusu", "mesaj": "Derginiz her ay daha da iyilesiyor. Bilim ve edebiyat bolumleri favorim!"},
        ],
        "sonraki_sayi": {"tema": "Gelecek Tema", "teasers": ["Bilim Ozel", "Tarih Kesfi", "Yeni Gezi Rotasi", "Spor Haberleri"]},
        # YENi BÖLÜMLER (template)
        "hobi_kosesi": {
            "baslik": "Hobi Kosesi",
            "hobiler": [
                {"ad": "El Sanatlari", "aciklama": f"{_t} temasiyla baglantili yaratici el sanatlari. Basit malzemelerle evde yapabilecginiz projeler ile hem ogrenin hem egllenin.", "emoji": "🎨"},
                {"ad": "Bilim Deneyleri", "aciklama": "Evde yapabilceginiz basit bilim deneyleri ile bilimsel dusunme becerinizi gelistirin. Guvenli ve egitici deneyler icin gerekli malzemeler genellikle mutfaginizda bulunur.", "emoji": "🔬"},
            ],
            "ipucu": f"{_t} temasina uygun hobiler kesfetmek icin merakinizi takip edin.",
        },
        "ilginc_bilgiler": [
            "Bir ahtapotun uc kalbi ve mavi kani vardir.",
            "Dunya uzerinde insanlardan daha fazla karinca yasamaktadir.",
            "Bir kelebegin kanatlarindaki renkler pigment degildir, isik kirinimindan olusur.",
            "Insan gozu yaklasik 10 milyon farkli rengi ayirt edebilir.",
            "Bir buluttaki ortalama su miktari yaklasik 500 tondur.",
            "Isik Gunes'ten Dunya'ya 8 dakika 20 saniyede ulasir.",
            "Ay her yil Dunya'dan 3.8 cm uzaklassmaktadir.",
            "Einstein 4 yasina kadar konusamamisstir.",
        ],
        "eglence_kosesi": {
            "fikralar": [
                "Ogretmen: 'Dunyanin en buyuk okyanusu hangisidir?' Ogrenci: 'Bilmiyorum ama en buyuk su birikintisi bizim bahcede!'",
                "Baba: 'Sinav nasil gecti?' Cocuk: 'Sorular kolaydii, cevaplar zordu!'",
            ],
            "bilgi_yarismasi": [
                {"soru": "Dunyanin en yuksek dagi hangisidir?", "cevap": "Everest"},
                {"soru": "Hangi element semboluu 'O' dir?", "cevap": "Oksijen"},
                {"soru": "Turkiye'nin baskenti neresidir?", "cevap": "Ankara"},
            ],
            "labirent_aciklama": "Labirentte A noktasindan B noktasina ulasin!",
        },
        "felsefe_kosesi": {
            "baslik": "Dusunce Dunyasi",
            "filozof": {"ad": "Aristoteles", "donem": "MO 384-322", "ulke": "Antik Yunanistan",
                "biyografi": "Aristoteles, Platon'un ogrencisi ve Buyuk Iskender'in hocasidir. Mantik, fizik, biyoloji, etik ve siyaset gibi pek cok alanda eserler vermistir.",
                "temel_fikir": "Mutluluk (eudaimonia) erdemli yasamla elde edilir. Bilgi deneyimle baslar.",
            },
            "dusunce_sorusu": f"{_t} ile ilgili: Bilgi mi guc getirir, yoksa guc mu bilgi?",
            "sozler": [
                '"Egitimin kokleri acidir, meyveleri tatlidir." - Aristoteles',
                '"Bilmek yetmez, uygulamak gerekir." - Goethe',
            ],
        },
        "muzik_kosesi": {
            "baslik": "Muzik Dunyasi",
            "sanatci": {"ad": "Wolfgang A. Mozart", "donem": "1756-1791", "ulke": "Avusturya",
                "bilgi": "Mozart, muzik tarihinin en buyuk dahilerinden biridir. 5 yasindan itibaren beste yapmaya baslayan Mozart, 35 yillik kisa yasaminda 600'den fazla eser bestemistir.",
            },
            "tur_tanitimi": {
                "ad": "Klasik Muzik",
                "aciklama": "Klasik muzik, yuzyillar boyunca gelisen zengin bir gelenektir. Orkestra, oda muzigi ve solo performanslar bu turun temel formlarini olusturur.",
            },
            "dinleme_onerisi": "Bu ay dinleyin: Mozart - Kucuk Gece Muzigi (Eine kleine Nachtmusik). Klasik muzige giris icin muhtesem bir eser.",
        },
        "kelime_bulmacasi_50": {
            "baslik": "Mega Kelime Bulmacasi (50 Kelime)",
            "kelimeler": [
                "BILIM", "TARIH", "DOGA", "SANAT", "SPOR", "MUZIK", "FELSEFE", "EDEBIYAT",
                "ATOM", "HUCRE", "GEZEGEN", "GALAKSI", "NORON", "ENZIM", "GEN", "PROTEIN",
                "ROMA", "MISIR", "YUNAN", "OSMANLI", "SUMER", "HITIT", "SELCUKLU", "ANADOLU",
                "ORMAN", "OKYANUS", "VOLKAN", "DEPREM", "IKLIM", "KUTUP", "CORAL", "FIRTINA",
                "RESIM", "HEYKEL", "TIYATRO", "SINEMA", "OPERA", "BALE", "SERAMIK", "EBRU",
                "FUTBOL", "BASKETBOL", "YUZME", "ATLETIZM", "TENIS", "VOLEYBOL", "OKCULUK", "GURES",
                "PIYANO", "KEMAN",
            ],
            "ipucu": "Kelimeler yatay, dikey ve capraz olarak gizlenmistir. Tum 50 kelimeyi bulun!",
        },
        "zeka_sorulari": [
            {"soru": "Hangi kelime sozlukte yanlis yazilmistir?", "cevap": "'Yanlis' kelimesi."},
            {"soru": "5 baligi 5 kedi 5 dakikada yer. 100 baligi 100 kedi kac dakikada yer?", "cevap": "5 dakikada. Her kedi 5 dakikada 1 balik yer."},
            {"soru": "Bir adam yagmurda semsiyesiz yuruyor ama saclari islanmiyor. Nasil?", "cevap": "Adam keldir."},
            {"soru": "Bir odada 4 kose var. Her kosede 1 kedi. Her kedinin onunde 3 kedi var. Toplam kac kedi?", "cevap": "4 kedi."},
        ],
    }


# ---------------------------------------------------------------------------
# STORY BUILDER - Tum icerik burada flowable olarak olusturulur
# ---------------------------------------------------------------------------
def _build_story(data, images=None):
    """Dergi icerigini Platypus flowable listesi olarak olusturur."""
    styles = _get_styles()
    story = []
    s = styles
    imgs = images or {}

    def _add_section_image(section_key, width=12*cm, height=7*cm):
        """Bolum gorseli varsa ekle."""
        path = imgs.get(section_key)
        img = _safe_image(path, width=width, height=height)
        if not isinstance(img, Spacer):
            story.append(Spacer(1, 6))
            story.append(img)
            story.append(Spacer(1, 6))

    # -----------------------------------------------------------------------
    # SAYFA 1: KAPAK (bos frame - cover page callback ile cizilir)
    # -----------------------------------------------------------------------
    story.append(Spacer(1, PAGE_H - 4 * cm))  # kapak sayfasi icin placeholder
    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 2-3: ICINDEKILER + EDITORDEN
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("ICINDEKILER", NAVY, icon=""))
    story.append(Spacer(1, 8))

    # TOC as table
    toc = data.get("icerik_tablosu", [])
    toc_data = []
    for title, page in toc:
        toc_data.append([
            Paragraph(title, s["TOCEntry"]),
            Paragraph(str(page), s["TOCPage"]),
        ])
    if toc_data:
        toc_table = Table(toc_data, colWidths=[PAGE_W - 5.5 * cm, 1.5 * cm])
        toc_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, HexColor("#e0e0e0")),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (0, -1), 5),
        ]))
        story.append(toc_table)

    story.append(Spacer(1, 12))
    story.append(GoldLine())
    story.append(Spacer(1, 8))

    # Editorden
    story.append(SectionHeaderBar("EDITORDEN", HexColor("#1e3a5f"), icon=""))
    story.append(Spacer(1, 8))

    # Mascot image in editorial
    mascot_img = _safe_image(MASCOT_PATH, width=2.5 * cm, height=2.5 * cm)
    if not isinstance(mascot_img, Spacer):
        mascot_para = Paragraph(
            "<b>Smarti Dergi Yayin Kurulu</b><br/>"
            "<i>Bilgi, ilham ve eglence dolu 30 sayfa!</i>",
            s["Body"])
        story.append(_make_two_col_table([mascot_img], [mascot_para], left_pct=0.2))
        story.append(Spacer(1, 8))

    editorial = data.get("editorial", "")
    for para_text in editorial.split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 4-6: BILIM & TEKNIK
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("BILIM & TEKNIK", SECTION_COLORS["bilim"], icon=""))
    _add_section_image("bilim", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))

    for idx, article in enumerate(data.get("bilim_teknik", [])):
        story.append(Paragraph(article["baslik"], s["ArticleTitle"]))
        if article.get("giris"):
            story.append(Paragraph(f'<i>{article["giris"]}</i>', s["BodySmall"]))
            story.append(Spacer(1, 4))

        for para_text in article.get("icerik", "").split("\n\n"):
            para_text = para_text.strip()
            if para_text:
                story.append(Paragraph(para_text, s["Body"]))

        # Biliyor muydunuz box
        if article.get("biliyor_muydunuz"):
            story.append(Spacer(1, 6))
            story.append(_make_info_box(
                "Biliyor Muydunuz?",
                article["biliyor_muydunuz"],
                accent_color=SECTION_COLORS["bilim"],
                bg="#e8f0fe"
            ))

        if idx < len(data.get("bilim_teknik", [])) - 1:
            story.append(Spacer(1, 10))
            story.append(GoldLine())
            story.append(Spacer(1, 6))

    # Bilim sozlugu
    sozluk = data.get("bilim_sozlugu", [])
    if sozluk:
        story.append(Spacer(1, 10))
        story.append(_make_section_bar("BILIM SOZLUGU", color_key="bilim"))
        story.append(Spacer(1, 4))
        story.extend(_make_glossary_table(sozluk))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 7-8: TEKNOLOJI
    # -----------------------------------------------------------------------
    tech = data.get("teknoloji", {})
    story.append(SectionHeaderBar("TEKNOLOJI DUNYASI", SECTION_COLORS["teknoloji"], icon=""))
    _add_section_image("teknoloji", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(tech.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in tech.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Haberler
    haberler = tech.get("haberler", [])
    if haberler:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Teknoloji Haberleri",
            haberler,
            accent_color=SECTION_COLORS["teknoloji"],
            bg="#f3e8ff"
        ))

    # Gelecekte Bu Var
    gelecek = tech.get("gelecekte_bu_var", "")
    if gelecek:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>GELECEKTE BU VAR</b>", s["SubTitle"]))
        story.append(Paragraph(gelecek, s["Body"]))

    # Ek teknoloji icerigi - sayfa doldurucu
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>DIJITAL OKURYAZARLIK REHBERI</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Dijital okuryazarlik, 21. yuzyilin en temel becerilerinden biridir. Bilgiye erisim, "
        "bilgiyi degerlendirme, dijital icerik uretme ve dijital ortamda guvenli davranma "
        "bu becerinin dort temel bilesenidir. Ogrencilerin internetteki bilgileri elestrel "
        "gozle degerlendirmesi, kaynak guvenilirligini sorgulmasi ve yanlis bilgiyi ayirt "
        "etmesi gunumuzde her zamankinden daha onemlidir.", s["Body"]))
    story.append(Paragraph(
        "Veri gizliligi ve kisisel bilgi guvenligi de dijital okuryazarligin kritik bir "
        "parcasidir. Guclu sifre olusturma, iki faktorlu dogrulama kullanma, supheli "
        "e-postalari tanimlama ve sosyal medyada paylasimlarda dikkatli olma temel "
        "guvenlik aliskanliklarindan biridir. KVKK (Kisisel Verilerin Korunmasi Kanunu) "
        "kapsaminda haklarinizi bilmeniz de buyuk onem tasimaktadir.", s["Body"]))
    story.append(Paragraph(
        "Yapay zeka araclari ile etik kullanim da yeni bir dijital okuryazarlik alanidir. "
        "AI uretilen iceriklerin kaynaklarini sorgulamak, AI araclariyla uretilen metinleri "
        "ozgun calismanin yerine koymamak ve bu araclari ogrenmeyi destekleyici bir sekilde "
        "kullanmak ogrencilerin gelistirmesi gereken yeni becerilerdir.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 9-10: TARIH
    # -----------------------------------------------------------------------
    tarih = data.get("tarih", {})
    story.append(SectionHeaderBar("TARIH SAYFASI", SECTION_COLORS["tarih"], icon=""))
    _add_section_image("tarih", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(tarih.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in tarih.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Zaman cizelgesi
    zc = tarih.get("zaman_cizelgesi", [])
    if zc:
        story.append(Spacer(1, 8))
        story.append(_make_section_bar("ZAMAN CIZELGESI", color_key="tarih"))
        story.extend(_make_timeline(zc))

    # Tarihte bu ay
    tba = tarih.get("tarihte_bu_ay", [])
    if tba:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Tarihte Bu Ay",
            tba,
            accent_color=SECTION_COLORS["tarih"],
            bg="#fef3c7"
        ))

    # Tarih sozu
    ts = tarih.get("tarih_sozu", {})
    if ts:
        story.append(Spacer(1, 6))
        story.append(_make_pull_quote(ts["soz"], ts["kisi"]))

    # Ek tarih icerigi
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>TARIHTEN ALINACAK DERSLER</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Tarih, yalnizca gecmiste ne oldugunu degil, neden oldugunu ve gelecekte "
        "ne olabilecegini anlamamiza yardimci olur. Tarihi olaylarin arka planindaki "
        "ekonomik, sosyal ve kulturel dinamikleri kavramak, bugunun karmasik sorunlarini "
        "cozumlemek icin bize anahtar sualr. Tarihi bilincle okuyan bireyler, "
        "propaganda ve manipulasyona karsi daha direncli olur.", s["Body"]))
    story.append(Paragraph(
        "Her ulkenin tarihi, o ulkenin kimliginin ve degerlerinin temelidir. Turk tarihi, "
        "Orta Asya'dan Anadolu'ya uzanan goc yolculugu, Selcuklu ve Osmanli "
        "medeniyetleri ve modern Turkiye Cumhuriyeti'nin kurulussuyla zengin bir anlatiya "
        "sahiptir. Bu zengin mirasi taniimak ve gelecek kusaklara aktarmak hepimizin "
        "gorevidir. Tarih bilinci, toplumsal birlik ve beraberligin temel "
        "taslarinndan biridir.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # COGRAFYA & GEZI
    # -----------------------------------------------------------------------
    gezi = data.get("cografya_gezi", {})
    story.append(SectionHeaderBar(
        f'COGRAFYA & GEZI: {gezi.get("yer", "")} ({gezi.get("ulke", "")})',
        SECTION_COLORS["gezi"], icon=""
    ))
    story.append(Spacer(1, 8))

    # Baskent bilgi kutusu
    bb = gezi.get("baskent_bilgi", {})
    if bb:
        info_items = [f"{k.title()}: {v}" for k, v in bb.items()]
        story.append(_make_info_box(
            f'{gezi.get("yer", "")} Bilgi Karti',
            info_items,
            accent_color=SECTION_COLORS["gezi"],
            bg="#ecfdf5"
        ))
        story.append(Spacer(1, 6))

    for para_text in gezi.get("tanitim", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Gorulmesi gereken yerler
    gg = gezi.get("gorulmesi_gereken", [])
    if gg:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>GORULMESI GEREKEN YERLER</b>", s["SubTitle"]))
        for yer in gg:
            story.append(Paragraph(f"<bullet>&bull;</bullet> {yer}", s["BulletItem"]))

    # Yemek onerileri
    yo = gezi.get("yemek_onerileri", [])
    if yo:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Lezzet Duraklari",
            yo,
            accent_color=HexColor("#ea580c"),
            bg="#fff7ed"
        ))

    # Harita aciklama
    ha = gezi.get("harita_aciklama", "")
    if ha:
        story.append(Spacer(1, 6))
        story.append(Paragraph(f'<i>{ha}</i>', s["BodySmall"]))

    # Ek gezi icerigi
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>SEYAHAT IPUCLARI</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Seyahat planlamasi, keyifli bir gezi deneyiminin temelidir. Gidilecek yerin iklimini, "
        "kulturel ozelliklerini ve ulasilm olanaklarini onceden arastirmak hem zaman hem de "
        "butce tasarrufu saglar. Yerel halk ile iletisim kurmak, turist mekanlarinin disindaki "
        "otantik deneyimleri kesfetmek seyahatin en degerli yanlaridir.", s["Body"]))
    story.append(Paragraph(
        "Surdurulebilir seyahat ilkeleri gunumuzde giderek daha onemli hale gelmektedir. "
        "Yerel isletmeleri tercih etmek, plastik atik uretimini minimumda tutmak, dogal "
        "alanlarda iz birakmamak ve yerel kulturlere saygi gostermek sorumlu gezginligin "
        "temel prensipleridir. Ekoturizm, hem gezginlere essiz deneyimler sunar hem de "
        "yerel topluluklara ekonomik katki saglar.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # DOGA & CEVRE
    # -----------------------------------------------------------------------
    doga = data.get("doga_cevre", {})
    story.append(SectionHeaderBar("DOGA & CEVRE", SECTION_COLORS["doga"], icon=""))
    _add_section_image("doga", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(doga.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in doga.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Nesli tehlikede turler
    nt = doga.get("nesli_tehlike", [])
    if nt:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>NESLI TEHLIKE ALTINDAKI TURLER</b>", s["SubTitle"]))
        for tur, bilgi in nt:
            story.append(Paragraph(f'<font color="#dc2626"><b>{tur}:</b></font> {bilgi}', s["BodySmall"]))

    # Eko ipuclari
    eko = doga.get("eko_ipuclari", [])
    if eko:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Cevre Dostuculuk Ipuclari",
            eko,
            accent_color=SECTION_COLORS["doga"],
            bg="#f0fdf4"
        ))

    # Mevsim gozlem
    mg = doga.get("mevsim_gozlem", "")
    if mg:
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<b>Mevsim Gozlemi:</b> {mg}", s["BodySmall"]))

    # Ek cevre icerigi
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>CEVRE GONULLULUGU</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Cevre gonullulugu, hem dogaya katki saglamanin hem de kisisel gelisimin en "
        "etkili yollarindan biridir. Sahil temizligi, agac dikme kampanyalari, hayvan "
        "barinaklarinda gonullu calisma ve cevre bilinclendirme etkinlikleri bu "
        "alandaki baslica faaliyetlerdir. Okullarda cevre kuluupleri olusturarak "
        "ogrencilerin erken yaslarda cevre sorumllulugu kazanmalari saglanabilir. "
        "Her kucuk adim buyuk farklilikllar yaratir.", s["Body"]))
    story.append(Paragraph(
        "Karbon ayak izi hesaplamak, bireysel cevre etkimizi anlamanin ilk adimidir. "
        "Online araclar sayesinde gunluk faaliyetlerinnizin cevreye etkisini "
        "olcebilirsiniz. Ulasiim, beslenme, enerji tuketimi ve tuketim aliskanliklari "
        "karbon ayak izinizin ana bilesenleridir. Kucuk degisiklikler bile birikince "
        "buyuk fark yaratir: yerel urun satin almak, toplu tasima kullanmak ve "
        "enerji verimli cihazlar tercih etmek gibi.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 15-16: EDEBIYAT
    # -----------------------------------------------------------------------
    ed = data.get("edebiyat", {})
    story.append(SectionHeaderBar("EDEBIYAT KOSESI", SECTION_COLORS["edebiyat"], icon=""))
    _add_section_image("edebiyat", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(f'{ed.get("kitap", "")} - {ed.get("yazar", "")}', s["ArticleTitle"]))
    if ed.get("tur") and ed.get("sayfa"):
        story.append(Paragraph(f'<i>Tur: {ed["tur"]} | {ed["sayfa"]} sayfa</i>', s["SmallGray"]))
    story.append(Spacer(1, 4))

    for para_text in ed.get("tanitim", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Yazar biyografi
    if ed.get("yazar_bio"):
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>YAZAR HAKKINDA</b>", s["SubTitle"]))
        story.append(Paragraph(ed["yazar_bio"], s["Body"]))

    # Edebi soz
    es = ed.get("edebi_soz", {})
    if es:
        story.append(Spacer(1, 6))
        story.append(PullQuote(es["soz"], es["kisi"], SECTION_COLORS["edebiyat"]))

    # Bu ay okuyun
    bao = ed.get("bu_ay_okuyun", [])
    if bao:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>BU AY OKUYUN</b>", s["SubTitle"]))
        for book in bao:
            story.append(Paragraph(
                f'<bullet>&bull;</bullet> <b>{book["kitap"]}</b> - {book["yazar"]} '
                f'({book["tur"]}, {book["sayfa"]} sayfa)',
                s["BulletItem"]
            ))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 17: SIIR KOSESI
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("SIIR KOSESI", SECTION_COLORS["siir"], icon=""))
    story.append(Spacer(1, 10))

    for poem in data.get("siir", []):
        story.append(Paragraph(poem["baslik"], s["PoemTitle"]))
        story.append(Paragraph(f'<i>{poem["sair"]}</i>', s["SmallGray"]))
        story.append(Spacer(1, 6))
        # Siir metni - satirlari <br/> ile ayir
        lines = poem["metin"].replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
        story.append(Paragraph(lines, s["PoemText"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(poem.get("bio", ""), s["PoemBio"]))
        story.append(Spacer(1, 10))
        story.append(GoldLine())
        story.append(Spacer(1, 10))

    # Ek siir icerigi - sayfa doldurucu
    story.append(Paragraph("<b>SIIR HAKKINDA</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Siir, insanligin en eski sanat formlarindan biridir. Sumerlerden bugun kadar "
        "uzanan zengin bir gelenegedayanir. Ritim, kafiye, imgelem ve duygu yuklenmis "
        "kelimeler araciligiyla siir, dusunceleri ve hisleri en yogun bicimde ifade eder. "
        "Turk siir gelenegi, Divan edebiyatinin aruz olcusunden Halk edebiyatinin hece "
        "olcusune, oradan serbest siire uzanan genis bir yelpazeye sahiptir.", s["Body"]))
    story.append(Paragraph(
        "Serbest siir, 20. yuzyilda siiri geleneksel kaliplardan kurtarmis ve siire yeni "
        "bir ifade ozgurlugu kazandirmistir. Orhan Veli Kanik, Oktay Rifat ve Melih Cevdet "
        "Anday'in onculuk ettigi Garip Hareketi, Turk siirinde devrimsel bir donusume yol "
        "acmistir. Nazim Hikmet'in toplumcu gercekci siiri ise dunya edebiyatinda buyuk "
        "yanki uyandirmistir.", s["Body"]))
    story.append(Paragraph(
        "Siir okumak, dil becerilerini gelistirir, soyut dusunme kapasitesini arttirir ve "
        "duygusal zekayi besler. Ogrencilerin siirle erken yaslarda tanisasi, hem "
        "edebiyat sevgisini hem de yaratici yazma becerilerini destekler. Kendiniz de "
        "siir yazmayi deneyin - duygu ve dusuncelerinizi kelimelerle ifade etmenin ne "
        "kadar tatmin edici oldugunu kesfedeceksiniz.", s["Body"]))
    story.append(Spacer(1, 8))
    story.append(PullQuote(
        "Siir, sozun muzigi; sozlerin resimlere donustugu buyulu bir sanattir.",
        "Smarti Dergi"
    ))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 18-19: PSIKOLOJI & REHBERLIK
    # -----------------------------------------------------------------------
    psi = data.get("psikoloji", {})
    story.append(SectionHeaderBar("PSIKOLOJI & REHBERLIK", SECTION_COLORS["psikoloji"], icon=""))
    _add_section_image("psikoloji", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(psi.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in psi.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Stres ipuclari
    si = psi.get("stres_ipuclari", [])
    if si:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Stres Yonetimi Ipuclari",
            si,
            accent_color=SECTION_COLORS["psikoloji"],
            bg="#ecfeff"
        ))

    # Ozguven
    ozg = psi.get("ozguven", "")
    if ozg:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>OZGUVEN GELISTIRME</b>", s["SubTitle"]))
        story.append(Paragraph(ozg, s["Body"]))

    # Rehberlik
    reh = psi.get("rehberlik", "")
    if reh:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>KARIYER REHBERLIGI</b>", s["SubTitle"]))
        story.append(Paragraph(reh, s["Body"]))

    # Soru cevap
    sc = psi.get("soru_cevap", [])
    if sc:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>SORU - CEVAP</b>", s["SubTitle"]))
        for soru, cevap in sc:
            story.append(Paragraph(f'<font color="#0891b2"><b>S:</b></font> {soru}', s["Body"]))
            story.append(Paragraph(f'<font color="#059669"><b>C:</b></font> {cevap}', s["Body"]))
            story.append(Spacer(1, 4))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # VELI KOSESI
    # -----------------------------------------------------------------------
    veli = data.get("veli", {})
    story.append(SectionHeaderBar("VELI KOSESI", SECTION_COLORS["veli"], icon=""))
    story.append(Spacer(1, 8))
    story.append(Paragraph(veli.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in veli.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Ev ortami
    eo = veli.get("ev_ortami", [])
    if eo:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Ideal Ev Calisma Ortami",
            eo,
            accent_color=SECTION_COLORS["veli"],
            bg="#fff7ed"
        ))

    # Iletisim
    ilet = veli.get("iletisim", "")
    if ilet:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>ETKILI ILETISIM</b>", s["SubTitle"]))
        story.append(Paragraph(ilet, s["Body"]))

    # Beslenme
    bes = veli.get("beslenme", [])
    if bes:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            "Saglikli Beslenme Onerileri",
            bes,
            accent_color=HexColor("#16a34a"),
            bg="#f0fdf4"
        ))

    # Aile etkinlik
    ae = veli.get("aile_etkinlik", "")
    if ae:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>AILE ETKINLIK ONERILERI</b>", s["SubTitle"]))
        story.append(Paragraph(ae, s["Body"]))

    # Ek veli icerigi
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>DIJITAL CAGDA EBEVEYNLIK</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Dijital cagda ebeveynlik, yeni zorluklar ve firsatlar sunmaktadir. Cocuklarin "
        "teknoloji ile iliskisini saglikli bir sekilde yonetmek, modern ebeveynligin "
        "en kritik gorevlerinden biridir. Yasaklayici bir yaklasim yerine, rehberlik "
        "edici bir tutum benimsemek cok daha etkilidir. Cocugunuzla birlikte teknolojiyi "
        "kesfetmek, guvenli internet kullanim aliskanliklarini birlikte olusturmak ve "
        "ekran basinda gecirilen zamani kaliteli iceriklerle doldurmak onemlidir.", s["Body"]))
    story.append(Paragraph(
        "Sosyal medya, ergenler icin hem firsatlar hem de riskler barindirmaktadir. "
        "Siber zorbalik, olumsuz beden imaji ve dijital bagimlilik en yaygin riskler "
        "arasindadir. Bu konularda cocugunuzla acik bir diyalog kurmak, yasadigi "
        "sorunlari paylasabilecegi guvenli bir ortam olusturmak buyuk onem tasir. "
        "Aile sozlesmesi adi altinda dijital kullanim kurallari birlikte beliirlenebilir.", s["Body"]))
    story.append(Paragraph(
        "Cocugunuzun ekran disinda gecirdigi zamani zenginlestirmek de dijital cag "
        "ebeveynliginin onemli bir boyutudur. Spor, muzik, resim, drama gibi sanatsal "
        "ve sportif etkinlikler cocugun cok yonlu gelisimini destekler. Dogada vakit "
        "gecirmek, bahceyle ilgilenmek veya bir hayvan bakmak sorumluluk duygusu ve "
        "empati gelistirir.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 22-23: OGRENCI TAVSIYELERI
    # -----------------------------------------------------------------------
    ogr = data.get("ogrenci_tavsiye", {})
    story.append(SectionHeaderBar("OGRENCILERE TAVSIYELER", SECTION_COLORS["ogrenci"], icon=""))
    story.append(Spacer(1, 8))
    story.append(Paragraph(ogr.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in ogr.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # 10 aliskanlik
    al = ogr.get("aliskanliklar", [])
    if al:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>BASARILI OGRENCILERIN 10 ALISKANLIGI</b>", s["SubTitle"]))
        for i, item in enumerate(al, 1):
            story.append(Paragraph(f'<font color="#2563eb"><b>{i}.</b></font> {item}', s["BodySmall"]))

    # Sinav hazirlik
    sh = ogr.get("sinav_hazirlik", "")
    if sh:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>SINAV HAZIRLIK PLANI</b>", s["SubTitle"]))
        story.append(Paragraph(sh, s["Body"]))

    # Haftalik plan
    hp = ogr.get("haftalik_plan", "")
    if hp:
        story.append(Spacer(1, 6))
        story.append(_make_info_box(
            "Ornek Haftalik Calisma Plani",
            [hp],
            accent_color=SECTION_COLORS["ogrenci"],
            bg="#eff6ff"
        ))

    # Motivasyon sozleri
    ms = ogr.get("motivasyon_sozleri", [])
    if ms:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>MOTIVASYON SOZLERI</b>", s["SubTitle"]))
        for soz in ms:
            story.append(Paragraph(f'<i>{soz}</i>', s["BodySmall"]))

    # Ek ogrenci icerigi
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>AKADEMIK BASARI ICIN ALTIN KURALLAR</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Akademik basari tesaduf degil, planlama ve disiplinin sonucudur. Duzenli "
        "calisma, etkili not alma, aktif geri cagirma ve aralikli tekrar yontemlerini "
        "birlestirerek kendi ogrenme sisteminizi kurun. Sinif icinde aktif katilim "
        "gostemek, derste soru sormak ve tartismalara katilmak ogrenmenin en etkili "
        "yollarindan biridir. Pasif dinleme yerine aktif katilim tercih edin.", s["Body"]))
    story.append(Paragraph(
        "Mentorlar ve rol modeller bulmak da basari yolculugunuzdda onemli bir "
        "destektir. Ogretmenlerinizden, ust sinif ogrencilerinden veya alaninda "
        "basarili insanlardan ilham ve rehberlik alabilirsiniz. Basarili insanlarin "
        "biyografilerini okumak, karsilastiklari zorluklari ve bunlari nasil "
        "astikllarini ogrenmek motivasyon kaynagidir.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 24-25: KULTUR & SANAT
    # -----------------------------------------------------------------------
    kul = data.get("kultur_sanat", {})
    story.append(SectionHeaderBar("KULTUR & SANAT", SECTION_COLORS["kultur"], icon=""))
    _add_section_image("kultur", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(kul.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in kul.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Film
    film = kul.get("film", {})
    if film:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>FILM ONERISI</b>", s["SubTitle"]))
        story.append(Paragraph(
            f'<b>{film.get("ad", "")}</b> ({film.get("yil", "")}) - Yonetmen: {film.get("yonetmen", "")}',
            s["Body"]
        ))
        story.append(Paragraph(film.get("aciklama", ""), s["Body"]))

    # Muzik
    muzik = kul.get("muzik", {})
    if muzik:
        story.append(Spacer(1, 6))
        story.append(Paragraph(f'<b>MUZIK: {muzik.get("baslik", "")}</b>', s["SubTitle"]))
        story.append(Paragraph(muzik.get("aciklama", ""), s["Body"]))

    # Sanat eseri
    se = kul.get("sanat_eseri", {})
    if se:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>SANAT ESERI</b>", s["SubTitle"]))
        story.append(Paragraph(
            f'<b>{se.get("ad", "")}</b> - {se.get("sanatci", "")} ({se.get("yil", "")})',
            s["Body"]
        ))
        story.append(Paragraph(se.get("aciklama", ""), s["Body"]))

    # Muze
    muze = kul.get("muze", "")
    if muze:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>MUZE ONERISI</b>", s["SubTitle"]))
        story.append(Paragraph(muze, s["Body"]))

    # Ek kultur icerigi
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>YARATICI DUSUNME VE SANAT</b>", s["SubTitle"]))
    story.append(Paragraph(
        "Yaratici dusunme, 21. yuzyilin en degerli becerilerinden biridir ve sanat "
        "egitimi bu becerinin gelisiminde kritik bir rol oynar. Sanatla ugrasan bireyler, "
        "farkli perspektiflerden bakma, kaliplarin disinda dusunme ve yenilikci cozumler "
        "uretme konusunda daha basarilidir. Steve Jobs, Apple'in basarisini teknoloji ve "
        "sanatin kesisim noktasinda bulma becerisine baglamistir.", s["Body"]))
    story.append(Paragraph(
        "Okullarda sanat egitimi yalnizca yetenekli ogrenciler icin degil, tum ogrenciler "
        "icin onemlidir. Muzik dersleri matematiksel dusunmeyi gelistirir, drama dersleri "
        "empati ve iletisim becerileri kazandirir, gorsel sanatlar gorselpmekansal zekaayi "
        "arttirir. STEAM (Science, Technology, Engineering, Arts, Mathematics) yaklaasimi, "
        "sanati STEM egitiminin ayrilmaz bir parcasi olarak gorur.", s["Body"]))
    story.append(Paragraph(
        "Dijital sanat da gunumuzde hizla gelisen bir alandir. Grafik tasarim, dijital "
        "illustrasyon, animasyon, video produksiyon ve muzik produksiyon gibi alanlar "
        "hem yaratici ifade hem de kariyer firsatlari sunmaktadir. Bu alanlarda "
        "yeteneklerini gelistiren gencler, dijital ekonominin en aranan profesyonelleri "
        "arasinda yer almaktadir.", s["Body"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 26: SPOR
    # -----------------------------------------------------------------------
    spor = data.get("spor", {})
    story.append(SectionHeaderBar("SPOR KOSESI", SECTION_COLORS["spor"], icon=""))
    _add_section_image("spor", width=14*cm, height=8*cm)
    story.append(Spacer(1, 8))
    story.append(Paragraph(spor.get("baslik", ""), s["ArticleTitle"]))
    story.append(Spacer(1, 4))

    for para_text in spor.get("icerik", "").split("\n\n"):
        para_text = para_text.strip()
        if para_text:
            story.append(Paragraph(para_text, s["Body"]))

    # Ayin sporcusu
    asp = spor.get("ayin_sporcusu", {})
    if asp:
        story.append(Spacer(1, 8))
        story.append(_make_info_box(
            f'Ayin Sporcusu: {asp.get("ad", "")} ({asp.get("dal", "")})',
            [asp.get("bilgi", "")],
            accent_color=SECTION_COLORS["spor"],
            bg="#fef2f2"
        ))

    # Saglik ipucu
    si2 = spor.get("saglik_ipucu", "")
    if si2:
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<b>Saglik Ipucu:</b> {si2}", s["Body"]))

    # Spor tarihi
    st2 = spor.get("spor_tarihi", "")
    if st2:
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>SPOR TARIHINDEN</b>", s["SubTitle"]))
        story.append(Paragraph(st2, s["BodySmall"]))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # OZLU SOZLER
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("OZLU SOZLER", SECTION_COLORS["sozler"], icon=""))
    story.append(Spacer(1, 10))

    sozler = data.get("ozlu_sozler", [])
    for i, item in enumerate(sozler):
        bg_hex = "#fef3c7" if i % 2 == 0 else "#f0f4ff"
        cat_color = "#854d0e" if item.get("kategori") in ("Bilim", "Felsefe") else "#1e3a5f"
        quote_box_paras = [
            Paragraph(f'<i>"{item["soz"]}"</i>', s["Quote"]),
            Paragraph(
                f'<font color="{cat_color}"><b>-- {item["kisi"]}</b></font>'
                f'  <font color="#999999" size="8">[{item.get("kategori", "")}]</font>',
                s["QuoteAuthor"]
            ),
        ]
        story.append(InfoBox(quote_box_paras, bg_color=HexColor(bg_hex), accent_color=GOLD, padding=6))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # HOBI KOSESI
    # -----------------------------------------------------------------------
    story.append(PageBreak())
    story.append(SectionHeaderBar("HOBI KOSESI", HexColor("#8b5cf6"), icon=""))
    _add_section_image("hobi", width=14*cm, height=8*cm)
    hobi = data.get("hobi_kosesi", {})
    story.append(Paragraph(hobi.get("baslik", "Hobi Kosesi"), s["SectionTitle"]))
    for h in hobi.get("hobiler", []):
        story.append(Paragraph(f'{h["emoji"]} <b>{h["ad"]}</b>', s["ArticleTitle"]))
        story.append(Paragraph(h["aciklama"], s["Body"]))
        story.append(Spacer(1, 4))
    if hobi.get("ipucu"):
        story.append(_make_info_box("Ipucu", [hobi["ipucu"]], accent_color=HexColor("#8b5cf6"), bg="#f5f3ff"))

    # -----------------------------------------------------------------------
    # ILGINC BILGILER
    # -----------------------------------------------------------------------
    story.append(CondPageBreak(350))
    story.append(SectionHeaderBar("ILGINC BILGILER", HexColor("#06b6d4"), icon=""))
    ilginc = data.get("ilginc_bilgiler", [])
    story.append(Paragraph("Bunlari Biliyor muydunuz?", s["SectionTitle"]))
    for idx, bilgi in enumerate(ilginc):
        story.append(Paragraph(f"<b>{idx+1}.</b> {bilgi}", s["Body"]))

    # -----------------------------------------------------------------------
    # EGLENCE KOSESI
    # -----------------------------------------------------------------------
    story.append(CondPageBreak(350))
    story.append(SectionHeaderBar("EGLENCE KOSESI", HexColor("#f59e0b"), icon=""))
    eglence = data.get("eglence_kosesi", {})
    story.append(Paragraph("Gulelim Eglenelim", s["SectionTitle"]))
    for fikra in eglence.get("fikralar", []):
        story.append(PullQuote(fikra, ""))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Mini Bilgi Yarismasi</b>", s["ArticleTitle"]))
    for by_item in eglence.get("bilgi_yarismasi", []):
        story.append(Paragraph(f"Soru: {by_item['soru']}", s["Body"]))
        story.append(Paragraph(f"<i>Cevap: {by_item['cevap']}</i>", s["SmallGray"]))
        story.append(Spacer(1, 4))

    # -----------------------------------------------------------------------
    # FELSEFE KOSESI
    # -----------------------------------------------------------------------
    story.append(PageBreak())
    story.append(SectionHeaderBar("FELSEFE KOSESI", HexColor("#6366f1"), icon=""))
    _add_section_image("felsefe", width=14*cm, height=8*cm)
    felsefe = data.get("felsefe_kosesi", {})
    story.append(Paragraph(felsefe.get("baslik", ""), s["SectionTitle"]))
    fil = felsefe.get("filozof", {})
    if fil:
        story.append(Paragraph(f'<b>{fil["ad"]}</b> ({fil["donem"]}) - {fil["ulke"]}', s["ArticleTitle"]))
        story.append(Paragraph(fil.get("biyografi", ""), s["Body"]))
        story.append(_make_info_box("Temel Fikir", [fil.get("temel_fikir", "")], accent_color=HexColor("#6366f1"), bg="#eef2ff"))
    ds = felsefe.get("dusunce_sorusu", "")
    if ds:
        story.append(PullQuote(ds, "Dusunce Sorusu"))
    for soz in felsefe.get("sozler", []):
        story.append(Paragraph(f"<i>{soz}</i>", s["Quote"]))

    # -----------------------------------------------------------------------
    # MUZIK KOSESI
    # -----------------------------------------------------------------------
    story.append(CondPageBreak(350))
    story.append(SectionHeaderBar("MUZIK KOSESI", HexColor("#ec4899"), icon=""))
    _add_section_image("muzik", width=14*cm, height=8*cm)
    muzik = data.get("muzik_kosesi", {})
    story.append(Paragraph(muzik.get("baslik", ""), s["SectionTitle"]))
    ms_sanatci = muzik.get("sanatci", {})
    if ms_sanatci:
        story.append(Paragraph(f'<b>{ms_sanatci["ad"]}</b> ({ms_sanatci["donem"]}) - {ms_sanatci["ulke"]}', s["ArticleTitle"]))
        story.append(Paragraph(ms_sanatci.get("bilgi", ""), s["Body"]))
    mt = muzik.get("tur_tanitimi", {})
    if mt:
        story.append(Paragraph(f'<b>{mt["ad"]}</b>', s["ArticleTitle"]))
        story.append(Paragraph(mt.get("aciklama", ""), s["Body"]))
    do_onerisi = muzik.get("dinleme_onerisi", "")
    if do_onerisi:
        story.append(_make_info_box("Bu Ay Dinleyin", [do_onerisi], accent_color=HexColor("#ec4899"), bg="#fdf2f8"))

    # -----------------------------------------------------------------------
    # MEGA KELIME BULMACASI (50 Kelime)
    # -----------------------------------------------------------------------
    story.append(PageBreak())
    story.append(SectionHeaderBar("MEGA KELIME BULMACASI", HexColor("#059669"), icon=""))
    kb50 = data.get("kelime_bulmacasi_50", {})
    story.append(Paragraph(kb50.get("baslik", "50 Kelime Bulmacasi"), s["SectionTitle"]))
    words = kb50.get("kelimeler", [])
    # Show words in 5-column table
    word_rows = []
    for i in range(0, len(words), 5):
        word_rows.append(words[i:i+5])
    if word_rows:
        # Pad last row
        while len(word_rows[-1]) < 5:
            word_rows[-1].append("")
        _content_w = PAGE_W - 4 * cm
        wt = Table(word_rows, colWidths=[_content_w/5]*5)
        wt.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('TEXTCOLOR', (0,0), (-1,-1), HexColor('#059669')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor('#d1d5db')),
            ('BACKGROUND', (0,0), (-1,-1), HexColor('#f0fdf4')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(wt)
    if kb50.get("ipucu"):
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<i>{kb50['ipucu']}</i>", s["SmallGray"]))

    # -----------------------------------------------------------------------
    # ZEKA SORULARI
    # -----------------------------------------------------------------------
    story.append(CondPageBreak(350))
    story.append(SectionHeaderBar("ZEKA SORULARI", HexColor("#7c3aed"), icon=""))
    zeka = data.get("zeka_sorulari", [])
    story.append(Paragraph("Beyninizi Zorlayan Sorular", s["SectionTitle"]))
    for idx, zs in enumerate(zeka):
        story.append(Paragraph(f"<b>Soru {idx+1}:</b> {zs['soru']}", s["Body"]))
        story.append(Paragraph(f"<i>Cevap: {zs['cevap']}</i>", s["SmallGray"]))
        story.append(GoldLine())

    # -----------------------------------------------------------------------
    # BILMECELER & BULMACALAR
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("BILMECELER & BULMACALAR", SECTION_COLORS["bilmece"], icon=""))
    story.append(Spacer(1, 8))

    # Bilmeceler
    story.append(Paragraph("<b>BILMECELER</b>", s["SubTitle"]))
    for i, (bilmece, _) in enumerate(data.get("bilmeceler", []), 1):
        story.append(Paragraph(f'<font color="#4f46e5"><b>{i}.</b></font> {bilmece}', s["Body"]))

    # Mantik sorulari
    ms2 = data.get("mantik_sorulari", [])
    if ms2:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>MANTIK SORULARI</b>", s["SubTitle"]))
        for i, (soru, _) in enumerate(ms2, 1):
            story.append(Paragraph(f'<font color="#7c3aed"><b>{i}.</b></font> {soru}', s["Body"]))

    # Matematik bulmacalari
    mb = data.get("matematik_bulmacalari", [])
    if mb:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>MATEMATIK BULMACALARI</b>", s["SubTitle"]))
        for i, bulmaca in enumerate(mb, 1):
            story.append(Paragraph(f'<font color="#0d9488"><b>{i}.</b></font> {bulmaca}', s["Body"]))

    # Kim bu?
    kb = data.get("kim_bu", {})
    if kb:
        story.append(Spacer(1, 8))
        ipuclari_text = kb.get("ipuclari", [])
        story.append(_make_info_box(
            "KIM BU? (Ipuclari)",
            ipuclari_text,
            accent_color=HexColor("#7c3aed"),
            bg="#f5f3ff"
        ))

    story.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # SAYFA 29: QUIZ
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("AYLIK QUIZ - 15 SORU", SECTION_COLORS["quiz"], icon=""))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f'<i>Puanlama: {data.get("quiz_puan_rehberi", "")}</i>',
        s["SmallGray"]
    ))
    story.append(Spacer(1, 6))

    for i, q in enumerate(data.get("quiz", []), 1):
        zorluk_str = "*" * q.get("zorluk", 1)
        story.append(Paragraph(
            f'<font color="#0d1b2a"><b>{i}.</b></font> {q["soru"]} '
            f'<font color="#c9a84c" size="8">{zorluk_str}</font>',
            s["QuizQ"]
        ))
        for opt in q.get("secenekler", []):
            story.append(Paragraph(opt, s["QuizOpt"]))
        story.append(Spacer(1, 2))

    # -----------------------------------------------------------------------
    # EK BOLUMLER: Sayfa doldurucu zengin icerik
    # -----------------------------------------------------------------------
    story.append(PageBreak())
    story.append(SectionHeaderBar("SANAT GALERISI", HexColor("#be185d"), icon=""))
    _add_section_image("sanat_galeri", width=14*cm, height=9*cm)
    story.append(Paragraph("Sanat, insanin ic dunyasini ve toplumsal gercekliklerini yansitan en guclu ifade bicimidir. "
        "Tarih boyunca resim, heykel, muzik, edebiyat ve tiyatro gibi sanat dallari, medeniyetlerin "
        "kulturel zenginligini ortaya koymustur. Ronesans'tan Empresyonizme, Kubizm'den Surrealizme "
        "kadar her sanat akimi, doneminin ruhunu ve dusunce yapisini yansitmistir.", s["Body"]))
    story.append(Paragraph("Bu ay sizin icin sectiklerimiz:", s["ArticleTitle"]))
    sanat_eserler = [
        ("Yildizli Gece - Vincent van Gogh (1889)", "Post-empresyonizmin basyapiti. Gece gokyuzunun burgacli, ritmik "
         "tasvirini iceren bu tablo, sanatcinin Saint-Remy'deki akil hastanesinde kaldigi donemde yapilmistir."),
        ("Son Akssam Yemegi - Leonardo da Vinci (1498)", "Ronesans'in en ikonik eserlerinden biri. Milano'daki Santa Maria "
         "delle Grazie kilisesinin duvarinda bulunan bu fresk, perspektif kullaniminin en ustaca orneglerinden biridir."),
        ("Guernica - Pablo Picasso (1937)", "Ispanya Ic Savasi sirasinda Guernica kasabasinin bombalanmasini konu alan "
         "bu dev boyutlu tablo, savasin dehsetini ve insanligin acisini evrensel bir dille anlatir."),
    ]
    for baslik, aciklama in sanat_eserler:
        story.append(Paragraph(f"<b>{baslik}</b>", s["ArticleTitle"]))
        story.append(Paragraph(aciklama, s["Body"]))

    story.append(PageBreak())
    story.append(SectionHeaderBar("SAGLIK & BESLENME", HexColor("#059669"), icon=""))
    story.append(Paragraph("Saglikli Yasam Rehberi", s["SectionTitle"]))
    story.append(Paragraph(
        "Saglikli beslenme, bedensel ve zihinsel performansin temelidir. Ozellikle ogrenciler icin "
        "dengeli beslenme, akademik basariyi dogrudan etkileyen bir faktordur. Beyin, vucut agirliginin "
        "sadece yuzde ikisini olustururken, toplam enerjinin yuzde yirmisini tuketir. Bu nedenle "
        "beynin ihtiyac duydugu besinleri yeterli miktarda almak buyuk onem tasir.", s["Body"]))
    beslenme_onerileri = [
        "Kahvalti mutlaka yapilmali — kahvalti atlayan ogrencilerde dikkat ve hafiza performansi duser.",
        "Omega-3 yag asitleri (balik, ceviz, keten tohumu) beyin fonksiyonlarini destekler.",
        "Gunluk en az 2 litre su icilmeli — dehidrasyon konsantrasyonu yuzde otuz azaltir.",
        "Tam tahillar ve lifli gidalar kan sekerini dengede tutar, enerji seviyesini sabit killar.",
        "Demir eksikligi dikkat dagilkligina yol acar — ispanak, mercimek, kirmizi et tuketin.",
        "Asiri seker ve islenmis gidalardan kacinin — ani enerji dususlerine neden olurlar.",
        "B grubu vitaminleri sinir sistemi icin kritiktir — yumurta, sut urunleri, yesil yapraklilar.",
        "Probiyotik gidalar (yogurt, kefir) bagirsak sagligini ve dolayisiyla bag isiklik sistemini guclendirir.",
    ]
    for idx, oneri in enumerate(beslenme_onerileri):
        story.append(Paragraph(f"<b>{idx+1}.</b> {oneri}", s["Body"]))
    story.append(_make_info_box("Gunun Tarifi", [
        "Beyin Dostu Smoothie: 1 muz + 1 avuc yaban mersini + 1 kasik ceviz + 1 bardak sut + 1 tatli kasigi bal. Blender'da karistirin. Antioksidan, omega-3 ve potasyum deposu bu icecek, sinav oncesi idealdir!"
    ], accent_color=HexColor("#059669"), bg="#f0fdf4"))

    story.append(PageBreak())
    story.append(SectionHeaderBar("DUNYA'DAN HABERLER", HexColor("#0284c7"), icon=""))
    story.append(Paragraph("Bu Ay Dunyada Neler Oldu?", s["SectionTitle"]))
    haberler = [
        ("Bilim", "Arastirmacilar, gunes enerjisini yuzde kirk verimlilikle elektrige ceviren yeni bir gunes hucresii gelistirdi. "
         "Bu buluus, mevcut ticari panellerin verimlIligini neredeyse ikiye katlayarak yenilenebilir enerji sektorunde devrim yaratabilir."),
        ("Teknoloji", "Kuantum bilgisayar alaninda yeni bir donum noktasi: 1000 kubitlik islemci basariyla test edildi. "
         "Bu gelisme, ilac kesfinden kriptografiye kadar pek cok alanda buyuk ilerlemelerin onunu acabilir."),
        ("Cevre", "Birkac ulke, okyanuslarIn yuzde otuzunu koruma altina almayi hedefleyen uluslararasi antlasmayi imzaladi. "
         "Bu antlasma, deniz biyocesitliliginin korunmasi icin atilmis en buyuk adim olarak degerlendiriliyor."),
        ("Egitim", "UNESCO raporuna gore, dijital okuryazarlik artik temel insan haklari arasinda sayilmalidir. "
         "Rapor, tum ulkelerin egitim mufredatlarIna dijital yetkinlik derslerini dahil etmesini onermektedir."),
        ("Saglik", "Yeni nesil mRNA asilari, kanser tedavisinde umut verici sonuclar gostermeye devam ediyor. "
         "Klinik denemelerde, kisisellestirilmis kanser asilariinin bagiisiklik sistemini tumore karsi harekete gecirdigi gozlendi."),
    ]
    for kategori, haber in haberler:
        story.append(Paragraph(f"<b>[{kategori}]</b> {haber}", s["Body"]))
        story.append(GoldLine())

    story.append(PageBreak())
    story.append(SectionHeaderBar("MESLEKLER DUNYASI", HexColor("#7c3aed"), icon=""))
    story.append(Paragraph("Gelecekte Parlayacak Meslekler", s["SectionTitle"]))
    story.append(Paragraph(
        "Teknolojik gelismeler ve toplumsal donusumler, meslek dunyasini hizla degistirmektedir. "
        "Bazi meslekler yok olurken, yepyeni alanlar ortaya cikmaktadir. Isste gelecekte en cok "
        "talep gorecek mesleklerden bazilari:", s["Body"]))
    meslekler = [
        ("Veri Bilimci", "Buyuk veriyi analiz ederek isletmelere stratejik kararlar almalarinda yardimci olur. "
         "Istatistik, programlama ve is zekasi becerilerini birlestirir."),
        ("Yapay Zeka Muhendisi", "Makine ogrenmesi algoritmalari ve sinir aglari gelistirir. "
         "Otonom sistemlerden dogal dil islemesine kadar genis bir alanda calisir."),
        ("Siber Guvenlik Uzmani", "Dijital sistemleri saldirilardan korur, guvenlik acIklarini tespit eder. "
         "Artan dijitallesmeyle birlikte en kritik mesleklerden biri haline gelmistir."),
        ("Biyomedikal Muhendis", "Tip ve muhendisligi birlestirerek yapay organlar, protezler ve tibbi cihazlar gelistirir."),
        ("Surdurulebilirlik Danismani", "Sirketlerin ve kurumlarin cevre dostu uygulamalar benimsemelerine yardimci olur."),
    ]
    for meslek, aciklama in meslekler:
        story.append(Paragraph(f"<b>{meslek}</b>", s["ArticleTitle"]))
        story.append(Paragraph(aciklama, s["Body"]))

    # -----------------------------------------------------------------------
    # INGILIZCE DIL EGITIMI KOSESI
    # -----------------------------------------------------------------------
    story.append(PageBreak())
    story.append(SectionHeaderBar("INGILIZCE OGRENIYORUM", HexColor("#2563eb"), icon=""))
    _add_section_image("ingilizce", width=14*cm, height=7*cm)
    story.append(Paragraph("Bu Ayin Kelimeleri (A1-A2)", s["SectionTitle"]))

    en_kelimeler = [
        ("Education", "Egitim", "The education system is changing."),
        ("Knowledge", "Bilgi", "Knowledge is power."),
        ("Discover", "Kesfetmek", "Scientists discover new things every day."),
        ("Environment", "Cevre", "We must protect the environment."),
        ("Technology", "Teknoloji", "Technology makes life easier."),
        ("Achievement", "Basari", "Hard work leads to achievement."),
        ("Community", "Topluluk", "We are part of a global community."),
        ("Creativity", "Yaraticilik", "Creativity is the key to innovation."),
        ("Responsibility", "Sorumluluk", "Taking responsibility is important."),
        ("Opportunity", "Firsat", "Every challenge is an opportunity."),
        ("Experience", "Deneyim", "Experience is the best teacher."),
        ("Challenge", "Meydan Okuma", "Accept the challenge and grow."),
    ]
    en_data = []
    for en, tr, ornek in en_kelimeler:
        en_data.append([en, tr, ornek])
    en_table = Table(
        [["English", "Turkce", "Ornek Cumle"]] + en_data,
        colWidths=[4*cm, 4*cm, 8.5*cm]
    )
    en_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#2563eb')),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#eff6ff')),
        ('TEXTCOLOR', (0,1), (-1,-1), HexColor('#1e3a5f')),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#93c5fd')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(en_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Gunluk Konusma Kaliplari", s["ArticleTitle"]))
    en_cumleler = [
        ("How are you doing today?", "Bugun nasilsin?"),
        ("I would like to ask a question.", "Bir soru sormak istiyorum."),
        ("Could you please help me?", "Bana yardim edebilir misiniz?"),
        ("What do you think about this?", "Bu konuda ne dusunuyorsunuz?"),
        ("I completely agree with you.", "Size tamamen katiliyorum."),
        ("Let me explain my point of view.", "Bakis acimi aciklamama izin verin."),
        ("That sounds like a great idea!", "Harika bir fikir gibi gorunuyor!"),
        ("I am looking forward to seeing you.", "Sizi gormek icin sabirsizlaniyorum."),
    ]
    for en, tr in en_cumleler:
        story.append(Paragraph(f'<b>"{en}"</b> — <i>{tr}</i>', s["Body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Gramer Notu:</b> Present Perfect Tense (Yakin Gecmis Zaman)", s["ArticleTitle"]))
    story.append(Paragraph(
        "Present Perfect, gecmiste baslayip simdiye kadar devam eden veya etkisi suregelen eylemleri ifade eder. "
        "Yapisi: Subject + have/has + past participle (V3). "
        "Ornek: 'I have visited Istanbul three times.' (Istanbul'u uc kez ziyaret ettim.) "
        "'She has just finished her homework.' (Odevini henuz bitirdi.) "
        "'We have known each other since childhood.' (Cocukluktan beri birbirimizi taniyoruz.)", s["Body"]))

    # -----------------------------------------------------------------------
    # ALMANCA DIL EGITIMI KOSESI
    # -----------------------------------------------------------------------
    story.append(PageBreak())
    story.append(SectionHeaderBar("ALMANCA OGRENIYORUM", HexColor("#16a34a"), icon=""))
    _add_section_image("almanca", width=14*cm, height=7*cm)
    story.append(Paragraph("Bu Ayin Kelimeleri (A1-A2)", s["SectionTitle"]))

    de_kelimeler = [
        ("die Bildung", "Egitim", "Bildung ist sehr wichtig."),
        ("das Wissen", "Bilgi", "Wissen ist Macht."),
        ("entdecken", "Kesfetmek", "Kinder entdecken die Welt."),
        ("die Umwelt", "Cevre", "Wir schuetzen die Umwelt."),
        ("die Technik", "Teknoloji", "Die Technik veraendert unser Leben."),
        ("der Erfolg", "Basari", "Erfolg braucht harte Arbeit."),
        ("die Gemeinschaft", "Topluluk", "Wir sind eine Gemeinschaft."),
        ("die Kreativitaet", "Yaraticilik", "Kreativitaet ist wichtig."),
        ("die Verantwortung", "Sorumluluk", "Jeder hat Verantwortung."),
        ("die Gelegenheit", "Firsat", "Das ist eine grosse Gelegenheit."),
        ("die Erfahrung", "Deneyim", "Erfahrung ist der beste Lehrer."),
        ("die Herausforderung", "Meydan Okuma", "Das ist eine Herausforderung."),
    ]
    de_data = []
    for de, tr, ornek in de_kelimeler:
        de_data.append([de, tr, ornek])
    de_table = Table(
        [["Deutsch", "Turkce", "Beispielsatz (Ornek)"]] + de_data,
        colWidths=[4*cm, 4*cm, 8.5*cm]
    )
    de_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#16a34a')),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f0fdf4')),
        ('TEXTCOLOR', (0,1), (-1,-1), HexColor('#14532d')),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#86efac')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(de_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Gunluk Konusma Kaliplari", s["ArticleTitle"]))
    de_cumleler = [
        ("Wie geht es Ihnen heute?", "Bugun nasilsiniz?"),
        ("Ich moechte eine Frage stellen.", "Bir soru sormak istiyorum."),
        ("Koennten Sie mir bitte helfen?", "Bana yardim edebilir misiniz?"),
        ("Was denken Sie darueber?", "Bu konuda ne dusunuyorsunuz?"),
        ("Ich bin voellig einverstanden.", "Tamamen katiliyorum."),
        ("Das klingt nach einer tollen Idee!", "Harika bir fikir gibi!"),
        ("Ich freue mich auf unser Treffen.", "Bulusmamizi dort gozle bekliyorum."),
        ("Entschuldigung, wo ist der Bahnhof?", "Pardon, istasyon nerede?"),
    ]
    for de, tr in de_cumleler:
        story.append(Paragraph(f'<b>"{de}"</b> — <i>{tr}</i>', s["Body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Gramer Notu:</b> Artikeller (der, die, das)", s["ArticleTitle"]))
    story.append(Paragraph(
        "Almanca'da her ismin bir cinsiyeti vardir ve bu cinsiyet artikelle belirlenir: "
        "der (eril), die (disil), das (notr). Ornegin: der Tisch (masa), die Lampe (lamba), "
        "das Buch (kitap). Cogul halde hepsi 'die' olur: die Tische, die Lampen, die Buecher. "
        "Artikelleri ezberlemek Almanca ogrenmenin en onemli asamalarindan biridir. "
        "Her yeni kelimeyi artikeliyle birlikte ogrenin!", s["Body"]))

    story.append(PageBreak())

    # -----------------------------------------------------------------------
    # ARKA KAPAK - CEVAPLAR + SONRAKI SAYI
    # -----------------------------------------------------------------------
    story.append(SectionHeaderBar("CEVAPLAR & GELECEK SAYI", NAVY, icon=""))
    story.append(Spacer(1, 8))

    # Quiz cevaplari
    story.append(Paragraph("<b>QUIZ CEVAPLARI</b>", s["SubTitle"]))
    quiz_cevap_text = ", ".join([
        f"{i+1}-{q['cevap']}" for i, q in enumerate(data.get("quiz", []))
    ])
    story.append(Paragraph(quiz_cevap_text, s["Body"]))
    story.append(Spacer(1, 6))

    # Bilmece cevaplari
    story.append(Paragraph("<b>BILMECE CEVAPLARI</b>", s["SubTitle"]))
    bilmece_cevap_text = " | ".join([
        f"{i+1}. {c}" for i, (_, c) in enumerate(data.get("bilmeceler", []))
    ])
    story.append(Paragraph(bilmece_cevap_text, s["BodySmall"]))
    story.append(Spacer(1, 4))

    # Mantik cevaplari
    ms3 = data.get("mantik_sorulari", [])
    if ms3:
        story.append(Paragraph("<b>MANTIK CEVAPLARI</b>", s["SubTitle"]))
        for i, (_, cevap) in enumerate(ms3, 1):
            story.append(Paragraph(f"<b>{i}.</b> {cevap}", s["BodySmall"]))
        story.append(Spacer(1, 4))

    # Matematik cevaplari
    mc = data.get("matematik_cevaplar", [])
    if mc:
        story.append(Paragraph("<b>MATEMATIK CEVAPLARI</b>", s["SubTitle"]))
        story.append(Paragraph(", ".join([f"{i+1}. {c}" for i, c in enumerate(mc)]), s["BodySmall"]))
        story.append(Spacer(1, 4))

    # Kim bu cevap
    kb2 = data.get("kim_bu", {})
    if kb2:
        story.append(Paragraph(f'<b>Kim Bu? Cevap:</b> {kb2.get("cevap", "")}', s["Body"]))
        story.append(Spacer(1, 8))

    # Okuyucu mektuplari
    om = data.get("okuyucu_mektuplari", [])
    if om:
        story.append(GoldLine())
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>OKUYUCU MEKTUPLARI</b>", s["SubTitle"]))
        for m in om:
            story.append(Paragraph(
                f'<font color="#2563eb"><b>{m["ad"]}:</b></font> <i>"{m["mesaj"]}"</i>',
                s["BodySmall"]
            ))

    # Sonraki sayi
    ss = data.get("sonraki_sayi", {})
    if ss:
        story.append(Spacer(1, 10))
        story.append(GoldLine())
        story.append(Spacer(1, 8))
        story.append(Paragraph(f'<b>GELECEK SAYI TEMASI: {ss.get("tema", "")}</b>', s["ArticleTitle"]))
        for teaser in ss.get("teasers", []):
            story.append(Paragraph(f"<bullet>&bull;</bullet> {teaser}", s["BulletItem"]))

    # Branding
    story.append(Spacer(1, 15))
    story.append(GoldLine())
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Smarti Dergi</b> | Aylik Egitim ve Kultur Dergisi",
        s["Centered"]
    ))
    story.append(Paragraph(
        "smartcampus.edu.tr | Her ay 30 sayfa bilgi, ilham ve eglence",
        s["SmallGray"]
    ))
    if os.path.exists(MASCOT_PATH):
        try:
            story.append(Spacer(1, 6))
            mascot_final = RLImage(MASCOT_PATH, width=2 * cm, height=2 * cm)
            mascot_final.hAlign = "CENTER"
            story.append(mascot_final)
        except Exception:
            pass

    return story


# ===========================================================================
# PDF URETIM ANA FONKSIYONU
# ===========================================================================
def generate_magazine_pdf(sayi_no, images=None):
    """Verilen sayi numarasi icin profesyonel 30 sayfalik dergi PDF'i uretir.
    images: dict of {section: image_path} — AI gorsellerini ekler.
    """
    data = DERGI_DATA.get(sayi_no)
    if not data:
        return None

    buf = BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title=f"Smarti Dergi - Sayi {sayi_no}",
        author="SmartCampus Egitim Platformu",
    )

    # Data ve gorselleri doc objesine ekle (callback'ler icin)
    doc._dergi_data = data
    doc._dergi_images = images or {}

    story = _build_story(data, images or {})

    doc.build(
        story,
        onFirstPage=_draw_cover_page,
        onLaterPages=_draw_later_pages,
    )

    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes


# ===========================================================================
# STREAMLIT UI
# ===========================================================================
def render_dergi_pdf_viewer():
    """Streamlit arayuzu: Dergi PDF onizleme ve indirme."""

    st.markdown("""
    <style>
    .dergi-header {
        background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 50%, #2563eb 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .dergi-header h1 { color: #d4a017; font-size: 28px; margin: 0; }
    .dergi-header p { color: #94a3b8; font-size: 13px; margin: 5px 0 0 0; }
    .dergi-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid rgba(212,160,23,0.25);
        border-radius: 10px;
        padding: 18px;
        margin: 10px 0;
        color: #e2e8f0;
    }
    .dergi-card h3 { color: #d4a017; }
    .dergi-card p { color: #94a3b8; }
    .dergi-card strong { color: #d4a017; }
    .dergi-stat {
        background: linear-gradient(135deg, #1e3a5f, #2563eb);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    .dergi-stat h2 { font-size: 28px; margin: 0; color: #d4a017; }
    .dergi-stat p { font-size: 11px; margin: 3px 0 0 0; color: #94a3b8; }
    .dergi-section-badge {
        display: inline-block;
        background: #1e3a5f;
        color: #d4a017;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        margin: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dergi-header">
        <h1>Smarti Dergi</h1>
        <p>Aylik Egitim ve Kultur Dergisi | 30 Sayfa | 20+ Bolum</p>
    </div>
    """, unsafe_allow_html=True)

    # Istatistikler
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="dergi-stat"><h2>12</h2><p>Sayi</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dergi-stat"><h2>30</h2><p>Sayfa/Sayi</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="dergi-stat"><h2>20+</h2><p>Bolum</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="dergi-stat"><h2>180</h2><p>Quiz Soru</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Sayi secici
    sayi_options = {
        v["sayi"]: f'Sayi {v["sayi"]} - {v["ay"]} ({v["tema"]})'
        for v in DERGI_DATA.values()
    }
    selected_sayi = st.selectbox(
        "Sayi Secin:",
        options=list(sayi_options.keys()),
        format_func=lambda x: sayi_options[x],
    )

    data = DERGI_DATA.get(selected_sayi, {})

    if data:
        st.markdown(f"""
        <div class="dergi-card">
            <h3>Sayi {data['sayi']} | {data['ay']}</h3>
            <p><strong>Tema:</strong> {data['tema']}</p>
            <p style="margin-top:8px;">{data['editorial'][:300]}...</p>
        </div>
        """, unsafe_allow_html=True)

        # Bolumler badge
        sections = [
            "Editorden", "Bilim & Teknik", "Teknoloji", "Tarih",
            "Cografya & Gezi", "Doga & Cevre", "Edebiyat", "Siir",
            "Psikoloji", "Veli Kosesi", "Ogrenci Tavsiyeleri",
            "Kultur & Sanat", "Spor", "Ozlu Sozler",
            "Bilmeceler", "Bulmacalar", "Quiz", "Cevaplar",
        ]
        badges_html = " ".join([f'<span class="dergi-section-badge">{sec}</span>' for sec in sections])
        st.markdown(f"<div style='margin: 10px 0;'>{badges_html}</div>", unsafe_allow_html=True)

        # Icerik on izleme
        with st.expander("Icerige Goz At", expanded=False):
            st.markdown("#### Bilim & Teknik")
            for art in data.get("bilim_teknik", []):
                st.markdown(f"**{art['baslik']}**")
                st.caption(art["icerik"][:200] + "...")

            tc = data.get("tarih", {})
            if tc:
                st.markdown(f"#### Tarih: {tc.get('baslik', '')}")

            ed_data = data.get("edebiyat", {})
            if ed_data:
                st.markdown(f"#### Edebiyat: {ed_data.get('kitap', '')} - {ed_data.get('yazar', '')}")

            gezi_data = data.get("cografya_gezi", {})
            if gezi_data:
                st.markdown(f"#### Gezi: {gezi_data.get('yer', '')} ({gezi_data.get('ulke', '')})")

            st.markdown("#### Siirler")
            for poem in data.get("siir", []):
                st.markdown(f"*{poem.get('baslik', '')}* - {poem.get('sair', '')}")

            st.markdown(f"#### Quiz: {len(data.get('quiz', []))} soru")

        st.markdown("---")

        # Gorseller
        _img_cache_key = f"_dergi_imgs_{selected_sayi}"
        dergi_images = st.session_state.get(_img_cache_key, {})

        col_img, col_pdf, col_dl = st.columns([1, 1, 1])

        with col_img:
            existing_count = sum(1 for k in ["kapak","bilim","teknoloji","tarih","gezi","doga","edebiyat","spor","kultur","psikoloji"]
                                 if os.path.exists(os.path.join(DERGI_IMG_DIR, f"sayi{selected_sayi}_{k}.png")))
            if existing_count > 0:
                st.success(f"{existing_count}/10 gorsel hazir")
            if st.button("AI Gorsel Uret (DALL-E 3)", use_container_width=True):
                progress_bar = st.progress(0)
                status = st.empty()
                status.info("AI gorselleri uretiliyor... (10 gorsel)")
                dergi_images = generate_dergi_images(
                    selected_sayi,
                    progress_callback=lambda p: progress_bar.progress(p)
                )
                st.session_state[_img_cache_key] = dergi_images
                progress_bar.progress(1.0)
                status.success(f"{len(dergi_images)} gorsel uretildi!")

        # Mevcut cache'li gorselleri yukle
        if not dergi_images:
            for k in ["kapak","bilim","teknoloji","tarih","gezi","doga","edebiyat","spor","kultur","psikoloji"]:
                p = os.path.join(DERGI_IMG_DIR, f"sayi{selected_sayi}_{k}.png")
                if os.path.exists(p):
                    dergi_images[k] = p

        # PDF olustur ve indir
        with col_pdf:
            if st.button("PDF Olustur", type="primary", use_container_width=True):
                img_note = f" ({len(dergi_images)} gorsel ile)" if dergi_images else " (gorselsiz)"
                with st.spinner(f"30 sayfalik PDF olusturuluyor{img_note}..."):
                    try:
                        pdf_bytes = generate_magazine_pdf(selected_sayi, images=dergi_images)
                        if pdf_bytes:
                            st.session_state["_dergi_pdf_bytes"] = pdf_bytes
                            st.session_state["_dergi_pdf_sayi"] = selected_sayi
                            st.success(f"Sayi {selected_sayi} - PDF basariyla olusturuldu!")
                        else:
                            st.error("PDF olusturulamadi.")
                    except Exception as e:
                        st.error(f"PDF olusturma hatasi: {str(e)}")

        # Indirme butonu
        if st.session_state.get("_dergi_pdf_bytes") and st.session_state.get("_dergi_pdf_sayi") == selected_sayi:
            with col_dl:
                st.download_button(
                    label="PDF Indir",
                    data=st.session_state["_dergi_pdf_bytes"],
                    file_name=f"Smarti_Dergi_Sayi{selected_sayi}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        # Toplu olusturma
        st.markdown("---")
        with st.expander("Toplu PDF Olusturma"):
            st.info("Tum sayilari tek seferde olusturabilirsiniz.")
            if st.button("Tum Sayilari Olustur (12 Sayi)"):
                progress = st.progress(0)
                for i, sayi in enumerate(DERGI_DATA.keys()):
                    try:
                        pdf_bytes = generate_magazine_pdf(sayi)
                        if pdf_bytes:
                            st.download_button(
                                label=f"Sayi {sayi} - {DERGI_DATA[sayi]['ay']}",
                                data=pdf_bytes,
                                file_name=f"Smarti_Dergi_Sayi{sayi}.pdf",
                                mime="application/pdf",
                                key=f"dergi_bulk_{sayi}",
                            )
                    except Exception as e:
                        st.warning(f"Sayi {sayi} olusturulamadi: {e}")
                    progress.progress((i + 1) / len(DERGI_DATA))
                st.success("Tum sayilar olusturuldu!")
