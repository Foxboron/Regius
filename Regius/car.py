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
        self.nexttile = 2
        self.position = Vector(10, 10)
        self.direction = Vector(10, 10)
        self.velocity = Vector(10, 10)
        self.test_velocity = Vector(10, 10)
        self.tilemap = TileMap()

    def initmap(self, data):
        self.tilemap.initmap(data)
        self.id = data["id"]

        for waypoint in data["map"]["path"]:
            vec = Vector(waypoint["tile_x"], waypoint["tile_y"])
            self.waypoints.append(self.tilemap.tilecenter(vec))


    def get_close_tile(self):
        target = self.waypoints[self.nexttile]
        print round(self.position.distance(target))
        if(round(self.position.distance(target)) <= 10):
            self.nexttile += 1
        if(self.nexttile == len(self.waypoints)-1):
            self.nexttile = 0
        return self.waypoints[self.nexttile]

    def seek(self, tar):
        new = Vector(0,0)
        desired = tar-self.position
#        desired = desired.normalize()
        return desired


    def update(self, data):
        # update map and car info
        if data:
            for car in range(len(data["cars"])):
                car = data["cars"][car]
                if car["id"] == self.id:
                    self.position = Vector(car["pos"]["x"], car["pos"]["y"])
                    self.velocity = Vector(car["velocity"]["x"], car["velocity"]["y"])
                    self.direction = Vector(car["direction"]["x"], car["direction"]["y"])

            tile_pos = self.get_close_tile()
            print "Pos: " + str(self.position)
            print "Direction: "+str(self.direction)
            print "Velocity: "+str(self.velocity)
            print "Tile pos: "+str(tile_pos)

            self.move(tile_pos)


    def move(self, tilepos):
#        tilepos = Vector(655,110)

        tile = tilepos.normalize()
        dist = self.position - tilepos
        dist = dist.normalize()
        dir = self.direction.normalize()
        self.position = self.position + self.velocity

        angle = self.position.angle(tilepos.normalize())
        threshold = 2
        if ((angle > threshold and angle < 180-threshold) or angle < -180 - threshold):
            print "Right: "+str(angle)
            self.commandlist.append(self.movements["right"])
        elif ((angle < 0 - threshold and angle > -180 + threshold) or angle > 180 + threshold):
            print "Left: "+str(angle)
            self.commandlist.append(self.movements["left"])
        elif (angle >= 0 - threshold and angle <= threshold):
            print "Up: "+str(angle)
            self.commandlist.append(self.movements["up"])
        else:
            print "Nothing: "+str(angle)
            #self.commandlist.append(self.movements["up"])

    def getmove(self):
        output = 1<<0

        if len(self.commandlist) > 0:
            output |= self.commandlist.pop()

        return output
