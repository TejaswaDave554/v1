"""
Chaalak - Professional Chauffeur Services
Main Streamlit Application Entry Point
"""

import streamlit as st
from config.settings import AppConfig
from src.auth.session_manager import SessionManager
from src.components.navigation import render_navigation
from src.components.hero_section import render_hero_section
from src.components.features import render_features
from src.components.statistics import render_statistics
from src.components.pricing import render_pricing
from src.components.testimonials import render_testimonials
from src.components.footer import render_footer
from src.auth.login import render_login_form
from src.auth.register import render_register_form
from src.utils.styles import load_custom_styles

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title=AppConfig.APP_TITLE,
        page_icon=AppConfig.APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom styles
    load_custom_styles()
    
    # Initialize session manager
    session_manager = SessionManager()
    session_manager.initialize_session()
    
    # Render navigation
    render_navigation()
    
    # Main content based on authentication status
    if not st.session_state.logged_in:
        render_guest_content()
    else:
        render_user_dashboard_simple()
    
    # Always render pricing, testimonials, and footer
    render_pricing()
    render_testimonials()
    render_footer()
    
    # Demo information
    render_demo_info()

def render_guest_content():
    """Render content for non-authenticated users"""
    render_hero_section()
    
    # Get current theme for key generation
    theme_key = "dark" if st.session_state.get('dark_theme', False) else "light"
    
    # Authentication section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Get Started")
        
        # Use theme-based key to force component refresh
        auth_tab = st.selectbox(
            "Choose Action", 
            ["Login", "Register", "Guest Access"],
            key=f"auth_selectbox_{theme_key}"  # This forces refresh on theme change
        )
        
        if auth_tab == "Login":
            render_login_form()
        elif auth_tab == "Register":
            render_register_form()
        else:  # Guest Access
            render_guest_access()
    
    # Features and statistics (these are working fine, don't change)
    render_features()
    render_statistics()

def render_user_dashboard_simple():
    """Render simplified user dashboard"""
    from src.dashboard.user_dashboard import render_user_dashboard
    render_user_dashboard()

def render_guest_access():
    """Render guest access option"""
    st.subheader("👤 Continue as Guest")
    st.info("Limited features available for guest users")
    if st.button("🚀 Continue as Guest", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.user_name = "Guest"
        st.success("✅ Welcome, Guest!")
        st.rerun()

def render_demo_info():
    """Render demo information"""
    if st.session_state.get('show_demo_info', True):
        with st.expander("ℹ️ Demo Information"):
            st.info("""
            **Demo Credentials:**
            - Username: admin
            - Password: admin123

            **Features Demonstrated:**
            - Theme toggle (light/dark mode)
            - User authentication (login/register)
            - Interactive booking system
            - Responsive design
            - Professional UI components
            """)
            if st.button("Hide Demo Info"):
                st.session_state.show_demo_info = False
                st.rerun()

if __name__ == "__main__":
    main()
