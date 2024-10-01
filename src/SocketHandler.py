
import socket
import time

import Debug
import InetMessage

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

    def connect(self, host, port):
        self.host = host
        self.port = port

        Debug.debug("Connecting to " + str(self.host) + ":" + str(self.port) + "...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)
        self.connected = True

    def is_connected(self):
        return self.connected

    def close(self):
        Debug.debug("Closing connection to " + str(self.host) + ":" + str(self.port) + "...")
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
                inetMessage = InetMessage.message_from_bytes(self.buffer)
                if inetMessage is not None:
                    self.buffer = self.buffer[inetMessage.get_len():]
                    return inetMessage
        except BlockingIOError:
            return None
        except OSError:
            self.close()
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

