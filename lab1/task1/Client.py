from socket import socket, AF_INET, SOCK_STREAM

SERVER_PATCH = "localhost"
SERVER_PORT = 20200


client = socket(AF_INET, SOCK_STREAM)
client.connect((SERVER_PATCH, SERVER_PORT))

name: str = input("Enter your name -> ")

client.send(name.encode('utf-8'))

try:
    while True:
        message: str = input("Enter message -> ")
        client.send(message.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')

        if response == "EXIT":
            print("Connection closed")
            client.close()
            exit()

        print(response)

except (ConnectionResetError, ConnectionRefusedError):
    print("Помилка: З'єднання з сервером втрачено.")
    exit()
