import pygame
import math
import random
from constants import Constants
from projectile import Projectile
from player import Player # you CANNOT import player because this file's name is player. 
#from powerselection import PowerSelectionMenu

SCREEN = pygame.display.set_mode((Constants.WIDTH,Constants.HEIGHT))
pygame.display.set_caption(Constants.APP_NAME)
clock = pygame.time.Clock()

SCREEN_WIDTH = Constants.WIDTH - 700
SCREEN_HEIGHT = Constants.HEIGHT + 200

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

def index_sp(power, special_powers):
    for i in range(len(special_powers)):
        if special_powers[i][0] == power: return i
    return -1

class PowerSelectionMenu:
    def __init__(self):
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

        self.player = Player(name= "Player", family= "Narcos") #will modify for the actual data from self.player.family
        # self.player = [player.name for player in self.player.name + self.player.family]
 
        self.player.init_for_client(ename="Enemy")
        self.option_name = [power.name for power in self.player.basic_powers + self.player.special_powers]
        self.option_cost = [str(power.cost) for power in self.player.basic_powers + self.player.special_powers]
        self.option_damage = [str(power.damage) for power in self.player.basic_powers + self.player.special_powers]
        self.coins = self.player.corruption_points

        for idx, option_name in enumerate(self.option_name):
            x_pos = self.spacing + idx * (self.button_width + 10)
            y_pos = Constants.HEIGHT - self.menu_height + 3 * self.spacing
            button_rect = pygame.Rect(x_pos, y_pos, self.button_width, self.button_height)
            self.option_rects.append(button_rect)

        self.power_images = {}
        for power_name, image_filename in Constants.POWER_IMAGE_NAME.items():
            image = pygame.image.load("Assets/" + image_filename).convert_alpha()
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
            self.draw_text(f"Corruption Points: {self.coins}", Constants.WHITE, self.menu_width - 170, Constants.HEIGHT - self.menu_height + 20, font_size=20)
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
                            return selected_power 

        pygame.quit()



# TODO: GET name input and family from EYL's welcome screen
dynasty = random.choice(["Dutete", "Narcos"])
name = "Kathryn"

# TODO: SEND name and dynasty to SERVER

# Initialize player in client's side
player = Player(name, dynasty)

# TODO: GET enemy name from SERVER
ename = "Daniel"

# Initialize player's other attributes
player.init_for_client(ename)
player.init_special_powers_coordinates()
player.update_phealth(10000)
player.update_ehealth(10000)

run = True # TODO: GET signal from SERVER that game starts

isPlayer = 0 # For testing functions on both player and enemy sides

while run: # Simulates taking turns between player and enemy
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Active and passive colors of names
    pactive_color = Constants.GREEN if isPlayer%2 else Constants.WHITE
    eactive_color = Constants.WHITE if isPlayer%2 else Constants.MAROON
    
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
    
    isPlayer += 1 # odd isPlayer: player's turn; even isPlayer: enemy's turn

    # TODO: GET signal from SERVER that player should launch a power
    launching = True

    # TODO: GET force from GEL's power menu
    power = PowerSelectionMenu()
    power = power.run_menu()

    # TODO: GET angle from EYL's cannon; verify if EYL uses deg or rad
    angle = int(input("angle: ")) * math.pi / 180
    
    if isPlayer:
        force = runSlider()
        print(force)
    # Initialize projectile; isPlayer = 1 means that projectile is launched from the player's side
    projectile = Projectile(angle, force, power, isPlayer%2)
    time = 0

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

        # Display player and enemy
        display_health(player.phealth, 1)
        display_health(player.ehealth, 0)
        
        hits = projectile.hits(1, player.pspecial_powers, SCREEN) if isPlayer%2 else projectile.hits(0, player.especial_powers, SCREEN)
        print(hits)
        
        if hits == "miss":
            # TODO: display "miss"
            launching = False
        elif hits == "fortress": # update health and stop projectile
            # TODO: display power damage
            if isPlayer%2:
                player.update_ehealth(player.ehealth-1500) # TODO: replace 1500 with power damage
            else:
                player.update_phealth(player.phealth-1500)
            launching = False
        else:
            if index_sp(hits, player.pspecial_powers) != -1: # remove power but dont stop projectile
                print(player.pspecial_powers.pop(index_sp(hits, player.pspecial_powers))) 
            elif index_sp(hits, player.especial_powers) != -1: # remove power but dont stop projectile
                print(player.especial_powers.pop(index_sp(hits, player.especial_powers))) 
            projectile.draw(SCREEN, clock)
            time += 0.25
            projectile.update(time)
        # TODO: SEND hits to SERVER
        pygame.display.flip()

    pygame.display.flip()

