from .game_map import GameMap
from .game_tile import GameTile, Terrain

class DefaultMap:
    ARiverRunsThroughItNoRiver = lambda : GameMap.with_map(
        (5, 3),
        {
            (0,0): GameTile(Terrain.MOUNTAIN),
            (1,0): GameTile(Terrain.WOOD),
            (2,0): GameTile(Terrain.ROCK),
            (3,0): GameTile(Terrain.MOUNTAIN),
            (1,1): GameTile(Terrain.DESERT),
            (2,1): GameTile(Terrain.WOOD),
            (3,1): GameTile(Terrain.PASTURE),
            (4,1): GameTile(Terrain.WATER),
            (1,2): GameTile(Terrain.DESERT),
            (2,2): GameTile(Terrain.PASTURE),
            (3,2): GameTile(Terrain.WATER),
        }
    )
    FourSailors = lambda : GameMap.with_map(
        (8, 9),
        {
            (1,0): GameTile(Terrain.WOOD),
            (2,0): GameTile(Terrain.WOOD),
            (3,0): GameTile(Terrain.WATER),
            (4,0): GameTile(Terrain.ROCK),
            (5,0): GameTile(Terrain.WATER),
            (6,0): GameTile(Terrain.WOOD),
            (7,0): GameTile(Terrain.WOOD),

            (1,1): GameTile(Terrain.WOOD),
            (2,1): GameTile(Terrain.ROCK),
            (3,1): GameTile(Terrain.WATER),
            (4,1): GameTile(Terrain.WATER),
            (5,1): GameTile(Terrain.ROCK),
            (6,1): GameTile(Terrain.WOOD),

            (1,2): GameTile(Terrain.DESERT),
            (2,2): GameTile(Terrain.PASTURE),
            (3,2): GameTile(Terrain.WATER),
            (4,2): GameTile(Terrain.MOUNTAIN),
            (5,2): GameTile(Terrain.WATER),
            (6,2): GameTile(Terrain.PASTURE),
            (7,2): GameTile(Terrain.DESERT),

            (0,3): GameTile(Terrain.PASTURE),
            (1,3): GameTile(Terrain.DESERT),
            (2,3): GameTile(Terrain.WATER),
            (3,3): GameTile(Terrain.MOUNTAIN),
            (4,3): GameTile(Terrain.MOUNTAIN),
            (5,3): GameTile(Terrain.WATER),
            (6,3): GameTile(Terrain.DESERT),
            (7,3): GameTile(Terrain.PASTURE),

            (0,4): GameTile(Terrain.ROCK),
            (1,4): GameTile(Terrain.MOUNTAIN),
            (2,4): GameTile(Terrain.WATER),
            (3,4): GameTile(Terrain.WATER),
            (4,4): GameTile(Terrain.WATER),
            (5,4): GameTile(Terrain.MOUNTAIN),
            (6,4): GameTile(Terrain.ROCK),

            (0,5): GameTile(Terrain.PASTURE),
            (1,5): GameTile(Terrain.DESERT),
            (2,5): GameTile(Terrain.WATER),
            (3,5): GameTile(Terrain.MOUNTAIN),
            (4,5): GameTile(Terrain.MOUNTAIN),
            (5,5): GameTile(Terrain.WATER),
            (6,5): GameTile(Terrain.DESERT),
            (7,5): GameTile(Terrain.PASTURE),

            (1,6): GameTile(Terrain.DESERT),
            (2,6): GameTile(Terrain.PASTURE),
            (3,6): GameTile(Terrain.WATER),
            (4,6): GameTile(Terrain.MOUNTAIN),
            (5,6): GameTile(Terrain.WATER),
            (6,6): GameTile(Terrain.PASTURE),
            (7,6): GameTile(Terrain.DESERT),

            (1,7): GameTile(Terrain.WOOD),
            (2,7): GameTile(Terrain.ROCK),
            (3,7): GameTile(Terrain.WATER),
            (4,7): GameTile(Terrain.WATER),
            (5,7): GameTile(Terrain.ROCK),
            (6,7): GameTile(Terrain.WOOD),

            (1,8): GameTile(Terrain.WOOD),
            (2,8): GameTile(Terrain.WOOD),
            (3,8): GameTile(Terrain.WATER),
            (4,8): GameTile(Terrain.ROCK),
            (5,8): GameTile(Terrain.WATER),
            (6,8): GameTile(Terrain.WOOD),
            (7,8): GameTile(Terrain.WOOD),
        }
    )