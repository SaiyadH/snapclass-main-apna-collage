import streamlit as st
from src.screen.ui.base_layout import style_background_dashboard, style_base_layout

def teacher_screen():
    base_layiut()
    style_background_dashboard()
    style_base_layout()
    st.header("Teacher Screen")