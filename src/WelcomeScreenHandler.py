import sys

import pygame

from Background import Background
from Button import Button
from Cannon import Cannon
from CannonMovement import CannonMovement
from ChooseName import ChooseName
from constants import Constants
from Movement import Movement


# functions needed for the welcome screen to the game proper
class WelcomeScreenHandler:
    def __init__(self):
        # Constants = Constants()
        self.player_name = ""
        self.setup_objects()
        self.family_name = ""
        self.bg = Background(Constants.welcome_screen_bg, Constants.screen)
        self.barrel_image = None
        self.stand_image = None
        self.cannon_image = None
        self.barrel_image = None
        self.rotated_image = None
        self.rotated_image_rect = None

    def setup_objects(self):
        self.chooseName = ChooseName(
            Constants.WIDTH,
            Constants.HEIGHT,
            Constants.max_characters,
            Constants.font,
            Constants.white,
            Constants.gray,
            Constants.dots,
            Constants.screen,
        )
        self.button = Button(
            Constants.button_paths,
            Constants.button_width,
            Constants.button_height,
            Constants.button_spacing,
            Constants.screen,
        )
    
    def connected(self):
        self.bg = Background(Constants.choose_name_bg, Constants.screen)


    # returns the player name if not empty
    def enter_name(self):
        if self.player_name != "":
            self.bg = Background(Constants.choose_fam_bg, Constants.screen)

            return self.player_name
        else:
            print("Player name is blank")

    # removes character from player name
    def remove_character(self):
        self.player_name = self.player_name[:-1]
        if len(self.player_name) > Constants.max_characters:
            self.player_name = self.player_name[: Constants.max_characters]

    # adds character to player name
    def add_character(self, event):
        if len(self.player_name) < Constants.max_characters:
            self.player_name += event.unicode

    # returns family chosen
    def choose_family(self, event):
        clicked_button_path = self.button.is_clicked(event.pos)

        if clicked_button_path == "../Assets/dutete_button.png":
            # Reset the button and set background for Dutete screen
            self.button = Button(
                Constants.dutete_button_paths,
                Constants.button_width,
                Constants.button_height,
                Constants.button_spacing,
                Constants.screen,
            )
            self.bg = Background(Constants.dutete_fam_bg, Constants.screen)

        # return dutete family
        elif clicked_button_path == "../Assets/dutete_button_hovered.png":
            self.family_name = "Dutete"

            self.create_family_instance(self.family_name)

        elif clicked_button_path == "../Assets/narcos_button.png":
            # Reset the button and set background for Narcos screen
            self.button = Button(
                Constants.narcos_button_paths,
                Constants.button_width,
                Constants.button_height,
                Constants.button_spacing,
                Constants.screen,
            )
            self.bg = Background(Constants.narcos_fam_bg, Constants.screen)

        # return narcos family
        elif clicked_button_path == "../Assets/narcos_button_hovered.png":
            self.family_name = "Narcos"

            self.create_family_instance(self.family_name)

        return self.family_name

    def player_two_family(self, chosen_family):
        self.family_name = chosen_family
        self.create_family_instance(self.family_name)

    # create cannon object instance for the chosen family
    def create_family_instance(self, family_name):
        self.bg = Background(
            Constants.family_images[family_name]["bg"], Constants.screen
        )

        # set family chosen
        self.barrel_image = Cannon(Constants.family_images[family_name]["barrel"], 1.75)
        self.stand_image = Cannon(Constants.family_images[family_name]["stand"], 1.5)
        self.cannon_image = Cannon(Constants.family_images[family_name]["cannon"], 1.75)
        self.barrel_rotate = Movement(
            self.barrel_image.scale_image(), Constants.WIDTH, Constants.HEIGHT
        )

    # display cannon object
    def display_cannon(self):
        if self.barrel_rotate.rotate:
            (
                self.rotated_image,
                self.rotated_image_rect,
            ) = self.barrel_rotate.rotate_barrel()

        cannons = CannonMovement(
            self.rotated_image,
            self.rotated_image_rect,
            self.stand_image.scale_image(),
            self.cannon_image.flip_image(),
            Constants.WIDTH,
            Constants.HEIGHT,
        )
        cannons.draw(Constants.screen)

    # returns rotation angle of cannon
    def get_angle(self):
        self.barrel_rotate.rotate = False
        rotation_angle = self.barrel_rotate.get_rotation_angle()

        return rotation_angle

    # draws button for choose family screen
    def draw_buttons(self):
        self.button.draw(Constants.screen)

    # displays background
    def display_background(self):
        Constants.screen.blit(self.bg.scale_image(), (0, 0))

    # displays name
    def display_name(self):
        self.chooseName.draw_screen(
            Constants.prompt_text,
            self.player_name,
            Constants.display_default_underscores,
        )
