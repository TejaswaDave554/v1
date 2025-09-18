"""
Features Section Component
"""

import streamlit as st

def render_features():
    """Render features section"""
    st.markdown("## ✨ Why Choose Chaalak?")
    
    col1, col2, col3 = st.columns(3)
    
    features_data = [
        {
            "icon": "🛡️",
            "title": "Professional Drivers", 
            "description": "Licensed, insured, and background-checked chauffeurs with years of experience."
        },
        {
            "icon": "🚗",
            "title": "Your Vehicle",
            "description": "Use your own car while our professionals handle the driving safely and efficiently."
        },
        {
            "icon": "📱", 
            "title": "Easy Booking",
            "description": "Book instantly through our platform with real-time driver tracking and updates."
        }
    ]
    
    for i, (col, feature) in enumerate(zip([col1, col2, col3], features_data)):
        with col:
            render_feature_card(feature)

def render_feature_card(feature: dict):
    """Render individual feature card"""
    st.markdown(f"""
    <div class="feature-card">
        <h4>{feature['icon']} {feature['title']}</h4>
        <p>{feature['description']}</p>
    </div>
    """, unsafe_allow_html=True)
