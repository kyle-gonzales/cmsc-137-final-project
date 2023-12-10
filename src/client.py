import socket
import sys

import pygame

from constants import Constants
from util import *
from WelcomeScreenHandler import WelcomeScreenHandler

pygame.init()
pygame.font.init()

# WIDTH, HEIGHT = 750, 750
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Client:
    # player info

    server = "192.168.1.25"  # paste the IP of the server here

    is_player_one = False
    player_name = ""  # ! player names should be unique

    def __init__(self):
        self.connected = False
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_ADDRESS = (self.server, Constants.PORT)

    def connect(self):
        self.server_connection.connect(self.SERVER_ADDRESS)
        self.server_connection.settimeout(0.1)
        self.send(f"TRY_CONNECT")  # replace color with player info
        # self.color = [int(channel) for channel in self.color.split(",")]

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

    def receive_message(self):
        message_length = self.server_connection.recv(Constants.HEADER_SIZE).decode(
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
        return message

    def main_game(self):
        is_running = True
        clock = pygame.time.Clock()

        x = 50

        while is_running:
            message = ""
            """
                Attempt to receive a message from the server
            """
            try:
                message = self.receive_message()
            except Exception as e:
                # print(e)
                pass

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(Constants.DISCONNECT_MESSAGE)
                    is_running = False
                    self.connected = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    x -= 10
                    self.send(f"PLAYER-{stringify_tuple(self.color)}-{str(x)}")
                if keys[pygame.K_d]:
                    x += 10
                    self.send(f"PLAYER-{stringify_tuple(self.color)}-{str(x)}")

            # Main Game Logic
            if not self.connected and message.startswith("CONNECTED"):
                self.connected = True

            elif self.connected:
                # WIN.fill((0, 0, 0))

                ##
                if message.startswith("PLAYER"):
                    players = message.split(";")
                    for player in players:
                        _, color, new_x = player.split("-")
                        color = [int(channel.strip()) for channel in color.split(",")]
                        pygame.draw.rect(
                            Constants.screen, tuple(color), (int(new_x), 100, 50, 50)
                        )

                    # Update the display
                    pygame.display.flip()

            clock.tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def welcome_screen(self):
        # game loop
        clock = pygame.time.Clock()

        game = WelcomeScreenHandler()
        choosen_family = ""

        stage_screen = "Welcome Screen"
        is_running = True

        while is_running:
            message = ""
            """
                Try to Accept Message
            """
            try:
                message = self.receive_message()
            except Exception as e:
                # print(e)
                pass

            """
                Handle Message
            """
            if stage_screen == "Welcome Screen":
                if "CONNECTED_PLAYER_ONE" in message:
                    stage_screen = "Enter Name Screen"
                    self.connected = True
                    self.is_player_one = True
                    print("i am player 1")
                    # TODO: ENABLE CHARACTER SELECTION FLAG

                elif "CONNECTED_PLAYER_TWO" in message:
                    stage_screen = "Enter Name Screen"
                    self.connected = True
                    print("i am player 2")

                elif "TRY_CONNECT_FAILED" in message:
                    print("failed to connect to the server")
            elif stage_screen == "Enter Name Screen":
                if message.startswith("CONNECTED"):
                    stage_screen = "Choose Family Screen"

            elif stage_screen == "Choose Family Screen":
                if message.startswith("PLAYER"):
                    players = message.split(";")

                    for player_info in players:
                        name, family = player_info.split("|")[1:]

                        if name == self.player_name:
                            chosen_family = family
                        else:
                            chosen_family = "Dutete" if family == "Narcos" else "Narcos"
                    print(f"you are in FAMILY: {chosen_family}")
                    stage_screen = "Game Proper Screen"

            """
                Handle Events
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(Constants.DISCONNECT_MESSAGE)
                    is_running = False
                    self.connected = False
                    pygame.quit()
                    sys.exit()

                if stage_screen == "Welcome Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and not self.connected:
                            # try to connect to the server
                            self.connect()

                elif stage_screen == "Enter Name Screen":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.player_name = game.enter_name()
                            print(self.player_name)
                            self.send(f"CONNECT|{self.player_name}")
                        elif event.key == pygame.K_BACKSPACE:
                            game.remove_character()
                        else:
                            game.add_character(event)

                elif stage_screen == "Choose Family Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.is_player_one:
                                chosen_family = game.choose_family(event)
                                if chosen_family != "":
                                    self.send(
                                        f"FAMILY1|{self.player_name}|{chosen_family}"
                                    )
                            else:
                                print("waiting for player 1 to select the family")

                elif stage_screen == "Game Proper Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            angle = game.get_angle()
                            print(angle)

            """
                Update Display
            """

            game.display_background()

            if stage_screen == "Enter Name Screen":
                game.display_name()
            if stage_screen == "Choose Family Screen":
                game.draw_buttons()
            if stage_screen == "Game Proper Screen":
                game.display_cannon()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def winning_screen(self):
        pass


c = Client()
c.welcome_screen()
