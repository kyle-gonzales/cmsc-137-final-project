import pygame
import math
from constants import Constants

class Projectile():
    def __init__(self, angle, xi, yi, vi, power):
        self.x:int = xi
        self.y:int = yi
        self.vi = vi
        self.vix = vi*math.cos(angle)
        self.viy = vi*math.sin(angle)
        self.img = pygame.image.load("Assets/" + Constants.POWER_IMAGE_NAME[power])
        
    def __str__(self):
        return "x = {}\ny = {}\nvix = {}\nviy = {}".format(self.x, self.y, self.vix, self.viy)
        
    def draw(self, SCREEN, clock, i):
        if self.vi < 40: 
            clock.tick(50)
        elif self.vi < 60:
            clock.tick(70)
        elif self.vi < 80:
            clock.tick(80)
        else:
            clock.tick(100)
        SCREEN.blit(self.img,(self.x, self.y))
        pygame.display.flip()

    def update(self, xi, yi, time):
        self.x = xi + self.vix * time
        self.y = yi - (self.viy * time - 5*(time ** 2))