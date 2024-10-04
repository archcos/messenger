import socket
import threading
from datetime import datetime

clients = {}  # Store client sockets with their usernames and addresses
admin_socket = None  # To hold the admin socket

def handle_client(client_socket):
    global admin_socket  # Declare it as global at the top of the function
    addr = client_socket.getpeername()  # Get the client's address
    username = client_socket.recv(1024).decode('utf-8')  # Receive the username first

    if username == "IS Admin":
        if admin_socket is not None:
            client_socket.send("Admin is already connected. Please try again later.".encode('utf-8'))
            client_socket.close()
            return
        admin_socket = client_socket  # Assign the socket to the admin
        clients[client_socket] = (username, addr)  # Store admin's username and address
        broadcast(f"{username} has joined the chat", client_socket)
        print("Admin has connected.")
    else:
        clients[client_socket] = (username, addr)  # Store username and address for other clients
        broadcast(f"{username} has joined the chat", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message == "/users":
                    send_user_list(client_socket)  # Send user list on request
                elif message.startswith("/ismsg"):
                    if admin_socket:
                        admin_socket.send(f"Message from {username}: {message[6:]}".encode('utf-8'))  # Send the message content without the command
                        # Send the message to the user who initiated the private chat
                        for client in clients.keys():
                            if clients[client][0] == message[6:].split(":")[0]:
                                client.send(f"Message from IS Admin: {message[6:]}".encode('utf-8'))
                elif message.startswith("/private"):
                    # Handle private messages
                    recipient = message.split(":")[1]
                    for client in clients.keys():
                        if clients[client][0] == recipient:
                            client.send(f"Private message from {username}: {message.split(":")[2]}".encode('utf-8'))
                else:
                    broadcast(message, client_socket)
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    remove(client_socket)

def broadcast(message, client_socket):
    timestamped_message = add_timestamp(message)
    for client in clients.keys():
        if client != client_socket:
            try:
                client.send(timestamped_message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                remove(client)

def add_timestamp(message):
    """Add a timestamp to the message."""
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"{current_time} {message}"

def send_user_list(client_socket):
    """Send the list of online users to the requesting client."""
    online_users = [f"{username}" for username, _ in clients.values()]
    user_list_message = "Online Users:\n" + "\n".join(online_users)
    client_socket.send(("/users " + user_list_message).encode('utf-8'))

def remove(client_socket):
    global admin_socket  # Declare it as global here
    if client_socket in clients:
        username, addr = clients.pop(client_socket)  # Get username and address
        disconnection_message = f"{username} has left the chat"
        broadcast(disconnection_message, client_socket)
        print(f"{username} from {addr} has disconnected.")  # Log disconnection on the server
        if client_socket == admin_socket:
            print("Admin has disconnected.")
            admin_socket = None  # Clear the admin socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 53214))
    server.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} has been established!")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()