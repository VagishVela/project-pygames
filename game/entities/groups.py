"""This module consists of the sprite groups used in the game"""

import bisect
from typing import Optional

import pygame
from pygame import Surface, Vector2
from pygame.sprite import Group

from game.config import STORE_PADDING
from game.custom_event import ITEM_FOCUSED, LEFT_CLICK
from game.entities.item import ItemTypes, StoreItem
from game.logger import logger

logger = logger.getChild("entities.item")


class NotPlayer(Group):
    """Group for anything in map view that is not the player"""

    def __init__(self):
        """Initialize the NotPlayer group"""
        super().__init__()

    def draw(self, surface: Surface, bgsurf=None, special_flags: int = 0):
        """Draw the objects"""
        for sprite in self.sprites():
            if sprite.visible:
                sprite.draw(surface)

    def disappear(self, sprites):
        """Make the objects disappear"""
        for sprite in sprites:
            if sprite in self.sprites():
                sprite.visible = False


class StoreItems(Group):
    """Group for StoreItem"""

    def __init__(self):
        super().__init__()
        # store the sprites
        self.atk_list = []
        self.def_list = []
        self.potion_list = []

        # store the sprite offsets
        self.atk_offset = Vector2(0, 0)
        self.def_offset = Vector2(0, 0)
        self.potion_offset = Vector2(0, 0)

        # store the sprites with their positions
        self.sprite_pos = []
        self.sprite_rects = {}

        # if inventory changed
        self._changed = False

        # currently active item
        self.active_item = None

    def add_internal(self, sprite, layer: None = None) -> None:
        self.spritedict[sprite] = None
        # sorted manner
        # sorted by name for now
        if sprite.type == ItemTypes.ATK:
            bisect.insort(self.atk_list, sprite, key=lambda x: x.name)
        elif sprite.type == ItemTypes.DEF:
            bisect.insort(self.def_list, sprite, key=lambda x: x.name)
        elif sprite.type == ItemTypes.POTION:
            bisect.insort(self.potion_list, sprite, key=lambda x: x.name)
        self._changed = True

    def remove_internal(self, sprite) -> None:
        lost_rect = self.spritedict[sprite]
        if lost_rect:
            self.lostsprites.append(lost_rect)
        del self.spritedict[sprite]

        if sprite.type == ItemTypes.ATK:
            self.atk_list.remove(sprite)
        elif sprite.type == ItemTypes.DEF:
            self.def_list.remove(sprite)
        elif sprite.type == ItemTypes.POTION:
            self.potion_list.remove(sprite)
        self._changed = True

    def draw(self, surface: Surface, bgsurf=None, special_flags: int = 0):
        if self._changed:
            self.atk_offset = Vector2(0, 0)
            for sprite in self.atk_list:
                if (
                    self.atk_offset[0] + STORE_PADDING * 1.2
                    > surface.get_width() - STORE_PADDING
                ):
                    self.atk_offset[1] += STORE_PADDING * 1.2
                    self.atk_offset[0] = 0
                pos = Vector2(STORE_PADDING, STORE_PADDING) + self.atk_offset
                self.sprite_pos.append((sprite, pos))
                self.sprite_rects.update(sprite.draw(surface, pos))
                self.atk_offset[0] += STORE_PADDING * 1.2

            self.def_offset = Vector2(0, self.atk_offset[1] + STORE_PADDING * 2.5)
            for sprite in self.def_list:
                if (
                    self.def_offset[0] + STORE_PADDING * 1.2
                    > surface.get_width() - STORE_PADDING
                ):
                    self.def_offset[1] += STORE_PADDING * 1.2
                    self.def_offset[0] = 0
                pos = Vector2(STORE_PADDING, STORE_PADDING) + self.def_offset
                self.sprite_pos.append((sprite, pos))
                self.sprite_rects.update(sprite.draw(surface, pos))
                self.def_offset[0] += STORE_PADDING * 1.2

            self.potion_offset = Vector2(0, self.def_offset[1] + STORE_PADDING * 2.5)
            for sprite in self.potion_list:
                if (
                    self.potion_offset[0] + STORE_PADDING * 1.2
                    > surface.get_width() - STORE_PADDING
                ):
                    self.potion_offset[1] += STORE_PADDING * 1.2
                    self.potion_offset[0] = 0
                pos = Vector2(STORE_PADDING, STORE_PADDING) + self.potion_offset
                self.sprite_pos.append((sprite, pos))
                self.sprite_rects.update(sprite.draw(surface, pos))
                self.potion_offset[0] += STORE_PADDING * 1.2

            self._changed = False
        else:
            for sprite, pos in self.sprite_pos:
                self.sprite_rects.update(sprite.draw(surface, pos))
                if self.active_item:
                    if sprite.name == self.active_item.name:
                        sprite.on_focus = True
                    else:
                        sprite.on_focus = False

    def on_update(self) -> Optional[StoreItem]:
        """To be invoked from the view update method"""

        # onclick events
        mouse_pos = Vector2(pygame.mouse.get_pos())
        # item_clicked = False

        for sprite, rect in self.sprite_rects.items():
            if rect.collidepoint(mouse_pos):
                if LEFT_CLICK.get():
                    ITEM_FOCUSED.post({"item": sprite})
                    logger.debug(f"pressed! {sprite.name}")
                    # item_clicked = True
                    break

        # todo: if user clicks outside items, set active_item to None
        # if not item_clicked:
        #     if LEFT_CLICK.get():
        #         self.active_item = None
        #         for sprite in self.sprites():
        #             sprite.on_focus = False

        if e := ITEM_FOCUSED.get():
            logger.debug(f"event received {e.item.name} is active")
            self.active_item = e.item
        return self.active_item

    def scroll(self, dx, dy):
        """scroll the items up or down"""

        for sprite in self.sprites():
            sprite.scroll(dx, dy)
