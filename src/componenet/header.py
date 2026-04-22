import streamlit as st

def header_home():
    # st.header("SS Class")
    # logo_url = st.image("C:/Users/taiya/Downloads/SS_Class.jpg")
    logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"

    st.markdown(f"""
                <div style='display: flex; flex-direction: column; align-items: center; justify-content: center;, margin-bottom:30px;, margin-top:30px;'>
                    <img src="{logo_url}"  style="height: 80px;"/>
                    <h1 style='text-align: center; color:#E0E3FF'>Apna <br/> Class</h1>
                </div>
                
            """, unsafe_allow_html=True)
    
def header_dashboard():
    # st.header("SS Class")
    # logo_url = st.image("C:/Users/taiya/Downloads/SS_Class.jpg")
    logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"

    st.markdown(f"""
                <div style='display:flex; align-items: center; justify-content: center;,gap:10px, margin-top:30px;'>
                    <img src="{logo_url}"  style="height: 70px;"/>
                    <h2 style='text-align: center; color:#5865F2'>Apna <br/> Class</h2>
                </div>
                
            """, unsafe_allow_html=True)
