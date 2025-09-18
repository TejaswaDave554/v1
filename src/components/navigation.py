"""
Navigation Bar Component - Key-Based Theme Refresh
"""

import streamlit as st
from config.settings import SessionKeys

def render_navigation():
    """Render navigation bar"""
    
    # Get theme for key generation
    theme_key = "dark" if st.session_state.get(SessionKeys.DARK_THEME, False) else "light"
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### 🚗 Chaalak")
    
    with col2:
        if st.button("🏠 Home", key=f"home_btn_{theme_key}", help="Go to home page"):
            st.rerun()
    
    with col3:
        if st.button("📋 Services", key=f"services_btn_{theme_key}", help="View our services"):
            st.info("Services section - Coming soon!")
    
    with col4:
        if st.button("📞 Contact", key=f"contact_btn_{theme_key}", help="Contact us"):
            st.info("Contact section - Coming soon!")
    
    with col5:
        render_theme_toggle()

def render_theme_toggle():
    """Render theme toggle button"""
    current_theme = st.session_state.get(SessionKeys.DARK_THEME, False)
    theme_icon = '🌙' if not current_theme else '☀️'
    theme_text = 'Dark' if not current_theme else 'Light'
    
    if st.button(f"{theme_icon} {theme_text}", key="theme_toggle_btn", 
                 help=f"Switch to {'dark' if not current_theme else 'light'} theme"):
        # Toggle theme
        st.session_state[SessionKeys.DARK_THEME] = not current_theme
        st.success(f"Switching to {theme_text.lower()} mode...")
        # Force complete page refresh
        st.rerun()
