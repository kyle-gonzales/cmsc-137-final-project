import socket
import sys
import pygame
import math
import random
import pygame
from projectile import Projectile
from player import Player
from constants import Constants
from util import *
from WelcomeScreenHandler import WelcomeScreenHandler
from GameProperHandler import GameProperHandler

pygame.init()
pygame.font.init()

SCREEN = pygame.display.set_mode((Constants.WIDTH,Constants.HEIGHT))
pygame.display.set_caption(Constants.APP_NAME)
clock = pygame.time.Clock()

SCREEN_WIDTH = Constants.WIDTH - 700
SCREEN_HEIGHT = Constants.HEIGHT + 200

pactive_color = None
eactive_color = None

def display_special_powers():
    for i in player.pspecial_powers: # (name, x, y)
        # shine bg
        shine = pygame.image.load("Assets/shine.png")
        SCREEN.blit(shine, (i[1], i[2]))
        # power icon
        img = pygame.image.load("Assets/" + Constants.POWER_IMAGE_NAME[i[0]])
        img = pygame.transform.scale(img, Constants.SPSIZE)
        SCREEN.blit(img, (i[1]+20, i[2]+20))
    for i in player.especial_powers:
        # shine bg
        poison = pygame.image.load("Assets/poison.png")
        SCREEN.blit(poison, (i[1], i[2]))
        # power icon
        img = pygame.image.load("Assets/" + Constants.POWER_IMAGE_NAME[i[0]])
        img = pygame.transform.scale(img, Constants.SPSIZE)
        SCREEN.blit(img, (i[1]+20, i[2]+20))

def display_header():
    # TODO: add name, health bar for both player and enemy
    pname_text = Constants.FONT32.render(player.name, True, pactive_color)
    ename_text = Constants.FONT32.render(player.ename, True, eactive_color)
    ename_text_rect = ename_text.get_rect()
    ename_text_rect.topright = (820,30)
    SCREEN.blit(pname_text, (140, 30))
    SCREEN.blit(ename_text, (675, 30))

    # Avatar
    pavatar = pygame.image.load("Assets/narcos_avatar.png") if player.family == Constants.NARCOS else pygame.image.load("Assets/dutete_avatar.png")
    eavatar = pygame.image.load("Assets/dutete_avatar.png") if player.family == Constants.NARCOS else pygame.image.load("Assets/narcos_avatar.png")
    pygame.draw.circle(SCREEN, pactive_color, (80,80), 50)
    pygame.draw.circle(SCREEN, eactive_color, (880,80), 50)
    SCREEN.blit(pavatar, (40,40))
    SCREEN.blit(eavatar, (840,40))

def display_health(current_health, isPlayer):
    # Health bar
    current_health_width = 200*current_health/10000
    maxhealth_rect = pygame.Rect(140, 60, 200, 15) if isPlayer else pygame.Rect(620, 60, 200, 15)
    current_health_rect = pygame.Rect(140, 60, current_health_width,15) if isPlayer else pygame.Rect(820 - current_health_width, 60, current_health_width, 15)
    pygame.draw.rect(SCREEN, Constants.BLACK, maxhealth_rect)
    pygame.draw.rect(SCREEN, pactive_color, current_health_rect) if isPlayer else pygame.draw.rect(SCREEN, eactive_color, current_health_rect)

    # Health in numbers
    phealth_text = Constants.FONT24.render(str(player.phealth), True, pactive_color)
    ehealth_text = Constants.FONT24.render(str(player.ehealth).rjust(5), True, eactive_color)
    SCREEN.blit(phealth_text, (140, 85))
    SCREEN.blit(ehealth_text, (770, 85))

def index_sp(power, special_powers):
    for i in range(len(special_powers)):
        if special_powers[i][0] == power: return i
    return -1

