import tkinter as tk
from tkinter import messagebox
import os
from main import MainApplication  # Import MainApplication class from main.py

def start_client():
    """Start the main application for guests."""
    guest_login_window.destroy()  # Close the login window

    # Create a new Tkinter window for the main application
    main_window = tk.Tk()
    app = MainApplication(main_window, "Guest PC")  # Pass a PC name or any identifier
    main_window.mainloop()  # Start the main application loop

def login():
    """Handle guest login logic."""
    messagebox.showinfo("Login", "Guest logged in")
    start_client()  # Start the client application for guest

# Create guest login window
guest_login_window = tk.Tk()
guest_login_window.title("Guest Login")
guest_login_window.iconbitmap("logo.ico")

# Guest Login Button
guest_button = tk.Button(guest_login_window, text="Login as Guest", command=login)
guest_button.pack(pady=10)

# Start the GUI loop
guest_login_window.mainloop()
