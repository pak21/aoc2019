#!/usr/bin/env python3

import math
import sys

import numpy as np

def ordering(p, laser_location):
    dy = laser_location[0] - p[0]
    dx = p[1] - laser_location[1]

    angle = (math.pi / 2 - math.atan2(dy, dx)) % (2 * math.pi)
    distance = abs(dy) + abs(dx)

    return (angle, distance, p)

def valid(data, p):
    return p[0] >= 0 and p[0] < data.shape[0] and p[1] >= 0 and p[1] < data.shape[1]

with open(sys.argv[1]) as f:
    data = np.array([[c == '#' for c in l.strip()] for l in f])

laser = (int(sys.argv[2]), int(sys.argv[3]))

ordered_positions = sorted([ordering(location, laser) for location in np.ndindex(data.shape) if location != laser])

last_vaporized_angle = None
next_index = 0
vaporized = 0

while True:
    angle, distance, location = ordered_positions[next_index]
    if data[location]:
        vaporized += 1
        if vaporized == 200:
            print('Vaporizing asteroid {} at {} -> {}'.format(vaporized, location, 100 * location[1] + location[0]))
            break
        last_vaporized_angle = angle
        data[location] = False

        # Move to next angle
        while ordered_positions[next_index][0] == last_vaporized_angle:
            next_index = (next_index + 1) % len(ordered_positions)
    else:
        next_index = (next_index + 1) % len(ordered_positions)
