import tkinter as tk
from tkinter import messagebox
import socket
from PIL import Image, ImageTk  # Import Pillow for image handling
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
guest_login_window.geometry("300x300")
guest_login_window.resizable(False, False)

# Load and resize the logo
original_logo = Image.open("logo.png")  # Load the image
resized_logo = original_logo.resize((150, 150), Image.LANCZOS)  # Resize the image
logo = ImageTk.PhotoImage(resized_logo)  # Convert to PhotoImage

logo_label = tk.Label(guest_login_window, image=logo)
logo_label.pack()

# Username Entry
name_label = tk.Label(guest_login_window, text="LocalLinks", font=("Arial", 12,"bold", "italic"), fg="#C70000")
name_label.pack()

username_label = tk.Label(guest_login_window, text="Enter your username:", font=("Arial", 10))
username_label.pack(pady=10)

username_entry = tk.Entry(guest_login_window, font=("Arial", 12), bg="#FFE6E6", fg="#C70000", borderwidth=2, relief="groove")
username_entry.pack(pady=5)

# Guest Login Button
guest_button = tk.Button(guest_login_window, text="Login as Guest", command=login, bg="#FF4D4D", fg="white", font=("Arial", 12, "bold"), relief="raised")
guest_button.pack(pady=10)

# Start the GUI loop
guest_login_window.mainloop()
