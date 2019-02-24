"""Classes to define world objects"""

import random
import math_utils
import color_utils


class Object:
    pos = (0, 0, 0)
    vec = (0, 0, 0)
    color = (0, 0, 0)
    size = 0.0
    max_size = 0.1
    alive = True

    def __init__(self, pos=(0, 0, 0), vec=(0, 0, 0), color=(0, 0, 0), size=0.1, ttl=10):
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
            self.pos = math_utils.add_vec(self.pos, self.vec, dt)
            self.ttl -= dt
            if self.ttl < 1:
                r, g, b = self.color
                r -= 0.1 * dt
                g -= 0.1 * dt
                b -= 0.1 * dt
                self.color = (r, g, b)

            self.alive = self.ttl > 0

    def draw(self, coord):
        """returns an rgb tuple to add to the current coordinates color"""

        color = self.color
        distance = math_utils.dist(coord, self.pos)
        (r, g, b) = (0.0, 0.0, 0.0)
        if distance < self.size + 0.1:
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
        self.size = random.uniform(0.1, 0.5)

    def random_ttl(self):
        self.ttl = random.uniform(3, 20)


class Ball(Object):
    """a ball"""


class Color(Object):
    """a solid color that fades in and out over its ttl"""

    def move(self, dt):
        if self.alive:
            self.ttl -= dt
            if self.ttl < 1:
                r, g, b = self.color
                r -= 0.1 * dt
                g -= 0.1 * dt
                b -= 0.1 * dt
                self.color = (r, g, b)
        self.alive = self.ttl > 0

    def draw(self, coord):
        return self.color

    def random_color(self):
        self.color = (random.random()/2.0, random.random()/2.0, random.random()/2.0)
        print(self.color)


class Grower(Object):
    """a ball that grows and fades as it gets too big"""

    growing = True

    def random_vec(self):
        self.vec = (0, 0, 0)

    def move(self, dt):
        if self.alive:
            if self.growing:
                if self.size < self.max_size:
                    self.size += 0.3 * dt
                else:
                    self.growing = False
            else:
                if self.size > 0.05:
                    self.size -= 0.3 * dt
                else:
                    self.growing = True

            self.ttl -= dt
            if self.ttl < 1:
                r, g, b = self.color
                r -= 0.1 * dt
                g -= 0.1 * dt
                b -= 0.1 * dt
                self.color = (r, g, b)

            self.alive = self.ttl > 0


class Ring(Grower):
    """a ring that expands"""

    speed = 0.8

    def random_size(self):
        self.max_size = random.uniform(0.4, 1)
        self.size = 0.05

    def move(self, dt):
        if self.alive:
            self.size += self.speed * dt
            self.speed -= dt / 5
            self.ttl -= dt
            if self.ttl < 1:
                r, g, b = self.color
                r -= 0.1 * dt
                g -= 0.1 * dt
                b -= 0.1 * dt
                self.color = (r, g, b)

            self.alive = self.ttl > 0

    def draw(self, coord):
        """returns an rgb tuple to add to the current coordinates color"""

        color = self.color
        distance = math_utils.dist(coord, self.pos)
        (r, g, b) = (0.0, 0.0, 0.0)
        if (distance > self.size - 0.07) and (distance < self.size + 0.07):
            dot = 0.8
            # # dot = abs(dot * 2 - 1)
            # dot = color_utils.remap(dot, 0, 10, 0.1, 1.1)
            # dot = color_utils.clamp(dot, -0.5, 1.1)
            # # dot **=2
            # dot = color_utils.clamp(dot, 0.2, 1)
            r = color[0] * dot
            g = color[1] * dot
            b = color[2] * dot
        new_color = (r, g, b)
        return new_color


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
        self.p2 = math_utils.add_vec(self.pos, self.vec, -self.size)

    def draw(self, coord):
        """returns an rgb tuple to add to the current coordinates color"""
        color = self.color
        (r, g, b) = (0, 0, 0)
        dist_line = math_utils.dist_line_point(self.pos, self.p2, coord)
        # only compute further if we are very close to the line already
        if dist_line < 0.08:
            distance = math_utils.dist_line_seg_point(self.pos, self.p2, coord)

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
