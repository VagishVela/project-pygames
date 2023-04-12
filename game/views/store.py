"""This module implements the Store class"""

from game.entities.groups import StoreItems
from game.entities.item import StoreItem, ItemTypes, StoreDiv
from game.views import View


class Store(View):
    """The game store"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_color = (50, 50, 50)

        self.items = StoreItems()

        item1 = StoreItem("assets/knife.png", ItemTypes.ATK, "knife")
        item1.add(self.items)

        item3 = StoreItem("assets/knife.png", ItemTypes.ATK, "apple")
        item3.add(self.items)
        item1 = StoreItem("assets/knife.png", ItemTypes.ATK, "knife")
        item1.add(self.items)

        item3 = StoreItem("assets/potion.png", ItemTypes.POTION, "apple")
        item3.add(self.items)
        item1 = StoreItem("assets/potion.png", ItemTypes.POTION, "knife")
        item1.add(self.items)

        item3 = StoreItem("assets/knife.png", ItemTypes.ATK, "apple")
        item3.add(self.items)
        item1 = StoreItem("assets/potion.png", ItemTypes.POTION, "knife")
        item1.add(self.items)

        item2 = StoreItem("assets/shield.png", ItemTypes.DEF, "shield")
        item2.add(self.items)

        self.atk_div = StoreDiv("ATK")
        self.def_div = StoreDiv("DEF")
        self.potion_div = StoreDiv("POTION")

    def on_draw(self):
        self.items.draw(self.screen)
        self.atk_div.draw(
            self.screen, (50, 50, self.width - 100, self.items.atk_offset[1] + 200)
        )
        self.def_div.draw(
            self.screen,
            (
                50,
                self.items.atk_offset[1] + 300,
                self.width - 100,
                self.items.def_offset[1] - self.items.atk_offset[1] - 50,
            ),
        )
        self.potion_div.draw(
            self.screen,
            (
                50,
                self.items.def_offset[1] + 300,
                self.width - 100,
                self.items.potion_offset[1] - self.items.def_offset[1] - 50,
            ),
        )

    def on_scroll(self, event):
        if event.mode == "up":
            self.items.scroll(0, 10)
            self.atk_div.scroll(0, 10)
            self.def_div.scroll(0, 10)
            self.potion_div.scroll(0, 10)
        elif event.mode == "down":
            self.items.scroll(0, -10)
            self.atk_div.scroll(0, -10)
            self.def_div.scroll(0, -10)
            self.potion_div.scroll(0, -10)
