"""Generate a level"""
# P is player
# E is Enemy -> En can be a way to have many different enemies
# W is wall -> Wn can be a way to have more obstacles
# x is walkable

import itertools
import random

import numpy as np


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

    def generate(self, m=9, n=9):
        """Generate a level"""
        x, y = self.loc
        for i, j in itertools.product(range(m), range(n)):
            if i == m // 2 and j == n // 2:
                self.arr[4][4] = ord("p")
            else:
                self.arr[i][j] = self._get_tile((y - i, x - j))
        return self.arr.tolist()

    def move(self, dx, dy):
        """Move the whole map in the given direction"""

        if f := self.check_collision(dx, dy):
            if f == "e":
                return [False, "e"]
            self.loc[0] += dx
            self.loc[1] += dy
            return [True, "ok"]
        return [False, "w"]

    def check_collision(self, dx, dy):
        """True, on no collision"""

        match (dx, dy):
            case (0, 1):
                return "e" if self.arr[3][4] == ord("e") else self.arr[3][4] == ord("x")
            case (0, -1):
                return "e" if self.arr[5][4] == ord("e") else self.arr[5][4] == ord("x")
            case (1, 0):
                return "e" if self.arr[4][3] == ord("e") else self.arr[4][3] == ord("x")
            case (-1, 0):
                return "e" if self.arr[4][5] == ord("e") else self.arr[4][5] == ord("x")
        return False
