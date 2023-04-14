""" Implements the Battle view """

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

        # -------- attacks and menu ----------- #

        self.attacks = [
            {"name": "Quick Attack", "power": 10},
            {"name": "Power Attack", "power": 20},
            {"name": "Super Attack", "power": 30},
            {"name": "Mega Attack", "power": 40},
        ]

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
            len(self.attacks) + self.num_buttons_per_row - 1
        ) // self.num_buttons_per_row

    def on_update(self):
        """Called every frame"""

    def win_game(self):
        """Called when the player wins"""
        # TODO Set the player abilities and health
        # TODO Go the the win view or map view

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

        _to.abilities["health"] -= power

        if _to.abilities["health"] <= 0:
            if isinstance(_to, Enemy):
                self.win_game()
            else:
                self.game_over()

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
        menu_rect = pygame.Rect(
            self.menu_x, self.menu_y, self.menu_width, self.menu_height
        )
        pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 2)

        Text(
            "Select an Attack",
            "sans-serif",
            self.menu_x + self.menu_width // 2,
            self.menu_y + 20,
            24,
            (255, 255, 255),
        ).blit_into(self.screen)

        for i, attack in enumerate(self.attacks):
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

    def on_click(self, event):
        """Called when the user clicks the mouse"""

        mouse_pos = event.pos
        for i, attack in enumerate(self.attacks):
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
                return
