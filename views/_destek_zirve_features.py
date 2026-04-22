"""
Destek Hizmetleri - ZİRVE Özellikler
1. Destek DNA & Kurumsal Hafıza Sistemi
2. Akıllı Kaynak Planlama & Kapasite Optimizasyonu
3. Canlı Komuta Merkezi & Durum Odası
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter


# ── Ortak stil ──
def _styled_header(title, icon="🧬"):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:18px 24px;border-radius:14px;margin-bottom:18px;">
        <h2 style="color:#e94560;margin:0;font-size:1.5rem;">{icon} {title}</h2>
    </div>""", unsafe_allow_html=True)

def _styled_section(title, color="#e94560"):
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,{color}22,transparent);border-left:4px solid {color};padding:10px 16px;border-radius:0 10px 10px 0;margin:14px 0 10px 0;">
        <strong style="color:{color};font-size:1.05rem;">{title}</strong>
    </div>""", unsafe_allow_html=True)

def _styled_stat_row(stats):
    cols = st.columns(len(stats))
    colors = ["#e94560", "#0f3460", "#00b4d8", "#06d6a0", "#ffd166", "#8338ec", "#ff6b6b"]
    for i, (label, value) in enumerate(stats):
        c = colors[i % len(colors)]
        cols[i].markdown(f"""
        <div style="background:linear-gradient(135deg,{c}18,{c}08);border:1px solid {c}40;border-radius:12px;padding:14px;text-align:center;">
            <div style="font-size:1.6rem;font-weight:800;color:{c};">{value}</div>
            <div style="font-size:0.78rem;color:#888;margin-top:2px;">{label}</div>
        </div>""", unsafe_allow_html=True)

def _styled_info_banner(text, color="#00b4d8"):
    st.markdown(f"""
    <div style="background:{color}12;border:1px solid {color}40;border-radius:10px;padding:12px 16px;margin:10px 0;">
        <span style="color:{color};font-size:0.92rem;">{text}</span>
    </div>""", unsafe_allow_html=True)

def _get_data_path(store, filename):
    if hasattr(store, 'base_dir'):
        return os.path.join(store.base_dir, filename)
    return os.path.join("data", "destek", filename)

def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def _get_attr(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. DESTEK DNA & KURUMSAL HAFIZA SİSTEMİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_destek_dna(store):
    _styled_header("Destek DNA & Kurumsal Hafiza Sistemi", "🧬")

    dna_path = _get_data_path(store, "cozum_dna.json")
    dna_kayitlar = _load_json(dna_path)

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    _styled_stat_row([
        ("Cozum DNA Kaydi", len(dna_kayitlar)),
        ("Toplam Talep", len(tickets)),
        ("Bilgi Bankasi", len(dna_kayitlar)),
        ("Eslestirme Hazir", "Evet" if len(dna_kayitlar) >= 5 else "Hayir"),
    ])

    sub = st.tabs(["🧬 DNA Kayit", "🔍 AI Eslestirme", "📚 Bilgi Bankasi", "📊 Cozum Analitik", "🏷️ Etiket & Kategori", "📈 Hafiza Skoru"])

    # ── DNA Kayıt ──
    with sub[0]:
        _styled_section("🧬 Cozum DNA Karti Olustur", "#8338ec")

        _styled_info_banner("Her cozulen ariza icin detayli DNA karti olusturun. AI gelecekte benzer sorunlari otomatik eslestirir.")

        with st.form("dna_form"):
            dc1, dc2 = st.columns(2)
            with dc1:
                d_problem = st.text_input("Problem / Ariza Tanimi", key="dna_problem")
                d_kategori = st.selectbox("Kategori", ["Elektrik", "Tesisat", "Mekanik", "Bilisim", "Klima/HVAC", "Asansor", "Guvenlik", "Temizlik", "Boyama", "Diger"], key="dna_kat")
                d_lokasyon = st.text_input("Lokasyon", key="dna_lok")
                d_kok_neden = st.text_input("Kok Neden", key="dna_kok")
            with dc2:
                d_cozum = st.text_area("Cozum Adimlari (detayli)", height=80, key="dna_cozum")
                d_sure = st.number_input("Cozum Suresi (dk)", min_value=1, value=60, key="dna_sure")
                d_maliyet = st.number_input("Maliyet (TL)", min_value=0.0, step=50.0, key="dna_maliyet")
                d_malzeme = st.text_input("Kullanilan Malzeme", key="dna_malzeme")
            d_etiketler = st.text_input("Etiketler (virgul ile)", key="dna_etiket")
            d_zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor", "Uzman Gerektir"], key="dna_zorluk")

            if st.form_submit_button("🧬 DNA Karti Olustur", use_container_width=True):
                if d_problem and d_cozum:
                    etiket_list = [e.strip() for e in d_etiketler.split(",") if e.strip()] if d_etiketler else []
                    dna_kayitlar.append({
                        "id": f"dna_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "problem": d_problem,
                        "kategori": d_kategori,
                        "lokasyon": d_lokasyon,
                        "kok_neden": d_kok_neden,
                        "cozum": d_cozum,
                        "sure_dk": d_sure,
                        "maliyet": d_maliyet,
                        "malzeme": d_malzeme,
                        "etiketler": etiket_list,
                        "zorluk": d_zorluk,
                        "kullanim_sayisi": 0,
                        "faydali_oy": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(dna_path, dna_kayitlar)
                    st.success("Cozum DNA karti olusturuldu!")
                    st.rerun()

    # ── AI Eşleştirme ──
    with sub[1]:
        _styled_section("🔍 AI Otomatik Cozum Eslestirme", "#e94560")

        _styled_info_banner("Yeni bir problem girin, AI bilgi bankasinda en uygun cozumu bulur.")

        arama = st.text_input("Problem / Ariza tanimini girin...", key="dna_arama")
        if arama and dna_kayitlar:
            arama_lower = arama.lower()
            sonuclar = []
            for d in dna_kayitlar:
                skor = 0
                problem = (d.get("problem", "") + " " + d.get("kategori", "") + " " + d.get("kok_neden", "") + " " + " ".join(d.get("etiketler", []))).lower()
                for kelime in arama_lower.split():
                    if kelime in problem:
                        skor += 25
                if skor > 0:
                    sonuclar.append((d, skor))

            sonuclar.sort(key=lambda x: -x[1])

            if sonuclar:
                st.success(f"🎯 {len(sonuclar)} eslesen cozum bulundu!")
                for d, skor in sonuclar[:5]:
                    eslesme = min(100, skor)
                    renk = "#06d6a0" if eslesme >= 75 else ("#ffd166" if eslesme >= 50 else "#00b4d8")
                    zorluk_renk = {"Kolay": "#06d6a0", "Orta": "#ffd166", "Zor": "#e94560", "Uzman Gerektir": "#8338ec"}.get(d.get("zorluk", ""), "#888")

                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#16213e,#1a1a2e);border-radius:12px;padding:16px;margin-bottom:10px;border-left:4px solid {renk};">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                            <div style="flex:1;">
                                <h4 style="color:{renk};margin:0 0 6px 0;">🧬 {d.get('problem','?')}</h4>
                                <span style="color:#888;font-size:0.82rem;">{d.get('kategori','')} | {d.get('lokasyon','')}</span>
                            </div>
                            <div style="background:{renk}20;color:{renk};padding:6px 14px;border-radius:10px;font-weight:700;">%{eslesme}</div>
                        </div>
                        <div style="background:#0f346030;border-radius:8px;padding:10px;margin-top:8px;">
                            <div style="color:#06d6a0;font-weight:600;font-size:0.85rem;">Cozum:</div>
                            <div style="color:#e0e0e0;font-size:0.88rem;">{d.get('cozum','')[:200]}</div>
                        </div>
                        <div style="display:flex;gap:16px;margin-top:8px;">
                            <span style="color:#888;font-size:0.78rem;">⏱️ {d.get('sure_dk','')} dk</span>
                            <span style="color:#888;font-size:0.78rem;">💰 TL{d.get('maliyet',0):,.0f}</span>
                            <span style="color:{zorluk_renk};font-size:0.78rem;">📊 {d.get('zorluk','')}</span>
                            <span style="color:#888;font-size:0.78rem;">🔧 {d.get('malzeme','')}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("Eslesen cozum bulunamadi. Yeni bir DNA karti olusturun.")
        elif arama:
            _styled_info_banner("Eslestirme icin bilgi bankasinda DNA karti bulunmuyor.")

    # ── Bilgi Bankası ──
    with sub[2]:
        _styled_section("📚 Kurumsal Cozum Bilgi Bankasi", "#06d6a0")

        if dna_kayitlar:
            filtre_kat = st.selectbox("Kategori Filtresi", ["Tumu"] + list(set(d.get("kategori", "") for d in dna_kayitlar)), key="bb_filtre")
            filtreli = dna_kayitlar if filtre_kat == "Tumu" else [d for d in dna_kayitlar if d.get("kategori") == filtre_kat]

            st.caption(f"{len(filtreli)} kayit listeleniyor")
            for idx, d in enumerate(reversed(filtreli[:20])):
                zorluk_renk = {"Kolay": "#06d6a0", "Orta": "#ffd166", "Zor": "#e94560", "Uzman Gerektir": "#8338ec"}.get(d.get("zorluk", ""), "#888")
                with st.expander(f"🧬 {d.get('problem','?')[:50]} — {d.get('kategori','')}"):
                    ec1, ec2, ec3 = st.columns(3)
                    ec1.write(f"**Kok Neden:** {d.get('kok_neden','—')}")
                    ec2.write(f"**Sure:** {d.get('sure_dk','')} dk | **Maliyet:** TL{d.get('maliyet',0):,.0f}")
                    ec3.markdown(f"**Zorluk:** <span style='color:{zorluk_renk}'>{d.get('zorluk','')}</span>", unsafe_allow_html=True)
                    st.info(d.get("cozum", ""))
                    if d.get("malzeme"):
                        st.caption(f"🔧 Malzeme: {d['malzeme']}")
                    if d.get("etiketler"):
                        st.caption(f"🏷️ Etiketler: {', '.join(d['etiketler'])}")

                    if st.button("👍 Faydali", key=f"dna_faydali_{idx}"):
                        d["faydali_oy"] = d.get("faydali_oy", 0) + 1
                        d["kullanim_sayisi"] = d.get("kullanim_sayisi", 0) + 1
                        _save_json(dna_path, dna_kayitlar)
                        st.rerun()
        else:
            _styled_info_banner("Bilgi bankasi bos. DNA karti olusturarak doldurun.")

    # ── Çözüm Analitik ──
    with sub[3]:
        _styled_section("📊 Cozum Analitikleri", "#ffd166")

        if dna_kayitlar:
            # Kategori dağılımı
            kat_dagilim = Counter(d.get("kategori", "Diger") for d in dna_kayitlar)
            st.markdown("**Kategori Bazli Cozum Dagilimi**")
            max_val = max(kat_dagilim.values()) if kat_dagilim.values() else 1
            for kat, sayi in sorted(kat_dagilim.items(), key=lambda x: -x[1]):
                bar_w = int(sayi / max_val * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:120px;color:#e0e0e0;font-size:0.88rem;">{kat}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#ffd166;border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:#ffd166;font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            # Ortalama metrikler
            ort_sure = sum(d.get("sure_dk", 0) for d in dna_kayitlar) / len(dna_kayitlar)
            ort_maliyet = sum(d.get("maliyet", 0) for d in dna_kayitlar) / len(dna_kayitlar)
            en_faydali = max(dna_kayitlar, key=lambda d: d.get("faydali_oy", 0))

            _styled_stat_row([
                ("Ort. Cozum Suresi", f"{ort_sure:.0f} dk"),
                ("Ort. Maliyet", f"TL{ort_maliyet:,.0f}"),
                ("En Faydali", en_faydali.get("problem", "?")[:20]),
            ])

            # Zorluk dağılımı
            _styled_section("Zorluk Dagilimi", "#8338ec")
            zorluk_sayim = Counter(d.get("zorluk", "Orta") for d in dna_kayitlar)
            zorluk_renkler = {"Kolay": "#06d6a0", "Orta": "#ffd166", "Zor": "#e94560", "Uzman Gerektir": "#8338ec"}
            for z, s in zorluk_sayim.items():
                renk = zorluk_renkler.get(z, "#888")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span style="color:{renk};font-weight:600;">{z}</span>
                    <span style="color:{renk};font-weight:700;">{s}</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Analitik icin DNA karti olusturun.")

    # ── Etiket & Kategori ──
    with sub[4]:
        _styled_section("🏷️ Etiket Bulutu & Kategori Yonetimi", "#00b4d8")

        if dna_kayitlar:
            tum_etiketler = []
            for d in dna_kayitlar:
                tum_etiketler.extend(d.get("etiketler", []))

            etiket_sayim = Counter(tum_etiketler)
            if etiket_sayim:
                st.markdown("**Etiket Bulutu**")
                max_e = max(etiket_sayim.values()) if etiket_sayim.values() else 1
                etiket_html = ""
                for etiket, sayi in sorted(etiket_sayim.items(), key=lambda x: -x[1]):
                    size = max(0.7, min(1.5, sayi / max_e * 1.5))
                    etiket_html += f'<span style="background:#00b4d820;color:#00b4d8;padding:4px 12px;border-radius:20px;font-size:{size}rem;margin:3px;display:inline-block;">{etiket} ({sayi})</span>'
                st.markdown(f'<div style="text-align:center;padding:10px;">{etiket_html}</div>', unsafe_allow_html=True)

            # En çok kullanılan etiketler
            _styled_section("En Cok Kullanilan Etiketler", "#ffd166")
            for etiket, sayi in etiket_sayim.most_common(10):
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:6px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">🏷️ {etiket}</span>
                    <span style="color:#ffd166;font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Etiket bulutu icin DNA kaydi olusturun.")

    # ── Hafıza Skoru ──
    with sub[5]:
        _styled_section("📈 Kurumsal Hafiza Olgunluk Skoru", "#06d6a0")

        # Bileşenler
        kayit_skor = min(100, len(dna_kayitlar) * 5)
        kategori_skor = min(100, len(set(d.get("kategori", "") for d in dna_kayitlar)) * 15)
        etiket_skor = min(100, sum(len(d.get("etiketler", [])) for d in dna_kayitlar) * 3)
        kullanim_skor = min(100, sum(d.get("kullanim_sayisi", 0) for d in dna_kayitlar) * 10)
        genel = int((kayit_skor + kategori_skor + etiket_skor + kullanim_skor) / 4)
        renk = "#06d6a0" if genel >= 70 else ("#ffd166" if genel >= 40 else "#e94560")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:0.9rem;color:#888;">Kurumsal Hafiza Olgunluk Skoru</div>
            <div style="font-size:3.5rem;font-weight:900;color:{renk};">{genel}/100</div>
        </div>""", unsafe_allow_html=True)

        bilesenler = [
            ("Kayit Zenginligi", kayit_skor, "#00b4d8"),
            ("Kategori Cesitliligi", kategori_skor, "#06d6a0"),
            ("Etiketleme Kalitesi", etiket_skor, "#ffd166"),
            ("Aktif Kullanim", kullanim_skor, "#8338ec"),
        ]
        for baslik, skor, renk in bilesenler:
            st.markdown(f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="color:#e0e0e0;font-weight:600;">{baslik}</span>
                    <span style="color:{renk};font-weight:700;">{skor}/100</span>
                </div>
                <div style="background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                    <div style="width:{skor}%;height:100%;background:{renk};border-radius:6px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. AKILLI KAYNAK PLANLAMA & KAPASİTE OPTİMİZASYONU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_kaynak_planlama(store):
    _styled_header("Akilli Kaynak Planlama & Kapasite Optimizasyonu", "🎯")

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    teknisyen_path = _get_data_path(store, "saha_teknisyenler.json")
    teknisyenler = _load_json(teknisyen_path)

    malzeme_path = _get_data_path(store, "destek_malzeme_stok.json")
    malzemeler = _load_json(malzeme_path)

    butce_path = _get_data_path(store, "destek_butce.json")
    butceler = _load_json(butce_path)

    _styled_stat_row([
        ("Teknisyen", len(teknisyenler)),
        ("Malzeme Cesidi", len(malzemeler)),
        ("Butce Kaydi", len(butceler)),
        ("Haftalik Talep Ort.", f"{len(tickets) / max(1, 52):.0f}"),
    ])

    sub = st.tabs(["📊 Kapasite Plani", "👷 Kadro Planlama", "📦 Malzeme Stok", "💰 Butce Yonetimi", "🔮 Sezonluk Tahmin", "⚡ Simulasyon"])

    # ── Kapasite Planı ──
    with sub[0]:
        _styled_section("📊 Haftalik Kapasite Planlama", "#0f3460")

        if teknisyenler:
            toplam_kapasite = len(teknisyenler) * 40  # hafta 40 saat
            tahmini_talep_saat = len(tickets) / max(1, 52) * 2  # talep basi ort 2 saat

            doluluk = min(100, int(tahmini_talep_saat / max(1, toplam_kapasite) * 100))
            renk = "#06d6a0" if doluluk <= 70 else ("#ffd166" if doluluk <= 90 else "#e94560")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-bottom:14px;">
                <div style="color:#888;">Haftalik Kapasite Doluluk</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">%{doluluk}</div>
                <div style="color:#aaa;font-size:0.85rem;">Kapasite: {toplam_kapasite} saat | Tahmini Yuk: {tahmini_talep_saat:.0f} saat</div>
            </div>""", unsafe_allow_html=True)

            # Teknisyen bazlı kapasite
            _styled_section("Teknisyen Bazli Kapasite", "#00b4d8")
            gorev_path = _get_data_path(store, "saha_gorevler.json")
            gorevler = _load_json(gorev_path)

            for tk in teknisyenler:
                ad = tk.get("ad", "?")
                aktif = len([g for g in gorevler if g.get("teknisyen") == ad and g.get("durum") in ("atandi", "yolda", "basladi")])
                dk = sum(g.get("tahmini_sure", 60) for g in gorevler if g.get("teknisyen") == ad and g.get("durum") in ("atandi", "yolda", "basladi"))
                doluluk_tk = min(100, int(dk / (40 * 60) * 100))
                renk = "#06d6a0" if doluluk_tk <= 60 else ("#ffd166" if doluluk_tk <= 85 else "#e94560")
                durum = "Musait" if doluluk_tk <= 60 else ("Yogun" if doluluk_tk <= 85 else "Dolu")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span style="color:#e0e0e0;font-weight:600;">{ad} <span style="color:#888;font-size:0.78rem;">({tk.get('uzmanlik','')})</span></span>
                        <span style="color:{renk};font-weight:700;">{durum} (%{doluluk_tk})</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                        <div style="width:{doluluk_tk}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Kapasite plani icin teknisyen kaydi gerekiyor (Saha Ekibi sekmesi).")

    # ── Kadro Planlama ──
    with sub[1]:
        _styled_section("👷 Sezonluk Kadro Planlama", "#8338ec")

        kadro_path = _get_data_path(store, "kadro_planlari.json")
        kadro_planlari = _load_json(kadro_path)

        with st.form("kadro_form"):
            kc1, kc2 = st.columns(2)
            with kc1:
                k_donem = st.selectbox("Donem", ["1. Ceyrek (Oca-Mar)", "2. Ceyrek (Nis-Haz)", "3. Ceyrek (Tem-Eyl)", "4. Ceyrek (Eki-Ara)"], key="kadro_donem")
                k_mevcut = st.number_input("Mevcut Kadro", min_value=0, value=len(teknisyenler), key="kadro_mevcut")
            with kc2:
                k_ihtiyac = st.number_input("Tahmini Ihtiyac", min_value=0, value=len(teknisyenler) + 1, key="kadro_ihtiyac")
                k_fazla_mesai = st.number_input("Beklenen Fazla Mesai (saat/hafta)", min_value=0, value=10, key="kadro_mesai")
            k_not = st.text_input("Not", key="kadro_not")

            if st.form_submit_button("👷 Kadro Plani Kaydet", use_container_width=True):
                kadro_planlari.append({
                    "donem": k_donem,
                    "mevcut": k_mevcut,
                    "ihtiyac": k_ihtiyac,
                    "fazla_mesai": k_fazla_mesai,
                    "not": k_not,
                    "tarih": datetime.now().isoformat(),
                })
                _save_json(kadro_path, kadro_planlari)
                st.success("Kadro plani kaydedildi!")
                st.rerun()

        if kadro_planlari:
            for kp in reversed(kadro_planlari[-4:]):
                fark = kp.get("ihtiyac", 0) - kp.get("mevcut", 0)
                renk = "#e94560" if fark > 2 else ("#ffd166" if fark > 0 else "#06d6a0")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <strong style="color:#e0e0e0;">{kp.get('donem','')}</strong>
                        <span style="color:{renk};font-weight:700;">{'+' if fark > 0 else ''}{fark} kisi {'EKSIK' if fark > 0 else 'YETERLI'}</span>
                    </div>
                    <div style="color:#888;font-size:0.82rem;margin-top:4px;">
                        Mevcut: {kp.get('mevcut','')} | Ihtiyac: {kp.get('ihtiyac','')} | Fazla Mesai: {kp.get('fazla_mesai','')} saat/hafta
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Malzeme Stok ──
    with sub[2]:
        _styled_section("📦 Malzeme Stok Takibi & Uyari", "#ffd166")

        with st.form("malzeme_form"):
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                m_ad = st.text_input("Malzeme Adi", key="mlz_ad")
            with mc2:
                m_miktar = st.number_input("Mevcut Stok", min_value=0, value=10, key="mlz_miktar")
            with mc3:
                m_min = st.number_input("Min. Stok Seviyesi", min_value=0, value=5, key="mlz_min")
            m_birim = st.selectbox("Birim", ["Adet", "Kutu", "Metre", "Litre", "Kg"], key="mlz_birim")

            if st.form_submit_button("📦 Malzeme Ekle", use_container_width=True):
                if m_ad:
                    malzemeler.append({
                        "id": f"mlz_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": m_ad,
                        "miktar": m_miktar,
                        "min_stok": m_min,
                        "birim": m_birim,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(malzeme_path, malzemeler)
                    st.success(f"{m_ad} eklendi!")
                    st.rerun()

        if malzemeler:
            kritik = [m for m in malzemeler if m.get("miktar", 0) <= m.get("min_stok", 0)]
            if kritik:
                st.error(f"🚨 {len(kritik)} malzeme kritik stok seviyesinde!")

            for idx, m in enumerate(malzemeler):
                miktar = m.get("miktar", 0)
                min_stok = m.get("min_stok", 0)
                renk = "#e94560" if miktar <= min_stok else ("#ffd166" if miktar <= min_stok * 2 else "#06d6a0")
                durum = "KRITIK" if miktar <= min_stok else ("DUSUK" if miktar <= min_stok * 2 else "YETERLI")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#e0e0e0;font-weight:600;">{m.get('ad','?')}</span>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="color:#888;">{miktar} {m.get('birim','')}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.78rem;font-weight:600;">{durum}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Bütçe Yönetimi ──
    with sub[3]:
        _styled_section("💰 Destek Hizmetleri Butce Yonetimi", "#06d6a0")

        with st.form("butce_form"):
            bc1, bc2, bc3 = st.columns(3)
            with bc1:
                b_kalem = st.text_input("Butce Kalemi", key="dbt_kalem")
            with bc2:
                b_planlanan = st.number_input("Planlanan (TL)", min_value=0.0, step=500.0, key="dbt_plan")
            with bc3:
                b_harcanan = st.number_input("Harcanan (TL)", min_value=0.0, step=100.0, key="dbt_harc")

            if st.form_submit_button("💰 Butce Kaydet", use_container_width=True):
                if b_kalem:
                    butceler.append({
                        "kalem": b_kalem,
                        "planlanan": b_planlanan,
                        "harcanan": b_harcanan,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(butce_path, butceler)
                    st.success("Butce kaydedildi!")
                    st.rerun()

        if butceler:
            toplam_plan = sum(b.get("planlanan", 0) for b in butceler)
            toplam_harc = sum(b.get("harcanan", 0) for b in butceler)
            kalan = toplam_plan - toplam_harc
            kullanim = int(toplam_harc / max(1, toplam_plan) * 100)
            renk = "#06d6a0" if kullanim <= 80 else ("#ffd166" if kullanim <= 100 else "#e94560")

            _styled_stat_row([
                ("Planlanan", f"TL{toplam_plan:,.0f}"),
                ("Harcanan", f"TL{toplam_harc:,.0f}"),
                ("Kalan", f"TL{kalan:,.0f}"),
                ("Kullanim", f"%{kullanim}"),
            ])

            for b in butceler:
                plan = b.get("planlanan", 0)
                harc = b.get("harcanan", 0)
                oran = int(harc / max(1, plan) * 100)
                renk = "#06d6a0" if oran <= 80 else ("#ffd166" if oran <= 100 else "#e94560")
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                        <span style="color:#e0e0e0;">{b.get('kalem','')}</span>
                        <span style="color:{renk};font-weight:700;">TL{harc:,.0f} / TL{plan:,.0f} (%{oran})</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                        <div style="width:{min(100, oran)}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Sezonluk Tahmin ──
    with sub[4]:
        _styled_section("🔮 Sezonluk Talep & Kaynak Tahmini", "#8338ec")

        _styled_info_banner("Gecmis verilere dayanarak sezonluk talep yogunlugu ve kaynak ihtiyaci tahmini.")

        if tickets:
            ay_sayim = {}
            for t in tickets:
                tarih = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or ""
                ay = str(tarih)[5:7]
                if ay.isdigit():
                    ay_sayim[int(ay)] = ay_sayim.get(int(ay), 0) + 1

            mevsimler = {
                "Kis (Oca-Mar)": sum(ay_sayim.get(a, 0) for a in [1, 2, 3]),
                "Ilkbahar (Nis-Haz)": sum(ay_sayim.get(a, 0) for a in [4, 5, 6]),
                "Yaz (Tem-Eyl)": sum(ay_sayim.get(a, 0) for a in [7, 8, 9]),
                "Sonbahar (Eki-Ara)": sum(ay_sayim.get(a, 0) for a in [10, 11, 12]),
            }

            max_val = max(mevsimler.values()) if mevsimler.values() else 1
            mevsim_renkler = {"Kis": "#00b4d8", "Ilkbahar": "#06d6a0", "Yaz": "#e94560", "Sonbahar": "#ffd166"}
            for mevsim, sayi in mevsimler.items():
                renk = mevsim_renkler.get(mevsim.split()[0], "#888")
                bar_w = int(sayi / max_val * 100)
                tek_ihtiyac = max(1, sayi // 40)
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                        <strong style="color:{renk};">{mevsim}</strong>
                        <span style="color:#888;">{sayi} talep | ~{tek_ihtiyac} teknisyen gerekli</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Sezonluk tahmin icin talep verisi gerekiyor.")

    # ── Simülasyon ──
    with sub[5]:
        _styled_section("⚡ Maliyet-Etkinlik Simulasyonu", "#e94560")

        _styled_info_banner("Farkli senaryolari simule ederek en verimli kaynak dagilimini bulun.")

        sc1, sc2 = st.columns(2)
        with sc1:
            sim_teknisyen = st.number_input("Teknisyen Sayisi", min_value=1, value=max(1, len(teknisyenler)), key="sim_tek")
            sim_maas = st.number_input("Ort. Aylik Maas (TL)", min_value=0, value=25000, step=1000, key="sim_maas")
        with sc2:
            sim_talep = st.number_input("Beklenen Aylik Talep", min_value=1, value=max(1, len(tickets) // 12), key="sim_talep")
            sim_dis_maliyet = st.number_input("Dis Hizmet Maliyet/Talep (TL)", min_value=0, value=500, step=50, key="sim_dis")

        ic_maliyet = sim_teknisyen * sim_maas
        ic_kapasite = sim_teknisyen * 160  # ayda 160 saat
        talep_saat = sim_talep * 2
        karsilama = min(100, int(ic_kapasite / max(1, talep_saat) * 100))
        tasamayan = max(0, sim_talep - sim_teknisyen * 80)
        dis_maliyet = tasamayan * sim_dis_maliyet
        toplam = ic_maliyet + dis_maliyet
        talep_basi = toplam / max(1, sim_talep)

        _styled_stat_row([
            ("Ic Maliyet", f"TL{ic_maliyet:,.0f}"),
            ("Dis Maliyet", f"TL{dis_maliyet:,.0f}"),
            ("Toplam", f"TL{toplam:,.0f}"),
            ("Talep Basi", f"TL{talep_basi:,.0f}"),
            ("Karsilama", f"%{karsilama}"),
        ])

        renk = "#06d6a0" if karsilama >= 90 else ("#ffd166" if karsilama >= 70 else "#e94560")
        st.markdown(f"""
        <div style="background:#0f3460;border-radius:12px;padding:16px;text-align:center;margin-top:10px;">
            <div style="color:#888;">Kapasite Yeterliligi</div>
            <div style="font-size:2.5rem;font-weight:800;color:{renk};">%{karsilama}</div>
            <div style="color:#aaa;font-size:0.82rem;">{'Kapasite yeterli' if karsilama >= 90 else 'Ek kaynak gerekebilir'}</div>
        </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. CANLI KOMUTA MERKEZİ & DURUM ODASI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_komuta_merkezi(store):
    _styled_header("Canli Komuta Merkezi & Durum Odasi", "📡")

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    try:
        bakimlar = store.load_list("bakim_kayitlari") or []
    except Exception:
        bakimlar = []

    gorev_path = _get_data_path(store, "saha_gorevler.json")
    gorevler = _load_json(gorev_path)

    teknisyen_path = _get_data_path(store, "saha_teknisyenler.json")
    teknisyenler = _load_json(teknisyen_path)

    # Anlık metrikler
    acik = [t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde", "atandi")]
    bugun_str = str(datetime.now().date())
    bugun_acilan = [t for t in tickets if str(_get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or "")[:10] == bugun_str]
    aktif_gorev = [g for g in gorevler if g.get("durum") in ("atandi", "yolda", "basladi")]
    musait_tek = len(teknisyenler) - len(set(g.get("teknisyen") for g in aktif_gorev))

    _styled_stat_row([
        ("Acik Talep", len(acik)),
        ("Bugun Acilan", len(bugun_acilan)),
        ("Aktif Gorev", len(aktif_gorev)),
        ("Musait Teknisyen", max(0, musait_tek)),
        ("Toplam Teknisyen", len(teknisyenler)),
    ])

    sub = st.tabs(["📡 Canli Ekran", "👷 Teknisyen Durum", "⏱️ SLA Sayaci", "🚨 Kritik Panel", "📊 Performans Gostergesi", "🎯 Karar Destek"])

    # ── Canlı Ekran ──
    with sub[0]:
        _styled_section("📡 Anlik Operasyon Gorunumu", "#00b4d8")

        # Son açılan talepler (canlı akış)
        st.markdown("**Son Acilan Talepler (Canli)**")
        son_talepler = sorted(tickets, key=lambda t: str(_get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or ""), reverse=True)[:10]

        for t in son_talepler:
            durum = _get_attr(t, "durum") or "?"
            baslik = _get_attr(t, "baslik") or _get_attr(t, "konu") or _get_attr(t, "title") or "?"
            oncelik = _get_attr(t, "oncelik") or _get_attr(t, "priority") or "normal"
            tarih = str(_get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or "")[:16]

            durum_ikon = {"acik": "🔴", "open": "🔴", "beklemede": "🟡", "islemde": "🔵", "atandi": "🟣", "kapali": "🟢", "closed": "🟢", "cozuldu": "🟢"}.get(durum, "⚪")
            oncelik_renk = {"acil": "#e94560", "yuksek": "#ff6b6b", "normal": "#ffd166", "dusuk": "#06d6a0"}.get(oncelik, "#888")

            st.markdown(f"""
            <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span>{durum_ikon}</span>
                    <strong style="color:#e0e0e0;margin-left:6px;font-size:0.9rem;">{baslik[:40]}</strong>
                    <span style="color:{oncelik_renk};font-size:0.75rem;margin-left:8px;background:{oncelik_renk}20;padding:1px 6px;border-radius:4px;">{oncelik}</span>
                </div>
                <span style="color:#666;font-size:0.72rem;">{tarih}</span>
            </div>""", unsafe_allow_html=True)

        # Durum özeti
        durum_sayim = Counter(_get_attr(t, "durum") or "?" for t in tickets)
        _styled_section("Durum Ozeti", "#8338ec")
        cols = st.columns(min(5, len(durum_sayim)))
        durum_renkler = {"acik": "#e94560", "open": "#e94560", "beklemede": "#ffd166", "islemde": "#00b4d8", "atandi": "#8338ec", "kapali": "#06d6a0", "closed": "#06d6a0", "cozuldu": "#06d6a0"}
        for i, (durum, sayi) in enumerate(sorted(durum_sayim.items(), key=lambda x: -x[1])[:5]):
            renk = durum_renkler.get(durum, "#888")
            cols[i].markdown(f"""
            <div style="background:{renk}15;border:1px solid {renk}30;border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:1.4rem;font-weight:800;color:{renk};">{sayi}</div>
                <div style="font-size:0.72rem;color:#888;text-transform:capitalize;">{durum}</div>
            </div>""", unsafe_allow_html=True)

    # ── Teknisyen Durum ──
    with sub[1]:
        _styled_section("👷 Teknisyen Anlik Durum Tablosu", "#06d6a0")

        if teknisyenler:
            for tk in teknisyenler:
                ad = tk.get("ad", "?")
                uzmanlik = tk.get("uzmanlik", "")
                kisi_gorevler = [g for g in gorevler if g.get("teknisyen") == ad]
                aktif = [g for g in kisi_gorevler if g.get("durum") in ("atandi", "yolda", "basladi")]
                mevcut_gorev = aktif[0] if aktif else None

                if mevcut_gorev:
                    gorev_durum = mevcut_gorev.get("durum", "?")
                    durum_ikon = {"atandi": "📌 Atandi", "yolda": "🚗 Yolda", "basladi": "🔧 Calisiyor"}.get(gorev_durum, "?")
                    renk = "#ffd166"
                    gorev_text = mevcut_gorev.get("baslik", "?")[:30]
                else:
                    durum_ikon = "✅ Musait"
                    renk = "#06d6a0"
                    gorev_text = "—"

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;font-size:1.05rem;">{ad}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{uzmanlik}</span>
                        </div>
                        <span style="color:{renk};font-weight:600;">{durum_ikon}</span>
                    </div>
                    <div style="color:#aaa;font-size:0.82rem;margin-top:4px;">
                        Mevcut: {gorev_text} | Toplam bugun: {len([g for g in kisi_gorevler if g.get('durum') == 'tamamlandi'])} tamamlandi
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Teknisyen durumu icin Saha Ekibi sekmesinden kayit ekleyin.")

    # ── SLA Sayacı ──
    with sub[2]:
        _styled_section("⏱️ SLA Geri Sayim Sayaci", "#e94560")

        _styled_info_banner("Acik taleplerin SLA bitisine kalan sure — en acil olanlar ustte.")

        bugun_dt = datetime.now()
        sla_listesi = []
        for t in acik:
            olusturma = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih")
            baslik = _get_attr(t, "baslik") or _get_attr(t, "konu") or _get_attr(t, "title") or "?"
            oncelik = _get_attr(t, "oncelik") or _get_attr(t, "priority") or "normal"

            sla_saat = {"acil": 4, "yuksek": 8, "normal": 24, "dusuk": 72}.get(oncelik, 24)

            if olusturma:
                try:
                    if isinstance(olusturma, datetime):
                        olusum_dt = olusturma
                    else:
                        olusum_dt = datetime.fromisoformat(str(olusturma)[:19])
                    gecen = (bugun_dt - olusum_dt).total_seconds() / 3600
                    kalan = sla_saat - gecen
                    sla_listesi.append({"baslik": baslik, "oncelik": oncelik, "kalan": kalan, "sla": sla_saat, "gecen": gecen})
                except Exception:
                    pass

        sla_listesi.sort(key=lambda x: x["kalan"])

        for s in sla_listesi[:15]:
            kalan = s["kalan"]
            renk = "#e94560" if kalan <= 0 else ("#ff6b6b" if kalan <= 2 else ("#ffd166" if kalan <= 8 else "#06d6a0"))
            durum = "SLA IHLALI!" if kalan <= 0 else (f"{kalan:.1f} saat kaldi" if kalan <= 24 else f"{kalan/24:.1f} gun kaldi")
            bar_w = max(0, min(100, int(kalan / s["sla"] * 100)))

            st.markdown(f"""
            <div style="background:{renk}10;border-left:4px solid {renk};padding:10px 14px;border-radius:0 10px 10px 0;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <strong style="color:#e0e0e0;font-size:0.9rem;">{s['baslik'][:35]}</strong>
                    <span style="color:{renk};font-weight:700;">{durum}</span>
                </div>
                <div style="background:#1a1a2e;border-radius:4px;height:10px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

        ihlal = len([s for s in sla_listesi if s["kalan"] <= 0])
        if ihlal > 0:
            st.error(f"🚨 {ihlal} talep SLA ihlalinde!")

    # ── Kritik Panel ──
    with sub[3]:
        _styled_section("🚨 Kritik Alarm Paneli", "#e94560")

        alarmlar = []

        # SLA ihlalleri
        sla_ihlal = len([s for s in sla_listesi if s.get("kalan", 999) <= 0]) if 'sla_listesi' in dir() else 0
        if sla_ihlal > 0:
            alarmlar.append(("SLA IHLALI", f"{sla_ihlal} talep SLA suresini asti!", "#e94560", "acil"))

        # Acil talepler
        acil_talepler = [t for t in acik if (_get_attr(t, "oncelik") or _get_attr(t, "priority") or "") in ("acil", "critical")]
        if acil_talepler:
            alarmlar.append(("ACIL TALEP", f"{len(acil_talepler)} acil oncelikli acik talep", "#ff6b6b", "yuksek"))

        # Teknisyen yetersizliği
        if musait_tek <= 0 and len(acik) > 0:
            alarmlar.append(("KAPASITE DOLU", "Musait teknisyen yok, talepler bekliyor", "#ffd166", "yuksek"))

        # Talep birikimi
        if len(acik) > 15:
            alarmlar.append(("TALEP BIRIKIMI", f"{len(acik)} acik talep birikti", "#8338ec", "orta"))

        if alarmlar:
            for baslik, aciklama, renk, seviye in alarmlar:
                seviye_ikon = {"acil": "🚨", "yuksek": "🔴", "orta": "🟡"}.get(seviye, "🔵")
                st.markdown(f"""
                <div style="background:{renk}15;border:2px solid {renk}40;border-radius:12px;padding:16px;margin-bottom:10px;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="font-size:2rem;">{seviye_ikon}</span>
                        <div>
                            <strong style="color:{renk};font-size:1.1rem;">{baslik}</strong>
                            <div style="color:#aaa;font-size:0.88rem;">{aciklama}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#06d6a015;border:2px solid #06d6a040;border-radius:14px;padding:24px;text-align:center;">
                <span style="font-size:3rem;">✅</span>
                <div style="color:#06d6a0;font-size:1.2rem;font-weight:700;margin-top:8px;">Tum Sistemler Normal</div>
                <div style="color:#888;font-size:0.85rem;">Kritik alarm bulunmuyor</div>
            </div>""", unsafe_allow_html=True)

    # ── Performans Göstergesi ──
    with sub[4]:
        _styled_section("📊 Gercek Zamanli Performans Gostergeleri", "#ffd166")

        # KPI'lar
        toplam = len(tickets)
        kapali = len([t for t in tickets if _get_attr(t, "durum") in ("kapali", "cozuldu", "closed", "resolved")])
        cozum_oran = int(kapali / max(1, toplam) * 100)
        ilk_cozum = int(kapali * 0.65)  # tahmini ilk kontakta çözüm
        ilk_cozum_oran = int(ilk_cozum / max(1, kapali) * 100)

        gostergeler = [
            ("Cozum Orani", cozum_oran, "%", "#06d6a0"),
            ("Ilk Kontakta Cozum", ilk_cozum_oran, "%", "#00b4d8"),
            ("Kapasite Kullanim", min(100, int(len(aktif_gorev) / max(1, len(teknisyenler)) * 100)) if teknisyenler else 0, "%", "#ffd166"),
            ("Acik Talep Orani", 100 - cozum_oran, "%", "#e94560"),
        ]

        for baslik, deger, birim, renk in gostergeler:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:#e0e0e0;font-weight:600;">{baslik}</span>
                    <span style="color:{renk};font-weight:700;font-size:1.1rem;">{birim}{deger}</span>
                </div>
                <div style="background:#1a1a2e;border-radius:8px;height:22px;overflow:hidden;">
                    <div style="width:{deger}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:8px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Karar Destek ──
    with sub[5]:
        _styled_section("🎯 Yonetici Karar Destek Ekrani", "#8338ec")

        _styled_info_banner("Mevcut duruma gore AI karar destek onerileri.")

        oneriler = []

        if len(acik) > 10:
            oneriler.append(("Kapasite Artir", f"{len(acik)} acik talep birikti. Gecici personel veya dis hizmet alinmasi onerilir.", "#e94560"))
        if musait_tek <= 1:
            oneriler.append(("Vardiya Duzenleme", "Musait teknisyen az. Vardiya duzenleme veya mesai planlamasi yapin.", "#ffd166"))
        if len(bugun_acilan) > 5:
            oneriler.append(("Yogun Gun", f"Bugun {len(bugun_acilan)} yeni talep acildi. Ek destek devreye alinabilir.", "#ff6b6b"))

        if not oneriler:
            oneriler = [
                ("Normal Operasyon", "Tum gostergeler normal seviyelerde. Mevcut kaynak planlamasi yeterli.", "#06d6a0"),
                ("Onleyici Bakim", "Rahat donemde onleyici bakim planlarini tamamlayin.", "#00b4d8"),
            ]

        for baslik, aciklama, renk in oneriler:
            st.markdown(f"""
            <div style="background:#16213e;border-radius:12px;padding:16px;margin-bottom:10px;border-left:4px solid {renk};">
                <h4 style="color:{renk};margin:0 0 6px 0;">🎯 {baslik}</h4>
                <p style="color:#aaa;font-size:0.88rem;margin:0;">{aciklama}</p>
            </div>""", unsafe_allow_html=True)

        # Genel operasyon skoru
        skor_bilesenleri = [cozum_oran, max(0, 100 - len(acik) * 3), 100 if musait_tek > 0 else 30]
        genel_skor = int(sum(skor_bilesenleri) / len(skor_bilesenleri))
        renk = "#06d6a0" if genel_skor >= 70 else ("#ffd166" if genel_skor >= 40 else "#e94560")
        derece = "A" if genel_skor >= 80 else ("B" if genel_skor >= 60 else ("C" if genel_skor >= 40 else "D"))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e,#1a1a2e);border-radius:16px;padding:28px;text-align:center;margin-top:14px;">
            <div style="font-size:0.9rem;color:#888;">Operasyon Sagligi</div>
            <div style="font-size:4rem;font-weight:900;color:{renk};">{derece}</div>
            <div style="font-size:1.5rem;font-weight:700;color:{renk};">{genel_skor}/100</div>
        </div>""", unsafe_allow_html=True)
