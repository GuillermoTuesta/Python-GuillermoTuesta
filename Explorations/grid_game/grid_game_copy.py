import pygame
import pygame.freetype
import random
import sys
from abc import ABC, abstractmethod

pygame.freetype.init()
def display():
    screen.fill(black)

    pygame.draw.rect(screen, dgrey, table_rect)

    spacing_count = 0
    for image in resource_images:
        screen.blit(image, (unit_length * 16 + ms * 2, unit_length * spacing_count + ms * 2))
        spacing_count += 1

    spacing_count = 0
    while spacing_count in range(len(inventory)):
        text.render_to(screen, (unit_length * 17, unit_length * spacing_count + ms * 2), f": {inventory[spacing_count]}",
                       fgcolor=white, size=25)
        spacing_count += 1

    text.render_to(screen, (unit_length * 17 - ms * 4, unit_length * 5 + ms * 2), f"CRAFTING",
                   fgcolor=white, size=25)

    for g in grids:
        g.render()

    for craftable in craftables:
        craftable.render()

    for craftable in craftables:
        if craftable.rect.collidepoint(mouse_pos):
            craftable.render_tooltip()

    for pickup in pickup_resources:
        pickup.render()

    screen.blit(character.img, character.rect)
    pygame.display.flip()

class Character:
    def __init__(self, cords):
        self.cords = cords
        self.rect = pygame.Rect(cords[0] * unit_length, cords[1] * unit_length, unit_length, unit_length)
        self.img = character_image
        self.pickaxe_count = 0
        self.axe_count = 1
    
    @property
    def cords(self):
        return self._cords
    
    @cords.setter
    def cords(self, new_cords): # Will handle all input validation, including some game logic.
        if not isinstance(new_cords, tuple):
            raise TypeError(f'Character class cord setter: new_cords is of type {type(new_cords)}')
        if len(new_cords) != 2:
            raise AttributeError(f'Character class cord setter: len(new_cords) = {len(new_cords)}. Can only be of length 2')
        if new_cords in grid_cords: # I believe the cords variable should always follow these conditions, so I'm putting them in the decorator.
            if grids[self.cords[0] + self.cords[1] * 16].walkable:
                self._cords = new_cords

    def move(self):
        PressedKey = event.key # Save the key that was pressed
        x, y = self.cords # Tuple unpacking, save previous cords for later comparisons.
        if PressedKey == pygame.K_UP:
            self.cords   = (x, y - 1) 
        if PressedKey == pygame.K_DOWN:
            self.cords   = (x, y + 1)
        if PressedKey == pygame.K_LEFT:
            self.cords   = (x - 1, y)
        if PressedKey == pygame.K_RIGHT:
            self.cords   = (x + 1, y)

        if self.cords == (x, y) and event.mod and pygame.KMOD_LSHIFT: # If still standing on the same spot and pressed leftshift, pickup resources.
            for m in pickup_resources:
                if m.cords == self.cords:
                    m.interact()

        if self.cords != (x, y) and event.mod and pygame.KMOD_LSHIFT: # If cords were successfully changed, and the modifier key is leftshift:
            grids[self.cords[0] + (self.cords[1] * 16)].interact() # Interact with the target grid. cords.setter handled validation already.
            self.cords = x, y # Return to previous Grid.

        self.rect = pygame.Rect(self.cords[0] * unit_length, self.cords[1] * unit_length, unit_length, unit_length)

class Grid:
    def __init__(self, cords, walkable, img):
        self.walkable = walkable
        self.cords = cords
        self.rect = pygame.Rect(cords[0] * unit_length, cords[1] * unit_length, unit_length, unit_length)
        self.img = img

    def render(self):
        if type(self).__name__ == "Tree" or type(self).__name__ == "Rock":
            screen.blit(grass_image, self.rect)
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
            grids[self.cords[0] + (self.cords[1] * 16)] = Grass(self.cords, grass_image)
            inventory[0] += 5

class Rock(Grid):
    def __init__(self, map_element, img):
        super().__init__(map_element, False, img)
        self.health = 20

    def interact(self):
        self.health -= character.pickaxe_count * 2  # character.pickaxe_count starts from 0
        if self.health <= 0:
            grids[self.cords[0] + (self.cords[1] * 16)] = Grass(self.cords, grass_image)
            inventory[1] += 5
            if random.randint(0, 3) == 1:
                inventory[2] += 5

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
        inventory[0] += 5
        pickup_resources.remove(self)

class StonePickup(PickupResource):
    def __init__(self, cords, img):
        super().__init__(cords, img)

    def interact(self):
        inventory[1] += 5
        pickup_resources.remove(self)

