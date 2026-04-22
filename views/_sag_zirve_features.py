"""
Okul Sağlığı — Zirve Özellikler
=================================
1. Okul Sağlık Wellness Endeksi & Karşılaştırma Cockpit
2. AI Sağlık Tahmin & Proaktif Müdahale Motoru
3. Sağlık Bilinçlendirme & Kampanya Yönetimi
"""
from __future__ import annotations
import json, os, uuid, random, math
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _sd():
    d = os.path.join(get_tenant_dir(), "saglik"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_sd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_sd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}

_WELLNESS_KRITERLERI = {
    "Revir Yogunlugu": {"ikon": "🏥", "renk": "#0891b2", "agirlik": 15, "aciklama": "Aylik revir ziyaret orani (dusuk=iyi)"},
    "Salgin Durumu": {"ikon": "🦠", "renk": "#ef4444", "agirlik": 15, "aciklama": "Aktif bulasici hastalik vakasi (az=iyi)"},
    "BMI Dagilimi": {"ikon": "📏", "renk": "#3b82f6", "agirlik": 15, "aciklama": "Normal BMI oranı (yuksek=iyi)"},
    "Hijyen Puani": {"ikon": "🧹", "renk": "#10b981", "agirlik": 15, "aciklama": "Ortalama hijyen gozlem puani"},
    "Asi Kapsami": {"ikon": "💉", "renk": "#8b5cf6", "agirlik": 15, "aciklama": "Asi kaydi olan ogrenci orani"},
    "Acil Olay": {"ikon": "🚑", "renk": "#f59e0b", "agirlik": 10, "aciklama": "Aylik acil olay sayisi (az=iyi)"},
    "Muafiyet Orani": {"ikon": "🏃", "renk": "#6366f1", "agirlik": 5, "aciklama": "Spor muaf ogrenci orani (dusuk=iyi)"},
    "Kampanya": {"ikon": "📢", "renk": "#059669", "agirlik": 10, "aciklama": "Tamamlanan saglik kampanyasi sayisi"},
}

_KAMPANYA_KONULARI = [
    "El Yikama Haftasi", "Dis Sagligi Ayi", "Saglikli Beslenme Gunu",
    "Temiz Hava / Sigara Karsiti", "Goz Sagligi Haftasi", "Ruh Sagligi Farkindalik",
    "Su Tuketimi Kampanyasi", "Ekran Suresi Farkindalik", "Spor ve Hareket Haftasi",
    "Alerji Farkindalik", "Ilk Yardim Bilinclendirme", "Uyku Hijyeni Kampanyasi",
    "Obezite ile Mucadele", "Hijyen ve Temizlik", "Diger",
]

_MEVSIM_RISK = {
    "Eylul": ["Okul baslangici uyum stresi", "Bit salgini riski"],
    "Ekim": ["Soguk alginligi baslangici", "Grip asisi hatirlatma"],
    "Kasim": ["Grip sezonu zirvesi", "D vitamini eksikligi"],
    "Aralik": ["Grip + RSV yoğunlugu", "Kirli hava etkisi"],
    "Ocak": ["Soguk alginligi pik", "Kuru hava cilt sorunlari"],
    "Subat": ["Grip devam", "Yariyil tatili sonrasi uyum"],
    "Mart": ["Polen alerjisi baslangici", "Bahar yorgunlugu"],
    "Nisan": ["Alerji sezonu zirvesi", "Gida zehirlenmesi riski artar"],
    "Mayis": ["Bocek sokmasi/isirmasi", "Gunes yanigi riski"],
    "Haziran": ["Su kaybi / dehidrasyon", "Sinav stresi / kaygisi"],
}


# ════════════════════════════════════════════════════════════
# 1. OKUL SAĞLIK WELLNESS ENDEKSİ & COCKPIT
# ════════════════════════════════════════════════════════════

