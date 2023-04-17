""" Implements the Battle view """

import random
import typing

import pygame

from game.custom_event import PASS_VIEW, WAIT_FOR_ENEMY
from game.data import game_data
from game.data.states import GameState
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.utils import Text
from game.utils.bar import HealthBar
from game.views import View, logger

if typing.TYPE_CHECKING:
    from game.views.map import Map

# get logger
logger = logger.getChild("battle")


class Battle(View):
    """The Battle view"""

    # the map view
    # if not passed any view, preserve the previous one
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
        # store the enemy position on map
        self.enemy_map_pos = None

        # ------ states ------ #
        self.current_attack = None
        self.my_turn = True
        self.result = ""  # "lost" or "won"

    def pre_run(self, _spl_args) -> None:
        # get the game view before running this view
        if e := PASS_VIEW.get():
            Battle.game_view = e.view
        # get the player from Map view
        self.player: Player = Battle.game_view.player
        # get enemy position on the map
        self.enemy_map_pos = Battle.game_view.enemy_pos
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
        self.player.draw(self.screen, (70, self.height - 300), scale=(128, 192))
        self.enemy.draw(self.screen, self.width - 170, 100, scale=(96, 96))

        # draw the health bars
        HealthBar(self.player.max_health).draw(
            self.screen,
            self.player.abilities["health"],
            (60, self.height - 100),
            150,
            20,
        )
        HealthBar(self.enemy.max_health).draw(
            self.screen, self.enemy.abilities["health"], (self.width - 190, 50), 150, 20
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
                self.height - 400,
                30,
                (255, 255, 255),
            ).blit_into(self.screen)
            Text(
                f"Power: {self.current_attack['power']}",
                "sans-serif",
                self.width // 2,
                self.height - 360,
                20,
                (255, 255, 255),
            ).blit_into(self.screen)

    def on_keydown(self, event) -> None:
        if event.key == pygame.K_ESCAPE:
            # open the pause menu
            game_data.save_temp(GameState(Battle.game_view.screen_map.level.state))
            self.change_views('pause.Pause#{"escape":"battle.Battle#{\\"dummy\\":0}"}')

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
                # if opponent is alive after player's turn
                if not self.my_turn and self.enemy.abilities["health"] > 0:
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
            self._evaluate(_to)
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
            self._evaluate(_to)
        # flip sides if opponent survived the attack
        self.my_turn ^= True

    def _evaluate(self, opponent):
        """evaluate the fight whether the player won or lost"""
        # if enemy's dead
        if isinstance(opponent, Enemy):
            logger.debug("enemy is killed")
            self.win_battle()
        # if player's dead
        elif isinstance(opponent, Player):
            logger.debug("player is killed")
            self.game_over()

    def win_battle(self):
        """Called when the player wins"""
        self.result = "won"
        # enemy is killed
        # remove enemy from map
        Battle.game_view.screen_map.level.remove_enemy(self.enemy_map_pos)
        # regenerate and reload the map internally
        Battle.game_view.screen_map.regenerate = True
        Battle.game_view.screen_map.load()
        # TODO: give player XP and rewards

    def game_over(self):
        """Called when the player dies"""
        self.result = "lost"
        # TODO: reduce player XP
