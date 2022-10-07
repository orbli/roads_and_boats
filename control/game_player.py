
from .game_tokens import PlayerToken
import names

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
        self.transporter_count = {}
        self.researches = set()
        self.home = None

    def export_state(self):
        return {
            'transporter_count': self.transporter_count,
            "researches": list(self.researches),
            "home": list(self.home),
        }

    # return name of transport
    def add_new_transport(self, transport_type):
        assert(self.land_transport_count() + self.water_transport_count() <= TOTAL_TRANSPORT_COUNT)
        if transport_type <= 2: # land_transport
            assert(self.land_transport_count() <= TOTAL_LAND_TRANSPORT_COUNT)
        elif transport_type >= 3: # water_transport
            assert(self.water_transport_count() <= TOTAL_WATER_TRANSPORT_COUNT)
        if transport_type not in self.transporter_count:
            self.transporter_count[transport_type] = 0
        self.transporter_count[transport_type] += 1
        
        transporter_name = [ 'donkey', 'wagon', 'truck', 'raft', 'rowboat', 'steamship' ]
        return f"{transporter_name[transport_type]} {names.get_first_name()}"
        
    def remove_transport(self, transport_type):
        assert(transport_type in self.transporter_count)
        self.transporter_count[transport_type] -= 1
        if self.transporter_count[transport_type] == 0:
            del self.transporter_count[transport_type]

    def land_transport_count(self):
        return sum([self.transporter_count.get(i, 0) for i in range(3)])

    def water_transport_count(self):
        return sum([self.transporter_count.get(i, 0) for i in range(3, 6)])