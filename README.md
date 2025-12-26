# Chaalak - Professional Chauffeur Services

A modern, full-featured chauffeur booking platform built with Streamlit and MySQL.

## Features

### Customer Features
- **Book Rides**: Immediate or scheduled bookings
- **Fare Calculator**: Real-time fare estimation with breakdown
- **Ride History**: Filter by status and date range
- **Rating System**: Rate drivers after ride completion
- **Cancel Bookings**: Cancel pending/confirmed rides
- **Emergency SOS**: Quick access to emergency contacts
- **Session Management**: Auto-logout after 30 minutes of inactivity

### Driver Features
- **Accept/Reject Rides**: View and manage ride requests
- **Earnings Dashboard**: Daily, weekly, monthly earnings tracking
- **Trip History**: Filter trips by status and date
- **Export Reports**: Download earnings as CSV
- **Rating Visibility**: View customer ratings and feedback
- **End Ride**: Mark rides as completed

### Admin Features
- **Dashboard**: Overview of all bookings, users, and drivers
- **Statistics**: Total bookings, revenue, completion rates
- **User Management**: View all users and their details
- **Driver Management**: View all drivers and their information
- **Booking Management**: Monitor all bookings in real-time

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: MySQL 8.0+
- **Authentication**: SHA-256 password hashing
- **Session Management**: Streamlit session state with timeout
- **Logging**: Python logging module

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Chaalak
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
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

## Default Credentials

### Customer Account
- Username: `john_doe`
- Password: `customer123`

### Driver Account
- Username: `driver_mike`
- Password: `driver123`

### Admin Account
- Username: `admin_user`
- Password: `admin123`

## Project Structure

```
Chaalak/
├── app.py                  # Main application entry point
├── pages/                  # Streamlit pages
│   ├── Login.py
│   ├── Register.py
│   ├── User_Dashboard.py
│   ├── Driver_Dashboard.py
│   └── Admin_Dashboard.py
├── src/
│   ├── auth/              # Authentication modules
│   ├── components/        # Reusable UI components
│   ├── utils/             # Utility functions
│   │   ├── custom_css.py
│   │   ├── fare_calculator.py
│   │   ├── notifications.py
│   │   ├── session_manager.py
│   │   └── error_logger.py
├── config/
│   ├── database.py        # Database operations
│   └── settings.py        # App configuration
├── data/
│   └── script.sql         # Database schema
├── logs/                  # Application logs
└── requirements.txt       # Python dependencies
```

## Security Features

- **Password Hashing**: SHA-256 encryption
- **Session Timeout**: 30-minute inactivity logout
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: Email, phone, password strength checks
- **Error Logging**: Comprehensive error tracking
- **Login Attempt Logging**: Track failed login attempts

## API Documentation

### Database Methods

#### User Operations
- `get_user_by_id(user_id)`: Get user by ID
- `get_user_by_username(username)`: Get user by username
- `create_user(user_data)`: Create new user
- `get_all_users()`: Get all users (admin only)

#### Booking Operations
- `create_booking(booking_data)`: Create new booking
- `get_bookings_by_customer(customer_id)`: Get customer bookings
- `get_bookings_by_driver(driver_id)`: Get driver bookings
- `update_booking_status(booking_id, status, driver_id)`: Update booking
- `cancel_booking(booking_id)`: Cancel booking
- `delete_booking(booking_id)`: Delete booking
- `update_booking_rating(booking_id, rating, feedback)`: Add rating

#### Driver Operations
- `get_driver_by_user_id(user_id)`: Get driver profile
- `create_driver(driver_data)`: Create driver profile
- `get_driver_average_rating(driver_id)`: Get driver rating stats
- `get_all_drivers_with_users()`: Get all drivers (admin only)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@chaalak.com or open an issue in the repository.

## Roadmap

- [ ] Real-time GPS tracking
- [ ] Payment gateway integration
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Push notifications
- [ ] Ride scheduling automation
- [ ] Driver background verification system
