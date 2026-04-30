import streamlit as st
import time
from src.database.db import enroll_student_to_subject
# from src.database.db import create_subject
from src.database.config import supabase
from PIL import Image
from src.database.db import create_attendance


# def show_attendance_results(df, logs):
#     st.write('Please review attendance before conforming.')
#     st.dataframe(df, hide_index=True, width='stretch')

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("Discard", width='stretch'):
#             st.session_state.voice_atttendance_results = None
#             st.session_state.attendance_images = []
#             st.rerun()


#         st.rerun()

#     with col2:
#         if st.button("Discard", width='stretch', type='primary'):
#             try:
#                 create_attendance(logs)
#                 st.toast("Attendance taken")
#                 st.session_state.attendance_images = []
#                 st.session_state.voice_atttendance_results = None
#                 st.rerun()

#             except Exception as e:
#                 st.error('Sync failed!')

    


# @st.dialog("Attendance Reports")
# def attendance_result_dialog(df, logs):
#     show_attendance_results(df, logs)

def show_attendance_results(df, logs):
    st.write('Please review attendance before confirming.')
    
    # 1. FIX: Display DataFrame (use_container_width use karein)
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # 2. FIX: Discard Button (Iske bahar wala st.rerun hata diya)
        if st.button("Discard", use_container_width=True):
            st.session_state.voice_atttendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        # 3. FIX: Button ka naam 'Confirm & Save' kijiye
        if st.button("Confirm & Save", use_container_width=True, type='primary'):
            try:
                if logs:
                    create_attendance(logs)
                    st.toast("Attendance taken successfully!")
                    st.session_state.attendance_images = []
                    st.session_state.voice_atttendance_results = None
                    time.sleep(1) # Toast dikhne ke liye thoda wait
                    st.rerun()
                else:
                    st.error("No data to save!")
            except Exception as e:
                st.error(f'Sync failed: {e}')

@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_results(df, logs)
