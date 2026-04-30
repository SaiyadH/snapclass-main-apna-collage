import streamlit as st
import time
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject",type='primary', width='stretch',use_container_width=True):
        if sub_id and sub_name and section:
            try:
                create_subject(sub_id, sub_name, section, teacher_id)
                # st.success("Subject created successfully!")
                st.toast("Subject created successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill all fields")

@st.dialog("Share Subject Code")
def share_subject_dialog(sub_name, sub_code):
    st.write(f"Share this code with your students for **{sub_name}**")
    st.code(sub_code, language="text")
    st.info("Students can use this code to join your class.")