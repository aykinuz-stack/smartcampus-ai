"""
AI Treni — Mega Özellikler
============================
1. Canlı Tren Simülasyonu & Multiplayer Quiz Düellosu
2. Öğretmen Makinist Paneli & Sınıf Kontrol Merkezi
3. Okul Arası Tren Ağı & Ulusal Sıralama
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "bilgi_treni"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_DERSLER = ["Matematik", "Turkce", "Fen", "Sosyal", "Ingilizce", "Genel Kultur"]
_DERS_IKON = {"Matematik":"🧮","Turkce":"📖","Fen":"🔬","Sosyal":"🌍","Ingilizce":"🇬🇧","Genel Kultur":"💡"}
_DERS_RENK = {"Matematik":"#3b82f6","Turkce":"#8b5cf6","Fen":"#10b981","Sosyal":"#f59e0b","Ingilizce":"#ef4444","Genel Kultur":"#059669"}


# ════════════════════════════════════════════════════════════
# 1. CANLI TREN SİMÜLASYONU & MULTIPLAYER QUİZ
# ════════════════════════════════════════════════════════════

def render_multiplayer_quiz():
    """Canlı Tren Simülasyonu — 2-4 öğrenci düello, gerçek zamanlı skor."""
    styled_section("Canli Tren Simulasyonu & Multiplayer Quiz Duellosu", "#ef4444")
    styled_info_banner(
        "2-4 ogrenci ayni anda quiz cozer — dogru cevap treni hizlandirir! "
        "Ders secimli duello, haftalik sampiyon.",
        banner_type="info", icon="🚂")

    duellolar = _lj("duello_kayitlari.json")

    bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    hafta_duello = [d for d in duellolar if d.get("tarih","")[:10] >= bu_hafta]

    styled_stat_row([
        ("Toplam Duello", str(len(duellolar)), "#ef4444", "⚔️"),
        ("Bu Hafta", str(len(hafta_duello)), "#f59e0b", "📅"),
    ])

    sub = st.tabs(["⚔️ Yeni Duello", "🏆 Duello Sonuclari", "👑 Haftalik Sampiyon", "📊 Istatistik"])

    with sub[0]:
        styled_section("Yeni Quiz Duellosu Baslat")
        with st.form("duello_form"):
            c1, c2 = st.columns(2)
            with c1:
                d_oyuncu1 = st.text_input("Oyuncu 1", key="du_o1")
                d_oyuncu2 = st.text_input("Oyuncu 2", key="du_o2")
            with c2:
                d_ders = st.selectbox("Ders (Vagon)", _DERSLER, key="du_ders")
                d_soru_sayi = st.selectbox("Soru Sayisi", [5, 10, 15, 20], key="du_soru")

            st.markdown("**Oyuncu Skorlari:**")
            sc1, sc2 = st.columns(2)
            with sc1:
                d_skor1 = st.number_input(f"{d_oyuncu1 or 'O1'} Dogru", 0, d_soru_sayi, 0, key="du_s1")
            with sc2:
                d_skor2 = st.number_input(f"{d_oyuncu2 or 'O2'} Dogru", 0, d_soru_sayi, 0, key="du_s2")

            if st.form_submit_button("Duello Sonucunu Kaydet", use_container_width=True, type="primary"):
                if d_oyuncu1 and d_oyuncu2:
                    kazanan = d_oyuncu1 if d_skor1 > d_skor2 else d_oyuncu2 if d_skor2 > d_skor1 else "Berabere"
                    duellolar.append({
                        "id": f"du_{uuid.uuid4().hex[:8]}",
                        "oyuncu1": d_oyuncu1, "oyuncu2": d_oyuncu2,
                        "skor1": d_skor1, "skor2": d_skor2,
                        "ders": d_ders, "soru_sayi": d_soru_sayi,
                        "kazanan": kazanan,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("duello_kayitlari.json", duellolar)

                    k_renk = "#10b981" if kazanan != "Berabere" else "#f59e0b"
                    st.markdown(f"""
                    <div style="background:{k_renk}15;border:2px solid {k_renk};border-radius:16px;
                        padding:20px;text-align:center;margin:10px 0;">
                        <div style="font-size:2rem;">⚔️</div>
                        <div style="color:#e2e8f0;font-size:1rem;margin-top:6px;">
                            {d_oyuncu1} <b>{d_skor1}</b> — <b>{d_skor2}</b> {d_oyuncu2}</div>
                        <div style="color:{k_renk};font-weight:900;font-size:1.2rem;margin-top:6px;">
                            {'🏆 ' + kazanan + ' Kazandi!' if kazanan != 'Berabere' else '🤝 Berabere!'}</div>
                    </div>""", unsafe_allow_html=True)
                    st.rerun()

    with sub[1]:
        styled_section("Son Duello Sonuclari")
        if not duellolar:
            st.info("Duello yok.")
        else:
            for d in sorted(duellolar, key=lambda x: x.get("tarih",""), reverse=True)[:15]:
                k = d.get("kazanan","")
                renk = "#10b981" if k != "Berabere" else "#f59e0b"
                ders_ikon = _DERS_IKON.get(d.get("ders",""), "📚")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:8px 14px;margin:4px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-size:0.82rem;">
                            {ders_ikon} {d.get('oyuncu1','')} <b>{d.get('skor1','')}</b> ⚔️
                            <b>{d.get('skor2','')}</b> {d.get('oyuncu2','')}</span>
                        <span style="color:{renk};font-weight:800;font-size:0.72rem;">{'🏆 '+k if k != 'Berabere' else '🤝'}</span>
                    </div>
                    <div style="color:#64748b;font-size:0.65rem;">{d.get('ders','')} | {d.get('soru_sayi','')} soru | {d.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Haftalik Duello Sampiyonu")
        if hafta_duello:
            ogr_galibiyet = Counter()
            for d in hafta_duello:
                k = d.get("kazanan","")
                if k and k != "Berabere":
                    ogr_galibiyet[k] += 1

            if ogr_galibiyet:
                sampiyon = ogr_galibiyet.most_common(1)[0]
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#c9a84c10,#c9a84c05);border:3px solid #c9a84c;
                    border-radius:20px;padding:24px;text-align:center;">
                    <div style="font-size:2.5rem;">👑</div>
                    <div style="color:#c9a84c;font-weight:900;font-size:1.2rem;margin-top:6px;">Haftalik Duello Sampiyonu</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.5rem;margin-top:4px;">
                        {sampiyon[0]} — {sampiyon[1]} galibiyet</div>
                </div>""", unsafe_allow_html=True)

                for sira, (ad, galibiyet) in enumerate(ogr_galibiyet.most_common(10), 1):
                    madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                        background:#0f172a;border-left:3px solid #c9a84c;border-radius:0 8px 8px 0;">
                        <span style="font-size:1rem;">{madalya}</span>
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ad}</span>
                        <span style="color:#c9a84c;font-weight:800;">{galibiyet} galibiyet</span>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Bu hafta duello yok.")

    with sub[3]:
        styled_section("Duello Istatistikleri")
        if duellolar:
            ders_say = Counter(d.get("ders","") for d in duellolar)
            styled_section("Ders Bazli Duello")
            for ders, sayi in ders_say.most_common():
                renk = _DERS_RENK.get(ders, "#94a3b8")
                ikon = _DERS_IKON.get(ders, "📚")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="font-size:1rem;">{ikon}</span>
                    <span style="min-width:100px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{ders}</span>
                    <span style="color:#ef4444;font-weight:700;">{sayi} duello</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. ÖĞRETMEN MAKİNİST PANELİ & SINIF KONTROL
