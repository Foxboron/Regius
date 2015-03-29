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
        self.available = {"-": ["right","left"],
                          "|": ["down","up"],
                          "`": ["down", "left"],
                          ",": ["left","up"],
                          "\\": ["right","up"],
                          "/": ["down","right"]}


        # for x in range(self.map_width):
        #     self.mapcost.append([])

        # for row in range(self.map_height):
        #     for column in range(self.map_width):
        #         self.mapcost[column].append(self.tilecost[data["map"]["tiles"][column][row]])
        self.init = True




    def pivot(self,m,pos):
        y = pos[1]
        x = pos[0]

        moves = {}


        # Since a possible spot might be outside the map
        # so CATCH ALL THE THINGS!

        try:
            moves["left"] = (x-1,y)
        except: pass

        try:
            moves["right"] = (x+1,y)
        except: pass

        try:
            moves["up"] = (x,y-1)
        except: pass

        try:
            moves["down"] = (x,y+1)
        except: pass

        main = m[y][x]
        if main in self.tiles:
            for i in self.available[main]:
                if moves[i] not in self.checkpoints:
                    return moves[i]



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
