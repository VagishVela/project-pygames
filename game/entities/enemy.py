import pygame.image
from pygame import Surface
from pygame.sprite import Sprite, Group


class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/enemy.png"), (32, 32)
        )
        self.pos = x, y
        self.rect = self.image.get_rect()
        self.visible = True

    def draw(self, screen: Surface):
        screen.blit(self.image, self.pos)


class NotPlayer(Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface: Surface, bgsurf=None, special_flags: int = 0):
        for sprite in self.sprites():
            if sprite.visible:
                sprite.draw(surface)

    def disappear(self, sprites):
        for sprite in sprites:
            if sprite in self.sprites():
                sprite.visible = False
