import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from config.database import db

from src.auth.login import check_authentication, logout_user
from src.booking.booking_form import render_booking_form
from src.booking.booking_history import render_booking_history

def render_user_dashboard():

    is_auth, message = check_authentication()
    if not is_auth:
        st.error(message)
        st.switch_page("pages/🔐_Login.py")
        return

    try:

        user = db.get_user_by_id(st.session_state.user_id)
        if not user:
            st.error("User not found!")
            return

        render_dashboard_header(user)

        tab1, tab2, tab3, tab4 = st.tabs(["🚗 Book Ride", "📊 My Bookings", "📈 Analytics", "👤 Profile"])

        with tab1:
            render_booking_form()

        with tab2:
            render_user_bookings()

        with tab3:
            render_user_analytics()

        with tab4:
            render_user_profile(user)

    except Exception as e:
        st.error(f"❌ Dashboard error: {str(e)}")
        print(f"Dashboard error: {e}")

def render_dashboard_header(user):

    col1, col2 = st.columns([3, 1])

    with col1:
        name = user.get('full_name', user['username'])
        st.title(f"Welcome back, {name}! 🎉")
        st.markdown("Book rides, track your trips, and manage your profile")

    with col2:
        if st.button("🚪 Logout", type="secondary"):
            logout_user()
            st.success("Logged out successfully!")
            st.switch_page("app.py")

def render_user_bookings():

    try:
        bookings = db.get_bookings_by_customer(st.session_state.user_id)

        if not bookings:
            st.info("📭 No bookings yet! Book your first ride in the 'Book Ride' tab.")
            return

        render_booking_quick_stats(bookings)

        st.subheader("📋 Recent Bookings")
        recent_bookings = sorted(bookings,
                               key=lambda x: datetime.fromisoformat(str(x['created_at']).replace('Z', '')),
                               reverse=True)[:5]

        for booking in recent_bookings:
            render_booking_summary_card(booking)

        if len(bookings) > 5:
            if st.button("📊 View All Bookings"):
                st.switch_page("pages/📊_Booking_History.py")

    except Exception as e:
        st.error(f"❌ Error loading bookings: {str(e)}")

def render_booking_quick_stats(bookings):

    total_bookings = len(bookings)
    completed = len([b for b in bookings if b['status'] == 'completed'])
    pending = len([b for b in bookings if b['status'] == 'pending'])
    total_spent = sum(float(b.get('actual_fare', b.get('estimated_fare', 0)))
                     for b in bookings if b['status'] == 'completed')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Total Bookings", total_bookings)

    with col2:
        st.metric("✅ Completed", completed)

    with col3:
        st.metric("⏳ Pending", pending)

    with col4:
        st.metric("💰 Total Spent", f"₹{total_spent:,.0f}")

    st.divider()

def render_booking_summary_card(booking):

    status_colors = {
        'pending': '🟡',
        'confirmed': '🔵',
        'in_progress': '🟢',
        'completed': '✅',
        'cancelled': '❌'
    }

    status_icon = status_colors.get(booking['status'], '⚪')

    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.markdown(f)

        with col2:
            st.markdown(f)

        with col3:
            if booking['status'] == 'pending':
                if st.button("❌", key=f"cancel_{booking['id']}", help="Cancel booking"):
                    if cancel_booking(booking['id']):
                        st.success("Cancelled!")
                        st.rerun()

        st.divider()

def render_user_analytics():

    st.subheader("📈 Your Travel Analytics")

    try:
        bookings = db.get_bookings_by_customer(st.session_state.user_id)

        if not bookings:
            st.info("📊 No data available yet. Complete some trips to see analytics!")
            return

        render_monthly_spending_chart(bookings)

        render_service_breakdown(bookings)

        render_travel_patterns(bookings)

    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")

def render_monthly_spending_chart(bookings):

    completed_bookings = [b for b in bookings if b['status'] == 'completed']

    if not completed_bookings:
        st.info("No completed trips to analyze yet.")
        return

    monthly_data = {}
    for booking in completed_bookings:
        try:
            month = str(booking['created_at'])[:7]
            fare = float(booking.get('actual_fare', booking.get('estimated_fare', 0)))
            monthly_data[month] = monthly_data.get(month, 0) + fare
        except (ValueError, TypeError):
            continue

    if monthly_data:
        df = pd.DataFrame(list(monthly_data.items()), columns=['Month', 'Amount'])
        df = df.sort_values('Month')

        st.markdown("
        st.bar_chart(df.set_index('Month'))

def render_service_breakdown(bookings):

    service_counts = {}
    for booking in bookings:
        service = booking['service_type'].replace('_', ' ').title()
        service_counts[service] = service_counts.get(service, 0) + 1

    if service_counts:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("
            df = pd.DataFrame(list(service_counts.items()), columns=['Service', 'Count'])
            st.bar_chart(df.set_index('Service'))

        with col2:
            st.markdown("
            for service, count in service_counts.items():
                percentage = (count / len(bookings)) * 100
                st.write(f"**{service}:** {count} trips ({percentage:.1f}%)")

def render_travel_patterns(bookings):

    st.markdown("

    pickup_counts = {}
    for booking in bookings:
        pickup = booking['pickup_location']
        pickup_counts[pickup] = pickup_counts.get(pickup, 0) + 1

    dropoff_counts = {}
    for booking in bookings:
        dropoff = booking['dropoff_location']
        dropoff_counts[dropoff] = dropoff_counts.get(dropoff, 0) + 1

    col1, col2 = st.columns(2)

    with col1:
        if pickup_counts:
            st.write("**Most Used Pickup Locations:**")
            sorted_pickups = sorted(pickup_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for location, count in sorted_pickups:
                st.write(f"• {location}: {count} times")

    with col2:
        if dropoff_counts:
            st.write("**Most Used Destinations:**")
            sorted_dropoffs = sorted(dropoff_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for location, count in sorted_dropoffs:
                st.write(f"• {location}: {count} times")

def render_user_profile(user):

    st.subheader("👤 Your Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("
        st.write(f"**Full Name:** {user.get('full_name', 'Not set')}")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Phone:** {user.get('phone', 'Not set')}")

    with col2:
        st.markdown("
        st.write(f"**Account Type:** {user['role'].title()}")
        st.write(f"**Member Since:** {str(user['created_at'])[:10]}")
        st.write(f"**Status:** {'Active' if user.get('is_active', True) else 'Inactive'}")
        st.write(f"**User ID:** {user['id'][:8]}...")

    st.divider()

    st.markdown("
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.info("Profile editing will be available in the next update!")

    with col2:
        if st.button("🔒 Change Password", use_container_width=True):
            st.info("Password change will be available in the next update!")

    with col3:
        if st.button("📧 Update Email", use_container_width=True):
            st.info("Email update will be available in the next update!")

def cancel_booking(booking_id):

    try:
        result = db.update_booking_status(booking_id, 'cancelled')
        return result is not None
    except Exception as e:
        print(f"Cancel booking error: {e}")
        return False
