"""
MEB Dijital Formlar — Generik Form Renderer
=============================================
35 MEB rehberlik formunu tek bir şema-tabanlı renderer ile dijitalleştirir.
Her form: Liste görünümü + Yeni form doldurma (2 sekmeli).
"""

from __future__ import annotations
import streamlit as st
from datetime import date, datetime
from typing import Any

from models.meb_formlar import MEB_FORM_SCHEMAS, get_schemas_by_kategori

import os


# ────────────────────────────────────────────────────────────
# AI ÖĞRENCİ DEĞERLENDİRME (Tüm modüllerden çağrılabilir)
# ────────────────────────────────────────────────────────────

def ai_ogrenci_degerlendirme(ogrenci_id: str, ogrenci_adi: str = "") -> str | None:
    """Bir öğrencinin TÜM MEB form verilerini AI ile analiz eder.
    Diğer modüllerden de çağrılabilir:
        from views.meb_formlar import ai_ogrenci_degerlendirme
        sonuc = ai_ogrenci_degerlendirme(ogrenci_id, "Ali Veli")
    Returns: AI değerlendirme metni veya None (hata/veri yok durumunda).
    """
    try:
        from openai import OpenAI
    except ImportError:
        return None

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None

    # ── 1. Tüm MEB formlarını yükle ──
    try:
        from models.erken_uyari import CrossModuleLoader
        all_forms = CrossModuleLoader.load_all_meb_forms()
    except Exception:
        return None

    # Öğrenci bazlı filtrele
    ogr_forms: dict[str, list[dict]] = {}
    for store_key, form_list in all_forms.items():
        for f in form_list:
            fid = f.get("ogrenci_id", "")
            fname = f.get("ogrenci_adi_soyadi", "")
            if (fid and fid == ogrenci_id) or (ogrenci_adi and fname and ogrenci_adi.upper() in fname.upper()):
                ogr_forms.setdefault(store_key, []).append(f)

    # Aile Bilgi Formu da ekle
    try:
        abf_list = CrossModuleLoader.load_aile_bilgi_formlari()
        ogr_abf = [f for f in abf_list if f.get("ogrenci_id") == ogrenci_id]
        if ogr_abf:
            ogr_forms["aile_bilgi_formlari"] = ogr_abf
    except Exception:
        pass

    if not ogr_forms:
        return None

    # ── 2. Veri metnini oluştur ──
    veri_metni = f"OGRENCI: {ogrenci_adi or ogrenci_id}\n\n"

    for store_key, forms in ogr_forms.items():
        schema = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == store_key), None)
        if schema:
            form_title = schema["title"]
        elif store_key == "aile_bilgi_formlari":
            form_title = "Aile Bilgi Formu (B.K.G.1.c)"
        else:
            form_title = store_key

        veri_metni += f"── {form_title} ({len(forms)} kayit) ──\n"
        for f in forms[-3:]:  # Son 3 kayıt
            for key, val in f.items():
                if key in ("id", "olusturma_zamani", "guncelleme_zamani", "ogrenci_id"):
                    continue
                if val and str(val).strip() and val not in ("", "Gözlenmedi", 0, "0", False):
                    # Alan adını okunabilir hale getir
                    label = key.replace("_", " ").title()
                    veri_metni += f"  {label}: {val}\n"
            veri_metni += "\n"

    # Max 6000 karakter (token limiti için)
    if len(veri_metni) > 6000:
        veri_metni = veri_metni[:6000] + "\n[...veri kisaltildi]"

    # ── 3. AI çağrısı ──
    system_prompt = """Sen Turkiye'nin en deneyimli okul rehber ogretmeni ve ogrenci degerlendirme uzmanisin.
Sana bir ogrencinin MEB rehberlik formlarindan elde edilen GERCEK veriler verilecek.

KRITIK KURALLAR:
1. SADECE verilen form verilerine dayanarak analiz yap. Uydurma YAPMA.
2. Her tespitinin kaynagini belirt: hangi formdan, hangi alandan geldi.
3. Formda "Bos/Belirtilmemis" olan alanlar hakkinda yorum yapma.
4. Formlardaki uzman degerlendirmelerini (rehber_degerlendirme, genel_degerlendirme) aynen referans al.

YANITINI su formatta ver (Turkce):

## OGRENCI PROFILI
(Formlardaki verilere dayanarak — aile, yasam, durum ozeti)

## GUCLU YONLER
- Formlardan tespit edilen olumlu noktalar (varsa)

## RISK FAKTORLERI VE HASSAS NOKTALAR
- Her risk icin kaynak form ve alan belirt
- Ciddiyet derecesi: DUSUK / ORTA / YUKSEK / KRITIK

## BIREYSEL MUDAHALE PLANI
- Her risk icin somut aksiyon (kim, ne, ne zaman)
- Mevcut yapilmis mudahalelerin degerlendirilmesi

## YONLENDIRME ONERILERI
- Formlardaki mevcut yonlendirmelere dayanarak
- RAM, saglik, psikolog gerekliligi

## TAKIP PLANI
- Hangi formlar ne siklikla yeniden doldurulmali

## 💡 KOCLUK TAVSIYELERI
- Ogretmenlere oneriler (sinif ici yaklasim)
- Veliye oneriler
- Ogrenciye yonelik motivasyon/destek stratejileri

ONEMLI:
- Formda veri olmayan alanlari belirtme, sadece mevcut verileri analiz et
- Somut, uygulanabilir, olculebilir tavsiyeler ver
- Her bolumde emoji kullan
- Gizlilik ilkesine uygun yaz (KVKK uyarisi ekle)
"""

    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": veri_metni},
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        return resp.choices[0].message.content
    except Exception:
        return None


