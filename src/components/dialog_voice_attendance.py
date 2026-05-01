import streamlit as st
import pandas as pd
from datetime import datetime
from src.database.db import enroll_student_to_subject
# from src.database.db import create_subject
from src.database.config import supabase
from PIL import Image
from src.database.db import create_attendance
from src.pipelines.voice_pipelines import process_bulk_audio
from src.components.dialog_attendance_results import show_attendance_results

@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    
    st.write("Record audio of students saying I am present. Then AI will reecognize the students")

    audio_data = None

    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio', width='stretch', type='primary'):

        if audio_data is None:
            st.error("Pehle audio record kijiye!")
            return # Yahan se code ruk jayega

        with st.spinner('Pressing Audio data'):
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this course")
                return
            condidates_dict = {
                s['students']['student_id'] : s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not condidates_dict:
                st.error('NO enrolled students have voice profiles registerd.')
                return
            
            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(audio_bytes, condidates_dict)

            results, attendance_to_log = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = bool(score > 0)

                results.append ({
                    "Name": student['name'],
                    "ID" : student['student_id'],
                    "Source": ", ".join(score) if is_present else "-",
                    "Status": "✅  Present" if is_present else " ❌ Absent"
                })

                attendance_to_log.append ({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)

                })
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider() 

        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_results(df_results, logs)
