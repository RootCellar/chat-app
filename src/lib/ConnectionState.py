
from enum import Enum

class ConnectionState(Enum):
    INITIATED = 0
    ENCRYPT_CONNECTION = 1
    SEND_USERNAME = 2
    CHATTING = 3

def connection_state_from_code(code):
    for i in list(ConnectionState):
        if i.value == code:
            return i
    return None