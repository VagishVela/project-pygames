""" Implements the Battle view """

import pygame
from game.helper import Text, Button

from views import View


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

    def on_update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.my_turn:
                    if event.key == pygame.K_a:
                        self.player_attack()
                else:
                    if event.key == pygame.K_SPACE:
                        self.player_dodge()
        

    def player_attck():
        # play some Attack animation

        pass

    def on_draw(self):
        self.screen.fill("#333333")
        self.screen.blit(self.player_image, (self.player_pos[0], self.player_pos[1]))
        self.screen.blit(self.enemy_image, (self.enemy_pos[0], self.enemy_pos[1]))

    def on_click(self):
        pass

