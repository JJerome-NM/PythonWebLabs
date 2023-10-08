import os
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

ENCODING_TYPE = 'utf-8'
DECODE_TYPE = 'utf-8'


class Client(Thread):

    def __init__(self, server_path: str = "localhost", server_port: int = 20200, client_name: str = "User"):
        super().__init__(daemon=True)

        self.name = client_name

        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.connect((server_path, server_port))
        self.send_message(client_name)

        self._cashed_messages = list()

    def run(self):
        try:
            while True:
                response = self.accept_message()

                self._cashed_messages.append(response)
                self._show_messages()

        except (EOFError, ConnectionResetError, ConnectionRefusedError):
            print("Something went wrong")
        finally:
            self._socket.close()

    def _show_messages(self):
        os.system("cls")
        for message in self._cashed_messages:
            print(message)

    def accept_message(self) -> str:
        return self._socket.recv(1024).decode(DECODE_TYPE)

    def send_message(self, message: str):
        self._socket.send(message.encode(ENCODING_TYPE))


if __name__ == '__main__':
    name = input("Enter your name -> ")

    client = Client(client_name=name)
    client.start()

    while True:
        message = input("message -> ")
        client.send_message(message)
