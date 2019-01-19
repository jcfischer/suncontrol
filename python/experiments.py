#!/usr/bin/env python

"""A demo client for Open Pixel Control
http://github.com/zestyping/openpixelcontrol

Creates moving stripes visualizing the x, y, and z coordinates
mapped to r, g, and b, respectively.  Also draws a moving white
spot which shows the order of the pixels in the layout file.

To run:
First start the gl simulator using, for example, the included "wall" layout

    make
    bin/gl_server layouts/wall.json

Then run this script in another shell to send colors to the simulator

    python_clients/spatial_stripes.py --layout layouts/wall.json

"""

from __future__ import division
import time
import sys
import optparse
import random
import objects

try:
    import json
except ImportError:
    import simplejson as json

import opc
import color_utils


#-------------------------------------------------------------------------------
# command line

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout',
                    action='store', type='string',
                    help='layout file')
parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890',
                    action='store', type='string',
                    help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=20,
                    action='store', type='int',
                    help='frames per second')

options, args = parser.parse_args()

if not options.layout:
    parser.print_help()
    print()
    print('ERROR: you must specify a layout file using --layout')
    print()
    sys.exit(1)


#-------------------------------------------------------------------------------
# parse layout file

print
print('    parsing layout file')
print

coordinates = []
for item in json.load(open(options.layout)):
    print(item)
    if item and 'point' in item:
        coordinates.append(tuple(item['point']))


#-------------------------------------------------------------------------------
# connect to server

client = opc.Client(options.server)
if client.can_connect():
    print('    connected to %s' % options.server)
else:
    # can't connect, but keep running in case the server appears later
    print('    WARNING: could not connect to %s' % options.server)
print


#-------------------------------------------------------------------------------




def update_world(t, world):
    """updates the world
    t: time in seonds since world started
    world: list of objects
    """
    last_time = world["time"]
    delta_t = t - last_time
    objs = world["objects"]
    new_world = {}

    for obj in objs:
        obj.move(delta_t)

    new_objects = list(filter(lambda x : x.alive, objs))
    if random.random() > 0.98:
        new_object = objects.Ball()
        new_object.init_random(world["boundary"])
        new_objects.append(new_object)

    if random.random() > 0.98:
        new_object = objects.Glider()
        new_object.init_random(world["boundary"])
        new_objects.append(new_object)

    new_world["time"] = t
    new_world["objects"] = new_objects
    new_world["boundary"] = world["boundary"]
    return new_world



# color function

def pixel_color(t, coord, ii, n_pixels, world, bound):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    world: information about the world outside
    bound: two tuples that hold the min and max coordinates of the display

    Returns an (r, g, b) tuple in the range 0-255

    """
    min_coord, max_coord = bound
    min_x, min_y, min_z = min_coord
    max_x, max_y, max_z = max_coord


    x, y, z = coord
    r = 0.0
    g = 0.0
    b = 0.0

    objects = world["objects"]
    for obj in objects:
        dr, dg, db = obj.draw(coord)
        r += dr
        g += dg
        b += db



    # apply gamma curve
    # only do this on live leds, not in the simulator
    r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r*128, g*128, b*128)


#-------------------------------------------------------------------------------
# send pixels

print('    sending pixels forever (control-c to exit)...')
print

n_pixels = len(coordinates)
random_values = [random.random() for ii in range(n_pixels)]
start_time = time.time()

min_x = 0.0
max_x = 0.0
min_y = 0.0
max_y = 0.0
min_z = 0.0
max_z = 0.0

for coord in coordinates:
    x,y,z = coord
    min_x = min(x, min_x)
    min_y = min(y, min_y)
    min_z = min(z, min_z)
    max_x = max(x, max_x)
    max_y = max(y, max_y)
    max_z = max(z, max_z)

min_coord = (min_x, min_y, min_z)
max_coord = (max_x, max_y, max_z)
bound = (min_coord, max_coord)

red_ball = objects.Ball((0, 0, 0), (0.0, 0, -0.0), (1, 0, 0), 0.3, 20)
blue_ball = objects.Ball((2, 0, 0), (-0.3, 0, 0.05), (0, 0, 1), 0.4, 20)
green_ball = objects.Ball((0, 0, 0), (-0.02, 0, 0.1), (0, 1, 0), 0.5, 20)
glider = objects.Glider((min_x, 0, max_z), (1.5, 0, 0), (0.8, 0.8, 0.8), 0.2, 4)

world = {"time": 0,
         "boundary": bound,
         "objects": [red_ball]}

while True:
    t = time.time() - start_time
    world = update_world(t, world)
    pixels = [pixel_color(t, coord, ii, n_pixels, world, bound) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    time.sleep(1 / options.fps)

