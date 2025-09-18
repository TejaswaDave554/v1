"""
Application Configuration and Constants
"""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppConfig:
    """Application configuration constants"""
    APP_TITLE: str = "Chaalak - Professional Chauffeur Services"
    APP_ICON: str = "🚗"
    
    # Authentication
    DEMO_USERNAME: str = "admin"
    DEMO_PASSWORD: str = "admin123"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///chaalak.db")
    
    # Theme settings
    PRIMARY_COLOR: str = "#667eea"
    SECONDARY_COLOR: str = "#764ba2"
    
    # Pricing
    STANDARD_RATE: int = 25
    PREMIUM_RATE: int = 40
    VIP_RATE: int = 65
    
    # Business settings
    COMPANY_EMAIL: str = "contact@chaalak.com"
    COMPANY_PHONE: str = "1-800-CHAALAK"
    COMPANY_WEBSITE: str = "www.chaalak.com"

class SessionKeys:
    """Session state keys constants"""
    LOGGED_IN = "logged_in"
    USER_NAME = "user_name"
    USER_ID = "user_id"
    DARK_THEME = "dark_theme"
    SHOW_DEMO_INFO = "show_demo_info"
    CURRENT_PAGE = "current_page"

# Sample data for development
SAMPLE_BOOKINGS = [
    {
        "date": "2025-09-10",
        "driver": "John Smith",
        "route": "Airport → Home",
        "status": "Completed",
        "rating": "⭐⭐⭐⭐⭐"
    },
    {
        "date": "2025-09-08", 
        "driver": "Sarah Johnson",
        "route": "Office → Restaurant",
        "status": "Completed",
        "rating": "⭐⭐⭐⭐"
    }
]
