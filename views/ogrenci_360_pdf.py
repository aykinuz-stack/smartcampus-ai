"""
Öğrenci 360° — Ultra Premium PDF Rapor Generator v2
=====================================================
Gerçek okul raporu kalitesinde, tüm veriler detaylı.
Her alan süzgeçten geçirilir, hiçbir veri atlanmaz.
"""

from __future__ import annotations
import io
from datetime import date

from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

from utils.shared_data import ensure_turkish_pdf_fonts

# ── RENKLER ──
NAVY = HexColor("#0f2744")
GOLD = HexColor("#C8952E")
GOLD_LIGHT = HexColor("#F5E6C8")
WHITE = HexColor("#FFFFFF")
CREAM = HexColor("#FFFBF0")
LGRAY = HexColor("#F1F5F9")
MGRAY = HexColor("#94A3B8")
DGRAY = HexColor("#475569")
DARK = HexColor("#1E293B")
RED = HexColor("#EF4444")
ORANGE = HexColor("#F97316")
AMBER = HexColor("#F59E0B")
GREEN = HexColor("#22C55E")
BLUE = HexColor("#3B82F6")
PURPLE = HexColor("#8B5CF6")
TEAL = HexColor("#0D9488")
PINK = HexColor("#EC4899")

W, H = A4
ML = 1.5 * cm
MR = 1.5 * cm
MT = 1.8 * cm
UW = W - ML - MR
PAGE = [0]

RISK_CLR = {"LOW": GREEN, "MEDIUM": AMBER, "HIGH": ORANGE, "CRITICAL": RED, "UNKNOWN": MGRAY}
RISK_TR = {"LOW": "Dusuk", "MEDIUM": "Orta", "HIGH": "Yuksek", "CRITICAL": "Kritik", "UNKNOWN": "?"}


# ═══════════════════════════════════════════════════════════
# YARDIMCI CIZIM FONKSIYONLARI
# ═══════════════════════════════════════════════════════════

def _np(c, fn, fb, kurum="SmartCampus AI", title="Ogrenci 360 Raporu"):
    """Yeni sayfa + header/footer."""
    PAGE[0] += 1
    if PAGE[0] > 1:
        c.showPage()
    c.setFillColor(NAVY)
    c.rect(0, H - 36, W, 36, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 38, W, 2, fill=1, stroke=0)
    c.setFont(fb, 8)
    c.setFillColor(WHITE)
    c.drawString(ML, H - 26, kurum)
    c.drawRightString(W - MR, H - 26, title)
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 28, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 28, W, 1.5, fill=1, stroke=0)
    c.setFont(fn, 7)
    c.setFillColor(WHITE)
    c.drawString(ML, 10, f"Olusturma: {date.today().isoformat()}")
    c.drawRightString(W - MR, 10, f"Sayfa {PAGE[0]}")
    c.setFillColor(MGRAY)
    c.setFont(fn, 5.5)
    c.drawCentredString(W / 2, 10, "Bu rapor gizlidir - KVKK kapsaminda korunur")
    return H - MT - 38


def _yc(c, y, fn, fb, kurum):
    """y kontrolu — yer yoksa yeni sayfa."""
    if y < 70:
        return _np(c, fn, fb, kurum)
    return y


def _sec(c, y, title, color, fn, fb, kurum):
    """Bolum basligi."""
    y = _yc(c, y, fn, fb, kurum)
    c.setFillColor(color)
    c.roundRect(ML, y - 16, UW, 20, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(fb, 9.5)
    c.drawString(ML + 8, y - 12, title)
    return y - 26


def _lv(c, y, label, value, fn, fb, vclr=None, kurum=""):
    """Etiket-deger satiri."""
    if y < 50:
        y = _np(c, fn, fb, kurum)
    c.setFont(fn, 8)
    c.setFillColor(DARK)
    c.drawString(ML + 8, y, label)
    c.setFont(fb, 8)
    c.setFillColor(vclr or DARK)
    c.drawRightString(W - MR - 8, y, str(value)[:60])
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.3)
    c.line(ML + 8, y - 4, W - MR - 8, y - 4)
    return y - 14


def _lv2(c, y, label, value, fn, fb, kurum=""):
    """Etiket-deger (ince, aciklama satirlari icin)."""
    if y < 50:
        y = _np(c, fn, fb, kurum)
    c.setFont(fn, 7.5)
    c.setFillColor(DGRAY)
    c.drawString(ML + 16, y, f"{label}:")
    c.setFont(fn, 7.5)
    c.setFillColor(DARK)
    # Uzun metni kes
    txt = str(value)[:80]
    c.drawString(ML + 130, y, txt)
    return y - 12


