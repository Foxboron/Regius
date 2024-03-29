import json
import math
from tilemap import TileMap
from collections import deque
from vector import Vector
from direction import DirectionManager


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
        self.nexttile = 1
        self.position = Vector(10, 10)
        self.direction = Vector(10, 10)
        self.velocity = Vector(10, 10)
        self.test_velocity = Vector(10, 10)
        self.tilemap = TileMap()

        self.obstacles = []
        self.boosters = []

    def initmap(self, data):
        self.tilemap.initmap(data)
        self.id = data["id"]

        self.m = data["map"]["path"]

        checkpoints = self.init_checkpoints()
        for x,y in checkpoints:
            vec = Vector(x,y)
            self.waypoints.append(self.tilemap.tilecenter(vec))

        # Save for backup
        # self.waypoints = []
        # for waypoint in data["map"]["path"]:
        #     vec = Vector(waypoint["tile_x"], waypoint["tile_y"])
        #     self.waypoints.append(self.tilemap.tilecenter(vec))

        for mod in data["map"]["modifiers"]:
            if mod["type"] in ("mud","ice"):
                self.obstacles.append(mod)
        for mod in data["map"]["modifiers"]:
            if mod["type"] in ("booster"):
                self.boosters.append(mod)


    def init_checkpoints(self):
        points = [(i["tile_x"],i["tile_y"]) for i in self.m]
        checkpoints = []
        #self.tilemap.actual_start = points[0]
        start = points.pop(0)
        end = points.pop(0)
        while True:
            for i in self.tilemap.process(start, end):
                if i not in checkpoints:
                    checkpoints.append(i)
            try:
                start = end
                end = points.pop(0)
            except: break
            print checkpoints
        return checkpoints


    def get_close_tile(self):
        target = self.waypoints[self.nexttile]
        # print round(self.position.distance(target))
        if(round(self.position.distance(target)) <= 110):
            self.nexttile += 1
        if(self.nexttile == len(self.waypoints)-1):
            self.nexttile = 0
        return self.waypoints[self.nexttile]

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
            # print "Pos: " + str(self.position)
            # print "Direction: "+str(self.direction)
            # print "Velocity: "+str(self.velocity)
            # print "Tile pos: "+str(tile_pos)

            self.dm = DirectionManager(self.position, self.direction, self.velocity,self.tilemap)

            self.move(tile_pos)


    def move(self, tilepos):
        #tilepos = Vector(800, 167)
        # We first find the dir we want to walk towards
        angle = self.dm.seek(tilepos)
        # Then e mofidy the angle with objects to avoid
        angle += self.dm.avoid(self.obstacles)
        angle += self.dm.seek_boost(self.boosters)
        threshold = 10

        if ((angle > threshold and angle < 180-threshold) or angle < -180 - threshold):
            # print "Left: "+str(angle)
            self.commandlist.append(self.movements["left"])
        elif ((angle < 0 - threshold and angle > -180 + threshold) or angle > 180 + threshold):
            # print "Right: "+str(angle)
            self.commandlist.append(self.movements["right"])
        elif(angle >= 0 - threshold and angle <= threshold):
            # print "Up: "+str(angle)
            self.commandlist.append(self.movements["up"])
        else:
            self.commandlist.append(self.movements["right"])
            # print "Nothing: "+str(angle)
            # self.commandlist.append(self.movements["up"])

    def getmove(self):
        output = 1<<0

        if len(self.commandlist) > 0:
            output |= self.commandlist.pop()

        return output
