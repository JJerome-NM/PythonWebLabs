from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

SERVER_PATCH = "localhost"
SERVER_PORT = 20200


server = socket(AF_INET, SOCK_STREAM)
server.bind((SERVER_PATCH, SERVER_PORT))
server.listen(5)

while True:
    client, addr = server.accept()

    name: str = client.recv(1024).decode('utf-8')
    connected_message = f"{name} -> Connected"

    print(connected_message)

    while True:
        try:
            message: str = client.recv(1024).decode('utf-8')
        except (ConnectionAbortedError, ConnectionResetError):
            print(f"{name} -> Disconnected")
            client.close()
            break

        if message == "EXIT":
            client.send("EXIT".encode('utf-8'))
            print(f"{name} -> Disconnected")
            client.close()
            break

        message_with_time: str = f"{str(datetime.now())} {name} -> {message}"
        print(message_with_time)

        checksum: int = client.send(message_with_time.encode('utf-8'))

        if len(message_with_time.encode('utf-8')) != checksum:
            print("Checksum is incorrect")

            client.send("Something when wrong".encode('utf-8'))
