"""
Ogrenci 360 — MEGA Ozellikleri
=================================
1. Dijital Portfolyo + Basari Vitrinesi
2. Akilli Ogrenci Eslestirme + Buddy Sistemi
3. Ogrenci Gelecek Tahmini (Predictive Analytics)
"""
from __future__ import annotations

import os
import uuid
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        import json
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


# ============================================================
# 1. DİJİTAL PORTFOLYO + BAŞARI VİTRİNESİ
# ============================================================

def render_portfolyo(d: dict):
    """Ogrencinin tum basarilari tek vitrinde."""
    styled_section("Dijital Portfolyo", "#c9a84c")

    sid = d.get("sid", "")
    ad = d.get("name", "?")

    # Basari topla
    basarilar = []

    # Sertifikalar
    for s in d.get("sertifikalar", []):
        basarilar.append({"tip": "Sertifika", "ikon": "🏅", "renk": "#f59e0b",
                           "baslik": s.get("ad", s.get("baslik", "Sertifika")),
                           "tarih": (s.get("tarih", s.get("created_at", "")) or "")[:10]})

    # En iyi notlar (top 5)
    grades = d.get("grades", [])
    puanli = [g for g in grades if isinstance(g.get("puan"), (int, float))]
    puanli.sort(key=lambda g: -g.get("puan", 0))
    for g in puanli[:5]:
        if g.get("puan", 0) >= 80:
            basarilar.append({"tip": "Yuksek Not", "ikon": "⭐", "renk": "#10b981",
                               "baslik": f"{g.get('ders', '')}: {g.get('puan', '')}",
                               "tarih": (g.get("tarih", g.get("created_at", "")) or "")[:10]})

    # Kulup uyelikleri
    for k in d.get("kulup_uyelikleri", []):
        basarilar.append({"tip": "Kulup", "ikon": "🎭", "renk": "#7c3aed",
                           "baslik": k.get("kulup_adi", k.get("ad", "Kulup")),
                           "tarih": (k.get("created_at", "") or "")[:10]})

    # Gamification rozetler
    rozetler = d.get("gamification", {}).get("rozetler", d.get("rozetler", []))
    if isinstance(rozetler, list):
        for r in rozetler[:5]:
            basarilar.append({"tip": "Rozet", "ikon": "🏆", "renk": "#ea580c",
                               "baslik": r if isinstance(r, str) else r.get("ad", "Rozet"),
                               "tarih": ""})

    # Kutuphane
    odunc = d.get("kutuphane_odunc", [])
    if odunc:
        basarilar.append({"tip": "Okuma", "ikon": "📚", "renk": "#0891b2",
                           "baslik": f"{len(odunc)} kitap odunc aldi",
                           "tarih": ""})

    # XP
    xp = d.get("gamification", {}).get("xp", 0)
    if xp and isinstance(xp, (int, float)) and xp > 0:
        basarilar.append({"tip": "XP", "ikon": "💎", "renk": "#6366f1",
                           "baslik": f"{xp} XP puan topladi",
                           "tarih": ""})

    if not basarilar:
        styled_info_banner("Portfolyo icin basari verisi bulunamadi.", banner_type="info", icon="📋")
        return

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,#3e2723 100%);
                border:2px solid #c9a84c;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(201,168,76,0.25);text-align:center;">
        <div style="font-size:10px;color:#c9a84c;letter-spacing:3px;text-transform:uppercase;">Dijital Portfolyo</div>
        <div style="font-size:28px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;margin:6px 0;">
            {ad}</div>
        <div style="font-size:12px;color:#e8d48b;">{len(basarilar)} basari · {d.get('sinif', '')}-{d.get('sube', '')}</div>
    </div>""", unsafe_allow_html=True)

    # Vitrin kartlari
    cols = st.columns(3)
    for idx, b in enumerate(basarilar):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {b['renk']}30;border-top:3px solid {b['renk']};
                        border-radius:0 0 12px 12px;padding:12px;margin-bottom:8px;text-align:center;min-height:80px;">
                <div style="font-size:24px;margin-bottom:4px;">{b['ikon']}</div>
                <div style="font-size:11px;font-weight:700;color:#e2e8f0;">{b['baslik'][:40]}</div>
                <div style="font-size:9px;color:#64748b;margin-top:3px;">{b['tip']}{(' · ' + b['tarih']) if b['tarih'] else ''}</div>
            </div>""", unsafe_allow_html=True)

    # Tip dagilimi
    tip_sayac = Counter(b["tip"] for b in basarilar)
    styled_section("Basari Dagilimi")
    for tip, sayi in tip_sayac.most_common():
        st.markdown(f"- **{tip}**: {sayi}")


