1. "class CraftingSeq: # Doesn't handle end of crafting list yet?"
2. 'Grids' class to create and hold all grids created from MapArray?
3. Iterator class to give cords to CraftingSeqs?
4. Are the cords being loaded in a backwards way??
5. Expand character class?

Far fetched(?):
1. 3. 'Grid' class will hold all cords it's given, and render it's own image onto each cord (Instead of having a grid object for every single grid)

22-11-21
1. Turned Inventory class into a normal class, it couldn't work with the functionality of a descriptor.
2. Added MapArray class to create and hold map_arrays and seeds.

2022-11-06
1. Added inventory descriptor class, used within character.
2. Changed the class CraftingSquare class into CraftingSeq, which can now hold an entire crafting branch instead of singular items. (It can hold all axes at once, instead of making a new class for each)