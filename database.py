# database.py
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import bcrypt
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.users = self.db[Config.USERS_COLLECTION]
        self.jobs = self.db[Config.JOBS_COLLECTION]
        self.saved_jobs = self.db[Config.SAVED_JOBS_COLLECTION]
        
        # Create indexes
        self.setup_indexes()
        
        
    def setup_indexes(self):
        """Create necessary indexes for optimization"""
        # Unique email index
        self.users.create_index("email", unique=True)
        # Job indexes for searching
        self.jobs.create_index("job_title")
        self.jobs.create_index("company")
        self.jobs.create_index("location")
        # Compound index for saved_jobs
        self.saved_jobs.create_index([("user_id", 1), ("job_id", 1)], unique=True)
    
    def register_user(self, email, password):
        """Register a new user with hashed password"""
        try:
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            user_doc = {
                "email": email,
                "password": hashed_password,
                "registration_date": datetime.now(),
                "last_login": None
            }
            
            result = self.users.insert_one(user_doc)
            return True, str(result.inserted_id)