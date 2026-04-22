"""
STEM Merkezi -- Ultra Premium Interaktif STEM Ekosistemi
========================================================
Matematik + Fen + Teknoloji + Muhendislik + Robotik + Kodlama + 3D + Maker
"""

from __future__ import annotations
import streamlit as st
from datetime import date, datetime
from utils.ui_common import (
    inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner,
)
from models.stem_merkezi import (
    get_stem_store, STEMProje, MuhendislikGorevi, STEMYarisma, STEMProfil,
    STEM_DALLARI, PROJE_DURUMLARI, PROJE_KATEGORILERI, MUHENDISLIK_ALANLARI,
    ZORLUK_SEVIYELERI, SINIF_GRUPLARI, STEM_XP_ODULLERI, VARSAYILAN_GOREVLER,
)


# ================================================================
#  ANA RENDER
# ================================================================

def render_stem_merkezi():
    inject_common_css()
    try:
        from utils.ui_common import ultra_premium_baslat
        ultra_premium_baslat("steam_merkezi")
    except Exception:
        pass
    try:
        from utils.ui_common import modul_hosgeldin, bildirim_cani
        bildirim_cani(0)
        modul_hosgeldin("steam_merkezi",
            "Matematik + Fen + Teknoloji + Muhendislik + Sanat — 100 STEAM projesi",
            [("100", "Proje"), ("33", "Mat Ekran"), ("33", "Bilisim"), ("31", "Sanat")])
    except Exception:
        pass

    # ─── PREMIUM HERO BANNER (animated gradient + particles) ───
    _stem_premium_hero()

    store = get_stem_store()
    stats = store.get_istatistikler()

    # ─── PREMIUM GLASS METRIC KARTS ───
    _stem_premium_metrics(stats)

    # ─── KOMPAKT TAB CSS ───
    st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-list"] {
        gap: 4px !important;
        flex-wrap: wrap !important;
        padding: 6px 0 !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"] {
        padding: 6px 12px !important;
        min-height: 32px !important;
        height: 32px !important;
        font-size: .73rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg,#1a1f3a,#131825) !important;
        border: 1px solid rgba(124,58,237,.25) !important;
        color: #c4b5fd !important;
        transition: all .2s ease !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg,#231a45,#1e1535) !important;
        border-color: rgba(168,85,247,.6) !important;
        color: #fff !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg,#7C3AED,#a855f7) !important;
        border-color: #c084fc !important;
        color: #fff !important;
        box-shadow: 0 4px 16px rgba(124,58,237,.4) !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-highlight"],
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-border"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # -- Tab Gruplama (30 tab -> 5 grup) --
    _GRP_55828 = {
        "📋 Grup A": [("📊 Panel", 0), ("🌟 Showcase", 1), ("🌳 Skill Tree", 2), ("🧪 Live Lab", 3), ("🏅 Rozetler", 4), ("🔬 Proje", 5), ("🔧 Müh.", 6)],
        "📊 Grup B": [("🏆 Yarış", 7), ("👤 Profil", 8), ("🧮 Mat.", 9), ("💻 Bilişim", 10), ("🎨 Sanat", 11), ("📈 Perf.", 12), ("🤖 AI", 13)],
        "🔧 Grup C": [("🔧 Makerspace", 14), ("🏆 TÜBİTAK", 15), ("📂 Portfolyo", 16), ("🏭 IoT Lab", 17), ("🌍 Proje Tasarım", 18), ("📊 STEAM Endeks", 19), ("🤖 AI Mentor", 20)],
        "📈 Grup D": [("🏗️ Challenge", 21), ("📡 Toplum", 22), ("🧬 STEAM DNA", 23), ("🏭 Kanban", 24), ("🌐 Açık Kaynak", 25), ("🎓 Sertifika", 26), ("🔬 Araştırma", 27)],
        "🎯 Grup E": [("🌍 Etki Ölçüm", 28), ("🤖 Smarti", 29)],
    }
    _sg_55828 = st.radio("", list(_GRP_55828.keys()), horizontal=True, label_visibility="collapsed", key="rg_55828")
    _gt_55828 = _GRP_55828[_sg_55828]
    _aktif_idx_55828 = set(t[1] for t in _gt_55828)
    _tab_names_55828 = [t[0] for t in _gt_55828]
    tabs = st.tabs(_tab_names_55828)
    _tab_real_55828 = {idx: t for idx, t in zip((t[1] for t in _gt_55828), tabs)}

    (t_panel, t_showcase, t_skill, t_lab, t_rozet,
     t_proje, t_muh, t_yar, t_profil, t_mat, t_bil, t_sanat,
     t_perf, t_ai, t_makerspace, t_tubitak, t_portfolyo,
     t_iot, t_tasarim, t_endeks, t_ai_mentor, t_challenge, t_toplum,
     t_dna, t_kanban, t_acik, t_sertifika, t_arastirma, t_etki, t_smarti) = tabs

    with t_panel:
        _tab_dashboard(store, stats)
    with t_showcase:
        _tab_showcase(store)
    with t_skill:
        _tab_skill_tree(store)
    with t_lab:
        _tab_live_lab()
    with t_rozet:
        _tab_rozet_duvari(store)
    with t_proje:
        _tab_projeler(store)
    with t_muh:
        _tab_muhendislik(store)
    with t_yar:
        _tab_yarismalar(store)
    with t_profil:
        _tab_profil(store)
    with t_mat:
        _tab_matematik()
    with t_bil:
        _tab_bilisim()
    with t_sanat:
        _tab_sanat(store)
    with t_perf:
        _tab_performans(store)
    with t_ai:
        _tab_ai_koc(store)

    with t_makerspace:
        try:
            from views._steam_yeni_ozellikler import render_makerspace
            render_makerspace(store)
        except Exception as _e:
            st.error(f"Makerspace yuklenemedi: {_e}")

    with t_tubitak:
        try:
            from views._steam_yeni_ozellikler import render_tubitak_merkez
            render_tubitak_merkez(store)
        except Exception as _e:
            st.error(f"TUBITAK yuklenemedi: {_e}")

    with t_portfolyo:
        try:
            from views._steam_yeni_ozellikler import render_steam_portfolyo
            render_steam_portfolyo(store)
        except Exception as _e:
            st.error(f"Portfolyo yuklenemedi: {_e}")

    with t_iot:
        try:
            from views._steam_super_features import render_iot_lab
            render_iot_lab(store)
        except Exception as _e:
            st.error(f"IoT Lab yuklenemedi: {_e}")

    with t_tasarim:
        try:
            from views._steam_super_features import render_proje_tasarim
            render_proje_tasarim(store)
        except Exception as _e:
            st.error(f"Proje Tasarim yuklenemedi: {_e}")

    with t_endeks:
        try:
            from views._steam_super_features import render_steam_endeks
            render_steam_endeks(store)
        except Exception as _e:
            st.error(f"STEAM Endeks yuklenemedi: {_e}")

    with t_ai_mentor:
        try:
            from views._steam_mega_features import render_ai_steam_mentor
            render_ai_steam_mentor(store)
        except Exception as _e:
            st.error(f"AI Mentor yuklenemedi: {_e}")

    with t_challenge:
        try:
            from views._steam_mega_features import render_steam_challenge
            render_steam_challenge(store)
        except Exception as _e:
            st.error(f"Challenge yuklenemedi: {_e}")

    with t_toplum:
        try:
            from views._steam_mega_features import render_steam_toplum
            render_steam_toplum(store)
        except Exception as _e:
            st.error(f"Toplum yuklenemedi: {_e}")

    with t_dna:
        try:
            from views._steam_zirve_features import render_steam_dna
            render_steam_dna(store)
        except Exception as _e:
            st.error(f"STEAM DNA yuklenemedi: {_e}")

    with t_kanban:
        try:
            from views._steam_zirve_features import render_maker_kanban
            render_maker_kanban(store)
        except Exception as _e:
            st.error(f"Kanban yuklenemedi: {_e}")

    with t_acik:
        try:
            from views._steam_zirve_features import render_acik_kaynak
            render_acik_kaynak(store)
        except Exception as _e:
            st.error(f"Acik Kaynak yuklenemedi: {_e}")

    with t_sertifika:
        try:
            from views._steam_final_features import render_steam_sertifika
            render_steam_sertifika(store)
        except Exception as _e:
            st.error(f"Sertifika yuklenemedi: {_e}")

    with t_arastirma:
        try:
            from views._steam_final_features import render_arastirma_gunlugu
            render_arastirma_gunlugu(store)
        except Exception as _e:
            st.error(f"Arastirma yuklenemedi: {_e}")

    with t_etki:
        try:
            from views._steam_final_features import render_etki_olcumu
            render_etki_olcumu(store)
        except Exception as _e:
            st.error(f"Etki Olcum yuklenemedi: {_e}")

    with t_smarti:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="stem_merkezi")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_stem_merkezi")
            if st.button("Gönder", key="smarti_send_stem_merkezi"):
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
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. stem_merkezi modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


