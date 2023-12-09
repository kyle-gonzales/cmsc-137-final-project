class CannonMovement:
    def __init__(self, rotated_barrel, rotated_barrel_rect, stand, cannon, screen_width, screen_height):
        self.rotated_barrel = rotated_barrel
        self.rotated_barrel_rect = rotated_barrel_rect
        self.stand = stand 
        self.cannon = cannon
        self.width = screen_width
        self.height = screen_height

    def draw(self, screen): 
        screen.blit(self.stand, (100, (self.height - (self.height//2.75))))
        screen.blit(self.cannon, (650, (self.height - (self.height//2.75))))
        screen.blit(self.rotated_barrel, self.rotated_barrel_rect.topleft)