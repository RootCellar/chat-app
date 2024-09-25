
import socket
import time

import Debug
import SocketHandler

class ServerSocket(object):

    def __init__(self):
        self.port = None
        self.server_socket = None

    def listen(self, port):
        self.server_socket = socket.socket()
        self.server_socket.bind(('', port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        Debug.debug("Listening on port " + str(port))

    def accept(self):
        try:
            socket, (host, port) = self.server_socket.accept()
        except BlockingIOError:
            return None
        Debug.debug("Received connection from " + str(host) + ":" + str(port))
        return SocketHandler.SocketHandler(socket, host, port)

if __name__ == "__main__":
    serv = ServerSocket()
    serv.listen(45000)
    socket = serv.accept()
    while True:
        while socket is None:
            socket = serv.accept()
            time.sleep(0.1)
        socket.write("Hello from server!")
        socket.close()
        socket = None
