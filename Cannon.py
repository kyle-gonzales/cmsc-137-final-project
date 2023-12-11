import pygame

#load cannon images
class Cannon:
    def __init__(self, image_path, scale):
        self.image_path = image_path
        self.scale = scale
    
    def load_image(self):
        return pygame.image.load(self.image_path)
    
    def scale_image(self):
        x, y = self.image_xy()
        return pygame.transform.scale(self.load_image(), (x//self.scale, y//self.scale))
    
    def image_xy(self):
        img = self.load_image()
        return img.get_width(), img.get_height()
    
    def flip_image(self):
        return pygame.transform.flip(self.scale_image(), True, False)