import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
from datetime import datetime

class MainApplicationAdmin:
    def __init__(self, master):
        self.master = master
        master.title("IS Admin Page")

        self.chat_requests = {}  # To track active chat requests

        # Chat history area
        self.chat_history = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_history.pack(fill='both', expand=True)

        # Method to receive messages from users
        threading.Thread(target=self.receive_user_messages, daemon=True).start()

    def receive_user_messages(self):
        while True:
            try:
                # Replace this with actual code to receive messages from the server
                message = self.socket.recv(1024).decode('utf-8')
                if message.startswith("/ismsg"):
                    self.handle_chat_request(message[6:])  # Get username from message
                else:
                    self.update_chat_history(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def handle_chat_request(self, username):
        if username not in self.chat_requests:
            self.chat_requests[username] = self.create_chat_window(username)

    def create_chat_window(self, username):
        chat_window = tk.Toplevel(self.master)
        chat_window.title(f"Chat with {username}")

        chat_history = scrolledtext.ScrolledText(chat_window, state='disabled')
        chat_history.pack(fill='both', expand=True)

        message_entry = tk.Entry(chat_window)
        message_entry.pack(fill='x', padx=5, pady=5)

        send_button = tk.Button(chat_window, text="Send", command=lambda: self.send_admin_message(username, message_entry, chat_history))
        send_button.pack(pady=5)

        message_entry.bind("<Return>", lambda event: self.send_admin_message(username, message_entry, chat_history))

        return chat_window

    def send_admin_message(self, username, message_entry, chat_history):
        message = message_entry.get()
        timestamp = self.get_timestamp()
        if message:
            full_message = f"{timestamp} [IS Admin]: {message}"
            self.update_chat_history(full_message + "\n", chat_history)
            message_entry.delete(0, tk.END)
            threading.Thread(target=self.send_to_server, args=(f"/ismsg {username}: {full_message}",), daemon=True).start()

    def update_chat_history(self, message, chat_history):
        chat_history.config(state='normal')
        chat_history.insert(tk.END, message)
        chat_history.config(state='disabled')
        chat_history.see(tk.END)

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplicationAdmin(root)
    root.mainloop()
