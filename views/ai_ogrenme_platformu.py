"""AI Öğrenme Platformu — Dijital Kütüphane + AI Bireysel Eğitim birleşik modül."""
import streamlit as st
from utils.ui_common import inject_common_css, styled_header


def render_ai_ogrenme_platformu(readonly=False):
    """Dijital Kütüphane + AI Bireysel Eğitim birleşik görünüm."""
    inject_common_css()
    styled_header("🎓 AI Öğrenme Platformu", "Dijital Kütüphane + AI Bireysel Eğitim")

    tab1, tab2 = st.tabs(["📱 Dijital Kütüphane", "🤖 AI Bireysel Eğitim"])

    with tab1:
        from views.dijital_kutuphane import render_dijital_kutuphane
        render_dijital_kutuphane(readonly=readonly)

    with tab2:
        from views.ai_bireysel_egitim import render_ai_bireysel_egitim
        render_ai_bireysel_egitim()
