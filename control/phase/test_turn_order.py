import pytest
from control.phase.production import Production
from control.phase.turn_order import TurnOrder

from control.test_game_state import game_state
from .test_setup import finish_setup

def test_no_redeetermination(finish_setup):
    game_state = finish_setup
    game_state.submit_command({'turn_order': ['to_pray', 0, False]})
    game_state.submit_command({'turn_order': ['to_pray', 1, False]})
    game_state.submit_command({'turn_order': ['to_pray', 2, False]})
    game_state.submit_command({'turn_order': ['to_pray', 3, False]})
    assert isinstance(game_state.current_phase, Production)

def test_no_redeetermination_without_last(finish_setup):
    game_state = finish_setup
    game_state.submit_command({'turn_order': ['to_pray', 0, False]})
    game_state.submit_command({'turn_order': ['to_pray', 1, False]})
    game_state.submit_command({'turn_order': ['to_pray', 3, False]})
    assert isinstance(game_state.current_phase, Production)

@pytest.fixture
def no_redetermination(finish_setup):
    game_state = finish_setup
    game_state.submit_command({'turn_order': ['to_pray', 0, False]})
    game_state.submit_command({'turn_order': ['to_pray', 1, False]})
    game_state.submit_command({'turn_order': ['to_pray', 2, False]})
    game_state.submit_command({'turn_order': ['to_pray', 3, False]})
    return game_state

# sub phase 1

@pytest.fixture
def subphase1(finish_setup):
    game_state = finish_setup
    game_state.submit_command({'turn_order': ['to_pray', 0, True]})
    return game_state

def test_subphase1(subphase1):
    assert isinstance(subphase1.current_phase, TurnOrder)
    assert subphase1.current_phase.sub_phase == 1


@pytest.fixture
def subphase2(subphase1):
    game_state = subphase1
    game_state.submit_command({'turn_order': ['pray', 3, False]})
    game_state.submit_command({'turn_order': ['pray', 1, True]})
    game_state.submit_command({'turn_order': ['pray', 0, True]})
    assert game_state.current_phase.new_pray_order == [1, 0, 2, 3]
    return game_state

def test_subphase2(subphase2):
    assert isinstance(subphase2.current_phase, TurnOrder)
    assert subphase2.current_phase.sub_phase == 2

@pytest.fixture
def subphase3(subphase2):
    game_state = subphase2
    game_state.submit_command({'turn_order': ['order', 1, 1]})
    game_state.submit_command({'turn_order': ['order', 0, 0]})
    game_state.submit_command({'turn_order': ['order', 2, 2]})
    game_state.submit_command({'turn_order': ['order', 3, 3]})
    assert game_state.turn_order == [0, 1, 2, 3]
    return game_state

def test_subphase3(subphase3):
    assert subphase3.pray_order == [1, 0, 2, 3]
    assert not isinstance(subphase3.current_phase, TurnOrder)