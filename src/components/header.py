# import streamlit as st

# def header_home():
    
#     logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"

#     st.markdown(f"""
#                 <div style='display: flex; flex-direction: column; align-items: center; justify-content: center;, margin-bottom:30px;, margin-top:30px;'>
#                     <img src="{logo_url}"  style="height: 80px;"/>
#                     <h1 style='text-align: center; color:#E0E3FF'>Apna <br/> Class</h1>
#                 </div>
                
#             """, unsafe_allow_html=True)
    
# def header_dashboard():
#     # st.header("SS Class")
#     # logo_url = st.image("C:/Users/taiya/Downloads/SS_Class.jpg")
#     logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"

#     st.markdown(f"""
#                 <div style='display:flex; align-items: center; justify-content: center;,gap:10px;'>
#                     <img src="{logo_url}"  style="height: 85px;"/>
#                     <h2 style='text-align: center; color:#5865F2'>Apna <br/> Class</h2>
#                 </div>
                
#             """, unsafe_allow_html=True)


import streamlit as st

def header_dashboard():
    logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"
    st.markdown(f"""
        <div style='display: flex; align-items: center; justify-content: flex-start; gap: 20px; margin-bottom: 20px;'>
            <img src="{logo_url}" style="height: 60px; border-radius: 10px;"/>
            <div style="line-height: 1;">
                <span style="font-family: 'Climate Crisis'; font-size: 25px; color: black;">APNA</span><br>
                <span style="font-family: 'Climate Crisis'; font-size: 25px; color: black;">CLASS</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def header_home():
    logo_url = "https://i.pinimg.com/736x/32/0d/9f/320d9f991e417508dc9ef46113664b03.jpg"

    st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom:30px; margin-top:30px;'>
            <img src="{logo_url}" style="height: 100px; border-radius: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);"/>
            <h1 style='text-align: center; color: #FFFFFF; font-family: "Climate Crisis", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                APNA <br/> CLASS
            </h1>
        </div>
    """, unsafe_allow_html=True)