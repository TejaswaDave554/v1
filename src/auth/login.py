"""
Login Form Component
"""

import streamlit as st
import time
from config.settings import AppConfig
from src.auth.session_manager import SessionManager
from src.utils.validators import validate_login

def render_login_form():
    """Render login form"""
    with st.form("login_form"):
        st.subheader("🔑 Login to Your Account")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_login, col_forgot = st.columns(2)
        
        with col_login:
            login_submit = st.form_submit_button("🚀 Login", use_container_width=True)
        
        with col_forgot:
            forgot_submit = st.form_submit_button("🔄 Forgot Password?", use_container_width=True)
        
        if login_submit:
            handle_login(username, password)
        
        if forgot_submit:
            handle_forgot_password()

def handle_login(username: str, password: str):
    """Handle login submission"""
    if not validate_login(username, password):
        st.warning("⚠️ Please fill in both fields")
        return
    
    # Demo authentication (replace with database authentication)
    if username == AppConfig.DEMO_USERNAME and password == AppConfig.DEMO_PASSWORD:
        SessionManager.login_user(username, user_id=1)
        st.success("✅ Login successful!")
        st.balloons()
        time.sleep(1)
        st.rerun()
    else:
        st.error("❌ Invalid credentials. Try admin/admin123")

def handle_forgot_password():
    """Handle forgot password"""
    st.info("Password reset link sent to your email!")

def authenticate_user(username: str, password: str) -> dict:
    """Authenticate user against database (future implementation)"""
    # TODO: Implement database authentication
    # from config.database import db_manager
    # from src.models.user import User
    # return User.authenticate(username, password)
    pass