def render_ai_ogrenci_panel(store, ogrenci_id: str, ogrenci_adi: str = ""):
    """Streamlit UI — Öğrenci bazlı AI MEB form değerlendirme paneli.
    Herhangi bir view'dan çağrılabilir."""
    _inject_meb_css()

    # Öğrenci form sayısını kontrol et
    try:
        from models.erken_uyari import CrossModuleLoader
        all_forms = CrossModuleLoader.load_all_meb_forms()
        ogr_count = 0
        for flist in all_forms.values():
            ogr_count += sum(1 for f in flist if f.get("ogrenci_id") == ogrenci_id)
        # Aile bilgi formu da dahil
        abf = CrossModuleLoader.load_aile_bilgi_formlari()
        ogr_count += sum(1 for f in abf if f.get("ogrenci_id") == ogrenci_id)
    except Exception:
        ogr_count = 0

    if ogr_count == 0:
        st.info("Bu öğrenci için MEB form kaydı bulunamadı.")
        return

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;'
        f'padding:12px 16px;border-radius:10px;margin:8px 0;">'
        f'<b>🤖 AI Öğrenci Değerlendirmesi</b> — {ogrenci_adi or ogrenci_id}'
        f'<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        f'{ogr_count} MEB form kaydı analiz edilecek (GPT-4o-mini)</p></div>',
        unsafe_allow_html=True,
    )

    cache_key = f"meb_ai_eval_{ogrenci_id}"
    if cache_key in st.session_state:
        st.markdown(st.session_state[cache_key])
        if st.button("🔄 Yeniden Değerlendir", key=f"meb_ai_refresh_{ogrenci_id}"):
            del st.session_state[cache_key]
            st.rerun()
        return

    if st.button("🤖 AI ile Değerlendir", key=f"meb_ai_btn_{ogrenci_id}",
                  type="primary", use_container_width=True):
        with st.spinner("AI analiz yapılıyor..."):
            result = ai_ogrenci_degerlendirme(ogrenci_id, ogrenci_adi)
        if result:
            st.session_state[cache_key] = result
            st.markdown(result)
        else:
            st.error("AI değerlendirme oluşturulamadı. OpenAI API anahtarını kontrol edin veya form verisi yetersiz.")


# ────────────────────────────────────────────────────────────
# CSS + STYLE HELPERS
# ────────────────────────────────────────────────────────────

