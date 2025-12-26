import streamlit as st

def render_quick_actions():

    st.markdown("
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🚨 Emergency Ride", use_container_width=True):
            st.error("🚨 Emergency booking activated! Nearest driver dispatched.")

    with col2:
        if st.button("⭐ Rate Driver", use_container_width=True):
            render_driver_rating()

    with col3:
        if st.button("💳 Payment Methods", use_container_width=True):
            st.info("💳 Manage your payment methods and billing")

    with col4:
        if st.button("🎁 Referral Program", use_container_width=True):
            st.success("🎁 Invite friends and earn rewards!")

def render_driver_rating():

    rating = st.select_slider("Rate your last ride",
                            options=[1, 2, 3, 4, 5], value=5)
    st.success(f"Thanks for rating! {rating} stars given.")
