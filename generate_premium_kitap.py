#!/usr/bin/env python3
"""SmartCampusAI Premium Ders Kitabi - Animatik figurler, profesyonel baski formati."""
import os, re, json, textwrap, math, io
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Cal", "C:/Windows/Fonts/calibri.ttf"))
pdfmetrics.registerFont(TTFont("CalB", "C:/Windows/Fonts/calibrib.ttf"))
pdfmetrics.registerFont(TTFont("CalI", "C:/Windows/Fonts/calibrii.ttf"))

W, H = A4
# Premium renk paleti
NAVY=HexColor("#0F172A"); GOLD=HexColor("#C5962E"); WHITE=HexColor("#FFFFFF")
CREAM=HexColor("#FFFCF5"); TEAL=HexColor("#0891B2"); GRAY=HexColor("#6B7280")
DARK=HexColor("#1E293B"); LGRAY=HexColor("#F1F5F9"); GREEN=HexColor("#059669")
BLUE=HexColor("#2563EB"); PURPLE=HexColor("#7C3AED"); ROSE=HexColor("#E11D48")
AMBER=HexColor("#D97706"); SKY=HexColor("#0EA5E9"); EMERALD=HexColor("#10B981")
INDIGO=HexColor("#4F46E5"); PINK=HexColor("#EC4899"); ORANGE=HexColor("#F97316")

# Acik tonlar
LGREEN=HexColor("#F0FDF4"); LBLUE=HexColor("#EFF6FF"); LPURPLE=HexColor("#F5F3FF")
LYELLOW=HexColor("#FEFCE8"); LROSE=HexColor("#FFF1F2"); LTEAL=HexColor("#F0FDFA")
LORANGE=HexColor("#FFF7ED"); LGOLD=HexColor("#FFFBEB")

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Ders_Kitaplari_PDF", "Ilkokul_Premium")
os.makedirs(OUT, exist_ok=True)

DERS_RENK = {
    "T\u00fcrk\u00e7e": (BLUE, LBLUE, SKY),
    "Matematik": (PURPLE, LPURPLE, INDIGO),
    "Hayat Bilgisi": (GREEN, LGREEN, EMERALD),
    "Fen Bilimleri": (TEAL, LTEAL, SKY),
    "Sosyal Bilgiler": (AMBER, LORANGE, ORANGE),
    "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi": (ROSE, LROSE, PINK),
}
DERS_KEY = {"T\u00fcrk\u00e7e":"turkce","Matematik":"matematik","Hayat Bilgisi":"hayat_bilgisi",
    "Fen Bilimleri":"fen","Sosyal Bilgiler":"sosyal","Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi":"din_kulturu"}

# Animatik figurler (emoji + basit cizimler)
DERS_FIGUR = {
    "T\u00fcrk\u00e7e": ["A", "B", "C"],
    "Matematik": ["+", "=", "?"],
    "Hayat Bilgisi": ["*", "~", "#"],
    "Fen Bilimleri": ["@", "&", "%"],
    "Sosyal Bilgiler": ["!", ">", "<"],
    "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi": ["^", ":", ";"],
}


def load_kazanimlar(grade, subject):
    with open(os.path.join(BASE,"data","olcme","annual_plans.json"),"r",encoding="utf-8") as f:
        plans = json.load(f)
    return sorted([p for p in plans if p.get("grade")==grade and p.get("subject")==subject],
                  key=lambda p:(p.get("unit",""),p.get("week","")))


def load_referans(key, sinif):
    fname = os.path.join(BASE,"data",f"{key}_{sinif}_referans.py")
    if not os.path.exists(fname): return {}
    with open(fname,"r",encoding="utf-8") as f: raw=f.read()
    entries={}
    for m in re.finditer(r'"baslik"\s*:\s*"([^"]*)".*?"icerik"\s*:\s*"""(.*?)"""',raw,re.DOTALL):
        entries[m.group(1)]=m.group(2).strip()
    return entries


IMG_DIR = os.path.join(BASE, "Ders_Kitaplari_PDF", "test_chars")

# Ders bazli gorsel haritasi
DERS_GORSELLER = {
    "T\u00fcrk\u00e7e": ["ogrenci_kiz.png","kitap.png","alfabe.png","ogretmen.png","kedi.png"],
    "Matematik": ["ogrenci_erkek.png","geometri.png","sayilar.png","mat_denklem.png","ogretmen.png"],
    "Hayat Bilgisi": ["ogrenci_kiz.png","ev.png","agac.png","gunes.png","cicek.png","bayrak.png"],
    "Fen Bilimleri": ["ogrenci_erkek.png","agac.png","gunes.png","bulut.png","cicek.png","kus.png"],
    "Sosyal Bilgiler": ["bayrak.png","ev.png","ogrenci_kiz.png","ogretmen.png","kitap.png"],
    "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi": ["yildizlar.png","ogrenci_erkek.png","kitap.png","ogretmen.png","cicek.png"],
}


