import pygame

class Constants:

    APP_NAME ="Dutete vs Narcos: Dynasty War" # temp

    GAME_START = 0
    GAME_IN_PROGRESS = 1
    GAME_END = 2
    WAITING_FOR_PLAYERS = 3

    PORT = 5050

    FORMAT = "utf-8"

    DISCONNECT_MESSAGE = "!DISCONNECT"

    HEADER_SIZE = 64
    
    # Screen dimensions
    WIDTH = 960
    HEIGHT = 540
    
    # Colors
    GOLD = (253,165,0)
    MAROON = (147,32,37)
    DARKERMAROON = (127, 12, 17)
    GREEN = (0,50,19)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    
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
        "Bo Go": "bogo.png"
    }
    
    IMAGE_PATH = "cmsc-137-final-project/Assets/"

    # Font
    # # Architype Aubette Source: https://www.onlinewebfonts.com/download/26afb49b8b7dda2c10686589d6fc7b55
    # pygame.init()
    # ARCH32 = pygame.font.Font("Assets/Architype_Aubette.ttf", 32)
    # ARCH24 = pygame.font.Font("Assets/Architype_Aubette.ttf", 24)
    # ARCH20 = pygame.font.Font("Assets/Architype_Aubette.ttf", 20)