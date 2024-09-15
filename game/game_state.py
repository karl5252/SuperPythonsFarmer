"""This module contains the GameState enum class to represent the game state."""
from enum import Enum


class GameState(Enum):
    """Enum class to represent the game state."""
    MAIN_MENU = 0
    IN_GAME = 1
    GAME_OVER = 2
