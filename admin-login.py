import tkinter as tk
from tkinter import messagebox
import bcrypt
import socket
from main import MainApplication  # Make sure main.py is accessible

# Predefined admin credentials (hashed for security)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = bcrypt.hashpw("13952".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate_admin(username, password):
    return username == ADMIN_USERNAME and bcrypt.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8'))

def login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate_admin(username, password):
        messagebox.showinfo("Login", "Admin logged in")
        open_main_window()  # Open the main application for Admin
    else:
        messagebox.showerror("Login", "Invalid username or password")

def open_main_window():
    login_window.destroy()  # Close the login window

    main_window = tk.Tk()
    main_window.title("Main Application")

    pc_name = socket.gethostname()  # Get the PC name

    # Initialize the main application
    app = MainApplication(main_window, pc_name)
    main_window.mainloop()

# Create login window
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.iconbitmap("logo.ico")

# Username and Password Entry
username_label = tk.Label(login_window, text="Username")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text="Password")
password_label.pack()
password_entry = tk.Entry(login_window, show='*')
password_entry.pack()

# Login Button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack(pady=10)

# Start the GUI loop
login_window.mainloop()
