#!/bin/python3

import time
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.server import ChatServer

port = 45000
if len(sys.argv) == 2:
    port = int(sys.argv[1])
server = ChatServer(port)
while True:
    time.sleep(0.1)
    server.handle_messages()
    new_client = server.accept_client()
