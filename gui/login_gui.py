import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root, auth_manager=None, on_success_callback=None):
        self.root = root
        self.auth_manager = auth_manager
        self.on_success_callback = on_success_callback
        
        self.root.title("Job Tracker System - Authentication")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.current_frame = None
        self.show_login_screen()
        self.root.deiconify()

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_login_screen(self):
        self.clear_current_frame()
        self.current_frame = tk.Frame(self.root, padx=20, pady=20)
        self.current_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(self.current_frame, text="Welcome Back", font=("Arial", 18, "bold"))
        title_label.pack(pady=(20, 30))
        
        tk.Label(self.current_frame, text="Email Address:", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.email_entry = tk.Entry(self.current_frame, font=("Arial", 12), width=30)
        self.email_entry.pack(pady=(0, 15))
        
        tk.Label(self.current_frame, text="Password:", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.password_entry = tk.Entry(self.current_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=(0, 30))
        
        login_btn = tk.Button(self.current_frame, text="Login", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", width=25, command=self.handle_login)
        login_btn.pack(pady=10)
        
        switch_btn = tk.Button(self.current_frame, text="Don't have an account? Register here", font=("Arial", 9, "underline"), borderwidth=0, command=self.show_register_screen)
        switch_btn.pack(pady=5)

    def show_register_screen(self):
        self.clear_current_frame()
        self.current_frame = tk.Frame(self.root, padx=20, pady=20)
        self.current_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(self.current_frame, text="Create Account", font=("Arial", 18, "bold"))
        title_label.pack(pady=(20, 30))
        
        tk.Label(self.current_frame, text="Email Address:", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.reg_email_entry = tk.Entry(self.current_frame, font=("Arial", 12), width=30)
        self.reg_email_entry.pack(pady=(0, 15))
        
        tk.Label(self.current_frame, text="Password:", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.reg_password_entry = tk.Entry(self.current_frame, font=("Arial", 12), width=30, show="*")
        self.reg_password_entry.pack(pady=(0, 30))
        
        signup_btn = tk.Button(self.current_frame, text="Register", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=25, command=self.handle_signup)
        signup_btn.pack(pady=10)
        
        back_btn = tk.Button(self.current_frame, text="Back to Login", font=("Arial", 10), command=self.go_back)
        back_btn.pack(pady=5)

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return
            
        try:
            if self.auth_manager and hasattr(self.auth_manager, 'get_collection'):
                user = self.auth_manager.get_collection("users").find_one({"email": email, "password": password})
            else:
                user = {"_id": "mock_id_12345", "email": email} if email == "admin@test.com" else None

            if user:
                messagebox.showinfo("Success", f"Welcome back, {email}!")
                self.clear_current_frame()
                if self.on_success_callback:
                    self.on_success_callback(self.root, user)
                else:
                    # Circular import solved: Import dynamically only on successful click
                    from .main_gui import MainWindow
                    MainWindow(self.root, user=user)
            else:
                messagebox.showerror("Authentication Failed", "Invalid email address or password structure.")
        except Exception as e:
            messagebox.showerror("Database Connection Error", f"Could not complete authentication: {e}")

    def handle_signup(self):
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
            
        data = {"email": email, "password": password}
        try:
            if self.auth_manager and hasattr(self.auth_manager, 'get_collection'):
                self.auth_manager.get_collection("users").insert_one(data)
            messagebox.showinfo("Success", "Account created successfully!") 
            self.go_back() 
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save user: {e}") 

    def go_back(self):
        self.show_login_screen()