class Slider:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.x = (SCREEN_WIDTH  - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2 + 40
        self.range_width = SCREEN_WIDTH
        self.position = 50
        self.speed = 3
        self.direction = 1
        self.moving = True

    def draw(self):
        # Display fortresses and background
        SCREEN.blit(player.bg, (0,0))
        SCREEN.blit(player.pfort_now, (0,0))
        SCREEN.blit(player.efort_now, (0,0))

        # Display names
        display_header()

        # Display special powers
        display_special_powers()

        # Display player and enemy
        display_health(player.phealth, 1)
        display_health(player.ehealth, 0)
        
        fill_width = SCREEN_WIDTH - self.width - self.position
        x_offset = (Constants.WIDTH - Constants.WIDTH + 700) // 2

        filled_slider_rect = pygame.Rect(self.position + x_offset, self.y, fill_width, self.height)
        pygame.draw.rect(SCREEN, Constants.MAROON, filled_slider_rect)

        unfilled_slider_rect = pygame.Rect(x_offset, self.y, self.position, self.height)
        pygame.draw.rect(SCREEN, Constants.GOLD, unfilled_slider_rect)

        pygame.draw.rect(SCREEN, Constants.GREEN, (x_offset, self.y, self.range_width-17, self.height), 5)
        pygame.draw.rect(SCREEN, Constants.BLACK, (self.x + x_offset - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(SCREEN, Constants.GOLD, (self.x + x_offset , self.y, self.width, self.height))

        font = pygame.font.Font(None, 25) 
        font2 = pygame.font.Font(None, 36) 
        text = font.render("Power: " + str(self.get_value()), True, Constants.WHITE) 
        text2 = font2.render("CLICK TO RELEASE", True, Constants.WHITE) 
        text_rect = text.get_rect(center=(Constants.WIDTH // 2 -10, self.y + self.height + 20)) 
        text_rect2 = text.get_rect(center=(Constants.WIDTH // 2 -90, self.y + self.height + 40)) 
        SCREEN.blit(text, text_rect) 
        SCREEN.blit(text2, text_rect2) 

        pygame.display.flip()

    def update_position(self):
        self.position += self.speed * self.direction

    def get_value(self):
        value_range = 150 - 50
        ratio = (self.position / self.range_width)
        return int(50 + (ratio * value_range))

class SliderRun:
    def __init__(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.slider = Slider()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.slider.moving = False
                        return self.slider.get_value()

            if self.slider.moving:
                self.slider.update_position()

                if self.slider.position <= 0 or self.slider.position >= SCREEN_WIDTH - self.slider.width:
                    self.slider.direction *= -1

            if self.slider.position < 0:
                self.slider.position = 0
            elif self.slider.position > SCREEN_WIDTH - self.slider.width:
                self.slider.position = SCREEN_WIDTH - self.slider.width

            self.slider.x = self.slider.position

            self.slider.draw()

            pygame.display.flip()
        print(self.slider.get_value())
    
def runSlider():
    slider = SliderRun()
    return slider.run()

class PowerSelectionMenu:
    def __init__(self, family1):
        pygame.init()
        SCREEN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        pygame.display.set_caption("Selection Menu")
        self.menu_width = 690
        self.menu_height = 250
        self.button_width = 100
        self.button_height = 120
        self.spacing = 20

        self.menu_rect = pygame.Rect(0, Constants.HEIGHT - self.menu_height, self.menu_width, self.menu_height)
        self.option_rects = []
        self.selected_options = 0

        self.option_name = [power.name for power in player.basic_powers]
        self.option_cost = [str(power.cost) for power in player.basic_power]
        self.option_damage = [str(power.damage) for power in player.basic_powers]
        player.corruption_points = player.corruption_points

        for idx, option_name in enumerate(self.option_name):
            x_pos = self.spacing + idx * (self.button_width + 10)
            y_pos = Constants.HEIGHT - self.menu_height + 3 * self.spacing
            button_rect = pygame.Rect(x_pos, y_pos, self.button_width, self.button_height)
            self.option_rects.append(button_rect)

        self.power_images = {}
        for power_name, image_filename in Constants.POWER_IMAGE_NAME.items():
            image = pygame.image.load("../Assets/" + image_filename).convert_alpha()
            self.power_images[power_name] = pygame.transform.scale(image, (self.button_width, self.button_height))

    def draw_text(self, text, color, x, y, center=False, font_size=20):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        SCREEN.blit(text_surface, text_rect)
        return text_rect

    def run_menu(self):
        clock.tick(300)
        running = True
        selected_power = ""

        while running:
            # Display fortresses and background
            SCREEN.blit(player.bg, (0,0))
            SCREEN.blit(player.pfort_now, (0,0))
            SCREEN.blit(player.efort_now, (0,0))

            # Display names
            display_header()

            # Display special powers
            display_special_powers()

            # Display player and enemy
            display_health(player.phealth, 1)
            display_health(player.ehealth, 0)
            
            pygame.draw.rect(SCREEN, Constants.MAROON, self.menu_rect, border_top_right_radius=10)
            pygame.draw.rect(SCREEN, Constants.GOLD, self.menu_rect, 5, border_top_right_radius=10)
            pygame.draw.rect(SCREEN, Constants.MAROON, (0, Constants.HEIGHT - self.menu_height + 5, 5, self.menu_height))  # Left side
            pygame.draw.rect(SCREEN, Constants.MAROON, (0, Constants.HEIGHT - 5, self.menu_width - 5, 5))  # Bottom side
            select_button = pygame.draw.rect(SCREEN, Constants.GOLD, (Constants.WIDTH // 2 - 185, Constants.HEIGHT - self.menu_height + 195, 100, 40), border_radius=5)

            for idx, text_rect in enumerate(self.option_rects):
                pygame.draw.rect(SCREEN, Constants.DARKERMAROON, text_rect, border_radius=10)
                white_rect = pygame.draw.rect(SCREEN, Constants.WHITE, (text_rect.x + 10, text_rect.y + 10  , 80, 50), border_radius=10)
                
                power_name = self.option_name[idx]
                if power_name in self.power_images:
                    image = self.power_images[power_name]
                    scaled_image = pygame.transform.scale(image, (white_rect.width - 20, white_rect.height))
                    image_x = text_rect.x + 10 + (white_rect.width - scaled_image.get_width()) // 2
                    image_y = text_rect.y + 10 + (white_rect.height - scaled_image.get_height()) // 2
                    SCREEN.blit(scaled_image, (image_x, image_y))
                
                self.draw_text(self.option_name[idx], Constants.WHITE, text_rect.x + self.button_width // 2, text_rect.y + 75, center=True, font_size=14)
                self.draw_text(self.option_cost[idx], Constants.WHITE, text_rect.x + self.button_width // 2, text_rect.y + 90, center=True, font_size=20)
                self.draw_text(self.option_damage[idx], Constants.WHITE, text_rect.x + self.button_width // 2, text_rect.y + 105, center=True, font_size=24)
            
            self.draw_text("Powers", Constants.WHITE, 20, Constants.HEIGHT - self.menu_height + 20, font_size=32)
            self.draw_text(f"Corruption Points: {player.corruption_points}", Constants.WHITE, self.menu_width - 170, Constants.HEIGHT - self.menu_height + 20, font_size=20)
            self.draw_text("Select", Constants.BLACK, self.menu_width // 2, Constants.HEIGHT - self.menu_height + 215, center=True, font_size= 30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for idx, rect in enumerate(self.option_rects):
                            if rect.collidepoint(mouse_pos) and idx != self.selected_options:
                                self.selected_options = idx
                                for r in self.option_rects:
                                    r.width = self.button_width
                                    r.height = self.button_height
                                print(f"Clicked on option: {self.option_name[idx]}")
                                self.option_rects[idx].inflate_ip(5, 5)
                                break
                        pygame.display.update()
                            
                        if select_button.collidepoint(mouse_pos):
                            selected_power = self.option_name[self.selected_options]
                            select_button.inflate_ip(5, 5)
                            index = index_sp(selected_power, player.basic_powers)
                            cost = (player.basic_powers[index]).cost
                            player.corruption_points -= cost
                            return selected_power 

        pygame.quit()

# TODO: GET name input and family from EYL's welcome screen
dynasty = ""
name = "Player"

# TODO: SEND name and dynasty to SERVER

# Initialize player in client's side
player = None

# TODO: GET enemy name from SERVER
ename = "Enemy"

class Client:
    # player info

    server = "192.168.101.7"  # paste the IP of the server here

    is_player_one = False
    player_name = ""  # ! player names should be unique
    chosen_family = ""

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
        game = WelcomeScreenHandler()

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
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(Constants.DISCONNECT_MESSAGE)
                    is_running = False
                    self.connected = False
                    pygame.quit()
                    sys.exit()
                    
            # if stage_screen is initialized here, the handle events will execute the next screen
            if stage_screen == "Welcome Screen":
                if "CONNECTED_PLAYER_ONE" in message:
                    # stage_screen = "Enter Name Screen"
                    self.connected = True
                    self.is_player_one = True
                    print("i am player 1")
                    # TODO: ENABLE CHARACTER SELECTION FLAG

                elif "CONNECTED_PLAYER_TWO" in message:
                    # stage_screen = "Enter Name Screen"
                    self.connected = True
                    print("i am player 2")

                elif "TRY_CONNECT_FAILED" in message:
                    print("too many players on server. disconnecting...")
                    self.send(Constants.DISCONNECT_MESSAGE)
            elif stage_screen == "Enter Name Screen":
                if message.startswith("CONNECTED"):
                    pass
                    # stage_screen = "Choose Family Screen"

            elif stage_screen == "Choose Family Screen":
                if message.startswith("PLAYER"):
                    players = message.split(";")

                    for player_info in players:
                        name, family = player_info.split("|")[1:]

                        if name == self.player_name:
                            self.chosen_family = family
                        else:
                            self.chosen_family = "Dutete" if family == "Narcos" else "Narcos"
                    print(f"you are in FAMILY: {self.chosen_family}")
                # removed the stage_screen = game proper

                if stage_screen == "Welcome Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # if connected proceed to enter name screen
                            if self.connected:
                                game.start_connect()
                                stage_screen = "Enter Name Screen"
                            else:
                                self.connect()

                elif stage_screen == "Enter Name Screen":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.player_name = game.enter_name()
                            print(self.player_name)
                            self.send(f"CONNECT|{self.player_name}")

                            stage_screen = "Choose Family Screen"
                        elif event.key == pygame.K_BACKSPACE:
                            game.remove_character()
                        else:
                            game.add_character(event)

                elif stage_screen == "Choose Family Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.is_player_one:
                                self.chosen_family = game.choose_family(event)
                                #will also call the game proper screen to initialize the cannons
                                if self.chosen_family != "":
                                    self.send(
                                        f"FAMILY1|{self.player_name}|{self.chosen_family}"
                                    )
                                    self.game_proper_screen()

                            else:
                                print("waiting for player 1 to select the family")

                    if not self.is_player_one:
                        if self.chosen_family != "":
                            stage_screen = "Game Proper Screen"
                            self.game_proper_screen()

            """
                Update Display
            """

            game.display_background()

            if stage_screen == "Enter Name Screen":
                game.display_name()
            if stage_screen == "Choose Family Screen":
                game.draw_buttons()

            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def game_proper_screen(self):
        p_num = 1 if self.is_player_one else 2
        name = "" #TODO: get name from server
        player = Player(name, dynasty)
        # TODO: GET enemy name from SERVER
        ename = ""

        # Initialize player's other attributes
        player.init_for_client(ename)
        player.init_special_powers_coordinates()
        player.update_phealth(10000)
        player.update_ehealth(10000)
        is_running = True
        
        gameProper = GameProperHandler()
        stage_screen = "Game Proper Screen"

        #create cannon instance
        gameProper.create_cannon_instance(self.chosen_family)

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

            message_split = message.split("|")
            
            # Display fortresses and background
            SCREEN.blit(player.bg, (0,0))
            SCREEN.blit(player.pfort_now, (0,0))
            SCREEN.blit(player.efort_now, (0,0))

            # Display names
            display_header()

            # Display special powers
            display_special_powers()

            # Display player and enemy
            display_health(player.phealth, 1)
            display_health(player.ehealth, 0)
            
            pygame.display.flip

            if message_split[0] == "TURN":
                if self.is_player_one == int(message_split[1]):
                    if self.chosen_family == Constants.DUTETE:
                        pactive_color = Constants.GREEN
                        eactive_color = Constants.WHITE
                    else:
                        pactive_color = Constants.MAROON
                        eactive_color = Constants.WHITE
                    power = PowerSelectionMenu(self.chosen_family)
                    power = power.run_menu()
                    # TODO: GET angle from EYL's cannon; verify if EYL uses deg or rad
                    angle = int(input("angle: ")) * math.pi / 180
                    force = runSlider()
                    self.send(f"PLAYER|{p_num}|PROJECTILE|{angle}|{force}|{power}")
                    isPlayer = True
                else: isPlayer = False
            elif message_split[0] == "PLAYER":
                if isPlayer == False:
                    if self.chosen_family == Constants.DUTETE:
                        pactive_color = Constants.WHITE
                        eactive_color = Constants.MAROON
                    else:
                        pactive_color = Constants.WHITE
                        eactive_color = Constants.GREEN
                    angle = int(message_split[3])
                    force = int(message_split[4])
                    power = message_split[5]
                time = 0
                projectile = Projectile(angle, force, power, isPlayer)
                launching = True
                while launching:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        
                    # Display fortresses and background
                    SCREEN.blit(player.bg, (0,0))
                    SCREEN.blit(player.pfort_now, (0,0))
                    SCREEN.blit(player.efort_now, (0,0))

                    # Display names
                    display_header()

                    # Display special powers
                    display_special_powers()
                    
                    hits = projectile.hits(1, player.pspecial_powers, SCREEN) if isPlayer%2 else projectile.hits(0, player.especial_powers, SCREEN)
                    print(hits)
                    
                    if hits == "miss":
                        # TODO: display "miss"
                        launching = False
                    elif hits == "fortress": # update health and stop projectile
                        damage = Constants.POWERS[power]
                        launching = False
                        if isPlayer and p_num == 1: player.ehealth -= damage
                        else: player.phealth -= damage
                        self.send(f"HEALTH|{player.phealth}{player.ehealth}") if isPlayer and p_num == 1 else self.send(f"HEALTH|{player.ehealth}{player.phealth}")
                    else:
                        if index_sp(hits, player.pspecial_powers) != -1: # remove power but dont stop projectile
                            player.basic_powers = player.pspecial_powers.pop(index_sp(hits, player.pspecial_powers))
                            
                        elif index_sp(hits, player.especial_powers) != -1: # remove power but dont stop projectile
                            print(player.especial_powers.pop(index_sp(hits, player.especial_powers))) 
                        projectile.draw(SCREEN, clock)
                        time += 0.25
                        projectile.update(time)
                    
                    pygame.display.flip()
                
            elif message_split[0] == "HEALTH":
                player.update_phealth(message_split[1])
                player.update_ehealth(message_split[2])
                
                # Display player and enemy
                display_health(player.phealth, 1)
                display_health(player.ehealth, 0)
            
            elif message_split[0] == "WINNER":
                self.winning_screen(message_split[1])
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(Constants.DISCONNECT_MESSAGE)
                    is_running = False
                    self.connected = False
                    pygame.quit()
                    sys.exit()

                if stage_screen == "Game Proper Screen":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            angle = gameProper.get_angle() #get angle
                            print(angle)

            """
                Update Display
            """

            gameProper.display_background()
            gameProper.display_cannon()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def winning_screen(self, winner):
        pass


c = Client()
c.welcome_screen()
