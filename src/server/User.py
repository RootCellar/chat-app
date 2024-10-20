
import nacl.utils
from nacl.public import PrivateKey, Box

from ..lib import InetMessage
from ..lib.MessageType import MessageType
from ..lib.ConnectionState import ConnectionState

class User(object):
    def __init__(self, sockethandler, username = "Guest"):
        self.username = username
        self.sockethandler = sockethandler
        self.state = ConnectionState.INITIATED
        self.enc_box = None

    def is_connected(self):
        return self.sockethandler.is_connected()

    def disconnect(self):
        self.sockethandler.close()

    def encrypt(self, public_key):
        self.private_key = PrivateKey.generate()
        self.send(MessageType.PUBLIC_KEY.value, self.private_key.public_key.encode())
        self.enc_box = Box(self.private_key, public_key)
        self.connection_encrypted = True

    def send(self, code, message):
        if self.is_connected() == False:
            return
        if self.enc_box is not None:
            message = bytes(self.enc_box.encrypt(InetMessage.encode_as_bytes(message)))
        self.sockethandler.write(code, message)

    def read(self):
        message = self.sockethandler.read()
        if message is not None and self.enc_box is not None:
            message_bytes = self.enc_box.decrypt(message.get_message())
            message.message_bytes = message_bytes
        return message