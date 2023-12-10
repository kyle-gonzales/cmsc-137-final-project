from player import Player

"""
player information serialization:

PLAYER id x;PLAYER id x
"""


class GameState:
    players = dict()  # player_name (string): player_instance (Player)

    def update(self, name: str, player: Player):
        self.players[name] = player

    def __str__(self) -> str:
        output = ""

        for name, player in self.players.items():
            output += str(player) + ";"

        return output[:-1]
