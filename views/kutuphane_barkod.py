"""
Kutuphane Barkod Yonetim Modulu - Streamlit UI
================================================
Kitap arama, odunc verme, iade alma, envanter ve barkod uretici.
"""

import streamlit as st
import json
import uuid
import pandas as pd
from pathlib import Path
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# Veri Yardimcilari
# ---------------------------------------------------------------------------

KITAPLAR_PATH = "data/kutuphane/kitaplar.json"
ODUNC_PATH = "data/kutuphane/odunc_kayitlari.json"
STUDENTS_PATH = "data/akademik/students.json"

KATEGORILER = [
    "Roman", "Hikaye", "Siir", "Bilim", "Tarih", "Felsefe",
    "Cocuk", "Genclik", "Ansiklopedi", "Ders Kitabi",
    "Biyografi", "Sanat", "Doga", "Matematik", "Edebiyat",
]


def _load(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _gen_id(prefix="kit"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _load_students():
    return _load(STUDENTS_PATH)


# ---------------------------------------------------------------------------
# Ornek Veri Olustur
# ---------------------------------------------------------------------------

SAMPLE_BOOKS = [
    {"baslik": "Kucuk Prens", "yazar": "Antoine de Saint-Exupery", "isbn": "9789750719387", "kategori": "Roman", "raf_no": "A-01", "adet": 3},
    {"baslik": "Sefiller", "yazar": "Victor Hugo", "isbn": "9789750738609", "kategori": "Roman", "raf_no": "A-02", "adet": 2},
    {"baslik": "Ince Memed", "yazar": "Yasar Kemal", "isbn": "9789750709869", "kategori": "Roman", "raf_no": "A-03", "adet": 2},
    {"baslik": "Tutunamayanlar", "yazar": "Oguz Atay", "isbn": "9789754705850", "kategori": "Roman", "raf_no": "A-04", "adet": 1},
    {"baslik": "Saatleri Ayarlama Enstitusu", "yazar": "Ahmet Hamdi Tanpinar", "isbn": "9789759952570", "kategori": "Roman", "raf_no": "A-05", "adet": 2},
    {"baslik": "Bereketli Topraklar Uzerinde", "yazar": "Orhan Kemal", "isbn": "9789750712456", "kategori": "Roman", "raf_no": "A-06", "adet": 1},
    {"baslik": "Nutuk", "yazar": "Mustafa Kemal Ataturk", "isbn": "9789754063844", "kategori": "Tarih", "raf_no": "B-01", "adet": 4},
    {"baslik": "Sofinin Dunyasi", "yazar": "Jostein Gaarder", "isbn": "9789750726422", "kategori": "Felsefe", "raf_no": "C-01", "adet": 2},
    {"baslik": "Hayvan Ciftligi", "yazar": "George Orwell", "isbn": "9789750718533", "kategori": "Roman", "raf_no": "A-07", "adet": 3},
    {"baslik": "Simyaci", "yazar": "Paulo Coelho", "isbn": "9789750726019", "kategori": "Roman", "raf_no": "A-08", "adet": 2},
    {"baslik": "Cosmos", "yazar": "Carl Sagan", "isbn": "9786053752813", "kategori": "Bilim", "raf_no": "D-01", "adet": 1},
    {"baslik": "Sapiens", "yazar": "Yuval Noah Harari", "isbn": "9786053752769", "kategori": "Tarih", "raf_no": "B-02", "adet": 2},
    {"baslik": "Olmeye Yatmak", "yazar": "Adalet Agaoglu", "isbn": "9789750512742", "kategori": "Roman", "raf_no": "A-09", "adet": 1},
    {"baslik": "Calisku Cocuk Haylaz Cocuk", "yazar": "Elif Safak", "isbn": "9789750519741", "kategori": "Cocuk", "raf_no": "E-01", "adet": 3},
    {"baslik": "Matematik Hikayeleri", "yazar": "Ali Nesin", "isbn": "9789752757239", "kategori": "Matematik", "raf_no": "F-01", "adet": 2},
    {"baslik": "Dede Korkut Hikayeleri", "yazar": "Muharrem Ergin", "isbn": "9789753381011", "kategori": "Hikaye", "raf_no": "E-02", "adet": 3},
    {"baslik": "Bir Bilim Adami Hikayesi", "yazar": "Aziz Sancar", "isbn": "9786050938586", "kategori": "Biyografi", "raf_no": "G-01", "adet": 1},
    {"baslik": "Kurt Seyt ve Shura", "yazar": "Nermin Bezmen", "isbn": "9789752100596", "kategori": "Roman", "raf_no": "A-10", "adet": 2},
    {"baslik": "Sessiz Ev", "yazar": "Orhan Pamuk", "isbn": "9789754704228", "kategori": "Roman", "raf_no": "A-11", "adet": 1},
    {"baslik": "Cocuklara Bilim", "yazar": "Canan Dagdeviren", "isbn": "9786050969153", "kategori": "Bilim", "raf_no": "D-02", "adet": 2},
]


def _ensure_sample_books():
    books = _load(KITAPLAR_PATH)
    if books:
        return books
    result = []
    for b in SAMPLE_BOOKS:
        result.append({
            "id": _gen_id("kit"),
            "baslik": b["baslik"],
            "yazar": b["yazar"],
            "isbn": b["isbn"],
            "kategori": b["kategori"],
            "raf_no": b["raf_no"],
            "adet": b["adet"],
            "odunc_adet": 0,
            "durum": "mevcut",
            "eklenme_tarihi": date.today().isoformat(),
        })
    _save(KITAPLAR_PATH, result)
    return result


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def _inject_css():
    st.markdown("""
    <style>
    .ktp-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 5px solid #e65100;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .ktp-card h4 { margin: 0 0 6px 0; color: #bf360c; }
    .ktp-card p { margin: 2px 0; font-size: 14px; }
    .barcode-box {
        font-family: 'Courier New', monospace;
        font-size: 18px;
        letter-spacing: 4px;
        background: white;
        border: 2px solid #333;
        padding: 12px 20px;
        text-align: center;
        margin: 8px 0;
        border-radius: 4px;
    }
    .barcode-label {
        font-size: 11px;
        text-align: center;
        color: #555;
        margin-top: 4px;
    }
    .barkod-container {
        border: 1px dashed #ccc;
        padding: 16px;
        margin: 8px;
        border-radius: 8px;
        text-align: center;
        page-break-inside: avoid;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 1: Kitap Arama
# ---------------------------------------------------------------------------

def _tab_kitap_arama():
    st.subheader("Kitap Arama")
    books = _ensure_sample_books()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        q_baslik = st.text_input("Baslik", key="search_baslik")
    with c2:
        q_yazar = st.text_input("Yazar", key="search_yazar")
    with c3:
        q_isbn = st.text_input("ISBN", key="search_isbn")
    with c4:
        q_kategori = st.selectbox("Kategori", ["Tumu"] + KATEGORILER, key="search_kat")

    # Filtrele
    filtered = books
    if q_baslik:
        filtered = [b for b in filtered if q_baslik.lower() in b.get("baslik", "").lower()]
    if q_yazar:
        filtered = [b for b in filtered if q_yazar.lower() in b.get("yazar", "").lower()]
    if q_isbn:
        filtered = [b for b in filtered if q_isbn in b.get("isbn", "")]
    if q_kategori != "Tumu":
        filtered = [b for b in filtered if b.get("kategori") == q_kategori]

    st.caption(f"{len(filtered)} kitap bulundu")

    if filtered:
        df_data = []
        for b in filtered:
            odunc_adet = b.get("odunc_adet", 0)
            mevcut = b.get("adet", 0) - odunc_adet
            durum = "Mevcut" if mevcut > 0 else "Tumu Odunc"
            df_data.append({
                "Baslik": b["baslik"],
                "Yazar": b["yazar"],
                "ISBN": b["isbn"],
                "Kategori": b.get("kategori", ""),
                "Raf No": b.get("raf_no", ""),
                "Adet": b.get("adet", 0),
                "Mevcut": max(mevcut, 0),
                "Durum": durum,
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        st.info("Arama kriterlerine uygun kitap bulunamadi.")


# ---------------------------------------------------------------------------
# TAB 2: Odunc Ver
# ---------------------------------------------------------------------------

def _tab_odunc_ver():
    st.subheader("Kitap Odunc Verme")
    books = _ensure_sample_books()
    students = _load_students()
    odunc = _load(ODUNC_PATH)

    # Mevcut kitaplar
    available_books = [
        b for b in books
        if (b.get("adet", 0) - b.get("odunc_adet", 0)) > 0
    ]

    if not available_books:
        st.warning("Odunc verilebilecek kitap bulunamadi.")
        return

    with st.form("odunc_form", clear_on_submit=True):
        st.markdown("**Odunc Verme Formu**")

        c1, c2 = st.columns(2)
        with c1:
            book_labels = [f"{b['baslik']} - {b['yazar']} (ISBN: {b['isbn']})" for b in available_books]
            sel_book = st.selectbox("Kitap Sec", book_labels, key="odunc_kitap")

            barkod_input = st.text_input("Barkod / ISBN (opsiyonel)", key="odunc_barkod",
                                         help="ISBN veya barkod ile hizli secim")

        with c2:
            student_labels = [f"{s['ad']} {s['soyad']} ({s.get('sinif', '?')}{s.get('sube', '')} - {s.get('numara', '')})"
                              for s in students]
            sel_student = st.selectbox("Ogrenci Sec", student_labels, key="odunc_ogrenci") if students else None

            odunc_tarihi = st.date_input("Odunc Tarihi", value=date.today(), key="odunc_tarih")
            iade_tarihi = st.date_input("Beklenen Iade Tarihi", value=date.today() + timedelta(days=15), key="iade_tarih")

        if st.form_submit_button("Odunc Ver", type="primary"):
            if not students or sel_student is None:
                st.error("Ogrenci secilmedi.")
            else:
                book_idx = book_labels.index(sel_book)
                book = available_books[book_idx]
                student_idx = student_labels.index(sel_student)
                student = students[student_idx]

                new_odunc = {
                    "id": _gen_id("odn"),
                    "kitap_id": book["id"],
                    "kitap_baslik": book["baslik"],
                    "isbn": book["isbn"],
                    "student_id": student["id"],
                    "ogrenci_adi": f"{student['ad']} {student['soyad']}",
                    "sinif": student.get("sinif", ""),
                    "sube": student.get("sube", ""),
                    "odunc_tarihi": odunc_tarihi.isoformat(),
                    "beklenen_iade": iade_tarihi.isoformat(),
                    "iade_tarihi": None,
                    "durum": "odunc",
                    "gecikme_gun": 0,
                    "gecikme_ucreti": 0,
                }
                odunc.append(new_odunc)
                _save(ODUNC_PATH, odunc)

                # Kitap odunc adetini guncelle
                for b in books:
                    if b["id"] == book["id"]:
                        b["odunc_adet"] = b.get("odunc_adet", 0) + 1
                        if b["odunc_adet"] >= b.get("adet", 0):
                            b["durum"] = "odunc"
                        break
                _save(KITAPLAR_PATH, books)

                st.success(f"'{book['baslik']}' kitabi {student['ad']} {student['soyad']}'a odunc verildi.")
                st.rerun()

    # Aktif odunc listesi
    st.divider()
    st.markdown("**Aktif Odunc Islemleri**")
    aktif = [o for o in odunc if o.get("durum") == "odunc"]
    if aktif:
        df_data = []
        for o in aktif:
            days_left = (date.fromisoformat(o["beklenen_iade"]) - date.today()).days
            durum_txt = f"{days_left} gun kaldi" if days_left >= 0 else f"{abs(days_left)} gun gecikme!"
            df_data.append({
                "Kitap": o["kitap_baslik"],
                "Ogrenci": o["ogrenci_adi"],
                "Sinif": f"{o.get('sinif', '')}{o.get('sube', '')}",
                "Odunc Tarihi": o["odunc_tarihi"],
                "Beklenen Iade": o["beklenen_iade"],
                "Durum": durum_txt,
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        st.info("Aktif odunc islemi bulunmuyor.")


# ---------------------------------------------------------------------------
# TAB 3: Iade Al
# ---------------------------------------------------------------------------

def _tab_iade_al():
    st.subheader("Kitap Iade Alma")
    books = _load(KITAPLAR_PATH)
    odunc = _load(ODUNC_PATH)

    aktif = [o for o in odunc if o.get("durum") == "odunc"]

    if not aktif:
        st.info("Iade alinacak odunc kitap bulunmuyor.")
        return

    GECIKME_UCRETI_GUN = 2  # TL per gun

    st.markdown("**Odunc Kitaplar**")

    for i, o in enumerate(aktif):
        beklenen = date.fromisoformat(o["beklenen_iade"])
        bugun = date.today()
        gecikme = (bugun - beklenen).days
        gecikme_gun = max(gecikme, 0)
        gecikme_ucreti = gecikme_gun * GECIKME_UCRETI_GUN

        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        with col1:
            st.markdown(f"**{o['kitap_baslik']}**")
            st.caption(f"ISBN: {o.get('isbn', '-')}")
        with col2:
            st.write(f"{o['ogrenci_adi']}")
            st.caption(f"{o.get('sinif', '')}{o.get('sube', '')}")
        with col3:
            st.write(f"Odunc: {o['odunc_tarihi']}")
            st.caption(f"Beklenen: {o['beklenen_iade']}")
        with col4:
            if gecikme_gun > 0:
                st.error(f"Gecikme: {gecikme_gun} gun")
                st.caption(f"Ucret: {gecikme_ucreti} TL")
            else:
                kalan = abs(gecikme)
                st.success(f"{kalan} gun kaldi")
        with col5:
            if st.button("Iade Al", key=f"iade_{o['id']}", type="primary"):
                # Odunc kaydini guncelle
                for rec in odunc:
                    if rec["id"] == o["id"]:
                        rec["durum"] = "iade_edildi"
                        rec["iade_tarihi"] = bugun.isoformat()
                        rec["gecikme_gun"] = gecikme_gun
                        rec["gecikme_ucreti"] = gecikme_ucreti
                        break
                _save(ODUNC_PATH, odunc)

                # Kitap adetini geri al
                for b in books:
                    if b["id"] == o.get("kitap_id"):
                        b["odunc_adet"] = max(b.get("odunc_adet", 1) - 1, 0)
                        if b["odunc_adet"] < b.get("adet", 0):
                            b["durum"] = "mevcut"
                        break
                _save(KITAPLAR_PATH, books)

                st.success(f"'{o['kitap_baslik']}' iade alindi." +
                           (f" Gecikme ucreti: {gecikme_ucreti} TL" if gecikme_ucreti > 0 else ""))
                st.rerun()

        st.divider()


# ---------------------------------------------------------------------------
# TAB 4: Envanter
# ---------------------------------------------------------------------------

def _tab_envanter():
    st.subheader("Kutuphane Envanteri")
    books = _ensure_sample_books()
    odunc = _load(ODUNC_PATH)

    # Metrikler
    toplam_kitap = sum(b.get("adet", 0) for b in books)
    toplam_odunc = sum(b.get("odunc_adet", 0) for b in books)
    mevcut = toplam_kitap - toplam_odunc
    cesit = len(books)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Kitap", toplam_kitap)
    with c2:
        st.metric("Odunc Verilen", toplam_odunc)
    with c3:
        st.metric("Mevcut", mevcut)
    with c4:
        st.metric("Kitap Cesidi", cesit)

    st.divider()

    # Kategori dagilimi - pie chart
    st.markdown("#### Kategori Dagilimi")
    kat_counts = {}
    for b in books:
        k = b.get("kategori", "Diger")
        kat_counts[k] = kat_counts.get(k, 0) + b.get("adet", 0)

    kat_df = pd.DataFrame(list(kat_counts.items()), columns=["Kategori", "Adet"])
    st.bar_chart(kat_df.set_index("Kategori"))

    st.divider()

    # En cok odunc alinan kitaplar
    st.markdown("#### En Cok Odunc Alinan Kitaplar")
    odunc_all = _load(ODUNC_PATH)
    kitap_odunc_count = {}
    for o in odunc_all:
        baslik = o.get("kitap_baslik", "Bilinmeyen")
        kitap_odunc_count[baslik] = kitap_odunc_count.get(baslik, 0) + 1

    if kitap_odunc_count:
        sorted_books = sorted(kitap_odunc_count.items(), key=lambda x: x[1], reverse=True)[:10]
        pop_df = pd.DataFrame(sorted_books, columns=["Kitap", "Odunc Sayisi"])
        st.dataframe(pop_df, use_container_width=True, hide_index=True)
    else:
        st.info("Henuz odunc verme islemi yapilmamis.")

    st.divider()

    # Dusuk stok uyarilari
    st.markdown("#### Dusuk Stok Uyarilari")
    low_stock = [b for b in books if (b.get("adet", 0) - b.get("odunc_adet", 0)) <= 1]
    if low_stock:
        for b in low_stock:
            mevcut_adet = b.get("adet", 0) - b.get("odunc_adet", 0)
            if mevcut_adet <= 0:
                st.error(f"**{b['baslik']}** - Tum kopyalar odunc verilmis! (Toplam: {b.get('adet', 0)})")
            else:
                st.warning(f"**{b['baslik']}** - Sadece {mevcut_adet} kopya kaldi (Toplam: {b.get('adet', 0)})")
    else:
        st.success("Tum kitaplarin yeterli stoku mevcut.")


# ---------------------------------------------------------------------------
# TAB 5: Barkod Uretici
# ---------------------------------------------------------------------------

def _generate_barcode_visual(isbn: str) -> str:
    """ISBN icin basit metin tabanli barkod gorseli olustur."""
    bars = ""
    for ch in isbn:
        d = int(ch) if ch.isdigit() else 0
        bars += "|" * (d % 4 + 1) + " "
    return bars


def _tab_barkod_uretici():
    st.subheader("Barkod Uretici")
    books = _ensure_sample_books()

    st.markdown("Kitaplari secin ve barkod etiketleri uretin.")

    book_labels = [f"{b['baslik']} ({b['isbn']})" for b in books]
    selected = st.multiselect("Kitap Sec", book_labels, key="barkod_secim")

    if not selected:
        st.info("Barkod olusturmak icin kitap secin.")
        return

    adet_per_book = st.number_input("Her kitap icin etiket adedi", min_value=1, max_value=20, value=1,
                                     key="barkod_adet")

    if st.button("Barkod Olustur", type="primary", key="gen_barcode"):
        st.divider()
        st.markdown("### Barkod Etiketleri")
        st.caption("Asagidaki etiketleri yazdirilabilir formatta kullanabilirsiniz.")

        cols_per_row = 3
        selected_books = [books[book_labels.index(s)] for s in selected]

        all_labels = []
        for b in selected_books:
            for _ in range(adet_per_book):
                all_labels.append(b)

        for i in range(0, len(all_labels), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx >= len(all_labels):
                    break
                b = all_labels[idx]
                barcode_visual = _generate_barcode_visual(b["isbn"])
                with col:
                    st.markdown(f"""
                    <div class="barkod-container">
                        <div style="font-weight:600; font-size:13px; margin-bottom:6px;">{b['baslik']}</div>
                        <div class="barcode-box">{barcode_visual}</div>
                        <div class="barcode-label">ISBN: {b['isbn']}</div>
                        <div class="barcode-label">Raf: {b.get('raf_no', '-')} | Kat: {b.get('kategori', '-')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        st.info("Yazdirmak icin tarayicinizin yazdir (Ctrl+P) ozelligini kullanin.")


# ---------------------------------------------------------------------------
# ANA FONKSIYON
# ---------------------------------------------------------------------------

def render_kutuphane_barkod():
    """Kutuphane Barkod Yonetim ana giris noktasi."""
    _inject_css()
    st.title("Kutuphane ve Barkod Yonetimi")
    st.caption("Kitap arama, odunc verme, iade, envanter ve barkod uretici")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Kitap Arama",
        "Odunc Ver",
        "Iade Al",
        "Envanter",
        "Barkod Uretici",
    ])

    with tab1:
        _tab_kitap_arama()
    with tab2:
        _tab_odunc_ver()
    with tab3:
        _tab_iade_al()
    with tab4:
        _tab_envanter()
    with tab5:
        _tab_barkod_uretici()


if __name__ == "__main__":
    render_kutuphane_barkod()
