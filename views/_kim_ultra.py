"""
Kurumsal Organizasyon — ULTRA Ozellikleri
==========================================
1. Kurum Itibar Endeksi + Canli Trend Monitoru
2. Stratejik Senaryo Simulatoru
3. Dijital Onay Akisi & Surec Motoru (Workflow Engine)
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _td() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
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
# 1. KURUM İTİBAR ENDEKSİ + CANLI TREND MONİTÖRÜ
# ============================================================

def _hesapla_itibar_segmentleri() -> dict:
    """Her segment icin 0-100 puan hesapla."""
    td = _td()
    ak = _ak_dir()
    segmentler = {}

    # 1. Veli Memnuniyet (%30)
    cevaplar = _lj(os.path.join(td, "veli_anket", "cevaplar.json"))
    if cevaplar:
        puanlar = [c.get("puan", 0) for c in cevaplar if isinstance(c.get("puan"), (int, float))]
        ort = sum(puanlar) / max(len(puanlar), 1)
        segmentler["memnuniyet"] = {"puan": round(ort / 5 * 100, 1), "agirlik": 30,
                                     "label": "Veli Memnuniyeti", "ikon": "😊", "renk": "#10b981",
                                     "detay": f"Ort: {ort:.1f}/5 ({len(puanlar)} cevap)"}
    else:
        segmentler["memnuniyet"] = {"puan": 50, "agirlik": 30, "label": "Veli Memnuniyeti",
                                     "ikon": "😊", "renk": "#10b981", "detay": "Veri yok (varsayilan 50)"}

    # 2. Sikayet Performansi (%20)
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))
    if sikayetler:
        cozumlenen = sum(1 for s in sikayetler if s.get("durum") == "cozumlendi")
        cozum_oran = round(cozumlenen / max(len(sikayetler), 1) * 100, 1)
        segmentler["sikayet"] = {"puan": cozum_oran, "agirlik": 20,
                                  "label": "Sikayet Yonetimi", "ikon": "📝", "renk": "#f59e0b",
                                  "detay": f"%{cozum_oran} cozum ({cozumlenen}/{len(sikayetler)})"}
    else:
        segmentler["sikayet"] = {"puan": 80, "agirlik": 20, "label": "Sikayet Yonetimi",
                                  "ikon": "📝", "renk": "#f59e0b", "detay": "Sikayet yok (iyi)"}

    # 3. Kayit Donusum (%15)
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        kesin = sum(1 for a in adaylar if a.asama == "kesin_kayit")
        toplam = len(adaylar)
        donusum = round(kesin / max(toplam, 1) * 100, 1) if toplam else 0
        segmentler["kayit"] = {"puan": min(donusum * 2, 100), "agirlik": 15,
                                "label": "Kayit Donusum", "ikon": "🎯", "renk": "#2563eb",
                                "detay": f"%{donusum} donusum ({kesin}/{toplam})"}
    except Exception:
        segmentler["kayit"] = {"puan": 50, "agirlik": 15, "label": "Kayit Donusum",
                                "ikon": "🎯", "renk": "#2563eb", "detay": "Veri yok"}

    # 4. Referans Gucu (%15)
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        referansli = sum(1 for a in adaylar if a.referans_veli)
        ref_oran = round(referansli / max(len(adaylar), 1) * 100, 1) if adaylar else 0
        segmentler["referans"] = {"puan": min(ref_oran * 5, 100), "agirlik": 15,
                                   "label": "Referans Gucu", "ikon": "🔗", "renk": "#7c3aed",
                                   "detay": f"%{ref_oran} referansli ({referansli} aday)"}
    except Exception:
        segmentler["referans"] = {"puan": 30, "agirlik": 15, "label": "Referans Gucu",
                                   "ikon": "🔗", "renk": "#7c3aed", "detay": "Veri yok"}

    # 5. Personel Baglilik (%10)
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        emp = ik.load_list("employees") if hasattr(ik, "load_list") else []
        aktif = sum(1 for e in emp if e.get("status") == "Aktif")
        izinler = ik.load_list("izinler") if hasattr(ik, "load_list") else []
        izin_oran = round(len(izinler) / max(aktif, 1) * 100, 1) if aktif else 0
        puan = max(0, 100 - izin_oran * 2)
        segmentler["personel"] = {"puan": round(puan, 1), "agirlik": 10,
                                   "label": "Personel Baglilik", "ikon": "👥", "renk": "#0d9488",
                                   "detay": f"{aktif} aktif, {len(izinler)} izin"}
    except Exception:
        segmentler["personel"] = {"puan": 70, "agirlik": 10, "label": "Personel Baglilik",
                                   "ikon": "👥", "renk": "#0d9488", "detay": "Veri yok"}

    # 6. Sosyal Medya/Etkilesim (%10)
    try:
        posts = _lj(os.path.join(td, "smm_posts.json"))
        yayinlanan = sum(1 for p in posts if p.get("status") == "published")
        puan = min(yayinlanan * 5, 100)
        segmentler["sosyal"] = {"puan": puan, "agirlik": 10,
                                 "label": "Sosyal Etkilesim", "ikon": "📱", "renk": "#e11d48",
                                 "detay": f"{yayinlanan} yayinlanan post"}
    except Exception:
        segmentler["sosyal"] = {"puan": 30, "agirlik": 10, "label": "Sosyal Etkilesim",
                                 "ikon": "📱", "renk": "#e11d48", "detay": "Veri yok"}

    return segmentler


def _itibar_genel_puan(segmentler: dict) -> float:
    toplam = sum(s["puan"] * s["agirlik"] for s in segmentler.values())
    agirlik_toplam = sum(s["agirlik"] for s in segmentler.values())
    return round(toplam / max(agirlik_toplam, 1), 1)


def render_itibar_endeksi():
    """Kurum itibar endeksi — tum geri bildirimlerden bilesik skor."""
    styled_section("Kurum Itibar Endeksi", "#c9a84c")
    styled_info_banner(
        "Veli memnuniyeti, sikayet cozum performansi, kayit donusum, referans gucu, "
        "personel bagliligi ve sosyal medya — 6 kaynaktan bilesik itibar puani.",
        banner_type="info", icon="🌡️")

    segmentler = _hesapla_itibar_segmentleri()
    genel = _itibar_genel_puan(segmentler)

    # Renk
    if genel >= 75:
        g_renk, g_etiket = "#10b981", "Guclu"
    elif genel >= 55:
        g_renk, g_etiket = "#f59e0b", "Orta"
    elif genel >= 35:
        g_renk, g_etiket = "#f97316", "Riskli"
    else:
        g_renk, g_etiket = "#ef4444", "Kritik"

    # ── HERO TERMOMETRE ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
                border:2px solid {g_renk};border-radius:20px;padding:28px;margin:0 0 18px 0;
                box-shadow:0 8px 32px {g_renk}30;text-align:center;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,{g_renk},{g_renk},transparent);"></div>
        <div style="font-size:10px;color:#94a3b8;letter-spacing:3px;text-transform:uppercase;">
            Kurumsal Itibar Endeksi</div>
        <div style="font-size:72px;font-weight:900;color:{g_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{genel}</div>
        <div style="background:{g_renk}20;color:{g_renk};display:inline-block;padding:6px 20px;
                    border-radius:10px;font-size:13px;font-weight:800;letter-spacing:1px;">{g_etiket}</div>
        <div style="font-size:11px;color:#64748b;margin-top:10px;">
            6 kaynaktan agirlikli ortalama · {date.today().strftime('%d.%m.%Y')}</div>

        <!-- TERMOMETRE BAR -->
        <div style="margin:20px auto 0;max-width:400px;">
            <div style="display:flex;justify-content:space-between;font-size:8px;color:#64748b;margin-bottom:4px;">
                <span>0 Kritik</span><span>25</span><span>50 Orta</span><span>75</span><span>100 Mukemmel</span>
            </div>
            <div style="background:linear-gradient(90deg,#ef4444,#f97316,#f59e0b,#22c55e,#10b981);
                        border-radius:6px;height:14px;position:relative;">
                <div style="position:absolute;left:{min(genel, 100)}%;top:-4px;transform:translateX(-50%);
                            width:4px;height:22px;background:#fff;border-radius:2px;
                            box-shadow:0 0 8px rgba(255,255,255,0.5);"></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── SEGMENT KARTLARI ──
    styled_section("Segment Bazli Analiz")
    cols = st.columns(3)
    for idx, (key, seg) in enumerate(segmentler.items()):
        with cols[idx % 3]:
            s_renk = "#10b981" if seg["puan"] >= 70 else "#f59e0b" if seg["puan"] >= 45 else "#ef4444"
            bar_w = min(seg["puan"], 100)
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {seg['renk']}30;border-left:4px solid {seg['renk']};
                        border-radius:0 12px 12px 0;padding:12px 14px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-size:13px;font-weight:700;color:#e2e8f0;">{seg['ikon']} {seg['label']}</span>
                    <span style="font-size:18px;font-weight:900;color:{s_renk};">{seg['puan']}</span>
                </div>
                <div style="background:#1e293b;border-radius:4px;height:6px;overflow:hidden;margin-bottom:4px;">
                    <div style="width:{bar_w}%;height:100%;background:{seg['renk']};border-radius:4px;"></div>
                </div>
                <div style="font-size:9px;color:#64748b;">Agirlik: %{seg['agirlik']} · {seg['detay']}</div>
            </div>""", unsafe_allow_html=True)

    # ── AI YORUM ──
    st.divider()
    if st.button("AI Itibar Degerlendirmesi", key="itibar_ai", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                seg_ozet = "\n".join(f"- {s['label']}: {s['puan']}/100 (agirlik %{s['agirlik']}) — {s['detay']}"
                                     for s in segmentler.values())
                with st.spinner("AI analiz ediyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul itibar danismanisin. Verilen itibar endeks verilerini analiz et. Guclu/zayif yonleri belirle, somut iyilestirme onerileri sun. Turkce, kisa."},
                            {"role": "user", "content": f"Genel Itibar: {genel}/100\n\nSegmentler:\n{seg_ozet}"},
                        ],
                        max_tokens=500, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                border-radius:14px;padding:16px 20px;margin-top:12px;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Degerlendirme</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API anahtari bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 2. STRATEJİK SENARYO SİMÜLATÖRÜ