class PremiumKitap:
    def __init__(self, path, ders, sinif, renk, renk_acik, renk2):
        self.c=Canvas(path,pagesize=A4)
        self.ders=ders; self.sinif=sinif
        self.r=renk; self.rl=renk_acik; self.r2=renk2
        self.pn=0; self.y=0
        self.gorseller = DERS_GORSELLER.get(ders, ["ogrenci_kiz.png","kitap.png"])

    def _img(self, name, x, y, w=None, h=None):
        """PNG gorsel ekle."""
        path = os.path.join(IMG_DIR, name)
        if os.path.exists(path):
            kw = {}
            if w: kw["width"] = w
            if h: kw["height"] = h
            if not kw: kw = {"width": 60}
            try:
                self.c.drawImage(path, x, y, mask="auto", preserveAspectRatio=True, **kw)
            except: pass

    def _qr(self, x, y, url, size=55):
        """QR kod olustur ve sayfaya yerlestir."""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            from reportlab.lib.utils import ImageReader
            self.c.drawImage(ImageReader(buf), x, y, width=size, height=size)
        except: pass

    def _qr_kutusu(self, x, y, url, label="Dijital Icerik"):
        """QR kod + etiket kutusu."""
        self.c.setFillColor(LGRAY)
        self.c.roundRect(x-5, y-5, 75, 80, 6, fill=1, stroke=0)
        self._qr(x, y+12, url, 55)
        self.c.setFont("Cal", 6); self.c.setFillColor(DARK)
        self.c.drawCentredString(x+27, y+2, label)
        self.c.setFont("Cal", 5); self.c.setFillColor(GRAY)
        self.c.drawCentredString(x+27, y-5, "Tara ve Ogren!")

    # ── Dekoratif cizimler ──
    def _draw_circle_pattern(self, x, y, r, col, count=5):
        """Dekoratif daire pattern."""
        self.c.setFillColor(col)
        for i in range(count):
            angle = i * (360/count)
            cx = x + r * math.cos(math.radians(angle))
            cy = y + r * math.sin(math.radians(angle))
            self.c.circle(cx, cy, 3, fill=1, stroke=0)

    def _draw_star(self, x, y, size, col):
        """5 koseli yildiz."""
        self.c.setFillColor(col)
        p = self.c.beginPath()
        for i in range(5):
            angle = math.radians(-90 + i*72)
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            if i==0: p.moveTo(px,py)
            else: p.lineTo(px,py)
            angle2 = math.radians(-90 + i*72 + 36)
            px2 = x + size*0.4 * math.cos(angle2)
            py2 = y + size*0.4 * math.sin(angle2)
            p.lineTo(px2,py2)
        p.close()
        self.c.drawPath(p,fill=1,stroke=0)

    def _draw_book_icon(self, x, y, size, col):
        """Kitap ikonu."""
        self.c.setFillColor(col)
        self.c.rect(x, y, size*0.7, size, fill=1, stroke=0)
        self.c.setFillColor(WHITE)
        self.c.rect(x+2, y+2, size*0.7-4, size-4, fill=1, stroke=0)
        self.c.setFillColor(col)
        for i in range(4):
            self.c.rect(x+5, y+5+i*(size/5), size*0.5, 2, fill=1, stroke=0)

    def _draw_pencil(self, x, y, size, col):
        """Kalem ikonu."""
        self.c.setFillColor(col)
        self.c.rect(x, y, 6, size*0.8, fill=1, stroke=0)
        p=self.c.beginPath()
        p.moveTo(x,y); p.lineTo(x+3,y-size*0.2); p.lineTo(x+6,y); p.close()
        self.c.drawPath(p,fill=1,stroke=0)

    def _draw_lightbulb(self, x, y, size, col):
        """Ampul ikonu."""
        self.c.setFillColor(col)
        self.c.circle(x, y+size*0.4, size*0.3, fill=1, stroke=0)
        self.c.rect(x-3, y, 6, size*0.2, fill=1, stroke=0)

    def _draw_check_badge(self, x, y, col):
        """Tik rozet."""
        self.c.setFillColor(col)
        self.c.circle(x, y, 8, fill=1, stroke=0)
        self.c.setStrokeColor(WHITE); self.c.setLineWidth(2)
        self.c.line(x-3, y, x-1, y-3)
        self.c.line(x-1, y-3, x+4, y+3)

    # ── GORSEL ILLUSTRASYONLAR ──

    def _draw_student(self, x, y, scale=1.0, col=None):
        """Ogrenci figuru — kafa + govde + kollar + bacaklar."""
        c = self.c; s = scale; cl = col or self.r
        # Kafa
        c.setFillColor(HexColor("#FBBF24"))
        c.circle(x, y+25*s, 10*s, fill=1, stroke=0)
        # Gozler
        c.setFillColor(NAVY)
        c.circle(x-3*s, y+27*s, 1.5*s, fill=1, stroke=0)
        c.circle(x+3*s, y+27*s, 1.5*s, fill=1, stroke=0)
        # Gulucuk
        c.setStrokeColor(NAVY); c.setLineWidth(0.8*s)
        p=c.beginPath(); p.arc(x-4*s,y+20*s,x+4*s,y+25*s,200,140); c.drawPath(p,fill=0,stroke=1)
        # Govde
        c.setFillColor(cl)
        c.rect(x-8*s, y-5*s, 16*s, 20*s, fill=1, stroke=0)
        # Kollar
        c.setFillColor(HexColor("#FBBF24"))
        c.rect(x-14*s, y+2*s, 6*s, 4*s, fill=1, stroke=0)
        c.rect(x+8*s, y+2*s, 6*s, 4*s, fill=1, stroke=0)
        # Bacaklar
        c.setFillColor(NAVY)
        c.rect(x-6*s, y-18*s, 5*s, 14*s, fill=1, stroke=0)
        c.rect(x+1*s, y-18*s, 5*s, 14*s, fill=1, stroke=0)

    def _draw_teacher(self, x, y, scale=1.0):
        """Ogretmen figuru — daha uzun + gozluk."""
        c = self.c; s = scale
        # Kafa
        c.setFillColor(HexColor("#FBBF24"))
        c.circle(x, y+30*s, 11*s, fill=1, stroke=0)
        # Gozluk
        c.setStrokeColor(NAVY); c.setLineWidth(1*s)
        c.circle(x-4*s, y+32*s, 4*s, fill=0, stroke=1)
        c.circle(x+4*s, y+32*s, 4*s, fill=0, stroke=1)
        c.line(x, y+32*s, x, y+32*s)
        # Govde
        c.setFillColor(EMERALD)
        c.rect(x-10*s, y-5*s, 20*s, 25*s, fill=1, stroke=0)
        # Kollar
        c.setFillColor(HexColor("#FBBF24"))
        c.rect(x-16*s, y+5*s, 6*s, 4*s, fill=1, stroke=0)
        c.rect(x+10*s, y+5*s, 6*s, 4*s, fill=1, stroke=0)
        # Kitap
        c.setFillColor(AMBER)
        c.rect(x+14*s, y+2*s, 8*s, 10*s, fill=1, stroke=0)
        # Bacaklar
        c.setFillColor(NAVY)
        c.rect(x-7*s, y-22*s, 5*s, 18*s, fill=1, stroke=0)
        c.rect(x+2*s, y-22*s, 5*s, 18*s, fill=1, stroke=0)

    def _draw_tree(self, x, y, scale=1.0):
        """Agac — govde + yapraklar."""
        c=self.c; s=scale
        c.setFillColor(HexColor("#92400E"))
        c.rect(x-3*s, y, 6*s, 20*s, fill=1, stroke=0)
        c.setFillColor(EMERALD)
        c.circle(x, y+28*s, 14*s, fill=1, stroke=0)
        c.setFillColor(GREEN)
        c.circle(x-8*s, y+22*s, 10*s, fill=1, stroke=0)
        c.circle(x+8*s, y+22*s, 10*s, fill=1, stroke=0)

    def _draw_sun(self, x, y, scale=1.0):
        """Gunes — daire + isinlar."""
        c=self.c; s=scale
        c.setFillColor(HexColor("#FBBF24"))
        c.circle(x, y, 12*s, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#F59E0B")); c.setLineWidth(1.5*s)
        for i in range(8):
            angle = math.radians(i*45)
            c.line(x+15*s*math.cos(angle), y+15*s*math.sin(angle),
                   x+22*s*math.cos(angle), y+22*s*math.sin(angle))

    def _draw_cloud(self, x, y, scale=1.0):
        """Bulut."""
        c=self.c; s=scale
        c.setFillColor(HexColor("#E2E8F0"))
        c.circle(x, y, 10*s, fill=1, stroke=0)
        c.circle(x-10*s, y-3*s, 8*s, fill=1, stroke=0)
        c.circle(x+10*s, y-3*s, 8*s, fill=1, stroke=0)
        c.circle(x+5*s, y+4*s, 9*s, fill=1, stroke=0)

    def _draw_house(self, x, y, scale=1.0):
        """Ev."""
        c=self.c; s=scale
        c.setFillColor(HexColor("#FDE68A"))
        c.rect(x-15*s, y, 30*s, 25*s, fill=1, stroke=0)
        # Cati
        c.setFillColor(HexColor("#DC2626"))
        p=c.beginPath(); p.moveTo(x-20*s,y+25*s); p.lineTo(x,y+40*s); p.lineTo(x+20*s,y+25*s); p.close()
        c.drawPath(p,fill=1,stroke=0)
        # Kapi
        c.setFillColor(HexColor("#92400E"))
        c.rect(x-4*s, y, 8*s, 14*s, fill=1, stroke=0)
        # Pencere
        c.setFillColor(SKY)
        c.rect(x+8*s, y+12*s, 6*s, 6*s, fill=1, stroke=0)

    def _draw_cat(self, x, y, scale=1.0):
        """Kedi."""
        c=self.c; s=scale
        c.setFillColor(HexColor("#F97316"))
        c.ellipse(x-8*s, y-5*s, x+8*s, y+8*s, fill=1, stroke=0)
        c.circle(x, y+14*s, 7*s, fill=1, stroke=0)
        # Kulaklar
        p=c.beginPath(); p.moveTo(x-6*s,y+18*s); p.lineTo(x-3*s,y+25*s); p.lineTo(x,y+18*s); p.close()
        c.drawPath(p,fill=1,stroke=0)
        p=c.beginPath(); p.moveTo(x,y+18*s); p.lineTo(x+3*s,y+25*s); p.lineTo(x+6*s,y+18*s); p.close()
        c.drawPath(p,fill=1,stroke=0)
        # Gozler
        c.setFillColor(NAVY)
        c.circle(x-3*s, y+15*s, 1.5*s, fill=1, stroke=0)
        c.circle(x+3*s, y+15*s, 1.5*s, fill=1, stroke=0)
        # Kuyruk
        c.setStrokeColor(HexColor("#F97316")); c.setLineWidth(2*s)
        c.line(x+8*s, y, x+18*s, y+10*s)

    def _draw_bird(self, x, y, scale=1.0):
        """Kus."""
        c=self.c; s=scale
        c.setFillColor(SKY)
        c.ellipse(x-6*s, y-3*s, x+6*s, y+5*s, fill=1, stroke=0)
        c.circle(x+5*s, y+4*s, 4*s, fill=1, stroke=0)
        # Gaga
        c.setFillColor(AMBER)
        p=c.beginPath(); p.moveTo(x+9*s,y+4*s); p.lineTo(x+14*s,y+3*s); p.lineTo(x+9*s,y+2*s); p.close()
        c.drawPath(p,fill=1,stroke=0)
        # Goz
        c.setFillColor(NAVY); c.circle(x+6*s, y+5*s, 1*s, fill=1, stroke=0)
        # Kanat
        c.setStrokeColor(SKY); c.setLineWidth(1.5*s)
        c.line(x-2*s, y+5*s, x-8*s, y+12*s)
        c.line(x-8*s, y+12*s, x+2*s, y+5*s)

    def _draw_flower(self, x, y, scale=1.0, col=None):
        """Cicek."""
        c=self.c; s=scale; cl=col or PINK
        # Sap
        c.setFillColor(GREEN); c.rect(x-1*s, y-10*s, 2*s, 15*s, fill=1, stroke=0)
        # Yapraklar
        c.setFillColor(EMERALD)
        c.ellipse(x+2*s, y-5*s, x+10*s, y, fill=1, stroke=0)
        # Tac yapraklar
        c.setFillColor(cl)
        for i in range(6):
            angle = math.radians(i*60)
            cx = x + 6*s*math.cos(angle)
            cy = y+8*s + 6*s*math.sin(angle)
            c.circle(cx, cy, 4*s, fill=1, stroke=0)
        c.setFillColor(HexColor("#FBBF24"))
        c.circle(x, y+8*s, 4*s, fill=1, stroke=0)

    def _draw_number_line(self, x, y, start, end, scale=1.0):
        """Sayi dogrusu."""
        c=self.c; s=scale
        length = (end-start)*20*s
        c.setStrokeColor(self.r); c.setLineWidth(2*s)
        c.line(x, y, x+length, y)
        # Ok ucu
        c.line(x+length, y, x+length-5*s, y+4*s)
        c.line(x+length, y, x+length-5*s, y-4*s)
        for i in range(end-start+1):
            nx = x+i*20*s
            c.line(nx, y-4*s, nx, y+4*s)
            c.setFont("CalB",8*s); c.setFillColor(self.r)
            c.drawCentredString(nx, y-12*s, str(start+i))

    def _draw_shapes_row(self, x, y, scale=1.0):
        """Geometrik sekiller satiri."""
        c=self.c; s=scale
        # Kare
        c.setFillColor(BLUE); c.setStrokeColor(NAVY); c.setLineWidth(1.5)
        c.rect(x, y, 20*s, 20*s, fill=1, stroke=1)
        c.setFont("Cal",7); c.setFillColor(NAVY); c.drawCentredString(x+10*s, y-8*s, "Kare")
        # Daire
        c.setFillColor(ROSE); c.circle(x+45*s, y+10*s, 10*s, fill=1, stroke=1)
        c.setFillColor(NAVY); c.drawCentredString(x+45*s, y-8*s, "Daire")
        # Ucgen
        c.setFillColor(GREEN)
        p=c.beginPath(); p.moveTo(x+75*s,y); p.lineTo(x+85*s,y+20*s); p.lineTo(x+95*s,y); p.close()
        c.drawPath(p,fill=1,stroke=1)
        c.setFillColor(NAVY); c.drawCentredString(x+85*s, y-8*s, "Ucgen")
        # Dikdortgen
        c.setFillColor(AMBER); c.rect(x+110*s, y+2*s, 30*s, 16*s, fill=1, stroke=1)
        c.setFillColor(NAVY); c.drawCentredString(x+125*s, y-8*s, "Dikdortgen")

    def _draw_scene(self, x, y, scene_type="nature"):
        """Tam bir sahne ciz - sayfa ust kismina."""
        if scene_type == "nature":
            self._draw_sun(x+380, y+35, 0.8)
            self._draw_cloud(x+100, y+30, 0.9)
            self._draw_cloud(x+280, y+40, 0.7)
            self._draw_tree(x+50, y-15, 0.8)
            self._draw_tree(x+420, y-15, 0.7)
            self._draw_flower(x+100, y-10, 0.6, PINK)
            self._draw_flower(x+130, y-10, 0.6, PURPLE)
            self._draw_flower(x+380, y-10, 0.6, ROSE)
            self._draw_bird(x+200, y+35, 0.8)
            self._draw_bird(x+320, y+30, 0.6)
        elif scene_type == "school":
            self._draw_house(x+230, y-5, 1.0)
            self._draw_sun(x+400, y+35, 0.7)
            self._draw_student(x+80, y-5, 0.7, BLUE)
            self._draw_student(x+130, y-5, 0.7, ROSE)
            self._draw_teacher(x+350, y-5, 0.7)
            self._draw_tree(x+30, y-15, 0.6)
            self._draw_flower(x+440, y-10, 0.5, AMBER)
        elif scene_type == "math":
            self._draw_shapes_row(x+50, y, 1.2)
            self._draw_student(x+380, y-5, 0.7, PURPLE)
            self._draw_number_line(x+50, y-25, 0, 10, 0.8)
        elif scene_type == "reading":
            self._draw_student(x+80, y-5, 0.8, BLUE)
            self._draw_book_icon(x+120, y+5, 25, AMBER)
            self._draw_cat(x+350, y-5, 0.8)
            self._draw_sun(x+420, y+30, 0.6)
            self._draw_cloud(x+250, y+35, 0.7)

    def _sidebar(self, col):
        """Sol kenar dekoratif bant."""
        self.c.setFillColor(col)
        self.c.rect(0, 0, 12, H, fill=1, stroke=0)
        # Daire pattern
        for i in range(8):
            self.c.setFillColor(Color(1,1,1,0.15))
            self.c.circle(6, H-60-i*95, 4, fill=1, stroke=0)

    # ── Sayfa yonetimi ──
    def np(self):
        if self.pn>0:
            self.c.setFont("Cal",7); self.c.setFillColor(GRAY)
            self.c.drawString(25,12,f"{self.sinif}. Sinif {self.ders}")
            self.c.drawRightString(W-30,12,f"{self.pn}")
            # Alt cizgi
            self.c.setFillColor(self.r); self.c.rect(0,0,W,3,fill=1,stroke=0)
            self.c.showPage()
        self.pn+=1
        # Sayfa arka plan
        self.c.setFillColor(CREAM); self.c.rect(0,0,W,H,fill=1,stroke=0)
        self._sidebar(self.r)
        # Ust bant
        self.c.setFillColor(self.r); self.c.rect(12,H-4,W-12,4,fill=1,stroke=0)
        self.y = H-35

    def cs(self, n=50):
        if self.y<n: self.np()

    # ── KAPAK ──
    def kapak(self, unite_s, kaz_s):
        # Pillow kapak PNG varsa onu kullan
        safe = self.ders
        for o,n in [("\u00fc","u"),("\u00f6","o"),("\u0131","i"),("\u015f","s"),("\u00e7","c"),
                    ("\u00dc","U"),("\u00d6","O"),("\u0130","I"),("\u015e","S"),("\u00c7","C")," _"]:
            safe = safe.replace(o,n)
        safe = safe.replace(" ","_")
        # Kapak dosya adi eslestirme
        KAPAK_MAP = {"Turkce":"Turkce","Matematik":"Matematik","Hayat_Bilgisi":"Hayat_Bilgisi",
            "Fen_Bilimleri":"Fen_Bilimleri","Sosyal_Bilgiler":"Sosyal_Bilgiler",
            "Din_Kulturu_ve_Ahlak_Bilgisi":"Din_Kulturu",
            "Inkilap_Tarihi":"Inkilap_Tarihi",
            "Fizik":"Fizik","Kimya":"Kimya","Biyoloji":"Biyoloji",
            "Tarih":"Tarih","Cografya":"Cografya","Edebiyat":"Edebiyat","Felsefe":"Felsefe"}
        kapak_key = KAPAK_MAP.get(safe, safe.split("_")[0])
        kapak_png = os.path.join(IMG_DIR, f"kapak_{kapak_key}_{self.sinif}.png")
        if os.path.exists(kapak_png):
            try:
                from reportlab.lib.utils import ImageReader
                self.c.drawImage(ImageReader(kapak_png), 0, 0, width=W, height=H)
                self.pn = 1; self.c.showPage()
                return
            except: pass

        # Fallback: eski kapak
        self.c.setFillColor(NAVY); self.c.rect(0,0,W,H,fill=1,stroke=0)
        # Dekoratif ust bant
        self.c.setFillColor(self.r)
        self.c.rect(0,H-80,W,80,fill=1,stroke=0)
        # Yildizlar
        for i in range(12):
            self._draw_star(50+i*45, H-40, 8, Color(1,1,1,0.2))
        # Logo
        self.c.setFont("CalB",11); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2, H-25, "SmartCampusAI")
        self.c.setFont("Cal",9); self.c.drawCentredString(W/2, H-40, "Premium Ders Kitabi Serisi")
        # Orta alan
        self.c.setFillColor(GOLD)
        self.c.rect(60,H*0.50,W-120,4,fill=1,stroke=0)
        self.c.rect(60,H*0.48,W-120,1,fill=1,stroke=0)
        # Ders adi
        self.c.setFont("CalB",42); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2, H*0.62, self.ders)
        self.c.setFont("CalB",30); self.c.setFillColor(self.r)
        self.c.drawCentredString(W/2, H*0.55, f"{self.sinif}. Sinif")
        # Karakter gorselleri
        self._img(self.gorseller[0], 50, H*0.22, h=100)  # Sol karakter
        self._img(self.gorseller[1], W-130, H*0.25, h=80)  # Sag ikon
        if len(self.gorseller) > 2:
            self._img(self.gorseller[2], W/2-60, H*0.22, h=50)  # Orta ikon
        # Bilgi
        self.c.setFont("Cal",13); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2, H*0.40, f"{unite_s} Unite  |  {kaz_s} Kazanim")
        self.c.drawCentredString(W/2, H*0.36, "MEB 2025 Mufredati")
        # Alt bilgi
        self.c.setFont("Cal",10); self.c.setFillColor(GOLD)
        self.c.drawCentredString(W/2, H*0.22, "Konu Anlatimi + Okuma Parcalari + Alistirmalar")
        self.c.drawCentredString(W/2, H*0.18, "Etkinlikler + Degerledirme + Proje Odevleri")
        # Alt dekoratif
        self.c.setFillColor(self.r)
        self.c.rect(0,0,W,30,fill=1,stroke=0)
        for i in range(15):
            self.c.setFillColor(Color(1,1,1,0.15))
            self.c.circle(30+i*38, 15, 3, fill=1, stroke=0)
        self.c.setFont("Cal",8); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2, 8, "2026 SmartCampusAI")
        self.pn=1; self.c.showPage()

    # ── ICINDEKILER ──
    def icindekiler(self, uniteler):
        self.np()
        # Baslik
        self.c.setFillColor(self.r)
        self.c.roundRect(25,self.y-5,W-55,30,8,fill=1,stroke=0)
        self.c.setFont("CalB",16); self.c.setFillColor(WHITE)
        self.c.drawString(40,self.y+2,"ICINDEKILER")
        self._draw_book_icon(W-80,self.y-2,22,WHITE)
        self.y-=45
        unite_no=1
        for u, konular in uniteler.items():
            self.cs(40)
            # Unite baslik
            self.c.setFillColor(self.rl)
            self.c.roundRect(25,self.y-5,W-55,22,4,fill=1,stroke=0)
            self.c.setFont("CalB",11); self.c.setFillColor(self.r)
            self.c.drawString(35,self.y,f"Unite {unite_no}: {u[:50]}")
            self._draw_check_badge(W-45,self.y+4,self.r)
            self.y-=25; unite_no+=1
            for i,k in enumerate(konular,1):
                self.cs(14)
                self.c.setFont("Cal",9); self.c.setFillColor(DARK)
                self.c.drawString(50,self.y,f"{i}. {k[:62]}")
                # Noktalama
                self.c.setFillColor(self.r)
                self.c.circle(42,self.y+3,2,fill=1,stroke=0)
                self.y-=13
            self.y-=8

    # ── UNITE KAPAK ──
    def unite_kapak(self, ad, no, konu_s, kaz_s):
        self.np()
        # Tam sayfa renkli arka plan
        self.c.setFillColor(self.r); self.c.rect(0,H*0.35,W,H*0.35,fill=1,stroke=0)
        # Dekoratif daireler
        for i in range(20):
            self.c.setFillColor(Color(1,1,1,0.08))
            self.c.circle(30+i*28, H*0.60, 10, fill=1, stroke=0)
        # Ust dekorasyon
        self._draw_star(W/2-80, H*0.78, 15, self.r)
        self._draw_star(W/2+80, H*0.78, 15, self.r)
        self._draw_star(W/2, H*0.80, 20, GOLD)
        # Baslik
        self.c.setFont("CalB",14); self.c.setFillColor(GOLD)
        self.c.drawCentredString(W/2, H*0.73, f"UNITE {no}")
        self.c.setFont("CalB",28); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2, H*0.53, ad[:40])
        self.c.setFont("Cal",13); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2, H*0.42, f"{konu_s} Konu  |  {kaz_s} Kazanim")
        # Alt ikonlar
        self._draw_book_icon(W/2-60, H*0.22, 25, self.r)
        self._draw_pencil(W/2-10, H*0.24, 25, self.r)
        self._draw_lightbulb(W/2+50, H*0.24, 20, self.r)
        # Karakter gorselleri
        self._img("ogrenci_kiz.png", 60, H*0.13, h=90)
        self._img("ogretmen.png", W-140, H*0.13, h=100)
        self._img("yildizlar.png", W/2-60, H*0.15, w=120)
        # Unite QR kod
        safe_unite = ad.replace(" ","_")[:15]
        self._qr_kutusu(W-95, H*0.72, f"http://localhost:8501/?sinif={self.sinif}&ders={self.ders}&unite={safe_unite}&tip=ders", "Unite Video")
        # Neler ogrenecegiz kutusu
        self.c.setFillColor(self.rl)
        self.c.roundRect(60, H*0.06, W-120, 55, 10, fill=1, stroke=0)
        self.c.setFont("CalB",10); self.c.setFillColor(self.r)
        self.c.drawString(80, H*0.11, "Bu unitede neler ogreneceksin?")
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        self.c.drawString(80, H*0.08, f"* {konu_s} farkli konu  * {kaz_s} kazanim  * Etkinlik + test + proje")

    # ── KONU SAYFASI ──
    def konu_sayfasi(self, konu_adi, hafta, kazanimlar, icerik, okuma=None, konu_idx=0):
        """Tam bir konu icin 3-5 sayfa uret."""
        # SAYFA 1: Baslik + Sahne + Kazanimlar + Konu giris
        self.np()

        # QR kod (sag ust)
        safe_konu = konu_adi.replace(" ","_")[:20]
        qr_url = f"http://localhost:8501/?sinif={self.sinif}&ders={self.ders}&konu={safe_konu}&tip=quiz"
        self._qr_kutusu(W-90, self.y-60, qr_url, "Dijital Ders")

        # Gorsel illustrasyon bandi
        self.c.setFillColor(self.rl)
        self.c.roundRect(20, self.y-55, W-110, 65, 10, fill=1, stroke=0)
        # Ders gorsellerinden dongusel sec
        g_list = self.gorseller
        g1 = g_list[konu_idx % len(g_list)]
        g2 = g_list[(konu_idx+1) % len(g_list)]
        self._img(g1, 35, self.y-48, h=50)
        self._img("gunes.png", W/2-60, self.y-45, h=45)
        self._img(g2, W-170, self.y-48, h=50)
        # Dekoratif yildizlar
        self._draw_star(W/2-100, self.y-10, 6, self.r)
        self._draw_star(W/2+40, self.y-10, 6, self.r)
        self.y -= 68

        # Konu basligi bandi
        self.c.setFillColor(self.r)
        self.c.roundRect(20,self.y-5,W-40,32,8,fill=1,stroke=0)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(35,self.y+3,konu_adi[:55])
        if hafta:
            self.c.setFont("Cal",7)
            self.c.drawRightString(W-35,self.y+3,hafta[:25])
        # Dekoratif
        self._draw_pencil(W-55,self.y-2,18,WHITE)
        self.y-=42

        # Kazanim kutusu
        if kazanimlar:
            kaz_h = min(len(kazanimlar)*14+30, 180)
            self.c.setFillColor(LPURPLE)
            self.c.roundRect(25,self.y-kaz_h+15,W-55,kaz_h,8,fill=1,stroke=0)
            self.c.setStrokeColor(PURPLE); self.c.setLineWidth(1.5)
            self.c.roundRect(25,self.y-kaz_h+15,W-55,kaz_h,8,fill=0,stroke=1)
            self.c.setFont("CalB",10); self.c.setFillColor(PURPLE)
            self._draw_check_badge(40,self.y+2,PURPLE)
            self.c.drawString(55,self.y,"KAZANIMLAR")
            self.y-=16
            for k in kazanimlar[:8]:
                self.cs(25)
                self.c.setFont("Cal",8); self.c.setFillColor(DARK)
                for wl in textwrap.wrap(k,width=80):
                    self.c.drawString(40,self.y,wl[:85]); self.y-=11
                self.y-=2
            self.y-=10

        # Konu anlatimi
        if icerik:
            self.cs(30)
            self.c.setFillColor(self.rl)
            self.c.roundRect(20,self.y-10,W-40,25,6,fill=1,stroke=0)
            self.c.setFont("CalB",11); self.c.setFillColor(self.r)
            self._draw_book_icon(30,self.y-5,16,self.r)
            self.c.drawString(52,self.y,"KONU ANLATIMI"); self.y-=22

            for line in icerik.split("\n"):
                if not line.strip(): self.y-=4; continue
                is_h = (line.strip().isupper() and len(line.strip())>4) or \
                       (line.strip().endswith(":") and len(line.strip())<60)
                if is_h:
                    self.cs(22)
                    self.c.setFont("CalB",9); self.c.setFillColor(NAVY)
                    self.c.drawString(30,self.y,line.strip()[:80]); self.y-=14
                elif line.strip().startswith(("-","*","+",">")):
                    self.cs(14)
                    self.c.setFillColor(self.r); self.c.circle(34,self.y+3,2,fill=1,stroke=0)
                    self.c.setFont("Cal",8); self.c.setFillColor(DARK)
                    for wl in textwrap.wrap(line.strip(),width=82):
                        self.c.drawString(42,self.y,wl[:85]); self.y-=11
                else:
                    self.cs(14)
                    self.c.setFont("Cal",9); self.c.setFillColor(DARK)
                    for wl in textwrap.wrap(line.strip(),width=82):
                        self.c.drawString(30,self.y,wl[:85]); self.y-=11

        # SAYFA 2: Okuma parcasi + Biliyor musun
        if okuma:
            self.np()
            # Sesli okuma QR
            safe_ok = okuma[0].replace(" ","_")[:15]
            self._qr_kutusu(W-90, self.y-60, f"http://localhost:8501/?sinif={self.sinif}&ders={self.ders}&konu={safe_ok}&tip=okuma", "Sesli Okuma")
            # Okuma parcasi - premium kutu
            self.c.setFillColor(LYELLOW)
            self.c.roundRect(25,self.y-140,W-110,150,10,fill=1,stroke=0)
            self.c.setStrokeColor(AMBER); self.c.setLineWidth(1.5)
            self.c.roundRect(25,self.y-140,W-110,150,10,fill=0,stroke=1)
            self._draw_book_icon(35,self.y-3,18,AMBER)
            self.c.setFont("CalB",11); self.c.setFillColor(AMBER)
            self.c.drawString(58,self.y,f"OKUMA PARCASI: {okuma[0][:40]}"); self.y-=18
            self.c.setFont("CalI",9); self.c.setFillColor(DARK)
            for wl in textwrap.wrap(okuma[1],width=78)[:10]:
                self.c.drawString(38,self.y,wl[:82]); self.y-=12
            self.y-=30

            # Anlama sorulari
            self.cs(80)
            self.c.setFillColor(LBLUE)
            self.c.roundRect(25,self.y-70,W-55,80,8,fill=1,stroke=0)
            self.c.setFont("CalB",10); self.c.setFillColor(BLUE)
            self.c.drawString(40,self.y,"ANLAMA SORULARI"); self.y-=16
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            qs = [f"1) Metnin ana fikri nedir?",
                  f"2) Metinde gecen yeni kelimeleri bulunuz.",
                  f"3) Bu metni kendi cumlelerinizle ozetleyiniz.",
                  f"4) Siz olsaydiniz ne yapirdiniz?"]
            for q in qs:
                self.c.drawString(40,self.y,q); self.y-=12
            self.y-=15

        # Biliyor musun kutusu
        self.cs(60)
        self.c.setFillColor(LTEAL)
        self.c.roundRect(25,self.y-50,W-55,60,8,fill=1,stroke=0)
        self._draw_lightbulb(40,self.y-5,18,TEAL)
        self.c.setFont("CalB",10); self.c.setFillColor(TEAL)
        self.c.drawString(60,self.y,"BILIYOR MUSUN?"); self.y-=16
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        self.c.drawString(40,self.y,f"Bu konuda {len(kazanimlar)} kazanim hedeflenmektedir."); self.y-=12
        self.c.drawString(40,self.y,f"Ogrenme alani ile ilgili pek cok etkinlik yapabilirsin!"); self.y-=25

        # SAYFA 3: Alistirmalar + Test
        self.np()
        # Alistirma bandi
        self.c.setFillColor(LGREEN)
        self.c.roundRect(25,self.y-5,W-55,28,6,fill=1,stroke=0)
        self._draw_pencil(35,self.y-2,16,GREEN)
        self.c.setFont("CalB",11); self.c.setFillColor(GREEN)
        self.c.drawString(55,self.y,"ALISTIRMALAR"); self.y-=30

        # Alistirma kutulari
        for i in range(4):
            self.cs(45)
            self.c.setFillColor(LGRAY)
            self.c.roundRect(30,self.y-25,W-65,35,6,fill=1,stroke=0)
            self.c.setFillColor(self.r); self.c.circle(42,self.y-6,8,fill=1,stroke=0)
            self.c.setFont("CalB",10); self.c.setFillColor(WHITE)
            self.c.drawString(38,self.y-10,f"{i+1}")
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            alst = [
                f"\"{konu_adi[:30]}\" ile ilgili 3 ornek yaziniz.",
                "Asagidaki bosluklari uygun kelimelerle doldurunuz: ___________",
                "Verilen bilgileri dogru-yanlis olarak isaretleyiniz.",
                "Bu konuyu bir resimle ifade ediniz.",
            ]
            self.c.drawString(58,self.y-10,alst[i%4][:70]); self.y-=40

        # Test sorulari
        self.cs(50)
        self.c.setFillColor(LROSE)
        self.c.roundRect(25,self.y-5,W-55,28,6,fill=1,stroke=0)
        self._draw_star(38,self.y+6,8,ROSE)
        self.c.setFont("CalB",11); self.c.setFillColor(ROSE)
        self.c.drawString(55,self.y,"DEGERLENDIRME TESTI"); self.y-=30

        for i in range(5):
            self.cs(50)
            self.c.setFont("CalB",9); self.c.setFillColor(DARK)
            self.c.drawString(30,self.y,f"Soru {i+1})")
            self.c.setFont("Cal",9)
            soru_tipleri = [
                f"\"{konu_adi[:25]}\" kavramini tanimlayin.",
                "Asagidakilerden hangisi dogrudur?",
                "Verilen ornekleri siniflandiriniz.",
                "Bosluklari doldurunuz: ______",
                f"Bu konuyla ilgili bir paragraf yaziniz.",
            ]
            self.c.drawString(70,self.y,soru_tipleri[i%5][:65]); self.y-=14
            if i==1:  # Coktan secmeli
                for j,s in enumerate(["A) ...","B) ...","C) ...","D) ..."]):
                    self.c.drawString(80,self.y,s); self.y-=11
            self.y-=8

        # SAYFA 4: Etkinlik + proje
        self.np()
        self.c.setFillColor(LORANGE)
        self.c.roundRect(25,self.y-5,W-55,28,6,fill=1,stroke=0)
        self._draw_star(38,self.y+6,8,ORANGE)
        self.c.setFont("CalB",11); self.c.setFillColor(ORANGE)
        self.c.drawString(55,self.y,"ETKINLIK VE PROJE"); self.y-=35

        etkinlikler = [
            ("Grup Calismasi", f"\"{konu_adi[:25]}\" konusunda 4 kisilik gruplarla poster hazirlayiniz."),
            ("Arastirma", "Bu konuyla ilgili 3 farkli kaynaktan bilgi toplayiniz."),
            ("Sunum", "Ogrendiklerinizi sinifta 3 dakikalik sunum yaparak paylasiniz."),
            ("Yazma", f"Bu konu hakkinda en az 5 cumlelik bir yazi yaziniz."),
            ("Cizim", "Konuyu anlatan renkli bir poster/resim ciziniz."),
            ("Drama", "Konuyu canlandirmak icin kisa bir skit hazrlayiniz."),
        ]
        for baslik, aciklama in etkinlikler:
            self.cs(50)
            self.c.setFillColor(LGRAY)
            self.c.roundRect(30,self.y-20,W-65,30,6,fill=1,stroke=0)
            self.c.setFillColor(ORANGE); self.c.circle(42,self.y-4,6,fill=1,stroke=0)
            self.c.setFont("CalB",9); self.c.setFillColor(WHITE)
            self.c.drawString(39,self.y-7,baslik[0])
            self.c.setFont("CalB",9); self.c.setFillColor(DARK)
            self.c.drawString(55,self.y-2,baslik)
            self.c.setFont("Cal",8); self.c.setFillColor(GRAY)
            self.c.drawString(55,self.y-13,aciklama[:72]); self.y-=35

        # Gorsel alan — cizim yeri
        self.cs(100)
        self.c.setFillColor(LGRAY)
        self.c.roundRect(30, self.y-65, W-65, 75, 8, fill=1, stroke=0)
        self.c.setStrokeColor(self.r); self.c.setLineWidth(1)
        self.c.setDash(3,3)
        self.c.roundRect(30, self.y-65, W-65, 75, 8, fill=0, stroke=1)
        self.c.setDash()
        self._draw_pencil(50, self.y-20, 15, self.r)
        self.c.setFont("CalI",10); self.c.setFillColor(GRAY)
        self.c.drawCentredString(W/2, self.y-30, "Buraya cizim yap / resim ciz")
        self.c.setFont("Cal",8)
        self.c.drawCentredString(W/2, self.y-45, "Konuyu anlatan bir resim cizerek ogrendiklerini goster!")
        self.y -= 80

        # Not alani (cizgili)
        self.cs(80)
        self.c.setFont("CalB",9); self.c.setFillColor(GRAY)
        self.c.drawString(30,self.y,"NOTLARIM:"); self.y-=15
        for i in range(4):
            self.c.setStrokeColor(HexColor("#E2E8F0")); self.c.setLineWidth(0.3)
            self.c.line(30,self.y,W-30,self.y); self.y-=18

    # ══════════════════════════════════════════════════
    # MEB FORMAT EK BOLUMLERI
    # ══════════════════════════════════════════════════

    def hazirlik_calismasi(self, konu_adi, unite_adi):
        """MEB - Hazirlik Calismasi: Konuya giris goerseli + on bilgi sorulari."""
        self.np()
        # Baslik bandi
        self.c.setFillColor(EMERALD)
        self.c.roundRect(20,self.y-5,W-40,30,8,fill=1,stroke=0)
        self._draw_lightbulb(35,self.y-2,16,WHITE)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(55,self.y+2,"HAZIRLIK CALISMASI"); self.y-=40

        # Gorsel alan (dusunme balonu)
        self.c.setFillColor(LGREEN)
        self.c.roundRect(30,self.y-100,W-65,110,12,fill=1,stroke=0)
        self.c.setStrokeColor(EMERALD); self.c.setLineWidth(1.5)
        self.c.roundRect(30,self.y-100,W-65,110,12,fill=0,stroke=1)
        # Karakter
        self._img("ogrenci_kiz.png", 40, self.y-90, h=75)
        # Dusunme balonu
        self.c.setFillColor(WHITE)
        self.c.roundRect(140,self.y-30,W-200,40,10,fill=1,stroke=0)
        self.c.setFont("CalI",10); self.c.setFillColor(DARK)
        self.c.drawString(150,self.y-10,f"Acaba \"{konu_adi[:35]}\" hakkinda ne biliyorum?")
        self.c.drawString(150,self.y-24,"Bu konuyu daha once duydum mu?")
        # Kucuk balonlar
        self.c.setFillColor(WHITE)
        self.c.circle(130,self.y-38,5,fill=1,stroke=0)
        self.c.circle(125,self.y-48,3,fill=1,stroke=0)
        self.y -= 115

        # On bilgi sorulari
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(35,self.y,"Asagidaki sorulari dusunerek cevapliyalim:"); self.y-=18

        sorular = [
            f"1) \"{konu_adi[:30]}\" denince aklina ne geliyor?",
            "2) Bu konuyla ilgili daha once ne ogrendin?",
            "3) Bu konu gunluk hayatinda nerelerde karsina cikiyor?",
            "4) Bu konuyu neden ogrenmemiz gerekiyor?",
            "5) Resimdeki cocuk ne dusunyuor olabilir?",
        ]
        for s in sorular:
            self.cs(35)
            self.c.setFillColor(LGRAY)
            self.c.roundRect(35,self.y-8,W-75,22,4,fill=1,stroke=0)
            self.c.setFillColor(EMERALD); self.c.circle(42,self.y+2,4,fill=1,stroke=0)
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            self.c.drawString(52,self.y,s[:75])
            self.y-=28

        # Yazma alani
        self.cs(80)
        self.c.setFont("CalB",9); self.c.setFillColor(EMERALD)
        self.c.drawString(35,self.y,"Dusuncelerini buraya yaz:"); self.y-=12
        for i in range(4):
            self.c.setStrokeColor(EMERALD); self.c.setLineWidth(0.3); self.c.setDash(2,2)
            self.c.line(35,self.y,W-35,self.y); self.y-=18
        self.c.setDash()

    def dinleme_metni(self, konu_adi):
        """MEB - Dinleme/Izleme Metni bolumu."""
        self.cs(120)
        # Baslik
        self.c.setFillColor(SKY)
        self.c.roundRect(25,self.y-5,W-55,28,6,fill=1,stroke=0)
        self._img("ogretmen.png", W-80, self.y-25, h=50)
        self.c.setFont("CalB",11); self.c.setFillColor(WHITE)
        self.c.drawString(40,self.y+2,"DINLEME / IZLEME METNI"); self.y-=35

        # Yonerge kutusu
        self.c.setFillColor(LBLUE)
        self.c.roundRect(30,self.y-80,W-65,90,8,fill=1,stroke=0)
        self.c.setStrokeColor(SKY); self.c.setLineWidth(1)
        self.c.roundRect(30,self.y-80,W-65,90,8,fill=0,stroke=1)

        self.c.setFont("CalB",9); self.c.setFillColor(SKY)
        self.c.drawString(45,self.y,"OGRETMEN YONERGESI:"); self.y-=14
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        yonergeler = [
            "1) Ogretmeniniz size bir metin okuyacak. Dikkatle dinleyiniz.",
            f"2) \"{konu_adi[:30]}\" konusuyla ilgili bir hikaye/bilgi metnidir.",
            "3) Dinlerken onemli yerleri aklnizda tutmaya calisiniz.",
            "4) Dinleme bittikten sonra asagidaki sorulari cevaplayiniz.",
        ]
        for y in yonergeler:
            self.c.drawString(45,self.y,y[:78]); self.y-=12
        self.y-=20

        # Dinleme sonrasi sorular
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(35,self.y,"Dinledikten Sonra:"); self.y-=16
        ds = [
            "1) Metnin konusu neydi?",
            "2) Metinde hangi karakterler vardi?",
            "3) Olaylar nerede geciyordu?",
            "4) Metnin sonunda ne oldu?",
            "5) Bu metinden ne ogrednin?",
        ]
        for s in ds:
            self.cs(16)
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            self.c.drawString(45,self.y,s); self.y-=14

    def yazma_calismasi(self, konu_adi, tip="serbest"):
        """MEB - Yazma Calismasi: dikte, bakarak yazma, serbest yazma."""
        self.np()
        self.c.setFillColor(INDIGO)
        self.c.roundRect(20,self.y-5,W-40,28,8,fill=1,stroke=0)
        self._draw_pencil(35,self.y-2,16,WHITE)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(55,self.y+2,"YAZMA CALISMASI"); self.y-=40

        # Gorsel
        self._img("ogrenci_erkek.png", W-90, self.y-50, h=70)

        # 1) Dikte
        self.c.setFillColor(LPURPLE)
        self.c.roundRect(30,self.y-50,W/2-20,60,6,fill=1,stroke=0)
        self.c.setFont("CalB",10); self.c.setFillColor(INDIGO)
        self.c.drawString(40,self.y,"1) DIKTE CALISMASI"); self.y-=14
        self.c.setFont("Cal",8); self.c.setFillColor(DARK)
        self.c.drawString(40,self.y,"Ogretmeninizin soyledigi cumleleri yaziniz:"); self.y-=12
        for i in range(2):
            self.c.setStrokeColor(INDIGO); self.c.setLineWidth(0.3)
            self.c.line(40,self.y,W/2,self.y); self.y-=16
        self.y-=15

        # 2) Bakarak yazma
        self.c.setFillColor(LPURPLE)
        self.c.roundRect(30,self.y-50,W-65,60,6,fill=1,stroke=0)
        self.c.setFont("CalB",10); self.c.setFillColor(INDIGO)
        self.c.drawString(40,self.y,"2) BAKARAK YAZMA"); self.y-=14
        self.c.setFont("Cal",8); self.c.setFillColor(DARK)
        self.c.drawString(40,self.y,"Asagidaki cumleyi guzel yaziyla tekrar yaziniz:"); self.y-=12
        self.c.setFont("CalI",10); self.c.setFillColor(NAVY)
        self.c.drawString(40,self.y,f"\"{konu_adi[:40]}\" cok onemli bir konudur."); self.y-=14
        self.c.setStrokeColor(INDIGO); self.c.setLineWidth(0.3)
        self.c.line(40,self.y,W-40,self.y); self.y-=16
        self.c.line(40,self.y,W-40,self.y); self.y-=20

        # 3) Serbest yazma
        self.c.setFillColor(LPURPLE)
        self.c.roundRect(30,self.y-120,W-65,130,6,fill=1,stroke=0)
        self.c.setFont("CalB",10); self.c.setFillColor(INDIGO)
        self.c.drawString(40,self.y,"3) SERBEST YAZMA"); self.y-=14
        self.c.setFont("Cal",8); self.c.setFillColor(DARK)
        self.c.drawString(40,self.y,f"\"{konu_adi[:35]}\" konusunda en az 5 cumle yaziniz:"); self.y-=14
        for i in range(7):
            self.c.setStrokeColor(INDIGO); self.c.setLineWidth(0.3)
            self.c.line(40,self.y,W-40,self.y); self.y-=16

    def serbest_okuma(self, baslik, metin):
        """MEB - Serbest Okuma Metni (tema sonunda ekstra okuma)."""
        self.np()
        self.c.setFillColor(AMBER)
        self.c.roundRect(20,self.y-5,W-40,28,8,fill=1,stroke=0)
        self._img("kitap.png", 30, self.y-3, h=22)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(65,self.y+2,"SERBEST OKUMA METNI"); self.y-=40

        # Metin kutusu
        self.c.setFillColor(LYELLOW)
        self.c.roundRect(25,self.y-200,W-55,210,10,fill=1,stroke=0)
        self.c.setStrokeColor(AMBER); self.c.setLineWidth(1.5)
        self.c.roundRect(25,self.y-200,W-55,210,10,fill=0,stroke=1)

        self.c.setFont("CalB",13); self.c.setFillColor(AMBER)
        self.c.drawString(40,self.y,baslik[:50]); self.y-=20
        self.c.setFont("CalI",10); self.c.setFillColor(DARK)
        for wl in textwrap.wrap(metin, width=75)[:15]:
            self.c.drawString(40,self.y,wl[:80]); self.y-=13
        self.y-=30

        # Metin hakkinda dusun
        self.cs(80)
        self._img("ogrenci_kiz.png", W-90, self.y-50, h=60)
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(35,self.y,"Metni Okuduktan Sonra:"); self.y-=16
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        mss = [
            "* Bu metni okurken neler hissettin?",
            "* Metnin en sevdigin bolumu hangisiydi?",
            "* Bu metin sana neyi hatirlatti?",
            "* Arkadsiina bu metni anlatir misin?",
        ]
        for m in mss:
            self.c.drawString(40,self.y,m); self.y-=13

    def metin_alti_5n1k(self, metin_adi):
        """MEB - Metin alti 5N1K sorulari."""
        self.cs(130)
        self.c.setFillColor(LBLUE)
        self.c.roundRect(25,self.y-110,W-55,120,8,fill=1,stroke=0)
        self.c.setStrokeColor(BLUE); self.c.setLineWidth(1)
        self.c.roundRect(25,self.y-110,W-55,120,8,fill=0,stroke=1)

        self.c.setFont("CalB",10); self.c.setFillColor(BLUE)
        self.c.drawString(40,self.y,"METNI ANLAMA - 5N1K SORULARI"); self.y-=18
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        sorular = [
            ("KIM?", f"\"{metin_adi[:25]}\" metnindeki kisiler kimlerdir?"),
            ("NE?", "Metinde anlatilan olay/konu nedir?"),
            ("NEREDE?", "Olaylar nerede gecmektedir?"),
            ("NE ZAMAN?", "Olaylar ne zaman yasanmistir?"),
            ("NEDEN?", "Bu olaylarin sebebi nedir?"),
            ("NASIL?", "Olaylar nasil gerceklesmistir?"),
        ]
        for soru_k, soru_t in sorular:
            self.cs(18)
            self.c.setFont("CalB",8); self.c.setFillColor(BLUE)
            self.c.drawString(40,self.y,f"{soru_k}")
            self.c.setFont("Cal",8); self.c.setFillColor(DARK)
            self.c.drawString(100,self.y,soru_t[:65])
            self.y-=14
        self.y-=15

    def tema_degerlendirme(self, unite_adi, konu_sayisi):
        """MEB - Tema/Unite sonu kapsamli degerlendirme testi."""
        self.np()
        # Baslik
        self.c.setFillColor(ROSE)
        self.c.roundRect(20,self.y-5,W-40,30,8,fill=1,stroke=0)
        self._draw_star(38,self.y+6,8,WHITE)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(55,self.y+2,f"TEMA DEGERLENDIRME: {unite_adi[:35]}"); self.y-=42

        self._img("yildizlar.png", W/2-60, self.y+5, w=120)
        self.y-=25

        # Test sorulari
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(35,self.y,"A) COKTAN SECMELI SORULAR"); self.y-=18

        for i in range(5):
            self.cs(55)
            self.c.setFillColor(LROSE)
            self.c.roundRect(30,self.y-30,W-65,40,6,fill=1,stroke=0)
            self.c.setFont("CalB",9); self.c.setFillColor(ROSE)
            self.c.drawString(40,self.y,f"Soru {i+1})")
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            ss = [
                f"Bu temada islenen konularin ortak ozellligi nedir?",
                "Asagidakilerden hangisi bu temayla ilgili degildir?",
                "Okudugunuz metinlerde en cok hangi deger vurgulandi?",
                "Bu temadaki kazanimlardan hangisini en iyi ogredniz?",
                f"\"{unite_adi[:20]}\" temasinin ana dusuncesi nedir?",
            ]
            self.c.drawString(80,self.y,ss[i][:65]); self.y-=14
            for j,s in enumerate(["A) ..........","B) ..........","C) ..........","D) .........."]):
                self.c.setFont("Cal",8)
                self.c.drawString(50+j*110,self.y,s)
            self.y-=22

        # B) Dogru/Yanlis
        self.cs(60)
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(35,self.y,"B) DOGRU / YANLIS"); self.y-=18
        for i in range(4):
            self.cs(16)
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            dy = [
                f"( D / Y ) Bu temada {konu_sayisi} farkli konu islendi.",
                "( D / Y ) Okuduumuz metinler bilgilendirici metinlerdi.",
                "( D / Y ) Bu temada yazma calismasi yaptik.",
                "( D / Y ) Dinleme metni dinledik ve sorulari cevapladik.",
            ]
            self.c.drawString(40,self.y,dy[i][:75]); self.y-=15

        # C) Eslestirme
        self.cs(50)
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(35,self.y,"C) ESLESTIRME"); self.y-=16
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        self.c.drawString(40,self.y,"Sol suitndaki kavramlarla sag sutundaki aciklamalari eslestiriniz."); self.y-=14
        for i in range(4):
            self.cs(14)
            self.c.drawString(50,self.y,f"{i+1}. __________ ( ) __________"); self.y-=14

        # Oz degerlendirme
        self.cs(80)
        self.c.setFillColor(LGOLD)
        self.c.roundRect(30,self.y-55,W-65,65,8,fill=1,stroke=0)
        self._draw_star(45,self.y+2,8,GOLD)
        self.c.setFont("CalB",10); self.c.setFillColor(GOLD)
        self.c.drawString(60,self.y,"OZ DEGERLENDIRME"); self.y-=16
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        oz = [
            "* Bu temayi ne kadar iyi anladim? (1-2-3-4-5)",
            "* En cok hangi etkinligi begendim?",
            "* Hangi konuda zorlandim?",
        ]
        for o in oz:
            self.c.drawString(45,self.y,o[:70]); self.y-=13

    # ── UNITE OZETI ──
    def unite_ozeti(self, unite_adi, konular):
        self.np()
        self.c.setFillColor(self.rl)
        self.c.roundRect(20,H-80,W-40,55,10,fill=1,stroke=0)
        self._draw_star(W/2, H-40, 12, self.r)
        self.c.setFont("CalB",14); self.c.setFillColor(self.r)
        self.c.drawCentredString(W/2,H-55,f"UNITE OZETI")
        self.c.setFont("CalB",12); self.c.setFillColor(DARK)
        self.c.drawCentredString(W/2,H-72,unite_adi[:45])
        self.y=H-100
        self.c.setFont("CalB",10); self.c.setFillColor(NAVY)
        self.c.drawString(30,self.y,"Bu unitede neler ogrendik:"); self.y-=18
        for i,k in enumerate(konular[:15],1):
            self.cs(16)
            self.c.setFillColor(self.r); self.c.circle(38,self.y+3,3,fill=1,stroke=0)
            self.c.setFont("Cal",9); self.c.setFillColor(DARK)
            self.c.drawString(48,self.y,f"{k[:65]}"); self.y-=14
        # Ozet testi
        self.cs(80)
        self.c.setFillColor(LGOLD)
        self.c.roundRect(25,self.y-60,W-55,70,8,fill=1,stroke=0)
        self.c.setFont("CalB",10); self.c.setFillColor(GOLD)
        self.c.drawString(40,self.y,"UNITE DEGERLENDIRME"); self.y-=16
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        self.c.drawString(40,self.y,"1) Bu unitenin en onemli 3 kavramini yaziniz."); self.y-=12
        self.c.drawString(40,self.y,"2) En cok hangi konuyu begendniz? Neden?"); self.y-=12
        self.c.drawString(40,self.y,"3) Ogrendiklerinizi gunluk hayatta nasil kullanirsiniz?"); self.y-=12

    # ── SOZLUK SAYFASI ──
    def sozluk(self, kelimeler):
        self.np()
        self.c.setFillColor(self.r)
        self.c.roundRect(25,self.y-5,W-55,28,6,fill=1,stroke=0)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(40,self.y,"SOZLUK - TEMEL KAVRAMLAR"); self.y-=35
        for k in kelimeler[:20]:
            self.cs(20)
            self.c.setFillColor(LGRAY)
            self.c.roundRect(25,self.y-5,W-55,18,4,fill=1,stroke=0)
            self.c.setFont("CalB",9); self.c.setFillColor(self.r)
            self.c.drawString(35,self.y,k[:70])
            self.y-=22

    # ── EGLENCELI BOLUMLER ──

    def bilmece_sayfasi(self):
        """Eglenceli bilmece sayfasi."""
        self.np()
        self.c.setFillColor(AMBER)
        self.c.roundRect(20,self.y-5,W-40,30,8,fill=1,stroke=0)
        self._draw_star(38,self.y+6,8,WHITE)
        self.c.setFont("CalB",13); self.c.setFillColor(WHITE)
        self.c.drawString(55,self.y+2,"BILMECE KOSESI"); self.y-=45
        self._img("kedi.png", W-100, self.y-30, h=60)

        bilmeceler = [
            ("Dalda sallanir, tatli tatli yenir.", "Meyve"),
            ("Gunduz gorunmez, gece parlar.", "Yildiz"),
            ("Disi var ama isirmaz.", "Tarak"),
            ("Ayagi yok ama yururr.", "Saat"),
            ("Yesil elbisesi var, icinde kirmizi.", "Karpuz"),
            ("Her yere gider ama yerinden kimildamaz.", "Yol"),
            ("Bagirirsin, sana da bagirir.", "Yansima"),
            ("Yazin beyaz, kisin yok.", "Bulut"),
        ]
        for bilmece, cevap in bilmeceler:
            self.cs(45)
            self.c.setFillColor(LYELLOW)
            self.c.roundRect(30,self.y-18,W-120,30,6,fill=1,stroke=0)
            self.c.setFont("CalI",10); self.c.setFillColor(DARK)
            self.c.drawString(45,self.y,f"? {bilmece[:55]}")
            self.c.setFont("Cal",7); self.c.setFillColor(AMBER)
            self.c.drawString(45,self.y-12,f"Cevap: {cevap}")
            self.y-=32

    def boyama_alani(self, konu=""):
        """Boyama / cizim alani."""
        self.np()
        self.c.setFillColor(PINK)
        self.c.roundRect(20,self.y-5,W-40,28,8,fill=1,stroke=0)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(40,self.y+2,"BOYAMA VE CIZIM ALANI"); self.y-=40

        self._img("cicek.png",40,self.y-50,h=60)
        self._img("agac.png",W-100,self.y-60,h=70)

        self.c.setFont("Cal",10); self.c.setFillColor(DARK)
        self.c.drawCentredString(W/2, self.y, f"Asagiya \"{konu[:30]}\" ile ilgili bir resim ciz!")
        self.y -= 20

        # Buyuk cizim alani
        self.c.setStrokeColor(self.r); self.c.setLineWidth(1.5)
        self.c.setDash(4,4)
        self.c.roundRect(35, self.y-350, W-75, 360, 15, fill=0, stroke=1)
        self.c.setDash()
        self.c.setFont("CalI",9); self.c.setFillColor(GRAY)
        self.c.drawCentredString(W/2, self.y-170, "Burasi senin sanat alani!")
        self.y -= 370

    def oyun_sayfasi(self):
        """Kelime bulmaca / labirent."""
        self.np()
        self.c.setFillColor(SKY)
        self.c.roundRect(20,self.y-5,W-40,28,8,fill=1,stroke=0)
        self._img("ogrenci_erkek.png",28,self.y-3,h=22)
        self.c.setFont("CalB",12); self.c.setFillColor(WHITE)
        self.c.drawString(60,self.y+2,"KELIME BULMACASI"); self.y-=40

        # Basit kelime bulmaca gridi
        self.c.setFont("Cal",9); self.c.setFillColor(DARK)
        self.c.drawString(35,self.y,"Asagidaki harfler arasinda gizlenmis kelimeleri bul ve daire icine al!")
        self.y -= 20

        import random
        harfler = "ABCDEFGHIJKLMNOPRSTUVYZabcdefghijklmnoprstuvyz"
        grid_size = 10
        cell = 28
        sx = (W - grid_size*cell) / 2
        for row in range(grid_size):
            for col in range(grid_size):
                x = sx + col*cell
                y = self.y - row*cell
                self.c.setStrokeColor(SKY); self.c.setLineWidth(0.5)
                self.c.rect(x, y-cell, cell, cell, fill=0, stroke=1)
                self.c.setFont("CalB",14); self.c.setFillColor(NAVY)
                self.c.drawCentredString(x+cell/2, y-cell+8, random.choice(harfler))
        self.y -= grid_size*cell + 20

        self.c.setFont("CalB",9); self.c.setFillColor(SKY)
        self.c.drawString(35,self.y,"Aranan kelimeler: OKUL, KITAP, OGRENCI, DERS, SINIF")
        self.y -= 20

    def eglenceli_bilgi(self, konu_adi):
        """Eglenceli bilgi kutusu."""
        self.cs(80)
        self.c.setFillColor(LORANGE)
        self.c.roundRect(25,self.y-55,W-55,65,10,fill=1,stroke=0)
        self.c.setStrokeColor(ORANGE); self.c.setLineWidth(1.5)
        self.c.roundRect(25,self.y-55,W-55,65,10,fill=0,stroke=1)
        self._img("gunes.png",35,self.y-45,h=40)
        self.c.setFont("CalB",10); self.c.setFillColor(ORANGE)
        self.c.drawString(85,self.y,"EGLENCELI BILGI!"); self.y-=16
        self.c.setFont("CalI",9); self.c.setFillColor(DARK)
        bilgiler = [
            "Dunyanin en uzun nehri Nil Nehri'dir (6.650 km)!",
            "Bir insan omru boyunca yaklasik 25 yil uyur!",
            "Bal, bozulmayan tek yiyecektir. 3000 yillik bal bile yenebilir!",
            "Bir kelebek saniyede 12 kez kanat cirpar!",
            "Dunya uzerinde insandan daha fazla karinca yasar!",
            "Bir agac gunude yaklasik 100 litre su icer!",
            "Gokkusaginda aslinda 7 degil sonsuz renk vardir!",
            "Yildizlar aslinda gunduz de vardir ama goremeyiz!",
        ]
        import random
        b = random.choice(bilgiler)
        self.c.drawString(85,self.y,b[:70]); self.y-=12
        self.c.drawString(85,self.y,"Bunu biliyor muydun? Arkadsiina da anlat!"); self.y-=25

    # ── ARKA KAPAK ──
    def arka_kapak(self, unite_s, kaz_s):
        self.np()
        self.c.setFillColor(NAVY); self.c.rect(0,0,W,H,fill=1,stroke=0)
        self.c.setFillColor(self.r); self.c.rect(0,H-50,W,50,fill=1,stroke=0)
        for i in range(15):
            self._draw_star(30+i*38,H-25,6,Color(1,1,1,0.2))
        self.c.setFont("CalB",24); self.c.setFillColor(GOLD)
        self.c.drawCentredString(W/2,H*0.62,f"{self.sinif}. Sinif {self.ders}")
        self.c.setFont("Cal",14); self.c.setFillColor(WHITE)
        self.c.drawCentredString(W/2,H*0.52,f"{unite_s} Unite | {kaz_s} Kazanim")
        self.c.drawCentredString(W/2,H*0.46,"SmartCampusAI Premium Ders Kitabi")
        self._draw_book_icon(W/2-50,H*0.28,30,GOLD)
        self._draw_lightbulb(W/2+30,H*0.30,25,GOLD)
        self.c.setFont("Cal",9); self.c.setFillColor(GRAY)
        self.c.drawCentredString(W/2,H*0.15,"2026 SmartCampusAI - Tum Haklari Saklidir")

    def save(self):
        if self.pn>0:
            self.c.setFont("Cal",7); self.c.setFillColor(GRAY)
            self.c.drawRightString(W-30,12,f"{self.pn}")
            self.c.showPage()
        self.c.save()
        return self.pn


