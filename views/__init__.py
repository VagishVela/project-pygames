""" This package contains the views """

import pygame

from game.config import FPS
from game.utils import Cache

views_cache = Cache()


class View:
    """An object representing the current 'view' on display"""

    def __init__(self, width, height, title: str = None, icon: pygame.Surface = None):
        self.width = width
        self.height = height

        if title:
            pygame.display.set_caption(title)
        if icon:
            pygame.display.set_icon(icon)

        self.size = (self.width, self.height)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.get_default_font()

        self._running = False

    def on_draw(self):
        """Draw things onto the View surface"""

    @staticmethod
    def exit():
        """Quit the view"""
        pygame.quit()

    def _refresh(self, frame_rate=FPS):
        self.clock.tick(frame_rate)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self._running = False
                case pygame.MOUSEBUTTONDOWN:
                    self.on_click()

    def on_update(self):
        """To override"""

    def run(self):
        """Runs the main loop for this view"""

        self._running = True
        print("Loading done!", self, flush=True)
        while self._running:
            try:
                self._handle_events()
                self.on_draw()
                self.on_update()
                self._refresh()
            except pygame.error:
                self._running = False
        self.exit()

    def on_click(self):
        """Called when the mouse is clicked"""

    # pylint: disable=too-many-arguments
    def change_views(
        self,
        destination_class_ptr,
        width: float | int = None,
        height: float | int = None,
        title: str = None,
        check_cache: bool = True,
    ):
        """
        Change views and display the next View

        :param destination_class_ptr: pointer to the View class to display
        :param title: Window title, stays the same by default
        :param height: Window height, stays the same by default
        :param width: Window width, stays the same by default
        :param check_cache: Whether to check for cached objects
        :return:
        """

        if not width:
            width = self.width
        if not height:
            height = self.height
        if not title:
            title = pygame.display.get_caption()[0]

        if check_cache:
            destination = views_cache.get(
                (destination_class_ptr.__name__, width, height, title),
                destination_class_ptr(width, height, title),
            )
        else:
            destination = destination_class_ptr(width, height, title)

        assert isinstance(destination, View), "Destination isn't of type View"
        print("switching views from", self, "to", destination, flush=True)
        destination.run()
