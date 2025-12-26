import streamlit as st

def render_pricing():
    st.markdown("### Pricing Plans")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Standard")
        st.write("₹25/hour")
        st.write("Perfect for daily commutes")
    
    with col2:
        st.markdown("#### Premium")
        st.write("₹40/hour")
        st.write("Experienced drivers")
    
    with col3:
        st.markdown("#### VIP")
        st.write("₹65/hour")
        st.write("Luxury service")
