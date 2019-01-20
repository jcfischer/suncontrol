"""Helper functions to make vector manipulations easier."""

import math

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