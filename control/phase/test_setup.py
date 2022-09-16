import pytest
from .turn_order import TurnOrder

from control.test_game_state import game_state
from control.test_game_map import game_map, game_map_config

@pytest.fixture
def finish_setup(game_state):
    game_state.submit_command({'setup': [0, [1,1]]})
    game_state.submit_command({'setup': [1, [3,1]]})
    return game_state

def test_setup(game_state):
    game_state.submit_command({'setup': [0, [1,1]]})
    game_state.submit_command({'setup': [1, [3,1]]})
    assert isinstance(game_state.current_phase, TurnOrder)

def test_starting_position_error(game_state):
    game_state.submit_command({'setup': [0, [1,1]]})
    with pytest.raises(Exception, match="Start tile is out of bounds"):
        game_state.submit_command({'setup': [1, [0,1]]})
    with pytest.raises(Exception, match="Start tile is water"):
        game_state.submit_command({'setup': [1, [3,2]]})
    with pytest.raises(Exception, match="Start tile is already occupied"):
        game_state.submit_command({'setup': [1, [1,1]]})
    with pytest.raises(Exception, match="Start tile has neighbor occupied"):
        game_state.submit_command({'setup': [1, [2,1]]})