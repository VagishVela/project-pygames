""" Initiate the game module """

import pygame

from .__main__ import main
from .utils.text import register_font

# friendly wait message
print("Sit tight, loading the game...", flush=True)

# initialise pygame
pygame.init()

# register the fonts
register_font("pokemon-hollow", "assets/Pokemon Hollow.ttf", 23)
register_font("pokemon-solid", "assets/Pokemon Solid.ttf", 23)

# export the main function
__all__ = ["main"]
