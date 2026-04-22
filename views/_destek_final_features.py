"""
Destek Hizmetleri - FİNAL Özellikler
1. Dijital Denetim & Uyumluluk Merkezi
2. Çok Kampüslü Operasyon & Benchmark Merkezi
3. AI Operasyon Asistanı & Otonom Karar Motoru
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter


# ── Ortak stil ──
def _styled_header(title, icon="📋"):
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
#  1. DİJİTAL DENETİM & UYUMLULUK MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_denetim_uyumluluk(store):
    _styled_header("Dijital Denetim & Uyumluluk Merkezi", "📋")

    checklist_path = _get_data_path(store, "uyumluluk_checklist.json")
    checklists = _load_json(checklist_path)

    capa_path = _get_data_path(store, "capa_kayitlari.json")
    capalar = _load_json(capa_path)

    sertifika_path = _get_data_path(store, "denetim_sertifikalari.json")
    sertifikalar = _load_json(sertifika_path)

    tamamlanan = [c for c in checklists if c.get("durum") == "tamamlandi"]
    uyum_oran = int(len(tamamlanan) / max(1, len(checklists)) * 100) if checklists else 0

    _styled_stat_row([
        ("Checklist Sayisi", len(checklists)),
        ("Tamamlanan", len(tamamlanan)),
        ("Uyumluluk", f"%{uyum_oran}"),
        ("CAPA Kaydi", len(capalar)),
        ("Sertifika", len(sertifikalar)),
    ])

    sub = st.tabs(["📋 Uyumluluk Checklist", "📊 Standart Takibi", "🔄 CAPA Yonetimi", "📜 Sertifika Takip", "📝 Denetim Hazirligi", "📈 Uyumluluk Skoru"])

    # ── Uyumluluk Checklist ──
    with sub[0]:
        _styled_section("📋 Uyumluluk Checklist Olustur", "#0f3460")

        with st.form("checklist_form"):
            cc1, cc2 = st.columns(2)
            with cc1:
                c_baslik = st.text_input("Checklist Maddesi", key="ck_baslik")
                c_standart = st.selectbox("Standart", ["ISO 9001", "OHSAS 18001", "ISO 14001", "MEB Denetim", "Is Guvenligi", "Yangin Guvenligi", "Hijyen", "Genel"], key="ck_standart")
            with cc2:
                c_kategori = st.selectbox("Kategori", ["Prosedur", "Dokuman", "Ekipman", "Egitim", "Kayit", "Fiziksel Ortam", "Diger"], key="ck_kat")
                c_sorumlu = st.text_input("Sorumlu", key="ck_sorumlu")
            c_aciklama = st.text_input("Aciklama", key="ck_acik")

            if st.form_submit_button("📋 Checklist Ekle", use_container_width=True):
                if c_baslik:
                    checklists.append({
                        "id": f"ck_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": c_baslik,
                        "standart": c_standart,
                        "kategori": c_kategori,
                        "sorumlu": c_sorumlu,
                        "aciklama": c_aciklama,
                        "durum": "beklemede",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(checklist_path, checklists)
                    st.success("Checklist maddesi eklendi!")
                    st.rerun()

        if checklists:
            standart_filtre = st.selectbox("Standart Filtresi", ["Tumu"] + list(set(c.get("standart", "") for c in checklists)), key="ck_filtre")
            filtreli = checklists if standart_filtre == "Tumu" else [c for c in checklists if c.get("standart") == standart_filtre]

            for idx, c in enumerate(filtreli):
                durum = c.get("durum", "beklemede")
                durum_ikon = {"beklemede": "⬜", "tamamlandi": "✅", "uygunsuz": "❌"}.get(durum, "⚪")
                renk = {"beklemede": "#888", "tamamlandi": "#06d6a0", "uygunsuz": "#e94560"}.get(durum, "#888")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{durum_ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{c.get('baslik','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{c.get('standart','')} | {c.get('sorumlu','')}</span>
                    </div>
                    <span style="color:{renk};font-weight:600;font-size:0.82rem;">{durum.upper()}</span>
                </div>""", unsafe_allow_html=True)

                bc1, bc2, bc3 = st.columns(3)
                if bc1.button("✅", key=f"ck_ok_{idx}"):
                    c["durum"] = "tamamlandi"
                    _save_json(checklist_path, checklists)
                    st.rerun()
                if bc2.button("❌", key=f"ck_fail_{idx}"):
                    c["durum"] = "uygunsuz"
                    _save_json(checklist_path, checklists)
                    st.rerun()
                if bc3.button("⬜", key=f"ck_reset_{idx}"):
                    c["durum"] = "beklemede"
                    _save_json(checklist_path, checklists)
                    st.rerun()

    # ── Standart Takibi ──
    with sub[1]:
        _styled_section("📊 Standart Bazli Uyumluluk Takibi", "#8338ec")

        if checklists:
            standart_grup = {}
            for c in checklists:
                s = c.get("standart", "Diger")
                if s not in standart_grup:
                    standart_grup[s] = {"toplam": 0, "tamam": 0, "uygunsuz": 0}
                standart_grup[s]["toplam"] += 1
                if c.get("durum") == "tamamlandi":
                    standart_grup[s]["tamam"] += 1
                elif c.get("durum") == "uygunsuz":
                    standart_grup[s]["uygunsuz"] += 1

            for standart, data in standart_grup.items():
                oran = int(data["tamam"] / max(1, data["toplam"]) * 100)
                renk = "#06d6a0" if oran >= 80 else ("#ffd166" if oran >= 50 else "#e94560")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:10px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <strong style="color:#e0e0e0;font-size:1.05rem;">{standart}</strong>
                        <span style="color:{renk};font-weight:800;font-size:1.3rem;">%{oran}</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;margin-bottom:6px;">
                        <div style="width:{oran}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <div style="display:flex;gap:16px;">
                        <span style="color:#06d6a0;font-size:0.78rem;">✅ {data['tamam']}</span>
                        <span style="color:#e94560;font-size:0.78rem;">❌ {data['uygunsuz']}</span>
                        <span style="color:#888;font-size:0.78rem;">⬜ {data['toplam'] - data['tamam'] - data['uygunsuz']}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Standart takibi icin checklist olusturun.")

    # ── CAPA Yönetimi ──
    with sub[2]:
        _styled_section("🔄 Duzeltici & Onleyici Faaliyet (CAPA)", "#e94560")

        with st.form("capa_form"):
            pc1, pc2 = st.columns(2)
            with pc1:
                p_bulgu = st.text_input("Uygunsuzluk / Bulgu", key="capa_bulgu")
                p_tur = st.selectbox("Faaliyet Turu", ["Duzeltici (Corrective)", "Onleyici (Preventive)"], key="capa_tur")
                p_neden = st.text_input("Kok Neden", key="capa_neden")
            with pc2:
                p_faaliyet = st.text_area("Planlanan Faaliyet", height=68, key="capa_faaliyet")
                p_sorumlu = st.text_input("Sorumlu", key="capa_sorumlu")
                p_hedef = st.date_input("Hedef Tarih", value=datetime.now().date() + timedelta(days=30), key="capa_hedef")

            if st.form_submit_button("🔄 CAPA Olustur", use_container_width=True):
                if p_bulgu and p_faaliyet:
                    capalar.append({
                        "id": f"capa_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "bulgu": p_bulgu,
                        "tur": p_tur,
                        "neden": p_neden,
                        "faaliyet": p_faaliyet,
                        "sorumlu": p_sorumlu,
                        "hedef": str(p_hedef),
                        "durum": "acik",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(capa_path, capalar)
                    st.success("CAPA kaydi olusturuldu!")
                    st.rerun()

        if capalar:
            for idx, ca in enumerate(reversed(capalar[-12:])):
                durum = ca.get("durum", "acik")
                renk = {"acik": "#e94560", "devam": "#ffd166", "tamamlandi": "#06d6a0", "dogrulandi": "#00b4d8"}.get(durum, "#888")
                ikon = {"acik": "🔴", "devam": "🟡", "tamamlandi": "🟢", "dogrulandi": "✅"}.get(durum, "⚪")

                with st.expander(f"{ikon} {ca.get('bulgu','?')[:40]} — {ca.get('tur','')[:10]}"):
                    st.write(f"**Kok Neden:** {ca.get('neden','—')}")
                    st.write(f"**Faaliyet:** {ca.get('faaliyet','')}")
                    st.write(f"**Sorumlu:** {ca.get('sorumlu','')} | **Hedef:** {ca.get('hedef','')}")
                    yeni = st.selectbox("Durum", ["acik", "devam", "tamamlandi", "dogrulandi"], index=["acik", "devam", "tamamlandi", "dogrulandi"].index(durum), key=f"capa_d_{idx}")
                    if st.button("Guncelle", key=f"capa_btn_{idx}"):
                        ca["durum"] = yeni
                        _save_json(capa_path, capalar)
                        st.rerun()

    # ── Sertifika Takip ──
    with sub[3]:
        _styled_section("📜 Sertifika & Belge Gecerlilik Takibi", "#ffd166")

        with st.form("sertifika_form"):
            sc1, sc2 = st.columns(2)
            with sc1:
                s_ad = st.text_input("Sertifika / Belge Adi", key="dsrt_ad")
                s_kurum = st.text_input("Veren Kurum", key="dsrt_kurum")
            with sc2:
                s_alis = st.date_input("Alis Tarihi", value=datetime.now().date(), key="dsrt_alis")
                s_bitis = st.date_input("Gecerlilik Bitis", value=datetime.now().date() + timedelta(days=365), key="dsrt_bitis")

            if st.form_submit_button("📜 Sertifika Ekle", use_container_width=True):
                if s_ad:
                    sertifikalar.append({
                        "id": f"dsrt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": s_ad,
                        "kurum": s_kurum,
                        "alis": str(s_alis),
                        "bitis": str(s_bitis),
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(sertifika_path, sertifikalar)
                    st.success("Sertifika eklendi!")
                    st.rerun()

        if sertifikalar:
            bugun = str(datetime.now().date())
            for s in sorted(sertifikalar, key=lambda x: x.get("bitis", "")):
                bitis = s.get("bitis", "9999-12-31")
                gecerli = bitis >= bugun
                try:
                    kalan_gun = (datetime.strptime(bitis, "%Y-%m-%d").date() - datetime.now().date()).days
                except Exception:
                    kalan_gun = 999

                renk = "#06d6a0" if kalan_gun > 90 else ("#ffd166" if kalan_gun > 30 else "#e94560")
                durum = "GECERLI" if gecerli else "SURESI DOLDU"

                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{s.get('ad','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{s.get('kurum','')}</span>
                    </div>
                    <div>
                        <span style="color:{renk};font-weight:700;">{bitis}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.72rem;margin-left:6px;">{durum}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            suresi_dolan = [s for s in sertifikalar if s.get("bitis", "9999") < bugun]
            yaklasan = [s for s in sertifikalar if bugun <= s.get("bitis", "") <= str(datetime.now().date() + timedelta(days=60))]
            if suresi_dolan:
                st.error(f"🚨 {len(suresi_dolan)} sertifikanin suresi doldu!")
            if yaklasan:
                st.warning(f"⏰ {len(yaklasan)} sertifika 60 gun icinde dolacak.")

    # ── Denetim Hazırlığı ──
    with sub[4]:
        _styled_section("📝 Denetim Hazirligi & Rapor Uretici", "#06d6a0")

        _styled_info_banner("Yaklasan denetimlere hazirlik durumunu gorun ve otomatik rapor uretin.")

        hazirlık_path = _get_data_path(store, "denetim_hazirlik.json")
        hazirliklar = _load_json(hazirlık_path)

        with st.form("hazirlik_form"):
            hc1, hc2 = st.columns(2)
            with hc1:
                h_denetim = st.text_input("Denetim Adi", key="hzr_ad")
                h_tarih = st.date_input("Denetim Tarihi", value=datetime.now().date() + timedelta(days=30), key="hzr_tarih")
            with hc2:
                h_standart = st.selectbox("Standart", ["ISO 9001", "MEB Denetim", "Is Guvenligi", "Yangin", "Genel"], key="hzr_std")
                h_denetci = st.text_input("Denetci / Kurum", key="hzr_denetci")

            if st.form_submit_button("📝 Hazirlik Baslat", use_container_width=True):
                if h_denetim:
                    # İlgili checklist'leri bul
                    ilgili = [c for c in checklists if c.get("standart") == h_standart]
                    tamam = len([c for c in ilgili if c.get("durum") == "tamamlandi"])
                    hazirlik_oran = int(tamam / max(1, len(ilgili)) * 100)

                    hazirliklar.append({
                        "id": f"hzr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "denetim": h_denetim,
                        "tarih": str(h_tarih),
                        "standart": h_standart,
                        "denetci": h_denetci,
                        "checklist_toplam": len(ilgili),
                        "checklist_tamam": tamam,
                        "hazirlik_oran": hazirlik_oran,
                        "olusturma": datetime.now().isoformat(),
                    })
                    _save_json(hazirlık_path, hazirliklar)
                    st.success(f"Hazirlik basladi! Mevcut uyum: %{hazirlik_oran}")
                    st.rerun()

        if hazirliklar:
            for h in reversed(hazirliklar[-6:]):
                oran = h.get("hazirlik_oran", 0)
                renk = "#06d6a0" if oran >= 80 else ("#ffd166" if oran >= 50 else "#e94560")
                try:
                    kalan = (datetime.strptime(h.get("tarih", "2099-01-01"), "%Y-%m-%d").date() - datetime.now().date()).days
                except Exception:
                    kalan = 999

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <div>
                            <strong style="color:#e0e0e0;">{h.get('denetim','')}</strong>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">{h.get('standart','')} | {h.get('denetci','')}</span>
                        </div>
                        <span style="color:{renk};font-weight:700;">%{oran} hazir | {kalan} gun</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                        <div style="width:{oran}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Uyumluluk Skoru ──
    with sub[5]:
        _styled_section("📈 Genel Uyumluluk Olgunluk Skoru", "#8338ec")

        ck_skor = uyum_oran
        capa_acik = len([c for c in capalar if c.get("durum") == "acik"])
        capa_skor = max(0, 100 - capa_acik * 15)
        sert_gecerli = len([s for s in sertifikalar if s.get("bitis", "") >= str(datetime.now().date())])
        sert_skor = int(sert_gecerli / max(1, len(sertifikalar)) * 100) if sertifikalar else 50
        genel = int((ck_skor + capa_skor + sert_skor) / 3)
        renk = "#06d6a0" if genel >= 70 else ("#ffd166" if genel >= 40 else "#e94560")
        derece = "A+" if genel >= 90 else ("A" if genel >= 80 else ("B" if genel >= 60 else ("C" if genel >= 40 else "D")))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:0.9rem;color:#888;">Uyumluluk Olgunluk Derecesi</div>
            <div style="font-size:4rem;font-weight:900;color:{renk};">{derece}</div>
            <div style="font-size:1.4rem;color:{renk};">{genel}/100</div>
        </div>""", unsafe_allow_html=True)

        bilesenler = [("Checklist Uyumu", ck_skor, "#00b4d8"), ("CAPA Durumu", capa_skor, "#06d6a0"), ("Sertifika Gecerliligi", sert_skor, "#ffd166")]
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
#  2. ÇOK KAMPÜSLÜ OPERASYON & BENCHMARK MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_benchmark_merkezi(store):
    _styled_header("Cok Kampuslu Operasyon & Benchmark Merkezi", "🌍")

    kampus_path = _get_data_path(store, "kampus_verileri.json")
    kampusler = _load_json(kampus_path)

    uygulama_path = _get_data_path(store, "en_iyi_uygulamalar.json")
    uygulamalar = _load_json(uygulama_path)

    _styled_stat_row([
        ("Kampus Sayisi", len(kampusler)),
        ("En Iyi Uygulama", len(uygulamalar)),
    ])

    sub = st.tabs(["🏫 Kampus Yonetimi", "📊 Performans Karsilastirma", "🏆 Sampiyon Kampus", "🔄 Uygulama Paylasimi", "💰 Maliyet Benchmark", "📈 Merkezi Dashboard"])

    # ── Kampüs Yönetimi ──
    with sub[0]:
        _styled_section("🏫 Kampus / Sube Tanimlama", "#0f3460")

        with st.form("kampus_form"):
            kc1, kc2 = st.columns(2)
            with kc1:
                k_ad = st.text_input("Kampus Adi", key="kmp_ad")
                k_adres = st.text_input("Adres / Sehir", key="kmp_adres")
            with kc2:
                k_teknisyen = st.number_input("Teknisyen Sayisi", min_value=0, value=5, key="kmp_tek")
                k_ogrenci = st.number_input("Ogrenci Sayisi", min_value=0, value=500, key="kmp_ogr")
            kc3, kc4 = st.columns(2)
            with kc3:
                k_aylik_talep = st.number_input("Aylik Ort. Talep", min_value=0, value=50, key="kmp_talep")
            with kc4:
                k_sla_uyum = st.number_input("SLA Uyum (%)", min_value=0, max_value=100, value=85, key="kmp_sla")

            if st.form_submit_button("🏫 Kampus Ekle", use_container_width=True):
                if k_ad:
                    kampusler.append({
                        "id": f"kmp_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": k_ad,
                        "adres": k_adres,
                        "teknisyen": k_teknisyen,
                        "ogrenci": k_ogrenci,
                        "aylik_talep": k_aylik_talep,
                        "sla_uyum": k_sla_uyum,
                        "memnuniyet": 0,
                        "maliyet": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(kampus_path, kampusler)
                    st.success(f"{k_ad} eklendi!")
                    st.rerun()

        if kampusler:
            for k in kampusler:
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;font-size:1.05rem;">🏫 {k.get('ad','')}</strong>
                        <div style="color:#888;font-size:0.78rem;">{k.get('adres','')} | {k.get('ogrenci',0)} ogrenci | {k.get('teknisyen',0)} teknisyen</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:#00b4d8;font-weight:700;">SLA %{k.get('sla_uyum',0)}</div>
                        <div style="color:#888;font-size:0.75rem;">{k.get('aylik_talep',0)} talep/ay</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Performans Karşılaştırma ──
    with sub[1]:
        _styled_section("📊 Kampus Performans Karsilastirmasi", "#8338ec")

        if len(kampusler) >= 2:
            metrikler = ["SLA Uyum", "Ogrenci Basi Talep", "Teknisyen Verimlilik"]
            for metrik in metrikler:
                st.markdown(f"**{metrik}**")
                for k in sorted(kampusler, key=lambda x: -x.get("sla_uyum", 0)):
                    if metrik == "SLA Uyum":
                        deger = k.get("sla_uyum", 0)
                        birim = "%"
                    elif metrik == "Ogrenci Basi Talep":
                        deger = round(k.get("aylik_talep", 0) / max(1, k.get("ogrenci", 1)) * 100, 1)
                        birim = "/100 ogr"
                    else:
                        deger = round(k.get("aylik_talep", 0) / max(1, k.get("teknisyen", 1)), 1)
                        birim = " talep/tek"

                    renk = "#06d6a0" if deger >= 80 or (metrik != "SLA Uyum" and deger <= 15) else "#ffd166"
                    bar_w = min(100, int(deger))
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                        <span style="width:140px;color:#e0e0e0;font-size:0.85rem;">{k.get('ad','')}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                        <span style="width:80px;text-align:right;color:{renk};font-weight:700;">{deger}{birim}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("")
        else:
            _styled_info_banner("Karsilastirma icin en az 2 kampus gerekiyor.")

    # ── Şampiyon Kampüs ──
    with sub[2]:
        _styled_section("🏆 Sampiyon Kampus Siralaması", "#ffd166")

        if kampusler:
            # Genel skor hesapla
            for k in kampusler:
                sla = k.get("sla_uyum", 0)
                verimlilik = 100 - min(100, int(k.get("aylik_talep", 0) / max(1, k.get("teknisyen", 1)) * 2))
                k["_genel_skor"] = int((sla * 0.5 + verimlilik * 0.3 + 50 * 0.2))

            siralama = sorted(kampusler, key=lambda x: -x.get("_genel_skor", 0))
            madalyalar = ["🥇", "🥈", "🥉"]

            for i, k in enumerate(siralama):
                madalya = madalyalar[i] if i < 3 else f"#{i+1}"
                renk = "#ffd166" if i == 0 else ("#c0c0c0" if i == 1 else ("#cd7f32" if i == 2 else "#888"))
                skor = k.get("_genel_skor", 0)

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:{'18px' if i < 3 else '12px'} 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span style="font-size:{'2rem' if i < 3 else '1.2rem'};">{madalya}</span>
                            <div>
                                <strong style="color:#e0e0e0;font-size:{'1.1rem' if i < 3 else '1rem'};">{k.get('ad','')}</strong>
                                <div style="color:#888;font-size:0.78rem;">{k.get('adres','')}</div>
                            </div>
                        </div>
                        <span style="color:{renk};font-weight:800;font-size:{'1.4rem' if i < 3 else '1rem'};">{skor} puan</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Uygulama Paylaşımı ──
    with sub[3]:
        _styled_section("🔄 En Iyi Uygulama Paylasimi", "#06d6a0")

        with st.form("uygulama_form"):
            uc1, uc2 = st.columns(2)
            with uc1:
                u_baslik = st.text_input("Uygulama Basligi", key="uyg_baslik")
                u_kampus = st.text_input("Kaynak Kampus", key="uyg_kampus")
            with uc2:
                u_kategori = st.selectbox("Kategori", ["Verimlilik", "Maliyet Tasarrufu", "Memnuniyet", "Guvenlik", "Surec", "Diger"], key="uyg_kat")
                u_etki = st.selectbox("Etki Seviyesi", ["Dusuk", "Orta", "Yuksek", "Cok Yuksek"], key="uyg_etki")
            u_aciklama = st.text_area("Aciklama", height=68, key="uyg_acik")

            if st.form_submit_button("🔄 Uygulama Paylas", use_container_width=True):
                if u_baslik:
                    uygulamalar.append({
                        "id": f"uyg_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": u_baslik,
                        "kampus": u_kampus,
                        "kategori": u_kategori,
                        "etki": u_etki,
                        "aciklama": u_aciklama,
                        "begeni": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(uygulama_path, uygulamalar)
                    st.success("Uygulama paylasildi!")
                    st.rerun()

        if uygulamalar:
            for idx, u in enumerate(reversed(uygulamalar[-10:])):
                etki_renk = {"Dusuk": "#888", "Orta": "#ffd166", "Yuksek": "#06d6a0", "Cok Yuksek": "#e94560"}.get(u.get("etki", ""), "#888")
                with st.expander(f"💡 {u.get('baslik','')} — {u.get('kampus','')}"):
                    st.markdown(f"**Kategori:** {u.get('kategori','')} | **Etki:** <span style='color:{etki_renk}'>{u.get('etki','')}</span>", unsafe_allow_html=True)
                    st.info(u.get("aciklama", ""))
                    if st.button(f"👍 Begeni ({u.get('begeni',0)})", key=f"uyg_beg_{idx}"):
                        u["begeni"] = u.get("begeni", 0) + 1
                        _save_json(uygulama_path, uygulamalar)
                        st.rerun()

    # ── Maliyet Benchmark ──
    with sub[4]:
        _styled_section("💰 Kampus Bazli Maliyet Benchmark", "#e94560")

        if kampusler:
            st.markdown("**Maliyet Verisi Guncelle**")
            for idx, k in enumerate(kampusler):
                yeni_mal = st.number_input(f"{k.get('ad','')} Aylik Maliyet (TL)", min_value=0.0, value=float(k.get("maliyet", 0)), step=1000.0, key=f"kmp_mal_{idx}")
                if yeni_mal != k.get("maliyet", 0):
                    k["maliyet"] = yeni_mal

            if st.button("💾 Maliyetleri Kaydet"):
                _save_json(kampus_path, kampusler)
                st.success("Maliyet verileri guncellendi!")
                st.rerun()

            maliyet_olan = [k for k in kampusler if k.get("maliyet", 0) > 0]
            if maliyet_olan:
                _styled_section("Ogrenci Basi Maliyet Karsilastirmasi", "#ffd166")
                for k in sorted(maliyet_olan, key=lambda x: x.get("maliyet", 0) / max(1, x.get("ogrenci", 1))):
                    ob_maliyet = k.get("maliyet", 0) / max(1, k.get("ogrenci", 1))
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                        <span style="color:#e0e0e0;">{k.get('ad','')}</span>
                        <span style="color:#ffd166;font-weight:700;">TL{ob_maliyet:,.0f}/ogrenci</span>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Maliyet benchmark icin kampus ekleyin.")

    # ── Merkezi Dashboard ──
    with sub[5]:
        _styled_section("📈 Merkezi Operasyon Dashboard", "#00b4d8")

        if kampusler:
            toplam_ogrenci = sum(k.get("ogrenci", 0) for k in kampusler)
            toplam_teknisyen = sum(k.get("teknisyen", 0) for k in kampusler)
            toplam_talep = sum(k.get("aylik_talep", 0) for k in kampusler)
            ort_sla = sum(k.get("sla_uyum", 0) for k in kampusler) / len(kampusler)

            _styled_stat_row([
                ("Toplam Ogrenci", f"{toplam_ogrenci:,}"),
                ("Toplam Teknisyen", toplam_teknisyen),
                ("Aylik Toplam Talep", toplam_talep),
                ("Ort. SLA Uyum", f"%{ort_sla:.0f}"),
            ])

            renk = "#06d6a0" if ort_sla >= 80 else ("#ffd166" if ort_sla >= 60 else "#e94560")
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Kurumsal Destek Operasyon Skoru</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">{ort_sla:.0f}/100</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Merkezi dashboard icin kampus verisi ekleyin.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. AI OPERASYON ASİSTANI & OTONOM KARAR MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_ai_operasyon(store):
    _styled_header("AI Operasyon Asistani & Otonom Karar Motoru", "🤖")

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    try:
        bakimlar = store.load_list("bakim_kayitlari") or []
    except Exception:
        bakimlar = []

    brief_path = _get_data_path(store, "ai_briefler.json")
    briefler = _load_json(brief_path)

    _styled_stat_row([
        ("Analiz Edilen Talep", len(tickets)),
        ("Bakim Kaydi", len(bakimlar)),
        ("Uretilen Brief", len(briefler)),
    ])

    sub = st.tabs(["💬 AI Soru-Cevap", "📋 Gunluk Brief", "🔍 Anomali Tespiti", "📊 Akilli Onceliklendirme", "🎯 Ne Yapmaliyim?", "📈 Operasyon Ozeti"])

    # ── AI Soru-Cevap ──
    with sub[0]:
        _styled_section("💬 Dogal Dil ile Soru Sorun", "#8338ec")

        _styled_info_banner("Destek operasyonlari hakkinda dogal dilde soru sorun, AI verileri analiz ederek yanit verir.")

        soru = st.text_input("Sorunuzu yazin...", placeholder="Bu ay en cok nerede ariza oldu?", key="ai_soru_input")

        if soru:
            soru_lower = soru.lower()
            yanit = None

            # Basit keyword eşleştirme
            if any(k in soru_lower for k in ["en cok", "en fazla", "nerede", "lokasyon", "ariza"]):
                lok_sayim = Counter(_get_attr(t, "lokasyon") or _get_attr(t, "konum") or _get_attr(t, "hizmet_alani") or "Belirtilmemis" for t in tickets)
                if lok_sayim:
                    en_cok = lok_sayim.most_common(3)
                    yanit = f"En cok ariza/talep olan yerler:\n"
                    for lok, sayi in en_cok:
                        yanit += f"• **{lok}**: {sayi} talep\n"

            elif any(k in soru_lower for k in ["kac", "sayisi", "toplam", "acik"]):
                acik = len([t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde")])
                kapali = len(tickets) - acik
                yanit = f"Toplam **{len(tickets)}** talep kaydi var.\n• Acik: **{acik}**\n• Kapali: **{kapali}**"

            elif any(k in soru_lower for k in ["sla", "uyum", "geciken"]):
                kapali = len([t for t in tickets if _get_attr(t, "durum") in ("kapali", "cozuldu", "closed", "resolved")])
                uyum = int(kapali / max(1, len(tickets)) * 100)
                yanit = f"SLA uyum orani: **%{uyum}**\n• Cozulen: {kapali}\n• Toplam: {len(tickets)}"

            elif any(k in soru_lower for k in ["oncelik", "acil", "kritik"]):
                oncelik_sayim = Counter(_get_attr(t, "oncelik") or "normal" for t in tickets)
                yanit = "Oncelik dagilimi:\n"
                for onc, sayi in oncelik_sayim.most_common():
                    yanit += f"• **{onc}**: {sayi}\n"

            elif any(k in soru_lower for k in ["trend", "artis", "azalis"]):
                yanit = f"Son veriye gore toplam {len(tickets)} talep mevcut. Detayli trend icin SLA Cockpit sekmesine bakin."

            if yanit:
                st.markdown(f"""
                <div style="background:#8338ec12;border-left:4px solid #8338ec;padding:14px 18px;border-radius:0 10px 10px 0;margin-top:10px;">
                    <div style="color:#8338ec;font-weight:700;margin-bottom:6px;">🤖 AI Yanit:</div>
                    <div style="color:#e0e0e0;font-size:0.92rem;">{yanit}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("Bu soru icin daha fazla veri gerekiyor. Daha spesifik bir soru deneyin (ornek: 'Kac acik talep var?', 'En cok ariza nerede?')")

        # Hazır sorular
        _styled_section("Sik Sorulan Sorular", "#00b4d8")
        hazir_sorular = [
            "Bu ay kac talep acildi?",
            "En cok ariza nerede oluyor?",
            "SLA uyum orani nedir?",
            "Acil talepler kac tane?",
            "Oncelik dagilimi nasil?",
        ]
        for hs in hazir_sorular:
            st.caption(f"💡 _{hs}_")

    # ── Günlük Brief ──
    with sub[1]:
        _styled_section("📋 Otomatik Gunluk / Haftalik Brief", "#06d6a0")

        if st.button("📋 Gunluk Brief Uret", use_container_width=True):
            bugun = str(datetime.now().date())
            bugun_acilan = [t for t in tickets if str(_get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or "")[:10] == bugun]
            acik = [t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde", "atandi")]

            brief = {
                "id": f"brf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "tarih": bugun,
                "bugun_acilan": len(bugun_acilan),
                "toplam_acik": len(acik),
                "toplam_talep": len(tickets),
                "olusturma": datetime.now().isoformat(),
            }
            briefler.append(brief)
            _save_json(brief_path, briefler)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#06d6a015,#16213e);border:1px solid #06d6a030;border-radius:14px;padding:18px;">
                <h3 style="color:#06d6a0;margin:0 0 12px 0;">📋 Gunluk Brief — {bugun}</h3>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <div style="background:#0f346030;padding:10px;border-radius:8px;">
                        <div style="color:#888;font-size:0.78rem;">Bugun Acilan</div>
                        <div style="color:#00b4d8;font-size:1.3rem;font-weight:700;">{len(bugun_acilan)}</div>
                    </div>
                    <div style="background:#0f346030;padding:10px;border-radius:8px;">
                        <div style="color:#888;font-size:0.78rem;">Toplam Acik</div>
                        <div style="color:#ffd166;font-size:1.3rem;font-weight:700;">{len(acik)}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        if briefler:
            _styled_section("Gecmis Briefler", "#888")
            for b in reversed(briefler[-5:]):
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                    <span style="color:#888;">📋 {b.get('tarih','')}</span>
                    <span style="color:#e0e0e0;">Acilan: {b.get('bugun_acilan',0)} | Acik: {b.get('toplam_acik',0)}</span>
                </div>""", unsafe_allow_html=True)

    # ── Anomali Tespiti ──
    with sub[2]:
        _styled_section("🔍 AI Anomali & Sapma Tespiti", "#e94560")

        _styled_info_banner("AI, normal operasyon kaliplarinin disina cikan durumlar tespit eder.")

        anomaliler = []

        if tickets:
            # Günlük talep sayısı anomalisi
            gun_sayim = Counter(str(_get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or "")[:10] for t in tickets)
            if gun_sayim:
                degerler = list(gun_sayim.values())
                ort = sum(degerler) / len(degerler)
                std = max(1, (sum((d - ort) ** 2 for d in degerler) / len(degerler)) ** 0.5)

                for gun, sayi in gun_sayim.items():
                    if gun and sayi > ort + 2 * std:
                        anomaliler.append(("Talep Spike", f"{gun} tarihinde {sayi} talep acildi (ort: {ort:.0f})", "#e94560"))

            # Acil talep yoğunluğu
            acil_talepler = [t for t in tickets if (_get_attr(t, "oncelik") or "") in ("acil", "critical")]
            if len(acil_talepler) > len(tickets) * 0.2:
                anomaliler.append(("Yuksek Acil Orani", f"Acil talep orani %{int(len(acil_talepler)/max(1,len(tickets))*100)} — normalin uzerinde", "#ff6b6b"))

        if anomaliler:
            for baslik, aciklama, renk in anomaliler:
                st.markdown(f"""
                <div style="background:{renk}12;border-left:4px solid {renk};padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:8px;">
                    <strong style="color:{renk};">🔍 {baslik}</strong>
                    <div style="color:#aaa;font-size:0.85rem;margin-top:3px;">{aciklama}</div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Anomali tespit edilmedi. Operasyon normal kaliplar icinde. ✅")

    # ── Akıllı Önceliklendirme ──
    with sub[3]:
        _styled_section("📊 AI Akilli Talep Onceliklendirme", "#ffd166")

        acik_talepler = [t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde", "atandi")]

        if acik_talepler:
            _styled_info_banner("AI, acik talepleri etki, aciliyet ve beklesuresi bazinda yeniden onceliklendirir.")

            skorlu = []
            bugun_dt = datetime.now()
            for t in acik_talepler:
                baslik = _get_attr(t, "baslik") or _get_attr(t, "konu") or _get_attr(t, "title") or "?"
                oncelik = _get_attr(t, "oncelik") or "normal"
                olusturma = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih")

                oncelik_puan = {"acil": 40, "yuksek": 30, "normal": 15, "dusuk": 5}.get(oncelik, 15)
                bekleme_puan = 0
                if olusturma:
                    try:
                        olusum_dt = datetime.fromisoformat(str(olusturma)[:19]) if not isinstance(olusturma, datetime) else olusturma
                        bekleme_saat = (bugun_dt - olusum_dt).total_seconds() / 3600
                        bekleme_puan = min(40, int(bekleme_saat / 4))
                    except Exception:
                        bekleme_saat = 0

                ai_skor = min(100, oncelik_puan + bekleme_puan + 10)
                skorlu.append({"baslik": baslik, "oncelik": oncelik, "ai_skor": ai_skor})

            skorlu.sort(key=lambda x: -x["ai_skor"])

            for s in skorlu[:12]:
                skor = s["ai_skor"]
                renk = "#e94560" if skor >= 70 else ("#ffd166" if skor >= 40 else "#06d6a0")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:50px;text-align:center;color:{renk};font-weight:800;font-size:1.1rem;">{skor}</span>
                    <div style="flex:1;background:#16213e;border-radius:8px;padding:8px 12px;border-left:3px solid {renk};">
                        <strong style="color:#e0e0e0;font-size:0.9rem;">{s['baslik'][:40]}</strong>
                        <span style="color:#888;font-size:0.75rem;margin-left:8px;">{s['oncelik']}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Onceliklendirme icin acik talep bulunmuyor. ✅")

    # ── Ne Yapmalıyım? ──
    with sub[4]:
        _styled_section("🎯 Su Anda Ne Yapmaliyim? — AI Karar Onerisi", "#06d6a0")

        acik = [t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde")]
        acil = [t for t in acik if (_get_attr(t, "oncelik") or "") in ("acil", "critical")]

        oneriler = []

        if acil:
            oneriler.append(("1. ONCELIK: Acil Talepleri Coz", f"{len(acil)} acil talep bekliyor. Hemen mudahale edin.", "#e94560", "🚨"))

        if len(acik) > 10:
            oneriler.append(("2. Talep Birikimine Mudahale", f"{len(acik)} acik talep birikti. Ek kaynak veya dis destek degerlendir.", "#ffd166", "📊"))

        gorev_path = _get_data_path(store, "saha_gorevler.json")
        gorevler = _load_json(gorev_path)
        bugun_gorev = [g for g in gorevler if g.get("planlanan_tarih") == str(datetime.now().date()) and g.get("durum") != "tamamlandi"]
        if bugun_gorev:
            oneriler.append(("3. Gunluk Gorevleri Takip Et", f"Bugun {len(bugun_gorev)} planli gorev var.", "#00b4d8", "📋"))

        if not oneriler:
            oneriler = [
                ("Onleyici Bakim Zamani", "Acil is yok — onleyici bakim planlarini ilerletin.", "#06d6a0", "🔧"),
                ("Bilgi Bankasini Zenginlestir", "Boş zamanda cozum DNA kartlari olusturun.", "#8338ec", "🧬"),
                ("Ekip Egitimi", "Yeni prosedur ve arac egitimleri planlayin.", "#ffd166", "📚"),
            ]

        for baslik, aciklama, renk, ikon in oneriler:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{renk}10,#16213e);border:1px solid {renk}30;border-radius:14px;padding:18px;margin-bottom:12px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <span style="font-size:2rem;">{ikon}</span>
                    <div>
                        <h4 style="color:{renk};margin:0 0 4px 0;">{baslik}</h4>
                        <p style="color:#aaa;font-size:0.9rem;margin:0;">{aciklama}</p>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Operasyon Özeti ──
    with sub[5]:
        _styled_section("📈 Kapsamli Operasyon Ozet Raporu", "#ffd166")

        toplam = len(tickets)
        kapali = len([t for t in tickets if _get_attr(t, "durum") in ("kapali", "cozuldu", "closed", "resolved")])
        acik_sayi = toplam - kapali
        cozum_oran = int(kapali / max(1, toplam) * 100)

        # Genel skor
        genel_skor = cozum_oran
        renk = "#06d6a0" if genel_skor >= 70 else ("#ffd166" if genel_skor >= 40 else "#e94560")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e,#1a1a2e);border-radius:16px;padding:28px;text-align:center;margin-bottom:16px;">
            <div style="font-size:1rem;color:#888;">Genel Operasyon Performansi</div>
            <div style="font-size:4rem;font-weight:900;color:{renk};">{genel_skor}/100</div>
            <div style="display:flex;justify-content:center;gap:40px;margin-top:12px;">
                <div><span style="color:#06d6a0;font-weight:700;font-size:1.4rem;">{kapali}</span><br><span style="color:#888;font-size:0.78rem;">Cozulen</span></div>
                <div><span style="color:#e94560;font-weight:700;font-size:1.4rem;">{acik_sayi}</span><br><span style="color:#888;font-size:0.78rem;">Acik</span></div>
                <div><span style="color:#00b4d8;font-weight:700;font-size:1.4rem;">{toplam}</span><br><span style="color:#888;font-size:0.78rem;">Toplam</span></div>
                <div><span style="color:#ffd166;font-weight:700;font-size:1.4rem;">{len(bakimlar)}</span><br><span style="color:#888;font-size:0.78rem;">Bakim</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Hızlı metrikler
        metrikler = [
            ("Cozum Orani", f"%{cozum_oran}", "#06d6a0"),
            ("Acik Talep", str(acik_sayi), "#e94560"),
            ("Toplam Bakim", str(len(bakimlar)), "#00b4d8"),
            ("Brief Sayisi", str(len(briefler)), "#8338ec"),
        ]
        for baslik, deger, renk in metrikler:
            st.markdown(f"""
            <div style="background:#16213e;border-radius:8px;padding:10px 16px;margin-bottom:5px;display:flex;justify-content:space-between;">
                <span style="color:#e0e0e0;">{baslik}</span>
                <span style="color:{renk};font-weight:700;">{deger}</span>
            </div>""", unsafe_allow_html=True)
