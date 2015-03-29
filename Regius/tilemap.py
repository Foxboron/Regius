# -*- coding: utf-8 -*-
import math
import json
from vector import Vector

class TileMap(object):
    init = False
    tilecost = {
        '*': 20,
        '-': 10,
        '|': 10,
        ',': 10,
        "`": 10,
        '/': 10,
        '\\': 10,
        '.': 20,
        "mud": 30,
        "booster": 0,
        "ice": 20
    }

    def __init__(self):
        pass

    def initmap(self, data):
        self.tile_width = data["map"]["tile_width"]
        self.tile_height = data["map"]["tile_height"]
        self.map_height = len(data["map"]["tiles"][0])
        self.map_width = len(data["map"]["tiles"])

        self.checkpoints = []
        self.m = data["map"]["tiles"]
        self.x = data["map"]["path"][0]["tile_x"]
        self.y = data["map"]["path"][0]["tile_y"]
        self.tiles = ("-","|",",","`","/","\\",)


        # for x in range(self.map_width):
        #     self.mapcost.append([])

        # for row in range(self.map_height):
        #     for column in range(self.map_width):
        #         self.mapcost[column].append(self.tilecost[data["map"]["tiles"][column][row]])


        self.init = True


    def pivot(self,m,pos):
        y = pos[1]
        x = pos[0]

        print pos

        main = m[y][x]

        right = m[y][x+1]
        down = m[y+1][x]
        left = m[y][x-1]
        up = m[y-1][x]

        if right in self.tiles and (x+1,y) not in self.checkpoints:
            return (x+1,y)

        elif down in self.tiles and (x,y+1) not in self.checkpoints:
            return (x,y+1)

        elif left in self.tiles and (x-1,y) not in self.checkpoints:
            return (x-1,y)

        elif up in self.tiles and (x,y-1) not in self.checkpoints:
            return (x,y-1)
        else:
            return None

    def path_finding(self):
        y,x = self.y, self.x
        self.checkpoints.append((x,y))
        while True:
            pos = self.pivot(self.m,(x,y))
            if pos:
                self.checkpoints.append(pos)
                x,y = pos[0],pos[1]
            else:
                 break
        self.checkpoints.append((x,y))
        return self.checkpoints


    def pixeltotile(self, pixel):
        return Vector(int(math.floor(pixel.x/self.tile_width)), int(math.floor(pixel.y/self.tile_height)))

    def pixelintile(self, pixel, tile):
        return self.pixeltotile(pixel) == tile

    def tilecenter(self, tile):
        return Vector(tile.x*self.tile_width+(self.tile_width/2), tile.y*self.tile_height+(self.tile_height/2))

    def pixel_to_pos(self,pixel):
        return self.tilecenter(self.pixeltotile(pixel))

    def initialised(self):
        return self.init
