# -*- coding: utf-8 -*-
import math
import json

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
        self.name = "map"

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

        print self.mapcost

        self.init = True



    def pixeltotile(self, pixel):
        return (math.floor(pixel[0]/self.tile_width), math.floor(pixel[1]/self.tile_height))

    def initialised(self):
        return self.init