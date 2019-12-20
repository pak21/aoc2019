#!/usr/bin/env python3

import os
import sys

import numpy as np

sys.path.append(os.path.join('..', 'intcode'))

import intcode

SHIP_SIZE = 100

LOW_START = 0.65
HIGH_START = 0.82

def get_left_right(y, memory):
    # Find left edge
    x = int(y * LOW_START)
    while True:
        program = intcode.Program(memory, input_values=[x, y])
        program.run()
        if program.outputs[0]:
            left = x
            break
        x += 1

    # Find right edge
    x = int(y * HIGH_START)
    while True:
        program = intcode.Program(memory, input_values=[x, y])
        program.run()
        if not program.outputs[0]:
            right = x - 1
            break
        x += 1

    return left, right

with open(sys.argv[1]) as f:
    line = f.readline().strip()
    memory = [int(x) for x in line.split(',')]

for value in range(930, 950):
    top = get_left_right(value, memory)
    bottom = get_left_right(value+SHIP_SIZE-1, memory)

    good = bottom[0] + SHIP_SIZE - 1 <= top[1]
    if good:
        print(10000 * bottom[0] + value)
        break
