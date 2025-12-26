import streamlit as st

def render_testimonials():
    st.markdown("### What Our Customers Say")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### John D.")
        st.write("⭐⭐⭐⭐⭐")
        st.write("Excellent service! Professional drivers and easy booking.")
    
    with col2:
        st.markdown("#### Sarah M.")
        st.write("⭐⭐⭐⭐⭐")
        st.write("Very reliable. I use Chaalak for all my business trips.")