# ================================================================
#  TAB 1 — Dashboard
# ================================================================

def _tab_dashboard(store, stats: dict):
    styled_section("STEM Merkezi Genel Bakis", "#7C3AED")

    c1, c2 = st.columns(2)

    with c1:
        styled_section("Proje Durum Dagilimi", "#6366F1")
        projeler = store.load_list("projeler")
        if projeler:
            durum_sayac: dict[str, int] = {}
            for p in projeler:
                d = p.get("durum", "fikir")
                durum_sayac[d] = durum_sayac.get(d, 0) + 1
            for durum, sayi in durum_sayac.items():
                pct = round(sayi / len(projeler) * 100)
                st.progress(pct / 100, text=f"{durum.title()}: {sayi} (%{pct})")
        else:
            styled_info_banner("Henuz proje bulunmuyor. STEM Projeleri sekmesinden yeni proje ekleyin.", "info")

    with c2:
        styled_section("Dal Dagilimi", "#059669")
        dal_dag = stats.get("dal_dagilimi", {})
        if dal_dag:
            for dal, sayi in sorted(dal_dag.items(), key=lambda x: -x[1]):
                st.markdown(f"**{dal}**: {sayi} proje")
        else:
            styled_info_banner("Henuz dal dagilimi verisi yok.", "info")

    st.divider()

    c3, c4 = st.columns(2)

    with c3:
        styled_section("Son Projeler", "#2563EB")
        son = sorted(projeler, key=lambda x: x.get("olusturma_tarihi", ""), reverse=True)[:5] if projeler else []
        if son:
            for p in son:
                dallar = ", ".join(p.get("stem_dallari", [])[:3])
                st.markdown(
                    f"- **{p.get('baslik', '-')}** — {p.get('durum', '').title()} | {dallar}"
                )
        else:
            st.caption("Proje yok.")

    with c4:
        styled_section("Yarisma Takvimi", "#D97706")
        yarismalar = store.load_list("yarismalar")
        gelecek = [
            y for y in yarismalar
            if y.get("tarih", "") >= date.today().isoformat()
        ]
        gelecek.sort(key=lambda x: x.get("tarih", ""))
        if gelecek[:5]:
            for y in gelecek[:5]:
                st.markdown(f"- **{y.get('yarisma_adi', '-')}** — {y.get('tarih', '')} | {y.get('organizator', '')}")
        else:
            st.caption("Yaklasan yarisma yok.")


# ================================================================
#  TAB 2 — STEM Projeleri
# ================================================================

