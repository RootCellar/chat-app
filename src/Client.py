
import SocketHandler
import time

if __name__ == "__main__":
    sock = SocketHandler.SocketHandler()
    sock.connect("localhost", 45000)

    sock.write("Hi")

    while True:

        time.sleep(0.1)

        if sock.is_connected() == False:
            print("Disconnected from server")
            exit(0)

        message = sock.read()
        if message is not None:
            print(message)
