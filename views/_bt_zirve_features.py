"""
AI Treni — Zirve Özellikler
==============================
1. Tren Hikaye Modu & Macera Senaryoları
2. AI Kişisel Tren Rotası & Zayıf Durak Tespiti
3. Tren Müzesi & Başarı Galerisi
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

_HIKAYE_BOLUMLERI = [
    {"bolum": 1, "ad": "Matematik Kalesi", "ikon": "🏰", "renk": "#3b82f6",
     "hikaye": "Bilgi Kralligi'nin ilk kalesi. Kapidan gecmek icin 5 denklem cozmalisin!",
     "gorev": "5 Matematik sorusu coz", "boss": "Sayi Canavari", "odul": "Zeka Kilici"},
    {"bolum": 2, "ad": "Fen Ormani", "ikon": "🌲", "renk": "#10b981",
     "hikaye": "Gizemli ormanda 3 deney tamamla ve buyulu iksiri kesfet!",
     "gorev": "3 Fen deneyi tamamla", "boss": "Formul Ejderhasi", "odul": "Bilim Kalkani"},
    {"bolum": 3, "ad": "Edebiyat Sarayi", "ikon": "📚", "renk": "#8b5cf6",
     "hikaye": "Saraydaki sirri cozmek icin 3 siir oku ve bir hikaye yaz!",
     "gorev": "3 siir oku + 1 paragraf yaz", "boss": "Kelime Buyucusu", "odul": "Hikaye Asasi"},
    {"bolum": 4, "ad": "Tarih Labirenti", "ikon": "🏛️", "renk": "#f59e0b",
     "hikaye": "Labirentten cikmak icin 5 tarih sorusunu dogru yanitle!",
     "gorev": "5 Tarih/Sosyal quizi coz", "boss": "Zaman Bekçisi", "odul": "Tarih Pusulasi"},
    {"bolum": 5, "ad": "Ingilizce Adasi", "ikon": "🏝️", "renk": "#ef4444",
     "hikaye": "Adadan kacmak icin 10 kelime ogren ve 1 diyalog tamamla!",
     "gorev": "10 kelime + 1 diyalog", "boss": "Grammar Korsani", "odul": "Dil Haritasi"},
    {"bolum": 6, "ad": "Bilgi Zirvesi", "ikon": "⛰️", "renk": "#c9a84c",
     "hikaye": "Son zirve! Tum bilgini kullanarak Bilgi Krali'ni yen!",
     "gorev": "Genel kultur + tum derslerden 10 soru", "boss": "Bilgi Krali", "odul": "Krallik Taci"},
]

_KARAKTER_OZELLIKLERI = {
    "Zeka": {"ikon": "🧠", "renk": "#3b82f6"},
    "Guc": {"ikon": "💪", "renk": "#ef4444"},
    "Hiz": {"ikon": "⚡", "renk": "#f59e0b"},
    "Bilgelik": {"ikon": "🦉", "renk": "#8b5cf6"},
}

_ISTASYONLAR = {
    "Matematik": {"ikon": "🧮", "renk": "#3b82f6", "duraklar": ["Sayilar","Islemler","Cebir","Geometri","Olasilik","Veri"]},
    "Turkce": {"ikon": "📖", "renk": "#8b5cf6", "duraklar": ["Dil Bilgisi","Paragraf","Anlama","Yazma","Sozcuk"]},
    "Fen": {"ikon": "🔬", "renk": "#10b981", "duraklar": ["Fizik","Kimya","Biyoloji","Yer Bilimi"]},
    "Sosyal": {"ikon": "🌍", "renk": "#f59e0b", "duraklar": ["Tarih","Cografya","Vatandaslik"]},
    "Ingilizce": {"ikon": "🇬🇧", "renk": "#ef4444", "duraklar": ["Grammar","Vocabulary","Reading","Listening"]},
    "Genel Kultur": {"ikon": "💡", "renk": "#059669", "duraklar": ["Bilim","Sanat","Spor","Doga"]},
}


# ════════════════════════════════════════════════════════════
# 1. TREN HİKAYE MODU & MACERA SENARYOLARI
# ════════════════════════════════════════════════════════════

def render_hikaye_modu():
    """Tren Hikaye Modu — Bilgi Krallığı macerası, bölüm, boss, ödül."""
    styled_section("Tren Hikaye Modu — Bilgi Kralligi Macerasi", "#c9a84c")
    styled_info_banner(
        "Bilgi Kralligi'nda kahraman ol! Her istasyon bir macera bolumu, "
        "gorev tamamla, boss yen, odul kazan!",
        banner_type="info", icon="🎭")

    hikaye_ilerleme = _lj("hikaye_ilerleme.json")
    karakter_kayit = _lj("karakter_kayitlari.json")

    sub = st.tabs(["🗺️ Macera Haritasi", "⚔️ Bolum Oyna", "👤 Karakter", "🏆 Oduller"])

    with sub[0]:
        styled_section("Bilgi Kralligi Macera Haritasi")
        ogr = st.text_input("Kahraman Adi", key="hk_ogr")

        ogr_ilerleme = [h for h in hikaye_ilerleme if h.get("ogrenci") == ogr] if ogr else []
        tamamlanan_bolumler = set(h.get("bolum") for h in ogr_ilerleme if h.get("tamamlandi"))

        for b in _HIKAYE_BOLUMLERI:
            gecti = b["bolum"] in tamamlanan_bolumler
            aktif = b["bolum"] == len(tamamlanan_bolumler) + 1
            kilitli = b["bolum"] > len(tamamlanan_bolumler) + 1

            opacity = "1" if gecti or aktif else "0.35"
            border = f"3px solid {b['renk']}" if aktif else f"2px solid {b['renk']}40" if gecti else "1px solid #334155"
            ikon = "✅" if gecti else "⚔️" if aktif else "🔒"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;padding:12px 18px;margin:6px 0;
                background:#0f172a;border:{border};border-radius:16px;opacity:{opacity};">
                <span style="font-size:2rem;">{b['ikon']}</span>
                <div style="flex:1;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:0.95rem;">
                        {ikon} Bolum {b['bolum']}: {b['ad']}</div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:2px;">{b['hikaye'][:60]}...</div>
                    <div style="color:{b['renk']};font-size:0.68rem;margin-top:2px;">
                        Gorev: {b['gorev']} | Boss: {b['boss']} | Odul: {b['odul']}</div>
                </div>
                {'<span style="color:#c9a84c;font-weight:800;font-size:0.75rem;">📌 ŞİMDİ</span>' if aktif else ''}
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Bolum Oyna")
        if not ogr:
            st.info("Once kahraman adini gir.")
        else:
            siradaki = len(tamamlanan_bolumler) + 1
            if siradaki > len(_HIKAYE_BOLUMLERI):
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#c9a84c10,#c9a84c05);border:3px solid #c9a84c;
                    border-radius:20px;padding:28px;text-align:center;">
                    <div style="font-size:3rem;">👑</div>
                    <div style="color:#c9a84c;font-weight:900;font-size:1.3rem;margin-top:8px;">
                        TEBRİKLER! Bilgi Kralligi'nin Yeni Krali!</div>
                    <div style="color:#e2e8f0;font-size:0.85rem;margin-top:6px;">
                        Tum 6 bolumu tamamladin. Sen gercek bir bilgi kahramanisin!</div>
                </div>""", unsafe_allow_html=True)
            else:
                bolum = _HIKAYE_BOLUMLERI[siradaki - 1]
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,{bolum['renk']}15);border:2px solid {bolum['renk']};
                    border-radius:18px;padding:20px 24px;margin:10px 0;">
                    <div style="text-align:center;">
                        <div style="font-size:2.5rem;">{bolum['ikon']}</div>
                        <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:6px;">
                            Bolum {bolum['bolum']}: {bolum['ad']}</div>
                        <div style="color:#94a3b8;font-size:0.82rem;margin-top:6px;">{bolum['hikaye']}</div>
                    </div>
                    <div style="display:flex;justify-content:center;gap:20px;margin-top:14px;">
                        <div style="text-align:center;background:#1e293b;padding:8px 14px;border-radius:10px;">
                            <div style="color:{bolum['renk']};font-weight:800;font-size:0.78rem;">📋 Gorev</div>
                            <div style="color:#e2e8f0;font-size:0.72rem;">{bolum['gorev']}</div>
                        </div>
                        <div style="text-align:center;background:#1e293b;padding:8px 14px;border-radius:10px;">
                            <div style="color:#ef4444;font-weight:800;font-size:0.78rem;">🐉 Boss</div>
                            <div style="color:#e2e8f0;font-size:0.72rem;">{bolum['boss']}</div>
                        </div>
                        <div style="text-align:center;background:#1e293b;padding:8px 14px;border-radius:10px;">
                            <div style="color:#c9a84c;font-weight:800;font-size:0.78rem;">🏆 Odul</div>
                            <div style="color:#e2e8f0;font-size:0.72rem;">{bolum['odul']}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

                if st.button(f"⚔️ Bolum {bolum['bolum']}'i Tamamladim!", use_container_width=True, type="primary"):
                    hikaye_ilerleme.append({
                        "ogrenci": ogr, "bolum": bolum["bolum"],
                        "ad": bolum["ad"], "tamamlandi": True,
                        "odul": bolum["odul"], "tarih": datetime.now().isoformat(),
                    })
                    _sj("hikaye_ilerleme.json", hikaye_ilerleme)

                    # Karakter guncelle
                    mevcut = next((k for k in karakter_kayit if k.get("ogrenci") == ogr), None)
                    if mevcut:
                        for oz in _KARAKTER_OZELLIKLERI:
                            mevcut[oz] = mevcut.get(oz, 10) + random.randint(3, 8)
                    else:
                        yeni = {"ogrenci": ogr}
                        for oz in _KARAKTER_OZELLIKLERI:
                            yeni[oz] = 10 + random.randint(3, 8)
                        karakter_kayit.append(yeni)
                    _sj("karakter_kayitlari.json", karakter_kayit)

                    st.success(f"🏆 Bolum {bolum['bolum']} tamamlandi! Odul: {bolum['odul']}")
                    st.rerun()

    with sub[2]:
        styled_section("Kahraman Profili")
        if not ogr:
            st.info("Kahraman adi gir.")
        else:
            karakter = next((k for k in karakter_kayit if k.get("ogrenci") == ogr), None)
            bolum_say = len(tamamlanan_bolumler)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1a2e,#c9a84c15);border:2px solid #c9a84c;
                border-radius:20px;padding:24px;text-align:center;">
                <div style="font-size:2.5rem;">⚔️</div>
                <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:4px;">{ogr}</div>
                <div style="color:#c9a84c;font-size:0.8rem;">{bolum_say}/6 Bolum Tamamlandi</div>
            </div>""", unsafe_allow_html=True)

            if karakter:
                styled_section("Karakter Ozellikleri")
                for oz, info in _KARAKTER_OZELLIKLERI.items():
                    deger = karakter.get(oz, 10)
                    pct = min(deger, 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
                        <span style="font-size:1rem;">{info['ikon']}</span>
                        <span style="min-width:70px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{oz}</span>
                        <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{info['renk']};border-radius:6px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.6rem;color:#fff;font-weight:700;">{deger}</span></div></div>
                    </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Kazanilan Oduller")
        if ogr and ogr_ilerleme:
            for h in sorted(ogr_ilerleme, key=lambda x: x.get("bolum",0)):
                b = next((b for b in _HIKAYE_BOLUMLERI if b["bolum"] == h.get("bolum")), None)
                if b:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:4px 0;
                        background:#c9a84c08;border:1px solid #c9a84c30;border-radius:12px;">
                        <span style="font-size:1.5rem;">{b['ikon']}</span>
                        <div style="flex:1;">
                            <span style="color:#c9a84c;font-weight:800;font-size:0.82rem;">{b['odul']}</span>
                            <div style="color:#94a3b8;font-size:0.68rem;">Bolum {b['bolum']}: {b['ad']}</div>
                        </div>
                        <span style="color:#10b981;font-size:0.72rem;">✅</span>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Henuz odul kazanilmadi.")


# ════════════════════════════════════════════════════════════
# 2. AI KİŞİSEL TREN ROTASI & ZAYIF DURAK TESPİTİ
# ════════════════════════════════════════════════════════════

def render_kisisel_rota():
    """AI Kişisel Tren Rotası — güçlü/zayıf durak, özel rota önerisi."""
    styled_section("AI Kisisel Tren Rotasi & Zayif Durak Tespiti", "#059669")
    styled_info_banner(
        "Quiz/oyun performansindan otomatik guclu/zayif durak haritasi. "
        "Kisisellestirmis rota: zayif duraklara cok, guclulere az zaman.",
        banner_type="info", icon="🧬")

    ilerleme = _lj("tren_ilerleme.json")
    adaptif = _lj("adaptif_log.json")
    gorev_log = _lj("gunluk_gorev_log.json")

    sub = st.tabs(["🗺️ Kisisel Rota", "📊 Durak Analizi", "💡 Haftalik Oneri", "📈 Gelisim"])

    with sub[0]:
        styled_section("Sana Ozel Tren Rotasi")
        ogr = st.text_input("Ogrenci Adi", key="kr_ogr")
        if ogr:
            # Durak performans hesapla
            durak_perf = defaultdict(lambda: {"dogru": 0, "yanlis": 0})
            for a in adaptif:
                if a.get("ogrenci","") == ogr:
                    durak_perf[a.get("ders","")]["dogru"] += a.get("dogru", 0)
                    durak_perf[a.get("ders","")]["yanlis"] += a.get("yanlis", 0)

            # Rota olustur
            zayif, guclu = [], []
            for ist, info in _ISTASYONLAR.items():
                perf = durak_perf.get(ist)
                if perf:
                    toplam = perf["dogru"] + perf["yanlis"]
                    oran = round(perf["dogru"] / max(toplam, 1) * 100) if toplam > 0 else 50
                else:
                    oran = 50  # varsayilan

                if oran < 60:
                    zayif.append((ist, info, oran))
                else:
                    guclu.append((ist, info, oran))

            if zayif:
                styled_section("🔴 Zayif Duraklar — Oncelikli Calis")
                for ist, info, oran in sorted(zayif, key=lambda x: x[2]):
                    st.markdown(f"""
                    <div style="background:#ef444410;border:1px solid #ef444430;border-left:5px solid #ef4444;
                        border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                        <span style="font-size:1rem;">{info['ikon']}</span>
                        <span style="color:#fca5a5;font-weight:800;font-size:0.85rem;margin-left:6px;">{ist}</span>
                        <span style="color:#ef4444;font-weight:700;font-size:0.78rem;float:right;">%{oran}</span>
                        <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                            Bu istasyona bu hafta ekstra 2 saat ayir!</div>
                    </div>""", unsafe_allow_html=True)

            if guclu:
                styled_section("🟢 Guclu Duraklar — Hizli Gec")
                for ist, info, oran in sorted(guclu, key=lambda x: x[2], reverse=True):
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                        background:#10b98108;border-left:3px solid #10b981;border-radius:0 8px 8px 0;">
                        <span style="font-size:0.9rem;">{info['ikon']}</span>
                        <span style="color:#6ee7b7;font-weight:700;font-size:0.82rem;flex:1;">{ist}</span>
                        <span style="color:#10b981;font-weight:700;">%{oran}</span>
                    </div>""", unsafe_allow_html=True)

            if not zayif and not guclu:
                st.info("Performans verisi yok — quiz ve oyunlari tamamladikca rota olusur.")

    with sub[1]:
        styled_section("Istasyon Bazli Durak Performansi")
        for ist, info in _ISTASYONLAR.items():
            # Tamamlanan durak sayisi
            ist_il = [il for il in ilerleme if il.get("istasyon") == ist and il.get("tamamlandi")]
            tamamlanan = len(set(il.get("durak") for il in ist_il))
            toplam = len(info["duraklar"])
            pct = round(tamamlanan / max(toplam, 1) * 100)
            renk = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444" if pct > 0 else "#334155"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                <span style="font-size:1.1rem;">{info['ikon']}</span>
                <span style="min-width:100px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ist}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{tamamlanan}/{toplam}</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Bu Hafta Icin AI Rota Onerisi")
        st.markdown(f"""
        <div style="background:#05966910;border:2px solid #059669;border-radius:16px;padding:16px 20px;">
            <div style="color:#10b981;font-weight:900;font-size:1rem;text-align:center;">🧬 Kisisel Haftalik Rota</div>
            <div style="color:#e2e8f0;font-size:0.82rem;margin-top:8px;line-height:1.6;">
                • <b>Pazartesi:</b> Zayif istasyon #1 — Konu tekrari + 5 soru<br>
                • <b>Sali:</b> Zayif istasyon #2 — Video + quiz<br>
                • <b>Carsamba:</b> Genel tekrar — tum istasyonlardan 1'er soru<br>
                • <b>Persembe:</b> Zayif istasyon #1 — Pekistirme + 8 soru<br>
                • <b>Cuma:</b> Guclu istasyon — Challenge sorular + duello
            </div>
        </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Haftalik Gelisim Takibi")
        if gorev_log:
            hafta_grp = Counter()
            for g in gorev_log:
                tarih = g.get("tarih","")[:10]
                try:
                    dt = date.fromisoformat(tarih)
                    hb = dt - timedelta(days=dt.weekday())
                    hafta_grp[hb.isoformat()] += 1
                except Exception: pass

            for h in sorted(hafta_grp.keys())[-6:]:
                sayi = hafta_grp[h]
                is_bu = h == (date.today() - timedelta(days=date.today().weekday())).isoformat()
                renk = "#10b981" if sayi >= 15 else "#f59e0b" if sayi >= 7 else "#3b82f6"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:3px 0;
                    {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                    <span style="min-width:65px;font-size:0.72rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{h[5:]}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{min(sayi*5,100)}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi} gorev</span></div></div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Gorev verisi yok.")


# ════════════════════════════════════════════════════════════
# 3. TREN MÜZESİ & BAŞARI GALERİSİ
# ════════════════════════════════════════════════════════════

def render_tren_muzesi():
    """Tren Müzesi — başarı galerisi, onur tablosu, motivasyon duvarı."""
    styled_section("Tren Muzesi & Basari Galerisi", "#c9a84c")
    styled_info_banner(
        "Tum okulun tren yolculugu gecmisinin arsivlendigi dijital muze. "
        "Onur tablosu, mezun arsivi, motivasyon duvari.",
        banner_type="info", icon="🏛️")

    ilerleme = _lj("tren_ilerleme.json")
    duellolar = _lj("duello_kayitlari.json")
    gorev_log = _lj("gunluk_gorev_log.json")
    yarisma = _lj("vagon_yarisi.json")
    hikaye_il = _lj("hikaye_ilerleme.json")
    motivasyon_duvari = _lj("motivasyon_duvari.json")

    sub = st.tabs(["🏆 Onur Tablosu", "📊 Okul Istatistik", "💬 Motivasyon Duvari", "📜 Mezun Arsivi"])

    with sub[0]:
        styled_section("Tren Onur Tablosu")

        # En cok durak tamamlayan
        ogr_durak = Counter(il.get("ogrenci","") for il in ilerleme if il.get("tamamlandi"))
        if ogr_durak:
            styled_section("🚏 En Cok Durak Tamamlayan")
            for sira, (ad, sayi) in enumerate(ogr_durak.most_common(5), 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #c9a84c;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ad}</span>
                    <span style="color:#c9a84c;font-weight:800;">{sayi} durak</span>
                </div>""", unsafe_allow_html=True)

        # En cok duello kazanan
        galibiyet = Counter(d.get("kazanan","") for d in duellolar if d.get("kazanan") and d.get("kazanan") != "Berabere")
        if galibiyet:
            styled_section("⚔️ En Cok Duello Kazanan")
            for sira, (ad, sayi) in enumerate(galibiyet.most_common(5), 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #ef4444;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ad}</span>
                    <span style="color:#ef4444;font-weight:800;">{sayi} galibiyet</span>
                </div>""", unsafe_allow_html=True)

        # Hikaye tamamlayan
        hikaye_tam = Counter(h.get("ogrenci","") for h in hikaye_il if h.get("tamamlandi"))
        tam_6 = [ad for ad, sayi in hikaye_tam.items() if sayi >= 6]
        if tam_6:
            styled_section("👑 Bilgi Kralligi Krallari")
            for ad in tam_6:
                st.markdown(f"""
                <div style="background:#c9a84c10;border:2px solid #c9a84c;border-radius:12px;
                    padding:8px 14px;margin:4px 0;text-align:center;">
                    <span style="color:#c9a84c;font-weight:900;font-size:0.9rem;">👑 {ad} — Bilgi Krali!</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Okul Genel Tren Istatistikleri")
        toplam_durak = len(set((il.get("istasyon",""), il.get("durak","")) for il in ilerleme if il.get("tamamlandi")))
        toplam_duello = len(duellolar)
        toplam_gorev = len(gorev_log)
        toplam_xp = sum(y.get("xp", 0) for y in yarisma)
        toplam_hikaye = len(set(h.get("ogrenci","") for h in hikaye_il))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#c9a84c08);border:2px solid #c9a84c;
            border-radius:20px;padding:24px 28px;text-align:center;">
            <div style="color:#c9a84c;font-weight:900;font-size:1.1rem;">🏛️ Tren Muzesi — Tum Zamanlar</div>
            <div style="display:flex;justify-content:center;gap:20px;margin-top:14px;flex-wrap:wrap;">
                <div><div style="color:#10b981;font-weight:900;font-size:1.8rem;">{toplam_durak}</div><div style="color:#64748b;font-size:0.62rem;">Durak</div></div>
                <div><div style="color:#ef4444;font-weight:900;font-size:1.8rem;">{toplam_duello}</div><div style="color:#64748b;font-size:0.62rem;">Duello</div></div>
                <div><div style="color:#3b82f6;font-weight:900;font-size:1.8rem;">{toplam_gorev}</div><div style="color:#64748b;font-size:0.62rem;">Gorev</div></div>
                <div><div style="color:#c9a84c;font-weight:900;font-size:1.8rem;">{toplam_xp}</div><div style="color:#64748b;font-size:0.62rem;">XP</div></div>
                <div><div style="color:#8b5cf6;font-weight:900;font-size:1.8rem;">{toplam_hikaye}</div><div style="color:#64748b;font-size:0.62rem;">Maceraci</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Motivasyon Duvari")
        st.caption("Basari mesajini birak — diger yolcular gorsun!")

        with st.form("motiv_form"):
            m_ad = st.text_input("Adin", key="md_ad")
            m_mesaj = st.text_input("Mesajin", placeholder="Bu trende cok sey ogrendim!", key="md_mesaj")

            if st.form_submit_button("Duvara Yaz", use_container_width=True):
                if m_ad and m_mesaj:
                    motivasyon_duvari.append({
                        "ad": m_ad, "mesaj": m_mesaj,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("motivasyon_duvari.json", motivasyon_duvari)
                    st.success("Mesajin duvara eklendi!")
                    st.rerun()

        if motivasyon_duvari:
            renkler = ["#3b82f6","#10b981","#8b5cf6","#f59e0b","#ef4444","#059669","#6366f1","#c9a84c"]
            for idx, m in enumerate(sorted(motivasyon_duvari, key=lambda x: x.get("tarih",""), reverse=True)[:12]):
                renk = renkler[idx % len(renkler)]
                st.markdown(f"""
                <div style="display:inline-block;background:{renk}10;border:1px solid {renk}30;
                    border-radius:12px;padding:8px 14px;margin:4px;max-width:280px;">
                    <div style="color:{renk};font-weight:700;font-size:0.72rem;">{m.get('ad','')}</div>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:2px;">"{m.get('mesaj','')}"</div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Mezun Arsivi")
        st.info("Mezun tren yolculugu arsivi — donem sonunda otomatik olusur.")
        st.caption("2026 mezunlari icin arsiv hazirlanacak.")
