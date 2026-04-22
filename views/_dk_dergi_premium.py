"""
Smarti Dergi - Premium Magazine PDF Generator (WeasyPrint + HTML/CSS)
============================================================================
Produces world-class magazine-quality PDFs using HTML/CSS rendered via WeasyPrint.
All images embedded as base64 data URIs for self-contained output.
"""
import streamlit as st
import base64
import os
from io import BytesIO

from views._dk_dergi_pdf import DERGI_DATA, DERGI_IMG_DIR, MASCOT_PATH, generate_dergi_images

# ---------------------------------------------------------------------------
# IMAGE HELPER
# ---------------------------------------------------------------------------
def _img_uri(path):
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        ext = path.rsplit(".", 1)[-1].lower()
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "gif": "gif", "webp": "webp"}.get(ext, "png")
        return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; padding: 0; font-family: Georgia, 'Times New Roman', serif; color: #1f2937; }

.page {
    width: 210mm; min-height: 297mm; position: relative;
    background: linear-gradient(170deg, #fffdf9, #faf8f5, #f5f1ec);
    padding: 12mm 15mm 15mm 15mm;
    page-break-after: always;
    overflow: hidden;
}

.page-hdr {
    position: absolute; top: 0; left: 0; right: 0; height: 7mm;
    background: linear-gradient(90deg, #0a0e27, #1a1a2e, #0a0e27);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 15mm; font-size: 7pt; color: #c9a84c;
    letter-spacing: 1px;
}

.page-ftr {
    position: absolute; bottom: 0; left: 0; right: 0; height: 6mm;
    background: #0a0e27;
    display: flex; align-items: center; justify-content: center;
    font-size: 7pt; color: #c9a84c;
}

.section-bar {
    background: linear-gradient(135deg, #0a0e27, #1a1a2e);
    color: #c9a84c; padding: 10px 18px;
    font-size: 16pt; font-weight: 900; letter-spacing: 4px;
    text-transform: uppercase;
    border-left: 5px solid #c9a84c;
    margin: 0 -15mm 12px -15mm; padding-left: 15mm;
}

.article-title {
    font-size: 20pt; font-weight: 700; color: #0a0e27;
    border-bottom: 2px solid #c9a84c; padding-bottom: 5px;
    margin-bottom: 10px; line-height: 1.2;
}

.two-col { column-count: 2; column-gap: 18px; column-rule: 1px solid #e5e7eb; }
.body { font-size: 10pt; line-height: 1.75; text-align: justify; }

.pull-quote {
    background: linear-gradient(135deg, #fef9c3, #fef08a);
    border-left: 4px solid #c9a84c; padding: 12px 16px;
    margin: 12px 0; font-style: italic; font-size: 11pt;
    color: #78350f; position: relative;
}

.info-box {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #93c5fd; border-radius: 6px;
    padding: 10px 14px; margin: 10px 0; font-size: 9pt;
}
.info-box b { color: #1e40af; }

.green-box {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #86efac; border-radius: 6px;
    padding: 10px 14px; margin: 10px 0; font-size: 9pt;
}

.gold-line { height: 1.5px; background: linear-gradient(90deg, transparent, #c9a84c, transparent); margin: 10px 0; }

.img-full { width: 500px; border-radius: 6px; margin: 8px 0; box-shadow: 0 3px 12px rgba(0,0,0,0.12); }
.img-half { width: 240px; float: right; margin: 0 0 8px 12px; border-radius: 6px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
.img-caption { font-size: 7.5pt; color: #9ca3af; text-align: center; font-style: italic; }

.tbl { width: 500px; border-collapse: collapse; margin: 8px 0; font-size: 9pt; }
.tbl th { background: #0a0e27; color: #c9a84c; padding: 7px 10px; text-align: left; }
.tbl td { padding: 5px 10px; border-bottom: 1px solid #e5e7eb; }
.tbl tr:nth-child(even) td { background: #f8fafc; }

.quiz-q { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 6px; padding: 8px 12px; margin: 6px 0; font-size: 9.5pt; }

.poem-box {
    border: 2px solid #c9a84c; border-radius: 10px; padding: 20px;
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    margin: 12px 0; text-align: center;
}
.poem-box .poem-title { font-size: 14pt; font-weight: 700; color: #0a0e27; margin-bottom: 4px; }
.poem-box .poem-poet { font-size: 9pt; color: #78350f; margin-bottom: 10px; }
.poem-box .poem-text { font-size: 10pt; line-height: 2; font-style: italic; color: #1f2937; white-space: pre-line; }

.quote-card {
    background: linear-gradient(135deg, #0a0e27, #1a1a2e);
    color: #c9a84c; padding: 12px 16px; border-radius: 8px;
    margin: 6px 0; font-size: 10pt; font-style: italic;
}
.quote-card .q-author { font-size: 8pt; color: #94a3b8; text-align: right; margin-top: 4px; font-style: normal; }
.quote-card .q-cat { font-size: 7pt; color: #64748b; float: left; }

.cover-page {
    width: 210mm; min-height: 297mm; position: relative;
    background: linear-gradient(170deg, #0a0e27 0%, #1a1a2e 40%, #0f172a 100%);
    page-break-after: always; overflow: hidden;
}

.timeline-item { border-left: 3px solid #c9a84c; padding: 5px 0 5px 12px; margin: 4px 0; font-size: 9pt; }
.timeline-item b { color: #0a0e27; }

.sub-title { font-size: 13pt; font-weight: 700; color: #1e40af; margin: 10px 0 5px 0; }
.small-title { font-size: 11pt; font-weight: 700; color: #0a0e27; margin: 8px 0 4px 0; }
"""


# ---------------------------------------------------------------------------
# PAGE HELPERS
# ---------------------------------------------------------------------------
def _page_start(ay, sayi, tema, page_num):
    return f'''<div class="page">
    <div class="page-hdr"><span>Smarti Dergi</span><span>{ay} | {tema}</span></div>'''


def _page_end(page_num):
    return f'''<div class="page-ftr">Sayfa {page_num} | Smarti Dergi</div></div>'''


def _paragraphs(text):
    """Convert \\n\\n separated text to <p> tags."""
    return "".join(f"<p>{p.strip()}</p>" for p in text.split("\n\n") if p.strip())


# ---------------------------------------------------------------------------
# SECTION BUILDERS
# ---------------------------------------------------------------------------
def _cover_page(data, cover_img, mascot_img):
    ay = data["ay"]
    sayi = data["sayi"]
    tema = data["tema"]
    teasers_html = ""
    for t, pg in data.get("kapak_teasers", []):
        teasers_html += f'<div style="color:#c9a84c;font-size:11pt;margin:4px 0;letter-spacing:1px;">&#9670; {t} <span style="font-size:8pt;color:#94a3b8;">s.{pg}</span></div>'

    cover_bg = f'<img src="{cover_img}" style="position:absolute;top:0;left:0;width:500px;height:100%;object-fit:cover;opacity:0.25;"/>' if cover_img else ""
    mascot_html = f'<img src="{mascot_img}" style="width:60px;height:60px;border-radius:50%;border:2px solid #c9a84c;"/>' if mascot_img else ""

    return f'''<div class="cover-page">
    {cover_bg}
    <div style="position:relative;z-index:2;padding:30mm 20mm 20mm 20mm;text-align:center;">
        {mascot_html}
        <div style="margin-top:15px;font-size:9pt;color:#94a3b8;letter-spacing:6px;text-transform:uppercase;">Aylik Egitim ve Kultur Dergisi</div>
        <div style="font-size:42pt;font-weight:900;color:#c9a84c;letter-spacing:3px;margin:10px 0;">SmartCampus</div>
        <div style="font-size:18pt;color:#e2e8f0;letter-spacing:8px;text-transform:uppercase;">Smarti</div>
        <div style="height:2px;background:linear-gradient(90deg,transparent,#c9a84c,transparent);margin:15px auto;width:60%;"></div>
        <div style="font-size:14pt;color:#e2e8f0;margin:8px 0;">{ay} | Sayi {sayi}</div>
        <div style="font-size:24pt;font-weight:700;color:#c9a84c;margin:10px 0;font-style:italic;">{tema}</div>
        <div style="margin-top:30px;text-align:left;max-width:70%;margin-left:auto;margin-right:auto;">
            {teasers_html}
        </div>
        <div style="position:absolute;bottom:25mm;left:0;right:0;text-align:center;">
            <div style="font-size:8pt;color:#64748b;letter-spacing:2px;">UCRETSIZ DIJITAL YAYIN</div>
        </div>
    </div>
</div>'''


def _toc_editorial(data, mascot_img):
    toc_rows = ""
    for title, pg in data.get("icerik_tablosu", []):
        toc_rows += f'<tr><td style="padding:3px 8px;font-size:9pt;">{title}</td><td style="padding:3px 8px;font-size:9pt;text-align:right;color:#c9a84c;font-weight:700;">{pg}</td></tr>'

    mascot = f'<img src="{mascot_img}" style="width:40px;height:40px;border-radius:50%;float:left;margin-right:10px;"/>' if mascot_img else ""
    editorial_paras = _paragraphs(data.get("editorial", ""))

    return f'''
    <div class="section-bar">Icerik</div>
    <table class="tbl" style="margin-bottom:15px;">
        <tr><th>Bolum</th><th style="text-align:right;">Sayfa</th></tr>
        {toc_rows}
    </table>
    <div class="gold-line"></div>
    <div class="section-bar">Editorden</div>
    {mascot}
    <div class="body" style="font-size:9.5pt;">
        {editorial_paras}
    </div>'''


def _bilim_section(data, img):
    articles = data.get("bilim_teknik", [])
    glossary = data.get("bilim_sozlugu", [])
    facts = articles[0].get("biliyor_muydunuz", []) if articles else []

    html = '<div class="section-bar">Bilim & Teknik</div>'

    for i, art in enumerate(articles):
        img_html = ""
        if i == 0 and img:
            img_html = f'<img src="{img}" class="img-half"/>'
        html += f'''
        <div class="article-title">{art.get("baslik", "")}</div>
        {img_html}
        <div class="pull-quote">{art.get("giris", "")}</div>
        <div class="two-col body">{_paragraphs(art.get("icerik", ""))}</div>
        <div class="gold-line"></div>'''

    if facts:
        html += '<div class="info-box"><b>Biliyor Muydunuz?</b><ul>'
        for f in facts:
            html += f'<li>{f}</li>'
        html += '</ul></div>'

    if glossary:
        html += '<div class="small-title">Bilim Sozlugu</div><table class="tbl"><tr><th>Terim</th><th>Aciklama</th></tr>'
        for term, desc in glossary:
            html += f'<tr><td style="font-weight:700;width:25%;">{term}</td><td>{desc}</td></tr>'
        html += '</table>'

    return html


def _teknoloji_section(data, img):
    tech = data.get("teknoloji", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    news_html = ""
    for n in tech.get("haberler", []):
        news_html += f'<li>{n}</li>'

    return f'''
    <div class="section-bar">Teknoloji</div>
    <div class="article-title">{tech.get("baslik", "")}</div>
    {img_html}
    <div class="two-col body">{_paragraphs(tech.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Teknoloji Haberleri</b><ul>{news_html}</ul></div>
    <div class="green-box"><b>Gelecekte Bu Var</b><br/>{tech.get("gelecekte_bu_var", "")}</div>'''


def _tarih_section(data, img):
    tarih = data.get("tarih", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    timeline = ""
    for yr, desc in tarih.get("zaman_cizelgesi", []):
        timeline += f'<div class="timeline-item"><b>{yr}</b> &mdash; {desc}</div>'

    bu_ay = ""
    for item in tarih.get("tarihte_bu_ay", []):
        bu_ay += f'<li>{item}</li>'

    soz = tarih.get("tarih_sozu", {})
    soz_html = f'<div class="pull-quote">"{soz.get("soz", "")}" &mdash; <b>{soz.get("kisi", "")}</b></div>' if soz else ""

    return f'''
    <div class="section-bar">Tarih</div>
    <div class="article-title">{tarih.get("baslik", "")}</div>
    {img_html}
    <div class="two-col body">{_paragraphs(tarih.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="small-title">Zaman Cizelgesi</div>
    {timeline}
    <div class="gold-line"></div>
    <div class="info-box"><b>Tarihte Bu Ay</b><ul>{bu_ay}</ul></div>
    {soz_html}'''


def _gezi_section(data, img):
    gezi = data.get("cografya_gezi", {})
    img_html = f'<img src="{img}" class="img-full"/>' if img else ""

    bilgi = gezi.get("baskent_bilgi", {})
    bilgi_rows = "".join(f'<tr><td style="font-weight:700;width:30%;">{k.title()}</td><td>{v}</td></tr>' for k, v in bilgi.items())

    gorulmesi = "".join(f'<li>{g}</li>' for g in gezi.get("gorulmesi_gereken", []))
    yemek = "".join(f'<li>{y}</li>' for y in gezi.get("yemek_onerileri", []))

    return f'''
    <div class="section-bar">Cografya & Gezi</div>
    <div class="article-title">{gezi.get("yer", "")} - {gezi.get("ulke", "")}</div>
    {img_html}
    <table class="tbl"><tr><th colspan="2">Genel Bilgiler</th></tr>{bilgi_rows}</table>
    <div class="two-col body">{_paragraphs(gezi.get("tanitim", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Gorulmesi Gereken Yerler</b><ul>{gorulmesi}</ul></div>
    <div class="green-box"><b>Lezzet Duraklari</b><ul>{yemek}</ul></div>
    <div class="pull-quote">{gezi.get("harita_aciklama", "")}</div>'''


def _doga_section(data, img):
    doga = data.get("doga_cevre", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    turler = ""
    for ad, aciklama in doga.get("nesli_tehlike", []):
        turler += f'<tr><td style="font-weight:700;width:25%;color:#dc2626;">{ad}</td><td>{aciklama}</td></tr>'

    tips = "".join(f'<li>{t}</li>' for t in doga.get("eko_ipuclari", []))

    return f'''
    <div class="section-bar">Doga & Cevre</div>
    <div class="article-title">{doga.get("baslik", "")}</div>
    {img_html}
    <div class="two-col body">{_paragraphs(doga.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Nesli Tehlike Altindaki Turler</b>
        <table class="tbl"><tr><th>Tur</th><th>Durum</th></tr>{turler}</table>
    </div>
    <div class="green-box"><b>Eko Ipuclari</b><ul>{tips}</ul></div>
    <div class="pull-quote">{doga.get("mevsim_gozlem", "")}</div>'''


def _edebiyat_section(data, img):
    ed = data.get("edebiyat", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    onerileri = ""
    for b in ed.get("bu_ay_okuyun", []):
        onerileri += f'<tr><td style="font-weight:700;">{b["kitap"]}</td><td>{b["yazar"]}</td><td>{b.get("tur","")}</td><td>{b.get("sayfa","")}</td></tr>'

    soz = ed.get("edebi_soz", {})
    soz_html = f'<div class="pull-quote">"{soz.get("soz","")}" &mdash; <b>{soz.get("kisi","")}</b></div>' if soz else ""

    return f'''
    <div class="section-bar">Edebiyat</div>
    <div class="article-title">{ed.get("kitap", "")} &mdash; {ed.get("yazar", "")}</div>
    <div style="font-size:9pt;color:#64748b;margin-bottom:8px;">{ed.get("tur","")} | {ed.get("sayfa","")} sayfa</div>
    {img_html}
    <div class="two-col body">{_paragraphs(ed.get("tanitim", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Yazar Hakkinda</b><br/>{ed.get("yazar_bio", "")}</div>
    <div class="small-title">Bu Ay Okuyun</div>
    <table class="tbl"><tr><th>Kitap</th><th>Yazar</th><th>Tur</th><th>Sayfa</th></tr>{onerileri}</table>
    {soz_html}'''


def _siir_section(data):
    poems = data.get("siir", [])
    html = '<div class="section-bar">Siir Kosesi</div>'
    for poem in poems:
        html += f'''
        <div class="poem-box">
            <div class="poem-title">{poem.get("baslik","")}</div>
            <div class="poem-poet">{poem.get("sair","")}</div>
            <div class="poem-text">{poem.get("metin","")}</div>
        </div>
        <div class="info-box" style="font-size:8.5pt;"><b>Sair Hakkinda:</b> {poem.get("bio","")}</div>'''
    return html


def _psikoloji_section(data, img):
    psi = data.get("psikoloji", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    tips = "".join(f'<li>{t}</li>' for t in psi.get("stres_ipuclari", []))

    qa = ""
    for q, a in psi.get("soru_cevap", []):
        qa += f'<div class="quiz-q"><b>S: {q}</b><br/>{a}</div>'

    return f'''
    <div class="section-bar">Psikoloji & Rehberlik</div>
    <div class="article-title">{psi.get("baslik","")}</div>
    {img_html}
    <div class="two-col body">{_paragraphs(psi.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Kariyer Rehberligi</b><br/>{psi.get("rehberlik","")}</div>
    <div class="green-box"><b>Stres Yonetimi Ipuclari</b><ul>{tips}</ul></div>
    <div class="info-box"><b>Ozguven</b><br/>{psi.get("ozguven","")}</div>
    <div class="small-title">Soru &amp; Cevap</div>
    {qa}'''


def _veli_section(data):
    veli = data.get("veli", {})

    ev = "".join(f'<li>{e}</li>' for e in veli.get("ev_ortami", []))
    beslenme = "".join(f'<li>{b}</li>' for b in veli.get("beslenme", []))

    return f'''
    <div class="section-bar">Veli Kosesi</div>
    <div class="article-title">{veli.get("baslik","")}</div>
    <div class="two-col body">{_paragraphs(veli.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="green-box"><b>Ev Ortami Onerileri</b><ul>{ev}</ul></div>
    <div class="info-box"><b>Iletisim</b><br/>{veli.get("iletisim","")}</div>
    <div class="green-box"><b>Beslenme Onerileri</b><ul>{beslenme}</ul></div>
    <div class="pull-quote">{veli.get("aile_etkinlik","")}</div>'''


def _ogrenci_section(data):
    ogr = data.get("ogrenci_tavsiye", {})

    aliskanliklar = "".join(f'<li>{a}</li>' for a in ogr.get("aliskanliklar", []))
    motivasyon = "".join(f'<div class="pull-quote" style="font-size:9.5pt;">{m}</div>' for m in ogr.get("motivasyon_sozleri", []))

    return f'''
    <div class="section-bar">Ogrenci Tavsiyeleri</div>
    <div class="article-title">{ogr.get("baslik","")}</div>
    <div class="two-col body">{_paragraphs(ogr.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>10 Altin Aliskanlik</b><ol>{aliskanliklar}</ol></div>
    <div class="green-box"><b>Sinav Hazirlik Plani</b><br/>{ogr.get("sinav_hazirlik","")}</div>
    <div class="small-title">Haftalik Plan</div>
    <div class="info-box">{ogr.get("haftalik_plan","")}</div>
    <div class="small-title">Motivasyon</div>
    {motivasyon}'''


def _kultur_section(data, img):
    kultur = data.get("kultur_sanat", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    film = kultur.get("film", {})
    muzik = kultur.get("muzik", {})
    sanat = kultur.get("sanat_eseri", {})

    return f'''
    <div class="section-bar">Kultur & Sanat</div>
    <div class="article-title">{kultur.get("baslik","")}</div>
    {img_html}
    <div class="two-col body">{_paragraphs(kultur.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Film Onerisi: {film.get("ad","")}</b> ({film.get("yonetmen","")}, {film.get("yil","")})<br/>{film.get("aciklama","")}</div>
    <div class="green-box"><b>Muzik: {muzik.get("baslik","")}</b><br/>{muzik.get("aciklama","")}</div>
    <div class="info-box"><b>Sanat Eseri: {sanat.get("ad","")}</b> &mdash; {sanat.get("sanatci","")} ({sanat.get("yil","")})<br/>{sanat.get("aciklama","")}</div>
    <div class="pull-quote">{kultur.get("muze","")}</div>'''


def _spor_section(data, img):
    spor = data.get("spor", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    sporcu = spor.get("ayin_sporcusu", {})

    return f'''
    <div class="section-bar">Spor</div>
    <div class="article-title">{spor.get("baslik","")}</div>
    {img_html}
    <div class="two-col body">{_paragraphs(spor.get("icerik", ""))}</div>
    <div class="gold-line"></div>
    <div class="info-box"><b>Spor Tarihi</b><br/>{spor.get("spor_tarihi","")}</div>
    <div class="green-box"><b>Ayin Sporcusu: {sporcu.get("ad","")}</b> ({sporcu.get("dal","")})<br/>{sporcu.get("bilgi","")}</div>
    <div class="pull-quote"><b>Saglik Ipucu</b><br/>{spor.get("saglik_ipucu","")}</div>'''


def _hobi_section(data, img):
    hobi = data.get("hobi_kosesi", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""

    hobiler = ""
    for h in hobi.get("hobiler", []):
        emoji = h.get("emoji", "")
        hobiler += f'<div class="info-box"><b>{emoji} {h["ad"]}</b><br/>{h["aciklama"]}</div>'

    return f'''
    <div class="section-bar">Hobi Kosesi</div>
    <div class="article-title">{hobi.get("baslik","")}</div>
    {img_html}
    {hobiler}
    <div class="pull-quote">{hobi.get("ipucu","")}</div>'''


def _ilginc_section(data):
    facts = data.get("ilginc_bilgiler", [])
    items = ""
    for i, f in enumerate(facts, 1):
        items += f'<div class="quiz-q"><b>{i}.</b> {f}</div>'

    return f'''
    <div class="section-bar">Ilginc Bilgiler</div>
    <div class="article-title">Bunu Biliyor Muydunuz?</div>
    <div style="column-count:2;column-gap:16px;">{items}</div>'''


def _eglence_section(data):
    eglence = data.get("eglence_kosesi", {})

    fikralar = ""
    for f in eglence.get("fikralar", []):
        fikralar += f'<div class="quiz-q" style="background:#fffbeb;">{f}</div>'

    yarismalar = ""
    for y in eglence.get("bilgi_yarismasi", []):
        yarismalar += f'<div class="quiz-q"><b>S:</b> {y["soru"]}<br/><b>C:</b> {y["cevap"]}</div>'

    return f'''
    <div class="section-bar">Eglence Kosesi</div>
    <div class="small-title">Fikralar</div>
    {fikralar}
    <div class="gold-line"></div>
    <div class="small-title">Bilgi Yarismasi</div>
    {yarismalar}
    <div class="pull-quote">{eglence.get("labirent_aciklama","")}</div>'''


def _felsefe_section(data, img):
    felsefe = data.get("felsefe_kosesi", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""
    filozof = felsefe.get("filozof", {})

    sozler = ""
    for s in felsefe.get("sozler", []):
        sozler += f'<div class="pull-quote" style="font-size:9.5pt;">{s}</div>'

    return f'''
    <div class="section-bar">Felsefe Kosesi</div>
    <div class="article-title">{felsefe.get("baslik","")}</div>
    {img_html}
    <div class="info-box"><b>{filozof.get("ad","")} ({filozof.get("donem","")}, {filozof.get("ulke","")})</b><br/>{filozof.get("biyografi","")}</div>
    <div class="green-box"><b>Temel Fikir:</b> {filozof.get("temel_fikir","")}</div>
    <div class="gold-line"></div>
    <div class="pull-quote"><b>Dusunce Sorusu:</b> {felsefe.get("dusunce_sorusu","")}</div>
    {sozler}'''


def _muzik_section(data, img):
    muzik = data.get("muzik_kosesi", {})
    img_html = f'<img src="{img}" class="img-half"/>' if img else ""
    sanatci = muzik.get("sanatci", {})
    tur = muzik.get("tur_tanitimi", {})

    return f'''
    <div class="section-bar">Muzik Dunyasi</div>
    <div class="article-title">{muzik.get("baslik","")}</div>
    {img_html}
    <div class="info-box"><b>Sanatci: {sanatci.get("ad","")} ({sanatci.get("donem","")}, {sanatci.get("ulke","")})</b><br/>{sanatci.get("bilgi","")}</div>
    <div class="green-box"><b>Tur: {tur.get("ad","")}</b><br/>{tur.get("aciklama","")}</div>
    <div class="pull-quote"><b>Dinleme Onerisi:</b> {muzik.get("dinleme_onerisi","")}</div>'''


def _bulmaca_section(data):
    bulmaca = data.get("kelime_bulmacasi_50", {})
    bilmeceler = data.get("bilmeceler", [])
    mantik = data.get("mantik_sorulari", [])
    matematik = data.get("matematik_bulmacalari", [])
    zeka = data.get("zeka_sorulari", [])
    kim_bu = data.get("kim_bu", {})

    kelimeler = bulmaca.get("kelimeler", [])
    kel_html = ", ".join(kelimeler) if kelimeler else ""

    bilm_html = ""
    for soru, _ in bilmeceler:
        bilm_html += f'<div class="quiz-q">{soru}</div>'

    mantik_html = ""
    for soru, _ in mantik:
        mantik_html += f'<div class="quiz-q">{soru}</div>'

    mat_html = ""
    for m in matematik:
        mat_html += f'<div class="quiz-q">{m}</div>'

    zeka_html = ""
    for z in zeka[:4]:
        zeka_html += f'<div class="quiz-q"><b>S:</b> {z["soru"]}</div>'

    ipucu_html = ""
    for ip in kim_bu.get("ipuclari", []):
        ipucu_html += f'<li>{ip}</li>'

    return f'''
    <div class="section-bar">Bulmacalar & Bilmeceler</div>
    <div class="small-title">{bulmaca.get("baslik","Kelime Bulmacasi")}</div>
    <div class="info-box"><b>Aranacak Kelimeler:</b> {kel_html}<br/><i>{bulmaca.get("ipucu","")}</i></div>
    <div class="gold-line"></div>
    <div class="small-title">Bilmeceler</div>
    {bilm_html}
    <div class="gold-line"></div>
    <div class="small-title">Mantik Sorulari</div>
    {mantik_html}
    <div class="gold-line"></div>
    <div class="small-title">Matematik Bulmacalari</div>
    {mat_html}
    <div class="gold-line"></div>
    <div class="small-title">Zeka Sorulari</div>
    {zeka_html}
    <div class="gold-line"></div>
    <div class="green-box"><b>Kim Bu?</b><ul>{ipucu_html}</ul></div>'''


def _ozlu_sozler_section(data):
    sozler = data.get("ozlu_sozler", [])
    html = '<div class="section-bar">Ozlu Sozler</div>'
    html += '<div style="column-count:2;column-gap:14px;">'
    for s in sozler:
        if isinstance(s, dict):
            html += f'''<div class="quote-card">
                <div class="q-cat">{s.get("kategori","")}</div>
                "{s.get("soz","")}"
                <div class="q-author">&mdash; {s.get("kisi","")}</div>
            </div>'''
        else:
            html += f'<div class="quote-card">{s}</div>'
    html += '</div>'
    return html


def _quiz_section(data):
    quiz = data.get("quiz", [])
    rehber = data.get("quiz_puan_rehberi", "")

    html = '<div class="section-bar">Aylik Quiz</div>'
    html += f'<div class="info-box"><b>Puan Rehberi:</b> {rehber}</div>'

    for i, q in enumerate(quiz, 1):
        opts = " &nbsp;|&nbsp; ".join(q.get("secenekler", []))
        diff = "&#9733;" * q.get("zorluk", 1)
        html += f'''<div class="quiz-q">
            <b>{i}.</b> {q.get("soru","")} <span style="float:right;color:#c9a84c;font-size:8pt;">{diff}</span>
            <br/><span style="font-size:8.5pt;color:#64748b;">{opts}</span>
        </div>'''

    return html


def _ingilizce_section(data):
    """English learning section with vocab, phrases, grammar from template data."""
    html = '<div class="section-bar">Ingilizce Kosesi</div>'
    html += '<div class="article-title">English Corner</div>'

    vocab = [
        ("Knowledge", "Bilgi"), ("Discovery", "Kesif"), ("Science", "Bilim"),
        ("Education", "Egitim"), ("Universe", "Evren"), ("Research", "Arastirma"),
        ("Experiment", "Deney"), ("Curiosity", "Merak"), ("Innovation", "Yenilik"),
        ("Achievement", "Basari"),
    ]
    phrases = [
        ("Practice makes perfect.", "Pratik mukemmellestirrir."),
        ("The early bird catches the worm.", "Erken kalkan yol alir."),
        ("Actions speak louder than words.", "Isler sozlerden daha yuksek sesle konusur."),
        ("Where there's a will, there's a way.", "Isteyen yolu, istemeyen bahane bulur."),
    ]
    grammar = (
        "Present Perfect Tense: I have studied / She has learned. "
        "Gecmiste baslayip etkisi devam eden eylemler icin kullanilir. "
        "have/has + past participle (V3) seklinde olusturulur. "
        "Zaman zarflari: already, yet, just, ever, never, since, for."
    )

    vocab_rows = "".join(f'<tr><td style="font-weight:700;">{e}</td><td>{t}</td></tr>' for e, t in vocab)
    phrase_items = "".join(f'<li><b>{e}</b> &mdash; {t}</li>' for e, t in phrases)

    return f'''{html}
    <div class="small-title">Kelime Bankasi</div>
    <table class="tbl"><tr><th>English</th><th>Turkce</th></tr>{vocab_rows}</table>
    <div class="gold-line"></div>
    <div class="small-title">Gunluk Ifadeler</div>
    <div class="info-box"><ul>{phrase_items}</ul></div>
    <div class="green-box"><b>Gramer Notu:</b> {grammar}</div>'''


def _almanca_section(data):
    """German learning section with vocab, phrases, grammar."""
    html = '<div class="section-bar">Almanca Kosesi</div>'
    html += '<div class="article-title">Deutsche Ecke</div>'

    vocab = [
        ("die Wissenschaft", "Bilim"), ("die Bildung", "Egitim"), ("die Schule", "Okul"),
        ("der Lehrer", "Ogretmen"), ("das Buch", "Kitap"), ("die Forschung", "Arastirma"),
        ("das Wissen", "Bilgi"), ("die Natur", "Doga"), ("die Kunst", "Sanat"),
        ("die Musik", "Muzik"),
    ]
    phrases = [
        ("Ubung macht den Meister.", "Alistirma ustasi yapar."),
        ("Wissen ist Macht.", "Bilgi guctur."),
        ("Der Apfel fallt nicht weit vom Stamm.", "Armut dibine duser."),
    ]
    grammar = (
        "Artikel Sistemi: der (eril), die (disil), das (nötr). "
        "Almanca'da her ismin bir artikeli vardir ve ezberlenmelidir. "
        "Cogul yapilarda hep 'die' kullanilir. Akkusativ: den, die, das."
    )

    vocab_rows = "".join(f'<tr><td style="font-weight:700;">{d}</td><td>{t}</td></tr>' for d, t in vocab)
    phrase_items = "".join(f'<li><b>{d}</b> &mdash; {t}</li>' for d, t in phrases)

    return f'''{html}
    <div class="small-title">Wortschatz (Kelime Bankasi)</div>
    <table class="tbl"><tr><th>Deutsch</th><th>Turkce</th></tr>{vocab_rows}</table>
    <div class="gold-line"></div>
    <div class="small-title">Redewendungen (Deyimler)</div>
    <div class="info-box"><ul>{phrase_items}</ul></div>
    <div class="green-box"><b>Grammatik:</b> {grammar}</div>'''


def _saglik_section(data):
    beslenme = data.get("veli", {}).get("beslenme", [])
    tips = "".join(f'<li>{b}</li>' for b in beslenme) if beslenme else ""
    spor_tip = data.get("spor", {}).get("saglik_ipucu", "")

    return f'''
    <div class="section-bar">Saglik & Beslenme</div>
    <div class="article-title">Saglikli Yasam Rehberi</div>
    <div class="two-col body">
        <p>Saglikli beslenme ve duznelit fiziksel aktivite, ogrencilerin hem akademik hem de
        fiziksel performansini dogrudan etkiler. Dengeli bir diyet; protein, karbonhidrat, yag,
        vitamin ve mineralleri uygun oranlarda icermelidir. Ozellikle beyin sagligi icin omega-3
        yag asitleri, demir, B vitaminleri ve antioksidanlar buyuk onem tasir.</p>
        <p>Gunluk en az 8 bardak su icmek, 7-9 saat uyumak ve 30-60 dakika fiziksel aktivite
        yapmak saglikli bir yasamin temel taslarini olusturur. Fast food ve islenimis gidalarin
        tuketimini sinirlamak, taze meyve ve sebze agirlikli beslenme tercih etmek onemlidir.</p>
    </div>
    <div class="green-box"><b>Beslenme Ipuclari</b><ul>{tips}</ul></div>
    <div class="pull-quote"><b>Spor & Saglik:</b> {spor_tip}</div>'''


def _dunya_haberleri_section(data):
    haberler = data.get("teknoloji", {}).get("haberler", [])
    hab_html = "".join(f'<div class="quiz-q">{h}</div>' for h in haberler)
    tarihte = data.get("tarih", {}).get("tarihte_bu_ay", [])
    tarih_html = "".join(f'<li>{t}</li>' for t in tarihte)

    return f'''
    <div class="section-bar">Dunya Gundemi</div>
    <div class="article-title">Bu Ay Dunyada Neler Oldu?</div>
    <div class="small-title">Teknoloji ve Bilim Haberleri</div>
    {hab_html}
    <div class="gold-line"></div>
    <div class="info-box"><b>Tarihte Bu Ay</b><ul>{tarih_html}</ul></div>'''


def _meslekler_section(data):
    rehberlik = data.get("psikoloji", {}).get("rehberlik", "")

    return f'''
    <div class="section-bar">Gelecek Meslekler</div>
    <div class="article-title">Gelecegin Meslekleri</div>
    <div class="two-col body">
        <p>Teknolojinin hizla gelisimi, yeni mesleklerin ortaya cikmasina yol acmaktadir.
        Yapay zeka uzmanligi, veri bilimciligi, siber guvenlik uzmanligi, robotik muhendisligi,
        drone pilotlugu, biyoinformatik ve uzay turizmi yoneticiligi gelecekteki en aranan
        meslekler arasinda yer almaktadir.</p>
        <p>Yaratici endustrilerde de dijital icerik ureticiligi, UX/UI tasarimi, oyun
        gelistirme ve sanal gerceklik icerik uretimi populer kariyer seçenekleri olarak
        one cikmaktadir. STEM (Bilim, Teknoloji, Muhendislik, Matematik) alanlarindaki
        beceriler gelecek is gucu piyasasinda buyuk avantaj saglayacaktir.</p>
    </div>
    <div class="info-box"><b>Kariyer Rehberligi</b><br/>{rehberlik}</div>
    <div class="green-box"><b>Gelecekte En Cok Aranan 5 Beceri:</b>
        <ol>
            <li>Elestrel dusunme ve problem cozme</li>
            <li>Dijital okuryazarlik ve kodlama</li>
            <li>Yaraticilik ve inovasyon</li>
            <li>Iletisim ve isbirligi</li>
            <li>Duygusal zeka ve uyum yettenegi</li>
        </ol>
    </div>'''


def _sanat_galerisi_section(data):
    sanat = data.get("kultur_sanat", {}).get("sanat_eseri", {})
    muze = data.get("kultur_sanat", {}).get("muze", "")

    return f'''
    <div class="section-bar">Sanat Galerisi</div>
    <div class="article-title">Ayin Sanat Eseri</div>
    <div class="info-box">
        <b>{sanat.get("ad","")} &mdash; {sanat.get("sanatci","")} ({sanat.get("yil","")})</b><br/>
        {sanat.get("aciklama","")}
    </div>
    <div class="gold-line"></div>
    <div class="green-box"><b>Muze Onerisi</b><br/>{muze}</div>
    <div class="two-col body">
        <p>Sanat, insanligin en eski ifade bicimlrrinden biridir. Magara resimlerinden dijital
        sanata, heykelden performans sanatina kadar genis bir yelpazede insanlar duygularini,
        dusuncelerini ve dunya goruslerini sanat araciligiyla ifade etmistir.</p>
        <p>Genc nesillerin sanatla tanismasi, yaraticilik, empati ve elestrel dusunme
        becerilerini gelistirir. Muzeler, galeriler ve sanat atolyeleri bu tanismayi
        saglamak icin ideal ortamlar sunmaktadir.</p>
    </div>'''


def _cevaplar_section(data):
    quiz = data.get("quiz", [])
    bilmeceler = data.get("bilmeceler", [])
    mantik = data.get("mantik_sorulari", [])
    mat_cevap = data.get("matematik_cevaplar", [])
    kim_bu = data.get("kim_bu", {})
    sonraki = data.get("sonraki_sayi", {})

    quiz_cevap = ", ".join(f'{i+1}:{q.get("cevap","")}' for i, q in enumerate(quiz))
    bilm_cevap = "".join(f'<li>{c}</li>' for _, c in bilmeceler)
    mantik_cevap = "".join(f'<li>{c}</li>' for _, c in mantik)
    mat_html = ", ".join(mat_cevap) if mat_cevap else ""

    teasers = "".join(f'<li>{t}</li>' for t in sonraki.get("teasers", []))

    return f'''
    <div class="section-bar">Cevaplar & Gelecek Sayi</div>
    <div class="small-title">Quiz Cevaplari</div>
    <div class="info-box">{quiz_cevap}</div>
    <div class="gold-line"></div>
    <div class="small-title">Bilmece Cevaplari</div>
    <div class="info-box"><ul>{bilm_cevap}</ul></div>
    <div class="small-title">Mantik Sorulari Cevaplari</div>
    <div class="info-box"><ul>{mantik_cevap}</ul></div>
    <div class="small-title">Matematik Cevaplari</div>
    <div class="info-box">{mat_html}</div>
    <div class="small-title">Kim Bu? Cevabi</div>
    <div class="green-box"><b>{kim_bu.get("cevap","")}</b></div>
    <div class="gold-line"></div>
    <div class="section-bar">Gelecek Sayi</div>
    <div class="article-title">{sonraki.get("tema","")}</div>
    <div class="info-box"><b>On Izleme:</b><ul>{teasers}</ul></div>
    <div class="pull-quote">Smarti Dergi'nin bir sonraki sayisinda gorusmek uzere! Keyifli okumalar.</div>'''


# ---------------------------------------------------------------------------
# HTML BUILDER
# ---------------------------------------------------------------------------
def _build_html(data, imgs):
    ay = data.get("ay", "")
    sayi = data.get("sayi", 1)
    tema = data.get("tema", "")

    cover_img = _img_uri(imgs.get("kapak", ""))
    mascot_img = _img_uri(MASCOT_PATH)

    bilim_img = _img_uri(imgs.get("bilim", ""))
    tekno_img = _img_uri(imgs.get("teknoloji", ""))
    tarih_img = _img_uri(imgs.get("tarih", ""))
    gezi_img = _img_uri(imgs.get("gezi", ""))
    doga_img = _img_uri(imgs.get("doga", ""))
    edebiyat_img = _img_uri(imgs.get("edebiyat", ""))
    spor_img = _img_uri(imgs.get("spor", ""))
    kultur_img = _img_uri(imgs.get("kultur", ""))
    psi_img = _img_uri(imgs.get("psikoloji", ""))

    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>{CSS}</style></head><body>'''

    # PAGE 1: COVER
    html += _cover_page(data, cover_img, mascot_img)

    # PAGE 2-3: TOC + EDITORIAL
    html += _page_start(ay, sayi, tema, 2)
    html += _toc_editorial(data, mascot_img)
    html += _page_end(2)

    # PAGE 4-6: BILIM
    html += _page_start(ay, sayi, tema, 4)
    html += _bilim_section(data, bilim_img)
    html += _page_end(4)

    # PAGE 7-8: TEKNOLOJI
    html += _page_start(ay, sayi, tema, 7)
    html += _teknoloji_section(data, tekno_img)
    html += _page_end(7)

    # PAGE 9-10: TARIH
    html += _page_start(ay, sayi, tema, 9)
    html += _tarih_section(data, tarih_img)
    html += _page_end(9)

    # PAGE 11-12: GEZI
    html += _page_start(ay, sayi, tema, 11)
    html += _gezi_section(data, gezi_img)
    html += _page_end(11)

    # PAGE 13-14: DOGA
    html += _page_start(ay, sayi, tema, 13)
    html += _doga_section(data, doga_img)
    html += _page_end(13)

    # PAGE 15-16: EDEBIYAT
    html += _page_start(ay, sayi, tema, 15)
    html += _edebiyat_section(data, edebiyat_img)
    html += _page_end(15)

    # PAGE 17: SIIR
    html += _page_start(ay, sayi, tema, 17)
    html += _siir_section(data)
    html += _page_end(17)

    # PAGE 18-19: PSIKOLOJI
    html += _page_start(ay, sayi, tema, 18)
    html += _psikoloji_section(data, psi_img)
    html += _page_end(18)

    # PAGE 20-21: VELI
    html += _page_start(ay, sayi, tema, 20)
    html += _veli_section(data)
    html += _page_end(20)

    # PAGE 22-23: OGRENCI
    html += _page_start(ay, sayi, tema, 22)
    html += _ogrenci_section(data)
    html += _page_end(22)

    # PAGE 24-25: KULTUR
    html += _page_start(ay, sayi, tema, 24)
    html += _kultur_section(data, kultur_img)
    html += _page_end(24)

    # PAGE 26: SPOR
    html += _page_start(ay, sayi, tema, 26)
    html += _spor_section(data, spor_img)
    html += _page_end(26)

    # PAGE 27: OZLU SOZLER
    html += _page_start(ay, sayi, tema, 27)
    html += _ozlu_sozler_section(data)
    html += _page_end(27)

    # PAGE 28: BULMACALAR
    html += _page_start(ay, sayi, tema, 28)
    html += _bulmaca_section(data)
    html += _page_end(28)

    # PAGE 29: QUIZ
    html += _page_start(ay, sayi, tema, 29)
    html += _quiz_section(data)
    html += _page_end(29)

    # EXTRA SECTIONS (flow into additional pages)
    # HOBI
    html += _page_start(ay, sayi, tema, 30)
    html += _hobi_section(data, None)
    html += _page_end(30)

    # ILGINC BILGILER
    html += _page_start(ay, sayi, tema, 31)
    html += _ilginc_section(data)
    html += _page_end(31)

    # EGLENCE
    html += _page_start(ay, sayi, tema, 32)
    html += _eglence_section(data)
    html += _page_end(32)

    # FELSEFE
    html += _page_start(ay, sayi, tema, 33)
    html += _felsefe_section(data, None)
    html += _page_end(33)

    # MUZIK
    html += _page_start(ay, sayi, tema, 34)
    html += _muzik_section(data, None)
    html += _page_end(34)

    # INGILIZCE
    html += _page_start(ay, sayi, tema, 35)
    html += _ingilizce_section(data)
    html += _page_end(35)

    # ALMANCA
    html += _page_start(ay, sayi, tema, 36)
    html += _almanca_section(data)
    html += _page_end(36)

    # SAGLIK
    html += _page_start(ay, sayi, tema, 37)
    html += _saglik_section(data)
    html += _page_end(37)

    # DUNYA HABERLERI
    html += _page_start(ay, sayi, tema, 38)
    html += _dunya_haberleri_section(data)
    html += _page_end(38)

    # MESLEKLER
    html += _page_start(ay, sayi, tema, 39)
    html += _meslekler_section(data)
    html += _page_end(39)

    # SANAT GALERISI
    html += _page_start(ay, sayi, tema, 40)
    html += _sanat_galerisi_section(data)
    html += _page_end(40)

    # LAST PAGE: CEVAPLAR
    html += _page_start(ay, sayi, tema, 41)
    html += _cevaplar_section(data)
    html += _page_end(41)

    html += '</body></html>'
    return html


# ---------------------------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------------------------
def generate_premium_pdf(sayi_no, images=None):
    """Generate premium magazine PDF using WeasyPrint. Returns bytes."""
    data = DERGI_DATA.get(sayi_no)
    if not data:
        return None

    imgs = images or {}
    # Auto-detect cached images
    if not imgs:
        for k in ["kapak", "bilim", "teknoloji", "tarih", "gezi", "doga", "edebiyat", "spor", "kultur", "psikoloji"]:
            p = os.path.join(DERGI_IMG_DIR, f"sayi{sayi_no}_{k}.png")
            if os.path.exists(p):
                imgs[k] = p

    html_str = _build_html(data, imgs)

    # xhtml2pdf yetersiz kaldi — ReportLab Platypus kullan (daha guvenilir)
    from views._dk_dergi_pdf import generate_magazine_pdf as _rl_generate
    return _rl_generate(sayi_no, images=imgs)


def _render_inline_magazine(data, images):
    """Dergiyi Streamlit icinde direkt HTML olarak goster — tam kalite, aninda yuklenme."""
    import streamlit.components.v1 as components

    def _img_tag(key, width="100%"):
        path = images.get(key, "")
        if path and os.path.exists(path):
            uri = _img_uri(path)
            return f'<img src="{uri}" style="width:{width};border-radius:8px;margin:10px 0;box-shadow:0 4px 15px rgba(0,0,0,0.15);">'
        return ""

    ay = data.get("ay", "")
    sayi = data.get("sayi", 1)
    tema = data.get("tema", "")

    # CSS
    css = """<style>
    .mag-page{background:#ffffff !important;
        border:2px solid #d1d5db;border-radius:10px;padding:28px 32px;margin-bottom:22px;
        box-shadow:0 6px 25px rgba(0,0,0,0.12);max-width:820px;margin-left:auto;margin-right:auto;
        color:#111827 !important;}
    .mag-page *{color:#111827 !important;}
    .mag-section{background:linear-gradient(135deg,#0a0e27,#1a1a2e) !important;color:#c9a84c !important;
        padding:14px 22px;font-size:19px;font-weight:900;letter-spacing:3px;
        text-transform:uppercase;border-left:5px solid #c9a84c;margin:0 -32px 20px -32px;padding-left:32px;}
    .mag-section *{color:#c9a84c !important;}
    .mag-title{font-size:23px;font-weight:800;color:#0a0e27 !important;border-bottom:3px solid #c9a84c;
        padding-bottom:8px;margin-bottom:14px;line-height:1.3;}
    .mag-body{font-size:15px;line-height:1.85;color:#111827 !important;text-align:justify;}
    .mag-body p{margin-bottom:12px;color:#111827 !important;}
    .mag-quote{background:linear-gradient(135deg,#fef9c3,#fef08a) !important;border-left:5px solid #c9a84c;
        padding:14px 18px;margin:14px 0;font-style:italic;color:#78350f !important;font-size:15px;
        border-radius:0 8px 8px 0;}
    .mag-quote *{color:#78350f !important;}
    .mag-info{background:linear-gradient(135deg,#eff6ff,#dbeafe) !important;border:1px solid #93c5fd;
        border-radius:8px;padding:14px 18px;margin:14px 0;font-size:14px;color:#1e3a5f !important;}
    .mag-info *{color:#1e3a5f !important;}
    .mag-info b{color:#1e40af !important;}
    .mag-green{background:linear-gradient(135deg,#f0fdf4,#dcfce7) !important;border:1px solid #86efac;
        border-radius:8px;padding:14px 18px;margin:14px 0;font-size:14px;color:#14532d !important;}
    .mag-green *{color:#14532d !important;}
    .mag-tbl{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px;}
    .mag-tbl th{background:#0a0e27 !important;color:#c9a84c !important;padding:10px 14px;text-align:left;}
    .mag-tbl td{padding:8px 14px;border-bottom:1px solid #d1d5db;color:#111827 !important;}
    .mag-tbl tr:nth-child(even) td{background:#f1f5f9 !important;}
    .mag-gold{height:2px;background:linear-gradient(90deg,transparent,#c9a84c,transparent);margin:16px 0;}
    .mag-sub{font-size:17px;font-weight:800;color:#0a0e27 !important;margin:16px 0 8px 0;}
    </style>"""

    def _paragraphs(text):
        if not text:
            return ""
        return "".join(f"<p>{p.strip()}</p>" for p in text.split("\n\n") if p.strip())

    # Build sections
    sections_html = []

    # KAPAK
    kapak_img = _img_tag("kapak", "100%")
    sections_html.append(f"""<div class="mag-page" style="text-align:center;background:linear-gradient(160deg,#0a0e27,#1a1a2e,#16213e);color:white;padding:40px;">
        <div style="color:#c9a84c;font-size:12px;letter-spacing:6px;text-transform:uppercase;">SmartCampus</div>
        <div style="font-size:42px;font-weight:900;margin:8px 0;">Smarti</div>
        <div style="width:60px;height:2px;background:#c9a84c;margin:8px auto;"></div>
        <div style="color:#c9a84c;font-size:18px;">{ay}</div>
        <div style="color:#94a3b8;font-size:13px;">Sayi {sayi}</div>
        {kapak_img}
        <div style="font-size:24px;font-weight:700;margin-top:12px;">"{tema}"</div>
    </div>""")

    # EDITORDEN
    mascot = ""
    if os.path.exists(MASCOT_PATH):
        mascot = f'<img src="{_img_uri(MASCOT_PATH)}" style="width:80px;float:right;margin:0 0 10px 15px;border-radius:50%;">'
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">EDITORDEN</div>
        {mascot}
        <div class="mag-body">{_paragraphs(data.get('editorial',''))}</div>
        <div style="text-align:right;color:#94a3b8;font-style:italic;margin-top:10px;">SmartCampus Yayin Kurulu</div>
    </div>""")

    # BILIM & TEKNIK
    bilim = data.get("bilim_teknik", [])
    bilim_html = ""
    for art in bilim:
        bilim_html += f'<div class="mag-title">{art.get("baslik","")}</div>'
        bilim_html += f'<div class="mag-body">{_paragraphs(art.get("icerik",""))}</div>'
        bmy = art.get("biliyor_muydunuz", [])
        if bmy:
            bilim_html += '<div class="mag-info"><b>Bunu Biliyor muydunuz?</b><ul>'
            for b in bmy:
                bilim_html += f"<li>{b}</li>"
            bilim_html += "</ul></div>"
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">BILIM &amp; TEKNIK</div>
        {_img_tag("bilim")}
        {bilim_html}
    </div>""")

    # TEKNOLOJI
    tekno = data.get("teknoloji", {})
    tekno_haberler = ""
    for h in tekno.get("haberler", []):
        tekno_haberler += f"<li>{h}</li>"
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">TEKNOLOJI DUNYASI</div>
        {_img_tag("teknoloji")}
        <div class="mag-title">{tekno.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(tekno.get("icerik",""))}</div>
        <div class="mag-info"><b>Teknoloji Haberleri</b><ul>{tekno_haberler}</ul></div>
        <div class="mag-quote">{tekno.get("gelecekte_bu_var","")}</div>
    </div>""")

    # TARIH
    tarih = data.get("tarih", {})
    zaman = ""
    for y, e in tarih.get("zaman_cizelgesi", []):
        zaman += f"<tr><td><b>{y}</b></td><td>{e}</td></tr>"
    tba = ""
    for t in tarih.get("tarihte_bu_ay", []):
        tba += f"<li>{t}</li>"
    ts = tarih.get("tarih_sozu", {})
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">TARIH SAYFASI</div>
        {_img_tag("tarih")}
        <div class="mag-title">{tarih.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(tarih.get("icerik",""))}</div>
        <table class="mag-tbl"><tr><th>Tarih</th><th>Olay</th></tr>{zaman}</table>
        <div class="mag-green"><b>Tarihte Bu Ay</b><ul>{tba}</ul></div>
        {"<div class='mag-quote'>\"" + ts.get('soz','') + "\" — " + ts.get('kisi','') + "</div>" if ts else ""}
    </div>""")

    # GEZI
    gezi = data.get("cografya_gezi", {})
    gezi_bilgi = gezi.get("baskent_bilgi", {})
    gezi_gorulmesi = "".join(f"<li>{g}</li>" for g in gezi.get("gorulmesi_gereken", []))
    gezi_yemek = "".join(f"<li>{y}</li>" for y in gezi.get("yemek_onerileri", []))
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">COGRAFYA &amp; GEZI</div>
        {_img_tag("gezi")}
        <div class="mag-title">{gezi.get("yer","")} — {gezi.get("ulke","")}</div>
        <div class="mag-body">{_paragraphs(gezi.get("tanitim",""))}</div>
        <div class="mag-info"><b>Gorulmesi Gereken</b><ul>{gezi_gorulmesi}</ul></div>
        <div class="mag-green"><b>Yemek Onerileri</b><ul>{gezi_yemek}</ul></div>
    </div>""")

    # DOGA
    doga = data.get("doga_cevre", {})
    eko = "".join(f"<li>{e}</li>" for e in doga.get("eko_ipuclari", []))
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">DOGA &amp; CEVRE</div>
        {_img_tag("doga")}
        <div class="mag-title">{doga.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(doga.get("icerik",""))}</div>
        <div class="mag-green"><b>Eko Ipuclari</b><ul>{eko}</ul></div>
    </div>""")

    # EDEBIYAT
    edb = data.get("edebiyat", {})
    kitap_onerileri = ""
    for k in edb.get("bu_ay_okuyun", []):
        if isinstance(k, dict):
            kitap_onerileri += f"<tr><td>{k.get('kitap','')}</td><td>{k.get('yazar','')}</td><td>{k.get('tur','')}</td></tr>"
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">EDEBIYAT KOSESI</div>
        {_img_tag("edebiyat")}
        <div class="mag-title">{edb.get("kitap","")} — {edb.get("yazar","")}</div>
        <div class="mag-body">{_paragraphs(edb.get("tanitim",""))}</div>
        <div class="mag-info"><b>Yazar:</b> {edb.get("yazar_bio","")}</div>
        {"<table class='mag-tbl'><tr><th>Kitap</th><th>Yazar</th><th>Tur</th></tr>" + kitap_onerileri + "</table>" if kitap_onerileri else ""}
    </div>""")

    # SIIR
    siir_html = ""
    for s in data.get("siir", []):
        metin = s.get("metin", "").replace("\n", "<br>")
        siir_html += f"""<div style="background:linear-gradient(135deg,#fdf4ff,#fae8ff);border:1px solid #e879f9;
            border-radius:8px;padding:16px 20px;margin:10px 0;">
            <div style="font-size:16px;font-weight:700;color:#7e22ce;">{s.get("baslik","")}</div>
            <div style="font-size:12px;color:#a855f7;margin-bottom:8px;">{s.get("sair","")}</div>
            <div style="font-size:14px;line-height:1.8;color:#581c87;font-style:italic;">{metin}</div>
            <div style="font-size:11px;color:#9ca3af;margin-top:6px;">{s.get("bio","")}</div>
        </div>"""
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">SIIR KOSESI</div>
        {siir_html}
    </div>""")

    # PSIKOLOJI
    psi = data.get("psikoloji", {})
    stres = "".join(f"<li>{s}</li>" for s in psi.get("stres_ipuclari", []))
    qa = ""
    for q, a in psi.get("soru_cevap", []):
        qa += f"<div class='mag-info'><b>S: {q}</b><br>C: {a}</div>"
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">PSIKOLOJI &amp; REHBERLIK</div>
        {_img_tag("psikoloji")}
        <div class="mag-title">{psi.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(psi.get("icerik",""))}</div>
        <div class="mag-green"><b>Stres ile Basa Cikma</b><ul>{stres}</ul></div>
        <div class="mag-sub">Soru &amp; Cevap</div>{qa}
    </div>""")

    # VELI
    veli = data.get("veli", {})
    ev = "".join(f"<li>{e}</li>" for e in veli.get("ev_ortami", []))
    bes = "".join(f"<li>{b}</li>" for b in veli.get("beslenme", []))
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">VELI KOSESI</div>
        <div class="mag-title">{veli.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(veli.get("icerik",""))}</div>
        <div class="mag-info"><b>Evde Calisma Ortami</b><ul>{ev}</ul></div>
        <div class="mag-body">{_paragraphs(veli.get("iletisim",""))}</div>
        <div class="mag-green"><b>Beslenme Onerileri</b><ul>{bes}</ul></div>
    </div>""")

    # OGRENCI
    ogr = data.get("ogrenci_tavsiye", {})
    alis = "".join(f"<li>{a}</li>" for a in ogr.get("aliskanliklar", []))
    mot = "".join(f"<div class='mag-quote'>{m}</div>" for m in ogr.get("motivasyon_sozleri", []))
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">OGRENCILERE TAVSIYELER</div>
        <div class="mag-title">{ogr.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(ogr.get("icerik",""))}</div>
        <div class="mag-info"><b>Basarili Ogrencilerin Aliskanliklari</b><ol>{alis}</ol></div>
        <div class="mag-sub">Motivasyon Sozleri</div>{mot}
    </div>""")

    # KULTUR & SANAT
    kul = data.get("kultur_sanat", {})
    film = kul.get("film", {})
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">KULTUR &amp; SANAT</div>
        {_img_tag("kultur")}
        <div class="mag-title">{kul.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(kul.get("icerik",""))}</div>
        <div class="mag-info"><b>Film Onerisi:</b> {film.get("ad","")} ({film.get("yil","")}) — {film.get("aciklama","")}</div>
    </div>""")

    # SPOR
    spor = data.get("spor", {})
    sporcu = spor.get("ayin_sporcusu", {})
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">SPOR KOSESI</div>
        {_img_tag("spor")}
        <div class="mag-title">{spor.get("baslik","")}</div>
        <div class="mag-body">{_paragraphs(spor.get("icerik",""))}</div>
        <div class="mag-info"><b>Ayin Sporcusu:</b> {sporcu.get("ad","")} ({sporcu.get("dal","")}) — {sporcu.get("bilgi","")}</div>
    </div>""")

    # HOBI
    hobi = data.get("hobi_kosesi", {})
    hobi_html = ""
    for h in hobi.get("hobiler", []):
        hobi_html += f"<div class='mag-sub'>{h.get('emoji','')} {h.get('ad','')}</div><div class='mag-body'><p>{h.get('aciklama','')}</p></div>"
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">HOBI KOSESI</div>
        {_img_tag("hobi")}
        {hobi_html}
    </div>""")

    # ILGINC BILGILER
    ilginc = data.get("ilginc_bilgiler", [])
    il_html = "".join(f"<li style='margin:6px 0;'>{b}</li>" for b in ilginc)
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">ILGINC BILGILER</div>
        <div class="mag-title">Bunlari Biliyor muydunuz?</div>
        <ol style="font-size:14px;line-height:1.8;color:#1f2937;padding-left:20px;">{il_html}</ol>
    </div>""")

    # FELSEFE
    fel = data.get("felsefe_kosesi", {})
    fil = fel.get("filozof", {})
    fel_sozler = "".join(f"<div class='mag-quote'>{s}</div>" for s in fel.get("sozler", []))
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">FELSEFE KOSESI</div>
        {_img_tag("felsefe")}
        <div class="mag-title">{fil.get("ad","")} ({fil.get("donem","")})</div>
        <div class="mag-body"><p>{fil.get("biyografi","")}</p></div>
        <div class="mag-info"><b>Temel Fikir:</b> {fil.get("temel_fikir","")}</div>
        <div class="mag-quote"><b>Dusunce Sorusu:</b> {fel.get("dusunce_sorusu","")}</div>
        {fel_sozler}
    </div>""")

    # MUZIK
    muz = data.get("muzik_kosesi", {})
    ms = muz.get("sanatci", {})
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">MUZIK KOSESI</div>
        {_img_tag("muzik")}
        <div class="mag-title">{ms.get("ad","")} ({ms.get("donem","")})</div>
        <div class="mag-body"><p>{ms.get("bilgi","")}</p></div>
        <div class="mag-info"><b>Dinleme Onerisi:</b> {muz.get("dinleme_onerisi","")}</div>
    </div>""")

    # OZLU SOZLER
    sozler_html = ""
    for s in data.get("ozlu_sozler", []):
        sozler_html += f"""<div style="background:linear-gradient(135deg,#f8fafc,#f1f5f9) !important;
            border-left:4px solid #c9a84c;padding:12px 16px;border-radius:0 8px 8px 0;margin:8px 0;font-size:14px;">
            <span style="color:#1f2937 !important;font-style:italic;">"{s.get('soz','')}"</span>
            <span style="color:#6b7280 !important;font-size:12px;"> — {s.get('kisi','')}</span>
            <span style="color:#9ca3af !important;font-size:11px;float:right;">{s.get('kategori','')}</span></div>"""
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">OZLU SOZLER</div>
        {sozler_html}
    </div>""")

    # QUIZ
    quiz_html = ""
    for i, q in enumerate(data.get("quiz", [])):
        opts = "".join(f"<div style='padding:3px 0;'>{o}</div>" for o in q.get("secenekler", []))
        quiz_html += f"""<div class="mag-info" style="margin:8px 0;">
            <b>{i+1}.</b> {q.get("soru","")}<br>{opts}
            <div style="color:#16a34a;font-size:11px;margin-top:4px;">Cevap: {q.get("cevap","")}</div></div>"""
    sections_html.append(f"""<div class="mag-page">
        <div class="mag-section">AYLIK QUIZ</div>
        {quiz_html}
    </div>""")

    # Render all sections as single HTML component (no Streamlit CSS interference)
    import streamlit.components.v1 as components
    full_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">{css}</head>
    <body style="background:#1a1a2e;margin:0;padding:20px;">
    {''.join(sections_html)}
    </body></html>"""
    # Calculate height based on content
    section_count = len(sections_html)
    est_height = section_count * 900  # ~900px per section average
    components.html(full_html, height=est_height, scrolling=True)


def render_premium_dergi_viewer():
    """Streamlit UI for premium magazine PDF generation."""
    st.markdown("""
    <style>
    .dergi-header {
        background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 50%, #2563eb 100%);
        padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px;
    }
    .dergi-header h1 { color: #d4a017; font-size: 28px; margin: 0; }
    .dergi-header p { color: #94a3b8; font-size: 13px; margin: 5px 0 0 0; }
    .dergi-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid rgba(212,160,23,0.25); border-radius: 10px;
        padding: 18px; margin: 10px 0; color: #e2e8f0;
    }
    .dergi-card h3 { color: #d4a017; }
    .dergi-card p { color: #94a3b8; }
    .dergi-card strong { color: #d4a017; }
    .dergi-stat {
        background: linear-gradient(135deg, #1e3a5f, #2563eb);
        border-radius: 10px; padding: 15px; text-align: center; color: white;
    }
    .dergi-stat h2 { font-size: 28px; margin: 0; color: #d4a017; }
    .dergi-stat p { font-size: 11px; margin: 3px 0 0 0; color: #94a3b8; }
    .dergi-section-badge {
        display: inline-block; background: #1e3a5f; color: #d4a017;
        padding: 3px 10px; border-radius: 12px; font-size: 11px; margin: 2px;
    }
    .premium-badge {
        display: inline-block; background: linear-gradient(135deg, #c9a84c, #f59e0b);
        color: #0a0e27; padding: 4px 14px; border-radius: 20px;
        font-size: 11px; font-weight: 700; letter-spacing: 1px; margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dergi-header">
        <h1>Smarti Dergi <span class="premium-badge">PREMIUM</span></h1>
        <p>WeasyPrint ile Profesyonel Magazine PDF | HTML/CSS Tabanli | Yuksek Kalite</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="dergi-stat"><h2>12</h2><p>Sayi</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dergi-stat"><h2>40+</h2><p>Sayfa/Sayi</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="dergi-stat"><h2>28+</h2><p>Bolum</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="dergi-stat"><h2>HD</h2><p>Kalite</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Rol kontrol — Yonetici tum sayilari gorur, diger roller sadece aktif ayi
    from datetime import datetime
    _auth = st.session_state.get("auth_user", {})
    _user_role = _auth.get("role", "")
    _is_admin = _user_role == "Yonetici"

    # Ay -> sayi numarasi eslestirmesi (Eylul=1, Ekim=2, ..., Agustos=12)
    _AY_SAYI_MAP = {9:1, 10:2, 11:3, 12:4, 1:5, 2:6, 3:7, 4:8, 5:9, 6:10, 7:11, 8:12}
    _current_month = datetime.now().month
    _current_sayi = _AY_SAYI_MAP.get(_current_month, 7)  # varsayilan Mart

    if _is_admin:
        # Yonetici: tum sayilari gorebilir
        sayi_options = {
            v["sayi"]: f'Sayi {v["sayi"]} - {v["ay"]} ({v["tema"]})'
            for v in DERGI_DATA.values()
        }
        selected_sayi = st.selectbox(
            "Sayi Secin (Yonetici):",
            options=list(sayi_options.keys()),
            format_func=lambda x: sayi_options[x],
            key="premium_sayi_sec",
            index=_current_sayi - 1,
        )
    else:
        # Ogretmen/Ogrenci/Veli: sadece aktif ay + onceki sayilar
        sayi_options = {}
        for v in DERGI_DATA.values():
            if v["sayi"] <= _current_sayi:
                sayi_options[v["sayi"]] = f'Sayi {v["sayi"]} - {v["ay"]} ({v["tema"]})'
        if not sayi_options:
            sayi_options = {_current_sayi: DERGI_DATA.get(_current_sayi, {}).get("ay", "Bu Ay")}

        # Aktif ayi varsayilan olarak sec
        sayi_keys = sorted(sayi_options.keys())
        default_idx = sayi_keys.index(_current_sayi) if _current_sayi in sayi_keys else len(sayi_keys) - 1

        selected_sayi = st.selectbox(
            "Dergi Sayisi:",
            options=sayi_keys,
            format_func=lambda x: sayi_options.get(x, f"Sayi {x}"),
            key="premium_sayi_sec",
            index=default_idx,
        )

        # Bu ayin dergisi bilgilendirmesi
        current_data = DERGI_DATA.get(_current_sayi, {})
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#059669,#10b981);color:white;'
            f'padding:10px 16px;border-radius:8px;margin-bottom:10px;font-size:13px;">'
            f'📅 Bu Ayin Dergisi: <b>{current_data.get("ay", "")}</b> — {current_data.get("tema", "")}'
            f'</div>',
            unsafe_allow_html=True,
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

        # Section badges
        sections = [
            "Editorden", "Bilim & Teknik", "Teknoloji", "Tarih",
            "Cografya & Gezi", "Doga & Cevre", "Edebiyat", "Siir",
            "Psikoloji", "Veli Kosesi", "Ogrenci Tavsiyeleri",
            "Kultur & Sanat", "Spor", "Ozlu Sozler", "Hobi Kosesi",
            "Ilginc Bilgiler", "Eglence", "Felsefe", "Muzik",
            "Ingilizce", "Almanca", "Saglik", "Dunya Gundemi",
            "Meslekler", "Sanat Galerisi", "Bulmacalar", "Quiz", "Cevaplar",
        ]
        badges = " ".join(f'<span class="dergi-section-badge">{s}</span>' for s in sections)
        st.markdown(f"<div style='margin:10px 0;'>{badges}</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Image management + PDF generation
        _img_cache_key = f"_premium_imgs_{selected_sayi}"
        dergi_images = st.session_state.get(_img_cache_key, {})

        col_img, col_pdf, col_dl = st.columns([1, 1, 1])

        with col_img:
            existing_count = sum(
                1 for k in ["kapak", "bilim", "teknoloji", "tarih", "gezi", "doga", "edebiyat", "spor", "kultur", "psikoloji"]
                if os.path.exists(os.path.join(DERGI_IMG_DIR, f"sayi{selected_sayi}_{k}.png"))
            )
            if existing_count > 0:
                st.success(f"{existing_count}/10 gorsel hazir")
            if st.button("AI Gorsel Uret (DALL-E 3)", use_container_width=True, key="premium_img_btn"):
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

        # Load cached images
        if not dergi_images:
            for k in ["kapak", "bilim", "teknoloji", "tarih", "gezi", "doga", "edebiyat", "spor", "kultur", "psikoloji"]:
                p = os.path.join(DERGI_IMG_DIR, f"sayi{selected_sayi}_{k}.png")
                if os.path.exists(p):
                    dergi_images[k] = p

        with col_pdf:
            if st.button("Premium PDF Olustur", type="primary", use_container_width=True, key="premium_pdf_btn"):
                img_note = f" ({len(dergi_images)} gorsel ile)" if dergi_images else " (gorselsiz)"
                with st.spinner(f"Premium PDF olusturuluyor{img_note}..."):
                    try:
                        pdf_bytes = generate_premium_pdf(selected_sayi, images=dergi_images)
                        if pdf_bytes:
                            st.session_state["_premium_pdf_bytes"] = pdf_bytes
                            st.session_state["_premium_pdf_sayi"] = selected_sayi
                            st.success(f"Sayi {selected_sayi} - Premium PDF olusturuldu! ({len(pdf_bytes)//1024} KB)")
                        else:
                            st.error("PDF olusturulamadi - veri bulunamadi.")
                    except ImportError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"PDF olusturma hatasi: {str(e)}")

        # Download + Flipbook Read
        if st.session_state.get("_premium_pdf_bytes") and st.session_state.get("_premium_pdf_sayi") == selected_sayi:
            with col_dl:
                st.download_button(
                    label="PDF Indir",
                    data=st.session_state["_premium_pdf_bytes"],
                    file_name=f"SmartCampus_Premium_Sayi{selected_sayi}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="premium_dl_btn",
                )

            col_flip1, col_flip2, col_flip3 = st.columns(3)
            with col_flip1:
                if st.button("📖 Burada Oku (HD)", type="primary", use_container_width=True, key="premium_inline_read"):
                    st.session_state["_premium_inline_read"] = selected_sayi
                    st.session_state.pop("_premium_flipbook_html", None)
                    st.rerun()
            with col_flip2:
                if st.button("📖 Flipbook Oku", use_container_width=True, key="premium_flip_light"):
                    with st.spinner("Flipbook hazırlanıyor..."):
                        from views._dk_dergi_pdf import generate_magazine_pdf as _rl_gen
                        _small_imgs = {}
                        try:
                            from PIL import Image as PILImage
                            from io import BytesIO as _BIO
                            for k, path in dergi_images.items():
                                if path and os.path.exists(path):
                                    img = PILImage.open(path)
                                    img.thumbnail((400, 400), PILImage.LANCZOS)
                                    buf = _BIO()
                                    img.save(buf, format="JPEG", quality=50)
                                    small_path = path.replace(".png", "_small.jpg")
                                    with open(small_path, "wb") as sf:
                                        sf.write(buf.getvalue())
                                    _small_imgs[k] = small_path
                        except ImportError:
                            _small_imgs = dergi_images
                        flip_pdf = _rl_gen(selected_sayi, images=_small_imgs)
                        pdf_mb = len(flip_pdf) / (1024 * 1024)
                        if pdf_mb > 20:
                            st.warning(f"PDF boyutu {pdf_mb:.0f} MB — flipbook yerine tarayıcı viewer önerilir. 'PDF Aç (Full HD)' butonunu kullanın.")
                        import base64
                        b64 = base64.b64encode(flip_pdf).decode()
                        from views.e_kitaplik import _pdf_reader_html
                        st.session_state["_premium_flipbook_html"] = _pdf_reader_html(b64, f"Smarti Dergi Sayi {selected_sayi}")
                        st.session_state.pop("_premium_inline_read", None)
                        st.rerun()
            with col_flip3:
                if st.button("📖 PDF Aç (Full HD)", use_container_width=True, key="premium_flip_full"):
                    import tempfile
                    temp_path = os.path.join(tempfile.gettempdir(), f"SmartCampus_Dergi_Sayi{selected_sayi}.pdf")
                    with open(temp_path, "wb") as tf:
                        tf.write(st.session_state["_premium_pdf_bytes"])
                    os.startfile(temp_path)
                    st.success("Full HD PDF tarayıcınızda açıldı!")

        # Show inline reader if active
        if st.session_state.get("_premium_inline_read") == selected_sayi:
            if st.button("✖ Okuyucuyu Kapat", key="premium_inline_close", type="secondary"):
                st.session_state.pop("_premium_inline_read", None)
                st.rerun()
            _render_inline_magazine(data, dergi_images)

        # Show flipbook if active
        if st.session_state.get("_premium_flipbook_html"):
            st.components.v1.html(st.session_state["_premium_flipbook_html"], height=800, scrolling=False)
            if st.button("✖ Flipbook Kapat", key="premium_flipbook_close"):
                st.session_state.pop("_premium_flipbook_html", None)
                st.rerun()

        # Bulk generation
        st.markdown("---")
        with st.expander("Toplu Premium PDF Olusturma"):
            st.info("Tum sayilari Premium formatta tek seferde olusturabilirsiniz.")
            if st.button("Tum Sayilari Olustur (12 Sayi)", key="premium_bulk_btn"):
                progress = st.progress(0)
                total = len(DERGI_DATA)
                for i, s_no in enumerate(DERGI_DATA.keys()):
                    try:
                        pdf_bytes = generate_premium_pdf(s_no)
                        if pdf_bytes:
                            st.download_button(
                                label=f"Sayi {s_no} - {DERGI_DATA[s_no]['ay']} ({len(pdf_bytes)//1024} KB)",
                                data=pdf_bytes,
                                file_name=f"SmartCampus_Premium_Sayi{s_no}.pdf",
                                mime="application/pdf",
                                key=f"premium_bulk_{s_no}",
                            )
                    except Exception as e:
                        st.warning(f"Sayi {s_no} olusturulamadi: {e}")
                    progress.progress((i + 1) / total)
                st.success("Toplu olusturma tamamlandi!")