# ════════════════════════════════════════════════════════════

def render_makinist_paneli():
    """Öğretmen Makinist Paneli — sınıf kontrol, istasyon takip, görev atama."""
    styled_section("Ogretmen Makinist Paneli & Sinif Kontrol Merkezi", "#2563eb")
    styled_info_banner(
        "Tum vagonlari (siniflari) kontrol edin. Hangi ogrenci nerede, "
        "ders bazli gorev atama, veli raporu.",
        banner_type="info", icon="📡")

    ilerleme = _lj("tren_ilerleme.json")
    gorev_log = _lj("gunluk_gorev_log.json")
    yarisma = _lj("vagon_yarisi.json")
    gorev_atama = _lj("ogretmen_gorev_atama.json")

    students = load_shared_students()

    sub = st.tabs(["🚦 Sinif Durumu", "📊 Istasyon Analiz", "📋 Gorev Ata", "📨 Veli Raporu"])

    with sub[0]:
        styled_section("Sinif Bazli Tren Durumu")
        ss = get_sinif_sube_listesi()
        siniflar = ss.get("siniflar", [])

        for sinif in siniflar[:12]:
            sinif_ogr = [s for s in students if str(s.get("sinif","")) == sinif]
            ogr_say = len(sinif_ogr)
            sinif_il = [il for il in ilerleme if any(
                f"{s.get('ad','')} {s.get('soyad','')}" == il.get("ogrenci","") for s in sinif_ogr)]
            tamamlanan = len(set((il.get("istasyon",""), il.get("durak","")) for il in sinif_il if il.get("tamamlandi")))
            sinif_gorev = sum(1 for g in gorev_log if any(
                f"{s.get('ad','')} {s.get('soyad','')}" == g.get("ogrenci","") for s in sinif_ogr))

            aktiflik = min(100, tamamlanan * 3 + sinif_gorev * 2)
            renk = "#10b981" if aktiflik >= 60 else "#f59e0b" if aktiflik >= 30 else "#ef4444"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                background:#0f172a;border-left:5px solid {renk};border-radius:0 12px 12px 0;">
                <span style="color:#e2e8f0;font-weight:900;font-size:0.9rem;min-width:60px;">🚃 {sinif}. Sinif</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                    <div style="width:{aktiflik}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">%{aktiflik}</span></div></div>
                <span style="color:#64748b;font-size:0.62rem;">{ogr_say} ogr | {tamamlanan} durak | {sinif_gorev} gorev</span>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Istasyon Bazli Sinif Analizi")
        if not ilerleme:
            st.info("Ilerleme verisi yok.")
        else:
            ist_say = Counter(il.get("istasyon","") for il in ilerleme if il.get("tamamlandi"))
            for ist, sayi in ist_say.most_common():
                ikon = _DERS_IKON.get(ist, "📚")
                renk = _DERS_RENK.get(ist, "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                    <span style="font-size:1rem;">{ikon}</span>
                    <span style="min-width:100px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ist}</span>
                    <span style="color:{renk};font-weight:700;">{sayi} durak tamamlandi</span>
                </div>""", unsafe_allow_html=True)

            # En zayif istasyon
            tum_ist = set(il.get("istasyon","") for il in ilerleme)
            eksik = [d for d in _DERSLER if d not in tum_ist]
            if eksik:
                st.warning(f"Hic ilerleme olmayan istasyonlar: {', '.join(eksik)}")

    with sub[2]:
        styled_section("Sinifa Gorev Ata")
        with st.form("mak_gorev_form"):
            c1, c2 = st.columns(2)
            with c1:
                g_sinif = st.selectbox("Sinif", list(range(1, 13)), key="mg_sinif")
                g_ders = st.selectbox("Ders (Istasyon)", _DERSLER, key="mg_ders")
            with c2:
                g_gorev = st.text_input("Gorev", placeholder="5 quiz coz, 3 deney tamamla...", key="mg_gorev")
                g_termin = st.date_input("Termin", key="mg_termin")

            if st.form_submit_button("Gorev Ata", use_container_width=True):
                if g_gorev:
                    gorev_atama.append({
                        "sinif": g_sinif, "ders": g_ders,
                        "gorev": g_gorev, "termin": g_termin.isoformat(),
                        "durum": "Aktif", "tarih": datetime.now().isoformat(),
                    })
                    _sj("ogretmen_gorev_atama.json", gorev_atama)
                    st.success(f"🚃 {g_sinif}. sinifa gorev atandi: {g_gorev}")
                    st.rerun()

        if gorev_atama:
            styled_section("Atanan Gorevler")
            for g in sorted(gorev_atama, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #2563eb;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;">🚃 {g.get('sinif','')}. Sinif</span>
                    <span style="color:#94a3b8;font-size:0.68rem;flex:1;">{g.get('ders','')} — {g.get('gorev','')}</span>
                    <span style="color:#64748b;font-size:0.62rem;">Termin: {g.get('termin','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Veli Icin Tren Raporu")
        st.caption("Sinif bazli tren yolculugu ozeti — veliye gonderilecek rapor.")

        toplam_durak_t = len(set((il.get("istasyon",""), il.get("durak","")) for il in ilerleme if il.get("tamamlandi")))
        toplam_gorev_t = len(gorev_log)
        toplam_duello = len(_lj("duello_kayitlari.json"))

        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #2563eb;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">🚂 Tren Yolculugu Raporu</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="display:flex;justify-content:center;gap:20px;margin-top:12px;">
                    <div><div style="color:#10b981;font-weight:900;font-size:1.5rem;">{toplam_durak_t}</div><div style="color:#64748b;font-size:0.62rem;">Durak</div></div>
                    <div><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{toplam_gorev_t}</div><div style="color:#64748b;font-size:0.62rem;">Gorev</div></div>
                    <div><div style="color:#ef4444;font-weight:900;font-size:1.5rem;">{toplam_duello}</div><div style="color:#64748b;font-size:0.62rem;">Duello</div></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. OKUL ARASI TREN AĞI & ULUSAL SIRALAMA
# ════════════════════════════════════════════════════════════

def render_ulusal_siralama():
    """Okul Arası Tren Ağı — okul kıyaslama, ulusal sıralama, benchmark."""
    styled_section("Okul Arasi Tren Agi & Ulusal Siralama", "#8b5cf6")
    styled_info_banner(
        "Farkli okullarin trenleri arasi karsilastirma. "
        "Ilce/il siralama, ulusal benchmark, guclu/zayif vagon analizi.",
        banner_type="info", icon="🌍")

    okul_verileri = _lj("okul_benchmark.json")

    sub = st.tabs(["📊 Okul Profili", "🏫 Kiyaslama", "📈 Benchmark Gir", "🏆 Ulusal Siralama"])

    with sub[0]:
        styled_section("Okulumuzun Tren Profili")

        ilerleme = _lj("tren_ilerleme.json")
        yarisma = _lj("vagon_yarisi.json")
        duellolar = _lj("duello_kayitlari.json")
        gorevler = _lj("gunluk_gorev_log.json")

        toplam_durak = len(set((il.get("istasyon",""), il.get("durak","")) for il in ilerleme if il.get("tamamlandi")))
        toplam_xp = sum(y.get("xp", 0) for y in yarisma)
        toplam_duello = len(duellolar)
        toplam_gorev = len(gorevler)

        # Okul skoru
        okul_skor = min(100, toplam_durak * 2 + toplam_xp // 50 + toplam_duello * 3 + toplam_gorev)
        s_renk = "#10b981" if okul_skor >= 70 else "#f59e0b" if okul_skor >= 40 else "#ef4444"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b,{s_renk}15);border:2px solid {s_renk};
            border-radius:20px;padding:24px 28px;text-align:center;margin:10px 0;">
            <div style="font-size:2rem;">🚂</div>
            <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;margin-top:4px;">Okulumuzun Tren Skoru</div>
            <div style="color:{s_renk};font-weight:900;font-size:3rem;margin-top:8px;">{okul_skor}</div>
            <div style="display:flex;justify-content:center;gap:20px;margin-top:12px;">
                <div><div style="color:#10b981;font-weight:800;font-size:1.2rem;">{toplam_durak}</div><div style="color:#64748b;font-size:0.6rem;">Durak</div></div>
                <div><div style="color:#c9a84c;font-weight:800;font-size:1.2rem;">{toplam_xp}</div><div style="color:#64748b;font-size:0.6rem;">XP</div></div>
                <div><div style="color:#ef4444;font-weight:800;font-size:1.2rem;">{toplam_duello}</div><div style="color:#64748b;font-size:0.6rem;">Duello</div></div>
                <div><div style="color:#3b82f6;font-weight:800;font-size:1.2rem;">{toplam_gorev}</div><div style="color:#64748b;font-size:0.6rem;">Gorev</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Vagon (sinif) bazli guc analizi
        styled_section("En Guclu & Zayif Vagonlar")
        sinif_skor = defaultdict(int)
        for y in yarisma:
            sinif_skor[y.get("sinif", 0)] += y.get("xp", 0)

        if sinif_skor:
            sirali = sorted(sinif_skor.items(), key=lambda x: x[1], reverse=True)
            en_guclu = sirali[0]
            en_zayif = sirali[-1]
            st.markdown(f"  🟢 **En Guclu:** {en_guclu[0]}. Sinif Vagonu ({en_guclu[1]} XP)")
            st.markdown(f"  🔴 **En Zayif:** {en_zayif[0]}. Sinif Vagonu ({en_zayif[1]} XP)")

    with sub[1]:
        styled_section("Okul Kiyaslama")
        if not okul_verileri:
            st.info("Benchmark verisi yok. 'Benchmark Gir' sekmesinden ekleyin.")
        else:
            sirali = sorted(okul_verileri, key=lambda x: x.get("skor", 0), reverse=True)
            for sira, o in enumerate(sirali, 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                bizim = o.get("okul","") == "Bizim Okul"
                renk = "#c9a84c" if bizim else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    {'border:1px solid #c9a84c;' if bizim else ''}">
                    <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                    <span style="color:{'#c9a84c' if bizim else '#e2e8f0'};font-weight:{'900' if bizim else '700'};
                        font-size:0.85rem;flex:1;">{'📌 ' if bizim else ''}{o.get('okul','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{o.get('il','')}/{o.get('ilce','')}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.85rem;">{o.get('skor',0)} puan</span>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Benchmark Verisi Gir")
        st.caption("Ilce/il ortalamasiyla kiyaslama icin diger okul verilerini girin.")
        with st.form("bench_form"):
            c1, c2 = st.columns(2)
            with c1:
                b_okul = st.text_input("Okul Adi", key="bn_okul")
                b_il = st.text_input("Il", key="bn_il")
            with c2:
                b_ilce = st.text_input("Ilce", key="bn_ilce")
                b_skor = st.number_input("Tren Skoru", 0, 100, 50, key="bn_skor")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if b_okul:
                    okul_verileri.append({
                        "okul": b_okul, "il": b_il, "ilce": b_ilce,
                        "skor": b_skor, "tarih": date.today().isoformat(),
                    })
                    _sj("okul_benchmark.json", okul_verileri)
                    st.success(f"{b_okul}: {b_skor} puan kaydedildi!")
                    st.rerun()

        # Kendi okulumuzu da ekle
        if not any(o.get("okul") == "Bizim Okul" for o in okul_verileri):
            if st.button("Kendi Okulumuzu Ekle (otomatik)", key="bn_biz"):
                okul_verileri.append({
                    "okul": "Bizim Okul", "il": "-", "ilce": "-",
                    "skor": okul_skor if 'okul_skor' in dir() else 50,
                    "tarih": date.today().isoformat(),
                })
                _sj("okul_benchmark.json", okul_verileri)
                st.rerun()

    with sub[3]:
        styled_section("Ulusal Tren Siralamasi")
        if len(okul_verileri) < 2:
            st.info("Siralama icin en az 2 okul verisi gerekli.")
        else:
            # Il bazli ortalama
            il_grp = defaultdict(list)
            for o in okul_verileri:
                il_grp[o.get("il","?")].append(o.get("skor", 0))

            styled_section("Il Bazli Ortalama")
            for il in sorted(il_grp.keys()):
                ort = round(sum(il_grp[il]) / max(len(il_grp[il]), 1))
                renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 40 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{il}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{ort}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{ort}</span></div></div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(il_grp[il])} okul</span>
                </div>""", unsafe_allow_html=True)
