class SessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.current_user = None
        self.is_authenticated = False
        self._initialized = True
    
    def login(self, user):
        """Set current user session"""
        self.current_user = user
        self.is_authenticated = True
    
    def logout(self):
        """Clear current session"""
        self.current_user = None
        self.is_authenticated = False
    
    def get_user_id(self):
        """Get current user ID"""
        return str(self.current_user['_id']) if self.current_user else None
    
    def get_user_email(self):
        """Get current user email"""
        return self.current_user['email'] if self.current_user else None