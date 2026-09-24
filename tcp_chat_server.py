import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = {}  # client_socket -> username


def broadcast(message):
    for client_socket in list(clients.keys()):
        try:
            client_socket.sendall((message + "\n").encode())
        except:
            remove_client(client_socket)


def remove_client(client_socket):
    username = clients.get(client_socket, "Unknown")

    if client_socket in clients:
        del clients[client_socket]

    try:
        client_socket.close()
    except:
        pass

    print(f"[LEAVE] {username} disconnected")
    broadcast(f"[SERVER] {username} left the chat.")


def handle_client(client_socket, address):
    try:
        username = client_socket.recv(1024).decode().strip()
        clients[client_socket] = username

        print(f"[JOIN] {username} joined from {address}")
        broadcast(f"[SERVER] {username} joined the chat.")

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode().strip()

            if message == "/quit":
                break

            print(f"[MESSAGE] {username}: {message}")
            broadcast(f"{username}: {message}")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        remove_client(client_socket)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("[STARTED] TCP chat server is running")
    print(f"[LISTENING] {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    start_server()