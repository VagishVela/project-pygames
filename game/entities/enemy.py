"""This module contains the Enemy class"""

import pygame.image
from pygame import Surface
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Class for the enemy"""

    def __init__(self, scale=(32, 32)):
        """Initialize the enemy"""
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/enemy.png"), scale
        )
        self.scale = scale
        self.rect = self.image.get_rect()
        self.abilities = {
            "attack": 5,
            "damage": 30,
            "health": 70,
        }
        self.max_health = 70
        self.details = ["I am Quantalocus.", "A deadly Alien with no special abilities"]
        self.visible = True
        self.name = "Alien"

        self.attacks = [
            {"name": "Quick Attack", "power": 10},
            {"name": "Power Attack", "power": 20},
            {"name": "Super Attack", "power": 30},
            {"name": "Mega Attack", "power": 40},
        ]

    def take_damage(self, p_ability):
        """Take damage from the player"""
        self.abilities["health"] -= (
            p_ability["attack"] * (100 - self.abilities["damage"]) / 100
        )
        # Return true if the enemy dies
        return self.abilities["health"] <= 0

    def draw(self, screen: Surface, pos_x, pos_y, scale=None):
        """Draw the enemy"""
        if scale is not None and self.scale != scale:
            self.scale = scale
            self.image = pygame.transform.scale(self.image, scale)

        screen.blit(self.image, (pos_x, pos_y))