# ============================================================

def render_senaryo_simulatoru():
    """Ya ... yaparsak? — stratejik etki simulasyonu."""
    styled_section("Senaryo Simulatoru", "#6366f1")
    styled_info_banner(
        "Stratejik kararlarin etkisini simule edin. Parametreleri ayarlayin, "
        "sistem mevcut verilere dayanarak tahmini sonuclari gosterir.",
        banner_type="info", icon="🔮")

    td = _td()

    # Mevcut verileri yukle
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        toplam_aday = len(adaylar)
        kesin_kayit = sum(1 for a in adaylar if a.asama == "kesin_kayit")
        olumsuz = sum(1 for a in adaylar if a.asama == "olumsuz")
        kayip_fiyat = sum(1 for a in adaylar if getattr(a, "kayip_nedeni", "") == "fiyat")
    except Exception:
        toplam_aday, kesin_kayit, olumsuz, kayip_fiyat = 100, 40, 30, 10

    gelirler = _lj(os.path.join(td, "butce", "gelir_kayitlari.json"))
    giderler = _lj(os.path.join(td, "butce", "gider_kayitlari.json"))
    t_gelir = sum(g.get("tutar", 0) for g in gelirler if isinstance(g.get("tutar"), (int, float)))
    t_gider = sum(g.get("tutar", 0) for g in giderler if isinstance(g.get("tutar"), (int, float)))

    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        emp = ik.load_list("employees") if hasattr(ik, "load_list") else []
        personel_sayi = len(emp)
    except Exception:
        personel_sayi = 30

    cevaplar = _lj(os.path.join(td, "veli_anket", "cevaplar.json"))
    memnuniyet_ort = round(sum(c.get("puan", 3) for c in cevaplar) / max(len(cevaplar), 1), 1) if cevaplar else 3.5

    # ── SENARYO SECİMİ ──
    senaryo = st.selectbox("Senaryo Secin", [
        "💰 Ucretleri Degistir",
        "👥 Personel Sayisini Degistir",
        "🎓 Kontenjani Degistir",
        "🚌 Hizmet Ekle/Kaldir",
        "🔮 Serbest Senaryo (AI)",
    ], key="sen_sec")

    st.divider()

    # ═══ UCRET DEĞİŞİKLİĞİ ═══
    if "Ucret" in senaryo:
        styled_section("Ucret Degisiklik Simulasyonu")
        st.markdown(f"**Mevcut durum:** {kesin_kayit} kesin kayit · {kayip_fiyat} fiyat kaynakli kayip · Gelir: {t_gelir:,.0f} TL")

        degisim = st.slider("Ucret Degisimi (%)", -30, 50, 0, 5, key="sen_ucret")

        if degisim != 0:
            # Simulasyon
            if degisim > 0:
                # Zam → kayip riski artar
                ek_kayip = round(kayip_fiyat * (degisim / 10) * 0.3)
                yeni_kayit = max(0, kesin_kayit - ek_kayip)
                gelir_degisim = t_gelir * (degisim / 100) - (ek_kayip * t_gelir / max(kesin_kayit, 1))
                risk = "Yuksek" if degisim > 15 else "Orta"
                risk_renk = "#ef4444" if degisim > 15 else "#f59e0b"
                memnuniyet_etki = round(memnuniyet_ort - degisim * 0.02, 1)
            else:
                # Indirim → kayip azalir
                kurtarilan = round(abs(degisim) / 10 * kayip_fiyat * 0.5)
                yeni_kayit = kesin_kayit + kurtarilan
                gelir_degisim = t_gelir * (degisim / 100) + (kurtarilan * t_gelir / max(kesin_kayit, 1))
                risk = "Dusuk"
                risk_renk = "#10b981"
                memnuniyet_etki = round(memnuniyet_ort + abs(degisim) * 0.01, 1)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid #3b82f6;border-radius:14px;padding:16px;text-align:center;">
                    <div style="font-size:10px;color:#64748b;text-transform:uppercase;">Mevcut</div>
                    <div style="font-size:28px;font-weight:900;color:#3b82f6;">{kesin_kayit}</div>
                    <div style="font-size:10px;color:#94a3b8;">Kesin Kayit</div>
                    <div style="font-size:14px;color:#94a3b8;margin-top:6px;">{t_gelir:,.0f} TL gelir</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                ok = "▲" if gelir_degisim >= 0 else "▼"
                g_r = "#10b981" if gelir_degisim >= 0 else "#ef4444"
                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid {g_r};border-radius:14px;padding:16px;text-align:center;">
                    <div style="font-size:10px;color:#64748b;text-transform:uppercase;">Tahmini</div>
                    <div style="font-size:28px;font-weight:900;color:{g_r};">{yeni_kayit}</div>
                    <div style="font-size:10px;color:#94a3b8;">Kesin Kayit</div>
                    <div style="font-size:14px;color:{g_r};margin-top:6px;">{ok} {abs(gelir_degisim):,.0f} TL</div>
                </div>""", unsafe_allow_html=True)

            # Etki ozeti
            st.markdown(f"""
            <div style="background:#1e293b;border-radius:12px;padding:14px 18px;margin-top:12px;">
                <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
                    <span style="color:#94a3b8;">Risk: <b style="color:{risk_renk};">{risk}</b></span>
                    <span style="color:#94a3b8;">Memnuniyet: <b style="color:#f59e0b;">{memnuniyet_ort} → {memnuniyet_etki}</b></span>
                    <span style="color:#94a3b8;">Ucret: <b>{'%+d' % degisim}</b></span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ PERSONEL DEĞİŞİKLİĞİ ═══
    elif "Personel" in senaryo:
        styled_section("Personel Degisiklik Simulasyonu")
        st.markdown(f"**Mevcut:** {personel_sayi} personel · Aylık gider: ~{t_gider / 12:,.0f} TL")

        degisim = st.slider("Personel Degisimi", -10, 20, 0, 1, key="sen_personel")
        if degisim != 0:
            yeni_sayi = personel_sayi + degisim
            maliyet_degisim = degisim * (t_gider / 12 / max(personel_sayi, 1))
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:14px 18px;margin-top:8px;">
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
                    <div><div style="font-size:24px;font-weight:800;color:#3b82f6;">{personel_sayi}</div>
                        <div style="font-size:9px;color:#64748b;">Mevcut</div></div>
                    <div><div style="font-size:24px;font-weight:800;color:{'#10b981' if degisim > 0 else '#ef4444'};">{yeni_sayi}</div>
                        <div style="font-size:9px;color:#64748b;">Tahmini</div></div>
                    <div><div style="font-size:24px;font-weight:800;color:{'#ef4444' if maliyet_degisim > 0 else '#10b981'};">
                        {'%+.0f' % maliyet_degisim} TL</div>
                        <div style="font-size:9px;color:#64748b;">Aylik Maliyet</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ KONTENJAN DEĞİŞİKLİĞİ ═══
    elif "Kontenjan" in senaryo:
        styled_section("Kontenjan Degisiklik Simulasyonu")
        st.markdown(f"**Mevcut:** {kesin_kayit} kayitli ogrenci · {toplam_aday} aday")

        ek_kontenjan = st.slider("Ek Kontenjan", 0, 100, 0, 5, key="sen_kontenjan")
        if ek_kontenjan > 0:
            aktif_aday = sum(1 for a in adaylar if a.aktif) if 'adaylar' in dir() else 20
            tahmini_dolum = min(ek_kontenjan, round(aktif_aday * 0.4))
            ek_gelir = tahmini_dolum * (t_gelir / max(kesin_kayit, 1))
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #0891b2;border-radius:12px;padding:14px 18px;">
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
                    <div><div style="font-size:24px;font-weight:800;color:#0891b2;">{ek_kontenjan}</div>
                        <div style="font-size:9px;color:#64748b;">Ek Kontenjan</div></div>
                    <div><div style="font-size:24px;font-weight:800;color:#10b981;">{tahmini_dolum}</div>
                        <div style="font-size:9px;color:#64748b;">Tahmini Dolum</div></div>
                    <div><div style="font-size:24px;font-weight:800;color:#f59e0b;">{ek_gelir:,.0f} TL</div>
                        <div style="font-size:9px;color:#64748b;">Tahmini Ek Gelir</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ HİZMET EKLE/KALDIR ═══
    elif "Hizmet" in senaryo:
        styled_section("Hizmet Ekleme/Kaldirma Simulasyonu")
        hizmet = st.selectbox("Hizmet", ["Servis", "Yemek", "Etut", "Pansiyon", "Dijital Platform"], key="sen_hizmet")
        islem = st.radio("Islem", ["Ekle", "Kaldir"], horizontal=True, key="sen_hizmet_islem")

        if islem == "Kaldir":
            risk_puan = 35 if hizmet == "Servis" else 25 if hizmet == "Yemek" else 15
            st.markdown(f"""
            <div style="background:#7f1d1d;border:1px solid #ef4444;border-radius:12px;padding:14px 18px;">
                <div style="font-size:14px;font-weight:800;color:#fca5a5;">
                    ⚠️ {hizmet} kaldirirsa</div>
                <div style="font-size:12px;color:#fca5a5;margin-top:6px;">
                    Memnuniyet riski: <b>%{risk_puan} dusus</b> · Sikayet artisi: <b>%{risk_puan * 2} tahmini</b> ·
                    Kayit kaybi: <b>~{round(kesin_kayit * risk_puan / 100)}</b> ogrenci</div>
            </div>""", unsafe_allow_html=True)
        else:
            gelir_artis = 15 if hizmet == "Etut" else 10 if hizmet == "Dijital Platform" else 8
            st.markdown(f"""
            <div style="background:#052e16;border:1px solid #10b981;border-radius:12px;padding:14px 18px;">
                <div style="font-size:14px;font-weight:800;color:#6ee7b7;">
                    ✅ {hizmet} eklenirse</div>
                <div style="font-size:12px;color:#6ee7b7;margin-top:6px;">
                    Memnuniyet artisi: <b>%{gelir_artis}</b> · Rekabet avantaji: <b>Yuksek</b> ·
                    Ek gelir potansiyeli: <b>~{round(t_gelir * gelir_artis / 100):,.0f} TL</b></div>
            </div>""", unsafe_allow_html=True)

    # ═══ SERBEST SENARYO (AI) ═══
    elif "Serbest" in senaryo:
        styled_section("AI Serbest Senaryo Analizi")
        soru = st.text_area("Senaryonuzu yazin...", key="sen_serbest", height=100,
                             placeholder="Ornek: Yeni bir sube acsak ne olur? Burs oranini %50'ye cikarsak?")

        if st.button("Simule Et", key="sen_ai_btn", type="primary"):
            if soru:
                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                    if client:
                        veri = (f"Mevcut: {kesin_kayit} kayit, {toplam_aday} aday, {personel_sayi} personel, "
                                f"Gelir: {t_gelir:,.0f} TL, Gider: {t_gider:,.0f} TL, "
                                f"Memnuniyet: {memnuniyet_ort}/5, Fiyat kaybi: {kayip_fiyat}")
                        with st.spinner("AI simule ediyor..."):
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen bir okul stratejik planlama danismanisin. Verilen okul verilerine dayanarak senaryo analizini yap. Olasi sonuclari, riskleri ve onerileri Turkce maddeler halinde sun."},
                                    {"role": "user", "content": f"Senaryo: {soru}\n\nOkul Verileri: {veri}"},
                                ],
                                max_tokens=600, temperature=0.7,
                            )
                            ai = resp.choices[0].message.content or ""
                        if ai:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #6366f1;
                                        border-radius:14px;padding:16px 20px;">
                                <div style="font-size:12px;color:#a5b4fc;font-weight:700;margin-bottom:6px;">AI Senaryo Analizi</div>
                                <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("OpenAI API anahtari bulunamadi.")
                except Exception as e:
                    st.error(f"Hata: {e}")


