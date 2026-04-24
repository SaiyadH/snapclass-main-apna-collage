import streamlit as st

def footer_home():
  
    
    logo_url = "https://lwfiles.mycourse.app/62a6cd5e1e9e2fbf212d608d-public/6efdd5e7f0d663cf231d0f2040be0a1e.png"

    st.markdown(f"""
               <div style="margin-top:2rem; display: flex; gap:6px; align-items: center; justify-content: center;">
                <p style="font-weight:bold; color:white;"> Designed by  </p>
                <img src="{logo_url}"  style="max-height: 25px;"/>
                
            """, unsafe_allow_html=True)
    
def footer_dashboard():
  
    
    logo_url = "https://lwfiles.mycourse.app/62a6cd5e1e9e2fbf212d608d-public/6efdd5e7f0d663cf231d0f2040be0a1e.png"

    st.markdown(f"""
               <div style="margin-top:2rem; display: flex; gap:6px; align-items: center; justify-content: center;">
                <p style="font-weight:bold; color:black;"> Designed by  </p>
                <img src="{logo_url}"  style="max-height: 25px;"/>
                
            """, unsafe_allow_html=True)
