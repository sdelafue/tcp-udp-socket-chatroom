import socket
import os
import math
import hashlib
import base64

HOST = "127.0.0.1"
PORT = 8000
FILES_FOLDER = "files"
TIMEOUT = 0.5
MAX_RETRIES = 10


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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    server_socket.settimeout(TIMEOUT)

    print("[STARTED] UDP file server is running")
    print(f"[LISTENING] {HOST}:{PORT}")

    while True:
        try:
            data, client_address = server_socket.recvfrom(4096)
            request = data.decode().strip()

            parts = request.split("|")

            if len(parts) != 3 or parts[0] != "GET":
                continue

            filename = parts[1]
            chunk_size = int(parts[2])

            file_path = os.path.join(FILES_FOLDER, filename)

            if not os.path.exists(file_path):
                server_socket.sendto("ERROR|File not found".encode(), client_address)
                continue

            file_size = os.path.getsize(file_path)
            checksum = sha256_file(file_path)
            total_packets = math.ceil(file_size / chunk_size)

            metadata = f"META|{file_size}|{checksum}|{total_packets}"
            server_socket.sendto(metadata.encode(), client_address)

            print(f"[REQUEST] {filename} from {client_address}")
            print(f"[INFO] size={file_size}, chunk={chunk_size}, packets={total_packets}")

            retransmissions = 0

            with open(file_path, "rb") as f:
                for seq in range(total_packets):
                    payload = f.read(chunk_size)
                    payload_b64 = base64.b64encode(payload).decode()

                    packet = f"DATA|{seq}|{total_packets}|{payload_b64}"

                    acknowledged = False
                    attempts = 0

                    while not acknowledged and attempts < MAX_RETRIES:
                        server_socket.sendto(packet.encode(), client_address)

                        try:
                            ack_data, _ = server_socket.recvfrom(4096)
                            ack = ack_data.decode().strip()

                            if ack == f"ACK|{seq}":
                                acknowledged = True

                        except socket.timeout:
                            attempts += 1
                            retransmissions += 1
                            print(f"[RETRANSMIT] seq={seq}, attempt={attempts}")

                    if not acknowledged:
                        print(f"[FAILED] Packet {seq} was not acknowledged.")
                        break

            end_packet = f"END|{retransmissions}"
            server_socket.sendto(end_packet.encode(), client_address)

            print(f"[DONE] {filename}, retransmissions={retransmissions}")

        except socket.timeout:
            continue


if __name__ == "__main__":
    start_server()