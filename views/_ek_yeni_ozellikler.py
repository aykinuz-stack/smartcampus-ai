"""
Eğitim Koçluğu — Yeni Özellikler
==================================
1. Koç Performans Karnesi & Öğrenci İlerleme Portfolyosu
2. LGS/YKS Net Tahmin & Hedef Simülatörü
3. Gamifiye Koçluk & Motivasyon Motoru
"""
from __future__ import annotations
import json, os, uuid, random, math
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "egitim_koclugu"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else d.get("items", d.get("data", []))
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_LGS = {"Turkce": 20, "Matematik": 20, "Fen": 20, "Inkilap": 10, "Din": 10, "Ingilizce": 10}
_TYT = {"Turkce": 40, "Matematik": 40, "Fen": 20, "Sosyal": 20}
_AYT_SAY = {"Matematik": 40, "Fizik": 14, "Kimya": 13, "Biyoloji": 13}

_SINAV_MAP = {
    "LGS": {"dersler": _LGS, "max": 500},
    "TYT": {"dersler": _TYT, "max": 500},
    "AYT-Sayisal": {"dersler": _AYT_SAY, "max": 500},
}

_ROZETLER = [
    {"ad": "Ilk Gorusme", "ikon": "🌱", "kosul": "gorusme_1", "hedef": 1, "xp": 10, "renk": "#10b981"},
    {"ad": "Hedef Avcisi", "ikon": "🎯", "kosul": "hedef_3", "hedef": 3, "xp": 30, "renk": "#f59e0b"},
    {"ad": "Odev Yildizi", "ikon": "📝", "kosul": "odev_10", "hedef": 10, "xp": 25, "renk": "#3b82f6"},
    {"ad": "Net Artisci", "ikon": "📈", "kosul": "net_artis_5", "hedef": 5, "xp": 35, "renk": "#059669"},
    {"ad": "Streak Ustasi", "ikon": "🔥", "kosul": "streak_7", "hedef": 7, "xp": 30, "renk": "#ef4444"},
    {"ad": "Motivasyon Guclu", "ikon": "💪", "kosul": "motivasyon_8", "hedef": 8, "xp": 20, "renk": "#8b5cf6"},
    {"ad": "Quiz Sampiyonu", "ikon": "🧠", "kosul": "quiz_5", "hedef": 5, "xp": 25, "renk": "#0891b2"},
    {"ad": "Deneme Kahramani", "ikon": "📋", "kosul": "deneme_10", "hedef": 10, "xp": 40, "renk": "#6366f1"},
    {"ad": "Surekli Gelisim", "ikon": "🏆", "kosul": "xp_300", "hedef": 300, "xp": 50, "renk": "#c9a84c"},
    {"ad": "Efsane Ogrenci", "ikon": "💎", "kosul": "xp_1000", "hedef": 1000, "xp": 100, "renk": "#8b5cf6"},
]

_XP_AKTIVITE = {
    "Gorusme Katilim": 8, "Hedef Tamamla": 15, "Odev Teslim": 5, "Deneme Coz": 10,
    "Net Artisi (+1)": 3, "Motivasyon Yuksek": 5, "Plan Tamamla": 7, "Quiz Basarili": 6,
}

_SEVIYELER = {
    (0,50): ("Cirak","🟤","#78716c"), (50,150): ("Ogrenci","🥉","#a8a29e"),
    (150,350): ("Calisan","🥈","#94a3b8"), (350,600): ("Basarili","🥇","#f59e0b"),
    (600,1000): ("Yildiz","👑","#c9a84c"), (1000,99999): ("Efsane","💎","#8b5cf6"),
}


# ════════════════════════════════════════════════════════════
# 1. KOÇ PERFORMANS KARNESİ & İLERLEME PORTFOLYOSU
# ════════════════════════════════════════════════════════════

