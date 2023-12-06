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
    GREEN = (0,50,19)
    WHITE = (255,255,255)
    
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
    
    # Projectile coordinates
    Yi = 390
    PXi = 60
    EXi = 900