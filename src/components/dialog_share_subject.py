
import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(sub_name, sub_code):
    # --- CSS Injection: Isse background white aur text black/visible hoga ---
    st.markdown("""
        <style>
            /* Dialog ke content ka background white karne ke liye */
            div[data-testid="stDialog"] div[role="dialog"] {
                background-color: white !important;
            }
            /* Saare text ko black karne ke liye taaki white background par dikhe */
            div[data-testid="stDialog"] p, 
            div[data-testid="stDialog"] h2, 
            div[data-testid="stDialog"] label {
                color: #31333F !important;
            }
        </style>
    """, unsafe_allow_html=True)



    app_domain = "APNACLASS-main.streamlit.app"  # Aapka deployed app ka domain
    join_url = f"{app_domain}/join?code={sub_code}"

    st.header(f'Scan to Join {sub_name}')

    # QR code generate karein (White background ke saath)
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1, light='white', dark='black')

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<p style='color: white; font-color:white; font-weight: bold;'>Copy Code</p>", unsafe_allow_html=True)

        st.code(join_url, language='text')
        st.code(sub_code, language='text')
        st.info("Copy this link to share on WhatsApp and Email.")

    with c2:
        st.markdown('**QR Code Image**')
        st.image(out.getvalue(), caption="Scan this QR code to join the class")



# @st.dialog("Share Class Link")
# def share_subject_dialog(sub_name, sub_code):
#     app_domain = "http://localhost:8501"  
#     join_url = f"{app_domain}/join?code={sub_code}"

#     # Use a specific color for the header to ensure it's visible
#     st.markdown(f"<h2 style='color: white;'>Scan to Join {sub_name}</h2>", unsafe_allow_html=True)

#     qr = segno.make(join_url)
#     out = io.BytesIO()

#     # light='white' sets the QR background
#     # dark='black' keeps the modules readable
#     qr.save(out, kind='png', scale=10, border=1, light='white', dark='black')

#     c1, c2 = st.columns(2)

#     with c1:
#         # Using HTML to force text color to white
#         st.markdown("<p style='color: white; font-weight: bold;'>Copy Code</p>", unsafe_allow_html=True)
#         st.code(join_url, language='text')
#         st.code(sub_code, language='text')
#         st.info("Copy this link to share on WhatsApp and Email.")

#     with c2:
#         st.markdown("<p style='color: white; font-weight: bold;'>QR Code Image</p>", unsafe_allow_html=True)
#         st.image(out.getvalue(), caption="Scan this QR code to join the class")



# # from src.database.db import create_subject

# @st.dialog("Share Class Link")

# def share_subject_dialog(sub_name, sub_code):
#     app_domain = "http://localhost:8501"  
#     join_url = f"{app_domain}/join?code={sub_code}"

#     st.header(f'Scan to Join {sub_name}')

#     qr = segno.make(join_url)

#     out = io.BytesIO()

#     qr.save(out, kind='png', scale=10, border=1)

#     c1, c2 = st.columns(2)

#     with c1:
#         st.markdown('**Copy Code**')
#         st.code(join_url, language='text')
#         st.code(sub_code, language='text')
#         st.info("Copy this link to share on Watsapp and Email.")

#     with c2:
#         st.markdown('**QR Code Image**')
#         st.image(out.getvalue(), caption="Scan this QR code to join the class")


# @st.dialog("Create New Subject")
# def create_subject_dialog(t_id):
#     # Input fields
#     # Note: st.text_input ka result seedha variable mein jata hai
#     sub_name = st.text_input("Subject Name (e.g. Mathematics)")
#     sub_code = st.text_input("Subject Code (e.g. CS101)")
#     sub_section = st.text_input("Section (e.g. A)")

#     if st.button("Create Subject"):
#         if sub_name and sub_code and sub_section:
#             # Backend function call
#             res = create_subject(sub_code, sub_name, sub_section, t_id)
#             if res:
#                 st.success(f"Subject '{sub_name}' Created Successfully!")
#                 st.rerun()
#         else:
#             st.error("Please fill all the fields!")

# # Share Dialog (Jo aapne QR code ke liye banaya hai)
# @st.dialog("Share Subject")
# def share_subject_dialog(sub_name, sub_code):
#     app_domain = "http://localhost:8501"  
#     join_url = f"{app_domain}/join?code={sub_code}"

#     st.header(f'Scan to Join {sub_name}')
#     qr = segno.make(join_url)
#     out = io.BytesIO()
#     qr.save(out, kind='png', scale=10, border=1)

#     c1, c2 = st.columns(2)
#     with c1:
#         st.write(f"**Code:** `{sub_code}`")
#         st.info("Students can use this code to join your class.")
#     with c2:
#         st.image(out.getvalue(), caption="Scan to join")