
from .game_tokens import PlayerToken

class GamePlayer:
    donkey_count = 0
    wagon_count = 0
    truck_count = 0
    raft_count = 0
    rowboat_count = 0
    steamship_count = 0
    
    def __init__(self):
        None

    def get_new_transport_name(self, transport_type):
        if transport_type == PlayerToken.DONKEY:
            self.donkey_count += 1
            return "Donkey " + str(self.donkey_count)
        elif transport_type == PlayerToken.WAGON:
            self.wagon_count += 1
            return "Wagon " + str(self.wagon_count)
        elif transport_type == PlayerToken.TRUCK:
            self.truck_count += 1
            return "Truck " + str(self.truck_count)
        elif transport_type == PlayerToken.RAFT:
            self.raft_count += 1
            return "Raft " + str(self.raft_count)
        elif transport_type == PlayerToken.ROWBOAT:
            self.rowboat_count += 1
            return "Rowboat " + str(self.rowboat_count)
        elif transport_type == PlayerToken.STEAMSHIP:
            self.steamship_count += 1
            return "Steamship " + str(self.steamship_count)
        else:
            raise ValueError("Invalid transport type")