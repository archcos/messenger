import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class MainApplication:
    def __init__(self, master, pc_name):
        self.master = master
        self.pc_name = pc_name
        master.title("Main Page")
        master.iconbitmap("logo.ico")
        
        self.pc_name_label = tk.Label(master, text=f"PC Name: {self.pc_name}", font=("Arial", 14))
        self.pc_name_label.pack(pady=10)

        self.side_panel = tk.Frame(master, width=150, bg='lightgrey')
        self.side_panel.pack(side='left', fill='y')

        btn1 = tk.Button(self.side_panel, text="Chat")
        btn1.pack(pady=10)

        btn2 = tk.Button(self.side_panel, text="Contact IS")
        btn2.pack(pady=10)

        btn3 = tk.Button(self.side_panel, text="Exit", command=master.quit)
        btn3.pack(pady=10)

        self.chat_frame = tk.Frame(master)
        self.chat_frame.pack(side='right', fill='both', expand=True)

        self.chat_history = scrolledtext.ScrolledText(self.chat_frame, state='disabled')
        self.chat_history.pack(fill='both', expand=True)

        self.message_entry = tk.Entry(self.chat_frame)
        self.message_entry.pack(fill='x', padx=5, pady=5)

        send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        send_button.pack(pady=5)

        self.server_address = ('192.168.50.219', 12345)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Start a thread for the server connection
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            self.socket.connect(self.server_address)
            self.update_chat_history("Connected to server!\n")
        except Exception as e:
            self.update_chat_history(f"Failed to connect to server: {e}\n")

    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.update_chat_history(f"{self.pc_name}: {message}\n")
            self.message_entry.delete(0, tk.END)

            # Send the message to the server in a separate thread
            threading.Thread(target=self.send_to_server, args=(message,), daemon=True).start()

    def send_to_server(self, message):
        try:
            self.socket.sendall(message.encode())
        except Exception as e:
            self.update_chat_history(f"Error sending message: {e}\n")