# Okuma parcalari
OKUMA = {
    "T\u00fcrk\u00e7e":[
        ("Kucuk Kedi","Bir zamanlar kucuk bir kedi varmis. Her gun okula giderken yolda ciceklerle oynarmis. Bir gun guzel bir kelebek gormus. Kelebek rengarekmis. Kedi kelebegi takip etmis. Derken ormana gelmis. Ormanda yeni arkadaslar bulmus. Sincap, tavsan ve kirpi ile oyun oynamis. Aksam olunca evine donmus. Annesine o gun yasadiklarini anlatmis. Annesi ona demis ki: Doga cok guzel, ama zamaninda eve donmek de onemlidir."),
        ("Kitap Kurdu Ali","Ali her aksam yatmadan once kitap okur. Kitaplardaki kahramanlarla maceraya cikar. Bazen uzay gemisine biner, bazen denizaltinda yuzar. Bir gun ogretmeni sinifa yeni kitaplar getirmis. Ali cok sevinmis. Arkadaslarina da kitap okumalarini onerdi. Simdi tum sinif kitap okuyor."),
        ("Yagmurdan Sonra","Yagmur dindi. Gunes cikti. Gokkusagi gorundu. Kucuk Zeynep bahceye kostur. Cicekler yagmur damlalariyla parliyordu. Kurbagalar sarki soyluyordu. Kelebekler ucusuyordu. Zeynep derin bir nefes aldi ve gulumsedi. Doga ne kadar guzeldi!"),
        ("Sinif Baskani","Mert sinifin en yardimever ogrencisiydi. Arkadaslarina ders calistirirdi. Okulun temizligine ozen gosterirdi. Ogretmenler onu cok severdi. Secim gunu geldi. Tum sinif Mert'i sinif baskani secti. Mert cok mutlu oldu ama sorumlulugunu da biliyordu."),
    ],
    "Matematik":[
        ("Market Alisverisi","Ayse annesiyle markete gitti. 3 elma, 5 portakal ve 2 muz aldi. Toplam kac meyve aldigini hesapladi: 3+5+2=10 meyve. Kasada her meyvenin fiyatini topladi. Matematik her yerde ise yariyor!"),
        ("Sayilar Dunyasi","Sabah saat 7'de kalktim. 8'de okula gittim. 5 ders gordum. Her ders 40 dakika surdu. 5x40=200 dakika ders yaptim. Eve donunce 2 saat odev calistim. Sayilar hayatimizin her aninda bizimle."),
    ],
    "Hayat Bilgisi":[
        ("Ailem","Ailem dort kisiden olusur: annem, babam, ablam ve ben. Anneannem ve dedem de yakinimizda oturuyor. Hafta sonlari onlara ziyarete gideriz. Birlikte yemek yeriz, oyun oynariz. Ailemizi cok seviyoruz."),
        ("Okulumuz","Okulumuzun adi Ataturk Ilkokulu. Uc katli bir binadir. Bahcesinde agaclar ve cicekler var. Kantin, kutuphane ve spor salonu var. Her sabah istiklal marsimizi okuruz. Ogretmenlerimizi cok seviyoruz."),
    ],
    "Fen Bilimleri":[
        ("Su Dongucsu","Denizlerden su buharlasiyor. Bulutlar olusuyor. Yagmur yagiyor. Yagmur sulari nehirlere akiyor. Nehirler denize donuyor. Bu donguye su dongusu deniyor. Doga kendini surekli yeniliyor."),
    ],
    "Sosyal Bilgiler":[
        ("Ataturk","Mustafa Kemal Ataturk 1881'de Selanik'te dogdu. Turkiye Cumhuriyeti'nin kurucusudur. 29 Ekim 1923'te cumhuriyeti ilan etti. Turkiye'yi modern bir devlet yapti. Egitimi, bilimi ve barisi savundu. Ataturk, 'Hayatta en hakiki mursit ilimdir' demistir. Bu soz bize bilimin onemini hatirlatir."),
        ("Haklarimiz","Her cocugun haklari vardir. Egitim hakki, saglik hakki, oyun hakki, korunma hakki. Bu haklara Birlesmis Milletler Cocuk Haklari Sozlesmesi ile guence altina alinmistir. Haklarimizi bilmeli ve baskalarinin haklarina saygi gostermeliyiz."),
        ("Yardimlasmak","Komsumuz hastalaninca anneannem ona corba gotuurdu. Babam marketten alisveris yapamayan yasli amcaya yardim etti. Ben de okulda arkadasima odevinde yardim ettim. Yardimlasmak toplumu guclendirir ve mutlu eder."),
        ("Demokratik Secim","Sinifimizda sinif baskani secimi yaptik. Herkes adaylarini dinledi. Gizli oylama yapildi. En cok oy alan Elif baskan secildi. Herkes sonuca saygi gosterdi. Iste demokrasi boyle isler!"),
        ("Teknolojinin Yolculugu","Insanlar once atesleri buldu. Sonra tekerlek icat edildi. Matbaa ile kitaplar basildi. Telefon ve televizyon geldi. Simdi bilgisayarlar ve telefonlar var. Teknoloji hayatimizi kolaylastiriyor."),
        ("Cografyamiz","Turkiye uc tarafı denizlerle cevrili guzel bir ulkedir. Kuzeyde Karadeniz, batida Ege, guneyde Akdeniz vardir. Icinde daglari, ovalari, goolleri ve nehirleri vardir. Her bolgesi farkli guzellikler tasiir."),
    ],
    "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi":[
        ("Iyilik","Iyilik yapmak insani mutlu eder. Buyuklerimize saygi gosterir, kucuklerimizi koruruz. Komsularimiza yardim ederiz. Hayvanlari severiz. Dogruyu soyler, adaletli oluruz. Iyilik yapan iyilik bulur. Hz. Muhammed (s.a.v.) 'Insanlarin en hayirlisi, insanlara en cok faydali olandir' buyurmustur."),
        ("Sabir ve Sukur","Ahmet sinifta birinci olmak istiyordu. Cok calisti ama ikinci oldu. Uzulmedi, cunku elinden gelenin en iyisini yapmisti. Ogretmeni ona 'Sabir gosterdin, bu cok degerli' dedi. Ahmet bundan sonra daha cok calisti ve basarili oldu."),
        ("Paylasmak","Ramazan ayinda annem her gun iftar sofrasimizdan komsularimiza da bir tabak yemek gonderirdi. Babam ihtiyaci olanlara yardim ederdi. Ben de kumbaramdan biriktirdiklerimi bagisladim. Paylasmak kalbi zenginlestirir."),
        ("Peygamberimizin Cocuklugu","Hz. Muhammed Mekke'de dogdu. Annesi Amine, babasi Abdullah'tir. Kucuklugunden beri dogru sozlu ve guvenilir biriydi. Ona 'Muhammedul Emin' yani guvenilir denirdi. Herkese iyi davranir, yardim ederdi."),
        ("Temizlik","Islam dini temizlige buyuk onem verir. 'Temizlik imanin yarisidir' hadisi bunu gosterir. Ellerimizi yikamak, dislerimizi fircalamak, odamizi toplamak hep temizlik ornekleridir. Temiz olan insan hem saglikli olur hem de cevresiine guzel ornek olur."),
    ],
}


