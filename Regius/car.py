import json
import math
from tilemap import TileMap

class Car(object):
    waypoints = []
    enemies = []

    def __init__(self):
        self.name = "Regius"
        self.mytile = 0
        self.nexttile = 1

        self.tilemap = TileMap()

    def initmap(self, data):
        self.tilemap.initmap(data)