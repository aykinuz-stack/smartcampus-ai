"""AI Destekli Bireysel Eğitim Modülü.

Dijital Kütüphane'deki AI Ders Asistanı + Kişisel Öğrenme Yol Haritası
+ Akıllı Çalışma Koçu + Bireysel Gelişim Analitik.
"""
from __future__ import annotations

import streamlit as st
from utils.ui_common import styled_header


def render_ai_bireysel_egitim():
    """Ana menüden erişilen AI Destekli Bireysel Eğitim modülü."""
    styled_header("AI Destekli Bireysel Egitim", "Kisisel ogrenme, adaptif plan, calisma kocu, gelisim analitik", icon="🤖")

    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("ai_bireysel_egitim")
    except Exception:
        pass

    # -- Tab Gruplama (13 -> 2 grup) --
    _G_71867 = {
        "Grup A": [("🤖 AI Ders Asistani", 0), ("🗺️ Yol Haritasi", 1), ("⏰ Calisma Kocu", 2), ("📊 Gelisim Analitik", 3), ("🎯 Sinav Hazirlik", 4), ("🧬 Ogrenme Stili", 5), ("🎮 Quest Macera", 6)],
        "Grup B": [("🧠 AI Ogretmen", 7), ("📋 Odev Asistani", 8), ("🔮 Dijital Ikiz", 9), ("👨‍👩‍👧 Veli Panel", 10), ("🏫 AI Cockpit", 11), ("🌐 Ekosistem", 12)],
    }
    _r_71867 = st.radio("", list(_G_71867.keys()), horizontal=True, label_visibility="collapsed", key="r_71867")
    _a_71867 = set(t[1] for t in _G_71867[_r_71867])
    tabs = st.tabs([t[0] for t in _G_71867[_r_71867]])
    _m_71867 = {idx: t for idx, t in zip((t[1] for t in _G_71867[_r_71867]), tabs)}

    if 0 in _a_71867:
      with _m_71867[0]:
        try:
            from views.dijital_kutuphane import render_ai_asistan
            render_ai_asistan()
        except Exception as _e:
            st.error(f"AI Ders Asistani yuklenemedi: {_e}")

    if 1 in _a_71867:
      with _m_71867[1]:
        try:
            from views._aibe_yeni_ozellikler import render_yol_haritasi
            render_yol_haritasi()
        except Exception as _e:
            st.error(f"Yol Haritasi yuklenemedi: {_e}")

    if 2 in _a_71867:
      with _m_71867[2]:
        try:
            from views._aibe_yeni_ozellikler import render_calisma_kocu
            render_calisma_kocu()
        except Exception as _e:
            st.error(f"Calisma Kocu yuklenemedi: {_e}")

    if 3 in _a_71867:
      with _m_71867[3]:
        try:
            from views._aibe_yeni_ozellikler import render_gelisim_analitik
            render_gelisim_analitik()
        except Exception as _e:
            st.error(f"Gelisim Analitik yuklenemedi: {_e}")

    if 4 in _a_71867:
      with _m_71867[4]:
        try:
            from views._aibe_super_features import render_sinav_hazirlik
            render_sinav_hazirlik()
        except Exception as _e:
            st.error(f"Sinav Hazirlik yuklenemedi: {_e}")

    if 5 in _a_71867:
      with _m_71867[5]:
        try:
            from views._aibe_super_features import render_ogrenme_stili
            render_ogrenme_stili()
        except Exception as _e:
            st.error(f"Ogrenme Stili yuklenemedi: {_e}")

    if 6 in _a_71867:
      with _m_71867[6]:
        try:
            from views._aibe_super_features import render_quest_sistemi
            render_quest_sistemi()
        except Exception as _e:
            st.error(f"Quest Sistemi yuklenemedi: {_e}")

    if 7 in _a_71867:
      with _m_71867[7]:
        try:
            from views._aibe_zirve_features import render_sokratik_ogretmen
            render_sokratik_ogretmen()
        except Exception as _e:
            st.error(f"AI Ogretmen yuklenemedi: {_e}")

    if 8 in _a_71867:
      with _m_71867[8]:
        try:
            from views._aibe_zirve_features import render_odev_asistani
            render_odev_asistani()
        except Exception as _e:
            st.error(f"Odev Asistani yuklenemedi: {_e}")

    if 9 in _a_71867:
      with _m_71867[9]:
        try:
            from views._aibe_zirve_features import render_dijital_ikiz
            render_dijital_ikiz()
        except Exception as _e:
            st.error(f"Dijital Ikiz yuklenemedi: {_e}")

    if 10 in _a_71867:
      with _m_71867[10]:
        try:
            from views._aibe_final_features import render_veli_kocluk
            render_veli_kocluk()
        except Exception as _e:
            st.error(f"Veli Panel yuklenemedi: {_e}")

    if 11 in _a_71867:
      with _m_71867[11]:
        try:
            from views._aibe_final_features import render_ai_cockpit
            render_ai_cockpit()
        except Exception as _e:
            st.error(f"AI Cockpit yuklenemedi: {_e}")

    if 12 in _a_71867:
      with _m_71867[12]:
        try:
            from views._aibe_final_features import render_ogrenme_ekosistemi
            render_ogrenme_ekosistemi()
        except Exception as _e:
            st.error(f"Ekosistem yuklenemedi: {_e}")
