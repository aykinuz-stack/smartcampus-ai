"""
Akademik Takip — Zirve Ozellikleri
=====================================
1. Akademik Komuta Merkezi (Academic Control Tower)
2. Sinif/Sube Karsilastirma Arena
3. AI Akademik Strateji Danismani
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
# 1. AKADEMİK KOMUTA MERKEZİ
# ============================================================

def render_akademik_komuta(store):
    """Tum akademik operasyonun canli kontrol paneli."""
    styled_section("Akademik Komuta Merkezi", "#2563eb")

    bugun = date.today()
    bugun_str = bugun.isoformat()
    simdi = datetime.now()
    ak = _ak_dir()

    # Veriler
    students = store.get_students(durum="aktif") if hasattr(store, "get_students") else []
    teachers = store.get_teachers() if hasattr(store, "get_teachers") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    # Bugunun verileri
    bugun_not = [g for g in grades if (getattr(g, "created_at", "") or "")[:10] == bugun_str]
    bugun_devamsiz = [a for a in attendance if getattr(a, "tarih", "") == bugun_str]
    devamsiz_ogrenci = len(set(getattr(a, "student_id", "") for a in bugun_devamsiz))

    # Kazanim isleme
    try:
        kazanim = store.get_kazanim_isleme() if hasattr(store, "get_kazanim_isleme") else []
    except Exception:
        kazanim = []

    # Odev
    try:
        import json
        odevler = json.load(open(os.path.join(ak, "odevler.json"), encoding="utf-8")) if os.path.exists(os.path.join(ak, "odevler.json")) else []
    except Exception:
        odevler = []

    # Su anki ders
    try:
        from views._yte_zirve_features import _aktif_ders_saati
        aktif_ders = _aktif_ders_saati()
    except Exception:
        aktif_ders = 0

    # Ogretmen bazli not girisi (bugun)
    ogretmen_not = Counter()
    for g in bugun_not:
        ogr = getattr(g, "ogretmen_adi", "") if hasattr(g, "ogretmen_adi") else (g.get("ogretmen_adi", "") if isinstance(g, dict) else "")
        if ogr:
            ogretmen_not[ogr] += 1

    not_giren_ogretmen = len(ogretmen_not)
    toplam_ogretmen = len(teachers)

    styled_stat_row([
        ("Aktif Ogrenci", str(len(students)), "#2563eb", "🎓"),
        ("Ogretmen", str(toplam_ogretmen), "#7c3aed", "👨‍🏫"),
        ("Bugun Not", str(len(bugun_not)), "#10b981", "📝"),
        ("Bugun Devamsiz", str(devamsiz_ogrenci), "#ef4444", "📋"),
    ])

    # ── HERO ──
    ders_txt = f"{aktif_ders}. Ders" if aktif_ders > 0 else "Ders yok"
    ders_renk = "#10b981" if aktif_ders > 0 else "#64748b"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b 0%,#1e3a5f 100%);
                border:2px solid #2563eb;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(37,99,235,0.25);">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:10px;color:#93c5fd;letter-spacing:3px;text-transform:uppercase;">Akademik Komuta</div>
                <div style="font-size:24px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                    {bugun.strftime('%d.%m.%Y')}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:24px;font-weight:900;color:{ders_renk};font-family:monospace;">
                    {simdi.strftime('%H:%M')}</div>
                <div style="font-size:10px;color:#93c5fd;">{ders_txt}</div>
            </div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:16px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#10b981;">{not_giren_ogretmen}</div>
                <div style="font-size:8px;color:#93c5fd;">Not Giren Ogt</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#f59e0b;">{toplam_ogretmen - not_giren_ogretmen}</div>
                <div style="font-size:8px;color:#93c5fd;">Not Girmeyen</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#7c3aed;">{len(kazanim)}</div>
                <div style="font-size:8px;color:#93c5fd;">Kazanim Isleme</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#ea580c;">{len(odevler)}</div>
                <div style="font-size:8px;color:#93c5fd;">Toplam Odev</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # En aktif ogretmenler
    if ogretmen_not:
        styled_section("Bugun En Aktif Ogretmenler (Not Girisi)")
        for ogr, sayi in ogretmen_not.most_common(5):
            st.markdown(f"- **{ogr}**: {sayi} not girisi")

    # Alarm
    alarmlar = []
    if devamsiz_ogrenci > 20:
        alarmlar.append(f"Bugun {devamsiz_ogrenci} devamsiz ogrenci — yuksek!")
    if not_giren_ogretmen == 0 and simdi.hour >= 10:
        alarmlar.append("Bugun hic not girisi yapilmamis!")

    # Sinif bazli yoklama durumu
    sinif_yoklama = Counter()
    for a in bugun_devamsiz:
        s = getattr(a, "sinif", a.get("sinif", "")) if isinstance(a, dict) else getattr(a, "sinif", "")
        sinif_yoklama[str(s)] += 1

    if sinif_yoklama:
        styled_section("Sinif Bazli Devamsizlik (Bugun)")
        for sinif_no, sayi in sinif_yoklama.most_common(8):
            renk = "#ef4444" if sayi > 5 else "#f59e0b" if sayi > 2 else "#10b981"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                <span style="min-width:60px;font-size:11px;color:#e2e8f0;font-weight:600;">{sinif_no}. Sinif</span>
                <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
                            font-size:11px;font-weight:700;">{sayi} devamsiz</span>
            </div>""", unsafe_allow_html=True)

    if alarmlar:
        for a in alarmlar:
            styled_info_banner(a, banner_type="error", icon="🚨")


