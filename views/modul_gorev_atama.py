"""
Modul Gorev Atama & Veli Raporu UI
====================================
Ogretmen gorev atama, gorev takibi, toplu atama ve
veli modul raporu arayuzu.
"""
from __future__ import annotations

import io
from datetime import date, datetime, timedelta
from typing import Any

import streamlit as st

from models.egitim_modulleri_ortak import (
    MODUL_ISIMLERI,
    MODUL_KATEGORILERI,
    GUCLU_ESIK,
    ZAYIF_ESIK,
    ActivityRecord,
    GorevTamamlama,
    ModulGorev,
    get_modul_ortak_store,
)
from utils.shared_data import load_shared_students
from utils.ui_common import styled_header, styled_section, _render_html, styled_info_banner

# ══════════════════════════════════════════════════════════════════════════════
# SABITLER
# ══════════════════════════════════════════════════════════════════════════════

_POPULER_AKTIVITELER: dict[str, list[dict[str, str]]] = {
    "matematik": [
        {"ad": "Hizli Hesap Oyunu", "tur": "oyun"},
        {"ad": "Olimpiyat Sorusu Cozumu", "tur": "olimpiyat"},
        {"ad": "Geometri Macerasi", "tur": "oyun"},
        {"ad": "Kesir Pizzasi", "tur": "oyun"},
        {"ad": "Sayi Bulmacasi", "tur": "bulmaca"},
        {"ad": "Denklem Dengesi", "tur": "oyun"},
        {"ad": "Carpim Savaslari", "tur": "oyun"},
        {"ad": "Sudoku", "tur": "bulmaca"},
        {"ad": "Mantik Problemi", "tur": "problem"},
        {"ad": "Konu Testi", "tur": "test"},
    ],
    "sanat": [
        {"ad": "Serbest Cizim", "tur": "gorsel"},
        {"ad": "Ritim Atolyesi", "tur": "muzik"},
        {"ad": "Hikaye Yazma", "tur": "yazarlik"},
        {"ad": "Kukla Tiyatrosu", "tur": "tiyatro"},
        {"ad": "Origami", "tur": "el_sanati"},
        {"ad": "Fotograf Gorevi", "tur": "fotograf"},
        {"ad": "Koro Calismasi", "tur": "muzik"},
        {"ad": "Kolaj Yapimi", "tur": "gorsel"},
    ],
    "bilisim": [
        {"ad": "Fizik Deneyi", "tur": "deney"},
        {"ad": "Kimya Deneyi", "tur": "deney"},
        {"ad": "Biyoloji Gozlemi", "tur": "deney"},
        {"ad": "Scratch Projesi", "tur": "kodlama"},
        {"ad": "Python Gorevi", "tur": "kodlama"},
        {"ad": "Bilim Senligi Projesi", "tur": "proje"},
        {"ad": "Robotik Gorev", "tur": "kodlama"},
        {"ad": "Deney Raporu Yazimi", "tur": "rapor"},
    ],
}

_DURUM_RENKLERI: dict[str, str] = {
    "tamamlandi": "#10b981",
    "kismi": "#f59e0b",
    "gecikti": "#ef4444",
    "bekliyor": "#64748b",
}

_DURUM_ETIKETLERI: dict[str, str] = {
    "tamamlandi": "Tamamlandi",
    "kismi": "Kismi",
    "gecikti": "Gecikti",
    "bekliyor": "Bekliyor",
}


# ══════════════════════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════════════════

def _get_sinif_ogrencileri(sinif: int, sube: str) -> list[dict]:
    """Belirtilen sinif ve subedeki ogrencileri dondurur."""
    students = load_shared_students()
    result = []
    for s in students:
        s_sinif = str(s.get("sinif", ""))
        s_sube = str(s.get("sube", ""))
        if s_sinif == str(sinif) and s_sube == sube:
            result.append(s)
    return result


def _get_student_id(student: dict) -> str:
    """Ogrenci dict'inden ID alanini dondurur."""
    return student.get("id", student.get("student_id", ""))


def _get_student_name(student: dict) -> str:
    """Ogrenci dict'inden ad soyad dondurur."""
    ad = student.get("ad", student.get("first_name", ""))
    soyad = student.get("soyad", student.get("last_name", ""))
    return f"{ad} {soyad}".strip()


