"""
CSS Styles - Minimal Version
"""

import streamlit as st

def load_custom_styles():
    """Load minimal custom CSS styles"""
    
    is_dark = st.session_state.get('dark_theme', False)
    
    st.markdown(f"""
    <style>
        /* Only the custom components that were working fine */
        .feature-card {{
            background: {'#262730' if is_dark else '#ffffff'};
            color: {'#ffffff' if is_dark else '#262730'};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            border: 1px solid {'#4a4a4a' if is_dark else '#e0e0e0'};
        }}

        .hero-section {{
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 15px;
            margin-bottom: 2rem;
            color: {'#ffffff' if is_dark else '#262730'};
        }}

        .stats-card {{
            text-align: center;
            padding: 1rem;
            background: {'#262730' if is_dark else '#ffffff'};
            color: {'#ffffff' if is_dark else '#262730'};
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border: 1px solid {'#4a4a4a' if is_dark else '#e0e0e0'};
        }}

        .testimonial {{
            background: {'#262730' if is_dark else '#f8f9fa'};
            color: {'#ffffff' if is_dark else '#262730'};
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
            font-style: italic;
        }}

        .price-card {{
            background: {'#262730' if is_dark else '#ffffff'};
            color: {'#ffffff' if is_dark else '#262730'};
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s;
        }}

        .price-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
        }}

        .footer {{
            background: #2c3e50;
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-top: 3rem;
            text-align: center;
        }}
        
        /* Theme indicator */
        .theme-indicator {{
            position: fixed;
            top: 10px;
            right: 10px;
            background: {'#333' if is_dark else '#fff'};
            color: {'#fff' if is_dark else '#333'};
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            z-index: 1000;
        }}
    </style>
    
    <div class="theme-indicator">
        {'🌙 Dark Mode' if is_dark else '☀️ Light Mode'}
    </div>
    """, unsafe_allow_html=True)
