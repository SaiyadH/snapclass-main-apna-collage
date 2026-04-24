# import streamlit as st

# from supabase import create_client, Client

# supabase: Client = create_client(
#     st.secrets["SUPABASE_URL"],
#     st.secrets["SUPABASE_KEY"]
# )

import streamlit as st
from supabase import create_client, Client

# Secrets se data uthana
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

# Client create karna
supabase: Client = create_client(url, key)

