"""Classes to define world objects"""

import random
import math
import color_utils

def add_vec(pos, vec, dt):
    """add a vector to a position"""
    px, py, pz = pos
    dx, dy, dz = vec
    px += dx * dt
    py += dy * dt
    pz += dz * dt
    p = (px, py, pz)
    return p


def sub_vec(v1, v2, dt=1):
    x1, y1, z1 = v1
    x2, y2, z2 = v2

    x = x1 - x2 * dt
    y = y1 - y2 * dt
    z = z1 - z2 * dt
    v = (x, y, z)
    return v


def scale_vec(v, n):
    x, y, z = v
    x *= n
    y *= n
    z *= n
    v = (x, y, z)
    return v


def dist(point_a, point_b):
    """compute the absolute distance between to (x,y,z) tuples"""

    x1,y1,z1 = point_a
    x2,y2,z2 = point_b

    return math.sqrt((x2-x1) ** 2 +(y2-y1) ** 2 +(z2-z1) ** 2)


def dot(v1, v2):
    """the dot product of two vectors"""
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x = x1 * x2
    y = y1 * y2
    z = z1 * z2
    return x + y + z


def cross(v1, v2):
    """the cross prodcuct of two vectors"""
    x1, y1, z1 = v1
    x2, y2, z2 = v2

    x = y1 * z2 - z1 * y1
    y = z1 * x2 - x1 * z2
    z = x1 * y2 - y1 * x2
    v = (x, y, z)
    return v


def magnitude(v):
    x, y, z = v
    return math.sqrt( x ** 2 + y ** 2 + z ** 2)


def dist_line_point(l1, l2, p):
    """the shortest distance between a line (l1,l2) and a point"""

    ab = sub_vec(l2, l1)
    ac = sub_vec(p, l1)
    area = magnitude(cross(ab, ac))
    cd = area / magnitude(ab)
    return cd


def dist_line_seg_point(l1, l2, p):
    """the shortest distance between a line segment (l1,l2) and a point"""
    n = sub_vec(l2, l1)
    pa = sub_vec(l1, p)

    c = dot(n, pa)

    # closest point is l1
    if (c > 0.0):
        return dot(pa, pa)

    bp = sub_vec(p, l2)

    # closest point is l2
    if (dot(n, bp) > 0.0):
        return dot(bp, bp)

    # closest point is between l1 and l2
    e = sub_vec(pa, scale_vec(n, (c / dot(n, n))))

    return dot(e, e)

class Object:
    pos = (0, 0, 0)
    vec = (0, 0, 0)
    color = (0, 0, 0)
    size = 0.0
    max_size = 0.1
    alive = True

    def __init__(self, pos=(0,0,0), vec=(0,0,0), color=(0,0,0), size=0.1, ttl=10):
        self.pos = pos
        self.vec = vec
        self.color = color
        self.max_size = size
        self.size = 0.1
        self.ttl = ttl
        self.alive = True

    def move(self, dt):
        if self.alive:
            if self.size < self.max_size:
                self.size += 0.1 * dt
            self.pos = add_vec(self.pos, self.vec, dt)
            self.ttl -= dt
            if self.ttl < 1:
                r,g,b = self.color
                r -= 0.1 * dt
                g -= 0.1 * dt
                b -= 0.1 * dt
                self.color = (r, g, b)

            self.alive = self.ttl > 0

    def draw(self, coord):
        """returns an rgb tuple to add to the current coordinates color"""

        color = self.color
        distance = dist(coord, self.pos)
        (r, g, b) = (0.0, 0.0, 0.0)
        if distance < self.size:
            dot = (1 / (distance + 0.0001))  # + (time.time()*twinkle_speed % 1)
            # dot = abs(dot * 2 - 1)
            dot = color_utils.remap(dot, 0, 10, 0.1, 1.1)
            dot = color_utils.clamp(dot, -0.5, 1.1)
            # dot **=2
            dot = color_utils.clamp(dot, 0.2, 1)
            r = color[0] * dot
            g = color[1] * dot
            b = color[2] * dot
        new_color = (r, g, b)
        return new_color

    def init_random(self, boundary):
        self.random_vec()
        self.random_pos(boundary)
        self.random_color()
        self.random_size()
        self.random_ttl()

    def random_pos(self, boundary):
        """set the position to a random point within the boundary"""
        min_bound, max_bound = boundary
        x = random.uniform(min_bound[0], max_bound[0])
        y = random.uniform(min_bound[1], max_bound[1])
        z = random.uniform(min_bound[2], max_bound[2])
        self.pos = (x, y, z)

    def random_vec(self):
        """set a random movement vector"""
        dx = random.uniform(-0.4, 0.4)
        dy = random.uniform(-0.4, 0.4)
        dz = random.uniform(-0.4, 0.4)
        self.vec = (dx, dy, dz)

    def random_color(self):
        self.color = (random.random(), random.random(), random.random())

    def random_size(self):
        self.size = random.uniform(0.1, 1)

    def random_ttl(self):
        self.ttl = random.uniform(3, 20)

class Ball(Object):
    """a ball"""

class Glider(Object):
    """a line in direction of the vector and size"""

    p2 = (0, 0, 0)
    direction = "x"

    def random_vec(self):
        """set a random movement vector in one of the cardinal axis"""
        self.direction = random.choice(["x", "y", "z"])
        dx, dy, dz = 0.0, 0.0, 0.0
        if self.direction == "x":
            dx = random.uniform(-0.4, 0.4) * 3
        if self.direction == "y":
            dy = random.uniform(-0.4, 0.4) * 3
        if self.direction == "z":
            dz = random.uniform(-0.4, 0.4) * 3
        self.vec = (dx, dy, dz)

    def random_pos(self, boundary):
        """set the position to a random point at the boundary"""
        min_bound, max_bound = boundary
        x, y, z = 0.0, 0.0, 0.0
        if self.direction == "x":
            if self.vec[0] < 0:
                x = max_bound[0]
            else:
                x = min_bound[0]
            y = random.uniform(min_bound[1], max_bound[1])
            z = random.uniform(min_bound[2], max_bound[2])
        if self.direction == "y":
            if self.vec[1] < 0:
                y = max_bound[1]
            else:
                y = min_bound[1]
            x = random.uniform(min_bound[0], max_bound[0])
            z = random.uniform(min_bound[2], max_bound[2])
        if self.direction == "z":
            if self.vec[2] < 0:
                z = max_bound[2]
            else:
                z = min_bound[2]
            x = random.uniform(min_bound[0], max_bound[0])
            y = random.uniform(min_bound[1], max_bound[1])

        self.pos = (x, y, z)

    def move(self, dt):
        Object.move(self, dt)
        self.p2 = add_vec(self.pos, self.vec, -self.size)

    def draw(self, coord):
        """returns an rgb tuple to add to the current coordinates color"""
        color = self.color
        (r, g, b) = (0, 0, 0)
        dist_line = dist_line_point(self.pos, self.p2, coord)
        # only compute further if we are very close to the line already
        if dist_line < 0.08:
            distance = dist_line_seg_point(self.pos, self.p2, coord)

            if distance < self.size:
                dot = (1 / (distance + 0.0001))  # + (time.time()*twinkle_speed % 1)
                # dot = abs(dot * 2 - 1)
                dot = color_utils.remap(dot, 0, 10, 0.1, 1.1)
                dot = color_utils.clamp(dot, -0.5, 1.1)
                # dot **=2
                dot = color_utils.clamp(dot, 0.2, 1)
                r = color[0] * dot
                g = color[1] * dot
                b = color[2] * dot
        new_color = (r, g, b)

        return new_color