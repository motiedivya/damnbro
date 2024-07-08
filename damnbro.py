import socket
import threading
import sys

def receive_messages(client_socket, running):
    while running[0]:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                running[0] = False
                print("Server closed the connection.")
        except Exception as e:
            print(f"Error receiving message: {e}")
            running[0] = False

def main():
    if len(sys.argv) != 3:
        print("Usage: python damnbro.py <SERVER_HOST> <SERVER_PORT>")
        return

    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(60)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print(f"Failed to connect to {SERVER_HOST}:{SERVER_PORT}")
        return

    running = [True]
    thread = threading.Thread(target=receive_messages, args=(client_socket, running))
    thread.start()

    try:
        while running[0]:
            message = input()
            if message.lower() == "quit":
                running[0] = False
            elif message:
                client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Interrupted.")
    finally:
        running[0] = False
        client_socket.close()
        thread.join()
        print("Connection closed.")

if __name__ == "__main__":
    main()