all_items = []
class CraftingSquare1:
    def __init__(self, image_seq, recipe_list, image_seq_index, placement_index, cords,  item_name):
        self.image_seq = image_seq
        self.recipe_list = recipe_list
        self.image_seq_index = image_seq_index
        self.placement_index = placement_index
        self.cords = cords
        self.item_name = item_name
        self.rect = pygame.Rect(left, top, unit_length//2, unit_length//2)

    @property
    def image_seq_index(self):
        return self._image_seq_index
    
    @image_seq_index.setter
    def image_seq_index(self, value):
        if not isinstance(value, int):
            raise TypeError(f'CraftingSquare class image_seq_index.setter: value is not of type int. type(value) = {type(value)}')
        if value not in range(len(self.image_seq)):
            raise AttributeError(f'CraftingSquare class image_seq_index.setter: value is outside of possible range. ')
        self._image_seq_index = value

    @property
    def image(self):
        return self.image_seq[self.image_seq_index] # Returns current image in sequence.

    def render(self):
        screen.blit()

class CraftingSquare:
    def __init__(self, recipe, cords, item, img_name):
        all_items.append(self)
        self.img = img_name
        self.recipe = recipe
        self.cords = cords
        self.index = 0
        self.item = item
        self.rect = pygame.Rect(cords[0] * unit_length + ms * 2, cords[1] * unit_length, int(unit_length / 2),
                                int(unit_length / 2))
        self.tooltip_rect = pygame.Rect(cords[0] * unit_length + ms * 2, cords[1] * unit_length, unit_length * 2,
                                        unit_length * 1.5)

    def render(self):
        screen.blit(self.img, self.rect)

    def render_tooltip(self):
        pygame.draw.rect(screen, black, self.tooltip_rect)
        text.render_to(screen, (self.cords[0] * unit_length + ms * 3, self.cords[1] * unit_length + ms), f"{self.item}",
                       fgcolor=white, size=15)
        text.render_to(screen, (self.cords[0] * unit_length + ms * 3, (self.cords[1] + 1) * unit_length + ms),
                       f"{self.recipe}", fgcolor=white, size=15)

    def switch(self, craftable, craftables): # i had a nice function for this before but i have to do this like a caveman instead apparently
        if craftable in crafting_pickaxes:
            if pickaxe_index in range(len(crafting_pickaxes)):
                craftables[craftables.index(self)] = crafting_pickaxes[pickaxe_index]
                pickaxe_index += 1
        if craftable in crafting_axes:
            if axe_index in range(len(crafting_axes)):
                craftables[craftables.index(self)] = crafting_axes[axe_index]
                axe_index += 1        

    def craft(self, inventory):  # thanks blubberquark (same idea, but very nicely written)
        for i, j in zip(inventory, self.recipe):
            if i < j:
                return False
        for i, n in enumerate(self.recipe):
            inventory[i] = inventory[i] - n
            if self in crafting_axes:
                character.axe_count += 1
            if self in crafting_pickaxes:
                character.pickaxe_count += 1
        return True

class WoodAxe(CraftingSquare):
    def __init__(self, cords):
        super().__init__([20], cords, "Wood Axe", wood_image_icon)

class StoneAxe(CraftingSquare):
    def __init__(self, cords):
        super().__init__([20], cords, "Stone Axe", wood_image_icon)

class IronAxe(CraftingSquare):
    def __init__(self, cords):
        super().__init__([20], cords, "Iron Axe", wood_image_icon)

class WoodPickaxe(CraftingSquare):
    def __init__(self, cords):
        super().__init__([20], cords, "Wood Pickaxe", wood_image_icon)

class StonePickaxe(CraftingSquare):
    def __init__(self, cords):
        super().__init__([20], cords, "Stone Pickaxe", wood_image_icon)

class IronPickaxe(CraftingSquare):
    def __init__(self, cords):
        super().__init__([20], cords, "Iron Pickaxe", wood_image_icon)

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

class Sprite: # Is it really a sprite though?
    def __init__(self, image):
        self.image = image
    
    def render(self):
        pass

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
inventory = [200, 0, 0]  # 1: wood,  2: rock, 3: iron
crafting_axes = [WoodAxe([16, 6]), StoneAxe([16, 6]), IronAxe([16, 6])]
crafting_pickaxes = [WoodPickaxe([17, 6]), StonePickaxe([17, 6]), IronPickaxe([17, 6])]
craftables = [crafting_axes[0], crafting_pickaxes[0]]

map_array = [] # Generates an array of random numbers that'll be converted to an array of grids
for y in range(16):
    for x in range(16):
        map_array.append([random.randrange(1, 23), (x, y)])  # (1-22), randrange excludes the last number

pickup_resources = []
grid_cords = [x[1] for x in map_array]
grass_cords = []
grids = []
for m in map_array:
    if m[0] in range(14):
        grids.append(Grass(m[1], grass_image))
        grass_cords.append(m[1])
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

character = Character(random.choice(grass_cords))

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for craftable in craftables:
                if craftable.rect.collidepoint(mouse_pos):
                    if craftable.craft(inventory):
                        for craftable in craftables:
                            craftable.switch(craftable, craftables)

        if event.type == pygame.KEYDOWN:
            character.move()

    display()