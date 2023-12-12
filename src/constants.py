import pygame


class Constants:
    APP_NAME = "Dutete vs Narcos: Dynasty War" # temp

    GAME_START = 0
    GAME_IN_PROGRESS = 1
    GAME_END = 2
    WAITING_FOR_PLAYERS = 3

    PORT = 5050

    FORMAT = "utf-8"

    DISCONNECT_MESSAGE = "!DISCONNECT"

    HEADER_SIZE = 64

    # Dynasty names
    NARCOS = "NARCOS"
    DUTETE = "DUTETE"

    # Colors
    GOLD = (253, 165, 0)
    MAROON = (147, 32, 37)
    DARKERMAROON = (127, 12, 17)
    GREEN = (0, 50, 19)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Screen dimensions
    WIDTH = 960
    HEIGHT = 540

     # Power Images
    POWER_IMAGE_NAME = {
        "Guns & Roses": "GunsAndRoses.png",
        "Drugs Race": "DrugsRace.png",
        "P*t*ng *n*": "ptng.png",
        "Corruption": "corruption.png",
        "Swiss Miss Bank": "swissmissbank.png",
        "Debate Na Lang Kaya": "debate.png",
        "Tank U": "tanku.png",
        "Designer Shoes": "shoes.png",
        "Tuna Panga": "panga.png",
        "I See See": "iseesee.png",
        "Bo Go": "bogo.png",
    }

    # Projectile coordinates
    Yi = 390
    PXi = 60
    EXi = 900
    
    # Special Power
    SPSIZE = (60, 60)
    SPX1 = 250
    SPX2 = 630
    SPY1 = 120
    SPY2 = 220
    
    # Font
    pygame.init()
    FONT32 = pygame.font.Font(None, 32)
    FONT24 = pygame.font.Font(None, 24)
    FONTH20 = pygame.font.Font(None, 20)
    
    
    pygame.init()

    #WELCOME SCREEN CONSTANTS
    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))
    welcome_screen_bg = "Assets/welcome_bg.png"
    welcome_screen = True

    # CHOOSE NAME CONSTANTS

    # background
    choose_name_bg = "../Assets/choose_name_bg.png"

    # Colors for the loading
    white = (255, 255, 255)
    gray = (128, 128, 128)

    # Calculate the center of the screen
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # Set up dots
    dot_radius = 5
    dot_spacing = 1
    dots = [
        (center_x - 50, center_y + 175),
        (center_x, center_y + 175),
        (center_x + 50, center_y + 175)
    ]

    # Set up the font
    font = pygame.font.SysFont("Courier", 50, "bold")
    prompt_text = font.render("Enter your name: ", True, (255, 255, 255))
    max_characters = 10
    display_default_underscores = True

    # CHOOSE FAMILY CONSTANTS

    # background for choose family
    choose_fam_bg = "../Assets/choose_family_bg.png"

    # family bg
    dutete_fam_bg = "../Assets/dutete_info.png"
    narcos_fam_bg = "../Assets/narcos_info.png"

    # button paths
    button_paths = ["Assets/dutete_button.png", "Assets/narcos_button.png"]
    dutete_button_paths = ["Assets/dutete_button_hovered.png", "Assets/narcos_button.png"]
    narcos_button_paths = ["Assets/dutete_button.png", "Assets/narcos_button_hovered.png"]
    button_width, button_height = 300, 85
    button_spacing = 20

    # CONSTANTS FOR CANNON MOVEMENT

    family_images = {
        "Narcos": {
            "bg": "../Assets/NarcosBG.png",
            "barrel": "../Assets/narcos_cannon_barrel.png",
            "stand": "../Assets/narcos_cannon_stand.png",
            "cannon": "../Assets/dutete_cannon_zero.png",
            "state": "False",
        },
        "Dutete": {
            "bg": "../Assets/DuteteBG.png",
            "barrel": "../Assets/dutete_cannon_barrel.png",
            "stand": "../Assets/dutete_cannon_stand.png",
            "cannon": "../Assets/narcos_cannon_zero.png",
            "state": "False",
        },
    }

    ANGLE = 0
    FORCE = 0
    POWER = 0
    ISHIT = 0