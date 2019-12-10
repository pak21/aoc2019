#!/usr/bin/env python3

import sys

import numpy as np

def valid(data, p):
    return p[0] >= 0 and p[0] < data.shape[0] and p[1] >= 0 and p[1] < data.shape[1]

def fourdiffs(location, distance, d):
    yield (-distance  , -distance+d)
    yield (-distance+d,  distance  )
    yield ( distance  ,  distance-d)
    yield ( distance-d, -distance  )

def analyze(data, location):
    if not data[location]:
        return 0

    count = 0
    seen = set()

    for distance in range(1, max(data.shape)):
        for d in range(2*distance):
            for diff in fourdiffs(location, distance, d):
                nextpos = location
                blocked = False
                while True:
                    nextpos = (nextpos[0] + diff[0], nextpos[1] + diff[1])
                    if not valid(data, nextpos):
                        break
                    if nextpos in seen:
                        break
                    seen.add(nextpos)
                    if data[nextpos]:
                        if not blocked:
#                            print('Seen at {}'.format(nextpos))
                            blocked = True
                            count += 1
                        else:
#                            print('Blocked at {}'.format(nextpos))
                            pass

    return count

with open(sys.argv[1]) as f:
    data = np.array([[c == '#' for c in l.strip()] for l in f])

maxseen = 0
for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        seen = analyze(data, (y, x))
        if seen > maxseen:
            print('Saw {} asteroids at {}'.format(seen, (y, x)))
            maxseen = seen
