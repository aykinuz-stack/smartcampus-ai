"""
Sosyal Etkinlik ve Kulüpler — Yeni Özellikler
===============================================
1. Kulüp Performans Karnesi & Üye Katılım Analizi
2. Yıllık Etkinlik Takvimi & Bütçe Planlama
3. Öğrenci Sosyal Gelişim Portfolyosu & Yetkinlik Haritası
"""
from __future__ import annotations
import json, os, uuid
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _sd():
    d = os.path.join(get_tenant_dir(), "sosyal_etkinlik"); os.makedirs(d, exist_ok=True); return d
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

_YETKINLIK_ALANLARI = {
    "Liderlik": {"ikon": "👑", "renk": "#f59e0b"},
    "Takim Calismasi": {"ikon": "🤝", "renk": "#10b981"},
    "Iletisim": {"ikon": "💬", "renk": "#3b82f6"},
    "Yaraticilik": {"ikon": "🎨", "renk": "#8b5cf6"},
    "Sorumluluk": {"ikon": "✅", "renk": "#059669"},
    "Problem Cozme": {"ikon": "🧩", "renk": "#0891b2"},
}


# ════════════════════════════════════════════════════════════
# 1. KULÜP PERFORMANS KARNESİ & ÜYE KATILIM ANALİZİ
# ════════════════════════════════════════════════════════════

