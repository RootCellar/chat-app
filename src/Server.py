
import SocketHandler
import ServerSocket

import time

class ChatServer(object):

    def __init__(self, port=45000):
        self.port = port
        self.serv = ServerSocket.ServerSocket()
        self.serv.listen(45000)
        self.clients = []

    def accept_client(self):
        socket = self.serv.accept()
        if socket is not None:
            self.clients.append(socket)
        return socket

    def handle_messages(self):
        for client in self.clients:
            if client.is_connected() is False:
                self.broadcast_message("Client Disconnected")
                self.clients.remove(client)
                continue

            message = client.read()
            if message is not None:
                self.broadcast_message("Client: " + message)

    def broadcast_message(self, message):
        for client in self.clients:
            client.write(message)

if __name__ == "__main__":
    server = ChatServer()
    while True:
        time.sleep(0.1)
        server.handle_messages()
        new_client = server.accept_client()
        if new_client is not None:
            server.broadcast_message("Accepted a new client!")
