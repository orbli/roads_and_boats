
from .game_tokens import PlayerToken

TOTAL_TRANSPORT_COUNT = 8
TOTAL_LAND_TRANSPORT_COUNT = 5
TOTAL_WATER_TRANSPORT_COUNT = 5

class Research:
    ROWBOAT = 0
    TRUCK = 1
    STEAMSHIP = 2
    OILRIGS = 3
    SPECIALIZE_MINE = 4
    BIG_MINE = 5
    REFILL_MINE = 6
    EASIER_RESEARCH = 7


class GamePlayer:
    
    def __init__(self):
        self.donkey_count = 0
        self.wagon_count = 0
        self.truck_count = 0
        self.raft_count = 0
        self.rowboat_count = 0
        self.steamship_count = 0
        self.researches = set()

    def export_state(self):
        return {
            "donkey_count": self.donkey_count,
            "wagon_count": self.wagon_count,
            "truck_count": self.truck_count,
            "raft_count": self.raft_count,
            "rowboat_count": self.rowboat_count,
            "steamship_count": self.steamship_count,
            "researches": list(self.researches),
        }

    # return name of transport
    def add_new_transport(self, transport_type):
        assert(self.land_transport_count() + self.water_transport_count() <= TOTAL_TRANSPORT_COUNT)
        if transport_type == PlayerToken.DONKEY:
            assert(self.land_transport_count() <= TOTAL_LAND_TRANSPORT_COUNT)
            self.donkey_count += 1
            return "donkey " + str(self.donkey_count)
        elif transport_type == PlayerToken.WAGON:
            assert(self.land_transport_count() <= TOTAL_LAND_TRANSPORT_COUNT)
            self.wagon_count += 1
            return "wagon " + str(self.wagon_count)
        elif transport_type == PlayerToken.TRUCK:
            assert(self.land_transport_count() <= TOTAL_LAND_TRANSPORT_COUNT)
            self.truck_count += 1
            return "truck " + str(self.truck_count)
        elif transport_type == PlayerToken.RAFT:
            assert(self.water_transport_count() <= TOTAL_WATER_TRANSPORT_COUNT)
            self.raft_count += 1
            return "raft " + str(self.raft_count)
        elif transport_type == PlayerToken.ROWBOAT:
            assert(self.water_transport_count() <= TOTAL_WATER_TRANSPORT_COUNT)
            self.rowboat_count += 1
            return "rowboat " + str(self.rowboat_count)
        elif transport_type == PlayerToken.STEAMSHIP:
            assert(self.water_transport_count() <= TOTAL_WATER_TRANSPORT_COUNT)
            self.steamship_count += 1
            return "steamship " + str(self.steamship_count)
        else:
            raise ValueError("Invalid transport type")
        
    def land_transport_count(self):
        return self.donkey_count + self.wagon_count + self.truck_count

    def water_transport_count(self):
        return self.raft_count + self.rowboat_count + self.steamship_count
