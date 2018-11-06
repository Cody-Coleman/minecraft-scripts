#! /usr/bin/env python3
from mcpi.minecraft import Minecraft, Vec3
from threading import Thread
import mcpi.block as block
import time


class MagicCarpet:
    def __init__(self):
        """
        initilize the carpet
        """
        self.mc = Minecraft.create()
        self.mc.postToChat("Magic Carpet Activated")
        self.block_list = []
        self.last_player_pos = self.mc.player.getPos()
        self.player_pos = Vec3(0, 0, 0)
        self.running = True
        self.t1 = None

    def match(self):
        return int(self.last_player_pos.x) == int(self.player_pos.x) \
               and int(self.last_player_pos.y) == int(self.player_pos.y) \
               and int(self.last_player_pos.z) == int(self.player_pos.z)

    def get_block_below(self, next_player_pos):
        block_below = Vec3(int(next_player_pos.x), int(next_player_pos.y), int(next_player_pos.z))
        if block_below.z < 0:
            block_below.z -= 1
        if block_below.x < 0:
            block_below.x -= 1
        block_below.y -= 1
        return block_below

    def start_carpet(self):
        self.running = True
        self.t1 = Thread(target=self.flying_carpet)
        self.t1.setDaemon(True)
        self.t1.start()

    def check_carpet(self, hit_list):
        for hit in hit_list:
            if self.mc.getBlock(hit.pos) == block.WOOL.id and len(self.block_list) > 0:
                # print("Checking on the carpet")
                for carpet in self.block_list:
                    # print("Cleaning up Carpet")
                    self.mc.setBlocks(carpet - Vec3(1, 0, 1), carpet + Vec3(1, 0, 2), block.AIR)
                time.sleep(2)
                break

    def flying_carpet(self):
        """
        put a carpet under you
        :return:
        """
        while self.running:
            self.player_pos = self.mc.player.getPos()
            mov_x = self.last_player_pos.x - self.player_pos.x
            mov_z = self.last_player_pos.z - self.player_pos.z
            if mov_x < -0.2 or mov_x > 0.2 or mov_z < -0.2 or mov_z > 0.2:
                # DETECTED HORIZONTAL MOVEMENT
                next_player_pos = self.player_pos
                while self.match():
                    next_player_pos = Vec3(next_player_pos.x - mov_x,
                                           next_player_pos.y, next_player_pos.z - mov_z)
                    block_below = self.get_block_below(next_player_pos)
                    if self.mc.getBlock(block_below) == block.AIR.id:
                        self.mc.setBlocks(block_below - Vec3(1, 0, 1), block_below + Vec3(1, 0, 2), 35, 10)
                        self.block_list.append(block_below)
                        if len(self.block_list) > 2:
                            block_cleanup = self.block_list.pop(0)
                            self.mc.setBlocks(block_cleanup - Vec3(1, 0, 1), block_cleanup + Vec3(1, 0, 2), block.AIR)
                self.last_player_pos = self.player_pos
            time.sleep(0.2)

    def stop_carpet(self):
        """
        remove the carpet
        :return:
        """
        self.running = False
