import pygame
from enum import Enum

from src.views.start_view import StartView
from src.views.menu_view import MenuView
from src.views.game_view import GameView
from src.views.battle_view import BattleView
from src.views.inventory_view import InventoryView
from src.views.game_over_view import GameOverView
from src.views.pause_view import PauseView

# Define different views
class View(Enum):
    StartView = 0
    MenuView = 1
    GameView = 2
    BattleView = 3
    InventoryView = 4
    GameOverView = 5
    PauseView = 6

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialize view instances
view_instances = {
    View.StartView: StartView(),
    View.MenuView: MenuView(),
    View.GameView: GameView(),
    View.BattleView: BattleView(),
    View.InventoryView: InventoryView(),
    View.GameOverView: GameOverView(),
    View.PauseView: PauseView()
}

# Set the initial view
current_view = View.StartView

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render the current view
    view_instances[current_view].render(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
