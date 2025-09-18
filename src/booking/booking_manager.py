"""
Booking Management Operations
"""

from datetime import datetime
from typing import Dict, List, Optional
from config.database import db_manager

class BookingManager:
    """Manages booking operations"""
    
    @staticmethod
    def create_booking(user_id: int, pickup_location: str, destination: str,
                      pickup_date: str, pickup_time: str, vehicle_type: str,
                      duration: str, special_requests: str = "") -> int:
        """Create a new booking"""
        query = """
            INSERT INTO bookings (user_id, pickup_location, destination, pickup_date, 
                                pickup_time, vehicle_type, duration, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (user_id, pickup_location, destination, pickup_date, 
                 pickup_time, vehicle_type, duration, special_requests)
        
        return db_manager.execute_insert(query, params)
    
    @staticmethod
    def get_user_bookings(user_id: int) -> List[Dict]:
        """Get all bookings for a user"""
        query = """
            SELECT b.*, d.name as driver_name
            FROM bookings b
            LEFT JOIN drivers d ON b.driver_id = d.id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC
        """
        
        results = db_manager.execute_query(query, (user_id,))
        return [dict(row) for row in results] if results else []
    
    @staticmethod
    def update_booking_status(booking_id: int, status: str) -> bool:
        """Update booking status"""
        query = "UPDATE bookings SET status = ? WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (status, booking_id))
        return affected_rows > 0
    
    @staticmethod
    def assign_driver(booking_id: int, driver_id: int) -> bool:
        """Assign driver to booking"""
        query = "UPDATE bookings SET driver_id = ?, status = 'confirmed' WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (driver_id, booking_id))
        return affected_rows > 0
