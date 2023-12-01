import socket
import threading

from constants import Constants
from game_state import GameState
from player import Player


class GameServer:
    player_data = ""

    connected_players_count = 0

    game: GameState

    game_stage = Constants.WAITING_FOR_PLAYERS

    def __init__(self) -> None:
        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # create socket

        self.SERVER_IP = socket.gethostbyname(socket.gethostname())  # get local IP;
        self.ADDRESS = (self.SERVER_IP, Constants.PORT)

        self.server_socket.bind(self.ADDRESS)

        print("SERVER INITIALIZED: Game created successfully...")

    def handle_client(self, client_connection, address):
        connected = True

        while connected:
            try:
                message_length = client_connection.recv(Constants.HEADER_SIZE).decode(
                    Constants.FORMAT
                )  # blocks thread until message is received. decode byte stream with UTF-8.

                if not message_length:
                    # stop processing message if message length is invalid
                    return

                message_length = int(message_length)

                message: str = client_connection.recv(message_length).decode(
                    Constants.FORMAT
                )

                if message == Constants.DISCONNECT_MESSAGE:
                    connected = False

                print(
                    f"MESSAGE RECEIVED FROM [{address}]: {message}"
                )  # TODO: handle message based on game state

                if self.game_stage == Constants.WAITING_FOR_PLAYERS:
                    pass
                elif self.game_stage == Constants.GAME_START:
                    pass
                elif self.game_stage == Constants.GAME_IN_PROGRESS:
                    pass
                elif self.game_stage == Constants.GAME_END:
                    pass
                else:
                    print(
                        f"INVALID GAME STAGE: '{self.game_stage}' is not a valid game stage"
                    )

            except:
                pass

        client_connection.close()
        print(f"SUCCESSFUL DISCONNECTION: {address} has disconnected.")
        # TODO: update number of connected players

    def run(self):
        self.server_socket.listen()

        is_running = True

        print(
            f"SERVER IS RUNNING: Server is listening on {self.SERVER_IP} via port {Constants.PORT}\n"
        )

        while is_running:
            client_connection, address = self.server_socket.accept()  # blocks thread

            thread = threading.Thread(
                target=self.handle_client, args=(client_connection, address)
            )

            thread.start()
            """
            print(
                f"\nACTIVE CONNECTIONS: {threading.active_count() - 1}"
            )  # how many threads (clients) are active in this process
            """

    def broadcast(self, msg: str):
        pass

    def send(self, player: Player, msg: str):
        pass
