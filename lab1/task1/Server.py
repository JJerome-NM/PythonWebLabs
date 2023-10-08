from datetime import datetime
import socket

SERVER_PATCH = "localhost"
SERVER_PORT = 20200


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_PATCH, SERVER_PORT))
server.listen(5)


client, addr = server.accept()

name: str = client.recv(1024).decode('utf-8')
connectedMessage = " -> " + name + " connected"

print(connectedMessage)


while True:
    message: str = client.recv(1024).decode('utf-8')
    messageWithTime: str = str(datetime.now()) + " -> " + message

    print(messageWithTime)

    client.send(messageWithTime.encode('utf-8'))

