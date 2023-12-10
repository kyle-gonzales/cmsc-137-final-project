import pygame

#creates button for the choose family screen
class Button:
    def __init__(self, paths, width, height, space, screen):
        self.listImagePaths = paths
        self.width = width
        self.height = height
        self.space = space
        self.screen = screen
        self.rects = []
        self.current_selection = None  
    
    def load_image(self):
        return [pygame.image.load(path) for path in self.listImagePaths]

    def scale(self):
        return [pygame.transform.scale(image, (self.width, self.height)) for image in self.load_image()]

    def width_between_button(self):
        return len(self.scale()) * (self.width + self.space) - self.space

    def is_clicked(self, mouse_pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                self.current_selection = self.listImagePaths[i]
                return self.current_selection

    def draw(self, surface):
        current_x = (surface.get_width() - self.width_between_button()) - 50
        button_y = (surface.get_height() - 100) - self.height //2

        for image in self.scale():
            rect = image.get_rect(topleft=(current_x, button_y))
            self.rects.append(rect)
            self.screen.blit(image, (current_x, button_y))
            current_x += self.width + self.space