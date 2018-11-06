from mcpi.minecraft import Minecraft, Vec3
from time import sleep
from threading import Thread


class Sword:
    def __init__(self, address="localhost", port=4711):
        self.mc = Minecraft.create(address, port)
        self.enable = False
        # Sword Types: 0 == Normal, 10 == Lava, 8 == Water, 79 == ice,
        self.sword_type = 'normal'

    def enable_sword(self):
        self.enable = True
        self.mc.events.clearAll()

    def disable_sword(self):
        self.enable = False

    def set_sword_type(self, sword_type):
        self.sword_type = sword_type

    def check_sword(self, hit_list):
        if self.enable:
            if self.sword_type == 'air':
                self.check_air_sword(hit_list)
            else:
                for hit in hit_list:
                    hit_block_pos = hit.pos
                    if self.sword_type == 'normal':
                        pass
                    elif self.sword_type == 'lava':
                        self.mc.setBlock(hit_block_pos, 10)
                    elif self.sword_type == 'water':
                        self.mc.setBlock(hit_block_pos, 8)
                    elif self.sword_type == 'ice':
                        self.mc.setBlock(hit_block_pos, 79)

    def check_air_sword(self, hit_list):
        """
        Checks the hit_list to see if it matches a block that is not air, and has nothing above it. If so will
        spin up a new thread to start that block floating up in the float_block function
        :param hit_list: a mcpi list of block hit data
        """
        if self.enable:
            for hit in hit_list:
                hit_block_data = self.mc.getBlockWithData(hit.pos)
                hit_block_pos = hit.pos
                next_block_pos = Vec3(hit.pos.x, hit.pos.y + 1, hit.pos.z)
                next_block_data = self.mc.getBlockWithData(next_block_pos)
                if hit_block_data.id != 0 and next_block_data.id == 0:
                    # self.mc.postToChat("Block found floating now")
                    t1 = Thread(target=self.float_block,
                                args=(hit_block_pos, hit_block_data))
                    t1.setDaemon(True)
                    t1.start()
                    break

    def float_block(self, hit_block_pos, hit_block_data):
        """
        rotates between the hit block and the one above it, setting the one above to the same type as hit, the hit to air
        then assigning hit to that position, and next to one above that, looping 10 times
        :param hit_block_pos: The position of the hit block
        :param hit_block_data: The data of the hit block, used to set the air block above hit block to this
        :return:
        """
        # self.mc.postToChat("Block found floating now")
        for i in range(1, 10):
            next_block_pos = Vec3(hit_block_pos.x, hit_block_pos.y+1, hit_block_pos.z)
            # self.mc.postToChat("hit_block: {}\nnext_block: {}".format(hit_block_data.id, next_block_data.id))
            # Sets current block to Air
            self.mc.setBlock(hit_block_pos, 0)
            # Sets block above to the same type as the block that was hit
            self.mc.setBlock(next_block_pos, hit_block_data.id, 0)
            # sets the hit_block to the next_block position, and next block to one spot higher
            hit_block_pos = Vec3(next_block_pos.x, next_block_pos.y, next_block_pos.z)
            sleep(0.5)

    def __del__(self):
        """
        Disable the sword / clean up any threads
        :return:
        """
        self.disable_sword()
