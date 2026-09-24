import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                break

            print(data.decode().strip())

        except:
            break


def send_messages(client_socket):
    while True:
        message = input("")

        try:
            client_socket.sendall(message.encode())

            if message == "/quit":
                print("You left the chat.")
                client_socket.close()
                break

        except:
            break


username = input("Choose a username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.sendall(username.encode())

receive_thread = threading.Thread(
    target=receive_messages,
    args=(client_socket,),
    daemon=True
)
receive_thread.start()

send_messages(client_socket)