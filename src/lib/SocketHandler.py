
import socket
import time

from . import Debug
from . import InetMessage

class SocketHandler(object):

    def __init__(self, socket = None, host = None, port = None):
        self.host = None
        self.port = None

        self.socket = None
        self.buffer = b''
        self.connected = False

        if socket != None:
            self.socket = socket
            self.socket.setblocking(0)
            self.connected = True
            self.host = host
            self.port = port

    def log(self, output):
        Debug.debug("[SOCKET HANDLER]" + output)

    def connect(self, host, port):
        self.host = host
        self.port = port

        self.log("Connecting to " + str(self.host) + ":" + str(self.port) + "...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)
        self.connected = True

    def is_connected(self):
        return self.connected

    def close(self):
        self.log("Closing connection to " + str(self.host) + ":" + str(self.port) + "...")
        self.connected = False
        self.host = None
        self.port = None

        try:
            self.socket.shutdown(1)
            self.socket.close()
        except OSError:
            pass

        self.socket = None

    def read(self):
        if self.socket is None:
            return None
        try:
            message = self.socket.recv(512)
            if len(message) < 1:
                self.close()
                return None
            elif message is not None:
                self.buffer = self.buffer + message
        except BlockingIOError:
            pass
        except OSError:
            self.close()

        if len(self.buffer) > 16384:
            self.log("Read buffer overflow")
            self.close()

        inetMessage = InetMessage.message_from_bytes(self.buffer)
        if inetMessage is not None:
            self.buffer = self.buffer[inetMessage.get_len():]
            return inetMessage
        return None

    def write(self, code, message):
        if self.socket is None:
            return
        try:
            self.socket.send(InetMessage.message_to_bytes(code, message))
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

