import streamlit as st
import sys
import os
import pandas as pd
from datetime import date, time, datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.custom_css import get_custom_css
from src.utils.session_manager import is_logged_in, check_session_timeout
from src.utils.fare_calculator import calculate_fare, estimate_distance
from src.utils.error_logger import log_error, log_info

st.set_page_config(page_title="Chaalak - Dashboard", page_icon="🚗", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

def main():
    if check_session_timeout():
        st.error("Session expired. Please login again")
        st.switch_page("pages/Login.py")
        return

    if not is_logged_in():
        st.error("Please login first")
        st.switch_page("pages/Login.py")
        return

    username = st.session_state.get('full_name') or st.session_state.get('username', 'User')
    user_id = st.session_state.get('user_id', 'N/A')

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"Welcome, {username}")
        st.caption(f"User ID: {str(user_id)[:8]}...")
    with col2:
        if st.button("Home", use_container_width=True):
            st.switch_page("app.py")
    with col3:
        if st.button("Logout", use_container_width=True):
            log_info(f"User logged out", user_id)
            for key in ['logged_in', 'user_id', 'username', 'user_role', 'full_name', 'last_activity']:
                st.session_state.pop(key, None)
            st.switch_page("app.py")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Book Ride", "My Bookings", "Emergency"])

    with tab1:
        render_overview(user_id)

    with tab2:
        render_booking_form(user_id)

    with tab3:
        render_my_bookings(user_id)

    with tab4:
        render_emergency()

def render_overview(user_id):
    st.header("Dashboard Overview")
    try:
        from config.database import db
        bookings = db.get_bookings_by_customer(user_id)

        total = len(bookings)
        completed = sum(1 for b in bookings if b['status'] == 'completed')
        pending = sum(1 for b in bookings if b['status'] in ['pending', 'confirmed'])
        total_spent = sum(b['estimated_fare'] for b in bookings if b['status'] == 'completed')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Bookings", total)
        with col2:
            st.metric("Completed", completed)
        with col3:
            st.metric("Pending", pending)
        with col4:
            st.metric("Total Spent", f"₹{total_spent:.2f}")

        if bookings:
            st.subheader("Recent Activity")
            recent = bookings[:5]
            df = pd.DataFrame([{
                "Route": f"{b['pickup_location']} → {b['dropoff_location']}",
                "Status": b['status'].title(),
                "Date": str(b['pickup_datetime']),
                "Fare": f"₹{b['estimated_fare']}"
            } for b in recent])
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        log_error("Dashboard", str(e), user_id)
        st.error("Unable to load dashboard data")

def render_booking_form(user_id):
    st.header("Book a New Ride")

    col1, col2 = st.columns(2)

    with col1:
        pickup = st.text_input("Pickup Location", placeholder="e.g., Mumbai Airport")
        dropoff = st.text_input("Dropoff Location", placeholder="e.g., Bandra West")
        vehicle = st.selectbox("Vehicle Type", ["Sedan", "SUV", "Hatchback", "Luxury", "Van"])

    with col2:
        booking_type = st.radio("Booking Type", ["Immediate", "Schedule"])

        if booking_type == "Schedule":
            pickup_date = st.date_input("Date", value=date.today(), min_value=date.today())
            pickup_time = st.time_input("Time", value=time(14, 0))
        else:
            pickup_date = date.today()
            pickup_time = datetime.now().time()

        service = st.selectbox("Service Type",
            ["Airport Transfer", "Corporate", "Wedding", "Hourly", "Outstation"])

    instructions = st.text_area("Special Instructions", placeholder="Any special requirements?")

    if pickup and dropoff:
        distance = estimate_distance(pickup, dropoff)
        fare_details = calculate_fare(distance, vehicle.lower(), service.lower().replace(' ', '_'))

        st.info(f"**Estimated Fare:** ₹{fare_details['total_fare']}")
        with st.expander("Fare Breakdown"):
            st.write(fare_details['breakdown'])

    if st.button("Book Now", type="primary", use_container_width=True):
        if pickup and dropoff:
            try:
                from config.database import db
                from src.utils.notifications import notify_booking_confirmed

                distance = estimate_distance(pickup, dropoff)
                fare_details = calculate_fare(distance, vehicle.lower(), service.lower().replace(' ', '_'))

                booking_data = {
                    'customer_id': user_id,
                    'pickup_location': pickup,
                    'dropoff_location': dropoff,
                    'pickup_datetime': datetime.combine(pickup_date, pickup_time),
                    'service_type': service.lower().replace(' ', '_'),
                    'vehicle_type': vehicle.lower(),
                    'estimated_fare': fare_details['total_fare'],
                    'special_instructions': instructions
                }
                booking_id = db.create_booking(booking_data)

                log_info(f"Booking created: {booking_id}", user_id)

                try:
                    user = db.get_user_by_id(user_id)
                    if user and user.get('email'):
                        booking_data['id'] = booking_id
                        notify_booking_confirmed(user['email'], booking_data)
                except:
                    pass

                st.success(f"Booking confirmed! ID: {booking_id[:8]}...")
                st.balloons()
                st.rerun()
            except Exception as e:
                log_error("Booking", str(e), user_id)
                st.error(f"Booking failed: {e}")
        else:
            st.error("Please fill in both pickup and dropoff locations")