# ============================================================
# 3. DİJİTAL ONAY AKIŞI & SÜREÇ MOTORU (WORKFLOW ENGINE)
# ============================================================

_AKIS_TURLERI = {
    "izin": {"label": "Izin Onayi", "ikon": "🏖️", "renk": "#f59e0b",
             "adimlar": ["Basvuru", "Birim Amiri", "Mudur", "Onaylandi"]},
    "harcama": {"label": "Harcama Onayi", "ikon": "💰", "renk": "#10b981",
                "adimlar": ["Talep", "Butce Kontrol", "Mud. Yrd.", "Mudur", "Onaylandi"]},
    "etkinlik": {"label": "Etkinlik Onayi", "ikon": "🎭", "renk": "#7c3aed",
                 "adimlar": ["Teklif", "Departman", "Mudur", "Onaylandi"]},
    "sertifika": {"label": "Sertifika Onayi", "ikon": "🏆", "renk": "#2563eb",
                  "adimlar": ["Tasarim", "Kontrol", "Imza", "Yayinlandi"]},
    "sikayet": {"label": "Sikayet Eskalasyon", "ikon": "📝", "renk": "#ef4444",
                "adimlar": ["Kayit", "Ilgili Birim", "Cozum", "Mudur Onayi", "Kapatildi"]},
}


