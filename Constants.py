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

    # background for choose family
    choose_fam_bg = "Assets/choose_family_bg.png"


    # family bg
    duterte_fam_bg = "Assets/dutete_info.png"
    marcos_fam_bg = "Assets/marcos_info.png"


    # button paths
    button_paths = ["Assets/duterte_button.png", "Assets/marcos_button.png"]
    duterte_button_paths = ["Assets/duterte_button_hovered.png", "Assets/marcos_button.png"]
    marcos_button_paths = ["Assets/duterte_button.png", "Assets/marcos_button_hovered.png"]
    button_width, button_height = 300, 85
    button_spacing = 20



