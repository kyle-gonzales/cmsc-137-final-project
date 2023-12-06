import pygame
import math
from constants import Constants

class Projectile():
    def __init__(self, angle, vi, power, isPlayer):
        self.x:int = Constants.PXi if isPlayer else Constants.EXi
        self.y:int = Constants.Yi
        self.vi = vi
        self.vix = vi*math.cos(angle) if isPlayer else -vi*math.cos(angle)
        self.viy = vi*math.sin(angle)
        self.isPlayer = isPlayer
        print(Constants.POWER_IMAGE_NAME[power])
        img = pygame.image.load("Assets/" + Constants.POWER_IMAGE_NAME[power])
        self.img = img if isPlayer else pygame.transform.flip(img, True, False)
    
    def __str__(self):
        return "x = {}\ny = {}\nvix = {}\nviy = {}".format(self.x, self.y, self.vix, self.viy)
        
    def draw(self, SCREEN, clock):
        if self.vi < 60:
            clock.tick(80)
        elif self.vi < 80:
            clock.tick(150)
        else:
            clock.tick(200)
        SCREEN.blit(self.img,(self.x, self.y))

    def update(self, time):
        self.x = Constants.PXi + self.vix * time if self.isPlayer else Constants.EXi + self.vix * time
        self.y = Constants.Yi - (self.viy * time - 5*(time ** 2))