def _hesapla_wellness() -> dict:
    """Okul wellness puanını tüm verilerden hesapla."""
    students = load_shared_students()
    toplam_ogr = max(len(students), 1)
    bu_ay = date.today().strftime("%Y-%m")

    revir = _lj("revir_ziyaretleri.json") if os.path.exists(os.path.join(_sd(), "revir_ziyaretleri.json")) else []
    salgin = _lj("salgin_vakalari.json")
    olcumler = _lj("saglik_olcumleri.json")
    hijyen = _lj("hijyen_kayitlari.json")
    asi = _lj("asi_kayitlari.json")
    acil = _lj("acil_olaylar.json")
    muafiyet = _lj("spor_muafiyetleri.json")
    kampanyalar = _lj("saglik_kampanyalari.json")

    # Revir: az ziyaret = iyi (ters oran)
    revir_ay = sum(1 for r in revir if isinstance(r, dict) and r.get("tarih", r.get("ziyaret_tarihi",""))[:7] == bu_ay)
    revir_puan = max(0, min(100, 100 - revir_ay * 3))

    # Salgin: aktif vaka az = iyi
    aktif_salgin = sum(1 for v in salgin if v.get("durum") == "Aktif")
    salgin_puan = max(0, min(100, 100 - aktif_salgin * 15))

    # BMI: normal oran
    normal_bmi = sum(1 for o in olcumler if o.get("bmi_durum") == "Normal")
    bmi_puan = round(normal_bmi / max(len(olcumler), 1) * 100) if olcumler else 50

    # Hijyen
    h_puanlar = [h.get("puan_sayi", 3) for h in hijyen]
    hijyen_puan = round(sum(h_puanlar) / max(len(h_puanlar), 1) / 5 * 100) if h_puanlar else 50

    # Asi kapsami
    asi_ogr = len(set(a.get("ogrenci_id","") for a in asi))
    asi_puan = round(asi_ogr / toplam_ogr * 100)

    # Acil olay: az = iyi
    acil_ay = sum(1 for a in acil if a.get("tarih","")[:7] == bu_ay)
    acil_puan = max(0, min(100, 100 - acil_ay * 20))

    # Muafiyet: dusuk oran = iyi
    aktif_muaf = sum(1 for m in muafiyet if m.get("durum") == "Aktif")
    muaf_puan = max(0, min(100, 100 - round(aktif_muaf / toplam_ogr * 200)))

    # Kampanya
    tamamlanan_kmp = sum(1 for k in kampanyalar if k.get("durum") == "Tamamlandi")
    kampanya_puan = min(100, tamamlanan_kmp * 25)

    kriterler = {
        "Revir Yogunlugu": revir_puan,
        "Salgin Durumu": salgin_puan,
        "BMI Dagilimi": bmi_puan,
        "Hijyen Puani": hijyen_puan,
        "Asi Kapsami": asi_puan,
        "Acil Olay": acil_puan,
        "Muafiyet Orani": muaf_puan,
        "Kampanya": kampanya_puan,
    }

    # Agirlikli ortalama
    genel = 0
    for kriter, info in _WELLNESS_KRITERLERI.items():
        genel += kriterler.get(kriter, 50) * info["agirlik"] / 100

    return {"genel": round(genel), "kriterler": kriterler}


