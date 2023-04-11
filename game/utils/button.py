""" This module implements the Button class """
import typing
from typing import Iterable, Callable, Tuple

import pygame

from game.common_types import ColorValue, NumType
from game.utils.text import Text

if typing.TYPE_CHECKING:
    from game.views import View


class Button:
    """Class to work with buttons"""

    def __init__(
        self,
        x: NumType,
        y: NumType,
        width: NumType,
        height: NumType,
        text: str = "Button",
        on_click: Callable = None,
        once: bool = False,
    ):
        """Initialize the button"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
        self.once = once
        self.text = text

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

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.button_rect.collidepoint(
                mouse_pos
            ):
                self.button_surface.fill(self.fill_colors["pressed"])
                if self.once:
                    self.on_click()
                elif not self.already_pressed:
                    self.on_click()
                    self.already_pressed = True

        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors["hover"])
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


class MenuButton(Button):
    """Buttons linking two views"""

    def __init__(
        self,
        view: "View",
        xy: Tuple[NumType, NumType],
        dimensions: Tuple[NumType, NumType],
        view_path: str,
        text: str = "Button",
        on_click=None,
    ) -> None:
        x, y = xy
        width, height = dimensions
        self._on_click = on_click
        self.view = view
        self.link_to_path = view_path
        super().__init__(
            x, y, width, height, text, on_click=self._change_to_view, once=True
        )

    def _change_to_view(self):
        """Switch views"""
        if self._on_click:
            # if there's something to do before switching views
            self._on_click()
        self.view.change_views(self.link_to_path)
