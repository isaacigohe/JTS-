import pymongo
from tkinter import messagebox
from utils.config import MONGO_URI, DB_NAME

class DBManager:
    def __init__(self):
        try:
            # Increase timeout to give the cloud connection more time
            self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.client.server_info() # This checks if the connection is actually alive
            print("✅ Successfully connected to MongoDB Atlas.")
        except Exception as e:
            error_msg = f"Could not connect to MongoDB Atlas.\n\nError: {e}\n\nCheck if your IP is whitelisted in the Atlas dashboard."
            print(f"❌ {error_msg}")
            # Show a popup so you know there is a connection problem
            messagebox.showerror("Database Connection Error", error_msg)
            raise e 

        self.db = self.client[DB_NAME]

    def get_collection(self, name):
        return self.db[name]

