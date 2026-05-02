import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
# SAHI IMPORT:
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import create_attendance, get_attendance_for_teacher




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

    # Error Fix: Data access safety
    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard() 

    with c2:

        st.subheader(f"Welcome, {teacher_data['name']}", text_alignment='right')

        if st.button("Logout", type="secondary", key="login_back", shortcut="ctrl+b", width='stretch'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()


    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'        

    # Tabs selection UI
    tab1, tab2, tab3 = st.columns(3)    

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subject' else 'tertiary'
        if st.button('Manage Subject', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()

    with tab3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_record' else 'tertiary'
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/cards_stack:'):
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


def teacher_tab_take_attendance():

    # Safe Teacher ID Retrieval
    teacher_info = st.session_state.get('teacher_data')
    if isinstance(teacher_info, (list, tuple)):
        teacher_id = teacher_info[1]['teacher_id']
    else:
        teacher_id = teacher_info['teacher_id']

    # teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subject yet! Please create one to begin!')

    subject_options = {f"{s['name']} - {s['subject_code']}" : s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added photos")
        galary_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with galary_cols[idx % 4]:
                st.image(img, width='stretch', caption=f"Photo {idx+1}")
        
    has_photos = bool(st.session_state.attendance_images)

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear All photos', width='stretch', type='tertiary', icon=':material/delete:',disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate (st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    # detected, _, _ = predict_attendance(img_np)
                    detected, *others = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course")

                else:

                    results, attendance_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append ({
                            "Name": student['name'],
                            "ID" : student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅  Present" if is_present else " ❌ Absent"
                        })

                        attendance_to_log.append ({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)

                        })

            attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    
    with c3: 
        if st.button('Use Voice attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)






# def teacher_tab_manage_subjects():
#     st.header('Take AI  Manage Subject')

def teacher_tab_manage_subjects():

    # Header logic
    # st.markdown('<h1 style="font-size:4rem; color:#2C2F38;">Manage<br>Subjects</h1>', unsafe_allow_html=True)

    # Safety Check: Agar data nahi hai toh login page par bhejo
    if 'teacher_data' not in st.session_state:
        st.error("Session Expired. Please Login again.")
        st.rerun()

    teacher_data = st.session_state.teacher_data
    
    # Check karo agar data tuple hai toh index lo, varna key lo
    if isinstance(teacher_data, (list, tuple)):
        teacher_id = teacher_data[0]  # Maan lete hain ID pehle column (0) par hai
    else:
        teacher_id = teacher_data.get('teacher_id')
        
    # Ab teacher_id ko niche use karo...

    try:
        if isinstance(teacher_data, (list, tuple)):
            teacher_id = teacher_data[0] # BigInt ID pehle column mein honi chahiye
        else:
            teacher_id = teacher_data.get('teacher_id')
        
        # Check karein ki teacher_id waqai ek number hai ya nahi
        if teacher_id is None or teacher_id is False:
            st.error("Invalid Teacher ID. Please Re-login.")
            return

    except Exception as e:
        st.error(f"Data Error: {e}")
        return


    # teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header('manage Subject')

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
            if st.button(f"Share Code: {sub['name']}", key = f"share_{sub['subject_code']}", icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()

        
        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats = stats,
            footer_callback = share_btn

        )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")
                      
import streamlit as st
from src.database.db import create_subject # Database function import karein

# @st.dialog("Create New Subject")
def create_subject_dialog(t_id):
    # Inputs le rahe hain
    s_name = st.text_input("Subject Name (e.g. Machine Learning)")
    s_code = st.text_input("Subject Code (e.g. AI-302)")
    s_section = st.text_input("Section (e.g. A)")

    if st.button("Submit & Create"):
        if s_name and s_code and s_section:
            # Database function call kar rahe hain
            # Yahan hum parameters bhej rahe hain, dictionary nahi (isliye KeyError nahi aayega)
            res = create_subject(s_code, s_name, s_section, t_id)
            if res:
                st.success(f"Subject '{s_name}' created successfully!")
                st.rerun() # Refresh taaki naya subject list mein dikhne lage
        else:
            st.warning("Please fill all the fields!")



def teacher_tab_attendance_record():
    st.header('attendance Record')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return st.info("No attendance records found for your subjects.")
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else "N/A",  # Grouping ke liye seconds hata diye
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else "N/A",
            "Subject":r['subjects']['name'] if r.get('subjects') else "N/A",
            "Subject code": r['subjects']['subject_code'] if r.get('subjects') else "N/A",
            "is_present": bool(r.get('is_present'))
        })

    df = pd.DataFrame(data)

    summary = ( df.groupby(['ts_group','Time', 'Subject', 'Subject code']).agg(
            Present_Count = ('is_present', 'sum'),
            Total_count = ('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / " + summary['Total_count'].astype(str) + 'Students'
    )

    desplay_df = ( summary.sort_values(by='ts_group', ascending=False)
                   [['Time', 'Subject', 'Subject code', 'Attendance Stats']]
                ) 

    st.dataframe(desplay_df, width='stretch', hide_index=True, use_container_width=True)              



def login_teacher(username, password):
    if not username or not password:
        return False, "Please enter both username and password."
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.teacher_data = teacher  # Store teacher data in session state
        st.session_state.is_teacher_logged_in = True
        st.session_state.user_role = 'teacher'
        st.success("Login successful!")
        st.rerun()
        # return True, "Login successful!"
    else:
        st.error("Invalid username or password.")
    
    # return False, "Invalid username or password."



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
        if st.button("Login ",  icon=':material/passkey:', width="stretch", shortcut="ctrl+enter", key="btn_login_submit"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!", icon="✅")
                import time
                time.sleep(1)  # Thoda time do user ko message padhne ke liye
                st.rerun()  # Screen refresh kar do taaki dashboard ya teacher specific screen

            else:
                st.error("Invalid username or password.")

    with btcn2:
        if st.button("Register Instead", type="primary", icon=':material/passkey:', width="stretch", key="btn_goto_reg"):
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

    st.space()
    st.space()

    teacher_username = st.text_input("Enter Username", placeholder="Enter your username", key="user_reg")
    teacher_name = st.text_input("Enter Name", placeholder="Enter your name", key="name_reg")
    teacher_password = st.text_input("Enter Password", placeholder="Enter your password", type="password", key="pass_reg")
    teacher_confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password", key="pass_conf_reg")

    st.divider()

    btcn1, btcn2 = st.columns(2)

    with btcn1:
        # Registration logic
        if st.button("Register Now", icon=':material/passkey:', width="stretch", key="btn_reg_final"):
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
        if st.button("Login Instead", type="primary",  icon=':material/passkey:', width="stretch", key="btn_back_to_login_ui"):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()