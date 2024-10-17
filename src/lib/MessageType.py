
from enum import Enum

class MessageType(Enum):
    CHAT_MESSAGE = 0
    USERNAME = 1
    CONN_STATE = 2
    PUBLIC_KEY = 3

def message_type_from_code(code):
    for i in list(MessageType):
        if i.value == code:
            return i
    return None