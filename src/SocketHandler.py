
import socket
import time

import Debug

class SocketHandler(object):

    def __init__(self, socket = None, host = None, port = None):
        self.host = None
        self.port = None

        self.socket = None
        self.connected = False

        if socket != None:
            self.socket = socket
            self.connected = True
            self.host = host
            self.port = port

    def connect(self, host, port):
        self.host = host
        self.port = port

        Debug.debug("Connecting to " + str(self.host) + ":" + str(self.port) + "...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)

    def close(self):
        Debug.debug("Closing connection to " + str(self.host) + ":" + str(self.port) + "...")
        try:
            self.socket.shutdown(1)
            self.socket.close()
        except OSError:
            pass

    def read(self):
        try:
            return self.socket.recv(512).decode("utf-8")
        except BlockingIOError:
            return None

    def write(self, message):
        try:
            self.socket.send(message.encode("utf-8"))
        except OSError:
            self.close()

if __name__ == "__main__":
    sock = SocketHandler()
    sock.connect("localhost", 45000)
    message = sock.read()
    while message is None:
        message = sock.read()
        time.sleep(0.1)
    print(message)
    sock.close()

