import pymongo
import mongomock
from utils.config import MONGO_URI, DB_NAME

class DBManager:
    def __init__(self):
        try:
            # Try real MongoDB first
            self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            self.client.server_info() # Force connection check
            print("Connected to real MongoDB.")
        except Exception:
            print("Real MongoDB not available. Using mongomock for demonstration.")
            self.client = mongomock.MongoClient()
        
        self.db = self.client[DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close_connection(self):
        self.client.close()
