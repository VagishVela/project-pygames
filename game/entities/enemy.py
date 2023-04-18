"""This module contains the Enemy class"""

import pygame.image
from pygame import Surface
from pygame.sprite import Sprite

from game.entities.player import PlayerAttributes


class Enemy(Sprite):
    """Class for the enemy"""

    def __init__(self, scale=(64, 64)):
        """Initialize the enemy"""
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/enemy.png"), scale
        )
        self.scale = scale
        self.rect = self.image.get_rect()
        self.details = ["I am Quantalocus.", "A deadly Alien with no special abilities"]
        self.visible = True
        self.name = "Alien"

        self.attacks = [
            {"name": "Quick Attack", "power": 10},
            {"name": "Power Attack", "power": 20},
            {"name": "Super Attack", "power": 30},
            {"name": "Mega Attack", "power": 40},
        ]
        # base case
        self.attributes = PlayerAttributes(
            health=40,
            xp=1,  # base xp received if this enemy is killed
        )
        self.max_health = 40  # base

    @property
    def level(self):
        """get enemy level"""
        # based on a formula i derived from observation
        try:
            return int(0.0222386 * (self.max_health**0.994036 - 40) ** 0.826446) + 1
        except TypeError:
            return 0

    @staticmethod
    def calculate_max_health(player_hp):
        """get max health"""
        return int((player_hp - 60) ** 1.006)

    def set_attributes(self, player):
        """set the enemy attributes"""
        self.max_health = self.calculate_max_health(player.max_health)
        self.attributes.health = self.max_health

    def draw(self, screen: Surface, pos_x, pos_y, scale=None):
        """Draw the enemy"""
        if scale is not None and self.scale != scale:
            self.scale = scale
            self.image = pygame.transform.scale(self.image, scale)

        screen.blit(self.image, (pos_x, pos_y))