def _inject_meb_css():
    """MEB Formlar için premium CSS — bir kez inject edilir."""
    if st.session_state.get("_meb_css_injected"):
        return
    st.markdown("""<style>
    .meb-header{background:linear-gradient(135deg,#1e293b,#334155);color:#fff;
        padding:18px 22px;border-radius:14px;margin-bottom:16px;
        border-left:4px solid #f59e0b;}
    .meb-header h3{margin:0;font-size:18px;font-weight:700;}
    .meb-header p{margin:3px 0 0;font-size:12px;opacity:.8;}
    .meb-section{background:linear-gradient(135deg,#f8fafc,#f1f5f9);
        border:1px solid #e2e8f0;border-radius:10px;padding:14px 16px;margin:10px 0;
        border-left:3px solid #3b82f6;}
    .meb-section h4{margin:0 0 8px;font-size:14px;color:#1e293b;}
    .meb-card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;
        padding:12px 16px;margin:6px 0;box-shadow:0 1px 3px rgba(0,0,0,.04);}
    .meb-stat{display:inline-block;background:linear-gradient(135deg,#eff6ff,#dbeafe);
        border:1px solid #bfdbfe;border-radius:8px;padding:8px 14px;margin:3px;
        font-size:13px;color:#1e40af;}
    .meb-kat-badge{display:inline-block;padding:4px 12px;border-radius:20px;
        font-size:12px;font-weight:600;color:#fff;margin:2px;}
    .meb-form-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;}
    .meb-form-item{background:#fff;border:1px solid #e2e8f0;border-radius:10px;
        padding:14px;cursor:pointer;transition:all .2s;border-left:3px solid var(--clr,#3b82f6);}
    .meb-form-item:hover{box-shadow:0 4px 12px rgba(0,0,0,.08);transform:translateY(-1px);}
    .meb-form-item .title{font-weight:600;font-size:13px;color:#1e293b;}
    .meb-form-item .sub{font-size:11px;color:#64748b;margin-top:2px;}
    .meb-rating-row{display:flex;gap:6px;align-items:center;margin:2px 0;}
    .meb-rating-dot{width:24px;height:24px;border-radius:50%;border:2px solid #cbd5e1;
        display:flex;align-items:center;justify-content:center;font-size:11px;
        cursor:pointer;transition:all .15s;}
    .meb-rating-dot.active{background:#3b82f6;border-color:#2563eb;color:#fff;}
    </style>""", unsafe_allow_html=True)
    st.session_state["_meb_css_injected"] = True


