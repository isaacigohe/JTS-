import bcrypt
from database.db_manager import DBManager

class AuthManager:
    def __init__(self):
        self.db_manager = DBManager()
        self.users_collection = self.db_manager.get_collection("users")

    def register_user(self, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {"email": email, "password": hashed_password.decode('utf-8')}
        self.users_collection.insert_one(user_data)
        return True

    def login_user(self, email, password):
        user = self.users_collection.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return user
        return None
