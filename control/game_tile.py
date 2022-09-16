
class Terrain:
    WOOD = 0
    PASTURE = 1
    ROCK = 2
    MOUNTAIN = 3
    DESERT = 4
    WATER = 5

class GameTile:
    terrain = None
    player_tokens = []
    resource_tokens = {}
    building = None
    mine_reserve = None # example data structure: [ Resource.IRON, Resource.IRON, Resource.IRON, Resource.GOLD, Resource.GOLD, Resource.GOLD, ]
    home = None

    def __init__(self, Terrain):
        self.terrain = Terrain

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
