
class Terrain:
    WOOD = 0
    PASTURE = 1
    ROCK = 2
    MOUNTAIN = 3
    DESERT = 4
    WATER = 5

class GameTile:
    terrain = None
    player_tokens = [] # transporter_type, owner, transporter_name, carrying_goods{} / playertoken[], docking_at
    # carrying_goods = {resource_type: resource_amount} -> carry resource
    # carrying_goods = [transporter_type, transporter_owner, transporter_name, {}] -> carrying transporter
    # extra_info: water transporter - need to record which coastline it is on; river: need to record which side the land transporter is on
    resource_tokens = {}
    building = None
    mine_reserve = None # example data structure: [ Resource.IRON, Resource.IRON, Resource.IRON, Resource.GOLD, Resource.GOLD, Resource.GOLD, ]
    home = None

    def export_state(self):
        rt = {
            "terrain": self.terrain,
            "player_tokens": self.player_tokens,
            "resource_tokens": self.resource_tokens,
            "building": self.building,
        }
        if self.mine_reserve is not None:
            rt["mine_reserve"] = self.mine_reserve
        if self.home is not None:
            rt["home"] = self.home
        return rt
    
    def import_state(self, state):
        self.terrain = state["terrain"]
        self.player_tokens = state["player_tokens"]
        self.resource_tokens = state["resource_tokens"]
        self.building = state["building"]
        if "mine_reserve" in state:
            self.mine_reserve = state["mine_reserve"]
        if "home" in state:
            self.home = state["home"]

    @classmethod
    def build_from_state(cls, state):
        rt = cls(state["terrain"])
        rt.import_state(state)
        return rt

    def __init__(self, Terrain):
        self.terrain = Terrain
        self.wall = set()

    def add_resource(self, resource, amount):
        if resource not in self.resource_tokens:
            self.resource_tokens[resource] = 0
        self.resource_tokens[resource] += amount

    def add_resources(self, resources):
        for resource, amount in resources.items():
            self.add_resource(resource, amount)

    def remove_resource(self, resource, amount):
        if resource not in self.resource_tokens:
            raise Exception("Not enough resources.")
        if self.resource_tokens[resource] < amount:
            raise Exception("Not enough resources.")
        self.resource_tokens[resource] -= amount

    def remove_resources(self, resources):
        for resource, amount in resources.items():
            self.remove_resource(resource, amount)

    def have_resource(self, resource, amount):
        if resource not in self.resource_tokens:
            return False
        return self.resource_tokens[resource] >= amount

    def have_resources(self, resources):
        for resource, amount in resources.items():
            if not self.have_resource(resource, amount):
                return False
        return True
