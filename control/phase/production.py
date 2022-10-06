import copy

from pyrsistent import discard
from control.game_player import Research
from control.game_tokens import BuildingToken, ResourceToken, PlayerToken
from control.game_tile import Terrain
from control.phase.common import load_goods, load_transporter, unload_goods
from .phase import Phase
import random
from collections import defaultdict

def mine_production(reserve, players):
    if len(reserve) == 0:
        return None, []
    if len(players) == 1:
        # [gold, iron]
        reserve_array = [0, 0]
        for resource in reserve:
            if resource == ResourceToken.GOLD:
                reserve_array[0] += 1
            elif resource == ResourceToken.IRON:
                reserve_array[1] += 1
        if reserve_array == [0, 0]:
            return None
        if reserve_array[0] < reserve_array[1]:
            rt = ResourceToken.IRON
            reserve_array[1] -= 1
        else:
            rt = ResourceToken.GOLD
            reserve_array[0] -= 1
        reserve = [ResourceToken.GOLD] * rt[0] + [ResourceToken.IRON] * rt[1]
    else:
        random.shuffle(reserve)
        rt = reserve.pop()
    return rt, reserve

primay_production_config = {
    BuildingToken.WOODCUTTER: ResourceToken.TRUNKS,
    BuildingToken.QUARRY: ResourceToken.STONE,
    BuildingToken.CLAYPIT: ResourceToken.CLAY,
    BuildingToken.OILRIG: ResourceToken.FUEL,
    BuildingToken.MINE: mine_production,
}

secondary_production_config = {
    BuildingToken.SAWMILL: [
        [ { ResourceToken.TRUNKS: 1 } ],
        { ResourceToken.BOARDS: 2 },
        6
    ],
    BuildingToken.STONEFACTORY: [
        [ { ResourceToken.CLAY: 1 } ],
        { ResourceToken.STONE: 2 },
        6
    ],
    BuildingToken.COALBURNER: [
        [ { ResourceToken.BOARDS: 2 }, { ResourceToken.TRUNKS: 1, ResourceToken.BOARDS: 1 }, { ResourceToken.TRUNKS: 2 } ],
        { ResourceToken.FUEL: 1 },
        6
    ],
    BuildingToken.PAPERMILL: [
        [ { ResourceToken.BOARDS: 2 }, { ResourceToken.TRUNKS: 1, ResourceToken.BOARDS: 1 }, { ResourceToken.TRUNKS: 2 } ],
        { ResourceToken.PAPER: 1 },
        1
    ],
    BuildingToken.MINT: [
        [ { ResourceToken.FUEL: 1, ResourceToken.GOLD: 2 } ],
        { ResourceToken.COINS: 1 },
        1
    ],
    BuildingToken.STOCKEXCHANGE: [
        [ { ResourceToken.COINS: 2, ResourceToken.PAPER: 1 } ],
        { ResourceToken.STOCK: 1 },
        6
    ]
}

