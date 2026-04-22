"""
Akademik Takvim — Tamamlayici Ozellikler
==========================================
1. Toplu Faaliyet Yukleme (Excel/CSV)
2. MEB Zorunlu Takvim Sablonu
3. Faaliyet Durumu Takibi
4. Yillik Karsilastirma
5. Takvim Paylasim (Veli/Ogretmen PDF)
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import date, datetime

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

_AY = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
       7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}


def _save(data):
    try:
        from views.academic_calendar import save_calendar_data
        save_calendar_data(data)
    except Exception:
        pass


# ============================================================
# 1. TOPLU FAALİYET YÜKLEME
# ============================================================

def render_toplu_yukleme(data: dict):
    """Excel/CSV ile toplu faaliyet yukleme."""
    styled_section("Toplu Faaliyet Yukleme", "#2563eb")
    styled_info_banner(
        "Excel veya CSV dosyasindan toplu faaliyet yukleyin. "
        "Sablon indirip doldurun, sonra yukleyin.",
        banner_type="info", icon="📤")

    sub = st.tabs(["📥 Sablon Indir", "📤 Dosya Yukle"])

    with sub[0]:
        styled_section("Excel Sablon")
        st.markdown("""
        **CSV Sablon Formati:**
        ```
        baslik,tur,tarih,bitis_tarihi,kademe,konum,aciklama
        1. Donem Baslangic,1. Donem Baslangic,2025-09-15,,Tum Kademeler,,Ders yili baslangici
        Matematik Yazili,Yazili Sinav,2025-10-20,,Ortaokul,Sinif,1. yazili sinav
        Sonbahar Gezisi,Gezi / Gozlem,2025-10-25,2025-10-25,Ilkokul,Belgrad Ormani,Doga gezisi
        ```
        """)
        # Sablon CSV olustur
        sablon = "baslik,tur,tarih,bitis_tarihi,kademe,konum,aciklama\n"
        sablon += "Ornek Sinav,Sinav,2025-10-15,,Ortaokul,Sinif,1. yazili\n"
        sablon += "Ornek Gezi,Gezi / Gozlem,2025-11-05,,Ilkokul,Muze,Sonbahar gezisi\n"
        st.download_button("📥 CSV Sablon Indir", sablon, file_name="takvim_sablon.csv",
                            mime="text/csv", use_container_width=True)

    with sub[1]:
        styled_section("Dosya Yukle")
        uploaded = st.file_uploader("CSV dosyasi secin", type=["csv"], key="akt_csv_upload")

        if uploaded:
            try:
                import csv
                import io
                content = uploaded.read().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)

                st.success(f"{len(rows)} faaliyet bulundu!")

                # Onizleme
                for r in rows[:5]:
                    st.markdown(f"- **{r.get('baslik', '?')}** — {r.get('tur', '')} — {r.get('tarih', '')}")
                if len(rows) > 5:
                    st.caption(f"... ve {len(rows) - 5} faaliyet daha")

                if st.button("Tumu Yukle", key="akt_csv_btn", type="primary", use_container_width=True):
                    eklenen = 0
                    for r in rows:
                        baslik = r.get("baslik", "").strip()
                        if not baslik:
                            continue
                        new_event = {
                            "id": f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{eklenen}",
                            "title": baslik,
                            "type": r.get("tur", "Genel Etkinlik"),
                            "date": r.get("tarih", ""),
                            "end_date": r.get("bitis_tarihi", "") or None,
                            "kademe": r.get("kademe", "Tum Kademeler"),
                            "location": r.get("konum", ""),
                            "description": r.get("aciklama", ""),
                            "durum": "Planli",
                            "created_at": datetime.now().isoformat(),
                        }
                        data.setdefault("events", []).append(new_event)
                        eklenen += 1
                    _save(data)
                    st.success(f"{eklenen} faaliyet yuklendi!")
                    st.rerun()
            except Exception as e:
                st.error(f"CSV okuma hatasi: {e}")


# ============================================================
# 2. MEB ZORUNLU TAKVİM ŞABLONU
# ============================================================

_MEB_2025_2026 = [
    {"baslik": "Akademik Yil Baslangic", "tur": "Akademik Yil Baslangic", "tarih": "2025-09-15", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "1. Donem Baslangic", "tur": "1. Donem Baslangic", "tarih": "2025-09-15", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "29 Ekim Cumhuriyet Bayrami", "tur": "Resmi Tatil", "tarih": "2025-10-29", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "10 Kasim Ataturk'u Anma", "tur": "Resmi Tatil", "tarih": "2025-11-10", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "Ogretmenler Gunu", "tur": "Kutlama / Anma / Toren", "tarih": "2025-11-24", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "1. Donem Bitis", "tur": "1. Donem Bitis", "tarih": "2026-01-23", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "Karne Gunu (1. Donem)", "tur": "Karne Gunu", "tarih": "2026-01-23", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "Yariyil Tatili", "tur": "Yariyil Tatili", "tarih": "2026-01-26", "bitis": "2026-02-06", "kademe": "Tum Kademeler"},
    {"baslik": "2. Donem Baslangic", "tur": "2. Donem Baslangic", "tarih": "2026-02-09", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "Ara Tatil (Nisan)", "tur": "Ara Tatil", "tarih": "2026-04-13", "bitis": "2026-04-17", "kademe": "Tum Kademeler"},
    {"baslik": "23 Nisan Ulusal Egemenlik", "tur": "Resmi Tatil", "tarih": "2026-04-23", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "1 Mayis Isci Bayrami", "tur": "Resmi Tatil", "tarih": "2026-05-01", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "19 Mayis Genclik Bayrami", "tur": "Resmi Tatil", "tarih": "2026-05-19", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "LGS Sinavi", "tur": "Deneme Sinavi (LGS/TYT/AYT)", "tarih": "2026-06-14", "bitis": None, "kademe": "Ortaokul"},
    {"baslik": "2. Donem Bitis", "tur": "2. Donem Bitis", "tarih": "2026-06-19", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "Karne Gunu (2. Donem)", "tur": "Karne Gunu", "tarih": "2026-06-19", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "Akademik Yil Bitis", "tur": "Akademik Yil Bitis", "tarih": "2026-06-19", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "15 Temmuz Demokrasi Bayrami", "tur": "Resmi Tatil", "tarih": "2026-07-15", "bitis": None, "kademe": "Tum Kademeler"},
    {"baslik": "30 Agustos Zafer Bayrami", "tur": "Resmi Tatil", "tarih": "2026-08-30", "bitis": None, "kademe": "Tum Kademeler"},
]


def render_meb_takvim(data: dict):
    """MEB resmi takvimini otomatik yukle."""
    styled_section("MEB Akademik Takvim Sablonu", "#dc2626")
    styled_info_banner(
        "2025-2026 egitim yili MEB resmi takvimini tek tikla yukleyin. "
        "Donem baslangic/bitis, resmi tatiller, karne gunleri, LGS tarihi.",
        banner_type="info", icon="🏛️")

    events = data.get("events", [])
    mevcut_basliklar = set(e.get("title", e.get("baslik", "")) for e in events)

    # Onizleme
    styled_section("MEB 2025-2026 Takvimi")
    yeni_sayisi = 0
    for m in _MEB_2025_2026:
        zaten_var = m["baslik"] in mevcut_basliklar
        durum = "✅ Zaten var" if zaten_var else "⬜ Eklenecek"
        durum_renk = "#10b981" if zaten_var else "#f59e0b"
        if not zaten_var:
            yeni_sayisi += 1
        bitis_txt = f" — {m['bitis']}" if m.get("bitis") else ""

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;padding:3px 0;border-bottom:1px solid #1e293b;">
            <span style="min-width:70px;font-size:10px;color:#94a3b8;">{m['tarih'][5:]}{bitis_txt}</span>
            <span style="flex:1;font-size:11px;color:#e2e8f0;font-weight:600;">{m['baslik']}</span>
            <span style="font-size:9px;color:{durum_renk};">{durum}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"**{yeni_sayisi} yeni faaliyet** eklenecek ({len(_MEB_2025_2026) - yeni_sayisi} zaten var)")

    if yeni_sayisi > 0:
        # Onay adimi — cift tiklama ve yanlislikla yuklemeyi onle
        onay_key = "meb_yukle_onay"
        if st.checkbox(f"{yeni_sayisi} MEB faaliyetini yuklemek istedigimi onayliyorum", key=onay_key):
            if st.button("MEB Takvimini Yukle", key="meb_yukle", type="primary", use_container_width=True):
                eklenen = 0
                for m in _MEB_2025_2026:
                    if m["baslik"] in mevcut_basliklar:
                        continue
                    new_event = {
                        "id": f"meb_{datetime.now().strftime('%Y%m%d%H%M%S')}_{eklenen}",
                        "title": m["baslik"], "type": m["tur"],
                        "date": m["tarih"], "end_date": m.get("bitis"),
                        "kademe": m["kademe"], "location": "", "description": "MEB resmi takvim",
                        "durum": "Planli", "created_at": datetime.now().isoformat(),
                    }
                    data.setdefault("events", []).append(new_event)
                    eklenen += 1
                _save(data)
                st.success(f"{eklenen} MEB faaliyeti yuklendi!")
                st.rerun()
    else:
        st.success("Tum MEB faaliyetleri zaten yuklu!")


# ============================================================
# 3. FAALİYET DURUMU TAKİBİ
# ============================================================

def render_durum_takip(data: dict, events: list):
    """Faaliyet gerceklesme durumu takibi."""
    styled_section("Faaliyet Durum Takibi", "#059669")
    styled_info_banner(
        "Planlanan faaliyetlerin gerceklesme durumunu izleyin. "
        "Planli → Gerceklesti / Ertelendi / Iptal",
        banner_type="info", icon="📋")

    bugun = date.today().isoformat()

    # Durum sayilari
    planli = sum(1 for e in events if e.get("durum", "Planli") == "Planli")
    gerceklesti = sum(1 for e in events if e.get("durum") == "Gerceklesti")
    ertelendi = sum(1 for e in events if e.get("durum") == "Ertelendi")
    iptal = sum(1 for e in events if e.get("durum") == "Iptal")
    gecmis_planli = sum(1 for e in events if e.get("durum", "Planli") == "Planli"
                          and (e.get("date", e.get("tarih", "")) or "")[:10] < bugun)

    toplam = len(events)
    gerceklesme = round(gerceklesti / max(toplam, 1) * 100)
    g_renk = "#10b981" if gerceklesme >= 70 else "#f59e0b" if gerceklesme >= 40 else "#ef4444"

    styled_stat_row([
        ("Toplam", str(toplam), "#059669", "📋"),
        ("Gerceklesti", str(gerceklesti), "#10b981", "✅"),
        ("Planli", str(planli), "#3b82f6", "📅"),
        ("Ertelendi", str(ertelendi), "#f59e0b", "🔄"),
        ("Iptal", str(iptal), "#ef4444", "❌"),
        ("Gerceklesme", f"%{gerceklesme}", g_renk, "📊"),
    ])

    # Gecmis ama hala planli
    if gecmis_planli > 0:
        styled_info_banner(
            f"{gecmis_planli} faaliyet tarihi gecmis ama durumu guncellenmemis! Asagidan guncelleyin.",
            banner_type="warning", icon="⚠️")

    # Durum guncelleme
    styled_section("Durum Guncelle")
    gecmis_events = [e for e in events if e.get("durum", "Planli") == "Planli"
                       and (e.get("date", e.get("tarih", "")) or "")[:10] < bugun]

    if not gecmis_events:
        st.success("Durum guncellenmesi gereken faaliyet yok!")
    else:
        degisiklik_var = False
        for e in gecmis_events[:20]:
            baslik = e.get("title", e.get("baslik", "?"))
            tarih = (e.get("date", e.get("tarih", "")) or "")[:10]
            eid = e.get("id", "")
            mevcut = e.get("durum", "Planli")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{baslik}** ({tarih})")
            with col2:
                secenekler = ["Planli", "Gerceklesti", "Ertelendi", "Iptal"]
                yeni_durum = st.selectbox("Durum", secenekler,
                                           index=secenekler.index(mevcut) if mevcut in secenekler else 0,
                                           key=f"ds_{eid}")
                if yeni_durum != mevcut:
                    e["durum"] = yeni_durum
                    e["durum_guncelleme"] = datetime.now().isoformat()
                    degisiklik_var = True

        if degisiklik_var:
            styled_info_banner("Kaydedilmemis degisiklikler var! Asagidaki butona basmayi unutmayin.",
                               banner_type="warning", icon="⚠️")

        if st.button("Durumlari Kaydet", key="ds_kaydet", type="primary", use_container_width=True):
            _save(data)
            st.success("Durumlar guncellendi!")
            st.rerun()


# ============================================================
# 4. YILLIK KARŞILAŞTIRMA
# ============================================================

def render_yil_karsilastir(events: list):
    """Bu yil vs gecen yil faaliyet karsilastirmasi."""
    styled_section("Yillik Karsilastirma", "#7c3aed")
    styled_info_banner(
        "Bu egitim yili ile gecen yilin faaliyet sayilarini, "
        "tur dagilimini ve gerceklesme oranlarini karsilastirin.",
        banner_type="info", icon="📊")

    bugun = date.today()
    if bugun.month >= 9:
        bu_yil_bas = f"{bugun.year}-09-01"
        bu_yil_bit = f"{bugun.year + 1}-08-31"
        gecen_yil_bas = f"{bugun.year - 1}-09-01"
        gecen_yil_bit = f"{bugun.year}-08-31"
        bu_yil_label = f"{bugun.year}-{bugun.year + 1}"
        gecen_yil_label = f"{bugun.year - 1}-{bugun.year}"
    else:
        bu_yil_bas = f"{bugun.year - 1}-09-01"
        bu_yil_bit = f"{bugun.year}-08-31"
        gecen_yil_bas = f"{bugun.year - 2}-09-01"
        gecen_yil_bit = f"{bugun.year - 1}-08-31"
        bu_yil_label = f"{bugun.year - 1}-{bugun.year}"
        gecen_yil_label = f"{bugun.year - 2}-{bugun.year - 1}"

    bu_yil = [e for e in events if bu_yil_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= bu_yil_bit]
    gecen_yil = [e for e in events if gecen_yil_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= gecen_yil_bit]

    bu_gercek = sum(1 for e in bu_yil if e.get("durum") == "Gerceklesti")
    gc_gercek = sum(1 for e in gecen_yil if e.get("durum") == "Gerceklesti")

    def _deg(bu, gc):
        if gc == 0:
            return "+∞" if bu > 0 else "—"
        f = round((bu - gc) / gc * 100, 1)
        return f"+{f}%" if f >= 0 else f"{f}%"

    col1, col2, col3 = st.columns([1, 0.2, 1])
    with col1:
        st.markdown(f'<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:16px;">{bu_yil_label}</div>', unsafe_allow_html=True)
        styled_stat_row([
            ("Faaliyet", str(len(bu_yil)), "#3b82f6", "📋"),
            ("Gerceklesen", str(bu_gercek), "#10b981", "✅"),
        ])
    with col2:
        st.markdown('<div style="text-align:center;font-size:28px;padding-top:20px;">⚖️</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:16px;">{gecen_yil_label}</div>', unsafe_allow_html=True)
        styled_stat_row([
            ("Faaliyet", str(len(gecen_yil)), "#64748b", "📋"),
            ("Gerceklesen", str(gc_gercek), "#64748b", "✅"),
        ])

    # Fark
    styled_section("Degisim")
    metrikler = [
        ("Toplam Faaliyet", len(bu_yil), len(gecen_yil)),
        ("Gerceklesen", bu_gercek, gc_gercek),
    ]
    for label, bu_val, gc_val in metrikler:
        deg = _deg(bu_val, gc_val)
        renk = "#10b981" if bu_val >= gc_val else "#ef4444"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
            <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">{label}</span>
            <span style="font-size:14px;font-weight:800;color:#3b82f6;">{bu_val}</span>
            <span style="color:#64748b;">vs</span>
            <span style="font-size:14px;font-weight:800;color:#94a3b8;">{gc_val}</span>
            <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
                        font-size:11px;font-weight:700;">{deg}</span>
        </div>""", unsafe_allow_html=True)

    # Tur bazli karsilastirma
    styled_section("Tur Bazli Karsilastirma")
    bu_tur = Counter(e.get("type", e.get("tur", "Diger")) for e in bu_yil)
    gc_tur = Counter(e.get("type", e.get("tur", "Diger")) for e in gecen_yil)
    tum_tur = sorted(set(list(bu_tur.keys()) + list(gc_tur.keys())))

    for tur in tum_tur[:15]:
        bu = bu_tur.get(tur, 0)
        gc = gc_tur.get(tur, 0)
        deg = _deg(bu, gc)
        renk = "#10b981" if bu >= gc else "#ef4444"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:6px;padding:2px 0;font-size:11px;">
            <span style="min-width:150px;color:#e2e8f0;">{tur}</span>
            <span style="min-width:25px;color:#3b82f6;font-weight:700;text-align:right;">{bu}</span>
            <span style="color:#64748b;">vs</span>
            <span style="min-width:25px;color:#94a3b8;font-weight:700;">{gc}</span>
            <span style="color:{renk};font-weight:700;font-size:10px;">{deg}</span>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 5. TAKVİM PAYLAŞIM (VELİ/ÖĞRETMEN PDF)