def render_my_bookings(user_id):
    st.header("My Bookings")

    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Confirmed", "Completed", "Cancelled"])
    with col2:
        date_from = st.date_input("From Date", value=date.today() - timedelta(days=30))
    with col3:
        date_to = st.date_input("To Date", value=date.today())

    try:
        from config.database import db
        bookings = db.get_bookings_by_customer(user_id)

        if status_filter != "All":
            bookings = [b for b in bookings if b['status'] == status_filter.lower()]

        bookings = [b for b in bookings if date_from <= b['pickup_datetime'].date() <= date_to]

        if bookings:
            for booking in bookings:
                with st.expander(f"{booking['pickup_location']} → {booking['dropoff_location']} - {booking['status'].title()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Status:** {booking['status'].title()}")
                        st.write(f"**Date:** {booking['pickup_datetime']}")
                        st.write(f"**Service:** {booking['service_type'].replace('_', ' ').title()}")
                    with col2:
                        st.write(f"**Fare:** ₹{booking['estimated_fare']}")
                        st.write(f"**Vehicle:** {booking['vehicle_type'].title()}")
                        if booking.get('rating'):
                            st.write(f"**Rating:** {'⭐' * booking['rating']}")

                    if booking.get('special_instructions'):
                        st.write(f"**Instructions:** {booking['special_instructions']}")

                    col1, col2, col3 = st.columns(3)

                    if booking['status'] == 'confirmed':
                        with col1:
                            if st.button("End Ride", key=f"end_{booking['id']}", type="primary"):
                                db.update_booking_status(booking['id'], 'completed')
                                log_info(f"Ride completed: {booking['id']}", user_id)
                                st.success("Ride completed")
                                st.rerun()

                    if booking['status'] in ['pending', 'confirmed']:
                        with col2:
                            if st.button("Cancel", key=f"cancel_{booking['id']}"):
                                db.cancel_booking(booking['id'])
                                log_info(f"Booking cancelled: {booking['id']}", user_id)
                                st.warning("Booking cancelled")
                                st.rerun()

                    if booking['status'] == 'completed' and not booking.get('rating'):
                        with col3:
                            if st.button("Rate", key=f"rate_{booking['id']}"):
                                st.session_state[f'rating_modal_{booking["id"]}'] = True
                                st.rerun()

                    if st.session_state.get(f'rating_modal_{booking["id"]}', False):
                        st.write("**Rate your experience:**")
                        rating = st.slider("Rating", 1, 5, 5, key=f"rating_slider_{booking['id']}")
                        feedback = st.text_area("Feedback (optional)", key=f"feedback_{booking['id']}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Submit Rating", key=f"submit_rating_{booking['id']}"):
                                db.update_booking_rating(booking['id'], rating, feedback)
                                log_info(f"Rating submitted: {booking['id']}", user_id)
                                st.session_state[f'rating_modal_{booking["id"]}'] = False
                                st.success("Thank you for your feedback!")
                                st.rerun()
                        with col2:
                            if st.button("Cancel", key=f"cancel_rating_{booking['id']}"):
                                st.session_state[f'rating_modal_{booking["id"]}'] = False
                                st.rerun()
        else:
            st.info("No bookings found")
    except Exception as e:
        log_error("My Bookings", str(e), user_id)
        st.error("Unable to load bookings")

def render_emergency():
    st.header("Emergency SOS")
    st.warning("⚠️ Use this only in case of emergency")

    emergency_contact = st.text_input("Emergency Contact Number", placeholder="+1234567890")

    if st.button("Send SOS Alert", type="primary"):
        if emergency_contact:
            st.success(f"SOS alert sent to {emergency_contact}")
            st.info("Your current location has been shared with your emergency contact")
            log_info(f"SOS triggered - Contact: {emergency_contact}", st.session_state.get('user_id'))
        else:
            st.error("Please enter emergency contact number")

    st.divider()
    st.subheader("Emergency Contacts")
    st.write("**Police:** 100")
    st.write("**Ambulance:** 102")
    st.write("**Women Helpline:** 1091")

if __name__ == "__main__":
    main()
