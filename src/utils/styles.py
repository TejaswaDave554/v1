"""
CSS Styles and Theme Management
"""

import streamlit as st

def load_custom_styles():
    """Load custom CSS styles"""
    # Check current theme
    is_dark = st.session_state.get('dark_theme', False)
    
    # Base colors
    bg_color = "#0e1117" if is_dark else "#ffffff"
    text_color = "#ffffff" if is_dark else "#262730"
    card_bg = "#262730" if is_dark else "#ffffff"
    input_bg = "#262730" if is_dark else "#ffffff"
    input_text = "#ffffff" if is_dark else "#262730"
    border_color = "#4a4a4a" if is_dark else "#e0e0e0"
    
    st.markdown(f"""
    <style>
        /* Main app styling */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Fix selectbox styling */
        .stSelectbox > div > div {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        /* Fix selectbox dropdown */
        .stSelectbox > div > div > div {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
        }}
        
        /* Fix text input styling */
        .stTextInput > div > div > input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        /* Fix text area styling */
        .stTextArea > div > div > textarea {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        /* Fix button styling */
        .stButton > button {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        /* Fix form submit button */
        .stFormSubmitButton > button {{
            background-color: #667eea !important;
            color: white !important;
            border: none !important;
        }}
        
        /* Fix date input */
        .stDateInput > div > div > input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        /* Fix time input */
        .stTimeInput > div > div > input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        /* Fix checkbox styling */
        .stCheckbox > label {{
            color: {text_color} !important;
        }}
        
        /* Fix radio button styling */
        .stRadio > label {{
            color: {text_color} !important;
        }}
        
        /* Fix sidebar if needed */
        .css-1d391kg {{
            background-color: {bg_color} !important;
        }}

        .main-header {{
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .feature-card {{
            background: {card_bg};
            color: {text_color};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            border: 1px solid {border_color};
        }}

        .hero-section {{
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 15px;
            margin-bottom: 2rem;
            color: {text_color};
        }}

        .cta-button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            margin: 0.5rem;
            border: none;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}

        .stats-card {{
            text-align: center;
            padding: 1rem;
            background: {card_bg};
            color: {text_color};
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border: 1px solid {border_color};
        }}

        .testimonial {{
            background: {card_bg};
            color: {text_color};
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
            font-style: italic;
            border: 1px solid {border_color};
        }}

        .price-card {{
            background: {card_bg};
            color: {text_color};
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
        
        /* Custom theme toggle indicator */
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
            border: 1px solid {border_color};
        }}
        
        /* Override Streamlit's default form styling */
        [data-testid="stForm"] {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
            padding: 1rem !important;
            border-radius: 10px !important;
        }}
        
        /* Fix expander styling */
        .streamlit-expanderHeader {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        .streamlit-expanderContent {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        /* Fix metric styling */
        [data-testid="metric-container"] {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
            padding: 1rem !important;
            border-radius: 10px !important;
        }}
        
        /* Fix dataframe styling */
        .stDataFrame {{
            background-color: {card_bg} !important;
        }}
        
        /* Fix info/success/warning boxes */
        .stAlert {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
    </style>
    
    <div class="theme-indicator">
        {'🌙 Dark Mode' if is_dark else '☀️ Light Mode'}
    </div>
    """, unsafe_allow_html=True)
