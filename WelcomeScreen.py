import pygame
import sys

from Constants import Constants
from Background import Background
from Button import Button
from ChooseName import ChooseName
from Cannon import Cannon
from Movement import Movement
from CannonMovement import CannonMovement

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

                        #player name
                        print(Constants.input_text)
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
                    clicked_button_path = button.is_clicked(event.pos)

                    if clicked_button_path == "Assets/dutete_button.png":
                        # Reset the button and set background for Dutete screen
                        button = Button(Constants.dutete_button_paths, Constants.button_width, Constants.button_height, Constants.button_spacing, Constants.screen)
                        bg = Background(Constants.dutete_fam_bg, Constants.screen)
                        Constants.dutete_screen = True
                        Constants.narcos_screen = False 
   
                    #if dutete button is hovered it creates instantiation needed for the cannon movement
                    elif clicked_button_path == "Assets/dutete_button_hovered.png":
                        Constants.family_name = "Dutete"
                        Constants.choose_family_screen = False
                        Constants.dutete_screen = False
                        Constants.game_proper_screen = True

                        # Set background for Dutete family
                        bg = Background(Constants.family_images[Constants.family_name]["bg"], Constants.screen)

                        # Set images for Dutete family
                        barrel_image = Cannon(Constants.family_images[Constants.family_name]["barrel"], 1.75)
                        stand_image = Cannon(Constants.family_images[Constants.family_name]["stand"], 1.5)
                        cannon_image = Cannon(Constants.family_images[Constants.family_name]["cannon"], 1.75)
                        barrel_rotate = Movement(barrel_image.scale_image(), Constants.width, Constants.height)
                        
                    elif clicked_button_path == "Assets/narcos_button.png":
                        # Reset the button and set background for Narcos screen
                        button = Button(Constants.narcos_button_paths, Constants.button_width, Constants.button_height, Constants.button_spacing, Constants.screen)
                        bg = Background(Constants.narcos_fam_bg, Constants.screen)
                        Constants.narcos_screen = True
                        Constants.dutete_screen = False
                    
                    #if narcos button is choses it creates instantiation needed for the cannon movement
                    elif clicked_button_path == "Assets/narcos_button_hovered.png":
                        Constants.family_name = "Narcos"
                        Constants.choose_family_screen = False
                        Constants.dutete_screen = False
                        Constants.game_proper_screen = True

                        # Set background for Narcos family
                        bg = Background(Constants.family_images[Constants.family_name]["bg"], Constants.screen)

                        # Set images for Narcos family
                        barrel_image = Cannon(Constants.family_images[Constants.family_name]["barrel"], 1.75)
                        stand_image = Cannon(Constants.family_images[Constants.family_name]["stand"], 1.5)
                        cannon_image = Cannon(Constants.family_images[Constants.family_name]["cannon"], 1.75)
                        barrel_rotate = Movement(barrel_image.scale_image(), Constants.width, Constants.height) 
                            
            elif Constants.game_proper_screen:
                if event.button == 1:
                    barrel_rotate.rotate = False
                    rotation_angle = barrel_rotate.get_rotation_angle()
                    print(rotation_angle)

        #from welcome screen to enter name screen
        if pygame.time.get_ticks() - current_time >= 2000 and Constants.welcome_screen:
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
    
    if Constants.game_proper_screen:
        if barrel_rotate.rotate:
        #Rotate from 0 to 90: 90 to 0:
            rotated_image, rotated_image_rect = barrel_rotate.rotate_barrel()

        cannons = CannonMovement(rotated_image, rotated_image_rect, stand_image.scale_image(), cannon_image.flip_image(), Constants.width, Constants.height)
        cannons.draw(Constants.screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)
