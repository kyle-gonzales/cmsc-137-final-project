import pygame

#loads and displays background
class Background:
    def __init__(self, bg_path, screen):
        self.bg_path = bg_path
        self.screen = screen
    
    def load_image(self):
        return pygame.image.load(self.bg_path).convert()
    
    def scale_image(self):
        return pygame.transform.smoothscale(self.load_image(), self.screen.get_size())