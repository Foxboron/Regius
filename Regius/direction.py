from Regius.vector import Vector

class DirectionManager(object):

    def __init__(self, position, direction, velocity, tilemap):
        self.position = position
        self.direction = direction
        self.velocity = velocity
        self.tilemap = tilemap


    def seek(self, target):
        target = target - self.position
        target = target.normalize()
        dir = self.direction.normalize()

        dir_angle = dir.angle()
        target_angle = target.angle()
        # print "Dir angle: " + str(dir_angle)
        # print "Target angle: " + str(target_angle)
        angle = target_angle - dir_angle
        return angle

    def seek_boost(self, targets):
        for target in targets:
            target = Vector(target["x"],target["y"])
            if target.distance(self.position) <= 200:
                target = target - self.position
                target = target.normalize()
                dir = self.direction.normalize()

                dir_angle = dir.angle()
                target_angle = target.angle()
                # print "Dir angle: " + str(dir_angle)
                # print "Target angle: " + str(target_angle)
                angle = target_angle - dir_angle
                if angle <= 70 and angle >=-70:
                    return angle * 9
                return 0
            return 0
        return 0

    def intersect(self, i, vec=None):
        o = Vector(i["x"],i["y"])
        return o.distance(self.ahead) <= i["width"]/2 \
            or o.distance(self.ahead2) <= i["width"]/2\
            or o.distance(self.ahead2) <= i["width"]/2

    def avoid(self, obs):
        MAX_SEE_AHEAD = 2
        self.ahead = (self.position + self.velocity) * MAX_SEE_AHEAD
        self.ahead2 = (self.position + self.velocity) * MAX_SEE_AHEAD * 0.5
        self.ahead3 = (self.position + self.velocity)
        avoidance = 0
        for i in obs:
            if self.intersect(i):
                avoidance = (self.ahead - Vector(i["x"],i["y"])).normalize()
                return (avoidance * 2).angle()
        return avoidance

    def avoid_void(self):
        MAX_SEE_AHEAD = 2
        self.ahead = (self.position + self.velocity) * MAX_SEE_AHEAD
        self.ahead2 = (self.position + self.velocity) * MAX_SEE_AHEAD * 0.5
        self.ahead3 = (self.position + self.velocity)
        avoidance = 0
        for i in self.tilemap.voids:
            if self.tilemap.tile_is_void(self.position, i) and self.intersect(i, vec=i):
                avoidance = (self.ahead - i).normalize()
                return (avoidance * 2).angle()
        return avoidance


