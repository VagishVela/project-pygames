import pygame.image
from pygame import Surface
from pygame.sprite import Sprite, Group


class Enemy(Sprite):
    def __init__(self, x, y, scale=(32, 32)):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/enemy.png"), scale
        )
        self.pos = x, y
        self.rect = self.image.get_rect()
        self.abilities = {
            "attack": 5,
            "damage": 30,
            "health": 70,
        }
        self.max_health = 70
        self.details = ["I am Quantalocus.", "A deadly Alien with no special abilities"]
        self.visible = True

    def take_damage(self, p_ability):
        self.abilities["health"] -= (
            p_ability["attack"] * (100 - self.abilities["damage"]) / 100
        )
        # Return true if the enemy dies
        return self.abilities["health"] <= 0

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
