import streamlit as st

SESSION_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {st.secrets['GENAI_API_KEY']}"
}