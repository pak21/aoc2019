#!/usr/bin/env python3

import re
import sys

import numpy as np

with open(sys.argv[1]) as f:
    pos = np.array([[int(n) for n in re.match(r'<x=(-?[\d]+), y=(-?[\d]+), z=(-?[\d]+)>', line).groups()] for line in f])

vel = np.zeros(pos.shape, dtype=np.int)

n_moons, n_axes = pos.shape

initial_state = [tuple(np.hstack((pos[:,i], vel[:,i]))) for i in range(n_axes)]
period = [None] * n_axes
found = 0

step = 0
while found < n_axes:
    for moon1 in range(n_moons):
        for moon2 in range(moon1 + 1, n_moons):
            pos_diff = pos[moon2,:] - pos[moon1,:]
            pos_sign = np.sign(pos_diff)
            vel[moon1,:] += pos_sign
            vel[moon2,:] -= pos_sign
    pos += vel

    step += 1

    for i in range(n_axes):
        if period[i]:
            continue
        axis_state = tuple(np.hstack((pos[:,i], vel[:,i])))
        if axis_state == initial_state[i]:
            print('Axis {} state repeated at {}'.format(i, step))
            period[i] = step
            found += 1

print('All axes will repeat at time {}'.format(np.lcm.reduce(period)))
