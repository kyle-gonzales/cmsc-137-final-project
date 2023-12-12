import pygame
import sys

from WelcomeScreenHandler import WelcomeScreenHandler

pygame.init()

def welcome_screen():


    # game loop
    clock = pygame.time.Clock()

    game = WelcomeScreenHandler()
    choosen_family = ""

    stage_screen = "Welcome Screen"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if stage_screen == "Welcome Screen":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #tries to connect to the server
                        connected = game.start_connect()
                        if connected:
                            stage_screen = "Enter Name Screen"
                        #if not connected, stays on the welcome screen
                        else:
                            pass

            elif stage_screen == "Enter Name Screen":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_name = game.enter_name()
                        stage_screen = "Choose Family Screen"
                    elif event.key == pygame.K_BACKSPACE:
                        game.remove_character()
                    else:
                        game.add_character(event)

            elif stage_screen == "Choose Family Screen":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        chosen_family = game.choose_family(event)
                        if chosen_family != "":
                            stage_screen = "Game Proper Screen"

            elif stage_screen ==  "Game Proper Screen":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        angle = game.get_angle()
                        print(angle)


        game.display_background()

        if stage_screen == "Enter Name Screen":
            game.display_name()

        if stage_screen == "Choose Family Screen":
            game.draw_buttons()

        if stage_screen == "Game Proper Screen":
            game.display_cannon()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

welcome_screen()