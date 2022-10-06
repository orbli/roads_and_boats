
class PlayerToken:
    DONKEY = 0
    WAGON = 1
    TRUCK = 2
    RAFT = 3
    ROWBOAT = 4
    STEAMSHIP = 5

PlayerTokenCapacity = {
    PlayerToken.DONKEY: 2,
    PlayerToken.WAGON: 3,
    PlayerToken.TRUCK: 6,
    PlayerToken.RAFT: 3,
    PlayerToken.ROWBOAT: 5,
    PlayerToken.STEAMSHIP: 8,
}

class ResourceToken:
    TRUNKS = 0
    BOARDS = 1
    PAPER = 2
    GOOSE = 3
    CLAY = 4
    STONE = 5
    FUEL = 6
    IRON = 7
    GOLD = 8
    COINS = 9
    STOCK = 10

class BuildingToken:
    # primary production
    WOODCUTTER = 0
    QUARRY = 5
    CLAYPIT = 3
    OILRIG = 6
    MINE = 8
    # secondary production
    SAWMILL = 1
    PAPERMILL = 2
    STONEFACTORY = 4
    COALBURNER = 7
    MINT = 9
    STOCKEXCHANGE = 10
    WAGONFACTORY = 11
    TRUCKFACTORY = 12
    RAFTFACTORY = 13
    ROWBOATFACTORY = 14
    STEAMERFACTORY = 15
