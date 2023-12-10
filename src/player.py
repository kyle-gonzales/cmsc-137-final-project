from util import *

class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.x = 100
        self.family = ""

    def __str__(self):
        output = "PLAYER|"

        output += self.id + "|"
        output += self.family

        return output
