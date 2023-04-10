""" This module implements the Text class """

from typing import Iterable

import pygame

from game._common import ColorValue


# pylint: disable=too-many-instance-attributes, too-many-arguments
class Text:
    """Class to handle text"""

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
            font: str | bytes | Iterable[str | bytes],
            x: float | int,
            y: float | int,
            size: int,
            color: ColorValue,
            bg_color: ColorValue = None,
            align: str = "center",
            style: Iterable[str] = (),
    ):
        self.surface = None
        self.text: str = text
        self.x: float | int = x
        self.y: float | int = y
        self.size = size
        self.color: ColorValue = color
        self.bg_color: ColorValue = bg_color
        self.align = align
        self.style = style
        self.font = font

    def render(self, antialias: bool = True) -> pygame.Surface:
        """
        Render a surface with the text on it.

        :param antialias: For performance reasons, it is good to know what type of image will be
            used. If antialiasing is not used, the return image will always be an 8-bit image with a
            two-color palette. Antialiased images are rendered to 24-bit RGB images. If the
            background is transparent a pixel alpha will be included.
            :return: The rendered surface
        """

        if isinstance(self.font, pygame.font.FontType):
            font = self.font
        else:
            font = pygame.font.Font = pygame.font.SysFont(self.font, self.size)

        font.strikethrough = "strikethrough" in self.style
        font.italic = "italic" in self.style
        font.bold = "bold" in self.style
        font.underline = "underline" in self.style

        self.surface: pygame.Surface = font.render(
            self.text, antialias, self.color, self.bg_color
        )
        return self.surface

    def blit_into(self, surface: pygame.Surface):
        """
        Blit the text into the provided surface.

        :param surface: Destination surface
        :return:
        """

        if not self.surface:
            self.surface = self.render()

        match self.align:
            case "right":
                surface.blit(
                    self.surface, (self.x, self.y - self.surface.get_height() / 2)
                )
            case "left":
                surface.blit(
                    self.surface,
                    (
                        self.surface.get_width() / 2 - self.x,
                        self.y - self.surface.get_height() / 2,
                    ),
                )
            case "center":
                surface.blit(
                    self.surface,
                    (
                        self.x - self.surface.get_width() / 2,
                        self.y - self.surface.get_height() / 2,
                    ),
                )
            case _:
                surface.blit(self.surface, (self.x, self.y))
