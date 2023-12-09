import pygame
import sys

from power import Power, SpecialPower
from constants import Constants
from player import Player

class PowerSelectionMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        pygame.display.set_caption("Selection Menu")
        self.menu_width = 690
        self.menu_height = 250
        self.button_width = 100
        self.button_height = 120
        self.spacing = 20

        self.menu_rect = pygame.Rect(0, Constants.HEIGHT - self.menu_height, self.menu_width, self.menu_height)
        self.option_rects = []
        self.selected_options = 0

        self.player = Player(name= "Player", family= "Marcos") #will modify for the actual data from self.player.family
        # self.player = [player.name for player in self.player.name + self.player.family]
 
        self.player.init_powers()
        self.option_name = [power.name for power in self.player.basic_powers + self.player.special_powers]
        self.option_cost = [str(power.cost) for power in self.player.basic_powers + self.player.special_powers]
        self.option_damage = [str(power.damage) for power in self.player.basic_powers + self.player.special_powers]
        self.coins = self.player.corruption_points

        for idx, text in enumerate(self.option_name):
            x_pos = self.spacing + idx * (self.button_width + 10)
            y_pos = Constants.HEIGHT - self.menu_height + 3 * self.spacing
            button_rect = pygame.Rect(x_pos, y_pos, self.button_width, self.button_height)
            self.option_rects.append(button_rect)

        self.power_images = {}
        for power_name, image_filename in Constants.POWER_IMAGE_NAME.items():
            image = pygame.image.load(Constants.IMAGE_PATH + image_filename).convert_alpha()
            self.power_images[power_name] = pygame.transform.scale(image, (self.button_width, self.button_height))

    def draw_text(self, text, color, x, y, center=False, font_size=20):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def run_menu(self):
        running = True
        selected_power = ""

        while running:
            self.screen.fill(Constants.BLACK)
            pygame.draw.rect(self.screen, Constants.MAROON, self.menu_rect, border_top_right_radius=10)
            pygame.draw.rect(self.screen, Constants.GOLD, self.menu_rect, 5, border_top_right_radius=10)
            pygame.draw.rect(self.screen, Constants.MAROON, (0, Constants.HEIGHT - self.menu_height + 5, 5, self.menu_height))  # Left side
            pygame.draw.rect(self.screen, Constants.MAROON, (0, Constants.HEIGHT - 5, self.menu_width - 5, 5))  # Bottom side
            select_button = pygame.draw.rect(self.screen, Constants.GOLD, (Constants.WIDTH // 2 - 185, Constants.HEIGHT - self.menu_height + 195, 100, 40), border_radius=5)

            for idx, text_rect in enumerate(self.option_rects):
                pygame.draw.rect(self.screen, Constants.DARKERMAROON, text_rect, border_radius=10)
                white_rect = pygame.draw.rect(self.screen, Constants.WHITE, (text_rect.x + 10, text_rect.y + 10  , 80, 50), border_radius=10)
                
                power_name = self.option_name[idx]
                if power_name in self.power_images:
                    image = self.power_images[power_name]
                    scaled_image = pygame.transform.scale(image, (white_rect.width - 20, white_rect.height))
                    image_x = text_rect.x + 10 + (white_rect.width - scaled_image.get_width()) // 2
                    image_y = text_rect.y + 10 + (white_rect.height - scaled_image.get_height()) // 2
                    self.screen.blit(scaled_image, (image_x, image_y))
                
                self.draw_text(self.option_name[idx], Constants.WHITE, text_rect.x + self.button_width // 2, text_rect.y + 75, center=True, font_size=14)
                self.draw_text(self.option_cost[idx], Constants.WHITE, text_rect.x + self.button_width // 2, text_rect.y + 90, center=True, font_size=20)
                self.draw_text(self.option_damage[idx], Constants.WHITE, text_rect.x + self.button_width // 2, text_rect.y + 105, center=True, font_size=24)
            
            self.draw_text("Powers", Constants.WHITE, 20, Constants.HEIGHT - self.menu_height + 20, font_size=32)
            self.draw_text(f"Corruption Points: {self.coins}", Constants.WHITE, self.menu_width - 170, Constants.HEIGHT - self.menu_height + 20, font_size=20)
            self.draw_text("Select", Constants.BLACK, self.menu_width // 2, Constants.HEIGHT - self.menu_height + 215, center=True, font_size= 30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for idx, rect in enumerate(self.option_rects):
                            if rect.collidepoint(mouse_pos) and idx != self.selected_options:
                                self.selected_options = idx
                                for r in self.option_rects:
                                    r.width = self.button_width
                                    r.height = self.button_height
                                print(f"Clicked on option: {self.option_name[idx]}")
                                self.option_rects[idx].inflate_ip(5, 5)
                                break
                        pygame.display.update()
                            
                        if select_button.collidepoint(mouse_pos):
                            selected_power = self.option_name[self.selected_options]
                            select_button.inflate_ip(5, 5)
                            return selected_power 

        pygame.quit()
        sys.exit()

def main():
    menu = PowerSelectionMenu()
    selected_power = menu.run_menu()
    print("Power Selected:", selected_power)

if __name__ == "__main__":
    main()