import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.auth.login import render_login_form
from src.utils.custom_css import get_custom_css

st.set_page_config(
    page_title="Chaalak - Login",
    page_icon="🚗",
    layout="centered",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Home"):
        st.switch_page("app.py")
with col2:
    if st.button("Register →"):
        st.switch_page("pages/Register.py")

st.title("Login to Chaalak")
render_login_form()
