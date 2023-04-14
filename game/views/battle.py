""" Implements the Battle view """
import random

import pygame

from game.entities.enemy import Enemy
from game.entities.player import Player
from game.utils import Text
from game.views import View


class Battle(View):
    """The Battle view"""

    def __init__(self, size, caption, icon, bg_color):
        """Initialize the battle view"""
        super().__init__(size, caption, icon, bg_color)
        self.my_turn = True

        self.player = Player()
        self.player.pos = (self.width * 0.1, self.height * 0.6)

        self.enemy = Enemy(self.width * 0.7, self.height * 0.25, (64, 64))

        self.menu_width = 400
        self.menu_height = 300
        self.menu_x = self.width - self.menu_width - 20
        self.menu_y = self.height - self.menu_height - 20

        # -------- buttons ----------- #

        self.button_width = 160
        self.button_height = 60
        self.button_spacing = 20
        self.num_buttons_per_row = 2
        self.num_rows = (
            len(self.player.attacks) + self.num_buttons_per_row - 1
        ) // self.num_buttons_per_row

        self.current_attack = None
        self.waiting_for_enemy = False

    def on_update(self):
        """Called every frame"""

    def win_battle(self):
        """Called when the player wins"""
        # TODO have a screen that shows the player won
        # TODO Set the player abilities and health
        # TODO Go the the win view or map view
        self.change_views("map.Map", caption="Map")

    def game_over(self):
        """Called when the player dies"""
        self.enemy.kill()  # Kill the enemy and remove reference
        self.enemy = None
        # TODO Give the player some coins

    def attack(self, _from: Player | Enemy, _to: Player | Enemy, power: int):
        """Called when the player selects an attack"""
        if _from == self.player:
            if not self.my_turn:
                return
            self.my_turn = False
        else:
            if self.my_turn:
                return
            self.my_turn = True

        if isinstance(_to, Player):
            _to.abilities["health"] -= power
            if _to.abilities["health"] <= 0:
                self.game_over()
        elif isinstance(_to, Enemy):
            _to.abilities["health"] -= power
            if _to.abilities["health"] <= 0:
                self.win_battle()

        self.waiting_for_enemy = True
        attack_name = [
            attack["name"] for attack in _from.attacks if attack["power"] == power
        ][0]
        self.current_attack = {
            "name": f"{_from.name} used {attack_name}!",
            "power": power,
        }

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
                150 * self.player.abilities["health"] / self.player.max_health
                if self.player.abilities["health"] > 0
                else 0,
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
                150 * self.enemy.abilities["health"] / self.enemy.max_health
                if self.enemy
                else 0,
                20,
            ),
        )

        # draw the attack menu
        menu_rect = pygame.Rect(
            self.menu_x, self.menu_y, self.menu_width, self.menu_height
        )
        pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 2)

        if self.waiting_for_enemy:
            Text(
                "Waiting for Alien to make a move...",
                "sans-serif",
                self.menu_x + self.menu_width // 2,
                self.menu_y + 20,
                24,
                (255, 255, 255),
            ).blit_into(self.screen)
        else:
            Text(
                "Select an Attack",
                "sans-serif",
                self.menu_x + self.menu_width // 2,
                self.menu_y + 20,
                24,
                (255, 255, 255),
            ).blit_into(self.screen)

            for i, attack in enumerate(self.player.attacks):
                row = i // self.num_buttons_per_row
                col = i % self.num_buttons_per_row
                button_x = (
                    self.menu_x
                    + col * (self.button_width + self.button_spacing)
                    + self.button_spacing
                )
                button_y = (
                    self.menu_y + row * (self.button_height + self.button_spacing) + 80
                )
                button_rect = pygame.Rect(
                    button_x, button_y, self.button_width, self.button_height
                )
                pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
                Text(
                    attack["name"],
                    "sans-serif",
                    button_x + self.button_width // 2,
                    button_y + 20,
                    20,
                    (255, 255, 255),
                ).blit_into(self.screen)
                Text(
                    f"Power: {attack['power']}",
                    "sans-serif",
                    button_x + self.button_width // 2,
                    button_y + 40,
                    14,
                    (255, 255, 255),
                ).blit_into(self.screen)

        # draw current attack info
        if self.current_attack is not None:
            Text(
                f"{self.current_attack['name']}!",
                "sans-serif",
                self.width // 2,
                self.height - 100,
                30,
                (255, 255, 255),
            ).blit_into(self.screen)
            Text(
                f"Power: {self.current_attack['power']}",
                "sans-serif",
                self.width // 2,
                self.height - 60,
                20,
                (255, 255, 255),
            ).blit_into(self.screen)

    def on_click(self, event):
        """Called when the user clicks the mouse"""

        mouse_pos = event.pos
        if self.waiting_for_enemy:
            return
        for i, attack in enumerate(self.player.attacks):
            row = i // self.num_buttons_per_row
            col = i % self.num_buttons_per_row
            button_x = (
                self.menu_x
                + col * (self.button_width + self.button_spacing)
                + self.button_spacing
            )
            button_y = (
                self.menu_y + row * (self.button_height + self.button_spacing) + 80
            )
            button_rect = pygame.Rect(
                button_x, button_y, self.button_width, self.button_height
            )
            if button_rect.collidepoint(mouse_pos):
                self.attack(self.player, self.enemy, attack["power"])
                if self.enemy.abilities["health"] >= 0:
                    self.waiting_for_enemy = True
                    # pygame.time.set_timer(pygame.USEREVENT, 2000)
                    self.attack(
                        self.enemy,
                        self.player,
                        random.choice(self.enemy.attacks)["power"],
                    )
                    # TODO if the player dies, have a screen that shows the player lost
                    self.waiting_for_enemy = False
                else:
                    self.win_battle()
