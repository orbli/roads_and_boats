import pytest
from .game_state import GameState

from .constants import DefaultMap
import random

@pytest.fixture
def game_state():
    random.seed(0)
    game_state = GameState()
    game_state.start_new_game(4, DefaultMap.FourSailors())
    return game_state

def test_game_state(game_state):
    assert game_state.turn_order == [2, 0, 1, 3]

def test_wonder_score(game_state):
    game_state.wonder = [1,2,-1,3,1,-1,-1,3,2,0,0,1]
    assert game_state.wonder_score() == [5, 10, 5, 8]

    game_state.wonder = [1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1]
    assert game_state.wonder_score() == [13, 20, 10, 13]

    game_state.wonder = [1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1]
    assert game_state.wonder_score() == [15, 25, 14, 19]

    game_state.wonder = [1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1]
    assert game_state.wonder_score() == [18, 31, 17, 25]

    game_state.wonder = [1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1,1,2,-1,3,1,-1,-1,3,2,0,0,1]
    assert game_state.wonder_score() == [21, 37, 20, 31]

    assert game_state.desert_as_pasture()
