import math

class Vector(object):

    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        ret = self.copy()
        ret.x += other.x
        ret.y += other.y
        return ret

    def __repr__(self):
        return '%s(%s, %s)' % ("Vector", self.x, self.y)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def __div__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        return Vector(self.x / other, self.y / other)

    def __isub__(self, other):
        ret = self.copy()
        ret.x -= other.x
        ret.y -= other.y
        return ret

    def __mul__(self, factor):
        if isinstance(factor, Vector):
            return Vector(self.x * factor.x, self.y * factor.y)
        return Vector(self.x * factor, self.y * factor)

    def __imul__(self, factor):
        ret = self.copy()
        ret.x *= factor
        ret.y *= factor
        return ret

    def __idiv__(self, dividend):
        ret = self.copy()
        ret.x /= dividend
        ret.y /= dividend

        return ret

    def __iter__(self):
        for v in (self.x, self.y):
            yield v

    def __eq__(self,comp):
        return self.x == comp.x and self.y == comp.y

    def copy(self):
        return Vector(self.x, self.y)

    def vectorlen(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def normalize(self):
        veclen = self.vectorlen()
        if veclen == 0:
            return Vector(0.0, 0.0)
        return Vector(self.x / veclen, self.y / veclen)

    '''def normalize(self):
        ret = self.copy()
        veclen = ret.vectorlen()
        ret /= veclen
        self = ret
        return self'''

    def distance(self, other):
        return math.sqrt(((self.x - other.x) * (self.x - other.x)) + ((self.y - other.y) * (self.y - other.y)))

    def angle(self):
        kartAngle = (math.atan2(-self.y, self.x) * 180/math.pi) + 180

        return kartAngle
