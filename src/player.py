from util import *

class Player:
    def __init__(self, id, x) -> None:
        self.id = id
        self.x = x

    def __str__(self):
        output = "PLAYER-"

        output += stringify_tuple(self.id) + "-"
        output += f"{self.x}"

        return output
