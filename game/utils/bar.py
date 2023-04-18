"""Implements Bar UI"""
import pygame

from game.utils import Text


# pylint:disable=too-few-public-methods
class HealthBar:
    """Shows the healthbar"""

    def __init__(self, entity):
        self.front_color = (255, 0, 0)
        self.back_color = (255, 255, 255)
        self.font_color = "black"
        self.font = "pokemon-solid"
        self.entity = entity
        self.max_health = entity.max_health

    def draw(self, screen, top_left, width, height):
        """draw the healthbar"""

        health = self.entity.attributes.health
        pygame.draw.rect(
            screen,
            self.back_color,
            (top_left[0] - 2, top_left[1] - 2, width + 4, height + 4),
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
            50 + top_left[0],
            12 + top_left[1],
            14,
            self.font_color,
        ).blit_into(screen)
        Text(
            f"Lv. {self.entity.level}",
            "pokemon-solid",
            top_left[0] - 50,
            12 + top_left[1],
            14,
            "white",
        ).blit_into(screen)
