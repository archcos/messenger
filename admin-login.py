import tkinter as tk
from tkinter import messagebox
import bcrypt
from PIL import Image, ImageTk 
from admin_client import AdminApplication 

ADMIN_USERNAME = "tcoisd"
ADMIN_PASSWORD_HASH = bcrypt.hashpw("13952".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate_admin(username, password):
    return username == ADMIN_USERNAME and bcrypt.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8'))

def login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate_admin(username, password):
        messagebox.showinfo("Login", "Admin logged in")
        open_main_window() 
    else:
        messagebox.showerror("Login", "Invalid username or password")

def open_main_window():
    login_window.destroy() 

    main_window = tk.Tk()
    main_window.title("Main Application")

    app = AdminApplication(main_window)
    main_window.mainloop()

login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("300x400") 
login_window.resizable(False, False) 

original_logo = Image.open("logo.png")
resized_logo = original_logo.resize((150, 150), Image.LANCZOS)
logo = ImageTk.PhotoImage(resized_logo)

logo_label = tk.Label(login_window, image=logo)
logo_label.pack()

name_label = tk.Label(login_window, text="LocalLinks", font=("Arial", 12, "bold", "italic"), fg="#C70000")
name_label.pack()

username_label = tk.Label(login_window, text="Username", font=("Arial", 10))
username_label.pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 10))
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Password", font=("Arial", 10))
password_label.pack(pady=(10, 5))
password_entry = tk.Entry(login_window, show='*', font=("Arial", 10))
password_entry.pack(pady=5)

login_window.bind('<Return>', lambda event: login())

login_button = tk.Button(login_window, text="Login", command=login, bg="#FF6666", fg="white", font=("Arial", 12, "bold"), relief="raised")
login_button.pack(pady=20)

login_window.mainloop()