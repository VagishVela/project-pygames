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
        self.abilities = {
            "attack": 3,
            "damage": 20,
            "health": 100,
        }

    def draw(self, screen: Surface, world_spece=False):
        if not world_spece:
            screen.blit(
                self.image,
                (
                    screen.get_width() / 2 - self.pos[0],
                    screen.get_height() / 2 - self.pos[1],
                ),
            )
        else:
            screen.blit(self.image, (self.pos[0], self.pos[1]))
