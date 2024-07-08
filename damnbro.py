#!/home/neural/DivyeshVishwakarma/damnbro/.venv/bin/python3
import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Error receiving message.")
            break

def main():
    if len(sys.argv) != 3:
        print("Usage: python damnbro.py <SERVER_HOST> <SERVER_PORT>")
        return

    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print(f"Failed to connect to {SERVER_HOST}:{SERVER_PORT}")
        return

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
