"""Useful structure components"""

from abc import ABC

import pygame
from pygame import Vector2, Surface

from game.utils.text import Text


# pylint: disable=too-few-public-methods
class Scrollable(ABC):
    """scrollable components, have scrolling behaviour"""

    def __init__(self):
        """Initialize the component"""

        self.offset = Vector2(0, 0)

    def scroll(self, dx, dy):
        """Scroll the component"""

        self.offset += Vector2(dx, dy)


class Div(Scrollable):
    """Makes a rect enclosing a section of the store view"""

    def __init__(self, caption):
        super().__init__()
        self.caption = caption
        self.rect = None

    def draw(self, screen: Surface, rect):
        """Draw the rect and caption"""

        surface = Surface(screen.get_size(), pygame.SRCALPHA)
        self.rect = pygame.Rect(rect)
        rect = self.rect
        rect[1] += self.offset[1]
        pygame.draw.rect(surface, "white", rect, 10, 5)

        if self.caption:
            text = Text(
                self.caption,
                pygame.font.get_default_font(),
                rect[0] + 100,
                rect[1],
                60,
                "white",
                (50, 50, 50),
            )
            text.blit_into(surface)
        screen.blit(surface, (0, 0))

        # on click behaviour
        self.on_click()

    def on_click(self):
        """Called if the rect is clicked"""

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if e := pygame.event.get(pygame.MOUSEBUTTONDOWN):
                if e[0].button != 1:
                    pygame.event.post(e[0])
                    return
                print("pressed!")