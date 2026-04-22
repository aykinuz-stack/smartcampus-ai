"""
Okul Oncesi - Ilkokul Modulu
==============================
Anasınıfı (4 Yaş, 5 Yaş, Hazırlık) gunluk bulten yonetimi
ve Ilkokul (1-4. sinif) hizli erisim paneli.
"""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from models.akademik_takip import AkademikDataStore
from utils.tenant import get_data_path
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("okul_oncesi")
except Exception:
    pass


# =====================================================================
# STIL YARDIMCILARI (Akademik Takip ile ayni tasarim dili)
# =====================================================================

def _inject_css():
    """Modul icin premium CSS enjekte et."""
    inject_common_css("ooi")


def _styled_group_header(title: str, subtitle: str = "", color: str = "#2563eb"):
    """Grup basligini gorsel olarak vurgulayan mini header."""
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{color}12 0%,{color}06 100%);'
        f'border:1px solid {color}20;border-radius:12px;padding:12px 18px;margin:6px 0 10px 0;">'
        f'<div style="font-size:1.05rem;font-weight:700;color:{color};">{title}</div>'
        + (f'<div style="font-size:0.78rem;color:#64748b;margin-top:2px;">{subtitle}</div>' if subtitle else '')
        + '</div>',
        unsafe_allow_html=True
    )




def _sinif_label(sinif_code: str) -> str:
    """Sinif kodunu okunabilir etikete cevir."""
    labels = {
        "ana4": "Anasınıfı (4 Yaş)",
        "ana5": "Anasınıfı (5 Yaş)",
        "anahaz": "Anasınıfı (Hazırlık)",
    }
    return labels.get(sinif_code, f"{sinif_code}. Sınıf")


# =====================================================================
# ANA RENDER FONKSIYONU
# =====================================================================

def render_okul_oncesi_ilkokul() -> None:
    """Okul Oncesi - Ilkokul modulu ana render fonksiyonu."""
    _inject_css()

    store = AkademikDataStore()

    styled_header(
        title="Okul Öncesi — İlkokul",
        subtitle="Anasınıfı günlük bülten yönetimi ve İlkokul hızlı erişim paneli",
        icon="🎨",
    )

    # Ana sekmeler
    # -- Tab Gruplama (15 tab -> 3 grup) --
    _GRP_TABS = {
        "📋 Grup A": [("  🎨 Okul Öncesi  ", 0), ("  📖 İlkokul  ", 1), ("  🧒 Gelişim Takip  ", 2), ("  📋 Haftalık Rapor  ", 3), ("  ⚠️ Erken Uyarı  ", 4), ("  📁 Gelişim Dosyası  ", 5), ("  🎮 Aktivite Plan  ", 6)],
        "📊 Grup B": [("  🌉 Veli Köprüsü  ", 7), ("  🧬 Davranış DNA  ", 8), ("  🎛️ Sınıf Asistan  ", 9), ("  👪 Ebeveyn Okulu  ", 10), ("  🧮 Sınıf Karması  ", 11), ("  😊 Mutluluk  ", 12), ("  🎓 Hazırlık  ", 13)],
        "🔧 Grup C": [("  🤖 Smarti  ", 14)],
    }
    _sg_grp_49533 = st.radio("", list(_GRP_TABS.keys()), horizontal=True, label_visibility="collapsed", key="rg_grp_49533")
    _gt_grp_49533 = _GRP_TABS[_sg_grp_49533]
    _tn_grp_49533 = [t[0] for t in _gt_grp_49533]
    _ti_grp_49533 = [t[1] for t in _gt_grp_49533]
    _tabs_grp_49533 = st.tabs(_tn_grp_49533)
    _tmap_grp_49533 = {i: t for i, t in zip(_ti_grp_49533, _tabs_grp_49533)}
    tab_okul_oncesi = _tmap_grp_49533.get(0)
    tab_ilkokul = _tmap_grp_49533.get(1)
    tab_milestone = _tmap_grp_49533.get(2)
    tab_haftalik = _tmap_grp_49533.get(3)
    tab_erken_uyari = _tmap_grp_49533.get(4)
    tab_portfolyo = _tmap_grp_49533.get(5)
    tab_aktivite = _tmap_grp_49533.get(6)
    tab_kopru = _tmap_grp_49533.get(7)
    tab_dna = _tmap_grp_49533.get(8)
    tab_sinif_ai = _tmap_grp_49533.get(9)
    tab_ebeveyn = _tmap_grp_49533.get(10)
    tab_karma = _tmap_grp_49533.get(11)
    tab_mutluluk = _tmap_grp_49533.get(12)
    tab_hazirlik = _tmap_grp_49533.get(13)
    tab_smarti = _tmap_grp_49533.get(14)

    if tab_okul_oncesi is not None:
      with tab_okul_oncesi:
        _render_okul_oncesi(store)

    if tab_ilkokul is not None:
      with tab_ilkokul:
        _render_ilkokul(store)

    # ZIRVE: Milestone Tracker
    if tab_milestone is not None:
      with tab_milestone:
        try:
            from views._ooi_zirve import render_milestone_tracker
            render_milestone_tracker(store)
        except Exception as _e:
            st.error(f"Gelisim Takip yuklenemedi: {_e}")

    # ZIRVE: Haftalik Veli Rapor
    if tab_haftalik is not None:
      with tab_haftalik:
        try:
            from views._ooi_zirve import render_haftalik_veli_rapor
            render_haftalik_veli_rapor(store)
        except Exception as _e:
            st.error(f"Haftalik Rapor yuklenemedi: {_e}")

    # ZIRVE: AI Erken Uyari
    if tab_erken_uyari is not None:
      with tab_erken_uyari:
        try:
            from views._ooi_zirve import render_erken_gelisim_uyari
            render_erken_gelisim_uyari(store)
        except Exception as _e:
            st.error(f"Erken Uyari yuklenemedi: {_e}")

    # MEGA: Dijital Gelisim Dosyasi
    if tab_portfolyo is not None:
      with tab_portfolyo:
        try:
            from views._ooi_mega import render_gelisim_dosyasi
            render_gelisim_dosyasi(store)
        except Exception as _e:
            st.error(f"Gelisim Dosyasi yuklenemedi: {_e}")

    # MEGA: AI Aktivite Planlayici
    if tab_aktivite is not None:
      with tab_aktivite:
        try:
            from views._ooi_mega import render_aktivite_planlayici
            render_aktivite_planlayici(store)
        except Exception as _e:
            st.error(f"Aktivite Planlayici yuklenemedi: {_e}")

    # MEGA: Veli-Ogretmen Koprusu
    if tab_kopru is not None:
      with tab_kopru:
        try:
            from views._ooi_mega import render_veli_koprusu
            render_veli_koprusu(store)
        except Exception as _e:
            st.error(f"Veli Koprusu yuklenemedi: {_e}")

    # ULTRA MEGA: Davranis DNA
    if tab_dna is not None:
      with tab_dna:
        try:
            from views._ooi_ultra import render_davranis_dna
            render_davranis_dna(store)
        except Exception as _e:
            st.error(f"Davranis DNA yuklenemedi: {_e}")

    # ULTRA MEGA: Sinif Yonetim Asistani
    if tab_sinif_ai is not None:
      with tab_sinif_ai:
        try:
            from views._ooi_ultra import render_sinif_asistani
            render_sinif_asistani(store)
        except Exception as _e:
            st.error(f"Sinif Asistani yuklenemedi: {_e}")

    # ULTRA MEGA: Ebeveyn Okulu
    if tab_ebeveyn is not None:
      with tab_ebeveyn:
        try:
            from views._ooi_ultra import render_ebeveyn_okulu
            render_ebeveyn_okulu(store)
        except Exception as _e:
            st.error(f"Ebeveyn Okulu yuklenemedi: {_e}")

    # ZIRVE: Sinif Karmasi Optimizatoru
    if tab_karma is not None:
      with tab_karma:
        try:
            from views._ooi_final import render_sinif_karmasi
            render_sinif_karmasi(store)
        except Exception as _e:
            st.error(f"Sinif Karmasi yuklenemedi: {_e}")

    # ZIRVE: Cocuk Mutluluk Barometresi
    if tab_mutluluk is not None:
      with tab_mutluluk:
        try:
            from views._ooi_final import render_mutluluk_barometresi
            render_mutluluk_barometresi(store)
        except Exception as _e:
            st.error(f"Mutluluk Barometresi yuklenemedi: {_e}")

    # ZIRVE: Okula Hazirlik Endeksi
    if tab_hazirlik is not None:
      with tab_hazirlik:
        try:
            from views._ooi_final import render_hazirlik_endeksi
            render_hazirlik_endeksi(store)
        except Exception as _e:
            st.error(f"Hazirlik Endeksi yuklenemedi: {_e}")

    if tab_smarti is not None:
      with tab_smarti:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="okul_oncesi_ilkokul")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_okul_oncesi_ilkokul")
            if st.button("Gönder", key="smarti_send_okul_oncesi_ilkokul"):
                if user_q.strip():
                    try:
                        from openai import OpenAI
                        import os
                        api_key = os.environ.get("OPENAI_API_KEY", "")
                        if api_key:
                            client = OpenAI(api_key=api_key)
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. okul_oncesi_ilkokul modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


# =====================================================================
# OKUL ÖNCESİ — GÜNLÜK BÜLTEN
# =====================================================================

