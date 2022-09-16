from control.game_tokens import BuildingToken, ResourceToken, PlayerToken
from control.game_tile import Terrain
from .phase import Phase
import random

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
    current_player = None
    subphase = None
    tile_activations = {}
    # subphase 3
    donkey_reproduction_pending = None

    def __init__(self):
        self.subphase = 1
    
    def waiting_user_input(self):
        return self.waiting_user_input_var

    def process(self, game_state):
        if self.subphase == 1:
            # 1: primary producer produces one good
            for _, tile in game_state.map.iterate_map():
                if tile.building is not None:
                    if tile.building == BuildingToken.WOODCUTTER:
                        tile.add_resource(ResourceToken.TRUNKS, 1)
                    elif tile.building == BuildingToken.QUARRY:
                        tile.add_resource(ResourceToken.STONE, 1)
                    elif tile.building == BuildingToken.CLAYPIT:
                        tile.add_resource(ResourceToken.CLAY, 1)
                    elif tile.building == BuildingToken.OILRIG:
                        tile.add_resource(ResourceToken.FUEL, 1)
                    elif tile.building == BuildingToken.MINE:
                        if len(game_state.players) == 1:
                            # [gold, iron]
                            rt = [0, 0]
                            for resource in tile.mine_reserve:
                                if resource == ResourceToken.GOLD:
                                    rt[0] += 1
                                elif resource == ResourceToken.IRON:
                                    rt[1] += 1
                            if rt == [0, 0]:
                                continue
                            if rt[0] < rt[1]:
                                tile.add_resource(ResourceToken.IRON, 1)
                                rt[1] -= 1
                            else:
                                tile.add_resource(ResourceToken.GOLD, 1)
                                rt[0] -= 1
                            tile.mine_reserve = [ResourceToken.GOLD] * rt[0] + [ResourceToken.IRON] * rt[1]
                        else:
                            random.shuffle(tile.mine_reserve)
                            resource = tile.mine_reserve.pop()
                            tile.add_resource(resource, 1)
            self.waiting_user_input_var = True
            self.current_player = game_state.turn_order[0]
            self.subphase = 2
        if self.subphase == 3 and self.current_player is None:
            self.donkey_reproduction_pending = [[]] * len(game_state.players)
            for coordinates, tile in game_state.map.iterate_map():
                if tile.terrain == Terrain.PASTURE and tile.building is None:
                    if len(tile.player_tokens) == 2 and \
                        tile.player_tokens[0][0] == PlayerToken.DONKEY and \
                        tile.player_tokens[1][0] == PlayerToken.DONKEY and \
                        tile.player_tokens[0][1] == tile.player_tokens[1][1] and \
                        len(tile.resource_tokens) == 0:
                        self.donkey_reproduction_pending[tile.player_tokens[0][1]].append(coordinates)
                    elif tile.resource_tokens == { ResourceToken.GOOSE: 2 }:
                        tile.resource_tokens[ResourceToken.GOOSE] += 1
            return self.proceed_subphase3(game_state)
        if self.subphase == 4:
            # neutral production
            for coordinates, tile in game_state.map.iterate_map():
                try:
                    while True:
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
                            self.tile_secondary_production(self, coordinates, tile, resources)
                except Exception as e:
                    if e.args[0] == "Tile cannot be activated further" or \
                        e.args[0] == "Not enough resources.":
                        continue
                    else:
                        raise e
            # TODO: remove transporter
            None
        return self

    def proceed_subphase3(self, game_state):
        for player in game_state.turn_order:
            if self.donkey_reproduction_pending[player] is not None:
                self.waiting_user_input_var = True
                self.current_player = player
                return self
        self.waiting_user_input_var = False
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
        # 3: donkey reproduction
        # 4: remove excess transporter
        raise NotImplementedError