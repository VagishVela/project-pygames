""" This module implements the Button class """

from typing import Iterable, Callable

import pygame

from game._common import ColorValue
from game.utils import Text


class Button:
    """Class to work with buttons"""

    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        text: str = "Button",
        module: str = None,
        screen: str = None,
        on_click: Callable = None,
        once: bool = False,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
        self.once = once
        self.text = text
        self.module = module
        self.screen = screen

        self.fill_colors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(
            self.x - self.width / 2, self.y - self.height / 2, self.width, self.height
        )
        self.already_pressed = False

    def update(self):
        """Process mouse input"""

        pygame.event.pump()  # Update internal state of pygame

        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors["normal"])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors["pressed"])
                if self.once:
                    self.on_click(self)
                elif not self.already_pressed:
                    self.on_click(self)
                    self.already_pressed = True
            else:
                self.already_pressed = False

    def blit_into(
        self,
        surface: pygame.Surface,
        font: str | bytes | Iterable[str | bytes] = None,
        size: int = 20,
        color: ColorValue = (20, 20, 20),
    ):
        """
        Blit the text into the provided surface.

        :param surface: Destination surface
        :param font: Desired font for the buttons. Uses the pygame default if None.
        :param size: Font size
        :param color: Font color
        :return:
        """
        if not font:
            font = pygame.font.get_default_font()
        Text(
            self.text,
            font,
            self.button_rect.width / 2,
            self.button_rect.height / 2,
            size,
            color,
        ).blit_into(self.button_surface)
        surface.blit(self.button_surface, self.button_rect)
