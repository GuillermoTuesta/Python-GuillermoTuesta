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