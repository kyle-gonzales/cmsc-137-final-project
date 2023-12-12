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
        
        img = pygame.image.load("Assets/" + Constants.POWER_IMAGE_NAME[power])
        img = img if isPlayer else pygame.transform.flip(img, True, False)
        self.img = pygame.transform.scale(img, (76,76))
    def __str__(self):
        return "x = {}\ny = {}\nvix = {}\nviy = {}".format(self.x, self.y, self.vix, self.viy)
        
    def draw(self, SCREEN, clock):
        # change projectile display speed
        if self.vi < 60:
            clock.tick(80)
        elif self.vi < 80:
            clock.tick(150)
        else:
            clock.tick(200)

        # power bg
        power_bg = pygame.image.load("Assets/shine.png") if self.isPlayer else pygame.image.load("Assets/poison.png")
        SCREEN.blit(power_bg, (self.x - 8, self.y - 8))
        # power icon
        SCREEN.blit(self.img,(self.x, self.y))

    def update(self, time):
        self.x = Constants.PXi + self.vix * time if self.isPlayer else Constants.EXi + self.vix * time
        self.y = Constants.Yi - (self.viy * time - 5*(time ** 2))
    
    def hits(self, isPlayer, special_powers, SCREEN):
    # midair
        projectile_rect = pygame.Rect(self.x, self.y, 80, 80)
        
        for i in special_powers:
            special_power_rect = pygame.Rect(i[1], i[2], 90, 90)
            if projectile_rect.colliderect(special_power_rect):
                return i[0]
            
        fortress_rect = pygame.Rect(700, 270, 260, 240) if isPlayer else pygame.Rect(0, 270, 260, 240)
        if projectile_rect.colliderect(fortress_rect): return "fortress"
        
        if self.y <= Constants.Yi and (
            (self.x <= Constants.WIDTH + 100 and isPlayer) 
            or (self.x >= -100 and not(isPlayer))
            ): return "midair"
        
        else: return "miss"