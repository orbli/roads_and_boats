import pytest
from control.phase.production import Production
from control.phase.turn_order import TurnOrder

from control.test_game_state import game_state
from control.test_game_map import game_map, game_map_config
from .test_setup import finish_setup

@pytest.fixture
def no_redetermination(finish_setup):
    game_state = finish_setup
    game_state.submit_command({'turn_order': ['to_pray', 0, False]})
    game_state.submit_command({'turn_order': ['to_pray', 1, False]})
    return game_state

def test_no_redetermination(no_redetermination):
    assert isinstance(no_redetermination.current_phase, Production)

@pytest.fixture
def subphase1(finish_setup):
    game_state = finish_setup
    game_state.submit_command({'turn_order': ['to_pray', 0, True]})
    game_state.submit_command({'turn_order': ['to_pray', 1, False]})
    return game_state

def test_subphase1(subphase1):
    assert isinstance(subphase1.current_phase, TurnOrder)
    assert subphase1.current_phase.sub_phase == 1

@pytest.fixture
def subphase2(subphase1):
    game_state = subphase1
    game_state.submit_command({'turn_order': ['pray', 1, True]})
    assert game_state.current_phase.new_pray_order == [1, None]
    game_state.submit_command({'turn_order': ['pray', 0, False]})
    return game_state

def test_subphase2(subphase2):
    assert isinstance(subphase2.current_phase, TurnOrder)
    assert subphase2.current_phase.sub_phase == 2
    assert subphase2.current_phase.new_pray_order == [1, 0]

@pytest.fixture
def subphase3(subphase2):
    game_state = subphase2
    game_state.submit_command({'turn_order': ['order', 1, 0]})
    assert game_state.current_phase.new_turn_order == [1, None]
    game_state.submit_command({'turn_order': ['order', 0, 1]})
    return game_state

def test_subphase3(subphase3):
    assert subphase3.turn_order == [1, 0]
    assert not isinstance(subphase3.current_phase, TurnOrder)