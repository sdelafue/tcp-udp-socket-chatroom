import socket
import os
import hashlib

HOST = "127.0.0.1"
PORT = 7000
FILES_FOLDER = "files"


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("[STARTED] TCP file server is running")
    print(f"[LISTENING] {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[CONNECTED] {address}")

        try:
            request = client_socket.recv(1024).decode().strip()

            parts = request.split("|")

            if len(parts) != 3 or parts[0] != "GET":
                client_socket.sendall("ERROR|Invalid request\n".encode())
                client_socket.close()
                continue

            filename = parts[1]
            chunk_size = int(parts[2])

            file_path = os.path.join(FILES_FOLDER, filename)

            if not os.path.exists(file_path):
                client_socket.sendall("ERROR|File not found\n".encode())
                client_socket.close()
                continue

            file_size = os.path.getsize(file_path)
            checksum = sha256_file(file_path)

            header = f"OK|{file_size}|{checksum}\n"
            client_socket.sendall(header.encode())

            with open(file_path, "rb") as f:
                while True:
                    data = f.read(chunk_size)

                    if not data:
                        break

                    client_socket.sendall(data)

            print(f"[SENT] {filename}, size={file_size} bytes")

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            client_socket.close()


if __name__ == "__main__":
    start_server()