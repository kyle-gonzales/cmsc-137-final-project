import socket
import threading
import traceback

from constants import Constants
from game_state import GameState
from player import Player
from util import *


class GameServer:
    def __init__(self) -> None:
        self.clients = []

        self.player_data = ""
        self.connected_players_count = 0
        self.game: GameState = GameState()
        self.game_stage = Constants.WAITING_FOR_PLAYERS

        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # create socket
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())  # get local IP;
        self.ADDRESS = (self.SERVER_IP, Constants.PORT)

        self.server_socket.bind(self.ADDRESS)

        print("SERVER INITIALIZED: Game created successfully...")

    def handle_client(self, client_connection, address):
        is_running = True

        while is_running:
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
                    is_running = False
                    self.clients.remove(client_connection)
                    self.connected_players_count -= 1

                print(f"MESSAGE RECEIVED FROM [{address}]: {message}")

                if self.game_stage == Constants.WAITING_FOR_PLAYERS:
                    if message.startswith("CONNECT"):
                        rgb = tuple(
                            [
                                int(channel.strip())
                                for channel in message.split()[1].split(",")
                            ]
                        )
                        player = Player(rgb, 100)
                        self.game.update("", player)

                        self.broadcast("CONNECTED " + str(rgb))
                        self.connected_players_count += 1
                        print(self.connected_players_count)

                        if self.connected_players_count == 2:
                            self.game_stage = Constants.GAME_START
                    else:
                        self.broadcast( # for testing
                            "waiting for players, but message is NOT 'CONNECT'"
                        )

                elif self.game_stage == Constants.GAME_START:
                    print(
                        "GAME START. Both players are connected and the game is starting"
                    )
                    self.broadcast("Game is starting")
                    self.game_stage = Constants.GAME_IN_PROGRESS

                elif self.game_stage == Constants.GAME_IN_PROGRESS:
                    if message.startswith("PLAYER"):
                        _, player_id, x = message.split("-")

                        player_id = tuple([int(x) for x in player_id.split(",")])  # rgb

                        # Todo update the game state

                        player: Player = self.game.players.get(player_id)
                        player.x = x

                        self.game.update("", player)

                        # broadcast the game state to all players

                        self.broadcast(str(self.game))

                elif self.game_stage == Constants.GAME_END:
                    pass
                else:
                    print(
                        f"INVALID GAME STAGE: '{self.game_stage}' is not a valid game stage"
                    )

            except Exception as e:
                print(traceback.format_exc())
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

            self.clients.append(client_connection)

            # print(
            #     f"\nACTIVE CONNECTIONS: {threading.active_count() - 1}"
            # )  # how many threads (clients) are active in this process

    def broadcast(
        self, package: str
    ):  # TODO: iterate through each of the client connections and broadcast the information to all the players
        for client in self.clients:
            self.send(client, package)
        # for name, player in self.game.players.items():
        #     self.send(player, package)

    def send(self, client, package: str):
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

        client.send(header)
        client.send(message)