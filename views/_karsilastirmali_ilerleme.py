"""
Karşılaştırmalı İlerleme (Anonim)
======================================
"Çocuğunuz matematik'te sınıfın üst %25'inde, okulun üst %40'ında,
Türkiye ortalamasının üstünde." — Diğer öğrenci isimleri görünmez.
Gerçekçi bağlam + motivasyon.
"""
from __future__ import annotations

import statistics
from typing import Any

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# TÜRKİYE ORTALAMA VERİLERİ (MEB istatistikleri — örnek)
# ══════════════════════════════════════════════════════════════

TURKIYE_ORTALAMA = {
    "Matematik":       {"lise": 62, "ortaokul": 68, "ilkokul": 75},
    "Türkçe":          {"lise": 68, "ortaokul": 72, "ilkokul": 78},
    "Fen Bilimleri":   {"lise": 64, "ortaokul": 70, "ilkokul": 76},
    "Sosyal Bilgiler": {"lise": 66, "ortaokul": 71, "ilkokul": 77},
    "İngilizce":       {"lise": 58, "ortaokul": 64, "ilkokul": 72},
    "Fizik":           {"lise": 60},
    "Kimya":           {"lise": 61},
    "Biyoloji":        {"lise": 63},
    "Tarih":           {"lise": 68},
    "Coğrafya":        {"lise": 67},
    "Edebiyat":        {"lise": 69},
    "Geometri":        {"lise": 59},
}


def _get_kademe_from_sinif(sinif: int) -> str:
    """Sınıf numarasından kademe."""
    if sinif <= 4:
        return "ilkokul"
    if sinif <= 8:
        return "ortaokul"
    return "lise"


# ══════════════════════════════════════════════════════════════
# PERCENTILE HESAPLAMA
# ══════════════════════════════════════════════════════════════

def _percentile_rank(value: float, data: list[float]) -> float:
    """Bir değerin listedeki yüzdelik sırasını hesapla.

    Returns: 0-100 arası — üst yüzdelik (100 = en iyi)
    """
    if not data:
        return 50
    sorted_data = sorted(data)
    below = sum(1 for d in sorted_data if d < value)
    equal = sum(1 for d in sorted_data if d == value)
    pct = (below + 0.5 * equal) / len(sorted_data) * 100
    return round(pct, 1)


def _ust_yuzdelik(percentile: float) -> str:
    """Percentile'ı 'üst %X' formatına çevir."""
    ust = 100 - percentile
    if ust < 10:
        return f"üst %{ust:.0f}"
    elif ust < 25:
        return f"üst %{ust:.0f} içinde"
    elif ust < 50:
        return f"ortalamanın üstünde"
    elif ust < 75:
        return f"ortalama civarında"
    else:
        return f"geliştirilmesi gereken alanda"


def _yorum_uret(pct_sinif: float, pct_okul: float, turkiye_fark: float) -> tuple[str, str]:
    """Percentile'lardan yorum metni ve renk üret."""
    # Renk: yeşil >70, sarı 40-70, kırmızı <40
    avg = (pct_sinif + pct_okul) / 2
    if avg >= 80:
        renk = "#059669"
        yorum = "🌟 **Harika!** Çocuğunuz bu derste üst düzeyde başarılı."
    elif avg >= 60:
        renk = "#0284C7"
        yorum = "👍 **İyi gidiyor.** Çocuğunuz bu derste başarılı."
    elif avg >= 40:
        renk = "#D97706"
        yorum = "📚 **Orta düzeyde.** Biraz daha çalışma ile yükselebilir."
    else:
        renk = "#DC2626"
        yorum = "⚠️ **Gelişim alanı.** Bu derste ek destek faydalı olacaktır."

    if turkiye_fark >= 10:
        yorum += f"\n\n🇹🇷 Türkiye ortalamasının **{turkiye_fark:+.0f}** puan üstünde."
    elif turkiye_fark <= -10:
        yorum += f"\n\n🇹🇷 Türkiye ortalamasının **{turkiye_fark:+.0f}** puan altında."

    return yorum, renk


