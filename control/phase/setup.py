from .phase import Phase
from control import game_tokens, game_tile
from .turn_order import TurnOrder
from .production import Production

class Setup(Phase):
    turn_order = None
    current_player = None

    def __init__(self, turn_order):
        self.turn_order = turn_order
        self.current_player = turn_order[0]

    def waiting_user_input(self):
        return True

    # command example = {'setup': [0, [1,3]]} // [player, [x,y]]
    def process_command(self, game_state, command):
        player, coor = command['setup']

        if player != self.current_player:
            raise Exception('Wrong player')

        expect_start_tile = game_state.map.get_tile(coor)

        if expect_start_tile is None:
            raise Exception('Start tile is out of bounds')

        if expect_start_tile.terrain == game_tile.Terrain.WATER:
            raise Exception('Start tile is water')

        if expect_start_tile.home is not None:
            raise Exception('Start tile is already occupied')

        for neighbor in game_state.map.adjacent_coordinates(coor):
            if game_state.map.get_tile(neighbor).home is not None:
                raise Exception('Start tile has neighbor occupied')

        expect_start_tile.player_tokens = [
            [
                game_tokens.PlayerToken.DONKEY, 
                self.current_player, 
                game_state.players[self.current_player].add_new_transport(game_tokens.PlayerToken.DONKEY), 
                {}
            ] for _ in range(3)
        ]
        expect_start_tile.resource_tokens = {
            game_tokens.ResourceToken.BOARDS: 5,
            game_tokens.ResourceToken.STONE: 1,
            game_tokens.ResourceToken.GOOSE: 2,
        }
        expect_start_tile.home = self.current_player

        return self.next_state(game_state)

    def next_state(self, game_state):
        if self.current_player != self.turn_order[-1]:
            self.current_player = self.turn_order[self.turn_order.index(self.current_player) + 1]
            return self
        else:
            return None
        
