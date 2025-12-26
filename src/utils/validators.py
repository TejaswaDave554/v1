import re
from typing import Dict, Any

def validate_login(username: str, password: str) -> bool:

    return bool(username and password)

def validate_registration(first_name: str, last_name: str, email: str, phone: str,
                        password: str, confirm_password: str, terms_accepted: bool) -> Dict[str, Any]:

    if not all([first_name, last_name, email, phone, password, confirm_password]):
        return {"valid": False, "message": "Please fill in all fields"}

    if not validate_email(email):
        return {"valid": False, "message": "Please enter a valid email address"}

    if not validate_phone(phone):
        return {"valid": False, "message": "Please enter a valid phone number"}

    if password != confirm_password:
        return {"valid": False, "message": "Passwords don't match"}

    if not validate_password_strength(password):
        return {"valid": False, "message": "Password must be at least 6 characters long"}

    if not terms_accepted:
        return {"valid": False, "message": "Please accept the terms and conditions"}

    return {"valid": True, "message": "Valid registration data"}

def validate_email(email: str) -> bool:

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:

    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) >= 10

def validate_password_strength(password: str) -> bool:

    return len(password) >= 6

def validate_booking_form(pickup_location: str, destination: str, pickup_date: str,
                        pickup_time: str, vehicle_type: str, duration: str) -> Dict[str, Any]:

    if not pickup_location.strip():
        return {"valid": False, "message": "Please enter pickup location"}

    if not destination.strip():
        return {"valid": False, "message": "Please enter destination"}

    if not pickup_date:
        return {"valid": False, "message": "Please select pickup date"}

    if not pickup_time:
        return {"valid": False, "message": "Please select pickup time"}

    if not vehicle_type:
        return {"valid": False, "message": "Please select vehicle type"}

    if not duration:
        return {"valid": False, "message": "Please select duration"}

    return {"valid": True, "message": "Valid booking data"}
