"""
Sample Data for Development and Testing
"""

from config.database import db_manager
from src.models.user import User
from src.models.driver import Driver
from src.models.booking import Booking

def populate_sample_data():
    """Populate database with sample data for development"""
    
    # Sample users
    sample_users = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+1234567890',
            'password': 'password123'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+1987654321',
            'password': 'password456'
        }
    ]
    
    # Sample drivers
    sample_drivers = [
        {
            'name': 'Michael Johnson',
            'email': 'michael@chaalak.com',
            'phone': '+1555123456',
            'license_number': 'DL123456789',
            'experience_years': 5
        },
        {
            'name': 'Sarah Wilson',
            'email': 'sarah@chaalak.com',
            'phone': '+1555987654',
            'license_number': 'DL987654321',
            'experience_years': 8
        },
        {
            'name': 'David Brown',
            'email': 'david@chaalak.com',
            'phone': '+1555456789',
            'license_number': 'DL456789123',
            'experience_years': 3
        }
    ]
    
    print("Populating sample data...")
    
    # Create sample users
    for user_data in sample_users:
        user = User.create(**user_data)
        if user:
            print(f"Created user: {user.username}")
    
    # Create sample drivers
    for driver_data in sample_drivers:
        driver = Driver.create(**driver_data)
        if driver:
            print(f"Created driver: {driver.name}")
    
    print("Sample data population complete!")

if __name__ == "__main__":
    populate_sample_data()
