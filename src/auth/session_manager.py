import streamlit as st
from config.settings import SessionKeys

class SessionManager:

    @staticmethod
    def initialize_session():

        defaults = {
            SessionKeys.LOGGED_IN: False,
            SessionKeys.USER_NAME: "",
            SessionKeys.USER_ID: None,
            SessionKeys.DARK_THEME: False,
            SessionKeys.SHOW_DEMO_INFO: True,
            SessionKeys.CURRENT_PAGE: "home"
        }

        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def login_user(username: str, user_id: int = None):

        st.session_state[SessionKeys.LOGGED_IN] = True
        st.session_state[SessionKeys.USER_NAME] = username
        st.session_state[SessionKeys.USER_ID] = user_id

    @staticmethod
    def logout_user():

        st.session_state[SessionKeys.LOGGED_IN] = False
        st.session_state[SessionKeys.USER_NAME] = ""
        st.session_state[SessionKeys.USER_ID] = None

    @staticmethod
    def is_logged_in() -> bool:

        return st.session_state.get(SessionKeys.LOGGED_IN, False)

    @staticmethod
    def get_current_user() -> str:

        return st.session_state.get(SessionKeys.USER_NAME, "")

    @staticmethod
    def get_user_id() -> int:

        return st.session_state.get(SessionKeys.USER_ID)

    @staticmethod
    def toggle_theme():

        current_theme = st.session_state.get(SessionKeys.DARK_THEME, False)
        st.session_state[SessionKeys.DARK_THEME] = not current_theme

        if st.session_state[SessionKeys.DARK_THEME]:
            st._config.set_option('theme.base', 'dark')
        else:
            st._config.set_option('theme.base', 'light')
