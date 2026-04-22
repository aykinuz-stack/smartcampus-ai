"""
AI Bireysel Eğitim — Süper Özellikler
=======================================
1. LGS/TYT/AYT Sınav Hazırlık Merkezi & Hedef Puan
2. Öğrenme Stili Tespiti & Adaptif İçerik Motoru
3. Gamifiye Öğrenme Macerası & Quest Sistemi
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "ai_bireysel"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None

# ════════════════════════════════════════════════════════════
# SINAV SABİTLERİ
# ════════════════════════════════════════════════════════════

_LGS_DERSLER = {"Turkce": 20, "Matematik": 20, "Fen Bilimleri": 20, "Inkilap": 10, "Din Kulturu": 10, "Ingilizce": 10}
_TYT_DERSLER = {"Turkce": 40, "Matematik": 40, "Fen": 20, "Sosyal": 20}
_AYT_SAY_DERSLER = {"Matematik": 40, "Fizik": 14, "Kimya": 13, "Biyoloji": 13}
_AYT_EA_DERSLER = {"Matematik": 40, "Edebiyat": 24, "Tarih": 10, "Cografya": 6}
_AYT_SOZ_DERSLER = {"Edebiyat": 24, "Tarih1": 10, "Cografya1": 6, "Tarih2": 11, "Cografya2": 11, "Felsefe": 12, "Din": 6}

_SINAV_TURLERI = {
    "LGS": {"dersler": _LGS_DERSLER, "max_puan": 500, "aciklama": "8. Sinif Liseye Gecis"},
    "TYT": {"dersler": _TYT_DERSLER, "max_puan": 500, "aciklama": "Temel Yeterlilik Testi"},
    "AYT-Sayisal": {"dersler": _AYT_SAY_DERSLER, "max_puan": 500, "aciklama": "Sayisal Alan"},
    "AYT-Esit Agirlik": {"dersler": _AYT_EA_DERSLER, "max_puan": 500, "aciklama": "Esit Agirlik Alan"},
    "AYT-Sozel": {"dersler": _AYT_SOZ_DERSLER, "max_puan": 500, "aciklama": "Sozel Alan"},
}

# ════════════════════════════════════════════════════════════
# ÖĞRENME STİLİ SABİTLERİ
# ════════════════════════════════════════════════════════════

_STILLER = {
    "Gorsel": {"ikon": "👁️", "renk": "#3b82f6", "aciklama": "Gorerek ogrenir — video, grafik, renk, harita",
        "oneriler": ["Video dersler izle", "Zihin haritasi cikar", "Renkli notlar al", "Infografik kullan", "3D modeller incele"]},
    "Isitsel": {"ikon": "👂", "renk": "#8b5cf6", "aciklama": "Dinleyerek ogrenir — ses, muzik, tartisma",
        "oneriler": ["Podcast dinle", "Sesli kitap kullan", "Konuyu birine anlat", "Grup tartismasi yap", "Sesli notlar kaydet"]},
    "Kinestetik": {"ikon": "🤲", "renk": "#10b981", "aciklama": "Yaparak ogrenir — deney, proje, hareket",
        "oneriler": ["Deney / proje yap", "Calisirken yuru", "Maket / model yap", "El yazisiyla not al", "Canlandirma yap"]},
    "Okuma-Yazma": {"ikon": "📝", "renk": "#f59e0b", "aciklama": "Okuyarak/yazarak ogrenir — metin, liste, ozet",
        "oneriler": ["Ders notlarini yeniden yaz", "Ozet cikar", "Liste olustur", "Makale oku", "Flash kart kullan"]},
}

_STIL_SORULARI = [
    ("Yeni bir konuyu en iyi nasil ogrenirsin?", {"Gorsel": "Video/resim izleyerek", "Isitsel": "Birinin anlatmasini dinleyerek", "Kinestetik": "Deneyerek/yaparak", "Okuma-Yazma": "Okuyarak/not alarak"}),
    ("Bir yeri nasil bulursun?", {"Gorsel": "Haritaya bakarim", "Isitsel": "Birinden tarif alirim", "Kinestetik": "Yuruyerek kesfederim", "Okuma-Yazma": "Yazili yol tarifini okurum"}),
    ("Sinav icin en iyi nasil calisirsin?", {"Gorsel": "Renkli sema/grafik hazirlarim", "Isitsel": "Konuyu sesli tekrar ederim", "Kinestetik": "Ornekler uzerinde uygularim", "Okuma-Yazma": "Ozetler yazarim"}),
    ("Bir sunum yaparken tercih ettigin:", {"Gorsel": "Gorseller ve grafikler", "Isitsel": "Hikaye anlatarak", "Kinestetik": "Canli demo gostererek", "Okuma-Yazma": "Detayli metin hazırlayarak"}),
    ("Bos zamaninda ne yapmayi seversin?", {"Gorsel": "Film/belgesel izlerim", "Isitsel": "Muzik dinlerim/podcast", "Kinestetik": "Spor/el isi/yuruyus", "Okuma-Yazma": "Kitap/dergi okurum"}),
    ("Yeni bir oyunu nasil ogrenirsin?", {"Gorsel": "Baskasinin oynadigini izlerim", "Isitsel": "Kurallari dinlerim", "Kinestetik": "Hemen deneyerek", "Okuma-Yazma": "Kurallar kitapcigini okurum"}),
    ("Bir seyden hoslandiginizi nasil ifade edersiniz?", {"Gorsel": "Yuzu gulumserim/mimikler", "Isitsel": "Sesli ifade ederim", "Kinestetik": "Sarilma/el sikma", "Okuma-Yazma": "Yazili mesaj gonderirim"}),
    ("Telefon rehberini nasil hatirlarsın?", {"Gorsel": "Numarayi goruntusu gozumde", "Isitsel": "Numarayi sesli tekrarlarim", "Kinestetik": "Parmaklarimla tuslarim", "Okuma-Yazma": "Yazarim/not alirim"}),
    ("Yeni bir dil ogrenirken:", {"Gorsel": "Resimli kelime kartlari", "Isitsel": "Dinleme pratigi", "Kinestetik": "Rol yapma/canlandirma", "Okuma-Yazma": "Gramer kitabi okurum"}),
    ("Bir problemi nasil cozersin?", {"Gorsel": "Cizerek/diyagram yaparak", "Isitsel": "Sesli dusunurum/tartisirim", "Kinestetik": "Farkli yontemler deneyerek", "Okuma-Yazma": "Arastirip listeler yaparak"}),
    ("Ders icinde en cok ne dikkatini ceker?", {"Gorsel": "Tahtadaki yazilar/gorseller", "Isitsel": "Ogretmenin anlatimi", "Kinestetik": "Uygulamali etkinlikler", "Okuma-Yazma": "Kitaptaki metinler"}),
    ("Yeni bir yemek tarifini nasil ogrenirsin?", {"Gorsel": "Video izleyerek", "Isitsel": "Birinin anlatmasini dinleyerek", "Kinestetik": "Deneyerek/pisirerek", "Okuma-Yazma": "Tarifi okuyarak"}),
]

# ════════════════════════════════════════════════════════════
# QUEST SABİTLERİ
# ════════════════════════════════════════════════════════════

_GUNLUK_QUESTLER = [
    {"ad": "Matematik Savaşçısı", "ikon": "⚔️", "gorev": "3 Matematik sorusu çöz", "xp": 15, "ders": "Matematik"},
    {"ad": "Kelime Avcısı", "ikon": "🎯", "gorev": "10 yeni kelime öğren", "xp": 10, "ders": "Ingilizce"},
    {"ad": "Fen Kâşifi", "ikon": "🔬", "gorev": "1 Fen konusu tekrar et", "xp": 12, "ders": "Fen"},
    {"ad": "Okuma Yıldızı", "ikon": "📚", "gorev": "15 dakika kitap oku", "xp": 8, "ders": "Turkce"},
    {"ad": "Tarih Gezgini", "ikon": "🏛️", "gorev": "1 tarih konusu öğren", "xp": 10, "ders": "Tarih"},
]

_HAFTALIK_GOREVLER = [
    {"ad": "Hafta Kahramanı", "ikon": "🦸", "gorev": "5 gün üst üste çalış", "xp": 50},
    {"ad": "Quiz Ustası", "ikon": "🧠", "gorev": "3 quiz tamamla", "xp": 30},
    {"ad": "Deney Lordu", "ikon": "🧪", "gorev": "2 deney/proje tamamla", "xp": 35},
    {"ad": "Flash Kart Pro", "ikon": "🃏", "gorev": "30 flash kart tekrar et", "xp": 25},
]

_BOSS_FIGHT = [
    {"ad": "Ay Sonu Boss: Deneme Sınavı", "ikon": "🐉", "gorev": "Deneme sınavında 30+ net", "xp": 100},
    {"ad": "Dönem Boss: Final", "ikon": "👹", "gorev": "Dönem sonu ortalama 75+", "xp": 200},
]

_SEVIYELER = {
    (0,50): ("Çırak", "🟤", "#78716c"), (50,150): ("Şövalye", "🥉", "#a8a29e"),
    (150,350): ("Savaşçı", "🥈", "#94a3b8"), (350,600): ("Komutan", "🥇", "#f59e0b"),
    (600,1000): ("General", "👑", "#c9a84c"), (1000,99999): ("Efsane Kral", "💎", "#8b5cf6"),
}


# ════════════════════════════════════════════════════════════
# 1. LGS/TYT/AYT SINAV HAZIRLIK MERKEZİ
# ════════════════════════════════════════════════════════════

def render_sinav_hazirlik():
    """LGS/TYT/AYT Sınav Hazırlık — hedef puan, net hesaplama, zayıf alan, program."""
    styled_section("LGS/TYT/AYT Sinav Hazirlik Merkezi", "#ef4444")
    styled_info_banner(
        "Hedef puani gir, ders bazli kac net gerektigini gor, "
        "eksik kazanimlari tara, kisisel calisma programi olustur.",
        banner_type="warning", icon="🎯")

    kayitlar = _lj("sinav_hazirlik.json")
    deneme_sonuclari = _lj("deneme_sonuclari.json")

    sub = st.tabs(["🎯 Hedef & Net Hesapla", "📝 Deneme Analizi", "📋 Haftalik Program", "📈 Ilerleme Takip"])

    # ── HEDEF & NET ──
    with sub[0]:
        styled_section("Hedef Puan & Net Hesaplayici")
        ogr = _ogr_sec("sh_ogr")
        sinav = st.selectbox("Sinav Turu", list(_SINAV_TURLERI.keys()), key="sh_sinav")
        hedef = st.number_input("Hedef Puan", min_value=100, max_value=500, value=400, key="sh_hedef")

        sinav_info = _SINAV_TURLERI[sinav]
        dersler = sinav_info["dersler"]
        toplam_soru = sum(dersler.values())

        # Basit puan-net iliskisi
        soru_puan = sinav_info["max_puan"] / toplam_soru
        gereken_net = round(hedef / soru_puan)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#ef444415);border:2px solid #ef4444;
            border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
            <div style="color:#94a3b8;font-size:0.8rem;">{sinav} — {sinav_info['aciklama']}</div>
            <div style="color:#ef4444;font-weight:900;font-size:2.5rem;margin-top:6px;">{hedef} puan</div>
            <div style="color:#e2e8f0;font-size:0.9rem;margin-top:4px;">
                Gereken toplam net: <b style="color:#f59e0b;">{gereken_net}/{toplam_soru}</b></div>
        </div>""", unsafe_allow_html=True)

        styled_section("Ders Bazli Net Dagılımı")
        ders_net = {}
        for ders, soru in dersler.items():
            oran = soru / toplam_soru
            gereken = round(gereken_net * oran)
            ders_net[ders] = gereken

            pct = round(gereken / max(soru, 1) * 100)
            renk = "#ef4444" if pct >= 80 else "#f59e0b" if pct >= 60 else "#10b981"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                <span style="min-width:110px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{gereken}/{soru}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        if ogr and st.button("Hedefi Kaydet", use_container_width=True, type="primary"):
            kayitlar.append({
                "ogrenci": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                "sinav": sinav, "hedef": hedef, "gereken_net": gereken_net,
                "ders_net": ders_net, "tarih": date.today().isoformat(),
            })
            _sj("sinav_hazirlik.json", kayitlar)
            st.success("Hedef kaydedildi!")

    # ── DENEME ANALİZİ ──
    with sub[1]:
        styled_section("Deneme Sinavi Analizi")
        with st.form("deneme_form"):
            c1, c2 = st.columns(2)
            with c1:
                d_ogr = st.text_input("Ogrenci", key="dn_ogr")
                d_sinav = st.selectbox("Sinav", list(_SINAV_TURLERI.keys()), key="dn_sinav")
            with c2:
                d_tarih = st.date_input("Tarih", key="dn_tarih")

            # Ders bazli netler
            d_info = _SINAV_TURLERI[d_sinav]
            netler = {}
            cols = st.columns(min(len(d_info["dersler"]), 3))
            for i, (ders, soru) in enumerate(d_info["dersler"].items()):
                with cols[i % len(cols)]:
                    netler[ders] = st.number_input(f"{ders} Net (/{soru})",
                        min_value=0.0, max_value=float(soru), value=0.0, step=0.5, key=f"dn_{ders}")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if d_ogr:
                    toplam_net = sum(netler.values())
                    tahmin_puan = round(toplam_net * d_info["max_puan"] / sum(d_info["dersler"].values()))
                    deneme_sonuclari.append({
                        "ogrenci": d_ogr, "sinav": d_sinav,
                        "netler": netler, "toplam_net": toplam_net,
                        "tahmin_puan": tahmin_puan, "tarih": d_tarih.isoformat(),
                    })
                    _sj("deneme_sonuclari.json", deneme_sonuclari)
                    st.success(f"Toplam: {toplam_net} net — Tahmini: {tahmin_puan} puan")
                    st.rerun()

        if deneme_sonuclari:
            styled_section("Son Deneme Sonuclari")
            for d in sorted(deneme_sonuclari, key=lambda x: x.get("tarih",""), reverse=True)[:5]:
                renk = "#10b981" if d.get("tahmin_puan",0) >= 400 else "#f59e0b" if d.get("tahmin_puan",0) >= 300 else "#ef4444"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;">{d.get('ogrenci','')} — {d.get('sinav','')}</span>
                        <span style="color:{renk};font-weight:800;">{d.get('tahmin_puan','')} puan ({d.get('toplam_net','')} net)</span>
                    </div>
                    <div style="color:#64748b;font-size:0.68rem;">{d.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    # ── HAFTALIK PROGRAM ──
    with sub[2]:
        styled_section("Kisisel Calisma Programi")
        if not kayitlar:
            st.info("Once hedef belirleyin.")
        else:
            son = sorted(kayitlar, key=lambda x: x.get("tarih",""), reverse=True)[0]
            st.markdown(f"**{son.get('ogrenci','')}** — {son.get('sinav','')} Hedef: {son.get('hedef','')} puan")

            gunler = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
            ders_list = list(son.get("ders_net", {}).keys())

            for gun_idx, gun in enumerate(gunler):
                ders_1 = ders_list[gun_idx % len(ders_list)] if ders_list else "Genel"
                ders_2 = ders_list[(gun_idx + 1) % len(ders_list)] if len(ders_list) > 1 else ders_1
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;">
                    <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.78rem;">{gun}</span>
                    <span style="color:#3b82f6;font-size:0.72rem;">{ders_1} (45dk)</span>
                    <span style="color:#8b5cf6;font-size:0.72rem;">+ {ders_2} (30dk)</span>
                    <span style="color:#10b981;font-size:0.65rem;margin-left:auto;">Soru Cozme (30dk)</span>
                </div>""", unsafe_allow_html=True)

    # ── İLERLEME TAKİP ──
    with sub[3]:
        styled_section("Deneme Net Ilerleme Trendi")
        if not deneme_sonuclari:
            st.info("Deneme verisi yok.")
        else:
            ogr_grp = defaultdict(list)
            for d in deneme_sonuclari:
                ogr_grp[d.get("ogrenci","")].append(d)

            for ogr, sonuclar in ogr_grp.items():
                sirali = sorted(sonuclar, key=lambda x: x.get("tarih",""))
                st.markdown(f"**{ogr}** — {len(sirali)} deneme")
                for idx, s in enumerate(sirali):
                    net = s.get("toplam_net", 0)
                    onceki = sirali[idx-1].get("toplam_net", net) if idx > 0 else net
                    fark = net - onceki
                    trend_renk = "#10b981" if fark > 0 else "#ef4444" if fark < 0 else "#94a3b8"
                    trend_txt = f"+{fark}" if fark > 0 else str(fark)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin:2px 0;padding-left:16px;">
                        <span style="min-width:65px;color:#64748b;font-size:0.68rem;">{s.get('tarih','')[:10]}</span>
                        <span style="color:#e2e8f0;font-size:0.75rem;font-weight:600;">{net} net</span>
                        <span style="color:{trend_renk};font-size:0.68rem;font-weight:700;">{trend_txt}</span>
                    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. ÖĞRENME STİLİ TESPİTİ & ADAPTİF İÇERİK
# ════════════════════════════════════════════════════════════

def render_ogrenme_stili():
    """Öğrenme Stili Tespiti — 12 soruluk test, stile uygun içerik önerisi."""
    styled_section("Ogrenme Stili Tespiti & Adaptif Icerik", "#8b5cf6")
    styled_info_banner(
        "Gorsel/Isitsel/Kinestetik/Okuma-Yazma ogrenme stili tespiti. "
        "Stile gore otomatik icerik onerisi.",
        banner_type="info", icon="🧬")

    profiller = _lj("ogrenme_stil_profilleri.json")

    sub = st.tabs(["🧪 Stil Testi", "👤 Profil Goruntule", "📚 Icerik Onerisi", "📊 Sinif Analiz"])

    # ── STİL TESTİ ──
    with sub[0]:
        styled_section("Ogrenme Stili Testi (12 Soru)")
        ogr = _ogr_sec("os_ogr")
        if ogr:
            with st.form("stil_form"):
                skorlar = {"Gorsel": 0, "Isitsel": 0, "Kinestetik": 0, "Okuma-Yazma": 0}
                for i, (soru, cevaplar) in enumerate(_STIL_SORULARI):
                    st.markdown(f"**{i+1}.** {soru}")
                    sec = st.radio("Seciniz:", list(cevaplar.values()), key=f"os_s_{i}", horizontal=True)
                    for stil, cevap in cevaplar.items():
                        if sec == cevap:
                            skorlar[stil] += 1

                if st.form_submit_button("Sonucu Hesapla", use_container_width=True, type="primary"):
                    baskin = max(skorlar, key=skorlar.get)
                    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

                    profiller.append({
                        "id": f"os_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "sinif": ogr.get("sinif",""), "sube": ogr.get("sube",""),
                        "skorlar": skorlar, "baskin_stil": baskin,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("ogrenme_stil_profilleri.json", profiller)

                    stil_info = _STILLER[baskin]
                    st.success(f"Baskin Ogrenme Stili: {stil_info['ikon']} {baskin}")

                    # Sonuc goster
                    for stil, info in _STILLER.items():
                        puan = skorlar.get(stil, 0)
                        pct = round(puan / 12 * 100)
                        renk = info["renk"]
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                            <span style="font-size:1.2rem;">{info['ikon']}</span>
                            <span style="min-width:90px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{stil}</span>
                            <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                                <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                                    display:flex;align-items:center;padding-left:8px;">
                                    <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/12</span>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    st.rerun()

    # ── PROFİL GÖRÜNTÜLE ──
    with sub[1]:
        styled_section("Ogrenci Stil Profilleri")
        if not profiller:
            st.info("Henuz profil yok.")
        else:
            for p in sorted(profiller, key=lambda x: x.get("tarih",""), reverse=True)[:15]:
                bs = p.get("baskin_stil","?")
                info = _STILLER.get(bs, {"ikon":"?","renk":"#94a3b8"})
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                    background:#0f172a;border-left:4px solid {info['renk']};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.2rem;">{info['ikon']}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{p.get('ogrenci','')}</span>
                    <span style="background:{info['renk']}20;color:{info['renk']};padding:3px 10px;border-radius:8px;
                        font-size:0.72rem;font-weight:700;">{bs}</span>
                </div>""", unsafe_allow_html=True)

    # ── İÇERİK ÖNERİSİ ──
    with sub[2]:
        styled_section("Stile Uygun Icerik Onerisi")
        if not profiller:
            st.info("Once stil testi uygulatin.")
        else:
            sec = st.selectbox("Ogrenci",
                [f"{p.get('ogrenci','')} ({p.get('baskin_stil','')})" for p in profiller], key="os_oneri")
            idx = [f"{p.get('ogrenci','')} ({p.get('baskin_stil','')})" for p in profiller].index(sec) if sec else 0
            p = profiller[idx]
            bs = p.get("baskin_stil","")
            info = _STILLER.get(bs, {})

            if info:
                st.markdown(f"### {info.get('ikon','')} {bs} Icin Oneriler")
                st.markdown(f"*{info.get('aciklama','')}*")
                for o in info.get("oneriler", []):
                    st.markdown(f"""
                    <div style="background:{info['renk']}08;border:1px solid {info['renk']}30;border-left:4px solid {info['renk']};
                        border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                        <span style="color:#e2e8f0;font-size:0.82rem;">💡 {o}</span>
                    </div>""", unsafe_allow_html=True)

    # ── SINIF ANALİZ ──
    with sub[3]:
        styled_section("Sinif Bazli Stil Dagilimi")
        if not profiller:
            st.info("Veri yok.")
        else:
            stil_say = Counter(p.get("baskin_stil","") for p in profiller)
            toplam = max(len(profiller), 1)
            for stil, sayi in stil_say.most_common():
                info = _STILLER.get(stil, {"ikon":"?","renk":"#94a3b8"})
                pct = round(sayi / toplam * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="font-size:1.2rem;">{info.get('ikon','')}</span>
                    <span style="min-width:100px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{stil}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{info.get('renk','#94a3b8')};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi} (%{pct})</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. GAMİFİYE ÖĞRENME MACERASI & QUEST SİSTEMİ
# ════════════════════════════════════════════════════════════

def render_quest_sistemi():
    """Gamifiye Öğrenme Macerası — günlük quest, haftalık görev, boss fight, XP."""
    styled_section("Gamifiye Ogrenme Macerasi & Quest Sistemi", "#c9a84c")
    styled_info_banner(
        "Ders calismayi RPG oyununa cevir! Gunluk quest, haftalik gorev, "
        "boss fight, XP, seviye, ozel gucler.",
        banner_type="info", icon="🎮")

    quest_log = _lj("quest_log.json")
    calisma_log = _lj("calisma_log.json")

    sub = st.tabs(["⚔️ Gunluk Quest", "🗓️ Haftalik Gorev", "🐉 Boss Fight", "👤 Kahraman Profil", "🏆 Liderlik"])

    # ── GÜNLÜK QUEST ──
    with sub[0]:
        styled_section("Bugunun Quest'leri")
        ogr = _ogr_sec("qst_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            bugun = date.today().isoformat()

            # Rastgele 3 quest sec (her gun ayni — seed)
            random.seed(hash(bugun + ogr_ad))
            gunun_questleri = random.sample(_GUNLUK_QUESTLER, min(3, len(_GUNLUK_QUESTLER)))

            tamamlanan_bugun = [q for q in quest_log
                                if q.get("ogrenci") == ogr_ad and q.get("tarih","")[:10] == bugun]
            tamamlanan_idler = set(q.get("quest","") for q in tamamlanan_bugun)

            for q in gunun_questleri:
                tamamlandi = q["ad"] in tamamlanan_idler
                renk = "#10b981" if tamamlandi else "#f59e0b"
                ikon = "✅" if tamamlandi else q["ikon"]

                st.markdown(f"""
                <div style="background:#0f172a;border:{'2px solid #10b981' if tamamlandi else '1px solid #334155'};
                    border-left:5px solid {renk};border-radius:0 14px 14px 0;
                    padding:12px 16px;margin:6px 0;{'opacity:0.7;' if tamamlandi else ''}">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">{ikon} {q['ad']}</span>
                        <span style="color:#c9a84c;font-weight:800;font-size:0.8rem;">+{q['xp']} XP</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">{q['gorev']}</div>
                </div>""", unsafe_allow_html=True)

                if not tamamlandi:
                    if st.button(f"Tamamladim! {q['ad']}", key=f"qst_{q['ad']}"):
                        quest_log.append({
                            "ogrenci": ogr_ad, "quest": q["ad"],
                            "xp": q["xp"], "tip": "gunluk",
                            "tarih": datetime.now().isoformat(),
                        })
                        _sj("quest_log.json", quest_log)
                        st.success(f"⚔️ {q['ad']} tamamlandi! +{q['xp']} XP")
                        st.rerun()

    # ── HAFTALIK GÖREV ──
    with sub[1]:
        styled_section("Bu Haftanin Gorevleri")
        for g in _HAFTALIK_GOREVLER:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #334155;border-left:4px solid #8b5cf6;
                border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{g['ikon']} {g['ad']}</span>
                    <span style="color:#c9a84c;font-weight:800;">+{g['xp']} XP</span>
                </div>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">{g['gorev']}</div>
            </div>""", unsafe_allow_html=True)

    # ── BOSS FIGHT ──
    with sub[2]:
        styled_section("Boss Fight — Buyuk Sinav!")
        for b in _BOSS_FIGHT:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a0a0a,#dc262615);border:2px solid #dc2626;
                border-radius:16px;padding:16px 20px;margin:8px 0;text-align:center;">
                <div style="font-size:3rem;">{b['ikon']}</div>
                <div style="color:#fca5a5;font-weight:900;font-size:1rem;margin-top:4px;">{b['ad']}</div>
                <div style="color:#94a3b8;font-size:0.78rem;margin-top:4px;">{b['gorev']}</div>
                <div style="color:#c9a84c;font-weight:900;font-size:1.2rem;margin-top:6px;">+{b['xp']} XP</div>
            </div>""", unsafe_allow_html=True)

    # ── KAHRAMAN PROFİL ──
    with sub[3]:
        styled_section("Kahraman Profilin")
        ogr2 = _ogr_sec("qst_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            ogr_quest = [q for q in quest_log if q.get("ogrenci") == ogr_ad2]
            xp = sum(q.get("xp", 0) for q in ogr_quest)

            # Calisma logundan ek XP
            ogr_cal = [c for c in calisma_log if c.get("ogrenci") == ogr_ad2]
            xp += len(ogr_cal) * 5

            # Seviye
            sev_ad, sev_ikon, sev_renk = "Cirak", "🟤", "#78716c"
            sev_pct, kalan = 0, 50
            for (lo, hi), (ad, ikon, renk) in _SEVIYELER.items():
                if lo <= xp < hi:
                    sev_ad, sev_ikon, sev_renk = ad, ikon, renk
                    sev_pct = round((xp - lo) / max(hi - lo, 1) * 100)
                    kalan = hi - xp
                    break

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1a2e,{sev_renk}20);border:2px solid {sev_renk};
                border-radius:20px;padding:24px;text-align:center;">
                <div style="font-size:3rem;">{sev_ikon}</div>
                <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">{ogr_ad2}</div>
                <div style="color:{sev_renk};font-weight:800;">{sev_ad}</div>
                <div style="color:{sev_renk};font-weight:900;font-size:2rem;margin-top:6px;">{xp} XP</div>
                <div style="background:#1e293b;border-radius:6px;height:12px;margin:10px 20px;overflow:hidden;">
                    <div style="width:{sev_pct}%;height:100%;background:{sev_renk};border-radius:6px;"></div>
                </div>
                <div style="color:#64748b;font-size:0.7rem;">Sonraki seviye: {kalan} XP | {len(ogr_quest)} quest tamamlandi</div>
            </div>""", unsafe_allow_html=True)

    # ── LİDERLİK ──
    with sub[4]:
        styled_section("Okul Quest Liderligi")
        ogr_xp = defaultdict(int)
        for q in quest_log:
            ogr_xp[q.get("ogrenci","")] += q.get("xp", 0)
        for c in calisma_log:
            ogr_xp[c.get("ogrenci","")] += 5

        lider = sorted(ogr_xp.items(), key=lambda x: x[1], reverse=True)
        if not lider:
            st.info("Quest tamamlanmamis.")
        else:
            for sira, (ad, xp) in enumerate(lider[:15], 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                for (lo, hi), (_, ikon, renk) in _SEVIYELER.items():
                    if lo <= xp < hi:
                        break
                else:
                    ikon, renk = "💎", "#8b5cf6"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{ad}</span>
                    <span style="font-size:0.75rem;">{ikon}</span>
                    <span style="color:#c9a84c;font-weight:800;">{xp} XP</span>
                </div>""", unsafe_allow_html=True)