def render_kulup_performans(store):
    """Kulüp Performans Karnesi — faaliyet gerçekleşme, üye katılım, liderlik tablosu."""
    styled_section("Kulup Performans Karnesi & Uye Katilim Analizi", "#7c3aed")
    styled_info_banner(
        "Her kulubun faaliyet gerceklesme orani, uye devam yuzdesi, "
        "en aktif uyeler, donem sonu kulup karnesi.",
        banner_type="info", icon="🏆")

    kulupler = store.load_objects("kulupler")
    faaliyetler = store.load_objects("kulup_faaliyetler")
    katilim_kayitlari = _lj("kulup_katilim.json")

    aktif = [k for k in kulupler if k.durum == "AKTIF"]

    styled_stat_row([
        ("Aktif Kulup", str(len(aktif)), "#7c3aed", "🎭"),
        ("Toplam Faaliyet", str(len(faaliyetler)), "#3b82f6", "📋"),
        ("Katilim Kaydi", str(len(katilim_kayitlari)), "#10b981", "✅"),
    ])

    sub = st.tabs(["📊 Kulup Karnesi", "👥 Uye Katilim", "🏆 Liderlik Tablosu", "✅ Katilim Kaydet"])

    # ── KULÜP KARNESİ ──
    with sub[0]:
        styled_section("Kulup Bazli Performans Karnesi")
        if not aktif:
            st.info("Aktif kulup yok.")
        else:
            for k in aktif:
                k_faal = [f for f in faaliyetler if f.kulup_id == k.id]
                tamamlanan = sum(1 for f in k_faal if f.durum == "TAMAMLANDI")
                toplam = max(len(k_faal), 1)
                gerceklesme = round(tamamlanan / toplam * 100)
                uye_sayi = len(k.ogrenciler)

                # Katilim orani
                k_katilim = [kt for kt in katilim_kayitlari if kt.get("kulup_id") == k.id]
                ort_katilim = 0
                if k_katilim:
                    ort_katilim = round(sum(kt.get("katilan", 0) for kt in k_katilim) /
                                        max(sum(kt.get("toplam", 1) for kt in k_katilim), 1) * 100)

                genel = round((gerceklesme + ort_katilim) / 2)
                renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
                harf = "A" if genel >= 85 else "B" if genel >= 70 else "C" if genel >= 55 else "D" if genel >= 40 else "F"

                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid {renk};border-left:6px solid {renk};
                    border-radius:0 16px 16px 0;padding:14px 18px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#e2e8f0;font-weight:900;font-size:1rem;">🎭 {k.ad}</span>
                            <span style="color:#64748b;font-size:0.72rem;margin-left:8px;">{uye_sayi} uye</span>
                        </div>
                        <div style="text-align:center;">
                            <span style="color:{renk};font-weight:900;font-size:2rem;">{harf}</span>
                            <span style="color:{renk};font-size:0.8rem;margin-left:4px;">{genel}%</span>
                        </div>
                    </div>
                    <div style="display:flex;gap:20px;margin-top:10px;">
                        <div style="flex:1;">
                            <div style="color:#94a3b8;font-size:0.65rem;">Faaliyet Gerceklesme</div>
                            <div style="background:#1e293b;border-radius:4px;height:12px;margin-top:3px;overflow:hidden;">
                                <div style="width:{gerceklesme}%;height:100%;background:#3b82f6;border-radius:4px;"></div>
                            </div>
                            <div style="color:#64748b;font-size:0.6rem;">{tamamlanan}/{len(k_faal)} (%{gerceklesme})</div>
                        </div>
                        <div style="flex:1;">
                            <div style="color:#94a3b8;font-size:0.65rem;">Uye Katilim</div>
                            <div style="background:#1e293b;border-radius:4px;height:12px;margin-top:3px;overflow:hidden;">
                                <div style="width:{ort_katilim}%;height:100%;background:#10b981;border-radius:4px;"></div>
                            </div>
                            <div style="color:#64748b;font-size:0.6rem;">%{ort_katilim}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── ÜYE KATILIM ──
    with sub[1]:
        styled_section("Ogrenci Bazli Katilim Takibi")
        if not aktif:
            st.info("Kulup yok.")
        else:
            sec_kulup = st.selectbox("Kulup Sec", [k.ad for k in aktif], key="kp_kulup")
            kulup = next((k for k in aktif if k.ad == sec_kulup), None)
            if kulup and kulup.ogrenciler:
                ogr_katilim = defaultdict(lambda: {"katilan": 0, "toplam": 0})
                for kt in katilim_kayitlari:
                    if kt.get("kulup_id") == kulup.id:
                        for ogr_ad in kt.get("katilanlar", []):
                            ogr_katilim[ogr_ad]["katilan"] += 1
                        for ogr_ad in kulup.ogrenciler:
                            ad = ogr_ad.get("ad_soyad", "") if isinstance(ogr_ad, dict) else str(ogr_ad)
                            ogr_katilim[ad]["toplam"] += 1

                for ogr_ad in kulup.ogrenciler:
                    ad = ogr_ad.get("ad_soyad", "") if isinstance(ogr_ad, dict) else str(ogr_ad)
                    data = ogr_katilim.get(ad, {"katilan": 0, "toplam": 0})
                    oran = round(data["katilan"] / max(data["toplam"], 1) * 100)
                    renk = "#10b981" if oran >= 75 else "#f59e0b" if oran >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                        background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{ad}</span>
                        <span style="color:{renk};font-weight:700;font-size:0.75rem;">%{oran}</span>
                    </div>""", unsafe_allow_html=True)
            elif kulup:
                st.info("Bu kulupte uye yok.")

    # ── LİDERLİK TABLOSU ──
    with sub[2]:
        styled_section("En Aktif Uyeler")
        ogr_toplam = Counter()
        for kt in katilim_kayitlari:
            for ogr_ad in kt.get("katilanlar", []):
                ogr_toplam[ogr_ad] += 1

        if ogr_toplam:
            for sira, (ad, sayi) in enumerate(ogr_toplam.most_common(15), 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                renk = "#c9a84c" if sira <= 3 else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{ad}</span>
                    <span style="color:#c9a84c;font-weight:800;font-size:0.85rem;">{sayi} katilim</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Henuz katilim kaydi yok.")

    # ── KATILIM KAYDET ──
    with sub[3]:
        styled_section("Faaliyet Katilim Kaydi")
        if not aktif:
            st.info("Kulup yok.")
        else:
            with st.form("katilim_form"):
                c1, c2 = st.columns(2)
                with c1:
                    sec_k = st.selectbox("Kulup", [k.ad for k in aktif], key="kt_kulup")
                    kt_tarih = st.date_input("Tarih", key="kt_tarih")
                with c2:
                    kt_toplam = st.number_input("Toplam Uye", min_value=1, value=10, key="kt_toplam")
                    kt_katilan = st.number_input("Katilan", min_value=0, value=8, key="kt_katilan")

                kt_katilanlar = st.text_area("Katilan Ogrenciler (her satira bir isim)", height=80, key="kt_list")

                if st.form_submit_button("Kaydet", use_container_width=True):
                    kulup = next((k for k in aktif if k.ad == sec_k), None)
                    if kulup:
                        isimler = [i.strip() for i in kt_katilanlar.split("\n") if i.strip()]
                        kayit = {
                            "id": f"kt_{uuid.uuid4().hex[:8]}",
                            "kulup_id": kulup.id,
                            "kulup_ad": kulup.ad,
                            "tarih": kt_tarih.isoformat(),
                            "toplam": kt_toplam,
                            "katilan": kt_katilan,
                            "katilanlar": isimler,
                            "created_at": datetime.now().isoformat(),
                        }
                        katilim_kayitlari.append(kayit)
                        _sj("kulup_katilim.json", katilim_kayitlari)
                        st.success(f"{sec_k}: {kt_katilan}/{kt_toplam} katilim kaydedildi!")
                        st.rerun()


# ════════════════════════════════════════════════════════════
# 2. YILLIK ETKİNLİK TAKVİMİ & BÜTÇE PLANLAMA
# ════════════════════════════════════════════════════════════

def render_etkinlik_takvimi(store):
    """Yıllık Etkinlik Takvimi & Bütçe Planlama."""
    styled_section("Yillik Etkinlik Takvimi & Butce Planlama", "#2563eb")
    styled_info_banner(
        "Tum sosyal etkinliklerin yillik takvim gorunumu. "
        "Butce atama, harcama takibi, etkinlik sonrasi degerlendirme.",
        banner_type="info", icon="📅")

    etkinlikler = store.load_objects("etkinlikler")
    butce_kayitlari = _lj("etkinlik_butce.json")
    degerlendirmeler = _lj("etkinlik_degerlendirme.json")

    # KPI
    toplam_butce = sum(b.get("butce", 0) for b in butce_kayitlari)
    harcanan = sum(b.get("harcanan", 0) for b in butce_kayitlari)
    kalan = toplam_butce - harcanan

    styled_stat_row([
        ("Toplam Etkinlik", str(len(etkinlikler)), "#2563eb", "📋"),
        ("Planlanan Butce", f"{toplam_butce:,.0f} TL", "#8b5cf6", "💰"),
        ("Harcanan", f"{harcanan:,.0f} TL", "#f59e0b", "💳"),
        ("Kalan", f"{kalan:,.0f} TL", "#10b981" if kalan >= 0 else "#ef4444", "💵"),
    ])

    sub = st.tabs(["📅 Aylik Takvim", "💰 Butce Yonetimi", "📝 Degerlendirme", "📊 Butce Analizi"])

    # ── AYLIK TAKVİM ──
    with sub[0]:
        styled_section("Egitim Yili Etkinlik Takvimi")
        bugun = date.today()
        yil_bas = bugun.year if bugun.month >= 9 else bugun.year - 1
        ay_sirasi = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]

        for ay in ay_sirasi:
            yil = yil_bas if ay >= 9 else yil_bas + 1
            ay_str = f"{yil}-{ay:02d}"
            ay_etkinlikler = [e for e in etkinlikler if e.tarih_baslangic[:7] == ay_str]
            is_bu_ay = ay == bugun.month and yil == bugun.year
            renk = "#c9a84c" if is_bu_ay else "#334155"

            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                padding:8px 14px;margin:4px 0;{'border:1px solid #c9a84c;' if is_bu_ay else ''}">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:{'#c9a84c' if is_bu_ay else '#e2e8f0'};font-weight:{'900' if is_bu_ay else '600'};
                        font-size:0.85rem;">{'📌 ' if is_bu_ay else ''}{_AY.get(ay,'')} {yil}</span>
                    <span style="color:#94a3b8;font-size:0.72rem;">{len(ay_etkinlikler)} etkinlik</span>
                </div>
            </div>""", unsafe_allow_html=True)

            for e in sorted(ay_etkinlikler, key=lambda x: x.tarih_baslangic):
                durum_renk = "#10b981" if e.durum == "TAMAMLANDI" else "#3b82f6" if e.durum == "PLANLANDI" else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:6px;padding:3px 12px 3px 24px;margin:1px 0;
                    border-left:2px solid {durum_renk};">
                    <span style="min-width:50px;color:#64748b;font-size:0.65rem;">{e.tarih_baslangic[8:10]}.{e.tarih_baslangic[5:7]}</span>
                    <span style="color:#e2e8f0;font-size:0.75rem;font-weight:600;flex:1;">{e.baslik}</span>
                    <span style="color:{durum_renk};font-size:0.6rem;font-weight:700;">{e.durum}</span>
                </div>""", unsafe_allow_html=True)

    # ── BÜTÇE YÖNETİMİ ──
    with sub[1]:
        styled_section("Etkinlik Butce Atama")
        with st.form("butce_form"):
            if not etkinlikler:
                st.info("Etkinlik yok.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    b_etkinlik = st.selectbox("Etkinlik",
                        [f"{e.baslik} ({e.tarih_baslangic[:10]})" for e in etkinlikler], key="bt_etk")
                    b_butce = st.number_input("Planlanan Butce (TL)", min_value=0, value=5000, key="bt_butce")
                with c2:
                    b_harcanan = st.number_input("Harcanan (TL)", min_value=0, value=0, key="bt_harc")
                    b_kalem = st.text_input("Harcama Kalemi", placeholder="Ulasim, yemek, malzeme...", key="bt_kalem")

                if st.form_submit_button("Butce Kaydet", use_container_width=True):
                    kayit = {
                        "id": f"bt_{uuid.uuid4().hex[:8]}",
                        "etkinlik": b_etkinlik,
                        "butce": b_butce, "harcanan": b_harcanan,
                        "kalem": b_kalem,
                        "tarih": datetime.now().isoformat(),
                    }
                    butce_kayitlari.append(kayit)
                    _sj("etkinlik_butce.json", butce_kayitlari)
                    st.success("Butce kaydedildi!")
                    st.rerun()

        if butce_kayitlari:
            styled_section("Butce Kayitlari")
            for b in sorted(butce_kayitlari, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                kalan_b = b.get("butce",0) - b.get("harcanan",0)
                renk = "#10b981" if kalan_b > 0 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.75rem;flex:1;">{b.get('etkinlik','')[:40]}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">Butce: {b.get('butce',0):,} TL</span>
                    <span style="color:{renk};font-size:0.68rem;font-weight:700;">Kalan: {kalan_b:,} TL</span>
                </div>""", unsafe_allow_html=True)

    # ── DEĞERLENDİRME ──
    with sub[2]:
        styled_section("Etkinlik Sonrasi Degerlendirme")
        tamamlanan = [e for e in etkinlikler if e.durum == "TAMAMLANDI"]
        if not tamamlanan:
            st.info("Tamamlanan etkinlik yok.")
        else:
            with st.form("deger_form"):
                d_etkinlik = st.selectbox("Etkinlik",
                    [f"{e.baslik} ({e.tarih_baslangic[:10]})" for e in tamamlanan], key="dg_etk")
                d_puan = st.select_slider("Genel Degerlendirme", options=[1,2,3,4,5], value=4, key="dg_puan")
                d_katilim = st.number_input("Katilimci Sayisi", min_value=0, value=50, key="dg_kat")
                d_yorum = st.text_area("Degerlendirme Notu", height=60, key="dg_yorum")

                if st.form_submit_button("Kaydet", use_container_width=True):
                    degerlendirmeler.append({
                        "etkinlik": d_etkinlik, "puan": d_puan,
                        "katilimci": d_katilim, "yorum": d_yorum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("etkinlik_degerlendirme.json", degerlendirmeler)
                    st.success("Degerlendirme kaydedildi!")

    # ── BÜTÇE ANALİZİ ──
    with sub[3]:
        styled_section("Butce Kullanim Analizi")
        if butce_kayitlari:
            kullanim_oran = round(harcanan / max(toplam_butce, 1) * 100)
            renk = "#10b981" if kullanim_oran <= 80 else "#f59e0b" if kullanim_oran <= 100 else "#ef4444"
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid {renk};border-radius:16px;padding:20px;text-align:center;">
                <div style="color:#94a3b8;font-size:0.8rem;">Butce Kullanim Orani</div>
                <div style="color:{renk};font-weight:900;font-size:2.5rem;">%{kullanim_oran}</div>
                <div style="color:#64748b;font-size:0.72rem;">{harcanan:,.0f} / {toplam_butce:,.0f} TL</div>
            </div>""", unsafe_allow_html=True)

            # Kalem bazli
            kalem_say = Counter(b.get("kalem","Diger") for b in butce_kayitlari if b.get("kalem"))
            if kalem_say:
                styled_section("Harcama Kalemi Dagilimi")
                for kalem, sayi in kalem_say.most_common():
                    st.markdown(f"- **{kalem}**: {sayi} kayit")
        else:
            st.info("Butce verisi yok.")


# ════════════════════════════════════════════════════════════
# 3. ÖĞRENCİ SOSYAL GELİŞİM PORTFOLYOSU & YETKİNLİK HARİTASI
# ════════════════════════════════════════════════════════════

def render_sosyal_portfolyo(store):
    """Öğrenci Sosyal Gelişim Portfolyosu — kulüp, etkinlik, yetkinlik, CV."""
    styled_section("Ogrenci Sosyal Gelisim Portfolyosu", "#6366f1")
    styled_info_banner(
        "Her ogrencinin kulup uyelikleri, katildigi etkinlikler, aldigi gorevler, "
        "sosyal yetkinlik haritasi. Universite basvurusu icin aktivite CV'si.",
        banner_type="info", icon="🎯")

    kulupler = store.load_objects("kulupler")
    etkinlikler = store.load_objects("etkinlikler")
    katilim_kayitlari = _lj("kulup_katilim.json")
    yetkinlik_kayitlari = _lj("sosyal_yetkinlik.json")

    sub = st.tabs(["👤 Portfolyo Kart", "🗺️ Yetkinlik Haritasi", "📝 Yetkinlik Degerlendir", "📄 Aktivite CV"])

    # ── PORTFOLYO KART ──
    with sub[0]:
        styled_section("Ogrenci Sosyal Portfolyosu")
        ogr = _ogr_sec("sp_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            # Kulup uyelikleri
            uye_kulupler = []
            for k in kulupler:
                if k.durum == "AKTIF":
                    for ogr_k in k.ogrenciler:
                        ad = ogr_k.get("ad_soyad","") if isinstance(ogr_k, dict) else str(ogr_k)
                        if ogr_ad.lower() in ad.lower() or ad.lower() in ogr_ad.lower():
                            uye_kulupler.append(k.ad)

            # Etkinlik katilimi
            katilim_sayi = sum(1 for kt in katilim_kayitlari if ogr_ad in kt.get("katilanlar", []))

            # Yetkinlik
            ogr_yetkinlik = [y for y in yetkinlik_kayitlari if y.get("ogrenci_ad") == ogr_ad]

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,#6366f130);border:2px solid #6366f1;
                border-radius:20px;padding:20px 24px;margin:10px 0;">
                <div style="text-align:center;">
                    <div style="font-size:2rem;">🎯</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">{ogr_ad}</div>
                    <div style="color:#c4b5fd;font-size:0.8rem;">Sosyal Gelisim Portfolyosu</div>
                </div>
                <div style="display:flex;justify-content:center;gap:24px;margin-top:14px;">
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Kulup</div>
                        <div style="color:#8b5cf6;font-weight:900;font-size:1.5rem;">{len(uye_kulupler)}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Katilim</div>
                        <div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{katilim_sayi}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#94a3b8;font-size:0.65rem;">Yetkinlik</div>
                        <div style="color:#10b981;font-weight:900;font-size:1.5rem;">{len(ogr_yetkinlik)}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            if uye_kulupler:
                styled_section("Kulup Uyelikleri")
                for k in uye_kulupler:
                    st.markdown(f"- 🎭 **{k}**")

    # ── YETKİNLİK HARİTASI ──
    with sub[1]:
        styled_section("Sosyal Yetkinlik Haritasi")
        ogr2 = _ogr_sec("sp_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            ogr_yet = [y for y in yetkinlik_kayitlari if y.get("ogrenci_ad") == ogr_ad2]

            if not ogr_yet:
                st.info(f"{ogr_ad2} icin yetkinlik degerlendirmesi yok.")
            else:
                # Son degerlendirme
                son = sorted(ogr_yet, key=lambda x: x.get("tarih",""), reverse=True)[0]
                puanlar = son.get("puanlar", {})

                for alan, info in _YETKINLIK_ALANLARI.items():
                    puan = puanlar.get(alan, 0)
                    pct = round(puan / 10 * 100)
                    renk = "#10b981" if puan >= 7 else "#f59e0b" if puan >= 5 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                        <span style="font-size:1.2rem;">{info['ikon']}</span>
                        <span style="min-width:110px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{alan}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                                border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                                <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/10</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── YETKİNLİK DEĞERLENDİR ──
    with sub[2]:
        styled_section("Yetkinlik Degerlendirmesi Yap")
        with st.form("yet_form"):
            ogr3 = _ogr_sec("sp_ogr3")
            puanlar = {}
            for alan, info in _YETKINLIK_ALANLARI.items():
                puanlar[alan] = st.slider(f"{info['ikon']} {alan}", 1, 10, 5, key=f"yet_{alan}")

            yet_not = st.text_area("Degerlendirme Notu", height=60, key="yet_not")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if ogr3:
                    ogr_ad3 = f"{ogr3.get('ad','')} {ogr3.get('soyad','')}"
                    kayit = {
                        "id": f"yet_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr3.get("id", ""),
                        "ogrenci_ad": ogr_ad3,
                        "sinif": ogr3.get("sinif", ""),
                        "sube": ogr3.get("sube", ""),
                        "puanlar": puanlar,
                        "not": yet_not,
                        "tarih": datetime.now().isoformat(),
                    }
                    yetkinlik_kayitlari.append(kayit)
                    _sj("sosyal_yetkinlik.json", yetkinlik_kayitlari)
                    genel = round(sum(puanlar.values()) / max(len(puanlar), 1), 1)
                    st.success(f"{ogr_ad3} — Genel Yetkinlik: {genel}/10")
                    st.rerun()

    # ── AKTİVİTE CV ──
    with sub[3]:
        styled_section("Aktivite CV'si (Universite Basvurusu)")
        ogr4 = _ogr_sec("sp_ogr4")
        if ogr4:
            ogr_ad4 = f"{ogr4.get('ad','')} {ogr4.get('soyad','')}"

            uye_k = []
            for k in kulupler:
                if k.durum == "AKTIF":
                    for ok in k.ogrenciler:
                        ad = ok.get("ad_soyad","") if isinstance(ok, dict) else str(ok)
                        if ogr_ad4.lower() in ad.lower() or ad.lower() in ogr_ad4.lower():
                            uye_k.append(k)

            katilim_s = sum(1 for kt in katilim_kayitlari if ogr_ad4 in kt.get("katilanlar", []))
            ogr_y = sorted([y for y in yetkinlik_kayitlari if y.get("ogrenci_ad") == ogr_ad4],
                          key=lambda x: x.get("tarih",""), reverse=True)

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #6366f1;border-radius:16px;padding:20px 24px;">
                <div style="text-align:center;margin-bottom:14px;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">📄 Sosyal Aktivite CV</div>
                    <div style="color:#c4b5fd;font-size:0.85rem;">{ogr_ad4}</div>
                    <div style="color:#94a3b8;font-size:0.72rem;">{ogr4.get('sinif','')}/{ogr4.get('sube','')} — {date.today().year}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if uye_k:
                styled_section("Kulup Uyelikleri")
                for k in uye_k:
                    st.markdown(f"- 🎭 **{k.ad}** — {k.faaliyet_gunu or ''} {k.faaliyet_saati or ''}")

            st.markdown(f"**Etkinlik Katilimi:** {katilim_s} faaliyet")

            if ogr_y:
                son_y = ogr_y[0]
                puanlar = son_y.get("puanlar", {})
                styled_section("Yetkinlik Profili")
                for alan, puan in puanlar.items():
                    info = _YETKINLIK_ALANLARI.get(alan, {"ikon":"", "renk":"#94a3b8"})
                    st.markdown(f"- {info['ikon']} **{alan}**: {puan}/10")

            st.caption("Bu bilgiler universite basvurusu, burs basvurusu ve referans mektubu icin kullanilabilir.")
