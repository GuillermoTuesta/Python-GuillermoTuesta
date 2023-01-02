import pygame
import pygame.freetype
import random
import sys

pygame.freetype.init()
def display():
    screen.fill(black)

    pygame.draw.rect(screen, dgrey, table_rect)

    spacing_count = 0
    for image in resource_images:
        screen.blit(image, (unit_length * 16 + ms * 2, unit_length * spacing_count + ms * 2))
        spacing_count += 1

    spacing_count = 0
    while spacing_count in range(len(character.inventory.current_inventory)): # Keep track of spacing and render each inventory item individually.
        text.render_to(screen, (unit_length * 17, unit_length * spacing_count + ms * 2), f": {character.inventory.current_inventory[spacing_count]}",
                       fgcolor=white, size=25)
        spacing_count += 1

    text.render_to(screen, (unit_length * 17 - ms * 4, unit_length * 5 + ms * 2), f"CRAFTING",
                   fgcolor=white, size=25)

    for g in grids:
        g.render()

    crafting_axes.render()
    crafting_pickaxes.render()

    for pickup in pickup_resources:
        pickup.render()

    screen.blit(character.img, character.rect)
    pygame.display.flip()

class MapArray: # Handles map array creation. 
    def __init__(self):
        self._current_map = None
        self._grass_cords = None
        self._valid_cords = None
        self._seed = None
    
    @property
    def current_map(self) -> list: # Lazy property. If not set then it'll generate a new map before returning.
        if self._current_map == None:
            self.current_map = self.generate_map_array()
        return self._current_map

    @current_map.setter
    def current_map(self, arr: list):
        if not isinstance(arr, list):
            raise TypeError(f'current_map.setter: given arr is not a list. type(arr) = {type(arr)} ')
        if len(arr) != 16*16:
            raise ValueError(f'current_map.setter: Given arr does not have the correct length. len(arr) = {len(arr)} ')
        self._current_map = arr

    @current_map.deleter
    def current_map(self):
        self._current_map = None # Just turn it into None, don't use the setter.

    @property
    def grass_cords(self) -> list: # Lazy properties. No setters needed.
        if self._grass_cords == None:
            self._grass_cords = [grid_arr[1] for grid_arr in self.current_map if grid_arr[0] in range(14)] # Makes a list of cords that have a grass grid_num.
        return self._grass_cords
    
    @property
    def seed(self) -> list:
        if self._seed == None:
            self._seed = [grid_arr[0] for grid_arr in self.current_map] # Append all grid_nums from current map.
        return self._seed

    @property
    def valid_cords(self) -> list:
        if self._valid_cords == None:
            self._valid_cords = [grid_arr[1] for grid_arr in self.current_map] # Save all valid cords.
        return self._valid_cords

    def generate_map_array(self, seed=None) -> list: # Seeds are a list of numbers between 0, 23.
        new_map = []
        for y in range(16):
            for x in range(16):  
                grid_num = random.randrange(1,23) if not seed else seed[x + (y * 16)] # Grid_num is random unless a seed is given.
                new_map.append([grid_num, (x, y)]) # Append grid_num and corresponding cord.

        self.current_map = new_map
        self._grass_grids = None # Reset grass grids.
        self._seed = None # Reset seed.

mapper = MapArray() # Immediately make an instance.
mapper.generate_map_array()

class Inventory: # Inventory class to handle everything to do with the character's inventory.
    def __init__(self, starting_inventory:dict = {'Wood': 0, 'Rock': 0, 'Iron': 0}): # Ugly default value for starting_list.
        self.current_inventory = starting_inventory
    
    @property
    def current_inventory(self):
        return self._current_inventory
    
    @current_inventory.setter
    def current_inventory(self, dict_value: dict):
        if not isinstance(dict_value, dict):
            raise TypeError(f'Inventory descriptor class in Character, __set__: Given dict_value is not a dictionary. type(dict_value) = {type(dict_value)} ')
        if len(dict_value) != 3: # Ugly default value! I only have 3 resources in the game at the moment.
            raise ValueError(f'Inventory descriptor class in Character, __set__: Given dict_value is not of length 3. len(dict_value) = {len(dict_value)} ')
        for value_index, value in dict_value.items():
            if value < 0:
                raise ValueError(f'Inventory descriptor class in Character, __set__: dict_value[{value_index}] ( = {dict_value[value_index]}) is less than zero. ')
        self._current_inventory = dict_value 

    def add(self, value_dict: dict) -> bool: # Returns True if successful.
        for given_name in value_dict.keys(): # Loop to check if value_dict contains any invalid resource names.
            if given_name not in self.current_inventory.keys():
                raise AttributeError(f'Inventory class, add function: Given dict contains invalid names. ({value_dict.keys()}) ')
        for value in value_dict.values():
            if value < 0:
                raise ValueError(f'Inventory class, add function: Given dict contains a value that is < 0. ({value_dict}) ')
        for resource_name, value in value_dict.items(): # If no errors are raised, then add all resources in value_dict to inventory.
            self.current_inventory[resource_name] += value
        return True
    
    def subtract(self, value_dict) -> bool: # Returns True is successful.
        for given_name in value_dict.keys(): # Loop to check if value_dict contains any invalid resource names.
            if given_name not in self.current_inventory.keys():
                raise AttributeError(f'Inventory class, subtract function: Given dict contains invalid names. ({value_dict.keys()}) ')
        for value in value_dict.items():
            if value < 0:
                raise ValueError(f'Inventory class, subtract function: Given dict contains a value that is < 0. ({value_dict}) ')
        for resource_name, value in value_dict: # If no errors are raised, then subtract all resources.
            self.current_inventory[resource_name] -= value
        return True

