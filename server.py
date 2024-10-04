import socket
import threading
from datetime import datetime

clients = {}  # Store client sockets with their usernames and addresses

def handle_client(client_socket):
    addr = client_socket.getpeername()  # Get the client's address
    username = client_socket.recv(1024).decode('utf-8')  # Receive the username first
    clients[client_socket] = (username, addr)  # Store username and address
    broadcast(f"{username} has joined the chat", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message == "/users":
                    send_user_list(client_socket)  # Send user list on request
                else:
                    broadcast(message, client_socket)
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the client and notify others
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
    return f"{current_time} - {message}"

def send_user_list(client_socket):
    """Send the list of online users to the requesting client."""
    online_users = [f"{username} ({add_timestamp('')})" for username, _ in clients.values()]
    user_list_message = "Online Users:\n" + "\n".join(online_users)
    client_socket.send(("/users " + user_list_message).encode('utf-8'))

def remove(client_socket):
    if client_socket in clients:
        username, addr = clients.pop(client_socket)  # Get username and address
        # Notify other clients of the disconnection
        disconnection_message = f"{username} has left the chat"
        broadcast(disconnection_message, client_socket)
        print(f"{username} from {addr} has disconnected.")  # Log disconnection on the server

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 53214))
    server.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        clients[client_socket] = (None, addr)  # Temporarily store the address
        print(f"Connection from {addr} has been established!")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
