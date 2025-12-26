-- Create Database
CREATE DATABASE IF NOT EXISTS chaalak_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE chaalak_db;

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB;

CREATE TABLE drivers (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_expiry DATE NOT NULL,
    experience_years INT DEFAULT 0,
    vehicle_types JSON,
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_trips INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    background_verified BOOLEAN DEFAULT FALSE,
    documents JSON,
    location JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_license (license_number)
) ENGINE=InnoDB;

CREATE TABLE vehicles (
    id VARCHAR(36) PRIMARY KEY,
    driver_id VARCHAR(36) NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type ENUM('sedan', 'suv', 'hatchback', 'luxury', 'van') NOT NULL,
    color VARCHAR(30),
    insurance_expiry DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
    INDEX idx_driver_id (driver_id),
    INDEX idx_vehicle_type (vehicle_type)
) ENGINE=InnoDB;

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL,
    INDEX idx_customer_id (customer_id),
    INDEX idx_driver_id (driver_id),
    INDEX idx_status (status),
    INDEX idx_pickup_datetime (pickup_datetime)
) ENGINE=InnoDB;

CREATE TABLE payments (
    id VARCHAR(36) PRIMARY KEY,
    booking_id VARCHAR(36) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'card', 'upi', 'netbanking') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    payment_gateway VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    INDEX idx_booking_id (booking_id),
    INDEX idx_status (payment_status)
) ENGINE=InnoDB;

-- Sample Users
INSERT INTO users (id, username, email, password_hash, phone, role, full_name) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'john_doe', 'john@example.com', SHA2('customer123', 256), '+1234567890', 'customer', 'John Doe'),
('550e8400-e29b-41d4-a716-446655440001', 'driver_mike', 'mike@example.com', SHA2('driver123', 256), '+9876543210', 'driver', 'Mike Wilson'),
('550e8400-e29b-41d4-a716-446655440002', 'admin_user', 'admin@chaalak.com', SHA2('admin123', 256), '+1122334455', 'admin', 'Admin User');

-- Sample Driver
INSERT INTO drivers (id, user_id, license_number, license_expiry, experience_years, vehicle_types, documents, location) VALUES 
('660e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440001', 'DL123456789', '2026-12-31', 5, '["sedan", "suv"]', '{"license_verified": true}', '{"city": "Mumbai", "area": "Bandra"}');

-- Sample Vehicle
INSERT INTO vehicles (id, driver_id, make, model, year, license_plate, vehicle_type, color, insurance_expiry) VALUES 
('770e8400-e29b-41d4-a716-446655440000', '660e8400-e29b-41d4-a716-446655440000', 'Honda', 'City', 2022, 'MH01AB1234', 'sedan', 'White', '2025-12-31');

-- Sample Booking
INSERT INTO bookings (id, customer_id, pickup_location, dropoff_location, pickup_datetime, service_type, estimated_fare) VALUES 
('880e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440000', 'Mumbai Airport', 'Bandra West', '2025-10-15 10:00:00', 'airport_transfer', 450.00);

-- Check all tables were created
SHOW TABLES;

-- Check sample data
SELECT * FROM users;
SELECT * FROM drivers;
SELECT * FROM bookings;

-- Check table structures
DESCRIBE users;
DESCRIBE drivers;
DESCRIBE bookings;
