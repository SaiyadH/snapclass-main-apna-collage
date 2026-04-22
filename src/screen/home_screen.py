import streamlit as st
from src.screen.components.header import header_home
from src.screen.ui.base_layout import style_base_layout, style_background_home, style_background_dashboard
from src.screen.components.footer import footer_home

def home_screen():
    # st.header("Home Screen")

    header_home()
    style_background_home()
    style_base_layout()


    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.pinimg.com/736x/c5/5a/84/c55a843b1ac7c09f49502d38b7ed0cd3.jpg", width=100, caption="Teacher") 

        if st.button("Login as Student", type="primary", icon = ":material/arrow_outward:", icon_position="right"):
            st.session_state['login_type'] = 'Student'
            st.rerun()
        

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.pinimg.com/736x/45/ba/d2/45bad2ff0901cfbce8b037d63c3764b3.jpg", width=100, caption="Student")

        if st.button("Login as Teacher", type="primary", icon = ":material/arrow_outward:", icon_position="right"):
            st.session_state['login_type'] = 'Teacher'
            st.rerun()
        

    footer_home()