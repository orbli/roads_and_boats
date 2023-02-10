from control.game_player import Research
from control.game_tile import Terrain
from control.game_tokens import BuildingToken, PlayerToken, ResourceToken
from control.phase.common import load_goods, load_transporter, unload_goods
from .phase import Phase

building_resource = {
    BuildingToken.WOODCUTTER: { ResourceToken.BOARDS: 1 },
    BuildingToken.QUARRY: { ResourceToken.BOARDS: 2 },
    BuildingToken.CLAYPIT: { ResourceToken.BOARDS: 3 },
    BuildingToken.OILRIG: { ResourceToken.BOARDS: 2, ResourceToken.STONE: 1 },
    BuildingToken.MINE: { ResourceToken.BOARDS: 2, ResourceToken.STONE: 1 },
    BuildingToken.SAWMILL: { ResourceToken.BOARDS: 2, ResourceToken.STONE: 1 },
    BuildingToken.COALBURNER: { ResourceToken.BOARDS: 3},
    BuildingToken.PAPERMILL: { ResourceToken.BOARDS: 1, ResourceToken.STONE: 1 },
    BuildingToken.STONEFACTORY: { ResourceToken.BOARDS: 2},
    BuildingToken.MINT: { ResourceToken.BOARDS: 2, ResourceToken.STONE: 1 },
    BuildingToken.STOCKEXCHANGE: { ResourceToken.STONE: 3 },
    BuildingToken.WAGONFACTORY: { ResourceToken.BOARDS: 2, ResourceToken.STONE: 1 },
    BuildingToken.TRUCKFACTORY: { ResourceToken.BOARDS: 1, ResourceToken.STONE: 2 },
    BuildingToken.RAFTFACTORY: { ResourceToken.BOARDS: 1, ResourceToken.STONE: 1 },
    BuildingToken.ROWBOATFACTORY: { ResourceToken.BOARDS: 2, ResourceToken.STONE: 1 },
    BuildingToken.STEAMERFACTORY: { ResourceToken.BOARDS: 1, ResourceToken.STONE: 2 },
}


def if_player_on_tile(tile, player_id):
    for player_token in tile.player_tokens:
        if player_token[1] == player_id:
            return True
    return False
def if_tile_is_shore(tile_coor, game_map):
    coors = game_map.adjacent_coordinates(tile_coor)
    for coor in coors:
        if game_map[coor].terrain == Terrain.WATER:
            return True
    return False
def fill_shaft(tile, research, shaft_type):
    if shaft_type == 0:
        tile.mine_reserve = [ ResourceToken.IRON ] * 3 + [ ResourceToken.GOLD ] * 3
    elif shaft_type == 1:
        if not Research.SPECIALIZE_MINE in research:
            raise Exception('Cannot build specialized mine without research')
        tile.mine_reserve = [ ResourceToken.GOLD ] * 4
    elif shaft_type == 2:
        if not Research.SPECIALIZE_MINE in research:
            raise Exception('Cannot build specialized mine without research')
        tile.mine_reserve = [ ResourceToken.IRON ] * 4
    elif shaft_type == 3:
        if not Research.BIG_MINE in research:
            raise Exception('Cannot build big mine without research')
        tile.mine_reserve = [ ResourceToken.IRON ] * 5 + [ ResourceToken.GOLD ] * 5

