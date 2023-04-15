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
        self.sprite_pos = {}
        self.sprite_rects = {}

        # if inventory changed
        self.items_changed = False

        # currently active item
        self.active_item = None

    def add_internal(self, sprite, layer: None = None) -> None:
        self.spritedict[sprite] = None
        # sorted manner
        # sorted by name for now
        match sprite.type:
            case ItemTypes.ATK:
                bisect.insort(self.atk_list, sprite, key=lambda x: x.name)
            case ItemTypes.DEF:
                bisect.insort(self.def_list, sprite, key=lambda x: x.name)
            case ItemTypes.POTION:
                bisect.insort(self.potion_list, sprite, key=lambda x: x.name)
        self.items_changed = True

    def remove_internal(self, sprite) -> None:
        if lost_rect := self.spritedict[sprite]:
            self.lostsprites.append(lost_rect)
        del self.spritedict[sprite]
        match sprite.type:
            case ItemTypes.ATK:
                self.atk_list.remove(sprite)
            case ItemTypes.DEF:
                self.def_list.remove(sprite)
            case ItemTypes.POTION:
                self.potion_list.remove(sprite)
        self.items_changed = True

    def draw(self, surface: Surface, bgsurf=None, special_flags: int = 0):
        if self.items_changed:
            self._on_item_changed(surface)
            return
        for sprite, pos in self.sprite_pos.items():
            self.sprite_rects.update(sprite.draw(surface, pos))
            if self.active_item:
                sprite.on_focus = sprite.name == self.active_item.name

    def _on_item_changed(self, surface):
        """run if items were changed, recalculate the offsets and rects"""

        self.atk_offset = Vector2(0, 0)
        for sprite in self.atk_list:
            if (
                self.atk_offset[0] + STORE_PADDING * 1.2
                > surface.get_width() - STORE_PADDING
            ):
                self.atk_offset[1] += STORE_PADDING * 1.2
                self.atk_offset[0] = 0
            pos = Vector2(STORE_PADDING, STORE_PADDING) + self.atk_offset
            self.sprite_pos.update({sprite: pos})
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
            self.sprite_pos.update({sprite: pos})
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
            self.sprite_pos.update({sprite: pos})
            self.sprite_rects.update(sprite.draw(surface, pos))
            self.potion_offset[0] += STORE_PADDING * 1.2

        self.items_changed = False

    def on_update(self) -> Optional[StoreItem]:
        """To be invoked from the view update method"""

        # onclick events
        mouse_pos = Vector2(pygame.mouse.get_pos())
        # item_clicked = False

        for sprite, rect in self.sprite_rects.items():
            if rect.collidepoint(mouse_pos) and LEFT_CLICK.get():
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
