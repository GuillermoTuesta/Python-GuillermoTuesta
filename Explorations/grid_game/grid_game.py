import pygame
import pygame.freetype
import random
import sys

pygame.freetype.init()


def display():
    screen.fill(black)

    pygame.draw.rect(screen, dgrey, table_rect)

    index = 0
    for resource in resources:
        screen.blit(resource, (UnitLength * 16 + ms * 2, UnitLength * index + ms * 2))
        index += 1

    index = 0
    while index in range(len(inventory)):
        text.render_to(screen, (UnitLength * 17, UnitLength * index + ms * 2), f": {inventory[index]}",
                       fgcolor=white, size=25)
        index += 1

    text.render_to(screen, (UnitLength * 17 - ms * 4, UnitLength * 5 + ms * 2), f"CRAFTING",
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
        self.rect = pygame.Rect(cords[0] * UnitLength, cords[1] * UnitLength, UnitLength, UnitLength)
        self.img = character_image
        self.pickaxe_count = 0
        self.axe_count = 1

    def move(self):

        PressedKey = event.key
        x, y = self.cords

        print self.grass_cords  

        if PressedKey == pygame.K_UP:
            self.cords = (x, y - 1)
            print("HEY")
        if PressedKey == pygame.K_DOWN:
            self.cords = (x, y + 1)
        if PressedKey == pygame.K_LEFT:
            self.cords = (x - 1, y)
        if PressedKey == pygame.K_RIGHT:
            self.cords = (x + 1, y)

        if self.cords != (x, y) and event.mod and pygame.KMOD_LSHIFT: # If cords were successfully changed, and the event is a modifier key, and that modifier key is leftshift:
            if self.cords[0] + (self.cords[1] * 16) in range(256): # If the target coordinate is within bounds:
                grids[self.cords[0] + (self.cords[1] * 16)].interact() # Interact with the target grid.
            self.cords = x, y # Return to previous Grid.

        if self.cords == (x, y): # If still standing on the same spot, pickup resources there.
            for m in pickup_resources:
                if m.cords == self.cords:
                    m.interact()

        if self.cords not in grid_cords or not grids[self.cords[0] + self.cords[1] * 16].walkable:
            self.cords = x, y

        self.rect = pygame.Rect(self.cords[0] * UnitLength, self.cords[1] * UnitLength, UnitLength, UnitLength)


class Grid:
    def __init__(self, cords, walkable, img):
        self.walkable = walkable
        self.cords = cords
        self.rect = pygame.Rect(cords[0] * UnitLength, cords[1] * UnitLength, UnitLength, UnitLength)
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
        self.rect = pygame.Rect(cords[0] * UnitLength + int(UnitLength / 2),
                                cords[1] * UnitLength + int(UnitLength / 2), UnitLength, UnitLength)


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
class CraftingSquare:
    def __init__(self, recipe, cords, item, img_name):
        all_items.append(self)
        self.img = img_name
        self.recipe = recipe
        self.cords = cords
        self.index = 0
        self.item = item
        self.rect = pygame.Rect(cords[0] * UnitLength + ms * 2, cords[1] * UnitLength, int(UnitLength / 2),
                                int(UnitLength / 2))
        self.tooltip_rect = pygame.Rect(cords[0] * UnitLength + ms * 2, cords[1] * UnitLength, UnitLength * 2,
                                        UnitLength * 1.5)

    def render(self):
        screen.blit(self.img, self.rect)

    def render_tooltip(self):
        pygame.draw.rect(screen, black, self.tooltip_rect)
        text.render_to(screen, (self.cords[0] * UnitLength + ms * 3, self.cords[1] * UnitLength + ms), f"{self.item}",
                       fgcolor=white, size=15)
        text.render_to(screen, (self.cords[0] * UnitLength + ms * 3, (self.cords[1] + 1) * UnitLength + ms),
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


UnitLength = int(960 / 16)
square = (UnitLength, UnitLength)
icon = (int(UnitLength / 2), int(UnitLength / 2))
pickup_size = (int(UnitLength / 4), int(UnitLength / 4))
ms = 5  # margin_space value, for consistent spacing
text = pygame.freetype.Font(None, size=14)  # default font, used for all text
screen = pygame.display.set_mode((UnitLength * 20, UnitLength * 16))
table_rect = pygame.Rect((UnitLength * 16 + ms, UnitLength * 0 + ms), (UnitLength * 4 - 2 * ms, UnitLength * 16 - 2 * ms))

black = (0, 0, 0)
dgrey = (51, 51, 77)
white = (255, 255, 255)

character_image = pygame.transform.scale(pygame.image.load("character.png"), square)
grass_image = pygame.transform.scale(pygame.image.load("grass.png"), square)
water_image = pygame.transform.scale(pygame.image.load("water.png"), square)
tree_image = pygame.transform.scale(pygame.image.load("tree.png"), square)
rock_image = pygame.transform.scale(pygame.image.load("rock.png"), square)
wood_image_icon = pygame.transform.scale(pygame.image.load("wood.png"), icon)
stone_image_icon = pygame.transform.scale(pygame.image.load("stone.png"), icon)
iron_image_icon = pygame.transform.scale(pygame.image.load("iron.png"), icon)
wood_image_pickup = pygame.transform.scale(pygame.image.load("wood.png"), pickup_size)
stone_image_pickup = pygame.transform.scale(pygame.image.load("stone.png"), pickup_size)

resources = [wood_image_icon, stone_image_icon, iron_image_icon]
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
