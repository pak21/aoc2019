#!/usr/bin/env python3

import sys

DIRECTIONS = {
    'R': (1, 0),
    'U': (0, 1),
    'L': (-1, 0),
    'D': (0, -1)
}


with open(sys.argv[1]) as f:
    moves = f.readline().split(',')
    moves2 = f.readline().split(',')

loc = (0, 0)
seen = {}
count = 0
for move in moves:
    direction = move[0]
    distance = int(move[1:])

    for i in range(distance):
        count += 1
        step = DIRECTIONS[direction]
        loc = (loc[0] + step[0], loc[1] + step[1])
        if loc not in seen:
            seen[loc] = (count, None)

loc = (0, 0)
count = 0
for move in moves2:
    direction = move[0]
    distance = int(move[1:])

    for i in range(distance):
        count += 1
        step = DIRECTIONS[direction]
        loc = (loc[0] + step[0], loc[1] + step[1])
        if loc in seen:
            seen[loc] = (seen[loc][0], count)

min_time = None
for k, v in seen.items():
    if v[1] is None:
        continue

    time = v[0] + v[1]
    if not min_time or time < min_time:
        min_time = time

    print(v, time)

print(min_time)
