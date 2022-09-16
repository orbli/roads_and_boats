
from .phase.setup import Setup
from .phase.placement import Placement
from .game_player import GamePlayer
from random import shuffle

class GameState:
    current_phase = None
    pray_order = None
    turn_order = None
    map = None
    players = None

    def __init__(self):
        None
    
    def start_new_game(self, player: int, map=None):
        turn_order = list(range(player))
        shuffle(turn_order)
        self.pray_order = turn_order
        self.turn_order = turn_order
        self.players = [GamePlayer() for _ in range(player)]
        if map is None:
            self.current_phase = Placement(turn_order)
        else:
            self.map = map
            self.current_phase = Setup(turn_order)

    def submit_command(self, command):
        self.current_phase = self.current_phase.process_command(self, command)
        while not self.current_phase.waiting_user_input():
            self.current_phase = self.current_phase.process(self)