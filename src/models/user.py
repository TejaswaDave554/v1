"""
User Data Model
"""

from typing import Optional, Dict, List
from config.database import db_manager
import bcrypt

class User:
    """User model class"""
    
    def __init__(self, user_id: int, username: str, email: str, 
                 first_name: str, last_name: str, phone: str = None):
        self.id = user_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
    
    @classmethod
    def create(cls, username: str, email: str, first_name: str, 
               last_name: str, phone: str, password: str) -> Optional['User']:
        """Create new user"""
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        query = """
            INSERT INTO users (username, email, first_name, last_name, phone, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (username, email, first_name, last_name, phone, password_hash.decode('utf-8'))
        
        try:
            user_id = db_manager.execute_insert(query, params)
            return cls.get_by_id(user_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = ? AND is_active = 1"
        result = db_manager.execute_query(query, (user_id,))
        
        if result:
            row = result[0]
            return cls(
                user_id=row['id'],
                username=row['username'],
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone=row['phone']
            )
        return None
    
    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['User']:
        """Authenticate user credentials"""
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        result = db_manager.execute_query(query, (username,))
        
        if result:
            row = result[0]
            stored_hash = row['password_hash'].encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return cls(
                    user_id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    phone=row['phone']
                )
        return None
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone
        }
