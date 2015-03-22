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

        self.mapcost = []

        for x in range(self.map_width):
            self.mapcost.append([])

        for row in range(self.map_height):
            for column in range(self.map_width):
                self.mapcost[column].append(self.tilecost[data["map"]["tiles"][column][row]])

        self.init = True


    def current_tile(self, pos):
        pass



    def pixeltotile(self, pixel):
        return Vector(int(math.floor(pixel.x/self.tile_width)), int(math.floor(pixel.y/self.tile_height)))

    def pixelintile(self, pixel, tile):
        return self.pixeltotile(pixel) == tile

    def tilecenter(self, tile):
        return Vector(tile.x*self.tile_width-(self.tile_width/2), tile.y*self.tile_height-(self.tile_height/2))

    def initialised(self):
        return self.init
