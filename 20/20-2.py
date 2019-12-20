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

states = [(start_location, 0, 0)]
seen = {(start_location, 0)}

def is_outer_portal(pos, grid):
    return pos[0] == 2 or pos[1] == 2 or pos[0] == grid.shape[0] - 3 or pos[1] == grid.shape[1] - 3

while states:
    pos, level, distance = states.pop(0)

    # If we're at a portal, move to the other end of the portal
    jumping = False
    if pos in portals and not(level == 0 and is_outer_portal(pos, grid)):
        new_pos = portals[pos]
        level_change = -1 if is_outer_portal(pos, grid) else 1
        new_level = level + level_change
        if (new_pos, new_level) not in seen:
            print('Jumping from {} after {} steps, state queue is {}, seen is {}'.format((pos, level), distance, len(states), len(seen)))
            seen = seen | {(new_pos, new_level)}
            if new_level < 30:
                states.append((new_pos, new_level, distance + 1))
            jumping = True
    
    if not jumping:
        for move in MOVES:
            new_pos = (pos[0] + move[0], pos[1] + move[1])

            if (new_pos, level) in seen:
                continue

            if level == 0 and new_pos == end_location:
                print('Reached {} in {} steps'.format(end_location, distance + 1))
                sys.exit(1)

            if grid[new_pos] == '.':
                seen = seen | {(new_pos, level)}
                states.append((new_pos, level, distance + 1))