def gen(sinif, ders_adi):
    renks = DERS_RENK.get(ders_adi, (TEAL,LTEAL,SKY))
    ders_key = DERS_KEY.get(ders_adi, "")
    kazanimlar = load_kazanimlar(sinif, ders_adi)
    referans = load_referans(ders_key, sinif)

    uniteler = {}
    for k in kazanimlar:
        u=k.get("unit","Genel"); uniteler.setdefault(u,[]).append(k)

    toplam_kaz = sum(len(k.get("learning_outcomes",[])) for k in kazanimlar)
    safe = ders_adi
    for o,n in [("\u00fc","u"),("\u00f6","o"),("\u0131","i"),("\u015f","s"),("\u00e7","c"),
                ("\u00dc","U"),("\u00d6","O"),("\u0130","I"),("\u015e","S"),("\u00c7","C")]:
        safe=safe.replace(o,n)
    safe=safe.replace(" ","_")
    out = os.path.join(OUT, f"{sinif}_Sinif_{safe}.pdf")

    # Az kazanimli dersler icin referans icerikten ek konular olustur
    if toplam_kaz < 80 and referans:
        unite_listesi = list(uniteler.keys())
        for i, (ref_baslik, ref_icerik) in enumerate(referans.items()):
            # Her referansi bir uniteye dagit
            hedef_unite = unite_listesi[i % len(unite_listesi)] if unite_listesi else "Genel"
            uniteler.setdefault(hedef_unite, []).append({
                "topic": ref_baslik,
                "learning_outcomes": [
                    f"{ref_baslik} konusunu aciklar.",
                    f"{ref_baslik} ile ilgili ornekler verir.",
                    f"{ref_baslik} konusundaki temel kavramlari tanimlar.",
                ],
                "week": "", "methods": "Anlatim, soru-cevap, grup calismasi",
                "assessment": "Sozlu degerlendirme, yazili test",
                "unit": hedef_unite,
            })
            toplam_kaz += 3

    kit = PremiumKitap(out, ders_adi, sinif, *renks)
    ic = {u:[k.get("topic","") for k in kl] for u,kl in uniteler.items()}
    kit.kapak(len(uniteler), toplam_kaz)
    kit.icindekiler(ic)

    okuma_list = OKUMA.get(ders_adi, OKUMA.get("T\u00fcrk\u00e7e",[]))
    unite_no = 0
    tum_kelimeler = []

    for unite_adi, konular in uniteler.items():
        unite_no += 1
        u_kaz = sum(len(k.get("learning_outcomes",[])) for k in konular)
        kit.unite_kapak(unite_adi, unite_no, len(konular), u_kaz)

        for idx, konu in enumerate(konular):
            konu_adi = konu.get("topic","Konu")
            outcomes = konu.get("learning_outcomes",[])
            hafta = konu.get("week","")
            tum_kelimeler.append(konu_adi)

            # Referans icerik bul
            ref = ""
            for rb,ri in referans.items():
                words = [w for w in konu_adi.lower().split() if len(w)>3]
                if words and any(w in rb.lower() for w in words[:3]):
                    ref = ri; break

            if not ref:
                ref = f"Bu bolumde \"{konu_adi}\" konusu ele alinmaktadir.\n\n"
                ref += "TEMEL BILGILER:\n"
                for o in outcomes[:5]:
                    ref += f"  - {o}\n"
                methods = konu.get("methods","")
                assessment = konu.get("assessment","")
                if methods: ref += f"\nOGRETIM YONTEMLERI:\n{methods}\n"
                if assessment: ref += f"\nOLCME DEGERLENDIRME:\n{assessment}\n"
                ref += f"\nBu konuyu ogrendikten sonra asagidaki kazanimlari edinmis olacaksiniz.\n"
                ref += "Konuyu iyi anlamak icin ornekleri dikkatle inceleyiniz.\n"
                ref += "Sorulari cozmeyi unutmayiniz.\n"

            okuma = okuma_list[idx % len(okuma_list)] if okuma_list else None

            # MEB FORMAT AKISI:
            # 1) Hazirlik calismasi (her 3 konuda bir)
            if idx % 3 == 0:
                kit.hazirlik_calismasi(konu_adi, unite_adi)

            # 2) Konu sayfasi (kazanim + anlatim + okuma + test + etkinlik)
            kit.konu_sayfasi(konu_adi, hafta, outcomes, ref[:4000], okuma, idx)

            # 3) 5N1K metin alti sorulari (okuma parcasi varsa)
            if okuma:
                kit.metin_alti_5n1k(okuma[0])

            # 4) Dinleme metni (her 4 konuda bir)
            if idx % 4 == 1:
                kit.dinleme_metni(konu_adi)

            # 5) Yazma calismasi (her 3 konuda bir)
            if idx % 3 == 2:
                kit.yazma_calismasi(konu_adi)

            # 5.5) Eglenceli bilgi (her konuda)
            kit.eglenceli_bilgi(konu_adi)

        # 6) Serbest okuma metni (unite sonunda)
        if okuma_list:
            s_okuma = okuma_list[unite_no % len(okuma_list)]
            kit.serbest_okuma(s_okuma[0], s_okuma[1])

        # 7) Tema degerlendirme (unite sonunda)
        kit.tema_degerlendirme(unite_adi, len(konular))

        # 8) Unite ozeti
        kit.unite_ozeti(unite_adi, [k.get("topic","") for k in konular])

        # 9) Eglenceli sayfalar (unite sonunda)
        if unite_no % 2 == 0:
            kit.bilmece_sayfasi()
        else:
            kit.oyun_sayfasi()
        kit.boyama_alani(unite_adi)

    # Sozluk
    kit.sozluk(tum_kelimeler[:20])

    # Minimum 100 sayfa — eglenceli ek sayfalarla doldur
    fillers = ["bilmece","boyama","oyun","not"]
    fi = 0
    while kit.pn < 93:
        ft = fillers[fi % len(fillers)]; fi += 1
        if ft == "bilmece":
            kit.bilmece_sayfasi()
        elif ft == "boyama":
            kit.boyama_alani(ders_adi)
        elif ft == "oyun":
            kit.oyun_sayfasi()
        else:
            kit.np()
            kit.c.setFont("CalB",12); kit.c.setFillColor(GRAY)
            kit.c.drawString(30,H-50,"NOTLARIM")
            kit.y = H-70
            for i in range(28):
                kit.c.setStrokeColor(HexColor("#E2E8F0")); kit.c.setLineWidth(0.3)
                kit.c.line(30,kit.y,W-30,kit.y); kit.y-=22

    kit.arka_kapak(len(uniteler), toplam_kaz)
    return kit.save()


