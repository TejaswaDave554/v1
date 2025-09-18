"""
Statistics Section Component
"""

import streamlit as st

def render_statistics():
    """Render statistics section"""
    st.markdown("## 📊 Our Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats_data = [
        {"number": "10,000+", "label": "Happy Customers"},
        {"number": "500+", "label": "Professional Drivers"}, 
        {"number": "50+", "label": "Cities Covered"},
        {"number": "24/7", "label": "Service Available"}
    ]
    
    for col, stat in zip([col1, col2, col3, col4], stats_data):
        with col:
            render_stats_card(stat)

def render_stats_card(stat: dict):
    """Render individual statistics card"""
    st.markdown(f"""
    <div class="stats-card">
        <h2 style="color: #667eea;">{stat['number']}</h2>
        <p>{stat['label']}</p>
    </div>
    """, unsafe_allow_html=True)
