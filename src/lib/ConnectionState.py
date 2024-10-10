
from enum import Enum

class ConnectionState(Enum):
    INITIATED = 0
    SEND_USERNAME = 1
    CHATTING = 2
