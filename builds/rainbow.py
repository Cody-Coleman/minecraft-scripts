import math
import time
import mcpi.block as block

rainbow = [14, 1, 4, 13, 11, 10, 2]


def create_rainbow(mc, pos, radius=30):
    """
    Creates a rainbow in the sky, handy when trying to mark spots
    :param mc: Minecraft client
    :param pos: position to start at, +3 for x, and z so it's not on top of you
    :param radius: how round to make the rainbow
    """
    x = int(pos.x) + 3
    y = int(pos.y)
    z = int(pos.z) + 3

    for angle in range(360):
        for i in range(len(rainbow)):
            j = x + (radius - i) * math.cos(angle * math.pi / 180)
            k = y + (radius - i) * math.sin(angle * math.pi / 180)
            mc.setBlock(j, k, z, block.WOOL.id, rainbow[i])
            time.sleep(0.1)
