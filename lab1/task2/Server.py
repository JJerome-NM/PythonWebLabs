from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


ENCODING_TYPE = 'utf-8'
DECODE_TYPE = 'utf-8'


class Client:

    def __init__(self, client_socket: socket, client_addr, client_name: str, disconnect_me_func):
        self._socket = client_socket
        self._addr = client_addr
        self.name = client_name
        self._disconnect_me_func = disconnect_me_func

    def accept_message(self) -> str:
        return self._socket.recv(1024).decode(DECODE_TYPE)

    def send_message(self, message: str):
        self._socket.send(message.encode(ENCODING_TYPE))

    def build_message_with_time_and_name(self, message: str):
        return f"{datetime.now().strftime('%H:%M:%S')} - {self.name} _> {message}"

    def close_connection(self):
        self._disconnect_me_func(self)
        self._socket.close()


class OutgoingMessageHandler:

    clients = list[Client]()

    @staticmethod
    def send_message(client: Client, message: str):
        if client in OutgoingMessageHandler.clients:
            client.send_message(message)

    @staticmethod
    def send_broadcast_message(message: str):
        for client in OutgoingMessageHandler.clients:
            OutgoingMessageHandler.send_message(client, message)


class IncomingMessageHandler(Thread):

    def __init__(self, client: Client):
        super().__init__(daemon=True)

        self._client = client

        super().start()

    def run(self):
        try:
            while True:
                message = self._client.accept_message()
                message = self._client.build_message_with_time_and_name(message)

                print(message)

                OutgoingMessageHandler.send_broadcast_message(message)
        except (ConnectionResetError, ):
            self._client.close_connection()


class Server(Thread):

    def __init__(self, path: str = "localhost", port: int = 20200):
        super().__init__(daemon=True)

        self._server = socket(AF_INET, SOCK_STREAM)
        self._server.bind((path, port))
        self._server.listen(5)

        self._clients = list()
        self._incomingHandlers = dict[Client, IncomingMessageHandler]()

        OutgoingMessageHandler.clients = self._clients

        super().start()

    def run(self):                              # Accept connection
        while True:
            socket_connection, addr = self._server.accept()

            name = socket_connection.recv(1024).decode(ENCODING_TYPE)
            client = Client(socket_connection, addr, name, disconnect_me_func=self.disconnect_client)

            self._add_client(client)
            self._incomingHandlers.pop(client, IncomingMessageHandler(client))

            connect_message = client.build_message_with_time_and_name("Connected")

            OutgoingMessageHandler.send_broadcast_message(connect_message)
            print(connect_message)

    def _add_client(self, client: Client):
        self._clients.append(client)

    def disconnect_client(self, client: Client):
        self._clients.remove(client)
        disconnect_message = client.build_message_with_time_and_name("Disconnected")

        OutgoingMessageHandler.send_broadcast_message(disconnect_message)
        print(disconnect_message)


if __name__ == '__main__':
    server = Server().join()