# ============================================================
# 2. BUDDY SİSTEMİ
# ============================================================

def render_buddy_sistemi(d: dict, students: dict):
    """Akran mentorluk eslestirme — guclü+zayif complementary."""
    styled_section("Buddy Eslestirme Sistemi", "#059669")

    sid = d.get("sid", "")
    ad = d.get("name", "?")
    grades = d.get("grades", [])

    if not grades:
        styled_info_banner("Eslestirme icin not verisi gerekli.", banner_type="info", icon="🤝")
        return

    ak = _ak_dir()
    tum_notlar = _lj(os.path.join(ak, "grades.json"))
    tum_ogrenciler = _lj(os.path.join(ak, "students.json"))
    aktif = [s for s in tum_ogrenciler if s.get("durum", "aktif") == "aktif" and s.get("id") != sid]

    if not aktif:
        styled_info_banner("Eslestirme icin baska ogrenci yok.", banner_type="info", icon="👤")
        return

    # Bu ogrencinin ders bazli ortalamalar
    ogr_dersler = {}
    for g in grades:
        if isinstance(g.get("puan"), (int, float)):
            ders = g.get("ders", "?")
            ogr_dersler.setdefault(ders, []).append(g["puan"])
    ogr_ders_ort = {d: round(sum(p) / len(p), 1) for d, p in ogr_dersler.items()}

    # Zayif dersler (< 60)
    zayif = {d: o for d, o in ogr_ders_ort.items() if o < 60}
    guclu = {d: o for d, o in ogr_ders_ort.items() if o >= 80}

    if not zayif:
        styled_info_banner(f"{ad}'in zayif dersi yok — buddy gerekmiyor!", banner_type="info", icon="🌟")
        return

    styled_info_banner(
        f"Zayif dersler: {', '.join(f'{d}({o})' for d, o in zayif.items())} · "
        f"Guclu dersler: {', '.join(f'{d}({o})' for d, o in guclu.items()) or 'Yok'}",
        banner_type="info", icon="📊")

    # Potansiyel buddy bul — zayif derslerimizde guclu olan
    buddy_adaylar = []
    for s in aktif[:100]:  # performans icin limit
        s_notlar = [n for n in tum_notlar if n.get("student_id") == s.get("id")
                      and isinstance(n.get("puan"), (int, float))]
        s_ders_ort = {}
        for n in s_notlar:
            ders = n.get("ders", "?")
            s_ders_ort.setdefault(ders, []).append(n["puan"])
        s_ders_ort = {d: round(sum(p) / len(p), 1) for d, p in s_ders_ort.items()}

        # Esleme skoru — zayif derslerimizde ne kadar guclu?
        skor = 0
        eslesen_dersler = []
        for ders, ogr_puan in zayif.items():
            buddy_puan = s_ders_ort.get(ders, 0)
            if buddy_puan >= 75:
                skor += (buddy_puan - ogr_puan)
                eslesen_dersler.append(f"{ders}({buddy_puan})")

        if skor > 0:
            buddy_adaylar.append({
                "ogrenci": s, "skor": round(skor),
                "eslesen": eslesen_dersler,
                "genel_ort": round(sum(s_ders_ort.values()) / max(len(s_ders_ort), 1), 1) if s_ders_ort else 0,
            })

    buddy_adaylar.sort(key=lambda x: -x["skor"])

    # Goster
    styled_section(f"En Uygun Buddy Adaylari ({len(buddy_adaylar)})")
    if not buddy_adaylar:
        styled_info_banner("Uygun buddy adayi bulunamadi.", banner_type="warning", icon="🤝")
    else:
        for sira, ba in enumerate(buddy_adaylar[:8], 1):
            s = ba["ogrenci"]
            madalya = {1: "🥇", 2: "🥈", 3: "🥉"}.get(sira, f"#{sira}")
            s_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
            s_sinif = f"{s.get('sinif', '')}-{s.get('sube', '')}"

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #05966940;border-radius:12px;
                        padding:12px 16px;margin-bottom:6px;display:flex;align-items:center;gap:14px;">
                <span style="font-size:22px;min-width:32px;text-align:center;">{madalya}</span>
                <div style="flex:1;">
                    <div style="font-weight:700;color:#e2e8f0;font-size:13px;">{s_ad}
                        <span style="color:#94a3b8;font-size:10px;margin-left:6px;">({s_sinif})</span></div>
                    <div style="font-size:10px;color:#6ee7b7;margin-top:2px;">
                        Guclu: {', '.join(ba['eslesen'][:4])}</div>
                    <div style="font-size:9px;color:#64748b;">Genel ort: {ba['genel_ort']}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:20px;font-weight:900;color:#059669;">{ba['skor']}</div>
                    <div style="font-size:8px;color:#94a3b8;">Uyum</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Karsilikli eslestirme onerisi
    if guclu and buddy_adaylar:
        styled_section("Karsilikli Buddy Onerisi")
        en_iyi = buddy_adaylar[0]
        st.markdown(f"""
        <div style="background:#052e16;border:2px solid #059669;border-radius:14px;
                    padding:16px;text-align:center;">
            <div style="font-size:13px;color:#6ee7b7;font-weight:700;margin-bottom:8px;">Onerilen Eslestirme</div>
            <div style="display:flex;justify-content:center;align-items:center;gap:20px;">
                <div>
                    <div style="font-size:14px;font-weight:800;color:#fff;">{ad}</div>
                    <div style="font-size:10px;color:#94a3b8;">Guclu: {', '.join(list(guclu.keys())[:3])}</div>
                </div>
                <div style="font-size:24px;color:#059669;">🤝</div>
                <div>
                    <div style="font-size:14px;font-weight:800;color:#fff;">
                        {en_iyi['ogrenci'].get('ad', '')} {en_iyi['ogrenci'].get('soyad', '')}</div>
                    <div style="font-size:10px;color:#94a3b8;">Guclu: {', '.join(en_iyi['eslesen'][:3])}</div>
                </div>
            </div>
            <div style="font-size:10px;color:#64748b;margin-top:8px;">Birbirlerinin zayif derslerinde destek olabilirler</div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. GELECEK TAHMİNİ (PREDİKTİF ANALİTİK)
# ============================================================

def render_gelecek_tahmini(d: dict):
    """Ogrencinin gelecek performansini tahmin et + senaryo."""
    styled_section("Gelecek Tahmini", "#f59e0b")

    grades = d.get("grades", [])
    devamsizlik = d.get("devamsizlik", [])
    risk = d.get("risk", {})
    ad = d.get("name", "?")

    puanli = [g for g in grades if isinstance(g.get("puan"), (int, float))]
    if len(puanli) < 3:
        styled_info_banner("Tahmin icin en az 3 not gerekli.", banner_type="info", icon="🔮")
        return

    # Not trendi (son 6 not ortalamasina gore)
    puanli.sort(key=lambda g: g.get("tarih", g.get("created_at", "")))
    son_puanlar = [g["puan"] for g in puanli[-6:]]
    ilk_yari = sum(son_puanlar[:len(son_puanlar)//2]) / max(len(son_puanlar)//2, 1)
    son_yari = sum(son_puanlar[len(son_puanlar)//2:]) / max(len(son_puanlar) - len(son_puanlar)//2, 1)
    trend = son_yari - ilk_yari  # pozitif = yukseliyor

    mevcut_ort = round(sum(son_puanlar) / len(son_puanlar), 1)

    # Yil sonu tahmini
    tahmin_ort = round(mevcut_ort + trend * 0.5, 1)  # conservative
    iyimser = round(tahmin_ort + abs(trend) * 0.8, 1)
    kotumser = round(tahmin_ort - abs(trend) * 0.8, 1)

    # Devamsizlik tahmini
    bugun = date.today()
    yil_basi = date(bugun.year if bugun.month >= 9 else bugun.year - 1, 9, 1)
    gecen_gun = max((bugun - yil_basi).days, 1)
    kalan_gun = max(180 - gecen_gun, 0)  # tahmini egitim yili 180 gun
    mevcut_dev = len(devamsizlik)
    gunluk_dev_oran = mevcut_dev / gecen_gun if gecen_gun > 0 else 0
    tahmin_dev = round(mevcut_dev + gunluk_dev_oran * kalan_gun)

    # Risk tahmini
    risk_skor = risk.get("skor", risk.get("risk_score", 30))
    if not isinstance(risk_skor, (int, float)):
        risk_skor = 30
    risk_trend_val = 0
    if trend < -5:
        risk_trend_val = 15  # not dususu riski artirir
    if gunluk_dev_oran > 0.1:
        risk_trend_val += 10  # yuksek devamsizlik
    tahmin_risk = min(100, round(risk_skor + risk_trend_val))

    t_renk = "#10b981" if tahmin_ort >= 70 else "#f59e0b" if tahmin_ort >= 50 else "#ef4444"

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#78350f 0%,#92400e 100%);
                border:2px solid #fbbf24;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(251,191,36,0.25);text-align:center;">
        <div style="font-size:10px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;">Yil Sonu Not Tahmini</div>
        <div style="font-size:56px;font-weight:900;color:{t_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{tahmin_ort}</div>
        <div style="font-size:12px;color:#fde68a;">
            Mevcut: {mevcut_ort} · Trend: {'↑' if trend > 0 else '↓'}{abs(trend):.1f}</div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:12px;">
                <div style="font-size:9px;color:#94a3b8;">Iyimser</div>
                <div style="font-size:24px;font-weight:900;color:#10b981;">{iyimser}</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:12px;border:1px solid #fbbf24;">
                <div style="font-size:9px;color:#fbbf24;">Gercekci</div>
                <div style="font-size:24px;font-weight:900;color:#fbbf24;">{tahmin_ort}</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:12px;">
                <div style="font-size:9px;color:#94a3b8;">Kotumser</div>
                <div style="font-size:24px;font-weight:900;color:#ef4444;">{kotumser}</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── DETAY TAHMİNLER ──
    styled_section("Detayli Tahminler")

    tahminler = [
        {"baslik": "Devamsizlik Yil Sonu", "mevcut": str(mevcut_dev), "tahmin": str(tahmin_dev),
         "renk": "#ef4444" if tahmin_dev > 20 else "#f59e0b" if tahmin_dev > 10 else "#10b981",
         "ikon": "📋", "yorum": f"Mevcut hiz devam ederse {kalan_gun} gunde +{tahmin_dev - mevcut_dev} gun daha"},
        {"baslik": "Risk Skoru Tahmini", "mevcut": str(round(risk_skor)), "tahmin": str(tahmin_risk),
         "renk": "#ef4444" if tahmin_risk >= 60 else "#f59e0b" if tahmin_risk >= 40 else "#10b981",
         "ikon": "⚠️", "yorum": "Not trendi ve devamsizlik baz alinarak hesaplandi"},
    ]

    for t in tahminler:
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {t['renk']}30;border-left:4px solid {t['renk']};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{t['ikon']} {t['baslik']}</span>
                <div style="display:flex;gap:10px;">
                    <span style="font-size:11px;color:#94a3b8;">Mevcut: <b>{t['mevcut']}</b></span>
                    <span style="font-size:11px;color:{t['renk']};font-weight:700;">Tahmin: <b>{t['tahmin']}</b></span>
                </div>
            </div>
            <div style="font-size:10px;color:#64748b;">{t['yorum']}</div>
        </div>""", unsafe_allow_html=True)

    # ── SENARYO SİMÜLASYONU ──
    styled_section("Senaryo Simulasyonu")
    st.caption("Parametreleri degistirin — etkiyi gorun:")

    col1, col2 = st.columns(2)
    with col1:
        ek_ders = st.slider("Haftalik Ek Ders (saat)", 0, 10, 0, key=f"o360_ek_{d.get('sid', '')}")
        devamsizlik_sifirla = st.checkbox("Devamsizligi sifirla", key=f"o360_dev0_{d.get('sid', '')}")
    with col2:
        kulup_katil = st.checkbox("Kulube katilsin", key=f"o360_kulup_{d.get('sid', '')}")
        rehberlik_gorsu = st.checkbox("Haftalik rehberlik", key=f"o360_reh_{d.get('sid', '')}")

    # Senaryo hesapla
    senaryo_not = tahmin_ort
    senaryo_risk = tahmin_risk
    senaryo_etki = []

    if ek_ders > 0:
        artis = ek_ders * 2.5
        senaryo_not += artis
        senaryo_risk -= ek_ders * 2
        senaryo_etki.append(f"Ek ders → +{artis:.0f} puan")
    if devamsizlik_sifirla:
        senaryo_not += 5
        senaryo_risk -= 15
        senaryo_etki.append("Devamsizlik sifir → +5 puan, risk -%15")
    if kulup_katil:
        senaryo_risk -= 8
        senaryo_etki.append("Kulup katilimi → risk -%8 (sosyal gelisim)")
    if rehberlik_gorsu:
        senaryo_not += 3
        senaryo_risk -= 10
        senaryo_etki.append("Haftalik rehberlik → +3 puan, risk -%10")

    senaryo_not = round(min(100, max(0, senaryo_not)), 1)
    senaryo_risk = round(min(100, max(0, senaryo_risk)))

    if senaryo_etki:
        s_renk = "#10b981" if senaryo_not > tahmin_ort else "#ef4444"
        fark = senaryo_not - tahmin_ort
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid {s_renk};border-radius:14px;
                    padding:16px;text-align:center;margin-top:12px;">
            <div style="font-size:10px;color:#94a3b8;">Senaryo Sonucu</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:8px 0;">
                <div><div style="font-size:10px;color:#64748b;">Mevcut Tahmin</div>
                    <div style="font-size:22px;font-weight:800;color:#f59e0b;">{tahmin_ort}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Senaryo</div>
                    <div style="font-size:22px;font-weight:800;color:{s_renk};">{senaryo_not}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Fark</div>
                    <div style="font-size:22px;font-weight:800;color:{s_renk};">{'+'if fark>=0 else ''}{fark:.1f}</div></div>
            </div>
            <div style="font-size:10px;color:#94a3b8;margin-top:4px;">
                Risk: {tahmin_risk} → {senaryo_risk} · Etkiler: {' · '.join(senaryo_etki)}</div>
        </div>""", unsafe_allow_html=True)

    # AI tahmin
    st.divider()
    if st.button("AI Gelecek Tahmini", key=f"o360_ai_tahmin_{d.get('sid', '')}", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                veri = (f"Ogrenci: {ad}, Sinif: {d.get('sinif', '')}-{d.get('sube', '')}\n"
                        f"Mevcut ort: {mevcut_ort}, Trend: {'yukselis' if trend > 0 else 'dusus'} ({trend:.1f})\n"
                        f"Devamsizlik: {mevcut_dev} (tahmin yil sonu: {tahmin_dev})\n"
                        f"Risk: {risk_skor}/100 (tahmin: {tahmin_risk})\n"
                        f"Kulup: {len(d.get('kulup_uyelikleri', []))}, Etkinlik: {len(d.get('etkinlik_katilimlari', []))}\n"
                        f"Son 6 not: {son_puanlar}")
                with st.spinner("AI tahmin hazirlaniyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir egitim analisti. Ogrenci verilerine dayanarak gelecek performans tahmini yap: 1) Yil sonu not tahmini 2) Risk degerlendirmesi 3) Guclu/zayif yonler 4) 3 somut oneri. Turkce, kisa."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=500, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:6px;">AI Gelecek Tahmini</div>
                        <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
