""" Implements the Battle view """

import random
import typing

import pygame

from game.custom_event import PASS_VIEW, WAIT_FOR_ENEMY
from game.data import game_data
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.utils import Text
from game.views import View, logger

if typing.TYPE_CHECKING:
    from game.views.map import Map

# get logger
logger = logger.getChild("battle")


class Battle(View):
    """The Battle view"""

    # the map view
    game_view: "Map" = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # -------- buttons ----------- #
        self.menu_width = 400
        self.menu_height = 300
        self.menu_x = self.width - self.menu_width - 20
        self.menu_y = self.height - self.menu_height - 20

        self.button_width = 160
        self.button_height = 60
        self.button_spacing = 20
        self.num_buttons_per_row = 2

        # --- depends on the game view --- #
        self.num_rows = None
        self.player = None
        self.enemy = Enemy()

        # ------ states ------ #
        self.current_attack = None
        self.my_turn = True
        self.result = ""  # "lost" or "won"

    def pre_run(self, _spl_args) -> None:
        # get the game view before running this view
        if e := PASS_VIEW.get():
            Battle.game_view = e.view
        self.player: Player = Battle.game_view.player
        num_attacks = len(self.player.attacks)
        self.num_rows = (
            num_attacks + self.num_buttons_per_row - 1
        ) // self.num_buttons_per_row

    def on_draw(self) -> None:
        """Draw the battle view"""

        if not getattr(self, "game_view"):
            raise RuntimeError(
                "Battle was not initiated properly, use PASS_VIEW to pass the Map "
                "view"
            )

        # draw the results view
        if self.result == "won":
            Text(
                "You won!",
                self.font,
                self.width / 2,
                self.height / 2 - 50,
                100,
                "red",
            ).blit_into(self.screen)
            Text(
                "Click to return to map!",
                self.font,
                self.width / 2,
                self.height / 2 + 50,
                50,
                "white",
            ).blit_into(self.screen)
            return
        if self.result == "lost":
            Text(
                "You lost.",
                self.font,
                self.width / 2,
                self.height / 2 - 50,
                100,
                "red",
            ).blit_into(self.screen)
            Text(
                "Click to return to map!",
                self.font,
                self.width / 2,
                self.height / 2 + 50,
                50,
                "white",
            ).blit_into(self.screen)
            return

        # draw the player and the enemy
        self.player.draw(self.screen, (50, 200))
        self.enemy.draw(self.screen, self.width - 150, 100)

        # draw the health bars
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(10, 10, 150, 20))
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
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
            (
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

        if not self.my_turn:
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

    def on_keydown(self, event) -> None:
        if event.key == pygame.K_ESCAPE:
            # open the pause menu
            game_data.save_temp((Battle.game_view.screen_map.level.loc, []))
            self.change_views('pause.Pause#{"escape":"batoru.Battle#{\\"dummy\\":0}"}')

    def on_click(self, event) -> None:
        """Called when the user clicks the mouse"""

        # if result view is shown
        if self.result:
            self.change_views("map.Map")
            return

        # not player's turn
        if not self.my_turn:
            return

        mouse_pos = event.pos
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
                self.attack(self.player, self.enemy, attack)
                # if alive after his turn
                if self.player.abilities["health"] > 0 and not self.my_turn:
                    # wait 2 seconds
                    WAIT_FOR_ENEMY.wait(2000)

    def on_update(self) -> None:
        """Called every frame"""
        # wait for the enemy
        if WAIT_FOR_ENEMY.get():
            self.attack(self.enemy, self.player, random.choice(self.enemy.attacks))

    def attack(
        self, _from: Player | Enemy, _to: Player | Enemy, attack: dict[str, ...]
    ) -> None:
        """Called when the player selects an attack or enemy attacks"""

        # if opponent's already dead
        if _to.abilities["health"] <= 0:
            return
        # set current attack
        self.current_attack = {
            "name": f"{_from.name} used {attack['name']}!",
            "power": attack["power"],
        }

        # deduct health
        _to.abilities["health"] -= attack["power"]
        # if last attack killed the opponent
        if _to.abilities["health"] <= 0:
            # if enemy's dead
            if isinstance(_to, Enemy):
                logger.debug("enemy is killed")
                self.win_battle()
                return
            # if player's dead
            if isinstance(_to, Player):
                logger.debug("player is killed")
                self.game_over()
                return
        # flip sides if opponent survived the attack
        self.my_turn ^= True

    def win_battle(self):
        """Called when the player wins"""
        self.result = "won"
        # TODO: give player XP and rewards

    def game_over(self):
        """Called when the player dies"""
        self.result = "lost"
        # TODO: reduce player XP
