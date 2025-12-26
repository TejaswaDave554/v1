import streamlit as st
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.custom_css import get_custom_css
from config.database import db

st.set_page_config(page_title="Chaalak - Admin", page_icon="🚗", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

def main():
    if not st.session_state.get('logged_in', False):
        st.error("Please login first")
        st.switch_page("pages/Login.py")
        return

    if st.session_state.get('user_role') != 'admin':
        st.error("Admin access only")
        st.switch_page("app.py")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Admin Dashboard")
    with col2:
        if st.button("Logout"):
            for key in ['logged_in', 'user_id', 'username', 'user_role', 'full_name']:
                st.session_state.pop(key, None)
            st.switch_page("app.py")

    st.divider()

    try:
        stats = db.get_booking_stats()
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Bookings", stats['total_bookings'] or 0)
        with col2:
            st.metric("Completed", stats['completed'] or 0)
        with col3:
            st.metric("Pending", stats['pending'] or 0)
        with col4:
            st.metric("Cancelled", stats['cancelled'] or 0)
        with col5:
            st.metric("Revenue", f"₹{stats['total_revenue'] or 0:.2f}")
    except:
        st.warning("Unable to load stats")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Users", "Drivers", "Bookings"])

    with tab1:
        st.subheader("All Users")
        try:
            users = db.get_all_users()
            if users:
                df = pd.DataFrame(users)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No users found")
        except Exception as e:
            st.error(f"Error loading users: {e}")

    with tab2:
        st.subheader("All Drivers")
        try:
            drivers = db.get_all_drivers_with_users()
            if drivers:
                df = pd.DataFrame(drivers)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No drivers found")
        except Exception as e:
            st.error(f"Error loading drivers: {e}")

    with tab3:
        st.subheader("All Bookings")
        try:
            bookings = db.get_all_bookings()
            if bookings:
                df = pd.DataFrame(bookings)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No bookings found")
        except Exception as e:
            st.error(f"Error loading bookings: {e}")

if __name__ == "__main__":
    main()
