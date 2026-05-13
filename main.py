
import tkinter as tk
from gui.login_gui import LoginWindow

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()