"""
Yemek Tercihi ve Alerji Takip Modulu - Streamlit UI
=====================================================
Ogrenci yemek tercihleri, alerji raporu, menu planlama ve istatistik.
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

TERCIH_PATH = "data/yemek/ogrenci_tercihleri.json"
MENU_PATH = "data/akademik/yemek_menusu.json"
STUDENTS_PATH = "data/akademik/students.json"

DIYET_TURLERI = ["Normal", "Vejetaryen", "Vegan", "Glutensiz", "Diger"]

ALERJI_TURLERI = [
    "Fistik", "Sut", "Yumurta", "Gluten",
    "Kabuklu Deniz Urunleri", "Soya", "Findik",
    "Susam", "Kereviz", "Hardal", "Diger",
]

# Yemek-alerjen eslestirmesi (basit kural tabani)
ALLERGEN_MAP = {
    "Makarna": ["Gluten"],
    "Kek": ["Gluten", "Yumurta", "Sut"],
    "Sutlac": ["Sut"],
    "Pilav": [],
    "Tavuk Sinitzel": ["Gluten", "Yumurta"],
    "Izgara Tavuk": [],
    "Firinda Balik": ["Kabuklu Deniz Urunleri"],
    "Karniyarik": [],
    "Kofte": ["Gluten"],
    "Etli Nohut": [],
    "Patates Pure": ["Sut"],
    "Sebze Sote": [],
    "Komposto": [],
    "Meyve": [],
    "Yayla Corbasi": ["Sut", "Yumurta"],
    "Domates Corbasi": [],
    "Tavuk Suyu Corbasi": [],
    "Ezogelin": [],
    "Coban Salata": [],
    "Mor Lahana": [],
    "Havuc Salata": [],
    "Mevsim Salata": [],
}

GUNLER = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]


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


def _gen_id(prefix="yt"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _load_students():
    return _load(STUDENTS_PATH)


# ---------------------------------------------------------------------------
# Ornek Veri Olustur
# ---------------------------------------------------------------------------

SAMPLE_PREFERENCES = [
    {"diyet_turu": "Normal", "alerjiler": []},
    {"diyet_turu": "Normal", "alerjiler": ["Fistik"]},
    {"diyet_turu": "Vejetaryen", "alerjiler": []},
    {"diyet_turu": "Normal", "alerjiler": ["Sut", "Yumurta"]},
    {"diyet_turu": "Glutensiz", "alerjiler": ["Gluten"]},
    {"diyet_turu": "Normal", "alerjiler": ["Kabuklu Deniz Urunleri"]},
    {"diyet_turu": "Vegan", "alerjiler": ["Sut", "Yumurta"]},
    {"diyet_turu": "Normal", "alerjiler": ["Soya"]},
    {"diyet_turu": "Normal", "alerjiler": ["Fistik", "Findik"]},
    {"diyet_turu": "Vejetaryen", "alerjiler": ["Sut"]},
]


def _ensure_sample_preferences():
    prefs = _load(TERCIH_PATH)
    if prefs:
        return prefs
    students = _load_students()
    if not students:
        return []
    result = []
    for i, s in enumerate(students[:30]):  # ilk 30 ogrenci
        pref_template = SAMPLE_PREFERENCES[i % len(SAMPLE_PREFERENCES)]
        result.append({
            "id": _gen_id("yt"),
            "student_id": s["id"],
            "ogrenci_adi": f"{s['ad']} {s['soyad']}",
            "sinif": s.get("sinif", ""),
            "sube": s.get("sube", ""),
            "diyet_turu": pref_template["diyet_turu"],
            "alerjiler": pref_template["alerjiler"],
            "notlar": "",
            "guncelleme_tarihi": date.today().isoformat(),
        })
    _save(TERCIH_PATH, result)
    return result


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def _inject_css():
    st.markdown("""
    <style>
    .alerji-critical {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #c62828;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .alerji-critical h4 { color: #b71c1c; margin: 0 0 6px 0; }
    .alerji-warning {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        border-left: 5px solid #f57f17;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .alerji-warning h4 { color: #e65100; margin: 0 0 6px 0; }
    .menu-day {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 8px;
        border-left: 5px solid #2e7d32;
    }
    .menu-day h4 { color: #1b5e20; margin: 0 0 6px 0; }
    .conflict-alert {
        background: #ff5252;
        color: white;
        padding: 6px 14px;
        border-radius: 8px;
        margin: 4px 0;
        font-size: 13px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1a237e 0%, #1565c0 100%);
        color: white;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .stat-card .val { font-size: 28px; font-weight: 700; }
    .stat-card .lbl { font-size: 13px; opacity: .85; }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 1: Tercihler
# ---------------------------------------------------------------------------

def _tab_tercihler():
    st.subheader("Ogrenci Yemek Tercihleri")
    prefs = _ensure_sample_preferences()
    students = _load_students()

    # Ozet metrikler
    toplam = len(prefs)
    alerji_var = len([p for p in prefs if p.get("alerjiler")])
    diyet_ozel = len([p for p in prefs if p.get("diyet_turu", "Normal") != "Normal"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Kayitli Ogrenci", toplam)
    with c2:
        st.metric("Alerjisi Olan", alerji_var)
    with c3:
        st.metric("Ozel Diyet", diyet_ozel)

    st.divider()

    # Mevcut tercihler tablosu
    if prefs:
        df_data = []
        for p in prefs:
            df_data.append({
                "Ogrenci": p.get("ogrenci_adi", ""),
                "Sinif": f"{p.get('sinif', '')}{p.get('sube', '')}",
                "Diyet Turu": p.get("diyet_turu", "Normal"),
                "Alerjiler": ", ".join(p.get("alerjiler", [])) or "-",
                "Guncelleme": p.get("guncelleme_tarihi", ""),
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)

    st.divider()

    # Tercih ekleme / duzenleme
    st.markdown("**Tercih Ekle / Duzenle**")

    existing_student_ids = {p["student_id"] for p in prefs}
    mode = st.radio("Islem", ["Yeni Kayit", "Mevcut Duzenle"], horizontal=True, key="tercih_mode")

    if mode == "Yeni Kayit":
        # Henuz tercihi olmayan ogrenciler
        unregistered = [s for s in students if s["id"] not in existing_student_ids]
        if not unregistered:
            st.info("Tum ogrencilerin tercihi kayitli.")
            return

        with st.form("add_pref_form", clear_on_submit=True):
            student_labels = [f"{s['ad']} {s['soyad']} ({s.get('sinif', '?')}{s.get('sube', '')})" for s in unregistered]
            sel_student = st.selectbox("Ogrenci", student_labels, key="pref_ogrenci")

            c1, c2 = st.columns(2)
            with c1:
                diyet = st.selectbox("Diyet Turu", DIYET_TURLERI, key="pref_diyet")
            with c2:
                alerjiler = st.multiselect("Alerjiler", ALERJI_TURLERI, key="pref_alerji")

            notlar = st.text_area("Ek Notlar", key="pref_notlar", height=80)

            if st.form_submit_button("Kaydet", type="primary"):
                s_idx = student_labels.index(sel_student)
                s = unregistered[s_idx]
                new_pref = {
                    "id": _gen_id("yt"),
                    "student_id": s["id"],
                    "ogrenci_adi": f"{s['ad']} {s['soyad']}",
                    "sinif": s.get("sinif", ""),
                    "sube": s.get("sube", ""),
                    "diyet_turu": diyet,
                    "alerjiler": alerjiler,
                    "notlar": notlar,
                    "guncelleme_tarihi": date.today().isoformat(),
                }
                prefs.append(new_pref)
                _save(TERCIH_PATH, prefs)
                st.success(f"{s['ad']} {s['soyad']} icin tercih kaydedildi.")
                st.rerun()

    elif mode == "Mevcut Duzenle" and prefs:
        pref_labels = [f"{p['ogrenci_adi']} ({p.get('sinif', '')}{p.get('sube', '')})" for p in prefs]
        sel_pref = st.selectbox("Ogrenci Sec", pref_labels, key="edit_pref_sel")
        p_idx = pref_labels.index(sel_pref)
        p = prefs[p_idx]

        with st.form("edit_pref_form"):
            c1, c2 = st.columns(2)
            with c1:
                diyet = st.selectbox("Diyet Turu", DIYET_TURLERI,
                                     index=DIYET_TURLERI.index(p.get("diyet_turu", "Normal")),
                                     key="edit_diyet")
            with c2:
                alerjiler = st.multiselect("Alerjiler", ALERJI_TURLERI,
                                           default=p.get("alerjiler", []),
                                           key="edit_alerji")

            notlar = st.text_area("Ek Notlar", value=p.get("notlar", ""), key="edit_notlar", height=80)

            if st.form_submit_button("Guncelle", type="primary"):
                prefs[p_idx]["diyet_turu"] = diyet
                prefs[p_idx]["alerjiler"] = alerjiler
                prefs[p_idx]["notlar"] = notlar
                prefs[p_idx]["guncelleme_tarihi"] = date.today().isoformat()
                _save(TERCIH_PATH, prefs)
                st.success("Tercih guncellendi.")
                st.rerun()


# ---------------------------------------------------------------------------
# TAB 2: Alerji Raporu
# ---------------------------------------------------------------------------

def _tab_alerji_raporu():
    st.subheader("Alerji Raporu")
    prefs = _ensure_sample_preferences()

    if not prefs:
        st.info("Tercih verisi bulunamadi.")
        return

    # Alerji turleri bazinda ogrenci sayisi
    alerji_counts = {}
    for p in prefs:
        for a in p.get("alerjiler", []):
            alerji_counts[a] = alerji_counts.get(a, 0) + 1

    if not alerji_counts:
        st.success("Kayitli ogrencilerde alerji bilgisi bulunmuyor.")
        return

    # Kritik alerji ozet
    st.markdown("#### Alerji Ozeti")
    sorted_allergies = sorted(alerji_counts.items(), key=lambda x: x[1], reverse=True)

    cols = st.columns(min(len(sorted_allergies), 4))
    for i, (alerji, count) in enumerate(sorted_allergies[:4]):
        with cols[i]:
            st.metric(alerji, f"{count} ogrenci")

    st.divider()

    # Detayli tablo
    st.markdown("#### Alerji Detay Tablosu")
    alerji_df = pd.DataFrame(sorted_allergies, columns=["Alerji Turu", "Ogrenci Sayisi"])
    st.dataframe(alerji_df, use_container_width=True, hide_index=True)

    st.divider()

    # Ciddi alerji uyari kartlari
    st.markdown("#### Kritik Alerji Uyarilari")
    CRITICAL_ALLERGIES = ["Fistik", "Kabuklu Deniz Urunleri", "Findik"]

    for alerji in CRITICAL_ALLERGIES:
        affected = [p for p in prefs if alerji in p.get("alerjiler", [])]
        if affected:
            names = ", ".join([p["ogrenci_adi"] for p in affected])
            st.markdown(f"""
            <div class="alerji-critical">
                <h4>KRITIK: {alerji} Alerjisi - {len(affected)} ogrenci</h4>
                <p><b>Etkilenen ogrenciler:</b> {names}</p>
                <p><em>Bu alerji ciddi anafilaktik reaksiyona neden olabilir. Menu planlamasinda ozel dikkat gereklidir.</em></p>
            </div>
            """, unsafe_allow_html=True)

    other_allergies = [a for a in alerji_counts if a not in CRITICAL_ALLERGIES]
    for alerji in other_allergies:
        affected = [p for p in prefs if alerji in p.get("alerjiler", [])]
        if affected:
            names = ", ".join([p["ogrenci_adi"] for p in affected])
            st.markdown(f"""
            <div class="alerji-warning">
                <h4>UYARI: {alerji} Alerjisi - {len(affected)} ogrenci</h4>
                <p><b>Etkilenen ogrenciler:</b> {names}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Export
    st.markdown("#### Rapor Disa Aktar")
    c1, c2 = st.columns(2)
    with c1:
        # CSV export
        export_data = []
        for p in prefs:
            if p.get("alerjiler"):
                export_data.append({
                    "Ogrenci": p["ogrenci_adi"],
                    "Sinif": f"{p.get('sinif', '')}{p.get('sube', '')}",
                    "Diyet": p.get("diyet_turu", ""),
                    "Alerjiler": ", ".join(p.get("alerjiler", [])),
                })
        if export_data:
            csv_df = pd.DataFrame(export_data)
            csv_data = csv_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "CSV Indir",
                data=csv_data,
                file_name=f"alerji_raporu_{date.today().isoformat()}.csv",
                mime="text/csv",
            )

    with c2:
        # Basit text rapor
        report_lines = [f"ALERJI RAPORU - {date.today().isoformat()}", "=" * 40, ""]
        for alerji, count in sorted_allergies:
            report_lines.append(f"{alerji}: {count} ogrenci")
            affected = [p["ogrenci_adi"] for p in prefs if alerji in p.get("alerjiler", [])]
            for name in affected:
                report_lines.append(f"  - {name}")
            report_lines.append("")

        report_text = "\n".join(report_lines)
        st.download_button(
            "Metin Rapor Indir",
            data=report_text.encode("utf-8"),
            file_name=f"alerji_raporu_{date.today().isoformat()}.txt",
            mime="text/plain",
        )


# ---------------------------------------------------------------------------
# TAB 3: Menu Planlama
# ---------------------------------------------------------------------------

def _tab_menu_planlama():
    st.subheader("Haftalik Menu Planlama")
    menu = _load(MENU_PATH)
    prefs = _ensure_sample_preferences()

    # Hafta secimi
    week_start = st.date_input("Hafta baslangici (Pazartesi)", value=date.today(), key="menu_week")

    st.divider()

    # Mevcut menu goruntuleme
    if menu:
        st.markdown("#### Mevcut Menu")
        for m in menu[:5]:
            st.markdown(f"""
            <div class="menu-day">
                <h4>{m.get('gun', '')} - {m.get('tarih', '')}</h4>
                <p><b>Corba:</b> {m.get('corba', '-')} | <b>Ana Yemek:</b> {m.get('ana_yemek', '-')}
                | <b>Yan Yemek:</b> {m.get('yan_yemek', '-')} | <b>Tatli:</b> {m.get('tatli', '-')}</p>
                <p><b>Kalori:</b> {m.get('kalori', '-')} kcal</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Menu duzenleme formu
    st.markdown("#### Yeni Haftalik Menu Olustur")

    new_menu = []
    for i, gun in enumerate(GUNLER):
        tarih = week_start + timedelta(days=i)
        if tarih.weekday() > 4:  # hafta sonu atla
            continue

        st.markdown(f"**{gun} ({tarih.isoformat()})**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            corba = st.text_input("Corba", key=f"menu_{gun}_corba", placeholder="Orn: Mercimek")
        with c2:
            ana = st.text_input("Ana Yemek", key=f"menu_{gun}_ana", placeholder="Orn: Kofte")
        with c3:
            yan = st.text_input("Yan Yemek", key=f"menu_{gun}_yan", placeholder="Orn: Pilav")
        with c4:
            tatli = st.text_input("Tatli", key=f"menu_{gun}_tatli", placeholder="Orn: Komposto")

        new_menu.append({
            "gun": gun,
            "tarih": tarih.isoformat(),
            "corba": corba,
            "ana_yemek": ana,
            "yan_yemek": yan,
            "tatli": tatli,
        })

    st.divider()

    # Alerji cakisma kontrolu
    st.markdown("#### Alerji Cakisma Kontrolu")
    conflicts_found = False

    all_student_allergies = {}
    for p in prefs:
        for a in p.get("alerjiler", []):
            if a not in all_student_allergies:
                all_student_allergies[a] = []
            all_student_allergies[a].append(p["ogrenci_adi"])

    for day_menu in new_menu:
        day_items = [
            day_menu.get("corba", ""),
            day_menu.get("ana_yemek", ""),
            day_menu.get("yan_yemek", ""),
            day_menu.get("tatli", ""),
        ]

        for item in day_items:
            if not item:
                continue
            allergens = ALLERGEN_MAP.get(item, [])
            for allergen in allergens:
                if allergen in all_student_allergies:
                    affected = all_student_allergies[allergen]
                    conflicts_found = True
                    st.markdown(f"""
                    <div class="conflict-alert">
                        <b>{day_menu['gun']}:</b> "{item}" iceriyor: <b>{allergen}</b> -
                        Etkilenen: {', '.join(affected[:5])}{f' (+{len(affected)-5})' if len(affected) > 5 else ''}
                    </div>
                    """, unsafe_allow_html=True)

    if not conflicts_found:
        filled = any(d.get("corba") or d.get("ana_yemek") for d in new_menu)
        if filled:
            st.success("Alerji cakismasi tespit edilmedi.")
        else:
            st.info("Menu ogelerini girin, alerji kontrolu otomatik yapilacaktir.")

    st.divider()

    if st.button("Menuyu Kaydet", type="primary", key="save_menu"):
        valid_menu = [d for d in new_menu if d.get("corba") or d.get("ana_yemek")]
        if not valid_menu:
            st.error("En az bir gun icin menu girisi yapin.")
        else:
            # Her gune id ve kalori ekle
            final_menu = []
            for d in valid_menu:
                d["id"] = _gen_id("ymk")
                d["kalori"] = 650  # tahmini varsayilan
                d["salata"] = "Mevsim Salata"
                final_menu.append(d)

            # Mevcut menuye ekle veya degistir
            existing = _load(MENU_PATH)
            new_dates = {d["tarih"] for d in final_menu}
            kept = [m for m in existing if m.get("tarih") not in new_dates]
            kept.extend(final_menu)
            kept.sort(key=lambda x: x.get("tarih", ""))
            _save(MENU_PATH, kept)
            st.success(f"{len(final_menu)} gunluk menu kaydedildi.")
            st.rerun()


# ---------------------------------------------------------------------------
# TAB 4: Istatistik
# ---------------------------------------------------------------------------

def _tab_istatistik():
    st.subheader("Yemek ve Alerji Istatistikleri")
    prefs = _ensure_sample_preferences()

    if not prefs:
        st.info("Tercih verisi bulunamadi.")
        return

    # Diyet turu dagilimi
    st.markdown("#### Diyet Turu Dagilimi")
    diyet_counts = {}
    for p in prefs:
        d = p.get("diyet_turu", "Normal")
        diyet_counts[d] = diyet_counts.get(d, 0) + 1

    c1, c2 = st.columns(2)
    with c1:
        diyet_df = pd.DataFrame(list(diyet_counts.items()), columns=["Diyet Turu", "Ogrenci Sayisi"])
        st.dataframe(diyet_df, use_container_width=True, hide_index=True)
    with c2:
        st.bar_chart(diyet_df.set_index("Diyet Turu"))

    st.divider()

    # En yaygin alerjiler
    st.markdown("#### En Yaygin Alerjiler")
    alerji_counts = {}
    for p in prefs:
        for a in p.get("alerjiler", []):
            alerji_counts[a] = alerji_counts.get(a, 0) + 1

    if alerji_counts:
        sorted_a = sorted(alerji_counts.items(), key=lambda x: x[1], reverse=True)
        alerji_df = pd.DataFrame(sorted_a, columns=["Alerji", "Ogrenci Sayisi"])

        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(alerji_df, use_container_width=True, hide_index=True)
        with c2:
            st.bar_chart(alerji_df.set_index("Alerji"))
    else:
        st.info("Alerji kaydedilmis ogrenci bulunmuyor.")

    st.divider()

    # Sinif bazinda alerji dagilimi
    st.markdown("#### Sinif Bazinda Alerji Dagilimi")
    sinif_alerji = {}
    for p in prefs:
        sinif = f"{p.get('sinif', '?')}{p.get('sube', '')}"
        alerji_count = len(p.get("alerjiler", []))
        if sinif not in sinif_alerji:
            sinif_alerji[sinif] = {"toplam": 0, "alerjili": 0}
        sinif_alerji[sinif]["toplam"] += 1
        if alerji_count > 0:
            sinif_alerji[sinif]["alerjili"] += 1

    if sinif_alerji:
        sinif_df_data = []
        for sinif, vals in sorted(sinif_alerji.items()):
            oran = round(vals["alerjili"] / vals["toplam"] * 100, 1) if vals["toplam"] else 0
            sinif_df_data.append({
                "Sinif": sinif,
                "Toplam Ogrenci": vals["toplam"],
                "Alerjili Ogrenci": vals["alerjili"],
                "Alerji Orani (%)": oran,
            })
        sinif_df = pd.DataFrame(sinif_df_data)
        st.dataframe(sinif_df, use_container_width=True, hide_index=True)

        # Sinif bazinda bar chart
        chart_df = pd.DataFrame({
            "Sinif": [d["Sinif"] for d in sinif_df_data],
            "Alerjili": [d["Alerjili Ogrenci"] for d in sinif_df_data],
            "Normal": [d["Toplam Ogrenci"] - d["Alerjili Ogrenci"] for d in sinif_df_data],
        })
        st.bar_chart(chart_df.set_index("Sinif"))

    st.divider()

    # Genel ozet metrikleri
    st.markdown("#### Genel Ozet")
    toplam = len(prefs)
    alerji_var = len([p for p in prefs if p.get("alerjiler")])
    diyet_ozel = len([p for p in prefs if p.get("diyet_turu", "Normal") != "Normal"])
    en_yaygin = sorted_a[0][0] if alerji_counts else "-"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Kayit", toplam)
    with c2:
        st.metric("Alerjili Ogrenci", alerji_var)
    with c3:
        st.metric("Ozel Diyet", diyet_ozel)
    with c4:
        st.metric("En Yaygin Alerji", en_yaygin)


# ---------------------------------------------------------------------------
# ANA FONKSIYON
# ---------------------------------------------------------------------------

def render_yemek_tercihi():
    """Yemek Tercihi ve Alerji Takip ana giris noktasi."""
    _inject_css()
    st.title("Yemek Tercihi ve Alerji Takip")
    st.caption("Ogrenci diyet tercihleri, alerji yonetimi, menu planlama ve istatistikler")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Tercihler",
        "Alerji Raporu",
        "Menu Planlama",
        "Istatistik",
    ])

    with tab1:
        _tab_tercihler()
    with tab2:
        _tab_alerji_raporu()
    with tab3:
        _tab_menu_planlama()
    with tab4:
        _tab_istatistik()


if __name__ == "__main__":
    render_yemek_tercihi()
