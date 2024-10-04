import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
from datetime import datetime

class MainApplication:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("Main Page")

        self.pc_name_label = tk.Label(master, text=f"Username: {self.username}", font=("Arial", 14))
        self.pc_name_label.pack(pady=10)

        self.side_panel = tk.Frame(master, width=150, bg='lightgrey')
        self.side_panel.pack(side='left', fill='y')

        btn1 = tk.Button(self.side_panel, text="Show Online Users", command=self.show_user_list)
        btn1.pack(pady=10)

        btn2 = tk.Button(self.side_panel, text="Contact IS", command=self.open_is_chat)
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

        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.server_address = ('172.16.10.155', 53214) 
        #self.server_address = ('192.168.51.75', 53214)  # Change to your server's IP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            self.socket.connect(self.server_address)
            self.update_chat_history(f"Connected to server!\nWelcome {self.username}!\n")
            self.socket.sendall(self.username.encode('utf-8'))  # Send username
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.update_chat_history(f"Failed to connect to server: {e}\n")

    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def get_timestamp(self):
        """Get the current timestamp formatted as a string."""
        return datetime.now().strftime("%H:%M:%S")

    def send_message(self):
        message = self.message_entry.get()
        timestamp = self.get_timestamp()
        if message:
            my_message = f"[{self.username}]: {message}"
            full_message = f"{timestamp} [{self.username}]: {message}"
            self.update_chat_history(full_message + "\n")
            self.message_entry.delete(0, tk.END)
            threading.Thread(target=self.send_to_server, args=(my_message,), daemon=True).start()

    def send_to_server(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.update_chat_history(f"Error sending message: {e}\n")

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message.startswith("/users"):
                    self.receive_user_list(message[6:])
                elif message.startswith("/ismsg"):
                    self.show_is_chat(message[6:])  # Strip command and show message
                else:
                    self.update_chat_history(message + "\n")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def show_user_list(self):
        self.send_to_server("/users")

    def receive_user_list(self, user_list):
        user_list_window = tk.Toplevel(self.master)
        user_list_window.title("Online Users")
        user_list_display = scrolledtext.ScrolledText(user_list_window, state='normal', height=10, width=30)
        user_list_display.pack(padx=10, pady=10)
        user_list_display.insert(tk.END, user_list)
        user_list_display.config(state='disabled')
        close_button = tk.Button(user_list_window, text="Close", command=user_list_window.destroy)
        close_button.pack(pady=5)

    def open_is_chat(self):
        # Create a new pop-up window for IS Admin chat
        self.is_chat_window = tk.Toplevel(self.master)
        self.is_chat_window.title("Chat with IS Admin")
        
        self.is_chat_history = scrolledtext.ScrolledText(self.is_chat_window, state='disabled')
        self.is_chat_history.pack(fill='both', expand=True)

        self.is_message_entry = tk.Entry(self.is_chat_window)
        self.is_message_entry.pack(fill='x', padx=5, pady=5)

        send_button = tk.Button(self.is_chat_window, text="Send", command=self.send_is_message)
        send_button.pack(pady=5)

        self.is_message_entry.bind("<Return>", lambda event: self.send_is_message())

        # Notify IS Admin about the chat request
        message = f"/ismsg {self.username} wants to chat"
        self.send_to_server(message)

    def send_is_message(self):
        message = self.is_message_entry.get()
        timestamp = self.get_timestamp()
        if message:
            full_message = f"{timestamp} [{self.username}]: {message}"
            self.update_is_chat_history(full_message + "\n")
            self.is_message_entry.delete(0, tk.END)
            threading.Thread(target=self.send_to_server, args=(full_message,), daemon=True).start()

    def update_is_chat_history(self, message):
        self.is_chat_history.config(state='normal')
        self.is_chat_history.insert(tk.END, message)
        self.is_chat_history.config(state='disabled')
        self.is_chat_history.see(tk.END)

    def show_is_chat(self, message):
        self.update_is_chat_history(message + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    username = simpledialog.askstring("Username", "Enter your username:")
    app = MainApplication(root, username)
    root.mainloop()
