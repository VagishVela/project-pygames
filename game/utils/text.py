""" This module implements the Text class """
import importlib
from typing import Iterable, Optional

import pygame
from pygame import Surface
from pygame.font import FontType

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


FONT_DICT: dict[str, Font] = {}


def find_font(name: str, size: int) -> FontType:
    """finds a font from string"""
    # see if name is in FONT_DICT else use SysFont
    if name in FONT_DICT:
        if FONT_DICT[name].font_size != size:
            FONT_DICT[name].set_size(size)
        return FONT_DICT[name]
    return pygame.font.SysFont("name", size)


def register_font(name: str, file: str, size: int):
    """registers a font"""
    if name in FONT_DICT:
        raise ValueError(f"{name}: Name already in use")
    FONT_DICT[name] = Font(file, size)


def unregister_font(name: str):
    """unregisters a font"""
    if name in FONT_DICT:
        FONT_DICT.pop(name)


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
        font: str,
        x: NumType,
        y: NumType,
        size: NumType,
        color: ColorValue,
        bg_color: Optional[ColorValue] = None,
        align: str = "center",
        style: Iterable[str] = (),
    ):
        self.text: str = text
        self.x: NumType = x
        self.y: NumType = y
        self.size = int(size)
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

        font = find_font(self.font, self.size)
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


class DisapearingText(Text):
    """Text that disappears after a while"""

    def __init__(
        self,
        text: str,
        font: str,
        x: NumType,
        y: NumType,
        size: NumType,
        color: ColorValue,
        time: int,
        *args,
        **kwargs,
    ):
        super().__init__(text, font, x, y, size, color, *args, **kwargs)
        self.time = time
        self.visible = False
        self.wait = False
        self.event = getattr(
            importlib.import_module("game.custom_event"), "TEXT_DISAPEAR"
        )

    def blit_into(self, surface: Surface):
        if not self.wait:
            # set text to disapear after `time`
            self.event.wait(self.time)
            self.wait = True
            self.visible = True
        if self.event.get():
            self.visible = False

        if self.visible:
            super().blit_into(surface)
