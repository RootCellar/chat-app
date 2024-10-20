
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

from ..lib import SocketHandler
from ..lib import InetMessage
from ..lib.Debug import debug

import time

from ..lib.MessageType import MessageType, message_type_from_code
from ..lib.ConnectionState import ConnectionState, connection_state_from_code

class Client(object):

    def __init__(self):
        self.reset()

    def log(self, output):
        debug("[CLIENT] " + output)

    def reset(self):
        self.socket = None
        self.serverhost = None
        self.serverport = None
        self.state = None
        self.server_state = None
        self.enc_box = None
        self.private_key = None
        self.connection_encrypted = False

    def set_username(self, username):
        self.username = username

    def connect(self, host, port):
        self.reset()
        self.socket = SocketHandler.SocketHandler()

        try:
            self.socket.connect(host, port)
        except ConnectionRefusedError:
            self.socket = None
            return False

        self.serverhost = host
        self.serverport = port
        self.state = ConnectionState.INITIATED
        return True

    def disconnect(self):
        self.socket.close()
        self.reset()

    def is_connected(self):
        if self.socket is None:
            return False
        return self.socket.is_connected()

    def read(self):
        if self.is_connected() is False:
            return None
        if self.socket.is_connected() is False:
            self.disconnect()
            return None

        message = self.read_message()

        if message is None:
            return None

        self.log("Received " + message_type_from_code(message.get_code()).name + " message")
        if message.get_code() == MessageType.CHAT_MESSAGE.value:
            return message
        elif message.get_code() == MessageType.PUBLIC_KEY.value:
            if self.connection_encrypted is True:
                self.enc_box = Box(self.private_key, PublicKey(message.get_message()))
        elif message.get_code() == MessageType.CONN_STATE.value:
            data = message.get_message()
            if len(data) != 4:
                # Protocol error
                self.log("Server sent wrong number of bytes for CONN_STATE")
                self.disconnect()
                return None
            self.server_state = int.from_bytes(data, byteorder='big')
            self.log("CONN_STATE: " + connection_state_from_code(self.server_state).name)

            if self.server_state == ConnectionState.SEND_USERNAME.value:
                self.log("Server needs username. Sending username to server...")
                self.write(MessageType.USERNAME.value, self.username)
            elif self.server_state == ConnectionState.ENCRYPT_CONNECTION.value:
                self.log("Encrypting connection...")
                self.private_key = PrivateKey.generate()
                self.write(MessageType.PUBLIC_KEY.value, self.private_key.public_key.encode())
                self.connection_encrypted = True

        return None

    def chat(self, message):
        if self.is_connected() is False:
            return
        self.write(MessageType.CHAT_MESSAGE.value, message)

    def write(self, code, message):
        if self.is_connected() is False:
            return
        if self.enc_box is not None:
            message = bytes(self.enc_box.encrypt(InetMessage.encode_as_bytes(message)))
        self.socket.write(code, message)

    def read_message(self):
        message = self.socket.read()
        if message is not None and self.enc_box is not None:
            message_bytes = self.enc_box.decrypt(message.get_message())
            message.message_bytes = message_bytes
        return message

if __name__ == "__main__":
    client = Client()
    connected = client.connect("localhost", 45000)

    if connected is False:
        print("Could not connect to server!")
        exit(1)

    client.chat("Hi")

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