# ══════════════════════════════════════════════════════════════
# KARŞILAŞTIRMA HESAPLAMA
# ══════════════════════════════════════════════════════════════

def calculate_student_comparison(student, all_students, all_grades) -> dict:
    """Öğrencinin sınıf, okul, Türkiye ile karşılaştırmasını hesapla."""
    result = {
        "ogrenci": {
            "id": student.id,
            "ad": student.tam_ad,
            "sinif": student.sinif,
            "sube": getattr(student, "sube", ""),
        },
        "dersler": [],
        "genel_ozet": {},
    }

    # Öğrencinin notlarını topla (ders bazlı ortalama)
    ogr_ders_notlar: dict[str, list[float]] = {}
    for g in all_grades:
        if str(g.student_id if hasattr(g, 'student_id') else g.get('student_id', '')) == str(student.id):
            ders = g.ders if hasattr(g, 'ders') else g.get('ders', '')
            try:
                puan = float(g.not_degeri if hasattr(g, 'not_degeri') else g.get('puan', 0))
            except Exception:
                continue
            if ders and puan > 0:
                ogr_ders_notlar.setdefault(ders, []).append(puan)

    if not ogr_ders_notlar:
        return result

    # Sınıf arkadaşlarının notlarını topla (aynı sınıf+şube)
    sinif_arkadas_ids = {s.id for s in all_students
                          if s.sinif == student.sinif and s.sube == getattr(student, "sube", "")}
    # Okul (tüm sınıf aynı seviye)
    okul_ayni_sinif_ids = {s.id for s in all_students if s.sinif == student.sinif}

    kademe = _get_kademe_from_sinif(student.sinif)

    # Her ders için karşılaştırma
    for ders, ogr_puanlar in ogr_ders_notlar.items():
        ogr_ort = round(sum(ogr_puanlar) / len(ogr_puanlar), 1)

        # Sınıf notları (bu ders, aynı sınıf+şube)
        sinif_ortlar = []
        for sid in sinif_arkadas_ids:
            sid_str = str(sid)
            sid_puanlar = []
            for g in all_grades:
                g_sid = str(g.student_id if hasattr(g, 'student_id') else g.get('student_id', ''))
                g_ders = g.ders if hasattr(g, 'ders') else g.get('ders', '')
                if g_sid == sid_str and g_ders == ders:
                    try:
                        p = float(g.not_degeri if hasattr(g, 'not_degeri') else g.get('puan', 0))
                        if p > 0:
                            sid_puanlar.append(p)
                    except Exception:
                        continue
            if sid_puanlar:
                sinif_ortlar.append(sum(sid_puanlar) / len(sid_puanlar))

        # Okul (aynı sınıf seviyesi, farklı şubeler)
        okul_ortlar = []
        for sid in okul_ayni_sinif_ids:
            sid_str = str(sid)
            sid_puanlar = []
            for g in all_grades:
                g_sid = str(g.student_id if hasattr(g, 'student_id') else g.get('student_id', ''))
                g_ders = g.ders if hasattr(g, 'ders') else g.get('ders', '')
                if g_sid == sid_str and g_ders == ders:
                    try:
                        p = float(g.not_degeri if hasattr(g, 'not_degeri') else g.get('puan', 0))
                        if p > 0:
                            sid_puanlar.append(p)
                    except Exception:
                        continue
            if sid_puanlar:
                okul_ortlar.append(sum(sid_puanlar) / len(sid_puanlar))

        # Türkiye ortalaması
        trkiye_ort = TURKIYE_ORTALAMA.get(ders, {}).get(kademe, None)

        # Percentile
        pct_sinif = _percentile_rank(ogr_ort, sinif_ortlar) if sinif_ortlar else 50
        pct_okul = _percentile_rank(ogr_ort, okul_ortlar) if okul_ortlar else 50

        sinif_ort_val = round(sum(sinif_ortlar) / len(sinif_ortlar), 1) if sinif_ortlar else None
        okul_ort_val = round(sum(okul_ortlar) / len(okul_ortlar), 1) if okul_ortlar else None

        turkiye_fark = (ogr_ort - trkiye_ort) if trkiye_ort else 0

        yorum, renk = _yorum_uret(pct_sinif, pct_okul, turkiye_fark)

        result["dersler"].append({
            "ders": ders,
            "ogrenci_ort": ogr_ort,
            "sinif_ort": sinif_ort_val,
            "okul_ort": okul_ort_val,
            "turkiye_ort": trkiye_ort,
            "pct_sinif": pct_sinif,
            "pct_okul": pct_okul,
            "sinif_rank_text": _ust_yuzdelik(pct_sinif),
            "okul_rank_text": _ust_yuzdelik(pct_okul),
            "turkiye_fark": turkiye_fark,
            "yorum": yorum,
            "renk": renk,
        })

    # Genel özet — tüm derslerin ortalaması
    if result["dersler"]:
        result["genel_ozet"] = {
            "not_ort": round(statistics.mean([d["ogrenci_ort"] for d in result["dersler"]]), 1),
            "ort_sinif_pct": round(statistics.mean([d["pct_sinif"] for d in result["dersler"]]), 1),
            "ort_okul_pct": round(statistics.mean([d["pct_okul"] for d in result["dersler"]]), 1),
            "ders_sayisi": len(result["dersler"]),
        }

    return result


