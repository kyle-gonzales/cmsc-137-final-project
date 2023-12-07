import pygame

from constants import Constants

SCREEN_WIDTH = Constants.WIDTH - 700
SCREEN_HEIGHT = Constants.HEIGHT + 200

class Slider:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.x = (SCREEN_WIDTH  - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.range_width = SCREEN_WIDTH - self.width
        self.position = 50
        self.speed = 0.5
        self.direction = 1
        self.moving = True

    def draw(self, screen):
        fill_width = SCREEN_WIDTH - self.width - self.position
        x_offset = (Constants.WIDTH - Constants.WIDTH + 700) // 2

        filled_slider_rect = pygame.Rect(self.position + x_offset, self.y, fill_width, self.height)
        pygame.draw.rect(screen, Constants.MAROON, filled_slider_rect)

        unfilled_slider_rect = pygame.Rect(x_offset, self.y, self.position, self.height)
        pygame.draw.rect(screen, Constants.GOLD, unfilled_slider_rect)

        pygame.draw.rect(screen, Constants.GREEN, (x_offset, self.y, self.range_width, self.height), 5)
        pygame.draw.rect(screen, Constants.BLACK, (self.x + x_offset - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, Constants.GOLD, (self.x + x_offset , self.y, self.width, self.height))

        font = pygame.font.Font(None, 25) 
        font2 = pygame.font.Font(None, 36) 
        text = font.render("Power: " + str(self.get_value()), True, Constants.WHITE) 
        text2 = font2.render("CLICK TO RELEASE", True, Constants.WHITE) 
        text_rect = text.get_rect(center=(Constants.WIDTH // 2 -10, self.y + self.height + 20)) 
        text_rect2 = text.get_rect(center=(Constants.WIDTH // 2 -90, self.y + self.height + 40)) 
        screen.blit(text, text_rect) 
        screen.blit(text2, text_rect2) 

    def update_position(self):
        self.position += self.speed * self.direction

    def get_value(self):
        value_range = 150 - 50
        ratio = (self.position / self.range_width)
        return int(50 + (ratio * value_range))

class SliderRun:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.slider = Slider()
        self.lightning = pygame.image.load(Constants.IMAGE_PATH + "lightning.png")
        self.lightning_x = (Constants.WIDTH - self.lightning.get_width()) // 2 -125
        self.lightning_y = SCREEN_HEIGHT // 2 - self.lightning.get_height() // 2

    def run(self):
        running = True
        while running:
            self.screen.fill(Constants.BLACK)
            running = self.handle_events()

            if self.slider.moving:
                self.slider.update_position()

                if self.slider.position <= 0 or self.slider.position >= SCREEN_WIDTH - self.slider.width:
                    self.slider.direction *= -1

            if self.slider.position < 0:
                self.slider.position = 0
            elif self.slider.position > SCREEN_WIDTH - self.slider.width:
                self.slider.position = SCREEN_WIDTH - self.slider.width

            self.slider.x = self.slider.position

            self.slider.draw(self.screen)
            self.screen.blit(self.lightning, (self.lightning_x, self.lightning_y))

            pygame.display.flip()

        slider_value = self.slider.get_value()
        return slider_value

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.slider.moving = False
        return True
    
def main():
    slider = SliderRun()
    value = slider.run() 
    return value

if __name__ == "__main__":
    # main()
    print("Power Value:", main())