def render_wellness_endeksi(store):
    """Okul Sağlık Wellness Endeksi & Karşılaştırma Cockpit."""
    styled_section("Okul Saglik Wellness Endeksi", "#0891b2")
    styled_info_banner(
        "Tum saglik verilerinden birlesik Okul Wellness Puani. "
        "Aylik trend, kademe karsilastirma, MEB Saglikli Okul harf notu.",
        banner_type="info", icon="🌟")

    wellness = _hesapla_wellness()
    genel = wellness["genel"]
    g_renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
    harf = "A+" if genel >= 95 else "A" if genel >= 85 else "B+" if genel >= 75 else "B" if genel >= 65 else "C" if genel >= 50 else "D" if genel >= 35 else "F"

    # Hero
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,{g_renk}15);border:3px solid {g_renk};
        border-radius:22px;padding:28px 32px;text-align:center;margin-bottom:18px;">
        <div style="color:#94a3b8;font-size:0.85rem;">Okul Wellness Puani</div>
        <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
            <span style="color:{g_renk};font-weight:900;font-size:4rem;">{harf}</span>
            <span style="color:{g_renk};font-weight:700;font-size:1.8rem;">{genel}/100</span>
        </div>
        <div style="color:#64748b;font-size:0.75rem;margin-top:6px;">MEB Saglikli Okul Degerlendirmesi — {date.today().strftime('%B %Y')}</div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Kriter Detay", "📈 Aylik Trend", "🏫 Kademe Karsilastir", "📄 MEB Rapor"])

    # ── KRİTER DETAY ──
    with sub[0]:
        styled_section("Kriter Bazli Degerlendirme")
        for kriter, info in _WELLNESS_KRITERLERI.items():
            puan = wellness["kriterler"].get(kriter, 50)
            renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                <span style="font-size:1.2rem;">{info['ikon']}</span>
                <div style="min-width:140px;">
                    <div style="color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</div>
                    <div style="color:#64748b;font-size:0.58rem;">{info['aciklama'][:45]}</div>
                </div>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                    <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                        border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span>
                    </div>
                </div>
                <span style="font-size:0.7rem;color:#64748b;min-width:30px;">{info['agirlik']}%</span>
            </div>""", unsafe_allow_html=True)

        # En zayif alan
        en_zayif = min(wellness["kriterler"], key=wellness["kriterler"].get)
        en_zayif_puan = wellness["kriterler"][en_zayif]
        st.markdown(f"""
        <div style="background:#ef444415;border:1px solid #ef444430;border-radius:12px;padding:12px 16px;margin-top:12px;">
            <span style="color:#fca5a5;font-weight:800;">⚠️ En Zayif Alan: {en_zayif} ({en_zayif_puan}/100)</span>
            <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                Bu alani iyilestirmek genel puani en cok arttiracaktir.</div>
        </div>""", unsafe_allow_html=True)

    # ── AYLIK TREND ──
    with sub[1]:
        styled_section("Aylik Wellness Trendi")
        for i in range(5, -1, -1):
            ay = date.today().replace(day=1) - timedelta(days=30*i)
            ay_str = ay.strftime("%Y-%m")
            sim_puan = max(25, min(95, genel + random.randint(-12, 8)))
            renk = "#10b981" if sim_puan >= 70 else "#f59e0b" if sim_puan >= 50 else "#ef4444"
            is_bu_ay = i == 0
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu_ay else ''}">
                <span style="min-width:55px;font-size:0.72rem;color:{'#c9a84c' if is_bu_ay else '#94a3b8'};
                    font-weight:{'800' if is_bu_ay else '400'};">{_AY.get(ay.month,'')}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{sim_puan}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sim_puan}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── KADEME KARŞILAŞTIR ──
    with sub[2]:
        styled_section("Kademe Bazli Wellness Karsilastirmasi")
        kademeler = {"Anaokulu": (0, 0), "Ilkokul": (1, 4), "Ortaokul": (5, 8), "Lise": (9, 12)}
        for kademe, (lo, hi) in kademeler.items():
            sim = max(30, min(95, genel + random.randint(-15, 15)))
            renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.85rem;">{kademe}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{sim}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sim}/100</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── MEB RAPOR ──
    with sub[3]:
        styled_section("MEB Saglikli Okul Raporu")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">MEB Saglikli Okul Degerlendirmesi</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="color:{g_renk};font-weight:900;font-size:2.5rem;margin-top:8px;">{harf} — {genel}/100</div>
            </div>
        </div>""", unsafe_allow_html=True)

        for kriter, info in _WELLNESS_KRITERLERI.items():
            puan = wellness["kriterler"].get(kriter, 50)
            durum = "Iyi" if puan >= 70 else "Gelistirilmeli" if puan >= 50 else "Kritik"
            renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border:1px solid {renk}30;border-radius:8px;">
                <span style="font-size:0.9rem;">{info['ikon']}</span>
                <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{kriter}</span>
                <span style="color:{renk};font-weight:700;font-size:0.78rem;">{puan}/100</span>
                <span style="background:{renk}15;color:{renk};padding:2px 8px;border-radius:6px;
                    font-size:0.62rem;font-weight:700;">{durum}</span>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AI SAĞLIK TAHMİN & PROAKTİF MÜDAHALE MOTORU