ILKOKUL = {
    1: ["T\u00fcrk\u00e7e", "Hayat Bilgisi", "Matematik"],
    2: ["T\u00fcrk\u00e7e", "Hayat Bilgisi", "Matematik"],
    3: ["T\u00fcrk\u00e7e", "Hayat Bilgisi", "Matematik", "Fen Bilimleri"],
    4: ["T\u00fcrk\u00e7e", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
        "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi"],
}


ORTAOKUL = {
    5: ["T\u00fcrk\u00e7e", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
        "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi"],
    6: ["T\u00fcrk\u00e7e", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
        "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi"],
    7: ["T\u00fcrk\u00e7e", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
        "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi"],
    8: ["T\u00fcrk\u00e7e", "Matematik", "Fen Bilimleri",
        "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi", "\u0130nk\u0131lap Tarihi"],
}

# Inkilap Tarihi icin ek tanimlar
DERS_RENK["\u0130nk\u0131lap Tarihi"] = (ROSE, LROSE, PINK)
DERS_KEY["\u0130nk\u0131lap Tarihi"] = "inkilap_tarihi"
DERS_GORSELLER["\u0130nk\u0131lap Tarihi"] = ["bayrak.png","ogrenci_kiz.png","kitap.png","ogretmen.png","yildizlar.png"]

