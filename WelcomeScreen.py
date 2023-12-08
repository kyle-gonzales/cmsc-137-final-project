import pygame
import sys

from Constants import Constants
from Background import Background
from Button import Button
from ChooseName import ChooseName

pygame.init()

#welcome screen background
bg = Background(Constants.welcome_screen_bg, Constants.screen)

#initialize buttons
button = Button(Constants.button_paths, Constants.button_width, Constants.button_height, Constants.button_spacing, Constants.screen)

# game loop
clock = pygame.time.Clock()

#switch screen timer
current_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if Constants.choose_name_screen:
                if event.key == pygame.K_RETURN:
                    #if name is not empty, proceed to choose family: This will be subjected to change once the waiting for another player is done.
                    if Constants.input_text != "":
                        #choose family background
                        bg = Background(Constants.choose_fam_bg, Constants.screen)
                        Constants.choose_family_screen = True
                        Constants.choose_name_screen = False
                    else:
                        print("User entered:", Constants.input_text)
                elif event.key == pygame.K_BACKSPACE:
                    #remove last character
                    Constants.input_text = Constants.input_text[:-1]
                    if len(Constants.input_text) > Constants.max_characters:
                        Constants.input_text = Constants.input_text[:Constants.max_characters]
                else:
                    #add characters while checking for max chars
                    if len(Constants.input_text) < Constants.max_characters:
                        Constants.input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            #if in choose family screen
            if Constants.choose_family_screen:
                if event.button == 1:  # Left mouse button
                    if (button.is_clicked(event.pos)) == "Assets/duterte_button.png":
                        button = Button(Constants.duterte_button_paths, Constants.button_width, Constants.button_height, Constants.button_spacing, Constants.screen)
                        bg = Background(Constants.duterte_fam_bg, Constants.screen)
                    elif (button.is_clicked(event.pos)) == "Assets/marcos_button.png":
                        button = Button(Constants.marcos_button_paths, Constants.button_width, Constants.button_height, Constants.button_spacing, Constants.screen)
                        bg = Background(Constants.marcos_fam_bg, Constants.screen)

        #from welcome screen to enter name screen
        if pygame.time.get_ticks() - current_time >= 2000 and not Constants.choose_family_screen:
            Constants.choose_name_screen = True
            Constants.welcome_screen = False

            #change the screen to name screen
            bg = Background(Constants.choose_name_bg, Constants.screen)
            chooseName = ChooseName(Constants.width, Constants.height, Constants.max_characters, Constants.font, Constants.white, Constants.gray, Constants.dots, Constants.screen)

    Constants.screen.blit(bg.scale_image(), (0,0))

    #draw screen for choose name
    if Constants.choose_name_screen:
        chooseName.draw_screen(Constants.prompt_text, Constants.input_text, Constants.display_default_underscores)

    #draw buttons for choose family
    if Constants.choose_family_screen:
        button.draw(Constants.screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)
