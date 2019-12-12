#!/usr/bin/env python3

import sys

import numpy as np

def valid(data, p):
    return p[0] >= 0 and p[0] < data.shape[0] and p[1] >= 0 and p[1] < data.shape[1]

def fourdiffs(distance, d):
    yield (-distance  , -distance+d)
    yield (-distance+d,  distance  )
    yield ( distance  ,  distance-d)
    yield ( distance-d, -distance  )

def analyze(data, location):
    count = 0
    seen = set()

    for distance in range(1, max(data.shape)):
        for d in range(2*distance):
            for diff in fourdiffs(distance, d):
                nextpos = location
                blocked = False
                while True:
                    nextpos = (nextpos[0] + diff[0], nextpos[1] + diff[1])
                    if not valid(data, nextpos) or nextpos in seen:
                        break
                    seen.add(nextpos)
                    if data[nextpos] and not blocked:
                        blocked = True
                        count += 1

    return count

with open(sys.argv[1]) as f:
    data = np.array([[c == '#' for c in l.strip()] for l in f])

maxseen = -1
maxlocation = None

for location, value in np.ndenumerate(data):
    if value:
        seen = analyze(data, location)
        if seen > maxseen:
            maxseen = seen
            maxlocation = location

print('Saw {} asteroids at {}'.format(maxseen, maxlocation))
