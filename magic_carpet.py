#! /usr/bin/env python3
import mcpi.minecraft as minecraft
import mcpi.block as block
import time

# function to round players float postion to integers and return a vector object
def roundVec3(vec3):
  return minecraft.Vec3(int(vec3.x), int(vec3.y), int(vec3.z))


if __name__ == "__main__":
  #time.sleep(2)

  # connect to minecraft
  mc = minecraft.Minecraft.create()

  # post a message to the player about the bridge
  mc.postToChat("Magic Carpet Activated")

  # get the player position
  last_player_pos = mc.player.getPos()
  block_list = []
  while True:
    
    # See if block was hit
    #block_hits = mc.events.pollBlockHits()
    #for block in block_hits:
    #    print("len of blocks: ", len(block_list))
    #    print("block: ", mc.getBlock(block.pos))
    #    if mc.getBlock(block.pos) == block.WOOL.id and len(block_list) > 0:
    #        print("Checking on the carpet")
    #        for block in block_list:
    #            print("Cleaning up Carpet")
    #            mc.setBlocks(block - minecraft.Vec3(1,0,1), block + minecraft.Vec3(1,0,1), block.AIR)


    # Get player position
    player_pos = mc.player.getPos()

    # Find the differences in the players positions
    movX = last_player_pos.x - player_pos.x
    movZ = last_player_pos.z - player_pos.z

    # check the players movement
    if ((movX < -0.2) or (movX > 0.2) or (movZ < -0.2) or (movZ > 0.2)):
        next_player_pos = player_pos
        #print(next_player_pos)
        # keep adding movement to player until next block is found
        while ((int(player_pos.x) == int(next_player_pos.x)) and  (int(player_pos.z) == int(next_player_pos.z))):
            # print("checking for movemnet")
            next_player_pos = minecraft.Vec3(next_player_pos.x - movX, next_player_pos.y, next_player_pos.z - movZ)
            # print("next_player_pos: ", next_player_pos)
            block_below = roundVec3(next_player_pos)
            if block_below.z < 0: 
                block_below.z = block_below.z - 1
            if block_below.x < 0:
                block_below.x = block_below.x -1
            block_below.y = block_below.y - 1
            # print("block_below coordinates", block_below)
            if mc.getBlock(block_below) == block.AIR.id:
                # print("block_below coordinates", block_below)
                # print("block is air")
                mc.setBlocks(block_below - minecraft.Vec3(1,0,1), block_below + minecraft.Vec3(1,0,2), 35, 10)
                block_list.append(block_below)
                # print("block_list: ", block_list)
                if len(block_list) > 2:
                    # print("to many blocks")
                    block_cleanup = block_list.pop(0)
                    mc.setBlocks(block_cleanup - minecraft.Vec3(1,0,1), block_cleanup + minecraft.Vec3(1,0,2), block.AIR)
            else:
                # print(mc.getBlock(block_below))
                block_hits = mc.events.pollBlockHits()
                # print("block hits: ", len(block_hits))
                for hit in block_hits:
                    # print("len of blocks: ", len(block_list))
                    # print("block: ", mc.getBlock(hit.pos))
                    if mc.getBlock(hit.pos) == block.WOOL.id and len(block_list) > 0:
                        # print("Checking on the carpet")
                        for carpet in block_list:
                            # print("Cleaning up Carpet")
                            mc.setBlocks(carpet - minecraft.Vec3(1,0,1), carpet + minecraft.Vec3(1,0,2), block.AIR)
                        time.sleep(2)
                        break
                # print(mc.getBlock(block_below))
            last_player_pos = player_pos

    
    time.sleep(0.01)
