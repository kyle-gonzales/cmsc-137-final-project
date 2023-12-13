import pygame
from power import Power
from constants import Constants

class Player:
    def __init__(self, name:str, family:str):
        self.name = name.upper()
        self.family = family
        self.corruption_points = 1000
        self.fortress_health = 10000
        self.basic_powers = []
        self.special_powers = []

    def __str__(self):
        return "name = {}\nfamily = {}\ncorruption points= {}\nfortress health = {}\nbasic powers = {}\nspecial powers = {}\n".format(
            self.name,self.family,self.corruption_points,self.fortress_health, self.basic_powers, self.special_powers
        )

    def init_for_client(self, ename):
        # p = player; e = enemy
        self.ename = ename.upper()
        # images, color
        self.bg = pygame.image.load("../Assets/NarcosBG.png") if self.family == Constants.NARCOS else pygame.image.load("../Assets/DuteteBG.png")
        self.pcolor = Constants.MAROON if self.family == Constants.NARCOS else Constants.GREEN
        self.ecolor = Constants.GREEN if self.family == Constants.NARCOS else Constants.MAROON
        if self.family == Constants.NARCOS:
            self.pfort = [pygame.image.load("../Assets/NarcosFortress.png"), 
                    pygame.image.load("../Assets/NarcosFortress75.png"),
                    pygame.image.load("../Assets/NarcosFortress50.png"),
                    pygame.image.load("../Assets/NarcosFortress25.png"),
                    #pygame.image.load("Assets/NarcosFortress0.png")
                    ] 
            self.efort = [pygame.image.load("../Assets/DuteteFortress.png"),
                    pygame.image.load("../Assets/DuteteFortress75.png"),
                    pygame.image.load("../Assets/DuteteFortress50.png"),
                    pygame.image.load("../Assets/DuteteFortress25.png"),
                    #pygame.image.load("Assets/DuteteFortress0.png")
                    ]
            for i in range(len(self.efort)):
                self.pfort[i] = pygame.transform.flip(self.pfort[i], True, False)
                self.efort[i] = pygame.transform.flip(self.efort[i], True, False)
        else:
            self.pfort = [pygame.image.load("../Assets/DuteteFortress.png"),
                    pygame.image.load("../Assets/DuteteFortress75.png"),
                    pygame.image.load("../Assets/DuteteFortress50.png"),
                    pygame.image.load("../Assets/DuteteFortress25.png"),
                    #pygame.image.load("Assets/DuteteFortress0.png")
                    ]
            self.efort = [pygame.image.load("../Assets/NarcosFortress.png"), 
                    pygame.image.load("../Assets/NarcosFortress75.png"),
                    pygame.image.load("../Assets/NarcosFortress50.png"),
                    pygame.image.load("../Assets/NarcosFortress25.png"),
                    #pygame.image.load("Assets/NarcosFortress0.png")
                    ]
        self.pfort_now = self.pfort[0]
        self.efort_now = self.efort[0]
        # player powers
        if self.family == Constants.DUTETE:
          self.basic_powers = [
              Power(name="Guns & Roses", cost=215, damage=1399),
              Power(name="Drugs Race", cost=135, damage=859),
              Power(name="P*t*ng *n*", cost=70, damage=459),
              Power(name="Corruption", cost=0, damage=99)
          ]
          self.special_powers = [
              Power(name="Swiss Miss Bank", cost=0, damage=1019),
              Power(name="Debate Na Lang Kaya", cost=0, damage=1679)
          ]
        else: # Marcos
          self.basic_powers = [
              Power(name="Tank U", cost=245, damage=1599),
              Power(name="Designer Shoes", cost=100, damage=619),
              Power(name="Tuna Panga", cost=75, damage=479),
              Power(name="Corruption", cost=0, damage=99)
          ]
          self.special_powers = [
              Power(name="I See See", cost=0, damage=929),
              Power(name="Bo Go", cost=0, damage=1769)
          ]
          
    def update_phealth(self, phealth):
        self.phealth = phealth
        if self.phealth > 7500: self.pfort_now = self.pfort[0]
        elif self.phealth > 5000: self.pfort_now = self.pfort[1]
        elif self.phealth > 2500: self.pfort_now = self.pfort[2]
        elif self.phealth > 0: self.pfort_now = self.pfort[3]
        else: self.pfort_now = self.pfort[0]   ### TODO: add image

    def update_ehealth(self, ehealth):
        self.ehealth = ehealth
        if self.ehealth > 7500: self.efort_now = self.efort[0]
        elif self.ehealth > 5000: self.efort_now = self.efort[1]
        elif self.ehealth > 2500: self.efort_now = self.efort[2]
        elif self.ehealth > 0: self.efort_now = self.efort[3]
        else: self.efort_now = self.efort[0]   ### TODO: add image
    
    def init_special_powers_coordinates(self): 
        self.pspecial_powers = [("I See See", Constants.SPX1, Constants.SPY2),
                            ("Bo Go", Constants.SPX2, Constants.SPY1)] if self.family == "Narcos" else [
                                ("Swiss Miss Bank", Constants.SPX1, Constants.SPY2),
                                ("Debate Na Lang Kaya", Constants.SPX2, Constants.SPY1)]
        self.especial_powers = [("Swiss Miss Bank", Constants.SPX1, Constants.SPY1),
                            ("Debate Na Lang Kaya", Constants.SPX2, Constants.SPY2)] if self.family == "Narcos" else [
                                ("I See See", Constants.SPX1, Constants.SPY1),
                                ("Bo Go", Constants.SPX2, Constants.SPY2)]