class Character:
    inventory = Inventory()

    def __init__(self):
        self._cords = random.choice(mapper.grass_cords)
        self.rect = pygame.Rect(self.cords[0] * unit_length, self.cords[1] * unit_length, unit_length, unit_length)
        self.img = character_image
        self.pickaxe_count = 0
        self.axe_count = 1

    @property
    def cords(self):
        return self._cords
    
    @cords.setter
    def cords(self, new_cords): # Will handle all input validation, including some game logic.
        if not isinstance(new_cords, tuple):
            raise TypeError(f'Character class cord setter: new_cords not a tuple, it''s of type {type(new_cords)}')
        if len(new_cords) != 2:
            raise AttributeError(f'Character class cord setter: len(new_cords) = {len(new_cords)}. Can only be of length 2')
        if new_cords not in mapper.valid_cords: # I believe coordinates should always follow these conditions, so I'm putting them in the decorator.
            raise ValueError(f'Character class cords.setter: Given cords are out of bounds ({new_cords}).')
        if grids[new_cords[0] + new_cords[1] * 16].walkable:
                self._cords = new_cords

    def move(self):
        PressedKey = event.key # Save the key that was pressed.
        x, y = self.cords # Tuple unpacking, save current cords for later comparisons.
        if PressedKey == pygame.K_UP:
            self.cords = (x, y - 1) 
        if PressedKey == pygame.K_DOWN:
            self.cords = (x, y + 1)
        if PressedKey == pygame.K_LEFT:
            self.cords = (x - 1, y)
        if PressedKey == pygame.K_RIGHT:
            self.cords = (x + 1, y)

        if self.cords == (x, y) and event.mod and pygame.KMOD_LSHIFT: # If still standing on the same spot and pressed leftshift..
            for m in pickup_resources:
                if m.cords == self.cords: # If standing on a pickup resource, use it.
                    m.interact()

        if self.cords != (x, y) and event.mod and pygame.KMOD_LSHIFT and not grids[self.cords[0] + (self.cords[1] * 16)].walkable: # If cords were successfully changed, and the modifier key is leftshift, and the target grid is not walkable:
            grids[self.cords[0] + (self.cords[1] * 16)].interact() # Interact with the target grid. cords.setter handled validation already.
            self.cords = x, y # Return to previous Grid.

        if self.cords != (x, y):
            self.rect = pygame.Rect(self.cords[0] * unit_length, self.cords[1] * unit_length, unit_length, unit_length) # Update rect if cords were changed.

class Grid:
    def __init__(self, cords, walkable, img):
        self.walkable = walkable
        self.cords = cords
        self.rect = pygame.Rect(cords[0] * unit_length, cords[1] * unit_length, unit_length, unit_length)
        self.img = img

    def render(self):
        screen.blit(self.img, self.rect)

class Grass(Grid):
    def __init__(self, cords, img):
        super().__init__(cords, True, img)

    def interact(self):
        pass

class Water(Grid):
    def __init__(self, cords, img):
        super().__init__(cords, False, img)

    def interact(self):
        pass

class Tree(Grid):
    def __init__(self, cords, img):
        super().__init__(cords, False, img)
        self.health = 10

    def interact(self):
        self.health -= character.axe_count * 2  # character.axe_count starts from 1
        if self.health <= 0:
            grids[self.cords[0] + (self.cords[1] * 16)] = Grass(self.cords, grass_image) # Formula finds index via cords and turns itself into a grass grid.
            character.inventory.add({'Wood':5})
        
    def render(self):
        screen.blit(grass_image, self.rect) # Render a grass square first, then pass onto superclass render().
        super().render()

