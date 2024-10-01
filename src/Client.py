
import tkinter

import SocketHandler
import InetMessage
import time

class Client(object):

    def __init__(self):
        self.serverhost = None
        self.serverport = None
        self.socket = None

    def connect(self, host, port):
        self.socket = SocketHandler.SocketHandler()

        try:
            self.socket.connect(host, port)
        except ConnectionRefusedError:
            self.socket = None
            return False

        self.serverhost = host
        self.serverport = port
        return True

    def disconnect(self):
        self.socket.close()
        self.socket = None

        self.serverhost = None
        self.serverport = None

    def is_connected(self):
        if self.socket is None:
            return False
        return self.socket.is_connected()

    def read(self):
        if self.is_connected() is False:
            return None
        return self.socket.read()

    def write(self, message):
        if self.is_connected() is False:
            return
        self.socket.write(0, message)



if __name__ == "__main__":
    client = Client()
    connected = client.connect("localhost", 45000)

    if connected is False:
        print("Could not connect to server!")
        exit(1)

    client.write("Hi")

    while True:

        time.sleep(0.1)

        if client.is_connected() == False:
            print("Disconnected from server")
            exit(0)

        inetMessage = client.read()
        if inetMessage is not None:
            code = inetMessage.get_code()
            message = inetMessage.get_message()
            if code == 0:
                message = message.decode("utf-8")
                print(message.replace("\n", ""))
