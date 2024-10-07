
class User(object):
    def __init__(self, sockethandler, username = "Guest"):
        self.username = username
        self.sockethandler = sockethandler

    def is_connected(self):
        return self.sockethandler.is_connected()

    def send(self, code, message):
        if self.is_connected() == False:
            return
        self.sockethandler.write(code, message)

    def read(self):
        return self.sockethandler.read()