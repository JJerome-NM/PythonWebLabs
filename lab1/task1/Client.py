from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

SERVER_PATCH = "localhost"
SERVER_PORT = 20200


client = socket(AF_INET, SOCK_STREAM)
client.connect((SERVER_PATCH, SERVER_PORT))

name: str = input("Enter your name -> ")

client.send(name.encode('utf-8'))

try:
    message: str = input("Enter message -> ")

    print(f"{str(datetime.now())} Your message -> {message}")

    client.send(message.encode('utf-8'))

    response = client.recv(1024).decode('utf-8')
    print(response)

except ConnectionResetError:
    print("Помилка: З'єднання з сервером втрачено.")
    exit()
