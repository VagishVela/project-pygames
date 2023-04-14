""" Implements the Map view, TopDown2D """
import itertools

import pygame
from pygame.sprite import Group

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.custom_event import MOVED, ENEMY_ENCOUNTERED
from game.entities.enemy import Enemy
from game.entities.groups import NotPlayer
from game.entities.player import Player
from game.entities.walls import Wall
from game.level_gen import Level
from game.views import View, logger

# store game data
data = {}
# get logger
logger.getChild("map")


class Map(View):
    """Map view"""

    player = Player()
    not_player = NotPlayer()
    enemies = Group()
    level = Level()
    _e_hash = {}
    _w_hash = {}
    _initiated = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed = 5

        self._cur = []
        self._moved = False

        if not Map._initiated:
            Map.initiate()

    def on_draw(self):
        self.not_player.draw(self.screen)
        self.player.draw(self.screen)

    def on_keydown(self, event):
        match event.key:
            case pygame.K_UP | pygame.K_w:
                self.level.move(0, 1)
            case pygame.K_DOWN | pygame.K_s:
                self.level.move(0, -1)
            case pygame.K_LEFT | pygame.K_a:
                self.level.move(1, 0)
            case pygame.K_RIGHT | pygame.K_d:
                self.level.move(-1, 0)
            case pygame.K_ESCAPE:
                logger.debug(" game paused")
                self.change_views("pause.Pause", caption="Paused")
                return
        if MOVED.get():
            self.not_player.disappear(self._cur)
            self._moved = True
        if ENEMY_ENCOUNTERED.get():
            logger.debug(" enemy encountered!")
            self.change_views("battle.Battle", caption="Battle")

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
            self._moved = False

    def save_data(self):
        """Save the data"""
        data["player_pos"] = self.level.loc
        data["e_hash"] = self._e_hash
        data["w_hash"] = self._w_hash
        print("saved data!")

    def terminate(self):
        """Terminate the view"""
        self.not_player.disappear(self._cur)
        self.level.loc = [0, 0]

    @classmethod
    def initiate(cls):
        """Initiate all the sprites the map ever needs"""

        # generating sprites is an expensive process, so if done mid-game,
        # it would make the game very clunky

        for i, j in itertools.product(range(9), range(9)):
            cls._e_hash[(i, j)] = Enemy(
                (i - 4.5) * SCREEN_WIDTH / 9 + SCREEN_WIDTH / 2,
                (j - 4.5) * SCREEN_HEIGHT / 9 + SCREEN_HEIGHT / 2,
            )
            cls._e_hash[(i, j)].add(cls.enemies, cls.not_player)
            cls._e_hash[(i, j)].visible = False
            cls._w_hash[(i, j)] = Wall(
                (i - 4.5) * SCREEN_WIDTH / 9 + SCREEN_WIDTH / 2,
                (j - 4.5) * SCREEN_HEIGHT / 9 + SCREEN_HEIGHT / 2,
            )
            cls._w_hash[(i, j)].add(cls.not_player)
            cls._w_hash[(i, j)].visible = False
            cls._initiated = True
