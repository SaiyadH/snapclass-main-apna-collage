import streamlit as st
import time
# from src.database.db import create_subject
from src.database.config import supabase



@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', use_container_width=True):
        if join_code:
            # 1. Check if Subject exists
            res = supabase.table('subjects').select('subject_id, name').eq('subject_code', join_code).execute()
            
            if res.data:
                subject = res.data[0]
                
                # --- SAFE STUDENT ID EXTRACTION (Main Fix) ---
                student_info = st.session_state.get('student_data')
                
                # Agar dictionary hai
                if isinstance(student_info, dict):
                    student_id = student_info.get('student_id')
                # Agar tuple hai (jaisa aapke system mein aksar aa raha hai)
                elif isinstance(student_info, (list, tuple)):
                    # Check karo ki 2nd element dictionary hai ya nahi
                    if len(student_info) > 1 and isinstance(student_info[1], dict):
                        student_id = student_info[1].get('student_id')
                    else:
                        student_id = student_info[0] # Fallback to first element
                else:
                    student_id = None

                if student_id:
                    # 2. Check if already enrolled
                    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                    
                    if check.data:
                        st.warning('You are already enrolled in this program')
                    else:
                        # 3. Final Enrollment
                        from src.database.db import enroll_student_to_subject
                        enroll_student_to_subject(student_id, subject['subject_id'])
                        st.success(f'Successfully enrolled in {subject["name"]}!')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Error: Student ID not found in session. Please re-login.")
            else:
                st.error("Invalid Subject Code!")
        else:
            st.warning('Please enter a subject code')