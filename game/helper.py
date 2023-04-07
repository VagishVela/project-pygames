""" Contains helper functions and classes to speed up development"""

from typing import Iterable, Callable

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


class Button:
    """Class to work with buttons"""

    def __init__(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        text: str = "Button",
        onclick: Callable = None,
        once: bool = False,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick = onclick
        self.once = once
        self.text = text

        self.fill_colors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.already_pressed = False

    def update(self):
        """Process mouse input"""

        # TODO: functionality doesn't work, needs investigation

        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors["normal"])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors["pressed"])
                if self.once:
                    self.onclick()
                elif not self.already_pressed:
                    self.onclick()
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
