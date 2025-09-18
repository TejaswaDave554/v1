"""
Pricing Section Component
"""

import streamlit as st
from config.settings import AppConfig

def render_pricing():
    """Render pricing section"""
    st.markdown("## 💰 Transparent Pricing")
    
    col1, col2, col3 = st.columns(3)
    
    pricing_plans = [
        {
            "title": "🚗 Standard",
            "price": f"${AppConfig.STANDARD_RATE}/hr", 
            "features": [
                "Professional driver",
                "Your own vehicle", 
                "Basic insurance",
                "24/7 support"
            ],
            "highlighted": False
        },
        {
            "title": "⭐ Premium",
            "price": f"${AppConfig.PREMIUM_RATE}/hr",
            "features": [
                "Senior chauffeur",
                "Vehicle maintenance check",
                "Premium insurance", 
                "Priority booking"
            ],
            "highlighted": True
        },
        {
            "title": "💎 VIP", 
            "price": f"${AppConfig.VIP_RATE}/hr",
            "features": [
                "Executive chauffeur",
                "Concierge services",
                "Full comprehensive coverage",
                "Personal assistant"
            ],
            "highlighted": False
        }
    ]
    
    for col, plan in zip([col1, col2, col3], pricing_plans):
        with col:
            render_pricing_card(plan)

def render_pricing_card(plan: dict):
    """Render individual pricing card"""
    border_style = 'border-color: #667eea;' if plan['highlighted'] else ''
    features_html = ''.join([f"<li>{feature}</li>" for feature in plan['features']])
    
    st.markdown(f"""
    <div class="price-card" style="{border_style}">
        <h3>{plan['title']}</h3>
        <h2 style="color: #667eea;">{plan['price']}</h2>
        <ul style="text-align: left; margin: 1rem 0;">
            {features_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)
