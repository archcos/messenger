import socket
import threading

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client_socket)
            else:
                remove(client_socket)
                break
        except:
            remove(client_socket)
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Connection from {addr} has been established!")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
