class ResourceIcon:
    def __init__(self, img):
        resource_icons.append(self)


class StoneIcon(ResourceIcon):
    def __init__(self):
        self.img = stone_image

    def render(self, ul):
        screen.blit(self.img, (unit_length * 16 + ms * 2, unit_length * ul + ms * 2))


class WoodIcon(ResourceIcon): 
    def __init__(self):
        self.img = wood_image

    def render(self, ul):
        screen.blit(self.img, (unit_length * 16 + ms * 2, unit_length * ul + ms * 2))

    def craft(self, old_inventory):
        new_inventory = old_inventory.copy()
        for i in range(len(self.recipe)):
            new_inventory[i] = new_inventory[i] - self.recipe[i]
        for i in inventory:
            if i < 0:
                return None
        self.list.append(self.item)
        return inventory

class Inventory: # First draft of inventory descriptor class.
    def __init__(self, starting_inventory={'Wood': 0, 'Stone': 0, 'Iron': 0}): # Ugly default value for starting_list.
        self.inventory = starting_inventory

    def __get__(self, obj, objtype=None) -> dict:
        return self.inventory
    
    def add(self, resource_name, value) -> bool: # Returns True if sucessful. I don't think there are any 'fail states' so it can either only Err or return true.
        if resource_name not in self.inventory.keys(): # If given resource name isn't found in list of keys..
            raise AttributeError(f'Inventory descriptor class in Character, add function: Given resource_name does not exist. ({resource_name})')
        if value <= 0:
            raise ValueError(f'Inventory descriptor class in Character, add function: Given value is <= 0. ({value})')
        self.inventory[resource_name] += value
        return True
    
    def subtract(self, resource_name, value) -> bool:
        if resource_name not in self.inventory.keys():
            raise AttributeError(f'Inventory descriptor class in Character, subtract function: Given resource_name does not exist. ({resource_name})')
        if value > self.inventory[resource_name]: # Prevents resources from ever having a negative value.
            return False
        self.inventory[resource_name] -= value
        return True

@dataclass # Try dataclass instead maybe?
class MapArray:
    pass

class MapArray: # First draft of MapArray class. Singleton?
    def __init__(self):
        self.map_array = None
        self.empty_grids = None
        self.valid_grids = None
    
    @property
    def map_array(self):
        return self._map_array # Could be None. Otherwise should always hold the latest generated map_array.

    @map_array.setter
    def map_array(self, arr: list):
        if not isinstance(arr, list):
            raise TypeError(f'map_array.setter: given arr is not a list. type(arr) = {type(arr)} ')
        if len(arr) != 16*16:
            raise ValueError(f'map_array.setter: Given arr does not have the correct length. len(arr) = {len(arr)} ')
        self._map_array = arr

    @map_array.deleter
    def map_array(self):
        self._map_array = None # Just turn it into None, don't use the setter.

    def generate_map_array(self, seed=None): # Seeds will just save each grid's given number.
        new_map_array = []
        for y in range(16):
            for x in range(16):
                new_map_array.append([random.randrange(1, 23), (x, y)])
        self.map_array = new_map_array

    @property
    def empty_grids(self):
        if self.map_array == None:
            return False
        if self.empty_grids == None:
            self._empty_grids = [arr[0] for arr in self.map_array if arr[0] in range (14)] # Return all grass grids (empty grids that can be spawned on)
        return self.empty_grids


class Grids:
    grid_list = []
    def __init__(self):
        




        