class Building(Phase):
    waiting_user_input = None
    
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
        'building': [0, {
            '0|0': [
                ['load', ['donkey 1', {ResourceToken.BOARDS, 2}]],
                ['unload', ['donkey 1', {ResourceToken.TRUNK: 1}]],
                ['load_transporter', ['donkey 2', 'donkey 3', 0]], # donkey 3 of player 0 on the donkey 2
                ['build_building', BuildingToken.WOODCUTTER],
                ['build_road', [0,1]],
                ['mine_shaft', 0],
                ['build_wall', [0,1]],
                ['strengthen_wall', [0,1]],
                ['demolist_wall', [0,1]],
            ]
        }]
    }
    """
    def process_command(self, game_state, cmd):
        player_id, cmds = cmd['building']
        if player_id != self.waiting_user_input:
            raise Exception('Wrong player')
        tile_state = {}
        try:
            for tile_coor, cmds in cmds.items():
                tile = game_state.map[tile_coor]
                if tile_coor not in tile_state:
                    tile_state[tile_coor] = tile.export_state()
                if not if_player_on_tile(tile, player_id):
                    raise Exception('Player not on tile')
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
                    elif cmd[0] == 'build_building':
                        if tile.building is not None:
                            raise Exception('Tile already have building')
                        building = cmd[1]
                        if tile.terrain == Terrain.WATER and building not in [BuildingToken.OILRIG]:
                            raise Exception('Cannot build building on water')
                        if tile.terrain == Terrain.DESERT and not game_state.desert_as_pasture():
                            raise Exception('Cannot build building on desert')
                        if building == BuildingToken.WOODCUTTER:
                            if tile.terrain != Terrain.WOOD:
                                raise Exception('Cannot build woodcutter on non-forest terrain')
                        elif building == BuildingToken.QUARRY:
                            if tile.terrain != Terrain.ROCK:
                                raise Exception('Cannot build quarry on non-stone terrain')
                        elif building == BuildingToken.CLAYPIT:
                            if not if_tile_is_shore(tile_coor, game_state.map):
                                raise Exception('Cannot build claypit on non-shore terrain')
                        elif building == BuildingToken.OILRIG:
                            if tile.terrain != Terrain.WATER:
                                raise Exception('Cannot build oilrig on non-water terrain')
                            # if player does not have oilrig research
                            if not Research.OILRIG in game_state.player[player_id].researches:
                                raise Exception('Cannot build oilrig without research')
                        elif building == BuildingToken.MINE:
                            if tile.terrain != Terrain.MOUNTAIN:
                                raise Exception('Cannot build mine on non-mountain terrain')
                            if len(cmd) > 2:
                                shaft_type = cmd[2]
                            else:
                                shaft_type = 0
                            fill_shaft(tile, game_state.player[player_id].researches, shaft_type)
                        elif building == BuildingToken.TRUCKFACTORY:
                            if not Research.TRUCK in game_state.player[player_id].researches:
                                raise Exception('Cannot build truck factory without research')
                        elif building == BuildingToken.RAFTFACTORY:
                            if not if_tile_is_shore(tile_coor, game_state.map):
                                raise Exception('Cannot build raft factory on non-shore terrain')
                        elif building == BuildingToken.ROWBOATFACTORY:
                            if not if_tile_is_shore(tile_coor, game_state.map):
                                raise Exception('Cannot build rowboat factory on non-shore terrain')
                            if not Research.ROWBOAT in game_state.player[player_id].researches:
                                raise Exception('Cannot build rowboat factory without research')
                        elif building == BuildingToken.STEAMERFACTORY:
                            if not if_tile_is_shore(tile_coor, game_state.map):
                                raise Exception('Cannot build rowboat factory on non-shore terrain')
                            if not Research.STEAMER in game_state.player[player_id].researches:
                                raise Exception('Cannot build steamer factory without research')
                        tile.remove_resources(building_resource[building])
                        tile.building = building
                    elif cmd[0] == 'build_road':
                        target = cmd[1]
                        if target not in game_state.map.adjacent_coordinates(tile_coor):
                            raise Exception('Target tile is not adjacent')
                        if tile.terrain == Terrain.WATER or game_state.map[target].terrain == Terrain.WATER:
                            raise Exception('Cannot build road on water')    
                        boundary = frozenset({tuple(target), tuple(tile_coor)})
                        if boundary not in game_state.map.boundaries:
                            game_state.map.boundaries[boundary] = [[-1, 0], False]
                        if game_state.map.boundaries[boundary][1]:
                            raise Exception('Road already exist')
                        tile.remove_resource(ResourceToken.STONE, 1)
                        game_state.map.boundaries[boundary][1] = True
                    elif cmd[0] == 'build_shaft':
                        shaft_type = cmd[1]
                        if tile.building != BuildingToken.MINE:
                            raise Exception('Cannot build shaft on non-mine building')
                        if not Research.REFILL_MINE in game_state.player[player_id].researches:
                            raise Exception('Cannot build shaft without research')
                        fill_shaft(tile, game_state.player[player_id].researches, shaft_type)
                    elif cmd[0] == 'build_wall':
                        target = cmd[1]
                        if target not in game_state.map.adjacent_coordinates(tile_coor):
                            raise Exception('Target tile is not adjacent')
                        if tile.terrain == Terrain.WATER and game_state.map[target].terrain == Terrain.WATER:
                            raise Exception('Cannot build wall on water')
                        boundary = frozenset({tuple(target), tuple(tile_coor)})
                        if boundary not in game_state.map.boundaries:
                            game_state.map.boundaries[boundary] = [[-1, 0], False]
                        if game_state.map.boundaries[boundary][0][0] != -1:
                            raise Exception('Wall already owned')
                        cost = 1 + game_state.map.boundaries[boundary][0][1]
                        if tile.terrain == Terrain.WATER:
                            cost += 2
                        tile.remove_resource(ResourceToken.STONE, cost)
                        game_state.map.boundaries[boundary][0][0] = player_id
                        game_state.map.boundaries[boundary][0][1] += 1
                        land_tile, water_tile = None, None
                        if tile.terrain == Terrain.WATER:
                            land_tile = game_state.map[target]
                            water_tile = tile
                        elif game_state.map[target].terrain == Terrain.WATER:
                            land_tile = tile
                            water_tile = game_state.map[target]
                        if water_tile is not None:
                            is_water_transport = lambda x: x >= PlayerToken.RAFT
                            for transport in land_tile.player_tokens:
                                if is_water_transport(transport[0]):
                                    if transport[1] != player_id:
                                        land_tile.player_tokens.remove(transport)
                                        water_tile.player_tokens.append(transport)
                    elif cmd[0] == 'demolish_wall':
                        target = cmd[1]
                        if target not in game_state.map.adjacent_coordinates(tile_coor):
                            raise Exception('Target tile is not adjacent')
                        boundary = frozenset({tuple(target), tuple(tile_coor)})
                        if boundary not in game_state.map.boundaries:
                            raise Exception('Cannot demolish non-exist wall')
                        if game_state.map.boundaries[boundary][0][0] == -1:
                            raise Exception('Cannot demolish wall not owned')
                        if game_state.map.boundaries[boundary][0][1] == 0:
                            raise Exception('Cannot demolish wall with no level')
                        cost = 1 + game_state.map.boundaries[boundary][0][1]
                        if tile.terrain == Terrain.WATER:
                            cost += 2
                        tile.remove_resource(ResourceToken.BOARD, cost)
                        game_state.map.boundaries[boundary][0][0] = -1
        except Exception as e:
            for tile_coor, state in tile_state.items():
                game_state.map[tile_coor].import_state(state)
            raise Exception('Invalid command')
