import os
import uuid
import pymysql
from dotenv import load_dotenv

load_dotenv()

class MySQLDB:
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', '')
        self.database = os.getenv('MYSQL_DATABASE', 'chaalak_db')
        self.port = int(os.getenv('MYSQL_PORT', 3306))

    def get_connection(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                connect_timeout=5,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except Exception as e:
            import sys
            print(f"DATABASE CONNECTION ERROR: {e}", file=sys.stderr, flush=True)
            raise ConnectionError(f"Database connection failed: {e}")

    def fetch_all(self, query: str, params=tuple()):
        try:
            conn = self.get_connection()
            try:
                cur = conn.cursor()
                cur.execute(query, params)
                return cur.fetchall()
            finally:
                try:
                    cur.close()
                except:
                    pass
                conn.close()
        except Exception as e:
            raise Exception(f"Database query failed: {e}")

    def fetch_one(self, query: str, params=tuple()):
        rows = self.fetch_all(query, params)
        return rows[0] if rows else None

    def execute(self, query: str, params=tuple()):
        try:
            conn = self.get_connection()
            try:
                cur = conn.cursor()
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount
            finally:
                try:
                    cur.close()
                except:
                    pass
                conn.close()
        except Exception as e:
            raise Exception(f"Database execution failed: {e}")

    def get_user_by_id(self, user_id: str):
        return self.fetch_one(
            "SELECT * FROM users WHERE id=%s AND is_active=1",
            (user_id,)
        )

    def get_user_by_username(self, username: str):
        return self.fetch_one(
            "SELECT * FROM users WHERE username=%s AND is_active=1",
            (username,)
        )

    def create_user(self, user_data: dict):
        user_id = user_data.get('id') or str(uuid.uuid4())
        self.execute(
            """INSERT INTO users 
            (id, username, email, password_hash, phone, role, full_name, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                user_id,
                user_data['username'],
                user_data['email'],
                user_data['password_hash'],
                user_data.get('phone'),
                user_data.get('role', 'customer'),
                user_data.get('full_name'),
                user_data.get('is_active', True)
            )
        )
        return user_id

    def get_driver_by_user_id(self, user_id: str):
        return self.fetch_one("SELECT * FROM drivers WHERE user_id=%s", (user_id,))

    def create_driver(self, driver_data: dict):
        driver_id = driver_data.get('id') or str(uuid.uuid4())
        self.execute(
            """INSERT INTO drivers 
            (id, user_id, license_number, license_expiry, experience_years, rating, is_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                driver_id,
                driver_data['user_id'],
                driver_data['license_number'],
                driver_data['license_expiry'],
                driver_data.get('experience_years', 0),
                driver_data.get('rating', 5.00),
                driver_data.get('is_available', True)
            )
        )
        return driver_id

    def create_booking(self, booking_data: dict):
        booking_id = booking_data.get('id') or str(uuid.uuid4())
        self.execute(
            """INSERT INTO bookings 
            (id, customer_id, driver_id, pickup_location, dropoff_location, 
             pickup_datetime, service_type, vehicle_type, status, 
             estimated_fare, actual_fare, special_instructions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                booking_id,
                booking_data['customer_id'],
                booking_data.get('driver_id'),
                booking_data['pickup_location'],
                booking_data['dropoff_location'],
                booking_data['pickup_datetime'],
                booking_data['service_type'],
                booking_data['vehicle_type'],
                booking_data.get('status', 'pending'),
                booking_data['estimated_fare'],
                booking_data.get('actual_fare'),
                booking_data.get('special_instructions', '')
            )
        )
        return booking_id

    def get_bookings_by_customer(self, customer_id: str):
        return self.fetch_all(
            "SELECT * FROM bookings WHERE customer_id=%s ORDER BY created_at DESC",
            (customer_id,)
        )

    def get_bookings_by_driver(self, driver_id: str):
        return self.fetch_all(
            "SELECT * FROM bookings WHERE driver_id=%s ORDER BY created_at DESC",
            (driver_id,)
        )

    def get_all_bookings(self):
        return self.fetch_all("SELECT * FROM bookings ORDER BY created_at DESC")

    def get_all_users(self):
        return self.fetch_all("SELECT id, username, email, phone, role, full_name, is_active, created_at FROM users ORDER BY created_at DESC")

    def get_all_drivers_with_users(self):
        return self.fetch_all(
            """SELECT d.*, u.username, u.email, u.phone, u.full_name 
            FROM drivers d 
            JOIN users u ON d.user_id = u.id 
            ORDER BY d.created_at DESC"""
        )

    def get_booking_stats(self):
        return self.fetch_one(
            """SELECT 
            COUNT(*) as total_bookings,
            SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END) as cancelled,
            SUM(CASE WHEN status='completed' THEN estimated_fare ELSE 0 END) as total_revenue
            FROM bookings"""
        )

    def get_pending_unassigned_bookings(self):
        return self.fetch_all(
            """SELECT * FROM bookings 
            WHERE status='pending' AND driver_id IS NULL 
            ORDER BY created_at DESC"""
        )

    def update_booking_status(self, booking_id: str, status: str, driver_id: str = None):
        if driver_id is None:
            return self.execute(
                "UPDATE bookings SET status=%s WHERE id=%s",
                (status, booking_id)
            )
        return self.execute(
            "UPDATE bookings SET status=%s, driver_id=%s WHERE id=%s",
            (status, driver_id, booking_id)
        )

    def delete_booking(self, booking_id: str):
        return self.execute(
            "DELETE FROM bookings WHERE id=%s",
            (booking_id,)
        )

    def update_booking_rating(self, booking_id: str, rating: int, feedback: str = None):
        return self.execute(
            "UPDATE bookings SET rating=%s, feedback=%s WHERE id=%s",
            (rating, feedback, booking_id)
        )

    def get_driver_average_rating(self, driver_id: str):
        result = self.fetch_one(
            "SELECT AVG(rating) as avg_rating, COUNT(rating) as total_ratings FROM bookings WHERE driver_id=%s AND rating IS NOT NULL",
            (driver_id,)
        )
        return result if result else {'avg_rating': 0, 'total_ratings': 0}

    def cancel_booking(self, booking_id: str):
        return self.execute(
            "UPDATE bookings SET status='cancelled' WHERE id=%s",
            (booking_id,)
        )

    def read_table(self, table_name: str):
        if table_name != 'bookings':
            raise ValueError(f"Unsupported table_name: {table_name}")
        return self.get_all_bookings()

    def connect(self):
        return self.get_connection()

db = MySQLDB()
