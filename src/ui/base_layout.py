import streamlit as st

def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            
            /* Hide Streamlit default elements */
            MainMenu, header, footer { visibility: hidden; }
                
            .block-container {
                padding-top:1.5rem !important;
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 !important;
                margin-bottom: 0rem !important;
            }
                

            /* Main Headings */
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom: 0rem !important;
                color:black !important;
            }
                
            

            /* Standard Text */
            h3, h4, p{
                font-family: 'Outfit', sans-serif !important;
                
            }
                
            button{
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition transform 0.25s ease-to-out !important;
            }
                
            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition transform 0.25s ease-to-out !important;
            }
                
            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition transform 1.25s ease-to-out !important;
            }

            /* Hover Effect */
            div.stButton > button:hover {
                background-color: #4752C4 !important; /* Darker Blue on Hover */
                border-color: #2C2F38 !important;
                # border-width: 3px !important;
                box-shadow: 0 10px 15px rgba(1, 0, 0, 0.5) !important;
                transform: translateY(-3px) scale(1.02) !important;
            }
           

        </style>
    """, unsafe_allow_html=True)


def style_background_home():
    st.markdown("""
        <style>
            /* Poore app ka background */
            .stApp { 
                background-color: #5865F2 !important; 
            }

            /* Column styling */
            [data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important; /* 5rem bahut zyada rounded dikhega */
            }
        </style>
    """, unsafe_allow_html=True)



def style_background_dashboard():
    st.markdown("""
                
                <style>
                    .stApp {
                
                        background-color: #E0E3FF !important; 
                    }
                
                    
                </style>
                
                
                """, unsafe_allow_html=True)


