"""
Sertifika Uretici Modulu
=========================
Basari belgesi, katilim belgesi, tesekkur ve takdir belgeleri
olusturma, toplu uretim ve arsivleme sistemi.
"""

from __future__ import annotations

import io
import json
import uuid
import zipfile
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import cm, mm
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "akademik"
SERTIFIKA_FILE = DATA_DIR / "sertifikalar.json"


def _load_json(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_students():
    return _load_json(DATA_DIR / "students.json")


def _load_sertifikalar():
    return _load_json(SERTIFIKA_FILE)


def _save_sertifikalar(data):
    _save_json(SERTIFIKA_FILE, data)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SERTIFIKA_TURLERI = [
    "Basari Belgesi",
    "Katilim Belgesi",
    "Tesekkur Belgesi",
    "Takdir Belgesi",
    "Birincilik Belgesi",
    "Ikincilik Belgesi",
    "Ucunculuk Belgesi",
]

SERTIFIKA_RENKLERI = {
    "Basari Belgesi": {"border": "#2563eb", "accent": "#1e40af", "bg": "#eff6ff"},
    "Katilim Belgesi": {"border": "#059669", "accent": "#065f46", "bg": "#ecfdf5"},
    "Tesekkur Belgesi": {"border": "#7c3aed", "accent": "#5b21b6", "bg": "#f5f3ff"},
    "Takdir Belgesi": {"border": "#d97706", "accent": "#92400e", "bg": "#fffbeb"},
    "Birincilik Belgesi": {"border": "#d4af37", "accent": "#92400e", "bg": "#fefce8"},
    "Ikincilik Belgesi": {"border": "#94a3b8", "accent": "#475569", "bg": "#f8fafc"},
    "Ucunculuk Belgesi": {"border": "#b45309", "accent": "#78350f", "bg": "#fff7ed"},
}

SERTIFIKA_BASLIK_MAP = {
    "Basari Belgesi": "BASARI BELGESI",
    "Katilim Belgesi": "KATILIM BELGESI",
    "Tesekkur Belgesi": "TESEKKUR BELGESI",
    "Takdir Belgesi": "TAKDIR BELGESI",
    "Birincilik Belgesi": "BIRINCILIK BELGESI",
    "Ikincilik Belgesi": "IKINCILIK BELGESI",
    "Ucunculuk Belgesi": "UCUNCULUK BELGESI",
}

SERTIFIKA_ACIKLAMA_MAP = {
    "Basari Belgesi": "gostermis oldugu ustun basaridan dolayi bu belge ile odullendirilmistir.",
    "Katilim Belgesi": "etkinlige katilimindan dolayi bu belge ile takdir edilmistir.",
    "Tesekkur Belgesi": "gostermis oldugu gayret ve caliskanliktan dolayi tesekkur edilir.",
    "Takdir Belgesi": "ustun basarisi ve ornek davranislarindan dolayi takdir edilmistir.",
    "Birincilik Belgesi": "yarismasinda birincilik elde ederek buyuk basari gostermistir.",
    "Ikincilik Belgesi": "yarismasinda ikincilik elde ederek basari gostermistir.",
    "Ucunculuk Belgesi": "yarismasinda ucunculuk elde ederek basari gostermistir.",
}

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS = """
<style>
.metric-card{
    background:linear-gradient(135deg,#1e293b,#0f172a);
    padding:20px;border-radius:12px;border-left:4px solid;color:white;
}
.metric-card h3{font-size:14px;color:#94a3b8;margin:0 0 6px 0;font-weight:500;}
.metric-card .val{font-size:28px;font-weight:700;margin:0;}
.mc-blue{border-color:#3b82f6;} .mc-green{border-color:#22c55e;}
.mc-amber{border-color:#f59e0b;} .mc-red{border-color:#ef4444;}
.mc-purple{border-color:#a855f7;} .mc-cyan{border-color:#06b6d4;}
.cert-header{
    background:linear-gradient(90deg,#0f172a 0%,#1e3a5f 100%);
    padding:24px 28px;border-radius:14px;margin-bottom:18px;color:white;
}
.cert-header h2{margin:0;font-size:22px;}
.cert-header p{margin:4px 0 0;color:#94a3b8;font-size:13px;}
.section-title{
    font-size:16px;font-weight:600;color:#1e293b;
    border-bottom:2px solid #3b82f6;padding-bottom:6px;margin:18px 0 12px;
}
.cert-preview{
    border:3px double #2563eb;border-radius:8px;padding:40px 30px;
    text-align:center;background:#fefefe;margin:16px 0;min-height:300px;
    position:relative;
}
.cert-preview .cert-title{
    font-size:28px;font-weight:700;letter-spacing:3px;margin:10px 0 20px;
}
.cert-preview .cert-recipient{
    font-size:22px;font-weight:600;margin:20px 0;
    border-bottom:2px solid;display:inline-block;padding-bottom:4px;
}
.cert-preview .cert-body{
    font-size:14px;line-height:1.8;color:#475569;margin:16px 0;
}
.cert-preview .cert-footer{
    display:flex;justify-content:space-between;margin-top:40px;
    padding:0 40px;
}
.cert-preview .cert-sign{
    text-align:center;font-size:13px;color:#64748b;
}
.cert-preview .cert-sign .line{
    border-top:1px solid #94a3b8;width:160px;margin:0 auto 6px;
}
.cert-preview .cert-school{
    font-size:16px;font-weight:600;color:#1e293b;margin-bottom:6px;
}
.cert-preview .cert-date{
    font-size:13px;color:#64748b;margin-top:8px;
}
</style>
"""


def _metric_card(title: str, value, color: str = "blue"):
    return (
        f'<div class="metric-card mc-{color}">'
        f'<h3>{title}</h3>'
        f'<p class="val">{value}</p>'
        f'</div>'
    )


def _section(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Certificate preview (HTML)
# ---------------------------------------------------------------------------

def _cert_preview_html(
    template: str,
    ogrenci_adi: str,
    sinif: str,
    etkinlik: str,
    tarih: str,
    imzalayan: str,
    okul_adi: str = "SmartCampus Egitim Kurumlari",
):
    renk = SERTIFIKA_RENKLERI.get(template, SERTIFIKA_RENKLERI["Basari Belgesi"])
    baslik = SERTIFIKA_BASLIK_MAP.get(template, template.upper())
    aciklama = SERTIFIKA_ACIKLAMA_MAP.get(template, "basarili calismalarindan dolayi bu belge ile odullendirilmistir.")

    body_text = f'<b>{etkinlik}</b> {aciklama}' if etkinlik else aciklama

    return f"""
    <div class="cert-preview" style="border-color:{renk['border']};background:{renk['bg']};">
        <div class="cert-school" style="color:{renk['accent']};">{okul_adi}</div>
        <div class="cert-title" style="color:{renk['accent']};">{baslik}</div>
        <div style="font-size:14px;color:#64748b;">Bu belge</div>
        <div class="cert-recipient" style="color:{renk['accent']};border-color:{renk['border']};">
            {ogrenci_adi}
        </div>
        <div style="font-size:13px;color:#94a3b8;">{sinif}</div>
        <div class="cert-body">{body_text}</div>
        <div class="cert-date">Tarih: {tarih}</div>
        <div class="cert-footer">
            <div class="cert-sign">
                <div class="line"></div>
                Okul Muduru
            </div>
            <div class="cert-sign">
                <div class="line"></div>
                {imzalayan}
            </div>
        </div>
    </div>
    """


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def _generate_cert_pdf(
    template: str,
    ogrenci_adi: str,
    sinif: str,
    etkinlik: str,
    tarih: str,
    imzalayan: str,
    okul_adi: str = "SmartCampus Egitim Kurumlari",
) -> bytes | None:
    """Generate a certificate PDF using ReportLab. Returns bytes or None."""
    if not HAS_REPORTLAB:
        return None

    buf = io.BytesIO()
    page_size = landscape(A4)
    c = rl_canvas.Canvas(buf, pagesize=page_size)
    w, h = page_size

    renk = SERTIFIKA_RENKLERI.get(template, SERTIFIKA_RENKLERI["Basari Belgesi"])

    # Parse hex color
    def _hex(hex_str):
        hex_str = hex_str.lstrip("#")
        return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    border_rgb = _hex(renk["border"])
    accent_rgb = _hex(renk["accent"])

    # Outer border
    c.setStrokeColorRGB(*border_rgb)
    c.setLineWidth(3)
    c.rect(30, 30, w - 60, h - 60)

    # Inner border
    c.setLineWidth(1)
    c.rect(38, 38, w - 76, h - 76)

    # School name
    c.setFillColorRGB(*accent_rgb)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, h - 90, okul_adi)

    # Title
    baslik = SERTIFIKA_BASLIK_MAP.get(template, template.upper())
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(w / 2, h - 140, baslik)

    # Decorative line
    c.setStrokeColorRGB(*border_rgb)
    c.setLineWidth(1.5)
    line_w = 200
    c.line(w / 2 - line_w / 2, h - 155, w / 2 + line_w / 2, h - 155)

    # "Bu belge"
    c.setFillColorRGB(0.4, 0.45, 0.52)
    c.setFont("Helvetica", 12)
    c.drawCentredString(w / 2, h - 185, "Bu belge")

    # Recipient name
    c.setFillColorRGB(*accent_rgb)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(w / 2, h - 220, ogrenci_adi)

    # Underline for name
    name_width = c.stringWidth(ogrenci_adi, "Helvetica-Bold", 22)
    c.setStrokeColorRGB(*border_rgb)
    c.setLineWidth(1)
    c.line(w / 2 - name_width / 2, h - 225, w / 2 + name_width / 2, h - 225)

    # Class
    c.setFillColorRGB(0.58, 0.65, 0.72)
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h - 245, sinif)

    # Body text
    aciklama = SERTIFIKA_ACIKLAMA_MAP.get(template, "basarili calismalarindan dolayi bu belge verilmistir.")
    body = f"{etkinlik} {aciklama}" if etkinlik else aciklama
    c.setFillColorRGB(0.28, 0.33, 0.4)
    c.setFont("Helvetica", 12)

    # Word-wrap body text
    max_line_w = w - 200
    words = body.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        if c.stringWidth(test, "Helvetica", 12) < max_line_w:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    y_body = h - 280
    for line in lines:
        c.drawCentredString(w / 2, y_body, line)
        y_body -= 18

    # Date
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.4, 0.45, 0.52)
    c.drawCentredString(w / 2, 110, f"Tarih: {tarih}")

    # Signatures
    sig_y = 70
    # Left: Okul Muduru
    c.setStrokeColorRGB(0.58, 0.65, 0.72)
    c.line(120, sig_y + 15, 280, sig_y + 15)
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.4, 0.45, 0.52)
    c.drawCentredString(200, sig_y, "Okul Muduru")

    # Right: Imzalayan
    c.line(w - 280, sig_y + 15, w - 120, sig_y + 15)
    c.drawCentredString(w - 200, sig_y, imzalayan)

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()


