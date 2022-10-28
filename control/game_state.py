
from control.phase.turn_order import TurnOrder
from .phase.setup import Setup
from .phase.placement import Placement
from .game_player import GamePlayer
from random import shuffle
from math import floor
from .phase.production import Production
from .phase.movement import Movement
from .phase.building import Building
from .phase.wonder import Wonder

class GameState:
    current_phase = None
    current_phase_number = None
    pray_order = None
    turn_order = None
    map = None
    players = None
    wonder = None

    def __init__(self):
        None
    
    def start_new_game(self, player: int, map=None):
        turn_order = list(range(player))
        shuffle(turn_order)
        self.pray_order = turn_order
        self.turn_order = turn_order
        self.players = [GamePlayer() for _ in range(player)]
        self.current_phase_number = 0
        if map is None:
            self.current_phase = Placement(turn_order)
        else:
            self.map = map
            self.current_phase = Setup(turn_order)
        self.wonder = []

    def submit_command(self, command):
        self.current_phase = self.current_phase.process_command(self, command)
        if self.current_phase is None:
            self.progress_phase()
        while not self.current_phase.waiting_user_input():
            self.current_phase = self.current_phase.process(self)
            if self.current_phase is None:
                self.progress_phase()

    def progress_phase(self):
        if self.current_phase_number == 4:
            self.current_phase_number = 1
        else:
            self.current_phase_number += 1

        self.current_phase = TurnOrder(self.pray_order, [Production, Movement, Building, Wonder][self.current_phase_number - 1])

    # wonder_helpers
    def desert_as_pasture(self):
        return len(self.wonder) > 44

    def game_end(self):
        return len(self.wonder) == [-1, -1, 62, 66, 69, 76, 83][len(self.players)] or self.wonder.count(-1) >= 33
    
    def wonder_score(self):
        rt = [0] * len(self.players)
        counted_wonders = 0
        for i, j in [(3,4), (4,5), (5,6), (3,7)]:
            for _ in range(i):
                row = self.wonder[counted_wonders:counted_wonders+j]
                if len(row) == 0:
                    return rt
                denominator = len(row) - row.count(-1)
                numerator = [ row.count(i) for i in range(len(self.players)) ]
                row_score = [ floor(10 * numerator[i] / denominator) for i in range(len(self.players))]
                rt = [ rt[i] + row_score[i] for i in range(len(self.players)) ]
                counted_wonders += j
        return rt

    def export(self):
        return {
            "current_phase": self.current_phase.export(),
            "pray_order": self.pray_order,
            "wonder": self.wonder,
            "turn_order": self.turn_order,
            "map": self.map.export_state(),
            "players": [player.export_state() for player in self.players],
        }