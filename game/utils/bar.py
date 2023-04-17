"""Implements Bar UI"""
import pygame

from game.utils import Text


# pylint:disable=too-few-public-methods
class HealthBar:
    """Shows the healthbar"""

    def __init__(self, max_health: int):
        self.max_health = max_health
        self.front_color = (255, 0, 0)
        self.back_color = (255, 255, 255)
        self.font_color = "black"
        self.font = "pokemon-solid"

    def draw(self, screen, health, top_left, width, height):
        """draw the healthbar"""

        pygame.draw.rect(
            screen, self.back_color, (top_left[0], top_left[1], width, height)
        )
        pygame.draw.rect(
            screen,
            self.front_color,
            (
                top_left[0],
                top_left[1],
                width * health / self.max_health,
                height,
            ),
        )
        Text(
            f"Health: {health}",
            self.font,
            60 + top_left[0],
            13 + top_left[1],
            15,
            self.font_color,
        ).blit_into(screen)
