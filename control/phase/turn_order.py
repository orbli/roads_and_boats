from .phase import Phase
from .production import Production
from .movement import Movement
from .building import Building
from .wonder import Wonder

class TurnOrder(Phase):
    pray_order = None
    next_phase = None
    sub_phase = None
    # sub_phase 0
    redetermine_order = []
    # sub_phase 1
    new_pray_order = None
    current_player_pray_order_pos = None
    # sub_phase 2
    new_turn_order = None
    current_player_pray_order_pos = None


    def __init__(self, pray_order, phase):
        self.pray_order = pray_order
        self.next_phase = phase
        self.sub_phase = 0
        self.redetermine_order = [None] * len(pray_order)
        
    def waiting_user_input(self):
        return True

    def process_command(self, game_state, command):
        if self.sub_phase == 0 and command['turn_order'][0] == 'to_pray':
            # command example = { 'turn_order': ['to_pray', 0, False] }
            self.redetermine_order[command['turn_order'][1]] = command['turn_order'][2]
            if len(list(filter(lambda x: x is None, self.redetermine_order))) == 0:
                if not len(list(filter(lambda x: x, self.redetermine_order))) > 0:
                    # Redetermine
                    return self.proceed_to_next_phase()
                else:
                    self.sub_phase = 1
                    self.new_pray_order = [None] * len(self.pray_order)
                    self.current_player_pray_order_pos = -1
            return self
        elif self.sub_phase == 1 and command['turn_order'][0] == 'pray':
            current_player = self.pray_order[self.current_player_pray_order_pos]
            # command example = { 'turn_order': ['pray', 0, True] }
            if current_player != command['turn_order'][1]:
                raise Exception('Wrong player')
            if command['turn_order'][2]:
                for i in range(len(self.pray_order)):
                    if self.new_pray_order[i] is None:
                        self.new_pray_order[i] = current_player
                        break
            else: # not command['turn_order'][2]
                for i in range(len(self.pray_order)):
                    if self.new_pray_order[-i-1] is None:
                        self.new_pray_order[-i-1] = current_player
                        break
            if len(list(filter(lambda x: x is None, self.new_pray_order))) == 0:
                self.sub_phase = 2
                self.new_turn_order = [None] * len(self.pray_order)
                self.current_player_pray_order_pos = 0
            else:
                self.current_player_pray_order_pos -= 1
            return self
        elif self.sub_phase == 2 and command['turn_order'][0] == 'order':
            # command example = { 'turn_order': ['order', 1, 0] } // [_, player, pos]
            if self.new_pray_order[self.current_player_pray_order_pos] != command['turn_order'][1]:
                raise Exception('Wrong player')
            self.new_turn_order[command['turn_order'][2]] = command['turn_order'][1]
            self.current_player_pray_order_pos += 1
            if self.current_player_pray_order_pos == len(self.pray_order):
                game_state.pray_order = self.new_pray_order
                game_state.turn_order = self.new_turn_order
                return self.proceed_to_next_phase()
            else:
                return self
        else:
            raise Exception('Wrong command')

    def proceed_to_next_phase(self):
        if self.next_phase == 1:
            return Production()
        elif self.next_phase == 2:
            return Movement()
        elif self.next_phase == 3:
            return Building()
        elif self.next_phase == 4:
            return Wonder()