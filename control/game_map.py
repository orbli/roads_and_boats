from typing import List

from .game_tile import GameTile

class GameMap:
    map = None

    def __init__(self, width, height):
        self.map = []
        for i in range(height):
            self.map.append([None] * width)

    def assign_tiles(self, assignments):
        for coordinate, tile in assignments.items():
            self.map[coordinate[1]][coordinate[0]] = tile

    def iterate_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] is not None:
                    yield [x, y], self.map[y][x]
        return None

    def get_tile(self, coordinate) -> GameTile:
        return self.map[coordinate[1]][coordinate[0]]

    def adjacent_coordinates(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        if x % 2 == 1:
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
        else: # x % 2 == 0
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
