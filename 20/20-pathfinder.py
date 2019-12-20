#!/usr/bin/env python3

import collections
import heapq
import sys

import numpy as np

MOVES = [(0, 1), (-1, 0), (0, -1), (1, 0)]

with open(sys.argv[1]) as f:
    grid = np.array([[c for c in row if c != '\n'] for row in f])

# Find portal locations and names

portal_locations = {True: {}, False: {}}
all_portal_locations = frozenset()

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
            # Top or left outer edge
            portal_location = (pos[0] + 2 * step[0], pos[1] + 2 * step[1])
            portal_is_outer = True
        elif pos[axis] == grid.shape[axis] - 2:
            # Bottom or right outer edge
            portal_location = (pos[0] - step[0], pos[1] - step[1])
            portal_is_outer = True
        elif pos[axis] < grid.shape[axis] / 2:
            # Top or left inner edge
            portal_location = (pos[0] - step[0], pos[1] - step[1])
            portal_is_outer = False
        else:
            # Bottom or right inner edge
            portal_location = (pos[0] + 2 * step[0], pos[1] + 2 * step[1])
            portal_is_outer = False

        portal_locations[portal_is_outer][portal_name] = portal_location
        all_portal_locations = all_portal_locations | {portal_location}

start_location = portal_locations[True]['AA']
end_location = portal_locations[True]['ZZ']

portals = {}
for portal_name, outer_location in portal_locations[False].items():
    inner_location = portal_locations[True][portal_name]
    portals[outer_location] = inner_location
    portals[inner_location] = outer_location

# Step 1 - BFS searches to find which portals are directly connected to others

portal_distances = collections.defaultdict(dict)
for start_pos in all_portal_locations:
    states = [(start_pos, 0)]
    seen = {start_pos}

    while states:
        pos, distance = states.pop(0)

        for move in MOVES:
            next_pos = (pos[0] + move[0], pos[1] + move[1])

            if next_pos in seen:
                continue

            if grid[next_pos] == '.':
                if next_pos in all_portal_locations:
                    portal_distances[start_pos][next_pos] = distance + 1
                states.append((next_pos, distance + 1))
                seen = seen | {next_pos}

# Step 2 - Djikstra to find the shortest route from entrace to exit

states = [(0, start_location)]
min_distances = {start_location: 0}
min_solution = None

while states:
    distance, pos = heapq.heappop(states)

    if min_solution and distance >= min_solution:
        # Already found a solution smaller than this, we can stop now
        break

    if pos in min_distances and distance > min_distances[pos]:
        # Already been to this spot with a shorter distance so ignore this
        continue

    for next_pos, steps in portal_distances[pos].items():
        next_distance = distance + steps

        if next_pos == end_location:
            if not min_solution or next_distance < min_solution:
                min_solution = next_distance
        elif next_pos == start_location:
            # Do nothing
            pass
        else:
            portal_end = portals[next_pos]
            next_distance += 1
            if portal_end not in min_distances or next_distance < min_distances[portal_end]:
                heapq.heappush(states, (next_distance, portal_end))
                min_distances[portal_end] = next_distance

print('Quickest solution in {} steps'.format(min_solution))
print('States seen: {}'.format(len(min_distances)))
