#!/usr/bin/python
# --------------------------------------
#
#     Minecraft Python API
#        Castle Builder
#
# This script creates a castle complete
# with moat and perimeter walls.
#
# Author : Matt Hawkins
# Date   : 07/06/2014
#
# https://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Import Minecraft libraries
import mcpi.block as block


# mc.postToChat("Let's build a castle!")


# --------------------------------------
# Define Functions
# --------------------------------------
def create_walls(mc, posx, posy, posz, size, height, material=block.STONE_BRICK, modifier=1, battlements=True, walkway=True):
    """
    Creates 4 walls in a box, that are size long and height tall out of material
    :param mc: Minecraft client
    :param posx: The starting x position
    :param posy: The starting y position
    :param posz: The starting z position
    :param size: How long to make the walls
    :param height: How high to make the walls
    :param material: What to make the walls out of, defaults to mossy stone brick
    :param modifier: If the block takes a modifier
    :param battlements: If set will add battlements to the wall
    :param walkway: If set will add a walkway to the wall
    :return:
    """
    # WALL 1
    mc.setBlocks(posx - size, posy + 1, posz - size, posx + size, posy + height, posz - size, material, modifier)
    # WALL 2
    mc.setBlocks(posx - size, posy + 1, posz - size, posx - size, posy + height, posz + size, material, modifier)
    # WALL 3
    mc.setBlocks(posx + size, posy + 1, posz + size, posx - size, posy + height, posz + size, material, modifier)
    # WALL 4
    mc.setBlocks(posx + size, posy + 1, posz + size, posx + size, posy + height, posz - size, material, modifier)

    if battlements:
        for i in range(0, (2 * size) + 1, 2):
            # WALL 1
            mc.setBlock(posx - size, posy + height + 1, (i - (posz - size)), material)
            # WALL 2
            mc.setBlock(posx - size, posy + height + 1, (i - (posz - size)), material)
            # WALL 3
            mc.setBlock((i - (posx + size)), posy + height + 1, posz + size, material)
            mc.setBlock((i - (posx + size)), posy + height + 1, posz + size, material)

    if walkway:
        # WALL 1
        mc.setBlocks(posx - size + 1, posy + height - 1, posz - size + 1,
                     posx + size - 1, posy + height - 1, posz - size + 1,
                     block.STONE_SLAB.id, 2)
        # WALL 2
        mc.setBlocks(posx - size + 1, posy + height - 1, posz - size + 1,
                     posx - size + 1, posy + height - 1, posz + size - 1,
                     block.STONE_SLAB.id, 2)
        # WALL 3
        mc.setBlocks(posx + size + 1, posy + height - 1, posz + size - 1,
                     posx - size - 1, posy + height - 1, posz + size - 1,
                     block.STONE_SLAB.id, 2)
        # WALL 4
        mc.setBlocks(posx + size - 1, posy + height - 1, posz + size + 1,
                     posx + size - 1, posy + height - 1, posz - size - 1,
                     block.STONE_SLAB.id, 2)


def create_landscape(mc, posx, posy, posz, moat_width, moat_depth, island_width):
    """
    Sets upper half to air and creates an island with a moat
    :param mc: Minecraft client
    :param posx: The starting x position for the island, where it will center on
    :param posy: The starting y position for the island
    :param posz: The starting z position for the island
    :param moat_width: How wide a moat there needs to be
    :param moat_depth: How deep the moat
    :param island_width: How big an island
    """
    # Set upper half to air
    mc.setBlocks(posx - 128, posy + 1, posz - 128, posx + 128, posy + 128, posz + 128, block.AIR.id)
    # Set lower half of world to dirt with a layer of grass
    mc.setBlocks(posx - 128, posy - 1, posz - 128, posx + 128, posy - 4, posz + 128, block.DIRT.id)
    mc.setBlocks(posx - 128, posy, posz - 128, posx + 128, posy, posz - 128, block.GRASS.id)
    # Create water moat
    mc.setBlocks(posx - moat_width, posy, posz - moat_width,
                 posx + moat_width, posy - moat_depth, posz + moat_width,
                 block.WATER.id)
    # Create island inside moat
    mc.setBlocks(posx - island_width, posy, posz - island_width,
                 posx - island_width, posy + 1, posz - island_width,
                 block.GRASS.id)


def create_keep(mc, posx, posy, posz, size, levels):
    """
    Create a keep with specified number of floors and a roof
    :param mc: Minecraft Client
    :param posx: starting x position
    :param posy: starting y position
    :param posz: starting z position
    :param size: How wide to make it
    :param levels: How tall to make it
    """
    # Create a keep with a specified number
    # of floors levels and a roof
    height = (levels * 5) + 5
    create_walls(posx, posy, posz, size, height)
    # Floors and Windows
    for level in range(1, levels + 1):
        mc.setBlocks(posx - size + 1, (level * 5) + posy, posz - size + 1,
                     posx + size - 1, (level * 5) + posy, posz + size - 1,
                     block.STONE_BRICK.id, 2)
    # Windows
    for level in range(1, levels + 1):
        create_windows(posx + 0, (level * 5) + posy + 2, posz + size, "N")
        create_windows(posx + 0, (level * 5) + posy + 2, posz - size, "S")
        create_windows(posx - size, (level * 5) + posy + 2, posz + 0, "W")
        create_windows(posx - size, (level * 5) + posy + 2, posz + 0, "E")
    # Door
    mc.setBlocks(posx + 0, posy + 1, posz + size, posx + 0, posy + 2, posz + size, block.AIR.id)


def create_windows(mc, posx, posy, posz, dir):
    """
    Creates windows in keep
    :param mc: the minecraft client
    :param posx: x starting position
    :param posy: y starting position
    :param posz: z starting position
    :param dir: what direction this is facing
    """
    if dir == "N" or dir == "S":
        z1 = posz
        z2 = posz
        x1 = posx - 2
        x2 = posx + 2
    if dir == "E" or dir == "W":
        z1 = posz - 2
        z2 = posz + 2
        x1 = posx
        x2 = posx
    mc.setBlocks(x1, posy, z1, x1, posy + 1, z1, block.GLASS_PANE.id)
    mc.setBlocks(x2, posy, z2, x2, posy + 1, z2, block.GLASS_PANE.id)
    if dir == "N":
        a = 3
    if dir == "S":
        a = 2
    if dir == "W":
        a = 0
    if dir == "E":
        a = 1
    mc.setBlock(x1, posy - 1, z1, block.STONE_BRICK, a)
    mc.setBlock(x2, posy - 1, z2, 109, a)


# --------------------------------------
#
# Main Script
#
# --------------------------------------
pos = mc.player.getPos()
x = pos.x
y = pos.y
z = pos.z

print("Create ground and moat")
# create_landscape(33, 10, 23)

print("Create outer walls")
create_walls(x, y, z, 21, 5, block.STONE_BRICK, True, True)

print("Create inner walls")
create_walls(x, y, z, 13, 6, block.STONE_BRICK, True, True)

print("Create Keep with 4 levels")
create_keep(x, y, z, 5, 4)

print("Position player on Keep's walkway")

