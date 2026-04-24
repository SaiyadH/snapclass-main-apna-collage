# import streamlit as st

# import time  # Import ko upar le aaye
# from src.ui.base_layout import style_background_dashboard, style_base_layout
# from src.components.header import header_dashboard
# from src.components.footer import footer_dashboard
# from PIL import Image
# import numpy as np
# from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
# from src.database.db import get_all_students, create_student
# from src.pipelines.voice_pipelines import get_voice_embedding

# def student_dashboard():
#     st.header("DASHBOARD HERE")

# def student_screen():
#     # st.header("Student Screen")

#     style_background_dashboard()
#     style_base_layout()

#     if "student_data" in st.session_state:
#         student_dashboard()
#         return

#     c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

#     with c1:
#         header_dashboard()

#     with c2:
#         if st.button("Go Back to Home", type='secondary', key='loginbackbtn', shortcut='ctrl+b'):
#             st.session_state['login_type'] = None
#             st.rerun()

    
#     st.header("Login using FaceID", text_alignment='center')
#     st.space()
#     st.space()

#     show_registration = False
    
#     photo_source = st.camera_input("Show your face to the camera to login", key="faceid_login")

#     if photo_source :
#         img = np.array(Image.open(photo_source))

#         with st.spinner('AI is scannig..'):
#             detected, all_ids, num_faces = predict_attendance(img)

#             if num_faces == 0:
#                 st.warning('Face not found!')
#             elif num_faces > 1:
#                 st.warning('Face not found!')
#             else :
#                 if detected:
#                     student_id = list(detected.keys())[0]
#                     all_students = get_all_students()

#                     student = next((s for s in all_students if s['student_id'] == student_id), None)

#                     if student :
#                         st.session_state.is_logged_in = True
#                         st.session_state.user_role = 'student'
#                         st.session_state.student_data = student
#                         st.toast(f'Welcome Back {student['name']}')
#                         time.sleep(1)
#                         st.rerun()

#                     else:
#                         st.info('Face not recognized! You might be a new student! ')
#                         show_registration = True


#     if show_registration:
#         with st.container(border=True):
#             st.header('Register new Profile')

#             new_name = st.text_input("Enter your name", placeholder='E.g. Saiyad Hussain')
#             st.info("Enroll your for voice only attendence")

#             audio_data = None

#             try:
#                 audio_data = st.audio_input('Record a short pharse like I am present, my name is Sahnsa.')
#             except Exception :
#                 st.error('Audio Data falled')

#             if st.button('Create Account', type='primary'):
#                 if new_name:
#                     with st.spinner('Creating Profile..'):
#                         img = np.array(Image.open(photo_source))
#                         encodings = get_face_embeddings(img)

#                         if encodings:
#                             face_emb = encodings[0].tolist()

#                             voice_emb = None

#                             if audio_data:
#                                 voice_emb = get_voice_embedding(audio_data.read())
                            
#                             response_data = create_student(new_name, face_embedding = face_emb, voice_embedding = voice_emb )

#                             if response_data:
#                                 train_classifier()
#                                 st.session_state.is_logged_in = True
#                                 st.session_state.user_role = 'student'
#                                 st.session_state.student_data = response_data[0]
#                                 st.toast(f'Profile Create ! Hi {new_name}!')
#                                 time.sleep(1)
#                                 st.rerun()
#                             else:
#                                 st.error('Couldnt capture your facial features for registration')

#                 else:
#                     st.warning('Please enter your name!')

                



#     footer_dashboard()

import streamlit as st
import time
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_student
from src.pipelines.voice_pipelines import get_voice_embedding

def student_dashboard():
    st.header("🎯 Student Dashboard")
    if st.button("Logout"):
        del st.session_state.student_data
        st.rerun()

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

    st.markdown("<h1 style='text-align: center;'>Login using FaceID</h1>", unsafe_allow_html=True)
    
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