# ============================================================

def render_takvim_paylas(data: dict, events: list):
    """Kademe bazli filtrelenmis takvim PDF — velilere/ogretmenlere gonderilecek."""
    styled_section("Takvim Paylasim", "#0891b2")
    styled_info_banner(
        "Kademe bazli filtrelenmis takvim olusturun. "
        "Velilere veya ogretmenlere gonderilecek formatta PDF.",
        banner_type="info", icon="🎓")

    bugun = date.today()
    if bugun.month >= 9:
        yb = bugun.year
    else:
        yb = bugun.year - 1
    ey = f"{yb}-{yb + 1}"
    ey_bas = f"{yb}-09-01"
    ey_bit = f"{yb + 1}-08-31"

    yil_events = [e for e in events if ey_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= ey_bit]

    col1, col2 = st.columns(2)
    with col1:
        hedef = st.selectbox("Hedef Kitle", ["Veliler", "Ogretmenler"], key="tp_hedef")
    with col2:
        kademe = st.selectbox("Kademe", ["Tum Kademeler", "Anaokulu", "Ilkokul", "Ortaokul", "Lise"], key="tp_kademe")

    # Filtrele
    if kademe != "Tum Kademeler":
        filtered = [e for e in yil_events if e.get("kademe", "Tum Kademeler") in (kademe, "Tum Kademeler")]
    else:
        filtered = yil_events

    # Ogretmen icin sadece toplanti/sinav/kurul
    if hedef == "Ogretmenler":
        ogretmen_turler = {"Toplanti", "Ogretmenler Kurulu", "Zumre Toplantisi", "Kurul/Komisyon",
                            "Sinav", "Yazili Sinav", "Sozlu Sinav", "KYT (Kazanim Olcme)",
                            "Ogretmen Egitimi / Seminer", "Mesleki Calisma", "Personel Gelisim",
                            "1. Donem Baslangic", "1. Donem Bitis", "2. Donem Baslangic", "2. Donem Bitis",
                            "Karne Gunu", "Resmi Tatil", "Yariyil Tatili", "Ara Tatil"}
        filtered = [e for e in filtered if e.get("type", e.get("tur", "")) in ogretmen_turler]

    st.caption(f"{len(filtered)} faaliyet ({hedef} — {kademe})")

    # Onizleme
    if filtered:
        for e in sorted(filtered, key=lambda x: x.get("date", x.get("tarih", "")))[:10]:
            tarih = (e.get("date", e.get("tarih", "")) or "")[:10]
            st.markdown(f"- {tarih} — **{e.get('title', e.get('baslik', ''))}** ({e.get('type', e.get('tur', ''))})")
        if len(filtered) > 10:
            st.caption(f"... ve {len(filtered) - 10} faaliyet daha")

    # PDF
    if st.button(f"{hedef} Takvim PDF Indir", key="tp_pdf_btn", type="primary", use_container_width=True):
        try:
            from views._akt_yillik_plan import _generate_yillik_plan_pdf
            pdf = _generate_yillik_plan_pdf(filtered, ey, yb, yb + 1, data.get("semesters", []), None)
            if pdf:
                st.download_button(f"📥 {hedef} — {kademe} PDF Indir", pdf,
                                   file_name=f"takvim_{hedef.lower()}_{kademe.lower()}_{ey}.pdf",
                                   mime="application/pdf", use_container_width=True, key="tp_pdf_dl")
        except Exception as _e:
            st.error(f"PDF hatasi: {_e}")
