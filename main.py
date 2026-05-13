import sys
import os
import tkinter as tk

# --- CRITICAL PATH FIX ---
# This line finds the folder where main.py is located
project_root = os.path.dirname(os.path.abspath(__file__))
# This line tells Python to look in that folder for all imports
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -------------------------

# Now we can import our modules safely
try:
    from gui.login_gui import LoginWindow
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current Path: {sys.path}")
    sys.exit(1)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window initially
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

