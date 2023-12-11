import pygame

from Constants import *

#used to display the choosen name
class ChooseName:
    def __init__(self, width, height, max_characters, font, white, gray, dots, screen):
        self.width = width
        self.height = height
        self.max_characters = max_characters
        self.screen = screen
        self.font = font
        self.white = white
        self.gray = gray
        self.dots = dots
    
    def draw_screen(self, prompt_text, input_text, display_default_underscores):
        text_width, text_height = prompt_text.get_size()

        # Calculate the position to center the text
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        # Display the default underscores if needed
        if display_default_underscores:
            underscore_text = self.font.render("_" * (self.max_characters - len(input_text)), True, self.white)
            underscore_x = (self.width - underscore_text.get_width()) // 2
            underscore_y = y / 2 + text_height + 10
            self.screen.blit(underscore_text, (underscore_x, underscore_y))
        
        # Display the input_text
        input_text_rendered = self.font.render(input_text, True, self.white)
        input_text_x = (self.width - input_text_rendered.get_width()) // 2
        input_text_y = y / 2 + text_height + 10
        self.screen.blit(input_text_rendered, (input_text_x, input_text_y))

        for i in range(len(self.dots)):
            dot_color = Constants.gray  # Default color
            if i == (pygame.time.get_ticks() // 500) % len(self.dots):
                dot_color = Constants.white  # Make the current dot glow

            pygame.draw.circle(Constants.screen, dot_color, self.dots[i], Constants.dot_radius)

        return self.screen
        
