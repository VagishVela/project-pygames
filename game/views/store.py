"""This module implements the Store class"""

from game.entities.groups import StoreItems
from game.entities.item import StoreItem, StoreDiv
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
        self.bg_color = (50, 50, 50)

        self.items = StoreItems()

        # list the items
        _items = ["knife", "shield", "potion"]
        for item in _items:
            item = StoreItem(item)
            item.add(self.items)

        self.divs = _Divs(
            {
                "ATK": [
                    StoreDiv("ATK"),
                    (50, 50, self.width - 100, self.items.atk_offset[1] + 200),
                ],
                "DEF": [
                    StoreDiv("DEF"),
                    (
                        50,
                        self.items.atk_offset[1] + 300,
                        self.width - 100,
                        self.items.def_offset[1] - self.items.atk_offset[1] - 50,
                    ),
                ],
                "POTION": [
                    StoreDiv("POTION"),
                    (
                        50,
                        self.items.def_offset[1] + 300,
                        self.width - 100,
                        self.items.potion_offset[1] - self.items.def_offset[1] - 50,
                    ),
                ],
            }
        )

    def on_draw(self):
        self.items.draw(self.screen)
        self.divs.draw(self.screen)
        self.divs.update_rect(
            {
                "ATK": (50, 50, self.width - 100, self.items.atk_offset[1] + 200),
                "DEF": (
                    50,
                    self.items.atk_offset[1] + 300,
                    self.width - 100,
                    self.items.def_offset[1] - self.items.atk_offset[1] - 50,
                ),
                "POTION": (
                    50,
                    self.items.def_offset[1] + 300,
                    self.width - 100,
                    self.items.potion_offset[1] - self.items.def_offset[1] - 50,
                ),
            }
        )

    def on_scroll(self, event):
        if event.mode == "up":
            self.items.scroll(0, 20)
            self.divs.scroll(0, 20)
        elif event.mode == "down":
            self.items.scroll(0, -20)
            self.divs.scroll(0, -20)