# ============================================================
# 2. SINIF/ŞUBE KARŞILAŞTIRMA ARENA
# ============================================================

def render_sinif_karsilastirma(store):
    """Iki sinif/subeyi yan yana karsilastir."""
    styled_section("Sinif/Sube Karsilastirma Arena", "#f59e0b")
    styled_info_banner(
        "Iki sinif veya subeyi yan yana karsilastirin. "
        "Not ortalamasi, devamsizlik, odev teslim, kazanim — hepsi.",
        banner_type="info", icon="⚔️")

    students = store.get_students(durum="aktif") if hasattr(store, "get_students") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    # Sinif/sube listesi
    sinif_sube = sorted(set(f"{getattr(s, 'sinif', '')}-{getattr(s, 'sube', '')}" for s in students if getattr(s, "sinif", "")))

    if len(sinif_sube) < 2:
        styled_info_banner("Karsilastirma icin en az 2 sinif/sube gerekli.", banner_type="warning", icon="📊")
        return

    col1, col2 = st.columns(2)
    with col1:
        sol = st.selectbox("Sinif A", sinif_sube, key="ska_sol")
    with col2:
        sag = st.selectbox("Sinif B", [s for s in sinif_sube if s != sol], key="ska_sag")

    if not sol or not sag:
        return

    def _sinif_metrik(sinif_sube_str):
        parts = sinif_sube_str.split("-")
        sinif_no = parts[0] if parts else ""
        sube_no = parts[1] if len(parts) > 1 else ""

        ogr = [s for s in students if str(getattr(s, "sinif", "")) == sinif_no and getattr(s, "sube", "") == sube_no]
        ogr_ids = set(getattr(s, "id", "") for s in ogr)

        ogr_notlar = [g for g in grades if getattr(g, "student_id", g.get("student_id", "") if isinstance(g, dict) else "") in ogr_ids]
        ogr_puanlar = []
        for g in ogr_notlar:
            p = getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0)
            if isinstance(p, (int, float)):
                ogr_puanlar.append(p)

        ogr_devamsiz = [a for a in attendance if getattr(a, "student_id", a.get("student_id", "") if isinstance(a, dict) else "") in ogr_ids]

        return {
            "ogrenci": len(ogr),
            "not_ort": round(sum(ogr_puanlar) / max(len(ogr_puanlar), 1), 1) if ogr_puanlar else 0,
            "not_sayisi": len(ogr_puanlar),
            "devamsizlik": len(ogr_devamsiz),
            "dev_kisi": len(set(getattr(a, "student_id", a.get("student_id", "") if isinstance(a, dict) else "") for a in ogr_devamsiz)),
        }

    sol_m = _sinif_metrik(sol)
    sag_m = _sinif_metrik(sag)

    # Yan yana karsilastirma
    metrikler = [
        ("Ogrenci Sayisi", sol_m["ogrenci"], sag_m["ogrenci"], False),
        ("Not Ortalamasi", sol_m["not_ort"], sag_m["not_ort"], False),
        ("Not Sayisi", sol_m["not_sayisi"], sag_m["not_sayisi"], False),
        ("Devamsizlik", sol_m["devamsizlik"], sag_m["devamsizlik"], True),
        ("Devamsiz Ogrenci", sol_m["dev_kisi"], sag_m["dev_kisi"], True),
    ]

    col1, col2, col3 = st.columns([1, 0.2, 1])
    with col1:
        st.markdown(f'<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:18px;">{sol}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align:center;font-size:28px;padding-top:10px;">⚔️</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:18px;">{sag}</div>', unsafe_allow_html=True)

    for label, sol_val, sag_val, ters in metrikler:
        # Kazanan
        if ters:
            sol_better = sol_val < sag_val
        else:
            sol_better = sol_val > sag_val

        if sol_val == sag_val:
            sol_renk = sag_renk = "#f59e0b"
        elif sol_better:
            sol_renk, sag_renk = "#10b981", "#ef4444"
        else:
            sol_renk, sag_renk = "#ef4444", "#10b981"

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <div style="flex:1;text-align:right;">
                <span style="font-size:18px;font-weight:900;color:{sol_renk};">{sol_val}</span>
            </div>
            <div style="min-width:120px;text-align:center;">
                <span style="font-size:11px;color:#94a3b8;font-weight:600;">{label}</span>
            </div>
            <div style="flex:1;text-align:left;">
                <span style="font-size:18px;font-weight:900;color:{sag_renk};">{sag_val}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # Kazanan
    sol_skor = sol_m["not_ort"] * 0.5 - sol_m["devamsizlik"] * 0.1
    sag_skor = sag_m["not_ort"] * 0.5 - sag_m["devamsizlik"] * 0.1
    kazanan = sol if sol_skor > sag_skor else sag if sag_skor > sol_skor else "Esit"
    k_renk = "#10b981"
    st.markdown(f"""
    <div style="background:{k_renk}15;border:2px solid {k_renk};border-radius:14px;
                padding:14px;text-align:center;margin-top:12px;">
        <span style="font-size:16px;font-weight:900;color:{k_renk};">
            🏆 {kazanan} {'daha iyi performans gosteriyor' if kazanan != 'Esit' else '— her iki sinif esit'}</span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# 3. AI AKADEMİK STRATEJİ DANIŞMANI
# ============================================================

def render_ai_strateji(store):
    """Tum akademik verileri capraz analiz eden AI strateji danismani."""
    styled_section("AI Akademik Strateji Danismani", "#7c3aed")
    styled_info_banner(
        "Tum akademik verileri capraz analiz eder. "
        "Zayif alanlar, guclu ogretmenler, risk trendleri — stratejik oneriler.",
        banner_type="info", icon="🧠")

    students = store.get_students(durum="aktif") if hasattr(store, "get_students") else []
    teachers = store.get_teachers() if hasattr(store, "get_teachers") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    # Istatistikler
    puanlar = []
    for g in grades:
        p = getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0)
        if isinstance(p, (int, float)):
            puanlar.append(p)
    genel_ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0

    # Ders bazli ortalama
    ders_notlar = {}
    for g in grades:
        ders = getattr(g, "ders", g.get("ders", "") if isinstance(g, dict) else "")
        p = getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0)
        if ders and isinstance(p, (int, float)):
            ders_notlar.setdefault(ders, []).append(p)
    ders_ort = {d: round(sum(p) / len(p), 1) for d, p in ders_notlar.items()}

    styled_stat_row([
        ("Ogrenci", str(len(students)), "#2563eb", "🎓"),
        ("Ogretmen", str(len(teachers)), "#7c3aed", "👨‍🏫"),
        ("Not Kaydi", str(len(grades)), "#10b981", "📝"),
        ("Genel Ort.", str(genel_ort), "#f59e0b", "📊"),
    ])

    # ── KURAL BAZLI INSIGHT'LAR ──
    insights = []

    # En basarili / en zayif ders
    if ders_ort:
        en_iyi = max(ders_ort.items(), key=lambda x: x[1])
        en_zayif = min(ders_ort.items(), key=lambda x: x[1])
        insights.append({"seviye": "basari", "ikon": "🌟",
                          "baslik": f"En basarili ders: {en_iyi[0]} (ort: {en_iyi[1]})",
                          "oneri": "Bu dersin ogretmeninin yontemlerini diger derslere yaygin."})
        if en_zayif[1] < 60:
            insights.append({"seviye": "uyari", "ikon": "📉",
                              "baslik": f"En zayif ders: {en_zayif[0]} (ort: {en_zayif[1]})",
                              "oneri": "Etut/destek programi planlayin, kazanim eksiklerini kontrol edin."})

    # Devamsizlik analizi
    devamsiz_toplam = len(attendance)
    if devamsiz_toplam > len(students) * 5:
        insights.append({"seviye": "uyari", "ikon": "📋",
                          "baslik": f"Devamsizlik yuksek ({devamsiz_toplam} kayit)",
                          "oneri": "Veli gorusmeleri planlayin, devamsizlik nedenlerini arastirin."})

    # Genel ortalama
    if genel_ort < 60:
        insights.append({"seviye": "kritik", "ikon": "🔴",
                          "baslik": f"Genel not ortalamasi dusuk: {genel_ort}",
                          "oneri": "Acil akademik destek programi baslatin."})
    elif genel_ort >= 75:
        insights.append({"seviye": "basari", "ikon": "🏆",
                          "baslik": f"Genel not ortalamasi iyi: {genel_ort}",
                          "oneri": "Bu basariyi koruyun, olimpiyat/yarisma katilimini artirin."})

    # Render
    seviye_renk = {"kritik": "#ef4444", "uyari": "#f97316", "bilgi": "#3b82f6", "basari": "#10b981"}
    seviye_bg = {"kritik": "#450a0a", "uyari": "#431407", "bilgi": "#0c1a3d", "basari": "#052e16"}

    for ins in sorted(insights, key=lambda x: {"kritik": 0, "uyari": 1, "bilgi": 2, "basari": 3}.get(x["seviye"], 2)):
        renk = seviye_renk.get(ins["seviye"], "#64748b")
        bg = seviye_bg.get(ins["seviye"], "#0f172a")
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {renk}40;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:16px;">{ins['ikon']}</span>
                <span style="font-weight:700;color:#fff;font-size:13px;">{ins['baslik']}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:6px 10px;">
                <span style="font-size:11px;color:{renk};font-weight:700;">Oneri:</span>
                <span style="font-size:11px;color:#cbd5e1;"> {ins['oneri']}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # Ders bazli ortalama bar
    if ders_ort:
        styled_section("Ders Bazli Not Ortalamasi")
        for ders, ort in sorted(ders_ort.items(), key=lambda x: -x[1]):
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

    # AI derin analiz
    st.divider()
    if st.button("AI Donemsel Strateji Raporu", key="at_ai_str", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                ders_ozet = ", ".join(f"{d}:{o}" for d, o in sorted(ders_ort.items(), key=lambda x: x[1])[:10])
                veri = (f"Ogrenci: {len(students)}, Ogretmen: {len(teachers)}, Not: {len(grades)}, "
                        f"Genel Ort: {genel_ort}, Devamsizlik: {devamsiz_toplam}\n"
                        f"Ders ortalamalar: {ders_ozet}")
                with st.spinner("AI strateji raporu hazirlaniyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul akademik strateji danisman. Verilen verileri analiz et: 1) Donem degerlendirmesi 2) Basarili alanlar 3) Zayif alanlar 4) Ogretmen onerileri 5) Gelecek donem icin 5 aksiyon. Turkce, somut."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=600, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Donemsel Strateji Raporu</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
