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
        st.image("https://i.pinimg.com/736x/c5/5a/84/c55a843b1ac7c09f49502d38b7ed0cd3.jpg", width=100) 

        if st.button("Login as Student", type="primary", icon_position="right"):
            st.session_state['login_type'] = 'Student'
            st.rerun()
        

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.pinimg.com/736x/45/ba/d2/45bad2ff0901cfbce8b037d63c3764b3.jpg", width=100)

        if st.button("Login as Teacher", type="primary", icon_position="right"):
            st.session_state['login_type'] = 'Teacher'
            st.rerun()
        

    footer_home()


# import streamlit as st
# from src.components.header import header_home
# from src.ui.base_layout import style_base_layout, style_background_home
# from src.components.footer import footer_home

# def home_screen():
#     # 1. Background aur Base Style hamesha upar rakhein
#     style_background_home()
#     style_base_layout()
    
#     # 2. Header
#     header_home()

#     # Thodi gap dene ke liye
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     # 3. Columns setup (gap="large" se visibility clear hoti hai)
#     col1, col2 = st.columns(2, gap="large")

#     with col1:
#         # Card style container manually through markdown if needed, 
#         # or just keep it clean with alignment
#         st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
#         st.header("I'm a Student")
        
#         # Sahi Image aur Caption (Student ke liye Student ki image)
#         st.image("https://i.pinimg.com/736x/c5/5a/84/c55a843b1ac7c09f49502d38b7ed0cd3.jpg", 
#                  use_container_width=True) 

#         if st.button("Login as Student", type="primary", icon="school", key="std_btn"):
#             st.session_state['login_type'] = 'Student'
#             st.rerun()
#         st.markdown("</div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
#         st.header("I'm a Teacher")
        
#         # Sahi Image (Teacher ke liye Teacher ki image)
#         st.image("https://i.pinimg.com/736x/45/ba/d2/45bad2ff0901cfbce8b037d63c3764b3.jpg", 
#                  use_container_width=True)

#         if st.button("Login as Teacher", type="primary", icon="instacart", key="tch_btn"):
#             st.session_state['login_type'] = 'Teacher'
#             st.rerun()
#         st.markdown("</div>", unsafe_allow_html=True)

#     # 4. Footer
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     footer_home()