def _workflow_path() -> str:
    return os.path.join(_td(), "yte", "workflows.json")


def _load_workflows() -> list[dict]:
    return _lj(_workflow_path())


def _save_workflows(wfs: list[dict]):
    path = _workflow_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(wfs, f, ensure_ascii=False, indent=2)


def render_onay_akisi():
    """Dijital onay akisi — surec motoru."""
    styled_section("Onay Akisi & Surec Yonetimi", "#059669")
    styled_info_banner(
        "Izin, harcama, etkinlik, sertifika ve sikayet eskalasyon surecleri. "
        "Her adim izlenebilir, onay/red + yorum eklenir, SLA takibi yapilir.",
        banner_type="info", icon="✅")

    workflows = _load_workflows()

    # Ozet
    bekleyen = sum(1 for w in workflows if w.get("durum") == "devam")
    tamamlanan = sum(1 for w in workflows if w.get("durum") == "tamamlandi")
    reddedilen = sum(1 for w in workflows if w.get("durum") == "reddedildi")

    styled_stat_row([
        ("Toplam Akis", str(len(workflows)), "#059669", "📋"),
        ("Bekleyen", str(bekleyen), "#f59e0b", "⏳"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
        ("Reddedilen", str(reddedilen), "#ef4444", "❌"),
    ])

    sub = st.tabs(["⏳ Bekleyen Onaylar", "➕ Yeni Akis", "📋 Gecmis", "📊 SLA"])

    # ═══ BEKLEYEN ONAYLAR ═══
    with sub[0]:
        styled_section("Bekleyen Onaylar")
        bekleyenler = [w for w in workflows if w.get("durum") == "devam"]

        if not bekleyenler:
            st.success("Bekleyen onay yok!")
        else:
            for w in bekleyenler:
                tur_info = _AKIS_TURLERI.get(w.get("tur", ""), {"label": "?", "ikon": "📋", "renk": "#64748b", "adimlar": []})
                adimlar = tur_info["adimlar"]
                aktif_adim = w.get("aktif_adim", 0)
                renk = tur_info["renk"]

                # Adim gostergesi
                adim_html = ""
                for i, adim in enumerate(adimlar):
                    if i < aktif_adim:
                        a_renk, a_bg = "#10b981", "#10b981"
                        a_icon = "✓"
                    elif i == aktif_adim:
                        a_renk, a_bg = renk, renk
                        a_icon = "●"
                    else:
                        a_renk, a_bg = "#475569", "transparent"
                        a_icon = "○"
                    adim_html += (
                        f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;">'
                        f'<div style="width:24px;height:24px;border-radius:50%;background:{a_bg};border:2px solid {a_renk};'
                        f'display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;font-weight:700;">{a_icon}</div>'
                        f'<span style="font-size:8px;color:{a_renk};font-weight:600;text-align:center;max-width:60px;">{adim}</span>'
                        f'</div>')
                    if i < len(adimlar) - 1:
                        line_clr = "#10b981" if i < aktif_adim else "#334155"
                        adim_html += f'<div style="flex:1;height:2px;background:{line_clr};margin:12px 0 0;min-width:20px;"></div>'

                # SLA
                created = w.get("created_at", "")[:10]
                gun_gecti = 0
                try:
                    gun_gecti = (date.today() - date.fromisoformat(created)).days
                except Exception:
                    pass
                sla_renk = "#ef4444" if gun_gecti > 5 else "#f59e0b" if gun_gecti > 2 else "#10b981"

                with st.expander(f"{tur_info['ikon']} {w.get('baslik', '')} — {adimlar[aktif_adim] if aktif_adim < len(adimlar) else 'Son'} asamasinda", expanded=False):
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;padding:8px;
                                background:#0f172a;border-radius:10px;">
                        {adim_html}
                    </div>""", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="font-size:11px;color:#94a3b8;margin-bottom:8px;">
                        Baslatan: {w.get('baslatan', '—')} · Tarih: {created} ·
                        <span style="color:{sla_renk};font-weight:700;">{gun_gecti} gun gecti</span>
                    </div>""", unsafe_allow_html=True)

                    # Gecmis adimlarin notlari
                    for log in w.get("log", []):
                        st.caption(f"✓ {log.get('adim', '')}: {log.get('onaylayan', '')} — {log.get('yorum', '')} ({log.get('tarih', '')})")

                    # Onay/Red formu
                    col1, col2 = st.columns(2)
                    yorum = st.text_input("Yorum", key=f"wf_yor_{w['id']}", placeholder="Onay/red yorumu...")
                    with col1:
                        if st.button("Onayla", key=f"wf_ok_{w['id']}", type="primary", use_container_width=True):
                            w.setdefault("log", []).append({
                                "adim": adimlar[aktif_adim] if aktif_adim < len(adimlar) else "",
                                "onaylayan": "Yonetici",
                                "karar": "onay",
                                "yorum": yorum,
                                "tarih": datetime.now().isoformat()[:16],
                            })
                            w["aktif_adim"] = aktif_adim + 1
                            if w["aktif_adim"] >= len(adimlar):
                                w["durum"] = "tamamlandi"
                                w["bitis_tarihi"] = date.today().isoformat()
                            _save_workflows(workflows)
                            st.success("Onaylandi!")
                            st.rerun()
                    with col2:
                        if st.button("Reddet", key=f"wf_red_{w['id']}", use_container_width=True):
                            w.setdefault("log", []).append({
                                "adim": adimlar[aktif_adim] if aktif_adim < len(adimlar) else "",
                                "onaylayan": "Yonetici",
                                "karar": "red",
                                "yorum": yorum,
                                "tarih": datetime.now().isoformat()[:16],
                            })
                            w["durum"] = "reddedildi"
                            w["bitis_tarihi"] = date.today().isoformat()
                            _save_workflows(workflows)
                            st.error("Reddedildi.")
                            st.rerun()

    # ═══ YENİ AKIŞ ═══
    with sub[1]:
        styled_section("Yeni Onay Akisi Baslat")
        with st.form("wf_yeni"):
            tur = st.selectbox("Akis Turu", list(_AKIS_TURLERI.keys()),
                                format_func=lambda x: f"{_AKIS_TURLERI[x]['ikon']} {_AKIS_TURLERI[x]['label']}",
                                key="wf_tur")
            baslik = st.text_input("Baslik", placeholder="Izin talebi: Ali Veli — 3 gun")
            aciklama = st.text_area("Aciklama", height=80)
            baslatan = st.text_input("Baslatan Kisi", placeholder="Ad Soyad")

            if st.form_submit_button("Akisi Baslat", type="primary"):
                if baslik:
                    yeni = {
                        "id": f"wf_{uuid.uuid4().hex[:8]}",
                        "tur": tur,
                        "baslik": baslik,
                        "aciklama": aciklama,
                        "baslatan": baslatan,
                        "aktif_adim": 1,  # Ilk adim (basvuru) otomatik tamamlandi
                        "durum": "devam",
                        "log": [{"adim": _AKIS_TURLERI[tur]["adimlar"][0], "onaylayan": baslatan,
                                 "karar": "baslat", "yorum": aciklama[:100],
                                 "tarih": datetime.now().isoformat()[:16]}],
                        "created_at": datetime.now().isoformat(),
                    }
                    workflows.append(yeni)
                    _save_workflows(workflows)
                    st.success(f"Akis baslatildi: {baslik}")
                    st.rerun()

    # ═══ GEÇMİŞ ═══
    with sub[2]:
        styled_section("Tamamlanan / Reddedilen Akislar")
        gecmis = [w for w in workflows if w.get("durum") in ("tamamlandi", "reddedildi")]
        gecmis.sort(key=lambda x: x.get("bitis_tarihi", ""), reverse=True)

        if not gecmis:
            st.info("Gecmis akis yok.")
        else:
            rows = ""
            for w in gecmis[:30]:
                tur_info = _AKIS_TURLERI.get(w.get("tur", ""), {"label": "?", "ikon": "?", "renk": "#64748b"})
                d_renk = "#10b981" if w["durum"] == "tamamlandi" else "#ef4444"
                d_label = "Tamamlandi" if w["durum"] == "tamamlandi" else "Reddedildi"
                rows += f"""<tr>
                    <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{w.get('created_at', '')[:10]}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#e2e8f0;font-weight:600;">{tur_info['ikon']} {tur_info['label']}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#e2e8f0;">{w.get('baslik', '')[:50]}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{w.get('baslatan', '')}</td>
                    <td style="padding:5px 8px;"><span style="background:{d_renk}20;color:{d_renk};
                        padding:2px 8px;border-radius:6px;font-size:10px;font-weight:700;">{d_label}</span></td>
                    <td style="padding:5px 8px;font-size:11px;color:#64748b;">{w.get('bitis_tarihi', '')}</td>
                </tr>"""
            if rows:
                st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">
                <thead><tr style="background:#1e293b;">
                    <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Tarih</th>
                    <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Tur</th>
                    <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Baslik</th>
                    <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Baslatan</th>
                    <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Durum</th>
                    <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Bitis</th>
                </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

    # ═══ SLA TAKİBİ ═══
    with sub[3]:
        styled_section("SLA Performansi")
        tamamlananlar = [w for w in workflows if w.get("durum") == "tamamlandi" and w.get("created_at") and w.get("bitis_tarihi")]

        if not tamamlananlar:
            st.info("SLA hesaplamak icin tamamlanan akis gerekli.")
        else:
            sureler = []
            for w in tamamlananlar:
                try:
                    bas = date.fromisoformat(w["created_at"][:10])
                    bit = date.fromisoformat(w["bitis_tarihi"][:10])
                    sureler.append((bit - bas).days)
                except Exception:
                    pass

            if sureler:
                ort_sure = round(sum(sureler) / len(sureler), 1)
                en_hizli = min(sureler)
                en_yavas = max(sureler)
                sla_ok = sum(1 for s in sureler if s <= 3)
                sla_pct = round(sla_ok / len(sureler) * 100, 1)

                styled_stat_row([
                    ("Ort. Cozum Suresi", f"{ort_sure} gun", "#2563eb", "⏱️"),
                    ("En Hizli", f"{en_hizli} gun", "#10b981", "🚀"),
                    ("En Yavas", f"{en_yavas} gun", "#ef4444", "🐌"),
                    ("SLA Basari (<=3 gun)", f"%{sla_pct}", "#f59e0b", "🎯"),
                ])

        # Bekleyen akislarin SLA durumu
        styled_section("Bekleyen Akis SLA Durumu")
        bekleyenler = [w for w in workflows if w.get("durum") == "devam"]
        if bekleyenler:
            for w in bekleyenler:
                try:
                    gun = (date.today() - date.fromisoformat(w["created_at"][:10])).days
                except Exception:
                    gun = 0
                sla_r = "#ef4444" if gun > 5 else "#f59e0b" if gun > 2 else "#10b981"
                sla_t = "GECIKTI" if gun > 5 else "UYARI" if gun > 2 else "NORMAL"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
                    <span style="font-size:11px;color:#e2e8f0;flex:1;">{w.get('baslik', '')[:60]}</span>
                    <span style="font-size:10px;color:#94a3b8;">{gun} gun</span>
                    <span style="background:{sla_r}20;color:{sla_r};padding:2px 8px;border-radius:4px;
                                font-size:9px;font-weight:700;">{sla_t}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Bekleyen akis yok.")
