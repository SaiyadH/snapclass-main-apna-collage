import streamlit as st

# def style_base_layout():
#     # Page ko wide mode mein set karne ke liye (Sabse pehle call hona chahiye)
#     st.markdown("""
#         <style>
#             @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');
            
#             # MainMenu, header, footer { visibility: hidden; }
            
#             .stApp {
#                 background-color: #F0F2F6; /* Light clean background */
#             }

#             h1 {
#                 font-family: 'Climate Crisis', sans-serif !important;
#                 color: white !important;
#                 font-size: 3.5rem !important;
#                 margin: 0px !important;
#                 line-height: 1 !important;
#             }
            
#             h2 {
#                 font-family: 'Climate Crisis', sans-serif !important;
#                 color: #2C2F38 !important;
#                 font-size: 3rem !important;
#             }

#             p, div, span {
#                 font-family: 'Outfit', sans-serif !important;
#             }
                
#             div[data-testid='primary'] {
#                 background-color:black;
#             }

#             /* Modern Buttons */
#             div.stButton > button {
#                 border-radius: 10px !important;
#                 background-color: #5865F2 !important;
#                 color: white !important;
#                 font-weight: 600 !important;
#                 border: none !important;
#                 height: 3em !important;
#                 width: 100% !important;
#                 transition: all 0.3s ease !important;
#             }

#             div.stButton > button:hover {
#                 transform: translateY(-2px) !important;
#                 box-shadow: 0 5px 15px rgba(88, 101, 242, 0.4) !important;
#             }
                
            

            
#             /* Secondary Button (Pink/Magenta) */
#             div[data-testid="stBaseButton-secondary"] {
#                 background-color: #EB459E !important;
#             }
                
#             .stApp div[data-testid="stColumn"] {
#                 background-color: white !important;
#                 padding: 2rem !important; /* Padding kam ki */
#                 border-radius: 3rem !important;
#                 box-shadow: 1px 10px 30px rgba(0,0,0,0.1) !important; /* Soft shadow */
#                 text-align: center;
#             }
            
#             button:hover{
#                 transform : scale(1.05)}
                


#         </style>
#     """, unsafe_allow_html=True)

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
                
            # .stApp {
            #     background-color :#5865F2 !important;
            # }
            
            # .stApp  .pink-btn button {
            #     background-color: #EB459E !important;
            #     border: 2px solid #2C2F38 !important;
            #     # background-color: #F0F2F6;
            #     font-family: 'Outfit', sans-serif !important;
            # }
            
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3rem !important;
                line-height:1.1 !important;
                margin-bottom: 0rem !important;
            
            }
            /* Main Headings */
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom: 0rem !important;
                color: black !important;
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

            

            # /* --- PILL BUTTONS (Snap Class Style) --- */
            # div.stButton > button {
            #     border-radius: 50px !important; /* Fully Round */
            #     background-color: #5865F2 !important; /* Brand Blue */
            #     color: white !important;
            #     font-weight: 700 !important;
            #     # padding: 0.5rem 2rem !important;
            #     # border: 2px solid #2C2F38 !important; /* Thick Border like image */
            #     transition: all 0.2s ease-in-out !important;
            # }

            /* Hover Effect */
            div.stButton > button:hover {
                background-color: #4752C4 !important; /* Darker Blue on Hover */
                border-color: #2C2F38 !important;
                # border-width: 3px !important;
                box-shadow: 0 10px 15px rgba(1, 0, 0, 0.5) !important;
                transform: translateY(-3px) scale(1.02) !important;
            }
                
            # # /* Primary Button (Manage Subject selected state) */
            # # div[data-testid="stBaseButton-primary"] {
            # #     # background-color: #5865F2 !important; /* Blue color */
            # #     # color: white !important;
            # #     border: 3px solid #2C2F38 !important;
            # # }

            # # /* Secondary/Pink Button Style */
            # # div[data-testid="stBaseButton-secondary"] {
            # #     background-color: #EB459E !important;
            # #     border: 2px solid #2C2F38 !important;
            # # }

            # /* --- DASHBOARD CARDS (White Boxes) --- */
            # .stApp div[data-testid="stColumn"] {
            #     background-color: white !important;
            #     padding: 0.8rem !important;
            #     border-radius: 2rem !important;
            #     # border: 2px solid #2C2F38 !important; /* Consistent border */
            #     box-shadow: #EB459E !important; /* Neubrutalism Shadow */
            # }
                
            

            # # /* Input Fields rounded */
            # # .stTextInput input {
            # #     border-radius: 15px !important;
            # # }

        </style>
    """, unsafe_allow_html=True)

# import streamlit as st

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



# def style_background_home():
#     st.markdown("""
#             <style>
                
#                 .stApp { 
#                     background-color: #5865F2 !important; 
#                 }

#                 .stApp div[data-teseid="stColumn"] {
#                     background-color: #E0E3FF !important;
#                     padding: 2.5rem !important;
#                     border-radius: 5rem !important;

                
#                 }
                
#             </style>
                
                
                
#             """, unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown("""
                
                <style>
                    .stApp {
                
                        background-color: #E0E3FF !important; 
                    }
                
                    
                </style>
                
                
                """, unsafe_allow_html=True)


