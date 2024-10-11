
from enum import Enum

def message_len(bytes):
    if type(bytes) is not bytes:
        raise RuntimeError

    if len(bytes) < 4:
        return -1

    len = int.from_bytes(bytes[0:4], byteorder='big')
    return len

def message_from_bytes(data):
    if type(data) is not bytes:
        raise RuntimeError

    if len(data) < 8:
        return None

    length = int.from_bytes(data[0:4], byteorder='big')
    code = int.from_bytes(data[4:8], byteorder='big')

    if length < 1 or code < 0:
        return InetMessage(8, -1, b'')

    message = data[8:(8 + length)]

    if len(message) < length:
        return None

    message = InetMessage(length + 8, code, message)
    return message

def message_to_bytes(code, data):
    if type(data) is str:
        message_bytes = data.encode("utf-8")
    elif type(data) is int:
        message_bytes = int.to_bytes(data, length=4, byteorder='big')
    else:
        raise NotImplementedError

    msgLen = len(message_bytes)
    message_bytes = int.to_bytes(msgLen, length=4, byteorder='big') + int.to_bytes(code, length=4, byteorder='big') + message_bytes

    return message_bytes

class InetMessage(object):
    def __init__(self, length, code, message):
        self.length = length
        self.code = code
        self.message_bytes = message
        self.msgLen = len(message)

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message_bytes

    def get_len(self):
        return self.length