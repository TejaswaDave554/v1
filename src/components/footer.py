import streamlit as st

def render_footer():
    st.divider()
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <p>© 2025 Chaalak. All rights reserved.</p>
            <p>Contact: support@chaalak.com | 1-800-CHAALAK</p>
        </div>
    """, unsafe_allow_html=True)
