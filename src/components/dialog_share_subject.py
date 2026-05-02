
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



    app_domain = "ApnaClass-main.streamlit.app"  # Aapka deployed app ka domain
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