def render_koc_karnesi(store):
    """Koç Performans Karnesi — koç etkinliği, öğrenci ilerleme, eşleştirme."""
    styled_section("Koc Performans Karnesi & Ogrenci Ilerleme Portfolyosu", "#6366f1")
    styled_info_banner(
        "Her koc-ogrenci iliskisinin etkinligini olcun. "
        "Net artisi, hedef gerceklesme, motivasyon egrisi.",
        banner_type="info", icon="🏆")

    ogrenciler = _lj("ogrenciler.json")
    gorusmeler = _lj("gorusmeler.json")
    hedefler = _lj("hedefler.json")
    denemeler = _lj("deneme_sonuclari.json")

    sub = st.tabs(["📊 Koc Karnesi", "👤 Ogrenci Portfolyo", "📈 Net Trend", "🤝 Eslestirme"])

    with sub[0]:
        styled_section("Koc Bazli Performans")
        if not ogrenciler:
            st.info("Ogrenci kaydi yok.")
        else:
            ogr_say = len(ogrenciler)
            gorusme_say = len(gorusmeler)
            hedef_ok = sum(1 for h in hedefler if h.get("durum") == "Tamamlandi")
            hedef_toplam = max(len(hedefler), 1)
            hedef_oran = round(hedef_ok / hedef_toplam * 100)

            styled_stat_row([
                ("Ogrenci", str(ogr_say), "#6366f1", "👥"),
                ("Gorusme", str(gorusme_say), "#3b82f6", "📅"),
                ("Hedef Basari", f"%{hedef_oran}", "#10b981" if hedef_oran >= 60 else "#f59e0b", "🎯"),
                ("Deneme", str(len(denemeler)), "#8b5cf6", "📋"),
            ])

            # Ogrenci bazli ozet
            for o in ogrenciler[:15]:
                ad = f"{o.get('ad','')} {o.get('soyad','')}"
                ogr_g = sum(1 for g in gorusmeler if g.get("ogrenci_adi","") == ad)
                ogr_h = sum(1 for h in hedefler if h.get("ogrenci_adi","") == ad and h.get("durum") == "Tamamlandi")
                ogr_h_t = max(sum(1 for h in hedefler if h.get("ogrenci_adi","") == ad), 1)
                ogr_d = [d for d in denemeler if d.get("ogrenci_adi","") == ad]

                # Net trend
                if len(ogr_d) >= 2:
                    ilk = ogr_d[0].get("net", 0)
                    son = ogr_d[-1].get("net", 0)
                    artis = son - ilk
                    trend_txt = f"+{artis}" if artis > 0 else str(artis)
                    trend_renk = "#10b981" if artis > 0 else "#ef4444"
                else:
                    trend_txt = "-"
                    trend_renk = "#94a3b8"

                h_oran = round(ogr_h / ogr_h_t * 100)
                renk = "#10b981" if h_oran >= 70 else "#f59e0b" if h_oran >= 40 else "#ef4444"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{ad}</span>
                    <span style="color:#3b82f6;font-size:0.65rem;">{ogr_g}g</span>
                    <span style="color:{renk};font-size:0.65rem;">{ogr_h}/{ogr_h_t}h</span>
                    <span style="color:{trend_renk};font-weight:700;font-size:0.7rem;">{trend_txt} net</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Bireysel Ilerleme Portfolyosu")
        if ogrenciler:
            ogr_opts = [f"{o.get('ad','')} {o.get('soyad','')}" for o in ogrenciler]
            sec = st.selectbox("Ogrenci", ogr_opts, key="kk_ogr")

            ogr_g = [g for g in gorusmeler if g.get("ogrenci_adi","") == sec]
            ogr_h = [h for h in hedefler if h.get("ogrenci_adi","") == sec]
            ogr_d = sorted([d for d in denemeler if d.get("ogrenci_adi","") == sec], key=lambda x: x.get("tarih",""))

            h_ok = sum(1 for h in ogr_h if h.get("durum") == "Tamamlandi")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,#6366f130);border:2px solid #6366f1;
                border-radius:18px;padding:20px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{sec}</div>
                <div style="display:flex;justify-content:center;gap:20px;margin-top:10px;">
                    <div><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{len(ogr_g)}</div><div style="color:#64748b;font-size:0.62rem;">Gorusme</div></div>
                    <div><div style="color:#10b981;font-weight:900;font-size:1.5rem;">{h_ok}/{len(ogr_h)}</div><div style="color:#64748b;font-size:0.62rem;">Hedef</div></div>
                    <div><div style="color:#8b5cf6;font-weight:900;font-size:1.5rem;">{len(ogr_d)}</div><div style="color:#64748b;font-size:0.62rem;">Deneme</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

            if ogr_d:
                styled_section("Deneme Net Trendi")
                for idx, d in enumerate(ogr_d):
                    net = d.get("net", 0)
                    onceki = ogr_d[idx-1].get("net", net) if idx > 0 else net
                    fark = net - onceki
                    renk = "#10b981" if fark > 0 else "#ef4444" if fark < 0 else "#94a3b8"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin:2px 0;">
                        <span style="min-width:18px;color:#64748b;font-size:0.65rem;">{idx+1}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{min(net*1.2, 100)}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{net}</span></div></div>
                        <span style="color:{renk};font-size:0.65rem;font-weight:700;min-width:30px;">{'+' if fark>0 else ''}{fark}</span>
                    </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Genel Net Artis Trendi")
        if denemeler:
            ogr_net = defaultdict(list)
            for d in denemeler:
                ogr_net[d.get("ogrenci_adi","")].append(d.get("net",0))
            for ad, netler in sorted(ogr_net.items()):
                if len(netler) >= 2:
                    artis = netler[-1] - netler[0]
                    renk = "#10b981" if artis > 0 else "#ef4444" if artis < 0 else "#94a3b8"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:4px 12px;margin:2px 0;
                        background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{ad}</span>
                        <span style="color:#94a3b8;font-size:0.65rem;">Ilk:{netler[0]} Son:{netler[-1]}</span>
                        <span style="color:{renk};font-weight:800;font-size:0.75rem;">{'+' if artis>0 else ''}{artis}</span>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Deneme verisi yok.")

    with sub[3]:
        styled_section("Koc-Ogrenci Eslestirme Onerisi")
        st.info("Mevcut verilerden en uygun koc-ogrenci eslestirmesi icin yeterli veri toplanmali.")
        st.caption("Eslestirme kriteri: kocluk alani, ogretmen bransi, ogrenci ihtiyaci.")


