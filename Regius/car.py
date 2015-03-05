import json
import math
from Regius.map import TileMap

class Car(object):
    waypoints = []
    enemies = []

    def __init__(self):
        self.name = "Regius"
        self.mytile = 0
        self.nexttile = 1

        self.tilemap = TileMap()
