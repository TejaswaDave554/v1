"""
User Dashboard Component
"""

import streamlit as st
from src.auth.session_manager import SessionManager
from src.booking.booking_history import render_booking_history
from src.dashboard.quick_actions import render_quick_actions

def render_user_dashboard():
    """Render main user dashboard"""
    username = SessionManager.get_current_user()
    st.markdown(f"## Welcome back, {username}! 👋")
    
    # User actions
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🚗 Hire a Chauffeur", use_container_width=True, type="primary"):
            st.success("🎉 Chauffeur booking system activated!")
            render_booking_form()
    
    with col2:
        if st.button("📊 My Bookings", use_container_width=True):
            render_booking_history()
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            SessionManager.logout_user()
            st.success("👋 Logged out successfully!")
            st.rerun()
    
    # Quick actions
    render_quick_actions()
    
    # Floating action button for quick booking
    render_floating_action_button()


def render_booking_form():
    """Render booking form inline"""
    with st.expander("📋 Complete Your Booking", expanded=True):
        with st.form("booking_form"):
            col_book1, col_book2 = st.columns(2)
            
            with col_book1:
                pickup_location = st.text_input("📍 Pickup Location", 
                                              placeholder="Enter pickup address")
                pickup_date = st.date_input("📅 Pickup Date", 
                                          min_value=st.session_state.get('today', None))
                vehicle_type = st.selectbox("🚗 Your Vehicle Type", 
                                          ["Sedan", "SUV", "Hatchback", "Luxury Car", "Other"])
            
            with col_book2:
                destination = st.text_input("🎯 Destination", 
                                          placeholder="Enter destination address")
                pickup_time = st.time_input("⏰ Pickup Time")
                duration = st.selectbox("⏱️ Expected Duration", 
                                       ["1-2 hours", "2-4 hours", "4-8 hours", "Full Day"])
            
            special_requests = st.text_area("💬 Special Requests", 
                                           placeholder="Any special requirements or preferences...")
            
            booking_submit = st.form_submit_button("🔥 Book Now", use_container_width=True)
            
            if booking_submit:
                handle_booking_submission(pickup_location, destination, pickup_date, 
                                        pickup_time, vehicle_type, duration, special_requests)


def handle_booking_submission(pickup_location: str, destination: str, pickup_date, 
                            pickup_time, vehicle_type: str, duration: str, special_requests: str):
    """Handle booking form submission"""
    
    # Basic validation
    if not pickup_location.strip():
        st.warning("⚠️ Please enter pickup location")
        return
    
    if not destination.strip():
        st.warning("⚠️ Please enter destination")
        return
    
    # TODO: Save booking to database
    # booking_id = save_booking_to_database(...)
    
    st.success("✅ Booking confirmed! Driver will contact you shortly.")
    st.balloons()


def render_floating_action_button():
    """Render floating action button"""
    st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 999;">
        <button class="cta-button" style="border-radius: 50%; width: 60px; height: 60px; font-size: 24px;">
            🚗
        </button>
    </div>
    """, unsafe_allow_html=True)
