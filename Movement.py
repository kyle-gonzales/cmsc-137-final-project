import pygame

class Movement:
    def __init__(self, barrel, screen_width, screen_height):
        self.barrel  = barrel
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rotate = True
        self.rotation_angle = 0
        self.rotation_direction = 1
    
    def rotate_barrel(self):
        #Rotate from 0 to 90: 90 to 0:
        self.rotation_angle += self.rotation_direction

        #Change rotation
        if self.rotation_angle == 90 or self.rotation_angle == 0:
            self.rotation_direction *= -1

        rotated_image = pygame.transform.rotate(self.barrel, self.rotation_angle)
        rotated_image_rect = rotated_image.get_rect(center=((self.screen_width//4.80), self.screen_height - (self.screen_height//3.25)))

        return rotated_image, rotated_image_rect
    
    def get_rotation_angle(self):
        return self.rotation_angle