import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config.database import db

def render_booking_history():

    st.subheader("📊 Your Booking History")

    if not st.session_state.get('logged_in', False):
        st.warning("Please login to view your booking history")
        return

    try:

        bookings = db.get_bookings_by_customer(st.session_state.user_id)

        if not bookings:
            st.info("📭 No bookings yet! Book your first ride to see it here.")
            if st.button("🚗 Book a Ride"):
                st.switch_page("pages/👤_User_Dashboard.py")
            return

        render_booking_stats(bookings)

        render_booking_filters(bookings)

    except Exception as e:
        st.error(f"❌ Error loading booking history: {str(e)}")
        print(f"Booking history error: {e}")

def render_booking_stats(bookings):

    total_bookings = len(bookings)
    completed_bookings = [b for b in bookings if b['status'] == 'completed']
    pending_bookings = [b for b in bookings if b['status'] == 'pending']
    cancelled_bookings = [b for b in bookings if b['status'] == 'cancelled']

    total_spent = sum(float(b.get('actual_fare', b.get('estimated_fare', 0)))
                     for b in completed_bookings)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Total Bookings", total_bookings)

    with col2:
        st.metric("✅ Completed", len(completed_bookings))

    with col3:
        st.metric("⏳ Pending", len(pending_bookings))

    with col4:
        st.metric("💰 Total Spent", f"₹{total_spent:,.0f}")

    st.divider()

def render_booking_filters(bookings):

    col1, col2, col3 = st.columns(3)

    with col1:
        status_options = ['All'] + list(set(b['status'] for b in bookings))
        selected_status = st.selectbox("Filter by Status", status_options)

    with col2:
        service_options = ['All'] + list(set(b['service_type'] for b in bookings))
        selected_service = st.selectbox("Filter by Service", service_options)

    with col3:

        date_filter = st.selectbox("Date Range",
                                 ["All Time", "Last 7 Days", "Last 30 Days", "Last 3 Months"])

    filtered_bookings = apply_booking_filters(bookings, selected_status, selected_service, date_filter)

    if filtered_bookings:
        render_booking_list(filtered_bookings)
    else:
        st.info("No bookings match the selected filters.")

def apply_booking_filters(bookings, status_filter, service_filter, date_filter):

    filtered = bookings.copy()

    if status_filter != 'All':
        filtered = [b for b in filtered if b['status'] == status_filter]

    if service_filter != 'All':
        filtered = [b for b in filtered if b['service_type'] == service_filter]

    if date_filter != 'All Time':
        now = datetime.now()
        if date_filter == 'Last 7 Days':
            cutoff = now - timedelta(days=7)
        elif date_filter == 'Last 30 Days':
            cutoff = now - timedelta(days=30)
        elif date_filter == 'Last 3 Months':
            cutoff = now - timedelta(days=90)
        else:
            cutoff = None

        if cutoff:
            filtered = [b for b in filtered
                       if datetime.fromisoformat(str(b['created_at']).replace('Z', '')) > cutoff]

    return filtered

def render_booking_list(bookings):

    sorted_bookings = sorted(bookings,
                           key=lambda x: datetime.fromisoformat(str(x['created_at']).replace('Z', '')),
                           reverse=True)

    for booking in sorted_bookings:
        render_booking_card(booking)

def render_booking_card(booking):

    status_colors = {
        'pending': '🟡',
        'confirmed': '🔵',
        'in_progress': '🟢',
        'completed': '✅',
        'cancelled': '❌'
    }

    status_icon = status_colors.get(booking['status'], '⚪')

    with st.expander(f"{status_icon} {booking['pickup_location']} → {booking['dropoff_location']} ({booking['status'].title()})", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f)

        with col2:
            actual_fare = booking.get('actual_fare') or booking.get('estimated_fare', 0)
            driver_name = booking.get('driver_name', 'Not assigned')

            st.markdown(f)

        if booking.get('special_instructions'):
            st.markdown(f"**📝 Instructions:** {booking['special_instructions']}")

        render_booking_actions(booking)

def render_booking_actions(booking):

    col1, col2, col3 = st.columns(3)

    with col1:
        if booking['status'] == 'pending':
            if st.button("❌ Cancel Booking", key=f"cancel_{booking['id']}"):
                if cancel_booking(booking['id']):
                    st.success("Booking cancelled!")
                    st.rerun()
                else:
                    st.error("Failed to cancel booking")

    with col2:
        if booking['status'] == 'completed' and not booking.get('rating'):
            if st.button("⭐ Rate Trip", key=f"rate_{booking['id']}"):
                render_rating_form(booking['id'])

    with col3:
        if st.button("📋 View Details", key=f"details_{booking['id']}"):
            render_booking_details(booking)

def cancel_booking(booking_id):

    try:
        result = db.update_booking_status(booking_id, 'cancelled')
        return result is not None
    except Exception as e:
        print(f"Cancel booking error: {e}")
        return False

def render_rating_form(booking_id):

    with st.form(f"rating_form_{booking_id}"):
        st.subheader("⭐ Rate Your Trip")

        rating = st.select_slider("Rating", options=[1, 2, 3, 4, 5], value=5,
                                format_func=lambda x: "⭐" * x)
        feedback = st.text_area("Feedback (Optional)", placeholder="How was your experience?")

        if st.form_submit_button("Submit Rating"):

            st.success("Thank you for your feedback!")

def render_booking_details(booking):

    st.subheader("📋 Booking Details")

    details_df = pd.DataFrame([
        ["Booking ID", booking['id']],
        ["Status", booking['status'].title()],
        ["Pickup Location", booking['pickup_location']],
        ["Dropoff Location", booking['dropoff_location']],
        ["Pickup DateTime", booking['pickup_datetime']],
        ["Service Type", booking['service_type'].replace('_', ' ').title()],
        ["Vehicle Type", booking['vehicle_type'].title()],
        ["Estimated Fare", f"₹{booking.get('estimated_fare', 0)}"],
        ["Actual Fare", f"₹{booking.get('actual_fare', 'N/A')}"],
        ["Driver", booking.get('driver_name', 'Not assigned')],
        ["Created At", str(booking['created_at'])],
        ["Special Instructions", booking.get('special_instructions', 'None')]
    ], columns=["Field", "Value"])

    st.table(details_df)
