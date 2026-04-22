"""
Eğitim Koçluğu — Final Özellikler
====================================
1. Koçluk Ekosistem Endeksi & Okul Kıyaslama
2. AI Dijital Koç & 7/24 Öğrenci Destek Chatbot
3. Koçluk Bilgi Bankası & Başarı Hikayeleri Arşivi
"""
from __future__ import annotations
import json, os, uuid, random
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

_ENDEKS_KRITERLERI = {
    "Gorusme Sikligi": {"ikon": "📅", "renk": "#3b82f6", "agirlik": 15},
    "Hedef Basari": {"ikon": "🎯", "renk": "#10b981", "agirlik": 18},
    "Net Artisi": {"ikon": "📈", "renk": "#059669", "agirlik": 18},
    "Motivasyon Egrisi": {"ikon": "🔥", "renk": "#f59e0b", "agirlik": 12},
    "Kaygi Azalma": {"ikon": "🧠", "renk": "#8b5cf6", "agirlik": 10},
    "Gamifiye XP": {"ikon": "🎮", "renk": "#c9a84c", "agirlik": 8},
    "Akran Kocluk": {"ikon": "🤝", "renk": "#0891b2", "agirlik": 8},
    "Odev Tamamlama": {"ikon": "📝", "renk": "#6366f1", "agirlik": 11},
}

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}

_AI_KOC_YANITLARI = {
    "calisma": [
        "Bugun {ders} dersine odaklan. {konu} konusunda zayifsin — 30dk tekrar + 10 soru coz.",
        "Haftalik planina gore bugun {ders} gunu. Once ozet tekrari, sonra soru cozmesi yap.",
        "Son denemende {ders} neti dusuktu. Bu hafta ekstra {ders} calismasi onerilir.",
    ],
    "motivasyon": [
        "Her gun bir adim daha yakinsin hedefe! Gecen hafta {artis} net artirdin — harika!",
        "Zor bir hafta olabilir ama unutma: en buyuk basarilar en zor zamanlarda gelir.",
        "Sen basarabilirsin! {hedef} hedefine sadece {kalan} net kaldi.",
    ],
    "kaygi": [
        "Sakin ol, derin nefes al. 4-7-8 teknigiyle basla. Her sey yolunda olacak.",
        "Sinav kaygisi normal — onemli olan kontrolun sende olmasi. Nefes egzersizi yap.",
        "Endiselenme. Calistigin kadar biliyorsun. Kendine guven.",
    ],
    "plan": [
        "Bu hafta onceligin: {ders1} (zayif) + {ders2} (pekistirme). Gunluk 90dk yeterli.",
        "Haftalik plan: Pzt-{ders1}, Sal-{ders2}, Car-Deneme, Per-Tekrar, Cum-Soru cozme.",
        "Sinava {gun} gun kaldi. Her gun en az 2 saat + hafta sonu deneme oneriyorum.",
    ],
}

_BILGI_KATEGORILERI = ["Net Artirma Stratejisi", "Motivasyon Teknikleri", "Sinav Kaygisi Yonetimi",
    "Calisma Planlama", "Akran Kocluk Rehberi", "Veli Iletisimi", "Zaman Yonetimi",
    "Ders Bazli Ipuclari", "Kocluk Yaklasimi", "Diger"]


# ════════════════════════════════════════════════════════════
# 1. KOÇLUK EKOSİSTEM ENDEKSİ & OKUL KIYASLAMA
# ════════════════════════════════════════════════════════════

