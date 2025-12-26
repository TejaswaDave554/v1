import streamlit as st
from config.settings import SessionKeys

def render_navigation():

    theme_key = "dark" if st.session_state.get(SessionKeys.DARK_THEME, False) else "light"

    if 'active_section' not in st.session_state:
        st.session_state.active_section = None

    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

    with col1:
        st.markdown("

    with col2:
        is_home_active = st.session_state.active_section == 'home'
        home_icon = "🏠 ▲" if is_home_active else "🏠 ▼"

        if st.button(home_icon, key=f"home_btn_{theme_key}", help="Toggle home information"):
            if is_home_active:
                st.session_state.active_section = None
            else:
                st.session_state.active_section = 'home'

    with col3:
        is_services_active = st.session_state.active_section == 'services'
        services_icon = "📋 ▲" if is_services_active else "📋 ▼"

        if st.button(services_icon, key=f"services_btn_{theme_key}", help="Toggle services information"):
            if is_services_active:
                st.session_state.active_section = None
            else:
                st.session_state.active_section = 'services'

    with col4:
        is_contact_active = st.session_state.active_section == 'contact'
        contact_icon = "📞 ▲" if is_contact_active else "📞 ▼"

        if st.button(contact_icon, key=f"contact_btn_{theme_key}", help="Toggle contact information"):
            if is_contact_active:
                st.session_state.active_section = None
            else:
                st.session_state.active_section = 'contact'

    with col5:
        is_theme_active = st.session_state.active_section == 'theme'
        theme_icon = "🎨 ▲" if is_theme_active else "🎨 ▼"

        if st.button(theme_icon, key="theme_info_btn", help="Toggle theme information"):
            if is_theme_active:
                st.session_state.active_section = None
            else:
                st.session_state.active_section = 'theme'

    if st.session_state.active_section == 'home':
        st.success()

    elif st.session_state.active_section == 'services':
        st.info()

    elif st.session_state.active_section == 'contact':
        st.warning()

    elif st.session_state.active_section == 'theme':
        st.info()

def handle_navigation_actions():

    pass
