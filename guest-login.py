import tkinter as tk
from tkinter import messagebox
import socket
from PIL import Image, ImageTk  
from client import MainApplication 



def start_client(username):
    guest_login_window.destroy() 
    main_window = tk.Tk()
    app = MainApplication(main_window, username)  
    main_window.mainloop() 

def request_user_list():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(sock)
    sock.settimeout(5)  # Set a timeout of 5 seconds
    try:
        server_address = ('172.16.10.155', 53214)
        sock.connect(server_address)
        sock.sendall("/users".encode('utf-8'))
        user_list = sock.recv(1024).decode('utf-8')
        print(f"User list received: {user_list}")  # For debugging
        return user_list
    except socket.timeout:
        messagebox.showerror("Error", "Request to server timed out.")
        return ""
    except ConnectionRefusedError:
        messagebox.showerror("Error", "Connection refused. Is the server running?")
        return ""
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return ""
    finally:
        sock.close()

def login():
    username = username_entry.get().strip()
    
    
    # Request the user list from the server
    user_list = request_user_list()

    if not user_list or len(user_list) == 1:
        # No users connected or invalid response, allow login directly
        messagebox.showinfo("Login", f"Logged in as: {username}")
        start_client(username)
        return

    for user in user_list[1:]:
        if user.strip().lower() == username.lower():
            messagebox.showerror("Error", "Username is already connected. Please choose another.")
            return

    if username.lower() == "is admin":
        messagebox.showerror("Error", "Username 'IS Admin' is not allowed.")
        return

    if not username: 
        username = socket.gethostname()

    messagebox.showinfo("Login", f"Logged in as: {username}")
    start_client(username)

guest_login_window = tk.Tk()
guest_login_window.title("Guest Login")
guest_login_window.geometry("300x300")
guest_login_window.resizable(False, False)

original_logo = Image.open("logo.png")  
resized_logo = original_logo.resize((150, 150), Image.LANCZOS) 
logo = ImageTk.PhotoImage(resized_logo)

logo_label = tk.Label(guest_login_window, image=logo)
logo_label.pack()

name_label = tk.Label(guest_login_window, text="LocalLinks", font=("Arial", 12, "bold", "italic"), fg="#C70000")
name_label.pack()

username_label = tk.Label(guest_login_window, text ="Enter your username:", font=("Arial", 10))
username_label.pack(pady=10)

username_entry = tk.Entry(guest_login_window, font=("Arial", 10), bg="#FFE6E6", borderwidth=2, relief="groove")
username_entry.pack(pady=5)

guest_login_window.bind('<Return>', lambda event: login())

guest_button = tk.Button(guest_login_window, text="Login as Guest", command=login, bg="#FF4D4D", fg="white", font=("Arial", 12, "bold"), relief="raised")
guest_button.pack(pady=10)

guest_login_window.mainloop()