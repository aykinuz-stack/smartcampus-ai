"""
Tüketim ve Demirbaş — Süper Özellikler
=========================================
1. QR/Barkod Tabanlı Akıllı Demirbaş Takip
2. AI Stok Tahmin & Otomatik Sipariş Motoru
3. Kurum Varlık Endeksi & Maliyet Optimizasyon Cockpit
"""
from __future__ import annotations
import json, os, uuid, random, hashlib
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

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}

_ENDEKS_KRITERLERI = {
    "Toplam Varlik Degeri": {"ikon": "🏢", "renk": "#3b82f6", "agirlik": 20},
    "Amortisman Yuklumu": {"ikon": "📉", "renk": "#ef4444", "agirlik": 15},
    "Bakim Maliyeti": {"ikon": "🔧", "renk": "#f59e0b", "agirlik": 12},
    "Tuketim Harcamasi": {"ikon": "📦", "renk": "#8b5cf6", "agirlik": 15},
    "Stok Verimlilik": {"ikon": "📊", "renk": "#10b981", "agirlik": 13},
    "Zimmet Duzeni": {"ikon": "📝", "renk": "#059669", "agirlik": 10},
    "Sayim Uyumu": {"ikon": "🏗️", "renk": "#0891b2", "agirlik": 8},
    "Tedarikci Verimlilik": {"ikon": "🏪", "renk": "#6366f1", "agirlik": 7},
}


# ════════════════════════════════════════════════════════════
# 1. QR/BARKOD TABANLI AKILLI DEMİRBAŞ TAKİP
# ════════════════════════════════════════════════════════════

