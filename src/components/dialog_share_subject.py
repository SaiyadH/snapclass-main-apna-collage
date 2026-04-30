
import streamlit as st
import segno
import io

from src.database.db import create_subject

@st.dialog("Create New Subject")

def share_subject_dialog(sub_name, sub_code):
    app_domain = "http://localhost:8501"  
    join_url = f"{app_domain}/join?code={sub_code}"

    st.header('Scan to Join Class')

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(out, kind='png', scale=10, border=1)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('**QR Code**')
        st.code(join_url, language='text')
        st.code(sub_code, language='text')
        st.info("Students can use this code to join your class.")

    with c2:
        st.markdown('**QR Code Image**')
        st.image(out.getvalue(), use_column_width=True, caption="Scan this QR code to join the class")

    # st.header(f"Share this code with your students for **{sub_name}**")
    # st.write(f"Share this code with your students for **{sub_name}**")
    # st.code(sub_code, language="text")
    # st.info("Students can use this code to join your class.")

# def create_subject_dialog(teacher_id):
#     st.write("Enter the details of the new subject")
#     sub_id = st.text_input("Subject Code", placeholder="CS101")
#     sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
#     section = st.text_input("Section", placeholder="A")

#     if st.button("Create Subject", use_container_width=True):
#         if sub_id and sub_name and section:
#             try:
#                 create_subject(sub_id, sub_name, section, teacher_id)
#                 st.success("Subject created successfully!")
#                 time.sleep(1)
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"Error: {e}")
#         else:
#             st.warning("Please fill all fields")

# @st.dialog("Share Subject Code")
# def share_subject_dialog(sub_name, sub_code):
#     st.write(f"Share this code with your students for **{sub_name}**")
#     st.code(sub_code, language="text")
#     st.info("Students can use this code to join your class.")