#!/home/neural/DivyeshVishwakarma/damnbro/.venv/bin/python3
import socket
import threading
import random
import os

# Server settings
HOST = os.getenv('RENDER_EXTERNAL_HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8086))

# List to keep track of connected clients and their names
clients = []
client_names = {}

# List of random names
names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Niaj", "Olivia", "Peggy", "Rupert", "Sybil", "Trent", "Victor", "Walter"]

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                client.close()
                try:
                    clients.remove(client)
                except ValueError:
                    pass

def handle_client(client_socket):
    name = random.choice(names)
    client_names[client_socket] = name
    welcome_message = f"{name} has joined the chat!"
    print(welcome_message)
    broadcast(welcome_message.encode('utf-8'), client_socket)
    # Send the client their name
    try:
        client_socket.send(f"Your name is {name}".encode('utf-8'))
    except BrokenPipeError as e:
        print(f"Error sending name to client: {e}")
        return

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                full_message = f"{name}: {message.decode('utf-8')}"
                print(full_message)
                broadcast(full_message.encode('utf-8'), client_socket)
            else:
                client_socket.close()
                if client_socket in clients:
                    clients.remove(client_socket)
                leave_message = f"{name} has left the chat."
                print(leave_message)
                broadcast(leave_message.encode('utf-8'), client_socket)
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.close()
            if client_socket in clients:
                clients.remove(client_socket)
            leave_message = f"{name} has left the chat."
            print(leave_message)
            broadcast(leave_message.encode('utf-8'), client_socket)
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started on {HOST}:{PORT}")
    except Exception as e:
        print(f"Error starting server: {e}")
        return

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Connection from {addr}")
            clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()
