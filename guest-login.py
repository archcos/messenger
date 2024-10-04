import tkinter as tk
from tkinter import messagebox
import socket
from main import MainApplication  # Import MainApplication class from main.py

def start_client(username):
    """Start the main application with the provided username."""
    guest_login_window.destroy()  # Close the login window

    # Create a new Tkinter window for the main application
    main_window = tk.Tk()
    
    # Initialize the main application with the username
    app = MainApplication(main_window, username)  # Pass the username
    main_window.mainloop()  # Start the main application loop

def login():
    """Handle guest login logic."""
    username = username_entry.get().strip()  # Get username input
    if not username:  # Default to PC name if no username is entered
        username = socket.gethostname()
    messagebox.showinfo("Login", f"Logged in as: {username}")
    start_client(username)  # Start the client application

# Create guest login window
guest_login_window = tk.Tk()
guest_login_window.title("Guest Login")
# guest_login_window.iconbitmap("logo.ico")

# Username Entry
username_label = tk.Label(guest_login_window, text="Enter your username:")
username_label.pack(pady=5)
username_entry = tk.Entry(guest_login_window)
username_entry.pack(pady=5)

# Guest Login Button
guest_button = tk.Button(guest_login_window, text="Login as Guest", command=login)
guest_button.pack(pady=10)

# Start the GUI loop
guest_login_window.mainloop()
