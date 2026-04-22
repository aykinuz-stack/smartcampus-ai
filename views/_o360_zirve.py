"""
Ogrenci 360 — Zirve Ozellikleri
==================================
1. Benchmark Karsilastirma (ogrenci vs sinif vs okul)
2. Gelisim Yolculugu + Milestone Takibi
3. Akilli Mudahale Onerici (AI Intervention Recommender)
"""
from __future__ import annotations

import os
from collections import Counter
from datetime import date, datetime

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
# 1. BENCHMARK KARŞILAŞTIRMA
# ============================================================

def render_benchmark(d: dict, students: dict):
    """Ogrenci vs sinif vs okul ortalamasi karsilastirmasi."""
    styled_section("Benchmark Karsilastirma", "#2563eb")

    grades = d.get("grades", [])
    sid = d.get("sid", "")
    sinif = d.get("sinif", "")
    sube = d.get("sube", "")

    if not grades:
        styled_info_banner("Not verisi yok — benchmark icin en az 1 not gerekli.", banner_type="info", icon="📊")
        return

    # Ogrenci not ortalamasi
    puanlar = [g.get("puan", 0) for g in grades if isinstance(g.get("puan"), (int, float))]
    ogr_ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0

    # Tum notlar (sinif + okul ortalamasi icin)
    ak = _ak_dir()
    tum_notlar = _lj(os.path.join(ak, "grades.json"))
    tum_ogrenciler = _lj(os.path.join(ak, "students.json"))

    # Sinif ortalamasi
    sinif_notlar = [n for n in tum_notlar
                      if str(n.get("sinif", "")) == str(sinif) and n.get("sube", "") == sube
                      and isinstance(n.get("puan"), (int, float))]
    sinif_ort = round(sum(n["puan"] for n in sinif_notlar) / max(len(sinif_notlar), 1), 1) if sinif_notlar else 0

    # Okul ortalamasi
    okul_puanlar = [n["puan"] for n in tum_notlar if isinstance(n.get("puan"), (int, float))]
    okul_ort = round(sum(okul_puanlar) / max(len(okul_puanlar), 1), 1) if okul_puanlar else 0

    # Percentile hesapla
    aktif_ogr = [s for s in tum_ogrenciler if s.get("durum", "aktif") == "aktif"]
    ogr_ortalamalar = []
    for s in aktif_ogr:
        s_notlar = [n["puan"] for n in tum_notlar if n.get("student_id") == s.get("id")
                      and isinstance(n.get("puan"), (int, float))]
        if s_notlar:
            ogr_ortalamalar.append(sum(s_notlar) / len(s_notlar))
    ogr_ortalamalar.sort()
    percentile = 0
    if ogr_ortalamalar:
        alt = sum(1 for o in ogr_ortalamalar if o < ogr_ort)
        percentile = round(alt / len(ogr_ortalamalar) * 100)

    # Devamsizlik karsilastirma
    devamsizlik = d.get("devamsizlik", [])
    ogr_dev = len(devamsizlik)
    sinif_dev_all = [n for n in _lj(os.path.join(ak, "attendance.json"))
                       if str(n.get("sinif", "")) == str(sinif) and n.get("sube", "") == sube]
    sinif_ogr_ids = set(n.get("student_id") for n in sinif_dev_all)
    sinif_dev_ort = round(len(sinif_dev_all) / max(len(sinif_ogr_ids), 1), 1) if sinif_ogr_ids else 0

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                border:2px solid #6366f1;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(99,102,241,0.25);">
        <div style="text-align:center;margin-bottom:16px;">
            <div style="font-size:10px;color:#a5b4fc;letter-spacing:3px;text-transform:uppercase;">Dilim Pozisyonu</div>
            <div style="font-size:56px;font-weight:900;color:#6366f1;
                        font-family:Playfair Display,Georgia,serif;line-height:1;margin:4px 0;">%{percentile}</div>
            <div style="font-size:12px;color:#a5b4fc;">{d.get('name', '')} okulun en iyi %{100-percentile} diliminde</div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:14px;text-align:center;
                        border:2px solid #6366f1;">
                <div style="font-size:9px;color:#a5b4fc;">Ogrenci</div>
                <div style="font-size:28px;font-weight:900;color:#6366f1;">{ogr_ort}</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:14px;text-align:center;">
                <div style="font-size:9px;color:#94a3b8;">Sinif Ort.</div>
                <div style="font-size:28px;font-weight:900;color:#f59e0b;">{sinif_ort}</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:14px;text-align:center;">
                <div style="font-size:9px;color:#94a3b8;">Okul Ort.</div>
                <div style="font-size:28px;font-weight:900;color:#94a3b8;">{okul_ort}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── DERS BAZLI KARŞILAŞTIRMA ──
    styled_section("Ders Bazli Karsilastirma")
    ders_grp = {}
    for g in grades:
        ders = g.get("ders", "?")
        if isinstance(g.get("puan"), (int, float)):
            ders_grp.setdefault(ders, []).append(g["puan"])

    for ders, puanlar_d in sorted(ders_grp.items()):
        ogr_d_ort = round(sum(puanlar_d) / len(puanlar_d), 1)
        # Sinif ortalamasi bu dersde
        sinif_d = [n["puan"] for n in sinif_notlar if n.get("ders") == ders and isinstance(n.get("puan"), (int, float))]
        sinif_d_ort = round(sum(sinif_d) / max(len(sinif_d), 1), 1) if sinif_d else 0
        # Okul
        okul_d = [n["puan"] for n in tum_notlar if n.get("ders") == ders and isinstance(n.get("puan"), (int, float))]
        okul_d_ort = round(sum(okul_d) / max(len(okul_d), 1), 1) if okul_d else 0

        fark = ogr_d_ort - sinif_d_ort
        renk = "#10b981" if fark >= 5 else "#f59e0b" if fark >= -5 else "#ef4444"
        fark_txt = f"+{fark:.0f}" if fark >= 0 else f"{fark:.0f}"

        max_val = max(ogr_d_ort, sinif_d_ort, okul_d_ort, 1)
        st.markdown(f"""
        <div style="margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
                <span style="font-size:12px;color:#e2e8f0;font-weight:700;">{ders}</span>
                <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:10px;font-weight:700;">{fark_txt}</span>
            </div>
            <div style="display:flex;gap:3px;height:14px;">
                <div style="flex:{ogr_d_ort / max_val};background:#6366f1;border-radius:3px;
                            display:flex;align-items:center;padding-left:4px;">
                    <span style="font-size:8px;color:#fff;font-weight:700;">{ogr_d_ort}</span></div>
                <div style="flex:{sinif_d_ort / max_val};background:#f59e0b;border-radius:3px;
                            display:flex;align-items:center;padding-left:4px;">
                    <span style="font-size:8px;color:#fff;font-weight:700;">{sinif_d_ort}</span></div>
                <div style="flex:{okul_d_ort / max_val};background:#64748b;border-radius:3px;
                            display:flex;align-items:center;padding-left:4px;">
                    <span style="font-size:8px;color:#fff;font-weight:700;">{okul_d_ort}</span></div>
            </div>
            <div style="display:flex;gap:8px;font-size:8px;color:#64748b;margin-top:2px;">
                <span>🟣 Ogrenci</span><span>🟡 Sinif</span><span>⚫ Okul</span></div>
        </div>""", unsafe_allow_html=True)

    # Devamsizlik karsilastirma
    styled_section("Devamsizlik Karsilastirma")
    dev_renk = "#10b981" if ogr_dev < sinif_dev_ort else "#ef4444"
    st.markdown(f"""
    <div style="display:flex;gap:16px;justify-content:center;">
        <div style="text-align:center;background:#0f172a;border:2px solid #6366f1;border-radius:12px;padding:12px 20px;">
            <div style="font-size:24px;font-weight:900;color:{dev_renk};">{ogr_dev}</div>
            <div style="font-size:9px;color:#94a3b8;">Ogrenci</div></div>
        <div style="text-align:center;background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:12px 20px;">
            <div style="font-size:24px;font-weight:900;color:#f59e0b;">{sinif_dev_ort}</div>
            <div style="font-size:9px;color:#94a3b8;">Sinif Ort.</div></div>
    </div>""", unsafe_allow_html=True)


