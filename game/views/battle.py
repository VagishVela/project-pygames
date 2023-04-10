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
        """Initialize the battle view"""
        super().__init__(*args, **kwargs)
        self.my_turn = True

        self.player = Player()
        self.player.pos = (self.width * 0.1, self.height * 0.6)

        self.enemy = Enemy(self.width * 0.7, self.height * 0.25, (64, 64))
        self.projectiles = []
        self.dodge_timer = 0
        self.dodge_for_frames = 60
        #        self.buttons

        self.attack(self.player, self.enemy)  # remove this when inputs are working

    def on_update(self):
        """Called every frame"""
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
        """Called when the player wins"""
        # TODO Set the player abilities and health
        # TODO Go the the win view or map view
        pass

    def game_over(self):
        """Called when the player dies"""
        self.enemy = self.enemy.kill()  # Kill the enemy and remove reference
        # TODO Give the player some coins
        # TODO Go the the Game over view

    def attack(self, _from: Player | Enemy, _to: Player | Enemy):
        """Called when the player presses the A key"""
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
        """Called when the player presses the space bar"""
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
        """Draw the battle view"""
        self.screen.fill((0, 0, 0))

        # draw the player and the enemy
        self.screen.blit(pygame.image.load("assets/player.png"), (50, 200))
        self.screen.blit(pygame.image.load("assets/enemy.png"), (self.width - 150, 50))

        # draw the health bars
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(10, 10, 150, 20))
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            pygame.Rect(
                10,
                10,
                150 * self.player.abilities["health"] / self.player.max_health,
                20,
            ),
        )

        pygame.draw.rect(
            self.screen, (255, 255, 255), pygame.Rect(self.width - 160, 50, 150, 20)
        )
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            pygame.Rect(
                self.width - 160,
                50,
                150 * self.enemy.abilities["health"] / self.enemy.max_health,
                20,
            ),
        )

        # draw the attack menu
        menu_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 80)
        pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 2)

        Text(
            "Select an Attack",
            "sans-serif",
            self.width // 2,
            menu_rect.y + 10,
            24,
            (255, 255, 255),
        ).blit_into(self.screen)

        Text(
            "1. Quick Attack",
            "sans-serif",
            self.width // 2,
            menu_rect.y + 40,
            20,
            (255, 255, 255),
        ).blit_into(self.screen)

        Text(
            "2. Power Attack",
            "sans-serif",
            self.width // 2,
            menu_rect.y + 60,
            20,
            (255, 255, 255),
        ).blit_into(self.screen)

    def on_click(self):
        """Called when the user clicks the mouse"""
        pass


class Projectile(Sprite):
    def __init__(
        self,
        pos: tuple[int, int] | list[int, int],
        direction: tuple[int, int],
        is_player=True,
    ) -> None:
        """Create a new projectile"""
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
        """Update the projectile position"""
        self.x += self.direction[0] * self.speed * 1
        self.y += self.direction[1] * self.speed * 1

    def draw(self, screen: Surface):
        """Draw the projectile on the screen"""
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, entity: Player | Enemy):
        """Check if the projectile is colliding with the entity"""
        return not (
            self.x + self.rect.w / 2 < entity.pos[0]
            or self.x + self.rect.w / 2 > entity.pos[0] + entity.rect.w
            or self.y + self.rect.h / 2 < entity.pos[1]
            or self.y + self.rect.h / 2 > entity.pos[1] + entity.rect.h
        )
