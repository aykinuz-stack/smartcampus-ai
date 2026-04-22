"""
STEAM Merkezi — Zirve Özellikler
==================================
1. STEAM Öğrenci DNA & Yetenek Keşif Motoru
2. Akıllı Maker Üretim Hattı & Kanban
3. STEAM Açık Kaynak & Okul Arası Proje Paylaşım
"""
from __future__ import annotations
import json, os, uuid, random, hashlib
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "steam_merkezi"); os.makedirs(d, exist_ok=True); return d
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

_STEAM = {
    "Science": {"ikon":"🔬","renk":"#10b981","aciklama":"Bilimsel dusunme, deney, arastirma"},
    "Technology": {"ikon":"💻","renk":"#3b82f6","aciklama":"Kodlama, IoT, dijital araçlar"},
    "Engineering": {"ikon":"🔧","renk":"#f59e0b","aciklama":"Tasarim, prototip, problem cozme"},
    "Art": {"ikon":"🎨","renk":"#8b5cf6","aciklama":"Yaraticilik, estetik, gorsel tasarim"},
    "Mathematics": {"ikon":"🧮","renk":"#ef4444","aciklama":"Analitik dusunme, hesaplama, modelleme"},
}

_KANBAN_SUTUNLAR = ["Fikir", "Tasarim", "Malzeme", "Uretim", "Test", "Sunum", "Sergi"]
_KANBAN_RENK = {"Fikir":"#94a3b8","Tasarim":"#3b82f6","Malzeme":"#f59e0b","Uretim":"#8b5cf6","Test":"#059669","Sunum":"#0891b2","Sergi":"#c9a84c"}

_YETENEK_ONERILERI = {
    "Science": ["Bilim olimpiyadi", "TUBITAK arastirma projesi", "Laboratuvar asistanligi"],
    "Technology": ["Robotik yarisma", "Hackathon", "Kodlama kampi", "IoT projesi"],
    "Engineering": ["Maker faire", "Kopru/kule yarismasi", "3D tasarim", "FLL"],
    "Art": ["Dijital sanat sergisi", "Interaktif instalasyon", "Gorsel tasarim"],
    "Mathematics": ["Matematik olimpiyadi", "Veri bilimi projesi", "Istatistik arastirma"],
}


# ════════════════════════════════════════════════════════════
# 1. STEAM ÖĞRENCİ DNA & YETENEK KEŞİF
# ════════════════════════════════════════════════════════════

