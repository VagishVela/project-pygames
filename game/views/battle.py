""" Implements the Battle view """

from asyncio import sleep
import pygame
from pygame import Surface
from pygame.sprite import Sprite
from game.entities.enemy import Enemy
from game.entities.player import Player
from views import View
import math


class Battle(View):
    """The Battle view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_turn = True

        self.player = Player()
        self.player.pos = (self.width*0.2, self.height*0.5)

        self.enemy = Enemy(self.width*0.7, self.height*0.4, (64, 64))
        self.projectiles = []
        self.player_attack()

    def on_update(self):
        for projectile in self.projectiles:
            projectile.update()
            if projectile.check_collision(self.enemy) or projectile.check_collision(self.player):
                self.projectiles.remove(projectile)
                if projectile.is_mine: 
                    self.enemy.take_damage(self.player.abilities)
                else: 
                    self.player.take_damage(self.enemy.abilities)
                    self.my_turn = True

                # TODO Somehow wait for some seconds and execute the next line
                if not self.my_turn: self.enemy_attack()

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
        projectile_direction = pygame.math.Vector2(
            (self.enemy.pos[0] + self.enemy.rect[0]/2) - self.player.pos[0],
            (self.enemy.pos[1] + self.enemy.rect[1]/2) - self.player.pos[1]
        )
        projectile_direction = projectile_direction.normalize()
        projectile_position = (
            self.player.pos[0] + projectile_direction.x*50,
            self.player.pos[1] + projectile_direction.y*50
        )
        self.projectiles.append(Projectile(projectile_position, tuple(projectile_direction), True))
        self.my_turn = False
    
    def enemy_attack(self):
        # play some Attack animation
        projectile_direction = pygame.math.Vector2(
            (self.enemy.pos[0] + self.enemy.rect[0]/2) - self.player.pos[0],
            (self.enemy.pos[1] + self.enemy.rect[1]/2) - self.player.pos[1]
        )
        projectile_direction = -projectile_direction.normalize()
        projectile_position = (
            self.enemy.pos[0] + projectile_direction.x*50,
            self.enemy.pos[1] + projectile_direction.y*50
        )
        self.projectiles.append(Projectile(projectile_position, tuple(projectile_direction), False))
    

    def player_dodge(self):
        pass

    def on_draw(self):
        self.screen.fill("#333333")
        self.player.draw(self.screen, True)
        self.enemy.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)

    def on_click(self):
        pass

class Projectile(Sprite):
    def __init__(self, pos: tuple[int, int] | list[int, int], direction: tuple[int, int], is_mine=True) -> None:
        self.x, self.y = pos
        self.direction = direction
        self.is_mine = is_mine
        self.speed = 5
        self.image = pygame.transform.rotozoom(
            pygame.image.load("assets/fireball_1.png"), 
            -math.degrees(math.atan2(self.direction[1], self.direction[0])),
            1.5
        )
        self.rect = self.image.get_rect()

    def update(self):
        self.x += self.direction[0] * self.speed * 1
        self.y += self.direction[1] * self.speed * 1

    def draw(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, entity: Player | Enemy):
        return not (
            self.x + self.rect.w/2 < entity.pos[0] or 
            self.x + self.rect.w/2 > entity.pos[0]+entity.rect.w or 
            self.y + self.rect.h/2 < entity.pos[1] or 
            self.y + self.rect.h/2 > entity.pos[1]+entity.rect.h
        )