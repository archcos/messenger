import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
from datetime import datetime
import time

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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.private_chat_windows = {}

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        while True:
            try:
                self.socket.connect(self.server_address)
                self.update_chat_history(f"Connected to server!\nWelcome {self.username}!\n")
                self.socket.sendall(self.username.encode('utf-8'))
                threading.Thread(target=self.receive_messages, daemon=True).start()
                break
            except (ConnectionRefusedError, TimeoutError):
                self.update_chat_history("Failed to connect to server. Retrying...\n")
                time.sleep(5)
            except Exception as e:
                self.update_chat_history(f"Failed to connect to server: {e}\n")
                break

    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def send_message(self):
        message = self.message_entry.get()
        timestamp = self.get_timestamp()
        if message:
            full_message = f"{timestamp} [{self.username}]: {message}"
            self.update_chat_history(full_message + "\n")
            self.message_entry.delete(0, tk.END)
            threading.Thread(target=self.send_to_server, args=(full_message,), daemon=True).start()

    def send_to_server(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.update_chat_history(f"Error sending message: {e}\n")

    def receive_messages(self):
        timestamp = self.get_timestamp()
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message.startswith("/users"):
                    self.receive_user_list(message[6:])
                elif message.startswith("/ismsg"):
                    self.show_is_chat(message[6:])
                elif message.startswith("IS"):
                    full_message = f"{timestamp} {message}"
                    print(message)
                    self.update_is_chat_history(full_message + "\n")
                else:
                    self.update_chat_history(message + "\n")
            except ConnectionResetError:
                self.update_chat_history("Disconnected from server.\n")
                break
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
        self.is_chat_window = tk.Toplevel(self.master)
        self.is_chat_window.title("Chat with IS Admin")

        self.is_chat_history = scrolledtext.ScrolledText(self.is_chat_window, state='disabled')
        self.is_chat_history.pack(fill='both', expand=True)

        self.is_message_entry = tk.Entry(self.is_chat_window)
        self.is_message_entry.pack(fill='x', padx=5, pady=5)

        send_button = tk.Button(self.is_chat_window, text="Send", command=self.send_is_message)
        send_button.pack(pady=5)

        self.is_message_entry.bind("<Return>", lambda event: self.send_is_message())

        message = f"/ismsg {self.username} wants to chat"
        self.send_to_server(message)

    def send_is_message(self):
        message = self.is_message_entry.get()
        timestamp = self.get_timestamp()
        receiver = "IS Admin"
        if message:
            full_message = f"{timestamp} [{self.username}]: {message}"
            self.update_is_chat_history(full_message + "\n")
            self.socket.send(f"/ismsg:{receiver}:{message}".encode('utf-8'))  # Send the private message
            self.is_message_entry.delete(0, tk.END)

    def update_is_chat_history(self, message):
        self.is_chat_history.config(state='normal')
        self.is_chat_history.insert(tk.END, message)
        self.is_chat_history.config(state='disabled')
        self.is_chat_history.see(tk.END)

    def show_is_chat(self, message):
        self.update_is_chat_history(message + "\n")

    def handle_private_message(self, message):
        parts = message.split(": ", 1)
        if len(parts) < 2:
            return

        sender = parts[0].strip()
        chat_message = parts[1].strip()

        if sender not in self.private_chat_windows:
            private_chat_window = tk.Toplevel(self.master)
            private_chat_window.title(f"Private Chat with {sender}")

            chat_history = scrolledtext.ScrolledText(private_chat_window, state='disabled')
            chat_history.pack(fill='both', expand=True)

            message_entry = tk.Entry(private_chat_window)
            message_entry.pack(fill='x', padx=5, pady=5)

            send_button = tk.Button(private_chat_window, text="Send", command=lambda: self.send_private_message(chat_history, message_entry, sender))
            send_button.pack(pady=5)

            message_entry.bind("<Return>", lambda event: self.send_private_message(chat_history, message_entry, sender))

            self.private_chat_windows[sender] = (chat_history, message_entry)

            private_chat_window.protocol("WM_DELETE_WINDOW", lambda: self.close_private_chat(sender))
        else:
            chat_history, _ = self.private_chat_windows[sender]

        chat_history.config(state='normal')
        chat_history.insert('end', f"{sender}: {chat_message}\n")
        chat_history.config(state='disabled')

    def send_private_message(self, chat_history, message_entry, recipient):
        message = message_entry.get()
        if message:
            full_message = f"/private {recipient}:{message}"
            threading.Thread(target=self.send_to_server, args=(full_message,), daemon=True).start()
            chat_history.config(state='normal')
            chat_history.insert('end', f"Me: {message}\n")
            chat_history.config(state='disabled')
            message_entry.delete(0, 'end')

    def close_private_chat(self, recipient):
        if recipient in self.private_chat_windows:
            del self.private_chat_windows[recipient]

if __name__ == "__main__":
    root = tk.Tk()
    username = simpledialog.askstring("Username", "Enter your username:")
    app = MainApplication(root, username)
    root.mainloop()
