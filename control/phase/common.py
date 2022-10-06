from functools import reduce

from control.game_tokens import PlayerTokenCapacity

def load_goods(tile, owner, transporter_name, goods):
    transporter = None
    for tile_transporter in tile.player_tokens:
        if owner == tile_transporter[1] and transporter_name == tile_transporter[2]:
            transporter = tile_transporter
            break
    if transporter is None:
        raise Exception("Transporter not found")

    tile.remove_resources(goods)
    for good_type, good_amount in goods.items():
        if good_type not in transporter[3]:
            transporter[3][good_type] = 0
        transporter[3][good_type] += good_amount
    if reduce(lambda x, y: x + y, transporter[3].values()) > PlayerTokenCapacity[transporter[0]]:
        raise Exception("Transporter capacity exceeded")

def unload_goods(tile, owner, transporter_name, goods) -> dict[int, int]:
    transporter = None
    for tile_transporter in tile.player_tokens:
        if owner == tile_transporter[1] and transporter_name == tile_transporter[2]:
            transporter = tile_transporter
            break
    if transporter is None:
        raise Exception("Transporter not found")
    
    for good_type, good_amount in goods.items():
        if good_type not in transporter[3]:
            raise Exception("Transporter does not have enough goods.")
        if transporter[3][good_type] < good_amount:
            raise Exception("Transporter does not have enough goods.")
        transporter[3][good_type] -= good_amount
        if transporter[3][good_type] == 0:
            del transporter[3][good_type]

    return goods

def load_transporter(tile, owner, transporter_name, loaded_owner, loaded_transporter):
    transporter = None
    for tile_transporter in tile.player_tokens:
        if owner == tile_transporter[1] and transporter_name == tile_transporter[2]:
            transporter = tile_transporter
            break
    if transporter is None:
        raise Exception("Transporter not found")

    for tile_transporter in tile.player_tokens:
        if loaded_owner == tile_transporter[1] and loaded_transporter == tile_transporter[2]:
            transporter[3] = tile_transporter
            tile.player_tokens.remove(tile_transporter)
            return
    raise Exception("Transporter not found")
