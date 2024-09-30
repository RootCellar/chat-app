

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