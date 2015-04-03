# -*- coding: utf-8 -*-
import math
import json
from vector import Vector
import heapq
from Regius.vector import Vector

class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.xy = (self.x, self.y)

    def __str__(self):
        return "(%s, %s)" % (self.x,self.y)

    def __repr__(self):
        return "(%s, %s)" % (self.x,self.y)

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
        self.op = []
        heapq.heapify(self.op)
        self.cl = set()
        self.cells = {}

        self.tile_width = data["map"]["tile_width"]
        self.tile_height = data["map"]["tile_height"]
        self.map_height = len(data["map"]["tiles"][0])
        self.map_width = len(data["map"]["tiles"])

        self.checkpoints = []
        for i in data["map"]["path"]:
            self.checkpoints.append((i["tile_x"],i["tile_y"]))
        self.closed = []
        self.m = data["map"]["tiles"]
        self.x = data["map"]["path"][0]["tile_x"]
        self.y = data["map"]["path"][0]["tile_y"]

        # Start is always first item in path
        self.start = self.checkpoints.pop(0)
        self.end = self.checkpoints.pop(0)
        self.tiles = ("-","|",",","`","/","\\","+")
        self.available = {"-": ["right","left"],
                          "|": ["down","up"],
                          "`": ["down", "left"],
                          ",": ["left","up"],
                          "\\": ["right","up"],
                          "+": ["left","up","down","right"],
                          "/": ["down","right"]}
        self.init_grid()

    def init_grid(self):
        for ny, y in enumerate(self.m):
            for nx, x in enumerate(y):
                if x in self.tiles:
                    reachable = True
                else:
                    reachable = False
                self.cells[(nx,ny)] = Cell(nx, ny, reachable)


    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))


    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        l = self.cells[(x, y)]
        return l


    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list
        """
        cells = []


        moves = {}
        x, y = cell.x, cell.y


        # Since a possible spot might be outside the map
        # so CATCH ALL THE THINGS!

        try:
            moves["left"] = self.get_cell(x-1,y)
        except:
            moves["left"] = None

        try:
            moves["right"] = self.get_cell(x+1,y)
        except:
            moves["right"] = None

        try:
            moves["up"] = self.get_cell(x,y-1)
        except: pass

        try:
            moves["down"] = self.get_cell(x,y+1)
        except: pass

        main = self.m[y][x]

        for i in self.available[main]:
            cells.append(moves[i])

        return cells

    def display_path(self):
        cell = self.end
        self.ll = []
        self.ll.append(self.end.xy)
        while cell.parent is not self.start:
            cell = cell.parent
            if not cell:
                break
            self.ll.append((cell.x, cell.y))
        self.ll.append(self.start.xy)
        self.ll = self.ll[::-1]
        return self.ll

    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self, start, end):
        self.cl = set()
        self.op = []
        # add starting cell to open heap queue
        self.start = self.get_cell(start[0], start[1])
        self.end = self.get_cell(end[0], end[1])
        heapq.heappush(self.op, (self.start.f, self.start))
        while len(self.op):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.op)
            # add cell to closed list so we don't process it twice
            self.cl.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.display_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for c in adj_cells:
                if c.reachable and c not in self.cl:
                    if (c.f, c) in self.op:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if c.g > cell.g + 10:
                            self.update_cell(c, cell)
                    else:
                        self.update_cell(c, cell)
                        # add adj cell to open list
                        heapq.heappush(self.op, (c.f, c))



    def tile_is_void(self,pos, tile):
        return self.pixelintile(pos, tile)


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
