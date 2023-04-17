"""This module implements the Store class"""

import pygame

from game.config import STORE_PADDING, STORE_BG, STORE_SCROLL_SPEED
from game.data import game_data
from game.entities.groups import StoreItems
from game.entities.item import StoreItem, StoreDiv, StoreFooter
from game.utils.div import Div
from game.views import View


class _Divs:
    """Class to work with multiple Div elements"""

    def __init__(self, _dict):
        self.div_list = []
        for i in _dict:
            setattr(self, i, _dict[i])
            assert isinstance(_dict[i][0], Div)
            self.div_list.append(i)

    def draw(self, screen):
        """Draw the rects in push order"""
        for i in self.div_list:
            div = getattr(self, i)
            div[0].draw(screen, div[1])

    def scroll(self, dx, dy):
        """Scroll the rects"""
        for i in self.div_list:
            div = getattr(self, i)
            div[0].scroll(dx, dy)

    def update_rect(self, new_rect_dict):
        """Update the rects boundary"""
        for i in self.div_list:
            div = getattr(self, i)
            div[1] = new_rect_dict[i]


class Store(View):
    """The game store"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escape_to = None
        self.bg_color = STORE_BG

        self.items = StoreItems()

        # list the items
        _items = [
            "knife1",
            "knife2",
            "knife3",
            "knife4",
            "knife5",
            "shield1",
            "shield2",
            "potion",
        ]
        for item in _items:
            item = StoreItem(item)
            item.add(self.items)

        self.divs = _Divs(
            {
                "ATK": [
                    StoreDiv("ATK"),
                    (
                        STORE_PADDING / 2,
                        STORE_PADDING / 2,
                        self.width - STORE_PADDING,
                        self.items.atk_offset[1] + 2 * STORE_PADDING,
                    ),
                ],
                "DEF": [
                    StoreDiv("DEF"),
                    (
                        STORE_PADDING / 2,
                        self.items.atk_offset[1] + 3 * STORE_PADDING,
                        self.width - STORE_PADDING,
                        self.items.def_offset[1]
                        - self.items.atk_offset[1]
                        - STORE_PADDING / 2,
                    ),
                ],
                "POTION": [
                    StoreDiv("POTION"),
                    (
                        STORE_PADDING / 2,
                        self.items.def_offset[1] + 3 * STORE_PADDING,
                        self.width - STORE_PADDING,
                        self.items.potion_offset[1]
                        - self.items.def_offset[1]
                        - STORE_PADDING / 2,
                    ),
                ],
            }
        )
        self.footer = StoreFooter()

    def on_draw(self):
        self.items.draw(self.screen)
        self.divs.draw(self.screen)
        self.footer.draw(self.screen)

    def on_update(self):
        self.divs.update_rect(
            {
                "ATK": (
                    STORE_PADDING / 2,
                    STORE_PADDING / 2,
                    self.width - STORE_PADDING,
                    self.items.atk_offset[1] + 2 * STORE_PADDING,
                ),
                "DEF": (
                    STORE_PADDING / 2,
                    self.items.atk_offset[1] + 3 * STORE_PADDING,
                    self.width - STORE_PADDING,
                    self.items.def_offset[1]
                    - self.items.atk_offset[1]
                    - STORE_PADDING / 2,
                ),
                "POTION": (
                    STORE_PADDING / 2,
                    self.items.def_offset[1] + 3 * STORE_PADDING,
                    self.width - STORE_PADDING,
                    self.items.potion_offset[1]
                    - self.items.def_offset[1]
                    - STORE_PADDING / 2,
                ),
            }
        )
        active_item = self.items.on_update()
        self.footer.update(active_item)

    def on_scroll(self, event):
        if event.mode == "up":
            self.items.scroll(0, STORE_SCROLL_SPEED)
            self.divs.scroll(0, STORE_SCROLL_SPEED)
        elif event.mode == "down":
            self.items.scroll(0, -STORE_SCROLL_SPEED)
            self.divs.scroll(0, -STORE_SCROLL_SPEED)

    def pre_run(self, _spl_args):
        escape_to_name: str = game_data.get_temp("return_to")
        self.escape_to = f"{escape_to_name.lower()}.{escape_to_name}"

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.change_views(self.escape_to)
