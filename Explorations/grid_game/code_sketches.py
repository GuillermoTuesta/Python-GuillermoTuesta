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

class MapArray: # First draft of MapArray class. Singleton?
    def __init__(self):
        self.map_array = None
        self.empty_grids = None
        self.valid_grids = None
        self.current_seed = None
    
    @property
    def map_array(self) -> list: # Lazy property. If not set then it'll generate a new map before returning.
        if self._map_array == None:
            self.map_array = self.generate_map_array()
        return self._map_array

    @map_array.setter
    def map_array(self, arr: list):
        if not isinstance(arr, list):
            raise TypeError(f'map_array.setter: given arr is not a list. type(arr) = {type(arr)} ')
        if len(arr) != 16*16:
            raise ValueError(f'map_array.setter: Given arr does not have the correct length. len(arr) = {len(arr)} ')
        self._map_array = arr
        for y in range(16):
            for x in range(16):
                if (x,y) != arr[x + (y * 16)]:
                    raise ValueError(f'MapArray Class map_array.setter, passed value cordarr[{x + (y * 16)}]')

    @map_array.deleter
    def map_array(self):
        self._map_array = None # Just turn it into None, don't use the setter.

    def generate_map_array(self, seed=None) -> list: # Seeds will just save each grid's given number.
        new_map_array = []
        new_seed = []

        for y in range(16):
            for x in range(16):  
                grid_num = random.randrange(1,23) if not seed else seed[x + (y * 16)] # Grid_num is random unless a seed is given.
                new_map_array.append([grid_num, (x, y)]) # Append random numbers to randomize grid type.
                new_seed.append(grid_num) # If a seed was given, it'll save it again.

        self.map_array = new_map_array
        self.current_seed = new_seed

    @property
    def empty_grids(self): # Keeps track of current empty grids. Returns False if there is no generated map. Is also a lazy property.
        if self.map_array == None:
            return False
        if self.empty_grids == None:
            self._empty_grids = [arr[0] for arr in self.map_array if arr[0] in range (14)] # Return all grass grids (empty grids that can be spawned on)
        return self.empty_grids





# Far fetched ideas...






# https://www.codespeedy.com/__setitem__-and-__getitem__-in-python-with-example/
# https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
# Testing this out so it can be more easily handled.
# Singleton class as well, which adds all new instances to it's own list without creating objects.
# And renderer should probably be it's own class, it'll handle conversions and image blitting.

""" class Grids:
    # Overriding magic methods to make it a singleton and handle a list of 'instances', and handles index behaviour.
    def __new__(cls):
        if not hasattr(cls, 'instance'): # Create new instance if one doesn't already exist. Otherwise, do not create a new one.
            cls.instance = super(Grids, cls).__new__(cls)
            cls.grid_list = [None]*64 # Default value. It will only hold 64 grids.
        return cls.instance

    def __setitem__(cls, index: int, map_arr: list, img: *PYGAME IMAGE OBJECT*, walkable: bool, rect: *PYGAME RECT OBJECT*, interact_func: function):
        cls[index] = {'grid_num':map_arr[0], 'cords':map_arr[1], 'image':img, 'walkable':walkable, 'rect':rect} # Add {Grid_num, cords, image, walkable, rect}

    def __getitem__(cls, index):
        return cls.grid_list[index] # Return item from created grid_list. Maybe the indexing should instead follow cords instead of just 0-64?

    @property
    def cords(cls, index: int) -> list: # Dependant on the cord list given by the __new__ override.
        return cls[index]['cords']

    @property
    def image(cls, index: int) -> *image object*: # Sort of lazy property. Gets corresponding image when it's actually asked for.
        img_element = cls[index]['image'] # Get img element from grid_list. Could be a name in str format.
        if img_element == str: # If it is a str, turn it into an image object.
            cls[index]['image'] = pygame IMAGE TRANSFORM!!!!!
        return img_element # Return the element.
    
    @property
    def walkable(cls, index: int) -> bool:
        return cls[index]['walkable']
    
    @property
    def rect(cls, index: int) -> *rect pygame object*: # Lazy property. Computes rect on demand.
        rect_element = cls[index]['rect']
        if rect_element == None:
            cls[index]['rect'] = pygame.Rect(rect_element[index][1][0] * unit_length, rect_element[index][1][0][1] * unit_length, unit_length, unit_length) # Get cords and actually make a rect.
        return cls[index]['rect']

    def render_all(cls):
        for render_index in range(64):
            screen.blit(cls[render_index].image, cls[render_index].rect)

class InteractFuncs: # Oooh... Maybe?
    def __init__(self, func):
        self. """
            




        



