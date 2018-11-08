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
from time import sleep

# mc.postToChat("Let's build a castle!")


# --------------------------------------
# Define Functions
# --------------------------------------
def create_walls(mc, posx, posy, posz, size, height, material=block.STONE_BRICK.id, modifier=1, battlements=True,
                 walkway=True):
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
    mc.postToChat("Creating Walls")
    # WALL 1
    mc.setBlocks(posx - size, posy + 1, posz - size, posx + size, posy + height, posz - size, material, modifier)
    # WALL 2
    mc.setBlocks(posx - size, posy + 1, posz - size, posx - size, posy + height, posz + size, material, modifier)
    # WALL 3
    mc.setBlocks(posx + size, posy + 1, posz + size, posx - size, posy + height, posz + size, material, modifier)
    # WALL 4
    mc.setBlocks(posx + size, posy + 1, posz + size, posx + size, posy + height, posz - size, material, modifier)
    sleep(5)

    if battlements:
        mc.postToChat("Creating battlements")
        for i in range(0, (2 * size) + 1, 2):
            # WALL 1
            mc.setBlock(((posx - size) + i), posy + height + 1, posz - size, material, modifier)
            mc.setBlock(((posx - size) + i), posy + height + 2, posz - size, block.TORCH.id, 5)
            # WALL 2
            mc.setBlock(posx - size, posy + height + 1, ((posz - size) + i), material, modifier)
            mc.setBlock(posx - size, posy + height + 2, ((posz - size) + i), block.TORCH.id, 5)

            # WALL 3
            mc.setBlock(((posx - size) + i), posy + height + 1, posz + size, material, modifier)
            mc.setBlock(((posx - size) + i), posy + height + 2, posz + size, block.TORCH.id, 5)

            # WALL 4
            mc.setBlock(posx + size, posy + height + 1, ((posz - size) + i), material, modifier)
            mc.setBlock(posx + size, posy + height + 2, ((posz - size) + i), block.TORCH.id, 5)

    if walkway:
        mc.postToChat("Creating Walkways")
        # WALL 1
        mc.setBlocks(posx - size + 1, posy + height - 1, posz - size + 1,
                     posx + size - 1, posy + height - 1, posz - size + 1,
                     block.STONE_SLAB.id, 2)
        # WALL 2
        mc.setBlocks(posx - size + 1, posy + height - 1, posz - size + 1,
                     posx - size + 1, posy + height - 1, posz + size - 1,
                     block.STONE_SLAB.id, 2)
        # WALL 3
        mc.setBlocks(posx + size - 1, posy + height - 1, posz + size - 1,
                     posx - size + 1, posy + height - 1, posz + size - 1,
                     block.STONE_SLAB.id, 2)
        # WALL 4
        mc.setBlocks(posx + size - 1, posy + height - 1, posz - size + 1,
                     posx + size - 1, posy + height - 1, posz + size - 1,
                     block.STONE_SLAB.id, 2)


