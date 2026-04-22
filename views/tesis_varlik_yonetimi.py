"""Tesis & Varlık Yönetimi — Tüketim/Demirbaş + Destek Hizmetleri birleşik modül."""
import streamlit as st
from utils.ui_common import inject_common_css, styled_header


def render_tesis_varlik_yonetimi():
    """Tüketim/Demirbaş + Destek Hizmetleri birleşik görünüm."""
    inject_common_css()
    styled_header("🏗️ Tesis & Varlık Yönetimi", "Tüketim/Demirbaş + Destek Hizmetleri")

    tab1, tab2 = st.tabs(["🗄️ Tüketim & Demirbaş", "🔧 Destek Hizmetleri"])

    with tab1:
        from views.tuketim_demirbas import render_tuketim_demirbas
        render_tuketim_demirbas()

    with tab2:
        from views.destek_hizmetleri import render_destek_hizmetleri
        render_destek_hizmetleri()