# ============================================================
# 2. GELİŞİM YOLCULUĞU + MİLESTONE
# ============================================================

def render_gelisim_yolculugu(d: dict):
    """Kronolojik gelisim timeline + milestone kartlari."""
    styled_section("Gelisim Yolculugu", "#7c3aed")

    # Timeline olaylari topla
    olaylar = []

    # Kayit
    kayit_t = d.get("kayit_tarihi", "")
    if kayit_t:
        olaylar.append({"tarih": kayit_t[:10], "tip": "Kayit", "ikon": "📝",
                         "detay": f"Okula kayit — {d.get('sinif', '')}/{d.get('sube', '')}", "renk": "#6366f1"})

    # Notlar (onemli donusum noktalari)
    grades = d.get("grades", [])
    if grades:
        puanlar = [g for g in grades if isinstance(g.get("puan"), (int, float))]
        puanlar.sort(key=lambda g: g.get("tarih", g.get("created_at", "")))
        # Ilk not
        if puanlar:
            ilk = puanlar[0]
            olaylar.append({"tarih": (ilk.get("tarih", ilk.get("created_at", "")) or "")[:10], "tip": "Ilk Not",
                             "ikon": "📊", "detay": f"{ilk.get('ders', '')}: {ilk.get('puan', '')}", "renk": "#10b981"})
            # En yuksek not
            en_yuksek = max(puanlar, key=lambda g: g.get("puan", 0))
            olaylar.append({"tarih": (en_yuksek.get("tarih", en_yuksek.get("created_at", "")) or "")[:10], "tip": "En Yuksek",
                             "ikon": "🏆", "detay": f"{en_yuksek.get('ders', '')}: {en_yuksek.get('puan', '')}", "renk": "#f59e0b"})

    # Rehberlik vakalari
    for v in d.get("vakalar", [])[:5]:
        olaylar.append({"tarih": (v.get("tarih", v.get("created_at", "")) or "")[:10], "tip": "Rehberlik",
                         "ikon": "🧠", "detay": v.get("konu", v.get("vaka_basligi", "Gorusme")), "renk": "#7c3aed"})

    # Risk degisiklikleri
    risk_trend = d.get("trend", {}).get("risk_trend", [])
    for r in risk_trend:
        if r.get("skor", 0) >= 60:
            olaylar.append({"tarih": r.get("tarih", "")[:10], "tip": "Risk Uyari",
                             "ikon": "⚠️", "detay": f"Risk: {r.get('skor', '')}/100 ({r.get('seviye', '')})", "renk": "#ef4444"})

    # Mudahaleler
    for m in d.get("mudahaleler", [])[:3]:
        olaylar.append({"tarih": (m.get("tarih", m.get("created_at", "")) or "")[:10], "tip": "Mudahale",
                         "ikon": "💊", "detay": m.get("baslik", m.get("mudahale_turu", ""))[:60], "renk": "#0891b2"})

    # Sertifikalar
    for s in d.get("sertifikalar", [])[:3]:
        olaylar.append({"tarih": (s.get("tarih", s.get("created_at", "")) or "")[:10], "tip": "Sertifika",
                         "ikon": "🏅", "detay": s.get("ad", s.get("baslik", ""))[:40], "renk": "#f59e0b"})

    # Sirala
    olaylar = [o for o in olaylar if o["tarih"]]
    olaylar.sort(key=lambda x: x["tarih"])

    if not olaylar:
        styled_info_banner("Yolculuk verisi yetersiz.", banner_type="info", icon="🗺️")
        return

    # Timeline
    for i, o in enumerate(olaylar):
        bekleme = ""
        if i > 0:
            try:
                onceki = date.fromisoformat(olaylar[i-1]["tarih"])
                simdi = date.fromisoformat(o["tarih"])
                gun = (simdi - onceki).days
                if gun > 0:
                    bekleme = f'<span style="font-size:9px;color:#64748b;margin-left:8px;">{gun}g sonra</span>'
            except Exception:
                pass

        st.markdown(f"""
        <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:2px;">
            <div style="display:flex;flex-direction:column;align-items:center;min-width:30px;">
                <div style="width:14px;height:14px;border-radius:50%;background:{o['renk']};
                            border:2px solid {o['renk']};"></div>
                {'<div style="width:2px;height:20px;background:#334155;"></div>' if i < len(olaylar) - 1 else ''}
            </div>
            <div style="flex:1;padding-bottom:6px;">
                <div style="display:flex;align-items:center;gap:6px;">
                    <span style="font-size:12px;">{o['ikon']}</span>
                    <span style="font-size:11px;font-weight:700;color:{o['renk']};">{o['tip']}</span>
                    <span style="font-size:10px;color:#64748b;">{o['tarih']}</span>
                    {bekleme}
                </div>
                <div style="font-size:10px;color:#94a3b8;margin-top:1px;">{o['detay']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Milestone ozet
    toplam_gun = 0
    if olaylar:
        try:
            toplam_gun = (date.fromisoformat(olaylar[-1]["tarih"]) - date.fromisoformat(olaylar[0]["tarih"])).days
        except Exception:
            pass

    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid #7c3aed40;border-radius:12px;padding:12px;
                text-align:center;margin-top:8px;">
        <span style="font-size:11px;color:#94a3b8;">{len(olaylar)} olay · {toplam_gun} gun · {d.get('name', '')}</span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# 3. AKILLI MÜDAHALE ÖNERİCİ
# ============================================================

def render_mudahale_onerici(d: dict):
    """AI ile otomatik mudahale onerisi — tespit + oneri + aksiyon."""
    styled_section("Akilli Mudahale Onerici", "#ef4444")

    onerileri = []

    # 1. Not dususu
    grades = d.get("grades", [])
    if grades:
        puanlar = [g for g in grades if isinstance(g.get("puan"), (int, float))]
        puanlar.sort(key=lambda g: g.get("tarih", g.get("created_at", "")))
        if len(puanlar) >= 3:
            son3 = [p["puan"] for p in puanlar[-3:]]
            if son3[-1] < son3[0] - 10:
                ders = puanlar[-1].get("ders", "?")
                onerileri.append({
                    "seviye": "yuksek", "ikon": "📉",
                    "sorun": f"{ders} dersinde son 3 notta dusus ({son3[0]}→{son3[-1]})",
                    "oneri": f"{ders} icin etut/destek dersi planlayin",
                    "sorumlu": "Ders Ogretmeni", "aksiyon": "Etut kaydet",
                })

    # 2. Devamsizlik
    devamsizlik = d.get("devamsizlik", [])
    son_30g = (date.today() - __import__('datetime').timedelta(days=30)).isoformat()
    son_devamsiz = sum(1 for dv in devamsizlik if (dv.get("tarih", "") or "") >= son_30g)
    if son_devamsiz >= 5:
        onerileri.append({
            "seviye": "acil", "ikon": "📋",
            "sorun": f"Son 30 gunde {son_devamsiz} devamsizlik kaydi",
            "oneri": "Veli gorusmesi planlayin, devamsizlik nedenini arastirin",
            "sorumlu": "Sinif Ogretmeni + Rehberlik", "aksiyon": "Veli arama",
        })

    # 3. Risk skoru
    risk = d.get("risk", {})
    risk_skor = risk.get("skor", risk.get("risk_score", 0))
    risk_seviye = risk.get("seviye", risk.get("risk_level", ""))
    if isinstance(risk_skor, (int, float)) and risk_skor >= 60:
        onerileri.append({
            "seviye": "acil", "ikon": "⚠️",
            "sorun": f"Risk skoru {risk_skor}/100 ({risk_seviye}) — yuksek",
            "oneri": "Rehberlik gorusmesi acil planlayin",
            "sorumlu": "Rehberlik", "aksiyon": "Rehberlige yonlendir",
        })

    # 4. Sosyal izolasyon
    kulupler = d.get("kulup_uyelikleri", [])
    etkinlikler = d.get("etkinlik_katilimlari", [])
    if not kulupler and not etkinlikler:
        onerileri.append({
            "seviye": "normal", "ikon": "🎭",
            "sorun": "Hicbir kulube uye degil, etkinlige katilmamis",
            "oneri": "Sosyal aktiviteye yonlendirin — ilgi alanina uygun kulup onerin",
            "sorumlu": "Sinif Ogretmeni", "aksiyon": "Kulup onerisi",
        })

    # 5. YD gerileme
    yd_results = d.get("yd_results", [])
    if yd_results and len(yd_results) >= 2:
        son_yd = yd_results[-1].get("score", yd_results[-1].get("puan", 0))
        onceki_yd = yd_results[-2].get("score", yd_results[-2].get("puan", 0))
        if isinstance(son_yd, (int, float)) and isinstance(onceki_yd, (int, float)) and son_yd < onceki_yd - 10:
            onerileri.append({
                "seviye": "yuksek", "ikon": "🌐",
                "sorun": f"Yabanci dil performansi dusus ({onceki_yd}→{son_yd})",
                "oneri": "Ek YD dersi veya adaptif ogrenme programi baslatin",
                "sorumlu": "YD Ogretmeni", "aksiyon": "AI Bireysel plan",
            })

    # 6. Kutuphane kullanim eksikligi
    kutuphane = d.get("kutuphane_odunc", [])
    if not kutuphane:
        onerileri.append({
            "seviye": "dusuk", "ikon": "📚",
            "sorun": "Kutuphane hic kullanilmamis — odunc kitap yok",
            "oneri": "Okuma alistirmasi onerin, kutuphane yonlendirmesi yapin",
            "sorumlu": "Sinif Ogretmeni", "aksiyon": "Okuma programi",
        })

    # ── RENDER ──
    if not onerileri:
        st.success("Harika! Bu ogrenci icin acil mudahale onerisi yok.")
        return

    seviye_renk = {"acil": "#ef4444", "yuksek": "#f97316", "normal": "#f59e0b", "dusuk": "#3b82f6"}
    seviye_bg = {"acil": "#450a0a", "yuksek": "#431407", "normal": "#422006", "dusuk": "#0c1a3d"}

    acil_c = sum(1 for o in onerileri if o["seviye"] == "acil")
    styled_stat_row([
        ("Toplam Oneri", str(len(onerileri)), "#ef4444", "💡"),
        ("Acil", str(acil_c), "#ef4444", "🚨"),
        ("Yuksek", str(sum(1 for o in onerileri if o["seviye"] == "yuksek")), "#f97316", "🟠"),
        ("Normal/Dusuk", str(sum(1 for o in onerileri if o["seviye"] in ("normal", "dusuk"))), "#3b82f6", "🔵"),
    ])

    for o in sorted(onerileri, key=lambda x: {"acil": 0, "yuksek": 1, "normal": 2, "dusuk": 3}[x["seviye"]]):
        renk = seviye_renk.get(o["seviye"], "#64748b")
        bg = seviye_bg.get(o["seviye"], "#0f172a")
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {renk}40;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span style="font-size:16px;">{o['ikon']}</span>
                <span style="font-weight:800;color:#fff;font-size:13px;">{o['sorun']}</span>
                <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:9px;font-weight:700;margin-left:auto;">{o['seviye'].upper()}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:8px 12px;margin-bottom:6px;">
                <span style="font-size:11px;color:{renk};font-weight:700;">Oneri:</span>
                <span style="font-size:11px;color:#cbd5e1;"> {o['oneri']}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;">
                <span>Sorumlu: <b style="color:#e2e8f0;">{o['sorumlu']}</b></span>
                <span>Aksiyon: <b style="color:{renk};">{o['aksiyon']}</b></span>
            </div>
        </div>""", unsafe_allow_html=True)

    # AI derin mudahale
    st.divider()
    if st.button("AI Kisisel Mudahale Plani", key=f"o360_ai_mud_{d.get('sid', '')}", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                veri = (f"Ogrenci: {d.get('name', '')}, Sinif: {d.get('sinif', '')}-{d.get('sube', '')}\n"
                        f"Not ort: {sum(g.get('puan', 0) for g in grades if isinstance(g.get('puan'), (int, float))) / max(len([g for g in grades if isinstance(g.get('puan'), (int, float))]), 1):.0f}\n"
                        f"Devamsizlik: {len(devamsizlik)}\n"
                        f"Risk: {risk_skor}/100\n"
                        f"Kulup: {len(kulupler)}, Etkinlik: {len(etkinlikler)}\n"
                        f"Tespit edilen sorunlar: {', '.join(o['sorun'][:40] for o in onerileri)}")
                with st.spinner("AI kisisel mudahale plani olusturuyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul rehberlik uzmanisin. Ogrenci verilerine dayanarak kisisel mudahale plani olustur: 1) Oncelikli sorunlar 2) Haftalik hedefler 3) Sorumlu atama 4) Takip takvimi 5) Veli iletisim plani. Turkce, somut."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=600, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#450a0a,#7f1d1d);border:1px solid #ef4444;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#fca5a5;font-weight:700;margin-bottom:6px;">AI Kisisel Mudahale Plani</div>
                        <div style="font-size:12px;color:#fecaca;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
