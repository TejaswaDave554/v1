"""
Hero Section Component
"""

import streamlit as st

def render_hero_section():
    """Render hero section"""
    st.markdown("""
    <div class="hero-section">
        <h1>🚗 Professional Chauffeur Services</h1>
        <h3>Your Car, Our Expert Drivers</h3>
        <p style="font-size: 1.2rem; margin: 2rem 0;">
            Experience luxury transportation with your own vehicle. 
            Our professional chauffeurs provide safe, reliable, and comfortable rides.
        </p>
    </div>
    """, unsafe_allow_html=True)
