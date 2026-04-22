"""
Sivil Savunma, ISG ve Okul Güvenliği - Yeni Özellikler
1. Acil Durum Komuta & Tahliye Merkezi
2. Yangın & Doğal Afet Risk Haritası
3. Güvenlik Kamera & Giriş-Çıkış Kontrol Paneli
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter

from utils.ui_common import (
    styled_header as _ui_styled_header,
    styled_section,
    styled_stat_row as _ui_styled_stat_row,
    styled_info_banner as _ui_styled_info_banner,
)

# Palette renklerini kullanarak shared helper'lara kopruleme
_STAT_COLORS = ["#e94560", "#0f3460", "#00b4d8", "#06d6a0", "#ffd166", "#8338ec", "#ff6b6b"]
_STAT_ICONS = ["📋", "📊", "🔍", "✅", "⚠️", "📈", "📝"]


def _styled_header(title: str, icon: str = "🗺️"):
    """Shared styled_header'a koprule."""
    _ui_styled_header(title, icon=icon)


def _styled_stat_row(stats: list):
    """2-tuple (label, value) listesini shared 4-tuple formatina donusturur."""
    converted = []
    for i, item in enumerate(stats):
        label, value = item[0], item[1]
        color = _STAT_COLORS[i % len(_STAT_COLORS)]
        icon = _STAT_ICONS[i % len(_STAT_ICONS)]
        converted.append((label, str(value), color, icon))
    _ui_styled_stat_row(converted)


def _styled_info_banner(text: str, color: str = "#00b4d8"):
    """Shared styled_info_banner'a koprule."""
    _ui_styled_info_banner(text, "info")


def _get_data_path(store, filename):
    if hasattr(store, 'base_path'):
        return os.path.join(store.base_path, filename)
    return os.path.join("data", "ssg", filename)

