from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, PyMongoError
from datetime import datetime
from config import Config

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DB_NAME]
            self._setup_collections()
            self._initialized = True
            print("✓ Database connected successfully")
        except PyMongoError as e:
            print(f"✗ Database connection failed: {e}")
            raise
    
    def _setup_collections(self):
        """Create collections and indexes"""
        # Users collection
        self.users = self.db[Config.USERS_COLLECTION]
        self.users.create_index([("email", ASCENDING)], unique=True)
        
        # Jobs collection
        self.jobs = self.db[Config.JOBS_COLLECTION]
        self.jobs.create_index([("job_id", ASCENDING)], unique=True)
        self.jobs.create_index([("title", ASCENDING)])
        self.jobs.create_index([("company", ASCENDING)])
        
        # Saved jobs collection
        self.saved_jobs = self.db[Config.SAVED_JOBS_COLLECTION]
        self.saved_jobs.create_index([("user_id", ASCENDING), ("job_id", ASCENDING)], unique=True)
    
    # User operations
    def create_user(self, email, hashed_password):
        """Create a new user"""
        try:
            user_doc = {
                "email": email,
                "password": hashed_password,
                "created_at": datetime.utcnow()
            }
            result = self.users.insert_one(user_doc)
            return result.inserted_id
        except DuplicateKeyError:
            raise ValueError("Email already exists")
    
    def get_user_by_email(self, email):
        """Retrieve user by email"""
        return self.users.find_one({"email": email})
    
    # Job operations
    def insert_job(self, job_data):
        """Insert or update a job listing"""
        try:
            job_data['scraped_at'] = datetime.utcnow()
            self.jobs.update_one(
                {"job_id": job_data['job_id']},
                {"$set": job_data},
                upsert=True
            )
        except Exception as e:
            print(f"Error inserting job: {e}")
    
    def get_all_jobs(self, limit=100):
        """Get all job listings"""
        return list(self.jobs.find().sort("scraped_at", -1).limit(limit))
    
    def search_jobs(self, query=None, location=None, company=None):
        """Search jobs with filters"""
        filter_dict = {}
        
        if query:
            filter_dict["$or"] = [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        
        if location:
            filter_dict["location"] = {"$regex": location, "$options": "i"}
        
        if company:
            filter_dict["company"] = {"$regex": company, "$options": "i"}
        
        return list(self.jobs.find(filter_dict).sort("scraped_at", -1))
    
    # Saved jobs operations
    def save_job(self, user_id, job_id, status="not applied"):
        """Save a job for a user"""
        try:
            doc = {
                "user_id": str(user_id),
                "job_id": job_id,
                "status": status,
                "saved_at": datetime.utcnow()
            }
            self.saved_jobs.insert_one(doc)
            return True
        except DuplicateKeyError:
            return False  # Already saved
    
    def unsave_job(self, user_id, job_id):
        """Remove a saved job"""
        result = self.saved_jobs.delete_one({
            "user_id": str(user_id),
            "job_id": job_id
        })
        return result.deleted_count > 0
    
    def update_job_status(self, user_id, job_id, status):
        """Update application status"""
        result = self.saved_jobs.update_one(
            {"user_id": str(user_id), "job_id": job_id},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def get_saved_jobs(self, user_id):
        """Get all saved jobs for a user"""
        saved = list(self.saved_jobs.find({"user_id": str(user_id)}))
        
        # Enrich with job details
        result = []
        for saved_job in saved:
            job = self.jobs.find_one({"job_id": saved_job['job_id']})
            if job:
                job['saved_status'] = saved_job['status']
                job['saved_at'] = saved_job['saved_at']
                result.append(job)
        
        return result
    
    def is_job_saved(self, user_id, job_id):
        """Check if a job is saved by user"""
        return self.saved_jobs.find_one({
            "user_id": str(user_id),
            "job_id": job_id
        }) is not None