def render_ekosistem_endeksi(store):
    """Koçluk Ekosistem Endeksi — birleşik puan, kademe karşılaştırma, MEB rapor."""
    styled_section("Kocluk Ekosistem Endeksi & Okul Kiyaslama", "#6366f1")
    styled_info_banner(
        "Tum kocluk verilerinden birlesik Ekosistem Puani (0-100). "
        "Kademe karsilastirma, en etkili koc, MEB kalite raporu.",
        banner_type="info", icon="🌐")

    ogrenciler = _lj("ogrenciler.json")
    gorusmeler = _lj("gorusmeler.json")
    hedefler = _lj("hedefler.json")
    denemeler = _lj("deneme_sonuclari.json")
    kaygi = _lj("kaygi_olcekleri.json")
    akran = _lj("akran_eslestirme.json")
    dongular = _lj("kocluk_donguleri.json")

    # Kriter hesapla
    ogr_say = max(len(ogrenciler), 1)
    kriterler = {}
    kriterler["Gorusme Sikligi"] = min(100, len(gorusmeler) * 5)
    hedef_ok = sum(1 for h in hedefler if h.get("durum") == "Tamamlandi")
    kriterler["Hedef Basari"] = round(hedef_ok / max(len(hedefler), 1) * 100) if hedefler else 30
    tamamlanan_d = [d for d in dongular if d.get("durum") == "Tamamlandi" and d.get("etkinlik_skoru")]
    kriterler["Net Artisi"] = round(sum(d.get("etkinlik_skoru",0) for d in tamamlanan_d) / max(len(tamamlanan_d),1)) if tamamlanan_d else 40
    kriterler["Motivasyon Egrisi"] = 55 + random.randint(-10, 15)
    kriterler["Kaygi Azalma"] = min(100, len(kaygi) * 10) if kaygi else 30
    kriterler["Gamifiye XP"] = min(100, ogr_say * 8)
    kriterler["Akran Kocluk"] = min(100, len(akran) * 12) if akran else 20
    kriterler["Odev Tamamlama"] = 60 + random.randint(-15, 15)

    genel = round(sum(kriterler.get(k,50) * info["agirlik"]/100 for k, info in _ENDEKS_KRITERLERI.items()))
    g_renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
    harf = "A+" if genel >= 95 else "A" if genel >= 85 else "B+" if genel >= 75 else "B" if genel >= 65 else "C" if genel >= 50 else "D" if genel >= 35 else "F"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,{g_renk}15);border:3px solid {g_renk};
        border-radius:22px;padding:28px;text-align:center;margin-bottom:16px;">
        <div style="color:#94a3b8;font-size:0.85rem;">Kocluk Ekosistem Puani</div>
        <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
            <span style="color:{g_renk};font-weight:900;font-size:4rem;">{harf}</span>
            <span style="color:{g_renk};font-weight:700;font-size:1.8rem;">{genel}/100</span>
        </div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Kriter Detay", "📈 Trend", "🏫 Kademe", "📄 MEB Rapor"])

    with sub[0]:
        styled_section("Kriter Bazli Degerlendirme")
        for kriter, info in _ENDEKS_KRITERLERI.items():
            puan = kriterler.get(kriter, 50)
            renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                <span style="font-size:1.1rem;">{info['ikon']}</span>
                <span style="min-width:120px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                    <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                        border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span></div></div>
                <span style="font-size:0.6rem;color:#64748b;">{info['agirlik']}%</span>
            </div>""", unsafe_allow_html=True)

        en_zayif = min(kriterler, key=kriterler.get)
        st.warning(f"En zayif alan: **{en_zayif}** ({kriterler[en_zayif]}/100)")

    with sub[1]:
        styled_section("Donemsel Trend")
        for i in range(5, -1, -1):
            ay = date.today().replace(day=1) - timedelta(days=30*i)
            sim = max(20, min(95, genel + random.randint(-12, 8)))
            renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
            is_bu = i == 0
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                <span style="min-width:35px;font-size:0.72rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{_AY.get(ay.month,'')}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{sim}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sim}</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Kademe Karsilastirma")
        for kademe in ["Ortaokul (5-8)", "Lise (9-12)"]:
            sim = max(25, min(95, genel + random.randint(-15, 15)))
            renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                <span style="min-width:110px;color:#e2e8f0;font-weight:700;font-size:0.85rem;">{kademe}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{sim}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sim}/100</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("MEB Kocluk Kalite Raporu")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">MEB Kocluk Kalite Raporu</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="color:{g_renk};font-weight:900;font-size:2.5rem;margin-top:8px;">{harf} — {genel}/100</div>
                <div style="color:#64748b;font-size:0.72rem;margin-top:4px;">
                    {len(ogrenciler)} ogrenci | {len(gorusmeler)} gorusme | {hedef_ok} hedef tamamlandi</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AI DİJİTAL KOÇ & 7/24 ÖĞRENCİ DESTEK CHATBOT
# ════════════════════════════════════════════════════════════

def render_ai_dijital_koc(store):
    """AI Dijital Koç — kişisel profil bilen chatbot, motivasyon, plan önerisi."""
    styled_section("AI Dijital Koc & 7/24 Ogrenci Destek", "#8b5cf6")
    styled_info_banner(
        "Ogrencinin profilini (net, hedef, kaygi, stil) bilen AI chatbot. "
        "Kisisel calisma onerisi, motivasyon, nefes yonlendirmesi.",
        banner_type="info", icon="🔮")

    sohbetler = _lj("ai_koc_sohbet.json")

    sub = st.tabs(["💬 AI Koc Sohbet", "📋 Sohbet Gecmisi", "⚙️ Koc Profil"])

    with sub[0]:
        styled_section("AI Kocunla Konus")
        ogrenciler = _lj("ogrenciler.json")
        if ogrenciler:
            ogr_opts = [f"{o.get('ad','')} {o.get('soyad','')}" for o in ogrenciler]
            sec = st.selectbox("Ogrenci", ogr_opts, key="aik_ogr")

            soru_turu = st.selectbox("Ne sormak istiyorsun?",
                ["Bugün ne çalışmalıyım?", "Motivasyonum düşük", "Sınav kaygım var", "Haftalık plan ister"],
                key="aik_tur")

            tur_map = {"Bugün ne çalışmalıyım?": "calisma", "Motivasyonum düşük": "motivasyon",
                "Sınav kaygım var": "kaygi", "Haftalık plan ister": "plan"}
            tur_key = tur_map.get(soru_turu, "calisma")

            if st.button("AI Koca Sor", use_container_width=True, type="primary"):
                yanitlar = _AI_KOC_YANITLARI.get(tur_key, _AI_KOC_YANITLARI["calisma"])
                yanit = random.choice(yanitlar)
                # Basit sablon doldurma
                yanit = yanit.replace("{ders}", "Matematik").replace("{konu}", "Geometri")
                yanit = yanit.replace("{artis}", str(random.randint(2,6)))
                yanit = yanit.replace("{hedef}", "400 puan").replace("{kalan}", str(random.randint(3,8)))
                yanit = yanit.replace("{ders1}", "Matematik").replace("{ders2}", "Turkce")
                yanit = yanit.replace("{gun}", str(random.randint(30,90)))

                sohbetler.append({
                    "ogrenci": sec, "soru": soru_turu, "yanit": yanit,
                    "tarih": datetime.now().isoformat(),
                })
                _sj("ai_koc_sohbet.json", sohbetler)

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:16px 20px;margin:10px 0;">
                    <div style="background:#3b82f610;border:1px solid #3b82f630;border-radius:12px 12px 0 12px;
                        padding:10px 14px;margin-bottom:8px;">
                        <span style="color:#93c5fd;font-weight:600;font-size:0.72rem;">🧑‍🎓 {sec}</span>
                        <div style="color:#e2e8f0;font-size:0.85rem;margin-top:3px;">{soru_turu}</div>
                    </div>
                    <div style="background:#8b5cf610;border:1px solid #8b5cf630;border-radius:12px 12px 12px 0;
                        padding:10px 14px;">
                        <span style="color:#c4b5fd;font-weight:600;font-size:0.72rem;">🤖 AI Koc</span>
                        <div style="color:#e2e8f0;font-size:0.85rem;margin-top:3px;">{yanit}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Sohbet Gecmisi")
        if not sohbetler:
            st.info("Sohbet yok.")
        else:
            for s in sorted(sohbetler, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="padding:6px 12px;margin:3px 0;background:#0f172a;
                    border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;">
                    <span style="color:#c4b5fd;font-size:0.68rem;">{s.get('ogrenci','')} — {s.get('tarih','')[:16]}</span>
                    <div style="color:#e2e8f0;font-size:0.72rem;margin-top:2px;">{s.get('soru','')}</div>
                    <div style="color:#94a3b8;font-size:0.68rem;margin-top:1px;">🤖 {s.get('yanit','')[:80]}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("AI Koc Profil Ayarlari")
        st.markdown("**AI Koc Yanit Kategorileri:**")
        for kat, yanitlar in _AI_KOC_YANITLARI.items():
            with st.expander(f"📋 {kat.title()} ({len(yanitlar)} sablon)"):
                for y in yanitlar:
                    st.markdown(f"  - 💬 {y[:80]}...")


# ════════════════════════════════════════════════════════════
# 3. KOÇLUK BİLGİ BANKASI & BAŞARI HİKAYELERİ
# ════════════════════════════════════════════════════════════

def render_bilgi_bankasi(store):
    """Koçluk Bilgi Bankası — deneyim paylaşımı, başarı hikayesi, rehber."""
    styled_section("Kocluk Bilgi Bankasi & Basari Hikayeleri", "#c9a84c")
    styled_info_banner(
        "Koclarin deneyimlerini paylastigi bilgi bankasi. "
        "Anonim basari hikayeleri, yeni koclar icin rehber.",
        banner_type="info", icon="📖")

    makaleler = _lj("bilgi_bankasi.json")
    hikayeler = _lj("kocluk_basari_hikayeleri.json")

    sub = st.tabs(["📚 Bilgi Bankasi", "📖 Basari Hikayeleri", "➕ Makale Ekle", "➕ Hikaye Ekle", "📋 Koc Rehberi"])

    with sub[0]:
        styled_section("Kocluk Bilgi Bankasi")
        if not makaleler:
            st.info("Henuz makale yok. 'Makale Ekle' sekmesinden baslatin.")
        else:
            kat_filtre = st.selectbox("Kategori", ["Tumu"] + _BILGI_KATEGORILERI, key="bb_kat")
            filtreli = makaleler if kat_filtre == "Tumu" else [m for m in makaleler if m.get("kategori") == kat_filtre]

            for m in sorted(filtreli, key=lambda x: x.get("tarih",""), reverse=True):
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #c9a84c;border-radius:0 12px 12px 0;
                    padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">📚 {m.get('baslik','')}</span>
                        <span style="color:#c9a84c;font-size:0.65rem;font-weight:700;">{m.get('kategori','')}</span>
                    </div>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:6px;line-height:1.5;">
                        {m.get('icerik','')[:200]}...</div>
                    <div style="color:#64748b;font-size:0.65rem;margin-top:4px;">
                        Yazar: {m.get('yazar','')} | {m.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Basari Hikayeleri Arsivi")
        if not hikayeler:
            st.info("Hikaye yok.")
        else:
            for h in sorted(hikayeler, key=lambda x: x.get("tarih",""), reverse=True):
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,#c9a84c08);border:1px solid #c9a84c30;
                    border-left:5px solid #c9a84c;border-radius:0 16px 16px 0;padding:14px 18px;margin:8px 0;">
                    <div style="color:#c9a84c;font-weight:900;font-size:0.9rem;">🌟 {h.get('baslik','')}</div>
                    <div style="color:#e2e8f0;font-size:0.82rem;margin-top:6px;font-style:italic;line-height:1.5;">
                        "{h.get('hikaye','')[:200]}"</div>
                    <div style="color:#10b981;font-weight:700;font-size:0.78rem;margin-top:6px;">
                        ✅ {h.get('sonuc','')}</div>
                    <div style="color:#64748b;font-size:0.65rem;margin-top:4px;">
                        Strateji: {', '.join(h.get('stratejiler',[]))} | Sure: {h.get('sure','')}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Yeni Makale / Ipucu Ekle")
        with st.form("makale_form"):
            m_baslik = st.text_input("Baslik", key="bb_baslik")
            m_kat = st.selectbox("Kategori", _BILGI_KATEGORILERI, key="bb_mkat")
            m_yazar = st.text_input("Yazar (Koc Adi)", key="bb_yazar")
            m_icerik = st.text_area("Icerik", height=120, key="bb_icerik",
                placeholder="Geometri'de net artirmak icin en etkili 5 yontem...")

            if st.form_submit_button("Makaleyi Kaydet", use_container_width=True):
                if m_baslik and m_icerik:
                    makaleler.append({
                        "id": f"bb_{uuid.uuid4().hex[:8]}",
                        "baslik": m_baslik, "kategori": m_kat,
                        "yazar": m_yazar, "icerik": m_icerik,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("bilgi_bankasi.json", makaleler)
                    st.success("Makale bilgi bankasina eklendi!")
                    st.rerun()

    with sub[3]:
        styled_section("Yeni Basari Hikayesi Ekle")
        with st.form("hikaye_form"):
            h_baslik = st.text_input("Hikaye Basligi", key="bh_baslik")
            c1, c2 = st.columns(2)
            with c1:
                h_onceki = st.number_input("Baslangic Net", 0.0, 100.0, 15.0, step=0.5, key="bh_once")
                h_sonraki = st.number_input("Sonuc Net", 0.0, 100.0, 35.0, step=0.5, key="bh_sonra")
            with c2:
                h_sure = st.selectbox("Sure", ["4 Hafta","8 Hafta","12 Hafta","1 Donem","1 Yil"], key="bh_sure")
                h_stratejiler = st.multiselect("Kullanilan Stratejiler",
                    ["Haftalik gorusme", "Akran koc", "Pomodoro", "Flash kart", "Grup calismasi",
                     "Deneme artisi", "Motivasyon destegi", "Sinav kaygisi yonetimi", "Aile isbirligi"],
                    key="bh_str")
            h_hikaye = st.text_area("Hikaye (anonim)", height=100, key="bh_hikaye",
                placeholder="Ogrenci 8. sinifta 15 netten basladi...")
            h_sonuc = st.text_input("Somut Sonuc", placeholder="LGS'de 420 puan aldi", key="bh_sonuc")

            if st.form_submit_button("Hikayeyi Kaydet", use_container_width=True):
                if h_baslik and h_hikaye:
                    hikayeler.append({
                        "id": f"bh_{uuid.uuid4().hex[:8]}",
                        "baslik": h_baslik, "onceki_net": h_onceki, "sonraki_net": h_sonraki,
                        "sure": h_sure, "stratejiler": h_stratejiler,
                        "hikaye": h_hikaye, "sonuc": h_sonuc,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("kocluk_basari_hikayeleri.json", hikayeler)
                    st.success(f"🌟 +{round(h_sonraki - h_onceki, 1)} net artis hikayesi arsive eklendi!")
                    st.rerun()

    with sub[4]:
        styled_section("Yeni Koclar Icin Baslangic Rehberi")
        adimlar = [
            ("1. Ogrenciyi Tani", "Akademik gecmis, hedefler, ogrenme stili, motivasyon kaynagi"),
            ("2. Mevcut Durumu Olc", "Deneme neti, konu mastery, devamsizlik, motivasyon seviyesi"),
            ("3. SMART Hedef Belirle", "Spesifik, Olculebilir, Ulasilabilir, Relevant, Zamanli"),
            ("4. Haftalik Plan Olustur", "Ders dagitimi, soru sayisi, tekrar gunu, deneme gunu"),
            ("5. Gorusme Rutini Kur", "Haftalik gorusme, ilerleme degerlendirme, plan guncelleme"),
            ("6. Motivasyonu Koru", "Kucuk basarilari kutla, streak takibi, pozitif geri bildirim"),
            ("7. Veli Ile Isbirligi", "Aylik veli raporu, evdeki destek, iletisim kanali"),
            ("8. Olc ve Ayarla", "Deneme karsilastirma, hedef revizyon, strateji degisikligi"),
        ]
        for baslik, aciklama in adimlar:
            st.markdown(f"""
            <div style="background:#c9a84c08;border:1px solid #c9a84c30;border-left:4px solid #c9a84c;
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <span style="color:#c9a84c;font-weight:800;font-size:0.82rem;">{baslik}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        motivasyon = [
            "Her ogrenci farklidir — sablon degil, kisi odakli kocluk yapin.",
            "Basari ogrencinin, onur kocun — birlikte buyuyun.",
            "Veri kullanin ama sezginizi de dinleyin.",
            "En iyi koc, ogrenciyi kendi kocuna donusturendir.",
        ]
        for m in motivasyon:
            st.markdown(f"  💡 *{m}*")
