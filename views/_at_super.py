"""
Akademik Takip — Super Ozellikleri
=====================================
1. Ogretmen Verimlilik Radari
2. Akademik Erken Mudahale Otomasyonu
3. Akademik Tahmin Motoru
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
# 1. ÖĞRETMEN VERİMLİLİK RADARI
# ============================================================

def render_ogretmen_verimlilik(store):
    """Her ogretmenin akademik uretkenligini olc + karsilastir."""
    styled_section("Ogretmen Verimlilik Radari", "#ea580c")
    styled_info_banner(
        "Not girisi, kazanim tamamlama, odev verme, ogrenci basarisi — "
        "her ogretmenin veri bazli verimlilik skoru.",
        banner_type="info", icon="👨‍🏫")

    teachers = store.get_teachers() if hasattr(store, "get_teachers") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    ak = _ak_dir()

    if not teachers:
        styled_info_banner("Ogretmen verisi bulunamadi.", banner_type="warning", icon="👨‍🏫")
        return

    # Kazanim isleme
    try:
        import json
        kazanim = json.load(open(os.path.join(ak, "kazanim_isleme.json"), encoding="utf-8")) if os.path.exists(os.path.join(ak, "kazanim_isleme.json")) else []
    except Exception:
        kazanim = []

    # Odevler
    try:
        import json
        odevler = json.load(open(os.path.join(ak, "odevler.json"), encoding="utf-8")) if os.path.exists(os.path.join(ak, "odevler.json")) else []
    except Exception:
        odevler = []

    # Ogretmen bazli metrikler
    ogr_veriler = []
    for t in teachers:
        t_ad = f"{getattr(t, 'ad', '')} {getattr(t, 'soyad', '')}".strip()
        t_brans = getattr(t, "brans", "")
        if not t_ad:
            continue

        t_ad_lower = t_ad.lower()

        # Not girisi
        t_notlar = [g for g in grades if (getattr(g, "ogretmen_adi", "") or "").lower() == t_ad_lower]
        not_sayi = len(t_notlar)
        not_puanlar = [getattr(g, "puan", 0) for g in t_notlar if isinstance(getattr(g, "puan", 0), (int, float))]
        ogr_basari = round(sum(not_puanlar) / max(len(not_puanlar), 1), 1) if not_puanlar else 0

        # Kazanim
        t_kazanim = sum(1 for k in kazanim if isinstance(k, dict) and t_ad_lower in (k.get("ogretmen_adi", "") or "").lower())

        # Odev
        t_odev = sum(1 for o in odevler if isinstance(o, dict) and t_ad_lower in (o.get("ogretmen", o.get("ogretmen_adi", "")) or "").lower())

        # Verimlilik skoru
        skor = min(100, not_sayi * 2 + t_kazanim * 3 + t_odev * 5 + (ogr_basari - 50) * 0.5 if ogr_basari > 50 else 0)
        skor = max(0, round(skor))

        ogr_veriler.append({
            "ad": t_ad, "brans": t_brans, "not_sayi": not_sayi,
            "kazanim": t_kazanim, "odev": t_odev,
            "ogr_basari": ogr_basari, "skor": skor,
        })

    ogr_veriler.sort(key=lambda x: -x["skor"])

    # Ozet
    ort_skor = round(sum(o["skor"] for o in ogr_veriler) / max(len(ogr_veriler), 1))
    styled_stat_row([
        ("Ogretmen Sayisi", str(len(ogr_veriler)), "#ea580c", "👨‍🏫"),
        ("Ort. Verimlilik", str(ort_skor), "#f59e0b", "📊"),
        ("En Verimli", ogr_veriler[0]["ad"].split()[0] if ogr_veriler else "-", "#10b981", "🏆"),
    ])

    # Siralama
    styled_section("Verimlilik Siralamasi")
    for sira, o in enumerate(ogr_veriler[:15], 1):
        madalya = {1: "🥇", 2: "🥈", 3: "🥉"}.get(sira, f"#{sira}")
        renk = "#10b981" if o["skor"] >= 70 else "#f59e0b" if o["skor"] >= 40 else "#ef4444"
        bar_w = min(o["skor"], 100)
        en_yuksek = ogr_veriler[0]["skor"] if ogr_veriler else 1

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {renk}30;border-radius:12px;
                    padding:10px 16px;margin-bottom:6px;display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;min-width:32px;text-align:center;">{madalya}</span>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{o['ad']}</span>
                    <span style="font-size:20px;font-weight:900;color:{renk};">{o['skor']}</span>
                </div>
                <div style="font-size:9px;color:#64748b;margin:2px 0;">
                    {o['brans']} · Not:{o['not_sayi']} · Kaz:{o['kazanim']} · Odev:{o['odev']} · Ogr.Ort:{o['ogr_basari']}</div>
                <div style="background:#1e293b;border-radius:3px;height:4px;overflow:hidden;">
                    <div style="width:{round(o['skor'] / max(en_yuksek, 1) * 100)}%;height:100%;background:{renk};border-radius:3px;"></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. AKADEMİK ERKEN MÜDAHALE OTOMASYONU
# ============================================================

def render_oto_mudahale(store):
    """Risk tespitinde otomatik aksiyon zinciri."""
    styled_section("Otomatik Mudahale Sistemi", "#dc2626")
    styled_info_banner(
        "Risk tespit edildiginde otomatik aksiyon zinciri baslatir. "
        "Not dususu → etut, devamsizlik → veli arama, kazanim borcu → telafi.",
        banner_type="warning", icon="⚡")

    students = store.get_students(durum="aktif") if hasattr(store, "get_students") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    # Mudahale tetikleyicileri
    mudahaleler = []

    for s in students:
        sid = getattr(s, "id", "")
        ad = f"{getattr(s, 'ad', '')} {getattr(s, 'soyad', '')}".strip()
        sinif = f"{getattr(s, 'sinif', '')}-{getattr(s, 'sube', '')}"

        # 1. Not ortalamasi < 50
        s_notlar = [g for g in grades if (getattr(g, "student_id", "") if hasattr(g, "student_id") else g.get("student_id", "")) == sid]
        s_puanlar = [getattr(g, "puan", 0) if hasattr(g, "puan") else g.get("puan", 0) for g in s_notlar]
        s_puanlar = [p for p in s_puanlar if isinstance(p, (int, float))]
        ort = round(sum(s_puanlar) / max(len(s_puanlar), 1), 1) if s_puanlar else 0

        if ort > 0 and ort < 50:
            mudahaleler.append({
                "ogrenci": ad, "sinif": sinif, "seviye": "acil", "ikon": "📉",
                "tetik": f"Not ort. {ort} (< 50)",
                "aksiyon": "Etut kaydi olustur + ogretmene bildir",
                "sorumlu": "Ders Ogretmeni",
            })

        # 2. Devamsizlik > 15
        s_dev = sum(1 for a in attendance if (getattr(a, "student_id", "") if hasattr(a, "student_id") else a.get("student_id", "")) == sid)
        if s_dev > 15:
            mudahaleler.append({
                "ogrenci": ad, "sinif": sinif, "seviye": "yuksek", "ikon": "📋",
                "tetik": f"{s_dev} devamsizlik (> 15)",
                "aksiyon": "Veli arama gorevi ata + rehberlige bildir",
                "sorumlu": "Sinif Ogretmeni + Rehberlik",
            })

        # 3. Son 3 notta dusus
        if len(s_puanlar) >= 3:
            son3 = s_puanlar[-3:]
            if son3[-1] < son3[0] - 15:
                dusus_ders = ""
                if s_notlar:
                    son = s_notlar[-1]
                    dusus_ders = getattr(son, "ders", son.get("ders", "")) if isinstance(son, dict) else getattr(son, "ders", "")
                mudahaleler.append({
                    "ogrenci": ad, "sinif": sinif, "seviye": "yuksek", "ikon": "📉",
                    "tetik": f"{dusus_ders} dersinde son 3 notta {son3[0]}→{son3[-1]} dusus",
                    "aksiyon": "Ek ders/etut planla",
                    "sorumlu": "Ders Ogretmeni",
                })

    # Ozet
    acil = sum(1 for m in mudahaleler if m["seviye"] == "acil")
    yuksek = sum(1 for m in mudahaleler if m["seviye"] == "yuksek")

    styled_stat_row([
        ("Toplam Mudahale", str(len(mudahaleler)), "#dc2626", "⚡"),
        ("Acil", str(acil), "#ef4444", "🚨"),
        ("Yuksek", str(yuksek), "#f97316", "🟠"),
        ("Taranan Ogrenci", str(len(students)), "#2563eb", "🎓"),
    ])

    if not mudahaleler:
        st.success("Harika! Otomatik mudahale gerektiren ogrenci yok.")
        return

    # Render
    seviye_renk = {"acil": "#ef4444", "yuksek": "#f97316", "normal": "#f59e0b"}
    seviye_bg = {"acil": "#450a0a", "yuksek": "#431407", "normal": "#422006"}

    for m in sorted(mudahaleler, key=lambda x: {"acil": 0, "yuksek": 1, "normal": 2}[x["seviye"]]):
        renk = seviye_renk.get(m["seviye"], "#64748b")
        bg = seviye_bg.get(m["seviye"], "#0f172a")
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {renk}40;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:16px;">{m['ikon']}</span>
                <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{m['ogrenci']}</span>
                <span style="color:#94a3b8;font-size:10px;">({m['sinif']})</span>
                <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:9px;font-weight:700;margin-left:auto;">{m['seviye'].upper()}</span>
            </div>
            <div style="font-size:11px;color:#94a3b8;margin-bottom:4px;">Tetik: {m['tetik']}</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:6px 10px;">
                <span style="font-size:11px;color:{renk};font-weight:700;">Aksiyon:</span>
                <span style="font-size:11px;color:#cbd5e1;"> {m['aksiyon']}</span>
                <span style="font-size:10px;color:#64748b;margin-left:8px;">({m['sorumlu']})</span>
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. AKADEMİK TAHMİN MOTORU
# ============================================================

def render_tahmin_motoru(store):
    """Donem sonu performans tahmini + senaryo simulasyonu."""
    styled_section("Akademik Tahmin Motoru", "#7c3aed")
    styled_info_banner(
        "Mevcut verilerden donem sonu not ortalamasi, devamsizlik ve "
        "kazanim tamamlanma tahmini. Senaryo simulasyonu ile mudahale plani.",
        banner_type="info", icon="🔮")

    students = store.get_students(durum="aktif") if hasattr(store, "get_students") else []
    grades = store.get_grades() if hasattr(store, "get_grades") else []
    attendance = store.get_attendance() if hasattr(store, "get_attendance") else []

    if not students or not grades:
        styled_info_banner("Tahmin icin yeterli veri yok.", banner_type="warning", icon="📊")
        return

    # Genel metrikler
    puanlar = [getattr(g, "puan", g.get("puan", 0) if isinstance(g, dict) else 0) for g in grades]
    puanlar = [p for p in puanlar if isinstance(p, (int, float))]
    mevcut_ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0
    toplam_dev = len(attendance)

    # Trend hesapla
    bugun = date.today()
    yil_basi = date(bugun.year if bugun.month >= 9 else bugun.year - 1, 9, 1)
    gecen_gun = max((bugun - yil_basi).days, 1)
    kalan_gun = max(180 - gecen_gun, 0)

    # Donem sonu tahmini (basit linear)
    # Not ortalamasi — son notlarin trendine gore
    son_notlar = sorted(puanlar[-100:]) if len(puanlar) >= 100 else puanlar
    ilk_yari = sum(son_notlar[:len(son_notlar)//2]) / max(len(son_notlar)//2, 1) if son_notlar else 0
    son_yari = sum(son_notlar[len(son_notlar)//2:]) / max(len(son_notlar) - len(son_notlar)//2, 1) if son_notlar else 0
    trend = son_yari - ilk_yari

    tahmin_ort = round(mevcut_ort + trend * 0.3, 1)
    iyimser = round(tahmin_ort + abs(trend) * 0.5, 1)
    kotumser = round(tahmin_ort - abs(trend) * 0.5, 1)

    # Devamsizlik tahmini
    gunluk_dev = toplam_dev / gecen_gun if gecen_gun > 0 else 0
    tahmin_dev = round(toplam_dev + gunluk_dev * kalan_gun)

    t_renk = "#10b981" if tahmin_ort >= 70 else "#f59e0b" if tahmin_ort >= 55 else "#ef4444"

    styled_stat_row([
        ("Mevcut Ort.", str(mevcut_ort), "#2563eb", "📊"),
        ("Tahmin Ort.", str(tahmin_ort), t_renk, "🔮"),
        ("Trend", f"{'↑' if trend > 0 else '↓'}{abs(trend):.1f}", "#10b981" if trend > 0 else "#ef4444", "📈"),
        ("Kalan Gun", str(kalan_gun), "#f59e0b", "📅"),
    ])

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#312e81 0%,#4c1d95 100%);
                border:2px solid {t_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {t_renk}30;text-align:center;">
        <div style="font-size:10px;color:#c4b5fd;letter-spacing:3px;text-transform:uppercase;">Donem Sonu Tahmin</div>
        <div style="font-size:56px;font-weight:900;color:{t_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{tahmin_ort}</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;">
                <div style="font-size:9px;color:#94a3b8;">Iyimser</div>
                <div style="font-size:22px;font-weight:900;color:#10b981;">{iyimser}</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;border:1px solid {t_renk};">
                <div style="font-size:9px;color:{t_renk};">Gercekci</div>
                <div style="font-size:22px;font-weight:900;color:{t_renk};">{tahmin_ort}</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;">
                <div style="font-size:9px;color:#94a3b8;">Kotumser</div>
                <div style="font-size:22px;font-weight:900;color:#ef4444;">{kotumser}</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Devamsizlik tahmini
    dev_renk = "#ef4444" if tahmin_dev > len(students) * 10 else "#f59e0b"
    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid {dev_renk}30;border-left:4px solid {dev_renk};
                border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:12px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-weight:700;color:#e2e8f0;font-size:13px;">Devamsizlik Yil Sonu Tahmini</span>
            <span style="font-size:18px;font-weight:900;color:{dev_renk};">{tahmin_dev}</span>
        </div>
        <div style="font-size:10px;color:#94a3b8;">Mevcut: {toplam_dev} · Gunluk ort: {gunluk_dev:.1f} · Kalan: {kalan_gun} gun</div>
    </div>""", unsafe_allow_html=True)

    # ── SENARYO SİMÜLASYONU ──
    styled_section("Senaryo Simulasyonu")
    st.caption("Parametreleri degistirin — etkiyi gorun:")

    col1, col2 = st.columns(2)
    with col1:
        ek_etut = st.slider("Haftalik Ek Etut (saat)", 0, 10, 0, key="at_ek_etut")
        devamsizlik_azalt = st.checkbox("Devamsizligi yarisina indir", key="at_dev_azalt")
    with col2:
        ek_sinav = st.slider("Ek Sinav/KYT Sayisi", 0, 10, 0, key="at_ek_sinav")
        odev_artir = st.checkbox("Odev teslim takibini sikistir", key="at_odev_artir")

    senaryo_ort = tahmin_ort
    senaryo_etki = []

    if ek_etut > 0:
        artis = ek_etut * 1.5
        senaryo_ort += artis
        senaryo_etki.append(f"Etut → +{artis:.0f} puan")
    if devamsizlik_azalt:
        senaryo_ort += 3
        senaryo_etki.append("Devamsizlik azalma → +3 puan")
    if ek_sinav > 0:
        senaryo_ort += ek_sinav * 0.8
        senaryo_etki.append(f"Ek sinav → +{ek_sinav * 0.8:.0f} puan")
    if odev_artir:
        senaryo_ort += 2
        senaryo_etki.append("Odev takip → +2 puan")

    senaryo_ort = round(min(100, max(0, senaryo_ort)), 1)

    if senaryo_etki:
        fark = senaryo_ort - tahmin_ort
        s_renk = "#10b981" if fark > 0 else "#ef4444"
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid {s_renk};border-radius:14px;
                    padding:16px;text-align:center;margin-top:12px;">
            <div style="font-size:10px;color:#94a3b8;">Senaryo Sonucu</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:8px 0;">
                <div><div style="font-size:10px;color:#64748b;">Mevcut Tahmin</div>
                    <div style="font-size:22px;font-weight:800;color:#7c3aed;">{tahmin_ort}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Senaryo</div>
                    <div style="font-size:22px;font-weight:800;color:{s_renk};">{senaryo_ort}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Fark</div>
                    <div style="font-size:22px;font-weight:800;color:{s_renk};">{'+'if fark>=0 else ''}{fark:.1f}</div></div>
            </div>
            <div style="font-size:10px;color:#94a3b8;margin-top:4px;">{' · '.join(senaryo_etki)}</div>
        </div>""", unsafe_allow_html=True)

    # AI tahmin
    st.divider()
    if st.button("AI Donem Sonu Projeksiyonu", key="at_ai_tahmin", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                veri = (f"Ogrenci: {len(students)}, Not Kaydi: {len(grades)}, Genel Ort: {mevcut_ort}, "
                        f"Trend: {'yukselis' if trend > 0 else 'dusus'} ({trend:.1f}), "
                        f"Devamsizlik: {toplam_dev}, Tahmin Ort: {tahmin_ort}, Kalan: {kalan_gun} gun")
                with st.spinner("AI tahmin hazirlaniyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir akademik analisti. Verilen verilere dayanarak donem sonu projeksiyonu yap: 1) Genel degerlendirme 2) Risk alanlari 3) Firsat alanlari 4) 5 somut mudahale onerisi. Turkce, somut."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=500, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Donem Sonu Projeksiyonu</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
