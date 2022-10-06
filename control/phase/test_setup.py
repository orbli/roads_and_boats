import pytest
from .turn_order import TurnOrder

from control.test_game_state import game_state

@pytest.fixture
def finish_setup(game_state):
    game_state.submit_command({'setup': [2, [1,7]]})
    game_state.submit_command({'setup': [0, [1,1]]})
    game_state.submit_command({'setup': [1, [6,1]]})
    game_state.submit_command({'setup': [3, [6,7]]})
    return game_state

def test_setup(game_state):
    game_state.submit_command({'setup': [2, [1,7]]})
    game_state.submit_command({'setup': [0, [1,1]]})
    game_state.submit_command({'setup': [1, [6,1]]})
    game_state.submit_command({'setup': [3, [6,7]]})
    assert isinstance(game_state.current_phase, TurnOrder)

def test_starting_position_error(game_state):
    assert not isinstance(game_state.current_phase, TurnOrder)
    assert game_state.map[[1,7]].resource_tokens == {}
    game_state.submit_command({'setup': [2, [1,7]]})
    with pytest.raises(Exception, match="Start tile is out of bounds"):
        game_state.submit_command({'setup': [0, [0,0]]})
    with pytest.raises(Exception, match="Start tile is water"):
        game_state.submit_command({'setup': [0, [3,0]]})
    with pytest.raises(Exception, match="Start tile is already occupied"):
        game_state.submit_command({'setup': [0, [1,7]]})
    with pytest.raises(Exception, match="Start tile has neighbor occupied"):
        game_state.submit_command({'setup': [0, [2,7]]})