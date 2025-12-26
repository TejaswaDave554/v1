import hashlib
import re
import streamlit as st
from config.database import db

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    digits = re.sub(r'[^0-9]', '', phone) or ""
    return len(digits) >= 10

def login_user(user: dict) -> None:
    st.session_state.logged_in = True
    st.session_state.user_id = user["id"]
    st.session_state.username = user.get("username", "")
    st.session_state.user_role = user.get("role", "customer")
    st.session_state.full_name = user.get("full_name") or user.get("username") or "User"

def logout_user() -> None:
    for key in ("logged_in", "user_id", "username", "user_role", "full_name"):
        st.session_state.pop(key, None)

def authenticate_user(username: str, password: str):
    if not username or not password:
        return False, None, "Please fill in all fields"

    try:
        user = db.get_user_by_username(username)
        if not user:
            return False, None, "User not found"

        if user.get("password_hash") != hash_password(password):
            return False, None, "Invalid password"

        return True, user, "Login successful"
    except Exception as e:
        return False, None, f"Database error: {str(e)}"
