"""
Akademik Takvim — Yillik Calisma Plani + Kurumsal PDF
=======================================================
A'dan Z'ye tum faaliyetler — yillik/aylik gorunum + PDF export
"""
from __future__ import annotations

import io
import os
from collections import Counter
from datetime import date, datetime

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

_AY_ADLARI = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
               7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}

_AY_SIRASI_EGITIM = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]  # Eylul → Agustos


def _load_kurum():
    try:
        from utils.shared_data import load_kurum_profili
        return load_kurum_profili() or {}
    except Exception:
        return {}


def render_yillik_calisma_plani(data: dict, events: list):
    """Yillik calisma plani — A'dan Z'ye + kurumsal PDF."""
    styled_section("Yillik Calisma Plani", "#1a237e")
    styled_info_banner(
        "Tum akademik yil faaliyetleri: sinav, gezi, seminer, tatil, toplanti, toren, "
        "kayit donemi — aylık goruntuleme + kurumsal kapakli baskiya hazir PDF.",
        banner_type="info", icon="📑")

    bugun = date.today()
    # Egitim yili (Eylul-Agustos)
    if bugun.month >= 9:
        yil_bas = bugun.year
    else:
        yil_bas = bugun.year - 1
    yil_bit = yil_bas + 1
    egitim_yili = f"{yil_bas}-{yil_bit}"

    # Doneler
    donemler = data.get("semesters", [])

    # Tum etkinlikleri egitim yilina filtrele
    egitim_yili_bas = f"{yil_bas}-09-01"
    egitim_yili_bit = f"{yil_bit}-08-31"
    yil_events = [e for e in events
                    if egitim_yili_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= egitim_yili_bit]

    # Tur sayaci
    tur_sayac = Counter(e.get("type", e.get("tur", "Diger")) for e in yil_events)

    styled_stat_row([
        ("Egitim Yili", egitim_yili, "#1a237e", "📅"),
        ("Toplam Faaliyet", str(len(yil_events)), "#2563eb", "📋"),
        ("Faaliyet Turu", str(len(tur_sayac)), "#7c3aed", "🏷️"),
    ])

    sub = st.tabs(["📊 Yillik Ozet", "📅 Aylik Goruntule", "📑 PDF Indir"])

    # ═══ YILLIK ÖZET ═══
    with sub[0]:
        styled_section(f"{egitim_yili} Egitim Yili Ozet")

        # Tur dagilimi
        if tur_sayac:
            styled_section("Faaliyet Turu Dagilimi")
            en_cok = tur_sayac.most_common(1)[0][1] if tur_sayac else 1
            for tur, sayi in tur_sayac.most_common():
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="min-width:180px;font-size:11px;color:#e2e8f0;font-weight:600;">{tur}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:16px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#2563eb;border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

        # Aylik dagilim
        styled_section("Aylik Faaliyet Dagilimi")
        for ay in _AY_SIRASI_EGITIM:
            yil = yil_bas if ay >= 9 else yil_bit
            ay_str = f"{yil}-{ay:02d}"
            ay_events = [e for e in yil_events if (e.get("date", e.get("tarih", "")) or "")[:7] == ay_str]
            ay_adi = _AY_ADLARI.get(ay, str(ay))
            bar_w = min(len(ay_events) * 5, 100)
            renk = "#ef4444" if len(ay_events) > 15 else "#f59e0b" if len(ay_events) > 8 else "#10b981"
            is_current = ay == bugun.month and yil == bugun.year

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;
                        {'border-left:3px solid #c9a84c;padding-left:8px;' if is_current else ''}">
                <span style="min-width:55px;font-size:11px;color:{'#c9a84c' if is_current else '#e2e8f0'};
                            font-weight:{'800' if is_current else '600'};">{'> ' if is_current else ''}{ay_adi}</span>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:8px;color:#fff;font-weight:700;">{len(ay_events)}</span></div></div>
            </div>""", unsafe_allow_html=True)

    # ═══ AYLIK GÖRÜNTÜLE ═══
    with sub[1]:
        styled_section("Aylik Detayli Goruntuleme")
        secili_ay = st.selectbox("Ay Secin", _AY_SIRASI_EGITIM,
                                   format_func=lambda x: _AY_ADLARI.get(x, str(x)),
                                   index=_AY_SIRASI_EGITIM.index(bugun.month) if bugun.month in _AY_SIRASI_EGITIM else 0,
                                   key="yp_ay")

        yil = yil_bas if secili_ay >= 9 else yil_bit
        ay_str = f"{yil}-{secili_ay:02d}"
        ay_events = sorted(
            [e for e in yil_events if (e.get("date", e.get("tarih", "")) or "")[:7] == ay_str],
            key=lambda e: e.get("date", e.get("tarih", ""))
        )

        st.caption(f"{_AY_ADLARI[secili_ay]} {yil} — {len(ay_events)} faaliyet")

        if not ay_events:
            st.info("Bu ayda faaliyet yok.")
        else:
            for e in ay_events:
                tarih = (e.get("date", e.get("tarih", "")) or "")[:10]
                baslik = e.get("title", e.get("baslik", ""))
                tur = e.get("type", e.get("tur", ""))
                kademe = e.get("kademe", "")
                konum = e.get("location", e.get("konum", ""))
                aciklama = e.get("description", e.get("aciklama", ""))
                bitis = e.get("end_date", e.get("bitis_tarihi", ""))

                from views.academic_calendar import EVENT_COLORS
                renk = EVENT_COLORS.get(tur, "#607D8B")

                tarih_txt = tarih[8:10] + "." + tarih[5:7] if tarih else ""
                bitis_txt = f" — {bitis[8:10]}.{bitis[5:7]}" if bitis else ""

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                            border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <div>
                            <span style="font-weight:800;color:#e2e8f0;font-size:13px;">{baslik}</span>
                            <span style="color:#94a3b8;font-size:10px;margin-left:8px;">({tur})</span>
                        </div>
                        <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
                                    font-size:10px;font-weight:700;">{tarih_txt}{bitis_txt}</span>
                    </div>
                    <div style="font-size:10px;color:#94a3b8;">
                        {f'Kademe: {kademe}' if kademe else ''}{f' · Konum: {konum}' if konum else ''}
                        {f' · {aciklama[:60]}' if aciklama else ''}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ PDF İNDİR ═══
    with sub[2]:
        styled_section("Kurumsal Yillik Calisma Plani PDF")
        styled_info_banner(
            "Kurum logosu + kapak sayfasi + aylık faaliyet tablolari — "
            "baskiya hazir profesyonel yillik calisma plani.",
            banner_type="info", icon="📑")

        pdf_tip = st.radio("PDF Tipi", ["Yillik (Tum Yil)", "Aylik (Secili Ay)"], horizontal=True, key="yp_pdf_tip")

        if pdf_tip == "Aylik (Secili Ay)":
            pdf_ay = st.selectbox("Ay", _AY_SIRASI_EGITIM,
                                    format_func=lambda x: _AY_ADLARI.get(x, str(x)), key="yp_pdf_ay")
        else:
            pdf_ay = None

        if st.button("PDF Olustur ve Indir", key="yp_pdf_btn", type="primary", use_container_width=True):
            with st.spinner("Kurumsal PDF olusturuluyor..."):
                pdf_bytes = _generate_yillik_plan_pdf(
                    yil_events, egitim_yili, yil_bas, yil_bit, donemler, pdf_ay)

            if pdf_bytes:
                dosya_adi = f"yillik_calisma_plani_{egitim_yili}.pdf" if not pdf_ay else f"aylik_plan_{_AY_ADLARI.get(pdf_ay, '')}_{yil_bas if pdf_ay >= 9 else yil_bit}.pdf"
                st.download_button("PDF Indir", pdf_bytes, file_name=dosya_adi,
                                   mime="application/pdf", use_container_width=True, key="yp_pdf_dl")
                st.success("PDF hazir!")
            else:
                st.error("PDF olusturulamadi.")


def _generate_yillik_plan_pdf(events: list, egitim_yili: str, yil_bas: int, yil_bit: int,
                                donemler: list, sadece_ay: int | None = None) -> bytes:
    """Ultra profesyonel kurumsal yillik calisma plani PDF.
    Her ay kendi sayfasinda, sarkma yok, kuse gorunumlu, renkli tablolar."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                          PageBreak, KeepTogether, HRFlowable)
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        import streamlit as _st
        _st.error("PDF olusturmak icin 'reportlab' kutuphanesi gereklidir. Lutfen: pip install reportlab")
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()

    # ── RENK PALETİ (kuşe/premium) ──
    NAVY = colors.HexColor('#0B1E3F')
    DARK_NAVY = colors.HexColor('#060E1F')
    GOLD = colors.HexColor('#C8952E')
    LIGHT_GOLD = colors.HexColor('#E8D48B')
    WHITE = colors.white
    CREAM = colors.HexColor('#FDFBF5')
    LIGHT_GRAY = colors.HexColor('#F1F5F9')
    MID_GRAY = colors.HexColor('#94A3B8')
    DARK_GRAY = colors.HexColor('#334155')

    # Tur renkleri
    _TUR_RENK = {
        "Sinav": colors.HexColor('#DC2626'), "Yazili Sinav": colors.HexColor('#DC2626'),
        "Sozlu Sinav": colors.HexColor('#DC2626'), "Deneme Sinavi (LGS/TYT/AYT)": colors.HexColor('#991B1B'),
        "Resmi Tatil": colors.HexColor('#7C3AED'), "Yariyil Tatili": colors.HexColor('#7C3AED'),
        "Ara Tatil": colors.HexColor('#7C3AED'), "Somestre Tatili": colors.HexColor('#7C3AED'),
        "Toplanti": colors.HexColor('#2563EB'), "Ogretmenler Kurulu": colors.HexColor('#1E40AF'),
        "Gezi / Gozlem": colors.HexColor('#059669'), "Seminer / Konferans": colors.HexColor('#0891B2'),
        "Kutlama / Anma / Toren": colors.HexColor('#DB2777'), "Mezuniyet": colors.HexColor('#DB2777'),
        "Karne Gunu": colors.HexColor('#0891B2'), "Spor Etkinligi": colors.HexColor('#65A30D'),
    }

    kurum = _load_kurum()
    kurum_adi = kurum.get("kurum_adi", kurum.get("name", kurum.get("okul_adi", "SmartCampus AI")))
    vizyon = kurum.get("vision", kurum.get("vizyon", ""))
    adres = kurum.get("address", kurum.get("adres", ""))
    telefon = kurum.get("phone", kurum.get("telefon", ""))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=1.8*cm, rightMargin=1.8*cm)
    elements = []
    W = 17.4 * cm  # kullanilabilir genislik

    # ── STILLER ──
    s_kurum = ParagraphStyle('kurum', fontSize=22, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY, spaceAfter=4)
    s_slogan = ParagraphStyle('slogan', fontSize=9, fontName=font_name, alignment=TA_CENTER, textColor=MID_GRAY, spaceAfter=6)
    s_baslik = ParagraphStyle('baslik', fontSize=28, fontName=font_bold, alignment=TA_CENTER, textColor=GOLD, spaceAfter=10)
    s_alt = ParagraphStyle('alt', fontSize=14, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY, spaceAfter=4)
    s_tarih = ParagraphStyle('tarih', fontSize=9, fontName=font_name, alignment=TA_CENTER, textColor=MID_GRAY)
    s_ay_baslik = ParagraphStyle('ay', fontSize=16, fontName=font_bold, textColor=WHITE, spaceAfter=0)
    s_ay_alt = ParagraphStyle('ay_alt', fontSize=9, fontName=font_name, textColor=LIGHT_GOLD, spaceAfter=0)
    s_footer = ParagraphStyle('footer', fontSize=7, fontName=font_name, alignment=TA_CENTER, textColor=MID_GRAY)
    s_bos = ParagraphStyle('bos', fontSize=10, fontName=font_name, textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=8)

    # ════════════════════════════════════════════
    # KAPAK SAYFASI
    # ════════════════════════════════════════════
    elements.append(Spacer(1, 2*cm))

    # Ust gold cizgi
    elements.append(HRFlowable(width="100%", thickness=3, color=GOLD, spaceAfter=0.5*cm))

    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph(kurum_adi, s_kurum))

    if vizyon:
        elements.append(Paragraph(f'"{vizyon[:150]}"', s_slogan))
    if adres:
        elements.append(Paragraph(adres, ParagraphStyle('adres', fontSize=8, fontName=font_name, alignment=TA_CENTER, textColor=MID_GRAY, spaceAfter=2)))
    if telefon:
        elements.append(Paragraph(f"Tel: {telefon}", ParagraphStyle('tel', fontSize=8, fontName=font_name, alignment=TA_CENTER, textColor=MID_GRAY, spaceAfter=8)))

    elements.append(Spacer(1, 2*cm))

    # Buyuk baslik blogu
    kapak_tbl = Table([
        [Paragraph("YILLIK CALISMA PLANI", ParagraphStyle('kb', fontSize=26, fontName=font_bold, alignment=TA_CENTER, textColor=WHITE))],
        [Paragraph(f"{egitim_yili} Egitim Ogretim Yili", ParagraphStyle('ky', fontSize=13, fontName=font_bold, alignment=TA_CENTER, textColor=LIGHT_GOLD))],
    ], colWidths=[W])
    kapak_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
        ('BOX', (0, 0), (-1, -1), 2, GOLD),
        ('LINEBELOW', (0, 0), (-1, 0), 1, GOLD),
    ]))
    elements.append(kapak_tbl)

    elements.append(Spacer(1, 2*cm))

    if sadece_ay:
        elements.append(Paragraph(f"{_AY_ADLARI.get(sadece_ay, '')} Ayi Calisma Plani", s_alt))

    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"Olusturma Tarihi: {date.today().strftime('%d.%m.%Y')}", s_tarih))

    # Alt gold cizgi
    elements.append(Spacer(1, 1.5*cm))
    elements.append(HRFlowable(width="100%", thickness=3, color=GOLD, spaceBefore=0.5*cm))

    elements.append(PageBreak())

    # ════════════════════════════════════════════
    # GENEL OZET SAYFASI
    # ════════════════════════════════════════════
    # Baslik bandi
    ozet_baslik = Table([
        [Paragraph("GENEL OZET", ParagraphStyle('ob', fontSize=14, fontName=font_bold, textColor=WHITE))],
    ], colWidths=[W])
    ozet_baslik.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('LINEBELOW', (0, 0), (-1, -1), 2, GOLD),
    ]))
    elements.append(ozet_baslik)
    elements.append(Spacer(1, 0.5*cm))

    tur_sayac = Counter(e.get("type", e.get("tur", "Diger")) for e in events)

    # Ozet metrik tablosu
    ozet_data = [
        [Paragraph("<b>Metrik</b>", ParagraphStyle('oh', fontSize=9, fontName=font_bold, textColor=WHITE)),
         Paragraph("<b>Deger</b>", ParagraphStyle('oh2', fontSize=9, fontName=font_bold, textColor=WHITE, alignment=TA_RIGHT))],
        ["Egitim Yili", egitim_yili],
        ["Toplam Faaliyet", str(len(events))],
        ["Faaliyet Turu Sayisi", str(len(tur_sayac))],
    ]
    for tur, sayi in tur_sayac.most_common(15):
        ozet_data.append([f"    {tur}", str(sayi)])

    ozet_tbl = Table(ozet_data, colWidths=[12*cm, 5.4*cm])
    ozet_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('BOX', (0, 0), (-1, -1), 1.5, NAVY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, 0), 2, GOLD),
    ]))
    elements.append(ozet_tbl)

    # Aylik dagılım mini tablo
    elements.append(Spacer(1, 0.6*cm))
    ay_baslik_tbl = Table([
        [Paragraph("AYLIK FAALIYET DAGILIMI", ParagraphStyle('ab', fontSize=11, fontName=font_bold, textColor=WHITE))],
    ], colWidths=[W])
    ay_baslik_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(ay_baslik_tbl)

    ay_header = ["Ay"]
    ay_row = ["Faaliyet"]
    aylar_list = [sadece_ay] if sadece_ay else _AY_SIRASI_EGITIM
    for ay in aylar_list:
        yil = yil_bas if ay >= 9 else yil_bit
        ay_str = f"{yil}-{ay:02d}"
        sayi = sum(1 for e in events if (e.get("date", e.get("tarih", "")) or "")[:7] == ay_str)
        ay_header.append(_AY_ADLARI.get(ay, "")[:3])
        ay_row.append(str(sayi))

    ay_tbl = Table([ay_header, ay_row], colWidths=[2.5*cm] + [((W - 2.5*cm) / len(aylar_list))] * len(aylar_list))
    ay_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, -1), font_bold),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOX', (0, 0), (-1, -1), 1, NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CREAM]),
    ]))
    elements.append(ay_tbl)

    elements.append(PageBreak())

    # ════════════════════════════════════════════
    # AYLIK DETAY SAYFALARI (HER AY AYRI SAYFA)
    # ════════════════════════════════════════════
    for ay in aylar_list:
        yil = yil_bas if ay >= 9 else yil_bit
        ay_str = f"{yil}-{ay:02d}"
        ay_events = sorted(
            [e for e in events if (e.get("date", e.get("tarih", "")) or "")[:7] == ay_str],
            key=lambda e: e.get("date", e.get("tarih", ""))
        )
        ay_adi = _AY_ADLARI.get(ay, str(ay))

        # ── AY BAŞLIK BANDI (navy + gold) ──
        ay_baslik_content = Table([
            [Paragraph(f"{ay_adi} {yil}", s_ay_baslik),
             Paragraph(f"{len(ay_events)} Faaliyet", s_ay_alt)],
        ], colWidths=[W * 0.65, W * 0.35])
        ay_baslik_content.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), NAVY),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (0, -1), 14),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('RIGHTPADDING', (1, 0), (1, -1), 14),
            ('LINEBELOW', (0, 0), (-1, -1), 3, GOLD),
        ]))
        elements.append(ay_baslik_content)
        elements.append(Spacer(1, 0.4*cm))

        if not ay_events:
            elements.append(Paragraph("Bu ayda planlanmis faaliyet bulunmamaktadir.", s_bos))
        else:
            # Tablo basligi
            header = [
                Paragraph("<b>#</b>", ParagraphStyle('h', fontSize=7, fontName=font_bold, textColor=WHITE, alignment=TA_CENTER)),
                Paragraph("<b>Tarih</b>", ParagraphStyle('h', fontSize=7, fontName=font_bold, textColor=WHITE, alignment=TA_CENTER)),
                Paragraph("<b>Faaliyet Adi</b>", ParagraphStyle('h', fontSize=7, fontName=font_bold, textColor=WHITE)),
                Paragraph("<b>Faaliyet Turu</b>", ParagraphStyle('h', fontSize=7, fontName=font_bold, textColor=WHITE)),
                Paragraph("<b>Kademe</b>", ParagraphStyle('h', fontSize=7, fontName=font_bold, textColor=WHITE, alignment=TA_CENTER)),
                Paragraph("<b>Konum</b>", ParagraphStyle('h', fontSize=7, fontName=font_bold, textColor=WHITE)),
            ]
            rows = [header]

            for idx, e in enumerate(ay_events, 1):
                tarih = (e.get("date", e.get("tarih", "")) or "")[:10]
                tarih_fmt = f"{tarih[8:10]}.{tarih[5:7]}.{tarih[:4]}" if len(tarih) >= 10 else ""
                bitis = e.get("end_date", e.get("bitis_tarihi", ""))
                if bitis and bitis != tarih:
                    tarih_fmt += f"\n{bitis[8:10]}.{bitis[5:7]}"

                baslik = (e.get("title", e.get("baslik", "")) or "")[:45]
                tur = (e.get("type", e.get("tur", "")) or "")[:25]
                kademe = (e.get("kademe", "") or "")[:18]
                konum = (e.get("location", e.get("konum", "")) or "")[:22]

                # Tur rengine gore sol kenar
                rows.append([
                    Paragraph(str(idx), ParagraphStyle('n', fontSize=7, fontName=font_bold, alignment=TA_CENTER)),
                    Paragraph(tarih_fmt, ParagraphStyle('t', fontSize=7, fontName=font_name, alignment=TA_CENTER)),
                    Paragraph(f"<b>{baslik}</b>", ParagraphStyle('b', fontSize=7, fontName=font_bold)),
                    Paragraph(tur, ParagraphStyle('tu', fontSize=7, fontName=font_name)),
                    Paragraph(kademe, ParagraphStyle('k', fontSize=7, fontName=font_name, alignment=TA_CENTER)),
                    Paragraph(konum, ParagraphStyle('ko', fontSize=7, fontName=font_name)),
                ])

            col_widths = [0.8*cm, 2.2*cm, 5.5*cm, 3.5*cm, 2.4*cm, 3*cm]
            tbl = Table(rows, colWidths=col_widths, repeatRows=1)

            # Satir renklendirme — tur bazli sol kenar efekti
            tbl_style = [
                ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
                ('FONTNAME', (0, 0), (-1, 0), font_bold),
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('ALIGN', (4, 0), (4, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#E2E8F0')),
                ('BOX', (0, 0), (-1, -1), 1.5, NAVY),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, 0), 2, GOLD),
            ]

            # Zebra satirlar
            for i in range(1, len(rows)):
                bg = CREAM if i % 2 == 0 else WHITE
                tbl_style.append(('BACKGROUND', (0, i), (-1, i), bg))

                # Tur rengine gore sol kenar (# sutunu)
                tur_str = ay_events[i - 1].get("type", ay_events[i - 1].get("tur", ""))
                tur_clr = _TUR_RENK.get(tur_str, DARK_GRAY)
                tbl_style.append(('BACKGROUND', (0, i), (0, i), tur_clr))
                tbl_style.append(('TEXTCOLOR', (0, i), (0, i), WHITE))

            tbl.setStyle(TableStyle(tbl_style))
            elements.append(tbl)

        # ── AY ALTI OZET ──
        elements.append(Spacer(1, 0.3*cm))
        if ay_events:
            ay_tur_sayac = Counter(e.get("type", e.get("tur", "Diger")) for e in ay_events)
            ozet_txt = " | ".join(f"{t}: {s}" for t, s in ay_tur_sayac.most_common(6))
            elements.append(Paragraph(
                f"<i>{ay_adi} ozet: {ozet_txt}</i>",
                ParagraphStyle('ao', fontSize=7, fontName=font_name, textColor=MID_GRAY, alignment=TA_LEFT)))

        # ── HER AY YENİ SAYFA ──
        if ay != aylar_list[-1]:
            elements.append(PageBreak())

    # ════════════════════════════════════════════
    # İMZA SAYFASI
    # ════════════════════════════════════════════
    elements.append(PageBreak())

    elements.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=1*cm))
    elements.append(Paragraph(f"{kurum_adi}", ParagraphStyle('ik', fontSize=14, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY, spaceAfter=4)))
    elements.append(Paragraph(f"{egitim_yili} Egitim Ogretim Yili Yillik Calisma Plani",
        ParagraphStyle('ia', fontSize=10, fontName=font_name, alignment=TA_CENTER, textColor=MID_GRAY, spaceAfter=2*cm)))

    # Onay blogu
    onay_data = [
        [Paragraph("<b>Hazirlayan</b>", ParagraphStyle('oh', fontSize=10, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY)),
         Paragraph("<b>Kontrol Eden</b>", ParagraphStyle('oh', fontSize=10, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY)),
         Paragraph("<b>Onaylayan</b>", ParagraphStyle('oh', fontSize=10, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY))],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["___________________", "___________________", "___________________"],
        ["Ad Soyad", "Ad Soyad", "Ad Soyad"],
        ["Mudur Yardimcisi", "Mudur Yardimcisi", "Okul Muduru"],
        ["Imza / Tarih", "Imza / Tarih", "Imza / Tarih / Muhur"],
    ]
    onay_tbl = Table(onay_data, colWidths=[W / 3] * 3)
    onay_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, NAVY),
        ('GRID', (0, 0), (-1, 0), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
        ('LINEBELOW', (0, 0), (-1, 0), 1, GOLD),
    ]))
    elements.append(onay_tbl)

    elements.append(Spacer(1, 1.5*cm))
    elements.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceBefore=0.5*cm))
    elements.append(Paragraph(
        f"{kurum_adi} — {egitim_yili} Yillik Calisma Plani — SmartCampus AI — {date.today().strftime('%d.%m.%Y')}",
        s_footer))

    doc.build(elements)
    return buf.getvalue()
