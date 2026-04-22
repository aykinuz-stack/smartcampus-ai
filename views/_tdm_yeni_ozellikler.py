"""
Tüketim ve Demirbaş — Yeni Özellikler
========================================
1. Demirbaş Yaşam Döngüsü & Amortisman Takibi
2. Harcama Analizi & Bütçe Karşılaştırma Cockpit
3. Envanter Sayım & Lokasyon Haritası
"""
from __future__ import annotations
import json, os, uuid, random, math
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "tuketim_demirbas"); os.makedirs(d, exist_ok=True); return d
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

_YASAM_ASAMALARI = ["Satin Alindi", "Aktif Kullanim", "Bakimda", "Amortize", "Hurda/Ayiklama"]
_YASAM_RENK = {"Satin Alindi":"#3b82f6","Aktif Kullanim":"#10b981","Bakimda":"#f59e0b","Amortize":"#8b5cf6","Hurda/Ayiklama":"#64748b"}

_AMORTISMAN_YONTEM = {"Dogrusal": "Yillik esit tutar", "Azalan Bakiye": "Ilk yillarda yuksek, sonra azalan"}
_BAKIM_PERIYOT = ["Aylik", "3 Aylik", "6 Aylik", "Yillik", "Ihtiyac Halinde"]

_HARCAMA_KATEGORILERI = ["Kirtasiye", "Temizlik", "Yiyecek/Icecek", "Elektrik/Su", "Bakim/Onarim",
    "Bilgi Teknolojileri", "Egitim Malzemesi", "Ofis Malzemesi", "Diger"]

_LOKASYONLAR = {
    "A Blok": {"katlar": ["Zemin", "1. Kat", "2. Kat", "3. Kat"]},
    "B Blok": {"katlar": ["Zemin", "1. Kat", "2. Kat"]},
    "C Blok (Spor)": {"katlar": ["Zemin"]},
    "Yemekhane": {"katlar": ["Zemin"]},
    "Kutuphane": {"katlar": ["Zemin", "1. Kat"]},
    "Idare": {"katlar": ["Zemin", "1. Kat"]},
}


# ════════════════════════════════════════════════════════════
# 1. DEMİRBAŞ YAŞAM DÖNGÜSÜ & AMORTİSMAN
# ════════════════════════════════════════════════════════════

