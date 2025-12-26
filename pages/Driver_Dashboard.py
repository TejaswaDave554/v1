import streamlit as st
import sys
import os
import pandas as pd
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.custom_css import get_custom_css
from src.utils.session_manager import is_logged_in, check_session_timeout
from src.utils.error_logger import log_error, log_info

st.set_page_config(page_title="Chaalak - Driver Dashboard", page_icon="🚗", layout="wide")
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

    if st.session_state.get('user_role') != 'driver':
        st.error("Driver access only")
        st.switch_page("pages/User_Dashboard.py")
        return

    username = st.session_state.get('full_name') or st.session_state.get('username', 'Driver')
    user_id = st.session_state.get('user_id')

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Driver Dashboard")
        st.markdown(f"**Welcome, {username}**")
    with col2:
        if st.button("Logout"):
            log_info(f"Driver logged out", user_id)
            for key in ['logged_in', 'user_id', 'username', 'user_role', 'full_name', 'last_activity']:
                st.session_state.pop(key, None)
            st.switch_page("app.py")

    st.divider()

    try:
        from config.database import db
        driver_info = db.get_driver_by_user_id(user_id)

        if not driver_info:
            st.error("Driver profile not found")
            return

        driver_id = driver_info['id']

        render_stats(driver_id)

        st.divider()

        tab1, tab2, tab3 = st.tabs(["Available Rides", "My Trips", "Earnings"])

        with tab1:
            render_available_rides(driver_id, user_id)

        with tab2:
            render_my_trips(driver_id, user_id)

        with tab3:
            render_earnings(driver_id)

    except Exception as e:
        log_error("Driver Dashboard", str(e), user_id)
        st.error(f"Error loading dashboard: {e}")

def render_stats(driver_id):
    try:
        from config.database import db
        my_bookings = db.get_bookings_by_driver(driver_id)
        rating_data = db.get_driver_average_rating(driver_id)

        total_trips = len(my_bookings)
        today_trips = sum(1 for b in my_bookings if b['pickup_datetime'].date() == date.today())
        total_earnings = sum(b['estimated_fare'] for b in my_bookings if b['status'] == 'completed')
        avg_rating = rating_data.get('avg_rating', 0) or 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rating", f"{avg_rating:.1f} ⭐")
        with col2:
            st.metric("Total Trips", total_trips)
        with col3:
            st.metric("Today's Trips", today_trips)
        with col4:
            st.metric("Total Earnings", f"₹{total_earnings:.2f}")
    except Exception as e:
        st.warning("Unable to load stats")

def render_available_rides(driver_id, user_id):
    st.subheader("Available Rides")

    try:
        from config.database import db
        pending_bookings = db.get_pending_unassigned_bookings()

        if pending_bookings:
            for booking in pending_bookings:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])

                    with col1:
                        st.write(f"**{booking['pickup_location']} → {booking['dropoff_location']}**")
                        st.caption(f"{booking['pickup_datetime']} | {booking['vehicle_type'].title()} | ₹{booking['estimated_fare']}")
                        if booking.get('special_instructions'):
                            st.caption(f"Note: {booking['special_instructions']}")

                    with col2:
                        if st.button("Accept", key=f"accept_{booking['id']}", type="primary"):
                            db.update_booking_status(booking['id'], 'confirmed', driver_id)
                            log_info(f"Ride accepted: {booking['id']}", user_id)
                            st.success("Ride accepted")
                            st.rerun()

                    with col3:
                        if st.button("Skip", key=f"reject_{booking['id']}"):
                            db.delete_booking(booking['id'])
                            log_info(f"Ride deleted: {booking['id']}", user_id)
                            st.success("Ride deleted")
                            st.rerun()

                    st.divider()
        else:
            st.info("No pending ride requests")
    except Exception as e:
        log_error("Available Rides", str(e), user_id)
        st.error(f"Error loading rides: {e}")

def render_my_trips(driver_id, user_id):
    st.subheader("My Trips")

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Confirmed", "Completed", "Cancelled"])
    with col2:
        date_filter = st.selectbox("Date Range", ["All Time", "Today", "This Week", "This Month"])

    try:
        from config.database import db
        my_bookings = db.get_bookings_by_driver(driver_id)

        if status_filter != "All":
            my_bookings = [b for b in my_bookings if b['status'] == status_filter.lower()]

        if date_filter == "Today":
            my_bookings = [b for b in my_bookings if b['pickup_datetime'].date() == date.today()]
        elif date_filter == "This Week":
            week_ago = date.today() - timedelta(days=7)
            my_bookings = [b for b in my_bookings if b['pickup_datetime'].date() >= week_ago]
        elif date_filter == "This Month":
            month_ago = date.today() - timedelta(days=30)
            my_bookings = [b for b in my_bookings if b['pickup_datetime'].date() >= month_ago]

        if my_bookings:
            for booking in my_bookings:
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

                    if booking.get('feedback'):
                        st.info(f"**Customer Feedback:** {booking['feedback']}")

                    if booking['status'] == 'confirmed':
                        if st.button("End Ride", key=f"end_{booking['id']}", type="primary"):
                            db.update_booking_status(booking['id'], 'completed')
                            log_info(f"Ride completed: {booking['id']}", user_id)
                            st.success("Ride completed")
                            st.rerun()
        else:
            st.info("No trips found")
    except Exception as e:
        log_error("My Trips", str(e), user_id)
        st.error("Unable to load trips")

def render_earnings(driver_id):
    st.subheader("Earnings Dashboard")

    try:
        from config.database import db
        my_bookings = db.get_bookings_by_driver(driver_id)
        completed = [b for b in my_bookings if b['status'] == 'completed']

        today_earnings = sum(b['estimated_fare'] for b in completed if b['pickup_datetime'].date() == date.today())
        week_earnings = sum(b['estimated_fare'] for b in completed if b['pickup_datetime'].date() >= date.today() - timedelta(days=7))
        month_earnings = sum(b['estimated_fare'] for b in completed if b['pickup_datetime'].date() >= date.today() - timedelta(days=30))
        total_earnings = sum(b['estimated_fare'] for b in completed)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Today", f"₹{today_earnings:.2f}")
        with col2:
            st.metric("This Week", f"₹{week_earnings:.2f}")
        with col3:
            st.metric("This Month", f"₹{month_earnings:.2f}")
        with col4:
            st.metric("Total", f"₹{total_earnings:.2f}")

        st.divider()

        if completed:
            st.subheader("Recent Earnings")
            df = pd.DataFrame([{
                "Date": str(b['pickup_datetime'].date()),
                "Route": f"{b['pickup_location']} → {b['dropoff_location']}",
                "Fare": f"₹{b['estimated_fare']}",
                "Rating": '⭐' * b['rating'] if b.get('rating') else 'Not rated'
            } for b in completed[:20]])
            st.dataframe(df, use_container_width=True)

            if st.button("Export Earnings Report"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"earnings_{date.today()}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No completed trips yet")

    except Exception as e:
        log_error("Earnings", str(e), st.session_state.get('user_id'))
        st.error("Unable to load earnings")

if __name__ == "__main__":
    main()
