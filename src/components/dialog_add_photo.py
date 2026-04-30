import streamlit as st
import time
from src.database.db import enroll_student_to_subject
# from src.database.db import create_subject
from src.database.config import supabase
from PIL import Image

@st.dialog("Capture or uplode photos")
def add_photos_dialog():

    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == "camera" else 'tertiary'
        if st.button('Uploade photos', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type='primary', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if cam_photo:
            st.session_state.attendance__image.append(Image.open(cam_photo))
            st.toast("Photo Captured")
            st.rerun()


    if st.session_state.photo_tab == 'upload':
        upload_files = st.file_uploader("Choose image files", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True,key='dialog_upload')

        if upload_files:
            for f in upload_files:
                st.session_state.attendeance_image(Image.open(f))


            st.toast("Photo CaUploaded successfully.")
            st.rerun()   

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()


