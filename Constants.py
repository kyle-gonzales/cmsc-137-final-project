import pygame
import sys

class Constants:
    pygame.init()

    #WELCOME SCREEN CONSTANTS
    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))
    welcome_screen_bg = "Assets/welcome_bg.png"
    welcome_screen = True

    #CHOOSE NAME CONSTANTS
    #Choose Name Screen
    choose_name_screen = False

    #background
    choose_name_bg = "Assets/choose_name_bg.png"

    # Colors for the loading
    white = (255, 255, 255)
    gray = (128, 128, 128)

    # Calculate the center of the screen
    center_x, center_y = width // 2, height // 2

    # Set up dots
    dot_radius = 5
    dot_spacing = 1
    dots = [(center_x - 50, center_y + 175), (center_x, center_y + 175), (center_x + 50, center_y + 175)]

    # Set up the font
    font = pygame.font.SysFont("Courier", 50, "bold")
    prompt_text = font.render("Enter your name: ", True, (255, 255, 255))
    max_characters = 10
    input_text = ""
    display_default_underscores = True

    #CHOOSE FAMILY CONSTANTS
    # screens
    choose_family_screen = False

    dutete_screen = False
    narcos_screen = False

    # background for choose family
    choose_fam_bg = "Assets/choose_family_bg.png"


    # family bg
    dutete_fam_bg = "Assets/dutete_info.png"
    narcos_fam_bg = "Assets/narcos_info.png"

    # button paths
    button_paths = ["Assets/dutete_button.png", "Assets/narcos_button.png"]
    dutete_button_paths = ["Assets/dutete_button_hovered.png", "Assets/narcos_button.png"]
    narcos_button_paths = ["Assets/dutete_button.png", "Assets/narcos_button_hovered.png"]
    button_width, button_height = 300, 85
    button_spacing = 20

    # CONSTANTS FOR CANNON MOVEMENT
    
    #the screen of where the cannon is located?
    game_proper_screen = False
    family_name = ""

    family_images = {
    "Narcos": {"bg": "Assets/NarcosBG.png", "barrel": "Assets/narcos_cannon_barrel.png", "stand": "Assets/narcos_cannon_stand.png", "cannon": "Assets/dutete_cannon_zero.png"},
    "Dutete": {"bg": "Assets/DuteteBG.png", "barrel": "Assets/dutete_cannon_barrel.png", "stand": "Assets/dutete_cannon_stand.png", "cannon": "Assets/narcos_cannon_zero.png"}
    }



