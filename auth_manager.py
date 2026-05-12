import bcrypt
from database.db_manager import DatabaseManager
from config import Config

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def hash_password(self, password):
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt(rounds=Config.SALT_ROUNDS)
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password, hashed):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def register_user(self, email, password):
        """Register a new user"""
        # Validation
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        # Hash password and create user
        hashed_pw = self.hash_password(password)
        user_id = self.db.create_user(email, hashed_pw)
        
        return user_id
    
    def login_user(self, email, password):
        """Authenticate a user"""
        user = self.db.get_user_by_email(email)
        
        if not user:
            raise ValueError("Invalid email or password")
        
        if not self.verify_password(password, user['password']):
            raise ValueError("Invalid email or password")
        
        return user