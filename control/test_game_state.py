import pytest
from .game_state import GameState

from .test_game_map import game_map, game_map_config
import random

@pytest.fixture
def game_state(game_map):
    random.seed(0)
    gs = GameState()
    gs.start_new_game(2, game_map)
    return gs

def test_game_state(game_state):
    assert game_state.turn_order == [0, 1]