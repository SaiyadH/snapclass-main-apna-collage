
# import streamlit as st
# import time  # Import ko upar le aaye
# from src.ui.base_layout import style_background_dashboard, style_base_layout
# from src.components.header import header_dashboard
# from src.components.footer import footer_dashboard
# from src.components.subject_card import subject_card
# # Duplicate imports saaf kar diye
# from src.database.db import  check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
# # from src.components.dialog_create_subject import create_subject_dialog
# # In dono ko alag-alag files se import karo
# from src.components.dialog_create_subject import create_subject_dialog
# from src.screen.student_screen import share_subject_dialog
# # from src.screen.student_screen import student_screen



import streamlit as st
import time
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
# SAHI IMPORT:
from src.components.dialog_create_subject import create_subject_dialog, share_subject_dialog





def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'teacher_data'  in st.session_state:
        teacher_dashboard()
        # st.session_state.teacher_login_type = 'login'

    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()


def teacher_dashboard():

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    

    # Error Fix: Data access safety
    teacher_data = st.session_state.teacher_data 

    st.header(f"Welcome Teacher Dashboard")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()  
    with c2:
        # TUPLE ERROR FIX: Agar dictionary hai toh ['name'], agar tuple hai toh [1]
        try:
            name = teacher_data['name']
        except TypeError:
            name = teacher_data[1] # Database row tuple index 1
            
        st.subheader(f"Welcome , {name}!")

        if st.button("Logout", type="secondary", key="login_back"):
            st.session_state['is_logged_in'] = False
            if 'teacher_data' in st.session_state:
                del st.session_state.teacher_data
            st.rerun()

    st.write("") # st.space() agar custom function nahi hai toh st.write use karein

    # Tabs selection UI
    tab1, tab2, tab3 = st.columns(3)    

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, width='stretch'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subject' else 'tertiary'
        if st.button('Manage Subjects', type=type2, width='stretch'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()

    with tab3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_record' else 'tertiary'
        if st.button('Attendance Records', type=type3, width='stretch'):
            st.session_state.current_teacher_tab = 'attendance_record'
            st.rerun()

    # --- UI FIX: Inhe 'with tab3' se bahar rakhein taaki ye full width dikhein ---
    st.divider()
    
    current_tab = st.session_state.get('current_teacher_tab', 'take_attendance')

    if current_tab == 'take_attendance':
        teacher_tab_take_attendance()

    elif current_tab == 'manage_subject':
        teacher_tab_manage_subjects()

    elif current_tab == 'attendance_record':
        teacher_tab_attendance_record()

    footer_dashboard()

# def teacher_dashboard():
#     teacher_data = st.session_state.teacher_data  # Assuming you set this after login

#     c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
#     with c1:
#         header_dashboard()  
#     with c2:
#         st.subheader(f"Welcome, {teacher_data['name']}!")

#         if st.button("Logout", type="secondary", key="login_back"):
#             st.session_state['is_logged_in'] = False
#             del st.session_state.teacher_data
#             st.rerun()

#     st.space()

#     tab1, tab2, tab3 = st.columns(3)    

#     with tab1:
#         type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
#         if st.button('Take Attendence', type=type1, width='stretch', icon=':material/ar_on_you:'):
#             st.session_state.current_teacher_tab = 'take_attendance'
#             st.rerun()

#     with tab2:
#         type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subject' else 'tertiary'
#         if st.button('Manage subjects',type=type2, width='stretch', icon=':material/book_ribbon:'):
#             st.session_state.current_teacher_tab = 'manage_subject'
#             st.rerun()

#     with tab3:
#         type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_record' else 'tertiary'
#         if st.button('Attendance Records',type=type3, width='stretch', icon=':material/card_stack:'):
#             st.session_state.current_teacher_tab = 'attendance_record'
#             st.rerun()

#         st.divider()
           
#         if st.session_state.current_teacher_tab == 'take_attendance':
#             teacher_tab_take_attendance()

#         if st.session_state.current_teacher_tab == 'manage_subject':
#             teacher_tab_manage_subjects()

#         if st.session_state.current_teacher_tab == 'attendance_record':
#             teacher_tab_attendance_record()

    

#     footer_dashboard()

def teacher_tab_take_attendance():
    st.header('Take AI Attendance')

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)

    with col1:
        st.header('manage Subject', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    # CREATE
    # LIST all  SUBJECTS
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub.get('total_students', 0)),
                ("📅", "Classes", sub.get('total_classes', 0)),
            ]

        def share_btn():
            if st.button(f"Share Code: {sub['name']}", key = f"share_{sub['subject_code']}"):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()

        
        subject_card(
            name = sub['subject_name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats = stats,
            footer_callback = share_btn

        )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")
                      

def teacher_tab_attendance_record():
    st.header('attendance Record')

def login_teacher(username, password):
    if not username or not password:
        return False, "Please enter both username and password."
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.teacher_data = teacher  # Store teacher data in session state
        st.session_state.is_teacher_logged_in = True
        st.session_state.user_role = 'teacher'
        return True, "Login successful!"
    
    return False, "Invalid username or password."

# def login_teacher(username, password):
#     if not username or not password:
#         return False
    
#     teacher = teacher_login(username, password)
#     if teacher:
#         st.session_state.teacher_data = teacher  # Store teacher data in session state
#         st.session_state.is_teacher_logged_in = True
#         st.session_state.user_role = 'teacher'
#         return True
    

    
#     return False


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()  
    with c2:
        if st.button("Go back to Dashboard", type="secondary", key="login_back"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using password", text_alignment='center')
    st.space()
    st.space()
    
    teacher_username = st.text_input("Enter Username", placeholder="Enter your username", key="user_login")
    teacher_password = st.text_input("Enter Password", placeholder="Enter your password", type="password", key="pass_login")

    st.divider()

    btcn1, btcn2 = st.columns(2, gap="large")

    with btcn1:
        # Passkey wala icon "key" use karein (st.version >= 1.35)
        if st.button("Login ", width="stretch", shortcut="ctrl+enter", key="btn_login_submit"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!", icon="✅")
                import time
                time.sleep(1)  # Thoda time do user ko message padhne ke liye
                st.rerun()  # Screen refresh kar do taaki dashboard ya teacher specific screen

            else:
                st.error("Invalid username or password.")

    with btcn2:
        if st.button("Register Instead", type="primary", width="stretch", key="btn_goto_reg"):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    footer_dashboard()

def register_teacher(teacher_username, teacher_password, teacher_pass_confirm, teacher_name):   
    if not teacher_username or not teacher_password or not teacher_name:
        return False, "All fields are required."
    
    if check_teacher_exists(teacher_username):
        return False, "Username already exists." 
    
    if teacher_password != teacher_pass_confirm:
        return False, "Passwords do not match."
    
    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Registered successfully! Redirecting to login..."
    except Exception as e:
        # 'Unexpected error' ko mita kar ye likhein
        return False, f"Actual Error: {str(e)}"

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()  
    with c2:
        if st.button("Go to Dashboard", type="secondary", key="reg_back", shortcut="ctrl+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your teacher profile")

    teacher_username = st.text_input("Enter Username", placeholder="Enter your username", key="user_reg")
    teacher_name = st.text_input("Enter Name", placeholder="Enter your name", key="name_reg")
    teacher_password = st.text_input("Enter Password", placeholder="Enter your password", type="password", key="pass_reg")
    teacher_confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password", key="pass_conf_reg")

    st.divider()
    btcn1, btcn2 = st.columns(2)

    with btcn1:
        # Registration logic
        if st.button("Register Now", width="stretch", key="btn_reg_final"):
            success, message = register_teacher(teacher_username, teacher_password, teacher_confirm_password, teacher_name)
            if success:
                st.success(message)
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)

    with btcn2:
        # Spelling sahi ki aur st.rerun add kiya
        if st.button("Login Instead", type="primary", width="stretch", key="btn_back_to_login_ui"):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()