import socket
import sys

import pygame

from constants import Constants
from util import *

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Client:
    # player info

    server = "192.168.1.25"  # paste the IP of the server here

    def __init__(self):
        self.connected = False
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_ADDRESS = (self.server, Constants.PORT)

    def connect(self):
        self.server_connection.connect(self.SERVER_ADDRESS)
        self.server_connection.settimeout(0.1)

        self.color = input("choose color [255,255,255]: ") # temp; player info
        self.send(f"CONNECT " + self.color) # replace color with player info
        self.color = [int(channel) for channel in self.color.split(",")]

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
                WIN.fill((0, 0, 0))

                ##
                if message.startswith("PLAYER"):
                    players = message.split(";")
                    for player in players:
                        _, color, new_x = player.split("-")
                        color = [int(channel.strip()) for channel in color.split(",")]
                        pygame.draw.rect(WIN, tuple(color), (int(new_x), 100, 50, 50))

                    # Update the display
                    pygame.display.flip()

            clock.tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def welcome_screen(self):
        pass

    def winning_screen(self):
        pass

    def family_selection_screen(self):
        pass

    # create event handlers


c = Client()
c.main_game()
