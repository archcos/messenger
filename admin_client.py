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
            self.update_chat_history(f"Connected to server!\nWelcome {self.username}!\n")
            self.socket.sendall(self.username.encode('utf-8'))  # Send username
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except ConnectionRefusedError:
            self.update_chat_history("Connection refused. Please ensure the server is running.\n")
        except TimeoutError:
            self.update_chat_history("Connection timed out. Please check your network connection.\n")
        except Exception as e:
            self.update_chat_history(f"Failed to connect to server: {e}\n")

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    if message.startswith("Private message from"):
                        self.show_private_chat(message)  # Display the private chat message
                    elif message.startswith("Message from"):
                        self.show_private_chat(message)  # Display the private chat message
                    else:
                        self.update_chat_history(message + "\n")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_message(self):
        message = self.message_entry.get()
        self.socket.send(message.encode('utf-8'))
        self.update_chat_history("IS Admin: " + message + "\n")
        self.message_entry.delete(0, 'end ')

    def show_private_chat(self, message):
        # Create a new window for the private chat
        private_chat_window = tk.Toplevel(self.master)
        private_chat_window.title("Private Chat")

        chat_history = scrolledtext.ScrolledText(private_chat_window, state='disabled')
        chat_history.pack(fill='both', expand=True)

        message_entry = tk.Entry(private_chat_window)
        message_entry.pack(fill='x', padx=5, pady=5)

        send_button = tk.Button(private_chat_window, text="Send", command=lambda: self.send_private_message(private_chat_window, message_entry, chat_history))
        send_button.pack(pady=5)

        message_entry.bind("<Return>", lambda event: self.send_private_message(private_chat_window, message_entry, chat_history))

        # Display the private chat message
        chat_history.config(state='normal')
        chat_history.insert('end', message + "\n")
        chat_history.config(state='disabled')

        # Keep the pop-up window open
        private_chat_window.protocol("WM_DELETE_WINDOW", lambda: None)

    def send_private_message(self, private_chat_window, message_entry, chat_history):
        message = message_entry.get()
        self.socket.send(f"/private:{message_entry.get()}".encode('utf-8'))  # Send the private message
        chat_history.config(state='normal')
        chat_history.insert('end', "IS Admin: " + message + "\n")
        chat_history.config(state='disabled')
        message_entry.delete(0, 'end')

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