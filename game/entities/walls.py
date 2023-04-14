"""Walls module."""
import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.config import TILE_SIZE


class Wall(Sprite):
    """Class for the wall"""

    def __init__(self, x, y):
        """Initialize the wall"""
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/wall.png"), (TILE_SIZE, TILE_SIZE)
        )
        self.pos = x, y
        self.rect = self.image.get_rect()
        self.visible = True

    def draw(self, screen: Surface):
        """Draw the wall"""
        screen.blit(self.image, self.pos)