def _generate_html_download(
    template: str,
    ogrenci_adi: str,
    sinif: str,
    etkinlik: str,
    tarih: str,
    imzalayan: str,
    okul_adi: str = "SmartCampus Egitim Kurumlari",
) -> str:
    """Generate downloadable HTML certificate."""
    renk = SERTIFIKA_RENKLERI.get(template, SERTIFIKA_RENKLERI["Basari Belgesi"])
    baslik = SERTIFIKA_BASLIK_MAP.get(template, template.upper())
    aciklama = SERTIFIKA_ACIKLAMA_MAP.get(template, "basarili calismalarindan dolayi verilmistir.")
    body_text = f"<b>{etkinlik}</b> {aciklama}" if etkinlik else aciklama

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{baslik}</title>
<style>
@page {{ size: A4 landscape; margin: 0; }}
body {{ margin: 0; display: flex; justify-content: center; align-items: center;
       min-height: 100vh; background: #f8fafc; font-family: Georgia, serif; }}
.cert {{ width: 900px; padding: 50px 40px; border: 3px double {renk['border']};
         border-radius: 8px; background: {renk['bg']}; text-align: center;
         position: relative; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
.school {{ font-size: 18px; font-weight: bold; color: {renk['accent']}; }}
.title {{ font-size: 32px; font-weight: bold; letter-spacing: 4px;
          color: {renk['accent']}; margin: 16px 0; }}
.subtitle {{ font-size: 14px; color: #64748b; }}
.recipient {{ font-size: 24px; font-weight: bold; color: {renk['accent']};
              border-bottom: 2px solid {renk['border']}; display: inline-block;
              padding-bottom: 4px; margin: 20px 0 6px; }}
.class-info {{ font-size: 13px; color: #94a3b8; }}
.body {{ font-size: 14px; line-height: 1.9; color: #475569; margin: 20px 40px; }}
.date {{ font-size: 13px; color: #64748b; margin-top: 16px; }}
.footer {{ display: flex; justify-content: space-between; margin-top: 50px; padding: 0 60px; }}
.sign {{ text-align: center; font-size: 13px; color: #64748b; }}
.sign .line {{ border-top: 1px solid #94a3b8; width: 180px; margin: 0 auto 8px; }}
</style></head>
<body>
<div class="cert">
    <div class="school">{okul_adi}</div>
    <div class="title">{baslik}</div>
    <div class="subtitle">Bu belge</div>
    <div class="recipient">{ogrenci_adi}</div>
    <div class="class-info">{sinif}</div>
    <div class="body">{body_text}</div>
    <div class="date">Tarih: {tarih}</div>
    <div class="footer">
        <div class="sign"><div class="line"></div>Okul Muduru</div>
        <div class="sign"><div class="line"></div>{imzalayan}</div>
    </div>
</div>
</body></html>"""


# ---------------------------------------------------------------------------
# Tab 1: Sertifika Olustur
# ---------------------------------------------------------------------------

def _tab_sertifika_olustur(students, sertifikalar):
    _section("Sertifika Olusturma")

    aktif = [s for s in students if s.get("durum") == "aktif"]

    c1, c2 = st.columns(2)
    with c1:
        template = st.selectbox("Sertifika Turu", SERTIFIKA_TURLERI, key="cert_type")
        student_options = {
            f'{s.get("ad", "")} {s.get("soyad", "")} ({s.get("sinif")}-{s.get("sube")})': s["id"]
            for s in aktif
        }
        sel_students = st.multiselect(
            "Ogrenci Secimi", list(student_options.keys()), key="cert_students"
        )

    with c2:
        etkinlik = st.text_input("Etkinlik / Ders Adi", key="cert_etkinlik",
                                 placeholder="Ornek: Matematik Olimpiyati")
        cert_date = st.date_input("Tarih", value=date.today(), key="cert_date")
        imzalayan = st.text_input("Imza Yetkili (Mudur Adi)", key="cert_imzalayan",
                                  placeholder="Ornek: Prof. Dr. Ahmet Yilmaz")

    okul_adi = st.text_input("Okul Adi", value="SmartCampus Egitim Kurumlari", key="cert_okul")

    # Preview
    if sel_students:
        _section("Onizleme")
        # Show preview for first selected student
        first_key = sel_students[0]
        first_id = student_options.get(first_key, "")
        first_stu = next((s for s in students if s["id"] == first_id), {})
        ogrenci_adi = f'{first_stu.get("ad", "")} {first_stu.get("soyad", "")}'
        sinif_str = f'{first_stu.get("sinif", "?")}-{first_stu.get("sube", "?")}. Sinif'
        tarih_str = cert_date.strftime("%d.%m.%Y") if cert_date else date.today().strftime("%d.%m.%Y")

        preview_html = _cert_preview_html(
            template=template,
            ogrenci_adi=ogrenci_adi,
            sinif=sinif_str,
            etkinlik=etkinlik,
            tarih=tarih_str,
            imzalayan=imzalayan or "Okul Muduru",
            okul_adi=okul_adi,
        )
        st.markdown(preview_html, unsafe_allow_html=True)

        if len(sel_students) > 1:
            st.info(f"Toplam {len(sel_students)} ogrenci secildi. Onizleme ilk ogrenci icin gosterilmektedir.")

    st.markdown("---")

    # Generate buttons
    col_pdf, col_html = st.columns(2)

    with col_pdf:
        if st.button("PDF Olustur", type="primary", use_container_width=True, key="gen_pdf",
                      disabled=not sel_students):
            if not imzalayan.strip():
                st.error("Lutfen imza yetkili adini girin.")
            elif not HAS_REPORTLAB:
                st.warning("ReportLab kurulu degil. HTML indirme secenegini kullanin.")
            else:
                tarih_str = cert_date.strftime("%d.%m.%Y") if cert_date else date.today().strftime("%d.%m.%Y")
                generated = 0
                for skey in sel_students:
                    sid = student_options.get(skey, "")
                    stu = next((s for s in students if s["id"] == sid), {})
                    ogrenci_adi = f'{stu.get("ad", "")} {stu.get("soyad", "")}'
                    sinif_str = f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}. Sinif'

                    pdf_bytes = _generate_cert_pdf(
                        template=template, ogrenci_adi=ogrenci_adi, sinif=sinif_str,
                        etkinlik=etkinlik, tarih=tarih_str,
                        imzalayan=imzalayan.strip(), okul_adi=okul_adi,
                    )
                    if pdf_bytes:
                        # Save record
                        record = {
                            "id": f"srt_{uuid.uuid4().hex[:8]}",
                            "student_id": sid,
                            "ogrenci_adi": ogrenci_adi,
                            "tur": template,
                            "aciklama": etkinlik,
                            "tarih": cert_date.isoformat() if cert_date else date.today().isoformat(),
                            "veren": imzalayan.strip(),
                            "akademik_yil": "2025-2026",
                            "olusturma_zamani": datetime.now().isoformat(),
                        }
                        sertifikalar.append(record)
                        generated += 1

                        fname = f"sertifika_{ogrenci_adi.replace(' ', '_')}_{template.replace(' ', '_')}.pdf"
                        st.download_button(
                            f"Indir: {ogrenci_adi}", pdf_bytes,
                            file_name=fname, mime="application/pdf",
                            key=f"dl_pdf_{sid}",
                        )

                if generated > 0:
                    _save_sertifikalar(sertifikalar)
                    st.success(f"{generated} sertifika basariyla olusturuldu!")

    with col_html:
        if st.button("HTML Indir", use_container_width=True, key="gen_html",
                      disabled=not sel_students):
            if not imzalayan.strip():
                st.error("Lutfen imza yetkili adini girin.")
            else:
                tarih_str = cert_date.strftime("%d.%m.%Y") if cert_date else date.today().strftime("%d.%m.%Y")
                generated = 0
                for skey in sel_students:
                    sid = student_options.get(skey, "")
                    stu = next((s for s in students if s["id"] == sid), {})
                    ogrenci_adi = f'{stu.get("ad", "")} {stu.get("soyad", "")}'
                    sinif_str = f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}. Sinif'

                    html_content = _generate_html_download(
                        template=template, ogrenci_adi=ogrenci_adi, sinif=sinif_str,
                        etkinlik=etkinlik, tarih=tarih_str,
                        imzalayan=imzalayan.strip(), okul_adi=okul_adi,
                    )

                    # Save record
                    record = {
                        "id": f"srt_{uuid.uuid4().hex[:8]}",
                        "student_id": sid,
                        "ogrenci_adi": ogrenci_adi,
                        "tur": template,
                        "aciklama": etkinlik,
                        "tarih": cert_date.isoformat() if cert_date else date.today().isoformat(),
                        "veren": imzalayan.strip(),
                        "akademik_yil": "2025-2026",
                        "olusturma_zamani": datetime.now().isoformat(),
                    }
                    sertifikalar.append(record)
                    generated += 1

                    fname = f"sertifika_{ogrenci_adi.replace(' ', '_')}_{template.replace(' ', '_')}.html"
                    st.download_button(
                        f"Indir: {ogrenci_adi}", html_content.encode("utf-8"),
                        file_name=fname, mime="text/html",
                        key=f"dl_html_{sid}",
                    )

                if generated > 0:
                    _save_sertifikalar(sertifikalar)
                    st.success(f"{generated} sertifika basariyla olusturuldu!")


# ---------------------------------------------------------------------------
# Tab 2: Toplu Sertifika
# ---------------------------------------------------------------------------

def _tab_toplu_sertifika(students, sertifikalar):
    _section("Toplu Sertifika Uretimi")

    aktif = [s for s in students if s.get("durum") == "aktif"]
    siniflar = sorted(set(s.get("sinif", 0) for s in aktif))
    subeler = sorted(set(s.get("sube", "") for s in aktif))

    c1, c2, c3 = st.columns(3)
    with c1:
        sel_sinif = st.selectbox("Sinif", siniflar, key="batch_sinif")
    with c2:
        sel_sube = st.selectbox("Sube", ["Tumu"] + subeler, key="batch_sube")
    with c3:
        batch_template = st.selectbox("Sertifika Turu", SERTIFIKA_TURLERI, key="batch_template")

    # Filter students
    filtered = [s for s in aktif if s.get("sinif") == sel_sinif]
    if sel_sube != "Tumu":
        filtered = [s for s in filtered if s.get("sube") == sel_sube]

    st.info(f"Secilen sinifta **{len(filtered)}** ogrenci bulunmaktadir.")

    if filtered:
        # Show student list
        with st.expander("Ogrenci Listesi"):
            rows = []
            for s in filtered:
                rows.append({
                    "Ad": s.get("ad", ""),
                    "Soyad": s.get("soyad", ""),
                    "Sinif": f'{s.get("sinif")}-{s.get("sube")}',
                    "Numara": s.get("numara", "-"),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    batch_etkinlik = st.text_input("Etkinlik / Ders Adi", key="batch_etkinlik",
                                   placeholder="Ornek: 2025-2026 Akademik Yil Sonu")
    batch_date = st.date_input("Tarih", value=date.today(), key="batch_date")
    batch_imza = st.text_input("Imza Yetkili", key="batch_imza",
                               placeholder="Okul Muduru adi")
    batch_okul = st.text_input("Okul Adi", value="SmartCampus Egitim Kurumlari", key="batch_okul")

    st.markdown("---")

    if st.button("Toplu Sertifika Olustur (ZIP)", type="primary",
                 use_container_width=True, key="batch_gen",
                 disabled=not filtered):
        if not batch_imza.strip():
            st.error("Lutfen imza yetkili adini girin.")
            return

        tarih_str = batch_date.strftime("%d.%m.%Y") if batch_date else date.today().strftime("%d.%m.%Y")

        zip_buf = io.BytesIO()
        generated = 0

        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for stu in filtered:
                ogrenci_adi = f'{stu.get("ad", "")} {stu.get("soyad", "")}'
                sinif_str = f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}. Sinif'

                if HAS_REPORTLAB:
                    pdf_bytes = _generate_cert_pdf(
                        template=batch_template, ogrenci_adi=ogrenci_adi,
                        sinif=sinif_str, etkinlik=batch_etkinlik,
                        tarih=tarih_str, imzalayan=batch_imza.strip(),
                        okul_adi=batch_okul,
                    )
                    if pdf_bytes:
                        fname = f"sertifika_{ogrenci_adi.replace(' ', '_')}.pdf"
                        zf.writestr(fname, pdf_bytes)
                else:
                    html = _generate_html_download(
                        template=batch_template, ogrenci_adi=ogrenci_adi,
                        sinif=sinif_str, etkinlik=batch_etkinlik,
                        tarih=tarih_str, imzalayan=batch_imza.strip(),
                        okul_adi=batch_okul,
                    )
                    fname = f"sertifika_{ogrenci_adi.replace(' ', '_')}.html"
                    zf.writestr(fname, html.encode("utf-8"))

                # Save record
                record = {
                    "id": f"srt_{uuid.uuid4().hex[:8]}",
                    "student_id": stu["id"],
                    "ogrenci_adi": ogrenci_adi,
                    "tur": batch_template,
                    "aciklama": batch_etkinlik,
                    "tarih": batch_date.isoformat() if batch_date else date.today().isoformat(),
                    "veren": batch_imza.strip(),
                    "akademik_yil": "2025-2026",
                    "olusturma_zamani": datetime.now().isoformat(),
                }
                sertifikalar.append(record)
                generated += 1

        _save_sertifikalar(sertifikalar)

        zip_buf.seek(0)
        sinif_label = f"{sel_sinif}-{sel_sube}" if sel_sube != "Tumu" else f"{sel_sinif}_tum"
        st.download_button(
            f"ZIP Indir ({generated} sertifika)",
            zip_buf.getvalue(),
            file_name=f"sertifikalar_{sinif_label}_{batch_template.replace(' ', '_')}.zip",
            mime="application/zip",
            key="dl_batch_zip",
        )
        st.success(f"{generated} sertifika basariyla olusturuldu ve ZIP dosyasina eklendi!")


# ---------------------------------------------------------------------------
# Tab 3: Sertifika Arsivi
# ---------------------------------------------------------------------------

def _tab_arsiv(students, sertifikalar):
    _section("Sertifika Arsivi")

    if not sertifikalar:
        st.info("Henuz olusturulmus sertifika bulunmamaktadir.")
        return

    stu_map = {s["id"]: s for s in students}

    # Metrics
    cols = st.columns(4)
    with cols[0]:
        st.markdown(_metric_card("Toplam Sertifika", len(sertifikalar), "blue"), unsafe_allow_html=True)
    with cols[1]:
        unique_students = len(set(s.get("student_id", "") for s in sertifikalar))
        st.markdown(_metric_card("Ogrenci Sayisi", unique_students, "green"), unsafe_allow_html=True)
    with cols[2]:
        type_counts = Counter(s.get("tur", "") for s in sertifikalar)
        most_common = type_counts.most_common(1)[0][0] if type_counts else "-"
        st.markdown(_metric_card("En Cok Verilen", most_common, "amber"), unsafe_allow_html=True)
    with cols[3]:
        this_year = len([s for s in sertifikalar if s.get("akademik_yil") == "2025-2026"])
        st.markdown(_metric_card("Bu Yil", this_year, "purple"), unsafe_allow_html=True)

    st.markdown("")

    # Filters
    c1, c2, c3 = st.columns(3)
    with c1:
        filter_student = st.text_input("Ogrenci Ara", key="arsiv_student",
                                       placeholder="Ad veya soyad...")
    with c2:
        type_options = ["Tumu"] + SERTIFIKA_TURLERI
        filter_type = st.selectbox("Sertifika Turu", type_options, key="arsiv_type")
    with c3:
        filter_date = st.date_input("Tarih (Sonrasi)", value=None, key="arsiv_date")

    # Filter
    filtered = sertifikalar[:]
    if filter_student:
        q = filter_student.lower()
        filtered = [s for s in filtered if q in s.get("ogrenci_adi", "").lower()]
    if filter_type != "Tumu":
        filtered = [s for s in filtered if s.get("tur") == filter_type]
    if filter_date:
        date_str = filter_date.isoformat()
        filtered = [s for s in filtered if s.get("tarih", "") >= date_str]

    # Sort by date descending
    filtered.sort(key=lambda x: x.get("tarih", ""), reverse=True)

    if filtered:
        rows = []
        for s in filtered:
            stu = stu_map.get(s.get("student_id", ""), {})
            rows.append({
                "Ogrenci": s.get("ogrenci_adi", "-"),
                "Sinif": f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}',
                "Sertifika Turu": s.get("tur", "-"),
                "Etkinlik": s.get("aciklama", "-"),
                "Tarih": s.get("tarih", "-"),
                "Veren": s.get("veren", "-"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Re-download option
        _section("Yeniden Indir")
        sel_cert_idx = st.selectbox(
            "Sertifika Sec",
            range(len(filtered)),
            format_func=lambda i: (
                f'{filtered[i].get("ogrenci_adi", "?")} - '
                f'{filtered[i].get("tur", "?")} - '
                f'{filtered[i].get("tarih", "?")}'
            ),
            key="redownload_sel",
        )

        if sel_cert_idx is not None and sel_cert_idx < len(filtered):
            cert = filtered[sel_cert_idx]
            stu = stu_map.get(cert.get("student_id", ""), {})
            ogrenci_adi = cert.get("ogrenci_adi", "?")
            sinif_str = f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}. Sinif'
            tarih_str = cert.get("tarih", "")
            try:
                tarih_display = date.fromisoformat(tarih_str).strftime("%d.%m.%Y")
            except (ValueError, TypeError):
                tarih_display = tarih_str
            etkinlik = cert.get("aciklama", "")
            imzalayan = cert.get("veren", "Okul Muduru")
            tur = cert.get("tur", "Basari Belgesi")

            c_pdf, c_html = st.columns(2)
            with c_pdf:
                if HAS_REPORTLAB:
                    pdf_bytes = _generate_cert_pdf(
                        template=tur, ogrenci_adi=ogrenci_adi, sinif=sinif_str,
                        etkinlik=etkinlik, tarih=tarih_display, imzalayan=imzalayan,
                    )
                    if pdf_bytes:
                        fname = f"sertifika_{ogrenci_adi.replace(' ', '_')}.pdf"
                        st.download_button("PDF Indir", pdf_bytes, file_name=fname,
                                           mime="application/pdf", key="redown_pdf")
                else:
                    st.info("PDF icin ReportLab gerekli.")

            with c_html:
                html_content = _generate_html_download(
                    template=tur, ogrenci_adi=ogrenci_adi, sinif=sinif_str,
                    etkinlik=etkinlik, tarih=tarih_display, imzalayan=imzalayan,
                )
                fname = f"sertifika_{ogrenci_adi.replace(' ', '_')}.html"
                st.download_button("HTML Indir", html_content.encode("utf-8"),
                                   file_name=fname, mime="text/html", key="redown_html")
    else:
        st.warning("Filtrelere uygun sertifika bulunamadi.")


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_sertifika_uretici():
    """Sertifika Uretici Modulu ana giris noktasi."""

    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown(
        '<div class="cert-header">'
        '<h2>Sertifika Uretici</h2>'
        '<p>Basari, katilim, tesekkur ve takdir belgeleri olusturma sistemi</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Load data
    students = _load_students()
    sertifikalar = _load_sertifikalar()

    tab1, tab2, tab3 = st.tabs([
        "Sertifika Olustur",
        "Toplu Sertifika",
        "Sertifika Arsivi",
    ])

    with tab1:
        _tab_sertifika_olustur(students, sertifikalar)
    with tab2:
        _tab_toplu_sertifika(students, sertifikalar)
    with tab3:
        _tab_arsiv(students, sertifikalar)
