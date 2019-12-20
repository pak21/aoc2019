#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.join('..', 'intcode'))

import intcode

SIZE=50

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

locations = [(x, y) for x in range(SIZE) for y in range(SIZE)]

count = 0
for location in locations:
    program = intcode.Program(memory, input_values=location)
    program.run()
    if program.outputs[0]:
        count += 1

print(count)
