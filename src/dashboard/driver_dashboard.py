from unicodedata import name
import streamlit as st
import pandas as pd
from datetime import datetime, date
from config.database import db
from src.auth.auth_utils import check_authentication, logout_user

def render_driver_dashboard():

    is_auth, message = check_authentication('driver')
    if not is_auth:
        st.error(message)
        st.switch_page("pages/🔐_Login.py")
        return

    user = db.get_user_by_id(st.session_state.user_id)
    driver = db.get_driver_by_user_id(st.session_state.user_id)

    if not user or not driver:
        st.error("Driver profile not found!")
        return

    render_driver_header(user, driver)

    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Overview", "🚨 Requests", "📊 History", "💰 Earnings"])

    with tab1:
        render_driver_overview(driver)

    with tab2:
        render_trip_requests(driver)

    with tab3:
        render_trip_history(driver)

    with tab4:
        render_earnings_summary(driver)

def render_driver_header(user, driver):

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.title("🚗 Driver Dashboard")
        name = user.get("full_name") or user.get("username") or "Driver"
        st.markdown(f"Welcome back, **{name}**!")

    with col2:

        is_available = st.toggle("Available for rides", value=driver['is_available'])
        if is_available != driver['is_available']:
            st.success("✅ Availability updated!")

    with col3:
        if st.button("🚪 Logout"):
            logout_user()
            st.switch_page("pages/🔐_Login.py")

def render_driver_overview(driver):

    bookings = db.get_bookings_by_driver(driver['id'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("⭐ Rating", f"{driver['rating']:.1f}", help="Your average rating")

    with col2:
        completed_trips = len([b for b in bookings if b['status'] == 'completed'])
        st.metric("🎯 Total Trips", completed_trips)

    with col3:
        pending_trips = len([b for b in bookings if b['status'] == 'pending'])
        st.metric("⏳ Pending Requests", pending_trips)

    with col4:
        today_trips = len([b for b in bookings if str(b['pickup_datetime']).startswith(date.today().isoformat())])
        st.metric("📅 Today's Trips", today_trips)

    st.divider()

    render_active_trips(driver)

def render_active_trips(driver):

    st.subheader("🎯 Your Active Trips")

    active_bookings = [b for b in db.get_bookings_by_driver(driver['id'])
                      if b['status'] in ['confirmed', 'in_progress']]

    if not active_bookings:
        st.info("📭 No active trips")
        return

    for booking in active_bookings:
        with st.expander(f"Trip to {booking['dropoff_location']} - {booking['status'].title()}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f)

            with col2:
                st.markdown(f)

            col3, col4, col5 = st.columns(3)

            with col3:
                if booking['status'] == 'confirmed' and st.button("🚀 Start Trip", key=f"start_{booking['id']}"):
                    db.update_booking_status(booking['id'], 'in_progress')
                    st.success("Trip started!")
                    st.rerun()

            with col4:
                if booking['status'] == 'in_progress' and st.button("✅ Complete", key=f"complete_{booking['id']}"):
                    db.update_booking_status(booking['id'], 'completed')
                    st.success("Trip completed!")
                    st.rerun()

            with col5:
                if st.button("❌ Cancel", key=f"cancel_{booking['id']}"):
                    db.update_booking_status(booking['id'], 'cancelled')
                    st.warning("Trip cancelled!")
                    st.rerun()

def render_trip_requests(driver):

    st.subheader("🚨 New Trip Requests")

    all_bookings = db._read_table('bookings')
    pending_bookings = [b for b in all_bookings if b['status'] == 'pending' and not b.get('driver_id')]

    if not pending_bookings:
        st.info("🎉 No pending requests at the moment!")
        return

    for booking in pending_bookings[:3]:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown(f)

            with col2:
                st.markdown(f)

            with col3:
                if st.button("✅ Accept", key=f"accept_{booking['id']}"):
                    db.update_booking_status(booking['id'], 'confirmed', driver['id'])
                    st.success("Trip accepted!")
                    st.rerun()

                if st.button("❌ Decline", key=f"decline_{booking['id']}"):
                    st.info("Request declined")

        st.divider()

def render_trip_history(driver):

    st.subheader("📊 Trip History")

    all_bookings = db.get_bookings_by_driver(driver['id'])

    if not all_bookings:
        st.info("No trip history yet!")
        return

    df_data = []
    for booking in all_bookings:
        df_data.append({
            'Date': booking['pickup_datetime'][:10],
            'Pickup': booking['pickup_location'],
            'Dropoff': booking['dropoff_location'],
            'Fare': booking['estimated_fare'],
            'Status': booking['status'].title()
        })

    df = pd.DataFrame(df_data)

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status",
                                   options=['All'] + list(df['Status'].unique()))

    with col2:
        date_range = st.date_input("Date Range", value=[])

    filtered_df = df.copy()
    if status_filter != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]

    st.dataframe(filtered_df, use_container_width=True)

def render_earnings_summary(driver):

    st.subheader("💰 Earnings Summary")

    completed_bookings = [b for b in db.get_bookings_by_driver(driver['id'])
                         if b['status'] == 'completed']

    if not completed_bookings:
        st.info("Complete some trips to see earnings!")
        return

    total_earnings = sum(b['estimated_fare'] for b in completed_bookings)
    avg_fare = total_earnings / len(completed_bookings) if completed_bookings else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💵 Total Earnings", f"₹{total_earnings:,.2f}")

    with col2:
        st.metric("📊 Average Fare", f"₹{avg_fare:.2f}")

    with col3:
        st.metric("🎯 Completed Trips", len(completed_bookings))
