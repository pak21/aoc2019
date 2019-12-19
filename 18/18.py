#!/usr/bin/env python3

import heapq
import re
import sys

import numpy as np

MOVES = [(0, 1), (-1, 0), (0, -1), (1, 0)]

def find_shortest_path(grid, start, end):
    seen = set(start)
    states = [(start, 0, set())]
    while True:
        pos, distance, doors = states.pop(0)
        for move in MOVES:
            next_pos = (pos[0] + move[0], pos[1] + move[1])
            if next_pos in seen:
                continue
            next_char = grid[next_pos]
            if next_char == '#':
                continue
            elif next_char.isupper():
                doors = doors | {next_char.lower()}

            if next_pos == end:
                return (distance + 1, doors)

            states.append((next_pos, distance + 1, doors))
            seen.add(next_pos)

with open(sys.argv[1]) as f:
    grid = np.array([[c for c in line.strip()] for line in f])

print('Read grid {}'.format(grid.shape))

locations = {c: index for index, c in np.ndenumerate(grid) if c != '#' and c != '.' and not c.isupper()}

print('Found locations ({})'.format(len(locations)))

distances = {(obj1, obj2): find_shortest_path(grid, pos1, pos2) for obj1, pos1 in locations.items() for obj2, pos2 in locations.items() if obj1 < obj2}
distances = {**distances, **{(obj2, obj1): v for (obj1, obj2), v in distances.items()}}

print('Found all distances ({})'.format(len(distances)))

to_collect = frozenset([key for key in locations.keys() if key != '@'])
min_distance = None

start_node = ('@', to_collect)
initial_state = (0, start_node)
min_seen = {start_node: 0}

states = [initial_state]
while states:
    old_state = heapq.heappop(states)
    total_distance, node = old_state

    if min_distance and total_distance >= min_distance:
        break

    if node in min_seen and total_distance > min_seen[node]:
        continue

    current_pos, needed = node
    collected = to_collect - needed

    for next_key in needed:
        distance, doors = distances[(current_pos, next_key)]

        if doors <= collected:
            new_needed = needed - {next_key}
            new_distance = total_distance + distance

            if new_needed:
                next_node = (next_key, new_needed)
                if next_node not in min_seen or new_distance < min_seen[next_node]:
                    heapq.heappush(states, (new_distance, next_node))
                    min_seen[next_node] = new_distance
            elif not min_distance or new_distance < min_distance:
                print('Solved in {} steps'.format(new_distance))
                min_distance = new_distance

print('Min distance', min_distance)
