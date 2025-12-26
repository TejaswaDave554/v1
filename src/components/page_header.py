import streamlit as st
from src.auth.auth_utils import logout_user

def render_page_header(page_title, page_icon="🚗", show_user_info=True, custom_nav=None):

    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"{page_icon} {page_title}")

    with col2:
        if st.session_state.get('logged_in', False) and show_user_info:
            user_name = st.session_state.get('username', 'User')
            st.markdown(f"**Welcome, {user_name}!**")

    if custom_nav:
        cols = st.columns(len(custom_nav))
        for i, nav_item in enumerate(custom_nav):
            with cols[i]:
                if st.button(nav_item["text"],
                           help=nav_item.get("help", "Navigate"),
                           use_container_width=True,
                           type=nav_item.get("type", "secondary"),
                           key=f"nav_{i}"):
                    if nav_item.get("action") == "logout":
                        logout_user()
                        st.success("Logged out!")
                        st.switch_page("app.py")
                    else:
                        st.switch_page(nav_item["page"])
    else:

        render_default_navigation()

    st.divider()

def render_default_navigation():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")

    with col2:
        if st.button("🔐 Login", use_container_width=True):
            st.switch_page("pages/🔐_Login.py")

    with col3:
        if st.button("📝 Register", use_container_width=True):
            st.switch_page("pages/📝_Register.py")

    with col4:
        if st.session_state.get('logged_in', False):
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                logout_user()
                st.success("Logged out!")
                st.switch_page("app.py")
        else:
            st.button("🚪 Logout", disabled=True, use_container_width=True)