def _styled_form_header(title: str, subtitle: str, icon: str = "📋", color: str = "#1e293b"):
    """Form başlık bileşeni."""
    st.markdown(
        f'<div class="meb-header" style="border-left-color:{color};">'
        f'<h3>{icon} {title}</h3>'
        f'<p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────────────────────────
# GENERİK FORM RENDERER
# ────────────────────────────────────────────────────────────

def _render_field(field: dict, prefix: str, idx: int = 0) -> Any:
    """Tek bir form alanını Streamlit widget'ına çevirir."""
    key = f"{prefix}_{field['key']}_{idx}"
    label = field["label"]
    ftype = field.get("type", "text")
    options = field.get("options", [])
    default = field.get("default", "")
    help_text = field.get("help", None)

    if ftype == "text":
        return st.text_input(label, value=str(default) if default else "", key=key, help=help_text)
    elif ftype == "textarea":
        return st.text_area(label, value=str(default) if default else "", key=key, height=80, help=help_text)
    elif ftype == "select":
        opts = [""] + options if options else [""]
        return st.selectbox(label, opts, key=key, help=help_text)
    elif ftype == "multiselect":
        return st.multiselect(label, options or [], key=key, help=help_text)
    elif ftype == "number":
        def_val = int(default) if default else 0
        return st.number_input(label, min_value=0, value=def_val, key=key, help=help_text)
    elif ftype == "date":
        return st.date_input(label, value=date.today(), key=key, help=help_text)
    elif ftype == "checkbox":
        return st.checkbox(label, value=bool(default), key=key, help=help_text)
    elif ftype == "rating":
        # 0-3 rating: Gözlenmedi / Nadiren / Bazen / Sıklıkla
        rating_labels = ["Gözlenmedi", "Nadiren", "Bazen", "Sıklıkla"]
        return st.select_slider(label, options=rating_labels, value="Gözlenmedi", key=key, help=help_text)
    else:
        return st.text_input(label, key=key, help=help_text)


def _collect_form_data(schema: dict, prefix: str) -> dict:
    """Tüm widget'lardan veri toplar (session_state'den)."""
    data = {}
    for sec_idx, section in enumerate(schema["sections"]):
        for field in section["fields"]:
            key = f"{prefix}_{field['key']}_{sec_idx}"
            val = st.session_state.get(key, "")
            # date nesnelerini string'e çevir
            if isinstance(val, (date, datetime)):
                val = val.isoformat()
            data[field["key"]] = val
    return data


def _display_form_summary(form_data: dict, schema: dict):
    """Kaydedilmiş formu özet olarak göster."""
    for section in schema["sections"]:
        vals = [form_data.get(f["key"], "") for f in section["fields"]]
        if not any(str(v).strip() for v in vals):
            continue
        icon = section.get("icon", "📋")
        st.markdown(f"**{icon} {section['title']}:**")
        for field in section["fields"]:
            val = form_data.get(field["key"], "")
            if val and str(val).strip():
                st.markdown(f"- **{field['label']}:** {val}")


def render_generic_form(store, schema_key: str):
    """Tek bir MEB formunu render eder (liste + yeni form)."""
    _inject_meb_css()

    schema = MEB_FORM_SCHEMAS.get(schema_key)
    if not schema:
        st.error(f"Form şeması bulunamadı: {schema_key}")
        return

    store_key = schema["store_key"]
    prefix = f"mf_{schema_key}"

    _styled_form_header(schema["title"], schema["subtitle"], schema["icon"], schema["color"])

    sub1, sub2 = st.tabs(["📋 Form Listesi", "➕ Yeni Form Doldur"])

    # ── Tab 1: Form Listesi ──
    with sub1:
        formlar = store.load_list(store_key)
        if not formlar:
            st.info(f"Henüz {schema['title']} doldurulmamış.")
        else:
            st.markdown(f"**Toplam {len(formlar)} kayıt**")
            for f in sorted(formlar, key=lambda x: x.get("olusturma_zamani", ""), reverse=True):
                # Başlık: ilk required alanın değeri veya tarih
                display_name = ""
                for sec in schema["sections"]:
                    for fld in sec["fields"]:
                        if fld.get("required") and f.get(fld["key"]):
                            display_name = f.get(fld["key"], "")
                            break
                    if display_name:
                        break
                if not display_name:
                    display_name = f.get("ogrenci_adi_soyadi", f.get("sinif_sube", f.get("id", "?")))
                tarih = f.get("tarih", f.get("olusturma_zamani", "")[:10] if f.get("olusturma_zamani") else "")

                with st.expander(f"{schema['icon']} {display_name} — {tarih}"):
                    _display_form_summary(f, schema)
                    # Silme butonu
                    if st.button("🗑️ Sil", key=f"del_{store_key}_{f.get('id', '')}"):
                        store.delete_by_id(store_key, f.get("id", ""))
                        st.success("Form silindi.")
                        st.rerun()

    # ── Tab 2: Yeni Form Doldur ──
    with sub2:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,{schema["color"]}cc,{schema["color"]}99);'
            f'color:#fff;padding:12px 16px;border-radius:10px;margin-bottom:12px;">'
            f'<b>{schema["icon"]} {schema["title"]}</b>'
            f'<p style="margin:2px 0 0;font-size:11px;opacity:.85;">{schema["subtitle"]}</p></div>',
            unsafe_allow_html=True,
        )

        # Öğrenci seçimi (form ogrenci_adi_soyadi alanı varsa)
        has_student = any(
            f["key"] == "ogrenci_adi_soyadi"
            for s in schema["sections"]
            for f in s["fields"]
        )
        stu_data = {}
        if has_student:
            try:
                from utils.shared_data import get_student_display_options
                students = get_student_display_options(include_empty=False)
            except Exception:
                students = {}
            sel_stu = st.selectbox("Öğrenci Seçin (opsiyonel):", [""] + list(students.keys()),
                                   key=f"{prefix}_stu_sel")
            stu_data = students.get(sel_stu, {}) if sel_stu else {}
            if sel_stu:
                st.caption(f"Seçilen: {sel_stu}")

        # Form bölümlerini render et
        for sec_idx, section in enumerate(schema["sections"]):
            icon = section.get("icon", "📋")
            st.markdown(f"### {icon} {section['title']}")
            cols_count = section.get("columns", 1)

            if cols_count > 1:
                cols = st.columns(cols_count)
                for fi, field in enumerate(section["fields"]):
                    with cols[fi % cols_count]:
                        # Otomatik doldurma
                        if field["key"] == "ogrenci_adi_soyadi" and stu_data:
                            st.text_input(
                                field["label"],
                                value=f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip(),
                                key=f"{prefix}_{field['key']}_{sec_idx}",
                            )
                        elif field["key"] == "sinif_sube" and stu_data:
                            st.text_input(
                                field["label"],
                                value=f"{stu_data.get('sinif', '')}/{stu_data.get('sube', '')}",
                                key=f"{prefix}_{field['key']}_{sec_idx}",
                            )
                        elif field["key"] == "okul_no" and stu_data:
                            st.text_input(
                                field["label"],
                                value=str(stu_data.get("numara", "")),
                                key=f"{prefix}_{field['key']}_{sec_idx}",
                            )
                        else:
                            _render_field(field, prefix, sec_idx)
            else:
                for fi, field in enumerate(section["fields"]):
                    if field["key"] == "ogrenci_adi_soyadi" and stu_data:
                        st.text_input(
                            field["label"],
                            value=f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip(),
                            key=f"{prefix}_{field['key']}_{sec_idx}",
                        )
                    elif field["key"] == "sinif_sube" and stu_data:
                        st.text_input(
                            field["label"],
                            value=f"{stu_data.get('sinif', '')}/{stu_data.get('sube', '')}",
                            key=f"{prefix}_{field['key']}_{sec_idx}",
                        )
                    elif field["key"] == "okul_no" and stu_data:
                        st.text_input(
                            field["label"],
                            value=str(stu_data.get("numara", "")),
                            key=f"{prefix}_{field['key']}_{sec_idx}",
                        )
                    else:
                        _render_field(field, prefix, sec_idx)

        st.markdown("---")
        if st.button("💾 Formu Kaydet", key=f"{prefix}_save", type="primary", use_container_width=True):
            # Zorunlu alan kontrolü
            form_data = _collect_form_data(schema, prefix)
            missing = []
            for sec_idx, sec in enumerate(schema["sections"]):
                for fld in sec["fields"]:
                    if fld.get("required"):
                        val = form_data.get(fld["key"], "")
                        if not val or not str(val).strip():
                            missing.append(fld["label"])
            if missing:
                st.error(f"Zorunlu alanlar: {', '.join(missing)}")
                return

            # ID ve zaman damgaları ekle
            from models.rehberlik import _gen_id, _now
            form_data["id"] = _gen_id(schema["id_prefix"])
            form_data["olusturma_zamani"] = _now()
            if stu_data:
                form_data["ogrenci_id"] = stu_data.get("id", "")

            store.upsert(store_key, form_data)
            st.success(f"✅ {schema['title']} kaydedildi!")
            st.rerun()


