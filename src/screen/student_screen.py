import streamlit as st
import time
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, enroll_student_to_subject, unenroll_student_to_subject
from src.pipelines.voice_pipelines import get_voice_embedding
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card




def student_dashboard():


    # student_data = st.session_state.get('student_data')
    # Safe Student Data Retrieval
    student_info = st.session_state.get('student_data')
    
    # Agar data list/tuple mein aa raha hai toh [1] index lein, warna direct use karein
    if isinstance(student_info, (list, tuple)):
        student_data = student_info[1]
    else:
        student_data = student_info
        
    student_id = student_data['student_id']

    # if student_data:
    #     # Ab ye line 100% chalegi kyunki student_data ek dictionary hai
    #     st.subheader(f"Welcome, {student_data['name']}", text_alignment='right')
    

    # st.header(f"Welcome student Dashboard")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard() 

    with c2:
        st.subheader(f"""Welcome, {student_data['name']}""")
        if st.button("Logout", type="secondary", key="login_back", shortcut="ctrl+b", width='stretch'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)

    with c1:
        st.header("Your Enrolled SUbject")

    with c2:
        if st.button("Enroll in Subject", type='primary', width='stretch', key='enroll_main_btn'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subject = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)


    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)

    for i, sub_node in enumerate(subject):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total":0, "attended": 0})

        def unenroll_button():
            if st.button("Unenroll from this course", type='secondary', width='stretch', icon=":material/delete_forever:", key=f'unenroll_{sid}'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenroll from {sub['name']} successfully!")
                st.rerun()

        with cols[ i % 2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ("📅", 'Total', stats['total']),
                    ("✅", "Attended", stats['attended'])
                ],
                footer_callback = unenroll_button
            )


    footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    # If student is already logged in, show dashboard
    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back to Home", type='secondary', key='loginbackbtn', shortcut='ctrl+b'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<h2 style='text-align: center;'>Login using FaceID</h2>", unsafe_allow_html=True)
    
    # Initialize registration state if not present
    if 'show_reg' not in st.session_state:
        st.session_state.show_reg = False

    photo_source = st.camera_input("Show your face to the camera to login", key="faceid_login")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning your face...'):
            # Using our refined predict_attendance
            detected, all_ids, num_faces, status = predict_attendance(img)

            if num_faces == 0:
                st.warning('No face detected. Please adjust your camera.')
            elif num_faces > 1:
                st.warning('Multiple faces detected. Please stay alone in the frame.')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back, {student['name']}! ✅")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! If you are new, please register below.')
                    st.session_state.show_reg = True

    # Registration Form
    if st.session_state.show_reg:
        with st.container(border=True):
            st.header('📝 Register New Profile')
            new_name = st.text_input("Enter your Full Name", placeholder='e.g. Saiyad Hussain')
            
            st.write("---")
            st.info("🎤 Optional: Enroll your voice for secondary verification.")
            audio_data = st.audio_input('Record: "I am present for the class."')

            if st.button('Create Account', type='primary', width="stretch"):
                if not new_name:
                    st.warning('Please enter your name first!')
                elif not photo_source:
                    st.error('Camera input is required for FaceID.')
                else:
                    with st.spinner('Generating AI Bio-metrics...'):
                        # Process Face
                        img_reg = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img_reg)

                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None

                            # Process Voice if available
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            
                            # Save to Database
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                # Retrain the AI model to recognize the new student
                                train_classifier()
                                
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.success(f'Account created successfully! Welcome {new_name}.')
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error('Database Error: Could not save profile.')
                        else:
                            st.error('Could not capture clear facial features. Try again.')

    footer_dashboard()