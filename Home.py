import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from src.components.hero_section import render_hero_section
    from src.components.features import render_features
    from src.components.statistics import render_statistics
    from src.components.pricing import render_pricing
    from src.components.testimonials import render_testimonials
    from src.components.footer import render_footer
    from src.utils.custom_css import get_custom_css
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="Chaalak - Professional Chauffeur Services",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown(get_custom_css(), unsafe_allow_html=True)

    try:
        is_logged_in = st.session_state.get('logged_in', False)

        if is_logged_in:
            user_role = st.session_state.get('user_role', 'customer')

            if user_role == 'driver':
                st.switch_page("pages/Driver_Dashboard.py")
            elif user_role == 'admin':
                st.switch_page("pages/Admin_Dashboard.py")
            else:
                st.switch_page("pages/User_Dashboard.py")
        else:
            render_landing_page()
    except Exception as e:
        st.error(f"Application Error: {e}")

def render_landing_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Chaalak</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Professional Chauffeur Services</p>", unsafe_allow_html=True)

    render_hero_section()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Get Started")

        col_login, col_register = st.columns(2)

        with col_login:
            if st.button("Login", use_container_width=True, type="primary"):
                st.switch_page("pages/Login.py")

        with col_register:
            if st.button("Register", use_container_width=True):
                st.switch_page("pages/Register.py")

    render_features()
    render_statistics()
    render_pricing()
    render_testimonials()
    render_footer()

if __name__ == "__main__":
    main()
