import socket
import time
import hashlib
import os
import base64

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
OUTPUT_FOLDER = "received_files"
TIMEOUT = 2.0


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

    output_path = os.path.join(OUTPUT_FOLDER, "udp_" + filename)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    request = f"GET|{filename}|{chunk_size}"
    client_socket.sendto(request.encode(), (SERVER_HOST, SERVER_PORT))

    try:
        data, _ = client_socket.recvfrom(4096)
    except socket.timeout:
        print("Timed out waiting for server metadata.")
        return

    metadata = data.decode().strip()
    parts = metadata.split("|")

    if parts[0] == "ERROR":
        print("Server error:", parts[1])
        return

    file_size = int(parts[1])
    original_checksum = parts[2]
    total_packets = int(parts[3])

    print(f"Receiving {filename} over UDP")
    print(f"File size: {file_size} bytes")
    print(f"Chunk size: {chunk_size} bytes")
    print(f"Total packets: {total_packets}")

    received_packets = {}
    retransmissions = 0
    start_time = time.time()

    while True:
        try:
            packet_data, server_address = client_socket.recvfrom(65535)
            packet = packet_data.decode().strip()

            if packet.startswith("DATA|"):
                parts = packet.split("|", 3)

                seq = int(parts[1])
                total = int(parts[2])
                payload_b64 = parts[3]

                payload = base64.b64decode(payload_b64.encode())

                received_packets[seq] = payload

                ack = f"ACK|{seq}"
                client_socket.sendto(ack.encode(), server_address)

                percent = (len(received_packets) / total_packets) * 100
                print(f"\rProgress: {percent:.2f}%", end="")

            elif packet.startswith("END|"):
                retransmissions = int(packet.split("|")[1])
                break

        except socket.timeout:
            print("\nTimed out waiting for UDP packets.")
            break

    end_time = time.time()
    client_socket.close()

    if len(received_packets) != total_packets:
        print()
        print("Transfer incomplete.")
        print(f"Received {len(received_packets)} of {total_packets} packets.")
        return

    with open(output_path, "wb") as f:
        for seq in range(total_packets):
            f.write(received_packets[seq])

    total_time = end_time - start_time
    throughput_kbps = (file_size / 1024) / total_time

    received_checksum = sha256_file(output_path)
    checksum_match = original_checksum == received_checksum

    print()
    print("UDP transfer complete.")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Throughput: {throughput_kbps:.2f} KB/s")
    print(f"UDP retransmissions: {retransmissions}")
    print(f"Checksum match: {'Yes' if checksum_match else 'No'}")


if __name__ == "__main__":
    filename = input("Enter filename: ")
    chunk_size = int(input("Enter chunk size, example 1024, 4096, 16384: "))

    receive_file(filename, chunk_size)