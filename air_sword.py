/env python3
from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
from time import sleep
from threading import Thread

class hitDetector():
    def __init__(self):
        self.check_list = []
        self.running = True
        self.t1 = None
        self.mc = Minecraft.create()
    def check_on(self):
        self.running = True
        self.t1 = Thread(target = self.check_hits)
        self.t1.setDaemon(True)
        self.t1.start()
    def check_hits(self):
        while self.running == True:
            sleep(0.5)
            hits = self.mc.events.pollBlockHits()
            for func in self.check_list:
                func(hits)
    def check_off(self):
        self.running = False
    def add_check(self, func):
        self.check_list.append(func)

class air_sword():
    def __init__(self):
        """ Sword Classifier """
        self.enable = False
        self.mc = Minecraft.create()
    def enable_sword(self):
        self.enable = True
        self.mc.events.clearAll()
    def disable_sword(self):
        self.disable = False
    def check_air_sword(self, hit_list):
        if self.enable:
            for hit in hit_list:
                self.mc.postToChat("HIT CHECKER")
                hit_block_data = self.mc.getBlockWithData(hit.pos)
                hit_block_pos = hit.pos
                next_block_pos = Vec3(hit.pos.x, hit.pos.y+1, hit.pos.z)
                next_block_data = self.mc.getBlockWithData(next_block_pos)
                if hit_block_data.id != 0 and next_block_data.id == 0:
                    self.mc.postToChat("Block found floating now")
                    t1 = Thread(target=self.float_block, args=(hit_block_pos, hit_block_data, next_block_pos, next_block_data))
                    t1.setDaemon(True)
                    t1.start()
                    # for i in range(1, 10):
                    #     # self.mc.postToChat("hit_block: {}\nnext_block: {}".format(hit_block_data.id, next_block_data.id))
                    #     self.mc.setBlock(hit_block_pos, 0)
                    #     self.mc.setBlock(next_block_pos, hit_block_data.id, 0)
                    #     hit_block_pos = Vec3(next_block_pos.x, next_block_pos.y, next_block_pos.z)
                    #     next_block_pos = Vec3(next_block_pos.x, next_block_pos.y+1, next_block_pos.z)
                    #     sleep(0.5)
                    break
    def float_block(self, hit_block_pos, hit_block_data, next_block_pos, next_block_data):
        self.mc.postToChat("Block found floating now")
        for i in range(1, 10):
            # self.mc.postToChat("hit_block: {}\nnext_block: {}".format(hit_block_data.id, next_block_data.id))
            self.mc.setBlock(hit_block_pos, 0)
            self.mc.setBlock(next_block_pos, hit_block_data.id, 0)
            hit_block_pos = Vec3(next_block_pos.x, next_block_pos.y, next_block_pos.z)
            next_block_pos = Vec3(next_block_pos.x, next_block_pos.y+1, next_block_pos.z)
            sleep(0.5)


sword = air_sword()
sword.enable_sword()
hd = hitDetector()
hd.add_check(sword.check_air_sword)
hd.check_on()