class Rock(Grid):
    def __init__(self, cords, img):
        super().__init__(cords, False, img)
        self.health = 20

    def interact(self):
        self.health -= character.pickaxe_count * 2  # character.pickaxe_count starts from 0
        if self.health <= 0:
            grids[self.cords[0] + (self.cords[1] * 16)] = Grass(self.cords, grass_image) # Formula finds index via cords and turns itself into a grass grid.
            character.inventory.add({'Rock':5})
            if random.randint(0, 3) == 1:
                character.inventory.add({'Iron':5})
    
    def render(self):
        screen.blit(grass_image, self.rect)
        super().render()

class PickupResource(Grid): 
    # A resource that spawns on the world and can simply be picked up without any harvesting required.
    def __init__(self, cords, img): # Coordinates to spawn, image to use.
        super().__init__(cords, True, img)
        self.rect = pygame.Rect(cords[0] * unit_length + int(unit_length / 2),
                                cords[1] * unit_length + int(unit_length / 2), unit_length, unit_length)

class WoodPickup(PickupResource):
    def __init__(self, cords, img):
        super().__init__(cords, img)

    def interact(self):
        character.inventory.add({'Wood':5})
        pickup_resources.remove(self)

class StonePickup(PickupResource):
    def __init__(self, cords, img):
        super().__init__(cords, img)

    def interact(self):
        character.inventory.add({'Rock':5})
        pickup_resources.remove(self)