class Production(Phase):
    waiting_user_input_var = False
    current_player_turn_order_index = None
    subphase = None
    tile_activations = None
    # subphase 2
    reverse_action_stack = []
    # subphase 3
    donkey_reproduction_pending = None

    def __init__(self):
        self.subphase = 1
        self.tile_activations = defaultdict(lambda: 0)
    
    def waiting_user_input(self):
        return self.waiting_user_input_var

    def process(self, game_state):
        if self.subphase == 1:
            # 1: primary producer produces one good
            for _, tile in game_state.map.iterate_map():
                if tile.building is not None:
                    if tile.building in primay_production_config:
                        if tile.building == BuildingToken.MINE:
                            rt, tile.mine_reserve = primay_production_config[tile.building](tile.mine_reserve, len(game_state.players))
                        else:
                            rt = primay_production_config[tile.building]
                        if rt is not None:
                            tile.add_resources(rt, 1)
            self.waiting_user_input_var = True
            self.current_player_turn_order_index = 0
            self.subphase = 3
        if self.subphase == 4 and self.current_player is None:
            self.donkey_reproduction_pending = [[]] * len(game_state.players)
            for coordinates, tile in game_state.map.iterate_map():
                if (tile.terrain == Terrain.PASTURE or (tile.terrain == Terrain.DESERT and game_state.monument.desert_as_pasture())) \
                    and tile.building is None:
                    if len(tile.player_tokens) == 2 and \
                        tile.player_tokens[0][0] == PlayerToken.DONKEY and \
                        tile.player_tokens[1][0] == PlayerToken.DONKEY and \
                        tile.player_tokens[0][1] == tile.player_tokens[1][1] and \
                        len(tile.resource_tokens) == 0:
                        self.donkey_reproduction_pending[tile.player_tokens[0][1]].append(coordinates)
                    elif tile.resource_tokens == { ResourceToken.GOOSE: 2 }:
                        tile.resource_tokens[ResourceToken.GOOSE] += 1
            return self.proceed_subphase4(game_state)
        if self.subphase == 5:
            # neutral secondary production
            for coordinates, tile in game_state.map.iterate_map():
                try:
                    while True:
                        resources = None
                        if tile.building == BuildingToken.COALBURNER or tile.building == BuildingToken.PAPERMILL:
                            for select_resource in secondary_production_config[tile.building][0]:
                                if tile.have_resources(select_resource):
                                    resources = select_resource
                                    break
                        else:
                            if tile.building in secondary_production_config:
                                selecting_resource = secondary_production_config[tile.building][0][0]
                                if tile.have_resources(selecting_resource):
                                    resources = selecting_resource
                        if resources:
                            self.tile_secondary_production(coordinates, tile, resources)
                        else:
                            break
                except Exception as e:
                    if e.args[0] == "Tile cannot be activated further" or \
                        e.args[0] == "Not enough resources.":
                        None
                    else:
                        raise e
                while tile.have_resources({ ResourceToken.GOOSE: 2, ResourceToken.PAPER: 1 }):
                    tile.remove_resources({ ResourceToken.GOOSE: 2, ResourceToken.PAPER: 1 })
            return None
        return self

    def proceed_subphase4(self, game_state):
        for player in game_state.turn_order:
            if self.donkey_reproduction_pending[player] is not None:
                self.waiting_user_input_var = True
                self.current_player = player
                return self
        self.waiting_user_input_var = False
        self.subphase = 5
        return self
                
    def tile_secondary_production(self, coordinate, tile, resources):
        if tile.building is not None:
            if tile.building in secondary_production_config:
                config = secondary_production_config[tile.building]
                if self.tile_activations[coordinate] >= config[2]:
                    raise Exception("Tile cannot be activated further")
                if resources in config[0]:
                    tile.remove_resources(resources)
                    tile.add_resources(config[1])
                    self.tile_activations[coordinate] += 1

    # TODO: need a command data structure template
    def process_command(self, game_state, command):
        # 2: player actions in production phase
        """
        {'production': [0, 'player_actions', {
            'actions': {
               '1|7': [
                    ['unload', ['donkey 1', {ResourceToken.TRUNK: 1}]],
                    ['activate', {ResourceToken.TRUNK: 2}],  # arg is {} for neutral secondary productions
                    ['load', ['donkey 1', {ResourceToken.BOARDS, 2}]],
                    ['load_transporter', ['donkey 2', 'donkey 3', 0]], # donkey 3 of player 0 on the donkey 2
                    ['research', [Research.ROWBOAT]], # upgrade transporter factory
                ],
                '2|5': [
                    ['unload', ResourceToken.BOARDS, 1, 'donkey 4'],
                    ['activate', ['wagon 1']], # produce transporter, remove wagon 1 if cap
                ],
                '3|6': [
                    ['activate', [None, [0,1]]] # [dont discard transporter, water transporter at direction[0,1] coast]
                ]
            },
            'upgrades': ['5|8'],
        }]}
        """
        if self.subphase == 3:
            player, phase_name, data = command['production']
            if player != game_state.turn_order[self.current_player_turn_order_index]:
                raise Exception("Not your turn.")
            if phase_name != 'player_actions':
                raise Exception("Wrong subphase")
            tile_snapshot = {}
            tile_activation_snapshot = copy.deepcopy(self.tile_activations)
            player_snapshot = copy.deepcopy(game_state.players[player])
            try:
                researches = set()
                for tile_coor_str, tile_cmds in data['actions'].items():
                    tile_coor = tuple(map(int, tile_coor_str.split('|')))
                    tile = game_state.map.get_tile(tile_coor)
                    tile_snapshot[tile_coor] = tile.export_state()
                    for tile_cmd in tile_cmds:
                        cmd, arg = tile_cmd
                        if cmd == 'unload':
                            transporter_name, goods = arg
                            load_goods(tile, player, transporter_name, goods)
                        elif cmd == 'load':
                            transporter_name, goods = arg
                            unloaded_goods = unload_goods(tile, player, transporter_name, goods)
                            tile.add_resources(unloaded_goods)
                        elif cmd == 'load_transporter':
                            transporter_name, transporter_name2, player2 = arg
                            if player != player2:
                                raise NotImplementedError("TODO: Cannot load transporter of other player")
                            load_transporter(tile, player, transporter_name, player2, transporter_name2)
                        elif cmd == 'research':
                            for research in arg:
                                tile.remove_resources({ ResourceToken.PAPER: 1, ResourceToken.GOOSE: 2 })
                                researches.add(research)
                        elif cmd == 'activate':
                            if tile.building in secondary_production_config:
                                if arg not in secondary_production_config[tile.building][0]:
                                    raise Exception("Wrong resource")
                                self.tile_secondary_production(tile_coor, tile, arg[0])
                            elif tile.building == BuildingToken.WAGONFACTORY:
                                if self.tile_activations[tile_coor] >= 1:
                                    raise Exception("Tile cannot be activated further")
                                found = False
                                for player_token in tile.player_tokens:
                                    transport_type, transport_owner, _, transport_goods, _ = player_token
                                    if transport_type == PlayerToken.DONKEY and transport_owner == player and transport_goods == {}:
                                        tile.player_tokens.remove(player_token)
                                        tile.player_tokens.append([
                                            PlayerToken.WAGON, 
                                            player, 
                                            game_state.players[player].add_new_transport(PlayerToken.WAGON),
                                            {},
                                            {},
                                        ])
                                        self.tile_activations[tile_coor] += 1
                                        found = True
                                        break
                                if not found:
                                    raise Exception("No donkey to upgrade")
                            elif tile.building == BuildingToken.TRUCKFACTORY:
                                if self.tile_activations[tile_coor] >= 1:
                                    raise Exception("Tile cannot be activated further")
                                if len(arg) != 0:
                                    found = False
                                    for player_token in tile.player_tokens:
                                        transport_type, transport_owner, transport_name, transport_goods, _ = player_token
                                        if transport_owner == player and transport_name == arg[0] and transport_goods == {}:
                                            game_state.players[player].remove_transport(transport_type)
                                            tile.player_tokens.remove(player_token)
                                            found = True
                                            break
                                    if not found:
                                        raise Exception("No existing transporter to discard")
                                self.tile_activations[tile_coor] += 1
                                tile.player_tokens.append([
                                    PlayerToken.TRUCK, 
                                    player, 
                                    game_state.players[player].add_new_transport(PlayerToken.TRUCK),
                                    {},
                                ])
                            else: # produce water transports
                                water_transporter_config = [
                                    (BuildingToken.RAFTFACTORY, PlayerToken.RAFT),
                                    (BuildingToken.ROWBOATFACTORY, PlayerToken.ROWBOAT),
                                    (BuildingToken.STEAMERFACTORY, PlayerToken.STEAMSHIP),
                                ]
                                for building, new_transport_type in water_transporter_config:
                                    if tile.building == building:
                                        if self.tile_activations[tile_coor] >= 1:
                                            raise Exception("Tile cannot be activated further")
                                        discard_transporter, direction = arg
                                        if discard_transporter is not None:
                                            found = False
                                            for player_token in tile.player_tokens:
                                                transport_type, transport_owner, transport_name, transport_goods, _ = player_token
                                                if transport_owner == player and transport_name == arg[0] and transport_goods == {}:
                                                    game_state.players[player].remove_transport(transport_type)
                                                    tile.player_tokens.remove(player_token)
                                                    found = True
                                                    break
                                            if not found:
                                                raise Exception("No existing transporter to discard")
                                        next_tile_coor = tile_coor[0] + direction[0], tile_coor[1] + direction[1]
                                        if game_state.map.get_tile(next_tile_coor).terrain != Terrain.WATER:
                                            raise Exception("Not coast direction")
                                        self.tile_activations[tile_coor] += 1
                                        tile.player_tokens.append([
                                            new_transport_type, 
                                            player, 
                                            game_state.players[player].add_new_transport(new_transport_type),
                                            {},
                                            {'direction': direction},
                                        ])
                
                if researches:
                    if 'upgrades' in command:
                        land_upgrade = None
                        sea_upgrade = None
                        if Research.TRUCK in researches:
                            land_upgrade = Research.TRUCK
                        if Research.ROWBOAT in researches:
                            sea_upgrade = Research.ROWBOAT
                        if Research.STEAMSHIP in researches:
                            sea_upgrade = Research.STEAMSHIP
                        for tile_coor_str in command['upgrades']:
                            tile_coor = tuple(map(int, tile_coor_str.split('|')))
                            tile = game_state.map.get_tile(tile_coor)
                            tile_snapshot[tile_coor] = tile.export_state()
                            found = False
                            for player_token in tile.player_tokens:
                                if player_token[1] == player:
                                    found = True
                                    break
                            if not found:
                                raise Exception("No active player token on tile")
                            if tile.building == BuildingToken.WAGONFACTORY:
                                if land_upgrade is None:
                                    raise Exception("No land upgrade researched")
                                tile.building = land_upgrade
                            if tile.building >= 13: # 13=raft 14=rowboat 15=steamer 
                                if sea_upgrade is None:
                                    raise Exception("No sea upgrade researched")
                                tile.building = sea_upgrade
                            
                    game_state.players[player].researches.update(researches)
            except Exception as e:
                for coor, tile in tile_snapshot.items():
                    game_state.map.set_tile(coor, tile)
                self.tile_activation = tile_activation_snapshot
                game_state.players[player] = player_snapshot
                raise e
            self.current_player_turn_order_index += 1
            if self.current_player_turn_order_index == len(game_state.players):
                self.subphase = 4
                self.waiting_user_input_var = False
            return self
        # 3: donkey reproduction
        # yes: {'production': [0, 'donkey_repro', [[1,3]] ]} // [player, 'donkey_repro', [[x,y]] ] // max only 1 pair of donkey reproduces
        # no:  {'production': [0, 'donkey_repro', [[1,3]] ]} // [player, 'donkey_repro', [] ]
        if self.subphase ==  4:
            player, subphase, donkey_reproduction = command['production']
            if player != game_state.turn_order[self.current_player_turn_order_index]:
                raise Exception("Not your turn.")
            if subphase != 'donkey_repro':
                raise Exception("Invalid subphase.")
            if donkey_reproduction == []:
                self.donkey_reproduction_pending[self.current_player] = None
                return self.proceed_subphase4(game_state)
            if len(donkey_reproduction) > 1:
                raise Exception("Too many donkey pairs.")
            if len(donkey_reproduction[0]) != 2:
                raise Exception("Invalid coordinate format.")
            if donkey_reproduction[0] not in self.donkey_reproduction_pending[self.current_player]:
                raise Exception("Wrong coordinate.")
            tile = game_state.map[donkey_reproduction[0]]
            self.donkey_reproduction_pending[self.current_player] = None
            game_state.map[donkey_reproduction[0]].add_player_token(PlayerToken.DONKEY, self.current_player)
            return self.proceed_subphase4(game_state)
        raise NotImplementedError