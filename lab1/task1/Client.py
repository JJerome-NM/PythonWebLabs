import socket


SERVER_PATCH = "localhost"
SERVER_PORT = 20200


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_PATCH, SERVER_PORT))

name: str = input("Enter your name -> ")

client.send(name.encode('utf-8'))

while True:
    message: str = input("Enter message -> ")
    client.send(message.encode('utf-8'))

    message: str = client.recv(1024).decode('utf-8')

    print(message)