def render_yasam_dongusu(store):
    """Demirbaş Yaşam Döngüsü — amortisman, garanti, bakım, MEB taşınır."""
    styled_section("Demirbas Yasam Dongusu & Amortisman Takibi", "#8b5cf6")
    styled_info_banner(
        "Satin alma → kullanim → bakim → amortisman → hurda yasam dongusu. "
        "Amortisman hesaplama, garanti suresi, periyodik bakim, MEB uyum.",
        banner_type="info", icon="🔄")

    yasam_kayitlari = _lj("yasam_dongusu.json")
    bakim_kayitlari = _lj("bakim_takvim.json")

    demirbaslar = []
    try:
        demirbaslar = store.load_objects("demirbaslar")
    except Exception: pass

    sub = st.tabs(["🔄 Yasam Durumu", "📊 Amortisman", "🔧 Bakim Takvim", "⚠️ Garanti Takip", "📄 MEB Tasinir"])

    with sub[0]:
        styled_section("Demirbas Yasam Dongusu Durumu")
        if not yasam_kayitlari and not demirbaslar:
            st.info("Demirbas verisi yok.")
        else:
            # Yasam asamasi kaydi
            with st.form("yasam_form"):
                c1, c2 = st.columns(2)
                with c1:
                    y_ad = st.text_input("Demirbas Adi", key="yd_ad")
                    y_asama = st.selectbox("Yasam Asamasi", _YASAM_ASAMALARI, key="yd_asama")
                with c2:
                    y_fiyat = st.number_input("Satin Alma Fiyati (TL)", 0.0, 1000000.0, 5000.0, key="yd_fiyat")
                    y_tarih = st.date_input("Satin Alma Tarihi", key="yd_tarih")
                y_omur = st.number_input("Faydali Omur (yil)", 1, 20, 5, key="yd_omur")

                if st.form_submit_button("Kaydet", use_container_width=True):
                    if y_ad:
                        yasam_kayitlari.append({
                            "id": f"yd_{uuid.uuid4().hex[:8]}",
                            "ad": y_ad, "asama": y_asama,
                            "fiyat": y_fiyat, "satin_alma": y_tarih.isoformat(),
                            "faydali_omur": y_omur,
                            "created_at": datetime.now().isoformat(),
                        })
                        _sj("yasam_dongusu.json", yasam_kayitlari)
                        st.success(f"🔄 {y_ad} — {y_asama}")
                        st.rerun()

            # Asama dagilimi
            if yasam_kayitlari:
                asama_say = Counter(y.get("asama","") for y in yasam_kayitlari)
                for asama in _YASAM_ASAMALARI:
                    sayi = asama_say.get(asama, 0)
                    renk = _YASAM_RENK.get(asama, "#94a3b8")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                        <span style="min-width:120px;color:{renk};font-weight:700;font-size:0.82rem;">{asama}</span>
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{sayi}</span>
                    </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Amortisman Hesaplama")
        if not yasam_kayitlari:
            st.info("Yasam dongusu kaydi yok.")
        else:
            for y in yasam_kayitlari:
                fiyat = y.get("fiyat", 0)
                omur = max(y.get("faydali_omur", 5), 1)
                try:
                    satin_alma = date.fromisoformat(y.get("satin_alma",""))
                    gecen_yil = (date.today() - satin_alma).days / 365.25
                except Exception:
                    gecen_yil = 0

                # Dogrusal amortisman
                yillik = round(fiyat / omur, 2)
                toplam_amor = round(min(yillik * gecen_yil, fiyat), 2)
                kalan_deger = round(max(fiyat - toplam_amor, 0), 2)
                amor_pct = round(toplam_amor / max(fiyat, 1) * 100)

                renk = "#ef4444" if amor_pct >= 80 else "#f59e0b" if amor_pct >= 50 else "#10b981"

                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{y.get('ad','')}</span>
                        <span style="color:{renk};font-weight:800;">%{amor_pct} amortize</span>
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:8px;margin:6px 0;overflow:hidden;">
                        <div style="width:{amor_pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;">
                        Alinma: {fiyat:,.0f} TL | Kalan: {kalan_deger:,.0f} TL | Yillik: {yillik:,.0f} TL | {round(gecen_yil,1)}/{omur} yil</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Periyodik Bakim Takvimi")
        with st.form("bakim_form"):
            c1, c2 = st.columns(2)
            with c1:
                b_demirbas = st.text_input("Demirbas", key="bk_dem")
                b_periyot = st.selectbox("Bakim Periyodu", _BAKIM_PERIYOT, key="bk_per")
            with c2:
                b_son = st.date_input("Son Bakim Tarihi", key="bk_son")
                b_sonraki = st.date_input("Sonraki Bakim", key="bk_sonraki")
            b_not = st.text_input("Bakim Notu", key="bk_not")

            if st.form_submit_button("Bakim Kaydet", use_container_width=True):
                if b_demirbas:
                    bakim_kayitlari.append({
                        "demirbas": b_demirbas, "periyot": b_periyot,
                        "son_bakim": b_son.isoformat(), "sonraki": b_sonraki.isoformat(),
                        "not": b_not, "tarih": datetime.now().isoformat(),
                    })
                    _sj("bakim_takvim.json", bakim_kayitlari)
                    st.success(f"🔧 {b_demirbas} bakim kaydedildi!")
                    st.rerun()

        if bakim_kayitlari:
            styled_section("Yaklasan Bakimlar")
            bugun = date.today().isoformat()
            for b in sorted(bakim_kayitlari, key=lambda x: x.get("sonraki","")):
                gecikme = b.get("sonraki","") < bugun
                renk = "#ef4444" if gecikme else "#f59e0b" if b.get("sonraki","")[:10] <= (date.today() + timedelta(days=30)).isoformat() else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">🔧 {b.get('demirbas','')}</span>
                    <span style="color:#94a3b8;font-size:0.65rem;">{b.get('periyot','')}</span>
                    <span style="color:{renk};font-size:0.65rem;font-weight:700;">
                        {'GECİKMİŞ!' if gecikme else b.get('sonraki','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Garanti Suresi Takibi")
        if yasam_kayitlari:
            for y in yasam_kayitlari:
                try:
                    satin_alma = date.fromisoformat(y.get("satin_alma",""))
                    garanti_bitis = satin_alma + timedelta(days=365*2)  # 2 yil varsayilan
                    kalan_gun = (garanti_bitis - date.today()).days
                    gecmis = kalan_gun < 0
                except Exception:
                    kalan_gun, gecmis = 0, True

                renk = "#ef4444" if gecmis else "#f59e0b" if kalan_gun < 90 else "#10b981"
                durum = "BITMIS" if gecmis else f"{kalan_gun} gun kaldi"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">{y.get('ad','')}</span>
                    <span style="color:{renk};font-size:0.68rem;font-weight:700;">{durum}</span>
                </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("MEB Tasinir Mal Yonetimi Uyumu")
        meb_kriterler = [
            ("Tasinir Kayit Defteri tutuldu", len(yasam_kayitlari) > 0),
            ("Zimmet fisletri guncellendi", True),
            ("Amortisman hesaplandi", len(yasam_kayitlari) > 0),
            ("Hurda/ayiklama islemi yapildi", any(y.get("asama") == "Hurda/Ayiklama" for y in yasam_kayitlari)),
            ("Periyodik bakim takibi yapiliyor", len(bakim_kayitlari) > 0),
            ("Envanter sayimi tamamlandi", False),
        ]
        karsilanan = sum(1 for _, ok in meb_kriterler if ok)
        for madde, ok in meb_kriterler:
            ikon = "✅" if ok else "❌"
            renk = "#10b981" if ok else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:4px 12px;margin:2px 0;
                background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                <span>{ikon}</span>
                <span style="color:#e2e8f0;font-size:0.78rem;">{madde}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"**Uyumluluk: {karsilanan}/{len(meb_kriterler)}**")


# ════════════════════════════════════════════════════════════
# 2. HARCAMA ANALİZİ & BÜTÇE KARŞILAŞTIRMA
# ════════════════════════════════════════════════════════════

def render_harcama_analizi(store):
    """Harcama Analizi — kategori trend, bütçe vs gerçek, tedarikçi, israf."""
    styled_section("Harcama Analizi & Butce Karsilastirma Cockpit", "#2563eb")
    styled_info_banner(
        "Tuketim maddesi harcamalarinin aylik/donemsel trend analizi. "
        "Butce vs gerceklesen, israf tespiti, tasarruf onerisi.",
        banner_type="info", icon="📊")

    harcamalar = _lj("harcama_kayitlari.json")

    sub = st.tabs(["📊 Kategori Trend", "⚖️ Butce vs Gercek", "🏪 Tedarikci Analiz", "💡 Tasarruf Oneri", "📝 Harcama Kaydet"])

    with sub[0]:
        styled_section("Kategori Bazli Harcama Trendi")
        if not harcamalar:
            st.info("Harcama kaydi yok. 'Harcama Kaydet' sekmesinden baslatin.")
        else:
            kat_tutar = defaultdict(float)
            for h in harcamalar:
                kat_tutar[h.get("kategori","")] += h.get("tutar", 0)

            toplam = sum(kat_tutar.values())
            for kat, tutar in sorted(kat_tutar.items(), key=lambda x: x[1], reverse=True):
                pct = round(tutar / max(toplam, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                    <span style="min-width:140px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{kat}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#2563eb;border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{tutar:,.0f} TL (%{pct})</span></div></div>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"**Toplam Harcama: {toplam:,.0f} TL**")

    with sub[1]:
        styled_section("Butce vs Gerceklesen Karsilastirma")
        st.caption("Kategorilerin butce ve gerceklesen tutarlarini karsilastirin.")
        with st.form("butce_form"):
            b_kat = st.selectbox("Kategori", _HARCAMA_KATEGORILERI, key="bk_kat")
            c1, c2 = st.columns(2)
            with c1:
                b_butce = st.number_input("Planlanan Butce (TL)", 0.0, 1000000.0, 10000.0, key="bk_but")
            with c2:
                b_gercek = st.number_input("Gerceklesen (TL)", 0.0, 1000000.0, 8000.0, key="bk_ger")

            if st.form_submit_button("Karsilastir", use_container_width=True):
                fark = b_gercek - b_butce
                oran = round(b_gercek / max(b_butce, 1) * 100)
                renk = "#10b981" if oran <= 100 else "#f59e0b" if oran <= 120 else "#ef4444"

                st.markdown(f"""
                <div style="display:flex;gap:16px;margin:14px 0;">
                    <div style="flex:1;background:#0f172a;border:1px solid #334155;border-radius:14px;padding:14px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.72rem;">Butce</div>
                        <div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{b_butce:,.0f} TL</div>
                    </div>
                    <div style="flex:1;background:#0f172a;border:2px solid {renk};border-radius:14px;padding:14px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.72rem;">Gerceklesen (%{oran})</div>
                        <div style="color:{renk};font-weight:900;font-size:1.5rem;">{b_gercek:,.0f} TL</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                if fark > 0:
                    st.warning(f"⚠️ {b_kat} kategorisinde {fark:,.0f} TL butce asimi!")
                else:
                    st.success(f"✅ {b_kat} kategorisinde {abs(fark):,.0f} TL tasarruf!")

    with sub[2]:
        styled_section("Tedarikci Fiyat Analizi")
        if harcamalar:
            ted_tutar = defaultdict(float)
            ted_say = Counter()
            for h in harcamalar:
                ted = h.get("tedarikci","Belirtilmemis")
                ted_tutar[ted] += h.get("tutar", 0)
                ted_say[ted] += 1

            for ted in sorted(ted_tutar.keys(), key=lambda x: ted_tutar[x], reverse=True):
                tutar = ted_tutar[ted]
                sayi = ted_say[ted]
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #2563eb;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">🏪 {ted}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{sayi} islem</span>
                    <span style="color:#2563eb;font-weight:800;">{tutar:,.0f} TL</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Tasarruf Onerileri")
        oneriler = [
            ("📄 Dijital Donusum", "Fotokopi/kagit kullanimi yuksek — dijital dokuman sistemi kurun", "#3b82f6"),
            ("♻️ Geri Donusum", "Tek kullanimlik urunler yerine yeniden kullanilabilir tercih edin", "#10b981"),
            ("📦 Toplu Alis", "Sik tuketilen urunleri toplu aliarak birim fiyat dusurun", "#f59e0b"),
            ("⚡ Enerji Tasarrufu", "LED aydinlatma, hareket sensorlu isik, zamanlayici klima", "#8b5cf6"),
            ("🔧 Bakim Programi", "Duzgun bakim demirbas omrunu uzatir, yenileme maliyetini dusurur", "#059669"),
        ]
        for baslik, aciklama, renk in oneriler:
            st.markdown(f"""
            <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <span style="color:{renk};font-weight:800;font-size:0.82rem;">{baslik}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Harcama Kaydi Ekle")
        with st.form("harcama_form"):
            c1, c2 = st.columns(2)
            with c1:
                h_kat = st.selectbox("Kategori", _HARCAMA_KATEGORILERI, key="hk_kat")
                h_urun = st.text_input("Urun/Hizmet", key="hk_urun")
                h_tutar = st.number_input("Tutar (TL)", 0.0, 1000000.0, 100.0, key="hk_tutar")
            with c2:
                h_ted = st.text_input("Tedarikci", key="hk_ted")
                h_tarih = st.date_input("Tarih", key="hk_tarih")
                h_adet = st.number_input("Adet", 1, 10000, 1, key="hk_adet")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if h_urun:
                    harcamalar.append({
                        "id": f"hk_{uuid.uuid4().hex[:8]}",
                        "kategori": h_kat, "urun": h_urun,
                        "tutar": h_tutar, "tedarikci": h_ted,
                        "adet": h_adet, "tarih": h_tarih.isoformat(),
                    })
                    _sj("harcama_kayitlari.json", harcamalar)
                    st.success(f"💰 {h_urun}: {h_tutar:,.0f} TL kaydedildi!")
                    st.rerun()


# ════════════════════════════════════════════════════════════
# 3. ENVANTER SAYIM & LOKASYON HARİTASI
# ════════════════════════════════════════════════════════════

def render_envanter_sayim(store):
    """Envanter Sayım — bina/kat/oda bazlı, sayım fark, kayıp/hasar, transfer."""
    styled_section("Envanter Sayim & Lokasyon Haritasi", "#059669")
    styled_info_banner(
        "Yillik envanter sayim, bina/kat/oda bazli demirbas lokasyon haritasi. "
        "Sayim fark raporu, kayip/hasar bildirimi, transfer kaydi.",
        banner_type="info", icon="🏗️")

    sayim_kayitlari = _lj("envanter_sayim.json")
    lokasyon_kayitlari = _lj("demirbas_lokasyon.json")
    transfer_kayitlari = _lj("demirbas_transfer.json")

    sub = st.tabs(["📋 Sayim Yap", "🗺️ Lokasyon Haritasi", "🔄 Transfer", "📊 Fark Raporu", "⚠️ Kayip/Hasar"])

    with sub[0]:
        styled_section("Envanter Sayim")
        with st.form("sayim_form"):
            c1, c2 = st.columns(2)
            with c1:
                s_bina = st.selectbox("Bina", list(_LOKASYONLAR.keys()), key="sy_bina")
                s_kat = st.selectbox("Kat", _LOKASYONLAR.get(s_bina, {}).get("katlar", ["Zemin"]), key="sy_kat")
                s_oda = st.text_input("Oda/Mekan", placeholder="Sinif 7A, Mudur Odasi...", key="sy_oda")
            with c2:
                s_sayan = st.text_input("Sayan Kisi", key="sy_sayan")
                s_tarih = st.date_input("Sayim Tarihi", key="sy_tarih")
            s_beklenen = st.number_input("Beklenen Adet", 0, 1000, 20, key="sy_bek")
            s_bulunan = st.number_input("Bulunan Adet", 0, 1000, 20, key="sy_bul")
            s_not = st.text_area("Sayim Notu", height=40, key="sy_not")

            if st.form_submit_button("Sayim Kaydet", use_container_width=True, type="primary"):
                fark = s_bulunan - s_beklenen
                sayim_kayitlari.append({
                    "id": f"sy_{uuid.uuid4().hex[:8]}",
                    "bina": s_bina, "kat": s_kat, "oda": s_oda,
                    "sayan": s_sayan, "tarih": s_tarih.isoformat(),
                    "beklenen": s_beklenen, "bulunan": s_bulunan,
                    "fark": fark, "not": s_not,
                })
                _sj("envanter_sayim.json", sayim_kayitlari)
                renk = "#10b981" if fark == 0 else "#ef4444"
                st.success(f"Sayim: {s_bina} > {s_kat} > {s_oda} — Fark: {fark}")
                st.rerun()

    with sub[1]:
        styled_section("Bina/Kat Bazli Lokasyon Haritasi")
        for bina, info in _LOKASYONLAR.items():
            bina_sayim = [s for s in sayim_kayitlari if s.get("bina") == bina]
            toplam_bul = sum(s.get("bulunan", 0) for s in bina_sayim)
            toplam_fark = sum(s.get("fark", 0) for s in bina_sayim)
            renk = "#10b981" if toplam_fark == 0 else "#f59e0b" if toplam_fark > -3 else "#ef4444"

            st.markdown(f"""
            <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 12px 12px 0;
                padding:10px 14px;margin:6px 0;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🏢 {bina}</span>
                    <span style="color:{renk};font-size:0.72rem;font-weight:700;">
                        {toplam_bul} demirbas | Fark: {toplam_fark}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                    Katlar: {', '.join(info['katlar'])} | {len(bina_sayim)} sayim</div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Demirbas Transfer Kaydi")
        with st.form("transfer_form"):
            c1, c2 = st.columns(2)
            with c1:
                t_demirbas = st.text_input("Demirbas", key="tr_dem")
                t_kaynak = st.text_input("Kaynak Lokasyon", placeholder="A Blok 2.Kat Sinif 7A", key="tr_kay")
            with c2:
                t_hedef = st.text_input("Hedef Lokasyon", placeholder="B Blok 1.Kat Lab", key="tr_hed")
                t_tarih = st.date_input("Transfer Tarihi", key="tr_tarih")
            t_neden = st.text_input("Transfer Nedeni", key="tr_ned")

            if st.form_submit_button("Transfer Kaydet", use_container_width=True):
                if t_demirbas:
                    transfer_kayitlari.append({
                        "demirbas": t_demirbas, "kaynak": t_kaynak, "hedef": t_hedef,
                        "tarih": t_tarih.isoformat(), "neden": t_neden,
                    })
                    _sj("demirbas_transfer.json", transfer_kayitlari)
                    st.success(f"🔄 {t_demirbas}: {t_kaynak} → {t_hedef}")
                    st.rerun()

        if transfer_kayitlari:
            for t in sorted(transfer_kayitlari, key=lambda x: x.get("tarih",""), reverse=True)[:8]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:6px;padding:4px 10px;margin:2px 0;
                    background:#0f172a;border-left:2px solid #059669;border-radius:0 6px 6px 0;">
                    <span style="color:#e2e8f0;font-size:0.75rem;flex:1;">🔄 {t.get('demirbas','')}</span>
                    <span style="color:#94a3b8;font-size:0.62rem;">{t.get('kaynak','')} → {t.get('hedef','')}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Sayim Fark Raporu")
        if not sayim_kayitlari:
            st.info("Sayim verisi yok.")
        else:
            fark_var = [s for s in sayim_kayitlari if s.get("fark", 0) != 0]
            tam = [s for s in sayim_kayitlari if s.get("fark", 0) == 0]

            styled_stat_row([
                ("Toplam Sayim", str(len(sayim_kayitlari)), "#059669", "📋"),
                ("Tam Eslesme", str(len(tam)), "#10b981", "✅"),
                ("Fark Var", str(len(fark_var)), "#ef4444", "⚠️"),
            ])

            if fark_var:
                for s in sorted(fark_var, key=lambda x: abs(x.get("fark",0)), reverse=True):
                    fark = s.get("fark", 0)
                    renk = "#ef4444" if fark < 0 else "#f59e0b"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                        background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">
                            {s.get('bina','')} > {s.get('kat','')} > {s.get('oda','')}</span>
                        <span style="color:#94a3b8;font-size:0.65rem;">Beklenen: {s.get('beklenen',0)}</span>
                        <span style="color:{renk};font-weight:800;font-size:0.75rem;">
                            Fark: {'+' if fark > 0 else ''}{fark}</span>
                    </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Kayip / Hasar Bildirimi")
        fark_eksi = [s for s in sayim_kayitlari if s.get("fark", 0) < 0]
        if fark_eksi:
            toplam_kayip = sum(abs(s.get("fark",0)) for s in fark_eksi)
            st.error(f"🚨 {len(fark_eksi)} lokasyonda toplam {toplam_kayip} eksik demirbas!")
            for s in fark_eksi:
                st.markdown(f"""
                <div style="background:#ef444410;border:1px solid #ef444430;border-left:4px solid #ef4444;
                    border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                    <span style="color:#fca5a5;font-weight:700;">⚠️ {s.get('bina','')} > {s.get('oda','')}</span>
                    <span style="color:#ef4444;font-weight:800;float:right;">{abs(s.get('fark',0))} eksik</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Kayip/hasar bildirimi yok — tum demirbaslar yerinde!")
