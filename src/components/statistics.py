import streamlit as st

def render_statistics():
    st.markdown("### Our Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Happy Customers", "10,000+")
    
    with col2:
        st.metric("Professional Drivers", "500+")
    
    with col3:
        st.metric("Cities Covered", "50+")
    
    with col4:
        st.metric("Service", "24/7")

def render_stats_card(stat: dict):
    pass
