import streamlit as st
import time
# from src.database.db import create_subject
from src.database.config import supabase

@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher to enroll.")
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button("Enroll Now", type = 'primary', width='stretch', use_container_width=True):
        if join_code:
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                subject_id = st.session_state.student_data['student_id']

                ckeck = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()