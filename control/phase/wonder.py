from control.phase.common import load_goods, load_transporter, unload_goods
from .phase import Phase
from functools import reduce
import copy

class Wonder(Phase):
    waiting_user_input = None
    current_processing_player_order = None

    def __init__(self):
        self.current_processing_player_order = 0

    def waiting_user_input(self):
        return self.waiting_user_input

    def process(self, game_state):
        while self.current_processing_player_order < len(game_state.turn_order):
            player_id = game_state.turn_order[self.current_processing_player_order]
            player = game_state.players[player_id]
            has_transporter = False
            for player_token in game_state.map[player.home].player_tokens:
                if player_token[1] == player_id:
                    has_transporter = True
                    break
            if has_transporter:
                self.waiting_user_input = player_id
                return self
            self.current_processing_player_order += 1
        game_state.wonder.append(-1)
        return None

    """
    cmd: {
        'wonder': [0, [
            ['load', ['donkey 1', {ResourceToken.BOARDS, 2}]],
            ['unload', ['donkey 1', {ResourceToken.TRUNK: 1}]],
            ['load_transporter', ['donkey 2', 'donkey 3', 0]], # donkey 3 of player 0 on the donkey 2
            ['wonder', {ResourceToken.BOARDS: 9}]
        ]]
    }
    """
    def process_command(self, game_state, cmd):
        player_id, cmds = cmd['wonder']
        if player_id != self.waiting_user_input:
            raise Exception('Wrong player')
        tile_coor = game_state.players[player_id].home
        tile = game_state.map[tile_coor]
        tile_state = tile.export_state()
        wonder_state = copy.deepcopy(game_state.wonder)
        try:
            for cmd in cmds:
                if cmd[0] == 'load':
                    transporter_name, goods = cmd[1]
                    load_goods(tile, player_id, transporter_name, goods)
                elif cmd[0] == 'unload':
                    transporter_name, goods = cmd[1]
                    unloaded_goods = unload_goods(tile, player_id, transporter_name, goods)
                    tile.add_resources(unloaded_goods)
                elif cmd[0] == 'load_transporter':
                    transporter_name, transporter_name2, player2 = cmd[1]
                    if player_id != player2:
                        raise NotImplementedError("TODO: Cannot load transporter of other player")
                    load_transporter(tile, player_id, transporter_name, player2, transporter_name2)
                elif cmd[0] == 'wonder':
                    tile.remove_resources(cmd[1])
                    total_amount = reduce(lambda x,y: x+y, cmd[1].values())
                    resource_req = 1
                    while not total_amount <= 0:
                        game_state.wonder.append(player_id)
                        total_amount -= resource_req + 1 if len(game_state.wonder) >= 18 else 0
                        resource_req += 1
                    if total_amount < 0:
                        raise Exception('Incorrect number of resources for wonder')
        except Exception as e:
            game_state.map[tile_coor].import_state(tile_state)
            game_state.wonder = wonder_state
            raise e
        self.current_processing_player_order += 1
        