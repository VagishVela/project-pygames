"""This module implements the classes required for the store"""

from enum import Enum, IntEnum
from typing import Self, NamedTuple

import pygame
from pygame import Surface, Vector2
from pygame.rect import RectType, Rect
from pygame.sprite import Sprite

from game.config import STORE_PADDING, STORE_BG, TILE_SIZE, STORE_ON_FOCUS
from game.logger import logger
from game.utils import Text, Button
from game.utils.div import Div, Scrollable

logger = logger.getChild("entities.item")


class ItemTypes(IntEnum):
    """Types of items in the store"""

    ATK = 1
    DEF = 2
    POTION = 3
    SPECIAL = 4


# named tuples reduce the chance of error while entering data
ITEM = NamedTuple("item", [("img_path", str), ("type", ItemTypes), ("name", str)])


# pylint: disable=no-member
class AllItems(Enum):
    """Enumerate all items for the store"""

    # itemID = (img_path, itemType, itemName)
    knife1 = ITEM("assets/knife.png", ItemTypes.ATK, "knife 1")
    knife2 = ITEM("assets/knife.png", ItemTypes.ATK, "knife 2")
    knife3 = ITEM("assets/knife.png", ItemTypes.ATK, "knife 3")
    knife4 = ITEM("assets/knife.png", ItemTypes.ATK, "knife 4")
    knife5 = ITEM("assets/knife.png", ItemTypes.ATK, "knife 5")
    shield1 = ITEM("assets/shield.png", ItemTypes.DEF, "shield 1")
    shield2 = ITEM("assets/shield.png", ItemTypes.DEF, "shield 2")
    potion = ITEM("assets/potion.png", ItemTypes.POTION, "potion")

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
        self.on_focus = False

    def draw(self, screen: Surface, pos) -> dict["Self", RectType]:
        """Draw the item"""

        surface = Surface((STORE_PADDING, STORE_PADDING), pygame.SRCALPHA)
        if self.on_focus:
            surface.fill(STORE_ON_FOCUS)
        name = Text(
            self.name,
            pygame.font.get_default_font(),
            STORE_PADDING / 2,
            STORE_PADDING * 0.9,
            STORE_PADDING // 3,
            "white",
        )
        name.blit_into(surface)
        surface.blit(self.image, (STORE_PADDING / 2 - TILE_SIZE / 2, 0))
        screen.blit(surface, Vector2(pos) + self.offset)

        rect = surface.get_rect()
        rect.x, rect.y = Vector2(pos) + self.offset

        return {self: rect}

    def buy(self):
        """Buy this item"""
        # todo: expand this
        return f"{self} was bought!"

    def use(self):
        """Use this item"""
        # todo: expand this
        return f"{self} was used!"

    def __repr__(self):
        return f"<StoreItem: {self.name}>"


# alias
class StoreDiv(Div):
    """Div customised for use in Store"""

    def draw(self, screen: Surface, rect: RectType):
        """Draw the rect and caption"""

        surface = Surface(screen.get_size(), pygame.SRCALPHA)
        if isinstance(rect, tuple):
            rect = Rect(rect)
        rect[1] += self.offset[1]
        pygame.draw.rect(surface, "white", rect, 10, 5)

        if self.caption:
            Text(
                self.caption,
                pygame.font.get_default_font(),
                rect[0] + STORE_PADDING,
                rect[1],
                STORE_PADDING // 3 * 2,
                "white",
                STORE_BG,
            ).blit_into(surface)
        screen.blit(surface, (0, 0))


class StoreFooter(Div):
    """Div customised for use as Store footer"""

    def __init__(self):
        super().__init__("")
        self.buttons = {}
        self.active_item = None

    def draw(self, screen: Surface, rect=None):
        """Draw the rect and caption"""

        height = STORE_PADDING
        border = 2

        surface = Surface((screen.get_width(), height))
        rect = (0, 0, screen.get_width(), height)
        surface.fill(STORE_BG)
        pygame.draw.rect(surface, "white", rect, border, 5)

        # -------------- buttons ------------ #

        if not self.buttons.get("buy"):
            self.buttons["buy"] = Button(
                (
                    surface.get_width() / 2 - STORE_PADDING * 1.5,
                    screen.get_height() - height / 2,
                ),
                (STORE_PADDING / 2, STORE_PADDING / 2),
                "Buy",
                on_click=lambda: print(
                    "pressed!", self.active_item.buy() if self.active_item else None
                ),
            )
        if not self.buttons.get("use"):
            self.buttons["use"] = Button(
                (
                    surface.get_width() / 2 + STORE_PADDING * 1.5,
                    screen.get_height() - height / 2,
                ),
                (STORE_PADDING / 2, STORE_PADDING / 2),
                "Use",
                on_click=lambda: print(
                    "pressed!", self.active_item.use() if self.active_item else None
                ),
            )

        # -------------- blit --------------- #

        screen.blit(surface, (0, screen.get_height() - height))
        for buttons in self.buttons.values():
            buttons.blit_into(screen, size=STORE_PADDING // 3)

    def update(self, active_item):
        """To be invoked from the view update method"""

        self.active_item = active_item
        for buttons in self.buttons.values():
            buttons.update()
