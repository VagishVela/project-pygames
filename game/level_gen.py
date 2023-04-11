"""Generate a level"""
# p is player
# e is Enemy -> En can be a way to have many different enemies
# w is wall -> Wn can be a way to have more obstacles
# x is walkable

import itertools
import random

import numpy as np

from game.custom_event import ENEMY_ENCOUNTERED, MOVED


class Level:
    """Class for generating a level"""

    def __init__(self, x=None, y=None):
        """Initialize the level"""
        self.x = 0
        self.y = 0
        self.arr = np.zeros((9, 9), dtype=np.int32)
        self.arr.fill(ord("x"))
        self.rng = random.Random()
        self.loc = [x, y] if x is not None and y is not None else [0, 0]

    def _get_tile(self, pos):
        """Get a tile"""
        self.rng.seed(str(pos))
        return ord(self.rng.choice("x" * 800 + "w" * 185 + "e" * 15))

    def generate(self, m=9, n=9) -> list:
        """Generate a level"""
        x, y = self.loc
        for i, j in itertools.product(range(m), range(n)):
            if i == m // 2 and j == n // 2:
                self.arr[4][4] = ord("p")
            else:
                self.arr[i][j] = self._get_tile((y - i, x - j))
        return list(self.arr)

    def move(self, dx, dy) -> None:
        """Move the whole map in the given direction"""

        if self.check_collision(dx, dy):
            self.loc[0] += dx
            self.loc[1] += dy
            MOVED.post()

    def check_collision(self, dx, dy) -> bool:
        """Check collision, return True if player can move to the next tile"""

        def _check_and_post(x, y) -> bool:
            if self.arr[x][y] == ord("e"):
                ENEMY_ENCOUNTERED.post()
                return False
            return self.arr[x][y] == ord("x")

        match (dx, dy):
            case (0, 1):
                return _check_and_post(3, 4)
            case (0, -1):
                return _check_and_post(5, 4)
            case (1, 0):
                return _check_and_post(4, 3)
            case (-1, 0):
                return _check_and_post(4, 5)
        return False
