import socket

from constants import Constants


class Client:
    # player info

    server = "192.168.1.41" # paste the IP of the server here
    connected = False

    def __init__(self):
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_ADDRESS = (self.server, Constants.PORT)
        self.server_connection.connect(self.SERVER_ADDRESS)

    def send(self, package: str):
        message = package.encode(
            Constants.FORMAT
        )  # encode the string into a byte stream

        message_length = len(message)

        header = str(message_length).encode(
            Constants.FORMAT
        )  # the initial header to send to the server

        header += b" " * (
            Constants.HEADER_SIZE - len(header)
        )  # pad the header with the byte representation of a whitespace to ensure that the header is 64 bytes long

        self.server_connection.send(header)
        self.server_connection.send(message)

    def run(self):
        is_running = True

        while is_running:

            # msg = input()
            # self.send(msg)
            try:
                message_length = self.server_connection.recv(
                    Constants.HEADER_SIZE
                ).decode(
                    Constants.FORMAT
                )  # blocks thread until message is received. decode byte stream with UTF-8.

                if not message_length:
                    # stop processing message if message length is invalid
                    return

                message_length = int(message_length)

                message: str = self.server_connection.recv(message_length).decode(
                    Constants.FORMAT
                )

                print(f"RECEIVED FROM SERVER: {message}")
            except:
                pass

    # create event handlers


c = Client()
c.run()