def _tab_projeler(store):
    styled_section("Yeni STEM Projesi", "#7C3AED")

    with st.form("stem_yeni_proje", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            baslik = st.text_input("Proje Basligi*")
            kategori = st.selectbox("Kategori", PROJE_KATEGORILERI)
            zorluk = st.selectbox("Zorluk", ZORLUK_SEVIYELERI, index=1)
        with c2:
            dallar = st.multiselect("STEM Dallari*", STEM_DALLARI)
            sinif = st.number_input("Sinif", 1, 12, 5)
            sube = st.text_input("Sube", "A")

        aciklama = st.text_area("Aciklama")

        # Ogrenci secimi
        ogrenci_adlari_str = st.text_input("Ogrenci Adlari (virgul ile ayirin)")

        submitted = st.form_submit_button("Proje Olustur", type="primary")
        if submitted:
            if not baslik or not dallar:
                st.error("Baslik ve en az bir STEM dali zorunludur.")
            else:
                ogrenci_list = [a.strip() for a in ogrenci_adlari_str.split(",") if a.strip()] if ogrenci_adlari_str else []
                proje = STEMProje(
                    baslik=baslik,
                    aciklama=aciklama,
                    kategori=kategori,
                    stem_dallari=dallar,
                    sinif=sinif,
                    sube=sube,
                    ogrenci_adlari=ogrenci_list,
                    zorluk=zorluk,
                )
                store.add_item("projeler", proje.to_dict())
                st.success(f"Proje '{baslik}' olusturuldu!")
                st.rerun()

    # Mevcut projeler
    styled_section("Mevcut Projeler", "#6366F1")

    projeler = store.load_list("projeler")
    if not projeler:
        styled_info_banner("Henuz proje yok.", "info")
        return

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_durum = st.selectbox("Durum Filtre", ["Tumu"] + PROJE_DURUMLARI, key="sprj_f_durum")
    with fc2:
        f_kat = st.selectbox("Kategori Filtre", ["Tumu"] + PROJE_KATEGORILERI, key="sprj_f_kat")
    with fc3:
        f_dal = st.selectbox("Dal Filtre", ["Tumu"] + STEM_DALLARI, key="sprj_f_dal")

    filtered = projeler
    if f_durum != "Tumu":
        filtered = [p for p in filtered if p.get("durum") == f_durum]
    if f_kat != "Tumu":
        filtered = [p for p in filtered if p.get("kategori") == f_kat]
    if f_dal != "Tumu":
        filtered = [p for p in filtered if f_dal in (p.get("stem_dallari") or [])]

    for proje in filtered:
        with st.expander(f"{proje.get('baslik', '-')} — {proje.get('durum', '').title()} | {proje.get('kategori', '')}"):
            st.markdown(f"**Aciklama:** {proje.get('aciklama', '-')}")
            st.markdown(f"**Dallar:** {', '.join(proje.get('stem_dallari', []))}")
            st.markdown(f"**Zorluk:** {proje.get('zorluk', '-')} | **Sinif:** {proje.get('sinif', '-')}/{proje.get('sube', '-')}")
            ogrenciler = proje.get("ogrenci_adlari", [])
            if ogrenciler:
                st.markdown(f"**Ogrenciler:** {', '.join(ogrenciler)}")

            # Asama gecisi
            mevcut_durum = proje.get("durum", "fikir")
            idx = PROJE_DURUMLARI.index(mevcut_durum) if mevcut_durum in PROJE_DURUMLARI else 0
            yeni_durum = st.selectbox(
                "Durum Degistir", PROJE_DURUMLARI, index=idx,
                key=f"durum_{proje.get('id')}",
            )
            if yeni_durum != mevcut_durum:
                if st.button("Durumu Guncelle", key=f"btn_durum_{proje.get('id')}"):
                    store.update_item("projeler", proje["id"], {"durum": yeni_durum})
                    st.success("Durum guncellendi!")
                    st.rerun()

            # Degerlendirme
            st.markdown("---")
            st.markdown("**Degerlendirme:**")
            deg = proje.get("degerlendirme", {})
            dc1, dc2, dc3, dc4 = st.columns(4)
            with dc1:
                st.metric("Yaraticilik", deg.get("yaraticilik", "-"))
            with dc2:
                st.metric("Teknik", deg.get("teknik", "-"))
            with dc3:
                st.metric("Sunum", deg.get("sunum", "-"))
            with dc4:
                st.metric("Takim", deg.get("takim", "-"))

            # Silme
            if st.button("Projeyi Sil", key=f"sil_{proje.get('id')}", type="secondary"):
                store.delete_item("projeler", proje["id"])
                st.success("Proje silindi.")
                st.rerun()


# ================================================================
#  TAB 3 — Muhendislik Atolyesi
# ================================================================

def _tab_muhendislik(store):
    styled_section("Muhendislik Tasarim Gorevleri", "#D97706")

    # Filtreler
    fc1, fc2 = st.columns(2)
    with fc1:
        f_zorluk = st.selectbox("Zorluk Filtre", ["Tumu"] + ZORLUK_SEVIYELERI, key="mhg_f_zor")
    with fc2:
        f_sinif = st.selectbox("Sinif Grubu Filtre", ["Tumu"] + list(SINIF_GRUPLARI.keys()), key="mhg_f_sinif")

    # Varsayilan gorevler + kayitli gorevler birlestir
    kayitli = store.load_list("gorevler")
    kayitli_basliklar = {g.get("baslik") for g in kayitli}
    tum_gorevler = list(kayitli)
    for vg in VARSAYILAN_GOREVLER:
        if vg["baslik"] not in kayitli_basliklar:
            tum_gorevler.append(vg)

    # Filtrele
    if f_zorluk != "Tumu":
        tum_gorevler = [g for g in tum_gorevler if g.get("zorluk") == f_zorluk]
    if f_sinif != "Tumu":
        tum_gorevler = [g for g in tum_gorevler if g.get("sinif_grubu") == f_sinif]

    if not tum_gorevler:
        styled_info_banner("Filtrelerinize uygun gorev bulunamadi.", "warning")
    else:
        st.caption(f"{len(tum_gorevler)} gorev listeleniyor")

    for gorev in tum_gorevler:
        with st.expander(f"{gorev.get('baslik', '-')} — {gorev.get('zorluk', '')} | {gorev.get('sinif_grubu', '')} | {gorev.get('alan', '')}"):
            st.markdown(f"**Aciklama:** {gorev.get('aciklama', '-')}")
            malzemeler = gorev.get("malzemeler", [])
            if malzemeler:
                st.markdown("**Malzemeler:** " + ", ".join(malzemeler))
            adimlar = gorev.get("adimlar", [])
            if adimlar:
                st.markdown("**Adimlar:**")
                for adim in adimlar:
                    if isinstance(adim, dict):
                        st.markdown(f"  {adim.get('adim_no', '-')}. {adim.get('aciklama', '')}")
                    else:
                        st.markdown(f"  - {adim}")
            kazanimlar = gorev.get("kazanimlar", [])
            if kazanimlar:
                st.markdown("**Kazanimlar:** " + ", ".join(kazanimlar))
            sure = gorev.get("sure_dk", 0)
            if sure:
                st.markdown(f"**Tahmini Sure:** {sure} dakika")

            # AI ile adim adim yapilis uret
            ai_key = f"mhg_ai_adim_{gorev.get('baslik', '')}"
            if ai_key in st.session_state:
                st.markdown("---")
                st.markdown("**Adım Adım Yapılış Talimatı (AI):**")
                st.markdown(st.session_state[ai_key])
            if st.button("🤖 Yapılış Adımlarını AI ile Üret", key=f"mhg_ai_btn_{gorev.get('id', gorev.get('baslik', ''))}"):
                with st.spinner("AI yapılış talimatı oluşturuyor..."):
                    try:
                        from openai import OpenAI
                        import os as _os
                        _api = _os.environ.get("OPENAI_API_KEY", "")
                        if _api:
                            _cl = OpenAI(api_key=_api)
                            _prompt = (
                                f"Asagidaki STEAM projesinin adim adim yapilisini yaz.\n"
                                f"Proje: {gorev.get('baslik', '')}\n"
                                f"Aciklama: {gorev.get('aciklama', '')}\n"
                                f"Malzemeler: {', '.join(gorev.get('malzemeler', []))}\n"
                                f"Zorluk: {gorev.get('zorluk', '')}\n"
                                f"Sinif Grubu: {gorev.get('sinif_grubu', '')}\n\n"
                                f"Turkce, numarali adimlar halinde, her adimda ne yapilacagini ve neden yapildigini acikla. "
                                f"Guvenlik uyarilari ekle. Ogretmen ve ogrenci icin anlasilir yaz."
                            )
                            _resp = _cl.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "STEAM egitim uzmanisin. Ogrencilere yonelik adim adim proje yapilis talimati yaziyorsun. Her adimi numaralandir, net ve guvenli yaz."},
                                    {"role": "user", "content": _prompt},
                                ],
                                temperature=0.7, max_tokens=800,
                            )
                            st.session_state[ai_key] = _resp.choices[0].message.content
                            st.rerun()
                        else:
                            st.warning("OpenAI API anahtari tanimli degil.")
                    except Exception as _e:
                        st.error(f"AI hatasi: {_e}")

            st.markdown("---")

            # Gorevi baslat -> proje olustur
            if st.button("Gorevi Baslat (Proje Olustur)", key=f"mhg_baslat_{gorev.get('id', gorev.get('baslik', ''))}"):
                proje = STEMProje(
                    baslik=f"[Muhendislik] {gorev.get('baslik', '')}",
                    aciklama=gorev.get("aciklama", ""),
                    kategori="Muhendislik Tasarim",
                    stem_dallari=["Muhendislik"],
                    zorluk=gorev.get("zorluk", "Orta"),
                    durum="planlama",
                )
                store.add_item("projeler", proje.to_dict())
                st.success(f"'{gorev.get('baslik', '')}' icin proje olusturuldu!")
                st.rerun()

    # Yeni gorev ekleme
    st.divider()
    styled_section("Yeni Muhendislik Gorevi Ekle", "#059669")

    with st.form("mhg_yeni_gorev", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            g_baslik = st.text_input("Gorev Basligi*")
            g_alan = st.selectbox("Muhendislik Alani", MUHENDISLIK_ALANLARI)
            g_zorluk = st.selectbox("Zorluk", ZORLUK_SEVIYELERI, index=1, key="mhg_new_zor")
        with c2:
            g_sinif = st.selectbox("Sinif Grubu", list(SINIF_GRUPLARI.keys()), key="mhg_new_sinif")
            g_sure = st.number_input("Sure (dk)", 10, 300, 45)
        g_aciklama = st.text_area("Aciklama")
        g_malzeme = st.text_input("Malzemeler (virgul ile)")
        g_kazanim = st.text_input("Kazanimlar (virgul ile)")

        if st.form_submit_button("Gorev Ekle", type="primary"):
            if not g_baslik:
                st.error("Baslik zorunlu.")
            else:
                gorev_obj = MuhendislikGorevi(
                    baslik=g_baslik,
                    aciklama=g_aciklama,
                    alan=g_alan,
                    zorluk=g_zorluk,
                    sinif_grubu=g_sinif,
                    sure_dk=g_sure,
                    malzemeler=[m.strip() for m in g_malzeme.split(",") if m.strip()],
                    kazanimlar=[k.strip() for k in g_kazanim.split(",") if k.strip()],
                )
                store.add_item("gorevler", gorev_obj.to_dict())
                st.success(f"Gorev '{g_baslik}' eklendi!")
                st.rerun()


# ================================================================
#  TAB 4 — Yarismalar
# ================================================================

def _tab_yarismalar(store):
    styled_section("Yarisma Takvimi", "#059669")

    yarismalar = store.load_list("yarismalar")
    gelecek = [y for y in yarismalar if y.get("tarih", "") >= date.today().isoformat()]
    gecmis = [y for y in yarismalar if y.get("tarih", "") < date.today().isoformat()]

    if gelecek:
        gelecek.sort(key=lambda x: x.get("tarih", ""))
        for y in gelecek:
            with st.expander(f"📅 {y.get('yarisma_adi', '-')} — {y.get('tarih', '')} | {y.get('organizator', '')}"):
                st.markdown(f"**Kategori:** {y.get('kategori', '-')}")
                st.markdown(f"**Yer:** {y.get('yer', '-')}")
                katilimcilar = y.get("katilimci_adlari", [])
                if katilimcilar:
                    st.markdown(f"**Katilimcilar:** {', '.join(katilimcilar)}")
                sonuc = y.get("sonuc", "")
                if sonuc:
                    st.markdown(f"**Sonuc:** {sonuc}")
                notlar = y.get("notlar", "")
                if notlar:
                    st.markdown(f"**Notlar:** {notlar}")
                # Silme
                if st.button("Yarismayi Sil", key=f"ydel_{y.get('id', '')}"):
                    store.delete_item("yarismalar", y["id"])
                    st.success("Yarisma silindi.")
                    st.rerun()
    else:
        styled_info_banner("Yaklasan yarisma bulunmuyor.", "info")

    if gecmis:
        styled_section("Gecmis Yarismalar", "#6366F1")
        for y in sorted(gecmis, key=lambda x: x.get("tarih", ""), reverse=True)[:10]:
            sonuc_txt = y.get("sonuc", "Sonuc girilmedi")
            st.markdown(f"- **{y.get('yarisma_adi', '-')}** — {y.get('tarih', '')} | {y.get('organizator', '')} | Sonuc: {sonuc_txt}")

    # Yeni yarisma formu
    st.divider()
    styled_section("Yeni Yarisma Kaydi", "#D97706")

    with st.form("stem_yeni_yarisma", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            y_adi = st.text_input("Yarisma Adi*")
            y_org = st.selectbox("Organizator", ["TUBiTAK", "Okul Ici", "Bolgesel", "Ulusal", "Uluslararasi", "Diger"])
            y_kat = st.selectbox("Kategori", PROJE_KATEGORILERI, key="yar_kat")
        with c2:
            y_tarih = st.date_input("Tarih", value=date.today(), key="yar_tarih")
            y_yer = st.text_input("Yer")
        y_katilimci = st.text_input("Katilimci Adlari (virgul ile)")
        y_not = st.text_area("Notlar", key="yar_not")

        if st.form_submit_button("Yarisma Kaydet", type="primary"):
            if not y_adi:
                st.error("Yarisma adi zorunlu.")
            else:
                yarisma = STEMYarisma(
                    yarisma_adi=y_adi,
                    organizator=y_org,
                    kategori=y_kat,
                    tarih=y_tarih.isoformat(),
                    yer=y_yer,
                    katilimci_adlari=[k.strip() for k in y_katilimci.split(",") if k.strip()],
                    notlar=y_not,
                )
                store.add_item("yarismalar", yarisma.to_dict())
                st.success(f"'{y_adi}' yarisma kaydedildi!")
                st.rerun()

    # Sonuc girisi
    if yarismalar:
        st.divider()
        styled_section("Sonuc Girisi", "#7C3AED")
        yarisma_sec = st.selectbox(
            "Yarisma Sec",
            [f"{y.get('yarisma_adi', '-')} ({y.get('tarih', '')})" for y in yarismalar],
            key="yar_sonuc_sec",
        )
        idx = [f"{y.get('yarisma_adi', '-')} ({y.get('tarih', '')})" for y in yarismalar].index(yarisma_sec) if yarisma_sec else 0
        secili = yarismalar[idx] if yarismalar else None
        if secili:
            sonuc = st.selectbox("Sonuc", ["", "Birincilik", "Ikincilik", "Ucunculuk", "Mansiyon", "Ozel Odul", "Katilim"], key="yar_sonuc_val")
            puan = st.number_input("Puan", 0.0, 100.0, 0.0, key="yar_sonuc_puan")
            if st.button("Sonuc Kaydet", key="yar_sonuc_btn"):
                store.update_item("yarismalar", secili["id"], {"sonuc": sonuc, "puan": puan})
                st.success("Sonuc kaydedildi!")
                st.rerun()


# ================================================================
#  TAB 5 — Ogrenci STEM Profili
# ================================================================

def _tab_profil(store):
    styled_section("Ogrenci STEM Profili", "#2563EB")

    # Ogrenci secimi
    try:
        from utils.shared_data import get_student_display_options
        ogrenci_opts = get_student_display_options()
    except Exception:
        ogrenci_opts = {}

    if ogrenci_opts:
        secim = st.selectbox("Ogrenci Sec", list(ogrenci_opts.keys()), key="stem_ogr_sec")
        student_id = ogrenci_opts.get(secim, "")
    else:
        student_id = st.text_input("Ogrenci ID", key="stem_ogr_id")
        secim = student_id

    if not student_id:
        styled_info_banner("Profil goruntuleme icin bir ogrenci secin.", "info")
        return

    birlesik = store.get_birlesik_stem_profil(student_id)

    # Genel ozet
    styled_section(f"{secim} -- Birlesik STEM Profili", "#7C3AED")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Proje", birlesik.get("toplam_proje", 0))
    with c2:
        st.metric("Tamamlanan", birlesik.get("tamamlanan_proje", 0))
    with c3:
        st.metric("Yarisma", birlesik.get("yarisma_sayisi", 0))
    with c4:
        stem_p = birlesik.get("stem_profil", {})
        st.metric("STEM XP", stem_p.get("stem_xp", 0))

    # Dal bazli radar (basit HTML tablo gosterimi)
    styled_section("Dal Bazli Skorlar", "#059669")
    mat = birlesik.get("matematik", {})
    bil = birlesik.get("bilisim", {})
    snt = birlesik.get("sanat", {})
    sp = birlesik.get("stem_profil", {})

    dallar_skor = {
        "Matematik": mat.get("genel_skor", sp.get("matematik_skoru", 0)),
        "Fen Bilimleri": sp.get("fen_skoru", 0),
        "Teknoloji": sp.get("teknoloji_skoru", 0),
        "Muhendislik": sp.get("muhendislik_skoru", 0),
        "Bilisim": bil.get("genel_skor", 0) if isinstance(bil, dict) else 0,
        "Sanat": snt.get("genel_skor", 0) if isinstance(snt, dict) else 0,
    }

    for dal, skor in dallar_skor.items():
        skor_val = float(skor) if skor else 0
        pct = min(skor_val / 100, 1.0)
        st.progress(pct, text=f"{dal}: {skor_val:.0f}/100")

    # Rozetler
    rozetler = sp.get("rozetler", [])
    if rozetler:
        styled_section("Rozetler", "#D97706")
        st.markdown(" | ".join([f"🏅 {r}" for r in rozetler]))

    # Guclu / Gelistirilecek alanlar
    c5, c6 = st.columns(2)
    with c5:
        styled_section("Guclu Alanlar", "#059669")
        guclu = sp.get("guclu_alanlar", [])
        if guclu:
            for g in guclu:
                st.markdown(f"- {g}")
        else:
            st.caption("Henuz belirlenmedi.")
    with c6:
        styled_section("Gelistirilecek Alanlar", "#ef4444")
        gelistir = sp.get("gelistirilecek_alanlar", [])
        if gelistir:
            for g in gelistir:
                st.markdown(f"- {g}")
        else:
            st.caption("Henuz belirlenmedi.")

    # Projeler listesi
    projeler = birlesik.get("projeler", [])
    if projeler:
        styled_section("Katildigi Projeler", "#6366F1")
        for p in projeler:
            st.markdown(f"- **{p.get('baslik', '-')}** — {p.get('durum', '').title()} | {', '.join(p.get('stem_dallari', []))}")


# ================================================================
#  TAB 6 — Matematik Koyu
# ================================================================

def _tab_matematik():
    try:
        from views.matematik_dunyasi import render_matematik_dunyasi
        render_matematik_dunyasi()
    except Exception as e:
        st.error(f"Matematik Koyu yuklenemedi: {e}")
        styled_info_banner(
            "Matematik Koyu modulu aktif degil veya yuklenirken hata olustu.",
            "warning",
        )


# ================================================================
#  TAB 7 — Bilisim Vadisi
# ================================================================

def _tab_bilisim():
    try:
        from views.bilisim_vadisi import render_bilisim_vadisi
        render_bilisim_vadisi()
    except Exception as e:
        st.error(f"Bilisim Vadisi yuklenemedi: {e}")
        styled_info_banner(
            "Bilisim Vadisi modulu aktif degil veya yuklenirken hata olustu.",
            "warning",
        )


# ================================================================
#  TAB 8 — Sanat Sokağı (STEAM entegre)
# ================================================================

def _tab_sanat(store):
    """Sanat Sokağı modülünü doğrudan STEAM içinde çalıştırır."""
    try:
        from views.sanat_sokagi import render_sanat_sokagi
        render_sanat_sokagi()
    except Exception as e:
        st.error(f"Sanat Sokağı yüklenemedi: {e}")
        styled_info_banner(
            "Sanat Sokağı modülü aktif değil veya yüklenirken hata oluştu.",
            "warning",
        )


# ================================================================
#  TAB 9 — Performans
# ================================================================

def _tab_performans(store):
    styled_section("STEM Merkezi Performans Olcumu", "#2563EB")

    perf = store.performans_olc()

    # Genel skor
    skor = perf.get("genel_performans_skoru", 0)
    durum = perf.get("genel_durum", "belirsiz")
    renk_map = {"basarili": "#059669", "iyi": "#2563EB", "gelistirilmeli": "#D97706", "kritik": "#ef4444"}
    renk = renk_map.get(durum, "#6366F1")

    styled_stat_row([
        ("Genel Skor", f"%{skor}", renk, "📊"),
        ("Durum", durum.title(), renk, "📋"),
        ("Olcum", perf.get("olcum_tarihi", "")[:10], "#6366F1", "📅"),
    ])

    # KPI tablosu
    styled_section("KPI Detaylari", "#7C3AED")
    gap = perf.get("gap_analiz", {})

    durum_icon = {"hedefte": "🟢", "yakin": "🟡", "geride": "🟠", "kritik": "🔴"}

    for kpi, d in gap.items():
        icon = durum_icon.get(d.get("durum", ""), "⚪")
        hedef = d.get("hedef", 0)
        gercek = d.get("gerceklesen", 0)
        oran = d.get("gerceklesme_orani", 0)
        aciklama = d.get("aciklama", "")

        with st.expander(f"{icon} {aciklama} — %{oran} ({d.get('durum', '').title()})"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Hedef", f"{hedef} {d.get('birim', '')}")
            with c2:
                st.metric("Gerceklesen", f"{gercek} {d.get('birim', '')}")
            with c3:
                fark = d.get("fark", 0)
                st.metric("Fark", f"{fark:+} {d.get('birim', '')}")
            st.progress(min(oran / 100, 1.0))

    # Yol haritasi
    st.divider()
    styled_section("Gap Kapatma Yol Haritasi", "#D97706")
    yol = store.yol_haritasi_olustur()
    if yol:
        oncelik_icon = {"yuksek": "🔴", "orta": "🟡", "dusuk": "🟢"}
        for item in yol:
            icon = oncelik_icon.get(item.get("oncelik", ""), "⚪")
            st.markdown(
                f"{icon} **{item.get('kpi', '')}** — "
                f"Mevcut: {item.get('mevcut', 0)} | Hedef: {item.get('hedef', 0)} | "
                f"Fark: {item.get('fark', 0)} | Sure: {item.get('tahmini_sure', '')}"
            )
    else:
        styled_info_banner("Tum KPI'lar hedefte -- tebrikler!", "success")

    # AI tavsiye
    st.divider()
    styled_section("AI Performans Tavsiyesi", "#7C3AED")
    if st.button("AI Tavsiye Al", key="perf_ai_btn", type="primary"):
        with st.spinner("AI analiz ediyor..."):
            tavsiye = store.ai_performans_tavsiye()
            if tavsiye:
                st.markdown(tavsiye)
            else:
                styled_info_banner(
                    "AI tavsiye icin OpenAI API anahtari gereklidir (OPENAI_API_KEY).",
                    "warning",
                )


# ================================================================
#  TAB 10 — AI STEM Kocu
# ================================================================

def _tab_ai_koc(store):
    styled_section("AI STEM Kocu", "#7C3AED")

    styled_info_banner(
        "AI STEM Kocu, proje onerileri, deney planlama ve problem cozme rehberligi sunar. "
        "OpenAI API anahtari (OPENAI_API_KEY) gerektirir.",
        "info",
        icon="🤖",
    )

    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "📊 Genel Analiz",
        "💡 Proje Onerisi",
        "🧪 Deney Planlama",
        "🧩 Problem Cozme",
    ])

    with tab_a:
        styled_section("STEM Merkezi AI Analizi", "#2563EB")
        if st.button("AI Analiz Baslat", key="ai_genel_btn", type="primary"):
            with st.spinner("AI analiz ediyor..."):
                analiz = store.ai_analiz()
                if analiz:
                    st.markdown(analiz)
                else:
                    styled_info_banner("AI analiz icin OpenAI API anahtari gerekli.", "warning")

    with tab_b:
        styled_section("AI Proje Onerisi", "#059669")
        st.markdown("Ogrenci seviyesi ve ilgi alanina gore kisisellestirilmis STEM proje onerisi alin.")
        c1, c2 = st.columns(2)
        with c1:
            oneri_sinif = st.selectbox("Sinif Seviyesi", list(SINIF_GRUPLARI.keys()), key="ai_oneri_sinif")
        with c2:
            oneri_dal = st.multiselect("Ilgi Alanlari", STEM_DALLARI, key="ai_oneri_dal")
        oneri_not = st.text_area("Ek Bilgi / Tercihler", key="ai_oneri_not")

        if st.button("Proje Onerisi Al", key="ai_oneri_btn", type="primary"):
            with st.spinner("AI proje onerisi olusturuyor..."):
                ek = f"Sinif: {oneri_sinif}, Dallar: {', '.join(oneri_dal)}, Not: {oneri_not}"
                sonuc = store.ai_analiz(veri_ozeti=f"Proje onerisi iste: {ek}")
                if sonuc:
                    st.markdown(sonuc)
                else:
                    styled_info_banner("AI proje onerisi icin OpenAI API anahtari gerekli.", "warning")

    with tab_c:
        styled_section("AI Deney Planlama Rehberi", "#D97706")
        st.markdown("Bir deney konusu girin, AI sizin icin adim adim deney plani olusstursun.")
        deney_konu = st.text_input("Deney Konusu", key="ai_deney_konu")
        deney_sinif = st.selectbox("Sinif Grubu", list(SINIF_GRUPLARI.keys()), key="ai_deney_sinif")

        if st.button("Deney Plani Olustur", key="ai_deney_btn", type="primary"):
            if not deney_konu:
                st.error("Deney konusu girin.")
            else:
                with st.spinner("AI deney plani olusturuyor..."):
                    sonuc = store.ai_analiz(
                        veri_ozeti=f"Deney plani olustur: Konu={deney_konu}, Sinif={deney_sinif}. "
                        "Hipotez, malzeme listesi, adimlar, guvenlik uyarilari ve degerlendirme kriterleri icermeli."
                    )
                    if sonuc:
                        st.markdown(sonuc)
                    else:
                        styled_info_banner("AI deney plani icin OpenAI API anahtari gerekli.", "warning")

    with tab_d:
        styled_section("AI Problem Cozme Rehberi", "#ef4444")
        st.markdown("Bir STEM problemi tanimlyin, AI size adim adim cozum rehberi sunsun.")
        problem = st.text_area("Problem Tanimi", key="ai_problem_tanim")
        problem_dal = st.selectbox("Ilgili STEM Dali", STEM_DALLARI, key="ai_problem_dal")

        if st.button("Cozum Rehberi Al", key="ai_problem_btn", type="primary"):
            if not problem:
                st.error("Problem tanimini girin.")
            else:
                with st.spinner("AI cozum rehberi olusturuyor..."):
                    sonuc = store.ai_analiz(
                        veri_ozeti=f"Problem cozme rehberi: Dal={problem_dal}, Problem={problem}. "
                        "Muhendislik tasarim sureci (Tanimla, Arastir, Tasarla, Uret, Test, Gelistir) adimlariyla cozum sun."
                    )
                    if sonuc:
                        st.markdown(sonuc)
                    else:
                        styled_info_banner("AI cozum rehberi icin OpenAI API anahtari gerekli.", "warning")


# ════════════════════════════════════════════════════════════
# PREMIUM YENILIKLER — Hero, Metrics, 4 Yeni Sekme
# ════════════════════════════════════════════════════════════


def _stem_premium_hero():
    """Animated gradient hero banner — STEAM Merkezi premium giris."""
    st.markdown("""
    <style>
    @keyframes stemHeroShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    @keyframes stemHeroFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    @keyframes stemPulseGlow {
        0%, 100% { box-shadow: 0 0 30px rgba(124,58,237,.3), 0 8px 32px rgba(0,0,0,.4); }
        50% { box-shadow: 0 0 60px rgba(168,85,247,.5), 0 12px 48px rgba(0,0,0,.5); }
    }
    .stem-hero {
        background: linear-gradient(135deg, #1a0b3d 0%, #2d1b4e 25%, #4c1d95 50%, #1e1b4b 75%, #1a0b3d 100%);
        background-size: 300% 300%;
        animation: stemHeroShimmer 12s ease infinite;
        border-radius: 24px;
        padding: 30px 36px;
        margin: 14px 0 18px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(168,85,247,.3);
        box-shadow: 0 12px 48px rgba(76,29,149,.3),
                    0 0 0 1px rgba(168,85,247,.1) inset;
    }
    .stem-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(192,132,252,.2) 0%, transparent 60%);
        border-radius: 50%;
        filter: blur(60px);
        pointer-events: none;
    }
    .stem-hero::after {
        content: '';
        position: absolute;
        bottom: -40%;
        left: -5%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(99,102,241,.18) 0%, transparent 60%);
        border-radius: 50%;
        filter: blur(70px);
        pointer-events: none;
    }
    .stem-hero-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .stem-hero-icon {
        width: 86px;
        height: 86px;
        border-radius: 22px;
        background: linear-gradient(135deg, #c084fc, #a855f7, #7c3aed);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 44px;
        animation: stemHeroFloat 4s ease-in-out infinite, stemPulseGlow 3s ease-in-out infinite;
        flex-shrink: 0;
    }
    .stem-hero-text {
        flex: 1;
        min-width: 240px;
    }
    .stem-hero-title {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #fff, #e9d5ff, #c4b5fd, #e9d5ff, #fff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: stemHeroShimmer 6s linear infinite;
        margin: 0;
        letter-spacing: -1px;
        line-height: 1;
    }
    .stem-hero-sub {
        color: rgba(196,181,253,.85);
        font-size: .85rem;
        letter-spacing: 1.5px;
        margin-top: 8px;
        text-transform: uppercase;
        font-weight: 600;
    }
    .stem-hero-tagline {
        color: rgba(255,255,255,.7);
        font-size: .82rem;
        margin-top: 6px;
        line-height: 1.5;
    }
    .stem-hero-pills {
        display: flex;
        gap: 8px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .stem-hero-pill {
        background: rgba(168,85,247,.18);
        border: 1px solid rgba(192,132,252,.35);
        color: #e9d5ff;
        padding: 4px 12px;
        border-radius: 14px;
        font-size: .68rem;
        font-weight: 700;
        letter-spacing: .5px;
        backdrop-filter: blur(8px);
    }
    </style>
    <div class="stem-hero">
        <div class="stem-hero-content">
            <div class="stem-hero-icon">🔬</div>
            <div class="stem-hero-text">
                <div class="stem-hero-title">STEAM MERKEZI</div>
                <div class="stem-hero-sub">Bilim · Teknoloji · Mühendislik · Sanat · Matematik</div>
                <div class="stem-hero-tagline">Yaratıcı düşünme, tasarım odaklı problem çözme ve yeni nesil maker laboratuvarı</div>
                <div class="stem-hero-pills">
                    <span class="stem-hero-pill">🤖 Robotik</span>
                    <span class="stem-hero-pill">💻 Kodlama</span>
                    <span class="stem-hero-pill">🎨 Sanat</span>
                    <span class="stem-hero-pill">🧮 Matematik</span>
                    <span class="stem-hero-pill">⚙️ Maker</span>
                    <span class="stem-hero-pill">🧪 Lab</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _stem_premium_metrics(stats: dict):
    """Glassmorphism premium metrik kartlari."""
    st.markdown("""
    <style>
    .stem-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
        margin: 8px 0 18px;
    }
    .stem-metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
        border: 1px solid rgba(168,85,247,.25);
        border-radius: 16px;
        padding: 16px 18px;
        backdrop-filter: blur(20px);
        transition: all .3s ease;
        position: relative;
        overflow: hidden;
    }
    .stem-metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--metric-color);
    }
    .stem-metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--metric-color);
        box-shadow: 0 12px 32px var(--metric-glow);
    }
    .stem-metric-icon {
        font-size: 1.6rem;
        opacity: .9;
    }
    .stem-metric-value {
        font-size: 2rem;
        font-weight: 900;
        color: #fff;
        margin: 4px 0 2px;
        line-height: 1;
        font-family: 'Inter', sans-serif;
    }
    .stem-metric-label {
        color: rgba(255,255,255,.6);
        font-size: .68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    metrikler = [
        ("Toplam Proje", stats.get("toplam_proje", 0), "#7C3AED", "rgba(124,58,237,.3)", "🔬"),
        ("Aktif Proje", stats.get("aktif_proje", 0), "#0891B2", "rgba(8,145,178,.3)", "⚡"),
        ("Yarışma", stats.get("toplam_yarisma", 0), "#059669", "rgba(5,150,105,.3)", "🏆"),
        ("Görev", stats.get("toplam_gorev", 0), "#D97706", "rgba(217,119,6,.3)", "🔧"),
        ("Profil", stats.get("toplam_profil", 0), "#2563EB", "rgba(37,99,235,.3)", "👤"),
    ]

    cards_html = '<div class="stem-metrics">'
    for label, val, color, glow, icon in metrikler:
        cards_html += (
            f'<div class="stem-metric-card" style="--metric-color:{color};--metric-glow:{glow}">'
            f'<div class="stem-metric-icon">{icon}</div>'
            f'<div class="stem-metric-value">{val}</div>'
            f'<div class="stem-metric-label">{label}</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
# YENILIK 1: PROJECT SHOWCASE GALLERY
# ────────────────────────────────────────────────────────────

def _tab_showcase(store):
    """3D efektli, tıklanabilir proje galerisi — Pinterest tarzı kart wall."""
    st.markdown("""
    <style>
    @keyframes scShimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .sc-showcase-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 18px;
        margin: 16px 0;
    }
    .sc-showcase-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
        border: 1px solid rgba(168,85,247,.3);
        border-radius: 18px;
        overflow: hidden;
        transition: all .4s cubic-bezier(.4, 0, .2, 1);
        cursor: pointer;
        position: relative;
        transform-style: preserve-3d;
    }
    .sc-showcase-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,.08) 50%, transparent 70%);
        background-size: 200% 100%;
        animation: scShimmer 4s linear infinite;
        pointer-events: none;
    }
    .sc-showcase-card:hover {
        transform: translateY(-8px) rotateX(2deg);
        border-color: #c084fc;
        box-shadow: 0 24px 48px rgba(124,58,237,.4),
                    0 0 0 1px rgba(192,132,252,.3) inset;
    }
    .sc-showcase-header {
        height: 100px;
        background: linear-gradient(135deg, var(--card-color, #7c3aed), #a855f7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        position: relative;
    }
    .sc-showcase-status {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,.4);
        backdrop-filter: blur(8px);
        color: #fff;
        font-size: .65rem;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid rgba(255,255,255,.2);
    }
    .sc-showcase-body {
        padding: 16px 18px;
        position: relative;
        z-index: 1;
    }
    .sc-showcase-title {
        color: #fff;
        font-size: 1rem;
        font-weight: 800;
        margin: 0 0 6px;
        letter-spacing: -.3px;
        font-family: 'Inter', sans-serif;
    }
    .sc-showcase-desc {
        color: rgba(196,181,253,.75);
        font-size: .78rem;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .sc-showcase-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(168,85,247,.2);
    }
    .sc-showcase-class {
        color: #c084fc;
        font-size: .7rem;
        font-weight: 700;
    }
    .sc-showcase-tags {
        display: flex;
        gap: 4px;
    }
    .sc-showcase-tag {
        background: rgba(168,85,247,.2);
        color: #e9d5ff;
        font-size: .58rem;
        padding: 2px 7px;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    styled_section("🌟 Project Showcase Gallery", "#a855f7")

    projeler = store.load_list("projeler")
    if not projeler:
        st.markdown(
            '<div style="text-align:center;padding:40px;background:linear-gradient(135deg,#1e1b4b,#312e81);'
            'border-radius:16px;border:1px dashed rgba(168,85,247,.4)">'
            '<div style="font-size:3rem;margin-bottom:8px">🎨</div>'
            '<div style="color:#e9d5ff;font-weight:700">Henuz showcase\'e eklenecek proje yok</div>'
            '<div style="color:#a78bfa;font-size:.8rem;margin-top:4px">"🔬 Proje" sekmesinden yeni proje ekleyin</div>'
            '</div>',
            unsafe_allow_html=True
        )
        return

    # Kategori → emoji + renk eslemesi
    kategori_stilleri = {
        "Robotik": ("🤖", "#dc2626"),
        "Kodlama": ("💻", "#2563eb"),
        "3D Tasarim": ("🎭", "#7c3aed"),
        "Elektronik": ("⚡", "#f59e0b"),
        "Maker": ("⚙️", "#059669"),
        "Bilim": ("🧪", "#0891b2"),
        "Matematik": ("🧮", "#ec4899"),
        "Sanat": ("🎨", "#a855f7"),
    }

    # Filter bar
    fc1, fc2 = st.columns([2, 1])
    with fc1:
        arama = st.text_input("🔎 Arama", key="sc_search", placeholder="Proje adı veya kategori")
    with fc2:
        siralama = st.selectbox("Sırala", ["En Yeni", "En Eski", "Adına Göre"], key="sc_sort")

    # Filtreleme + sıralama
    gosterilen = projeler[:]
    if arama:
        ar = arama.lower()
        gosterilen = [p for p in gosterilen
                      if ar in p.get("baslik", "").lower()
                      or ar in p.get("kategori", "").lower()
                      or ar in p.get("aciklama", "").lower()]
    if siralama == "En Yeni":
        gosterilen.sort(key=lambda x: x.get("olusturma_tarihi", ""), reverse=True)
    elif siralama == "En Eski":
        gosterilen.sort(key=lambda x: x.get("olusturma_tarihi", ""))
    else:
        gosterilen.sort(key=lambda x: x.get("baslik", ""))

    st.caption(f"📦 {len(gosterilen)} proje gösteriliyor")

    # Card grid
    cards_html = '<div class="sc-showcase-grid">'
    for p in gosterilen[:30]:  # max 30
        kat = p.get("kategori", "Diger")
        emoji, color = kategori_stilleri.get(kat, ("🔬", "#7c3aed"))
        baslik = p.get("baslik", "İsimsiz")[:60]
        aciklama = p.get("aciklama", "Açıklama yok")[:120]
        durum = p.get("durum", "fikir")
        sinif = p.get("sinif", "-")
        sube = p.get("sube", "-")
        dallar = (p.get("stem_dallari") or [])[:2]
        tags_html = "".join(f'<span class="sc-showcase-tag">{d[:8]}</span>' for d in dallar)

        cards_html += (
            f'<div class="sc-showcase-card" style="--card-color:{color}">'
            f'<div class="sc-showcase-header">'
            f'<span>{emoji}</span>'
            f'<div class="sc-showcase-status">{durum.upper()}</div>'
            f'</div>'
            f'<div class="sc-showcase-body">'
            f'<div class="sc-showcase-title">{baslik}</div>'
            f'<div class="sc-showcase-desc">{aciklama}</div>'
            f'<div class="sc-showcase-meta">'
            f'<span class="sc-showcase-class">{sinif}/{sube}</span>'
            f'<div class="sc-showcase-tags">{tags_html}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
# YENILIK 2: SKILL TREE — Interaktif Gelisim Roadmapi
# ────────────────────────────────────────────────────────────

def _tab_skill_tree(store):
    """Oyun tarzi skill tree — STEM dallarinda gelisim haritasi."""
    st.markdown("""
    <style>
    .skill-tree-wrap {
        background: radial-gradient(ellipse at center, #1e1b4b 0%, #0f0a1f 100%);
        border-radius: 20px;
        padding: 24px;
        margin: 14px 0;
        border: 1px solid rgba(168,85,247,.3);
    }
    .skill-branch {
        margin-bottom: 22px;
    }
    .skill-branch-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #fff;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 12px;
        font-family: 'Inter', sans-serif;
    }
    .skill-branch-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .skill-nodes {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .skill-node {
        flex: 1;
        min-width: 110px;
        max-width: 160px;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        transition: all .25s ease;
        position: relative;
    }
    .skill-node-locked {
        background: rgba(255,255,255,.03);
        border: 1px dashed rgba(255,255,255,.15);
        color: rgba(255,255,255,.3);
    }
    .skill-node-active {
        background: linear-gradient(135deg, var(--branch-color), rgba(255,255,255,.1));
        border: 2px solid var(--branch-color);
        color: #fff;
        box-shadow: 0 4px 16px var(--branch-glow);
    }
    .skill-node-mastered {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border: 2px solid #fcd34d;
        color: #1a0a00;
        box-shadow: 0 6px 20px rgba(251,191,36,.5);
    }
    .skill-node:hover {
        transform: translateY(-3px) scale(1.03);
    }
    .skill-node-icon {
        font-size: 1.6rem;
        margin-bottom: 4px;
    }
    .skill-node-title {
        font-size: .72rem;
        font-weight: 800;
    }
    .skill-node-xp {
        font-size: .58rem;
        font-weight: 700;
        margin-top: 4px;
        opacity: .85;
    }
    .skill-progress-bar {
        height: 6px;
        background: rgba(255,255,255,.1);
        border-radius: 3px;
        overflow: hidden;
        margin-top: 4px;
    }
    .skill-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        transition: width .8s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    styled_section("🌳 STEM Skill Tree — Yetenek Haritası", "#a855f7")

    st.caption(
        "Her STEM dalında ilerlemenizi takip edin. "
        "Projeler tamamladıkça yeni yetenekler açılır, ustalaşırsanız altın rozet kazanırsınız."
    )

    # Mevcut profil performansını cek
    projeler = store.load_list("projeler")

    # Dal bazli proje sayisi
    dal_sayilari: dict = {}
    for p in projeler:
        for d in (p.get("stem_dallari") or []):
            dal_sayilari[d] = dal_sayilari.get(d, 0) + 1

    # 5 ana branch + 4 yetenek seviyesi (Baslangic → Orta → Ileri → Usta)
    branches = [
        ("Robotik & Mekatronik", "🤖", "#dc2626", "rgba(220,38,38,.4)", [
            ("Motor Kontrol", "⚙️", 1),
            ("Sensor Okuma", "📡", 2),
            ("Mikrodenetleyici", "🔌", 4),
            ("Otonom Robot", "🦾", 8),
        ]),
        ("Kodlama & Yazilim", "💻", "#2563eb", "rgba(37,99,235,.4)", [
            ("Algoritma", "🧠", 1),
            ("Web Gelistirme", "🌐", 2),
            ("Veri Yapilari", "📊", 4),
            ("Yapay Zeka", "🤖", 8),
        ]),
        ("Mühendislik Tasarim", "⚙️", "#f59e0b", "rgba(245,158,11,.4)", [
            ("Brainstorm", "💡", 1),
            ("CAD Tasarim", "📐", 2),
            ("Prototip", "🛠️", 4),
            ("Optimizasyon", "🎯", 8),
        ]),
        ("Bilim & Deney", "🧪", "#059669", "rgba(5,150,105,.4)", [
            ("Hipotez", "🔬", 1),
            ("Veri Toplama", "📈", 2),
            ("Analiz", "📊", 4),
            ("Yayin", "📜", 8),
        ]),
        ("Sanat & Sunum", "🎨", "#a855f7", "rgba(168,85,247,.4)", [
            ("Eskiz", "✏️", 1),
            ("Dijital Tasarim", "🖼️", 2),
            ("Animasyon", "🎬", 4),
            ("Sergi", "🏛️", 8),
        ]),
    ]

    wrap_html = '<div class="skill-tree-wrap">'
    for branch_name, branch_icon, branch_color, branch_glow, nodes in branches:
        # Bu daldaki proje sayisini bul
        dal_proje = 0
        for d in dal_sayilari:
            if any(k in d.lower() for k in branch_name.lower().split()):
                dal_proje += dal_sayilari[d]

        wrap_html += '<div class="skill-branch">'
        wrap_html += (
            f'<div class="skill-branch-title">'
            f'<div class="skill-branch-icon" style="background:{branch_color}30;border:1px solid {branch_color}">{branch_icon}</div>'
            f'<span>{branch_name}</span>'
            f'<span style="margin-left:auto;color:{branch_color};font-size:.72rem">{dal_proje} proje</span>'
            f'</div>'
        )
        wrap_html += '<div class="skill-nodes">'
        for i, (node_name, node_icon, esik) in enumerate(nodes):
            if dal_proje >= esik * 2:
                durum = "mastered"
                progress = 100
            elif dal_proje >= esik:
                durum = "active"
                progress = min(100, int(dal_proje / (esik * 2) * 100))
            else:
                durum = "locked"
                progress = int((dal_proje / esik) * 100) if esik > 0 else 0

            xp_text = f"+{esik * 10} XP"
            wrap_html += (
                f'<div class="skill-node skill-node-{durum}" style="--branch-color:{branch_color};--branch-glow:{branch_glow}">'
                f'<div class="skill-node-icon">{node_icon}</div>'
                f'<div class="skill-node-title">{node_name}</div>'
                f'<div class="skill-node-xp">{xp_text}</div>'
                f'<div class="skill-progress-bar"><div class="skill-progress-fill" style="width:{progress}%"></div></div>'
                f'</div>'
            )
        wrap_html += '</div></div>'
    wrap_html += '</div>'
    st.markdown(wrap_html, unsafe_allow_html=True)

    # Genel ilerleme
    st.markdown("---")
    toplam_node = sum(len(nodes) for _, _, _, _, nodes in branches)
    acilan = sum(
        1 for _, _, _, _, nodes in branches
        for _, _, esik in nodes
        if any(dal_sayilari.get(d, 0) >= esik for d in dal_sayilari)
    )

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.metric("📌 Toplam Yetenek", toplam_node)
    with cc2:
        st.metric("🔓 Açılan", acilan)
    with cc3:
        oran = round(acilan / max(toplam_node, 1) * 100)
        st.metric("📈 İlerleme", f"%{oran}")


# ────────────────────────────────────────────────────────────
# YENILIK 3: LIVE LAB — Interaktif Simulasyon Laboratuvari
# ────────────────────────────────────────────────────────────

def _tab_live_lab():
    """Canli simulasyon laboratuvari — fizik, kimya, matematik."""
    styled_section("🧪 Live Lab Simulator", "#0891B2")

    st.caption(
        "Tarayıcıda canlı simulasyonlar — fizik, kimya, matematik, "
        "biyoloji konularında interaktif deneyler. Tüm simulasyonlar PhET'ten."
    )

    # Simulasyon kataloglari (PhET embed URL'leri)
    simulasyonlar = {
        "🔥 Fizik": [
            ("Yer Çekimi ve Yörünge", "Gezegenlerin yörünge hareketleri", "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_tr.html"),
            ("Sürtünme", "Sürtünme katsayısı deneyleri", "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_tr.html"),
            ("Dalgalar", "Su dalgaları + ses dalgaları", "https://phet.colorado.edu/sims/html/wave-on-a-string/latest/wave-on-a-string_tr.html"),
            ("Optik", "Lens ve prizma deneyleri", "https://phet.colorado.edu/sims/html/bending-light/latest/bending-light_tr.html"),
        ],
        "🧪 Kimya": [
            ("pH Skalası", "Asit-baz dengesi", "https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_tr.html"),
            ("Atom Yapısı", "Periodik tablo + elektron yapısı", "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_tr.html"),
            ("Molekül Şekli", "VSEPR teorisi", "https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_tr.html"),
            ("Reaksiyon Hızı", "Kimyasal reaksiyon hızları", "https://phet.colorado.edu/sims/html/reactants-products-and-leftovers/latest/reactants-products-and-leftovers_tr.html"),
        ],
        "🧮 Matematik": [
            ("Fonksiyon Grafikleri", "y=mx+b grafikleme", "https://phet.colorado.edu/sims/html/graphing-lines/latest/graphing-lines_tr.html"),
            ("Kesirler", "Kesir işlemleri", "https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_tr.html"),
            ("Cebir", "Denklem dengeleme", "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_tr.html"),
            ("Trigonometri", "Birim çember", "https://phet.colorado.edu/sims/html/trig-tour/latest/trig-tour_tr.html"),
        ],
        "🌱 Biyoloji": [
            ("Doğal Seçilim", "Evrim ve adaptasyon", "https://phet.colorado.edu/sims/html/natural-selection/latest/natural-selection_tr.html"),
            ("Yeşil Bilim", "Bitkilerin gelişimi", "https://phet.colorado.edu/sims/html/plate-tectonics/latest/plate-tectonics_en.html"),
        ],
    }

    # Kategori secimi
    kategori = st.selectbox(
        "Bilim Dalı Seçin",
        list(simulasyonlar.keys()),
        key="lab_kategori",
    )

    # Simulasyon kart grid
    st.markdown("""
    <style>
    .lab-sim-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 14px;
        margin: 14px 0;
    }
    .lab-sim-card {
        background: linear-gradient(135deg, #0c4a6e, #075985);
        border: 1px solid rgba(14,165,233,.4);
        border-radius: 14px;
        padding: 16px;
        cursor: pointer;
        transition: all .25s ease;
    }
    .lab-sim-card:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
        box-shadow: 0 12px 28px rgba(14,165,233,.4);
    }
    .lab-sim-title {
        color: #fff;
        font-weight: 800;
        font-size: .92rem;
        margin-bottom: 4px;
    }
    .lab-sim-desc {
        color: rgba(186,230,253,.8);
        font-size: .75rem;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

    sims = simulasyonlar.get(kategori, [])

    # State: hangi simulasyon acik
    secili_key = f"lab_secili_{kategori}"
    if secili_key not in st.session_state:
        st.session_state[secili_key] = None

    cards_html = '<div class="lab-sim-grid">'
    for ad, aciklama, url in sims:
        cards_html += (
            f'<div class="lab-sim-card">'
            f'<div class="lab-sim-title">{ad}</div>'
            f'<div class="lab-sim-desc">{aciklama}</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Buton ile simulasyon ac
    st.markdown("##### Simulasyonu Çalıştır")
    sim_dict = {ad: url for ad, _, url in sims}
    sec = st.selectbox("Hangi simulasyonu açmak istiyorsun?", list(sim_dict.keys()),
                        key=f"lab_sim_sec_{kategori}")

    if st.button("🚀 Simulasyonu Başlat", key=f"lab_btn_{kategori}", type="primary",
                  use_container_width=True):
        st.session_state[secili_key] = sim_dict[sec]

    # Simulasyon iframe goster
    if st.session_state.get(secili_key):
        url = st.session_state[secili_key]
        st.markdown(
            f'<div style="background:#0a0e1f;border:2px solid #38bdf8;border-radius:14px;'
            f'padding:6px;margin-top:14px;box-shadow:0 12px 32px rgba(14,165,233,.3)">'
            f'<iframe src="{url}" width="100%" height="500" frameborder="0" '
            f'style="border-radius:10px" allowfullscreen></iframe>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button("✕ Simulasyonu Kapat", key=f"lab_close_{kategori}"):
            st.session_state[secili_key] = None
            st.rerun()


# ────────────────────────────────────────────────────────────
# YENILIK 4: ROZET DUVARI — Achievement Wall
# ────────────────────────────────────────────────────────────

def _tab_rozet_duvari(store):
    """STEM rozetleri duvarı — kazanılan/kilitli rozetler."""
    st.markdown("""
    <style>
    @keyframes rozetGlow {
        0%, 100% { box-shadow: 0 0 20px var(--rozet-glow), 0 8px 24px rgba(0,0,0,.4); }
        50% { box-shadow: 0 0 40px var(--rozet-glow), 0 12px 32px rgba(0,0,0,.5); }
    }
    @keyframes rozetFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-4px) rotate(2deg); }
    }
    .rozet-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 16px;
        margin: 16px 0;
    }
    .rozet-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid rgba(168,85,247,.3);
        border-radius: 18px;
        padding: 20px 14px;
        text-align: center;
        transition: all .3s ease;
        position: relative;
        overflow: hidden;
    }
    .rozet-card.kazandi {
        background: linear-gradient(135deg, var(--rozet-color), rgba(255,255,255,.1));
        border: 2px solid var(--rozet-color);
        animation: rozetGlow 3s ease-in-out infinite;
    }
    .rozet-card.kilitli {
        opacity: .4;
        filter: grayscale(.7);
    }
    .rozet-icon {
        font-size: 3rem;
        margin-bottom: 8px;
        display: inline-block;
    }
    .rozet-card.kazandi .rozet-icon {
        animation: rozetFloat 3s ease-in-out infinite;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,.4));
    }
    .rozet-name {
        color: #fff;
        font-size: .85rem;
        font-weight: 800;
        margin-bottom: 4px;
        letter-spacing: -.2px;
    }
    .rozet-desc {
        color: rgba(196,181,253,.7);
        font-size: .68rem;
        line-height: 1.3;
    }
    .rozet-status {
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(0,0,0,.6);
        backdrop-filter: blur(8px);
        padding: 3px 8px;
        border-radius: 10px;
        font-size: .58rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .rozet-card.kazandi .rozet-status {
        background: rgba(251,191,36,.9);
        color: #1a0a00;
    }
    .rozet-card.kilitli .rozet-status {
        background: rgba(100,116,139,.6);
        color: #cbd5e1;
    }
    </style>
    """, unsafe_allow_html=True)

    styled_section("🏅 Achievement Wall — Rozet Duvarı", "#fbbf24")

    st.caption(
        "STEM dünyasında ilerledikçe kazandığın rozetleri gör. "
        "Her rozet bir başarının simgesi — kazanmak için projeler tamamla, görevleri başar, yarışmalara katıl."
    )

    # Mevcut performans verilerini topla
    projeler = store.load_list("projeler")
    yarismalar = store.load_list("yarismalar")
    gorevler = store.load_list("gorevler")
    profiller = store.load_list("profiller")

    proje_sayisi = len(projeler)
    aktif_proje = sum(1 for p in projeler if p.get("durum") == "tamamlandi")
    yarisma_sayisi = len(yarismalar)
    gorev_sayisi = len(gorevler)
    profil_sayisi = len(profiller)
    dal_cesitliligi = len({d for p in projeler for d in (p.get("stem_dallari") or [])})

    # Rozet tanımlamaları
    rozetler = [
        ("Ilk Adim", "🌱", "#10b981", "rgba(16,185,129,.5)", "İlk projeni oluştur", proje_sayisi >= 1),
        ("Kasif", "🔍", "#06b6d4", "rgba(6,182,212,.5)", "5 farklı proje tamamla", aktif_proje >= 5),
        ("Maker Usta", "🛠️", "#f59e0b", "rgba(245,158,11,.5)", "10 proje üret", proje_sayisi >= 10),
        ("Cok Yonlu", "🌈", "#a855f7", "rgba(168,85,247,.5)", "5 farklı STEM dalında çalış", dal_cesitliligi >= 5),
        ("Robotik Sef", "🤖", "#dc2626", "rgba(220,38,38,.5)", "3 robotik projesi tamamla",
         sum(1 for p in projeler if "robotik" in p.get("kategori", "").lower()) >= 3),
        ("Kod Ninja", "💻", "#2563eb", "rgba(37,99,235,.5)", "5 kodlama projesi yap",
         sum(1 for p in projeler if "kod" in p.get("kategori", "").lower()) >= 5),
        ("Yarismaci", "🏆", "#fbbf24", "rgba(251,191,36,.5)", "İlk yarışmana katıl", yarisma_sayisi >= 1),
        ("Sampiyon", "👑", "#fbbf24", "rgba(251,191,36,.7)", "5 yarışmada yer al", yarisma_sayisi >= 5),
        ("Muhendis", "⚙️", "#ea580c", "rgba(234,88,12,.5)", "10 mühendislik görevi tamamla", gorev_sayisi >= 10),
        ("Bilim Adami", "🧪", "#0891b2", "rgba(8,145,178,.5)", "Bilim kategorisinde 3 proje",
         sum(1 for p in projeler if "bilim" in p.get("kategori", "").lower()) >= 3),
        ("Sanatci", "🎨", "#ec4899", "rgba(236,72,153,.5)", "Sanat dalında 3 proje",
         sum(1 for p in projeler if "sanat" in p.get("kategori", "").lower()
             or "Sanat" in (p.get("stem_dallari") or [])) >= 3),
        ("STEAM Efsanesi", "💎", "#8b5cf6", "rgba(139,92,246,.7)", "20 proje + 5 yarışma + 5 dal",
         proje_sayisi >= 20 and yarisma_sayisi >= 5 and dal_cesitliligi >= 5),
    ]

    # Toplam istatistik
    kazanildi = sum(1 for *_, k in rozetler if k)
    toplam = len(rozetler)
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);'
        f'border:1px solid rgba(168,85,247,.3);border-radius:14px;'
        f'padding:14px 18px;margin:10px 0;display:flex;align-items:center;gap:14px">'
        f'<div style="font-size:2rem">🏅</div>'
        f'<div style="flex:1">'
        f'<div style="color:#fff;font-weight:800;font-size:1rem">{kazanildi} / {toplam} Rozet</div>'
        f'<div style="color:#c4b5fd;font-size:.78rem">Sıradaki rozeti kazanmak için aktif projeler oluştur</div>'
        f'</div>'
        f'<div style="font-size:1.4rem;font-weight:900;color:#fbbf24">%{round(kazanildi / max(toplam, 1) * 100)}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Rozet grid
    grid_html = '<div class="rozet-grid">'
    for ad, ikon, renk, glow, aciklama, kazandi in rozetler:
        cls = "kazandi" if kazandi else "kilitli"
        status = "KAZANILDI" if kazandi else "KILITLI"
        grid_html += (
            f'<div class="rozet-card {cls}" style="--rozet-color:{renk};--rozet-glow:{glow}">'
            f'<div class="rozet-status">{status}</div>'
            f'<div class="rozet-icon">{ikon}</div>'
            f'<div class="rozet-name">{ad}</div>'
            f'<div class="rozet-desc">{aciklama}</div>'
            f'</div>'
        )
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
