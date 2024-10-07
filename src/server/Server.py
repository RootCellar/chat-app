from ..lib import SocketHandler
from ..lib import ServerSocket

from . import User

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
            client = User.User(socket)
            self.clients.append(client)
        return socket

    def handle_messages(self):
        for client in self.clients:
            if client.is_connected() is False:
                self.broadcast_message("Client Disconnected")
                self.clients.remove(client)
                continue

            inetMessage = client.read()
            if inetMessage is not None:
                if inetMessage.get_code() == 0:
                    message = inetMessage.get_message().decode("utf-8")
                    message = message.replace("\n", "")
                    self.broadcast_message(client.username + ": " + message)
                elif inetMessage.get_code() == 1:
                    message = inetMessage.get_message().decode("utf-8")
                    print("Client name change to " + message)
                    client.username = message

    def broadcast_message(self, message):
        print("Broadcast: " + message)
        for client in self.clients:
            client.send(0, message + "\n")



if __name__ == "__main__":
    server = ChatServer()
    while True:
        time.sleep(0.1)
        server.handle_messages()
        new_client = server.accept_client()
        if new_client is not None:
            server.broadcast_message("Accepted a new client!")
