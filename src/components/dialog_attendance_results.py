import streamlit as st
import time
from src.database.db import enroll_student_to_subject
# from src.database.db import create_subject
from src.database.config import supabase
from PIL import Image

@st.dialog("Capture or uplode photos")
def attendance_result_dialog():
    st.write('Please review attendance before conforming.')
