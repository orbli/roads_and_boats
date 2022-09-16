import pytest
from .game_map import GameMap
from .game_tile import GameTile, Terrain

@pytest.fixture
def game_map_config():
    map_size = (5, 3)
    map_assignment = {
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
    return map_size, map_assignment

def test_create_map(game_map_config):
    map_size, map_assignment = game_map_config
    game_map = GameMap(map_size[0], map_size[1])
    game_map.assign_tiles(map_assignment)

@pytest.fixture
def game_map(game_map_config):
    map_size, map_assignment = game_map_config
    game_map = GameMap(map_size[0], map_size[1])
    game_map.assign_tiles(map_assignment)
    return game_map