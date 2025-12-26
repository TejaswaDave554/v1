import os
import uuid
import hashlib

import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "chaalak_db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def create_tables():
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(

            )

            cur.execute(

            )

            cur.execute(

            )

            cur.execute(

            )

        print("✅ Tables created/verified in DB:", DB_NAME)
    finally:
        conn.close()

def seed_data():

    conn = connect_db()
    try:
        with conn.cursor() as cur:

            cur.execute(
                ,
                (
                    str(uuid.uuid4()),
                    "admin",
                    "admin@chaalak.com",
                    hash_password("admin123"),
                    "admin",
                    "Admin User",
                    "0000000000",
                ),
            )

            cur.execute(
                ,
                (
                    str(uuid.uuid4()),
                    "john_doe",
                    "john@example.com",
                    hash_password("customer123"),
                    "customer",
                    "John Doe",
                    "1234567890",
                ),
            )

            cur.execute(
                ,
                (
                    str(uuid.uuid4()),
                    "driver_mike",
                    "mike@example.com",
                    hash_password("driver123"),
                    "driver",
                    "Mike Wilson",
                    "9876543210",
                ),
            )

            cur.execute("SELECT id FROM users WHERE username=%s", ("john_doe",))
            customer_id = cur.fetchone()["id"]

            cur.execute("SELECT id FROM users WHERE username=%s", ("driver_mike",))
            driver_user_id = cur.fetchone()["id"]

            cur.execute(
                ,
                (
                    str(uuid.uuid4()),
                    driver_user_id,
                    "DL123456789",
                    "2026-12-31",
                    5,
                    5.00,
                    True,
                ),
            )

            cur.execute("SELECT id FROM drivers WHERE user_id=%s", (driver_user_id,))
            driver_id = cur.fetchone()["id"]

            cur.execute(
                ,
                (customer_id, "Mumbai Airport", "Bandra"),
            )
            existing = cur.fetchone()

            if existing:
                booking_id = existing["id"]
            else:
                booking_id = str(uuid.uuid4())
                cur.execute(
                    ,
                    (
                        booking_id,
                        customer_id,
                        driver_id,
                        "Mumbai Airport",
                        "Bandra",
                        "2025-12-25 10:00:00",
                        "airport_transfer",
                        "sedan",
                        "confirmed",
                        800.00,
                        "Please wait at Gate 2",
                    ),
                )

            cur.execute(
                "SELECT id FROM payments WHERE booking_id=%s LIMIT 1",
                (booking_id,),
            )
            pay_existing = cur.fetchone()
            if not pay_existing:
                cur.execute(
                    ,
                    (
                        str(uuid.uuid4()),
                        booking_id,
                        800.00,
                        "upi",
                        "completed",
                        "DEMO-TXN-001",
                    ),
                )

        print("✅ Seed data inserted/verified.")
        print("Demo accounts:")
        print("  admin / admin123")
        print("  john_doe / customer123")
        print("  driver_mike / driver123")
    finally:
        conn.close()

def main():
    print(f"🚀 Using existing database: {DB_NAME}")
    create_tables()
    seed_data()
    print("✅ Setup complete.")

if __name__ == "__main__":
    main()
