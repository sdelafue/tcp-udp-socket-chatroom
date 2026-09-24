import socket
import threading
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000

TIMEOUT = 0.5
MAX_RETRIES = 5

username = input("Choose a username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

acks_received = set()
seq_number = 0
retransmissions = 0


def register():
    while True:
        try:
            client_socket.sendto(
                f"REGISTER|{username}".encode(),
                (SERVER_HOST, SERVER_PORT)
            )

            data, _ = client_socket.recvfrom(4096)

            if data.decode().strip() == "REGISTERED":
                print("Registered with UDP server.")
                break

        except socket.timeout:
            print("Retrying registration...")


def receive_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)
            message = data.decode().strip()

            if message.startswith("ACK|"):
                seq = int(message.split("|")[1])
                acks_received.add(seq)
            else:
                print(message)

        except socket.timeout:
            continue

        except:
            break


def send_reliable_message(text):
    global seq_number, retransmissions

    current_seq = seq_number
    seq_number += 1

    packet = f"DATA|{current_seq}|{username}|{text}"

    start_time = time.time()
    attempts = 0

    while attempts < MAX_RETRIES:
        client_socket.sendto(packet.encode(), (SERVER_HOST, SERVER_PORT))

        wait_start = time.time()

        while time.time() - wait_start < TIMEOUT:
            if current_seq in acks_received:
                latency_ms = (time.time() - start_time) * 1000
                print(f"[DELIVERED] seq={current_seq}, latency={latency_ms:.2f} ms")
                return True

            time.sleep(0.01)

        attempts += 1
        retransmissions += 1
        print(f"[RETRANSMIT] seq={current_seq}, attempt={attempts}")

    print(f"[FAILED] Message seq={current_seq} was not acknowledged.")
    return False


def send_messages():
    while True:
        message = input("")

        if message == "/quit":
            print(f"Total UDP retransmissions: {retransmissions}")
            client_socket.close()
            break

        send_reliable_message(message)


register()

receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

send_messages()