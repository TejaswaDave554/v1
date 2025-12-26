# Chaalak - Professional Chauffeur Services
## Complete Documentation

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [API Reference](#api-reference)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)

---

## Overview

Chaalak is a full-featured chauffeur booking platform built with Streamlit and MySQL. It provides a complete solution for customers to book professional drivers, drivers to manage rides and earnings, and admins to oversee operations.

### Technology Stack
- **Frontend**: Streamlit 1.28+
- **Backend**: Python 3.8+
- **Database**: MySQL 8.0+ (using PyMySQL)
- **Authentication**: SHA-256 password hashing
- **Session Management**: 30-minute timeout
- **Logging**: Python logging module

---

## Features

### Customer Features
- **Ride Booking**: Book immediate or scheduled rides
- **Fare Calculator**: Real-time fare estimation with detailed breakdown
- **Ride History**: View all bookings with filters (status, date range)
- **Rating System**: Rate drivers after completed rides
- **Cancel Bookings**: Cancel pending or confirmed rides
- **Emergency SOS**: Quick access to emergency contacts
- **Session Management**: Auto-logout after 30 minutes of inactivity

### Driver Features
- **Accept/Reject Rides**: View and manage available ride requests
- **Earnings Dashboard**: Track daily, weekly, and monthly earnings
- **Trip History**: View all trips with filters
- **Export Reports**: Download earnings as CSV
- **Rating Visibility**: View customer ratings and feedback
- **End Ride**: Mark rides as completed

### Admin Features
- **Dashboard**: Overview of all bookings, users, and drivers
- **Statistics**: Total bookings, revenue, completion rates
- **User Management**: View all registered users
- **Driver Management**: View all registered drivers
- **Booking Management**: Monitor all bookings in real-time

---

## Installation

### Prerequisites
```bash
Python 3.8 or higher
MySQL 8.0 or higher
pip (Python package manager)
```

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Chaalak
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup MySQL database**
```bash
mysql -u root -p < data/script.sql
```

5. **Configure environment variables**

Create a `.env` file in the root directory:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=chaalak_db
MYSQL_PORT=3306

# Optional: Email notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

6. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| MYSQL_HOST | MySQL server host | localhost | Yes |
| MYSQL_USER | MySQL username | root | Yes |
| MYSQL_PASSWORD | MySQL password | - | Yes |
| MYSQL_DATABASE | Database name | chaalak_db | Yes |
| MYSQL_PORT | MySQL port | 3306 | Yes |
| SMTP_SERVER | Email server | smtp.gmail.com | No |
| SMTP_PORT | Email port | 587 | No |
| SENDER_EMAIL | Sender email | - | No |
| SENDER_PASSWORD | Email password | - | No |

### Streamlit Configuration

Located in `.streamlit/config.toml`:
```toml
[theme]
base = "light"
primaryColor = "#4F46E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F9FAFB"
textColor = "#1F2937"

[client]
toolbarMode = "minimal"

[server]
enableCORS = true
enableXsrfProtection = true
```

---

## Usage

### Default Credentials

#### Customer Account
- Username: `john_doe`
- Password: `customer123`

#### Driver Account
- Username: `driver_mike`
- Password: `driver123`

#### Admin Account
- Username: `admin_user`
- Password: `admin123`

### Customer Workflow

1. **Register/Login**
   - Navigate to Login page
   - Enter credentials or register new account
   - Choose "Customer" account type

2. **Book a Ride**
   - Go to "Book Ride" tab
   - Enter pickup and dropoff locations
   - Select vehicle type and service type
   - Choose immediate or scheduled booking
   - View fare estimate
   - Click "Book Now"

3. **View Bookings**
   - Go to "My Bookings" tab
   - Filter by status or date range
   - View booking details
   - Cancel pending bookings
   - End confirmed rides
   - Rate completed rides

4. **Emergency SOS**
   - Go to "Emergency" tab
   - Enter emergency contact
   - Click "Send SOS Alert"

### Driver Workflow

1. **Login**
   - Use driver credentials
   - Redirected to Driver Dashboard

2. **Accept Rides**
   - View available rides in "Available Rides" section
   - Click "Accept" to take a ride
   - Click "Skip" to delete unwanted requests

3. **Manage Trips**
   - Go to "My Trips" tab
   - View all accepted rides
   - Click "End Ride" for confirmed trips
   - View customer ratings and feedback

4. **Track Earnings**
   - Go to "Earnings" tab
   - View daily, weekly, monthly earnings
   - See recent earnings breakdown
   - Export earnings report as CSV

### Admin Workflow

1. **Login**
   - Use admin credentials
   - Redirected to Admin Dashboard

2. **Monitor System**
   - View statistics (bookings, revenue, etc.)
   - Check "Users" tab for all customers
   - Check "Drivers" tab for all drivers
   - Check "Bookings" tab for all rides

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('customer', 'driver', 'admin') DEFAULT 'customer',
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Drivers Table
```sql
CREATE TABLE drivers (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_expiry DATE NOT NULL,
    experience_years INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_trips INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    driver_id VARCHAR(36),
    pickup_location VARCHAR(255) NOT NULL,
    dropoff_location VARCHAR(255) NOT NULL,
    pickup_datetime DATETIME NOT NULL,
    service_type ENUM('airport_transfer', 'corporate', 'wedding', 'hourly', 'outstation') NOT NULL,
    vehicle_type ENUM('sedan', 'suv', 'hatchback', 'luxury', 'van') DEFAULT 'sedan',
    status ENUM('pending', 'confirmed', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    estimated_fare DECIMAL(10,2) NOT NULL,
    actual_fare DECIMAL(10,2),
    special_instructions TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL
);
```

---

## API Reference

### Database Operations

#### User Operations

**get_user_by_id(user_id: str)**
- Returns user details by ID
- Returns: dict or None

**get_user_by_username(username: str)**
- Returns user details by username
- Returns: dict or None

**create_user(user_data: dict)**
- Creates new user
- Parameters: username, email, password_hash, phone, role, full_name
- Returns: user_id (str)

**get_all_users()**
- Returns all users (admin only)
- Returns: list of dicts

#### Booking Operations

**create_booking(booking_data: dict)**
- Creates new booking
- Parameters: customer_id, pickup_location, dropoff_location, pickup_datetime, service_type, vehicle_type, estimated_fare, special_instructions
- Returns: booking_id (str)

**get_bookings_by_customer(customer_id: str)**
- Returns all bookings for a customer
- Returns: list of dicts

**get_bookings_by_driver(driver_id: str)**
- Returns all bookings for a driver
- Returns: list of dicts

**update_booking_status(booking_id: str, status: str, driver_id: str = None)**
- Updates booking status
- Status values: 'pending', 'confirmed', 'completed', 'cancelled'
- Returns: row count

**cancel_booking(booking_id: str)**
- Cancels a booking
- Returns: row count

**delete_booking(booking_id: str)**
- Deletes a booking
- Returns: row count

**update_booking_rating(booking_id: str, rating: int, feedback: str = None)**
- Adds rating and feedback to completed booking
- Rating: 1-5
- Returns: row count

#### Driver Operations

**get_driver_by_user_id(user_id: str)**
- Returns driver profile
- Returns: dict or None

**create_driver(driver_data: dict)**
- Creates driver profile
- Parameters: user_id, license_number, license_expiry, experience_years
- Returns: driver_id (str)

**get_driver_average_rating(driver_id: str)**
- Returns driver's average rating and total ratings
- Returns: dict with avg_rating and total_ratings

**get_all_drivers_with_users()**
- Returns all drivers with user details (admin only)
- Returns: list of dicts

#### Admin Operations

**get_all_bookings()**
- Returns all bookings
- Returns: list of dicts

**get_booking_stats()**
- Returns booking statistics
- Returns: dict with total_bookings, completed, pending, cancelled, total_revenue

**get_pending_unassigned_bookings()**
- Returns all pending bookings without assigned driver
- Returns: list of dicts

### Fare Calculator

**calculate_fare(distance_km: float, vehicle_type: str, service_type: str, duration_hours: float = 0)**
- Calculates fare based on parameters
- Returns: dict with base_fare, distance_fare, service_charge, total_fare, breakdown

**estimate_distance(pickup: str, dropoff: str)**
- Estimates distance between locations
- Returns: float (km)

### Session Management

**check_session_timeout()**
- Checks if session has expired (30 minutes)
- Returns: bool

**is_logged_in()**
- Checks if user is logged in and session is valid
- Returns: bool

**logout_user()**
- Clears session state
- Returns: None

### Notifications

**send_email_notification(to_email: str, subject: str, body: str)**
- Sends email notification
- Returns: bool (success/failure)

**notify_booking_confirmed(user_email: str, booking_details: dict)**
- Sends booking confirmation email
- Returns: bool

**notify_ride_completed(user_email: str, booking_id: str)**
- Sends ride completion email
- Returns: bool

---

## Security

### Password Security
- SHA-256 hashing for all passwords
- Minimum password requirements:
  - At least 8 characters
  - One uppercase letter
  - One lowercase letter
  - One number
  - One special character
- Password strength validation on registration

### Session Security
- 30-minute inactivity timeout
- Automatic logout on timeout
- Session state cleared on logout

### Database Security
- Parameterized queries (SQL injection protection)
- Connection timeout: 5 seconds
- Error handling for all database operations

### Input Validation
- Email format validation
- Phone number validation (minimum 10 digits)
- Username validation (minimum 3 characters)
- License number validation (minimum 5 characters)

### Logging
- All login attempts logged
- Failed login attempts tracked
- Error logging with user context
- Log files stored in `logs/` directory

---

## Troubleshooting

### Common Issues

**1. Database Connection Failed**
```
Error: Database connection failed
```
Solution:
- Check MySQL is running: `net start MySQL80`
- Verify credentials in `.env` file
- Ensure database exists: `chaalak_db`
- Check port 3306 is not blocked

**2. Import Errors**
```
Error: Import Error: No module named 'streamlit'
```
Solution:
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

**3. Session Timeout**
```
Error: Session expired. Please login again
```
Solution:
- This is normal after 30 minutes of inactivity
- Simply login again

**4. Email Notifications Not Working**
```
Warning: Email notification failed
```
Solution:
- Configure SMTP settings in `.env`
- Use app-specific password for Gmail
- Email notifications are optional

**5. Port Already in Use**
```
Error: Port 8501 is already in use
```
Solution:
- Stop other Streamlit instances
- Or use different port: `streamlit run app.py --server.port 8502`

### Debug Mode

Run with verbose logging:
```bash
streamlit run app.py --logger.level=debug
```

Check logs:
```bash
# View today's log
type logs\app_YYYYMMDD.log
```

### Database Reset

To reset database:
```bash
mysql -u root -p
DROP DATABASE chaalak_db;
CREATE DATABASE chaalak_db;
USE chaalak_db;
SOURCE data/script.sql;
```

---

## Project Structure

```
Chaalak/
├── app.py                      # Main entry point
├── Home.py                     # Home page logic
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
├── DOCUMENTATION.md            # This file
├── .gitignore                  # Git ignore rules
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── pages/                      # Streamlit pages
│   ├── Login.py               # Login page
│   ├── Register.py            # Registration page
│   ├── User_Dashboard.py      # Customer dashboard
│   ├── Driver_Dashboard.py    # Driver dashboard
│   └── Admin_Dashboard.py     # Admin dashboard
│
├── src/
│   ├── auth/                  # Authentication
│   │   ├── auth_utils.py      # Auth utilities
│   │   ├── login.py           # Login component
│   │   ├── register.py        # Registration component
│   │   └── password_validator.py  # Password validation
│   │
│   ├── components/            # UI components
│   │   ├── hero_section.py
│   │   ├── features.py
│   │   ├── statistics.py
│   │   ├── pricing.py
│   │   ├── testimonials.py
│   │   └── footer.py
│   │
│   └── utils/                 # Utilities
│       ├── custom_css.py      # Custom styling
│       ├── session_manager.py # Session management
│       ├── error_logger.py    # Error logging
│       ├── fare_calculator.py # Fare calculation
│       └── notifications.py   # Email notifications
│
├── config/
│   ├── database.py            # Database operations
│   └── settings.py            # App configuration
│
├── data/
│   └── script.sql             # Database schema
│
└── logs/                      # Application logs
    └── app_YYYYMMDD.log
```

---

## Support

For issues or questions:
- Email: support@chaalak.com
- GitHub: Open an issue in the repository

---

## License

This project is licensed under the MIT License.

---

## Version History

### v1.0.0 (Current)
- Initial release
- Customer booking system
- Driver management
- Admin dashboard
- Rating system
- Fare calculator
- Session management
- Email notifications
- Error logging
- Emergency SOS

---

*Last Updated: December 2025*