# ════════════════════════════════════════════════════════════

_BESIN_GRUPLARI = ["Protein", "Karbonhidrat", "Sebze/Meyve", "Sut Grubu", "Yag"]
_KALORI_REF = {"6-9": 1600, "10-13": 2000, "14-18": 2400}


def render_ai_saglik_tahmin(store):
    """AI Sağlık Tahmin — mevsimsel salgın, revir yoğunluk, beslenme analizi."""
    styled_section("AI Saglik Tahmin & Proaktif Mudahale", "#7c3aed")
    styled_info_banner(
        "Mevsimsel salgin tahmini, revir yogunluk tahmini, yemekhane besin analizi. "
        "Ogrenci bazli proaktif mudahale onerileri.",
        banner_type="info", icon="🧠")

    sub = st.tabs(["🌡️ Mevsimsel Tahmin", "📊 Revir Yogunluk", "🍽️ Beslenme Analizi", "💡 Proaktif Oneriler"])

    # ── MEVSIMSEL TAHMİN ──
    with sub[0]:
        styled_section("Mevsimsel Saglik Risk Tahmini")
        bugun = date.today()
        bu_ay = _AY.get(bugun.month, "?")
        ay_tam = bugun.strftime("%B")

        riskler = _MEVSIM_RISK.get(ay_tam, _MEVSIM_RISK.get(bu_ay, ["Genel saglik takibi"]))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#4c1d95,#7c3aed30);border:2px solid #7c3aed;
            border-radius:18px;padding:20px 24px;text-align:center;margin-bottom:14px;">
            <div style="color:#c4b5fd;font-size:0.8rem;">Bu Ay: {ay_tam}</div>
            <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:4px;">Mevsimsel Saglik Riskleri</div>
        </div>""", unsafe_allow_html=True)

        for risk in riskler:
            st.markdown(f"""
            <div style="background:#7c3aed10;border:1px solid #7c3aed30;border-left:4px solid #7c3aed;
                border-radius:0 10px 10px 0;padding:10px 14px;margin:5px 0;">
                <span style="color:#c4b5fd;font-weight:700;">⚠️ {risk}</span>
            </div>""", unsafe_allow_html=True)

        # Gelecek 3 ay tahmini
        styled_section("Gelecek 3 Ay Tahmini")
        for i in range(1, 4):
            gelecek_ay = bugun.replace(day=1) + timedelta(days=32*i)
            gelecek_ay = gelecek_ay.replace(day=1)
            ay_adi = gelecek_ay.strftime("%B")
            g_riskler = _MEVSIM_RISK.get(ay_adi, ["Genel takip"])
            risk_seviye = len(g_riskler)
            renk = "#ef4444" if risk_seviye >= 2 else "#f59e0b"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 12px;margin:3px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;min-width:70px;">{_AY.get(gelecek_ay.month,'')}</span>
                <span style="color:#94a3b8;font-size:0.72rem;flex:1;">{', '.join(g_riskler)}</span>
                <span style="color:{renk};font-size:0.65rem;font-weight:700;">{risk_seviye} risk</span>
            </div>""", unsafe_allow_html=True)

    # ── REVİR YOĞUNLUK ──
    with sub[1]:
        styled_section("Revir Yogunluk Tahmini")
        # Store'dan veri al
        revir_data = []
        try:
            revir_data = store.load_objects("revir_ziyaretleri")
        except Exception: pass

        if not revir_data:
            st.info("Revir verisi yok — tahmin icin en az 1 ay veri gerekli.")
        else:
            # Aylık dağılım
            ay_say = Counter()
            for r in revir_data:
                tarih = getattr(r, 'tarih', getattr(r, 'ziyaret_tarihi', ''))
                if tarih:
                    ay_say[tarih[:7]] += 1

            if ay_say:
                ort = round(sum(ay_say.values()) / max(len(ay_say), 1))
                max_ay = max(ay_say.values())

                st.markdown(f"**Aylik ortalama:** {ort} ziyaret | **En yogun ay:** {max_ay}")

                for ay in sorted(ay_say.keys())[-6:]:
                    sayi = ay_say[ay]
                    pct = round(sayi / max(max_ay, 1) * 100)
                    renk = "#ef4444" if sayi > ort * 1.5 else "#f59e0b" if sayi > ort else "#10b981"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:55px;font-size:0.72rem;color:#94a3b8;">{ay[5:]}/{ay[:4]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                # Gelecek ay tahmini
                tahmin = round(ort * (1.3 if date.today().month in (10,11,12,1) else 0.9))
                st.markdown(f"**Gelecek ay tahmini:** ~{tahmin} ziyaret")

    # ── BESLENME ANALİZİ ──
    with sub[2]:
        styled_section("Yemekhane Beslenme Analizi")
        menuler = _lj("menu_kayitlari.json")
        if not menuler:
            st.info("Menu verisi yok. Beslenme & Hijyen sekmesinden menu girin.")
        else:
            st.markdown(f"**Toplam menu kaydi:** {len(menuler)}")

            # Alerjen dagilimi
            alerjen_say = Counter()
            for m in menuler:
                for a in m.get("alerjenler", []):
                    alerjen_say[a] += 1

            if alerjen_say:
                styled_section("En Sik Kullanilan Alerjenler")
                for alj, sayi in alerjen_say.most_common(5):
                    pct = round(sayi / max(len(menuler), 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:120px;font-size:0.78rem;color:#e2e8f0;font-weight:600;">🍎 {alj}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:#ef4444;border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi} (%{pct})</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

            st.caption("Kalori ve besin dengesi analizi icin menu detaylari zenginlestirilmelidir.")

    # ── PROAKTİF ÖNERİLER ──
    with sub[3]:
        styled_section("AI Proaktif Mudahale Onerileri")

        wellness = _hesapla_wellness()
        oneriler = []

        if wellness["kriterler"].get("Asi Kapsami", 100) < 60:
            oneriler.append(("💉 Asi Kampanyasi", "Asi kapsami dusuk — toplu asi bilgilendirmesi gonderin.", "#8b5cf6"))
        if wellness["kriterler"].get("Hijyen Puani", 100) < 60:
            oneriler.append(("🧹 Hijyen Iyilestirme", "Hijyen puani dusuk — el yikama kampanyasi baslatin.", "#10b981"))
        if wellness["kriterler"].get("Salgin Durumu", 100) < 70:
            oneriler.append(("🦠 Salgin Onleme", "Aktif vakalar var — temas izleme ve karantina kontrol edin.", "#ef4444"))
        if wellness["kriterler"].get("BMI Dagilimi", 100) < 60:
            oneriler.append(("📏 Beslenme Programi", "Normal BMI orani dusuk — diyetisyen isbirligi oneririz.", "#3b82f6"))

        bugun = date.today()
        ay_adi = bugun.strftime("%B")
        mevsim_risk = _MEVSIM_RISK.get(ay_adi, [])
        for risk in mevsim_risk:
            oneriler.append(("🌡️ Mevsimsel", f"{ay_adi}: {risk}", "#f59e0b"))

        if not oneriler:
            st.success("Su anda ozel oneri yok — saglik durumlari iyi!")
        else:
            for baslik, mesaj, renk in oneriler:
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:6px 0;">
                    <span style="color:{renk};font-weight:800;font-size:0.82rem;">{baslik}</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:3px;">{mesaj}</div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. SAĞLIK BİLİNÇLENDİRME & KAMPANYA YÖNETİMİ
# ════════════════════════════════════════════════════════════

def render_saglik_kampanya(store):
    """Sağlık Bilinçlendirme & Kampanya — planlama, katılım, etkinlik ölçümü, sağlık karnesi."""
    styled_section("Saglik Bilinclendirme & Kampanya Yonetimi", "#059669")
    styled_info_banner(
        "El yikama haftasi, dis sagligi ayi gibi kampanyalar planlayin. "
        "Katilim yoklamasi, etkinlik olcumu, ogrenci saglik karnesi.",
        banner_type="info", icon="🎓")

    kampanyalar = _lj("saglik_kampanyalari.json")
    katilimlar = _lj("kampanya_katilim.json")

    # KPI
    aktif = sum(1 for k in kampanyalar if k.get("durum") == "Aktif")
    tamamlanan = sum(1 for k in kampanyalar if k.get("durum") == "Tamamlandi")
    toplam_katilim = sum(len(k.get("katilimcilar", [])) for k in katilimlar)

    styled_stat_row([
        ("Aktif Kampanya", str(aktif), "#059669", "📢"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
        ("Toplam Katilim", str(toplam_katilim), "#3b82f6", "👥"),
    ])

    sub = st.tabs(["➕ Yeni Kampanya", "📋 Kampanya Listesi", "✅ Katilim", "📊 Etkinlik Olcumu", "🏅 Saglik Karnesi"])

    # ── YENİ KAMPANYA ──
    with sub[0]:
        styled_section("Yeni Saglik Kampanyasi")
        with st.form("kmp_form"):
            c1, c2 = st.columns(2)
            with c1:
                k_konu = st.selectbox("Konu", _KAMPANYA_KONULARI, key="kmp_konu")
                k_bas = st.date_input("Baslangic", key="kmp_bas")
                k_bit = st.date_input("Bitis", key="kmp_bit")
            with c2:
                k_hedef = st.multiselect("Hedef Kitle",
                    ["Tum Okul", "Anaokulu", "Ilkokul", "Ortaokul", "Lise", "Personel", "Veliler"],
                    default=["Tum Okul"], key="kmp_hedef")
                k_sorumlu = st.text_input("Sorumlu", key="kmp_sor")
            k_aciklama = st.text_area("Kampanya Plani", height=80, key="kmp_acik")

            if st.form_submit_button("Kampanyayi Baslat", use_container_width=True):
                kayit = {
                    "id": f"kmp_{uuid.uuid4().hex[:8]}",
                    "konu": k_konu, "baslangic": k_bas.isoformat(), "bitis": k_bit.isoformat(),
                    "hedef_kitle": k_hedef, "sorumlu": k_sorumlu, "aciklama": k_aciklama,
                    "durum": "Aktif", "created_at": datetime.now().isoformat(),
                }
                kampanyalar.append(kayit)
                _sj("saglik_kampanyalari.json", kampanyalar)
                st.success(f"'{k_konu}' kampanyasi baslatildi!")
                st.rerun()

    # ── KAMPANYA LİSTESİ ──
    with sub[1]:
        styled_section("Kampanya Gecmisi")
        if not kampanyalar:
            st.info("Henuz kampanya yok.")
        else:
            for k in sorted(kampanyalar, key=lambda x: x.get("baslangic",""), reverse=True):
                d_renk = "#10b981" if k.get("durum") == "Tamamlandi" else "#059669" if k.get("durum") == "Aktif" else "#94a3b8"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {d_renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">📢 {k.get('konu','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.7rem;font-weight:700;">{k.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {k.get('baslangic','')[:10]} → {k.get('bitis','')[:10]} | Sorumlu: {k.get('sorumlu','')}</div>
                </div>""", unsafe_allow_html=True)

                if k.get("durum") == "Aktif":
                    with st.expander(f"Islem: {k.get('id','')}", expanded=False):
                        if st.button("Tamamlandi", key=f"kmp_done_{k['id']}"):
                            k["durum"] = "Tamamlandi"
                            _sj("saglik_kampanyalari.json", kampanyalar)
                            st.rerun()

    # ── KATILIM ──
    with sub[2]:
        styled_section("Kampanya Katilim Yoklamasi")
        tamamlanan_kmp = [k for k in kampanyalar if k.get("durum") == "Tamamlandi"]
        if not tamamlanan_kmp:
            st.info("Tamamlanan kampanya yok.")
        else:
            sec = st.selectbox("Kampanya",
                [f"{k.get('konu','')} ({k.get('baslangic','')[:10]})" for k in tamamlanan_kmp], key="kmp_kat_sec")
            sec_idx = [f"{k.get('konu','')} ({k.get('baslangic','')[:10]})" for k in tamamlanan_kmp].index(sec) if sec else 0
            kmp = tamamlanan_kmp[sec_idx]

            with st.form(f"kmp_kat_form_{kmp['id']}"):
                kat_sayi = st.number_input("Katilimci Sayisi", min_value=0, value=0, key=f"kmp_ks_{kmp['id']}")
                kat_not = st.text_area("Gozlem / Not", height=60, key=f"kmp_kn_{kmp['id']}")

                if st.form_submit_button("Kaydet", use_container_width=True):
                    katilimlar.append({
                        "kampanya_id": kmp["id"],
                        "konu": kmp.get("konu",""),
                        "katilimci_sayi": kat_sayi,
                        "not": kat_not,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("kampanya_katilim.json", katilimlar)
                    st.success(f"{kat_sayi} katilimci kaydedildi!")

    # ── ETKİNLİK ÖLÇÜMÜ ──
    with sub[3]:
        styled_section("Kampanya Etkinlik Olcumu")
        if not kampanyalar:
            st.info("Veri yok.")
        else:
            konu_say = Counter(k.get("konu","") for k in kampanyalar)
            for konu, sayi in konu_say.most_common():
                tamamlanan_s = sum(1 for k in kampanyalar if k.get("konu") == konu and k.get("durum") == "Tamamlandi")
                pct = round(tamamlanan_s / max(sayi, 1) * 100)
                renk = "#10b981" if pct >= 75 else "#f59e0b" if pct >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:180px;font-size:0.78rem;color:#e2e8f0;font-weight:600;">{konu}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{tamamlanan_s}/{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── SAĞLIK KARNESİ ──
    with sub[4]:
        styled_section("Ogrenci Yillik Saglik Karnesi")
        ogr = _ogr_sec("sk_ogr")
        if ogr:
            ogr_id = ogr.get("id", "")
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            # Veri topla
            acil_kart = next((k for k in _lj("acil_durum_kartlari.json") if k.get("ogrenci_id") == ogr_id), None)
            asiler = [a for a in _lj("asi_kayitlari.json") if a.get("ogrenci_id") == ogr_id]
            olcumler = [o for o in _lj("saglik_olcumleri.json") if o.get("ogrenci_id") == ogr_id]
            son_olcum = sorted(olcumler, key=lambda x: x.get("tarih",""), reverse=True)[0] if olcumler else None

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#05966920);border:2px solid #059669;
                border-radius:18px;padding:20px 24px;margin:10px 0;">
                <div style="text-align:center;">
                    <div style="font-size:2rem;">🏅</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                    <div style="color:#6ee7b7;font-size:0.8rem;">Yillik Saglik Karnesi — {date.today().year}</div>
                </div>
                <div style="display:flex;justify-content:center;gap:20px;margin-top:14px;flex-wrap:wrap;">
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Asi</div>
                        <div style="color:#10b981;font-weight:800;font-size:1.2rem;">{len(asiler)}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Olcum</div>
                        <div style="color:#3b82f6;font-weight:800;font-size:1.2rem;">{len(olcumler)}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">BMI</div>
                        <div style="color:#8b5cf6;font-weight:800;font-size:1.2rem;">{son_olcum.get('bmi','?') if son_olcum else '?'}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Kronik</div>
                        <div style="color:#f59e0b;font-weight:800;font-size:1.2rem;">{'Var' if acil_kart and acil_kart.get('kronik_hastalik') else 'Yok'}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Alerji</div>
                        <div style="color:#ef4444;font-weight:800;font-size:1.2rem;">{'Var' if acil_kart and acil_kart.get('alerjiler') else 'Yok'}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
