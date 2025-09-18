"""
Testimonials Section Component
"""

import streamlit as st

def render_testimonials():
    """Render testimonials section"""
    st.markdown("## 💬 What Our Customers Say")
    
    col1, col2 = st.columns(2)
    
    testimonials_data = [
        {
            "text": "Excellent service! The driver was professional and my car was in perfect condition. Highly recommend Chaalak for anyone who wants to use their own vehicle.",
            "author": "Sarah M., Business Executive"
        },
        {
            "text": "Perfect for special occasions when you want to arrive in your own luxury car but don't want to drive. The chauffeur was impeccably dressed and very courteous.",
            "author": "James R., Entrepreneur"
        }
    ]
    
    for col, testimonial in zip([col1, col2], testimonials_data):
        with col:
            render_testimonial_card(testimonial)

def render_testimonial_card(testimonial: dict):
    """Render individual testimonial card"""
    st.markdown(f"""
    <div class="testimonial">
        <p>"{testimonial['text']}"</p>
        <strong>- {testimonial['author']}</strong>
    </div>
    """, unsafe_allow_html=True)
