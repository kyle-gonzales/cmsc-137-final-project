import random

import pygame

from constants import Constants


class Power:
    def __init__(self, name: str, cost: int, damage: int):
        self.name = name
        self.cost = cost 
        self.damage = damage

    def __str__(self):
        return "power name = {}\ncost = {}\ndamage = {}".format(
            self.name, self.cost, self.damage
        )
