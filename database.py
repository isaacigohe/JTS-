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


