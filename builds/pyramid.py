import math
from mcpi import block


def create_pyramid(mc, posx, posy, posz, width, base=block.COBBLESTONE.id, walls=block.SANDSTONE.id,
                   top_block=block.GOLD_BLOCK.id):
    """
    Creates a pyramid at the posx, posy and posz coordinates with a width and height
    :param mc: Minecraft Client
    :param posx: The starting X coordinate
    :param posy: The starting Y coordinate
    :param posz: The starting Z coordinate
    :param width: How wide the base of the pyramid is
    :param base: what type of block the base of the pyramid is
    :param walls: what type of block the walls of the pyramid is
    :param top_block: what type of block goes on the very top of the pyramid
    """
    mc.postToChat("About to create pyramid!")
    # May sure width is odd number so pyramid ends
    # with a single block
    if width % 2 == 0:
        width = width + 1
    height = int((width + 1) / 2)
    half_size = int(math.floor(width / 2))
    mc.postToChat(f"Player : {posx} {posy} {posz}")
    mc.postToChat(f"Size : {width} Height : {height} Halfsize : {half_size}")
    # Create base for pyramid
    print("Create solid base")
    mc.setBlocks(posx - half_size - 2, posy - 2, posz - half_size - 2,
                 posx + half_size + 2, posy - 2, posz + half_size + 2,
                 block.DIRT.id)
    mc.setBlocks(posx - half_size - 2, posy - 1, posz - half_size - 2,
                 posx + half_size + 2, posy - 1, posz + half_size + 2,
                 base)
    # Create solid Pyramid
    print("Create Pyramid")
    for i in range(posy, posy + height):
        mc.setBlocks(posx - half_size, i, posz - half_size,
                     posx + half_size, i, posz + half_size,
                     walls)
        half_size = half_size - 1
    # Change top block
    print("Set top block")
    mc.setBlock(posx, posy + height - 1, posz, top_block)
