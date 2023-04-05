""" Implements the Menu view """

from game.helper import Text, Button
from views import View


class Menu(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ["Option 1", "Option 2", "Option 3"]
        self.buttons = [
            Button(
                self.width / 2,
                self.height / 2 + i * 60,
                100,
                50,
                option,
                onclick=lambda: print("button pressed!", option),
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
            self.height / 2 - 50,
            200,
            "red",
        ).blit_into(self.screen)

        for b in self.buttons:
            b.blit_into(self.screen)

    def on_click(self):
        # import here to avoid circular imports
        # pylint: disable=C0415
        from game.views.start import Start

        self.change_views(Start, self.width, self.height, "Menu")
