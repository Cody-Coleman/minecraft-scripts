#!/usr/bin/env python3
from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
from time import sleep
from threading import Thread
import subprocess
import sys


def matchVec3(vec1, vec2):
    if int(vec1.x) == int(vec2.x) and int(vec1.y) == int(vec2.y) and int(vec1.z) == int(vec2.z):
        return True
    else:
        return False


class RecordPlayer():
    def __init__(self, x, y, z):
        # Thread.__init__(self)
        self.running = True
        self.x = x
        self.y = y
        self.z = z
        self.running = True
        self.t1 = None
        self.proc = None
        # PERHAPS BUILD THE RECORD PLAYER IN THE INIT

    def on(self):
        self.running = True
        if self.proc is None:
            self.proc = subprocess.Popen(['pianobar'], stdout=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.Popen("echo ' ' > ~/.config/pianobar/ctl", shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
        self.t1 = Thread(target=self.lights)
        self.t1.setDaemon(True)
        self.t1.start()

    def lights(self):
        while self.running == True:
            # START UP PANDORA
            mc.setBlock(self.x + 2, self.y + 1, self.z + 2, block.NETHER_REACTOR_CORE.id, 1)
            mc.setBlock(self.x - 1, self.y + 1, self.z + 2, block.NETHER_REACTOR_CORE.id, 1)
            sleep(0.25)
            mc.setBlock(self.x + 2, self.y + 1, self.z + 2, block.NETHER_REACTOR_CORE.id, 2)
            mc.setBlock(self.x - 1, self.y + 1, self.z + 2, block.NETHER_REACTOR_CORE.id, 2)
            sleep(0.25)

    def off(self):
        self.running = False
        # STOP PANDORA
        print("Got stop command")
        if self.proc is not None:
            print("proc is not None")
            proc = subprocess.Popen("echo ' ' > ~/.config/pianobar/ctl", shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
        mc.setBlock(self.x + 2, self.y + 1, self.z + 2, block.NETHER_REACTOR_CORE.id, 2)
        mc.setBlock(self.x - 1, self.y + 1, self.z + 2, block.NETHER_REACTOR_CORE.id, 2)

    def next(self):
        # SKIP SONG
        if self.proc is not None:
            proc = subprocess.Popen("echo 'n' > ~/.config/pianobar/ctl", shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    def check_player(self, hit_list):
        for hit in hit_list:
            if matchVec3(hit.pos, Vec3(self.x, self.y + 1, self.z + 2)):
                block_data = mc.getBlockWithData(hit.pos)
                if block_data.id == 96 and block_data.data == 7:
                    mc.postToChat("stopping record player")
                    self.off()
                    break
                elif block_data.id == 96 and block_data.data == 3:
                    mc.postToChat("starting record player")
                    self.on()
                    break
            elif matchVec3(hit.pos, Vec3(self.x + 1, self.y, self.z + 2)):
                block_data = mc.getBlockWithData(hit.pos)
                if block_data.id == 47:
                    mc.postToChat("changing song")
                    self.next()
                    break

    def quit_player(self):
        print("Got quit command")
        proc = subprocess.Popen("echo 'q' > ~/.config/pianobar/ctl", shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)

#
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
