""" Initiate the game module """

import pygame

from .__main__ import main

# friendly wait message
print("Sit tight, loading the game...", flush=True)

# initialise pygame
pygame.init()

# export the main function
__all__ = ["main"]
