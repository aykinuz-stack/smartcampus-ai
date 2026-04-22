"""Öğrenci Zeka Merkezi — Öğrenci 360° + Erken Uyarı Sistemi birleşik modül."""
import streamlit as st
from utils.ui_common import inject_common_css, styled_header


def render_ogrenci_zeka_merkezi():
    """Öğrenci 360 + Erken Uyarı birleşik görünüm."""
    inject_common_css()
    styled_header("🧠 Öğrenci Zeka Merkezi", "360° Profil + Risk Analizi + Erken Uyarı")

    tab1, tab2 = st.tabs(["📊 Öğrenci 360°", "⚠️ Erken Uyarı & Risk"])

    with tab1:
        from views.ogrenci_360 import render_ogrenci_360
        render_ogrenci_360()

    with tab2:
        from views.erken_uyari import render_erken_uyari
        render_erken_uyari()