def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. ACİL DURUM KOMUTA & TAHLİYE MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_acil_durum_merkezi(store):
    _styled_header("Acil Durum Komuta & Tahliye Merkezi", "🗺️")

    tahliye_path = _get_data_path(store, "tahliye_planlari.json")
    tahliye_planlari = _load_json(tahliye_path)

    toplanma_path = _get_data_path(store, "toplanma_noktalari.json")
    toplanma_noktalari = _load_json(toplanma_path)

    iletisim_path = _get_data_path(store, "acil_iletisim_zinciri.json")
    iletisim_zinciri = _load_json(iletisim_path)

    tatbikat_path = _get_data_path(store, "tahliye_tatbikatlari.json")
    tatbikatlar = _load_json(tatbikat_path)

    _styled_stat_row([
        ("Tahliye Plani", len(tahliye_planlari)),
        ("Toplanma Noktasi", len(toplanma_noktalari)),
        ("Iletisim Zinciri", len(iletisim_zinciri)),
        ("Tatbikat Sayisi", len(tatbikatlar)),
    ])

    sub = st.tabs(["🏃 Tahliye Plani", "📍 Toplanma Noktalari", "👥 Kisi Sayim", "📞 Iletisim Zinciri", "⏱️ Tatbikat Kronometresi", "📊 Tahliye Analizi"])

    # ── Tahliye Planı ──
    with sub[0]:
        styled_section("🏃 Bina Bazli Tahliye Plani", "#e94560")

        with st.form("tahliye_form"):
            tc1, tc2 = st.columns(2)
            with tc1:
                t_bina = st.text_input("Bina Adi", key="thl_bina")
                t_kat = st.text_input("Kat", key="thl_kat")
                t_cikis = st.text_input("Acil Cikis Yolu", key="thl_cikis")
            with tc2:
                t_kapasite = st.number_input("Kat Kapasitesi (kisi)", min_value=0, value=100, key="thl_kap")
                t_toplanma = st.text_input("Atanan Toplanma Noktasi", key="thl_toplanma")
                t_sure = st.number_input("Hedef Tahliye Suresi (sn)", min_value=30, value=180, step=30, key="thl_sure")
            t_sorumlu = st.text_input("Kat Tahliye Sorumlusu", key="thl_sorumlu")

            if st.form_submit_button("🏃 Tahliye Plani Ekle", use_container_width=True):
                if t_bina and t_kat:
                    tahliye_planlari.append({
                        "id": f"thl_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "bina": t_bina,
                        "kat": t_kat,
                        "cikis_yolu": t_cikis,
                        "kapasite": t_kapasite,
                        "toplanma": t_toplanma,
                        "hedef_sure": t_sure,
                        "sorumlu": t_sorumlu,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(tahliye_path, tahliye_planlari)
                    st.success(f"{t_bina}/{t_kat} tahliye plani eklendi!")
                    st.rerun()

        if tahliye_planlari:
            styled_section("Tanimli Tahliye Planlari", "#06d6a0")
            bina_grup = {}
            for t in tahliye_planlari:
                b = t.get("bina", "?")
                if b not in bina_grup:
                    bina_grup[b] = []
                bina_grup[b].append(t)

            for bina, planlar in bina_grup.items():
                toplam_kap = sum(p.get("kapasite", 0) for p in planlar)
                with st.expander(f"🏢 {bina} ({len(planlar)} kat, {toplam_kap} kisi kapasitesi)"):
                    for p in planlar:
                        pid = p.get("id", "")
                        tc1, tc2 = st.columns([5, 1])
                        with tc1:
                            st.markdown(f"""
                            <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:4px;display:flex;justify-content:space-between;">
                                <div>
                                    <strong style="color:#e0e0e0;">Kat: {p.get('kat','')}</strong>
                                    <span style="color:#888;font-size:0.78rem;margin-left:8px;">Cikis: {p.get('cikis_yolu','')}</span>
                                </div>
                                <div>
                                    <span style="color:#06d6a0;">{p.get('kapasite','')} kisi</span>
                                    <span style="color:#ffd166;margin-left:8px;">Hedef: {p.get('hedef_sure','')}sn</span>
                                    <span style="color:#888;margin-left:8px;">Sorumlu: {p.get('sorumlu','—')}</span>
                                </div>
                            </div>""", unsafe_allow_html=True)
                        with tc2:
                            if st.button("🗑️", key=f"del_thl_{pid}", help="Tahliye planini sil"):
                                tahliye_planlari[:] = [x for x in tahliye_planlari if x.get("id") != pid]
                                _save_json(tahliye_path, tahliye_planlari)
                                st.rerun()

    # ── Toplanma Noktaları ──
    with sub[1]:
        styled_section("📍 Toplanma Noktasi Tanimlama & Takip", "#06d6a0")

        with st.form("toplanma_form"):
            nc1, nc2 = st.columns(2)
            with nc1:
                n_ad = st.text_input("Toplanma Noktasi Adi", key="tpn_ad")
                n_konum = st.text_input("Konum Tanimi", key="tpn_konum")
            with nc2:
                n_kapasite = st.number_input("Kapasite (kisi)", min_value=10, value=200, key="tpn_kap")
                n_binalar = st.text_input("Atanan Binalar (virgul ile)", key="tpn_bina")

            if st.form_submit_button("📍 Nokta Ekle", use_container_width=True):
                if n_ad:
                    toplanma_noktalari.append({
                        "id": f"tpn_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": n_ad,
                        "konum": n_konum,
                        "kapasite": n_kapasite,
                        "binalar": n_binalar,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(toplanma_path, toplanma_noktalari)
                    st.success(f"Toplanma noktasi '{n_ad}' eklendi!")
                    st.rerun()

        if toplanma_noktalari:
            for n in toplanma_noktalari:
                nid = n.get("id", "")
                nc1, nc2 = st.columns([6, 1])
                with nc1:
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#06d6a0;font-size:1.05rem;">📍 {n.get('ad','')}</strong>
                            <div style="color:#888;font-size:0.78rem;">{n.get('konum','')} | Binalar: {n.get('binalar','')}</div>
                        </div>
                        <div style="background:#06d6a020;color:#06d6a0;padding:6px 14px;border-radius:10px;font-weight:700;">
                            {n.get('kapasite','')} kisi
                        </div>
                    </div>""", unsafe_allow_html=True)
                with nc2:
                    if st.button("🗑️", key=f"del_tpn_{nid}", help="Toplanma noktasini sil"):
                        toplanma_noktalari[:] = [x for x in toplanma_noktalari if x.get("id") != nid]
                        _save_json(toplanma_path, toplanma_noktalari)
                        st.rerun()

    # ── Kişi Sayım ──
    with sub[2]:
        styled_section("👥 Acil Durum Kisi Sayim Sistemi", "#00b4d8")

        _styled_info_banner("Tahliye sonrasi toplanma noktalarinda kisi sayimi yaparak eksik/fazla tespiti.")

        sayim_path = _get_data_path(store, "kisi_sayimlari.json")
        sayimlar = _load_json(sayim_path)

        with st.form("sayim_form"):
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                s_nokta = st.text_input("Toplanma Noktasi", key="sy_nokta")
            with sc2:
                s_beklenen = st.number_input("Beklenen Kisi", min_value=0, value=100, key="sy_beklenen")
            with sc3:
                s_mevcut = st.number_input("Mevcut Kisi", min_value=0, value=95, key="sy_mevcut")
            s_tarih = st.date_input("Tarih", value=datetime.now().date(), key="sy_tarih")

            if st.form_submit_button("👥 Sayim Kaydet", use_container_width=True):
                if s_nokta:
                    eksik = s_beklenen - s_mevcut
                    sayimlar.append({
                        "id": f"sy_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "nokta": s_nokta,
                        "beklenen": s_beklenen,
                        "mevcut": s_mevcut,
                        "eksik": max(0, eksik),
                        "tarih": str(s_tarih),
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(sayim_path, sayimlar)
                    if eksik > 0:
                        st.error(f"⚠️ {eksik} kisi eksik! Arama baslatin.")
                    else:
                        st.success("Tam sayim — tum kisiler toplanma noktasinda. ✅")
                    st.rerun()

        if sayimlar:
            styled_section("Son Sayim Kayitlari", "#ffd166")
            for s in reversed(sayimlar[-10:]):
                eksik = s.get("eksik", 0)
                renk = "#e94560" if eksik > 0 else "#06d6a0"
                durum = f"{eksik} EKSIK" if eksik > 0 else "TAM"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{s.get('nokta','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{s.get('tarih','')}</span>
                    </div>
                    <div>
                        <span style="color:#888;">{s.get('mevcut',0)}/{s.get('beklenen',0)}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.78rem;margin-left:8px;font-weight:600;">{durum}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── İletişim Zinciri ──
    with sub[3]:
        styled_section("📞 Acil Iletisim Zinciri", "#8338ec")

        with st.form("iletisim_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                i_ad = st.text_input("Ad Soyad", key="ilt_ad")
                i_gorev = st.selectbox("Gorev / Rol", [
                    "Acil Durum Koordinatoru", "Sivil Savunma Sorumlusu",
                    "ISG Uzmani", "Okul Muduru", "Mudur Yardimcisi",
                    "Kat Sorumlusu", "Guvenlik Amiri", "Saglik Gorevlisi",
                    "Itfaiye Irtibat", "Ambulans Irtibat",
                ], key="ilt_gorev")
            with ic2:
                i_telefon = st.text_input("Telefon", key="ilt_tel")
                i_email = st.text_input("E-posta", key="ilt_email")
            with ic3:
                i_sira = st.number_input("Arama Sirasi", min_value=1, value=len(iletisim_zinciri) + 1, key="ilt_sira")
                i_yedek = st.text_input("Yedek Kisi", key="ilt_yedek")

            if st.form_submit_button("📞 Zincire Ekle", use_container_width=True):
                if i_ad and i_telefon:
                    iletisim_zinciri.append({
                        "id": f"ilt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": i_ad,
                        "gorev": i_gorev,
                        "telefon": i_telefon,
                        "email": i_email,
                        "sira": i_sira,
                        "yedek": i_yedek,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(iletisim_path, iletisim_zinciri)
                    st.success(f"{i_ad} iletisim zincirine eklendi!")
                    st.rerun()

        if iletisim_zinciri:
            siralama = sorted(iletisim_zinciri, key=lambda x: x.get("sira", 999))
            for i, kisi in enumerate(siralama):
                kid = kisi.get("id", "")
                gorev_renk = {"Acil Durum Koordinatoru": "#e94560", "ISG Uzmani": "#ffd166", "Okul Muduru": "#8338ec"}.get(kisi.get("gorev", ""), "#00b4d8")
                ic1, ic2 = st.columns([7, 1])
                with ic1:
                    st.markdown(f"""
                    <div style="display:flex;gap:14px;margin-bottom:0;">
                        <div style="display:flex;flex-direction:column;align-items:center;min-width:35px;">
                            <div style="background:{gorev_renk};color:white;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;">{kisi.get('sira','')}</div>
                            {'<div style="width:2px;height:25px;background:' + gorev_renk + '40;"></div>' if i < len(siralama)-1 else ''}
                        </div>
                        <div style="background:#16213e;border-radius:10px;padding:10px 16px;flex:1;margin-bottom:6px;">
                            <div style="display:flex;justify-content:space-between;">
                                <strong style="color:#e0e0e0;">{kisi.get('ad','')}</strong>
                                <span style="color:{gorev_renk};font-size:0.82rem;">{kisi.get('gorev','')}</span>
                            </div>
                            <div style="color:#888;font-size:0.8rem;">📞 {kisi.get('telefon','')} | ✉️ {kisi.get('email','')} | Yedek: {kisi.get('yedek','—')}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with ic2:
                    if st.button("🗑️", key=f"del_ilt_{kid}", help="Iletisim kaydini sil"):
                        iletisim_zinciri[:] = [x for x in iletisim_zinciri if x.get("id") != kid]
                        _save_json(iletisim_path, iletisim_zinciri)
                        st.rerun()

    # ── Tatbikat Kronometresi ──
    with sub[4]:
        styled_section("⏱️ Tahliye Tatbikat Kronometresi & Kayit", "#ffd166")

        with st.form("tatbikat_krono_form"):
            kc1, kc2 = st.columns(2)
            with kc1:
                k_bina = st.text_input("Bina", key="krn_bina")
                k_tur = st.selectbox("Tatbikat Turu", ["Deprem", "Yangin", "Bomba Tehdidi", "Kimyasal", "Genel Tahliye"], key="krn_tur")
                k_tarih = st.date_input("Tarih", value=datetime.now().date(), key="krn_tarih")
            with kc2:
                k_sure = st.number_input("Gerceklesen Tahliye Suresi (sn)", min_value=0, value=180, step=10, key="krn_sure")
                k_katilimci = st.number_input("Katilimci Sayisi", min_value=0, value=300, key="krn_katilim")
                k_puan = st.slider("Degerlendirme (1-10)", 1, 10, 7, key="krn_puan")
            k_not = st.text_area("Notlar / Eksiklikler", height=60, key="krn_not")

            if st.form_submit_button("⏱️ Tatbikat Kaydet", use_container_width=True):
                if k_bina:
                    tatbikatlar.append({
                        "id": f"tat_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "bina": k_bina,
                        "tur": k_tur,
                        "tarih": str(k_tarih),
                        "sure_sn": k_sure,
                        "katilimci": k_katilimci,
                        "puan": k_puan,
                        "notlar": k_not,
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(tatbikat_path, tatbikatlar)
                    st.success("Tatbikat kaydi olusturuldu!")
                    st.rerun()

        if tatbikatlar:
            styled_section("Tatbikat Gecmisi", "#00b4d8")
            for t in reversed(tatbikatlar[-8:]):
                puan = t.get("puan", 0)
                renk = "#06d6a0" if puan >= 7 else ("#ffd166" if puan >= 5 else "#e94560")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;">{t.get('bina','')} — {t.get('tur','')}</strong>
                            <div style="color:#888;font-size:0.78rem;">{t.get('tarih','')} | {t.get('katilimci','')} kisi</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="color:#ffd166;font-weight:700;">{t.get('sure_sn','')} sn</div>
                            <div style="color:{renk};font-size:0.85rem;">Puan: {puan}/10</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Tahliye Analizi ──
    with sub[5]:
        styled_section("📊 Bina Bazli Tahliye Sure Analizi", "#8338ec")

        if tatbikatlar:
            bina_sureler = {}
            for t in tatbikatlar:
                b = t.get("bina", "?")
                if b not in bina_sureler:
                    bina_sureler[b] = []
                bina_sureler[b].append(t.get("sure_sn", 0))

            st.markdown("**Bina Bazli Ortalama Tahliye Suresi**")
            for bina, sureler in sorted(bina_sureler.items(), key=lambda x: sum(x[1])/len(x[1])):
                ort = sum(sureler) / len(sureler)
                en_iyi = min(sureler)
                en_kotu = max(sureler)
                # Hedef süre bulma
                hedef = 180
                for p in tahliye_planlari:
                    if p.get("bina") == bina:
                        hedef = p.get("hedef_sure", 180)
                        break

                basarili = ort <= hedef
                renk = "#06d6a0" if basarili else "#e94560"

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <strong style="color:#e0e0e0;">{bina}</strong>
                        <span style="color:{renk};font-weight:700;">Ort: {ort:.0f}sn (Hedef: {hedef}sn)</span>
                    </div>
                    <div style="display:flex;gap:16px;">
                        <span style="color:#06d6a0;font-size:0.78rem;">En iyi: {en_iyi}sn</span>
                        <span style="color:#e94560;font-size:0.78rem;">En kotu: {en_kotu}sn</span>
                        <span style="color:#888;font-size:0.78rem;">{len(sureler)} tatbikat</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Genel tahliye skoru
            tum_puanlar = [t.get("puan", 5) for t in tatbikatlar]
            ort_puan = sum(tum_puanlar) / len(tum_puanlar)
            renk = "#06d6a0" if ort_puan >= 7 else ("#ffd166" if ort_puan >= 5 else "#e94560")
            st.markdown(f"""
            <div style="background:#0f3460;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Genel Tahliye Hazirlik Skoru</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">{ort_puan:.1f}/10</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Tahliye analizi icin tatbikat kaydi gerekiyor.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. YANGIN & DOĞAL AFET RİSK HARİTASI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_yangin_afet_risk(store):
    _styled_header("Yangin & Dogal Afet Risk Haritasi", "🔥")

    ekipman_path = _get_data_path(store, "yangin_ekipman.json")
    ekipmanlar = _load_json(ekipman_path)

    denetim_path = _get_data_path(store, "yangin_denetimleri.json")
    denetimler = _load_json(denetim_path)

    risk_path = _get_data_path(store, "afet_risk_skorlari.json")
    risk_kayitlari = _load_json(risk_path)

    eylem_path = _get_data_path(store, "risk_eylem_planlari.json")
    eylem_planlari = _load_json(eylem_path)

    _styled_stat_row([
        ("Yangin Ekipmani", len(ekipmanlar)),
        ("Denetim Kaydi", len(denetimler)),
        ("Risk Degerlendirme", len(risk_kayitlari)),
        ("Eylem Plani", len(eylem_planlari)),
    ])

    sub = st.tabs(["🧯 Ekipman Envanteri", "🔍 Yangin Merdiveni", "📊 Risk Skorlama", "🌊 Afet Risk", "📋 Eylem Plani", "📈 Risk Dashboard"])

    # ── Ekipman Envanteri ──
    with sub[0]:
        styled_section("🧯 Yangin Sondurme Ekipman Envanteri", "#e94560")

        with st.form("ekipman_form"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_tip = st.selectbox("Ekipman Tipi", ["Yangin Sondurme Tupu", "Yangin Hortumu", "Yangin Dolabi", "Duman Dedektoru", "Yangin Alarm Butonu", "Sprinkler", "Yangin Battaniyesi", "Diger"], key="ye_tip")
                e_konum = st.text_input("Konum (Bina/Kat/Oda)", key="ye_konum")
            with ec2:
                e_son_kontrol = st.date_input("Son Kontrol Tarihi", value=datetime.now().date(), key="ye_kontrol")
                e_gecerlilik = st.date_input("Gecerlilik Bitis", value=datetime.now().date() + timedelta(days=365), key="ye_gecerlilik")
            e_durum = st.selectbox("Durum", ["Calisiyor", "Bakimda", "Suresi Doldu", "Arizali"], key="ye_durum")

            if st.form_submit_button("🧯 Ekipman Ekle", use_container_width=True):
                if e_konum:
                    ekipmanlar.append({
                        "id": f"ye_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "tip": e_tip,
                        "konum": e_konum,
                        "son_kontrol": str(e_son_kontrol),
                        "gecerlilik": str(e_gecerlilik),
                        "durum": e_durum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(ekipman_path, ekipmanlar)
                    st.success("Ekipman eklendi!")
                    st.rerun()

        if ekipmanlar:
            # Durum özeti
            durum_sayim = Counter(e.get("durum", "?") for e in ekipmanlar)
            suresi_dolan = [e for e in ekipmanlar if e.get("gecerlilik", "9999") < str(datetime.now().date())]
            if suresi_dolan:
                st.error(f"🚨 {len(suresi_dolan)} ekipmanin suresi doldu!")

            tip_sayim = Counter(e.get("tip", "?") for e in ekipmanlar)
            styled_section("Ekipman Dagilimi", "#ffd166")
            for tip, sayi in sorted(tip_sayim.items(), key=lambda x: -x[1]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">🧯 {tip}</span>
                    <span style="color:#ffd166;font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            styled_section("Detayli Liste", "#00b4d8")
            for e in ekipmanlar:
                eid = e.get("id", "")
                durum_renk = {"Calisiyor": "#06d6a0", "Bakimda": "#ffd166", "Suresi Doldu": "#e94560", "Arizali": "#ff6b6b"}.get(e.get("durum", ""), "#888")
                ec1, ec2 = st.columns([6, 1])
                with ec1:
                    st.markdown(f"""
                    <div style="background:#1a1a2e;border-radius:8px;padding:6px 12px;margin-bottom:3px;display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e0e0e0;font-size:0.88rem;">{e.get('tip','')} — {e.get('konum','')}</span>
                        <span style="color:{durum_renk};font-size:0.8rem;font-weight:600;">{e.get('durum','')} | Son: {e.get('son_kontrol','')}</span>
                    </div>""", unsafe_allow_html=True)
                with ec2:
                    if st.button("🗑️", key=f"del_ye_{eid}", help="Ekipmani sil"):
                        ekipmanlar[:] = [x for x in ekipmanlar if x.get("id") != eid]
                        _save_json(ekipman_path, ekipmanlar)
                        st.rerun()

    # ── Yangın Merdiveni ──
    with sub[1]:
        styled_section("🔍 Yangin Merdiveni & Acil Cikis Denetimi", "#06d6a0")

        with st.form("merdiven_form"):
            mc1, mc2 = st.columns(2)
            with mc1:
                m_bina = st.text_input("Bina", key="ym_bina")
                m_merdiven = st.text_input("Merdiven / Cikis No", key="ym_mer")
            with mc2:
                m_durum = st.selectbox("Denetim Sonucu", ["Uygun", "Kismi Uygun", "Uygun Degil", "Acil Mudahale"], key="ym_durum")
                m_tarih = st.date_input("Denetim Tarihi", value=datetime.now().date(), key="ym_tarih")
            m_bulgular = st.text_area("Bulgular / Eksiklikler", height=60, key="ym_bulgu")

            if st.form_submit_button("🔍 Denetim Kaydet", use_container_width=True):
                if m_bina:
                    denetimler.append({
                        "id": f"ymd_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "bina": m_bina,
                        "merdiven": m_merdiven,
                        "durum": m_durum,
                        "tarih": str(m_tarih),
                        "bulgular": m_bulgular,
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(denetim_path, denetimler)
                    st.success("Denetim kaydedildi!")
                    st.rerun()

        if denetimler:
            for d in reversed(denetimler[-10:]):
                durum_renk = {"Uygun": "#06d6a0", "Kismi Uygun": "#ffd166", "Uygun Degil": "#e94560", "Acil Mudahale": "#ff6b6b"}.get(d.get("durum", ""), "#888")
                durum_ikon = {"Uygun": "✅", "Kismi Uygun": "🟡", "Uygun Degil": "❌", "Acil Mudahale": "🚨"}.get(d.get("durum", ""), "⚪")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{durum_ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{d.get('bina','')} — {d.get('merdiven','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{d.get('tarih','')}</span>
                    </div>
                    <span style="background:{durum_renk}20;color:{durum_renk};padding:3px 10px;border-radius:6px;font-weight:600;font-size:0.82rem;">{d.get('durum','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Risk Skorlama ──
    with sub[2]:
        styled_section("📊 Bina Bazli Yangin Risk Skorlamasi", "#e94560")

        with st.form("risk_skor_form"):
            rc1, rc2 = st.columns(2)
            with rc1:
                r_bina = st.text_input("Bina / Alan", key="rs_bina")
                r_yangin_dedektoru = st.slider("Dedektoru Kapsama (%)", 0, 100, 80, key="rs_dedek")
                r_sondurme = st.slider("Sondurme Ekipmani Yeterliligi (%)", 0, 100, 70, key="rs_sond")
            with rc2:
                r_merdiven = st.slider("Acil Cikis Uygunlugu (%)", 0, 100, 85, key="rs_mer")
                r_egitim = st.slider("Personel Egitim Durumu (%)", 0, 100, 60, key="rs_egitim")
                r_elektrik = st.slider("Elektrik Tesisati Guvenligi (%)", 0, 100, 75, key="rs_elek")

            if st.form_submit_button("📊 Risk Degerlendirmesi Kaydet", use_container_width=True):
                if r_bina:
                    genel_skor = int((r_yangin_dedektoru + r_sondurme + r_merdiven + r_egitim + r_elektrik) / 5)
                    risk_seviye = "DUSUK" if genel_skor >= 80 else ("ORTA" if genel_skor >= 60 else ("YUKSEK" if genel_skor >= 40 else "KRITIK"))

                    risk_kayitlari.append({
                        "id": f"rs_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "bina": r_bina,
                        "dedektoru": r_yangin_dedektoru,
                        "sondurme": r_sondurme,
                        "merdiven": r_merdiven,
                        "egitim": r_egitim,
                        "elektrik": r_elektrik,
                        "genel_skor": genel_skor,
                        "seviye": risk_seviye,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(risk_path, risk_kayitlari)
                    st.success(f"{r_bina} risk skoru: {genel_skor}/100 ({risk_seviye})")
                    st.rerun()

        if risk_kayitlari:
            for r in sorted(risk_kayitlari, key=lambda x: x.get("genel_skor", 0)):
                skor = r.get("genel_skor", 0)
                renk = "#06d6a0" if skor >= 80 else ("#ffd166" if skor >= 60 else ("#e94560" if skor >= 40 else "#ff6b6b"))
                seviye = r.get("seviye", "?")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <strong style="color:#e0e0e0;font-size:1.05rem;">🏢 {r.get('bina','')}</strong>
                        <div>
                            <span style="color:{renk};font-weight:800;font-size:1.3rem;">{skor}/100</span>
                            <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.75rem;margin-left:6px;">{seviye}</span>
                        </div>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                        <div style="width:{skor}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Afet Risk ──
    with sub[3]:
        styled_section("🌊 Dogal Afet Risk Degerlendirmesi", "#00b4d8")

        afet_path = _get_data_path(store, "afet_risk.json")
        afetler = _load_json(afet_path)

        with st.form("afet_form"):
            ac1, ac2 = st.columns(2)
            with ac1:
                a_tur = st.selectbox("Afet Turu", ["Deprem", "Sel/Su Baskini", "Firtina", "Toprak Kaymasi", "Heyelan", "Kar/Buz", "Diger"], key="afet_tur")
                a_olasilik = st.selectbox("Olasilik", ["Cok Dusuk", "Dusuk", "Orta", "Yuksek", "Cok Yuksek"], key="afet_olas")
            with ac2:
                a_etki = st.selectbox("Etki Seviyesi", ["Ihmal Edilebilir", "Dusuk", "Orta", "Yuksek", "Felaket"], key="afet_etki")
                a_onlem = st.text_input("Alinan / Alinmasi Gereken Onlem", key="afet_onlem")

            if st.form_submit_button("🌊 Risk Degerlendirmesi Ekle", use_container_width=True):
                olas_puan = {"Cok Dusuk": 1, "Dusuk": 2, "Orta": 3, "Yuksek": 4, "Cok Yuksek": 5}.get(a_olasilik, 3)
                etki_puan = {"Ihmal Edilebilir": 1, "Dusuk": 2, "Orta": 3, "Yuksek": 4, "Felaket": 5}.get(a_etki, 3)
                risk_puan = olas_puan * etki_puan

                afetler.append({
                    "id": f"aft_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "tur": a_tur,
                    "olasilik": a_olasilik,
                    "etki": a_etki,
                    "risk_puan": risk_puan,
                    "onlem": a_onlem,
                    "tarih": datetime.now().isoformat(),
                })
                _save_json(afet_path, afetler)
                st.success(f"Afet riski eklendi! Risk puani: {risk_puan}/25")
                st.rerun()

        if afetler:
            for a in sorted(afetler, key=lambda x: -x.get("risk_puan", 0)):
                rp = a.get("risk_puan", 0)
                renk = "#e94560" if rp >= 15 else ("#ffd166" if rp >= 8 else "#06d6a0")
                seviye = "KRITIK" if rp >= 15 else ("YUKSEK" if rp >= 8 else "KABUL EDILEBILIR")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{a.get('tur','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">Olasilik: {a.get('olasilik','')} | Etki: {a.get('etki','')}</span>
                    </div>
                    <div>
                        <span style="color:{renk};font-weight:700;">{rp}/25</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.72rem;margin-left:6px;">{seviye}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Eylem Planı ──
    with sub[4]:
        styled_section("📋 Risk Azaltma Eylem Plani", "#ffd166")

        with st.form("eylem_risk_form"):
            erc1, erc2 = st.columns(2)
            with erc1:
                er_risk = st.text_input("Ilgili Risk / Bulgu", key="er_risk")
                er_eylem = st.text_area("Eylem / Onlem", height=60, key="er_eylem")
            with erc2:
                er_sorumlu = st.text_input("Sorumlu", key="er_sorumlu")
                er_hedef = st.date_input("Hedef Tarih", value=datetime.now().date() + timedelta(days=30), key="er_hedef")
                er_oncelik = st.selectbox("Oncelik", ["Acil", "Yuksek", "Normal", "Dusuk"], key="er_oncelik")

            if st.form_submit_button("📋 Eylem Plani Olustur", use_container_width=True):
                if er_risk and er_eylem:
                    eylem_planlari.append({
                        "id": f"ep_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "risk": er_risk,
                        "eylem": er_eylem,
                        "sorumlu": er_sorumlu,
                        "hedef": str(er_hedef),
                        "oncelik": er_oncelik,
                        "durum": "acik",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(eylem_path, eylem_planlari)
                    st.success("Eylem plani olusturuldu!")
                    st.rerun()

        if eylem_planlari:
            for idx, ep in enumerate(reversed(eylem_planlari[-10:])):
                durum = ep.get("durum", "acik")
                durum_ikon = {"acik": "🔴", "devam": "🟡", "tamamlandi": "🟢"}.get(durum, "⚪")
                onc_renk = {"Acil": "#e94560", "Yuksek": "#ff6b6b", "Normal": "#ffd166", "Dusuk": "#06d6a0"}.get(ep.get("oncelik", ""), "#888")

                with st.expander(f"{durum_ikon} {ep.get('risk','')[:40]} — {ep.get('oncelik','')}"):
                    st.write(f"**Eylem:** {ep.get('eylem','')}")
                    st.write(f"**Sorumlu:** {ep.get('sorumlu','')} | **Hedef:** {ep.get('hedef','')}")
                    yeni = st.selectbox("Durum", ["acik", "devam", "tamamlandi"], index=["acik", "devam", "tamamlandi"].index(durum), key=f"ep_d_{idx}")
                    if st.button("Guncelle", key=f"ep_btn_{idx}"):
                        ep["durum"] = yeni
                        _save_json(eylem_path, eylem_planlari)
                        st.rerun()

    # ── Risk Dashboard ──
    with sub[5]:
        styled_section("📈 Risk Genel Bakis Dashboard", "#8338ec")

        # Bileşenler
        ekipman_skor = 100 - len([e for e in ekipmanlar if e.get("durum") != "Calisiyor"]) * 10 if ekipmanlar else 50
        denetim_skor = len([d for d in denetimler if d.get("durum") == "Uygun"]) / max(1, len(denetimler)) * 100 if denetimler else 50
        risk_skor = sum(r.get("genel_skor", 50) for r in risk_kayitlari) / max(1, len(risk_kayitlari)) if risk_kayitlari else 50

        genel = int((max(0, ekipman_skor) + denetim_skor + risk_skor) / 3)
        renk = "#06d6a0" if genel >= 70 else ("#ffd166" if genel >= 40 else "#e94560")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:0.9rem;color:#888;">Yangin & Afet Guvenlik Skoru</div>
            <div style="font-size:3.5rem;font-weight:900;color:{renk};">{genel:.0f}/100</div>
        </div>""", unsafe_allow_html=True)

        bilesenler = [
            ("Ekipman Durumu", max(0, int(ekipman_skor)), "#e94560"),
            ("Denetim Uyumu", int(denetim_skor), "#06d6a0"),
            ("Risk Skorlama", int(risk_skor), "#ffd166"),
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
#  3. GÜVENLİK KAMERA & GİRİŞ-ÇIKIŞ KONTROL PANELİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_guvenlik_kontrol(store):
    _styled_header("Guvenlik Kamera & Giris-Cikis Kontrol Paneli", "📊")

    kamera_path = _get_data_path(store, "kamera_noktalari.json")
    kameralar = _load_json(kamera_path)

    giris_path = _get_data_path(store, "giris_cikis_kayitlari.json")
    giris_kayitlari = _load_json(giris_path)

    personel_path = _get_data_path(store, "guvenlik_personeli.json")
    guvenlik_personeli = _load_json(personel_path)

    tehdit_path = _get_data_path(store, "tehdit_seviyeleri.json")
    tehditler = _load_json(tehdit_path)

    _styled_stat_row([
        ("Kamera Noktasi", len(kameralar)),
        ("Giris/Cikis Kaydi", len(giris_kayitlari)),
        ("Guvenlik Personeli", len(guvenlik_personeli)),
        ("Tehdit Kaydi", len(tehditler)),
    ])

    sub = st.tabs(["📹 Kamera Yonetimi", "🚪 Giris-Cikis", "👮 Personel Vardiya", "🚨 Tehdit Seviyesi", "📋 Olay Zaman Cizelgesi", "📊 Guvenlik Skoru"])

    # ── Kamera Yönetimi ──
    with sub[0]:
        styled_section("📹 Kamera Noktasi Yonetimi", "#0f3460")

        with st.form("kamera_form"):
            kc1, kc2 = st.columns(2)
            with kc1:
                k_ad = st.text_input("Kamera Adi / No", key="kam_ad")
                k_konum = st.text_input("Konum", key="kam_konum")
                k_tip = st.selectbox("Kamera Tipi", ["Sabit", "PTZ (Donebilen)", "Dome", "Bullet", "IP Kamera"], key="kam_tip")
            with kc2:
                k_cozunurluk = st.selectbox("Cozunurluk", ["HD (720p)", "Full HD (1080p)", "2K", "4K"], key="kam_coz")
                k_kayit = st.selectbox("Kayit Suresi", ["7 Gun", "15 Gun", "30 Gun", "60 Gun", "90 Gun"], key="kam_kayit")
                k_durum = st.selectbox("Durum", ["Aktif", "Arizali", "Bakimda", "Pasif"], key="kam_durum")

            if st.form_submit_button("📹 Kamera Ekle", use_container_width=True):
                if k_ad:
                    kameralar.append({
                        "id": f"kam_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": k_ad,
                        "konum": k_konum,
                        "tip": k_tip,
                        "cozunurluk": k_cozunurluk,
                        "kayit_suresi": k_kayit,
                        "durum": k_durum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(kamera_path, kameralar)
                    st.success(f"Kamera '{k_ad}' eklendi!")
                    st.rerun()

        if kameralar:
            aktif = len([k for k in kameralar if k.get("durum") == "Aktif"])
            arizali = len([k for k in kameralar if k.get("durum") == "Arizali"])
            if arizali > 0:
                st.error(f"⚠️ {arizali} kamera arizali!")

            for k in kameralar:
                kid = k.get("id", "")
                durum_renk = {"Aktif": "#06d6a0", "Arizali": "#e94560", "Bakimda": "#ffd166", "Pasif": "#888"}.get(k.get("durum", ""), "#888")
                durum_ikon = {"Aktif": "🟢", "Arizali": "🔴", "Bakimda": "🟡", "Pasif": "⚫"}.get(k.get("durum", ""), "⚪")
                kc1, kc2 = st.columns([6, 1])
                with kc1:
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span>{durum_ikon}</span>
                            <strong style="color:#e0e0e0;margin-left:6px;">{k.get('ad','')}</strong>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">{k.get('konum','')} | {k.get('tip','')} | {k.get('cozunurluk','')}</span>
                        </div>
                        <span style="color:{durum_renk};font-size:0.82rem;font-weight:600;">{k.get('durum','')}</span>
                    </div>""", unsafe_allow_html=True)
                with kc2:
                    if st.button("🗑️", key=f"del_kam_{kid}", help="Kamerayi sil"):
                        kameralar[:] = [x for x in kameralar if x.get("id") != kid]
                        _save_json(kamera_path, kameralar)
                        st.rerun()

    # ── Giriş-Çıkış ──
    with sub[1]:
        styled_section("🚪 Giris-Cikis Kayit Sistemi", "#00b4d8")

        with st.form("giris_form"):
            gc1, gc2, gc3 = st.columns(3)
            with gc1:
                g_kisi = st.text_input("Kisi Adi", key="gc_kisi")
                g_tur = st.selectbox("Kisi Turu", ["Ogrenci", "Personel", "Ziyaretci", "Veli", "Kurye", "Diger"], key="gc_tur")
            with gc2:
                g_yonu = st.selectbox("Giris/Cikis", ["Giris", "Cikis"], key="gc_yon")
                g_kapi = st.text_input("Kapi / Giris Noktasi", key="gc_kapi")
            with gc3:
                g_tarih = st.date_input("Tarih", value=datetime.now().date(), key="gc_tarih")
                g_saat = st.time_input("Saat", value=datetime.now().time(), key="gc_saat")

            if st.form_submit_button("🚪 Kayit Ekle", use_container_width=True):
                if g_kisi:
                    giris_kayitlari.append({
                        "id": f"gc_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "kisi": g_kisi,
                        "tur": g_tur,
                        "yon": g_yonu,
                        "kapi": g_kapi,
                        "tarih": str(g_tarih),
                        "saat": str(g_saat),
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(giris_path, giris_kayitlari)
                    st.success(f"{g_kisi} — {g_yonu} kaydedildi!")
                    st.rerun()

        if giris_kayitlari:
            bugun = str(datetime.now().date())
            bugun_kayit = [g for g in giris_kayitlari if g.get("tarih") == bugun]
            giris_sayi = len([g for g in bugun_kayit if g.get("yon") == "Giris"])
            cikis_sayi = len([g for g in bugun_kayit if g.get("yon") == "Cikis"])

            _styled_stat_row([
                ("Bugun Giris", giris_sayi),
                ("Bugun Cikis", cikis_sayi),
                ("Icerdeki Kisi", max(0, giris_sayi - cikis_sayi)),
            ])

            styled_section("Son Kayitlar", "#ffd166")
            for g in reversed(giris_kayitlari[-12:]):
                yon_ikon = "🟢 Giris" if g.get("yon") == "Giris" else "🔴 Cikis"
                yon_renk = "#06d6a0" if g.get("yon") == "Giris" else "#e94560"
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:6px 12px;margin-bottom:3px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="color:{yon_renk};font-size:0.82rem;font-weight:600;">{yon_ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{g.get('kisi','')}</strong>
                        <span style="color:#888;font-size:0.75rem;margin-left:6px;">({g.get('tur','')})</span>
                    </div>
                    <span style="color:#888;font-size:0.75rem;">{g.get('kapi','')} | {g.get('tarih','')} {g.get('saat','')[:5]}</span>
                </div>""", unsafe_allow_html=True)

    # ── Personel Vardiya ──
    with sub[2]:
        styled_section("👮 Guvenlik Personeli Vardiya Plani", "#8338ec")

        with st.form("personel_form"):
            pc1, pc2 = st.columns(2)
            with pc1:
                p_ad = st.text_input("Ad Soyad", key="gp_ad")
                p_gorev = st.selectbox("Gorev", ["Guvenlik Amiri", "Guvenlik Gorevlisi", "Nobetci", "Kapi Gorevlisi"], key="gp_gorev")
            with pc2:
                p_vardiya = st.selectbox("Vardiya", ["Sabah (07-15)", "Aksam (15-23)", "Gece (23-07)", "Tam Gun"], key="gp_vardiya")
                p_telefon = st.text_input("Telefon", key="gp_tel")

            if st.form_submit_button("👮 Personel Ekle", use_container_width=True):
                if p_ad:
                    guvenlik_personeli.append({
                        "id": f"gp_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": p_ad,
                        "gorev": p_gorev,
                        "vardiya": p_vardiya,
                        "telefon": p_telefon,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(personel_path, guvenlik_personeli)
                    st.success(f"{p_ad} eklendi!")
                    st.rerun()

        if guvenlik_personeli:
            vardiya_grup = {}
            for p in guvenlik_personeli:
                v = p.get("vardiya", "?")
                if v not in vardiya_grup:
                    vardiya_grup[v] = []
                vardiya_grup[v].append(p)

            for vardiya, kisiler in vardiya_grup.items():
                styled_section(f"{vardiya} ({len(kisiler)} kisi)", "#00b4d8")
                for p in kisiler:
                    pid = p.get("id", "")
                    pc1, pc2 = st.columns([6, 1])
                    with pc1:
                        st.markdown(f"""
                        <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                            <span style="color:#e0e0e0;">👮 {p.get('ad','')} — {p.get('gorev','')}</span>
                            <span style="color:#888;font-size:0.78rem;">📞 {p.get('telefon','')}</span>
                        </div>""", unsafe_allow_html=True)
                    with pc2:
                        if st.button("🗑️", key=f"del_gp_{pid}", help="Personeli sil"):
                            guvenlik_personeli[:] = [x for x in guvenlik_personeli if x.get("id") != pid]
                            _save_json(personel_path, guvenlik_personeli)
                            st.rerun()

    # ── Tehdit Seviyesi ──
    with sub[3]:
        styled_section("🚨 Tehdit Seviyesi Gostergesi", "#e94560")

        seviyeler = [
            {"ad": "YESIL — Normal", "renk": "#06d6a0", "aciklama": "Rutin operasyon, bilinen tehdit yok"},
            {"ad": "MAVI — Dusuk", "renk": "#00b4d8", "aciklama": "Genel uyari, artirilmis farkindalik"},
            {"ad": "SARI — Orta", "renk": "#ffd166", "aciklama": "Belirli tehdit mevcut, artirilmis guvenlik"},
            {"ad": "TURUNCU — Yuksek", "renk": "#ff6b6b", "aciklama": "Ciddi tehdit, ek onlemler aktif"},
            {"ad": "KIRMIZI — Kritik", "renk": "#e94560", "aciklama": "Yakin tehdit, tam guvenlik modu"},
        ]

        mevcut_seviye = tehditler[-1].get("seviye", "YESIL") if tehditler else "YESIL"
        mevcut_bilgi = next((s for s in seviyeler if s["ad"].startswith(mevcut_seviye)), seviyeler[0])

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{mevcut_bilgi['renk']}20,#16213e);border:2px solid {mevcut_bilgi['renk']}40;border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:0.9rem;color:#888;">Mevcut Tehdit Seviyesi</div>
            <div style="font-size:2rem;font-weight:900;color:{mevcut_bilgi['renk']};margin:8px 0;">{mevcut_bilgi['ad']}</div>
            <div style="color:#aaa;font-size:0.88rem;">{mevcut_bilgi['aciklama']}</div>
        </div>""", unsafe_allow_html=True)

        yeni_seviye = st.selectbox("Tehdit Seviyesi Degistir", ["YESIL", "MAVI", "SARI", "TURUNCU", "KIRMIZI"], key="tehdit_sec")
        t_neden = st.text_input("Degisiklik Nedeni", key="tehdit_neden")
        if st.button("🚨 Seviye Guncelle"):
            tehditler.append({
                "seviye": yeni_seviye,
                "neden": t_neden,
                "tarih": datetime.now().isoformat(),
            })
            _save_json(tehdit_path, tehditler)
            st.success(f"Tehdit seviyesi {yeni_seviye} olarak guncellendi!")
            st.rerun()

        if tehditler:
            styled_section("Tehdit Gecmisi", "#888")
            for t in reversed(tehditler[-8:]):
                sev_renk = {"YESIL": "#06d6a0", "MAVI": "#00b4d8", "SARI": "#ffd166", "TURUNCU": "#ff6b6b", "KIRMIZI": "#e94560"}.get(t.get("seviye", ""), "#888")
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:6px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                    <span style="color:{sev_renk};font-weight:600;">{t.get('seviye','')}</span>
                    <span style="color:#888;font-size:0.75rem;">{t.get('neden','')} | {t.get('tarih','')[:16]}</span>
                </div>""", unsafe_allow_html=True)

    # ── Olay Zaman Çizelgesi ──
    with sub[4]:
        styled_section("📋 Guvenlik Olayi Zaman Cizelgesi", "#ffd166")

        olay_path = _get_data_path(store, "guvenlik_olaylari.json")
        olaylar = _load_json(olay_path)

        with st.form("guvenlik_olay_form"):
            oc1, oc2 = st.columns(2)
            with oc1:
                o_baslik = st.text_input("Olay Tanimi", key="go_baslik")
                o_tur = st.selectbox("Olay Turu", ["Hirsizlik/Kayip", "Kavga/Siddet", "Izinsiz Giris", "Vandalizm", "Tehdit", "Kaza", "Suphe", "Diger"], key="go_tur")
            with oc2:
                o_konum = st.text_input("Konum", key="go_konum")
                o_ciddiyet = st.selectbox("Ciddiyet", ["Dusuk", "Orta", "Yuksek", "Kritik"], key="go_ciddiyet")
            o_detay = st.text_area("Detay", height=60, key="go_detay")

            if st.form_submit_button("📋 Olay Kaydet", use_container_width=True):
                if o_baslik:
                    olaylar.append({
                        "id": f"go_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": o_baslik,
                        "tur": o_tur,
                        "konum": o_konum,
                        "ciddiyet": o_ciddiyet,
                        "detay": o_detay,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(olay_path, olaylar)
                    st.success("Guvenlik olayi kaydedildi!")
                    st.rerun()

        if olaylar:
            for i, o in enumerate(reversed(olaylar[-12:])):
                cid_renk = {"Dusuk": "#06d6a0", "Orta": "#ffd166", "Yuksek": "#ff6b6b", "Kritik": "#e94560"}.get(o.get("ciddiyet", ""), "#888")
                tur_ikon = {"Hirsizlik/Kayip": "🔓", "Kavga/Siddet": "⚡", "Izinsiz Giris": "🚫", "Vandalizm": "💥", "Tehdit": "⚠️", "Kaza": "🤕", "Suphe": "🔍"}.get(o.get("tur", ""), "📋")

                st.markdown(f"""
                <div style="display:flex;gap:14px;margin-bottom:0;">
                    <div style="display:flex;flex-direction:column;align-items:center;min-width:30px;">
                        <div style="font-size:1.2rem;">{tur_ikon}</div>
                        {'<div style="width:2px;height:25px;background:#ffd16640;"></div>' if i < 11 else ''}
                    </div>
                    <div style="background:#16213e;border-radius:8px;padding:10px 14px;flex:1;margin-bottom:6px;border-left:3px solid {cid_renk};">
                        <div style="display:flex;justify-content:space-between;">
                            <strong style="color:#e0e0e0;">{o.get('baslik','')}</strong>
                            <span style="color:#888;font-size:0.75rem;">{o.get('tarih','')[:16]}</span>
                        </div>
                        <span style="color:#888;font-size:0.8rem;">{o.get('konum','')} | <span style="color:{cid_renk}">{o.get('ciddiyet','')}</span></span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Güvenlik Skoru ──
    with sub[5]:
        styled_section("📊 Genel Guvenlik Skoru", "#06d6a0")

        kamera_skor = int(len([k for k in kameralar if k.get("durum") == "Aktif"]) / max(1, len(kameralar)) * 100) if kameralar else 50
        personel_skor = min(100, len(guvenlik_personeli) * 20) if guvenlik_personeli else 30
        tehdit_skor = {"YESIL": 100, "MAVI": 80, "SARI": 60, "TURUNCU": 40, "KIRMIZI": 20}.get(mevcut_seviye, 50)

        genel = int((kamera_skor + personel_skor + tehdit_skor) / 3)
        renk = "#06d6a0" if genel >= 70 else ("#ffd166" if genel >= 40 else "#e94560")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:0.9rem;color:#888;">Genel Guvenlik Skoru</div>
            <div style="font-size:3.5rem;font-weight:900;color:{renk};">{genel}/100</div>
        </div>""", unsafe_allow_html=True)

        bilesenler = [
            ("Kamera Sistemi", kamera_skor, "#00b4d8"),
            ("Personel Yeterliligi", personel_skor, "#06d6a0"),
            ("Tehdit Seviyesi", tehdit_skor, "#ffd166"),
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
