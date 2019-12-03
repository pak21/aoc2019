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
seen = set()
for move in moves:
    direction = move[0]
    distance = int(move[1:])

    for i in range(distance):
        step = DIRECTIONS[direction]
        loc = (loc[0] + step[0], loc[1] + step[1])
        seen.add(loc)

loc = (0, 0)
min_distance = None
for move in moves2:
    direction = move[0]
    distance = int(move[1:])

    for i in range(distance):
        step = DIRECTIONS[direction]
        loc = (loc[0] + step[0], loc[1] + step[1])
        if loc in seen:
            distance = abs(loc[0]) + abs(loc[1])
            print('Crossing at {}, distance = {}'.format(loc, distance))
            if not min_distance or distance < min_distance:
                min_distance = distance

print(min_distance)
