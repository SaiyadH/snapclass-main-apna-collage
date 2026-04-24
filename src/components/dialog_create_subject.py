# # import streamlit as st
# # from src.database.db import create_subject

# # @st.dialog("Create New Subject")
# # def create_subject_dialog(teacher_id):
# #     st.write("Enter the details of new subject")
# #     sub_id = st.text_input("Subject_code", placeholder='CS101')
# #     sub_name = st.text_input("Subject Name", placeholder="Introduction of Computer Science")
# #     sub_section = st.text_input("Section", placeholder="A")


# #     if st.button("Create Subject Now", type="primary", width='stretch'):
# #         if sub_id and sub_name and sub_section:
# #             try:
# #                 create_subject(sub_id, sub_name, sub_section, teacher_id)
# #                 st.toast("Subject created succesfully!")
# #                 st.rerun()

# #             except Exception as e:
# #                 st.error(f", {str(e)}")
# #         else:
# #             st.warning("Please fill all the feilds")

# import streamlit as st
# from src.database.db import create_subject

# @st.dialog("Create New Subject")
# def create_subject_dialog(teacher_id):
#     st.write("Enter the details of new subject")
    
#     # Inputs
#     sub_id = st.text_input("Subject Code", placeholder='CS101')
#     sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
#     sub_section = st.text_input("Section", placeholder="A")

#     # Button: use_container_width=True use karein full width ke liye
#     if st.button("Create Subject Now", type="primary", use_container_width=True):
#         if sub_id and sub_name and sub_section:
#             try:
#                 create_subject(sub_id, sub_name, sub_section, teacher_id)
                
#                 # Success feedback
#                 st.success("Subject created successfully!") 
                
#                 # Thoda wait ya direct rerun
#                 st.rerun()

#             except Exception as e:
#                 # Error message formatting sahi ki hai
#                 st.error(f"Error: {str(e)}")
#         else:
#             st.warning("Please fill all the fields")

# # src/components/dialog_create_subject.py file mein ye add karein:

# @st.dialog("Share Subject Code")
# def share_subject_dialog(sub_name, sub_code):
#     st.write(f"Share this code with your students for **{sub_name}**")
#     st.code(sub_code, language="text")
#     st.info("Students can use this code to join your class.")


import streamlit as st
import time
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject", use_container_width=True):
        if sub_id and sub_name and section:
            try:
                create_subject(sub_id, sub_name, section, teacher_id)
                st.success("Subject created successfully!")
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