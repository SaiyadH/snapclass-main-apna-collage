import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    # 1. Main Card Opening
    # Fixed: border-radius typo and margin-bottom typo
    html = f""" 
        <div style='background:white; border-left:8px solid #EB459E; padding:25px; border-radius: 20px; border: 1px solid #e2e8f0; margin-bottom:20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05)'>
        <h3 style="margin:0; color: #1e293b; font-size: 1.5rem "> {name} </h3>
        <p style="color: #64748b; margin:10px 0; "> Code: <span style="background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius: 5px"> {code} </span> | Section : {section} </p>
    """

    # 2. Stats Section
    if stats:
        html += """ <div style="display:flex; gap: 8px; flex-wrap:wrap; margin-bottom: 15px;"> """
        for icon, label, value in stats:
            html += f'<div style="background: #EB459E10; color:#EB459E; padding: 5px 12px; border-radius: 12px; font-size: 0.9rem"> {icon} <b> {value} </b> {label} </div>'
        html += "</div>" # Closing stats flexbox

    # 3. Closing Main Card Div
    html += "</div>"

    # Rendering
    st.markdown(html, unsafe_allow_html=True)

    # 4. Footer Callback (Buttons wagera ke liye)
    if footer_callback:
        footer_callback()

# --- Example Usage ---
# stats_data = [("📚", "Assignments", 5), ("✅", "Attendance", "90%")]
# subject_cart("Mathematics", "CS101", "A", stats=stats_data)

