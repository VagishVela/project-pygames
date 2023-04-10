""" Implements the Menu view """

from game.utils import Text, Button
from game.views import View


class Menu(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = [{"name": "New Game", "module": "map", "screen": "Map"}]
        self.buttons = [
            Button(
                self.width / 2,
                self.height / 2 - 120 + i * 60,
                100,
                50,
                text=option["name"],
                module=option["module"],
                screen=option["screen"],
                on_click=self.on_button_click,
            )
            for i, option in enumerate(self.options)
        ]
        print(self.buttons)

    def on_button_click(self, button):
        self.change_views(
            f"{button.module}.{button.screen}",
            button.screen,
        )

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
