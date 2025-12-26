import streamlit as st
from datetime import datetime, timedelta

SESSION_TIMEOUT_MINUTES = 30

def check_session_timeout():
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
        return False

    last_activity = st.session_state.last_activity
    if datetime.now() - last_activity > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        logout_user()
        return True

    st.session_state.last_activity = datetime.now()
    return False

def logout_user():
    keys_to_clear = ['logged_in', 'user_id', 'username', 'user_role', 'full_name', 'last_activity']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def is_logged_in():
    if not st.session_state.get('logged_in', False):
        return False

    if check_session_timeout():
        return False

    return True
