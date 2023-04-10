""" Implements the Menu view """

from game.utils import Text, MenuButton
from game.views import View


class Menu(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = [
            {"text": "New Game", "link_to_path": "map.Map"},
            {"text": "Continue", "link_to_path": "map.Map"},
            {"text": "TEST - Battle", "link_to_path": "battle.Battle"},
        ]
        self.buttons = [
            MenuButton(
                self,
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(100, 50),
                view_path=option["link_to_path"],
                text=option["text"],
                on_click=lambda: print("pressed"),  # debug
            )
            for i, option in enumerate(self.options)
        ]
        print(self.buttons)

    def on_update(self):
        for b in self.buttons:
            b.update()

    def on_draw(self):
        self.screen.fill("black")
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
