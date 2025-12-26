import streamlit as st

def render_features():
    st.markdown("### Why Choose Chaalak?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🛡️ Professional Drivers")
        st.write("Licensed, insured, and background-checked chauffeurs")
    
    with col2:
        st.markdown("#### 🚗 Your Vehicle")
        st.write("Use your own car with our professional drivers")
    
    with col3:
        st.markdown("#### 📱 Easy Booking")
        st.write("Book instantly with real-time tracking")

def render_feature_card(feature: dict):
    pass
