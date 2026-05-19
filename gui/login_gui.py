import tkinter as tk
from tkinter import messagebox
import gui.styles as theme  # Connect directly to our styling architecture

class LoginWindow:
    def __init__(self, root, auth_manager=None, on_success_callback=None):
        self.root = root
        self.auth_manager = auth_manager
        self.on_success_callback = on_success_callback
        
        self.root.title("JTS - Authentication")
        self.root.geometry("400x530")
        self.root.resizable(False, False)
        self.root.configure(bg=theme.WHITE) # Matches modern registration canvas background
        
        self.current_frame = None
        self.show_login_screen()
        self.root.deiconify()

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_login_screen(self):
        self.clear_current_frame()
        # Style the frame backing with clean white surface
        self.current_frame = tk.Frame(self.root, padx=30, pady=20, bg=theme.WHITE)
        self.current_frame.pack(fill="both", expand=True)
        
        # Professional Heading using our Executive Navy Palette Text
        title_label = tk.Label(self.current_frame, text="Welcome Back", font=("Helvetica", 20, "bold"), bg=theme.WHITE, fg=theme.NAVY)
        title_label.pack(pady=(30, 25))
        
        tk.Label(self.current_frame, text="Email Address:", font=("Arial", 10, "bold"), bg=theme.WHITE, fg=theme.TEXT_MAIN).pack(anchor="w", pady=(0, 5))
        self.email_entry = theme.create_input(self.current_frame, width=32)
        self.email_entry.pack(pady=(0, 20))
        
        tk.Label(self.current_frame, text="Password:", font=("Arial", 10, "bold"), bg=theme.WHITE, fg=theme.TEXT_MAIN).pack(anchor="w", pady=(0, 5))
        self.password_entry = theme.create_input(self.current_frame, width=32)
        self.password_entry.config(show="*")
        self.password_entry.pack(pady=(0, 35))
        
        # Sleek Flat Login Execution Control Action
        login_btn = theme.create_btn(self.current_frame, "Login", self.handle_login)
        login_btn.config(width=25, font=("Arial", 11, "bold"), pady=8)
        login_btn.pack(pady=10)
        
        # Clean Flat Link Interface Component
        switch_btn = tk.Button(self.current_frame, text="Don't have an account? Register here", font=("Arial", 9, "underline"), borderwidth=0, bg=theme.WHITE, fg="#457B9D", activebackground=theme.WHITE, activeforeground=theme.NAVY, cursor="hand2")
        switch_btn.config(command=self.show_register_screen)
        switch_btn.pack(pady=10)

    def show_register_screen(self):
        self.clear_current_frame()
        self.current_frame = tk.Frame(self.root, padx=30, pady=20, bg=theme.WHITE)
        self.current_frame.pack(fill="both", expand=True)
        
        # Clean registration tracking banner text headers
        title_label = tk.Label(self.current_frame, text="Create Account", font=("Helvetica", 20, "bold"), bg=theme.WHITE, fg=theme.NAVY)
        title_label.pack(pady=(30, 25))
        
        tk.Label(self.current_frame, text="Email Address:", font=("Arial", 10, "bold"), bg=theme.WHITE, fg=theme.TEXT_MAIN).pack(anchor="w", pady=(0, 5))
        self.reg_email_entry = theme.create_input(self.current_frame, width=32)
        self.reg_email_entry.pack(pady=(0, 20))
        
        tk.Label(self.current_frame, text="Password:", font=("Arial", 10, "bold"), bg=theme.WHITE, fg=theme.TEXT_MAIN).pack(anchor="w", pady=(0, 5))
        self.reg_password_entry = theme.create_input(self.current_frame, width=32)
        self.reg_password_entry.config(show="*")
        self.reg_password_entry.pack(pady=(0, 35))
        
        # Clean account generation control triggers
        signup_btn = theme.create_btn(self.current_frame, "Register", self.handle_signup, role="refresh")
        signup_btn.config(width=25, font=("Arial", 11, "bold"), pady=8)
        signup_btn.pack(pady=10)
        
        back_btn = tk.Button(self.current_frame, text="Back to Login", font=("Arial", 10, "underline"), borderwidth=0, bg=theme.WHITE, fg=theme.TEXT_MUTED, activebackground=theme.WHITE, activeforeground=theme.TEXT_MAIN, cursor="hand2", command=self.go_back)
        back_btn.pack(pady=10)

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
            # Check if auth_manager is present
            if self.auth_manager and hasattr(self.auth_manager, 'get_collection'):
                self.auth_manager.get_collection("users").insert_one(data)
                messagebox.showinfo("Success", "Account created successfully!") 
                self.go_back() 
            else:
                # If auth_manager is missing, trigger the except block explicitly
                raise ConnectionError("Database manager (auth_manager) was not passed to the Login Window.")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save user to MongoDB: {e}")
    def go_back(self):
        self.show_login_screen()
        
        
    def logout(self):
        self.master.destroy()
        from gui.login_gui import LoginWindow
        root = tk.Tk()
        
        # Make sure to pass your active DBManager class here as well
        from database.db_manager import DBManager
        LoginWindow(root, auth_manager=DBManager())
        root.mainloop()