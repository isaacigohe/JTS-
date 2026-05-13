import tkinter as tk
from tkinter import messagebox
from auth.auth_manager import AuthManager
from .main_gui import MainWindow

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login / Register")
        self.auth_manager = AuthManager()

        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Email:").grid(row=0, column=0, sticky="w")
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.frame, text="Password:").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=10)

        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.auth_manager.login_user(email, password)
        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()  # Close login window
            self.open_main_window(user)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.auth_manager.register_user(email, password):
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
        else:
            messagebox.showerror("Error", "Registration failed. User might already exist.")

    def open_main_window(self, user):
        root = tk.Tk()
        MainWindow(root, user)
        root.mainloop()