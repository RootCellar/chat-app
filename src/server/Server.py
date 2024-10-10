import sys

from ..lib import SocketHandler
from ..lib import ServerSocket
from ..lib.Debug import debug

from ..lib.MessageType import MessageType
from ..lib.ConnectionState import ConnectionState

from . import User

import time

class ChatServer(object):

    def __init__(self, port=45000):
        self.port = port
        self.serv = ServerSocket.ServerSocket()
        self.serv.listen(port)
        self.clients = []

    def log(self, output):
        debug("[SERVER] " + output)

    def accept_client(self):
        socket = self.serv.accept()
        if socket is not None:
            client = User.User(socket)
            self.change_state(client, ConnectionState.SEND_USERNAME)
            self.clients.append(client)
        return socket

    def change_state(self, client, state):
        client.state = state
        client.send(MessageType.CONN_STATE.value, state.value)
        self.log("Client state change to " + str(state.value))

    def handle_messages(self):
        for client in self.clients:
            if client.is_connected() is False:
                self.clients.remove(client)
                if client.state == ConnectionState.CHATTING:
                    self.broadcast_message(client.username + " left the chat")
                continue

            inetMessage = client.read()
            if inetMessage is not None:
                if inetMessage.get_code() == MessageType.CHAT_MESSAGE.value:
                    if client.state == ConnectionState.CHATTING:
                        message = inetMessage.get_message().decode("utf-8")
                        message = message.replace("\n", "")
                        self.broadcast_message(client.username + ": " + message)
                elif inetMessage.get_code() == MessageType.USERNAME.value:
                    message = inetMessage.get_message().decode("utf-8")
                    self.log("Client name change to " + message)
                    client.username = message
                    if client.state == ConnectionState.SEND_USERNAME:
                        self.change_state(client, ConnectionState.CHATTING)
                        self.broadcast_message(client.username + " has joined the chat")

    def broadcast_message(self, message):
        self.log("Broadcast: " + message)
        for client in self.clients:
            if client.state == ConnectionState.CHATTING:
                client.send(MessageType.CHAT_MESSAGE.value, message + "\n")



if __name__ == "__main__":
    port = 45000
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    server = ChatServer(port)
    while True:
        time.sleep(0.1)
        server.handle_messages()
        new_client = server.accept_client()

        #if new_client is not None:
