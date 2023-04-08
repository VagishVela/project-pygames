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
        self.has_shield = True
        self.dodging = False
    
    def take_damage(self, e_ability):
        self.abilities["health"] -= (e_ability["attack"] * (100-self.abilities["damage"])/100)

    def draw(self, screen: Surface, world_spece=False):
        if not world_spece:
            pos = (
                    screen.get_width() / 2 - self.pos[0],
                    screen.get_height() / 2 - self.pos[1],
                )
        else:
            pos = (self.pos[0], self.pos[1])
        screen.blit(self.image, pos)
            
        if self.dodging:
            pygame.draw.circle(screen, pygame.Color(255, 255, 255, 50), pos, self.rect.w*1.5)
