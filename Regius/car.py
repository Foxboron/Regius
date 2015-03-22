import json
import math
from tilemap import TileMap
from collections import deque
from vector import Vector


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
        # Testing
        self.nexttile = 3
        self.position = Vector(10, 10)
        self.direction = Vector(10, 10)
        self.velocity = Vector(10, 10)
        self.tilemap = TileMap()

    def initmap(self, data):
        self.tilemap.initmap(data)
        self.id = data["id"]

        for waypoint in data["map"]["path"]:
            vec = Vector(waypoint["tile_x"], waypoint["tile_y"])
            self.waypoints.append(vec)


    def update(self, data):
        # update map and car info
        if data:

            for car in range(len(data["cars"])):
                car = data["cars"][car]
                if car["id"] == self.id:
                    self.position = Vector(car["pos"]["x"], car["pos"]["y"])
                    self.velocity = Vector(car["velocity"]["x"], car["velocity"]["y"])
                    self.direction = Vector(car["direction"]["x"], car["direction"]["y"])

            print "Pos: "+str(self.position)
            print "Tile pos: "+str(self.tilemap.tilecenter(self.waypoints[self.nexttile]))

            self.turntowards(self.waypoints[self.nexttile])
            
            if self.tilemap.pixelintile(self.position, self.waypoints[self.nexttile]):
                print "Heyho"
                self.nexttile += 1
                self.mytile += 1

    def turntowards(self, tile):
        tilepos = self.tilemap.tilecenter(tile)
        distvector = self.position - tilepos
        normaldist = distvector.normalize()
        normaldir = self.direction.normalize()

        turnangle = self.direction.angle(tilepos)
        if turnangle >= 10 or turnangle <= -10:
            if turnangle < 0 :
                print "Left: "+str(turnangle)
                self.commandlist.append(self.movements["left"])
            else:
                print "Right: "+str(turnangle)
                self.commandlist.append(self.movements["right"])
        else:
            self.commandlist.append(self.movements["up"])

    def getmove(self):
        output = 0

        if len(self.commandlist) > 0:
            output += self.commandlist.pop()

        return output
