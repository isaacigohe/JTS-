# config.py
import os

class Config:
    # MongoDB Configuration
    MONGO_URI = "mongodb+srv://isaacigohe120_db_user:crdSGNZijQo4K8bE@jit.9quiczw.mongodb.net/?appName=jit"
    DB_NAME = "JTS_db"
    
    # Collections
    USERS_COLLECTION = "users"
    JOBS_COLLECTION = "jobs"
    SAVED_JOBS_COLLECTION = "saved_jobs"
    
    # RemoteOK API
    REMOTEOK_URL = ""
    
    # GUI Configuration
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    PRIMARY_COLOR = "#2C3E50"
    SECONDARY_COLOR = "#3498DB"
    ACCENT_COLOR = "#E74C3C"