def render_steam_dna(store):
    """STEAM Öğrenci DNA — 5 boyut profil, yetenek keşif, kariyer önerisi."""
    styled_section("STEAM Ogrenci DNA & Yetenek Kesif Motoru", "#6366f1")
    styled_info_banner(
        "Her ogrencinin STEAM aktivitelerinden 'STEAM DNA' profili. "
        "5 boyut radar, yetenek onerisi, kariyer yonlendirme.",
        banner_type="info", icon="🧬")

    dna_profiller = _lj("steam_dna_profiller.json")

    sub = st.tabs(["🧬 DNA Olustur", "👤 Profil Goruntule", "💡 Yetenek Oneri", "📊 Okul Dagilim"])

    with sub[0]:
        styled_section("STEAM DNA Profili Olustur")
        ogr = _ogr_sec("sd_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            with st.form("dna_form"):
                st.markdown("**Her STEAM alanini 0-100 arasi puanla:**")
                puanlar = {}
                cols = st.columns(5)
                for i, (alan, info) in enumerate(_STEAM.items()):
                    with cols[i]:
                        puanlar[alan] = st.slider(f"{info['ikon']} {alan[:3]}", 0, 100, 50, key=f"sd_{alan}")

                if st.form_submit_button("DNA Kaydet", use_container_width=True, type="primary"):
                    sirali = sorted(puanlar.items(), key=lambda x: x[1], reverse=True)
                    dna_kod = "-".join(f"{a[0][:1]}{a[1]}" for a in sirali[:3])
                    baskin = sirali[0][0]

                    dna_profiller.append({
                        "id": f"sd_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "sinif": ogr.get("sinif",""), "sube": ogr.get("sube",""),
                        "puanlar": puanlar, "dna_kod": dna_kod, "baskin": baskin,
                        "tarih": date.today().isoformat(),
                    })
                    _sj("steam_dna_profiller.json", dna_profiller)
                    st.success(f"🧬 STEAM DNA: {dna_kod} — Baskin: {_STEAM[baskin]['ikon']} {baskin}")
                    st.rerun()

    with sub[1]:
        styled_section("STEAM DNA Profil Kartlari")
        if not dna_profiller:
            st.info("Profil yok.")
        else:
            for p in sorted(dna_profiller, key=lambda x: x.get("tarih",""), reverse=True)[:15]:
                baskin = p.get("baskin","?")
                b_info = _STEAM.get(baskin, {"ikon":"?","renk":"#94a3b8"})

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f172a,{b_info['renk']}10);
                    border:2px solid {b_info['renk']};border-radius:18px;padding:16px 20px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">🧬 {p.get('ogrenci','')}</div>
                            <div style="color:#94a3b8;font-size:0.72rem;">{p.get('sinif','')}/{p.get('sube','')}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-family:monospace;color:{b_info['renk']};font-weight:900;font-size:0.9rem;">
                                {p.get('dna_kod','')}</div>
                            <div style="background:{b_info['renk']}20;color:{b_info['renk']};padding:2px 8px;
                                border-radius:6px;font-size:0.68rem;font-weight:700;margin-top:2px;">
                                {b_info['ikon']} {baskin}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

                # Boyut bar
                for alan, info in _STEAM.items():
                    puan = p.get("puanlar",{}).get(alan, 50)
                    renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin:2px 0;padding-left:16px;">
                        <span style="font-size:0.8rem;">{info['ikon']}</span>
                        <span style="min-width:15px;color:#e2e8f0;font-size:0.68rem;">{alan[:1]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:3px;height:10px;overflow:hidden;">
                            <div style="width:{puan}%;height:100%;background:{renk};border-radius:3px;"></div>
                        </div>
                        <span style="color:#64748b;font-size:0.6rem;min-width:20px;">{puan}</span>
                    </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Yetenek Kesif & Kariyer Onerisi")
        if not dna_profiller:
            st.info("Once DNA profili olusturun.")
        else:
            sec = st.selectbox("Ogrenci",
                [f"{p.get('ogrenci','')} ({p.get('baskin','')})" for p in dna_profiller], key="sd_oneri")
            idx = [f"{p.get('ogrenci','')} ({p.get('baskin','')})" for p in dna_profiller].index(sec) if sec else 0
            profil = dna_profiller[idx]
            puanlar = profil.get("puanlar",{})

            # En guclu 2 alan
            sirali = sorted(puanlar.items(), key=lambda x: x[1], reverse=True)
            for alan, puan in sirali[:2]:
                info = _STEAM[alan]
                oneriler = _YETENEK_ONERILERI.get(alan, [])
                st.markdown(f"""
                <div style="background:{info['renk']}08;border:1px solid {info['renk']}30;border-left:5px solid {info['renk']};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                    <span style="color:{info['renk']};font-weight:800;font-size:0.9rem;">{info['ikon']} {alan} (Puan: {puan})</span>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">{info['aciklama']}</div>
                    <div style="margin-top:6px;">
                        {"".join(f"<div style='color:#e2e8f0;font-size:0.75rem;padding:2px 0;'>💡 {o}</div>" for o in oneriler)}
                    </div>
                </div>""", unsafe_allow_html=True)

            # En zayif
            en_zayif = sirali[-1]
            st.info(f"Gelisim firsati: **{en_zayif[0]}** ({en_zayif[1]}/100) — bu alanda challenge ve proje oneririz.")

    with sub[3]:
        styled_section("Okul Geneli STEAM DNA Dagilimi")
        if dna_profiller:
            baskin_say = Counter(p.get("baskin","") for p in dna_profiller)
            toplam = max(len(dna_profiller), 1)
            for alan, info in _STEAM.items():
                sayi = baskin_say.get(alan, 0)
                pct = round(sayi / toplam * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="font-size:1.2rem;">{info['ikon']}</span>
                    <span style="min-width:90px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{alan}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{info['renk']};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sayi} (%{pct})</span></div></div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AKILLI MAKER ÜRETİM HATTI & KANBAN
# ════════════════════════════════════════════════════════════

def render_maker_kanban(store):
    """Akıllı Maker Üretim Hattı — Kanban board, darboğaz, kaynak çakışma."""
    styled_section("Akilli Maker Uretim Hatti & Kanban Panosu", "#f59e0b")
    styled_info_banner(
        "Tum STEAM projelerini Kanban board uzerinde izleyin. "
        "Darbogaz tespiti, kaynak cakisma uyarisi, tahmini tamamlanma.",
        banner_type="info", icon="🏭")

    kanban_kartlar = _lj("kanban_kartlar.json")

    # Sutun sayilari
    sutun_say = Counter(k.get("sutun","Fikir") for k in kanban_kartlar)
    toplam = len(kanban_kartlar)

    styled_stat_row([
        ("Toplam Proje", str(toplam), "#f59e0b", "📋"),
        ("Uretimde", str(sutun_say.get("Uretim",0)), "#8b5cf6", "🔧"),
        ("Tamamlanan", str(sutun_say.get("Sergi",0)), "#10b981", "✅"),
    ])

    sub = st.tabs(["📋 Kanban Board", "➕ Kart Ekle", "⚠️ Darbogaz", "📊 Akis Analizi"])

    with sub[0]:
        styled_section("Maker Kanban Panosu")
        if not kanban_kartlar:
            st.info("Kart yok. 'Kart Ekle' sekmesinden baslatin.")
        else:
            for sutun in _KANBAN_SUTUNLAR:
                renk = _KANBAN_RENK.get(sutun, "#94a3b8")
                kartlar = [k for k in kanban_kartlar if k.get("sutun") == sutun]

                st.markdown(f"""
                <div style="background:{renk}10;border:1px solid {renk}30;border-top:4px solid {renk};
                    border-radius:10px;padding:10px 14px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="color:{renk};font-weight:800;font-size:0.85rem;">{sutun}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{len(kartlar)}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

                for k in kartlar:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;padding:4px 12px 4px 24px;margin:2px 0;
                        border-left:2px solid {renk};background:#0f172a80;border-radius:0 6px 6px 0;">
                        <span style="color:#e2e8f0;font-size:0.75rem;font-weight:600;flex:1;">{k.get('ad','')}</span>
                        <span style="color:#64748b;font-size:0.62rem;">{k.get('ekip','')[:15]}</span>
                    </div>""", unsafe_allow_html=True)

                    with st.expander(f"Tasi: {k.get('id','')}", expanded=False):
                        mevcut_idx = _KANBAN_SUTUNLAR.index(sutun) if sutun in _KANBAN_SUTUNLAR else 0
                        if mevcut_idx < len(_KANBAN_SUTUNLAR) - 1:
                            sonraki = _KANBAN_SUTUNLAR[mevcut_idx + 1]
                            if st.button(f"→ {sonraki}'a Tasi", key=f"kn_t_{k['id']}"):
                                k["sutun"] = sonraki
                                _sj("kanban_kartlar.json", kanban_kartlar)
                                st.rerun()

    with sub[1]:
        styled_section("Yeni Kanban Karti Ekle")
        with st.form("kanban_form"):
            c1, c2 = st.columns(2)
            with c1:
                kn_ad = st.text_input("Proje Adi", key="kn_ad")
                kn_ekip = st.text_input("Ekip", key="kn_ekip")
            with c2:
                kn_sutun = st.selectbox("Baslangic Asamasi", _KANBAN_SUTUNLAR, key="kn_sutun")
                kn_oncelik = st.selectbox("Oncelik", ["Dusuk","Normal","Yuksek","Acil"], key="kn_onc")

            if st.form_submit_button("Kart Ekle", use_container_width=True):
                if kn_ad:
                    kanban_kartlar.append({
                        "id": f"kn_{uuid.uuid4().hex[:8]}",
                        "ad": kn_ad, "ekip": kn_ekip,
                        "sutun": kn_sutun, "oncelik": kn_oncelik,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("kanban_kartlar.json", kanban_kartlar)
                    st.success(f"📋 '{kn_ad}' Kanban'a eklendi!")
                    st.rerun()

    with sub[2]:
        styled_section("Darbogaz Tespiti")
        if kanban_kartlar:
            max_sutun = max(sutun_say.values()) if sutun_say else 0
            darbogaz = [s for s, c in sutun_say.items() if c >= max(3, max_sutun * 0.6)]

            if darbogaz:
                for d in darbogaz:
                    sayi = sutun_say[d]
                    renk = _KANBAN_RENK.get(d, "#ef4444")
                    st.markdown(f"""
                    <div style="background:#ef444410;border:1px solid #ef444430;border-left:5px solid {renk};
                        border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                        <span style="color:#fca5a5;font-weight:800;font-size:0.85rem;">
                            ⚠️ DARBOGAZ: {d} asamasinda {sayi} proje bekleniyor!</span>
                        <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                            Kaynak artirin veya projeleri oncelik sirasina koyun.</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("Darbogaz tespit edilmedi — akis duzenli!")

            # Akis grafigi
            styled_section("Sutun Bazli Dagılım")
            for sutun in _KANBAN_SUTUNLAR:
                sayi = sutun_say.get(sutun, 0)
                pct = round(sayi / max(toplam, 1) * 100) if toplam > 0 else 0
                renk = _KANBAN_RENK.get(sutun, "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:65px;color:{renk};font-weight:700;font-size:0.78rem;">{sutun}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Akis Analizi & Tahmin")
        if kanban_kartlar:
            tamamlanan = sutun_say.get("Sergi", 0)
            devam_eden = toplam - tamamlanan
            tamamlama_oran = round(tamamlanan / max(toplam, 1) * 100)
            renk = "#10b981" if tamamlama_oran >= 60 else "#f59e0b" if tamamlama_oran >= 30 else "#ef4444"

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid {renk};border-radius:16px;padding:16px;text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">Maker Uretim Hatti Durumu</div>
                <div style="display:flex;justify-content:center;gap:24px;margin-top:10px;">
                    <div><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{devam_eden}</div><div style="color:#64748b;font-size:0.62rem;">Devam Eden</div></div>
                    <div><div style="color:#10b981;font-weight:900;font-size:1.5rem;">{tamamlanan}</div><div style="color:#64748b;font-size:0.62rem;">Tamamlanan</div></div>
                    <div><div style="color:{renk};font-weight:900;font-size:1.5rem;">%{tamamlama_oran}</div><div style="color:#64748b;font-size:0.62rem;">Oran</div></div>
                </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 3. STEAM AÇIK KAYNAK & PROJE PAYLAŞIM
# ════════════════════════════════════════════════════════════

def render_acik_kaynak(store):
    """STEAM Açık Kaynak — proje paylaşım, indirme, okul arası işbirliği."""
    styled_section("STEAM Acik Kaynak & Okul Arasi Proje Paylasim", "#059669")
    styled_info_banner(
        "Tamamlanan projeleri diger okullarla paylasin. "
        "Proje karti, malzeme listesi, adimlar, okul arasi isbirligi.",
        banner_type="info", icon="🌐")

    paylasimlar = _lj("acik_kaynak_projeler.json")
    indirmeler = _lj("proje_indirme.json")
    isbirlikleri = _lj("okul_arasi_isbirligi.json")

    styled_stat_row([
        ("Paylasilan", str(len(paylasimlar)), "#059669", "📤"),
        ("Indirme", str(len(indirmeler)), "#3b82f6", "📥"),
        ("Isbirligi", str(len(isbirlikleri)), "#8b5cf6", "🤝"),
    ])

    sub = st.tabs(["📤 Proje Paylas", "📥 Proje Kesfet", "🤝 Isbirligi", "🏆 En Populer"])

    with sub[0]:
        styled_section("Proje Paylas (Acik Kaynak)")
        with st.form("paylas_form"):
            c1, c2 = st.columns(2)
            with c1:
                py_ad = st.text_input("Proje Adi", key="py_ad")
                py_alan = st.multiselect("STEAM Alanlari", list(_STEAM.keys()), key="py_alan")
                py_zorluk = st.selectbox("Zorluk", ["Kolay","Orta","Zor","Uzman"], key="py_zor")
            with c2:
                py_sinif = st.text_input("Hedef Sinif", placeholder="5-8. sinif", key="py_sinif")
                py_sure = st.text_input("Tahmini Sure", placeholder="2 saat, 1 hafta...", key="py_sure")
            py_aciklama = st.text_area("Proje Aciklamasi", height=60, key="py_acik")
            py_malzeme = st.text_area("Malzeme Listesi", height=40, key="py_mal", placeholder="Arduino, LED, direnc...")
            py_adimlar = st.text_area("Proje Adimlari", height=60, key="py_adim", placeholder="1. Devre kur\n2. Kod yaz...")

            if st.form_submit_button("Projeyi Paylas", use_container_width=True, type="primary"):
                if py_ad:
                    paylasimlar.append({
                        "id": f"py_{uuid.uuid4().hex[:8]}",
                        "ad": py_ad, "alanlar": py_alan, "zorluk": py_zorluk,
                        "sinif": py_sinif, "sure": py_sure,
                        "aciklama": py_aciklama, "malzeme": py_malzeme,
                        "adimlar": py_adimlar, "indirme_sayi": 0,
                        "begeni": 0, "tarih": date.today().isoformat(),
                    })
                    _sj("acik_kaynak_projeler.json", paylasimlar)
                    st.success(f"📤 '{py_ad}' acik kaynak olarak paylasıldı!")
                    st.rerun()

    with sub[1]:
        styled_section("Proje Kesfet & Indir")
        if not paylasimlar:
            st.info("Paylasilan proje yok.")
        else:
            alan_filtre = st.selectbox("STEAM Filtre", ["Tumu"] + list(_STEAM.keys()), key="py_filtre")
            filtreli = paylasimlar if alan_filtre == "Tumu" else [p for p in paylasimlar if alan_filtre in p.get("alanlar",[])]

            for p in sorted(filtreli, key=lambda x: x.get("indirme_sayi",0), reverse=True):
                alanlar = " ".join(_STEAM.get(a,{}).get("ikon","") for a in p.get("alanlar",[]))
                zorluk_renk = {"Kolay":"#10b981","Orta":"#f59e0b","Zor":"#ef4444","Uzman":"#8b5cf6"}.get(p.get("zorluk",""),"#94a3b8")

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #05966930;border-left:5px solid #059669;
                    border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">📦 {p.get('ad','')}</span>
                        <span style="background:{zorluk_renk}20;color:{zorluk_renk};padding:2px 8px;
                            border-radius:6px;font-size:0.68rem;font-weight:700;">{p.get('zorluk','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        {alanlar} | {p.get('sinif','')} | {p.get('sure','')}</div>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:4px;">{p.get('aciklama','')[:100]}</div>
                    <div style="color:#64748b;font-size:0.65rem;margin-top:4px;">
                        📥 {p.get('indirme_sayi',0)} indirme | ❤️ {p.get('begeni',0)} begeni</div>
                </div>""", unsafe_allow_html=True)

                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button(f"📥 Indir", key=f"py_i_{p['id']}"):
                        p["indirme_sayi"] = p.get("indirme_sayi", 0) + 1
                        indirmeler.append({"proje": p["ad"], "tarih": datetime.now().isoformat()})
                        _sj("acik_kaynak_projeler.json", paylasimlar)
                        _sj("proje_indirme.json", indirmeler)
                        st.success(f"📥 {p['ad']} indirildi!")
                with bc2:
                    if st.button(f"❤️ Begen", key=f"py_b_{p['id']}"):
                        p["begeni"] = p.get("begeni", 0) + 1
                        _sj("acik_kaynak_projeler.json", paylasimlar)
                        st.rerun()

    with sub[2]:
        styled_section("Okul Arasi Isbirligi")
        with st.form("isbirligi_form"):
            c1, c2 = st.columns(2)
            with c1:
                ib_okul = st.text_input("Partner Okul", key="ib_okul")
                ib_proje = st.text_input("Ortak Proje Fikri", key="ib_proje")
            with c2:
                ib_alan = st.multiselect("STEAM Alanlari", list(_STEAM.keys()), key="ib_alan")

            if st.form_submit_button("Isbirligi Oner", use_container_width=True):
                if ib_okul and ib_proje:
                    isbirlikleri.append({
                        "okul": ib_okul, "proje": ib_proje,
                        "alanlar": ib_alan, "durum": "Onerild",
                        "tarih": date.today().isoformat(),
                    })
                    _sj("okul_arasi_isbirligi.json", isbirlikleri)
                    st.success(f"🤝 {ib_okul} ile isbirligi onerisi gonderildi!")
                    st.rerun()

        if isbirlikleri:
            for ib in isbirlikleri:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">
                        🤝 {ib.get('okul','')} — {ib.get('proje','')}</span>
                    <span style="color:#8b5cf6;font-size:0.65rem;font-weight:700;">{ib.get('durum','')}</span>
                </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("En Populer Projeler")
        if paylasimlar:
            sirali = sorted(paylasimlar, key=lambda x: x.get("indirme_sayi",0) + x.get("begeni",0), reverse=True)
            for sira, p in enumerate(sirali[:10], 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                renk = "#c9a84c" if sira <= 3 else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{p.get('ad','')}</span>
                    <span style="color:#3b82f6;font-size:0.68rem;">📥{p.get('indirme_sayi',0)}</span>
                    <span style="color:#ef4444;font-size:0.68rem;">❤️{p.get('begeni',0)}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Proje yok.")
