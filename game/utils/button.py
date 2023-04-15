""" This module implements the Button class """
import importlib
import typing
from typing import Optional, Iterable, Callable

import pygame
from pygame import Surface, Rect

from game.common_types import ColorValue, NumType
from game.utils.text import Text

if typing.TYPE_CHECKING:
    from game.views import View


class Button:
    """Class to work with buttons"""

    def __init__(
        self,
        xy: tuple[NumType, NumType],
        dimensions: tuple[NumType, NumType],
        text: str = "Button",
        on_click: Optional[Callable] = None,
        once: bool = True,
    ):
        """Initialize the button"""
        self.x, self.y = xy
        self.width, self.height = dimensions
        self.on_click = on_click
        self.once = once
        self.text = text

        self.fill_colors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        self.button_surface = Surface((self.width, self.height))
        self.button_rect = Rect(
            self.x - self.width / 2, self.y - self.height / 2, self.width, self.height
        )
        self.already_pressed = False
        self.left_click = getattr(
            importlib.import_module("game.custom_event"), "LEFT_CLICK"
        )

    def update(self):
        """Process mouse input"""

        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors["normal"])

        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors["hover"])
            if self.left_click.get():
                self.button_surface.fill(self.fill_colors["pressed"])
                if self.on_click:
                    if self.once:
                        self.on_click()
                    elif not self.already_pressed:
                        self.on_click()
                        self.already_pressed = True
        else:
            self.already_pressed = False

    def __repr__(self):
        return f"<Button {self.text}>"

    def blit_into(
        self,
        surface: Surface,
        font: Optional[str | bytes | Iterable[str | bytes]] = None,
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


class MenuButton(Button):
    """Buttons linking two views"""

    def __init__(
        self,
        view: "View",
        xy: tuple[NumType, NumType],
        dimensions: tuple[NumType, NumType],
        view_path: str,
        text: str = "Button",
        on_click=None,
    ) -> None:
        self._on_click = on_click
        self.view = view
        self.link_to_path = view_path
        super().__init__(xy, dimensions, text, on_click=self._change_to_view, once=True)

    def _change_to_view(self):
        """Switch views"""
        if self._on_click:
            # if there's something to do before switching views
            self._on_click()
        if self.link_to_path:
            # if path was empty, act like a normal button
            self.view.change_views(self.link_to_path, self.link_to_path.split(".")[-1])