def _alert(c, y, text, color, fn, kurum="", fb=""):
    """Uyari kutusu."""
    if y < 50:
        y = _np(c, fn, fb, kurum)
    c.setFillColor(CREAM)
    c.roundRect(ML + 6, y - 3, UW - 12, 14, 3, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont(fn, 7.5)
    c.drawString(ML + 12, y, str(text)[:90])
    return y - 17


def _tbl(c, y, headers, rows, widths, fn, fb, kurum=""):
    """Tablo."""
    y = _yc(c, y, fn, fb, kurum)
    c.setFillColor(NAVY)
    c.rect(ML + 4, y - 2, UW - 8, 15, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(fb, 7)
    x = ML + 8
    for i, h in enumerate(headers):
        c.drawString(x, y + 1, h)
        x += widths[i]
    y -= 16
    c.setFont(fn, 7)
    for ri, row in enumerate(rows):
        if y < 50:
            y = _np(c, fn, fb, kurum)
            # Header tekrar
            c.setFillColor(NAVY)
            c.rect(ML + 4, y - 2, UW - 8, 15, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(fb, 7)
            x = ML + 8
            for i, h in enumerate(headers):
                c.drawString(x, y + 1, h)
                x += widths[i]
            y -= 16
            c.setFont(fn, 7)
        if ri % 2 == 0:
            c.setFillColor(GOLD_LIGHT)
            c.rect(ML + 4, y - 2, UW - 8, 13, fill=1, stroke=0)
        c.setFillColor(DARK)
        x = ML + 8
        for i, val in enumerate(row):
            c.drawString(x, y + 1, str(val)[:35])
            x += widths[i]
        y -= 13
    return y - 6


def _gauge(c, x, y, value, mx, label, color, fn, fb, r=26):
    """Gauge."""
    pct = min(value / mx, 1.0) if mx > 0 else 0
    ang = pct * 270
    c.setStrokeColor(LGRAY)
    c.setLineWidth(4.5)
    c.arc(x - r, y - r, x + r, y + r, 135, 270)
    c.setStrokeColor(color)
    c.setLineWidth(4.5)
    if ang > 0:
        c.arc(x - r, y - r, x + r, y + r, 135, ang)
    c.setFillColor(color)
    c.setFont(fb, 11)
    c.drawCentredString(x, y - 3, f"{value:.0f}")
    c.setFillColor(DARK)
    c.setFont(fn, 5.5)
    c.drawCentredString(x, y - 14, label)


def _bar(c, x, y, labels, values, colors, w=200, h=100, fn="TurkishFont"):
    """Bar chart."""
    if not values or all(v == 0 for v in values):
        return
    d = Drawing(w, h)
    bc = VerticalBarChart()
    bc.x = 35
    bc.y = 25
    bc.height = h - 40
    bc.width = w - 55
    bc.data = [values]
    bc.categoryAxis.categoryNames = labels
    bc.categoryAxis.labels.fontName = fn
    bc.categoryAxis.labels.fontSize = 5.5
    bc.categoryAxis.labels.angle = 25
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(values) * 1.2 if values else 100
    bc.valueAxis.labels.fontName = fn
    bc.valueAxis.labels.fontSize = 6
    for i in range(len(values)):
        bc.bars[(0, i)].fillColor = colors[i] if i < len(colors) else BLUE
    d.add(bc)
    renderPDF.draw(d, c, x, y)


def _pie(c, x, y, data, colors, sz=80):
    """Pie chart."""
    if not data or sum(data.values()) == 0:
        return
    d = Drawing(sz, sz)
    p = Pie()
    p.x = 5
    p.y = 5
    p.width = sz - 10
    p.height = sz - 10
    p.data = list(data.values())
    p.labels = [f"{k} ({v})" for k, v in data.items()]
    for i, cl in enumerate(colors[:len(data)]):
        p.slices[i].fillColor = cl
        p.slices[i].strokeWidth = 0.5
        p.slices[i].strokeColor = WHITE
    p.slices.fontName = "TurkishFont"
    p.slices.fontSize = 6
    d.add(p)
    renderPDF.draw(d, c, x, y)


def _multiline(c, y, text, fn, fb, kurum, indent=8, max_w=None):
    """Uzun metni word-wrap ile yaz."""
    if not text or not str(text).strip():
        return y
    max_w = max_w or (UW - 20)
    c.setFont(fn, 7.5)
    c.setFillColor(DARK)
    words = str(text).split()
    line = ""
    for w in words:
        test = f"{line} {w}".strip()
        if c.stringWidth(test, fn, 7.5) > max_w:
            if y < 50:
                y = _np(c, fn, fb, kurum)
            c.drawString(ML + indent, y, line)
            y -= 10
            line = w
        else:
            line = test
    if line:
        if y < 50:
            y = _np(c, fn, fb, kurum)
        c.drawString(ML + indent, y, line)
        y -= 10
    return y


# ═══════════════════════════════════════════════════════════
# ANA PDF URETICI
# ═══════════════════════════════════════════════════════════

def generate_ogrenci_360_pdf(d: dict, ai_text: str = "") -> bytes:
    fn, fb = ensure_turkish_pdf_fonts()
    PAGE[0] = 0
    buf = io.BytesIO()
    c = pdf_canvas.Canvas(buf, pagesize=A4)

    stu = d.get("stu", {})
    name = d.get("name", "?")
    sinif = f'{stu.get("sinif", "?")}/{stu.get("sube", "?")}'
    risk = d.get("latest_risk")
    rs = risk.get("risk_score", 0) if risk else 0
    rl = risk.get("risk_level", "UNKNOWN") if risk else "UNKNOWN"
    rlc = RISK_CLR.get(rl, MGRAY)
    rlt = RISK_TR.get(rl, "?")

    kurum = "SmartCampus AI"
    try:
        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili()
        kurum = kp.get("kurum_adi", kp.get("name", kurum)) or kurum
    except Exception:
        pass

    grades = d.get("grades", [])
    puanlar = [float(g.get("puan", 0)) for g in grades if g.get("puan")]
    ort = sum(puanlar) / len(puanlar) if puanlar else 0
    att = d.get("attendance", [])
    ozursuz = sum(1 for a in att if "ozursuz" in str(a.get("turu", "")).lower())
    ozurlu = len(att) - ozursuz
    yd = d.get("yd_results", [])
    ydp = [float(r.get("score", r.get("puan", 0))) for r in yd if r.get("score") or r.get("puan")]
    yd_avg = sum(ydp) / len(ydp) if ydp else 0

    # ═══════════════════════════════════════
    # SAYFA 1: KAPAK
    # ═══════════════════════════════════════
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(ML, H - 80, W - MR, H - 80)
    c.line(ML, 100, W - MR, 100)
    for dx, dy in [(ML + 10, H - 90), (W - MR - 10, H - 90), (ML + 10, 90), (W - MR - 10, 90)]:
        c.setFillColor(GOLD)
        c.saveState()
        c.translate(dx, dy)
        c.rotate(45)
        c.rect(-4, -4, 8, 8, fill=1, stroke=0)
        c.restoreState()
    c.setFillColor(GOLD)
    c.setFont(fb, 13)
    c.drawCentredString(W / 2, H - 130, kurum)
    c.setFillColor(WHITE)
    c.setFont(fb, 26)
    c.drawCentredString(W / 2, H / 2 + 55, "OGRENCI 360")
    c.setFont(fb, 15)
    c.drawCentredString(W / 2, H / 2 + 32, "PROFIL RAPORU")
    c.setFillColor(GOLD)
    c.rect(W / 2 - 55, H / 2 + 20, 110, 2, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(fb, 17)
    c.drawCentredString(W / 2, H / 2 - 15, name)
    c.setFont(fn, 11)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, H / 2 - 38, f"Sinif: {sinif}  |  No: {stu.get('numara', '-')}")
    c.setFillColor(rlc)
    c.roundRect(W / 2 - 65, H / 2 - 72, 130, 24, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(fb, 9)
    c.drawCentredString(W / 2, H / 2 - 64, f"Risk: {rs:.0f}/100 - {rlt}")
    c.setFillColor(MGRAY)
    c.setFont(fn, 8)
    c.drawCentredString(W / 2, 135, f"Rapor Tarihi: {date.today().isoformat()}")
    c.setFont(fn, 6.5)
    c.drawCentredString(W / 2, 120, "Bu rapor gizlidir - Kisisel Verilerin Korunmasi Kanunu (KVKK) kapsaminda korunur")

    # ═══════════════════════════════════════
    # SAYFA 2: OZET GOSTERGELER
    # ═══════════════════════════════════════
    y = _np(c, fn, fb, kurum)
    c.setFont(fb, 13)
    c.setFillColor(NAVY)
    c.drawString(ML, y, "OZET GOSTERGELER")
    c.setFillColor(GOLD)
    c.rect(ML, y - 6, UW, 1.5, fill=1, stroke=0)
    y -= 35

    # 4 gauge
    gd = [
        (ort, 100, "Akademik Ort", BLUE if ort >= 70 else AMBER if ort >= 50 else RED),
        (rs, 100, "Risk Skoru", rlc),
        (yd_avg, 100, "YD Ortalama", GREEN if yd_avg >= 70 else AMBER if yd_avg >= 50 else RED),
        (ozursuz, 20, "Ozursuz Dev", RED if ozursuz > 10 else AMBER if ozursuz > 5 else GREEN),
    ]
    gx = ML + 55
    for val, mx, lbl, cl in gd:
        _gauge(c, gx, y, val, mx, lbl, cl, fn, fb)
        gx += (UW - 20) / 4
    y -= 55

    # 6 stat kutu
    stats = [
        ("Not", str(len(grades)), BLUE), ("Sinav", str(len(d.get("exams", []))), PURPLE),
        ("Devam.", str(len(att)), AMBER), ("Rehber.", f'{len(d.get("vakalar", []))}V {len(d.get("gorusmeler", []))}G', TEAL),
        ("MEB F.", str(d.get("meb_total", 0) + len(d.get("aile_bilgi", []))), PURPLE),
        ("Saglik", str(len(d.get("saglik", []))), PINK),
    ]
    bw = (UW - 25) / 6
    bx = ML
    for lbl, val, cl in stats:
        c.setFillColor(cl)
        c.roundRect(bx, y - 6, bw, 30, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(fb, 12)
        c.drawCentredString(bx + bw / 2, y + 6, val)
        c.setFont(fn, 6)
        c.drawCentredString(bx + bw / 2, y - 3, lbl)
        bx += bw + 5
    y -= 50

    # Ozet bilgi satirlari
    y = _sec(c, y, "OGRENCI KIMLIK BILGILERI", NAVY, fn, fb, kurum)
    y = _lv(c, y, "Ad Soyad", name, fn, fb, NAVY, kurum)
    y = _lv(c, y, "Sinif / Sube / No", f"{sinif}  /  {stu.get('numara', '-')}", fn, fb, kurum=kurum)
    y = _lv(c, y, "TC Kimlik", stu.get("tc_kimlik", "-"), fn, fb, kurum=kurum)
    y = _lv(c, y, "Veli", f'{stu.get("veli_adi", "-")} {stu.get("veli_soyadi", "")}', fn, fb, kurum=kurum)
    y = _lv(c, y, "Veli Telefon", stu.get("veli_tel", "-"), fn, fb, kurum=kurum)
    y = _lv(c, y, "Risk Seviyesi", f"{rs:.0f}/100 - {rlt}", fn, fb, rlc, kurum)
    y = _lv(c, y, "Akademik Ortalama", f"{ort:.1f}", fn, fb, BLUE if ort >= 70 else RED, kurum)
    y = _lv(c, y, "Devamsizlik", f"{len(att)} gun (ozurlu: {ozurlu}, ozursuz: {ozursuz})", fn, fb, RED if ozursuz > 5 else GREEN, kurum)
    cefr_lvl = d.get("cefr_placement", [{}])[-1].get("cefr_level", "-") if d.get("cefr_placement") else "-"
    y = _lv(c, y, "Yabanci Dil / CEFR", f"Ort: {yd_avg:.0f} / Seviye: {cefr_lvl}", fn, fb, BLUE, kurum)

    # ═══════════════════════════════════════
    # SAYFA 3: AILE BILGI FORMU (DETAYLI)
    # ═══════════════════════════════════════
    y = _np(c, fn, fb, kurum)
    y = _sec(c, y, "AILE BILGI FORMU (B.K.G.1.c) - DETAYLI", TEAL, fn, fb, kurum)

    abf_list = d.get("aile_bilgi", [])
    if abf_list:
        a = abf_list[-1]
        # Anne
        y = _lv(c, y, "Anne Ad Soyad", a.get("anne_adi_soyadi", "-"), fn, fb, kurum=kurum)
        y = _lv(c, y, "Anne Sag/Olu", a.get("anne_sag_olu", "-"), fn, fb,
                RED if a.get("anne_sag_olu") == "Olu" else GREEN, kurum)
        y = _lv(c, y, "Anne Medeni Durum", a.get("anne_birlikte_bosanmis", "-"), fn, fb,
                AMBER if a.get("anne_birlikte_bosanmis") in ("Bosanmis", "Ayri", "Boşanmış", "Ayrı") else GREEN, kurum)
        y = _lv(c, y, "Anne Yeniden Evlenme", a.get("anne_yeniden_evlenme", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Anne Egitim/Meslek", a.get("anne_egitim_meslek", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Anne Iletisim", a.get("anne_tel_eposta", "-") or "-", fn, fb, kurum=kurum)
        y -= 4
        # Baba
        y = _lv(c, y, "Baba Ad Soyad", a.get("baba_adi_soyadi", "-"), fn, fb, kurum=kurum)
        y = _lv(c, y, "Baba Sag/Olu", a.get("baba_sag_olu", "-"), fn, fb,
                RED if a.get("baba_sag_olu") == "Olu" else GREEN, kurum)
        y = _lv(c, y, "Baba Medeni Durum", a.get("baba_birlikte_bosanmis", "-"), fn, fb,
                AMBER if a.get("baba_birlikte_bosanmis") in ("Bosanmis", "Ayri", "Boşanmış", "Ayrı") else GREEN, kurum)
        y = _lv(c, y, "Baba Yeniden Evlenme", a.get("baba_yeniden_evlenme", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Baba Egitim/Meslek", a.get("baba_egitim_meslek", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Baba Iletisim", a.get("baba_tel_eposta", "-") or "-", fn, fb, kurum=kurum)
        y -= 4
        # Bakim veren
        if a.get("bakim_veren_adi"):
            y = _lv(c, y, "Bakim Veren", a.get("bakim_veren_adi", ""), fn, fb, kurum=kurum)
            y = _lv(c, y, "Bakim Veren Bilgi", a.get("bakim_veren_bilgi", "-") or "-", fn, fb, kurum=kurum)
        # Yasam
        y = _lv(c, y, "Kiminle/Nerede Yasiyor", a.get("kiminle_nerede_yasiyor", "-"), fn, fb,
                AMBER if a.get("kiminle_nerede_yasiyor") not in ("Aile", "", None) else GREEN, kurum)
        y = _lv(c, y, "Kardes (Oz/Uvey)", f'Oz: {a.get("kardes_oz_sayisi", 0)}, Uvey: {a.get("kardes_uvey_sayisi", 0)}', fn, fb, kurum=kurum)
        y -= 4
        # Saglik
        y = _sec(c, y, "SAGLIK BILGILERI (Aile Formu)", PINK, fn, fb, kurum)
        y = _lv(c, y, "Suregen Hastalik", a.get("suregen_hastalik", "-") or "Yok", fn, fb,
                RED if a.get("suregen_hastalik") else GREEN, kurum)
        y = _lv(c, y, "Surekli Ilac", a.get("surekli_ilac", "-") or "Yok", fn, fb, kurum=kurum)
        y = _lv(c, y, "Surekli Cihaz", a.get("surekli_cihaz", "-") or "Yok", fn, fb, kurum=kurum)
        y = _lv(c, y, "Etkisindeki Olay (Travma)", a.get("etkisindeki_olay", "-") or "Yok", fn, fb,
                RED if a.get("etkisindeki_olay") else GREEN, kurum)
        # Sosyo-ekonomik
        y = _sec(c, y, "SOSYO-EKONOMIK DURUM", AMBER, fn, fb, kurum)
        y = _lv(c, y, "Aile Yapisi", a.get("aile_kimlerden_olusiyor", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Ekonomiye Katki Saglayan", a.get("ekonomiye_katki_saglayan", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Ortalama Gelir", a.get("ortalama_gelir", "-") or "-", fn, fb,
                RED if any(k in str(a.get("ortalama_gelir", "")).lower() for k in ("dusuk", "asgari", "yetersiz", "düşük")) else DARK, kurum)
        y = _lv(c, y, "Ev Sahipligi", a.get("ev_sahipligi", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Kurum Yardimi", a.get("kurum_yardimi", "-") or "Yok", fn, fb, kurum=kurum)
        y = _lv(c, y, "Suca Karismis Birey", a.get("suca_karismis_birey", "-") or "Yok", fn, fb,
                RED if a.get("suca_karismis_birey") else GREEN, kurum)
        y = _lv(c, y, "Yetersizlik/Suregen Hastalik", a.get("yetersizlik_suregen_hastalik", "-") or "Yok", fn, fb, kurum=kurum)
        y = _lv(c, y, "Bagimlilik Durumu", a.get("bagimllik_durumu", "-") or "Yok", fn, fb,
                RED if a.get("bagimllik_durumu") else GREEN, kurum)
        # Egitim
        y = _sec(c, y, "OGRENCININ EGITIMI", BLUE, fn, fb, kurum)
        y = _lv(c, y, "Okul Oncesi Egitim", a.get("okul_oncesi_egitim", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Okuma Yazma Zamani", a.get("okuma_yazma_zamani", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Okula Tutum", a.get("okula_tutum", "-") or "-", fn, fb,
                AMBER if a.get("okula_tutum") and any(k in str(a.get("okula_tutum", "")).lower() for k in ("olumsuz", "isteksiz")) else DARK, kurum)
        y = _lv(c, y, "Ogretmenlere Tutum", a.get("ogretmenlere_tutum", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Ders Calisma Alani", a.get("ders_calisma_alani", "-") or "-", fn, fb,
                RED if a.get("ders_calisma_alani") == "Hayir" or a.get("ders_calisma_alani") == "Hayır" else GREEN, kurum)
        y = _lv(c, y, "Bagimsiz Calisma", a.get("bagimsiz_calisma_aliskanligi", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Ders Kontrol Eden", a.get("ders_kontrol_eden", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Ders Destegi", a.get("ders_destegi", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Okula Ulasim", a.get("okula_ulasim", "-") or "-", fn, fb, kurum=kurum)
        # Gelisim
        if a.get("dogum_oykusu") or a.get("konusma_baslangic") or a.get("gunluk_rutini"):
            y = _sec(c, y, "OGRENCININ GELISIMI", PURPLE, fn, fb, kurum)
            for key, lbl in [("dogum_oykusu", "Dogum Oykusu"), ("konusma_baslangic", "Konusma Baslangic"),
                             ("yurume_baslangic", "Yurume Baslangic"), ("tuvalet_aliskanligi", "Tuvalet Aliskanligi"),
                             ("aile_disi_iletisim", "Aile Disi Iletisim"), ("gunluk_rutini", "Gunluk Rutin")]:
                val = a.get(key, "")
                if val:
                    y = _lv(c, y, lbl, val, fn, fb, kurum=kurum)
        # Aile ici iletisim
        if a.get("vakit_gecirme") or a.get("birlikte_etkinlikler") or a.get("karar_alma"):
            y = _sec(c, y, "AILE ICI ILETISIM", TEAL, fn, fb, kurum)
            for key, lbl in [("vakit_gecirme", "Vakit Gecirme"), ("birlikte_etkinlikler", "Birlikte Etkinlikler"),
                             ("karar_alma", "Karar Alma"), ("aile_ici_kurallar", "Aile Kurallari"),
                             ("hoslanilar_davranislar", "Hoslanilan Davranislar"),
                             ("hoslanilmayan_davranislar", "Hoslanilmayan Davranislar")]:
                val = a.get(key, "")
                if val:
                    y = _lv(c, y, lbl, val, fn, fb, kurum=kurum)
        # Diger
        if a.get("diger_aciklamalar"):
            y = _lv(c, y, "Diger Aciklamalar", a.get("diger_aciklamalar", ""), fn, fb, kurum=kurum)
        y = _lv(c, y, "Uygulayici", a.get("uygulayici", "-") or "-", fn, fb, kurum=kurum)
        y = _lv(c, y, "Form Tarihi", a.get("tarih", "-") or "-", fn, fb, kurum=kurum)

        # RISK OZETI KUTUSU
        risk_items = []
        if a.get("anne_birlikte_bosanmis") in ("Bosanmis", "Ayri", "Boşanmış", "Ayrı") or a.get("baba_birlikte_bosanmis") in ("Bosanmis", "Ayri", "Boşanmış", "Ayrı"):
            risk_items.append("RISK: Aile bosanmis/ayri")
        if a.get("anne_sag_olu") in ("Olu", "Ölü") or a.get("baba_sag_olu") in ("Olu", "Ölü"):
            risk_items.append("RISK: Ebeveyn kaybi")
        if a.get("etkisindeki_olay"):
            risk_items.append(f"RISK: Travma - {a['etkisindeki_olay']}")
        if a.get("bagimllik_durumu"):
            risk_items.append(f"RISK: Ailede bagimlilik - {a['bagimllik_durumu']}")
        if a.get("suca_karismis_birey"):
            risk_items.append(f"RISK: Ailede suc - {a['suca_karismis_birey']}")
        if a.get("kiminle_nerede_yasiyor") not in ("Aile", "", None):
            risk_items.append(f"RISK: Aile disi yasam - {a['kiminle_nerede_yasiyor']}")
        if a.get("ders_calisma_alani") in ("Hayir", "Hayır"):
            risk_items.append("RISK: Evde calisma alani yok")
        gelir = str(a.get("ortalama_gelir", "")).lower()
        if any(k in gelir for k in ("dusuk", "asgari", "yetersiz", "düşük")):
            risk_items.append("RISK: Ekonomik zorluk")
        if risk_items:
            y -= 4
            y = _sec(c, y, f"AILE RISK OZETI ({len(risk_items)} FAKTOR)", RED, fn, fb, kurum)
            for ri in risk_items:
                y = _alert(c, y, ri, RED, fn, kurum, fb)
        else:
            y = _alert(c, y, "Aile risk faktoru tespit edilmedi", GREEN, fn, kurum, fb)
    else:
        y = _lv(c, y, "Durum", "Aile bilgi formu henuz doldurulmamis", fn, fb, AMBER, kurum)

    # ═══════════════════════════════════════
    # SAYFA: AKADEMIK PERFORMANS
    # ═══════════════════════════════════════
    y = _np(c, fn, fb, kurum)
    y = _sec(c, y, "AKADEMIK PERFORMANS - DERS BAZLI ANALIZ", BLUE, fn, fb, kurum)

    ders_map: dict[str, list] = {}
    for g in grades:
        ders = g.get("ders", g.get("subject", "?"))
        try:
            ders_map.setdefault(ders, []).append(float(g.get("puan", 0)))
        except (ValueError, TypeError):
            pass

    if ders_map:
        labels = list(ders_map.keys())[:10]
        avgs = [sum(ders_map[dd]) / len(ders_map[dd]) for dd in labels]
        colors = [GREEN if a >= 70 else AMBER if a >= 50 else RED for a in avgs]
        _bar(c, ML, y - 130, labels, avgs, colors, w=UW, h=120, fn=fn)
        y -= 145

        headers = ["Ders", "Not Say.", "Ortalama", "Min", "Max", "Durum"]
        rows = []
        for dn in sorted(ders_map.keys()):
            vals = ders_map[dn]
            avg = sum(vals) / len(vals)
            mn, mx = min(vals), max(vals)
            durum = "Basarili" if avg >= 70 else "Dikkat" if avg >= 50 else "Kritik"
            rows.append([dn[:18], str(len(vals)), f"{avg:.0f}", f"{mn:.0f}", f"{mx:.0f}", durum])
        y = _tbl(c, y, headers, rows, [100, 50, 55, 45, 45, 60], fn, fb, kurum)

        # Her ders icin tum notlar
        y -= 6
        y = _sec(c, y, "NOT DETAYLARI", BLUE, fn, fb, kurum)
        headers2 = ["Ders", "Not Turu", "Puan"]
        rows2 = [[g.get("ders", "?")[:18], g.get("not_turu", "-"), str(g.get("puan", "-"))] for g in grades]
        y = _tbl(c, y, headers2, rows2, [130, 140, 80], fn, fb, kurum)
    else:
        y = _lv(c, y, "Durum", "Not kaydi bulunamadi", fn, fb, MGRAY, kurum)

    # Sinav sonuclari
    exams = d.get("exams", [])
    if exams:
        y -= 6
        y = _sec(c, y, "SINAV SONUCLARI", PURPLE, fn, fb, kurum)
        headers = ["Sinav Adi", "Puan", "Tarih"]
        rows = []
        for e in sorted(exams, key=lambda x: x.get("tarih", ""), reverse=True):
            sc = float(e.get("score", e.get("puan", 0)))
            rows.append([e.get("exam_title", e.get("sinav_adi", "?"))[:30], f"{sc:.0f}", str(e.get("tarih", ""))[:10]])
        y = _tbl(c, y, headers, rows, [220, 70, 90], fn, fb, kurum)

    # ═══════════════════════════════════════
    # DEVAMSIZLIK
    # ═══════════════════════════════════════
    y = _sec(c, y, "DEVAMSIZLIK DETAYI", AMBER, fn, fb, kurum)
    y = _lv(c, y, "Toplam Gun", str(len(att)), fn, fb, kurum=kurum)
    y = _lv(c, y, "Ozurlu", str(ozurlu), fn, fb, GREEN, kurum)
    y = _lv(c, y, "Ozursuz", str(ozursuz), fn, fb, RED if ozursuz > 5 else AMBER, kurum)
    if ozursuz > 10:
        y = _alert(c, y, f"KRITIK: Ozursuz devamsizlik {ozursuz} gun - acil mudahale", RED, fn, kurum, fb)
    elif ozursuz > 5:
        y = _alert(c, y, f"UYARI: Ozursuz devamsizlik {ozursuz} gun - takip gerekli", AMBER, fn, kurum, fb)
    if att:
        headers = ["Tarih", "Turu"]
        rows = [[str(a.get("tarih", ""))[:10], a.get("turu", "-")] for a in sorted(att, key=lambda x: x.get("tarih", ""), reverse=True)]
        y = _tbl(c, y, headers, rows, [180, 180], fn, fb, kurum)
        if ozurlu > 0 or ozursuz > 0:
            _pie(c, W - MR - 110, y - 70, {"Ozurlu": ozurlu, "Ozursuz": ozursuz}, [GREEN, RED], 70)

    # ═══════════════════════════════════════
    # ERKEN UYARI
    # ═══════════════════════════════════════
    y = _np(c, fn, fb, kurum)
    y = _sec(c, y, "ERKEN UYARI & RISK DEGERLENDIRMESI", RED, fn, fb, kurum)
    if risk:
        y = _lv(c, y, "Risk Skoru", f"{rs:.0f}/100", fn, fb, rlc, kurum)
        y = _lv(c, y, "Risk Seviyesi", rlt, fn, fb, rlc, kurum)
        y -= 4
        comps = [
            ("Not Riski", "grade_risk"), ("Devamsizlik Riski", "attendance_risk"),
            ("Sinav Riski", "exam_risk"), ("Odev Riski", "homework_risk"),
            ("Kazanim Borcu", "outcome_debt_risk"), ("Rehberlik", "counseling_risk"),
            ("Saglik", "health_risk"), ("Trend", "trend_risk"),
            ("Davranis", "behavior_risk"), ("Yabanci Dil", "foreign_lang_risk"),
        ]
        clbls, cvals, cclrs = [], [], []
        for lbl, key in comps:
            val = risk.get(key, 0)
            vc = RED if val > 60 else AMBER if val > 30 else GREEN
            y = _lv(c, y, f"  {lbl}", f"{val:.0f}/100", fn, fb, vc, kurum)
            clbls.append(lbl[:8])
            cvals.append(val)
            cclrs.append(vc)

        if any(v > 0 for v in cvals):
            _bar(c, ML, y - 120, clbls, cvals, cclrs, w=UW, h=110, fn=fn)
            y -= 135

        fl = risk.get("foreign_lang_performance", {})
        flags = [
            ("dehb_yonlendirme", "DEHB yonlendirme onerilmis"),
            ("oog_yonlendirme", "OOG yonlendirme onerilmis"),
            ("psikolojik_acil", "Psikolojik destek - ACIL"),
            ("psikolojik_orta", "Psikolojik destek - Orta"),
            ("ev_ziyareti_acil", "Ev ziyareti - acil takip"),
            ("ebeveyn_kaybi", "Ebeveyn kaybi"),
            ("aile_bosanmis", "Aile bosanmis/ayri"),
            ("travmatik_olay", "Travma mevcut"),
            ("ailede_bagimlilik", "Ailede bagimlilik"),
            ("ekonomik_zorluk", "Ekonomik zorluk"),
            ("duygusal_risk", "Duygusal risk"),
            ("disiplin_olay_sayisi", "Disiplin olayi"),
        ]
        active_flags = [(lbl, fl.get(fk)) for fk, lbl in flags if fl.get(fk)]
        if active_flags:
            y -= 4
            y = _sec(c, y, f"RISK FLAGLERI ({len(active_flags)} TESPIT)", RED, fn, fb, kurum)
            for lbl, val in active_flags:
                detail = f" ({val})" if isinstance(val, str) and val not in ("True", "true") else ""
                y = _alert(c, y, f"{lbl}{detail}", RED, fn, kurum, fb)
    else:
        y = _lv(c, y, "Durum", "Risk henuz hesaplanmadi", fn, fb, MGRAY, kurum)

    # ═══════════════════════════════════════
    # YABANCI DIL
    # ═══════════════════════════════════════
    y = _sec(c, y, "YABANCI DIL GELISIMI", BLUE, fn, fb, kurum)
    cefr = d.get("cefr_placement", [])
    if cefr:
        last = cefr[-1]
        y = _lv(c, y, "CEFR Seviyesi", last.get("cefr_level", "-"), fn, fb, BLUE, kurum)
        y = _lv(c, y, "Yerlestirme Puani", str(last.get("total_score", "-")), fn, fb, kurum=kurum)
    if yd:
        y = _lv(c, y, f"Sinav/Quiz ({len(yd)} adet)", f"Ort: {yd_avg:.0f}", fn, fb,
                GREEN if yd_avg >= 70 else AMBER if yd_avg >= 50 else RED, kurum)
        headers = ["Tur", "Puan", "Tarih"]
        rows = [[r.get("exam_type", r.get("tur", "?"))[:20], f'{float(r.get("score", r.get("puan", 0))):.0f}',
                 str(r.get("tarih", r.get("date", "")))[:10]]
                for r in sorted(yd, key=lambda x: x.get("tarih", x.get("date", "")), reverse=True)]
        y = _tbl(c, y, headers, rows, [160, 80, 120], fn, fb, kurum)
    mock = d.get("cefr_mock", [])
    if mock:
        y = _lv(c, y, "CEFR Mock Sinav", f"{len(mock)} adet", fn, fb, kurum=kurum)

    # ═══════════════════════════════════════
    # REHBERLIK
    # ═══════════════════════════════════════
    y = _np(c, fn, fb, kurum)
    y = _sec(c, y, "REHBERLIK - VAKA & GORUSME & TEST DETAYI", TEAL, fn, fb, kurum)
    vakalar = d.get("vakalar", [])
    if vakalar:
        y = _lv(c, y, "Aktif Vaka", str(len(vakalar)), fn, fb, RED if any(v.get("durum") == "ACIK" for v in vakalar) else AMBER, kurum)
        headers = ["Vaka Basligi", "Durum", "Oncelik"]
        rows = [[v.get("vaka_basligi", v.get("konu", "?"))[:30], v.get("durum", "?"), v.get("oncelik", "-")] for v in vakalar]
        y = _tbl(c, y, headers, rows, [220, 70, 80], fn, fb, kurum)

    gorusmeler = d.get("gorusmeler", [])
    if gorusmeler:
        y -= 4
        y = _lv(c, y, "Toplam Gorusme", str(len(gorusmeler)), fn, fb, TEAL, kurum)
        headers = ["Gorusme Konusu", "Tarih"]
        rows = [[g.get("gorusme_konusu", g.get("konu", "?"))[:35], str(g.get("tarih", ""))[:10]]
                for g in sorted(gorusmeler, key=lambda x: x.get("tarih", ""), reverse=True)]
        y = _tbl(c, y, headers, rows, [280, 100], fn, fb, kurum)

    oturumlar = d.get("rhb_oturumlar", [])
    if oturumlar:
        y -= 4
        y = _sec(c, y, "REHBERLIK TEST SONUCLARI", PURPLE, fn, fb, kurum)
        tst_map = {t.get("id", ""): t for t in d.get("rhb_testler", [])}
        cevaplar = d.get("rhb_cevaplar", [])
        headers = ["Test Adi", "Durum", "Cevap Say.", "Ort. Puan"]
        rows = []
        for o in oturumlar:
            tst = tst_map.get(o.get("test_id", ""), {})
            oc = [cc for cc in cevaplar if cc.get("oturum_id") == o.get("id")]
            pp = [float(cc.get("puan", 0)) for cc in oc if cc.get("puan")]
            avg = f"{sum(pp)/len(pp):.1f}" if pp else "-"
            rows.append([tst.get("test_adi", "?")[:25], o.get("durum", "?"), str(len(oc)), avg])
        y = _tbl(c, y, headers, rows, [150, 80, 60, 70], fn, fb, kurum)

    if not vakalar and not gorusmeler and not oturumlar:
        y = _lv(c, y, "Durum", "Rehberlik kaydi yok", fn, fb, MGRAY, kurum)

    # ═══════════════════════════════════════
    # MEB DIJITAL FORMLAR
    # ═══════════════════════════════════════
    meb = d.get("meb_forms", {})
    if meb:
        y -= 6
        y = _sec(c, y, f"MEB DIJITAL FORMLAR ({sum(len(v) for v in meb.values())} KAYIT)", PURPLE, fn, fb, kurum)
        try:
            from models.meb_formlar import MEB_FORM_SCHEMAS
        except ImportError:
            MEB_FORM_SCHEMAS = {}
        for sk, forms in meb.items():
            sch = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == sk), None)
            fname = sch["title"] if sch else sk
            fclr = RED if sk in ("dehb_gozlem_formlari", "psikolojik_yonlendirme_formlari", "ozel_ogrenme_guclugu_formlari") else AMBER if sk in ("disiplin_gorusme_formlari", "ev_ziyareti_formlari") else BLUE
            y = _lv(c, y, fname[:35], f"{len(forms)} kayit", fn, fb, fclr, kurum)
            # Her formun detayli alanlari
            for f in forms[-2:]:  # Son 2 kayit
                for key, val in f.items():
                    if key in ("id", "olusturma_zamani", "guncelleme_zamani", "ogrenci_id", "ogrenci_adi_soyadi"):
                        continue
                    if val and str(val).strip() and val not in ("", "Gozlenmedi", 0, "0", False, "False"):
                        y = _lv2(c, y, key.replace("_", " ").title()[:25], str(val)[:70], fn, fb, kurum)

    # ═══════════════════════════════════════
    # SAGLIK + TELAFI + KOCLUK + ODEV
    # ═══════════════════════════════════════
    y = _np(c, fn, fb, kurum)

    # Saglik
    y = _sec(c, y, "OKUL SAGLIGI (REVIR)", PINK, fn, fb, kurum)
    saglik = d.get("saglik", [])
    if saglik:
        y = _lv(c, y, "Ziyaret Sayisi", str(len(saglik)), fn, fb, kurum=kurum)
        takip = sum(1 for s in saglik if s.get("takip_gerekiyor"))
        if takip:
            y = _lv(c, y, "Takip Gereken", str(takip), fn, fb, AMBER, kurum)
        headers = ["Sikayet", "Tarih", "Takip"]
        rows = [[s.get("sikayet_kategorisi", "?"), str(s.get("basvuru_tarihi", ""))[:10],
                 "Evet" if s.get("takip_gerekiyor") else "Hayir"] for s in saglik]
        y = _tbl(c, y, headers, rows, [180, 100, 60], fn, fb, kurum)
    else:
        y = _lv(c, y, "Durum", "Saglik ziyareti yok", fn, fb, GREEN, kurum)

    # Kazanim Borcu
    borc = d.get("borc", [])
    y -= 6
    y = _sec(c, y, "KAZANIM BORCU & TELAFI", ORANGE, fn, fb, kurum)
    if borc:
        acik = [b for b in borc if b.get("durum") == "borc_var"]
        y = _lv(c, y, "Acik Borc", str(len(acik)), fn, fb, RED if acik else GREEN, kurum)
        y = _lv(c, y, "Kapatilan", str(len(borc) - len(acik)), fn, fb, GREEN, kurum)
        if acik:
            headers = ["Ders", "Kazanim Kodu", "Durum"]
            rows = [[b.get("ders", ""), b.get("kazanim_kodu", ""), b.get("durum", "")] for b in borc]
            y = _tbl(c, y, headers, rows, [120, 150, 80], fn, fb, kurum)
    telafi = d.get("telafi", [])
    if telafi:
        comp = sum(1 for t in telafi if t.get("status") == "completed")
        y = _lv(c, y, "Telafi Gorevi", f"{len(telafi)} ({comp} tamamlanan)", fn, fb, kurum=kurum)
        bands: dict[str, int] = {}
        for t in telafi:
            bands[t.get("color_band", "?")] = bands.get(t.get("color_band", "?"), 0) + 1
        bc = {"RED": RED, "YELLOW": AMBER, "GREEN": GREEN, "BLUE": BLUE}
        if bands:
            for bn, cnt in bands.items():
                y = _lv(c, y, f"  {bn} Band", str(cnt), fn, fb, bc.get(bn, MGRAY), kurum)
    if not borc and not telafi:
        y = _lv(c, y, "Durum", "Kazanim borcu ve telafi yok", fn, fb, GREEN, kurum)

    # Kocluk
    y -= 6
    y = _sec(c, y, "EGITIM KOCLUGU", GREEN, fn, fb, kurum)
    kc = d.get("kocluk")
    if kc:
        y = _lv(c, y, "Koc", kc.get("koc_adi", "-"), fn, fb, kurum=kurum)
        y = _lv(c, y, "Motivasyon", f'{kc.get("motivasyon_seviyesi", "-")}/5', fn, fb,
                RED if (kc.get("motivasyon_seviyesi") or 0) <= 2 else AMBER if (kc.get("motivasyon_seviyesi") or 0) <= 3 else GREEN, kurum)
        y = _lv(c, y, "Hedef Sinav / Puan", f'{kc.get("hedef_sinav", "-")} {kc.get("hedef_puan", "")}', fn, fb, kurum=kurum)
        y = _lv(c, y, "Guclu Dersler", kc.get("guclu_dersler", "-"), fn, fb, GREEN, kurum)
        y = _lv(c, y, "Zayif Dersler", kc.get("zayif_dersler", "-"), fn, fb, RED, kurum)
    else:
        y = _lv(c, y, "Durum", "Kocluk kaydi yok", fn, fb, MGRAY, kurum)

    # Odev & KYT
    hw = d.get("hw_subs", [])
    kyt = d.get("kyt", [])
    if hw or kyt:
        y -= 6
        y = _sec(c, y, "ODEV & KAZANIM YOKLAMA TESTI", DGRAY, fn, fb, kurum)
        if hw:
            teslim = sum(1 for s in hw if s.get("durum") in ("teslim_edildi", "degerlendirildi"))
            oran = (teslim / len(hw) * 100) if hw else 0
            y = _lv(c, y, "Odev Teslim", f"{teslim}/{len(hw)} (%{oran:.0f})", fn, fb,
                    GREEN if oran >= 80 else AMBER if oran >= 60 else RED, kurum)
        if kyt:
            dogru = sum(1 for k in kyt if k.get("dogru"))
            oran = (dogru / len(kyt) * 100) if kyt else 0
            y = _lv(c, y, "KYT Basari", f"{dogru}/{len(kyt)} (%{oran:.0f})", fn, fb,
                    GREEN if oran >= 70 else AMBER if oran >= 50 else RED, kurum)

    # TUM TEST SONUCLARI (Rehberlik + Kayit birlesik)
    tum_t = d.get("tum_testler", []) or d.get("kayit_testler", [])
    if tum_t:
        y -= 6
        rhb_cnt = sum(1 for t in tum_t if "Rehberlik" in t.get("kaynak", ""))
        km_cnt = sum(1 for t in tum_t if "Kayit" in t.get("kaynak", ""))
        y = _sec(c, y, f"TUM TEST SONUCLARI ({len(tum_t)} TEST: Rehberlik {rhb_cnt} + Kayit {km_cnt})", PURPLE, fn, fb, kurum)
        for t in tum_t:
            kaynak = t.get("kaynak", "?")
            test_adi = t.get("test_adi", "?")[:30]
            durum = t.get("durum", t.get("sonuc", "-"))
            tarih = str(t.get("tarih", ""))[:10]
            y = _lv(c, y, f'{test_adi}', f'{durum} | {tarih}', fn, fb, PURPLE, kurum)
            y = _lv2(c, y, "Kaynak", kaynak, fn, fb, kurum)
            if t.get("test_kategorisi"):
                y = _lv2(c, y, "Kategori", t["test_kategorisi"], fn, fb, kurum)
            if t.get("genel_ortalama"):
                y = _lv2(c, y, "Genel Ort", str(t["genel_ortalama"]), fn, fb, kurum)
            skorlar = t.get("skorlar", {})
            if skorlar:
                skor_str = " | ".join(f"{k}: {v}" for k, v in list(skorlar.items())[:6])
                y = _lv2(c, y, "Skorlar", skor_str, fn, fb, kurum)
            olcek_p = t.get("olcek_puanlari", {})
            if olcek_p:
                olc_str = " | ".join(f"{k}: {v}" for k, v in list(olcek_p.items())[:6])
                y = _lv2(c, y, "Olcek Puan", olc_str, fn, fb, kurum)
            top3 = t.get("top3", [])
            if top3:
                top3_str = ", ".join(f'{i.get("alan","?")}: {i.get("skor","-")}' for i in top3)
                y = _lv2(c, y, "En Guclu 3", top3_str, fn, fb, kurum)
            y -= 2

    # ═══════════════════════════════════════
    # YIL BAZLI TREND ANALIZI
    # ═══════════════════════════════════════
    tr = d.get("trend", {})
    yil_bazli = tr.get("yil_bazli", {})
    if yil_bazli and len(yil_bazli) >= 1:
        y = _np(c, fn, fb, kurum)
        y = _sec(c, y, f"YIL BAZLI TREND ANALIZI ({len(yil_bazli)} EGITIM YILI)", BLUE, fn, fb, kurum)

        # Tablo
        headers = ["Egitim Yili", "Not Ort", "Devamsiz", "Ozursuz", "Sinav Ort", "Gorusme", "Vaka"]
        rows = []
        for ey, data in sorted(yil_bazli.items()):
            rows.append([ey, f"{data['not_ort']:.0f}", str(data['devamsiz_toplam']),
                         str(data['devamsiz_ozursuz']), f"{data['sinav_ort']:.0f}",
                         str(data['gorusme']), str(data['vaka'])])
        y = _tbl(c, y, headers, rows, [80, 50, 50, 50, 55, 50, 40], fn, fb, kurum)

        # Yıllar arası değişim
        yillar = sorted(yil_bazli.keys())
        if len(yillar) >= 2:
            y -= 6
            y = _sec(c, y, "YILLAR ARASI DEGISIM", AMBER, fn, fb, kurum)
            for i in range(1, len(yillar)):
                prev_ey = yillar[i - 1]
                curr_ey = yillar[i]
                prev = yil_bazli[prev_ey]
                curr = yil_bazli[curr_ey]
                not_diff = curr["not_ort"] - prev["not_ort"]
                dev_diff = curr["devamsiz_ozursuz"] - prev["devamsiz_ozursuz"]
                nc = GREEN if not_diff > 0 else RED if not_diff < -5 else AMBER
                dc = RED if dev_diff > 3 else GREEN if dev_diff < 0 else AMBER
                y = _lv(c, y, f"{prev_ey} → {curr_ey} Not", f"{not_diff:+.0f} puan", fn, fb, nc, kurum)
                y = _lv(c, y, f"{prev_ey} → {curr_ey} Ozursuz", f"{dev_diff:+d} gun", fn, fb, dc, kurum)

        # Risk trendi
        risk_trend = tr.get("risk_trend", [])
        if risk_trend:
            y -= 4
            y = _lv(c, y, "Risk Trendi",
                    " → ".join(f'{r["skor"]:.0f}({r["seviye"]})' for r in risk_trend), fn, fb, RED, kurum)

        # Donum noktalari
        donum = tr.get("donum_noktalari", [])
        if donum:
            y -= 6
            y = _sec(c, y, f"DONUM NOKTALARI ({len(donum)} TESPIT)", RED, fn, fb, kurum)
            for dn in donum:
                y = _alert(c, y, f"[{dn['tarih']}] {dn['olay']} — {dn['etki']}", RED, fn, kurum, fb)

        # Mudahale etkinligi
        mudahale = tr.get("mudahale_etkinlik", [])
        if mudahale:
            y -= 6
            y = _sec(c, y, f"MUDAHALE ETKINLIGI ({len(mudahale)})", TEAL, fn, fb, kurum)
            for m in mudahale:
                etki_clr = GREEN if m["etki"] == "olumlu" else RED if m["etki"] == "olumsuz" else AMBER
                y = _lv(c, y, m["mudahale"][:40], f'{m["oncesi"]} → {m["sonrasi"]}', fn, fb, etki_clr, kurum)

    # ═══════════════════════════════════════
    # AI 360 DEGERLENDIRME
    # ═══════════════════════════════════════
    if ai_text:
        y = _np(c, fn, fb, kurum)
        y = _sec(c, y, "AI 360 MEGA DEGERLENDIRME (GPT-4o-mini)", PURPLE, fn, fb, kurum)
        for line in ai_text.split("\n"):
            line = line.strip()
            if not line:
                y -= 5
                continue
            if y < 55:
                y = _np(c, fn, fb, kurum)
            if line.startswith("## "):
                y -= 3
                c.setFillColor(NAVY)
                c.roundRect(ML + 4, y - 2, UW - 8, 15, 3, fill=1, stroke=0)
                c.setFillColor(GOLD)
                c.setFont(fb, 8.5)
                c.drawString(ML + 10, y + 1, line.replace("## ", ""))
                y -= 18
                continue
            if line.startswith("- "):
                c.setFillColor(GOLD)
                c.circle(ML + 14, y + 2, 1.5, fill=1, stroke=0)
                c.setFillColor(DARK)
                y = _multiline(c, y, line[2:], fn, fb, kurum, indent=20)
            else:
                y = _multiline(c, y, line, fn, fb, kurum, indent=10)

    # ═══════════════════════════════════════
    # IMZA ALANI
    # ═══════════════════════════════════════
    if y < 180:
        y = _np(c, fn, fb, kurum)
    y -= 20
    c.setFillColor(GOLD)
    c.rect(ML, y, UW, 1.5, fill=1, stroke=0)
    y -= 30
    boxes = [("Rehber Ogretmen", ML + 15), ("Sinif Ogretmeni", W / 2 - 50), ("Okul Muduru", W - MR - 120)]
    for title, bx in boxes:
        c.setFont(fb, 8)
        c.setFillColor(DARK)
        c.drawString(bx, y, title)
        c.setFont(fn, 7.5)
        c.drawString(bx, y - 14, "Ad Soyad: ......................")
        c.drawString(bx, y - 28, "Imza:     ......................")
        c.drawString(bx, y - 42, f"Tarih:    {date.today().isoformat()}")

    c.save()
    return buf.getvalue()
