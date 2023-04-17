"""This module contains the Player class"""
from dataclasses import dataclass

import pygame.image
from pygame import Surface
from pygame.sprite import Sprite


@dataclass
class PlayerAttributes:
    """Represents player attributes"""

    health: int
    max_health: int


class Player(Sprite):
    """Class for the player"""

    def __init__(self):
        """Initialize the player"""
        super().__init__()
        self.scale = (64, 96)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/player.png"), self.scale
        ).convert_alpha()
        self.pos = self.image.get_width() / 2, self.image.get_height() / 2
        self.rect = self.image.get_rect()
        self.attributes = PlayerAttributes(
            health=100,
            max_health=100,
        )
        self.max_health = 100
        self.has_shield = True
        self.dodging = False
        self.name = "Player"
        self.is_ghost = False

        self.attacks = [
            {"name": "Quick Attack", "power": 10},
            {"name": "Power Attack", "power": 20},
            {"name": "Super Attack", "power": 30},
            {"name": "Mega Attack", "power": 40},
        ]

    def draw(self, screen: Surface, pos=None, scale=None):
        """Draw the player"""
        if scale is not None and self.scale != scale:
            self.scale = scale
            self.image = pygame.transform.scale(self.image, scale)

        if self.attributes.health <= 0:
            # ghost mode!
            if not self.is_ghost:
                self.image.set_alpha(120)
                self.is_ghost = True
        elif self.is_ghost:
            self.is_ghost = False
            self.image.set_alpha(255)

        if pos is None:
            screen.blit(
                self.image,
                (
                    screen.get_width() / 2 - self.pos[0],
                    screen.get_height() / 2 - self.pos[1],
                ),
            )
        else:
            screen.blit(self.image, pos)

        if self.dodging:
            pygame.draw.circle(
                screen, pygame.Color(255, 255, 255, 50), pos, self.rect.w * 1.5
            )
