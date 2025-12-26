import streamlit as st

def render_hero_section():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2>Your Professional Chauffeur Service</h2>
            <p>Book experienced drivers for your vehicle anytime, anywhere</p>
        </div>
    """, unsafe_allow_html=True)
