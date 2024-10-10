import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import socket
from PIL import Image, ImageTk  
from client import MainApplication 
import random
import string
import ctypes

def generate_random_character():
    return random.choice(string.ascii_letters + string.digits)

def start_client(username):
    guest_login_window.destroy() 
    main_window = tk.Tk()
    app = MainApplication(main_window, username)  
    main_window.mainloop() 

def login():
    username = username_entry.get().strip()
    selected_option = dropdown.get()
    r = generate_random_character()
    r2 = generate_random_character()

    if selected_option == "":
        messagebox.showerror("Error", "Please select a valid username from the dropdown.")
        return
    
    full_username = f"{selected_option}{r}{r2}-{username}"
    
    if username == "":
        username = socket.gethostname()
    
    messagebox.showinfo("Login", f"Logged in as: {full_username}")
    start_client(full_username)

guest_login_window = tk.Tk()
guest_login_window.title("Guest Login")
guest_login_window.geometry("300x300")
guest_login_window.resizable(False, False)

original_logo = Image.open("logo.png")  
resized_logo = original_logo.resize((100, 100), Image.LANCZOS) 
logo = ImageTk.PhotoImage(resized_logo)

logo_label = tk.Label(guest_login_window, image=logo)
logo_label.pack()

name_label = tk.Label(guest_login_window, text="LocalLinks", font=("Arial", 12, "bold", "italic"), fg="#C70000")
name_label.pack()

dept_label = tk.Label(guest_login_window, text ="Select Department:", font=("Arial", 10))
dept_label.pack(pady=(10, 0))  

options = ["", "ASD", "CALP", "CRD", "FAD", "HRD", "SA", "VSD", "OTHERS"]
dropdown = ttk.Combobox(guest_login_window, values=options, state="readonly")
dropdown.pack(pady=(10, 0))   

username_label = tk.Label(guest_login_window, text ="Create Username:", font=("Arial", 10))
username_label.pack(pady=(10, 0))  

username_entry = tk.Entry(guest_login_window, font=("Arial", 10), bg="#FFE6E6", borderwidth=2, relief="groove")
username_entry.pack(pady=5)

guest_login_window.bind('<Return>', lambda event: login())

guest_button = tk.Button(guest_login_window, text="Login as Guest", command=login, bg="#FF4D4D", fg="white", font=("Arial", 12, "bold"), relief="raised")
guest_button.pack(pady=10)

myappid = 'archcos.locallinks.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
guest_login_window.iconbitmap('logobg.ico')
guest_login_window.mainloop()