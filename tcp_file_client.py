import socket
import time
import hashlib
import os

HOST = "127.0.0.1"
PORT = 7000
OUTPUT_FOLDER = "received_files"


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def receive_file(filename, chunk_size):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_path = os.path.join(OUTPUT_FOLDER, "tcp_" + filename)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    request = f"GET|{filename}|{chunk_size}\n"
    client_socket.sendall(request.encode())

    header = b""

    while not header.endswith(b"\n"):
        header += client_socket.recv(1)

    header_text = header.decode().strip()
    parts = header_text.split("|")

    if parts[0] == "ERROR":
        print("Server error:", parts[1])
        client_socket.close()
        return

    file_size = int(parts[1])
    original_checksum = parts[2]

    print(f"Receiving {filename}")
    print(f"File size: {file_size} bytes")
    print(f"Chunk size: {chunk_size} bytes")

    bytes_received = 0
    start_time = time.time()

    with open(output_path, "wb") as f:
        while bytes_received < file_size:
            data = client_socket.recv(chunk_size)

            if not data:
                break

            f.write(data)
            bytes_received += len(data)

            percent = (bytes_received / file_size) * 100
            print(f"\rProgress: {percent:.2f}%", end="")

    end_time = time.time()
    client_socket.close()

    total_time = end_time - start_time
    throughput_kbps = (file_size / 1024) / total_time

    received_checksum = sha256_file(output_path)
    checksum_match = original_checksum == received_checksum

    print()
    print("Transfer complete.")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Throughput: {throughput_kbps:.2f} KB/s")
    print(f"Checksum match: {'Yes' if checksum_match else 'No'}")


if __name__ == "__main__":
    filename = input("Enter filename: ")
    chunk_size = int(input("Enter chunk size, example 1024, 4096, 16384: "))

    receive_file(filename, chunk_size)