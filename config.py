import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI',"mongodb+srv://isaacigohe120_db_user:crdSGNZijQo4K8bE@jit.9quiczw.mongodb.net/?appName=jit")
    DB_NAME = 'job_tracker_db'
    
    # Collections
    USERS_COLLECTION = 'users'
    JOBS_COLLECTION = 'jobs'
    SAVED_JOBS_COLLECTION = 'saved_jobs'
    
    # Security
    SALT_ROUNDS = 12
    
    # Application
    APP_TITLE = "Job Listing Tracker System"
    WINDOW_SIZE = "1200x700"