class CraftingSeq: # Doesn't handle end of crafting list yet.
    def __init__(self, image_seq: list, recipe_seq: dict, name_seq: str, cords):
        self._seq_index = 0 # Always start from first item.
        self.image_seq = image_seq
        self.recipe_seq = recipe_seq
        self.name_seq = name_seq
        self.cords = cords
        self.rect = pygame.Rect(cords[0] * unit_length + ms * 2, cords[1] * unit_length, unit_length//2, unit_length//2)
        self.tooltip_rect = pygame.Rect(cords[0] * unit_length + ms * 2, cords[1] * unit_length, unit_length * 2, unit_length * 1.5)

        #Lazy Properties later on..
        self._image = None
        self._recipe = None
        self._item_name = None

        if not (len(self.image_seq) == len(self.recipe_seq)): # Where to put this?
            raise AttributeError(f'CraftingSquare class __init__, Seq lengths do not match: image_seq: {len(self.image_seq)}, recipe_seq: {len(self.recipe_seq)}')
        self.seq_max_len = len(self.image_seq) # Any given slist will work.

    @property 
    def seq_index(self): # Property to hold the current index of the class.
        return self._seq_index

    @seq_index.setter
    def seq_index(self, value): # Ugly. Maybe just a normal function would be better?
        new_seq_index = self.seq_index + value
        if not isinstance(value, int):
            raise TypeError(f'CraftingSquare class seq_index.setter: Passed value is not of type int. type(value) = {type(value)} ')
        if new_seq_index not in range(self.seq_max_len):
            raise ValueError(f'CraftingSquare class seq_index.setter: Passed value gives an invalid index. self.seq_index + value = {self.seq_index + value} ')
        if value < 0:
            raise ValueError(f'CraftingSquare class seq_index.setter: Passed value is < 0. ')
        self._seq_index = new_seq_index
        self.image = None
        self.recipe = None
        self.item_name = None

    @property
    def image(self): # Lazy property. Returns current image in sequence.
        if self._image == None:
            self._image = self.image_seq[self.seq_index]
        return self._image 

    @property
    def recipe(self): # Lazy property. Returns current recipe in sequence.
        if self.recipe == None:
            self._recipe = self.recipe_seq[self.seq_index]
        return self._recipe

    @property
    def item_name(self): # Lazy property. Returns current item_name in sequence.
        if self.item_name == None:
            self._item_name = self.name_seq[self.seq_index]
        return self._item_name

    def render(self):
        screen.blit(self.image, self.rect)
    
    def render_tooltip(self): # I don't dare touch this. It renders a tooltip, which I call when the mouse is hovered above the crafting square.
        pygame.draw.rect(screen, black, self.tooltip_rect)
        text.render_to(screen, (self.cords[0] * unit_length + ms * 3, self.cords[1] * unit_length + ms), f"{self.item_name}",
                       fgcolor=white, size=15)
        text.render_to(screen, (self.cords[0] * unit_length + ms * 3, (self.cords[1] + 1) * unit_length + ms),
                       f"{self.recipe}", fgcolor=white, size=15)

    def craft(self, inventory: Inventory) -> bool: # Inventory descriptor class is expected.
        for resource_name in self.recipe.keys(): # First check if all crafting conditions are met.
            if inventory[resource_name] < self.recipe[resource_name]: # If player has less than the amount of required resources, return False.
                return False
        for resource_name in self.recipe.keys():
            inventory.subtract(resource_name, self.recipe[resource_name]) # Use subtract function, pass resource_name and it's corresponding recipe value to subtract.       
        return True

unit_length = int(960/16)
square_size = (unit_length, unit_length)
icon_size = (int(unit_length / 2), int(unit_length / 2))
pickup_size = (int(unit_length / 4), int(unit_length / 4))
ms = 5  # margin_space value, for consistent spacing
text = pygame.freetype.Font(None, size=14)  # default font, used for all text
screen = pygame.display.set_mode((unit_length * 20, unit_length * 16))
table_rect = pygame.Rect((unit_length * 16 + ms, unit_length * 0 + ms), (unit_length * 4 - 2 * ms, unit_length * 16 - 2 * ms))

black = (0, 0, 0)
dgrey = (51, 51, 77)
white = (255, 255, 255)

character_image = pygame.transform.scale(pygame.image.load("character.png"), square_size)
grass_image = pygame.transform.scale(pygame.image.load("grass.png"), square_size)
water_image = pygame.transform.scale(pygame.image.load("water.png"), square_size)
tree_image = pygame.transform.scale(pygame.image.load("tree.png"), square_size)
rock_image = pygame.transform.scale(pygame.image.load("rock.png"), square_size)
wood_image_icon = pygame.transform.scale(pygame.image.load("wood.png"), icon_size)
stone_image_icon = pygame.transform.scale(pygame.image.load("stone.png"), icon_size)
iron_image_icon = pygame.transform.scale(pygame.image.load("iron.png"), icon_size)
wood_image_pickup = pygame.transform.scale(pygame.image.load("wood.png"), pickup_size)
stone_image_pickup = pygame.transform.scale(pygame.image.load("stone.png"), pickup_size)
resource_images = [wood_image_icon, stone_image_icon, iron_image_icon]

axes_image_icon_seq = [pygame.transform.scale(pygame.image.load('Sprites/Axes/WoodAxe.png'), icon_size), pygame.transform.scale(pygame.image.load('Sprites/Axes/StoneAxe.png'), icon_size), pygame.transform.scale(pygame.image.load('Sprites/Axes/IronAxe.png'), icon_size)]
pickaxes_image_icon_seq = [pygame.transform.scale(pygame.image.load('Sprites/Pickaxes/WoodPickaxe.png'), icon_size), pygame.transform.scale(pygame.image.load('Sprites/Pickaxes/StonePickaxe.png'), icon_size), pygame.transform.scale(pygame.image.load('Sprites/Pickaxes/IronPickaxe.png'), icon_size)]
generic_recipe_seq = [{'Wood': 20}, {'Wood': 20, 'Stone': 20}, {'Wood': 20, 'Stone': 20, 'Iron': 20}] # Generic seq for now, can make my own recipe seqs later on if I want.
axes_name_seq = ['Wood Axe', 'Stone Axe', 'Iron Axe']
pickaxes_name_seq = ['Wood Pickaxe', 'Stone Pickaxe', 'Iron Pickaxe']

crafting_axes = CraftingSeq(axes_image_icon_seq, generic_recipe_seq, axes_name_seq, [15,15])
crafting_pickaxes = CraftingSeq(pickaxes_image_icon_seq, generic_recipe_seq, pickaxes_name_seq, [14,14])

character = Character()

pickup_resources = []
valid_cords = [grid_arr[1] for grid_arr in mapper.current_map] # Save all valid coordinates.
grids = []
for m in mapper.current_map:
    if m[0] in range(14):
        grids.append(Grass(m[1], grass_image))
        if m[0] in range(3):
            pickup_resources.append(WoodPickup(m[1], wood_image_pickup))
        if m[0] in range(3, 5):
            pickup_resources.append(StonePickup(m[1], stone_image_pickup))
    if m[0] in range(14, 17):
        grids.append(Water(m[1], water_image))
    if m[0] in range(17, 21):
        grids.append(Tree(m[1], tree_image))
    if m[0] in range(21, 23):
        grids.append(Rock(m[1], rock_image))

character = Character()

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for craftable in craftables:
                if craftable.rect.collidepoint(mouse_pos):
                    if craftable.craft(character.inventory):
                        pass

        if event.type == pygame.KEYDOWN:
            character.move()

    display()