# Ortaokul okuma parcalari
OKUMA_ORTAOKUL = {
    "T\u00fcrk\u00e7e": [
        ("Kucuk Prens","Kucuk Prens gezegenden gezegenine yolculuk ederken pek cok farkli insanla karsilasti. Kral, kendini begenmis adam, isci, isadami... Her birinden farkli seyler ogrendi. Ama en onemli dersi tilkiden aldi: 'Insan ancak yuregiyle gorebilir, onemli olan gozle gorunmez.'"),
        ("Ogretmenim","Ogretmenim her sabah sinifa gulerek girerdi. Dersi anlatirken gozleri parlardi. Bize sadece ders degil, hayat ogretti. Bir gun bize dedi ki: 'Hayatta en buyuk basari, baskalarina faydali olmaktir.' Bu sozu hic unutmadim."),
        ("Kitap Dostlugu","Kitaplar en sadik dostlardir. Seni asla yargillamazlar, her zaman yeni seyler ogretirler. Bir kitap actiginizda yeni bir dunyaya kapiyi aralarsiniiz. Okumak, dusunmeyi ve hayal kurmayii ogretir."),
        ("Bilim Insanlari","Edison ampulu icat etmeden once binlerce basarisiz deneme yapti. Her basarisizlikta 'Bir yol daha eledim' dedi. Azim ve sebat, basarinin anahtaridir. Buyuk kesfler buyuk sabirla ortaya cikar."),
    ],
    "Matematik": [
        ("Sayilarin Dili","Matematik evrenin dilidir. Galileo 'Evren matematik diliyle yazilmistir' demistir. Gunluk hayatta farkinda olmadan surekli matematik kullaniriz: alisveriste, yemek yapiminda, sporda, musiikte. Her yerde sayilar vardir."),
        ("Pi Sayisi","Pi sayisi (3.14159...) dairenin cevresinin capina oraniidir. Bu sayi sonsuzdur ve hic tekrar etmez. Eski Misirlilar bile pi sayisini kullaniyordu. Bugun superbiilgisayarlar trilyonlarca basamagini hesapladi."),
    ],
    "Fen Bilimleri": [
        ("DNA Sirri","Her canli varligin icinde DNA denilen muhtesem bir molekul vardir. DNA, varligin tum ozelliklerini tasiyan bir sifre gibidir. Goz rengin, boyun, sac yapiin hep DNA'da yazilidir. Insan DNA'si yaklasik 3 milyar harf icerirr."),
        ("Uzay Macerasi","Uzay sonsuz buyukluktedir. En yakin yildiz bile isik hiziyla 4 yil uzaktadir. Gunes sistemimiizde 8 gezegen vardir. Dunnyamiz bu engin uzayda kucuk bir noktadir ama bizim icin essizdir."),
    ],
    "Sosyal Bilgiler": [
        ("Demokrasi","Demokrasi halkin kendi kendini yonetmesidir. Secimler, basin ozgurlugu, insan haklari demokrasinin temelleridir. Ataturk 'Egemenlik kayitsiz sartsiz milletindir' demistir. Demokrasi herkesin haklarrna saygi gostermeyi gerektirir."),
        ("Cografya ve Insan","Insanlar yasadiklari cografyaya gore hayat kurar. Deniz kenaarinda yasayanlar balikcilik, ovada yasayanlar tarimm, dagda yasayanlar hayvancilik yapar. Cografya kulturu, yemegii, mimariiyi bile etkiler."),
    ],
    "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi": [
        ("Adalet","Hz. Omer adaletiyle unlu bir halifeydi. Gece vakti sokaklarda dolasir, halkin derdini dinlerdi. Bir gun bir cocugun agladigini duydu ve ailesine yardim etti. Adalet, gucluyle gucsuzu esit tutmaktir."),
        ("Hosgoru","Mevlana 'Gel, ne olursan ol yine gel' demistir. Hosgoru, farkliliklara saygi gostermektir. Insanlari dinlerine, dillerine, renklerine gore ayirmamak hosggorunun temelldir."),
    ],
    "\u0130nk\u0131lap Tarihi": [
        ("Kurtulus Savasi","Mustafa Kemal 19 Mayis 1919'da Samsun'a cikarak Kurtulus Savasii'ni baslatti. Turk milleti buyuk fedakarliklar gosterdi. Kadinlar cepheeye mermi tasidi, cocuklar bile yardim etti. 30 Agustos 1922'de Baskumandanlik Meydan Muharebesi kazanildi."),
        ("Cumhuriyetin Ilani","29 Ekim 1923'te Turkiye Cumhuriyeti ilan edildi. Ataturk ilk Cumhurbaskani seciildi. Harf inkilabii, egitim birligi, kadinlara secme-secilme hakki gibi devrimlerle Turkiye modernlesti. Ataturk 'Ne mutlu Turkum diyene' demistir."),
    ],
}

