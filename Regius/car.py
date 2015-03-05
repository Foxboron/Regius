import json
import math
from tilemap import TileMap
from collections import deque

class Car(object):
    waypoints = []
    enemies = []
    movements = {"up": 1<<0,
             "down": 1<<1,
             "left": 1<<2,
             "right": 1<<3,
             "space": 1<<4,
             "return": 1<<5}

    commandlist = deque()

    def __init__(self):
        self.name = "Regius"
        self.mytile = 0
        self.nexttile = 1

        self.tilemap = TileMap()

    def initmap(self, data):
        self.tilemap.initmap(data)

    def update(self, data):
        # update map and car info
        pass

    def getmove(self):
        output = 0

        if len(commandlist) > 0:
            output += commandlist.pop(0)

        return output