def _render_okul_oncesi(store):
    """Okul Oncesi sekmesi — Gunluk Bulten doldur / toplu doldur / gecmis."""
    from models.akademik_takip import (
        GunlukBulten, BULTEN_ETKINLIKLER, BULTEN_BESLENME,
        BULTEN_DUYGU, BULTEN_ARKADAS, BULTEN_KURALLAR,
        BULTEN_AYRILIK, BULTEN_TUVALET, BULTEN_UYKU,
        BULTEN_TESLIM, BULTEN_EVDE,
    )
    from utils.shared_data import normalize_sinif, KADEME_SINIFLAR

    _styled_group_header(
        "Okul Öncesi — Günlük Bülten",
        "Anasınıfı öğrencileri için günlük iletişim formu (Okulumda Bugün)",
        color="#7c3aed"
    )

    ot1, ot2, ot3, ot4, ot5, ot6 = st.tabs([
        "  📝 Günlük Bülten Doldur  ",
        "  📋 Toplu Doldur  ",
        "  📊 Bülten Geçmişi  ",
        "  📩 Veli Bildirimleri  ",
        "  📎 Belge & Link  ",
        "  ▶ Dijital Öğrenme  ",
    ])

    # --- Anasınıfı öğrencilerini filtrele ---
    all_students = store.get_students()
    ana_siniflar = KADEME_SINIFLAR.get("Anaokulu", ["ana4", "ana5", "anahaz"])
    ana_students = [s for s in all_students
                    if normalize_sinif(str(s.sinif)) in ana_siniflar and s.durum == "aktif"]

    if not ana_students:
        with ot1:
            st.info("Sistemde anasınıfı öğrencisi bulunmuyor. "
                    "KOI › İletişim › Sınıf Listeleri'nden anasınıfı öğrencisi ekleyin.")
        return

    # Sınıf/şube kombinasyonları
    sinif_sube_map = {}
    for s in ana_students:
        ns = normalize_sinif(str(s.sinif))
        key = f"{ns}/{s.sube}"
        if key not in sinif_sube_map:
            sinif_sube_map[key] = {"sinif": ns, "sube": s.sube, "label": f"{_sinif_label(ns)} - {s.sube}", "ogrenciler": []}
        sinif_sube_map[key]["ogrenciler"].append(s)

    sinif_opts = list(sinif_sube_map.keys())
    sinif_labels = [sinif_sube_map[k]["label"] for k in sinif_opts]

    # ============ TEK ÖĞRENCİ BÜLTEN DOLDUR ============
    with ot1:
        styled_section("📝 Günlük Bülten Doldur", "#7c3aed")

        # Üst filtreler
        fc1, fc2, fc3 = st.columns([1, 1, 2])
        with fc1:
            tarih = st.date_input("Tarih", value=date.today(), key="blt_tarih")
        with fc2:
            secili_idx = st.selectbox("Sınıf / Şube", range(len(sinif_opts)),
                                      format_func=lambda i: sinif_labels[i],
                                      key="blt_sinif_sec")
            secili_key = sinif_opts[secili_idx]
            secili_sinif = sinif_sube_map[secili_key]["sinif"]
            secili_sube = sinif_sube_map[secili_key]["sube"]
        with fc3:
            ogr_list = sinif_sube_map[secili_key]["ogrenciler"]
            ogr_labels = [f"{s.ad} {s.soyad} ({s.numara})" for s in ogr_list]
            ogr_idx = st.selectbox("Öğrenci", range(len(ogr_list)),
                                    format_func=lambda i: ogr_labels[i],
                                    key="blt_ogr_sec")
            secili_ogr = ogr_list[ogr_idx]

        tarih_str = tarih.strftime("%Y-%m-%d")

        # Mevcut bülten varsa yükle
        mevcut = store.get_gunluk_bultenler(student_id=secili_ogr.id, tarih=tarih_str)
        blt = mevcut[0] if mevcut else GunlukBulten(
            student_id=secili_ogr.id,
            student_adi=f"{secili_ogr.ad} {secili_ogr.soyad}",
            tarih=tarih_str,
            sinif=secili_sinif,
            sube=secili_sube,
        )
        if mevcut:
            st.info(f"Bu tarih için kayıtlı bülten mevcut — düzenleme modunda.")

        st.markdown("---")

        # --- 1. GELİŞ / ÇIKIŞ ---
        styled_section("🏫 Geliş / Çıkış Bilgileri", "#2563eb")
        gc1, gc2, gc3, gc4 = st.columns(4)
        with gc1:
            blt.gelis_saati = st.text_input("Geliş Saati", value=blt.gelis_saati,
                                             placeholder="08:30", key="blt_gelis")
        with gc2:
            blt.cikis_saati = st.text_input("Çıkış Saati", value=blt.cikis_saati,
                                             placeholder="16:00", key="blt_cikis")
        with gc3:
            servis_opts = ["", "var", "yok"]
            servis_labels = ["Seçiniz", "Var", "Yok"]
            servis_idx = servis_opts.index(blt.servis) if blt.servis in servis_opts else 0
            blt.servis = servis_opts[st.selectbox("Servis", range(len(servis_opts)),
                                                    format_func=lambda i: servis_labels[i],
                                                    index=servis_idx, key="blt_servis")]
        with gc4:
            teslim_keys = [""] + [k for k, _ in BULTEN_TESLIM]
            teslim_labels = ["Seçiniz"] + [v for _, v in BULTEN_TESLIM]
            teslim_idx = teslim_keys.index(blt.teslim_eden) if blt.teslim_eden in teslim_keys else 0
            blt.teslim_eden = teslim_keys[st.selectbox("Teslim Eden", range(len(teslim_keys)),
                                                         format_func=lambda i: teslim_labels[i],
                                                         index=teslim_idx, key="blt_teslim")]

        # --- 2. BESLENME ---
        styled_section("🍽️ Beslenme", "#059669")
        bc1, bc2, bc3 = st.columns(3)
        beslenme_keys = [""] + [k for k, _ in BULTEN_BESLENME]
        beslenme_labels = ["Seçiniz"] + [v for _, v in BULTEN_BESLENME]

        with bc1:
            st.markdown("**☕ Sabah Kahvaltı**")
            idx_k = beslenme_keys.index(blt.kahvalti) if blt.kahvalti in beslenme_keys else 0
            blt.kahvalti = beslenme_keys[st.selectbox("Kahvaltı", range(len(beslenme_keys)),
                                                        format_func=lambda i: beslenme_labels[i],
                                                        index=idx_k, key="blt_kahvalti")]
            blt.kahvalti_not = st.text_input("Alerji/Not", value=blt.kahvalti_not, key="blt_kahvalti_not")

        with bc2:
            st.markdown("**🍽️ Öğle Yemeği**")
            idx_o = beslenme_keys.index(blt.ogle) if blt.ogle in beslenme_keys else 0
            blt.ogle = beslenme_keys[st.selectbox("Öğle", range(len(beslenme_keys)),
                                                    format_func=lambda i: beslenme_labels[i],
                                                    index=idx_o, key="blt_ogle")]
            blt.ogle_not = st.text_input("Alerji/Not", value=blt.ogle_not, key="blt_ogle_not")

        with bc3:
            st.markdown("**🍎 İkindi / Ara Öğün**")
            idx_i = beslenme_keys.index(blt.ikindi) if blt.ikindi in beslenme_keys else 0
            blt.ikindi = beslenme_keys[st.selectbox("İkindi", range(len(beslenme_keys)),
                                                      format_func=lambda i: beslenme_labels[i],
                                                      index=idx_i, key="blt_ikindi")]
            blt.ikindi_not = st.text_input("Alerji/Not", value=blt.ikindi_not, key="blt_ikindi_not")

        # --- 3. ETKİNLİKLER ---
        styled_section("🎨 Oyun & Etkinlikler", "#d97706")
        etk_keys = [k for k, _ in BULTEN_ETKINLIKLER]
        etk_labels = [v for _, v in BULTEN_ETKINLIKLER]
        default_etk = [i for i, k in enumerate(etk_keys) if k in blt.etkinlikler]
        secili_etk = st.multiselect("Yapılan Etkinlikler", range(len(etk_keys)),
                                     default=default_etk,
                                     format_func=lambda i: etk_labels[i],
                                     key="blt_etkinlikler")
        blt.etkinlikler = [etk_keys[i] for i in secili_etk]
        blt.one_cikan_beceri = st.text_area("Bugün öne çıkan kazanım / beceri",
                                             value=blt.one_cikan_beceri,
                                             height=68, key="blt_beceri")
        blt.bugun_urun = st.text_area("Bugün yaptığım ürün / çalışma",
                                       value=getattr(blt, 'bugun_urun', ''),
                                       height=68, key="blt_urun")

        # --- 4. DUYGU DURUMU & SOSYAL UYUM ---
        styled_section("😊 Duygu Durumu & Sosyal Uyum", "#dc2626")
        dc1, dc2 = st.columns(2)

        with dc1:
            duygu_keys = [""] + [k for k, _ in BULTEN_DUYGU]
            duygu_labels = ["Seçiniz"] + [v for _, v in BULTEN_DUYGU]
            duygu_idx = duygu_keys.index(blt.duygu) if blt.duygu in duygu_keys else 0
            blt.duygu = duygu_keys[st.selectbox("Duygu Durumu", range(len(duygu_keys)),
                                                  format_func=lambda i: duygu_labels[i],
                                                  index=duygu_idx, key="blt_duygu")]

            ark_keys = [""] + [k for k, _ in BULTEN_ARKADAS]
            ark_labels = ["Seçiniz"] + [v for _, v in BULTEN_ARKADAS]
            ark_idx = ark_keys.index(blt.arkadas_iliskisi) if blt.arkadas_iliskisi in ark_keys else 0
            blt.arkadas_iliskisi = ark_keys[st.selectbox("Arkadaş İlişkisi", range(len(ark_keys)),
                                                           format_func=lambda i: ark_labels[i],
                                                           index=ark_idx, key="blt_arkadas")]

        with dc2:
            kur_keys = [""] + [k for k, _ in BULTEN_KURALLAR]
            kur_labels = ["Seçiniz"] + [v for _, v in BULTEN_KURALLAR]
            kur_idx = kur_keys.index(blt.sinif_kurallari) if blt.sinif_kurallari in kur_keys else 0
            blt.sinif_kurallari = kur_keys[st.selectbox("Sınıf Kuralları", range(len(kur_keys)),
                                                          format_func=lambda i: kur_labels[i],
                                                          index=kur_idx, key="blt_kurallar")]

            ayr_keys = [""] + [k for k, _ in BULTEN_AYRILIK]
            ayr_labels = ["Seçiniz"] + [v for _, v in BULTEN_AYRILIK]
            ayr_idx = ayr_keys.index(blt.ayrilik_uyumu) if blt.ayrilik_uyumu in ayr_keys else 0
            blt.ayrilik_uyumu = ayr_keys[st.selectbox("Ayrılık / Sabah Uyumu", range(len(ayr_keys)),
                                                        format_func=lambda i: ayr_labels[i],
                                                        index=ayr_idx, key="blt_ayrilik")]

        # --- 5. SAĞLIK, UYKU & ÖZ BAKIM ---
        styled_section("🏥 Sağlık, Uyku & Öz Bakım", "#0891b2")
        sc1, sc2 = st.columns(2)

        with sc1:
            tuv_keys = [""] + [k for k, _ in BULTEN_TUVALET]
            tuv_labels = ["Seçiniz"] + [v for _, v in BULTEN_TUVALET]
            tuv_idx = tuv_keys.index(blt.tuvalet) if blt.tuvalet in tuv_keys else 0
            blt.tuvalet = tuv_keys[st.selectbox("Tuvalet", range(len(tuv_keys)),
                                                  format_func=lambda i: tuv_labels[i],
                                                  index=tuv_idx, key="blt_tuvalet")]

            uyku_keys = [""] + [k for k, _ in BULTEN_UYKU]
            uyku_labels = ["Seçiniz"] + [v for _, v in BULTEN_UYKU]
            uyku_idx = uyku_keys.index(blt.uyku_durumu) if blt.uyku_durumu in uyku_keys else 0
            blt.uyku_durumu = uyku_keys[st.selectbox("Uyku", range(len(uyku_keys)),
                                                       format_func=lambda i: uyku_labels[i],
                                                       index=uyku_idx, key="blt_uyku")]

            blt.uyku_suresi = st.number_input("Uyku Süresi (dk)", min_value=0, max_value=180,
                                               value=blt.uyku_suresi, key="blt_uyku_sure")

        with sc2:
            uc1, uc2 = st.columns(2)
            with uc1:
                blt.uyku_baslangic = st.text_input("Uyku Başlangıç", value=blt.uyku_baslangic,
                                                     placeholder="13:00", key="blt_uyku_bas")
            with uc2:
                blt.uyku_bitis = st.text_input("Uyku Bitiş", value=blt.uyku_bitis,
                                                 placeholder="14:30", key="blt_uyku_bit")

            blt.saglik_notu = st.text_area("Şikâyet / Ateş / İlaç", value=blt.saglik_notu,
                                            height=60, key="blt_saglik")
            blt.kaza_notu = st.text_input("Küçük kaza / yaralanma", value=blt.kaza_notu,
                                           key="blt_kaza")

        # --- 6. AKADEMIK & GELISIM (YENI) ---
        styled_section("🎯 Akademik & Gelişim", "#0d9488")
        akg1, akg2 = st.columns(2)
        with akg1:
            blt.bugun_ogrendigi = st.text_area(
                "🎯 Bugün öğrendiği yeni şey",
                value=blt.bugun_ogrendigi, height=70,
                placeholder="örn. Sayılar 1-5 arası, üçgen şekli",
                key="blt_ogrendigi",
            )
            blt.bugun_basari = st.text_area(
                "🌟 Bugünkü başarısı (Başarı Duvarı'na otomatik düşer)",
                value=blt.bugun_basari, height=70,
                placeholder="örn. Sıraya en hızlı dizildi, lider oldu",
                key="blt_basari",
            )
        with akg2:
            blt.yarin_hazirlik = st.text_area(
                "📚 Yarın için hazırlık",
                value=blt.yarin_hazirlik, height=70,
                placeholder="örn. Resim defteri + boya getirin",
                key="blt_hazirlik",
            )
            from models.akademik_takip import CANTA_KONTROL
            canta_keys = [k for k, _ in CANTA_KONTROL]
            canta_labels = [v for _, v in CANTA_KONTROL]
            default_canta = [i for i, k in enumerate(canta_keys) if k in (blt.canta_kontrolu or [])]
            secili_canta = st.multiselect(
                "🎒 Çıkış çanta kontrolü", range(len(canta_keys)),
                default=default_canta,
                format_func=lambda i: canta_labels[i],
                key="blt_canta",
            )
            blt.canta_kontrolu = [canta_keys[i] for i in secili_canta]

        # --- 7. MULTIMEDYA (YENI) ---
        styled_section("📷 Fotoğraf & Video", "#7c3aed")
        mc1, mc2 = st.columns(2)
        with mc1:
            yuklenen_fotolar = st.file_uploader(
                "📷 Günün fotoğrafları (en fazla 3)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key="blt_foto_upload",
                help="Çocuğun bugünkü etkinliklerinden fotoğraflar"
            )
            if yuklenen_fotolar:
                import os as _os_blt
                _media_dir = _os_blt.path.join("data", "akademik", "bulten_media")
                _os_blt.makedirs(_media_dir, exist_ok=True)
                _yeni_yollar = []
                for _f_idx, _uf in enumerate(yuklenen_fotolar[:3]):
                    _fname = f"blt_{secili_ogr.id}_{tarih_str}_{_f_idx}_{_uf.name}"
                    _fpath = _os_blt.path.join(_media_dir, _fname)
                    with open(_fpath, "wb") as _of:
                        _of.write(_uf.getbuffer())
                    _yeni_yollar.append(_fpath)
                blt.foto_yollari = _yeni_yollar
                st.caption(f"✅ {len(_yeni_yollar)} fotoğraf yüklendi")
            elif blt.foto_yollari:
                st.caption(f"📎 {len(blt.foto_yollari)} mevcut fotoğraf")
        with mc2:
            yuklenen_video = st.file_uploader(
                "🎥 Kısa video (max 30 sn)",
                type=["mp4", "mov", "webm"],
                key="blt_video_upload",
                help="Etkinlik veya günün öne çıkan anı"
            )
            if yuklenen_video:
                import os as _os_blt2
                _media_dir = _os_blt2.path.join("data", "akademik", "bulten_media")
                _os_blt2.makedirs(_media_dir, exist_ok=True)
                _vname = f"blt_{secili_ogr.id}_{tarih_str}_{yuklenen_video.name}"
                _vpath = _os_blt2.path.join(_media_dir, _vname)
                with open(_vpath, "wb") as _ov:
                    _ov.write(yuklenen_video.getbuffer())
                blt.video_yolu = _vpath
                st.caption(f"✅ Video yüklendi")
            elif blt.video_yolu:
                st.caption(f"📎 Mevcut video: {blt.video_yolu.split('/')[-1]}")

        # --- 8. AKILLI BILDIRIM (YENI) ---
        styled_section("🔔 Akıllı Bildirim", "#dc2626")
        ab1, ab2 = st.columns([1, 3])
        with ab1:
            blt.acil_mi = st.checkbox(
                "🚨 ACİL Mesaj",
                value=blt.acil_mi,
                key="blt_acil",
                help="Veliye anında push bildirim gönder",
            )
        with ab2:
            blt.kisisel_mesaj = st.text_area(
                "⭐ Sadece bu veliye özel mesaj (opsiyonel)",
                value=blt.kisisel_mesaj, height=60,
                placeholder="örn. Ali bugün sizi çok sordu, çok mutluydu",
                key="blt_kisisel",
            )

        # --- 9. ÖĞRETMEN NOTU ---
        styled_section("📝 Öğretmen Notu (Genel)", "#4338ca")
        blt.ogretmen_notu = st.text_area("Öğretmen notu / gözlem", value=blt.ogretmen_notu,
                                          height=80, key="blt_ogr_notu")

        # --- KAYDET ---
        st.markdown("---")
        if st.button("💾 Kaydet", type="primary", use_container_width=True, key="blt_kaydet"):
            from utils.auth import AuthManager
            auth = AuthManager.get_current_user()
            blt.ogretmen_adi = auth.get("name", "")
            blt.student_adi = f"{secili_ogr.ad} {secili_ogr.soyad}"
            blt.sinif = secili_sinif
            blt.sube = secili_sube
            blt.tarih = tarih_str
            store.save_gunluk_bulten(blt)

            # ── AILE BASARI DUVARI'NA OTOMATIK BASARI EKLE ──
            if blt.bugun_basari and blt.bugun_basari.strip():
                try:
                    from models.aile_basari_duvari import BasariDuvariStore, Achievement
                    _bd = BasariDuvariStore()
                    _ach = Achievement(
                        student_id=secili_ogr.id,
                        student_adi=f"{secili_ogr.ad} {secili_ogr.soyad}",
                        sinif=str(secili_sinif),
                        sube=secili_sube,
                        baslik=blt.bugun_basari[:60],
                        aciklama=blt.bugun_basari,
                        kategori="davranis",
                        kaynak="auto_bulten",
                        referans_id=blt.id,
                        ogretmen_adi=auth.get("name", ""),
                        tarih=tarih_str,
                    )
                    _bd.save_achievement(_ach)
                except Exception:
                    pass

            mesajlar = [f"✅ {secili_ogr.ad} {secili_ogr.soyad} için {tarih_str} bülteni kaydedildi!"]
            if blt.bugun_basari:
                mesajlar.append("🌟 Başarı, Aile Başarı Duvarı'na otomatik eklendi.")
            if blt.acil_mi:
                mesajlar.append("🚨 ACİL bildirim veliye gönderildi.")
            for m in mesajlar:
                st.success(m)
            if blt.bugun_basari or blt.acil_mi:
                st.balloons()

    # ============ TOPLU DOLDUR ============
    with ot2:
        styled_section("📋 Toplu Bülten Doldur", "#7c3aed")
        st.caption("Sınıfa ortak alanları bir kez doldurup, öğrenci bazlı farklılaştırma yapın.")

        tf1, tf2 = st.columns(2)
        with tf1:
            toplu_tarih = st.date_input("Tarih", value=date.today(), key="blt_toplu_tarih")
        with tf2:
            toplu_sinif_idx = st.selectbox("Sınıf / Şube", range(len(sinif_opts)),
                                            format_func=lambda i: sinif_labels[i],
                                            key="blt_toplu_sinif")
            toplu_key = sinif_opts[toplu_sinif_idx]
            toplu_sinif = sinif_sube_map[toplu_key]["sinif"]
            toplu_sube = sinif_sube_map[toplu_key]["sube"]
            toplu_ogr = sinif_sube_map[toplu_key]["ogrenciler"]

        toplu_tarih_str = toplu_tarih.strftime("%Y-%m-%d")

        # Ortak etkinlikler
        styled_section("🎨 Ortak Etkinlikler (tüm sınıf)", "#d97706")
        tetk_keys = [k for k, _ in BULTEN_ETKINLIKLER]
        tetk_labels = [v for _, v in BULTEN_ETKINLIKLER]
        ortak_etk = st.multiselect("Bugünkü etkinlikler", range(len(tetk_keys)),
                                    format_func=lambda i: tetk_labels[i],
                                    key="blt_toplu_etk")
        ortak_etk_values = [tetk_keys[i] for i in ortak_etk]

        # Ortak beslenme
        styled_section("🍽️ Ortak Beslenme Menüsü", "#059669")
        st.caption("Menü aynı ise işaretleyin, her öğrencinin ne kadar yediği aşağıda seçilir.")

        st.markdown("---")
        styled_section("👦 Öğrenci Bazlı Giriş", "#2563eb")

        if st.button("📋 Öğrenci Listesini Göster", key="blt_toplu_goster"):
            st.session_state.blt_toplu_gosterildi = True

        if st.session_state.get("blt_toplu_gosterildi"):
            for idx_s, ogr in enumerate(toplu_ogr):
                with st.expander(f"👦 {ogr.ad} {ogr.soyad} ({ogr.numara})", expanded=False):
                    # Mevcut bülten
                    mevcut_t = store.get_gunluk_bultenler(student_id=ogr.id, tarih=toplu_tarih_str)
                    blt_t = mevcut_t[0] if mevcut_t else GunlukBulten(
                        student_id=ogr.id, student_adi=f"{ogr.ad} {ogr.soyad}",
                        tarih=toplu_tarih_str, sinif=toplu_sinif, sube=toplu_sube,
                    )
                    if not blt_t.etkinlikler:
                        blt_t.etkinlikler = ortak_etk_values

                    tc1, tc2, tc3 = st.columns(3)
                    with tc1:
                        d_keys = [""] + [k for k, _ in BULTEN_DUYGU]
                        d_labels = ["Seçiniz"] + [v for _, v in BULTEN_DUYGU]
                        d_idx = d_keys.index(blt_t.duygu) if blt_t.duygu in d_keys else 0
                        blt_t.duygu = d_keys[st.selectbox("Duygu", range(len(d_keys)),
                                                            format_func=lambda i: d_labels[i],
                                                            index=d_idx,
                                                            key=f"blt_t_duygu_{idx_s}")]
                    with tc2:
                        b_keys = [""] + [k for k, _ in BULTEN_BESLENME]
                        b_labels = ["Seçiniz"] + [v for _, v in BULTEN_BESLENME]
                        k_idx = b_keys.index(blt_t.kahvalti) if blt_t.kahvalti in b_keys else 0
                        blt_t.kahvalti = b_keys[st.selectbox("Kahvaltı", range(len(b_keys)),
                                                               format_func=lambda i: b_labels[i],
                                                               index=k_idx,
                                                               key=f"blt_t_kahv_{idx_s}")]
                        o_idx = b_keys.index(blt_t.ogle) if blt_t.ogle in b_keys else 0
                        blt_t.ogle = b_keys[st.selectbox("Öğle", range(len(b_keys)),
                                                           format_func=lambda i: b_labels[i],
                                                           index=o_idx,
                                                           key=f"blt_t_ogle_{idx_s}")]
                    with tc3:
                        blt_t.ogretmen_notu = st.text_input("Not",
                                                             value=blt_t.ogretmen_notu,
                                                             key=f"blt_t_not_{idx_s}")

                    blt_t.one_cikan_beceri = st.text_input("⭐ Öne çıkan kazanım / beceri",
                                                            value=blt_t.one_cikan_beceri,
                                                            key=f"blt_t_beceri_{idx_s}")
                    blt_t.bugun_urun = st.text_input("🎨 Bugün yaptığım ürün / çalışma",
                                                      value=getattr(blt_t, 'bugun_urun', ''),
                                                      key=f"blt_t_urun_{idx_s}")

                    st.session_state[f"blt_toplu_data_{idx_s}"] = blt_t

            st.markdown("---")
            if st.button("💾 Tümünü Kaydet", type="primary", use_container_width=True, key="blt_toplu_kaydet"):
                from utils.auth import AuthManager
                auth = AuthManager.get_current_user()
                saved_count = 0
                for idx_s, ogr in enumerate(toplu_ogr):
                    blt_s = st.session_state.get(f"blt_toplu_data_{idx_s}")
                    if blt_s:
                        blt_s.ogretmen_adi = auth.get("name", "")
                        blt_s.etkinlikler = ortak_etk_values if not blt_s.etkinlikler else blt_s.etkinlikler
                        store.save_gunluk_bulten(blt_s)
                        saved_count += 1
                st.success(f"✅ {saved_count} öğrenci için bülten kaydedildi!")

    # ============ BÜLTEN GEÇMİŞİ ============
    with ot3:
        styled_section("📊 Bülten Geçmişi", "#7c3aed")

        hf1, hf2, hf3 = st.columns(3)
        with hf1:
            gecmis_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=7),
                                        key="blt_gecmis_bas")
        with hf2:
            gecmis_bit = st.date_input("Bitiş", value=date.today(), key="blt_gecmis_bit")
        with hf3:
            gecmis_sinif_idx = st.selectbox("Sınıf / Şube", range(len(sinif_opts)),
                                             format_func=lambda i: sinif_labels[i],
                                             key="blt_gecmis_sinif")
            g_key = sinif_opts[gecmis_sinif_idx]
            g_sinif = sinif_sube_map[g_key]["sinif"]
            g_sube = sinif_sube_map[g_key]["sube"]

        tum_bultenler = store.get_gunluk_bultenler(sinif=g_sinif, sube=g_sube)
        bas_str = gecmis_bas.strftime("%Y-%m-%d")
        bit_str = gecmis_bit.strftime("%Y-%m-%d")
        filtre_bultenler = [b for b in tum_bultenler if bas_str <= b.tarih <= bit_str]
        filtre_bultenler.sort(key=lambda b: b.tarih, reverse=True)

        if not filtre_bultenler:
            st.info("Seçilen tarih aralığında bülten bulunamadı.")
        else:
            st.caption(f"Toplam {len(filtre_bultenler)} bülten")

            # Duygu label helper
            duygu_map = dict(BULTEN_DUYGU)
            beslenme_map = dict(BULTEN_BESLENME)

            rows = []
            for b in filtre_bultenler:
                rows.append({
                    "Tarih": b.tarih,
                    "Öğrenci": b.student_adi,
                    "Duygu": duygu_map.get(b.duygu, "-"),
                    "Kahvaltı": beslenme_map.get(b.kahvalti, "-"),
                    "Öğle": beslenme_map.get(b.ogle, "-"),
                    "Öğretmen Notu": (b.ogretmen_notu[:40] + "...") if len(b.ogretmen_notu) > 40 else b.ogretmen_notu,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            # Detay expander
            for b in filtre_bultenler[:20]:
                with st.expander(f"{b.tarih} — {b.student_adi}"):
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.markdown(f"**Duygu:** {duygu_map.get(b.duygu, '-')}")
                        st.markdown(f"**Arkadaş:** {dict(BULTEN_ARKADAS).get(b.arkadas_iliskisi, '-')}")
                        st.markdown(f"**Kurallar:** {dict(BULTEN_KURALLAR).get(b.sinif_kurallari, '-')}")
                    with d2:
                        etk_map = dict(BULTEN_ETKINLIKLER)
                        etk_str = ", ".join([etk_map.get(e, e) for e in b.etkinlikler]) if b.etkinlikler else "-"
                        st.markdown(f"**Etkinlikler:** {etk_str}")
                        st.markdown(f"**Öne Çıkan:** {b.one_cikan_beceri or '-'}")
                        st.markdown(f"**Ürün/Çalışma:** {getattr(b, 'bugun_urun', '') or '-'}")
                    with d3:
                        st.markdown(f"**Tuvalet:** {dict(BULTEN_TUVALET).get(b.tuvalet, '-')}")
                        st.markdown(f"**Uyku:** {dict(BULTEN_UYKU).get(b.uyku_durumu, '-')} ({b.uyku_suresi} dk)")
                        st.markdown(f"**Sağlık:** {b.saglik_notu or '-'}")
                    if b.ogretmen_notu:
                        st.info(f"📝 {b.ogretmen_notu}")

                    # Sil butonu
                    if st.button("🗑️ Sil", key=f"blt_sil_{b.id}"):
                        store.delete_gunluk_bulten(b.id)
                        st.success("Silindi!")
                        st.rerun()

    # ============ VELİ BİLDİRİMLERİ ============
    with ot4:
        _render_ogretmen_veli_bildirimleri(store, kademe="anaokulu")

    # ============ BELGE & LİNK ============
    with ot5:
        _render_belge_link_gonder(store, sinif_sube_map, sinif_opts, sinif_labels, prefix="oo_")

    # ============ DİJİTAL ÖĞRENME ============
    with ot6:
        styled_section("▶ Dijital Öğrenme — Okul Öncesi YouTube Kanalları", "#7c3aed")
        st.caption("Okul öncesi öğrencileriniz için önerilen ücretsiz eğitim ve eğlence kanalları")

        # --- TÜRKÇE (Çizgi Film / Şarkı / Masal) ---
        st.markdown("#### 🎬 Türkçe — Çizgi Film / Şarkı / Masal")

        _OKUL_ONCESI_YT_TR_CIZGI = (
            ("TRT Çocuk", "TRT Çocuk Resmi Kanalı",
             "https://www.youtube.com/trtcocuk", "#dc2626", "#991b1b", "#fecaca"),
            ("Niloya", "Niloya Çizgi Film",
             "https://www.youtube.com/@niloyatv", "#e11d48", "#be123c", "#fecdd3"),
            ("Kukuli", "Kukuli — Eğlenceli Çizgi Film",
             "https://www.youtube.com/Kukuli", "#ea580c", "#c2410c", "#fed7aa"),
            ("Düşyeri (Pepee vb.)", "Pepee, Leliko ve daha fazlası",
             "https://www.youtube.com/@Dusyeri", "#d97706", "#b45309", "#fef3c7"),
            ("BabyTV Türkçe", "BabyTV Türkçe Çocuk Kanalı",
             "https://www.youtube.com/channel/UCIIxdvCLc0c_iJ8xbtFVPNQ", "#ca8a04", "#a16207", "#fef9c3"),
            ("LooLoo Çocuklar", "LooLoo Çocuk Şarkıları",
             "https://www.youtube.com/@LooLooCocuklar", "#16a34a", "#15803d", "#dcfce7"),
            ("HeyKids Türkçe", "Bebek Şarkıları Türkçe",
             "https://www.youtube.com/channel/UCUwOn6rugJcI6eS-cPUegMA", "#0d9488", "#0f766e", "#ccfbf1"),
            ("Adisebaba Masal", "Masal ve Çocuk Şarkıları",
             "https://www.youtube.com/channel/UCFHuNk4ZyCkWdxKKULyEKKA", "#7c3aed", "#6d28d9", "#ede9fe"),
        )

        cards_html = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px;margin-bottom:20px;">'
        for ad, aciklama, link, r1, r2, rt in _OKUL_ONCESI_YT_TR_CIZGI:
            cards_html += (
                f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
                f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
                f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
                f'transition:transform 0.15s,box-shadow 0.15s;">'
                f'<div style="font-size:11px;position:absolute;top:8px;left:12px;'
                f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
                f'padding:1px 8px;">▶ YouTube</div>'
                f'<div style="font-size:16px;font-weight:800;color:white;'
                f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
                f'<div style="color:{rt};font-size:10px;margin-top:6px;">{aciklama}</div>'
                f'</div></a>'
            )
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # --- TÜRKÇE (Etkinlik / Öğretmen Kanalları) ---
        st.markdown("#### 👩‍🏫 Türkçe — Etkinlik / Öğretmen Kanalları")

        _OKUL_ONCESI_YT_TR_OGRETMEN = (
            ("Buse Öğretmen", "Okul Öncesi Etkinlikler",
             "https://www.youtube.com/c/BuseDurano%C4%9Flu", "#2563eb", "#1d4ed8", "#bfdbfe"),
            ("Yonca Öğretmen", "Okul Öncesi Eğitim",
             "https://www.youtube.com/channel/UCf1Y0wt9IyqZuvcH5Tw07dg", "#7c3aed", "#6d28d9", "#ede9fe"),
            ("AÇEV", "Anne Çocuk Eğitim Vakfı",
             "https://www.youtube.com/channel/UCknrine7khh3jBWiushNOpw", "#059669", "#047857", "#d1fae5"),
        )

        cards_html2 = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;margin-bottom:20px;">'
        for ad, aciklama, link, r1, r2, rt in _OKUL_ONCESI_YT_TR_OGRETMEN:
            cards_html2 += (
                f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
                f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
                f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
                f'transition:transform 0.15s,box-shadow 0.15s;">'
                f'<div style="font-size:11px;position:absolute;top:8px;left:12px;'
                f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
                f'padding:1px 8px;">▶ YouTube</div>'
                f'<div style="font-size:16px;font-weight:800;color:white;'
                f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
                f'<div style="color:{rt};font-size:10px;margin-top:6px;">{aciklama}</div>'
                f'</div></a>'
            )
        cards_html2 += '</div>'
        st.markdown(cards_html2, unsafe_allow_html=True)

        # --- İNGİLİZCE (Güçlü Eğitsel Kanallar) ---
        st.markdown("#### 🌍 İngilizce — Eğitsel Kanallar")

        _OKUL_ONCESI_YT_EN = (
            ("Super Simple Songs", "Çocuk Şarkıları & Eğitim",
             "https://www.youtube.com/user/SuperSimpleSongs", "#dc2626", "#991b1b", "#fecaca"),
            ("Sesame Street", "Susam Sokağı Resmi Kanalı",
             "https://www.youtube.com/sesamestreet", "#16a34a", "#15803d", "#dcfce7"),
            ("Numberblocks", "Sayılar ve Matematik",
             "https://www.youtube.com/channel/UCPlwvN0w4qFSP1FllALB92w", "#2563eb", "#1d4ed8", "#bfdbfe"),
            ("Alphablocks", "Harfler ve Okuma",
             "https://www.youtube.com/channel/UC_qs3c0ehDvZkbiEbOj6Drg", "#7c3aed", "#6d28d9", "#ede9fe"),
            ("PBS KIDS", "PBS Çocuk Eğitim",
             "https://www.youtube.com/channel/UCrNnk0wFBnCS1awGjq_ijGQ", "#0d9488", "#0f766e", "#ccfbf1"),
            ("CBeebies", "BBC Çocuk Kanalı",
             "https://www.youtube.com/cbeebies", "#d97706", "#b45309", "#fef3c7"),
            ("Pinkfong", "Baby Shark & Eğitsel İçerikler",
             "https://www.youtube.com/Pinkfong", "#e11d48", "#be123c", "#fecdd3"),
        )

        cards_html3 = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px;margin-bottom:20px;">'
        for ad, aciklama, link, r1, r2, rt in _OKUL_ONCESI_YT_EN:
            cards_html3 += (
                f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
                f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
                f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
                f'transition:transform 0.15s,box-shadow 0.15s;">'
                f'<div style="font-size:11px;position:absolute;top:8px;left:12px;'
                f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
                f'padding:1px 8px;">▶ YouTube</div>'
                f'<div style="font-size:16px;font-weight:800;color:white;'
                f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
                f'<div style="color:{rt};font-size:10px;margin-top:6px;">{aciklama}</div>'
                f'</div></a>'
            )
        cards_html3 += '</div>'
        st.markdown(cards_html3, unsafe_allow_html=True)

        # ── Dijital Kütüphane Okul Öncesi İçerikler ──
        st.markdown("---")
        styled_section("🎮 Dijital Kütüphane — Okul Öncesi Oyun & Hikayeler", "#7c3aed")
        st.caption("Eğlenceli matematik, bilim, genel yetenek oyunları, MEB hikayeleri ve sınıf etkinlikleri")
        from views.dijital_kutuphane import render_okul_oncesi_dijital_icerik
        render_okul_oncesi_dijital_icerik(prefix="ooi")


# =====================================================================
# İLKOKUL PANELİ
# =====================================================================

def _render_ilkokul(store):
    """Ilkokul (1-4. sinif) — Gunluk Rapor + yonetim paneli."""
    from utils.shared_data import normalize_sinif
    from models.akademik_takip import (
        IlkokulGunlukRapor,
        ILKOKUL_DERSLER, ILKOKUL_DEVAM, ILKOKUL_KATILIM,
        ILKOKUL_DIKKAT, ILKOKUL_SORUMLULUK, ILKOKUL_EVDE,
        BULTEN_BESLENME, BULTEN_TESLIM, BULTEN_ARKADAS, BULTEN_KURALLAR,
    )

    _styled_group_header(
        "İlkokul — Okulumda Bugün",
        "1-4. sınıf günlük iletişim & takip formu + sınıf yönetimi",
        color="#2563eb"
    )

    all_students = store.get_students()
    ilk_siniflar = ["1", "2", "3", "4"]
    ilk_students = [s for s in all_students
                    if normalize_sinif(str(s.sinif)) in ilk_siniflar and s.durum == "aktif"]

    if not ilk_students:
        st.info("Sistemde ilkokul (1-4. sınıf) öğrencisi bulunmuyor. "
                "KOI › İletişim › Sınıf Listeleri'nden ilkokul öğrencisi ekleyin.")
        return

    # Sınıf/Şube kombinasyonları
    sinif_sube_map = {}
    for s in ilk_students:
        ns = normalize_sinif(str(s.sinif))
        key = f"{ns}/{s.sube}"
        if key not in sinif_sube_map:
            sinif_sube_map[key] = {"sinif": ns, "sube": s.sube,
                                    "label": f"{ns}. Sınıf - {s.sube}",
                                    "ogrenciler": []}
        sinif_sube_map[key]["ogrenciler"].append(s)

    sinif_opts = sorted(sinif_sube_map.keys())
    sinif_labels = [sinif_sube_map[k]["label"] for k in sinif_opts]

    # 8 alt sekme
    it_rapor, it_toplu, it_gecmis, it_liste, it_program, it_perf, it_vgb_ilk, it_belge_ilk, it_dijital = st.tabs([
        "  📝 Günlük Rapor Doldur  ",
        "  📋 Toplu Doldur  ",
        "  📊 Rapor Geçmişi  ",
        "  👥 Sınıf Listesi  ",
        "  📅 Ders Programı  ",
        "  📈 Performans Özeti  ",
        "  📩 Veli Bildirimleri  ",
        "  📎 Belge & Link  ",
        "  ▶ Dijital Öğrenme  ",
    ])

    # ============ TEK ÖĞRENCİ GÜNLÜK RAPOR DOLDUR ============
    with it_rapor:
        styled_section("📝 İlkokul Günlük Rapor Doldur", "#2563eb")

        fc1, fc2, fc3 = st.columns([1, 1, 2])
        with fc1:
            tarih = st.date_input("Tarih", value=date.today(), key="ilk_tarih")
        with fc2:
            sec_idx = st.selectbox("Sınıf / Şube", range(len(sinif_opts)),
                                    format_func=lambda i: sinif_labels[i],
                                    key="ilk_sinif_sec")
            sec_key = sinif_opts[sec_idx]
            sec_sinif = sinif_sube_map[sec_key]["sinif"]
            sec_sube = sinif_sube_map[sec_key]["sube"]
        with fc3:
            ogr_list = sinif_sube_map[sec_key]["ogrenciler"]
            ogr_labels = [f"{s.ad} {s.soyad} ({s.numara})" for s in ogr_list]
            ogr_idx = st.selectbox("Öğrenci", range(len(ogr_list)),
                                    format_func=lambda i: ogr_labels[i],
                                    key="ilk_ogr_sec")
            secili_ogr = ogr_list[ogr_idx]

        tarih_str = tarih.strftime("%Y-%m-%d")

        # Mevcut rapor varsa yükle
        mevcut = store.get_ilkokul_gunluk_raporlar(student_id=secili_ogr.id, tarih=tarih_str)
        rpr = mevcut[0] if mevcut else IlkokulGunlukRapor(
            student_id=secili_ogr.id,
            student_adi=f"{secili_ogr.ad} {secili_ogr.soyad}",
            tarih=tarih_str, sinif=sec_sinif, sube=sec_sube,
        )
        if mevcut:
            st.info("Bu tarih için kayıtlı rapor mevcut — düzenleme modunda.")

        st.markdown("---")

        # --- 1) DEVAM & DERS KATILIMI ---
        styled_section("📋 Devam & Ders Katılımı", "#2563eb")
        dk1, dk2, dk3 = st.columns(3)
        with dk1:
            devam_keys = [""] + [k for k, _ in ILKOKUL_DEVAM]
            devam_labels = ["Seçiniz"] + [v for _, v in ILKOKUL_DEVAM]
            devam_idx = devam_keys.index(rpr.devam) if rpr.devam in devam_keys else 0
            rpr.devam = devam_keys[st.selectbox("Devam Durumu", range(len(devam_keys)),
                                                  format_func=lambda i: devam_labels[i],
                                                  index=devam_idx, key="ilk_devam")]
        with dk2:
            kat_keys = [""] + [k for k, _ in ILKOKUL_KATILIM]
            kat_labels = ["Seçiniz"] + [v for _, v in ILKOKUL_KATILIM]
            kat_idx = kat_keys.index(rpr.katilim) if rpr.katilim in kat_keys else 0
            rpr.katilim = kat_keys[st.selectbox("Ders Katılımı", range(len(kat_keys)),
                                                  format_func=lambda i: kat_labels[i],
                                                  index=kat_idx, key="ilk_katilim")]
        with dk3:
            dik_keys = [""] + [k for k, _ in ILKOKUL_DIKKAT]
            dik_labels = ["Seçiniz"] + [v for _, v in ILKOKUL_DIKKAT]
            dik_idx = dik_keys.index(rpr.dikkat) if rpr.dikkat in dik_keys else 0
            rpr.dikkat = dik_keys[st.selectbox("Dikkat", range(len(dik_keys)),
                                                format_func=lambda i: dik_labels[i],
                                                index=dik_idx, key="ilk_dikkat")]

        # Geliş/Çıkış
        gc1, gc2, gc3, gc4 = st.columns(4)
        with gc1:
            rpr.gelis_saati = st.text_input("Geliş Saati", value=rpr.gelis_saati,
                                             placeholder="08:30", key="ilk_gelis")
        with gc2:
            rpr.cikis_saati = st.text_input("Çıkış Saati", value=rpr.cikis_saati,
                                             placeholder="16:00", key="ilk_cikis")
        with gc3:
            servis_opts = ["", "var", "yok"]
            servis_lbl = ["Seçiniz", "Var", "Yok"]
            servis_idx = servis_opts.index(rpr.servis) if rpr.servis in servis_opts else 0
            rpr.servis = servis_opts[st.selectbox("Servis", range(len(servis_opts)),
                                                    format_func=lambda i: servis_lbl[i],
                                                    index=servis_idx, key="ilk_servis")]
        with gc4:
            teslim_keys = [""] + [k for k, _ in BULTEN_TESLIM]
            teslim_lbl = ["Seçiniz"] + [v for _, v in BULTEN_TESLIM]
            teslim_idx = teslim_keys.index(rpr.teslim_eden) if rpr.teslim_eden in teslim_keys else 0
            rpr.teslim_eden = teslim_keys[st.selectbox("Teslim Eden", range(len(teslim_keys)),
                                                         format_func=lambda i: teslim_lbl[i],
                                                         index=teslim_idx, key="ilk_teslim")]

        # --- 2) BESLENME ---
        styled_section("🍽️ Beslenme", "#059669")
        bes_keys = [""] + [k for k, _ in BULTEN_BESLENME]
        bes_labels = ["Seçiniz"] + [v for _, v in BULTEN_BESLENME]
        bc1, bc2 = st.columns([1, 2])
        with bc1:
            bes_idx = bes_keys.index(rpr.beslenme) if rpr.beslenme in bes_keys else 0
            rpr.beslenme = bes_keys[st.selectbox("Kahvaltı / Öğle / Ara Öğün",
                                                   range(len(bes_keys)),
                                                   format_func=lambda i: bes_labels[i],
                                                   index=bes_idx, key="ilk_beslenme")]
        with bc2:
            rpr.beslenme_not = st.text_input("Alerji / Not", value=rpr.beslenme_not,
                                              key="ilk_beslenme_not")

        # --- 3) BUGÜN İŞLENEN DERSLER ---
        styled_section("📚 Bugün İşlenen Dersler", "#7c3aed")
        ders_keys = [k for k, _ in ILKOKUL_DERSLER]
        ders_labels = [v for _, v in ILKOKUL_DERSLER]
        default_ders = [i for i, k in enumerate(ders_keys) if k in rpr.islenen_dersler]
        secili_ders = st.multiselect("Dersler (işaretle)", range(len(ders_keys)),
                                      default=default_ders,
                                      format_func=lambda i: ders_labels[i],
                                      key="ilk_dersler")
        rpr.islenen_dersler = [ders_keys[i] for i in secili_ders]
        rpr.one_cikan_konu = st.text_input("Öne çıkan konu / kazanım",
                                            value=rpr.one_cikan_konu, key="ilk_konu")

        # --- 4) ÖDEV & OKUMA TAKİBİ ---
        styled_section("📖 Ödev & Okuma Takibi", "#d97706")
        od1, od2, od3, od4 = st.columns(4)
        with od1:
            odev_opts = ["", "verildi", "yok"]
            odev_lbl = ["Seçiniz", "Verildi", "Yok"]
            odev_idx = odev_opts.index(rpr.odev_durumu) if rpr.odev_durumu in odev_opts else 0
            rpr.odev_durumu = odev_opts[st.selectbox("Ödev", range(len(odev_opts)),
                                                       format_func=lambda i: odev_lbl[i],
                                                       index=odev_idx, key="ilk_odev")]
        with od2:
            teslim_opts = ["", "tam", "eksik"]
            teslim_lbl2 = ["Seçiniz", "Tam", "Eksik"]
            teslim_idx2 = teslim_opts.index(rpr.odev_teslim) if rpr.odev_teslim in teslim_opts else 0
            rpr.odev_teslim = teslim_opts[st.selectbox("Teslim", range(len(teslim_opts)),
                                                         format_func=lambda i: teslim_lbl2[i],
                                                         index=teslim_idx2, key="ilk_odev_teslim")]
        with od3:
            rpr.okuma_suresi = st.number_input("Okuma (dk)", min_value=0, max_value=180,
                                                value=rpr.okuma_suresi, key="ilk_okuma")
        with od4:
            rpr.kitap_adi = st.text_input("Kitap Adı", value=rpr.kitap_adi, key="ilk_kitap")
        rpr.odev_aciklama = st.text_input("Ödev Açıklaması", value=rpr.odev_aciklama,
                                           key="ilk_odev_acik")

        # --- 5) DAVRANIŞ & SOSYAL GELİŞİM ---
        styled_section("🤝 Davranış & Sosyal Gelişim", "#dc2626")
        dv1, dv2, dv3 = st.columns(3)
        with dv1:
            kur_keys = [""] + [k for k, _ in BULTEN_KURALLAR]
            kur_labels = ["Seçiniz"] + [v for _, v in BULTEN_KURALLAR]
            kur_idx = kur_keys.index(rpr.sinif_kurallari) if rpr.sinif_kurallari in kur_keys else 0
            rpr.sinif_kurallari = kur_keys[st.selectbox("Sınıf Kuralları", range(len(kur_keys)),
                                                          format_func=lambda i: kur_labels[i],
                                                          index=kur_idx, key="ilk_kurallar")]
        with dv2:
            ark_keys = [""] + [k for k, _ in BULTEN_ARKADAS]
            ark_labels = ["Seçiniz"] + [v for _, v in BULTEN_ARKADAS]
            ark_idx = ark_keys.index(rpr.arkadas_iliskisi) if rpr.arkadas_iliskisi in ark_keys else 0
            rpr.arkadas_iliskisi = ark_keys[st.selectbox("Arkadaş İlişkisi", range(len(ark_keys)),
                                                           format_func=lambda i: ark_labels[i],
                                                           index=ark_idx, key="ilk_arkadas")]
        with dv3:
            sor_keys = [""] + [k for k, _ in ILKOKUL_SORUMLULUK]
            sor_labels = ["Seçiniz"] + [v for _, v in ILKOKUL_SORUMLULUK]
            sor_idx = sor_keys.index(rpr.sorumluluk) if rpr.sorumluluk in sor_keys else 0
            rpr.sorumluluk = sor_keys[st.selectbox("Sorumluluk", range(len(sor_keys)),
                                                     format_func=lambda i: sor_labels[i],
                                                     index=sor_idx, key="ilk_sorumluluk")]
        rpr.davranis_notu = st.text_input("Not (opsiyonel)", value=rpr.davranis_notu,
                                           key="ilk_davranis_not")

        # --- 6) AKADEMIK & GELISIM (YENI) ---
        styled_section("🎯 Akademik & Gelişim", "#0d9488")
        ilk_akg1, ilk_akg2 = st.columns(2)
        with ilk_akg1:
            rpr.bugun_ogrendigi = st.text_area(
                "🎯 Bugün öğrendiği yeni şey",
                value=rpr.bugun_ogrendigi, height=70,
                placeholder="örn. Çarpma 7'lere kadar, dünyanın katmanları",
                key="ilk_ogrendigi",
            )
            rpr.bugun_basari = st.text_area(
                "🌟 Bugünkü başarısı (Başarı Duvarı'na otomatik düşer)",
                value=rpr.bugun_basari, height=70,
                placeholder="örn. Sınıf temsilcisi seçildi, kompozisyonu okudu",
                key="ilk_basari",
            )
        with ilk_akg2:
            rpr.yarin_hazirlik = st.text_area(
                "📚 Yarın için hazırlık",
                value=rpr.yarin_hazirlik, height=70,
                placeholder="örn. Matematik kitabı ve cetvel getirin",
                key="ilk_hazirlik",
            )
            from models.akademik_takip import CANTA_KONTROL
            ilk_canta_keys = [k for k, _ in CANTA_KONTROL]
            ilk_canta_labels = [v for _, v in CANTA_KONTROL]
            ilk_default_canta = [i for i, k in enumerate(ilk_canta_keys) if k in (rpr.canta_kontrolu or [])]
            ilk_secili_canta = st.multiselect(
                "🎒 Çıkış çanta kontrolü", range(len(ilk_canta_keys)),
                default=ilk_default_canta,
                format_func=lambda i: ilk_canta_labels[i],
                key="ilk_canta",
            )
            rpr.canta_kontrolu = [ilk_canta_keys[i] for i in ilk_secili_canta]

        # --- 7) MULTIMEDYA (YENI) ---
        styled_section("📷 Fotoğraf & Video", "#7c3aed")
        ilk_mc1, ilk_mc2 = st.columns(2)
        with ilk_mc1:
            ilk_yuk_fotolar = st.file_uploader(
                "📷 Günün fotoğrafları (en fazla 3)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key="ilk_foto_upload",
            )
            if ilk_yuk_fotolar:
                import os as _os_ilk
                _media_dir = _os_ilk.path.join("data", "akademik", "bulten_media")
                _os_ilk.makedirs(_media_dir, exist_ok=True)
                _yeni_yollar = []
                for _f_idx, _uf in enumerate(ilk_yuk_fotolar[:3]):
                    _fname = f"igr_{secili_ogr.id}_{tarih_str}_{_f_idx}_{_uf.name}"
                    _fpath = _os_ilk.path.join(_media_dir, _fname)
                    with open(_fpath, "wb") as _of:
                        _of.write(_uf.getbuffer())
                    _yeni_yollar.append(_fpath)
                rpr.foto_yollari = _yeni_yollar
                st.caption(f"✅ {len(_yeni_yollar)} fotoğraf yüklendi")
            elif rpr.foto_yollari:
                st.caption(f"📎 {len(rpr.foto_yollari)} mevcut fotoğraf")
        with ilk_mc2:
            ilk_yuk_video = st.file_uploader(
                "🎥 Kısa video (max 30 sn)",
                type=["mp4", "mov", "webm"],
                key="ilk_video_upload",
            )
            if ilk_yuk_video:
                import os as _os_ilk2
                _media_dir = _os_ilk2.path.join("data", "akademik", "bulten_media")
                _os_ilk2.makedirs(_media_dir, exist_ok=True)
                _vname = f"igr_{secili_ogr.id}_{tarih_str}_{ilk_yuk_video.name}"
                _vpath = _os_ilk2.path.join(_media_dir, _vname)
                with open(_vpath, "wb") as _ov:
                    _ov.write(ilk_yuk_video.getbuffer())
                rpr.video_yolu = _vpath
                st.caption(f"✅ Video yüklendi")
            elif rpr.video_yolu:
                st.caption(f"📎 Mevcut video: {rpr.video_yolu.split('/')[-1]}")

        # --- 8) AKILLI BILDIRIM (YENI) ---
        styled_section("🔔 Akıllı Bildirim", "#dc2626")
        ilk_ab1, ilk_ab2 = st.columns([1, 3])
        with ilk_ab1:
            rpr.acil_mi = st.checkbox(
                "🚨 ACİL Mesaj",
                value=rpr.acil_mi,
                key="ilk_acil",
                help="Veliye anında push bildirim gönder",
            )
        with ilk_ab2:
            rpr.kisisel_mesaj = st.text_area(
                "⭐ Sadece bu veliye özel mesaj (opsiyonel)",
                value=rpr.kisisel_mesaj, height=60,
                placeholder="örn. Ali bugün matematik soruları çözmede çok hızlıydı",
                key="ilk_kisisel",
            )

        # --- 9) ÖĞRETMEN NOTU ---
        styled_section("📝 Öğretmen Notu (Genel)", "#4338ca")
        rpr.ogretmen_notu = st.text_area("Öğretmen notu / gözlem", value=rpr.ogretmen_notu,
                                          height=80, key="ilk_ogr_notu")

        # --- KAYDET ---
        st.markdown("---")
        if st.button("💾 Kaydet", type="primary", use_container_width=True, key="ilk_kaydet"):
            from utils.auth import AuthManager
            auth = AuthManager.get_current_user()
            rpr.ogretmen_adi = auth.get("name", "")
            rpr.student_adi = f"{secili_ogr.ad} {secili_ogr.soyad}"
            rpr.sinif = sec_sinif
            rpr.sube = sec_sube
            rpr.tarih = tarih_str
            store.save_ilkokul_gunluk_rapor(rpr)

            # ── AILE BASARI DUVARI'NA OTOMATIK BASARI EKLE ──
            if rpr.bugun_basari and rpr.bugun_basari.strip():
                try:
                    from models.aile_basari_duvari import BasariDuvariStore, Achievement
                    _bd = BasariDuvariStore()
                    _ach = Achievement(
                        student_id=secili_ogr.id,
                        student_adi=f"{secili_ogr.ad} {secili_ogr.soyad}",
                        sinif=str(sec_sinif),
                        sube=sec_sube,
                        baslik=rpr.bugun_basari[:60],
                        aciklama=rpr.bugun_basari,
                        kategori="davranis",
                        kaynak="auto_bulten",
                        referans_id=rpr.id,
                        ogretmen_adi=auth.get("name", ""),
                        tarih=tarih_str,
                    )
                    _bd.save_achievement(_ach)
                except Exception:
                    pass

            mesajlar = [f"✅ {secili_ogr.ad} {secili_ogr.soyad} için {tarih_str} raporu kaydedildi!"]
            if rpr.bugun_basari:
                mesajlar.append("🌟 Başarı, Aile Başarı Duvarı'na otomatik eklendi.")
            if rpr.acil_mi:
                mesajlar.append("🚨 ACİL bildirim veliye gönderildi.")
            for m in mesajlar:
                st.success(m)
            if rpr.bugun_basari or rpr.acil_mi:
                st.balloons()

    # ============ TOPLU DOLDUR ============
    with it_toplu:
        styled_section("📋 Toplu Günlük Rapor Doldur", "#2563eb")
        st.caption("Sınıfa ortak alanları bir kez doldurup, öğrenci bazlı farklılaştırma yapın.")

        tf1, tf2 = st.columns(2)
        with tf1:
            toplu_tarih = st.date_input("Tarih", value=date.today(), key="ilk_toplu_tarih")
        with tf2:
            toplu_sinif_idx = st.selectbox("Sınıf / Şube", range(len(sinif_opts)),
                                            format_func=lambda i: sinif_labels[i],
                                            key="ilk_toplu_sinif")
            toplu_key = sinif_opts[toplu_sinif_idx]
            toplu_sinif = sinif_sube_map[toplu_key]["sinif"]
            toplu_sube = sinif_sube_map[toplu_key]["sube"]
            toplu_ogr = sinif_sube_map[toplu_key]["ogrenciler"]

        toplu_tarih_str = toplu_tarih.strftime("%Y-%m-%d")

        # Ortak dersler
        styled_section("📚 Ortak İşlenen Dersler (tüm sınıf)", "#7c3aed")
        t_ders_keys = [k for k, _ in ILKOKUL_DERSLER]
        t_ders_labels = [v for _, v in ILKOKUL_DERSLER]
        ortak_ders = st.multiselect("Bugünkü dersler", range(len(t_ders_keys)),
                                     format_func=lambda i: t_ders_labels[i],
                                     key="ilk_toplu_ders")
        ortak_ders_values = [t_ders_keys[i] for i in ortak_ders]
        ortak_konu = st.text_input("Ortak öne çıkan konu / kazanım", key="ilk_toplu_konu")

        # Ortak ödev
        styled_section("📖 Ortak Ödev Bilgisi", "#d97706")
        to1, to2, to3 = st.columns(3)
        with to1:
            ortak_odev_opts = ["", "verildi", "yok"]
            ortak_odev_lbl = ["Seçiniz", "Verildi", "Yok"]
            ortak_odev = ortak_odev_opts[st.selectbox("Ödev", range(len(ortak_odev_opts)),
                                                        format_func=lambda i: ortak_odev_lbl[i],
                                                        key="ilk_toplu_odev")]
        with to2:
            ortak_odev_acik = st.text_input("Ödev Açıklaması", key="ilk_toplu_odev_acik")
        with to3:
            ortak_kitap = st.text_input("Kitap Adı", key="ilk_toplu_kitap")

        st.markdown("---")
        styled_section("👦 Öğrenci Bazlı Giriş", "#2563eb")

        if st.button("📋 Öğrenci Listesini Göster", key="ilk_toplu_goster"):
            st.session_state.ilk_toplu_gosterildi = True

        if st.session_state.get("ilk_toplu_gosterildi"):
            for idx_s, ogr in enumerate(toplu_ogr):
                with st.expander(f"👦 {ogr.ad} {ogr.soyad} ({ogr.numara})", expanded=False):
                    mevcut_t = store.get_ilkokul_gunluk_raporlar(
                        student_id=ogr.id, tarih=toplu_tarih_str)
                    rpr_t = mevcut_t[0] if mevcut_t else IlkokulGunlukRapor(
                        student_id=ogr.id,
                        student_adi=f"{ogr.ad} {ogr.soyad}",
                        tarih=toplu_tarih_str, sinif=toplu_sinif, sube=toplu_sube,
                    )
                    if not rpr_t.islenen_dersler:
                        rpr_t.islenen_dersler = ortak_ders_values

                    tc1, tc2, tc3 = st.columns(3)
                    with tc1:
                        d_keys = [""] + [k for k, _ in ILKOKUL_DEVAM]
                        d_labels = ["Seçiniz"] + [v for _, v in ILKOKUL_DEVAM]
                        d_idx = d_keys.index(rpr_t.devam) if rpr_t.devam in d_keys else 0
                        rpr_t.devam = d_keys[st.selectbox("Devam", range(len(d_keys)),
                                                            format_func=lambda i: d_labels[i],
                                                            index=d_idx,
                                                            key=f"ilk_t_devam_{idx_s}")]
                    with tc2:
                        b_keys = [""] + [k for k, _ in BULTEN_BESLENME]
                        b_labels = ["Seçiniz"] + [v for _, v in BULTEN_BESLENME]
                        b_idx = b_keys.index(rpr_t.beslenme) if rpr_t.beslenme in b_keys else 0
                        rpr_t.beslenme = b_keys[st.selectbox("Beslenme", range(len(b_keys)),
                                                               format_func=lambda i: b_labels[i],
                                                               index=b_idx,
                                                               key=f"ilk_t_bes_{idx_s}")]
                    with tc3:
                        rpr_t.ogretmen_notu = st.text_input("Not",
                                                             value=rpr_t.ogretmen_notu,
                                                             key=f"ilk_t_not_{idx_s}")

                    st.session_state[f"ilk_toplu_data_{idx_s}"] = rpr_t

            st.markdown("---")
            if st.button("💾 Tümünü Kaydet", type="primary", use_container_width=True,
                         key="ilk_toplu_kaydet"):
                from utils.auth import AuthManager
                auth = AuthManager.get_current_user()
                saved_count = 0
                for idx_s, ogr in enumerate(toplu_ogr):
                    rpr_s = st.session_state.get(f"ilk_toplu_data_{idx_s}")
                    if rpr_s:
                        rpr_s.ogretmen_adi = auth.get("name", "")
                        if not rpr_s.islenen_dersler:
                            rpr_s.islenen_dersler = ortak_ders_values
                        if not rpr_s.one_cikan_konu:
                            rpr_s.one_cikan_konu = ortak_konu
                        if not rpr_s.odev_durumu:
                            rpr_s.odev_durumu = ortak_odev
                        if not rpr_s.odev_aciklama:
                            rpr_s.odev_aciklama = ortak_odev_acik
                        if not rpr_s.kitap_adi:
                            rpr_s.kitap_adi = ortak_kitap
                        store.save_ilkokul_gunluk_rapor(rpr_s)
                        saved_count += 1
                st.success(f"✅ {saved_count} öğrenci için günlük rapor kaydedildi!")

    # ============ RAPOR GEÇMİŞİ ============
    with it_gecmis:
        styled_section("📊 Günlük Rapor Geçmişi", "#2563eb")

        hf1, hf2, hf3 = st.columns(3)
        with hf1:
            gecmis_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=7),
                                        key="ilk_gecmis_bas")
        with hf2:
            gecmis_bit = st.date_input("Bitiş", value=date.today(), key="ilk_gecmis_bit")
        with hf3:
            gecmis_sinif_idx = st.selectbox("Sınıf / Şube", range(len(sinif_opts)),
                                             format_func=lambda i: sinif_labels[i],
                                             key="ilk_gecmis_sinif")
            g_key = sinif_opts[gecmis_sinif_idx]
            g_sinif = sinif_sube_map[g_key]["sinif"]
            g_sube = sinif_sube_map[g_key]["sube"]

        tum_raporlar = store.get_ilkokul_gunluk_raporlar(sinif=g_sinif, sube=g_sube)
        bas_str = gecmis_bas.strftime("%Y-%m-%d")
        bit_str = gecmis_bit.strftime("%Y-%m-%d")
        filtre_raporlar = [r for r in tum_raporlar if bas_str <= r.tarih <= bit_str]
        filtre_raporlar.sort(key=lambda r: r.tarih, reverse=True)

        if not filtre_raporlar:
            st.info("Seçilen tarih aralığında rapor bulunamadı.")
        else:
            st.caption(f"Toplam {len(filtre_raporlar)} rapor")

            devam_map = dict(ILKOKUL_DEVAM)
            katilim_map = dict(ILKOKUL_KATILIM)
            bes_map = dict(BULTEN_BESLENME)
            ders_map = dict(ILKOKUL_DERSLER)

            rows = []
            for r in filtre_raporlar:
                rows.append({
                    "Tarih": r.tarih,
                    "Öğrenci": r.student_adi,
                    "Devam": devam_map.get(r.devam, "-"),
                    "Katılım": katilim_map.get(r.katilim, "-"),
                    "Beslenme": bes_map.get(r.beslenme, "-"),
                    "Öğretmen Notu": (r.ogretmen_notu[:40] + "...") if len(r.ogretmen_notu) > 40 else r.ogretmen_notu,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            for r in filtre_raporlar[:20]:
                with st.expander(f"{r.tarih} — {r.student_adi}"):
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.markdown(f"**Devam:** {devam_map.get(r.devam, '-')}")
                        st.markdown(f"**Katılım:** {katilim_map.get(r.katilim, '-')}")
                        st.markdown(f"**Dikkat:** {dict(ILKOKUL_DIKKAT).get(r.dikkat, '-')}")
                        st.markdown(f"**Beslenme:** {bes_map.get(r.beslenme, '-')}")
                    with d2:
                        d_str = ", ".join([ders_map.get(d, d) for d in r.islenen_dersler]) if r.islenen_dersler else "-"
                        st.markdown(f"**Dersler:** {d_str}")
                        st.markdown(f"**Öne Çıkan:** {r.one_cikan_konu or '-'}")
                        st.markdown(f"**Ödev:** {'Verildi' if r.odev_durumu == 'verildi' else 'Yok' if r.odev_durumu == 'yok' else '-'}")
                        st.markdown(f"**Okuma:** {r.okuma_suresi} dk — {r.kitap_adi or '-'}")
                    with d3:
                        st.markdown(f"**Kurallar:** {dict(BULTEN_KURALLAR).get(r.sinif_kurallari, '-')}")
                        st.markdown(f"**Arkadaş:** {dict(BULTEN_ARKADAS).get(r.arkadas_iliskisi, '-')}")
                        st.markdown(f"**Sorumluluk:** {dict(ILKOKUL_SORUMLULUK).get(r.sorumluluk, '-')}")
                    if r.ogretmen_notu:
                        st.info(f"📝 {r.ogretmen_notu}")

                    if st.button("🗑️ Sil", key=f"ilk_sil_{r.id}"):
                        store.delete_ilkokul_gunluk_rapor(r.id)
                        st.success("Silindi!")
                        st.rerun()

    # ============ SINIF LİSTESİ ============
    with it_liste:
        styled_section("👥 İlkokul Sınıf Listesi", "#2563eb")
        sinif_keys = sorted(sinif_sube_map.keys())
        sinif_labels_ilk = [sinif_sube_map[k]["label"] for k in sinif_keys]
        liste_idx = st.selectbox("Sınıf / Şube", range(len(sinif_keys)),
                                  format_func=lambda i: sinif_labels_ilk[i],
                                  key="ilk_liste_sinif")
        liste_key = sinif_keys[liste_idx]
        ogr_liste = sinif_sube_map[liste_key]["ogrenciler"]

        rows_l = []
        for ogr in sorted(ogr_liste, key=lambda s: (s.numara or "0")):
            rows_l.append({
                "No": ogr.numara,
                "Ad Soyad": f"{ogr.ad} {ogr.soyad}",
                "Cinsiyet": ogr.cinsiyet,
                "Veli": ogr.veli_adi or "-",
                "Veli Tel": ogr.veli_telefon or "-",
            })
        if rows_l:
            st.dataframe(pd.DataFrame(rows_l), use_container_width=True, hide_index=True)
        st.metric("Öğrenci Sayısı", len(ogr_liste))

    # ============ DERS PROGRAMI ============
    with it_program:
        styled_section("📅 Ders Programı", "#059669")
        prog_idx = st.selectbox("Sınıf / Şube", range(len(sinif_keys)),
                                 format_func=lambda i: sinif_labels_ilk[i],
                                 key="ilk_prog_sinif")
        prog_key = sinif_keys[prog_idx]
        prog_sinif = sinif_sube_map[prog_key]["sinif"]
        prog_sube = sinif_sube_map[prog_key]["sube"]

        try:
            sinif_int = int(prog_sinif)
        except ValueError:
            sinif_int = 1
        slots = store.get_schedule(sinif=sinif_int, sube=prog_sube)
        if not slots:
            st.info("Ders programı henüz girilmemiş.")
        else:
            gunler = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]
            max_saat = max(s.ders_saati for s in slots)
            program = {}
            for s in slots:
                program[(s.gun, s.ders_saati)] = s.ders
            rows_p = []
            for saat in range(1, max_saat + 1):
                row = {"Saat": f"{saat}. Ders"}
                for gun in gunler:
                    row[gun] = program.get((gun, saat), "-")
                rows_p.append(row)
            st.dataframe(pd.DataFrame(rows_p), use_container_width=True, hide_index=True)

    # ============ PERFORMANS ÖZETİ ============
    with it_perf:
        styled_section("📈 Performans Özeti", "#d97706")
        perf_idx = st.selectbox("Sınıf / Şube", range(len(sinif_keys)),
                                 format_func=lambda i: sinif_labels_ilk[i],
                                 key="ilk_perf_sinif")
        perf_key = sinif_keys[perf_idx]
        ogr_list_perf = sinif_sube_map[perf_key]["ogrenciler"]

        rows_perf = []
        for ogr in sorted(ogr_list_perf, key=lambda s: (s.numara or "0")):
            notlar = store.get_grades(student_id=ogr.id)
            if notlar:
                ort = sum(n.puan for n in notlar) / len(notlar)
                rows_perf.append({
                    "No": ogr.numara,
                    "Ad Soyad": f"{ogr.ad} {ogr.soyad}",
                    "Not Sayısı": len(notlar),
                    "Ortalama": f"{ort:.1f}",
                })
            else:
                rows_perf.append({
                    "No": ogr.numara,
                    "Ad Soyad": f"{ogr.ad} {ogr.soyad}",
                    "Not Sayısı": 0,
                    "Ortalama": "-",
                })
        if rows_perf:
            st.dataframe(pd.DataFrame(rows_perf), use_container_width=True, hide_index=True)
        else:
            st.info("Not verisi bulunamadı.")

    # ============ VELİ BİLDİRİMLERİ ============
    with it_vgb_ilk:
        _render_ogretmen_veli_bildirimleri(store, kademe="ilkokul")

    # ============ BELGE & LİNK ============
    with it_belge_ilk:
        _render_belge_link_gonder(store, sinif_sube_map, sinif_opts, sinif_labels, prefix="ilk_")

    # ============ DİJİTAL ÖĞRENME ============
    with it_dijital:
        styled_section("▶ Dijital Öğrenme — İlkokul YouTube Kanalları", "#dc2626")
        st.caption("Öğrencileriniz için önerilen ücretsiz eğitim kanalları")

        _ILKOKUL_YT_KANALLAR = (
            ("Tonguç 1. Sınıf", "Tonguç Akademi 1. Sınıf Dersleri",
             "https://www.youtube.com/tonguc1", "#dc2626", "#991b1b", "#fecaca"),
            ("Tonguç 2. Sınıf", "Tonguç Akademi 2. Sınıf Dersleri",
             "https://www.youtube.com/c/tonguc2", "#ea580c", "#c2410c", "#fed7aa"),
            ("Tonguç 3. Sınıf", "Tonguç Akademi 3. Sınıf Dersleri",
             "https://www.youtube.com/channel/UCWKFn2p0uodV8JCdsYtGLIw", "#d97706", "#b45309", "#fef3c7"),
            ("Tonguç 4. Sınıf", "Tonguç Akademi 4. Sınıf Dersleri",
             "https://www.youtube.com/@tonguc4", "#ca8a04", "#a16207", "#fef9c3"),
            ("Sade Öğretmen", "İlkokul Ders Anlatımları",
             "https://www.youtube.com/@Sade_Ogretmen", "#16a34a", "#15803d", "#dcfce7"),
        )

        cards_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;">'
        for ad, aciklama, link, r1, r2, rt in _ILKOKUL_YT_KANALLAR:
            cards_html += (
                f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
                f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
                f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
                f'transition:transform 0.15s,box-shadow 0.15s;">'
                f'<div style="font-size:13px;position:absolute;top:8px;left:12px;'
                f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
                f'padding:1px 8px;">▶ YouTube</div>'
                f'<div style="font-size:18px;font-weight:800;color:white;'
                f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
                f'<div style="color:{rt};font-size:11px;margin-top:6px;">{aciklama}</div>'
                f'</div></a>'
            )
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # ── Dijital Kütüphane İlkokul İçerikler ──
        st.markdown("---")
        styled_section("🎮 Dijital Kütüphane — İlkokul Oyun & Hikayeler", "#dc2626")
        st.caption("Matematik, bilim, genel yetenek, kodlama oyunları, MEB hikayeleri ve kitapları")
        from views.dijital_kutuphane import render_ilkokul_dijital_icerik
        render_ilkokul_dijital_icerik(prefix="ooi_ilk")


# =====================================================================
# ÖĞRETMEN — BELGE & LİNK GÖNDER
# =====================================================================

def _render_belge_link_gonder(store, sinif_sube_map, sinif_opts, sinif_labels, prefix=""):
    """Öğretmen panelinde velilere belge ve link gönderme."""
    import uuid as _uuid
    from models.akademik_takip import OgretmenBelge, BELGE_KATEGORILER

    styled_section("📎 Belge & Link Gönder", "#2563eb")

    if not sinif_opts:
        st.info("Henüz kayıtlı sınıf/şube bulunmuyor.")
        return

    # ── Sınıf / Şube seçimi ──
    secili_idx = st.selectbox(
        "Sınıf / Şube", range(len(sinif_opts)),
        format_func=lambda i: sinif_labels[i],
        key=f"{prefix}belge_sinif_sec",
    )
    secili_key = sinif_opts[secili_idx]
    secili_sinif = sinif_sube_map[secili_key]["sinif"]
    secili_sube = sinif_sube_map[secili_key]["sube"]

    st.markdown("---")

    # ── Yeni Belge/Link Gönder Formu ──
    with st.form(f"{prefix}belge_link_form", clear_on_submit=True):
        st.markdown("##### ✏️ Yeni Belge / Link Gönder")

        baslik = st.text_input("Başlık *", placeholder="Örn: Şubat Ayı Etkinlik Takvimi")

        aciklama = st.text_area("Açıklama", placeholder="Velilere iletmek istediğiniz not...", height=80)


        kat_keys = [k for k, _ in BELGE_KATEGORILER]
        kat_labels = [v for _, v in BELGE_KATEGORILER]
        kat_idx = st.selectbox("Kategori", range(len(kat_keys)),
                               format_func=lambda i: kat_labels[i])
        kategori = kat_keys[kat_idx]

        st.markdown("**📎 Dosya Yükle** _(PDF, Word, Resim, Excel)_")
        dosyalar = st.file_uploader(
            "Dosya seçin", accept_multiple_files=True,
            type=["pdf", "doc", "docx", "jpg", "jpeg", "png", "gif", "xlsx", "xls", "pptx"],
            key=f"{prefix}belge_dosya_yukle", label_visibility="collapsed",
        )

        st.markdown("**🔗 Link Ekle**")
        lc1, lc2 = st.columns([3, 1])
        with lc1:
            link_url = st.text_input("URL", placeholder="https://www.youtube.com/watch?v=...", key=f"{prefix}belge_link_url")
        with lc2:
            link_baslik = st.text_input("Link Başlığı", placeholder="Video adı", key=f"{prefix}belge_link_baslik")

        gonder = st.form_submit_button("💾 Gönder", use_container_width=True, type="primary")

    if gonder:
        if not baslik.strip():
            st.error("Başlık alanı zorunludur.")
        elif not dosyalar and not link_url.strip():
            st.warning("En az bir dosya veya link eklemelisiniz.")
        else:
            # Dosyaları kaydet
            kaydedilen_dosyalar = []
            if dosyalar:
                from utils.security import validate_upload
                _valid_dosyalar = []
                for _f in dosyalar:
                    _ok, _msg = validate_upload(_f, allowed_types=["pdf", "doc", "docx", "jpg", "jpeg", "png", "gif", "xlsx", "xls", "pptx"], max_mb=50)
                    if _ok:
                        _valid_dosyalar.append(_f)
                    else:
                        st.warning(f"⚠️ {_f.name}: {_msg}")
                dosyalar = _valid_dosyalar
            if dosyalar:
                belge_dir = get_data_path("akademik", "belge_dosyalari")
                os.makedirs(belge_dir, exist_ok=True)
                for f in dosyalar:
                    ext = os.path.splitext(f.name)[1].lower()
                    safe_name = f"belge_{_uuid.uuid4().hex[:8]}_{f.name}"
                    dosya_yolu = os.path.join(belge_dir, safe_name)
                    with open(dosya_yolu, "wb") as out:
                        out.write(f.getbuffer())
                    kaydedilen_dosyalar.append({
                        "dosya_adi": f.name,
                        "dosya_yolu": dosya_yolu,
                        "tur": ext.replace(".", ""),
                    })

            # Linkler
            kaydedilen_linkler = []
            if link_url.strip():
                kaydedilen_linkler.append({
                    "url": link_url.strip(),
                    "baslik": link_baslik.strip() or link_url.strip(),
                })

            belge = OgretmenBelge(
                ogretmen_id=st.session_state.get("user_id", ""),
                ogretmen_adi=st.session_state.get("display_name", ""),
                sinif=secili_sinif,
                sube=secili_sube,
                baslik=baslik.strip(),
                aciklama=aciklama.strip(),
                kategori=kategori,
                dosyalar=kaydedilen_dosyalar,
                linkler=kaydedilen_linkler,
            )
            store.save_ogretmen_belge(belge)
            st.success(f"✅ '{baslik.strip()}' başarıyla gönderildi!")
            st.rerun()

    # ── Geçmiş Gönderimler ──
    st.markdown("---")
    styled_section("📋 Geçmiş Gönderimler", "#6b7280")

    belgeler = store.get_ogretmen_belgeleri(sinif=secili_sinif, sube=secili_sube)
    belgeler.sort(key=lambda b: b.tarih, reverse=True)

    if not belgeler:
        st.info("Bu sınıfa henüz belge/link gönderilmemiş.")
    else:
        for b in belgeler:
            kat_map = dict(BELGE_KATEGORILER)
            kat_label = kat_map.get(b.kategori, b.kategori)
            dosya_count = len(b.dosyalar) if b.dosyalar else 0
            link_count = len(b.linkler) if b.linkler else 0

            with st.expander(f"📌 {b.baslik}  —  {b.tarih}  |  {kat_label}  |  📎{dosya_count}  🔗{link_count}"):
                if b.aciklama:
                    st.markdown(b.aciklama)

                # Dosyalar
                if b.dosyalar:
                    st.markdown("**📎 Dosyalar:**")
                    for d in b.dosyalar:
                        dosya_yolu = d.get("dosya_yolu", "")
                        if os.path.exists(dosya_yolu):
                            with open(dosya_yolu, "rb") as fp:
                                st.download_button(
                                    f"📥 {d['dosya_adi']}",
                                    data=fp.read(),
                                    file_name=d["dosya_adi"],
                                    key=f"dl_{b.id}_{d['dosya_adi']}",
                                )
                        else:
                            st.caption(f"⚠️ {d['dosya_adi']} — dosya bulunamadı")

                # Linkler
                if b.linkler:
                    st.markdown("**🔗 Linkler:**")
                    for lnk in b.linkler:
                        st.markdown(f"- [{lnk.get('baslik', lnk['url'])}]({lnk['url']})")

                st.caption(f"Gönderen: {b.ogretmen_adi}  |  {b.created_at[:16]}")

                if st.button("🗑️ Sil", key=f"belge_sil_{b.id}"):
                    # Dosyaları da sil
                    if b.dosyalar:
                        for d in b.dosyalar:
                            yol = d.get("dosya_yolu", "")
                            if os.path.exists(yol):
                                try:
                                    os.remove(yol)
                                except OSError:
                                    pass
                    store.delete_ogretmen_belge(b.id)
                    st.success("Silindi!")
                    st.rerun()


# =====================================================================
# ÖĞRETMEN — VELİ GERİ BİLDİRİMLERİ GÖRÜNTÜLEME
# =====================================================================

def _render_ogretmen_veli_bildirimleri(store, kademe="anaokulu"):
    """Öğretmen panelinde veli geri bildirimlerini görüntüle + okundu/not ekle."""
    from models.akademik_takip import (
        VeliGeriBildirim, VELI_GB_YEMEK, VELI_GB_UYKU, VELI_GB_RUH_HALI,
        VELI_GB_SAGLIK, VELI_GB_EVDE_ANA, VELI_GB_EVDE_ILKOKUL,
    )
    from utils.shared_data import normalize_sinif, KADEME_SINIFLAR

    styled_section("📩 Veli Geri Bildirimleri", "#059669")

    # ── Filtre ──
    f1, f2, f3 = st.columns(3)
    with f1:
        filtre_tarih = st.date_input("Tarih", value=date.today(), key=f"ogr_vgb_tarih_{kademe}")
    with f2:
        filtre_durum = st.selectbox("Durum", ["Tümü", "Okunmadı", "Okundu"],
                                     key=f"ogr_vgb_durum_{kademe}")
    with f3:
        all_students = store.get_students()
        if kademe == "anaokulu":
            ana_siniflar = KADEME_SINIFLAR.get("Anaokulu", ["ana4", "ana5", "anahaz"])
            kademe_students = [s for s in all_students
                               if normalize_sinif(str(s.sinif)) in ana_siniflar and s.durum == "aktif"]
        else:
            ilk_siniflar = KADEME_SINIFLAR.get("Ilkokul", ["1", "2", "3", "4"])
            kademe_students = [s for s in all_students
                               if normalize_sinif(str(s.sinif)) in ilk_siniflar and s.durum == "aktif"]
        sinif_sube_set = sorted({f"{s.sinif}/{s.sube}" for s in kademe_students})
        sinif_opts = ["Tümü"] + sinif_sube_set
        filtre_sinif = st.selectbox("Sınıf/Şube", sinif_opts, key=f"ogr_vgb_sinif_{kademe}")

    tarih_str = filtre_tarih.strftime("%Y-%m-%d")

    okundu_param = None
    if filtre_durum == "Okunmadı":
        okundu_param = False
    elif filtre_durum == "Okundu":
        okundu_param = True

    tum_bildirimler = store.get_veli_geri_bildirimler(tarih=tarih_str, okundu=okundu_param)

    if filtre_sinif != "Tümü":
        _fs, _fsube = filtre_sinif.split("/")
        tum_bildirimler = [b for b in tum_bildirimler if str(b.sinif) == _fs and b.sube == _fsube]

    if kademe == "anaokulu":
        ana_siniflar = KADEME_SINIFLAR.get("Anaokulu", ["ana4", "ana5", "anahaz"])
        tum_bildirimler = [b for b in tum_bildirimler if normalize_sinif(str(b.sinif)) in ana_siniflar]
    else:
        ilk_siniflar = KADEME_SINIFLAR.get("Ilkokul", ["1", "2", "3", "4"])
        tum_bildirimler = [b for b in tum_bildirimler if normalize_sinif(str(b.sinif)) in ilk_siniflar]

    tum_bildirimler.sort(key=lambda b: b.created_at, reverse=True)

    okunmamis = sum(1 for b in tum_bildirimler if not b.okundu)
    toplam = len(tum_bildirimler)

    styled_stat_row([
        ("Toplam Bildirim", str(toplam), "#2563eb", "📩"),
        ("Okunmadı", str(okunmamis), "#ef4444" if okunmamis > 0 else "#22c55e", "🔔"),
        ("Okundu", str(toplam - okunmamis), "#22c55e", "✅"),
    ])

    if not tum_bildirimler:
        st.info(f"📭 {filtre_tarih.strftime('%d.%m.%Y')} tarihinde bildirim bulunamadı.")
        return

    yemek_map = dict(VELI_GB_YEMEK)
    uyku_map = dict(VELI_GB_UYKU)
    ruh_map = dict(VELI_GB_RUH_HALI)
    saglik_map = dict(VELI_GB_SAGLIK)
    evde_map = dict(VELI_GB_EVDE_ANA if kademe == "anaokulu" else VELI_GB_EVDE_ILKOKUL)

    def _yemek_icon(val):
        return {"hepsini_yedi": "✅", "bir_kismini": "🟡", "yemedi": "❌"}.get(val, "⬜")

    def _yemek_renk(val):
        return {"hepsini_yedi": "#22c55e", "bir_kismini": "#f59e0b", "yemedi": "#ef4444"}.get(val, "#94a3b8")

    def _ruh_icon(val):
        return {"mutlu": "😄", "normal": "😐", "huzursuz": "😕", "aglamali": "😢"}.get(val, "⬜")

    def _saglik_renk(val):
        return {"iyi": "#22c55e", "hafif_rahatsiz": "#f59e0b", "hasta": "#ef4444",
                "ilac_kullaniyor": "#dc2626"}.get(val, "#94a3b8")

    for gb in tum_bildirimler:
        border_color = "#ef4444" if not gb.okundu else "#22c55e"
        badge = ('🔴 <span style="color:#ef4444;font-weight:700;">Yeni</span>'
                 if not gb.okundu
                 else '✅ <span style="color:#22c55e;font-weight:700;">Okundu</span>')

        evde_badges = ""
        for e in (gb.evde_yapilan or []):
            lbl = evde_map.get(e, e)
            evde_badges += (f"<span style='display:inline-block;background:#f0fdf4;color:#166534;"
                           f"padding:2px 8px;border-radius:10px;margin:2px;font-size:0.72rem;"
                           f"font-weight:600;border:1px solid #86efac'>{lbl}</span>")

        aksam_not_html = (f'<div style="font-size:0.75rem;color:#92400e;margin-top:2px;">'
                          f'{gb.aksam_yemegi_not}</div>') if gb.aksam_yemegi_not else ""
        kahv_not_html = (f'<div style="font-size:0.75rem;color:#92400e;margin-top:2px;">'
                         f'{gb.kahvalti_not}</div>') if gb.kahvalti_not else ""
        saglik_not_html = (f'<div style="font-size:0.75rem;color:#dc2626;margin-top:2px;">'
                           f'{gb.saglik_notu}</div>') if gb.saglik_notu else ""
        veli_not_html = (f'<div style="background:#111827;padding:8px 12px;border-radius:8px;'
                         f'font-size:0.82rem;margin-bottom:8px;"><b>Veli notu:</b> '
                         f'{gb.veli_notu}</div>') if gb.veli_notu else ""
        evde_html = f'<div style="margin-bottom:8px;">{evde_badges}</div>' if evde_badges else ""

        html = f"""
        <div style="border:2px solid {border_color}40;border-left:5px solid {border_color};
                    border-radius:12px;padding:16px;margin-bottom:12px;background:#fff;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div>
              <span style="font-weight:800;font-size:1rem;color:#0B0F19;">{gb.student_adi}</span>
              <span style="color:#64748b;font-size:0.82rem;margin-left:8px;">{gb.sinif}/{gb.sube}</span>
            </div>
            <div>{badge}</div>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;">
            <div style="background:#fff7ed;padding:6px 12px;border-radius:8px;border-left:3px solid {_yemek_renk(gb.aksam_yemegi)};min-width:120px;">
              <div style="font-size:0.68rem;color:#92400e;">🍽️ Akşam</div>
              <div style="font-weight:700;font-size:0.82rem;">{_yemek_icon(gb.aksam_yemegi)} {yemek_map.get(gb.aksam_yemegi, '—')}</div>
              {aksam_not_html}
            </div>
            <div style="background:#fff7ed;padding:6px 12px;border-radius:8px;border-left:3px solid {_yemek_renk(gb.kahvalti)};min-width:120px;">
              <div style="font-size:0.68rem;color:#92400e;">☕ Kahvaltı</div>
              <div style="font-weight:700;font-size:0.82rem;">{_yemek_icon(gb.kahvalti)} {yemek_map.get(gb.kahvalti, '—')}</div>
              {kahv_not_html}
            </div>
            <div style="background:#eff6ff;padding:6px 12px;border-radius:8px;min-width:120px;">
              <div style="font-size:0.68rem;color:#1d4ed8;">😴 Uyku</div>
              <div style="font-weight:700;font-size:0.82rem;">{uyku_map.get(gb.gece_uykusu, '—')}</div>
              <div style="font-size:0.68rem;color:#64748b;">{gb.uyku_saati} — {gb.uyanma_saati}</div>
            </div>
            <div style="background:#fdf4ff;padding:6px 12px;border-radius:8px;min-width:100px;">
              <div style="font-size:0.68rem;color:#7c3aed;">😊 Sabah</div>
              <div style="font-weight:700;font-size:0.82rem;">{_ruh_icon(gb.sabah_ruh_hali)} {ruh_map.get(gb.sabah_ruh_hali, '—')}</div>
            </div>
            <div style="background:#fef2f2;padding:6px 12px;border-radius:8px;border-left:3px solid {_saglik_renk(gb.saglik_durumu)};min-width:120px;">
              <div style="font-size:0.68rem;color:#dc2626;">🏥 Sağlık</div>
              <div style="font-weight:700;font-size:0.82rem;">{saglik_map.get(gb.saglik_durumu, '—')}</div>
              {saglik_not_html}
            </div>
          </div>
          {evde_html}
          {veli_not_html}
          <div style="font-size:0.72rem;color:#94a3b8;margin-top:6px;">Veli: {gb.veli_adi} | Gönderim: {gb.created_at[:16].replace("T"," ")}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

        ac1, ac2 = st.columns([3, 1])
        with ac1:
            ogr_not = st.text_input("Öğretmen notu",
                                     value=gb.ogretmen_notu,
                                     key=f"ogr_vgb_not_{gb.id}",
                                     placeholder="Veliye yanıt yazın...")
        with ac2:
            st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
            btn_label = "✅ Okundu + Kaydet" if not gb.okundu else "💾 Güncelle"
            if st.button(btn_label, key=f"ogr_vgb_btn_{gb.id}", type="primary"):
                gb.okundu = True
                gb.ogretmen_notu = ogr_not
                store.save_veli_geri_bildirim(gb)
                st.success(f"✅ {gb.student_adi} bildirimi güncellendi!")
                st.rerun()
