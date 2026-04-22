"""
Kurum Hizmetleri — ULTRA MEGA Ozellikleri
===========================================
1. Okul Operasyon Zekasi (School Operations AI)
2. Dijital Okul Pasaportu (Digital School Passport)
3. Kurum Hizmetleri Simulasyon & Maliyet Optimizasyonu
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


def _sj(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


# ============================================================
# 1. OKUL OPERASYON ZEKASI
# ============================================================

def render_operasyon_ai():
    """Capraz operasyonel analiz + AI verimlilik onerileri."""
    styled_section("Okul Operasyon Zekasi", "#7c3aed")
    styled_info_banner(
        "Tum hizmet verilerini capraz analiz ederek gizli verimsizlikleri bulur. "
        "AI haftalik operasyon raporu + tasarruf firsatlari.",
        banner_type="info", icon="🧠")

    td = _td()
    ak = _ak_dir()

    # Veri topla
    temizlik = _lj(os.path.join(td, "kurum_hizmetleri", "temizlik_kayitlari.json"))
    enerji = _lj(os.path.join(td, "kurum_hizmetleri", "enerji_tuketim.json"))
    menuler = _lj(os.path.join(td, "kurum_hizmetleri", "yemek_menu.json"))
    if not menuler:
        menuler = _lj(os.path.join(ak, "yemek_menusu.json"))
    nobet = _lj(os.path.join(ak, "nobet_kayitlar.json"))
    devamsizlik = _lj(os.path.join(ak, "attendance.json"))
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))
    ogrenciler = _lj(os.path.join(ak, "students.json"))
    aktif_ogr = sum(1 for s in ogrenciler if s.get("durum", "aktif") == "aktif")

    # Servis
    try:
        from models.servis_yonetimi import ServisDataStore
        ss = ServisDataStore(os.path.join(td, "servis"))
        hatlar = ss.load_list("hatlar") if hasattr(ss, "load_list") else []
        olaylar = ss.load_list("olaylar") if hasattr(ss, "load_list") else []
    except Exception:
        hatlar, olaylar = [], []

    # Revir
    try:
        from models.okul_sagligi import SaglikDataStore
        sag = SaglikDataStore(os.path.join(td, "saglik"))
        revir = sag.load_list("revir_ziyaretleri") if hasattr(sag, "load_list") else []
    except Exception:
        revir = []

    # ── KURAL BAZLI INSIGHT MOTORU ──
    insights = []

    # 1. Temizlik + sikayet korelasyonu
    temizlik_az = sum(1 for t in temizlik if t.get("durum") == "Yapilmadi")
    temizlik_sikayet = sum(1 for s in sikayetler if "temizlik" in (s.get("konu", "") + s.get("kategori", "")).lower())
    if temizlik_az > 3 and temizlik_sikayet > 0:
        insights.append({"seviye": "uyari", "ikon": "🧹",
                          "baslik": f"Temizlik yapilmayan {temizlik_az} kayit + {temizlik_sikayet} temizlik sikayeti",
                          "oneri": "Temizlik personeli takvimini gozden gecirin."})

    # 2. Enerji anomali
    if enerji:
        son = enerji[-1]
        onceki = enerji[-2] if len(enerji) >= 2 else {}
        if onceki:
            e_fark = (son.get("elektrik", 0) - onceki.get("elektrik", 0)) / max(onceki.get("elektrik", 1), 1) * 100
            if e_fark > 20:
                insights.append({"seviye": "uyari", "ikon": "⚡",
                                  "baslik": f"Elektrik tuketimi %{e_fark:.0f} artti (onceki aya gore)",
                                  "oneri": "Klima saatlerini ve bos sinif isiklanmasini kontrol edin."})

    # 3. Servis olay
    bugun = date.today().isoformat()
    son_30g = (date.today() - timedelta(days=30)).isoformat()
    son30_olay = sum(1 for o in olaylar if (o.get("tarih", "") or "")[:10] >= son_30g)
    if son30_olay > 3:
        insights.append({"seviye": "kritik", "ikon": "🚌",
                          "baslik": f"Son 30 gunde {son30_olay} servis olayi — ortalamanin uzerinde",
                          "oneri": "Sofor egitimleri planlayin, arac bakimlarini kontrol edin."})

    # 4. Nobet boslugu
    nobet_bos = sum(1 for n in nobet if n.get("durum") in ("tutulmadi", "gelmedi"))
    if nobet_bos > 5:
        insights.append({"seviye": "uyari", "ikon": "🛡️",
                          "baslik": f"{nobet_bos} nobet tutulmadi/gelmedi kaydi",
                          "oneri": "Nobet cizelgesini yeniden duzenleyin, yedek nobetci atayin."})

    # 5. Menu + revir
    if revir and menuler:
        insights.append({"seviye": "bilgi", "ikon": "🍽️",
                          "baslik": f"Revir: {len(revir)} basvuru · Menu: {len(menuler)} gun kayitli",
                          "oneri": "Kizartma/agir gunlerinde revir artisi varsa menu dengesini kontrol edin."})

    # 6. Basarili alanlar
    if temizlik_az == 0 and len(temizlik) > 10:
        insights.append({"seviye": "basari", "ikon": "✨",
                          "baslik": "Temizlik tam puanli — tum alanlar temizleniyor",
                          "oneri": "Temizlik ekibini tebrik edin."})

    if son30_olay == 0 and hatlar:
        insights.append({"seviye": "basari", "ikon": "🚌",
                          "baslik": "Son 30 gunde sifir servis olayi",
                          "oneri": "Servis guvenligi mukemmel durumda."})

    # ── RENDER ──
    seviye_renk = {"kritik": "#ef4444", "uyari": "#f97316", "bilgi": "#3b82f6", "basari": "#10b981"}
    seviye_bg = {"kritik": "#450a0a", "uyari": "#431407", "bilgi": "#0c1a3d", "basari": "#052e16"}

    kritik_c = sum(1 for i in insights if i["seviye"] == "kritik")
    uyari_c = sum(1 for i in insights if i["seviye"] == "uyari")

    styled_stat_row([
        ("Bulgu", str(len(insights)), "#7c3aed", "🧠"),
        ("Kritik", str(kritik_c), "#ef4444", "🔴"),
        ("Uyari", str(uyari_c), "#f97316", "🟠"),
        ("Basari", str(sum(1 for i in insights if i["seviye"] == "basari")), "#10b981", "🌟"),
    ])

    for ins in sorted(insights, key=lambda x: {"kritik": 0, "uyari": 1, "bilgi": 2, "basari": 3}[x["seviye"]]):
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

    # AI derin analiz
    st.divider()
    if st.button("AI Operasyon Raporu Olustur", key="ops_ai_btn", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                veri = (f"Ogrenci: {aktif_ogr}, Servis Hat: {len(hatlar)}, Olay: {len(olaylar)}, "
                        f"Menu: {len(menuler)} gun, Temizlik: {len(temizlik)} kayit (yapilmadi: {temizlik_az}), "
                        f"Enerji: {len(enerji)} ay, Nobet bos: {nobet_bos}, Revir: {len(revir)}, "
                        f"Sikayet: {len(sikayetler)}, Bulgu: {len(insights)} (kritik: {kritik_c})")
                with st.spinner("AI operasyon raporu hazirlaniyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul operasyon uzmanisin. Verilen verileri capraz analiz et. Verimsizlikleri bul, tasarruf onerileri sun, kalite iyilestirmeleri oener. Turkce, somut, maddeli."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=600, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Operasyon Raporu</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 2. DİJİTAL OKUL PASAPORTU
# ============================================================

def _pasaport_path() -> str:
    return os.path.join(_td(), "kurum_hizmetleri", "dijital_pasaport.json")


def render_dijital_pasaport():
    """QR kodlu dijital kimlik — ogrenci/personel/ziyaretci."""
    styled_section("Dijital Okul Pasaportu", "#0891b2")
    styled_info_banner(
        "Tek QR ile: yemekhane, kutuphane, servis, etkinlik. "
        "Her tarama otomatik loglanir. Veli aninda bilgilendirilir.",
        banner_type="info", icon="🪪")

    ak = _ak_dir()
    td = _td()

    ogrenciler = _lj(os.path.join(ak, "students.json"))
    aktif = [s for s in ogrenciler if s.get("durum", "aktif") == "aktif"]
    loglar = _lj(_pasaport_path())

    styled_stat_row([
        ("Aktif Ogrenci", str(len(aktif)), "#0891b2", "🎓"),
        ("Tarama Logu", str(len(loglar)), "#2563eb", "📋"),
    ])

    sub = st.tabs(["🪪 Pasaport Uret", "📋 Tarama Simule", "📊 Kullanim Analizi"])

    # ═══ PASAPORT ÜRET ═══
    with sub[0]:
        styled_section("Ogrenci Dijital Pasaport")
        if not aktif:
            styled_info_banner("Aktif ogrenci yok.", banner_type="warning", icon="⚠️")
        else:
            ogr_labels = [f"{s.get('ad', '')} {s.get('soyad', '')} — {s.get('sinif', '')}/{s.get('sube', '')}" for s in aktif]
            secili = st.selectbox("Ogrenci Secin", [""] + ogr_labels, key="pp_sec")

            if secili:
                idx = ogr_labels.index(secili)
                s = aktif[idx]
                pp_kod = (s.get("id", "") or uuid.uuid4().hex)[:8].upper()
                ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                sinif = f"{s.get('sinif', '')}-{s.get('sube', '')}"

                st.markdown(f"""
                <div style="max-width:360px;margin:12px auto;background:linear-gradient(135deg,#0B0F19,#0c4a6e);
                            border:3px solid #0891b2;border-radius:16px;overflow:hidden;">
                    <div style="background:linear-gradient(90deg,#0891b2,#06b6d4,#0891b2);padding:6px;text-align:center;">
                        <span style="font-size:10px;font-weight:800;color:#fff;letter-spacing:2px;">DIJITAL OKUL PASAPORTU</span>
                    </div>
                    <div style="padding:16px 20px;text-align:center;">
                        <div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#0891b2,#06b6d4);
                                    display:flex;align-items:center;justify-content:center;margin:0 auto 8px;
                                    font-size:20px;color:#fff;font-weight:900;">{ad[0] if ad else '?'}</div>
                        <div style="font-size:18px;font-weight:900;color:#fff;">{ad}</div>
                        <div style="font-size:12px;color:#67e8f9;">{sinif}</div>
                        <div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:8px;margin:10px 0;">
                            <div style="font-size:8px;color:#94a3b8;">PASAPORT KODU</div>
                            <div style="font-size:20px;font-weight:900;color:#06b6d4;font-family:monospace;letter-spacing:3px;">{pp_kod}</div>
                        </div>
                        <div style="font-size:8px;color:#64748b;">QR tarandiginda: yemekhane, kutuphane, servis, etkinlik</div>
                    </div>
                    <div style="background:linear-gradient(90deg,#0891b2,#06b6d4,#0891b2);padding:4px;text-align:center;">
                        <span style="font-size:7px;color:#fff;">SmartCampus AI · Dijital Pasaport Sistemi</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ═══ TARAMA SİMÜLE ═══
    with sub[1]:
        styled_section("Tarama Simulasyonu")
        styled_info_banner("Gercek QR tarayici olmadan tarama test edin.", banner_type="info", icon="📋")

        with st.form("tarama_form"):
            t_c1, t_c2 = st.columns(2)
            with t_c1:
                t_ogr = st.selectbox("Ogrenci", [f"{s.get('ad', '')} {s.get('soyad', '')}" for s in aktif[:50]], key="pp_t_ogr")
                t_alan = st.selectbox("Alan", ["Yemekhane", "Kutuphane", "Servis Binis", "Etkinlik", "Bina Giris", "Bina Cikis"], key="pp_t_alan")
            with t_c2:
                t_tarih = st.date_input("Tarih", value=date.today(), key="pp_t_tarih")
                t_saat = st.time_input("Saat", key="pp_t_saat")

            if st.form_submit_button("Tarama Kaydet", type="primary"):
                log = {
                    "id": f"pp_{uuid.uuid4().hex[:8]}",
                    "ogrenci": t_ogr, "alan": t_alan,
                    "tarih": t_tarih.isoformat(), "saat": t_saat.strftime("%H:%M"),
                    "created_at": datetime.now().isoformat(),
                }
                loglar.append(log)
                _sj(_pasaport_path(), loglar)
                st.success(f"Tarama kaydedildi: {t_ogr} → {t_alan}")
                st.rerun()

        # Son loglar
        styled_section("Son Taramalar")
        for l in sorted(loglar, key=lambda x: x.get("created_at", ""), reverse=True)[:15]:
            alan_ikon = {"Yemekhane": "🍽️", "Kutuphane": "📚", "Servis Binis": "🚌",
                           "Etkinlik": "🎭", "Bina Giris": "🏢", "Bina Cikis": "🚶"}.get(l.get("alan", ""), "📋")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:3px 0;border-bottom:1px solid #1e293b;">
                <span style="font-size:12px;">{alan_ikon}</span>
                <span style="min-width:60px;font-size:10px;color:#94a3b8;">{l.get('tarih', '')[:10]}</span>
                <span style="min-width:40px;font-size:10px;color:#67e8f9;">{l.get('saat', '')}</span>
                <span style="flex:1;font-size:11px;color:#e2e8f0;">{l.get('ogrenci', '')}</span>
                <span style="font-size:10px;color:#0891b2;font-weight:600;">{l.get('alan', '')}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ KULLANIM ANALİZİ ═══
    with sub[2]:
        styled_section("Pasaport Kullanim Analizi")
        if not loglar:
            styled_info_banner("Henuz tarama verisi yok.", banner_type="info", icon="📊")
        else:
            # Alan dagilimi
            alan_sayac = Counter(l.get("alan", "") for l in loglar)
            styled_section("Alan Bazli Kullanim")
            en_cok = max(alan_sayac.values()) if alan_sayac else 1
            for alan, sayi in alan_sayac.most_common():
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="min-width:100px;font-size:11px;color:#e2e8f0;font-weight:600;">{alan}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#0891b2;border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

            # En aktif ogrenciler
            styled_section("En Aktif Ogrenciler")
            ogr_sayac = Counter(l.get("ogrenci", "") for l in loglar)
            for ogr, sayi in ogr_sayac.most_common(10):
                st.markdown(f"- **{ogr}**: {sayi} tarama")


