import pygame.image
from pygame import Surface
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/player.png"), (64, 96)
        )
        self.pos = self.image.get_width() / 2, self.image.get_height() / 2
        self.rect = self.image.get_rect()

    def draw(self, screen: Surface):
        screen.blit(
            self.image,
            (
                screen.get_width() / 2 - self.pos[0],
                screen.get_height() / 2 - self.pos[1],
            ),
        )
