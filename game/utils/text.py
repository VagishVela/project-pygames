""" This module implements the Text class """

from typing import Iterable, Optional

import pygame
from pygame import Surface

from game.common_types import ColorValue, NumType


class Font(pygame.font.Font):
    """Expand font functionality"""

    def __init__(self, name, size):
        super().__init__(name, size)
        self.name = name
        self.font_size = size

    # pylint: disable=unnecessary-dunder-call
    def set_size(self, size):
        """re-initiate with a different font size"""
        if size != self.font_size:
            self.__init__(self.name, size)


# pylint: disable=too-many-instance-attributes, too-many-arguments
class Text:
    """Class to handle text"""

    RIGHT = "right"
    CENTER = "center"
    LEFT = "left"

    __slots__ = [
        "font",
        "text",
        "x",
        "y",
        "color",
        "size",
        "bg_color",
        "surface",
        "align",
        "style",
    ]

    def __init__(
        self,
        text: str,
        font: str | bytes | Iterable[str | bytes] | pygame.font.FontType,
        x: NumType,
        y: NumType,
        size: int,
        color: ColorValue,
        bg_color: Optional[ColorValue] = None,
        align: str = "center",
        style: Iterable[str] = (),
    ):
        self.text: str = text
        self.x: NumType = x
        self.y: NumType = y
        self.size: int = size
        self.color: ColorValue = color
        self.bg_color: Optional[ColorValue] = bg_color
        self.align: str = align
        self.style = style
        self.font = font

    def render(self, antialias: bool = True) -> Surface:
        """
        Render a surface with the text on it.

        :param antialias: For performance reasons, it is good to know what type of image will be
            used. If antialiasing is not used, the return image will always be an 8-bit image with a
            two-color palette. Antialiased images are rendered to 24-bit RGB images. If the
            background is transparent a pixel alpha will be included.
            :return: The rendered surface
        """

        if isinstance(self.font, Font):
            font = self.font
            if font.font_size != self.size:
                font.set_size(self.size)
                self.font = font
        elif isinstance(self.font, pygame.font.Font):
            # fallback
            font = self.font
        else:
            font = pygame.font.SysFont(self.font, self.size)

        font.strikethrough = "strikethrough" in self.style
        font.italic = "italic" in self.style
        font.bold = "bold" in self.style
        font.underline = "underline" in self.style

        surface: Surface = font.render(self.text, antialias, self.color, self.bg_color)
        return surface

    def blit_into(self, surface: Surface):
        """
        Blit the text into the provided surface.

        :param surface: Destination surface
        :return:
        """

        text_surface = self.render()

        match self.align:
            case "right":
                surface.blit(
                    text_surface, (self.x, self.y - text_surface.get_height() / 2)
                )
            case "left":
                surface.blit(
                    text_surface,
                    (
                        text_surface.get_width() / 2 - self.x,
                        self.y - text_surface.get_height() / 2,
                    ),
                )
            case "center":
                surface.blit(
                    text_surface,
                    (
                        self.x - text_surface.get_width() / 2,
                        self.y - text_surface.get_height() / 2,
                    ),
                )
            case _:
                surface.blit(text_surface, (self.x, self.y))
