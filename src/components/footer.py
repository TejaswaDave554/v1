"""
Footer Component
"""

import streamlit as st
from config.settings import AppConfig

def render_footer():
    """Render footer"""
    st.markdown(f"""
    <div class="footer">
        <h3>🚗 Chaalak - Your Car, Our Expertise</h3>
        <p>📧 {AppConfig.COMPANY_EMAIL} | 📞 {AppConfig.COMPANY_PHONE} | 🌐 {AppConfig.COMPANY_WEBSITE}</p>
        <p style="margin-top: 1rem; opacity: 0.8;">
            © 2025 Chaalak Inc. All rights reserved. | Privacy Policy | Terms of Service
        </p>
    </div>
    """, unsafe_allow_html=True)