# ────────────────────────────────────────────────────────────
# KATEGORİ BAZLI FORM SEÇİCİ (MEB Formları sekmesi)
# ────────────────────────────────────────────────────────────

_KATEGORI_SIRASI = ["Görüşme", "Gözlem", "Aile", "Yönlendirme", "Rapor", "Grup", "İhtiyaç", "Okul Öncesi"]

_KATEGORI_META = {
    "Görüşme":      ("💬", "#7c3aed", "Öğrenci, veli, öğretmen ve disiplin görüşme formları"),
    "Gözlem":       ("👁️", "#3b82f6", "Öğrenci gözlem, ÖÖG ve DEHB gözlem formları"),
    "Aile":         ("👨‍👩‍👧", "#0d9488", "Ev ziyareti ve çocuk tanıma formları"),
    "Yönlendirme":  ("🧭", "#f59e0b", "Eğitsel değerlendirme, psikolojik ve sağlık yönlendirme"),
    "Rapor":        ("📈", "#10b981", "Bireysel gelişim raporu, randevu ve görüşme kayıt çizelgeleri"),
    "Grup":         ("👥", "#8b5cf6", "Grup çalışma, sosyometri, yaşam pencerem, kimdir bu"),
    "İhtiyaç":      ("🎯", "#ef4444", "İhtiyaç belirleme, sınıf ve okul risk haritaları"),
    "Okul Öncesi":  ("🎓", "#ec4899", "Okul öncesi kazanım kontrol ve ihtiyaç analizi formları"),
}


