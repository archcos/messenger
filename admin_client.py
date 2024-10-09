import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import time
from datetime import datetime

class AdminApplication:
    def __init__(self, master):
        self.master = master
        master.title("Admin Page")

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
                self.socket.send("IS Admin".encode('utf-8'))
                threading.Thread(target=self.receive_messages, daemon=True).start()
                self.update_chat_history("Connected to server!\nWelcome IS Admin!\n")
                break
            except (ConnectionRefusedError, TimeoutError):
                self.update_chat_history("Failed to connect to server. Retrying...\n")
                time.sleep(5)
            except Exception as e:
                self.update_chat_history(f"Failed to connect to server: {e}\n")
                break

    def send_message(self):
        timestamp = self.get_timestamp()
        message = self.message_entry.get()
        full_message = f"IS Admin: {message}"
        if full_message:
            self.socket.send(full_message.encode('utf-8'))
            self.update_chat_history(f"{timestamp} [IS Admin]: " + message + "\n")
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    if message.startswith("/user"):
                        self.show_private_chat(message)  # Handle private message
                        print(f"user {message}")
                    elif message.startswith("/ismsg"):
                        self.show_private_chat(message)  # Handle admin messages
                        print(f"ism {message}")
                    else:
                        self.update_chat_history(message[9:] + "\n")
                        print("Chat" +message[9:])
            except ConnectionResetError:
                self.update_chat_history("Disconnected from server.\n")
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def send_private_message(self, chat_history, message_entry, recipient):
            timestamp = self.get_timestamp()
            message = message_entry.get()
            print(f"ms {message}, ss {recipient}")
            if message:
                print(recipient)  # Ensure the message is not empty
                self.socket.send(f"/private:{recipient}:{message}".encode('utf-8'))  # Send the private message
                chat_history.config(state='normal')
                chat_history.insert('end', f"{timestamp} [IS Admin]: " + message + "\n")
                chat_history.config(state='disabled')
                message_entry.delete(0, 'end')

    def show_private_chat(self, message):
        parts = message.split(":")
        print(message)
        if len(parts) < 2:
            return  # Unexpected message format

        sender = parts[1].replace("Private message from ", "").strip()
        chat_message = parts[2]
        print(f"sender {sender}")
        print(message)

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

        timestamp = self.get_timestamp()
        chat_history.config(state='normal')
        chat_history.insert('end', f"{timestamp} [{sender}]: {chat_message}\n")
        chat_history.config(state='disabled')

 

    def close_private_chat(self, recipient):
        """Close the private chat window."""
        if recipient in self.private_chat_windows:
            del self.private_chat_windows[recipient]

    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApplication(root)
    root.mainloop()
