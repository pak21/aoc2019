#!/usr/bin/env python3

import math
import sys

import numpy as np

def ordering(p, laser_location):
    if p == laser_location:
        return (1000, 0) # Invalid angle so can be ignored later

    dy = laser_location[0] - p[0]
    dx = p[1] - laser_location[1]

    angle = math.pi / 2 - math.atan2(dy, dx)
    if angle < 0:
        angle += 2 * math.pi
    elif angle > 2 * math.pi:
        angle -= 2 * math.pi

    distance = abs(dy) + abs(dx)

    return (angle, distance)

def valid(data, p):
    return p[0] >= 0 and p[0] < data.shape[0] and p[1] >= 0 and p[1] < data.shape[1]

with open(sys.argv[1]) as f:
    data = np.array([[c == '#' for c in l.strip()] for l in f])

laser = (int(sys.argv[2]), int(sys.argv[3]))

foo = []
for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        o = ordering((y, x), laser)
        foo.append((*o, (y, x)))

foo = sorted([f for f in foo if f[0] != 1000])

total = np.sum(data) - 1

last_vaporized_angle = None
next_index = 0
vaporized = 0

while True:
    angle, distance, location = foo[next_index]
    if data[location]:
        vaporized += 1
        last_vaporized_angle = angle
        print('Vaporizing asteroid {} at {}, angle {}'.format(vaporized, location, angle))
        data[location] = False

        if vaporized == total:
            break

        # Move to next angle
        while foo[next_index][0] == last_vaporized_angle:
            next_index = (next_index + 1) % len(foo)
    else:
        next_index = (next_index + 1) % len(foo)
