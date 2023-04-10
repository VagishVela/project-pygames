""" Implements the Map view, TopDown2D """
import itertools

import pygame
from pygame.sprite import Group

from game.entities.enemy import Enemy, NotPlayer
from game.entities.player import Player
from game.entities.walls import Wall
from game.level_gen import Level
from views import View

data = {}


class Map(View):
    """Map view"""

    player: Player
    not_player: NotPlayer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = Player()
        self.not_player = NotPlayer()
        self.enemies = Group()
        self.level = Level()

        self.speed = 5

        self._e_hash = {}
        self._w_hash = {}
        self._cur = []
        self._moved = [False, "nr"]

        for i, j in itertools.product(range(9), range(9)):
            self._e_hash[(i, j)] = Enemy(
                (i - 4.5) * self.width / 9 + self.width / 2,
                (j - 4.5) * self.height / 9 + self.height / 2,
            )
            self._e_hash[(i, j)].add(self.enemies, self.not_player)
            self._e_hash[(i, j)].visible = False
            self._w_hash[(i, j)] = Wall(
                (i - 4.5) * self.width / 9 + self.width / 2,
                (j - 4.5) * self.height / 9 + self.height / 2,
            )
            self._w_hash[(i, j)].add(self.not_player)
            self._w_hash[(i, j)].visible = False

    def on_draw(self):
        self.screen.fill("black")
        self.not_player.draw(self.screen)
        self.player.draw(self.screen)

    def _handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self._running = False
                case pygame.MOUSEBUTTONDOWN:
                    self.on_click()
                case pygame.KEYDOWN:
                    self._moved = [False, "nr"]
                    match event.key:
                        case pygame.K_UP | pygame.K_w:
                            self._moved = self.level.move(0, 1)
                        case pygame.K_DOWN | pygame.K_s:
                            self._moved = self.level.move(0, -1)
                        case pygame.K_LEFT | pygame.K_a:
                            self._moved = self.level.move(1, 0)
                        case pygame.K_RIGHT | pygame.K_d:
                            self._moved = self.level.move(-1, 0)
                        case pygame.K_ESCAPE:
                            from game.views.pause import Pause

                            self.change_views(Pause, self.width, self.height, "Paused")

                    if self._moved[0]:
                        self.not_player.disappear(self._cur)
                    elif self._moved[1] == "e":
                        from game.views.battle import Battle
                        self.change_views(Battle, title="Battle")

    def on_update(self):
        if self._moved or not self._cur:
            floor = self.level.generate(9, 9)
            for y, row in enumerate(floor):
                for x, e in enumerate(row):
                    match chr(e):
                        case "e":
                            self._e_hash[(x, y)].visible = True
                            self._cur.append(self._e_hash[(x, y)])
                        case "w":
                            self._w_hash[(x, y)].visible = True
                            self._cur.append(self._w_hash[(x, y)])

    def save_data(self):
        data["player_pos"] = self.level.loc
        data["e_hash"] = self._e_hash
        data["w_hash"] = self._w_hash
        print("saved data!")

    def terminate(self):
        self.not_player.disappear(self._cur)
        self.level.loc = [0, 0]
