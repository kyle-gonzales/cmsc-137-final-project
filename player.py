from power import Power, SpecialPower

class Player:
    def __init__(self, name:str, family:str):
        self.name = name
        self.family = family
        self.corruption_points = 1000
        self.fortress_health = 10000
        self.basic_powers = []
        self.special_powers = []

    def __str__(self):
        return "name: " + self.name + "\nfamily: " + self.family

    def init_powers(self):
        if self.family == "Duterte": # Duterte
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