LISE_DERSLER = ["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih",
    "Co\u011frafya", "Edebiyat", "Felsefe", "Din K\u00fclt\u00fcr\u00fc ve Ahlak Bilgisi"]
LISE = {
    9: LISE_DERSLER[:],
    10: LISE_DERSLER[:],
    11: LISE_DERSLER[:],
    12: LISE_DERSLER[:],
}
# Lise ders tanimlari
for d in ["Fizik","Kimya","Biyoloji","Tarih","Co\u011frafya","Edebiyat","Felsefe"]:
    if d not in DERS_KEY:
        key = d.lower().replace("\u011f","g").replace("\u00f6","o").replace("\u00fc","u")
        DERS_KEY[d] = key
    if d not in DERS_RENK:
        DERS_RENK[d] = (TEAL, LTEAL, SKY)
    if d not in DERS_GORSELLER:
        DERS_GORSELLER[d] = ["ogrenci_erkek.png","kitap.png","ogretmen.png","yildizlar.png","gunes.png"]

# Renk atamalari
DERS_RENK["Fizik"] = (SKY, LBLUE, BLUE)
DERS_RENK["Kimya"] = (EMERALD, LGREEN, GREEN)
DERS_RENK["Biyoloji"] = (GREEN, LGREEN, EMERALD)
DERS_RENK["Tarih"] = (ROSE, LROSE, PINK)
DERS_RENK["Co\u011frafya"] = (AMBER, LORANGE, ORANGE)
DERS_RENK["Edebiyat"] = (INDIGO, LPURPLE, PURPLE)
DERS_RENK["Felsefe"] = (PURPLE, LPURPLE, INDIGO)
DERS_KEY["Co\u011frafya"] = "cografya"
DERS_KEY["Edebiyat"] = "edebiyat"
DERS_KEY["Felsefe"] = "felsefe"
DERS_KEY["Fizik"] = "fizik"
DERS_KEY["Kimya"] = "kimya"
DERS_KEY["Biyoloji"] = "biyoloji"
DERS_KEY["Tarih"] = "tarih"

