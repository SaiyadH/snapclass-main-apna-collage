import streamlit as st

def header_home():
    logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"

    st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom:30px; margin-top:30px;'>
            <img src="{logo_url}" style="height: 100px;"/>
            <h1 style='text-align: center; color: #E0E3FF;'>APNA<br/>CLASS</h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"
    st.markdown(f"""
        <div style='display: flex; align-items: center; justify-content:center; gap: 10px; margin-top: 30px;'>
            <img src="{logo_url}" style="height: 60px; border-radius: 10px;"/>
            <h2 style='text-align:center; color:#5865F2'>APNA<br/>CLASS</h2>
        </div>
    """, unsafe_allow_html=True)