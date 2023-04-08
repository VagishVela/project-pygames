""" Implements the Battle view """

import pygame
from pygame import Surface
from pygame.sprite import Sprite
from views import View
import math


class Battle(View):
    """The Battle view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_turn = True
        self.player_pos = [self.width*0.2, self.height*0.5]
        self.player_image = pygame.transform.scale(
            pygame.image.load("assets/player.png"), (64, 96)
        )
        self.player_abilities = {
            "attack": 3,
            "damage": 20,
            "health": 100,
        }
        self.enemy_pos = [self.width*0.7, self.height*0.4]
        self.enemy_image = pygame.transform.scale(
            pygame.image.load("assets/enemy.png"), (64, 64)
        )
        self.enemy_abilities = {
            "attack": 5,
            "damage": 30,
            "health": 70,
        }
        self.projectiles = []
        self.player_attack()

    def on_update(self):
        for event in pygame.event.get():
            print("EVENT")
            if event.type == pygame.KEYDOWN:
                if self.my_turn:
                    if event.key == pygame.K_a:
                        self.player_attack()
                else:
                    if event.key == pygame.K_SPACE:
                        self.player_dodge()
        

    def player_attack(self):
        # play some Attack animation
        projectile_direction = (
            self.enemy_pos[0] - self.player_pos[0],
            self.enemy_pos[1] - self.player_pos[1],
        )
        self.projectiles.append(Projectile(self.player_pos, projectile_direction))

    def on_draw(self):
        self.screen.fill("#333333")
        self.screen.blit(self.player_image, (self.player_pos[0], self.player_pos[1]))
        self.screen.blit(self.enemy_image, (self.enemy_pos[0], self.enemy_pos[1]))
        for projectile in self.projectiles:
            projectile.update()
            projectile.draw(self.screen)

    def on_click(self):
        pass

class Projectile(Sprite):
    def __init__(self, pos: tuple[int, int] | list[int, int], direction: tuple[int, int]) -> None:
        self.x, self.y = pos
        self.direction = direction
        self.speed = 5
        self.image = pygame.transform.rotozoom(
            pygame.image.load("assets/fireball_1.png"), 
            -math.degrees(math.atan2(self.direction[1], self.direction[0])),
            1.5
        )
    def update(self):
        self.x += self.direction[0] * self.speed * 0.001
        self.y += self.direction[1] * self.speed * 0.001
    def draw(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))