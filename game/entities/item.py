"""This module implements the classes required for the store"""

from enum import Enum

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.utils import Text
from game.utils.div import Div, Scrollable


class ItemTypes(Enum):
    """Types of items in the store"""

    ATK = 1
    DEF = 2
    POTION = 3
    SPECIAL = 4


# pylint: disable=no-member
class AllItems(Enum):
    """Enumerate all items for the store"""

    # itemID = (img_path, itemType, itemName)
    knife = ("assets/knife.png", ItemTypes.ATK, "knife")
    shield = ("assets/shield.png", ItemTypes.DEF, "shield")
    potion = ("assets/potion.png", ItemTypes.POTION, "potion")

    @property
    def img_path(self) -> str:
        """get the image path of the item"""

        return self._value_[0]

    @property
    def type(self) -> int:
        """get the item type of the item"""

        return self._value_[1]

    @property
    def item_name(self) -> str:
        """get the item name of the item"""

        return self._value_[2]

    @property
    def id(self) -> str:
        """get the itemID of the item"""

        return self.name


class StoreItem(Sprite, Scrollable):
    """Class for the items in store"""

    def __init__(self, itemID: str):
        """Initialize the item"""

        # super() doesn't initiate both
        Sprite.__init__(self)
        Scrollable.__init__(self)

        # if locked, grey out
        self.locked = False

        self.item = getattr(AllItems, itemID)
        self.type = self.item.type
        self.name = self.item.item_name
        self.image = pygame.transform.scale(
            pygame.image.load(self.item.img_path), (72, 72)
        )
        self.rect = self.image.get_rect()

    def draw(self, screen: Surface, pos):
        """Draw the item"""

        surface = Surface((100, 100), pygame.SRCALPHA)
        name = Text(self.name, pygame.font.get_default_font(), 50, 90, 30, "white")
        name.blit_into(surface)
        surface.blit(self.image, (14, 0))
        screen.blit(surface, pygame.Vector2(pos) + self.offset)


# alias
StoreDiv = Div
