"""
Helper Utility Functions
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:.2f}"

def calculate_booking_cost(duration: str, service_type: str) -> float:
    """Calculate booking cost based on duration and service type"""
    from config.settings import AppConfig
    
    # Duration mapping
    duration_hours = {
        "1-2 hours": 1.5,
        "2-4 hours": 3,
        "4-8 hours": 6,
        "Full Day": 8
    }
    
    # Service type rates
    rates = {
        "Standard": AppConfig.STANDARD_RATE,
        "Premium": AppConfig.PREMIUM_RATE,
        "VIP": AppConfig.VIP_RATE
    }
    
    hours = duration_hours.get(duration, 1)
    rate = rates.get(service_type, AppConfig.STANDARD_RATE)
    
    return hours * rate

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M")

def get_greeting() -> str:
    """Get time-appropriate greeting"""
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

def generate_booking_reference() -> str:
    """Generate unique booking reference"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"CK{timestamp}"

def validate_future_datetime(date_str: str, time_str: str) -> bool:
    """Validate that datetime is in the future"""
    try:
        booking_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        return booking_datetime > datetime.now()
    except ValueError:
        return False