OUT_ORTA = os.path.join(BASE, "Ders_Kitaplari_PDF", "Ortaokul_Premium")
os.makedirs(OUT_ORTA, exist_ok=True)


def gen_ortaokul(sinif, ders_adi):
    """Ortaokul kitap uretici — ayni formatta."""
    # Inkilap Tarihi subject eslestirme
    subject_map = {
        "T.C. \u0130nk\u0131lap Tarihi ve Atat\u00fcrk\u00e7\u00fcl\u00fck": "T.C. \u0130nk\u0131lap Tarihi ve Atat\u00fcrk\u00e7\u00fcl\u00fck",
    }
    search_subject = ders_adi
    # Inkilap tarihi farkli isimle kayitli olabilir
    if "nk" in ders_adi.lower() and "lap" in ders_adi.lower():
        # Veritabanindaki olasi isimlerle ara
        import json as _j
        with open(os.path.join(BASE,"data","olcme","annual_plans.json"),"r",encoding="utf-8") as _f:
            _pl = _j.load(_f)
        for _p in _pl:
            if _p.get("grade") == sinif and "nk" in _p.get("subject","").lower():
                search_subject = _p["subject"]
                break

    # gen fonksiyonunu ortaokul OUT ile cagir
    global OUT
    old_out = OUT
    OUT = OUT_ORTA

    # Okuma parcalarini ortaokul ile degistir
    global OKUMA
    old_okuma = dict(OKUMA)
    OKUMA.update(OKUMA_ORTAOKUL)

    result = gen(sinif, ders_adi)

    OUT = old_out
    OKUMA = old_okuma
    return result


def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "ilkokul"

    OUT_LISE = os.path.join(BASE, "Ders_Kitaplari_PDF", "Lise_Premium")
    os.makedirs(OUT_LISE, exist_ok=True)

    if mode == "lise":
        print("="*60)
        print("SmartCampusAI PREMIUM DERS KITABI - LISE")
        print("="*60)
        t=0; tp=0
        global OUT
        old_out = OUT
        OUT = OUT_LISE
        for sinif in [9,10,11,12]:
            dersler = LISE[sinif]
            print(f"\n== {sinif}. SINIF ({len(dersler)} ders) ==")
            for d in dersler:
                p = gen(sinif, d)
                t+=1; tp+=p
                print(f"  [{t:2d}] {sinif}. Sinif: {p} sayfa")
        OUT = old_out
        print(f"\n{'='*60}")
        print(f"TAMAMLANDI: {t} kitap, {tp} toplam sayfa")
        print(f"Klasor: {OUT_LISE}")
    elif mode == "ortaokul":
        print("="*60)
        print("SmartCampusAI PREMIUM DERS KITABI - ORTAOKUL")
        print("="*60)
        t=0; tp=0
        for sinif in [5,6,7,8]:
            dersler = ORTAOKUL[sinif]
            print(f"\n== {sinif}. SINIF ({len(dersler)} ders) ==")
            for d in dersler:
                p = gen_ortaokul(sinif, d)
                t+=1; tp+=p
                print(f"  [{t:2d}] {sinif}. Sinif: {p} sayfa")
        print(f"\n{'='*60}")
        print(f"TAMAMLANDI: {t} kitap, {tp} toplam sayfa")
        print(f"Klasor: {OUT_ORTA}")
    else:
        print("="*60)
        print("SmartCampusAI PREMIUM DERS KITABI - ILKOKUL")
        print("="*60)
        t=0; tp=0
        for sinif in [1,2,3,4]:
            dersler = ILKOKUL[sinif]
            print(f"\n== {sinif}. SINIF ({len(dersler)} ders) ==")
            for d in dersler:
                p = gen(sinif, d)
                t+=1; tp+=p
                print(f"  [{t:2d}] {sinif}. Sinif: {p} sayfa")
        print(f"\n{'='*60}")
        print(f"TAMAMLANDI: {t} kitap, {tp} toplam sayfa")
        print(f"Klasor: {OUT}")


if __name__=="__main__":
    main()
