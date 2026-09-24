import socket

HOST = "127.0.0.1"
PORT = 6000

clients = {}  # username -> address


def broadcast(server_socket, message):
    for username, address in clients.items():
        server_socket.sendto(message.encode(), address)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print("[STARTED] UDP chat server is running")
    print(f"[LISTENING] from: {HOST} on port: {PORT}")

    while True:
        data, address = server_socket.recvfrom(4096)
        message = data.decode().strip()

        if message.startswith("REGISTER|"):
            username = message.split("|")[1]
            clients[username] = address

            print(f"[REGISTER] {username} from {address}")
            server_socket.sendto("REGISTERED".encode(), address)
            broadcast(server_socket, f"[SERVER] {username} joined the UDP chat.")

        elif message.startswith("DATA|"):
            parts = message.split("|", 3)

            if len(parts) < 4:
                continue

            seq = parts[1]
            username = parts[2]
            text = parts[3]

            ack = f"ACK|{seq}"
            server_socket.sendto(ack.encode(), address)

            print(f"[MESSAGE] seq={seq} {username}: {text}")

            broadcast(server_socket, f"{username}: {text}")


if __name__ == "__main__":
    start_server()