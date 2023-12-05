import random
import pygame
from constants import Constants

class Power:
  def __init__(self, name:str, cost:int, damage:int):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.image_name = Constants.POWER_IMAGE_NAME(name)

class SpecialPower(Power):
  def __init__(self, name:str, cost:int, damage:int, x:int, y:int):
    super().__init__(name, cost, damage)
    self.x = random.randint(Constants.WIDTH*0.25, Constants.WIDTH*0.75)
    self.y = random.randint(Constants.HEIGHT*0.25, Constants.HEIGHT*0.8)