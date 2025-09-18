"""
Booking Form Component
"""

import streamlit as st
from datetime import datetime
from src.utils.validators import validate_booking_form

def render_booking_form():
    """Render booking form"""
    with st.expander("📋 Complete Your Booking", expanded=True):
        with st.form("booking_form"):
            col_book1, col_book2 = st.columns(2)
            
            with col_book1:
                pickup_location = st.text_input("📍 Pickup Location", 
                                              placeholder="Enter pickup address")
                pickup_date = st.date_input("📅 Pickup Date", 
                                          min_value=datetime.now().date())
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
    
    validation_result = validate_booking_form(
        pickup_location, destination, str(pickup_date), str(pickup_time), vehicle_type, duration
    )
    
    if not validation_result["valid"]:
        st.warning(f"⚠️ {validation_result['message']}")
        return
    
    # TODO: Save booking to database
    # booking_id = save_booking_to_database(...)
    
    st.success("✅ Booking confirmed! Driver will contact you shortly.")
    st.balloons()

def save_booking_to_database(pickup_location: str, destination: str, pickup_date, 
                           pickup_time, vehicle_type: str, duration: str, special_requests: str):
    """Save booking to database (future implementation)"""
    # TODO: Implement database booking creation
    # from config.database import db_manager
    # from src.models.booking import Booking
    # return Booking.create(...)
    pass
