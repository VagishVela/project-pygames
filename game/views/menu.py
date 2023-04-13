""" Implements the Menu view """

from game.utils import Text, MenuButton
from game.views import View, logger

# get logger
logger = logger.getChild("menu")


class Menu(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = [
            {"text": "New Game", "view_path": "map.Map"},
            {"text": "Continue", "view_path": "map.Map"},
            {"text": "TEST - Battle", "view_path": "battle.Battle"},
            {"text": "TEST - Store", "view_path": "store.Store"},
        ]
        self.buttons = [
            MenuButton(
                self,
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(100, 50),
                view_path=option["view_path"],
                text=option["text"],
                on_click=lambda: print("pressed"),  # debug
            )
            for i, option in enumerate(self.options)
        ]
        logger.debug(f" buttons: {self.buttons}")

    def on_update(self):
        for b in self.buttons:
            # ensure display is initiated
            if self._running:
                b.update()

    def on_draw(self):
        Text(
            "Menu",
            self.font,
            self.width / 2,
            self.height / 2 - 200,
            40,
            "red",
        ).blit_into(self.screen)

        for b in self.buttons:
            b.blit_into(self.screen)
