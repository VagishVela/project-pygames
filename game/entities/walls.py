import pygame
from pygame import Surface
from pygame.sprite import Sprite


class Wall(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/wall.png"), (72, 72)
        )
        self.pos = x, y
        self.rect = self.image.get_rect()
        self.visible = True

    def draw(self, screen: Surface):
        screen.blit(self.image, self.pos)
