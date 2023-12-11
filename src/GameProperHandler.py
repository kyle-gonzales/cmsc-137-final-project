from Background import Background
from Cannon import Cannon
from CannonMovement import CannonMovement
from constants import Constants
from Movement import Movement


class GameProperHandler:
    def __init__(self):
        self.player_name = ""
        self.family_name = ""
        self.bg = None
        self.barrel_image = None
        self.stand_image = None
        self.cannon_image = None
        self.barrel_image = None
        self.rotated_image = None
        self.rotated_image_rect = None

    #create cannon object instance for the chosen family
    def player_two_family(self, chosen_family):
        self.family_name = chosen_family
        self.create_cannon_instance(self.family_name)

    # create cannon object instance for the chosen family
    def create_cannon_instance(self, family_name):
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
    
    # displays background
    def display_background(self):
        Constants.screen.blit(self.bg.scale_image(), (0, 0))