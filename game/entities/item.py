"""This module implements the classes required for the store"""

from abc import ABC
from enum import Enum

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.utils import Text


class ItemTypes(Enum):
    """Types of items in the store"""

    ATK = 1
    DEF = 2
    POTION = 3
    SPECIAL = 4


# pylint: disable=too-few-public-methods
class StoreComponent(ABC):
    """Store components, has scrolling behaviour"""

    def __init__(self):
        """Initialize the component"""

        self.offset = pygame.Vector2(0, 0)

    def scroll(self, dx, dy):
        """Scroll the component"""

        self.offset += pygame.Vector2(dx, dy)


class StoreItem(Sprite, StoreComponent):
    """Class for the items in store"""

    def __init__(self, img_path, item_type, name):
        """Initialize the item"""

        super().__init__()
        self.offset = pygame.Vector2(0, 0)
        self.image = pygame.transform.scale(pygame.image.load(img_path), (72, 72))
        self.rect = self.image.get_rect()
        self.locked = False
        self.type = item_type
        self.name = name

    def draw(self, screen: Surface, pos):
        """Draw the item"""

        surface = Surface((100, 100), pygame.SRCALPHA)
        name = Text(self.name, pygame.font.get_default_font(), 50, 90, 30, "white")
        name.blit_into(surface)
        surface.blit(self.image, (14, 0))
        screen.blit(surface, pygame.Vector2(pos) + self.offset)


class StoreDiv(StoreComponent):
    """Makes a rect enclosing a section of the store view"""

    def __init__(self, caption):
        super().__init__()
        self.caption = caption
        self.rect = None

    def draw(self, screen: pygame.Surface, rect):
        """Draw the rect and caption"""

        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
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
