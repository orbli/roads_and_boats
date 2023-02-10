from .phase import Phase
from control.phase.common import load_goods, load_transporter, unload_goods

class Movement(Phase):
    waiting_user_input = None
    current_processing_player_order = None

    def __init__(self):
        self.current_processing_player_order = 0

    def waiting_user_input(self):
        return self.waiting_user_input is not None

    def process(self, game_state):
        if self.waiting_user_input is None:
            self.waiting_user_input = game_state.turn_order[self.current_processing_player_order]
        return self
        
    """
    cmd: {
        'move': [
            0, # player id 0
            [
                ['donkey 0', '3|5', 'unload_transporter'],
                ['donkey 0', '3|5', 'unload', {ResourceToken.STONE: 1}],
                ['donkey 0', '3|5', 'load', {ResourceToken.BOARDS: 2}],
                ['donkey 0', '3|5', 'move', '3|6', {ResourceToken.GOOSE: 3}],
                ['donkey 0', '3|5', 'load_transporter', 'donkey 1', 0], # load donkey 1 of player 0
            ]
        ]
    }
    """
    def process_command(self, game_state, command):
        cache = {}
        player = command['move'][0]
        if player != self.waiting_user_input:
            raise Exception('Wrong player')
        for command_entry in enumerate(command['move'][1]):
            cmd = command_entry[1]
            if cmd[1] not in cache:
                cache[cmd[1]] = game_state.map[cmd[1]].export_state()
            tile = game_state.map[cmd[1]]
            token = None
            for t in game_state.map[cmd[1]].player_tokens:
                if t[1] == player and t[2] == cmd[0]:
                    token = t[0]
                    break
            if token is None:
                raise Exception('Token not found')
            
            
            # manage commands
            if cmd[2] == 'unload_transporter':
                if command_entry[0] != 0:
                    raise Exception('Unload transporter must be the first command')
                if not isinstance(token[3], list):
                    raise Exception('is not carrying transporter')
                new_transporter = token[3]
                token[3] = {}
                game_state.map[cmd[1]].player_tokens.append(new_transporter)
            elif cmd[2] == 'unload':
                unloaded_goods = unload_goods(tile, player, cmd[0], cmd[3])
                tile.add_resources(unloaded_goods)
            elif cmd[2] == 'load':
                load_goods(tile, player, cmd[0], cmd[3])
            elif cmd[2] == 'load_transporter':
                load_transporter(tile, player, cmd[0], cmd[3], cmd[4])
            elif cmd[2] == 'move':
                # TODO: many thing to do
                pass



    def export_state(self):
        raise NotImplementedError()