def _durum_badge(durum: str) -> str:
    """Durum icin renkli HTML badge dondurur."""
    renk = _DURUM_RENKLERI.get(durum, "#64748b")
    etiket = _DURUM_ETIKETLERI.get(durum, durum)
    return (
        f'<span style="background:{renk};color:#fff;padding:3px 10px;'
        f'border-radius:6px;font-size:0.8rem;font-weight:600">{etiket}</span>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# ANA GIRIS NOKTASI
# ══════════════════════════════════════════════════════════════════════════════

def render_modul_gorev_atama():
    """Ogretmen gorev atama ve takip ana ekrani."""
    styled_header("Modul Gorev Atama", "Ogretmen gorev olusturma, takip ve toplu atama")

    tab1, tab2, tab3 = st.tabs(["Gorev Olustur", "Gorev Takibi", "Toplu Atama"])

    with tab1:
        _render_gorev_olustur()
    with tab2:
        _render_gorev_takibi()
    with tab3:
        _render_toplu_atama()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GOREV OLUSTUR
# ══════════════════════════════════════════════════════════════════════════════

def _render_gorev_olustur():
    """Tek gorev olusturma formu."""
    styled_section("Yeni Gorev Olustur", color="#6366F1")

    col1, col2 = st.columns(2)

    with col1:
        modul_secenekleri = {v: k for k, v in MODUL_ISIMLERI.items()}
        modul_label = st.selectbox(
            "Modul",
            options=list(modul_secenekleri.keys()),
            key="gorev_modul_sec",
        )
        modul_key = modul_secenekleri.get(modul_label, "matematik")

        aktiviteler = _POPULER_AKTIVITELER.get(modul_key, [])
        aktivite_isimleri = [a["ad"] for a in aktiviteler]
        secilen_aktivite = st.selectbox(
            "Aktivite",
            options=aktivite_isimleri,
            key="gorev_aktivite_sec",
        )
        aktivite_turu = ""
        for a in aktiviteler:
            if a["ad"] == secilen_aktivite:
                aktivite_turu = a["tur"]
                break

    with col2:
        sinif = st.number_input(
            "Sinif",
            min_value=1,
            max_value=12,
            value=5,
            step=1,
            key="gorev_sinif_input",
        )
        sube = st.text_input("Sube", value="A", key="gorev_sube_input")

    baslik = st.text_input(
        "Gorev Basligi",
        value=secilen_aktivite or "",
        key="gorev_baslik_input",
    )
    aciklama = st.text_area(
        "Aciklama",
        value="",
        height=80,
        key="gorev_aciklama_input",
    )

    col3, col4, col5 = st.columns(3)
    with col3:
        son_tarih = st.date_input(
            "Son Tarih",
            value=date.today() + timedelta(days=7),
            key="gorev_son_tarih_input",
        )
    with col4:
        min_sure = st.number_input(
            "Min. Sure (dk)",
            min_value=0,
            max_value=300,
            value=15,
            step=5,
            key="gorev_min_sure_input",
        )
    with col5:
        min_puan = st.number_input(
            "Min. Puan",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=5.0,
            key="gorev_min_puan_input",
        )

    tekrar = st.number_input(
        "Tekrar Sayisi",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
        key="gorev_tekrar_input",
    )

    # Ogretmen bilgisi — session'dan
    ogretmen_id = st.session_state.get("user_id", "ogretmen_01")
    ogretmen_adi = st.session_state.get("user_name", "Ogretmen")

    if st.button("Gorev Olustur", key="btn_gorev_olustur", type="primary"):
        if not baslik.strip():
            st.error("Gorev basligi bos olamaz.")
            return

        store = get_modul_ortak_store()
        ogrenciler = _get_sinif_ogrencileri(int(sinif), sube.strip())

        gorev = ModulGorev(
            ogretmen_id=ogretmen_id,
            ogretmen_adi=ogretmen_adi,
            modul=modul_key,
            aktivite_turu=aktivite_turu,
            aktivite_adi=secilen_aktivite or "",
            baslik=baslik.strip(),
            aciklama=aciklama.strip(),
            sinif=int(sinif),
            sube=sube.strip(),
            son_tarih=son_tarih.isoformat(),
            min_sure_dk=int(min_sure),
            min_puan=float(min_puan),
            tekrar_sayisi=int(tekrar),
            hedef_ogrenciler=[_get_student_id(s) for s in ogrenciler],
        )
        store.add_gorev(gorev)

        # Her ogrenci icin tamamlama kaydi olustur
        for s in ogrenciler:
            tam = GorevTamamlama(
                gorev_id=gorev.id,
                student_id=_get_student_id(s),
                student_name=_get_student_name(s),
            )
            store.add_tamamlama(tam)

        st.success(
            f"Gorev olusturuldu: {baslik} — "
            f"{len(ogrenciler)} ogrenciye atandi."
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — GOREV TAKIBI
# ══════════════════════════════════════════════════════════════════════════════

def _render_gorev_takibi():
    """Gorev listesi ve ogrenci bazli tamamlama durumu."""
    styled_section("Gorev Takibi", color="#10b981")

    store = get_modul_ortak_store()

    col1, col2 = st.columns(2)
    with col1:
        modul_filtre_opts = ["Tumu"] + list(MODUL_ISIMLERI.values())
        modul_filtre = st.selectbox(
            "Modul Filtresi",
            options=modul_filtre_opts,
            key="takip_modul_filtre",
        )
    with col2:
        sinif_filtre = st.number_input(
            "Sinif Filtresi (0=Tumu)",
            min_value=0,
            max_value=12,
            value=0,
            step=1,
            key="takip_sinif_filtre",
        )

    # Modul key cevir
    modul_key_filtre = None
    if modul_filtre != "Tumu":
        for k, v in MODUL_ISIMLERI.items():
            if v == modul_filtre:
                modul_key_filtre = k
                break

    sinif_val = int(sinif_filtre) if sinif_filtre else None
    if sinif_val == 0:
        sinif_val = None

    gorevler = store.get_gorevler(modul=modul_key_filtre, sinif=sinif_val)
    gorevler.sort(key=lambda g: g.get("created_at", ""), reverse=True)

    if not gorevler:
        styled_info_banner("Filtreye uygun gorev bulunamadi.", banner_type="info")
        return

    for idx, g in enumerate(gorevler):
        modul_adi = MODUL_ISIMLERI.get(g.get("modul", ""), g.get("modul", ""))
        baslik = g.get("baslik", "Gorev")
        sinif_str = f"{g.get('sinif', '')}/{g.get('sube', '')}"
        son_tarih = g.get("son_tarih", "")
        durum = g.get("durum", "aktif")

        with st.expander(f"{baslik} — {modul_adi} — Sinif {sinif_str} — Son: {son_tarih}", expanded=False):
            st.markdown(
                f"**Ogretmen:** {g.get('ogretmen_adi', '')} | "
                f"**Aktivite:** {g.get('aktivite_adi', '')} | "
                f"**Min Sure:** {g.get('min_sure_dk', 0)} dk | "
                f"**Min Puan:** {g.get('min_puan', 0)} | "
                f"**Tekrar:** {g.get('tekrar_sayisi', 1)}"
            )
            if g.get("aciklama"):
                st.markdown(f"*{g['aciklama']}*")

            # Ogrenci tamamlama tablosu
            tamamlamalar = store.get_tamamlamalar(gorev_id=g["id"])
            if tamamlamalar:
                # Son tarih kontrolu
                bugun = date.today().isoformat()
                rows_html = ""
                for t in tamamlamalar:
                    t_durum = t.get("durum", "bekliyor")
                    if t_durum == "bekliyor" and son_tarih and bugun > son_tarih:
                        t_durum = "gecikti"
                    badge = _durum_badge(t_durum)
                    rows_html += (
                        f"<tr>"
                        f"<td style='padding:8px;border-bottom:1px solid #1e293b'>"
                        f"{t.get('student_name', '')}</td>"
                        f"<td style='padding:8px;border-bottom:1px solid #1e293b;text-align:center'>"
                        f"{t.get('tamamlama_sayisi', 0)}/{g.get('tekrar_sayisi', 1)}</td>"
                        f"<td style='padding:8px;border-bottom:1px solid #1e293b;text-align:center'>"
                        f"{t.get('toplam_sure_dk', 0)} dk</td>"
                        f"<td style='padding:8px;border-bottom:1px solid #1e293b;text-align:center'>"
                        f"{t.get('ortalama_puan', 0)}</td>"
                        f"<td style='padding:8px;border-bottom:1px solid #1e293b;text-align:center'>"
                        f"{badge}</td>"
                        f"</tr>"
                    )

                table_html = f"""
                <div style="background:#0f172a;border-radius:10px;padding:12px;margin-top:8px;
                    border:1px solid #1e293b">
                <table style="width:100%;border-collapse:collapse;color:#e2e8f0;font-size:0.85rem">
                <thead>
                <tr style="border-bottom:2px solid #334155">
                    <th style="padding:8px;text-align:left;color:#94a3b8">Ogrenci</th>
                    <th style="padding:8px;text-align:center;color:#94a3b8">Tamamlama</th>
                    <th style="padding:8px;text-align:center;color:#94a3b8">Sure</th>
                    <th style="padding:8px;text-align:center;color:#94a3b8">Ort. Puan</th>
                    <th style="padding:8px;text-align:center;color:#94a3b8">Durum</th>
                </tr>
                </thead>
                <tbody>{rows_html}</tbody>
                </table>
                </div>
                """
                _render_html(table_html)

                # Istatistik ozet
                toplam = len(tamamlamalar)
                tamamlanan = sum(
                    1 for t in tamamlamalar if t.get("durum") == "tamamlandi"
                )
                _render_html(
                    f"<div style='margin-top:8px;color:#94a3b8;font-size:0.8rem'>"
                    f"Toplam: {toplam} ogrenci | Tamamlayan: {tamamlanan} | "
                    f"Oran: %{round(tamamlanan / toplam * 100) if toplam else 0}"
                    f"</div>"
                )
            else:
                st.info("Henuz tamamlama kaydi yok.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TOPLU ATAMA
# ══════════════════════════════════════════════════════════════════════════════

def _render_toplu_atama():
    """Hizli toplu gorev atama."""
    styled_section("Toplu Gorev Atama", color="#f59e0b")

    col1, col2 = st.columns(2)
    with col1:
        sinif_toplu = st.number_input(
            "Sinif",
            min_value=1,
            max_value=12,
            value=5,
            step=1,
            key="toplu_sinif_input",
        )
        sube_toplu = st.text_input("Sube", value="A", key="toplu_sube_input")
    with col2:
        son_tarih_toplu = st.date_input(
            "Son Tarih",
            value=date.today() + timedelta(days=7),
            key="toplu_son_tarih_input",
        )
        tekrar_toplu = st.number_input(
            "Tekrar Sayisi",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key="toplu_tekrar_input",
        )

    styled_section("Hizli Aktivite Secimi", color="#8b5cf6")

    secilen_gorevler: list[dict] = []

    for mod_key, mod_adi in MODUL_ISIMLERI.items():
        st.markdown(f"**{mod_adi}**")
        aktiviteler = _POPULER_AKTIVITELER.get(mod_key, [])
        cols = st.columns(min(len(aktiviteler), 4)) if aktiviteler else []
        for i, akt in enumerate(aktiviteler):
            col_idx = i % (len(cols) if cols else 1)
            with cols[col_idx] if cols else st.container():
                checked = st.checkbox(
                    akt["ad"],
                    key=f"toplu_chk_{mod_key}_{i}",
                )
                if checked:
                    secilen_gorevler.append({
                        "modul": mod_key,
                        "aktivite_adi": akt["ad"],
                        "aktivite_turu": akt["tur"],
                    })

    if secilen_gorevler:
        _render_html(
            f"<div style='background:#1e293b;padding:10px 16px;border-radius:8px;"
            f"color:#e2e8f0;margin:12px 0;font-size:0.9rem'>"
            f"Secilen gorev sayisi: <b>{len(secilen_gorevler)}</b></div>"
        )

    ogretmen_id = st.session_state.get("user_id", "ogretmen_01")
    ogretmen_adi = st.session_state.get("user_name", "Ogretmen")

    if st.button("Toplu Gorev Olustur", key="btn_toplu_olustur", type="primary"):
        if not secilen_gorevler:
            st.error("En az bir aktivite seciniz.")
            return

        store = get_modul_ortak_store()
        ogrenciler = _get_sinif_ogrencileri(int(sinif_toplu), sube_toplu.strip())
        olusturulan = 0

        for sg in secilen_gorevler:
            gorev = ModulGorev(
                ogretmen_id=ogretmen_id,
                ogretmen_adi=ogretmen_adi,
                modul=sg["modul"],
                aktivite_turu=sg["aktivite_turu"],
                aktivite_adi=sg["aktivite_adi"],
                baslik=sg["aktivite_adi"],
                aciklama="Toplu atama ile olusturuldu.",
                sinif=int(sinif_toplu),
                sube=sube_toplu.strip(),
                son_tarih=son_tarih_toplu.isoformat(),
                min_sure_dk=10,
                min_puan=50.0,
                tekrar_sayisi=int(tekrar_toplu),
                hedef_ogrenciler=[_get_student_id(s) for s in ogrenciler],
            )
            store.add_gorev(gorev)

            for s in ogrenciler:
                tam = GorevTamamlama(
                    gorev_id=gorev.id,
                    student_id=_get_student_id(s),
                    student_name=_get_student_name(s),
                )
                store.add_tamamlama(tam)
            olusturulan += 1

        st.success(
            f"{olusturulan} gorev olusturuldu, "
            f"{len(ogrenciler)} ogrenciye atandi."
        )


# ══════════════════════════════════════════════════════════════════════════════
# VELİ MODUL RAPORU
# ══════════════════════════════════════════════════════════════════════════════

def render_veli_modul_raporu(student_id: str, student_name: str):
    """Veli paneline entegre edilecek modul raporu."""
    styled_header(
        f"{student_name} — Modul Ilerleme Raporu",
        "Haftalik ozet, guclu/zayif alanlar ve son aktiviteler",
    )

    store = get_modul_ortak_store()
    rapor = store.veli_raporu(student_id)

    # ── Haftalik Ozet ────────────────────────────────────────────────────
    styled_section("Haftalik Ozet", color="#6366F1")

    haftalik = rapor.get("haftalik_ozet", {})
    modul_ozet = haftalik.get("modul_ozet", {})

    if not modul_ozet:
        styled_info_banner("Bu hafta henuz aktivite kaydi yok.", banner_type="info")
    else:
        # Toplam sure karti
        toplam_sure = haftalik.get("toplam_sure_dk", 0)
        _render_html(
            f"<div style='background:linear-gradient(135deg,#131825,#1a2035);"
            f"border-radius:12px;padding:16px 20px;margin-bottom:16px;"
            f"border:1px solid #1e293b;text-align:center'>"
            f"<div style='font-size:2rem;font-weight:800;color:#e2e8f0'>"
            f"{toplam_sure} dk</div>"
            f"<div style='font-size:0.85rem;color:#94a3b8;margin-top:4px'>"
            f"Bu Hafta Toplam Calisma Suresi</div></div>"
        )

        # Modul bazli kartlar
        mod_renkleri = {"matematik": "#6366F1", "sanat": "#ec4899", "bilisim": "#10b981"}
        cards_html = '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">'

        for mod_key, mod_data in modul_ozet.items():
            renk = mod_renkleri.get(mod_key, "#6366F1")
            mod_adi = MODUL_ISIMLERI.get(mod_key, mod_key)
            cards_html += (
                f"<div style='flex:1;min-width:200px;background:#0f172a;"
                f"border-radius:10px;padding:16px;border-left:4px solid {renk};"
                f"border:1px solid #1e293b'>"
                f"<div style='font-weight:700;color:#e2e8f0;margin-bottom:8px'>"
                f"{mod_adi}</div>"
                f"<div style='color:#94a3b8;font-size:0.85rem'>"
                f"Aktivite: <b style=\"color:#e2e8f0\">{mod_data.get('aktivite_sayisi', 0)}</b><br>"
                f"Sure: <b style=\"color:#e2e8f0\">{mod_data.get('sure_dk', 0)} dk</b><br>"
                f"Ort. Puan: <b style=\"color:{renk}\">{mod_data.get('ort_puan', 0)}</b>"
                f"</div></div>"
            )
        cards_html += "</div>"
        _render_html(cards_html)

    # ── Guclu / Zayif Analiz ─────────────────────────────────────────────
    styled_section("Guclu ve Gelistirilecek Alanlar", color="#10b981")

    analiz = rapor.get("guclu_zayif", {})
    guclu = analiz.get("guclu", [])
    calisma = analiz.get("calisma_gereken", [])
    oneri = analiz.get("oneri", "")

    if not guclu and not calisma:
        styled_info_banner(
            "Henuz yeterli aktivite verisi yok. Analizler aktivite sayisi arttikca detaylanacaktir.",
            banner_type="info",
        )
    else:
        items_html = ""
        if guclu:
            items_html += "<div style='margin-bottom:12px'>"
            items_html += "<div style='color:#94a3b8;font-size:0.8rem;margin-bottom:6px;font-weight:600'>GUCLU ALANLAR</div>"
            for g in guclu:
                items_html += (
                    f"<div style='background:#0f2a1a;border:1px solid #166534;"
                    f"border-radius:8px;padding:8px 14px;margin-bottom:6px;"
                    f"display:flex;justify-content:space-between;align-items:center'>"
                    f"<span style='color:#4ade80;font-weight:600'>{g['kategori']}</span>"
                    f"<span style='color:#86efac'>%{g['ortalama']} "
                    f"({g['aktivite_sayisi']} aktivite)</span></div>"
                )
            items_html += "</div>"

        if calisma:
            items_html += "<div style='margin-bottom:12px'>"
            items_html += "<div style='color:#94a3b8;font-size:0.8rem;margin-bottom:6px;font-weight:600'>GELISTIRILECEK ALANLAR</div>"
            for c in calisma:
                items_html += (
                    f"<div style='background:#2a1a0f;border:1px solid #9a3412;"
                    f"border-radius:8px;padding:8px 14px;margin-bottom:6px;"
                    f"display:flex;justify-content:space-between;align-items:center'>"
                    f"<span style='color:#fb923c;font-weight:600'>{c['kategori']}</span>"
                    f"<span style='color:#fdba74'>%{c['ortalama']} "
                    f"({c['aktivite_sayisi']} aktivite)</span></div>"
                )
            items_html += "</div>"

        if oneri:
            items_html += (
                f"<div style='background:#1e293b;border-radius:8px;padding:10px 14px;"
                f"color:#94a3b8;font-size:0.85rem;font-style:italic'>"
                f"{oneri}</div>"
            )

        _render_html(items_html)

    # ── Son Aktiviteler ──────────────────────────────────────────────────
    styled_section("Son Aktiviteler", color="#8b5cf6")

    son_akt = rapor.get("son_aktiviteler", [])
    if not son_akt:
        styled_info_banner("Henuz aktivite kaydi yok.", banner_type="info")
    else:
        rows_html = ""
        for a in son_akt:
            mod_adi = MODUL_ISIMLERI.get(a.get("modul", ""), a.get("modul", ""))
            puan = a.get("puan", 0)
            puan_renk = "#10b981" if puan >= GUCLU_ESIK else ("#f59e0b" if puan >= ZAYIF_ESIK else "#ef4444")
            rows_html += (
                f"<tr>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #1e293b;color:#94a3b8;"
                f"font-size:0.8rem'>{a.get('tarih', '')}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #1e293b;color:#e2e8f0'>"
                f"{mod_adi}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #1e293b;color:#e2e8f0'>"
                f"{a.get('aktivite_adi', '')}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #1e293b;color:#e2e8f0;"
                f"text-align:center'>{a.get('sure_dk', 0)} dk</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #1e293b;"
                f"text-align:center;color:{puan_renk};font-weight:700'>{puan}</td>"
                f"</tr>"
            )

        _render_html(
            f"<div style='background:#0f172a;border-radius:10px;padding:12px;"
            f"border:1px solid #1e293b;margin-top:8px'>"
            f"<table style='width:100%;border-collapse:collapse;font-size:0.85rem'>"
            f"<thead><tr style='border-bottom:2px solid #334155'>"
            f"<th style='padding:8px 10px;text-align:left;color:#94a3b8'>Tarih</th>"
            f"<th style='padding:8px 10px;text-align:left;color:#94a3b8'>Modul</th>"
            f"<th style='padding:8px 10px;text-align:left;color:#94a3b8'>Aktivite</th>"
            f"<th style='padding:8px 10px;text-align:center;color:#94a3b8'>Sure</th>"
            f"<th style='padding:8px 10px;text-align:center;color:#94a3b8'>Puan</th>"
            f"</tr></thead>"
            f"<tbody>{rows_html}</tbody></table></div>"
        )

    # ── PDF Indirme ──────────────────────────────────────────────────────
    styled_section("Rapor Indir", color="#3b82f6")

    pdf_text = _build_text_report(student_name, rapor)
    st.download_button(
        label="Raporu Indir (TXT)",
        data=pdf_text.encode("utf-8"),
        file_name=f"modul_rapor_{student_id}_{date.today().isoformat()}.txt",
        mime="text/plain",
        key=f"btn_rapor_indir_{student_id}",
    )


def _build_text_report(student_name: str, rapor: dict) -> str:
    """Veli raporu icin duz metin olusturur."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"  MODUL ILERLEME RAPORU — {student_name}")
    lines.append(f"  Tarih: {date.today().isoformat()}")
    lines.append("=" * 60)
    lines.append("")

    # Haftalik ozet
    haftalik = rapor.get("haftalik_ozet", {})
    lines.append("HAFTALIK OZET")
    lines.append("-" * 40)
    lines.append(f"Hafta: {haftalik.get('hafta_baslangic', '')} — {haftalik.get('hafta_bitis', '')}")
    lines.append(f"Toplam Sure: {haftalik.get('toplam_sure_dk', 0)} dakika")
    modul_ozet = haftalik.get("modul_ozet", {})
    for mk, mv in modul_ozet.items():
        mod_adi = MODUL_ISIMLERI.get(mk, mk)
        lines.append(
            f"  {mod_adi}: {mv.get('aktivite_sayisi', 0)} aktivite, "
            f"{mv.get('sure_dk', 0)} dk, ort. {mv.get('ort_puan', 0)} puan"
        )
    lines.append("")

    # Guclu / zayif
    analiz = rapor.get("guclu_zayif", {})
    lines.append("GUCLU ALANLAR")
    lines.append("-" * 40)
    for g in analiz.get("guclu", []):
        lines.append(f"  {g['kategori']}: %{g['ortalama']} ({g['aktivite_sayisi']} aktivite)")
    if not analiz.get("guclu"):
        lines.append("  Henuz veri yok.")
    lines.append("")

    lines.append("GELISTIRILECEK ALANLAR")
    lines.append("-" * 40)
    for c in analiz.get("calisma_gereken", []):
        lines.append(f"  {c['kategori']}: %{c['ortalama']} ({c['aktivite_sayisi']} aktivite)")
    if not analiz.get("calisma_gereken"):
        lines.append("  Henuz veri yok.")
    lines.append("")

    oneri = analiz.get("oneri", "")
    if oneri:
        lines.append(f"ONERI: {oneri}")
        lines.append("")

    # Son aktiviteler
    lines.append("SON AKTIVITELER")
    lines.append("-" * 40)
    for a in rapor.get("son_aktiviteler", []):
        mod_adi = MODUL_ISIMLERI.get(a.get("modul", ""), a.get("modul", ""))
        lines.append(
            f"  {a.get('tarih', '')} | {mod_adi} | "
            f"{a.get('aktivite_adi', '')} | {a.get('sure_dk', 0)} dk | "
            f"Puan: {a.get('puan', 0)}"
        )
    if not rapor.get("son_aktiviteler"):
        lines.append("  Henuz aktivite yok.")

    lines.append("")
    lines.append("=" * 60)
    lines.append("SmartCampusAI — Egitim Modulleri Raporu")
    lines.append("=" * 60)

    return "\n".join(lines)
