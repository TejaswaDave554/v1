"""
Booking Data Model
"""

from typing import Optional, List, Dict
from datetime import datetime
from config.database import db_manager

class Booking:
    """Booking model class"""
    
    def __init__(self, booking_id: int, user_id: int, pickup_location: str,
                 destination: str, pickup_date: str, pickup_time: str,
                 vehicle_type: str, duration: str, status: str = 'pending',
                 driver_id: int = None, special_requests: str = None,
                 total_cost: float = None):
        self.id = booking_id
        self.user_id = user_id
        self.driver_id = driver_id
        self.pickup_location = pickup_location
        self.destination = destination
        self.pickup_date = pickup_date
        self.pickup_time = pickup_time
        self.vehicle_type = vehicle_type
        self.duration = duration
        self.special_requests = special_requests
        self.status = status
        self.total_cost = total_cost
    
    @classmethod
    def create(cls, user_id: int, pickup_location: str, destination: str,
               pickup_date: str, pickup_time: str, vehicle_type: str,
               duration: str, special_requests: str = None) -> Optional['Booking']:
        """Create new booking"""
        query = """
            INSERT INTO bookings (user_id, pickup_location, destination, pickup_date,
                                pickup_time, vehicle_type, duration, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (user_id, pickup_location, destination, pickup_date,
                 pickup_time, vehicle_type, duration, special_requests)
        
        try:
            booking_id = db_manager.execute_insert(query, params)
            return cls.get_by_id(booking_id)
        except Exception as e:
            print(f"Error creating booking: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, booking_id: int) -> Optional['Booking']:
        """Get booking by ID"""
        query = "SELECT * FROM bookings WHERE id = ?"
        result = db_manager.execute_query(query, (booking_id,))
        
        if result:
            row = result[0]
            return cls(
                booking_id=row['id'],
                user_id=row['user_id'],
                pickup_location=row['pickup_location'],
                destination=row['destination'],
                pickup_date=row['pickup_date'],
                pickup_time=row['pickup_time'],
                vehicle_type=row['vehicle_type'],
                duration=row['duration'],
                status=row['status'],
                driver_id=row['driver_id'],
                special_requests=row['special_requests'],
                total_cost=row['total_cost']
            )
        return None
    
    @classmethod
    def get_by_user(cls, user_id: int) -> List['Booking']:
        """Get all bookings for a user"""
        query = """
            SELECT * FROM bookings 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """
        results = db_manager.execute_query(query, (user_id,))
        
        bookings = []
        if results:
            for row in results:
                booking = cls(
                    booking_id=row['id'],
                    user_id=row['user_id'],
                    pickup_location=row['pickup_location'],
                    destination=row['destination'],
                    pickup_date=row['pickup_date'],
                    pickup_time=row['pickup_time'],
                    vehicle_type=row['vehicle_type'],
                    duration=row['duration'],
                    status=row['status'],
                    driver_id=row['driver_id'],
                    special_requests=row['special_requests'],
                    total_cost=row['total_cost']
                )
                bookings.append(booking)
        
        return bookings
    
    def update_status(self, new_status: str) -> bool:
        """Update booking status"""
        query = "UPDATE bookings SET status = ? WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (new_status, self.id))
        if affected_rows > 0:
            self.status = new_status
            return True
        return False
    
    def assign_driver(self, driver_id: int) -> bool:
        """Assign driver to booking"""
        query = "UPDATE bookings SET driver_id = ?, status = 'confirmed' WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (driver_id, self.id))
        if affected_rows > 0:
            self.driver_id = driver_id
            self.status = 'confirmed'
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'driver_id': self.driver_id,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'pickup_date': self.pickup_date,
            'pickup_time': self.pickup_time,
            'vehicle_type': self.vehicle_type,
            'duration': self.duration,
            'special_requests': self.special_requests,
            'status': self.status,
            'total_cost': self.total_cost
        }
