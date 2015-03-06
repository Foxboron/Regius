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
        self.position = (0, 0)
        self.direction = (0, 0)
        self.velocity = (0, 0)
        self.tilemap = TileMap()

    def initmap(self, data):
        self.tilemap.initmap(data)
        self.id = data["id"]

        for waypoint in data["map"]["path"]:
            self.waypoints.append((waypoint["tile_x"], waypoint["tile_y"]))

        print self.waypoints

    def update(self, data):
        # update map and car info
        if data == None:
            return

        for car in range(len(data["cars"])):
            car = data["cars"][car]
            if car["id"] == self.id:
                self.position = (car["pos"]["x"], car["pos"]["y"])
                self.velocity = (car["velocity"]["x"], car["velocity"]["y"])
                self.direction = (car["direction"]["x"], car["direction"]["y"])

        self.turntowards(self.waypoints[self.nexttile])

    def turntowards(self, tile):
        tilepos = self.tilemap.tilecenter(tile)
        distvector = self.distance(self.position, tilepos)
        normaldist = self.normalized(distvector)
        normaldir = self.normalized(self.direction)

        turnangle = self.angle(normaldist, normaldir)
        if math.fabs(turnangle) > 20:
            if turnangle < 0:
                self.commandlist.append(self.movements["left"])
            else:
                self.commandlist.append(self.movements["right"])

    def dotproduct(self, vec1, vec2):
        return sum([vec1[i]*vec2[i] for i in range(len(vec1))])

    def distance(self, pos1, pos2):
        return (pos2[0] - pos1[0], pos2[1] - pos1[1])

    def vectorlen(self, vector):
        return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

    def normalized(self, vector):
        veclen = self.vectorlen(vector)
        return (vector[0] / veclen, vector[1] / veclen)

    def multiply(self, vector, factor):
        return (vector[0] * factor, vector[1] * factor)

    def angle(self, vec1, vec2):
        angle = math.atan2(vec2[1], vec2[0]) - math.atan2(vec1[1], vec1[0])
        return math.degrees(angle)

    def getmove(self):
        output = 1 << 0

        if len(self.commandlist) > 0:
            output += self.commandlist.popleft()

        return output