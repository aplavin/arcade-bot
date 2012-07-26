from math import hypot

class vec:
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __repr__(self):
        return '{%f, %f}' % (self.x, self.y)

    def __len__(self):
        return 2

    def __nonzero__(self):
        return self.x != 0 and self.y != 0

    def __add__(self, other):
        return vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return vec(self.x * other, self.y * other)

    def __truediv__(self, other):
        return vec(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __neg__(self):
        return vec(-self.x, -self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def abs(self):
        return hypot(self.x, self.y)

    def abs2(self):
        return self.x * self.x + self.y * self.y

    def dist(self, other):
        return hypot(self.x - other.x, self.y - other.y)

    def dist2(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy