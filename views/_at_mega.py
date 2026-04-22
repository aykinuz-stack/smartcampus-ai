"""
Akademik Takip — MEGA Ozellikleri
====================================
1. Mufredat GPS (Curriculum Navigation)
2. Sinif Dijital Ikiz (Class Digital Twin)
3. Akademik Zaman Makinesi + Donem Karsilastirma
"""
from __future__ import annotations

import os
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


# ============================================================
# 1. MÜFREDAT GPS
# ============================================================

def render_mufredat_gps(store):
    """Ders bazli mufredat ilerleme haritasi."""
    styled_section("Mufredat GPS", "#059669")
    styled_info_banner(
        "Her dersin mufredat ilerlemesini gercek zamanli izleyin. "
        "Kalan kazanimlar, tahmini bitis, geride kalan dersler.",
        banner_type="info", icon="🗺️")

    ak = _ak_dir()

    # Kazanim isleme verileri
    try:
        import json
        kazanim_isleme = json.load(open(os.path.join(ak, "kazanim_isleme.json"), encoding="utf-8")) if os.path.exists(os.path.join(ak, "kazanim_isleme.json")) else []
    except Exception:
        kazanim_isleme = []

    # Yillik plan (toplam kazanim sayisi)
    try:
        import json
        yillik_plan = json.load(open(os.path.join("data", "olcme", "annual_plans.json"), encoding="utf-8")) if os.path.exists(os.path.join("data", "olcme", "annual_plans.json")) else []
    except Exception:
        yillik_plan = []

    if not kazanim_isleme and not yillik_plan:
        styled_info_banner("Kazanim veya yillik plan verisi bulunamadi.", banner_type="warning", icon="📋")
        return

    # Ders bazli gruplama
    ders_ilerleme = {}

    # Yillik plandan toplam kazanim
    for p in yillik_plan:
        ders = p.get("subject", p.get("ders", ""))
        sinif = p.get("grade", p.get("sinif", ""))
        kaz_list = p.get("learning_outcomes", [])
        key = f"{sinif}. Sinif — {ders}"
        if key not in ders_ilerleme:
            ders_ilerleme[key] = {"toplam": 0, "islenen": 0, "ders": ders, "sinif": sinif}
        ders_ilerleme[key]["toplam"] += len(kaz_list)

    # Islenen kazanimlar
    for k in kazanim_isleme:
        ders = k.get("ders", "")
        sinif = k.get("sinif", "")
        durum = k.get("durum", k.get("islendi", ""))
        key = f"{sinif}. Sinif — {ders}"
        if key in ders_ilerleme:
            if durum in ("islendi", True, "tamamlandi"):
                ders_ilerleme[key]["islenen"] += 1
        else:
            ders_ilerleme[key] = {"toplam": 1, "islenen": 1 if durum in ("islendi", True) else 0, "ders": ders, "sinif": sinif}

    if not ders_ilerleme:
        styled_info_banner("Ders bazli ilerleme verisi yok.", banner_type="info", icon="📊")
        return

    # Ozet
    toplam_kaz = sum(d["toplam"] for d in ders_ilerleme.values())
    islenen_kaz = sum(d["islenen"] for d in ders_ilerleme.values())
    genel_pct = round(islenen_kaz / max(toplam_kaz, 1) * 100)
    kalan = toplam_kaz - islenen_kaz

    bugun = date.today()
    yil_basi = date(bugun.year if bugun.month >= 9 else bugun.year - 1, 9, 1)
    gecen_gun = max((bugun - yil_basi).days, 1)
    kalan_gun = max(180 - gecen_gun, 0)
    gunluk_hiz = round(islenen_kaz / gecen_gun, 1) if gecen_gun > 0 else 0
    tahmini_bitis = round(kalan / gunluk_hiz) if gunluk_hiz > 0 else 999

    g_renk = "#10b981" if genel_pct >= 70 else "#f59e0b" if genel_pct >= 45 else "#ef4444"

    styled_stat_row([
        ("Toplam Kazanim", str(toplam_kaz), "#059669", "📋"),
        ("Islenen", str(islenen_kaz), "#10b981", "✅"),
        ("Kalan", str(kalan), "#f59e0b", "⏳"),
        ("Ilerleme", f"%{genel_pct}", g_renk, "📊"),
    ])

    # Hero
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#052e16 0%,#065f46 100%);
                border:2px solid {g_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {g_renk}30;text-align:center;">
        <div style="font-size:10px;color:#6ee7b7;letter-spacing:3px;text-transform:uppercase;">Mufredat Ilerleme</div>
        <div style="font-size:56px;font-weight:900;color:{g_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">%{genel_pct}</div>
        <div style="font-size:12px;color:#6ee7b7;">
            {islenen_kaz}/{toplam_kaz} kazanim · Hiz: {gunluk_hiz}/gun · Tahmini bitis: {tahmini_bitis} gun</div>
        <div style="margin:12px auto 0;max-width:300px;background:#1e293b;border-radius:6px;height:12px;overflow:hidden;">
            <div style="width:{genel_pct}%;height:100%;background:{g_renk};border-radius:6px;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Ders bazli ilerleme
    styled_section("Ders Bazli Mufredat Ilerlemesi")
    sirali = sorted(ders_ilerleme.items(), key=lambda x: x[1]["islenen"] / max(x[1]["toplam"], 1))

    for key, d in sirali:
        pct = round(d["islenen"] / max(d["toplam"], 1) * 100)
        kalan_d = d["toplam"] - d["islenen"]
        renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 45 else "#ef4444"
        alarm = " 🚨" if pct < 40 and kalan_gun < 60 else ""

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{key}{alarm}</span>
                <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
                            font-size:11px;font-weight:700;">%{pct} · {kalan_d} kalan</span>
            </div>
            <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. SINIF DİJİTAL İKİZ
# ============================================================

def render_sinif_dijital_ikiz(store):
    """Sinifin kolektif akademik profili."""
    styled_section("Sinif Dijital Ikiz", "#6366f1")
    styled_info_banner(
        "Sinifin kolektif akademik DNA'si. Not dagilimi, devamsizlik "
        "isi haritasi, risk haritasi, guclu/zayif dersler.",
        banner_type="info", icon="🧬")

    students = store.get_students(durum="aktif") if hasattr(store, "get_students") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    # Sinif/sube sec
    sinif_sube = sorted(set(f"{getattr(s, 'sinif', '')}-{getattr(s, 'sube', '')}" for s in students if getattr(s, "sinif", "")))
    if not sinif_sube:
        styled_info_banner("Sinif verisi yok.", banner_type="warning", icon="📊")
        return

    secili = st.selectbox("Sinif/Sube Secin", sinif_sube, key="sdi_sec")
    parts = secili.split("-")
    sinif_no, sube_no = parts[0], parts[1] if len(parts) > 1 else ""

    sinif_ogr = [s for s in students if str(getattr(s, "sinif", "")) == sinif_no and getattr(s, "sube", "") == sube_no]
    sinif_ids = set(getattr(s, "id", "") for s in sinif_ogr)

    if not sinif_ogr:
        styled_info_banner("Bu sinifta ogrenci yok.", banner_type="warning", icon="👤")
        return

    # Not verileri
    sinif_notlar = [g for g in grades if (getattr(g, "student_id", "") if hasattr(g, "student_id") else g.get("student_id", "")) in sinif_ids]
    sinif_puanlar = [getattr(g, "puan", 0) if hasattr(g, "puan") else g.get("puan", 0) for g in sinif_notlar]
    sinif_puanlar = [p for p in sinif_puanlar if isinstance(p, (int, float))]
    sinif_ort = round(sum(sinif_puanlar) / max(len(sinif_puanlar), 1), 1) if sinif_puanlar else 0

    # Devamsizlik
    sinif_dev = [a for a in attendance if (getattr(a, "student_id", "") if hasattr(a, "student_id") else a.get("student_id", "")) in sinif_ids]

    # Risk ogrenciler
    risk_ogrenci = 0
    for s in sinif_ogr:
        sid = getattr(s, "id", "")
        s_puanlar = [p for g in sinif_notlar
                      if (getattr(g, "student_id", "") if hasattr(g, "student_id") else g.get("student_id", "")) == sid
                      for p in [getattr(g, "puan", 0) if hasattr(g, "puan") else g.get("puan", 0)]
                      if isinstance(p, (int, float))]
        if s_puanlar and sum(s_puanlar) / len(s_puanlar) < 50:
            risk_ogrenci += 1

    s_renk = "#10b981" if sinif_ort >= 70 else "#f59e0b" if sinif_ort >= 55 else "#ef4444"

    styled_stat_row([
        ("Mevcut", str(len(sinif_ogr)), "#6366f1", "👤"),
        ("Not Ort.", str(sinif_ort), s_renk, "📊"),
        ("Devamsizlik", str(len(sinif_dev)), "#ef4444", "📋"),
        ("Risk Ogrenci", str(risk_ogrenci), "#dc2626", "⚠️"),
    ])

    # Hero
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                border:2px solid {s_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {s_renk}30;text-align:center;">
        <div style="font-size:10px;color:#a5b4fc;letter-spacing:3px;text-transform:uppercase;">
            {secili} Sinif Dijital Ikiz</div>
        <div style="font-size:56px;font-weight:900;color:{s_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{sinif_ort}</div>
        <div style="font-size:12px;color:#a5b4fc;">
            {len(sinif_ogr)} ogrenci · {len(sinif_dev)} devamsizlik · {risk_ogrenci} riskli</div>
    </div>""", unsafe_allow_html=True)

    # Ders bazli ortalama
    styled_section("Ders Bazli Ortalama")
    ders_grp = {}
    for g in sinif_notlar:
        ders = getattr(g, "ders", g.get("ders", "")) if isinstance(g, dict) else getattr(g, "ders", "")
        p = getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0)
        if ders and isinstance(p, (int, float)):
            ders_grp.setdefault(ders, []).append(p)

    for ders, puanlar_d in sorted(ders_grp.items(), key=lambda x: -sum(x[1]) / len(x[1])):
        ort = round(sum(puanlar_d) / len(puanlar_d), 1)
        renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 55 else "#ef4444"
        bar_w = min(ort, 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="min-width:100px;font-size:11px;color:#e2e8f0;font-weight:600;">{ders}</span>
            <div style="flex:1;background:#1e293b;border-radius:3px;height:16px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                            display:flex;align-items:center;padding-left:6px;">
                    <span style="font-size:9px;color:#fff;font-weight:700;">{ort}</span></div></div>
        </div>""", unsafe_allow_html=True)

    # Basari dagilimi
    styled_section("Basari Dagilimi")
    if sinif_puanlar:
        # Ogrenci bazli ortalama
        ogr_ort = {}
        for s in sinif_ogr:
            sid = getattr(s, "id", "")
            s_p = [p for g in sinif_notlar
                    if (getattr(g, "student_id", "") if hasattr(g, "student_id") else g.get("student_id", "")) == sid
                    for p in [getattr(g, "puan", 0) if hasattr(g, "puan") else g.get("puan", 0)]
                    if isinstance(p, (int, float))]
            if s_p:
                ogr_ort[sid] = round(sum(s_p) / len(s_p), 1)

        dilimler = {"90-100 (Cok Iyi)": 0, "70-89 (Iyi)": 0, "55-69 (Orta)": 0, "40-54 (Zayif)": 0, "0-39 (Basarisiz)": 0}
        for ort in ogr_ort.values():
            if ort >= 90: dilimler["90-100 (Cok Iyi)"] += 1
            elif ort >= 70: dilimler["70-89 (Iyi)"] += 1
            elif ort >= 55: dilimler["55-69 (Orta)"] += 1
            elif ort >= 40: dilimler["40-54 (Zayif)"] += 1
            else: dilimler["0-39 (Basarisiz)"] += 1

        dilim_renk = {"90-100 (Cok Iyi)": "#10b981", "70-89 (Iyi)": "#22c55e", "55-69 (Orta)": "#f59e0b",
                       "40-54 (Zayif)": "#f97316", "0-39 (Basarisiz)": "#ef4444"}
        for dilim, sayi in dilimler.items():
            renk = dilim_renk.get(dilim, "#64748b")
            bar_w = round(sayi / max(len(sinif_ogr), 1) * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="min-width:120px;font-size:10px;color:{renk};font-weight:600;">{dilim}</span>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:8px;color:#fff;font-weight:700;">{sayi}</span></div></div>
            </div>""", unsafe_allow_html=True)

    # AI sinif degerlendirmesi
    st.divider()
    if st.button("AI Sinif Degerlendirmesi", key=f"sdi_ai_{secili}", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                ders_ozet = ", ".join(f"{d}:{round(sum(p)/len(p),1)}" for d, p in ders_grp.items())
                veri = (f"Sinif: {secili}, Mevcut: {len(sinif_ogr)}, Not Ort: {sinif_ort}, "
                        f"Devamsizlik: {len(sinif_dev)}, Risk: {risk_ogrenci}\nDersler: {ders_ozet}")
                with st.spinner("AI sinif analizi..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir sinif analisti. Sinifin kolektif profilini degerlendir: 1) Genel durum 2) Guclu dersler 3) Zayif dersler 4) Risk analizi 5) Oneri. Turkce, kisa."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=400, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #6366f1;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#a5b4fc;font-weight:700;margin-bottom:6px;">AI Sinif Profili — {secili}</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 3. AKADEMİK ZAMAN MAKİNESİ
# ============================================================

def render_akademik_zaman(store):
    """Donemler arasi akademik karsilastirma."""
    styled_section("Akademik Zaman Makinesi", "#f59e0b")
    styled_info_banner(
        "1. Donem vs 2. Donem, bu yil vs gecen yil — tum metrikleri karsilastirin.",
        banner_type="info", icon="⏰")

    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    if not grades:
        styled_info_banner("Karsilastirma icin not verisi gerekli.", banner_type="warning", icon="📊")
        return

    # Donem bazli ayir
    bugun = date.today()
    yil = bugun.year if bugun.month >= 9 else bugun.year - 1
    donem1_bas = f"{yil}-09-01"
    donem1_bit = f"{yil + 1}-01-31"
    donem2_bas = f"{yil + 1}-02-01"
    donem2_bit = f"{yil + 1}-06-30"

    d1_notlar = [g for g in grades if donem1_bas <= (getattr(g, "created_at", g.get("created_at", "")) if isinstance(g, dict) else getattr(g, "created_at", "") or "")[:10] <= donem1_bit]
    d2_notlar = [g for g in grades if donem2_bas <= (getattr(g, "created_at", g.get("created_at", "")) if isinstance(g, dict) else getattr(g, "created_at", "") or "")[:10] <= donem2_bit]

    def _donem_metrik(notlar):
        puanlar = [getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0) for g in notlar]
        puanlar = [p for p in puanlar if isinstance(p, (int, float))]
        return {
            "not_sayi": len(puanlar),
            "ort": round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0,
            "en_yuksek": max(puanlar) if puanlar else 0,
            "en_dusuk": min(puanlar) if puanlar else 0,
        }

    d1 = _donem_metrik(d1_notlar)
    d2 = _donem_metrik(d2_notlar)

    # Degisim
    def _fark(bu, gecen):
        if gecen == 0:
            return "+∞" if bu > 0 else "—"
        f = round(bu - gecen, 1)
        return f"+{f}" if f >= 0 else str(f)

    def _fark_renk(bu, gecen):
        return "#10b981" if bu >= gecen else "#ef4444"

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr auto 1fr;gap:12px;margin:16px 0;">
        <div style="background:#0f172a;border:2px solid #3b82f6;border-radius:14px;padding:16px;text-align:center;">
            <div style="font-size:14px;font-weight:800;color:#3b82f6;margin-bottom:12px;">1. Donem</div>
            <div style="font-size:28px;font-weight:900;color:#e2e8f0;">{d1['ort']}</div>
            <div style="font-size:10px;color:#94a3b8;">{d1['not_sayi']} not</div>
        </div>
        <div style="display:flex;align-items:center;font-size:24px;color:#f59e0b;">⏰</div>
        <div style="background:#0f172a;border:2px solid #f59e0b;border-radius:14px;padding:16px;text-align:center;">
            <div style="font-size:14px;font-weight:800;color:#f59e0b;margin-bottom:12px;">2. Donem</div>
            <div style="font-size:28px;font-weight:900;color:#e2e8f0;">{d2['ort']}</div>
            <div style="font-size:10px;color:#94a3b8;">{d2['not_sayi']} not</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Fark analizi
    styled_section("Donem Fark Analizi")
    metrikler = [
        ("Not Ortalamasi", d1["ort"], d2["ort"], False),
        ("Not Sayisi", d1["not_sayi"], d2["not_sayi"], False),
        ("En Yuksek Not", d1["en_yuksek"], d2["en_yuksek"], False),
        ("En Dusuk Not", d1["en_dusuk"], d2["en_dusuk"], False),
    ]

    for label, d1_val, d2_val, ters in metrikler:
        fark = _fark(d2_val, d1_val)
        renk = _fark_renk(d2_val, d1_val) if not ters else _fark_renk(d1_val, d2_val)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">{label}</span>
            <span style="min-width:50px;font-size:14px;font-weight:800;color:#3b82f6;text-align:right;">{d1_val}</span>
            <span style="color:#64748b;">→</span>
            <span style="min-width:50px;font-size:14px;font-weight:800;color:#f59e0b;">{d2_val}</span>
            <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
                        font-size:11px;font-weight:700;">{fark}</span>
        </div>""", unsafe_allow_html=True)

    # Ders bazli donem karsilastirma
    styled_section("Ders Bazli Donem Karsilastirma")
    d1_dersler = {}
    d2_dersler = {}
    for g in d1_notlar:
        ders = getattr(g, "ders", g.get("ders", "")) if isinstance(g, dict) else getattr(g, "ders", "")
        p = getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0)
        if ders and isinstance(p, (int, float)):
            d1_dersler.setdefault(ders, []).append(p)
    for g in d2_notlar:
        ders = getattr(g, "ders", g.get("ders", "")) if isinstance(g, dict) else getattr(g, "ders", "")
        p = getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0)
        if ders and isinstance(p, (int, float)):
            d2_dersler.setdefault(ders, []).append(p)

    tum_dersler = sorted(set(list(d1_dersler.keys()) + list(d2_dersler.keys())))
    for ders in tum_dersler:
        d1_ort = round(sum(d1_dersler.get(ders, [0])) / max(len(d1_dersler.get(ders, [1])), 1), 1)
        d2_ort = round(sum(d2_dersler.get(ders, [0])) / max(len(d2_dersler.get(ders, [1])), 1), 1)
        fark_val = d2_ort - d1_ort
        fark_renk = "#10b981" if fark_val >= 0 else "#ef4444"
        fark_txt = f"+{fark_val:.0f}" if fark_val >= 0 else f"{fark_val:.0f}"

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="min-width:100px;font-size:11px;color:#e2e8f0;font-weight:600;">{ders}</span>
            <span style="min-width:35px;font-size:12px;color:#3b82f6;font-weight:700;text-align:right;">{d1_ort}</span>
            <span style="color:#64748b;font-size:10px;">→</span>
            <span style="min-width:35px;font-size:12px;color:#f59e0b;font-weight:700;">{d2_ort}</span>
            <span style="background:{fark_renk}20;color:{fark_renk};padding:1px 8px;border-radius:4px;
                        font-size:10px;font-weight:700;">{fark_txt}</span>
        </div>""", unsafe_allow_html=True)