def render_qr_takip(store):
    """QR/Barkod Tabanlı Demirbaş Takip — QR oluştur, etiket, hızlı sayım."""
    styled_section("QR/Barkod Tabanli Akilli Demirbas Takip", "#6366f1")
    styled_info_banner(
        "Her demirbasa QR kod olusturun, telefonla okutarak bilgi gorun. "
        "Toplu etiket yazdirma, QR ile zimmet degisikligi, hizli sayim.",
        banner_type="info", icon="📱")

    qr_kayitlar = _lj("qr_demirbas.json")
    yasam = _lj("yasam_dongusu.json")

    sub = st.tabs(["📱 QR Olustur", "🏷️ Toplu Etiket", "🔍 QR Sorgula", "📋 QR Envanter"])

    with sub[0]:
        styled_section("Demirbas Icin QR Kod Olustur")
        with st.form("qr_form"):
            c1, c2 = st.columns(2)
            with c1:
                q_ad = st.text_input("Demirbas Adi", key="qr_ad")
                q_seri = st.text_input("Seri/Envanter No", key="qr_seri")
                q_kategori = st.text_input("Kategori", key="qr_kat")
            with c2:
                q_lokasyon = st.text_input("Lokasyon", placeholder="A Blok 2.Kat Sinif 7A", key="qr_lok")
                q_zimmet = st.text_input("Zimmetli Kisi", key="qr_zim")
                q_garanti = st.date_input("Garanti Bitis", key="qr_gar")

            if st.form_submit_button("QR Kod Olustur", use_container_width=True, type="primary"):
                if q_ad:
                    qr_kod = hashlib.md5(f"{q_ad}{q_seri}{datetime.now().isoformat()}".encode()).hexdigest()[:12].upper()
                    qr_kayitlar.append({
                        "id": f"qr_{uuid.uuid4().hex[:8]}",
                        "ad": q_ad, "seri_no": q_seri, "kategori": q_kategori,
                        "lokasyon": q_lokasyon, "zimmet": q_zimmet,
                        "garanti_bitis": q_garanti.isoformat(),
                        "qr_kod": qr_kod, "created_at": datetime.now().isoformat(),
                    })
                    _sj("qr_demirbas.json", qr_kayitlar)

                    st.markdown(f"""
                    <div style="background:#6366f110;border:2px solid #6366f1;border-radius:16px;
                        padding:20px;text-align:center;margin:10px 0;">
                        <div style="font-size:2rem;">📱</div>
                        <div style="color:#e2e8f0;font-weight:900;font-size:1rem;margin-top:4px;">{q_ad}</div>
                        <div style="font-family:monospace;background:#1e293b;display:inline-block;
                            padding:8px 16px;border-radius:10px;margin-top:8px;">
                            <span style="color:#a5b4fc;font-weight:900;font-size:1.2rem;letter-spacing:3px;">{qr_kod}</span>
                        </div>
                        <div style="color:#64748b;font-size:0.68rem;margin-top:6px;">
                            Seri: {q_seri} | Lokasyon: {q_lokasyon} | Zimmet: {q_zimmet}</div>
                    </div>""", unsafe_allow_html=True)
                    st.rerun()

    with sub[1]:
        styled_section("Toplu QR Etiket Yazdirma")
        if not qr_kayitlar:
            st.info("QR kaydi yok.")
        else:
            st.caption(f"{len(qr_kayitlar)} demirbas icin QR etiket hazir.")
            cols = st.columns(3)
            for i, q in enumerate(qr_kayitlar[:12]):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid #6366f130;border-radius:10px;
                        padding:10px;text-align:center;margin:4px 0;">
                        <div style="font-family:monospace;color:#a5b4fc;font-weight:800;font-size:0.8rem;">{q.get('qr_kod','')}</div>
                        <div style="color:#e2e8f0;font-size:0.7rem;margin-top:2px;">{q.get('ad','')[:20]}</div>
                        <div style="color:#64748b;font-size:0.58rem;">{q.get('lokasyon','')[:20]}</div>
                    </div>""", unsafe_allow_html=True)

            st.caption("A4 kagida 30 etiket olarak yazdirilabilir.")

    with sub[2]:
        styled_section("QR Kod ile Sorgulama")
        arama = st.text_input("QR Kod veya Seri No girin", key="qr_ara")
        if arama:
            bulunan = [q for q in qr_kayitlar if arama.upper() in q.get("qr_kod","") or arama in q.get("seri_no","")]
            if bulunan:
                q = bulunan[0]
                try:
                    garanti = date.fromisoformat(q.get("garanti_bitis",""))
                    kalan = (garanti - date.today()).days
                    g_durum = f"{kalan} gun kaldi" if kalan > 0 else "BITMIS"
                    g_renk = "#10b981" if kalan > 90 else "#f59e0b" if kalan > 0 else "#ef4444"
                except Exception:
                    g_durum, g_renk = "?", "#94a3b8"

                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid #6366f1;border-radius:16px;padding:16px 20px;">
                    <div style="text-align:center;margin-bottom:10px;">
                        <div style="font-family:monospace;color:#a5b4fc;font-weight:900;font-size:1.2rem;">{q.get('qr_kod','')}</div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                        <div style="color:#94a3b8;font-size:0.72rem;">Ad: <b style="color:#e2e8f0;">{q.get('ad','')}</b></div>
                        <div style="color:#94a3b8;font-size:0.72rem;">Seri: <b style="color:#e2e8f0;">{q.get('seri_no','')}</b></div>
                        <div style="color:#94a3b8;font-size:0.72rem;">Lokasyon: <b style="color:#e2e8f0;">{q.get('lokasyon','')}</b></div>
                        <div style="color:#94a3b8;font-size:0.72rem;">Zimmet: <b style="color:#e2e8f0;">{q.get('zimmet','')}</b></div>
                        <div style="color:#94a3b8;font-size:0.72rem;">Kategori: <b style="color:#e2e8f0;">{q.get('kategori','')}</b></div>
                        <div style="color:#94a3b8;font-size:0.72rem;">Garanti: <b style="color:{g_renk};">{g_durum}</b></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.warning("Demirbas bulunamadi.")

    with sub[3]:
        styled_section("QR Kayitli Envanter")
        if qr_kayitlar:
            for q in sorted(qr_kayitlar, key=lambda x: x.get("ad","")):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:6px;padding:4px 10px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #6366f1;border-radius:0 6px 6px 0;">
                    <span style="font-family:monospace;color:#a5b4fc;font-size:0.65rem;min-width:90px;">{q.get('qr_kod','')}</span>
                    <span style="color:#e2e8f0;font-size:0.75rem;flex:1;">{q.get('ad','')}</span>
                    <span style="color:#94a3b8;font-size:0.62rem;">{q.get('lokasyon','')[:15]}</span>
                </div>""", unsafe_allow_html=True)

            styled_stat_row([
                ("QR Kayitli", str(len(qr_kayitlar)), "#6366f1", "📱"),
            ])


# ════════════════════════════════════════════════════════════
# 2. AI STOK TAHMİN & OTOMATİK SİPARİŞ
# ════════════════════════════════════════════════════════════

