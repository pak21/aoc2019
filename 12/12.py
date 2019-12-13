#!/usr/bin/env python3

import re
import sys

import numpy as np

with open(sys.argv[1]) as f:
    pos = np.array([[int(n) for n in re.match(r'<x=(-?[\d]+), y=(-?[\d]+), z=(-?[\d]+)>', line).groups()] for line in f])

vel = np.zeros(pos.shape, dtype=np.int)

steps = int(sys.argv[2])

for step in range(steps):
    for moon1 in range(pos.shape[0]):
        for moon2 in range(moon1 + 1, pos.shape[0]):
            pos_diff = pos[moon2,:] - pos[moon1,:]
            pos_sign = np.sign(pos_diff)
            vel[moon1,:] += pos_sign
            vel[moon2,:] -= pos_sign
    pos += vel

potential = np.sum(np.abs(pos), axis=1)
kinetic = np.sum(np.abs(vel), axis=1)

print(np.dot(potential, kinetic))
