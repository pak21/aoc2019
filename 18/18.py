#!/usr/bin/env python3

import heapq
import re
import sys

import numpy as np

MOVES = [(0, 1), (-1, 0), (0, -1), (1, 0)]

def parse_trace(trace):
    doors = set([d for d in re.sub(r'[^A-Z]', '', trace)])
    return (len(trace), doors)

def find_shortest_path(grid, start, end):
    seen = set(start)
    states = [(start, '')]
    while True:
        pos, trace = states.pop(0)
        for move in MOVES:
            next_pos = (pos[0] + move[0], pos[1] + move[1])
            if next_pos in seen:
                continue
            if grid[next_pos] == '#':
                continue
            seen.add(next_pos)
            next_trace = trace + grid[next_pos]
            if next_pos == end:
                return parse_trace(next_trace)
            states.append((next_pos, next_trace))

with open(sys.argv[1]) as f:
    grid = np.array([[c for c in line.strip()] for line in f])

print('Read grid')

locations = {c: index for index, c in np.ndenumerate(grid) if c != '#' and c != '.'}

print('Found locations')

traces = {}
for obj1, pos1 in locations.items():
    for obj2, pos2 in locations.items():
        if obj1 >= obj2:
            continue
        if obj1.isupper() or obj2.isupper():
            continue
        if (obj1, obj2) in traces:
            continue
        path = find_shortest_path(grid, pos1, pos2)
        traces[(obj1, obj2)] = path

print('Found all traces')

to_collect = set([key for key in locations.keys() if key.islower()])
min_distance = None

def make_key(state):
    return state[1] + ''.join(sorted(list(state[2])))

initial_state = (0, '@', set(), to_collect)
states = [initial_state]
min_seen = {make_key(initial_state): 0}

heapq.heapify(states)

while states:
    old_state = heapq.heappop(states)
    old_key = make_key(old_state)
    total_distance, current_pos, collected, needed = old_state

    if min_distance and total_distance >= min_distance:
        break

    if old_key in min_seen and total_distance > min_seen[old_key]:
        continue

#    print('At {}, collected {}, needed {}, total distance {}'.format(current_pos, collected, needed, total_distance))
    for next_key in needed:

        trace_key = (current_pos, next_key) if current_pos < next_key else (next_key, current_pos)
        distance, doors = traces[trace_key]
        blocked = doors - collected
        if not blocked:
#            print('  Could move from {} to {} through {} -> {}'.format(current_pos, next_key, doors, blocked))
            new_collected = collected | set(next_key.upper())
            new_needed = needed - set(next_key)
            new_distance = total_distance + distance
            new_state = (new_distance, next_key, new_collected, new_needed)

            if new_needed:
                new_key = make_key(new_state)
                if new_key not in min_seen or new_distance < min_seen[new_key]:
                    min_seen[new_key] = new_distance
                    heapq.heappush(states, new_state)
            else:
                if not min_distance or new_distance < min_distance:
                    print('Solved in {} steps'.format(new_distance))
                    min_distance = new_distance

print('Min distance', min_distance)
