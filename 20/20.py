#!/usr/bin/env python3

import sys

import numpy as np

MOVES = [(0, 1), (-1, 0), (0, -1), (1, 0)]

with open(sys.argv[1]) as f:
    grid = np.array([[c for c in row if c != '\n'] for row in f])

# Find portal locations and names

portal_locations = {True: {}, False: {}}

for pos, c in np.ndenumerate(grid):
    if pos[0] == grid.shape[0]-1 or pos[1] == grid.shape[1]-1:
        continue
    if not c.isupper():
        continue
    for step in [(1, 0), (0, 1)]:
        next_pos = (pos[0] + step[0], pos[1] + step[1])
        next_c = grid[next_pos]
        if not next_c.isupper():
            continue
        portal_name = c + next_c
        axis = 0 if step == (1, 0) else 1
        if pos[axis] == 0:
            portal_location = (pos[0] + 2 * step[0], pos[1] + 2 * step[1])
            portal_is_outer = True
        elif pos[axis] == grid.shape[axis] - 2:
            portal_location = (pos[0] - step[0], pos[1] - step[1])
            portal_is_outer = True
        elif pos[axis] < grid.shape[axis] / 2:
            portal_location = (pos[0] - step[0], pos[1] - step[1])
            portal_is_outer = False
        else:
            portal_location = (pos[0] + 2 * step[0], pos[1] + 2 * step[1])
            portal_is_outer = False

        if portal_name == 'AA':
            start_location = portal_location
        elif portal_name == 'ZZ':
            end_location = portal_location
        else:
            portal_locations[portal_is_outer][portal_name] = portal_location

portals = {}
for portal_name, outer_location in portal_locations[True].items():
    inner_location = portal_locations[False][portal_name]
    portals[outer_location] = inner_location
    portals[inner_location] = outer_location

states = [(start_location, 0)]
seen = {start_location}

while states:
    pos, distance = states.pop(0)
    for move in MOVES:
        new_pos = (pos[0] + move[0], pos[1] + move[1])

        if new_pos in seen:
            continue

        if new_pos == end_location:
            print('Reached {} in {} steps'.format(end_location, distance + 1))
            sys.exit(1)

        if new_pos in portals:
            seen = seen | {new_pos}
            new_pos = portals[new_pos]
            seen = seen | {new_pos}
            states.append((new_pos, distance + 2))
        elif grid[new_pos] == '.':
            seen = seen | {new_pos}
            states.append((new_pos, distance + 1))
