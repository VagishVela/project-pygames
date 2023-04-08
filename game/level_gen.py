# P is player
# E is Enemy -> En can be a way to have many different enemies
# W is wall -> Wn can be a way to have more obstacles
# x is walkable

import itertools
import random

import numpy as np


class Level:
    def __init__(self, x=None, y=None):
        self.x = 0
        self.y = 0
        self.arr = np.zeros((9, 9), dtype=np.int32)
        self.arr.fill(ord("x"))
        self.rng = random.Random()
        self.loc = [x, y] if x is not None and y is not None else [0, 0]

    def _get_tile(self, pos):
        self.rng.seed(str(pos))
        return ord(self.rng.choice("x" * 800 + "w" * 185 + "e" * 15))

    def generate(self, m=9, n=9):
        x, y = self.loc
        for i, j in itertools.product(range(m), range(n)):
            if i == m // 2 and j == n // 2:
                self.arr[4][4] = ord("p")
            else:
                self.arr[i][j] = self._get_tile((y - i, x - j))
        return self.arr.tolist()

    def move(self, x, y):
        if self.check_collision(x, y):
            self.loc[0] += x
            self.loc[1] += y
            return True
        return False

    def check_collision(self, x, y):
        """True, on no collision"""

        match (x, y):
            case (0, 1):
                return self.arr[3][4] == ord("x")
            case (0, -1):
                return self.arr[5][4] == ord("x")
            case (1, 0):
                return self.arr[4][3] == ord("x")
            case (-1, 0):
                return self.arr[4][5] == ord("x")
        return False
