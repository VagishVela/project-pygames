# pylint: skip-file
from game.utils import Text
from game.views import View


class View1(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self):
        text = Text(
            "This is View1", self.font, self.width / 2, self.height / 2, 60, "white"
        )
        text.blit_into(self.screen)

    def on_click(self, event):
        self.change_views("view2.View2", "View2")
