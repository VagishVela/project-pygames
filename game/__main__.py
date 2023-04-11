""" All game logic is implemented in this module """

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE
from game.views.start import Start


def main():
    """The main function, initiates and runs the game"""

    game = Start((SCREEN_WIDTH, SCREEN_HEIGHT), GAME_TITLE)
    game.run()
