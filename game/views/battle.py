""" Implements the Battle view """

import math

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.entities.enemy import Enemy
from game.entities.player import Player
from game.utils import Text
from game.views import View


class Battle(View):
    """The Battle view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_turn = True

        self.player = Player()
        self.player.pos = (self.width * 0.2, self.height * 0.5)

        self.enemy = Enemy(self.width * 0.7, self.height * 0.4, (64, 64))
        self.projectiles = []
        self.dodge_timer = 0
        self.dodge_for_frames = 60
        #        self.buttons

        self.attack(self.player, self.enemy)  # remove this when inputs are working

    def on_update(self):
        for projectile in self.projectiles:
            projectile.update()
            if projectile.check_collision(self.enemy) or projectile.check_collision(
                self.player
            ):
                self.projectiles.remove(projectile)
                if projectile.is_player:
                    died = self.enemy.take_damage(self.player.abilities)
                    if died:
                        self.win_game()
                else:
                    if self.dodge_timer <= 0:
                        died = self.player.take_damage(self.enemy.abilities)
                        if died:
                            self.game_over()
                    self.my_turn = True

                # TODO Somehow wait for some seconds and execute the next line
                if not self.my_turn:
                    self.attack(self.enemy, self.player)

        ##### EVENTS ARE NOT WORKING AT ALL !!!!!!!!!!!!!1
        # TODO fix the keyboard input :(

        for event in pygame.event.get():
            print("EVENT")
            if event.type == pygame.KEYDOWN:
                if self.my_turn:
                    if event.key == pygame.K_a:
                        self.attack(self.player, self.enemy)
                else:
                    if event.key == pygame.K_SPACE:
                        self.player_dodge()

    def win_game(self):
        # TODO Set the player abilities and health
        # TODO Go the the win view or map view
        pass

    def game_over(self):
        self.enemy = self.enemy.kill()  # Kill the enemy and remove reference
        # TODO Give the player some coins
        # TODO Go the the Game over view

    def attack(self, _from: Player | Enemy, _to: Player | Enemy):
        # play some Attack animation
        projectile_direction = pygame.math.Vector2(
            (_to.pos[0] + _to.rect[0] / 2) - _from.pos[0],
            (_to.pos[1] + _to.rect[1] / 2) - _from.pos[1],
        )
        projectile_direction = projectile_direction.normalize()
        projectile_position = (
            _from.pos[0] + projectile_direction.x * 50,
            _from.pos[1] + projectile_direction.y * 50,
        )
        self.projectiles.append(
            Projectile(
                projectile_position, tuple(projectile_direction), type(_from) == Player
            )
        )
        if type(_from) == Player:
            self.my_turn = False

    def player_dodge(self):
        if self.my_turn:
            return
        if self.dodge_timer <= 0:
            self.dodge_timer = self.dodge_for_frames
            self.player.dodging = True
        else:
            self.dodge_timer -= 1
            self.dodge_timer = pygame.math.clamp(
                self.dodge_timer, 0, self.dodge_for_frames
            )
        if self.dodge_timer == 0:
            self.player.dodging = False

    def on_draw(self):
        self.screen.fill("#333333")
        dialog_box_rect = (
            self.screen.get_width() * 0.1,
            20,
            self.screen.get_width() * 0.8,
            100,
        )
        dialog_box_color = (200, 200, 200)
        pygame.draw.rect(self.screen, dialog_box_color, dialog_box_rect, 0, 20)
        for i, text in enumerate(self.enemy.details):
            Text(
                text,
                "sans-serif",
                self.screen.get_width() / 2,
                dialog_box_rect[1] + 30 * (i + 1),
                24,
                (0, 0, 0),
            ).blit_into(self.screen)
        self.player.draw(self.screen, True)
        self.enemy.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        self.draw_health(self.player)
        self.draw_health(self.enemy)

    def draw_health(self, entity: Player | Enemy):
        width = 100
        pygame.draw.rect(
            self.screen, (0, 0, 0), (entity.pos[0] - 10, entity.pos[1] - 40, width, 20)
        )
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
                entity.pos[0] - 10,
                entity.pos[1] - 40,
                width * entity.abilities["health"] / entity.max_health,
                20,
            ),
        )

    def on_click(self):
        pass


class Projectile(Sprite):
    def __init__(
        self,
        pos: tuple[int, int] | list[int, int],
        direction: tuple[int, int],
        is_player=True,
    ) -> None:
        self.x, self.y = pos
        self.direction = direction
        self.is_player = is_player
        self.speed = 5
        self.image = pygame.transform.rotozoom(
            pygame.image.load("assets/fireball_1.png"),
            -math.degrees(math.atan2(self.direction[1], self.direction[0])),
            1.5,
        )
        self.rect = self.image.get_rect()

    def update(self):
        self.x += self.direction[0] * self.speed * 1
        self.y += self.direction[1] * self.speed * 1

    def draw(self, screen: Surface):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, entity: Player | Enemy):
        return not (
            self.x + self.rect.w / 2 < entity.pos[0]
            or self.x + self.rect.w / 2 > entity.pos[0] + entity.rect.w
            or self.y + self.rect.h / 2 < entity.pos[1]
            or self.y + self.rect.h / 2 > entity.pos[1] + entity.rect.h
        )
