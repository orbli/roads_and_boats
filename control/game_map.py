from typing import List

from .game_tile import GameTile

class GameMap:
    map = None
    boundaries = None # { frozenset({(x1,y1),(x2,y2)}): [[wall_player_no, level], has_road(T/F)] })]}

    # @classmethod
    # def from_json(cls, json):

    def export_state(self):
        map = {}
        for coordinate, tile in self.iterate_map():
            x, y = coordinate
            map[f"{x}|{y}"] = tile.export_state()
        boundaries = {}
        for coors, boundary in self.boundaries.items():
            coors_set = set(coors)
            coor1 = coors_set.pop()
            coor2 = coors_set.pop()
            boundaries[f"{coor1[0]}|{coor1[1]},{coor2[0]}|{coor2[1]}"] = boundary
        return {
            'map_size': [len(self.map[0]), len(self.map)],
            'map': map,
            'boundaries': boundaries,
        }

    @classmethod
    def build_from_state(cls, state):
        rt = cls()
        rt.set_map_size(state['map_size'])
        for coordinate, tile_state in state['map'].items():
            x, y = map(int, coordinate.split('|'))
            rt.map[y][x] = GameTile.build_from_state(tile_state)
        for coors, boundary in state['boundaries'].items():
            coors = coors.split(',')
            coor1 = tuple(map(int, coors[0].split('|')))
            coor2 = tuple(map(int, coors[1].split('|')))
            rt.boundaries[frozenset({coor1, coor2})] = boundary
        return rt

    def __init__(self):
        self.boundaries = {}
    
    def set_map_size(self, map_size):
        width, height = map_size
        self.map = [ [None] * width for _ in range(height) ]
            
    @classmethod
    def with_map(cls, map_size, assignments):
        instance = cls()
        instance.set_map_size(map_size)
        instance.assign_tiles(assignments)
        return instance

    def assign_tiles(self, assignments):
        for coordinate, tile in assignments.items():
            self.map[coordinate[1]][coordinate[0]] = tile

    def iterate_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] is not None:
                    yield [x, y], self.map[y][x]
        return None

    def __getitem__(self, key) -> GameTile:
        return self.get_tile(key)

    def get_tile(self, coordinate) -> GameTile:
        x, y = coordinate
        return self.map[y][x]

    def set_tile(self, coordinate, tile_state):
        self.get_tile(coordinate).import_state(tile_state)

    def adjacent_coordinates(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        if y % 2 == 1:
            """
            0) 0  --- (1) --- (2) --- 3
            1)    (0) ---  1  --- (2)
            2) 0  --- (1) --- (2) --- 3
            """
            candidates = [
                [x+1, y],
                [x-1, y],
                [x, y+1],
                [x+1, y+1],
                [x, y-1],
                [x+1, y-1],
            ]
        else: # y % 2 == 0
            """
            0)  0  ---  1  ---  2  ---  3
            1)     (0) --- (1) ---  2
            2) (0) ---  1  --- (2) ---  3
            3)     (0) --- (1) ---  2
            """
            candidates = [
                [x+1, y],
                [x-1, y],
                [x, y+1],
                [x-1, y+1],
                [x, y-1],
                [x-1, y-1],
            ]
        # filter for out of array bound
        rt = filter(lambda c: c[0] >= 0 and c[1] >= 0 and c[0] < len(self.map[0]) and c[1] < len(self.map), candidates)
        # filter for out of map bound
        rt = filter(lambda c: self.map[c[1]][c[0]] is not None, rt)
        return list(rt)

    def adjacent_tiles(self, coordinate) -> List[GameTile]:
        rt = self.adjacent_coordinates(coordinate)
        return list(map(lambda c: self.map[c[1]][c[0]], rt))