def create_landscape(mc, posx, posy, posz, size, moat_depth=3):
    """
    Sets upper half to air and creates an island with a moat floating in the air
    :param mc: Minecraft client
    :param size: the initial size of everything, the island and moat are multiples of this
    :param posx: The starting x position for the island, where it will center on
    :param posy: The starting y position for the island
    :param posz: The starting z position for the island
    :param moat_depth: How deep the moat
    """
    island_size = size * 2
    moat_size = (size * 2) + 3

    # Set upper half to air
    mc.postToChat("setting upper half to air")
    mc.setBlocks(posx - moat_size, posy-4, posz - moat_size,
                 posx + moat_size, posy + 25, posz + moat_size, block.AIR.id)
    sleep(10)

    # Create water moat
    mc.postToChat("Setting up moat")
    mc.setBlocks(posx - moat_size, posy, posz - moat_size,
                 posx + moat_size, posy - moat_depth, posz + moat_size,
                 block.WATER.id)

    sleep(5)

    # Set lower half of world to dirt with a layer of grass
    mc.postToChat("Creating Land")
    mc.setBlocks(posx - island_size, posy, posz - island_size,
                 posx + island_size, posy - 4, posz + island_size, block.DIRT.id)

    # create island
    mc.postToChat("Creating Grass")
    mc.setBlocks(posx - island_size, posy, posz - island_size,
                 posx + island_size, posy, posz + island_size, block.GRASS.id)



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
    levels += 1
    mc.postToChat("Creating Keep")
    height = (levels * 5) + 5
    create_walls(mc, posx, posy-6, posz, size, height)
    # Floors and Windows
    for level in range(1, levels + 1):
        mc.setBlocks(posx - size + 1, (level * 5) + posy, posz - size + 1,
                     posx + size - 1, (level * 5) + posy, posz + size - 1,
                     block.STONE_BRICK.id, 2)
    # Windows
    for level in range(1, levels + 1):
        # WALL 3
        create_windows(mc, posx, (level * 5) + posy + 2, posz + size, "N")
        # WALL 1
        create_windows(mc, posx, (level * 5) + posy + 2, posz - size, "S")
        # WALL
        create_windows(mc, posx - size, (level * 5) + posy + 2, posz, "W")
        create_windows(mc, posx + size, (level * 5) + posy + 2, posz, "E")
    # Door
    mc.setBlocks(posx - 1, posy + 1, posz - size, posx + 1, posy + 2, posz - size, block.AIR.id)


def create_windows(mc, posx, posy, posz, direction):
    """
    Creates windows in keep
    :param mc: the minecraft client
    :param posx: x starting position
    :param posy: y starting position
    :param posz: z starting position
    :param direction: what direction this is facing
    """
    if direction == "N" or direction == "S":
        z1 = posz
        z2 = posz
        z3 = posz
        x1 = posx - 3
        x2 = posx + 3
        x3 = posx
    if direction == "E" or direction == "W":
        z1 = posz - 3
        z2 = posz + 3
        z3 = posz
        x1 = posx
        x2 = posx
        x3 = posx
    mc.setBlocks(x1, posy, z1, x1, posy + 1, z1, block.GLASS_PANE.id)
    mc.setBlocks(x2, posy, z2, x2, posy + 1, z2, block.GLASS_PANE.id)
    mc.setBlocks(x3, posy, z3, x3, posy + 1, z3, block.GLASS_PANE.id)
    if direction == "N":
        a = 3
    if direction == "S":
        a = 2
    if direction == "W":
        a = 0
    if direction == "E":
        a = 1
    mc.setBlock(x1, posy - 1, z1, 109, a)
    mc.setBlock(x2, posy - 1, z2, 109, a)
    mc.setBlock(x3, posy - 1, z3, 109, a)


def create_castle(mc, posx, posy, posz, size=10):
    """
    Creates the castle in the sky, uses the initial positions and size to determine all other values
    :param mc: minecraft client
    :param size: How big the keep is, affects the island, walls and moat as a result
    :param posx: where the x center should start
    :param posy: where the y should start, castle then moves up 10 spaces
    :param posz: where the z center should start
    """
    # first create landscape
    posy = posy+10
    mc.postToChat("Creating Landscape")
    create_landscape(mc, posx, posy, posz, size)
    # next create walls
    mc.postToChat("Creating border walls")
    create_walls(mc, posx, posy, posz, size*2, 5)
    mc.postToChat("Creating Keep")
    create_keep(mc, posx, posy, posz, size, 5)

# --------------------------------------
#
# Main Script
#
# --------------------------------------
# pos = mc.player.getPos()
# x = pos.x
# y = pos.y
# z = pos.z
#
# print("Create ground and moat")
# # create_landscape(33, 10, 23)
#
# print("Create outer walls")
# create_walls(x, y, z, 21, 5, block.STONE_BRICK, True, True)
#
# print("Create inner walls")
# create_walls(x, y, z, 13, 6, block.STONE_BRICK, True, True)
#
# print("Create Keep with 4 levels")
# create_keep(x, y, z, 5, 4)
#
# print("Position player on Keep's walkway")
