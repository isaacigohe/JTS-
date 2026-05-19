import tkinter as tk
from tkinter import ttk

# =====================================================================
# JTS PROFESSIONAL PALETTE MATRICES
# =====================================================================
NAVY = "#0D1B2A"         # Deep executive navy header background
BLUE_ACCENT = "#1B263B"  # Primary functional blue button focus
GREY_BG = "#E0E1DD"      # Clean neutral slate background canvas
WHITE = "#FFFFFF"        # Secondary clean surfaces
TEXT_MAIN = "#1B263B"    # Clear typography tracking ink
TEXT_MUTED = "#5F6368"   # Subtle contrast metadata labeling ink
ALERT_RED = "#E63946"    # Danger/Logout target action indicator

def apply_global_styles():
    """Configures the unified clam engine styles across all app components."""
    style = ttk.Style()
    style.theme_use("clam")
    
    # Standardize Table Treeview Layout properties
    style.configure("Treeview", 
                    background=WHITE, 
                    foreground=TEXT_MAIN, 
                    rowheight=35, # Extra padding makes text easy to read
                    fieldbackground=WHITE, 
                    font=("Arial", 10))
    
    style.configure("Treeview.Heading", 
                    font=("Arial", 10, "bold"), 
                    background=GREY_BG, 
                    foreground=TEXT_MAIN, 
                    relief="flat", 
                    padding=8)
    
    # Modern highlight selection track colors
    style.map("Treeview", 
              background=[('selected', '#A8DADC')], 
              foreground=[('selected', TEXT_MAIN)])

def create_btn(parent, text, command, role="primary"):
    """Factory helper to build consistent flat modern buttons instantly."""
    bg_color = BLUE_ACCENT
    if role == "danger": bg_color = ALERT_RED
    if role == "secondary": bg_color = "#6D6875"
    if role == "refresh": bg_color = "#457B9D"
    
    return tk.Button(
        parent, text=text, command=command,
        bg=bg_color, fg=WHITE, font=("Arial", 10, "bold"),
        relief="flat", bd=0, padx=15, pady=6, cursor="hand2",
        activebackground=bg_color, activeforeground=WHITE
    )

def create_input(parent, width=30):
    """Generates an input field with a solid edge layout."""
    return tk.Entry(parent, font=("Arial", 11), width=width, relief="solid", bd=1)