# import streamlit as st

# from src.screen.teacher_screen import teacher_screen
# from src.screen.student_screen import student_screen
# from src.screen.home_screen import home_screen


# def main():
#     if 'login_type' not in st.session_state:
#         st.session_state['login_type'] = None

#     match st.session_state['login_type']:
#         case 'Teacher':
#             teacher_screen()
#         case 'Student':
#             student_screen()
#         case None:
#             home_screen()

# main()

import streamlit as st

# 1. YE LINE SABSE UPAR HONI CHAHIYE (No Exception!)
st.set_page_config(
    page_title="Apna Class",
    page_icon="🎓",
    layout="wide", # Isse aapka dashboard poori screen par failega
    initial_sidebar_state="collapsed"
)

# Imports ko hamesha set_page_config ke niche rakhein
from src.screen.teacher_screen import teacher_screen
from src.screen.student_screen import student_screen
from src.screen.home_screen import home_screen


def main():
    # Session state initialization
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # Screen routing logic
    match st.session_state['login_type']:
        case 'Teacher':
            teacher_screen()
        case 'Student':
            student_screen()
        case _: # 'case None' ki jagah default case use karna behtar hai
            home_screen()

if __name__ == "__main__":
    main()
    