# ══════════════════════════════════════════════════════════════
# UI — Karşılaştırmalı Rapor
# ══════════════════════════════════════════════════════════════

def render_karsilastirmali_ilerleme(student=None):
    """Karşılaştırmalı ilerleme raporu — bir öğrenci için tam analiz."""
    styled_section("📊 Karşılaştırmalı İlerleme (Anonim)", "#4F46E5")

    styled_info_banner(
        "Çocuğunuzun sınıf, okul ve Türkiye ortalaması ile karşılaştırmalı durumu. "
        "**Diğer öğrenci isimleri görünmez.** Sadece istatistiksel pozisyon gösterilir.",
        "info", "📊",
    )

    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        all_students = ak.get_students(durum="aktif")
        all_grades = ak.get_grades()
    except Exception as e:
        st.error(f"Veri yüklenemedi: {e}")
        return

    if not all_students:
        styled_info_banner("Öğrenci verisi bulunamadı.", "warning")
        return

    # Öğrenci seçimi
    if student is None:
        names = [f"{s.tam_ad} ({s.sinif}/{s.sube})" for s in all_students]
        sel_idx = st.selectbox("Öğrenci seç", range(len(all_students)),
                                format_func=lambda i: names[i], key="_kri_sel_widget")
        student = all_students[sel_idx]

    # Hesapla
    result = calculate_student_comparison(student, all_students, all_grades)

    if not result["dersler"]:
        styled_info_banner(
            "Bu öğrenci için yeterli not verisi yok. Karşılaştırma için önce notları girin.",
            "warning",
        )
        return

    # Hero özet kart
    genel = result["genel_ozet"]
    ort = genel.get("not_ort", 0)
    sinif_pct = genel.get("ort_sinif_pct", 50)
    okul_pct = genel.get("ort_okul_pct", 50)

    # Renk
    if sinif_pct >= 75:
        hero_renk = "#059669"
        hero_ikon = "🌟"
    elif sinif_pct >= 50:
        hero_renk = "#0284C7"
        hero_ikon = "👍"
    elif sinif_pct >= 25:
        hero_renk = "#D97706"
        hero_ikon = "📚"
    else:
        hero_renk = "#DC2626"
        hero_ikon = "💪"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{hero_renk}30,{hero_renk}10);
    border:2px solid {hero_renk}60;border-radius:16px;padding:24px;margin:16px 0;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:0.82rem;color:#94A3B8;letter-spacing:2px;text-transform:uppercase;">
                    Genel Karşılaştırmalı Durum
                </div>
                <div style="font-size:1.8rem;font-weight:800;color:{hero_renk};margin-top:4px;">
                    {hero_ikon} Not Ort. {ort}
                </div>
                <div style="font-size:0.95rem;color:#E4E4E7;margin-top:8px;line-height:1.7;">
                    📊 Sınıfınızın <strong>{_ust_yuzdelik(sinif_pct)}</strong><br/>
                    🏫 Okulun <strong>{_ust_yuzdelik(okul_pct)}</strong>
                </div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:3rem;font-weight:900;color:{hero_renk};">
                    {sinif_pct:.0f}
                </div>
                <div style="font-size:0.72rem;color:#94A3B8;letter-spacing:1.5px;">
                    SINIF YÜZDELİĞİ
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ders bazlı detay
    styled_section("📚 Ders Bazlı Karşılaştırma", "#7C3AED")

    for d in sorted(result["dersler"], key=lambda x: -x["pct_sinif"]):
        pct_s = d["pct_sinif"]
        pct_o = d["pct_okul"]
        ogr_ort = d["ogrenci_ort"]
        sinif_ort = d["sinif_ort"]
        okul_ort = d["okul_ort"]
        trkiye = d["turkiye_ort"]

        # Görsel bar
        bar_width_sinif = min(100, max(0, pct_s))
        bar_width_okul = min(100, max(0, pct_o))

        renk = d["renk"]

        with st.expander(f"📖 **{d['ders']}** — Notun: {ogr_ort} · {_ust_yuzdelik(pct_s)}"):
            # Percentile barları
            st.markdown(f"""
            <div style="margin:12px 0;">
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:4px;">
                    <span style="color:#94A3B8;">Sınıf İçi</span>
                    <span style="color:{renk};font-weight:700;">Üst %{100-pct_s:.0f} ({pct_s:.0f}. yüzdelik)</span>
                </div>
                <div style="background:#18181B;border-radius:8px;height:14px;overflow:hidden;">
                    <div style="width:{bar_width_sinif}%;height:100%;background:{renk};border-radius:8px;"></div>
                </div>
            </div>
            <div style="margin:12px 0;">
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:4px;">
                    <span style="color:#94A3B8;">Okul Geneli</span>
                    <span style="color:{renk};font-weight:700;">Üst %{100-pct_o:.0f} ({pct_o:.0f}. yüzdelik)</span>
                </div>
                <div style="background:#18181B;border-radius:8px;height:14px;overflow:hidden;">
                    <div style="width:{bar_width_okul}%;height:100%;background:{renk};border-radius:8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Karşılaştırma tablosu
            cols = st.columns(4)
            with cols[0]:
                st.metric("Öğrenci", f"{ogr_ort}")
            with cols[1]:
                if sinif_ort is not None:
                    fark = ogr_ort - sinif_ort
                    st.metric("Sınıf Ort.", f"{sinif_ort}", f"{fark:+.1f}")
            with cols[2]:
                if okul_ort is not None:
                    fark = ogr_ort - okul_ort
                    st.metric("Okul Ort.", f"{okul_ort}", f"{fark:+.1f}")
            with cols[3]:
                if trkiye is not None:
                    fark = ogr_ort - trkiye
                    st.metric("🇹🇷 Türkiye", f"{trkiye}", f"{fark:+.1f}")

            # Yorum
            st.markdown(f"""
            <div style="background:{renk}20;border-left:4px solid {renk};
            border-radius:0 12px 12px 0;padding:12px 16px;margin-top:12px;">
                <div style="color:#E4E4E7;font-size:0.9rem;line-height:1.6;">
                    {d['yorum']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Genel öneri
    st.divider()
    styled_section("💡 Öneriler", "#EC4899")

    # En güçlü ve zayıf ders
    dersler_sorted = sorted(result["dersler"], key=lambda x: -x["pct_sinif"])
    en_iyi = dersler_sorted[0]
    en_zor = dersler_sorted[-1]

    st.markdown(f"""
    <div style="background:#059669 20;border-left:4px solid #059669;
    border-radius:0 12px 12px 0;padding:12px 16px;margin:8px 0;">
        <div style="font-weight:700;color:#059669;">🌟 Güçlü Yan: {en_iyi['ders']}</div>
        <div style="color:#E4E4E7;font-size:0.88rem;margin-top:4px;">
            Bu derste sınıfın {en_iyi['sinif_rank_text']}. Başarısını sürdür!
        </div>
    </div>

    <div style="background:#D97706 20;border-left:4px solid #D97706;
    border-radius:0 12px 12px 0;padding:12px 16px;margin:8px 0;">
        <div style="font-weight:700;color:#D97706;">📚 Gelişim Alanı: {en_zor['ders']}</div>
        <div style="color:#E4E4E7;font-size:0.88rem;margin-top:4px;">
            Bu derste ek destek çalışması faydalı olacaktır.
            Öğretmenden etüt veya ödev planı isteyebilirsiniz.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TOPLU LİSTE — Tüm öğrencilerin percentile listesi
# ══════════════════════════════════════════════════════════════

def render_sinif_percentile_listesi():
    """Tüm öğrencileri percentile'a göre listele (öğretmen görünümü)."""
    styled_section("📊 Sınıf Percentile Listesi", "#4F46E5")

    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        all_students = ak.get_students(durum="aktif")
        all_grades = ak.get_grades()
    except Exception:
        all_students = []
        all_grades = []

    if not all_students:
        styled_info_banner("Öğrenci bulunamadı.", "warning")
        return

    # Sınıf filtresi
    siniflar = sorted(set(f"{s.sinif}/{s.sube}" for s in all_students if s.sube))
    sel_sinif = st.selectbox("Sınıf", ["Tümü"] + siniflar, key="_kri_sinif_widget")

    filtered = all_students
    if sel_sinif != "Tümü":
        sinif, sube = sel_sinif.split("/")
        filtered = [s for s in all_students if s.sinif == int(sinif) and s.sube == sube]

    # Her öğrenci için hesapla
    sonuclar = []
    for s in filtered:
        r = calculate_student_comparison(s, all_students, all_grades)
        if r["genel_ozet"]:
            sonuclar.append({
                "ad": s.tam_ad,
                "sinif": f"{s.sinif}/{s.sube}",
                "not_ort": r["genel_ozet"].get("not_ort", 0),
                "sinif_pct": r["genel_ozet"].get("ort_sinif_pct", 50),
                "okul_pct": r["genel_ozet"].get("ort_okul_pct", 50),
                "ders_sayisi": r["genel_ozet"].get("ders_sayisi", 0),
            })

    if not sonuclar:
        styled_info_banner("Not verisi yeterli değil.", "info")
        return

    # Sırala
    sonuclar.sort(key=lambda x: -x["sinif_pct"])

    # Tablo
    for i, r in enumerate(sonuclar, 1):
        pct = r["sinif_pct"]
        renk = "#059669" if pct >= 75 else ("#0284C7" if pct >= 50 else ("#D97706" if pct >= 25 else "#DC2626"))
        st.markdown(f"""
        <div style="background:#18181B;border-left:3px solid {renk};border-radius:8px;
        padding:10px 16px;margin:4px 0;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="color:#94A3B8;font-weight:600;">#{i}</span>
                <strong style="color:#FAFAFA;margin-left:8px;">{r['ad']}</strong>
                <span style="color:#94A3B8;font-size:0.78rem;margin-left:8px;">({r['sinif']})</span>
            </div>
            <div style="text-align:right;">
                <span style="color:{renk};font-weight:800;font-size:1.1rem;">{r['not_ort']}</span>
                <span style="color:#94A3B8;font-size:0.78rem;margin-left:8px;">Üst %{100-pct:.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
