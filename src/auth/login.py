import streamlit as st
from src.auth.auth_utils import login_user, authenticate_user
from src.utils.error_logger import log_login_attempt

def render_login_form():
    with st.form("login_form"):
        st.subheader("Login to Your Account")

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns(2)

        with col1:
            login_btn = st.form_submit_button("Login", use_container_width=True, type="primary")

        with col2:
            register_btn = st.form_submit_button("Register Instead", use_container_width=True)

        if login_btn:
            if not username or not password:
                st.error("Please fill in all fields")
            else:
                try:
                    success, user, message = authenticate_user(username, password)

                    log_login_attempt(username, success)

                    if success:
                        login_user(user)
                        st.success(f"Welcome back, {st.session_state.get('full_name', 'User')}!")

                        role = user.get("role", "customer")
                        if role == "driver":
                            st.switch_page("pages/Driver_Dashboard.py")
                        elif role == "admin":
                            st.switch_page("pages/Admin_Dashboard.py")
                        else:
                            st.switch_page("pages/User_Dashboard.py")
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
                    st.stop()

        if register_btn:
            st.switch_page("pages/Register.py")
