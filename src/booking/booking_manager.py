from datetime import datetime
from typing import Dict, List, Optional
from config.database import db_manager

class BookingManager:

    @staticmethod
    def create_booking(user_id: int, pickup_location: str, destination: str,
                      pickup_date: str, pickup_time: str, vehicle_type: str,
                      duration: str, special_requests: str = "") -> int:

        query =
        params = (user_id, pickup_location, destination, pickup_date,
                 pickup_time, vehicle_type, duration, special_requests)

        return db_manager.execute_insert(query, params)

    @staticmethod
    def get_user_bookings(user_id: int) -> List[Dict]:

        query =

        results = db_manager.execute_query(query, (user_id,))
        return [dict(row) for row in results] if results else []

    @staticmethod
    def update_booking_status(booking_id: int, status: str) -> bool:

        query = "UPDATE bookings SET status = ? WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (status, booking_id))
        return affected_rows > 0

    @staticmethod
    def assign_driver(booking_id: int, driver_id: int) -> bool:

        query = "UPDATE bookings SET driver_id = ?, status = 'confirmed' WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (driver_id, booking_id))
        return affected_rows > 0
