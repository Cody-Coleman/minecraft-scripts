import sys
import random
import time
from detectors.hit_detector import HitDetector
from swords.swords import Sword


def type_output(sentence, speed=80):
    for letter in sentence:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / (speed + 10))
    print("\n")


if __name__ == '__main__':
    sword = Sword()
    hd = HitDetector()
    hd.add_check(sword.check_sword)
    sword_selection = {'1': 'normal', '2': 'lava', '3': 'water', '4': 'ice', '5': 'air'}
    sword.enable_sword()
    hd.check_on()
    while True:
        print("\033c")
        type_output("Welcome to the Minecraft Sword Arsenal selection screen")
        type_output("Select your sword type from below")
        type_output("1.) Normal Sword -> No special effects")
        type_output("2.) Lava Sword -> Change blocks to flowing Lava")
        type_output("3.) Water Sword -> Change blocks into flowing water")
        type_output("4.) Ice Sword -> Change blocks into Ice")
        type_output("5.) Air Sword -> Float Blocks")
        sword_input = input("Select your Sword [1-5]: ")
        if sword_input not in sword_selection:
            pass
        else:
            type_output("You've selected {} sword type".format(sword_selection[sword_input]))
            sword.set_sword_type(sword_selection[sword_input])


# sword = air_sword()
# sword.enable_sword()
# hd = hitDetector()
# hd.add_check(sword.check_air_sword)
# hd.check_on()


# # GET INITIAL POSITIONS AND CONNECTIONS
# mc = Minecraft.create()
# pos = mc.player.getPos()
# x, y, z = int(pos.x), int(pos.y), int(pos.z)
#
# # CREATE RECORD PLAYER
# mc.setBlock(x, y, z + 2, block.CRAFTING_TABLE.id)
# mc.setBlock(x, y + 1, z + 2, 96, 7)
# # REMEMBER THE LIDS LOCATION
# lid = Vec3(x, y + 1, z + 2)
#
# mc.setBlock(x - 1, y, z + 2, 49)
# mc.setBlock(x - 1, y + 1, z + 2, block.NETHER_REACTOR_CORE.id, 2)
# mc.setBlock(x + 1, y, z + 2, 47)
# mc.setBlock(x + 2, y, z + 2, 49)
# mc.setBlock(x + 2, y + 1, z + 2, block.NETHER_REACTOR_CORE.id, 2)
# mc.setBlock(x - 1, y + 2, z + 2, block.OBSIDIAN.id)
# mc.setBlock(x + 2, y + 2, z + 2, block.OBSIDIAN.id)
#
# record = recordPlayer(x, y, z)
# hd = hitDetector()
# hd.add_check(record.check_player)
# hd.check_on()
#
# while True:
#     try:
#         sleep(1)
#     except KeyboardInterrupt:
#         record.quit_player()
#         sys.exit()
