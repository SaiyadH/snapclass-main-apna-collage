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
    st.write("Record audio of students saying 'I am present'. Then AI will recognize the students.")

    # Audio input setup
    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio', width='stretch', type='primary'):
        if audio_data is None:
            st.error("Pehle audio record kijiye!")
            return 

        with st.spinner('Processing Audio data...'):
            # Fetch students
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this course")
                return

            # Prepare candidate embeddings
            condidates_dict = {
                s['students']['student_id'] : s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not condidates_dict:
                st.error('No enrolled students have voice profiles registered.')
                return
            
            # Read bytes and process
            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, condidates_dict)

            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            # --- THRESHOLD SETTING ---
            # AI match score agar 0.5 se zyada hai tabhi present mark karein
            threshold = 0.5 

            for node in enrolled_students:
                student = node['students']
                # Get score, default 0.0 if not found
                score = detected_scores.get(student['student_id'], 0.0)
                
                # Check presence based on threshold
                is_present = score >= threshold

                results.append({
                    "Name": student['name'],
                    "ID" : student['student_id'],
                    # FIX: score ko string mein convert kiya join ke bajaye
                    "Source": f"Score: {score:.2f}" if is_present else "-", 
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })

            # Save to session state
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)
            # Force rerun to show results immediately
            st.rerun()

    # Display Results
    if 'voice_attendance_results' in st.session_state:
        st.divider() 
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_results(df_results, logs)