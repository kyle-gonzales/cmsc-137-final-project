import pygame
import math
import random
from constants import Constants
from projectile import Projectile
from player import Player # you CANNOT import player because this file's name is player. 
from powerselection import PowerSelectionMenu

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

SCREEN = pygame.display.set_mode((Constants.WIDTH,Constants.HEIGHT))
pygame.display.set_caption(Constants.APP_NAME)
clock = pygame.time.Clock()


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
    isPlayer += 1 # odd isPlayer: player's turn; even isPlayer: enemy's turn

    # TODO: GET signal from SERVER that player should launch a power
    launching = True

    # TODO: GET force from GEL's power menu
    power = PowerSelectionMenu()
    power = power.run_menu()

    # TODO: GET force from GEL's slider
    force = int(input("force: "))

    # TODO: GET angle from EYL's cannon; verify if EYL uses deg or rad
    angle = int(input("angle: ")) * math.pi / 180

    # Initialize projectile; isPlayer = 1 means that projectile is launched from the player's side
    projectile = Projectile(angle, force, power, isPlayer%2)
    time = 0

    # Active and passive colors of names
    pactive_color = Constants.GREEN if isPlayer%2 else Constants.WHITE
    eactive_color = Constants.WHITE if isPlayer%2 else Constants.MAROON

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
        pygame.display.flip()

    pygame.display.flip()