# ============================================================
# 3. MALİYET OPTİMİZASYON SİMÜLATÖRÜ
# ============================================================

def render_maliyet_optimizasyon():
    """Operasyonel maliyet simulasyonu + AI tasarruf onerileri."""
    styled_section("Maliyet Optimizasyon Simulatoru", "#f59e0b")
    styled_info_banner(
        "Operasyonel kararlarin maliyet etkisini simule edin. "
        "AI ile tasarruf firsatlari + 12 aylik projeksiyon.",
        banner_type="info", icon="💎")

    td = _td()
    ak = _ak_dir()

    ogrenciler = _lj(os.path.join(ak, "students.json"))
    aktif_ogr = sum(1 for s in ogrenciler if s.get("durum", "aktif") == "aktif")
    enerji = _lj(os.path.join(td, "kurum_hizmetleri", "enerji_tuketim.json"))

    # Tahmini maliyet kalemleri
    _MALIYET = {
        "yemek": {"label": "Yemek Servisi", "ikon": "🍽️", "aylik": aktif_ogr * 25 * 20, "renk": "#f59e0b"},
        "servis": {"label": "Servis/Ulasim", "ikon": "🚌", "aylik": 80000, "renk": "#2563eb"},
        "temizlik": {"label": "Temizlik", "ikon": "🧹", "aylik": 25000, "renk": "#10b981"},
        "enerji": {"label": "Enerji (Elek+Su+Gaz)", "ikon": "⚡", "aylik": 35000, "renk": "#ef4444"},
        "bakim": {"label": "Bakim/Onarim", "ikon": "🔧", "aylik": 15000, "renk": "#7c3aed"},
        "guvenlik": {"label": "Guvenlik", "ikon": "🛡️", "aylik": 20000, "renk": "#dc2626"},
    }

    # Gercek enerji varsa guncelle
    if enerji:
        son = enerji[-1]
        e_toplam = son.get("elektrik", 0) * 3.5 + son.get("su", 0) * 25 + son.get("dogalgaz", 0) * 8
        if e_toplam > 0:
            _MALIYET["enerji"]["aylik"] = round(e_toplam)

    aylik_toplam = sum(m["aylik"] for m in _MALIYET.values())
    yillik_toplam = aylik_toplam * 12

    styled_stat_row([
        ("Aylik Toplam", f"{aylik_toplam:,.0f} TL", "#f59e0b", "💰"),
        ("Yillik Tahmin", f"{yillik_toplam:,.0f} TL", "#ef4444", "📊"),
        ("Ogrenci Basi/Ay", f"{round(aylik_toplam / max(aktif_ogr, 1)):,.0f} TL", "#2563eb", "👤"),
    ])

    sub = st.tabs(["📊 Maliyet Dagilimi", "🔮 Simulasyon", "🤖 AI Tasarruf"])

    # ═══ MALİYET DAĞILIMI ═══
    with sub[0]:
        styled_section("Aylik Maliyet Kalemleri")
        for key, m in _MALIYET.items():
            pct = round(m["aylik"] / max(aylik_toplam, 1) * 100)
            bar_w = min(pct * 2, 100)
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {m['renk']}30;border-left:4px solid {m['renk']};
                        border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <span style="font-size:13px;font-weight:700;color:#e2e8f0;">{m['ikon']} {m['label']}</span>
                    <span style="font-size:14px;font-weight:900;color:{m['renk']};">{m['aylik']:,.0f} TL</span>
                </div>
                <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{m['renk']};border-radius:4px;"></div>
                </div>
                <div style="font-size:9px;color:#64748b;margin-top:3px;text-align:right;">%{pct} pay</div>
            </div>""", unsafe_allow_html=True)

    # ═══ SİMÜLASYON ═══
    with sub[1]:
        styled_section("Maliyet Simulasyonu")
        senaryo = st.selectbox("Senaryo", [
            "🍽️ Yemek porsiyon kucult (%10)",
            "🚌 Servis hat birlestir (2 hat)",
            "⚡ Enerji tasarruf paketi",
            "🧹 Temizlik disardan al (outsource)",
            "🔮 Serbest Senaryo (AI)",
        ], key="mo_sen")

        if "porsiyon" in senaryo:
            tasarruf = round(_MALIYET["yemek"]["aylik"] * 0.10)
            risk = "Dusuk — porsiyon kuculur ama cesit ayni"
        elif "hat" in senaryo:
            tasarruf = round(80000 / max(6, 1) * 2)  # 2 hat tasarrufu
            risk = "Orta — kapasite sikismasi olabilir"
        elif "Enerji" in senaryo:
            tasarruf = round(_MALIYET["enerji"]["aylik"] * 0.25)
            risk = "Dusuk — LED + sensor + zamanlayici"
        elif "outsource" in senaryo:
            tasarruf = round(_MALIYET["temizlik"]["aylik"] * 0.15)
            risk = "Orta — kalite kontrolu gerekli"
        else:
            tasarruf = 0
            risk = ""

        if "Serbest" not in senaryo:
            yillik_tasarruf = tasarruf * 12
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #10b981;border-radius:16px;padding:16px;
                        text-align:center;margin:12px 0;">
                <div style="font-size:10px;color:#94a3b8;">Tahmini Aylik Tasarruf</div>
                <div style="font-size:36px;font-weight:900;color:#10b981;">{tasarruf:,.0f} TL</div>
                <div style="font-size:12px;color:#6ee7b7;">Yillik: {yillik_tasarruf:,.0f} TL · Risk: {risk}</div>
            </div>""", unsafe_allow_html=True)
        else:
            soru = st.text_area("Senaryonuzu yazin...", key="mo_serbest", height=80,
                                 placeholder="Yemekhanesini kapatip kumanya dagitsak ne olur?")
            if st.button("AI Simule Et", key="mo_ai_btn", type="primary"):
                if soru:
                    try:
                        from utils.smarti_helper import _get_client
                        client = _get_client()
                        if client:
                            veri = f"Aylik: {aylik_toplam:,.0f} TL, Kalemler: " + ", ".join(f"{m['label']}:{m['aylik']:,.0f}" for m in _MALIYET.values())
                            with st.spinner("AI simule ediyor..."):
                                resp = client.chat.completions.create(
                                    model="gpt-4o-mini",
                                    messages=[
                                        {"role": "system", "content": "Sen bir okul maliyet optimizasyon uzmanisin. Senaryo analizi yap: tasarruf, risk, oneri. Turkce, somut."},
                                        {"role": "user", "content": f"Senaryo: {soru}\n\nMaliyet: {veri}\nOgrenci: {aktif_ogr}"},
                                    ],
                                    max_tokens=500, temperature=0.7,
                                )
                                ai = resp.choices[0].message.content or ""
                            if ai:
                                st.markdown(f"""
                                <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                            border-radius:14px;padding:16px 20px;">
                                    <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:6px;">AI Senaryo Analizi</div>
                                    <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                                </div>""", unsafe_allow_html=True)
                        else:
                            st.warning("OpenAI API bulunamadi.")
                    except Exception as e:
                        st.error(f"Hata: {e}")

    # ═══ AI TASARRUF ═══
    with sub[2]:
        styled_section("AI Tasarruf Onerileri")
        if st.button("AI Tasarruf Raporu", key="mo_tasarruf_btn", type="primary", use_container_width=True):
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    veri = (f"Maliyet kalemleri: " + ", ".join(f"{m['label']}={m['aylik']:,.0f}TL/ay" for m in _MALIYET.values()) +
                            f"\nToplam: {aylik_toplam:,.0f} TL/ay, {yillik_toplam:,.0f} TL/yil" +
                            f"\nOgrenci: {aktif_ogr}, Enerji kaydi: {len(enerji)} ay")
                    with st.spinner("AI tasarruf firsatlari ariyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir okul maliyet uzmanisin. Verilen maliyet kalemlerini analiz et. En az 5 somut tasarruf onerisi sun: ne yapilmali, tahmini tasarruf TL, risk seviyesi. Turkce, tablo formati."},
                                {"role": "user", "content": veri},
                            ],
                            max_tokens=600, temperature=0.7,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:6px;">AI Tasarruf Onerileri</div>
                            <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")