def render_meb_dijital_formlar(store):
    """MEB Dijital Formlar ana sekmesi — kategori seçimi + form açma."""
    _inject_meb_css()

    # Smarti AI welcome
    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("meb_formlar")
    except Exception:
        pass

    _styled_form_header(
        "MEB Dijital Formlar",
        "Özel Eğitim ve Rehberlik Hizmetleri Genel Müdürlüğü — 36 Resmi Form (Dijital)",
        "📄", "#1e293b",
    )

    # ── İstatistik kartları ──
    total_forms = len(MEB_FORM_SCHEMAS) + 1  # +1 for Aile Bilgi
    total_records = 0
    for schema in MEB_FORM_SCHEMAS.values():
        total_records += len(store.load_list(schema["store_key"]))
    total_records += len(store.load_list("aile_bilgi_formlari"))

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(f'<div class="meb-stat">📄 <b>{total_forms}</b> Form Şablonu</div>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<div class="meb-stat">📝 <b>{total_records}</b> Doldurulan Kayıt</div>', unsafe_allow_html=True)
    with sc3:
        st.markdown(f'<div class="meb-stat">📂 <b>8</b> Kategori</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Tüm Formlar — Global Selectbox ──
    # Kategoriye göre gruplu seçenek listesi oluştur
    all_form_options: list[tuple[str, str, str]] = []  # (schema_key, display_label, kategori)
    for kategori in _KATEGORI_SIRASI:
        # Aile Bilgi Formu özel
        if kategori == "Aile":
            all_form_options.append(("__aile_bilgi__",
                                     f"📋 Aile Bilgi Formu (B.K.G.1.c)", kategori))
        schemas = get_schemas_by_kategori(kategori)
        for s_key, s in schemas:
            kat_icon = _KATEGORI_META[kategori][0]
            all_form_options.append((s_key, f"{s['icon']} {s['title']}", kategori))

    # Grouped display: "Kategori > Form Adı"
    option_keys = [o[0] for o in all_form_options]
    option_labels = {o[0]: f"[{o[2]}]  {o[1]}" for o in all_form_options}

    selected_key = st.selectbox(
        "📄 Form Seçin:",
        option_keys,
        format_func=lambda x: option_labels.get(x, x),
        key="meb_global_form_sel",
        help="Tüm 36 MEB rehberlik formuna buradan ulaşabilirsiniz",
    )

    if selected_key:
        st.markdown("---")

        if selected_key == "__aile_bilgi__":
            from views.rehberlik import _render_aile_bilgi_formu, _get_rhb_store
            _render_aile_bilgi_formu(_get_rhb_store())
        else:
            sk = MEB_FORM_SCHEMAS[selected_key]["store_key"]
            count = len(store.load_list(sk))
            st.caption(f"Mevcut kayıt: {count}")
            render_generic_form(store, selected_key)

    # ── AI Öğrenci Değerlendirmesi ──
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed22,#6d28d911);'
        'border:1px solid #7c3aed44;border-radius:10px;padding:12px 16px;margin-top:10px;">'
        '<b>🤖 AI Öğrenci Değerlendirmesi</b> — Bir öğrencinin tüm MEB form verilerini AI ile analiz edin</div>',
        unsafe_allow_html=True,
    )
    try:
        from utils.shared_data import get_student_display_options
        _ai_students = get_student_display_options(include_empty=False)
    except Exception:
        _ai_students = {}

    _ai_sel = st.selectbox("Öğrenci Seçin:", [""] + list(_ai_students.keys()),
                           key="meb_ai_stu_sel")
    if _ai_sel:
        _ai_stu = _ai_students.get(_ai_sel, {})
        _ai_sid = _ai_stu.get("id", "")
        _ai_name = _ai_sel.split("(")[0].strip() if _ai_sel else ""
        if _ai_sid:
            render_ai_ogrenci_panel(store, _ai_sid, _ai_name)