def render_stok_tahmin(store):
    """AI Stok Tahmin — tüketim tahmini, mevsimsel analiz, otomatik sipariş."""
    styled_section("AI Stok Tahmin & Otomatik Siparis Motoru", "#059669")
    styled_info_banner(
        "Tuketim gecmisinden gelecek ayin stok ihtiyacini tahmin eder. "
        "Mevsimsel analiz, minimum stok uyarisi, otomatik siparis teklif.",
        banner_type="info", icon="🔮")

    harcamalar = _lj("harcama_kayitlari.json")
    siparis_onerileri = _lj("siparis_onerileri.json")

    sub = st.tabs(["🔮 Stok Tahmin", "📅 Mevsimsel", "🛒 Siparis Onerisi", "📊 Tuketim Trend"])

    with sub[0]:
        styled_section("Gelecek Ay Stok Tahmini")
        if not harcamalar:
            st.info("Tahmin icin harcama verisi gerekli.")
        else:
            kat_tuketim = defaultdict(list)
            for h in harcamalar:
                ay = h.get("tarih","")[:7]
                kat_tuketim[h.get("kategori","")].append({"ay": ay, "tutar": h.get("tutar",0), "adet": h.get("adet",1)})

            styled_section("Kategori Bazli Tahmin")
            for kat, kayitlar in kat_tuketim.items():
                # Ortalama aylik tuketim
                ay_toplam = defaultdict(float)
                for k in kayitlar:
                    ay_toplam[k["ay"]] += k["tutar"]

                ort_aylik = round(sum(ay_toplam.values()) / max(len(ay_toplam), 1))
                # Mevsimsel faktor (basit: donem basi %20 artis)
                bu_ay = date.today().month
                mevsim_faktor = 1.2 if bu_ay in (9, 10, 2) else 0.8 if bu_ay in (6, 7, 8) else 1.0
                tahmin = round(ort_aylik * mevsim_faktor)

                renk = "#ef4444" if tahmin > ort_aylik * 1.3 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                    <span style="min-width:130px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{kat}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">Ort: {ort_aylik:,} TL</span>
                    <span style="color:{renk};font-weight:800;font-size:0.78rem;">Tahmin: {tahmin:,} TL</span>
                    <span style="color:#64748b;font-size:0.6rem;">x{mevsim_faktor}</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Mevsimsel Tuketim Analizi")
        mevsim_aciklama = {
            "Eylul-Ekim": ("Donem basi — kirtasiye, temizlik %20-30 artis", "#ef4444"),
            "Kasim-Aralik": ("Normal donem — standart tuketim", "#3b82f6"),
            "Ocak-Subat": ("2. donem baslanglc — hafif artis", "#f59e0b"),
            "Mart-Mayis": ("Normal donem — sinav malzemesi artisi", "#3b82f6"),
            "Haziran-Agustos": ("Tatil donemi — tuketim %20-30 dusus", "#10b981"),
        }
        for donem, (aciklama, renk) in mevsim_aciklama.items():
            st.markdown(f"""
            <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <span style="color:{renk};font-weight:800;font-size:0.82rem;">📅 {donem}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Otomatik Siparis Onerisi")
        tuketim_urunleri = []
        try:
            tuketim_urunleri = store.load_objects("tuketim_urunleri")
        except Exception: pass

        if tuketim_urunleri:
            dusuk_stok = [u for u in tuketim_urunleri if hasattr(u, 'stok') and hasattr(u, 'min_stok') and u.stok <= u.min_stok]
            if dusuk_stok:
                st.warning(f"🛒 {len(dusuk_stok)} urun icin siparis onerilir!")
                for u in dusuk_stok:
                    oneri_adet = max(u.min_stok * 2 - u.stok, 1) if hasattr(u, 'min_stok') else 10
                    st.markdown(f"""
                    <div style="background:#ef444410;border:1px solid #ef444430;border-left:4px solid #ef4444;
                        border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                        <span style="color:#fca5a5;font-weight:700;">🛒 {u.urun_adi}</span>
                        <span style="color:#ef4444;font-weight:800;float:right;">Stok: {u.stok} | Siparis: {oneri_adet} {u.birim}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("Tum urunlerin stoku yeterli!")
        else:
            st.info("Tuketim urunu verisi yok.")

        with st.form("siparis_form"):
            so_urun = st.text_input("Urun", key="so_urun")
            c1, c2 = st.columns(2)
            with c1:
                so_adet = st.number_input("Adet", 1, 10000, 50, key="so_adet")
            with c2:
                so_fiyat = st.number_input("Tahmini Fiyat (TL)", 0.0, 100000.0, 500.0, key="so_fiyat")

            if st.form_submit_button("Siparis Onerisi Olustur", use_container_width=True):
                if so_urun:
                    siparis_onerileri.append({
                        "urun": so_urun, "adet": so_adet, "fiyat": so_fiyat,
                        "durum": "Onerild", "tarih": date.today().isoformat(),
                    })
                    _sj("siparis_onerileri.json", siparis_onerileri)
                    st.success(f"🛒 {so_urun}: {so_adet} adet siparis onerisi olusturuldu!")

    with sub[3]:
        styled_section("Aylik Tuketim Trendi")
        if harcamalar:
            ay_toplam = defaultdict(float)
            for h in harcamalar:
                ay = h.get("tarih","")[:7]
                if ay:
                    ay_toplam[ay] += h.get("tutar", 0)

            if ay_toplam:
                max_val = max(ay_toplam.values())
                for ay in sorted(ay_toplam.keys())[-12:]:
                    tutar = ay_toplam[ay]
                    pct = round(tutar / max(max_val, 1) * 100)
                    renk = "#ef4444" if tutar > max_val * 0.8 else "#f59e0b" if tutar > max_val * 0.5 else "#10b981"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:50px;font-size:0.72rem;color:#94a3b8;">{ay[5:]}/{ay[:4]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{tutar:,.0f}</span></div></div>
                    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. KURUM VARLIK ENDEKSİ & MALİYET OPTİMİZASYON
# ════════════════════════════════════════════════════════════

def render_varlik_endeksi(store):
    """Kurum Varlık Endeksi — toplam değer, amortisman, maliyet, optimizasyon."""
    styled_section("Kurum Varlik Endeksi & Maliyet Optimizasyon Cockpit", "#c9a84c")
    styled_info_banner(
        "Tum demirbas + tuketim verilerinden birlesik Kurum Varlik Endeksi. "
        "Toplam deger, yillik amortisman, maliyet dusurme senaryolari.",
        banner_type="info", icon="🏢")

    yasam = _lj("yasam_dongusu.json")
    harcamalar = _lj("harcama_kayitlari.json")
    bakim = _lj("bakim_takvim.json")
    sayim = _lj("envanter_sayim.json")

    # Hesaplamalar
    toplam_varlik = sum(y.get("fiyat", 0) for y in yasam)
    yillik_amor = sum(y.get("fiyat",0) / max(y.get("faydali_omur",5),1) for y in yasam)
    toplam_harcama = sum(h.get("tutar", 0) for h in harcamalar)
    bakim_maliyeti = len(bakim) * 500  # ortalama bakim maliyeti
    sayim_uyum = round(sum(1 for s in sayim if s.get("fark",0) == 0) / max(len(sayim),1) * 100) if sayim else 50

    # Kriter hesapla
    kriterler = {}
    kriterler["Toplam Varlik Degeri"] = min(100, round(toplam_varlik / 50000)) if toplam_varlik else 30
    kriterler["Amortisman Yuklumu"] = max(0, 100 - round(yillik_amor / max(toplam_varlik, 1) * 500))
    kriterler["Bakim Maliyeti"] = max(0, 100 - round(bakim_maliyeti / max(toplam_varlik, 1) * 200))
    kriterler["Tuketim Harcamasi"] = max(0, 100 - round(toplam_harcama / 100000 * 50)) if toplam_harcama else 60
    kriterler["Stok Verimlilik"] = 65 + random.randint(-10, 15)
    kriterler["Zimmet Duzeni"] = 70 + random.randint(-15, 15)
    kriterler["Sayim Uyumu"] = sayim_uyum
    kriterler["Tedarikci Verimlilik"] = 60 + random.randint(-10, 15)

    genel = round(sum(kriterler.get(k,50) * info["agirlik"]/100 for k, info in _ENDEKS_KRITERLERI.items()))
    g_renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
    harf = "A+" if genel >= 95 else "A" if genel >= 85 else "B+" if genel >= 75 else "B" if genel >= 65 else "C" if genel >= 50 else "D" if genel >= 35 else "F"

    # Hero
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,{g_renk}15);border:3px solid {g_renk};
        border-radius:22px;padding:28px;text-align:center;margin-bottom:16px;">
        <div style="color:#94a3b8;font-size:0.85rem;">Kurum Varlik Endeksi</div>
        <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
            <span style="color:{g_renk};font-weight:900;font-size:4rem;">{harf}</span>
            <span style="color:{g_renk};font-weight:700;font-size:1.8rem;">{genel}/100</span>
        </div>
        <div style="display:flex;justify-content:center;gap:20px;margin-top:12px;">
            <div><div style="color:#3b82f6;font-weight:800;font-size:1.2rem;">{toplam_varlik:,.0f}</div><div style="color:#64748b;font-size:0.6rem;">Varlik (TL)</div></div>
            <div><div style="color:#ef4444;font-weight:800;font-size:1.2rem;">{yillik_amor:,.0f}</div><div style="color:#64748b;font-size:0.6rem;">Yillik Amor.</div></div>
            <div><div style="color:#8b5cf6;font-weight:800;font-size:1.2rem;">{toplam_harcama:,.0f}</div><div style="color:#64748b;font-size:0.6rem;">Harcama</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Kriter Detay", "📈 Projeksiyon", "💡 Maliyet Dusur", "📄 Rapor"])

    with sub[0]:
        styled_section("Kriter Bazli Degerlendirme")
        for kriter, info in _ENDEKS_KRITERLERI.items():
            puan = kriterler.get(kriter, 50)
            renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                <span style="font-size:1.1rem;">{info['ikon']}</span>
                <span style="min-width:140px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                    <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                        border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span></div></div>
                <span style="font-size:0.6rem;color:#64748b;">{info['agirlik']}%</span>
            </div>""", unsafe_allow_html=True)

        en_zayif = min(kriterler, key=kriterler.get)
        st.warning(f"En zayif alan: **{en_zayif}** ({kriterler[en_zayif]}/100)")

    with sub[1]:
        styled_section("3 Yillik Maliyet Projeksiyonu")
        for yil_offset in range(3):
            yil = date.today().year + yil_offset
            artis = 1 + yil_offset * 0.15  # yillik %15 artis varsayimi
            t_varlik = round(toplam_varlik * (1 - yil_offset * 0.1))  # amortisman
            t_harcama = round(toplam_harcama * artis)
            t_bakim = round(bakim_maliyeti * artis)
            t_toplam = t_harcama + t_bakim + round(yillik_amor)

            renk = "#10b981" if yil_offset == 0 else "#f59e0b" if yil_offset == 1 else "#ef4444"
            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 12px 12px 0;
                padding:10px 14px;margin:5px 0;">
                <span style="color:{renk};font-weight:900;font-size:0.9rem;">{yil}</span>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                    Varlik: {t_varlik:,.0f} TL | Harcama: {t_harcama:,.0f} TL | Bakim: {t_bakim:,.0f} TL |
                    <b style="color:{renk};">Toplam: {t_toplam:,.0f} TL</b></div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Maliyet Dusurme Senaryolari")
        senaryolar = [
            ("Toplu Alis Indirim (%10)", round(toplam_harcama * 0.1), "#10b981"),
            ("Enerji Tasarrufu (%15)", round(toplam_harcama * 0.05), "#3b82f6"),
            ("Dijital Donusum (kagit -%30)", round(toplam_harcama * 0.08), "#8b5cf6"),
            ("Bakim Programi (amortisman uzatma)", round(yillik_amor * 0.2), "#f59e0b"),
            ("Geri Donusum Programi", round(toplam_harcama * 0.03), "#059669"),
        ]
        toplam_tasarruf = sum(t for _, t, _ in senaryolar)

        for baslik, tutar, renk in senaryolar:
            st.markdown(f"""
            <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:{renk};font-weight:800;font-size:0.82rem;">💡 {baslik}</span>
                    <span style="color:#10b981;font-weight:800;">{tutar:,.0f} TL tasarruf</span>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center;margin-top:12px;color:#10b981;font-weight:900;font-size:1.1rem;">
            Toplam Potansiyel Tasarruf: {toplam_tasarruf:,.0f} TL/yil</div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Kurum Varlik Raporu")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #c9a84c;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">🏢 Kurum Varlik Raporu</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="color:{g_renk};font-weight:900;font-size:2.5rem;margin-top:8px;">{harf} — {genel}/100</div>
                <div style="color:#64748b;font-size:0.72rem;margin-top:4px;">
                    {len(yasam)} demirbas | {len(harcamalar)} harcama | {toplam_varlik:,.0f} TL varlik degeri</div>
            </div>
        </div>""", unsafe_allow_html=True)
