"""
Driver Data Model
"""

from typing import Optional, List, Dict
from config.database import db_manager

class Driver:
    """Driver model class"""
    
    def __init__(self, driver_id: int, name: str, email: str, phone: str,
                 license_number: str, rating: float = 0.0, 
                 experience_years: int = 0, is_available: bool = True):
        self.id = driver_id
        self.name = name
        self.email = email
        self.phone = phone
        self.license_number = license_number
        self.rating = rating
        self.experience_years = experience_years
        self.is_available = is_available
    
    @classmethod
    def create(cls, name: str, email: str, phone: str, license_number: str,
               experience_years: int = 0) -> Optional['Driver']:
        """Create new driver"""
        query = """
            INSERT INTO drivers (name, email, phone, license_number, experience_years)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (name, email, phone, license_number, experience_years)
        
        try:
            driver_id = db_manager.execute_insert(query, params)
            return cls.get_by_id(driver_id)
        except Exception as e:
            print(f"Error creating driver: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, driver_id: int) -> Optional['Driver']:
        """Get driver by ID"""
        query = "SELECT * FROM drivers WHERE id = ?"
        result = db_manager.execute_query(query, (driver_id,))
        
        if result:
            row = result[0]
            return cls(
                driver_id=row['id'],
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                license_number=row['license_number'],
                rating=row['rating'],
                experience_years=row['experience_years'],
                is_available=bool(row['is_available'])
            )
        return None
    
    @classmethod
    def get_available_drivers(cls) -> List['Driver']:
        """Get all available drivers"""
        query = "SELECT * FROM drivers WHERE is_available = 1 ORDER BY rating DESC"
        results = db_manager.execute_query(query)
        
        drivers = []
        if results:
            for row in results:
                driver = cls(
                    driver_id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    phone=row['phone'],
                    license_number=row['license_number'],
                    rating=row['rating'],
                    experience_years=row['experience_years'],
                    is_available=bool(row['is_available'])
                )
                drivers.append(driver)
        
        return drivers
    
    def update_availability(self, is_available: bool) -> bool:
        """Update driver availability"""
        query = "UPDATE drivers SET is_available = ? WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (is_available, self.id))
        if affected_rows > 0:
            self.is_available = is_available
            return True
        return False
    
    def update_rating(self, new_rating: float) -> bool:
        """Update driver rating"""
        query = "UPDATE drivers SET rating = ? WHERE id = ?"
        affected_rows = db_manager.execute_update(query, (new_rating, self.id))
        if affected_rows > 0:
            self.rating = new_rating
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert driver to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'license_number': self.license_number,
            'rating': self.rating,
            'experience_years': self.experience_years,
            'is_available': self.is_available
        }
