# import streamlit as st

# def style_background_home():

#     st.markdown("""
#        <style>
                
#                 .stApp {
#                     background-color: #5865F2 !important;
                    
#                 }

#                 .stApp div[data-testid="stColumn"] {
#                 background-color:#E0E3FF !important;
#                 padding:2.5rem !important;
#                 border-radius:5rem !important;
#                 }

#     <style>
                
#                 """
#             ,unsafe_allow_html=True)
    
# def style_background_dashboard():

#     st.markdown("""
#        <style>
                
#                 .stApp {
#                     background-color: #E0E3FF !important;
                    
#                 }

#                 .stApp div[data-testid="stColumn"] {
#                     background-color: #E0E3FF !important;
#                     border-radius: 2.5rem !important;
#                     padding: 5rem !important;
#                 }

#     <style>
                
#                 """
#             ,unsafe_allow_html=True)

# def style_base_layout():



#     st.markdown("""
#        <style>
#             @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
#             @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
#         /* Hide Top Bar Streamlit*/
                
#             #MainMenu, header, footer {
#                 visibility: hidden;
#             }
            

#             .block-container {
#                 padding-top: 1.5rem !important;
                   
#             }
            
#             h1 {
#                 font-family: 'Climate Crisis', sans-serif !important;
#                 font-size: 3rem !important;
#                 line-height: 1.1 !important;
#                 margin-bottom: 0rem !important;
#                 margin-top: 0rem !important;

#             }
                
#             h2 {
#                 font-family: 'Climate Crisis', sans-serif !important;
#                 font-size: 2rem !important;
#                 line-height: 0.9 !important;
#                 margin-bottom: 0rem !important;
#             }
                
#             h3, h4, p{
#                 font-family: 'Outfit', sans-serif !important;
#             }
                
#              button {
#                 border-radius: 1.5rem !important;
#                 background: #5865F2 !important;
#                 color: white !important;
#                 border: none !important;
#                 padding: 10px 20px !important;
#                 transition: transform 0.2s ease-in-out !important;
#             }

                
#             button[kind="secondary"] {
#                 border-radius: 1.5rem !important;
#                 background: #EB459E !important;
#                 color: white !important;
#                 border: none !important;
#                 padding: 10px 20px !important;
#                 transition: transform 0.2s ease-in-out !important;
#             }
                
#             button[kind="ternsary"] {
#                 border-radius: 1.5rem !important;
#                 background: black !important;
#                 color: white !important;
#                 border: none !important;
#                 padding: 10px 20px !important;
#                 transition: transform 0.2s ease-in-out !important;
#             }

#             button:hover {
#                 transform: scale(1.05) !important;


#         <style>
                
#                 """
#             ,unsafe_allow_html=True)



import streamlit as st

def style_base_layout():
    # Page ko wide mode mein set karne ke liye (Sabse pehle call hona chahiye)
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');
            
            # MainMenu, header, footer { visibility: hidden; }
            
            .stApp {
                background-color: #F0F2F6; /* Light clean background */
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                color: white !important;
                font-size: 3.5rem !important;
                margin: 0px !important;
                line-height: 1 !important;
            }
            
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                color: #2C2F38 !important;
                font-size: 3rem !important;
            }

            p, div, span {
                font-family: 'Outfit', sans-serif !important;
            }

            /* Modern Buttons */
            div.stButton > button {
                border-radius: 10px !important;
                background-color: #5865F2 !important;
                color: white !important;
                font-weight: 600 !important;
                border: none !important;
                height: 3em !important;
                width: 100% !important;
                transition: all 0.3s ease !important;
            }

            div.stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 5px 15px rgba(88, 101, 242, 0.4) !important;
            }
                
            

            
            /* Secondary Button (Pink/Magenta) */
            div[data-testid="stBaseButton-secondary"] {
                background-color: #EB459E !important;
            }
                
            .stApp div[data-testid="stColumn"] {
                background-color: white !important;
                padding: 2rem !important; /* Padding kam ki */
                border-radius: 3rem !important;
                box-shadow: 1px 10px 30px rgba(0,0,0,0.1) !important; /* Soft shadow */
                text-align: center;
            }
            
            button:hover{
                transform : scale(1.05)}
                


        </style>
    """, unsafe_allow_html=True)

def style_background_home():
    st.markdown("<style>.stApp { background-color: #5865F2 !important; }</style>", unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown("<style>.stApp { background-color: #E0E3FF !important; }</style>", unsafe_allow_html=True)