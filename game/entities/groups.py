"""This module consists of the sprite groups used in the game"""

import bisect

import pygame
from pygame import Surface
from pygame.sprite import Group

from game.entities.item import ItemTypes


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
        self.atk_offset = pygame.Vector2(0, 0)
        self.def_offset = pygame.Vector2(0, 0)
        self.potion_offset = pygame.Vector2(0, 0)

        # store the sprites with their positions
        self.atk_sprites = []
        self.def_sprites = []
        self.potion_sprites = []

        # if inventory changed
        self._changed = False

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
            self.atk_offset = pygame.Vector2(0, 0)
            for sprite in self.atk_list:
                if self.atk_offset[0] + 120 > surface.get_width() - 100:
                    self.atk_offset[1] += 120
                    self.atk_offset[0] = 0
                pos = pygame.Vector2(100, 100) + self.atk_offset
                self.atk_sprites.append((sprite, pos))
                sprite.draw(surface, pos)
                self.atk_offset[0] += 120

            self.def_offset = pygame.Vector2(0, self.atk_offset[1] + 250)
            for sprite in self.def_list:
                if self.def_offset[0] + 120 > surface.get_width() - 100:
                    self.def_offset[1] += 120
                    self.def_offset[0] = 0
                pos = pygame.Vector2(100, 100) + self.def_offset
                self.def_sprites.append((sprite, pos))
                sprite.draw(surface, pos)
                self.def_offset[0] += 120

            self.potion_offset = pygame.Vector2(0, self.def_offset[1] + 250)
            for sprite in self.potion_list:
                if self.potion_offset[0] + 120 > surface.get_width() - 100:
                    self.potion_offset[1] += 120
                    self.potion_offset[0] = 0
                pos = pygame.Vector2(100, 100) + self.potion_offset
                self.potion_sprites.append((sprite, pos))
                sprite.draw(surface, pos)
                self.potion_offset[0] += 120

            self._changed = False
        else:
            for sprite in self.atk_sprites:
                sprite, pos = sprite
                sprite.draw(surface, pos)
            for sprite in self.def_sprites:
                sprite, pos = sprite
                sprite.draw(surface, pos)
            for sprite in self.potion_sprites:
                sprite, pos = sprite
                sprite.draw(surface, pos)

    def scroll(self, dx, dy):
        """scroll the items up or down"""

        for sprite in self.sprites():
            sprite.scroll(dx, dy)
