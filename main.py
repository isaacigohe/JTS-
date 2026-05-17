import tkinter as tk
from database.db_manager import DBManager
from gui.login_gui import LoginWindow
from gui.main_gui import MainWindow

def on_login_success(root, user_data):
    """
    Callback function that runs when the user authenticates successfully.
    It cleans up the login window elements and builds the dashboard.
    """
    # Initialize the main dashboard window layout
    MainWindow(root, user=user_data)

def main():
    # 1. Initialize the root Tkinter application instance
    root = tk.Tk()
    
    # Hide the main window frame while things load up
    root.withdraw()
    
    try:
        # 2. Establish connection to your MongoDB instance
        auth_manager = DBManager()
        print("Database connection established successfully.")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        auth_manager = None

    # 3. Initialize the Login Interface window
    # We pass the root instance, the db wrapper, and our success callback function
    LoginWindow(root, auth_manager=auth_manager, on_success_callback=on_login_success)
    
    # 4. Start the Tkinter application lifecycle loop
    root.mainloop()

if __name__ == "__main__":
    main()