# ════════════════════════════════════════════════════════════
# 2. LGS/YKS NET TAHMİN & HEDEF SİMÜLATÖRÜ
# ════════════════════════════════════════════════════════════

def render_net_tahmin(store):
    """LGS/YKS Net Tahmin — mevcut tempo, what-if, hedef ters hesaplama."""
    styled_section("LGS/YKS Net Tahmin & Hedef Simulatoru", "#ef4444")
    styled_info_banner(
        "Mevcut deneme netlerinden sinav gunu tahmini. "
        "What-if: 'Geometri'yi arttirsam nete etkisi ne?' Hedef puan → gereken plan.",
        banner_type="warning", icon="🎯")

    denemeler = _lj("deneme_sonuclari.json")

    sub = st.tabs(["🔮 Net Tahmin", "⚖️ What-If", "🎯 Hedef Planla", "📈 Projeksiyon"])

    with sub[0]:
        styled_section("Mevcut Tempo ile Sinav Gunu Tahmini")
        sinav = st.selectbox("Sinav", list(_SINAV_MAP.keys()), key="nt_sinav")
        info = _SINAV_MAP[sinav]
        toplam_soru = sum(info["dersler"].values())

        ogrenciler = _lj("ogrenciler.json")
        if ogrenciler:
            ogr_opts = [f"{o.get('ad','')} {o.get('soyad','')}" for o in ogrenciler]
            sec = st.selectbox("Ogrenci", ogr_opts, key="nt_ogr")

            ogr_d = sorted([d for d in denemeler if d.get("ogrenci_adi","") == sec], key=lambda x: x.get("tarih",""))
            if ogr_d:
                son = ogr_d[-1]
                mevcut_net = son.get("net", 0)
                tahmin_puan = round(mevcut_net / toplam_soru * info["max"])

                # Trend
                if len(ogr_d) >= 3:
                    son_3 = [d.get("net",0) for d in ogr_d[-3:]]
                    haftalik_artis = round((son_3[-1] - son_3[0]) / 2, 1)
                else:
                    haftalik_artis = 0

                renk = "#10b981" if tahmin_puan >= 400 else "#f59e0b" if tahmin_puan >= 300 else "#ef4444"

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,{renk}15);border:2px solid {renk};
                    border-radius:18px;padding:20px;text-align:center;margin:10px 0;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">{sec} — {sinav}</div>
                    <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                        <div><div style="color:#3b82f6;font-weight:900;font-size:2rem;">{mevcut_net}</div><div style="color:#64748b;font-size:0.62rem;">Mevcut Net</div></div>
                        <div><div style="color:{renk};font-weight:900;font-size:2rem;">{tahmin_puan}</div><div style="color:#64748b;font-size:0.62rem;">Tahmin Puan</div></div>
                        <div><div style="color:{'#10b981' if haftalik_artis>0 else '#ef4444'};font-weight:900;font-size:2rem;">{'+' if haftalik_artis>0 else ''}{haftalik_artis}</div><div style="color:#64748b;font-size:0.62rem;">Haftalik Artis</div></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info(f"{sec} icin deneme verisi yok.")
        else:
            st.info("Ogrenci kaydi yok.")

    with sub[1]:
        styled_section("What-If — Ders Bazli Etki Simulasyonu")
        sinav2 = st.selectbox("Sinav", list(_SINAV_MAP.keys()), key="wf_sinav")
        info2 = _SINAV_MAP[sinav2]
        toplam2 = sum(info2["dersler"].values())

        mevcut_net = st.number_input("Mevcut Toplam Net", 0.0, float(toplam2), 30.0, step=0.5, key="wf_mevcut")
        st.markdown("**Ders bazli ek net artisi:**")

        ek_toplam = 0
        cols = st.columns(min(len(info2["dersler"]), 3))
        for i, (ders, soru) in enumerate(info2["dersler"].items()):
            with cols[i % len(cols)]:
                ek = st.number_input(f"{ders} (+net)", 0.0, float(soru), 0.0, step=0.5, key=f"wf_{ders}")
                ek_toplam += ek

        yeni_net = mevcut_net + ek_toplam
        mevcut_puan = round(mevcut_net / toplam2 * info2["max"])
        yeni_puan = round(yeni_net / toplam2 * info2["max"])
        fark = yeni_puan - mevcut_puan

        renk_m = "#f59e0b" if mevcut_puan < 400 else "#10b981"
        renk_y = "#10b981" if yeni_puan >= 400 else "#f59e0b"

        st.markdown(f"""
        <div style="display:flex;gap:16px;margin:14px 0;">
            <div style="flex:1;background:#0f172a;border:2px solid {renk_m};border-radius:16px;padding:16px;text-align:center;">
                <div style="color:#94a3b8;font-size:0.75rem;">Mevcut</div>
                <div style="color:{renk_m};font-weight:900;font-size:2rem;">{mevcut_net} net</div>
                <div style="color:#64748b;font-size:0.7rem;">~{mevcut_puan} puan</div>
            </div>
            <div style="display:flex;align-items:center;color:#94a3b8;font-size:1.5rem;">→</div>
            <div style="flex:1;background:#0f172a;border:2px solid {renk_y};border-radius:16px;padding:16px;text-align:center;">
                <div style="color:#94a3b8;font-size:0.75rem;">+{ek_toplam} net sonrasi</div>
                <div style="color:{renk_y};font-weight:900;font-size:2rem;">{yeni_net} net</div>
                <div style="color:#64748b;font-size:0.7rem;">~{yeni_puan} puan (+{fark})</div>
            </div>
        </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Hedef Puan → Gereken Net & Plan")
        sinav3 = st.selectbox("Sinav", list(_SINAV_MAP.keys()), key="hp_sinav")
        info3 = _SINAV_MAP[sinav3]
        toplam3 = sum(info3["dersler"].values())

        hedef_puan = st.number_input("Hedef Puan", 100, 500, 400, key="hp_hedef")
        gereken_net = round(hedef_puan / info3["max"] * toplam3, 1)

        st.markdown(f"""
        <div style="background:#ef444415;border:2px solid #ef4444;border-radius:16px;
            padding:16px;text-align:center;margin:10px 0;">
            <div style="color:#fca5a5;font-size:0.8rem;">{sinav3} — Hedef: {hedef_puan} puan</div>
            <div style="color:#ef4444;font-weight:900;font-size:2.5rem;margin-top:6px;">{gereken_net} net</div>
        </div>""", unsafe_allow_html=True)

        styled_section("Ders Bazli Gereken Net Dagilimi")
        for ders, soru in info3["dersler"].items():
            oran = soru / toplam3
            ders_net = round(gereken_net * oran, 1)
            pct = round(ders_net / max(soru, 1) * 100)
            renk = "#ef4444" if pct >= 80 else "#f59e0b" if pct >= 60 else "#10b981"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                <span style="min-width:90px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{ders_net}/{soru}</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("30 Gun Net Projeksiyon")
        mevcut = st.number_input("Mevcut Net", 0.0, 100.0, 30.0, step=0.5, key="pj_mevcut")
        haftalik = st.number_input("Haftalik Net Artis", 0.0, 5.0, 1.0, step=0.25, key="pj_haftalik")

        for hafta in range(0, 5):
            gun = hafta * 7
            tahmin = round(mevcut + haftalik * hafta, 1)
            tarih = (date.today() + timedelta(days=gun)).strftime("%d.%m")
            renk = "#10b981" if tahmin >= 40 else "#f59e0b" if tahmin >= 25 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                <span style="min-width:50px;color:#94a3b8;font-size:0.72rem;">+{gun}g ({tarih})</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                    <div style="width:{min(tahmin*1.2,100)}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.55rem;color:#fff;font-weight:700;">{tahmin}</span></div></div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. GAMİFİYE KOÇLUK & MOTİVASYON MOTORU
# ════════════════════════════════════════════════════════════

def render_gamifiye_kocluk(store):
    """Gamifiye Koçluk — XP, rozet, streak, liderlik, challenge."""
    styled_section("Gamifiye Kocluk & Motivasyon Motoru", "#c9a84c")
    styled_info_banner(
        "Gorusme katilimi, hedef tamamlama, odev teslimi, deneme artisi "
        "icin XP/rozet kazan! Streak, challenge, liderlik tablosu.",
        banner_type="info", icon="🎮")

    gamifiye_log = _lj("gamifiye_log.json")
    ogrenciler = _lj("ogrenciler.json")
    gorusmeler = _lj("gorusmeler.json")
    hedefler = _lj("hedefler.json")
    denemeler = _lj("deneme_sonuclari.json")

    sub = st.tabs(["👤 Profil", "🏆 Liderlik", "🎖️ Rozetler", "⚡ Challenge", "📊 XP Tablosu"])

    with sub[0]:
        styled_section("Ogrenci Gamifiye Profili")
        if not ogrenciler:
            st.info("Ogrenci yok.")
            return
        ogr_opts = [f"{o.get('ad','')} {o.get('soyad','')}" for o in ogrenciler]
        sec = st.selectbox("Ogrenci", ogr_opts, key="gm_ogr")

        # XP hesapla
        ogr_g = sum(1 for g in gorusmeler if g.get("ogrenci_adi","") == sec and g.get("durum") == "Tamamlandi")
        ogr_h = sum(1 for h in hedefler if h.get("ogrenci_adi","") == sec and h.get("durum") == "Tamamlandi")
        ogr_d = len([d for d in denemeler if d.get("ogrenci_adi","") == sec])

        xp = ogr_g * _XP_AKTIVITE["Gorusme Katilim"] + ogr_h * _XP_AKTIVITE["Hedef Tamamla"] + ogr_d * _XP_AKTIVITE["Deneme Coz"]

        # Rozetler
        kazanilan = []
        for r in _ROZETLER:
            kazandi = False
            if r["kosul"] == "gorusme_1" and ogr_g >= 1: kazandi = True
            elif r["kosul"] == "hedef_3" and ogr_h >= 3: kazandi = True
            elif r["kosul"] == "deneme_10" and ogr_d >= 10: kazandi = True
            elif r["kosul"] == "xp_300" and xp >= 300: kazandi = True
            elif r["kosul"] == "xp_1000" and xp >= 1000: kazandi = True
            if kazandi:
                xp += r["xp"]
                kazanilan.append(r)

        # Seviye
        sev_ad, sev_ikon, sev_renk = "Cirak", "🟤", "#78716c"
        sev_pct = 0
        for (lo, hi), (ad, ikon, renk) in _SEVIYELER.items():
            if lo <= xp < hi:
                sev_ad, sev_ikon, sev_renk = ad, ikon, renk
                sev_pct = round((xp - lo) / max(hi - lo, 1) * 100)
                break

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,{sev_renk}20);border:2px solid {sev_renk};
            border-radius:20px;padding:24px;text-align:center;">
            <div style="font-size:3rem;">{sev_ikon}</div>
            <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">{sec}</div>
            <div style="color:{sev_renk};font-weight:800;">{sev_ad}</div>
            <div style="color:{sev_renk};font-weight:900;font-size:2rem;margin-top:6px;">{xp} XP</div>
            <div style="background:#1e293b;border-radius:6px;height:12px;margin:10px 20px;overflow:hidden;">
                <div style="width:{sev_pct}%;height:100%;background:{sev_renk};border-radius:6px;"></div>
            </div>
            <div style="color:#64748b;font-size:0.7rem;">{len(kazanilan)} rozet | {ogr_g}g + {ogr_h}h + {ogr_d}d</div>
        </div>""", unsafe_allow_html=True)

        if kazanilan:
            cols = st.columns(min(len(kazanilan), 4))
            for i, r in enumerate(kazanilan):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div style="background:#0f172a;border:2px solid {r['renk']};border-radius:14px;
                        padding:10px;text-align:center;margin:3px 0;">
                        <div style="font-size:1.5rem;">{r['ikon']}</div>
                        <div style="color:{r['renk']};font-weight:800;font-size:0.68rem;">{r['ad']}</div>
                    </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Kocluk Liderlik Tablosu")
        lider = []
        for o in ogrenciler:
            ad = f"{o.get('ad','')} {o.get('soyad','')}"
            g = sum(1 for x in gorusmeler if x.get("ogrenci_adi","") == ad and x.get("durum") == "Tamamlandi")
            h = sum(1 for x in hedefler if x.get("ogrenci_adi","") == ad and x.get("durum") == "Tamamlandi")
            d = len([x for x in denemeler if x.get("ogrenci_adi","") == ad])
            xp_s = g * 8 + h * 15 + d * 10
            if xp_s > 0:
                lider.append({"ad": ad, "xp": xp_s})

        lider.sort(key=lambda x: x["xp"], reverse=True)
        for sira, l in enumerate(lider[:15], 1):
            madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
            for (lo,hi),(_, ikon, renk) in _SEVIYELER.items():
                if lo <= l["xp"] < hi: break
            else: ikon, renk = "💎", "#8b5cf6"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{l['ad']}</span>
                <span style="font-size:0.75rem;">{ikon}</span>
                <span style="color:#c9a84c;font-weight:800;">{l['xp']} XP</span>
            </div>""", unsafe_allow_html=True)

        if not lider:
            st.info("XP kazanilmamis.")

    with sub[2]:
        styled_section("Tum Rozetler")
        cols = st.columns(3)
        for i, r in enumerate(_ROZETLER):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {r['renk']}30;border-radius:14px;
                    padding:12px;text-align:center;margin:4px 0;">
                    <div style="font-size:1.8rem;">{r['ikon']}</div>
                    <div style="color:{r['renk']};font-weight:800;font-size:0.75rem;margin-top:3px;">{r['ad']}</div>
                    <div style="color:#94a3b8;font-size:0.6rem;">{r.get('hedef','')} hedef</div>
                    <div style="color:#c9a84c;font-size:0.68rem;font-weight:700;margin-top:2px;">+{r['xp']} XP</div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Haftalik Challenge")
        challenges = [
            {"ad": "3 Deneme Coz", "ikon": "📋", "xp": 30, "renk": "#3b82f6"},
            {"ad": "5 Gun Streak", "ikon": "🔥", "xp": 25, "renk": "#ef4444"},
            {"ad": "2 Hedef Tamamla", "ikon": "🎯", "xp": 30, "renk": "#f59e0b"},
            {"ad": "Tum Odevleri Teslim", "ikon": "📝", "xp": 20, "renk": "#10b981"},
        ]
        for ch in challenges:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {ch['renk']}30;border-left:5px solid {ch['renk']};
                border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">{ch['ikon']} {ch['ad']}</span>
                    <span style="color:#c9a84c;font-weight:800;font-size:0.85rem;">+{ch['xp']} XP</span>
                </div>
            </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Aktivite XP Tablosu")
        for akt, puan in sorted(_XP_AKTIVITE.items(), key=lambda x: x[1], reverse=True):
            bar_w = round(puan / 15 * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                <span style="min-width:130px;font-size:0.8rem;color:#e2e8f0;font-weight:600;">{akt}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#c9a84c;border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">+{puan}</span></div></div>
            </div>""", unsafe_allow_html=True)
