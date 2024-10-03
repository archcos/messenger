import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, chat_history):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_history.config(state='normal')
            chat_history.insert(tk.END, f"{message}\n")
            chat_history.config(state='disabled')
            chat_history.see(tk.END)
        except:
            print("An error occurred!")
            client_socket.close()
            break

def send_message(client_socket, message_entry):
    message = message_entry.get()
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.50.219', 12345))  # Replace with the server's IP address

    # Create the chat window
    chat_window = tk.Tk()
    chat_window.title("Chat")

    chat_history = scrolledtext.ScrolledText(chat_window, state='disabled')
    chat_history.pack(fill='both', expand=True)

    message_entry = tk.Entry(chat_window)
    message_entry.pack(fill='x')

    send_button = tk.Button(chat_window, text="Send", command=lambda: send_message(client_socket, message_entry))
    send_button.pack()

    threading.Thread(target=receive_messages, args=(client_socket, chat_history)).start()

    chat_window.mainloop()

if __name__ == "__main__":
    start_client()
