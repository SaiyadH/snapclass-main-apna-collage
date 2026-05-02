import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home, style_background_dashboard
from src.components.footer import footer_home

def home_screen():
    

    header_home()
    style_background_home()
    style_base_layout()


    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image(r"C:\Users\taiya\Downloads\1B (1).png", width=160) 

        if st.button("Login as Student", type="primary",icon=':material/arrow_outward:', icon_position="right"):
            st.session_state['login_type'] = 'Student'
            st.rerun()
        

    with col2:
        st.header("I'm Teacher")
        st.image(r"C:\Users\taiya\Downloads\Untitled.png", width=160)

        if st.button("Login as Teacher", type="primary", icon=':material/arrow_outward:',icon_position="right"):
            st.session_state['login_type'] = 'Teacher'
            st.rerun()
        

    footer_home()
