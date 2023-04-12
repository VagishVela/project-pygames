"""This module implements the classes required for the store"""

from enum import Enum

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.config import STORE_PADDING, STORE_BG, TILE_SIZE
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
    knife1 = ("assets/knife.png", ItemTypes.ATK, "knife 1")
    knife2 = ("assets/knife.png", ItemTypes.ATK, "knife 2")
    knife3 = ("assets/knife.png", ItemTypes.ATK, "knife 3")
    knife4 = ("assets/knife.png", ItemTypes.ATK, "knife 4")
    knife5 = ("assets/knife.png", ItemTypes.ATK, "knife 5")
    shield1 = ("assets/shield.png", ItemTypes.DEF, "shield 1")
    shield2 = ("assets/shield.png", ItemTypes.DEF, "shield 2")
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
            pygame.image.load(self.item.img_path), (TILE_SIZE, TILE_SIZE)
        )
        self.rect = self.image.get_rect()

    def draw(self, screen: Surface, pos):
        """Draw the item"""

        surface = Surface((STORE_PADDING, STORE_PADDING), pygame.SRCALPHA)
        name = Text(
            self.name,
            pygame.font.get_default_font(),
            STORE_PADDING / 2,
            STORE_PADDING * 0.9,
            STORE_PADDING // 3,
            "white",
        )
        name.blit_into(surface)
        surface.blit(self.image, (STORE_PADDING / 2 - 36, 0))
        screen.blit(surface, pygame.Vector2(pos) + self.offset)


# alias
class StoreDiv(Div):
    """Div customised for use in Store"""

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
                rect[0] + STORE_PADDING,
                rect[1],
                STORE_PADDING // 3 * 2,
                "white",
                STORE_BG,
            )
            text.blit_into(surface)
        screen.blit(surface, (0, 0))

        # on click behaviour
        self.on_click()
