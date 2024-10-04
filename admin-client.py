import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
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

        self.server_address = ('192.168.51.75', 53214) 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            self.socket.connect(self.server_address)
            self.socket.send("IS Admin".encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f "Error connecting to server: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    if message.startswith("Message from"):
                        self.show_private_chat(message)  # Display the private chat message
                    else:
                        self.update_chat_history(message + "\n")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def show_private_chat(self, message):
        username = message.split(":")[0].split(" ")[-1]
        private_chat_window = tk.Toplevel(self.master)
        private_chat_window.title(f"Private Chat with {username}")

        private_chat_history = scrolledtext.ScrolledText(private_chat_window, state='disabled')
        private_chat_history.pack(fill='both', expand=True)

        private_message_entry = tk.Entry(private_chat_window)
        private_message_entry.pack(fill='x', padx=5, pady=5)

        send_button = tk.Button(private_chat_window, text="Send", command=lambda: self.send_private_message(private_message_entry, username))
        send_button.pack(pady=5)

        private_message_entry.bind("<Return>", lambda event: self.send_private_message(private_message_entry, username))

        private_chat_history.config(state='normal')
        private_chat_history.insert(tk.END, message + "\n")
        private_chat_history.config(state='disabled')
        private_chat_history.see(tk.END)

    def send_private_message(self, private_message_entry, username):
        message = private_message_entry.get()
        if message:
            full_message = f"Message from IS Admin: {message}"
            private_message_entry.delete(0, tk.END)
            self.socket.send(full_message.encode('utf-8'))

    def update_chat_history(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_entry.delete(0, tk.END)
            self.socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApplication(root)
    root.mainloop()