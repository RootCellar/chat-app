
from enum import Enum

class ConnectionState(Enum):
    INITIATED = 0
    ENCRYPT_CONNECTION = 1
    SEND_USERNAME = 2
    CHATTING = 3
